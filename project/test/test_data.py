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



a = [1,2,3,[1,2],5]

a.remove(1)


print (100%1)


