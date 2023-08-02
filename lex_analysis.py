import sys

class Token():        
    def __init__(self,type,value):
        self.type = type  #operator/var/func/int/float/eof_token/error_token
        self.value = value #(exp,mul,left_brack,right_brack,dic,plus,minus,equal)/name_of_var/name_of_func/int/float
    

class InputParser():
    leftover_char = None
    def __init__(self):
        pass
    def GetToken():
        state = "start" #start/var/func/int/int_dot/float
        string = ""
        while True:
            if(InputParser.leftover_char==None):
                char = sys.stdin.read(1)
            else:
                char = InputParser.leftover_char
                InputParser.leftover_char = None
            
            if state == "start":
                if char in ["^","*","(",")","/","+","-","="]:
                    if(char == "^"):
                        return Token("operator","exp")
                    elif(char == "*"):
                        return Token("operator","mul")
                    elif(char == "("):
                        return Token("operator","left_brack")
                    elif(char == ")"):
                        return Token("operator","right_brack")
                    elif(char == "/"):
                        return Token("operator","div")
                    elif(char == "+"):
                        return Token("operator","plus")
                    elif(char == "-"):
                        return Token("operator","minus")
                    elif(char == "="):
                        return Token("operator","equal")
                    else:
                        print("lol")
                        return None
                #if str(char).isalpha and char != "" and not str(char).isnumeric:
                if ('a' <= char and char <= 'z') or ('A' <= char and char <= 'Z'):
                    state = "var"
                    string += char
                    continue
                # if str(char).isnumeric and char != "" and not str(char).isalpha: 
                if ('0' <= char and char <= '9'): 
                    state = "int"
                    string += char
                    continue
            if state == "var":
                if ('a' <= char and char <= 'z') or ('A' <= char and char <= 'Z'):
                    state = "func"
                    string += char
                    continue
                else:
                    InputParser.leftover_char = char
                    return Token("var",string)
            if state == "func":
                if ('a' <= char and char <= 'z') or ('A' <= char and char <= 'Z'):
                    state = "func"
                    string += char
                    continue
                else:
                    InputParser.leftover_char = char
                    return Token("func",string)
            if state == "int":
                if ('0' <= char and char <= '9'):
                    string += char
                    continue
                elif(char == "."):
                    string += char
                    state = "int_dot"
                    continue
                else:
                    InputParser.leftover_char = char
                    return Token("int",int(string))
            if state == "int_dot":
                if ('0' <= char and char <= '9'):
                    string += char
                    state = "float"
                    continue
                else:
                    #ERROR dodelat
                    return Token("error_token","")
            if state == "float":
                if ('0' <= char and char <= '9'):
                    string += char
                    continue
                else:
                    InputParser.leftover_char = char
                    return Token("float",float(string))
            if char == "":
                return Token("eof_token","")
            else:
                return Token("error_token","")


