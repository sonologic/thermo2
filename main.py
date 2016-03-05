#!/usr/bin/env python

import argparse
from config import Config
from thermo2 import Thermo2
from time import sleep
import logging

class LogHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        self.setFormatter(logging.Formatter(fmt="%(asctime)s %(levelname)s %(message)s"))

    def emit(self, record):
        print self.format(record)


class Main(object):
    def __init__(self):
        self.logger = logging.getLogger('')
        self.logger.setLevel(logging.WARNING)
        self.logger.addHandler(LogHandler())
        self.logger.error("test")

    def main(self):
        self.parseArgs()

    def parseArgs(self):
        parser = argparse.ArgumentParser(description='Thermo2 arguments')
        parser.add_argument("--config", nargs=1, help='config file', required=True)
        parser.add_argument("--delay", nargs=1, help='delay in seconds (float)', default=0.5)
        parser.add_argument("--verbose", help='be verbose', action='store_const', const=True, default=False)
        parser.add_argument("--debug", help='be more verbose', action='store_const', const=True, default=False)

        args = parser.parse_args()

        if args.debug:
            self.logger.setLevel(logging.DEBUG)
        elif args.verbose:
            self.logger.setLevel(logging.INFO)

        self.logger.debug("----[ arguments:")
        self.logger.debug(str(args))

        config_txt = file(args.config[0]).read()

        self.logger.debug("----[ config text:")
        self.logger.debug(config_txt)

        config = Config(config_txt)

        self.logger.debug("----[ parsed config:")
        self.logger.debug(str(config))

        thermo2 = Thermo2(config)

        thermo2.verbose = args.verbose

        delay = args.delay

        while True:
            if thermo2.run():
                sleep(delay)


if __name__ == '__main__':
    main = Main()

    main.main()
