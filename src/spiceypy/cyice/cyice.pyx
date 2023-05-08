# cython: language_level = 3
# cython: embedsignature = True
# cython: c_string_type = bytes
# cython: c_string_encoding = utf-8
"""
main cython wrapper code
"""
from libc.stdlib cimport malloc, calloc, free
from libc.string cimport memcpy, strlen
from cython cimport boundscheck, wraparound
import numpy as np
cimport numpy as np
np.import_array()

DEF TIMELEN = 64

ctypedef np.double_t DOUBLE_t

from .cyice cimport *


cpdef double b1900() nogil:
    return b1900_c()


cpdef double b1950() nogil:
    return b1950_c()


cpdef str et2utc(double et, str format_str, int prec):
    cdef char[TIMELEN+1] string 
    et2utc_c(et, format_str, prec, TIMELEN, string)
    return <unicode> string


@boundscheck(False)
@wraparound(False)
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
    for i in range(n):
        et2utc_c(ets[i], _format_str, prec, TIMELEN, _utcstr)
        # todo this will call strlen so it would be slow, would be best to 
        #  compute length in bytes ahead of time given format and prec
        results[i] = <unicode> _utcstr
    # free temporary char pointer
    free(_utcstr)
    # return array
    return results


cpdef str etcal(double et):
    cdef char[49] string
    etcal_c(et, 49, string)
    return <unicode> string


@boundscheck(False)
@wraparound(False)
cpdef etcal_v(double[:] ets):
    cdef int i, n
    n = ets.shape[0]
    cdef char[49] string
    cdef list results = [None] * n
    for i in range(n):
        etcal_c(ets[i], 49, string)
        results[i] = <unicode> string
    return results


cpdef furnsh(str file):
    furnsh_c(file)
    
    
cpdef spkez(int target, double epoch, str ref, str abcorr, int observer):
    cdef double[6] state = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    cdef double lt = 0.0
    spkez_c(target, epoch, ref, abcorr, observer, state, &lt)
    return state, lt


@boundscheck(False)
@wraparound(False)
cpdef spkez_v(int target, double[:] epoch, str ref, str abcorr, int observer):
    # initialize c variables
    cdef double[6] state = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    cdef double lt = 0.0
    cdef int i, n
    # get the number of epochs defining the size of everything else
    n = epoch.shape[0]
    # convert the strings to pointers once
    cdef int _target   = target
    cdef const char* _ref    = ref
    cdef const char* _abcorr = abcorr
    cdef int _observer = observer
    # initialize output arrays
    cdef np.ndarray[dtype=np.double_t, ndim=2] states = np.zeros((n,6), dtype=np.double)
    cdef double[:,::1] _states = states
    cdef np.ndarray[dtype=np.double_t, ndim=1] lts = np.zeros(n, dtype=np.double)
    cdef double[:] _lts = lts
    # main loop
    with nogil:
        for i in range(n):
            spkez_c(_target, epoch[i], _ref, _abcorr, _observer, state, &lt)
            _states[i][0] = state[0]
            _states[i][1] = state[1]
            _states[i][2] = state[2]
            _states[i][3] = state[3]
            _states[i][4] = state[4]
            _states[i][5] = state[5]
            _lts[i] = lt
    # return results
    return states, lts

    
cpdef spkezr(str target, double epoch, str frame, str abcorr, str observer):
    cdef double[6] state = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    cdef double lt = 0.0
    spkezr_c(target, epoch, frame, abcorr, observer, state, &lt)
    return state, lt


@boundscheck(False)
@wraparound(False)
cpdef spkezr_v(str target, double[:] epoch, str frame, str abcorr, str observer):
    # initialize c variables
    cdef double[6] state = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    cdef double lt = 0.0
    cdef int i, n
    # get the number of epochs defining the size of everything else
    n = epoch.shape[0]
    # convert the strings to pointers once
    cdef const char* _target   = target
    cdef const char* _frame    = frame
    cdef const char* _abcorr   = abcorr
    cdef const char* _observer = observer
    # initialize output arrays
    cdef np.ndarray[dtype=np.double_t, ndim=2] states = np.zeros((n,6), dtype=np.double)
    cdef double[:,::1] _states = states
    cdef np.ndarray[dtype=np.double_t, ndim=1] lts = np.zeros(n, dtype=np.double)
    cdef double[:] _lts = lts
    # main loop
    with nogil:
        for i in range(n):
            spkezr_c(_target, epoch[i], _frame, _abcorr, _observer, state, &lt)
            _states[i][0] = state[0]
            _states[i][1] = state[1]
            _states[i][2] = state[2]
            _states[i][3] = state[3]
            _states[i][4] = state[4]
            _states[i][5] = state[5]
            _lts[i] = lt
    # return results
    return states, lts


