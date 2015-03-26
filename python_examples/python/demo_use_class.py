from __future__ import print_function, division
from demo_class import Dog, Poodle

# using the help function
help(Dog)
print("---------------------------------------------")

# using class Dog:
MyDog = Dog(True) # we want to see the printouts
MyDog.SetColor("brown")
print("Color of my dog:", MyDog.GetColor())
Dog.SetColor(MyDog, "white") # alternative syntax for method calling: method parameter self = object MyDog
print("Color of my dog:", MyDog.color)
# accessing MyDog.now would cause an error
print("---------------------------------------------")

# using class Poodle:        
MyPoodle = Poodle(50, "black", True)
if isinstance(MyPoodle, Dog): # test whether MyPoodle is also an instance of class Dog
    print("MyPoodle is a Dog")
print("Height of my poodle is", MyPoodle.GetHeight())
print("Color of my poodle is", MyPoodle.GetColor())
print("My poodle has {0} legs".format(MyPoodle.numberOfLegs))
print("My poodle has {0.numberOfLegs} legs".format(MyPoodle)) # alternative syntax of .format with objects
MyPoodle.Accident()
print("My poodle has {0} legs left".format(MyPoodle.numberOfLegs))

MyOtherPoodle = Poodle(45, "red")
if MyOtherPoodle < MyPoodle: # using the operator < (method __lt__) of class Dog
    print("the other poodle is smaller")


