class StateMachine:
    def __init__(self):
        self.StartInput = None
        self.PickStates = []
        self.DropStates = []
        self.ConsumeStates = []
        self.ExploreStates = []
        self.DenStates = []
        self.KnownStates = []
        self.CurrentState = None
        self.currentCodon = 0
    
    def createSM(self, phenotype, genotype):
        commandList = phenotype.replace(",", " ").split()
        isFirst = True
        for command in commandList:
            if command == "Pick":
                node = Pick()
                self.PickStates.append(node)
                if isFirst is True:
                    self.StartInput["start"] = node
                    isFirst = False
            elif command == "Drop":
                node = Drop()
                self.DropStates.append(node)
                if isFirst is True:
                    self.StartInput["start"] = node
                    isFirst = False
            elif command == "Consume":
                node = Consume()
                self.DropStates.append(node)
                if isFirst is True:
                    self.StartInput["start"] = node
                    isFirst = False
            elif command == "Explore":
                node = Explore()
                self.DropStates.append(node)
                if isFirst is True:
                    self.StartInput["start"] = node
                    isFirst = False
            elif command == "Den":
                node = Den()
                self.DropStates.append(node)  
                if isFirst is True:
                    self.StartInput["start"] = node
                    isFirst = False  
            elif command == "Known":
                node = Known()
                self.DropStates.append(node)
                if isFirst is True:
                    self.StartInput["start"] = node
                    isFirst = False
            elif "(" in command and ")" in command:
                inputCommand = command[1:-1].replace("-"," ").split()
                firstCommand = inputCommand[0]
                inputType = inputCommand[1]
                lastCommand = inputCommand[2]
                if firstCommand == "Pick":
                    if self.currentCodon > len(genotype):
                        self.currentCodon = 0
                    if len(self.PickStates) != 0:
                        firstNode = self.PickStates[genotype[self.currentCodon] % len(self.PickStates)]
                        self.currentCodon += 1
                    else:
                        firstNode = None
                elif firstCommand == "Drop":
                    if self.currentCodon > len(genotype):
                        self.currentCodon = 0
                    if len(self.DropStates) != 0:
                        firstNode = self.DropStates[genotype[self.currentCodon] % len(self.DropStates)]
                        self.currentCodon += 1
                    else:
                        firstNode = None
                elif firstCommand == "Consume":
                    if self.currentCodon > len(genotype):
                        self.currentCodon = 0
                    if len(self.ConsumeStates) != 0:
                        firstNode = self.ConsumeStates[genotype[self.currentCodon] % len(self.ConsumeStates)]
                        self.currentCodon += 1
                    else:
                        firstNode = None
                elif firstCommand == "Explore":
                    if self.currentCodon > len(genotype):
                        self.currentCodon = 0
                    if len(self.ExploreStates) != 0:
                        firstNode = self.ExploreStates[genotype[self.currentCodon] % len(self.ExploreStates)]
                        self.currentCodon += 1
                    else:
                        firstNode = None
                elif firstCommand == "Den":
                    if self.currentCodon > len(genotype):
                        self.currentCodon = 0
                    if len(self.DenStates) != 0:
                        firstNode = self.DenStates[genotype[self.currentCodon] % len(self.DenStates)]
                        self.currentCodon += 1
                    else:
                        firstNode = None  
                elif firstCommand == "Known":
                    if self.currentCodon > len(genotype):
                        self.currentCodon = 0
                    if len(self.KnownStates) != 0:
                        firstNode = self.KnownStates[genotype[self.currentCodon] % len(self.KnownStates)]
                        self.currentCodon += 1
                    else:
                        firstNode = None
                if lastCommand == "Pick":
                    if self.currentCodon > len(genotype):
                        self.currentCodon = 0
                    if len(self.PickStates) != 0:
                        firstNode = self.PickStates[genotype[self.currentCodon] % len(self.PickStates)]
                        self.currentCodon += 1
                    else:
                        lastNode = None
                elif lastCommand == "Drop":
                    if self.currentCodon > len(genotype):
                        self.currentCodon = 0
                    if len(self.DropStates) != 0:
                        lastNode = self.DropStates[genotype[self.currentCodon] % len(self.DropStates)]
                        self.currentCodon += 1
                    else:
                        lastNode = None
                elif lastCommand == "Consume":
                    if self.currentCodon > len(genotype):
                        self.currentCodon = 0
                    if len(self.ConsumeStates) != 0:
                        lastNode = self.ConsumeStates[genotype[self.currentCodon] % len(self.ConsumeStates)]
                        self.currentCodon += 1
                    else:
                        lastNode = None
                elif lastCommand == "Explore":
                    if self.currentCodon > len(genotype):
                        self.currentCodon = 0
                    if len(self.ExploreStates) != 0:
                        lastNode = self.ExploreStates[genotype[self.currentCodon] % len(self.ExploreStates)]
                        self.currentCodon += 1
                    else:
                        lastNode = None
                elif lastCommand == "Den":
                    if self.currentCodon > len(genotype):
                        self.currentCodon = 0
                    if len(self.DenStates) != 0:
                        lastNode = self.DenStates[genotype[self.currentCodon] % len(self.DenStates)]
                        self.currentCodon += 1
                    else:
                        lastNode = None
                elif lastCommand == "Known":
                    if self.currentCodon > len(genotype):
                        self.currentCodon = 0
                    if len(self.KnownStates) != 0:
                        lastNode = self.KnownStates[genotype[self.currentCodon] % len(self.KnownStates)]
                        self.currentCodon += 1
                    else:
                        lastNode = None
                if firstNode is not None and lastNode is not None:
                    firstNode.inputState(inputType, lastNode)
                
    def changeState(self, input):
        self.CurrentState = self.CurrentState.changeState(input)
        return self.CurrentState
        # inputs the input into the current state
    
    def getStartState(self):
        return self.StartInput["start"]
    
class State:
    def __init__(self):
        self.Outros = {}
    
    def changeState(self, input):
        # check state?
        return self.Outros[input]
    
    def inputState(self, input, state):
        if input not in self.Outros:
            self.Outros[input] = state
        
class Pick(State):
    def behavior(self):
        return "Pick"

class Drop(State):
    def behavior(self):
        return "Drop"
    
class Consume(State):
    def behavior(self):
        return "Consume"
    
class Explore(State):
    def behavior(self):
        return "Explore"
    
class Den(State):
    def behavior(self):
        return "Den"
    
class Known(State):
    def behavior(self):
        return "Known"