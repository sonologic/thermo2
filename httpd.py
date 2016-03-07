import BaseHTTPServer
import json
import urlparse

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

        print "post " + str(path_elm)

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

            value = post_data['value']
            t = post_data['t']

            self.server.scheduler.setValue(label, value, t)
            self.server.scheduler.schedule()

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
        self.scheduler = scheduler
        BaseHTTPServer.HTTPServer.__init__(self, addr, MyRequestHandler)
        
