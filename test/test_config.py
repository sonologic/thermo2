import unittest
from time import time
import sys

if __name__ == "__main__":
    sys.path.insert(0, "../")

from config import *

class ConfigTest(unittest.TestCase):

    def test_parser(self):
        exp = Config('''global {
                            logfile: foobar
                        }

                        process simple {
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

    def test_parser_timer(self):
        config = Config('''timer t1 {
                               interval: 2
                               event: timerevent
                           }''')

        self.assertEqual('t1' in config.timers.keys(), True)
        self.assertEqual(config.timers['t1'].label, 't1')
        self.assertEqual(config.timers['t1'].event, 'timerevent')
        self.assertEqual(config.timers['t1'].period, 2)

    def test_parser_sensor_json(self):
        config = Config('''sensor json {
                               label: test_sensor
                               trigger: test_trigger
                               url: "http://www.koenmartens.nl/setting.json"
                           }''')
        self.assertEqual(len(config.sensors),1)

    def test_parser_sensor_DS18B20(self):
        config = Config('''sensor DS18B20 {
                                label: sensor_event
                                trigger: sensor_trigger
                                id: 28-0000045b3ed5
                           }''')
        self.assertEqual(len(config.sensors),1)

    def test_parser_comment(self):
        config = Config('''# foo bar
                            # baz boo''')

        self.assertEqual(len(config.processes),0)
        self.assertEqual(len(config.timers),0)
        self.assertEqual(len(config.sensors),0)

    def test_parser_global(self):
        config = Config('''global {
                               listen: 10.0.0.1:1234
                               logfile: /var/log/thermo2.log
                           }
                        ''')

        self.assertEqual(config.listen, '10.0.0.1:1234')
        self.assertEqual(config.logfile, '/var/log/thermo2.log')

    def test_parser_global_defaults(self):
        config = Config('')

        self.assertEqual(config.listen, '127.0.0.1:8822')
        self.assertEqual(config.logfile, None)

if __name__ == "__main__":
    unittest.main()
