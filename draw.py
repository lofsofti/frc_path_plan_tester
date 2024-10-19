
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
from dataclasses import dataclass, field\

def run():
	plot_ticks = 1
	plot_axis = [
		-10, # min x
		10, # max y
		-18, # min y
		0, # max y
	]
	plt.axis(plot_axis)
	plt.xticks(range(plot_axis[0],plot_axis[1],plot_ticks))
	plt.yticks(range(plot_axis[2],plot_axis[3],plot_ticks))
	plt.grid(True)
	plt.show()


@dataclass(eq=True)
class PolarVertex2D:
	r: float
	a: float
	
	def get_distance(self, p2):
		cp1 = self.asCart()
		cp2 = p2.asCart()
		return math.sqrt(math.pow(cp1.x-cp2.x, 2)+math.pow(cp1.y-cp2.y, 2))
	def asCart(self, x_off=0.0, y_off=0.0):
		return  CartVertex2D(self.r * math.cos(math.radians(self.a))+x_off, self.r * math.sin(math.radians(self.a))+y_off)
	def asPolar(self):
		return self
	def add_r(self, dist: float):
		return PolarVertex2D(self.r+dist, self.a)
	def addVector(self, vector):
		m = self.asCart()
		v = vector.asCart()
		return CartVertex2D(m.x+v.x, m.y+v.y).asPolar()
	def diffVector(self, vector):
		m = self.asCart()
		v = vector.asCart()
		return CartVertex2D(m.x-v.x, m.y-v.y).asPolar()
	def __str__(self):
		return f"(r:{self.r:.1f}, a:{self.a:.1f})"
	def __format__(self, format_spec):
		return self.__str__()

@dataclass(eq=True)
class CartVertex2D:
	x: float
	y: float
	#polar: PolarVertex2D = field(init=False)
	
	def get_distance(self, p2):
		cp1 = self
		cp2 = p2.asCart()
		return math.sqrt(math.pow(cp1.x-cp2.x, 2)+math.pow(cp1.y-cp2.y, 2))
	def asPolar(self):
		if self.x == 0.0:
			if self.y < 0.0:
				return PolarVertex2D(-self.y, 270)
			else:
				return PolarVertex2D(self.y, 90)
		elif self.x >= 0.0 and self.y < 0.0:
			adjust = 2*math.pi
		elif self.x >= 0.0 and self.y >= 0.0:
			adjust = 0
		else:
			adjust = math.pi
		return PolarVertex2D(math.sqrt(math.pow(self.x,2)+math.pow(self.y,2)), math.degrees(math.atan(self.y/self.x)+adjust))
	def asCart(self):
		return self
	def addVector(self, vector):
		v = vector.asCart()
		return CartVertex2D(self.x+v.x, self.y+v.y)
	def get_distance(self, p2):
		cp2 = p2.asCart()
		return math.sqrt(math.pow(self.x-cp2.x, 2)+math.pow(self.y-cp2.y, 2))
	def __str__(self):
		return f"(x:{self.x:.3f}, y:{self.y:.3f})"

fig = plt.figure(figsize=(15,15))


def draw_vect(plt, offset, vect, c, head=0.1, alpha=None):
	start_point = offset.asCart()
	arrow_point = vect.asCart()
	plt.arrow(start_point.x, start_point.y, arrow_point.x, arrow_point.y, fc=c, ec=c, head_width=head, head_length=0.1,length_includes_head=True,alpha=alpha)



