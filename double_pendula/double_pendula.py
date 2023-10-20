"""Model of a double pendulum"""

from typing import Tuple, List

import pandas as pd
import numpy as np
from scipy import constants

from .pendulum import Pendulum
from .equations import derivative, solve_ode

class DoublePendula:
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
        """Return x coordinates of the system of a specific index.

        Parameters
        ----------
        i : int
            The index of the frame for which to return x coordinates.

        Returns
        -------
        Tuple[int]
            A tuple containing the x coordinates of the system at the specified index.
            The first element is always 0, followed by the x coordinate of `pendulum1` and
            the x coordinate of `pendulum2`.
        """
        return (0, self.pendulum1.x[i], self.pendulum2.x[i])

    def get_frame_y(self, i: int) -> Tuple[int]:
        """
        Return y coordinates of the system of a specific index.

        Parameters
        ----------
        i : int
            The index of the frame for which to return y coordinates.

        Returns
        -------
        Tuple[int]
            A tuple containing the y coordinates of the system at the specified index.
            The first element is always 0, followed by the y coordinate of `pendulum1` and
            the y coordinate of `pendulum2`.
        """
        return (0, self.pendulum1.y[i],self.pendulum2.y[i])

    def get_frame_coordinates(self, i: int) -> Tuple[Tuple[int]]:
        """Return the x,y coordinates at a given frame.

        Parameters
        ----------
        i : int
            The index of the frame for which to return x,y coordinates.

        Returns
        -------
        Tuple[Tuple[int]]
            A tuple containing two tuples: the first one is the x coordinates
            and the second one is the y coordinates of the system at the specified
            index. Each inner tuple follows the format:
            (coordinate of origin, coordinate of `pendulum1`, coordinate of `pendulum2`).
        """
        return (self.get_frame_x(i), self.get_frame_y(i))

    def get_max_x(self) -> float:
        """
        Return the maximum x-coordinate of the double pendulum.

        Returns
        -------
        float
            The maximum x-coordinate that the double pendulum reaches.
        """
        return self.pendulum2.get_max_x()

    def get_max_y(self) -> float:
        """
        Return the maximum y-coordinate of the double pendulum.

        Returns
        -------
        float
            The maximum y-coordinate that the double pendulum reaches.
        """
        return self.pendulum2.get_max_y()

    def get_max_coordinates(self) -> float:
        """
        Return the maximum coordinates the overall system reaches.

        Returns
        -------
        float
            The maximum distance from the origin that the overall double pendulum system reaches.
        """
        return self.pendulum2.get_max_coordinates()

    @classmethod
    def create_multiple_double_pendula(
            cls, num_pendula: int = 1, L1: float = 1.0,
            L2: float = 1.0, m1: float = 1.0, m2: float = 1.0,
            initial_theta: float = 90, dtheta: float = .05) -> List["DoublePendula"]:
        """
        Creates and returns a list of DoublePendula objects with initial
        conditions offset by dtheta.

        Parameters
        ----------
        num_pendula : int, optional
            Number of DoublePendula objects to create, default is 1.
        L1 : float, optional
            Length of the first pendulum arm, default is 1.0.
        L2 : float, optional
            Length of the second pendulum arm, default is 1.0.
        m1 : float, optional
            Mass of the first pendulum bob, default is 1.0.
        m2 : float, optional
            Mass of the second pendulum bob, default is 1.0.
        initial_theta : float, optional
            Initial angle in degrees of the first pendulum, default is 90.
        dtheta : float, optional
            Offset in initial angle in degrees for each subsequent pendulum,
            default is 0.05.

        Returns
        -------
        List["DoublePendula"]
            A list containing the created DoublePendula objects.
        """
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
        return f"< DoublePendula: L1={self.pendulum1.L} m1={self.pendulum1.m} L2={self.pendulum2.L} m2={self.pendulum2.m} y0={self.y0} >"