# projde strom a vraci
class PathAndRule():
    def __init__(self, path, rule):
        self.path = path  # "lrdl" l=left, r = right, d = down
        self.rule = rule

class Rules():
    def __init__(self,type):
        self.type = type
