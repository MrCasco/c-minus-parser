from globalTypes import *
from symtab import *

Error = False
location = 0
cur_table = 0
prev_var = None

# Stack that has all symbol
# tables within the environment
tables = [{}]

def needNewStack(ast):
    if ast.exp == ExpKind.IdK and len(ast.children) == 2:
        return True
    return ast.statement in (StmtKind.IfK, StmtKind.WhileK)

def generateTable(ast):
    # import ipdb; ipdb.set_trace()
    global tables, cur_table
    needed_new_stack = False

    if needNewStack(ast):
        insertNode(ast)
        tables += [{}]
        prev_table = cur_table
        cur_table = len(tables)-1
        needed_new_stack = True
    else:
        insertNode(ast)
    for child in ast.children:
        if child:
            generateTable(child)
    if needed_new_stack:
        cur_table = prev_table

def typeChecker(ast):
    for child in ast.children:
        if child:
            typeChecker(child)
    checkNode(ast)

# Procedure insertNode inserts identifiers stored in t into
# the symbol table
def insertNode(t):
    # import ipdb; ipdb.set_trace()
    global location, cur_table, prev_var
    if t.nodekind == NodeKind.StmtK:
        if t.statement in [StmtKind.AssignK, StmtKind.Inputk]:
            if st_lookup(t.name, tables[cur_table]) == -1:
                # not yet in table, so treat as error
                print('Unknown variable:', t.name, 'has not been previously declared at line', t.lineno)
                Error = True
    elif t.nodekind == NodeKind.ExpK:
        if t.exp == ExpKind.IdK:
            if (st_lookup(t.name, tables[cur_table]) == -1):
                # not yet in table, so treat as new definition */
                st_insert(t, tables, cur_table)
            else:
                tables[cur_table][t.name]['type'] = t.type
# Function buildSymtab constructs the symbol
# table by preorder traversal of the syntax tree
def tabla(syntaxTree, imprime):
    generateTable(syntaxTree)
    # traverse(syntaxTree, insertNode, nullProc)
    if imprime:
        print()
        print("Symbol table:")
        printSymTables(tables)

def typeError(t, message):
    print("Type error at line", t.lineno, ":",message)
    Error = True

# Procedure checkNode performs type checking at a single tree node
def checkNode(t):
    if t.nodekind == NodeKind.ExpK:
        if t.exp == ExpKind.OpK:
            if ((t.child[0].type != ExpType.Integer) or (t.child[1].type != ExpType.Integer)):
                typeError(t,"Op applied to non-integer")
            if ((t.op == TokenType.EQ) or (t.op == TokenType.LT)):
                t.type = ExpType.Boolean
            else:
                t.type = ExpType.Integer
        elif t.exp in [ExpKind.ConstK, ExpKind.IdK]:
            t.type = ExpType.Integer
    elif t.nodekind == NodeKind.StmtK:
        if t.statement == StmtKind.IfK:
            if (t.child[0].type == ExpType.Integer):
                typeError(t.child[0],"if test is not Boolean")
        elif t.statement == StmtKind.AssignK:
            if (t.child[0].type != ExpType.Integer):
                typeError(t.child[0],"assignment of non-integer value")
        elif t.statement == StmtKind.WriteK:
            if (t.child[0].type != ExpType.Integer):
                typeError(t.child[0],"write of non-integer value")
        elif t.statement == StmtKind.RepeatK:
            if (t.child[1].type == ExpType.Integer):
                typeError(t.child[1],"repeat test is not Boolean")

# Procedure typeCheck performs type checking
# by a postorder syntax tree traversal
def typeCheck(syntaxTree):
    traverse(syntaxTree,nullProc,checkNode)
