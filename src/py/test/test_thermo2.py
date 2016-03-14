import unittest
from thermo2 import Thermo2
from config import Config
from time import sleep

class Thermo2Test(unittest.TestCase):

    def setUp(self):
        config = Config('''
                timer test_timer {
                    interval: 0.02 
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
                        emit op2_trigger
                    }
                }

                process gen_op2 {
                    trigger: op2_trigger
                    script: {
                        emit op2_value(3)
                    }
                }''')

        self.thermo2 = Thermo2(config)


    def test_thermo2_run(self):
        """Thermo2 test-runs"""
        for i in range(16):
            #self.assertEqual(self.thermo2.run(), 0)
            ec = self.thermo2.run()

            if i==2:
                self.assertEqual(self.thermo2.scheduler.lastEvent,'test_timer_event')
                self.assertEqual(len(self.thermo2.scheduler.events), 2)
            elif i==3:
                self.assertEqual(self.thermo2.scheduler.lastEvent,'op1_value')
                self.assertEqual(len(self.thermo2.scheduler.events), 1)
            elif i==4:
                self.assertEqual(self.thermo2.scheduler.lastEvent,'op2_trigger')
                self.assertEqual(len(self.thermo2.scheduler.events), 1)
            elif i==5:
                self.assertEqual(self.thermo2.scheduler.lastEvent,'op2_value')
                self.assertEqual(len(self.thermo2.scheduler.events), 1)
            elif i==6:
                self.assertEqual(self.thermo2.scheduler.lastEvent,'sum_value')
                self.assertEqual(len(self.thermo2.scheduler.events), 0)
            elif i==9:
                self.assertEqual(self.thermo2.scheduler.lastEvent,'test_timer_event')
                self.assertEqual(len(self.thermo2.scheduler.events), 2)
            elif i==10:
                self.assertEqual(self.thermo2.scheduler.lastEvent,'op1_value')
                self.assertEqual(len(self.thermo2.scheduler.events), 2)
            elif i==11:
                self.assertEqual(self.thermo2.scheduler.lastEvent,'op2_trigger')
                self.assertEqual(len(self.thermo2.scheduler.events), 2)
            elif i==12:
                self.assertEqual(self.thermo2.scheduler.lastEvent,'sum_value')
                self.assertEqual(len(self.thermo2.scheduler.events), 1)
            elif i==13:
                self.assertEqual(self.thermo2.scheduler.lastEvent,'op2_value')
                self.assertEqual(len(self.thermo2.scheduler.events), 1)
            elif i==14:
                self.assertEqual(self.thermo2.scheduler.lastEvent,'sum_value')
                self.assertEqual(len(self.thermo2.scheduler.events), 0)
            else:
                self.assertEqual(self.thermo2.scheduler.lastEvent,'idle')
                self.assertEqual(len(self.thermo2.scheduler.events), 0)

            if ec:
                sleep(0.01)


if __name__ == "__main__":
    unittest.main()
