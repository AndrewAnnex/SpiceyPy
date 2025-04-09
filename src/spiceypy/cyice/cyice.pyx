# cython: language_level = 3
# cython: embedsignature = True
# cython: c_string_type = bytes
# cython: c_string_encoding = utf-8
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION
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

ctypedef fused double_arr_t:
   np.double_t[:]
   np.double_t[::1]

ctypedef fused int_arr_t:
   np.uint64_t[:]
   np.uint64_t[::1]

ctypedef fused char_arr_t:
   np.uint8_t[:]
   np.uint8_t[::1]

ctypedef fused bool_arr_t:
   np.uint8_t[:]
   np.uint8_t[::1]



from .cyice cimport *


#B

cpdef double b1900() noexcept:
    """
    Return the Julian Date corresponding to Besselian Date 1900.0.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/b1900_c.html

    :return: The Julian Date corresponding to Besselian Date 1900.0.
    """
    return b1900_c()


cpdef double b1950() noexcept:
    """
    Return the Julian Date corresponding to Besselian Date 1950.0.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/b1950_c.html

    :return: The Julian Date corresponding to Besselian Date 1950.0.
    """
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
    """
    Get pointing (attitude) for a specified spacecraft clock time.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckgp_c.html

    :param inst: NAIF ID of instrument, spacecraft, or structure.
    :param sclkdp: Encoded spacecraft clock time.
    :param tol: Time tolerance.
    :param ref: Reference frame.
    :return:
            C-matrix pointing data,
            Output encoded spacecraft clock time
    """
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


