"""
The MIT License (MIT)

Copyright (c) [2015-2019] [Andrew Annex]

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
from .support_types import SpiceCell

UDFUNS = CFUNCTYPE(None, c_double, POINTER(c_double))
UDFUNB = CFUNCTYPE(None, UDFUNS, c_double, POINTER(c_int))
UDSTEP = CFUNCTYPE(None, c_double, POINTER(c_double))
UDREFN = CFUNCTYPE(None, c_double, c_double, c_int, c_int, POINTER(c_double))
UDREPI = CFUNCTYPE(None, POINTER(SpiceCell), c_char_p, c_char_p)
UDREPU = CFUNCTYPE(None, c_double, c_double, c_double)
UDREPF = CFUNCTYPE(None)
UDBAIL = CFUNCTYPE(c_int)


def SpiceUDFUNS(f):
    """
    Decorator for wrapping python functions in spice udfuns callback type
    :param f: function that has one argument of type float, and returns a float
    :type f: builtins.function
    :return: wrapped udfunc function
    :rtype: builtins.function
    """

    @functools.wraps(f)
    def wrapping_udfuns(x, value):
        result = f(x)
        value[0] = c_double(result)

    return UDFUNS(wrapping_udfuns)


def SpiceUDFUNB(f):
    """
    Decorator for wrapping python functions in spice udfunb callback type
    :param f: function to be wrapped
    :type f: builtins.function
    :return: wrapped udfunb function
    :rtype: builtins.function
    """

    @functools.wraps(f)
    def wrapping_udfunb(udf, et, xbool):
        result = f(udf, et)  # the function takes a udffunc as a argument
        xbool[0] = c_int(result)  # https://github.com/numpy/numpy/issues/14397

    return UDFUNB(wrapping_udfunb)


def SpiceUDSTEP(f):
    """
    Decorator for wrapping python functions in spice udstep callback type
    :param f: function to be wrapped
    :type f: builtins.function
    :return: wrapped udstep function
    :rtype: builtins.function
    """

    @functools.wraps(f)
    def wrapping_udstep(x, value):
        result = f(x)
        value[0] = c_double(result)

    return UDSTEP(wrapping_udstep)


def SpiceUDREFN(f):
    """
    Decorator for wrapping python functions in spice udrefn callback type
    :param f: function to be wrapped
    :type f: builtins.function
    :return: wrapped udrefn function
    :rtype: builtins.function
    """

    @functools.wraps(f)
    def wrapping_udrefn(t1, t2, s1, s2, t):
        result = f(t1, t2, s1, s2)
        t[0] = c_double(result)

    return UDREFN(wrapping_udrefn)


def SpiceUDREPI(f):
    """
    Decorator for wrapping python functions in spice udfrepi callback type
    :param f: function to be wrapped
    :type f: builtins.function
    :return: wrapped udrepi function
    :rtype: builtins.function
    """

    @functools.wraps(f)
    def wrapping_udrepi(cnfine, srcpre, srcsurf):
        f(cnfine, srcpre, srcsurf)

    return UDREPI(wrapping_udrepi)


def SpiceUDREPU(f):
    """
    Decorator for wrapping python functions in spice udrepu callback type
    :param f: function to be wrapped
    :type f: builtins.function
    :return: wrapped udrepu function
    :rtype: builtins.function
    """

    @functools.wraps(f)
    def wrapping_udrepu(beg, end, et):
        f(beg, end, et)

    return UDREPU(wrapping_udrepu)


def SpiceUDREPF(f):
    """
    Decorator for wrapping python functions in spice udrepf callback type
    :param f: function to be wrapped
    :type f: builtins.function
    :return: wrapped udrepf function
    :rtype: builtins.function
    """

    @functools.wraps(f)
    def wrapping_udrepf():
        f()

    return UDREPF(wrapping_udrepf)


def SpiceUDBAIL(f):
    """
    Decorator for wrapping python functions in spice udbail callback type
    :param f: function to be wrapped
    :type f: builtins.function
    :return: wrapped udbail function
    :rtype: builtins.function
    """

    @functools.wraps(f)
    def wrapping_udbail():
        result = f()
        return int(result)

    return UDBAIL(wrapping_udbail)


def CallUDFUNS(f, x):
    """
    We are given a UDF CFUNCTYPE and want to call it in python

    :param f: SpiceUDFUNS
    :type f: CFUNCTYPE
    :param x: some scalar
    :type x: float
    :return: value
    :rtype: float
    """
    value = c_double()
    f(x, byref(value))
    return value.value
