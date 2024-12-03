from functools import partial
from draw import *

# robo initial location 
curr_state = {
    "bot_loc": CartVertex2D(8, -12),
    "bot_pose": PolarVertex2D(0.5, 130),
    "tag_loc": CartVertex2D(2, -1),
    "tag_pose": PolarVertex2D(0.3, 90),
    "frame": 0,
}

# Bézier control points
# here you can put new points for different curves 
# in an array with indexs starting at 0
curves = [
    {
        # INDEX 0
        "p1": curr_state["bot_loc"],
        "p2": CartVertex2D(9, -10),
        "p3": CartVertex2D(3, -3),
        "p4": curr_state["tag_loc"]
    },
    {
        # INDEX 1
        "p1": curr_state["bot_loc"],
        "p2": CartVertex2D(7, -14),
        "p3": CartVertex2D(4, -2),
        "p4": curr_state["tag_loc"]
    },
    {
        # INDEX 2
        "p1": curr_state["bot_loc"],
        "p2": CartVertex2D(6, -6),
        "p3": CartVertex2D(3, -5),
        "p4": curr_state["tag_loc"]
    },
    {
        # INDEX 3
        "p1": curr_state["bot_loc"],
        "p2": CartVertex2D(6, -10),
        "p3": CartVertex2D(4, -4),
        "p4": curr_state["tag_loc"]
    },
    {
        # INDEX 4
        "p1": curr_state["bot_loc"],
        "p2": CartVertex2D(8, -2),
        "p3": CartVertex2D(3, -6),
        "p4": curr_state["tag_loc"]
    },
    {
        # INDEX 5
        "p1": curr_state["bot_loc"],
        "p2": CartVertex2D(7, -8),
        "p3": CartVertex2D(4, -2),
        "p4": curr_state["tag_loc"]
    },
    {
        # INDEX 6
        "p1": curr_state["bot_loc"],    
        "p2": CartVertex2D(10, -16),
        "p3": CartVertex2D(5, 0),
        "p4": curr_state["tag_loc"]
    }
    ,
    {
        # INDEX 6
        "p1": curr_state["bot_loc"],
        "p2": CartVertex2D(7, -12),
        "p3": CartVertex2D( 9, -3),
        "p4": curr_state["tag_loc"]
    }
]

# curve select  
curve_index = 4 # choose index # for which curve you want to run
selected_curve = curves[curve_index]

# Bézier curve calculation
def calc_bezier(t, p1, p2, p3, p4):
    return (((1.0 - t) ** 3.0) * p1
            + 3.0 * t * ((1.0 - t) ** 2.0) * p2
            + 3.0 * (t ** 2) * (1.0 - t) * p3
            + (t ** 3) * p4)

# calculations from current pos and target pos
def home_point(target, curr, max_speed):
    target = target.asCart()
    curr = curr.asCart()
    x = min(max(target.x - curr.x, -max_speed), max_speed)
    y = min(max(target.y - curr.y, -max_speed), max_speed)
    return CartVertex2D(x, y)

# main pathfinding strategy
def strategy_smooth(state):
    state["frame"] += 1 # increment frame for progress along the curve
    t = min(max(0.0, float(state["frame"]) / 175.0), 1.0)  # adjust timing for smoother animation

    # get the points from chosen index
    p1 = selected_curve["p1"]
    p2 = selected_curve["p2"]
    p3 = selected_curve["p3"]
    p4 = selected_curve["p4"]

    # get the target position on Bézier curve
    x = calc_bezier(t, p1.x, p2.x, p3.x, p4.x)
    y = calc_bezier(t, p1.y, p2.y, p3.y, p4.y)
    target = CartVertex2D(x, y)

    # get the rotation adjustment
    angle = state["tag_loc"].asPolar().addVector(CartVertex2D(-state["bot_loc"].x, -state["bot_loc"].y)).asPolar().a
    rotation = (state["tag_pose"].asPolar().a - state["bot_pose"].asPolar().a) * t

    # debugging output
    print(f" from {state['bot_loc'].asPolar()} to {state['tag_loc'].asPolar()} got angle {angle:.3f} rotation {rotation:.3f}")
    print(f"t: {t:.3f}   {target} - {state['bot_loc']} => {target.asPolar().diffVector(state['bot_loc']).asCart()}")

    # calculate next movement point and rotation
    return home_point(target, state["bot_loc"], 1.0), rotation

# animate
ani = FuncAnimation(fig, partial(animate_holonomic, state=curr_state, strategy=strategy_smooth), interval=30)

run()