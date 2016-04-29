import Stack


class Symbol:
    def __init__(self, name, value, type):
        self.name = name
        self.value = value
        self.type = type


class SymbolTable(object):
    # each symbol table has a list of symbols it contains and a list of sub symbol tables (scopes)
    def __init__(self, name):
        self.name = name
        self.symbols = Stack.Stack()

    def add_symbol(self, symbol):
        # output = ("name \"" + symbol.name + "\"").ljust(20) + (" type " + str(symbol.type)).ljust(20) #nice formatting
        output = "name " + symbol.name + " type " + str(symbol.type)
        if symbol.value is not None:
            output = output + " value " + str(symbol.value)

        duplicate_exists = self.check_duplicate(symbol)
        if duplicate_exists:
            quit()
        else:
            print(output)
            self.symbols.push(symbol)

    def check_duplicate(self, symbol):
        for sym in self.symbols.items:
            if symbol.name == sym.name:
                print("DECLARATION ERROR", symbol.name)
                return True
        return False

    def search_symbol_table(self,looking_for):
        return self.symbols.search_stack(looking_for)
    def print_symbol_table(self):
        self.symbols.print_stack()
class IRNode:
    def __init__(self, op_code, op1, op2, result):
        self.op_code = op_code
        self.op1 = op1
        self.op2 = op2
        self.result = result


class LittleNode:
    def __init__(self, op_code, op1="", op2=""):
        self.op_code = op_code
        self.op1 = op1
        self.op2 = op2

class AlgebreicNode:
    def __init__(self,value,l_child=None,r_child=None):
        self.value = value
        self.l_child = l_child
        self.r_child = r_child
    def pre_order(self):
        if self.l_child is not None:
            self.l_child.pre_order()
        if isinstance(self.value,AlgebreicNode):
            self.value.pre_order()
        else:
            print(self.value)
        if self.r_child is not None:
            self.r_child.pre_order()