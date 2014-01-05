import unittest

from test_thermo2 import Thermo2Test
from test_scheduler import SchedulerTest
from test_timer import TimerTest
from test_event import EventTest

suite = []

suite.append(unittest.TestLoader().loadTestsFromTestCase(Thermo2Test))
suite.append(unittest.TestLoader().loadTestsFromTestCase(SchedulerTest))
suite.append(unittest.TestLoader().loadTestsFromTestCase(TimerTest))
suite.append(unittest.TestLoader().loadTestsFromTestCase(EventTest))

unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(suite))

