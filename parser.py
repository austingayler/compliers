import Stack
import ply.yacc as yacc
import scanner
import Node
import ir_to_tiny

tokens = scanner.tokens
data = scanner.data

counter = 0
error = False
register_count = 1

debug = 4 #None, 3, 4

global_scope = Node.SymbolTable("GLOBAL")
if debug is 3:
    print("Symbol table", global_scope.name)

scope_stack = Stack.Stack()
scope_stack.push(global_scope)

id_stack = Stack.Stack()
cur_sym_type = None
id_list_symbols = []
list_var_decl = False
label_stack = Stack.Stack()
label_count = 0
output_IR_code = []
cur_reg = 0

## PROGRAM
def p_program(p):
    'program : PROGRAM id BEGIN pgm_body END'
    #end_scope()

def p_id(p):
    'id : IDENTIFIER'

    # print("Encountered ", p[1].strip(), "Scope stax name =", scope_stack.peek().name)

    p[0] = p[1]
    
    id = p[1].strip()
    
    if scope_stack.peek().name == "FUNC":
        cur_scope = scope_stack.pop()
        if debug is 3:
            print("renaming scope \"" + cur_scope.name + "\" to", id)
        cur_scope.name = id
        scope_stack.push(cur_scope)
        if debug is 3:
            print("\nSymbol table", cur_scope.name)
        
    else:
        id_stack.push(p[1].strip())

def p_pgm_body(p):
    'pgm_body : pgm_body_var_decl_aux decl func_declarations'

def p_pgm_body_var_decl_aux(p):
    'pgm_body_var_decl_aux : empty'
    global list_var_decl
    list_var_decl = True

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
    sym = Node.Symbol(id_stack.pop(), p[1].strip(), "STRING")
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
    if list_var_decl:
        for id_ in reversed(id_list_symbols):
            sym = Node.Symbol(id_, None, cur_sym_type)
            scope_stack.peek().add_symbol(sym)
        id_list_symbols = []

def p_id_tail(p):
    """id_tail : COMMA id id_tail
    | empty"""
    if list_var_decl:
        global id_list_symbols
        id_list_symbols.append(id_stack.pop())

## Function Paramater List
def p_param_decl_list(p):
    """param_decl_list : param_decl param_decl_tail
    | empty"""

def p_param_decl(p):
    'param_decl : var_type id'
    global cur_sym_type
    sym = Node.Symbol(id_stack.pop(), None, cur_sym_type)
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
    global output_IR_code
    temp_IR_code = generate_assign_expr_IR_code(p[1],p[3])
    for item in temp_IR_code:
        output_IR_code.append(item)

def p_read_stmt(p):
    """read_stmt : READ LPAREN id_list RPAREN SEMI"""
    
def p_write_stmt(p):
    """write_stmt : WRITE LPAREN id_list RPAREN SEMI"""

def p_return_stmt(p):
    """return_stmt : RETURN expr SEMI"""

## Expressions
def p_expr(p):
    """expr : expr_prefix factor"""

    if p[1] and p[2]:
        p[0] = p[1]+p[2]
    elif p[1]:
        p[0] = p[1]
    elif p[2]:
        p[0] = p[2]
    
def p_expr_prefix(p):
    """expr_prefix : expr_prefix factor addop
    | empty"""
    if len(p)>2:
        if p[1]:
            p[0] = p[1]+p[2]+p[3]
        else:
            p[0] = p[2]+p[3]    

def p_factor(p):
    """factor : factor_prefix postfix_expr"""
    if p[1] and p[2]:
        p[0] = p[1]+p[2]
    elif p[1]:
        p[0] = p[1]
    elif p[2]:
        p[0] = p[2]

def p_factor_prefix(p):
    """factor_prefix : factor_prefix postfix_expr mulop
    | empty"""
    if len(p)>2:
        if p[1]:
            p[0] = p[1]+p[2]+p[3]
        else:
            p[0] = p[2]+p[3]

def p_postfix_expr(p):
    """postfix_expr : primary
    | call_expr"""
    if p[1] is None:
        pass
        #p[0] = None
    else:
        p[0] = p[1]
        
    # dylan's code says only
    # p[0] = p[1] for p_postfix_expr
    # I think this is wrong though, since we only have 1 function?

def p_call_expr(p):
    """call_expr : id LPAREN expr_list RPAREN"""
    p[0] = p[1]+["("]+p[2]+[")"] #dylan
    p[0] = None #aj

def p_expr_list(p):
    """expr_list : expr expr_list_tail
    | empty"""
    if p[1]:
        p[0] = p[1]+p[2]

