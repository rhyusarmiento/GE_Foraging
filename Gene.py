import re
import random
from const import STATE_RULES, EXPLORE_RULES, EXPLOREGENE, STATEGENE
from const import MUTATION_RATE, MUTATION_FIRSTDECUT, MUTATION_SECONDDECUT, MUTATION_THIRDDECUT
from const import LARGE_MUTATION_RATE, LARGE_MUTATION_FIRSTDECUT, LARGE_MUTATION_SECONDDECUT, LARGE_MUTATION_THIRDDECUT
from const import GENE_LEN, GENE_FIRSTCUT, GENE_SECONDCUT, GENE_THIRDCUT
from GGraph import GGraph

class DNAManager:
    def __init__(self):
        self.Genes = {}
        self.stateGraph = GGraph(STATE_RULES)
        self.stateGraph.setNodeIndex()
        self.behaviorGraph = GGraph(EXPLORE_RULES)
        self.behaviorGraph.setNodeIndex()
        
    def addGene(self, name, gene=None):
        if gene is None:
            genelist = []
            if name == STATEGENE:
                for x in range(GENE_LEN):
                    num = random.randint(0, self.stateGraph.nodesSize)
                    genelist.append(num)
            elif name == EXPLOREGENE:
                for x in range(GENE_LEN):
                    num = random.randint(0, self.behaviorGraph.nodesSize)
                    genelist.append(num)
            
            gene = Gene(genelist)
        self.Genes[name] = gene
        
    def getGene(self, name):
        gene = self.Genes.get(name)
        if gene is None:
            self.addGene(name)
            gene = self.Genes.get(name)
        return gene
    
    def getGenePhenotype(self, name):
        gene = self.getGene(name)
        if name == EXPLOREGENE:
            return gene.generate_phenotype(self.behaviorGraph, "<start>", EXPLOREGENE)
        elif name == STATEGENE:
            return gene.generate_phenotype(self.stateGraph, "<start>", STATEGENE)
        else:
            return None
        
    def mutateGenes(self):
        for key in self.Genes:
            self.Genes[key].mutate()
            
    def crossoverProduction(self, parentGenes, myGene, graphID):
        newGenotype = []
        codonIndex = 0
        while codonIndex < len(myGene.genotype):
            randGeneIndex = random.randint(0, len(parentGenes) - 1)
            currentParent = parentGenes[randGeneIndex]
            disectBlock = []
            currentCodon = currentParent.genotype[codonIndex]
            if graphID == STATEGENE:
                if currentCodon % self.stateGraph.nodesSize == myGene.genotype[codonIndex] % self.stateGraph.nodesSize:
                    newIndex = self.genoAppendSearch(codonIndex, disectBlock, graphID, currentCodon, currentParent.genotype)
                    codonIndex += newIndex
                else:
                    disectBlock.append(myGene.genotype[codonIndex])
                    codonIndex += 1     
            elif graphID == EXPLOREGENE:
                if currentCodon % self.behaviorGraph.nodesSize == myGene.genotype[codonIndex] % self.behaviorGraph.nodesSize:
                    newIndex = self.genoAppendSearch(codonIndex, disectBlock, graphID, currentCodon, currentParent.genotype)
                    codonIndex += newIndex
                else:
                    disectBlock.append(myGene.genotype[codonIndex])
                    codonIndex += 1  
            if len(newGenotype) > len(myGene.genotype):
                print(f"houston deadloop {newGenotype}")
                
            newGenotype.extend(disectBlock)
        if len(newGenotype) > GENE_LEN:
            print(f"houston crossover {newGenotype}")
        return newGenotype
    
    def genoAppendSearch(self, codonIndex, disectBlock, graphID, currentCodon, parentGeno):
        if not codonIndex + 1 >= len(parentGeno):
            if codonIndex > len(parentGeno):
                print(codonIndex)
                
            if graphID == STATEGENE:
                # I have an issue with the mod value. the number bounds and size matter for each
                currentNode = self.stateGraph.nodeIndex[currentCodon % self.stateGraph.nodesSize]
                nextnode = self.stateGraph.find_for_crossover(currentCodon, parentGeno[codonIndex + 1])
            elif graphID == EXPLOREGENE:
                currentNode = self.behaviorGraph.nodeIndex[currentCodon % self.behaviorGraph.nodesSize]
                nextnode = self.behaviorGraph.find_for_crossover(currentCodon, parentGeno[codonIndex + 1])

            if nextnode is False:
                disectBlock.append(currentCodon)
                codonIndex += 1
                currentCodon = parentGeno[codonIndex]
                codonIndex += self.genoAppendSearch(codonIndex, disectBlock, graphID, currentCodon, parentGeno)
                return codonIndex
            elif nextnode is not None:
                if nextnode.isTerminal:
                    disectBlock.append(currentCodon)
                    codonIndex += 1
                    currentCodon = parentGeno[codonIndex]
                    disectBlock.append(currentCodon)
                    return codonIndex
                else:
                    disectBlock.append(currentCodon)
                    codonIndex += 1
                    currentCodon = parentGeno[codonIndex]
                    codonIndex += self.genoAppendSearch(codonIndex, disectBlock, graphID, currentCodon, parentGeno)
                    return codonIndex
            elif currentNode.isTermminal:
                disectBlock.append(currentCodon)
                codonIndex += 1
                return codonIndex
            
    # mutation fix remove geno expanition
    def mutation(self, gene, graphid):
        newGenotype = []
        codonIndex = 0
        while codonIndex < len(gene.genotype):
            insertCodon = self.mutateValue(codonIndex, graphid, gene.genotype)
            if insertCodon is False:
                newGenotype.append(gene.genotype[codonIndex])
                codonIndex += 1
            else: 
                newGenotype.append(insertCodon)
                codonIndex += 1
        if len(newGenotype) > GENE_LEN:
            print(f"houston mutation {newGenotype}")
        return newGenotype

    def mutateValue(self, num, graphid, genotype):
        if graphid == STATEGENE:    
            if random.randint(1,100) > (100 * (MUTATION_RATE)):
                return random.randint(0, self.stateGraph.nodesSize)
            else:
                return False
        elif graphid == EXPLOREGENE:
            if num < (len(genotype) * GENE_FIRSTCUT):
                if random.randint(1,100) > (100 * MUTATION_RATE):
                    return random.randint(0, self.behaviorGraph.nodesSize)
            elif num < (len(genotype) * GENE_SECONDCUT):
                if random.randint(1,100) > (100 * (MUTATION_RATE - MUTATION_FIRSTDECUT)):
                    return random.randint(0, self.behaviorGraph.nodesSize)
            elif num < (len(genotype) * GENE_THIRDCUT):
                if random.randint(1,100) > (100 * (MUTATION_RATE - MUTATION_SECONDDECUT)):
                    return random.randint(0, self.behaviorGraph.nodesSize)
            else:
                if random.randint(1,100) > (100 * (MUTATION_RATE - MUTATION_THIRDDECUT)):
                    return random.randint(0, self.behaviorGraph.nodesSize)
            return False
        
