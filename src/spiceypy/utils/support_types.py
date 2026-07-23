"""
The MIT License (MIT)

Copyright (c) [2015-2025] [Andrew Annex]

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

import builtins
import collections.abc as collections_abc

from array import array
from ctypes import (
    c_char_p,
    c_int,
    c_double,
    c_char,
    c_void_p,
    sizeof,
    Array,
    create_string_buffer,
    cast,
    Structure,
    string_at,
    POINTER,
)

import numpy
from numpy import ctypeslib as numpc

from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Iterator,
    List,
    Optional,
    Sequence,
    Union,
)
from typing import cast as type_cast

if TYPE_CHECKING:
    # spiceypy.py injects these exception classes into this module at import
    # time for backwards compatibility (importing them here at runtime would
    # be a circular import); declare them so static checkers know they exist.
    from . import exceptions as _exceptions

    SpiceyError: type[_exceptions.SpiceyError]
    SpiceyPyError: type[_exceptions.SpiceyPyError]
    NotFoundError: type[_exceptions.NotFoundError]
    SpiceyPyIOError: type[_exceptions.SpiceyPyIOError]
    SpiceyPyMemoryError: type[_exceptions.SpiceyPyMemoryError]
    SpiceyPyTypeError: type[_exceptions.SpiceyPyTypeError]
    SpiceyPyKeyError: type[_exceptions.SpiceyPyKeyError]
    SpiceyPyIndexError: type[_exceptions.SpiceyPyIndexError]
    SpiceyPyRuntimeError: type[_exceptions.SpiceyPyRuntimeError]
    SpiceyPyZeroDivisionError: type[_exceptions.SpiceyPyZeroDivisionError]
    SpiceyPyValueError: type[_exceptions.SpiceyPyValueError]

# Collection of supporting functions for wrapper functions
__author__ = "AndrewAnnex"


def to_double_vector(x: Any) -> Array[c_double]:
    return DoubleArray.from_param(param=x)


def to_double_matrix(x: Any) -> Array[Array[c_double]]:
    return DoubleMatrix.from_param(param=x)


def to_int_vector(x: Any) -> Array[c_int]:
    return IntArray.from_param(param=x)


def to_int_matrix(x: Any) -> Array[Array[c_int]]:
    return IntMatrix.from_param(param=x)


def is_iterable(i: Any) -> bool:
    """
    From stackoverflow "how-to-tell-a-variable-is-iterable-but-not-a-string"
    :param i: input collection
    :return: if the input is iterable but not a string
    """
    return isinstance(i, collections_abc.Iterable) and not isinstance(i, str)


def to_python_string(in_string: Any) -> str:
    if isinstance(in_string, c_char_p):
        return to_python_string(in_string.value)
    else:
        return bytes.decode(string_at(in_string), errors="ignore").rstrip()


def empty_char_array(
    x_len: int | c_int | None = None, y_len: int | c_int | None = None
) -> Array[Array[c_char]]:
    if not y_len:
        y_len = 1
    if not x_len:
        x_len = 1
    if isinstance(x_len, c_int):
        x_len = x_len.value
    if isinstance(y_len, c_int):
        y_len = y_len.value
    assert isinstance(x_len, int)
    assert isinstance(y_len, int)
    return ((c_char * x_len) * y_len)()


def empty_double_matrix(
    x: int | c_int = 3, y: int | c_int = 3
) -> Array[Array[c_double]]:
    if isinstance(x, c_int):
        x = x.value
    if isinstance(y, c_int):
        y = y.value
    return ((c_double * x) * y)()


def empty_double_vector(n: int | c_int) -> Array[c_double]:
    if isinstance(n, c_int):
        n = n.value
    assert isinstance(n, int)
    return (c_double * n)()


def empty_int_matrix(x: int | c_int = 3, y: int | c_int = 3) -> Array[Array[c_int]]:
    if isinstance(x, c_int):
        x = x.value
    if isinstance(y, c_int):
        y = y.value
    return ((c_int * x) * y)()


def empty_int_vector(n: int | c_int) -> Array[c_int]:
    if isinstance(n, c_int):
        n = n.value
    assert isinstance(n, int)
    return (c_int * n)()


def c_vector_to_python(x: Any) -> Any:
    """
    Convert the c vector data into the correct python data type
    (numpy arrays or strings)

    :param x: ctypes array
    :return: Iterable
    """
    if isinstance(x[0], bool):
        return numpy.frombuffer(x, dtype=numpy.bool_).copy()
    elif isinstance(x[0], int):
        return numpy.frombuffer(x, dtype=numpy.int32).copy()
    elif isinstance(x[0], float):
        return numpy.frombuffer(x, dtype=numpy.float64).copy()
    elif isinstance(x[0].value, bytes):
        return [to_python_string(y) for y in x]


def c_int_vector_to_bool_python(x: Any) -> Any:
    return numpc.as_array(x).copy().astype(bool)


def c_matrix_to_numpy(x: Any) -> Any:
    """
    Convert a ctypes 2d array (or matrix) into a numpy array for python use

    :param x: thing to convert
    :return: numpy.ndarray
    """
    return numpc.as_array(x).copy()


def string_to_char_p(inobject: Any, inlen: int | None = None) -> Any:
    """
    convert a python string to a char_p

    :param inobject: input string, int for getting null string of length of int
    :param inlen: optional parameter, length of a given string can be specified
    :return:
    """
    if inlen and isinstance(inobject, str):
        return create_string_buffer(inobject.encode(encoding="UTF-8"), inlen)
    if isinstance(inobject, bytes):
        return inobject
    if isinstance(inobject, c_int):
        return string_to_char_p(" " * inobject.value)
    if isinstance(inobject, int):
        return string_to_char_p(" " * inobject)
    if isinstance(inobject, numpy.str_):
        return c_char_p(inobject.encode(encoding="utf-8"))
    return c_char_p(inobject.encode(encoding="UTF-8"))


def list_to_char_array(
    arg: Any, x_len: int | c_int | None = None, y_len: int | c_int | None = None
) -> Array[Array[c_char]]:
    assert is_iterable(arg)
    if not y_len:
        y_len = len(arg)
    if not x_len:
        x_len = max(len(s) for s in arg) + 1
    if isinstance(x_len, c_int):
        x_len = x_len.value
    if isinstance(y_len, c_int):
        y_len = y_len.value
    return ((c_char * x_len) * y_len)(*[string_to_char_p(l, inlen=x_len) for l in arg])


def list_to_char_array_ptr(
    input: Any, x_len: int | c_int | None = None, y_len: int | c_int | None = None
) -> Any:
    return cast(list_to_char_array(input, x_len=x_len, y_len=y_len), c_char_p)


class DoubleArrayType:
    """
    Class type that will handle all double vectors,
    inspiration from python cookbook 3rd edition
    """

    def from_param(self, param: Any) -> Array[c_double]:
        if hasattr(param, "__array_interface__"):
            return self.from_ndarray(param)
        elif isinstance(param, Array):
            return param
        elif isinstance(param, (list, tuple)):
            return self.from_list(param)
        elif isinstance(param, array):
            if param.typecode != "d":
                raise TypeError("must be an array of doubles")
            return self.from_list(param)
        else:
            raise TypeError(f"Can't convert {type(param)}")

    # Cast from lists/tuples
    def from_list(self, param: Sequence[float]) -> Array[c_double]:
        val = ((c_double) * len(param))(*param)
        return val

    # Cast from a numpy array,
    def from_ndarray(self, param: Any) -> Array[c_double]:
        # return param.data_as(POINTER(c_double))
        # the above older method does not work with
        # functions which take vectors of known size
        return type_cast(
            "Array[c_double]",
            numpc.as_ctypes(
                param.astype(numpy.float64, casting="same_kind", copy=False)
            ),
        )


class DoubleMatrixType:
    """
    Class type that will handle all 2d double arrays,
    inspiration from python cookbook 3rd edition
    """

    def from_param(self, param: Any) -> Array[Array[c_double]]:
        if hasattr(param, "__array_interface__"):
            return self.from_ndarray(param)
        elif isinstance(param, Array):
            return param
        elif isinstance(param, (list, tuple)):
            return self.from_list(param)
        else:
            raise TypeError(f"Can't convert {type(param)}")

    # Cast from lists/tuples
    def from_list(self, param: Sequence[Sequence[float]]) -> Array[Array[c_double]]:
        val = ((c_double * len(param[0])) * len(param))(
            *[DoubleArray.from_param(x) for x in param]
        )
        return val

    # Cast from a numpy array
    def from_ndarray(self, param: Any) -> Array[Array[c_double]]:
        return type_cast(
            "Array[Array[c_double]]",
            numpc.as_ctypes(
                param.astype(numpy.float64, casting="same_kind", copy=False)
            ),
        )


class IntArrayType:
    """
    Class type that will handle all int vectors,
    inspiration from python cookbook 3rd edition
    """

    def from_param(self, param: Any) -> Array[c_int]:
        if hasattr(param, "__array_interface__"):
            return self.from_ndarray(param)
        elif isinstance(param, Array):
            return param
        elif isinstance(param, (list, tuple)):
            return self.from_list(param)
        elif isinstance(param, array):
            if param.typecode != "i":
                raise TypeError("must be an array of ints")
            return self.from_list(param)
        else:
            raise TypeError(f"Can't convert {type(param)}")

    # Cast from lists/tuples
    def from_list(self, param: Sequence[int]) -> Array[c_int]:
        val = ((c_int) * len(param))(*param)
        return val

    # Cast from a numpy array
    def from_ndarray(self, param: Any) -> Array[c_int]:
        # cspice always uses a int size half as big as the float, ie int32 if a float64 system default
        return type_cast(
            "Array[c_int]",
            numpc.as_ctypes(param.astype(numpy.int32, casting="same_kind", copy=False)),
        )


class IntMatrixType:
    """
    Class type that will handle all 2d int arrays,
    inspiration from python cookbook 3rd edition
    """

    def from_param(self, param: Any) -> Array[Array[c_int]]:
        if hasattr(param, "__array_interface__"):
            return self.from_ndarray(param)
        elif isinstance(param, Array):
            return param
        elif isinstance(param, (list, tuple)):
            return self.from_list(param)
        else:
            raise TypeError(f"Can't convert {type(param)}")

    # Cast from lists/tuples
    def from_list(self, param: Sequence[Sequence[int]]) -> Array[Array[c_int]]:
        val = ((c_int * len(param[0])) * len(param))(
            *[IntArray.from_param(x) for x in param]
        )
        return val

    # Cast from a numpy array
    def from_ndarray(self, param: Any) -> Array[Array[c_int]]:
        # cspice always uses a int size half as big as the float, ie int32 if a float64 system default
        return type_cast(
            "Array[Array[c_int]]",
            numpc.as_ctypes(param.astype(numpy.int32, casting="same_kind", copy=False)),
        )


DoubleArray = DoubleArrayType()

DoubleMatrix = DoubleMatrixType()

IntArray = IntArrayType()

IntMatrix = IntMatrixType()


class Plane(Structure):
    _normal: Array[c_double]
    _constant: float
    _fields_ = [("_normal", c_double * 3), ("_constant", c_double)]

    @property
    def normal(self) -> Any:
        return c_vector_to_python(self._normal)

    @property
    def constant(self) -> float:
        return self._constant

    def __str__(self) -> str:
        return f"<SpicePlane: normal={', '.join([str(x) for x in self._normal])}; constant={self._constant}>"


class Ellipse(Structure):
    _center: Array[c_double]
    _semi_major: Array[c_double]
    _semi_minor: Array[c_double]
    _fields_ = [
        ("_center", c_double * 3),
        ("_semi_major", c_double * 3),
        ("_semi_minor", c_double * 3),
    ]

    @property
    def center(self) -> Any:
        return c_vector_to_python(self._center)

    @property
    def semi_major(self) -> Any:
        return c_vector_to_python(self._semi_major)

    @property
    def semi_minor(self) -> Any:
        return c_vector_to_python(self._semi_minor)

    def __str__(self) -> str:
        return f"<SpiceEllipse: center = {self.center} semi_major = {self.semi_major}, semi_minor = {self.semi_minor}>"


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

    def __init__(self) -> None:
        pass


class SpiceDSKDescr(Structure):
    _surfce: int
    _center: int
    _dclass: int
    _dtype: int
    _frmcde: int
    _corsys: int
    _corpar: Array[c_double]
    _co1min: float
    _co1max: float
    _co2min: float
    _co2max: float
    _co3min: float
    _co3max: float
    _start: float
    _stop: float
    _fields_ = [
        ("_surfce", c_int),
        ("_center", c_int),
        ("_dclass", c_int),
        ("_dtype", c_int),
        ("_frmcde", c_int),
        ("_corsys", c_int),
        ("_corpar", c_double * 10),
        ("_co1min", c_double),
        ("_co1max", c_double),
        ("_co2min", c_double),
        ("_co2max", c_double),
        ("_co3min", c_double),
        ("_co3max", c_double),
        ("_start", c_double),
        ("_stop", c_double),
    ]

    @property
    def surfce(self) -> int:
        return self._surfce

    @property
    def center(self) -> int:
        return self._center

    @property
    def dclass(self) -> int:
        return self._dclass

    @property
    def dtype(self) -> int:
        return self._dtype

    @property
    def frmcde(self) -> int:
        return self._frmcde

    @property
    def corsys(self) -> int:
        return self._corsys

    @property
    def corpar(self) -> Any:
        return c_vector_to_python(self._corpar)

    @property
    def co1min(self) -> float:
        return self._co1min

    @property
    def co1max(self) -> float:
        return self._co1max

    @property
    def co2min(self) -> float:
        return self._co2min

    @property
    def co2max(self) -> float:
        return self._co2max

    @property
    def co3min(self) -> float:
        return self._co3min

    @property
    def co3max(self) -> float:
        return self._co3max

    @property
    def start(self) -> float:
        return self._start

    @property
    def stop(self) -> float:
        return self._stop


class SpiceDLADescr(Structure):
    _bwdptr: int
    _fwdptr: int
    _ibase: int
    _isize: int
    _dbase: int
    _dsize: int
    _cbase: int
    _csize: int
    _fields_ = [
        ("_bwdptr", c_int),
        ("_fwdptr", c_int),
        ("_ibase", c_int),
        ("_isize", c_int),
        ("_dbase", c_int),
        ("_dsize", c_int),
        ("_cbase", c_int),
        ("_csize", c_int),
    ]

    @property
    def bwdptr(self) -> int:
        return self._bwdptr

    @property
    def fwdptr(self) -> int:
        return self._fwdptr

    @property
    def ibase(self) -> int:
        return self._ibase

    @property
    def isize(self) -> int:
        return self._isize

    @property
    def dbase(self) -> int:
        return self._dbase

    @property
    def dsize(self) -> int:
        return self._dsize

    @property
    def cbase(self) -> int:
        return self._cbase

    @property
    def csize(self) -> int:
        return self._csize


class SpiceEKDataType(c_int):
    _SPICE_CHR = c_int(0)
    _SPICE_DP = c_int(1)
    _SPICE_INT = c_int(2)
    _SPICE_TIME = c_int(3)
    _SPICE_BOOL = c_int(4)

    _fields_ = [
        ("SPICE_CHR", _SPICE_CHR),
        ("SPICE_DP", _SPICE_DP),
        ("SPICE_INT", _SPICE_INT),
        ("SPICE_TIME", _SPICE_TIME),
        ("SPICE_BOOL", _SPICE_BOOL),
    ]

    SPICE_CHR = _SPICE_CHR.value
    SPICE_DP = _SPICE_DP.value
    SPICE_INT = _SPICE_INT.value
    SPICE_TIME = _SPICE_TIME.value
    SPICE_BOOL = _SPICE_BOOL.value


def empty_spice_ek_data_type_vector(n: int | c_int) -> Array[SpiceEKDataType]:
    if isinstance(n, c_int):
        n = n.value
    assert isinstance(n, int)
    return (SpiceEKDataType * n)()


class SpiceEKExprClass(c_int):
    _SPICE_EK_EXP_COL = c_int(0)
    _SPICE_EK_EXP_FUNC = c_int(1)
    _SPICE_EK_EXP_EXPR = c_int(2)

    _fields_ = [
        ("SPICE_EK_EXP_COL", _SPICE_EK_EXP_COL),
        ("SPICE_EK_EXP_FUNC", _SPICE_EK_EXP_FUNC),
        ("SPICE_EK_EXP_EXPR", _SPICE_EK_EXP_EXPR),
    ]

    SPICE_EK_EXP_COL = _SPICE_EK_EXP_COL.value
    SPICE_EK_EXP_FUNC = _SPICE_EK_EXP_FUNC.value
    SPICE_EK_EXP_EXPR = _SPICE_EK_EXP_EXPR.value


class SpiceSPK18Subtype(c_int):
    _S18TP0 = c_int(0)
    _S18TP1 = c_int(1)
    S18TP0 = _S18TP0.value
    S18TP1 = _S18TP1.value
    _fields_ = [("S18TP0", _S18TP0), ("S18TP1", _S18TP1)]


def empty_spice_ek_expr_class_vector(n: int | c_int) -> Array[SpiceEKExprClass]:
    if isinstance(n, c_int):
        n = n.value
    assert isinstance(n, int)
    return (SpiceEKExprClass * n)()


class SpiceEKAttDsc(Structure):
    _cclass: int
    _dtype: SpiceEKDataType
    _strlen: int
    _size: int
    _indexd: int
    _nullok: int
    _fields_ = [
        ("_cclass", c_int),
        ("_dtype", SpiceEKDataType),
        ("_strlen", c_int),
        ("_size", c_int),
        ("_indexd", c_int),
        ("_nullok", c_int),
    ]

    @property
    def cclass(self) -> int:
        return self._cclass

    @property
    def dtype(self) -> int:
        return self._dtype.value

    @property
    def strlen(self) -> int:
        return self._strlen

    @property
    def size(self) -> int:
        return self._size

    @property
    def indexd(self) -> bool:
        return bool(self._indexd)

    @property
    def nullok(self) -> bool:
        return bool(self._nullok)

    def __str__(self) -> str:
        return (
            f"<SpiceEKAttDsc cclass = {self.cclass}, dtype = {self.dtype}, strlen = {self.strlen}, "
            f"size = {self.size}, indexd = {self.indexd}, nullok = {self.nullok} >"
        )


class SpiceEKSegSum(Structure):
    _tabnam: Array[c_char]
    _nrows: int
    _ncols: int
    _cnames: Array[Array[c_char]]
    _cdescrs: Array[SpiceEKAttDsc]
    _fields_ = [
        ("_tabnam", c_char * 65),
        ("_nrows", c_int),
        ("_ncols", c_int),
        ("_cnames", (c_char * 100) * 33),
        ("_cdescrs", SpiceEKAttDsc * 100),
    ]

    @property
    def tabnam(self) -> str:
        return to_python_string(self._tabnam)

    @property
    def nrows(self) -> int:
        return self._nrows

    @property
    def ncols(self) -> int:
        return self._ncols

    @property
    def cnames(self) -> Any:
        return c_vector_to_python(self._cnames)[0 : self.ncols]

    @property
    def cdescrs(self) -> Any:
        return self._cdescrs[0 : self.ncols]

    def __str__(self) -> str:
        return (
            f"<SpiceEKSegSum tabnam = {self.tabnam}, nrows = {self.nrows}, ncols = {self.ncols},"
            f" cnames = {self.cnames}, cdescrs = {self.cdescrs} >"
        )


# SpiceCell implementation below is inpart from github.com/DaRasch/spiceminer/
# and modified as needed for this author, maybe we should work together?

# helper classes/functions
BITSIZE = {
    "char": sizeof(c_char),
    "int": sizeof(c_int),
    "double": sizeof(c_double),
    "bool": sizeof(c_int),
    "time": sizeof(c_int),
}


def _char_getter(data_p: int, index: int, length: int) -> str:
    return to_python_string(
        (c_char * length).from_address(data_p + index * length * BITSIZE["char"])
    )


def _double_getter(data_p: int, index: int, length: int) -> float:
    return c_double.from_address(data_p + index * BITSIZE["double"]).value


def _int_getter(data_p: int, index: int, length: int) -> int:
    return c_int.from_address(data_p + index * BITSIZE["int"]).value


class SpiceCell(Structure):
    # Most written by DaRasch, see included MIT license at file header
    DATATYPES_ENUM = {"char": 0, "double": 1, "int": 2, "time": 3, "bool": 4}
    DATATYPES_GET: List[Callable[[int, int, int], Any]] = [
        _char_getter,
        _double_getter,
        _int_getter,
        _int_getter,
        _int_getter,
    ]
    baseSize = 6
    minCharLen = 6
    CTRLBLOCK = 6
    dtype: Optional[int]
    length: Optional[int]
    size: Optional[int]
    card: Optional[int]
    isSet: Optional[int]
    adjust: int
    init: int
    _fields_ = [
        ("dtype", c_int),
        ("length", c_int),
        ("size", c_int),
        ("card", c_int),
        ("isSet", c_int),
        ("adjust", c_int),
        ("init", c_int),
        ("base", c_void_p),
        ("data", c_void_p),
    ]

    def __init__(
        self,
        dtype: Optional[int] = None,
        length: Optional[int] = None,
        size: Optional[int] = None,
        card: Optional[int] = None,
        isSet: Optional[int] = None,
        base: Any = None,
        data: Any = None,
    ) -> None:
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

    def __str__(self) -> str:
        return (
            f"<SpiceCell dtype = {self.dtype}, length = {self.length}, size = {self.size}, card = {self.card},"
            f" is_set = {self.isSet}, adjust = {self.adjust}, init = {self.init}, base = {self.base}, data = {self.data}>"
        )

    def is_int(self) -> bool:
        return self.dtype == 2

    def is_double(self) -> bool:
        return self.dtype == 1

    def is_char(self) -> bool:
        return self.dtype == 0

    def is_time(self) -> bool:
        return self.dtype == 3

    def is_bool(self) -> bool:
        return self.dtype == 4

    def is_set(self) -> bool:
        return self.isSet == 1

    @classmethod
    def character(cls, size: int, length: int) -> "SpiceCell":
        base = (c_char * ((cls.CTRLBLOCK + size) * length))()
        data = (c_char * (size * length)).from_buffer(
            base, cls.CTRLBLOCK * BITSIZE["char"] * length
        )
        instance = cls(
            cls.DATATYPES_ENUM["char"],
            length,
            size,
            0,
            1,
            cast(base, c_void_p),
            cast(data, c_void_p),
        )
        return instance

    @classmethod
    def integer(cls, size: int) -> "SpiceCell":
        base = (c_int * (cls.CTRLBLOCK + size))()
        data = (c_int * size).from_buffer(base, cls.CTRLBLOCK * BITSIZE["int"])
        instance = cls(
            cls.DATATYPES_ENUM["int"],
            0,
            size,
            0,
            1,
            cast(base, c_void_p),
            cast(data, c_void_p),
        )
        return instance

    @classmethod
    def double(cls, size: int) -> "SpiceCell":
        base = (c_double * (cls.CTRLBLOCK + size))()
        data = (c_double * size).from_buffer(base, cls.CTRLBLOCK * BITSIZE["double"])
        instance = cls(
            cls.DATATYPES_ENUM["double"],
            0,
            size,
            0,
            1,
            cast(base, c_void_p),
            cast(data, c_void_p),
        )
        return instance

    @classmethod
    def bool(cls, size: int) -> "SpiceCell":
        base = (c_int * (cls.CTRLBLOCK + size))()
        data = (c_int * size).from_buffer(base, cls.CTRLBLOCK * BITSIZE["bool"])
        instance = cls(
            cls.DATATYPES_ENUM["bool"],
            0,
            size,
            0,
            1,
            cast(base, c_void_p),
            cast(data, c_void_p),
        )
        return instance

    @classmethod
    def time(cls, size: int) -> "SpiceCell":
        base = (c_int * (cls.CTRLBLOCK + size))()
        data = (c_int * size).from_buffer(base, cls.CTRLBLOCK * BITSIZE["time"])
        instance = cls(
            cls.DATATYPES_ENUM["time"],
            0,
            size,
            0,
            1,
            cast(base, c_void_p),
            cast(data, c_void_p),
        )
        return instance

    def __len__(self) -> int:
        assert self.card is not None
        return self.card

    def __iter__(self) -> Iterator[Any]:
        assert self.dtype is not None
        assert self.length is not None
        assert self.card is not None
        getter = SpiceCell.DATATYPES_GET[self.dtype]
        length, card, data = self.length, self.card, self.data
        for i in range(card):
            yield getter(data, i, length)

    def __contains__(self, key: Any) -> builtins.bool:
        return key in self.__iter__()

    def __getitem__(self, key: Union[int, slice]) -> Any:
        assert self.dtype is not None
        assert self.card is not None
        assert self.length is not None
        getter = SpiceCell.DATATYPES_GET[self.dtype]
        if isinstance(key, slice):
            # TODO Typechecking
            if self.card == 0:
                return []
            else:
                start, stop, step = key.indices(self.card)
                return [
                    getter(self.data, i, self.length) for i in range(start, stop, step)
                ]
        elif key in range(-self.card, self.card):
            index = key if key >= 0 else self.card - abs(key)
            return getter(self.data, index, self.length)
        elif not isinstance(key, int):
            raise TypeError(
                "SpiceCell indices must be integers, not {}".format(type(key))
            )
        else:
            raise IndexError("SpiceCell index out of range")

    def reset(self) -> None:
        self.card = 0
        self.init = 0

    def __eq__(self, other: Any) -> builtins.bool:
        """
        element wise equality, other can be a list or cell
        I think sets should not equal a non set even if
        elements are equal... might be a bad idea
        :param other:
        :return:
        """
        if not hasattr(other, "__iter__"):
            return False
        if len(self) != len(other):
            return False
        if isinstance(other, SpiceCell):
            if other.dtype != self.dtype:
                return False
            if other.isSet != self.isSet:
                return False
        for x, y in zip(self, other):
            if x != y:
                return False
        return True


if TYPE_CHECKING:
    from ctypes import _Pointer
    from typing import TypeAlias

    # POINTER() products are opaque to static checkers; typeshed's spelling
    # for the same runtime class is the generic _Pointer[SpiceCell].
    SpiceCellPointer: TypeAlias = _Pointer[SpiceCell]
else:
    SpiceCellPointer = POINTER(SpiceCell)


def SPICEDOUBLE_CELL(size: int) -> SpiceCell:
    """
    Returns a Double Spice Cell with a given size
    :param size: number of elements
    :return: empty Spice Cell
    """
    return SpiceCell.double(size)


def SPICEINT_CELL(size: int) -> SpiceCell:
    """
    Returns a Int Spice Cell with a given size
    :param size: number of elements
    :return: empty Spice Cell
    """
    return SpiceCell.integer(size)


def SPICECHAR_CELL(size: int, length: int) -> SpiceCell:
    """
    Returns a Char Spice Cell with a given size
    :param size: number of elements
    :param length: width of elements
    :return: empty Spice Cell
    """
    return SpiceCell.character(size, length)


def SPICEBOOL_CELL(size: int) -> SpiceCell:
    """
    Returns a Bool Spice Cell with a given size
    :param size: number of elements
    :return: empty Spice Cell
    """
    return SpiceCell.bool(size)


def SPICETIME_CELL(size: int) -> SpiceCell:
    """
    Returns a Time Spice Cell with a given size
    :param size: number of elements
    :return: empty Spice Cell
    """
    return SpiceCell.time(size)


# Spice Cell classes


class Cell_Time(SpiceCell):
    def __init__(self, size: int) -> None:
        """
        Init a Time Spice Cell with a given size and length
        :param size: number of elements
        """
        base = (c_int * (6 + size))()
        data = (c_int * size).from_buffer(base, 6 * BITSIZE["time"])
        super(Cell_Time, self).__init__(
            3, 0, size, 0, 1, cast(base, c_void_p), cast(data, c_void_p)
        )


class Cell_Bool(SpiceCell):
    def __init__(self, size: int) -> None:
        """
        Init a Bool Spice Cell with a given size and length
        :param size: number of elements
        """
        base = (c_int * (6 + size))()
        data = (c_int * size).from_buffer(base, 6 * BITSIZE["bool"])
        super(Cell_Bool, self).__init__(
            4, 0, size, 0, 1, cast(base, c_void_p), cast(data, c_void_p)
        )


class Cell_Int(SpiceCell):
    def __init__(self, size: int) -> None:
        """
        Init a Int Spice Cell with a given size and length
        :param size: number of elements
        """
        base = (c_int * (6 + size))()
        data = (c_int * size).from_buffer(base, 6 * BITSIZE["int"])
        super(Cell_Int, self).__init__(
            2, 0, size, 0, 1, cast(base, c_void_p), cast(data, c_void_p)
        )


class Cell_Double(SpiceCell):
    def __init__(self, size: int) -> None:
        """
        Init a Double Spice Cell with a given size and length
        :param size: number of elements
        """
        base = (c_double * (6 + size))()
        data = (c_double * size).from_buffer(base, 6 * BITSIZE["double"])
        super(Cell_Double, self).__init__(
            1, 0, size, 0, 1, cast(base, c_void_p), cast(data, c_void_p)
        )


class Cell_Char(SpiceCell):
    def __init__(self, size: int, length: int) -> None:
        """
        Init a Char Spice Cell with a given size and length
        :param size: number of elements
        :param length: width of elements
        """
        base = (c_char * ((6 + size) * length))()
        data = (c_char * (size * length)).from_buffer(
            base, 6 * BITSIZE["char"] * length
        )
        super(Cell_Char, self).__init__(
            0, length, size, 0, 1, cast(base, c_void_p), cast(data, c_void_p)
        )
