from const import ENVIORN_DIM, ENVIORNTEST, TESTFOOD, WORLDFILL, DENBORDERSIZE, FOODCOLOR, FOODSIZE, DENCOLOR, DENSIZE, TOTALFOOD #FOODPERCENT,
from const import AGENTSIZE, AGENTVISIONINCREASE, AGENTCOLOR, NEIGHBOOR_LIMIT, HUNGER, MOVEMENTSPEED, EVO_SEC
from const import NORTH, AGENT, FOOD, DEN, WEST, EAST, SOUTH, ISDONE
import pygame as pyg
import numpy as np
import random
import threading
# import math as m

lock_envir = threading.Lock()
lock_food = threading.Lock()
lock_den = threading.Lock()
lock_object = threading.Lock()
lock_denFood = threading.Lock()
lock_move = threading.Lock()

class Environment:
    def __init__(self):
        self.objects = set()
        self.mapPositions = {}
        self.numFood = 0
        self.size = ENVIORN_DIM
        # self.sprites = pyg.sprite.Group()
        self.rendering = False
                        
    def startPyGame(self):
        pyg.init()
        self.screen = pyg.display.set_mode((ENVIORN_DIM, ENVIORN_DIM))
        self.screen.fill(WORLDFILL)
        clock = pyg.time.Clock() 
        
        self.rendering = True
        while(self.rendering):
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    self.rendering = False
                    
            
            agentlist = []
            self.screen.fill(WORLDFILL)
            for object in self.objects.copy():
                if object.who() == AGENT:
                    agentlist.append(object)
                else:
                    self.drawObject(object)
                    
            numAgents = 0
            numDone = 0
            for object in agentlist:
                self.drawObject(object)
                numAgents += 1
                if object.agentBrain.running is False:
                    numDone += 1
                
            # print(f"{numAgents} to done {numDone}")
            if numAgents == numDone:
                self.rendering = False
                
            pyg.display.flip()
            clock.tick(60)
            
    def drawObject(self, object):
        if object.who() == DEN:
            pyg.draw.lines(self.screen, object.color, False, object.positions, width=DENBORDERSIZE)
        elif object.who() == AGENT:
            pyg.draw.rect(self.screen, object.color, (object.center[0], object.center[1], (object.size), (object.size)), width=0)
            # print(f'{object.center}')
        elif object.who() == FOOD:
            pyg.draw.rect(self.screen, object.color, (object.center[0], object.center[1], (object.size), (object.size)), width=0)

    # TODO: multi thread this function (maybe)
    def testSetUp(self):
        self.size = ENVIORNTEST
        for x in range(TOTALFOOD):
            self.addNewObject(FoodContainer(self, (random.randint(0, self.size), random.randint(0, self.size))))
            
    def testReset(self):
        garbage = []
        for object in self.objects:
            if object.who() == AGENT:
                garbage.append(object)
            if object.who() == FOOD and object.foodHere > 1:
                self.numFood -= object.foodHere
                garbage.append(object)  
        
        for item in garbage:
            self.removeObject(item)
        
        differenceFood = (TOTALFOOD) - self.numFood
        if differenceFood > 0:
            for x in range(differenceFood):
                self.addNewObject(FoodContainer(self, (random.randint(0, self.size), random.randint(0, self.size))))
        elif differenceFood < 0:
            print(f"not good {differenceFood}")

    def testEvoSetup(self):
        garbage = []
        for object in self.objects:
            if object.who() == AGENT:
                garbage.append(object)
            if object.who() == FOOD and object.foodHere > 1:
                self.numFood -= object.foodHere
                garbage.append(object)  
        
        for item in garbage:
            self.removeObject(item)
        
        differenceFood = (TESTFOOD) - self.numFood
        if differenceFood > 0:
            for x in range(differenceFood):
                self.addNewObject(FoodContainer(self, (random.randint(0, self.size), random.randint(0, self.size))))
        elif differenceFood < 0:
            print(f"not good {differenceFood}")
    
    def printEnvironment(self):
        pass
            
    def addFood(self, food):
        with lock_envir:
            self.numFood += food
            
    def removeFood(self, food):
        with lock_envir:
            self.numFood -= food
                                
    def addNewObject(self, item):
        # if item.who() == AGENT:
        #     print("bro")
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
        with lock_object:
            for newPosition in positions:
                newObject.addPosition(newPosition)
                positionSet = self.mapPositions.setdefault(newPosition, set())
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
    
    # TODO: contiune to be movement problems  
    def removeObject(self, object):
        if object.who() != AGENT:
            with lock_object:    
                if object in self.objects:
                    self.objects.remove(object)
                    # print(f'bang {object}')
                    for position in object.positions:
                        positionSet = self.mapPositions[position]
                        positionSet.remove(object)
                        if len(self.mapPositions[position]) == 0:
                            del self.mapPositions[position]
        else:
            # print(f'bang {object}')
            with lock_move:
                for position in object.positions:
                    if position not in self.mapPositions:
                        print(f"not here {position}")
                # why wouldn't an agent position be recorded in the positions
                        positionSet = self.mapPositions.get(position)
                        if positionSet is None:
                            print(f"not here {position}")
                        positionSet.remove(object)
                        if len(positionSet) == 0:
                            self.mapPositions.pop(position)
                self.objects.remove(object)
        
    # TODO: location problem
    def addObject(self, object, objectPositions):
        with lock_move:
            self.objects.add(object)
            for position in objectPositions:
                positionSet = self.mapPositions.setdefault(position, set())
                positionSet.add(object)
    
    def isObjectByLocation(self, location):
        x,y = location
        cleanLocation = (self.cleanCor(x), self.cleanCor(y))
        if cleanLocation in self.mapPositions:
            return True
        return False
    
    def getObjectsByLocation(self, location):
        x,y = location
        cleanLocation = (self.cleanCor(x), self.cleanCor(y))
        if cleanLocation in self.mapPositions:
            return self.mapPositions[cleanLocation]
        return None
    
