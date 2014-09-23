from threading import Thread

class EventProcessor(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.event = event
        self.returnEvents = []

    def run(self):
        pass
