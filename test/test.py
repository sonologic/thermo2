import unittest
import sys, os

sys.path.insert(0, "../")

from test_thermo2 import Thermo2Test
from test_scheduler import SchedulerTest
from test_timer import TimerTest
from test_event import EventTest
from test_event_listener import EventListenerTest
from test_sensor_event import SensorEventTest
from test_sensor import SensorTest

if __name__ == "__main__":

        suite = []

        suite.append(unittest.TestLoader().loadTestsFromTestCase(Thermo2Test))
        suite.append(unittest.TestLoader().loadTestsFromTestCase(SchedulerTest))
        suite.append(unittest.TestLoader().loadTestsFromTestCase(TimerTest))
        suite.append(unittest.TestLoader().loadTestsFromTestCase(EventTest))
        suite.append(unittest.TestLoader().loadTestsFromTestCase(EventListenerTest))
        suite.append(unittest.TestLoader().loadTestsFromTestCase(SensorEventTest))
        suite.append(unittest.TestLoader().loadTestsFromTestCase(SensorTest))

        unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(suite))

