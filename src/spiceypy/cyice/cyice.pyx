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
from cython.parallel import prange
from cpython.unicode cimport PyUnicode_DecodeUTF8
import numpy as np
cimport numpy as np
np.import_array()

DEF _default_len_out = 256

DEF TIMELEN = 64

ctypedef np.double_t DOUBLE_t
ctypedef np.uint64_t INT_t 
ctypedef np.uint8_t CHAR_t
ctypedef np.uint8_t BOOL_t


from .cyice cimport *


#B

cpdef double b1900() noexcept:
    return b1900_c()


cpdef double b1950() noexcept:
    return b1950_c()

#C

@boundscheck(False)
@wraparound(False)
cpdef ckgp(
        inst: int,
        sclkdp: double,
        tol: double,
        ref: str
    ):
    # initialize c variables
    cdef long c_inst = inst
    cdef double c_sclkdp = sclkdp
    cdef double c_tol = tol
    cdef double c_clkout = 0.0
    cdef bint c_found = False
    cdef double[3][3] _c_cmat 
    # convert the strings to pointers once
    cdef const char* c_ref = ref
    # initialize output arrays
    # TODO avoiding the extra python numpy dec may be better
    cdef double[:,::1] c_cmat = np.empty((3,3), dtype=np.double)
    # perform the call
    ckgp_c(
        c_inst,
        c_sclkdp,
        c_tol,
        c_ref,
        _c_cmat, # todo attempt to avoid extra c array with memoryview
        &c_clkout,
        &c_found
    )
    # accumulate the results
    c_cmat[0][0] = _c_cmat[0][0]
    c_cmat[0][1] = _c_cmat[0][1]
    c_cmat[0][2] = _c_cmat[0][2]
    c_cmat[1][0] = _c_cmat[1][0]
    c_cmat[1][1] = _c_cmat[1][1]
    c_cmat[1][2] = _c_cmat[1][2]
    c_cmat[2][0] = _c_cmat[2][0]
    c_cmat[2][1] = _c_cmat[2][1]
    c_cmat[2][2] = _c_cmat[2][2]
    # return results
    return c_cmat, c_clkout, c_found


cpdef ckgpav(
        inst: int,
        sclkdp: double,
        tol: double,
        ref: str
    ):
    # initialize c variables
    cdef long c_inst = inst
    cdef double c_sclkdp = sclkdp
    cdef double c_tol = tol
    cdef double c_clkout = 0.0
    cdef bint c_found = False
    cdef double[3][3] _c_cmat 
    cdef double[3] _c_av
    # convert the strings to pointers once
    cdef const char* c_ref = ref
    # initialize output arrays
    # TODO avoiding the extra python numpy dec may be better
    cdef double[:,::1] c_cmat = np.empty((3,3), dtype=np.double)
    cdef double[::1] c_av = np.empty(3, dtype=np.double)
    # perform the call
    ckgpav_c(
        c_inst,
        c_sclkdp,
        c_tol,
        c_ref,
        _c_cmat, # todo attempt to avoid extra c array with memoryview
        _c_av,
        &c_clkout,
        &c_found
    )
    # accumulate the results
    c_cmat[0][0] = _c_cmat[0][0]
    c_cmat[0][1] = _c_cmat[0][1]
    c_cmat[0][2] = _c_cmat[0][2]
    c_cmat[1][0] = _c_cmat[1][0]
    c_cmat[1][1] = _c_cmat[1][1]
    c_cmat[1][2] = _c_cmat[1][2]
    c_cmat[2][0] = _c_cmat[2][0]
    c_cmat[2][1] = _c_cmat[2][1]
    c_cmat[2][2] = _c_cmat[2][2]
    c_av[0] = _c_av[0]
    c_av[1] = _c_av[1]
    c_av[2] = _c_av[2]
    # return results
    return c_cmat, c_av, c_clkout, c_found


cpdef double convrt(double x, str inunit, str outunit):
    cdef double out
    cdef const char * _inunit = inunit
    cdef const char * _outunit = outunit
    convrt_c(x, _inunit, _outunit, &out)
    return out


@boundscheck(False)
@wraparound(False)
cpdef double[::1] convrt_v(
    double[::1] x, 
    str inunit, 
    str outunit
    ):
    cdef Py_ssize_t i, n = x.shape[0]
    cdef const char * c_inunit = inunit
    cdef const char * c_outunit = outunit
    cdef double[::1] c_outs = np.empty(n, dtype=np.double)
    # main loop
    for i in range(n):
        convrt_c(
            x[i], 
            c_inunit,
            c_outunit, 
            &c_outs[i]
        )
    return c_outs


#D


cpdef double deltet(epoch: float, eptype: str):
    cdef double delta
    cdef const char* c_eptype = eptype
    deltet_c(
        epoch, 
        c_eptype, 
        &delta
    )
    return delta


# new rule: always use type name style if accepting arrays as input
@boundscheck(False)
@wraparound(False)
cpdef double[:] deltet_v(
    double[::1] epochs, 
    str eptype
    ):
    cdef Py_ssize_t i, n = epochs.shape[0]
    cdef const char* c_eptype = eptype
    # allocate output array
    cdef double[::1] deltas = np.empty(n, dtype=np.double)
    # perform the loop
    with nogil:
        for i in range(n):
            deltet_c(
                epochs[i], 
                c_eptype, 
                &deltas[i]
            )
    # return results
    return deltas

#E 


cpdef et2lst(
    et: float,
    body: int,
    lon: float,
    typein: str,
):
    cdef SpiceInt hr, mn, sc
    cdef SpiceInt c_body = body
    cdef char[_default_len_out] time
    cdef char[_default_len_out] ampm
    cdef const char * c_typein = typein
    et2lst_c(
        et,
        c_body,
        lon,
        c_typein,
        _default_len_out,
        _default_len_out,
        &hr,
        &mn,
        &sc,
        time,
        ampm
    )
    return hr, mn, sc, PyUnicode_DecodeUTF8(time, strlen(time), "strict"), PyUnicode_DecodeUTF8(ampm, strlen(ampm), "strict")


@boundscheck(False)
@wraparound(False)
cpdef et2lst_v(
   ets: double[:],
   body: int,
   lon: double,
   typein: str
):
    cdef double[:] c_ets = ets
    cdef Py_ssize_t i, n = c_ets.shape[0]
    cdef char[_default_len_out] time
    cdef char[_default_len_out] ampm
    cdef const char * c_typein = typein
    cdef int c_body = body
    cdef double c_lon = lon
    # initialize output arrays 
    cdef int[:] c_hrs = np.empty(n, dtype=np.int)
    cdef int[:] c_mns = np.empty(n, dtype=np.int)
    cdef int[:] c_scs = np.empty(n, dtype=np.int)
    # TODO: using a unicode numpy array?
    cdef np.ndarray[dtype=CHAR_t, ndim=2] times = np.empty((n, _default_len_out), dtype=np.uint8)
    #cdef list times = [None] * n
    cdef np.ndarray[dtype=CHAR_t, ndim=2] ampms = np.empty((n, _default_len_out), dtype=np.uint8)
    # main loop
    for i in range(n):
        et2lst_c(
            c_ets[i],
            c_body,
            c_lon,
            c_typein,
            _default_len_out,
            _default_len_out,
            &c_hrs[i],
            &c_mns[i], 
            &c_scs[i], 
            <char*> &times[i, 0], 
            <char*> &ampms[i, 0]
        )
    # return values
    # TODO I don't like how I handle strings here, consider reverting to manual method
    return c_hrs, c_mns, c_scs, times.astype(np.str_), ampms.astype(np.str_) 


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
    cdef double[:] c_ets = ets
    n = c_ets.shape[0]
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
            et2utc_c(
                c_ets[i], 
                _format_str, 
                prec, 
                TIMELEN, 
                c_buffer
            )
            results[i] = PyUnicode_DecodeUTF8(c_buffer, fixed_length, "strict")
    # return array
    return results


cpdef str etcal(double et):
    cdef char[TIMELEN] c_buffer
    etcal_c(et, TIMELEN, &c_buffer[0])
    # Convert the C char* to a Python string
    return PyUnicode_DecodeUTF8(c_buffer, strlen(c_buffer), "strict")


