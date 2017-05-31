class BaseData:
	_fields = []
	def __init__(self, *args):
		if (len(args) != len(self._fields)):
			raise TypeError('Expected {0} arguments'.format(len(self._fields))) 
		for name, value in zip(self._fields, args):
			setattr(self, name, value)

class FixPnt(BaseData):
	_fields = ['x',\
	 'y']


class RoadData(BaseData):
	_fields = ['name', 'vFixpnt']

a = []
a.append(FixPnt(1,2))
a.append(FixPnt(2,3))

c = a[1].y
print (c)
# b = RoadData('road1', a)

for i in range(len(a)):
	print (a[i].x) 

class A(object):
	def __init__(self,data):
		self.data = data

	def getData(self):
		return self.data

	def doWork(self):
		return self.getData()

	def setData(self, num):
		self.data = num


a = A(10)
print (a.doWork())
print (id(a))

b = A(10)

print (id(b))
print (type(a))
print (b.doWork())
b.setData(50)
print (b.doWork())
print (a.doWork())


# print (b.name)
# print (b.vFixpnt)
# for i in len(b.vFixpnt):
# 	pass 
# 	# print (b.vFixpnt[i].x)




