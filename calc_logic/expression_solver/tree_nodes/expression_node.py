from calc_logic.lex_analysis import Token
from calc_logic.expression_solver.values.values import FloatValue
from calc_logic.expression_solver.values.values import IntegerValue
from calc_logic.expression_solver.values.values import VarValue

FUNC_SCORE = 1
VAR_SCORE = 1
INT_SCORE = 2
FLOAT_SCORE = 1
PLUS_SCORE = 3
MINUS_SCORE = 1
MUL_SCORE = 2
DIV_SCORE = 2
EXP_SCORE = 4

class ExpressionNode():
    def __init__(self):
        pass

    def __eq__(self, other):
        return treeEqual(self,other)

    # idc
    def __hash__(self):
        return 1

    def countNode(node):
        if(isinstance(node,FunctionNode)):
            return 1 + ExpressionNode.countNode(node.child)
        elif(isinstance(node,OperatorNode)):
            return 1 + ExpressionNode.countNode(node.left_child) + ExpressionNode.countNode(node.right_child)
        else:
            return 1


    # in expanded solution is sum of terms
    def expandedSolutionScore(node):
        if isinstance(node,FunctionNode):
            return FUNC_SCORE + ExpressionNode.expandedSolutionScore(node.child)
        elif isinstance(node,OperandNode):
            if node.type == "var":
                return VAR_SCORE
            elif node.type == "int":
                return INT_SCORE
            else:
                return FLOAT_SCORE
        else:
            left_mul = 1
            right_mul = 1
            if node.type == "plus":
                if isinstance(node.left_child,OperatorNode):
                    if node.left_child.type == "plus" or node.left_child.type == "minus":
                        left_mul =+ 1
                if isinstance(node.right_child,OperatorNode):
                    if node.right_child.type == "plus":
                        right_mul += 1
                return PLUS_SCORE + left_mul * ExpressionNode.expandedSolutionScore(node.left_child) + right_mul * ExpressionNode.expandedSolutionScore(node.right_child)
            elif node.type == "minus":
                if isinstance(node.left_child,OperatorNode):
                    if node.left_child.type == "plus" or node.left_child.type == "minus":
                        left_mul =+ 1
                return MINUS_SCORE + left_mul * ExpressionNode.expandedSolutionScore(node.left_child) + ExpressionNode.expandedSolutionScore(node.right_child)
            elif node.type == "mul":
                return MUL_SCORE + ExpressionNode.expandedSolutionScore(node.left_child) + ExpressionNode.expandedSolutionScore(node.right_child)
            elif node.type == "div":
                return DIV_SCORE + ExpressionNode.expandedSolutionScore(node.left_child) + ExpressionNode.expandedSolutionScore(node.right_child)
            elif node.type == "exp":
                return EXP_SCORE + ExpressionNode.expandedSolutionScore(node.left_child) + ExpressionNode.expandedSolutionScore(node.right_child)


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


def treeEqual(original_node,compare_to):
    if(type(original_node) != type(compare_to)):
        return False
    if(isinstance(original_node,OperatorNode)):
        if(original_node.type == compare_to.type):
            return True and treeEqual(original_node.left_child,compare_to.left_child) and treeEqual(original_node.right_child,compare_to.right_child)
        else:
            return False
    if(isinstance(original_node,OperandNode)):
        if(original_node.type == compare_to.type):
            if(original_node.type == "var"):
                if(original_node.value.name == compare_to.value.name):
                    return True
                else:
                    return False

            if(original_node.value.value == compare_to.value.value):
                return True
            else:
                return False
        else:
            return False
    if(isinstance(original_node,FunctionNode)):
        if(original_node.type == compare_to.type):
            return True and treeEqual(original_node.child,compare_to.child)
        else:
            return False