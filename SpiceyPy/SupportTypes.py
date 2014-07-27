# Collection of supporting functions for wrapper functions
__author__ = 'Apollo117'
import ctypes
from ctypes import c_char_p
import numpy
import six


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
        return inString.split('\x00')[0]
    elif six.PY3:
        if isinstance(inString, c_char_p):
            return toPythonString(inString.value)
        return bytes.decode(inString)


def listtocharvector(x):
    assert (isinstance(x, list))
    return (ctypes.c_char_p * len(x))(*[stringToCharP(y) for y in x])


def charvector(ndim=1, lenvals=10):
    return ((ctypes.c_char * lenvals)*ndim)()


def listtodoublematrix(data, x=3, y=3):
    matrix = ((ctypes.c_double * x) * y)()
    for i, row in enumerate(data):
        matrix[i] = tuple(row)
    return matrix


def emptyDoubleMatrix(x=3, y=3):
    return ((ctypes.c_double * x) * y)()


def emptyDoubleVector(n):
    assert(isinstance(n, int))
    return (ctypes.c_double*n)()


def emptyIntVector(n):
    assert(isinstance(n, int))
    return (ctypes.c_int*n)()


def vectorToList(x):
    if isinstance(x[0], bool):
        return [y for y in x]
    elif isinstance(x[0], int):
        return [y for y in x]
    elif isinstance(x[0], float):
        return [y for y in x]
    elif isinstance(x[0].value, bytes):
        return [bytes.decode(y.value) for y in x]


def matrixToList(x):
    return [vectorToList(y) for y in x]


def stringToCharP(inobject, inlen=None):

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
        return stringToCharP(" " * inobject.value)
    if isinstance(inobject, int):
        return stringToCharP(" " * inobject)
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
    return ((ctypes.c_char * xLen) * yLen)(*[stringToCharP(l, inlen=xLen) for l in inList])


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
    return ctypes.cast(((ctypes.c_char * xLen) * yLen)(*[stringToCharP(l, inlen=xLen) for l in inList]),
                       ctypes.c_char_p)


class DoubleArrayType:
    # Class type that will handle all double vectors, inspiration from python cookbook 3rd edition
    def from_param(self, param):
        typename = type(param).__name__
        if hasattr(self, 'from_' + typename):
            return getattr(self, 'from_' + typename)(param)
        elif isinstance(param, ctypes.Array):
            return param
        else:
            raise TypeError("Can't convert %s" % typename)

    # Cast from lists/tuples
    def from_list(self, param):
        val = ((ctypes.c_double)*len(param))(*param)
        return val

    # Cast from Tuple
    def from_tuple(self, param):
        val = ((ctypes.c_double) * len(param))(*param)
        return val

    # Cast from a numpy array,
    def from_ndarray(self, param):
        #return param.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        # the above older method does not work with functions which take vectors of known size
        return numpy.ctypeslib.as_ctypes(param)

    # Cast from array.array objects
    def from_array(self, param):
        if param.typecode != 'd':
            raise TypeError('must be an array of doubles')
        ptr, _ = param.buffer_info()
        return ctypes.cast(ptr, ctypes.POINTER(ctypes.c_double))


class DoubleMatrixType:
    # Class type that will handle all double matricies, inspiration from python cookbook 3rd edition
    def from_param(self, param):
        typename = type(param).__name__
        if hasattr(self, 'from_' + typename):
            return getattr(self, 'from_' + typename)(param)
        elif isinstance(param, ctypes.Array):
            return param
        else:
            raise TypeError("Can't convert %s" % typename)

    # Cast from lists/tuples
    def from_list(self, param):
        val = ((ctypes.c_double*len(param[0]))*len(param))(*[DoubleArray.from_param(x) for x in param])
        return val

    # Cast from Tuple
    def from_tuple(self, param):
        val = ((ctypes.c_double*len(param[0]))*len(param))(*[DoubleArray.from_param(x) for x in param])
        return val

    # Cast from a numpy array
    def from_ndarray(self, param):
        #return param.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        return numpy.ctypeslib.as_ctypes(param)

    # Cast from a numpy matrix
    def from_matrix(self, param):
        #return param.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        return numpy.ctypeslib.as_ctypes(param)


