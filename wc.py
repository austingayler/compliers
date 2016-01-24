
import ply.lex as lex

newline_counter = 0
word_counter = 0
character_counter = 0
# List of token names.   This is always required
tokens = (
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'NEW_LINE',
   'WORD',
)

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_NEW_LINE= r'\n'

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    global newline_counter
    newline_counter += 1
    t.lexer.lineno += len(t.value)

def t_WORD(t):
    r'\w+'
    global word_counter
    global character_counter
    character_counter = character_counter + len(t.value)
    word_counter = word_counter + 1
    return t

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test it out
data = '''
6 7 23
three more words
'''

# Give the lexer some input
lexer.input(data)

# Tokenize

while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    # print(tok.value)
print(str(newline_counter)+" "+str(word_counter)+" "+str(character_counter))
