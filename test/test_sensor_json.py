import unittest
from time import time
import BaseHTTPServer
from Queue import Empty
import sys

if __name__ == "__main__":
    sys.path.insert(0, "../")

from event import Event
from sensor_json import JsonSensor
from multiprocessing import Process,Queue

class http_handler(BaseHTTPServer.BaseHTTPRequestHandler):
    test_sequence = [ 15, 15, 21, 21, 18 ]
    test_no = 0

    def do_GET(self):
        val = http_handler.test_sequence[http_handler.test_no]
        http_handler.test_no = (http_handler.test_no + 1) % len(http_handler.test_sequence)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write('{ "value": ' + str(val) + ' }')

def http_server():
    server_address = ('127.0.0.1', 53901)
    httpd = BaseHTTPServer.HTTPServer(server_address, http_handler)
    while True:
        httpd.handle_request()

class JsonSensorTest(unittest.TestCase):
    def setUp(self):
        self.serverProcess = Process(target=http_server)
        self.serverProcess.start()

    def tearDown(self):
        self.serverProcess.terminate()
        self.serverProcess.join()

    def test_json_sensor(self):
        """JsonSensor"""
        sensor = JsonSensor()
        sensor.url='http://localhost:53901/setting.json'
        sensor.label='test_sensor'
        sensor.addEvent('test_sensor_event')
        sensor.value = False

        sensor_event = Event(time(),'test_sensor_event')
      
        events = sensor.event(sensor_event)

        self.assertEqual(len(events),2)
        self.assertEqual(events[0].getLabel(),'test_sensor_event')
        self.assertEqual(events[1].getLabel(),'test_sensor')
        self.assertEqual(events[1].getValue(),15)

        events = sensor.event(sensor_event)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0].getLabel(),'test_sensor_event')

        events = sensor.event(sensor_event)
        self.assertEqual(len(events),2)
        self.assertEqual(events[0].getLabel(),'test_sensor_event')
        self.assertEqual(events[1].getLabel(),'test_sensor')
        self.assertEqual(events[1].getValue(),21)

        events = sensor.event(sensor_event)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0].getLabel(),'test_sensor_event')

if __name__ == "__main__":
    unittest.main()

