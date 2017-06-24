from .baseDataDef import BaseData


##brief 配置文件
##iFlightPlanNum->飞行计划数量
##iWorkState->1:学习模式 2：验证模式
##bNeedShow->是否需要演示
##iStepCount->快进倍速
##dThresholdScore->最小分数
##iFutureTimeMin->考虑未来航班分钟数
##iConflictTimeThread->冲突判断门限阈值
##dBeta->学习因子
##remark

class ConfigReader(BaseData):
	_fields = ['iFlightPlanNum','iWorkState','bNeedShow', 'iStepCount',\
	           'dThresholdScore', 'iFutureTimeMin', 'iConflictTimeThread','dBeta']

	@classmethod
	def loadConfig(cls):
		bSucess = False
		return bSucess