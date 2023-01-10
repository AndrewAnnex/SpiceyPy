# cython: language_level = 3
"""
main cython wrapper code

defs are visible to python
cdef's are not visible to python and are pure c, use for inner loops
cpdefs are both, really only useful for recursion

"""

# okay for some reason making a pxd file causes cython to fail
cdef extern from "SpiceUsr.h" nogil:
    ctypedef int SpiceBoolean
    ctypedef char SpiceChar
    ctypedef long SpiceInt
    ctypedef double SpiceDouble
    ctypedef const int ConstSpiceBool
    ctypedef const char ConstSpiceChar
    ctypedef const long ConstSpiceInt
    ctypedef const double ConstSpiceDouble
    cdef double b1900_c()

cpdef b1900():
    return b1900_c()
