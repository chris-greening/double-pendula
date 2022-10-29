# Author: Chris Greening
# Date: 2022-10-29
# Purpose: Model of a single pendulum

class Pendulum:
    def __init__(self, L, m):
        self.L = L
        self.m = m

    def set_axes(self, ax):
        self.ax = ax

        # defines line that tracks where pendulum's have gone
        self.p, = self.ax.plot([], [], color='r')
        self.w = self.ax.plot([], [])

    def calculate_path(self, theta, dtheta, x0=0, y0=0):
        self.theta = theta
        self.dtheta = dtheta
        self.df = pd.DataFrame({"theta": self.theta, "dtheta": self.dtheta})
        self.x = self.L*np.sin(self.theta) + x0
        self.y = self.L*np.cos(self.theta) + y0