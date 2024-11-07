import re
from const import EXPLORE_RULES, STATE_RULES

class GGraph:
    def __init__(self, rules):
        self.Nodes = []
        self.generateGraph(rules)
        self.isGood = False
        self.nodeIndex = {}
        self.nodesSize = 0
        
    def setNodeIndex(self):
        num = 0
        for node in self.Nodes:
            node.indexValue = num
            self.nodeIndex[num] = node
            num += 1
        
        self.nodesSize = num
        
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
                non_terminals = re.findall("<[^>]+>", production)
                nonTerminalSet = set()
                for non_terminal in non_terminals:
                    if non_terminal != branchNode.value:
                        nonTerminalSet.add(non_terminal)
                for non_terminal in nonTerminalSet:
                    currNode = self.selectNode(non_terminal)
                    branchNode.appendOutNode(currNode)
                    currNode.appendInNode(branchNode)
                self.updateWeights(branchNode)
            self.updateWeights(trunckNode)
        if self.isGood:
            return True
        else:
            return False
    
    def printGraph(self):
        for node in self.Nodes:
            print(f'{node.value}:{node.weight}', [n.value for n in node.outNodes])
    
    def find_by_mod(self, rule, gene):
        productions = self.getNode(rule).outNodes
        codon = gene.get_codon()
        # if type(codon) == list:
        #     print(f"this is bad {codon} type why {type(codon)}")
        # print(f"nodessize {type(self.nodesSize)}")
        modValue = codon % self.nodesSize
        # print(f"modvalue {type(modValue)}")
        productionValue = None
        while productionValue is None:
            for production in productions:
                if production.indexValue == modValue:
                    productionValue = production.value
            gene.current_codon += 1
            if gene.current_codon >= len(gene.genotype):   
                return None 
            modValue = gene.get_codon() % self.nodesSize
        return productionValue
    
    # Fix
    def find_for_crossover(self, inputCodon, nextCodon):
        node = self.nodeIndex[inputCodon % self.nodesSize]
        productions = node.outNodes
        productionNode = False
        for production in productions:
            if production.indexValue == nextCodon % self.nodesSize:
                productionNode = production
        return productionNode
            
    def weight_traveral(self, Node, codon):
        if Node.isTerminal is True:
            return Node.value
        else:
            terminalPath = []
            # find available options
            for node in Node.outNodes:
                if node.isTerminal or (node.weight > Node.weight):
                    terminalPath.append(node)
            
            if len(terminalPath) == 0:
                for node in Node.inNodes:
                    if node.isTerminal or (node.weight > Node.weight):
                        terminalPath.append(node)
            
            if len(terminalPath) == 0:
                if len(Node.outNodes) > 0:
                    node = Node.outNodes[0]
                    terminalPath.append(node)
                
            if len(terminalPath) == 0:
                if len(Node.inNodes) > 0:
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
        self.indexValue = 0
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
    ggraphstate = GGraph(STATE_RULES)
    ggraphstate.printGraph()
    print("next ggraph")
    ggraphexplore = GGraph(EXPLORE_RULES)
    ggraphexplore.printGraph()
    # print(ggraph.find_by_mod('<progs>', 32))
    # print(ggraph.find_by_weight('<code>', 32))
    