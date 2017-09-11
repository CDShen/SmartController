class A(object):
	def __init__(self):
		self.dData = None
	def doWork(self):
		self.setVal(10)
		print ('Start Work Flag={0}'.format(self.dData))



	def setVal(self, dData):
		self.dData = dData




A().doWork()
