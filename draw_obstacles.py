import sys, os
import numpy as np
from matplotlib import pyplot as plt


def usage():
	print("Usage: python draw_obstacles.py goal_x goal_y")

class Drawer():
	def __init__(self, ax):
		self.ax = ax
		fig = ax.get_figure()
		self.cid = fig.canvas.mpl_connect('button_press_event', self)

	def __call__(self, event):
		print('click', event)

if __name__ == "__main__":
	if len(sys.argv) != 3:
		usage()
		sys.exit(0)

	fig, ax = plt.subplots()
	ax.set_xlim(-300, 900)
	ax.set_ylim(-300, 300)
	ax.set_aspect('equal')

	start_coord = [0, 0]
	end_coord = [int(sys.argv[1]), int(sys.argv[2])]

	ax.plot(start_coord[0], start_coord[1], color='g', marker='o')
	ax.plot(end_coord[0], end_coord[1], color='r', marker='o')

	drawer = Drawer(ax)

	plt.show()