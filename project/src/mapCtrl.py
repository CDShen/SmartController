"""
通用函数
目前有算出过点时间和判断是否和计划集合有冲突

"""

print (__doc__)

from math import *
from ..public.dataObj import *
from ..public.scenarioDataObj import *
from ..public.dataManage import DataManager
from .utility import UtilityTool
import copy
from ..public.config import ConfigReader
import matplotlib.pyplot as plt

class MapCtrl(object):
	def __init__(self):
		self.RoadDataDic = {}

	class FixPointData(BaseData):
		_fields = ['iID', 'strName', 'dX', 'dY', 'eConflictType']

	def setRoadData(self, stRoadData):
		self.RoadDataDic = copy.deepcopy(stRoadData)
		for i in self.RoadDataDic:
			vFixPntData = self.RoadDataDic.get(i).vFixPnt
			for j in range(len(vFixPntData)):
				stFixData = vFixPntData[j]
				cugPos = CguPos(stFixData.dX, stFixData.dY)
				cguCenterPos = CguPos(ConfigReader.dCenterLon, ConfigReader.dCenterLat)
				cguCovertPos = UtilityTool.covertLonLat2XY(cugPos, cguCenterPos)
				stFixData.dX = cguCovertPos.x
				stFixData.dY = cguCovertPos.y



	def showData(self):
		#显示地面滑行图

		##显示滑行道基础数据
		self.showRoadData()

	def showRoadData(self):

		for i in self.RoadDataDic:
			vFixPntData = self.RoadDataDic.get(i).vFixPnt
			strRoadName = self.RoadDataDic.get(i).strName
			xLst = []
			yLst = []
			sumX = 0.0
			sumY = 0.0
			for j in range(len(vFixPntData)):
				stFixData = vFixPntData[j]
				xLst.append(stFixData.dX)
				yLst.append(stFixData.dY)
				sumX += stFixData.dX
				sumY += stFixData.dY
				# plt.figure(figsize=(100, 10))
				# 画图
			# plt.plot(xLst, yLst, label = strRoadName, color=' black ', linestyle='-')  # 默认
			avgX = sumX / len(vFixPntData)
			avgY = sumY / len(vFixPntData)
			plt.plot(xLst, yLst, color = 'black', linestyle= '-')
			plt.text(avgX, avgY,strRoadName)
		plt.show()

