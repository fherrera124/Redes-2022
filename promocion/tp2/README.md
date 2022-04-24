

## Modo de uso:

`python3 server.py `

Por defecto se iniciara el servidor con HTTP/1.0, para utilizar HTTP/1.1 ejecutar:

`python3 server.py 1.1`



## Casos de prueba

...

## Enunciado

12. (Ejercicio de promoción) Programar en el lenguaje que sea de su elección un servidor HTTP/1.0
reducido que sólo implementará lo enumerado a continuación:
NOTA: para quienes hagan la promoción, este será un ejercicio “entregable”. En la entrega deberán
incluir el código fuente debidamente comentado y un README, o README.md que explique cómo
generar el programa, cómo ejecutarlo y cómo testearlo.
a. Deberá recibir requerimientos HTTP 1.0 y 1.1 para procesarlos y determinar sí la solicitud es válida.
Si detecta que el requerimiento no es válido responderá con un error 400.
b. Sólo debe implementar el método GET. Sí el método es otro responderá con un error 405.
c. La respuesta será una página HTML generada automáticamente que incluye en su cuerpo el string
del recurso HTTP solicitado.
d. La respuesta HTTP debe ser válida, respetando el protocolo, e incluír las cabeceras apropiadas para
indicar el tipo de contenido, el tamaño, la fecha y el tipo de servidor.
e. Todas las cabeceras envíadas por el cliente deben ser válidas y en principio ignoradas.
f. Debe ser programado utilizando la API de socket, es decir las llamadas, socket, listen, accept,
etc.
g. El servidor debe ser testeado con un navegador/user-agent http tradicional. Por ejemplo, sí ejecutamos el servidor localmente en puerto 80 las siguientes serían algunas interacciones posibles.

$ telnet localhost 80
GET /index.html HTTP/1.0
HTTP/1.0 200 OK
Date: Wed, 16 Mar 2022 15:26 GMT
Server: Silly/0.1
Content-Length: 33
Content-Type: text/html
Connection: Closed
<HTML><H1>/index.html</H1></HTML>
Connection closed by foreign host.
Ejemplo 1
$ telnet localhost 80
GET dir/subdir/test.html HTTP/1.1
Host: 127.0.0.1:8000
Connection: keep-alive
User-Agent: Mozilla/5.0 (X11; Linux x86_64)
HTTP/1.0 200 OK
Date: Wed, 16 Mar 2022 15:39 GMT
Server: Silly/0.1
Content-Length: 42
Content-Type: text/html
Connection: Closed
<HTML><H1>dir/subdir/test.html</H1></HTML>
Connection closed by foreign host.

$ telnet localhost 80
FFF /
HTTP/1.0 400 Bad Request
Connection closed by foreign host.
Ejemplo 3
$ telnet localhost 80
....GET
HTTP/1.0 400 Bad Request
Connection closed by foreign host.
Ejemplo 4
$ telnet localhost 80
HEAD /index.html HTTP/1.0
HTTP/1.0 405 Method Not Allowed
Connection closed by foreign host.
Ejemplo 5