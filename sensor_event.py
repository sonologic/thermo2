from event import Event

class SensorEvent(Event):

    def __init__(self, t, label, value):
        Event.__init__(self, t, label)
        self.value = value

    def getValue(self):
        return self.value
 
