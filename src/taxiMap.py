"""
brief 1、滑行路线和地图节点的更新 2、负责有部分冲突的解决

滑行地图结构体类型例子
taxiPathMap = {iNodeID:[NodeFlightPlanData]}
"""
from ..public.baseDataDef import BaseData
from ..public.dataManage import DataManager
from .flightPlan import FlightPlan
from .flightPlanMgr import FlightPlanMgr
from math import *
from .utility import MathUtilityTool
from ..public.dataObj import *


class NodeFlightPlanData(BaseData):
	_fields = ['iFlightPlanID', 'iRealPassTime']


##地图滑行节点类
class TaxiMap(object):
	def __init__(self, pFlightPlanMgr, pDataManager):
		self.taxiNodeDic = {} ## 每个节点的相邻节点。格式{id:[adjId....], ....}
		self.taxiPathDic = {} ## 每个节点的滑行数据。格式{id:[NodeFlightPlanData...],....}
		self.pDataManager = pDataManager
		self.pFlightPlanMgr = pFlightPlanMgr
	##brief 初始化基础地图数据
	def initMapData(self):
		pass
	def delFlightPlanPath(self, iFlightPlanID):
		for i in self.taxiPathDic:
			delData = []
			for j in range(len(self.taxiPathDic.get(i))):
				stNodeFlightPlanData = self.taxiPathDic.get(i)[j]
				if stNodeFlightPlanData.iFlightPlanID == iFlightPlanID:
					delData.append(j)
			for j in delData:
				self.taxiPathDic.get(i).remove(delData[j])


	##brief 添加一个飞行计划路径
	def addFlightPlanPath(self, pFlightPlan):
		stFlightPlanData = pFlightPlan.getFlightPlanData()
		stFPPathData = pFlightPlan.getFlightPlanPath()
		for i in range(len(stFPPathData.vFPPassPntData)):
			stFPPassPntData = stFPPathData.vFPPassPntData[i]

			stNodeFlightPlanData = NodeFlightPlanData(stFlightPlanData.iID, stFPPassPntData.iRealPassTime)
			if self.taxiPathDic.get(stFPPassPntData.iFixID) == None:
				self.taxiPathDic.setdefault(stFPPassPntData.iFixID,[stNodeFlightPlanData])
			else:
				self.taxiPathDic.get(stFPPassPntData.iFixID).append(stNodeFlightPlanData)

	##返回相邻节点lst
	def getAdjNode(self, iFixPntID):
		return  self.taxiNodeDic.get(iFixPntID)
	##返回节点飞机lst
	def getNodePassPnt(self, iFixPntID):
		return  self.taxiPathDic.get(iFixPntID)

	##判断是否需要Q函数解决冲突
	def judgeNeedQFunResolveCon(self, pFlightPlan, PathData ,pConFlightPlan, ConflictData, iFirstPassTime, iSecOndPassTime):
		eCurFlightPlanType = pFlightPlan.getFlightType()
		eConFlightPlanType = pConFlightPlan.getFlightType()
		eConFixType = ConflictData.efixPntType
		bIsFuturePlan = pConFlightPlan.isFutureFlightPlan()
		if eCurFlightPlanType == eConFlightPlanType or\
			(eCurFlightPlanType != eConFlightPlanType and eConFixType.value == E_FIXPOINT_CONF_TYPE.E_FIXPOINT_CONF_FIFS):

			if iFirstPassTime > iSecOndPassTime:
				##需要Q函数处理
				pass
			else:
				if bIsFuturePlan == True:
					##不需要处理
					pass
				else:
					##调用公共函数解决冲突
					pass

		elif eCurFlightPlanType != eConFlightPlanType and eCurFlightPlanType.value == eConFixType.value:
			if bIsFuturePlan == True:
				##不需要处理
				pass
			else:
				##调用公共函数解决冲突
				pass

		elif eCurFlightPlanType != eConFlightPlanType and eConFlightPlanType.value == eConFixType.value:
			##需要Q函数处理
			pass




	##brief 判断当前路线是否有冲突，只返回需要用Q函数需要解决的冲突
	##ConflictData[out] 返回冲突数据
	##1、如果当前冲突是当前航班优先，则不认为有冲突
	def isConflict(self, pFlightPlan, PathData,ConflictData):
		bConflict = False
		vConflictData = [] ##冲突集合，如果冲突集合超过2次，需要警告
		iStartTime = pFlightPlan.getFlightPlanStartTime()
		for i in range(len(PathData.vPassPntData)-1):
			stPassPntData = PathData.vPassPntData[i]
			stNextPassPntData = PathData.vPassPntData[i+1]
			NodeFlightPlanDataLst = self.getNodePassPnt(stNextPassPntData.iFixID)

			##找到相邻的节点，选取过点时间比较
			##如果这里超过1次冲突，必须告警
			##还有相同滑行节点没有考虑
			AdjNodeLst = self.getAdjNode(stNextPassPntData.iFixID)
			for j in range(len(AdjNodeLst)):
				##相反节点A->B 与 B->A
				if AdjNodeLst[j] == stPassPntData.iFixID:
					##AdjNodeFlightPlanDataLst:固定点的所有飞行计划和过点时间
					AdjNodeFlightPlanDataLst = self.getNodePassPnt(AdjNodeLst[j])
					TmpNodeFlightPlanDataLst = [] ## [[1,2], [1,2]]两个点都需要知道
					TmpNodeFlightPlanDataPair = []
					for k in range(len(AdjNodeFlightPlanDataLst)):
						for m in range(len(NodeFlightPlanDataLst)):
							if NodeFlightPlanDataLst[m].iFlightPlanID == AdjNodeFlightPlanDataLst[k].iFlightPlanID:
								#TmpNodeFlightPlanDataLst.append(AdjNodeFlightPlanDataLst[k])
								TmpNodeFlightPlanDataPair.append(NodeFlightPlanDataLst[m])
								TmpNodeFlightPlanDataPair.append(AdjNodeFlightPlanDataLst[k])
								TmpNodeFlightPlanDataLst.append(TmpNodeFlightPlanDataPair)

					iFirstTime = stPassPntData.iRelaPassTime + iStartTime
					iFirstTimeNext = stNextPassPntData.iRelaPassTime + iStartTime
					##冲突超过2个需要警告
					for k in range(len(TmpNodeFlightPlanDataLst)):
						iSecondTime = TmpNodeFlightPlanDataLst[k][0].iRealPassTime
						iSecondTimeNext = TmpNodeFlightPlanDataLst[k][1].iRealPassTime
						##不考虑顺向冲突
						if iSecondTime > iSecondTimeNext:
							break

						iConFlightPlanID = TmpNodeFlightPlanDataLst[k][0].iFlightPlanID
						eFixPntType = self.pDataManager.getFixPntConType(stNextPassPntData.iFixID)
						if MathUtilityTool.isInsect(iFirstTime, iFirstTimeNext, iSecondTime, iSecondTimeNext):
							##有冲突，继续判断是否需要Q函数解决
							pass


					pass
				##如果不相等
				else:
					AdjNodeFlightPlanDataLst = self.getNodePassPnt(AdjNodeLst[j])
					TmpNodeFlightPlanDataLst = []
					for k in range(len(AdjNodeFlightPlanDataLst)):
						for m in range(len(NodeFlightPlanDataLst)):
							if NodeFlightPlanDataLst[m].iFlightPlanID == AdjNodeFlightPlanDataLst[k].iFlightPlanID:
								TmpNodeFlightPlanDataLst.append(AdjNodeFlightPlanDataLst[k])

					##比较
					for k in range(len(TmpNodeFlightPlanDataLst)):
						iPassTime = iStartTime + stNextPassPntData.iRelaPassTime
						if fabs(iPassTime - TmpNodeFlightPlanDataLst.iRealPassTime) < 10:
							##有冲突，继续判断是否需要Q函数解决
							pass














