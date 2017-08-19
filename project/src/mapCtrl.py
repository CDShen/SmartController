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
		self.plt = plt
	class FixPointData(BaseData):
		_fields = ['iID', 'strName', 'dX', 'dY', 'eConflictType']

	def setRoadData(self, stRoadData):
		self.RoadDataDic = copy.deepcopy(stRoadData)
		# for i in self.RoadDataDic:
		# 	vFixPntData = self.RoadDataDic.get(i).vFixPnt
		# 	for j in range(len(vFixPntData)):
		# 		stFixData = vFixPntData[j]
		# 		cugPos = CguPos(stFixData.dX, stFixData.dY)
		# 		cguCenterPos = CguPos(ConfigReader.dCenterLon, ConfigReader.dCenterLat)
		# 		cguCovertPos = UtilityTool.covertLonLat2XY(cugPos, cguCenterPos)
		# 		stFixData.dX = cguCovertPos.x
		# 		stFixData.dY = cguCovertPos.y



	def showData(self):
		#显示地面滑行图

		##显示滑行道基础数据
		self.showRoadData()

	def showRoadData(self):
		xLst = []
		yLst = []
		for i in self.RoadDataDic:
			vFixPntData = self.RoadDataDic.get(i).vFixPnt
			strRoadName = self.RoadDataDic.get(i).strName
			for j in range(len(vFixPntData)):
				stFixData = vFixPntData[j]
				xLst.append(stFixData.dX)
				yLst.append(stFixData.dY)

		fig = self.plt.figure()
		ax1 = fig.add_subplot(1, 1, 1, xlim=(min(xLst) - 100, max(xLst) + 100), ylim=(min(yLst) - 100, max(yLst) + 100))
		ax1.set_title('Airport')
		# line, = ax1.plot([], [], '-', label='TaxiLine', lw=1)

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
			##'k-':黑色直线
			ax1.plot(xLst, yLst, 'k-', label='TaxiLine', lw=1)
			ax1.text(avgX, avgY, strRoadName, family='serif', style='italic', ha='right', wrap=True)
		plt.show()

