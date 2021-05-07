from math import log
from .koefisien import bigr, koefReg5


class __IdealPart__:

    def __init__(self):
        self.capj = koefReg5["capjo"]
        self.n = koefReg5["no"]

    def gamma(self, pi0, tau0):
        ans = log(pi0)
        for k in range(6):
            ans += self.n[k]*(tau0**self.capj[k])
        return ans

    def parGammaPi(self, pi0):
        return 1./pi0

    def parGammaPi2(self, pi0):
        return -1./(pi0**2)

    def parGammaTau(self, tau0):
        ans = 0.
        for k in range(6):
            ans += self.n[k]*self.capj[k]*(tau0**(self.capj[k]-1))
        return ans

    def parGammaTau2(self, tau0):
        ans = 0.
        for k in range(6):
            ans += self.n[k]*self.capj[k]*(self.capj[k]-1)*(tau0**(self.capj[k]-2))
        return ans

    def parGammaPiTau(self):
        return 0.


class __ResiduPart__:

    def __init__(self):
        self.capi = koefReg5["capi"]
        self.capj = koefReg5["capj"]
        self.n = koefReg5["n"]

    def gamma(self, pi0, tau0):
        ans = 0.
        for k in range(5):
            ans += self.n[k]*(pi0**self.capi[k])*(tau0**self.capj[k])
        return ans

    def parGammaPi(self, pi0, tau0):
        ans = 0.
        for k in range(5):
            ans += self.n[k]*self.capi[k]*(pi0**(self.capi[k]-1))*(tau0**self.capj[k])
        return ans

    def parGammaPi2(self, pi0, tau0):
        ans = 0.
        for k in range(5):
            ans += self.n[k]*self.capi[k]*(self.capi[k]-1)*(pi0**(self.capi[k]-2))*(tau0**self.capj[k])
        return ans

    def parGammaTau(self, pi0, tau0):
        ans = 0.
        for k in range(5):
            ans += self.n[k]*self.capj[k]*(pi0**self.capi[k])*(tau0**(self.capj[k]-1))
        return ans

    def parGammaTau2(self, pi0, tau0):
        ans = 0.
        for k in range(5):
            ans += self.n[k]*self.capj[k]*(self.capj[k]-1)*(pi0**self.capi[k])*(tau0**(self.capj[k]-2))
        return ans

    def parGammaPiTau(self, pi0, tau0):
        ans = 0.
        for k in range(5):
            ans += self.n[k]*self.capi[k]*self.capj[k]*(pi0**(self.capi[k]-1))*(tau0**(self.capj[k]-1))
        return ans


class PropReg5:

    def __init__(self):
        self.ideal = __IdealPart__()
        self.residu = __ResiduPart__()
        self.p0 = 1000
        self.t0 = 1000

    def getSpecVol(self, p, t):
        pi = p/self.p0
        tau = self.t0/t
        gamma1 = self.ideal.parGammaPi(pi0=pi)
        gamma2 = self.residu.parGammaPi(pi0=pi, tau0=tau)
        ans = ((bigr*t)/p)*pi*(gamma1 + gamma2)
        return ans

    def getSpecInternal(self, p, t):
        pi = p/self.p0
        tau = self.t0/t
        gamma1 = self.ideal.parGammaTau(tau0=tau)
        gamma2 = self.residu.parGammaTau(pi0=pi, tau0=tau)
        gamma3 = self.ideal.parGammaPi(pi0=pi)
        gamma4 = self.residu.parGammaPi(pi0=pi, tau0=tau)
        ans = bigr*t*tau*(gamma1+gamma2)-bigr*t*pi*(gamma3+gamma4)
        return ans

    def getSpecEntropy(self, p, t):
        pi = p/self.p0
        tau = self.t0/t
        gamma1 = self.ideal.parGammaTau(tau0=tau)
        gamma2 = self.residu.parGammaTau(pi0=pi, tau0=tau)
        gamma3 = self.ideal.gamma(pi0=pi, tau0=tau)
        gamma4 = self.residu.gamma(pi0=pi, tau0=tau)
        ans = bigr*tau*(gamma1+gamma2)-bigr*(gamma3+gamma4)
        return ans

    def getSpecEnthalpy(self, p, t):
        pi = p/self.p0
        tau = self.t0/t
        gamma1 = self.ideal.parGammaTau(tau0=tau)
        gamma2 = self.residu.parGammaTau(pi0=pi, tau0=tau)
        ans = bigr*t*tau*(gamma1+gamma2)
        return ans

    def getCp(self, p, t):
        pi = p/self.p0
        tau = self.t0/t
        gamma1 = self.ideal.parGammaTau2(tau0=tau)
        gamma2 = self.residu.parGammaTau2(pi0=pi, tau0=tau)
        ans = -bigr*(tau**2)*(gamma1+gamma2)
        return ans

    def getCv(self, p, t):
        pi = p/self.p0
        tau = self.t0/t
        gamma1 = self.residu.parGammaPi(pi0=pi, tau0=tau)
        gamma2 = self.residu.parGammaPiTau(pi0=pi, tau0=tau)
        gamma3 = self.residu.parGammaPi2(pi0=pi, tau0=tau)
        ans1 = ((1 + pi*gamma1 - tau*pi*gamma3)**2)/(1 - (pi**2)*gamma2)
        gamma4 = self.ideal.parGammaTau2(tau0=tau)
        gamma5 = self.residu.parGammaTau2(pi0=pi, tau0=tau)
        ans = -bigr*(tau**2)*(gamma4+gamma5) - bigr*ans1
        return ans