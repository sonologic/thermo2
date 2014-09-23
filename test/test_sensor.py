import unittest
from time import time
from event import Event
from sensor import Sensor

class SensorTest(unittest.TestCase):

    def test_sensor(self):
        sensor = Sensor('test_sensor','test_sensor_event')
        sensor.value = False

        sensor_event = Event(time(),'test_sensor_event')
      
        events = sensor.event(sensor_event)
 
        self.assertEqual(len(events),2)
        self.assertEqual(events[0].getLabel(),'test_sensor_event')
        self.assertEqual(events[1].getLabel(),'test_sensor')
        self.assertEqual(events[1].getValue(),False)

        events = sensor.event(sensor_event)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0].getLabel(),'test_sensor_event')

        sensor.value = True
        events = sensor.event(sensor_event)
        self.assertEqual(len(events),2)
        self.assertEqual(events[0].getLabel(),'test_sensor_event')
        self.assertEqual(events[1].getLabel(),'test_sensor')
        self.assertEqual(events[1].getValue(),True)

        events = sensor.event(sensor_event)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0].getLabel(),'test_sensor_event')

        sensor.value = False
        events = sensor.event(sensor_event)
        self.assertEqual(len(events),2)
        self.assertEqual(events[0].getLabel(),'test_sensor_event')
        self.assertEqual(events[1].getLabel(),'test_sensor')
        self.assertEqual(events[1].getValue(),False)

        events = sensor.event(sensor_event)
        self.assertEqual(len(events),1)
        self.assertEqual(events[0].getLabel(),'test_sensor_event')

if __name__ == "__main__":
    unittest.main()

