from Agent import AgentMind
from Environment import Environment, FoodContainer, Den, AgentBody
from Gene import DNAManager
from const import TOTALFOOD, ENVIORN_DIM
import random

world = Environment()
base = Den(world, (random.randint(0,ENVIORN_DIM), random.randint(0,ENVIORN_DIM)))
world.testSetUp()
world.addNewObject(base)

agents = []
for x in range(100):
    agent = AgentMind(DNAManager(), x)
    agentObject = AgentBody(world, base.center, agent, base)
    agent.addBody(agentObject)
    world.addNewObject(agentObject)
    agents.append(agent)

for agent in agents:
    agent.runAgent()
    print(f"score {agent.score}")

print("jajaj done")
# world.printSpace()
# # agent.StateMachine.printSM()
# # agent.StateMachine.display()
# world.printSpace()
# print("PRINT Tree")
# agent.ExploreTree.printTree()
# agent.printStateHistory()
# print(f'Food in World: before:{foodBefore} then:{world.numFood} Agent:{agent.numFood}')
# print(f'hunger: {agent.hunger}')
# print(f'score: {agent.score}')
# world.printSpace()