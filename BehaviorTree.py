import plotly.graph_objects as go
import plotly.io as pio

class BehaviorTree:
    def __init__(self):
        self.root = None
        self.currentCommand = 0

    def appendchildren(self, parent, commandList):
        if commandList[self.currentCommand] == "ifFood":
            node = ifFood()
            self.currentCommand += 1
            for x in range(node.maxchilren + 1):
                node.children.append(self.appendchildren(node, commandList))
            return node
        elif commandList[self.currentCommand] == "progs":
            node = progs()
            self.currentCommand += 1
            for x in range(node.maxchilren + 1):
                node.children.append(self.appendchildren(node, commandList))
            return node
        elif commandList[self.currentCommand] == "isFood":
            node = isFood()
            self.currentCommand += 1
            return node
        elif commandList[self.currentCommand] == "isBored":
            node = isBored()
            self.currentCommand += 1
            return node
        elif commandList[self.currentCommand] == "left":
            node = left()
            self.currentCommand += 1
            return node
        elif commandList[self.currentCommand] == "forward":
            node = forward()
            self.currentCommand += 1
            return node
        elif commandList[self.currentCommand] == "right":
            node = right()
            self.currentCommand += 1
            return node
    
    def createBehavior(self, phenotype):        
        commandList = phenotype.replace("(", " ").replace(")", " ").replace(",", " ").split()
        self.currentCommand = 0
        self.root = self.appendchildren(None, commandList)
        return self.root
        # appends once terminal or next recrise part
        # checks for max children

    
class ifFood:
    def __init__(self):
        self.Name = "ifFood"
        self.children = []
        self.maxChildren = 2
    
    def whichChild(self, result):
        if result is True:
            return self.children[0]
        else:
            return self.children[1]

class progs:
    def __init__(self):
        self.Name = "progs"
        self.children = []
        self.maxChildren = 2
    
    def getChild(self, result):
        if result == 1:
            return self.children[0]
        if result == 2:
            return self.children[1]
        else:
            return False
        
class left:
    def __init__(self):
        self.Name = "left"

class forward:
    def __init__(self):
        self.Name = "forward"

class right:
    def __init__(self):
        self.Name = "right"
        
class isBored:
    def __init__(self):
        self.Name = "isBored"
        
class isFood:
    def __init__(self):
        self.Name = "isFood"