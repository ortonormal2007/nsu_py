from random import random as rd
from math import sqrt as sq
from time import perf_counter as pc
from numpy import linspace, sum
from numpy import sqrt as sq_num
from numpy.random import random as rd_num
from numba import njit
from matplotlib.pyplot import (plot, legend, show, xscale,
                               yscale, xlabel, ylabel, title)

def my_time(func, *args):
    t = []
    for i in range(3):
        t1 = pc()
        res = func(*args)
        t2 = pc()
        t.append(t2 - t1)
    return min(t)


def plt(func):
    n = 0
    t = my_time(func, 0)
    print(t)
    x = []
    y = []
    while t < 0.1:
        x.append(n)
        y.append(t)
        t = my_time(func, n)
        print(t)
        n += 1
    return(x, y)


def pi_mk(n):
    N_in = 0
    N = 2 ** n
    for i in range(N):
        if rd() ** 2 + rd() ** 2 <= 1:
            N_in += 1
    pi = 4 * N_in/N
    return pi


def pi_numpy(n):
    N = 2 ** n
    point_x = rd_num(2 ** n)
    point_y = rd_num(2 ** n)
    N_in = (point_x ** 2 + point_y ** 2 < 1).sum()
    pi = 4 * N_in/N
    return pi 


@njit
def pi_jit(n):
    N_in = 0
    N = 2 ** n
    for i in range(N):
        if rd() ** 2 + rd() ** 2 <= 1:
            N_in += 1
    pi = 4 * N_in/N
    return pi


@njit
def pi_numpy_jit(n):
    N = 2 ** n
    point_x = rd_num(2 ** n)
    point_y = rd_num(2 ** n)
    N_in = (point_x ** 2 + point_y ** 2 < 1).sum()
    pi = 4 * N_in/N
    return pi


def main():
    title('Pi Monte Carlo')
    xlabel('n')
    ylabel('time')
    yscale('log')


    plt_data = (
        (plt(pi_mk), 'python'),
        (plt(pi_numpy), 'numpy'),
        (plt(pi_jit), 'jit'),
        (plt(pi_numpy_jit), 'numpy jit')
    )


    for coords, lab in plt_data:
        n, _time = coords
        print(coords)
        plot(n, _time, label=lab)
    # plt(pi_numpy)
    # coords, lab = (plt(pi_numpy_jit), 'numpy jit')
    # n, _time = coords
    # plot(n, _time, label=lab)
    legend()
    show()



if __name__ == '__main__':
    main()
    pi_numpy_jit.revise_types()
