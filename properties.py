from scipy import optimize
import math
from math import log, exp, sqrt
import numpy as np
from .formulation import *
from ._koefisien_ import bigr, rhoc, tempc, tempt, presst

#inisialisasi
__residu__ = ResiduPart()
__ideal__ = IdealPart()
__ideal2__ = IdealPart2()


#Saturasi
def getSaturDeltas(tsat):

    if not math.isclose(tsat, tempc, abs_tol=1e-3):
        deltas0 = initDeltas(tsat)
        deltas = optimize.fsolve(SaturDeltas, x0=np.array(deltas0), args=(tsat,))
        return list(deltas)
    else:
        deltas = optimize.fsolve(SaturDeltas, x0=np.array([0.99999999, 0.99999999]), args=(tsat,))
        return list(deltas)


def getSaturPress(tsat):
    """Fungsi untuk mendapatkan data tekanan, dan massa jenis pada titik saturasi dengan data suhu/temperatur"""

    tau1 = tempc/tsat
    c1 = rhoc*bigr*tsat
    if not math.isclose(tsat, tempc, abs_tol=1e-3):
        delta0, delta1 = getSaturDeltas(tsat)
        phi = __residu__.phi(delta0=delta0, tau0=tau1)
        phi2 = __residu__.phi(delta0=delta1, tau0=tau1)
        d = (1./delta1)-(1./delta0)
        p = (c1*(phi-phi2) + c1*log(delta0/delta1))/d
        return p
    else:
        delta0, delta1 = getSaturDeltas(tsat)
        phi1 = __residu__.parPhiDelta(delta0=delta0, tau0=tau1)
        p = rhoc*bigr*tsat*delta0*(1+delta0*phi1)
        return p


def getSaturTemp(psat):
    """Method untuk mendapatkan suhu/temperatur, dan massa jenis pada titik saturasi dengan data tekanan"""

    tau0 = optimize.fsolve(initTau, x0=np.array([1.]), args=(psat,))
    if psat != pressc:
        t0 = tempc/tau0[0]
        delta1, delta2 = getSaturDeltas(t0)
        t = list(optimize.fsolve(SaturTau, x0=np.array([tau0[0], delta1, delta2]), args=(psat,)))
        return tempc/t[0]
    else:
        t = list(optimize.fsolve(SaturTau, x0=np.array([tau0[0], 0.99999999, 0.99999999]), args=(psat,)))
        return tempc/t[0]


#Satu fase
def getDelta(delta0, p, t):
    ans = optimize.fsolve(SingleDelta, x0=np.array([delta0]), args=(p, t))
    return ans[0]


#Energi
def getSpecInternal(delta, t):
    tau = tempc/t

    if t == tempt:
        phi1 = __ideal2__.parPhiTau(tau)
    else:
        phi1 = __ideal__.parPhiTau(tau)

    phi2 = __residu__.parPhiTau(delta0=delta, tau0=tau)
    ans = bigr*t*tau*(phi1+phi2)
    return ans


def getSpecEntropy(delta, t):
    tau = tempc/t

    if t == tempt:
        phi1 = __ideal2__.parPhiTau(tau0=tau)
        phi2 = __ideal2__.phi(delta0=delta, tau0=tau)
    else:
        phi1 = __ideal__.parPhiTau(tau0=tau)
        phi2 = __ideal__.phi(delta0=delta, tau0=tau)

    phi3 = __residu__.parPhiTau(delta0=delta, tau0=tau)
    phi4 = __residu__.phi(delta0=delta, tau0=tau)
    ans = bigr*tau*(phi1+phi3)-bigr*(phi2+phi4)
    return ans


def getSpecEnthalpy(delta, t):
    tau = tempc/t

    if t == tempt:
        phi1 = __ideal2__.parPhiTau(tau0=tau)
    else:
        phi1 = __ideal__.parPhiTau(tau0=tau)

    phi2 = __residu__.parPhiTau(delta0=delta, tau0=tau)
    phi3 = __residu__.parPhiDelta(delta0=delta, tau0=tau)
    ans = bigr*t+bigr*t*tau*(phi1+phi2)+bigr*t*delta*phi3
    return ans


def getCv(delta, t):
    tau = tempc/t

    if t == tempt:
        phi1 = __ideal2__.parPhiTau2(tau0=tau)
    else:
        phi1 = __ideal__.parPhiTau2(tau0=tau)

    phi2 = __residu__.parPhiTau2(delta0=delta, tau0=tau)
    ans = -bigr*(tau**2)*(phi1+phi2)
    return ans


def getCp(delta, t):
    tau = tempc/t

    if t == tempt:
        phi1 = __ideal2__.parPhiTau2(tau0=tau)
    else:
        phi1 = __ideal__.parPhiTau2(tau0=tau)

    phi2 = __residu__.parPhiTau2(delta0=delta, tau0=tau)
    phi3 = __residu__.parPhiDelta(delta0=delta, tau0=tau)
    phi4 = __residu__.parPhiDelta2(delta0=delta, tau0=tau)
    phi5 = __residu__.parPhiDeltaTau(delta0=delta, tau0=tau)
    eq1 = 1 + delta*phi3 - delta*tau*phi5
    eq2 = 1 + 2*delta*phi3 + (delta**2)*phi4

    ans = -bigr*(tau**2)*(phi1+phi2) + bigr*((eq1**2)/eq2)
    return ans