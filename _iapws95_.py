from .properties import *
from ._koefisien_ import rhoc, tempt, tempc, presst, pressc


def singlephase(P0, T0):
    ans = dict()
    tsat0 = None
    deltas = None

    if (P0 >= presst) and (P0 <= pressc):
        tsat0 = getSaturTemp(psat=P0)
        deltas = getSaturDeltas(tsat=tsat0)
    elif (P0 > pressc) and (P0 <= 1e6):
        tsat0 = tempc
        deltas = [3.1, 1e-6]

    if (tsat0 is not None) and (deltas is not None):
        if (T0 >= 0.) and (T0 < tsat0):
            delta = getDelta(delta0=deltas[0], p=P0, t=T0)
            ans["rho"] = delta*rhoc
            ans["v"] = 1./(delta*rhoc)
            ans["u"] = getSpecInternal(delta, T0)
            ans["h"] = getSpecEnthalpy(delta, T0)
            ans["s"] = getSpecEntropy(delta, T0)
            ans["Cp"] = getCp(delta, T0)
            ans["Cv"] = getCv(delta, T0)
        elif (T0 > tsat0) and (T0 <= 1273.15):
            delta = getDelta(delta0=deltas[1], p=P0, t=T0)
            ans["rho"] = delta*rhoc
            ans["v"] = 1./(delta*rhoc)
            ans["u"] = getSpecInternal(delta, T0)
            ans["h"] = getSpecEnthalpy(delta, T0)
            ans["s"] = getSpecEntropy(delta, T0)
            ans["Cp"] = getCp(delta, T0)
            ans["Cv"] = getCv(delta, T0)

    return ans


def saturation(Psat0=None, Tsat0=None, x0=None):
    ans = dict()

    if (Psat0 is None) and (Tsat0 is not None) and (x0 is None):
        if (Tsat0 >= tempt) and (Tsat0 <= tempc):
            psat0 = getSaturPress(tsat=Tsat0)
            deltas = getSaturDeltas(tsat=Tsat0)
            ans["Psat"] = psat0
            ans["Tsat"] = Tsat0
            ans["rhof"] = rhoc*deltas[0]
            ans["rhog"] = rhoc*deltas[1]
            ans["vf"] = 1./(rhoc*deltas[0])
            ans["vg"] = 1./(rhoc*deltas[1])
            ans["uf"] = getSpecInternal(delta=deltas[0], t=Tsat0)
            ans["ug"] = getSpecInternal(delta=deltas[1], t=Tsat0)
            ans["hf"] = getSpecEnthalpy(delta=deltas[0], t=Tsat0)
            ans["hg"] = getSpecEnthalpy(delta=deltas[1], t=Tsat0)
            ans["sf"] = getSpecEntropy(delta=deltas[0], t=Tsat0)
            ans["sg"] = getSpecEntropy(delta=deltas[1], t=Tsat0)
            ans["Cpf"] = getCp(delta=deltas[0], t=Tsat0)
            ans["Cpg"] = getCp(delta=deltas[1], t=Tsat0)
            ans["Cvf"] = getCv(delta=deltas[0], t=Tsat0)
            ans["Cvg"] = getCv(delta=deltas[1], t=Tsat0)
    elif (Psat0 is not None) and (Tsat0 is None) and (x0 is None):
        if (Psat0 >= presst) and (Psat0 <= pressc):
            tsat0 = getSaturTemp(psat=Psat0)
            ans = saturation(Tsat0=tsat0).copy()
    elif (Psat0 is None) and (Tsat0 is not None) and (x0 is not None):
        if (x0 >= 0.) and (x0 <= 1.):
            ans0 = saturation(Tsat0=Tsat0).copy()
            psat0 = getSaturPress(tsat=Tsat0)
            ans["Psat"] = psat0
            ans["Tsat"] = Tsat0
            ans["x"] = x0
            ans["rho"] = ans0["rhof"] + x0*(ans0["rhog"] - ans0["rhof"])
            ans["v"] = ans0["vf"] + x0*(ans0["vg"] - ans0["vf"])
            ans["u"] = ans0["uf"] + x0*(ans0["ug"] - ans0["uf"])
            ans["h"] = ans0["hf"] + x0*(ans0["hg"] - ans0["hf"])
            ans["s"] = ans0["sf"] + x0*(ans0["sg"] - ans0["sf"])
            ans["Cv"] = ans0["Cvf"] + x0*(ans0["Cvg"] - ans0["Cvf"])
            ans["Cp"] = ans0["Cpf"] + x0*(ans0["Cpg"] - ans0["Cpf"])
    elif (Psat0 is not None) and (Tsat0 is None) and (x0 is not None):
        tsat0 = getSaturTemp(psat=Psat0)
        ans = saturation(Tsat0=tsat0, x0=x0).copy()

    return ans


def water95(P=None, T=None, Psat=None, Tsat=None, x=None, desc=None):

    ans = None

    if (P is not None) and (T is not None) and (Psat is None) and (Tsat is None) and (x is None):
        ans = singlephase(P0=P, T0=T).copy()
    elif (P is None) and (T is None) and (Psat is None) and (Tsat is not None) and (x is None):
        ans = saturation(Tsat0=Tsat).copy()
    elif (P is None) and (T is None) and (Psat is not None) and (Tsat is None) and (x is None):
        ans = saturation(Psat0=Psat).copy()
    elif (P is None) and (T is None) and (Psat is None) and (Tsat is not None) and (x is not None):
        ans = saturation(Tsat0=Tsat, x0=x).copy()
    elif (P is None) and (T is None) and (Psat is not None) and (Tsat is None) and (x is not None):
        ans = saturation(Psat0=Psat, x0=x).copy()

    if desc is None:
        return ans
    elif desc in ans.keys():
        return ans[desc]
    else:
        return None