def p_expr_list_tail(p):
    """expr_list_tail : COMMA expr expr_list_tail
    | empty"""
    if p[1]:
        p[0] = p[1]+p[2]

def p_primary(p):
    """primary : LPAREN expr RPAREN
    | id
    | INTLITERAL
    | FLOATLITERAL"""

    if len(p)<3:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]]+p[2]+[p[3]]

def p_addop(p):
    """addop : PLUS
    | MINUS"""

    p[0] = [p[1]]
    
def p_mulop(p):
    """mulop : TIMES
    | DIVIDE"""

    p[0] = [p[1]]
    
## Complex Statements and Condition
def p_if_stmt(p):
    """if_stmt : IF LPAREN cond RPAREN pgm_body_var_decl_aux decl stmt_list end_if else_part ENDIF"""
    global label_stack
    global output_IR_code
    endif = label_stack.pop()
    lbl = "LABEL label" + str(endif)
    #print(lbl)
    output_IR_code.append(lbl)

def p_write_jump(p):
    """write_jump : empty"""
    global label_count
    global label_stack
    global output_IR_code
    label_count += 1 
    
    label_stack.push(label_count)
    jump = "JUMP label" + str(label_stack.pop())
    else_ = "LABEL label" + str(label_stack.pop())

    label_stack.push(label_count)
    #print(jump)
    output_IR_code.append(jump)
    #print(else_)
    output_IR_code.append(else_)
    
def p_else_part(p):
    """else_part : write_jump ELSE pgm_body_var_decl_aux else_scope decl stmt_list
    | empty"""
    if (p[1]): #if ELSE part
        end_scope()
        
    #else:
     #   global label_stack
      #  endif = label_stack.pop()
       # 
        #print(";LABEL label" + str(endif))
    
def p_cond(p):
    """cond : expr compop expr"""
    global label_count
    global label_stack
    global output_IR_code

    temp_IR_code,expr1,expr2,op_type = generate_cond_IR_code(p[1],p[2],p[3])
    if op_type == "INT":
        op_type = "I"
    else:
        op_type = "F"
    for item in temp_IR_code:
        output_IR_code.append(str(item))

    new_cond_scope()
    label_count += 1 
    label_stack.push(label_count)
    end_ctrl = "label" + str(label_count)
    
    op = str(p[2].strip())

    out = ""
    if op == ">=":
        out = "LT"+op_type+" " + expr1 + " " + expr2 + " " +  end_ctrl
    elif op == "<=":
        out = "GT"+op_type+" " + expr1 + " " +  expr2 + " " +  end_ctrl
    elif op == "!=":
        out = "EQ"+op_type+" " + expr1 + " " +  expr2 + " " +  end_ctrl
    elif op == "<":
        out = "GE"+op_type+" " + expr1 + " " +  expr2 + " " +  end_ctrl
    elif op == ">":
        out = "LE"+op_type+" " + expr1 + " " +  expr2 + " " +  end_ctrl
    elif op == "=":
        out = "NE"+op_type+" " + expr1 + " " +  expr2 + " " +  end_ctrl
    
    #print(out)
    output_IR_code.append(out)
    #print()
    
def p_compop(p):
    """compop : COMPOP"""
    p[0] = p[1]

def p_insert_label(p): #cuz idk how to tell if we got to cond from while or if
    """insert_label : empty"""
    global label_stack
    global label_count
    global output_IR_code
    
    label_count += 1
    label_stack.push(label_count)
    
    out = "LABEL label" + str(label_count)
    #print(out)
    output_IR_code.append(out)
    
## While statements
def p_while_stmt(p):
    """while_stmt : WHILE insert_label LPAREN cond RPAREN pgm_body_var_decl_aux decl stmt_list ENDWHILE"""
    global output_IR_code
    end_scope()
    endwhile = label_stack.pop()
    jump_stmt = label_stack.pop()
    
    jmp = "JUMP label" + str(jump_stmt)
    lbl = "LABEL label" + str(endwhile)
    
    #print(jmp)
    output_IR_code.append(jmp)
    #print(lbl)
    output_IR_code.append(lbl)
    
def p_empty(p):
    'empty :'
    p[0] = None

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
    cond_sym_table = Node.SymbolTable("")
    counter += 1
    cond_sym_table.name = "BLOCK " + str(counter)
    if debug is 3:
        print("new scope", cond_sym_table.name, "which has a parent", scope_stack.peek().name)
    scope_stack.push(cond_sym_table)

    if debug is 3:
        print("\nSymbol table", cond_sym_table.name)

