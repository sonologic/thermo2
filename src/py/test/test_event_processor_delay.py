import unittest
import sys

if __name__ == "__main__":
    sys.path.insert(0, "../")

from event import Event
from event_processor_delay import EventProcessorDelay
from time import time

class EventProcessorDelayTest(unittest.TestCase):

    def test_return_event_list(self):
        error = 0.01

        e = Event(time(), 'foo')
        p = EventProcessorDelay(e,2)

        p.start()

        p.join()

        self.assertEqual(len(p.returnEvents),1)

        re = p.returnEvents[0]

        self.assertEqual(isinstance(re,Event),True)
        self.assertEqual(re.getLabel(),'foo')
        self.assertEqual( e.getTime()+2.0 < re.getTime() + error , True)
        self.assertEqual( e.getTime()+2.0 > re.getTime() - error , True)

if __name__ == "__main__":
    unittest.main()
