class Event:
    def __init__(self, t, label):
        self.t = t
        self.label = label

    def getTime(self):
        return self.t

    def getLabel(self):
        return self.label

