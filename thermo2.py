from config import Config
from scheduler import Scheduler

class Thermo2:

    def __init__(self, config):
        self.scheduler = Scheduler()
        self.scheduler.bind(config)
        self.idle = False
        self.tick = 0
        self.verbose = False

    def run(self):
        state = self.scheduler.schedule()
        if type(state)==type(""):
            if state == 'idle':
                if self.idle == False:
                    if self.verbose:
                        print str(self.tick) + ": idle"
                    self.idle = True
            else:
                if self.verbose:
                    print str(self.tick) + ": " + str(state) + ", queue: " + str(self.scheduler.events)
                self.idle = False
        else:
            if self.verbose:
                print str(self.tick) + ": " + str(state) + ", queue: " + str(self.scheduler.events)
            self.idle = False

        self.tick+=1;

        return self.idle
