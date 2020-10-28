import math

import numpy as np

global last_covariance_matrix


def calculate_positions(start_position, steps):
    """
    Calculate position regarding to taken steps/rotations

    :param start_position: start position (dict with 'x' & 'y')
    :param steps: movement, a dict with
                    ('move' ... movement in x direction of moving robot
                     'rotation_degrees' ... rotation in degrees)
    :return: a list of positions: position is dict with 'x', 'y' and 'alpha'
    """
    alpha_rads = 0
    previous_x = start_position['x']
    previous_y = start_position['y']
    positions = []

    for step in steps:
        alpha_rads = alpha_rads + math.radians(step['rotation_degrees'])
        position = dict()
        position['x'] = previous_x + step['move'] * math.cos(alpha_rads)
        position['y'] = previous_y + step['move'] * math.sin(alpha_rads)
        position['alpha'] = alpha_rads
        positions.append(position)
        previous_x = position['x']
        previous_y = position['y']

    return positions


def calculate_error_ellipse(drive_uncertainty_factors, wheel_distance, alpha):
    """
    Calculate error ellipse

    :param drive_uncertainty_factors: the factors
    :param wheel_distance: wheel distance
    :param alpha: rotation
    :return: a dict containing 'width', 'height' and 'angle'
    """
    sigma_d = drive_uncertainty_factors['kr']
    sigma_alpha = drive_uncertainty_factors['kl']

    covariance_matrix_x = [[sigma_d,           0],
                           [0,       sigma_alpha]]

    g_x = [[math.cos(alpha), -wheel_distance * math.sin(alpha)],
           [math.sin(alpha), wheel_distance * math.cos(alpha)]]

    covariance_matrix = np.matmul(np.matmul(g_x, covariance_matrix_x), np.transpose(g_x))
    result = dict()

    result['width'] = 10
    result['height'] = 10
    result['angle'] = 0

    last_covariance_matrix = covariance_matrix
    return result
