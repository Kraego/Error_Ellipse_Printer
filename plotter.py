import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse


class Plotter:
    @staticmethod
    def init(xmin, xmax, ymin, ymax):
        plt.title('Error Ellipse Printer')
        plt.grid()
        plt.axis([xmin, xmax, ymin, ymax])

    @staticmethod
    def add_position(x, y):
        plt.plot(x, y, 'ro', markersize=3)

    @staticmethod
    def add_ellipse(x, y, error_ellipse):
        ellipse = Ellipse(xy=(x, y), width=0.036, height=0.012,
                          edgecolor='b', fc='None', lw=2)

        ax = plt.gca()
        ax.add_patch(ellipse)

    @staticmethod
    def plot():
        plt.show()
