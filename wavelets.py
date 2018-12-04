from sympy import *
from sympy.plotting import plot3d

init_printing()

def one_d():
    C1, C2 = symbols('C1 C2', real=True)
    a = Symbol('a', positive=True)
    t = Symbol('t', real=True)
    psi = C1 * (1 + C2 * t ** 2) * exp(-t ** 2 / (2 * a ** 2))
    it1 = Integral(psi, (t, -oo, oo)).doit()
    it2 = Integral(psi ** 2, (t, -oo, oo)).doit()

    roots = [C1, C2]
    slv = solve([it1, it2 - 1], roots)
    preview(slv)

    slv1 = dict(zip(roots, slv[0]))
    slv2 = dict(zip(roots, slv[1]))
    psi1 = psi.subs(slv1)
    psi1 = psi1.subs(a, 1)
    psi2 = psi.subs(slv2)
    psi2 = psi2.subs(a, 1)

    plot(psi1, psi2, (t, -5, 5))

def two_d():
    C1, C2 = symbols('C1 C2', real=True)
    a = Symbol('a', positive=True)
    x, y = symbols('x y', real=True)   
    psi = C1 * (1 + C2 * (x ** 2 + y ** 2)) * exp(-(x ** 2 + y ** 2) / (2 * a ** 2))

    it1 = Integral(psi, (x, -oo, oo), (y, -oo, oo)).doit()
    it2 = Integral(psi ** 2, (x, -oo, oo), (y, -oo, oo)).doit()

    roots = [C1, C2]
    slv = solve([it1, it2 - 1], roots)

    preview(slv)

    slv1 = dict(zip(roots, slv[0]))
    slv2 = dict(zip(roots, slv[1]))

    psi1 = psi.subs(slv1)
    psi1 = psi1.subs(a, 1)
    psi2 = psi.subs(slv2)
    psi2 = psi2.subs(a, 1)
    print(psi1)

    plot3d(psi1, (x, -5, 5), (y, -5, 5))

two_d()