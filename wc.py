import ply.lex as lex
import sys

firstInput = sys.argv[1]
inputFile = open(firstInput)
data = inputFile.read()

# List of token names.   This is always required
tokens = (
   'KEYWORD',
   'LINE_COMMENT',
   'STRINGLITERAL',
   'FLOATLITERAL',
   'INTLITERAL',
   'IDENTIFIER',
)
# Define a rule so we can track line numbers
def t_KEYWORD(t):
    r'(^| )(?i)(PROGRAM|BEGIN|END|FUNCTION|READ|WRITE|IF|ELSE|ENDIF|WHILE|ENDWHILE|CONTINUE|BREAK|RETURN|INT|VOID|STRING|FLOAT)(\s|$)'
    print("Token Type: KEYWORD")
    print("Value: "+t.value.strip())

def t_OPERATOR(t):
    
    r'(^| )(:=|\+|\-|\*|/|=|!=|\<|\>|\(|\)|;|,|\<=|\>=)(\s|$)'
    print("Token Type: OPERATOR")
    print("Value: "+t.value.strip())

def t_STRINGLITERAL(t):
    r'(\".*\")|(\'.*\')'
    print("Token Type: STRINGLITERAL")
    print("Value: "+t.value.strip())

def t_FLOATLITERAL(t):
    r'(-|)(\d*)(\.)(\d+)\ *'
    print("Token Type: FLOATLITERAL")
    print("Value: "+t.value.strip())

def t_INTLITERAL(t):
    r'(-|)(\d+)\ *'
    print("Token Type: INTLITERAL")
    print("Value: "+t.value.strip())

def t_IDENTIFIER(t):
    r'(^| )[a-zA-Z_]\w*(\s|$)'
    print("Token Type: IDENTIFIER")
    print("Value: "+t.value.strip())

def t_LINE_COMMENT(t):
    r'--.*(\n|$)'
#    print("Line Comment: "+t.value.strip())

# A string containing ignored characters (spaces and tabs)
# t_ignore  = ' \t'

#Error handling rule
def t_error(t):
    #print("Illegal character '%s'" % t.value[0])
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
        break      # No more input
    # print(tok.value)
