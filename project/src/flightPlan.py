from ..public.scenarioDataObj import *
from .taxSimulator import TaxSimulator


class FlightPlan(object):
	##brief 飞行计划初始化
	##FlightPlanData[in]->飞行计划信息
	def __init__(self, FlightPlanData, FPPathData):
		self.FlightPlanData = FlightPlanData
		self.FPPathData = FPPathData
		self.eStatus = ENUM_FP_STATUS.E_STATUS_FUTURE

	#brief获取最佳的滑行路线
	def setBestProperPath(self, FPPathData):
		self.FPPathData = FPPathData
	def getFlightPlanPath(self):
		return self.FPPathData

	def getFlightPlanData(self):
		return self.FlightPlanData
	def setTaxState(self, FPPathData):
		self.TaxState = TaxSimulator(self, FPPathData)

	##brief 飞行计划计算，看是否完成已经结束
	##dframe 计算帧率
	def updateState(self, dFrame):
		if self.eStatus == ENUM_FP_STATUS.E_STATUS_FIN or self.FPPathData == None or self.eStatus == ENUM_FP_STATUS.E_STATUS_FUTURE:
			return

	def updateFPStatus(self, eStatus):
		self.eStatus = eStatus

	##breif 通过时间更新飞行计划状态
	def updateTaxState(self, iTime):
		vFPPassPntData = self.FPPathData.vFPPassPntData
		stLastFPPassPntData = vFPPassPntData[len(vFPPassPntData)-1]
		if iTime >= stLastFPPassPntData.iRealPassTime:
			self.updateFPStatus(ENUM_FP_STATUS.E_STATUS_FIN)

	##brief 飞行计划是否结束
	def isFlightPlanFin(self):
		if self.eStatus.value >= ENUM_FP_STATUS.E_STATUS_FIN.value:
			return  True
		else:
			return  False

	##brief 飞行计划开始时刻
	def getFlightPlanStartTime(self):
		return  self.FlightPlanData.iTaxStartTime

	##飞行计划ID
	def getFlightPlanID(self):
		return self.FlightPlanData.iID
	##得到飞行计划滑行路径
	def getFlightPlanPath(self):
		return self.FPPathData

	def isFutureFlightPlan(self):
		if self.eStatus.value == ENUM_FP_STATUS.E_STATUS_FUTURE.value:
			return  True
		else:
			return  False

	def getFlightType(self):
		return  self.FlightPlanData.eFlightType

	def clearPath(self):
		self.FPPathData = None




