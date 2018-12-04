import tkinter as tkr
import rect as rt
from random import randint as rd

GRID = 10


def draw_rects(r1, r2):
    # draws rectangles using Tkinter modules
    wind = tkr.Tk()
    wind.title('domiki')
    canv = tkr.Canvas(wind, width=200, height=200, bg='#bbbbbb')
    canv.grid()
    canv.create_rectangle(r1.x1 * GRID, r1.y1 * GRID,
                          r1.x2 * GRID, r1.y2 * GRID)
    canv.create_rectangle(r2.x1 * GRID, r2.y1 * GRID,
                          r2.x2 * GRID, r2.y2 * GRID)
    wind.mainloop()


def test_ridiculous(count):
    # Returns difference between numbers of triggering of correct and incorrect
    # overlapping-control functions
    inter1, inter2 = 0, 0
    for i in range(count):
        # Generates coordinates within 0 - 10 range
        x1, y1, dx1, dy1 = (rd(0, 10) for i in range(4))
        x2, y2, dx2, dy2 = (rd(0, 10) for i in range(4))

        # Creates instances of  rect()
        rect1 = rt.rect(x1, y1, dx1, dy1)
        rect2 = rt.rect(x2, y2, dx2, dy2)

        # Gets booleans of overlapping
        is_inter1 = rect2.intersect1(rect1)
        is_inter2 = rect2 & rect1
        if is_inter1 and not is_inter2:
            draw_rects(rect1, rect2)

        # Piece of manual test
        # draw_rects(rect1, rect2)
        # print(str(i + 1) + ' turn')
        # print('Intersection 1 is ' + str(is_inter1))
        # print('Intersection 2 is ' + str(is_inter2))
        # print('___________')

        # Counting Trues
        inter1 += int(is_inter1)
        inter2 += int(is_inter2)
    # print('inter1: ' + str(inter1) + ', ' + 'inter2: ' + str(inter2))

    # Returns difference
    return(inter2 - inter1)


def test_ridiculous1():
    # kinda Mote-Karlos method:
    sum = 0
    for i in range(1, 10100, 100):
        a = test_ridiculous(i)
        sum += a/i
        print(str(i) + '  ' + str(a) + '  ' + '*' * a)
    # average percentage
    print(sum/100)


def test_manual():
    # Manual coordinates entering
    x1, y1, dx1, dy1 = (
        int(x) for x in input('Enter x1, y1, dx1, dy1 :').split())
    x2, y2, dx2, dy2 = (
        int(y) for y in input('Enter x2, y2, dx2, dy2 :').split())
    rect1 = rt.rect(x1, y1, dx1, dy1)
    rect2 = rt.rect(x2, y2, dx2, dy2)
    # print(rect2.intersect1(rect1))
    print(rect2 & (rect1,))
    draw_rects(rect1, rect2)


def test_many(count):
    def coord_gen():
        a = {note: rd(0, 10) for note in ('x', 'y', 'dx', 'dy')}
        return a

    print(rt.rect(**coord_gen()) &
          list(rt.rect(**coord_gen()) for i in range(count)))


def main():
    # print(rt.rect(1, 1, 2, 3) & rt.rect(5, 5, 7, 1), rt.rect(5, 5, 5, 5))
    # test_many(10)
    test_manual()
    # test_ridiculous1()


main()