def draw_bot(plt, location, velocity):
	print(f"bot at {location} heading {velocity}")
	center_point = location.asCart()
	center_pointp = location.asPolar()
	heading_point = PolarVertex2D(0.5, velocity.a).asCart()
	velocity_point = heading_point.addVector(velocity).asCart()
	velocity_pointp = velocity_point.asPolar()
	front_right = center_pointp.addVector(PolarVertex2D(0.5, velocity_pointp.a + 40.1)).asCart()
	front_left = center_pointp.addVector(PolarVertex2D(0.5, velocity_pointp.a - 40.1)).asCart()
	back_right = center_pointp.addVector(PolarVertex2D(-0.5, velocity_pointp.a - 40.1)).asCart()
	back_left = center_pointp.addVector(PolarVertex2D(-0.5, velocity_pointp.a + 40.1)).asCart()
	#print(f"bot fr: {front_right} fl: {front_left}")
	#print(f"heading_point:{heading_point.asPolar()} velocity_pointp:{velocity_pointp}")
	plt.plot([front_right.x, front_left.x], [front_right.y, front_left.y], color='g')
	plt.plot([front_left.x, back_left.x], [front_left.y, back_left.y], color='k')
	plt.plot([back_left.x, back_right.x], [back_left.y, back_right.y], color='r')
	plt.plot([back_right.x, front_right.x], [back_right.y, front_right.y], color='k')
	plt.arrow(center_point.x, center_point.y, heading_point.x, heading_point.y, fc='b', ec='b', head_width=0.06, head_length=0.1,length_includes_head=True,alpha=0.3)
	plt.arrow(center_point.x, center_point.y, velocity_point.x, velocity_point.y, fc='r', ec='r', head_width=0.12, head_length=0.2,length_includes_head=True,alpha=0.4)

def draw_tag(plt, location, pose):
	p1 = location.addVector(PolarVertex2D(pose.r, pose.a+90)).asCart()
	p2 = location.addVector(PolarVertex2D(pose.r, pose.a-90)).asCart()
	plt.plot([p1.x, p2.x], [p1.y, p2.y], color='g')


def animate_holonomic(i, state, strategy):
	tag_dist = state["bot_loc"].get_distance(state["tag_loc"])
	# stop simulation if at target or off the field
	if state["bot_loc"].y > 0 or tag_dist > 25 or tag_dist < 0.5 or state["frame"]  > 100:
		return
	state["frame"] = state["frame"] + 1
	# update bot location
	if "bot_req_dir" in state:
		state["bot_loc"] = state["bot_loc"].addVector(state["bot_req_dir"])
	# set new heading
	if "bot_req_rot" in state:
		new_rot = state["bot_pose"].asPolar()
		new_rot.r = state["bot_req_rot"].asPolar().r
		state["bot_pose"] = new_rot
	
	# store/scale new input 
	dir, rot = strategy(state)
	if "bot_req_rot" in state:
		pose = state["bot_pose"].asPolar()
		last_rot = state["bot_req_rot"].asPolar()
		new_rot = rot.asPolar()
		if last_rot.a - new_rot.a > math.pi/8.0:
			new_rot.a = last_rot.a - math.pi/8.0
		elif new_rot.a - last_rot.a > math.pi/8.0:
			new_rot.a = last_rot.a + math.pi/8.0
		pose.a = pose.a + new_rot.a 
		state["bot_pose"] = pose
	if "bot_req_dir" in state:
		last_dir = state["bot_req_dir"].asPolar()
		new_dir = dir.asPolar()
		if last_dir.a - new_dir.a > math.pi/4.0:
			new_dir.a = last_dir.a - math.pi/4.0
			new_dir = state["bot_pose"]
		elif new_dir.a - last_dir.a > math.pi/4.0:
			new_dir.a = last_dir.a + math.pi/4.0
			new_dir = state["bot_pose"]
	state["bot_req_dir"] = dir
	state["bot_req_rot"] = rot
	draw_tag(plt, state["tag_loc"], state["tag_pose"])
	draw_bot(plt, state["bot_loc"], state["bot_pose"])

def animate_nonholonomic(i, state, strategy):
	tag_dist = state["bot_loc"].get_distance(state["tag_loc"])
	if state["bot_loc"].y > 0 or tag_dist > 25 or tag_dist < 0.5 or state["frame"]  > 100:
		return
	state["frame"] = state["frame"] + 1
	# update bot location
	state["bot_loc"] = state["bot_loc"].addVector(state["bot_pose"])
	# set new heading
	state["bot_pose"] = strategy(state)
	draw_tag(plt, state["tag_loc"], state["tag_pose"])
	draw_bot(plt, state["bot_loc"], state["bot_pose"])