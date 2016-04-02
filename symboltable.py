from pprint import pprint

class Symbol:
    def __init__(self, name, value, type):
        self.name = name
        self.value = value
        self.type = type

class SymbolTable(object):

    #each symbol table has a list of symbols it contains and a list of sub symbol tables (scopes)
    def __init__(self, name):
        self.name = name

        self.symbols = []
        self.subtables = []

        self.parent = None

    def add_symbol(self, symbol):
        # output = ("name \"" + symbol.name + "\"").ljust(20) + (" type " + str(symbol.type)).ljust(20) #nice formatting
        output = "name " + symbol.name + " type " + str(symbol.type)
        if symbol.value is not None:
            output = output + " value " + str(symbol.value)
        print(output)
        self.symbols.append(symbol)

    def get_all_parent_symbols(self, tbl):
        if tbl is None:
            return []
        ret = [] + tbl.symbols
        if self.parent is not None:
            return ret + self.get_all_parent_symbols(tbl.parent)
        else:
            return ret

    def parent_table(self):
        return self.parent

    def add_subtable(self, sym_tbl):
        sym_tbl.parent = self
        self.subtables.append(sym_tbl)

    def traverse_subtable(self):
        return self.subtables[-1]

    def print_symbols(self):
        print(self.name, ":")
        for sym in self.symbols:
            output = ("    name \"" + sym.name + "\"").ljust(20) + (" type " + str(sym.type)).ljust(20)
            #output = ("name \n" + sym.name + " \"")
            if sym.value is not None:
                output = output + " value " + str(sym.value)
            print(output)

    def print_subtables(self): #prints subtables 1 level deeper
        print("\nPrinting subtables:")
        for tbl in self.subtables:
            print(tbl.name)
        print("\n")

    def recursive_print_all_subtables(self, subtable, depth):
        #recursive call to print all subtables. meant for global sym table

        print("Symbol table", subtable.name)#, str(depth))
        for sym in subtable.symbols:
            str_out = "name " + sym.name + " type " + sym.type
            if sym.value is not None and sym.value is not -1:
                str_out = str_out + " value " + str(sym.value)
            print(str_out)
        print()

        for tbl in subtable.subtables:
            self.recursive_print_all_subtables(tbl, depth + 1)

    def recursive_print_scopes(self, subtable, depth):
        #recursive call to print all subtables. meant for global sym table

        out = ""
        for i in range(0, depth):
            out += "    "
        print(out + subtable.name)
        for tbl in subtable.subtables:
            self.recursive_print_scopes(tbl, depth + 1)



    def get_root_table(self):
        st = self
        while st.name is not "GLOBAL":
            st = st.parent_table()
        return st
