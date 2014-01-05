from timer import Timer

class Scheduler:
    def __init__(self):
        self.timers={}

    def schedule(self):
        for label in self.timers.keys():
            trigger = self.timers[label].poll()
            if not trigger == None:
                return label 
        return 'idle'

    def add_timer(self,period,label):
        timer = Timer(period)
        self.timers[label]=timer

