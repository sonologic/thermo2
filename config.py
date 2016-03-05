import re
from line_reader import LineReader
from parser_constants import *
from script import *
from process import *
from timer import *
from myexceptions import *
from sensor import Sensor
from sensor_json import JsonSensor
from sensor_DS18B20 import DS18B20Sensor

class ConfigParseError(ParserError):
    pass

class Config(object):
    def __init__(self,str):
        self.processes = {}
        self.timers = {}
        self.sensors = {}
        self.parse(str)

    def _parseScript(self,linereader):
        scriptString = ""
        while not linereader.eof():
            (lineno, line) = linereader.consume()

            if re.match('^\s*}\s*$', line):
                return Script(scriptString)

            scriptString += line + "\n"

        raise ConfigParseError(lineno,"premature end of file while parsing script")

    def _parseTimer(self,linereader,label):
        timerString = ""

        while not linereader.eof():
            (lineno, line) = linereader.consume()

            # closing braces
            if re.match('^\s*}\s*$', line):
                timer = Timer(timerString)
                timer.label = label
                return timer

            timerString += line + "\n"

        raise ConfigParseError(lineno,"premature end of file while parsing timer")

    def _parseSensor(self,linereader,sensortype):
        sensorString = ""
        args={}

        while not linereader.eof():
            (lineno, line) = linereader.consume()

            # closing braces
            if re.match('^\s*}\s*$', line):
                sensor=None

                if sensortype=='json':
                    sensor = JsonSensor()
                elif sensortype=='DS18B20':
                    sensor = DS18B20Sensor()

                if sensor==None:
                    raise ConfigParseError(lineno,"invalid sensor type")

                for arg in args:
                    sensor.__dict__[arg] = args[arg]
                    if arg=='trigger':
                        sensor.addEvent(args[arg])

                if not 'label' in sensor.__dict__:
                    raise ConfigParseError(lineno,"sensor has no label")

                return sensor
            else:
                m = re.match('^\s*('+ParserConstants.RE_IDENTIFIER+')\s*:\s*(.*)$', line)
                if m!=None:
                    args[m.group(1)]=m.group(2)

            sensorString += line + "\n"

        raise ConfigParseError(lineno,"premature end of file while parsing sensor")
            
        
    def _parseProcess(self,linereader,label):

        process = Process()

        process.label = label

        while not linereader.eof():
            (lineno, line) = linereader.consume()

            # closing braces
            if re.match('^\s*}\s*$', line):
                return process

            # trigger
            match = re.match('^\s*trigger:\s*(('+ParserConstants.RE_IDENTIFIER+')(\s*,\s*('+ParserConstants.RE_IDENTIFIER+'))*)\s*$', line)
            if match:
                for event in re.split('\s*,\s*',match.group(1)):
                    process.addEvent(event)
                continue

            # script
            if re.match('^\s*script:\s*{\s*$', line):
                process.script = self._parseScript(linereader)
                continue

        raise ConfigParseError(lineno,"premature end of file while parsing process")

    def parse(self,str):
        linereader = LineReader(str)

        while not linereader.eof():
            (lineno, line) = linereader.consume()

            # empty line
            if re.match('^\s*$', line):
                continue

            # comments
            if re.match('^\s*#', line):
                continue

            # process
            match = re.match('^\s*process\s*('+ParserConstants.RE_IDENTIFIER+')\s*{\s*',line)
            if match:
                label=match.group(1)
                if label in self.processes.keys():
                    raise ConfigParseError(lineno, "duplicate process label %s" % label)
                process = self._parseProcess(linereader, label)
                self.processes[label]=process
                continue

            # timer
            match = re.match('^\s*timer\s*('+ParserConstants.RE_IDENTIFIER+')\s*{\s*',line)
            if match:
                label=match.group(1)
                if label in self.timers.keys():
                    raise ConfigParseError(lineno, "duplicate timer label %s" % label)
                timer = self._parseTimer(linereader, label)
                self.timers[label]=timer
                continue

            # sensor
            match = re.match('^\s*sensor\s*('+ParserConstants.RE_IDENTIFIER+')\s*{\s*',line)
            if match:
                sensortype=match.group(1)
                #if label in self.sensors.keys():
                #    raise ConfigParseError(lineno, "duplicate sensor label %s" % label)
                sensor = self._parseSensor(linereader, sensortype) 
                # todo: verify that label is set
                self.sensors[sensor.label]=sensor
                continue

            raise ConfigParseError(lineno,"unable to parse line: %s" % line)

    def __str__(self):
        rv  = "config {\n"
        for label in self.timers:
            timer = self.timers[label]
            rv += " timer "+timer.label+" {\n"
            p = str(timer)
            ip = "\n".join((4 * " ") + i for i in p.splitlines())
            rv += ip+"\n"
            rv += "  }\n"

        for label in self.processes:
            process = self.processes[label]
            rv += "  process "+(process.label)+" {\n"
            p = str(process)
            ip = "\n".join((4 * " ") + i for i in p.splitlines())
            rv += ip+"\n"
            rv += "  }\n"

        for label in self.sensors:
            sensor = self.sensors[label]
            rv += "  sensor " + sensor.__class__.__name__ + " " + label + " " + sensor.trigger + " {\n"
            rv += "    url: " + str(sensor.url)+"\n";
            rv += "  }\n"

        rv += "}"

        return rv
