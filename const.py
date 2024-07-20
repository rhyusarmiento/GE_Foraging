GENE_LEN = 1000

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
    "<inputtype>": ["isFood", "isTired", "isHungry", "isBored", "isProductive", "isDone"]
}