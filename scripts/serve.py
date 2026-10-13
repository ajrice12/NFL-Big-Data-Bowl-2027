"""Serve only presentation assets and generated research outputs on loopback."""
import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit
from src.load_data import ROOT

class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,directory=str(ROOT),**kwargs)
    def do_GET(self):
        path=unquote(urlsplit(self.path).path)
        if path=='/':
            self.send_response(302);self.send_header('Location','/presentation/');self.end_headers();return
        candidate=(ROOT/path.lstrip('/')).resolve()
        allowed=[ROOT/'presentation',ROOT/'outputs/figures',ROOT/'outputs/animations',ROOT/'outputs/presentation']
        permitted=any(candidate.is_relative_to(p.resolve()) for p in allowed) or candidate==(ROOT/'outputs/presentation/research.json').resolve()
        if not permitted:
            self.send_error(404,'Not a presentation asset');return
        if candidate.is_dir() and candidate!=(ROOT/'presentation').resolve():
            self.send_error(404,'Directory browsing disabled');return
        super().do_GET()
    def do_HEAD(self):
        # Same whitelist as GET; base handler sends no body for HEAD.
        self.do_GET()
    def end_headers(self):
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        super().end_headers()

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--port',type=int,default=8765);args=parser.parse_args()
    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
    print(f'Presentation: http://127.0.0.1:{args.port}/presentation/',flush=True)
    print('Local only. Ctrl+C stops the server.',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
if __name__=='__main__':main()
