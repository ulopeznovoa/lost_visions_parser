import unittest

from rect_overlap import *

class TestShape(unittest.TestCase):
    def test_overlap_percent(self):

        r1 = Rect(Point(1,1),Point(4,5))
        r2 = Rect(Point(1,1),Point(2,2))

        out = Rect.overlap_percent(r1,r2)

        print(out)
        #self.fail()


if __name__ == '__main__':
    unittest.main()