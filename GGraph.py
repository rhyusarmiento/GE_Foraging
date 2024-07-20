from const import RULES

class GGraph:
    def __init__(self, rules):
        self.Nodes = []
        self.generateGraph(rules)
        self.isGood = False
        
    # return True if node is in graph
    def isNode(self, rule):
        for node in self.Nodes:
            if rule == node.value:
                return True
        return False
    
    def getNode(self, rule):
        for node in self.Nodes:
            if rule == node.value:
                return node
            
    # if node exist return if not create new
    def selectNode(self, header):
        if not self.isNode(header):
            currNode = Node(header)
            self.Nodes.append(currNode)
        else:
            currNode = self.getNode(header)
        return currNode
    
    # depth first traversal 
    def updateWeights(self, coreNode):
        for node in coreNode.inNodes:
            if node.weight < (coreNode.weight - 1):
                node.weight = coreNode.weight - 1
                self.updateWeights(node)
    
    # generates Graph
    def generateGraph(self, rules):
        # check if node exist in Graph
        for rule in rules:
            trunckNode = self.selectNode(rule)
            # create node for each non existant production node and set in node list
            terminalCount = 0
            for production in rules[rule]:
                branchNode = self.selectNode(production)
                if branchNode.isTerminal is True:
                    terminalCount += 1
                    self.isGood = True
                # set truck weight only if its more
                if trunckNode.weight < terminalCount:
                    trunckNode.weight = terminalCount    
                trunckNode.appendOutNode(branchNode)
                branchNode.appendInNode(trunckNode)
                self.updateWeights(branchNode)
            self.updateWeights(trunckNode)
        if self.isGood:
            return True
        else:
            return False
    
    def printGraph(self):
        for node in self.Nodes:
            print(f'{node.value}:{node.weight}', [n.value for n in node.outNodes])
    
    def find_by_mod(self, rule, codon):
        productions = self.getNode(rule).outNodes
        return productions[codon % len(productions)].value
            
    def weight_traveral(self, Node, codon):
        if Node.isTerminal is True:
            return Node.value
        else:
            terminalPath = []
            # find available options
            for node in Node.outNodes:
                if node.isTerminal or (node.weight > Node.weight):
                    terminalPath.append(node)
            # NOTE: not all inculsive could still break with super 'cold' nodes
            if len(terminalPath) == 0:
                for node in Node.inNodes:
                    if node.isTerminal or (node.weight > Node.weight):
                        terminalPath.append(node)
            
            if len(terminalPath) == 0:
                node = Node.outNodes[0]
                terminalPath.append(node)
                
            if len(terminalPath) == 0:
                node = Node.inNodes[0]
                terminalPath.append(node)
            
            return self.weight_traveral(terminalPath[codon % len(terminalPath)], codon)  
        
    def find_by_weight(self, rule, codon):
        rootNode = self.getNode(rule)
        terminal = self.weight_traveral(rootNode, codon)
        return terminal

class Node:
    def __init__(self, inValue) -> None:
        # termial in this context means that there is no <> non terminals in the statement
        self.inNodes = []
        self.outNodes = []
        self.value = inValue
        if "<" not in inValue and ">" not in inValue:
            self.isTerminal = True
        else: 
            self.isTerminal = False
        self.weight = 0
    def appendOutNode(self, node):
        self.outNodes.append(node)
    def appendInNode(self, node):
        self.inNodes.append(node)

if __name__ == "__main__":
    ggraph = GGraph(RULES)
    ggraph.printGraph()
    print(ggraph.find_by_mod('<progs>', 32))
    print(ggraph.find_by_weight('<code>', 32))
    