@boundscheck(False)
@wraparound(False)
cpdef etcal_v(double[:] ets):
    cdef double[:] c_ets = ets
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # Allocate a 2D buffer of shape (n, 24) with dtype np.uint8
    cdef np.ndarray[dtype=CHAR_t, ndim=2] results = np.empty((n, 25), dtype=np.uint8)
    # Create a typed memoryview over the buffer
    cdef unsigned char[:, :] view = results
    for i in prange(n, nogil=True):
        # Get a pointer to the start of the i-th row and call etcal_c
        etcal_c(
            c_ets[i], 
            25, 
            <char*> &view[i, 0]
        )
    # Convert the buffer to a 1D array of fixed-length byte strings (dtype "|S25") (need extra byte for termination)
    return results.view(dtype="|S25").reshape(n) #.astype(np.str_) this converts it to a more usable dtype but adds overhead

# F

cpdef int failed() noexcept:
    return failed_c()


@boundscheck(False)
@wraparound(False)
cpdef bint fovray(
    str inst,
    double[::1] raydir,
    str rframe,
    str abcorr,
    str obsrvr,
    double et
):
    # initialize c variables
    cdef double c_et = et
    cdef SpiceBoolean c_visibl = False
    # convert the strings to pointers once
    cdef const char* c_inst     = inst
    cdef const char* c_rframe   = rframe
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsrvr   = obsrvr
    # perform the call
    fovray_c(
        c_inst,
        &raydir[0],
        c_rframe,
        c_abcorr,
        c_obsrvr,
        &c_et,
        &c_visibl
    )
    # return
    return c_visibl


@boundscheck(False)
@wraparound(False)    
cpdef np.ndarray[BOOL_t, ndim=1] fovray_v(
    str inst,
    double[::1] raydir,
    str rframe,
    str abcorr,
    str obsrvr,
    double[::1] ets
):
    # initialize c variables
    cdef Py_ssize_t i, n = ets.shape[0]
    # convert the strings to pointers once
    cdef const char* c_inst     = inst
    cdef const char* c_rframe   = rframe
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsrvr   = obsrvr
    # initialize output arrays
    cdef bint[:] c_visibl = np.empty(n, dtype=np.uint8)
    # perform the call
    with nogil:
        for i in range(n):
            fovray_c(
                c_inst,
                &raydir[0],
                c_rframe,
                c_abcorr,
                c_obsrvr,
                &ets[i],
                &c_visibl[i]
            )
    # return
    return c_visibl
  

cpdef bint fovtrg(
    inst: str,
    target: str,
    tshape: str,
    tframe: str,
    abcorr: str,
    obsrvr: str,
    et: float
):
    # initialize c variables
    cdef double c_et = et
    cdef bint c_visibl = False
    # convert the strings to pointers once
    cdef const char* c_inst     = inst
    cdef const char* c_target   = target
    cdef const char* c_tshape   = tshape
    cdef const char* c_tframe   = tframe
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsrvr   = obsrvr
    # perform the call
    fovtrg_c(
        c_inst,
        c_target,
        c_tshape,
        c_tframe,
        c_abcorr,
        c_obsrvr,
        &c_et,
        &c_visibl
    )
    # return
    return c_visibl


@boundscheck(False)
@wraparound(False)    
cpdef np.ndarray[BOOL_t, ndim=1] fovtrg_v(
    inst: str,
    target: str,
    tshape: str,
    tframe: str,
    abcorr: str,
    obsrvr: str,
    ets: double[:]
):
    # initialize c variables
    cdef double[:] c_ets = ets
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert the strings to pointers once
    cdef const char* c_inst     = inst
    cdef const char* c_target   = target
    cdef const char* c_tshape   = tshape
    cdef const char* c_tframe   = tframe
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsrvr   = obsrvr
    # initialize output arrays
    cdef np.ndarray[dtype=BOOL_t, ndim=1, mode="c"] p_visibl = np.empty(n, dtype=np.uint8)
    cdef bint[:] c_visibl = p_visibl
    # perform the call
    with nogil:
        for i in range(n):
            fovtrg_c(
                c_inst,
                c_target,
                c_tshape,
                c_tframe,
                c_abcorr,
                c_obsrvr,
                &c_ets[i],
                &c_visibl[i]
            )
    # return
    return p_visibl


cpdef void furnsh(file: str):
    cdef const char* _file = file
    furnsh_c(_file)
    

# G
cpdef str getmsg(str option, int msglen):
    cdef const char * _option = option
    cdef char* _msgstr = <char *> malloc((msglen) * sizeof(char))
    getmsg_c(_option, msglen, _msgstr)
    pymsg = <unicode> _msgstr
    free(_msgstr)
    return pymsg


# H

# i


# J


# K


# L

cpdef double lspcn(body: str, et: double, abcorr: str):
    cdef double l_s
    cdef const char * c_body   = body
    cdef const char * c_abcorr = abcorr
    l_s = lspcn_c(
        c_body, 
        et, 
        c_abcorr
    )
    return l_s


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[DOUBLE_t, ndim=1] lspcn_v(body: str, ets: double[:], abcorr: str):
    cdef double l_s
    cdef const char * _body   = body
    cdef const char * _abcorr = abcorr
    cdef Py_ssize_t n, i
    n = ets.shape[0]
    cdef const double[:] _ets = ets
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] l_s_s = np.empty(n, dtype=np.double)
    cdef double[:] _l_s_s = l_s_s
    for i in range(n):
        l_s = lspcn_c(_body, _ets[i], _abcorr)
        _l_s_s[i] = l_s
    return  l_s_s

#M 

#N 

#O 

#P 

# Q

cpdef str qcktrc(int tracelen):
    cdef char * _tracestr = <char *> malloc((tracelen) * sizeof(char))
    qcktrc_c(tracelen, _tracestr)
    pytracestr = <unicode> _tracestr
    free(_tracestr)
    return pytracestr

# R


cpdef void reset() noexcept:
    reset_c()

#S

cpdef str scdecd(sc: int, sclkdp: float):
    cdef SpiceInt _sc = sc
    cdef char[_default_len_out] c_buffer 
    scdecd_c(_sc, sclkdp, _default_len_out, c_buffer)
    return PyUnicode_DecodeUTF8(c_buffer, strlen(c_buffer), "strict")


@boundscheck(False)
@wraparound(False)
cpdef list[str] scdecd_v(sc: int, sclkdps: double[:]):
    cdef SpiceInt _sc = sc
    cdef Py_ssize_t n, i, length
    n = len(sclkdps)
    cdef double[:] _sclkdps = sclkdps
    cdef char[_default_len_out] c_buffer 
    cdef list sclkchs = [None] * n
    scdecd_c(_sc, sclkdps[0], _default_len_out, &c_buffer[0])
    length = strlen(c_buffer)
    sclkchs[0] = PyUnicode_DecodeUTF8(c_buffer, length, "strict") 
    if n > 1:
        for i in range(1, n):
            scdecd_c(_sc, _sclkdps[i], _default_len_out, &c_buffer[0])
            sclkchs[i] = PyUnicode_DecodeUTF8(c_buffer, length, "strict")
    return sclkchs


cpdef double scencd(sc: int, sclkch: str):
    cdef SpiceInt _sc = sc
    cdef double sclkdp
    cdef const char * _sclkch = sclkch
    scencd_c(_sc, _sclkch, &sclkdp)
    return sclkdp


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[DOUBLE_t, ndim=1] scencd_v(sc: int, sclkchs: list[str]):
    cdef SpiceInt _sc = sc
    cdef Py_ssize_t n, i
    n = len(sclkchs)
    cdef double sclkdp
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] sclkdps = np.empty(n, dtype=np.double)
    cdef double[:] _sclkdps = sclkdps
    for i in range(n):
        scencd_c(_sc, sclkchs[i], &sclkdp)
        _sclkdps[i] = sclkdp
    return sclkdp


cpdef double sce2c(sc: int, et: float):
    cdef SpiceInt _sc = sc
    cdef double sclkdp
    sce2c_c(_sc, et, &sclkdp)
    return sclkdp


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[DOUBLE_t, ndim=1] sce2c_v(sc: int, double[:] ets):
    cdef SpiceInt _sc = sc
    cdef double sclkdp
    cdef Py_ssize_t i, n = ets.shape[0]
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] sclkdps = np.empty(n, dtype=np.double)
    cdef double[:] _sclkdps = sclkdps
    for i in range(n):
        sce2c_c(_sc, ets[i], &sclkdp)
        _sclkdps[i] = sclkdp
    return sclkdps


cpdef double sce2s(
    int sc, 
    double et
    ):
    cdef int c_sc = sc
    cdef double c_et = et
    cdef char[_default_len_out] c_buffer
    sce2s_c(
        c_sc, 
        c_et, 
        _default_len_out, 
        &c_buffer[0]
    )
    return PyUnicode_DecodeUTF8(c_buffer, strlen(c_buffer), "strict")


