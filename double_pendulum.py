#Author: Chris Greening
#Date: 7/15/19
#Purpose: Another crack at the double pendulum to convert it to OOP
#to support multiple pendula

import numpy as np
import pandas as pd
from pandas import Series, DataFrame
from numpy import sin, cos
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib.animation as animation

the_figure = plt.figure()

class DoublePendulum:
    def __init__(
            self, 
            L1=1, 
            L2=1, 
            m1=1, 
            m2=1, 
            g=9.81,
            y0=[90, 0, -10, 0],
            color = "g"
        ):

        self.L1 = L1 
        self.L2 = L2 
        self.m1 = m1
        self.m2 = m2 
        self.g = g
        self.color = color

        self.tmax, self.dt = 180, 0.05
        self.t = np.arange(0, self.tmax+self.dt, self.dt)
        
        # Initial conditions: theta1, dtheta1/dt, theta2, dtheta2/dt.
        self.y0 = np.array(np.radians(y0))

        # Do the numerical integration of the equations of motion
        self.y = odeint(self.deriv, self.y0, self.t, args=(self.L1, self.L2, self.m1, self.m2))

        self.x1 = self.L1*sin(self.y[:, 0])
        self.y1 = -self.L1*cos(self.y[:, 0])

        self.x2 = self.L2*sin(self.y[:, 2]) + self.x1
        self.y2 = -self.L2*cos(self.y[:, 2]) + self.y1

        self.w = self.y[:, 1]

        self.fig = the_figure
        self.ax_range = self.L1 + self.L2
        self.ax = self.fig.add_subplot(111, autoscale_on=False, xlim=(-self.ax_range, self.ax_range), ylim=(-self.ax_range, self.ax_range))
        self.ax.set_aspect('equal')
        self.ax.grid()

        self.p1, = self.ax.plot([], [], color='r-') #defines line that tracks where pendulum's have gone
        self.p2, = self.ax.plot([], [], color=color + '-')
        self.w1 = self.ax.plot([], [])
        self.w2 = self.ax.plot([], [])

        self.line, = self.ax.plot([], [], 'o-', lw=2,color=self.color)
        self.time_template = 'time = %.1fs'
        self.time_text = self.ax.text(0.05, 0.9, '', transform=self.ax.transAxes)

        # self.ani = animation.FuncAnimation(self.fig, self.animate, np.arange(1, len(self.y)),
        #                       interval=25, blit=True, init_func=self.init)

        # plt.show()

    def deriv(self, y, t, L1, L2, m1, m2):
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

    def calc_E(self, y):
        """Return the total energy of the system."""

        th1, th1d, th2, th2d = y.T
        V = -(m1+m2)*L1*g*np.cos(th1) - m2*L2*g*np.cos(th2)
        T = 0.5*m1*(L1*th1d)**2 + 0.5*m2*((L1*th1d)**2 + (L2*th2d)**2 +
                2*L1*L2*th1d*th2d*np.cos(th1-th2))
        return T + V

    def init(self):
        self.line.set_data([], [])
        self.time_text.set_text('')
        return self.line, self.time_text

def animate(i):
    arr = pendula #pendulum2, pendulum3, pendulum4, pendulum5, pendulum6]
    return_arr = []
    for pendulum in arr:
        pendulum.thisx = [0, pendulum.x1[i], pendulum.x2[i]]
        pendulum.thisy = [0, pendulum.y1[i], pendulum.y2[i]]

        # pendulum.p1.set_data(pendulum.x1[:i], pendulum.y1[:i]) #draws path of p1
        # pendulum.p2.set_data(pendulum.x2[:i], pendulum.y2[:i]) #draws path of p2
        
        pendulum.line.set_data(pendulum.thisx, pendulum.thisy)
        pendulum.time_text.set_text(pendulum.time_template % (i*pendulum.dt))

        return_arr.append(pendulum.line) 
        return_arr.append(pendulum.time_text)
        return_arr.append(pendulum.p1)
        return_arr.append(pendulum.p2)

    return return_arr

def random_hex():
    
    hex_chars = "0123456789ABCDEF"
    
    hex_string = "#"
    for i in range(6):
        index = np.random.randint(0, len(hex_chars))
        hex_string += hex_chars[index]

    return hex_string

def double_pendula_generator(
            L1=5, 
            L1=5, 
            initial_dtheta=0, 
            inital_theta=160, 
            dtheta=1
            ):

    pendula = []


    #creates pendula 
    for _ in range(10):
        pendula.append(DoublePendulum(L1=L1,L2=L2,y0=[initial_theta-initial_dtheta, 0,0,0], color=random_hex()))
        initial_dtheta += dtheta

    # plt.plot(pendula[0].x2, pendula[0].y2, color=pendula[0].color)

    ani = animation.FuncAnimation(the_figure, animate, np.arange(1, len(pendula[0].y)),
                                interval=25, blit=True, init_func=pendula[0].init)

    plt.show()

if __name__ == '__main__':
    double_pendula_generator()


