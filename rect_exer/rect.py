class rect():
    def __init__(self, x, y, dx, dy):
        self.x1 = x
        self.y1 = y
        self.dx = dx
        self.dy = dy
        self.x2 = self.x1 + self.dx
        self.y2 = self.y1 - self.dy

    def __repr__(self):
        mes = 'x1 = {}, y1 = {}, x2 = {}, y2 = {}'.format(
              self.x1, self.y1, self.x2, self.y2)
        return mes

    def __and__(self, rects):
        # & overloading
        if isinstance(rects, (list, tuple)):
            a = [self.intersect2(r) for r in rects]
            return any(a)
        elif isinstance(rects, rect):
            return self.intersect2(rect)

    def intersect1(self, b2):
        # "stupid" method
        a = [self.is_inside(coords) for coords in b2.corners()]
        b = [b2.is_inside(coords) for coords in self.corners()]
        return any(a) or any(b)

    def intersect2(self, b2):
        # correct method
        if (self.x1 <= b2.x2 and self.x2 >= b2.x1) and\
           (self.y1 >= b2.y2 and self.y2 <= b2.y1):
            return True
        else:
            return False

    def area(self):
        return self.dx * self.dy

    def is_inside(self, coords):
        x = coords[0]
        y = coords[1]
        if self.x1 <= x <= self.x2 and self.y2 <= y <= self.y1:
            return True
        else:
            return False

    def corners(self):
        return [(self.x1, self.y1), (self.x1 + self.dx, self.y1),
                (self.x1, self.y1 - self.dy), (self.x2, self.y2)]


if __name__ == "__main__":
    rect1 = rect(1, 1, 1, 1)
    rect2 = rect(3, 1, 1, 1)
    print(rect2.is_crossing(rect1))
