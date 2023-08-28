from syntax_analysis import *

def prepareTreeFromInput(input):
    analyser = SyntaxAnalysis()
    analyser.loadTokens(input)
    analyser.checkSyntax()
    analyser.checkForMinus()
    analyser.infixToPrefix()
    strom = ExpressionTree(analyser.token_list)
    strom.root = strom.constructTree()
    return strom

def solveExpression(strom):
    strom.generatePathAndRules(strom.root,"")
    stromy_to_do = []
    best_solution_yet = strom
    number_of_nodes_yet = ExpressionNode.countNode(best_solution_yet.root)

    # counter = 20
    while(True):
        # counter = counter -1
        # if(strom.path_and_rules == []):
        #     if(stromy_to_do != []):
        #         strom = stromy_to_do.pop(0)
        #     else:
        #         break
        stromy_to_do.extend( strom.generateNextGeneration())
        if(stromy_to_do == []):
            return  best_solution_yet
        strom = stromy_to_do.pop(0)
        while strom.isTreeAlreadyDone():
            if(len(stromy_to_do) == 0):
                return best_solution_yet
            strom = stromy_to_do.pop(0)

        # if counter == 0:
        #     pass
        #     # exit(1)

        strom.generatePathAndRules(strom.root,"")
        #end if is best, remake to coplex function later
        if(ExpressionNode.countNode(strom.root) <= number_of_nodes_yet):
            best_solution_yet = strom
            number_of_nodes_yet = ExpressionNode.countNode(strom.root)
        if(strom.path_and_rules==[]):
            return strom

        
    return best_solution_yet

# strom = prepareTreeFromInput()
#
# strom = solveExpression(strom)
#
# stromy = [strom]
# while True:
#     prevTree = ExpressionTree.getFinishedTree(strom.father_tree_id)
#     stromy.append(prevTree)
#     if(prevTree.id == 0):
#         break

def doTheThing(input):
    strom = prepareTreeFromInput(input)
    print(printTree(strom.root))

    strom = solveExpression(strom)
    print(printTree(strom.root))
    stromy = [strom]
    prevTree = ExpressionTree.getFinishedTree(strom.father_tree_id)
    while True and prevTree != None:
        stromy.append(prevTree)
        if (prevTree.id == 0):
            break
        prevTree = ExpressionTree.getFinishedTree(prevTree.father_tree_id)

    stringStromy = []

    for i in stromy:
        str = ExpressionTree.treeToInfix(i.root)
        str = ExpressionTree.getRidOfBrakcets(str)
        stringStromy.append(str)

    stringStromy.reverse()

    print("program successful end")
    return stringStromy
