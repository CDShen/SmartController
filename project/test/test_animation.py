import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

#first set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax1 = fig.add_subplot(1, 1 ,1 ,xlim=(0, 200), ylim=(0, 200))
line,  = ax1.plot([], [], 'o',label = 'good',lw=1)
ax1.legend(loc = 'upper right')
ax1.set_title('airport')

# dot  = ax1.scatter(1,1)

# animation function.  this is called sequentially
def animate(iFrame):
	# x = np.linspace(0, 2, 100)
	# y = np.sin(2 * np.pi * (x - 0.01 * iFrame))
	ax1.cla()
	ax1.set_ylim(0,200)
	ax1.set_xlim(0, 200)
	line, = ax1.plot([], [], 'o', label='good{0}'.format(iFrame), lw=1)
	line1, = ax1.plot([], [], 'o', label='bad{0}'.format(iFrame), lw=1)

	ax1.legend(loc='upper right')
	ax1.set_title('airport')
	x = iFrame
	y = iFrame
	line.set_data(x,y)
	line1.set_data(x+5,y+5)
	# ax1.text(x, y, str((1, 1)), family='serif', style='italic', ha='right', wrap=True)
	ax1.text(x, y, str((1, 1)), family='serif', style='italic', ha='right', wrap=True)
	ax1.text(x+5, y+5, str((2, 2)), family='serif', style='italic', ha='right', wrap=True)

	return line,line1


# anim1 = animation.FuncAnimation(fig, animate, init_func=init, frames=50, interval=1000)
anim1 = animation.FuncAnimation(fig, animate, frames=200, interval=1000)
plt.show()