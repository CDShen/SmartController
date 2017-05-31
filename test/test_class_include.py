class A(object):
	def __init__(self):
		self.dData = None
	def doWork(self):
		print ('Start Work Flag={0}'.format(self.dData))
	def setVal(self, dData):
		self.dData = dData




class B(object):
	conponent = None
	def __init__(self, a):
		self.a = a
	def doWork(self):
		self.a.doWork()



a = A()

b = B(a)
a.setVal(10)
b.doWork()
c =B(a)
c.doWork()



