from functools import partial

from draw import *

curr_state = {
	"bot_pos": CartVertex2D(9,-14), 
	"bot_dir": PolarVertex2D(0.5,90),
	"tag_loc": CartVertex2D(2,-1),
	"tag_pose": PolarVertex2D(0.3,90),
	"frame":0,
}

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

def strategy_simple_smooth(state):
	speed = state["bot_pos"].get_distance(state["tag_loc"]) / 10 + 0.1
	angle = state["tag_loc"].asPolar().addVector(CartVertex2D(-state["bot_pos"].x, -state["bot_pos"].y)).asPolar().a
	angle = (angle + state["bot_dir"].a)/2
	print(f" from {state['bot_pos'].asPolar()} to {state['tag_loc'].asPolar()} got angle {angle:.3f}") 
	return PolarVertex2D(speed, angle)

ani = FuncAnimation(fig, partial(animate, state=curr_state, strategy=strategy_simple_smooth), interval=300)
plt.show()
