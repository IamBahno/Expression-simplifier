from calc_logic.expression_solver.tree_nodes.expression_node import OperatorNode
from calc_logic.expression_solver.tree_nodes.expression_node import OperandNode
from calc_logic.expression_solver.tree_nodes.expression_node import FunctionNode
from calc_logic.lex_analysis import Token
from calc_logic.expression_solver.values.values import FloatValue
from calc_logic.expression_solver.values.values import IntegerValue
from calc_logic.expression_solver.values.values import VarValue
from calc_logic.expression_solver.PathAndRule import Rules
import copy
from calc_logic.expression_solver.rules.utils import isMultiplicationWithOnePresent

# a*(b*c/3) mul before parentheses and mul and div inside
#a+(b+c-d) plus before parantheses and plus and minus inside
def checkForCommutativeProperty(node):
    if(isinstance(node,OperatorNode)):
        if node.type == "plus":
            if isinstance(node.right_child,OperatorNode) and (node.right_child.type == "plus" or node.right_child.type == "minus"):
                tmp = node.right_child.left_child
                while isinstance(tmp,OperatorNode):
                    if(tmp.type not in ["plus","minus"]):
                        return []
                    tmp = tmp.left_child
                return [Rules("CommutativeAddition")]
        elif node.type == "mul":
            if isinstance(node.right_child,OperatorNode) and (node.right_child.type == "mul" or node.right_child.type == "div"):
                tmp = node.right_child.left_child
                while isinstance(tmp,OperatorNode):
                    if(tmp.type not in ["mul","div"]):
                        return []
                    tmp = tmp.left_child
                #prevents creating loops
                if isMultiplicationWithOnePresent(node):
                    return []
                return [Rules("CommutativeMultiplication")]
        else:
            return []
    return []

def commutativeProperty(node):
    # new_node = node.right_child
    new_node = copy.deepcopy(node.right_child)
    if isinstance(new_node.left_child,OperatorNode) == False:
        tmp = new_node.left_child
        new_node.left_child = node
        new_node.left_child.right_child = tmp
        return new_node
    tmp = new_node
    while isinstance(tmp.left_child,OperatorNode):
        tmp = tmp.left_child
    tmp_node = tmp.left_child
    tmp.left_child = node
    tmp.left_child.right_child = tmp_node
    return new_node
