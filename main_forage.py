from Agent import Agent
from Environment import Environment, FoodContainer, Den
from const import TOTALFOOD, ENVIORN_DIM
import random
from GGraph import GGraph
from const import STATE_RULES, EXPLORE_RULES

world = Environment()
for food in range(TOTALFOOD):
    spot = (random.randint(0,ENVIORN_DIM), random.randint(0,ENVIORN_DIM))
    foodContainer = FoodContainer(location=spot)
    world.inputObjectXY(spot, foodContainer)

agentDen = Den((random.randint(0,ENVIORN_DIM), random.randint(0,ENVIORN_DIM)))
world.inputObjectXY(agentDen.locationXY, agentDen)

stateGraph = GGraph(STATE_RULES)
exploreGraph = GGraph(EXPLORE_RULES)
agent = Agent(stateGraph, exploreGraph, agentDen, world)
# world.printSpace()
foodBefore = world.numFood
agent.runAgent()
# agent.SM.printSM()
# agent.SM.display()
world.printSpace()
print("PRINT Tree")
agent.ExploreTree.printTree()
agent.printStateHistory()
print(f'Food in World: before:{foodBefore} then:{world.numFood} Agent: {agent.numFood}')
print(f'hunger: {agent.hunger}')
print(f'score: {agent.score}')
# world.printSpace()