from functools import partial
from functools import partial

from draw import *
	
curr_state = {
	"bot_loc": CartVertex2D(8,-12), 
	"bot_pose": PolarVertex2D(0.5,130),
	"tag_loc": CartVertex2D(2,-1),
	"tag_pose": PolarVertex2D(0.3,90),
	"frame":0,
}

p1 = curr_state["bot_loc"]
p2 = CartVertex2D(6, -10)
p3 = CartVertex2D(4, -4)
p4 = curr_state["tag_loc"]

def calc_bezier(t, p1, p2, p3, p4):
	#print(f"{((1.0 - t) ** 3.0)} {((3.0 * t * ((1.0 - t) ** 2.0)))} {(3.0 * (t * t) * (1.0 - t))} {(t ** 3)}")
	return (((1.0 - t) ** 3.0) * p1
		+ 3.0 * t * ((1.0 - t) ** 2.0) * p2 
		+ 3.0 * (t * t) * (1.0 - t) * p3
		+ (t ** 3) * p4)

def home_point(target, curr, max_speed):
	target = target.asCart()
	curr = curr.asCart()
	x = target.x - curr.x
	x = min(max(x, -max_speed), max_speed)
	y = min(max(target.y - curr.y, -max_speed), max_speed)
	return CartVertex2D(x, y)


def strategy_simple(state):
	t = min(max(0.0, float(state["frame"]) / 75.0), 1.0)
	x = calc_bezier(t, p1.x, p2.x, p3.x, p4.x)
	y = calc_bezier(t, p1.y, p2.y, p3.y, p4.y)
	target = CartVertex2D(x, y)
	angle = state["tag_loc"].asPolar().addVector(CartVertex2D(-state["bot_loc"].x, -state["bot_loc"].y)).asPolar().a
	rotation = ( state["tag_pose"].asPolar().a - state["bot_pose"].asPolar().a) * t
	print(f" from {state['bot_loc'].asPolar()} to {state['tag_loc'].asPolar()} got angle {angle:.3f} rotation {rotation:.3f}")
	print(f"t: {t:.3f}   {target} - {state['bot_loc']} => {target.asPolar().diffVector(state['bot_loc']).asCart()}")
	return home_point(target, state["bot_loc"], 1.0), rotation

ani = FuncAnimation(fig, partial(animate_holonomic, state=curr_state, strategy=strategy_simple), interval=30)

run()
