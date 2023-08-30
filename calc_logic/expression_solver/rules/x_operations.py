from calc_logic.expression_solver.tree_nodes.expression_node import OperatorNode
from calc_logic.expression_solver.tree_nodes.expression_node import OperandNode
from calc_logic.expression_solver.tree_nodes.expression_node import FunctionNode
from calc_logic.lex_analysis import Token
from calc_logic.expression_solver.values.values import FloatValue
from calc_logic.expression_solver.values.values import IntegerValue
from calc_logic.expression_solver.values.values import VarValue
from calc_logic.expression_solver.PathAndRule import Rules
from calc_logic.expression_solver.rules.utils import isXMulSmthing
from collections import Counter

class VarAndCoeficient:
    def __init__(self):
        self.legit = True
        self.vars = []
        self.number = False

# a*x + x
def checkForXOperations(node):
    operation = ""
    if(isinstance(node,OperatorNode) and (node.type == "plus" or node.type == "minus")):
        if(node.type == "plus"):
            operation = "plus"
        else:
            operation = "minus"
    else:
        return []
    left = VarAndCoeficient()
    right = VarAndCoeficient()

    if(isinstance(node.left_child,OperandNode) and node.left_child.type == "var"):
        left.vars.append(node.left_child.value.name)
    if(isinstance(node.right_child,OperandNode) and node.right_child.type == "var"):
        right.vars.append(node.right_child.value.name)
    # x o x
    if(left.vars != [] and right.vars != []):
        return []
    if(left.vars == [] and right.vars == []):
        isXMulSmthing(node.left_child,left)
        isXMulSmthing(node.right_child,right)
        if(left.legit == False or right.legit == False):
            return []
        if(Counter(left.vars) == Counter(right.vars)):
            if(left.vars) == []:
                return []
            if operation == "minus":
                return [Rules("node-minus-node")]
            else:
                return [Rules("node-plus-node")]

        else:
            return []

    elif(left.vars == [] and right.vars != []):
        isXMulSmthing(node.left_child,left)
        if(left.legit == True):
            if len(left.vars) != 1:
                return []
            if left.vars[0] != node.right_child.value.name:
                return []
            else:
                if operation == "minus":
                    #node meaning a*x or y*x
                    return [Rules("node-minus-var")]
                else:
                    return [Rules("node-plus-var")]

        else:
            return []
    else:
        isXMulSmthing(node.right_child,right)
        if(right.legit == True and right.number == True):
            if len(right.vars) != 1:
                return []
            if right.vars[0] != node.left_child.value.name:
                return []
            else:
                if operation == "minus":
                    return [Rules("var-minus-node")]
                else:
                    return [Rules("var-plus-node")]
        else:
            return []

    return []

def applyXOperations(node,rule):
    operation = ""
    left_val = 0
    right_val = 0
    if(rule.type.find("minus") != -1):
        operation = "minus"
    else:
        operation = "plus"
    if(rule.type[:3] == "var"):
        if(node.left_child.value.sign == "minus"):
            left_val = -1
        else:
            left_val = 1

    else:
        val = HoldValue(1)
        val.mulValTogether(node.left_child)
        left_val = val.value

    tmp = rule.type[rule.type.index('-')+1:]
    tmp = tmp[tmp.index('-')+1:]

    if(tmp[:3] == "var"):
        if(node.right_child.value.sign == "minus"):
            right_val = -1
        else:
            right_val = 1
    else:
        val = HoldValue(1)
        val.mulValTogether(node.right_child)
        right_val = val.value



    final_val = 0
    if(operation == "plus"):
        final_val = left_val + right_val
    else:
        final_val = left_val - right_val

    names = getVarNames(node.left_child)

    if(final_val == 0):
        return OperandNode(Token("int",0))

    new_node = OperatorNode(Token("operator","mul"))
    if(len(names) == 1):
        new_node.left_child = OperandNode(Token("var",names[0]))
        if(isinstance(final_val,int)):
            new_node.right_child = OperandNode(Token("int",final_val))
        else:
            new_node.right_child = OperandNode(Token("float",final_val))
        return new_node

    tmp = new_node
    #there is more than one var

    for i in names[1:]:
        tmp.left_child = OperatorNode(Token("operator","mul"))
        tmp = tmp.left_child
    tmp = new_node
    while True:
        if(len(names) == 1):
            tmp.right_child = OperandNode(Token("var", names[0]))
            if (isinstance(final_val, int)):
                tmp.left_child = OperandNode(Token("int", final_val))
            else:
                tmp.left_child = OperandNode(Token("float", final_val))
            break
        tmp.right_child = OperandNode(Token("var",names[0]))
        names = names[1:]
        tmp = tmp.left_child
    return new_node

class HoldValue():
    def __init__(self,value):
        self.value = value

    def mulValTogether(self,node):
        if isinstance(node,OperatorNode):
            if(isinstance(node.left_child,OperandNode) and (node.left_child.type == "int" or node.left_child.type == "float")):
                self.value = self.value * node.left_child.value.value
            if(isinstance(node.right_child,OperandNode) and (node.right_child.type == "int" or node.right_child.type == "float")):
                self.value = self.value * node.right_child.value.value
            if(isinstance(node.left_child,OperandNode) and node.left_child.type == "var" and node.left_child.value.sign == "minus"):
                self.value = self.value * (-1)
            if (isinstance(node.right_child,OperandNode) and node.right_child.type == "var" and node.right_child.value.sign == "minus"):
                self.value = self.value * (-1)
            if(isinstance(node.left_child,OperatorNode)):
                self.mulValTogether(node.left_child)
            if(isinstance(node.right_child,OperatorNode)):
                self.mulValTogether(node.right_child)

def getVarNames(node):
    if(isinstance(node,OperatorNode)):
        return getVarNames(node.left_child) + getVarNames(node.right_child)
    if(isinstance(node,OperandNode)):
        if node.type == "int" or node.type == "float":
            return ""
        return node.value.name
    return ""