class ObjectWraper:
    def __init__(self, environment, location):
        self.positions = []
        self.world = environment
        self.movedNum = 0
        self.lastMove = ""
        self.center = (self.world.cleanCor(location[0]), self.world.cleanCor(location[1]))
        
    def addPosition(self, position):
        self.positions.append(position)
        
    def who():
        return "Empty Object"
    
    def cleanCor(self, num):
        return self.world.cleanCor(num)
        
    def seeLocation(self, location):
        return self.world.getObjectsByLocation(location)
        
    def moveTo(self, newPositions, dir):
        self.world.removeObject(self)
        self.positions.clear()
        self.positions.extend(newPositions)
        self.world.addObject(self, self.positions)
        self.movedNum =+ 1
        self.lastMove = dir
        
    def moveNorth(self):
        newPositions = []
        x,y = self.center
        self.center = (x, self.world.cleanCor(y + MOVEMENTSPEED))
        for position in self.positions:
            newPositions.append(tuple((position[0], self.world.cleanCor(position[1] + MOVEMENTSPEED))))
        
        self.moveTo(newPositions, "north")

    def moveSouth(self):
        newPositions = []
        x,y = self.center
        self.center = (x, self.world.cleanCor(y - MOVEMENTSPEED))
        for position in self.positions:
            newPositions.append(tuple((position[0], self.world.cleanCor(position[1] - MOVEMENTSPEED))))
        
        self.moveTo(newPositions, "south")
        
    def moveWest(self):
        newPositions = []
        x,y = self.center
        self.center = (self.world.cleanCor(x - MOVEMENTSPEED), y)
        for position in self.positions:
            newPositions.append(tuple((self.world.cleanCor(position[0] - MOVEMENTSPEED), position[1])))
        
        self.moveTo(newPositions, "west")

    def moveEast(self):
        newPositions = []
        x,y = self.center
        self.center = (self.world.cleanCor(x + MOVEMENTSPEED), y)
        for position in self.positions:
            newPositions.append(tuple((self.world.cleanCor(position[0] + MOVEMENTSPEED), position[1])))
        
        self.moveTo(newPositions, "east")
        
    def getWorldFood(self):
        return self.world.numFood
    
    def removeWorldObject(self, object):
        # print(f"remove food {object}")
        self.world.removeObject(object)
        
    def addWorldObject(self, item):
        self.world.addNewObject(item)

# class AgentDisplay(pyg.sprite.Sprite):
#     def __init__(self, color, width, height):
#         super().__init__()
#         self.image = pyg.Surface([width, height])
#         self.image.fill(color)
#         self.rect = self.image.get_rect()

