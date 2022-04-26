from lexer import *
from TypeExpression import *
from Node import *

token = None # holds current token
tokenString = None # holds the token string value
Error = False
SintaxTree = None
imprimeScanner = False
root = None

def match(expected):
    global token, tokenString, lineno
    if token == expected:
        token, tokenString, lineno = getToken(imprimeScanner)
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
            else:
                root.children.append(q)
                p = q

def type_specifier():
    global token
    if token == TokenType.INT:
        match(token)
        return ExpType.Integer
    else:
        match(TokenType.VOID)
        return ExpType.Void

def declaration(param=False):
    global token, tokenString, lineno
    # import ipdb; ipdb.set_trace()
    var_type = type_specifier()
    var_name = tokenString
    match(TokenType.ID)
    t = newExpNode(ExpKind.IdK)
    t.lineno = lineno
    t.name = var_name
    t.type = var_type
    if not param:
        if token == TokenType.OPENBRACKET:
            t.type = ExpType.Array
            match(TokenType.OPENBRACKET)
            t.size = int(tokenString)
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
            token, tokenString, lineno = getToken()
    else:
        if token == TokenType.OPENBRACKET:
            t.type = ExpType.Array
            match(TokenType.OPENBRACKET)
            match(TokenType.CLOSEBRACKET)
    return t

def params():
    global token, tokenString, lineno
    t = newExpNode(ExpKind.ParamsK)
    t.lineno = lineno
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
    global lineno
    t = newStmtNode(StmtKind.BodyK)
    t.lineno = lineno
    match(TokenType.OPENCURLY)
    t.children += [local_declaration()]
    statement_list(t)
    match(TokenType.CLOSECURLY)
    return t

def local_declaration():
    global lineno
    t = newExpNode(ExpKind.LocalsK)
    t.lineno = lineno
    while token == TokenType.INT:
        t.children += [declaration()]
    return t

def statement_list(parent):
    # import ipdb; ipdb.set_trace()
    while token != TokenType.CLOSECURLY and token != TokenType.ELSE:
        if token == TokenType.INT or token == TokenType.OPENCURLY:
            parent.children += [compound_stmt()]
        elif token == TokenType.ID:
            parent.children += [expression()]
            match(TokenType.SEMICOLON)
        elif token == TokenType.RETURN:
            parent.children += [return_stmt()]
        elif token == TokenType.IF:
            parent.children += [selection_stmt()]
        elif token == TokenType.WHILE:
            parent.children += [iteration_stmt()]

def iteration_stmt():
    # import ipdb; ipdb.set_trace()
    t = newStmtNode(StmtKind.WhileK)
    match(TokenType.WHILE)
    match(TokenType.OPENPAR)
    condition = expression()
    match(TokenType.CLOSEPAR)
    t.children += [condition]
    statement_list(t)
    return t

def selection_stmt():
    # import ipdb; ipdb.set_trace()
    t = newStmtNode(StmtKind.IfK)
    match(TokenType.IF)
    match(TokenType.OPENPAR)
    condition = expression()
    match(TokenType.CLOSEPAR)
    t.children += [condition]
    statement_list(t)
    if token == TokenType.ELSE:
        match(TokenType.ELSE)
        statement_list(t)
    return t

