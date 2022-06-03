def suma(t):
    if t.op == '-':
        codeGen(t.childNodes[0], file)
        fileCode.append('     sw $a0 0($sp)')
        fileCode.append('     addiu $sp $sp ‐4')
        codeGen(t.childNodes[1].childNodes[1], file)
        fileCode.append('     lw $t1 4($sp)')
        fileCode.append('     sub $a0 $t1 $a0')
        fileCode.append('     addiu $sp $sp 4')
    elif t.op == '+':
        codeGen(t.childNodes[0], file)
        fileCode.append('     sw $a0 0($sp)')
        fileCode.append('     addiu $sp $sp ‐4')
        codeGen(t.childNodes[1].childNodes[1], file)
        fileCode.append('     lw $t1 4($sp)')
        fileCode.append('     add $a0 $t1 $a0')
        fileCode.append('     addiu $sp $sp 4')


def codeGen(t, file):
    if t.nodekind == StmtK:
        if t.statement == ExpKind.RootK:
            fileCode.append('.text')
            fileCode.append('.align 2')
            fileCode.append('.globl main')
            for child in t.children:
                codeGen(child, file)

        elif t.statement == ExpKind.OpK:
            if t.op == '+' or t.op == '-':
                suma(t, t.op)
    else:
