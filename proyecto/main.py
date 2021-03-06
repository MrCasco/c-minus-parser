from Parser import *
from semantica import *
from cgen import *

f = open('test1.c', 'r')
programa = f.read()       # lee todo el archivo a compilar
progLong = len(programa)   # longitud original del programa
programa = programa + '$'   # agregar un caracter $ que represente EOF
posicion = 0       # posicion del caracter actual del string

# funcion para pasar los valores iniciales de las variables globales
globales(programa, posicion, progLong)

AST = parser(True)

print()
print("Building Symbol Table...")
tabla(AST, False)
print()
print("Checking Types...")
semantica(AST, False)
print()
print("Type Checking Finished")
codeGen(AST, 'assembly_code.s')
