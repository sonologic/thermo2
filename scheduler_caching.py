from scheduler import Scheduler
from sensor_event import SensorEvent

class CachingScheduler(Scheduler):
    def __init__(self):
        Scheduler.__init__(self)
        self.cache = {}

    def getValue(self, label):
        if label in self.cache.keys():
            return self.cache[label]
        return None

    def setValue(self, label, value, t):
        event = SensorEvent(t, label, value)
        self.events += [event]

    def schedule(self, events=[]):
        event = Scheduler.schedule(self, events)

        if isinstance(event, SensorEvent):
            self.cache[event.label] = (event.value, event.t)

        return event