class AgentBody(ObjectWraper):
    # all movement and interface with the environment
    def __init__(self, environment, location, agentMind, base):
        super().__init__(environment, location)
        self.agentBrain = agentMind
        self.home = base
        self.size = AGENTSIZE
        self.isFill = True
        self.numFood = 0
        self.lifetimeFood = 0
        self.hunger = HUNGER
        self.isXCorDirection = True
        self.heading = NORTH
        self.movement = 0
        self.vision = AGENTSIZE + AGENTVISIONINCREASE
        self.consumedFood = 0
        self.color = AGENTCOLOR
        self.agentNearLimit = NEIGHBOOR_LIMIT
        self.foodDepositInterval = 0
        self.totalFoodInterval = 0
            
    def addFood(self, num):
        self.numFood += num
        self.totalFoodInterval += num
        self.lifetimeFood += num
      
    def who(self):
        return AGENT
    
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
                    for object in objects.copy():
                        if object.who() == AGENT and limiter > 0:
                            agentsNear.append(object)
                            limiter -= 1
                yCurr += 1
            yCurr = yStart
            xCurr += 1
        return agentsNear
    
    def isFoodNear(self):
        # radius = self.vision // 2
        # x,y = self.center
        # xStart = x - radius
        # yStart = y - radius
        # xCurr = xStart
        # yCurr = yStart
        # isFood = False
        
        foodNear = self.checkForFooditems()
        if len(foodNear) > 0:
            return True
        else:
            return False
        
        # while isFood is False and xCurr <= xStart + (2 * radius):
        #     while isFood is False and yCurr <= yStart + (2 * radius):
        #         objects = self.seeLocation((self.cleanCor(xCurr), self.cleanCor(yCurr)))
        #         if objects is not None:
        #             for object in objects.copy():
        #                 if object.who() == FOOD:
        #                     isFood = True
        #         yCurr += 1
        #     yCurr = yStart
        #     xCurr += 1
        # return isFood
            
    
    def checkForFooditems(self):
        # should be a set
        foodNear = set()
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
                    for object in objects.copy():
                        if object.who() == FOOD:
                            foodNear.add(object)
                yCurr += 1
            yCurr = yStart
            xCurr += xStart
            
        for food in foodNear:
            self.home.addFoodLocation(food)
            
        return foodNear
    
    def pickFood(self, objects, pickLimit):
        garbage = set()
        if objects is not None:
            for object in objects.copy():
                if object.who() == FOOD:
                    if object.takeFood():
                        pickLimit -= 1
                        self.addFood(1)
                    else:
                        garbage.add(object)
        for item in garbage:
            self.removeWorldObject(item)
            self.home.removeFoodLocation(item)
            # print(f"agent {self} pick food {item}")
                        
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
            for object in objects.copy():
                # TODO: no checks on food
                if self.numFood > 0:
                    if object.who() == FOOD:
                        object.addFood()
                        self.numFood -= 1
                        dropLimit -= 1
                    elif object.who() == DEN:
                        object.depositFood(1)
                        self.foodDepositInterval += 1
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
            # self.numFood -= 1
            self.consumedFood += 1
            # self.hunger += 3
    
    def left(self):
        if self.heading == NORTH:
            self.hunger -= .5
            self.heading = WEST
            self.moveWest()
        elif self.heading == SOUTH:
            self.hunger -= .5
            self.heading = EAST
            self.moveEast()
        elif self.heading == EAST:
            self.hunger -= .5
            self.heading = NORTH
            self.moveNorth()
        elif self.heading == WEST:
            self.hunger -= .5
            self.heading = SOUTH
            self.moveSouth()
    
    def forward(self):
        if self.heading == WEST:
            self.hunger -= .5
            self.heading = WEST
            self.moveWest()
        elif self.heading == EAST:
            self.hunger -= .5
            self.heading = EAST
            self.moveEast()
        elif self.heading == NORTH:
            self.hunger -= .5
            self.heading = NORTH
            self.moveNorth()
        elif self.heading == SOUTH:
            self.hunger -= .5
            self.heading = SOUTH
            self.moveSouth()
    
    def right(self):
        if self.heading == SOUTH:
            self.hunger -= .5
            self.heading = WEST
            self.moveWest()
        elif self.heading == NORTH:
            self.hunger -= .5
            self.heading = EAST
            self.moveEast()
        elif self.heading == WEST:
            self.hunger -= .5
            self.heading = NORTH
            self.moveNorth()
        elif self.heading == EAST:
            self.hunger -= .5
            self.heading = SOUTH
            self.moveSouth()
            
    def denGoToo(self):
        currLocation = self.center
        clock = pyg.time.Clock()
        
        if currLocation != self.home.center:
            while currLocation != self.home.center:
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
                    
                if self.agentBrain.should_end():
                    self.agentBrain.end()
                self.hunger -= .5
                currLocation = self.center
                clock.tick(100)
                
            self.home.depositFood(self.numFood)
            self.foodDepositInterval += self.numFood
            if self.numFood > 0:
                print(f"deposit {self.numFood}")
            self.numFood = 0
            
            while self.home.isfeed() and self.hunger < HUNGER:
                # self.home.eatFood()
                self.hunger += 10
                
            return ISDONE
        else:
            self.home.depositFood(self.numFood)
            self.foodDepositInterval += self.numFood
            if self.numFood > 0:
                print(f"deposit {self.numFood}")
            self.numFood = 0
            
            while self.home.isfeed() and self.hunger < HUNGER:
                # self.home.eatFood()
                self.hunger += 10
                
            return ISDONE
        
    def getHomeFoodSize(self):
        return len(self.home.foodLocations.copy())    
        
    def known(self):
        currLocation = self.center
        destination = self.home.getFoodLocation().center
        clock = pyg.time.Clock()
        
        while currLocation != destination and not self.needFood():
            self.direction = tuple(np.subtract(destination, currLocation))
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
            if self.agentBrain.should_end():
                self.agentBrain.end()
            self.hunger -= .5
            currLocation = self.center
            # print(f"continue {self.agentBrain.id}")
            clock.tick(100)
    
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
        self.size = FOODSIZE
        self.isFill = True
        self.color = FOODCOLOR
        self.world.addFood(food)
    
    def addFood(self):
        self.foodHere += 1
        self.world.addFood(1)
    
    def who(self):
        return FOOD
    
    def takeFood(self):
        with lock_food:
            if self.foodHere <= 0:
                return False
            elif self.foodHere > 0:
                self.foodHere -= 1
                # requires lock 
                self.world.removeFood(1)
                return True
        
