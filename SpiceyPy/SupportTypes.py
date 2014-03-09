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
    return ctypes.c_char_p(x.encode(encoding='UTF-8'))


#def doublePtr():
#    return ctypes.POINTER(ctypes.c_double)


#def intPrt():
#    return ctypes.POINTER(ctypes.c_int)