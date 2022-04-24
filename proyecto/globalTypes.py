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

class NodeKind(Enum):
    StmtK = 0
    ExpK = 1

class StmtKind(Enum):
    IfK = 0
    RepeatK = 1
    AssignK = 2
    Inputk = 3
    OutputK = 4
    DeclareK = 5

class ExpKind(Enum):
    OpK = 0
    ConstK = 1
    IdK = 2
    IntegerK = 3
    VoidK = 4

# ExpType is used for type checking
class ExpType(Enum):
    Void = 0
    Integer = 1
    Boolean = 2
