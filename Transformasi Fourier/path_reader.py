import Fourier
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
import json
from matplotlib.animation import FuncAnimation
from time import perf_counter


#Membuka file yg berisi titik2 koordinat gambar
with open("lumba2_path.json", "r") as fin:
    points_list = json.load(fin)
    fin.close()

p = len(points_list)
ttk = [points_list[i] for i in range(0, p, 2)]
ttk.append(ttk[0])

points = np.array(ttk, dtype=np.float64)

(m, n) = points.shape

for i in range(m):
    points[i, 1] = -1*points[i, 1]

#Menghitung transformasi fourier dari titik2 koordinat
fhats = Fourier.dft2dim(points)

#Inisialisai
fig1, ax = plt.subplots()
epi = Fourier.Epicycles(fhats)
ttx, tty = [], []


def animate(f, limx=[0., 0.], limy=[0., 0.]):

    ax.cla()
    ax.axis("scaled")
    ax.grid(True)
    ax.set_xlim(limx)
    ax.set_ylim(limy)
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    teks1 = "Frame = " + str(f+1)

    ttk2 = epi.drawepic(ax, M=m, frame=f, center=(0., 0.), rot=0.)

    for xt, yt in ttk2:
        ttx.append(xt)
        tty.append(yt)

    ax.plot(ttx, tty)

    count = perf_counter()
    teks1 = teks1 + f'\nTime = {count:.3f} detik'
    ax.text((xmin+10), (ymin+10), teks1)


if __name__ == '__main__':
    anim = FuncAnimation(fig1, animate, frames=m, repeat=False, interval=1, fargs=([-100, 100], [-100, 100]))
    anim.save("lumba2_fourier.mp4", writer="ffmpeg", fps=30)
    print("Selesai!!!!!")