@boundscheck(False)
@wraparound(False)
cpdef ckgpav(
        inst: int,
        sclkdp: double,
        tol: double,
        ref: str
    ):
    """
    Get pointing (attitude) and angular velocity
    for a specified spacecraft clock time.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckgpav_c.html

    :param inst: NAIF ID of instrument, spacecraft, or structure.
    :param sclkdp: Encoded spacecraft clock time.
    :param tol: Time tolerance.
    :param ref: Reference frame.
    :return:
            C-matrix pointing data,
            Angular velocity vector,
            Output encoded spacecraft clock time.
    """
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
    cdef np.double_t[:,::1] c_cmat = np.empty((3,3), dtype=np.double)
    cdef np.double_t[::1] c_av = np.empty(3, dtype=np.double)
    # perform the call
    ckgpav_c(
        c_inst,
        c_sclkdp,
        c_tol,
        c_ref,
        _c_cmat, # todo attempt to avoid extra c array with memoryview
        &c_av[0],
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
    return c_cmat, c_av, c_clkout, c_found


cpdef double convrt(double x, str inunit, str outunit):
    """
    Take a measurement X, the units associated with
    X, and units to which X should be converted; return Y
    the value of the measurement in the output units.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/convrt_c.html

    :param x: Number representing a measurement in some units.
    :param inunit: The units in which x is measured.
    :param outunit: Desired units for the measurement.
    :return: The measurment in the desired units.
    """
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
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.convrt`

    Take measurements X, the units associated with each
    X, and units to which each X should be converted; return Y
    the values of the measurements in the output units.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/convrt_c.html

    :param x: Numbers representing a measurement in some units.
    :param inunit: The units in which x is measured.
    :param outunit: Desired units for the measurement.
    :return: The measurment in the desired units.
    """
    cdef Py_ssize_t i, n = x.shape[0]
    cdef const char * c_inunit = inunit
    cdef const char * c_outunit = outunit
    cdef np.double_t[::1] c_outs = np.empty(n, dtype=np.double)
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
    """
    Return the value of Delta ET (ET-UTC) for an input epoch.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/deltet_c.html

    :param epoch: Input epoch (seconds past J2000).
    :param eptype: Type of input epoch ("UTC" or "ET").
    :return: Delta ET (ET-UTC) at input epoch.
    """
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
cpdef double[::1] deltet_v(
    double[::1] epochs, 
    str eptype
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.deltet`

    Return the values of Delta ET (ET-UTC) for all input epochs.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/deltet_c.html

    :param epochs: Input epoch (seconds past J2000).
    :param eptype: Type of input epoch ("UTC" or "ET").
    :return: Delta ET (ET-UTC) at input epoch.
    """
    cdef Py_ssize_t i, n = epochs.shape[0]
    cdef const char* c_eptype = eptype
    # allocate output array
    cdef np.double_t[::1] deltas = np.empty(n, dtype=np.double)
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
    """
    Given an ephemeris epoch, compute the local solar time for
    an object on the surface of a body at a specified longitude.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/et2lst_c.html

    :param et: Epoch in seconds past J2000 epoch.
    :param body: ID-code of the body of interest.
    :param lon: Longitude of surface point (RADIANS).
    :param typein: Type of longitude "PLANETOCENTRIC", etc.
    :param timlen: Available room in output time string.
    :param ampmlen: Available room in output ampm string.
    :return:
            Local hour on a "24 hour" clock,
            Minutes past the hour,
            Seconds past the minute,
            String giving local time on 24 hour clock,
            String giving time on A.M. / P.M. scale.
    """
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
   ets: double[::1],
   body: int,
   lon: double,
   typein: str
):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.et2lst`

    Given ephemeris epochs, compute the local solar time for
    an object on the surface of a body at a specified longitude.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/et2lst_c.html

    :param ets: Epochs in seconds past J2000 epoch.
    :param body: ID-code of the body of interest.
    :param lon: Longitude of surface point (RADIANS).
    :param typein: Type of longitude "PLANETOCENTRIC", etc.
    :param timlen: Available room in output time string.
    :param ampmlen: Available room in output ampm string.
    :return:
            Local hour on a "24 hour" clock,
            Minutes past the hour,
            Seconds past the minute,
            String giving local time on 24 hour clock,
            String giving time on A.M. / P.M. scale.
    """
    cdef double[:] c_ets = ets
    cdef Py_ssize_t i, n = c_ets.shape[0]
    cdef char[_default_len_out] time
    cdef char[_default_len_out] ampm
    cdef const char * c_typein = typein
    cdef int c_body = body
    cdef double c_lon = lon
    # initialize output arrays 
    cdef int[::1] c_hrs = np.empty(n, dtype=np.int)
    cdef int[::1] c_mns = np.empty(n, dtype=np.int)
    cdef int[::1] c_scs = np.empty(n, dtype=np.int)
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


cpdef str et2utc(
    et: float, 
    format_str: str, 
    prec: int
):
    """
    Convert an input time from ephemeris seconds past J2000
    to Calendar, Day-of-Year, or Julian Date format, UTC.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/et2utc_c.html

    :param et: Input epoch, given in ephemeris seconds past J2000.
    :param format_str: Format of output epoch.
    :param prec: Digits of precision in fractional seconds or days.
    :param lenout: The length of the output string plus 1.
    :return: Output time string in UTC
    """
    cdef char[TIMELEN] c_buffer
    cdef const char* c_format_str = format_str
    et2utc_c(
        et, 
        c_format_str, 
        prec, 
        TIMELEN, 
        c_buffer
    ) # TODO or &c_buffer[0]?
    return PyUnicode_DecodeUTF8(c_buffer, strlen(c_buffer), "strict")


@boundscheck(False)
@wraparound(False)
cpdef et2utc_v(double[::1] ets, str format_str, int prec):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.et2utc`

    Convert an input time from ephemeris seconds past J2000
    to Calendar, Day-of-Year, or Julian Date format, UTC.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/et2utc_c.html

    :param ets: Input epochs, given in ephemeris seconds past J2000.
    :param format_str: Format of output epoch.
    :param prec: Digits of precision in fractional seconds or days.
    :param lenout: The length of the output string plus 1.
    :return: Output time string in UTC
    """
    cdef char[TIMELEN] c_buffer
    cdef Py_ssize_t i, n, fixed_length
    cdef double[::1] c_ets = ets
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
    """
    Convert from an ephemeris epoch measured in seconds past
    the epoch of J2000 to a calendar string format using a
    formal calendar free of leapseconds.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/etcal_c.html

    :param et: Ephemeris time measured in seconds past J2000 TDB.
    :return: A standard calendar representation of et.
    """
    cdef char[TIMELEN] c_buffer
    etcal_c(et, TIMELEN, &c_buffer[0])
    # Convert the C char* to a Python string
    return PyUnicode_DecodeUTF8(c_buffer, strlen(c_buffer), "strict")


@boundscheck(False)
@wraparound(False)
cpdef etcal_v(double[::1] ets):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.etcal`

    Convert from an ephemeris epoch measured in seconds past
    the epoch of J2000 to a calendar string format using a
    formal calendar free of leapseconds.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/etcal_c.html

    :param ets: Ephemeris times measured in seconds past J2000 TDB.
    :return: A standard calendar representation of et.
    """
    cdef Py_ssize_t i, n = ets.shape[0]
    # Allocate a 2D buffer of shape (n, 24) with dtype np.uint8
    cdef np.ndarray[dtype=CHAR_t, ndim=2] results = np.empty((n, 25), dtype=np.uint8)
    # Create a typed memoryview over the buffer
    cdef unsigned char[:, :] view = results
    for i in prange(n, nogil=True):
        # Get a pointer to the start of the i-th row and call etcal_c
        etcal_c(
            ets[i], 
            25, 
            <char*> &view[i, 0]
        )
    # Convert the buffer to a 1D array of fixed-length byte strings (dtype "|S25") (need extra byte for termination)
    return results.view(dtype="|S25").reshape(n) #.astype(np.str_) this converts it to a more usable dtype but adds overhead

# F

cpdef int failed() noexcept:
    """
    True if an error condition has been signalled via sigerr_c.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/failed_c.html

    :return: a boolean
    """
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
    """
    Determine if a specified ray is within the field-of-view (FOV) of a
    specified instrument at a given time.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/fovray_c.html

    :param inst: Name or ID code string of the instrument.
    :param raydir: Ray's direction vector.
    :param rframe: Body-fixed, body-centered frame for target body.
    :param abcorr: Aberration correction flag.
    :param observer: Name or ID code string of the observer.
    :param et: Time of the observation (seconds past J2000).
    :return: Visibility flag
    """
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
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.fovray`

    Determine if a specified ray is within the field-of-view (FOV) of a
    specified instrument at a given time.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/fovray_c.html

    :param inst: Name or ID code string of the instrument.
    :param raydir: Ray's direction vector.
    :param rframe: Body-fixed, body-centered frame for target body.
    :param abcorr: Aberration correction flag.
    :param observer: Name or ID code string of the observer.
    :param ets: Times of the observation (seconds past J2000).
    :return: Visibility flags
    """
    # initialize c variables
    cdef Py_ssize_t i, n = ets.shape[0]
    # convert the strings to pointers once
    cdef const char* c_inst     = inst
    cdef const char* c_rframe   = rframe
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsrvr   = obsrvr
    # initialize output arrays
    cdef bint[::1] c_visibl = np.empty(n, dtype=np.uint8)
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
    """
    Determine if a specified ephemeris object is within the field-of-view (FOV)
    of a specified instrument at a given time.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/fovtrg_c.html

    :param inst: Name or ID code string of the instrument.
    :param target: Name or ID code string of the target.
    :param tshape: Type of shape model used for the target.
    :param tframe: Body-fixed, body-centered frame for target body.
    :param abcorr: Aberration correction flag.
    :param observer: Name or ID code string of the observer.
    :param et: Time of the observation (seconds past J2000).
    :return: Visibility flag
    """
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
    str inst,
    str target,
    str tshape,
    str tframe,
    str abcorr,
    str obsrvr,
    np.double_t[::1] ets
):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.fovtrg`

    Determine if a specified ephemeris object is within the field-of-view (FOV)
    of a specified instrument at a given time.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/fovtrg_c.html

    :param inst: Name or ID code string of the instrument.
    :param target: Name or ID code string of the target.
    :param tshape: Type of shape model used for the target.
    :param tframe: Body-fixed, body-centered frame for target body.
    :param abcorr: Aberration correction flag.
    :param observer: Name or ID code string of the observer.
    :param ets: Times of the observation (seconds past J2000).
    :return: Visibility flags
    """
    # initialize c variables
    cdef Py_ssize_t i, n = ets.shape[0]
    # convert the strings to pointers once
    cdef const char* c_inst     = inst
    cdef const char* c_target   = target
    cdef const char* c_tshape   = tshape
    cdef const char* c_tframe   = tframe
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsrvr   = obsrvr
    # initialize output arrays
    cdef bint[::1] c_visibl = np.empty(n, dtype=np.uint8)
    # perform the call
    for i in range(n):
        fovtrg_c(
            c_inst,
            c_target,
            c_tshape,
            c_tframe,
            c_abcorr,
            c_obsrvr,
            &ets[i],
            &c_visibl[i]
        )
    # return
    return c_visibl


cpdef void furnsh(file: str):
    """
    Load one or more SPICE kernels into a program.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/furnsh_c.html

    :param path: one or more paths to kernels
    """
    cdef const char* _file = file
    furnsh_c(_file)
    

# G
cpdef str getmsg(str option, int msglen):
    """
    Retrieve the current short error message,
    the explanation of the short error message, or the
    long error message.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/getmsg_c.html

    :param option: Indicates type of error message.
    :param lenout: Available space in the output string msg.
    :return: The error message to be retrieved.
    """
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

cpdef double lspcn(
    body: str, 
    et: double, 
    abcorr: str
    ):
    """
    Compute L_s, the planetocentric longitude of the sun, as seen
    from a specified body.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lspcn_c.html

    :param body: Name of central body.
    :param et: Epoch in seconds past J2000 TDB.
    :param abcorr: Aberration correction.
    :return: planetocentric longitude of the sun in radians
    """
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
cpdef np.double_t[::1] lspcn_v(
    str body, 
    np.double_t[::1] ets, 
    str abcorr
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.lspcn`

    Compute L_s, the planetocentric longitude of the sun, as seen
    from a specified body.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lspcn_c.html

    :param body: Name of central body.
    :param ets: Epochs in seconds past J2000 TDB.
    :param abcorr: Aberration correction.
    :return: planetocentric longitudes of the sun in radians
    """
    cdef Py_ssize_t i, n = ets.shape[0]
    cdef const char * _body   = body
    cdef const char * _abcorr = abcorr
    cdef np.double_t[::1] l_s_s = np.empty(n, dtype=np.double)
    for i in range(n):
        l_s_s[i] = lspcn_c(
            _body, 
            ets[i], 
            _abcorr
        )
    return  l_s_s

#M 

#N 

#O 

#P 

# Q

cpdef str qcktrc(int tracelen):
    """
    Return a string containing a traceback.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/qcktrc_c.html

    :param tracelen: Maximum length of output traceback string.
    :return: A traceback string.
    """
    cdef char * _tracestr = <char *> malloc((tracelen) * sizeof(char))
    qcktrc_c(tracelen, _tracestr)
    pytracestr = <unicode> _tracestr
    free(_tracestr)
    return pytracestr

# R


cpdef void reset() noexcept:
    """
    Reset the SPICE error status to a value of "no error."
    As a result, the status routine, failed, will return a value
    of False

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/reset_c.html

    """
    reset_c()

#S

cpdef str scdecd(sc: int, sclkdp: float):
    """
    Convert double precision encoding of spacecraft clock time into
    a character representation.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scdecd_c.html

    :param sc: NAIF spacecraft identification code.
    :param sclkdp: Encoded representation of a spacecraft clock count.
    :return: Character representation of a clock count.
    """
    cdef SpiceInt _sc = sc
    cdef char[_default_len_out] c_buffer 
    scdecd_c(_sc, sclkdp, _default_len_out, c_buffer)
    return PyUnicode_DecodeUTF8(c_buffer, strlen(c_buffer), "strict")


@boundscheck(False)
@wraparound(False)
cpdef list[str] scdecd_v(sc: int, sclkdps: double[::1]):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.scdecd`

    Convert double precision encoding of spacecraft clock time into
    a character representation.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scdecd_c.html

    :param sc: NAIF spacecraft identification code.
    :param sclkdps: Encoded representations of a spacecraft clock count.
    :return: Character representation of a clock count.
    """
    cdef SpiceInt _sc = sc
    cdef Py_ssize_t i, length, n = sclkdps.shape[0]
    cdef double[:] _sclkdps = sclkdps
    cdef char[_default_len_out] c_buffer 
    cdef list sclkchs = [None] * n
    scdecd_c(_sc, sclkdps[0], _default_len_out, &c_buffer[0])
    length = strlen(c_buffer)
    sclkchs[0] = PyUnicode_DecodeUTF8(c_buffer, length, "strict") 
    if n > 1:
        for i in range(1, n):
            scdecd_c(
                _sc, 
                _sclkdps[i], 
                _default_len_out, 
                &c_buffer[0]
            )
            sclkchs[i] = PyUnicode_DecodeUTF8(c_buffer, length, "strict")
    return sclkchs


