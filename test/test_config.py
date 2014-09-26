import unittest
from time import time
import sys

if __name__ == "__main__":
    sys.path.insert(0, "../")

from config import *

class ConfigTest(unittest.TestCase):

    def test_parser(self):
        exp = Config('''process simple {
                        trigger: setting_value, sensor_value
                        script: {
                                if setting_value > sensor_value then
                                    emit heating_on
                                endif
                                if setting_value < sensor_value then
                                    emit heating_off
                                endif
                            }
                        }''')

    def test_parser_two(self):
        exp = Config('''process simple {
                        trigger: setting_value, sensor_value
                        script: {
                                if setting_value > sensor_value then
                                    emit heating_on
                                endif
                                if setting_value < sensor_value then
                                    emit heating_off
                                endif
                            }
                        }

                        process simple2 {
                            trigger: in_value
                            script: {
                                emit out_value(in_value)
                            }
                        }''')

if __name__ == "__main__":
    unittest.main()
