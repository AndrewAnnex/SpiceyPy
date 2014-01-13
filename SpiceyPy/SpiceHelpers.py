__author__ = 'Apollo117'
#misc functions and such
import numpy


def MaxAbs(a, b):
    one = numpy.abs(a)
    two = numpy.abs(b)
    if one > two:
        return one
    elif two > one:
        return two
    else:
        return one