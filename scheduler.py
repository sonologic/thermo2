from timer import Timer
from event import Event
from time import time
from config import Config

class Scheduler(object):
    def __init__(self):
        self.timers={}
        self.listeners={}
        self.events=[]
        self.lastEvent=None

    def schedule(self, events=None):
        """Invoke scheduler.

        Optionally accepts a list of events to inject into the event queue.

        Returns the label of the processed event, or 'idle'. A maximum of one
        event is processed per invocation of schedule().

        The scheduler:
        1. injects the optional list of events
        2. injects event on timer expiries
        3. processes the event queue
            - consume oldest element on queue, call listeners
            - returns the label of the event
        4. return 'idle'
        
        """
   
        # process optional events by adding to event queue 
        if not events == None:
            for event in events:
                self.events.append(event)

        # check all timers, inject events on expiry
        for label in self.timers.keys():
            trigger = self.timers[label].poll()
            if not trigger == None:
                self.events.append(Event(time(), label))

        # process event queue:
        for event in self.events:
            # check if anyone cares about this event:
            if event.getLabel() in self.listeners.keys():
                # if so, loop over list of interested listeners
                for listener in self.listeners[event.getLabel()]:

                    # invoke listener:
                    newEvents = listener.event(event)

                    # process events returned by listener
                    retry = False
                    for newEvent in newEvents:
                        if newEvent == event:
                            retry = True
                        else:
                            self.events.append(newEvent)

                    # if listener did not return the original event, listener has consumed it
                    # do not attempt further event listeners
                    if not retry:
                        break
        
            # consume event
            self.events = self.events[1:]
            
            # and return the label of the processed event
            self.lastEvent = event.getLabel()
            return event
                   
        # if no events were to be processed, return idle state 
        self.lastEvent = 'idle'
        return 'idle'

    def add_timer(self,period,label):
        timer = Timer(period)
        self.timers[label]=timer

    def add_listener(self,listener):
        for event in listener.eventList():
            if not isinstance(event, str):
                raise TypeError('element of listener event array is not string')
            if not event in self.listeners.keys():
                self.listeners[event] = []
            self.listeners[event].append(listener)

    def bind(self, config):
        if type(config)!=type(Config('')):
            raise TypeError('binding with something not a config')

        for timer in config.timers:
            self.add_timer(config.timers[timer].period, config.timers[timer].event)

        for process in config.processes:
            self.add_listener(config.processes[process])
     
        for sensor in config.sensors:
            self.add_listener(config.sensors[sensor]) 
