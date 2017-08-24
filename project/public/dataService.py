from .dataServer import MSSQL
from .scenarioDataObj import *
from .dataObj import *
from .config import ConfigReader
from ..src.utility import UtilityTool

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
        for fixpoint_id, icon_id, fixpoint_name, airport_id, type, x, y, z, is_waiting_point, fix_conflict_type in resultList:
            eConflictType = E_FIXPOINT_CONF_TYPE(fix_conflict_type)

            cugPos = CguPos(x, y)
            cguCenterPos = CguPos(ConfigReader.dCenterLon, ConfigReader.dCenterLat)
            cguCovertPos = UtilityTool.covertLonLat2XY(cugPos, cguCenterPos)

            stFixPntData = FixPointData(fixpoint_id, fixpoint_name, cguCovertPos.x, cguCovertPos.y, eConflictType)
            FixPointDataDic.setdefault(fixpoint_id, stFixPntData)
        return FixPointDataDic

    def loadQStateActionScoreDataLst(self):
        sql = 'select * from qstate_info'
        stQStateActionScoreDataLst = []
        resultList = self.pMsSql.execQuery(sql)
        for start_fix_id, end_fix_id, conflict_fix_id, fix_pnt_type, cur_flight_type, conflict_flight_type, \
            conflict_type, path_id, con_path_id, state_id, state_score, action_type in resultList:
            eFixPntType = E_FIXPOINT_CONF_TYPE(fix_pnt_type)
            curFlightType = ENUM_FP_TYPE(cur_flight_type)
            conFlightType = ENUM_FP_TYPE(conflict_flight_type)
            conflictType = E_CONFLICT_TYPE(conflict_type)
            stQStateData = QStateData(start_fix_id, end_fix_id, conflict_fix_id, eFixPntType, curFlightType, conFlightType, \
                                      conflictType, path_id, con_path_id)
            stQAction = ENUM_QACTION_TYPE(action_type)
            dScore = state_score
            stQStateActionScoreData = QStateActionScoreData(stQStateData, stQAction, dScore)
            stQStateActionScoreDataLst.append(stQStateActionScoreData)
        return stQStateActionScoreDataLst

    def loadPathData(self):
        pathDataDic = {}
        sql = 'select * from path'
        resultList = self.pMsSql.execQuery(sql)
        for path_id, path_name, start_fix_id, end_fix_id, use_num in resultList:
            stPathData = PathData(path_id, path_name, start_fix_id, end_fix_id, use_num, [])
            sqlSub = 'select * from path_pass_info where path_id = {0} order by path_id, sequence'.format(path_id)
            resultSubList = self.pMsSql.execQuery(sqlSub)
            vPassPntData = []
            for path_id, sequence, fix_id, fix_name, rela_pass_time in resultSubList:
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
        for road_id, airport_id, road_name, type, width, max_aircraft in resultList:
            stRoadData = RoadData(road_id, road_name, [])
            sqlSub = 'select * from road_fixpoint where road_id = {0} order by road_id, sequence'.format(road_id)
            resultSubList = self.pMsSql.execQuery(sqlSub)
            vFixPnt = []
            for road_id, sequence, type, key_id, airport_id, in resultSubList:
                sqlSecondSub = 'select * from fixpoint where fixpoint_id = {0}'.format(key_id)
                resultSecondSubList = self.pMsSql.execQuery(sqlSecondSub)
                if (len(resultSecondSubList) == 1):
                    for fixpoint_id, icon_id, fixpoint_name, airport_id, type, x, y, z, is_waiting_point, fix_conflict_type in resultSecondSubList:
                        cugPos = CguPos(x, y)
                        cguCenterPos = CguPos(ConfigReader.dCenterLon, ConfigReader.dCenterLat)
                        cguCovertPos = UtilityTool.covertLonLat2XY(cugPos, cguCenterPos)
                        stFixPointData = FixPointData(fixpoint_id, fixpoint_name, cguCovertPos.x, cguCovertPos.y, fix_conflict_type)
                        vFixPnt.append(stFixPointData)
                        break
            stRoadData.vFixPnt = vFixPnt
            roadDataDic.setdefault(stRoadData.iId, stRoadData)
        return roadDataDic

    def saveQStateData(self, QStateActionScoreDataLst):
        if QStateActionScoreDataLst == None:
            return

        for i in range(len(QStateActionScoreDataLst)):
            stQStateData = QStateActionScoreDataLst[i].QStateData
            stQActionData = QStateActionScoreDataLst[i].QActionData
            dScore = QStateActionScoreDataLst[i].dScore
            ##先删除存在的Q数据
            sql = 'DELETE  FROM  qstate_info WHERE start_fix_id = {0} AND end_fix_id = {1} AND conflict_fix_id ={2}\
            AND fix_pnt_type = {3} AND cur_flight_type = {4} AND conflict_flight_type = {5} \
            AND conflict_type = {6} AND path_id = {7} AND con_path_id = {8}  AND action_type = {9}' \
            .format(stQStateData.iStartFixID, stQStateData.iEndFixID,stQStateData.iConflictFixID, stQStateData.efixPntType.value,\
                    stQStateData.eCurFlightType.value, stQStateData.eConFlightType.value,stQStateData.eConflictType.value,\
                    stQStateData.iPathID, stQStateData.iConPathID, stQActionData.value)
            self.pMsSql.execNonQuery(sql)

            sql = 'INSERT INTO qstate_info VALUES({0}, {1}, {2},{3},{4},{5},{6},{7},{8}, {9}, {10}, {11})'\
            .format(stQStateData.iStartFixID, stQStateData.iEndFixID,stQStateData.iConflictFixID, stQStateData.efixPntType.value,\
                    stQStateData.eCurFlightType.value, stQStateData.eConFlightType.value,stQStateData.eConflictType.value,\
                    stQStateData.iPathID, stQStateData.iConPathID, 1,dScore,stQActionData.value)
            self.pMsSql.execNonQuery(sql)


    def savePathData(self, PathIDLst):
        if PathIDLst == None:
            return
        for i in range(len(PathIDLst)):
            iID = PathIDLst[i]
            sql = 'UPDATE path SET use_num = use_num + 1 WHERE path_id = {0}'.format(iID)
            self.pMsSql.execNonQuery(sql)