def expression():
    # import ipdb; ipdb.set_trace()
    t = None
    if token == TokenType.ID:
        t = newExpNode(ExpKind.IdK)
        t.name = tokenString
        name = t.name
        t.type = ExpType.Integer
        match(TokenType.ID)
        if token in (TokenType.PLUS, TokenType.MINUS):
            op = newExpNode(ExpKind.OpK)
            op.op = token
            match(token)
            right = add_expression()
            op.children += [t, right]
            return op
        elif token == TokenType.OPENBRACKET:
            # import ipdb; ipdb.set_trace()
            t = newStmtNode(StmtKind.ArrayAtK)
            t.name = name
            t.type = ExpType.Array
            match(TokenType.OPENBRACKET)
            index = expression()
            match(TokenType.CLOSEBRACKET)
            t.children += [index]
            if token == TokenType.EQUALS:
                assign = newStmtNode(StmtKind.AssignK)
                assign.name = name
                match(TokenType.EQUALS)
                q = expression()
                assign.children += [t, q]
                return assign
            elif token == TokenType.SEMICOLON:
                return t
            elif token in (TokenType.LESSTHAN, TokenType.LEQ, TokenType.GREATERTHAN, TokenType.GEQ, TokenType.EQEQ, TokenType.DIFF):
                op = newExpNode(ExpKind.OpK)
                op.op = token
                match(token)
                right = expression()
                op.children += [t, right]
                return op
        elif token == TokenType.EQUALS:
            name = t.name
            assign = newStmtNode(StmtKind.AssignK)
            assign.name = name
            match(TokenType.EQUALS)
            q = expression()
            assign.children += [t, q]
            return assign
        elif token == TokenType.SEMICOLON:
            t = newExpNode(ExpKind.IdK)
            t.name = name
            t.type = ExpType.Integer
        elif token in (TokenType.LESSTHAN, TokenType.LEQ, TokenType.GREATERTHAN, TokenType.GEQ, TokenType.EQEQ, TokenType.DIFF):
            cond = newExpNode(ExpKind.OpK)
            cond.op = token
            match(token)
            p = add_expression()
            cond.children += [t, p]
            return cond
        elif token == TokenType.OPENPAR:
            t = newStmtNode(StmtKind.FunCallK)
            t.name = name
            match(TokenType.OPENPAR)
            args(t)
            match(TokenType.CLOSEPAR)
            return t
        elif token == TokenType.COMMA:
            return t
    else:
        t = add_expression()
        if token in (TokenType.LESSTHAN, TokenType.LEQ, TokenType.GREATERTHAN, TokenType.GEQ, TokenType.EQEQ, TokenType.DIFF):
            q = newExpNode(ExpKind.OpK)
            q.op = token
            q.children += [t]
            match(token)
            t = add_expression()
            q.children += [t]
            t = q
    return t

def return_stmt():
    global lineno
    match(TokenType.RETURN)
    return_node = newStmtNode(StmtKind.ReturnK)
    return_node.lineno = lineno
    if token != TokenType.SEMICOLON:
        return_node.children += [add_expression()]
    else:
        return_node.type = ExpType.Void
    match(TokenType.SEMICOLON)
    return return_node

def add_expression():
    # import ipdb; ipdb.set_trace()
    left = term()
    while token in (TokenType.PLUS, TokenType.MINUS):
        tree = newExpNode(ExpKind.OpK)
        if tree:
            tree.children += [left]
            tree.op = token
            left = tree
            match(token)
            left.children += [term()]
    return left

def term():
    # import ipdb; ipdb.set_trace()
    t = factor();
    while token == TokenType.TIMES or token == TokenType.DIV:
        p = newExpNode(ExpKind.OpK)
        if p != None:
            p.children += [t]
            p.op = token
            t = p
            match(token)
            t.children += [factor()]
    return t

def factor():
    # import ipdb; ipdb.set_trace()
    global token, tokenString
    t = None
    if token == TokenType.NUM:
        t = newExpNode(ExpKind.ConstK)
        t.type = ExpType.Integer
        if t != None and token == TokenType.NUM:
            t.val = int(tokenString)
        match(TokenType.NUM)
    elif token == TokenType.ID:
        name = tokenString
        match(TokenType.ID)
        if token == TokenType.OPENPAR:
            t = newStmtNode(StmtKind.FunCallK)
            t.type = ExpType.Integer
            t.name = name
            match(TokenType.OPENPAR)
            arguments = args(t)
            if arguments:
                t.children += [arguments]
            match(TokenType.CLOSEPAR)
        elif token == TokenType.OPENBRACKET:
            t = newExpNode(ExpKind.IdK)
            t.name = name
            t.type = ExpType.Array
        else:
            t = newExpNode(ExpKind.IdK)
            t.type = ExpType.Integer
            t.name = name
    elif token == TokenType.OPENPAR:
        match(TokenType.OPENPAR)
        t = add_expression()
        match(TokenType.CLOSEPAR)
    else:
        syntaxError("unexpected token -> ")
        printToken(token,tokenString)
        token, tokenString, lineno = getToken()
    return t

