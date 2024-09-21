import random
from BehaviorTree import BehaviorTree
from StateMachine import StateMachine
from const import DEAD, ISHUNGRY, ISDONE, ISBORED, ISFOOD, ISTIRED, FUNC2
from const import EXPLOREGENE, STATEGENE, ENVIORNTEST, EVO_TIMER, EVO_LIMIT, TERMINALLIMIT
from const import NOVELTYSTANDARD, CROSSOVER_PRODUCTION
from Gene import Gene, DNAManager
from Environment import Environment, AgentBody, Den
import numpy as np
import pygame as pyg
# import sys

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
        self.evoLimit = EVO_LIMIT
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

        isDone = None
        while self.running or isDone != ISBORED or isDone != ISFOOD:
            isDone = self.runExploreTree()
            if self.agentBody.isDead():
                return DEAD
            if self.agentBody.needFood():
                return ISHUNGRY
            if self.agentBody.checkLoad():
                return ISTIRED
            if isDone == ISBORED:
                return isDone
            if isDone == ISFOOD:
                return isDone
                
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
        
        if len(self.foodLocations) <= 0:
            return ISBORED
        elif len(self.foodLocations) > 0:
            return self.agentBody.known()
        
        if self.agentBody.isFoodNear() > 0:
            return ISFOOD
        else:
            self.foodLocations.pop(0)
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
                    clock.tick(180)
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
        
        if self.isTest:
            if self.terminal_functions_run == EVO_TIMER:
                return True
            return False
        else:
            # print(f'{self.id} DEATH INCOMEING {self.terminal_functions_run}')
            if self.evoLimit <= self.evoTimer:
                # print("run Evolution")
                self.sense()
                self.actUpdate()
                # print("done")
                self.evoTimer = 0
            else:
                self.evoTimer += 1
            if self.terminal_functions_run == TERMINALLIMIT:
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
    
    def novelty_select(self, agents):
        totalFood = 0
        for agent in agents:
            totalFood += agent.score
        popAverage = np.round((totalFood / len(agents)), 2)
        novelAgents = []
        for agent in agents:
            if (np.abs(popAverage - agent.score) > popAverage * NOVELTYSTANDARD):
                novelAgents.append(agent)
        return novelAgents
    
    def getDNAChildren(self):
        stateGenes = []
        exploreGenes = []
        for agent in self.memoryAgents:
            currState = agent.DNA.getGene(STATEGENE)
            currExplore = agent.DNA.getGene(EXPLOREGENE)
            stateGenes.append(currState.genotype)
            exploreGenes.append(currExplore.genotype)
        
        stateChildren = []
        for x in range(CROSSOVER_PRODUCTION):
            newGene = []
            for y in range(len(stateGenes[0])):
                randGene = random.randint(0, len(stateGenes) - 1)
                newGene.append(stateGenes[randGene][y])
            stateChildren.append(Gene(newGene).mutate())
            
        exploreChildren = []
        for x in range(CROSSOVER_PRODUCTION):
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
        base = Den(testEnvironment, (ENVIORNTEST // 2, ENVIORNTEST // 2))
        
        for agent in fakeAgents:
            base.testReset()
            testEnvironment.testReset()
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