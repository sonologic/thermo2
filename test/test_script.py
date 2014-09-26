import unittest
from time import time
import sys

if __name__ == "__main__":
    sys.path.insert(0, "../")

from sensor_event import *
from event import *
from script import *

class ScriptTest(unittest.TestCase):

    def test_parser(self):
        script = Script('''sum := op1_value + op2_value
                           emit sum_value(sum)''')

    def test_parser_nl_ending(self):
        script = Script('''sum := op1_value + op2_value
                           emit sum_value(sum)
                        ''')

    def test_parser_fail(self):
        try:
            script = Script('''foo''')
        except ScriptParseError:
            pass
        else:
            self.fail("Expected a ScriptParseError")

    def test_parser_if(self):
        script = Script('''if value < 10 then
                               emit small_value(value)
                           endif''')

    def test_eval(self):
        script = Script('''sum := op1_value + op2_value
                           emit sum_value(sum)''')

        e1 = SensorEvent(time(), 'op1_value', 2)
        rv = script.eval(e1)

        self.assertEqual(rv,[])

        e2 = SensorEvent(time(), 'op2_value', 3)
        rv = script.eval(e2)

        self.assertEqual(isinstance(rv,list),True)
        self.assertEqual(len(rv),1)

        e3 = rv[0]

        self.assertEqual(isinstance(e3,SensorEvent),True)
        self.assertEqual(e3.getLabel(),'sum_value')
        self.assertEqual(e3.getValue(),5)

    def test_eval_if_pass(self):
        script = Script('''if value < 10 then
                               emit small_value(value)
                           endif''')
        rv = script.eval(SensorEvent(time(),'value',2))

        self.assertEqual(isinstance(rv,list),True)
        self.assertEqual(len(rv),1)

        e = rv[0]

        self.assertEqual(isinstance(e,SensorEvent),True)
        self.assertEqual(e.getLabel(),'small_value')
        self.assertEqual(e.getValue(),2)


    def test_eval_if_fail(self):
        script = Script('''if value > 10 then
                               emit large_value(value)
                           endif''')
        rv = script.eval(SensorEvent(time(),'value',2))

        self.assertEqual(rv,[])

    def test_eval_emit_simple(self):
        script = Script('''emit simple_event''')

        rv = script.eval()

        self.assertEqual(isinstance(rv,list),True)
        self.assertEqual(len(rv),1)

        e = rv[0]

        self.assertEqual(isinstance(e,Event),True)
        self.assertEqual(e.getLabel(),'simple_event')
        


if __name__ == "__main__":
    unittest.main()
