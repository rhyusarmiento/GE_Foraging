from const import ENVIORN_DIM, HUNGER
import pygame as py
import numpy as np

class Environment:
    def __init__(self):
        self.objects = set()
        self.positions = {}
        self.numFood = 0
        self.screen = py.display.set_mode((ENVIORN_DIM, ENVIORN_DIM))
    
    def startAction(self):
        py.init()
        self.screen.fill('white')
        self.screen.blit()
        
    # def updateScreen(self):
    #     for row in self.spacesYX:
    #         for spot in row:
    #             if spot is not None:
    #                 if spot.who() == "Food":
    #                     py.draw.circle(self.screen, (0, 255, 0, 100), spot.locationXY, 3)
    #                 elif spot.who() == "Den":
    #                     py.draw.circle(self.screen, (0, 100, 0, 100), spot.locationXY, 12)

    # def printSpace(self):
    #     for y in self.spacesYX:
    #         printStr = ""
    #         for x in y:
    #             if x is None:
    #                 printStr += "o"
    #             elif x.who() == "Food":
    #                 printStr += "F"
    #             elif x.who() == "Den":
    #                 printStr += "D"
    #         print(printStr)
            
    def addFood(self, food):
        self.numFood += food
            
    def removeFood(self, food):
        self.numFood -= food
            
    def addNewObject(self, item):
        newObject = item
        positions = []
        radius = item.size // 2
        x,y = item.center
        xStart = x - radius
        yStart = y - radius
        xCurr = xStart
        yCurr = yStart
        
        # get new positions
        for xCurr in range(xStart + (2 * radius)):
            for yCurr in range(yStart + (2 * radius)):
                newPosition = None
                if item.isFill:
                    newPosition = (self.cleanCor(xCurr), self.cleanCor(yCurr))
                elif (xCurr != xStart or xCurr != (xStart + (2 * radius))) and (yCurr != yStart or yCurr != (yStart + (2 * radius))):
                    newPosition = (self.cleanCor(xCurr), self.cleanCor(yCurr))
                if newPosition is not None:
                    positions.append(newPosition)
        
        # add new object
        for newPosition in positions:
            newObject.addPosition(newPosition)
            self.positions.setdefault(newPosition, set()).add(newObject)
        self.objects.add(newObject)
        
    def cleanCor(self, num):
        clean = num
        if num >= ENVIORN_DIM:
            clean = (num - ENVIORN_DIM)
        if num < 0:
            clean = (ENVIORN_DIM + num)
        return clean
    
    # def isPosition(self, newLocation):
    #     if newLocation in self.positions:
    #         return True
    #     else:
    #         return False
        
    def removeObject(self, object, positions):
        for position in positions:
            self.positions[position].remove(object)
            if len(self.positions[position]) == 0:
                del self.positions[position]
        
    def addObject(self, object, positions):
        for position in positions:
            self.positions.setdefault(position, set()).add(object)
    
    def isObjectByLocation(self, location):
        x,y = location
        cleanLocation = (self.cleanCor(x), self.cleanCor(y))
        if cleanLocation in self.positions:
            return True
        return False
    
    def getObjectsByLocation(self, location):
        x,y = location
        cleanLocation = (self.cleanCor(x), self.cleanCor(y))
        if cleanLocation in self.positions:
            return self.positions[cleanLocation]
        return None
    
# TODO make every other enviroment object an inheritance of the Wrapper
class ObjectWraper:
    def __init__(self, environment, location):
        self.positions = []
        self.world = environment
        self.center = location
        
    def addPosition(self, position):
        self.positions.append(position)
        
    def who():
        return "Empty Object"
    
    def cleanCor(self, num):
        return self.world.cleanCor(num)
        
    def seeLocation(self, location):
        return self.world.getObjectsByLocation(location)
        
    def moveTo(self, newPositions):
        self.world.removeObject(self, self.positions)
        self.positions.clear()
        self.positions.append(newPositions)
        self.world.addObject(self, self.positions)
        
    def moveNorth(self):
        newPositions = []
        x,y = self.center
        self.center = (x, y + 1)
        for position in self.positions:
            newPositions.append(position[0], position[1] + 1)
        
        self.moveTo(newPositions)

    def moveSouth(self):
        newPositions = []
        x,y = self.center
        self.center = (x, y - 1)
        for position in self.positions:
            newPositions.append(position[0], position[1] - 1)
        
        self.moveTo(newPositions)
        
    def moveWest(self):
        newPositions = []
        x,y = self.center
        self.center = (x - 1, y)
        for position in self.positions:
            newPositions.append(position[0] - 1, position[1])
        
        self.moveTo(newPositions)

    def moveEast(self):
        newPositions = []
        x,y = self.center
        self.center = (x + 1, y)
        for position in self.positions:
            newPositions.append(position[0] + 1, position[1])
        
        self.moveTo(newPositions)
        
    def getWorldFood(self):
        return self.world.numFood
    
    def removeWorldFood(self, num):
        self.world.removeFood(num)
    
    def removeWorldObject(self, object):
        self.world.removeObject(object, object.positions)
        
    def addWorldObject(self, item):
        self.world.addNewObject(item)

