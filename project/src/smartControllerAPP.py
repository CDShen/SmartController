from ..public.dataManage import DataManager
from ..public.config import ConfigReader
from .flightPlanMgr import FlightPlanMgr
from .controllerWorkState import *
from .utility import UtilityTool
from .mapCtrl import MapCtrl

class SmartControllerAPP(object):
    def __init__(self):
        self.pDataManager = None
        self.pWorkState = None
        self.pMapCtrl = None
    def init(self, iSeq):

        ##根据配置文件更新数据库
        self.pDataManager = DataManager()
        if self.pDataManager.init() == False:
            print ('数据库启动失败')
            return False


        ##根据配置文件产生对应飞行计划，现在是读取所有的产生的.csv文件
        # n = ConfigReader.iFlightPlanNum
        pFlightPlanMgr = FlightPlanMgr(self.pDataManager)
        pFlightPlanMgr.createFlightPlan(iSeq)  ##根据CSV文件产生飞行计划

        if ConfigReader.iWorkState == 1:
            self.pWorkState = LearnWorkState(pFlightPlanMgr)
        ##1,2暂时都一样，待修改
        elif ConfigReader.iWorkState == 2:
            ##其他工作模式
            self.pWorkState = LearnWorkState(pFlightPlanMgr)
            pass

        ##公共转换中需要DataManager获取某些数据
        UtilityTool.pDataManager = self.pDataManager

        self.pMapCtrl = MapCtrl(pFlightPlanMgr)
        self.pMapCtrl.setRoadData(self.pDataManager.getRoadDataDic())

        return True

    def _save(self):
        ##获取需要保存的数据1、QState状态 2、滑行路线
        QStateActionScoreDataLst = self.pWorkState.getQStateActionData()
        PathIDLst = self.pWorkState.getAllFlightPlanBestPath()

        ##存储数据
        if self.pDataManager.saveData(QStateActionScoreDataLst, PathIDLst):
            print('保存数据库成功')
            return True
        else:
            print('保存数据库失败')
            return False

    def run(self, bLast = False):
        ##开始工作
        self.pWorkState.doWork()

        ##输出学习结果
        self.pWorkState.LearnEpisodeMsg()

        ##如果是验证状态不保存，因为是经过大量样本训练，所以本次的影响可以不计入
        bSave = True
        if ConfigReader.iWorkState == 2:
            bSave = False
        if bSave == True:
            if self._save() == False:
                print('存储数据失败')
        else:
            print ('验证模式，不存储')



        ##演示滑行
        if ConfigReader.bNeedShow == True and bLast == True:
            ##test地图显示
            self.pMapCtrl.showData()
            # test_end








