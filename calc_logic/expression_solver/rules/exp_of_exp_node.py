from calc_logic.expression_solver.tree_nodes.expression_node import OperatorNode
from calc_logic.expression_solver.tree_nodes.expression_node import OperandNode
from calc_logic.expression_solver.tree_nodes.expression_node import FunctionNode
from calc_logic.lex_analysis import Token
from calc_logic.expression_solver.values.values import FloatValue
from calc_logic.expression_solver.values.values import IntegerValue
from calc_logic.expression_solver.values.values import VarValue
from calc_logic.expression_solver.PathAndRule import Rules

def checkForExpOfExpNode(node):
    if isinstance(node,OperatorNode) and node.type == "exp":
        if isinstance(node.left_child,OperatorNode) and node.left_child.type == "exp":
            return [Rules("exp-of-exp-node")]
    return []

# (x^a)^b = x^(a*c)
def expOfExpNode(node):
    new_node = OperatorNode(Token("operator","exp"))
    new_node.left_child = node.left_child.left_child
    new_node.right_child = OperatorNode(Token("operator","mul"))
    new_node.right_child.left_child = node.left_child.right_child
    new_node.right_child.right_child = node.right_child
    return new_node