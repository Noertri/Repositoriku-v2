#Program untuk mencari akar fungsi dengan menggunakan metode bisection

def bisect(fun, a, b, es):
    """
    :param fun: fungsi yg akan dicari akarnya
    :param a: interval bawah
    :param b: interval atas
    :param es: error yg diinginkan
    """

    ea = 100
    iter = 0
    sol = []
    err = []
    xr = a

    while ea > es:
        xrold  = xr
        xr = (a + b)/2

        if xr != 0:
            ea = abs((xr-xrold)/xr)*100
        else:
            ea = 100
            sol.append(xr)
            err.append(ea)
            break

        tes = fun(a)*fun(xr)

        if tes < 0:
            b = xr
        elif tes > 0:
            a = xr
        else:
            sol.append(xr)
            err.append(ea)
            break

        sol.append(xr)
        err.append(ea)
        iter = iter + 1

    return iter, sol, err


#Program untuk mencari akar fungsi dengan menggunakan metode false position
def falsi(fun, a, b, es):
    """
    :param fun: fungsi yg akan dicari akarnya
    :param a: interval bawah
    :param b: interval atas
    :param es: error yg diinginkan
    """

    ea = 100
    iter = 0
    sol = []
    err = []
    xr = a

    while ea > es:
        xrold  = xr
        xr = b - (fun(b)*((a-b)/(fun(a)-fun(b))))

        if xr != 0:
            ea = abs((xr-xrold)/xr)*100
        else:
            ea = 100
            sol.append(xr)
            err.append(ea)
            break

        tes = fun(a)*fun(xr)

        if tes < 0:
            b = xr
        elif tes > 0:
            a = xr
        else:
            sol.append(xr)
            err.append(ea)
            break

        sol.append(xr)
        err.append(ea)
        iter = iter + 1

    return iter, sol, err