class Symbol:
    def __init__(self, name, type):
        self.name = name
        self.type = type

class SymbolTable(object):

    def __init__(self, parent, name): # parent scope and symbol table name
        self.symbols = {}
        self.name = name
        self.parent = parent

    def put(self, symbol): # put variable symbol or fundef under <name> entry
        if self.symbols.__contains__(symbol.name):
            return False
        else:
            self.symbols[symbol.name]= symbol
            return True

    def get(self, name): # get variable symbol or fundef from <name> entry
        if self.symbols.__contains__(name):
            return self.symbols[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            return None


    def getParentScope(self):
        return self.parent


class IRNode:

    def __init__(self, op_code, op1, op2, result):
        self.op_code = op_code
        self.op1 = op1
        self.op2 = op2
        self.result = result

class LittleNode:

    def __init__(self, op_code, op1 = "", op2 = ""):
        self.op_code = op_code
        self.op1 = op1
        self.op2 = op2