"""
brief 方法包括数据库数据的初始化、获取结构方法
"""
from .dataObj import *
from ..src.utility import *

##brief 数据管理类
class DataManager(object):
    QStateActionScoreDataLst = []
    FixPointDataDic = {}
    PathDataDic = {}
    def init(self):
        bInit = True
        return  bInit
    def getFlightPlanAllPath(self, iStartID, iEndID):
        vPathData = []
        for k in self.PathDataDic:
            if PathData[k].iStartFixID == iStartID and PathData[k].iEndFixID == iEndID:
                vPathData.append(PathData[k])
        return vPathData
    def getPathDataByID(self, iPathID):
        return self.PathDataDic.get(iPathID)

    def getFixPntConType(self, iFixPntID):
        eFixPntType = E_FIXPOINT_CONF_TYPE.E_FIXPOINT_CONF_ARR
        return eFixPntType
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

    def saveData(self):
        bSucess = True
        return  bSucess

    def findQState(self, QStateData):
        bFind = False
        QStateActionScoreDataLst = []
        iCount = 0
        for i in range(len(self.QStateActionScoreDataLst)):
            stQStateData = self.QStateActionScoreDataLst[i].QStateActionScoreData.QStateData
            if stQStateData == QStateData:
                QStateActionScoreDataLst.append(QStateActionScoreDataLst[i])
                iCount += 1
                if iCount == 2:
                    bFind = True
                    return bFind, QStateActionScoreDataLst

        return bFind, QStateActionScoreDataLst

    def getPathAverageRatio(self, iPathID):
        vPathData = []
        stPathData = self.getPathDataByID(iPathID)
        iCurPathTotalTime = UtilityTool.getTotalPathTaxiTime(stPathData)
        vPathData = self.getFlightPlanAllPath(stPathData.iStartFixID, stPathData.iEndFixID)
        iTotalTime = 0
        for i in range(len(vPathData)):
            iTotalTime += UtilityTool.getTotalPathTaxiTime(vPathData[i])

        return iCurPathTotalTime/iTotalTime