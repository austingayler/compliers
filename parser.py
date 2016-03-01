import ply.yacc as yacc
import scanner


tokens = scanner.tokens
data = scanner.data

error = False

## PROGRAM
def p_program(p):
    'program : PROGRAM id BEGIN pgm_body END'
    pass

def p_id(p):
    'id : IDENTIFIER'
    pass

def p_pgm_body(p):
    'pgm_body : decl func_declarations'
    pass

def p_decl(p):
    """decl : string_decl decl
    | var_decl decl
    | empty"""
    pass

## GLOBAL STRING DECLARATIONS
def p_string_decl(p):
    'string_decl : STRING id ASSIGN str SEMI'
    pass

def p_str(p):
    'str : STRINGLITERAL'
    pass

## Variable Declaration
def p_var_decl(p):
    'var_decl : var_type id_list SEMI'
    pass

def p_var_type(p):
    """var_type : FLOAT
    | INT"""
    pass

def p_any_type(p):
    """any_type : var_type
    | VOID"""
    pass

def p_id_list(p):
    'id_list : id id_tail'
    pass

def p_id_tail(p):
    """id_tail : COMMA id id_tail
    | empty"""
    pass

## Function Paramater List
def p_param_decl_list(p):
    """param_decl_list : param_decl param_decl_tail
    | empty"""
    pass

def p_param_decl(p):
    'param_decl : var_type id'
    pass

def p_param_decl_tail(p):
    """param_decl_tail : COMMA param_decl param_decl_tail
    | empty"""
    pass

## Function Declarations
def p_func_declarations(p):
    """func_declarations : func_decl func_declarations
    | empty"""
    pass

def p_func_decl(p):
    """func_decl : FUNCTION any_type id LPAREN param_decl_list RPAREN BEGIN func_body END"""
    pass

def p_func_body(p):
    'func_body : decl stmt_list'
    pass

## Statement List
def p_stmt_list(p):
    """stmt_list : stmt stmt_list
    | empty"""
    pass

def p_stmt(p):
    """stmt : base_stmt
    | if_stmt
    | while_stmt"""
    pass

def p_base_stmt(p):
    """base_stmt : assign_stmt
    | read_stmt
    | write_stmt
    | return_stmt"""
    pass

## Basic Statements
def p_assign_stmt(p):
    """assign_stmt : assign_expr SEMI"""
    pass

def p_assign_expr(p):
    """assign_expr : id ASSIGN expr"""
    pass

def p_read_stmt(p):
    """read_stmt : READ LPAREN id_list RPAREN SEMI"""
    pass

def p_write_stmt(p):
    """write_stmt : WRITE LPAREN id_list RPAREN SEMI"""
    pass

def p_return_stmt(p):
    """return_stmt : RETURN expr SEMI"""
    pass

## Expressions
def p_expr(p):
    """expr : expr_prefix factor"""
    pass

def p_expr_prefix(p):
    """expr_prefix : expr_prefix factor addop
    | empty"""
    pass

def p_factor(p):
    """factor : factor_prefix postfix_expr"""
    pass

def p_factor_prefix(p):
    """factor_prefix : factor_prefix postfix_expr mulop
    | empty"""
    pass

def p_postfix_expr(p):
    """postfix_expr : primary
    | call_expr"""
    pass

def p_call_expr(p):
    """call_expr : id LPAREN expr_list RPAREN"""
    pass

def p_expr_list(p):
    """expr_list : expr expr_list_tail
    | empty"""
    pass

def p_expt_list_tail(p):
    """expr_list_tail : COMMA expr expr_list_tail
    | empty"""
    pass

def p_primary(p):
    """primary : LPAREN expr RPAREN
    | id
    | INTLITERAL
    | FLOATLITERAL"""
    pass

# """addop : + | -"""
def p_addop(p):
    """addop : PLUS
    | MINUS"""
    pass

# """mulop :  | /"""
def p_mulop(p):
    """mulop : TIMES
    | DIVIDE"""
    pass

## Complex Statements and Condition
def p_if_stmt(p):
    """if_stmt : IF LPAREN cond RPAREN decl stmt_list else_part ENDIF"""
    pass

def p_else_part(p):
    """else_part : ELSE decl stmt_list
    | empty"""
    pass

def p_cond(p):
    """cond : expr compop expr"""
    pass

def p_compop(p):
    """compop : COMPOP"""
    pass

## While statements
def p_while_stmt(p):
    """while_stmt : WHILE LPAREN cond RPAREN decl stmt_list ENDWHILE"""
    pass

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print("Not accepted")
    global error
    error = True

parser = yacc.yacc()

result = parser.parse(data)

if not error:
    print("Accepted")
