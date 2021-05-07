from math import exp, log, expm1, log1p, sqrt
from ._koefisien_ import koef, abc, pressc, tempc, rhoc, bigr


class ResiduPart:
    """Kumpulan rumus energi bebas spesifik Helmhotz bagian residu dan turunannya"""

    def __init__(self):
        self.a = koef["ai"]
        self.b = koef["bi"]
        self.c = koef["ci"]
        self.d = koef["di"]
        self.big_a = koef["big_ai"]
        self.big_b = koef["big_bi"]
        self.big_c = koef["big_ci"]
        self.big_d = koef["big_di"]
        self.t = koef["ti"]
        self.n = koef["ni"]
        self.alpha = koef["alphai"]
        self.beta = koef["betai"]
        self.gamma = koef["gammai"]
        self.eps = koef["epsi"]

    #theta, big delta, psi
    def theta(self, i=0, delta1=1., tau1=1.):
        ans = (1 - tau1) + self.big_a[i]*((delta1 - 1)**2)**(1/(2*self.beta[i]))
        return ans

    def psi(self, i=0, delta2=1., tau2=1.):
        pw = (self.big_c[i]*(delta2 - 1)**2) + (self.big_d[i]*(tau2 - 1)**2)
        ans = exp(-pw)
        return ans

    def bigDelta(self, i=0, delta3=1., tau3=1.):
        theta = self.theta(i=i, delta1=delta3, tau1=tau3)
        ans = (theta**2)+self.big_b[i]*((delta3 - 1)**2)**self.a[i]
        return ans

    #turunan parsial big delta0 terhadap delta
    def parBigDeltaDelta(self, i=0, delta4=1., tau4=1.):
        """Turunan parsial pertama big delta terhadap delta"""

        theta = self.theta(i=i, delta1=delta4, tau1=tau4)
        pw = (1/(2*self.beta[i])) - 1
        ans1 = (delta4 - 1)**2
        ans = (delta4 - 1)*(self.big_a[i]*theta*(2/self.beta[i])*(ans1**pw) + 2*self.big_b[i]*self.a[i]*(ans1**(
                self.a[i] - 1)))
        return ans

    def parBigDeltaDelta2(self, i=0, delta5=1., tau5=1.):
        """Turunan parsial kedua big delta terhadap delta"""

        theta = self.theta(i=i, delta1=delta5, tau1=tau5)
        bigDelta = self.parBigDeltaDelta(i=i, delta4=delta5, tau4=tau5)
        pw = self.a[i]-2
        pw1 = (1/(2*self.beta[i]))-1
        pw2 = (1/(2*self.beta[i]))-2
        ans4 = (delta5-1)**2
        ans1 = 4*self.big_b[i]*self.a[i]*(self.a[i]-1)*(ans4**pw)
        ans2 = 2*(self.big_a[i]**2)*((1/self.beta[i])**2)*((ans4**pw1)**2)
        ans3 = self.big_a[i]*theta*pw1*(ans4**pw2)
        ans = (1/(delta5-1))*bigDelta+((delta5-1)**2)*(ans1+ans2+ans3)
        return ans

    #turunan parsial psi terhadap delta
    def parPsiDelta(self, i=0, delta6=1., tau6=1.):
        """Turunan parsial pertama psi terhadap delta"""

        psi = self.psi(i=i, delta2=delta6, tau2=tau6)
        ans = -2*self.big_c[i]*(delta6-1)*psi
        return ans

    def parPsiDelta2(self, i=0, delta7=1., tau7=1.):
        """Turunan parsial kedua psi terhadap delta"""

        psi = self.psi(i=i, delta2=delta7, tau2=tau7)
        ans = 2*self.big_c[i]*psi*(2*self.big_c[i]*((delta7-1)**2)-1)
        return ans

    #turunan parsial psi terhadap tau
    def parPsiTau(self, i=0, delta8=1., tau8=1.):
        """Turunan parsial pertama psi terhadap tau0"""

        psi = self.psi(i=i, delta2=delta8, tau2=tau8)
        ans = -2*self.big_d[i]*(tau8-1)*psi
        return ans

    def parPsiTau2(self, i=0, delta9=1., tau9=1.):
        """Turunan parsial kedua psi terhadap tau0"""

        psi = self.psi(i=i, delta2=delta9, tau2=tau9)
        ans = 2*self.big_d[i]*psi*(2*self.big_d[i]*((tau9-1)**2)-1)
        return ans

    #turunan parsial psi terhadap delta dan tau0
    def parPsiDeltaTau(self, i=0, delta10=1., tau10=1.):
        """Turunan parsial psi terhadap tau0 dan delta"""

        psi = self.psi(i=i, delta2=delta10, tau2=tau10)
        ans = 4*self.big_c[i]*self.big_d[i]*(delta10-1)*(tau10-1)*psi
        return ans

    #turunan parsial big delta pangkat b terhadap delta
    def parBigDeltaBDelta(self, i=0, delta11=1., tau11=1.):
        """Turunan parsial pertama big delta0 pangkat b terhadap delta"""

        bigDelta = self.bigDelta(i=i, delta3=delta11, tau3=tau11)
        bigDelta2 = self.parBigDeltaDelta(i=i, delta4=delta11, tau4=tau11)
        ans = self.b[i]*(bigDelta**(self.b[i]-1))*bigDelta2
        return ans

    def parBigDeltaBDelta2(self, i=0, delta12=1., tau12=1.):
        """Turunan parsial kedua big delta pangkat b terhadap delta"""

        ans1 = self.bigDelta(i=i, delta3=delta12, tau3=tau12)
        ans2 = self.parBigDeltaDelta(i=i, delta4=delta12, tau4=tau12)
        ans3 = self.parBigDeltaDelta2(i=i, delta5=delta12, tau5=tau12)
        pw = self.b[i]-1
        pw2 = self.b[i]-2
        ans = self.b[i]*((ans1**pw)*ans3+pw*(ans1**pw2)*(ans2**2))
        return ans

    #turunan parsial big delta pangkat b terhadap tau0
    def parBigDeltaBTau(self, i=0, delta13=1., tau13=1.):
        """Turunan parsial big delta pangkat b terhadap tau"""

        theta = self.theta(i=i, delta1=delta13, tau1=tau13)
        bigDelta = self.bigDelta(i=i, delta3=delta13, tau3=tau13)
        ans = -2*theta*self.b[i]*(bigDelta**(self.b[i]-1))
        return ans

    def parBigDeltaBTau2(self, i=0, delta14=1., tau14=1.):
        """Turunan parsial kedua big delta pangkat b terhadap tau"""

        theta = self.theta(i=i, delta1=delta14, tau1=tau14)
        bigDelta = self.bigDelta(i=i, delta3=delta14, tau3=tau14)
        ans = 2*self.b[i]*(bigDelta**(self.b[i]-1))+4*(theta**2)*self.b[i]*(self.b[i]-1)*(bigDelta**(self.b[i]-2))
        return ans

    #turunan parsial big delta pangkat b terhadap delta dan tau0
    def parBigDeltaBDeltaTau(self, i=0, delta15=1., tau15=1.):
        """Turunan parsial big delta0 pangkat b terhadap delta dan tau0"""

        bigDelta = self.bigDelta(i=i, delta3=15, tau3=tau15)
        theta = self.theta(i=i, delta1=delta15, tau1=tau15)
        bigDelta2 = self.parBigDeltaDelta(i=i, delta4=delta15, tau4=tau15)
        pw = (1/(2*self.beta[i]))-1
        pw1 = self.b[i]-1
        ans3 = (delta15-1)**2
        ans1 = -self.big_a[i]*self.b[i]*(2/self.beta[i])*(bigDelta**pw1)*(delta15-1)*(ans3**pw)
        ans2 = 2*theta*self.b[i]*(self.b[i]-1)*(bigDelta**(self.b[i]-2))*bigDelta2
        ans = ans1-ans2
        return ans

    #phi
    def phi(self, delta0, tau0):
        """Bagian residu dari rumus energi bebas spesifik Helmhotz"""

        ans = 0.
        for i in range(56):
            if (i >= 0) and (i < 7):
                ans += self.n[i]*(delta0**self.d[i])*(tau0**self.t[i])
            elif (i >= 7) and (i < 51):
                pw = delta0**self.c[i]
                ans += self.n[i]*(delta0**self.d[i])*(tau0**self.t[i])*exp(-pw)
            elif (i >= 51) and (i < 54):
                pw1 = (self.alpha[i]*(delta0 - self.eps[i])**2) + (self.beta[i]*(tau0 - self.gamma[i])**2)
                ans += self.n[i]*(delta0**self.d[i])*(tau0**self.t[i])*exp(-pw1)
            elif (i >= 54) and (i < 56):
                bigDelta = self.bigDelta(i=i, delta3=delta0, tau3=tau0)
                psi = self.psi(i=i, delta2=delta0, tau2=tau0)
                ans += self.n[i]*(bigDelta**self.b[i])*delta0*psi

        return ans

    #turunan parsial phi terhadap delta
    def parPhiDelta(self, delta0=1., tau0=1.):
        """Turunan parsial phi tehadap delta"""

        ans = 0.
        for i in range(56):
            if (i >= 0) and (i < 7):
                pw = self.d[i]-1
                ans += self.n[i]*self.d[i]*(delta0**pw)*(tau0**self.t[i])
            elif (i >= 7) and (i < 51):
                pw = delta0**self.c[i]
                pw1 = self.d[i]-1
                phi1 = self.n[i]*(expm1(-pw) + 1)
                phi2 = (delta0**pw1)*(tau0**self.t[i])
                phi3 = self.d[i]-self.c[i]*pw
                ans += phi1*phi2*phi3
            elif (i >= 51) and (i < 54):
                pw1 = delta0-self.eps[i]
                pw2 = tau0-self.gamma[i]
                pw3 = self.alpha[i]*(pw1**2)+self.beta[i]*(pw2**2)
                phi1 = self.n[i]*(delta0**self.d[i])*(tau0**self.t[i])*(expm1(-pw3)+1)
                phi2 = (self.d[i]/delta0)-2*self.alpha[i]*pw1
                ans += phi1*phi2
            elif (i >= 54) and (i < 56):
                psi = self.psi(i=i, delta2=delta0, tau2=tau0)
                bigDelta2 = self.parBigDeltaBDelta(i=i, delta11=delta0, tau11=tau0)
                psi2 = self.parPsiDelta(i=i, delta6=delta0, tau6=tau0)
                bigDelta = self.bigDelta(i=i, delta3=delta0, tau3=tau0)
                phi1 = (bigDelta**self.b[i])*(psi+delta0*psi2)
                phi2 = bigDelta2*delta0*psi
                ans += self.n[i]*(phi1+phi2)

        return ans

    def parPhiDelta2(self, delta0=1., tau0=1.):
        """Turunan parsial kedua phi tehadap delta"""

        ans = 0.
        for i in range(56):
            if (i >= 0) and (i < 7):
                pw = self.d[i]-2
                ans += self.n[i]*self.d[i]*(self.d[i]-1)*(delta0**pw)*(tau0**self.t[i])
            elif (i >= 7) and (i < 51):
                pw = delta0**self.c[i]
                pw1 = self.d[i]-2
                phi1 = self.n[i]*(expm1(-pw) + 1)
                phi2 = (delta0**pw1)*(tau0**self.t[i])
                phi3 = self.d[i]-self.c[i]*pw
                phi4 = self.d[i]-1-self.c[i]*pw
                phi5 = (self.c[i]**2)*pw
                ans += phi1*(phi2*(phi3*phi4-phi5))
            elif (i >= 51) and (i < 54):
                pw = delta0-self.eps[i]
                pw1 = tau0-self.gamma[i]
                pw2 = self.alpha[i]*(pw**2)+self.beta[i]*(pw1**2)
                pw3 = self.d[i]-1
                pw4 = self.d[i]-2
                phi1 = self.n[i]*(tau0**self.t[i])*(expm1(-pw2) + 1)
                phi2 = -2*self.alpha[i]*(delta0**self.d[i])
                phi3 = 4*(self.alpha[i]**2)*(delta0**self.d[i])*((delta0-self.eps[i])**2)
                phi4 = 4*self.d[i]*self.alpha[i]*(delta0**pw3)*(delta0-self.eps[i])
                phi5 = self.d[i]*(self.d[i]-1)*(delta0**pw4)
                ans += phi1*(phi2+phi3-phi4+phi5)
            elif (i >= 54) and (i < 56):
                psi = self.psi(i=i, delta2=delta0, tau2=tau0)
                bigDelta2 = self.parBigDeltaBDelta(i=i, delta11=delta0, tau11=tau0)
                psi2 = self.parPsiDelta(i=i, delta6=delta0, tau6=tau0)
                bigDelta = self.bigDelta(i=i, delta3=delta0, tau3=tau0)
                psi3 = self.parPsiDelta2(i=i, delta7=delta0, tau7=tau0)
                bigDelta3 = self.parBigDeltaBDelta2(i=i, delta12=delta0, tau12=tau0)
                phi1 = (bigDelta**self.b[i])*(2*psi2+delta0*psi3)
                phi2 = 2*bigDelta2*(psi+delta0*psi2)
                phi3 = bigDelta3*psi2
                ans += self.n[i]*(phi1+phi2+phi3)

        return ans

    #turunan parsial phi terhadap delta dan tau0
    def parPhiTau(self, delta0=1., tau0=1.):
        """Turunan parsial phi tehadap tau0"""

        ans = 0.
        for i in range(56):
            if (i >= 0) and (i < 7):
                ans += self.n[i]*self.t[i]*(delta0**self.d[i])*(tau0**(self.t[i]-1))
            elif (i >= 7) and (i < 51):
                pw = delta0**self.c[i]
                ans += self.n[i]*self.t[i]*(delta0**self.d[i])*(tau0**(self.t[i]-1))*(expm1(-pw) + 1)
            elif (i >= 51) and (i < 54):
                pw = (self.alpha[i]*(delta0-self.eps[i])**2) + (self.beta[i]*(tau0-self.gamma[i])**2)
                phi1 = (self.t[i]/tau0)-2*self.beta[i]*(tau0-self.gamma[i])
                ans += self.n[i]*(delta0**self.d[i])*(tau0**self.t[i])*(expm1(-pw) + 1)*phi1
            elif (i >= 54) and (i < 56):
                psi = self.psi(i=i, delta2=delta0, tau2=tau0)
                bigDelta2 = self.parBigDeltaBTau(i=i, delta13=delta0, tau13=tau0)
                psi2 = self.parPsiTau(i=i, delta8=delta0, tau8=tau0)
                bigDelta = self.bigDelta(i=i, delta3=delta0, tau3=tau0)
                ans += self.n[i]*delta0*(bigDelta2*psi+(bigDelta**self.b[i])*psi2)

        return ans

    def parPhiTau2(self, delta0=1., tau0=1.):
        """Turunan parsial kedua phi tehadap tau0"""

        ans = 0.
        for i in range(56):
            if (i >= 0) and (i < 7):
                ans += self.n[i] * self.t[i] * (self.t[i] - 1) * (delta0**self.d[i]) * (tau0**(self.t[i]-2))
            elif (i >= 7) and (i < 51):
                pw = delta0**self.c[i]
                ans += self.n[i]*self.t[i]*(self.t[i]-1)*(delta0**self.d[i])*(tau0**(self.t[i]-2))*(expm1(-pw) + 1)
            elif (i >= 51) and (i < 54):
                pw = (self.alpha[i] * (delta0 - self.eps[i])**2) + (self.beta[i] * (tau0 - self.gamma[i])**2)
                phi1 = self.n[i]*(delta0**self.d[i])*(tau0**self.t[i])*(expm1(-pw) + 1)
                phi2 = ((self.t[i]/tau0)-2*self.beta[i]*(tau0-self.gamma[i]))**2
                phi3 = (self.t[i]/(tau0**2))+2*self.beta[i]
                ans += phi1*(phi2-phi3)
            elif (i >= 54) and (i < 56):
                psi = self.psi(i=i, delta2=delta0, tau2=tau0)
                bigDelta2 = self.parBigDeltaBTau(i=i, delta13=delta0, tau13=tau0)
                psi2 = self.parPsiTau(i=i, delta8=delta0, tau8=tau0)
                bigDelta = self.bigDelta(i=i, delta3=delta0, tau3=tau0)
                psi3 = self.parPsiTau2(i=i, delta9=delta0, tau9=tau0)
                bigDelta3 = self.parBigDeltaBTau2(i=i, delta14=delta0, tau14=tau0)
                phi1 = bigDelta3*psi
                phi2 = 2*bigDelta2*psi2
                phi3 = (bigDelta**self.b[i])*psi3
                ans += self.n[i]*delta0*(phi1 + phi2 + phi3)

        return ans

    #turunan parsial phi terhadap delta dan tau0
    def parPhiDeltaTau(self, delta0=1., tau0=1.):
        """Turunan parsial kedua phi tehadap delta0 dan tau0"""

        ans = 0.
        for i in range(56):
            if (i >= 0) and (i < 7):
                ans += self.n[i]*self.t[i]*self.d[i]*(delta0**(self.d[i]-1))*(tau0**(self.t[i]-1))
            elif (i >= 7) and (i < 51):
                pw = -delta0**self.c[i]
                ans += self.n[i]*self.t[i]*(delta0**(self.d[i]-1))*(tau0**(self.t[i]-1))*\
                       (self.d[i]+self.c[i]*pw)*(expm1(pw) + 1)
            elif (i >= 51) and (i < 54):
                pw = (self.alpha[i]*(delta0 - self.eps[i])**2)+(self.beta[i]*(tau0 - self.gamma[i])**2)
                phi1 = self.n[i]*(delta0**self.d[i])*(tau0**self.t[i])*(expm1(-pw) + 1)
                phi2 = (self.d[i]/delta0-2*self.alpha[i]*(delta0-self.eps[i]))
                phi3 = (self.t[i]/tau0)-2*self.beta[i]*(tau0-self.gamma[i])
                ans += phi1*phi2*phi3
            elif (i >= 54) and (i < 56):
                psi = self.psi(i=i, delta2=delta0, tau2=tau0)
                bigdelta = self.bigDelta(i=i, delta3=delta0, tau3=tau0)
                psi2 = self.parPsiTau(i=i, delta8=delta0, tau8=tau0)
                psi3 = self.parPsiDeltaTau(i=i, delta10=delta0, tau10=tau0)
                bigdelta2 = self.parBigDeltaBDelta(i=i, delta11=delta0, tau11=tau0)
                bigdelta3 = self.parBigDeltaBTau(i=i, delta13=delta0, tau13=tau0)
                psi4 = self.parPsiDelta(i=i, delta6=delta0, tau6=tau0)
                bigdelta4 = self.parBigDeltaBDeltaTau(i=i, delta15=delta0, tau15=tau0)
                phi1 = (bigdelta**self.b[i])*(psi2+delta0*psi3)
                phi2 = delta0*bigdelta2*psi2
                phi3 = bigdelta3*(psi+delta0*psi4)
                phi4 = bigdelta4*delta0*psi
                ans += self.n[i]*(phi1+phi2+phi3+phi4)

        return ans


