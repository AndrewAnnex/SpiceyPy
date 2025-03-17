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
from cpython.unicode cimport PyUnicode_DecodeUTF8
import numpy as np
cimport numpy as np
from numpy cimport PyArray_GETPTR1
np.import_array()

DEF _default_len_out = 256

DEF TIMELEN = 64

ctypedef np.double_t DOUBLE_t

from .cyice cimport *


#B

cpdef double b1900() noexcept:
    return b1900_c()


cpdef double b1950() noexcept:
    return b1950_c()

#C

cpdef double convrt(double x, str inunit, str outunit):
    cdef double out
    cdef const char * _inunit = inunit
    cdef const char * _outunit = outunit
    convrt_c(x, _inunit, _outunit, &out)
    return out


@boundscheck(False)
@wraparound(False)
cpdef convrt_v(double[:] x, str inunit, str outunit):
    cdef int i, n
    n = x.shape[0]
    cdef const char * _inunit = inunit
    cdef const char * _outunit = outunit
    cdef np.ndarray[dtype=np.double_t, ndim=1, mode="c"] outs = np.zeros(n, dtype=np.double)
    cdef double[:] _outs = outs
    cdef double out = 0.0
    # main loop
    for i in range(n):
        convrt_c(x[n], _inunit, _outunit, &out)
        _outs[i] = out
    return outs


#D


cpdef double deltet(epoch: float, eptype: str):
    cdef double delta
    cdef const char* _eptype = eptype
    deltet_c(epoch, _eptype, &delta)
    return delta


#E 


cpdef et2lst(
    et: float,
    body: int,
    lon: float,
    typein: str,
):
    cdef SpiceInt hr, mn, sc
    cdef char[_default_len_out] time
    cdef char[_default_len_out] ampm
    cdef const char * _typein = typein
    et2lst_c(
        et,
        body,
        lon,
        _typein,
         _default_len_out,
         _default_len_out,
        &hr, &mn, &sc, time, ampm
    )
    return hr, mn, sc, PyUnicode_DecodeUTF8(time, strlen(time), "strict"), PyUnicode_DecodeUTF8(ampm, strlen(ampm), "strict")


# cpdef et2lst_c(
#    double[:] ets,
#    int body,
#    double lon,
#    str typein
# ):
#     cdef Py_ssize_t i, n
#     n = ets.shape[0]
#     cdef SpiceInt hr, mn, sc
#     cdef char[_default_len_out] time
#     cdef char[_default_len_out] ampm
#     cdef const char * _typein = typein
#     # initialize output arrays 
#     cdef np.ndarray[dtype=np.int, ndim=1] hrs = np.zeros(n, dtype=np.int)
#     cdef int[:] _hrs = hrs
#     cdef np.ndarray[dtype=np.int, ndim=1] mns = np.zeros(n, dtype=np.int)
#     cdef int[:] _mns = mns
#     cdef np.ndarray[dtype=np.int, ndim=1] scs = np.zeros(n, dtype=np.int)
#     cdef int[:] _scs = scs
#     # TODO: using a unicode numpy array?
#     cdef np.ndarray[dtype=np.str_, ndim=2] times = np.zeros(n, dtype=np.str_)
#     #cdef list times = [None] * n
#     cdef np.ndarray[dtype=np.str_, ndim=2] ampms = np.zeros(n, dtype=np.str_)
#     # main loop
#     for i in range(n):
#         et2lst_c(
#             ets[i],
#             body,
#             lon,
#             _typein,
#              _default_len_out,
#              _default_len_out,
#             &hr, &mn, &sc, time, ampm
#         )
#         #
#         _hrs[i] = hr
#         _mns[i] = mn
#         _scs[i] = sc
#         # Idea, set strlen once on first iteration thne re-use
#         times[i] = PyUnicode_DecodeUTF8(time, strlen(time), "strict")
#         ampms[i] = PyUnicode_DecodeUTF8(ampm, strlen(ampm), "strict")

#     return hrs, mns, scs, times, ampms 


cpdef str et2utc(et: float, format_str: str, prec: int):
    cdef char[TIMELEN] c_buffer
    cdef const char* _format_str = format_str
    et2utc_c(et, _format_str, prec, TIMELEN, c_buffer) # TODO or &c_buffer[0]?
    return PyUnicode_DecodeUTF8(c_buffer, strlen(c_buffer), "strict")


@boundscheck(False)
@wraparound(False)
cpdef et2utc_v(double[:] ets, str format_str, int prec):
    cdef char[TIMELEN] c_buffer
    cdef Py_ssize_t i, n, fixed_length
    n = ets.shape[0]
    # convert the strings to pointers once
    cdef const char* _format_str = format_str
    # initialize output arrays TODO: using a unicode numpy array?
    cdef list results = [None] * n
    # Process the first element and compute the fixed length.
    et2utc_c(ets[0], _format_str, prec, TIMELEN, c_buffer)  # TODO or &c_buffer[0]?
    fixed_length = strlen(c_buffer)
    results[0] = PyUnicode_DecodeUTF8(c_buffer, fixed_length, "strict")
    # main loop for all other values
    if n > 1:
        for i in range(1, n):
            et2utc_c(ets[i], _format_str, prec, TIMELEN, c_buffer)
            results[i] = PyUnicode_DecodeUTF8(c_buffer, fixed_length, "strict")
    # return array
    return results


