import unittest
from scheduler import Scheduler
from time import time

class SchedulerTest(unittest.TestCase):

    def test_scheduler_schedule(self):
        self.scheduler = Scheduler()
        self.assertEqual(self.scheduler.schedule(),'idle')

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

    def test_scheduler_add_timer(self):
        self.scheduler = Scheduler()

        self.scheduler.add_timer(2, 'test_timer')

        self.assertEqual(len(self.scheduler.timers),1);

        self.assertTrue('test_timer' in self.scheduler.timers.keys())

        self.assertEqual(self.scheduler.timers['test_timer'].getPeriod(),2)

if __name__ == "__main__":
    unittest.main()
