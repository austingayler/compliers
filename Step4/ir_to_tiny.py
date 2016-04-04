import sys

import Node
import pprint


node_list = []


def read_file(file_name):
    with open(file_name) as f:
        for instructions in f:
            split = instructions.split()
            build_ir_node(split)


def build_ir_node(instructions_list):
    if "LABEL" in instructions_list[0] or "LINK" in instructions_list[0]:
        pass
    else:
        try:
            op_code = instructions_list[0]
        except IndexError:
            op_code = None

        try:
            op1 = instructions_list[1]
        except IndexError:
            op1 = None

        try:
            op2 = instructions_list[2]
        except IndexError:
            op2 = None

        try:
            result = instructions_list[3]
        except IndexError:
            result = None

        node = Node.IRNode(op_code, op1, op2, result)
        node_list.append(node)

input = sys.argv[1]
read_file(input)

pp = pprint.PrettyPrinter(indent=4)

for node in node_list:
    print(vars(node))