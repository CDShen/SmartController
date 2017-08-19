"""
brief 飞行计划生成器，暂时读取Designer生成后的csv格式生成，每个csv文件对应一个episode
"""

from ..public.scenarioDataObj import *
from ..public.dataObj import *
from ..public.dataManage import DataManager
from .flightPlan import FlightPlan
from ..public.config import ConfigReader

import csv
class FlightPlanGen(object):
	#brief 根据文件序号读取文件产生飞行计划
	@classmethod
	def geneFlightPlan(cls, iSeq, pDataManager):
		pFlightPlanLst = []
		##读取本次序号的航班计划

		with open(ConfigReader.strTrainDataPath + '/flightplan{0}.csv'.format(iSeq+1)) as f:
			f_csv = csv.DictReader(f)
			for r in f_csv:
				iObjID = int(r.get('ID'))
				strCallsign = r.get('Callsign')
				eFlightType = ENUM_FP_TYPE(int(r.get('FlightType')))
				iStartTime = int(r.get('StartTime'))
				iStartFixID = int(r.get('StartFixID'))
				iEndFIxID = int(r.get('EndFixID'))

				stFlightPlanData = FlightPlanData(iObjID, strCallsign, eFlightType,iStartTime, iStartFixID, iEndFIxID )
				PathData = pDataManager.getMaxUseValPath(iStartFixID, iEndFIxID)
				##转换为场景数据
				FPPathData = FlightPlanGen._transDataObjData(PathData, iStartTime, pDataManager)
				pFlightPlan = FlightPlan(stFlightPlanData , FPPathData)
				pFlightPlanLst.append(pFlightPlan)
			return pFlightPlanLst
	#brief 将数据库数据转化为场景数据
	@classmethod
	def _transDataObjData(self, PathData, iStartTime, pDataManager):
		vFPPassPntData = []
		for i in range(len(PathData.vPassPntData)):
			PassPntData = PathData.vPassPntData[i]
			stFixPointData = pDataManager.getFixPointByID(PassPntData.iFixID)
			stFPPassPntData = FPPassPntData(PassPntData.iFixID, PassPntData.iRelaPassTime + iStartTime, stFixPointData.dX, \
										  stFixPointData.dY, ENUM_PASSPNT_TYPE.E_PASSPNT_NORMAL)
			vFPPassPntData.append(stFPPassPntData)
		return FPPathData(PathData.iPathID ,vFPPassPntData)










