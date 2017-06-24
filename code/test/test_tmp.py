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


a = [1,2,3]
b = [2,3]

a.append(b)
print (a)




