from http.server import BaseHTTPRequestHandler, HTTPServer
import runtimeREF
import threading

class RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        threading.Thread(target=runtimeREF.fnDir[int(self.headers.get('fn'))], args=({"data":self.rfile.read(content_length),"headers":self.headers},)).start()
        # filename = self.headers.get('Content-Disposition').split('=')[1].strip('"')
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Successfully received file\n')

def startServer():
    port = 8000
    server_address = (runtimeREF.HOSTIP, port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'HTTP Server listening on {runtimeREF.HOSTIP}:{port}')
    httpd.serve_forever()

if __name__ == '__main__':
    startServer()