from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import urllib2
import httplib

PORT_NUMBER = 8080

ZABBIX_SETTINGS = {
    "host": "zabbix.example.org",
    "login": "admin",
    "password": "admin"
}

COOKIE = ''

class ThreadedHTTPConnection(ThreadingMixIn, httplib.HTTPConnection):
    pass


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


class graphHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            graph_id = int(self.path[1:])
        except ValueError as error:
            print(error)
            self.send_response(500)
            self.send_header('Content-type','text/html')
            self.wfile.write('Requested id is not an integer')
            self.wfile.flush()
            self.wfile.close()
            return

        print(self.path)
        handler_connection = ThreadedHTTPConnection(ZABBIX_SETTINGS['host'])

        handler_connection.request(
            "GET",
            "/zabbix/chart2.php?graphid={0}&width=640&height=150".format(self.path[1:]),
            None,
            {'cookie': COOKIE}
        )

        handler_connection_response = handler_connection.getresponse()

        self.send_response(200)
        self.send_header('Content-type','image/png')
        self.end_headers()
        self.wfile.write(handler_connection_response.read())
        self.wfile.flush()
        self.wfile.close()
        return


try:
    main_connection = httplib.HTTPConnection(ZABBIX_SETTINGS['host'])
    main_connection.request(
        "POST",
         "/zabbix/index.php?request=&name={0}&password={1}&autologin=1&enter=Sign+in".format(
             ZABBIX_SETTINGS['login'],
             ZABBIX_SETTINGS['password']
         )
    )

    main_response = main_connection.getresponse()

    COOKIE = dict(main_response.getheaders())['set-cookie']
    print('connected successfuly; cookie: {0}'.format(COOKIE))

    server = ThreadedHTTPServer(('', PORT_NUMBER), graphHandler)
    print('Started httpserver on port {0}'.format(PORT_NUMBER))

    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()
