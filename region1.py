from .koefisien import bigr, koefReg1


class __BasicReg1__:
    """Persamaan2 dasar untuk region 1"""

    def __init__(self):
        self.capi = koefReg1["capi"]
        self.capj = koefReg1["capj"]
        self.n = koefReg1["n"]

    def gamma(self, pi0, tau0):
        ans = 0.
        for k in range(34):
            ans += self.n[k]*((7.1-pi0)**self.capi[k])*((tau0-1.222)**self.capj[k])

        return ans

    def parGammaPi(self, pi0, tau0):
        ans = 0.
        for k in range(34):
            ans += -self.n[k]*self.capi[k]*((7.1-pi0)**(self.capi[k]-1))*((tau0-1.222)**self.capj[k])

        return ans

    def parGammaPi2(self, pi0, tau0):
        ans = 0.
        for k in range(34):
            ans += self.n[k]*self.capi[k]*(self.capi[k]-1)*((7.1-pi0)**(self.capi[k]-2))*((tau0-1.222)**self.capj[k])

        return ans

    def parGammaTau(self, pi0, tau0):
        ans = 0.
        for k in range(34):
            ans += self.n[k]*self.capj[k]*((7.1-pi0)**self.capi[k])*((tau0-1.222)**(self.capj[k]-1))

        return ans

    def parGammaTau2(self, pi0, tau0):
        ans = 0.
        for k in range(34):
            ans += self.n[k]*self.capj[k]*(self.capj[k]-1)*((7.1-pi0)**self.capi[k])*((tau0-1.222)**(self.capj[k]-2))

        return ans

    def parGammaPiTau(self, pi0, tau0):
        ans = 0.
        for k in range(34):
            ans += -self.n[k]*self.capi[k]*self.capj[k]*((7.1-pi0)**(self.capi[k]-1))*((tau0-1.222)**(self.capj[k]-1))

        return ans


class PropReg1:
    """Properties2 pada region 1"""

    def __init__(self):
        self.p0 = 16.53e3
        self.t0 = 1386
        self.basic = __BasicReg1__()

    def getSpecVol(self, p, t):
        pi = p/self.p0
        tau = self.t0/t
        gamma1 = self.basic.parGammaPi(pi0=pi, tau0=tau)
        ans = ((bigr*t)/p)*pi*gamma1
        return ans

    def getSpecInternal(self, p, t):
        pi = p/self.p0
        tau = self.t0/t
        gamma1 = self.basic.parGammaTau(pi0=pi, tau0=tau)
        gamma2 = self.basic.parGammaPi(pi0=pi, tau0=tau)
        ans = (bigr*t)*(tau*gamma1-pi*gamma2)
        return ans

    def getSpecEntropy(self, p, t):
        pi = p/self.p0
        tau = self.t0/t
        gamma1 = self.basic.gamma(pi0=pi, tau0=tau)
        gamma2 = self.basic.parGammaTau(pi0=pi, tau0=tau)
        ans = bigr*(tau*gamma2-gamma1)
        return ans

    def getSpecEnthalpy(self, p, t):
        pi = p/self.p0
        tau = self.t0/t
        gamma1 = self.basic.parGammaTau(pi0=pi, tau0=tau)
        ans = bigr*t*tau*gamma1
        return ans

    def getCp(self, p, t):
        pi = p/self.p0
        tau = self.t0/t
        gamma1 = self.basic.parGammaTau2(pi0=pi, tau0=tau)
        ans = -bigr*(tau**2)*gamma1
        return ans

    def getCv(self, p, t):
        pi = p/self.p0
        tau = self.t0/t
        gamma1 = self.basic.parGammaPi(pi0=pi, tau0=tau)
        gamma2 = self.basic.parGammaPi2(pi0=pi, tau0=tau)
        gamma3 = self.basic.parGammaTau2(pi0=pi, tau0=tau)
        gamma4 = self.basic.parGammaPiTau(pi0=pi, tau0=tau)
        ans = -bigr*(tau**2)*gamma3 + bigr*(((gamma1-tau*gamma4)**2)/gamma2)
        return ans