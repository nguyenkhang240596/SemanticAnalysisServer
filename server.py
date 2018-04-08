from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import config
import semantic 
import os

PORT = os.environ.get("PORT", 5000)

class SimpleHTTP(BaseHTTPRequestHandler):
  # Nhận GET request gửi lên.
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _set_cors_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        
    def do_GET(self):
        self._set_headers()
        html = open("./client.html")
        # message = website
        # message = """<html>
        #     <head></head>
        #     <body><p>Hello World!</p></body>
        #     </html>"""
        self.wfile.write(str.encode(html.read()))
        # self.wfile.write(bytes(message, "utf8"))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
#         self._set_headers()
        self._set_cors_headers()
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        data = self.data_string.decode("utf-8")
        #parse to json object
        obj = json.loads(data)
        
        #get data in setence field
        sentence = obj["sentence"]
        print(sentence)

        res = semantic.semanticAnalysisExecute(sentence)
        
        #convert res to bytes
        res = str.encode(res)
        self.wfile.write(res)  
        
    def do_OPTIONS(self):
        self._set_cors_headers()
        
        
def startServer(server_address):
    #server_address = ('127.0.0.1', 3333)
    # cấu hình host và cổng port cho server

    # Khởi tạo server với thông số cấu hình ở trên.
    semantic.init()
    httpd = HTTPServer(server_address, SimpleHTTP)


    print("Starting server")

    # Tiến hành chạy server
    httpd.serve_forever()

# server_address = (config.server_ip, config.server_port)
server_address = (config.server_ip, int(PORT))
startServer(server_address)