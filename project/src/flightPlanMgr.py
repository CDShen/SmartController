from ..public.scenarioDataObj import *
from .taxiMap import TaxiMap
from .flightPlanGen import FlightPlanGen
from .flightPlan import FlightPlan
from ..public.dataManage import DataManager

class FlightPlanMgr(object):
	def __init__(self, pDataManager):
		self.FlightPlanDic = {} ##所有生成的飞行计划数据 格式{ id, 'FlightPlan'}
		self.curFlightPlanDic = {} ##当前需要参加运算的飞行计划集合
		self.iCurFlanID = -1
		self.pTaxiMap = TaxiMap(self, pDataManager)
		self.pDataManage = pDataManager
	##brief 创建飞行计划
	def createFlightPlan(self, iSeq):
		pFlightPlanLst = FlightPlanGen.geneFlightPlan(iSeq, self.pDataManage)
		for i in range(len(pFlightPlanLst)):
			self.FlightPlanDic.setdefault(pFlightPlanLst[i].getFlightPlanID(), pFlightPlanLst[i])

	##1、获取下一个飞行计划，如果为空表示该episode结束，时间根据ID递增
	##2、判断是否该飞行计划时候是否有飞行计划已经结束并置位
	##3、如果开始为-1证明从头开始取
	def getNextFlightPlan(self, iStartID = -1):
		iNextPlanID = -1
		if iStartID == -1:
			iNextPlanID = 1
		else:
			iNextPlanID = iStartID + 1
		pFlightPlan = self.FlightPlanDic.get(iNextPlanID)
		if pFlightPlan == None:
			return  None
		else:
			return  pFlightPlan

	def setCurFlightPlanID(self, iFPlanID):
		self.iCurFlanID = iFPlanID

	##更新未来的飞行计划看是否结束
	def updateFutureFlightPlan(self):
		pass

	##更新飞行计划状态
	def updateFlightPlan(self, iTime):
		for k in self.curFlightPlanDic:
			pFlightPlan = self.curFlightPlanDic.get(k)
			pFlightPlan.updateTaxState(iTime)


	##brief 获取指定ID的飞行计划
	def getFlightPlanByID(self, iFPlanID):
		return self.FlightPlanDic.get(iFPlanID)

	def getAllFlightPlanBestPath(self):
		PathIDLst = []
		for i in self.FlightPlanDic:
			pFlightPlan = self.curFlightPlanDic.get(i)
			FPPathData = pFlightPlan.getFlightPlanPath()
			PathIDLst.append(FPPathData.iPathID)
		return  PathIDLst


	def addFutureFlightPlan(self, iTime):
		##当前计划
		pCurFlightPlan = self.getFlightPlanByID(self.iCurFlanID)
		if self.curFlightPlanDic.get(self.iCurFlanID) == None:
			self.curFlightPlanDic.setdefault(self.iCurFlanID, pCurFlightPlan)

		##后续计划
		pFlightPlan = self.getNextFlightPlan(self.iCurFlanID)
		while pFlightPlan != None:
			iFutureFlightPlanID = pFlightPlan.getFlightPlanID()
			iStartTime = pFlightPlan.getFlightPlanStartTime()
			##开始时间大于未来时间时候直接退出循环
			if  iStartTime <= iTime:
				if self.curFlightPlanDic.get(iFutureFlightPlanID) == None:
					self.curFlightPlanDic.setdefault(iFutureFlightPlanID, pFlightPlan)
					##添加当前从没加入到未来航班汇总的计划到滑行地图中
					self.pTaxiMap.addFlightPlanPath(pFlightPlan)
			else:
				break
			iFutureFlightPlanID += 1
			pFlightPlan = self.getNextFlightPlan(iFutureFlightPlanID)

	def refreshFlightPlan(self):
		for k in self.curFlightPlanDic:
			pFlightPlan = self.FlightPlanDic.get(k)
			if k < self.iCurFlanID:
				if pFlightPlan.isFlightPlanFin():
					##删除taxiMap滑行路线
					self.pTaxiMap.delFlightPlanPath(pFlightPlan.getFlightPlanID())
					##删除飞行计划
					del self.curFlightPlanDic[k]
			elif k == self.iCurFlanID:
				pFlightPlan.updateFPStatus(ENUM_FP_STATUS.E_STATUS_ACTIVE)
				pFlightPlan.clearPath()
				##删除当前的滑行数据
				self.pTaxiMap.delFlightPlanPath(self.iCurFlanID)
			else:
				pFlightPlan.updateFPStatus(ENUM_FP_STATUS.E_STATUS_FUTURE)


	def isFlightPlanStartByID(self, iFlightPlanID):
		return  self.FlightPlanDic.get(iFlightPlanID).isFplightPlanStart()




