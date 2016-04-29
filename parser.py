import Node
import Stack
import ply.yacc as yacc
import scanner
import pprint

tokens = scanner.tokens
data = scanner.data

counter = 0
error = False
step3 = False

debug = False

global_scope = Node.SymbolTable("GLOBAL")
if step3:
    print("Symbol table", global_scope.name)

scope_stack = Stack.Stack()
scope_stack.push(global_scope)

id_stack = Stack.Stack()
cur_sym_type = None
id_list_symbols = []
list_var_decl = False

var_types = {}


## PROGRAM
def p_program(p):
    'program : PROGRAM id BEGIN pgm_body END'
    p[0] = ("PROGRAM", p[1], p[2], p[3], p[4], p[5])
    end_scope()


def p_id(p):
    'id : IDENTIFIER'
    p[0] = ("IDENT", p[1])
    # print("Encountered ", p[1].strip(), "Scope stax name =", scope_stack.peek().name)

    if scope_stack.peek().name == "FUNC":
        cur_scope = scope_stack.pop()
        if debug:
            print("renaming scope \"" + cur_scope.name + "\" to", p[1])
        cur_scope.name = p[1].strip()
        scope_stack.push(cur_scope)
        print("Label", cur_scope.name)
        if step3:
            print("\nSymbol table", cur_scope.name)

    else:
        id_stack.push(p[1].strip())


def p_pgm_body(p):
    'pgm_body : pgm_body_var_decl_aux decl func_declarations'
    p[0] = ("PGRM_BODY", p[2], p[3])


def p_pgm_body_var_decl_aux(p):
    'pgm_body_var_decl_aux : empty'
    global list_var_decl
    list_var_decl = True


def p_decl(p):
    """decl : string_decl decl
    | var_decl decl
    | empty"""
    if len(p) == 3:
        p[0] = ("DECL", p[1], p[2])

    elif len(p) == 2:
        global list_var_decl
        list_var_decl = False


## GLOBAL STRING DECLARATIONS
def p_string_decl(p):
    'string_decl : STRING id ASSIGN str SEMI'
    p[0] = ("STRING_DECL", p[1], p[2], p[3], p[4], p[5])


def p_str(p):
    'str : STRINGLITERAL'
    p[0] = ("STRING", p[1])
    sym = Node.Symbol(id_stack.pop(), p[1].strip(), "STRING")
    scope_stack.peek().add_symbol(sym)


## Variable Declaration
def p_var_decl(p):
    'var_decl : var_type id_list SEMI'
    p[0] = ("VAR_DECL", p[1], p[2], p[3])
    global cur_sym_type
    cur_sym_type = None


def p_var_type(p):
    """var_type : FLOAT
    | INT"""
    p[0] = ("VAR_TYPE", p[1])
    global cur_sym_type
    cur_sym_type = p[1].strip()


def p_any_type(p):
    """any_type : var_type
    | VOID"""
    p[0] = ("ANY_TYPE", p[1])
    new_func_scope()


def p_id_list(p):
    'id_list : id id_tail'
    p[0] = ("ID_LIST", p[1], p[2])
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
    if len(p) == 4:
        p[0] = ("ID_TAIL", p[1], p[2], p[3])

    if list_var_decl:
        global id_list_symbols
        id_list_symbols.append(id_stack.pop())


## Function Paramater List
def p_param_decl_list(p):
    """param_decl_list : param_decl param_decl_tail
    | empty"""
    if len(p) == 3:
        p[0] = ("PARAM_DECL_LIST", p[1], p[2])


def p_param_decl(p):
    'param_decl : var_type id'
    p[0] = ("PARAM_DECL", p[1], p[2])
    global cur_sym_type
    sym = Node.Symbol(id_stack.pop(), None, cur_sym_type)
    scope_stack.peek().add_symbol(sym)


def p_param_decl_tail(p):
    """param_decl_tail : COMMA param_decl param_decl_tail
    | empty"""
    if len(p) == 4:
        p[0] = ("PARAM_DECL_TAIL", p[1], p[2], p[3])


