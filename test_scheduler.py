import unittest
from scheduler import Scheduler

class SchedulerSetupTest(unittest.TestCase):

    def setUp(self):
        self.scheduler = Scheduler()

class SchedulerScheduleTest(SchedulerSetupTest):

    def test_scheduler_schedule(self):
        self.assertEqual(self.scheduler.schedule(),'idle')

if __name__ == "__main__":
    unittest.main()
