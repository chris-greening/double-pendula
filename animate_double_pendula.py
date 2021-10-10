"""Animate a system of multiple double pendula, each with slightly different 
initial conditions to exemplify the signficance of initial conditions in a 
chaotic systems
"""

from typing import List

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from double_pendulum import DoublePendulum

# if color is None:
#     color = random_hex()

# self.ax = self._create_axis(fig=fig)
# self.pendulum1.set_axes(self.ax)
# self.pendulum2.set_axes(self.ax)
# self.line, = self.ax.plot([], [], 'o-', lw=2, color=color)
# self.time_text = self.ax.text(0.05, 0.9, '', transform=self.ax.transAxes)

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

