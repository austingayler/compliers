import sys

import Node
import Stack


def read_file(file_name):
    ir_node_list = []
    with open(file_name) as f:
        for instructions in f:
            split = instructions.split()
            node = build_ir_node(split)
            if node is not None:
                ir_node_list.append(node)
    return ir_node_list

def build_ir_node(instructions_list):
    if "LABEL" in instructions_list[0] or "LINK" in instructions_list[0]:
        pass
    else:
        op_code = instructions_list[0]

        try:
            op1 = instructions_list[1]
        except IndexError:
            op1 = ""

        try:
            op2 = instructions_list[2]
        except IndexError:
            op2 = ""

        try:
            result = instructions_list[3]
        except IndexError:
            result = ""

        return Node.IRNode(op_code, op1, op2, result)


def transpile(ir_node_list):
    node_list = []
    name_map = {"STOREI": "move", "MULTI": "muli", "ADDI": "addi", "DIVI": "divi", "WRITEI": "sys writei",
                "RET": "sys halt"}
    var_stack = Stack.Stack()
    seen_var_names = []
    for ir_node in ir_node_list:
        if ir_node.op_code == "STOREI":
            new_op1, new_op2, _ = new_op(ir_node.op1, ir_node.op2)
            node = Node.LittleNode("move", new_op1, new_op2)
            node_list.append(node)
            # add values to stack to append to the beginning of the little_list when done.
            if ir_node.op2.isalpha():
                if ir_node.op2 not in seen_var_names:
                    node = Node.LittleNode("var", new_op2)
                    var_stack.push(node)
                    seen_var_names.append(ir_node.op2)
        elif ir_node.op_code in ["ADDI", "DIVI", "MULTI"]:
            new_op1, new_op2, new_result = new_op(ir_node.op1, ir_node.op2, ir_node.result)
            node0 = Node.LittleNode("move", new_op1, new_result)
            node1 = Node.LittleNode(name_map[ir_node.op_code], new_op2, new_result)
            node_list.append(node0)
            node_list.append(node1)
            pass
        elif ir_node.op_code in ["WRITEI", "RET"]:
            new_op1, _, _ = new_op(ir_node.op1)
            node = Node.LittleNode(name_map[ir_node.op_code], new_op1)
            node_list.append(node)
        else:
            print("ERROR - Unhandeled op_code:", ir_node.op_code)

    # put the variable declarations into the beginning of little_node_list in the correct order.
    for _ in range(len(var_stack.items)):
        node_list.insert(0, var_stack.pop())

    return node_list


def new_op(op1, op2="", op3=""):
    # Strip "$T" from ir_node op codes and replace with "r". also decrement op values (may not be necessary).
    new_op1, new_op2, new_op3 = op1, op2, op3
    if "$T" in op1:
        new_op1 = "r" + str(int(op1[2:]) - 1)

    if "$T" in op2:
        new_op2 = "r" + str(int(op2[2:]) - 1)

    if "$T" in op3:
        new_op3 = "r" + str(int(op3[2:]) - 1)

    return new_op1, new_op2, new_op3


little_node_list = transpile(read_file(sys.argv[1]))

for node in little_node_list:
    print(node.op_code, node.op1, node.op2)