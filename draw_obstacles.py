import sys, os
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from scipy import spatial
import datetime

COORD_PRECISION = 25.0

def usage():
	print("Usage: python draw_obstacles.py goal_x goal_y")

def export(drawer):
	timestamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
	filename = "world_obstacles_"+timestamp+".txt"
	num_obstacles = len(drawer.obs_list)
	if not num_obstacles:
		print('No obstacles to export.')
		return
	with open(filename, 'w') as file:
		file.write(str(num_obstacles)+'\n')
		for i in range(num_obstacles):
			num_verts = len(drawer.obs_list[i])
			file.write(str(num_verts)+'\n')
			for j in range(num_verts):
				file.write(str(drawer.obs_list[i][j][0])+' '+str(drawer.obs_list[i][j][1])+'\n')
	print('Wrote', str(num_obstacles), 'obstacles to file', filename)



class Drawer():
	def __init__(self, ax):
		self.ax = ax
		self.fig = ax.get_figure()
		self.cid = fig.canvas.mpl_connect('button_press_event', self)

		self.new_obs = True
		self.obs_list = []

		self.curr_obs = []
		self.curr_line,  = self.ax.plot([], [])
		self.guide_point,  = self.ax.plot([], [], marker='.', color='b')

	def __call__(self, event):
		if event.inaxes!=self.ax: return

		raw_coord = [event.xdata, event.ydata]
		round_coord = self.round_coord(raw_coord)

		if self.new_obs:
			# start new figure
			self.new_obs = False
			self.curr_obs = [round_coord]
			self.curr_line.set_data(np.array(self.curr_obs)[:,0], np.array(self.curr_obs)[:, 1])
			self.guide_point.set_data(round_coord[0], round_coord[1])
		else:
			if self.curr_obs[0] == round_coord:
				# closed figure
				self.curr_line.set_data([], [])

				# enforce convex obstacles
				self.curr_obs = np.array(self.curr_obs)
				convex_hull = spatial.ConvexHull(self.curr_obs)
				self.curr_obs = self.curr_obs[convex_hull.vertices]

				self.ax.add_patch(matplotlib.patches.Polygon(self.curr_obs, closed=True))
				self.obs_list.append(self.curr_obs.tolist())
				self.new_obs = True
			else:
				# continue drawing figure
				self.curr_obs.append(round_coord)
				self.curr_line.set_data(np.array(self.curr_obs)[:,0], np.array(self.curr_obs)[:, 1])
				self.guide_point.set_data([], [])

		self.fig.canvas.draw()



	def round_coord(self, coord):
		nd = np.array(coord)
		nd = np.round(nd / COORD_PRECISION) * COORD_PRECISION
		nd = nd.astype(int)
		return nd.tolist()


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

	export(drawer)