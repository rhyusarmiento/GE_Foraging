# issue with ending known food node
# Issue with not pickup food
# protential issue with evo

# World
TOTALFOOD = 300
ENVIORN_DIM = 500
DENSIZE = 20
WORLDFILL = (255, 255, 255)
DENBORDERSIZE = 3
FOODPERCENT = 130
FOODCOLOR = (0, 255, 0)
FOODSIZE = 6
DENCOLOR = (0, 255, 255)
NUMAGENTS = 30

# Agent body Simulation
HUNGER = 100
NEIGHBOOR_LIMIT = 10
AGENTSIZE = 15
AGENTVISIONINCREASE = 7
AGENTCOLOR = (255, 0, 0) # red
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
ORAGNE = (255, 165, 0)
YELLOW = (255, 255, 0)
PURPLE = (165, 32, 240)
MOVEMENTSPEED = 1

# Agent mind simulation
EVO_TIMER = 70
EVO_LIMIT = 50
ENVIORNTEST = 50
TESTFOOD = 20
TERMINALLIMIT = 5000

# Agent Evolution
EVO_SEC = 200
GENE_LEN = 300
GENE_FIRSTCUT = .2
GENE_SECONDCUT = .6
GENE_THIRDCUT = .8
CROSSOVER_PRODUCTION = 5
MUTATION_RATE = .9
MUTATION_FIRSTDECUT = .1
MUTATION_SECONDDECUT = .15
MUTATION_THIRDDECUT = .2
LARGE_MUTATION_RATE = .7
LARGE_MUTATION_FIRSTDECUT = .2
LARGE_MUTATION_SECONDDECUT = .2
LARGE_MUTATION_THIRDDECUT = .2
NOVELTYSTANDARD = 1.1
POPLUATIONTOLERANCE = .2

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