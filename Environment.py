from const import ENVIORN_DIM, NEIGHBOOR_LIMIT, HUNGER
import pygame as py
import numpy as np

class Environment:
    def __init__(self):
        self.playerSpaceYX = []
        self.spacesYX = []
        self.numFood = 0
        self.screen = py.display.set_mode((ENVIORN_DIM, ENVIORN_DIM))
        for y in range(ENVIORN_DIM):
            newRow = []
            for x in range(ENVIORN_DIM):
                newRow.append(None)
            self.spacesYX.append(newRow)
        
        for y in range(ENVIORN_DIM):
            newRow = []
            for x in range(ENVIORN_DIM):
                newRow.append({})
            self.playerSpaceYX.append(newRow)
    
    def startAction(self):
        py.init()
        self.screen.fill('white')
        self.screen.blit()
        
    def moveAgentNorth(self, locationXY, agent):
        self.playerSpaceYX[locationXY[0]][locationXY[1]].pop(agent)
        newXY = (self.cleanCor(locationXY[0]), self.cleanCor(locationXY[1] + 2))
        self.playerSpaceYX[newXY[1]][newXY[0]][agent] = agent

    def moveAgentSouth(self, locationXY, agent):
        self.playerSpaceYX[locationXY[0]][locationXY[1]].pop(agent)
        newXY = (self.cleanCor(locationXY[0]), self.cleanCor(locationXY[1] - 2))
        self.playerSpaceYX[newXY[1]][newXY[0]][agent] = agent
        
    def moveAgentWest(self, locationXY, agent):
        self.playerSpaceYX[locationXY[0]][locationXY[1]].pop(agent)
        newXY = (self.cleanCor(locationXY[0]) - 2, self.cleanCor(locationXY[1]))
        self.playerSpaceYX[newXY[1]][newXY[0]][agent] = agent

    def moveAgentEast(self, locationXY, agent):
        self.playerSpaceYX[locationXY[0]][locationXY[1]].pop(agent)
        newXY = (self.cleanCor(locationXY[0]) + 2, self.cleanCor(locationXY[1]))
        self.playerSpaceYX[newXY[1]][newXY[0]][agent] = agent
        
    def getNearestAgents(self, memory, currAgents):
        incre = 0
        while(len(memory) < NEIGHBOOR_LIMIT and len(currAgents) > incre):
            memory.append(currAgents[incre])
        
    def lookAround(self, locationXY):
        agentsNearMemory = []
        x,y = locationXY
        if len(self.playerSpaceYX[y][x].keys()) > 0 and len(agentsNearMemory) < NEIGHBOOR_LIMIT:
            self.getNearestAgents(agentsNearMemory, self.playerSpaceYX[y][x].keys())
        elif len(self.playerSpaceYX[y][x + 1].keys()) > 0 and len(agentsNearMemory) < NEIGHBOOR_LIMIT:
            self.getNearestAgents(agentsNearMemory, self.playerSpaceYX[y][x + 1].keys())
        elif len(self.playerSpaceYX[y][x - 1].keys()) > 0 and len(agentsNearMemory) < NEIGHBOOR_LIMIT:
            self.getNearestAgents(agentsNearMemory, self.playerSpaceYX[y][x - 1].keys())
        elif len(self.playerSpaceYX[y - 1][x].keys()) > 0 and len(agentsNearMemory) < NEIGHBOOR_LIMIT:
            self.getNearestAgents(agentsNearMemory, self.playerSpaceYX[y - 1][x].keys())
        elif len(self.playerSpaceYX[y + 1][x].keys()) > 0 and len(agentsNearMemory) < NEIGHBOOR_LIMIT:
            self.getNearestAgents(agentsNearMemory, self.playerSpaceYX[y + 1][x].keys())
        elif len(self.playerSpaceYX[y + 1][x + 1].keys()) > 0 and len(agentsNearMemory) < NEIGHBOOR_LIMIT:
            self.getNearestAgents(agentsNearMemory, self.playerSpaceYX[y + 1][x + 1].keys())
        elif len(self.playerSpaceYX[y - 1][x + 1].keys()) > 0 and len(agentsNearMemory) < NEIGHBOOR_LIMIT:
            self.getNearestAgents(agentsNearMemory, self.playerSpaceYX[y - 1][x + 1].keys())
        elif len(self.playerSpaceYX[y - 1][x - 1].keys()) > 0 and len(agentsNearMemory) < NEIGHBOOR_LIMIT:
            self.getNearestAgents(agentsNearMemory, self.playerSpaceYX[y - 1][x - 1].keys())
        elif len(self.playerSpaceYX[y + 1][x - 1].keys()) > 0 and len(agentsNearMemory) < NEIGHBOOR_LIMIT:
            self.getNearestAgents(agentsNearMemory, self.playerSpaceYX[y + 1][x - 1].keys())
        
        return agentsNearMemory
        
    def updateScreen(self):
        for row in self.spacesYX:
            for spot in row:
                if spot is not None:
                    if spot.who() == "Food":
                        py.draw.circle(self.screen, (0, 255, 0, 100), spot.locationXY, 3)
                    elif spot.who() == "Den":
                        py.draw.circle(self.screen, (0, 100, 0, 100), spot.locationXY, 12)

    def printSpace(self):
        for y in self.spacesYX:
            printStr = ""
            for x in y:
                if x is None:
                    printStr += "o"
                elif x.who() == "Food":
                    printStr += "F"
                elif x.who() == "Den":
                    printStr += "D"
            print(printStr)
               
    def preBuild(self, locationAndObject):
        None
            
    def addFood(self, food):
        self.numFood += food
            
    def removeFood(self, food):
        self.numFood -= food
            
    def inputObjectXY(self, location, object):
        x,y = location
        if self.getSpaceYX((x,y)) is None:
            if object is not None and object.who() == "Food":
                self.addFood(object.foodHere)
            self.spacesYX[self.cleanCor(y)][self.cleanCor(x)] = object
        elif self.getSpaceYX((x,y)).who() == "Food":
            if object is not None and object.who() == "Food":
                self.addFood(object.foodHere)
                self.getSpaceYX((x,y)).addFood()
            elif object.who() == "Den":
                self.removeFood(self.getSpaceYX((x,y)).foodHere)
                self.spacesYX[self.cleanCor(y)][self.cleanCor(x)] = object
        elif self.getSpaceYX((x,y)).who() == "Den":
            if object is not None and object.who() == "Food":
                self.addFood(object.foodHere)
                self.getSpaceYX((x,y)).depositFood(1)
        
    def cleanCor(self, num):
        clean = num
        if num >= ENVIORN_DIM:
            clean = (num - ENVIORN_DIM)
        if num < 0:
            clean = (ENVIORN_DIM + num)
        return clean 
        
    def inputLargeObjectXY(self, location, radius, object):
        xcor,ycor = location
        for y in range(radius):
            for x in range(radius):
                self.spacesYX[self.cleanCor(ycor + y)][self.cleanCor(xcor + x)] = object
        
        for y in range(radius):
            for x in range(radius):
                self.spacesYX[self.cleanCor(ycor + y)][self.cleanCor(xcor - x)] = object

        for y in range(radius):
            for x in range(radius):
                self.spacesYX[self.cleanCor(ycor - y)][self.cleanCor(xcor + x)] = object
        
        for y in range(radius):
            for x in range(radius):
                self.spacesYX[self.cleanCor(ycor - y)][self.cleanCor(xcor - x)] = object
        # a way to remove large object
        
    def getSpaceYX(self, location):
        x,y = location
        return self.spacesYX[self.cleanCor(y)][self.cleanCor(x)]
    
    def removeObjectXY(self, location):
        x,y = location
        object = self.getSpaceYX((x,y))
        if object is not None and object.who() == "Food":
            self.removeFood(object.foodHere)
            self.spacesYX[self.cleanCor(y)][self.cleanCor(x)] = None
    
