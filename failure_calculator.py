import math
import numpy as np
import numpy.linalg as linalg


def calculate_sigma_p_n_1(sigma_p_n, uncertainty_factors, wheel_distance, movement, alpha):
    """
    Calculate covariance of current step - sigma p(n+1) n..steps

    :param sigma_p_n covariance matrix of step n (previous step)
    :param uncertainty_factors: the uncertainty factors of the drive
    :param wheel_distance: wheel distance
    :param movement: desired movement
    :param alpha: rotation
    :return: sigma p (n+1)
    """
    sigma_r = uncertainty_factors['kr']
    sigma_l = uncertainty_factors['kl']

    rotation = math.radians(alpha)

    sigma_s = [[sigma_r * abs(movement), 0],
               [0, sigma_l * abs(movement)]]

    g_p = [[1, 0, -movement * math.sin(rotation)],
           [0, 1, movement * math.cos(rotation)],
           [0, 0, 1]]

    g_s = [[0.5 * math.cos(alpha) - (movement / (2 * wheel_distance)) * math.sin(alpha),
            0.5 * math.cos(alpha) + (movement / (2 * wheel_distance)) * math.sin(alpha)],
           [0.5 * math.sin(alpha) + (movement / (2 * wheel_distance)) * math.cos(alpha),
            0.5 * math.sin(alpha) - (movement / (2 * wheel_distance)) * math.cos(alpha)],
           [1 / wheel_distance, 1 / wheel_distance]]

    sigma_p_n_1 = np.matmul(np.matmul(g_p, sigma_p_n), np.transpose(g_p)) + np.matmul(np.matmul(g_s, sigma_s), np.transpose(g_s))

    return sigma_p_n_1


def extract_ellipse_axes(sigma_p_n):
    ew, ev = linalg.eig(sigma_p_n)
    return 1 / math.sqrt(ew[0]), 1 / math.sqrt(ew[1])
