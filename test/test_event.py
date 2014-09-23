import unittest
from event import Event
from time import time

class EventTest(unittest.TestCase):

    def test_event_setup(self):
        t = time()
        event = Event(t,'test_event')
        self.assertEqual(event.getTime(),t)
        self.assertEqual(event.getLabel(),'test_event')

if __name__ == "__main__":
    unittest.main()
