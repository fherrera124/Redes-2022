

## Breve descripción:

Este programa tiene en cuenta versiones de HTTP/1.0 y HTTP/1.1. Dependiendo de la versión,
evaluará si cerrar la conexión o no.

## Modo de uso:

`python3 server.py `

Por defecto se iniciara el servidor con HTTP/1.0, para utilizar HTTP/1.1 ejecutar:

`python3 server.py 1.1`


## Casos de prueba

A continuación listamos algunos casos de pruebas más ineresantes:

#### Caso 1

##### Para la entrada:
    $ telnet localhost 8010
    GET /index.html HTTP/1.0
##### Su respuesta debe ser:
    HTTP/1.0 200 OK
    Date: Sat, 07 May 2022 16:07:46 GMT
    Server: Redes-2021/grupo-z
    Content-Length: 35
    Content-Type: text/html
    Connection: close
    <HTML><H1>/index.html</H1></HTML>
    
    Se ha perdido la conexión con el host.
-Notar que como es HTTP 1.0 la conexión se cierra de manera automática.

#### Caso 2
##### Para la entrada:
    $ telnet localhost 8010
    GET prueba-de-uso/ok.html HTTP/1.1
##### La respuesta debe ser:
    HTTP/1.1 200 OK
    Date: Fri, 27 May 2022 02:06:02 GMT
    Server: Redes-2021/grupo-z
    Content-Length: 45
    Content-Type: text/html
    Connection: keep-alive

    <HTML><H1>prueba-de-uso/ok.html</H1></HTML>

Notar que la conexión no se cierra a pesar de que el servidor se inició por defecto con la versión HTTP/1.0. En cambio responde con la versión de HTTP/1.1 como se solicitó explícitamente ( HTTP/1.1 200 OK ), y mantiene la conexión abierta. En este momento se puede realizar otra consulta. IMPORTANTE: recordar que la versión con la que está corriendo el servidor es 1.0, por lo que si no se vuelve a pedir explicitamente por la version 1.1 en la siguiente consulta, la conexión se cerrará por defecto.
    

#### Caso 3

##### Para la entrada:
    $ telnet localhost 8010
    GET dir/subdir/test.html
    Connection: keep-alive
##### La respuesta debe ser:
    HTTP/1.0 200 OK
    Date: Sat, 07 May 2022 16:12:09 GMT
    Server: Redes-2021/grupo-z
    Content-Length: 44
    Content-Type: text/html
    Connection: keep-alive
    
    <HTML><H1>dir/subdir/test.html</H1></HTML>


Notar que la conexión no se cierra, pero a diferencia que el ejemplo anterior, la respuesta dice "HTTP/1.0 200 OK", es decir, respondió con la versión por defecto, pero como nosotros para la versión HTTP/1.0 tenemos implementada la instrucción keep-alive, entonces la conexión no se cierra. Parecida a la aclaración para el ejemplo anterior, si no se vuelve a enviar la cabezera keep-alive en la siguiente consulta, la conexión se cerrará por defecto.


#### Modo HTTP/1.1  
Puede iniciar el server con algun parametro: 1.0 o 1.1, 1.0 es el por defecto

Si usted ejecuta en una terminal  `python server.py 1.1 ` la conexion seguira activa, por lo que puede mandar más consultas.

#### Caso 4
##### Para la entrada:
        GET index.html HTTP/1.1
##### La salida va a ser (se puede seguir mandando consultas):
        HTTP/1.1 200 OK
        Date: Thu, 26 May 2022 19:23:22 GMT
        Server: Redes-2021/grupo-z
        Content-Length: 38
        Content-Type: text/html
        Connection: keep-alive

        <HTML><H1>index.html</H1></HTML>

La conexión no se cierra.

#### Caso 5
        
##### Si esperan 100 segundos sin enviar una consulta
    
##### La salida del lado del servidor va a ser:
        127.0.0.1 - - timed out

#### Caso 6

##### Para la entrada (se solicita usar el protocolo HTTP/1.0):
        GET H HTTP/1.0
##### La salida será:
        HTTP/1.0 200 OK
        Date: Thu, 26 May 2022 19:40:34 GMT
        Server: Redes-2021/grupo-z
        Content-Length: 25
        Content-Type: text/html
        Connection: close

        <HTML><H1>H</H1></HTML>

        Se ha perdido la conexión con el host.
    
    Notar que se cerró la conexión, pues se solicitó la versión 1.0.

#### Caso 7

##### Para la entrada (se solicita que se cierre la conexion): 
        GET G HTTP/1.1
        Connection: close
##### La salida va a ser:
        HTTP/1.1 200 OK
        Date: Thu, 26 May 2022 19:44:34 GMT
        Server: Redes-2021/grupo-z
        Content-Length: 25
        Content-Type: text/html
        Connection: close

        <HTML><H1>G</H1></HTML>

        Se ha perdido la conexión con el host.
    
    Notar que se cerró la conexión, pues se envió la cabecera close.


#### Respuesta ante errores en la consulta

Tanto para la versión 1.0 como 1.1, los siguientes errores son devueltos por el servidor ante consultas erróneas por parte del cliente.

#### Caso 8

##### Para la entrada
    $ telnet localhost 8010
    FFF /
##### La salida va a ser:
    HTTP/1.0 400 BAD REQUEST

    Se ha perdido la conexión con el host.

#### Caso 9

##### Para la entrada:
    $ telnet localhost 8010
    ....GET

##### La salida va a ser:
    HTTP/1.0 400 BAD REQUEST

    Se ha perdido la conexión con el host.

#### Caso 10

##### Para la entrada:
    $ telnet localhost 8010
    HEAD /index.html HTTP/1.0
    
##### La salida va a ser:
    HTTP/1.0 405 METHOD NOT ALLOWED

    Se ha perdido la conexión con el host.

        
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
