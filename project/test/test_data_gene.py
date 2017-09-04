import csv
from configparser import ConfigParser
import random
import copy

import os


def delete_file_folder(src):
    '''delete files and folders'''

    if os.path.isfile(src):
        try:
            os.remove(src)
        except:
            pass

            # www.iplaypy.com

    elif os.path.isdir(src):
        for item in os.listdir(src):
            itemsrc = os.path.join(src, item)
            delete_file_folder(itemsrc)
        # try:
        #     os.rmdir(src)
        # except:
        #     pass





class FlyPlanGen(object):
    GroupFlyPlanDataLst = []
    ArrStartFixLst = []
    ArrEndFixLst = []
    DepStartFixLst = []
    DepEndFixLst = []
    CallSignLst = []
    dInterval = 0.0
    iTotalNum = 50
    iGroupNum = 1
    strSavePath  = None

    def readConfig(self):
        cfg = ConfigParser()
        cfg.read('../../flyplanConfig.ini')
        sectionHeaderLst = cfg.sections()

        if len(sectionHeaderLst) == 0:
            return False
        ##获取进港开始点集合
        strParaLst = cfg.get('DataBase', 'ArrStartFixIDSet')
        tmpLst = strParaLst.split(',')
        for i in tmpLst:
            self.ArrStartFixLst.append(int(i))

        ##获取进港结束点集合
        strParaLst = cfg.get('DataBase', 'ArrEndFixIDSet')
        tmpLst = strParaLst.split(',')
        for i in tmpLst:
            self.ArrEndFixLst.append(int(i))

        ##获取离港开始点集合
        strParaLst = cfg.get('DataBase', 'DepStartFixIDSet')
        tmpLst = strParaLst.split(',')
        for i in tmpLst:
            self.DepStartFixLst.append(int(i))

        ##获取离港结束点集合
        strParaLst = cfg.get('DataBase', 'DepEndFixIDSet')
        tmpLst = strParaLst.split(',')
        for i in tmpLst:
            self.DepEndFixLst.append(int(i))


        ##获取可用呼号
        strParaLst = cfg.get('DataBase','CallsignSet')
        tmpLst = strParaLst.split(' ')
        for i in tmpLst:
            self.CallSignLst.append(str(i))

        self.strSavePath = cfg.get('DataBase', 'Path')
        self.dInterval = cfg.getfloat('DataBase', 'Interval')
        self.iTotalNum = cfg.getint('DataBase', 'TotalNum')
        self.iGroupNum = cfg.getint('DataBase', 'GroupNum')

    def geneFlyPlanData(self):
        for i in range(self.iGroupNum):
            FlyPlanDataLst = []
            ##已经使用的呼号下标
            usedCallsignSeqDic = {}
            for j in range(self.iTotalNum):
                oneFlyPlanData = []
                ##产生随机数，如果偶数为进港，基数是离港  1进港 2离港
                k = random.randint(0,1000) % 2
                ##首先取出呼号
                iRanCallsignSeq = random.randint(0,len(self.CallSignLst)-1)
                while usedCallsignSeqDic.get(iRanCallsignSeq) != None:
                    iRanCallsignSeq = random.randint(0, len(self.CallSignLst) - 1)
                usedCallsignSeqDic.setdefault(iRanCallsignSeq, iRanCallsignSeq)
                strCallsign = self.CallSignLst[iRanCallsignSeq]

                if k==0:
                    oneFlyPlanData.append(j+1)
                    oneFlyPlanData.append(strCallsign)
                    oneFlyPlanData.append(1)
                    oneFlyPlanData.append(int(self.dInterval * 60.0 * j))
                    oneFlyPlanData.append(random.choice(self.ArrStartFixLst))
                    oneFlyPlanData.append(random.choice(self.ArrEndFixLst))
                else:
                    oneFlyPlanData.append(j+1)
                    oneFlyPlanData.append(strCallsign)
                    oneFlyPlanData.append(2)
                    oneFlyPlanData.append(int(self.dInterval * 60.0 * j))
                    oneFlyPlanData.append(random.choice(self.DepStartFixLst))
                    oneFlyPlanData.append(random.choice(self.DepEndFixLst))

                FlyPlanDataLst.append(oneFlyPlanData)

            self.GroupFlyPlanDataLst.append(FlyPlanDataLst)
    def save(self):
        delete_file_folder(self.strSavePath[:-1])
        headers = ['ID', 'Callsign', 'FlightType', 'StartTime', 'StartFixID', 'EndFixID']
        for i in range(len(self.GroupFlyPlanDataLst)):
            rows = self.GroupFlyPlanDataLst[i]
            with open(self.strSavePath +'flightplan{0}.csv'.format(i+1), 'w') as f:
                f_csv = csv.writer(f)
                f_csv.writerow(headers)
                f_csv.writerows(rows)


pFlyPlanGene = FlyPlanGen()
pFlyPlanGene.readConfig()
pFlyPlanGene.geneFlyPlanData()
pFlyPlanGene.save()
print ('data create sucessfully')