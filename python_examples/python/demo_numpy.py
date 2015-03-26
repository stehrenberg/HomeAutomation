from __future__ import print_function, division
import numpy as np
from math import pi, sin
import time

v = np.array([1,2,3,4]) # vector creation from python list

M = np.array([[1,4,3,6], # matrix creation from python list (of lists)
              [7,5,9,0],
              [4,2,1,1],
              [9,9,7,8]])

print(np.shape(v))
print(np.shape(M))
print(np.ndim(M)) # number of dimensions of M
print("\n")

w = np.dot(M,v) # matrix - vector multiplication
print(w)
x = np.dot(v,w) # scalar product of two vectors
print(x)
print("\n")

r = M[3,:] # slicing: r is 4th row of M (no data are copied!)
print(r)
print("\n")

S = M[:2,1:3] # slicing: S is a sub-matrix of M
print(S)
print("\n")

R = M[1:2,:] # this is a matrix, not a vector !!
print(R)
print(np.shape(R))
print("\n")

N = 2*M # arithmetic operations with arrays
print(N)
print("\n")


M[0,1:] = [5,5,5] # changing values of an array
print(M)
print("\n")
print(N) # data of N remain unchanged
print("\n")

P = M.reshape(2,8) # reshaping: no data are copied! It is a new view on the same data of M
# P = M.reshape(3,3) would fail
print(P)
print(np.shape(P))
print("\n")

M[0,1:] = [0,0,0] # altering data of M will alter data of P
print(P)
print("\n")
print(N) # still the same values
print("\n")

M2 = np.vstack([M,v]) # adding a row at the bottom
print(M2)
print(np.shape(M2))
print("\n")

M3 = np.column_stack([M2,[5,5,5,5,5]]) # adding a column to the right
print(M3)
print(np.shape(M3))
print("\n")

B = M<5 # boolean operations an matrices
print(B) 
print("\n")

b = M[B] # b is a vector containing all elements of M that are < 5
print(M)
print("\n")
print(b)
print("\n")

M[M<5] = 0 # setting all elements of M that are <5 to 0
print(M)
print("\n")

# test performance of numpy array computations
N = 10000
start = time.clock()
x_val1 = np.linspace(0, 2*pi, N) # numpy linspace generates an array from start to end and with equal distances
sin_val1 = np.around(np.sin(x_val1),4) # numpy functions can operate on arrays (example: sin and around)
end = time.clock()
print("numpy computation time: {0} ms".format(1000*(end-start)))

# alternative computation
start = time.clock()
x_val2 = []
sin_val2 = []
step = 2*pi/(N-1)
for i in range(N):
    x_val2.append(i*step)
    sin_val2.append(round(sin(x_val2[i]),4))
end = time.clock()
print("for-loop computation time: {0} ms".format(1000*(end-start)))

print("sin_val1 == sin_val2 ?", np.all(sin_val1==sin_val2))


