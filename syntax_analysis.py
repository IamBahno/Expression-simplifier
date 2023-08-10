from lex_analysis import Token,InputParser
import tools
from error import errorExit
from math import pi,e
import copy


def printTree(root):
    if(isinstance(root,FunctionNode)):
        return f"(Funkce:{root.type},argument:({printTree(root.child)}))"
    elif(isinstance(root,OperatorNode)):
        return f"[Operator:{root.type},leva_strana:{printTree(root.left_child)},prava_strana:{printTree(root.right_child)}]"

    elif(isinstance(root,OperandNode)):
        if(root.type == "var"):
            return f"<Operand:{root.type},value:{root.value.name}>"
        else:
            return f"<Operand:{root.type},value:{root.value.value}>"
    else:
        print("error")
def printToken(token):
    print(f"Type:{token.type},  Value: {token.value}")

#load tokens
#check syntax
#infix
#tree
class SyntaxAnalysis():
    def __init__(self):
        self.token_list = []

    def loadTokens(self,input):
        token = None
        InputParser.input = input + '\n'
        token = InputParser.GetToken()
        while(token.type != "eof_token" and token.type != "error_token"):
            # tools.printToken(token)
            self.token_list.append(token)
            token = InputParser.GetToken()
        if(token.type == "error_token"):
            errorExit("error token")

        if(token.type != "eof_token"):
            errorExit("missing eof")

    def checkSyntax(self):
        left_brack_counter = 0
        right_brack_counter = 0
        equal_counter = 0
        for i in self.token_list:
            if i.value == "left_brack":
                left_brack_counter += 1
            if i.value == "right_brack":
                right_brack_counter += 1
            if right_brack_counter > left_brack_counter:
                errorExit("right bracket without left")
            if i.value == "equal":
                equal_counter += 1
        if(left_brack_counter != right_brack_counter):
            errorExit("unmatching number of paranthesis")
        if(equal_counter > 1):
            errorExit('more then one "="')

    def operatorPriority(token):
        if token.value in ["equal"]:
            return 1
        if token.value in ["plus","minus"]: 
            return 2

        if token.value in ["mul","div"]:
            return 3

        if token.value in ["exp"]:
            return 4

        if token.value in ["left_brack","right_brack"]:
            return 5



    def infixToPrefix(self):
        #if therer is equal in expression i give parathesis at both sides

        for i in range(len(self.token_list)):
            if(self.token_list[i].value == "equal"):
                new_list = [Token("operator","left_brack")]
                new_list.extend(self.token_list[:i])
                new_list.extend([Token("operator","right_brack"),Token("operator","equal"),Token("operator","left_brack")])
                new_list.extend(self.token_list[i+1:])
                new_list.append(Token("operator","right_brack"))
                self.token_list = new_list
                break

        # zaporne cisla problem
        # for i in range(len(self.token_list)):
        #     if(self.token_list[i].value == "minus"):
        #         if(i == 0 or (self.token_list[i-1].type == "func" and (self.token_list[i-1].value != "exp" or self.token_list[i-1].value != "pi")) or self.token_list[i-1].type == "operator" ):
        #             new_list = []
        #             new_list.extend(self.token_list[:i])
        #             new_list.append(Token("int",0))
        #             new_list.extend(self.token_list[i:])
        #             self.token_list = new_list
        #             break        


        self.token_list.reverse()

        stack = []
        prefixList = []

        #this algo "https://www.youtube.com/watch?v=8QxlrRws9OI&ab_channel=Jenny%27sLecturesCSIT"
        for i in self.token_list:
            #throwing operands to output
            if i.type != "operator":
                prefixList.append(i)
            elif i.type == "operator":
                #stacking operators
                if stack == []:
                    stack.append(i)
                else:
                    #always push right_brack
                    if(i.value == "right_brack"):
                        stack.append(i)

                    #right brack at top of stack
                    elif stack[len(stack)-1].value == "right_brack":
                        #always push on right brack
                        if i.value != "left_brack":
                            stack.append(i)

                        #unless its left bracket
                        else:
                            stack.pop()

                    #left bracket
                    #pop until right bracket
                    elif i.value == "left_brack":
                        while stack!=[] and stack[len(stack)-1].value != "right_brack":
                            prefixList.append(stack.pop())
                        if(stack != []):

                            stack.pop()


                    #push at top of the stack
                    elif SyntaxAnalysis.operatorPriority( stack[len(stack)-1] ) < SyntaxAnalysis.operatorPriority(i):
                        stack.append(i)
                    #same prirority, "^" pop to input, otherwise push to stack (left/right associativity)
                    elif SyntaxAnalysis.operatorPriority( stack[len(stack)-1] ) == SyntaxAnalysis.operatorPriority(i):
                        if(i.value=="exp"):
                            prefixList.append(i)
                        else:
                            stack.append(i)
                    #new operator have lesser priority
                    #pop until you reach your or lower
                    #exponent shouldt even happen
                    #stop at brackets
                    elif SyntaxAnalysis.operatorPriority( stack[len(stack)-1] ) > SyntaxAnalysis.operatorPriority(i):
                        while stack!=[] and stack[len(stack)-1].value != "right_brack" and SyntaxAnalysis.operatorPriority(stack[len(stack)-1]) > SyntaxAnalysis.operatorPriority(i):
                            prefixList.append(stack.pop())
                        
                        stack.append(i)
        #pop operators on stack
        while stack != []:
            prefixList.append(stack.pop())

        prefixList.reverse()
        self.token_list = prefixList



        
