import unittest
from event import Event

class EventTest(unittest.TestCase):

    def test_setup(self):
        t = time()
        event = Event(t,'test_event')
        assertEqual(event.getTime(),t)
        assertEqual(event.getLabel(),t)

if __name__ == "__main__":
    unittest.main()
