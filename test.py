import unittest

from test_thermo2 import Thermo2Test
from test_scheduler import SchedulerTest
from test_timer import TimerTest

suite1 = unittest.TestLoader().loadTestsFromTestCase(Thermo2Test)
suite2 = unittest.TestLoader().loadTestsFromTestCase(SchedulerTest)
suite3 = unittest.TestLoader().loadTestsFromTestCase(TimerTest)

suite = unittest.TestSuite([suite1, suite2, suite3])

unittest.TextTestRunner(verbosity=2).run(suite)

