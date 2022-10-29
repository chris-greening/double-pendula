"""Module for storing equations relevant to calculating the double pendulum's movement"""

import numpy as np

def derivative(y, t, L1, L2, m1, m2, g):
    """Return the first derivatives of y = theta1, z1, theta2, z2."""
    
    # Unpack initial conditions
    theta1, z1, theta2, z2 = y
    theta1dot, theta2dot = z1, z2

    c, s = np.cos(theta1-theta2), np.sin(theta1-theta2)

    z1dot = _calculate_z1dot(m1, m2, L1, L2, theta1, theta2, z1, z2, g, s, c)
    z2dot = _calculate_z2dot(m1, m2, L1, L2, theta1, theta2, z1, z2, g, s, c)
    return theta1dot, z1dot, theta2dot, z2dot

def _calculate_z1dot(m1, m2, L1, L2, theta1, theta2, z1, z2, g, s, c) -> float:
    """Return calculated z1dot"""
    return (m2*g*np.sin(theta2)*c - m2*s*(L1*z1**2*c + L2*z2**2) - (m1+m2)*g*np.sin(theta1)) / L1 / (m1 + m2*s**2)

def _calculate_z2dot(m1, m2, L1, L2, theta1, theta2, z1, z2, g, s, c) -> float:
    return ((m1+m2)*(L1*z1**2*s - g*np.sin(theta2) + g*np.sin(theta1)*c) + m2*L2*z2**2*s*c) / L2 / (m1 + m2*s**2)
