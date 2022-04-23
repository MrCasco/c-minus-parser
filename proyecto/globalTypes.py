from enum import Enum

class TokenType(Enum):
    ENDFILE = 300
    ERROR = 301
    # reserved words
    ELSE = 'else'
    IF = 'if'
    INT = 'int'
    RETURN = 'return'
    VOID = 'void'
    WHILE = 'while'

    # multicharacter tokens
    ID = 310
    NUM = 311
    BODYCMNT = 200

    # special symbols
    PLUS = '+'
    MINUS = '-'
    TIMES = '*'
    DIV = '/'
    LESSTHAN = '<'
    LEQ = '<='
    GREATERTHAN = '>'
    GEQ = '>='
    EQEQ = '=='
    DIFF = '!='
    EQUALS = '='
    SEMICOLON = ';'
    COMMA =','
    OPENPAR = '('
    CLOSEPAR = ')'
    OPENBRACKET = '['
    CLOSEBRACKET = ']'
    OPENCURLY = '{'
    CLOSECURLY = '}'
    OPENCMNT = '/*'
    CLOSECMNT = '*/'
