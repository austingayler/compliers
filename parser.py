import ply.yacc as yacc
import scanner
import symboltable
import Stack

tokens = scanner.tokens
data = scanner.data
scope_type = None
asgn_type = None

counter = 0
error = False

cur_scope = symboltable.SymbolTable("GLOBAL")
cur_scope.symbols = Stack.Stack()


def add_to_symbol(p, assigning):
    # for val in p:
    #     print(str(val).strip() + ", ", end="")
    # print()
    try:
        sym_id = p[1].strip()
        sym= symboltable.Symbol(sym_id, 42, assigning)
        cur_scope.putSymbol(sym)
    except IndexError as ie:
        print("indexError")
        print(ie)
    except AttributeError as ae:
        print("AttributeError")
        print(ae)


## PROGRAM
def p_program(p):
    'program : PROGRAM id BEGIN pgm_body END'

def p_id(p):
    'id : IDENTIFIER'
    global scope_type
    global sym_type
    # print("add_to_symbol(p, \"id\")")
    if scope_type:
        print("renaming scope \"" + cur_scope.name + "\" to", p[1])
        cur_scope.name = p[1]
        scope_type = None

def p_pgm_body(p):
    'pgm_body : decl func_declarations'

def p_decl(p):
    """decl : string_decl decl
    | var_decl decl
    | empty"""

## GLOBAL STRING DECLARATIONS
def p_string_decl(p):
    'string_decl : STRING id ASSIGN str SEMI'


def p_str(p):
    'str : STRINGLITERAL'
    # print("add_to_symbol(p, \"str\")")

## Variable Declaration
def p_var_decl(p):
    'var_decl : var_type id_list SEMI'

def p_var_type(p):
    """var_type : FLOAT
    | INT"""
    #print("add_to_symbol(p, \"var_type\")")


def p_any_type(p):
    """any_type : var_type
    | VOID"""
    global cur_scope
    global scope_type
    scope_type = "FUNC"
    # add_to_symbol(p, "any_type")
    func_sym_table = symboltable.SymbolTable("")
    cur_scope.sub_scopes.append(func_sym_table)
    func_sym_table.parent = cur_scope
    cur_scope = func_sym_table
    print("new scope \"" + func_sym_table.name + "\" which has a parent", cur_scope.getParent().name)
    #print("add_to_symbol(p, \"any_type\")")

def p_id_list(p):
    'id_list : id id_tail'

def p_id_tail(p):
    """id_tail : COMMA id id_tail
    | empty"""


## Function Paramater List
def p_param_decl_list(p):
    """param_decl_list : param_decl param_decl_tail
    | empty"""

def p_param_decl(p):
    'param_decl : var_type id'

def p_param_decl_tail(p):
    """param_decl_tail : COMMA param_decl param_decl_tail
    | empty"""

## Function Declarations
def p_func_declarations(p):
    """func_declarations : func_decl func_declarations
    | empty"""

def p_func_decl(p):
    """func_decl : FUNCTION any_type id LPAREN param_decl_list RPAREN BEGIN func_body END"""
    endScope()
    #print("add_to_symbol(p, \"function\")")

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
    endScope()

def p_else_part(p):
    """else_part : ELSE decl stmt_list
    | empty"""
    if (p[1]):
        newScope()

def p_cond(p):
    """cond : expr compop expr"""
    newScope()


def p_compop(p):
    """compop : COMPOP"""

## While statements
def p_while_stmt(p):
    """while_stmt : WHILE LPAREN cond RPAREN decl stmt_list ENDWHILE"""
    endScope()

def p_empty(p):
    'empty :'

def p_error(p):
    print("Not accepted")
    global error
    error = True

def endScope():
    global cur_scope
    if cur_scope.getParent():
        print("getting parent scope of", cur_scope.name, end=" ")
        print("which is", cur_scope.getParent().name)
        cur_scope = cur_scope.getParent()

def newScope():
    global counter
    global cur_scope
    counter += 1
    cond_sym_table = symboltable.SymbolTable("BLOCK " + str(counter))
    cur_scope.sub_scopes.append(cond_sym_table)
    cond_sym_table.parent = cur_scope
    cur_scope = cond_sym_table
    print("new scope", cond_sym_table.name, "which has a parent", cur_scope.getParent().name)

parser = yacc.yacc()

result = parser.parse(data)

endScope()
print()
cur_scope.print_scope_stack(cur_scope)

if not error:
    print("Accepted")
