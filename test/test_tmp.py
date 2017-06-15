import math
import copy


class A(object):
    def __init__(self):
        self.data = 1
    def getData(self):
        return  self.data

class B(object):
    def __init__(self, A):
         self.data = copy.deepcopy(A.data)

    def getData(self):
        return copy.deepcopy(self.data)
# print (len(a))


a = A()
a.data = [1,2,3]

b = B(a)

c = b.getData()

c[1] = 'xxx'


print(a.data)
print(b.data)
print(c)

print(id(a), id(b))

