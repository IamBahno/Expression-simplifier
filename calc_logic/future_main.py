from calc_logic.expression_solver.syntax_analysis import *
from calc_logic.expression_solver.expression_tree import ExpressionTree
from calc_logic.expression_solver.tree_nodes.expression_node import ExpressionNode
from calc_logic.expression_solver.tree_rule_val import ListOfTreeRuleValues
import time

TIME_LIMIT = 10


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
    stromy_to_do = strom.gen_first_generation()

    best_solution_yet = strom
    number_of_nodes_yet = ExpressionNode.countNode(best_solution_yet.root)

    expanded_solution = strom
    expanded_score = ExpressionNode.expandedSolutionScore(expanded_solution.root)

    time_limit = TIME_LIMIT
    start_time = time.time()

    # counter = 0
    while(True):
        # counter = counter +1
        # if counter == 7:
        #     exit(1)
        try:
            tree_rule_val = stromy_to_do.pop()
        except:
            return [best_solution_yet,expanded_solution]

        new_tree,new_gen = ExpressionTree.generateNextGeneration(tree_rule_val)
        if new_tree == "done":
            continue
        for i in new_gen:
            stromy_to_do.insert(i)
        if stromy_to_do == []:
            return [best_solution_yet,expanded_solution]


        #end if is best, remake to coplex function later
        if(ExpressionNode.countNode(new_tree.root) <= number_of_nodes_yet):
            best_solution_yet = new_tree
            number_of_nodes_yet = ExpressionNode.countNode(new_tree.root)
        if(ExpressionNode.expandedSolutionScore(new_tree.root) > expanded_score):
            expanded_solution = new_tree
            expanded_score = ExpressionNode.expandedSolutionScore(new_tree.root)


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