## Function Declarations
def p_func_declarations(p):
    """func_declarations : func_decl func_declarations
    | empty"""
    if len(p) == 3:
        p[0] = ("FUNC_DECLARATIONS", p[1], p[2])


def p_func_decl(p):
    """func_decl : FUNCTION any_type id LPAREN param_decl_list RPAREN BEGIN func_body END"""
    p[0] = ("FUNC_DECL", p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9])
    end_scope()


def p_func_body(p):
    'func_body : list_var_decl_part decl stmt_list'
    p[0] = ("FUNC_BODY", p[2], p[3])


def p_list_var_decl_part(p):
    'list_var_decl_part : empty'
    global list_var_decl
    list_var_decl = True


## Statement List
def p_stmt_list(p):
    """stmt_list : stmt stmt_list
    | empty"""
    if len(p) == 3:
        p[0] = ("STMT_LIST", p[1], p[2])


def p_stmt(p):
    """stmt : base_stmt
    | if_stmt
    | while_stmt"""
    p[0] = ("STMT", p[1])


def p_base_stmt(p):
    """base_stmt : assign_stmt
    | read_stmt
    | write_stmt
    | return_stmt"""
    p[0] = ("BASE_STMT", p[1])


## Basic Statements
def p_assign_stmt(p):
    """assign_stmt : assign_expr SEMI"""
    p[0] = ("ASSIGN_STMT", p[1], p[2])


def p_assign_expr(p):
    """assign_expr : id ASSIGN expr"""
    # FIXME?
    p[0] = ("ASSIGN_EXPR", p[1], p[2], p[3])


def p_read_stmt(p):
    """read_stmt : READ LPAREN id_list RPAREN SEMI"""
    p[0] = ("READ_STMT", p[1], p[2], p[3], p[4], p[5])


def p_write_stmt(p):
    """write_stmt : WRITE LPAREN id_list RPAREN SEMI"""
    p[0] = ("WRITE_STMT", p[1], p[2], p[3], p[4], p[5])


def p_return_stmt(p):
    """return_stmt : RETURN expr SEMI"""
    p[0] = ("RETURN_STMT", p[1], p[2], p[3])


## Expressions
def p_expr(p):
    """expr : expr_prefix factor"""
    p[0] = ("EXPR", p[1], p[2])


def p_expr_prefix(p):
    """expr_prefix : expr_prefix factor addop
    | empty"""
    if len(p) == 4:
        p[0] = ("EXPR_PRE", p[1], p[2], p[3])


def p_factor(p):
    """factor : factor_prefix postfix_expr"""
    p[0] = ("FACTOR", p[1], p[2])


def p_factor_prefix(p):
    """factor_prefix : factor_prefix postfix_expr mulop
    | empty"""
    if len(p) == 4:
        p[0] = ("FACTOR_PREFIX", p[1], p[2], p[3])


def p_postfix_expr(p):
    """postfix_expr : primary
    | call_expr"""
    p[0] = ("POSTFIX_EPR", p[1])


def p_call_expr(p):
    """call_expr : id LPAREN expr_list RPAREN"""
    p[0] = ("CALL_EXPR", p[1], p[2], p[3], p[4])


def p_expr_list(p):
    """expr_list : expr expr_list_tail
    | empty"""
    if len(p) == 3:
        p[0] = ("EXPR_LIST", p[1], p[2])


def p_expt_list_tail(p):
    """expr_list_tail : COMMA expr expr_list_tail
    | empty"""
    if len(p) == 4:
        p[0] = ("EXPR_LIST_TAIL", p[1], p[2], p[3])


def p_primary(p):
    """primary : LPAREN expr RPAREN
    | id
    | INTLITERAL
    | FLOATLITERAL"""
    # add p[0] for value
    # This is where we get variable values.
    if len(p) == 4:
        p[0] = ("PRI", p[1], p[2], p[3])
    else:
        p[0] = ("PRI", p[1])


