"""
通用函数
目前有算出过点时间和判断是否和计划集合有冲突

"""

print (__doc__)

from math import *
from ..public.data import *
from ..public.data import *
from ..public.scenarioDataObj import CguPos
from ..public.dataManage import DataManager




class UtilityTool(object):
	dTheta = None
	pDataManager = None

	# brief:输入当前的计划，返回历史使用概率最高滑行路径
	# FlightPlanData:[in] 未来N时刻的飞行计划数据
	# vPassPntTimeData:[out] 未来N时刻的飞行计划过点时间
	# return:无
	@classmethod
	def predict_pass_time(cls, FlightPlanData, FPPathData):
		pass

	# brief:输入当前的计划，确定否和现在计划集合有冲突，并返回冲突类型等其他信息
	# FlightPlanData:[in] 当前飞行计划
	# FPPathData:[in] 当前过点信息
	# FPPathDataSet:[out] 目前航班计划集合，计划完成了就不需要了
	# ConflictData:[out] 冲突航班对和具体信息
	# return: bool 是否有冲突
	@classmethod
	def isConflict(cls, FlightPlanData, FPPathData, FPPathDataSet ,ConflictData):
		pass


	# def resolveConflict(cls, eActionType, vPassPntData):
	# 	pass


class MathUtilityTool(object):
	@classmethod
	def Distance(cls, CguPos1,CguPos2):
		dis = sqrt(pow((CguPos1.x - CguPos2.x),2) +  pow((CguPos1.y - CguPos2.y),2))

	@classmethod
	def GetUnitVec(cls, CguPos1):
		dis = MathUtilityTool.Distance(CguPos1, CguPos(0,0))
		return CguPos(CguPos1.x/dis, CguPos1.y/dis)
