from calc_logic.expression_solver.tree_nodes.expression_node import FunctionNode
from calc_logic.expression_solver.tree_nodes.expression_node import OperandNode
from calc_logic.lex_analysis import Token
from calc_logic.expression_solver.PathAndRule import Rules
import math

def checkForComputeFunc(node):
    ret_rules = []
    if isinstance(node,FunctionNode):
        if node.type in ["sin","cos","tg","ctg","ln"]:
            if isinstance(node.child,OperandNode):
                if node.child.type == "int" or node.child.type == "float":
                    return [Rules("compute_function")]

    return ret_rules

def computeFunction(node):
    value = 0
    if node.type == "sin":
        value = math.sin(node.child.value.value)
    elif node.type == "cos":
        value = math.cos(node.child.value.value)
    elif node.type == "tg":
        value = math.tan(node.child.value.value)
    elif node.type == "ln":
        if node.child.value.value <= 0:
            return OperandNode(Token("var","UNDEFINED VALUE"))
        value = math.log(node.child.value.value)
    if int(value) == value:
        return OperandNode(Token("int",value))
    return OperandNode(Token("float",value))


