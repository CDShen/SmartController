"""
brief 1、滑行路线和地图节点的更新

滑行地图结构体类型例子
taxiPathMap = {iNodeID:[NodeFlightPlanData]}
"""
from ..public.baseDataDef import BaseData
from ..public.dataManage import DataManager
from .flightPlan import FlightPlan
from math import *
from .utility import MathUtilityTool


class NodeFlightPlanData(BaseData):
	_fields = ['iFlightPlanID', 'iRealPassTime']


##地图滑行节点类
class TaxiMap(object):
	def __init__(self, pDataManager):
		self.taxiNodeDic = {} ## 格式{id:[adjId....], ....}
		self.taxiPathDic = {} ## 格式{id:[NodeFlightPlanData...]}
		self.pDataManager = pDataManager

	##brief 初始化基础地图数据
	def initMapData(self):
		pass
	def delFlightPlanPath(self, pFlightPlan):
		stFlightPlanData = pFlightPlan.getFlightPlanData()
		stFPPathData = pFlightPlan.getFlightPlanPath()
		for i in self.taxiPathDic:
			delData = []
			for j in range(len(self.taxiPathDic.get(i))):
				stNodeFlightPlanData = self.taxiPathDic.get(i)[j]
				if stNodeFlightPlanData.iFlightPlanID == stFlightPlanData.iID:
					delData.append(j)
			for j in delData:
				self.taxiPathDic.get(i).remove(delData[j])



	##brief 添加一个飞行计划
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



	##brief 判断当前路线是否有冲突
	##ConflictData[out] 返回冲突数据
	##1、如果当前冲突是当前航班优先，则不认为有冲突
	def isConflict(self, pFlightPlan, PathData, ConflictData):
		bConflict = False
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
					for k in range(len(TmpNodeFlightPlanDataLst)):
						iSecondTime = TmpNodeFlightPlanDataLst[k][0].iRealPassTime
						iSecondTimeNext = TmpNodeFlightPlanDataLst[k][1].iRealPassTime
						if MathUtilityTool.isInsect(iFirstTime, iFirstTimeNext, iSecondTime, iSecondTimeNext):
							##有冲突
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
							##有冲突
							pass














