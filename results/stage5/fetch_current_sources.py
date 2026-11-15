"""Archive USCIS page text and sanitized HTML copies for the saved selection."""
import concurrent.futures
import datetime
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))

from scripts.sanitize_uscis_captures import (
    PRIVATE_ROOT,
    has_public_marker,
    preserve_original,
    sanitize_capture,
    sha256,
    update_public_manifest,
)


class MainText(HTMLParser):
    """Extract readable text inside the main page element of an HTML response."""
    def __init__(self):
        """Initialize the HTML parser’s main-content and skip state."""
        super().__init__(convert_charrefs=True)
        self.active = False
        self.skip = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        """Track main content and ignore script, style, and other non-content sections."""
        if tag == 'main':
            self.active = True
        if tag in ('script', 'style', 'noscript', 'svg'):
            self.skip += 1
        if self.active and not self.skip and tag in ('p','div','h1','h2','h3','h4','li','tr','td','th','br','section'):
            self.parts.append('\n')

    def handle_endtag(self, tag):
        """Close skipped sections and stop collecting after the main element."""
        if tag in ('script', 'style', 'noscript', 'svg'):
            self.skip = max(0, self.skip - 1)
        if self.active and not self.skip and tag in ('p','div','h1','h2','h3','h4','li','tr','td','th','section'):
            self.parts.append('\n')
        if tag == 'main':
            self.active = False

    def handle_data(self, data):
        """Collect text only while inside visible main-page content."""
        if self.active and not self.skip:
            self.parts.append(data)

    def text(self):
        """Return normalized text collected from the page’s main element."""
        lines = [re.sub(r'[^\S\n]+', ' ', line).strip() for line in ''.join(self.parts).splitlines()]
        return re.sub(r'\n{3,}', '\n\n', '\n'.join(lines)).strip()


def fetch(item):
    """Download and archive one selected official USCIS page with access metadata."""
    doc_id, url = item
    assert urlsplit(url).hostname == 'www.uscis.gov'
    folder = HERE / 'current_pages'
    folder.mkdir(exist_ok=True)
    html, headers, text = [folder / f'{doc_id}.{suffix}' for suffix in ('html','headers.txt','txt')]
    now = datetime.datetime.now(datetime.timezone.utc)
    started = now.isoformat()
    with tempfile.TemporaryDirectory() as temporary_dir:
        downloaded = Path(temporary_dir) / 'response.html'
        response = subprocess.run(['curl','-LsS','--max-time','60','-D',str(headers),'-o',str(downloaded),
                                   '-w','%{http_code}\n%{url_effective}\n',url], capture_output=True,text=True)
        parts = response.stdout.splitlines()
        code, effective = parts[0] if parts else '', parts[1] if len(parts)>1 else ''
        original = downloaded.read_bytes() if downloaded.exists() else b''
        private_dir = PRIVATE_ROOT / now.strftime('%Y-%m-%d')
        if html.exists():
            previous = html.read_bytes()
            if not has_public_marker(previous):
                preserve_original(ROOT / 'results/stage5/current_pages' / f'{doc_id}.html', previous, private_dir)
        if original:
            preserve_original(ROOT / 'results/stage5/current_pages' / f'{doc_id}.html', original, private_dir)
        try:
            safe_html, redacted = sanitize_capture(original)
            if original:
                html.write_bytes(safe_html)
        except ValueError as error:
            safe_html = b''
            sanitization_error = str(error)
        else:
            sanitization_error = ''
            if original and redacted:
                update_public_manifest([{
                    'path': str(html.relative_to(ROOT)),
                    'original_sha256': sha256(original),
                    'sanitized_sha256': sha256(safe_html),
                    'redacted_config_fields': ['uscis_design.apiKey_aao_pm_search'],
                    'original_preserved_privately': True,
                }])
    parser = MainText()
    if original:
        parser.feed(original.decode('utf-8', errors='replace'))
    text.write_text(parser.text()+'\n')
    ok = (response.returncode == 0 and code == '200' and bool(parser.text())
          and urlsplit(effective).hostname == 'www.uscis.gov' and not sanitization_error
          and not re.search(r'AIza[0-9A-Za-z_-]{35}', safe_html.decode('utf-8', errors='ignore')))
    record = {'source_doc_id':doc_id,'requested_url':url,'effective_url':effective,'accessed_at_utc':started,
              'access_date':now.astimezone(ZoneInfo('America/New_York')).date().isoformat(),
              'http_status':code,'curl_exit_code':response.returncode,
              'transport_status':'content_retrieved' if ok else 'incomplete_or_blocked',
              'error':response.stderr or sanitization_error,'html_file':str(html.relative_to(HERE)),
              'headers_file':str(headers.relative_to(HERE)),'main_text_file':str(text.relative_to(HERE)),
              'html_sha256':hashlib.sha256(safe_html).hexdigest() if html.exists() else None,
              'original_html_sha256':hashlib.sha256(original).hexdigest() if original else None,
              'html_sanitized_derivative':bool(html.exists()),
              'redacted_config_fields':['uscis_design.apiKey_aao_pm_search'] if b'apiKey_aao_pm_search' in original and b'[redacted upstream page configuration]' in safe_html else [],
              'original_preserved_privately':bool(original),
              'main_text_sha256':hashlib.sha256(text.read_bytes()).hexdigest(),
              'web_reader_attempt':'HTTP 403 Forbidden; direct public curl request used instead',
              'note':'HTTP/content capture alone is not a relevance check; inspect each source-review row.'}
    return record


def main():
    """Archive current pages for the saved selection unless an access archive already exists."""
    log = HERE / 'current_page_access.jsonl'
    if log.exists():
        print('Existing access archive retained; inspect its recorded timestamps rather than claiming a fresh access.')
        return
    selection = [json.loads(l) for l in (HERE/'selection.jsonl').read_text().splitlines()]
    documents = sorted({r['source_doc_id']:r['source_url'] for r in selection}.items())
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        records = list(pool.map(fetch, documents))
    log.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records))
    print(json.dumps([{k:r[k] for k in ('source_doc_id','http_status','transport_status')} for r in records],indent=2))


if __name__ == '__main__':
    main()
