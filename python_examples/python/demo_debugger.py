# python debugger
# see also https://docs.python.org/2/tutorial/classes.html
import pdb
pdb.set_trace() 

def afunction(n):
    s = 0
    for i in range(n):
        s += i
    return s

res = afunction(200)
print res
