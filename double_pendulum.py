"""Visualizing the butterfly effect via Python and Lagrangian mechanics."""
#Author: Chris Greening
#Date: 7/15/19

from typing import List
import string

import pandas as pd
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class DoublePendulum:
    g = -9.81
    tmax = 15.0
    dt = .05
    t = np.arange(0, tmax+dt, dt)
    time_template = 'time = %.1fs'
    def __init__(self, L1: int = 1, L2: int = 1, m1: int = 1, m2: int = 1, 
                 y0: List[int] = [90, 0, -10, 0]) -> None:
        """
        Instantiates a double pendulum with the given parameters and initial 
        conditions

        Parameters
        ----------
        L1 : int = 1
            Length of the first pendulum arm
        L2 : int = 1
            Length of the second pendulum arm 
        m1 : int = 1
            Mass of the first pendulum bob
        m2 : int = 1
            Mass of the second pendulum bob
        y0 : List[int] = [90, 0, -10, 0]
            Initial angle (in degrees) and angular velocity
        """
        self.pendulum1 = Pendulum(L1, m1)
        self.pendulum2 = Pendulum(L2, m2)
        self.y0 = np.array(np.radians(y0))

        # Do the numerical integration of the equations of motion
        self._calculate_system(L1, m1, L2, m2)

    def plot(self, fig: "matplotlib.figure.Figure", color: str = None) -> None:
        """Plot the double pendulum on an axis attached to a given figure
        
        Parameters
        ----------
        fig : matplotlib.figure.Figure
            Figure instance to attach the axis too
        color : str (optional)
            Color of the double pendulum, defaults to a random hex value
        """

        # TODO: there is probably a way to optimize this
        if color is None:
            color = random_hex()

        self.ax = self._create_axis(fig=fig)
        self.pendulum1.set_axes(self.ax)
        self.pendulum2.set_axes(self.ax)
        self.line, = self.ax.plot([], [], 'o-', lw=2, color=color)
        self.time_text = self.ax.text(0.05, 0.9, '', transform=self.ax.transAxes)

    def get_frame_x(self, i: int) -> List[int]:
        """Return x coordinates of the system of a specific frame"""
        return [
            0, 
            self.pendulum1.x[i], 
            self.pendulum2.x[i]
        ]
    
    def get_frame_y(self, i: int) -> List[int]:
        """Return y coordinates of the system of a specific frame"""
        return [
            0, 
            self.pendulum1.y[i],
            self.pendulum2.y[i]
        ]

    def set_frame(self, i: int) -> None:
        """Set the plot of this system to line as it appears at given frame"""
        frame_x = self.get_frame_x(i=i)
        frame_y = self.get_frame_y(i=i)
        self.line.set_data(frame_x, frame_y)
        self.time_text.set_text(self.time_template % (i*DoublePendulum.dt))

    @classmethod
    def create_multiple_double_pendula(
            cls, num_pendula: int = 1, L1: float = 1.0,                                
            L2: float = 1.0, m1: float = 1.0, m2: float = 1.0, 
            initial_theta: float = 90, dtheta: float = .05) -> List["DoublePendulum"]:
        fig = plt.figure()
        pendula = []
        created_pendula = 0
        while created_pendula < num_pendula:
            double_pendulum = cls(
                L1=L1,
                L2=L2,
                y0=[initial_theta, 0, -10, 0]
            )
            pendula.append(double_pendulum)

            # HACK: temp fix, plotting will be removed soon so the class can 
            # focus on modeling and not plotting
            double_pendulum.plot(fig)
            initial_theta += dtheta
            created_pendula += 1
        return pendula

    def _create_axis(self, fig: "matplotlib.figure.Figure") -> None:
        """Create dynamic axis to plot the double pendulum to"""
        ax_range = self.pendulum1.L + self.pendulum2.L
        ax = fig.add_subplot(
            111, 
            autoscale_on=False, 
            xlim=(-ax_range, ax_range), 
            ylim=(-ax_range, ax_range),
        )
        ax.set_aspect('equal')
        ax.grid()
        return ax

    def _calculate_system(self, L1: int, m1: int, L2: int, m2: int) -> None:
        """Solve the ODE and calculate the path for both pendulum's in the 
        system"""
        self.y = odeint(self.derivative, self.y0, self.t, 
                        args=(self.pendulum1.L, self.pendulum2.L, 
                              self.pendulum1.m, self.pendulum2.m,
                              DoublePendulum.g)
        )

        # Calculate individual pendulum paths
        self.pendulum1.calculate_path(
            theta=self.y[:, 0], 
            dtheta=self.y[:, 1]
        )
        self.pendulum2.calculate_path(
            theta=self.y[:, 2], 
            dtheta=self.y[:, 3], 
            x0=self.pendulum1.x, 
            y0=self.pendulum1.y
        )

        self.w = self.y[:, 1]
        self.df = pd.DataFrame(
            self.y, 
            columns=["theta1", "dtheta1", "theta2", "dtheta2"]
        )

    @staticmethod
    def derivative(y, t, L1, L2, m1, m2, g):
        """Return the first derivatives of y = theta1, z1, theta2, z2."""
        
        # Unpack initial conditions
        theta1, z1, theta2, z2 = y
        theta1dot, theta2dot = z1, z2

        c, s = np.cos(theta1-theta2), np.sin(theta1-theta2)

        z1dot = (m2*g*np.sin(theta2)*c - m2*s*(L1*z1**2*c + L2*z2**2) -
                (m1+m2)*g*np.sin(theta1)) / L1 / (m1 + m2*s**2)
        z2dot = ((m1+m2)*(L1*z1**2*s - g*np.sin(theta2) + g*np.sin(theta1)*c) + 
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

    def calculate_path(self, theta, dtheta, x0=0, y0=0):
        self.theta = theta
        self.dtheta = dtheta
        self.df = pd.DataFrame({"theta": self.theta, "dtheta": self.dtheta})
        self.x = self.L*np.sin(self.theta) + x0
        self.y = self.L*np.cos(self.theta) + y0

def random_hex() -> str:
    """Return a random hex color i.e. #FFFFFF"""
    hex_value = "".join(
        np.random.choice(
            list(string.hexdigits), 
            6
        )
    )
    return f"#{hex_value}"