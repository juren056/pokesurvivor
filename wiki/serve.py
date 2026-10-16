"""Local preview with true 404 responses. No game directory is served."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse
import fnmatch
import re
from urllib.parse import urlsplit

DIST = Path(__file__).resolve().parent / 'dist'


def header_rules():
    rules=[]
    current=None
    source=DIST/'_headers'
    if not source.is_file():
        return rules
    for raw in source.read_text(encoding='utf-8').splitlines():
        if not raw.strip():
            continue
        if not raw.startswith((' ', '\t')):
            current=[raw.strip(), []]
            rules.append(current)
        elif current and ':' in raw:
            name,value=raw.strip().split(':',1)
            current[1].append((name.strip(),value.strip()))
    return rules


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIST), **kwargs)

    def guess_type(self, path):
        if path.endswith('.md'):
            return 'text/markdown; charset=utf-8'
        if path.endswith('.txt'):
            return 'text/plain; charset=utf-8'
        return super().guess_type(path)

    def end_headers(self):
        route=urlsplit(self.path).path
        existing=b''.join(getattr(self,'_headers_buffer',[])).lower()
        for pattern, headers in header_rules():
            if fnmatch.fnmatch(route,pattern):
                for name,value in headers:
                    if (name.lower()+':').encode() not in existing:
                        self.send_header(name,value)
        super().end_headers()

    def send_head(self):
        # Match static-host byte ranges so the preview can test real video seeking.
        target=Path(self.translate_path(self.path)).resolve()
        header=self.headers.get('Range')
        if target.is_file() and target.suffix=='.webm' and target.is_relative_to(DIST.resolve()):
            size=target.stat().st_size
            match=re.fullmatch(r'bytes=(\d*)-(\d*)',header.strip()) if header else None
            start,end=0,size-1
            valid=not header or bool(match and (match[1] or match[2]))
            if valid and header:
                if match[1]:start=int(match[1]);end=min(int(match[2]),size-1) if match[2] else size-1
                else:start=max(0,size-int(match[2]));valid=int(match[2])>0
                valid=valid and 0<=start<=end<size
            if not valid:
                self.send_response(416);self.send_header('Content-Range',f'bytes */{size}');self.send_header('Content-Length','0');self.end_headers();return None
            self.send_response(206 if header else 200);self.send_header('Content-Type','video/webm');self.send_header('Accept-Ranges','bytes')
            if header:self.send_header('Content-Range',f'bytes {start}-{end}/{size}')
            self.send_header('Content-Length',str(end-start+1));self.end_headers()
            if self.command!='HEAD':
                with target.open('rb') as source:
                    source.seek(start);remaining=end-start+1
                    while remaining:
                        chunk=source.read(min(65536,remaining))
                        if not chunk:break
                        self.wfile.write(chunk);remaining-=len(chunk)
            return None
        return super().send_head()

    def send_error(self, code, message=None, explain=None):
        if code == 404 and (DIST / '404.html').exists():
            body = (DIST / '404.html').read_bytes()
            self.send_response(404)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            if self.command != 'HEAD':
                self.wfile.write(body)
        else:
            super().send_error(code, message, explain)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=4173)
    args = parser.parse_args()
    if not (DIST / 'index.html').exists():
        raise SystemExit('Build the Wiki first: python wiki/build.py')
    print(f'Wiki preview: http://127.0.0.1:{args.port}', flush=True)
    ThreadingHTTPServer(('127.0.0.1', args.port), Handler).serve_forever()