@boundscheck(False)
@wraparound(False)
cpdef list[str] sce2s_v(sc: long, ets: double[:]):
    cdef SpiceInt _sc = sc
    cdef Py_ssize_t i, n = ets.shape[0]
    cdef char[_default_len_out] c_buffer
    cdef list sclkchs = [None] * n
    # perform the first iteration
    sce2s_c(_sc, ets[0], _default_len_out, &c_buffer[0])
    length = strlen(c_buffer)
    sclkchs[0] = PyUnicode_DecodeUTF8(c_buffer, length, "strict") 
    if n > 1:
        for i in range(1, n):
            sce2s_c(_sc, ets[i], _default_len_out, &c_buffer[0])
            sclkchs[i] = PyUnicode_DecodeUTF8(c_buffer, length, "strict")
    return sclkchs


cpdef double scs2e(sc: int, sclkch: str):
    cdef double et
    cdef const char * _sclkch = sclkch
    scs2e_c(sc, _sclkch, &et)
    return et


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[DOUBLE_t, ndim=1] scs2e_v(sc: long, sclkchs: np.ndarray):
    cdef SpiceInt _sc = sc
    cdef Py_ssize_t i, n = sclkchs.shape[0]
    cdef double et
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] ets = np.empty(n, dtype=np.double)
    cdef double[:] _ets = ets
    for i in range(1, n):
        scs2e_c(_sc, sclkchs[i],  &et)
        _ets[i] = et
    return ets


cpdef double sct2e(sc: int, sclkdp: float):
    cdef SpiceInt _sc = sc
    cdef double et
    sct2e_c(_sc, sclkdp, &et)
    return et


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[DOUBLE_t, ndim=1] sct2e_v(long sc, double[:] sclkdps):
    cdef SpiceInt _sc = sc
    cdef Py_ssize_t i, n = sclkdps.shape[0]
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] ets = np.empty(n, dtype=np.double)
    cdef double[:] c_ets = ets
    cdef double et
    for i in range(n):
        sct2e_c(_sc, sclkdps[i], &et)
        c_ets[i] = et
    return ets


@boundscheck(False)
@wraparound(False)
cpdef spkapo(
    targ: int,  
    et: float, 
    ref: str,
    sobs: double[:], 
    abcorr: str):
    # initialize c variables
    cdef double[6] c_sobs = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    c_sobs[0] = sobs[0]
    c_sobs[1] = sobs[1]
    c_sobs[2] = sobs[2]
    c_sobs[3] = sobs[3]
    c_sobs[4] = sobs[4]
    c_sobs[5] = sobs[5]
    cdef double[3] c_ptarg = (0.0, 0.0, 0.0)
    cdef double lt = 0.0
    # convert the strings to pointers once
    cdef const char* c_ref    = ref
    cdef const char* c_abcorr = abcorr
    cdef long c_targ = targ
    # initialize output arrays
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] ptarg = np.empty(3, dtype=np.double)
    cdef double[:] p_ptarg = ptarg
    spkapo_c(
        c_targ, 
        et, 
        c_ref, 
        c_sobs,
        c_abcorr, 
        c_ptarg, 
        &lt
    )
    p_ptarg[0] = c_ptarg[0]
    p_ptarg[1] = c_ptarg[1]
    p_ptarg[2] = c_ptarg[2]
    return ptarg, lt


@boundscheck(False)
@wraparound(False)
cpdef spkapo_v(
    targ: int,  
    ets: double[:], 
    ref: str,
    sobs: double[:], 
    abcorr: str):
    # initialize c variables
    cdef Py_ssize_t i, n = ets.shape[0]
    cdef double[:] c_ets = ets
    cdef double[6] c_sobs = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    c_sobs[0] = sobs[0]
    c_sobs[1] = sobs[1]
    c_sobs[2] = sobs[2]
    c_sobs[3] = sobs[3]
    c_sobs[4] = sobs[4]
    c_sobs[5] = sobs[5]
    cdef double[3] c_ptarg = (0.0, 0.0, 0.0)
    cdef double c_lt = 0.0
    # convert the strings to pointers once
    cdef const char* c_ref    = ref
    cdef const char* c_abcorr = abcorr
    cdef long c_targ = targ
    # initialize output arrays
    cdef np.ndarray[dtype=DOUBLE_t, ndim=2, mode="c"] ptarg = np.empty((n,3), dtype=np.double)
    cdef double[:,:] p_ptarg = ptarg
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] lts = np.empty(n, dtype=np.double)
    cdef double[:,:] p_lts = lts
    # perform the call
    with nogil:
        for i in range(n):
            spkapo_c(
                c_targ, 
                c_ets[i], 
                c_ref, 
                c_sobs,
                c_abcorr, 
                c_ptarg, 
                &c_lt
            )
            p_ptarg[i,0] = c_ptarg[0]
            p_ptarg[i,1] = c_ptarg[1]
            p_ptarg[i,2] = c_ptarg[2]
            p_lts[i] = c_lt
    return ptarg, lts



@boundscheck(False)
@wraparound(False)    
cpdef spkez(
    int target, 
    double epoch, 
    str ref, 
    str abcorr, 
    int observer
    ):
    # convert the strings to pointers once
    cdef const char* c_ref    = ref
    cdef const char* c_abcorr = abcorr
    # allocate output variables
    cdef double lt = 0.0
    cdef double[::1] c_state = np.empty(6, dtype=np.double)
    spkez_c(
        target, 
        epoch, 
        c_ref, 
        c_abcorr, 
        observer, 
        &c_state[0], 
        &lt)
    return c_state, lt


@boundscheck(False)
@wraparound(False)
cpdef spkez_v(
    int target, 
    double[::1] epoch, 
    str ref, 
    str abcorr, 
    int observer):
    # initialize c variables
    cdef Py_ssize_t i, n = epoch.shape[0]
    # convert the strings to pointers once
    cdef int c_target   = target
    cdef const char* c_ref    = ref
    cdef const char* c_abcorr = abcorr
    cdef int c_observer = observer
    # initialize output arrays
    cdef double[:,::1] c_states = np.empty((n,6), dtype=np.double)
    cdef double[:] c_lts = np.empty(n, dtype=np.double)
    # main loop
    with nogil:
        for i in range(n):
            spkez_c(
                c_target, 
                epoch[i], 
                c_ref, 
                c_abcorr, 
                c_observer, 
                &c_states[i][0], 
                &c_lts[i]
            )
    # return results
    return c_states, c_lts


@boundscheck(False)
@wraparound(False)
cpdef spkezp(
    targ: int,  
    et: float, 
    ref: str, 
    abcorr: str, 
    obs: int):
    # initialize c variables
    cdef double[3] c_ptarg = (0.0, 0.0, 0.0)
    cdef double lt = 0.0
    # convert the strings to pointers once
    cdef const char* _ref    = ref
    cdef const char* _abcorr = abcorr
    cdef int _targ = targ
    cdef int _obs = obs
    # initialize output arrays
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] ptarg = np.empty(3, dtype=np.double)
    cdef double[:] _ptarg = ptarg
    spkezp_c(
        _targ, 
        et, 
        _ref, 
        _abcorr, 
        _obs, 
        c_ptarg, 
        &lt
    )
    _ptarg[0] = c_ptarg[0]
    _ptarg[1] = c_ptarg[1]
    _ptarg[2] = c_ptarg[2]
    return ptarg, lt
    

@boundscheck(False)
@wraparound(False)
cpdef spkezp_v(
    int targ, 
    double[::1] ets, 
    str ref, 
    str abcorr, 
    int obs):
    cdef Py_ssize_t i, n = ets.shape[0]
    # initialize c variables
    cdef double lt = 0.0
    # convert the strings to pointers once
    cdef const char* c_ref    = ref
    cdef const char* c_abcorr = abcorr
    cdef int c_targ = targ
    cdef int c_obs = obs
    # initialize output arrays
    cdef double[:,::1] c_ptargs = np.empty((n,3), dtype=np.double)
    cdef double[::1] c_lts = np.empty(n, dtype=np.double)
    # main loop
    with nogil:
        for i in range(n):
            spkezp_c(
                c_targ, 
                ets[i],
                c_ref, 
                c_abcorr, 
                c_obs, 
                &c_ptargs[i][0], 
                &c_lts[i]
            )
    # return results
    return c_ptargs, c_lts


