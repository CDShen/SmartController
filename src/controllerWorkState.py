
class ControllerWorkState(object):

	def onProcessMsg(self, msg):
		pass


##brief:学习状态类
##remark:暂时先写到LearnWorkState最后在放在基类中
class LearnWorkState(ControllerWorkState):
	def __init__(self, pFlightMgr, pPathSelect):
		self.pFlightMgr = pFlightMgr
		self.pPathSelect = pPathSelect
		self.bFinished = False
		self.iFutureMin = 10 ##未来N分钟的时间

	##brief 加载数据集
	def loadDataSet(self):
		pass
	def onProcessMsg(self, msg):
		pass
	##brief 处理时钟包，学习模式不需要处理时钟包
	##整个数据集处理完成之后在开始滑行，因为可能涉及到已经开始滑行的飞机也需要调整路径
	def processTimePacket(self, timePacket):
		##取当前的计划运算更新Q状态
		##当前集合的飞机运算看是否结束
		pass
	##brief 开始学习入口
	def doWork(self):
		while 1>0:
			##获取下一个飞行计划
			pNextFlightPlan = self._getNextFlightPlan()
			if pNextFlightPlan == None:
				##训练结束
				return
			else:
				self.pFlightMgr.setCurFlightPlanID(pNextFlightPlan.getFlightPlanID())
				iTime = pNextFlightPlan.getFlightPlanStartTime()
				##更新此时刻的飞行计划状态
				self._updateFlightPlan(iTime)
				##将此计划N分钟后的飞行计划加入集合和去除已经完成的飞行计划
				self._addFutureFlightPlan(iTime + self.iFutureMin*60)
				self._refreshFlightPlanSet()
				##对合法路径进行打分、更新Q值后加入集合
				self.pPathSelect.setCurFlightPlan(pNextFlightPlan)
				self._pathSelect()

				pass
		pass
	def _getNextFlightPlan(self):
		return self.pFlightMgr.getNextFlightPlan()
	def _addFutureFlightPlan(self, iTime):
		self.pFlightMgr.addFutureFlightPlan(iTime)

	def _pathSelect(self):
		self.pPathSelect.selectPath()
	def _updateFlightPlan(self, iTime):
		self.pFlightMgr.updateFlightPlan(iTime)
	##更新需要计算的飞行计划集合
	def _refreshFlightPlanSet(self):
		self.pFlightMgr.refreshFlightPlanSet()







##brief:验证状态类
class ValidateWorkState(ControllerWorkState):
	def onProcessMsg(self, msg):
		pass
	def processTimePacket(self, timePacket):
		##取当前计划的加入直接从Q函数中获取结果


		##当前计划的飞机运算看是否结束
		pass


