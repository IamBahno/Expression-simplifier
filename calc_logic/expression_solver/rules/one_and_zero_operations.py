from calc_logic.expression_solver.tree_nodes.expression_node import OperatorNode
from calc_logic.expression_solver.tree_nodes.expression_node import OperandNode
from calc_logic.expression_solver.tree_nodes.expression_node import FunctionNode
from calc_logic.lex_analysis import Token
from calc_logic.expression_solver.values.values import FloatValue
from calc_logic.expression_solver.values.values import IntegerValue
from calc_logic.expression_solver.values.values import VarValue
from calc_logic.expression_solver.PathAndRule import Rules


def isOne(node):
    if isinstance(node,OperandNode):
        if node.type in ["int","float"]:
            if node.value.value == 1:
                return True
    return False

def isZero(node):
    if isinstance(node,OperandNode):
        if node.type in ["int","float"]:
            if node.value.value == 0:
                return True
    return False

# node is not Operand
# node * 1, node * 0, node/1, node/0, 0/node, node + 0, node - 0, node^1, node^0,
def checkForOneAndZeroOperations(node):
    if isinstance(node,OperatorNode):
        if node.type == "mul":
            if isOne(node.left_child):
                return [Rules("one-mul-node")]
            elif isOne(node.right_child):
                return [Rules("node-mul-one")]
            elif isZero(node.left_child):
                return [Rules("zero-mul-node")]
            elif isZero(node.right_child):
                return [Rules("node-mul-zero")]
            else:
                return []
        elif node.type == "div":
            if isOne(node.right_child) :
                return [Rules("node-div-one")]
            elif isZero(node.right_child):
                return [Rules("node-div-zero")]
            elif isZero(node.left_child):
                return [Rules("zero-div-node")]
            else:
                return []
        elif node.type in ["plus","minus"]:
            if isZero(node.left_child) :
                return [Rules("zero-plus-minus-node")]
            elif isZero(node.right_child):
                return [Rules("node-plus-minus-zero")]
        elif node.type == "exp":
            if isOne(node.left_child) :
                return [Rules("one-exp-node")]
            elif isOne(node.right_child):
                return [Rules("node-exp-one")]
            elif isZero(node.left_child):
                return [Rules("zero-exp-node")]
            elif isZero(node.right_child):
                return [Rules("node-exp-zero")]
            else:
                return []
        else:
            return []
    return []


# ["one-mul-node","node-mul-one","zero-mul-node","node-mul-zero","node-div-one","node-div-zero","zero-div-node",
#                            "zero-plus-minus-node","node-plus-minus-zero","one-exp-node","node-exp-one","zero-exp-node","node-exp-zero"]):
def oneZeroNodeOperations(node,rule):
    if rule.type == "one-mul-node":
        return node.right_child
    elif rule.type == "node-mul-one":
        return node.left_child
    elif rule.type in ["zero-mul-node","node-mul-zero"]:
        return OperandNode(Token("int",0))
    elif rule.type == "node-div-one":
        return node.left_child
    elif rule.type == "node-div-zero":
        return FunctionNode(Token("func","error"))
    elif rule.type == "zero-div-node":
        return OperandNode(Token("int",0))
    elif rule.type == "zero-plus-minus-node":
        return node.right_child
    elif rule.type == "node-plus-minus-zero":
        return node.left_child
    elif rule.type == "one-exp-node":
        return OperandNode(Token("int",1))
    elif rule.type == "node-exp-one":
        return node.left_child
    elif rule.type == "zero-exp-node":
        return OperandNode(Token("int",0))
    elif rule.type == "node-exp-zero":
        return OperandNode(Token("int",1))
    else:
        print("err")
        exit(1)