from calc_logic.expression_solver.tree_nodes.expression_node import OperatorNode
from calc_logic.expression_solver.tree_nodes.expression_node import OperandNode
from calc_logic.expression_solver.tree_nodes.expression_node import FunctionNode
from calc_logic.lex_analysis import Token
from calc_logic.expression_solver.values.values import FloatValue
from calc_logic.expression_solver.values.values import IntegerValue
from calc_logic.expression_solver.values.values import VarValue
from calc_logic.expression_solver.PathAndRule import Rules

from calc_logic.expression_solver.rules.utils import treeEqual

def checkForExponentMulDiv(node):
    if(isinstance(node,OperatorNode) == False):
        return []
    if(node.type not in ["mul","div"]):
        return []
    if node.type == "mul":
        operator = "mul"
    else:
        operator = "div"
    # exponents on both sides
    if(isinstance(node.left_child,OperatorNode) and isinstance(node.right_child,OperatorNode)):
        if node.left_child.type == "exp" and node.right_child.type == "exp":
            if treeEqual(node.left_child.left_child,node.right_child.left_child):
                return [Rules("exponent_" + operator)]
            return []
    # check for something to power of 1
    if treeEqual(node.left_child,node.right_child):
        return [Rules("same_nodes_" + operator)]
    if isinstance(node.left_child,OperatorNode):
        if node.left_child.type == "exp":
            if treeEqual(node.left_child.left_child,node.right_child):
                return [Rules("exponent_left_" + operator)]
        return []
    if isinstance(node.right_child,OperatorNode):
        if node.right_child.type == "exp":
            if treeEqual(node.right_child.left_child,node.left_child):
                return [Rules("exponent_right_" + operator)]
        return []
    return []


def exponentMulDiv(node,rule):
    if(rule.type in ["exponent_mul","same_nodes_mul","exponent_left_mul","exponent_right_mul"]):
        operator_node = OperatorNode(Token("operator", "plus"))
    else:
        operator_node = OperatorNode(Token("operator", "minus"))

    new_node = OperatorNode(Token("operator","exp"))

    if(rule.type in ["exponent_mul","exponent_div"]):
        new_node.left_child = node.left_child.left_child
        new_node.right_child = operator_node
        new_node.right_child.left_child = node.left_child.right_child
        new_node.right_child.right_child = node.right_child.right_child
        return new_node
    if(rule.type in ["same_nodes_mul","same_nodes_div"]):
        if rule.type == "same_nodes_mul":
            new_node.left_child = node.left_child
            new_node.right_child = OperandNode(Token("int",2))
        else:
            new_node = OperandNode(Token("int",1))
        return new_node

    if(rule.type in ["exponent_left_mul","exponent_left_div"]):
        new_node.left_child = node.right_child
        new_node.right_child = operator_node
        new_node.right_child.left_child = node.left_child.right_child
        new_node.right_child.right_child = OperandNode(Token("int",1))
        return new_node
    if(rule.type in ["exponent_right_mul","exponent_right_div"]):
        new_node.left_child = node.left_child
        new_node.right_child = operator_node
        new_node.right_child.left_child = node.right_child.right_child
        new_node.right_child.right_child = OperandNode(Token("int",1))
        return new_node
    return "errorek"