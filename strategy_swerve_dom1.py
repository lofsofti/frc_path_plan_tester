from functools import partial
import math
from draw import *

curr_state = {
	#"bot_loc": CartVertex2D(9,-14), 
	"bot_loc": CartVertex2D(6,-17), 
	"bot_pose": PolarVertex2D(0.5,130),
	"tag_loc": CartVertex2D(2,-1),
	"tag_pose": PolarVertex2D(0.3,90),
	"frame":0,
}

def strategy_simple(state):
	x = (state["tag_loc"].asCart().x - state["bot_loc"].asCart().x) * 0.025
	if x > 0:
		x = math.sqrt(x)
	elif x < 0:
		x = -math.sqrt(-x)
	y = (state["tag_loc"].asCart().y - state["bot_loc"].asCart().y) * 0.25
	speed = state["bot_loc"].get_distance(state["tag_loc"]) / 10 +0.1
	angle = state["tag_loc"].asPolar().addVector(CartVertex2D(-state["bot_loc"].x, -state["bot_loc"].y)).asPolar().a
	rotation = ( state["tag_pose"].asPolar().a - state["bot_pose"].asPolar().a) * 0.2
	print(f" from {state['bot_loc'].asPolar()} to {state['tag_loc'].asPolar()} got angle {angle:.3f} rotation {rotation}")
	#return PolarVertex2D(speed, angle), rotation
	return CartVertex2D(x,y), rotation

ani = FuncAnimation(fig, partial(animate_holonomic, state=curr_state, strategy=strategy_simple), interval=300)

run()
