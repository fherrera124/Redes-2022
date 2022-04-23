from datetime import datetime
import socket
from warnings import catch_warnings


class Server:
    
    def server_close(self):
        """Called to clean-up the server.

        May be overridden.

        """
        self.socket.close()
    
    

    def parse_request(self):
        """Parse a request (internal).

        The request should be stored in self.raw_requestline; the results
        are in self.command, self.path, self.request_version and
        self.headers.

        Return True for success, False for failure; on failure, any relevant
        error response has already been sent back.

        """
        self.command = None  # set in case of error on the first line
        self.request_version = version = self.default_request_version
        self.close_connection = True
        requestline = str(self.raw_requestline, 'iso-8859-1')
        requestline = requestline.rstrip('\r\n')
        self.requestline = requestline
        words = requestline.split()
        if len(words) == 0:
            return False

        if len(words) >= 3:  # Enough to determine protocol version
            version = words[-1]
            try:
                if not version.startswith('HTTP/'):
                    raise ValueError
                base_version_number = version.split('/', 1)[1]
                version_number = base_version_number.split(".")
                # RFC 2145 section 3.1 says there can be only one "." and
                #   - major and minor numbers MUST be treated as
                #      separate integers;
                #   - HTTP/2.4 is a lower version than HTTP/2.13, which in
                #      turn is lower than HTTP/12.3;
                #   - Leading zeros MUST be ignored by recipients.
                if len(version_number) != 2:
                    raise ValueError
                version_number = int(version_number[0]), int(version_number[1])
            except (ValueError, IndexError):
                self.send_error(
                    HTTPStatus.BAD_REQUEST,
                    "Bad request version (%r)" % version)
                return False
            if version_number >= (1, 1) and self.protocol_version >= "HTTP/1.1":
                self.close_connection = False
            if version_number >= (2, 0):
                self.send_error(
                    HTTPStatus.HTTP_VERSION_NOT_SUPPORTED,
                    "Invalid HTTP version (%s)" % base_version_number)
                return False
            self.request_version = version

        if not 2 <= len(words) <= 3:
            self.send_error(
                HTTPStatus.BAD_REQUEST,
                "Bad request syntax (%r)" % requestline)
            return False
        command, path = words[:2]
        if len(words) == 2:
            self.close_connection = True
            if command != 'GET':
                self.send_error(
                    HTTPStatus.BAD_REQUEST,
                    "Bad HTTP/0.9 request type (%r)" % command)
                return False
        self.command, self.path = command, path

        # Examine the headers and look for a Connection directive.
        try:
            self.headers = http.client.parse_headers(self.rfile,
                                                    _class=self.MessageClass)
        except http.client.LineTooLong as err:
            self.send_error(
                HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE,
                "Line too long",
                str(err))
            return False
        except http.client.HTTPException as err:
            self.send_error(
                HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE,
                "Too many headers",
                str(err)
            )
            return False

        conntype = self.headers.get('Connection', "")
        if conntype.lower() == 'close':
            self.close_connection = True
        elif (conntype.lower() == 'keep-alive' and
            self.protocol_version >= "HTTP/1.1"):
            self.close_connection = False
        # Examine the headers and look for an Expect directive
        expect = self.headers.get('Expect', "")
        if (expect.lower() == "100-continue" and
                self.protocol_version >= "HTTP/1.1" and
                self.request_version >= "HTTP/1.1"):
            if not self.handle_expect_100():
                return False
        return True


    def handle(self): #main
        """por defecto cerramos la conexion"""
        self.close_connection = True

        self.parse_request()
        while not self.close_connection:
            self.parse_request()


    while True:
        connection, address = serversocket.accept()
        request = connection.recv(1024).decode('utf-8')
        print(request)
        string_list = request.split(' ')
        method = string_list[0]
    # try:
        protocol = string_list[2]
        # except Exception as e:
        #protocol = 'HTTP/1.0'
        print('Request HTTP version:', protocol)
        #print('Client Method',method)
        requesting_file = string_list[1]
        #print('Client request',requesting_file)
        myfile = requesting_file.split('?')[0]
        myfile = myfile.lstrip('/')

        metodos_validos = ('GET', 'POST', 'PUT', 'HEAD', 'DELETE', 'PATCH')

        if method in metodos_validos:
            if (method != 'GET'):
                header = 'HTTP/1.0 405 METHOD NOT ALLOWED\n'
                response = '<html><body>Error 405: HTTP Method Not Allowed</body></html>'.encode(
                    'utf-8')
            else:
                if(myfile == ''):
                    myfile = 'index.html'

                try:
                    file = open(myfile, 'rb')
                    response = file.read()
                    file.close()
                    if (protocol == ' HTTP/1.1'):
                        header += 'Host:'+str(host)+':'+str(port) + \
                            '\n Connection: Keep Alive\n User-Agent: \n'
                    header += 'HTTP/1.0 200 OK\n Date: '+str(fecha)+'\n'
                    if(myfile.endswith('.jpg')):
                        mimetype = 'image/jpg'
                    elif(myfile.endswith('.css')):
                        mimetype = 'text/css'
                    elif(myfile.endswith('.pdf')):
                        mimetype = 'application/pdf'
                    else:
                        mimetype = 'text/html'

                    header += 'Content-Type: ' + \
                        str(mimetype)+'\n Connection: Closed\n\n'

                except Exception as e:
                    print("-")
                    header = 'HTTP/1.0 404 Not Found\n\n'
                    response = '<html><body>Error 404: File not found</body></html>'.encode(
                        'utf-8')
        else:
            header = 'HTTP/1.0 400 BAD REQUEST\n'
            response = '<html><body>Error 400: Bad request</body></html>'.encode(
                'utf-8')
        final_response = header.encode('utf-8')
        final_response += response
        connection.send(final_response)
        if (1 == 2):
            connection.close()


if __name__ == "__main__":

    #webServer = HTTPServer((hostName, serverPort), MyServer)
    
    webServer = Server()

    host, port = '127.0.0.1', 8010
    fecha = datetime.now
    header = ''
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((host, port))
    serversocket.listen(1)
    print('servidor en el puerto', port)


    try:
        webServer.handle()
    except KeyboardInterrupt:
        pass

    #webServer.server_close()
    serversocket.close()
    print("Server stopped.")