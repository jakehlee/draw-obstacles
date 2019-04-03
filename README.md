# draw-obstacles
Draw your own obstacles for COMS4733 HW4!

## Getting Started

### Prerequisites
- `python 3`
- `matplotlib`
- `numpy`
- `scipy`

That's it!

## Usage

`python draw_obstacles.py goal_x goal_y`

for example, `python draw_obstacles.py 600 0`

A blank map will pop up. The green dot is the starting point `(0,0)` and the red dot is the goal, in our case, `(600,0)`

Click where you want each vertex of the polygon to be. Once you click on the starting vertex again, the lines will be replaced by a *convex hull* of the vertices you drew. Continue until all obstacles are drawn.

Exit out of the figure with the 'x' button on the top left or top right of the window (do not `ctrl-c`!). The terminal will now print something similar to:

`Wrote 6 obstacles to file world_obstacles_20190403T191907.txt`

The exported file is located in the same directory as the script.
