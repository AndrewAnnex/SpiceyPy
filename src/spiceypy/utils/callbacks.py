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
"""

import functools
from ctypes import c_int, c_double, c_char_p, POINTER, CFUNCTYPE, byref
from .support_types import SpiceCell, SpiceCellPointer, to_python_string
from typing import Callable, Union

UDFUNC = CFUNCTYPE(None, c_double, POINTER(c_double))
UDFUNS = CFUNCTYPE(None, c_double, POINTER(c_double))
UDFUNB = CFUNCTYPE(None, UDFUNS, c_double, POINTER(c_int))
UDSTEP = CFUNCTYPE(None, c_double, POINTER(c_double))
UDREFN = CFUNCTYPE(None, c_double, c_double, c_int, c_int, POINTER(c_double))
UDREPI = CFUNCTYPE(None, POINTER(SpiceCell), c_char_p, c_char_p)
UDREPU = CFUNCTYPE(None, c_double, c_double, c_double)
UDREPF = CFUNCTYPE(None)
UDBAIL = CFUNCTYPE(c_int)


def SpiceUDFUNC(f: Callable[[float], float]) -> UDFUNC:
    """
    Decorator for wrapping python functions in spice udfunc callback type

    :param f: function that has one argument of type float, and returns a float
    :return: wrapped udfunc function
    """

    @functools.wraps(f)
    def wrapping_udfunc(x: float, value: POINTER(c_double)) -> None:
        result = f(x)
        value[0] = c_double(result)

    return UDFUNC(wrapping_udfunc)


def SpiceUDFUNS(f: Callable[[float], float]) -> UDFUNS:
    """
    Decorator for wrapping python functions in spice udfuns callback type

    :param f: function that has one argument of type float, and returns a float
    :return: wrapped udfunc function
    """

    @functools.wraps(f)
    def wrapping_udfuns(x: float, value: POINTER(c_double)) -> None:
        result = f(x)
        value[0] = c_double(result)

    return UDFUNS(wrapping_udfuns)


def SpiceUDFUNB(f: Callable[[UDFUNS, float], int]) -> UDFUNB:
    """
    Decorator for wrapping python functions in spice udfunb callback type

    :param f: function to be wrapped
    :return: wrapped udfunb function
    """

    @functools.wraps(f)
    def wrapping_udfunb(udf: UDFUNS, et: float, xbool: POINTER(c_int)) -> None:
        # casting to bool fixes https://github.com/numpy/numpy/issues/14397
        result = bool(f(udf, et))
        xbool[0] = c_int(result)

    return UDFUNB(wrapping_udfunb)


def SpiceUDSTEP(f: Callable[[float], float]) -> UDSTEP:
    """
    Decorator for wrapping python functions in spice udstep callback type

    :param f: function to be wrapped
    :return: wrapped udstep function
    """

    @functools.wraps(f)
    def wrapping_udstep(x: float, value: POINTER(c_double)) -> None:
        result = f(x)
        value[0] = c_double(result)

    return UDSTEP(wrapping_udstep)


def SpiceUDREFN(
    f: Callable[[float, float, Union[bool, int], Union[bool, int]], float]
) -> UDREFN:
    """
    Decorator for wrapping python functions in spice udrefn callback type

    :param f: function to be wrapped
    :return: wrapped udrefn function
    """

    @functools.wraps(f)
    def wrapping_udrefn(
        t1: float,
        t2: float,
        s1: Union[bool, int],
        s2: Union[bool, int],
        t: POINTER(c_double),
    ) -> None:
        result = f(t1, t2, s1, s2)
        t[0] = c_double(result)

    return UDREFN(wrapping_udrefn)


def SpiceUDREPI(
    f: Callable[[Union[SpiceCell, SpiceCellPointer], str, str], None]
) -> UDREPI:
    """
    Decorator for wrapping python functions in spice udfrepi callback type

    :param f: function to be wrapped
    :return: wrapped udrepi function
    """

    @functools.wraps(f)
    def wrapping_udrepi(
        cnfine: Union[SpiceCell, SpiceCellPointer], srcpre: bytes, srcsurf: bytes
    ) -> None:
        f(cnfine, to_python_string(srcpre), to_python_string(srcsurf))

    return UDREPI(wrapping_udrepi)


def SpiceUDREPU(f: Callable[[float, float, float], None]) -> UDREPU:
    """
    Decorator for wrapping python functions in spice udrepu callback type

    :param f: function to be wrapped
    :return: wrapped udrepu function
    """

    @functools.wraps(f)
    def wrapping_udrepu(beg: float, end: float, et: float) -> None:
        f(beg, end, et)

    return UDREPU(wrapping_udrepu)


def SpiceUDREPF(f: Callable) -> UDREPF:
    """
    Decorator for wrapping python functions in spice udrepf callback type

    :param f: function to be wrapped
    :return: wrapped udrepf function
    """

    @functools.wraps(f)
    def wrapping_udrepf() -> None:
        f()

    return UDREPF(wrapping_udrepf)


def SpiceUDBAIL(f: Callable[[], Union[bool, int]]) -> UDBAIL:
    """
    Decorator for wrapping python functions in spice udbail callback type

    :param f: function to be wrapped
    :return: wrapped udbail function
    """

    @functools.wraps(f)
    def wrapping_udbail() -> int:
        result = f()
        return int(result)

    return UDBAIL(wrapping_udbail)


def CallUDFUNS(f: UDFUNS, x: float) -> float:
    """
    We are given a UDF CFUNCTYPE and want to call it in python

    :param f: SpiceUDFUNS
    :param x: some scalar
    :return: value
    """
    value = c_double()
    f(x, byref(value))
    return value.value
