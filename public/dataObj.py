"""
breif:主要定义存储在文件中读取后的原始数据，读取数据格式为CSV或数据库表，这里只负责读取，不需要增删改
"""



from enum import Enum
from baseDataDef import BaseData




###################数据库基础数据
##########地图基础数据
#brief:基础数据表构成需要 fixPoint, road, road_fixPnt, aiport四个基础表
#####固定点
##iID->固定节点的ID 
##strName->固定节点的名称
##dX->固定节点笛卡尔X坐标值
##dY->固定节点笛卡尔Y坐标值
##eConflictType->固定节点冲突类型 0：先来先服务 1：进港优先 2：离港优先


class FixPointData(BaseData):
	_fields = ['iID', 'strName', 'dX', 'dY','eConflictType']

#####滑行道
##iId->道路的ID
##strName->道路的名称
##vFixPnt->道路的固定点组成list，list顺序即是滑行点的序号
class RoadData(BaseData):
	_fields = ['iId', 'strName', 'vFixPnt']

#####机场
##iId->机场的ID
##strName->机场的名称
##vRoad->机场组成的滑行道list，没有先后顺序
class AirportData(BaseData):
	_fields = ['iID', 'strName', 'vRoad']


###################历史滑行路径数据
##########历史滑行数据
#####过点时间
##iFixID->固定点
##iRelaPassTime->相对默认40km/h滑行时间，包含起始点和终止点
class PassPntData(BaseData):
	_fields = ['iFixID', 'iRelaPassTime']

#####滑行路径
##iRoadID->滑行路径ID
##iUseNum->使用次数
##vPassPntData->过点时间list, list顺序即滑行序号
class PathData(BaseData):
	_fields = ['iRoadID', 'iUseNum', 'vPassPntData']

#####起始/终点滑行路径集合
##iStartID->起始固定点ID
##iEndID->结束固定点ID
##vPathData->起始/终点对应的所有滑行路径集合
class HistoryPathData(BaseData):
	_fields = ['iStartID','iEndID', 'vPathData']




