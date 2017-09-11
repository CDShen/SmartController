"""
通用函数
目前有算出过点时间和判断是否和计划集合有冲突

"""

print (__doc__)

from math import *
from ..public.dataObj import *
from ..public.scenarioDataObj import *
##DataManager相互包含后续修改
# from ..public.dataManage import DataManager
from ..public.config import ConfigReader
import copy


class MathUtilityTool(object):
    @classmethod
    def distance(cls, CguPos1, CguPos2):
        dis = sqrt(pow((CguPos1.x - CguPos2.x),2) +  pow((CguPos1.y - CguPos2.y),2))
        return dis
    @classmethod
    def GetUnitVec(cls, CguPos1):
        dis = MathUtilityTool.distance(CguPos1, CguPos(0, 0))
        return CguPos(CguPos1.x/dis, CguPos1.y/dis)

    @classmethod
    def isInsect(cls, num1Start, num1End, num2Start, num2End):
        if num2End < num1Start or num2Start > num1End:
            return  False
        else:
            return  True

    @classmethod
    def getUnitVec(cls,CguPosS,CguPosE):
        dis = MathUtilityTool.distance(CguPosS, CguPosE)
        CguVec = CguPos(CguPosE.x - CguPosS.x, CguPosE.y - CguPosS.y)
        return CguPos(CguVec.x/dis, CguVec.y/dis)

    @classmethod
    def getPosBySpdTime(cls, CguPosS, CguPosE, iTime, dSpd, ePassTYPE):
        cguData = CguPos(0,0)
        cguVec = MathUtilityTool.getUnitVec(CguPosS, CguPosE)
        dis = iTime * dSpd
        cguData.x = CguPosS.x + dis*cguVec.x
        cguData.y = CguPosS.y + dis*cguVec.y
        dCurSpd = dSpd
        if ePassTYPE == ENUM_PASSPNT_TYPE.E_PASSPNT_STOP:
            cguStop = CguPos(0,0)
            cguStop.x = CguPosE.x - ConfigReader.dSafeDis * cguVec.x
            cguStop.y = CguPosE.y - ConfigReader.dSafeDis * cguVec.y
            cguVecStop = MathUtilityTool.getUnitVec(cguData, cguStop)
            dFlag = cguVecStop.x*cguVec.x + cguVecStop.y*cguVec.y
            ##反向
            if dFlag <= 0.0:
                cguData = cguStop
                dCurSpd = 0.0

        return cguData,dCurSpd

