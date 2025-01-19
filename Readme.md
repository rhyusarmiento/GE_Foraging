## NOTES

This is a live repo

### Current work
- O-time problem on some runs
- ideas fixes for occasional dead populations

## Results paper

https://docs.google.com/document/d/1_15dOPsC7pc95uiwGSaxSmBIca3GRO-0FgT2vfFadLg/edit?usp=sharing

# Real Time Grammatical Evolution FSM Agent Swarm

Swarm Algorithms is a field of study that emulates the intelligent behaviors observed in natural swarms. Like their real-world counterparts, collective intelligence in these systems arises from the interactions and behaviors of individual, non-intelligent components.

Instead of explicitly coding or programming the behavior of each individual component, their actions are derived using a grammatical evolution algorithm. This method allows the swarm to dynamically optimize its behaviors based on available commands and environmental factors. For clarity, the individual components within the swarm will be referred to as agents throughout this summary.

The project is implemented using Pygame and leverages Python's multithreading capabilities. Each agent's game loop operates on a separate thread until specific end conditions are met. The primary end condition is determined by the number of actions performed by the agent.

- **Dependencies**
    - Numpy
    - Pygame
    - Plotly

This summary will go over the anatomy of the agent and the grammatical evolution proccess. 

## Agent

Each agent is structured as a Finite State Machine (FSM), where each state represents either an explicitly defined action or a behavior derived from a behavior tree. The behavior tree itself is dynamically generated through grammatical evolution.

Note: Each agent stores two FSM and Behavior trees. One is the tested FSM and Tree. The other is the testing FSM and Behavior Tree. 

### FSM

The agent constructs a Finite State Machine (FSM) based on a given phenotype string, which is generated through grammatical evolution. The phenotype comprises various states and defines the transitions between these states based on the available inputs.

- **Commands and Corresponding States**:
  - `"Pick"` → `Pick`
  - `"Drop"` → `Drop`
  - `"Consume"` → `Consume`
  - `"Explore"` → `Explore`
  - `"Den"` → `Den`
  - `"Known"` → `Known`

- **Transition Types**:
  - `"isDone"`
  - `"isFood"`
  - `"isTired"`
  - `"isBored"`
  - `"isHungry"`

The phenotype specifies an ordered sequence of commands, with each command corresponding to a state in the Finite State Machine (FSM). For every command, a new state is created and added to a fillqueue. The transition type isDone is assigned between each state and the subsequent state in the sequence. The final state in the phenotype loops back to the first state by setting its isDone transition, creating a continuous cycle.

Subsequently, the fillqueue is iterated through to establish connections between the created states and any remaining transition types. Each state connects to an existing state determined by the command list and the iteration process. The chosen state is the most recently created state of the corresponding type. To ensure uniqueness, no two transition types for a given state lead to the same destination state; this is enforced by decrementing through the list of available states for that type.

![Completed FSM](./AgentFSMVisual.png)

### Explore Tree

In the Explore state, the agent constructs a behavior tree from a given phenotype string. The tree consists of nodes, each representing a specific command, which are hierarchically connected according to the structure defined by the phenotype.

- **Tree Node Types**:
  - `left`
  - `forward`
  - `right`
  - `isBored`
  - `func2`
  - `ifFood`
  - `isFood`

## Grammatical Evolution

This project's grammatical evolution (GE) is modeled after the GEESE.
https://faculty.cs.byu.edu/~mike/mikeg/papers/NeupaneGoodrichMercer-GECCO2018.pdf

### Phenotype Production

A phenotype is the output of the Grammatical Evolution (GE) process. In standard GE implementations, each agent possesses a genotype, which is represented as a list of numerical values. Each number corresponds to either a terminal or non-terminal in the defined grammar. The genotype is then parsed into a sequence of terminals using this grammar, resulting in the phenotype.

This project distinguishes itself by employing a weighted graph to fully express each genotype. The weighted graph encapsulates the grammar's structure and is designed to return the nearest terminal for any given input. This innovative approach ensures that every genotype is comprehensively expressed, providing a robust mechanism for translating genetic information into actionable behaviors or commands.

### Conditions for Evolution 

The agent runs the evolution command once two conditions are met. First, the rate of food gathered at the Den is not positive. Second, if the agents tested gene score is lower than a percentage of the averge score of the local population. 

Additionally, there is a special condition to ensure productivity: if an agent has collected no food during the previous interval and is located at the den, the evolution process is triggered.

### Process of Evolution

Before the evolution process begins, the tested gene is assigned a score based on the food deposited and the total amount of food gathered during the time interval. If the testing gene achieves a higher score, it replaces the current tested gene. Once the conditions for evolution are met, the agent generates a new gene through crossover with nearby agents. This new gene is stored in the testing genes and will be evaluated in the next interval.

### Crossover

Parents are selected from nearby agents based on a novelty threshold derived from their tested gene scores. Novelty is determined by comparing an agent’s score to the average score of the surrounding agents. Once novel parents are identified, crossover is performed by randomly selecting one of the parents. A sequence of numbers is transferred from the parent genotype until a terminal number is reached. This process continues until a new genotype is formed based on the parental information.

If no novel parents are available, the agent’s genotype undergoes mutation, where integers within the genotype are randomly altered to create variation in the evolving agent's genetic code.
