"""
The MIT License (MIT)

Copyright (c) [2015-2017] [Andrew Annex]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

The MIT License (MIT)

Copyright (c) 2013 Philipp Rasch

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from ctypes import c_char_p, c_bool, c_int, c_double,\
    c_char, c_void_p, sizeof, \
    Array, create_string_buffer, cast, Structure, \
    string_at

import numpy
import six
from numpy import ctypeslib as numpc
# Collection of supporting functions for wrapper functions
__author__ = 'AndrewAnnex'

errorformat = """
================================================================================

Toolkit version: {tkvsn}

{short} --
{explain}
{long}

{traceback}

================================================================================\
"""


class SpiceyError(Exception):
    """
    SpiceyError wraps CSPICE errors.
    :type value: str
    """
    def __init__(self, value, found=None):
        self.value = value
        self.found = found

    def __str__(self):
        return self.value


def toDoubleVector(x):
    return DoubleArray.from_param(param=x)


def toDoubleMatrix(x):
    return DoubleMatrix.from_param(param=x)


def toIntVector(x):
    return IntArray.from_param(param=x)


def toIntMatrix(x):
    return IntMatrix.from_param(param=x)


def toBoolVector(x):
    return BoolArray.from_param(param=x)


def toPythonString(inString):
    if six.PY2:
        if isinstance(inString, c_char_p):
            return toPythonString(inString.value)
        return string_at(inString).rstrip()
    elif six.PY3:
        if isinstance(inString, c_char_p):
            return toPythonString(inString.value)
        return bytes.decode(string_at(inString), errors="ignore").rstrip()


def emptyCharArray(xLen=None, yLen=None):
    if not yLen:
        yLen = 1
    if not xLen:
        xLen = 1
    if isinstance(xLen, c_int):
        xLen = xLen.value
    if isinstance(yLen, c_int):
        yLen = yLen.value
    return ((c_char * xLen) * yLen)()


def emptyDoubleMatrix(x=3, y=3):
    if isinstance(x, c_int):
        x = x.value
    if isinstance(y, c_int):
        y = y.value
    return ((c_double * x) * y)()


def emptyDoubleVector(n):
    if isinstance(n, c_int):
        n = n.value
    assert(isinstance(n, int))
    return (c_double * n)()


def emptyIntMatrix(x=3, y=3):
    if isinstance(x, c_int):
        x = x.value
    if isinstance(y, c_int):
        y = y.value
    return ((c_int * x) * y)()


def emptyIntVector(n):
    if isinstance(n, c_int):
        n = n.value
    assert (isinstance(n, int))
    return (c_int * n)()


def emptyBoolVector(n):
    if isinstance(n, c_int):
        n = n.value
    return (c_bool * n)()


def cVectorToPython(x):
    """
    Convert the c vector data into the correct python data type
    (numpy arrays or strings)
    :param x:
    :return:
    """
    if isinstance(x[0], bool):
        return numpy.fromiter(x, numpy.bool, count=len(x))
    elif isinstance(x[0], int):
        return numpy.fromiter(x, numpy.int_, count=len(x))
    elif isinstance(x[0], float):
        return numpy.fromiter(x, numpy.float64, count=len(x))
    elif isinstance(x[0].value, bytes):
        return [toPythonString(y) for y in x]


def cMatrixToNumpy(x):
    """
    Convert a ctypes 2d array (or matrix) into a numpy array for python use
    :param x: thing to convert
    :return: numpy.ndarray
    """
    return numpc.as_array(x)


def stringToCharP(inobject, inlen=None):

    """
    :param inobject: input string, int for getting null string of length of int
    :param inlen: optional parameter, length of a given string can be specified
    :return:
    """
    if inlen and isinstance(inobject, str):
        return create_string_buffer(inobject.encode(encoding='UTF-8'), inlen)
    if isinstance(inobject, bytes):
        return inobject
    if isinstance(inobject, c_int):
        return stringToCharP(" " * inobject.value)
    if isinstance(inobject, int):
        return stringToCharP(" " * inobject)
    return c_char_p(inobject.encode(encoding='UTF-8'))


def listToCharArray(inList, xLen=None, yLen=None):
    assert (isinstance(inList, list))
    if not yLen:
        yLen = len(inList)
    if not xLen:
        xLen = max(len(s) for s in inList) + 1
    if isinstance(xLen, c_int):
        xLen = xLen.value
    if isinstance(yLen, c_int):
        yLen = yLen.value
    return ((c_char * xLen) * yLen)(*[stringToCharP(l, inlen=xLen) for l in inList])


def listToCharArrayPtr(inList, xLen=None, yLen=None):
    assert (isinstance(inList, list))
    if not yLen:
        yLen = len(inList)
    if not xLen:
        xLen = max(len(s) for s in inList) + 1
    if isinstance(xLen, c_int):
        xLen = xLen.value
    if isinstance(yLen, c_int):
        yLen = yLen.value
    return cast(((c_char * xLen) * yLen)(*[stringToCharP(l, inlen=xLen) for l in inList]), c_char_p)


class DoubleArrayType:
    # Class type that will handle all double vectors,
    # inspiration from python cookbook 3rd edition
    def from_param(self, param):
        typename = type(param).__name__
        if hasattr(self, 'from_' + typename):
            return getattr(self, 'from_' + typename)(param)
        elif isinstance(param, Array):
            return param
        else:
            raise TypeError("Can't convert %s" % typename)

    # Cast from lists/tuples
    def from_list(self, param):
        val = ((c_double) * len(param))(*param)
        return val

    # Cast from Tuple
    def from_tuple(self, param):
        val = ((c_double) * len(param))(*param)
        return val

    # Cast from a numpy array,
    def from_ndarray(self, param):
        # return param.data_as(POINTER(c_double))
        # the above older method does not work with
        # functions which take vectors of known size
        return numpy.ctypeslib.as_ctypes(param)

    # Cast from array.array objects
    def from_array(self, param):
        if param.typecode != 'd':
            raise TypeError('must be an array of doubles')
        return self.from_list(param)


class DoubleMatrixType:
    # Class type that will handle all double matricies,
    # inspiration from python cookbook 3rd edition
    def from_param(self, param):
        typename = type(param).__name__
        if hasattr(self, 'from_' + typename):
            return getattr(self, 'from_' + typename)(param)
        elif isinstance(param, Array):
            return param
        else:
            raise TypeError("Can't convert %s" % typename)

    # Cast from lists/tuples
    def from_list(self, param):
        val = ((c_double * len(param[0])) * len(param))(*[DoubleArray.from_param(x) for x in param])
        return val

    # Cast from Tuple
    def from_tuple(self, param):
        val = ((c_double * len(param[0])) * len(param))(*[DoubleArray.from_param(x) for x in param])
        return val

    # Cast from a numpy array
    def from_ndarray(self, param):
        return numpy.ctypeslib.as_ctypes(param)

    # Cast from a numpy matrix
    def from_matrix(self, param):
        return numpy.ctypeslib.as_ctypes(param)


class IntArrayType:
    # Class type that will handle all int vectors,
    # inspiration from python cookbook 3rd edition
    def from_param(self, param):
        typename = type(param).__name__
        if hasattr(self, 'from_' + typename):
            return getattr(self, 'from_' + typename)(param)
        elif isinstance(param, Array):
            return param
        else:
            raise TypeError("Can't convert %s" % typename)

    # Cast from lists/tuples
    def from_list(self, param):
        val = ((c_int) * len(param))(*param)
        return val

    # Cast from Tuple
    def from_tuple(self, param):
        val = ((c_int) * len(param))(*param)
        return val

    # Cast from a numpy array
    def from_ndarray(self, param):
        # return param.data_as(POINTER(c_int))
        # not sure if long is same as int, it should be..
        # return numpy.ctypeslib.as_ctypes(param)
        return self.from_param(param.tolist())

    # Cast from array.array objects
    def from_array(self, param):
        if param.typecode != 'i':
            raise TypeError('must be an array of ints')
        return self.from_list(param)


class IntMatrixType:
    # Class type that will handle all int matricies,
    # inspiration from python cookbook 3rd edition
    def from_param(self, param):
        typename = type(param).__name__
        if hasattr(self, 'from_' + typename):
            return getattr(self, 'from_' + typename)(param)
        elif isinstance(param, Array):
            return param
        else:
            raise TypeError("Can't convert %s" % typename)

    # Cast from lists/tuples
    def from_list(self, param):
        val = ((c_int * len(param[0])) * len(param))(*[IntArray.from_param(x) for x in param])
        return val

    # Cast from Tuple
    def from_tuple(self, param):
        val = ((c_int * len(param[0])) * len(param))(*[IntArray.from_param(x) for x in param])
        return val

    # Cast from a numpy array
    def from_ndarray(self, param):
        return numpy.ctypeslib.as_ctypes(param)

    # Cast from a numpy matrix
    def from_matrix(self, param):
        return numpy.ctypeslib.as_ctypes(param)

class BoolArrayType:
    # Class type that will handle all int vectors,
    # inspiration from python cookbook 3rd edition
    def from_param(self, param):
        typename = type(param).__name__
        if hasattr(self, 'from_' + typename):
            return getattr(self, 'from_' + typename)(param)
        elif isinstance(param, Array):
            return param
        else:
            raise TypeError("Can't convert %s" % typename)

    # Cast from lists/tuples
    def from_list(self, param):
        val = ((c_bool) * len(param))(*param)
        return val

    # Cast from Tuple
    def from_tuple(self, param):
        val = ((c_bool) * len(param))(*param)
        return val

    # Cast from a numpy array
    def from_ndarray(self, param):
        # return param.data_as(POINTER(c_int))
        # not sure if long is same as int, it should be..
        # return numpy.ctypeslib.as_ctypes(param)
        return self.from_param(param.tolist())


DoubleArray = DoubleArrayType()

IntArray = IntArrayType()

IntMatrix = IntMatrixType()

BoolArray = BoolArrayType()

DoubleMatrix = DoubleMatrixType()


class Plane(Structure):
    _fields_ = [
        ('_normal', c_double * 3),
        ('_constant', c_double)
    ]

    @property
    def normal(self):
        return cVectorToPython(self._normal)

    @property
    def constant(self):
        return self._constant

    def __str__(self):
        return '<SpicePlane: normal=%s; constant=%s>' % (', '.join([str(x) for x in self._normal]), self._constant)


class Ellipse(Structure):
    _fields_ = [
        ('_center', c_double * 3),
        ('_semi_major', c_double * 3),
        ('_semi_minor', c_double * 3)
    ]

    @property
    def center(self):
        return cVectorToPython(self._center)

    @property
    def semi_major(self):
        return cVectorToPython(self._semi_major)

    @property
    def semi_minor(self):
        return cVectorToPython(self._semi_minor)

    def __str__(self):
        return '<SpiceEllipse: center = %s, semi_major = %s, semi_minor = %s>' % \
               (self.center, self.semi_major, self.semi_minor)


class DataType(object):
    SPICE_CHR = 0
    SPICE_DP = 1
    SPICE_INT = 2
    SPICE_TIME = 3
    SPICE_BOOL = 4
    CHR = 0
    DP = 1
    INT = 2
    TIME = 3
    BOOL = 4

    def __init__(self):
        pass


class SpiceDSKDescr(Structure):
    _fields_ = [
        ('_surfce', c_int),
        ('_center', c_int),
        ('_dclass', c_int),
        ('_dtype', c_int),
        ('_frmcde', c_int),
        ('_corsys', c_int),
        ('_corpar', c_double * 10),
        ('_co1min', c_double),
        ('_co1max', c_double),
        ('_co2min', c_double),
        ('_co2max', c_double),
        ('_co3min', c_double),
        ('_co3max', c_double),
        ('_start', c_double),
        ('_stop', c_double),
    ]
    @property
    def surfce(self):
        return self._surfce

    @property
    def center(self):
        return self._center

    @property
    def dclass(self):
        return self._dclass

    @property
    def dtype(self):
        return self._dtype

    @property
    def frmcde(self):
        return self._frmcde

    @property
    def corsys(self):
        return self._corsys

    @property
    def corpar(self):
        return cVectorToPython(self._corpar)

    @property
    def co1min(self):
        return self._co1min

    @property
    def co1max(self):
        return self._co1max

    @property
    def co2min(self):
        return self._co2min

    @property
    def co2max(self):
        return self._co2max

    @property
    def co3min(self):
        return self._co3min

    @property
    def co3max(self):
        return self._co3max

    @property
    def start(self):
        return self._start

    @property
    def stop(self):
        return self._stop


class SpiceDLADescr(Structure):
    _fields_ = [
        ('_bwdptr', c_int),
        ('_fwdptr', c_int),
        ('_ibase', c_int),
        ('_isize', c_int),
        ('_dbase', c_int),
        ('_dsize', c_int),
        ('_cbase', c_int),
        ('_csize', c_int)
    ]
    @property
    def bwdptr(self):
        return self._bwdptr

    @property
    def fwdptr(self):
        return self._fwdptr

    @property
    def ibase(self):
        return self._ibase

    @property
    def isize(self):
        return self._isize

    @property
    def dbase(self):
        return self._dbase

    @property
    def dsize(self):
        return self._dsize

    @property
    def cbase(self):
        return self._cbase

    @property
    def csize(self):
        return self._csize


class SpiceEKDataType(c_int):
    _SPICE_CHR = c_int(0)
    _SPICE_DP  = c_int(1)
    _SPICE_INT = c_int(2)
    _SPICE_TIME = c_int(3)
    _SPICE_BOOL = c_int(4)


    _fields_ = [
        ('SPICE_CHR', _SPICE_CHR),
        ('SPICE_DP', _SPICE_DP),
        ('SPICE_INT', _SPICE_INT),
        ('SPICE_TIME', _SPICE_TIME),
        ('SPICE_BOOL', _SPICE_BOOL),
    ]

    SPICE_CHR =  _SPICE_CHR.value
    SPICE_DP  =  _SPICE_DP.value
    SPICE_INT =  _SPICE_INT.value
    SPICE_TIME = _SPICE_TIME.value
    SPICE_BOOL = _SPICE_BOOL.value


def emptySpiceEKDataTypeVector(n):
    if isinstance(n, c_int):
        n = n.value
    assert(isinstance(n, int))
    return (SpiceEKDataType * n)()


class SpiceEKExprClass(c_int):
    _SPICE_EK_EXP_COL = c_int(0)
    _SPICE_EK_EXP_FUNC = c_int(1)
    _SPICE_EK_EXP_EXPR = c_int(2)

    _fields_ = [
        ('SPICE_EK_EXP_COL',  _SPICE_EK_EXP_COL),
        ('SPICE_EK_EXP_FUNC', _SPICE_EK_EXP_FUNC),
        ('SPICE_EK_EXP_EXPR', _SPICE_EK_EXP_EXPR)
    ]

    SPICE_EK_EXP_COL = _SPICE_EK_EXP_COL.value
    SPICE_EK_EXP_FUNC = _SPICE_EK_EXP_FUNC.value
    SPICE_EK_EXP_EXPR = _SPICE_EK_EXP_EXPR.value


class SpiceSPK18Subtype(c_int):
    _S18TP0 = c_int(0)
    _S18TP1 = c_int(1)
    S18TP0  = _S18TP0.value
    S18TP1  = _S18TP1.value
    _fields_ = [
        ('S18TP0', _S18TP0),
        ('S18TP1', _S18TP1)
    ]


def emptySpiceEKExprClassVector(n):
    if isinstance(n, c_int):
        n = n.value
    assert(isinstance(n, int))
    return (SpiceEKExprClass * n)()


class SpiceEKAttDsc(Structure):
    _fields_ = [
        ('_cclass', c_int),
        ('_dtype', SpiceEKDataType),
        ('_strlen', c_int),
        ('_size', c_int),
        ('_indexd', c_bool),
        ('_nullok', c_bool)
    ]

    @property
    def cclass(self):
        return self._cclass

    @property
    def dtype(self):
        return self._dtype.value

    @property
    def strlen(self):
        return self._strlen

    @property
    def size(self):
        return self._size

    @property
    def indexd(self):
        return self._indexd

    @property
    def nullok(self):
        return self._nullok

    def __str__(self):
        return '<SpiceEKAttDsc cclass = %s, dtype = %s, strlen = %s, size = %s, indexd = %s, nullok = %s >' % \
               (self.cclass, self.dtype, self.strlen, self.size, self.indexd, self.nullok)


class SpiceEKSegSum(Structure):
    _fields_ = [
        ('_tabnam', c_char * 65),
        ('_nrows', c_int),
        ('_ncols', c_int),
        ('_cnames', (c_char * 100) * 33),
        ('_cdescrs', SpiceEKAttDsc * 100)
    ]

    @property
    def tabnam(self):
        return toPythonString(self._tabnam)

    @property
    def nrows(self):
        return self._nrows

    @property
    def ncols(self):
        return self._ncols

    @property
    def cnames(self):
        return cVectorToPython(self._cnames)[0:self.ncols]

    @property
    def cdescrs(self):
        return self._cdescrs[0:self.ncols]

    def __str__(self):
        return '<SpiceEKSegSum tabnam = %s, nrows = %s, ncols = %s, cnames = %s, cdescrs = %s >' % (self.tabnam, self.nrows, self.ncols, self.cnames, self.cdescrs)


# SpiceCell implementation below is inpart from github.com/DaRasch/spiceminer/
# and modified as needed for this author, maybe we should work together?

### helper classes/functions ###
BITSIZE = {'char': sizeof(c_char), 'int': sizeof(c_int), 'double': sizeof(c_double), 'bool': sizeof(c_int), 'time': sizeof(c_int)}


def _char_getter(data_p, index, length):
    return toPythonString((c_char * length).from_address(data_p + index * length * BITSIZE['char']))


def _double_getter(data_p, index, length):
    return c_double.from_address(data_p + index * BITSIZE['double']).value


def _int_getter(data_p, index, length):
    return c_int.from_address(data_p + index * BITSIZE['int']).value


def SPICEDOUBLE_CELL(size):
    return SpiceCell.double(size)


def SPICEINT_CELL(size):
    return SpiceCell.integer(size)


def SPICECHAR_CELL(size, length):
    return SpiceCell.character(size, length)

def SPICEBOOL_CELL(size):
    return SpiceCell.bool(size)

def SPICETIME_CELL(size):
    return SpiceCell.time(size)


class SpiceCell(Structure):
    #Most written by DaRasch, see included MIT license at file header
    DATATYPES_ENUM = {'char': 0, 'double': 1, 'int': 2, 'time': 3, 'bool': 4}
    DATATYPES_GET = [_char_getter, _double_getter] + [_int_getter] * 3
    baseSize = 6
    minCharLen = 6
    CTRLBLOCK = 6
    _fields_ = [
        ('dtype', c_int),
        ('length', c_int),
        ('size', c_int),
        ('card', c_int),
        ('isSet', c_int),
        ('adjust', c_int),
        ('init', c_int),
        ('base', c_void_p),
        ('data', c_void_p)
    ]

    def __init__(self, dtype=None, length=None, size=None, card=None, isSet=None, base=None, data=None):
        super(SpiceCell, self).__init__()
        self.dtype = dtype
        self.length = length
        self.size = size
        self.card = card
        self.isSet = isSet
        self.adjust = 0  # Always False, because not implemented
        self.init = 0  # Always False, because this is the constructor
        self.base = base  # void pointer
        self.data = data

    def __str__(self):
        return '<SpiceCell dtype = %s, length = %s, size = %s, card = %s,' \
               ' isSet = %s, adjust = %s, init = %s, base = %s, data = %s>' % \
               (self.dtype, self.length, self.size, self.card, self.isSet,
                self.adjust, self.init, self.base, self.data)

    def is_int(self):
        return self.dtype == 2

    def is_double(self):
        return self.dtype == 1

    def is_char(self):
        return self.dtype == 0

    def is_time(self):
        return self.dtype == 3

    def is_bool(self):
        return self.dtype == 4

    def is_set(self):
        return self.isSet == 1

    @classmethod
    def character(cls, size, length):
        base = (c_char * ((cls.CTRLBLOCK + size) * length))()
        data = (c_char * (size * length)).from_buffer(
            base, cls.CTRLBLOCK * BITSIZE['char'] * length)
        instance = cls(cls.DATATYPES_ENUM['char'], length, size, 0, 1,
                       cast(base, c_void_p),
                       cast(data, c_void_p))
        return instance

    @classmethod
    def integer(cls, size):
        base = (c_int * (cls.CTRLBLOCK + size))()
        data = (c_int * size).from_buffer(
            base, cls.CTRLBLOCK * BITSIZE['int'])
        instance = cls(cls.DATATYPES_ENUM['int'], 0, size, 0, 1,
                       cast(base, c_void_p),
                       cast(data, c_void_p))
        return instance

    @classmethod
    def double(cls, size):
        base = (c_double * (cls.CTRLBLOCK + size))()
        data = (c_double * size).from_buffer(
            base, cls.CTRLBLOCK * BITSIZE['double'])
        instance = cls(cls.DATATYPES_ENUM['double'], 0, size, 0, 1,
                       cast(base, c_void_p),
                       cast(data, c_void_p))
        return instance

    @classmethod
    def bool(cls, size):
        base = (c_int * (cls.CTRLBLOCK + size))()
        data = (c_int * size).from_buffer(
            base, cls.CTRLBLOCK * BITSIZE['bool'])
        instance = cls(cls.DATATYPES_ENUM['bool'], 0, size, 0, 1,
                       cast(base, c_void_p),
                       cast(data, c_void_p))
        return instance

    @classmethod
    def time(cls, size):
        base = (c_int * (cls.CTRLBLOCK + size))()
        data = (c_int * size).from_buffer(
            base, cls.CTRLBLOCK * BITSIZE['time'])
        instance = cls(cls.DATATYPES_ENUM['time'], 0, size, 0, 1,
                       cast(base, c_void_p),
                       cast(data, c_void_p))
        return instance

    def __len__(self):
        return self.card

    def __iter__(self):
        getter = SpiceCell.DATATYPES_GET[self.dtype]
        length, card, data = self.length, self.card, self.data
        for i in six.moves.range(card):
            yield (getter(data, i, length))

    def __contains__(self, key):
        return key in self.__iter__()

    def __getitem__(self, key):
        getter = SpiceCell.DATATYPES_GET[self.dtype]
        if isinstance(key, slice):
            #TODO Typechecking
            if self.card == 0:
                return []
            else:
                start, stop, step = key.indices(self.card)
                return [getter(self.data, i, self.length) for i in six.moves.range(start, stop, step)]
        elif key in six.moves.range(-self.card, self.card):
            index = key if key >= 0 else self.card - abs(key)
            return getter(self.data, index, self.length)
        elif not isinstance(key, int):
            raise TypeError('SpiceCell indices must be integers, not {}'.format(type(key)))
        else:
            raise IndexError('SpiceCell index out of range')

    def reset(self):
        self.card = 0
        self.init = 0
