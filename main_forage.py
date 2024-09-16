from Agent import AgentMind
from Environment import Environment, Den, AgentBody
from Gene import DNAManager
from const import ENVIORN_DIM
import random
# import sys
import threading

if __name__ == '__main__':
    world = Environment()
    base = Den(world, (random.randint(0,ENVIORN_DIM), random.randint(0,ENVIORN_DIM)))
    world.testReset()
    world.addNewObject(base)

    agents = []
    for x in range(20):
        agent = AgentMind(DNAManager(), x)
        agentObject = AgentBody(world, base.center, agent, base)
        agent.addBody(agentObject)
        world.addNewObject(agentObject)
        agents.append(agent)

    allscore = []
    threads = []
    for agent in agents:
        thread = threading.Thread(target=agent.runAgent)
        threads.append(thread)
        thread.start()
        
    for thread in threads:
        thread.join()
        
    for agent in agents:
        allscore.append(f'agent {agent.id} score {agent.score}')

    print(allscore)
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