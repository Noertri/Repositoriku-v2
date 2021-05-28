from math import sin, cos, sqrt, atan2, pi
import matplotlib.patches as mp
import numpy as np


def dft(x):
    """
    Fungsi untuk DFT(Discrete Fourier Transform)
    """

    N = len(x)
    freq = []
    amp = []
    fase = []
    xhat = (freq, amp, fase, N)

    for n in range(N):
        re = 0
        im = 0
        for k in range(N):
            theta = (2*pi)/N
            a = cos(theta*k*n)
            b = sin(theta*k*n)

            re += x[k]*a
            im -= x[k]*b

        freq.append(n)
        amp.append(sqrt(re**2 + im**2))
        fase.append(atan2(im, re))

    return xhat


def dft2dim(x):
    """
    Fungsi untuk menghitung DFT(Discrete Fourier Transform)
    x yang memiliki 2 dimensi
    """

    (N, M) = x.shape
    fhats = []
    for n in range(N):
        re = 0
        im = 0
        for k in range(N):
            theta = (-2*pi)/N
            a = cos(theta*k*n)
            b = sin(theta*k*n)
            c = x[k, 0]
            d = x[k, 1]

            re += (a*c - b*d)
            im += (a*d + b*c)

        fhats.append(complex(re, im))

    return np.array(fhats)


class Epicycles:
    """
    Class untuk menggambar epicycles
    """
    def __init__(self, masukan):
        self.masukan = np.copy(masukan)

    def epicycles_gen(self, N=1, t=0., rot=0.):

        for i in range(1, N):

            fhat = self.masukan[i]
            re = cos(i*t + rot)
            im = sin(i*t + rot)
            b = complex(re, im)
            cn = (1/N)*fhat*b
            dx = cn.real
            dy = cn.imag
            rad = abs(cn)
            yield dx, dy, rad

    def drawepic(self, ax, M=1, frame=0, center=(0., 0.), rot=0.):

        lnx = [center[0]]
        lny = [center[1]]
        xn = center[0]
        yn = center[1]
        time = 2 * pi * frame / M
        for dx, dy, rad in self.epicycles_gen(t=time, rot=rot, N=M):
            co = (xn, yn)
            xn += dx
            yn += dy
            lnx.append(xn)
            lny.append(yn)
            self.drawcircles(ax, co, rad)

        self.drawlines(ax, lnx, lny)

        yield xn, yn

    def drawlines(self, ax, xox=[], yoy=[]):
        ax.plot(xox, yoy, color='black', marker='o', markersize=1)

    def drawcircles(self, ax, center=(0., 0.), rad=0.):
        circle = mp.Circle(center, rad, color='grey', fill=False)
        ax.add_patch(circle)