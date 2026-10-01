"""
Report Indexer - Scans and indexes markdown reports from OpenClaw
"""
import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

DEFAULT_REPORTS_DIR = os.environ.get("OPENCLAW_REPORTS_DIR", "/home/dg/openclaw-reports")


class ReportIndexer:
    def __init__(self, reports_dir: str = None):
        self.reports_dir = Path(reports_dir or DEFAULT_REPORTS_DIR)
        self._index = []
        self._content_cache = {}
    
    def scan_reports(self) -> List[Dict]:
        """Recursively scan for markdown reports"""
        self._index = []
        
        if not self.reports_dir.exists():
            return self._index
        
        for md_file in self.reports_dir.rglob("*.md"):
            try:
                stat = md_file.stat()
                
                # Extract metadata from filename
                filename = md_file.name
                relative_path = md_file.relative_to(self.reports_dir)
                
                # Determine report type from path/filename
                report_type = self._classify_report(str(relative_path))
                
                self._index.append({
                    'filename': filename,
                    'path': str(md_file),
                    'relative_path': str(relative_path),
                    'folder': str(relative_path.parent),
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime),
                    'type': report_type,
                    'safe_id': self._safe_filename(str(relative_path))
                })
            except Exception as e:
                print(f"Error indexing {md_file}: {e}")
                continue
        
        # Sort by modification time (newest first)
        self._index.sort(key=lambda x: x['modified'], reverse=True)
        return self._index
    
    def _classify_report(self, path: str) -> str:
        """Classify report type based on path/filename"""
        path_lower = path.lower()
        
        if 'daily-brief' in path_lower:
            return 'Daily Brief'
        elif 'mika' in path_lower and 'executive' in path_lower:
            return 'Executive Summary'
        elif 'mika' in path_lower:
            return 'Country Report'
        elif 'twitter' in path_lower:
            return 'Twitter Digest'
        elif 'structured' in path_lower:
            return 'Structured Data'
        else:
            return 'Other'
    
    def _safe_filename(self, path: str) -> str:
        """Create safe identifier from path"""
        return re.sub(r'[^a-zA-Z0-9_-]', '_', path)
    
    def get_report(self, safe_id: str) -> Optional[Dict]:
        """Get report by safe ID"""
        for report in self._index:
            if report['safe_id'] == safe_id:
                return report
        return None
    
    def read_content(self, file_path: str) -> str:
        """Read markdown content from file"""
        if file_path in self._content_cache:
            return self._content_cache[file_path]
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self._content_cache[file_path] = content
                return content
        except Exception as e:
            return f"Error reading file: {e}"
    
    def search(self, query: str) -> List[Dict]:
        """Search reports by filename or content"""
        if not query:
            return self._index
        
        query_lower = query.lower()
        results = []
        
        for report in self._index:
            # Search in filename
            if query_lower in report['filename'].lower():
                results.append({**report, 'match_type': 'filename'})
                continue
            
            # Search in folder path
            if query_lower in report['folder'].lower():
                results.append({**report, 'match_type': 'path'})
                continue
            
            # Search in content (expensive, so do last)
            content = self.read_content(report['path'])
            if query_lower in content.lower():
                # Find context snippet
                idx = content.lower().find(query_lower)
                start = max(0, idx - 50)
                end = min(len(content), idx + 100)
                snippet = content[start:end].replace('\n', ' ')
                
                results.append({
                    **report,
                    'match_type': 'content',
                    'snippet': f"...{snippet}..."
                })
        
        return results
    
    def get_stats(self) -> Dict:
        """Get statistics about indexed reports"""
        if not self._index:
            return {}
        
        total_size = sum(r['size'] for r in self._index)
        types = {}
        for r in self._index:
            types[r['type']] = types.get(r['type'], 0) + 1
        
        return {
            'total_reports': len(self._index),
            'total_size_mb': round(total_size / 1024 / 1024, 2),
            'by_type': types,
            'oldest': min(r['modified'] for r in self._index),
            'newest': max(r['modified'] for r in self._index)
        }
