# python dictionary
# see also https://docs.python.org/2/tutorial/datastructures.html#dictionaries
from __future__ import print_function, division
import json

dic = {"a": 1, "b": "text", "c": True, "d": [1,2,3], 15: "a"} # dictionary = unordered sequence of 'key: value' pairs

print("general properties")
print("number of elements in dic: ", len(dic))
print("type of dic is", type(dic))


print("\n"+"accessing elements of a dictionary")
print("dic['c']:", dic['c'])
print("dic['d'][1]:", dic['d'][1])
print("dic[15]:", dic[15])


print("\n"+"checking presence of elements")
if "x" in dic:
    print("x is in dic")
else:
    print("x is not in dic")


print("\n"+"adding new values to a dictionary")
dic['e'] = 15 # would not work with lists
print(dic)


print("\n"+"deleting values from a dictionary")
del dic['a']
print(dic)


print("\n"+"iterating over a dictionary")
for k in dic:
    print(k, dic[k])
print("-----------")
for k in dic.keys():
    print(k, dic[k])
print("-----------")
for v in dic.values():
    print(v)
print("-----------")
for i in dic.items():
    print(i)


print("\n"+"enumerating a dictionary and iteration")
for (i, k) in enumerate(dic):
    print(i, k, dic[k])


print("\n"+"json encoding of dictionary")
dic_string = json.dumps(dic)
print("dic_string: ", dic_string)
print("dic_string is", type(dic_string))
print("length is ", len(dic_string))


print("\n"+"create dictionary object through json decoding")
dic2 = json.loads('{"a": 1, "b": true, "c": [3,4,5], "d": "text", "15": "a"}') # last item as 15: "a" would not work, names required by json.loads
print("dic2 is", type(dic2))
print(dic2["d"])
if dic2["b"]:
    print(dic2["b"])
print(dic2["15"]) # dic2[15] would raise an exception
