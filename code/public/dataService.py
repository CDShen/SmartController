from .dataServer import MSSQL
from .scenarioDataObj import *
from .dataObj import *
from .config import ConfigReader

class DataService(object):
	def __init__(self):
		self.pMsSql = MSSQL(ConfigReader.strIP, ConfigReader.strUser, ConfigReader.strPwd, ConfigReader.DBName)
	def isConnectDB(self):
		if self.pMsSql.getConnect() == None:
			return False
		else:
			return True
	def loadFixPntData(self):
		sql = 'select * from fixpoint'
		FixPointDataDic = {}
		resultList = self.pMsSql.execQuery(sql)
		for fixpoint_id,icon_id,fixpoint_name,airport_id,type,x,y,z,is_waiting_point,fix_conflict_type in resultList:
			stFixPntData = FixPointData(fixpoint_id, fixpoint_name,x,y,fix_conflict_type )
			FixPointDataDic.setdefault(fixpoint_id, stFixPntData)
		return FixPointDataDic

	def loadQStateActionScoreDataLst(self):
		sql = 'select * from qstate_info'
		stQStateActionScoreDataLst = []
		resultList = self.pMsSql.execQuery(sql)
		for start_fix_id,end_fix_id,conflict_fix_id,fix_pnt_type,cur_flight_type,conflict_flight_type, \
		    conflict_type, path_id, con_path_id, state_id, state_score, action_type in resultList:
			stQStateData = QStateData(start_fix_id, end_fix_id, conflict_fix_id, fix_pnt_type, cur_flight_type,conflict_flight_type, \
			                          conflict_type, path_id,con_path_id)
			stQAction = ENUM_QACTION_TYPE(action_type)
			dScore = state_score
			stQStateActionScoreData = QStateActionScoreData(stQStateData, stQAction, dScore)
			stQStateActionScoreDataLst.append(stQStateActionScoreData)
		return stQStateActionScoreDataLst

	class PassPntData(BaseData):
		_fields = ['iFixID', 'iRelaPassTime']

	#####滑行路径
	##iPathID->滑行路径ID  唯一
	##iUseNum->使用次数
	##iStartFixID->开始固定点ID
	##iEndFixID->结束固定点ID
	##vPassPntData->过点时间list, list顺序即滑行序号
	class PathData(BaseData):
		_fields = ['iPathID', 'iStartFixID', 'iEndFixID', 'iUseNum', 'vPassPntData']

	def loadPathData(self):
		pathDataDic = {}
		sql = 'select * from path'
		resultList = self.pMsSql.execQuery(sql)
		for path_id, start_fix_id, end_fix_id, ues_num in resultList:
			stPathData = PathData(path_id, start_fix_id, end_fix_id, ues_num, [])
			sqlSub = 'select * from path_pass_info where path_id = {0} order by path_id, sequence'.format(path_id)
			resultSubList = self.pMsSql.execQuery(sqlSub)
			vPassPntData = []
			for path_id, sequence, fix_id, rela_pass_time in resultSubList:
				stPassPntData = PassPntData(fix_id, rela_pass_time)
				vPassPntData.append(stPassPntData)

			stPathData.vPassPntData = vPassPntData
			pathDataDic.setdefault(path_id, stPathData)
		return pathDataDic