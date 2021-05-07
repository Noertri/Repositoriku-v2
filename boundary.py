from math import sqrt, log
from .koefisien import b23


class Bound23:
    """Persamaan garis batas untuk region 2 dan 3"""

    def __init__(self):
        self._n = b23

    def getPress(self, t0):
        theta = t0/1
        ans = self._n[0] + self._n[1]*theta + self._n[2]*(theta**2)
        return ans*1000

    def getTemp(self, p0):
        pi = p0/1000
        ans = self._n[3] + sqrt((pi - self._n[4])/_n[2])
        return ans*1


class Bound3:
    """Persamaan2 garis batas untuk sub2 region 3"""

    def __init__(self):
        self._koef = None

    def setKoef(self, koef):
        self._koef = koef.copy()

    def getTemp(self, p0):
        """Persamaan garis batas untuk selain garis batas 3ab, 3op, dan 3ef"""

        pi = p0/1e3
        n = self._koef["n"]
        cap_i = self._koef["cap_i"]
        N = len(n)

        ans = 0.
        for k in range(N):
            ans += n[k]*(pi**cap_i[k])
        return round(ans*1, 7)

    def getTemp2(self, p0):
        """Persamaan batas untuk garis batas 3ab dan 3op"""

        pi = p0/1000
        n = self._koef["n"]
        cap_i = self._koef["cap_i"]
        N = len(n)

        ans = 0.
        for k in range(N):
            ans += n[k]*((log(pi))**cap_i[k])
        return round(ans*1, 7)

    def getTemp3(self, p0):
        """Persamaaan pembatas untuk garis batas 3ef"""

        pi = p0/1000
        ans = 3.727888004*(pi-22.064)+647.096
        return round(ans*1, 7)