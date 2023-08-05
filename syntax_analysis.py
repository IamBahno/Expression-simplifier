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


#load tokens
#check syntax
#infix
#tree
class SyntaxAnalysis():
    def __init__(self):
        self.token_list = []

    def loadTokens(self):
        token = None
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


class ExpressionTree():
    def __init__(self,token_list):
        self.path_and_rules = []
        self.token_list = token_list
        self.root = None

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

    def generateRules(node):
        return ["pravidlo1"]


    def generatePathAndRules(self,node,path):
        rules = ExpressionTree.generateRules(node)
        for i in rules:
            self.path_and_rules.append(PathAndRule(path,i))
        if(isinstance(node,OperandNode)):
            return
        elif(isinstance(node,OperatorNode)):
            self.generatePathAndRules(node.left_child,path+"l")
            self.generatePathAndRules(node.right_child,path+"r")
        elif(isinstance(node,FunctionNode)):
            self.generatePathAndRules(node.child,path+"d")
            












class OperatorNode(ExpressionNode):
    def __init__(self,operator):
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


analyser = SyntaxAnalysis()
analyser.loadTokens()
analyser.checkSyntax()
for i in analyser.token_list:
    tools.printToken(i)
print("--------------")
analyser.infixToPrefix()
for i in analyser.token_list:
    tools.printToken(i)
print("--------------")
strom = ExpressionTree(analyser.token_list)
strom.root = strom.constructTree()

print(printTree(strom.root))

strom.generatePathAndRules(strom.root,"")

for i in strom.path_and_rules:
    print(i.path)