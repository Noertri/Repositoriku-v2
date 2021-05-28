import matplotlib.patches as mp
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()


def animate(frame):
    ax.cla()
    ax.grid(True)
    ax.axis('scaled')
    ax.set_xlim([-20, 20])
    ax.set_ylim([-20, 20])

    dx = lambda time, n: np.cos((2 * np.pi*n*time) / 10)
    dy = lambda time, n: np.sin((2 * np.pi*n*time) / 10)
    # ax.plot([0, dx(frame)], [0, dy(frame)])

    r = 5
    x = -10
    y = 0
    for n in range(1, 5):
        ro = r
        circle = mp.Circle((x, y), r, color='grey', fill=False)
        ax.add_patch(circle)
        x += ro * dx(frame, n)
        y += ro * dy(frame, n)
        r = r-0.5


anim = FuncAnimation(fig, animate, frames=31, interval=10)