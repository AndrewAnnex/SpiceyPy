import ctypes
import functools



UDFUNC = ctypes.CFUNCTYPE(None, ctypes.c_double, ctypes.POINTER(ctypes.c_double))


def SpiceUDF(f):
    """
    Decorator for wrapping python functions in spice udfunc callback type
    :param f: function that has one argument of type float, and returns a float
    :type f: builtins.function
    :return: wrapped udfunc function
    :rtype: builtins.function
    """
    @functools.wraps(f)
    def wrapping_udfunc(x, value):
        result = f(x)
        value[0] = ctypes.c_double(result)
        pass

    return UDFUNC(wrapping_udfunc)

