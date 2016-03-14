import unittest
import sys

if __name__ == "__main__":
    sys.path.insert(0, "../")

from actor import Actor
from sensor_event import SensorEvent

class ActorTest(unittest.TestCase):

    def test_actor(self):
        a = Actor()

        a.addEvent('test_event')

        e = SensorEvent(42, 'test_event', 23)

        events = a.event(e)

        self.assertEqual(events, [e])
        self.assertEqual(a.value, 23)
        self.assertEqual(a.label, 'test_event')
        self.assertEqual(a.t, 42)

if __name__ == "__main__":
    sys.path.insert(0, "../")

    unittest.main()