class UtilityTool(object):
    dTheta = None
    pDataManager = None
    ##队列去重
    @classmethod
    def cleardump(cls, items):
        seen = set()
        for item in items:
            if item not in seen:
                yield item
                seen.add(item)

    # brief:解决冲突并返回冲突后的路径，只考虑改变冲突路线的方式
    # curFPPathData:[in] 当前计划滑行路线
    # conFPPathData:[in] 冲突滑行路线
    # ConflictData:[in] 冲突数据
    # return newPath:[out] 解决后新的滑行路线
    # warning
    @classmethod
    def resolveConflict(cls, curFPathData, conFPPathData ,ConflictData):
        newPath = copy.deepcopy(conFPPathData)
        ##清空lst
        newPath.vFPPassPntData = []
        iConFixID = ConflictData.iConflictFixID
        iFirstStartIndex = -1
        iSecondStartFixIDIndex = -1

        for i in range(len(curFPathData.vFPPassPntData)):
            if curFPathData.vFPPassPntData[i].iFixID == iConFixID:
                iFirstStartIndex = i
                break

        for i in range(len(curFPathData.vFPPassPntData)):
            if conFPPathData.vFPPassPntData[i].iFixID == iConFixID:
                iSecondStartFixIDIndex = i
                break
        ##查找到最开始的公共冲突点
        j=1
        iFirstCommonStartIndex = iFirstStartIndex
        iSecCommonStartIndex = iSecondStartFixIDIndex
        for i in range(iFirstStartIndex+1, len(curFPathData.vFPPassPntData)):
            if iSecondStartFixIDIndex - j < 0:
                break

            if curFPathData.vFPPassPntData[i].iFixID == conFPPathData.vFPPassPntData[iSecondStartFixIDIndex-j].iFixID:
                iFirstCommonStartIndex = i
                iSecCommonStartIndex = iSecondStartFixIDIndex-j
                j += 1
            else:
                break

        if iSecCommonStartIndex == 0:
            print('Error:不会出现初始点冲突情况')
        ##获得公共节点的过点时间
        iCommonConPassPntTime = curFPathData.vFPPassPntData[iFirstCommonStartIndex].iRealPassTime
        iDiffTime = -1
        for i in range(len(conFPPathData.vFPPassPntData)):
            if i < iSecCommonStartIndex:
                newPath.vFPPassPntData.append(copy.deepcopy(conFPPathData.vFPPassPntData[i]))
            elif i == iSecCommonStartIndex:
                stFPPassPntData = copy.deepcopy(conFPPathData.vFPPassPntData[i])
                iOrgTime = conFPPathData.vFPPassPntData[i].iRealPassTime
                ##时间可能有问题，待修改
                iNewTime = iCommonConPassPntTime + ConfigReader.iResolveConfilictTime
                iDiffTime = iNewTime - iOrgTime
                stFPPassPntData.iRealPassTime = iNewTime ##默认添加20s
                newPath.vFPPassPntData.append(stFPPassPntData)
            else:
                stFPPassPntData = copy.deepcopy(conFPPathData.vFPPassPntData[i])
                stFPPassPntData.iRealPassTime += iDiffTime
                newPath.vFPPassPntData.append(stFPPassPntData)
        return newPath

    ##Q学习解决动作方式
    @classmethod
    def resolveConflictByAction(cls, curFPathData, conFPPathData ,ConflictData, eActionType):
        newPath = copy.deepcopy(curFPathData)
        ##清空lst
        newPath.vFPPassPntData = []
        iConFixID = ConflictData.iConflictFixID
        iFirstStartIndex = -1
        iSecondStartFixIDIndex = -1
        for i in range(len(curFPathData.vFPPassPntData)):
            if curFPathData.vFPPassPntData[i].iFixID == iConFixID:
                iFirstStartIndex = i
                break

        for i in range(len(curFPathData.vFPPassPntData)):
            if conFPPathData.vFPPassPntData[i].iFixID == iConFixID:
                iSecondStartFixIDIndex = i
                break

        if iFirstStartIndex == 0:
            print('Error:Q学习中不会出现初始点冲突情况')
        ##查找到最开始的公共冲突点
        j=1
        iFirstCommonStartIndex = iFirstStartIndex
        iSecCommonStartIndex = iSecondStartFixIDIndex
        for i in range(iSecondStartFixIDIndex+1, len(conFPPathData.vFPPassPntData)):
            if iFirstStartIndex - j < 0:
                break

            if curFPathData.vFPPassPntData[iFirstStartIndex-j].iFixID == conFPPathData.vFPPassPntData[i].iFixID:
                iFirstCommonStartIndex = iFirstStartIndex-j
                j += 1
                iSecCommonStartIndex = i
            else:
                break

        if iFirstCommonStartIndex == 0:
            print ('Error:Q学习中不会出现初始点冲突情况')
        ##获得公共节点的过点时间
        dTotalDis = 0.0
        iCommonConPassPntTime = curFPathData.vFPPassPntData[iFirstCommonStartIndex].iRealPassTime
        iDiffTime = -1
        for i in range(len(curFPathData.vFPPassPntData)-1):
            if i < iFirstCommonStartIndex:
                cguPos1 = CguPos(curFPathData.vFPPassPntData[i].x, curFPathData.vFPPassPntData[i].y)
                cguPos2 = CguPos(curFPathData.vFPPassPntData[i+1].x, curFPathData.vFPPassPntData[i+1].y)
                dTotalDis += MathUtilityTool.distance(cguPos1, cguPos2)

        if eActionType == ENUM_QACTION_TYPE.E_ACTION_SLOWDOWN:
            dDis = (dTotalDis-ConfigReader.dSafeDis)
            iTime = curFPathData.vFPPassPntData[iFirstCommonStartIndex].iRealPassTime - \
                    curFPathData.vFPPassPntData[0].iRealPassTime + ConfigReader.iResolveConfilictTime
            dSpd = dDis/iTime
            ##减速每段增加时间
            ##iSlowTime = ConfigReader.iResolveConfilictTime / iFirstCommonStartIndex
            iSlowTime = ConfigReader.iResolveConfilictTime / iFirstCommonStartIndex
            if dSpd < ConfigReader.dSlowMinSpd:
                print('warning:Q学习中减速动作速度小于最小阈值={0} m/s，冲突位置序号={1}'.format(ConfigReader.dSlowMinSpd, iFirstCommonStartIndex+1))
                return None
            else:
                for i in range(len(curFPathData.vFPPassPntData)):
                    if i == 0:
                        newPath.vFPPassPntData.append(copy.deepcopy(curFPathData.vFPPassPntData[i]))
                    elif i <= iFirstCommonStartIndex and i>0:
                        stFPPrePassPntData = copy.deepcopy(newPath.vFPPassPntData[i-1])
                        stFPPassPntData = copy.deepcopy(curFPathData.vFPPassPntData[i])
                        dRoadDis = MathUtilityTool.distance(CguPos(stFPPrePassPntData.x, stFPPrePassPntData.y), CguPos(stFPPassPntData.x, stFPPassPntData.y))
                        dTime = dRoadDis/dSpd
                        stFPPassPntData.iRealPassTime = stFPPrePassPntData.iRealPassTime + dTime
                        stFPPassPntData.ePassPntType = ENUM_PASSPNT_TYPE.E_PASSPNT_SLOWDOWN
                        newPath.vFPPassPntData.append(stFPPassPntData)
                    else:
                        stFPPassPntData = copy.deepcopy(curFPathData.vFPPassPntData[i])
                        stFPPassPntData.iRealPassTime = curFPathData.vFPPassPntData[i].iRealPassTime + ConfigReader.iResolveConfilictTime
                        newPath.vFPPassPntData.append(stFPPassPntData)


        elif eActionType == ENUM_QACTION_TYPE.E_ACTION_STOP:
            for i in range(len(curFPathData.vFPPassPntData)):
                if i < iFirstCommonStartIndex:
                    newPath.vFPPassPntData.append(copy.deepcopy(curFPathData.vFPPassPntData[i]))
                else:
                    stFPPassPntData = copy.deepcopy(curFPathData.vFPPassPntData[i])
                    stFPPassPntData.iRealPassTime = curFPathData.vFPPassPntData[i].iRealPassTime + ConfigReader.iResolveConfilictTime
                    if i == iFirstCommonStartIndex:
                        stFPPassPntData.ePassPntType = ENUM_PASSPNT_TYPE.E_PASSPNT_STOP
                    newPath.vFPPassPntData.append(stFPPassPntData)

        return newPath

    ##是否最初冲突时在起点
    @classmethod
    def isConflictAtStart(cls, curFPathData, conFPPathData, ConflictData):
        bIsConAtStart = False
        newPath = copy.deepcopy(conFPPathData)
        ##清空lst
        newPath.vFPPassPntData = []
        iConFixID = ConflictData.iConflictFixID
        iFirstStartIndex = -1
        iSecondStartFixIDIndex = -1

        for i in range(len(curFPathData.vFPPassPntData)):
            if curFPathData.vFPPassPntData[i].iFixID == iConFixID:
                iFirstStartIndex = i
                if iFirstStartIndex == 0:
                    return True
        return bIsConAtStart

    # brief:解决冲突并返回冲突后的路径滑行时间
    # iStartTime:[in] 当前开始滑行时间
    # FPPathData:[in] 冲突滑行路线
    # return 返回滑行时间
    @classmethod
    def getTotalFPTaxiTime(cls, iStartTime, FPPathData):
        return  FPPathData.vFPPassPntData[len(FPPathData.vFPPassPntData)-1].iRealPassTime - iStartTime

    # brief:计划滑行路径总时间
    # PathData:[in] 当前计划滑行路线
    # return 返回滑行时间
    @classmethod
    def getTotalPathTaxiTime(cls,PathData):
        return PathData.vPassPntData[len(PathData.vPassPntData)-1].iRelaPassTime

    @classmethod
    def getConflictType(cls, cguPos1_1,cguPos1_2, cguPos2_1, cguPos2_2):
        eConflictType = None

        vecPos1 = MathUtilityTool.getUnitVec(cguPos1_1, cguPos1_2)
        vecPos2 = MathUtilityTool.getUnitVec(cguPos2_1, cguPos2_2)

        val = (vecPos1.x * vecPos2.x + vecPos1.y * vecPos2.y)/(1.0)
        theta = (180.0 / pi * acos(val))
        if theta < 30.0 and theta > 0:
            eConflictType = E_CONFLICT_TYPE.E_CONFLICT_CONS
        elif theta <= 150.0 and theta >= 30.0:
            eConflictType = E_CONFLICT_TYPE.E_CONFLICT_CROSS
        else:
            eConflictType = E_CONFLICT_TYPE.E_CONFLICT_OPP

        return  eConflictType

    ##如果在初始点发生冲突则需要等待
    @classmethod
    def transPathData2FPPathData(self, iStartTime, PathData , iWaitTime = 0):
        vstFPPassPntData = []
        for i in range(len(PathData.vPassPntData)):
            stFixPointData = self.pDataManager.getFixPointByID(PathData.vPassPntData[i].iFixID)
            stFPPassPntData = FPPassPntData(stFixPointData.iID,iStartTime + PathData.vPassPntData[i].iRelaPassTime,\
                            stFixPointData.dX, stFixPointData.dY,ENUM_PASSPNT_TYPE.E_PASSPNT_NORMAL)
            vstFPPassPntData.append(stFPPassPntData)
        stFPPathData = FPPathData(PathData.iPathID, vstFPPassPntData)
        return  stFPPathData

    @classmethod
    def covertLonLat2XY(cls,  pos,  center):
        r = 6371000## 地球半径
        pos_xy = CguPos(0,0)
        delta_longitude = pos.x - center.x
        tmp = sin(pos.y) * sin(center.y) + cos(pos.y) * cos(center.y) * cos(delta_longitude)
        pos_xy.x = (r * cos(pos.y) * sin(delta_longitude)) / tmp
        pos_xy.y = (r * (sin(pos.y) * cos(center.y) - cos(pos.y) * sin(center.y) * cos(delta_longitude))) / tmp
        return  pos_xy

    @classmethod
    def convertXY2LatLong( pos_xy,  center):
        r = 6371000 ## 地球半径
        pos_xy.x = pos_xy.x / r
        pos_xy.y = pos_xy.y / r

        temp = sqrt(pos_xy.x * pos_xy.x + pos_xy.y * pos_xy.y)
        if temp > -0.0 and temp < 0.0:
            return center

        c = atan(temp)
        pos_latlong = CguPos(0,0)
        pos_latlong.y = asin(cos(c) * sin(center.y) + pos_xy.y * sin(c) * cos(center.y) / temp)
        pos_latlong.x = center.x + atan(pos_xy.x * sin(c) / (temp * cos(center.y) * cos(c) - pos_xy.y * sin(center.y) * sin(c)))

        return pos_latlong