@boundscheck(False)
@wraparound(False)    
cpdef spkezr(
    str target, 
    double epoch, 
    str frame, 
    str abcorr, 
    str observer):
    cdef double lt = 0.0
    cdef double[::1] c_state = np.empty(6, dtype=np.double)
    spkezr_c(
        target, 
        epoch,
        frame, 
        abcorr, 
        observer, 
        &c_state[0], 
        &lt)
    return c_state, lt


@boundscheck(False)
@wraparound(False)
cpdef spkezr_v(
    str target, 
    double[::1] epoch, 
    str frame, 
    str abcorr, 
    str observer):
    # initialize c variables
    cdef double[6] state = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    cdef double lt = 0.0
    cdef Py_ssize_t i, n = epoch.shape[0]
    # convert the strings to pointers once
    cdef const char* _target   = target
    cdef const char* _frame    = frame
    cdef const char* _abcorr   = abcorr
    cdef const char* _observer = observer
    # initialize output arrays
    cdef np.ndarray[dtype=DOUBLE_t, ndim=2, mode="c"] states = np.empty((n,6), dtype=np.double)
    cdef double[:,::1] _states = states
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] lts = np.empty(n, dtype=np.double)
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


@boundscheck(False)
@wraparound(False)
cpdef spkcpo(
    target: str,
    et: float,
    outref: str,
    refloc: str,
    abcorr: str,
    obspos: double[:],
    obsctr: str,
    obsref: str):
    # initialize c variables
    cdef double[3] c_obspos
    c_obspos[0] = obspos[0] 
    c_obspos[1] = obspos[1] 
    c_obspos[2] = obspos[2] 
    cdef double[6] c_state = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    cdef double c_lt = 0.0
    cdef double c_et = et
    # convert the strings to pointers once
    cdef const char* c_target   = target
    cdef const char* c_outref   = outref
    cdef const char* c_refloc   = refloc
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsctr   = obsctr
    cdef const char* c_obsref   = obsref
    # initialize output arrays
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] state = np.empty(6, dtype=np.double)
    cdef double[:] _state = state
    # perform the call
    spkcpo_c(
        c_target,
        c_et,
        c_outref,
        c_refloc,
        c_abcorr,
        c_obspos,
        c_obsctr,
        c_obsref,
        c_state,
        &c_lt
    )
    # accumulate output
    _state[0] = c_state[0]
    _state[1] = c_state[1]
    _state[2] = c_state[2]
    _state[3] = c_state[3]
    _state[4] = c_state[4]
    _state[5] = c_state[5]
    # return output
    return state, c_lt


@boundscheck(False)
@wraparound(False)
cpdef spkcpo_v(
    target: str,
    ets: double[:],
    outref: str,
    refloc: str,
    abcorr: str,
    obspos: double[:], #TODO determine if to also vectorize this
    obsctr: str,
    obsref: str):
    cdef const double[:] c_ets = ets
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # initialize c variables TODO: vectorize obspos?
    cdef double[3] c_obspos
    c_obspos[0] = obspos[0] 
    c_obspos[1] = obspos[1] 
    c_obspos[2] = obspos[2] 
    cdef double[6] c_state = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    cdef double c_lt = 0.0
    # convert the strings to pointers once
    cdef const char* c_target   = target
    cdef const char* c_outref   = outref
    cdef const char* c_refloc   = refloc
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsctr   = obsctr
    cdef const char* c_obsref   = obsref
    # initialize output arrays
    cdef np.ndarray[dtype=DOUBLE_t, ndim=2, mode="c"] state = np.empty((n,6), dtype=np.double)
    cdef double[:, :] _state = state
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] lts = np.empty(n, dtype=np.double)
    cdef double[:, :] _lts = lts
    # perform the call
    with nogil:
        for i in range(n):
            spkcpo_c(
                c_target,
                c_ets[i],
                c_outref,
                c_refloc,
                c_abcorr,
                c_obspos,
                c_obsctr,
                c_obsref,
                c_state,
                &c_lt
            )
            # accumulate output
            _state[i, 0] = c_state[0]
            _state[i, 1] = c_state[1]
            _state[i, 2] = c_state[2]
            _state[i, 3] = c_state[3]
            _state[i, 4] = c_state[4]
            _state[i, 5] = c_state[5]
            _lts[i] = c_lt
    # return output
    return state, lts


@boundscheck(False)
@wraparound(False)
cpdef spkcpt(
    trgpos: double[:],
    trgctr: str,
    trgref: str,
    et: float,
    outref: str,
    refloc: str,
    abcorr: str,
    obsrvr: str):
    # initialize c variables
    cdef double[3] c_trgpos
    c_trgpos[0] = trgpos[0] 
    c_trgpos[1] = trgpos[1] 
    c_trgpos[2] = trgpos[2] 
    cdef double[6] c_state = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    cdef double c_lt = 0.0
    cdef double c_et = et
    # convert the strings to pointers once
    cdef const char* c_trgctr   = trgctr
    cdef const char* c_trgref   = trgref
    cdef const char* c_outref   = outref
    cdef const char* c_refloc   = refloc
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsrvr   = obsrvr
    # initialize output arrays
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] state = np.empty(6, dtype=np.double)
    cdef double[:] _state = state
    # perform the call
    spkcpt_c(
        c_trgpos,
        c_trgctr,
        c_trgref,
        c_et,
        c_outref,
        c_refloc,
        c_abcorr,
        c_obsrvr,
        c_state,
        &c_lt
    )
    # accumulate output
    _state[0] = c_state[0]
    _state[1] = c_state[1]
    _state[2] = c_state[2]
    _state[3] = c_state[3]
    _state[4] = c_state[4]
    _state[5] = c_state[5]
    # return output
    return state, c_lt


@boundscheck(False)
@wraparound(False)
cpdef spkcpt_v(
    trgpos: double[:],
    trgctr: str,
    trgref: str,
    ets: double[:],
    outref: str,
    refloc: str,
    abcorr: str,
    obsrvr: str):
    cdef const double[:] c_ets = ets
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # initialize c variables TODO: vectorize obspos?
    cdef double[3] c_trgpos
    c_trgpos[0] = trgpos[0] 
    c_trgpos[1] = trgpos[1] 
    c_trgpos[2] = trgpos[2] 
    cdef double[6] c_state = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    cdef double c_lt = 0.0
    # convert the strings to pointers once
    cdef const char* c_trgctr   = trgctr
    cdef const char* c_trgref   = trgref
    cdef const char* c_outref   = outref
    cdef const char* c_refloc   = refloc
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsrvr   = obsrvr
    # initialize output arrays
    cdef np.ndarray[dtype=DOUBLE_t, ndim=2, mode="c"] state = np.empty((n,6), dtype=np.double)
    cdef double[:, :] _state = state
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] lts = np.empty(n, dtype=np.double)
    cdef double[:, :] _lts = lts
    # perform the call
    with nogil:
        for i in range(n):
            spkcpt_c(
                c_trgpos,
                c_trgctr,
                c_trgref,
                c_ets[i],
                c_outref,
                c_refloc,
                c_abcorr,
                c_obsrvr,
                c_state,
                &c_lt
            )
            # accumulate output
            _state[i, 0] = c_state[0]
            _state[i, 1] = c_state[1]
            _state[i, 2] = c_state[2]
            _state[i, 3] = c_state[3]
            _state[i, 4] = c_state[4]
            _state[i, 5] = c_state[5]
            _lts[i] = c_lt
    # return output
    return state, lts


@boundscheck(False)
@wraparound(False)
cpdef spkcvo(
    target: str,
    et: float,
    outref: str,
    refloc: str,
    abcorr: str,
    obssta: double[:],
    obsepc: double,
    obsctr: str,
    obsref: str):
    # initialize c variables
    cdef double c_et = et
    cdef double[6] c_obssta
    c_obssta[0] = obssta[0] 
    c_obssta[1] = obssta[1] 
    c_obssta[2] = obssta[2] 
    c_obssta[3] = obssta[3] 
    c_obssta[4] = obssta[4] 
    c_obssta[5] = obssta[5] 
    cdef double c_obsepc = obsepc
    cdef double[6] c_state = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    cdef double c_lt = 0.0
    # convert the strings to pointers once
    cdef const char* c_target   = target
    cdef const char* c_outref   = outref
    cdef const char* c_refloc   = refloc
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsctr   = obsctr
    cdef const char* c_obsref   = obsref
    # initialize output arrays
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] state = np.empty(6, dtype=np.double)
    cdef double[:] _state = state
    # perform the call
    spkcvo_c(
        c_target,
        c_et,
        c_outref,
        c_refloc,
        c_abcorr,
        c_obssta,
        c_obsepc,
        c_obsctr,
        c_obsref,
        c_state,
        &c_lt
    )
    # accumulate output
    _state[0] = c_state[0]
    _state[1] = c_state[1]
    _state[2] = c_state[2]
    _state[3] = c_state[3]
    _state[4] = c_state[4]
    _state[5] = c_state[5]
    # return output
    return state, c_lt


