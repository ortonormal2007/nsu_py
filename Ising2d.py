from math import exp
from matplotlib.pyplot import plot, show
from random import random
from timeit import timeit


class Ising(object):
    def __init__(self, n):
        self.n = n
        self.states = [[1 for i in range(n)] for j in range(n)]
        self.p_up = [[1 for i in range(n)] for j in range(n)]

    def set(self, T):
        for i in range(self.n):
            for j in range(self.n):
                i_next = i + 1
                i_prev = i - 1
                j_next = j + 1
                j_prev = j - 1
                if i == self.n - 1:
                    i_next = 0
                if j == self.n - 1:
                    j_next = 0
                S = self.states[i][j] * (self.states[i_next][j] +
                                         self.states[i_prev][j] +
                                         self.states[i][j_next] +
                                         self.states[i][j_prev])
                self.p_up[i][j] = exp(S/T) / (exp(S/T) + exp(-S/T))

    def sweep(self):
        for i in range(self.n):
            for j in range(self.n):
                if random() <= self.p_up[i][j]:
                    self.states[i][j] = 1
                else:
                    self.states[i][j] = -1

    def M(self):
        return(sum((sum(x) for x in self.states)) / self.n ** 2)


def test():
    lat = Ising(10000)
    magn = []
    for t in range(1, 300):
        lat.set(t)
        lat.sweep()
        print(lat.M())
        # magn.append(lat.M())
    # plot(magn)
    # show()


if __name__ == '__main__':
    # test()
    print(timeit('test', number=100000, globals=globals()))