#projde strom a vraci
class PathAndRule():
    def __init__(self,path,rule):
        self.path = path # "lrdl" l=left, r = right, d = down
        self.rule = rule
  

class ExpressionNode():
    def __init__(self):
        pass
    def applyRule(node,rule):
        if (rule.type in ["basic_plus","basic_minus","basic_div","basic_mul","basic_exp"]):
            node = applyBasicOperations(node,rule)
    # return OperandNode(Token("int",5))
        return node

    def treeEqual(original_node,compare_to):
        if(type(original_node) != type(compare_to)):
            return False
        if(isinstance(original_node,OperatorNode)):
            if(original_node.type == compare_to.type):
                return True and ExpressionNode.treeEqual(original_node.left_child,compare_to.left_child) and ExpressionNode.treeEqual(original_node.right_child,compare_to.right_child)
            else:
                return False
        if(isinstance(original_node,OperandNode)):
            if(original_node.type == compare_to.type):
                if(original_node.type == "var"):
                    if(original_node.value.name == compare_to.value.name):
                        return True
                    else:
                        return False

                if(original_node.value.value == compare_to.value.value):
                    return True
                else:
                    return False
            else:
                return False
        if(isinstance(original_node,FunctionNode)):
            if(original_node.value == compare_to.value):
                return True and ExpressionNode.treeEqual(original_node.child,compare_to.child)
            else:
                return False

        



