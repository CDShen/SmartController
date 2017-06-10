from ..public.scenarioDataObj import *

class FlightPlanMgr(object):
	def __init__(self):
		self.FlightPlanDic = None ##格式{ id, 'FlightPlan'}
		self.curFlightPlanDic = None ##当前需要参加运算的飞行计划集合
		self.iCurFlanID = -1
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


	def setBestProperPath(self, iFPlanID, FPPathData):
		FlightPlanPath = self.getFlightPlanByID(iFPlanID)
		FlightPlanPath.FPPathData = FPPathData

	def addFutureFlightPlan(self, iTime):
		iFPlanID = self.iCurFlanID
		pFlightPlan = self.getNextFlightPlan(iFPlanID)
		while pFlightPlan != None:
			iStartTime = pFlightPlan.getFlightPlanStartTime()
			if  iStartTime <= iTime:
				if self.curFlightPlanDic[iFPlanID] == None:
					pFlightPlan.updateFPStatus(ENUM_FP_STATUS.E_STATUS_FUTURE)
					self.curFlightPlanDic.setdefault(iFPlanID, pFlightPlan)
			else:
				break
			iFPlanID+=1
			pFlightPlan = self.getNextFlightPlan(iFPlanID)

	def refreshFlightPlanSet(self):
		for k in self.curFlightPlanDic:
			pFlightPlan = self.FlightPlanDic.get(k)
			if pFlightPlan.isFlightPlanFin():
				del self.FlightPlanDic[k]




