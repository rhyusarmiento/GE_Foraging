# import plotly.graph_objects as go
# import plotly.io as pio
from const import EXPLORE_RULES
from GGraph import GGraph
import random
from Gene import Gene

class BehaviorTree:
    def __init__(self, phenotype):
        commandList = phenotype.replace("(", " ").replace(")", " ").replace(",", " ").split()
        self.currentCommand = 0
        self.root = self.appendchildren(commandList)

    def appendchildren(self, commandList):
        if commandList[self.currentCommand] == "ifFood":
            node = ifFood()
            self.currentCommand += 1
            for x in range(node.maxChildren):
                node.children.append(self.appendchildren(commandList))
            return node
        elif commandList[self.currentCommand] == "func2":
            node = func2()
            self.currentCommand += 1
            for x in range(node.maxChildren):
                node.children.append(self.appendchildren(commandList))
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
        
    def printTree(self):    
        stringQueue = []
        tobeQueue = []
        tobeQueue.insert(0, self.root)
        while len(tobeQueue) > 0:
            insertString = []
            tobeQueue = self.printHelper(tobeQueue, insertString)
            stringQueue.insert(0, insertString)
        while len(stringQueue) > 0:
            stringLine = stringQueue.pop()
            printString = ""
            for string in stringLine:
                printString += f" {string}"
            print(printString)
        
    def printHelper(self, previousQueue, inputString):
        nextQueue = []  
        while len(previousQueue) > 0:
            nextNode = previousQueue.pop()
            # print(nextNode.Name)
            inputString.append(nextNode.Name)
            if nextNode.Name != "isBored" and nextNode.Name != "isFood" and nextNode.Name != "left" and nextNode.Name != "forward" and nextNode.Name != "right":
                for node in nextNode.children:
                    nextQueue.insert(0, node)
        return nextQueue
    
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

class func2:
    def __init__(self):
        self.Name = "func2"
        self.children = []
        self.maxChildren = 3
    
    def getChild(self, result):
        if result == 0:
            return self.children[0]
        if result == 1:
            return self.children[1]
        if result == 2:
            return self.children[2]
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
        
if __name__ == "__main__":
    ggraph = GGraph(EXPLORE_RULES)
    # ggraph.printGraph()
    genelist = []
    behaviorGene = None
    for x in range(500):
        num = random.randint(-60, 60)
        while num == 0:
            num = random.randint(-60, 60)
        genelist.append(num)    
    behaviorGene = Gene(genelist)
    pheno = behaviorGene.generate_phenotype(ggraph, "<start>")
    newTree = BehaviorTree()
    newTree.createBehavior(pheno)
    newTree.printTree()
    # print(ggraph.find_by_mod('<>', 32))
    # print(ggraph.find_by_weight('<code>', 32))