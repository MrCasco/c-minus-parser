from lexer import *
from TypeExpression import *
from Node import *
# from globalTypesTYNY import *

token = None # holds current token
tokenString = None # holds the token string value
Error = False
lineno = 1
SintaxTree = None
imprimeScanner = False

def syntaxError(mensaje):
    print('>>> Error de sintaxis: ' + mensaje)

def printBlanks():
    print(' '*endentacion, end='')

def declaration_list():
    import ipdb; ipdb.set_trace()
    t = declaration()
    global token
    while token != TokenType.SEMICOLON:
        import ipdb; ipdb.set_trace()
        q = declaration()
        if q != None:
            if t == None:
                t = p = q
            else: # now p cannot be NULL either
                p.sibling = q
                p = q
    return t

def type_specifier():
    global token, tokenString, lineno
    if tokenString == 'int':
        return newNode(TipoExpresion.Int)
    return newNode(TipoExpresion.Void)

def declaration():
    import ipdb; ipdb.set_trace()
    global token, tokenString, lineno
    t = type_specifier()
    match(TokenType.INT)
    match(TokenType.ID)
    if token == TokenType.SEMICOLON:
        match(TokenType.SEMICOLON)
    elif token == TokenType.OPENBRACKET:
        match(TokenType.OPENBRACKET)
        match(TokenType.NUM)
        match(TokenType.CLOSEBRACKET)
    elif token == TokenType.OPENPAR:
        match(TokenType.OPENPAR)
        match(TokenType.NUM)
        match(TokenType.CLOSEPAR)
        t = compound_stmt()
    else:
        syntaxError("unexpected token -> ")
        printToken(token,tokenString)
        token, tokenString = getToken()
    return t

def fun_declaration():
    pass

def match(expected):
    import ipdb; ipdb.set_trace()
    global token, tokenString, lineno
    if token == expected:
        token, tokenString = getToken(imprimeScanner)
        print("TOKEN:", token, lineno)
    else:
        syntaxError("unexpected token -> ")
        # printToken(token, tokenString)
        print("      ")

def printToken(token, tokenString):
    if token in {TokenType.IF, TokenType.ELSE}:
        print(" reserved word: " + tokenString)
    elif token == TokenType.OPENPAR:
        print("(")
    elif token == TokenType.CLOSEPAR:
        print(")")
    # elif token == TokenType.ASSIGN:
    #     print(":=")
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
    # elif token == TokenType.ENDFILE:
    #     print("EOF")
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

def newNode(kind):
    global lineno, token, tokenString
    t = Node()
    if t == None:
        print('Error: Out of memory at line' + lineno)
    else:
        t.val = tokenString
        t.exp = kind
        t.lineno = lineno
    return t

indentno = 0

def printTree(tree):
    global indentno
    indentno += 2 # INDENT
    while tree != None:
        printSpaces();
        if (tree.nodekind == NodeKind.StmtK):
            if tree.stmt == StmtKind.IfK:
                print(tree.lineno, "If")
            elif tree.stmt == StmtKind.RepeatK:
                print(tree.lineno, "Repeat")
            elif tree.stmt == StmtKind.AssignK:
                print(tree.lineno, "Assign to: ",tree.name)
            elif tree.stmt == StmtKind.ReadK:
                print(tree.lineno, "Read: ",tree.name)
            elif tree.stmt == StmtKind.WriteK:
                print(tree.lineno, "Write")
            else:
                print(tree.lineno, "Unknown ExpNode kind")
        elif tree.nodekind == NodeKind.ExpK:
            if tree.exp == ExpKind.OpK:
                print(tree.lineno, "Op: ", end ="")
                printToken(tree.op," ")
            elif tree.exp == ExpKind.ConstK:
                print(tree.lineno, "Const: ",tree.val)
            elif tree.exp == ExpKind.IdK:
                print(tree.lineno, "Id: ",tree.name)
            else:
                print(tree.lineno, "Unknown ExpNode kind")
        else:
            print(tree.lineno, "Unknown node kind");
        for i in range(MAXCHILDREN):
            printTree(tree.child[i])
        tree = tree.sibling
    indentno -= 2 #UNINDENT

def parser(imprime = True):
    global token, tokenString, lineno
    token, tokenString = getToken(imprimeScanner)
    t = declaration_list()
    if (token != TokenType.ENDFILE):
        syntaxError("Code ends before file. Missing ENDFILE character ($)\n")
    if imprime:
        printTree(t)
    return Error
