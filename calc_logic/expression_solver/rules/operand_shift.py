from calc_logic.expression_solver.tree_nodes.expression_node import OperatorNode
from calc_logic.expression_solver.tree_nodes.expression_node import OperandNode
from calc_logic.expression_solver.tree_nodes.expression_node import FunctionNode
from calc_logic.lex_analysis import Token
from calc_logic.expression_solver.values.values import FloatValue
from calc_logic.expression_solver.values.values import IntegerValue
from calc_logic.expression_solver.values.values import VarValue
from calc_logic.expression_solver.PathAndRule import Rules

from calc_logic.expression_solver.rules.utils import minusExpresions

# find where are you can shift operands
# a + b + c,
# a - b - c,
# a * b * c,
# a/(b/c),
#        div_right_shift
#           /
#       a      /
#           b     c
#
# (a/b)/c,
#        div_left_shift
#
#           /
#       /       c
#   a      b
#
# a - b + c,
#       plus_minus_shift
#           +
#       -      c
#     a    b
# a + b -c
#        minus_plus_shift
#           -
#       +      c
#     a    b
def checkForOperandShift(node):
    rules = []
    if isinstance(node, OperatorNode) and isinstance(node.left_child,OperatorNode):
        if(node.type == "plus" and node.left_child.type == "plus"):
            rules.append(Rules("plus_shift"))
        elif(node.type == "minus" and node.left_child.type == "minus"):
            rules.append(Rules("minus_shift"))
        elif(node.type == "mul" and node.left_child.type == "mul"):
            rules.append(Rules("mul_shift"))
        elif(node.type == "div" and node.left_child.type == "div"):
            rules.append(Rules("div_left_shift"))
        elif(node.type == "plus" and node.left_child.type == "minus"):
            rules.append(Rules("plus_minus_shift"))
        elif(node.type == "minus" and node.left_child.type == "plus"):
            rules.append(Rules("minus_plus_shift"))
    if isinstance(node, OperatorNode) and isinstance(node.right_child, OperatorNode):
        if(node.type == "div" and node.right_child.type == "div"):
            rules.append(Rules("div_right_shift"))

    return rules

def applyShiftOperations(node,rule):
    new_node = None
    if(rule.type == "plus_shift" or rule.type == "mul_shift" or rule.type == "plus_minus_shift"):
        new_node = node
        tmp = new_node.left_child.left_child
        new_node.left_child.left_child = node.right_child
        new_node.left_child.right_child,tmp = tmp,new_node.left_child.right_child
        new_node.right_child = tmp
        if rule.type == "plus_minus_shift":
            new_node.type = "minus"
            new_node.left_child.type = "plus"
    elif(rule.type == "minus_shift" or rule.type == "minus_plus_shift"):
        new_node = node
        if(rule.type == "minus_plus_shift"):
            new_node.type = "plus"
        new_node.left_child.type = "plus"
        tmp_node = node.left_child.left_child

        #legacy
        # new_node.left_child.left_child = OperatorNode(Token("operator","minus"))
        # new_node.left_child.left_child.left_child = OperandNode(Token("int",0))
        # new_node.left_child.left_child.right_child = node.right_child

        new_node.left_child.left_child = minusExpresions(node.right_child)

        new_node.left_child.right_child,tmp_node = tmp_node, new_node.left_child.right_child
        new_node.right_child = tmp_node
    elif(rule.type == "div_left_shift"):
        new_node = OperatorNode(Token("operator","div"))
        new_node.left_child = node.left_child.left_child
        new_node.right_child = OperatorNode(Token("operator","mul"))
        new_node.right_child.left_child = node.left_child.right_child
        new_node.right_child.right_child = node.right_child
    elif(rule.type == "div_right_shift"):
        new_node = OperatorNode(Token("operator","div"))
        new_node.left_child = OperatorNode(Token("operator","mul"))
        new_node.left_child.left_child = node.left_child
        new_node.left_child.right_child = node.right_child.right_child
        new_node.right_child = node.right_child.left_child


    return new_node