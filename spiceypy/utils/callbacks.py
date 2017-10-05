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
"""

import functools
from ctypes import c_bool, c_double, POINTER, CFUNCTYPE, byref

UDFUNS = CFUNCTYPE(None, c_double, POINTER(c_double))
UDFUNB = CFUNCTYPE(None, UDFUNS, c_double, POINTER(c_bool))

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
    :param f:
    :type f: builtins.function
    :return:
    """

    @functools.wraps(f)
    def wrapping_udfunb(udf, et, xbool):
        result = f(udf, et) # the function takes a udffunc as a argument
        xbool[0] = c_bool(result)

    return UDFUNB(wrapping_udfunb)

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