class IntArrayType:
    # Class type that will handle all int vectors, inspiration from python cookbook 3rd edition
    def from_param(self, param):
        typename = type(param).__name__
        if hasattr(self, 'from_' + typename):
            return getattr(self, 'from_' + typename)(param)
        elif isinstance(param, ctypes.Array):
            return param
        else:
            raise TypeError("Can't convert %s" % typename)

    # Cast from lists/tuples
    def from_list(self, param):
        val = ((ctypes.c_int)*len(param))(*param)
        return val

    # Cast from Tuple
    def from_tuple(self, param):
        val = ((ctypes.c_int) * len(param))(*param)
        return val

    # Cast from a numpy array
    def from_ndarray(self, param):
        #return param.ctypes.data_as(ctypes.POINTER(ctypes.c_int)) # not sure if long is same as int, it should be..
        #return numpy.ctypeslib.as_ctypes(param)
        return self.from_param(param.tolist())

    # Cast from array.array objects
    def from_array(self, param):
        if param.typecode != 'i':
            raise TypeError('must be an array of ints')
        ptr, _ = param.buffer_info()
        return ctypes.cast(ptr, ctypes.POINTER(ctypes.c_int))


class BoolArrayType:
    # Class type that will handle all int vectors, inspiration from python cookbook 3rd edition
    def from_param(self, param):
        typename = type(param).__name__
        if hasattr(self, 'from_' + typename):
            return getattr(self, 'from_' + typename)(param)
        elif isinstance(param, ctypes.Array):
            return param
        else:
            raise TypeError("Can't convert %s" % typename)

    # Cast from lists/tuples
    def from_list(self, param):
        val = ((ctypes.c_bool) * len(param))(*param)
        return val

    # Cast from Tuple
    def from_tuple(self, param):
        val = ((ctypes.c_bool) * len(param))(*param)
        return val

    # Cast from a numpy array
    def from_ndarray(self, param):
        #return param.ctypes.data_as(ctypes.POINTER(ctypes.c_int)) # not sure if long is same as int, it should be..
        #return numpy.ctypeslib.as_ctypes(param)
        return self.from_param(param.tolist())


DoubleArray = DoubleArrayType()

IntArray = IntArrayType()

BoolArray = BoolArrayType()

DoubleMatrix = DoubleMatrixType()


class Plane(ctypes.Structure):
    _fields_ = [
        ('_normal', ctypes.c_double * 3),
        ('_constant', ctypes.c_double)
    ]

    @property
    def normal(self):
        return vectorToList(self._normal)

    @property
    def constant(self):
        return self._constant

    def __str__(self):
        return '<Plane: normal=%s; constant=%s>' % (', '.join([str(x) for x in self._normal]), self._constant)


