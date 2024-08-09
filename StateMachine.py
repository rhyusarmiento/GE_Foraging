import random
import plotly.graph_objects as go
import plotly.io as pio

class StateMachine:
    def __init__(self):
        self.StartInput = {}
        self.PickStates = []
        self.DropStates = []
        self.ConsumeStates = []
        self.ExploreStates = []
        self.DenStates = []
        self.KnownStates = []
        self.CurrentState = None
        self.currentCodon = 0
    
    def initGetState(self, command, inputs):
        if command == "Pick":
            node = Pick(1, inputs)
            self.PickStates.append(node)
            self.StartInput["start"] = node
            return node
        elif command == "Drop":
            node = Drop(1, inputs)
            self.DropStates.append(node)
            self.StartInput["start"] = node
            return node
        elif command == "Consume":
            node = Consume(1, inputs)
            self.ConsumeStates.append(node)
            self.StartInput["start"] = node
            return node
        elif command == "Explore":
            node = Explore(1, inputs)
            self.ExploreStates.append(node)
            self.StartInput["start"] = node
            return node
        elif command == "Den":
            node = Den(1, inputs)
            self.DenStates.append(node)  
            self.StartInput["start"] = node
            return node
        elif command == "Known":
            node = Known(1, inputs)
            self.KnownStates.append(node)
            self.StartInput["start"] = node
            return node
        else:
            return None
        
    # this fuction sometimes has long runtime because of a possible infinte loop
    def createSM(self, phenotype, genotype, availableInputs):
        # print(phenotype)
        # print(availableInputs)
        commandList = phenotype.replace(",", " ").split()
        # print(commandList)
        inCre = 1
        fillQueue = []
        stateStack = []
        while self.initGetState(commandList[0], availableInputs) is None:
            commandList.append(commandList.pop(0))
        currState = self.initGetState(commandList[0], availableInputs)
        holdState = commandList.pop(0)
        inputNum = 0
        # print(holdState)
        
        for command in commandList:
            if "(" in command and ")" in command:
                inputNum += 1
            if "(" in command and ")" in command and len(stateStack) != 0:
                inCre += 1
                inputType = command[1:-1]
                toState = stateStack.pop()
                if toState == "Pick":
                    if self.currentCodon >= len(genotype):
                        self.currentCodon = 0
                    if len(self.PickStates) > 0:
                        state = self.PickStates[genotype[self.currentCodon] % len(self.PickStates)]
                        self.currentCodon += 1
                        if state.isFull():
                            newState = Pick(inCre, availableInputs)
                            self.PickStates.append(newState)
                    else:
                        state = Pick(inCre, availableInputs)
                        self.PickStates.append(state)
                elif toState == "Drop":
                    if self.currentCodon >= len(genotype):
                        self.currentCodon = 0
                    if len(self.DropStates) > 0:
                        state = self.DropStates[genotype[self.currentCodon] % len(self.DropStates)]
                        self.currentCodon += 1
                        if state.isFull():
                            newState = Drop(inCre, availableInputs)
                            self.DropStates.append(newState)
                    else:
                        state = Drop(inCre, availableInputs)
                        self.DropStates.append(state)
                elif toState == "Consume":
                    if self.currentCodon >= len(genotype):
                        self.currentCodon = 0
                    if len(self.ConsumeStates) > 0:
                        state = self.ConsumeStates[genotype[self.currentCodon] % len(self.ConsumeStates)]
                        if state.isFull():
                            newState = Consume(inCre, availableInputs)
                            self.ConsumeStates.append(newState)
                        self.currentCodon += 1
                    else:
                        state = Consume(inCre, availableInputs)
                        self.ConsumeStates.append(state)
                elif toState == "Explore":
                    if self.currentCodon >= len(genotype):
                        self.currentCodon = 0
                    if len(self.ExploreStates) > 0:
                        state = self.ExploreStates[genotype[self.currentCodon] % len(self.ExploreStates)]
                        if state.isFull():
                            newState = Explore(inCre, availableInputs)
                            self.ExploreStates.append(newState)
                        self.currentCodon += 1
                    else:
                        state = Explore(inCre, availableInputs)
                        self.ExploreStates.append(state)
                elif toState == "Den":
                    if self.currentCodon >= len(genotype):
                        self.currentCodon = 0
                    if len(self.DenStates) > 0:
                        state = self.DenStates[genotype[self.currentCodon] % len(self.DenStates)]
                        if state.isFull():
                            newState = Den(inCre, availableInputs)
                            self.DenStates.append(newState)
                        self.currentCodon += 1
                    else:
                        state = Den(inCre, availableInputs)
                        self.DenStates.append(state)
                elif toState == "Known":
                    if self.currentCodon >= len(genotype):
                        self.currentCodon = 0
                    if len(self.KnownStates) > 0:
                        state = self.KnownStates[genotype[self.currentCodon] % len(self.KnownStates)]
                        if state.isFull():
                            newState = Known(inCre, availableInputs)
                            self.KnownStates.append(newState)
                        self.currentCodon += 1
                    else:
                        state = Known(inCre, availableInputs)
                        self.KnownStates.append(state)
                else:
                    print(f'Error: unhandled Condition toState:{toState} command:{command}') 
                currState.inputState(inputType, state)
                if not state.isFull():
                    fillQueue.append(state)
                if currState.isFull():
                    currState = fillQueue.pop(0)
            elif "(" not in command and ")" not in command:
                stateStack.append(command)
        # self.currentCodon = 0
        commandIncr = 0
        commandList.insert(0, holdState)
        # print(f"bro {inputNum}")
        bootleg = 0
        while len(fillQueue) > 0 or not currState.isFull():
            if (len(stateStack) > 0 or bootleg == 0) and (len(stateStack) > 0 and bootleg == 0):
                if commandIncr >= len(commandList) - 1:
                    commandIncr = 0
                else:
                    commandIncr += 1
                currCommand = commandList[commandIncr]
                if "(" in currCommand and ")" in currCommand and len(stateStack) != 0:
                    inCre += 1
                    inputType = currCommand[1:-1]
                    toState = stateStack.pop()
                    if toState == "Pick":
                        if self.currentCodon >= len(genotype):
                            self.currentCodon = 0
                        if len(self.PickStates) > 0:
                            state = self.PickStates[genotype[self.currentCodon] % len(self.PickStates)]
                            self.currentCodon += 1
                        else:
                            state = Pick(inCre, availableInputs)
                            self.PickStates.append(state)
                    elif toState == "Drop":
                        if self.currentCodon >= len(genotype):
                            self.currentCodon = 0
                        if len(self.DropStates) > 0:
                            state = self.DropStates[genotype[self.currentCodon] % len(self.DropStates)]
                            self.currentCodon += 1
                        else:
                            state = Drop(inCre, availableInputs)
                            self.DropStates.append(state)
                    elif toState == "Consume":
                        if self.currentCodon >= len(genotype):
                            self.currentCodon = 0
                        if len(self.ConsumeStates) > 0:
                            state = self.ConsumeStates[genotype[self.currentCodon] % len(self.ConsumeStates)]
                            self.currentCodon += 1
                        else:
                            state = Consume(inCre, availableInputs)
                            self.ConsumeStates.append(state)
                    elif toState == "Explore":
                        if self.currentCodon >= len(genotype):
                            self.currentCodon = 0
                        if len(self.ExploreStates) > 0:
                            state = self.ExploreStates[genotype[self.currentCodon] % len(self.ExploreStates)]
                            self.currentCodon += 1
                        else:
                            state = Explore(inCre, availableInputs)
                            self.ExploreStates.append(state)
                    elif toState == "Den":
                        if self.currentCodon >= len(genotype):
                            self.currentCodon = 0
                        if len(self.DenStates) > 0:
                            state = self.DenStates[genotype[self.currentCodon] % len(self.DenStates)]
                            self.currentCodon += 1
                        else:
                            state = Den(inCre, availableInputs)
                            self.DenStates.append(state)
                    elif toState == "Known":
                        if self.currentCodon >= len(genotype):
                            self.currentCodon = 0
                        if len(self.KnownStates) > 0:
                            state = self.KnownStates[genotype[self.currentCodon] % len(self.KnownStates)]
                            self.currentCodon += 1
                        else:
                            state = Known(inCre, availableInputs)
                            self.KnownStates.append(state)
                    else:
                        print(f'Error: unhandled Condition toState:{toState} command:{currCommand}') 
                    # print(f"currState: {currState.printName()}  input: {inputType} state: {state.printName()}")
                    # print(currState.isFull())
                    # print(len(stateStack))
                    currState.inputState(inputType, state)
                    if not state.isFull():
                        fillQueue.append(state)
                    if currState.isFull() and len(fillQueue) > 0:
                        currState = fillQueue.pop(0)
                elif "(" not in currCommand and ")" not in currCommand:
                    stateStack.append(currCommand)
            else:
                if len(stateStack) == 0:
                    bootleg = bootleg + inputNum
                if commandIncr >= len(commandList) - 1:
                    commandIncr = 0
                else:
                    commandIncr += 1
                currCommand = commandList[commandIncr]
                if "(" not in currCommand and ")" not in currCommand:
                    bootleg -= 1    
                    stateStack.append(currCommand)
                
    def printSM(self):
        num = 0
        for key in self.StartInput:
            print(f'{key}: {self.StartInput[key].printName()}')
        
        for state in self.PickStates:
            num += 1
            print(f'Pick{num}:')
            for key in state.Outros:
                print(f'{key}: {state.Outros[key].printName()}')
        num = 0
        for state in self.DropStates:
            num += 1
            print(f'Drop{num}:')
            for key in state.Outros:
                print(f'{key}: {state.Outros[key].printName()}')
        num = 0
        for state in self.ConsumeStates:
            num += 1
            print(f'Consume{num}:')
            for key in state.Outros:
                print(f'{key}: {state.Outros[key].printName()}')
        num = 0
        for state in self.ExploreStates:
            num += 1
            print(f'Explore{num}:')
            for key in state.Outros:
                print(f'{key}: {state.Outros[key].printName()}')
        num = 0
        for state in self.DenStates:
            num += 1
            print(f'Den{num}:')
            for key in state.Outros:
                print(f'{key}: {state.Outros[key].printName()}')
        num = 0 
        for state in self.KnownStates:
            num += 1
            print(f'Known{num}:')
            for key in state.Outros:
                print(f'{key}: {state.Outros[key].printName()}')
        num = 0
        
    # def filloutDisplay(self, state, stateDic, nodeX, nodeY):
    #     nodeX.append
        
    def display(self):
        nodex = []
        nodey = []
        edgex = []
        edgey = []
        node_labels = []
        edge_labels = []
        beenTo = {}
            
        for state in self.PickStates:
            if state not in beenTo:
                x,y = state.getLocation()
                node_labels.append(state.printName())
                nodey.append(y)
                nodex.append(x)
                beenTo[state] = True
            for key in state.Outros:
                currState = state.Outros[key]
                x1,y1 = currState.getLocation()
                midpointX = x + ((x1 - x) / 2)
                midpointY = y + ((y1 - y) / 2)
                edgex.append(x)
                edgey.append(y)
                edge_labels.append("")
                edgex.append(midpointX)
                edgey.append(midpointY)
                edge_labels.append(f"{key}")
                edgex.append(x1)
                edgey.append(y1)
                edge_labels.append("")
                edgex.append(None)
                edgey.append(None)
                edge_labels.append("")
    
        for state in self.DropStates:            
            if state not in beenTo:
                x,y = state.getLocation()
                node_labels.append(state.printName())
                nodey.append(y)
                nodex.append(x)
                beenTo[state] = True
            for key in state.Outros:
                currState = state.Outros[key]
                x1,y1 = currState.getLocation()
                midpointX = x + ((x1 - x) / 2)
                midpointY = y + ((y1 - y) / 2)
                edgex.append(x)
                edgey.append(y)
                edge_labels.append("")
                edgex.append(midpointX)
                edgey.append(midpointY)
                edge_labels.append(f"{key}")
                edgex.append(x1)
                edgey.append(y1)
                edge_labels.append("")
                edgex.append(None)
                edgey.append(None)
                edge_labels.append("")
    
        for state in self.ConsumeStates:            
            if state not in beenTo:
                x,y = state.getLocation()
                node_labels.append(state.printName())
                nodey.append(y)
                nodex.append(x)
                beenTo[state] = True
            for key in state.Outros:
                currState = state.Outros[key]
                x1,y1 = currState.getLocation()
                midpointX = x + ((x1 - x) / 2)
                midpointY = y + ((y1 - y) / 2)
                edgex.append(x)
                edgey.append(y)
                edge_labels.append("")
                edgex.append(midpointX)
                edgey.append(midpointY)
                edge_labels.append(f"{key}")
                edgex.append(x1)
                edgey.append(y1)
                edge_labels.append("")
                edgex.append(None)
                edgey.append(None)
                edge_labels.append("")
    
        for state in self.ExploreStates:            
            if state not in beenTo:
                x,y = state.getLocation()
                node_labels.append(state.printName())
                nodey.append(y)
                nodex.append(x)
                beenTo[state] = True
            for key in state.Outros:
                currState = state.Outros[key]
                x1,y1 = currState.getLocation()
                midpointX = x + ((x1 - x) / 2)
                midpointY = y + ((y1 - y) / 2)
                edgex.append(x)
                edgey.append(y)
                edge_labels.append("")
                edgex.append(midpointX)
                edgey.append(midpointY)
                edge_labels.append(f"{key}")
                edgex.append(x1)
                edgey.append(y1)
                edge_labels.append("")
                edgex.append(None)
                edgey.append(None)
                edge_labels.append("")
    
        for state in self.DenStates:            
            if state not in beenTo:
                x,y = state.getLocation()
                node_labels.append(state.printName())
                nodey.append(y)
                nodex.append(x)
                beenTo[state] = True
            for key in state.Outros:
                currState = state.Outros[key]
                x1,y1 = currState.getLocation()
                midpointX = x + ((x1 - x) / 2)
                midpointY = y + ((y1 - y) / 2)
                edgex.append(x)
                edgey.append(y)
                edge_labels.append("")
                edgex.append(midpointX)
                edgey.append(midpointY)
                edge_labels.append(f"{key}")
                edgex.append(x1)
                edgey.append(y1)
                edge_labels.append("")
                edgex.append(None)
                edgey.append(None)
                edge_labels.append("")
    
        for state in self.KnownStates:            
            if state not in beenTo:
                x,y = state.getLocation()
                node_labels.append(state.printName())
                nodey.append(y)
                nodex.append(x)
                beenTo[state] = True
            for key in state.Outros:
                currState = state.Outros[key]
                x1,y1 = currState.getLocation()
                midpointX = x + ((x1 - x) / 2)
                midpointY = y + ((y1 - y) / 2)
                edgex.append(x)
                edgey.append(y)
                edge_labels.append("")
                edgex.append(midpointX)
                edgey.append(midpointY)
                edge_labels.append(f"{key}")
                edgex.append(x1)
                edgey.append(y1)
                edge_labels.append("")
                edgex.append(None)
                edgey.append(None)
                edge_labels.append("")
    
        edge_trace = go.Scatter(
            x=edgex, y=edgey,
            mode='lines+text',
            # hoverinfo='text',
            # hovertext=edge_labels,
            line=dict(width=0.5),
            marker=dict(symbol="arrow-right"),
            text=edge_labels,
            textposition='middle left'
        )
        
        node_trace = go.Scatter(
            x=nodex, y=nodey,
            mode='markers+text',
            text=node_labels,
            textposition='top center'
        )
        
        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title='Agent State Machine',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                )
            )
        
        pio.renderers.default = 'notebook'
        fig.show()
                
    def changeState(self, input):
        self.CurrentState = self.CurrentState.changeState(input)
        return self.CurrentState
        # inputs the input into the current state
    
    def getStartState(self):
        return self.StartInput["start"]
    
class State:
    def __init__(self, disIncr, availableInputs):
        self.Outros = {}
        self.displayLocation = (disIncr + random.randint(0,3), random.randint(0, 20))
        self.inputs = availableInputs
    
    def isFull(self):
        isFull = True
        for input in self.inputs:
            if input not in self.Outros:
                isFull = False
        return isFull
        
    def getLocation(self):
        return self.displayLocation
    
    def changeState(self, input):
        if input in self.Outros:
            return self.Outros[input]
        else:
            return None
    
    def inputState(self, input, state):
        if input not in self.Outros:
            self.Outros[input] = state
        
class Pick(State):
    def printName(self):
        return "Pick"
    def behavior(self):
        return "Pick"

class Drop(State):
    def printName(self):
        return "Drop"
    def behavior(self):
        return "Drop"
    
class Consume(State):
    def printName(self):
        return "Consume"
    def behavior(self):
        return "Consume"
    
class Explore(State):
    def printName(self):
        return "Explore"
    def behavior(self):
        return "Explore"
    
class Den(State):
    def printName(self):
        return "Den"
    def behavior(self):
        return "Den"
    
class Known(State):
    def printName(self):
        return "Known"
    def behavior(self):
        return "Known"