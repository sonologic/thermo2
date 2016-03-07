#!/usr/bin/env python

import argparse
from config import Config
from thermo2 import Thermo2
from time import sleep
import logging
from loghandler import LogHandler

class Main(object):
    def __init__(self):
        self.logger = logging.getLogger('')
        self.logger.setLevel(logging.WARNING)
        self.logger.addHandler(LogHandler())

    def main(self):
        self.parseArgs()

        if self.args.debug:
            self.logger.setLevel(logging.DEBUG)
        elif self.args.verbose:
            self.logger.setLevel(logging.INFO)

        self.logger.info("Thermo2 starting up")

        self.logger.debug("----[ arguments:")
        self.logger.debug(str(self.args))

        config_txt = file(self.args.config[0]).read()

        self.logger.debug("----[ config text:")
        self.logger.debug(config_txt)

        config = Config(config_txt)

        self.logger.debug("----[ parsed config:")
        self.logger.debug(str(config))

        thermo2 = Thermo2(config)

        thermo2.verbose = self.args.verbose

        delay = self.args.delay

        while True:
            if thermo2.run():
                sleep(delay)

    def parseArgs(self):
        parser = argparse.ArgumentParser(description='Thermo2 arguments')
        parser.add_argument("--config", nargs=1, help='config file', required=True)
        parser.add_argument("--delay", nargs=1, help='delay in seconds (float)', default=0.5)
        parser.add_argument("--verbose", help='be verbose', action='store_const', const=True, default=False)
        parser.add_argument("--debug", help='be more verbose', action='store_const', const=True, default=False)

        self.args = parser.parse_args()

if __name__ == '__main__':
    main = Main()

    main.main()
