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
        elif ConfigReader.iWorkState == 2:
            ##其他工作模式
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


        if self._save() == False:
            print ('存储数据失败')



        ##演示滑行
        if ConfigReader.bNeedShow == True and bLast == True:
            ##test地图显示
            self.pMapCtrl.showData()
            # test_end








