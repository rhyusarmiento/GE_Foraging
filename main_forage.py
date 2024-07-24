from Agent import Agent
from Environment import Environment, FoodContainer, Den
from const import TOTALFOOD, ENVIORN_DIM
import random
from GGraph import GGraph
from const import RULES

world = Environment()
world.buildEnvironment()
for food in range(TOTALFOOD):
    foodContainer = FoodContainer()
    world.inputObjectXY((random.randint(0,ENVIORN_DIM), random.randint(0,ENVIORN_DIM)),foodContainer)

agentDen = Den((random.randint(0,ENVIORN_DIM), random.randint(0,ENVIORN_DIM)))
world.inputObjectXY(agentDen.locationXY, agentDen)

ggraph = GGraph(RULES)
agent = Agent(ggraph, agentDen, world)
agent.runAgent()
world.printSpace()
# agent.setup()
# agent.SM.display()