import random
from BehaviorTree import BehaviorTree
from StateMachine import StateMachine
from const import DEAD, ISHUNGRY, ISDONE, ISBORED, ISFOOD, ISTIRED, FUNC2, AGENTCOLOR, BLACK, BLUE, YELLOW, ORAGNE, PURPLE
from const import EXPLOREGENE, STATEGENE, ENVIORNTEST, EVO_LIMIT, TERMINALLIMIT, EVO_SEC
from const import NOVELTYSTANDARD, POPLUATIONTOLERANCE, NUMAGENTS
from Gene import Gene
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
            
        self.DNATesting = DNAmanager
        self.DNATested = DNAmanager
        self.StatePhenotypeTesting = None
        self.BehaviorPhenotypeTesting = None
        self.StatePhenotypeTested = None
        self.BehaviorPhenotypeTested = None
        # state and behavior
        self.ExploreTreeTested = None
        self.ExploreTreeTesting = None
        self.StateMachineTesting = None
        self.StateMachineTested = None
        self.currentStateTested = None
        self.currentStateTested = None
        # # oritation
        self.agentBody = None
        # simulation
        self.terminal_functions_run = 0
        self.running = False
        # Agent Stat
        # self.foodLocations = []
        self.stateHistory = []
        # evolution
        self.memoryAgents = set()
        self.evoLimit = EVO_LIMIT
        self.evoTimer = 0
        self.isTest = False
        self.foodFound = 0
        self.runExploreTesting = False
        self.runStateTesting = False
        self.runStateTurn = True
        self.runExploreTurn = True
        
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
        self.agentBody.color = BLACK
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
        self.agentBody.color = PURPLE
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
        self.agentBody.color = ORAGNE
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
            
    def runExploreTreeTesting(self):
        if self.ExploreTreeTesting.root.Name is None:
            print("no tree provided")
            self.end()
        else:
            return self.runTreeChildren(self.ExploreTreeTesting.root)
        
    def runExploreTreeTested(self):
        if self.ExploreTreeTested.root.Name is None:
            print("no tree provided")
            self.end()
        else:
            return self.runTreeChildren(self.ExploreTreeTested.root)
        
    def Explore(self):
        self.agentBody.color = BLUE
        if self.should_end():
            self.end()
        
        clock = pyg.time.Clock() 
        isDone = None
        while isDone != ISBORED and isDone != ISFOOD:
            # print(f'{self} is increment {self.terminal_functions_run}')
            if self.runExploreTesting is True:
                isDone = self.runExploreTreeTesting()
            else:
                isDone = self.runExploreTreeTested()
                
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
        self.agentBody.color = AGENTCOLOR
        
        if self.should_end():
            self.end()

        if self.agentBody.denGoToo() == "continue":
            return "continue"
        
        if self.agentBody.isDead():
            return DEAD 
        else:
            return ISDONE
        
    def Known(self):
        self.agentBody.color = YELLOW
        
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
        
    def runStates(self, behaviorKey):
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
            # print(f"bro dead {self}")
            setter = self.Den() 
        return setter

    def runStateTestingBehavior(self):
        behaviorKey = self.currentStateTesting.behavior()
        doneVal = self.runStates(behaviorKey)
        # print(f"yo testing {doneVal}")
        if doneVal != "continue":
            state = self.currentStateTesting.changeState(doneVal)
            if state is not None:
                self.currentStateTesting = state
            else:
                # print("BAd Testing FSM")
                self.currentStateTesting = self.StateMachineTesting.getStartState()

    def runStateTestedBehavior(self):            
        # self.stateHistory.append(behaviorKey)
        behaviorKey = self.currentStateTested.behavior()
        doneVal = self.runStates(behaviorKey)
        # print(f"yo tested {doneVal}")
        if doneVal != "continue":
            state = self.currentStateTested.changeState(doneVal)
            if state is not None:
                self.currentStateTested = state
            else:
                # print("BAd Tested FSM")
                self.currentStateTested = self.StateMachineTested.getStartState()
            
    def findInputAvail(self, inputList, searchString):
        if f"({ISFOOD})" in searchString:
            inputList.append(ISFOOD)
        if f"({ISTIRED})" in searchString:
            inputList.append(ISTIRED)
        if f"({ISHUNGRY})" in searchString:
            inputList.append(ISHUNGRY)
        if f"({ISBORED})" in searchString:
            inputList.append(ISBORED)
        if f"({ISDONE})" in searchString:
            inputList.append(ISDONE)
        
    def generate_StateMachineTesting(self):
        inputsAvailable = []
        self.StatePhenotypeTesting = self.DNATesting.getGenePhenotype(STATEGENE)
        if self.StatePhenotypeTesting is None:
            self.running = False
            print("no state phenotype provided")
        else:
            self.findInputAvail(inputsAvailable, self.StatePhenotypeTesting)
            self.StateMachineTesting = StateMachine() 
            self.StateMachineTesting.createStateMachine(self.StatePhenotypeTesting)
        
    def generate_StateMachineTested(self):
        inputsAvailable = []
        self.StatePhenotypeTested = self.DNATested.getGenePhenotype(STATEGENE)
        if self.StatePhenotypeTested is None:
            self.running = False
            print("no state phenotype provided")
        else:
            self.findInputAvail(inputsAvailable, self.StatePhenotypeTested)
            self.StateMachineTested = StateMachine() 
            self.StateMachineTested.createStateMachine(self.StatePhenotypeTested)
    
    def generate_ExploreTreeTesting(self):
        self.BehaviorPhenotypeTesting = self.DNATesting.getGenePhenotype(EXPLOREGENE)
        if self.BehaviorPhenotypeTesting is None:
            self.running = False
            print("no Behavior phenotype provided")
        else:
            self.ExploreTreeTesting = BehaviorTree(self.BehaviorPhenotypeTesting)
            
    def generate_ExploreTreeTested(self):
        self.BehaviorPhenotypeTested = self.DNATested.getGenePhenotype(EXPLOREGENE)
        if self.BehaviorPhenotypeTested is None:
            self.running = False
            print("no Behavior phenotype provided")
        else:
            self.ExploreTreeTested = BehaviorTree(self.BehaviorPhenotypeTested)
    
    def runAgent(self):
        try:
            self.running = True
            self.score = 0
            self.evoTimer = 0
            self.terminal_functions_run = 0
            if self.StateMachineTesting is None:
                self.generate_StateMachineTesting()
            if self.StateMachineTested is None:
                self.generate_StateMachineTested()
            if self.ExploreTreeTesting is None:
                self.generate_ExploreTreeTesting()
            if self.ExploreTreeTested is None:
                self.generate_ExploreTreeTested()
            self.currentStateTesting = self.StateMachineTesting.getStartState()
            self.currentStateTested = self.StateMachineTested.getStartState()
            # print("runagent setup done")
            clock = pyg.time.Clock() 
            numSec = 0
            if self.currentStateTested is not None:
                while(self.running):
                    numSec += 1
                    if numSec == EVO_SEC:
                        if self.agentBody.home.CurrentFoodVelocityAvg == 0:
                            print(f"{self.id} bad poputation")
                            # or self.agentBody.home.CurrentFoodAcclerAvg < 0
                            self.sense()
                            self.actUpdateState()
                        elif self.agentBody.center == self.agentBody.home.center and self.agentBody.home.intervalFood / NUMAGENTS > self.agentBody.foodDepositInterval:
                            print(f"{self.id} bad self")
                            
                            self.sense()
                            self.actUpdateState()
                        numSec = 0
                    else:
                        if self.runExploreTesting is True:
                            self.runExploreTreeTesting()
                        else:
                            self.runExploreTreeTested()
                        
                        if self.runStateTesting is False:
                            self.runStateTestedBehavior()
                            # print(f"istested {self.id}")
                        else:
                            self.runStateTestingBehavior()
                            # print(f"istesting {self.id}")       
                    clock.tick(60)
                    # print(f"{self.id}")
            else:
                print("dead agent; no start state")
        except EndException:
            print(f"{self.id} i died")
            self.running = False
    
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
            self.memoryAgents.add(agentBody.agentBrain)
    
    def noveltyFoodSelect(self, genes):
        totalFoodScore = 0
        for gene in genes:
            totalFoodScore += gene.score
        popAverage = totalFoodScore / len(genes)
        novelAgents = []
        for gene in genes:
            if gene.score > (popAverage * NOVELTYSTANDARD):
                novelAgents.append(gene)
        return novelAgents
    
    def getDNAStateChild(self):
        stateGenes = []
        for agent in self.memoryAgents:
            currState = agent.DNATested.getGene(STATEGENE)
            stateGenes.append(currState)
        
        totalFoodScore = 0
        for gene in stateGenes:
            totalFoodScore += gene.score
        popAverage = totalFoodScore / len(stateGenes)
        
        if self.DNATested.getGene(STATEGENE).score <= (popAverage * POPLUATIONTOLERANCE) and len(stateGenes) > 1:
            self.runStateTesting = True
            novelParents = self.noveltyFoodSelect(stateGenes)
            newGene = []
            # print(f"novel parents {len(novelParents)}")
            if len(novelParents) > 0:
                selfGene = self.DNATested.getGene(STATEGENE)
                geneSegment = self.DNATested.crossoverProduction(novelParents, selfGene, STATEGENE)
                newGene.extend(geneSegment)
                if len(newGene) > 300:
                    print(f"houston {newGene}")
                stateChild = Gene(newGene)
                # stateChild.mutate()
            else:
                newGene = self.DNATested.mutation(self.DNATested.getGene(STATEGENE))
                if len(newGene) > 300:
                    print(f"houston {newGene}")
                stateChild = Gene(newGene)

        else:
            stateChild = None
            
        # if self.runStateTurn:
        #     self.runStateTurn = False
        # else:
        #     self.runStateTurn = True
        
        return stateChild
        
    def actUpdateState(self):
        if self.runStateTesting is True:
            evoScore = 2*(self.agentBody.foodDepositInterval) + self.agentBody.totalFoodInterval
            # + self.agentBody.home.intervalFood / NUMAGENTS
            self.DNATesting.getGene(STATEGENE).score = evoScore
            self.agentBody.foodDepositInterval = 0
            self.agentBody.totalFoodInterval = 0
            
        self.runStateTesting = False
        if self.DNATested.getGene(STATEGENE).score <= self.DNATesting.getGene(STATEGENE).score:
            self.DNATested.addGene(STATEGENE, self.DNATesting.getGene(STATEGENE))
        # self.memoryAgents.add(self)
        newGene = self.getDNAStateChild()
        if self.runStateTesting is True:
            # print(f"testing State {self.id}")
            if len(newGene.genotype) > 300:
                print(f"houston {newGene.genotype}")
            self.DNATesting.addGene(STATEGENE, newGene)
            self.generate_StateMachineTesting()
            # Test here for solid mutation
    
    def noveltyFoundSelect(self, genes):
        totalFound = 0
        for gene in genes:
            totalFound += gene.score
        popAverage = np.round((totalFound / len(genes)), 2)
        novelAgents = []
        for gene in genes:
            # Formula check novel parent
            if gene.score > (popAverage * NOVELTYSTANDARD):
                novelAgents.append(gene)
        return novelAgents
    
    def getDNAExploreChild(self):
        exploreGenes = []
        for agent in self.memoryAgents:
            currExplore = agent.DNATested.getGene(EXPLOREGENE)
            exploreGenes.append(currExplore)
        
        totalFound = 0
        for gene in exploreGenes:
            totalFound += gene.score
        popAverage = totalFound / len(exploreGenes)
        
        # Formula check should switch
        if self.DNATested.getGene(EXPLOREGENE).score <= (popAverage * POPLUATIONTOLERANCE) and len(exploreGenes) > 1:
            self.runExploreTesting = True
            novelParents = self.noveltyFoundSelect(exploreGenes)
            newGene = []
            if len(novelParents) > 0:
                selfGene = self.DNATested.getGene(EXPLOREGENE)
                geneSegment = self.DNATested.crossoverProduction(novelParents, selfGene, EXPLOREGENE)
                newGene.append(geneSegment)
                exploreChild = Gene(newGene)
                # exploreChild = Gene(newGene).mutate()
            else:
                exploreChild = Gene(self.DNATested.mutation(self.DNATested.getGene(EXPLOREGENE)))
        else:
            exploreChild = None
        
        # if self.runExploreTurn:
        #     self.runExploreTurn = False
        # else:
        #     self.runExploreTurn = True
            
        return exploreChild
            
    def actUpdateExplore(self):
        if self.runExploreTesting is True:
            self.DNATesting.getGene(EXPLOREGENE).score = self.foodFound
            
        if self.DNATested.getGene(EXPLOREGENE).score <= self.DNATesting.getGene(EXPLOREGENE).score:
            self.DNATested.addGene(EXPLOREGENE, self.DNATesting.getGene(EXPLOREGENE))
        
        self.runExploreTesting = False
        # self.memoryAgents.append(self)
        newDNA = self.getDNAExploreChild()
        if self.runExploreTesting is True: 
            print(f"{self.id} testing explore")
            self.DNATesting.addGene(EXPLOREGENE, newDNA)
            self.generate_ExploreTreeTesting()
    
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