import math

# moved distance to get to actual pos
POS_MOVED = 'movement'
# intended Rotation
POS_DIRECTION = 'direction'
POS_Y = 'y'
POS_X = 'x'
# input data
STEP_MOVE = 'move'
STEP_ROT_DEGREES = 'rotation_degrees'


def calculate_positions(start_position, steps):
    """
    Calculate position regarding to taken steps/rotations

    :param start_position: start position (dict with 'x' & 'y')
    :param steps: movement, a dict with
                    ('move' ... movement in x direction of moving robot
                     'rotation_degrees' ... rotation in degrees)
    :return: a list of positions: position is dict with 'x', 'y', 'movement' and 'alpha'
    """
    theta_rads = 0
    previous_x = start_position[POS_X]
    previous_y = start_position[POS_Y]
    positions = []

    for step in steps:
        theta_rads = theta_rads + math.radians(step[STEP_ROT_DEGREES])
        position = dict()
        position[POS_X] = previous_x + step[STEP_MOVE] * math.cos(theta_rads)
        position[POS_Y] = previous_y + step[STEP_MOVE] * math.sin(theta_rads)
        position[POS_DIRECTION] = theta_rads
        position[POS_MOVED] = step[STEP_MOVE]
        positions.append(position)
        previous_x = position[POS_X]
        previous_y = position[POS_Y]

    return positions
