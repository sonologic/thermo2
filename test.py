import unittest

from test_thermo2 import Thermo2Test
from test_scheduler import SchedulerSetupTest

suite1 = unittest.TestLoader().loadTestsFromTestCase(Thermo2Test)
suite2 = unittest.TestLoader().loadTestsFromTestCase(SchedulerSetupTest)

unittest.TextTestRunner(verbosity=2).run(suite1)
unittest.TextTestRunner(verbosity=2).run(suite2)

