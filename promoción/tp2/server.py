from time import time
import socket
import http.client
import sys
from email.utils import formatdate


class HTTPServer:
    """
    Esta clase representa a un servidor HTTP, implementado por nosotros mediante la
    conexión con un socket TCP.

    Soporta versiones HTTP/1.0 y HTTP/1.1

    - Si la version del protocolo es la 1.0, la conexion se cierra luego de la consulta,
    salvo que el cliente en cada consulta envie el header [Connection: keep-alive]

    - Si la version del protocolo es la 1.1, la conexion NO se cierra, salvo que el cliente
    en cada consulta envie el header [Connection: close]

    - Por defecto cierra la conexion con el socket despues de 100 segundos de inactividad
    """

    def __init__(self, socket, host, port, http_version="HTTP/1.0"):

        self.host = host
        self.port = port
        self.header = ''
        self.socket = socket

        # lo que el server asume si el cliente NO lo proporciona
        self.default_request_version = "HTTP/1.0"

        # la version con la que trabaja el servidor siempre
        if http_version in ('HTTP/1.0', 'HTTP/1.1'):
            self.protocol_version = http_version
        else:
            self.protocol_version = "HTTP/1.0"

        # asumimos misma version que el servidor
        self.request_version = self.protocol_version

        print("Protocolo por defecto: %s" % self.protocol_version)

        # cant de segundos de inactividad, None para infinito
        self.timeout = 100

        print("Esperando que se conecte un cliente")
        self.connection, self.address = self.socket.accept()  # blocking wait for client
        print("Cliente conectado!")
        self.setup()
        try:
            self.handle()
        finally:
            self.connection.close()
            self.finish()

    def default_close_connection(self):
        if self.protocol_version == 'HTTP/1.1':
            return False
        return True

    def setup(self):
        self.rfile = self.connection.makefile('rb', 0)

        if self.timeout is None:
            self.connection.settimeout(0)
        else:
            self.connection.settimeout(self.timeout)

    def handle(self):
        self.handle_one_request()
        while (not self.close_connection):
            self.handle_one_request()

    def finish(self):
        self.rfile.close()

    def handle_one_request(self):
        self.close_connection = self.default_close_connection()
        try:
            self.raw_requestline = self.rfile.readline(65537)

            if not self.raw_requestline:
                self.close_connection = True
                return

            if (self.raw_requestline.strip() == b''):
                # si el cliente ingresa blancos, no
                # forzamos el cierre de la conexión.
                # Como vimos que hace google.com.
                return

            if not self.parse_request() or\
                    not self.handle_command():
                self.close_connection = True
                return

        except socket.timeout as e:
            # read o write timed out. Descartamos la conexión
            sys.stderr.write("%s - - %s\n" % (self.address[0], e))
            self.close_connection = True
            return

    def parse_request(self):
        self.command = None
        requestline = str(self.raw_requestline, 'iso-8859-1')
        self.requestline = requestline.rstrip('\r\n')
        words = requestline.split()
        if len(words) >= 3:  # Suficiente para determinar la version de protocolo
            self.request_version = words[-1]
            try:
                if self.request_version not in ('HTTP/1.0', 'HTTP/1.1'):
                    raise ValueError
            except (ValueError, IndexError):
                error = "\n400, Bad request version: (%r)\n" % self.request_version
                self.connection.send(error.encode('utf-8'))
                return False

            if self.request_version == "HTTP/1.1":
                self.close_connection = False
            else:
                self.close_connection = True

        if not 2 <= len(words) <= 3:
            rta = '%s 400 BAD REQUEST\n' % self.protocol_version
            self.connection.send(
                rta.encode('utf-8')
            )
            return False
        # Guardamos en variables de instancia el comando y la ruta
        self.command, self.path = words[:2]
        # Leemos los headers
        self.headers = http.client.parse_headers(self.rfile)
        # Examinamos los encabezados para detectar la directiva Connection.
        conntype = self.headers.get('Connection', "")
        if conntype.lower() == 'close':
            self.close_connection = True
        elif (conntype.lower() == 'keep-alive'):
            self.close_connection = False
        return True

    def handle_command(self):
        metodos_validos = ('GET', 'POST', 'PUT', 'HEAD',
                           'DELETE', 'PATCH', 'CONNECT', 'OPTIONS', 'TRACE')
        # formato de fecha segun RFC 2822
        date_time = formatdate(time(), usegmt=True)

        success = True
        if self.command in metodos_validos:
            if (self.command == 'GET'):
                body = ('<HTML><H1>%s</H1></HTML>\n\n' % self.path)
                body = body.encode('utf-8')
                rta = '%s 200 OK\n' % self.request_version
                rta += 'Date: %s\n' % date_time
                rta += 'Server: Redes-2021/grupo-z\n'
                # es clave informar la cantidad de bytes, al menos
                # en los browsers, donde notamos comportamientos erroneos
                rta += 'Content-Length: %s\n' % len(body)
                rta += 'Content-Type: text/html\n'
                rta += 'Connection: %s\n\n' % (
                    'close' if self.close_connection else 'keep-alive')
                rta = rta.encode('utf-8')
                rta += body

            else:
                success = False
                rta = ('%s 405 METHOD NOT ALLOWED\n' %
                       self.protocol_version).encode('utf-8')
        else:
            success = False
            rta = ('%s 400 BAD REQUEST\n' %
                   self.protocol_version).encode('utf-8')
        self.connection.send(rta)
        return success


if __name__ == "__main__":

    http_version = 'HTTP/' + '1.1' if (sys.argv[-1] == '1.1') else '1.0'
    # escuchamos por conexiones entrantes desde cualquier ip
    # setear a 'localhost' para solo local.
    host = ''
    port = 8010
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((host, port))
    srv.listen(1)
    print("Server iniciado en puerto %s" % port)
    while True:
        HTTPServer(srv, host, port, http_version)
    print("Server detenido.")
