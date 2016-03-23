from pprint import pprint

class Symbol:
    def __init__(self, name, value, type):
        self.name = name
        self.value = value
        self.type = type

class SymbolTable(object):

    def __init__(self, parent, scope_name): # parent scope and symbol table name
        self.symbols = {}
        self.scope_name = scope_name
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

    def printSymbols(self):
        for key in self.symbols:
            sym = self.get(key)
            output = "name " + sym.name + " type " + str(sym.type)
            if sym.value is not None:
                output = output + " value " + str(sym.value)
            print(output)


symbolTable = SymbolTable(None, "GLOBAL")
scopeStack = ["GLOBAL"]
