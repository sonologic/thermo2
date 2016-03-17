#!/usr/bin/env python

import unittest
import sys, os
import logging
import argparse

sys.path.insert(0, "../")

from loghandler import LogHandler
from test_thermo2 import Thermo2Test
from test_scheduler import SchedulerTest
from test_scheduler_caching import CachingSchedulerTest
from test_timer import TimerTest
from test_event import EventTest
from test_event_listener import EventListenerTest
from test_actor import ActorTest
from test_actor_post import PostActorTest
from test_sensor_event import SensorEventTest
from test_sensor import SensorTest
from test_sensor_json import JsonSensorTest
from test_event_processor import EventProcessorTest
from test_event_processor_delay import EventProcessorDelayTest
from test_script import ScriptTest
from test_script_expression import ScriptExpressionTest
from test_line_reader import LineReaderTest
from test_process import ProcessTest
from test_myexceptions import MyexceptionsTest
from test_config import ConfigTest
from test_httpd import HttpdTest

if __name__ == "__main__":


        parser = argparse.ArgumentParser(description='Test runner')
        parser.add_argument('--verbose', dest='verbose', action='store_const',
                           const=True, default=False,
                           help='Verbose output')

        args = parser.parse_args()

        logger = logging.getLogger('')
        if args.verbose:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.ERROR)
        logger.addHandler(LogHandler())

        suites = unittest.TestSuite()

        suite = unittest.TestSuite()

        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(MyexceptionsTest))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(LineReaderTest))

        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(EventTest))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(EventListenerTest))

        suites.addTest(suite)
        suite = unittest.TestSuite()

        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ActorTest))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(PostActorTest))

        suites.addTest(suite)
        suite = unittest.TestSuite()

        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TimerTest))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(EventProcessorTest))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(EventProcessorDelayTest))

        suites.addTest(suite)
        suite = unittest.TestSuite()

        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(SensorEventTest))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(SensorTest))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(JsonSensorTest))

        suites.addTest(suite)
        suite = unittest.TestSuite()

        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ScriptTest))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ScriptExpressionTest))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ProcessTest))

        suites.addTest(suite)
        suite = unittest.TestSuite()

        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(SchedulerTest))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(CachingSchedulerTest))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ConfigTest))
        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Thermo2Test))

        suites.addTest(suite)

        suite = unittest.TestSuite()

        suite.addTest(unittest.TestLoader().loadTestsFromTestCase(HttpdTest))

        suites.addTest(suite)

        unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(suites))

