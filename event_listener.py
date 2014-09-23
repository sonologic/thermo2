class EventListener:

    def __init__(self):
        self.events = []

    def addEvent(self,event):
        self.events.append(event)

    def eventList(self):
        return self.events

    def event(self,event):
        return [event]
