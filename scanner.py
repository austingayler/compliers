import sys

import ply.lex as lex
import re
import os

firstInput = sys.argv[1]
inputFile = open(firstInput)

# Remove os agnostic path and .micro from input file name
outputName = re.sub('\.micro', '', firstInput)
pathSep = os.path.sep
regex = r'(.+'+ re.escape(pathSep) + r')*'
outputName = re.sub(regex, '', outputName) + ".out"
# create new file in outputs/
outputFile = open("outputs/" + outputName, "w+")
outputFile.close()

data = inputFile.read()


def writeOut(tokenType, value):
    with open("outputs/" + outputName, "a+") as f:
        # \r\n is needed so diff works properly (He has stupid C/windows style carriage returns in his testOutput files)
        #print("Token Type: " + tokenType + "\nValue: " + value.strip())
        f.write("Token Type: " + tokenType + "\n")
        f.write("Value: " + value + "\n")


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
    return t


def t_KEYWORD(t):
    r'(^|\ *)(PROGRAM|BEGIN|FUNCTION|READ|WRITE|ENDIF|IF|ELSE|ENDWHILE|WHILE|CONTINUE|BREAK|RETURN|END|INT|VOID|STRING|FLOAT|VOID|READ|WRITE)(\ *|$)'
    writeOut("KEYWORD", t.value)
    return t


def t_OPERATOR(t):
    r'(^|\ *)(\<=|\>=|:=|\+|\-|\*|/|=|!=|\<|\>|\(|\)|;|,)'
    writeOut("OPERATOR", t.value)
    return t


def t_STRINGLITERAL(t):
    r'(\".*\")|(\'.*\')'
    writeOut("STRINGLITERAL", t.value)
    return t


def t_FLOATLITERAL(t):
    r'(-|)(\d*)(\.)(\d+)\ *'
    writeOut("FLOATLITERAL", t.value)
    return t


def t_INTLITERAL(t):
    r'(-|)(\d+)\ *'
    writeOut("INTLITERAL", t.value)
    return t


def t_IDENTIFIER(t):
    r'(^|\ *)[a-zA-Z_]\w*'
    writeOut("IDENTIFIER", t.value)
    return t


t_ignore = '\t\n\r'


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
    print(tok)
