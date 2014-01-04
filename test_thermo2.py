import unittest
from thermo2 import Thermo2

class Thermo2Test(unittest.TestCase):

    def setUp(self):
        self.thermo2 = Thermo2()

    def test_thermo2_run(self):
        self.assertEqual(self.thermo2.run(), 0)

if __name__ == "__main__":
    unittest.main()
