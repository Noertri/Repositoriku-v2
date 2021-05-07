from math import sqrt
from .koefisien import koefReg4

_n = koefReg4["n"]


def getSaturPress(tsat0):
    nu = (tsat0/1)+(_n[8]/((tsat0/1) - _n[9]))
    cap_a = (nu**2) + _n[0]*nu + _n[1]
    cap_b = _n[2]*(nu**2) + _n[3]*nu + _n[4]
    cap_c = _n[5]*(nu**2) + _n[6]*nu + _n[7]
    ans = 1e3*((2*cap_c/(-cap_b + sqrt(cap_b**2 - 4*cap_a*cap_c)))**4)
    return ans


def getSaturTemp(psat0):
    beta = (psat0/1000)**(1/4)
    cap_e = (beta**2) + _n[2]*beta + _n[5]
    cap_f = _n[0]*(beta**2) + _n[3]*beta + _n[6]
    cap_g = _n[1]*(beta**2) + _n[4]*beta + _n[7]
    cap_d = 2*cap_g/(-cap_f - sqrt((cap_f**2) - 4*cap_e*cap_g))
    ans = 1*((_n[9] + cap_d - sqrt((_n[9] + cap_d)**2 - 4*(_n[8] + _n[9]*cap_d)))/2)
    return ans