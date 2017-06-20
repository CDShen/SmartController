from .baseDataDef import BaseData


##brief 配置文件
##iFlightPlanNum->飞行计划数量
##iWorkState->1:学习模式 2：验证模式
##bNeedShow->是否需要演示
##iStepCount->快进倍速
##remark
class ConfigReader(BaseData):
	_fields = ['iFlightPlanNum','iWorkState','bNeedShow', 'iStepCount', 'dThresholdScore']

	@classmethod
	def loadConfig(cls):
		bSucess = False
		return bSucess