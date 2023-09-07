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

def check_for_multinomial(node):
    if isinstance(node,OperatorNode) and node.type == "exp":
        if isinstance(node.left_child,OperatorNode) and (node.left_child.type == "plus" or node.left_child.type == "minus"):
            if isinstance(node.right_child,OperandNode) and (node.right_child.type == "int" or (node.right_child.type == "float" and node.right_child.value.value == int(node.right_child.value.value)) ):
                if node.right_child.value.value > 1:
                    return [Rules("multinomial_theorem")]
    return []



class TermAndSign():
    def __init__(self,term,sign):
        self.term = term
        self.sign = sign

# return list of lists of combinations (of size elements) that add up to sum
def generate_combinations(total_sum, num_terms):
    def generate_combinations_helper(total_sum, num_terms, current_combination):
        if num_terms == 0:
            if total_sum == 0:
                combinations.append(list(current_combination))
            return
        for i in range(total_sum + 1):
            current_combination.append(i)
            generate_combinations_helper(total_sum - i, num_terms - 1, current_combination)
            current_combination.pop()

    combinations = []
    generate_combinations_helper(total_sum, num_terms, [])
    return combinations


def chain_of_operands(length,type):
    if type == "mul":
        new_node = OperatorNode(Token("operator","mul"))
    elif type == "plus":
        new_node = OperatorNode(Token("operator","plus"))
    else:
        new_node = OperatorNode(Token("operator","mul"))


    tmp = new_node
    for i in range(length - 1):
        tmp.left_child = OperatorNode(Token("operator","mul"))
        tmp = tmp.left_child
    return new_node

def sign_switch(sign):
    if sign == "plus":
        return "minus"
    return "plus"

# only for integer power
# power > 1
# (a+b+c)^3 = a^3+b^3+c^3+a*b^2....
def multinomial_theorem(node):
    power = int(node.right_child.value.value)
    terms_and_signs = []
    tmp = node.left_child
    while isinstance(tmp,OperatorNode) and (tmp.type == "plus" or tmp.type == "minus"):
        if tmp.type == "plus":
            terms_and_signs.append(TermAndSign(tmp.right_child,"plus"))
        else:
            terms_and_signs.append(TermAndSign(tmp.right_child,"minus"))
        tmp = tmp.left_child
    terms_and_signs.append(TermAndSign(tmp, "plus"))
    combinations = generate_combinations(power,len(terms_and_signs))
    final_nodes = []
    for i in combinations:
        count_not_zero = sum(1 for item in i if item > 0)
        if count_not_zero == 1:
            #if there is only one x,y,... in this term
            for j in range(len(i)):
                if (i[j] != 0):
                    tmp = OperatorNode(Token("operator","exp"))
                    tmp.left_child = copy.deepcopy(terms_and_signs[j].term)
                    tmp.right_child = OperandNode(Token("int",i[j]))
                    sign = "plus"
                    if(terms_and_signs[j].sign == "minus" and i[j] % 2 == 1):
                        sign = "minus"
                    final_nodes.append(TermAndSign(tmp,sign))
                    break
        else:
            new_node = chain_of_operands(count_not_zero -1,"mul")
            tmp = new_node
            sign = "plus"
            for j in range(len(i)):

                if (i[j] != 0):
                    # last x,y,...
                    if(tmp.left_child  == None):
                        if (i[j] == 1):
                            tmp.right_child = copy.deepcopy(terms_and_signs[j].term)
                            if terms_and_signs[j].sign == "minus":
                                sign = sign_switch(sign)
                        else:
                            tmp.right_child = OperatorNode(Token("operator", "exp"))
                            tmp.right_child.left_child = copy.deepcopy(terms_and_signs[j].term)
                            tmp.right_child.right_child = OperandNode(Token("int", i[j]))
                            if (terms_and_signs[j].term == "minus" and i[j] % 2 == 1):
                                sign = sign_switch(sign)
                        #find ne last and get it to left
                        for k in range(j+1,len(i)):
                            if (i[k] == 1):
                                tmp.left_child = copy.deepcopy(terms_and_signs[k].term)
                                if terms_and_signs[k].sign == "minus":
                                    sign = sign_switch(sign)
                            elif i[k] > 1:
                                tmp.left_child = OperatorNode(Token("operator", "exp"))
                                tmp.left_child.left_child = copy.deepcopy(terms_and_signs[k].term)
                                tmp.left_child.right_child = OperandNode(Token("int", i[k]))
                                if (terms_and_signs[k].term == "minus" and i[k] % 2 == 1):
                                    sign = sign_switch(sign)
                            else:
                                continue
                        break
                    if (i[j] == 1):
                        tmp.right_child = copy.deepcopy(terms_and_signs[j].term)
                        if terms_and_signs[j].sign == "minus":
                            sign = sign_switch(sign)
                    else:
                        tmp.right_child = OperatorNode(Token("operator", "exp"))
                        tmp.right_child.left_child = copy.deepcopy(terms_and_signs[j].term)
                        tmp.right_child.right_child = OperandNode(Token("int", i[j]))
                        if(terms_and_signs[j].term == "minus" and i[j] % 2 == 1):
                            sign = sign_switch(sign)
                    tmp = tmp.left_child

            #add coeficient
            if  isinstance(new_node,OperatorNode) and new_node.type == "mul":
                numerator = math.factorial(power)
                denumenator = 1
                for l in i :
                    if l > 1:
                        denumenator = denumenator * math.factorial(l)
                coeficient = numerator/denumenator
                newer_node = OperatorNode(Token("operator","mul"))
                newer_node.left_child = new_node
                newer_node.right_child = OperandNode(Token("int",int(coeficient)))
                final_nodes.append(TermAndSign(newer_node,sign))
            else:
                final_nodes.append(TermAndSign(new_node,sign))

    #now get all the terms together
    # for i in final_nodes:
    #     print(printTree(i.term),i.sign)
    #get posivite sign at the end
    for i in range(len(final_nodes)):
        if final_nodes[i].sign == "plus":
            term = final_nodes.pop(i)
            final_nodes.append(term)
            break


    new_node = None
    tmp = None
    for i in range(len(final_nodes)):
        #the first node
        if i == 0:
            if final_nodes[i].sign == "plus":
                new_node = OperatorNode(Token("operator","plus"))
            else:
                new_node = OperatorNode(Token("operator","minus"))
            new_node.right_child = final_nodes[i].term
            tmp = new_node
        elif i == len(final_nodes)-1:
            tmp.left_child = final_nodes[i].term
        else:
            if final_nodes[i].sign == "plus":
                tmp.left_child = OperatorNode(Token("operator", "plus"))
            else:
                tmp.left_child = OperatorNode(Token("operator", "minus"))
            tmp.left_child.right_child = final_nodes[i].term
            tmp = tmp.left_child
    return new_node

