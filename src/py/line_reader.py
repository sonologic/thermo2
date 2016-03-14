class LineReader:
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

