from calc_logic.expression_solver.tree_nodes.expression_node import OperatorNode
from calc_logic.expression_solver.tree_nodes.expression_node import OperandNode
from calc_logic.expression_solver.tree_nodes.expression_node import FunctionNode
from calc_logic.lex_analysis import Token
from calc_logic.expression_solver.values.values import FloatValue
from calc_logic.expression_solver.values.values import IntegerValue
from calc_logic.expression_solver.values.values import VarValue
from calc_logic.expression_solver.PathAndRule import Rules
import copy


def checkForBrackMulDiv(node):
    rules = []
    if isinstance(node,OperatorNode) and (node.type == "mul" or node.type == "div"):
        if isinstance(node.left_child,OperatorNode) or isinstance(node.right_child,OperatorNode):
            if node.type == "mul":
                # return [Rules("brack_mul_right"),Rules("brack_mul_left")]
                return [Rules("brack_mul_right")]
            else:
                return [Rules("brack_div_right")]
    return []


def mulDivBracket(node,rule):
    # print("pred:"+printTree(node))

    #a * (b + c) = a*b+a*c
    # if rule.type == "brack_mul_right" or rule.type == "brack_div_right":
    if rule.type == "brack_mul_right":

        multiplier = node.left_child
        tmp = node.right_child
    else:
        multiplier = node.right_child
        tmp = node.left_child

    # the node iam about to multiply is operator or function or things mul together (one "value" basically)
    if( isinstance(tmp,OperatorNode) == False or (isinstance(tmp,OperatorNode) and tmp.type != "plus" and tmp.type != "minus")):
        if(rule.type in ["brack_mul_right","brack_mul_left"]):
            new_node = OperatorNode(Token("operator","mul"))
        else:
            new_node = OperatorNode(Token("operator","div"))

        new_node.right_child = multiplier
        new_node.left_child = tmp
        return new_node

    new_node=tmp

    while isinstance(tmp.left_child,OperatorNode) and (tmp.left_child.type == "plus" or tmp.left_child.type == "minus"):
        tmp_right = tmp.right_child
        if(rule.type in ["brack_mul_right","brack_mul_left"]):
            tmp.right_child = OperatorNode(Token("operator","mul"))
        else:
            tmp.right_child = OperatorNode(Token("operator","div"))
        tmp.right_child.right_child = copy.deepcopy(multiplier)
        tmp.right_child.left_child = tmp_right
        tmp = tmp.left_child
    tmp_left = tmp.left_child
    tmp_right = tmp.right_child
    if (rule.type in ["brack_mul_right", "brack_mul_left"]):
        tmp.left_child = OperatorNode(Token("operator","mul"))
        tmp.right_child = OperatorNode(Token("operator","mul"))
    else:
        tmp.left_child = OperatorNode(Token("operator", "div"))
        tmp.right_child = OperatorNode(Token("operator", "div"))
    tmp.right_child.right_child = copy.deepcopy(multiplier)
    tmp.left_child.right_child = copy.deepcopy(multiplier)
    tmp.right_child.left_child = tmp_right
    tmp.left_child.left_child = tmp_left
    # print("po:"+printTree(new_node))
    return new_node