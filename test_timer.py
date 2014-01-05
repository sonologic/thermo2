import unittest
from time import time
from timer import Timer

class TimerTest(unittest.TestCase):

    def setUp(self):
        self.timer=Timer(1)

    def test_timer_poll(self):
        reset_time = self.timer.reset()
        while time() < reset_time + 1 - 0.05:
            self.assertEqual(self.timer.poll(), None)
        count = 0
        while time() < reset_time + 1 + 0.05:
            poll = self.timer.poll()
            if not poll == None:
                if round(poll) == 0:
                    count = count + 1
        self.assertEqual(count,1)

    def test_timer_poll_count(self):
        reset_time = self.timer.reset()
        count = 0
        while(time() < reset_time + 3.1):
            if self.timer.poll() != None:
                count = count + 1
        self.assertEqual(count,3)

if __name__ == "__main__":
    unittest.main()