cpdef str etcal(double et):
    cdef char[TIMELEN] c_buffer
    etcal_c(et, TIMELEN, &c_buffer[0])
    return <unicode> c_buffer


@boundscheck(False)
@wraparound(False)
cpdef etcal_v(double[:] ets):
    cdef Py_ssize_t i, n = ets.shape[0]
    # Allocate a 2D buffer of shape (n, 24) with dtype np.uint8
    cdef np.ndarray[dtype=np.uint8_t, ndim=2] buf = np.empty((n, 25), dtype=np.uint8)
    # Create a typed memoryview over the buffer
    cdef unsigned char[:, :] view = buf
    for i in range(n):
        # Get a pointer to the start of the i-th row and call etcal_c
        etcal_c(ets[i], 25, <char*> &view[i, 0])
    # Convert the buffer to a 1D array of fixed-length byte strings (dtype "|S25") (need extra byte for termination)
    return buf.view(dtype="|S25").reshape(n)

# # F

cpdef int failed() noexcept:
    return failed_c()


cpdef void furnsh(file: str):
    cdef const char* _file = file
    furnsh_c(_file)
    
    
cpdef str getmsg(str option, int msglen):
    cdef const char * _option = option
    cdef char* _msgstr = <char *> malloc((msglen) * sizeof(char))
    getmsg_c(_option, msglen, _msgstr)
    pymsg = <unicode> _msgstr
    free(_msgstr)
    return pymsg


cpdef str qcktrc(int tracelen):
    cdef char * _tracestr = <char *> malloc((tracelen) * sizeof(char))
    qcktrc_c(tracelen, _tracestr)
    pytracestr = <unicode> _tracestr
    free(_tracestr)
    return pytracestr

#L

cpdef double lspcn(body: str, et: double, abcorr: str):
    cdef double l_s
    cdef const char * _body   = body
    cdef const char * _abcorr = abcorr
    l_s = lspcn_c(_body, et, _abcorr)
    return l_s


@boundscheck(False)
@wraparound(False)
cpdef double lspcn_v(body: str, ets: double[:], abcorr: str):
    cdef double l_s
    cdef const char * _body   = body
    cdef const char * _abcorr = abcorr
    cdef Py_ssize_t n, i
    n = ets.shape[0]
    cdef np.ndarray[dtype=np.double_t, ndim=1] l_s_s = np.zeros(n, dtype=np.double)
    cdef double[:] _l_s_s = l_s_s
    for i in range(n):
        l_s = lspcn_c(_body, ets[i], _abcorr)
        _l_s_s[i] = l_s
    return  l_s_s


cpdef void reset() noexcept:
    reset_c()

#S

cpdef str scdecd(sc: int, sclkdp: float):
    cdef int _sc
    _sc = sc
    cdef char[_default_len_out] c_buffer 
    scdecd_c(_sc, sclkdp, _default_len_out, c_buffer)
    return PyUnicode_DecodeUTF8(c_buffer, strlen(c_buffer), "strict")


@boundscheck(False)
@wraparound(False)
cpdef list[str] scdecd_v(sc: int, sclkdps: double[:]):
    cdef int _sc
    _sc = sc
    cdef Py_ssize_t n, i, length
    n = len(sclkdps)
    cdef double[:] _sclkdps = sclkdps
    cdef char[_default_len_out] c_buffer 
    cdef list sclkchs = [None] * n
    scdecd_c(sc, sclkdps[0], _default_len_out, c_buffer)
    length = strlen(c_buffer)
    sclkchs[0] = PyUnicode_DecodeUTF8(c_buffer, length, "strict") 
    if n > 1:
        for i in range(1, n):
            scdecd_c(_sc, _sclkdps[i], _default_len_out, c_buffer)
            sclkchs[i] = PyUnicode_DecodeUTF8(c_buffer, length, "strict")
    return sclkchs


cpdef double scencd(sc: int, sclkch: str):
    cdef int _sc
    _sc = sc
    cdef double sclkdp
    cdef const char * _sclkch = sclkch
    scencd_c(_sc, _sclkch, &sclkdp)
    return sclkdp


@boundscheck(False)
@wraparound(False)
cpdef double scencd_v(sc: int, sclkchs: list[str]):
    cdef int _sc
    _sc = sc
    cdef Py_ssize_t n, i
    n = len(sclkchs)
    cdef double sclkdp
    cdef np.ndarray[dtype=np.double_t, ndim=1] sclkdps = np.empty(n, dtype=np.double)
    cdef double[:] _sclkdps = sclkdps
    for i in range(n):
        scencd_c(_sc, sclkchs[i], &sclkdp)
        _sclkdps[i] = sclkdp
    return sclkdp


cpdef double sce2c(sc: int, et: float):
    cdef int _sc
    _sc = sc
    cdef double sclkdp
    sce2c_c(_sc, et, &sclkdp)
    return sclkdp


