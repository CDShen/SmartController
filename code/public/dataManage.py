"""
brief 方法包括数据库数据的初始化、获取结构方法
"""
from .dataObj import *

##brief 数据管理类
class DataManager(object):
    FixPointDataDic = {}
    def init(self):
        bInit = True
        return  bInit
    def getFlightPlanAllPath(self, iStartID, iEndID):
        vPathData = None
        return vPathData
    def getFixPntConType(self, iFixPntID):
        efixPntType = E_FIXPOINT_CONF_TYPE.E_FIXPOINT_CONF_ARR
        return efixPntType
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