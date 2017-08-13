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
	def createFlightPlan(self, n):
		pFlightPlanLst = FlightPlanGen.geneFlightPlan(n)
		for i in range(len(pFlightPlanLst)):
			self.FlightPlanDic.setdefault(pFlightPlanLst[i].getFlightPlanID, pFlightPlanLst[i])

	##1、获取下一个飞行计划，如果为空表示该episode结束，时间根据ID递增
	##2、判断是否该飞行计划时候是否有飞行计划已经结束并置位
	def getNextFlightPlan(self, iStartID = -1):
		iNextPlanID = -1
		if iStartID == -1:
			iNextPlanID = self.iCurFlanID+1
		else:
			iNextPlanID = 0
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
		return self.FlightPlanPathDic.get(iFPlanID)

	def addFutureFlightPlan(self, iTime):
		iFPlanID = self.iCurFlanID
		pFlightPlan = self.getNextFlightPlan(iFPlanID)
		while pFlightPlan != None:
			iStartTime = pFlightPlan.getFlightPlanStartTime()
			if  iStartTime <= iTime:
				if self.curFlightPlanDic.get(iFPlanID) == None:
					pFlightPlan.updateFPStatus(ENUM_FP_STATUS.E_STATUS_FUTURE)
					self.curFlightPlanDic.setdefault(iFPlanID, pFlightPlan)
					self.pTaxiMap.addFlightPlanPath(pFlightPlan)
			else:
				break
			iFPlanID += 1
			pFlightPlan = self.getNextFlightPlan(iFPlanID)

	def refreshFlightPlan(self):
		for k in self.curFlightPlanDic:
			pFlightPlan = self.FlightPlanDic.get(k)
			if pFlightPlan.isFlightPlanFin():
				##删除taxiMap滑行路线
				self.pTaxiMap.delFlightPlanPath(pFlightPlan.getFlightPlanID())
				##删除飞行计划
				del self.curFlightPlanDic[k]
		##删除当前的滑行数据
		self.pTaxiMap.delFlightPlanPath(self.iCurFlanID)

	def isFlightPlanStartByID(self, iFlightPlanID):
		return  self.FlightPlanDic.get(iFlightPlanID).isFplightPlanStart()




