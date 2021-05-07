import numpy as np


#Fungsi untuk menghitung invers matriks dengan metode
#eliminasi gauss-jordan
def gaussjor(B):
    A = np.copy(B)
    n = len(A)
    sol = np.identity(n)

#Eliminasi maju
    for k in range((n-1)):
        for i in range((k+1), n):
            kons = A[i, k]/A[k, k]
            sol[i,:n] = sol[i,:n] - kons*sol[k,:n]
            A[i,:n] = A[i,:n] - kons*A[k,:n]

#Membuat elemen diagonal matriks menjadi nilai 1
    for i in range(n):
        if A[i, i] != 1:
            sol[i, :n] = sol[i, :n]/A[i, i]
            A[i, :n] = A[i, :n]/A[i, i]

#Eliminasi mundur
    for j in range((n-1), 0, -1):
        for i in range((j-1), -1, -1):
            kons = A[i, j]
            sol[i, :n] = sol[i, :n] - kons*sol[j, :n]
            A[i, :n] = A[i, :n] - kons*A[j, :n]

    return A,sol


class invMatrix(object):

    def submat(A, row, col):
        b = np.copy(A)
        n = len(b)
        blist = np.zeros((n - 1, n - 1))

        k = 0
        for i in range(n):
            m = 0
            for j in range(n):
                if (i != row) and (j != col):
                    blist[ k, m ] = np.copy(b[i,j])
                    m = m + 1
                    if m >= (n - 1):
                        k = k + 1

        return blist

    def determinan(self, A):
        b = np.copy(A)
        n = len(b)
        det = 0

        flag = True
        while flag:
            if n == 2:
                det = b[ 0, 0 ] * b[ 1, 1 ] - b[ 0, 1 ] * b[ 1, 0 ]

                flag = False
            else:
                for j in range(n):
                    sub = invMatrix.submat(b, 0, j)
                    det += b[ 0, j ] * ((-1) ** (0 + j)) * self.determinan(sub)

                flag = False

        return det

    def adjoin(self, A):
        b = np.copy(A)
        n = len(b)
        cof = np.zeros((n, n))
        # min = invMatrix()

        for i in range(n):
            for j in range(n):
                sub = invMatrix.submat(b, i, j)
                minor = self.determinan(sub)
                cof[ i, j ] = ((-1) ** (i + j)) * minor

        return cof

    def inverse(self, A):
        a = np.copy(A)
        n = len(a)
        (row, col) = a.shape
        det = self.determinan(a)
        adj = np.copy(self.adjoin(a))
        b = 0

        flag = True
        while flag == True:
            if row != col:
                print("\nBukan matriks persegi!!!!!!")
                b = None
                break
            elif n < 2:
                print("\nMatriks minimal berdimensi 2x2")
                b = None
                break
            elif det == 0:
                print("\nMatriks tidak mempunyai invers!!!!!")
                b = None
                break

            b = (1. / det) * np.transpose(adj)

            flag = False

        return b