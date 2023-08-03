import lex_analysis


def printToken(token):
    print(f"Type:{token.type},  Value: {token.value}")

# def printTree(root):
#     if(isinstance(root,FunctionNode)):
#         print(f"(Funkce:{root.type},argument:({printTree(root.child)}))")
#     elif(isinstance(root,OperatorNode)):
#         print(f"[Operator:{root.type},leva_strana:{printTree(root.left_child)},prava_strana:{printTree(root.right_child)}]")
#     elif(isinstance(root,OperandNode)):
#         if(root.type == "var"):
#             print(f"<Operand:{root.type},value:{root.value.name}>")
#         else:
#             print(f"<Operand:{root.type},value:{root.value.value}>")
    