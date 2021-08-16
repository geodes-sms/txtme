# ===============================================================================
#Prototype AJAX Test: Server side script (start first)
#USAGE: main.py <port>
#Daniel Riegelhaupt, 2014
#===============================================================================
import sys
import SimpleHTTPServer
import SocketServer
from mainRequestHandler import MainRequestHandler
from saveLoadRequestHandler import SaveLoadRequestHandler
from grammarRequestHandler import GrammarRequestHandler
import codecs

RUN = True
TEMP_SAVE_DIR = "temp"

def startHTTPServer(port):
    """
    Minimal web server.
    """

    class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
        def __init__(self, request, client_address, server):
            SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, request, client_address, server)
            SimpleHTTPServer.SimpleHTTPRequestHandler.extensions_map['.svg'] = 'image/svg+xml'
            SimpleHTTPServer.SimpleHTTPRequestHandler.extensions_map['.rtf'] = 'text/rtf'
            SimpleHTTPServer.SimpleHTTPRequestHandler.extensions_map['.txt'] = 'text/plain'
            SimpleHTTPServer.SimpleHTTPRequestHandler.extensions_map['.text'] = 'text/plain'

        def do_GET(self):
            if TEMP_SAVE_DIR in self.path:
                filePath = '.' + self.path
                with codecs.open(filePath, 'rb', encoding='utf-8') as fh:
                    self.send_response(200)
                    self.send_header('Content-Disposition', 'attachment')
                    #TODO manually add correct header type here ? not sure that the extension map is used since this is overwritting the default do_GET
                    self.end_headers()
                    self.wfile.write(fh.read().encode('utf-8'))
            else:
                SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


        def do_POST(self):
            """ Receives input from Firefox as well as polls for updates """
            length = int(self.headers.getheader('content-length'))
            request = self.rfile.read(length)

            retval = MainRequestHandler.INSTANCE.processRequest(request)
            global RUN
            RUN = MainRequestHandler.INSTANCE.getIsOpen()

            #maybe change the code depending on return value,
            #but send response line must be here (with end headers) or the app will crash !!!
            self.send_response(200)
            self.end_headers()
            self.wfile.write(retval)

    httpd = SocketServer.TCPServer(("", port), Handler)

    print "HTTP server is now serving at port", port
    global RUN
    while RUN:
        httpd.handle_request()

    httpd.socket.close()  #explictly stop the socket this should avoid the wait after every time we want to restart te server
    print "HTTP server has been closed normally because the application closed"


def main():
    if (len(sys.argv) == 2):
        port = int(sys.argv[1])
    else:
        port = 8000

    MainRequestHandler.INSTANCE = MainRequestHandler(TEMP_SAVE_DIR)
    startHTTPServer(port)
    return 0


if __name__ == '__main__':
    sys.exit(main())

  
  

