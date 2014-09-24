import re
from parser_constants import ParserConstants

class ScriptParseError(Exception):
    def __init__(self,str):
        Exception.__init__(self,str)

class Script:
    def __init__(self,str):
        self.script=[]
        self.parse(str)

    def parse(self,str):
        lineno = 1
        for line in str.split("\n"):
            # assignment
            if re.match('\s*('+ParserConstants.RE_IDENTIFIER+')\s*:=\s*(.*)\s*$', line):
                return
            
            # emit 
            if re.match('^\s*emit\s*('+ParserConstants.RE_IDENTIFIER+')\s*\(\s*('+ParserConstants.RE_IDENTIFIER+')\s*\)\s*$', line):
                return

            # parse error
            raise ScriptParseError("Unable to parse line %d: %s" % (lineno,line) )

            lineno += 1

