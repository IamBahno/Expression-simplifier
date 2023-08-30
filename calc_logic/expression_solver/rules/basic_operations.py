from calc_logic.expression_solver.values.values import VarValue
from calc_logic.expression_solver.tree_nodes.expression_node import OperatorNode
from calc_logic.expression_solver.tree_nodes.expression_node import OperandNode
# from calc_logic.expression_solver.syntax_analysis import FunctionNode
from calc_logic.lex_analysis import Token
from calc_logic.expression_solver.values.values import FloatValue
from calc_logic.expression_solver.values.values import IntegerValue
from calc_logic.expression_solver.values.values import VarValue
from calc_logic.expression_solver.PathAndRule import Rules

# returns rules: plus/minus/divide/multiply/exp
def checkForBasicOperations(node):

    #it is operand above 2 operators
    if isinstance(node, OperatorNode) and isinstance(node.left_child, OperandNode)  and isinstance(node.right_child, OperandNode):
        #both sides are variables
        # all but x^x
        if isinstance(node.left_child.value, VarValue) and isinstance(node.right_child.value, VarValue) and (node.left_child.value.name == node.right_child.value.name):
            if node.type == "plus":
                return [Rules("basic_plus")]
            if node.type == "minus":
                return [Rules("basic_minus")]
            if node.type == "div":
                return [Rules("basic_div")]
            if node.type == "mul":
                return [Rules("basic_mul")]
            return []


        #both sides are numbers
        #can do all operations
        if (isinstance(node.left_child.value, IntegerValue)or isinstance(node.left_child.value, FloatValue)) and (isinstance(node.right_child.value, IntegerValue) or isinstance(node.right_child.value, FloatValue)):
            if node.type == "plus":
                return [Rules("basic_plus")]
            if node.type == "minus":
                return [Rules("basic_minus")]
            if node.type == "div":
                return [Rules("basic_div")]
            if node.type == "mul":
                return [Rules("basic_mul")]
            if node.type == "exp":
                return [Rules("basic_exp")]

        # it is 0-x
        if(node.left_child.type in ["int","float"] and node.left_child.value.value == 0 and node.type == "minus"):
            return [Rules("zero-var")]

        if node.type == "mul":
            if node.left_child.type in ["int","float"] and node.left_child.value.value == -1 and node.right_child.type == "var":
                return [Rules("minus-one-mul-var")]
            if node.right_child.type in ["int","float"] and node.right_child.value.value == -1 and node.left_child.type == "var":
                return [Rules("var-mul-minus-one")]
        if node.type == "mul":
            if node.left_child.type in ["int","float"] and node.left_child.value.value == 1 and node.right_child.type == "var":
                return [Rules("one-mul-var")]
            if node.right_child.type in ["int","float"] and node.right_child.value.value == 1 and node.left_child.type == "var":
                return [Rules("var-mul-one")]
    return []

def applyBasicOperations(node,rule):
    #operations at variables
    new_node = None
    if(isinstance(node.left_child.value,VarValue)):
        if(rule.type == "basic_plus"):
            # x+x = 2*x
            # (-x)+(-x) = -2*x
            if(node.left_child.value.sign == node.right_child.value.sign):
                new_node = OperatorNode(Token("operator","mul"))
                if(node.left_child.value.sign == "plus"):
                    new_node.left_child = OperandNode(Token("int",2))
                else:
                    new_node.left_child = OperandNode(Token("int",-2))
                new_node.right_child = OperandNode(Token("var",node.left_child.value.name))
                new_node.right_child.value.sign = "plus"
            # x+(-x), (-x)+x = 0
            else:
                new_node = OperandNode(Token("int",0))

        if(rule.type == "basic_minus"):
            # x - x = (-x)-(-x) = 0
            if(node.left_child.value.sign == node.right_child.value.sign):
                new_node = OperandNode(Token("int", 0))
            # -x - x = -2x
            # x - (-x) = 2x
            else:
                new_node = OperatorNode(Token("operator","mul"))
                if(node.left_child.value.sign == "plus"):
                    new_node.left_child = OperandNode(Token("int",2))
                else:
                    new_node.left_child = OperandNode(Token("int",-2))
                new_node.right_child = OperandNode(Token("var",node.left_child.value.name))
                new_node.right_child.value.sign = "plus"
        if(rule.type == "basic_div"):
            if(node.left_child.value.sign == node.right_child.value.sign):
                new_node = OperandNode(Token("int",1))
            else:
                new_node = OperandNode(Token("int",-1))
        if(rule.type == "basic_mul"):
            new_node = OperatorNode(Token("operator", "exp"))
            new_node.left_child = OperandNode(Token("var", node.left_child.value.name))
            # x*x = (-x)*(-x) = x^2
            if(node.left_child.value.sign == node.right_child.value.sign):
                new_node.right_child = OperandNode(Token("int",2))
            # (-x)*(x) = x*(-x) = -x^2
            else:
                new_node.right_child = OperandNode(Token("int",-2))


    #operations on numbers
    else:
        value = 0
        if(rule.type == "basic_plus"):
            value = node.left_child.value.value + node.right_child.value.value
        if(rule.type == "basic_minus"):
            value = node.left_child.value.value - node.right_child.value.value
        if(rule.type == "basic_mul"):
            value = node.left_child.value.value * node.right_child.value.value
        if(rule.type == "basic_div"):
            if(node.right_child.value.value == 0):
                return node
            value = node.left_child.value.value / node.right_child.value.value
        if(rule.type == "basic_exp"):
            value = node.left_child.value.value ** node.right_child.value.value

        if type(value) == int:
            new_node = OperandNode(Token("int",value))
        else:
            new_node = OperandNode(Token("float",value))




    return new_node