@boundscheck(False)
@wraparound(False)
cpdef spkcvo_v(
    target: str,
    ets: double[:],
    outref: str,
    refloc: str,
    abcorr: str,
    obssta: double[:], # TODO vectorize here?
    obsepc: double,    # TODO vectorize here?
    obsctr: str,
    obsref: str):
    cdef const double[:] c_ets = ets
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # initialize c variables TODO: vectorize obssta?
    cdef double[6] c_obssta
    c_obssta[0] = obssta[0] 
    c_obssta[1] = obssta[1] 
    c_obssta[2] = obssta[2] 
    c_obssta[3] = obssta[3] 
    c_obssta[4] = obssta[4] 
    c_obssta[5] = obssta[5] 
    cdef double c_obsepc = obsepc
    cdef double[6] c_state = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    cdef double c_lt = 0.0
    # convert the strings to pointers once
    cdef const char* c_target   = target
    cdef const char* c_outref   = outref
    cdef const char* c_refloc   = refloc
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsctr   = obsctr
    cdef const char* c_obsref   = obsref
    # initialize output arrays
    cdef np.ndarray[dtype=DOUBLE_t, ndim=2, mode="c"] state = np.empty((n,6), dtype=np.double)
    cdef double[:, :] _state = state
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] lts = np.empty(n, dtype=np.double)
    cdef double[:, :] _lts = lts
    # perform the call
    with nogil:
        for i in range(n):
            spkcvo_c(
                c_target,
                c_ets[i],
                c_outref,
                c_refloc,
                c_abcorr,
                c_obssta,
                c_obsepc,
                c_obsctr,
                c_obsref,
                c_state,
                &c_lt
            )
            # accumulate output
            _state[i, 0] = c_state[0]
            _state[i, 1] = c_state[1]
            _state[i, 2] = c_state[2]
            _state[i, 3] = c_state[3]
            _state[i, 4] = c_state[4]
            _state[i, 5] = c_state[5]
            _lts[i] = c_lt
    # return output
    return state, lts


@boundscheck(False)
@wraparound(False)
cpdef spkcvt(
    double[::1] trgsta,
    double trgepc,
    str trgctr,
    str trgref,
    double et,
    str outref,
    str refloc,
    str abcorr,
    str obsrvr):
    # initialize c variables
    cdef double c_lt = 0.0
    # convert the strings to pointers once
    cdef const char* c_trgctr   = trgctr
    cdef const char* c_trgref   = trgref
    cdef const char* c_outref   = outref
    cdef const char* c_refloc   = refloc
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsrvr   = obsrvr
    # initialize output arrays
    cdef double[::1] c_state = np.empty(6, dtype=np.double)
    # perform the call
    spkcvt_c(
        &trgsta[0],
        trgepc,
        c_trgctr,
        c_trgref,
        et,
        c_outref,
        c_refloc,
        c_abcorr,
        c_obsrvr,
        &c_state[0],
        &c_lt
    )
    # return output
    return c_state, c_lt


@boundscheck(False)
@wraparound(False)
cpdef spkcvt_v(
    double[::1] trgsta,
    double trgepc,
    str trgctr,
    str trgref,
    double[::1] ets,
    str outref,
    str refloc,
    str abcorr,
    str obsrvr):
    # initialize c variables
    cdef Py_ssize_t i, n = ets.shape[0]
    # convert the strings to pointers once
    cdef const char* c_trgctr   = trgctr
    cdef const char* c_trgref   = trgref
    cdef const char* c_outref   = outref
    cdef const char* c_refloc   = refloc
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsrvr   = obsrvr
    # initialize output arrays
    cdef double[:, ::1] c_states = np.empty((n,6), dtype=np.double)
    cdef double[::1] c_lts = np.empty(n, dtype=np.double)
    # perform the call
    with nogil:
        for i in range(n):
            spkcvt_c(
                &trgsta[0],
                trgepc,
                c_trgctr,
                c_trgref,
                ets[i],
                c_outref,
                c_refloc,
                c_abcorr,
                c_obsrvr,
                &c_states[i][0],
                &c_lts[i]
            )
    # return output
    return c_states, c_lts


@boundscheck(False)
@wraparound(False)
cpdef spkgeo(
    targ: int,
    et: float,
    ref: str,
    obs: int
    ):
    # initialize c variables
    cdef long c_targ = targ
    cdef double c_et = et
    cdef double c_lt = 0.0
    cdef long c_obs  = obs
    # convert the strings to pointers once
    cdef const char* c_ref   = ref
    # initialize output arrays
    cdef double[::1] c_state = np.empty(6, dtype=np.double)
    # perform the call
    spkgeo_c(
        c_targ,
        c_et,
        c_ref,
        c_obs,
        &c_state[0],
        &c_lt
    )
    # return output
    return c_state, c_lt


@boundscheck(False)
@wraparound(False)
cpdef spkgeo_v(
    int targ,
    double[::1] ets,
    str ref,
    int obs,
    ):
    # initialize c variables
    cdef Py_ssize_t i, n = ets.shape[0]
    cdef long c_targ = targ
    cdef long c_obs  = obs
    # convert the strings to pointers once
    cdef const char* c_ref   = ref
    # initialize output arrays
    cdef double[:,::1] c_state = np.empty((n,6), dtype=np.double)
    cdef double[::1] c_lts = np.empty(n, dtype=np.double)
    # perform the call
    with nogil:
        for i in range(n):
            spkgeo_c(
                c_targ,
                ets[i],
                c_ref,
                c_obs,
                &c_state[i][0],
                &c_lts[i]
            )
    # return output
    return c_state, c_lts


@boundscheck(False)
@wraparound(False)
cpdef spkgps(
    int targ,
    double et,
    str ref,
    int obs
    ):
    # initialize c variables
    cdef int c_targ = targ
    cdef double c_et = et
    cdef double c_lt = 0.0
    cdef int c_obs  = obs
    # convert the strings to pointers once
    cdef const char* c_ref   = ref
    # initialize output arrays
    cdef double[::1] c_pos = np.empty(3, dtype=np.double)
    # perform the call
    spkgeo_c(
        c_targ,
        c_et,
        c_ref,
        c_obs,
        &c_pos[0],
        &c_lt
    )
    # return output
    return c_pos, c_lt


@boundscheck(False)
@wraparound(False)
cpdef spkgps_v(
    int targ,
    double[::1] ets,
    str ref,
    int obs,
    ):
    # initialize c variables
    cdef Py_ssize_t i, n = ets.shape[0]
    cdef long c_targ = targ
    cdef long c_obs  = obs
    # convert the strings to pointers once
    cdef const char* c_ref   = ref
    # initialize output arrays
    cdef double[:,::1] c_pos = np.empty((n,3), dtype=np.double)
    cdef double[::1] c_lts = np.empty(n, dtype=np.double)
    # perform the call
    with nogil:
        for i in range(n):
            spkgps_c(
                c_targ,
                ets[i],
                c_ref,
                c_obs,
                &c_pos[i][0],
                &c_lts[i]
            )
    # return output
    return c_pos, c_lts


@boundscheck(False)
@wraparound(False)
cpdef spkpvn(
    int handle,
    double[::1] descr,
    double et
    ):
    # initialize c variables
    cdef int c_handle = handle
    cdef double c_et = et
    # inititalize output variables
    cdef int c_ref = 0
    cdef int c_center = 0
    # initialize output arrays
    cdef double[::1] c_state = np.empty(6, dtype=np.double)
    # perform the call
    spkpvn_c(
        c_handle,
        &descr[0],
        c_et,
        &c_ref,
        &c_state[0],
        &c_center
    )
    # return output 
    return c_ref, c_state, c_center