class IdealPart:
    """Kumpulan rumus energi bebas spesifik Helmhotz bagian ideal dan turunannya"""

    def __init__(self):
        self.n0 = koef["no"].copy()
        self.gamma0 = koef["gammao"]

    def phi(self, delta0=1., tau0=1.):
        ans = log(delta0) + self.n0[0] + self.n0[1]*tau0 + self.n0[2]*log(tau0)
        for i in range(3, 8):
            pw = self.gamma0[i]*tau0
            phi1 = expm1(-pw)+1
            phi2 = 1 - phi1
            ans += self.n0[i]*log1p(phi2-1)
        return ans

    def parPhiDelta(self, delta0=1.):
        return 1/delta0

    def parPhiDelta2(self, delta0=1.):
        return -1/(delta0**2)

    def parPhiTau(self, tau0=1.):
        ans = self.n0[1] + (self.n0[2]/tau0)
        for i in range(3,8):
            pw = self.gamma0[i]*tau0
            phi1 = expm1(-pw) + 1
            phi2 = 1 - phi1
            ans += self.n0[i]*self.gamma0[i]*((1/phi2) - 1)
        return ans

    def parPhiTau2(self, tau0=1.):
        ans = -(self.n0[2]/(tau0**2))
        ans1 = 0.
        for i in range(3,8):
            pw = self.gamma0[i]*tau0
            phi1 = expm1(-pw)+1
            phi2 = 1 - phi1
            ans1 += self.n0[i]*(self.gamma0[i]**2)*phi1*(1/(phi2**2))
        return ans - ans1

    def parPhiDeltaTau(self, delta0=1., tau0=1.):
        return 0.


