import re
from parser_constants import ParserConstants
from script_expression import *
from sensor_event import *
from time import time

class ScriptParseError(Exception):
    def __init__(self,str):
        Exception.__init__(self,str)

class Script:
    def __init__(self,str):
        self.script=[]
        self.var={}
        self.parse(str)

    def parse(self,str):
        lineno = 0
        for line in str.split("\n"):
            lineno += 1

            # assignment
            match=re.match('\s*('+ParserConstants.RE_IDENTIFIER+')\s*:=\s*(.*)\s*$', line)
            if match:
                exp = ScriptExpression(match.group(2))
                self.script.append( { 'line':lineno, 'action':'assign', 'dst':match.group(1), 'exp':exp } )
                continue
            
            # emit 
            match=re.match('^\s*emit\s*('+ParserConstants.RE_IDENTIFIER+')\s*\(\s*('+ParserConstants.RE_IDENTIFIER+')\s*\)\s*$', line)
            if match:
                self.script.append( { 'line':lineno, 'action':'emit', 'event':match.group(1), 'arg':match.group(2) } )
                continue

            if re.match('^\s*$',line):
                continue

            # parse error
            raise ScriptParseError("Unable to parse line %d: %s" % (lineno,line) )

    def _setVar(self,var,val):
        self.var[var]=val

    def _getVar(self,var):
        if var in self.var.keys():
            return self.var[var]

        raise Exception("Variable "+var+" used before assignment")        

    def eval(self,event=None):
        returnEvents = []

        if event!=None:
            self._setVar(event.getLabel(),event.getValue())

        for line in self.script:
            if line['action']=='assign':
                self._setVar(line['dst'], line['exp'].eval(self.var))
                continue
            if line['action']=='emit':
                if self._getVar(line['arg'])!=None:
                    e = SensorEvent(time(), line['event'], self._getVar(line['arg']))
                    returnEvents.append(e)
                continue

        return returnEvents

