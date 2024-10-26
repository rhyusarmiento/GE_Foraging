from Agent import AgentMind
from Environment import Environment, Den, AgentBody
from Gene import DNAManager
from const import ENVIORN_DIM, NUMAGENTS
import random
# import sys
import threading

# notes:
# movement, known locations removeal, novel parents, bad transfer, downwards agents, solo agents dieing, 11 novel parents
# Color Test:
# Stuck on consume and pick/drop
# Den goes around the whole map
# known gets stuck 
# knowns go to dead spot reapeatily 
# deposit when no known food exist

if __name__ == '__main__':
    world = Environment()
    base = Den(world, (random.randint(60,ENVIORN_DIM - 60), random.randint(60,ENVIORN_DIM - 60)))
    world.testReset()
    world.addNewObject(base)

    agents = []
    for x in range(NUMAGENTS):
        agent = AgentMind(DNAManager(), x)
        agentObject = AgentBody(world, base.center, agent, base)
        agent.addBody(agentObject)
        world.addNewObject(agentObject)
        agents.append(agent)

    print("done")
    allscore = []
    threads = []
    
    world.rendering = True
    for agent in agents:
        thread = threading.Thread(target=agent.runAgent)
        threads.append(thread)
        thread.start()
    threadevo = threading.Thread(target=base.evoTimer)
    threads.append(threadevo)
    threadevo.start()
    world.startPyGame()
    
    for thread in threads:
        thread.join()
        
    for agent in agents:
        allscore.append(f'agent {agent.id} score {agent.agentBody.lifetimeFood}')

    print(f"{allscore} home lifetime food {base.lifetimeFood}")
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