from math import log, log1p, exp, isclose
from scipy import optimize
import numpy as np
from .koefisien import bigr, tempc, pressc, rhoc, koefReg3, koefB3, koefSubReg3
from .region4 import getSaturPress, getSaturTemp
from .boundary import Bound3


class __BasicReg3__:
    """Persamaan2 dasar untuk region 3"""

    def __init__(self):
        self.n = koefReg3["n"]
        self.capi = koefReg3["capi"]
        self.capj = koefReg3["capj"]

    def phi(self, delta0, tau0):
        ans = self.n[0]*log(delta0)
        for k in range(1, 40):
            ans += self.n[k]*(delta0**self.capi[k])*(tau0**self.capj[k])
        return ans

    def parPhiDelta(self, delta0, tau0):
        ans = self.n[0]/delta0
        for k in range(1, 40):
            pw = self.capi[k]-1
            ans += self.n[k]*self.capi[k]*(delta0**pw)*(tau0**self.capj[k])
        return ans

    def parPhiDelta2(self, delta0, tau0):
        ans = -self.n[0]/(delta0**2)
        for k in range(1, 40):
            pw = self.capi[k]-2
            ans += self.n[k]*self.capi[k]*(self.capi[k]-1)*(delta0**pw)*(tau0**self.capj[k])
        return ans

    def parPhiTau(self, delta0, tau0):
        ans = 0.
        for k in range(1, 40):
            pw = self.capj[k]-1
            ans += self.n[k]*self.capj[k]*(delta0**self.capi[k])*(tau0**pw)
        return ans

    def parPhiTau2(self, delta0, tau0):
        ans = 0.
        for k in range(1, 40):
            pw = self.capj[k]-2
            ans += self.n[k]*self.capj[k]*(self.capj[k]-1)*(delta0**self.capi[k])*(tau0**pw)
        return ans

    def parPhiDeltaTau(self, delta0, tau0):
        ans = 0.
        for k in range(1, 40):
            pw = self.capi[k]-1
            pw1 = self.capj[k]-1
            ans += self.n[k]*self.capi[k]*self.capj[k]*(delta0**pw)*(tau0**pw1)
        return ans


class PropReg3:

    def __init__(self):
        self.basic = __BasicReg3__()

    def __SingleDelta__(self, delta, p, t):
        tau = tempc/t
        c = p/(rhoc*bigr*t)
        phi = self.basic.parPhiDelta(delta0=delta, tau0=tau)
        ans = (delta**2)*phi - c
        return ans

    def __dfunc__(self, delta, p, t):
        tau = tempc/t
        phi1 = self.basic.parPhiDelta(delta0=delta, tau0=tau)
        phi2 = self.basic.parPhiDelta2(delta0=delta, tau0=tau)
        return 2*delta*phi1 + (delta**2)*phi2

    def __dfunc2__(self, delta, delta1, t):
        tau = tempc/t
        phi1 = self.basic.parPhiDelta(delta0=delta, tau0=tau)
        phi2 = self.basic.parPhiDelta2(delta0=delta, tau0=tau)
        return -2*delta*phi1 - (delta**2)*phi2

    def __SaturDeltag__(self, delta, delta1, t):
        tau = tempc/t
        phi1 = self.basic.parPhiDelta(delta0=delta, tau0=tau)
        phi2 = self.basic.parPhiDelta(delta0=delta1, tau0=tau)
        return (delta1**2)*phi2 - (delta**2)*phi1

    def getRho(self, p, t):
        ans = optimize.newton(self.__SingleDelta__, fprime=self.__dfunc__, x0=1.7, args=(p, t))
        return ans*rhoc

    def getSatRho(self, tsat):
        psat = getSaturPress(tsat0=tsat)
        delta1 = optimize.newton(func=self.__SingleDelta__, fprime=self.__dfunc__, x0=1.7, args=(psat, tsat))
        delta2 = optimize.newton(func=self.__SaturDeltag__, fprime=self.__dfunc2__, x0=0.1, args=(delta1, tsat))
        return delta1*rhoc, delta2*rhoc

    def getSpecInternal(self, rho, t):
        delta = rho/rhoc
        tau = tempc/t
        phi = self.basic.parPhiTau(delta0=delta, tau0=tau)
        ans = bigr*t*tau*phi
        return ans

    def getSpecEntropy(self, rho, t):
        delta = rho/rhoc
        tau = tempc/t
        phi1 = self.basic.parPhiTau(delta0=delta, tau0=tau)
        phi2 = self.basic.phi(delta0=delta, tau0=tau)
        ans = bigr*tau*phi1-bigr*phi2
        return ans

    def getSpecEnthalpy(self, rho, t):
        delta = rho/rhoc
        tau = tempc/t
        phi1 = self.basic.parPhiTau(delta0=delta, tau0=tau)
        phi2 = self.basic.parPhiDelta(delta0=delta, tau0=tau)
        ans = bigr*t*(tau*phi1+delta*phi2)
        return ans

    def getCv(self, rho, t):
        delta = rho/rhoc
        tau = tempc/t
        phi = self.basic.parPhiTau2(delta0=delta, tau0=tau)
        ans = -bigr*(tau**2)*phi
        return ans

    def getCp(self, rho, t):
        delta = rho/rhoc
        tau = tempc/t
        phi1 = self.basic.parPhiDelta(delta0=delta, tau0=tau)
        phi2 = self.basic.parPhiDelta2(delta0=delta, tau0=tau)
        phi3 = self.basic.parPhiDeltaTau(delta0=delta, tau0=tau)
        ans1 = ((delta*phi1-delta*tau*phi3)**2)/(2*delta*phi1+(delta**2)*phi2)
        phi4 = self.basic.parPhiTau2(delta0=delta, tau0=tau)
        ans = -bigr*(tau**2)*phi4+bigr*ans1
        return ans


