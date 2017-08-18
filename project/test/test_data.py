from math import *
import copy

class BaseData:
	_fields = []
	def __init__(self, *args):
		if (len(args) != len(self._fields)):
			raise TypeError('Expected {0} arguments'.format(len(self._fields)))
		for name, value in zip(self._fields, args):
			setattr(self, name, value)

class FixPnt(BaseData):
	_fields = ['x','y']


class RoadData(BaseData):
	_fields = ['name', 'vFixpnt']



stRoadData = RoadData('a',[])

stRoadData.vFixpnt.append(FixPnt(1,1))
stRoadData.vFixpnt.append(FixPnt(2,1))
stRoadData.vFixpnt.append(FixPnt(3,1))
stRoadData.vFixpnt.append(FixPnt(4,1))




#for j in len(stRoadData.vFixpnt):
#	print (stRoadData.vFixpnt[j].x)

a = [3,2,1,5,6]
print (max(a), min(a))