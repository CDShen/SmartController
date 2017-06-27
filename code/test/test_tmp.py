from math import *
import copy

#
#
class A(object):
    aLst = None

    @classmethod
    def getData(cls):
        return A.aLst

def clearLst(data):
    data = []
A.aLst = [1,2,3]
clearLst(A.aLst)

print (A.aLst)
#






