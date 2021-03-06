
"""
brief 场景内部数据
"""
from .baseDataDef import BaseData
from enum import Enum

###################场景内部数据
##########航班计划数据

#####飞行计划状态
class ENUM_FP_STATUS(Enum):
	E_STATUS_ACTIVE = 1  ##激活
	E_STATUS_FUTURE = 2  ##未来计划
	E_STATUS_FIN = 3 ##结束





#####飞行计划
##iID->飞行计划ID, 唯一
##strName->飞行计划呼号
##eFlightType->飞行计划类型 0：其他 1：进港 2：离港
##iTaxStartTime->飞机开始滑行时间
##iStartPosID->飞行计划起始固定点ID
##iEndPosID->飞行计划结束固定点ID
class FlightPlanData(BaseData):
	_fields = ['iID', 'strName', 'eFlightType','iTaxStartTime', 'iStartPosID', 'iEndPosID']

#####飞行计划集合
##vFlightPlan->飞行计划list
class FlightPlanSetData(BaseData):
	_fields = ['vFlightPlan']





##########计划滑行路径结果数据


##########过点类型枚举
class ENUM_PASSPNT_TYPE(Enum):
	E_PASSPNT_NORMAL =0 ##正常通过
	E_PASSPNT_SLOWDOWN = 1 ##减速
	E_PASSPNT_STOP = 2 ##停止



#####最终过点时间
##iFixID->固定点ID
##iRealPassTime->最终绝对滑行时间，包含起始点和终止点
##x->x坐标
##y->y坐标
##ePassPntType->过点的动作 0:正常通过 1:停止通过 2：减速通过
class FPPassPntData(BaseData):
	_fields = ['iFixID', 'iRealPassTime', 'x', 'y','ePassPntType']

#####最终滑行路径
##iPathID->滑行路径ID，如果已经存在使用次数+1，如果不存在需要新生成
##vFPPassPntData->最终过点时间list, list顺序即滑行序号
class FPPathData(BaseData):
	_fields = ['iPathID', 'vFPPassPntData']

#####最终飞行计划计划滑行路线结果
##FlightPlanData->飞行计划数据
##FPPathData->滑行结果
class FlightPlanPathData(BaseData):
	_fields = ['FlightPlanData', 'FPPathData']



####冲突结果
##iCurFPID->当前飞行计划ID
##iConfFPID->冲突飞行计划ID
##eConfType->冲突类型  1：对头冲突 2：交叉冲突
##efixPntType->冲突固定点类型
##iConflictFixID->冲突固定点ID
##iCurPathID->当前计划的冲突路线ID
##iConPathID->冲突计划的滑行路线ID
##iFirstPassTime->当前计划过冲突点时间
##iSecOndPassTime->冲突计划过冲突点时间
class ConflictData(BaseData):
	_fields = ['iCurFPID', 'iConfFPID', 'eConfType', 'efixPntType', 'iConflictFixID',\
	           'iCurPathID', 'iConPathID', 'iFirstPassTime', 'iSecondPassTime']



##########其他数据
##x->X方向笛卡尔坐标
##y->Y方向笛卡尔坐标
class CguPos(BaseData):
	_fields = ['x','y']


class E_RESOLVE_TYPE(Enum):
	E_RESOLVE_NONE = 1  ##不需要处理冲突
	E_RESOLVE_INNER = 2  ##内部解决冲突
	E_RESOLVE_QFUN = 3  ##通过Q函数解决
	E_RESOLVE_ADDTIME = 4 ##冲突发生在起始点需要后续航班延后


##########已经解决的冲突对，在滑行时间过后解除冲突对
#iCurFPID->当前飞行计划ID
#iConFPID->冲突飞行计划ID
#iCurPathID->当前路径ID
#iConPathID->冲突路径iD
#iFirstPassTime->第一个过公共点时间
#iSecPassTime->第二个过公用点时间
class ResolveConflictData(BaseData):
	_fields = ['iCurFPID','iConFPID','iCurPathID', 'iConPathID', 'iFirstPassTime', 'iSecPassTime']






