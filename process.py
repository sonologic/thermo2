from event_listener import *

class Process(EventListener):
    def __init__(self):
        EventListener.__init__(self)
        self.label=None
        self.script=None

    def __str__(self):
        rv  = "label: "+str(self.label)+"\n"
        rv += "trigger: "+", ".join(self.events)+"\n"
        rv += "script: {\n"
        rv += "\n".join((2 * " ") + i for i in str(self.script).splitlines())
        rv += "\n}\n"

        return rv

    def event(self,event):
        return self.script.eval(event)
