from .pathSelect import PathSelect
from ..public.config import ConfigReader



class ControllerWorkState(object):

	def onProcessMsg(self, msg):
		pass


##brief:学习状态类
##remark:暂时先写到LearnWorkState最后在放在基类中
class LearnWorkState(ControllerWorkState):
	def __init__(self, pFlightMgr):
		self.pFlightMgr = pFlightMgr
		self.pPathSelect = PathSelect(pFlightMgr)

	##brief 初始化
	def init(self):
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
	##学习时候都是学习完成之后在开始滑行
	def doWork(self):
		##获取下一个飞行计划
		pNextFlightPlan = self._getNextFlightPlan()
		while pNextFlightPlan != None:
			##删除该飞行计划的计划滑行数据
			# pNextFlightPlan.clearPath()
			iCurID = pNextFlightPlan.getFlightPlanID()
			self.pFlightMgr.setCurFlightPlanID(iCurID)
			iTime = pNextFlightPlan.getFlightPlanStartTime()
			##更新此时刻的飞行计划状态
			self._updateFlightPlan(iTime)
			##将此计划N分钟后的飞行计划(包括自己)加入集合和去除已经完成的飞行计划
			self._addFutureFlightPlan(iTime + ConfigReader.iFutureTimeMin*60)
			self._refreshFlightPlan()
			##对合法路径进行打分、更新Q值后加入集合
			self.pPathSelect.setCurFlightPlan(pNextFlightPlan)
			self._pathSelect()
			##将当前滑行路径添加到滑行地图中
			self.pFlightMgr.addCurPath2TaxMap()
			##判断当前是否有多个冲突
			self.pFlightMgr.judgeIsHasConflict()
			pNextFlightPlan = self._getNextFlightPlan(iCurID)
	def getQStateActionData(self):
		return self.pPathSelect.getQStateActionData()

	def getAllFlightPlanBestPath(self):
		return self.pFlightMgr.getAllFlightPlanBestPath()
	def _getNextFlightPlan(self,iStartID = -1):
		return self.pFlightMgr.getNextFlightPlan(iStartID)
	def _addFutureFlightPlan(self, iTime):
		self.pFlightMgr.addFutureFlightPlan(iTime)

	def _pathSelect(self):
		self.pPathSelect.selectPath()
	def _updateFlightPlan(self, iTime):
		self.pFlightMgr.updateFlightPlan(iTime)
	##更新需要计算的飞行计划集合
	def _refreshFlightPlan(self):
		self.pFlightMgr.refreshFlightPlan()







##brief:验证状态类
class ValidateWorkState(ControllerWorkState):
	def onProcessMsg(self, msg):
		pass
	def processTimePacket(self, timePacket):
		##取当前计划的加入直接从Q函数中获取结果


		##当前计划的飞机运算看是否结束
		pass


