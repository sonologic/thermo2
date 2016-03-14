import unittest
from event import Event
from event_processor import EventProcessor
from time import time

class EventProcessorTest(unittest.TestCase):

    def test_return_event_list(self):
        e = Event(time(), 'foo')
        p = EventProcessor(e)

        p.start()

        p.join()

        self.assertEqual(p.returnEvents,[])

if __name__ == "__main__":
    unittest.main()
