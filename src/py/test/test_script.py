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
        """Test Script parser"""
        script = Script('''sum := op1_value + op2_value
                           emit sum_value(sum)''')

    def test_parser_nl_ending(self):
        """Test Script parser with newline ending"""
        script = Script('''sum := op1_value + op2_value
                           emit sum_value(sum)
                        ''')

    def test_parser_fail(self):
        """Test Script parser failure"""
        try:
            script = Script('''foo''')
        except ScriptParseError:
            pass
        else:
            self.fail("Expected a ScriptParseError")

    def test_parser_if(self):
        """Test Script parser for if construction"""
        script = Script('''if value < 10 then
                               emit small_value(value)
                           endif''')

    def test_eval(self):
        """Test Script evaluation of assignment and emit"""
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

    def test_eval_emit_int(self):
        """Test Script evaluation of emit of integer"""
        script = Script('''emit test(23)''')

        rv = script.eval()

        self.assertEqual(isinstance(rv,list),True)
        self.assertEqual(len(rv),1)

        e = rv[0]

        self.assertEqual(isinstance(e,SensorEvent),True)
        self.assertEqual(e.getLabel(),'test')
        self.assertEqual(e.getValue(),23)



    def test_eval_if_pass(self):
        """Test Script if evaluation for pass"""
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
        """Test Script if evaluation for fail"""
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

    def test_eval_simple_in(self):
        script = Script('''emit simple_event''')

        e = Event(time(), 'simple_event')

        rv = script.eval(e)

        self.assertEqual(isinstance(rv,list),True)
        self.assertEqual(len(rv),1)

        e = rv[0]

        self.assertEqual(isinstance(e,Event),True)
        self.assertEqual(e.getLabel(),'simple_event')

    def test_eval_persist_state(self):
        script = Script('''a := a + 1''')

        script.var = { 'a' : 0 }

        self.assertEqual(script.eval(), [])
        self.assertEqual(script.var['a'], 1)

        self.assertEqual(script.eval(), [])
        self.assertEqual(script.var['a'], 2)

        self.assertEqual(script.eval(), [])
        self.assertEqual(script.var['a'], 3)

if __name__ == "__main__":
    unittest.main()
