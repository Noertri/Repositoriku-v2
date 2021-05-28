#Program untuk menyelesaikan persamaan dengan metode eliminasi gauss
import numpy as np

def gausselim(A, B):
    N = A.shape
    n = N[0] - 1
    sol = B

    for k in range(0, (N[0]-1)):
        for i in range((k+1), N[0]):
            c = A[i, k]/A[k, k]
            for j in range(k, N[0]):
                A[i, j] = A[i, j] - c*A[k, j]

            B[i] = B[i] - c*B[k]

    sol[n] = B[n]/A[n, n]

    for i in range((n-1), -1, -1):
        sum = B[i]
        for j in range((i+1), N[0]):
            sum = sum - A[i, j]*sol[j]

        sol[i] = sum/A[i, i]

    return sol