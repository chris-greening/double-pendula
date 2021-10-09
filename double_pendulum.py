"""Visualizing the butterfly effect via Python and Lagrangian mechanics."""
#Author: Chris Greening
#Date: 7/15/19

from typing import List
import string

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()

class DoublePendulum:
    g = -9.81
    tmax = 15.0
    dt = .05
    t = np.arange(0, tmax+dt, dt)
    def __init__(self, L1: int = 1, L2: int = 1, m1: int = 1, m2: int = 1, 
                 y0: List[int] = [90, 0, -10, 0], color: str = "g") -> None:
    
        self.color = color
        self.pendulum1 = Pendulum(L1, m1)
        self.pendulum2 = Pendulum(L2, m2)
        
        # Initial conditions: theta1, dtheta1/dt, theta2, dtheta2/dt.
        self.y0 = np.array(np.radians(y0))

        # Do the numerical integration of the equations of motion
        self.y = odeint(self.derivative, self.y0, self.t, args=(self.pendulum1.L, self.pendulum2.L, self.pendulum1.m, self.pendulum2.m))

        self.pendulum1.calculate_path(self.y[:, 0])
        self.pendulum2.calculate_path(self.y[:, 2], self.pendulum1.x, self.pendulum1.y)

        self.w = self.y[:, 1]

        self.fig = fig
        self.ax_range = self.pendulum1.L + self.pendulum2.L
        self.ax = self.fig.add_subplot(111, autoscale_on=False, xlim=(-self.ax_range, self.ax_range), ylim=(-self.ax_range, self.ax_range))
        self.ax.set_aspect('equal')
        self.ax.grid()

        self.pendulum1.set_axes(self.ax)
        self.pendulum2.set_axes(self.ax)

        self.line, = self.ax.plot([], [], 'o-', lw=2,color=self.color)
        self.time_template = 'time = %.1fs'
        self.time_text = self.ax.text(0.05, 0.9, '', transform=self.ax.transAxes)

    def derivative(self, y, t, L1, L2, m1, m2):
        """Return the first derivatives of y = theta1, z1, theta2, z2."""
        theta1, z1, theta2, z2 = y

        c, s = np.cos(theta1-theta2), np.sin(theta1-theta2)

        theta1dot = z1
        z1dot = (m2*self.g*np.sin(theta2)*c - m2*s*(L1*z1**2*c + L2*z2**2) -
                (m1+m2)*self.g*np.sin(theta1)) / L1 / (m1 + m2*s**2)
        theta2dot = z2
        z2dot = ((m1+m2)*(L1*z1**2*s - self.g*np.sin(theta2) + self.g*np.sin(theta1)*c) + 
                m2*L2*z2**2*s*c) / L2 / (m1 + m2*s**2)
        return theta1dot, z1dot, theta2dot, z2dot

    def init(self):
        self.line.set_data([], [])
        self.time_text.set_text('')
        return self.line, self.time_text

class Pendulum:
    def __init__(self, L, m):
        self.L = L
        self.m = m

    def set_axes(self, ax):
        self.ax = ax

        # defines line that tracks where pendulum's have gone
        self.p, = self.ax.plot([], [], color='r')
        self.w = self.ax.plot([], [])

    def calculate_path(self, y, x0=0, y0=0):
        self.x = self.L*np.sin(y) + x0
        self.y = self.L*np.cos(y) + y0

def animate(i):
    arr = pendula #pendulum2, pendulum3, pendulum4, pendulum5, pendulum6]
    return_arr = []
    for double_pendulum in arr:
        thisx = [0, double_pendulum.pendulum1.x[i], double_pendulum.pendulum2.x[i]]
        thisy = [0, double_pendulum.pendulum1.y[i],
                          double_pendulum.pendulum2.y[i]]
        
        double_pendulum.line.set_data(thisx, thisy)
        double_pendulum.time_text.set_text(double_pendulum.time_template % (i*double_pendulum.dt))

        return_arr.append(double_pendulum.line)
        return_arr.append(double_pendulum.time_text)
        return_arr.append(double_pendulum.pendulum1.p)
        return_arr.append(double_pendulum.pendulum2.p)

    return return_arr

def random_hex() -> str:
    hex_value = "".join(
        np.random.choice(
            list(string.hexdigits), 
            6
        )
    )
    return f"#{hex_value}"
     
L1 = 5
L2 = 5

pendula = []
initial_dtheta = 0
initial_theta = 90
dtheta = .5

#creates pendula 
for _ in range(10):
    pendula.append(DoublePendulum(L1=L1,L2=L2,y0=[initial_theta-initial_dtheta, 0,-10,0], color=random_hex()))
    initial_dtheta += dtheta

# plt.plot(pendula[0].x2, pendula[0].y2, color=pendula[0].color)

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(pendula[0].y)),
                            interval=25, blit=True, init_func=pendula[0].init)

# ani.save('line.gif', dpi=80, writer='imagemagick')

plt.show()

