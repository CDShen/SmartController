"""
brief 结合DataManager、FlightMgr和utility进行错误的滑行路线的评分和输出
"""
from .flightPlanMgr import FlightPlanMgr
from ..public.dataManage import DataManager
from .utility import UtilityTool
from .flightPlan import FlightPlan
from .taxiMap import TaxiMap
from .qLearnCore import QLearnFunction
from ..public.scenarioDataObj import *
from ..public.config import ConfigReader

class PathSelect(object):
    def __init__(self, pFlightMgr):
        self.pFlightPlan = None
        self.dThresholdScore = ConfigReader.dThresholdScore ##路线最低分阈值
        self.pTaxiMap = pFlightMgr.pTaxiMap
        self.pFlightMgr = pFlightMgr
        self.pDataManage = pFlightMgr.pDataManage
        self.pQLearnFunction = QLearnFunction(pFlightMgr.pDataManage)

    def setCurFlightPlan(self, pFlightPlan):
        self.pFlightPlan = pFlightPlan

    def selectPath(self):
        #获取该路径的所有合法路径
        CurFlightPlanData = self.pFlightPlan.getFlightPlanData()
        iStartID = CurFlightPlanData.iStartPosID
        iEndId = CurFlightPlanData.iEndPosID
        vPathData = self.pDataManage.getFlightPlanAllPath(iStartID, iEndId)
        bNeedAddTime = False
        #判断该路径是否有冲突，如果有冲突用Q学习产生并更新Q数据
        ScorePathLst = []
        for i in range(len(vPathData)):
            ScorePathDic = self._pathScore(vPathData[i])
            ScorePathLst.append(ScorePathDic)

        ##路线排序,冒泡分数由大到小
        for i in range(len(ScorePathLst) - 1):
            bOK = True
            for j in range(0, len(ScorePathLst) - 1 - i):
                item = ScorePathLst[j]
                itemNext = ScorePathLst[j + 1]
                if item.get('score') < itemNext.get('score'):
                    itemTmp = itemNext
                    ScorePathLst[j + 1] = item
                    ScorePathLst[j] = itemTmp
                    bOK = False
            if bOK:
                break


        dMaxScore = ScorePathLst[0].get('score')
        bestProperFPPath = ScorePathLst[0].get('FPPath')


        if bestProperFPPath == None:
            print ('呼号={0}查找不到路线'.format(CurFlightPlanData.strName))
        ##如果分数小于阈值，重新寻路获取值
        if dMaxScore < self.dThresholdScore:
            print ('呼号={0}分数过低,当前分数为{1},当前阈值为{2}'.format(CurFlightPlanData.strName,dMaxScore,self.dThresholdScore))
            ##可以先不做，因为地图小，可以穷举出可能路径
            ##添加错误信息
            self.path = self.pFlightPlan.setBestProperPath(bestProperFPPath)
        else:
            self.path = self.pFlightPlan.setBestProperPath(bestProperFPPath)

        return  bNeedAddTime
    ##返回dict
    def _pathScore(self, PathData):
        #test start
        strCallsign = self.pFlightPlan.getCallsign()
        if strCallsign == 'CBJ5698' or strCallsign == 'CSN3111':
            x = 1
            pass
        #test end

        iStartTime = self.pFlightPlan.getFlightPlanStartTime()
        ScorePathDic = {'score': None, 'orgPath': None,'FPPath': None}
        dScore = 0.0
        orgPath = None
        FPPath = None
        eResolveType, ConflictData  = self.pTaxiMap.calConflictType(self.pFlightPlan, PathData)
        if eResolveType == E_RESOLVE_TYPE.E_RESOLVE_NONE:
            dScore = UtilityTool.getTotalPathTaxiTime(PathData)
            orgPath = PathData
            FPPath = UtilityTool.transPathData2FPPathData(iStartTime, PathData)

        elif eResolveType == E_RESOLVE_TYPE.E_RESOLVE_INNER:
            ##其他飞机避让
            iFlightPlanID, FPPathData =  self.pTaxiMap.getResolveFlightPlanData()
            self.pFlightMgr.getFlightPlanByID(iFlightPlanID).setBestProperPath(FPPathData)
            self.pTaxiMap.clearResolveFlightPlanData()
            dScore = UtilityTool.getTotalPathTaxiTime(PathData)
            orgPath = PathData
            FPPath = UtilityTool.transPathData2FPPathData(iStartTime, PathData)

        elif eResolveType == E_RESOLVE_TYPE.E_RESOLVE_QFUN:
            ##交给Q函数处理
            self.pQLearnFunction.setCurFlightPlan(self.pFlightPlan)
            pConFlightPlan = self.pFlightMgr.getFlightPlanByID(ConflictData.iConfFPID)
            ##dscore为一个综合值，并不只是解决冲突时间
            dScore, orgPath ,FPPath= self.pQLearnFunction.pathSelect(self.pFlightPlan, PathData, pConFlightPlan, ConflictData)
        ##如果是在起点有冲突需要加时间重新算

        ScorePathDic['score'] = dScore
        ScorePathDic['orgPath'] = orgPath
        ScorePathDic['FPPath'] = FPPath
        return  ScorePathDic

    def getQStateActionData(self):
        return self.pQLearnFunction.getQStateActionData()





