import calc_logic.expression_solver.rules as RulesPack
from calc_logic.tools import printTree

def applyRule(node, rule):
    # print("pred:" + printTree(node))
    if (rule.type in ["basic_plus", "basic_minus", "basic_div", "basic_mul", "basic_exp"]):
        node = RulesPack.basic_operations.applyBasicOperations(node, rule)
    elif (rule.type in ["plus_shift", "minus_shift", "mul_shift", "div_left_shift", "div_right_shift",
                        "plus_minus_shift", "minus_plus_shift"]):
        node = RulesPack.applyShiftOperations(node, rule)
    elif (rule.type in ["node-minus-node", "var-minus-node", "node-minus-var", "node-plus-node",
                            "var-plus-node", "node-plus-var"]):
        node = RulesPack.applyXOperations(node, rule)
    elif(rule.type == "zero-var"):
        node = RulesPack.zeroMinusVar(node)
    elif(rule.type in ["minus-one-mul-var","var-mul-minus-one"]):
        node = RulesPack.minusOneMulVar(node,rule)
    elif(rule.type.find("div_to_mul") != -1):
        node = RulesPack.divToMul(node,rule)
    elif(rule.type in ["brack_mul_right","brack_mul_left","brack_div_right","brack_div_left"]):
        node = RulesPack.mulDivBracket(node,rule)
    elif(rule.type in ["exponent_mul","exponent_div","same_nodes_mul","same_nodes_div","exponent_left_mul","exponent_left_div","exponent_right_mul","exponent_right_div"]):
        node = RulesPack.exponentMulDiv(node,rule)
    elif(rule.type in ["CommutativeAddition","CommutativeMultiplication"]):
        node = RulesPack.commutativeProperty(node)
    elif(rule.type == "node-minus-bracket"):
        node = RulesPack.nodeMinusBracket(node)
    elif(rule.type in ["one-mul-node","node-mul-one","zero-mul-node","node-mul-zero","node-div-one","node-div-zero","zero-div-node",
                       "zero-plus-minus-node","node-plus-minus-zero","one-exp-node","node-exp-one","zero-exp-node","node-exp-zero"]):
        node= RulesPack.oneZeroNodeOperations(node,rule)
    elif(rule.type == "exp-of-exp-node"):
        node = RulesPack.expOfExpNode(node)
    #function, but is a mess,
    # elif(rule.type in ["exp-of-mult-or-div","exp-by-multiplication"]):
    #     node = RulesPack.expOfNode(node,rule)

    elif rule.type == "neg-exp-to-div":
        node = RulesPack.negativeExpToDiv(node)
    # elif (rule.type.find("fraction-canceling-") != -1) or (rule.type.find("mul-of-fract-canceling-") != -1):
    #     node = RulesPack.fractCanceling(node,rule)

    elif(rule.type == "multinomial_theorem"):
        node = RulesPack.multinomial_theorem(node)

    # return OperandNode(Token("int",5))
    # print(rule.type)
    # print("po:" + printTree(node))
    return node