cpdef double scencd(sc: int, sclkch: str):
    """
    Encode character representation of spacecraft clock time into a
    double precision number.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scencd_c.html

    :param sc: NAIF spacecraft identification code.
    :param sclkch: Character representation of a spacecraft clock.
    :return: Encoded representation of the clock count.
    """
    cdef SpiceInt c_sc = sc
    cdef double sclkdp
    cdef const char * c_sclkch = sclkch
    scencd_c(
        c_sc, 
        c_sclkch, 
        &sclkdp
    )
    return sclkdp


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[DOUBLE_t, ndim=1] scencd_v(sc: int, sclkchs: list[str]):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.scencd`

    Encode character representation of spacecraft clock time into a
    double precision number.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scencd_c.html

    :param sc: NAIF spacecraft identification code.
    :param sclkchs: Character representations of a spacecraft clock.
    :return: Encoded representations of the clock count.
    """
    cdef SpiceInt c_sc = sc
    cdef Py_ssize_t n, i
    n = len(sclkchs)
    cdef np.double_t[::1] c_sclkdps  = np.empty(n, dtype=np.double)
    for i in range(n):
        scencd_c(
            c_sc, 
            sclkchs[i], 
            &c_sclkdps[i]
        )
    return c_sclkdps


cpdef double sce2c(sc: int, et: float):
    """
    Convert ephemeris seconds past J2000 (ET) to continuous encoded
    spacecraft clock "ticks".  Non-integral tick values may be
    returned.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sce2c_c.html

    :param sc: NAIF spacecraft ID code.
    :param et: Ephemeris time, seconds past J2000 TDB.
    :return:
            SCLK, encoded as ticks since spacecraft clock start.
            sclkdp need not be integral.
    """
    cdef SpiceInt c_sc = sc
    cdef double sclkdp
    sce2c_c(
        c_sc, 
        et, 
        &sclkdp
    )
    return sclkdp


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[DOUBLE_t, ndim=1] sce2c_v(
    int sc, 
    double[::1] ets
):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.sce2c`

    Convert ephemeris seconds past J2000 (ET) to continuous encoded
    spacecraft clock "ticks".  Non-integral tick values may be
    returned.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sce2c_c.html

    :param sc: NAIF spacecraft ID code.
    :param ets: Ephemeris times, seconds past J2000 TDB.
    :return:
            SCLK, encoded as ticks since spacecraft clock start.
            sclkdp need not be integral.
    """
    cdef Py_ssize_t i, n = ets.shape[0]
    cdef SpiceInt c_sc = sc
    cdef np.double_t[::1] sclkdps = np.empty(n, dtype=np.double)
    for i in range(n):
        sce2c_c(
            c_sc, 
            ets[i], 
            &sclkdps[i]
        )
    return sclkdps


cpdef double sce2s(
    int sc, 
    double et
    ):
    """
    Convert an epoch specified as ephemeris seconds past J2000 (ET) to a
    character string representation of a spacecraft clock value (SCLK).

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sce2s_c.html

    :param sc: NAIF spacecraft clock ID code.
    :param et: Ephemeris time, specified as seconds past J2000 TDB.
    :return: An SCLK string.
    """
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
cpdef list[str] sce2s_v(
    int sc, 
    double[::1] ets
):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.sce2s`

    Convert an epoch specified as ephemeris seconds past J2000 (ET) to a
    character string representation of a spacecraft clock value (SCLK).

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sce2s_c.html

    :param sc: NAIF spacecraft clock ID code.
    :param ets: Ephemeris times, specified as seconds past J2000 TDB.
    :param lenout: Maximum length of output string.
    :return: An SCLK string.
    """
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
    """
    Convert a spacecraft clock string to ephemeris seconds past J2000 (ET).

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scs2e_c.html

    :param sc: NAIF integer code for a spacecraft.
    :param sclkch: An SCLK string.
    :return: Ephemeris time, seconds past J2000.
    """
    cdef double et
    cdef const char * _sclkch = sclkch
    scs2e_c(sc, _sclkch, &et)
    return et


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[DOUBLE_t, ndim=1] scs2e_v(sc: long, sclkchs: np.ndarray):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.scs2e`

    Convert a spacecraft clock string to ephemeris seconds past J2000 (ET).

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scs2e_c.html

    :param sc: NAIF integer code for a spacecraft.
    :param sclkchs: SCLK strings.
    :return: Ephemeris time, seconds past J2000.
    """
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
    """
    Convert encoded spacecraft clock ("ticks") to ephemeris
    seconds past J2000 (ET).

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sct2e_c.html

    :param sc: NAIF spacecraft ID code.
    :param sclkdp: SCLK, encoded as ticks since spacecraft clock start.
    :return: Ephemeris time, seconds past J2000.
    """
    cdef SpiceInt _sc = sc
    cdef double et
    sct2e_c(_sc, sclkdp, &et)
    return et


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[DOUBLE_t, ndim=1] sct2e_v(long sc, double[::1] sclkdps):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.sct2e`

    Convert encoded spacecraft clock ("ticks") to ephemeris
    seconds past J2000 (ET).

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sct2e_c.html

    :param sc: NAIF spacecraft ID code.
    :param sclkdps: SCLKs, encoded as ticks since spacecraft clock start.
    :return: Ephemeris time, seconds past J2000.
    """
    cdef Py_ssize_t i, n = sclkdps.shape[0]
    cdef SpiceInt c_sc = sc
    cdef double[::1] c_ets = np.empty(n, dtype=np.double)
    for i in range(n):
        sct2e_c(
            c_sc, 
            sclkdps[i], 
            &c_ets[i]
        )
    return c_ets


@boundscheck(False)
@wraparound(False)
cpdef spkapo(
    int targ,  
    float et, 
    str ref,
    double[::1] sobs, 
    str abcorr
):
    """
    Return the position of a target body relative to an observer,
    optionally corrected for light time and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkapo_c.html

    :param targ: Target body.
    :param et: Observer epoch in seconds past J2000 TDB..
    :param ref: Inertial reference frame of observer's state.
    :param sobs: State of observer wrt. solar system barycenter.
    :param abcorr: Aberration correction flag.
    :return:
            Position of target in km,
            One way light time between observer and target in seconds.
    """
    # initialize c variables
    cdef double lt = 0.0
    # convert the strings to pointers once
    cdef const char* c_ref    = ref
    cdef const char* c_abcorr = abcorr
    cdef long c_targ = targ
    # initialize output arrays
    cdef double[::1] c_ptarg =  np.empty(3, dtype=np.double)
    spkapo_c(
        c_targ, 
        et, 
        c_ref, 
        &sobs[0],
        c_abcorr, 
        &c_ptarg[0], 
        &lt
    )
    return c_ptarg, lt


@boundscheck(False)
@wraparound(False)
cpdef spkapo_v(
    targ: int,  
    ets: double[::1], 
    ref: str,
    sobs: double[::1], 
    abcorr: str):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.spkapo`

    Return the position of a target body relative to an observer,
    optionally corrected for light time and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkapo_c.html

    :param targ: Target body.
    :param ets: Observer epochs in seconds past J2000 TDB..
    :param ref: Inertial reference frame of observer's state.
    :param sobs: State of observer wrt. solar system barycenter.
    :param abcorr: Aberration correction flag.
    :return:
            Position of target in km,
            One way light time between observer and target in seconds.
    """
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
    """
    Return the state (position and velocity) of a target body
    relative to an observing body, optionally corrected for light
    time (planetary aberration) and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkez_c.html

    :param target: Target body.
    :param et: Observer epoch in seconds past J2000 TDB.
    :param ref: Reference frame of output state vector.
    :param abcorr: Aberration correction flag.
    :param observer: Observing body.
    :return:
            State of target in km and km/sec,
            One way light time between observer and target in seconds.
    """
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
    double[::1] epochs, 
    str ref, 
    str abcorr, 
    int observer):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.spkez`

    Return the state (position and velocity) of a target body
    relative to an observing body, optionally corrected for light
    time (planetary aberration) and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkez_c.html

    :param target: Target body.
    :param epochs: Observer epoch in seconds past J2000 TDB.
    :param ref: Reference frame of output state vector.
    :param abcorr: Aberration correction flag.
    :param observer: Observing body.
    :return:
            State of target in km and km/sec,
            One way light time between observer and target in seconds.
    """
    # initialize c variables
    cdef Py_ssize_t i, n = epochs.shape[0]
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
                epochs[i], 
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
    """
    Return the position of a target body relative to an observing
    body, optionally corrected for light time (planetary aberration)
    and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkezp_c.html

    :param targ: Target body NAIF ID code.
    :param et: Observer epoch in seconds past J2000 TDB.
    :param ref: Reference frame of output position vector.
    :param abcorr: Aberration correction flag.
    :param obs: Observing body NAIF ID code.
    :return:
            Position of target in km,
            One way light time between observer and target in seconds.
    """
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
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.spkezp`

    Return the position of a target body relative to an observing
    body, optionally corrected for light time (planetary aberration)
    and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkezp_c.html

    :param targ: Target body NAIF ID code.
    :param ets: Observer epochs in seconds past J2000 TDB.
    :param ref: Reference frame of output position vector.
    :param abcorr: Aberration correction flag.
    :param obs: Observing body NAIF ID code.
    :return:
            Position of target in km,
            One way light time between observer and target in seconds.
    """
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
    """
    Return the state (position and velocity) of a target body
    relative to an observing body, optionally corrected for light
    time (planetary aberration) and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkezr_c.html

    :param target: Target body name.
    :param epoch: Observer epoch in seconds past J2000 TDB.
    :param frame: Reference frame of output state vector.
    :param abcorr: Aberration correction flag.
    :param observer: Observing body name.
    :return:
            State of target in km and km/sec,
            One way light time between observer and target in seconds.
    """
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
    double[::1] epochs, 
    str frame, 
    str abcorr, 
    str observer):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.spkezr`

    Return the state (position and velocity) of a target body
    relative to an observing body, optionally corrected for light
    time (planetary aberration) and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkezr_c.html

    :param target: Target body name.
    :param epochs: Observer epochs in seconds past J2000 TDB.
    :param frame: Reference frame of output state vector.
    :param abcorr: Aberration correction flag.
    :param observer: Observing body name.
    :return:
            State of target in km and km/sec,
            One way light time between observer and target in seconds.
    """
    # initialize c variables
    cdef double[6] state = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    cdef double lt = 0.0
    cdef Py_ssize_t i, n = epochs.shape[0]
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
            spkezr_c(_target, epochs[i], _frame, _abcorr, _observer, state, &lt)
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
    """
    Return the state of a specified target relative to an "observer,"
    where the observer has constant position in a specified reference
    frame. The observer's position is provided by the calling program
    rather than by loaded SPK files.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkcpo_c.html

    :param target: Name of target ephemeris object.
    :param et: Observation epoch in ephemeris seconds past J2000 TDB.
    :param outref: Reference frame of output state.
    :param refloc: Output reference frame evaluation locus.
    :param abcorr: Aberration correction.
    :param obspos: Observer position relative to center of motion.
    :param obsctr: Center of motion of observer.
    :param obsref: Frame of observer position.
    :return:
            State of target with respect to observer in km and km/sec,
            One way light time between target and observer.
    """
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
    ets: double[::1],
    outref: str,
    refloc: str,
    abcorr: str,
    obspos: double[::1], #TODO determine if to also vectorize this
    obsctr: str,
    obsref: str):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.spkcpo`
    
    Return the state of a specified target relative to an "observer,"
    where the observer has constant position in a specified reference
    frame. The observer's position is provided by the calling program
    rather than by loaded SPK files.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkcpo_c.html

    :param target: Name of target ephemeris object.
    :param ets: Observation epochs in ephemeris seconds past J2000 TDB.
    :param outref: Reference frame of output state.
    :param refloc: Output reference frame evaluation locus.
    :param abcorr: Aberration correction.
    :param obspos: Observer position relative to center of motion.
    :param obsctr: Center of motion of observer.
    :param obsref: Frame of observer position.
    :return:
            State of target with respect to observer in km and km/sec,
            One way light time between target and observer.
    """
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
    trgpos: double[::1],
    trgctr: str,
    trgref: str,
    et: float,
    outref: str,
    refloc: str,
    abcorr: str,
    obsrvr: str
):
    """
    Return the state, relative to a specified observer, of a target
    having constant position in a specified reference frame. The
    target's position is provided by the calling program rather than by
    loaded SPK files.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkcpt_c.html

    :param trgpos: Target position relative to center of motion.
    :param trgctr: Center of motion of target.
    :param trgref: Observation epoch.
    :param et: Observation epoch in ephemeris seconds past J2000 TDB.
    :param outref: Reference frame of output state.
    :param refloc: Output reference frame evaluation locus.
    :param abcorr: Aberration correction.
    :param obsrvr: Name of observing ephemeris object.
    :return:
            State of target with respect to observer in km and km/sec,
            One way light time between target and observer.
    """
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
    trgpos: double[::1],
    trgctr: str,
    trgref: str,
    ets: double[::1],
    outref: str,
    refloc: str,
    abcorr: str,
    obsrvr: str
):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.spkcpt`
    
    Return the state, relative to a specified observer, of a target
    having constant position in a specified reference frame. The
    target's position is provided by the calling program rather than by
    loaded SPK files.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkcpt_c.html

    :param trgpos: Target position relative to center of motion.
    :param trgctr: Center of motion of target.
    :param trgref: Observation epoch.
    :param ets: Observation epochs in ephemeris seconds past J2000 TDB.
    :param outref: Reference frame of output state.
    :param refloc: Output reference frame evaluation locus.
    :param abcorr: Aberration correction.
    :param obsrvr: Name of observing ephemeris object.
    :return:
            State of target with respect to observer in km and km/sec,
            One way light time between target and observer.
    """
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
    obssta: double[::1],
    obsepc: double,
    obsctr: str,
    obsref: str):
    """
    Return the state of a specified target relative to an "observer,"
    where the observer has constant velocity in a specified reference
    frame.  The observer's state is provided by the calling program
    rather than by loaded SPK files.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkcvo_c.html

    :param target: Name of target ephemeris object.
    :param et: Observation epoch in ephemeris seconds past J2000 TDB.
    :param outref: Reference frame of output state.
    :param refloc: Output reference frame evaluation locus.
    :param abcorr: Aberration correction.
    :param obssta: Observer state relative to center of motion.
    :param obsepc: Epoch of observer state.
    :param obsctr: Center of motion of observer.
    :param obsref: Frame of observer state.
    :return:
            State of target with respect to observer in km and km/sec,
            One way light time between target and observer.
    """
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
    ets: double[::1],
    outref: str,
    refloc: str,
    abcorr: str,
    obssta: double[::1], # TODO vectorize here?
    obsepc: double,    # TODO vectorize here?
    obsctr: str,
    obsref: str):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.spkcvo`
    
    Return the state of a specified target relative to an "observer,"
    where the observer has constant velocity in a specified reference
    frame.  The observer's state is provided by the calling program
    rather than by loaded SPK files.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkcvo_c.html

    :param target: Name of target ephemeris object.
    :param ets: Observation epochs in ephemeris seconds past J2000 TDB.
    :param outref: Reference frame of output state.
    :param refloc: Output reference frame evaluation locus.
    :param abcorr: Aberration correction.
    :param obssta: Observer state relative to center of motion.
    :param obsepc: Epoch of observer state.
    :param obsctr: Center of motion of observer.
    :param obsref: Frame of observer state.
    :return:
            State of target with respect to observer in km and km/sec,
            One way light time between target and observer.
    """
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
    """
    Return the state, relative to a specified observer, of a target
    having constant velocity in a specified reference frame. The
    target's state is provided by the calling program rather than by
    loaded SPK files.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkcvt_c.html

    :param trgsta: Target state relative to center of motion.
    :param trgepc: Epoch of target state.
    :param trgctr: Center of motion of target.
    :param trgref: Frame of target state.
    :param et: Observation epoch in ephemeris seconds past J2000 TDB.
    :param outref: Reference frame of output state.
    :param refloc: Output reference frame evaluation locus.
    :param abcorr: Aberration correction.
    :param obsrvr: Name of observing ephemeris object.
    :return:
            State of target with respect to observer in km and km/sec,
            One way light time between target and observer.
    """
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
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.spkcvt`
    
    Return the state, relative to a specified observer, of a target
    having constant velocity in a specified reference frame. The
    target's state is provided by the calling program rather than by
    loaded SPK files.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkcvt_c.html

    :param trgsta: Target state relative to center of motion.
    :param trgepc: Epoch of target state.
    :param trgctr: Center of motion of target.
    :param trgref: Frame of target state.
    :param ets: Observation epochs in ephemeris seconds past J2000 TDB.
    :param outref: Reference frame of output state.
    :param refloc: Output reference frame evaluation locus.
    :param abcorr: Aberration correction.
    :param obsrvr: Name of observing ephemeris object.
    :return:
            State of target with respect to observer in km and km/sec,
            One way light time between target and observer.
    """
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
    """
    Compute the geometric state (position and velocity) of a target
    body relative to an observing body.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkgeo_c.html

    :param targ: Target body.
    :param et: Target epoch.
    :param ref: Target reference frame.
    :param obs: Observing body.
    :return: 
        State of target in km and km/sec, 
        One way light time between observer and target in seconds.
    """
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
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.spkgeo`
    
    Compute the geometric state (position and velocity) of a target
    body relative to an observing body.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkgeo_c.html

    :param targ: Target body.
    :param ets: Target epochs.
    :param ref: Target reference frame.
    :param obs: Observing body.
    :return: 
        State of target in km and km/sec, 
        One way light time between observer and target in seconds.
    """
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
    """
    Compute the geometric position of a target body relative to an
    observing body.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkgps_c.html

    :param targ: Target body.
    :param et: Target epoch.
    :param ref: Target reference frame.
    :param obs: Observing body.
    :return: Position of target in km, Light time.
    """
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
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.spkgps`
    
    Compute the geometric position of a target body relative to an
    observing body.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkgps_c.html

    :param targ: Target body.
    :param ets: Target epochs.
    :param ref: Target reference frame.
    :param obs: Observing body.
    :return: Position of target in km, Light time.
    """
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
    """
    For a specified SPK segment and time, return the state (position and
    velocity) of the segment's target body relative to its center of
    motion.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkpvn_c.html

    :param handle: File handle.
    :param descr: Segment descriptor.
    :param et: Evaluation epoch.
    :return:
            Segment reference frame ID code,
            Output state vector,
            Center of state.
    """
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
    double[::1] ets
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.spkpvn`
    
    For a specified SPK segment and time, return the state (position and
    velocity) of the segment's target body relative to its center of
    motion.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkpvn_c.html

    :param handle: File handle.
    :param descr: Segment descriptor.
    :param ets: Evaluation epochs.
    :return:
            Segment reference frame ID code,
            Output state vector,
            Center of state.
    """
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
cpdef spkpos(
    str target, 
    double et, 
    str ref, 
    str abcorr, 
    str obs
):
    """
    Return the position of a target body relative to an observing
    body, optionally corrected for light time (planetary aberration)
    and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkpos_c.html

    :param targ: Target body name.
    :param et: Observer epoch in seconds past J2000 TDB.
    :param ref: Reference frame of output position vector.
    :param abcorr: Aberration correction flag.
    :param obs: Observing body name.
    :return:
            Position of target in km,
            One way light time between observer and target in seconds.
    """
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
cpdef spkpos_v(
    str targ, 
    double[::1] ets, 
    str ref, 
    str abcorr, 
    str obs
):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.spkpos`
    
    Return the position of a target body relative to an observing
    body, optionally corrected for light time (planetary aberration)
    and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkpos_c.html

    :param targ: Target body name.
    :param ets: Observer epochs in seconds past J2000 TDB.
    :param ref: Reference frame of output position vector.
    :param abcorr: Aberration correction flag.
    :param obs: Observing body name.
    :return:
            Position of target in km,
            One way light time between observer and target in seconds.
    """
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
    """
    Return the state (position and velocity) of a target body
    relative to the solar system barycenter.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkssb_c.html

    :param targ: Target body.
    :param et: Target epoch.
    :param ref: Target reference frame.
    :return: State of target.
    """
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
    ets: double[::1],
    ref: str,
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.spkssb`
    
    Return the state (position and velocity) of a target body
    relative to the solar system barycenter.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkssb_c.html

    :param targ: Target body.
    :param ets: Target epochs.
    :param ref: Target reference frame.
    :return: States of target.
    """
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
    """
    Convert a string representing an epoch to a double precision
    value representing the number of TDB seconds past the J2000
    epoch corresponding to the input epoch.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/str2et_c.html

    :param time: A string representing an epoch.
    :return: The equivalent value in seconds past J2000, TDB.
    """
    cdef double et
    cdef const char* _time = time
    str2et_c(_time, &et)
    return et
    

