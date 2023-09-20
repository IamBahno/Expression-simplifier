from calc_logic.expression_solver.syntax_analysis import *
from calc_logic.expression_solver.expression_tree import ExpressionTree
from calc_logic.expression_solver.tree_nodes.expression_node import ExpressionNode
import time

TIME_LIMIT = 10

#TODO priority queue

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

    expanded_solution = strom
    expanded_score = ExpressionNode.expandedSolutionScore(expanded_solution.root)

    time_limit = TIME_LIMIT
    start_time = time.time()

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
            return [best_solution_yet,expanded_solution]
        strom = stromy_to_do.pop(0)
        while strom.isTreeAlreadyDone():
            if(len(stromy_to_do) == 0):
                return [best_solution_yet, expanded_solution]
            strom = stromy_to_do.pop(0)

        # if counter == 0:
        #     pass
            # exit(1)

        print("lol" + printTree(strom.root))

        strom.generatePathAndRules(strom.root,"")
        #end if is best, remake to coplex function later
        if(ExpressionNode.countNode(strom.root) <= number_of_nodes_yet):
            best_solution_yet = strom
            number_of_nodes_yet = ExpressionNode.countNode(strom.root)
        if(ExpressionNode.expandedSolutionScore(strom.root) > expanded_score):
            expanded_solution = strom
            expanded_score = ExpressionNode.expandedSolutionScore(strom.root)

        if(strom.path_and_rules==[]):
            return [strom,expanded_solution]

        # Check if the time limit has been reached
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time >= time_limit:
            print("time_limit")
            break  # Exit the loop if the time limit is reached

        
    return [best_solution_yet,expanded_solution]



def doTheThing(input):
    strom = prepareTreeFromInput(input)
    print(printTree(strom.root))

    stromy = solveExpression(strom)
    strom = stromy[0]
    expanded_strom = stromy[1]
    print(printTree(strom.root))
    print("expanded" + printTree(expanded_strom.root))
    stromy = [strom]

    #best strom
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
    #######

    expanded_stromy = [expanded_strom]
    #expanded strom
    if expanded_strom != strom:
        prevTree = ExpressionTree.getFinishedTree(expanded_strom.father_tree_id)
        while True and prevTree != None:
            expanded_stromy.append(prevTree)
            if (prevTree.id == 0):
                break
            prevTree = ExpressionTree.getFinishedTree(prevTree.father_tree_id)

        stringExpandedStromy = []

        for i in expanded_stromy:
            str = ExpressionTree.treeToInfix(i.root)
            str = ExpressionTree.getRidOfBrakcets(str)
            stringExpandedStromy.append(str)

        stringExpandedStromy.reverse()

        print("program successful end 2")
        return [stringStromy,stringExpandedStromy]


    print("program successful end")
    return stringStromy
