from calc_logic.expression_solver.tree_nodes.expression_node import FunctionNode
from calc_logic.expression_solver.tree_nodes.expression_node import OperandNode
from calc_logic.expression_solver.tree_nodes.expression_node import OperatorNode
def printToken(token):
    print(f"Type:{token.type},  Value: {token.value}")

def printTree(root):
    if(isinstance(root,FunctionNode)):
        return f"(Funkce:{root.type},argument:({printTree(root.child)}))"
    elif(isinstance(root,OperatorNode)):
        return f"[Operator:{root.type},leva_strana:{printTree(root.left_child)},prava_strana:{printTree(root.right_child)}]"

    elif(isinstance(root,OperandNode)):
        if(root.type == "var"):
            if(root.value.sign == "minus"):
                return f"<Operand:{root.type},value:-{root.value.name}>"
            else:
                return f"<Operand:{root.type},value:{root.value.name}>"
        else:
            return f"<Operand:{root.type},value:{root.value.value}>"
    else:
        print("error_print_Tree")