#!/usr/bin/env python3
"""
OpenClaw Reports UI - Local Web Interface
Lightweight Flask app for browsing reports and querying intelligence database
"""
import os
from flask import Flask, render_template, request, jsonify, abort
from modules.report_indexer import ReportIndexer
from modules.markdown_renderer import MarkdownRenderer
from modules.db_browser import DatabaseBrowser

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-me')
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Initialize modules
indexer = ReportIndexer()
renderer = MarkdownRenderer()
db_browser = DatabaseBrowser()

# Scan reports on startup
print("Scanning reports...")
indexer.scan_reports()
print(f"Found {len(indexer._index)} reports")


@app.route('/')
def index():
    """Home page with overview"""
    indexer.scan_reports()
    report_stats = indexer.get_stats()
    db_stats = db_browser.get_db_stats()
    
    # Get latest reports
    latest_reports = indexer._index[:10]
    
    return render_template('index.html',
                          report_stats=report_stats,
                          db_stats=db_stats,
                          latest_reports=latest_reports)


@app.route('/reports')
def reports():
    """List all reports with search and filtering"""
    indexer.scan_reports()
    query = request.args.get('q', '')
    report_type = request.args.get('type', '')
    
    # Get reports
    if query:
        results = indexer.search(query)
    else:
        results = indexer._index
    
    # Filter by type
    if report_type:
        results = [r for r in results if r['type'] == report_type]
    
    # Get unique types for filter dropdown
    all_types = sorted(set(r['type'] for r in indexer._index))
    
    return render_template('reports.html',
                          reports=results,
                          query=query,
                          report_type=report_type,
                          all_types=all_types)


@app.route('/reports/<safe_id>')
def view_report(safe_id):
    """View individual report"""
    if not indexer.get_report(safe_id):
        indexer.scan_reports()
    report = indexer.get_report(safe_id)
    
    if not report:
        abort(404)
    
    # Read and render content
    content = indexer.read_content(report['path'])
    html_content = renderer.render(content)
    title = renderer.extract_title(content)
    
    return render_template('report_view.html',
                          report=report,
                          title=title,
                          content=html_content)


@app.route('/api/reports/refresh')
def refresh_reports():
    """API endpoint to refresh report index"""
    indexer.scan_reports()
    return jsonify({
        'status': 'success',
        'count': len(indexer._index)
    })


@app.route('/database')
def database():
    """Database explorer home"""
    tables = db_browser.get_tables()
    db_stats = db_browser.get_db_stats()
    
    # Separate tables and views
    table_info = []
    for table in tables:
        info = db_browser.get_table_info(table)
        table_info.append(info)
    
    return render_template('database.html',
                          tables=table_info,
                          db_stats=db_stats)


@app.route('/database/<table_name>')
def view_table(table_name):
    """View table contents with pagination"""
    # Get pagination parameters
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    offset = (page - 1) * per_page
    
    # Get filter parameters
    filters = {}
    for key in request.args:
        if key.startswith('filter_'):
            col_name = key.replace('filter_', '')
            filters[col_name] = request.args[key]
    
    # Get table info
    table_info = db_browser.get_table_info(table_name)
    
    # Query data
    rows, total = db_browser.query_table(
        table_name,
        limit=per_page,
        offset=offset,
        order_by='id' if any(c['name'] == 'id' for c in table_info['columns']) else None,
        filters=filters if filters else None
    )
    
    # Calculate pagination
    total_pages = (total + per_page - 1) // per_page
    
    return render_template('table_view.html',
                          table_name=table_name,
                          table_info=table_info,
                          rows=rows,
                          total=total,
                          page=page,
                          per_page=per_page,
                          total_pages=total_pages,
                          filters=filters)


@app.route('/database/query', methods=['GET', 'POST'])
def query_database():
    """Execute custom SELECT queries"""
    query = request.form.get('query', '') if request.method == 'POST' else request.args.get('query', '')
    results = []
    error = None
    
    if query:
        results, error = db_browser.execute_select(query)
    
    return render_template('query.html',
                          query=query,
                          results=results,
                          error=error)


@app.errorhandler(404)
def not_found(e):
    """404 error handler"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    """500 error handler"""
    return render_template('500.html'), 500


if __name__ == '__main__':
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'

    print("\n" + "="*60)
    print("OpenClaw Reports UI")
    print("="*60)
    print(f"Reports directory: {indexer.reports_dir}")
    print(f"Database: {db_browser.db_path}")
    print(f"Indexed reports: {len(indexer._index)}")
    print(f"\nStarting server on http://{host}:{port}")
    print("Set HOST=0.0.0.0 to expose beyond localhost (e.g. over Tailscale)")
    print("Press Ctrl+C to stop")
    print("="*60 + "\n")

    app.run(host=host, port=port, debug=debug)
