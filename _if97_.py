import math
from .region1 import PropReg1
from .region2 import PropReg2a, PropReg2b
from .region3 import PropReg3, PropPTReg3
from .region4 import getSaturTemp
from .region4 import getSaturPress
from .region5 import PropReg5
from .boundary import Bound23
from .koefisien import bigr, rhoc, tempc, pressc, presst, tempt


def singlephase(P0, T0):

    ans = dict()

    Prop1 = PropReg1()
    Prop2 = PropReg2a()
    Prop4 = PropReg3()
    Prop5 = PropReg5()
    Prop6 = PropPTReg3()
    B23 = Bound23()
    SatPress = getSaturPress

    if (T0 > 273.15) and (T0 <= 623.15):
        psat0 = SatPress(tsat0=T0)
        if (P0 > psat0) and (P0 <= 1e5):
            ans["v"] = Prop1.getSpecVol(P0, T0)
            ans["h"] = Prop1.getSpecEnthalpy(P0, T0)
            ans["s"] = Prop1.getSpecEntropy(P0, T0)
            ans["u"] = Prop1.getSpecInternal(P0, T0)
            ans["Cv"] = Prop1.getCv(P0, T0)
            ans["Cp"] = Prop1.getCp(P0, T0)
        elif (P0 > 0) and (P0 < psat0):
            ans["v"] = Prop2.getSpecVol(P0, T0)
            ans["h"] = Prop2.getSpecEnthalpy(P0, T0)
            ans["s"] = Prop2.getSpecEntropy(P0, T0)
            ans["u"] = Prop2.getSpecInternal(P0, T0)
            ans["Cv"] = Prop2.getCv(P0, T0)
            ans["Cp"] = Prop2.getCp(P0, T0)
    elif (T0 > 623.15) and (T0 <= 863.15):
        p23 = B23.getPress(t0=T0)
        if (P0 > 0) and (P0 < p23):
            ans["v"] = Prop2.getSpecVol(P0, T0)
            ans["h"] = Prop2.getSpecEnthalpy(P0, T0)
            ans["s"] = Prop2.getSpecEntropy(P0, T0)
            ans["u"] = Prop2.getSpecInternal(P0, T0)
            ans["Cv"] = Prop2.getCv(P0, T0)
            ans["Cp"] = Prop2.getCp(P0, T0)
        elif (P0 >= p23) and (P0 <= 1e5):
            v = Prop6.getSpecVol(P0, T0)
            rho = 1./v
            ans["v"] = Prop6.getSpecVol(P0, T0)
            ans["h"] = Prop4.getSpecEnthalpy(rho, T0)
            ans["s"] = Prop4.getSpecEntropy(rho, T0)
            ans["u"] = Prop4.getSpecInternal(rho, T0)
            ans["Cv"] = Prop4.getCv(rho, T0)
            ans["Cp"] = Prop4.getCp(rho, T0)
    elif (T0 > 863.15) and (T0 <= 1073.15):
        if (P0 > 0) and (P0 <= 1e5):
            ans["v"] = Prop2.getSpecVol(P0, T0)
            ans["h"] = Prop2.getSpecEnthalpy(P0, T0)
            ans["s"] = Prop2.getSpecEntropy(P0, T0)
            ans["u"] = Prop2.getSpecInternal(P0, T0)
            ans["Cv"] = Prop2.getCv(P0, T0)
            ans["Cp"] = Prop2.getCp(P0, T0)
    elif (T0 > 1073.15) and (T0 <= 2273.15):
        if (P0 > 0) and (P0 <= 50e3):
            ans["v"] = Prop5.getSpecVol(P0, T0)
            ans["h"] = Prop5.getSpecEnthalpy(P0, T0)
            ans["s"] = Prop5.getSpecEntropy(P0, T0)
            ans["u"] = Prop5.getSpecInternal(P0, T0)
            ans["Cv"] = Prop5.getCv(P0, T0)
            ans["Cp"] = Prop5.getCp(P0, T0)

    return ans


