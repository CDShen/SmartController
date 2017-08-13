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

	##获取滑行道数据
	def loadRoadData(self):
		roadDataDic = {}
		sql = 'select * from road'
		resultList = self.pMsSql.execQuery(sql)
		for road_id, airport_id, road_name, type, width,  max_aircraft in resultList:
			stRoadData = RoadData(road_id, road_name,[])
			sqlSub = 'select * from road_fixpoint where road_id = {0} order by road_id, sequence'.format(road_id)
			resultSubList = self.pMsSql.execQuery(sqlSub)
			vFixPnt = []
			for road_id, sequence, type, key_id, airport_id, in resultSubList:
				sqlSecondSub = 'select * from fixpoint where fixpoint_id = {0}'.format(key_id)
				resultSecondSubList = self.pMsSql.execQuery(sqlSecondSub)
				if (len(resultSecondSubList) == 1):
					for fixpoint_id, icon_id, fixpoint_name, airport_id, type, x, y, z, is_waiting_point, fix_conflict_type in resultSecondSubList:
						stFixPointData = FixPointData(fixpoint_id, fixpoint_name, x, y,fix_conflict_type)
						vFixPnt.append(stFixPointData)
						break
			stRoadData.vFixPnt = vFixPnt
			roadDataDic.setdefault(stRoadData.iId, stRoadData)
		return  roadDataDic