@boundscheck(False)
@wraparound(False)
cpdef spkpvn_v(
    int handle,
    double[::1] descr,
    double[:] ets
    ):
    cdef Py_ssize_t i, n = ets.shape[0]
    # initialize c variables
    cdef int c_handle = handle
    # initialize output arrays
    cdef int[::1] c_refs  = np.empty(n, dtype=np.int)
    cdef double[:,::1] c_states = np.empty((n,6), dtype=np.double)
    cdef int[::1] c_centers  = np.empty(n, dtype=np.int)
    # perform the call
    with nogil:
        for i in range(n):
            spkpvn_c(
                c_handle,
                &descr[0],
                ets[i],
                &c_refs[i],
                &c_states[i][0],
                &c_centers[i]
            )
    # return output 
    return c_refs, c_states, c_centers


@boundscheck(False)
@wraparound(False)
cpdef spkpos(str target, double et, str ref, str abcorr, str obs):
    # initialize c variables
    cdef double[3] c_ptarg = (0.0, 0.0, 0.0)
    cdef double lt = 0.0
    # convert the strings to pointers once
    cdef const char* _targ   = target
    cdef const char* _ref    = ref
    cdef const char* _abcorr = abcorr
    cdef const char* _obs    = obs
    # initialize output arrays
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] ptarg = np.empty(3, dtype=np.double)
    cdef double[:] _ptarg = ptarg
    spkpos_c(
        _targ, 
        et, 
        _ref, 
        _abcorr, 
        _obs, 
        c_ptarg, 
        &lt
    )
    _ptarg[0] = c_ptarg[0]
    _ptarg[1] = c_ptarg[1]
    _ptarg[2] = c_ptarg[2]
    return ptarg, lt
    

@boundscheck(False)
@wraparound(False)
cpdef spkpos_v(str targ, double[:] ets, str ref, str abcorr, str obs):
    cdef const double[:] c_ets = ets
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # initialize c variables
    cdef double[3] ptarg = (0.0, 0.0, 0.0)
    cdef double lt = 0.0
    # convert the strings to pointers once
    cdef const char* _targ   = targ
    cdef const char* _ref    = ref
    cdef const char* _abcorr = abcorr
    cdef const char* _obs    = obs
    # initialize output arrays
    cdef np.ndarray[dtype=DOUBLE_t, ndim=2, mode="c"] ptargs = np.empty((n,3), dtype=np.double)
    cdef double[:,::1] _ptargs = ptargs
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] lts = np.empty(n, dtype=np.double)
    cdef double[:] _lts = lts
    # main loop
    with nogil:
        for i in range(n):
            spkpos_c(_targ, c_ets[i], _ref, _abcorr, _obs, ptarg, &lt)
            _ptargs[i][0] = ptarg[0]
            _ptargs[i][1] = ptarg[1]
            _ptargs[i][2] = ptarg[2]
            _lts[i] = lt
    # return results
    return ptargs, lts


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[DOUBLE_t, ndim=1] spkssb(
    targ: int,
    et: float,
    ref: str,
    ):
    # initialize c variables
    cdef long c_targ = targ
    cdef double c_et = et
    # convert the strings to pointers once
    cdef const char* c_ref   = ref
    # initialize output arrays
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] p_state = np.empty(6, dtype=np.double)
    cdef double[:] c_state = p_state
    # perform the call
    spkssb_c(
        c_targ,
        c_et,
        c_ref,
        &c_state[0],
    )
    # return output
    return p_state


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[DOUBLE_t, ndim=2] spkssb_v(
    targ: int,
    ets: double[:],
    ref: str,
    ):
    # initialize c variables
    cdef const double[:] c_ets = ets
    cdef Py_ssize_t i, n = c_ets.shape[0]
    cdef long c_targ = targ
    # convert the strings to pointers once
    cdef const char* c_ref   = ref
    # initialize output arrays
    cdef np.ndarray[dtype=DOUBLE_t, ndim=2, mode="c"] p_state = np.empty((n,6), dtype=np.double)
    cdef double[:,:] c_state = p_state
    # perform the call
    with nogil:
        for i in range(n):
            spkssb_c(
                c_targ,
                c_ets[i],
                c_ref,
                &c_state[i][0],
            )
    # return output
    return p_state


cpdef double str2et(time: str):
    cdef double et
    cdef const char* _time = time
    str2et_c(_time, &et)
    return et
    

@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[DOUBLE_t, ndim=1] str2et_v(np.ndarray times):
    cdef Py_ssize_t i, n = times.shape[0]
    cdef double _et
    # initialize output
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1] ets = np.empty(n, dtype=np.double)
    cdef double[:] _ets = ets
    #main loop
    for i in range(n):
        # should this be unicode? or bytes? <unicode> seemed to work but unsure if safe
        str2et_c(times[i], &_et)
        _ets[i] = _et
    # return results
    return ets

# TODO need error check, need found exception thrower in cython
@wraparound(False)
@boundscheck(False)
cpdef sincpt(
    method: str,
    target: str,
    et: float,
    fixref: str,
    abcorr: str,
    obsrvr: str,
    dref: str,
    dvec: double[:]):
    # convert strings 
    cdef const char * _method = method
    cdef const char * _target = target
    cdef const char * _fixref = fixref
    cdef const char * _abcorr = abcorr
    cdef const char * _obsrvr = obsrvr
    cdef const char * _dref   = dref
    # convert dvec to c #TODO vectorize over dvec too?
    cdef double[3] c_dvec
    c_dvec[0] = dvec[0]
    c_dvec[1] = dvec[1]
    c_dvec[2] = dvec[2]
    # Allocate output floats and arrays with appropriate shapes.
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] spoint = np.empty(3, dtype=np.double)
    cdef double[:] _spoint = spoint
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] srfvec = np.empty(3, dtype=np.double)
    cdef double[:] _srfvec = srfvec
    cdef double[3] c_spoint
    cdef double[3] c_srfvec
    cdef double c_trgepc
    cdef SpiceBoolean c_found
    # perform the call
    sincpt_c(
        _method,
        _target,
        et,
        _fixref,
        _abcorr,
        _obsrvr,
        _dref,
        c_dvec,
        c_spoint,
        &c_trgepc,
        c_srfvec,
        &c_found
    )
    # accumulate the results to output arrays
    _spoint[0] = c_spoint[0]
    _spoint[1] = c_spoint[1]
    _spoint[2] = c_spoint[2]
    _srfvec[0] = c_srfvec[0]
    _srfvec[1] = c_srfvec[1]
    _srfvec[2] = c_srfvec[2]
    # return results
    return spoint, c_trgepc, srfvec, c_found


# TODO need error check, need found exception thrower in cython
@wraparound(False)
@boundscheck(False)
cpdef sincpt_v(
    method: str,
    target: str,
    ets: double[:],
    fixref: str,
    abcorr: str,
    obsrvr: str,
    dref: str,
    dvec: double[:]):
    # get size of input array
    cdef Py_ssize_t i, n = ets.shape[0]
    cdef const double[:] _ets = ets
    # convert strings 
    cdef const char * _method = method
    cdef const char * _target = target
    cdef const char * _fixref = fixref
    cdef const char * _abcorr = abcorr
    cdef const char * _obsrvr = obsrvr
    cdef const char * _dref   = dref
    # convert dvec to c #TODO vectorize over dvec too?
    cdef double[3] c_dvec
    c_dvec[0] = dvec[0]
    c_dvec[1] = dvec[1]
    c_dvec[2] = dvec[2]
    # Allocate output floats and arrays with appropriate shapes.
    cdef np.ndarray[dtype=DOUBLE_t, ndim=2, mode="c"] spoint = np.empty((n,3), dtype=np.double)
    cdef double[:,:] _spoint = spoint
    cdef np.ndarray[dtype=DOUBLE_t, ndim=2, mode="c"] srfvec = np.empty((n,3), dtype=np.double)
    cdef double[:,:] _srfvec = srfvec
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] trgepc = np.empty(n, dtype=np.double)
    cdef double[:,:] _trgepc = trgepc
    cdef np.ndarray[dtype=BOOL_t, ndim=1, mode="c", cast=True] found = np.empty(n, dtype=np.uint8)
    cdef BOOL_t[:,:] _found = found
    cdef double[3] c_spoint
    cdef double[3] c_srfvec
    cdef double c_trgepc
    cdef SpiceBoolean c_found
    # perform the call
    for i in range(n):
        sincpt_c(
            _method,
            _target,
            _ets[i],
            _fixref,
            _abcorr,
            _obsrvr,
            _dref,
            c_dvec,
            c_spoint,
            &c_trgepc,
            c_srfvec,
            &c_found
        )
        # accumulate the results to output arrays
        _spoint[i,0] = c_spoint[0]
        _spoint[i,1] = c_spoint[1]
        _spoint[i,2] = c_spoint[2]
        _srfvec[i,0] = c_srfvec[0]
        _srfvec[i,1] = c_srfvec[1]
        _srfvec[i,2] = c_srfvec[2]
        _trgepc[i] = c_trgepc
        _found[i]  = c_found
        # return results
    return spoint, trgepc, srfvec, found



