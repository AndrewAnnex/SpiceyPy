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
from cpython.unicode cimport PyUnicode_DecodeUTF8, PyUnicode_DecodeASCII, PyUnicode_DecodeCharmap
import numpy as np
cimport numpy as np
np.import_array()

DEF _default_len_out = 256

DEF TIMELEN = 60

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

def b1900():
    """
    Return the Julian Date corresponding to Besselian Date 1900.0.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/b1900_c.html

    :return: The Julian Date corresponding to Besselian Date 1900.0.
    """
    return b1900_c()


def b1950():
    """
    Return the Julian Date corresponding to Besselian Date 1950.0.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/b1950_c.html

    :return: The Julian Date corresponding to Besselian Date 1950.0.
    """
    return b1950_c()

#C

@boundscheck(False)
@wraparound(False)
def ckgp(
    int inst,
    double sclkdp,
    double tol,
    str ref
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
    cdef double c_clkout = 0.0
    cdef bint c_found
    # convert the strings to pointers once
    cdef const char* c_ref = ref
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2] p_cmat = np.empty((3,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_cmat = p_cmat
    # perform the call
    ckgp_c(
        inst,
        sclkdp,
        tol,
        c_ref,
        <SpiceDouble (*)[3]> &c_cmat[0,0],
        &c_clkout,
        &c_found
    )
    # return results
    return p_cmat, c_clkout, c_found


@boundscheck(False)
@wraparound(False)
def ckgp_v(
    int inst,
    double[::1] sclkdps,
    double tol,
    str ref
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.ckgp`

    Get pointing (attitude) for specified spacecraft clock times.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckgp_c.html

    :param inst: NAIF ID of instrument, spacecraft, or structure.
    :param sclkdps: Encoded spacecraft clock times.
    :param tol: Time tolerance.
    :param ref: Reference frame.
    :return:
            C-matrix pointing data,
            Output encoded spacecraft clock time
    """
    # initialize c variables
    cdef const double[::1] c_sclkdps= np.ascontiguousarray(sclkdps)
    cdef Py_ssize_t i, n = c_sclkdps.shape[0]
    # convert the strings to pointers once
    cdef const char* c_ref = ref
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=3, mode='c'] p_cmat = np.empty((n,3,3), dtype=np.double, order='C')
    cdef np.double_t[:,:,::1] c_cmat = p_cmat
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_clkout = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_clkout = p_clkout
    cdef np.ndarray[np.uint8_t, ndim=1, mode='c'] p_found = np.empty(n, dtype=np.bool_, order='C')
    cdef np.uint8_t[::1] c_found = p_found
    # perform the call
    for i in range(n):
        ckgp_c(
            inst,
            c_sclkdps[i],
            tol,
            c_ref,
            <SpiceDouble (*)[3]> &c_cmat[i,0,0],
            &c_clkout[i],
            <SpiceBoolean *> &c_found[i]
        )
    # return results
    return p_cmat, p_clkout, p_found


@boundscheck(False)
@wraparound(False)
def ckgpav(
    int    inst,
    double sclkdp,
    double tol,
    str    ref
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
    cdef double c_clkout = 0.0
    cdef bint c_found 
    # convert the strings to pointers once
    cdef const char* c_ref = ref
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_cmat = np.empty((3,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_cmat = p_cmat
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_av   = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1]   c_av   = p_av   
    # perform the call
    ckgpav_c(
        inst,
        sclkdp,
        tol,
        c_ref,
        <SpiceDouble (*)[3]> &c_cmat[0,0],
        &c_av[0],
        &c_clkout,
        &c_found
    )
    # return results
    return p_cmat, p_av, c_clkout, c_found


@boundscheck(False)
@wraparound(False)
def ckgpav_v(
    int    inst,
    double[::1] sclkdps,
    double tol,
    str    ref
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.ckgpav`

    Get pointing (attitude) and angular velocity
    for specified spacecraft clock times.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckgpav_c.html

    :param inst: NAIF ID of instrument, spacecraft, or structure.
    :param sclkdp: Encoded spacecraft clock times.
    :param tol: Time tolerance.
    :param ref: Reference frame.
    :return:
            C-matrix pointing data,
            Angular velocity vector,
            Output encoded spacecraft clock time.
    """
    # initialize c variables
    cdef const double[::1] c_sclkdps= np.ascontiguousarray(sclkdps)
    cdef Py_ssize_t i, n = c_sclkdps.shape[0]
    # convert the strings to pointers once
    cdef const char* c_ref = ref
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=3, mode='c'] p_cmat = np.empty((n,3,3), dtype=np.double, order='C')
    cdef np.double_t[:,:,::1] c_cmat = p_cmat
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_av   = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1]   c_av = p_av
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_clkout = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_clkout = p_clkout
    cdef np.ndarray[np.uint8_t, ndim=1, mode='c'] p_found = np.empty(n, dtype=np.bool_, order='C')
    cdef np.uint8_t[::1] c_found = p_found
    # perform the call
    for i in range(n):
        ckgpav_c(
            inst,
            c_sclkdps[i],
            tol,
            c_ref,
            <SpiceDouble (*)[3]> &c_cmat[i,0,0],
            &c_av[i,0],
            &c_clkout[i],
            <SpiceBoolean *> &c_found[i]
        )
    # return results
    return p_cmat, p_av, p_clkout, p_found


def convrt(double x, str inunit, str outunit):
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
    cdef const char * c_inunit = inunit
    cdef const char * c_outunit = outunit
    convrt_c(x, c_inunit, c_outunit, &out)
    return out


@boundscheck(False)
@wraparound(False)
def convrt_v(
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
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_outs = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_outs = p_outs
    # main loop
    for i in range(n):
        convrt_c(
            x[i], 
            c_inunit,
            c_outunit, 
            &c_outs[i]
        )
    return p_outs


#D


def deltet(
    double epoch, 
    str eptype
    ):
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
def deltet_v(
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
    cdef const double[::1] c_epochs = np.ascontiguousarray(epochs)
    cdef Py_ssize_t i, n = c_epochs.shape[0]
    cdef const char* c_eptype = eptype
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_deltas = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_deltas = p_deltas
    # perform the loop
    for i in range(n):
        deltet_c(
            c_epochs[i], 
            c_eptype, 
            &c_deltas[i]
        )
    # return results
    return p_deltas

#E 


def et2lst(
    double et,
    int body,
    double lon,
    str typein
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
    cdef int hr, mn, sc
    cdef char[TIMELEN] time
    cdef char[TIMELEN] ampm
    cdef const char * c_typein = typein
    et2lst_c(
        et,
        body,
        lon,
        c_typein,
        TIMELEN,
        TIMELEN,
        &hr,
        &mn,
        &sc,
        time,
        ampm
    )
    return hr, mn, sc, PyUnicode_DecodeUTF8(time, strlen(time), "strict"), PyUnicode_DecodeUTF8(ampm, strlen(ampm), "strict")


@boundscheck(False)
@wraparound(False)
def et2lst_v(
   double[::1] ets,
   int body,
   double lon,
   str typein
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
    cdef const double[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    cdef const char * c_typein = typein
    cdef int c_body = body
    cdef double c_lon = lon
    # initialize output arrays 
    p_np_s_dtype = np.dtype(('S', TIMELEN))
    p_np_u_dtype = np.dtype(('U', TIMELEN))
    cdef np.ndarray[np.int32_t, ndim=1, mode='c'] p_hrs = np.empty(n, dtype=np.int32, order='C')
    cdef np.ndarray[np.int32_t, ndim=1, mode='c'] p_mns = np.empty(n, dtype=np.int32, order='C')
    cdef np.ndarray[np.int32_t, ndim=1, mode='c'] p_scs = np.empty(n, dtype=np.int32, order='C')
    cdef np.ndarray[np.uint8_t, ndim=2, mode='c'] p_times = np.zeros((n, TIMELEN), dtype=np.uint8, order='C')
    cdef np.ndarray[np.uint8_t, ndim=2, mode='c'] p_ampms = np.zeros((n, TIMELEN), dtype=np.uint8, order='C')
    cdef SpiceInt[::1] c_hrs = p_hrs
    cdef SpiceInt[::1] c_mns = p_mns
    cdef SpiceInt[::1] c_scs = p_scs
    cdef np.uint8_t[:,::1] times = p_times
    cdef np.uint8_t[:,::1] ampms = p_ampms
    # main loop
    for i in range(n):
        et2lst_c(
            c_ets[i],
            c_body,
            c_lon,
            c_typein,
            TIMELEN,
            TIMELEN,
            &c_hrs[i],
            &c_mns[i], 
            &c_scs[i], 
            <char*> &times[i, 0], 
            <char*> &ampms[i, 0]
        )
    # return values
    py_times = p_times.view(p_np_s_dtype).reshape(n)
    py_times = np.char.rstrip(py_times).astype(p_np_u_dtype)
    py_ampms = p_ampms.view(p_np_s_dtype).reshape(n)
    py_ampms = np.char.rstrip(py_ampms).astype(p_np_u_dtype)
    return p_hrs, p_mns, p_scs, py_times, py_ampms


def et2utc(
    double et, 
    str format_str, 
    int prec
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
    cdef double c_et = et
    cdef int c_prec = prec
    cdef char[TIMELEN] c_buffer
    cdef const char* c_format_str = format_str
    et2utc_c(
        c_et, 
        c_format_str, 
        c_prec, 
        TIMELEN, 
        &c_buffer[0]
    ) 
    return PyUnicode_DecodeUTF8(c_buffer, strlen(c_buffer), "strict")


@boundscheck(False)
@wraparound(False)
def et2utc_v(
    double[::1] ets,
    str format_str, 
    int prec
    ):
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
    cdef int c_prec = prec
    cdef char[TIMELEN] c_buffer
    cdef const double[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t i, fixed_length, n = c_ets.shape[0]
    # convert the strings to pointers once
    cdef const char * c_format_str = format_str
    # initialize output arrays TODO: using a unicode numpy array?
    cdef list results = [None] * n
    # Process the first element and compute the fixed length.
    et2utc_c(
        c_ets[0], 
        c_format_str, 
        c_prec, 
        TIMELEN, 
        &c_buffer[0]
    )  
    fixed_length = strlen(c_buffer)
    results[0] = PyUnicode_DecodeUTF8(c_buffer, fixed_length, "strict")
    # main loop for all other values
    if n > 1:
        for i in range(1, n):
            et2utc_c(
                c_ets[i], 
                c_format_str, 
                c_prec, 
                TIMELEN, 
                &c_buffer[0]
            )
            results[i] = PyUnicode_DecodeUTF8(c_buffer, fixed_length, "strict")
    # return array
    return np.asarray(results)


def etcal(double et):
    """
    Convert from an ephemeris epoch measured in seconds past
    the epoch of J2000 to a calendar string format using a
    formal calendar free of leapseconds.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/etcal_c.html

    :param et: Ephemeris time measured in seconds past J2000 TDB.
    :return: A standard calendar representation of et.
    """
    cdef char[TIMELEN] c_buffer
    etcal_c(
        et, 
        TIMELEN, 
        &c_buffer[0]
    )
    # Convert the C char* to a Python string
    return PyUnicode_DecodeUTF8(c_buffer, strlen(c_buffer), "strict")


@boundscheck(False)
@wraparound(False)
def etcal_v(double[::1] ets):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.etcal`

    Convert from an ephemeris epoch measured in seconds past
    the epoch of J2000 to a calendar string format using a
    formal calendar free of leapseconds.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/etcal_c.html

    :param ets: Ephemeris times measured in seconds past J2000 TDB.
    :return: A standard calendar representation of et.
    """
    cdef const double[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # Allocate a 2D buffer of shape (n, 24) with dtype np.uint8
    cdef np.ndarray[dtype=CHAR_t, ndim=2] results = np.empty((n, 25), dtype=np.uint8)
    # Create a typed memoryview over the buffer
    cdef unsigned char[:, ::1] view = results
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

def failed():
    """
    True if an error condition has been signalled via sigerr_c.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/failed_c.html

    :return: a boolean
    """
    return failed_c()


@boundscheck(False)
@wraparound(False)
def fovray(
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
    cdef bint c_visibl
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
def fovray_v(
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
    cdef const double[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert the strings to pointers once
    cdef const char* c_inst     = inst
    cdef const char* c_rframe   = rframe
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsrvr   = obsrvr
    # initialize output arrays
    cdef np.ndarray[np.uint8_t, ndim=1, mode='c'] p_visibl = np.empty(n, dtype=np.bool_, order='C')
    cdef np.uint8_t[::1] c_visibl = p_visibl
    # perform the call
    for i in range(n):
        fovray_c(
            c_inst,
            &raydir[0],
            c_rframe,
            c_abcorr,
            c_obsrvr,
            &ets[i],
            <SpiceBoolean *> &c_visibl[0]
        )
    # return
    return p_visibl
  

def fovtrg(
    str inst,   
    str target,
    str tshape,
    str tframe,
    str abcorr,
    str obsrvr,
    double et
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
    cdef bint c_visibl 
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
def fovtrg_v(
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
    cdef const double[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert the strings to pointers once
    cdef const char* c_inst     = inst
    cdef const char* c_target   = target
    cdef const char* c_tshape   = tshape
    cdef const char* c_tframe   = tframe
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsrvr   = obsrvr
    # initialize output arrays
    cdef np.ndarray[np.uint8_t, ndim=1, mode='c'] p_visibl = np.empty(n, dtype=np.bool_, order='C')
    cdef np.uint8_t[::1] c_visibl = p_visibl
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
            <SpiceBoolean *> &c_visibl[0]
        )
    # return
    return p_visibl


def furnsh(str file):
    """
    Load one or more SPICE kernels into a program.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/furnsh_c.html

    :param path: one or more paths to kernels
    """
    cdef const char * c_file = file
    furnsh_c(c_file)
    

# G
def getmsg(
    str option, 
    int msglen
    ):
    """
    Retrieve the current short error message,
    the explanation of the short error message, or the
    long error message.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/getmsg_c.html

    :param option: Indicates type of error message.
    :param lenout: Available space in the output string msg.
    :return: The error message to be retrieved.
    """
    cdef const char * c_option = option
    cdef char* c_msgstr = <char *> malloc((msglen) * sizeof(char))
    getmsg_c(
        c_option, 
        msglen, 
        c_msgstr
    )
    pymsg = <unicode> c_msgstr
    free(c_msgstr)
    return pymsg


# H

# i


# J


# K


# L

def lspcn(
    str body, 
    double et, 
    str abcorr
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
def lspcn_v(
    str body, 
    double[::1] ets, 
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
    cdef const double[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    cdef const char * c_body   = body
    cdef const char * c_abcorr = abcorr
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_l_s_s = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_l_s_s = p_l_s_s
    for i in range(n):
        c_l_s_s[i] = lspcn_c(
            c_body, 
            c_ets[i], 
            c_abcorr
        )
    return p_l_s_s

#M 

#N 

#O 

#P 

# Q

def qcktrc(int tracelen):
    """
    Return a string containing a traceback.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/qcktrc_c.html

    :param tracelen: Maximum length of output traceback string.
    :return: A traceback string.
    """
    cdef char * _tracestr = <char *> malloc((tracelen) * sizeof(char))
    qcktrc_c(
        tracelen, 
        _tracestr
    )
    pytracestr = <unicode> _tracestr
    free(_tracestr)
    return pytracestr

# R


def reset():
    """
    Reset the SPICE error status to a value of "no error."
    As a result, the status routine, failed, will return a value
    of False

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/reset_c.html

    """
    reset_c()

#S

def scdecd(int sc, double sclkdp):
    """
    Convert double precision encoding of spacecraft clock time into
    a character representation.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scdecd_c.html

    :param sc: NAIF spacecraft identification code.
    :param sclkdp: Encoded representation of a spacecraft clock count.
    :return: Character representation of a clock count.
    """
    cdef char[_default_len_out] c_buffer 
    scdecd_c(
        sc, 
        sclkdp, 
        _default_len_out, 
        &c_buffer[0]
    )
    return PyUnicode_DecodeUTF8(c_buffer, strlen(c_buffer), "strict")


@boundscheck(False)
@wraparound(False)
def scdecd_v(
    int sc, 
    double[::1] sclkdps
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.scdecd`

    Convert double precision encoding of spacecraft clock time into
    a character representation.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scdecd_c.html

    :param sc: NAIF spacecraft identification code.
    :param sclkdps: Encoded representations of a spacecraft clock count.
    :return: Character representation of a clock count.
    """
    cdef const double[::1] c_sclkdps = np.ascontiguousarray(sclkdps)
    cdef Py_ssize_t i, length, n = c_sclkdps.shape[0]
    cdef char[_default_len_out] c_buffer 
    cdef list sclkchs = [None] * n
    scdecd_c(
        sc, 
        c_sclkdps[0], 
        _default_len_out, 
        &c_buffer[0]
    )
    length = strlen(c_buffer)
    sclkchs[0] = PyUnicode_DecodeUTF8(c_buffer, length, "strict") 
    if n > 1:
        for i in range(1, n):
            scdecd_c(
                sc, 
                c_sclkdps[i], 
                _default_len_out, 
                &c_buffer[0]
            )
            sclkchs[i] = PyUnicode_DecodeUTF8(c_buffer, length, "strict")
    return np.asarray(sclkchs)


def scencd(
    int sc, 
    str sclkch
    ):
    """
    Encode character representation of spacecraft clock time into a
    double precision number.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scencd_c.html

    :param sc: NAIF spacecraft identification code.
    :param sclkch: Character representation of a spacecraft clock.
    :return: Encoded representation of the clock count.
    """
    cdef double sclkdp
    cdef const char * c_sclkch = sclkch
    scencd_c(
        sc, 
        c_sclkch, 
        &sclkdp
    )
    return sclkdp


@boundscheck(False)
@wraparound(False)
def scencd_v(
    int sc, 
    list[str] sclkchs
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.scencd`

    Encode character representation of spacecraft clock time into a
    double precision number.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scencd_c.html

    :param sc: NAIF spacecraft identification code.
    :param sclkchs: Character representations of a spacecraft clock.
    :return: Encoded representations of the clock count.
    """
    cdef Py_ssize_t i, n = len(sclkchs)
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_sclkdps = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_sclkdps = p_sclkdps
    for i in range(n):
        scencd_c(
            sc, 
            sclkchs[i], 
            &c_sclkdps[i]
        )
    return p_sclkdps


def sce2c(
    int sc, 
    double et
    ):
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
    cdef double sclkdp
    sce2c_c(
        sc, 
        et, 
        &sclkdp
    )
    return sclkdp


@boundscheck(False)
@wraparound(False)
def sce2c_v(
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
    cdef const double[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_sclkdps = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_sclkdps = p_sclkdps
    for i in range(n):
        sce2c_c(
            sc, 
            c_ets[i], 
            &c_sclkdps[i]
        )
    return p_sclkdps


def sce2s(
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
def sce2s_v(
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
    cdef int c_sc = sc
    cdef const double[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t length, i, n = c_ets.shape[0]
    cdef char[_default_len_out] c_buffer
    cdef list sclkchs = [None] * n
    # perform the first iteration
    sce2s_c(
        c_sc, 
        c_ets[0], 
        _default_len_out, 
        &c_buffer[0]
    )
    length = strlen(c_buffer)
    # store the result
    sclkchs[0] = PyUnicode_DecodeUTF8(c_buffer, length, "strict") 
    if n > 1:
        for i in range(1, n):
            sce2s_c(
                c_sc, 
                c_ets[i], 
                _default_len_out, 
                &c_buffer[0]
            )
            sclkchs[i] = PyUnicode_DecodeUTF8(c_buffer, length, "strict")
    return np.asarray(sclkchs)


def scs2e(
    int sc,
    str sclkch
    ):
    """
    Convert a spacecraft clock string to ephemeris seconds past J2000 (ET).

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scs2e_c.html

    :param sc: NAIF integer code for a spacecraft.
    :param sclkch: An SCLK string.
    :return: Ephemeris time, seconds past J2000.
    """
    cdef double et
    cdef const char * c_sclkch = sclkch
    scs2e_c(
        sc, 
        c_sclkch, 
        &et
    )
    return et


@boundscheck(False)
@wraparound(False)
def scs2e_v(
    int sc, 
    np.ndarray sclkchs
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.scs2e`

    Convert a spacecraft clock string to ephemeris seconds past J2000 (ET).

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scs2e_c.html

    :param sc: NAIF integer code for a spacecraft.
    :param sclkchs: SCLK strings.
    :return: Ephemeris time, seconds past J2000.
    """
    cdef Py_ssize_t i, n = sclkchs.shape[0]
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_ets = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_ets = p_ets
    for i in range(n):
        scs2e_c(
            sc, 
            sclkchs[i],
            &c_ets[i]
        )
    return p_ets


def sct2e(
    int sc, 
    double sclkdp
    ):
    """
    Convert encoded spacecraft clock ("ticks") to ephemeris
    seconds past J2000 (ET).

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sct2e_c.html

    :param sc: NAIF spacecraft ID code.
    :param sclkdp: SCLK, encoded as ticks since spacecraft clock start.
    :return: Ephemeris time, seconds past J2000.
    """
    cdef double et
    sct2e_c(
        sc, 
        sclkdp, 
        &et
    )
    return et


@boundscheck(False)
@wraparound(False)
def sct2e_v(
    int sc, 
    double[::1] sclkdps
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.sct2e`

    Convert encoded spacecraft clock ("ticks") to ephemeris
    seconds past J2000 (ET).

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sct2e_c.html

    :param sc: NAIF spacecraft ID code.
    :param sclkdps: SCLKs, encoded as ticks since spacecraft clock start.
    :return: Ephemeris time, seconds past J2000.
    """
    cdef const double[::1] c_sclkdps = np.ascontiguousarray(sclkdps)
    cdef Py_ssize_t i, n = c_sclkdps.shape[0]
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_ets = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_ets = p_ets
    for i in range(n):
        sct2e_c(
            sc, 
            c_sclkdps[i], 
            &c_ets[i]
        )
    return p_ets


@boundscheck(False)
@wraparound(False)
def spkapo(
    int targ,  
    double et, 
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
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_ptarg = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_ptarg = p_ptarg
    spkapo_c(
        targ, 
        et, 
        c_ref, 
        &sobs[0],
        c_abcorr, 
        &c_ptarg[0], 
        &lt
    )
    return p_ptarg, lt


@boundscheck(False)
@wraparound(False)
def spkapo_v(
    int targ,  
    double[::1] ets, 
    str ref,
    double[::1] sobs, 
    str abcorr
    ):
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
    cdef const double[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert the strings to pointers once
    cdef const char* c_ref    = ref
    cdef const char* c_abcorr = abcorr
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_ptargs = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_ptargs = p_ptargs
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_lts = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_lts = p_lts
    # perform the call
    for i in range(n):
        spkapo_c(
            targ, 
            c_ets[i], 
            c_ref, 
            &sobs[0],
            c_abcorr, 
            &c_ptargs[i,0], 
            &c_lts[i]
        )
    return p_ptargs, p_lts



@boundscheck(False)
@wraparound(False)    
def spkez(
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
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_state = np.empty(6, dtype=np.double, order='C')
    cdef np.double_t[::1] c_state = p_state
    spkez_c(
        target, 
        epoch, 
        c_ref, 
        c_abcorr, 
        observer, 
        &c_state[0], 
        &lt)
    return p_state, lt


@boundscheck(False)
@wraparound(False)
def spkez_v(
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
    cdef const double[::1] c_epochs = np.ascontiguousarray(epochs)
    cdef Py_ssize_t i, n = c_epochs.shape[0]
    # convert the strings to pointers once
    cdef int c_target   = target
    cdef const char* c_ref    = ref
    cdef const char* c_abcorr = abcorr
    cdef int c_observer = observer
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_states = np.empty((n,6), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_states = p_states
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_lts = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_lts = p_lts
    # main loop
    for i in range(n):
        spkez_c(
            c_target, 
            c_epochs[i], 
            c_ref, 
            c_abcorr, 
            c_observer, 
            &c_states[i,0], 
            &c_lts[i]
        )
    # return results
    return p_states, p_lts


@boundscheck(False)
@wraparound(False)
def spkezp(
    int targ,  
    double et, 
    str ref, 
    str abcorr, 
    int obs
    ):
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
    # convert the strings to pointers once
    cdef const char* c_ref    = ref
    cdef const char* c_abcorr = abcorr
    cdef int c_targ = targ
    cdef int c_obs = obs
    cdef double c_lt
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_ptarg = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_ptarg = p_ptarg
    spkezp_c(
        c_targ, 
        et, 
        c_ref, 
        c_abcorr, 
        c_obs, 
        &c_ptarg[0], 
        &c_lt
    )
    return p_ptarg, c_lt
    

@boundscheck(False)
@wraparound(False)
def spkezp_v(
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
    cdef const double[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # initialize c variables
    cdef double lt = 0.0
    # convert the strings to pointers once
    cdef const char* c_ref    = ref
    cdef const char* c_abcorr = abcorr
    cdef int c_targ = targ
    cdef int c_obs = obs
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_ptargs = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_ptargs = p_ptargs
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_lts = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_lts = p_lts
    # main loop
    for i in range(n):
        spkezp_c(
            c_targ, 
            c_ets[i],
            c_ref, 
            c_abcorr, 
            c_obs, 
            &c_ptargs[i,0], 
            &c_lts[i]
        )
    # return results
    return p_ptargs, p_lts


@boundscheck(False)
@wraparound(False)    
def spkezr(
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
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_state = np.empty(6, dtype=np.double, order='C')
    cdef np.double_t[::1] c_state = p_state
    spkezr_c(
        target, 
        epoch,
        frame, 
        abcorr, 
        observer, 
        &c_state[0], 
        &lt)
    return p_state, lt


@boundscheck(False)
@wraparound(False)
def spkezr_v(
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
    cdef const double[::1] c_epochs = np.ascontiguousarray(epochs)
    cdef Py_ssize_t i, n = c_epochs.shape[0]
    # convert the strings to pointers once
    cdef const char* c_target   = target
    cdef const char* c_frame    = frame
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_observer = observer
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_states = np.empty((n,6), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_states = p_states
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_lts = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_lts = p_lts
    # main loop
    for i in range(n):
        spkezr_c(
            c_target,
            c_epochs[i], 
            c_frame, 
            c_abcorr, 
            c_observer, 
            &c_states[i,0], 
            &c_lts[i]
        )

    # return results
    return p_states, p_lts


@boundscheck(False)
@wraparound(False)
def spkcpo(
    str target,
    double et,
    str outref,
    str refloc,
    str abcorr,
    double[::1] obspos,
    str obsctr,
    str obsref
    ):
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
    # convert the strings to pointers once
    cdef const char* c_target   = target
    cdef const char* c_outref   = outref
    cdef const char* c_refloc   = refloc
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsctr   = obsctr
    cdef const char* c_obsref   = obsref
    # initialize output arrays
    cdef double c_lt
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_state = np.empty(6, dtype=np.double, order='C')
    cdef np.double_t[::1] c_state = p_state
    # perform the call
    spkcpo_c(
        c_target,
        et,
        c_outref,
        c_refloc,
        c_abcorr,
        &obspos[0],
        c_obsctr,
        c_obsref,
        &c_state[0],
        &c_lt
    )
    # return output
    return p_state, c_lt


@boundscheck(False)
@wraparound(False)
def spkcpo_v(
    str target,
    double[::1] ets,
    str outref,
    str refloc,
    str abcorr,
    double[::1] obspos,
    str obsctr,
    str obsref):
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
    cdef const double[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # initialize c variables TODO: vectorize obspos?
    cdef double c_lt = 0.0
    # convert the strings to pointers once
    cdef const char* c_target   = target
    cdef const char* c_outref   = outref
    cdef const char* c_refloc   = refloc
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsctr   = obsctr
    cdef const char* c_obsref   = obsref
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_states = np.empty((n,6), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_states = p_states
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_lts = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_lts = p_lts
    # perform the call
    for i in range(n):
        spkcpo_c(
            c_target,
            c_ets[i],
            c_outref,
            c_refloc,
            c_abcorr,
            &obspos[0],
            c_obsctr,
            c_obsref,
            &c_states[i][0],
            &c_lts[i]
        )
    # return output
    return p_states, p_lts


@boundscheck(False)
@wraparound(False)
def spkcpt(
    double[::1] trgpos,
    str trgctr,
    str trgref,
    double et,
    str outref,
    str refloc,
    str abcorr,
    str obsrvr
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
    cdef double c_lt = 0.0
    # convert the strings to pointers once
    cdef const char* c_trgctr   = trgctr
    cdef const char* c_trgref   = trgref
    cdef const char* c_outref   = outref
    cdef const char* c_refloc   = refloc
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsrvr   = obsrvr
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_state = np.empty(6, dtype=np.double, order='C')
    cdef np.double_t[::1] c_state = p_state
    # perform the call
    spkcpt_c(
        &trgpos[0],
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
    return p_state, c_lt


@boundscheck(False)
@wraparound(False)
def spkcpt_v(
    double[::1] trgpos,
    str trgctr,
    str trgref,
    double[::1] ets,
    str outref,
    str refloc,
    str abcorr,
    str obsrvr
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
    # initialize c variables TODO: vectorize obspos?
    cdef const double[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert the strings to pointers once
    cdef const char* c_trgctr   = trgctr
    cdef const char* c_trgref   = trgref
    cdef const char* c_outref   = outref
    cdef const char* c_refloc   = refloc
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsrvr   = obsrvr
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_states = np.empty((n,6), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_states = p_states
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_lts = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_lts = p_lts
    # perform the call
    for i in range(n):
        spkcpt_c(
            &trgpos[0],
            c_trgctr,
            c_trgref,
            c_ets[i],
            c_outref,
            c_refloc,
            c_abcorr,
            c_obsrvr,
            &c_states[i,0],
            &c_lts[i]
        )
    # return output
    return p_states, p_lts


@boundscheck(False)
@wraparound(False)
def spkcvo(
    str target,
    double et,
    str outref,
    str refloc,
    str abcorr,
    double[::1] obssta,
    double obsepc,
    str obsctr,
    str obsref):
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
    cdef double c_obsepc = obsepc
    cdef double c_lt = 0.0
    # convert the strings to pointers once
    cdef const char* c_target   = target
    cdef const char* c_outref   = outref
    cdef const char* c_refloc   = refloc
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsctr   = obsctr
    cdef const char* c_obsref   = obsref
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_state = np.empty(6, dtype=np.double, order='C')
    cdef np.double_t[::1] c_state = p_state
    # perform the call
    spkcvo_c(
        c_target,
        c_et,
        c_outref,
        c_refloc,
        c_abcorr,
        &obssta[0],
        c_obsepc,
        c_obsctr,
        c_obsref,
        &c_state[0],
        &c_lt
    )
    # return output
    return p_state, c_lt


@boundscheck(False)
@wraparound(False)
def spkcvo_v(
    str target,
    double[::1] ets,
    str outref,
    str refloc,
    str abcorr,
    double[::1] obssta, # TODO vectorize here?
    double obsepc,    # TODO vectorize here?
    str obsctr,
    str obsref):
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
    # initialize c variables TODO: vectorize obssta?
    cdef const double[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert the strings to pointers once
    cdef const char * c_target   = target
    cdef const char * c_outref   = outref
    cdef const char * c_refloc   = refloc
    cdef const char * c_abcorr   = abcorr
    cdef const char * c_obsctr   = obsctr
    cdef const char * c_obsref   = obsref
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_states = np.empty((n,6), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_states = p_states
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_lts = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_lts = p_lts
    # perform the call
    for i in range(n):
        spkcvo_c(
            c_target,
            c_ets[i],
            c_outref,
            c_refloc,
            c_abcorr,
            &obssta[0],
            obsepc,
            c_obsctr,
            c_obsref,
            &c_states[i,0],
            &c_lts[i]
        )
    # return output
    return p_states, p_lts


@boundscheck(False)
@wraparound(False)
def spkcvt(
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
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_state = np.empty(6, dtype=np.double, order='C')
    cdef np.double_t[::1] c_state = p_state
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
    return p_state, c_lt


@boundscheck(False)
@wraparound(False)
def spkcvt_v(
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
    cdef const double[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert the strings to pointers once
    cdef const char* c_trgctr   = trgctr
    cdef const char* c_trgref   = trgref
    cdef const char* c_outref   = outref
    cdef const char* c_refloc   = refloc
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsrvr   = obsrvr
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_states = np.empty((n,6), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_states = p_states
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_lts = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_lts = p_lts
    # perform the call
    for i in range(n):
        spkcvt_c(
            &trgsta[0],
            trgepc,
            c_trgctr,
            c_trgref,
            c_ets[i],
            c_outref,
            c_refloc,
            c_abcorr,
            c_obsrvr,
            &c_states[i,0],
            &c_lts[i]
        )
    # return output
    return p_states, p_lts


@boundscheck(False)
@wraparound(False)
def spkgeo(
    int targ,
    double et,
    str ref,
    int obs
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
    cdef int c_targ = targ
    cdef double c_et = et
    cdef double c_lt = 0.0
    cdef int c_obs  = obs
    # convert the strings to pointers once
    cdef const char* c_ref   = ref
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_state = np.empty(6, dtype=np.double, order='C')
    cdef np.double_t[::1] c_state = p_state
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
    return p_state, c_lt


@boundscheck(False)
@wraparound(False)
def spkgeo_v(
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
    cdef const double[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert the strings to pointers once
    cdef const char* c_ref   = ref
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_states = np.empty((n,6), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_states = p_states
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_lts = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_lts = p_lts
    # perform the call
    for i in range(n):
        spkgeo_c(
            targ,
            c_ets[i],
            c_ref,
            obs,
            &c_states[i,0],
            &c_lts[i]
        )
    # return output
    return p_states, p_lts


@boundscheck(False)
@wraparound(False)
def spkgps(
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
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_pos = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_pos = p_pos
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
    return p_pos, c_lt


@boundscheck(False)
@wraparound(False)
def spkgps_v(
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
    cdef const double[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert the strings to pointers once
    cdef const char* c_ref   = ref
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_pos = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_pos = p_pos
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_lts = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_lts = p_lts
    # perform the call
    for i in range(n):
        spkgps_c(
            targ,
            c_ets[i],
            c_ref,
            obs,
            &c_pos[i,0],
            &c_lts[i]
        )
    # return output
    return p_pos, p_lts


@boundscheck(False)
@wraparound(False)
def spkpvn(
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
    cdef int c_ref, c_center = 0
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_state = np.empty(6, dtype=np.double, order='C')
    cdef np.double_t[::1] c_state = p_state
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
    return c_ref, p_state, c_center


@boundscheck(False)
@wraparound(False)
def spkpvn_v(
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
    cdef const double[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # initialize c variables
    cdef int c_handle = handle
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_states = np.empty((n,6), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_states = p_states
    cdef np.ndarray[np.int32_t, ndim=1, mode='c'] p_refs = np.empty(n, dtype=np.int32, order='C')
    cdef np.int32_t[::1] c_refs = p_refs
    cdef np.ndarray[np.int32_t, ndim=1, mode='c'] p_centers = np.empty(n, dtype=np.int32, order='C')
    cdef np.int32_t[::1] c_centers = p_centers
    # perform the call
    for i in range(n):
        spkpvn_c(
            c_handle,
            &descr[0],
            c_ets[i],
            <SpiceInt *> &c_refs[i],
            &c_states[i,0],
            <SpiceInt *> &c_centers[i]
        )
    # return output 
    return p_refs, p_states, p_centers


@boundscheck(False)
@wraparound(False)
def spkpos(
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
    cdef double lt = 0.0
    # convert the strings to pointers once
    cdef const char* c_targ   = target
    cdef const char* c_ref    = ref
    cdef const char* c_abcorr = abcorr
    cdef const char* c_obs    = obs
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_ptarg = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_ptarg = p_ptarg
    spkpos_c(
        c_targ, 
        et, 
        c_ref, 
        c_abcorr, 
        c_obs, 
        &c_ptarg[0], 
        &lt
    )
    return p_ptarg, lt
    

@boundscheck(False)
@wraparound(False)
def spkpos_v(
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
    # initialize c variables
    cdef const double[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    cdef double[3] c_ptarg 
    cdef double c_lt 
    # convert the strings to pointers once
    cdef const char * c_targ   = targ
    cdef const char * c_ref    = ref
    cdef const char * c_abcorr = abcorr
    cdef const char * c_obs    = obs
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_ptargs = np.empty((n,3), dtype=np.double, order='C')
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_lts = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_ptargs = p_ptargs
    cdef np.double_t[::1]   c_lts = p_lts
    # main loop
    for i in range(n):
        spkpos_c(
            c_targ, 
            c_ets[i],
            c_ref, 
            c_abcorr, 
            c_obs, 
            &c_ptargs[i,0], 
            &c_lts[i]
        )
    # return results
    return p_ptargs, p_lts


@boundscheck(False)
@wraparound(False)
def spkssb(
    int targ,
    double et,
    str ref,
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
    cdef double c_et = et
    # convert the strings to pointers once
    cdef const char* c_ref   = ref
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_state = np.empty(6, dtype=np.double, order='C')
    cdef np.double_t[::1] c_state = p_state
    # perform the call
    spkssb_c(
        targ,
        c_et,
        c_ref,
        &c_state[0],
    )
    # return output
    return p_state


@boundscheck(False)
@wraparound(False)
def spkssb_v(
    int targ,
    double[::1] ets,
    str ref,
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
    cdef const double[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert the strings to pointers once
    cdef const char* c_ref   = ref
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_states = np.empty((n,6), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_states = p_states
    # perform the call
    for i in range(n):
        spkssb_c(
            targ,
            c_ets[i],
            c_ref,
            &c_states[i,0],
        )
    # return output
    return p_states


def str2et(
    str time
    ):
    """
    Convert a string representing an epoch to a double precision
    value representing the number of TDB seconds past the J2000
    epoch corresponding to the input epoch.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/str2et_c.html

    :param time: A string representing an epoch.
    :return: The equivalent value in seconds past J2000, TDB.
    """
    cdef double et
    cdef const char * c_time = time
    str2et_c(
        c_time, 
        &et
    )
    return et
    

@boundscheck(False)
@wraparound(False)
def str2et_v(
    np.ndarray times
    ):
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
    # initialize output
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_ets = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_ets = p_ets
    #main loop
    for i in range(n):
        # should this be unicode? or bytes? <unicode> seemed to work but unsure if safe
        str2et_c(
            times[i], 
            &c_ets[i]
        )
    # return results
    return p_ets

# TODO need error check, need found exception thrower in cython
@wraparound(False)
@boundscheck(False)
def sincpt(
    str method,
    str target,
    double et,
    str fixref, 
    str abcorr,
    str obsrvr,
    str dref,
    double[::1] dvec
    ):
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
    cdef const char * c_method = method
    cdef const char * c_target = target
    cdef const char * c_fixref = fixref
    cdef const char * c_abcorr = abcorr
    cdef const char * c_obsrvr = obsrvr
    cdef const char * c_dref   = dref
    # Allocate output floats and arrays with appropriate shapes.
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_spoint = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_spoint = p_spoint
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_srfvec = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_srfvec = p_srfvec
    cdef double c_trgepc
    cdef bint c_found 
    # perform the call
    sincpt_c(
        c_method,
        c_target,
        et,
        c_fixref,
        c_abcorr,
        c_obsrvr,
        c_dref,
        &dvec[0],
        &c_spoint[0],
        &c_trgepc,
        &c_srfvec[0],
        &c_found
    )
    # return results
    return p_spoint, c_trgepc, p_srfvec, c_found


# TODO need error check, need found exception thrower in cython
@wraparound(False)
@boundscheck(False)
def sincpt_v(
    str method,
    str target,
    double[::1] ets,
    str fixref, 
    str abcorr,
    str obsrvr,
    str dref,
    double[::1] dvec
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
    cdef const double[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert strings 
    cdef const char * c_method = method
    cdef const char * c_target = target
    cdef const char * c_fixref = fixref
    cdef const char * c_abcorr = abcorr
    cdef const char * c_obsrvr = obsrvr
    cdef const char * c_dref   = dref
    # Allocate output floats and arrays with appropriate shapes.
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_spoint = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_spoint = p_spoint 
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_srfvec = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_srfvec = p_srfvec 
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_trgepc = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1]   c_trgepc = p_trgepc 
    cdef np.ndarray[np.uint8_t, ndim=1, mode='c'] p_found = np.empty(n, dtype=np.bool_, order='C')
    cdef np.uint8_t[::1] c_found = p_found
    # perform the call
    for i in range(n):
        sincpt_c(
            c_method,
            c_target,
            c_ets[i],
            c_fixref,
            c_abcorr,
            c_obsrvr,
            c_dref,
            &dvec[0],
            &c_spoint[i,0],
            &c_trgepc[i],
            &c_srfvec[i,0],
            <SpiceBoolean *> &c_found[i]
        )
        # return results
    return p_spoint, p_trgepc, p_srfvec, p_found


@wraparound(False)
@boundscheck(False)
def subpnt(
    str method,
    str target, 
    double et, 
    str fixref, 
    str abcorr, 
    str obsrvr
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
    cdef const char * c_method = method
    cdef const char * c_target = target
    cdef const char * c_fixref = fixref
    cdef const char * c_abcorr = abcorr
    cdef const char * c_obsrvr = obsrvr
    # Allocate output floats and arrays with appropriate shapes.
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_spoint = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_spoint = p_spoint
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_srfvec = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_srfvec = p_srfvec
    cdef double trgepc
    # perform the call
    subpnt_c(
        c_method,
        c_target,
        et,
        c_fixref,
        c_abcorr,
        c_obsrvr,
        &c_spoint[0],
        &trgepc,
        &c_srfvec[0]
        )
    # return results
    return p_spoint, trgepc, p_srfvec


@boundscheck(False)
@wraparound(False)
def subpnt_v(
    str method,
    str target, 
    double[::1] ets, 
    str fixref, 
    str abcorr, 
    str obsrvr
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
    cdef const double[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert strings 
    cdef const char * c_method = method
    cdef const char * c_target = target
    cdef const char * c_fixref = fixref
    cdef const char * c_abcorr = abcorr
    cdef const char * c_obsrvr = obsrvr
    # Allocate output floats and arrays with appropriate shapes.
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_spoint = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_spoint = p_spoint
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_srfvec = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_srfvec = p_srfvec
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_trgepc = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_trgepc = p_trgepc
    # perform the call
    for i in range(n):
        subpnt_c(
            c_method,
            c_target,
            c_ets[i],
            c_fixref,
            c_abcorr,
            c_obsrvr,
            &c_spoint[i,0],
            &c_trgepc[i],
            &c_srfvec[i,0]
        )
    # return results
    return p_spoint, p_trgepc, p_srfvec


@wraparound(False)
@boundscheck(False)
def subslr(
    str method,
    str target, 
    double et, 
    str fixref, 
    str abcorr, 
    str obsrvr
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
    cdef const char * c_method = method
    cdef const char * c_target = target
    cdef const char * c_fixref = fixref
    cdef const char * c_abcorr = abcorr
    cdef const char * c_obsrvr = obsrvr
    # Allocate output floats and arrays with appropriate shapes.
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_spoint = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_spoint = p_spoint
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_srfvec = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_srfvec = p_srfvec
    cdef double trgepc
    # perform the call
    subslr_c(
        c_method,
        c_target,
        et,
        c_fixref,
        c_abcorr,
        c_obsrvr,
        &c_spoint[0],
        &trgepc,
        &c_srfvec[0]
        )
    # return results
    return p_spoint, trgepc, p_srfvec


@boundscheck(False)
@wraparound(False)
def subslr_v(
    str method,
    str target, 
    double[::1] ets, 
    str fixref, 
    str abcorr, 
    str obsrvr
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
    cdef const double[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert strings 
    cdef const char * c_method = method
    cdef const char * c_target = target
    cdef const char * c_fixref = fixref
    cdef const char * c_abcorr = abcorr
    cdef const char * c_obsrvr = obsrvr
    # Allocate output floats and arrays with appropriate shapes.
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_spoint = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_spoint = p_spoint
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_srfvec = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_srfvec = p_srfvec
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_trgepc = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_trgepc = p_trgepc
    # perform the call
    for i in range(n):
        subslr_c(
            c_method,
            c_target,
            c_ets[i],
            c_fixref,
            c_abcorr,
            c_obsrvr,
            &c_spoint[i,0],
            &c_trgepc[i],
            &c_srfvec[i,0]
        )
    # return results
    return p_spoint, p_trgepc, p_srfvec

@boundscheck(False)
@wraparound(False)
def sxform(
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
    cdef const char * c_fromstring = fromstring
    cdef const char * c_tostring = tostring
    # initialize output
    cdef np.ndarray[np.double_t, ndim=2, mode="c"] p_xform = np.empty((6,6), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_xform = p_xform
    sxform_c(
        c_fromstring, 
        c_tostring, 
        et, 
        <SpiceDouble (*)[6]> &c_xform[0,0]
    )
    return p_xform


@boundscheck(False)
@wraparound(False)
def sxform_v(
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
    cdef const double[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    cdef const char * c_fromstring = fromstring
    cdef const char * c_tostring = tostring
    # initialize output
    cdef np.ndarray[dtype=DOUBLE_t, ndim=3, mode="c"] p_xform = np.empty((n, 6, 6), dtype=np.double)
    cdef np.double_t[:,:,::1] c_xform = p_xform
    for i in range(n):
        sxform_c(
            c_fromstring, 
            c_tostring, 
            c_ets[i], 
            <SpiceDouble (*)[6]> &c_xform[i,0,0]
        )
    return p_xform

# T

@wraparound(False)
@boundscheck(False)
def tangpt(
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
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_tanpt = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_tanpt = p_tanpt 
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_srfpt = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_srfpt = p_srfpt
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_srfvec = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_srfvec = p_srfvec
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
    return p_tanpt, alt, vrange, p_srfpt, trgepc, p_srfvec


@boundscheck(False)
@wraparound(False)
def tangpt_v(    
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
    cdef const double[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert strings to ascii
    cdef const char * c_method = method
    cdef const char * c_target = target
    cdef const char * c_fixref = fixref
    cdef const char * c_abcorr = abcorr
    cdef const char * c_corloc = corloc
    cdef const char * c_obsrvr = obsrvr
    cdef const char * c_dref   = dref
    # Allocate output floats and arrays with appropriate shapes.
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_tanpt = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_tanpt = p_tanpt
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_alt = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_alt = p_alt
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_vrange = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_vrange = p_vrange
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_srfpt = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_srfpt = p_srfpt
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_srfvec = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_srfvec = p_srfvec
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_trgepc = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_trgepc = p_trgepc
    # perform the calls
    for i in range(n):
        tangpt_c(
            c_method, 
            c_target, 
            c_ets[i], 
            c_fixref, 
            c_abcorr,
            c_corloc,
            c_obsrvr,
            c_dref,
            &dvec[0],
            &c_tanpt[i,0],
            &c_alt[i],
            &c_vrange[i],
            &c_srfpt[i,0],
            &c_trgepc[i],
            &c_srfvec[i,0]
        )
    # return values
    return p_tanpt, p_alt, p_vrange, p_srfpt, p_trgepc, p_srfvec


def timout(
    double et, 
    str pictur
    ):
    """
    This vectorized routine converts an input epoch represented in TDB seconds
    past the TDB epoch of J2000 to a character string formatted to
    the specifications of a user's format picture.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/timout_c.html

    :param et: An epoch in seconds past the ephemeris epoch J2000.
    :param pictur: A format specification for the output string.
    :return: A string representation of the input epoch.
    """
    cdef const char * c_pictur = pictur 
    cdef char[TIMELEN] c_buffer
    timout_c(
        et, 
        c_pictur, 
        TIMELEN, 
        &c_buffer[0]
    )
    return PyUnicode_DecodeUTF8(c_buffer, strlen(c_buffer), "strict")


@boundscheck(False)
@wraparound(False)
def timout_v(
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
    cdef const double[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    cdef const char * c_pictur = pictur 
    cdef char[TIMELEN] c_buffer
     # initialize output
    cdef list output = [None] * n
    for i in range(n):
        timout_c(
            c_ets[i], 
            c_pictur, 
            TIMELEN, 
            &c_buffer[0]
        )
        output[i] = PyUnicode_DecodeUTF8(c_buffer, strlen(c_buffer), "strict")
    return np.asarray(output)


def trgsep(
    double et, 
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
    cdef const char * c_targ1   = targ1
    cdef const char * c_shape1  = shape1
    cdef const char * c_frame1  = frame1
    cdef const char * c_targ2   = targ2
    cdef const char * c_shape2  = shape2
    cdef const char * c_frame2  = frame2
    cdef const char * c_obsrvr  = obsrvr
    cdef const char * c_abcorr  = abcorr
    return trgsep_c(
        et, 
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
def trgsep_v(
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
    cdef const double[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t i, n = c_ets.shape[0] 
    cdef const char * c_targ1   = targ1
    cdef const char * c_shape1  = shape1
    cdef const char * c_frame1  = frame1
    cdef const char * c_targ2   = targ2
    cdef const char * c_shape2  = shape2
    cdef const char * c_frame2  = frame2
    cdef const char * c_obsrvr  = obsrvr
    cdef const char * c_abcorr  = abcorr
    # initialize output
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_angseps = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_angseps = p_angseps
    for i in range(n):
        c_angseps[i] = trgsep_c(
            c_ets[i], 
            c_targ1, 
            c_shape1, 
            c_frame1, 
            c_targ2, 
            c_shape2,
            c_frame2, 
            c_obsrvr, 
            c_abcorr
        )
    return p_angseps

# U

def unitim(
        double epoch,
        str insys,
        str outsys,
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
    cdef const char * c_insys = insys
    cdef const char * c_outsys = outsys
    return unitim_c(epoch, c_insys, c_outsys)


@boundscheck(False)
@wraparound(False)
def unitim_v(
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
    cdef const double[::1] c_epochs = np.ascontiguousarray(epochs)
    cdef Py_ssize_t i, n = c_epochs.shape[0]
    cdef const char * c_insys = insys
    cdef const char * c_outsys = outsys
    # initialize output
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_unitims = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_unitims = p_unitims
    # perform the actual call
    for i in range(n):
        c_unitims[i] = unitim_c(
            c_epochs[i], 
            c_insys, 
            c_outsys
        )
    return p_unitims


def unload(str file):
    """
    Unload a SPICE kernel.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/unload_c.html

    :param filename: The name of a kernel to unload.
    """
    cdef const char * c_file = file
    unload_c(c_file)


def utc2et(str utcstr):
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
def utc2et_v(
    np.ndarray utcstr
    ):
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
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_ets = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_ets = p_ets
    for i in range(n):
        utc2et_c(
            utcstr[i], 
            &c_ets[i]
        )
    return p_ets