class AgentBody(ObjectWraper):
    # all movement and interface with the environment
    def __init__(self, environment, location, agentMind, base):
        super().__init__(environment, location)
        self.agentBrain = agentMind
        self.home = base
        self.size = 5
        self.isFill = True
        self.numFood = 0
        self.hunger = HUNGER
        self.isXCorDirection = True
        self.heading = "North"
        self.movement = 0
        self.vision = 5
            
    def who(self):
        return "Agent"
    
    def getHomeScore(self):
        return self.home.foodStored - self.getWorldFood()
    
    def checkForAgents(self):
        agentsNear = []
        radius = self.vision // 2
        x,y = self.center
        xStart = x - radius
        yStart = y - radius
        xCurr = xStart
        yCurr = yStart
    
        for xCurr in range(xStart + (2 * radius)):
            for yCurr in range(yStart + (2 * radius)):
                objects = self.seeLocation((self.cleanCor(xCurr), self.cleanCor(yCurr)))
                for object in objects:
                    if object is not None and object.who() == "Agent":
                        agentsNear.append(object)
        return agentsNear
    
    def checkForFood(self):
        foodNear = []
        radius = self.vision // 2
        x,y = self.center
        xStart = x - radius
        yStart = y - radius
        xCurr = xStart
        yCurr = yStart
    
        for xCurr in range(xStart + (2 * radius)):
            for yCurr in range(yStart + (2 * radius)):
                objects = self.seeLocation((self.cleanCor(xCurr), self.cleanCor(yCurr)))
                for object in objects:
                    if object is not None and object.who() == "Food":
                        foodNear.append(object)
        return foodNear
    
    # picks up all food within vision
    def pick(self):
        radius = self.vision // 2
        x,y = self.center
        xStart = x - radius
        yStart = y - radius
        xCurr = xStart
        yCurr = yStart
    
        for xCurr in range(xStart + (2 * radius)):
            for yCurr in range(yStart + (2 * radius)):
                objects = self.seeLocation((self.cleanCor(xCurr), self.cleanCor(yCurr)))
                for object in objects:
                    if object is not None and object.who() == "Food":
                        if object.takeFood():
                            self.numFood += 1
                            self.removeWorldFood(1)
                        else:
                            self.removeWorldObject(object)
                            del object
            
    def drop(self):
        radius = self.vision // 2
        x,y = self.center
        xStart = x - radius
        yStart = y - radius
        xCurr = xStart
        yCurr = yStart
        dropFood = 1
    
        for xCurr in range(xStart + (2 * radius)):
            if dropFood > 0:
                for yCurr in range(yStart + (2 * radius)):
                    objects = self.seeLocation((self.cleanCor(xCurr), self.cleanCor(yCurr)))
                    for object in objects:
                        if object is not None and object.who() == "Food":
                            object.item.addFood()
                            dropFood -= 1
                        elif object.who() == "Den":
                            object.item.depositFood(1)
                            dropFood -= 1
                        else:
                            self.addWorldObject(FoodContainer(self.world, self.center))
                            dropFood -= 1
            
    def consume(self):
        if self.numFood > 0:
            self.numFood -= 1
            self.hunger += 3
    
    def left(self):
        if self.heading == "North":
            self.hunger -= .5
            self.heading = "West"
            self.moveWest()
        elif self.heading == "South":
            self.hunger -= .5
            self.heading = "East"
            self.moveEast()
        elif self.heading == "East":
            self.hunger -= .5
            self.heading = "North"
            self.moveNorth()
        elif self.heading == "West":
            self.hunger -= .5
            self.heading = "South"
            self.moveSouth()
    
    def forward(self):
        if self.heading == "West":
            self.hunger -= .5
            self.heading = "West"
            self.moveWest()
        elif self.heading == "East":
            self.hunger -= .5
            self.heading = "East"
            self.moveEast()
        elif self.heading == "North":
            self.hunger -= .5
            self.heading = "North"
            self.moveNorth()
        elif self.heading == "South":
            self.hunger -= .5
            self.heading = "South"
            self.moveSouth()
    
    def right(self):
        if self.heading == "South":
            self.hunger -= .5
            self.heading = "West"
            self.moveWest()
        elif self.heading == "North":
            self.hunger -= .5
            self.heading = "East"
            self.moveEast()
        elif self.heading == "West":
            self.hunger -= .5
            self.heading = "North"
            self.moveNorth()
        elif self.heading == "East":
            self.hunger -= .5
            self.heading = "South"
            self.moveSouth()
            
    def denGoToo(self):
        currLocation = self.center
        if currLocation != self.home.center:
            self.direction = tuple(np.subtract(self.home.center, currLocation))
            if self.isXCorDirection:
                if self.direction[0] > 0:
                    self.moveEast()
                elif self.direction[0] < 0:
                    self.moveWest()
                self.isXCorDirection = False
            else:
                if self.direction[1] > 0:
                    self.moveNorth()
                elif self.direction[1] < 0:
                    self.moveSouth()
                self.isXCorDirection = True
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
        currLocation = self.center
        if currLocation != self.agentBrain.getKnownFood(0):
            self.direction = tuple(np.subtract(self.agentBrain.getKnownFood(0), currLocation))
            if self.isXCorDirection:
                if self.direction[0] > 0:
                    self.moveEast()
                elif self.direction[0] < 0:
                    self.moveWest()
                self.isXCorDirection = False
            else:
                if self.direction[1] > 0:
                    self.moveNorth()
                elif self.direction[1] < 0:
                    self.moveSouth()
                self.isXCorDirection = True
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
        
class FoodContainer(ObjectWraper):
    def __init__(self, environment, location, food=1):
        super().__init__(environment, location)
        self.foodHere = food
        self.size = 3
        self.isFill = True
    
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
        
class Den(ObjectWraper):
    def __init__(self, environment, location):
        super().__init__(environment, location)
        self.size = 15
        self.isFill = False
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