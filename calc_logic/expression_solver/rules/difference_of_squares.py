from calc_logic.expression_solver.tree_nodes.expression_node import OperatorNode
from calc_logic.expression_solver.tree_nodes.expression_node import OperandNode
from calc_logic.expression_solver.tree_nodes.expression_node import FunctionNode
from calc_logic.lex_analysis import Token
from calc_logic.expression_solver.values.values import FloatValue
from calc_logic.expression_solver.values.values import IntegerValue
from calc_logic.expression_solver.values.values import VarValue
from calc_logic.expression_solver.PathAndRule import Rules
from calc_logic.tools import printTree
import copy
import math

#return list of divisors, without 1
def divisorGenerator(n):
    large_divisors = []
    for i in range(2, int(math.sqrt(n) + 1)):
        if n % i == 0:
            yield int(i)
            if i*i != n:
                large_divisors.append(n / i)
    for divisor in reversed(large_divisors):
        yield int(divisor)
