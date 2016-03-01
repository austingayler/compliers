import sys

import ply.lex as lex

firstInput = sys.argv[1]
inputFile = open(firstInput)

# Remove os agnostic path and .micro from input file name
# outputName = re.sub('\.micro', '', firstInput)
# pathSep = os.path.sep
# regex = r'(.+'+ re.escape(pathSep) + r')*'
# outputName = re.sub(regex, '', outputName) + ".out"
# create new file in outputs/
# outputFile = open("Step2/outputs/" + outputName, "w+")
# outputFile.close()

data = inputFile.read()


def writeOut(tokenType, value):
    # pass
    print("Token Type: " + tokenType + "\nValue: " + value.strip())
    # with open("outputs/" + outputName, "a+") as f:
    # \r\n is needed so diff works properly (He has stupid C/windows style carriage returns in his testOutput files)

    # f.write("Token Type: " + tokenType + "\n")
    # f.write("Value: " + value.strip() + "\n")

# IGNORE THESE, tried using the same way that I did with the operators below the
#   tokens, but it didn't seem to work.  Leave them here in case they need to be used.

# "BEGIN",
# "PROGRAM",
# "STRING",
# "FLOAT",
# "INT",
# "END",
# "VOID",
# "FUNCTION",
# "READ",
# "WRITE",
# "IF",
# "ELSE",
# "ENDIF",
# "WHILE",
# "ENDWHILE",
# "CONTINUE",
# "RETURN",
# "BREAK",

# List of token names.   This is always required
tokens = (
    'KEYWORD',
    'OPERATOR',
    'LINE_COMMENT',
    'STRINGLITERAL',
    'FLOATLITERAL',
    'INTLITERAL',

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

# t_PROGRAM = r'(PROGRAM)'
# t_BEGIN = r"(BEGIN)"
# t_END = r"(END)"
# t_INT = r"(INT)"
# t_FLOAT = r"(FLOAT)"
# t_STRING = r"(STRING)"
# t_VOID = r"(VOID)"
# t_FUNCTION = r"(FUNCTION)"
# t_READ = r"(READ)"
# t_WRITE = r"(WRITE)"
# t_IF = r"(IF)"
# t_ELSE = r"(ELSE)"
# t_ENDIF = r"(ENDIF)"
# t_WHILE = r"(WHILE)"
# t_ENDWHILE = r"(ENDWHILE)"
# t_CONTINUE = r"(CONTINUE)"
# t_RETURN = r"(RETURN)"
# t_BREAK = r"(BREAK)"


# SOMETHING IS VERY WRONG, This seems like it should be the way to do it
#  but then the parser doesn't know it is an operator... However OPERATOR
#  isn't even used in the grammer... wttf.
t_ASSIGN = r":="
t_SEMI = r";"
t_COMMA = r","
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_PLUS = r"\+"
t_MINUS = r"\-"
t_TIMES = r"\*"
t_DIVIDE = r"\/"
t_COMPOP = r"(<|>|=|!=|<=|>=)"

def t_LINE_COMMENT(t):
    r'--.*(\n|$)'
    # writeOut("COMMENT", t.value)
    pass


def t_KEYWORD(t):
    r'(^|\ *)(PROGRAM|BEGIN|FUNCTION|READ|WRITE|ENDIF|IF|ELSE|ENDWHILE|WHILE|CONTINUE|BREAK|RETURN|END|INT|VOID|STRING|FLOAT|VOID|READ|WRITE)(\ *|$)'
    writeOut("KEYWORD", t.value)
    t.value = t.value.strip()
    return t


def t_OPERATOR(t):
    r'(^|\ *)(\<=|\>=|:=|\+|\-|\*|/|=|!=|\<|\>|\(|\)|;|,)(\s*|$)'
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
    r'(^|\ *)[a-zA-Z_]\w*(\s*|$)'
    writeOut("IDENTIFIER", t.value)
    t.value = t.value.strip()
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
    # print(tok)
