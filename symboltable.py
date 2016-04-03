from pprint import pprint
import Stack

class Symbol:
    def __init__(self, name, value, type):
        self.name = name
        self.value = value
        self.type = type

class SymbolTable(object):

    #each symbol table has a list of symbols it contains and a list of sub symbol tables (scopes)
    def __init__(self, name):
        self.name = name
        self.symbols = Stack.Stack()

    def add_symbol(self, symbol):
        # output = ("name \"" + symbol.name + "\"").ljust(20) + (" type " + str(symbol.type)).ljust(20) #nice formatting
        output = "name " + symbol.name + " type " + str(symbol.type)
        if symbol.value is not None:
            output = output + " value " + str(symbol.value)
        print(output)
        self.symbols.push(symbol)
