from const import ENVIORN_DIM

class Environment:
    def __init__(self):
        self.spacesYX = []
    
    def preBuild(self, locationAndObject):
        None
    
    def buildEnvironment(self):
        for y in range(ENVIORN_DIM):
            newRow = []
            for x in range(ENVIORN_DIM):
                newRow.append(None)
            self.spacesYX.append(newRow)
            
    def inputObjectXY(self, location, object):
        x,y = location
        self.spacesYX[self.cleanCor(y)][self.cleanCor(x)] = object
        
    def cleanCor(num):
        if num > ENVIORN_DIM:
            clean = (num - ENVIORN_DIM)
        elif num < 0:
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
        
    def checkSpaceXY(self, location):
        x,y = location
        return self.spacesYX[self.cleanCor(y)][self.cleanCor(x)]
    
    def removeObjectXY(self, location):
        x,y = location
        self.spacesYX[self.cleanCor(y)][self.cleanCor(x)] = None
    
class FoodContainer:
    def __init__(self, food=0):
        self.foodHere = food
    
    def addFood(self):
        self.foodHere += 1
    
    def who():
        return "Food"
    
    def takeFood(self):
        if self.foodHere <= 0:
            return False
        else:
            self.foodHere -= 1
            return True
        
class Den:
    def __init__(self, location):
        self.locationXY = location
        self.foodStored = 0
    
    def who():
        return "Den"
    
    def depositFood(self, food):
        self.foodStored += food
        
    def isfeed(self):
        if self.foodStored > 0:
            return True
        else:
            return False

