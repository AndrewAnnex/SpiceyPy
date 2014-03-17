# Collection of supporting functions for wrapper functions
__author__ = 'Apollo117'
import ctypes


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


def vectortotuple(x):
    return tuple(vectortolist(x))


def matrixtolist(x):
    return [vectortolist(y) for y in x]


def strtocharpoint(inobject, inlen=None):

    """
    :param inobject: input string, int for getting null string of length of int
    :param inlen: optional parameter, length of a given string can be specified
    :return:
    """
    if inlen and isinstance(inobject, str):
        return ctypes.create_string_buffer(inobject.encode(encoding='UTF-8'), inlen)
    if isinstance(inobject, bytes):
        return inobject
    if isinstance(inobject, ctypes.c_int):
        return strtocharpoint(" " * inobject.value)
    if isinstance(inobject, int):
        return strtocharpoint(" " * inobject)
    return ctypes.c_char_p(inobject.encode(encoding='UTF-8'))


def listToCharArray(inList, xLen=None, yLen=None):
    assert (isinstance(inList, list))
    if not yLen:
        yLen = len(inList)
    if not xLen:
        xLen = max(len(s) for s in inList)
    if isinstance(xLen, ctypes.c_int):
        xLen = xLen.value
    if isinstance(yLen, ctypes.c_int):
        yLen = yLen.value
    return ((ctypes.c_char*xLen)*yLen)(*[strtocharpoint(l, inlen=xLen) for l in inList])


def listToCharArrayPtr(inList, xLen=None, yLen=None):
    assert (isinstance(inList, list))
    if not yLen:
        yLen = len(inList)
    if not xLen:
        xLen = max(len(s) for s in inList)
    if isinstance(xLen, ctypes.c_int):
        xLen = xLen.value
    if isinstance(yLen, ctypes.c_int):
        yLen = yLen.value
    return ctypes.cast(((ctypes.c_char*xLen)*yLen)(*[strtocharpoint(l, inlen=xLen) for l in inList]), ctypes.c_char_p)


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


class Ellipse(ctypes.Structure):
    _fields_ = [
        ('center', ctypes.c_double*3),
        ('semi_major', ctypes.c_double*3),
        ('semi_minor', ctypes.c_double*3)
    ]

    def __str__(self):
        return '<SpiceEllipse: center = %s, semi_major = %s, semi_minor = %s>' % (self.center, self.semi_major, self.semi_minor)