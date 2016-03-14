import unittest
from time import time, sleep
import sys

if __name__ == "__main__":
    sys.path.insert(0, "../")

from scheduler import Scheduler
from config import Config
from event_listener import EventListener
from event import Event
from timer import Timer


class SchedulerTestListener(EventListener):

    def __init__(self, label):
        EventListener.__init__(self)
        self.count = 0
        self.label = label
        self.addEvent(label)

    def event(self, event):
        if event.getLabel() == self.label:
            self.count = self.count + 1
            return []
        return []


class SchedulerTest(unittest.TestCase):

    def test_scheduler_schedule(self):
        self.scheduler = Scheduler()
        self.assertEqual(self.scheduler.schedule(),'idle')

    def test_scheduler_insert_event(self):
        scheduler = Scheduler()
        
        t = time()
        while time() < t+1:
            self.assertEqual(scheduler.schedule(),'idle')
            sleep(0.05)
     
        event = Event(time(), 'test_event')
        self.assertEqual(scheduler.schedule([event]),event)

    def test_scheduler_add_timer(self):
        self.scheduler = Scheduler()

        self.scheduler.add_timer(2, 'test_timer')

        self.assertEqual(len(self.scheduler.timers),1);

        self.assertTrue('test_timer' in self.scheduler.timers.keys())

        self.assertEqual(self.scheduler.timers['test_timer'].getPeriod(),2)

    def test_scheduler_timer(self):
        self.scheduler = Scheduler()
        error = 0.1
        delay = 2

        startTime = time()
        self.scheduler.add_timer(delay,'test_timer')
        while time() < startTime+delay-error:
            self.assertEqual(self.scheduler.schedule(),'idle')
            sleep(error/10)

        event_count = 0

        while time() < startTime+delay+error:
            event = self.scheduler.schedule()

            if event!='idle' and event.label=='test_timer':
                event_count = event_count + 1
            sleep(error/10)

        self.assertEqual(event_count,1)

    def test_scheduler_add_listener(self):
        self.scheduler = Scheduler()

        listener = SchedulerTestListener('foo')

        self.scheduler.add_listener(listener)

        self.assertEqual(len(self.scheduler.listeners),1)
        self.assertEqual(self.scheduler.listeners['foo'],[listener])

    def test_scheduler_add_bad_listener(self):
        self.scheduler = Scheduler()

        listener = SchedulerTestListener('foo')
        listener.addEvent(None)

        type_error = False

        try:
            self.scheduler.add_listener(listener)
        except TypeError:
            type_error = True

        self.assertEqual(type_error,True)

    def test_scheduler_listener(self):
        scheduler = Scheduler()

        listener = SchedulerTestListener('test_event')

        scheduler.add_listener(listener)

        self.assertEqual(scheduler.schedule(),'idle')

        event = Event(time(),'test_event')

        self.assertEqual(scheduler.schedule([event]),event)

        self.assertEqual(listener.count,1)

    def test_scheduler_timed_listener(self):
        scheduler = Scheduler()

        listener = SchedulerTestListener('test_event')

        scheduler.add_listener(listener)

        scheduler.add_timer(0.250,'test_event')

        start = time()
        count = 0

        while time() < start+1.05:
            event = scheduler.schedule()
    
            if event!='idle' and event.label == 'test_event':
                count = count + 1
            sleep(0.05)

        self.assertEqual(count,4)
        self.assertEqual(listener.count,4)

    def test_scheduler_bind_config(self):
        scheduler = Scheduler()

        config = Config('''
                        timer test_timer {
                            interval: 2
                            event: test_timer_event
                        }

                        process demo_add {
                            trigger: op1_value, op2_value
                            script: {
                                sum := op1_value + op2_value
                                emit sum_value(sum)
                            }
                        }

                        process gen_op1 {
                            trigger: test_timer_event
                            script: {
                                emit op1_value(2)
                            }
                        }

                        process gen_op2 {
                            trigger: test_timer_event
                            script: {
                                emit op2_value(3)
                            }
                        }''')

        scheduler.bind(config)


if __name__ == "__main__":
    unittest.main()
