# python exception
# see also http://www.tutorialspoint.com/python/python_exceptions.htm
from __future__ import print_function, division
from time import strftime


l = [4,7,5]  # list with 3 entries
index = 3    # l[index] will raise an exception if index > 2

# handling predefined exceptions
try:
    l[index] = 10
except IndexError, Argument: # KeyError, NameError, ValueError, IOError, ZeroDivisionError, ...
#except Exception, Argument: # handling any exception
    print("IndexError:", Argument) # Argument depends on the type of exception
else:
    print("this block will be executed if there is no exception")
finally:
    print("this block will be executed in any case")


# raising exceptions
# defining a function that raises an exception
def insertList(p_list, p_index, p_value):
    if p_index > len(p_list)-1:
        raise IndexError("index too high!!")
    else:
        p_list[p_index] = p_value

# using the function insertList()
try:
    insertList(l,index,10)
except IndexError, Argument:
    print("IndexError:", Argument)
else:
    print(l)
    

# defining own exceptions
class MyException(Exception): # base class Exception
    def __init__(self,description):
        self.expr = description
    def __str__(self): # defines how to convert the description to a string
        now = strftime("%H:%M:%S")
        return str(self.expr) + " actual time is " + now
    
# using MyException
try:
    if index > len(l)-1:
        raise MyException("index too high!!")
    else:
        l[index] = 11
except MyException, Argument:
    print("MyException:", Argument)
else:
    print(l)
