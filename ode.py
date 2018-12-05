import numpy as np
from scipy.integrate import odeint
from matplotlib.pyplot import (plot, legend, show, xscale,
                               yscale, xlabel, ylabel, title)
from time import perf_counter as pc

def my_time(func, *args):
    t1 = pc()
    res = func(args)
    t2 = pc()
    

def ans(t):
    100 * exp(t)


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


for n in range(2, 17):
    x, y = euler(100, 0, 20, 20 / 2 ** n, f)
    t = np.linspace(0, 20, 2 ** n)
    u = odeint(f, 100, t)


t = np.linspace(0, 20)
x, y = euler(100, 0, 20, 1, f)
u = odeint(f, 100, t)
plot(x, y, 'r-')
plot(t, u)
show()