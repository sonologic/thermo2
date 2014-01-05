from time import time

class Timer:
    def __init__(self,period):
        self.period = period
        self.last_trigger = time()
        self.next_trigger = self.last_trigger + period

    def getPeriod(self):
        return self.period

    def reset(self):
        self.last_trigger = time()
        self.next_trigger = self.last_trigger + self.period
        return self.last_trigger       

    def poll(self):
        t = time()

        if t < self.next_trigger:
            return None

        self.last_trigger = t
        lateness = t - self.next_trigger

        self.next_trigger = self.next_trigger + self.period

        return lateness        
