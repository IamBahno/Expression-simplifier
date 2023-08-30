from calc_logic.expression_solver.tree_nodes.expression_node import OperatorNode
from calc_logic.expression_solver.tree_nodes.expression_node import OperandNode
from calc_logic.expression_solver.tree_nodes.expression_node import FunctionNode
from calc_logic.lex_analysis import Token
from calc_logic.expression_solver.values.values import FloatValue
from calc_logic.expression_solver.values.values import IntegerValue
from calc_logic.expression_solver.values.values import VarValue
from calc_logic.expression_solver.PathAndRule import Rules

def checkForMinusParentheses(node):
    if isinstance(node,OperatorNode) and node.type == "minus":
        if isinstance(node.right_child,OperatorNode) and (node.right_child.type == "minus" or node.right_child.type == "plus"):
            return [Rules("node-minus-bracket")]
    return []

# a - (b+c) = a + (-1)*(b+c)
def nodeMinusBracket(node):
    new_node = OperatorNode(Token("operator","plus"))
    new_node.left_child = node.left_child
    new_node.right_child = OperatorNode(Token("operator","mul"))
    new_node.right_child.left_child = OperandNode(Token("int",-1))
    new_node.right_child.right_child = node.right_child
    return new_node