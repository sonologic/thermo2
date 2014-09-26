class ParserError(Exception):
    def __init__(self,lineno,message):
        Exception.__init__(self)
        self.lineno=lineno
        self.message=message

    def __str__(self):
        return "line %d: %s" % (self.lineno, self.message)

