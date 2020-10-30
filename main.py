import json
import math
from plotter import Plotter
from odometrie_calculator import calculate_sigma_p_n_1, calculate_position, POS_Y, POS_X, POS_THETA, STEP_MOVE, \
    STEP_ROT_DEGREES, calculate_ellipse_points_from_covariance_matrix

CONFIG_FILE = 'movingConfig_homework_no5.json'


def __init_plot_area():
    plot_area = data['plot_area']
    Plotter.init(plot_area['xmin'], plot_area['xmax'],
                 plot_area['ymin'], plot_area['ymax'])


def __plot_add_positions_and_failure_ellipses(start_pos, steps, uncertainty_factors, wheel_distance):
    sigma_p_n = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    Plotter.add_position(start_pos['x'], start_pos['y'], 'r')
    previous_location = None
    theta_n = 0

    for step in steps:
        #  Calculate
        if previous_location:
            pos = calculate_position(step, previous_location[POS_X], previous_location[POS_Y], previous_location[POS_THETA])
            theta_n = previous_location[POS_THETA]
        else:
            pos = calculate_position(step, 0, 0, 0)

        sigma_p_n_1 = calculate_sigma_p_n_1(sigma_p_n, uncertainty_factors, wheel_distance, step[STEP_MOVE], theta_n, math.radians(step[STEP_ROT_DEGREES]))
        ex, ey = calculate_ellipse_points_from_covariance_matrix(pos, sigma_p_n_1)

        #  Plot
        Plotter.add_position(pos[POS_X], pos[POS_Y], 'r')
        Plotter.add_lines(ex, ey, 'blue')

        sigma_p_n = sigma_p_n_1  # aggregation
        previous_location = pos


if __name__ == '__main__':
    print('Initiating Error Ellipse Printer')

    with open(CONFIG_FILE) as f:
        data = json.load(f)

    __init_plot_area()
    __plot_add_positions_and_failure_ellipses(data['start_position'], data['steps'], data['drive_uncertainty_factors'], data['wheel_distance'])
    Plotter.plot()
