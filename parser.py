import ply.yacc as yacc
import scanner
import symboltable
import Stack

tokens = scanner.tokens
data = scanner.data

counter = 0
error = False

debug = False

global_scope = symboltable.SymbolTable("GLOBAL")
print("Symbol table", global_scope.name)

scope_stack = Stack.Stack()
scope_stack.push(global_scope)

id_stack = Stack.Stack()
cur_sym_type = None
id_list_symbols = []
list_var_decl = False

## PROGRAM
def p_program(p):
    'program : PROGRAM id BEGIN pgm_body END'
    end_scope()

def p_id(p):
    'id : IDENTIFIER'
    if scope_stack.peek().name == "FUNC":
        cur_scope = scope_stack.pop()
        if debug is True:
            print("renaming scope \"" + cur_scope.name + "\" to", p[1])
        cur_scope.name = p[1].strip()
        scope_stack.push(cur_scope)
        print("\nSymbol table", cur_scope.name)

    else:
        id_stack.push(p[1].strip())

def p_pgm_body(p):
    'pgm_body : decl func_declarations'

def p_decl(p):
    """decl : string_decl decl
    | var_decl decl
    | empty"""
    if len(p) == 2:
        global list_var_decl
        list_var_decl = False

## GLOBAL STRING DECLARATIONS
def p_string_decl(p):
    'string_decl : STRING id ASSIGN str SEMI'

def p_str(p):
    'str : STRINGLITERAL'
    sym = symboltable.Symbol(id_stack.pop(), p[1].strip(), "STRING")
    scope_stack.peek().add_symbol(sym)

## Variable Declaration
def p_var_decl(p):
    'var_decl : var_type id_list SEMI'
    global cur_sym_type
    cur_sym_type = None

def p_var_type(p):
    """var_type : FLOAT
    | INT"""
    global cur_sym_type
    cur_sym_type = p[1].strip()

def p_any_type(p):
    """any_type : var_type
    | VOID"""
    new_func_scope()

def p_id_list(p):
    'id_list : id id_tail'
    global cur_sym_type
    global id_list_symbols
    if list_var_decl is True:
        for id_ in reversed(id_list_symbols):
            sym = symboltable.Symbol(id_, None, cur_sym_type)
            scope_stack.peek().add_symbol(sym)
        id_list_symbols = []


def p_id_tail(p):
    """id_tail : COMMA id id_tail
    | empty"""
    if list_var_decl is True:
        global id_list_symbols
        id_list_symbols.append(id_stack.pop())

## Function Paramater List
def p_param_decl_list(p):
    """param_decl_list : param_decl param_decl_tail
    | empty"""

def p_param_decl(p):
    'param_decl : var_type id'
    global cur_sym_type
    sym = symboltable.Symbol(id_stack.pop(), None, cur_sym_type)
    scope_stack.peek().add_symbol(sym)

def p_param_decl_tail(p):
    """param_decl_tail : COMMA param_decl param_decl_tail
    | empty"""

## Function Declarations
def p_func_declarations(p):
    """func_declarations : func_decl func_declarations
    | empty"""

def p_func_decl(p):
    """func_decl : FUNCTION any_type id LPAREN param_decl_list RPAREN BEGIN func_body END"""
    end_scope()

def p_func_body(p):
    'func_body : list_var_decl_part decl stmt_list'

def p_list_var_decl_part(p):
    'list_var_decl_part : empty'
    global list_var_decl
    list_var_decl = True

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
    """if_stmt : IF LPAREN cond RPAREN decl stmt_list end_if else_part ENDIF"""

def p_else_part(p):
    """else_part : ELSE else_scope decl stmt_list
    | empty"""
    if (p[1]):
        end_scope()

def p_cond(p):
    """cond : expr compop expr"""
    new_cond_scope()

def p_compop(p):
    """compop : COMPOP"""

## While statements
def p_while_stmt(p):
    """while_stmt : WHILE LPAREN cond RPAREN decl stmt_list ENDWHILE"""
    end_scope()

def p_empty(p):
    'empty :'

## Scoping
def p_else_scope(p):
    """else_scope : empty"""
    new_cond_scope()

def p_end_if(p):
    """end_if : empty"""
    end_scope()

def p_error(p):
    print("Not accepted")
    global error
    error = True

def new_cond_scope():
    global counter
    cond_sym_table = symboltable.SymbolTable("")
    counter += 1
    cond_sym_table.name = "BLOCK " + str(counter)
    if debug is True:
        print("new scope", cond_sym_table.name, "which has a parent", scope_stack.peek().name)
    scope_stack.push(cond_sym_table)

    print("\nSymbol table", cond_sym_table.name)

def new_func_scope():
    func_sym_table = symboltable.SymbolTable("FUNC")
    if debug is True:
        print("new scope", func_sym_table.name, "which has a parent", scope_stack.peek().name)
    scope_stack.push(func_sym_table)



def end_scope():
    if not scope_stack.is_empty():
        cur_scope = scope_stack.pop()
        if debug is True:
            print("getting parent scope of", cur_scope.name, " ")
            print("which is", scope_stack.peek().name)
    else:
        print("Stack is empty")

parser = yacc.yacc()

result = parser.parse(data)

#symbol_table = scope_stack.peek().get_root_table()

# print("\nScope structure:")
# symbol_table.recursive_print_scopes(symbol_table, 0)

# print("\nComplete symbol table:")
# symbol_table.recursive_print_all_subtables(symbol_table, 0)

#if not error:
    #print("Accepted")