class ExpressionTree():
    tree_counter = 0
    finished_trees = []
    def __init__(self,token_list):
        self.path_and_rules = []
        self.token_list = token_list
        self.root = None
        self.father_tree_id = 0
        self.id = 0

    # function constants converts  to floats
    def tokenToNode(token : Token) -> ExpressionNode :
        if token.type == "operator":
            return OperatorNode(token)
        elif token.type in ["int","float","var"]:
            return OperandNode(token)
        elif token.type == "func":
            if(token.value == "pi"):
                tmp = OperandNode(Token("float",pi))
                tmp.value.constant_value = "pi"
                return tmp
            elif(token.value == "exp"):
                tmp = OperandNode(Token("float",e))
                tmp.value.constant_value = "exp"
                return tmp
            else:
                if token.value not in ["sin","cos","ln"]:
                    return errorExit("Not known function error")
                else:
                    return FunctionNode(token)
        else:
            return OperandNode(token)
    
    def isClosed(root) -> True:
        if(isinstance(root,FunctionNode)):
            if(root.child == None):
                return False
            else:
                return ExpressionTree.isClosed(root.child)
        elif(isinstance(root,OperandNode)):
            return True
        elif(isinstance(root,OperatorNode)):
            if(root.left_child == None or root.right_child == None):
                return False
            else:
                return ExpressionTree.isClosed(root.left_child) and ExpressionTree.isClosed(root.right_child)
        else:
            return False
    
    def addNodeToOpen(root,new_node) -> ExpressionNode:
        if(isinstance(root,FunctionNode)):
            if(root.child == None):
                root.child = new_node
            else:
                root.child = ExpressionNode.addNodeToOpen(root.child,new_node)
        elif(isinstance(root,OperatorNode)):
            if(root.left_child == None):
                root.left_child = new_node
            elif(ExpressionTree.isClosed(root.left_child) == False):
                root.left_child = ExpressionTree.addNodeToOpen(root.left_child,new_node)
            elif(root.right_child == None):
                root.right_child = new_node
            elif(ExpressionTree.isClosed(root.right_child) == False):
                root.right_child = ExpressionTree.addNodeToOpen(root.right_child,new_node)
            else:
                errorExit("Adding node to close operator")
        elif(isinstance(root,OperandNode)):
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
            if(ExpressionTree.isClosed(root)):
                break
            root = ExpressionTree.addNodeToOpen(root,nodeList.pop(0))

        if nodeList != []:
            errorExit("wrong syntax of expression")
        return root




    def generatePathAndRules(self,node,path):
        rules = generateRules(node)
        for i in rules:
            self.path_and_rules.append(PathAndRule(path,i))
        if(isinstance(node,OperandNode)):
            return
        elif(isinstance(node,OperatorNode)):
            self.generatePathAndRules(node.left_child,path+"l")
            self.generatePathAndRules(node.right_child,path+"r")
        elif(isinstance(node,FunctionNode)):
            self.generatePathAndRules(node.child,path+"d")
    


    # modify given tree
    def applyRuleOnTree(self,path_and_rule):
        print(path_and_rule.path)
        if(path_and_rule.path == ""):
            self.root = self.root.applyRule(path_and_rule.rule)
            return
        node_to_expend = self.root
        #loop until the next node is to expend
        i = 0
        while i != len(path_and_rule.path) - 1:
            print("counter")
            if(path_and_rule.path[i] == 'l'):
                print(1)
                node_to_expend = node_to_expend.left_child
            elif(path_and_rule.path[i] == 'r'):
                print(2)
                node_to_expend = node_to_expend.right_child
            elif(path_and_rule.path[i] == 'd'):
                node_to_expend = node_to_expend.child
            i += 1

        #sem to spadne vzdycky (snad)
        if(len(path_and_rule.path) - i==1):
            if(path_and_rule.path[i] == "l"):
                node_to_expend.left_child = ExpressionNode.applyRule(node_to_expend.left_child,path_and_rule.rule)
            elif(path_and_rule.path[i] == "r"):
                node_to_expend.right_child = ExpressionNode.applyRule(node_to_expend.right_child,path_and_rule.rule)
            elif(path_and_rule.path[i] == "d"):
                node_to_expend.child = ExpressionNode.applyRule(node_to_expend.child,path_and_rule.rule)
            return
            

    def isTreeAlreadyDone(self):
        for i in ExpressionTree.finished_trees:
            if(ExpressionNode.treeEqual(self.root,i.root)):
                return True
        return False


    #return list of new trees
    def generateNextGeneration(self):
        newTrees = []
        for i in self.path_and_rules:
            treeCopy = copy.deepcopy(self)
            treeCopy.path_and_rules = []
            ExpressionTree.tree_counter += 1
            treeCopy.id = ExpressionTree.tree_counter
            treeCopy.father_tree_id = self.id
            treeCopy.applyRuleOnTree(i)
            newTrees.append( treeCopy)
        ExpressionTree.finished_trees.append(self)
        return newTrees

    def getRidOfBrakcets(str):
        print(str)
        without_brackets = False
        while without_brackets == False:
            without_brackets = True
            for i in range(1,len(str)):
                if(i == len(str)-1):
                    continue
                if (str[i-1] == '(' and str[i+1] == ')'):
                    str = str[:i-1] + str[i] + str[i+2:]
                    without_brackets = False
                    break
        return str



    #tree to infix
    def treeToInfix(root : ExpressionNode):
        if(isinstance(root,OperandNode)):
            if(root.type == "int" or root.type == "float"):
                return str(root.value.value)
            else:
                return root.value.name
        if(isinstance(root,OperatorNode)):
            if(root.type == 'plus'):
                return f"({ExpressionTree.treeToInfix(root.left_child)}) + ({ExpressionTree.treeToInfix(root.right_child)})"
            if(root.type == 'minus'):
                return f"({ExpressionTree.treeToInfix(root.left_child)}) - ({ExpressionTree.treeToInfix(root.right_child)})"
            if(root.type == 'mul'):
                return f"({ExpressionTree.treeToInfix(root.left_child)}) * ({ExpressionTree.treeToInfix(root.right_child)})"
            if(root.type == 'div'):
                return f"({ExpressionTree.treeToInfix(root.left_child)}) / ({ExpressionTree.treeToInfix(root.right_child)})"
            if(root.type == 'exp'):
                return f"({ExpressionTree.treeToInfix(root.left_child)}) ^ ({ExpressionTree.treeToInfix(root.right_child)})"
            if(root.type == 'equal'):
                return f"{ExpressionTree.treeToInfix(root.left_child)} = {ExpressionTree.treeToInfix(root.right_child)}"
        if(isinstance(root,FunctionNode)):
            return f"{root.type}({ExpressionTree.treeToInfix(root.child)})"

        return ""

    def getFinishedTree(id):
        for i in ExpressionTree.finished_trees:
            if i.id == id:
                return i


