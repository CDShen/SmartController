from math import *
import copy

#
#
class A(object):
    def __init__(self):
        self.data = 1
    def getData(self):
        return  self.data
#
class B(object):
    def __init__(self, A):
         self.data = A.data

    def getData(self,d):
        # d = [1,2,3]
        b= d
        return b
    def changeData(self):
        data = self.data[3]
        data[0] = 7


a = A()
a.data = [1,2,3,[4,5]]

b = B(a)

print (b.data)
b.changeData()
print(b.data)





