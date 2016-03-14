import unittest

from sensor_event import SensorEvent

class SensorEventTest(unittest.TestCase):

    def test_sensor_event(self):
        event = SensorEvent(42,'test_sensor_event',1337)
        self.assertEqual(event.getTime(), 42)
        self.assertEqual(event.getLabel(), 'test_sensor_event')
        self.assertEqual(event.getValue(), 1337)

if __name__ == "__main__":
    unittest.main()
