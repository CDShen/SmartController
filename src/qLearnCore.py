from ..public.data import * 
from . import Utility




# 1、回报函数R(s,a)
# 2、动作A
# 3、评价函数Q(s,a)
# 4、解决冲突函数
# 5、预测时间函数

class LearnFunction(object):
	pass



class QLearnFunction(LearnFunction):
	def __init__(self, theta, dBeta, pUtility):
		self.dBeta = dBeta
		self.pUtility = pUtility


	# state[in] 冲突状态
	# path[out] 最高分数的滑行路线
	# return 最高分数
	def getScore(self, state, path):
		pass
	def _reward(self, state, action, path):
		pass
	def _qValue(self, state, action, path):
		self.__getqValue(state, action)*(1.0-self.beta)+\
		self.beta*_reward(state, action,path)

	def __getqValue(self, state, action):
		dScore=0.0
		return dScore





