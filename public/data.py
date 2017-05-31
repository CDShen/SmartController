from enum import Enum

class BaseData:
	_fields = []
	def __init__(self, *args):
		if (len(args) != len(self._fields)):
			raise TypeError('Expected {0} arguments'.format(len(self._fields))) 
		for name, value in zip(self._fields, args):
			setattr(self, name, value)

class Point(BaseData):
	_fields = ['x', 'y']



###########地图基础数据
##固定点
class FixPointData(BaseData):
	_fields = ['iID', 'strName', 'dX', 'dY','eConflictType']

##滑行道
class RoadData(BaseData):
	_fields = ['iId', 'strName', 'vFixPnt']

##机场
class AirportData(BaseData):
	_fields = ['iID', 'strName', 'vRoad']



###########航班数据
##飞行计划
class FlightPlan(BaseData):
	_fields = ['iID', 'strName', 'eFlightType','iTaxStartTime', 'iStartPosID', 'iEndPosID', 'bFinished']
#航班时刻表集合
class FlightSchedule(BaseData):
	_fields = ['vFlightPlan']


##########路线结果
class PassPntTime(BaseData):
	_fields = ['iFixPntID', 'iTime']


class PathOutData(BaseData):
	_fields = ['iFlightPlanID', 'vPassPntTime']	

class PathOutDataSet(BaseData):
	_fields = ['vPathOutData']

#########冲突对
class ConflictPair(BaseData):
	_fields = ['iFlightOneID', 'iFligtSecID', 'iConfFixID']


#航班过每个节点集合

#地图节点

##########Q学习数据
#状态S
class QState(BaseData):
	_fields = ['iStartFixID', 'iEndFixID', 'iConFixID', 'eConFixType',\
	'eConflictType' ,'eCurFlightType', 'eConFlightType','iPathFixSetID']

class QAction(BaseData):
	_fields = ['eActionType']

class QStateScore(BaseData):
	_fields = ['qState', 'qAction', 'dScore']


class QStateScoreSet(BaseData):
	_fields = ['vQStateScore']

class QStatePathSet(BaseData):
	_fields = ['iPathID', 'vFixPntID']




class ENUM_QACTION_TYPE(Enum):
	E_ACTION_STOP = 1
	E_ACTION_SLOWDOWN = 2


