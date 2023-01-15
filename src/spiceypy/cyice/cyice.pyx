# cython: language_level = 3
# cython: embedsignature = True
# cython: c_string_type = bytes
# cython: c_string_encoding = utf-8
"""
main cython wrapper code

defs are visible to python
cdef's are not visible to python and are pure c, use for inner loops
cpdefs are both, really only useful for recursion

"""
from libc.stdlib cimport malloc, free
from cython cimport boundscheck, wraparound
import numpy as np
cimport numpy as np
np.import_array()

cdef extern from "Python.h":
    object PyString_FromStringAndSize(char *, Py_ssize_t)
    char *PyString_AsString(object)


# okay for some reason making a pxd file causes cython to fail
# todo maybe okay to just use "*" for header file
# grab externs from SpiceZpr.h
cdef extern from "SpiceUsr.h" nogil:
    ctypedef bint SpiceBoolean
    ctypedef char SpiceChar
    ctypedef long SpiceInt
    ctypedef double SpiceDouble
    ctypedef const int ConstSpiceBool
    ctypedef const char ConstSpiceChar
    ctypedef const long ConstSpiceInt
    ctypedef const double ConstSpiceDouble

    # Cells
    cdef enum SpiceCellDataType:
        char = 0,
        double = 1,
        int = 2,
        time = 3,
        bool = 4

    cdef struct _SpiceCell:
        SpiceCellDataType dtype
        SpiceInt           length
        SpiceInt           size
        SpiceInt           card
        SpiceBoolean       isSet
        SpiceBoolean       adjust
        SpiceBoolean       init
        void * base
        void * data

    ctypedef _SpiceCell SpiceCell
    ctypedef const SpiceCell ConstSpiceCell

    # start of function defs
    cdef double b1900_c()

    cdef double b1950_c()

    #C 

    #F 
    cdef void furnsh_c(ConstSpiceChar * file)

    #S
    cdef void spkez_c(SpiceInt            target,
                      SpiceDouble         epoch,
                      ConstSpiceChar * frame,
                      ConstSpiceChar * abcorr,
                      SpiceInt            observer,
                      SpiceDouble         state[6],
                      SpiceDouble * lt)

    cdef void spkezp_c(SpiceInt            targ,
                        SpiceDouble         et,
                        ConstSpiceChar * ref,
                        ConstSpiceChar * abcorr,
                        SpiceInt            obs,
                        SpiceDouble         ptarg[3],
                        SpiceDouble * lt)

    cdef void spkezr_c(ConstSpiceChar * target,
                        SpiceDouble      epoch,
                        ConstSpiceChar * frame,
                        ConstSpiceChar * abcorr,
                        ConstSpiceChar * observer,
                        SpiceDouble state[6],
                        SpiceDouble * lt)


cpdef double b1900() nogil:
    return b1900_c()

cpdef double b1950() nogil:
    return b1950_c()

cpdef furnsh(str file):
    furnsh_c(file)

cpdef spkezr_vectorized(str target, double[:] epoch, str frame, str abcorr, str observer):
    # initialize c variables
    cdef double[6] state = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    cdef double lt = 0.0
    cdef int i,j, N
    # get the number of epochs defining the size of everything else
    N = epoch.shape[0]
    # convert the strings to pointers once
    py_target   = target.encode('utf-8')
    py_frame    = frame.encode('utf-8')
    py_abcorr   = abcorr.encode('utf-8')
    py_observer = observer.encode('utf-8')
    cdef const char* _target   = py_target
    cdef const char* _frame    = py_frame
    cdef const char* _abcorr   = py_abcorr
    cdef const char* _observer = py_observer
    # initialize output arrays
    cdef double[:,:] states = np.zeros((N,6), dtype=np.double)
    cdef double[:] lts = np.zeros(N, dtype=np.double)
    # main loop
    with nogil, boundscheck(False), wraparound(False):
        for i in range(N):
            spkezr_c(_target, epoch[i], _frame, _abcorr, _observer, state, &lt)
            for j in range(6):
                states[i][j] = state[j]
            lts[i] = lt
    # return results
    return np.asarray(states), np.asarray(lts)
    