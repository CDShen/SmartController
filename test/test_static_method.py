class TmpStaticMethod(object):
	dTheta = None
	@classmethod
	def doWork(cls):
		print ('dTheta ={0}'.format(1))
		TmpStaticMethod.doWorkStatic()

	@staticmethod
	def doWorkStatic():
		print ('dTheta ={0}'.format(2))


class B(object):
	def doWork(self):
		TmpStaticMethod.doWork()


TmpStaticMethod.dTheta = 0.90
print (TmpStaticMethod.dTheta)
b = B()
b.doWork()






