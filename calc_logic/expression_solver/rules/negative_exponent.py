from calc_logic.expression_solver.tree_nodes.expression_node import OperatorNode
from calc_logic.expression_solver.tree_nodes.expression_node import OperandNode
from calc_logic.expression_solver.tree_nodes.expression_node import FunctionNode
from calc_logic.lex_analysis import Token
from calc_logic.expression_solver.values.values import FloatValue
from calc_logic.expression_solver.values.values import IntegerValue
from calc_logic.expression_solver.values.values import VarValue
from calc_logic.expression_solver.PathAndRule import Rules
from calc_logic.expression_solver.rules.utils import isThereNegatavive
from calc_logic.expression_solver.rules.utils import isNegNumOrVar
from calc_logic.expression_solver.rules.utils import negOperand

def checkForNegativeExpToDiv(node):
    #x^a, x^-a
    if isinstance(node,OperatorNode) and node.type == "exp":
        if isThereNegatavive(node.right_child):
            # print("zz")
            return [Rules("neg-exp-to-div")]
    return []

def negativeExpToDiv(node):
    new_node = OperatorNode(Token("operator","div"))
    new_node.left_child = OperandNode(Token("int",1))
    tmp = node.right_child
    while True:
        while isinstance(tmp, OperatorNode) and tmp.type == "mul":
            if isNegNumOrVar(tmp.right_child):
                negOperand(tmp.right_child)
                new_node.right_child = node
                return new_node
            tmp = tmp.left_child
        if isinstance(tmp, OperatorNode) and tmp.type == "exp":
            if isinstance(tmp, OperandNode):
                if isNegNumOrVar(tmp):
                    negOperand(tmp)
                    new_node.right_child = node
                    return new_node
            else:
                tmp = tmp.left_child
                continue
        if isinstance(tmp, OperandNode):
            if isNegNumOrVar(tmp):
                negOperand(tmp)
                new_node.right_child = node
                return new_node

        if isinstance(tmp, OperatorNode) and tmp.type == "div":
            if isThereNegatavive(tmp.left_child):
                tmp = tmp.left_child
            elif isThereNegatavive(tmp.right_child):
                tmp = tmp.right_child
            continue

        print("chyba exp neg")
        exit(1)
