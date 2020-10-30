import matplotlib.pyplot as plt


class Plotter:
    @staticmethod
    def init(x_min, x_max, y_min, y_max):
        plt.title('Error Ellipse Printer')
        plt.grid()
        plt.axis([x_min, x_max, y_min, y_max])

    @staticmethod
    def add_position(x, y):
        plt.plot(x, y, 'ro', markersize=3)

    @staticmethod
    def add_ellipse(ellipse_x, ellipse_y):
        plt.plot(ellipse_x, ellipse_y, '-', color='blue', linewidth=1)

    @staticmethod
    def plot():
        plt.show()
