"""
brief 方法包括数据库数据的初始化、获取结构方法
"""
from .dataObj import *

##brief 数据管理类
class DataManager(object):
    def init(self):
        pass
    def getFlightPlanAllPath(self, iStartID, iEndID):
        return vPathData
    def getFixPntConType(self, iFixPntID):
        efixPntType = E_FIXPOINT_CONF_TYPE.E_FIXPOINT_CONF_ARR
        return efixPntType