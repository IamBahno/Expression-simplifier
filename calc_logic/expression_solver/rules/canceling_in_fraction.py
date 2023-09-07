from calc_logic.expression_solver.tree_nodes.expression_node import OperatorNode
from calc_logic.expression_solver.tree_nodes.expression_node import OperandNode
from calc_logic.expression_solver.tree_nodes.expression_node import FunctionNode
from calc_logic.lex_analysis import Token
from calc_logic.expression_solver.values.values import FloatValue
from calc_logic.expression_solver.values.values import IntegerValue
from calc_logic.expression_solver.values.values import VarValue
from calc_logic.expression_solver.PathAndRule import Rules
from calc_logic.tools import printTree
from calc_logic.expression_solver.rules.utils import treeEqual

import copy
import math
from fractions import Fraction

# num = numerator
# den = denominator
def gcd_non_integer(a, b):
    fraction_a = Fraction(a)
    fraction_b = Fraction(b)
    hcf = Fraction.gcd(fraction_b)
    return hcf

def expressionToMulParts(node):
    ex_list = []
    tmp_numerator = node
    while isinstance(tmp_numerator, OperatorNode) and tmp_numerator.type == "mul":
        # if there is exponent i only append the base
        if isinstance(tmp_numerator.right_child, OperatorNode) and tmp_numerator.right_child.type == "exp":
            ex_list.append(tmp_numerator.right_child.left_child)
        else:
            ex_list.append(tmp_numerator.right_child)
        tmp_numerator = tmp_numerator.left_child
    if isinstance(tmp_numerator, OperatorNode) and tmp_numerator.type == "exp":
        ex_list.append(tmp_numerator.left_child)
    else:
        ex_list.append(tmp_numerator)
    return ex_list

# a*x/x
def checkForFractionCanceling(node):
    ret_rules = []

    numerator_list = []
    denominator_list = []
    if isinstance(node,OperatorNode) and node.type == "div":
        tmp_numerator = node.left_child
        numerator_list = expressionToMulParts(tmp_numerator)


        tmp_denominator = node.right_child
        denominator_list = expressionToMulParts(tmp_denominator)


    highest_gcd_yet = 0
    for i in numerator_list:
        if isinstance(i,OperandNode) and (i.type == "int" or i.type == "float"):
            for j in denominator_list:
                gcd = 0
                if isinstance(j,OperandNode) and (j.type == "int" or j.type == "float"):
                    try:
                        gcd = math.gcd(i.value.value,j.value.value)
                    # for floats
                    # dont support floats yet
                    except:
                        continue
                if gcd > highest_gcd_yet:
                    highest_gcd_yet = gcd
        else:
            continue
    if highest_gcd_yet > 1:
        ret_rules.append(Rules("fraction-canceling-"+str(highest_gcd_yet)))

    intersection = list(set(numerator_list).intersection(denominator_list))
    if intersection != []:
        ret_rules.append(Rules("fraction-canceling-node"))

    return ret_rules

# (a/b)*(b/a)
def checkForMulOfFractCanceling(node):
    ret_rules = []
    if isinstance(node,OperatorNode) and node.type == "mul":
        if (isinstance(node.left_child,OperatorNode) and node.left_child.type == "div") or (isinstance(node.right_child,OperatorNode) and node.right_child.type == "div"):
            left_num_list = []
            left_den_list = []
            right_num_list = []
            right_den_list = []

            # (a/a)*node
            if (isinstance(node.left_child, OperatorNode) and node.left_child.type == "div"):
                tmp_left_numerator = node.left_child.left_child
                left_num_list = expressionToMulParts(tmp_left_numerator)

                tmp_left_denominator = node.left_child.right_child
                left_den_list = expressionToMulParts(tmp_left_denominator)
            else:
                tmp_left_numerator = node.left_child
                left_num_list = expressionToMulParts(tmp_left_numerator)

            # node*(a/a)
            if (isinstance(node.right_child, OperatorNode) and node.right_child.type == "div"):
                tmp_right_numerator = node.right_child.left_child
                right_num_list = expressionToMulParts(tmp_right_numerator)

                tmp_right_denominator = node.right_child.right_child
                right_den_list = expressionToMulParts(tmp_right_denominator)
            else:
                tmp_right_numerator = node.right_child
                right_num_list = expressionToMulParts(tmp_right_numerator)


            # (x/a)*(a/x), x*(a/x)
            if right_den_list != []:
                highest_gcd_yet = 0
                for i in left_num_list:
                    if isinstance(i, OperandNode) and (i.type == "int" or i.type == "float"):
                        for j in right_den_list:
                            gcd = 0
                            if isinstance(j, OperandNode) and (j.type == "int" or j.type == "float"):
                                try:
                                    gcd = math.gcd(i.value.value, j.value.value)
                                # for floats
                                # dont support floats yet
                                except:
                                    continue
                            if gcd > highest_gcd_yet:
                                highest_gcd_yet = gcd
                    else:
                        continue
                if highest_gcd_yet > 1:
                    ret_rules.append(Rules("mul-of-fract-canceling-left-num-" + str(highest_gcd_yet)))

                intersection = list(set(left_num_list).intersection(right_den_list))
                if intersection != []:
                    ret_rules.append(Rules("mul-of-fract-canceling-left-num-node"))

            # (a/x)*(x/a), (a/x)*x
            if left_den_list != []:
                highest_gcd_yet = 0
                for i in left_den_list:
                    if isinstance(i, OperandNode) and (i.type == "int" or i.type == "float"):
                        for j in right_num_list:
                            gcd = 0
                            if isinstance(j, OperandNode) and (j.type == "int" or j.type == "float"):
                                try:
                                    gcd = math.gcd(i.value.value, j.value.value)
                                # for floats
                                # dont support floats yet
                                except:
                                    continue
                            if gcd > highest_gcd_yet:
                                highest_gcd_yet = gcd
                    else:
                        continue
                if highest_gcd_yet > 1:
                    ret_rules.append(Rules("mul-of-fract-canceling-left-den-" + str(highest_gcd_yet)))

                intersection = list(set(left_den_list).intersection(right_num_list))
                if intersection != []:
                    ret_rules.append(Rules("mul-of-fract-canceling-left-den-node"))
    return ret_rules

