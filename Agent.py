import random
from BehaviorTree import BehaviorTree
from StateMachine import StateMachine
from const import DEAD, ISHUNGRY, ISDONE, ISBORED, ISFOOD, ISTIRED, FUNC2
from const import EXPLOREGENE, STATEGENE, ENVIORNTEST, EVO_LIMIT, TERMINALLIMIT
from const import NOVELTYSTANDARD
from Gene import Gene, DNAManager
from Environment import Environment, AgentBody, Den
import numpy as np
import pygame as pyg
# import sys

class AgentMind:
    def __init__(self, DNAmanager, id=None):
        super().__init__()
        if id is None:
            self.id = f'ID{random.randint(0, 1000)}'
        else:
            self.id = id
            
        self.DNA = DNAmanager
        self.DNATested = DNAManager()
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
        self.running = False
        # Agent Stat
        # self.foodLocations = []
        self.stateHistory = []
        # evolution
        self.memoryAgents = []
        self.evoLimit = EVO_LIMIT
        self.evoTimer = 0
        self.isTest = False
        self.foodFound = 0
        
    def printID(self):
        print(f"{self.id}")
        
    def addBody(self, agentBody):
        self.agentBody = agentBody
        
    def isTesting(self):
        self.isTest = True
    
    # def addFoodLocation(self, location):
    #     self.foodLocations.append(location)
    
    # def getKnownFood(self, spot):
    #     return self.foodLocations[spot]
        
    def Pick(self):
        if self.should_end():
            self.end()
            
        self.agentBody.pick()
        
        if self.agentBody.isDead():
            return DEAD  
        if self.agentBody.needFood():
            return ISHUNGRY
        if self.agentBody.checkLoad():
            return ISTIRED
        else:
            return ISDONE
        
    def Drop(self):
        if self.should_end():
            self.end()
            
        self.agentBody.drop()
        
        if self.agentBody.isDead():
            return DEAD 
        if self.agentBody.needFood():
            return ISHUNGRY
        if self.agentBody.checkLoad():
            return ISTIRED
        else:
            return ISDONE
        
    def Consume(self):
        if self.should_end():
            self.end()
        
        self.agentBody.consume()
        
        if self.agentBody.isDead():
            return DEAD
        if self.agentBody.needFood():
            return ISHUNGRY
        if self.agentBody.checkLoad():
            return ISTIRED
        return ISDONE

    def runTreeChildren(self, parent):
        if parent.Name == ISFOOD:
            return parent.Name
        elif parent.Name == ISBORED:
            return parent.Name
        elif parent.Name == "ifFood":
            if self.agentBody.isFoodNear() > 0:
                self.foodFound += 1
                result = True
            else:
                result = False
            return self.runTreeChildren(parent.whichChild(result))
        elif parent.Name == FUNC2:
            for x in range(parent.maxChildren):
                result = self.runTreeChildren(parent.getChild(x))
                if result == ISFOOD:
                    return result
                elif result == ISBORED:
                    return result
                elif result == DEAD:
                    return result
                elif result == ISHUNGRY:
                    return result
                elif result == ISTIRED:
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
        
        clock = pyg.time.Clock() 
        isDone = None
        while isDone != ISBORED and isDone != ISFOOD:
            # print(f'hunger {self.agentBody.hunger}')
            isDone = self.runExploreTree()
            if self.agentBody.isDead():
                return DEAD
            if self.agentBody.needFood():
                return ISHUNGRY
            if self.agentBody.checkLoad():
                return ISTIRED
            if isDone == ISBORED:
                # print(f'treeput {isDone}')
                return isDone
            if isDone == ISFOOD:
                return isDone
            clock.tick(100)
        
        self.sense()
        self.actUpdateExplore()
        self.foodFound = 0
                
    def left(self):
        if self.should_end():
            self.end()

        self.agentBody.left()
            
        if self.agentBody.isDead():
            return DEAD
        if self.agentBody.needFood():
            return ISHUNGRY
        if self.agentBody.checkLoad():
            return ISTIRED
        
    def forward(self):
        if self.should_end():
            self.end()

        self.agentBody.forward()
            
        if self.agentBody.isDead():
            return DEAD
        if self.agentBody.needFood():
            return ISHUNGRY
        if self.agentBody.checkLoad():
            return ISTIRED
    
    def right(self):
        if self.should_end():
            self.end()

        self.agentBody.right()
            
        if self.agentBody.isDead():
            return DEAD
        if self.agentBody.needFood():
            return ISHUNGRY
        if self.agentBody.checkLoad():
            return ISTIRED
            
    def Den(self):
        if self.should_end():
            self.end()

        if self.agentBody.denGoToo() == "continue":
            return "continue"
        
        if self.agentBody.isDead():
            return DEAD 
        else:
            return ISDONE
        
    def Known(self):
        if self.should_end():
            self.end()
            
        if self.agentBody.isDead():
            return DEAD
        
        if self.agentBody.getHomeFoodSize() <= 0:
            return ISBORED
        elif self.agentBody.getHomeFoodSize() > 0:
            self.agentBody.known()
        
        if self.agentBody.isFoodNear() is True:
            return ISFOOD
        if self.agentBody.needFood():
            return ISHUNGRY
        if self.agentBody.checkLoad():
            return ISTIRED
        else:
            return ISDONE

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
        
        if setter == DEAD:
            setter = self.Den()
        if setter != "continue":
            # print(f"{setter} agent{self.id}")
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
            if f"({ISFOOD})" in self.StatePhenotype:
                inputsAvailable.append(ISFOOD)
            if f"({ISTIRED})" in self.StatePhenotype:
                inputsAvailable.append(ISTIRED)
            if f"({ISHUNGRY})" in self.StatePhenotype:
                inputsAvailable.append(ISHUNGRY)
            if f"({ISBORED})" in self.StatePhenotype:
                inputsAvailable.append(ISBORED)
            if f"({ISDONE})" in self.StatePhenotype:
                inputsAvailable.append(ISDONE)
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
            # print("runagent setup done")
            clock = pyg.time.Clock() 
            if self.currentState is not None:
                while(self.running):
                    self.runStateBehavior()
                    # print(f"{self.id}")
                    clock.tick(100)
            else:
                print("dead agent; no start state")
        except EndException:
            self.running = False
            self.score = self.agentBody.getHomeScore()
    
    def printStateHistory(self):
        for state in self.stateHistory:
            print(state)
        
    def should_end(self):
        self.terminal_functions_run += 1
        # print(f'{self.id} DEATH INCOMEING {self.terminal_functions_run}')
        if self.terminal_functions_run >= TERMINALLIMIT:
            return True
        return False

    def end(self):
        raise EndException("End of simulation")
    
    def sense(self):
        self.memoryAgents.clear()
        agents = self.agentBody.checkForAgents()
        # print(f"{len(agents)} and {self.id}")
        for agentBody in agents:
            # print(f"I can seeeeee {self.id}")
            self.memoryAgents.append(agentBody.agentBrain)
    
    def noveltyFoodSelect(self, genes):
        totalFood = 0
        for gene in genes:
            totalFood += gene.score
        popAverage = np.round((totalFood / len(genes)), 2)
        novelAgents = []
        for gene in genes:
            if np.abs(popAverage - gene.score) > (popAverage * NOVELTYSTANDARD):
                novelAgents.append(gene)
        return novelAgents
    
    def getDNAStateChild(self):
        stateGenes = []
        for agent in self.memoryAgents:
            currState = agent.DNATested.getGene(STATEGENE)
            stateGenes.append(currState)
        
        novelParents = self.noveltyFoodSelect(stateGenes)
        newGene = []
        if len(novelParents) > 0:
            for y in range(len(novelParents[0].genotype)):
                randGene = random.randint(0, len(novelParents) - 1)
                newGene.append(novelParents[randGene].genotype[y])
            stateChild = Gene(newGene).mutate()
        else:
            stateChild = Gene(self.DNA.getGene(STATEGENE).genotype).mutate()
            
        return stateChild
        
    def actUpdateState(self):
        homeScore = self.agentBody.home.intervalFood
        if homeScore != 0:
            evoScore = homeScore + (self.agentBody.foodInterval * (self.agentBody.foodInterval / homeScore))
        else: 
            evoScore = 0
        self.DNA.getGene(STATEGENE).score = evoScore
        if self.DNATested.getGene(STATEGENE).score < self.DNA.getGene(STATEGENE).score:
            self.DNATested.addGene(STATEGENE, self.DNA.getGene(STATEGENE))
        self.memoryAgents.append(self)
        newDNA = self.getDNAStateChild()
        self.DNA.addGene(STATEGENE, newDNA)
        self.generate_StateMachine()
    
    def noveltyFoundSelect(self, genes):
        totalFound = 0
        for gene in genes:
            totalFound += gene.score
        popAverage = np.round((totalFound / len(genes)), 2)
        novelAgents = []
        for gene in genes:
            if np.abs(popAverage - gene.score) > (popAverage * NOVELTYSTANDARD):
                novelAgents.append(gene)
        return novelAgents
    
    def getDNAExploreChild(self):
        exploreGenes = []
        for agent in self.memoryAgents:
            currExplore = agent.DNA.getGene(EXPLOREGENE)
            exploreGenes.append(currExplore)
        
        novelParents = self.noveltyFoundSelect(exploreGenes)
        newGene = []
        if len(novelParents) > 0:
            for y in range(len(novelParents[0].genotype)):
                randGene = random.randint(0, len(novelParents) - 1)
                newGene.append(novelParents[randGene].genotype[y])
            exploreChild = Gene(newGene).mutate()
        else:
            exploreChild = Gene(self.DNA.getGene(EXPLOREGENE).genotype).mutate()
            
        return exploreChild
            
    def actUpdateExplore(self):
        self.DNA.getGene(EXPLOREGENE).score = self.foodFound
        if self.DNATested.getGene(EXPLOREGENE).score < self.DNA.getGene(EXPLOREGENE).score:
            self.DNATested.addGene(EXPLOREGENE, self.DNA.getGene(EXPLOREGENE))
        self.memoryAgents.append(self)
        newDNA = self.getDNAExploreChild()
        self.DNA.addGene(EXPLOREGENE, newDNA)
        self.generate_ExploreTree()
    
    def runChildrenTests(self, fakeAgents):
        testEnvironment = Environment()
        base = Den(testEnvironment, (ENVIORNTEST // 2, ENVIORNTEST // 2))
        
        for agent in fakeAgents:
            base.testReset()
            testEnvironment.testEvoSetup()
            # maxFood = testEnvironment.numFood
            agentObject = AgentBody(testEnvironment, base.center, agent, base)
            agent.addBody(agentObject)
            testEnvironment.addNewObject(agentObject)
            agent.isTesting()
            agent.runAgent()
            # print(f'num {agent.agentBody.numFood} agent {agent.agentBody.numFood + agent.agentBody.consumedFood} diff {(agent.agentBody.numFood + agent.agentBody.consumedFood) + testEnvironment.numFood} be? old: {maxFood}; new: {testEnvironment.numFood}')

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