# """addop : + | -"""
def p_addop(p):
    """addop : PLUS
    | MINUS"""
    p[0] = ("BinOP", p[1])


# """mulop :  | /"""
def p_mulop(p):
    """mulop : TIMES
    | DIVIDE"""
    p[0] = ("BinOP", p[1])


## Complex Statements and Condition
def p_if_stmt(p):
    """if_stmt : IF LPAREN cond RPAREN pgm_body_var_decl_aux decl stmt_list end_if else_part ENDIF"""
    # FIXME removed rules not-lits going to empty
    p[0] = ("IF", p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[9], p[10])


def p_else_part(p):
    """else_part : ELSE pgm_body_var_decl_aux else_scope decl stmt_list
    | empty"""
    if len(p) == 6:
        # FIXME removed rules not-lits going to empty
        p[0] = ("ELSE", p[1], p[4], p[5])
    if (p[1]):
        end_scope()


def p_cond(p):
    """cond : expr compop expr"""
    p[0] = ("COND", p[1], p[2], p[3])
    new_cond_scope()


def p_compop(p):
    """compop : COMPOP"""
    p[0] = ("COMP_OP", p[1])


## While statements
def p_while_stmt(p):
    """while_stmt : WHILE LPAREN cond RPAREN pgm_body_var_decl_aux decl stmt_list ENDWHILE"""
    # FIXME removed rules not-lits going to empty
    p[0] = ("WHILE", p[1], p[2], p[3], p[4], p[6], p[7], p[8])
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
    cond_sym_table = Node.SymbolTable("")
    counter += 1
    cond_sym_table.name = "BLOCK " + str(counter)
    scope_stack.push(cond_sym_table)
    if debug:
        print("new scope", cond_sym_table.name, "which has a parent", scope_stack.peek().name)
    if step3:
        print("\nSymbol table", cond_sym_table.name)


def new_func_scope():
    func_sym_table = Node.SymbolTable("FUNC")
    if debug:
        print("new scope", func_sym_table.name, "which has a parent", scope_stack.peek().name)
    scope_stack.push(func_sym_table)


def end_scope():
    if not scope_stack.is_empty():
        cur_scope = scope_stack.pop()
        if debug:
            print("getting parent scope of", cur_scope.name, " ")
            print("which is", scope_stack.peek().name)
    else:
        print("Error: Stack is empty")


#def generate_ir(tree):
    # """post order traverse tree.  need a case for every type of node we want to generate IR for"""
    # print("______________________________________________________________________________")
    # for t in tree[1:]:
    #     if isinstance(t, tuple):
    #         generate_ir(t)
    #
    # if tree[0] == "EXPR":
    #     op = op_type(tree)
    #     if op == "+":
    #
    #     print("OP", op_type(tree))
    # #print(tree)
    #
    # pass

#
# def op_type(expr):
#     if expr and expr[1] and expr[1][3]:
#         return expr[1][3][1]
#
#
# def type_check(node, idt):
#     """post order traversal of the tree to find the type of a var."""
#     found = False
#     cur_type = None
#     # nested functions so there are no globals
#     def walker(nod):
#         nonlocal found
#         if found:
#             return False
#         else:
#             if nod[0]=="VAR_DECL":
#                 cur_type = nod[1][1] #should be type thing
#             if nod[0]=="IDENT" and nod[1] == idt:
#                 found = True
#             return True
#
#     temp_node = node
#     while not found:
#         for t in temp_node[1:]:
#             if isinstance(t, tuple):
#                 if not walker(t):
#                     break
#             if found:
#                 break
#
#     return cur_type
#
#



#--------------------------------------

