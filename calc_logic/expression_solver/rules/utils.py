from calc_logic.expression_solver.tree_nodes.expression_node import OperandNode
from calc_logic.expression_solver.tree_nodes.expression_node import OperatorNode
from calc_logic.expression_solver.tree_nodes.expression_node import FunctionNode
from calc_logic.lex_analysis import Token


#0 - x
def zeroMinusVar(node):
    new_node = OperandNode(Token("var",node.right_child.value.name))
    if(node.right_child.value.sign == "plus"):
        new_node.value.sign = "minus"
    else:
        new_node.value.sign = "plus"
    return new_node

# node * (-1)
def minusExpresions(node):
    if(isinstance(node,OperandNode)):
        if node.type == "var":
            tmp = OperatorNode(Token("operator","minus"))
            tmp.right_child = node
            node = zeroMinusVar(tmp)
        elif node.type == "float" or node.type == "int":
            node.value.value = node.value.value * (-1)
    elif(isinstance(node,FunctionNode)):
        new_node = OperatorNode(Token("operator","minus"))
        new_node.left_child = OperandNode(Token("int",0))
        new_node.right_child = node
        node = new_node
    #expression
    else:
        new_node = OperatorNode(Token("operator","mul"))
        new_node.left_child = OperandNode(Token("int",-1))
        new_node.right_child = node
        node = new_node
    return node

# a * x * y
def isXMulSmthing(node,var_and_const):
    if(isinstance(node,OperatorNode) and node.type == "mul"):
        if(isinstance(node.left_child,OperandNode) and isinstance(node.right_child,OperandNode)):
            if(node.left_child.type == "var" and node.right_child.type == "var"):
                var_and_const.vars.append(node.left_child.value.name)
                var_and_const.vars.append(node.right_child.value.name)
            elif(node.left_child.type == "var" and (node.right_child.type == "int" or node.right_child.type == "float")):
                var_and_const.vars.append(node.left_child.value.name)
                var_and_const.number = True
            elif(node.right_child.type == "var" and (node.left_child.type == "int" or node.left_child.type == "float")):
                var_and_const.vars.append(node.right_child.value.name)
                var_and_const.number = True
            else:
                var_and_const.number = True

        elif(isinstance(node.left_child,OperandNode) and isinstance(node.right_child,OperatorNode)) or \
                (isinstance(node.left_child,OperatorNode) and isinstance(node.right_child,OperandNode)):
            if(isinstance(node.left_child,OperandNode) and isinstance(node.right_child,OperatorNode)):
                if(node.left_child.type == "var"):
                    var_and_const.vars.append(node.left_child.value.name)
                else:
                    var_and_const.number = True
                isXMulSmthing(node.right_child,var_and_const)
            else:
                if(node.right_child.type == "var"):
                    var_and_const.vars.append(node.right_child.value.name)
                else:
                    var_and_const.number = True
                isXMulSmthing(node.left_child,var_and_const)
        else:
            var_and_const.legit = False
    else:
        var_and_const.legit = False

def treeEqual(original_node,compare_to):
    if(type(original_node) != type(compare_to)):
        return False
    if(isinstance(original_node,OperatorNode)):
        if(original_node.type == compare_to.type):
            return True and treeEqual(original_node.left_child,compare_to.left_child) and treeEqual(original_node.right_child,compare_to.right_child)
        else:
            return False
    if(isinstance(original_node,OperandNode)):
        if(original_node.type == compare_to.type):
            if(original_node.type == "var"):
                if(original_node.value.name == compare_to.value.name):
                    return True
                else:
                    return False

            if(original_node.value.value == compare_to.value.value):
                return True
            else:
                return False
        else:
            return False
    if(isinstance(original_node,FunctionNode)):
        if(original_node.value == compare_to.value):
            return True and treeEqual(original_node.child,compare_to.child)
        else:
            return False

def isMultiplicationWithOnePresent(node):
    if(isinstance(node,OperatorNode) or node.type == "mul"):
        return isMultiplicationWithOnePresent(node.left_child) or isMultiplicationWithOnePresent(node.right_child)
    elif (isinstance(node,OperatorNode) or node.type == "div"):
        return isMultiplicationWithOnePresent(node.left_child)
    elif(isinstance(node,OperandNode) and (node.type == "int" or node.type == "float")):
        if(node.value.value == 1 or node.value.value ==0):
            return True
        else:
            return False
    elif(isinstance(node,FunctionNode)):
        return False
    else:
        return False

# "minus-one-mul-var","var-mul-minus-one"
def minusOneMulVar(node,rule):
    tmp = None
    if rule.type == "minus-one-mul-var":
        tmp = node.right_child
    else:
        tmp = node.left_child
    if tmp.value.sign == "plus":
        tmp.value.sign = "minus"
    else:
        tmp.value.sign = "plus"
    return tmp


def isNegNumOrVar(node):
    if isinstance(node,OperandNode):
        if node.type == "int" or node.type == "float":
            if node.value.value < 0:
                return True
        else:
            if node.value.sign == "minus":
                return True
    else:
        return False


#goes thought node, looks if there is negative num or var to take out
def isThereNegatavive(node):
    tmp = node
    while True:
        while isinstance(tmp,OperatorNode) and tmp.type == "mul":
            if isNegNumOrVar(tmp.right_child):
                return True
            tmp = tmp.left_child
        if isinstance(tmp,OperatorNode) and node.type == "exp":
            if isinstance(tmp, OperandNode):
                if isNegNumOrVar(tmp.left_child):
                    return True
                else:
                    return False
            else:
                tmp = tmp.left_child
                continue
        elif isinstance(tmp,OperatorNode) and node.type == "div":
            return isThereNegatavive(tmp.left_child) or isThereNegatavive(tmp.right_child)
        elif isinstance(tmp, OperatorNode):
            return False
        elif isinstance(tmp,OperandNode):
            if isNegNumOrVar(tmp):
                return True
        else:
            return False
        return False

#x => -x, -3 => 3
def negOperand(node):
    if node.type == "int" or node.type == "float":
        node.value.value = node.value.value * (-1)
    else:
        if node.value.sign == "plus":
            node.value.sign = "minus"
        else:
            node.value.sign = "plus"