def new_func_scope():
    func_sym_table = Node.SymbolTable("FUNC")
    if debug is 3:
        print("new scope", func_sym_table.name, "which has a parent", scope_stack.peek().name)
    scope_stack.push(func_sym_table)

def end_scope():
    if not scope_stack.is_empty():
        cur_scope = scope_stack.pop()
        if debug is 3:
            print("getting parent scope of", cur_scope.name, " ")
            print("which is", scope_stack.peek().name)
    else:
        print("Stack is empty")

def generate_cond_IR_code(expr1,compop,expr2):
    input_list1 = convert_to_postfix(expr1)
    input_list2 = convert_to_postfix(expr2)
    return_string = []
    index = 0
    got_in = False
    while len(input_list1)>1:
        if input_list1[index] in["+","-","*","/"]:
            got_in = True
            reg1 = get_next_reg()
            reg2 = get_next_reg()
            op_type = scope_stack.search_stack(input_list1[index-2].strip())
            if op_type == "INT":
                op_type = "I"
            else:
                op_type = "F"
            return_string.append("STORE"+op_type+" "+input_list1[index-2]+" $T"+str(reg1))
            return_string.append("STORE"+op_type+" "+input_list1[index-1]+" $T"+str(reg2))
            the_reg = get_next_reg()
            if input_list1[index] == "+":
                return_string.append("ADD"+op_type+" "+" $T"+str(reg1)+" $T"+str(reg2)+" "+"$T"+str(the_reg))
            elif input_list1[index] == "-":
                return_string.append("SUB"+op_type+" "+" $T"+str(reg1)+" $T"+str(reg2)+" "+"$T"+str(the_reg))
            elif input_list1[index] == "*":
                return_string.append("MUL"+op_type+" "+" $T"+str(reg1)+" $T"+str(reg2)+" "+"$T"+str(the_reg))
            elif input_list1[index] == "/":
                return_string.append("DIV"+op_type+" "+" $T"+str(reg1)+" $T"+str(reg2)+" "+"$T"+str(the_reg))

            input_list1.pop(index-2)
            input_list1.pop(index-2)
            input_list1.pop(index-2)
            input_list1.insert(index-2,"$T"+str(the_reg))
            index = index-2
        index = index+1
    
    # used to be important_reg1 = the_reg 
    important_reg1 = get_next_reg() # changed to this dylan
    #THIS MIGHT BE BAD. doesn't work with test_adv
    
    if not got_in:
        op_type = scope_stack.search_stack(input_list1[0].strip())
        the_reg = get_next_reg()
        important_reg1 = the_reg
        if op_type == "INT":
            return_string.append("STOREI "+input_list1[0]+" $T"+str(the_reg))
        else:
            return_string.append("STOREF "+input_list1[0]+" $T"+str(the_reg))

    index = 0
    got_in = False
    while len(input_list2)>1:
        if input_list2[index] in["+","-","*","/"]:
            got_in = True
            reg1 = get_next_reg()
            reg2 = get_next_reg()
            op_type = scope_stack.search_stack(input_list2[index-2].strip())
            if op_type == "INT":
                op_type = "I"
            else:
                op_type = "F"
            return_string.append("STORE"+op_type+" "+input_list2[index-2]+" $T"+str(reg1))
            return_string.append("STORE"+op_type+" "+input_list2[index-1]+" $T"+str(reg2))
            the_reg = get_next_reg()
            if input_list2[index] == "+":
                return_string.append("ADD"+op_type+" "+" $T"+str(reg1)+" $T"+str(reg2)+" "+"$T"+str(the_reg))
            elif input_list2[index] == "-":
                return_string.append("SUB"+op_type+" "+" $T"+str(reg1)+" $T"+str(reg2)+" "+"$T"+str(the_reg))
            elif input_list2[index] == "*":
                return_string.append("MUL"+op_type+" "+" $T"+str(reg1)+" $T"+str(reg2)+" "+"$T"+str(the_reg))
            elif input_list2[index] == "/":
                return_string.append("DIV"+op_type+" "+" $T"+str(reg1)+" $T"+str(reg2)+" "+"$T"+str(the_reg))

            input_list2.pop(index-2)
            input_list2.pop(index-2)
            input_list2.pop(index-2)
            input_list2.insert(index-2,"$T"+str(the_reg))
            index = index-2
        index = index+1
    important_reg2 = the_reg
    if not got_in:
        op_type = scope_stack.search_stack(input_list1[0].strip())
        the_reg = get_next_reg()
        important_reg2 = the_reg
        if op_type == "INT":
            return_string.append("STOREI "+input_list2[0]+" $T"+str(the_reg))
        else:
            return_string.append("STOREF "+input_list2[0]+" $T"+str(the_reg))

    return return_string,"$T"+str(important_reg1),"$T"+str(important_reg2),op_type

