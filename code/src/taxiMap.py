"""
brief 1、滑行路线和地图节点的更新 
      2、负责有不需要Q函数的冲突解决 
      3、负责不需要冲突解决的飞行计划滑行更新

滑行地图结构体类型例子
taxiPathMap = {iNodeID:[NodeFlightPlanData]}
"""

from ..public.baseDataDef import BaseData
from ..public.dataManage import DataManager
from .flightPlan import FlightPlan
from ..public.scenarioDataObj import *
from ..public.dataObj import *
from .utility import *

from math import *
from .utility import MathUtilityTool
from ..public.dataObj import *
from ..public.publicParaDef import PublicParaDef


class NodeFlightPlanData(BaseData):
	_fields = ['iFlightPlanID', 'iRealPassTime']


##地图滑行节点类
class TaxiMap(object):
	def __init__(self, pFlightPlanMgr, pDataManager):
		self.taxiNodeDic = {} ## 每个节点的相邻节点。格式{id:[adjId....], ....}
		self.taxiPathDic = {} ## 每个节点的滑行数据。格式{id:[NodeFlightPlanData...],....}
		self.pDataManager = pDataManager
		self.pFlightPlanMgr = pFlightPlanMgr
		self.iResolveFligtPlanID = -1.0 ##内部可以解决冲突的飞行计划ID
		self.newFPPathData = None   ##内部可以解决从图的飞行计划新滑行路径

	def clearResolveFlightPlanData(self):
		self.iResolveFligtPlanID = -1.0
		self.newFPPathData = None
	def getResolveFlightPlanData(self):
		return  self.iResolveFligtPlanID, self.newFPPathData

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
				self.taxiPathDic.setdefault(stFPPassPntData.iFixID, [stNodeFlightPlanData])
			else:
				self.taxiPathDic.get(stFPPassPntData.iFixID).append(stNodeFlightPlanData)

	##返回相邻节点lst
	def getAdjNode(self, iFixPntID):
		return  self.taxiNodeDic.get(iFixPntID)
	##返回节点飞机lst
	def getNodePassPnt(self, iFixPntID):
		return  self.taxiPathDic.get(iFixPntID)

	##判断是否需要Q函数解决冲突
	def _judgeNeedQFunResolveCon(self, pFlightPlan, PathData ,pConFlightPlan, ConflictData):
		eCurFlightPlanType = pFlightPlan.getFlightType()
		eConFlightPlanType = pConFlightPlan.getFlightType()
		iFirstPassTime = ConflictData.iFirstPassTime
		iSecondPassTime = ConflictData.iSecondPassTime
		eConFixType = ConflictData.efixPntType
		bIsFuturePlan = pConFlightPlan.isFutureFlightPlan()
		iStartTime = pFlightPlan.getFlightPlanStartTime()

		##将PathData数据转化为FPPathData
		stFPPathData = FPPathData(PathData.iPathID, [])
		for i in range(len(PathData.vPassPntData)):
			stFixPntData = self.pDataManager.getFixPointByID(PathData.vPassPntData[i].iFixID)
			stFPPassPntData = FPPassPntData(PathData.vPassPntData[i].iFixID, iStartTime + PathData.vPassPntData.iRelaPassTime, \
			                                stFixPntData.x, stFixPntData.y, ENUM_PASSPNT_TYPE.E_PASSPNT_NORMAL)
			stFPPathData.vFPPassPntData.append(stFPPassPntData)


		if eCurFlightPlanType == eConFlightPlanType or\
			(eCurFlightPlanType != eConFlightPlanType and eConFixType.value == E_FIXPOINT_CONF_TYPE.E_FIXPOINT_CONF_FIFS):

			if iFirstPassTime > iSecondPassTime:
				##需要Q函数处理
				return E_RESOLVE_TYPE.E_RESOLVE_QFUN
			else:
				if bIsFuturePlan == True:
					##不需要处理
					return E_RESOLVE_TYPE.E_RESOLVE_NONE
				else:
					##调用公共函数解决冲突
					newPath = None
					UtilityTool.resolveConflict(stFPPathData, pConFlightPlan.getFlightPlanPath(), ConflictData, newPath)
					self.iResolveFligtPlanID = pConFlightPlan.getFlightPlanID()
					self.newFPPathData = newPath
					return E_RESOLVE_TYPE.E_RESOLVE_INNER

		elif eCurFlightPlanType != eConFlightPlanType and eCurFlightPlanType.value == eConFixType.value:
			if bIsFuturePlan == True:
				##不需要处理
				return E_RESOLVE_TYPE.E_RESOLVE_NONE
			else:
				##调用公共函数解决冲突
				newPath = None
				UtilityTool.resolveConflict(stFPPathData, pConFlightPlan.getFlightPlanPath(), ConflictData, newPath)
				self.iResolveFligtPlanID = pConFlightPlan.getFlightPlanID()
				self.newFPPathData = newPath
				return E_RESOLVE_TYPE.E_RESOLVE_INNER

		elif eCurFlightPlanType != eConFlightPlanType and eConFlightPlanType.value == eConFixType.value:
			##需要Q函数处理
			return E_RESOLVE_TYPE.E_RESOLVE_QFUN




	##brief 判断当前路线是否有冲突，只返回需要用Q函数需要解决的冲突
	##pFlightPlan[in] 当前飞行计划
	##PathData[in]  当前滑行数据
	##eResolveType[out] 解决冲突类型
	##ConflictData[out] 冲突数据
	##1、如果当前冲突是当前航班优先，则不认为有冲突
	def calConflictType(self, pFlightPlan, PathData):
		stConflictData = None
		eResolveType = None

		iCountNum = 0
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
						if MathUtilityTool.isInsect(iFirstTime, iFirstTimeNext, iSecondTime, iSecondTimeNext):
							iConFlightPlanID = TmpNodeFlightPlanDataLst[k][0].iFlightPlanID
							pConFlightPlan = self.pFlightPlanMgr.getFlightPlanData(iConFlightPlanID)
							eFixPntType = self.pDataManager.getFixPntConType(stNextPassPntData.iFixID)
							iCurPathID = PathData.iPathID
							iConPathID = pConFlightPlan.getFlightPlanPath().iPathID

							iFirstPassTime = iFirstTimeNext
							iSecondPassTime = iSecondTime
							iCountNum+=1
							if iCountNum == 2:
								##添加日志
								pass
							stConflictData = ConflictData(pFlightPlan.getFlightPlanID(),iConFlightPlanID,\
							E_CONFLICT_TYPE.E_CONFLICT_CROSS,eFixPntType ,stNextPassPntData.iFixID,iCurPathID, \
							iConPathID, iFirstPassTime, iSecondPassTime  )
							##有冲突，继续判断是否需要Q函数解决
							return  self._judgeNeedQFunResolveCon(pFlightPlan, PathData,\
							        pConFlightPlan,stConflictData), stConflictData




					pass
				##如果后续节点不相等
				else: ##  AdjNodeLst[j] == stPassPntData.iFixID:
					AdjNodeFlightPlanDataLst = self.getNodePassPnt(AdjNodeLst[j])
					TmpNodeFlightPlanDataLst = []
					for k in range(len(AdjNodeFlightPlanDataLst)):
						for m in range(len(NodeFlightPlanDataLst)):
							if NodeFlightPlanDataLst[m].iFlightPlanID == AdjNodeFlightPlanDataLst[k].iFlightPlanID:
								TmpNodeFlightPlanDataLst.append(AdjNodeFlightPlanDataLst[k])

					##比较
					for k in range(len(TmpNodeFlightPlanDataLst)):
						iPassTime = iStartTime + stNextPassPntData.iRelaPassTime
						if fabs(iPassTime - TmpNodeFlightPlanDataLst.iRealPassTime) < PublicParaDef.iConFlictTimeThread:
							##有冲突，继续判断是否需要Q函数解决
							pass
