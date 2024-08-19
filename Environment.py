from const import ENVIORN_DIM
import pygame as py

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
        
    def moveAgentLeft(self, locationXY, agent):
        self.playerSpaceYX[locationXY[0]][locationXY[1]].pop(agent)
        # left operation
        newXY = (0,0)
        self.playerSpaceYX[newXY[0]][newXY[1]][agent] = agent
        
    def lookAround(self, locationXY):
        agentsNear = []
        x,y = locationXY
        if len(self.playerSpaceYX[y][x + 1].keys()) > 0:
            agentsNear.append(self.playerSpaceYX[y][x + 1].keys())
        elif len(self.playerSpaceYX[y][x].keys()) > 0:
            agentsNear.append(self.playerSpaceYX[y][x].keys())
        elif len(self.playerSpaceYX[y][x].keys()) > 0:
            agentsNear.append(self.playerSpaceYX[y][x - 1].keys())
        elif self.playerSpaceYX((x,y-1)):
            agentsNear.append(self.playerSpaceYX[y - 1][x].keys())
        elif self.playerSpaceYX((x,y+1)):
            agentsNear.append(self.playerSpaceYX[y + 1][x].keys())
        elif self.playerSpaceYX((x + 1,y+1)):
            agentsNear.append(self.playerSpaceYX[y + 1][x + 1].keys())
        elif self.playerSpaceYX((x+1,y-1)):
            agentsNear.append(self.playerSpaceYX[y - 1][x + 1].keys())
        elif self.playerSpaceYX((x-1,y-1)):
            agentsNear.append(self.playerSpaceYX[y - 1][x - 1].keys())
        elif self.playerSpaceYX((x-1,y+1)):
            agentsNear.append(self.playerSpaceYX[y + 1][x - 1].keys())
        
        return agentsNear
        
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
        if self.playerSpaceYX((x,y)) is None:
            if object is not None and object.who() == "Food":
                self.addFood(object.foodHere)
            self.spacesYX[self.cleanCor(y)][self.cleanCor(x)] = object
        elif self.playerSpaceYX((x,y)).who() == "Food":
            if object is not None and object.who() == "Food":
                self.addFood(object.foodHere)
                self.playerSpaceYX((x,y)).addFood()
            elif object.who() == "Den":
                self.removeFood(self.playerSpaceYX((x,y)).foodHere)
                self.spacesYX[self.cleanCor(y)][self.cleanCor(x)] = object
        elif self.playerSpaceYX((x,y)).who() == "Den":
            if object is not None and object.who() == "Food":
                self.addFood(object.foodHere)
                self.playerSpaceYX((x,y)).depositFood(1)
        
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
        
    def playerSpaceYX(self, location):
        x,y = location
        return self.spacesYX[self.cleanCor(y)][self.cleanCor(x)]
    
    def removeObjectXY(self, location):
        x,y = location
        object = self.playerSpaceYX((x,y))
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

