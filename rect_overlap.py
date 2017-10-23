# Classes and function for rectangle overlapping calculations, from:
# https://codereview.stackexchange.com/questions/31352/overlapping-rectangles

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Rect(object):
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

