from math import log
from .koefisien import bigr, koefReg2


class __IdealPart__:

    def __init__(self):
        self.n = koefReg2["no"].copy()
        self.capj = koefReg2["capjo"].copy()

    def gamma(self, pi0, tau0):
        ans = log(pi0)
        for k in range(9):
            ans += self.n[k]*(tau0**self.capj[k])
        return ans

    def parGammaPi(self, pi0):
        return 1/pi0

    def parGammaPi2(self, pi0):
        return -1/(pi0**2)

    def parGammaTau(self, tau0):
        ans = 0.
        for k in range(9):
            ans += self.n[k]*self.capj[k]*(tau0**(self.capj[k]-1))
        return ans

    def parGammaTau2(self, tau0):
        ans = 0
        for k in range(9):
            ans += self.n[k]*self.capj[k]*(self.capj[k]-1)*(tau0**(self.capj[k]-2))
        return ans

    def parGammaPiTau(self):
        return 0.


class __ResiduPart__:

    def __init__(self):
        self.capi = koefReg2["capi"].copy()
        self.capj = koefReg2["capj"].copy()
        self.n = koefReg2["n"].copy()

    def gamma(self, pi0, tau0):
        ans = 0.
        for k in range(43):
            ans += self.n[k]*(pi0**self.capi[k])*((tau0-0.5)**self.capj[k])
        return ans

    def parGammaPi(self, pi0, tau0):
        ans = 0.
        for k in range(43):
            ans += self.n[k]*self.capi[k]*(pi0**(self.capi[k]-1))*((tau0-0.5)**self.capj[k])
        return ans

    def parGammaPi2(self, pi0, tau0):
        ans = 0.
        for k in range(43):
            ans += self.n[k]*self.capi[k]*(self.capi[k]-1)*(pi0**(self.capi[k]-2))*((tau0-0.5)**self.capj[k])
        return ans

    def parGammaTau(self, pi0, tau0):
        ans = 0.
        for k in range(43):
            ans += self.n[k]*self.capj[k]*(pi0**self.capi[k])*((tau0-0.5)**(self.capj[k]-1))
        return ans

    def parGammaTau2(self, pi0, tau0):
        ans = 0.
        for k in range(43):
            ans += self.n[k]*self.capj[k]*(self.capj[k]-1)*(pi0**self.capi[k])*((tau0-0.5)**(self.capj[k]-2))
        return ans

    def parGammaPiTau(self, pi0, tau0):
        ans = 0.
        for k in range(43):
            ans += self.n[k]*self.capi[k]*self.capj[k]*(pi0**(self.capi[k]-1))*((tau0-0.5)**(self.capj[k]-1))
        return ans


class PropReg2a:

    def __init__(self):
        self.ideal = __IdealPart__()
        self.residu = __ResiduPart__()
        self.p0 = 1e3
        self.t0 = 540

    def getSpecVol(self, p, t):
        pi = p/self.p0
        tau = self.t0/t
        gamma1 = self.ideal.parGammaPi(pi0=pi)
        gamma2 = self.residu.parGammaPi(pi0=pi, tau0=tau)
        ans = ((bigr*t)/p)*pi*(gamma1+gamma2)
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
        ans = bigr*tau*(gamma2+gamma1)-bigr*(gamma3+gamma4)
        return ans

    def getSpecEnthalpy(self, p, t):
        pi = p/self.p0
        tau = self.t0/t
        gamma1 = self.ideal.parGammaTau(tau0=tau)
        gamma2 = self.residu.parGammaTau(pi0=pi, tau0=tau)
        ans = bigr*t*tau*(gamma1 + gamma2)
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
        gamma2 = self.residu.parGammaPi2(pi0=pi, tau0=tau)
        gamma3 = self.residu.parGammaPiTau(pi0=pi, tau0=tau)
        gamma4 = self.ideal.parGammaTau2(tau0=tau)
        gamma5 = self.residu.parGammaTau2(pi0=pi, tau0=tau)
        ans1 = ((1+pi*gamma1-tau*pi*gamma3)**2)/(1-(pi**2)*gamma2)
        ans = -bigr*(tau**2)*(gamma4+gamma5)-bigr*ans1
        return ans


#Persamaan2 pelengkap untuk p <= 10 MPa
class __IdealPart2__(__IdealPart__):

    def __init__(self):
        super().__init__()
        self.n[0] = -0.96937268393049e1
        self.n[1] = 0.10087275970006e2


class __ResiduPart2__:

    def __init__(self):
        self.capi = koefReg2["capi2"].copy()
        self.capj = koefReg2["capj2"].copy()
        self.n = koefReg2["n2"].copy()

    def gamma(self, pi0, tau0):
        ans = 0.
        for k in range(13):
            ans += self.n[k]*(pi0**self.capi[k])*((tau0-0.5)**self.capj[k])
        return ans

    def parGammaPi(self, pi0, tau0):
        ans = 0.
        for k in range(13):
            ans += self.n[k]*self.capi[k]*(pi0**(self.capi[k]-1))*((tau0-0.5)**self.capj[k])
        return ans

    def parGammaPi2(self, pi0, tau0):
        ans = 0.
        for k in range(13):
            ans += self.n[k]*self.capi[k]*(self.capi[k]-1)*(pi0**(self.capi[k]-2))*((tau0-0.5)**self.capj[k])
        return ans

    def parGammaTau(self, pi0, tau0):
        ans = 0.
        for k in range(13):
            ans += self.n[k]*self.capj[k]*(pi0**self.capi[k])*((tau0-0.5)**(self.capj[k]-1))
        return ans

    def parGammaTau2(self, pi0, tau0):
        ans = 0.
        for k in range(13):
            ans += self.n[k]*self.capj[k]*(self.capj[k]-1)*(pi0**self.capi[k])*((tau0-0.5)**(self.capj[k]-2))
        return ans

    def parGammaPiTau(self, pi0, tau0):
        ans = 0.
        for k in range(13):
            ans += self.n[k]*self.capi[k]*self.capj[k]*(pi0**(self.capi[k]-1))*((tau0-0.5)**(self.capj[k]-1))
        return ans


class PropReg2b(PropReg2a):

    def __init__(self):
        super().__init__()
        self.ideal = __IdealPart2__()
        self.residu = __ResiduPart2__()