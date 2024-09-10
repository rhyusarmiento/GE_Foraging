from Agent import AgentMind
from Environment import Environment, FoodContainer, Den
from const import TOTALFOOD, ENVIORN_DIM
import random

world = Environment()
for food in range(TOTALFOOD):
    spot = (random.randint(0,ENVIORN_DIM), random.randint(0,ENVIORN_DIM))
    foodContainer = FoodContainer(location=spot)
    world.inputObjectXY(spot, foodContainer)

agentDen = Den((random.randint(0,ENVIORN_DIM), random.randint(0,ENVIORN_DIM)))
world.inputObjectXY(agentDen.locationXY, agentDen)

# agent = Agent(stateGraph, exploreGraph, agentDen, world)
# world.printSpace()
foodBefore = world.numFood
# agent.runAgent()
# # agent.SM.printSM()
# # agent.SM.display()
# world.printSpace()
# print("PRINT Tree")
# agent.ExploreTree.printTree()
# agent.printStateHistory()
# print(f'Food in World: before:{foodBefore} then:{world.numFood} Agent: {agent.numFood}')
# print(f'hunger: {agent.hunger}')
# print(f'score: {agent.score}')
# world.printSpace()