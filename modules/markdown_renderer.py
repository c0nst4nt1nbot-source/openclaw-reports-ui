"""
Markdown Renderer - Converts markdown to HTML with syntax highlighting
"""
import markdown
import nh3
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.toc import TocExtension


# Raw HTML embedded in reports passes through Python-Markdown untouched, so the
# rendered output is sanitized against an allowlist before it is marked safe.
ALLOWED_TAGS = {
    'a', 'abbr', 'b', 'blockquote', 'br', 'code', 'dd', 'del', 'div', 'dl',
    'dt', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img', 'ins',
    'li', 'ol', 'p', 'pre', 'span', 'strong', 'sub', 'sup', 'table', 'tbody',
    'td', 'tfoot', 'th', 'thead', 'tr', 'ul',
}
ALLOWED_ATTRIBUTES = {
    '*': {'class', 'id'},
    'a': {'href', 'title'},
    'img': {'src', 'alt', 'title'},
    'th': {'align'},
    'td': {'align'},
}
ALLOWED_URL_SCHEMES = {'http', 'https', 'mailto'}


def sanitize_html(html: str) -> str:
    """Strip scripts, event handlers and unsafe URL schemes from HTML"""
    return nh3.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        url_schemes=ALLOWED_URL_SCHEMES,
        link_rel='noopener noreferrer',
    )


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
        """Render markdown to sanitized HTML"""
        # Reset the markdown instance
        self.md.reset()
        
        # Convert to HTML
        html = self.md.convert(content)
        
        return sanitize_html(html)
    
    def extract_title(self, content: str) -> str:
        """Extract title from markdown (first H1)"""
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                return line[2:].strip()
        return "Untitled Report"
