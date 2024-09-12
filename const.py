TOTALFOOD = 400
HUNGER = 300

GENE_LEN = 200
CROSSOVER_PRODUCTION = 2
STATEGENE = "stateGene"
BEHAVIORGENE = "behaviorGene"

ENVIORN_DIM = 100
DEN_SIZE = 5
NEIGHBOOR_LIMIT = 5

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