@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[DOUBLE_t, ndim=1] str2et_v(np.ndarray times):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.str2et`
    
    Convert a string representing an epoch to a double precision
    value representing the number of TDB seconds past the J2000
    epoch corresponding to the input epoch.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/str2et_c.html

    :param times: Strings representing an epoch.
    :return: The equivalent values in seconds past J2000, TDB.
    """
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
    dvec: double[::1]):
    """
    Given an observer and a direction vector defining a ray, compute
    the surface intercept of the ray on a target body at a specified
    epoch, optionally corrected for light time and stellar
    aberration.

    This routine supersedes :func:`srfxpt`.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sincpt_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param et: Epoch in ephemeris seconds past J2000 TDB.
    :param fixref: Body-fixed, body-centered target body frame.
    :param abcorr: Aberration correction.
    :param obsrvr: Name of observing body.
    :param dref: Reference frame of ray's direction vector.
    :param dvec: Ray's direction vector.
    :return:
            Surface intercept point on the target body in km,
            Intercept epoch,
            Vector from observer to intercept point in km.
    """
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
    ets: double[::1],
    fixref: str,
    abcorr: str,
    obsrvr: str,
    dref: str,
    dvec: double[::1]
):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.sincpt`
    
    Given an observer and a direction vector defining a ray, compute
    the surface intercept of the ray on a target body at a specified
    epoch, optionally corrected for light time and stellar
    aberration.

    This routine supersedes :func:`srfxpt`.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sincpt_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param ets: Epochs in ephemeris seconds past J2000 TDB.
    :param fixref: Body-fixed, body-centered target body frame.
    :param abcorr: Aberration correction.
    :param obsrvr: Name of observing body.
    :param dref: Reference frame of ray's direction vector.
    :param dvec: Ray's direction vector.
    :return:
            Surface intercept point on the target body in km,
            Intercept epoch,
            Vector from observer to intercept point in km.
    """
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
    obsrvr: str
):
    """
    Compute the rectangular coordinates of the sub-observer point on
    a target body at a specified epoch, optionally corrected for
    light time and stellar aberration.

    This routine supersedes :func:`subpt`.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/subpnt_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param et: Epoch in ephemeris seconds past J2000 TDB.
    :param fixref: Body-fixed, body-centered target body frame.
    :param abcorr: Aberration correction.
    :param obsrvr: Name of observing body.
    :return:
            Sub-observer point on the target body,
            Sub-observer point epoch,
            Vector from observer to sub-observer point.
    """
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
    ets: double[::1], 
    fixref: str, 
    abcorr: str, 
    obsrvr: str
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.subpnt`
    
    Compute the rectangular coordinates of the sub-observer point on
    a target body at a specified epoch, optionally corrected for
    light time and stellar aberration.

    This routine supersedes :func:`subpt`.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/subpnt_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param ets: Epochs in ephemeris seconds past J2000 TDB.
    :param fixref: Body-fixed, body-centered target body frame.
    :param abcorr: Aberration correction.
    :param obsrvr: Name of observing body.
    :return:
            Sub-observer point on the target body,
            Sub-observer point epoch,
            Vector from observer to sub-observer point.
    """
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
    cdef double[:,::1] _spoint = spoint
    cdef np.ndarray[dtype=DOUBLE_t, ndim=2, mode="c"] srfvec = np.empty((n,3), dtype=np.double)
    cdef double[:,::1] _srfvec = srfvec
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] trgepc = np.empty(n, dtype=np.double)
    cdef double[::1] _trgepc = trgepc
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
    obsrvr: str
):
    """
    Compute the rectangular coordinates of the sub-solar point on
    a target body at a specified epoch, optionally corrected for
    light time and stellar aberration.

    This routine supersedes subsol_c.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/subslr_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param et: Epoch in ephemeris seconds past J2000 TDB.
    :param fixref: Body-fixed, body-centered target body frame.
    :param abcorr: Aberration correction.
    :param obsrvr: Name of observing body.
    :return:
            Sub-solar point on the target body in km,
            Sub-solar point epoch,
            Vector from observer to sub-solar point in km.
    """
    # convert strings 
    cdef const char * _method = method
    cdef const char * _target = target
    cdef const char * _fixref = fixref
    cdef const char * _abcorr = abcorr
    cdef const char * _obsrvr = obsrvr
    # Allocate output floats and arrays with appropriate shapes.
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] spoint = np.empty(3, dtype=np.double)
    cdef double[::1] _spoint = spoint
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] srfvec = np.empty(3, dtype=np.double)
    cdef double[::1] _srfvec = srfvec
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
    ets: double[::1], 
    fixref: str, 
    abcorr: str, 
    obsrvr: str
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.subslr`
    
    Compute the rectangular coordinates of the sub-solar point on
    a target body at a specified epoch, optionally corrected for
    light time and stellar aberration.

    This routine supersedes subsol_c.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/subslr_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param ets: Epochs in ephemeris seconds past J2000 TDB.
    :param fixref: Body-fixed, body-centered target body frame.
    :param abcorr: Aberration correction.
    :param obsrvr: Name of observing body.
    :return:
            Sub-solar point on the target body in km,
            Sub-solar point epoch,
            Vector from observer to sub-solar point in km.
    """
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
    cdef double[:,::1] _spoint = spoint
    cdef np.ndarray[dtype=DOUBLE_t, ndim=2, mode="c"] srfvec = np.empty((n,3), dtype=np.double)
    cdef double[:,::1] _srfvec = srfvec
    cdef np.ndarray[dtype=DOUBLE_t, ndim=1, mode="c"] trgepc = np.empty(n, dtype=np.double)
    cdef double[::1] _trgepc = trgepc
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
cpdef np.ndarray[DOUBLE_t, ndim=2] sxform(
    str fromstring, 
    str tostring, 
    double et
):
    """
    Return the state transformation matrix from one frame to
    another at a specified epoch.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sxform_c.html


    :param instring: Name of the frame to transform from.
    :param tostring: Name of the frame to transform to.
    :param et: Epoch of the state transformation matrix.
    :return: A state transformation matrix.
    """
    cdef double[6][6] tform 
    cdef const char * c_fromstring = fromstring
    cdef const char * c_tostring = tostring
    # initialize output
    cdef np.ndarray[dtype=DOUBLE_t, ndim=2, mode="c"] xform = np.empty((6, 6), dtype=np.double)
    cdef double[:,:] _xform = xform
    sxform_c(
        c_fromstring, 
        c_tostring, 
        et, 
        tform
    )
    _xform[:,:] = tform
    return xform


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[DOUBLE_t, ndim=3] sxform_v(
    str fromstring, 
    str tostring, 
    double[::1] ets
):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.sxform`
    
    Return the state transformation matrix from one frame to
    another at a specified epoch.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sxform_c.html


    :param instring: Name of the frame to transform from.
    :param tostring: Name of the frame to transform to.
    :param et: Epochs of the state transformation matrix.
    :return: A state transformation matrix.
    """
    cdef Py_ssize_t i, n = ets.shape[0]
    cdef double[6][6] c_tform
    cdef const char * c_fromstring = fromstring
    cdef const char * c_tostring = tostring
    # initialize output
    cdef np.ndarray[dtype=DOUBLE_t, ndim=3, mode="c"] xform = np.empty((n, 6, 6), dtype=np.double)
    cdef double[:,:,::1] _xform = xform
    for i in range(n):
        sxform_c(
            c_fromstring, 
            c_tostring, 
            ets[i], 
            c_tform
        )
        _xform[i,:,:] = c_tform
    return xform

# T

@wraparound(False)
@boundscheck(False)
cpdef tangpt(
    str method,
    str target,
    double et,
    str fixref,
    str abcorr,
    str corloc,
    str obsrvr,
    str dref,
    double[::1] dvec
    ):
    """
    Compute, for a given observer, ray emanating from the observer,
    and target, the "tangent point": the point on the ray nearest
    to the target's surface. Also compute the point on the target's
    surface nearest to the tangent point.

    The locations of both points are optionally corrected for light
    time and stellar aberration.

    The surface shape is modeled as a triaxial ellipsoid.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tangpt_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param et: Epoch in ephemeris seconds past J2000 TDB.
    :param fixref: Body-fixed, body-centered target body frame.
    :param abcorr: Aberration correction.
    :param corloc: Aberration correction locus: "TANGENT POINT" or
                   "SURFACE POINT".
    :param obsrvr: Name of observing body.
    :param dref: Reference frame of ray direction vector.
    :param dvec: Ray direction vector.
    :return: "Tangent point": point on ray nearest to surface, Altitude of
     tangent point above surface, Distance of tangent point from observer,
     Point on surface nearest to tangent point, Epoch associated with
     correction locus, Vector from observer to surface point `srfpt'.
    """
    # convert strings 
    cdef const char * c_method = method
    cdef const char * c_target = target
    cdef const char * c_fixref = fixref
    cdef const char * c_abcorr = abcorr
    cdef const char * c_corloc = corloc
    cdef const char * c_obsrvr = obsrvr
    cdef const char * c_dref   = dref
    # Allocate output floats and arrays with appropriate shapes.
    cdef double alt, vrange, trgepc
    cdef np.double_t[::1] c_tanpt = np.empty(3, dtype=np.double)
    cdef np.double_t[::1] c_srfpt = np.empty(3, dtype=np.double)
    cdef np.double_t[::1] c_srfvec = np.empty(3, dtype=np.double)
    # perform the call
    tangpt_c(
        c_method, 
        c_target, 
        et, 
        c_fixref, 
        c_abcorr,
        c_corloc,
        c_obsrvr,
        c_dref,
        &dvec[0],
        &c_tanpt[0],
        &alt,
        &vrange,
        &c_srfpt[0],
        &trgepc,
        &c_srfvec[0]
    )
    # return values
    return c_tanpt, alt, vrange, c_srfpt, trgepc, c_srfvec


@boundscheck(False)
@wraparound(False)
cpdef tangpt_v(    
    str method,
    str target,
    double[::1] ets,
    str fixref,
    str abcorr,
    str corloc,
    str obsrvr,
    str dref,
    double[::1] dvec
):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.tangpt`
    
    Compute, for a given observer, ray emanating from the observer,
    and target, the "tangent point": the point on the ray nearest
    to the target's surface. Also compute the point on the target's
    surface nearest to the tangent point.

    The locations of both points are optionally corrected for light
    time and stellar aberration.

    The surface shape is modeled as a triaxial ellipsoid.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tangpt_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param ets: Epochs in ephemeris seconds past J2000 TDB.
    :param fixref: Body-fixed, body-centered target body frame.
    :param abcorr: Aberration correction.
    :param corloc: Aberration correction locus: "TANGENT POINT" or
                   "SURFACE POINT".
    :param obsrvr: Name of observing body.
    :param dref: Reference frame of ray direction vector.
    :param dvec: Ray direction vector.
    :return: "Tangent point": point on ray nearest to surface, Altitude of
     tangent point above surface, Distance of tangent point from observer,
     Point on surface nearest to tangent point, Epoch associated with
     correction locus, Vector from observer to surface point `srfpt'.
    """
    # allocate sizes
    cdef Py_ssize_t i, n = ets.shape[0]
    # convert strings to ascii
    cdef const char * c_method = method
    cdef const char * c_target = target
    cdef const char * c_fixref = fixref
    cdef const char * c_abcorr = abcorr
    cdef const char * c_corloc = corloc
    cdef const char * c_obsrvr = obsrvr
    cdef const char * c_dref   = dref
    # Allocate output floats and arrays with appropriate shapes.
    cdef np.double_t[:,::1] c_tanpt  = np.empty((n,3), dtype=np.double)
    cdef np.double_t[::1]   c_alt    = np.empty(n, dtype=np.float64)
    cdef np.double_t[::1]   c_vrange = np.empty(n, dtype=np.float64)
    cdef np.double_t[:,::1] c_srfpt  = np.empty((n,3), dtype=np.double)
    cdef np.double_t[::1]   c_trgepc = np.empty(n, dtype=np.float64)
    cdef np.double_t[:,::1]   c_srfvec = np.empty((n,3), dtype=np.double)
    # perform the calls
    for i in range(n):
        tangpt_c(
            c_method, 
            c_target, 
            ets[i], 
            c_fixref, 
            c_abcorr,
            c_corloc,
            c_obsrvr,
            c_dref,
            &dvec[0],
            &c_tanpt[i][0],
            &c_alt[i],
            &c_vrange[i],
            &c_srfpt[i][0],
            &c_trgepc[i],
            &c_srfvec[i][0]
        )
    # return values
    return c_tanpt, c_alt, c_vrange, c_srfpt, c_trgepc, c_srfvec


cpdef str timout(et: float, pictur: str):
    """
    This vectorized routine converts an input epoch represented in TDB seconds
    past the TDB epoch of J2000 to a character string formatted to
    the specifications of a user's format picture.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/timout_c.html

    :param et: An epoch in seconds past the ephemeris epoch J2000.
    :param pictur: A format specification for the output string.
    :return: A string representation of the input epoch.
    """
    cdef const char * _pictur = pictur 
    cdef char[_default_len_out] c_buffer
    timout_c(et, _pictur, _default_len_out, c_buffer)
    return PyUnicode_DecodeUTF8(c_buffer, strlen(c_buffer), "strict")


@boundscheck(False)
@wraparound(False)
cpdef list[str] timout_v(
    double[::1] ets, 
    str pictur
):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.timout`
    
    This routine converts an input epoch represented in TDB seconds
    past the TDB epoch of J2000 to a character string formatted to
    the specifications of a user's format picture.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/timout_c.html

    :param ets: Epochs in seconds past the ephemeris epoch J2000.
    :param pictur: A format specification for the output string.
    :return: A string representation of the input epoch.
    """
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
    """
    Compute the angular separation in radians between two spherical
    or point objects.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/trgsep_c.html

    :param et: Ephemeris seconds past J2000 TDB.
    :param targ1: First target body name.
    :param shape1: First target body shape.
    :param frame1: Reference frame of first target (UNUSED).
    :param targ2: Second target body name.
    :param shape2: First target body shape.
    :param frame2: Reference frame of second target (UNUSED).
    :param obsrvr: Observing body name.
    :param abcorr: Aberration corrections flag.
    :return: angular separation in radians.
    """
    cdef SpiceDouble c_et = et
    cdef const char * c_targ1   = targ1
    cdef const char * c_shape1  = shape1
    cdef const char * c_frame1  = frame1
    cdef const char * c_targ2   = targ2
    cdef const char * c_shape2  = shape2
    cdef const char * c_frame2  = frame2
    cdef const char * c_obsrvr  = obsrvr
    cdef const char * c_abcorr  = abcorr
    return trgsep_c(
        c_et, 
        c_targ1, 
        c_shape1, 
        c_frame1, 
        c_targ2, 
        c_shape2, 
        c_frame2, 
        c_obsrvr, 
        c_abcorr
    )


@boundscheck(False)
@wraparound(False)
cpdef double[::1] trgsep_v(
    double[::1] ets, 
    str targ1,
    str shape1,
    str frame1,
    str targ2, 
    str shape2, 
    str frame2, 
    str obsrvr, 
    str abcorr
):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.trgsep`
    
    Compute the angular separation in radians between two spherical
    or point objects.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/trgsep_c.html

    :param ets: Ephemeris seconds past J2000 TDB.
    :param targ1: First target body name.
    :param shape1: First target body shape.
    :param frame1: Reference frame of first target (UNUSED).
    :param targ2: Second target body name.
    :param shape2: First target body shape.
    :param frame2: Reference frame of second target (UNUSED).
    :param obsrvr: Observing body name.
    :param abcorr: Aberration corrections flag.
    :return: angular separation in radians.
    """
    cdef Py_ssize_t i, n = ets.shape[0] 
    cdef const char * c_targ1   = targ1
    cdef const char * c_shape1  = shape1
    cdef const char * c_frame1  = frame1
    cdef const char * c_targ2   = targ2
    cdef const char * c_shape2  = shape2
    cdef const char * c_frame2  = frame2
    cdef const char * c_obsrvr  = obsrvr
    cdef const char * c_abcorr  = abcorr
    # initialize output
    cdef np.double_t[::1] c_angseps = np.empty(n, dtype=np.double)
    for i in range(n):
        c_angseps[i] = trgsep_c(
            ets[i], 
            c_targ1, 
            c_shape1, 
            c_frame1, 
            c_targ2, 
            c_shape2,
            c_frame2, 
            c_obsrvr, 
            c_abcorr
        )
    return c_angseps

