from time import time
from event_listener import EventListener
from sensor_event import SensorEvent
import re

class Sensor(EventListener):
        
    def __init__(self):
        EventListener.__init__(self)
        self.value = None
        self.lastValue = None

    def event(self,event):
        if event.getLabel() in self.events:
            self.getValue()
            if self.value != self.lastValue:
                self.lastValue = self.value
                return [event, SensorEvent(time(), self.label, self.value)]
        return [event]

    def getValue(self):
        pass
