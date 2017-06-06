from ..public.scenarioDataObj import FlightPlanData
from ..public.scenarioDataObj import CguPos
from ..public.scenarioDataObj import ENUM_PASSPNT_TYPE


##brief 负责滑行的计算
class TaxSimulator(object):
	def __init__(self, FlightPlan, FPPathData):
		self.FlightPlan = FlightPlan
		self.FPPathData = FPPathData
		self.iCurIndex = 0
		self.bFinished = False
	##更新飞机滑行位置
	def updateState(self, dFrame):
		if self.bFinished == True:
			return
		##更新位置
		i = self.iCurIndex
		stCurPntData = self.FPPathData.vFPPassPntData[i]
		stNextPntData = self.FPPathData.vFPPassPntData[i+1]
		ePassPntType = self.FPPathData.vFPPassPntData[i+1].ePassPntType

		dSpd = 0.0  ##速度单位m/s
		##正常按40km/h滑行
		if ePassPntType.value == ENUM_PASSPNT_TYPE.E_PASSPNT_NORMAL.value:
			pass
		##停止需要
		elif ePassPntType.value == ENUM_PASSPNT_TYPE.E_PASSPNT_STOP.value:
			pass
		elif ePassPntType.value == ENUM_PASSPNT_TYPE.E_ACTION_SLOWDOWN.value:
			pass





class FlightPlan(object):
	##brief 飞行计划初始化
	##FlightPlanData[in]->飞行计划信息
	def __init__(self, FlightPlanData):
		self.FlightPlanData = FlightPlanData
		self.bFinished = False
		self.FPPathData = None
		self.CguPos = None
		self.bStarted = False ##是否是未来计划
		self.TaxState = None

	def setTaxState(self, FPPathData):
		self.TaxState = TaxSimulator(self, FPPathData)

	##brief 飞行计划计算，看是否完成已经结束
	##dframe 计算帧率
	def updateState(self, dFrame):
		if self.bFinished == True or self.FPPathData == None or self.bStarted == False:
			return







