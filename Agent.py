import random
from Gene import Gene
import const as const
from copy import deepcopy
# import numpy as np
from StateMachine import StateMachine
from GGraph import GGraph
from Environment import FoodContainer

class Agent:
    def __init__(self, rules, home, worldMap, id='', gene=None) -> None:
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
        
        self.home = home
        self.worldMap = worldMap
        self.locationXY = None
        
        self.terminal_functions_run = 0
        
        self.numFood = 0
        self.hunger = 10
        self.movement = 0
        self.foodLocations = []
    
    def printID(self):
        print(f"{self.id}ID")
    
    def needFood(self):
        if self.hunger < 2:
            return True
        else: 
            return False
    
    def checkLoad(self):
        if self.numFood > 10:
            return True
        else:
            return False
        
    def checkFood(self):
        x,y = self.locationXY
        if self.worldMap.checkSpaceXY((x + 1,y)) is not None and self.worldMap.checkSpaceXY((x + 1,y)).who() == "Food":
            self.foodLocations.append((x+1,y))
            return True
        if self.worldMap.checkSpaceXY((x - 1,y)) is not None and self.worldMap.checkSpaceXY((x-1,y)).who() == "Food":
            self.foodLocations.append((x-1,y))
            return True
        if self.worldMap.checkSpaceXY((x,y-1)) is not None and self.worldMap.checkSpaceXY((x,y-1)).who() == "Food":
            self.foodLocations.append((x,y-1))
            return True
        if self.worldMap.checkSpaceXY((x,y+1)) is not None and self.worldMap.checkSpaceXY((x,y+1)).who() == "Food":
            self.foodLocations.append((x,y+1))
            return True
        if self.worldMap.checkSpaceXY((x,y)) is not None and self.worldMap.checkSpaceXY((x,y)).who() == "Food":
            self.foodLocations.append((x,y))
            return True
        else:
            return False
        
    def Pick(self):
        if self.should_end():
            self.end()
            
        x,y = self.locationXY
        if self.worldMap.checkSpaceXY((x + 1,y)) is not None and self.worldMap.checkSpaceXY((x+1,y)).who() == "Food":
            self.foodLocations.append((x+1,y))
            if self.worldMap.checkSpaceXY((x+1,y)).takeFood():
                self.numFood += 1
            else:
                self.worldMap.removeObjectXY((x+1,y))
        elif self.worldMap.checkSpaceXY((x,y)) is not None and self.worldMap.checkSpaceXY((x,y)).who() == "Food":
            self.foodLocations.append((x,y))
            if self.worldMap.checkSpaceXY((x,y)).takeFood():
                self.numFood += 1
            else:
                self.worldMap.removeObjectXY((x,y))
        elif self.worldMap.checkSpaceXY((x - 1,y)) is not None and self.worldMap.checkSpaceXY((x-1,y)).who() == "Food":
            self.foodLocations.append((x-1,y))
            if self.worldMap.checkSpaceXY((x-1,y)).takeFood():
                self.numFood += 1
            else:
                self.worldMap.removeObjectXY((x-1,y))
        elif self.worldMap.checkSpaceXY((x,y-1)) is not None and self.worldMap.checkSpaceXY((x,y-1)).who() == "Food":
            self.foodLocations.append((x,y-1))
            if self.worldMap.checkSpaceXY((x,y-1)).takeFood():
                self.numFood += 1
            else:
                self.worldMap.removeObjectXY((x,y-1))
        elif self.worldMap.checkSpaceXY((x,y+1)) is not None and self.worldMap.checkSpaceXY((x,y+1)).who() == "Food":
            self.foodLocations.append((x,y+1))
            if self.worldMap.checkSpaceXY((x,y+1)).takeFood():
                self.numFood += 1
            else:
                self.worldMap.removeObjectXY((x,y+1))
                
        if self.needFood():
            return "isHungry"
        if self.checkLoad():
            return "isTried"
        else:
            return "isDone"
        
    def Drop(self):
        if self.should_end():
            self.end()
            
        if self.numFood > 0:
            if self.worldMap.checkSpaceXY(self.locationXY) is not None and self.worldMap.checkSpaceXY(self.locationXY).who() == "Food":
                self.worldMap.checkSpaceXY(self.locationXY).addFood()
            elif self.worldMap.checkSpaceXY(self.locationXY) is not None and self.worldMap.checkSpaceXY(self.locationXY).who() == "Den":
                self.worldMap.checkSpaceXY(self.locationXY).depositFood(1)
            else:
                self.worldMap.inputObjectXY(self.locationXY, FoodContainer(1))
            self.numFood -= 1
        if self.needFood():
            return "isHungry"
        if self.checkLoad():
            return "isTried"
        else:
            return "isDone"
        
    def Consume(self):
        if self.should_end():
            self.end()
        
        if self.numFood > 0:
            self.numFood -= 1
            self.hunger += 3
        if self.needFood():
            return "isHungry"
        if self.checkLoad():
            return "isTried"
        return "isDone"
        
    def Explore(self):
        if self.should_end():
            self.end()
        dir = random.randint(0,3)
        x,y = self.locationXY
        if dir == 0:
            self.locationXY = (self.worldMap.cleanCor(x-1),self.worldMap.cleanCor(y))
            self.hunger -= .5
        elif dir == 1:
            self.locationXY = (self.worldMap.cleanCor(x+1),self.worldMap.cleanCor(y))
            self.hunger -= .5
        elif dir == 2:
            self.hunger -= .5
            self.locationXY = (self.worldMap.cleanCor(x),self.worldMap.cleanCor(y+1))
        elif dir == 3:
            self.hunger -= .5
            self.locationXY = (self.worldMap.cleanCor(x),self.worldMap.cleanCor(y-1))

        if self.checkFood():
            self.movement = 0
            return "isFood"
        if self.needFood():
            self.movement = 0
            return "isHungry"
        if self.checkLoad():
            return "isTried"
        if self.movement > 15:
            self.movement = 0
            return "isBored"
        else:
            self.movement += 1
            return "continue"
        
    def Den(self):
        if self.should_end():
            self.end()

        self.hunger -= 1
        x,y = self.home.locationXY
        self.locationXY = (x,y)
        self.home.depositFood(self.numFood)
        self.numFood = 0
        
        if self.home.isfeed() and self.hunger < 10:
            self.home.foodStored -= 1
            self.hunger += 3
            return "continue"
        else:
            return "isDone"
        
    def Known(self):
        if self.should_end():
            self.end()
        if len(self.foodLocations) <= 0:
            return "isBored"
        
        self.hunger -= 1
        x,y = self.foodLocations[0]
        self.locationXY = (x,y)
        if self.checkFood():
            return "isFood"
        else:
            self.foodLocations.pop(0)
        if self.needFood():
            return "isHungry"
        if self.checkLoad():
            return "isTried"
        else:
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
            state = self.currentState.changeState(setter)
            if state is not None:
                self.currentState = state
            
    def generate_SM(self):
        self.SM = StateMachine()
        self.SM.createSM(self.phenotype, self.gene.genotype)
    
    def runAgent(self):
        try:
            self.terminal_functions_run = 0
            self.gene.current_codon = 0
            self.locationXY = self.home.locationXY
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
        if self.terminal_functions_run == 500:
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