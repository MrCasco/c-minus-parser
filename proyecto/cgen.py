from globalTypes import *

file_code = []

def suma(t):
    codeGen(t.childNodes[0], file_name)
    file_code.append(str('  sw $a0 0($sp)'))
    file_code.append('  addiu $sp $sp ‐4')
    codeGen(t.childNodes[1].childNodes[1], file_name)
    file_code.append('  lw $t1 4($sp)')
    if t.op == '-':
        file_code.append('  sub $a0 $t1 $a0')
    else:
        file_code.append('  add $a0 $t1 $a0')
    file_code.append('  addiu $sp $sp 4')


def codeGen(t, file_name):
    if t.nodekind == NodeKind.ExpK:
        if t.exp == ExpKind.RootK:
            file_code.append('.text')
            file_code.append('.align 2')
            file_code.append('.globl main')
            for child in t.children:
                codeGen(child, file_name)

        elif t.exp == ExpKind.OpK:
            if t.op == '+' or t.op == '-':
                suma(t)

    print('\n'.join(file_code))
    with open('assembly.s', 'w') as f:
        f.writelines(file_code)
