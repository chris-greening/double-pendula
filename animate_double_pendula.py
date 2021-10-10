"""Animate a system of multiple double pendula, each with slightly different 
initial conditions to exemplify the signficance of initial conditions in a 
chaotic systems
"""

import string
from typing import List

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from double_pendulum import DoublePendulum

def random_hex() -> str:
    """Return a random hex color i.e. #FFFFFF"""
    hex_value = "".join(
        np.random.choice(
            list(string.hexdigits), 
            6
        )
    )
    return f"#{hex_value}"

def animate(i):
    return_arr = []
    for double_pendulum in pendula:
        double_pendulum.set_frame(i=i)

        return_arr.extend([
            double_pendulum.line,
            double_pendulum.time_text,
            double_pendulum.pendulum1.p,
            double_pendulum.pendulum2.p
        ])
    return return_arr

def create_axes(pendula: List["DoublePendulum"]) -> List["matplotlib.axes._subplots.AxesSubplot"]:
    fig = plt.figure()
    axes = []
    for double_pendulum in pendula:
        color = random_hex()

        ax = _create_individual_axis(double_pendulum=double_pendulum, fig=fig)
        double_pendulum.pendulum1.set_axes(ax)
        double_pendulum.pendulum2.set_axes(ax)
        line, = ax.plot([], [], 'o-', lw=2, color=color)
        time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
        axes.append((ax, line))
    return axes

def _create_individual_axis(double_pendulum: "DoublePendulum", fig: "matplotlib.figure.Figure") -> None:
    """Create dynamic axis to plot the double pendulum to"""
    ax_range = double_pendulum.pendulum1.L + double_pendulum.pendulum2.L
    ax = fig.add_subplot(
        111, 
        autoscale_on=False, 
        xlim=(-ax_range, ax_range), 
        ylim=(-ax_range, ax_range),
    )
    ax.set_aspect('equal')
    ax.grid()
    return ax

if __name__ == "__main__":  
    NUM_PENDULUMS = 10
    L1 = 5
    L2 = 5

    pendula = []
    initial_dtheta = 0
    initial_theta = 90
    dtheta = .5

    # Create the pendula
    pendula = DoublePendulum.create_multiple_double_pendula(num_pendula=10) 
    
    axes = create_axes(pendula=pendula)

    # plt.plot(pendula[0].x2, pendula[0].y2, color=pendula[0].color)

    ani = animation.FuncAnimation(
        fig, 
        animate, 
        np.arange(1, len(pendula[0].y)),
        interval=25, 
        blit=True, 
        init_func=pendula[0].init
    )

    # ani.save('line.gif', dpi=80, writer='imagemagick')

    plt.show()