class Den(ObjectWraper):
    def __init__(self, environment, location):
        super().__init__(environment, location)
        self.size = DENSIZE
        self.isFill = False
        self.lifetimeFood = 0
        self.foodStored = 0
        self.intervalFood = 0
        self.lastFoodVelAvg = 0
        self.CurrentFoodVelocityAvg = 0
        self.CurrentFoodAcclerAvg = 0
        self.color = DENCOLOR
        self.foodLocations = set()
    
    def who(self):
        return DEN
    
    def evoTimer(self):
        clock = pyg.time.Clock() 
        numSec = 0
        while self.world.rendering:
            numSec += 1
            if numSec == EVO_SEC:
                self.CurrentFoodVelocityAvg = self.intervalFood / EVO_SEC
                self.CurrentFoodAcclerAvg = (self.CurrentFoodVelocityAvg - self.lastFoodVelAvg) / EVO_SEC
                # Formula check done
                self.lastFoodVelAvg = self.CurrentFoodVelocityAvg
                self.intervalFood = 0 
                numSec = 0
            clock.tick(60)
    
    def depositFood(self, food):
        with lock_den:
            self.foodStored += food
            self.lifetimeFood += food
            self.intervalFood += food
    
    def eatFood(self):
        with lock_den:
            self.foodStored -= 1
    
    def testReset(self):
        self.foodStored = 0    
    
    def isfeed(self):
        # if self.foodStored > 0:
        #     return True
        # else:
        #     return False
        return True
        
    def getFoodLocation(self):
        with lock_denFood:
            toGo = self.foodLocations.pop()
            self.foodLocations.add(toGo)
            return toGo
    
    def addFoodLocation(self, food):
        with lock_denFood:
            self.foodLocations.add(food)
    
    def removeFoodLocation(self, food):
        with lock_denFood:
            self.foodLocations.discard(food)
        
if __name__ == "__main__":
    envir = Environment()
    base = Den(envir, (30,30))
    envir.addNewObject(base)
    food = None
    for i in range(1):
        food = FoodContainer(envir, (random.randint(0, ENVIORN_DIM), random.randint(0, ENVIORN_DIM)))
        envir.addNewObject(food)
    
    envir.removeObject(base)
    
    for position in envir.mapPositions:
        print(f'envir {position} {envir.mapPositions[position]}')
    
    for spot in food.positions:
        print(f'food {spot}')
    
    food.moveEast()
    
    for position in envir.mapPositions:
        print(f'envir {position} {envir.mapPositions[position]}')
    
    for spot in food.positions:
        print(f'food {spot}')