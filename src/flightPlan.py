from ..public.scenarioDataObj import FlightPlanData
from ..public.scenarioDataObj import CguPos
from ..public.scenarioDataObj import ENUM_PASSPNT_TYPE
from ..public.scenarioDataObj import ENUM_FP_STATUS


class FlightPlan(object):
	##brief 飞行计划初始化
	##FlightPlanData[in]->飞行计划信息
	def __init__(self, FlightPlanData):
		self.FlightPlanData = FlightPlanData
		self.FPPathData = None
		self.CguPos = None
		self.eStatus = ENUM_FP_STATUS.E_STATUS_FUTURE.value

	#brief获取最佳的滑行路线
	def setBestProperPath(self, FPPathData):
		self.FPPathData = FPPathData

	def GetFlightPlanData(self):
		return self.FlightPlanData
	def setTaxState(self, FPPathData):
		self.TaxState = TaxSimulator(self, FPPathData)

	##brief 飞行计划计算，看是否完成已经结束
	##dframe 计算帧率
	def updateState(self, dFrame):
		if self.eStatus == ENUM_FP_STATUS.E_STATUS_FIN.value or self.FPPathData == None or self.eStatus == ENUM_FP_STATUS.E_STATUS_FUTURE.value:
			return

	def updateFPStatus(self, eStatus):
		self.eStatus = eStatus







