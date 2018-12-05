from matplotlib.pyplot import (plot, legend, show, xscale,
                               yscale, xlabel, ylabel, title)


def f(y, x):
    r = 0.1
    return r * y


def euler(xinit, tinit, tfinal, step, right):
    x = []
    y = []

    n = 1;
    x_next = 0;
    x_cur = xinit
    t_cur = tinit

    while t_cur <= tfinal:
        x_next = x_cur + step * right(x_cur, t_cur)
        x_cur = x_next
        x.append(t_cur)
        y.append(x_cur)
        t_cur = step * n
        n += 1
    print(x, y)
    plot(x, y)
    show()


euler(100, 0, 20, 1, f)