class IdealPart2(IdealPart):

    def __init__(self):
        super().__init__()
        self.n0[0] = -8.320446136002927
        self.n0[1] = 6.683210380797977


__a__ = abc["a"]
__b__ = abc["b"]
__c__ = abc["c"]


def initDeltas(t):
    """Fungsi bantuan untuk nilai awal delta pada titik saturasi"""

    nu = 1 - (t/tempc)
    pw = __c__[0]*nu**(2/6) + __c__[1]*nu**(4/6) + __c__[2]*nu**(8/6) + __c__[3]*nu**(18/6) + __c__[4]*nu**(37/6) \
         + __c__[5]*nu**(71/6)
    f1 = 1 + __b__[0]*nu**(1/3) + __b__[1]*nu**(2/3) + __b__[2]*nu**(5/3) + __b__[3]*nu**(16/3) + __b__[4]*nu**(43/3) \
         + __b__[5]*nu**(110/3)
    f2 = exp(pw)
    return [f1, f2]


def initTau(tau, p):
    """Fungsi bantuan untuk nilai awal tau pada titik saturasi"""

    nu = 1 - (1/tau)
    f1 = log(p/pressc) - tau*(__a__[0]*nu + __a__[1]*(nu**1.5) + __a__[2]*(nu**3) + __a__[3]*(nu**3.5) +
                              __a__[4]*(nu**4) + __a__[5]*(nu**7.5))
    return f1


