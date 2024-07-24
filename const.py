GENE_LEN = 1000
TOTALFOOD = 10

ENVIORN_DIM = 10
DEN_SIZE = 5

RULES = {
    "<start>": ["<start>", "<SM>"],
    "<SM>": ["<node>", "<input>"],
    "<node>": ["<Pick>", "<Drop>", "<Consume>", "<Explore>", "<Den>", "<Known>"],
    "<Pick>": ["Pick,<SM>"],
    "<Drop>": ["Drop,<SM>"],
    "<Consume>": ["Consume,<SM>"],
    "<Explore>": ["Explore,<SM>"],
    "<Den>": ["Den,<SM>"],
    "<Known>": ["Known,<SM>"],
    "<input>": ["(<nodeID>-<inputtype>-<nodeID>),<SM>"],
    "<nodeID>": ["Pick", "Drop", "Consume", "Explore", "Den", "Known"],
    "<inputtype>": ["isFood", "isTired", "isHungry", "isBored", "isDone"]
}