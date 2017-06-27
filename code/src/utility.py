"""
通用函数
目前有算出过点时间和判断是否和计划集合有冲突

"""

print (__doc__)

from math import *
from ..public.dataObj import *
from ..public.scenarioDataObj import *
from ..public.dataManage import DataManager
import copy


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



class UtilityTool(object):
	dTheta = None
	pDataManager = None




	# brief:解决冲突并返回冲突后的路径，只考虑改变冲突路线的方式
	# curFPPathData:[in] 当前计划滑行路线
	# conFPPathData:[in] 冲突滑行路线
	# ConflictData:[in] 冲突数据
	# return newPath:[out] 解决后新的滑行路线
	# warning
	@classmethod
	def resolveConflict(cls, curFPathData, conFPPathData ,ConflictData):
		newPath = copy.deepcopy(conFPPathData)
		##清空lst
		newPath.vFPPassPntData = []
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
				newPath.vFPPassPntData.append(conFPPathData.vFPPassPntData[i])
		return newPath
	# brief:解决冲突并返回冲突后的路径滑行时间
	# iStartTime:[in] 当前开始滑行时间
	# FPPathData:[in] 冲突滑行路线
	# return 返回滑行时间
	@classmethod
	def getTotalFPTaxiTime(cls, iStartTime, FPPathData):
		return  FPPathData.vFPPassPntData[len(FPPathData.vFPPassPntData)-1].iRealPassTime - iStartTime

	# brief:计划滑行路径总时间
	# PathData:[in] 当前计划滑行路线
	# return 返回滑行时间
	@classmethod
	def getTotalPathTaxiTime(cls,PathData):
		return PathData.vPassPntData[len(PathData.vPassPntData)-1].iRelaPassTime

	@classmethod
	def getConflictType(cls, cguPos1_1,cguPos1_2, cguPos2_1, cguPos2_2):
		eConflictType = None
		vecPos1 = (cguPos1_2.x-cguPos1_1.x, cguPos1_2.y-cguPos1_1.y)
		vecPos2 = (cguPos2_2.x - cguPos2_1.x, cguPos2_2.y - cguPos2_1.y)
		vecPos1Mod = sqrt(pow(vecPos1.x,2)+pow(vecPos1.y,2))
		vecPos2Mod = sqrt(pow(vecPos2.x,2)+pow(vecPos2.y,2))

		val = (vecPos1.x * vecPos2.x + vecPos1.y * vecPos2.y)/(vecPos1Mod*vecPos2Mod)
		theta = (180 / pi * acos(val))
		if theta < 30.0 and theta > 0:
			eConflictType = E_CONFLICT_TYPE.E_CONFLICT_CONS
		elif theta <= 150.0 and theta >= 30.0:
			eConflictType = E_CONFLICT_TYPE.E_CONFLICT_CROSS
		else:
			eConflictType = E_CONFLICT_TYPE.E_CONFLICT_OPP

		return  eConflictType


	def transPathData2FPPathData(self, iStartTime, PathData):
		vstFPPassPntData = []
		for i in range(len(PathData.vPassPntData)):
			stFixPointData = self.pDataManager.getFixPointByID(PathData.vPassPntData[i].iFixID)
			stFPPassPntData = FPPassPntData(stFixPointData.iFixID,iStartTime + PathData.vPassPntData[i].iRelaPassTime,\
			                stFixPointData.dX, stFixPointData.dY,ENUM_PASSPNT_TYPE.E_PASSPNT_NORMAL)
			vstFPPassPntData.append(stFPPassPntData)

			stFPPathData = FPPathData(PathData.iPathID, vstFPPassPntData)
			return  stFPPathData




