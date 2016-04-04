class IRNode:

    def __init__(self, op_code, op1, op2, result):
        self.op_code = op_code
        self.op1 = op1
        self.op2 = op2
        self.result = result

class LittleNode:

    def __init__(self, op_code, op1, op2):
        self.op_code = op_code
        self.op1 = op1
        self.op2 = op2