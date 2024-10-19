from functools import partial

from draw import *

curr_state = {
	"bot_loc": CartVertex2D(9,-14), 
	"bot_pose": PolarVertex2D(0.5,90),
	"tag_loc": CartVertex2D(2,-1),
	"tag_pose": PolarVertex2D(0.3,90),
	"frame":0,
}

def strategy_angle_simple(state):
	speed = state["bot_loc"].get_distance(state["tag_loc"]) / 10 + 0.1
	x_translate = state["bot_loc"].x + (state["bot_loc"].x - state["tag_loc"].x) * 2
	
	angle = state["tag_loc"].asPolar().addVector(CartVertex2D(-x_translate, -state["bot_loc"].y)).asPolar().a
	angle = (angle + state["bot_pose"].a)/2
	print(f" from {state['bot_loc'].asPolar()} to {state['tag_loc'].asPolar()} got angle {angle:.3f}") 
	return PolarVertex2D(speed, angle)

ani = FuncAnimation(fig, partial(animate_nonholonomic, state=curr_state, strategy=strategy_angle_simple), interval=300)

run()
