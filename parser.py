import ply.yacc as yacc
import scanner

tokens = scanner.tokens
data = scanner.data

error = False

## PROGRAM
def p_program(p):
    'program : PROGRAM id BEGIN pgm_body END'
    print("program:", list(p))

def p_id(p):
    'id : IDENTIFIER'
    print("id", list(p))

def p_pgm_body(p):
    'pgm_body : decl func_declarations'
    print("pgm_body", list(p))

def p_decl(p):
    """decl : string_decl decl
    | var_decl decl
    | empty"""
    print("decl", list(p))

## GLOBAL STRING DECLARATIONS
def p_string_decl(p):
    'string_decl : STRING id ASSIGN str SEMI'
    print("string_decl", list(p))

def p_str(p):
    'str : STRINGLITERAL'
    print("str", list(p))

## Variable Declaration
def p_var_decl(p):
    'var_decl : var_type id_list SEMI'
    print("var_decl", list(p))

def p_var_type(p):
    """var_type : FLOAT
    | INT"""
    print("var_type", list(p))

def p_any_type(p):
    """any_type : var_type
    | VOID"""
    print("any_type", list(p))

def p_id_list(p):
    'id_list : id id_tail'
    print("id_list", list(p))

def p_id_tail(p):
    """id_tail : COMMA id id_tail
    | empty"""
    print("id_tail", list(p))

## Function Paramater List
def p_param_decl_list(p):
    """param_decl_list : param_decl param_decl_tail
    | empty"""
    print("param_decl_list", list(p))

def p_param_decl(p):
    'param_decl : var_type id'
    print("param_decl", list(p))

def p_param_decl_tail(p):
    """param_decl_tail : COMMA param_decl param_decl_tail
    | empty"""
    print("param_decl_tail", list(p))

## Function Declarations
def p_func_declarations(p):
    """func_declarations : func_decl func_declarations
    | empty"""
    print("func_declarations", list(p))

def p_func_decl(p):
    """func_decl : FUNCTION any_type id LPAREN param_decl_list RPAREN BEGIN func_body END"""
    print("func_decl", list(p))

def p_func_body(p):
    'func_body : decl stmt_list'
    print("func_body", list(p))

## Statement List
def p_stmt_list(p):
    """stmt_list : stmt stmt_list
    | empty"""
    print("stmt_list", list(p))

def p_stmt(p):
    """stmt : base_stmt
    | if_stmt
    | while_stmt"""
    print("stmt", list(p))

def p_base_stmt(p):
    """base_stmt : assign_stmt
    | read_stmt
    | write_stmt
    | return_stmt"""
    print("base_stmt", list(p))

## Basic Statements
def p_assign_stmt(p):
    """assign_stmt : assign_expr SEMI"""
    print("assign_stmt", list(p))

def p_assign_expr(p):
    """assign_expr : id ASSIGN expr"""
    print("assign_expr", list(p))


def p_read_stmt(p):
    """read_stmt : READ LPAREN id_list RPAREN SEMI"""
    print("read_stmt", list(p))

def p_write_stmt(p):
    """write_stmt : WRITE LPAREN id_list RPAREN SEMI"""
    print("write_stmt", list(p))

def p_return_stmt(p):
    """return_stmt : RETURN expr SEMI"""
    print("return_stmt", list(p))

## Expressions
def p_expr(p):
    """expr : expr_prefix factor"""
    print("expr", list(p))

def p_expr_prefix(p):
    """expr_prefix : expr_prefix factor addop
    | empty"""
    print("expr_prefix", list(p))

def p_factor(p):
    """factor : factor_prefix postfix_expr"""
    print("factor", list(p))

def p_factor_prefix(p):
    """factor_prefix : factor_prefix postfix_expr mulop
    | empty"""
    print("factor_prefix", list(p))


def p_postfix_expr(p):
    """postfix_expr : primary
    | call_expr"""
    print("postfix_expr", list(p))

def p_call_expr(p):
    """call_expr : id LPAREN expr_list RPAREN"""
    print("call_expr", list(p))

def p_expr_list(p):
    """expr_list : expr expr_list_tail
    | empty"""
    print("expr_list", list(p))

def p_expt_list_tail(p):
    """expr_list_tail : COMMA expr expr_list_tail
    | empty"""
    print("expr_list_tail", list(p))

def p_primary(p):
    """primary : LPAREN expr RPAREN
    | id
    | INTLITERAL
    | FLOATLITERAL"""
    print("primary", list(p))

# """addop : + | -"""
def p_addop(p):
    """addop : PLUS
    | MINUS"""
    print("addop", list(p))

# """mulop :  | /"""
def p_mulop(p):
    """mulop : TIMES
    | DIVIDE"""
    print("mulop", list(p))

## Complex Statements and Condition
def p_if_stmt(p):
    """if_stmt : IF LPAREN cond RPAREN decl stmt_list else_part ENDIF"""
    print("if_stmt", list(p))

def p_else_part(p):
    """else_part : ELSE decl stmt_list
    | empty"""
    print("else_part", list(p))

def p_cond(p):
    """cond : expr compop expr"""
    print("cond", list(p))

def p_compop(p):
    """compop : COMPOP"""
    print("compop", list(p))

## While statements
def p_while_stmt(p):
    """while_stmt : WHILE LPAREN cond RPAREN decl stmt_list ENDWHILE"""
    print("while_stmt", list(p))

def p_empty(p):
    'empty :'
    print("empty", list(p))

def p_error(p):
    print("Not accepted")
    global error
    error = True

parser = yacc.yacc()

result = parser.parse(data)

if not error:
    print("Accepted")
