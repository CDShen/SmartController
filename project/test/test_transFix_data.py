from math import *
from project.public.dataServer import MSSQL
from project.public.dataObj import *
from project.src.utility import UtilityTool
from project.public.scenarioDataObj import *

class DataService(object):
    def __init__(self):
        self.pMsSql = MSSQL('192.168.0.163', 'sa', '123456', 'ATCSIM_VIRTUAL')
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

    def loadPathData(self):
        pathDataDic = {}
        sql = 'select * from path'
        resultList = self.pMsSql.execQuery(sql)
        for path_id, path_name, start_fix_id, end_fix_id, ues_num in resultList:
            stPathData = PathData(path_id, path_name, start_fix_id, end_fix_id, ues_num,[])
            sqlSub = 'select * from path_pass_info where path_id = {0} order by path_id, sequence'.format(path_id)
            resultSubList = self.pMsSql.execQuery(sqlSub)
            vPassPntData = []
            for path_id, sequence, fix_id, fix_name,rela_pass_time in resultSubList:
                stPassPntData = PassPntData(fix_id, rela_pass_time)
                vPassPntData.append(stPassPntData)

            stPathData.vPassPntData = vPassPntData
            pathDataDic.setdefault(path_id, stPathData)
        return pathDataDic

    def reFormatPathData(self, pathDataDic):
        for k in pathDataDic:
            for i in range(len(pathDataDic.get(k).vPassPntData)):
                iPassTime = pathDataDic.get(k).vPassPntData[i].iRelaPassTime
                iFixID = pathDataDic.get(k).vPassPntData[i].iFixID
                iPathID = k
                sql = 'UPDATE  path_pass_info SET rela_pass_time = {0} WHERE path_id = {1} AND fix_id = {2}'.format(iPassTime, iPathID, iFixID)
                self.pMsSql.execNonQuery(sql)



dCenterLon = 1.9869022130175
dCenterLat = 0.6024779615148

pDataService = DataService()
if pDataService.isConnectDB() ==  False:
    print ('DB is not connected')
fixDataDic = pDataService.loadFixPntData()
pathDataDic = pDataService.loadPathData()

##数据转换
for k in pathDataDic:
    vFixData = pathDataDic.get(k).vPassPntData
    iRealTime = 0
    vFixData[0].iRelaPassTIme = 0
    for i in range(len(vFixData)-1):
        stFirFixData = fixDataDic.get(vFixData[i].iFixID)
        stSecFixData = fixDataDic.get(vFixData[i+1].iFixID)
        cugFirPos = CguPos(stFirFixData.dX, stFirFixData.dY)
        cugSecPos = CguPos(stSecFixData.dX, stSecFixData.dY)
        cguCenterPos = CguPos(dCenterLon, dCenterLat)
        cguFirCovertPos = UtilityTool.covertLonLat2XY(cugFirPos, cguCenterPos)
        cguSecCovertPos = UtilityTool.covertLonLat2XY(cugSecPos, cguCenterPos)
        dDis = pow(pow(cguFirCovertPos.x-cguSecCovertPos.x,2) + pow(cguFirCovertPos.y-cguSecCovertPos.y,2),0.5)
        iTIme = int(dDis/10)
        vFixData[i+1].iRelaPassTime = vFixData[i].iRelaPassTime + iTIme

pDataService.reFormatPathData(pathDataDic)