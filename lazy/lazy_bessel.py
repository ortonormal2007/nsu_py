from lazy import *
from math import factorial


class Bessel(Series):
    def __init__(self, n):
        self.n = n
        self.l = [0 for i in range(abs(n))] +\
            [Fraction(1, (2 ** abs(n)) * factorial(abs(n)))]
        if n < 0:
            self.l = [((-1) ** (abs(n))) * num for num in self.l]

    def __repr__(self):
        return f'J_{self.n}(x)'

    def step(self):
        k = int(((len(self.l) - 1) - self.n) / 2) + 1
        num = Fraction(-1, (4 * k * (self.n + k)))
        self.l.extend([0, self.l[-1] * num])


def b_eq_test(a, deg):
    b = Bessel(a)
    c = Shift(Diff(Diff(b)), 2) +           \
        Shift(Diff(b), 1) +                 \
        ((Series([0, 0, 1]) - a ** 2) * b)

    c[deg]
    b[deg]

    print('Equation: ' + str(c), 'Bessel: ' + str(b), '______', sep='\n')


def diff_test(a, deg):
    b = Bessel(a)
    be1 = Bessel(a - 1)
    be2 = Bessel(a + 1)
    d = Fraction(1, 2) * (be1 - be2)
    d1 = Diff(b)
    d[deg]
    d1[deg]
    print(f'(1/2) * (J_{a - 1} - J_{a + 1}) = ' + str(d),
          f'(J_{a})\' = ' + str(d1),
          '______', sep='\n')


def rec_test(a, deg):
    b = Bessel(a)
    be1 = Bessel(a - 1)
    be2 = Bessel(a + 1)
    d2 = be1 + be2
    d3 = 2 * a * Shift(b, -1)
    d2[deg]
    d3[deg]
    print(f'J_{a - 1} - J_{a + 1} = ' + str(d2),
          f'2 * J_{a} / x = ' + str(d3), sep='\n')


if __name__ == '__main__':
    a = 1
    deg = 5
    b_eq_test(a, deg)
    diff_test(a, deg)
    try:
        rec_test(a, deg)
    except AssertionError:
        print('Error: we have no any Loran yet =(')
