from math import *
import copy


class CClass(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
#
#
class A(object):
    aLst = None
    @classmethod
    def getData(cls, Datalst):
        bLst = copy.deepcopy(Datalst)
        bLst.append(Datalst[4])

        bLst[5].y = 7

        print (Datalst[4].y)
        print (bLst[5].y)



a = 3
b = 4
print(3/4)



# Datalst.append(CClass(1,1))
# print (Datalst)
#

#print (A.aLst)
#






