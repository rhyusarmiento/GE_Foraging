# Real Time Grammatical Evolution FSM Agent Swarm

Swarm Algorithms is a field of study that mimics the intelligent behavior of natural swarms found in nature. Similar to their counterparts in nature, the collective intelligence emerges from the interactions and behaviors of individual, non-intelligent components.

Rather than explicitly coding or programming the behavior of each non-intelligent component, the behavior is derived using a grammatical evolution algorithm. This approach enables the swarm to optimize its actions relative to its available commands and environment. For the remainder of the summary, the individual components of the swarm will be referred to as agents.

The project is simulated through Pygame and uses python's mulithreading. Each agent's game loop is run on an individual thread until end condtions are met. The end condition is determined by the number of actions. 

- **Dependencies**
    - Numpy
    - Pygame
    - Plotly

This summary will go over the anatomy of the agent and the grammatical evolution proccess. 

## Agent

Each agent is composed of a finite state machine (FSM), where each state represents either an explicitly defined action or a behavior determined by a behavior tree. The behavior tree itself is generated through grammatical evolution. 

### FSM

The agent builds a FSM based on a given `phenotype` string which was generated by the grammatical evolution. The `phenotype` is composed of different states. It assigns transitions between states based on available inputs.

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

1. **Input Parsing**:
   - The `phenotype` string is processed into a list of commands (`commandList`) by splitting it on commas and whitespace.

2. **State Initialization**:
   - The first state is initialized using `self.initGetState` with the first command in the list.
   - This state is stored as `currState` and added to the `fillQueue` for processing.

3. **State Creation**:
   - For each subsequent command in `commandList`:
     - A new state is created based on the command type (`Pick`, `Drop`, `Consume`, etc.).
     - The state is added to the corresponding state list (`self.PickStates`, `self.DropStates`, etc.).
     - A transition is defined between the current state and the new state for the first available input.
     - The new state becomes the current state.

4. **Transition Back to Start**:
   - A transition from the final state back to the first state is created to complete the loop.

5. **Adding Transitions for Remaining Inputs**:
   - For each state in the `fillQueue`:
     - Additional transitions are defined for all remaining inputs.
     - The target state for a transition is determined based on the next command in `commandList`.
     - States of the same type are cycled through, ensuring no self-loops for the current state.


![Completed FSM](./AgentFSMVisual.png)

### Explore Tree

For the explore state, the agent builds a behavior tree from a `phenotype` string. The tree is composed of nodes that represent specific commands, and these nodes are connected hierarchically based on the `phenotype`. 

- **Tree Node Types**:
  - `left`
  - `forward`
  - `right`
  - `isBored`
  - `func2`
  - `ifFood`
  - `isFood`

## Grammatical Evolution

