import json
from plotter import Plotter
from movement_calculator import calculate_positions, calculate_error_ellipse

CONFIG_FILE = './movingConfig.json'


if __name__ == '__main__':
    print('Initiating Error Ellipse Printer')

    with open(CONFIG_FILE) as f:
        data = json.load(f)

    plot_area = data['plot_area']
    Plotter.init(plot_area['xmin'], plot_area['xmax'],
                 plot_area['ymin'], plot_area['ymax'])

    Plotter.add_position(data['start_position']['x'], data['start_position']['y'])
    positions = calculate_positions(data['start_position'], data['steps'])

    for pos in positions:
        Plotter.add_position(pos['x'], pos['y'])
        error_ellipse = calculate_error_ellipse(data['drive_uncertainty_factors'],
                                                data['wheel_distance'], pos['alpha'])
        Plotter.add_ellipse(pos['x'], pos['y'], error_ellipse)
    Plotter.plot()
