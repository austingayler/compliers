from pprint import pprint

class Symbol:
    def __init__(self, name, value, type):
        self.name = name
        self.value = value
        self.type = type

class SymbolTable(object):

    #each symbol table has a list of symbols it contains and a list of sub symbol tables (scopes)
    def __init__(self, scope_name):
        self.symbols = {}
        self.scope_name = scope_name
        self.subScopes = {}
        self.parent = None #this might be useful to have? Idk

    def putSymbol(self, symbol): # put variable symbol or fundef under <name> entry
        if self.symbols.__contains__(symbol.name):
            return False
        else:
            self.symbols[symbol.name]= symbol
            return True

    def getSymbol(self, name): # get variable symbol or function name from name var
        if self.symbols.__contains__(name):
            return self.symbols[name]
        elif self.parent:
            return self.parent.getSymbol(name)
        else:
            return None

    def getParentScope(self):
        return self.parent

    def printSymbols(self):
        for key in self.symbols:
            sym = self.getSymbol(key)
            output = "name " + sym.name + " type " + str(sym.type)
            if sym.value is not None:
                output = output + " value " + str(sym.value)
            print(output)


symbolTable = SymbolTable("GLOBAL")
scopeStack = ["GLOBAL"]
