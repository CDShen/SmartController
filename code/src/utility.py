"""
通用函数
目前有算出过点时间和判断是否和计划集合有冲突

"""

print (__doc__)

from math import *
from ..public.dataObj import *
from ..public.scenarioDataObj import CguPos
from ..public.dataManage import DataManager
import copy




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
	# warning
	@classmethod
	def resolveConflict(cls, curFPathData, conFPPathData ,ConflictData, newPath):
		iConFixID = ConflictData.iConflictFixID
		iFirstStartIndex = -1
		iSecondStartFixIDIndex = -1
		for i in range(len(curFPathData.vFPPassPntData)):
			if curFPathData.vFPPassPntData[i].iFixID == iConFixID:
				iFirstStartIndex = i

		for i in range(len(curFPathData.vFPPassPntData)):
			if conFPPathData.vFPPassPntData[i].iFixID == iConFixID:
				iSecondStartFixIDIndex = i

		##查找到最开始的公共冲突点
		j=1
		iFirstCommonStartIndex = -1
		iSecCommonStartIndex = -1
		for i in range(iFirstStartIndex+1, len(curFPathData.vFPPassPntData)):
			if iSecondStartFixIDIndex - j <= 0:
				break

			if curFPathData.vFPPassPntData[i].iFixID == conFPPathData.vFPPassPntData[iSecondStartFixIDIndex-j].iFixID:
				j+=1
				iFirstCommonStartIndex = i
				iSecCommonStartIndex = iSecondStartFixIDIndex-j
			else:
				break

		##获得公共节点的过点时间
		iCommonConPassPntTime = curFPathData.vFPPassPntData[iFirstCommonStartIndex].iRealPassTime
		iDiffTime = -1
		for i in range(len(conFPPathData.vFPPassPntData)):
			if i < iSecCommonStartIndex:
				newPath.vFPPassPntData.append(conFPPathData.vFPPassPntData[i])
				pass
			elif i == iSecCommonStartIndex:
				stFPPassPntData = conFPPathData.vFPPassPntData[i]
				iOrgTime = conFPPathData.vFPPassPntData[i].iRealPassTime
				iNewTime = iCommonConPassPntTime + 20
				iDiffTime = iNewTime - iOrgTime
				stFPPassPntData.iRealPassTime = iNewTime ##默认添加20s
				newPath.vFPPassPntData.append(conFPPathData.vFPPassPntData[i])
			else:
				stFPPassPntData = conFPPathData.vFPPassPntData[i]
				stFPPassPntData.iRealPassTime += iDiffTime

	# brief:解决冲突并返回冲突后的路径
	# iStartTime:[in] 当前计划滑行路线
	# FPPathData:[in] 冲突滑行路线
	# return iTotalTime返回滑行时间
	@classmethod
	def getTotalFPTaxiTime(cls, iStartTime,FPPathData):
		iTotalTime = 0
		for i in range(len(FPPathData.vFPPassPntData)):
			iTotalTime += FPPathData.vFPPassPntData[i].iRealPassTime - iStartTime
		return  iTotalTime

	def getTotalPathTaxiTime(cls,PathData):
		iTotalTime = 0
		for i in range(len(PathData.vPassPntData)):
			iTotalTime += PathData.vPassPntData[i].iRelaPassTime
		return  iTotalTime



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
