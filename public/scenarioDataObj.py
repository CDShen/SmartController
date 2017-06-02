
"""
brief 场景内部数据
"""
from baseDataDef import BaseData


###########航班数据
##飞行计划
class FlightPlanData(BaseData):
	_fields = ['iID', 'strName', 'eFlightType','iTaxStartTime', 'iStartPosID', 'iEndPosID', 'bFinished']
#航班时刻表集合
class FlightScheduleData(BaseData):
	_fields = ['vFlightPlan']


# brief:起始-终点路径点集合，包含了固定点和其默认过点时间
class PlanPathData(BaseData):
	_fields = ['iStartPosID', 'iEndPosID', 'vPassPntTime']


##########路线结果
class PassPntTimeData(BaseData):
	_fields = ['iFixPntID', 'iTime']


class PathOutData(BaseData):
	_fields = ['iFlightPlanID', 'vPassPntTime']	

class PathOutDataSet(BaseData):
	_fields = ['vPathOutData']

#########冲突对
class ConflictDataPair(BaseData):
	_fields = ['iFlightOneID', 'iFligtSecID', 'iConfFixID']


#航班过每个节点集合

#地图节点

##########Q学习数据
#状态S
class QStateData(BaseData):
	_fields = ['iStartFixID', 'iEndFixID', 'iConFixID', 'eConFixType',\
	'eConflictType' ,'eCurFlightType', 'eConFlightType','iPathFixSetID']

class QActionData(BaseData):
	_fields = ['eActionType']

class QStateScoreData(BaseData):
	_fields = ['qState', 'qAction', 'dScore']


class QStateScoreDataSet(BaseData):
	_fields = ['vQStateScore']

class QStatePathDataSet(BaseData):
	_fields = ['iPathID', 'vFixPntID']





