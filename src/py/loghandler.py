import logging

class LogHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
        self.setFormatter(logging.Formatter(fmt="%(asctime)s %(levelname)s %(message)s"))

    def emit(self, record):
        print self.format(record)

