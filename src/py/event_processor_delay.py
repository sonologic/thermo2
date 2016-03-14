from threading import Thread
from time import sleep,time

from event_processor import EventProcessor
from event import Event

class EventProcessorDelay(EventProcessor):
    def __init__(self, event, delay):
        EventProcessor.__init__(self, event)
        self.delay = delay
        self.returnEvents = []

    def run(self):
        sleep(self.delay)
        self.returnEvents=[Event(time(), self.event.getLabel())]
