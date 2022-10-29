"""Objects for modeling the system via Lagrangian mechanics"""
#Author: Chris Greening
#Date: 7/15/19

from typing import Tuple, List

import pandas as pd
import numpy as np
from scipy.integrate import odeint
from scipy import constants

from pendulum import Pendulum

class DoublePendulum:
    tmax = 15.0
    dt = .05
    t = np.arange(0, tmax+dt, dt)
    def __init__(self, L1: int = 1, L2: int = 1, m1: int = 1, m2: int = 1, 
                 y0: List[int] = [90, 0, -10, 0], g: float = -1*constants.g) -> None:
        """Instantiates a double pendulum with the given parameters and initial 
        conditions

        Parameters
        ----------
        L1 : int = 1
            Length of the first pendulum arm (m)
        L2 : int = 1
            Length of the second pendulum arm (m)
        m1 : int = 1
            Mass of the first pendulum bob (g)
        m2 : int = 1
            Mass of the second pendulum bob (g)
        y0 : List[int] = [90, 0, -10, 0]
            Initial angle and angular velocity (degrees)
        g : float = -9.81
            Gravitational acceleration (m/(s^2))
        """
        self.pendulum1 = Pendulum(L1, m1)
        self.pendulum2 = Pendulum(L2, m2)
        self.y0 = np.array(np.radians(y0))
        self.g = g

        # Do the numerical integration of the equations of motion
        self._calculate_system(L1, m1, L2, m2)

        self.max_length = self.pendulum1.L + self.pendulum2.L

    def get_frame_x(self, i: int) -> Tuple[int]:
        """Return x coordinates of the system of a specific index"""
        return (
            0, 
            self.pendulum1.x[i], 
            self.pendulum2.x[i]
        )
    
    def get_frame_y(self, i: int) -> Tuple[int]:
        """Return y coordinates of the system of a specific index"""
        return (
            0, 
            self.pendulum1.y[i],
            self.pendulum2.y[i]
        )

    def get_frame_coordinates(self, i: int) -> Tuple[Tuple[int]]:
        """Return the x,y coordinates at a given frame"""
        return (self.get_frame_x(i), self.get_frame_y(i))

    def get_max_x(self) -> float:
        """Return the maximum x-value that this system reaches"""
        return self.pendulum2.get_max_x()
    
    def get_max_y(self) -> float:
        return self.pendulum2.get_max_y()

    def get_max_coordinates(self) -> float:
        return self.pendulum2.get_max_coordinates()

    @classmethod
    def create_multiple_double_pendula(
            cls, num_pendula: int = 1, L1: float = 1.0,                                
            L2: float = 1.0, m1: float = 1.0, m2: float = 1.0, 
            initial_theta: float = 90, dtheta: float = .05) -> List["DoublePendulum"]:
        """Returns a list of DoublePendulum's each offset slightly from each other"""
        pendula = []
        created_pendula = 0
        while created_pendula < num_pendula:
            double_pendulum = cls(
                L1=L1,
                L2=L2,
                y0=[initial_theta, 0, -10, 0]
            )
            pendula.append(double_pendulum)

            initial_theta += dtheta
            created_pendula += 1
        return pendula

    def _calculate_system(self, L1: int, m1: int, L2: int, m2: int) -> None:
        """Solve the ODE and calculate the path for both pendulum's in the 
        system"""
        self.y = odeint(self._derivative, self.y0, self.t, 
                        args=(self.pendulum1.L, self.pendulum2.L, 
                              self.pendulum1.m, self.pendulum2.m,
                              self.g)
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
    def _derivative(y, t, L1, L2, m1, m2, g):
        """Return the first derivatives of y = theta1, z1, theta2, z2."""
        
        # Unpack initial conditions
        theta1, z1, theta2, z2 = y
        theta1dot, theta2dot = z1, z2

        c, s = np.cos(theta1-theta2), np.sin(theta1-theta2)

        z1dot = (m2*g*np.sin(theta2)*c - m2*s*(L1*z1**2*c + L2*z2**2) - (m1+m2)*g*np.sin(theta1)) / L1 / (m1 + m2*s**2)
        z2dot = ((m1+m2)*(L1*z1**2*s - g*np.sin(theta2) + g*np.sin(theta1)*c) + m2*L2*z2**2*s*c) / L2 / (m1 + m2*s**2)
        return theta1dot, z1dot, theta2dot, z2dot

    def __repr__(self):
        return f"< DoublePendulum: L1={self.pendulum1.L} m1={self.pendulum1.m} L2={self.pendulum2.L} m2={self.pendulum2.m} y0={self.y0} >"
