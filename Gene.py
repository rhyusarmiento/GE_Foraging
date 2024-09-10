import re
import random
from const import CROSSOVER_PRODUCTION, STATE_RULES, EXPLORE_RULES, GENE_LEN, BEHAVIORGENE, STATEGENE
from GGraph import GGraph

class DNAManager:
    def __init__(self):
        self.Genes = {}
        self.stateGraph = GGraph(STATE_RULES)
        self.behaviorGraph = GGraph(EXPLORE_RULES)
    
    def addGene(self, name, gene=None):
        if gene is None:
            genelist = []
            for x in range(GENE_LEN):
                num = random.randint(-60, 60)
                while num == 0:
                    num = random.randint(-60, 60)
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
        if name == BEHAVIORGENE:
            return gene.generate_phenotype(self.behaviorGraph, "<start>")
        elif name == STATEGENE:
            return gene.generate_phenotype(self.stateGraph, "<start>")
        else:
            return None
        
class Gene:
    def __init__(self, genotype) -> None:
        self.genotype = genotype
        self.current_codon = 0
    
    def get_codon(self):
        return self.genotype[self.current_codon]
    
    # A recursive function that evaluates non-terminals in a string in a depth-first search.
    def parse_expression(rules, expression, gene, terminal_string):
        non_terminals = re.findall("<[^>]+>", expression)
        for non_terminal in non_terminals:
                if gene.current_codon >= len(gene.genotype):
                    return terminal_string
                
                production = rules.find_by_mod(non_terminal, gene.get_codon())
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
    def generate_phenotype(self, rules, start_symbol):
        expression = Gene.parse_expression(rules, start_symbol, self, start_symbol)
        print(expression)
        self.current_codon = 0
        expression = Gene.finish_expression(rules, self, expression)
        return expression
    
    def crossoverProduction(self, genotypes):
        children = []
        for x in range(CROSSOVER_PRODUCTION * len(genotypes)):
            newGene = []
            for y in range(len(genotypes[0])):
                randGene = random.randint(0, len(genotypes) - 1)
                newGene.append(genotypes[randGene][y])
            children.append(Gene(newGene).mutate())
        return children
 
# if __name__ == "__main__":
#     genes = []
#     for i in range(4):
#         genes.append(Gene([random.randint(0, 100) for x in range(GENE_LEN)]))
#     gene = Gene([random.randint(0, 100) for x in range(GENE_LEN)])
#     print(gene.crossoverProduction(genes))