@wraparound(False)
@boundscheck(False)
cpdef subpnt(
    method: str,
    target: str, 
    et: float, 
    fixref: str, 
    abcorr: str, 
    obsrvr: str):
    # convert strings 
    cdef const char * _method = method
    cdef const char * _target = target
    cdef const char * _fixref = fixref
    cdef const char * _abcorr = abcorr
    cdef const char * _obsrvr = obsrvr
    # Allocate output floats and arrays with appropriate shapes.
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] spoint = np.empty(3, dtype=np.double)
    cdef double[:] _spoint = spoint
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] srfvec = np.empty(3, dtype=np.double)
    cdef double[:] _srfvec = srfvec
    cdef double trgepc
    cdef double[3] c_spoint
    cdef double[3] c_srfvec
    # perform the call
    subpnt_c(
        _method,
        _target,
        et,
        _fixref,
        _abcorr,
        _obsrvr,
        c_spoint,
        &trgepc,
        c_srfvec
        )
    # accumulate the results to output arrays
    _spoint[0] = c_spoint[0]
    _spoint[1] = c_spoint[1]
    _spoint[2] = c_spoint[2]
    _srfvec[0] = c_srfvec[0]
    _srfvec[1] = c_srfvec[1]
    _srfvec[2] = c_srfvec[2]
    # return results
    return spoint, trgepc, srfvec


@boundscheck(False)
@wraparound(False)
cpdef subpnt_v(
    method: str,
    target: str, 
    ets: double[:], 
    fixref: str, 
    abcorr: str, 
    obsrvr: str):
    # get size of input array
    cdef Py_ssize_t i, n = ets.shape[0]
    # convert strings 
    cdef const char * _method = method
    cdef const char * _target = target
    cdef const char * _fixref = fixref
    cdef const char * _abcorr = abcorr
    cdef const char * _obsrvr = obsrvr
    # Allocate output floats and arrays with appropriate shapes.
    cdef np.ndarray[dtype=DOUBLE_t, ndim=2, mode="c"] spoint = np.empty((n,3), dtype=np.double)
    cdef double[:,:] _spoint = spoint
    cdef np.ndarray[dtype=DOUBLE_t, ndim=2, mode="c"] srfvec = np.empty((n,3), dtype=np.double)
    cdef double[:,:] _srfvec = srfvec
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] trgepc = np.empty(n, dtype=np.double)
    cdef double[:] _trgepc = trgepc
    cdef double c_trgepc
    cdef double[3] c_spoint
    cdef double[3] c_srfvec
    # perform the call
    for i in range(n):
        subpnt_c(
            _method,
            _target,
            ets[i],
            _fixref,
            _abcorr,
            _obsrvr,
            c_spoint,
            &c_trgepc,
            c_srfvec
            )
        # accumulate the results to output arrays
        _spoint[i, 0] = c_spoint[0]
        _spoint[i, 1] = c_spoint[1]
        _spoint[i, 2] = c_spoint[2]
        _trgepc[i] = c_trgepc
        _srfvec[i, 0] = c_srfvec[0]
        _srfvec[i, 1] = c_srfvec[1]
        _srfvec[i, 2] = c_srfvec[2]
    # return results
    return spoint, trgepc, srfvec


@wraparound(False)
@boundscheck(False)
cpdef subslr(
    method: str,
    target: str, 
    et: float, 
    fixref: str, 
    abcorr: str, 
    obsrvr: str):
    # convert strings 
    cdef const char * _method = method
    cdef const char * _target = target
    cdef const char * _fixref = fixref
    cdef const char * _abcorr = abcorr
    cdef const char * _obsrvr = obsrvr
    # Allocate output floats and arrays with appropriate shapes.
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] spoint = np.empty(3, dtype=np.double)
    cdef double[:] _spoint = spoint
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] srfvec = np.empty(3, dtype=np.double)
    cdef double[:] _srfvec = srfvec
    cdef double trgepc
    cdef double[3] c_spoint
    cdef double[3] c_srfvec
    # perform the call
    subslr_c(
        _method,
        _target,
        et,
        _fixref,
        _abcorr,
        _obsrvr,
        c_spoint,
        &trgepc,
        c_srfvec
        )
     # accumulate the results to output arrays
    _spoint[0] = c_spoint[0]
    _spoint[1] = c_spoint[1]
    _spoint[2] = c_spoint[2]
    _srfvec[0] = c_srfvec[0]
    _srfvec[1] = c_srfvec[1]
    _srfvec[2] = c_srfvec[2]
    # return results
    return spoint, trgepc, srfvec


@boundscheck(False)
@wraparound(False)
cpdef subslr_v(
    method: str,
    target: str, 
    ets: double[:], 
    fixref: str, 
    abcorr: str, 
    obsrvr: str):
    # get size of input array
    cdef Py_ssize_t i, n = ets.shape[0]
    # convert strings 
    cdef const char * _method = method
    cdef const char * _target = target
    cdef const char * _fixref = fixref
    cdef const char * _abcorr = abcorr
    cdef const char * _obsrvr = obsrvr
    # Allocate output floats and arrays with appropriate shapes.
    cdef np.ndarray[dtype=DOUBLE_t, ndim=2, mode="c"] spoint = np.empty((n,3), dtype=np.double)
    cdef double[:,:] _spoint = spoint
    cdef np.ndarray[dtype=DOUBLE_t, ndim=2, mode="c"] srfvec = np.empty((n,3), dtype=np.double)
    cdef double[:,:] _srfvec = srfvec
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] trgepc = np.empty(n, dtype=np.double)
    cdef double[:] _trgepc = trgepc
    cdef double c_trgepc
    cdef double[3] c_spoint
    cdef double[3] c_srfvec
    # perform the call
    for i in range(n):
        subslr_c(
            _method,
            _target,
            ets[i],
            _fixref,
            _abcorr,
            _obsrvr,
            c_spoint,
            &c_trgepc,
            c_srfvec
            )
        # accumulate the results to output arrays
        _spoint[i, 0] = c_spoint[0]
        _spoint[i, 1] = c_spoint[1]
        _spoint[i, 2] = c_spoint[2]
        _trgepc[i] = c_trgepc
        _srfvec[i, 0] = c_srfvec[0]
        _srfvec[i, 1] = c_srfvec[1]
        _srfvec[i, 2] = c_srfvec[2]
    # return results
    return spoint, trgepc, srfvec

@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[DOUBLE_t, ndim=2] sxform(str fromstring, str tostring, double et):
    cdef double[6][6] tform 
    cdef const char * _fromstring = fromstring
    cdef const char * _tostring = tostring
    # initialize output
    cdef np.ndarray[dtype=DOUBLE_t, ndim=2, mode="c"] xform = np.empty((6, 6), dtype=np.double)
    cdef double[:,:] _xform = xform
    sxform_c(_fromstring, _tostring, et, tform)
    _xform[:,:] = tform
    return xform


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[DOUBLE_t, ndim=3] sxform_v(str fromstring, str tostring, double[:] ets):
    cdef double[:] c_ets = ets
    cdef Py_ssize_t i, n = c_ets.shape[0]
    cdef double[6][6] tform
    cdef const char * _fromstring = fromstring
    cdef const char * _tostring = tostring
    # initialize output
    cdef np.ndarray[dtype=DOUBLE_t, ndim=3, mode="c"] xform = np.empty((n, 6, 6), dtype=np.double)
    cdef double[:,:,::1] _xform = xform
    for i in range(n):
        sxform_c(_fromstring, _tostring, c_ets[i], tform)
        _xform[i,:,:] = tform
    return xform

# T

