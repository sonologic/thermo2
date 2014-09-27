from time import time
import re

from line_reader import LineReader
from parser_constants import *
from myexceptions import *

class TimerParserError(ParserError):
    pass

class Timer:
    def __init__(self,initval,event=None):
        self.event=event
        self.period=None
        if isinstance(initval, str):
            self._parse(initval)
        else:
            self.period = initval
        self.last_trigger = time()
        self.next_trigger = self.last_trigger + self.period

    def _parse(self,str):
        linereader = LineReader(str)
        while not linereader.eof():
            (lineno, line) = linereader.consume()

            # period
            match = re.match('^\s*interval:\s*('+ParserConstants.RE_FLOAT+')\s*$', line)
            if match:
                self.period=float(match.group(1))
                continue

            # event
            match = re.match('^\s*event:\s*('+ParserConstants.RE_IDENTIFIER+')\s*$', line)
            if match:
                self.event=match.group(1)
                continue

            # empty line
            if re.match('^\s*$', line):
                continue

            raise TimerParserError(lineno, "unable to parse line: %s" % line)
        if self.event == None or self.period == None:
            raise TimerParserError(-1, "event or period not set")

    def getPeriod(self):
        return self.period

    def reset(self):
        self.last_trigger = time()
        self.next_trigger = self.last_trigger + self.period
        return self.last_trigger       

    def poll(self):
        t = time()

        if t < self.next_trigger:
            return None

        self.last_trigger = t
        lateness = t - self.next_trigger

        self.next_trigger = self.next_trigger + self.period

        return lateness        

    def __str__(self):
        rv  = "event: %s\n" % self.event
        rv  = "interval: %d\n" % self.period
        rv += "next_trigger: %d\n" % self.next_trigger
        rv += "last_trigger: %d\n" % self.last_trigger

        return rv
