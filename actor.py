from time import time
from event_listener import EventListener
from sensor_event import SensorEvent
import re

class Actor(EventListener):
        
    def __init__(self):
        EventListener.__init__(self)
        self.value = None
        self.lastValue = None

    def event(self,event):
        if event.getLabel() in self.events:
            self.actOnValue(event.label, event.t, event.value)
        return [event]

    def actOnValue(self, label, t, value):
        self.label = label
        self.value = value
        self.t = t
