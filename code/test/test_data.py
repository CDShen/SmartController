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





class A(object):
	def __init__(self, name):
		self.name = name
	def getName(self):
		return  self.name


class B(A):
	pass





