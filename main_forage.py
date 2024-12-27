from Agent import AgentMind
from Environment import Environment, Den, AgentBody
from Gene import DNAManager
from const import ENVIORN_DIM, NUMAGENTS
import random
# import sys
import threading
import plotly.express as px
import pandas as pd

# notes:
# movement, known locations removeal, novel parents, bad transfer, downwards agents, solo agents dieing, 11 novel parents
# Color Test:
# Stuck on consume and pick/drop
# Den goes around the whole map
# known gets stuck 
# knowns go to dead spot reapeatily 
# deposit when no known food exist
# discet block recursion bad aka deleteing sixe

# FIX:
# why is 10 apprearing in the gene size


if __name__ == '__main__':
    df = pd.DataFrame({
        'Food_Collected': [],
        'Agent_Quantity': []
    })
    
    NUMAGENTS = 5

    while NUMAGENTS <= 50 :    
        sampleSize = 30
        testIndex = 0
        # popluationScores = []
        # averageAgentScores = []

        while testIndex < sampleSize:
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
                
            # averageAgent = 0
            # for agent in agents:
            #     averageAgent += agent.agentBody.lifetimeFood

            # averageAgent = averageAgent // len(agents)
            # averageAgentScores.append(averageAgent)
            testIndex += 1
            new_row = {
                'Food_Collected': base.lifetimeFood,
                'Agent_Quantity': NUMAGENTS
            }
            df.loc[len(df)] = new_row
        NUMAGENTS += 5
        
    fig = px.box(df, y="Food_Collected", x="Agent_Quantity")
    print("all done")
    # fig.show()
    
#     for agent in agents:
#         allscore.append(f'agent {agent.id} score {agent.agentBody.lifetimeFood}')

#     print(f"{allscore} home lifetime food {base.lifetimeFood}")
    
#     for agent in agents:
#         print(f"{agent.crossover}")
#         print(f"{agent.mutate}")
#         print(f"{agent.StatePhenotypeTesting}")
#         print(f"{agent.BehaviorPhenotypeTesting}")
#         print(f"{agent.StatePhenotypeTested}")
#         print(f"{agent.BehaviorPhenotypeTested}")
#         agent.ExploreTreeTested.printTree()
#         agent.ExploreTreeTesting.printTree()
#         agent.StateMachineTesting.display()
#         agent.StateMachineTested.display()