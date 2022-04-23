from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import urllib
import socket
from http import HTTPStatus

hostName = "localhost"
serverPort = 8010


class MyServer(BaseHTTPRequestHandler):

    metodos_validos = ('GET', 'POST', 'PUT', 'HEAD', 'DELETE', 'PATCH')

    def handle_one_request(self):

        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(HTTPStatus.REQUEST_URI_TOO_LONG)
                return
            if not self.raw_requestline:
                self.close_connection = True
                return
            if not self.parse_request():
                # An error code has been sent, just exit
                return

            if self.command in self.metodos_validos:
                if self.command == 'GET':
                    self.do_GET()
                else:
                    self.send_error(code=405, message="Metodo no permitido")
            else:
                self.send_error(code=400, message="Mala peticion")

            # actually send the response if not already done.
            self.wfile.flush()
        except socket.timeout as e:
            # a read or a write timed out.  Discard this connection
            self.log_error("Request timed out: %r", e)
            self.close_connection = True
        return

    




    def do_GET(self):
        self.performReq(urllib.parse.unquote(self.path))

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
            self.send_error(
                code=404, message="A donde queres ir titan galactico?")





if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
