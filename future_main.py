from syntax_analysis import *

def prepareTreeFromInput(input):
    analyser = SyntaxAnalysis()
    analyser.loadTokens(input)
    analyser.checkSyntax()
    analyser.infixToPrefix()
    strom = ExpressionTree(analyser.token_list)
    strom.root = strom.constructTree()
    return strom

def solveExpression(strom):
    strom.generatePathAndRules(strom.root,"")
    stromy_to_do = []
    while(strom.path_and_rules != []):
        stromy_to_do.extend( strom.generateNextGeneration())
        strom = stromy_to_do.pop(0)

        while strom.isTreeAlreadyDone():
            if(len(stromy_to_do) == 0):
                return  strom
            strom = stromy_to_do.pop(0)

        strom.generatePathAndRules(strom.root,"")


        #end if tree cannot be expend, remake to coplex function later
        if(strom.path_and_rules == []):
            return strom

        
    return strom

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
