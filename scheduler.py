from timer import Timer
from event import Event
from time import time

class Scheduler:
    def __init__(self):
        self.timers={}
        self.listeners={}
        self.events=[]

    def schedule(self, events=None):
        if not events == None:
            #print "in "+str(events)
            for event in events:
                #print "  append "+event.getLabel()
                self.events.append(event)
            #print "events queued "+str(self.events)
        #print "listeners "+str(self.listeners)

        for label in self.timers.keys():
            trigger = self.timers[label].poll()
            if not trigger == None:
                self.events.append(Event(time(), label))

        for event in self.events:
            #print "--> "+str(event.getTime())+": "+event.getLabel()
            #print "--> l "+str(self.listeners)
            if event.getLabel() in self.listeners.keys():
                for listener in self.listeners[event.getLabel()]:
                    #print "listener "+str(listener)
                    newEvents = listener.event(event)

                    retry = False

                    for newEvent in newEvents:
                        if newEvent == event:
                            retry = True
                        else:
                            self.events.append(newEvent)

                    if not retry:
                        break
            self.events = self.events[1:]
            return event.getLabel()
                    
        return 'idle'

    def add_timer(self,period,label):
        timer = Timer(period)
        self.timers[label]=timer

    def add_listener(self,listener):
        for event in listener.eventList():
            #print "addloop "+event
            if not event in self.listeners.keys():
                self.listeners[event] = []
        self.listeners[event].append(listener)
        #print "add result "+str(self.listeners)
