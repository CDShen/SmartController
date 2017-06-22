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

    def getData(self):
        return self



a =A()
b = B(a)

print(b.getData().data)



