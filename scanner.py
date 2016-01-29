import sys

import ply.lex as lex

firstInput = sys.argv[1]
inputFile = open(firstInput)
# Remove inputs/ and .micro from input file name
outputName = firstInput[7:-6] + ".out"
# create new file in outputs/
outputFile = open("outputs/" + outputName, "w+")
outputFile.close()

data = inputFile.read()


def writeOut(tokenType, value):
    with open("outputs/" + outputName, "a+") as f:
        # \r\n is needed so diff works properly (He has stupid C/windows style carriage returns in his testOutput files)
        print("Token Type: " + tokenType + "\nValue: " + value.strip())
        f.write("Token Type: " + tokenType + "\r\n")
        f.write("Value: " + value.strip() + "\r\n")


# List of token names.   This is always required
tokens = (
    'KEYWORD',
    'OPERATOR',
    'LINE_COMMENT',
    'STRINGLITERAL',
    'FLOATLITERAL',
    'INTLITERAL',
    'IDENTIFIER',
)


def t_LINE_COMMENT(t):
    r'--.*(\n|$)'
    # writeOut("COMMENT", t.value)


def t_KEYWORD(t):
    r'(^|\ *)(PROGRAM|BEGIN|FUNCTION|READ|WRITE|ENDIF|IF|ELSE|ENDWHILE|WHILE|CONTINUE|BREAK|RETURN|END|INT|VOID|STRING|FLOAT|VOID|READ|WRITE)(\ *|$)'
    writeOut("KEYWORD", t.value)


def t_OPERATOR(t):
    r'(^|\ *)(\<=|\>=|:=|\+|\-|\*|/|=|!=|\<|\>|\(|\)|;|,)(\s*|$)'
    writeOut("OPERATOR", t.value)


def t_STRINGLITERAL(t):
    r'(\".*\")|(\'.*\')'
    writeOut("STRINGLITERAL", t.value)


def t_FLOATLITERAL(t):
    r'(-|)(\d*)(\.)(\d+)\ *'
    writeOut("FLOATLITERAL", t.value)


def t_INTLITERAL(t):
    r'(-|)(\d+)\ *'
    writeOut("INTLITERAL", t.value)


def t_IDENTIFIER(t):
    r'(^|\ *)[a-zA-Z_]\w*(\s*|$)'
    writeOut("IDENTIFIER", t.value)


t_ignore = '\t\n'


# Error handling rule
def t_error(t):
    # print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

# Test it out

# Give the lexer some input
lexer.input(data)

# Tokenize

while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
        # print(tok.value)
