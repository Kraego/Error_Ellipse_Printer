import matplotlib.pyplot as plt
import matplotlib.patches as m_patches


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
    def add_ellipse(x, y, width, height, angle):
        ellipse = m_patches.Ellipse(xy=(x, y), width=width, height=height,
                                    angle=angle, edgecolor='b', lw=1, fill=False)

        ax = plt.gca()
        ax.add_artist(ellipse)

    @staticmethod
    def plot():
        plt.show()
