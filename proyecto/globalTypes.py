from enum import Enum

class TokenType(Enum):
    ENDFILE = 300
    ERROR = 301
    # reserved words
    IF = 'if'
    ELSE = 'else'
    INT = 'int'
    RETURN = 'return'
    VOID = 'void'
    WHILE = 'while'
    INPUT = 'input'
    OUTPUT = 'output'
    MAIN = 'main'

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
    WhileK = 1
    AssignK = 2
    Inputk = 3
    OutputK = 4
    BodyK = 5
    ReturnK = 6
    MainK = 7
    FunCallK = 8
    ArrayAtK = 9

class ExpKind(Enum):
    RootK = 0
    OpK = 1
    ConstK = 2
    IdK = 3
    ParamsK = 4
    LocalsK = 5

# ExpType is used for type checking
class ExpType(Enum):
    Void = 'void'
    Integer = 'int'
    Boolean = 'bool'
    Array = 'array'
