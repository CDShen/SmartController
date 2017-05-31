class TestStaticMethod(object):
	dTheta = None
	@classmethod
	def doWork(cls):
		print ('dTheta ={0}'.format(TestStaticMethod.dTheta))

	@staticmethod	
	def doWorkStatic():
		print ('dTheta ={0}'.format(TestStaticMethod.dTheta))




class B(object):
	def doWork(self):
		TestStaticMethod.doWorkStatic()

# TestStaticMethod.dTheta = 0.90
# b = B()
# b.doWork()