class OperatorNode(ExpressionNode):
    def __init__(self,operator : Token):
        super().__init__()
        self.type = operator.value # exp,mul,div,plus,minus,equal
        self.left_child = None
        self.right_child = None


class OperandNode(ExpressionNode):
    def __init__(self,operand):
        super().__init__()
        self.type = operand.type # var,int,float
        if self.type == "int":
            self.value  = IntegerValue(operand)
        if self.type == "float":
            self.value  = FloatValue(operand)
        if self.type == "var":
            self.value  = VarValue(operand)

class FunctionNode(ExpressionNode):
    def __init__(self,operator):
        super().__init__()
        self.type = operator.value # sin,cos,
        self.child = None

class IntegerValue():
    def __init__(self, operand):
        self.value = operand.value

#dodelat nejak pi a exp
class FloatValue():
    def __init__(self, operand):
        self.value = operand.value
        self.constant_value = None

class VarValue():
    def __init__(self, operand):
        self.name = operand.value



class Rules():
    def __init__(self,type):
        self.type = type

# returns rules: plus/minus/divide/multiply/exp
def checkForBasicOperations(node):
    #it is operand above 2 operators
    if isinstance(node, OperatorNode) and isinstance(node.left_child, OperandNode)  and isinstance(node.right_child, OperandNode):
        #both sides are variables
        # all but x^x
        if isinstance(node.left_child.value, VarValue) and isinstance(node.right_child.value, VarValue) and (node.left_child.value.name == node.right_child.value.name):
            if node.type == "plus":
                return Rules("basic_plus")
            if node.type == "minus":
                return Rules("basic_minus")
            if node.type == "div":
                return Rules("basic_div")
            if node.type == "mul":
                return Rules("basic_mul")
            return


        #both sides are numbers
        #can do all operations
        if (isinstance(node.left_child.value, IntegerValue)or isinstance(node.left_child.value, FloatValue)) and (isinstance(node.right_child.value, IntegerValue) or isinstance(node.right_child.value, FloatValue)):
            if node.type == "plus":
                return Rules("basic_plus")
            if node.type == "minus":
                return Rules("basic_minus")
            if node.type == "div":
                return Rules("basic_div")
            if node.type == "mul":
                return Rules("basic_mul")
            if node.type == "exp":
                return Rules("basic_exp")

    else:
        return

