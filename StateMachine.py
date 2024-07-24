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
    
    def createSM(self, phenotype, genotype):
        commandList = phenotype.replace(",", " ").split()
        isFirst = True
        inCre = 0
        for command in commandList:
            inCre += 1
            if command == "Pick":
                node = Pick(inCre)
                self.PickStates.append(node)
                if isFirst is True:
                    self.StartInput["start"] = node
                    isFirst = False
            elif command == "Drop":
                node = Drop(inCre)
                self.DropStates.append(node)
                if isFirst is True:
                    self.StartInput["start"] = node
                    isFirst = False
            elif command == "Consume":
                node = Consume(inCre)
                self.ConsumeStates.append(node)
                if isFirst is True:
                    self.StartInput["start"] = node
                    isFirst = False
            elif command == "Explore":
                node = Explore(inCre)
                self.ExploreStates.append(node)
                if isFirst is True:
                    self.StartInput["start"] = node
                    isFirst = False
            elif command == "Den":
                node = Den(inCre)
                self.DenStates.append(node)  
                if isFirst is True:
                    self.StartInput["start"] = node
                    isFirst = False  
            elif command == "Known":
                node = Known(inCre)
                self.KnownStates.append(node)
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
                edgex.append(x)
                edgex.append(x1)
                edgex.append(None)
                edgey.append(y)
                edgey.append(y1)
                edgey.append(None)
                edge_labels.append(key)
                
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
                edgex.append(x)
                edgex.append(x1)
                edgex.append(None)
                edgey.append(y)
                edgey.append(y1)
                edgey.append(None)
                edge_labels.append(key)
        
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
                edgex.append(x)
                edgex.append(x1)
                edgex.append(None)
                edgey.append(y)
                edgey.append(y1)
                edgey.append(None)
                edge_labels.append(key)
                
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
                edgex.append(x)
                edgex.append(x1)
                edgex.append(None)
                edgey.append(y)
                edgey.append(y1)
                edgey.append(None)
                edge_labels.append(key)
                
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
                edgex.append(x)
                edgex.append(x1)
                edgex.append(None)
                edgey.append(y)
                edgey.append(y1)
                edgey.append(None)
                edge_labels.append(key)
                
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
                edgex.append(x)
                edgex.append(x1)
                edgex.append(None)
                edgey.append(y)
                edgey.append(y1)
                edgey.append(None)
                edge_labels.append(key)
    
        edge_trace = go.Scatter(
            x=edgex, y=edgey,
            mode='lines+text',
            line=dict(width=0.5, color='#888'),
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
    def __init__(self, disIncr):
        self.Outros = {}
        self.displayLocation = (disIncr + random.randint(0,3), random.randint(0, 20))
    
    def getLocation(self):
        return self.displayLocation
    
    def changeState(self, input):
        # check state?
        return self.Outros[input]
    
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