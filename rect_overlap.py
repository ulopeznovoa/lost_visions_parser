# Classes and function for rectangle overlapping calculations, from:
# https://codereview.stackexchange.com/questions/31352/overlapping-rectangles


class Shape(object):
    pass

class Point(Shape):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rect(Shape):
    def __init__(self, p1, p2):
        '''Store the top, bottom, left and right values for points p1 and p2 are the (corners) in either order'''
        self.left   = min(p1.x, p2.x)
        self.right  = max(p1.x, p2.x)
        self.bottom = min(p1.y, p2.y)
        self.top    = max(p1.y, p2.y)

    def overlap(r1,r2):
        hoverlaps = (r1.left <= r2.right) and (r1.right >= r2.left)
        voverlaps = (r1.top >= r2.bottom) and (r1.bottom <= r2.top)
        return hoverlaps and voverlaps

    def overlap_percent(r1,r2):
        iLeft = max(r1.left, r2.left)
        iRight = min(r1.right, r2.right)
        iTop = min(r1.top, r2.top)
        iBottom = max(r1.bottom, r2.bottom)

        si = max(0, iRight - iLeft) * max(0, iTop - iBottom)
        s_r1 = (r1.right - r1.left) * (r1.top - r1.bottom)
        s_r2 = (r2.right - r2.left) * (r2.top - r2.bottom)

        #return s_r1 + s_r2 - si
        return si/s_r2

