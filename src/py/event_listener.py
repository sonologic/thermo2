import logging

class EventListener(object):
    """An EventListener can be registered with the scheduler, keyed on
    event label.

    When the scheduler processes an event for which this listener is registered
    (one listener may be registered on various events), the event method is
    invoked.
    """

    def __init__(self):
        self.events = []
        self.logger = logging.getLogger('thermo2.'+__name__)

    def addEvent(self,event):
        """Add an event label to the sensitivity list.

        Changes to the sensitivity list after the listener has been registered
        with the scheduler will be ignored.
        """
        self.events.append(event)

    def eventList(self):
        return self.events

    def event(self,event):
        """Callback for events.

        Called by the scheduler. This listener may be registered to multiple
        events, in that case the overriding method must distinguish based on 
        the event object's label.

        Returns a list of events (possibly empty). If the event that was passed
        to this method is in the return list, the scheduler will continue to try
        other listeners.
        """ 
        return [event]
