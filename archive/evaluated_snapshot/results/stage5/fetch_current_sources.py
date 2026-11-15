"""Archive current official pages for the saved selection; no retrieval/generation."""
import concurrent.futures
import datetime
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent


class MainText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.active = False
        self.skip = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == 'main':
            self.active = True
        if tag in ('script', 'style', 'noscript', 'svg'):
            self.skip += 1
        if self.active and not self.skip and tag in ('p','div','h1','h2','h3','h4','li','tr','td','th','br','section'):
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript', 'svg'):
            self.skip = max(0, self.skip - 1)
        if self.active and not self.skip and tag in ('p','div','h1','h2','h3','h4','li','tr','td','th','section'):
            self.parts.append('\n')
        if tag == 'main':
            self.active = False

    def handle_data(self, data):
        if self.active and not self.skip:
            self.parts.append(data)

    def text(self):
        lines = [re.sub(r'[^\S\n]+', ' ', line).strip() for line in ''.join(self.parts).splitlines()]
        return re.sub(r'\n{3,}', '\n\n', '\n'.join(lines)).strip()


def fetch(item):
    doc_id, url = item
    assert urlsplit(url).hostname == 'www.uscis.gov'
    folder = HERE / 'current_pages'
    folder.mkdir(exist_ok=True)
    html, headers, text = [folder / f'{doc_id}.{suffix}' for suffix in ('html','headers.txt','txt')]
    now = datetime.datetime.now(datetime.timezone.utc)
    started = now.isoformat()
    response = subprocess.run(['curl','-LsS','--max-time','60','-D',str(headers),'-o',str(html),
                               '-w','%{http_code}\n%{url_effective}\n',url], capture_output=True,text=True)
    parts = response.stdout.splitlines()
    code, effective = parts[0] if parts else '', parts[1] if len(parts)>1 else ''
    parser = MainText()
    if html.exists():
        parser.feed(html.read_text(errors='replace'))
    text.write_text(parser.text()+'\n')
    ok = response.returncode == 0 and code == '200' and bool(parser.text()) and urlsplit(effective).hostname == 'www.uscis.gov'
    record = {'source_doc_id':doc_id,'requested_url':url,'effective_url':effective,'accessed_at_utc':started,
              'access_date':now.astimezone(ZoneInfo('America/New_York')).date().isoformat(),
              'http_status':code,'curl_exit_code':response.returncode,
              'transport_status':'content_retrieved' if ok else 'incomplete_or_blocked',
              'error':response.stderr,'html_file':str(html.relative_to(HERE)),
              'headers_file':str(headers.relative_to(HERE)),'main_text_file':str(text.relative_to(HERE)),
              'html_sha256':hashlib.sha256(html.read_bytes()).hexdigest() if html.exists() else None,
              'main_text_sha256':hashlib.sha256(text.read_bytes()).hexdigest(),
              'web_reader_attempt':'HTTP 403 Forbidden; direct public curl request used instead',
              'note':'HTTP/content capture alone is not a relevance check; inspect each source-review row.'}
    return record


def main():
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
