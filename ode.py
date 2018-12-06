import math as mt
import numpy as np
from scipy.integrate import odeint
from matplotlib.pyplot import (plot, legend, show, xscale,
                               yscale, xlabel, ylabel, title)
from time import perf_counter as pc


def err(x, y, ref):
    a = zip(x, y)
    errors = []
    for t, u in a:
        errors.append(abs(ref(t) - u))
    # print(errors)
    return(max(errors))


def my_time(func, *args):
    t = []
    for i in range(3):
        t1 = pc()
        res = func(*args)
        t2 = pc()
        t.append((t2 - t1, res))
    return(sorted(t, key=lambda a: a[0])[0])
    

def ans(t):
    return 100 * mt.exp(0.1 * t)


def f(y, x):
    r = 0.1
    return r * y


def euler(xinit, tinit, tfinal, step, right):
    x = []
    y = []
    n = 1;
    x_next = 0;
    x_cur = xinit
    t_cur = tinit
    while t_cur <= tfinal:
        x_next = x_cur + step * right(x_cur, t_cur)
        x_cur = x_next
        x.append(t_cur)
        y.append(x_cur)
        t_cur = step * n
        n += 1
    return (x, y)


def ode_int(xinit, tinit, tfinal, sect, right):
    t = np.linspace(tinit, tfinal, sect)
    u = odeint(right, xinit, t)

    return(t, u)

eu_time, od_time = [], []
eu_err, od_err = [], []
for n in range(2, 17):
    eu = my_time(euler, 100, 0, 20, 20 / (2 ** n - 1), f)
    od = my_time(ode_int, 100, 0, 20, 2 ** n, f) 

    eu_time.append(eu[0])
    od_time.append(od[0])

    eu_err.append(err(*eu[1], ans))
    od_err.append(err(*od[1], ans))



xlabel('time')
ylabel('error')
yscale('log')
plot(eu_time, eu_err, label='eu')
plot(od_time, od_err, label='od')

# x, y = eu[1]
# t, u = od[1]
# plot(x, y, 'r-')
# plot(t, u)
# xscale('log')
# yscale('log')
# x = np.linspace(0, 20, 1024)
# plot(od[1][0], od[1][1])
# plot(eu[1][0], eu[1][1])
# plot(x, 100 * np.exp(0.1 * x))
legend()
show()
