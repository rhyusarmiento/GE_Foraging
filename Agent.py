import random
from Gene import Gene
import const as const
from copy import deepcopy
# import numpy as np
from StateMachine import StateMachine
from GGraph import GGraph
from Environment import FoodContainer
import numpy as np
import pygame as py

class Agent:
    def __init__(self, rules, home, worldMap, id='', gene=None) -> None:
        if id == '':
            self.id = f'ID{random.randint(0, 1000)}'
        else:
            self.id = id
        # geno and pheno
        if gene is None:
            genelist = []
            for x in range(const.GENE_LEN):
                num = random.randint(-60, 60)
                while num == 0:
                    num = random.randint(-60, 60)
                genelist.append(num)
            self.gene = Gene(genelist)
        else:
            self.gene = deepcopy(gene)
        
        self.rules = rules
        self.phenotype = None
        # state
        self.SM = None
        self.currentState = None
        self.inputsAvailable = []
        self.isXCor = True
        # oritation
        self.home = home
        self.worldMap = worldMap
        self.locationXY = None
        self.direction = None
        self.heading = "North"
        # simulation
        self.terminal_functions_run = 0
        self.score = 0
        # Agent Stat
        self.numFood = 0
        self.hunger = 500
        self.movement = 0
        self.foodLocations = []
    
    def printID(self):
        print(f"{self.id}ID")
    
    def isDead(self):
        if self.hunger < -10:
            return True
        else:
            return False
        
    def needFood(self):
        if self.hunger < 5:
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
        if self.worldMap.checkSpaceXY((x+1,y+1)) is not None and self.worldMap.checkSpaceXY((x+1,y+1)).who() == "Food":
            self.foodLocations.append((x+1,y+1))
            return True
        if self.worldMap.checkSpaceXY((x+1,y-1)) is not None and self.worldMap.checkSpaceXY((x+1,y-1)).who() == "Food":
            self.foodLocations.append((x+1,y-1))
            return True
        if self.worldMap.checkSpaceXY((x-1,y-1)) is not None and self.worldMap.checkSpaceXY((x-1,y-1)).who() == "Food":
            self.foodLocations.append((x-1,y-1))
            return True
        if self.worldMap.checkSpaceXY((x-1,y+1)) is not None and self.worldMap.checkSpaceXY((x-1,y+1)).who() == "Food":
            self.foodLocations.append((x-1,y+1))
            return True
        else:
            return False
        
    def Pick(self):
        if self.should_end():
            self.end()
            
        x,y = self.locationXY
        if self.worldMap.checkSpaceXY((x + 1,y)) is not None and self.worldMap.checkSpaceXY((x + 1,y)).who() == "Food":
            self.foodLocations.append((x + 1,y))
            if self.worldMap.checkSpaceXY((x + 1,y)).takeFood():
                self.numFood += 1
                self.worldMap.removeFood(1)
            else:
                self.worldMap.removeObjectXY((x+1,y))
        elif self.worldMap.checkSpaceXY((x,y)) is not None and self.worldMap.checkSpaceXY((x,y)).who() == "Food":
            self.foodLocations.append((x,y))
            if self.worldMap.checkSpaceXY((x,y)).takeFood():
                self.numFood += 1
                self.worldMap.removeFood(1)
            else:
                self.worldMap.removeObjectXY((x,y))
        elif self.worldMap.checkSpaceXY((x - 1,y)) is not None and self.worldMap.checkSpaceXY((x-1,y)).who() == "Food":
            self.foodLocations.append((x-1,y))
            if self.worldMap.checkSpaceXY((x-1,y)).takeFood():
                self.numFood += 1
                self.worldMap.removeFood(1)
            else:
                self.worldMap.removeObjectXY((x-1,y))
        elif self.worldMap.checkSpaceXY((x,y-1)) is not None and self.worldMap.checkSpaceXY((x,y-1)).who() == "Food":
            self.foodLocations.append((x,y-1))
            if self.worldMap.checkSpaceXY((x,y-1)).takeFood():
                self.numFood += 1
                self.worldMap.removeFood(1)
            else:
                self.worldMap.removeObjectXY((x,y-1))
        elif self.worldMap.checkSpaceXY((x,y+1)) is not None and self.worldMap.checkSpaceXY((x,y+1)).who() == "Food":
            self.foodLocations.append((x,y+1))
            if self.worldMap.checkSpaceXY((x,y+1)).takeFood():
                self.numFood += 1
                self.worldMap.removeFood(1)
            else:
                self.worldMap.removeObjectXY((x,y+1))
        elif self.worldMap.checkSpaceXY((x + 1,y+1)) is not None and self.worldMap.checkSpaceXY((x + 1,y+1)).who() == "Food":
            self.foodLocations.append((x + 1,y+1))
            if self.worldMap.checkSpaceXY((x + 1,y+1)).takeFood():
                self.numFood += 1
                self.worldMap.removeFood(1)
            else:
                self.worldMap.removeObjectXY((x+1,y+1))
        elif self.worldMap.checkSpaceXY((x+1,y-1)) is not None and self.worldMap.checkSpaceXY((x+1,y-1)).who() == "Food":
            self.foodLocations.append((x+1,y-1))
            if self.worldMap.checkSpaceXY((x+1,y-1)).takeFood():
                self.numFood += 1
                self.worldMap.removeFood(1)
            else:
                self.worldMap.removeObjectXY((x+1,y-1))
        elif self.worldMap.checkSpaceXY((x-1,y-1)) is not None and self.worldMap.checkSpaceXY((x-1,y-1)).who() == "Food":
            self.foodLocations.append((x-1,y-1))
            if self.worldMap.checkSpaceXY((x-1,y-1)).takeFood():
                self.numFood += 1
                self.worldMap.removeFood(1)
            else:
                self.worldMap.removeObjectXY((x-1,y-1))
        elif self.worldMap.checkSpaceXY((x-1,y+1)) is not None and self.worldMap.checkSpaceXY((x-1,y+1)).who() == "Food":
            self.foodLocations.append((x-1,y+1))
            if self.worldMap.checkSpaceXY((x-1,y+1)).takeFood():
                self.numFood += 1
                self.worldMap.removeFood(1)
            else:
                self.worldMap.removeObjectXY((x-1,y+1))
              
        if self.isDead():
            return "Dead"  
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
            self.numFood -= 1
            if self.worldMap.checkSpaceXY(self.locationXY) is not None and self.worldMap.checkSpaceXY(self.locationXY).who() == "Food":
                self.worldMap.checkSpaceXY(self.locationXY).addFood()
            elif self.worldMap.checkSpaceXY(self.locationXY) is not None and self.worldMap.checkSpaceXY(self.locationXY).who() == "Den":
                self.worldMap.checkSpaceXY(self.locationXY).depositFood(1)
            else:
                self.worldMap.inputObjectXY(self.locationXY, FoodContainer())
        
        if self.isDead():
            return "Dead" 
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
        
        if self.isDead():
            return "Dead"
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
        if dir == 0 and not self.heading == "West":
            self.locationXY = (self.worldMap.cleanCor(x-2),self.worldMap.cleanCor(y))
            self.hunger -= .5
            self.heading = "West"
        elif dir == 1 and not self.heading == "East":
            self.locationXY = (self.worldMap.cleanCor(x+2),self.worldMap.cleanCor(y))
            self.hunger -= .5
            self.heading = "East"
        elif dir == 2 and not self.heading == "North":
            self.hunger -= .5
            self.locationXY = (self.worldMap.cleanCor(x),self.worldMap.cleanCor(y+2))
            self.heading = "North"
        elif dir == 3 and not self.heading == "South":
            self.hunger -= .5
            self.heading = "South"
            self.locationXY = (self.worldMap.cleanCor(x),self.worldMap.cleanCor(y-2))

        if self.isDead():
            return "Dead"
        if self.needFood():
            self.movement = 0
            return "isHungry"
        if self.checkFood():
            self.movement = 0
            return "isFood"
        if self.checkLoad():
            return "isTried"
        if self.movement > 500:
            self.movement = 0
            return "isBored"
        else:
            self.movement += 1
            return "continue"
        
    def Den(self):
        if self.should_end():
            self.end()

        if self.locationXY != self.home.locationXY:
            self.direction = tuple(np.subtract(self.home.locationXY, self.locationXY))
            if self.isXCor:
                if self.direction[0] > 0:
                    self.locationXY = (self.locationXY[0] + 1, self.locationXY[1])
                elif self.direction[0] < 0:
                    self.locationXY = (self.locationXY[0] - 1, self.locationXY[1])
                self.isXCor = False
            else:
                if self.direction[1] > 0:
                    self.locationXY = (self.locationXY[0], self.locationXY[1] + 1)
                elif self.direction[1] < 0:
                    self.locationXY = (self.locationXY[0], self.locationXY[1] - 1)
                self.isXCor = True
            self.hunger -= .5
            return "continue" 
        else:
            self.home.depositFood(self.numFood)
            self.numFood = 0
        
            if self.home.isfeed() and self.hunger < 10:
                self.home.foodStored -= 1
                self.hunger += 3
                return "continue"
        if self.isDead():
            return "Dead" 
        else:
            return "isDone"
        
    def Known(self):
        if self.should_end():
            self.end()
            
        if self.isDead():
            return "Dead"
        
        if len(self.foodLocations) <= 0:
            return "isBored"
        
        if self.locationXY != self.foodLocations[0]:
            self.direction = tuple(np.subtract(self.foodLocations[0], self.locationXY))
            if self.isXCor:
                if self.direction[0] > 0:
                    self.locationXY = (self.locationXY[0] + 1, self.locationXY[1])
                elif self.direction[0] < 0:
                    self.locationXY = (self.locationXY[0] - 1, self.locationXY[1])
                self.isXCor = False
            else:
                if self.direction[1] > 0:
                    self.locationXY = (self.locationXY[0], self.locationXY[1] + 1)
                elif self.direction[1] < 0:
                    self.locationXY = (self.locationXY[0], self.locationXY[1] - 1)
                self.isXCor = True
            self.hunger -= .5
            return "continue" 
        
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
        
        if setter == "Dead":
            setter = self.Den()
        if setter != "continue":
            state = self.currentState.changeState(setter)
            if state is not None:
                self.currentState = state
            
    def generate_SM(self):
        self.SM = StateMachine()
        self.SM.createSM(self.phenotype, self.gene.genotype, self.inputsAvailable)
    
    def runAgent(self):
        try:
            self.terminal_functions_run = 0
            self.gene.current_codon = 0
            self.locationXY = self.home.locationXY
            if self.phenotype is None:
                self.phenotype = self.gene.generate_phenotype(self.rules, "<start>")
                if "(isFood)" in self.phenotype:
                    self.inputsAvailable.append("isFood")
                if "(isTired)" in self.phenotype:
                    self.inputsAvailable.append("isTired")
                if "(isHungry)" in self.phenotype:
                    self.inputsAvailable.append("isHungry")
                if "(isBored)" in self.phenotype:
                    self.inputsAvailable.append("isBored")
                if "(isDone)" in self.phenotype:
                    self.inputsAvailable.append("isDone")
            if self.SM is None:
                self.generate_SM()
            self.currentState = self.SM.getStartState()
            running = True
            clock = py.time.Clock() 
            if self.currentState is not None:
                while(running):
                    py.display.flip()
                    for event in py.event.get():
                        if event.type == py.QUIT:
                            running = False
                    self.runStateBehavior()
                    self.worldMap.updateScreen()
                    py.draw.rect(self.worldMap.screen, (50,50,50,50), py.Rect(self.locationXY, (10,10)))
                    clock.tick(60)
                    py.display.update()
            else:
                print("dead agent; no start state")
        except EndException:
            self.score = self.home.foodStored - self.worldMap.numFood
    
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