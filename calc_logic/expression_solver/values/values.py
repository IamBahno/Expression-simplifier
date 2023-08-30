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
        self.sign = "plus" #"minus"
