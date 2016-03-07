import unittest
import sys
from multiprocessing import Process
import requests
import json

if __name__ == "__main__":
    sys.path.insert(0, "../")

from scheduler import Scheduler
from scheduler_caching import CachingScheduler
from httpd import Httpd

class TestScheduler(Scheduler):
    def getValue(self, label):
        if label in self.__dict__.keys():
            return self.__dict__[label]
        return None

    def schedule(self, events=[]):
        return 'idle' 


def server_process():
    s = CachingScheduler()
    h = Httpd(('127.0.0.1',36718), s)
    h.serve_forever()


class TestScheduler(Scheduler):
    def getValue(self, label):
        if label in self.__dict__.keys():
            return self.__dict__[label]
        return None

    def schedule(self, events=[]):
        return 'idle' 

class HttpdTest(unittest.TestCase):

    def tearDown(self):
        self.serverProcess.terminate()
        self.serverProcess.join()

    def test_httpd(self):
        self.serverProcess = Process(target=server_process)
        self.serverProcess.start()

        response = requests.get('http://127.0.0.1:36718/get/test_event')

        self.assertEqual(response.status_code, 200)

        self.assertEqual('content-type' in response.headers.keys(), True)
        self.assertEqual(response.headers['Content-type'], 'application/json')

        data = json.loads(response.text)

        self.assertEqual(len(data), 1)
        self.assertEqual('label' in data.keys(), True)
        self.assertEqual(data['label'], 'test_event')

        post_data = {
            't' : 1234,
            'value' : 20.5,
        }
        response = requests.post('http://127.0.0.1:36718/set/test_event', data=post_data)

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.text)

        self.assertEqual(len(data), 1)
        self.assertEqual('label' in data.keys(), True)
        self.assertEqual(data['label'], 'test_event')

        self.serverProcess.terminate()
        self.serverProcess.join()



if __name__ == "__main__":
    unittest.main()
