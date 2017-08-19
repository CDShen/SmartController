from .baseDataDef import BaseData
from configparser import ConfigParser



##brief 配置文件

##strIP->数据库IP
##strUser->用户名
##strPwd->密码
##strDbName->数据库名称
##strTrainDataPath->训练计划数据位置
##dCenterLon->中心经度
##dCenterLat->中心纬度
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
##iResolveConfilictTime->过点多少时间后才认为解决冲突
##dNonePathFine->没有解决冲突时候的惩罚值
##remark


class ConfigReader(BaseData):
	_fields = ['strIP', 'strUser','strPwd','strDbName','strTrainDataPath','dCenterLon','dCenterLat','iFlightPlanNum','iWorkState','bNeedShow', 'iStepCount',\
	           'dThresholdScore', 'iFutureTimeMin', 'iConflictTimeThread','dBeta','dTheta'\
	           'dSlowMinSpd', 'dSafeDis', 'iResolveConfilictTime', 'dNonePathFine']

	@classmethod
	def loadConfig(cls):
		cfg = ConfigParser()
		cfg.read('config.ini')
		sectionHeaderLst = cfg.sections()

		if len(sectionHeaderLst) == 0:
			return False
		##读取数据库数据
		ConfigReader.strIP = cfg.get('DataBase', 'IP')
		ConfigReader.strUser = cfg.get('DataBase', 'User')
		ConfigReader.strPwd = cfg.get('DataBase', 'Password')
		ConfigReader.DBName = cfg.get('DataBase', 'DBName')
		ConfigReader.strTrainDataPath = cfg.get('DataBase', 'TrainDataPath')
		##读取系统参数
		ConfigReader.dCenterLon = cfg.getfloat('Para', 'dCenterLon')
		ConfigReader.dCenterLat = cfg.getfloat('Para', 'dCenterLat')
		ConfigReader.iFlightPlanNum = cfg.getint('Para', 'iFlightPlanNum')
		ConfigReader.iWorkState = cfg.getint('Para', 'iWorkState')
		ConfigReader.bNeedShow = cfg.getboolean('Para', 'bNeedShow')
		ConfigReader.iStepCount = cfg.getint('Para', 'iStepCount')
		ConfigReader.dThresholdScore = cfg.getfloat('Para', 'dThresholdScore')
		ConfigReader.iFutureTimeMin = cfg.getint('Para', 'iFutureTimeMin')
		ConfigReader.iConflictTimeThread = cfg.getint('Para', 'iConflictTimeThread')
		ConfigReader.dBeta = cfg.getfloat('Para', 'dBeta')
		ConfigReader.dTheta = cfg.getfloat('Para', 'dTheta')
		ConfigReader.dSlowMinSpd = cfg.getint('Para', 'dSlowMinSpd')
		ConfigReader.dSafeDis = cfg.getint('Para', 'dSafeDis')
		ConfigReader.iResolveConfilictTime = cfg.getint('Para', 'iResolveConfilictTime')
		ConfigReader.dNonePathFine = cfg.getfloat('Para', 'dNonePathFine')


		return True