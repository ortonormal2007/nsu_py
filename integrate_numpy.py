from numpy import linspace, exp, sin, arange
import timeit
from matplotlib.pyplot import (plot, legend, show, xscale,
                               yscale, xlabel, ylabel, title)


def f(x):
    return exp(x)
    # return exp(-x) * sin(x)


def num_rect(a, b, n):
    h = (b - a) / n
    # x = linspace(a + h / 2, a + h / 2 + h * (n - 1), n)
    x = linspace(a + h * 0.5, a + h * (n - 0.5), n)
    fun = f(x) * h
    res = fun.sum()
    return res


def num_trap(a, b, n):
    h = (b - a) / n
    # x = linspace(a + h, a + h + h * (n - 2), n - 1)
    x = linspace(a + h, a + h * (n - 1), n - 1)
    res = (f(a) + f(b)) * 0.5 + f(x).sum()
    return h * res


def num_simp(a, b, n):
    h = (b - a) / n
    # x1 = linspace(a + h / 2, a + h / 2 + h * (n - 1), n)
    # x2 = linspace(a + h, a + h + h * (n - 2), n - 1)
    x1 = linspace(a + h * 0.5, a + h * (n - 0.5), n)
    x2 = linspace(a + h, a + h * (n - 1), n - 1)
    res = f(a) + f(b) + 4 * f(x1).sum() + 2 * f(x2).sum()
    return h * res / 6


if __name__ == '__main__':
    true_res = exp(1) - 1

    time_r = []
    err_r = []
    for n in range(11):
        time_r.append(timeit.timeit("intf_rect(0, 1, 2 ** n) - true_res",
                      number=5, globals=globals()))
        err_r.append(abs(intf_rect(0, 1, 2 ** n) - true_res))

    time_t = []
    err_t = []
    for n in range(11):
        time_t.append(timeit.timeit("intf_trap(0, 1, 2 ** n) - true_res",
                                    number=5, globals=globals()))
        err_t.append(abs(intf_trap(0, 1, 2 ** n) - true_res))

    time_s = []
    err_s = []
    for n in range(11):
        time_s.append(timeit.timeit("intf_simp(0, 1, 2 ** n) - true_res",
                                    number=5, globals=globals()))
        err_s.append(abs(intf_simp(0, 1, 2 ** n) - true_res))

    title('Numpy integr')
    xlabel('time')
    ylabel('error')
    xscale('log')
    yscale('log')
    plot(time_r, err_r, label='time_r')
    plot(time_t, err_t, label='time_t')
    plot(time_s, err_s, label='time_s')
    legend()
    show()
