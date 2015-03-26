# lists
# see also https://docs.python.org/2/tutorial/datastructures.html 
from __future__ import print_function, division

L1 = (1,2,3,4) # this is not a list, but a tuple!! (i.e., an immutable list)
L2 = [1,2,3,4]
L3 = ["a", "b", "c", "d", "e"]
L4 = [1, 2, "a", 3.141, (5,6), "a"] # types can be mixed up
L5 = [[1,2],[3,4]] # a matrix is a list of lists
L6 = range(20) # standard method to generate lists of number sequences

print("general properties and operations")
print("type of L1 is", type(L1), "length is", len(L1))
print("type of L2 is", type(L2), "length is", len(L2))
print("type of L3 is", type(L3), "length is", len(L3))
print("type of L4 is", type(L4), "length is", len(L4))
print("type of L5 is", type(L5), "length is", len(L5))
print("L6:", L6)
print("L2 + L3:", L2 + L3)
print("3*L2:", 3*L2)


print("\n"+"accessing elements of a list (and tuples)")
print("L1[1]:", L1[1])
print("L2[0]:", L2[0])
print("L3[-1]:", L3[-1])
print("L5[0][1]:", L5[0][1])
# slicing examples:
print("L2[1:3]:", L2[1:3])
print("L3[1:-1]:", L3[1:-1])
print("L3[2:]:", L3[2:])
print("L6[4:17:3]:", L6[4:17:3]) # step 3

L2[:2] = [5,6] # would fail with tuples
print("altered L2:", L2)


print("\n"+"list methods")
L4.append(15)
print("result of L4.append(15):", L4)
L4.pop()
print("result of L4.pop():", L4) # removes last element
L4.insert(2,33)
print("result of L4.insert(2,33):", L4)
print("L4.count('a'):", L4.count('a'))
L4.remove('a')
print("result of L4.remove('a'):", L4) # first occurrence is removed
L2.sort()
print("result of L2.sort():", L2)
L2.reverse()
print("result of L2.reverse():", L2)



print("\n"+"iterating through a list")
n = 100
s = 0
for i in range(n): 
    s += i         # s = 0+1+2+3+4+....+(n-1)
if s == (n-1)*n/2:
    print("C. F. Gauss was right. s=", s)


print("\n"+"enumeration and iterating through a list")
for i,l in enumerate(L3):
    print(i,l)



