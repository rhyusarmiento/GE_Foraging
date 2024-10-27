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
            for x in range(GENE_LEN):
                num = random.randint(0, 60)
                while num == 0:
                    num = random.randint(0, 60)
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
            
    def crossoverProduction(self, parentGenes, graphID):
        newGenotype = []
        codonIndex = 0
        while codonIndex < len(parentGenes[0].genotype):
            randGeneIndex = random.randint(0, len(parentGenes) - 1)
            currentParent = parentGenes[randGeneIndex]
            disectBlock = []
            currentCodon = currentParent.genotype[codonIndex]
            if graphID == STATEGENE:
                self.genoAppendSearch(codonIndex, disectBlock, graphID, currentCodon, currentParent.genotype)            
            elif graphID == EXPLOREGENE:
                self.genoAppendSearch(codonIndex, disectBlock, graphID, currentCodon, currentParent.genotype)
            newGenotype.append(disectBlock)
        return newGenotype
    
    def genoAppendSearch(self, codonIndex, disectBlock, graphID, currentCodon, geno):
        if not codonIndex + 1 >= len(geno):
            if graphID == STATEGENE:
                nextnode = self.stateGraph.find_for_crossover(currentCodon)
            elif graphID == EXPLOREGENE:
                nextnode = self.behaviorGraph.find_for_crossover(currentCodon)

            if nextnode is False:
                disectBlock.append(currentCodon)
                codonIndex += 1
                currentCodon = geno[codonIndex]
                self.genoAppendSearch(codonIndex, disectBlock, graphID, currentCodon, geno)
            else:
                if nextnode.isTerminal:
                    disectBlock.append(currentCodon)
                    codonIndex += 1
                else:
                    disectBlock.append(currentCodon)
                    codonIndex += 1
                    currentCodon = geno[codonIndex]
                    self.genoAppendSearch(codonIndex, disectBlock, graphID, currentCodon, geno)
                    
    def mutation(self, gene, graphID):
        newGenotype = []
        codonIndex = 0
        while codonIndex < len(gene.genotype):
            insertCodon = gene.mutateValue(codonIndex)
            if insertCodon is False:
                codonIndex += 1
            else: 
                disectBlock = []
                if graphID == STATEGENE:
                    self.genoAppendSearch(codonIndex, disectBlock, graphID, insertCodon, gene.genotype)            
                elif graphID == EXPLOREGENE:
                    self.genoAppendSearch(codonIndex, disectBlock, graphID, insertCodon, gene.genotype)
                newGenotype.append(disectBlock)
        return newGenotype
        
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
        expression = Gene.parse_expression(rules, start_symbol, self, start_symbol)
        # print(expression)
        self.current_codon = 0
        expression = Gene.finish_expression(rules, self, expression)
        return expression
    
    def mutateValue(self, num):
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