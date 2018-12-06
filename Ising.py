from math import exp
from matplotlib.pyplot import plot, show
from random import random
from timeit import timeit

class Ising(object):
    def __init__(self, n):
        self.n = n
        self.states = [1 for i in range(n ** 2)]
        self.p_up = [1 for i in range(n ** 2)]

    def set(self, T):
        p = []
        for s in range(-4, 5):
            p.append(exp(s/T) / (exp(s/T) + exp(-s/T)))
        for i in range(self.n ** 2):
            i_next = i + 1
            i_prev = i - 1
            i1_next = i + self.n
            i1_prev = i - self.n
            if i % self.n == 0:
                i_prev = i + (self.n - 1)
            elif i % self.n == self.n - 1:
                i_next = i - (self.n - 1)
            if i < self.n:
                i1_prev = self.n ** 2 - self.n + i
            elif i >= self.n ** 2 - 1 - self.n:
                i1_next = i % self.n
            S = self.states[i] * (self.states[i_next] + self.states[i_prev] + self.states[i1_next] + self.states[i1_prev])
            self.p_up[i] = p[s + 4]
    def sweep(self):
            for i in range(self.n ** 2):
                if random() <= self.p_up[i]:
                    self.states[i] = 1
                else:
                    self.states[i] = -1


    def M(self):
        return(sum(self.states) / self.n ** 2)


def test():
    lat = Ising(300)
    magn = []
    for t in range(1, 300):
        lat.set(t)
        lat.sweep()
        magn.append(lat.M())
    plot(magn)
    show()


if __name__ == '__main__':
    test()
