import unittest
import sys
import urlparse
import BaseHTTPServer
from multiprocessing import Process

if __name__ == "__main__":
    sys.path.insert(0, "../")

from actor_post import PostActor
from sensor_event import SensorEvent

class http_handler(BaseHTTPServer.BaseHTTPRequestHandler):
    #test_sequence = [ 15, 15, 21, 21, 18 ]
    #test_no = 0

    def do_POST(self):
        print "post"
        #val = http_handler.test_sequence[http_handler.test_no]
        #http_handler.test_no = (http_handler.test_no + 1) % len(http_handler.test_sequence)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write('{')

        length = int(self.headers['Content-Length'])
        post_data = urlparse.parse_qs(self.rfile.read(length).decode('utf-8'))
        first = True
        for key, value in post_data.iteritems():
            if first:
                first = False
            else:
                self.wfile.write(',')
            self.server.__dict__["last_post_test_" + str(key)] = value
            self.wfile.write("\"%s\":\"%s\"" % (key, value))
        self.wfile.write('}')

def http_server():
    server_address = ('127.0.0.1', 53901)
    httpd = BaseHTTPServer.HTTPServer(server_address, http_handler)

    httpd.handle_request()

    ec = 0

    if httpd.last_post_test_t[0] != '42':
        ec |= 1
    if httpd.last_post_test_label[0] != 'test_event':
        ec |= 2
    if httpd.last_post_test_value[0] != '23':
        ec |= 4

    exit(ec)

class PostActorTest(unittest.TestCase):

    def test_actor(self):
        # start http server
        serverProcess = Process(target=http_server)
        serverProcess.start()

        a = PostActor()
        a.url = 'http://127.0.0.1:53901/'

        a.addEvent('test_event')

        e = SensorEvent(42, 'test_event', 23)

        events = a.event(e)

        self.assertEqual(events, [e])

        # terminate server and test return code
        serverProcess.join()

        self.assertEqual(serverProcess.exitcode, 0)

if __name__ == "__main__":
    unittest.main()
