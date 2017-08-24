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
from matplotlib import animation
import datetime

class MapCtrl(object):
	def __init__(self, pFlightPlanMgr):
		self.RoadDataDic = {}
		self.pFlightPlanMgr = pFlightPlanMgr
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

	def _resetFlightPlanData(self):
		self.pFlightPlanMgr.resetFlightPlanData()
	def animate(self, iFrame):
		iTime = iFrame * ConfigReader.iStepCount
		hour = int(iTime/3600%24)
		min = int(iTime/60%60)
		second = int(iTime%60)
		time = datetime.datetime.combine(datetime.date.today(), datetime.time(hour, min, second))
		strTime = time.strftime('%Y-%m-%d %H:%M:%S')



		# x = np.linspace(0, 2, 100)
		# y = np.sin(2 * np.pi * (x - 0.01 * iFrame))
		ax1 = plt.subplot(1,1,1)
		ax1.cla()
		xMin,xMax,yMin,yMax = self._getMaxMinLim()
		ax1.set_ylim(yMin, yMax)
		ax1.set_xlim(xMin, xMax)


		ax1.set_title('Time:  '+strTime)

		##显示滑行道基础数据
		self.showRoadData(ax1)

		self.pFlightPlanMgr.updateFlightPlanData(iTime)
		ActiveFlightPlanLst = self.pFlightPlanMgr.getActiveFlightPlanLst(iTime)
		if ActiveFlightPlanLst == None:
			return

		LineList = []
		for i in range(len(ActiveFlightPlanLst)):
			pFlightPlan = ActiveFlightPlanLst[i]
			cguCurPos = pFlightPlan.getPosByTime(iTime)
			strCallsign = pFlightPlan.getCallsign()
			eFlightType = pFlightPlan.getFlightType()
			iStartTime = pFlightPlan.getFlightPlanStartTime()
			StartTime = datetime.time(int(iStartTime/3600%24), int(iStartTime/60%60), int(iStartTime%60))
			strStartTime = StartTime.strftime('%H:%M:%S')
			strStartPosName = pFlightPlan.getStartPosName()
			strEndPosName = pFlightPlan.getEndPosName()
			if eFlightType == ENUM_FP_TYPE.E_FP_TYPE_ARR:
				strFlightType = 'ARR'
			elif eFlightType == ENUM_FP_TYPE.E_FP_TYPE_DEP:
				strFlightType = 'DEP'
			strLabel = strCallsign + ',' + strFlightType + ',' + strStartTime + ','+strStartPosName+'-->'+strEndPosName
			if eFlightType == ENUM_FP_TYPE.E_FP_TYPE_ARR:
				line, = ax1.plot(cguCurPos.x, cguCurPos.y, 'ro', label=strLabel, lw=1)
			elif eFlightType == ENUM_FP_TYPE.E_FP_TYPE_DEP:
				line, = ax1.plot(cguCurPos.x, cguCurPos.y, 'go', label=strLabel, lw=1)
			ax1.text(cguCurPos.x, cguCurPos.y, strCallsign, family='serif', style='italic', ha='right', wrap=True)
			LineList.append(line)

		ax1.legend(loc='upper right')

		return LineList

	def showTaxiData(self, ax):
		pass

	def showData(self):
		self._resetFlightPlanData()
		fig = plt.figure()
		xMin,xMax,yMin,yMax = self._getMaxMinLim()
		fig.add_subplot(1, 1, 1, xlim=(xMin, xMax), ylim=(yMin, yMax))
		##animal没用也不能消除，这是一个对象
		animal = animation.FuncAnimation(fig, self.animate, frames=3600, interval=1000)
		plt.show()

	def _getMaxMinLim(self):
		xLst = []
		yLst = []
		for i in self.RoadDataDic:
			vFixPntData = self.RoadDataDic.get(i).vFixPnt
			for j in range(len(vFixPntData)):
				stFixData = vFixPntData[j]
				xLst.append(stFixData.dX)
				yLst.append(stFixData.dY)
		return min(xLst)-100,max(xLst)+100, min(yLst)-100, max(yLst)+100

	def showRoadData(self, ax):
		ax1 = ax
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
			ax1.plot(xLst, yLst, 'k-.', lw=1)
			ax1.text(avgX, avgY, strRoadName, family='serif', style='italic', ha='right', wrap=True)

