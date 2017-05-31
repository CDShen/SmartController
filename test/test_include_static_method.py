
import sys
sys.path.append('..')
from test_static_method import *

TestStaticMethod.dTheta = 0.8
print (TestStaticMethod.dTheta)

TestStaticMethod.doWorkStatic()

b = B()
b.doWork()







