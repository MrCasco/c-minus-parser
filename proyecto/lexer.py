from globalTypes import *


incomment = False
lineno = 1

def globalesLexer(programa, posicion, progLong):
    global string, p, lng
    p = posicion
    lng = progLong
    string = programa

def reset(lexem, token, imprime=True):
    if imprime:
        print(lexem, token)
    global p
    p += 1
    return '', 0

def getToken(imprime=True):
    global string
    global p
    global lineno
    global incomment
    table = [
        [1, 3, 12, 18, 13, 5, 6, 7, 8, 9, 10, 11, 14, 15, 16, 17, 19, 20, 0],
        [1]+[2]*19,
        [0]*20,
        [4, 3]+[4]*18,
        [0]*20,
        [0]*20,
        [0]*20,
        [32]*8+[31]+[32]*11,
        [29]*7+[30]+[29]*12,
        [21]*11+[22]+[21]*8,
        [23]*11+[24]+[23]*8,
        [25]*11+[26]+[25]*8,
        [0]*20,
        [0]*20,
        [0]*20,
        [0]*20,
        [0]*20,
        [0]*20,
        [0]*20,
        [0]*20,
        [27]*11+[28]+[27]*8,
        [0]*20,
        [0]*20,
        [0]*20,
        [0]*20,
        [0]*20,
        [0]*20,
        [0]*20,
        [0]*20,
        [0]*20,
        [0]*7+[7]+[0]*12,
        [0]*20
    ]
    reserved = {
        'else': TokenType.ELSE,
        'if': TokenType.IF,
        'int': TokenType.INT,
        'return': TokenType.RETURN,
        'void': TokenType.VOID,
        'while': TokenType.WHILE
    }
    # s = '1+1$'
    # string = 'int gcd(int u, int v){ /**/ }$'
    # string = '!=!=!=$'
    # string = '*$'
    # string = open('test.c', 'r')
    # string = string.read() + '$'     # lee todo el archivo a compilar

    blank = ' \n\t$'
    digit = '0123456789'
    letter = 'acbdefghijklmnopqrstuvwxyz'+'acbdefghijklmnopqrstuvwxyz'.upper()

    state = 0
    lexem = ''
    token = ''
    # import ipdb; ipdb.set_trace()
    while p < len(string) and (string[p] != '$' or (string[p] == '$' and state != 0)):
        char = string[p]
        if char in letter:
            col = 0
        elif char in blank:
            if char == '\n':
                lineno += 1
            col = 18
        elif char in digit:
            col = 1
        elif char == '[':
            col = 2
        elif char == ',':
            col = 3
        elif char == ']':
            col = 4
        elif char == '+':
            col = 5
        elif char == '-':
            col = 6
        elif char == '*':
            col = 7
        elif char == '/':
            col = 8
        elif char == '<':
            col = 9
        elif char == '>':
            col = 10
        elif char == '=':
            col = 11
        elif char == '(':
            col = 12
        elif char == ')':
            col = 13
        elif char == '{':
            col = 14
        elif char == '}':
            col = 15
        elif char == ';':
            col = 16
        elif char == '!':
            col = 17
        else:
            if incomment:
                state = 0
                col = 0
            else:
                return TokenType.ERROR, 'ERROR' + char + 'invalid'

        state = table[state][col]

        if state == 2:
            p -= 1
            if lexem in reserved:
                token = reserved[lexem]
            else:
                token = TokenType.ID
            lx = lexem
            lexem, state = reset(lexem, token, imprime)
            if not incomment:
                return token, lx, lineno
            else:
                state = 7
        elif state == 4:
            p -= 1
            token = TokenType.NUM
            lx = lexem
            lexem, state = reset(lexem, token, imprime)
            if not incomment:
                return token, lx, lineno
        elif state == 5:
            token = TokenType.PLUS
            lexem = '+'
            lx = lexem
            lexem, state = reset(lexem, token, imprime)
            if not incomment:
                return token, lx, lineno
        elif state == 6:
            token = TokenType.MINUS
            lexem = '-'
            lx = lexem
            lexem, state = reset(lexem, token, imprime)
            if not incomment:
                return token, lx, lineno
        elif state == 12:
            token = TokenType.OPENBRACKET
            lexem += '['
            lx = lexem
            lexem, state = reset(lexem, token, imprime)
            if not incomment:
                return token, lx, lineno
        elif state == 13:
            token = TokenType.CLOSEBRACKET
            lexem = ']'
            lx = lexem
            lexem, state = reset(lexem, token, imprime)
            if not incomment:
                return token, lx, lineno
        elif state == 14:
            token = TokenType.OPENPAR
            lexem = '('
            lx = lexem
            lexem, state = reset(lexem, token, imprime)
            if not incomment:
                return token, lx, lineno
        elif state == 15:
            token = TokenType.CLOSEPAR
            lexem = ')'
            lx = lexem
            lexem, state = reset(lexem, token, imprime)
            if not incomment:
                return token, lx, lineno
        elif state == 16:
            token = TokenType.OPENCURLY
            lexem = '{'
            lx = lexem
            lexem, state = reset(lexem, token, imprime)
            if not incomment:
                return token, lx, lineno
        elif state == 17:
            token = TokenType.CLOSECURLY
            lexem = '}'
            lx = lexem
            lexem, state = reset(lexem, token, imprime)
            if not incomment:
                return token, lx, lineno
        elif state == 18:
            token = TokenType.COMMA
            lexem = ','
            lx = lexem
            lexem, state = reset(lexem, token, imprime)
            if not incomment:
                return token, lx, lineno
        elif state == 19:
            token = TokenType.SEMICOLON
            lexem = ';'
            lx = lexem
            lexem, state = reset(lexem, token, imprime)
            if not incomment:
                return token, lx, lineno
        elif state == 21:
            token = TokenType.LESSTHAN
            lexem = '<'
            lx = lexem
            lexem, state = reset(lexem, token, imprime)
            if not incomment:
                return token, lx, lineno
        elif state == 22:
            token = TokenType.LEQ
            lexem = '<='
            lx = lexem
            lexem, state = reset(lexem, token, imprime)
            if not incomment:
                return token, lx, lineno
        elif state == 23:
            token = TokenType.GREATERTHAN
            lexem = '>'
            lx = lexem
            lexem, state = reset(lexem, token, imprime)
            if not incomment:
                return token, lx, lineno
        elif state == 24:
            token = TokenType.GEQ
            lexem = '>='
            lx = lexem
            lexem, state = reset(lexem, token, imprime)
            if not incomment:
                return token, lx, lineno
        elif state == 25:
            token = TokenType.EQUALS
            lexem = '='
            lx = lexem
            lexem, state = reset(lexem, token, imprime)
            if not incomment:
                return token, lx, lineno
        elif state == 26:
            token = TokenType.EQEQ
            lexem = '=='
            lx = lexem
            lexem, state = reset(lexem, token, imprime)
            if not incomment:
                return token, lx, lineno
        elif state == 27:
            token = TokenType.ERROR
            lexem = '!'
            lx = lexem
            lexem, state = reset(lexem, token, imprime)
            if not incomment:
                return token, lx, lineno
        elif state == 28:
            token = TokenType.DIFF
            lexem = '!='
            lx = lexem
            lexem, state = reset(lexem, token, imprime)
            if not incomment:
                return token, lx, lineno
        elif state == 29:
            p -= 1
            token = TokenType.DIV
            lexem = '/'
            lx = lexem
            lexem, state = reset(lexem, token, imprime)
            if not incomment:
                return token, lx, lineno
        elif state == 30:
            p -= 1
            token = TokenType.OPENCMNT
            lexem = '/*'
            lx = lexem
            lexem, state = reset(lexem, token, imprime)
            incomment = True
        elif state == 31:
            token = TokenType.CLOSECMNT
            lexem = '*/'
            lx = lexem
            lexem, state = reset(lexem, token, imprime)
            incomment = False
        elif state == 32:
            p -= 1
            token = TokenType.TIMES
            lexem = '*'
            lx = lexem
            lexem, state = reset(lexem, token, imprime)
            if not incomment:
                return token, lx, lineno
        p += 1
        if state != 0:
            if char in ' ':
                p -= 1
            else:
                lexem += char
        else:
            while p < lng and string[p] in blank:
                if string[p] == '\n':
                    lineno += 1
                p += 1
    return TokenType.ENDFILE, '$', lineno
