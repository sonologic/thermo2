import unittest
from event import Event
from event_listener import EventListener

class EventListenerTest(unittest.TestCase):

    def test_event_listener_add_event(self):
        listener = EventListener()
        listener.addEvent('foo')
        listener.addEvent('bar')
        self.assertEqual(listener.eventList(),['foo','bar'])
    
    def test_event_listener(self):
        listener = EventListener()
        listener.addEvent('foo')
        listener.addEvent('bar')

        event = Event(42, 'foo')
        self.assertEqual(listener.event(event), [event])

        event = Event(1337, 'bar')
        self.assertEqual(listener.event(event), [event])

if __name__ == "__main__":
    unittest.main()
