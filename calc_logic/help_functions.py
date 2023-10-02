from calc_logic.expression_solver.expression_tree import ExpressionTree

def getListOfAncestors(tree):
    trees = [tree]

    #best strom
    prevTree = ExpressionTree.getFinishedTree(tree.father_tree_id)
    while True and prevTree != None:
        if prevTree.rule_applied_to_get.type.find("shift") == -1:
            trees.append(prevTree)
        if (prevTree.id == 0):
            break
        prevTree = ExpressionTree.getFinishedTree(prevTree.father_tree_id)

    return trees

def listOfTreesToStrings(trees):
    stringStromy = []

    for i in trees:
        str = ExpressionTree.treeToInfix(i.root)
        str = ExpressionTree.getRidOfBrakcets(str)
        stringStromy.append(str)

    stringStromy.reverse()
    return stringStromy

