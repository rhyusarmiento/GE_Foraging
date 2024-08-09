GENE_LEN = 150
TOTALFOOD = 400

ENVIORN_DIM = 500
DEN_SIZE = 5

EXPLORE_RULES = {
    "<start>": ["<start>", "<prog>"],
    "<prog>": ["<move>", "<prog2>", "isBored", "<condition>"],
    "<move>": ["left", "forward", "right"],
    "<prog2>": ["progs(<prog>,<prog>)"],
    "<condition>": ["ifFood(isFood,<prog>)", "ifFood(<prog>,<prog>)"]
}

STATE_RULES = {
    "<start>": ["<start>", "<SM>"],
    "<SM>": ["<stateID>,<SM>", "(<inputtype>),<SM>"],
    "<stateID>": ["Pick", "Drop", "Consume", "Explore", "Den", "Known"],
    "<inputtype>": ["isFood", "isTired", "isHungry", "isBored", "isDone"]
}