__residu__ = ResiduPart()
__ideal__ = IdealPart()
__ideal2__ = IdealPart2()


def SaturDeltas(props, t):
    """Fungsi bantuan untuk mendapatkan delta pada titik saturasi dengan data suhu/temperatur"""

    tau1 = tempc/t
    phi1 = __residu__.phi(delta0=props[0], tau0=tau1)
    phi2 = __residu__.phi(delta0=props[1], tau0=tau1)
    phi3 = __residu__.parPhiDelta(delta0=props[0], tau0=tau1)
    phi4 = __residu__.parPhiDelta(delta0=props[1], tau0=tau1)

    f1 = ((props[1]**2)*phi4 + props[1]) - ((props[0]**2)*phi3 + props[0])
    f2 = (props[1]*phi4+phi2+log(props[1]))-(props[0]*phi3+phi1+log(props[0]))
    return [f1, f2]


def SaturTau(props, p):
    """Method bantuan untuk mendapatkan suhu/temperatur, massa jenis pada titik saturasi dengan data tekanan"""

    a1 = p/(rhoc*bigr*tempc)
    phi1 = __residu__.phi(delta0=props[1], tau0=props[0])
    phi2 = __residu__.phi(delta0=props[2], tau0=props[0])
    phi3 = __residu__.parPhiDelta(delta0=props[1], tau0=props[0])
    phi4 = __residu__.parPhiDelta(delta0=props[2], tau0=props[0])
    phi5 = sqrt(props[1]**2)/sqrt(props[2]**2)
    f1 = (a1*props[0])*((1/props[2]) - (1/props[1])) - log(phi5) - phi1 + phi2
    f2 = (a1*props[0]) - props[1] - (props[1]**2)*phi3
    f3 = (a1*props[0]) - props[2] - (props[2]**2)*phi4
    return [f1, f2, f3]


def SingleDelta(delta, p, t):
    tau = tempc/t
    k = p/(rhoc*bigr*t)
    phi1 = __residu__.parPhiDelta(delta0=delta, tau0=tau)
    ans = (delta**2)*phi1 + delta - k
    return ans