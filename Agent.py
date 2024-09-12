import random
from BehaviorTree import BehaviorTree
import const as const
# import numpy as np
from StateMachine import StateMachine
from const import EXPLOREGENE, STATEGENE, CROSSOVER_PRODUCTION, ENVIORNTEST, TOTALFOOD, ENVIORN_DIM
from Gene import Gene, DNAManager
from Environment import Environment, AgentBody, Den
import numpy as np
# import pygame as py

# TODO: maybe move known food to body then inherit body
class AgentMind:
    def __init__(self, DNAManager, id=None):
        super().__init__()
        if id is None:
            self.id = f'ID{random.randint(0, 1000)}'
        else:
            self.id = id
            
        self.DNA = DNAManager
        self.StatePhenotype = None
        self.BehaviorPhenotype = None
        # state and behavior
        self.ExploreTree = None
        self.StateMachine = None
        self.currentState = None
        # # oritation
        self.agentBody = None
        # simulation
        self.terminal_functions_run = 0
        self.score = 0
        self.running = False
        # Agent Stat
        self.foodLocations = []
        self.stateHistory = []
        # evolution
        self.memoryAgents = []
        self.evoLimit = 20
        self.evoTimer = 0
        self.isTest = False
        
    def printID(self):
        print(f"{self.id}")
        
    def addBody(self, agentBody):
        self.agentBody = agentBody
        
    def isTesting(self):
        self.isTest = True
    
    def addFoodLocation(self, location):
        self.foodLocations.append(location)
    
    def getKnownFood(self, spot):
        return self.foodLocations[spot]
        
    def Pick(self):
        if self.should_end():
            self.end()
            
        self.agentBody.pick()
        
        if self.agentBody.isDead():
            return "Dead"  
        if self.agentBody.needFood():
            return "isHungry"
        if self.agentBody.checkLoad():
            return "isTried"
        else:
            return "isDone"
        
    def Drop(self):
        if self.should_end():
            self.end()
            
        self.agentBody.drop()
        
        if self.agentBody.isDead():
            return "Dead" 
        if self.agentBody.needFood():
            return "isHungry"
        if self.agentBody.checkLoad():
            return "isTried"
        else:
            return "isDone"
        
    def Consume(self):
        if self.should_end():
            self.end()
        
        self.agentBody.consume()
        
        if self.agentBody.isDead():
            return "Dead"
        if self.agentBody.needFood():
            return "isHungry"
        if self.agentBody.checkLoad():
            return "isTried"
        return "isDone"

    def runTreeChildren(self, parent):
        if parent.Name == "isFood":
            return parent.Name
        elif parent.Name == "isBored":
            return parent.Name
        elif parent.Name == "ifFood":
            result = self.agentBody.checkFood()
            return self.runTreeChildren(parent.whichChild(result))
        elif parent.Name == "func2":
            for x in range(parent.maxChildren):
                result = self.runTreeChildren(parent.getChild(x))
                if result == "isFood":
                    return result
                elif result == "isBored":
                    return result
                elif result == "Dead":
                    return result
                elif result == "isHungry":
                    return result
                elif result == "isTried":
                    return result
        elif parent.Name == "left":
            return self.left()
        elif parent.Name == "forward":
            return self.forward()
        elif parent.Name == "right":
            return self.right()
            
    def runExploreTree(self):
        if self.ExploreTree.root.Name is None:
            print("no tree provided")
            self.end()
        else:
            return self.runTreeChildren(self.ExploreTree.root)
        
    def Explore(self):
        if self.should_end():
            self.end()

        isDone = None
        while self.running or isDone != "isBored" or isDone != "isFood":
            isDone = self.runExploreTree()
            if self.agentBody.isDead():
                return "Dead"
            if self.agentBody.needFood():
                return "isHungry"
            if self.agentBody.checkLoad():
                return "isTried"
            if isDone == "isBored":
                return isDone
            if isDone == "isFood":
                return isDone
                
    def left(self):
        if self.should_end():
            self.end()

        self.agentBody.left()
            
        if self.agentBody.isDead():
            return "Dead"
        if self.agentBody.needFood():
            return "isHungry"
        if self.agentBody.checkLoad():
            return "isTried"
        
    def forward(self):
        if self.should_end():
            self.end()

        self.agentBody.forward()
            
        if self.agentBody.isDead():
            return "Dead"
        if self.agentBody.needFood():
            return "isHungry"
        if self.agentBody.checkLoad():
            return "isTried"
    
    def right(self):
        if self.should_end():
            self.end()

        self.agentBody.right()
            
        if self.agentBody.isDead():
            return "Dead"
        if self.agentBody.needFood():
            return "isHungry"
        if self.agentBody.checkLoad():
            return "isTried"
            
    def Den(self):
        if self.should_end():
            self.end()

        if self.agentBody.denGoToo() == "continue":
            return "continue"
        
        if self.agentBody.isDead():
            return "Dead" 
        else:
            return "isDone"
        
    def Known(self):
        if self.should_end():
            self.end()
            
        if self.agentBody.isDead():
            return "Dead"
        
        if len(self.foodLocations) <= 0:
            return "isBored"
        elif len(self.foodLocations) > 0:
            return self.agentBody.known()
        
        if self.agentBody.checkFood():
            return "isFood"
        else:
            self.foodLocations.pop(0)
        if self.agentBody.needFood():
            return "isHungry"
        if self.agentBody.checkLoad():
            return "isTried"
        else:
            return "isDone"

    def runStateBehavior(self):            
        behaviorKey = self.currentState.behavior()
        self.stateHistory.append(behaviorKey)
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
            
    def generate_StateMachine(self):
        inputsAvailable = []
        self.StatePhenotype = self.DNA.getGenePhenotype(STATEGENE)
        if self.StatePhenotype is None:
            self.running = False
            print("no state phenotype provided")
        else:
            if "(isFood)" in self.StatePhenotype:
                inputsAvailable.append("isFood")
            if "(isTired)" in self.StatePhenotype:
                inputsAvailable.append("isTired")
            if "(isHungry)" in self.StatePhenotype:
                inputsAvailable.append("isHungry")
            if "(isBored)" in self.StatePhenotype:
                inputsAvailable.append("isBored")
            if "(isDone)" in self.StatePhenotype:
                inputsAvailable.append("isDone")
            self.StateMachine = StateMachine() 
            self.StateMachine.createStateMachine(self.StatePhenotype, self.DNA.getGene(STATEGENE).genotype, inputsAvailable)
        
    def generate_ExploreTree(self):
        self.BehaviorPhenotype = self.DNA.getGenePhenotype(EXPLOREGENE)
        if self.BehaviorPhenotype is None:
            self.running = False
            print("no Behavior phenotype provided")
        else:
            self.ExploreTree = BehaviorTree(self.BehaviorPhenotype)
    
    def runAgent(self):
        try:
            self.running = True
            self.score = 0
            self.evoTimer = 0
            self.terminal_functions_run = 0
            if self.StateMachine is None:
                self.generate_StateMachine()
            if self.ExploreTree is None:
                self.generate_ExploreTree()
            self.currentState = self.StateMachine.getStartState()
            # clock = py.time.Clock() 
            if self.currentState is not None:
                while(self.running):
                    # py.display.flip()
                    # for event in py.event.get():
                    #     if event.type == py.QUIT:
                    #         running = False
                    self.runStateBehavior()
                    # self.worldMap.updateScreen()
                    # py.draw.rect(self.worldMap.screen, (50,50,50,50), py.Rect(self.locationXY, (10,10)))
                    # clock.tick(60)
                    # py.display.update()
            else:
                print("dead agent; no start state")
        except EndException:
            self.score = self.agentBody.getHomeScore()
    
    def printStateHistory(self):
        for state in self.stateHistory:
            print(state)
        
    def should_end(self):
        self.terminal_functions_run += 1
        if self.evoLimit <= self.evoTimer:
            self.sense()
            self.actUpdate()
            self.evoTimer = 0
        else:
            self.evoTimer += 1
        
        if self.isTest:
            if self.terminal_functions_run == 200:
                return True
            return False
        else:
            if self.terminal_functions_run == 1000:
                return True
            return False
    
    def end(self):
        raise EndException("End of simulation")
    
    def sense(self):
        self.memoryAgents.clear()
        self.memoryAgents.extend(self.agentBody.checkForAgents())     
    
    def novelty_select(self, agents):
        totalFood = 0
        for agent in agents:
            totalFood += agent.score
        popAverage = np.round((totalFood / len(agents)), 2)
        novelAgents = []
        for agent in agents:
            if (np.abs(popAverage - agent.score) > popAverage * .8):
                novelAgents.append(agent)
        return novelAgents
    
    def getDNAChildren(self):
        stateGenes = []
        exploreGenes = []
        for agent in self.memorAgents:
            stateGenes.append(agent.DNA.getGene(STATEGENE).genotype)
            exploreGenes.append(agent.DNA.getGene(EXPLOREGENE).genotype)
        
        stateChildren = []
        for x in range(CROSSOVER_PRODUCTION * len(stateGenes)):
            newGene = []
            for y in range(len(stateGenes[0])):
                randGene = random.randint(0, len(stateGenes) - 1)
                newGene.append(stateGenes[randGene][y])
            stateChildren.append(Gene(newGene).mutate())
            
        exploreChildren = []
        for x in range(CROSSOVER_PRODUCTION * len(exploreGenes)):
            newGene = []
            for y in range(len(exploreGenes[0])):
                randGene = random.randint(0, len(exploreGenes) - 1)
                newGene.append(exploreGenes[randGene][y])
            exploreChildren.append(Gene(newGene).mutate())
            
        dnaPackets = []
        for x in range(len(stateChildren)):
            dna = DNAManager()
            dna.addGene(STATEGENE, stateChildren[x])
            dna.addGene(EXPLOREGENE, exploreChildren[x])
            dnaPackets.append(dna)
            
        return dnaPackets
        
    def actUpdate(self):
        # self.projectionresult = 0
        # self.mutateresult = 0
        self.memoryAgents.append(self)
        childrenDNA = self.getDNAChildren()
        fakeAgents = []
        incre = 0
        while(incre < len(childrenDNA)):
            a = AgentMind(childrenDNA[incre])
            fakeAgents.append(a)
            incre += 1
        self.runChildrenTests(fakeAgents)
        novelFoodAgents = self.novelty_select(fakeAgents)
        # update
        if len(novelFoodAgents) > 0:
            num = random.randint(0, len(novelFoodAgents) - 1)
            self.DNA = novelFoodAgents[num].DNA
            self.generate_StateMachine()
            self.generate_ExploreTree()
            # self.projectionresult += 1 
        else:
            self.DNA.mutateGenes()
            self.generate_StateMachine()
            self.generate_ExploreTree()
            # self.mutateresult += 1
    
    def runChildrenTests(self, fakeAgents):
        testEnvironment = Environment()
        base = Den(testEnvironment, (ENVIORN_DIM // 2, ENVIORN_DIM // 2))
        
        for agent in fakeAgents:
            testEnvironment.testSetUp()
            agentObject = AgentBody(testEnvironment, base.center, agent, base)
            agent.addBody(agentObject)
            testEnvironment.addNewObject(base)
            testEnvironment.addNewObject(agentObject)
            agent.isTesting()
            agent.runAgent()
            testEnvironment.clearAll()

class EndException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

if __name__ == "__main__":
    # ggraph = GGraph(const.RULES)
    # ggraph.printGraph()
    print("Agent:")
    # agent = AgentMind(ggraph)
    # agent.setup()
    # agent.StateMachine.printStateMachine()