import unittest
from time import time
import sys
import re

if __name__ == "__main__":
    sys.path.insert(0, "../")

from script import *
from process import *

class ProcessTest(unittest.TestCase):

    def test_line_reader(self):
        p = Process()
        p.label = 'test'
        p.script = Script('emit testout')

        rv = p.event(Event(time(),'testin'))

        self.assertEqual(isinstance(rv,list),True)
        self.assertEqual(len(rv),1)

        e = rv[0]

        self.assertEqual(isinstance(e,Event),True)
        self.assertEqual(e.getLabel(),'testout')


if __name__ == "__main__":
    unittest.main()
