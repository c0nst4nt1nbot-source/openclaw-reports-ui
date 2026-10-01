"""
Markdown Renderer - Converts markdown to HTML with syntax highlighting
"""
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.toc import TocExtension


class MarkdownRenderer:
    def __init__(self):
        self.md = markdown.Markdown(
            extensions=[
                'extra',
                'codehilite',
                'fenced_code',
                'tables',
                'toc',
                'nl2br',
                'sane_lists'
            ],
            extension_configs={
                'codehilite': {
                    'css_class': 'highlight',
                    'linenums': False
                }
            }
        )
    
    def render(self, content: str) -> str:
        """Render markdown to HTML"""
        # Reset the markdown instance
        self.md.reset()
        
        # Convert to HTML
        html = self.md.convert(content)
        
        return html
    
    def extract_title(self, content: str) -> str:
        """Extract title from markdown (first H1)"""
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                return line[2:].strip()
        return "Untitled Report"
