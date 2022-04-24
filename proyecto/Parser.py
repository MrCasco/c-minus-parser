from lexer import *
from TypeExpression import *
from Node import *

token = None # holds current token
tokenString = None # holds the token string value
Error = False
lineno = 1
SintaxTree = None
imprimeScanner = False
root = None

def match(expected):
    global token, tokenString, lineno
    if token == expected:
        token, tokenString = getToken(imprimeScanner)
    else:
        syntaxError("unexpected token -> ")
        printToken(token, tokenString)
        print("      ")

def declaration_list():
    global token, root
    t = declaration()
    p = t
    root.children.append(t)
    while token in (TokenType.INT, TokenType.VOID) :
        q = declaration()
        if q != None:
            if t == None:
                t = p = q
            else: # now p cannot be NULL either
                root.children.append(q)
                p = q

def type_specifier():
    # import ipdb; ipdb.set_trace()
    global token
    if token == TokenType.INT:
        match(token)
        return ExpType.Integer
    else:
        match(TokenType.VOID)
        return ExpType.Void

def declaration(param=False):
    global token, tokenString, lineno
    var_type = type_specifier()
    var_name = tokenString
    match(TokenType.ID)
    t = newExpNode(ExpKind.IdK)
    t.val = var_name
    t.type = var_type
    if not param:
        if token == TokenType.OPENBRACKET:
            match(TokenType.OPENBRACKET)
            match(TokenType.NUM)
            match(TokenType.CLOSEBRACKET)
            match(TokenType.SEMICOLON)
        elif token == TokenType.SEMICOLON:
            match(TokenType.SEMICOLON)
        elif token == TokenType.OPENPAR:
            match(TokenType.OPENPAR)
            t.children += [params()]
            match(TokenType.CLOSEPAR)
            t.children += [compound_stmt()]
        else:
            syntaxError("unexpected token -> ")
            printToken(token,tokenString)
            token, tokenString = getToken()
    return t

def params():
    global token, tokenString
    t = newExpNode(ExpKind.ParamsK)
    if token == TokenType.INT:
        t.children += [declaration(True)]
        while token == TokenType.COMMA:
            match(TokenType.COMMA)
            t.children += [declaration(True)]
        return t
    t.children += [newExpNode(ExpKind.ConstK)]
    match(TokenType.VOID)
    return t

def compound_stmt():
    t = newStmtNode(StmtKind.FunBodyK)
    match(TokenType.OPENCURLY)
    t.children += [local_declaration()]
    # statement_list()
    match(TokenType.CLOSECURLY)
    return t

def local_declaration():
    t = newExpNode(ExpKind.LocalsK)
    while token == TokenType.INT:
        # print('Before: ', token)
        t.children += [declaration()]
        # print('After: ', token)
    return t

def printToken(token, tokenString):
    if token in {TokenType.IF, TokenType.ELSE}:
        print(" reserved word: " + tokenString)
    elif token == TokenType.OPENPAR:
        print("(")
    elif token == TokenType.CLOSEPAR:
        print(")")
    elif token == TokenType.ENDFILE:
        print("EOF")
    # elif token == TokenType.ASSIGN:
    #     print("=")
    # elif token == TokenType.LT:
    #     print("<")
    # elif token == TokenType.EQ:
    #     print("=")
    # elif token == TokenType.SEMI:
    #     print(";")
    # elif token == TokenType.PLUS:
    #     print("+")
    # elif token == TokenType.MINUS:
    #     print("-")
    # elif token == TokenType.TIMES:
    #     print("*")
    # elif token == TokenType.OVER:
    #     print("/")
    # elif token == TokenType.NUM:
    #   print("NUM, val= " + tokenString)
    # elif token == ID:
    #     print("ID, name= " + tokenString);
    # elif token == TokenType.ERROR:
    #     print("ERROR: " + tokenString)
    # else: # should never happen
    #     print("Unknown token: " + token)

def globales(prog, pos, long):
    globalesLexer(prog, pos, long)

def newStmtNode(kind):
    t = Node()
    global tokenString
    if t == None:
        print("Out of memory error at line " + lineno)
    else:
        t.nodekind = NodeKind.StmtK
        t.stmt = kind
        t.lineno = lineno
    return t

# Function newExpNode creates a new expression
# node for syntax tree construction
def newExpNode(kind):
    t = Node()
    if t == None:
        print("Out of memory error at line " + lineno)
    else:
        t.nodekind = NodeKind.ExpK
        t.exp = kind
        t.lineno = lineno
        t.type = ExpType.Void
    return t

def syntaxError(mensaje):
    global Error, lineno
    print(">>> Syntax error at line " + str(lineno) + ": " + mensaje, end='')
    Error = True

indentno = 0

def printBlanks():
    global indentno
    print(' '*indentno, end='')

def printTree(tree):
    global indentno
    indentno += 2 # INDENT
    while tree != None:
        printBlanks();
        if (tree.nodekind == NodeKind.StmtK):
            if tree.stmt == StmtKind.IfK:
                print(tree.lineno, "If")
            elif tree.stmt == StmtKind.RepeatK:
                print(tree.lineno, "Repeat")
            elif tree.stmt == StmtKind.AssignK:
                print(tree.lineno, "Assign to: ", tree.name)
            elif tree.stmt == StmtKind.Inputk:
                print(tree.lineno, "Input: ", tree.name)
            elif tree.stmt == StmtKind.OutputK:
                print(tree.lineno, "Output")
            elif tree.stmt == StmtKind.FunBodyK:
                print(tree.lineno, "Body: ")
            else:
                print(tree.lineno, "Unknown ExpNode kind")
        elif tree.nodekind == NodeKind.ExpK:
            if tree.exp == ExpKind.RootK:
                print(tree.lineno, tree.val)
            elif tree.exp == ExpKind.OpK:
                print(tree.lineno, "Op: ", end ="")
                printToken(tree.op," ")
            elif tree.exp == ExpKind.ConstK:
                print(tree.lineno, "Const: ", tree.val)
            elif tree.exp == ExpKind.IdK:
                print(tree.lineno, "Id:", tree.val + ' Type: ' + tree.type.value)
            elif tree.exp == ExpKind.ParamsK:
                print(tree.lineno, "Params: ")
            elif tree.exp == ExpKind.LocalsK:
                print(tree.lineno, "Locals: ")
            else:
                print(tree.lineno, "Unknown ExpNode kind")
        else:
            print(tree.lineno, "Unknown node kind")
        for i in range(len(tree.children)):
            printTree(tree.children[i])
        tree = tree.sibling
    indentno -= 2 #UNINDENT

def parser(imprime = True):
    global token, tokenString, lineno, root
    token, tokenString = getToken(imprimeScanner)
    root = newExpNode(ExpKind.RootK)
    root.val = 'Root'
    declaration_list()
    if (token != TokenType.ENDFILE):
        syntaxError("Code ends before file. Missing ENDFILE character ($)\n")
    if imprime:
        printTree(root)
    return Error
