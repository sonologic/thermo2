import unittest
from scheduler import Scheduler
from time import time
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
        while time() < t+2:
            self.assertEqual(scheduler.schedule(),'idle')
     
        event = Event(time(), 'test_event')
        self.assertEqual(scheduler.schedule([event]),'test_event')

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

        event_count = 0

        while time() < startTime+delay+error:
            if(self.scheduler.schedule()=='test_timer'):
                event_count = event_count + 1

        self.assertEqual(event_count,1)

    def test_scheduler_add_listener(self):
        self.scheduler = Scheduler()

        listener = SchedulerTestListener('foo')

        self.scheduler.add_listener(listener)

        self.assertEqual(len(self.scheduler.listeners),1)
        self.assertEqual(self.scheduler.listeners['foo'],[listener])

    def test_scheduler_listener(self):
        scheduler = Scheduler()

        listener = SchedulerTestListener('test_event')

        scheduler.add_listener(listener)

        self.assertEqual(scheduler.schedule(),'idle')

        event = Event(time(),'test_event')

        self.assertEqual(scheduler.schedule([event]),'test_event')

        self.assertEqual(listener.count,1)

    def test_scheduler_timed_listener(self):
        scheduler = Scheduler()

        listener = SchedulerTestListener('test_event')

        scheduler.add_listener(listener)

        scheduler.add_timer(0.250,'test_event')

        start = time()
        count = 0

        while time() < start+1.05:
            if scheduler.schedule() == 'test_event':
                count = count + 1

        self.assertEqual(count,4)
        self.assertEqual(listener.count,4)
 
if __name__ == "__main__":
    unittest.main()
