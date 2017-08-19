"""
brief 方法包括数据库数据的初始化、获取结构方法
"""
from .dataObj import *
from .dataService import DataService
from ..src.utility import *

##brief 数据管理类
class DataManager(object):
    QStateActionScoreDataLst = []
    PathDataDic = {}
    FixPointDataDic = {}
    RoadDataDic = {}
    def init(self):
        bInit = True
        self.pDataService = DataService()
        if self.pDataService.isConnectDB() == False:
            return False

        self.QStateActionScoreDataLst = self.pDataService.loadQStateActionScoreDataLst()
        self.FixPointDataDic = self.pDataService.loadFixPntData()
        self.PathDataDic = self.pDataService.loadPathData()
        self.RoadDataDic = self.pDataService.loadRoadData()


        return  bInit
    def getFlightPlanAllPath(self, iStartID, iEndID):
        vPathData = []
        for k in self.PathDataDic:
            if self.PathDataDic.get(k).iStartFixID == iStartID and self.PathDataDic.get(k).iEndFixID == iEndID:
                vPathData.append(self.PathDataDic.get(k))
        return vPathData
    def getPathDataByID(self, iPathID):
        return self.PathDataDic.get(iPathID)

    def getFixPntConType(self, iFixPntID):
        eConflictType = self.FixPointDataDic.get(iFixPntID).eConflictType
        return eConflictType

    def getMaxUseValPath(self, iStartID, iEndID):
        vPathData = self.getFlightPlanAllPath(iStartID, iEndID)
        iUseMaxNum = -1
        iPathIndex = -1
        for i in range(len(vPathData)):
            if vPathData[i].iUseNum > iUseMaxNum:
                iUseMaxNum = vPathData[i].iUseNum
                iPathIndex = i
        return  vPathData[iPathIndex]

    def getFixPointByID(self, iFixPntID):
        return  self.FixPointDataDic.get(iFixPntID)

    ##brief:存储更新训练数据，1、Q函数 2、历史滑行路径选择
    def saveData(self, QStateActionScoreDataLst, PathIDLst):
        self.pDataService.saveQStateData(QStateActionScoreDataLst)
        self.pDataService.savePathData(PathIDLst)
        bSucess = True
        return  bSucess

    def findQState(self, QStateData):
        bFind = False
        QCurStateActionScoreDataLst = []
        iCount = 0
        for i in range(len(self.QStateActionScoreDataLst)):
            stQStateData = self.QStateActionScoreDataLst[i].QStateData
            if stQStateData == QStateData:
                QCurStateActionScoreDataLst.append(QStateActionScoreDataLst[i])
                iCount += 1
                ##因为只有减速和等待两种方式
                if iCount == 2:
                    bFind = True
                    return bFind, QCurStateActionScoreDataLst

        return bFind, QCurStateActionScoreDataLst




    def getPathAverageRatio(self, iPathID):
        vPathData = []
        stPathData = self.getPathDataByID(iPathID)
        iCurPathTotalTime = UtilityTool.getTotalPathTaxiTime(stPathData)
        vPathData = self.getFlightPlanAllPath(stPathData.iStartFixID, stPathData.iEndFixID)
        iTotalTime = 0
        for i in range(len(vPathData)):
            iTotalTime += UtilityTool.getTotalPathTaxiTime(vPathData[i])
        return iCurPathTotalTime/iTotalTime

    def getRoadDataDic(self):
        return  self.RoadDataDic