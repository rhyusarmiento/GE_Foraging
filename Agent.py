import random
from Gene import Gene
import const as const
from copy import deepcopy
# import numpy as np
from StateMachine import StateMachine
from GGraph import GGraph

class Agent:
    def __init__(self, rules, id='', gene=None) -> None:
        if id == '':
            self.id = f'ID{random.randint(0, 1000)}'
        else:
            self.id = id
        
        if gene is None:
            genelist = []
            for x in range(const.GENE_LEN):
                num = random.randint(-40, 40)
                while num == 0:
                    num = random.randint(-40, 40)
                genelist.append(num)
            self.gene = Gene(genelist)
        else:
            self.gene = deepcopy(gene)
        
        self.rules = rules
        self.phenotype = None
            
        self.SM = None
        self.currentState = None
        
        self.terminal_functions_run = 0
        
        self.numFood = 0
    
    def printID(self):
        print(f"{self.id}ID")
    
    def Pick(self):
        if self.should_end():
            self.end()
        # would check if there is food
        if True:
            self.numFood += 1
        return "isDone"
        
    def Drop(self):
        if self.should_end():
            self.end()
        # drop food
        if self.numFood > 0:
            self.numFood -= 1
        return "isDone"
        
    def Consume(self):
        if self.should_end():
            self.end()
            
        if self.numFood > 0:
            self.numFood -= 1
        return "isDone"
        
    def Explore(self):
        if self.should_end():
            self.end()
        # move 
        # one found food
        if True:
            return "isDone"
        return "continue"
        
    def Den(self):
        if self.should_end():
            self.end()
        return "isDone"
        
    def Known(self):
        if self.should_end():
            self.end()
        # go to known food that is stored in memory
        return "isDone"

    def runStateBehavior(self):            
        behaviorKey = self.currentState.behavior()
        if behaviorKey == "Pick":
            setter = self.Pick()
        elif behaviorKey == "Drop":
            setter = self.Drop()
        elif behaviorKey == "Consume":
            setter = self.Consume()
        elif behaviorKey == "Explore":
            setter = self.Explore()
        elif behaviorKey == "Den":
            setter = self.Den()
        elif behaviorKey == "Known":
            setter = self.Known()
        
        if setter != "continue":
            self.currentState.changeState(setter)
            
    def generate_SM(self):
        self.SM = StateMachine()
        self.SM.createSM(self.phenotype, self.gene.genotype)
    
    def runAgent(self):
        try:
            self.terminal_functions_run = 0
            self.gene.current_codon = 0
            if self.phenotype is None:
                self.phenotype = self.gene.generate_phenotype(self.rules, "<start>")
            if self.SM is None:
                self.generate_SM()
            self.currentState = self.SM.getStartState()
            if self.currentState is not None:
                while(True):
                    self.runStateBehavior()
            else:
                print("dead agent; no start state")
        except EndException:
            None
            # reward for food, punish for distance
            # self.gene.cost = np.round((((self.consecutiveFood * const.CONSECUTIVE_FOOD) + (self.food_touched * const.FOOD_INCENTIVE)) - ((self.distance * const.DISTANCEPINCH) + (self.offPath * const.OFFPATHPENALTY))), 2)
            # if self.food_touched == const.FOOD_NUM:
                # self.gene.cost += 50
    
    def setup(self):
        self.phenotype = self.gene.generate_phenotype(self.rules, "<start>")
        self.generate_SM()
    
    def should_end(self):
        self.terminal_functions_run += 1
        if self.terminal_functions_run == 1000:
            return True
        return False
    
    def end(self):
        raise EndException("End of simulation")

class EndException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

if __name__ == "__main__":
    ggraph = GGraph(const.RULES)
    # ggraph.printGraph()
    print("Agent:")
    agent = Agent(ggraph)
    agent.setup()
    agent.SM.printSM()