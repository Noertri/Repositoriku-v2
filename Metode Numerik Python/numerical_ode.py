from math import sin, cos, pi, radians, sqrt
import numpy as np
import matplotlib
matplotlib.use("Qt5Agg", force=True)
import matplotlib.pyplot as plt


z10 = radians(10.)
z20 = 0.


def z2dot(t, *args):
    """
    t : independen variabel
    args : dependen variabel
    """
    return (-9.81/1.)*sin(args[0]) - 0.35*args[1]


def z1dot(t, *args):
    """
    t : independen variabel
    args : dependen variabel
    """
    return args[1]


#Menyelesaikan persamaan ODE dengan metode Euler
def eulerMethod(funcs=[], init=[], step=0., tspan=[0., 0.]):
    outlist = [init]
    ti = [tspan[0]]
    j = 0
    for tn in np.arange(tspan[0], tspan[1], step):
        k = 0
        yn = []
        for func in funcs:
            yi = outlist[j][k] + func(ti[j], *outlist[j])*step
            yn.append(yi)
            k += 1
        outlist.append(yn)
        ti.append(tn)
        j += 1

    youts = np.array(outlist)

    return ti, youts


def eulerHeunMethod(funcs=[], init=[], step=0., tspan=[0., 0.]):
    outlist = [init]
    ti = [tspan[0]]
    j = 0
    for tn in np.arange(tspan[0], tspan[1], step):

        #Predictor
        k = 0
        yn_old = []
        for func in funcs:
            yi_old = outlist[j][k] + func(ti[j], *outlist[j])*step
            yn_old.append(yi_old)
            k += 1

        #Corector
        i = 0
        yn_new = []
        for func in funcs:
            yi_new = outlist[j][i] + (func(ti[j], *outlist[j]) + func(ti[j], *yn_old))*step*0.5
            yn_new.append(yi_new)
            i += 1

        outList.append(yn_new)
        ti.append(tn)
        j += 1

    youts = np.array(outlist)

    return ti, youts


#Menyelesaikan persamaan ODE dengan metode Runge-Kutta
def rk2ndHeun(funcs=[], init=[], step=0., tspan=[0., 0.]):
    outlist = [init]
    ti = [tspan[0]]
    j = 0
    for tn in np.arange(tspan[0], tspan[1], step):
        k = 0
        yn = []
        for func in funcs:
            k1 = func(ti[j], *outlist[j])
            args = [a+k1*step for a in outlist[j]].copy()
            k2 = func(ti[j]+step, *args)
            yi = outlist[j][k] + (0.5*k1 + 0.5*k2)*step
            yn.append(yi)
            k += 1

        outlist.append(yn)
        ti.append(tn)
        j += 1

    youts = np.array(outlist)

    return ti, youts


def rk2ndMid(funcs=[], init=[], step=0., tspan=[0., 0.]):
    outlist = [init]
    ti = [tspan[0]]
    j = 0
    for tn in np.arange(tspan[0], tspan[1], step):
        k = 0
        yn = []
        for func in funcs:
            k1 = func(ti[j], *outlist[j])
            args = [a+0.5*k1*step for a in outlist[j]].copy()
            k2 = func(ti[j]+0.5*step, *args)
            yi = outlist[j][k] + k2*step
            yn.append(yi)
            k += 1

        outlist.append(yn)
        ti.append(tn)
        j += 1

    youts = np.array(outlist)

    return ti, youts


def rk2ndRols(funcs=[], init=[], step=0., tspan=[0., 0.]):
    outlist = [init]
    ti = [tspan[0]]
    j = 0
    for tn in np.arange(tspan[0], tspan[1], step):
        k = 0
        yn = []
        for func in funcs:
            k1 = func(ti[j], *outlist[j])
            args = [a+(3/4)*k1*step for a in outlist[j]].copy()
            k2 = func(ti[j]+(3/4)*step, *args)
            yi = outlist[j][k] + ((1/3)*k1 + (2/3)*k2)*step
            yn.append(yi)
            k += 1

        outlist.append(yn)
        ti.append(tn)
        j += 1

    youts = np.array(outlist)

    return ti, youts


def rk4th(funcs=[], init=[], step=0., tspan=[0., 0.]):
    outlist = [init]
    ti = [tspan[0]]
    j = 0
    for tn in np.arange(tspan[0], tspan[1], step):
        k = 0
        yn = []
        for func in funcs:
            k1 = func(ti[j], *outlist[j])
            args1 = [a+0.5*k1*step for a in outlist[j]].copy()
            k2 = func(ti[j]+0.5*step, *args1)
            args2 = [a+0.5*k2*step for a in outlist[j]].copy()
            k3 = func(ti[j]+0.5*step, *args2)
            args3 = [a+k3*step for a in outlist[j]].copy()
            k4 = func(ti[j]+step, *args3)
            yi = outlist[j][k] + (k1 + 2.*k2 + 2.*k + k4)*step*(1./6.)
            yn.append(yi)
            k += 1

        outlist.append(yn)
        ti.append(tn)
        j += 1

    youts = np.array(outlist)

    return ti, youts


time, outs = rk4th(funcs=[z1dot, z2dot], init=[z10, z20], step=0.01, tspan=[0., 30.])
plt.grid(True)
plt.xlim([-1, 30.])
plt.plot(time, outs[:, 0])