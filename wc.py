import sys

import ply.lex as lex
import re

firstInput = sys.argv[1]
inputFile = open(firstInput)
# Remove inputs/ and .micro from input file name
outputName = firstInput[7:-6] + ".out"
# create new file in outputs/
outputFile = open("outputs/" + outputName, "w+")
outputFile.close()

data = inputFile.read()

def writeToFile(fileName, content):
    with open("outputs/" + fileName, "a+") as f:
        f.write(content + "\n")


def writeOut(tokenType, value):
    with open("outputs/" + outputName, "a+") as f:
        f.write("Token Type: " + tokenType + "\n")
        f.write("Value: " + value.strip() + "\n")


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


def t_KEYWORD(t):
    r'(^| )(?i)(PROGRAM|BEGIN|END|FUNCTION|READ|WRITE|IF|ELSE|ENDIF|WHILE|ENDWHILE|CONTINUE|BREAK|RETURN|INT| \
    VOID|STRING|FLOAT)(\s|$)'
    writeOut("KEYWORD", t.value)


def t_OPERATOR(t):
    r'(^| )(:=|\+|\-|\*|/|=|!=|\<|\>|\(|\)|;|,|\<=|\>=)(\s|$)'
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
    r'(^| )[a-zA-Z_]\w*(\s|$)'
    writeOut("IDENTIFIER", t.value)


def t_LINE_COMMENT(t):
    r'--.*(\n|$)'
    # writeOut("COMMENT", t.value)


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