class FoodContainer:
    def __init__(self, location, food=1):
        self.foodHere = food
        self.locationXY = location
    
    def addFood(self):
        self.foodHere += 1
    
    def who(self):
        return "Food"
    
    def takeFood(self):
        if self.foodHere <= 0:
            return False
        elif self.foodHere > 0:
            self.foodHere -= 1
            return True
        
class Den:
    def __init__(self, location):
        self.locationXY = location
        self.foodStored = 0
    
    def who(self):
        return "Den"
    
    def depositFood(self, food):
        self.foodStored += food
        
    def isfeed(self):
        if self.foodStored > 0:
            return True
        else:
            return False

class AgentBody:
    # all movement and interface with the environment
    def __init__(self, agent, environment, base):
        self.agentBrain = agent
        self.home = base
        self.locationXY = self.home.locationXY
        self.worldMap = environment
        self.agentSize = 10
        self.numFood = 0
        self.hunger = HUNGER
        self.isXCor = True
        self.heading = "North"
        self.movement = 0
    
    def who(self):
        return "Agent"
    
    def getHomeScore(self):
        return self.home.foodStored - self.worldMap.numFood
    
    def getAgentsNear(self):
        return self.worldMap.lookAround()
    
    def checkFood(self):
        x,y = self.locationXY
        if self.worldMap.checkSpaceXY((x + 1,y)) is not None and self.worldMap.checkSpaceXY((x + 1,y)).who() == "Food":
            self.agentBrain.addFoodLocation((x+1,y))
            return True
        if self.worldMap.checkSpaceXY((x - 1,y)) is not None and self.worldMap.checkSpaceXY((x-1,y)).who() == "Food":
            self.agentBrain.addFoodLocation((x-1,y))
            return True
        if self.worldMap.checkSpaceXY((x,y-1)) is not None and self.worldMap.checkSpaceXY((x,y-1)).who() == "Food":
            self.agentBrain.addFoodLocation((x,y-1))
            return True
        if self.worldMap.checkSpaceXY((x,y+1)) is not None and self.worldMap.checkSpaceXY((x,y+1)).who() == "Food":
            self.agentBrain.addFoodLocation((x,y+1))
            return True
        if self.worldMap.checkSpaceXY((x,y)) is not None and self.worldMap.checkSpaceXY((x,y)).who() == "Food":
            self.agentBrain.addFoodLocation((x,y))
            return True
        if self.worldMap.checkSpaceXY((x+1,y+1)) is not None and self.worldMap.checkSpaceXY((x+1,y+1)).who() == "Food":
            self.agentBrain.addFoodLocation((x+1,y+1))
            return True
        if self.worldMap.checkSpaceXY((x+1,y-1)) is not None and self.worldMap.checkSpaceXY((x+1,y-1)).who() == "Food":
            self.agentBrain.addFoodLocation((x+1,y-1))
            return True
        if self.worldMap.checkSpaceXY((x-1,y-1)) is not None and self.worldMap.checkSpaceXY((x-1,y-1)).who() == "Food":
            self.agentBrain.addFoodLocation((x-1,y-1))
            return True
        if self.worldMap.checkSpaceXY((x-1,y+1)) is not None and self.worldMap.checkSpaceXY((x-1,y+1)).who() == "Food":
            self.agentBrain.addFoodLocation((x-1,y+1))
            return True
        else:
            return False
    
    def pick(self):
        x,y = self.locationXY
        if self.worldMap.checkSpaceXY((x + 1,y)) is not None and self.worldMap.checkSpaceXY((x + 1,y)).who() == "Food":
            self.agentBrain.addFoodLocation((x + 1,y))
            if self.worldMap.checkSpaceXY((x + 1,y)).takeFood():
                self.numFood += 1
                self.worldMap.removeFood(1)
            else:
                self.worldMap.removeObjectXY((x+1,y))
        elif self.worldMap.checkSpaceXY((x,y)) is not None and self.worldMap.checkSpaceXY((x,y)).who() == "Food":
            self.agentBrain.addFoodLocation((x,y))
            if self.worldMap.checkSpaceXY((x,y)).takeFood():
                self.numFood += 1
                self.worldMap.removeFood(1)
            else:
                self.worldMap.removeObjectXY((x,y))
        elif self.worldMap.checkSpaceXY((x - 1,y)) is not None and self.worldMap.checkSpaceXY((x-1,y)).who() == "Food":
            self.agentBrain.addFoodLocation((x-1,y))
            if self.worldMap.checkSpaceXY((x-1,y)).takeFood():
                self.numFood += 1
                self.worldMap.removeFood(1)
            else:
                self.worldMap.removeObjectXY((x-1,y))
        elif self.worldMap.checkSpaceXY((x,y-1)) is not None and self.worldMap.checkSpaceXY((x,y-1)).who() == "Food":
            self.agentBrain.addFoodLocation((x,y-1))
            if self.worldMap.checkSpaceXY((x,y-1)).takeFood():
                self.numFood += 1
                self.worldMap.removeFood(1)
            else:
                self.worldMap.removeObjectXY((x,y-1))
        elif self.worldMap.checkSpaceXY((x,y+1)) is not None and self.worldMap.checkSpaceXY((x,y+1)).who() == "Food":
            self.agentBrain.addFoodLocation((x,y+1))
            if self.worldMap.checkSpaceXY((x,y+1)).takeFood():
                self.numFood += 1
                self.worldMap.removeFood(1)
            else:
                self.worldMap.removeObjectXY((x,y+1))
        elif self.worldMap.checkSpaceXY((x + 1,y+1)) is not None and self.worldMap.checkSpaceXY((x + 1,y+1)).who() == "Food":
            self.agentBrain.addFoodLocation((x + 1,y+1))
            if self.worldMap.checkSpaceXY((x + 1,y+1)).takeFood():
                self.numFood += 1
                self.worldMap.removeFood(1)
            else:
                self.worldMap.removeObjectXY((x+1,y+1))
        elif self.worldMap.checkSpaceXY((x+1,y-1)) is not None and self.worldMap.checkSpaceXY((x+1,y-1)).who() == "Food":
            self.agentBrain.addFoodLocation((x+1,y-1))
            if self.worldMap.checkSpaceXY((x+1,y-1)).takeFood():
                self.numFood += 1
                self.worldMap.removeFood(1)
            else:
                self.worldMap.removeObjectXY((x+1,y-1))
        elif self.worldMap.checkSpaceXY((x-1,y-1)) is not None and self.worldMap.checkSpaceXY((x-1,y-1)).who() == "Food":
            self.agentBrain.addFoodLocation((x-1,y-1))
            if self.worldMap.checkSpaceXY((x-1,y-1)).takeFood():
                self.numFood += 1
                self.worldMap.removeFood(1)
            else:
                self.worldMap.removeObjectXY((x-1,y-1))
        elif self.worldMap.checkSpaceXY((x-1,y+1)) is not None and self.worldMap.checkSpaceXY((x-1,y+1)).who() == "Food":
            self.agentBrain.addFoodLocation((x-1,y+1))
            if self.worldMap.checkSpaceXY((x-1,y+1)).takeFood():
                self.numFood += 1
                self.worldMap.removeFood(1)
            else:
                self.worldMap.removeObjectXY((x-1,y+1))
        
    def drop(self):
        if self.numFood > 0:
            self.numFood -= 1
            if self.worldMap.checkSpaceXY(self.locationXY) is not None and self.worldMap.checkSpaceXY(self.locationXY).who() == "Food":
                self.worldMap.checkSpaceXY(self.locationXY).addFood()
            elif self.worldMap.checkSpaceXY(self.locationXY) is not None and self.worldMap.checkSpaceXY(self.locationXY).who() == "Den":
                self.worldMap.checkSpaceXY(self.locationXY).depositFood(1)
            else:
                self.worldMap.inputObjectXY(self.locationXY, FoodContainer())
        
    def consume(self):
        if self.numFood > 0:
            self.numFood -= 1
            self.hunger += 3
    
    def left(self):
        x,y = self.locationXY
        if self.heading == "North":
            self.hunger -= .5
            self.heading = "West"
            self.locationXY = (self.worldMap.cleanCor(x-2),self.worldMap.cleanCor(y))
            self.moveAgentWest(self.locationXY, self)
        elif self.heading == "South":
            self.hunger -= .5
            self.heading = "East"
            self.locationXY = (self.worldMap.cleanCor(x+2),self.worldMap.cleanCor(y))
            self.moveAgentEast(self.locationXY, self)
        elif self.heading == "East":
            self.hunger -= .5
            self.heading = "North"
            self.locationXY = (self.worldMap.cleanCor(x),self.worldMap.cleanCor(y+2))
            self.moveAgentNorth(self.locationXY, self)
        elif self.heading == "West":
            self.hunger -= .5
            self.heading = "South"
            self.locationXY = (self.worldMap.cleanCor(x),self.worldMap.cleanCor(y-2))
            self.moveAgentSouth(self.locationXY, self)
    
    def forward(self):
        x,y = self.locationXY
        if self.heading == "West":
            self.hunger -= .5
            self.heading = "West"
            self.locationXY = (self.worldMap.cleanCor(x-2),self.worldMap.cleanCor(y))
            self.moveAgentWest(self.locationXY, self)
        elif self.heading == "East":
            self.hunger -= .5
            self.heading = "East"
            self.locationXY = (self.worldMap.cleanCor(x+2),self.worldMap.cleanCor(y))
            self.moveAgentEast(self.locationXY, self)
        elif self.heading == "North":
            self.hunger -= .5
            self.heading = "North"
            self.locationXY = (self.worldMap.cleanCor(x),self.worldMap.cleanCor(y+2))
            self.moveAgentNorth(self.locationXY, self)
        elif self.heading == "South":
            self.hunger -= .5
            self.heading = "South"
            self.locationXY = (self.worldMap.cleanCor(x),self.worldMap.cleanCor(y-2))
            self.moveAgentSouth(self.locationXY, self)
    
    def right(self):
        x,y = self.locationXY
        if self.heading == "South":
            self.hunger -= .5
            self.heading = "West"
            self.locationXY = (self.worldMap.cleanCor(x-2),self.worldMap.cleanCor(y))
            self.moveAgentWest(self.locationXY, self)
        elif self.heading == "North":
            self.hunger -= .5
            self.heading = "East"
            self.locationXY = (self.worldMap.cleanCor(x+2),self.worldMap.cleanCor(y))
            self.moveAgentEast(self.locationXY, self)
        elif self.heading == "West":
            self.hunger -= .5
            self.heading = "North"
            self.locationXY = (self.worldMap.cleanCor(x),self.worldMap.cleanCor(y+2))
            self.moveAgentNorth(self.locationXY, self)
        elif self.heading == "East":
            self.hunger -= .5
            self.heading = "South"
            self.locationXY = (self.worldMap.cleanCor(x),self.worldMap.cleanCor(y-2))
            self.moveAgentSouth(self.locationXY, self)
            
    def denGoToo(self):
        if self.locationXY != self.home.locationXY:
            self.direction = tuple(np.subtract(self.home.locationXY, self.locationXY))
            if self.isXCor:
                if self.direction[0] > 0:
                    self.locationXY = (self.locationXY[0] + 1, self.locationXY[1])
                elif self.direction[0] < 0:
                    self.locationXY = (self.locationXY[0] - 1, self.locationXY[1])
                self.isXCor = False
            else:
                if self.direction[1] > 0:
                    self.locationXY = (self.locationXY[0], self.locationXY[1] + 1)
                elif self.direction[1] < 0:
                    self.locationXY = (self.locationXY[0], self.locationXY[1] - 1)
                self.isXCor = True
            self.hunger -= .5
            return "continue" 
        else:
            self.home.depositFood(self.numFood)
            self.numFood = 0
        
            if self.home.isfeed() and self.hunger < 10:
                self.home.foodStored -= 1
                self.hunger += 3
                return "continue"
            else:
                return "isDone"
        
    def known(self):
        if self.locationXY != self.agentBrain.getKnownFood(0):
            direction = tuple(np.subtract(self.agentBrain.getKnownFood(0), self.locationXY))
            if self.isXCor:
                if direction[0] > 0:
                    self.locationXY = (self.locationXY[0] + 1, self.locationXY[1])
                elif direction[0] < 0:
                    self.locationXY = (self.locationXY[0] - 1, self.locationXY[1])
                self.isXCor = False
            else:
                if direction[1] > 0:
                    self.locationXY = (self.locationXY[0], self.locationXY[1] + 1)
                elif direction[1] < 0:
                    self.locationXY = (self.locationXY[0], self.locationXY[1] - 1)
                self.isXCor = True
            self.hunger -= .5
            return "continue"
    
    def isDead(self):
        if self.hunger < -10:
            return True
        else:
            return False
        
    def needFood(self):
        if self.hunger < 5:
            return True
        else: 
            return False
    
    def checkLoad(self):
        if self.numFood > 10:
            return True
        else:
            return False