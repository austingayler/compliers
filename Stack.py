import Node
class Stack:
    def __init__(self):
        self.items = []
        self.debug = True

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)
    def search_stack(self,looking_for):
        found_it = False
        for item in self.items:
            if isinstance(item,Node.SymbolTable):
                thingToReturn = item.search_symbol_table(looking_for)
                if thingToReturn is not None:
                    return thingToReturn
            else:
                if item.name == looking_for:
                    found_it = True
                    return item.type
        if not found_it:
            return None
    def print_stack(self):
        print("in print_stack")
        for item in self.items:
            if isinstance(item,Node.SymbolTable):
                item.print_symbol_table()
            else:
                print(item.name)
        # temp_stack = []
        # while self.items != []:
        #     temp_stack.insert(0,self.items[0])
        #     self.items[0].print_symbol_table()
        #     self.items.pop(0)
        # while temp_stack != []:
        #     self.items.insert(0,temp_stack[0])
        #     temp_stack.pop(0)

    def printStackOp(self, op, sym_id, size):
        if self.debug is True:
            pass
