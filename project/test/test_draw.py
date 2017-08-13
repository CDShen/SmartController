# 导入 matplotlib 的所有内容（nympy 可以用 np 这个名字来使用）
#from pylab import *
import matplotlib.pyplot as plt
import numpy as npx

x = [1,2,3,4,5,6,7,8]
y = [1,2,3,4,5,5,5,4]

plt.figure(figsize=(100,10))

#画图
plt.plot(x,y) #默认
plt.plot([9.10,11,12],[9.9,9,9])
#所有绘图对象
plt.show()





