"""
通用函数
目前有算出过点时间和判断是否和计划集合有冲突

"""

print (__doc__)

from ..public.data import *


class Utility(object):
	def __init__(self, dTheta):
		self.dTheta = dTheta
	# brief:输入当前的计划，返回过点时间
	# flightschedule:[in] 当前计划
	# passPntData:[out] 过点时间
	# return:无
	def predict_pass_time(self, curFlightschedule, passPntData):
		pass
	# passPntData:[in] 当前过点时间
	# vPassPntData:[in] 当前过点时间
	# conflict:[out] 冲突航班对
	def isConflict(self, passPntData, vPassPntData, conflict):
		pass

	def resolveConflict(self, eActionType, vPassPntData):
		psss
