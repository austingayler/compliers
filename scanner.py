import sys

import ply.lex as lex

firstInput = sys.argv[1]
inputFile = open(firstInput)

data = inputFile.read()


def writeOut(tokenType, value):
    pass


# List of token names.   This is always required
tokens = (
    'LINE_COMMENT',
    'STRINGLITERAL',
    'FLOATLITERAL',
    'INTLITERAL',

    "BEGIN",
    "PROGRAM",
    "STRING",
    "FLOAT",
    "INT",
    "END",
    "VOID",
    "FUNCTION",
    "READ",
    "WRITE",
    "IF",
    "ELSE",
    "ENDIF",
    "WHILE",
    "ENDWHILE",
    "CONTINUE",
    "RETURN",
    "BREAK",

    "COMPOP",
    "ASSIGN",
    "SEMI",
    "COMMA",
    "LPAREN",
    "RPAREN",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    'IDENTIFIER',

)

t_ASSIGN = r":="
t_SEMI = r";"
t_COMMA = r","
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_PLUS = r"\+"
t_MINUS = r"\-"
t_TIMES = r"\*"
t_DIVIDE = r"\/"
t_COMPOP = r"(<=|>=|!=|<|>|=)"


def t_LINE_COMMENT(t):
    r'--.*(\n|$)'
    # writeOut("COMMENT", t.value)
    pass


def t_ENDWHILE(t):
    r'(^|\ *)(ENDWHILE)(\ *|$)'
    return t


def t_ENDIF(t):
    r'(^|\ *)(ENDIF)(\ *|$)'
    return t


def t_FLOAT(t):
    r'(^|\ *)(FLOAT)(\ *|$)'
    return t


def t_STRING(t):
    r'(^|\ *)(STRING)(\ *|$)'
    return t


def t_VOID(t):
    r'(^|\ *)(VOID)(\ *|$)'
    return t


def t_INT(t):
    r'(^|\ *)(INT)(\ *|$)'
    return t


def t_END(t):
    r'(^|\ *)(END)(\ *|$)'
    return t


def t_RETURN(t):
    r'(^|\ *)(RETURN)(\ *|$)'
    return t


def t_BREAK(t):
    r'(^|\ *)(BREAK)(\ *|$)'
    return t


def t_CONTINUE(t):
    r'(^|\ *)(CONTINUE)(\ *|$)'
    return t


def t_WHILE(t):
    r'(^|\ *)(WHILE)(\ *|$)'
    return t


def t_ELSE(t):
    r'(^|\ *)(ELSE)(\ *|$)'
    return t


def t_IF(t):
    r'(^|\ *)(IF)(\ *|$)'
    return t


def t_WRITE(t):
    r'(^|\ *)(WRITE)(\ *|$)'
    return t


def t_READ(t):
    r'(^|\ *)(READ)(\ *|$)'
    return t


def t_FUNCTION(t):
    r'(^|\ *)(FUNCTION)(\ *|$)'
    return t


def t_BEGIN(t):
    r'(^|\ *)(BEGIN)(\ *|$)'
    return t


def t_PROGRAM(t):
    r'(^|\ *)(PROGRAM)(\ *|$)'
    return t


def t_STRINGLITERAL(t):
    r'(\".*?\")|(\'.*?\')'
    return t


def t_FLOATLITERAL(t):
    r'(\d*)(\.)(\d+)\ *'
    return t


def t_INTLITERAL(t):
    r'(\d+)\ *'
    return t


def t_IDENTIFIER(t):
    r'(^|\ *)[a-zA-Z_]\w*(\s*|$)'
    return t


t_ignore = '\t\n\r'


# Error handling rule
def t_error(t):
    # print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
