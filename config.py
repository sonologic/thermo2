import re
from line_reader import LineReader
from parser_constants import *
from script import *
from process import *

class ConfigError(Exception):
    """ TODO: abstract this, duplicates ScriptError """
    def __init__(self,lineno,message):
        Exception.__init__(self)
        self.lineno=lineno
        self.message=message

    def __str__(self):
        return "line %d: %s" % (self.lineno, self.message)

class ConfigParseError(ConfigError):
    pass

class Config:
    def __init__(self,str):
        self.processes = {}
        self.parse(str)

    def _parseScript(self,linereader):
        scriptString = ""
        while not linereader.eof():
            (lineno, line) = linereader.consume()

            if re.match('^\s*}\s*$', line):
                return Script(scriptString)

            scriptString += line + "\n"

        raise ConfigParseError(lineno,"premature end of file while parsing script")
        
    def _parseProcess(self,linereader,label):

        process = Process()

        process.label = label

        while not linereader.eof():
            (lineno, line) = linereader.consume()

            # closing braces
            if re.match('^\s*}\s*$', line):
                return process

            # trigger
            match = re.match('^\s*trigger:\s*('+ParserConstants.RE_IDENTIFIER+')(\s*,\s*('+ParserConstants.RE_IDENTIFIER+'))*\s*$', line)
            if match:
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

            # process
            match = re.match('^\s*process\s*('+ParserConstants.RE_IDENTIFIER+')\s*{\s*',line)
            if match:
                label=match.group(1)
                if label in self.processes.keys():
                    raise ConfigParseError(lineno, "duplicate process label %s" % label)
                process = self._parseProcess(linereader, label)
                self.processes[label]=process
                continue

            raise ConfigParseError(lineno,"unable to parse line: %s" % line)

    def __str__(self):
        rv  = "config {\n"
        for label in self.processes:
            process = self.processes[label]
            rv += "  process "+(process.label)+" {\n"
            p = str(process)
            ip = "\n".join((4 * " ") + i for i in p.splitlines())
            rv += ip+"\n"
            rv += "  }\n"
        rv += "}"

        return rv
