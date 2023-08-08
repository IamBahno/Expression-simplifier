from syntax_analysis import *

def prepareTreeFromInput():
    analyser = SyntaxAnalysis()
    analyser.loadTokens()
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
            strom = stromy_to_do.pop(0)
        strom.generatePathAndRules(strom.root,"")

        
    return strom

strom = prepareTreeFromInput()


print(printTree(strom.root))

strom = solveExpression(strom)

print(printTree(strom.root))

print(ExpressionTree.treeToInfix(strom.root))

