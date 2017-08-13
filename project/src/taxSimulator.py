from ..public.scenarioDataObj import FlightPlanData
from ..public.scenarioDataObj import CguPos
from ..public.scenarioDataObj import ENUM_PASSPNT_TYPE
from ..public.scenarioDataObj import ENUM_FP_STATUS


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