# "fraction-canceling-"+str(highest_gcd_yet)"
# "fraction-canceling-node"

#"mul-of-fract-canceling-left-num-" + str(highest_gcd_yet)
# "mul-of-fract-canceling-left-num-node"
# "mul-of-fract-canceling-left-den-" + str(highest_gcd_yet)
# "mul-of-fract-canceling-left-den-node"

def fractCanceling(node,rule):
    numerator_list = []
    denominator_list = []

    #nodes
    if rule.type in ["fraction-canceling-node","mul-of-fract-canceling-left-num-node","mul-of-fract-canceling-left-den-node"]:
        if rule.type == "fraction-canceling-node":
                numerator_list = expressionToMulParts(node.left_child)
                denominator_list = expressionToMulParts(node.right_child)
        elif rule.type == "mul-of-fract-canceling-left-num-node":
            # (a/a)/(a/a)
            if isinstance(node.left_child,OperatorNode) and node.left_child.type == "div":
                numerator_list = expressionToMulParts(node.left_child.left_child)
            # node / (a/a)
            else:
                numerator_list = expressionToMulParts(node.left_child)
            denominator_list = expressionToMulParts(node.right.right_child)
        elif rule.type == "mul-of-fract-canceling-left-den-node":
            # (a/a)/(a/a)
            if isinstance(node.right_child,OperatorNode) and node.right_child.type == "div":
                numerator_list = expressionToMulParts(node.right_child.left_child)
            # (a/a)/node
            else:
                numerator_list = expressionToMulParts(node.right_child)
            denominator_list = expressionToMulParts(node.left_child.right_child)
        intersection = list(set(numerator_list).intersection(denominator_list))


    #numes
    else:
        pass

# find node in expression mul together and replace
def findInExpressAndReplace(expresion,node):
    tmp = expresion
    if treeEqual(tmp,node):
        return OperandNode(Token("int",1))
    if(isinstance(tmp,OperandNode) and node.type == "mul"):
        if treeEqual(tmp.right_child, node):
            tmp.right_child = OperandNode(Token("int",1))
    while isinstance(tmp.left_child,OperatorNode) and tmp.type == "mul":
        if treeEqual(tmp.right_child,node):
            tmp.right_child = OperandNode(Token("int",1))
            return expresion
        tmp = tmp.left_child
    if treeEqual(tmp.left_child,node):
        tmp.left_child = OperandNode(Token("int",1))
        return expresion
    elif treeEqual(tmp.right_child,node):
        tmp.right_child = OperandNode(Token("int",1))
        return expresion
    else:
        print("canceling err")
        exit(1)

#finde node in expresion and returns node, with its power
def findInExpressAndRetPower(expresion,node):
    tmp = expresion
    if treeEqual(tmp,node):
        return OperandNode(Token("int",1))
    elif isinstance(tmp,OperatorNode) and tmp.type == "exp" and treeEqual(tmp.left_child,node):
        return copy.deepcopy(tmp.right_child)
    if(isinstance(tmp,OperandNode) and node.type == "mul"):
        if treeEqual(tmp.right_child, node):
            return OperandNode(Token("int", 1))
        elif isinstance(tmp.right_child, OperatorNode) and tmp.right_child.type == "exp" and treeEqual(tmp.right_child.left_child, node):
            return copy.deepcopy(tmp.right_child.right_child)
    while isinstance(tmp.left_child,OperatorNode) and tmp.type == "mul":
        if treeEqual(tmp.right_child,node):
            return OperandNode(Token("int", 1))
        elif isinstance(tmp.right_child, OperatorNode) and tmp.right_child.type == "exp" and treeEqual(tmp.right_child.left_child, node):
            return copy.deepcopy(tmp.right_child.right_child)
        tmp = tmp.left_child
    if treeEqual(tmp.left_child,node):
        return OperandNode(Token("int", 1))
    elif isinstance(tmp.left_child, OperatorNode) and tmp.left_child.type == "exp" and treeEqual(tmp.left_child.left_child, node):
        return copy.deepcopy(tmp.left_child.right_child)
    elif treeEqual(tmp.right_child,node):
        return OperandNode(Token("int", 1))
    elif isinstance(tmp.right_child, OperatorNode) and tmp.right_child.type == "exp" and treeEqual(
            tmp.right_child.left_child, node):
        return copy.deepcopy(tmp.right_child.right_child)
    print("problemek")
    exit(1)

