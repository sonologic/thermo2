import unittest
from time import time
import sys

if __name__ == "__main__":
    sys.path.insert(0, "../")

from sensor_event import *
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


if __name__ == "__main__":
    unittest.main()