class Ellipse(ctypes.Structure):
    _fields_ = [
        ('_center', ctypes.c_double * 3),
        ('_semi_major', ctypes.c_double * 3),
        ('_semi_minor', ctypes.c_double * 3)
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


class SpiceEKDataType(ctypes.c_int):
    _fields_ = [
        ('SPICE_CHR', ctypes.c_int(0)),
        ('SPICE_DP', ctypes.c_int(1)),
        ('SPICE_INT', ctypes.c_int(2)),
        ('SPICE_TIME', ctypes.c_int(3)),
        ('SPICE_BOOL', ctypes.c_int(4)),
    ]


class SpiceEKExprClass(ctypes.c_int):
    _fields_ = [
        ('SPICE_EK_EXP_COL', ctypes.c_int(0)),
        ('SPICE_EK_EXP_FUNC', ctypes.c_int(1)),
        ('SPICE_EK_EXP_EXPR', ctypes.c_int(2))
    ]


class SpiceEKAttDsc(ctypes.Structure):
    _fields_ = [
        ('cclass', ctypes.c_int),
        ('dtype', SpiceEKDataType),
        ('strlen', ctypes.c_int),
        ('size', ctypes.c_int),
        ('indexd', ctypes.c_bool),
        ('nullok', ctypes.c_bool)
    ]

    def __str__(self):
        return '<SpiceEKAttDsc cclass = %s, dtype = %s, strlen = %s, size = %s, indexd = %s, nullok = %s >' % \
               (self.cclass, self.dtype, self.strlen, self.size, self.indexd, self.nullok)


class SpiceEKSegSum(ctypes.Structure):
    _fields_ = [
        ('tabnam', ctypes.c_char * 65),
        ('nrows', ctypes.c_int),
        ('ncols', ctypes.c_int),
        ('cnames', (ctypes.c_char * 100) * 33),
        ('cdescrs', ctypes.c_char * 100)
    ]

    def __str__(self):
        return '<SpiceEKSegSum tabnam = %s, nrows = %s, ncols = %s, cnames = %s, cdescrs = %s >' % (self.tabnam, self.nrows, self.ncols, self.cnames, self.cdescrs)


#SpiceCell implementation below is inpart from github.com/DaRasch/spiceminer/
# and modified as needed for this author, maybe we should work together?

### helper classes/functions ###
BITSIZE = {'char': ctypes.sizeof(ctypes.c_char), 'int': ctypes.sizeof(ctypes.c_int), 'double': ctypes.sizeof(ctypes.c_double)}


def _char_getter(data_p, index, length):
    return toPythonString((ctypes.c_char * length).from_address(data_p + index * BITSIZE['char']))


def _double_getter(data_p, index, length):
    return ctypes.c_double.from_address(data_p + index * BITSIZE['double']).value


def _int_getter(data_p, index, length):
    return ctypes.c_int.from_address(data_p + index * BITSIZE['int']).value


def SPICEDOUBLE_CELL(size):
    return SpiceCell.double(size)


def SPICEINT_CELL(size):
    return SpiceCell.integer(size)


def SPICECHAR_CELL(size, length):
    return SpiceCell.character(size, length)


class SpiceCell(ctypes.Structure):
    #Most written by DaRasch
    DATATYPES_ENUM = {'char': 0, 'double': 1, 'int': 2, 'time': 3, 'bool': 4}
    DATATYPES_GET = [_char_getter, _double_getter] + [_int_getter] * 3
    baseSize = 6
    minCharLen = 6
    CTRLBLOCK = 6
    _fields_ = [
        ('dtype', ctypes.c_int),
        ('length', ctypes.c_int),
        ('size', ctypes.c_int),
        ('card', ctypes.c_int),
        ('isSet', ctypes.c_int),
        ('adjust', ctypes.c_int),
        ('init', ctypes.c_int),
        ('base', ctypes.c_void_p),
        ('data', ctypes.c_void_p)
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
        return '<SpiceCell dtype = %s, length = %s, size = %s, card = %s, isSet = %s, adjust = %s, init = %s, base = %s, data = %s>' % (self.dtype, self.length, self.size, self.card, self.isSet, self.adjust, self.init, self.base, self.data)

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
        return self.isSet is True

    @classmethod
    def character(cls, size, length):
        base = (ctypes.c_char * ((cls.CTRLBLOCK + size) * length))()
        data = (ctypes.c_char * (size * length)).from_buffer(
            base, cls.CTRLBLOCK * BITSIZE['char'] * length)
        instance = cls(cls.DATATYPES_ENUM['char'], length, size, 0, 1,
                       ctypes.cast(base, ctypes.c_void_p),
                       ctypes.cast(data, ctypes.c_void_p))
        return instance

    @classmethod
    def integer(cls, size):
        base = (ctypes.c_int * (cls.CTRLBLOCK + size))()
        data = (ctypes.c_int * size).from_buffer(
            base, cls.CTRLBLOCK * BITSIZE['int'])
        instance = cls(cls.DATATYPES_ENUM['int'], 0, size, 0, 1,
                       ctypes.cast(base, ctypes.c_void_p),
                       ctypes.cast(data, ctypes.c_void_p))
        return instance

    @classmethod
    def double(cls, size):
        base = (ctypes.c_double * (cls.CTRLBLOCK + size))()
        data = (ctypes.c_double * size).from_buffer(
            base, cls.CTRLBLOCK * BITSIZE['double'])
        instance = cls(cls.DATATYPES_ENUM['double'], 0, size, 0, 1,
                       ctypes.cast(base, ctypes.c_void_p),
                       ctypes.cast(data, ctypes.c_void_p))
        return instance

    def __len__(self):
        return self.card

    def __iter__(self):
        getter = SpiceCell.DATATYPES_GET[self.dtype]
        length, card, data = self.length, self.card, self.data
        for i in range(card):
            yield (getter(data, i, length))

    def __contains__(self, key):
        return key in self.__iter__()

    def __getitem__(self, key):
        getter = SpiceCell.DATATYPES_GET[self.dtype]
        length, card, data = self.length, self.card, self.data
        if isinstance(key, slice):
            start, stop, step = key.start or 0, key.stop or -1, key.step or 1
            #TODO Typechecking
            if card == 0:
                return []
            else:
                return list(getter(data, i, length)
                            for i in range(start % card, stop % card + 1, step))
        if key in range(-card, card):
            return getter(data, key, length)
        elif not isinstance(key, int):
            msg = 'SpiceCell inices must be integers, not {}'.format(type(key))
            raise TypeError(msg)
        else:
            raise IndexError('SpiceCell index out of range')

    def reset(self):
        self.card = 0
        self.init = 0