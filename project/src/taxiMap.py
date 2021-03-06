"""
brief 1、滑行路线和地图节点的更新 
      2、负责有不需要Q函数的冲突解决 
      3、负责不需要冲突解决的飞行计划滑行更新

滑行地图结构体类型例子
taxiPathMap = {iNodeID:[NodeFlightPlanData]}
"""

from .utility import *
from ..public.config import ConfigReader
from ..public.dataObj import *
from ..public.scenarioDataObj import *

class NodeFlightPlanData(BaseData):
	_fields = ['iFlightPlanID', 'iRealPassTime', 'iFixPntID']


##地图滑行节点类
class TaxiMap(object):
	def __init__(self, pFlightPlanMgr, pDataManager):
		self.taxiNodeDic = {} ## 每个节点的相邻节点。格式{id:[adjId....], ....}
		self.taxiPathDic = {} ## 每个节点的滑行数据。格式{id:[NodeFlightPlanData...],....}
		self.pDataManager = pDataManager
		self.pFlightPlanMgr = pFlightPlanMgr
		self.iResolveFligtPlanID = -1 ##内部可以解决冲突的飞行计划ID
		self.newFPPathData = None   ##内部可以解决从图的飞行计划新滑行路径
		self.initData()
		self.ResolveData = None
	##创建基础数据
	def initData(self):
		self.initMapData()

	def clearResolveFlightPlanData(self):
		self.iResolveFligtPlanID = -1
		self.newFPPathData = None
		self.ResolveData = None
	def getResolveFlightPlanData(self):
		return  self.iResolveFligtPlanID, self.newFPPathData, self.ResolveData

	##brief 初始化基础地图数据
	def initMapData(self):
		self.taxiNodeDic = self._createAdjNodeDic()

	def delFlightPlanPath(self, iFlightPlanID):
		delDicLst = []
		for i in self.taxiPathDic:
			delData = []
			vNodeFlightPlanData = self.taxiPathDic.get(i)

			for j in range(len(vNodeFlightPlanData)):
				stNodeFlightPlanData = vNodeFlightPlanData[j]
				if stNodeFlightPlanData.iFlightPlanID == iFlightPlanID:
					delData.append(stNodeFlightPlanData)
			##只能移除值
			for j in range(len(delData)):
				vNodeFlightPlanData.remove(delData[j])

			if len(vNodeFlightPlanData) == 0:
				delDicLst.append(i)

		for i in range(len(delDicLst)):
			del self.taxiPathDic[delDicLst[i]]

	##brief 添加一个飞行计划路径
	def addFlightPlanPath(self, pFlightPlan):
		stFlightPlanData = pFlightPlan.getFlightPlanData()
		stFPPathData = pFlightPlan.getFlightPlanPath()
		for i in range(len(stFPPathData.vFPPassPntData)):
			stFPPassPntData = stFPPathData.vFPPassPntData[i]
			stNodeFlightPlanData = NodeFlightPlanData(stFlightPlanData.iID, stFPPassPntData.iRealPassTime, stFPPassPntData.iFixID)
			if self.taxiPathDic.get(stFPPassPntData.iFixID) == None:
				self.taxiPathDic.setdefault(stFPPassPntData.iFixID, [stNodeFlightPlanData])
			else:
				self.taxiPathDic.get(stFPPassPntData.iFixID).append(stNodeFlightPlanData)

	def _tryAddAdjNode(self, AdjNodeDic, NodeID, AdjNodeID):
		if AdjNodeDic.get(NodeID) == None:
			AdjNodeDic.setdefault(NodeID,[AdjNodeID])
		else:
			AdjNodeLst = AdjNodeDic.get(NodeID)
			bFInd = False
			for i in range(len(AdjNodeLst)):
				if AdjNodeLst[i] == AdjNodeID:
					bFInd = True
					break
			if bFInd == False:
				AdjNodeLst.append(AdjNodeID)


	def _createAdjNodeDic(self):
		AdjNodeDic = {}
		RoadDataDic =  self.pDataManager.getRoadDataDic()
		for i in RoadDataDic:
			vFixPnt = RoadDataDic.get(i).vFixPnt
			for j in range(len(vFixPnt)-1):
				stFixPntID = vFixPnt[j].iID
				stNextPntID = vFixPnt[j+1].iID
				self._tryAddAdjNode(AdjNodeDic, stFixPntID, stNextPntID)
				self._tryAddAdjNode(AdjNodeDic, stNextPntID, stFixPntID)
		return AdjNodeDic


	##设置所有节点的临接点
	def setAdjNodeDic(self, AdjNodeDic):
		self.taxiNodeDic = AdjNodeDic
	##返回相邻节点lst
	def _getAdjNode(self, iFixPntID):
		return  self.taxiNodeDic.get(iFixPntID)
	##返回节点飞机lst
	def _getNodePassPnt(self, iFixPntID):
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
		newPath = None

		##将PathData数据转化为FPPathData
		stFPPathData = UtilityTool.transPathData2FPPathData(iStartTime, PathData)

		##如果当前解决的冲突飞机已经有了解决冲突方案，则需要用Q函数解决
		##如果已经解决了冲突就直接使用，当成一个pair看待
		ConFlightPlanData = pConFlightPlan.getFlightPlanData()
		if self.pFlightPlanMgr.judgeIsAlreadyResolved(ConFlightPlanData.iID):
			return E_RESOLVE_TYPE.E_RESOLVE_QFUN
		else:
			if eCurFlightPlanType == eConFlightPlanType or\
				(eCurFlightPlanType != eConFlightPlanType and eConFixType == E_FIXPOINT_CONF_TYPE.E_FIXPOINT_CONF_FIFS):

				if iFirstPassTime > iSecondPassTime:
					##需要Q函数处理
					return E_RESOLVE_TYPE.E_RESOLVE_QFUN
				else:
					if bIsFuturePlan == True:
						##不需要处理
						return E_RESOLVE_TYPE.E_RESOLVE_NONE
					else:
						##调用公共函数解决冲突
						newPath ,iSecCommonStartIndex = UtilityTool.resolveConflict(stFPPathData, pConFlightPlan.getFlightPlanPath(), ConflictData)
						self.iResolveFligtPlanID = pConFlightPlan.getFlightPlanID()
						self.newFPPathData = newPath
						##打印日志
						if iSecCommonStartIndex >= 0:
							conPathData = pConFlightPlan.getFlightPlanPath()
							# 初始冲突点名称
							strCurPathID = ConflictData.iCurPathID
							strConPathID = ConflictData.iConPathID
							strFirstName = self.pDataManager.getFixPointByID(ConflictData.iConflictFixID).strName
							strFixName = self.pDataManager.getFixPointByID(conPathData.vFPPassPntData[iSecCommonStartIndex].iFixID).strName
							strCurCallsign = pFlightPlan.getCallsign()
							strConCallsign = pConFlightPlan.getCallsign()
							iCurFPID = pFlightPlan.getFlightPlanData().iID
							iConFPID = pConFlightPlan.getFlightPlanData().iID
							iSecondPassTime = newPath.vFPPassPntData[iSecCommonStartIndex].iRealPassTime
							self.ResolveData = ResolveConflictData(iCurFPID, iConFPID, strCurPathID, strConPathID,iSecondPassTime, iSecondPassTime)
							print('优先滑行时候冲突呼号对[{0},{1}]，冲突道路[{2},{3}]初始冲突点{4},冲突点{5}'.format(strCurCallsign, strConCallsign, strCurPathID, strConPathID,strFirstName,strFixName))
						return E_RESOLVE_TYPE.E_RESOLVE_INNER

			##当前冲突类型和固定点冲突类型值一致
			elif eCurFlightPlanType != eConFlightPlanType and eCurFlightPlanType.value == eConFixType.value:
				if bIsFuturePlan == True:
					##不需要处理
					return E_RESOLVE_TYPE.E_RESOLVE_NONE
				else:
					##调用公共函数解决冲突
					newPath, iSecCommonStartIndex = UtilityTool.resolveConflict(stFPPathData, pConFlightPlan.getFlightPlanPath(), ConflictData)
					self.iResolveFligtPlanID = pConFlightPlan.getFlightPlanID()
					self.newFPPathData = newPath
					#打印日志
					if iSecCommonStartIndex >= 0:
						conPathData = pConFlightPlan.getFlightPlanPath()
						# 初始冲突点名称
						strCurPathID = ConflictData.iCurPathID
						strConPathID = ConflictData.iConPathID
						strFirstName = self.pDataManager.getFixPointByID(ConflictData.iConflictFixID).strName
						strFixName = self.pDataManager.getFixPointByID(conPathData.vFPPassPntData[iSecCommonStartIndex].iFixID).strName
						strCurCallsign = pFlightPlan.getCallsign()
						strConCallsign = pConFlightPlan.getCallsign()
						iCurFPID = pFlightPlan.getFlightPlanData().iID
						iConFPID = pConFlightPlan.getFlightPlanData().iID
						iSecondPassTime = newPath.vFPPassPntData[iSecCommonStartIndex].iRealPassTime
						self.ResolveData = ResolveConflictData(iCurFPID, iConFPID, strCurPathID, strConPathID, iSecondPassTime, iSecondPassTime)
						print('优先滑行时候冲突呼号对[{0},{1}]，冲突道路[{2},{3}]初始冲突点{4},冲突点{5}'.format(strCurCallsign, strConCallsign, strCurPathID, strConPathID,strFirstName, strFixName))
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
	##remark 只能解决滑行过程中有一次冲突，现在是保证航班时间>滑行时间来保证只有一次冲突
	def calConflictType(self, pFlightPlan, PathData):
		stConflictData = None
		iCountNum = 0
		iStartTime = pFlightPlan.getFlightPlanStartTime()
		for i in range(len(PathData.vPassPntData)-1):
			stPassPntData = PathData.vPassPntData[i]
			stNextPassPntData = PathData.vPassPntData[i+1]
			NodeFlightPlanDataLst = self._getNodePassPnt(stNextPassPntData.iFixID)
			if NodeFlightPlanDataLst == None:
				continue

			##找到相邻的节点，选取过点时间比较
			##如果这里超过1次冲突，必须告警
			##还有相同滑行节点没有考虑
			##！！地面节点中没有自己的数据！！
			AdjNodeLst = self._getAdjNode(stNextPassPntData.iFixID)

			##首先处理有相反情况的,目前只处理一次
			for j in range(len(AdjNodeLst)):
				if AdjNodeLst[j] == stPassPntData.iFixID:
					##AdjNodeFlightPlanDataLst:固定点的所有飞行计划和过点时间
					AdjNodeFlightPlanDataLst = self._getNodePassPnt(AdjNodeLst[j])
					if AdjNodeFlightPlanDataLst == None:
						continue

					TmpNodeFlightPlanDataLst = []  ## [[1,2], [1,2]]两个点都需要知道

					for k in range(len(AdjNodeFlightPlanDataLst)):
						for m in range(len(NodeFlightPlanDataLst)):
							if NodeFlightPlanDataLst[m].iFlightPlanID == AdjNodeFlightPlanDataLst[k].iFlightPlanID:
								TmpNodeFlightPlanDataPair = []
								##有先后滑行顺序
								TmpNodeFlightPlanDataPair.append(NodeFlightPlanDataLst[m])
								TmpNodeFlightPlanDataPair.append(AdjNodeFlightPlanDataLst[k])
								TmpNodeFlightPlanDataLst.append(TmpNodeFlightPlanDataPair)

					iFirstTime = stPassPntData.iRelaPassTime + iStartTime
					iFirstTimeNext = stNextPassPntData.iRelaPassTime + iStartTime
					##冲突超过2个需要警告
					# if len(TmpNodeFlightPlanDataLst) > 1:
					# 	print ('warning:在相反节点中，存在潜在冲突对={0}'.format(len(TmpNodeFlightPlanDataLst)))
					for k in range(len(TmpNodeFlightPlanDataLst)):
						iSecondTime = TmpNodeFlightPlanDataLst[k][0].iRealPassTime
						iSecondTimeNext = TmpNodeFlightPlanDataLst[k][1].iRealPassTime
						##不考虑顺向冲突
						if iSecondTime > iSecondTimeNext:
							continue
						if MathUtilityTool.isInsect(iFirstTime, iFirstTimeNext, iSecondTime, iSecondTimeNext):
							iConFlightPlanID = TmpNodeFlightPlanDataLst[k][0].iFlightPlanID
							pConFlightPlan = self.pFlightPlanMgr.getFlightPlanByID(iConFlightPlanID)
							eFixPntType = self.pDataManager.getFixPntConType(stNextPassPntData.iFixID)
							iCurPathID = PathData.iPathID
							iConPathID = pConFlightPlan.getFlightPlanPath().iPathID

							iFirstPassTime = iFirstTimeNext
							iSecondPassTime = iSecondTime

							stConflictData = ConflictData(pFlightPlan.getFlightPlanID(), iConFlightPlanID, \
														  E_CONFLICT_TYPE.E_CONFLICT_CROSS, eFixPntType,
														  stNextPassPntData.iFixID, iCurPathID, \
														  iConPathID, iFirstPassTime, iSecondPassTime)
							##有冲突，继续判断是否需要Q函数解决
							return self._judgeNeedQFunResolveCon(pFlightPlan, PathData, \
																 pConFlightPlan, stConflictData), stConflictData

			for j in range(len(AdjNodeLst)):
				##相反节点A->B 与 B->A
				##处理不相等情况
				if AdjNodeLst[j] != stPassPntData.iFixID:
					AdjNodeFlightPlanDataLst = self._getNodePassPnt(AdjNodeLst[j])
					TmpNodeFlightPlanDataLst = []

					if AdjNodeFlightPlanDataLst == None:
						continue

					for k in range(len(AdjNodeFlightPlanDataLst)):
						for m in range(len(NodeFlightPlanDataLst)):
							##当前后两个节点飞行计划相同时候纳入考虑
							if NodeFlightPlanDataLst[m].iFlightPlanID == AdjNodeFlightPlanDataLst[k].iFlightPlanID:
								TmpNodeFlightPlanDataPair = []
								##和上面加入顺序刚好相反
								TmpNodeFlightPlanDataPair.append(AdjNodeFlightPlanDataLst[k])
								TmpNodeFlightPlanDataPair.append(NodeFlightPlanDataLst[m])
								TmpNodeFlightPlanDataLst.append(TmpNodeFlightPlanDataPair)

					##冲突超过2个需要警告
					# if len(TmpNodeFlightPlanDataLst) > 1:
					# 	print('warning:在不同节点中，存在潜在冲突对={0}'.format(len(TmpNodeFlightPlanDataLst)))
					for k in range(len(TmpNodeFlightPlanDataLst)):
						iPassTime = iStartTime + stNextPassPntData.iRelaPassTime
						iSecondTime = TmpNodeFlightPlanDataLst[k][0].iRealPassTime
						iSecondTimeNext = TmpNodeFlightPlanDataLst[k][1].iRealPassTime

						##不考虑顺向冲突
						if iSecondTime > iSecondTimeNext:
							continue

						if fabs(iPassTime - iSecondTimeNext) < ConfigReader.iConflictTimeThread:
							##有冲突，继续判断是否需要Q函数解决
							iConFlightPlanID = TmpNodeFlightPlanDataLst[k][0].iFlightPlanID
							pConFlightPlan = self.pFlightPlanMgr.getFlightPlanByID(iConFlightPlanID)
							eFixPntType = self.pDataManager.getFixPntConType(stNextPassPntData.iFixID)
							iCurPathID = PathData.iPathID
							iConPathID = pConFlightPlan.getFlightPlanPath().iPathID

							iFirstPassTime = iPassTime
							iSecondPassTime = iSecondTimeNext

							stFirstFixData = self.pDataManager.getFixPointByID(stPassPntData.iFixID)
							stNextFixPntData = self.pDataManager.getFixPointByID(stNextPassPntData.iFixID)
							stConFirstFixPntData = self.pDataManager.getFixPointByID(TmpNodeFlightPlanDataLst[k][0].iFixPntID)
							stConNextFixPntData = stNextFixPntData


							eConType = UtilityTool.getConflictType(CguPos(stFirstFixData.dX,stFirstFixData.dY ),CguPos(stNextFixPntData.dX,stNextFixPntData.dY), \
							                            CguPos(stConFirstFixPntData.dX, stConFirstFixPntData.dY),CguPos(stConNextFixPntData.dX,stConNextFixPntData.dY ))
							stConflictData = ConflictData(pFlightPlan.getFlightPlanID(),iConFlightPlanID, \
							                             eConType,eFixPntType ,stNextPassPntData.iFixID,iCurPathID, \
														  iConPathID, iFirstPassTime, iSecondPassTime  )
							##有冲突，继续判断是否需要Q函数解决
							return  self._judgeNeedQFunResolveCon(pFlightPlan, PathData,\
							        pConFlightPlan,stConflictData), stConflictData
		##end of for
		return E_RESOLVE_TYPE.E_RESOLVE_NONE,None