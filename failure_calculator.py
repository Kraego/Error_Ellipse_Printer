import math
import numpy as np
import numpy.linalg as linalg


def calculate_sigma_p_n_1(sigma_p_n, uncertainty_factors, d, delta_s):
    """
    Calculate covariance of current step - sigma p(n+1) n..steps
    ! ROTATION + MOVEMENT is not allowed !

    :param sigma_p_n covariance matrix of step n (previous step)
    :param uncertainty_factors: the uncertainty factors of the drive
    :param d: wheel distance
    :param delta_s: desired movement
    :return: sigma p (n+1)
    """

    sigma_r = uncertainty_factors['kr']
    sigma_l = uncertainty_factors['kl']

    theta_n = 0

    sigma_s = [[sigma_r * abs(delta_s), 0],
               [0, sigma_l * abs(delta_s)]]

    g_p = [[1, 0, -delta_s * math.sin(theta_n)],
           [0, 1, delta_s * math.cos(theta_n)],
           [0, 0, 1]]

    g_s = [[0.5 * math.cos(theta_n) - (delta_s / (2 * d)) * math.sin(theta_n),
            0.5 * math.cos(theta_n) + (delta_s / (2 * d)) * math.sin(theta_n)],
           [0.5 * math.sin(theta_n) + (delta_s / (2 * d)) * math.cos(theta_n),
            0.5 * math.sin(theta_n) - (delta_s / (2 * d)) * math.cos(theta_n)],
           [1 / d, -1 / d]]

    sigma_p_n_1 = np.matmul(np.matmul(g_p, sigma_p_n), np.transpose(g_p)) + np.matmul(np.matmul(g_s, sigma_s), np.transpose(g_s))

    return sigma_p_n_1


def extract_ellipse_axes(sigma_p_n):
    # TODO: entweder invertieren problem oder was mit den Einheiten??
    #inverted_sigma_p_n = np.linalg.inv(sigma_p_n)
    ew, ev = linalg.eig(sigma_p_n)
    # Todo: add rotation
    return 1 / math.sqrt(abs(ew[0])), 1 / math.sqrt(abs(ew[1]))
