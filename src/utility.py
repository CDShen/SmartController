"""
通用函数
目前有算出过点时间和判断是否和计划集合有冲突

"""

print (__doc__)

from math import *
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

	# brief:解决冲突并返回冲突后的路径
	# curFPPathData:[in] 当前计划滑行路线
	# conFPPathData:[in] 冲突滑行路线
	# ConflictData:[in] 冲突数据
	# newPath:[out] 解决后新的滑行路线
	@classmethod
	def resolveConflict(cls, curFPPathData, conFPPathData ,ConflictData, newPath):
		iConFixID = ConflictData.iConflictFixID
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

	@classmethod
	def isInsect(cls, num1Start, num1End, num2Start, num2End):
		if num2End < num1Start or num2Start > num1End:
			return  False
		else:
			return  True