def args(parent):
    # import ipdb; ipdb.set_trace()
    if token != TokenType.CLOSEPAR:
        parent.children += [expression()]
        while token == TokenType.COMMA:
            match(token)
            parent.children += [expression()]

def printToken(token, tokenString):
    if token in {TokenType.IF, TokenType.ELSE}:
        print(" reserved word: " + tokenString)
    elif token == TokenType.OPENPAR:
        print("(")
    elif token == TokenType.CLOSEPAR:
        print(")")
    elif token == TokenType.ENDFILE:
        print("EOF")
    elif token == TokenType.EQUALS:
        print("=")
    elif token == TokenType.LESSTHAN:
        print("<")
    elif token == TokenType.EQEQ:
        print("==")
    elif token == TokenType.SEMICOLON:
        print(";")
    elif token == TokenType.PLUS:
        print("+")
    elif token == TokenType.MINUS:
        print("-")
    elif token == TokenType.TIMES:
        print("*")
    elif token == TokenType.DIV:
        print("/")
    elif token == TokenType.NUM:
      print("NUM, val= " + tokenString)
    elif token == TokenType.ID:
        print("ID, name= " + tokenString);
    elif token == TokenType.ERROR:
        print("ERROR: " + tokenString)
    else: # should never happen
        if type(token) == TokenType:
            print("Unknown token: " + token.value)
        else:
            print("Unknown token: " + token)

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
            elif tree.stmt == StmtKind.WhileK:
                print(tree.lineno, "While: ")
            elif tree.stmt == StmtKind.AssignK:
                print(tree.lineno, "Assign: ")
            elif tree.stmt == StmtKind.Inputk:
                print(tree.lineno, "Input: ", tree.name)
            elif tree.stmt == StmtKind.OutputK:
                print(tree.lineno, "Output")
            elif tree.stmt == StmtKind.BodyK:
                print(tree.lineno, "Body: ")
            elif tree.stmt == StmtKind.ReturnK:
                print(tree.lineno, "Return: ")
            elif tree.stmt == StmtKind.FunCallK:
                print(tree.lineno, "Call: ", tree.name)
            elif tree.stmt == StmtKind.ArrayAtK:
                print(tree.lineno, "Array: ", tree.name, ' at index:')
            else:
                print(tree.lineno, "Unknown ExpNode kind")
        elif tree.nodekind == NodeKind.ExpK:
            if tree.exp == ExpKind.RootK:
                print(tree.lineno, tree.name)
            elif tree.exp == ExpKind.OpK:
                print(tree.lineno, "Op: ", end ="")
                printToken(tree.op, " ")
            elif tree.exp == ExpKind.ConstK:
                print(tree.lineno, "Const: ", tree.val)
            elif tree.exp == ExpKind.IdK:
                print(tree.lineno, "Id:", tree.name + ' Type: ', tree.type, end='')
                if tree.size:
                    print(' Size: ', tree.size)
                else:
                    print('')
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

def parser(imprime = True):
    global token, tokenString, lineno, root
    token, tokenString, lineno = getToken(imprimeScanner)
    root = newExpNode(ExpKind.RootK)
    root.name = 'Root'
    declaration_list()
    if (token != TokenType.ENDFILE):
        syntaxError("Code ends before file. Missing ENDFILE character ($)\n")
    if imprime:
        printTree(root)
    return Error
