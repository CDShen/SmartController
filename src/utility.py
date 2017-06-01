"""
通用函数
目前有算出过点时间和判断是否和计划集合有冲突

"""

print (__doc__)

from ..public.data import *


class UtilityTool(object):
	dTheta = None

	# brief:输入当前的计划，返回常规过点时间
	# flightschedule:[in] 当前飞行计划数据
	# vPassPntTimeData:[out] 当前飞行计划过点时间
	# return:无
	@classmethod
	def predict_pass_time(curFlightscheduleData, vPassPntTimeData):
		pass
	# passPntData:[in] 当前过点时间
	# vPassPntData:[in] 当前过点时间
	# conflict:[out] 冲突航班对
	def isConflict(self, passPntData, vPassPntData, conflict):
		pass

	def resolveConflict(self, eActionType, vPassPntData):
		pass
