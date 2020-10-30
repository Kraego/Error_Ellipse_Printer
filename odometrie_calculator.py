import math
import numpy as np
import numpy.linalg as linalg

# moved distance to get to actual pos
POS_MOVED = 'movement'
# intended Rotation
POS_DIRECTION = 'direction'
POS_Y = 'y'
POS_X = 'x'
POS_THETA = 'theta'
# input data
STEP_MOVE = 'move'
STEP_ROT_DEGREES = 'rotation_degrees'


def calculate_position(step, x_n, y_n, theta_n):
    """
    Calculate position regarding to taken step/rotations

    :param step: current step
                    ('move' ... movement in x direction of moving robot
                     'rotation_degrees' ... rotation in degrees)
    :param x_n: previous position x coordinate
    :param y_n: previous position y coordinate
    :param theta_n: previous rotation
    :return: a position: position is dict with 'x', 'y', 'theta'
    """
    delta_s = step[STEP_MOVE]
    delta_theta = math.radians(step[STEP_ROT_DEGREES])

    #  calculate new position
    pos = np.array(
        [
            np.add(
                np.array([
                    x_n,
                    y_n,
                    theta_n
                ]),
                np.array([
                    delta_s * np.cos(theta_n + (delta_theta / 2)),
                    delta_s * np.sin(theta_n + (delta_theta / 2)),
                    delta_theta
                ])
            )
        ]
    )

    #  return as dict for convenience
    position = dict()
    position[POS_X] = pos[0][0]
    position[POS_Y] = pos[0][1]
    position[POS_THETA] = pos[0][2]
    return position


def calculate_ellipse_points_from_covariance_matrix(position, sigma_p_n):
    """
    Calcualte sigma ellipse for given covariance matrix

    :param position: position of the ellipse
    :param sigma_p_n: covariance matrix
    :return: tuple with list of x coordinates and list of y coordinates representing ellipse
    """

    t = np.linspace(0, 2 * np.pi, 100)

    ew, ev = linalg.eig(np.linalg.inv(sigma_p_n[0:2, 0:2]))

    ellipse = np.array((
        (1 / np.sqrt(ew[0]) * np.cos(t)),
        (1 / np.sqrt(ew[1]) * np.sin(t))
    ))

    ellipse_x, ellipse_y = np.transpose(
        np.add(
            np.transpose(
                np.matmul(ev, ellipse)
            ),
            [position[POS_X], position[POS_Y]]
        )
    )

    return ellipse_x, ellipse_y


def calculate_sigma_p_n_1(sigma_p_n, uncertainty_factors, d, delta_s, theta_n, delta_theta):
    """
    Calculate covariance of current step - sigma p(n+1) n..steps

    :param sigma_p_n covariance matrix of step n (previous step)
    :param uncertainty_factors: the uncertainty factors of the drive
    :param d: wheel distance
    :param delta_s: desired movement
    :param theta_n: theta of step n
    :param delta_theta: current rotation
    :return: sigma p (n+1)
    """

    sigma_r = uncertainty_factors['kr']
    sigma_l = uncertainty_factors['kl']

    sigma_s = [[sigma_r * abs(delta_s), 0],
               [0, sigma_l * abs(delta_s)]]

    g_p = [[1, 0, -delta_s * np.sin(theta_n + (delta_theta / 2))],
           [0, 1, delta_s * np.cos(theta_n + (delta_theta / 2))],
           [0, 0, 1]]

    g_s = [[0.5 * np.cos(theta_n + (delta_theta / 2)) - (delta_s / (2 * d)) * np.sin(theta_n + (delta_theta / 2)),
            0.5 * np.cos(theta_n + (delta_theta / 2)) + (delta_s / (2 * d)) * np.sin(theta_n + (delta_theta / 2))],
           [0.5 * np.sin(theta_n + (delta_theta / 2)) + (delta_s / (2 * d)) * np.cos(theta_n + (delta_theta / 2)),
            0.5 * np.sin(theta_n + (delta_theta / 2)) - (delta_s / (2 * d)) * np.cos(theta_n + (delta_theta / 2))],
           [1 / d, -1 / d]]

    sigma_p_n_1 = np.matmul(np.matmul(g_p, sigma_p_n), np.transpose(g_p)) + np.matmul(np.matmul(g_s, sigma_s), np.transpose(g_s))

    return sigma_p_n_1
