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
    # rst = {'x':random.random(), 'y':random.random(), 'z': random.random(), 'text':'hoge'}
    rst = pdf2map.random_choice()
    rst = json.dumps(rst)
    body = bytes(rst, 'utf-8')
    self.wfile.write(body)
    return

HOST = 'localhost'
PORT = 7000
httpd = HTTPServer((HOST, PORT), Handler)
print('Backend brain alive 🔥 ', HOST, ':', PORT)
httpd.serve_forever()
