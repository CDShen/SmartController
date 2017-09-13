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
import random

pause = False




class MapCtrl(object):
	def __init__(self, pFlightPlanMgr):
		self.RoadDataDic = {}
		self.pFlightPlanMgr = pFlightPlanMgr
		self.callSignDic = {}
		##b-蓝色 olive-暗黄色  m-品红  darkslategray-暗青色 orange-橘色 brown-褐色
		self.colorLst = ['blue', 'olive', 'magenta', 'teal', 'brown', 'orange']
		self.iFrameCount = 0
	class FixPointData(BaseData):
		_fields = ['iID', 'strName', 'dX', 'dY', 'eConflictType']

	def onClick(self, event):
		global pause
		pause ^= True

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
	def animate(self, iFrameStep):
		if not pause:
			self.iFrameCount += 1

		iFrame = self.iFrameCount
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

		##更新选择颜色方案,首先删除这次没有和保留已有的
		delLst = []
		for k in self.callSignDic:
			bFind = False
			for i in range(len(ActiveFlightPlanLst)):
				pFlightPlan = ActiveFlightPlanLst[i]
				strCallsign = pFlightPlan.getCallsign()
				if k == strCallsign:
					bFind = True
					break
			if bFind == False:
				delLst.append(k)
		for k in range(len(delLst)):
			del self.callSignDic[delLst[k]]

		LineList = []
		for i in range(len(ActiveFlightPlanLst)):
			pFlightPlan = ActiveFlightPlanLst[i]
			strCallsign = pFlightPlan.getCallsign()
			cguCurPos, iIndex = pFlightPlan.getPosIndexByTime(iTime)

			##获得滑行线
			FPPathData = pFlightPlan.getFlightPlanPath()
			CguPosLst = []
			CguPosLst.append(cguCurPos)
			for i in range(iIndex,len(FPPathData.vFPPassPntData)):
				stFirstData = FPPathData.vFPPassPntData[i]
				cguPos = CguPos(stFirstData.x,stFirstData.y)
				CguPosLst.append(cguPos)

			self.showTaxData(ax1, CguPosLst,strCallsign)


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
				Objline, = ax1.plot(cguCurPos.x, cguCurPos.y, 'ro', label=strLabel, lw=1)
			elif eFlightType == ENUM_FP_TYPE.E_FP_TYPE_DEP:
				Objline, = ax1.plot(cguCurPos.x, cguCurPos.y, 'go', label=strLabel, lw=1)

			eCurPassPntType = pFlightPlan.getCurPassPntType()
			strPassPntType = ''
			if eCurPassPntType == ENUM_PASSPNT_TYPE.E_PASSPNT_NORMAL:
				strPassPntType = 'N'
			if eCurPassPntType == ENUM_PASSPNT_TYPE.E_PASSPNT_SLOWDOWN:
				strPassPntType = 'S'
			if eCurPassPntType == ENUM_PASSPNT_TYPE.E_PASSPNT_STOP:
				strPassPntType = 'P'

			strText = '{0} {1}km/h {2}'.format(strCallsign, int(pFlightPlan.getCurSpd()*3.6), strPassPntType)
			ax1.text(cguCurPos.x, cguCurPos.y, strText, family='serif', style='italic', ha='right', wrap=True)
			LineList.append(Objline)

		ax1.legend(loc='upper right')

		return LineList

	def showTaxiData(self, ax):
		pass

	def showData(self):
		self._resetFlightPlanData()
		fig = plt.figure()
		xMin,xMax,yMin,yMax = self._getMaxMinLim()
		fig.add_subplot(1, 1, 1, xlim=(xMin, xMax), ylim=(yMin, yMax))
		fig.canvas.mpl_connect('button_press_event', self.onClick)
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

	##iIndex 决定颜色
	def showTaxData(self, ax, CugPosLst,callSign):
		if self.callSignDic.get(callSign) != None:
			color = self.callSignDic.get(callSign)
		else:
			delLst=[]
			colorLst = copy.deepcopy(self.colorLst)
			for i in range(len(colorLst)):
				for k in self.callSignDic:
					if colorLst[i] == self.callSignDic.get(k):
						delLst.append(colorLst[i])
			##去重
			delLst = list(UtilityTool.cleardump(delLst))
			for i in range(len(delLst)):
				colorLst.remove(delLst[i])
			if len(colorLst) == 0:
				color = 'blue'
			else:
				k = random.randint(0, 1000) % len(colorLst)
				color = colorLst[k]
			self.callSignDic.setdefault(callSign, color)

		ax1 = ax
		xLst = []
		yLst = []
		for i in range(len(CugPosLst)):
			stCugPos = CugPosLst[i]
			xLst.append(stCugPos.x)
			yLst.append(stCugPos.y)
			##'y-':黄色直线
			# plot(x, y, color='green', linestyle='dashed', marker='o',
			#      markerfacecolor='blue', markersize=12).
			# ax1.plot(xLst, yLst, '{0}-.'.format(colorLst[iOrder]), lw=1)
			ax1.plot(xLst, yLst, color = color, linestyle = '-.',lw=1)