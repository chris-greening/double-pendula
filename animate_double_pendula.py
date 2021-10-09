"""Animate a system of multiple double pendula, each with slightly different 
initial conditions to exemplify the signficance of initial conditions in a 
chaotic systems
"""

import string

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from double_pendulum import DoublePendulum

fig = plt.figure()

def animate(i):
    arr = pendula #pendulum2, pendulum3, pendulum4, pendulum5, pendulum6]
    return_arr = []
    for double_pendulum in arr:
        thisx = [0, double_pendulum.pendulum1.x[i], double_pendulum.pendulum2.x[i]]
        thisy = [0, double_pendulum.pendulum1.y[i],
                          double_pendulum.pendulum2.y[i]]
        
        double_pendulum.line.set_data(thisx, thisy)
        double_pendulum.time_text.set_text(double_pendulum.time_template % (i*double_pendulum.dt))

        return_arr.append(double_pendulum.line)
        return_arr.append(double_pendulum.time_text)
        return_arr.append(double_pendulum.pendulum1.p)
        return_arr.append(double_pendulum.pendulum2.p)

    return return_arr

def random_hex() -> str:
    hex_value = "".join(
        np.random.choice(
            list(string.hexdigits), 
            6
        )
    )
    return f"#{hex_value}"

if __name__ == "__main__":  
    L1 = 5
    L2 = 5

    pendula = []
    initial_dtheta = 0
    initial_theta = 90
    dtheta = .5

    #creates pendula 
    for _ in range(10):
        double_pendulum = DoublePendulum(L1=L1,L2=L2,y0=[initial_theta-initial_dtheta, 0,-10,0], color=random_hex())
        double_pendulum.plot(fig=fig)
        pendula.append(double_pendulum)
        initial_dtheta += dtheta

    # plt.plot(pendula[0].x2, pendula[0].y2, color=pendula[0].color)

    ani = animation.FuncAnimation(fig, animate, np.arange(1, len(pendula[0].y)),
                                interval=25, blit=True, init_func=pendula[0].init)

    # ani.save('line.gif', dpi=80, writer='imagemagick')

    plt.show()

