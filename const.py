# World
TOTALFOOD = 500
ENVIORN_DIM = 500
DENSIZE = 60
WORLDFILL = (255, 255, 255)
DENBORDERSIZE = 3
FOODPERCENT = 130
FOODCOLOR = (0, 255, 0)
FOODSIZE = 6
DENCOLOR = (0, 255, 255)
NUMAGENTS = 100

# Agent body Simulation
HUNGER = 1000
NEIGHBOOR_LIMIT = 10
AGENTSIZE = 15
AGENTVISIONINCREASE = 4
AGENTCOLOR = (255, 0, 0)
MOVEMENTSPEED = 1

# Agent mind simulation
EVO_TIMER = 70
EVO_LIMIT = 50
ENVIORNTEST = 50
TESTFOOD = 20
TERMINALLIMIT = 1000

# Agent Evolution
EVO_SEC = 30
GENE_LEN = 200
GENE_FIRSTCUT = .2
GENE_SECONDCUT = .6
GENE_THIRDCUT = .8
CROSSOVER_PRODUCTION = 5
MUTATION_RATE = .8
MUTATION_FIRSTDECUT = .1
MUTATION_SECONDDECUT = .15
MUTATION_THIRDDECUT = .2
NOVELTYSTANDARD = .5

# grammer
EXPLORE_RULES = {
    "<start>": ["<start>", "<progs>"],
    "<progs>": ["<run2>"],
    "<node>": ["<move>", "<progs>", "<condition>"],
    "<move>": ["left", "forward", "right", "isBored"],
    "<run2>": ["func2(<node>,<node>,<node>)"],
    "<condition>": ["ifFood(isFood,<node>)", "ifFood(<node>,<node>)"]
}
STATE_RULES = {
    "<start>": ["<start>", "<SM>"],
    "<SM>": ["<stateID>,<SM>", "(<inputtype>),<SM>"],
    "<stateID>": ["Pick", "Drop", "Consume", "Explore", "Den", "Known"],
    "<inputtype>": ["isFood", "isTired", "isHungry", "isBored", "isDone"]
}

# Data Constants
DEAD = "Dead"
ISHUNGRY = "isHungry"
ISTIRED = "isTired"
ISDONE = "isDone"
ISBORED = "isBored"
IFFOOD = "ifFood"
ISFOOD = "isFood"
FUNC2 = "func2"
EAST = "East"
SOUTH = "South"
WEST = "West"
DEN = "Den"
FOOD = "Food"
AGENT = "Agent"
NORTH = "North"
STATEGENE = "stateGene"
EXPLOREGENE = "exploreGene"