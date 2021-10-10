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
    time_template = 'time = %.1fs'
    dt = .05
    return_arr = []
    for double_pendulum, ax_data in pendula_axes:
        ax, line, time_text = ax_data
        frame_x, frame_y = double_pendulum.get_frame_coordinates(i)
        line.set_data(frame_x, frame_y)
        time_text.set_text(time_template % (dt*i))
        return_arr.extend([
            line,
            time_text,
        ])
    return return_arr

def create_axes(fig: "matplotlib.figure.Figure", pendula: List["DoublePendulum"]) -> List["matplotlib.axes._subplots.AxesSubplot"]:
    axes = []
    for double_pendulum in pendula:
        color = random_hex()
        ax = _create_individual_axis(double_pendulum=double_pendulum, fig=fig)
        line, = ax.plot([], [], 'o-', lw=2, color=color)
        time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
        axes.append((ax, line, time_text))
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

    # Create the pendula
    fig = plt.figure()
    pendula = DoublePendulum.create_multiple_double_pendula(num_pendula=10) 
    axes = create_axes(fig=fig, pendula=pendula)
    pendula_axes = list(zip(pendula, axes))

    ani = animation.FuncAnimation(
        fig, 
        animate, 
        np.arange(1, len(pendula[0].y)),
        interval=25, 
        blit=True, 
    )
    plt.show()