cpdef spkpos(str targ, double et, str ref, str abcorr, str obs):
    cdef double[3] ptarg = (0.0, 0.0, 0.0)
    cdef double lt = 0.0
    spkpos_c(targ, et, ref, abcorr, obs, ptarg, &lt)
    return ptarg, lt
    

@boundscheck(False)
@wraparound(False)
cpdef spkpos_v(str targ, double[:] ets, str ref, str abcorr, str obs):
    # initialize c variables
    cdef double[3] ptarg = (0.0, 0.0, 0.0)
    cdef double lt = 0.0
    cdef int i, j, n
    # get the number of epochs defining the size of everything else
    n = ets.shape[0]
    # convert the strings to pointers once
    cdef const char* _targ   = targ
    cdef const char* _ref    = ref
    cdef const char* _abcorr = abcorr
    cdef const char* _obs    = obs
    # initialize output arrays
    cdef np.ndarray[dtype=np.double_t, ndim=2] ptargs = np.zeros((n,3), dtype=np.double)
    cdef double[:,::1] _ptargs = ptargs
    cdef np.ndarray[dtype=np.double_t, ndim=1] lts = np.zeros(n, dtype=np.double)
    cdef double[:] _lts = lts
    # main loop
    with nogil:
        for i in range(n):
            spkpos_c(_targ, ets[i], _ref, _abcorr, _obs, ptarg, &lt)
            _ptargs[i][0] = ptarg[0]
            _ptargs[i][1] = ptarg[1]
            _ptargs[i][2] = ptarg[2]
            _lts[i] = lt
    # return results
    return ptargs, lts


cpdef double str2et(str time):
    cdef double et
    str2et_c(time, &et)
    return et
    

@boundscheck(False)
@wraparound(False)
cpdef str2et_v(np.ndarray times):
    cdef double et
    cdef int i, n
    n = times.shape[0]
    # initialize output
    cdef np.ndarray[dtype=np.double_t, ndim=1] ets = np.zeros(n, dtype=np.double)
    cdef double[:] _ets = ets
    #main loop
    for i in range(n):
        # should this be unicode? or bytes? <unicode> seemed to work but unsure if safe
        str2et_c(times[i], &et)
        _ets[i] = et
    # return results
    return ets


cpdef sxform(str fromstring, str tostring, double et):
    cdef double[6][6] tform 
    sxform_c(fromstring, tostring, et, tform)
    return np.asarray(<np.double_t[:6, :6]> tform)


@boundscheck(False)
@wraparound(False)
cpdef sxform_v(str fromstring, str tostring, double[:] ets):
    cdef double[6][6] tform
    cdef size_t i, n
    n = ets.shape[0]
    cdef np.ndarray[dtype=np.double_t, ndim=3] xform = np.zeros((n, 6, 6), dtype=np.double)
    cdef double[:,:,::1] _xform = xform
    for i in range(n):
        sxform_c(fromstring, tostring, ets[i], tform)
        _xform[i,:,:] = tform
    return xform


cpdef double utc2et(str utcstr):
    cdef double et
    utc2et_c(utcstr, &et)
    return et


@boundscheck(False)
@wraparound(False)
cpdef utc2et_v(np.ndarray utcstr):
    cdef double et
    cdef int i, n
    n = utcstr.shape[0]
    cdef np.ndarray[dtype=np.double_t, ndim=1] ets = np.zeros(n, dtype=np.double)
    cdef double[:] _ets = ets
    
    for i in range(n):
        utc2et_c(utcstr[i], &et)
        _ets[i] = et

    return ets