def generate_assign_expr_IR_code(in_id, expr):
    input_list = convert_to_postfix(expr)
    return_string = []
    index = 0
    got_in = False
    while len(input_list)>1:
        if input_list[index] in["+","-","*","/"]:
            got_in = True
            reg1 = get_next_reg()
            reg2 = get_next_reg()
            op_type = scope_stack.search_stack(input_list[index-2].strip())
            if op_type == "INT":
                op_type = "I"
            else:
                op_type = "F"
            return_string.append("STORE"+op_type+" "+input_list[index-2]+" $T"+str(reg1))
            return_string.append("STORE"+op_type+" "+input_list[index-1]+" $T"+str(reg2))
            the_reg = get_next_reg()
            if input_list[index] == "+":
                return_string.append("ADD"+op_type+" "+" $T"+str(reg1)+" $T"+str(reg2)+" "+"$T"+str(the_reg))
            elif input_list[index] == "-":
                return_string.append("SUB"+op_type+" "+" $T"+str(reg1)+" $T"+str(reg2)+" "+"$T"+str(the_reg))
            elif input_list[index] == "*":
                return_string.append("MUL"+op_type+" "+" $T"+str(reg1)+" $T"+str(reg2)+" "+"$T"+str(the_reg))
            elif input_list[index] == "/":
                return_string.append("DIV"+op_type+" "+" $T"+str(reg1)+" $T"+str(reg2)+" "+"$T"+str(the_reg))

            input_list.pop(index-2)
            input_list.pop(index-2)
            input_list.pop(index-2)
            input_list.insert(index-2,"$T"+str(the_reg))
            index = index-2
        index = index+1
    
    if not got_in:
        op_type = scope_stack.search_stack(in_id.strip())
        the_reg = get_next_reg()
        if op_type == "INT":
            return_string.append("STOREI "+input_list[0]+" $T"+str(the_reg))
            return_string.append("STOREI $T"+str(the_reg)+" "+in_id)
        else:
            return_string.append("STOREF "+input_list[0]+" $T"+str(the_reg))
            return_string.append("STOREF $T"+str(the_reg)+" "+in_id)
        return return_string

    return_string.append("STORE"+op_type+" "+" $T"+str(the_reg)+" "+in_id)
    return return_string

def convert_to_postfix(input_string):
  #  input_string = input_string.replace(" ","")
    index = 0
    stack = []
    symbol_list = []
    while index < len(input_string):
        if  (input_string[index].find("+") == -1) and \
            (input_string[index].find("-") == -1) and \
            (input_string[index].find("*") == -1) and \
            (input_string[index].find("/") == -1) and \
            (input_string[index].find("(") == -1) and \
            (input_string[index].find(")") == -1):
            symbol_list.append(input_string[index])
        else:
            if len(stack) == 0 or stack[0] == "(" or input_string[index] == "(":
                stack.insert(0,input_string[index])
            elif input_string[index] == ")":
                while stack[0] != "(":
                    symbol_list.append(stack[0])
                    stack.pop(0)
                stack.pop(0) 
            elif input_string[index] in ["*","/"] and stack[0] in ["+","-"]:
                stack.insert(0,input_string[index])
            elif input_string[index] in ["*","/"] and stack[0] in ["*","/"]:
                symbol_list.append(stack[0])
                stack.pop(0)
                stack.insert(0,input_string[index])
            elif input_string[index] in ["+","-"] and stack[0] in ["+","-"]:
                symbol_list.append(stack[0])
                stack.pop(0)
                stack.insert(0,input_string[index])
            elif input_string[index] in ["+","-"] and stack[0] in ["*","/"]:
                symbol_list.append(stack[0])
                stack.pop(0)
                index = index -1
        index = index+1
    while len(stack) > 0:
        symbol_list.append(stack[0])
        stack.pop(0)
    return symbol_list

def get_next_reg():
    global cur_reg
    cur_reg += 1
    return cur_reg



#here starts the executing of code
parser = yacc.yacc()

result = parser.parse(data)

if False:
    print(";IR code\n")
for stmt in output_IR_code:
    #print(stmt)
    pass

tiny_code = ir_to_tiny.convert_ir_to_tiny(output_IR_code)
print(";tiny code\n")
for stmt in tiny_code:
    print(stmt)




#swag