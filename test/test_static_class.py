class TestClass(object):
	def funMethod(self):
		print ('good data')

	@classmethod
	def ClassMethod(cls):
		print ('classMethod')

	@staticmethod
	def Staticmethod():
		print ('StaticMethod')


a = TestClass()
a.funMethod()
a.ClassMethod()
TestClass.Staticmethod()
TestClass.ClassMethod()