class ParserConstants:
    RE_IDENTIFIER = '[A-Za-z_][A-Za-z0-9_]*'
    RE_INTEGER = '[0-9]+'
    RE_MATH_OP = '[+-/*]'
    RE_TERM = '('+RE_IDENTIFIER+')|('+RE_INTEGER+')'
