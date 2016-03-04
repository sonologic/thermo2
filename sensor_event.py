from event import Event

class SensorEvent(Event):

    def __init__(self, t, label, value):
        Event.__init__(self, t, label)
        self.value = value

    def getValue(self):
        return self.value

    def __repr__(self):
        return "SensorEvent["+str(self.label)+",t="+str(self.t)+",value="+str(self.value)+"]" 
