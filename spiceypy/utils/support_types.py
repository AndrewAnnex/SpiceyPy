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
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


def toDoubleVector(x):
    return DoubleArray.from_param(param=x)


def toDoubleMatrix(x):
    return DoubleMatrix.from_param(param=x)


def toIntVector(x):
    return IntArray.from_param(param=x)


def toBoolVector(x):
    return BoolArray.from_param(param=x)


def toPythonString(inString):
    if six.PY2:
        if isinstance(inString, c_char_p):
            return toPythonString(inString.value)
        return string_at(inString)
    elif six.PY3:
        if isinstance(inString, c_char_p):
            return toPythonString(inString.value)
        return bytes.decode(string_at(inString))


def charvector(ndim=1, lenvals=10):
    return ((c_char * lenvals) * ndim)()


def listtodoublematrix(data, x=3, y=3):
    matrix = ((c_double * x) * y)()
    for i, row in enumerate(data):
        matrix[i] = tuple(row)
    return matrix


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
    return ((c_double * x) * y)()


def emptyDoubleVector(n):
    if isinstance(n, c_int):
        n = n.value
    assert(isinstance(n, int))
    return (c_double * n)()


def emptyIntVector(n):
    if isinstance(n, c_int):
        n = n.value
    assert (isinstance(n, int))
    return (c_int * n)()


def vectorToList(x):
    if isinstance(x[0], bool):
        return numpy.fromiter(x, numpy.bool, count=len(x))
    elif isinstance(x[0], int):
        return numpy.fromiter(x, numpy.int_, count=len(x))
    elif isinstance(x[0], float):
        return numpy.fromiter(x, numpy.float64, count=len(x))
    elif isinstance(x[0].value, bytes):
        return [toPythonString(y) for y in x]


def matrixToList(x):
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
        # return param.data_as(POINTER(c_double))
        return numpy.ctypeslib.as_ctypes(param)

    # Cast from a numpy matrix
    def from_matrix(self, param):
        # return param.data_as(POINTER(c_double))
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

BoolArray = BoolArrayType()

DoubleMatrix = DoubleMatrixType()


class Plane(Structure):
    _fields_ = [
        ('_normal', c_double * 3),
        ('_constant', c_double)
    ]

    @property
    def normal(self):
        return vectorToList(self._normal)

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
        return vectorToList(self._center)

    @property
    def semi_major(self):
        return vectorToList(self._semi_major)

    @property
    def semi_minor(self):
        return vectorToList(self._semi_minor)

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


class SpiceEKDataType(c_int):
    _fields_ = [
        ('SPICE_CHR', c_int(0)),
        ('SPICE_DP', c_int(1)),
        ('SPICE_INT', c_int(2)),
        ('SPICE_TIME', c_int(3)),
        ('SPICE_BOOL', c_int(4)),
    ]


class SpiceEKExprClass(c_int):
    _fields_ = [
        ('SPICE_EK_EXP_COL', c_int(0)),
        ('SPICE_EK_EXP_FUNC', c_int(1)),
        ('SPICE_EK_EXP_EXPR', c_int(2))
    ]


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
        return vectorToList(self._cnames)[0:self.ncols]

    @property
    def cdescrs(self):
        return self._cdescrs[0:self.ncols]

    def __str__(self):
        return '<SpiceEKSegSum tabnam = %s, nrows = %s, ncols = %s, cnames = %s, cdescrs = %s >' % (self.tabnam, self.nrows, self.ncols, self.cnames, self.cdescrs)


# SpiceCell implementation below is inpart from github.com/DaRasch/spiceminer/
# and modified as needed for this author, maybe we should work together?

### helper classes/functions ###
BITSIZE = {'char': sizeof(c_char), 'int': sizeof(c_int), 'double': sizeof(c_double)}


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


class SpiceCell(Structure):
    #Most written by DaRasch
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