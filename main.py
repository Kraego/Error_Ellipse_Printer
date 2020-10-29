import json
from plotter import Plotter
from failure_calculator import calculate_sigma_p_n_1, extract_ellipse_axes
from movement_calculator import POS_Y, POS_X, POS_MOVED, POS_ALPHA, calculate_positions

CONFIG_FILE = './movingConfig.json'


def __init_plot_area():
    plot_area = data['plot_area']
    Plotter.init(plot_area['xmin'], plot_area['xmax'],
                 plot_area['ymin'], plot_area['ymax'])


def __plot_add_start_point(x, y):
    Plotter.add_position(x, y)


def __plot_add_positions_and_failure_ellipses(start_pos, steps, uncertainty_factors, wheel_distance):
    positions = calculate_positions(start_pos, steps)
    orientation = 0
    sigma_p_n = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    for pos in positions:
        Plotter.add_position(pos[POS_X], pos[POS_Y])
        sigma_p_n_1 = calculate_sigma_p_n_1(sigma_p_n, uncertainty_factors, wheel_distance, pos[POS_MOVED], pos[POS_ALPHA])
        orientation = orientation + pos[POS_ALPHA]

        error_ellipse_axes = extract_ellipse_axes(sigma_p_n_1)
        Plotter.add_ellipse(pos[POS_X], pos[POS_Y], error_ellipse_axes[0], error_ellipse_axes[1],
                            orientation)
        sigma_p_n = sigma_p_n_1


if __name__ == '__main__':
    print('Initiating Error Ellipse Printer')

    with open(CONFIG_FILE) as f:
        data = json.load(f)

    __init_plot_area()
    __plot_add_start_point(data['start_position']['x'], data['start_position']['y'])
    __plot_add_positions_and_failure_ellipses(data['start_position'], data['steps'], data['drive_uncertainty_factors'], data['wheel_distance'])
    Plotter.plot()
