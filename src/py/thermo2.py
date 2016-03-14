from config import Config
from scheduler_caching import CachingScheduler
import logging

class Thermo2:

    def __init__(self, config):
        self.scheduler = CachingScheduler()
        self.scheduler.bind(config)
        self.idle = False
        self.tick = 0
        self.verbose = False
        self.logger = logging.getLogger('thermo2.'+__name__)

    def run(self):
        state = self.scheduler.schedule()
        if type(state)==type(""):
            if state == 'idle':
                if self.idle == False:
                    self.logger.info(str(self.tick) + ": idle")
                    self.idle = True
            else:
                self.logger.info(str(self.tick) + ": " + str(state) + ", queue: " + str(self.scheduler.events))
                self.idle = False
        else:
            self.logger.info(str(self.tick) + ": " + str(state) + ", queue: " + str(self.scheduler.events))
            self.idle = False

        self.tick+=1;

        return self.idle
