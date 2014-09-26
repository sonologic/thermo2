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
from test_event_processor import EventProcessorTest
from test_event_processor_delay import EventProcessorDelayTest
from test_script import ScriptTest
from test_script_expression import ScriptExpressionTest
from test_line_reader import LineReaderTest
from test_process import ProcessTest
from test_myexceptions import MyexceptionsTest

if __name__ == "__main__":

        suite = []

        suite.append(unittest.TestLoader().loadTestsFromTestCase(MyexceptionsTest))
        suite.append(unittest.TestLoader().loadTestsFromTestCase(LineReaderTest))
        suite.append(unittest.TestLoader().loadTestsFromTestCase(Thermo2Test))
        suite.append(unittest.TestLoader().loadTestsFromTestCase(SchedulerTest))
        suite.append(unittest.TestLoader().loadTestsFromTestCase(TimerTest))
        suite.append(unittest.TestLoader().loadTestsFromTestCase(EventTest))
        suite.append(unittest.TestLoader().loadTestsFromTestCase(EventListenerTest))
        suite.append(unittest.TestLoader().loadTestsFromTestCase(EventProcessorTest))
        suite.append(unittest.TestLoader().loadTestsFromTestCase(EventProcessorDelayTest))
        suite.append(unittest.TestLoader().loadTestsFromTestCase(SensorEventTest))
        suite.append(unittest.TestLoader().loadTestsFromTestCase(SensorTest))
        suite.append(unittest.TestLoader().loadTestsFromTestCase(ScriptTest))
        suite.append(unittest.TestLoader().loadTestsFromTestCase(ScriptExpressionTest))
        suite.append(unittest.TestLoader().loadTestsFromTestCase(ProcessTest))

        unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(suite))