#find where are you can shift operands
# a + b + c,
# a - b - c,
# a * b * c,
# a/(b/c),
#        div_right_shift
#           /
#       a      /
#           b     c
#
# (a/b)/c,
#        div_left_shift
#
#           /
#       /       c
#   a      b
#
# a - b + c,
#       plus_minus_shift
#           +
#       -      c
#     a    b
# a + b -c
#        minus_plus_shift
#           -
#       +      c
#     a    b
def checkForOperandShift(node):
    rules = []
    if isinstance(node, OperatorNode) and isinstance(node.left_child,OperatorNode):
        if(node.type == "plus" and node.left_child.type == "plus"):
            rules.append(Rules("plus_shift"))
        if(node.type == "minus" and node.left_child.type == "minus"):
            rules.append(Rules("minus_shift"))
        if(node.type == "mul" and node.left_child.type == "mul"):
            rules.append(Rules("mul_shift"))
        if(node.type == "div" and node.left_child.type == "div"):
            rules.append(Rules("div_left_shift"))
        if(node.type == "plus" and node.left_child.type == "minus"):
            rules.append(Rules("plus_minus_shift"))
        if(node.type == "minus" and node.left_child.type == "plus"):
            rules.append(Rules("minus_plus_shift"))
    if isinstance(node, OperatorNode) and isinstance(node.right_child, OperatorNode):
        if(node.type == "div" and node.right_child.type == "div"):
            rules.append(Rules("div_right_shift"))

    return rules


def generateRules(node:ExpressionNode):
    rules = []
    rule = checkForBasicOperations(node)
    if(rule != None):
        rules.append(rule)

    rules.extend(checkForOperandShift(node))

    return rules

def applyBasicOperations(node,rule):
    #operations at variables
    new_node = None
    if(isinstance(node.left_child.value,VarValue)):
        if(rule.type == "basic_plus"):
            new_node = OperatorNode(Token("operator","mul"))
            new_node.left_child = OperandNode(Token("int","2"))
            new_node.right_child = OperandNode(Token("var",node.left_child.value.name))
        if(rule.type == "basic_minus"):
            new_node = OperandNode(Token("int","0"))
        if(rule.type == "basic_div"):
            new_node = OperandNode(Token("int","1"))
        if(rule.type == "basic_mul"):
            new_node = OperatorNode(Token("operator","exp"))
            new_node.left_child = OperandNode(Token("var",node.left_child.value.name))
            new_node.right_child = OperandNode(Token("int","2"))

    #operations on numbers
    else:
        value = 0
        if(rule.type == "basic_plus"):
            value = node.left_child.value.value + node.right_child.value.value
        if(rule.type == "basic_minus"):
            value = node.left_child.value.value - node.right_child.value.value
        if(rule.type == "basic_mul"):
            value = node.left_child.value.value * node.right_child.value.value
        if(rule.type == "basic_div"):
            if(node.right_child.value.value == 0):
                return node
            value = node.left_child.value.value / node.right_child.value.value
        if(rule.type == "basic_exp"):
            value = node.left_child.value.value ** node.right_child.value.value

        if type(value) == int:
            new_node = OperandNode(Token("int",value))
        else:
            new_node = OperandNode(Token("float",value))




    return new_node