#Persamaan2 kebalikan region 3
class __BackReg3PT__:
    """Persamaan kebalikan untuk region 3 untuk input (P, T)"""

    def __init__(self):
        self._koef = None
        self.vol0 = None
        self.press0 = None
        self.temp0 = None
        self.N = None
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.e = None
        self.n = None
        self.capi = None
        self.capj = None

    def setKoef(self, koef):
        self._koef = koef.copy()
        self.vol0 = self._koef["vol0"]
        self.press0 = self._koef["press0"]
        self.temp0 = self._koef["temp0"]
        self.N = self._koef["N"]
        self.a = self._koef["a"]
        self.b = self._koef["b"]
        self.c = self._koef["c"]
        self.d = self._koef["d"]
        self.e = self._koef["e"]
        self.n = self._koef["n"]
        self.capi = self._koef["capi"]
        self.capj = self._koef["capj"]

    def omega(self, p0, t0):
        pi = p0/self.press0
        theta = t0/self.temp0
        ans = 0.
        for k in range(self.N):
            ans1 = (pi-self.a)**self.c
            ans2 = (theta-self.b)**self.d
            ans += self.n[k]*(ans1**self.capi[k])*(ans2**self.capj[k])
        return (ans**self.e)*self.vol0

    def omega3n(self, p0, t0):
        pi = p0/self.press0
        theta = t0/self.temp0
        ans = 0.
        for k in range(self.N):
            ans += self.n[k]*((pi-self.a)**self.capi[k])*((theta-self.b)**self.capj[k])
        return exp(ans)*self.vol0


