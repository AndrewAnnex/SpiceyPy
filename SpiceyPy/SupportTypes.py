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


class SpiceEKDataType(ctypes.py_object):
    #No clue whatsoever if py_object works here
    SPICE_CHR = ctypes.c_int(0)
    SPICE_DP = ctypes.c_int(1)
    SPICE_INT = ctypes.c_int(2)
    SPICE_TIME = ctypes.c_int(3)
    SPICE_BOOL = ctypes.c_int(4)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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

#SpiceCell implementation below is inpart from github.com/DaRasch/spiceminer/
# and modified as needed for this author, maybe we should work together?

### helper classes/functions ###
BITSIZE = {'char': ctypes.sizeof(ctypes.c_char), 'int': ctypes.sizeof(ctypes.c_int), 'double': ctypes.sizeof(ctypes.c_double)}


def _char_getter(data_p, index, length):
    return (ctypes.c_char * length).from_address(data_p + index * BITSIZE['char']).value


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