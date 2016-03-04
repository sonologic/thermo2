from config import Config
from scheduler import Scheduler

class Thermo2:

    def __init__(self, config):
        self.scheduler = Scheduler()
        self.scheduler.bind(config)
        self.idle = False
        self.tick = 0

    def run(self):
        state = self.scheduler.schedule()
        if type(state)==type(""):
            if state == 'idle':
                if self.idle == False:
                    #print str(self.tick) + ": idle"
                    self.idle = True
            else:
                #print str(self.tick) + ": " + str(state) + ", queue: " + str(self.scheduler.events)
                self.idle = False
        else:
            #print str(self.tick) + ": " + str(state) + ", queue: " + str(self.scheduler.events)
            self.idle = False

        self.tick+=1;

        return self.idle
