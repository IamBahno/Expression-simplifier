from calc_logic.lex_analysis import Token
from calc_logic.expression_solver.values.values import FloatValue
from calc_logic.expression_solver.values.values import IntegerValue
from calc_logic.expression_solver.values.values import VarValue
# import calc_logic.expression_solver.rules as RulesPack

class ExpressionNode():
    def __init__(self):
        pass

    def countNode(node):
        if(isinstance(node,FunctionNode)):
            return 1 + ExpressionNode.countNode(node.child)
        elif(isinstance(node,OperatorNode)):
            return 1 + ExpressionNode.countNode(node.left_child) + ExpressionNode.countNode(node.right_child)
        else:
            return 1

class OperatorNode(ExpressionNode):
    def __init__(self,operator : Token):
        super().__init__()
        self.type = operator.value# exp,mul,div,plus,minus,equal
        self.left_child = None
        self.right_child = None


class OperandNode(ExpressionNode):
    def __init__(self,operand):
        super().__init__()
        self.type = operand.type # var,int,float
        if self.type == "int":
            self.value  = IntegerValue(operand)
        if self.type == "float":
            self.value  = FloatValue(operand)
        if self.type == "var":
            self.value  = VarValue(operand)

class FunctionNode(ExpressionNode):
    def __init__(self,operator):
        super().__init__()
        self.type = operator.value # sin,cos,
        self.child = None