def saturation(Psat0=None, Tsat0=None, x0=None):

    ans = dict()

    Prop1 = PropReg1()
    Prop2 = PropReg2a()
    Prop3 = PropReg3()
    Prop4 = PropReg2b()
    SatTemp = getSaturTemp
    SatPress = getSaturPress

    if (Psat0 is None) and (Tsat0 is not None) and (x0 is None):
        if (Tsat0 > 273.15) and (Tsat0 <= 623.15):
            psat0 = SatPress(tsat0=Tsat0)
            ans["Psat"] = round(psat0, 8)
            ans["Tsat"] = Tsat0
            ans["vf"] = Prop1.getSpecVol(p=psat0, t=Tsat0)
            ans["vg"] = Prop2.getSpecVol(p=psat0, t=Tsat0)
            ans["hf"] = Prop1.getSpecEnthalpy(p=psat0, t=Tsat0)
            ans["hg"] = Prop2.getSpecEnthalpy(p=psat0, t=Tsat0)
            ans["sf"] = Prop1.getSpecEntropy(p=psat0, t=Tsat0)
            ans["sg"] = Prop2.getSpecEntropy(p=psat0, t=Tsat0)
            ans["uf"] = Prop1.getSpecInternal(p=psat0, t=Tsat0)
            ans["ug"] = Prop2.getSpecInternal(p=psat0, t=Tsat0)
            ans["Cvf"] = Prop1.getCv(p=psat0, t=Tsat0)
            ans["Cvg"] = Prop2.getCv(p=psat0, t=Tsat0)
            ans["Cpf"] = Prop1.getCp(p=psat0, t=Tsat0)
            ans["Cpg"] = Prop2.getCp(p=psat0, t=Tsat0)
        elif (Tsat0 > 623.15) and (Tsat0 < tempc):
            psat0 = SatPress(tsat0=Tsat0)
            rhoes = Prop3.getSatRho(Tsat0)
            ans["Psat"] = round(psat0, 8)
            ans["Tsat"] = Tsat0
            ans["vf"] = 1./rhoes[0]
            ans["vg"] = 1./rhoes[1]
            ans["hf"] = Prop3.getSpecEnthalpy(rho=rhoes[0], t=Tsat0)
            ans["hg"] = Prop3.getSpecEnthalpy(rho=rhoes[1], t=Tsat0)
            ans["sf"] = Prop3.getSpecEntropy(rho=rhoes[0], t=Tsat0)
            ans["sg"] = Prop3.getSpecEntropy(rho=rhoes[1], t=Tsat0)
            ans["uf"] = Prop3.getSpecInternal(rho=rhoes[0], t=Tsat0)
            ans["ug"] = Prop3.getSpecInternal(rho=rhoes[1], t=Tsat0)
            ans["Cvf"] = Prop3.getCv(rho=rhoes[0], t=Tsat0)
            ans["Cvg"] = Prop3.getCv(rho=rhoes[1], t=Tsat0)
            ans["Cpf"] = Prop3.getCp(rho=rhoes[0], t=Tsat0)
            ans["Cpg"] = Prop3.getCp(rho=rhoes[1], t=Tsat0)
        elif math.isclose(Tsat0, tempc, abs_tol=1e-4):
            psat0 = SatPress(tsat0=Tsat0)
            rhoes = Prop3.getSatRho(Tsat0)
            ans["Psat"] = round(psat0,8)
            ans["Tsat"] = Tsat0
            ans["vf"] = 1./round(rhoes[0])
            ans["vg"] = 1./round(rhoes[1])
            ans["hf"] = Prop3.getSpecEnthalpy(rho=round(rhoes[0]), t=Tsat0)
            ans["hg"] = Prop3.getSpecEnthalpy(rho=round(rhoes[1]), t=Tsat0)
            ans["sf"] = Prop3.getSpecEntropy(rho=round(rhoes[0]), t=Tsat0)
            ans["sg"] = Prop3.getSpecEntropy(rho=round(rhoes[1]), t=Tsat0)
            ans["uf"] = Prop3.getSpecInternal(rho=round(rhoes[0]), t=Tsat0)
            ans["ug"] = Prop3.getSpecInternal(rho=round(rhoes[1]), t=Tsat0)
            ans["Cvf"] = Prop3.getCv(rho=rhoes[0], t=Tsat0)
            ans["Cvg"] = Prop3.getCv(rho=rhoes[1], t=Tsat0)
            ans["Cpf"] = Prop3.getCp(rho=rhoes[0], t=Tsat0)
            ans["Cpg"] = Prop3.getCp(rho=rhoes[1], t=Tsat0)
    elif (Psat0 is not None) and (Tsat0 is None) and (x0 is None):
        if (Psat0 >= presst) and (Psat0 <= 16529.2):
            tsat0 = SatTemp(psat0=Psat0)
            ans = saturation(Tsat0=tsat0).copy()
        elif (Psat0 > 16529.2) and (Psat0 < pressc):
            tsat0 = SatTemp(psat0=Psat0)
            ans = saturation(Tsat0=tsat0).copy()
        elif math.isclose(Psat0, pressc, abs_tol=1e-14):
            tsat0 = SatTemp(psat0=Psat0)
            ans = saturation(Tsat0=round(tsat0, 3)).copy()
    elif (Psat0 is None) and (Tsat0 is not None) and (x0 is not None):
        if (Tsat0 > 273.15) and (Tsat0 <= 623.15):
            psat0 = SatPress(tsat0=Tsat0)
            if (psat0 >= presst) and (psat0 <= 10e3):
                if (x0 > 0.95) and (x0 <= 1.):
                    ans0 = saturation(Tsat0=Tsat0).copy()
                    ans["Psat"] = ans0["Psat"]
                    ans["Tsat"] = Tsat0
                    ans["x"] = x0
                    ans["v"] = ans0["vf"] + x0*(ans0["vg"] - ans0["vf"])
                    ans["h"] = ans0["hf"] + x0*(ans0["hg"] - ans0["hf"])
                    ans["s"] = ans0["sf"] + x0*(ans0["sg"] - ans0["sf"])
                    ans["u"] = ans0["uf"] + x0*(ans0["ug"]-ans0["uf"])
                    ans["Cp"] = ans0["Cpf"]+x0*(ans0["Cpg"]-ans0["Cpf"])
                    ans["Cv"] = ans0["Cvf"]+x0*(ans0["Cvg"]-ans0["Cvf"])
                elif (x0 >= 0.) and (x0 <= 0.95):
                    ans0 = saturation(Tsat0=Tsat0).copy()
                    ans0["vg"] = Prop4.getSpecVol(p=psat0, t=Tsat0)
                    ans0["hg"] = Prop4.getSpecEnthalpy(p=psat0, t=Tsat0)
                    ans0["sg"] = Prop4.getSpecEntropy(p=psat0, t=Tsat0)
                    ans0["ug"] = Prop4.getSpecInternal(p=psat0, t=Tsat0)
                    ans0["Cvg"] = Prop4.getCv(p=psat0, t=Tsat0)
                    ans0["Cpg"] = Prop4.getCp(p=psat0, t=Tsat0)
                    ans["Psat"] = ans0["Psat"]
                    ans["Tsat"] = Tsat0
                    ans["x"] = x0
                    ans["v"] = ans0["vf"] + x0*(ans0["vg"] - ans0["vf"])
                    ans["h"] = ans0["hf"] + x0*(ans0["hg"] - ans0["hf"])
                    ans["s"] = ans0["sf"] + x0*(ans0["sg"] - ans0["sf"])
                    ans["u"] = ans0["uf"] + x0*(ans0["ug"] - ans0["uf"])
                    ans["Cp"] = ans0["Cpf"] + x0*(ans0["Cpg"] - ans0["Cpf"])
                    ans["Cv"] = ans0["Cvf"] + x0*(ans0["Cvg"] - ans0["Cvf"])
            elif psat0 > 10e3:
                ans0 = saturation(Tsat0=Tsat0).copy()
                ans["Psat"] = ans0["Psat"]
                ans["Tsat"] = Tsat0
                ans["x"] = x0
                ans["v"] = ans0["vf"] + x0*(ans0["vg"] - ans0["vf"])
                ans["h"] = ans0["hf"] + x0*(ans0["hg"] - ans0["hf"])
                ans["s"] = ans0["sf"] + x0*(ans0["sg"] - ans0["sf"])
                ans["u"] = ans0["uf"] + x0*(ans0["ug"] - ans0["uf"])
                ans["Cp"] = ans0["Cpf"] + x0*(ans0["Cpg"] - ans0["Cpf"])
                ans["Cv"] = ans0["Cvf"] + x0*(ans0["Cvg"] - ans0["Cvf"])
        elif (Tsat0 > 623.15) and (Tsat0 <= tempc):
            ans0 = saturation(Tsat0=Tsat0).copy()
            ans["Psat"] = ans0["Psat"]
            ans["Tsat"] = Tsat0
            ans["x"] = x0
            ans["v"] = ans0["vf"]+x0*(ans0["vg"]-ans0["vf"])
            ans["h"] = ans0["hf"]+x0*(ans0["hg"]-ans0["hf"])
            ans["s"] = ans0["sf"]+x0*(ans0["sg"]-ans0["sf"])
            ans["u"] = ans0["uf"]+x0*(ans0["ug"]-ans0["uf"])
            ans["Cp"] = ans0["Cpf"]+x0*(ans0["Cpg"]-ans0["Cpf"])
            ans["Cv"] = ans0["Cvf"]+x0*(ans0["Cvg"]-ans0["Cvf"])
    elif (Psat0 is not None) and (Tsat0 is None) and (x0 is not None):
        if (Psat0 >= presst) and (Psat0 <= 16529.2):
            tsat0 = SatTemp(psat0=Psat0)
            if (Psat0 >= presst) and (Psat0 <= 10e3):
                if (x0 >= 0.) and (x0 <= 0.95):
                    ans = saturation(Tsat0=tsat0, x0=x0).copy()
                elif (x0 > 0.95) and (x0 <= 1.):
                    ans = saturation(Tsat0=tsat0, x0=x0).copy()
            if Psat0 > 10e3:
                ans = saturation(Tsat0=tsat0, x0=x0)
        elif (Psat0 > 16529.2) and (Psat0 < pressc):
            tsat0 = SatTemp(psat0=Psat0)
            ans = saturation(Tsat0=tsat0, x0=x0).copy()
        elif math.isclose(Psat0, pressc, abs_tol=1e-14):
            tsat0 = SatTemp(psat0=Psat0)
            ans = saturation(Tsat0=round(tsat0, 3), x0=x0).copy()

    return ans


def water97(P=None, T=None, Psat=None, Tsat=None, x=None, desc=None):

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