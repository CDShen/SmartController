from ..public.dataManage import DataManager
from ..public.config import ConfigReader
from .flightPlanMgr import FlightPlanMgr
from .controllerWorkState import *

class SmartControllerAPP(object):
    def __init__(self):
        self.pDataManager = None
        self.pWorkState = None
    def init(self):
        bSucess = True
        ##读取配置文件
        if ConfigReader.loadConfig() == False:
            print ('读取配置文件失败')
            return False

        ##根据配置文件更新数据库
        self.pDataManager = DataManager()
        if self.pDataManager.init() == False:
            print ('数据库启动失败')
            return False

        ##根据配置文件产生对应飞行计划
        n = ConfigReader.iFlightPlanNum
        pFlightPlanMgr = FlightPlanMgr(self.pDataManager)
        pFlightPlanMgr.createFlightPlan(n)  ##根据配置文件产生正确的工作模式


        if ConfigReader.iWorkState == 1:
            self.pWorkState = LearnWorkState(pFlightPlanMgr)
        elif ConfigReader.iWorkState == 2:
            ##其他工作模式
            pass
        return bSucess

    def run(self):
        ##开始工作
        self.pWorkState.doWork()
        ##保存数据
        if self.pDataManager.saveData():
            print('保存数据库成功')
        else:
            print('保存数据库失败')

        ##演示滑行
        if ConfigReader.bNeedShow == True:
            ##滑行结果显示
            pass







