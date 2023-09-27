import bisect
from operator import attrgetter
class TreeRuleValue():
    def __init__(self,tree,rule_and_path):
        self.tree = tree
        self.rule_and_path = rule_and_path
        self.value = TreeRuleValue.calculateValue(tree.rules_applied,rule_and_path.rule)

    @staticmethod
    def calculateValue(rules_applied,rule):
        rule_value = 1
        deep_of_expression_value = rules_applied
        if (rule.type in ["basic_plus", "basic_minus", "basic_div", "basic_mul", "basic_exp"]):
            rule_value = 10
        elif (rule.type in ["plus_shift", "minus_shift", "mul_shift", "div_left_shift", "div_right_shift",
                            "plus_minus_shift", "minus_plus_shift"]):
            rule_value = 2
        elif (rule.type in ["node-minus-node", "var-minus-node", "node-minus-var", "node-plus-node",
                            "var-plus-node", "node-plus-var"]):
            rule_value = 3
        elif (rule.type == "zero-var"):
            rule_value = 8
        elif (rule.type in ["minus-one-mul-var", "var-mul-minus-one"]):
            rule_value = 8
        elif (rule.type.find("div_to_mul") != -1):
            rule_value = 1
        elif (rule.type in ["brack_mul_right", "brack_mul_left", "brack_div_right", "brack_div_left"]):
            rule_value = 1
        elif (rule.type in ["exponent_mul", "exponent_div", "same_nodes_mul", "same_nodes_div", "exponent_left_mul",
                            "exponent_left_div", "exponent_right_mul", "exponent_right_div"]):
            rule_value = 10
        elif (rule.type in ["CommutativeAddition", "CommutativeMultiplication"]):
            rule_value = 4
        elif (rule.type == "node-minus-bracket"):
            rule_value = 4
        elif (rule.type in ["one-mul-node", "node-mul-one", "zero-mul-node", "node-mul-zero", "node-div-one",
                            "node-div-zero", "zero-div-node",
                            "zero-plus-minus-node", "node-plus-minus-zero", "one-exp-node", "node-exp-one",
                            "zero-exp-node", "node-exp-zero"]):
            rule_value = 10
        elif (rule.type == "exp-of-exp-node"):
            rule_value = 10
        # function, but is a mess,
        # elif(rule.type in ["exp-of-mult-or-div","exp-by-multiplication"]):
        #     node = RulesPack.expOfNode(node,rule)

        elif rule.type == "neg-exp-to-div":
            rule_value = 1
        # elif (rule.type.find("fraction-canceling-") != -1) or (rule.type.find("mul-of-fract-canceling-") != -1):
        #     node = RulesPack.fractCanceling(node,rule)

        elif (rule.type == "multinomial_theorem"):
            rule_value = 8
        return 0.3 * rule_value + 0.7 * deep_of_expression_value

class ListOfTreeRuleValues():
    def __init__(self):
        self.list = []

    def insert(self,new):

        bisect.insort(self.list,new,key= lambda x:x.value)

    def pop(self):
        return self.list.pop()

