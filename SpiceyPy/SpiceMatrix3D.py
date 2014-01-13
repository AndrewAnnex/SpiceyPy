__author__ = 'Apollo117'
import numpy


class SpiceMatrix3D(numpy.matrix):
    pass






def test():
    a = SpiceMatrix3D([[0,0,0],[1,1,0],[1,1,1]])
    print(a)

test()