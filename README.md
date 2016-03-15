Design
======

An event is a tuple (time,label).

Events trigger event listeners. An event listener fires of an asynchronous
process, and returns to the scheduler. This may result in any number of
asynchronous processes, in case of many listeners.

Only when all of the asynchronous processes have completed will another
event with that label be able to fire. Any events with that label in the
time before completion of all asynchronous event handlers will be ignored.

Use cases
=========

1wire temp sensor
-----------------

1 start sensor read
2 read sensor
3 event (if changed)

arp sensor
----------

1 fetch munin value
2 event (if changed)

knob
----

1 fetch knob value
2 event (if changed)
