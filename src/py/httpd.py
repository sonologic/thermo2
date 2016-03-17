import BaseHTTPServer
import json
import urlparse
import re
from parser_constants import ParserConstants

class MyRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        path_elm = self.path.split('/')
        path_elm = path_elm[1:]

        if len(path_elm)!=2:
            self.send_error(500, "Invalid path")
        else:
            if path_elm[0]!='get':
                self.send_error(500, "Invalid command")
            label = path_elm[1]

            # todo: sanitize label..

            event = self.server.scheduler.getValue(label)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            if event==None:
                self.wfile.write(json.dumps({ 'label' : label }))
            else:
                (value, t) = event
                self.wfile.write(json.dumps({ 'label' : label, 'value' : value, 't' : t }))

    def do_POST(self):
        path_elm = self.path.split('/')
        path_elm = path_elm[1:]

        if len(path_elm)!=2:
            self.send_error(500, "Invalid path")
        else:
            if path_elm[0]!='set':
                self.send_error(500, "Invalid command")
                return

            # todo: sanitize input..
            label = path_elm[1]

            # todo: sanitize post input
            length = int(self.headers['Content-Length'])
            post_data = urlparse.parse_qs(self.rfile.read(length).decode('utf-8'))

            if not 't' in post_data.keys():
                self.send_error(500, "POST error")
                return
            if not 'value' in post_data.keys():
                self.send_error(500, "POST error")
                return

            value = post_data['value'][0]
            t = post_data['t'][0]

            if not re.match('^'+ParserConstants.RE_FLOAT+'$', t):
                self.send_error(500, "POST error")
                return

            t = float(t)

            if re.match('^'+ParserConstants.RE_INTEGER+'$', value):
                value = int(value)
            elif re.match('^'+ParserConstants.RE_FLOAT+'$', value):
                value = float(value)

            self.server.scheduler.setValue(label, value, t)

            event = self.server.scheduler.getValue(label)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            if event==None:
                self.wfile.write(json.dumps({ 'label' : label }))
            else:
                (value, t) = event
                self.wfile.write(json.dumps({ 'label' : label, 'value' : value, 't' : t }))

class Httpd(BaseHTTPServer.HTTPServer):
    def __init__(self, addr, scheduler):
        if type(addr)==type(""):
            split = addr.split(":")
            if len(split)!=2:
                raise Exception("invalid server address")
            addr = (split[0], int(split[1]))
        self.scheduler = scheduler
        BaseHTTPServer.HTTPServer.__init__(self, addr, MyRequestHandler)
        