# U

cpdef double unitim(
        epoch: float,
        insys: str,
        outsys: str,
    ):
    """
    Transform time from one uniform scale to another.  The uniform
    time scales are TAI, TDT, TDB, ET, JED, JDTDB, JDTDT.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/unitim_c.html

    :param epoch: An epoch to be converted.
    :param insys: The time scale associated with the input epoch.
    :param outsys: The time scale associated with the function value.
    :return:
            The float in outsys that is equivalent
            to the epoch on the insys time scale.
    """
    cdef const char * _insys = insys
    cdef const char * _outsys = outsys
    return unitim_c(epoch, _insys, _outsys)


@boundscheck(False)
@wraparound(False)
cpdef np.double_t[::1] unitim_v(
        double[::1] epochs,
        insys: str,
        outsys: str,
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.unitim`
    
    Transform time from one uniform scale to another.  The uniform
    time scales are TAI, TDT, TDB, ET, JED, JDTDB, JDTDT.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/unitim_c.html

    :param epochs: Epochs to be converted.
    :param insys: The time scale associated with the input epoch.
    :param outsys: The time scale associated with the function value.
    :return:
            The float in outsys that is equivalent
            to the epoch on the insys time scale.
    """
    cdef Py_ssize_t i, n = epochs.shape[0]
    cdef double _unitim
    cdef const char * c_insys = insys
    cdef const char * c_outsys = outsys
    # initialize output
    cdef np.double_t[::1] c_unitims = np.empty(n, dtype=np.double)
    # perform the actual call
    for i in range(n):
        c_unitims[i] = unitim_c(
            epochs[i], 
            c_insys, 
            c_outsys
        )
    return c_unitims


cpdef void unload(file: str) noexcept:
    """
    Unload a SPICE kernel.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/unload_c.html

    :param filename: The name of a kernel to unload.
    """
    cdef const char* _file = file
    unload_c(_file)


cpdef double utc2et(utcstr: str):
    """
    Convert an input time from Calendar or Julian Date format, UTC,
    to ephemeris seconds past J2000.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/utc2et_c.html

    :param utcstr: Input time string, UTC.
    :return: Output epoch, ephemeris seconds past J2000.
    """
    cdef const char* c_utcstr = utcstr
    cdef double et
    utc2et_c(
        c_utcstr, 
        &et
    )
    return et


@boundscheck(False)
@wraparound(False)
cpdef double[::1] utc2et_v(np.ndarray utcstr):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.utc2et`
    
    Convert an input time from Calendar or Julian Date format, UTC,
    to ephemeris seconds past J2000.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/utc2et_c.html

    :param utcstr: Input time strings, UTC.
    :return: Output epochs, ephemeris seconds past J2000.
    """
    cdef Py_ssize_t i, n = utcstr.shape[0]
    # initialize output
    cdef np.double_t[::1] c_ets = np.empty(n, dtype=np.double)
    for i in range(n):
        utc2et_c(
            utcstr[i], 
            &c_ets[i]
        )
    return c_ets
