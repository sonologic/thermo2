import re
from parser_constants import ParserConstants
from script_expression import *
from sensor_event import *
from line_reader import *
from time import time
from myexceptions import *

class ScriptParseError(ParserError):
    pass

class ScriptRuntimeError(ParserError):
    pass

class Script:
    def __init__(self,str):
        self.script=[]
        self.var={}
        self.parse(str)

    def parse(self,str):
        lines = LineReader(str)
        self.script = self._parse(0,lines)
        #print "parsed script:"
        #print self.script

    def _parseTerm(self,str):
        if re.match('^'+ParserConstants.RE_INTEGER+'$',str):
            return ('int',int(str))
        if re.match('^'+ParserConstants.RE_IDENTIFIER+'$',str):
            return ('identifier',str)

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
            
            # emit SensorEvent (with value)
            match=re.match('^\s*emit\s*('+ParserConstants.RE_IDENTIFIER+')\s*\(\s*('+ParserConstants.RE_TERM+')\s*\)\s*$', line)
            if match:
                script.append( { 'line':lineno, 'action':'emit', 'event':match.group(1), 'arg':self._parseTerm(match.group(2)) } )
                continue

            if re.match('^\s*$',line):
                continue

            # emit Event (without value)
            match=re.match('^\s*emit\s*('+ParserConstants.RE_IDENTIFIER+')\s*$', line)
            if match:
                script.append( { 'line':lineno, 'action':'emit', 'event':match.group(1) } )
                continue

            # if
            match=re.match('^\s*if\s*('+ParserConstants.RE_CONDITION+')\s*then\s*$', line)
            if match:
                subscript = self._parse(level+1,lines)
                t1 = self._parseTerm(match.group(2))
                t2 = self._parseTerm(match.group(6))
                script.append( { 'line':lineno, 'action':'if', 'sub':subscript, 'cmp':match.group(5), \
                                 't1':t1, 't2':t2 } )
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

    def _hasVar(self,var):
        if var in self.var.keys():
            return True
        return False

    def _evalTerm(self,term):
        (termtype, val) = term
        if termtype == 'int':
            return val
        if termtype == 'identifier':
            if self._hasVar(val):
                return self._getVar(val)
            else:
                return None
        
    def eval(self,event=None):
        if event!=None:
            if isinstance(event, SensorEvent):
                self._setVar(event.getLabel(),event.getValue())
        return self._eval(self.script)

    def _eval(self,script):
        returnEvents = []

        for line in script:
            if line['action']=='assign':
                self._setVar(line['dst'], line['exp'].eval(self.var))
                continue
            if line['action']=='emit':
                if 'arg' in line.keys():
                    # SensorEvent
                    value = self._evalTerm(line['arg'])
                    if value != None:
                        e = SensorEvent(time(), line['event'], value)
                        returnEvents.append(e)
                else:
                    # Event
                    e = Event(time(), line['event'])
                    returnEvents.append(e)
                continue
                #script.append( { 'line':lineno, 'action':'if', 'sub':subscript, 'cmp':match.group(5), \
                #                 't1':match.group(2), 't2':match.group(6) } )
            if line['action']=='if':
                # evaluate terms (t1 cmp t2)
                t1_val = self._evalTerm(line['t1'])
                t2_val = self._evalTerm(line['t2'])
                
                # condition with any one term None is always false
                if t1_val==None or t2_val==None:
                    continue

                # evaluate comparison on evaluated terms
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

    def __str__(self):
        rv = ""
        rv += "vars: "+str(self.var)+"\n"
        rv += "script: "+str(self.script)+"\n"
        return rv
