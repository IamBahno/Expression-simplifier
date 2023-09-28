from calc_logic.expression_solver.tree_nodes.expression_node import OperatorNode
from calc_logic.expression_solver.tree_nodes.expression_node import OperandNode
from calc_logic.expression_solver.tree_nodes.expression_node import FunctionNode
from calc_logic.lex_analysis import Token
from calc_logic.expression_solver.values.values import FloatValue
from calc_logic.expression_solver.values.values import IntegerValue
from calc_logic.expression_solver.values.values import VarValue
from calc_logic.expression_solver.PathAndRule import Rules

import copy

# (x*y)^a
def checkExpOfNode(node):
    if isinstance(node,OperatorNode) and node.type == "exp":
        if isinstance(node.left_child,OperatorNode) and (node.left_child.type == "mul" or node.left_child.type == "div"):
            return [Rules("exp-of-mult-or-div")]
    return []

def expOfNode(node,rule):
    # (a*b)^x or (a/b)^x
    # == a^x*b^x
    if rule.type == "exp-of-mult-or-div":
        #(a * b) ^ x
        if node.left_child.type == "mul":
            new_node = node.left_child
            tmp = new_node
            while isinstance(tmp.left_child,OperatorNode) and tmp.left_child.type== "mul":
                tmp_right =tmp.right_child
                tmp.right_child = OperatorNode(Token("operator","exp"))
                tmp.right_child.left_child = tmp_right
                tmp.right_child.right_child = copy.deepcopy(node.right_child)
                tmp = tmp.left_child
            #right side of last node
            tmp_right = tmp.right_child
            tmp.right_child = OperatorNode(Token("operator", "exp"))
            tmp.right_child.left_child = tmp_right
            tmp.right_child.right_child = copy.deepcopy(node.right_child)
            #left side of last ndoe
            tmp_left = tmp.left_child
            tmp.left_child = OperatorNode(Token("operator", "exp"))
            tmp.left_child.left_child = tmp_left
            tmp.left_child.right_child = copy.deepcopy(node.right_child)
            return new_node


        # (a / b) ^ x == a^2/b^2
        else:
            new_node = OperatorNode(Token("operator","div"))
            new_node.left_child = OperatorNode(Token("operator","exp"))
            new_node.right_child = OperatorNode(Token("operator", "exp"))
            new_node.left_child.left_child = node.left_child.left_child
            new_node.left_child.right_child = copy.deepcopy(node.right_child)
            new_node.right_child.left_child = node.left_child.right_child
            new_node.right_child.right_child = copy.deepcopy(node.right_child)
            return new_node


    return node