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

def build_little_node_list(ir):
    ir_node_list = []
    for stmt in ir:
        split = stmt.split()
        node = build_ir_node(split)
        if node is not None:
            ir_node_list.append(node)
    return ir_node_list
    
def build_ir_node(instructions_list):
    if "LINK" in instructions_list[0]: #or "LABEL" in instructions_list[0]
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
    name_map = {"ADDI": "addi","SUBI": "subi", "MULI": "muli",  "DIVI": "divi", "ADDF": "addr","SUBF": "subr", "MULF": "mulr",  "DIVF": "divr",
                "GTI":"jgt","GEI":"jge","LTI": "jlt","LEI": "jle","NEI":"jne","EQI":"jeq","GTF":"jgt","GEF":"jge","LTF":"jlt","LEF":"jle",
                "READI": "sys readi","READF": "sys readr","WRITEI": "sys writei","WRITEF": "sys writer","WRITES":"sys writes",
                "STOREI": "move", "STOREF":"move", "WRITEI": "sys writei","RET": "sys halt"}
    var_stack = Stack.Stack()
    seen_var_names = []
    for ir_node in ir_node_list:
        if ir_node.op_code in ["GTI","GEI","LTI","LEI","NEI","EQI"]:
            new_op1, new_op2,new_label = new_op(ir_node.op1, ir_node.op2,ir_node.result)
            node0 = Node.LittleNode("cmpi",new_op1, new_op2)
            node1 = Node.LittleNode(name_map[ir_node.op_code],new_label)
            node_list.append(node0)
            node_list.append(node1)
        elif ir_node.op_code in ["GTF","GEF","LTF","LEF"]:
            new_op1, new_op2,new_label = new_op(ir_node.op1, ir_node.op2,ir_node.result)
            node0 = Node.LittleNode("cmpr",new_op1, new_op2)
            node1 = Node.LittleNode(name_map[ir_node.op_code],new_label)
            node_list.append(node0)
            node_list.append(node1)
            # add values to stack to append to the beginning of the little_list when done.
        elif ir_node.op_code in ["JUMP"]:
            node = Node.LittleNode("jmp", ir_node.op1)
            node_list.append(node)
        elif ir_node.op_code in ["LABEL"]:
            node = Node.LittleNode("label", ir_node.op1)
            node_list.append(node)
        elif ir_node.op_code in ["WRITEI","WRITEF","WRITES"]:
            node = Node.LittleNode(name_map[ir_node.op_code],ir_node.op1)
            node_list.append(node)
        elif ir_node.op_code in ["READI","READF"]:
            new_op1, new_op2, _ = new_op(ir_node.op1, ir_node.op2)
            node = Node.LittleNode(name_map[ir_node.op_code],ir_node.op1)
            node_list.append(node)
            if ir_node.op1.isalpha():
                if ir_node.op1 not in seen_var_names:
                    node = Node.LittleNode("var", new_op1)
                    var_stack.push(node)
                    seen_var_names.append(ir_node.op1)

        elif ir_node.op_code in ["STOREI","STOREF"]:
            new_op1, new_op2, _ = new_op(ir_node.op1, ir_node.op2)
            node = Node.LittleNode(name_map[ir_node.op_code], new_op1, new_op2)
            node_list.append(node)
            # add values to stack to append to the beginning of the little_list when done.
            if ir_node.op2.isalpha():
                if ir_node.op2 not in seen_var_names:
                    node = Node.LittleNode("var", new_op2)
                    var_stack.push(node)
                    seen_var_names.append(ir_node.op2)
        elif ir_node.op_code in ["ADDI", "DIVI", "MULI", "ADDF","SUBF","MULF","DIVF"]:
            new_op1, new_op2, new_result = new_op(ir_node.op1, ir_node.op2, ir_node.result)
            node0 = Node.LittleNode("move", new_op1, new_result)
            node1 = Node.LittleNode(name_map[ir_node.op_code], new_op2, new_result)
            node_list.append(node0)
            node_list.append(node1)
        elif ir_node.op_code in ["WRITEI", "RET"]:
            new_op1, _, _ = new_op(ir_node.op1)
            node = Node.LittleNode(name_map[ir_node.op_code], new_op1)
            node_list.append(node)
        else:
            print("ERROR - Unhandeled op_code:", "\"" + ir_node.op_code + "\"")

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

def convert_ir_to_tiny(ir):
    little_node_list = transpile(build_little_node_list(ir))
    #little_node_list = transpile(read_file("IR_code_output.txt"))
    return_list = []
    for node in little_node_list:
        return_list.append(node.op_code+" "+node.op1+" "+node.op2)
    return return_list