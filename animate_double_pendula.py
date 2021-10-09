"""Animate a system of multiple double pendula, each with slightly different 
initial conditions to exemplify the signficance of initial conditions in a 
chaotic systems
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from double_pendulum import DoublePendulum

fig = plt.figure()

def animate(i):
    return_arr = []
    for double_pendulum in pendula:
        double_pendulum.set_frame(i=i)

        return_arr.append(
            *(
                double_pendulum.line,
                double_pendulum.time_text,
                double_pendulum.pendulum1.p,
                double_pendulum.pendulum2.p
            )
        )

    return return_arr

if __name__ == "__main__":  
    L1 = 5
    L2 = 5

    pendula = []
    initial_dtheta = 0
    initial_theta = 90
    dtheta = .5

    #creates pendula 
    for _ in range(10):
        double_pendulum = DoublePendulum(L1=L1,L2=L2,y0=[initial_theta-initial_dtheta, 0,-10,0])
        double_pendulum.plot(fig=fig)
        pendula.append(double_pendulum)
        initial_dtheta += dtheta

    # plt.plot(pendula[0].x2, pendula[0].y2, color=pendula[0].color)

    ani = animation.FuncAnimation(fig, animate, np.arange(1, len(pendula[0].y)),
                                interval=25, blit=True, init_func=pendula[0].init)

    # ani.save('line.gif', dpi=80, writer='imagemagick')

    plt.show()

