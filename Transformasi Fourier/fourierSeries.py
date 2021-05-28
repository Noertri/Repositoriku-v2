from math import sin, cos, pi

import matplotlib.patches as mp
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


class Epicycles:
    def __init__(self, center, funrad, funx, funy):
        self.center = center
        self.funrad = funrad
        self.funx = funx
        self.funy = funy

    def drawEpi(self, ax, N, t):
        x = self.center[0]
        y = self.center[1]

        for n in range(1, N):
            xo = x
            yo = y
            dx = self.funx(n, t)
            dy = self.funy(n, t)
            rad = self.funrad(n)
            self.drawcircle(ax, (x, y), rad)
            x += rad*dx
            y += rad*dy
            ax.plot([xo, x], [yo, y], color='black', marker='o', markersize=0.5)

        return x, y

    def drawcircle(self, ax, center, rad):
        circle = mp.Circle(center, rad, fill=False, color='grey')
        ax.add_patch(circle)


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

rad = lambda n: 5/(n*pi)*(1 - cos(n*pi))
funx = lambda n, t: cos((n*pi*t)/5)
funy = lambda n, t: sin((n*pi*t)/5)
titikx = []
titiky = []


def animate(i):
    ax.cla()
    ax.axis('scaled')
    ax.grid(True)
    ax.set_xlim(left=-50, right=55)
    ax.set_ylim(top=10, bottom=-10)

    epi = Epicycles((-25, 2.5), rad, funx, funy)
    x, y = epi.drawEpi(ax, 101, i)

    titikx.append(i)
    titiky.append(y)

    ax.plot(titikx, titiky)


anim = FuncAnimation(fig, animate, frames=np.linspace(0, 51, 100), repeat=False)
plt.show()