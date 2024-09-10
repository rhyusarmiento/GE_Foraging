import random
from BehaviorTree import BehaviorTree
import const as const
# import numpy as np
from StateMachine import StateMachine
from const import BEHAVIORGENE, STATEGENE
# import numpy as np
# import pygame as py

class AgentMind:
    def __init__(self, DNAManager, agentBody, id=None):
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
        # oritation
        self.agentBody = agentBody
        # simulation
        self.terminal_functions_run = 0
        self.score = 0
        self.running = False
        self.evoTest = False
        # Agent Stat
        self.foodLocations = []
        self.stateHistory = []
        # evolution
        self.memoryAgents = []
    
    def printID(self):
        print(f"{self.id}")
    
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
            self.StateMachine.createStateMachine(self.StatePhenotype, self.DNA.getGene(STATEGENE), inputsAvailable)
        
    def generate_ExploreTree(self):
        self.BehaviorPhenotype = self.DNA.getGenePhenotype(BEHAVIORGENE)
        if self.BehaviorPhenotype is None:
            self.running = False
            print("no Behavior phenotype provided")
        else:
            self.ExploreTree = BehaviorTree(self.BehaviorPhenotype)
    
    def runAgent(self):
        try:
            self.running = True
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
    
    # def setup(self):
    #     self.StatePhenotype = self.gene.generate_phenotype(self.rules, "<start>")
    #     self.generate_StateMachine()
    
    def printStateHistory(self):
        for state in self.stateHistory:
            print(state)
        
    def should_end(self):
        self.terminal_functions_run += 1
        if self.terminal_functions_run == 1000:
            return True
        return False
    
    def end(self):
        raise EndException("End of simulation")
    
    def sense(self):
        self.memoryAgents.clear()
        self.memoryAgents.extend(self.agentBody.getAgentsNear)     
    
    def novelty_select(self, agents):
        pass
        # totalFood = 0
        # totalConsecu = 0
        # totalOffPath = 0
        # totalDistance = 0
        # for agent in agents:
        #     totalFood += agent.food_touched
        #     totalConsecu += agent.consecutiveFood
        #     totalOffPath += agent.offPath
        #     totalDistance += agent.distance
        # totalFood = np.round((totalFood / len(agents)), 2)
        # totalConsecu = np.round((totalConsecu / len(agents)), 2)
        # totalOffPath = np.round((totalOffPath / len(agents)), 2)
        # totalDistance = np.round((totalDistance / len(agents)), 2)
        # novelAgents = []
        # for agent in agents:
        #     if (np.abs(totalFood - agent.food_touched) > totalFood * const.NOVELTY_TOLERANCE_FOOD):
        #         novelAgents.append(agent)
        # return novelAgents
    
    def novelty_select_OffPath(self, agents):
        pass
        # totalOffPath = 0
        # for agent in agents:
        #     totalOffPath += agent.offPath
        # novelAgents = []
        # if len(agents) > 0:
        #     totalOffPath = np.round((totalOffPath / len(agents)), 2)
        #     for agent in agents:
        #         if (np.abs(totalOffPath - agent.offPath) > totalOffPath * const.NOVELTY_TOLERANCE_OFFPATH):
        #             novelAgents.append(agent)
        # return novelAgents
            # (np.abs(totalDistance - agent.distance) > totalDistance * const.NOVELTY_TOLERANCE)
            # (np.abs(totalOffPath - agent.offPath) > totalOffPath * const.NOVELTY_TOLERANCE) and
            # (np.abs(totalFood - agent.food_touched) > totalFood * const.NOVELTY_TOLERANCE)
            # (np.abs(totalConsecu - agent.consecutiveFood) > totalConsecu * const.NOVELTY_TOLERANCE)
            
    def getStateChildren(self):
        holdGeno = []
        for agent in self.memoryAgents:
            holdGeno.append(agent.stateGene.genotype)
        return self.stateGene.crossoverProduction(holdGeno)
    
    def getBehaviorChildren(self):
        holdGeno = []
        for agent in self.memoryAgents:
            holdGeno.append(agent.behaviorGene.genotype)
        return self.behaviorGene.crossoverProduction(holdGeno)
        
    def actUpdate(self):
        self.projectionresult = 0
        self.mutateresult = 0
        self.memoryAgents.append(self)
        childrenState = self.getStateChildren()
        childrenBehavior = self.getBehaviorChildren()
        agents = []
        incre = 0
        while(incre < len(childrenBehavior)):
            # stateRules, behaviorRules, home, worldMap, id='', stateGene=None, behaviorGene=None
            a = AgentMind(self.stateRules, self.behaviorRules, self.home, self.worldMap, id='testrun', stateGene=childrenState[incre], behaviorGene=childrenBehavior[incre])
            agents.append(a)
            a.runTest()
            incre += 1
        novelFoodAgents = self.novelty_select(agents)
        novelOffPathAgents = self.novelty_select_OffPath(novelFoodAgents)
        pickme = []
        for agent in novelOffPathAgents:
            pickme.append(agent)
        if len(pickme) > 0:
            num = random.randint(0, len(pickme) - 1)
            self.stateGene = pickme[num].stateGene
            self.projectionresult += 1 
        else:
            a = AgentMind(self.grid, self.rules, id='testrun', gene=self.stateGene.mutate())
            a.runAgent()
            self.stateGene = a.stateGene
            self.mutateresult += 1

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