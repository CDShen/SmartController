from .flightPlanMgr import FlightPlanMgr
from ..public.dataManage import DataManager

def main():
	##根据配置文件更新数据库
	pDataManager = DataManager()
	pDataManager.init()
	##根据配置文件产生对应飞行计划
	n = 100
	pFlightPlanMgr = FlightPlanMgr()
	vFlightPlanData = pFlightPlanMgr.createFlightPlan(n)
	##根据配置文件产生正确的工作模式

	pass



if __name__=='__main__':
	main()