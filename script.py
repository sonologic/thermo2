import re
from parser_constants import ParserConstants
from script_expression import *
from sensor_event import *
from time import time

class ScriptError(Exception):
    def __init__(self,lineno,message):
        Exception.__init__(self)
        self.lineno=lineno
        self.message=message

    def __str__(self):
        return "line %d: %s" % (self.lineno, self.message)

class ScriptParseError(ScriptError):
    pass

class ScriptRuntimeError(ScriptError):
    pass

class ScriptLines:
    def __init__(self,str):
        self.lines=str.split("\n")
        self.lineno=0

    def consume(self):
        if self.lineno > len(self.lines)-1:
            return (None,None)

        self.lineno += 1

        return (self.lineno,self.lines[self.lineno-1])

    def eof(self):
        return self.lineno > len(self.lines)-1

class Script:
    def __init__(self,str):
        self.script=[]
        self.var={}
        self.parse(str)

    def parse(self,str):
        lines = ScriptLines(str)
        self.script = self._parse(0,lines)
        #print "parsed script:"
        #print self.script

    def _parse(self,level,lines):
        script = []
        while not lines.eof():
            (lineno, line) = lines.consume()

            # assignment
            match=re.match('\s*('+ParserConstants.RE_IDENTIFIER+')\s*:=\s*(.*)\s*$', line)
            if match:
                exp = ScriptExpression(match.group(2))
                script.append( { 'line':lineno, 'action':'assign', 'dst':match.group(1), 'exp':exp } )
                continue
            
            # emit 
            match=re.match('^\s*emit\s*('+ParserConstants.RE_IDENTIFIER+')\s*\(\s*('+ParserConstants.RE_IDENTIFIER+')\s*\)\s*$', line)
            if match:
                script.append( { 'line':lineno, 'action':'emit', 'event':match.group(1), 'arg':match.group(2) } )
                continue

            if re.match('^\s*$',line):
                continue

            # if
            match=re.match('^\s*if\s*('+ParserConstants.RE_CONDITION+')\s*then\s*$', line)
            if match:
                subscript = self._parse(level+1,lines)
                script.append( { 'line':lineno, 'action':'if', 'sub':subscript, 'cmp':match.group(5), \
                                 't1':match.group(2), 't2':match.group(6) } )
                continue;

            # endif
            if re.match('^\s*endif\s*$', line):
                if level>0:
                    return script
                raise ScripteParseError("parse error on line %d, unbalanced endif" % lineno)

            # parse error
            raise ScriptParseError(lineno, "Unable to parse '%s'" % line)
        
        # end of file
        if level!=0:
            raise ScriptParseError(lineno, "premature eof (level %d)" % level)

        return script

    def _setVar(self,var,val):
        self.var[var]=val

    def _getVar(self,var):
        if var in self.var.keys():
            return self.var[var]

        raise Exception("Variable "+var+" used before assignment")        

        
    def eval(self,event=None):
        if event!=None:
            self._setVar(event.getLabel(),event.getValue())
        return self._eval(self.script)

    def _eval(self,script):
        returnEvents = []

        for line in script:
            if line['action']=='assign':
                self._setVar(line['dst'], line['exp'].eval(self.var))
                continue
            if line['action']=='emit':
                if self._getVar(line['arg'])!=None:
                    e = SensorEvent(time(), line['event'], self._getVar(line['arg']))
                    returnEvents.append(e)
                continue
                #script.append( { 'line':lineno, 'action':'if', 'sub':subscript, 'cmp':match.group(5), \
                #                 't1':match.group(2), 't2':match.group(6) } )
            if line['action']=='if':
                t1_val=None
                t2_val=None
                # todo, this should have been parsed earlier
                if re.match('^'+ParserConstants.RE_INTEGER+'$',line['t1']):
                    t1_val=int(line['t1'])
                if re.match('^'+ParserConstants.RE_INTEGER+'$',line['t2']):
                    t2_val=int(line['t2'])
                if re.match('^'+ParserConstants.RE_IDENTIFIER+'$',line['t1']):
                    t1_val=self._getVar(line['t1'])
                if re.match('^'+ParserConstants.RE_IDENTIFIER+'$',line['t2']):
                    t2_val=self._getVar(line['t2'])
                
                # condition with any one term None is always false
                if t1_val==None or t2_val==None:
                    continue

                runScript = False
                if line['cmp'] == '<':
                    runScript = t1_val < t2_val
                if line['cmp'] == '>':
                    runScript = t1_val > t2_val
                if line['cmp'] == '==':
                    runScript = t1_val == t2_val
                if line['cmp'] == '!=':
                    runScript = t1_val != t2_val
                if line['cmp'] == '>=':
                    runScript = t1_val >= t2_val
                if line['cmp'] == '<=':
                    runScript = t1_val <= t2_val
   
                if runScript:
                    subEvents = self._eval(line['sub'])
                    returnEvents = returnEvents + subEvents

                continue

            raise ScriptRuntimeError(line['line'], "invalid action %s" % line['action'])

        return returnEvents

