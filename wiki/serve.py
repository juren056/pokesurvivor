"""Local preview with true 404 responses. No game directory is served."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse

DIST = Path(__file__).resolve().parent / 'dist'


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIST), **kwargs)

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
