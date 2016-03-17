Introduction
============

Thermo2 is a generic event-driven control framework, intended
to run a house thermostat. 

It is written in python, with command-line clients for python
and .net (mono).

Multiple thermo2 daemons can be running, communicating each 
other and users over http(s).


Running
=======

To run a single daemon with an example config, try:

$ cd src/py
$ ./main.py --config examples/test.cfg --verbose

In another console, now try:

$ cd src/py
$ ./thermo2cli.py -g sum_value


Testing
=======

To run python unit tests:

$ cd src/py/test
$ ./test.py


.NET
====

The C# code lives under src/cs/Thermo2Cli, where you will find a
MS Visual Studio solution file.

Windows
-------

Install Visual Studio, double-click the solution file, magic happens.

Linux
-----

Get nuget.exe:

https://dist.nuget.org/index.html

Then restore packages (use latest mono):

$ cd src/cs/Thermo2Cli
$ mono ~/path/to/nuget.exe restore -o packages

This will install CommandLineParser and Newtonsoft.Json.

then:

$ xbuild

This will build eveything. 

To run unit tests:

$ mono packages/xunit.runner.console.2.1.0/tools/xunit.console.exe Thermo2Cli.Tests/bin/Debug/Thermo2Cli.Tests.dll

or:

$ mono packages/xunit.runner.console.2.1.0/tools/xunit.console.exe Thermo2Cli.Tests/bin/Debug/Thermo2Cli.Tests.dll -verbose


Security
========

It is wise to have a thermo2 instance that has access to valves
and other moving parts isolated from the internet.

On the other hand, one wants interaction from a web interface
or mobile app.

By setting up two instances, both goals can be satisfied.

The instance controlling physical actors can be placed behind a
firewall.

A second instance can be placed on a web server (preferably with
a reverse proxy in front) to interact with the user.

The first instance can be set up to poll the second instance for
user input, avoiding the need for direct interaction between 
user and first instance.


Design
======

An event is a tuple (time,label,value).

The value member of the tuple is optional.

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
