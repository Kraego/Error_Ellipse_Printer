import math
from failure_model import calculate_sigma_p_n_1, extract_ellipse

# moved distance to get to actual pos
POS_MOVED = 'movement'
# intended Rotation
POS_ALPHA = 'alpha'
POS_Y = 'y'
POS_X = 'x'
# input data
STEP_MOVE = 'move'
STEP_ROT_DEGREES = 'rotation_degrees'


class Movement:
    sigma_p_n = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    @staticmethod
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
            position[POS_ALPHA] = theta_rads
            position[POS_MOVED] = step[STEP_MOVE]
            positions.append(position)
            previous_x = position[POS_X]
            previous_y = position[POS_Y]

        return positions

    @staticmethod
    def calculate_error_ellipse(drive_uncertainty_factors, wheel_distance, movement, alpha):
        """
        Calculate error ellipse, and accumulate covariance in sigma_p_n

        :param drive_uncertainty_factors: the factors
        :param wheel_distance: wheel distance
        :param movement: desired movement
        :param alpha: rotation
        :return: a dict containing 'width', 'height' and 'angle'
        """
        Movement.sigma_p_n = calculate_sigma_p_n_1(Movement.sigma_p_n, drive_uncertainty_factors, wheel_distance, movement, alpha)
        return extract_ellipse(Movement.sigma_p_n)
