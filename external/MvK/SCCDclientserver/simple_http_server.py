import BaseHTTPServer
import SimpleHTTPServer
import urllib2
import traceback
import cgi
import urlparse
import sys

import server
from python_runtime.statecharts_core import Event

class MvKHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        try:
            data = self.rfile.read(int(self.headers.getheader('content-length')))
            postvars = urlparse.parse_qs(data, keep_blank_values=1)

            MvKHandler.controller.addInput(Event("request", "request", [postvars["func"][0], postvars["args"][0], postvars["client_id"][0]]))
            returndata = MvKHandler.listener.fetch(-1).getParameters()[0]
        except Exception:
            print(traceback.format_exc())
            returndata = '{"type": "MvKReadLog", "value": {"keys": [{"type": "StringValue", "value": "status_message"}, {"type": "StringValue", "value": "status_code"}], "values": [{"type": "StringValue", "value": "HTTP internal POST problem"}, {"type": "IntegerValue", "value": 802}]}}'

        self.send_header("Content-Length", str(len(returndata)))
        self.end_headers()
        self.wfile.write(returndata)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        try:
            parsed_path = urlparse.urlparse(self.path)
            params = dict([p.split('=') for p in parsed_path[4].split('&')])
            func = params["func"]
            args = urllib2.unquote(params["args"])
            if func not in ["read", "keepalive", "get_files"]:
                returndata = '{"type": "MvKReadLog", "value": {"keys": [{"type": "StringValue", "value": "status_message"}, {"type": "StringValue", "value": "status_code"}], "values": [{"type": "StringValue", "value": "Unsupported GET operation"}, {"type": "IntegerValue", "value": 804}]}}'
            if func == "keepalive":
                MvKHandler.controller.addInput(Event("keepalive", "request", [params["client_id"]]))
                returndata = '{"type": "MvKReadLog", "value": {"keys": [{"type": "StringValue", "value": "status_message"}, {"type": "StringValue", "value": "status_code"}], "values": [{"type": "StringValue", "value": "Keepalive OK"}, {"type": "IntegerValue", "value": 699}]}}'
            else:
                MvKHandler.controller.addInput(Event("request", "request", [func, args, params["client_id"]]))
                returndata = MvKHandler.listener.fetch(-1).getParameters()[0]
        except Exception:
            import traceback
            print(traceback.format_exc())
            returndata = '{"type": "MvKReadLog", "value": {"keys": [{"type": "StringValue", "value": "status_message"}, {"type": "StringValue", "value": "status_code"}], "values": [{"type": "StringValue", "value": "HTTP internal GET problem"}, {"type": "IntegerValue", "value": 803}]}}'

        self.send_header('Content-Length', str(len(returndata)))
        self.end_headers()
        self.wfile.write(returndata)

def run_server(port):
    server_address = ("", port)
    MvKHandler.controller = server.Controller()
    MvKHandler.listener = MvKHandler.controller.addOutputListener("reply")
    MvKHandler.controller.start()
    http_server = BaseHTTPServer.HTTPServer(server_address, MvKHandler)
    try:
        http_server.serve_forever()
    finally:
        MvKHandler.controller.stop()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Requires port number as argument")
        sys.exit(1)
    else:
        run_server(int(sys.argv[1]))
