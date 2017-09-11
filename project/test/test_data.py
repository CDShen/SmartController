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


def updateQValue(i):
	ScorePathDic = {'score': None, 'orgPath': None, 'FPPath':None, 'qscore':None}
	ScorePathDic['score'] = i
	ScorePathDic['orgPath'] = i
	ScorePathDic['FPPath'] = i
	ScorePathDic['qscore'] = i
	return ScorePathDic

ScorePathDicLst = []
for k in range(1,3):
	ScorePathDicLst.append(updateQValue(k))


print (ScorePathDicLst)