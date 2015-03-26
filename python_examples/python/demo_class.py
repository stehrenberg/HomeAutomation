# python class
# see also https://docs.python.org/2/tutorial/classes.html
from __future__ import print_function, division
from time import strftime

class Dog():
    """class dog as a base class"""
    def __init__(self, p_printout=False):
        self.color = "undefined" # attributes starting with self. can be accessed within class methods and from outside the object
        self.height = None
        self.numberOfLegs = 4
        self.printout = p_printout
        if self.printout:
            now = strftime("%H:%M:%S") # local variables are valid only within the context of the function (__init__ in this case)
            print("method Dog.__init__() called at time", now)
    
    def SetColor(self, p_color):
        if type(p_color) == str:
            self.color = p_color
        else:
            raise ValueError
    
    def GetColor(self):
        return self.color
    
    def GetHeight(self):
        return self.height
    
    def __lt__(self, other): # implementation of operator '<' for dogs
        if self.height < other.height:
            return True
        else:
            return False


class Poodle(Dog): # inheritance: base class name must be in current scope
    """class poodle as a sub-class"""
    def __init__(self, p_height, p_color, p_printout=False):
        Dog.__init__(self, p_printout) # calling __init__ function of base class Dog
        self.height = p_height # access to attribute of base class Dog
        self.SetColor(p_color) # calling method of base class Dog
        self.picture = bytearray(2000000) # new attribute in class Poodle: allocation of memory for a picture
    
    def Accident(self): # definition of new method for class Poodle
        if self.printout:
            print("an accident happened!!")
        self.numberOfLegs -= 1 # access to attribute of base class Dog
        
    def __del__(self):
        # for freeing resources, closing sockets, ...
        del self.picture
        if self.printout:
            print("function Poodle.__del__() has been called")
