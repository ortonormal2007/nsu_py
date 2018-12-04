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
            # print(f'({i_prev},{i_next},{i1_prev},{i1_next})', sep=' ')
            # if i % self.n == self.n - 1:
            #     print('\n')
            S = self.states[i] * (self.states[i_next] + self.states[i_prev] + self.states[i1_next] + self.states[i1_prev])
            self.p_up[i] = exp(S/T) / (exp(S/T) + exp(-S/T))
    def sweep(self):
            for i in range(self.n ** 2):
                if random() <= self.p_up[i]:
                    self.states[i] = 1
                else:
                    self.states[i] = -1


    def M(self):
        return(sum(self.states) / self.n ** 2)


def test():
    lat = Ising(10000)
    # magn = []
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
