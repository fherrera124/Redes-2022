# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

from urllib import urlunquote


hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.performReq(unlunquote(self.path).decode('utf-8'))

    def performReq(self, req):
        curDir = os.getcwd()
        fname = curDir + '/' + self.path[1:]
        try:
            self.send_response(200, "Ok!")
            ext = os.path.splitext(self.path)[1]
            self.send_header('Content', 'text/xml; charset=UTF-8')
            self.end_headers()
            f = open(fname, 'rb')
            for l in f:
                self.wfile.write(l)
            f.close()
            print('file '+fname+" Ok")
        except IOError:
            print('no file '+fname)
            self.send_error(code=404, message="A donde queres ir titan galactico?")


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
