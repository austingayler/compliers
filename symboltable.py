class Symbol:
    def __init__(self, name, value, type):
        self.name = name
        self.value = value
        self.type = type


class SymbolTable(object):
    # each symbol table has a list of symbols it contains and a list of sub symbol tables (scopes)
    def __init__(self, scope_name):
        self.symbols = []
        self.scope_name = scope_name
        self.subScopes = []
        self.parent = None  # this might be useful to have? Idk

    def putSymbol(self, symbol):  # put variable symbol or fundef under <name> entry
        if symbol.name in self.symbols:
            # print(symbol.name, "in", self.symbols)
            return False
        else:
            # print("appending", symbol.name, "to", self.symbols)
            self.symbols.append(symbol)
            return True

    def getParentScope(self):
        return self.parent

    def printSymbols(self):
        for sym in self.symbols:
            output = ("name \"" + sym.name + "\"").ljust(20) + (" type " + str(sym.type)).ljust(20)
            #output = ("name \n" + sym.name + " \"")
            if sym.value is not None:
                output = output + " value " + str(sym.value)
            print(output)
