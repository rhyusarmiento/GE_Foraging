GENE_LEN = 500
TOTALFOOD = 10

ENVIORN_DIM = 10
DEN_SIZE = 5

RULES = {
    "<start>": ["<start>", "<SM>"],
    "<SM>": ["<stateID>, <SM>", "(<inputtype>),<SM>"],
    "<stateID>": ["Pick", "Drop", "Consume", "Explore", "Den", "Known"],
    "<inputtype>": ["isFood", "isTired", "isHungry", "isBored", "isDone"]
}