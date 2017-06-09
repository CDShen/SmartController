class FlightPlanMgr(object):
	def __init__(self):
		self.FlightPlanPathDic = None ##格式{ id, 'FlightPlanPathData'} _fields = ['FlightPlanData', 'FPPathData']
	##1、获取下一个飞行计划，如果为空表示该episode结束，时间根据ID递增
	##2、判断是否该飞行计划时候是否有飞行计划已经结束并置位
	def getNextFlightPlan(self):
		pass
	##更新未来的飞行计划看是否结束
	def updateFutureFlightPlan(self):
		pass

	##brief 获取指定ID的飞行计划
	def getFlightPlanByID(self, iObjID):
		return self.FlightPlanPathDic.get(iObjID)


	def setBestProperPath(self, iObjID, FPPathData):
		FlightPlanPath = self.getFlightPlanByID(iObjID)
		FlightPlanPath.FPPathData = FPPathData


