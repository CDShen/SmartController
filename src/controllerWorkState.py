
class ControllerWorkState(object):
	def onProcessMsg(self, msg):
		pass


##brief:学习状态类
class LearnWorkState(ControllerWorkState):
	def onProcessMsg(self, msg):
		pass
	##brief 处理时钟包
	def processTimePacket(self, timePacket):
		##取当前的计划运算更新Q状态
		##当前集合的飞机运算看是否结束
		pass


##brief:验证状态类
class ValidateWorkState(ControllerWorkState):
	def onProcessMsg(self, msg):
		pass
	def processTimePacket(self, timePacket):
		##取当前计划的加入直接从Q函数中获取结果


		##当前计划的飞机运算看是否结束
		pass


