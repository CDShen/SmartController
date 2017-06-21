"""
brief 结合DataManager、FlightMgr和utility进行错误的滑行路线的评分和输出
"""
from .flightPlanMgr import FlightPlanMgr
from ..public.dataManage import DataManager
from .utility import UtilityTool
from .flightPlan import FlightPlan
from .taxiMap import TaxiMap

class PathSelect(object):
    def __init__(self, dThresholdScore, pFlightMgr):
        self.pFlightPlan = None
        self.dThresholdScore = dThresholdScore ##路线最低分阈值
        self.pTaxiMap = pFlightMgr.pTaxiMap
        self.pFlightMgr = pFlightMgr
        self.pDataManage = pFlightMgr.pDataManage

    def setCurFlightPlan(self, pFlightPlan):
        self.pFlightPlan = pFlightPlan

    def selectPath(self):
        #获取该路径的所有合法路径
        CurFlightPlanData = self.pFlightPlan.getFlightPlanData()
        iStartID = CurFlightPlanData.iStartPosID
        iEndId = CurFlightPlanData.iEndPosID
        vPathData = self.pDataManage.getFlightPlanAllPath(iStartID, iEndId)

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
        bestProperPath = ScorePathLst[0].get('path')

        ##如果分数小于阈值，重新寻路获取值
        if dMaxScore < self.dThresholdScore:
            ##可以先不做，因为地图小，可以穷举出可能路径
            ##添加错误信息
            pass
        else:
            self.pFlightPlan.setBestProperPath(bestProperPath)


    ##返回dict
    def _pathScore(self, PathData):
        ScorePathDic = {'score': None, 'path': None}
        dScore = 0.0
        path = None
        ConflictData = None
        ##
        if self.pTaxiMap.isConflict(self.pFlightPlan, PathData, ConflictData) == False:
            dScore = UtilityTool.getTotalPathTaxiTime(PathData)
            path = PathData

        else:
            ##交给Q函数处理
            pass
        ScorePathDic['score'] = dScore
        ScorePathDic['path'] = PathData






