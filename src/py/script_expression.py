import re

from parser_constants import ParserConstants

class ScriptExpressionParseError(Exception):
    def __init__(self,str):
        Exception.__init__(self,str)

class ScriptExpressionEvalError(Exception):
    def __init__(self,str):
        Exception.__init__(self,str)

class ScriptExpression:
    def __init__(self,str):
        self.input={}
        self.oper=None
        self.term1=None
        self.term2=None
        self.term1_type=None
        self.term2_type=None
        self.parse(str)

    def parse(self,str):

        # simple math op ( val1 op val2 )
        match=re.match('^\s*('+ParserConstants.RE_TERM+')\s*('+ParserConstants.RE_MATH_OP+')\s*('+ParserConstants.RE_TERM+')\s*$',str)
        if match:
            self.term1 = match.group(1)
            self.term2 = match.group(6)
            self.oper = match.group(5)
    
            if re.match('^'+ParserConstants.RE_IDENTIFIER+'$',self.term1):
                self.term1_type = 'identifier'
            if re.match('^'+ParserConstants.RE_IDENTIFIER+'$',self.term2):
                self.term2_type = 'identifier'
            if re.match('^'+ParserConstants.RE_FLOAT+'$',self.term1):
                self.term1_type = 'float'
            if re.match('^'+ParserConstants.RE_INTEGER+'$',self.term1):
                self.term1_type = 'int'
            if re.match('^'+ParserConstants.RE_FLOAT+'$',self.term2):
                self.term2_type = 'float'
            if re.match('^'+ParserConstants.RE_INTEGER+'$',self.term2):
                self.term2_type = 'int'

            if self.term1==None or self.term1_type==None:
                raise ScriptExpressionParseError("term1 invalid")
            if self.term2==None or self.term2_type==None:
                raise ScriptExpressionParseError("term2 invalid")

            return

        raise ScriptExpressionParseError("Unable to parse ScriptExpression: %s" % str)

    def eval(self,args=None):
        term1_val=None
        if self.term1_type=='int':
            term1_val = int(self.term1)
        if self.term1_type=='float':
            term1_val = float(self.term1)
        if self.term1_type=='identifier':
            if self.term1 in args.keys():
                term1_val = args[self.term1]

        term2_val=None
        if self.term2_type=='int':
            term2_val = int(self.term2)
        if self.term2_type=='float':
            term2_val = float(self.term2)
        if self.term2_type=='identifier':
            if self.term2 in args.keys():
                term2_val = args[self.term2]

        if term1_val==None or term2_val==None:
            return None

        if self.oper=='+':
            return term1_val + term2_val
        if self.oper=='-':
            return term1_val - term2_val
        if self.oper=='/':
            return term1_val / term2_val
        if self.oper=='*':
            return term1_val * term2_val

        raise ScriptExpressionEvalError('invalid operator: '+self.oper)

