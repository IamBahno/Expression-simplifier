from calc_logic.lex_analysis import Token,InputParser
from calc_logic.error import errorExit
from math import pi,e
import copy

from calc_logic.expression_solver.tree_nodes.expression_node import OperatorNode
from calc_logic.expression_solver.tree_nodes.expression_node import OperandNode
from calc_logic.expression_solver.tree_nodes.expression_node import FunctionNode
from calc_logic.expression_solver.tree_nodes.expression_node import ExpressionNode

import calc_logic.expression_solver.rules as RulePack
from calc_logic.expression_solver.PathAndRule import PathAndRule
from calc_logic.expression_solver.tree_rule_val import TreeRuleValue
from calc_logic.expression_solver.tree_rule_val import ListOfTreeRuleValues
from calc_logic.expression_solver.apply_rule import applyRule


class ExpressionTree():
    tree_counter = 0
    finished_trees = []

    def __init__(self, token_list):
        self.path_and_rules = []
        self.token_list = token_list
        self.root = None
        self.father_tree_id = 0
        self.id = 0
        self.rules_applied = 0
        self.rule_applied_to_get = ""

    # function constants converts  to floats
    def tokenToNode(token: Token) -> ExpressionNode:
        if token.type == "operator":
            return OperatorNode(token)
        elif token.type in ["int", "float", "var"]:
            return OperandNode(token)
        elif token.type == "func":
            if (token.value == "pi"):
                tmp = OperandNode(Token("float", pi))
                tmp.value.constant_value = "pi"
                return tmp
            elif (token.value == "exp"):
                tmp = OperandNode(Token("float", e))
                tmp.value.constant_value = "exp"
                return tmp
            else:
                if token.value not in ["sin", "cos","tg","ln"]:
                    return errorExit("Not known function error")
                else:
                    return FunctionNode(token)
        else:
            return OperandNode(token)

    def isClosed(root) -> True:
        if (isinstance(root, FunctionNode)):
            if (root.child == None):
                return False
            else:
                return ExpressionTree.isClosed(root.child)
        elif (isinstance(root, OperandNode)):
            return True
        elif (isinstance(root, OperatorNode)):
            if (root.left_child == None or root.right_child == None):
                return False
            else:
                return ExpressionTree.isClosed(root.left_child) and ExpressionTree.isClosed(root.right_child)
        else:
            return False

    def addNodeToOpen(root, new_node) -> ExpressionNode:
        if (isinstance(root, FunctionNode)):
            if (root.child == None):
                root.child = new_node
            else:
                root.child = ExpressionTree.addNodeToOpen(root.child, new_node)
        elif (isinstance(root, OperatorNode)):
            if (root.left_child == None):
                root.left_child = new_node
            elif (ExpressionTree.isClosed(root.left_child) == False):
                root.left_child = ExpressionTree.addNodeToOpen(root.left_child, new_node)
            elif (root.right_child == None):
                root.right_child = new_node
            elif (ExpressionTree.isClosed(root.right_child) == False):
                root.right_child = ExpressionTree.addNodeToOpen(root.right_child, new_node)
            else:
                errorExit("Adding node to close operator")
        elif (isinstance(root, OperandNode)):
            errorExit("Adding node to operand")
        else:
            errorExit("unknown problem")
        return root

    def tokenListToNodeList(tokenList):
        nodeList = []
        for i in tokenList:
            nodeList.append(ExpressionTree.tokenToNode(i))
        return nodeList

    def constructTree(self) -> ExpressionNode:
        nodeList = ExpressionTree.tokenListToNodeList(self.token_list)
        root = nodeList.pop(0)
        for i in range(len(nodeList)):
            if (ExpressionTree.isClosed(root)):
                break
            root = ExpressionTree.addNodeToOpen(root, nodeList.pop(0))

        if nodeList != []:
            errorExit("wrong syntax of expression")
        return root

    def generatePathAndRules(self, node, path):
        rules = generateRules(node)
        for i in rules:
            self.path_and_rules.append(PathAndRule(path, i))
        if (isinstance(node, OperandNode)):
            return
        elif (isinstance(node, OperatorNode)):
            self.generatePathAndRules(node.left_child, path + "l")
            self.generatePathAndRules(node.right_child, path + "r")
        elif (isinstance(node, FunctionNode)):
            self.generatePathAndRules(node.child, path + "d")

    # modify given tree
    def applyRuleOnTree(self, path_and_rule):
        if (path_and_rule.path == ""):
            self.root = applyRule(self.root, path_and_rule.rule)
            return
        node_to_expend = self.root
        # loop until the next node is to expend
        i = 0
        while i != len(path_and_rule.path) - 1:
            if (path_and_rule.path[i] == 'l'):
                node_to_expend = node_to_expend.left_child
            elif (path_and_rule.path[i] == 'r'):
                node_to_expend = node_to_expend.right_child
            elif (path_and_rule.path[i] == 'd'):
                node_to_expend = node_to_expend.child
            i += 1
        # sem to spadne vzdycky (snad)
        if (len(path_and_rule.path) - i == 1):
            if (path_and_rule.path[i] == "l"):
                node_to_expend.left_child = applyRule(node_to_expend.left_child, path_and_rule.rule)
            elif (path_and_rule.path[i] == "r"):
                node_to_expend.right_child = applyRule(node_to_expend.right_child, path_and_rule.rule)
            elif (path_and_rule.path[i] == "d"):
                node_to_expend.child = applyRule(node_to_expend.child, path_and_rule.rule)
            return

    def isTreeAlreadyDone(self):
        for i in ExpressionTree.finished_trees:
            if (RulePack.utils.treeEqual(self.root, i.root)):
                return True
        return False

    # takes TreeRuleValue execute the rule
    # find rules and paths in new strom
    # return tree and list of new TreeRuleValue
    @staticmethod
    def generateNextGeneration(self : TreeRuleValue):

        new_tree = copy.deepcopy(self.tree)
        new_tree.applyRuleOnTree(self.rule_and_path)
        if new_tree.isTreeAlreadyDone():
            return "done",None
        new_tree.rules_applied += 1
        new_tree.path_and_rules = []
        new_tree.rule_applied_to_get = self.rule_and_path.rule
        ExpressionTree.tree_counter += 1
        new_tree.id = ExpressionTree.tree_counter
        new_tree.father_tree_id = self.tree.id
        ExpressionTree.finished_trees.append(new_tree)

        new_TreeRuleVals = []
        new_tree.generatePathAndRules(new_tree.root,"")
        for i in new_tree.path_and_rules:
            new_TreeRuleVals.append(TreeRuleValue(new_tree,i)) #new tree is just reference

        return new_tree,new_TreeRuleVals

    def gen_first_generation(self):
        self.generatePathAndRules(self.root,"")
        new_gen = ListOfTreeRuleValues()
        for i in self.path_and_rules:
            new_gen.insert(TreeRuleValue(self,i))
        return new_gen






    def getRidOfBrakcets(str):
        without_brackets = False
        while without_brackets == False:
            without_brackets = True
            for i in range(1, len(str)):
                if (i == len(str) - 1):
                    continue
                if (str[i - 1] == '(' and str[i + 1] == ')'):
                    str = str[:i - 1] + str[i] + str[i + 2:]
                    without_brackets = False
                    break
        return str

    # tree to infix
    def treeToInfix(root: ExpressionNode):
        if (isinstance(root, OperandNode)):
            if (root.type == "int" or root.type == "float"):
                return str(root.value.value)
            else:
                if (root.value.sign == "minus"):
                    return f"-{root.value.name}"
                else:
                    return f"{root.value.name}"
        if (isinstance(root, OperatorNode)):
            if (root.type == 'plus'):
                return f"{ExpressionTree.treeToInfix(root.left_child)} + ({ExpressionTree.treeToInfix(root.right_child)})"
            if (root.type == 'minus'):
                return f"{ExpressionTree.treeToInfix(root.left_child)} - ({ExpressionTree.treeToInfix(root.right_child)})"
            if (root.type == 'mul'):
                return f"({ExpressionTree.treeToInfix(root.left_child)}) * ({ExpressionTree.treeToInfix(root.right_child)})"
            if (root.type == 'div'):
                return f"({ExpressionTree.treeToInfix(root.left_child)}) / ({ExpressionTree.treeToInfix(root.right_child)})"
            if (root.type == 'exp'):
                return f"({ExpressionTree.treeToInfix(root.left_child)}) ^ ({ExpressionTree.treeToInfix(root.right_child)})"
            if (root.type == 'equal'):
                return f"{ExpressionTree.treeToInfix(root.left_child)} = {ExpressionTree.treeToInfix(root.right_child)}"
        if (isinstance(root, FunctionNode)):
            return f"{root.type}({ExpressionTree.treeToInfix(root.child)})"

        return ""

    def getFinishedTree(id):
        for i in ExpressionTree.finished_trees:
            if i.id == id:
                return i


def generateRules(node:ExpressionNode):
    rules = []

    rules.extend(RulePack.checkForBasicOperations(node))
    rules.extend(RulePack.checkForOperandShift(node))
    rules.extend(RulePack.checkForXOperations(node))
    rules.extend(RulePack.checkForDivToMul(node))
    rules.extend(RulePack.checkForBrackMulDiv(node))
    rules.extend(RulePack.checkForExponentMulDiv(node))
    rules.extend(RulePack.checkForCommutativeProperty(node))
    rules.extend(RulePack.checkForMinusParentheses(node))
    rules.extend(RulePack.checkForOneAndZeroOperations(node))
    rules.extend(RulePack.checkForExpOfExpNode(node))
    rules.extend(RulePack.checkExpOfNode(node))

    rules.extend(RulePack.checkForNegativeExpToDiv(node))

    #unececery and broken
    # rules.extend(RulePack.checkForFractionCanceling(node))
    # rules.extend(RulePack.checkForMulOfFractCanceling(node))

    rules.extend(RulePack.check_for_multinomial(node))
    rules.extend(RulePack.checkForComputeFunc(node))

    return rules
