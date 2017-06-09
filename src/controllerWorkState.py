
class ControllerWorkState(object):

	def onProcessMsg(self, msg):
		pass


##brief:学习状态类
class LearnWorkState(ControllerWorkState):
	def __init__(self, pFlightMgr, pPathSelect):
		self.pFlightMgr = pFlightMgr
		self.pPathSelect = pPathSelect
		self.bFinished = False
		self.iFutureMin = 10 ##未来N分钟的时间
	def onProcessMsg(self, msg):
		pass
	##brief 处理时钟包，学习模式不需要处理时钟包
	def processTimePacket(self, timePacket):
		##取当前的计划运算更新Q状态
		##当前集合的飞机运算看是否结束
		pass
	##brief 开始学习入口
	def doWork(self):
		while 1>0:
			##获取下一个飞行计划
			nextFlightPlan = self._getNextFlightPlan()
			if nextFlightPlan == None:
				return
			else:
				pass
			##将此计划的后N分钟计划加入集合



		##对合法路径进行打分、更新Q值后加入集合
		##返回合法路径
		pass
	def _getNextFlightPlan(self):
		return self.pFlightMgr.getNextFlightPlan()
	def _updateFutureFlightPlan(self):
		self.pFlightMgr.updateFutureFlightPlan()
	def _pathSelect(self, curFlpghtPlan):
		pass







##brief:验证状态类
class ValidateWorkState(ControllerWorkState):
	def onProcessMsg(self, msg):
		pass
	def processTimePacket(self, timePacket):
		##取当前计划的加入直接从Q函数中获取结果


		##当前计划的飞机运算看是否结束
		pass


