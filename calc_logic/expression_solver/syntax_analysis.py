from calc_logic.lex_analysis import Token,InputParser
from calc_logic.error import errorExit

from calc_logic.tools import printToken
from calc_logic.tools import printTree



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

    def checkForMinus(self):
        for i in range(len(self.token_list)):
            if self.token_list[i].type == "operator" and self.token_list[i].value == "minus":
                #vlevo je '('
                if(i == 0):
                    self.token_list = [Token("int",0)] + self.token_list
                    continue
                if(self.token_list[i-1].type == "operator" and self.token_list[i-1].value == "left_brack"):
                    self.token_list.insert(i,Token("int",0))



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








