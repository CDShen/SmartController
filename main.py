from code.src.smartControllerAPP import SmartControllerAPP


def mainApp():
	theApp =  SmartControllerAPP()
	if theApp.init() == False:
		print ('程序初始化错误')

	theApp.run()


if __name__=='__main__':
	mainApp()