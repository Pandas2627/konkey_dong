import os
from http.server import BaseHTTPRequestHandler
import urllib.request
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # This pulls the key from Vercel's "Environment Variables" 
        private_key = os.environ.get("DREAMLO_PRIVATE_KEY")
        
        # Parses the URL (e.g., /api/add_score?name=User&score=100)
        query = parse_qs(urlparse(self.path).query)
        name = query.get('name', [''])[0]
        score = query.get('score', ['0'])[0]
        
        if name and score and private_key:
            # Forwards the data to Dreamlo with your secret key attached
            url = f"http://dreamlo.com/lb/{private_key}/add/{name}/{score}"
            urllib.request.urlopen(url)
            
        self.send_response(200)
        # Allows your GitHub game to talk to your Vercel Proxy
        self.send_header('Access-Control-Allow-Origin', '*') 
        self.end_headers()
        self.wfile.write(b"Score Saved!")