class PropPTReg3:

    def __init__(self):
        self.bound = Bound3()
        self.back = __BackReg3PT__()
        self.koef3ab = koefB3["3ab"]
        self.koef3cd = koefB3["3cd"]
        self.koef3gh = koefB3["3gh"]
        self.koef3ij = koefB3["3ij"]
        self.koef3jk = koefB3["3jk"]
        self.koef3mn = koefB3["3mn"]
        self.koef3op = koefB3["3op"]
        self.koef3qu = koefB3["3qu"]
        self.koef3rx = koefB3["3rx"]
        self.koef3uv = koefB3["3uv"]
        self.koef3wx = koefB3["3wx"]
        self.koef3a = koefSubReg3["koef3a"]
        self.koef3b = koefSubReg3["koef3b"]
        self.koef3c = koefSubReg3["koef3c"]
        self.koef3d = koefSubReg3["koef3d"]
        self.koef3e = koefSubReg3["koef3e"]
        self.koef3f = koefSubReg3["koef3f"]
        self.koef3g = koefSubReg3["koef3g"]
        self.koef3h = koefSubReg3["koef3h"]
        self.koef3i = koefSubReg3["koef3i"]
        self.koef3j = koefSubReg3["koef3j"]
        self.koef3k = koefSubReg3["koef3k"]
        self.koef3l = koefSubReg3["koef3l"]
        self.koef3m = koefSubReg3["koef3m"]
        self.koef3n = koefSubReg3["koef3n"]
        self.koef3o = koefSubReg3["koef3o"]
        self.koef3p = koefSubReg3["koef3p"]
        self.koef3q = koefSubReg3["koef3q"]
        self.koef3r = koefSubReg3["koef3r"]
        self.koef3s = koefSubReg3["koef3s"]
        self.koef3t = koefSubReg3["koef3t"]
        self.koef3u = koefSubReg3["koef3u"]
        self.koef3v = koefSubReg3["koef3v"]
        self.koef3w = koefSubReg3["koef3w"]
        self.koef3x = koefSubReg3["koef3x"]
        self.koef3y = koefSubReg3["koef3y"]
        self.koef3z = koefSubReg3["koef3z"]

    def getSpecVol(self, p, t):
        """Volume jenis untuk region 3 dengan input (P, T)"""

        self.bound.setKoef(koef=self.koef3ab)
        t3ab = self.bound.getTemp2(p)
        self.bound.setKoef(koef=self.koef3cd)
        t3cd = self.bound.getTemp(p)
        t3ef = self.bound.getTemp3(p)
        self.bound.setKoef(koef=self.koef3gh)
        t3gh = self.bound.getTemp(p)
        self.bound.setKoef(koef=self.koef3ij)
        t3ij = self.bound.getTemp(p)
        self.bound.setKoef(koef=self.koef3jk)
        t3jk = self.bound.getTemp(p)
        self.bound.setKoef(koef=self.koef3mn)
        t3mn = self.bound.getTemp(p)
        self.bound.setKoef(koef=self.koef3op)
        t3op = self.bound.getTemp2(p)
        self.bound.setKoef(koef=self.koef3qu)
        t3qu = self.bound.getTemp(p)
        self.bound.setKoef(koef=self.koef3rx)
        t3rx = self.bound.getTemp(p)
        self.bound.setKoef(koef=self.koef3uv)
        t3uv = self.bound.getTemp(p)
        self.bound.setKoef(koef=self.koef3wx)
        t3wx = self.bound.getTemp2(p)

        psat0 = getSaturPress(tsat0=623.15)
        tsat0 = getSaturTemp(psat0=p)
        p3cd = 1.900_881_189_173_929e4
        psat1 = 2.193_161_551e4
        psat2 = 2.190_096_265e4
        psat3 = getSaturPress(tsat0=643.15)

        ans = 0.
        if ((p > 4e4) and (p < 1e5)) or isclose(p, 1e5, abs_tol=1e-14):
            if (t < t3ab) or isclose(t, t3ab, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3a)
                ans = self.back.omega(p0=p, t0=t)
            elif t > t3ab:
                self.back.setKoef(koef=self.koef3b)
                ans = self.back.omega(p0=p, t0=t)
        elif ((p > 25e3) and (p < 4e4)) or isclose(p, 4e4, abs_tol=1e-14):
            if (t < t3cd) or isclose(t, t3cd, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3c)
                ans = self.back.omega(p0=p, t0=t)
            elif ((t > t3cd) and (t < t3ab)) or isclose(t, t3ab, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3d)
                ans = self.back.omega(p0=p, t0=t)
            elif ((t > t3ab) and (t < t3ef)) or isclose(t, t3ef, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3e)
                ans = self.back.omega(p0=p, t0=t)
            elif t > t3ef:
                self.back.setKoef(koef=self.koef3f)
                ans = self.back.omega(p0=p, t0=t)
        elif ((p > 23.5e3) and (p < 25e3)) or isclose(p, 25e3, abs_tol=1e-14):
            if (t < t3cd) or isclose(t, t3cd, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3c)
                ans = self.back.omega(p0=p, t0=t)
            elif ((t > t3cd) and (t < t3gh)) or isclose(t, t3gh, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3g)
                ans = self.back.omega(p0=p, t0=t)
            elif ((t > t3gh) and (t < t3ef)) or isclose(t, t3ef, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3h)
                ans = self.back.omega(p0=p, t0=t)
            elif ((t > t3ef) and (t < t3ij)) or isclose(t, t3ij, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3i)
                ans = self.back.omega(p0=p, t0=t)
            elif ((t > t3ij) and (t < t3jk)) or isclose(t, t3jk, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3j)
                ans = self.back.omega(p0=p, t0=t)
            elif t > t3jk:
                self.back.setKoef(koef=self.koef3k)
                ans = self.back.omega(p0=p, t0=t)
        elif ((p > 23e3) and (p < 23.5e3)) or isclose(p, 23.5e3, abs_tol=1e-14):
            if (t < t3cd) or isclose(t, t3cd, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3c)
                ans = self.back.omega(p0=p, t0=t)
            elif ((t > t3cd) and (t < t3gh)) or isclose(t, t3gh, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3l)
                ans = self.back.omega(p0=p, t0=t)
            elif ((t > t3gh) and (t < t3ef)) or isclose(t, t3ef, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3h)
                ans = self.back.omega(p0=p, t0=t)
            elif ((t > t3ef) and (t < t3ij)) or isclose(t, t3ij, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3i)
                ans = self.back.omega(p0=p, t0=t)
            elif ((t > t3ij) and (t < t3jk)) or isclose(t, t3jk, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3j)
                ans = self.back.omega(p0=p, t0=t)
            elif t > t3jk:
                self.back.setKoef(koef=self.koef3k)
                ans = self.back.omega(p0=p, t0=t)
        elif ((p > 22.5e3) and (p <= 23e3)) or isclose(p, 23e3, abs_tol=1e-14):
            if (t < t3cd) or isclose(t, t3cd, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3c)
                ans = self.back.omega(p0=p, t0=t)
            elif ((t > t3cd) and (t < t3gh)) or isclose(t, t3gh, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3l)
                ans = self.back.omega(p0=p, t0=t)
            elif ((t > t3gh) and (t < t3mn)) or isclose(t, t3mn, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3m)
                ans = self.back.omega(p0=p, t0=t)
            elif ((t > t3mn) and (t < t3ef)) or isclose(t, t3ef, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3n)
                ans = self.back.omega3n(p0=p, t0=t)
            elif ((t > t3ef) and (t < t3op)) or isclose(t, t3op, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3o)
                ans = self.back.omega(p0=p, t0=t)
            elif ((t > t3op) and (t < t3ij)) or isclose(t, t3ij, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3p)
                ans = self.back.omega(p0=p, t0=t)
            elif ((t > t3ij) and (t < t3jk)) or isclose(t, t3jk, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3j)
                ans = self.back.omega(p0=p, t0=t)
            elif t > t3jk:
                self.back.setKoef(koef=self.koef3k)
                ans = self.back.omega(p0=p, t0=t)
        elif ((p > 21.043_367_32e3) and (p < 22.5e3)) or isclose(p, 22.5e3, abs_tol=1e-14):
            if (t < t3cd) or isclose(t, t3cd, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3c)
                ans = self.back.omega(p0=p, t0=t)
            elif ((t > t3cd) and (t < t3qu)) or isclose(t, t3qu, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3q)
                ans = self.back.omega(p0=p, t0=t)
            elif ((t > t3rx) and (t < t3jk)) or isclose(t, t3jk, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3r)
                ans = self.back.omega(p0=p, t0=t)
            elif t > t3jk:
                self.back.setKoef(koef=self.koef3k)
                ans = self.back.omega(p0=p, t0=t)
        elif ((p > 20.5e3) and (p < 21.043_367_32e3)) or isclose(p, 21.043_367_32e3, abs_tol=1e-9):
            tsat = _reg4.getSaturTemp(psat0=p)
            if (t < t3cd) or isclose(t, t3cd, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3c)
                ans = self.back.omega(p0=p, t0=t)
            elif ((t > t3cd) and (t < tsat)) or isclose(t, tsat, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3s)
                ans = self.back.omega(p0=p, t0=t)
            elif ((t > tsat) and (t < t3jk)) or isclose(t, t3jk, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3r)
                ans = self.back.omega(p0=p, t0=t)
            elif t > t3jk:
                self.back.setKoef(koef=self.koef3k)
                ans = self.back.omega(p0=p, t0=t)
        elif ((p > p3cd) and (p < 20.5e3)) or isclose(p, 20.5e3, abs_tol=1e-9):
            tsat = _reg4.getSaturTemp(psat0=p)
            if (t < t3cd) or isclose(t, t3cd, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3c)
                ans = self.back.omega(p0=p, t0=t)
            elif ((t > t3cd) and (t < tsat)) or isclose(t, tsat, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3s)
                ans = self.back.omega(p0=p, t0=t)
            elif t > tsat:
                self.back.setKoef(koef=self.koef3t)
                ans = self.back.omega(p0=p, t0=t)
        elif ((p > psat0) and (p < p3cd)) or isclose(p, p3cd, abs_tol=1e-14):
            tsat = _reg4.getSaturTemp(psat0=p)
            if (t < tsat) or isclose(t, tsat, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3c)
                ans = self.back.omega(p0=p, t0=t)
            elif t > tsat:
                self.back.setKoef(koef=self.koef3t)
                ans = self.back.omega(p0=p, t0=t)

        #Untuk region melebihi tekanan kritis
        if ((p > 22.11e3) and (p < 22.5e3)) or isclose(p, 22.5e3, abs_tol=1e-14):
            if ((t > t3qu) and (t < t3uv)) or isclose(t, t3uv, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3u)
                ans = self.back.omega(p0=p, t0=t)
            elif ((t > t3uv) and (t < t3ef)) or isclose(t, t3ef, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3v)
                ans = self.back.omega(p0=p, t0=t)
            elif ((t > t3ef) and (t < t3wx)) or isclose(t, t3wx, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3w)
                ans = self.back.omega(p0=p, t0=t)
            elif ((t > t3wx) and (t < t3rx)) or isclose(t, t3rx, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3x)
                ans = self.back.omega(p0=p, t0=t)
        elif ((p > 22.064e3) and (p < 22.11e3)) or isclose(p, 22.11e3, abs_tol=1e-14):
            if ((t > t3qu) and (t < t3uv)) or isclose(t, t3uv, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3u)
                ans = self.back.omega(p0=p, t0=t)
            elif ((t > t3uv) and (t < t3ef)) or isclose(t, t3ef, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3y)
                ans = self.back.omega(p0=p, t0=t)
            elif ((t > t3ef) and (t < t3wx)) or isclose(t, t3wx, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3z)
                ans = self.back.omega(p0=p, t0=t)
            elif ((t > t3wx) and (t < t3rx)) or isclose(t, t3rx, abs_tol=1e-9):
                self.back.setKoef(koef=self.koef3x)
                ans = self.back.omega(p0=p, t0=t)

        #Untuk region disekitar titik kritis
        if t < tsat0:
            if ((p > psat1) and (p < 22.064e3)) or isclose(p, 22.064e3, abs_tol=1e-6):
                if ((t > t3qu) and (t < t3uv)) or isclose(t, t3uv, abs_tol=1e-9):
                    self.back.setKoef(koef=self.koef3u)
                    ans = self.back.omega(p0=p, t0=t)
                elif t > t3uv:
                    self.back.setKoef(koef=self.koef3y)
                    ans = self.back.omega(p0=p, t0=t)
            elif ((p > psat3) and (p < psat1)) or isclose(p, psat1, abs_tol=1e-14):
                if t > t3qu:
                    self.back.setKoef(koef=self.koef3u)
                    ans = self.back.omega(p0=p, t0=t)
        elif t > tsat0 or isclose(t, tsat0, abs_tol=1e-9) or isclose(t, tsat0, abs_tol=1e-9):
            if ((p > psat2) and (p < 22.064e3)) or isclose(p, 22.064e3, abs_tol=1e-6):
                if (t < t3wx) or isclose(t, t3wx, abs_tol=1e-9):
                    self.back.setKoef(koef=self.koef3z)
                    ans = self.back.omega(p0=p, t0=t)
                elif ((t > t3wx) and (t < t3rx)) or isclose(t, t3rx, abs_tol=1e-9):
                    self.back.setKoef(koef=self.koef3x)
                    ans = self.back.omega(p0=p, t0=t)
            elif ((p > psat3) and (p < psat2)) or isclose(p, psat2, abs_tol=1e-9):
                if (t < t3rx) or isclose(t, t3rx, abs_tol=1e-9):
                    self.back.setKoef(koef=self.koef3x)
                    ans = self.back.omega(p0=p, t0=t)

        return ans