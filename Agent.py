import random
from Gene import Gene
import const as const
from copy import deepcopy
# import numpy as np
from StateMachine import StateMachine

class Agent:
    def __init__(self, grid, rules, id='', gene=None) -> None:
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
        self.SM = None
        self.currentState = None
        # agent id: either set manually else set randomly
        if id == '':
            self.id = f'ID{random.randint(0, 1000)}'
        else:
            self.id = id
            
        self.memory = []
        # generate string representation of program from grammar
        self.phenotype = None
        self.terminal_functions_run = 0
    
    def printID(self):
        print(f"{self.id}ID")
    
    def Pick():
        None
        
    def Drop():
        None
        
    def Consume():
        None
        
    def Explore():
        None
        
    def Den():
        None
        
    def Known():
        None

    def runStateBehavior(self, keyWord):
        if keyWord == "Pick":
            setter = self.Pick()
        elif keyWord == "Drop":
            setter = self.Drop()
        elif keyWord == "Consume":
            setter = self.Consume()
        elif keyWord == "Explore":
            setter = self.Explore()
        elif keyWord == "Den":
            setter = self.Den()
        elif keyWord == "Known":
            setter = self.Known()
        return setter
            
    # functions to taking the output of generate_phenotype and turning it into a runnable program
    def run_phenotype_once(self):
        if self.should_end():
            self.end()
            
        behaviorKey = self.currentState.behavior()
        input = self.runStateBehavior(behaviorKey)
        self.currentState = self.changeState(input)
            
    def generate_SM(self):
        self.SM = StateMachine()
        self.SM.createSM(self.phenotype, self.gene.genotype)
    
    def run_phenotype(self):
        # repeatedly run the phenotype until the should_end is true
        try:
            self.grid.history[self.id].clear() # reset before running again
            self.terminal_functions_run = 0
            self.position = (0,0)
            # self.heading = const.NORTH
            self.grid.update_history(self, self.position)
            self.gene.current_codon = 0
            if self.phenotype is None:
                self.phenotype = self.gene.generate_phenotype(self.rules, "<start>")
            if self.SM is None:
                self.generate_SM()
            self.currentState = self.SM.getStartState()
            while(True):
                self.run_phenotype_once()
        except EndException:
            None
            # reward for food, punish for distance
            # self.gene.cost = np.round((((self.consecutiveFood * const.CONSECUTIVE_FOOD) + (self.food_touched * const.FOOD_INCENTIVE)) - ((self.distance * const.DISTANCEPINCH) + (self.offPath * const.OFFPATHPENALTY))), 2)
            # if self.food_touched == const.FOOD_NUM:
                # self.gene.cost += 50
            #TODO: how big should the diversity addition be? 
            #print("cost: ", self.phenotype, "\n->", self.gene.cost)S
    
    # functions for ending the simulation (terminal_functions_run is probably useless)
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

# if __name__ == "__main__":
#     inputgrid = Grid(const.GRID_WIDTH, const.GRID_HEIGHT) 
    
#     for i in range(5):
#         # need rules
#         a = Agent(grid=inputgrid, gene=Gene([0, 2, 3, 4, 5]))
#         a.run_phenotype()
#         # if a.gene.cost > 10:
#         print("the phenotype is ", a.phenotype)
#         print(inputgrid.printed_history(a))
#         print("cost is ", a.gene.cost)
#         print("_____________________")