import unittest
from time import time
import sys

if __name__ == "__main__":
    sys.path.insert(0, "../")

from script_expression import *

class ScriptExpressionTest(unittest.TestCase):

    def test_parser_id_id(self):
        exp = ScriptExpression('op1_value + op2_value')

    def test_parser_id_int(self):
        exp = ScriptExpression('op1_value + 843')

    def test_parser_int_id(self):
        exp = ScriptExpression('743 + op1_value')

    def test_parser_evaluate_lit_lit(self):
        exp = ScriptExpression('2 + 3')
        rv = exp.eval()
        self.assertEqual(rv, 5)
        
    def test_parser_evaluate_lit_id(self):
        exp = ScriptExpression('19 + foo_bar')
        rv = exp.eval({'foo_bar':12})
        self.assertEqual(rv, 31)
        
    def test_parser_evaluate_id_lit(self):
        exp = ScriptExpression('foo_bar + 31')
        rv = exp.eval({'foo_bar':11})
        self.assertEqual(rv, 42)
        
    def test_parser_evaluate_id_id(self):
        exp = ScriptExpression('foo + bar')
        rv = exp.eval({'foo':3984,'bar':747})
        self.assertEqual(rv, 3984+747)
        
        

    def test_parser_fail(self):
        try:
            exp = ScriptExpression('+1---+')
        except ScriptExpressionParseError:
            pass
        else:
            self.fail("Expected a ScriptExpressionParseError")


if __name__ == "__main__":
    unittest.main()