@wraparound(False)
@boundscheck(False)
cpdef tangpt(
    method: str,
    target: str,
    et: float,
    fixref: str,
    abcorr: str,
    corloc: str,
    obsrvr: str,
    dref: str,
    dvec: double[:]
    ):
    # convert strings 
    cdef const char * _method = method
    cdef const char * _target = target
    cdef const char * _fixref = fixref
    cdef const char * _abcorr = abcorr
    cdef const char * _corloc = corloc
    cdef const char * _obsrvr = obsrvr
    cdef const char * _dref   = dref
    # convert dvec to c
    cdef double[3] _dvec
    _dvec[0] = dvec[0]
    _dvec[1] = dvec[1]
    _dvec[2] = dvec[2]
    # Allocate output floats and arrays with appropriate shapes.
    cdef double alt, vrange, trgepc
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] tanpt = np.empty(3, dtype=np.double)
    cdef double[:] _tanpt = tanpt
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] srfpt = np.empty(3, dtype=np.double)
    cdef double[:] _srfpt = srfpt
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] srfvec = np.empty(3, dtype=np.double)
    cdef double[:] _srfvec = srfvec
    cdef double[3] c_tanpt
    cdef double[3] c_srfpt
    cdef double[3] c_srfvec
    # perform the call
    tangpt_c(
        _method, 
        _target, 
        et, 
        _fixref, 
        _abcorr,
        _corloc,
        _obsrvr,
        _dref,
        _dvec,
        c_tanpt,
        &alt,
        &vrange,
        c_srfpt,
        &trgepc,
        c_srfvec
    )
    # accumulate the results to output arrays
    _tanpt[0] = c_tanpt[0]
    _tanpt[1] = c_tanpt[1]
    _tanpt[2] = c_tanpt[2]
    _srfpt[0] = c_srfpt[0]
    _srfpt[1] = c_srfpt[1]
    _srfpt[2] = c_srfpt[2]
    _srfvec[0] = c_srfvec[0]
    _srfvec[1] = c_srfvec[1]
    _srfvec[2] = c_srfvec[2]
    # return values
    return tanpt, alt, vrange, srfpt, trgepc, srfvec


@boundscheck(False)
@wraparound(False)
cpdef tangpt_v(    
    method: str,
    target: str,
    ets: double[:],
    fixref: str,
    abcorr: str,
    corloc: str,
    obsrvr: str,
    dref: str,
    dvec: double[:]):
    # allocate sizes
    cdef Py_ssize_t i, n = ets.shape[0]
    # get memoryview of ets TODO not sure if this works
    cdef const double[:] _ets = ets
    # convert strings to ascii
    cdef const char *_method = method
    cdef const char *_target = target
    cdef const char *_fixref = fixref
    cdef const char *_abcorr = abcorr
    cdef const char *_corloc = corloc
    cdef const char *_obsrvr = obsrvr
    cdef const char *_dref   = dref
    # convert dvec to c TODO vectorize also over this?
    cdef double[3] _dvec
    _dvec[0] = dvec[0]
    _dvec[1] = dvec[1]
    _dvec[2] = dvec[2]
    # Allocate output floats and arrays with appropriate shapes.
    cdef np.ndarray[dtype=DOUBLE_t, ndim=2, mode="c"] tanpt  = np.empty((n,3), dtype=np.double)
    cdef double[:,:] _tanpt = tanpt
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] alt    = np.empty(n, dtype=np.float64)
    cdef double[:] _alt = alt
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] vrange = np.empty(n, dtype=np.float64)
    cdef double[:] _vrange = vrange
    cdef np.ndarray[dtype=DOUBLE_t, ndim=2, mode="c"] srfpt  = np.empty((n,3), dtype=np.double)
    cdef double[:,:] _srfpt = srfpt
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] trgepc = np.empty(n, dtype=np.float64)
    cdef double[:] _trgepc = trgepc
    cdef np.ndarray[dtype=DOUBLE_t, ndim=2, mode="c"] srfvec = np.empty((n,3), dtype=np.double)
    cdef double[:,:] _srfvec = srfvec
    cdef double[3] c_tanpt
    cdef double[3] c_srfpt
    cdef double[3] c_srfvec
    cdef double c_alt, c_range, c_trgepc
    # perform the calls
    for i in range(n):
        tangpt_c(
            _method, 
            _target, 
            _ets[i], 
            _fixref, 
            _abcorr,
            _corloc,
            _obsrvr,
            _dref,
            _dvec,
            c_tanpt,
            &c_alt,
            &c_range,
            c_srfpt,
            &c_trgepc,
            c_srfvec
        )
        # accumulate the results in output arrays
        _tanpt[i, 0] = c_tanpt[0]
        _tanpt[i, 1] = c_tanpt[1]
        _tanpt[i, 2] = c_tanpt[2]
        _alt[i]    = c_alt
        _vrange[i]  = c_range
        _srfpt[i, 0] = c_srfpt[0]
        _srfpt[i, 1] = c_srfpt[1]
        _srfpt[i, 2] = c_srfpt[2]
        _trgepc[i] = c_trgepc
        _srfvec[i, 0] = c_srfvec[0]
        _srfvec[i, 1] = c_srfvec[1]
        _srfvec[i, 2] = c_srfvec[2]
    # return values
    return tanpt, alt, range, srfpt, trgepc, srfvec


cpdef str timout(et: float, pictur: str):
    cdef const char * _pictur = pictur 
    cdef char[_default_len_out] c_buffer
    timout_c(et, _pictur, _default_len_out, c_buffer)
    return PyUnicode_DecodeUTF8(c_buffer, strlen(c_buffer), "strict")


@boundscheck(False)
@wraparound(False)
cpdef list[str] timout_v(double[:] ets, str pictur):
    cdef Py_ssize_t i, n = ets.shape[0]
    cdef const char * _pictur = pictur 
    cdef char[_default_len_out] c_buffer
     # initialize output
    cdef list output = [None] * n
    for i in range(n):
        timout_c(ets[i], _pictur, _default_len_out, c_buffer)
        output[i] = PyUnicode_DecodeUTF8(c_buffer, strlen(c_buffer), "strict")
    return output


cpdef double trgsep(et: float, targ1: str, shape1: str, frame1: str, targ2: str, shape2: str, frame2: str, obsrvr: str, abcorr: str):
    cdef SpiceDouble _et = et
    cdef const char* _targ1   = targ1
    cdef const char* _shape1  = shape1
    cdef const char* _frame1  = frame1
    cdef const char* _targ2   = targ2
    cdef const char* _shape2  = shape2
    cdef const char* _frame2  = frame2
    cdef const char* _obsrvr  = obsrvr
    cdef const char* _abcorr  = abcorr
    return trgsep_c(_et, _targ1, _shape1, _frame1, _targ2, _shape2, _frame2, _obsrvr, _abcorr)


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[DOUBLE_t, ndim=1] trgsep_v(ets: double[:], targ1: str, shape1: str, frame1: str, targ2: str, shape2: str, frame2: str, obsrvr: str, abcorr: str):
    cdef SpiceDouble _angsep
    cdef Py_ssize_t i, n = ets.shape[0] 
    cdef const char* _targ1   = targ1
    cdef const char* _shape1  = shape1
    cdef const char* _frame1  = frame1
    cdef const char* _targ2   = targ2
    cdef const char* _shape2  = shape2
    cdef const char* _frame2  = frame2
    cdef const char* _obsrvr  = obsrvr
    cdef const char* _abcorr  = abcorr
    # initialize output
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1] angseps = np.empty(n, dtype=np.double)
    cdef double[:] _angseps = angseps
    for i in range(n):
        _angsep = trgsep_c(ets[i], _targ1, _shape1, _frame1, _targ2, _shape2, _frame2, _obsrvr, _abcorr)
        _angseps[i] = _angsep  
    return angseps
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
cpdef np.ndarray[DOUBLE_t, ndim=1] unitim_v(
        double[:] epochs,
        insys: str,
        outsys: str,
    ):
    cdef Py_ssize_t i, n = epochs.shape[0]
    cdef double _unitim
    cdef const char * _insys = insys
    cdef const char * _outsys = outsys
    # initialize output
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1] unitims = np.empty(n, dtype=np.double)
    cdef double[:] _unitims = unitims
    for i in range(n):
        _unitim = unitim_c(epochs[i], _insys, _outsys)
        _unitims[i] = _unitim
    return unitims


cpdef void unload(file: str) noexcept:
    cdef const char* _file = file
    unload_c(_file)


cpdef double utc2et(utcstr: str):
    cdef const char* _utcstr = utcstr
    cdef double et
    utc2et_c(_utcstr, &et)
    return et


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[DOUBLE_t, ndim=1] utc2et_v(np.ndarray utcstr):
    cdef Py_ssize_t i, n = utcstr.shape[0]
    cdef double et
    # initialize output
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1] p_ets = np.empty(n, dtype=np.double)
    cdef double[:] c_ets = p_ets
    for i in range(n):
        utc2et_c(utcstr[i], &et)
        c_ets[i] = et
    return p_ets
