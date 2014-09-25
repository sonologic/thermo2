import unittest
from time import time
import sys
import re

if __name__ == "__main__":
    sys.path.insert(0, "../")

from line_reader import *

class LineReaderTest(unittest.TestCase):

    def test_line_reader(self):
        r = LineReader('''line1
                          line2
                          line3''')
        
        self.assertEqual(r.eof(),False)

        for i in range(1,4):
            self.assertEqual(r.eof(),False)
            (n,s) = r.consume()
            self.assertEqual(n,i)
            if re.match('^\s*line%d\s*$' % i,s) == None:
                self.fail("Line %d does not match" % i)

        self.assertEqual(r.eof(),True)

if __name__ == "__main__":
    unittest.main()
