from .baseDataDef import BaseData


##brief 配置文件
##iFlightPlanNum->飞行计划数量
##iWorkState->1:学习模式 2：验证模式
##bNeedShow->是否需要演示
##iStepCount->快进倍速
##dThresholdScore->最小分数
##iFutureTimeMin->考虑未来航班分钟数
##iConflictTimeThread->冲突判断门限阈值
##dBeta->Q学习权重
##dTheta->Q学习冲突时间和历史时间的权重
##dSlowMinSpd->减速动作时候的最小速度
##dSafeDis->减速运动和停止时候的最小安全距离
##iResolveConfilictTime->过点多少时间后才仍为解决冲突
##dNonePathFine->没有解决冲突时候的惩罚值
##remark

class ConfigReader(BaseData):
	_fields = ['iFlightPlanNum','iWorkState','bNeedShow', 'iStepCount',\
	           'dThresholdScore', 'iFutureTimeMin', 'iConflictTimeThread','dBeta','dTheta'\
	           'dSlowMinSpd', 'dSafeDis', 'iResolveConfilictTime', 'dNonePathFine']

	@classmethod
	def loadConfig(cls):
		bSucess = False
		return bSucess