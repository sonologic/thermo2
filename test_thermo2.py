import unittest
from thermo2 import Thermo2

class Thermo2Test(unittest.TestCase):

    def test_thermo2_initialization(self):
        thermo2 = Thermo2()

    def test_thermo2_iterate(self):
        thermo2 = Thermo2()
        self.assertIsInstance(thermo2.iterate(), int)

if __name__ == "__main__":
    unittest.main()
