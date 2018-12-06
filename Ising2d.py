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
        p = []
        for s in range(-4, 5):
            p.append(exp(s/T) / (exp(s/T) + exp(-s/T)))
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
                self.p_up[i][j] = p[s + 4]

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
    lat = Ising(100)
    magn = []
    for t in range(1, 300):
        lat.set(t)
        lat.sweep()
        magn.append(lat.M())
    plot(magn)
    show()


if __name__ == '__main__':
    test()
