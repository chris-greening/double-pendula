"""Model of a single pendulum"""
# Author: Chris Greening
# Date: 2022-10-29

import numpy as np
import pandas as pd

class Pendulum:
    def __init__(self, L: float = 1.0, m: float = 1.0) -> None:
        """A single pendulum with rod of length L and a bob of mass M fixed at 
        the end
        
        Parameters
        ----------
        L : float
            Length of the pendulum rod
        m : float
            Mass of the bob
        """
        self.L = L
        self.m = m

    def calculate_path(self, theta: float, dtheta: float, x0: float = 0, y0: float = 0) -> None:
        """Calculate the (x,y) coordinate path of the pendulum
        
        Parameters
        ----------
        theta : float 
            Angle of the single pendulum rod
        dtheta : float 
            Change of angle of the pendulum rod
        x0 : float 
            x-offset. If this is only a single pendulum this is zero but if 
            this is a pendulum fixed to the bob of another pendulum then this 
            is nonzero
        y0 : float 
            y-offset. If this is only a single pendulum this is zero but if 
            this is a pendulum fixed to the bob of another pendulum then this 
            is nonzero
        """
        self.theta = theta
        self.dtheta = dtheta
        self.x = self.L*np.sin(self.theta) + x0
        self.y = self.L*np.cos(self.theta) + y0
        self.df = pd.DataFrame({"theta": self.theta, "dtheta": self.dtheta, 
                                "x": self.x, "y": self.y})

    def get_max_x(self) -> float:
        """Return the maximum x-value that this pendulum reaches"""
        return max(self.x)
    
    def get_max_y(self) -> float:
        """Return the maximum y-value that this pendulum reaches"""
        return max(self.y)

    def get_max_coordinates(self) -> Tuple[float, float]:
        """Return maximum cartesian coordinate that this system reaches"""
        return (self.get_max_x(), self.get_max_y())