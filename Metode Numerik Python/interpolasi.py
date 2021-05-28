import numpy as np
from math import sqrt


def interpol(x=0, data1=(0,0), data2=(0,0)):
    y = data1[1] + ((data2[1]-data1[1])/(data2[0]-data1[0]))*(x-data1[0])
    return y


def delta(titik1=(0,0), titik2=(0,0)):
    ans = (titik2[1]-titik1[1])/(titik2[0]-titik1[0])
    return ans


def interpol2(x, titik1, titik2, titik3):
    b1 = titik1[1]
    b2 = delta(titik1, titik2)
    b3 = (delta(titik2, titik3)-delta(titik1, titik2))/(titik3[0]-titik1[0])

    y = b1 + b2*(x-titik1[0]) + b3*(x-titik1[0])*(x-titik2[0])
    return y


#Mencari nilai interpolasi dengan metode Newton
def newinter(x, titikx, titiky):
    n = len(titiky)

    b = np.zeros((n,n))

    b[:n, 0] = titiky.copy()

    for j in range(1, n):
        for i in range(0, (n-j)):
            b[i, j] = (b[i, (j-1)] - b[(i+1), (j-1)])/(titikx[i]-titikx[(i+j)])

    yint = b[0, 0]
    xx = 1.
    for i in range(1, n):
        xx = xx*(x - titikx[(i-1)])
        yint = yint + b[0, i]*xx

    return yint


#Mencari nilai interpolasi dengan metode Newton
#dengan cara recursive
class NewtInter2:

    def fbracket(self, titikx, titiky):
        n = len(titiky)

        if n == 2:
            hasil = (titiky[0] - titiky[1])/(titikx[0] - titikx[1])
        else:
            a = self.fbracket(titikx[0:(n-1)], titiky[0:(n-1)])
            b = self.fbracket(titikx[1:n], titiky[1:n])
            hasil = (a-b)/(titikx[0]-titikx[(n-1)])

        return hasil

    def ninter(self, xx, titikx, titiky):
        b = []
        ny = len(titiky)

        b.append(titiky[0])
        for i in range(2, (ny+1)):
            bi = self.fbracket(titikx[0:i], titiky[0:i])
            b.append(bi)

        yint = b[0]
        xt = 1.
        for j in range(1, ny):
            xt = xt*(xx - titikx[(j-1)])
            yint = yint + b[j]*xt

        return yint


x = [1., 3.61, 4.41, 9., 16.]
fx = [1., 1.9, 2.1, 3., 4.]

inter = NewtInter2()
ans = inter.ninter(4, x, fx)

er = abs(sqrt(4) - ans)/sqrt(4)
print(ans)
print(er)