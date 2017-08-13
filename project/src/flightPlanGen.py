"""
brief 飞行计划生成器，暂时读取Designer生成后的csv格式生成，每个csv文件对应一个episode
"""

from ..public.scenarioDataObj import *
from ..public.dataObj import *
from ..public.dataManage import DataManager
from .flightPlan import FlightPlan


class FlightPlanGen(object):
	#brief 产生飞行计划，产生的飞行计划已经包含了历史滑行数据
	@classmethod
	def geneFlightPlan(cls, n, pDataManager):
		pFlightPlanLst = []
		for i in range(n):
			##通过外部获取飞行计划数据
			FlightPlanData = None
			PathData = pDataManager.getMaxUseValPath(FlightPlanData.iStartPosID, FlightPlanData.iEndPosID)
			##转换为场景数据
			FPPathData = FlightPlanGen._transDataObjData(PathData, FlightPlanData.iTaxStartTime, pDataManager)
			pFlightPlan = FlightPlan(FlightPlanData, FPPathData)
			pFlightPlanLst.append(pFlightPlan)
		return pFlightPlanLst
	#brief 将数据库数据转化为场景数据
	@classmethod
	def _transDataObjData(self, PathData, iStartTime, pDataManager):
		vFPPassPntData = []
		for i in range(PathData.vPassPntData):
			PassPntData = PathData.vPassPntData[i]
			FixPointData = pDataManager.getFixPointByID(PassPntData.iFixID)
			FPPassPntData = FPPassPntData(PassPntData.iFixID, PassPntData.iRelaPassTime + iStartTime, FixPointData.x, \
										  FixPointData.y, ENUM_PASSPNT_TYPE.E_PASSPNT_NORMAL)
			vFPPassPntData.append(FPPassPntData)
		return FPPathData(PathData.iPathID ,vFPPassPntData)










