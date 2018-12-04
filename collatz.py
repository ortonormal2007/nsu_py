from numba import njit
from time import perf_counter as pc
from matplotlib.pyplot import plot, legend, xlabel, ylabel, show





def my_time(func, *args):
    arr = []
    for i in range(3):
        t1 = pc()
        res = func(*args)
        t2 = pc()
        arr.append((t2 - t1, res))
    return(sorted(arr, key=lambda x: x[0])[0])


def collatz(n):
    lngt = 0
    while n != 1:
        if n % 2 == 0:
            n /= 2
        else:
            n = 3 * n + 1
        lngt += 1
    return lngt


@njit
def collatz_jit(n):
    lngt = 0
    while n != 1:
        if n % 2 == 0:
            n /= 2
        else:
            n = 3 * n + 1
        lngt += 1
    return lngt


def test():
    n = list(range(1, 100001))
    t_col = []
    t_col_jit = []
    print('Length eqality TEST:')
    for i in n:
        a = my_time(collatz, i)
        b = my_time(collatz_jit, i)
        if a[1] != b[1]:
            raise RuntimeError('Lengths are not equal!')
        t_col.append(a[0])
        t_col_jit.append(b[0])

    print('+++Lengths are equal+++', 'Sequences are converging!', sep='\n')

    xlabel('n')
    ylabel('time')
    plot(n, t_col, label='py')
    plot(n, t_col_jit, label='jit')
    legend()
    show()


if __name__ == '__main__':
    test()
    print('Git test!')