@boundscheck(False)
@wraparound(False)
cpdef double sce2c_v(sc: int, double[:] ets):
    cdef int _sc
    _sc = sc
    cdef double sclkdp
    cdef Py_ssize_t n, i
    n = ets.shape[0]
    cdef np.ndarray[dtype=np.double_t, ndim=1] sclkdps = np.zeros(n, dtype=np.double)
    cdef double[:] _sclkdps = sclkdps
    for i in range(n):
        sce2c_c(_sc, ets[i], &sclkdp)
        _sclkdps[i] = sclkdp
    return sclkdps


cpdef double sce2s(sc: int, et: float):
    cdef int _sc
    _sc = sc
    cdef char c_buffer[_default_len_out]
    sce2s_c(_sc, et, _default_len_out, c_buffer)
    return PyUnicode_DecodeUTF8(c_buffer, strlen(c_buffer), "strict")


cpdef double scs2e(sc: int, sclkch: str):
    cdef double et
    cdef const char * _sclkch = sclkch
    scs2e_c(sc, _sclkch, &et)
    return et


# todo need to accept a list or array of strings
# cpdef double scs2e_v(sc: int, sclkch: str):
#     cdef double et
#     cdef const char * _sclkch = sclkch
#     sct2e_c(sc, _sclkch, &et)
#     return et



cpdef double sct2e(sc: int, sclkdp: float):
    cdef int _sc
    _sc = sc
    cdef double et
    sct2e_c(_sc, sclkdp, &et)
    return et


@boundscheck(False)
@wraparound(False)
cpdef double sct2e_v(long sc, double[:] sclkdp):
    cdef Py_ssize_t n, i
    n = sclkdp.shape[0]
    cdef np.ndarray[dtype=np.double_t, ndim=1] ets = np.zeros(n, dtype=np.double)
    cdef double[:] _ets = ets
    cdef double et
    for i in range(n):
        sct2e_c(sc, sclkdp[0], &et)
        _ets[i] = et
    return ets

    
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


cpdef double str2et(time: str):
    cdef double et
    cdef const char* _time = time
    str2et_c(_time, &et)
    return et
    

@boundscheck(False)
@wraparound(False)
cpdef str2et_v(np.ndarray times):
    cdef double et
    cdef Py_ssize_t i, n
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
    cdef const char * _fromstring = fromstring
    cdef const char * _tostring = tostring
    sxform_c(_fromstring, _tostring, et, tform)
    return np.asarray(<np.double_t[:6, :6]> tform)


@boundscheck(False)
@wraparound(False)
cpdef sxform_v(str fromstring, str tostring, double[:] ets):
    cdef double[6][6] tform
    cdef const char * _fromstring = fromstring
    cdef const char * _tostring = tostring
    cdef size_t i, n
    n = ets.shape[0]
    cdef np.ndarray[dtype=np.double_t, ndim=3] xform = np.zeros((n, 6, 6), dtype=np.double)
    cdef double[:,:,::1] _xform = xform
    for i in range(n):
        sxform_c(_fromstring, _tostring, ets[i], tform)
        _xform[i,:,:] = tform
    return xform

# T

cpdef str timout(et: float, pictur: str):
    cdef const char * _pictur = pictur 
    cdef char[_default_len_out] c_buffer
    timout_c(et, _pictur, _default_len_out, c_buffer)
    return PyUnicode_DecodeUTF8(c_buffer, strlen(c_buffer), "strict")


@boundscheck(False)
@wraparound(False)
cpdef list[str] timout_v(double[:] ets, str pictur):
    cdef Py_ssize_t n, i
    n = ets.shape[0]
    cdef const char * _pictur = pictur 
    cdef char[_default_len_out] c_buffer
    cdef list output = [None] * n
    for i in range(n):
        timout_c(ets[i], _pictur, _default_len_out, c_buffer)
        output[i] = PyUnicode_DecodeUTF8(c_buffer, strlen(c_buffer), "strict")
    return output


# U

cpdef double unitim(
        epoch: float,
        insys: str,
        outsys: str,
    ):
    cdef const char * _insys = insys
    cdef const char * _outsys = outsys
    return unitim_c(epoch, _insys, _outsys)

@boundscheck(False)
@wraparound(False)
cpdef double[:] unitim_v(
        double[:] epochs,
        insys: str,
        outsys: str,
    ):
    cdef double _unitim
    cdef Py_ssize_t i, n 
    n = epochs.shape[0]
    cdef np.ndarray[dtype=np.double_t, ndim=1] unitims = np.zeros(n, dtype=np.double)
    cdef double[:] _unitims = unitims
    cdef const char * _insys = insys
    cdef const char * _outsys = outsys
    for i in range(n):
        _unitim = unitim_c(epochs[i], _insys, _outsys)
        _unitims[i] = _unitim
    return unitims


cpdef void unload(file: str) noexcept:
    cdef const char* _file = file
    unload_c(_file)


cpdef double utc2et(utcstr: str):
    cdef double et
    cdef const char* _utcstr = utcstr
    utc2et_c(_utcstr, &et)
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
