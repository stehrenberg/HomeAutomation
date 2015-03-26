# python function
# see also http://www.tutorialspoint.com/python/python_functions.htm
from __future__ import print_function, division

def SayHello(p_name):
    """This is the documentation string of the function.
    The function prints 'Hello p_name!'
    There is no return value."""
    print("Hello ", p_name, "!", sep='')
    return # not really necessary but recommended

help(SayHello)
SayHello("Hubert")
print("------------------------------------------------------")


# numbers, strings and tuples are immutable arguments and passed to the function by copy
def ChangeNumber(n): 
    """The argument n will be left unchanged outside the function"""
    n = n + 1
    return n

my_n = 100
new_n = ChangeNumber(my_n)
print("value of my_n after calling ChangeNumber():", my_n)
print("return value of ChangeNumber():", new_n)


# function arguments that are mutable are passed by reference (lists, dictionaries, objects) !!
# note: the following function definition is considered bad style
def ChangeList(l): 
    """The argument l (as a list) will be changed also outside the function.
    This is called a side-effect of the function call."""
    l.append(33) 
    return

my_list = [1,2,3]
ChangeList(my_list)
print("value of my_list after calling ChangeList():", my_list)
print("------------------------------------------------------")


# function arguments with default values
def SumUpNumbers(n, start=1, step=1):
    """Demonstration of optional arguments with default values."""
    s = 0
    i = start
    end = start + n*step
    while i < end:
        s = s + i
        i += step
    return s

s = SumUpNumbers(100)
print("sum of 100 integers starting from 1 is", s)
s = SumUpNumbers(100, 100)
print("sum of 100 integers starting from 100 is", s)
s = SumUpNumbers(100, step=2)
print("sum of 100 integers starting from 1 and with step 2 is", s)
s = SumUpNumbers(100, 200, 2)
print("sum of 100 integers starting from 200 and with step 2 is", s)
s = SumUpNumbers(100, step=2, start=200)
print("sum of 100 integers starting from 200 and with step 2 is", s)
print("------------------------------------------------------")


# variable length arguments
# the list of variable length must follow the mandatory arguments
def PrintNumbers(arg1, *argv): # *argv is a list, **argv is a dict
    """Demonstration of vaiable length arguments."""
    print(arg1) # mandatory argument
    for a in argv:
        print(a)
    print("number of variable arguments was:", len(argv))        
    return

PrintNumbers(10)
PrintNumbers(10,20,30,40)




