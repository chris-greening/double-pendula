"""Model of a double pendulum"""
# Author: Chris Greening
# Date: 2019-07-15

from typing import Tuple, List

import pandas as pd
import numpy as np
from scipy import constants

from pendulum import Pendulum
from equations import derivative, solve_ode

class DoublePendulum:
    """Model of a double pendulum"""
    # pylint: disable=too-many-instance-attributes
    tmax = 15.0
    dt = .05
    t = np.arange(0, tmax+dt, dt)
    def __init__(self, L1: int = 1, L2: int = 1, m1: int = 1, m2: int = 1,
                 y0: List[int] = None, g: float = -1*constants.g) -> None:
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
        # pylint: disable=too-many-arguments,too-many-instance-attributes
        if y0 is None:
            y0 = [90, 0, -10, 0]
        self.pendulum1 = Pendulum(L1, m1)
        self.pendulum2 = Pendulum(L2, m2)
        self.y0 = np.array(np.radians(y0))
        self.g = g

        # Do the numerical integration of the equations of motion
        self._calculate_system()

        self.max_length = self.pendulum1.L + self.pendulum2.L

    def get_frame_x(self, i: int) -> Tuple[int]:
        """Return x coordinates of the system of a specific index"""
        return (0, self.pendulum1.x[i], self.pendulum2.x[i])

    def get_frame_y(self, i: int) -> Tuple[int]:
        """Return y coordinates of the system of a specific index"""
        return (0, self.pendulum1.y[i],self.pendulum2.y[i])

    def get_frame_coordinates(self, i: int) -> Tuple[Tuple[int]]:
        """Return the x,y coordinates at a given frame"""
        return (self.get_frame_x(i), self.get_frame_y(i))

    def get_max_x(self) -> float:
        """Return the maximum x-coord of the double pendulum"""
        return self.pendulum2.get_max_x()

    def get_max_y(self) -> float:
        """Return the maximum y-coord of the double pendulum"""
        return self.pendulum2.get_max_y()

    def get_max_coordinates(self) -> float:
        """Return the maximum coordinates the overall system reaches"""
        return self.pendulum2.get_max_coordinates()

    @classmethod
    def create_multiple_double_pendula(
            cls, num_pendula: int = 1, L1: float = 1.0,
            L2: float = 1.0, m1: float = 1.0, m2: float = 1.0,
            initial_theta: float = 90, dtheta: float = .05) -> List["DoublePendulum"]:
        """Returns a list of DoublePendulum's each offset slightly from each other"""
        # pylint: disable=too-many-arguments
        pendula = []
        created_pendula = 0
        while created_pendula < num_pendula:
            double_pendulum = cls(
                L1=L1,
                L2=L2,
                m1=m1,
                m2=m2,
                y0=[initial_theta, 0, -10, 0]
            )
            pendula.append(double_pendulum)

            initial_theta += dtheta
            created_pendula += 1
        return pendula

    def _calculate_system(self) -> None:
        """Solve the ODE and calculate the path for both pendulum's in the
        system"""
        self.y = solve_ode(
            derivative,
            self.y0,
            self.t,
            self.g,
            self.pendulum1,
            self.pendulum2
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

    def __repr__(self):
        # pylint: disable=line-too-long
        return f"< DoublePendulum: L1={self.pendulum1.L} m1={self.pendulum1.m} L2={self.pendulum2.L} m2={self.pendulum2.m} y0={self.y0} >"