class Gene:
    def __init__(self, genotype) -> None:
        self.genotype = genotype
        self.current_codon = 0
        self.latestScore = 0
        self.score = 0
    
    def get_codon(self):
        return self.genotype[self.current_codon]
    
    # A recursive function that evaluates non-terminals in a string in a depth-first search.
    def parse_expression(rules, expression, gene, terminal_string):
        non_terminals = re.findall("<[^>]+>", expression)
        # gene genotype len explostion therefore not reaching ending w
        for non_terminal in non_terminals:
            if gene.current_codon >= len(gene.genotype):
                return terminal_string
                
            response = rules.find_by_mod(non_terminal, gene)
            if response is None:
                return terminal_string
            else:
                production = response
                    
            # substitute the non-terminal with the decided on production
            terminal_string = re.sub(non_terminal, production, terminal_string, 1)
            gene.current_codon += 1
            # repeat on the non-terminals in the production
            terminal_string = Gene.parse_expression(rules, production, gene, terminal_string)
        return terminal_string
                
    def finish_expression(rules, gene, terminal_string):
        non_terminals = re.findall("<[^>]+>", terminal_string)
        for non_terminal in non_terminals:
                if gene.current_codon >= len(gene.genotype):
                    print(len(gene.genotype))
                    gene.current_codon = 0
                    
                production = rules.find_by_weight(non_terminal, gene.get_codon())
                # substitute the non-terminal with the decided on production
                terminal_string = re.sub(non_terminal, production, terminal_string, 1)
                gene.current_codon += 1
        return terminal_string
    
    # Generates the program/expression represented by the gene i.e. the phenotype.
    def generate_phenotype(self, rules, start_symbol, genetype):
        if len(self.genotype) > 300:
            print(f"{self.genotype}")
        expression = Gene.parse_expression(rules, start_symbol, self, start_symbol)
        # print(expression)
        self.current_codon = 0
        expression = Gene.finish_expression(rules, self, expression)
        self.current_codon = 0
        return expression
    
    def mutateValue(self, num, graphid):
        newGeno = self.genotype.copy()
        if num < (len(newGeno) * GENE_FIRSTCUT):
            if random.randint(1,100) > (100 * MUTATION_RATE):
                return random.randint(0, 60)
        elif num < (len(newGeno) * GENE_SECONDCUT):
            if random.randint(1,100) > (100 * (MUTATION_RATE - MUTATION_FIRSTDECUT)):
                return random.randint(0, 60)
        elif num < (len(newGeno) * GENE_THIRDCUT):
            if random.randint(1,100) > (100 * (MUTATION_RATE - MUTATION_SECONDDECUT)):
                return random.randint(0, 60)
        else:
            if random.randint(1,100) > (100 * (MUTATION_RATE - MUTATION_THIRDDECUT)):
                return random.randint(0, 60)
        return False
        
    def largeMutate(self):
        newGeno = self.genotype.copy()
        for num in range(len(newGeno)):
            if num < (len(newGeno) * GENE_FIRSTCUT):
                if random.randint(1,100) > (100 * LARGE_MUTATION_RATE):
                    input = random.randint(-40, 40)
                    while input == 0:
                        input = random.randint(-40, 40)
                    newGeno[num] = input
            elif num < (len(newGeno) * GENE_SECONDCUT):
                if random.randint(1,100) > (100 * (LARGE_MUTATION_RATE - LARGE_MUTATION_FIRSTDECUT)):
                    input = random.randint(-40, 40)
                    while input == 0:
                        input = random.randint(-40, 40)
                    newGeno[num] = input
            elif num < (len(newGeno) * GENE_THIRDCUT):
                if random.randint(1,100) > (100 * (LARGE_MUTATION_RATE - LARGE_MUTATION_SECONDDECUT)):
                    input = random.randint(-40, 40)
                    while input == 0:
                        input = random.randint(-40, 40)
                    newGeno[num] = input
            else:
                if random.randint(1,100) > (100 * (LARGE_MUTATION_RATE - LARGE_MUTATION_THIRDDECUT)):
                    input = random.randint(-40, 40)
                    while input == 0:
                        input = random.randint(-40, 40)
                    newGeno[num] = input
        self.genotype = newGeno
        self.score = 0
 
# if __name__ == "__main__":
#     genes = []
#     for i in range(4):
#         genes.append(Gene([random.randint(0, 100) for x in range(GENE_LEN)]))
#     gene = Gene([random.randint(0, 100) for x in range(GENE_LEN)])
#     print(gene.crossoverProduction(genes))