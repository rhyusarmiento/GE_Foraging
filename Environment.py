from const import ENVIORN_DIM

class Environment:
    def __init__(self):
        self.spacesYX = []
        self.numFood = 0
        
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
    
    def buildEnvironment(self):
        for y in range(ENVIORN_DIM):
            newRow = []
            for x in range(ENVIORN_DIM):
                newRow.append(None)
            self.spacesYX.append(newRow)
            
    def addFood(self, food):
        self.numFood += food
            
    def removeFood(self, food):
        self.numFood -= food
            
    def inputObjectXY(self, location, object):
        x,y = location
        if self.checkSpaceXY((x,y)) is None:
            if object is not None and object.who() == "Food":
                self.addFood(object.foodHere)
            self.spacesYX[self.cleanCor(y)][self.cleanCor(x)] = object
        elif self.checkSpaceXY((x,y)).who() == "Food":
            if object is not None and object.who() == "Food":
                self.addFood(object.foodHere)
                self.checkSpaceXY((x,y)).addFood()
            elif object.who() == "Den":
                self.removeFood(self.checkSpaceXY((x,y)).foodHere)
                self.spacesYX[self.cleanCor(y)][self.cleanCor(x)] = object
        elif self.checkSpaceXY((x,y)).who() == "Den":
            if object is not None and object.who() == "Food":
                self.addFood(object.foodHere)
                self.checkSpaceXY((x,y)).depositFood(1)
        
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
        
    def checkSpaceXY(self, location):
        x,y = location
        return self.spacesYX[self.cleanCor(y)][self.cleanCor(x)]
    
    def removeObjectXY(self, location):
        x,y = location
        object = self.checkSpaceXY((x,y))
        if object is not None and object.who() == "Food":
            self.removeFood(object.foodHere)
            self.spacesYX[self.cleanCor(y)][self.cleanCor(x)] = None
    
class FoodContainer:
    def __init__(self, food=1):
        self.foodHere = food
    
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

