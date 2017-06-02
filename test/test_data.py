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


vFixpnt = []
i = 0
i += 1
vFixpnt.append(FixPnt(i,i))
i += 1
vFixpnt.append(FixPnt(i,i))
i += 1
vFixpnt.append(FixPnt(i,i))
i += 1
vFixpnt.append(FixPnt(i,i))
i += 1
vFixpnt.append(FixPnt(i,i))
stRaodData = RoadData('road1', vFixpnt)
stRaodData = RoadData('road1', vFixpnt)
stRaodDataMap = {}
stRaodDataMap.setdefault(1,RoadData('road1', vFixpnt))
stRaodDataMap.setdefault(2,RoadData('road2', vFixpnt))
stRaodDataMap.setdefault(3,RoadData('road3', vFixpnt))

print (stRaodDataMap[1].name)

# print ('roadName = {0}'.format(stRaodData.name) )
# for j in range(len(stRaodData.vFixpnt)):
# 	print ('fixPntSeq = {0}, xVal = {1}'.format(j, stRaodData.vFixpnt[j].x))
