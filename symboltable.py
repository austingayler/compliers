class Symbol:
    #def __init__(self, name, value, type):
    def __init__(self, name=None, value=None, type=None):
        self.name = name
        self.value = value
        self.type = type


class SymbolTable(object):
    # each symbol table has a list of symbols it contains and a list of sub symbol tables (scopes)
    def __init__(self, scope_name):
        self.symbols = None
        self.name = scope_name

    def put_symbol(self, symbol):  # put variable symbol or fundef under <name> entry
        if symbol.name in self.symbols:
            # print(symbol.name, "in", self.symbols)
            return False
        else:
            # print("appending", symbol.name, "to", self.symbols)
            self.symbols.append(symbol)
            return True

    def print_symbols(self):
        for sym in self.symbols:
            output = ("name \"" + sym.name + "\"").ljust(20) + (" type " + str(sym.type)).ljust(20)
            if sym.value is not None:
                output = output + " value " + str(sym.value)
            print(output)


    def print_scope_stack(self, root):
        print("Symbol Table", root.name)
        # self.print_symbols(root)
        for scope in root.sub_scopes:
            self.print_scope_stack(scope)