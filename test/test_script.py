import unittest
from time import time
import sys

if __name__ == "__main__":
    sys.path.insert(0, "../")

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


if __name__ == "__main__":
    unittest.main()
