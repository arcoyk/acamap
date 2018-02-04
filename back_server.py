from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse as parser
import random
import json
import pdf2map

class Handler(SimpleHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200)
    self.send_header("Access-Control-Allow-Origin", "*")
    self.end_headers()
    qs = parser.parse_qs(self.path)
    doc_id = int(qs['id'][0])
    rst = pdf2map.by_id(doc_id)
    rst = json.dumps(rst)
    body = bytes(rst, 'utf-8')
    self.wfile.write(body)
    return

HOST = 'localhost'
PORT = 7000
httpd = HTTPServer((HOST, PORT), Handler)
print('Backend brain alive 🔥 ', HOST, ':', PORT)
httpd.serve_forever()
