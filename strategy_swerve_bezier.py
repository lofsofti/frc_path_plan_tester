from functools import partial
from functools import partial

from draw import *

curr_state = {
	"bot_loc": CartVertex2D(9,-12), 
	"bot_pose": PolarVertex2D(0.5,130),
	"tag_loc": CartVertex2D(2,-1),
	"tag_pose": PolarVertex2D(0.3,90),
	"frame":0,
}

p1 = curr_state["bot_loc"]
p2 = CartVertex2D(8, -2)
p3 = CartVertex2D(3, -6)
p4 = curr_state["tag_loc"]

def calc_bezier(t, p1, p2, p3, p4):
	#print(f"{((1.0 - t) ** 3.0)} {((3.0 * t * ((1.0 - t) ** 2.0)))} {(3.0 * (t * t) * (1.0 - t))} {(t ** 3)}")
	return (((1.0 - t) ** 3.0) * p1
		+ 3.0 * t * ((1.0 - t) ** 2.0) * p2 
		+ 3.0 * (t * t) * (1.0 - t) * p3
		+ (t ** 3) * p4)


def strategy_simple(state):
	dist = state["bot_loc"].get_distance(state["tag_loc"])
	speed = dist / 10 +0.01
	t = min(max(0.0, float(state["frame"]) / 375.0), 1.0)
	#print("t:  ", t)
	#~ print("b1: ",  ((1.0-t)**2.0)*p1.x)
	#~ print("b2: ",  (2.0*t*(1.0-t)**2.0)*p2.x)
	#~ print("b3: ",  3.0*(t**2.0)*p3.x + t**3)
	#~ print("b4: ",  t**3 * p4.x)
	
	x = calc_bezier(t, p1.x, p2.x, p3.x, p4.x)
	y = calc_bezier(t, p1.y, p2.y, p3.y, p4.y)
	target = CartVertex2D(x, y)
	print(f"t: {t}   {target}")
	angle = state["tag_loc"].asPolar().addVector(CartVertex2D(-state["bot_loc"].x, -state["bot_loc"].y)).asPolar().a
	rotation = ( state["tag_pose"].asPolar().a - state["bot_pose"].asPolar().a) * 0.10
	print(f" from {state['bot_loc'].asPolar()} to {state['tag_loc'].asPolar()} got angle {angle:.3f} rotation {rotation}")
	print( target.asPolar().diffVector(state["bot_loc"]).asCart())
	return target.asPolar().diffVector(state["bot_loc"]), rotation

ani = FuncAnimation(fig, partial(animate_holonomic, state=curr_state, strategy=strategy_simple), interval=300)

run()