import unittest
from time import time
import sys
import re

if __name__ == "__main__":
    sys.path.insert(0, "../")

from myexceptions import *

class MyexceptionsTest(unittest.TestCase):

    def test_raise(self):
        try:
            raise ParserError(123,'foo bar')
        except ParserError as e:
            self.assertEqual(e.lineno, 123)
            self.assertEqual(e.message, 'foo bar') 

if __name__ == "__main__":
    unittest.main()