class ASTNode():
    def __init__(self, name, stuff, children):
        self.name = name
        self.stuff = stuff
        self.children = children

    def __str__(self):
        return self.__str_helper__(0)

    def __str_helper__(self, level):
        st = ""
        st += ((level * ' ') + "Name:%s, Stuff:%s, Children:%s\n" % (self.name, self.stuff, self.children))
        for c in self.children:
            st += c.__str_helper__(level+1)
        return st

    def __repr__(self):
        return self.name

    def clean(self):
        good_children = []

        for c in self.children:
            c.clean()
            if c.name in []: #"ID_TAIL", "DECL", "POSTFIX_EPR", "BASE_STMT", "ASSIGN_STMT"
                good_children.extend(c.children)
                self.stuff.extend(c.stuff)
            else:
                if c is not None:
                    good_children.append(c)
        good_stuff = []
        for s in self.stuff:
            if s is not None:
                good_stuff.append(s.strip())

        self.children = good_children
        self.stuff = good_stuff

    def has(self, string):
        return string in str(self.children)

    def get(self, string):
        for c in self.children:
            if c.name == string:
                return c


class Context():
    def __init__(self):
        self.var_count = 0
        self.var_stack = []
        self.prog = ""

    def write(self, string):
        self.prog += string

    def macaroni(self, node): #if we create a new variable, we return its name.
        if node is None:
            return

        if node.name == "PRI":
            if len(node.children)==0:
                self.push(node.stuff[0])
            else:
                self.macaroni(node.children[0])
            return

        if node.name == "IDENT":
            self.push(node.stuff[0])
            return

        if node.name == "EXPR_PRE":

            self.macaroni(node.get("EXPR_PRE"))
            n1 = self.pop()
            self.macaroni(node.get("FACTOR"))
            n2 = self.pop()

            nw = self.nv()
            self.macaroni(node.get("BIN_OP"))
            self.write(n1 + " " + n2  + " " + nw)
            self.write("\n")
            return



        if node.name == "BIN_OP":

            marp = {
            "+":"addi",
            "-":"subi",
            "*":"muli",
            "/":"divi",
            ">=":"GEI",
            ">":"GTI",
            "<=":"LEI",
            "<":"LTI",
            "!=":"NEI",
            "=":"EQI"
            }

            self.write(marp[node.stuff[0]] +" ")
            return

        if node.name == "ASSIGN_EXPR":
            self.macaroni(node.get("EXPR"))
            self.macaroni(node.get("IDENT"))
            self.write("STOREI %s %s\n" % (self.pop(), self.pop()))
            return

        # if node.name == "WHILE":
        #     cond = node.get("COND")
        #     stmtlst = node.get("STMT_LIST")
        #     lbl = self.nv()
        #     end_lbl = self.nv()

        #     self.macaroni(cond)
        #     boo = self.pop()
        #     self.write("EQ " + boo + " 1 " + end_lbl +"\n")
        #     self.write("\n"+lbl + ":\n")
        #     self.macaroni(stmtlst)
        #     self.macaroni(cond)
        #     boo = self.pop()
        #     self.write("EQ " + boo + " 1 " + lbl +"\n")

        #     self.write("\n"+ end_lbl + ":\n")


        # if node.name == "COND":
        #     for c in node.children:
        #         self.macaroni(c)
        #     return

        if node.name == "IF":
            pass


        for c in node.children:
            self.macaroni(c)


    def push(self, var_name):
        self.var_stack.append(var_name)

    def pop(self):
        v = self.var_stack[-1]
        self.var_stack = self.var_stack[:-1]
        return v

    def nv(self):
        n = self.var_count
        self.var_count+=1
        self.var_stack.append("t"+str(n))
        return "t"+str(n)

def unwrap(tup):
    name = tup[0]
    stuff = []
    children = []
    for t in tup[1:]:
        if isinstance(t, tuple):
            children.append(unwrap(t))
        else:
            stuff.append(t)

    nod = ASTNode(name, stuff, children)
    for c in children:
        c.parent = nod
    return nod




parser = yacc.yacc()

pp = pprint.PrettyPrinter(indent=4)
result = parser.parse(data)
pp.pprint(result)

asTree = unwrap(result)

asTree.clean()
ctx = Context()
prog = ctx.macaroni(asTree)
print(ctx.prog)
print(asTree)

#--------------------------------------
