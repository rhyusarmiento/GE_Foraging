from const import ENVIORN_DIM, HUNGER, ENVIORNTEST, NEIGHBOOR_LIMIT
import pygame as py
import numpy as np
import random

class Environment:
    def __init__(self):
        self.objects = set()
        self.positions = {}
        self.numFood = 0
        self.size = ENVIORN_DIM
    
    def startAction(self):
        self.screen = py.display.set_mode((ENVIORN_DIM, ENVIORN_DIM))
        py.init()
        self.screen.fill('white') # not working 
        self.screen.blit()
        # sprites
        # image for surface
        # display filp
        
    # TODO: multi thread this function
    def testSetUp(self):
        self.size = ENVIORNTEST
        for x in range(self.size * (self.size // 4)):
            self.addNewObject(FoodContainer(self, (random.randint(0, self.size), random.randint(0, self.size))))
            
    def testReset(self):
        garbage = []
        for object in self.objects:
            if object.who() == "Agent":
                garbage.append(object)
            if object.who() == "Food" and object.foodHere > 1:
                self.numFood -= object.foodHere
                garbage.append(object)  
        
        for item in garbage:
            self.removeObject(item)
        
        differenceFood = (self.size * (self.size // 4)) - self.numFood
        if differenceFood > 0:
            for x in range(differenceFood):
                self.addNewObject(FoodContainer(self, (random.randint(0, self.size), random.randint(0, self.size))))
        elif differenceFood < 0:
            print(f"not good {differenceFood}")
        
        
    # TODO: work on display to see what is happening if happening 
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
        xEnd = xStart + (2 * radius)
        yEnd = yStart + (2 * radius)
        # TODO: location problem adding more spots than needed aka from 0
        # TODO: Adding masive food list big bug, also mulitiple agents
        # get new positions
        while xCurr <= xEnd:
            while yCurr <= yEnd:
                newPosition = None
                if item.isFill:
                    newPosition = tuple((self.cleanCor(xCurr), self.cleanCor(yCurr)))
                elif (yCurr == yStart and (xCurr >= xStart and xCurr <= xEnd)) or (yCurr == yEnd and (xCurr >= xStart and xCurr <= xEnd)) or (xCurr == xStart and (yCurr >= yStart and yCurr <= yEnd)) or (xCurr == xEnd and (yCurr >= yStart and yCurr <= yEnd)):
                    newPosition = tuple((self.cleanCor(xCurr), self.cleanCor(yCurr)))
                if newPosition is not None:
                    positions.append(newPosition)
                yCurr += 1
            yCurr = yStart
            xCurr += 1
        
        # add new object
        for newPosition in positions:
            newObject.addPosition(newPosition)
            positionSet = self.positions.setdefault(newPosition, set())
            positionSet.add(newObject)
        self.objects.add(newObject)
        
    def cleanCor(self, num):
        clean = num
        if num >= self.size:
            clean = (num - self.size)
        if num < 0:
            clean = (self.size + num)
        return clean
    
    # def isPosition(self, newLocation):
    #     if newLocation in self.positions:
    #         return True
    #     else:
    #         return False
                
    def removeObject(self, object):
        self.objects.remove(object)
        # print(f'bang {object}')
        for position in object.positions:
            positionSet = self.positions[position]
            positionSet.remove(object)
            if len(self.positions[position]) == 0:
                del self.positions[position]
        
    # TODO: location problem
    def addObject(self, object, objectPositions):
        self.objects.add(object)
        for position in objectPositions:
            positionSet = self.positions.setdefault(position, set())
            positionSet.add(object)
    
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
    
class ObjectWraper:
    def __init__(self, environment, location):
        self.positions = []
        self.world = environment
        self.center = (self.world.cleanCor(location[0]), self.world.cleanCor(location[1]))
        
    def addPosition(self, position):
        self.positions.append(position)
        
    def who():
        return "Empty Object"
    
    def cleanCor(self, num):
        return self.world.cleanCor(num)
        
    def seeLocation(self, location):
        return self.world.getObjectsByLocation(location)
        
    def moveTo(self, newPositions):
        self.world.removeObject(self)
        self.positions.clear()
        self.positions.extend(newPositions)
        self.world.addObject(self, self.positions)
        
    def moveNorth(self):
        newPositions = []
        x,y = self.center
        self.center = (x, y + 1)
        for position in self.positions:
            newPositions.append(tuple((position[0], position[1] + 1)))
        
        self.moveTo(newPositions)

    def moveSouth(self):
        newPositions = []
        x,y = self.center
        self.center = (x, y - 1)
        for position in self.positions:
            newPositions.append(tuple((position[0], position[1] - 1)))
        
        self.moveTo(newPositions)
        
    def moveWest(self):
        newPositions = []
        x,y = self.center
        self.center = (x - 1, y)
        for position in self.positions:
            newPositions.append(tuple((position[0] - 1, position[1])))
        
        self.moveTo(newPositions)

    def moveEast(self):
        newPositions = []
        x,y = self.center
        self.center = (x + 1, y)
        for position in self.positions:
            newPositions.append(tuple((position[0] + 1, position[1])))
        
        self.moveTo(newPositions)
        
    def getWorldFood(self):
        return self.world.numFood
    
    def removeWorldObject(self, object):
        self.world.removeObject(object)
        
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
        self.lifetimeFood = 0
        self.hunger = HUNGER
        self.isXCorDirection = True
        self.heading = "North"
        self.movement = 0
        self.vision = 5
        self.consumedFood = 0
        self.agentNearLimit = NEIGHBOOR_LIMIT
            
    def addFood(self, num):
        self.numFood += num
        self.lifetimeFood += num
      
    def who(self):
        return "Agent"
    
    def getHomeScore(self):
        return self.home.lifetimeFood
    
    def checkForAgents(self):
        agentsNear = []
        radius = self.vision // 2
        x,y = self.center
        xStart = x - radius
        yStart = y - radius
        xCurr = xStart
        yCurr = yStart
        limiter = self.agentNearLimit
    
        while limiter > 0 and xCurr <= xStart + (2 * radius):
            while limiter > 0 and yCurr <= yStart + (2 * radius):
                objects = self.seeLocation((self.cleanCor(xCurr), self.cleanCor(yCurr)))
                if objects is not None:
                    for object in objects:
                        if object.who() == "Agent" and limiter > 0:
                            agentsNear.append(object)
                            limiter -= 1
                yCurr += 1
            yCurr = yStart
            xCurr += 1
        return agentsNear
    
    def isFoodNear(self):
        radius = self.vision // 2
        x,y = self.center
        xStart = x - radius
        yStart = y - radius
        xCurr = xStart
        yCurr = yStart
        isFood = False
        
        while isFood is False and xCurr <= xStart + (2 * radius):
            while isFood is False and yCurr <= yStart + (2 * radius):
                objects = self.seeLocation((self.cleanCor(xCurr), self.cleanCor(yCurr)))
                if objects is not None:
                    for object in objects:
                        if object.who() == "Food":
                            isFood = True
                yCurr += 1
            yCurr = yStart
            xCurr += 1
            
        return isFood
    
    def checkForFooditems(self):
        foodNear = []
        radius = self.vision // 2
        x,y = self.center
        xStart = x - radius
        yStart = y - radius
        xCurr = xStart
        yCurr = yStart
    
        while xCurr <= xStart + (2 * radius):
            while yCurr <= yStart + (2 * radius):
                objects = self.seeLocation((self.cleanCor(xCurr), self.cleanCor(yCurr)))
                if objects is not None:    
                    for object in objects:
                        if object.who() == "Food":
                            foodNear.append(object)
                yCurr += 1
            yCurr = yStart
            xCurr += xStart
        return foodNear
    
    def pickFood(self, objects, pickLimit):
        garbage = set()
        if objects is not None:
            for object in objects:
                if object.who() == "Food":
                    if object.takeFood():
                        pickLimit -= 1
                        self.addFood(1)
                    else:
                        garbage.add(object)
        for item in garbage:
            self.removeWorldObject(item)
                        
    def pick(self):
        visionRadius = self.vision // 2
        bodyRadius = self.size // 2
        x,y = self.center
        xStart = x - visionRadius
        yStart = y - visionRadius
        xCurr = xStart
        yCurr = yStart
        xBodyStart = x - bodyRadius
        yBodyStart = y - bodyRadius
        xBodyCurr = xBodyStart
        yBodyCurr = yBodyStart
        pickLimit = 1
        
        # check core first
        objects = self.seeLocation((self.cleanCor(x), self.cleanCor(y)))
        self.pickFood(objects, pickLimit)
        
        while pickLimit > 0 and xBodyCurr <= xBodyStart + (2 * bodyRadius):
            while pickLimit > 0 and yBodyCurr <= yBodyStart + (2 * bodyRadius):
                objects = self.seeLocation((self.cleanCor(xBodyCurr), self.cleanCor(yBodyCurr)))
                self.pickFood(objects, pickLimit)
                yBodyCurr += 1 
            yBodyCurr = yBodyStart                     
            xBodyCurr += 1
        # not body
        while pickLimit > 0 and (xCurr <= xStart + (2 * visionRadius) and not (xCurr >= xBodyStart and xCurr <= xBodyStart + (2 * bodyRadius))):
            while pickLimit > 0 and (yCurr <= yStart + (2 * visionRadius) and not (yCurr >= yBodyStart and yCurr <= yBodyStart + (2 * bodyRadius))):
                objects = self.seeLocation((self.cleanCor(xCurr), self.cleanCor(yCurr)))
                self.pickFood(objects, pickLimit)
                yCurr += 1
            yCurr = yStart
            xCurr += 1
    
    def dropFood(self, objects, dropLimit):
        toAdd = []
        if objects is not None:
            for object in objects:
                # TODO: no checks on food
                if self.numFood > 0:
                    if object.who() == "Food":
                        object.addFood()
                        self.numFood -= 1
                        dropLimit -= 1
                    elif object.who() == "Den":
                        object.depositFood(1)
                        self.numFood -= 1
                        dropLimit -= 1
                    else:
                        toAdd.append(FoodContainer(self.world, self.center))
                        self.numFood -= 1
                        dropLimit -= 1
        for item in toAdd:
            self.addWorldObject(item)
    
    def drop(self):
        radius = self.vision // 2
        bodyRadius = self.size // 2
        x,y = self.center
        xStart = x - radius
        yStart = y - radius
        xCurr = xStart
        yCurr = yStart
        xBodyStart = x - bodyRadius
        yBodyStart = y - bodyRadius
        xBodyCurr = xBodyStart
        yBodyCurr = yBodyStart
        dropLimit = 1
        
        # check core first
        objects = self.seeLocation((self.cleanCor(x), self.cleanCor(y)))
        self.dropFood(objects, dropLimit)
        
        while dropLimit > 0 and xBodyCurr <= xBodyStart + (2 * bodyRadius):
            while dropLimit > 0 and yBodyCurr <= yBodyStart + (2 * bodyRadius):
                objects = self.seeLocation((self.cleanCor(xBodyCurr), self.cleanCor(yBodyCurr)))
                self.dropFood(objects, dropLimit)
                yBodyCurr += 1  
            yBodyCurr = yBodyStart                    
            xBodyCurr += 1
        # not body
        while dropLimit > 0 and (xCurr <= xStart + (2 * radius) and not (xCurr >= xBodyStart and xCurr <= xBodyStart + (2 * bodyRadius))):
            while dropLimit > 0 and (yCurr <= yStart + (2 * radius) and not (yCurr >= yBodyStart and yCurr <= yBodyStart + (2 * bodyRadius))):
                objects = self.seeLocation((self.cleanCor(xCurr), self.cleanCor(yCurr)))
                self.dropFood(objects, dropLimit)
                yCurr += 1
            yCurr = yStart
            xCurr += 1
            
    def consume(self):
        if self.numFood > 0:
            self.numFood -= 1
            self.consumedFood += 1
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
                self.home.eatFood()
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
        self.world.addFood(food)
    
    def addFood(self):
        self.foodHere += 1
        self.world.addFood(1)
    
    def who(self):
        return "Food"
    
    def takeFood(self):
        if self.foodHere <= 0:
            return False
        elif self.foodHere > 0:
            self.foodHere -= 1
            self.world.removeFood(1)
            return True
        
class Den(ObjectWraper):
    def __init__(self, environment, location):
        super().__init__(environment, location)
        self.size = 15
        self.isFill = False
        self.lifetimeFood = 0
        self.foodStored = 0
    
    def who(self):
        return "Den"
    
    def depositFood(self, food):
        self.foodStored += food
        self.lifetimeFood += food
    
    def eatFood(self):
        self.foodStored -= 1
    
    def testReset(self):
        self.foodStored = 0    
    
    def isfeed(self):
        if self.foodStored > 0:
            return True
        else:
            return False
        

if __name__ == "__main__":
    envir = Environment()
    base = Den(envir, (30,30))
    envir.addNewObject(base)
    food = None
    for i in range(1):
        food = FoodContainer(envir, (random.randint(0, ENVIORN_DIM), random.randint(0, ENVIORN_DIM)))
        envir.addNewObject(food)
    
    envir.removeObject(base)
    
    for position in envir.positions:
        print(f'envir {position} {envir.positions[position]}')
    
    for spot in food.positions:
        print(f'food {spot}')
    
    food.moveEast()
    
    for position in envir.positions:
        print(f'envir {position} {envir.positions[position]}')
    
    for spot in food.positions:
        print(f'food {spot}')