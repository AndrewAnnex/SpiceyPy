# Collection of supporting functions for wrapper functions
__author__ = 'Apollo117'
import ctypes
import numpy.ctypeslib as npc


def listtodoublevector(x):
    assert(isinstance(x, list))
    return (ctypes.c_double * len(x))(*x)


def listtointvector(x):
    assert(isinstance(x, list))
    return (ctypes.c_int * len(x))(*x)


def listtocharvector(x):
    assert (isinstance(x, list))
    return (ctypes.c_char_p * len(x))(*[strtocharpoint(y) for y in x])


def charvector(ndim=1, lenvals=10):
    return ((ctypes.c_char * lenvals)*ndim)()


def listtodoublematrix(data, x=3, y=3):
    matrix = ((ctypes.c_double * x) * y)()
    for i, row in enumerate(data):
        matrix[i] = tuple(row)
    return matrix


def doubleMatrix(x=3, y=3):
    return ((ctypes.c_double * x) * y)()


def doubleVector(n):
    assert(isinstance(n, int))
    return (ctypes.c_double*n)()


def intvector(n):
    assert(isinstance(n, int))
    return (ctypes.c_int*n)()


def vectortolist(x):
    return [y for y in x]


def matrixtolist(x):
    return [vectortolist(y) for y in x]


def strtocharpoint(x):
    if isinstance(x, bytes):
        return x
    if isinstance(x, ctypes.c_int):
        return strtocharpoint(" " * x.value)
    if isinstance(x, int):
        return strtocharpoint(" " * x)
    return ctypes.c_char_p(x.encode(encoding='UTF-8'))


def listtosmartstrarray(inlist):
    lenvals = max([len(x) for x in inlist])
    n = len(inlist)
    print(lenvals, n)

#def doublePtr():
#    return ctypes.POINTER(ctypes.c_double)


#def intPrt():
#    return ctypes.POINTER(ctypes.c_int)

class Plane(ctypes.Structure):
    _fields_ = [
        ('normal', ctypes.c_double*3),
        ('constant', ctypes.c_double)
    ]

    def __str__(self):
        return '<Plane: normal=%s; constant=%s>' % (', '.join([str(x) for x in self.normal]), self.constant)