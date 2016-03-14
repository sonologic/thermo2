import unittest
import sys

if __name__ == "__main__":
    sys.path.insert(0, "../")

from scheduler_caching import CachingScheduler
from sensor_event import SensorEvent

class CachingSchedulerTest(unittest.TestCase):

    def test_caching_scheduler(self):
        s = CachingScheduler()

        self.assertEqual(s.getValue('sensor_event'), None)
        self.assertEqual(s.getValue('foo'), None)
        self.assertEqual(s.getValue('bar'), None)

        e = SensorEvent(42, 'sensor_event', 23)
        event = s.schedule([e])

        self.assertEqual(s.getValue('sensor_event'), (23, 42))
        self.assertEqual(s.getValue('foo'), None)
        self.assertEqual(s.getValue('bar'), None)

        e = SensorEvent(1337, 'foo', 314)
        event = s.schedule([e])

        self.assertEqual(s.getValue('sensor_event'), (23, 42))
        self.assertEqual(s.getValue('foo'), (314, 1337))
        self.assertEqual(s.getValue('bar'), None)


if __name__ == "__main__":
    unittest.main()
