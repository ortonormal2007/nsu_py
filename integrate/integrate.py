import integrate_numpy as ign
from math import exp, sin
from time import perf_counter as pc
from numpy import linspace, exp, sin, arange
from matplotlib.pyplot import (plot, legend, show, xscale,
                               yscale, xlabel, ylabel, title)


def my_time(func, a, b, n):
    t = []
    for i in range(3):
        t1 = pc()
        res = func(a, b, n)
        t2 = pc()
        t.append((t2 - t1, res))
    # print(sorted(t, key=lambda p: p[0]))
    return (sorted(t, key=lambda p: p[0])[0])


def plt(func, true_res, n_max=11, a=0, b=1):
    time_x = []
    err_y = []
    for n in range(n_max):
        t_r = my_time(func, a, b, 2 ** n)
        time_x.append(t_r[0])
        err_y.append(abs(t_r[1] - true_res))
    return (time_x, err_y)


def f(x):
    return exp(x)


def intf_rect(a, b, n):
    h = (b - a) / n
    x = a + h * 0.5
    res = 0
    for i in range(n):
        res += f(x) * h
        x += h
    return res


def intf_trap(a, b, n):
    h = (b - a) / n
    x = a + h
    res = (f(a) + f(b)) * 0.5
    for i in range(n - 1):
        res += f(x)
        x += h
    return h * res


def intf_simp(a, b, n):
    h = (b - a) / n
    x = a + h * 0.5
    res = f(a) + f(b)
    for i in range(n):
        res += 4 * f(x)
        x += h

    x = a + h
    for i in range(n - 1):
        res += 2 * f(x)
        x += h
    return h * res / 6


if __name__ == '__main__':
    true_res = exp(1) - 1

    title('Python integr')
    xlabel('time')
    ylabel('error')
    xscale('log')
    yscale('log')

    plt_data = (
        (plt(intf_rect, true_res), 'rect py'),
        (plt(intf_trap, true_res), 'trap py'),
        (plt(intf_simp, true_res), 'simp py'),
        (plt(ign.num_rect, true_res), 'rect numpy'),
        (plt(ign.num_trap, true_res), 'trap numpy'),
        (plt(ign.num_simp, true_res), 'simp numpy')
    )

    for coords, lab in plt_data:
        time_, err_ = coords
        plot(time_, err_, label=lab)

    legend()
    show()

    title('Python integr')
    xlabel('split')
    ylabel('time')
    splt = tuple(map(lambda x: 2 ** x, range(11)))
    for coords, lab in plt_data:
        time_, err_ = coords
        plot(splt, time_, label=lab)

    legend()
    show()
