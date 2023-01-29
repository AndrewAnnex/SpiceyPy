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
from libc.stdlib cimport malloc, calloc, free
from libc.string cimport memcpy, strlen
from libc.stdio cimport printf
from cython cimport boundscheck, wraparound
import numpy as np
cimport numpy as np
np.import_array()

DEF TIMELEN = 64

ctypedef np.double_t DOUBLE_t

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
    
    #E
    cdef void et2utc_c(SpiceDouble         et,
                       ConstSpiceChar * format,
                       SpiceInt            prec,
                       SpiceInt            lenout,
                       SpiceChar * utcstr)

    #F 
    cdef void furnsh_c(ConstSpiceChar * file)

    #S
    cdef void spkezr_c(ConstSpiceChar * target,
                       SpiceDouble      epoch,
                       ConstSpiceChar * frame,
                       ConstSpiceChar * abcorr,
                       ConstSpiceChar * observer,
                       SpiceDouble state[6],
                       SpiceDouble * lt)

    cdef void spkpos_c(ConstSpiceChar * targ,
                       SpiceDouble         et,
                       ConstSpiceChar * ref,
                       ConstSpiceChar * abcorr,
                       ConstSpiceChar * obs,
                       SpiceDouble         ptarg[3],
                       SpiceDouble * lt)

    cdef void str2et_c(ConstSpiceChar * date,
                       SpiceDouble * et);

cdef unicode tounicode(char* s):
    return s.decode('utf8', 'strict')

cdef unicode tounicode_with_length(
        char* s, size_t length):
    return s[:length].decode('utf8', 'strict')

cdef to_char_pointer(s):
    if isinstance(s, unicode):
        s = (<unicode>s).encode('utf8')
    return s

cpdef double b1900() nogil:
    return b1900_c()

cpdef double b1950() nogil:
    return b1950_c()

cpdef et2utc_v(double[:] ets, str format_str, int prec):
    cdef int i, n
    n = ets.shape[0]
    # convert the strings to pointers once
    py_format_str = format_str.encode('utf-8')
    cdef const char* _format_str = py_format_str
    # create temporary char pointer 
    # todo use macro/contant for buffer size here?
    cdef char* _utcstr = <char *> malloc((TIMELEN+1) * sizeof(char))
    # initialize output arrays TODO: using a unicode numpy array?
    cdef list results = [None] * n
    # main loop
    with boundscheck(False), wraparound(False):
        for i in range(n):
            et2utc_c(ets[i], _format_str, prec, TIMELEN, _utcstr)
            # todo this will call strlen so it would be slow, would be best to 
            #  compute length in bytes ahead of time given format and prec
            results[i] = <unicode> _utcstr
    # free temporary char pointer
    free(_utcstr)
    # return array
    return results
    

cpdef furnsh(str file):
    furnsh_c(file)

cpdef spkezr_v(str target, double[:] epoch, str frame, str abcorr, str observer):
    # initialize c variables
    cdef double[6] state = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    cdef double lt = 0.0
    cdef int i, n
    # get the number of epochs defining the size of everything else
    n = epoch.shape[0]
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
    cdef double[:,:] states = np.zeros((n,6), dtype=np.double)
    cdef double[:] lts = np.zeros(n, dtype=np.double)
    # main loop
    with nogil, boundscheck(False), wraparound(False):
        for i in range(n):
            spkezr_c(_target, epoch[i], _frame, _abcorr, _observer, state, &lt)
            states[i][0] = state[0]
            states[i][1] = state[1]
            states[i][2] = state[2]
            states[i][3] = state[3]
            states[i][4] = state[4]
            states[i][5] = state[5]
            lts[i] = lt
    # return results
    return np.asarray(states), np.asarray(lts)
    
cpdef spkpos_v(str targ, double[:] ets, str ref, str abcorr, str obs):
    # initialize c variables
    cdef double[3] ptarg = (0.0, 0.0, 0.0)
    cdef double lt = 0.0
    cdef int i,j, n
    # get the number of epochs defining the size of everything else
    n = ets.shape[0]
    # convert the strings to pointers once
    py_targ   = targ.encode('utf-8')
    py_ref    = ref.encode('utf-8')
    py_abcorr = abcorr.encode('utf-8')
    py_obs    = obs.encode('utf-8')
    cdef const char* _targ   = py_targ
    cdef const char* _ref    = py_ref
    cdef const char* _abcorr = py_abcorr
    cdef const char* _obs    = py_obs
    # initialize output arrays
    cdef double[:,:] ptargs = np.zeros((n,3), dtype=np.double)
    cdef double[:] lts = np.zeros(n, dtype=np.double)
    # main loop
    with nogil, boundscheck(False), wraparound(False):
        for i in range(n):
            spkpos_c(_targ, ets[i], _ref, _abcorr, _obs, ptarg, &lt)
            ptargs[i][0] = ptarg[0]
            ptargs[i][1] = ptarg[1]
            ptargs[i][2] = ptarg[2]
            lts[i] = lt
    # return results
    return np.asarray(ptargs), np.asarray(lts)

cpdef str2et_v(np.ndarray times):
    cdef double et
    cdef int i, n
    n = times.shape[0]
    # initialize output
    cdef double[:] ets = np.zeros(n, dtype=np.double)
    #main loop
    with boundscheck(False), wraparound(False):
        for i in range(n):
            # should this be unicode? or bytes? <unicode> seemed to work but unsure if safe
            str2et_c(<unicode> times[i], &et)
            ets[i] = et
    # return results
    return np.asarray(ets)
