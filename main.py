from project.src.smartControllerAPP import SmartControllerAPP
from project.public.config import ConfigReader
from project.utility import fileTool
def mainApp():
	##首先读取配置文件
	##读取配置文件
	if ConfigReader.loadConfig() == False:
		print('读取配置文件失败')
		return False

	##根据训练计划组数进行训练
	iFileCount = fileTool.find_file_num(ConfigReader.strTrainDataPath)

	for i in range(iFileCount):
		theApp =  SmartControllerAPP()
		if theApp.init(i) == False:
			print ('程序初始化错误')

		theApp.run()
		print('train process {0}/{1}'.format(i+1,iFileCount))


if __name__=='__main__':
	mainApp()