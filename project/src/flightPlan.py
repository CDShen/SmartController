from ..public.scenarioDataObj import *
from .taxSimulator import TaxSimulator
from .utility import MathUtilityTool
from ..public.config import ConfigReader

class FlightPlan(object):
	##brief 飞行计划初始化
	##FlightPlanData[in]->飞行计划信息
	def __init__(self, FlightPlanData, FPPathData, strStartPosName,strEndPosName):
		self.FlightPlanData = FlightPlanData
		self.FPPathData = FPPathData
		self.eStatus = ENUM_FP_STATUS.E_STATUS_FUTURE
		self.strStartPosName = strStartPosName
		self.strEndPosName = strEndPosName
	#brief获取最佳的滑行路线
	def setBestProperPath(self, FPPathData):
		self.FPPathData = FPPathData
	def getFlightPlanPath(self):
		return self.FPPathData

	def getCallsign(self):
		return self.FlightPlanData.strName

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
	def getFlightFPStatus(self):
		return self.eStatus
	##breif 通过时间更新飞行计划状态
	def updateTaxState(self, iTime):
		vFPPassPntData = self.FPPathData.vFPPassPntData
		stFirstFPPassPntData = vFPPassPntData[0]
		stLastFPPassPntData = vFPPassPntData[len(vFPPassPntData)-1]
		if iTime < stFirstFPPassPntData.iRealPassTime:
			self.updateFPStatus(ENUM_FP_STATUS.E_STATUS_FUTURE)
		elif iTime >= stFirstFPPassPntData.iRealPassTime and iTime < stLastFPPassPntData.iRealPassTime:
			self.updateFPStatus(ENUM_FP_STATUS.E_STATUS_ACTIVE)
		elif iTime >= stLastFPPassPntData.iRealPassTime:
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

	def getStartPosName(self):
		return self.strStartPosName
	def getEndPosName(self):
		return self.strEndPosName
	##飞行计划ID
	def getFlightPlanID(self):
		return self.FlightPlanData.iID

	def isFutureFlightPlan(self):
		if self.eStatus.value == ENUM_FP_STATUS.E_STATUS_FUTURE.value:
			return  True
		else:
			return  False

	def getFlightType(self):
		return  self.FlightPlanData.eFlightType

	def clearPath(self):
		self.FPPathData = None

	def getPosByTime(self, iTime):
		cguPos = CguPos(0,0)
		for i in range(len(self.FPPathData.vFPPassPntData)-1):
			stFirstPassPntData = self.FPPathData.vFPPassPntData[i]
			stNextPassPntData = self.FPPathData.vFPPassPntData[i+1]
			if iTime >=  stFirstPassPntData.iRealPassTime and iTime < stNextPassPntData.iRealPassTime:
				ePassPntType = stNextPassPntData.ePassPntType
				if ePassPntType == ENUM_PASSPNT_TYPE.E_PASSPNT_NORMAL:
					cguPos = MathUtilityTool.getPosBySpdTime(CguPos(stFirstPassPntData.x,stFirstPassPntData.y), CguPos(stNextPassPntData.x,stNextPassPntData.y), \
															 iTime-stFirstPassPntData.iRealPassTime, ConfigReader.dNormalTaxSpd/3.6)

				elif ePassPntType == ENUM_PASSPNT_TYPE.E_PASSPNT_STOP:
					pass
				elif ePassPntType == ENUM_PASSPNT_TYPE.E_PASSPNT_STOP:
					pass

				return cguPos
