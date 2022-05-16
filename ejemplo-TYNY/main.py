from globalTypes import *
#from scanner import *
from Parser import *
from analyze import *
# from cgen import *

fileName = "prueba"
f = open(fileName + '.tny', 'r')
program = f.read() 		# lee todo el archivo a compilar
f.close()                       # cerrar el archivo con programa fuente
progLong = len(program) 	# longitud original del programa
program = program + '$' 	# agregar un caracter $ que represente EOF
position = 0 			# posición del caracter actual del string

### Para probar el scanner solito
##recibeScanner(program, position, progLong) # para mandar los globales
##
##token, tokenString = getToken()
##while (token != TokenType.ENDFILE):
##    token, tokenString = getToken()

Error = False
recibeParser(program, position, progLong) # para mandar los globales al parser
syntaxTree, Error = parse(True)

if not(Error):
    print()
    print("Building Symbol Table...")
    buildSymtab(syntaxTree, True)
    print()
    print("Checking Types...")
    typeCheck(syntaxTree)
    print()
    print("Type Checking Finished")
    # print(BucketList) # ¿Por qué se mantiene esta variable si está declarada en symtab.py?
# if not(Error):
#     codeGen(syntaxTree, fileName, True)
