from calc_logic.expression_solver.tree_nodes.expression_node import OperatorNode
from calc_logic.expression_solver.tree_nodes.expression_node import OperandNode
from calc_logic.expression_solver.tree_nodes.expression_node import FunctionNode
from calc_logic.lex_analysis import Token
from calc_logic.expression_solver.values.values import FloatValue
from calc_logic.expression_solver.values.values import IntegerValue
from calc_logic.expression_solver.values.values import VarValue
from calc_logic.expression_solver.PathAndRule import Rules
from calc_logic.expression_solver.rules.utils import isMultiplicationWithOnePresent




def checkForDivToMul(node):
    if(isinstance(node,OperatorNode) and node.type == "div"):
        if(isinstance(node.left_child,OperandNode) and (node.left_child.type == "int" or node.left_child.type == "float") and node.left_child.value.value == 1):
            return []
        converPerPartes = True
        tmp = node.left_child
        while isinstance(tmp,OperatorNode):
            if(isinstance(tmp,OperatorNode) and tmp.type != "mul"):
                converPerPartes = False
                break
            tmp = tmp.left_child

        if(converPerPartes == False):
            return [Rules("div_to_mul_whole_top")]
        else:
            ret = [Rules("div_to_mul_whole_top")]
            ret_str = "div_to_mul"
            operand_count = 1
            tmp = node.left_child
            while isinstance(tmp, OperatorNode):
                ret_str = ret_str + str(operand_count)
                operand_count += 1
                ret.append(Rules(ret_str))
                tmp = tmp.left_child
            return ret


    return []


def divToMul(node,rule):
    if rule.type == "div_to_mul_whole_top":
        #to prevent infinite loop
        if isMultiplicationWithOnePresent(node):
            return node
        new_node = OperatorNode(Token("operator","mul"))
        new_node.right_child = node.left_child
        new_node_left = OperatorNode(Token("operator","div"))
        new_node.left_child = new_node_left
        new_node_left.left_child = OperandNode(Token("int",1))
        new_node_left.right_child = node.right_child
        return new_node
    else:
        guide_string = rule.type[len("div_to_mul"):]
        node_list = []
        tmp = node.left_child
        while isinstance(tmp,OperatorNode):
            node_list.append(tmp.right_child)
            tmp = tmp.left_child
        node_list.append(tmp)
        node_list.reverse()

        new_node = OperatorNode(Token("operator","mul"))
        #prava strana
        if(len(guide_string) == 1):
            new_node.right_child = node_list[0]
        elif len(guide_string) == 2:
            new_node.right_child = OperatorNode(Token("operator","mul"))
            new_node.right_child.left_child = node_list[0]
            new_node.right_child.right_child = node_list[1]
        else:
            new_node.right_child = OperatorNode(Token("operator","mul"))
            new_node.right_child.right_child = node_list[0]

            tmp = new_node.right_child # ukazuje na mul
            for i in node_list[1:len(guide_string)-1]:
                tmp.left_child = OperatorNode(Token("operator","mul"))
                tmp .left_child.right_child = i
                tmp = tmp.left_child
            tmp.left_child = node_list[len(guide_string)-1]

        new_node.left_child = OperatorNode(Token("operator","div"))
        new_node.left_child.right_child = node.right_child


        if(len(node_list) - len(guide_string)) == 1:
            new_node.left_child.left_child = node_list[len(node_list) - 1]
        elif(len(node_list) - len(guide_string)) == 2:
            new_node.left_child.left_child = OperatorNode(Token("operator","mul"))
            new_node.left_child.left_child.left_child = node_list[len(node_list) - 2]
            new_node.left_child.left_child.right_child = node_list[len(node_list) - 1]
        else:
            new_node.left_child.left_child = OperatorNode(Token("operator","mul"))
            new_node.left_child.left_child.right_child = node_list[len(guide_string)]
            tmp = new_node.left_child.left_child
            for i in node_list[len(guide_string)+1:]:
                tmp.left_child = OperatorNode(Token("operator","mul"))
                tmp.left_child.right_child = i
                tmp = tmp.left_child
            tmp.left_child = node_list[len(node_list)-1]
        return new_node

