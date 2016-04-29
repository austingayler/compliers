import listOP
import ply.yacc as yacc
import scanner
from symboltable import *
from Stack import *

tokens = scanner.tokens
data = scanner.data

error = False
id_stack = Stack()

symbol_table = SymbolTable("GLOBAL")  # the scope/symbol table we're currently in
# sym = Symbol("n","v","t")
# symbol_table.add_symbol(sym)
# new_s_t = SymbolTable("new")
# new_s_t.add_symbol(Symbol("1","2","3"))
# symbol_table.add_subtable(new_s_t)

## PROGRAM
def p_program(p):
    'program : PROGRAM id BEGIN pgm_body END'
    print(id_stack.pop()+" program")

def p_id(p):
    'id : IDENTIFIER'
    id_stack.push(p[1])

def p_pgm_body(p):
    'pgm_body : decl func_declarations'
def p_decl(p):
    """decl : string_decl decl
    | var_decl decl
    | empty"""

## GLOBAL STRING DECLARATIONS
def p_string_decl(p):
    'string_decl : STRING id ASSIGN str SEMI'
    print(id_stack.pop()+" string")



def p_str(p):
    'str : STRINGLITERAL'
## Variable Declaration
def p_var_decl(p):
    'var_decl : var_type id_list SEMI'


def p_var_type(p):
    """var_type : FLOAT
    | INT"""
def p_any_type(p):
    """any_type : var_type
    | VOID"""

def p_id_list(p):
    'id_list : id id_tail'



def p_id_tail(p):
    """id_tail : COMMA id id_tail
    | empty"""
    print(id_stack.pop()+" id in list")


## Function Paramater List
def p_param_decl_list(p):
    """param_decl_list : param_decl param_decl_tail
    | empty"""


def p_param_decl(p):
    'param_decl : var_type id'
    print(id_stack.pop()+" is a parameter")



def p_param_decl_tail(p):
    """param_decl_tail : COMMA param_decl param_decl_tail
    | empty"""


## Function Declarations
def p_func_declarations(p):
    """func_declarations : func_decl func_declarations
    | empty"""


def p_func_decl(p):
    """func_decl : FUNCTION any_type id LPAREN param_decl_list RPAREN BEGIN func_body END"""
    print(id_stack.pop()+" is a function")

def p_func_body(p):
    'func_body : decl stmt_list'


## Statement List
def p_stmt_list(p):
    """stmt_list : stmt stmt_list
    | empty"""


def p_stmt(p):
    """stmt : base_stmt
    | if_stmt
    | while_stmt"""


def p_base_stmt(p):
    """base_stmt : assign_stmt
    | read_stmt
    | write_stmt
    | return_stmt"""


## Basic Statements
def p_assign_stmt(p):
    """assign_stmt : assign_expr SEMI"""


def p_assign_expr(p):
    """assign_expr : id ASSIGN expr"""
    print(id_stack.pop()+" is a assign expression")


def p_read_stmt(p):
    """read_stmt : READ LPAREN id_list RPAREN SEMI"""


def p_write_stmt(p):
    """write_stmt : WRITE LPAREN id_list RPAREN SEMI"""


def p_return_stmt(p):
    """return_stmt : RETURN expr SEMI"""


## Expressions
def p_expr(p):
    """expr : expr_prefix factor"""

def p_expr_prefix(p):
    """expr_prefix : expr_prefix factor addop
    | empty"""


def p_factor(p):
    """factor : factor_prefix postfix_expr"""


def p_factor_prefix(p):
    """factor_prefix : factor_prefix postfix_expr mulop
    | empty"""


def p_postfix_expr(p):
    """postfix_expr : primary
    | call_expr"""

def p_call_expr(p):
    """call_expr : id LPAREN expr_list RPAREN"""



def p_expr_list(p):
    """expr_list : expr expr_list_tail
    | empty"""


def p_expt_list_tail(p):
    """expr_list_tail : COMMA expr expr_list_tail
    | empty"""


def p_primary(p):
    """primary : LPAREN expr RPAREN
    | id
    | INTLITERAL
    | FLOATLITERAL"""
    if(p[1] is None):
        print(id_stack.pop()+" is a primary")

# """addop : + | -"""
def p_addop(p):
    """addop : PLUS
    | MINUS"""


# """mulop :  | /"""
def p_mulop(p):
    """mulop : TIMES
    | DIVIDE"""


## Complex Statements and Condition
def p_if_stmt(p):
    """if_stmt : IF LPAREN cond RPAREN decl stmt_list else_part ENDIF"""

def p_else_part(p):
    """else_part : ELSE decl stmt_list
    | empty"""

def p_cond(p):
    """cond : expr compop expr"""


def p_compop(p):
    """compop : COMPOP"""


## While statements
def p_while_stmt(p):
    """while_stmt : WHILE LPAREN cond RPAREN decl stmt_list ENDWHILE"""

def p_empty(p):
    'empty :'


def p_error(p):
    print("Not accepted")
    global error
    error = True


parser = yacc.yacc()

result = parser.parse(data)


print(id_stack.print_items())
#symbol_table.d_print_all()




if not error:
    print("\n\nAccepted")