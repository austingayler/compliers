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
        self.debug = 4

    def add_symbol(self, symbol):
        # output = ("name \"" + symbol.name + "\"").ljust(20) + (" type " + str(symbol.type)).ljust(20) #nice formatting
        output = "name " + symbol.name + " type " + str(symbol.type)
        if symbol.value is not None:
            output = output + " value " + str(symbol.value)

        duplicate_exists = self.check_duplicate(symbol)
        if duplicate_exists:
            quit()
        else:
            if self.debug is 3:
                print(output)
            self.symbols.push(symbol)

    def check_duplicate(self, symbol):
        for sym in self.symbols.items:
            if symbol.name == sym.name:
                print("DECLARATION ERROR", symbol.name)
                return True
        return False
        
    def get_last_symbol(self):
        if(self.symbols.size()):
            return self.symbols.peek().value
        else:
            return ""


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
