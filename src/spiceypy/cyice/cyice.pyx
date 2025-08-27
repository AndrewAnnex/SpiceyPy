# cython: language_level = 3
# cython: embedsignature = True
# cython: c_string_type = unicode
# cython: c_string_encoding = ascii
# cython: cdivision = True
# cython: profile = False
# cython: linetrace = False
# cython: warn.unused = True
# cython: warn.maybe_uninitialized = True
# cython: warn.multiple_declarators = True
# cython: show_performance_hints = True
# cython: always_allow_keywords = False

"""
The MIT License (MIT)

Copyright (c) [2015-2025] [Andrew Annex]

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

from libc.stdlib cimport malloc, free
from libc.string cimport strlen, memcpy
from cython      cimport boundscheck, wraparound
from cpython.float      cimport PyFloat_Check
from cpython.long       cimport PyLong_Check
from cpython.unicode    cimport PyUnicode_DecodeUTF8, PyUnicode_Check, PyUnicode_AsASCIIString
from cpython.bool       cimport PyBool_Check, PyBool_FromLong
from cpython.tuple      cimport PyTuple_GET_SIZE

from cython.parallel import prange

import functools
from typing import Annotated, Literal

import numpy as np
cimport numpy as np
np.import_array()

DEF _default_len_out = 256

DEF TIMELEN = 64
DEF TLELEN = 70

DEF SHORTLEN = 32
DEF EXPLAINLEN = 128
DEF LONGLEN = 2048
DEF TRACELEN = 256

ctypedef fused double_arr_t:
    np.double_t[:]
    np.double_t[::1]

ctypedef fused int_arr_t:
    np.int32_t[:]
    np.int32_t[::1]
    np.int64_t[:]
    np.int64_t[::1]

ctypedef fused char_arr_t:
    np.uint8_t[:]
    np.uint8_t[::1]

ctypedef fused bool_arr_t:
    np.uint8_t[:]
    np.uint8_t[::1]


# typing stuff
StringArray = np.typing.NDArray[np.str_]
BoolArray   = np.typing.NDArray[np.uint8]
IntArray    = np.typing.NDArray[np.int32]
DoubleArray = np.typing.NDArray[np.double]
String_N    = Annotated[StringArray, Literal["N"]]
Found_N     = Annotated[BoolArray, Literal["N"]]
Int_N       = Annotated[IntArray, Literal["N"]]
Double_N    = Annotated[DoubleArray, Literal["N"]]
Vector      = Annotated[DoubleArray, Literal[3]]
Vector_N    = Annotated[DoubleArray, Literal["N", 3]]
Cylindrical_N    = Annotated[DoubleArray, Literal["N", 3]]
Geodetic_N       = Annotated[DoubleArray, Literal["N", 3]]
Latitudinal_N    = Annotated[DoubleArray, Literal["N", 3]]
Planetographic_N = Annotated[DoubleArray, Literal["N", 3]]
Rectangular_N    = Annotated[DoubleArray, Literal["N", 3]]
Spherical_N      = Annotated[DoubleArray, Literal["N", 3]]
State       = Annotated[DoubleArray, Literal[6]]
State_N     = Annotated[DoubleArray, Literal["N", 6]]
Matrix      = Annotated[DoubleArray, Literal[3, 3]]
Matrix_3    = Annotated[DoubleArray, Literal[3, 3]]
Matrix_6    = Annotated[DoubleArray, Literal[6, 6]]
Matrix_N    = Annotated[DoubleArray, Literal["N", 3, 3]]
Matrix_N_3  = Annotated[DoubleArray, Literal["N", 3, 3]]
Matrix_N_6  = Annotated[DoubleArray, Literal["N", 6, 6]]


from .cyice cimport *
from spiceypy import config
from spiceypy.utils.exceptions import dynamically_instantiate_spiceyerror, NotFoundError, SpiceyError


# support functions


cpdef void check_for_spice_error():
    """
    Internal decorator function to check spice error system for failed calls

    :param f: function
    :raise SpiceyError:
    """
    cdef char[SHORTLEN]   shortmsg
    cdef char[EXPLAINLEN] explain
    cdef char[LONGLEN]    longmsg
    cdef char[TRACELEN]   traceback
    cdef object py_shortmsg
    cdef object py_explain
    cdef object py_longmsg
    cdef object py_traceback
    if failed_c():
        with nogil:
            getmsg_c("SHORT", SHORTLEN, shortmsg)
            getmsg_c("EXPLAIN", EXPLAINLEN, explain)
            getmsg_c("LONG", LONGLEN, longmsg)
            qcktrc_c(TRACELEN, traceback)
            reset_c()
            shortmsg[SHORTLEN - 1] = b'\0'
            explain[EXPLAINLEN - 1] = b'\0'
            longmsg[LONGLEN - 1] = b'\0'
            traceback[TRACELEN - 1] = b'\0'
        py_shortmsg  = PyUnicode_DecodeUTF8(shortmsg, strlen(shortmsg), 'replace')
        py_explain   = PyUnicode_DecodeUTF8(explain, strlen(explain), 'replace')
        py_longmsg   = PyUnicode_DecodeUTF8(longmsg, strlen(longmsg), 'replace')
        py_traceback = PyUnicode_DecodeUTF8(traceback, strlen(traceback), 'replace')
        raise dynamically_instantiate_spiceyerror(
          py_shortmsg,
          py_explain,
          py_longmsg,
          py_traceback
        )


@boundscheck(False)
@wraparound(False)
cdef inline bint _all(np.uint8_t[::1] arr) nogil:
    cdef Py_ssize_t i
    for i in prange(arr.shape[0], nogil=True):
        if arr[i] == 0:
            return False
    return True


@boundscheck(False)
@wraparound(False)
cdef inline char[:, ::1] make_char_array(np.ndarray input_array, int max_len):
    cdef const char *c_encoded
    cdef bytes encoded
    cdef Py_ssize_t elen, i, n = input_array.shape[0]
    cdef char[:, ::1] output = np.zeros((n, max_len), dtype=np.uint8, order='C') 
    for i in range(n):
        encoded = input_array[i].encode('ascii') 
        elen = len(encoded)
        c_encoded = encoded 
        if elen >= max_len:
            raise ValueError(f"String at index {i} is too long for max_len={max_len}")
        memcpy(&output[i, 0], c_encoded, min(elen, max_len - 1))
        output[i, min(elen, max_len - 1)] = 0  # null-terminate
    return output


@wraparound(False)
@boundscheck(False)
def cyice_found_exception_thrower(f):
    """
    Decorator for wrapping functions that use status codes
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        cdef tuple py_res = f(*args, **kwargs)
        cdef object found
        cdef np.uint8_t c_found
        cdef np.uint8_t[::1] found_arr
        cdef Py_ssize_t n, last
        cdef bint all_true = True
        # first check if the config to see if shortcut can be run. TODO move config to cyice?
        if not config.catch_false_founds:
            return py_res
        else:
            n = PyTuple_GET_SIZE(py_res)
            last = n - 1
            # get the last value which is the
            found = py_res[last]
            # if we have a scalar boolean
            if PyBool_Check(<object>found):
                # cast to bint
                # and perform the bool test
                c_found = found
                if c_found == 0:
                    # if true raise the exception
                    raise NotFoundError(
                        "Spice returns not found for function: {}".format(f.__name__),
                        found=found,
                    )
            else:
                # else assume we have a numpy array, so cast it to np.uint8_t
                found_arr = found
                # compute if all true using cython optimized version and prange
                all_true = _all(found_arr)
                # and perform the bool test
                if all_true < 1:
                    # if true raise exception
                    raise NotFoundError(
                        f"Spice returns not found in a series of calls for function: {f.__name__}",
                        found=found,
                    )
            # at this point we know all found flags were true, so get the length of the tuple
            # slice off the "found" flag
            if last == 1:
                # return single value unwrapped
                return py_res[0]
            else:
                # return the remaining elements
                return py_res[0:last]
    return wrapper


# A

@boundscheck(False)
@wraparound(False)
cpdef tuple[np.ndarray, float] azlcpo_s(
    const char * method,
    const char * target,
    double et,
    const char * abcorr,
    SpiceBoolean azccw,
    SpiceBoolean elplsz,
    double[::1] obspos,
    const char * obsctr,
    const char * obsref
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.azlcpo`

    Return the azimuth/elevation coordinates of a specified target
    relative to an "observer," where the observer has constant
    position in a specified reference frame. The observer's position
    is provided by the calling program rather than by loaded SPK
    files.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/azlcpo_c.html

    :param method: Method to obtain the surface normal vector.
    :param target: Name of target ephemeris object.
    :param et: Observation epoch in ephemeris seconds past J2000 TDB.
    :param abcorr: Aberration correction.
    :param azccw: Flag indicating how azimuth is measured.
    :param elplsz: Flag indicating how elevation is measured.
    :param obspos: Observer position relative to center of motion.
    :param obsctr: Center of motion of observer.
    :param obsref: Body fixed body centered frame of observer's center.
    :return: State of target with respect to observer, in azimuth/elevation coordinates. and One way light time between target and observer.
    """
    # allocate outputs
    cdef double c_lt = 0.0
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_state = np.empty(6, dtype=np.double, order='C')
    cdef np.double_t[::1] c_state = p_state
    azlcpo_c(
        method,
        target,
        et,
        abcorr,
        <SpiceBoolean> azccw, 
        <SpiceBoolean> elplsz, 
        &obspos[0],
        obsctr,
        obsref,
        &c_state[0],
        &c_lt
    )
    check_for_spice_error()
    return p_state, c_lt


@boundscheck(False)
@wraparound(False)
cpdef tuple[np.ndarray, np.ndarray] azlcpo_v(
    const char* method,
    const char* target,
    double[::1] ets,
    const char* abcorr,
    SpiceBoolean azccw,
    SpiceBoolean elplsz,
    double[:,::1] obspos,
    const char* obsctr,
    const char* obsref
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.azlcpo`

    Return the azimuth/elevation coordinates of a specified target
    relative to an "observer," where the observer has constant
    position in a specified reference frame. The observer's position
    is provided by the calling program rather than by loaded SPK
    files.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/azlcpo_c.html

    :param method: Method to obtain the surface normal vector.
    :param target: Name of target ephemeris object.
    :param ets: Observation epochs in ephemeris seconds past J2000 TDB.
    :param abcorr: Aberration correction.
    :param azccw: Flag indicating how azimuth is measured.
    :param elplsz: Flag indicating how elevation is measured.
    :param obspos: Observer positions relative to center of motion.
    :param obsctr: Center of motion of observer.
    :param obsref: Body fixed body centered frame of observer's center.
    :return: States of target with respect to observer, in azimuth/elevation coordinates. and One way light times between target and observer.
    """
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef const np.double_t[:,::1] c_obspos = np.ascontiguousarray(obspos, dtype=np.double)
    cdef Py_ssize_t i, j, n, m = 0
    n = c_ets.shape[0]
    m = c_obspos.shape[0]
    cdef double c_et_r = 0.0
    cdef SpiceBoolean c_azccw  = <SpiceBoolean> azccw
    cdef SpiceBoolean c_elplsz = <SpiceBoolean> elplsz
    # allocate outputs
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_lts = np.empty((n,m), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_lts = p_lts
    cdef np.ndarray[np.double_t, ndim=3, mode='c'] p_states = np.empty((n,m,6), dtype=np.double, order='C')
    cdef np.double_t[:,:,::1] c_states = p_states
    # make the call
    with nogil:
        for i in range(n):
            c_et_r = c_ets[i]
            for j in range(m):
                azlcpo_c(
                    method,
                    target,
                    c_et_r,
                    abcorr,
                    c_azccw, 
                    c_elplsz, 
                    &obspos[j,0],
                    obsctr,
                    obsref,
                    &c_states[i,j,0],
                    &c_lts[i,j]
                )
    check_for_spice_error()
    return p_states, p_lts


def azlcpo(
    method: str,
    target: str,
    et: float | double[::1],
    abcorr: str,
    azccw: bool,
    elplsz: bool,
    obspos: double[::1] | double[:,::1],
    obsctr: str,
    obsref: str,
    ) -> tuple[np.ndarray, float] | tuple[np.ndarray, np.ndarray]:
    """
    Return the azimuth/elevation coordinates of a specified target
    relative to an "observer," where the observer has constant
    position in a specified reference frame. The observer's position
    is provided by the calling program rather than by loaded SPK
    files.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/azlcpo_c.html

    :param method: Method to obtain the surface normal vector.
    :param target: Name of target ephemeris object.
    :param ets: Observation epochs in ephemeris seconds past J2000 TDB.
    :param abcorr: Aberration correction.
    :param azccw: Flag indicating how azimuth is measured.
    :param elplsz: Flag indicating how elevation is measured.
    :param obspos: Observer positions relative to center of motion.
    :param obsctr: Center of motion of observer.
    :param obsref: Body fixed body centered frame of observer's center.
    :return: States of target with respect to observer, in azimuth/elevation coordinates. and One way light times between target and observer.
    """
    if PyFloat_Check(et):
        return azlcpo_s(method, target, et, abcorr, azccw, elplsz, obspos, obsctr, obsref)
    else:
        return azlcpo_v(method, target, et, abcorr, azccw, elplsz, obspos, obsctr, obsref)


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=1, mode='c'] azlrec_s(
    double inrange, 
    double az, 
    double el,
    SpiceBoolean azccw,
    SpiceBoolean elplsz
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.azlrec`

    Convert from range, azimuth and elevation of a point to
    rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/azlrec_c.html

    :param inrange: Distance of the point from the origin.
    :param az: Azimuth in radians.
    :param el: Elevation in radians.
    :param azccw: Flag indicating how azimuth is measured.
    :param elplsz: Flag indicating how elevation is measured.
    :return: Rectangular coordinates of a point.
    """
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_rec = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_rec = p_rec
    azlrec_c(
        inrange, 
        az, 
        el, 
        <SpiceBoolean> azccw, 
        <SpiceBoolean> elplsz, 
        &c_rec[0],
    )
    return p_rec


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=2, mode='c'] azlrec_v(
    double[::1] inrange, 
    double[::1] az, 
    double[::1] el,
    SpiceBoolean azccw,
    SpiceBoolean elplsz
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.azlrec`

    Convert from range, azimuth and elevation of a point to
    rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/azlrec_c.html

    :param range: Distance of the point from the origin.
    :param az: Azimuth in radians.
    :param el: Elevation in radians.
    :param azccw: Flag indicating how azimuth is measured.
    :param elplsz: Flag indicating how elevation is measured.
    :return: Rectangular coordinates of a point.
    """
    cdef SpiceBoolean c_azccw  = <SpiceBoolean> azccw 
    cdef SpiceBoolean c_elplsz = <SpiceBoolean> elplsz
    cdef const np.double_t[::1] c_inrange = np.ascontiguousarray(inrange, dtype=np.double)
    cdef Py_ssize_t i, n = inrange.shape[0]
    cdef const np.double_t[::1] c_az = np.ascontiguousarray(az, dtype=np.double)
    cdef const np.double_t[::1] c_el = np.ascontiguousarray(el, dtype=np.double)
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_rec = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_rec = p_rec
    # TODO fix strides lookups below
    with nogil:
        for i in range(n):
            azlrec_c(
                c_inrange[i], 
                c_az[i],
                c_el[i],
                c_azccw,
                c_elplsz, 
                &c_rec[i, 0]
            )
    return p_rec


def azlrec(
    inrange: float | double[:,::1],
    az: float | double[:,::1], 
    el: float | double[:,::1],  
    azccw: bool | SpiceBoolean, 
    elplsz: bool | SpiceBoolean
    ) -> Vector | Rectangular_N:
    """
    Convert from range, azimuth and elevation of a point to
    rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/azlrec_c.html

    :param inrange: Distance of the point from the origin.
    :param az: Azimuth in radians.
    :param el: Elevation in radians.
    :param azccw: Flag indicating how azimuth is measured.
    :param elplsz: Flag indicating how elevation is measured.
    :return: Rectangular coordinates of a point.
    """
    if PyFloat_Check(inrange):
        return azlrec_s(inrange, az, el, azccw, elplsz)
    else:
        return azlrec_v(inrange, az, el, azccw, elplsz)


# B

def b1900() -> float:
    """
    Return the Julian Date corresponding to Besselian Date 1900.0.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/b1900_c.html

    :return: The Julian Date corresponding to Besselian Date 1900.0.
    """
    return b1900_c()


def b1950() -> float:
    """
    Return the Julian Date corresponding to Besselian Date 1950.0.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/b1950_c.html

    :return: The Julian Date corresponding to Besselian Date 1950.0.
    """
    return b1950_c()

# C


@boundscheck(False)
@wraparound(False)
@cyice_found_exception_thrower
def ckgp_s(
    int inst,
    double sclkdp,
    double tol,
    const char* ref
    ) -> tuple[Matrix_3, float, bool] | tuple[Matrix_3, float]:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.ckgp_s`
    
    Get pointing (attitude) for a specified spacecraft clock time.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/ckgp_c.html

    :param inst: NAIF ID of instrument, spacecraft, or structure.
    :param sclkdp: Encoded spacecraft clock time.
    :param tol: Time tolerance.
    :param ref: Reference frame.
    :return:
            C-matrix pointing data,
            Output encoded spacecraft clock time
            Found flag (possibly)
    """
    # initialize c variables
    cdef double c_clkout = 0.0
    cdef SpiceBoolean c_found = SPICEFALSE
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_cmat = np.empty((3, 3), dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_cmat = p_cmat
    # perform the call
    ckgp_c(
        inst,
        sclkdp,
        tol,
        ref,
        <SpiceDouble (*)[3]> &c_cmat[0, 0],
        &c_clkout,
        <SpiceBoolean *> &c_found
    )
    check_for_spice_error()

    return p_cmat, c_clkout, PyBool_FromLong(c_found)


@boundscheck(False)
@wraparound(False)
@cyice_found_exception_thrower
def ckgp_v(
    int inst,
    double[::1] sclkdps,
    double tol,
    const char* c_ref
    )-> tuple[Matrix_N, Double_N, Found_N] | tuple[Matrix_N, Double_N]:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.ckgp`

    Get pointing (attitude) for specified spacecraft clock times.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/ckgp_c.html

    :param inst: NAIF ID of instrument, spacecraft, or structure.
    :param sclkdps: Encoded spacecraft clock times.
    :param tol: Time tolerance.
    :param ref: Reference frame.
    :return:
            C-matrix pointing data,
            Output encoded spacecraft clock time
            Found flags (possibly)
    """
    # initialize c variables
    cdef const np.double_t[::1] c_sclkdps = np.ascontiguousarray(sclkdps, dtype=np.double)
    cdef Py_ssize_t i, n = c_sclkdps.shape[0]
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=3, mode='c'] p_cmat   = np.empty((n, 3, 3), dtype=np.double, order='C')
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_clkout = np.empty(n, dtype=np.double, order='C')
    cdef np.ndarray[np.uint8_t, ndim=1, mode='c'] p_found   = np.empty(n, dtype=np.uint8, order='C')
    cdef np.double_t[:, :, ::1] c_cmat = p_cmat
    cdef np.double_t[::1] c_clkout   = p_clkout
    cdef np.uint8_t[::1] c_found     = p_found
    # perform the call
    with nogil:
        for i in range(n):
            ckgp_c(
                inst,
                c_sclkdps[i],
                tol,
                c_ref,
                <SpiceDouble (*)[3]> &c_cmat[i, 0, 0],
                &c_clkout[i],
                <SpiceBoolean *> &c_found[i]
            )
    check_for_spice_error()

    return p_cmat, p_clkout, p_found


def ckgp(
    inst: int,
    sclkdp: float | float[::1],
    tol: float,
    ref: str
    )-> tuple[Matrix_3, float, bool] | tuple[Matrix_3, float] | tuple[Matrix_N, Vector, Found_N] | tuple[Matrix_N, Vector_N]:
    """
    Get pointing (attitude) for specified spacecraft clock times.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/ckgp_c.html

    :param inst: NAIF ID of instrument, spacecraft, or structure.
    :param sclkdps: Encoded spacecraft clock times.
    :param tol: Time tolerance.
    :param ref: Reference frame.
    :return:
            C-matrix pointing data,
            Output encoded spacecraft clock time
            Found flag(s) (possibly)
    """
    if PyFloat_Check(sclkdp):
        return ckgp_s(inst, sclkdp, tol, ref)
    else:
        return ckgp_v(inst, sclkdp, tol, ref)


@boundscheck(False)
@wraparound(False)
@cyice_found_exception_thrower
def ckgpav_s(
    int    inst,
    double sclkdp,
    double tol,
    const char* c_ref
    ) -> tuple[Matrix_3, Vector, float, bool] | tuple[Matrix_3, Vector, float]:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.ckgpav`

    Get pointing (attitude) and angular velocity
    for a specified spacecraft clock time.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/ckgpav_c.html

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
    cdef int c_inst = inst
    cdef double c_sclkdp = sclkdp
    cdef double c_tol = tol
    cdef double c_clkout = 0.0
    cdef SpiceBoolean c_found = SPICEFALSE
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_cmat = np.empty((3, 3), dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_cmat = p_cmat
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_av   = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1]   c_av   = p_av
    # perform the call
    ckgpav_c(
        c_inst,
        c_sclkdp,
        c_tol,
        c_ref,
        <SpiceDouble (*)[3]> &c_cmat[0, 0],
        &c_av[0],
        &c_clkout,
        <SpiceBoolean *> &c_found
    )
    check_for_spice_error()

    return p_cmat, p_av, c_clkout, PyBool_FromLong(c_found)


@boundscheck(False)
@wraparound(False)
@cyice_found_exception_thrower
def ckgpav_v(
    int    inst,
    double[::1] sclkdps,
    double tol,
    const char* c_ref
    ) -> tuple[Matrix_N, Vector_N, Double_N, Found_N] | tuple[Matrix_N, Vector_N, Double_N]:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.ckgpav`

    Get pointing (attitude) and angular velocity
    for specified spacecraft clock times.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/ckgpav_c.html

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
    cdef int c_inst = inst
    cdef double c_tol = tol
    cdef const np.double_t[::1] c_sclkdps = np.ascontiguousarray(sclkdps, dtype=np.double)
    cdef Py_ssize_t i, n = c_sclkdps.shape[0]
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=3, mode='c'] p_cmat = np.empty((n, 3, 3), dtype=np.double, order='C')
    cdef np.double_t[:, :, ::1] c_cmat = p_cmat
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_av   = np.empty((n, 3), dtype=np.double, order='C')
    cdef np.double_t[:, ::1]   c_av = p_av
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_clkout = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_clkout = p_clkout
    cdef np.ndarray[np.uint8_t, ndim=1, mode='c'] p_found = np.empty(n, dtype=np.uint8, order='C')
    cdef np.uint8_t[::1] c_found = p_found
    # perform the call
    with nogil:
        for i in range(n):
            ckgpav_c(
                c_inst,
                c_sclkdps[i],
                c_tol,
                c_ref,
                <SpiceDouble (*)[3]> &c_cmat[i, 0, 0],
                &c_av[i, 0],
                &c_clkout[i],
                <SpiceBoolean *> &c_found[i]
            )
    check_for_spice_error()

    return p_cmat, p_av, p_clkout, p_found


def ckgpav(
    inst: int,
    sclkdp: float | float[::1],
    tol: float,
    ref: str
    ) -> tuple[Matrix_3, Vector, float, bool] | tuple[Matrix_3, Vector, float] | tuple[Matrix_N, Vector_N, Double_N, Found_N] | tuple[Matrix_N, Vector_N, Double_N]:
    """
    Get pointing (attitude) and angular velocity
    for a specified spacecraft clock time.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/ckgpav_c.html

    :param inst: NAIF ID of instrument, spacecraft, or structure.
    :param sclkdp: Encoded spacecraft clock time.
    :param tol: Time tolerance.
    :param ref: Reference frame.
    :return:
            C-matrix pointing data,
            Angular velocity vector,
            Output encoded spacecraft clock time.
    """
    if PyFloat_Check(sclkdp):
        return ckgpav_s(inst, sclkdp, tol, ref)
    else:
        return ckgpav_v(inst, sclkdp, tol, ref)


def clight() -> float:
    """
    Return the speed of light in a vacuum (IAU official value, in km/sec).

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/clight_c.html

    :return: The function returns the speed of light in vacuum (km/sec).
    """
    return clight_c()


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=1, mode='c'] conics_s(
    double[::1] elts,
    double et,
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.conics`

    Determine the state (position, velocity) of an orbiting body
    from a set of elliptic, hyperbolic, or parabolic orbital
    elements.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/conics_c.html

    :param elts: Conic elements, units are km, rad, rad/sec, km**3/sec**2.
    :param et: Input time in ephemeris seconds J2000.
    :return: State of orbiting body at et (x, y, z, dx/dt, dy/dt, dz/dt).
    """
    cdef const np.double_t[::1] c_elts = np.ascontiguousarray(elts, dtype=np.double)
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_state = np.empty(6, dtype=np.double, order='C')
    cdef np.double_t[::1] c_state = p_state
    conics_c(
        &c_elts[0],
        et,
        &c_state[0],
    )
    check_for_spice_error()
    return p_state


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=2, mode='c'] conics_v(
    double[:,::1] elts,
    double[::1] ets,
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.conics`

    Determine the state (position, velocity) of an orbiting body
    from a set of elliptic, hyperbolic, or parabolic orbital
    elements.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/conics_c.html

    :param elts: Conic elements, units are km, rad, rad/sec, km**3/sec**2. 1 per et
    :param ets: Input times in ephemeris seconds J2000.
    :return: State of orbiting body at et (x, y, z, dx/dt, dy/dt, dz/dt).
    """
    cdef const np.double_t[:,::1] c_elts = np.ascontiguousarray(elts, dtype=np.double)
    cdef Py_ssize_t i, n = c_elts.shape[0]
    cdef np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_states = np.empty((n,6), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_states = p_states
    # main loop
    with nogil:
        for i in range(n):
            conics_c(
                &c_elts[i,0],
                c_ets[i],
                &c_states[i,0],
            )
    check_for_spice_error()
    return p_states


def conics(
    elts: double[::1] | double[:,::1],
    et: float | double[::1],
    )-> State | State_N:
    """
    Determine the state (position, velocity) of an orbiting body
    from a set of elliptic, hyperbolic, or parabolic orbital
    elements.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/conics_c.html

    :param elts: Conic elements, units are km, rad, rad/sec, km**3/sec**2.
    :param et: Input time in ephemeris seconds J2000.
    :return: State of orbiting body at et (x, y, z, dx/dt, dy/dt, dz/dt).
    """
    if PyFloat_Check(et):
        return conics_s(elts, et)
    else:
        return conics_v(elts, et)


def convrt_s(
    double x,
    str inunit,
    str outunit
    )-> float:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.convrt`

    Take a measurement X, the units associated with
    X, and units to which X should be converted; return Y
    the value of the measurement in the output units.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/convrt_c.html

    :param x: Number representing a measurement in some units.
    :param inunit: The units in which x is measured.
    :param outunit: Desired units for the measurement.
    :return: The measurment in the desired units.
    """
    cdef double c_x = x
    cdef double c_out = 0.0
    cdef const char* c_inunit = inunit
    cdef const char* c_outunit = outunit
    convrt_c(
        c_x,
        c_inunit,
        c_outunit,
        &c_out
    )
    check_for_spice_error()
    return c_out


@boundscheck(False)
@wraparound(False)
def convrt_v(
    double[::1] x,
    str inunit,
    str outunit
    ) -> Double_N:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.convrt`

    Take measurements X, the units associated with each
    X, and units to which each X should be converted; return Y
    the values of the measurements in the output units.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/convrt_c.html

    :param x: Numbers representing a measurement in some units.
    :param inunit: The units in which x is measured.
    :param outunit: Desired units for the measurement.
    :return: The measurment in the desired units.
    """
    cdef const np.double_t[::1] c_x = np.ascontiguousarray(x, dtype=np.double)
    cdef Py_ssize_t i, n = c_x.shape[0]
    cdef const char* c_inunit = inunit
    cdef const char* c_outunit = outunit
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_outs = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_outs = p_outs
    # main loop
    with nogil:
        for i in range(n):
            convrt_c(
                c_x[i],
                c_inunit,
                c_outunit,
                &c_outs[i]
            )
    check_for_spice_error()
    return p_outs


def convrt(
    x: float | float[::1],
    inunit:  str,
    outunit: str
    )-> float | Double_N:
    """
    Take a measurement X, the units associated with
    X, and units to which X should be converted; return Y
    the value of the measurement in the output units.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/convrt_c.html

    :param x: Number representing a measurement in some units.
    :param inunit: The units in which x is measured.
    :param outunit: Desired units for the measurement.
    :return: The measurment in the desired units.
    """
    if PyFloat_Check(x):
        return convrt_s(x, inunit, outunit)
    else:
        return convrt_v(x, inunit, outunit)


cpdef tuple[float, float, float] cyllat_s(
    r: float, 
    clon: float, 
    z: float
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.cyllat`

    Convert from cylindrical to latitudinal coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/cyllat_c.html

    :param r: Distance of point from z axis.
    :param clon: Cylindrical angle of point from XZ plane (radians).
    :param z: Height of point above XY plane.
    :return: Distance, Longitude (radians), and Latitude of point (radians).
    """
    cdef double radius = 0.0
    cdef double lon    = 0.0
    cdef double lat    = 0.0
    cyllat_c(
        r, 
        clon,
        z,
        &radius, 
        &lon, 
        &lat, 
    )
    return radius, lon, lat


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=2, mode='c'] cyllat_v(
    const double[::1] r, 
    const double[::1] clon, 
    const double[::1] z
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.cyllat`

    Convert from cylindrical to latitudinal coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/cyllat_c.html

    :param r: Distance of point from z axis.
    :param clon: Cylindrical angle of point from XZ plane (radians).
    :param z: Height of point above XY plane.
    :return: Distance, Longitude (radians), and Latitude of point (radians).
    """
    cdef const np.double_t[::1] c_r = np.ascontiguousarray(r, dtype=np.double)
    cdef Py_ssize_t i, n = c_r.shape[0]
    cdef const np.double_t[::1] c_clon = np.ascontiguousarray(clon, dtype=np.double)
    cdef const np.double_t[::1] c_z = np.ascontiguousarray(z, dtype=np.double)
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_lat = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_lat = p_lat
    # TODO fix strides lookups below
    with nogil:
        for i in range(n):
            cyllat_c(
                c_r[i], 
                c_clon[i], 
                c_z[i], 
                <SpiceDouble *> &c_lat[i,0], 
                <SpiceDouble *> &c_lat[i,1],
                <SpiceDouble *> &c_lat[i,2]
            )
    return p_lat


def cyllat(
    r: float | double[::1], 
    clon: float | double[::1], 
    z: float | double[::1]
    ) -> tuple[float, float, float] | Vector_N:
    """
    Convert from cylindrical to latitudinal coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/cyllat_c.html

    :param r: Distance of point from z axis.
    :param clon: Cylindrical angle of point from XZ plane (radians).
    :param z: Height of point above XY plane.
    :return: Distance, Longitude (radians), and Latitude of point (radians).
    """
    if PyFloat_Check(r):
        return cyllat_s(r, clon, z)
    else:
        return cyllat_v(r, clon, z)


cpdef np.ndarray[np.double_t, ndim=1, mode='c'] cylrec_s(
    r: float, 
    lon: float, 
    z: float
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.cylrec`

    Convert from cylindrical to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/cylrec_c.html

    :param r: Distance of a point from z axis.
    :param lon: Angle (radians) of a point from xZ plane.
    :param z: Height of a point above xY plane.
    :return: Rectangular coordinates of the point.
    """
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_rec = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_rec = p_rec
    cylrec_c(
        r, 
        lon, 
        z, 
        &c_rec[0],
    )
    return p_rec


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=2, mode='c'] cylrec_v(
    const double[::1] r, 
    const double[::1] lon, 
    const double[::1] z
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.cylrec`

    Convert from cylindrical to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/cylrec_c.html

    :param r: Distance of a point from z axis.
    :param lon: Angle (radians) of a point from xZ plane.
    :param z: Height of a point above xY plane.
    :return: Rectangular coordinates of the point.
    """
    cdef const np.double_t[::1] c_r = np.ascontiguousarray(r, dtype=np.double)
    cdef Py_ssize_t i, n = c_r.shape[0]
    cdef const np.double_t[::1] c_lon = np.ascontiguousarray(lon, dtype=np.double)
    cdef const np.double_t[::1] c_z   = np.ascontiguousarray(z, dtype=np.double)
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_rec = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_rec = p_rec
    # TODO fix strides lookups below
    with nogil:
        for i in range(n):
            cylrec_c(
                c_r[i], 
                c_lon[i], 
                c_z[i], 
                &c_rec[i, 0]
            )
    return p_rec


def cylrec(
    r: float | double[::1], 
    lon: float | double[::1], 
    z: float | double[::1]
    ) -> Vector | Vector_N:
    """
    Convert from cylindrical to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/cylrec_c.html

    :param r: Distance of a point from z axis.
    :param lon: Angle (radians) of a point from xZ plane.
    :param z: Height of a point above xY plane.
    :return: Rectangular coordinates of the point.
    """
    if PyFloat_Check(r):
        return cylrec_s(r, lon, z)
    else:
        return cylrec_v(r, lon, z)


cpdef tuple[float, float, float] cylsph_s(
    r: float, 
    clon: float, 
    z: float
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.cylsph`

    Convert from cylindrical to spherical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/cylsph_c.html

    :param r: Rectangular coordinates of the point.
    :param lonc: Angle (radians) of point from XZ plane.
    :param z: Height of point above XY plane.
    :return:
            Distance of point from origin,
            Polar angle (co-latitude in radians) of point,
            Azimuthal angle (longitude) of point (radians).
    """
    cdef double radius = 0.0
    cdef double colat  = 0.0
    cdef double slon   = 0.0
    cylsph_c(
        r, 
        clon,
        z,
        &radius, 
        &colat, 
        &slon, 
    )
    return radius, colat, slon


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=2, mode='c'] cylsph_v(
    const double[::1] r, 
    const double[::1] clon, 
    const double[::1] z
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.cylsph`

    Convert from cylindrical to spherical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/cylsph_c.html

    :param r: Rectangular coordinates of the point.
    :param lonc: Angle (radians) of point from XZ plane.
    :param z: Height of point above XY plane.
    :return:
            Distance of point from origin,
            Polar angle (co-latitude in radians) of point,
            Azimuthal angle (longitude) of point (radians).
    """
    cdef const np.double_t[::1] c_r = np.ascontiguousarray(r, dtype=np.double)
    cdef Py_ssize_t i, n = c_r.shape[0]
    cdef const np.double_t[::1] c_clon = np.ascontiguousarray(clon, dtype=np.double)
    cdef const np.double_t[::1] c_z = np.ascontiguousarray(z, dtype=np.double)
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_sph = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_sph = p_sph
    # TODO fix strides lookups below
    with nogil:
        for i in range(n):
            cylsph_c(
                c_r[i], 
                c_clon[i], 
                c_z[i], 
                <SpiceDouble *> &c_sph[i,0], 
                <SpiceDouble *> &c_sph[i,1],
                <SpiceDouble *> &c_sph[i,2]
            )
    return p_sph


def cylsph(
    r: float | double[::1], 
    clon: float | double[::1], 
    z: float | double[::1]
    ) -> tuple[float, float, float] | Cylindrical_N:
    """
    Convert from cylindrical to spherical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/cylsph_c.html

    :param r: Rectangular coordinates of the point.
    :param lonc: Angle (radians) of point from XZ plane.
    :param z: Height of point above XY plane.
    :return:
            Distance of point from origin,
            Polar angle (co-latitude in radians) of point,
            Azimuthal angle (longitude) of point (radians).
    """
    if PyFloat_Check(r):
        return cylsph_s(r, clon, z)
    else:
        return cylsph_v(r, clon, z)


# D


def deltet_s(
    double epoch,
    str eptype
    )-> float:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.deltet`

    Return the value of Delta ET (ET-UTC) for an input epoch.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/deltet_c.html

    :param epoch: Input epoch (seconds past J2000).
    :param eptype: Type of input epoch ("UTC" or "ET").
    :return: Delta ET (ET-UTC) at input epoch.
    """
    cdef double c_epoch = epoch
    cdef double c_delta = 0.0
    cdef const char* c_eptype = eptype
    deltet_c(
        c_epoch,
        c_eptype,
        &c_delta
    )
    check_for_spice_error()
    return c_delta


# new rule: always use type name style if accepting arrays as input
@boundscheck(False)
@wraparound(False)
def deltet_v(
    double[::1] epochs,
    str eptype
    ) -> Double_N:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.deltet`

    Return the values of Delta ET (ET-UTC) for all input epochs.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/deltet_c.html

    :param epochs: Input epoch (seconds past J2000).
    :param eptype: Type of input epoch ("UTC" or "ET").
    :return: Delta ET (ET-UTC) at input epoch.
    """
    cdef const np.double_t[::1] c_epochs = np.ascontiguousarray(epochs, dtype=np.double)
    cdef Py_ssize_t i, n = c_epochs.shape[0]
    cdef const char* c_eptype = eptype
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_deltas = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_deltas = p_deltas
    # perform the loop
    with nogil:
        for i in range(n):
            deltet_c(
                c_epochs[i],
                c_eptype,
                &c_deltas[i]
            )
    check_for_spice_error()

    return p_deltas


def deltet(
    epoch: float | float[::1],
    eptype: str
    )-> float | Double_N:
    """
    Return the value of Delta ET (ET-UTC) for an input epoch.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/deltet_c.html

    :param epoch: Input epoch (seconds past J2000).
    :param eptype: Type of input epoch ("UTC" or "ET").
    :return: Delta ET (ET-UTC) at input epoch.
    """
    if PyFloat_Check(epoch):
        return deltet_s(epoch, eptype)
    else:
        return deltet_v(epoch, eptype)


def dpr() -> float:
    """
    Return the number of degrees per radian.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/dpr_c.html

    :return: The number of degrees per radian.
    """
    return dpr_c()


# E


def et2lst_s(
    double et,
    int body,
    double lon,
    str typein
    ) -> tuple[int, int, int, str, str]:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.et2lst`

    Given an ephemeris epoch, compute the local solar time for
    an object on the surface of a body at a specified longitude.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/et2lst_c.html

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
    cdef double c_et = et
    cdef int c_body = body
    cdef double c_lon = lon
    cdef int c_hr = 0
    cdef int c_mn = 0
    cdef int c_sc = 0
    cdef char[TIMELEN] time
    cdef char[TIMELEN] ampm
    cdef const char* c_typein = typein
    et2lst_c(
        c_et,
        c_body,
        c_lon,
        c_typein,
        TIMELEN,
        TIMELEN,
        &c_hr,
        &c_mn,
        &c_sc,
        time,
        ampm
    )
    check_for_spice_error()
    p_time = PyUnicode_DecodeUTF8(time, strlen(time), "strict")
    p_ampm = PyUnicode_DecodeUTF8(ampm, strlen(ampm), "strict")
    return c_hr, c_mn, c_sc, p_time, p_ampm


@boundscheck(False)
@wraparound(False)
def et2lst_v(
    double[::1] ets,
    int body,
    double lon,
    str typein
    ) -> tuple[Int_N, Int_N, Int_N, String_N, String_N]:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.et2lst`

    Given ephemeris epochs, compute the local solar time for
    an object on the surface of a body at a specified longitude.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/et2lst_c.html

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
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    cdef const char* c_typein = typein
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
    cdef np.uint8_t[:, ::1] c_times = p_times
    cdef np.uint8_t[:, ::1] c_ampms = p_ampms
    cdef char* _c_times = <char*> &c_times[0, 0]
    cdef char* _c_ampms = <char*> &c_ampms[0, 0]
    # main loop
    with nogil:
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
                _c_times + i*TIMELEN,
                _c_ampms + i*TIMELEN
            )
    check_for_spice_error()
    # return values
    py_times = p_times.view(p_np_s_dtype).reshape(n)
    py_times = np.char.rstrip(py_times).astype(p_np_u_dtype)
    py_ampms = p_ampms.view(p_np_s_dtype).reshape(n)
    py_ampms = np.char.rstrip(py_ampms).astype(p_np_u_dtype)
    return p_hrs, p_mns, p_scs, py_times, py_ampms


def et2lst(
    et: float | float[::1],
    body: int,
    lon: float,
    typein: str
    ) -> tuple[int, int, int, str, str] | tuple[Int_N, Int_N, Int_N, String_N, String_N]:
    """
    Given an ephemeris epoch, compute the local solar time for
    an object on the surface of a body at a specified longitude.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/et2lst_c.html

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
    if PyFloat_Check(et):
        return et2lst_s(et, body, lon, typein)
    else:
        return et2lst_v(et, body, lon, typein)


def et2utc_s(
    double et,
    str format_str,
    int prec
    ) -> str:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.et2utc`

    Convert an input time from ephemeris seconds past J2000
    to Calendar, Day-of-Year, or Julian Date format, UTC.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/et2utc_c.html

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
    check_for_spice_error()
    return PyUnicode_DecodeUTF8(c_buffer, strlen(c_buffer), "strict")


@boundscheck(False)
@wraparound(False)
def et2utc_v(
    double[::1] ets,
    str format_str,
    int prec
    ) -> String_N:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.et2utc`

    Convert an input time from ephemeris seconds past J2000
    to Calendar, Day-of-Year, or Julian Date format, UTC.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/et2utc_c.html

    :param ets: Input epochs, given in ephemeris seconds past J2000.
    :param format_str: Format of output epoch.
    :param prec: Digits of precision in fractional seconds or days.
    :param lenout: The length of the output string plus 1.
    :return: Output time string in UTC
    """
    cdef int c_prec = prec
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert the strings to pointers once
    cdef const char* c_format_str = format_str
    # initialize output arrays
    p_np_s_dtype = np.dtype(('S', TIMELEN))
    p_np_u_dtype = np.dtype(('U', TIMELEN))
    cdef np.ndarray[np.uint8_t, ndim=2, mode='c'] p_utcstr = np.zeros((n, TIMELEN), dtype=np.uint8, order='C')
    cdef np.uint8_t[:, ::1] c_utcstr = p_utcstr
    cdef char* base = <char*> &c_utcstr[0, 0]
    # main loop
    with nogil:
        for i in range(n):
            et2utc_c(
                c_ets[i],
                c_format_str,
                c_prec,
                TIMELEN,
                base + i*TIMELEN,
            )
    check_for_spice_error()
    # return values
    py_utcstr = p_utcstr.view(p_np_s_dtype).reshape(n)
    py_utcstr = np.char.rstrip(py_utcstr).astype(p_np_u_dtype)
    return py_utcstr


def et2utc(
    et: float | float[::1],
    format_str: str,
    prec: int
    ) -> str | String_N:
    """
    Convert an input time from ephemeris seconds past J2000
    to Calendar, Day-of-Year, or Julian Date format, UTC.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/et2utc_c.html

    :param et: Input epoch, given in ephemeris seconds past J2000.
    :param format_str: Format of output epoch.
    :param prec: Digits of precision in fractional seconds or days.
    :param lenout: The length of the output string plus 1.
    :return: Output time string in UTC
    """
    if PyFloat_Check(et):
        return et2utc_s(et, format_str, prec)
    else:
        return et2utc_v(et, format_str, prec)


def etcal_s(
    double et
    ) -> str:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.etcal`

    Convert from an ephemeris epoch measured in seconds past
    the epoch of J2000 to a calendar string format using a
    formal calendar free of leapseconds.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/etcal_c.html

    :param et: Ephemeris time measured in seconds past J2000 TDB.
    :return: A standard calendar representation of et.
    """
    cdef double c_et = et
    cdef char[TIMELEN] c_buffer
    etcal_c(
        c_et,
        TIMELEN,
        &c_buffer[0]
    )
    check_for_spice_error()
    # Convert the C char* to a Python string
    p_cal = PyUnicode_DecodeUTF8(c_buffer, strlen(c_buffer), "strict")
    return p_cal


@boundscheck(False)
@wraparound(False)
def etcal_v(
    double[::1] ets
    ) -> String_N:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.etcal`

    Convert from an ephemeris epoch measured in seconds past
    the epoch of J2000 to a calendar string format using a
    formal calendar free of leapseconds.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/etcal_c.html

    :param ets: Ephemeris times measured in seconds past J2000 TDB.
    :return: A standard calendar representation of et.
    """
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # Allocate a 2D buffer of shape (n, 24) with dtype np.uint8
    p_np_s_dtype = np.dtype(('S', 25))
    p_np_u_dtype = np.dtype(('U', 25))
    cdef np.ndarray[np.uint8_t, ndim=2, mode='c'] p_results = np.empty((n, 25), dtype=np.uint8, order='C')
    cdef np.uint8_t[:, ::1] c_results = p_results
    cdef char* base = <char*> &c_results[0, 0]
    with nogil:
        for i in range(n):
            etcal_c(
                c_ets[i],
                25,
                base + i*25
            )
    check_for_spice_error()
    # return values
    py_results = p_results.view(p_np_s_dtype).reshape(n)
    py_results = np.char.rstrip(py_results).astype(p_np_u_dtype)
    return py_results


def etcal(
    et: float | float[::1]
    ) -> str | String_N:
    """
    Convert from an ephemeris epoch measured in seconds past
    the epoch of J2000 to a calendar string format using a
    formal calendar free of leapseconds.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/etcal_c.html

    :param et: Ephemeris time measured in seconds past J2000 TDB.
    :return: A standard calendar representation of et.
    """
    if PyFloat_Check(et):
        return etcal_s(et)
    else:
        return etcal_v(et)


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=1, mode='c'] evsgp4_s(
    double et,
    double[::1] geophs,
    double[::1] elems
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.evsgp4`

    Evaluate NORAD two-line element data for earth orbiting
    spacecraft. This evaluator uses algorithms as described
    in Vallado 2006

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/evsgp4_c.html

    :param et: Epoch in seconds past ephemeris epoch J2000.
    :param geophs: Geophysical constants
    :param elems: Two-line element data
    :return: Evaluated state
    """
    cdef const np.double_t[::1] c_geophs = np.ascontiguousarray(geophs, dtype=np.double)
    cdef const np.double_t[::1] c_elems  = np.ascontiguousarray(elems, dtype=np.double)
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_state = np.empty(6, dtype=np.double, order='C')
    cdef np.double_t[::1] c_state = p_state
    # call 
    evsgp4_c(
        et,
        &c_geophs[0],
        &c_elems[0],
        &c_state[0]
    )
    # return state
    return p_state


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=2, mode='c'] evsgp4_v(
    double[::1] ets,
    double[::1] geophs,
    double[:,::1] elems
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.evsgp4`

    Evaluate NORAD two-line element data for earth orbiting
    spacecraft. This evaluator uses algorithms as described
    in Vallado 2006

    TODO does it make sense to assume 1 et per 1 geophs and 1 elems?

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/evsgp4_c.html

    :param ets: Epochs in seconds past ephemeris epoch J2000.
    :param geophs: Geophysical constants
    :param elems: Two-line element data
    :return: Evaluated state
    """
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    cdef const np.double_t[::1] c_geophs = np.ascontiguousarray(geophs, dtype=np.double)
    cdef const double* c_geophs_ptr = &c_geophs[0]
    cdef const np.double_t[:,::1] c_elems  = np.ascontiguousarray(elems, dtype=np.double)
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_states = np.empty((n,6), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_states = p_states
    # call 
    with nogil:
        for i in range(n):
            evsgp4_c(
                c_ets[i],
                c_geophs_ptr,
                &c_elems[i, 0],
                &c_states[i, 0]
            )
    # return states
    return p_states


def evsgp4(
    et: float | double[::1],
    geophs: double[::1],
    elems: double[::1] | double[:,::1],
    ):
    """
    Evaluate NORAD two-line element data for earth orbiting
    spacecraft. This evaluator uses algorithms as described
    in Vallado 2006

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/evsgp4_c.html

    :param et: Epoch in seconds past ephemeris epoch J2000.
    :param geophs: Geophysical constants
    :param elems: Two-line element data
    :return: Evaluated state
    """
    if PyFloat_Check(et):
        return evsgp4_s(et, geophs, elems)
    else:
        return evsgp4_v(et, geophs, elems)

# F


cpdef SpiceBoolean failed() noexcept:
    """
    True if an error condition has been signalled via sigerr_c.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/failed_c.html

    :return: a boolean
    """
    return failed_c()


@boundscheck(False)
@wraparound(False)
def fovray_s(
    str inst,
    double[::1] raydir,
    str rframe,
    str abcorr,
    str obsrvr,
    double et
) -> bool:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.fovray`

    Determine if a specified ray is within the field-of-view (FOV) of a
    specified instrument at a given time.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/fovray_c.html

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
    cdef SpiceBoolean c_visibl = SPICEFALSE
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
        <SpiceBoolean *> &c_visibl
    )
    check_for_spice_error()
    # return
    return PyBool_FromLong(c_visibl)


@boundscheck(False)
@wraparound(False)
def fovray_v(
    str inst,
    double[::1] raydir,
    str rframe,
    str abcorr,
    str obsrvr,
    double[::1] ets
) -> BoolArray:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.fovray`

    Determine if a specified ray is within the field-of-view (FOV) of a
    specified instrument at a given time.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/fovray_c.html

    :param inst: Name or ID code string of the instrument.
    :param raydir: Ray's direction vector.
    :param rframe: Body-fixed, body-centered frame for target body.
    :param abcorr: Aberration correction flag.
    :param observer: Name or ID code string of the observer.
    :param ets: Times of the observation (seconds past J2000).
    :return: Visibility flags
    """
    # initialize c variables
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert the strings to pointers once
    cdef const char* c_inst     = inst
    cdef const char* c_rframe   = rframe
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsrvr   = obsrvr
    # initialize output arrays
    cdef np.ndarray[np.int32_t, ndim=1, mode='c'] p_visibl = np.empty(n, dtype=np.int32, order='C')
    cdef np.int32_t[::1] c_visibl = p_visibl
    # perform the call
    with nogil:
        for i in range(n):
            fovray_c(
                c_inst,
                &raydir[0],
                c_rframe,
                c_abcorr,
                c_obsrvr,
                <SpiceDouble *> &c_ets[i],  # I got a warning converting const double * to SpiceDouble related to discard qualifiers without the cast here
                <SpiceBoolean *> &c_visibl[i]
            )
    check_for_spice_error()
    # return
    return p_visibl.astype(np.bool_)


def fovray(
    inst: str,
    raydir: float[::1],
    rframe: str,
    abcorr: str,
    obsrvr: str,
    et: float | float[::1]
) -> bool | BoolArray:
    """
    Determine if a specified ray is within the field-of-view (FOV) of a
    specified instrument at a given time.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/fovray_c.html

    :param inst: Name or ID code string of the instrument.
    :param raydir: Ray's direction vector.
    :param rframe: Body-fixed, body-centered frame for target body.
    :param abcorr: Aberration correction flag.
    :param observer: Name or ID code string of the observer.
    :param et: Time of the observation (seconds past J2000).
    :return: Visibility flag
    """
    if PyFloat_Check(et):
        return fovray_s(inst, raydir, rframe, abcorr, obsrvr, et)
    else:
        return fovray_v(inst, raydir, rframe, abcorr, obsrvr, et)


def fovtrg_s(
    str inst,
    str target,
    str tshape,
    str tframe,
    str abcorr,
    str obsrvr,
    double et
    ) -> bool:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.fovtrg`

    Determine if a specified ephemeris object is within the field-of-view (FOV)
    of a specified instrument at a given time.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/fovtrg_c.html

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
    cdef SpiceBoolean c_visibl = SPICEFALSE
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
        <SpiceBoolean *> &c_visibl
    )
    check_for_spice_error()
    # return
    return PyBool_FromLong(c_visibl)


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
    ) -> BoolArray:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.fovtrg`

    Determine if a specified ephemeris object is within the field-of-view (FOV)
    of a specified instrument at a given time.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/fovtrg_c.html

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
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert the strings to pointers once
    cdef const char* c_inst     = inst
    cdef const char* c_target   = target
    cdef const char* c_tshape   = tshape
    cdef const char* c_tframe   = tframe
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsrvr   = obsrvr
    # initialize output arrays
    cdef np.ndarray[np.int32_t, ndim=1, mode='c'] p_visibl = np.empty(n, dtype=np.int32, order='C')
    cdef np.int32_t[::1] c_visibl = p_visibl
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
                <SpiceDouble *> &c_ets[i],  # I got a warning converting const double * to SpiceDouble related to discard qualifiers without the cast here
                <SpiceBoolean *> &c_visibl[i]
            )
    check_for_spice_error()
    # return
    return p_visibl.astype(np.bool_)


def fovtrg(
    inst:   str,
    target: str,
    tshape: str,
    tframe: str,
    abcorr: str,
    obsrvr: str,
    et: float | float[::1]
    ) -> bool | BoolArray:
    """
    Determine if a specified ephemeris object is within the field-of-view (FOV)
    of a specified instrument at a given time.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/fovtrg_c.html

    :param inst: Name or ID code string of the instrument.
    :param target: Name or ID code string of the target.
    :param tshape: Type of shape model used for the target.
    :param tframe: Body-fixed, body-centered frame for target body.
    :param abcorr: Aberration correction flag.
    :param observer: Name or ID code string of the observer.
    :param et: Time of the observation (seconds past J2000).
    :return: Visibility flag
    """
    if PyFloat_Check(et):
        return fovtrg_s(inst, target, tshape, tframe, abcorr, obsrvr, et)
    else:
        return fovtrg_v(inst, target, tshape, tframe, abcorr, obsrvr, et)


def furnsh(
    str file
    ) -> None:
    """
    Load one or more SPICE kernels into a program.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/furnsh_c.html

    :param path: one or more paths to kernels
    """
    cdef const char* c_file = file
    if c_file == NULL:
        raise UnicodeError("Failed to encode file path in furnsh")
    furnsh_c(c_file)
    check_for_spice_error()


# G
@boundscheck(False)
cpdef np.ndarray[np.double_t, ndim=1, mode='c'] georec_s(
    double lon,
    double lat,
    double alt,
    double re,
    double f,
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.georec`

    Convert geodetic coordinates to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/georec_c.html

    :param lon: Geodetic longitude of point (radians).
    :param lat: Geodetic latitude  of point (radians).
    :param alt: Altitude of point above the reference spheroid.
    :param re: Equatorial radius of the reference spheroid.
    :param f: Flattening coefficient.
    :return: Rectangular coordinates of point.
    """
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_rec = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_rec = p_rec
    georec_c(
        lon,
        lat,
        alt,
        re,
        f,
        &c_rec[0]
    )
    return p_rec


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=2, mode='c'] georec_v(
    const double[::1] lon,
    const double[::1] lat,
    const double[::1] alt,
    double re,
    double f,
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.georec`

    Convert geodetic coordinates to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/georec_c.html

    :param lon: Geodetic longitude of point (radians).
    :param lat: Geodetic latitude  of point (radians).
    :param alt: Altitude of point above the reference spheroid.
    :param re: Equatorial radius of the reference spheroid.
    :param f: Flattening coefficient.
    :return: Rectangular coordinates of point.
    """
    cdef const np.double_t[::1] c_lon = np.ascontiguousarray(lon, dtype=np.double)
    cdef Py_ssize_t i, n = lon.shape[0]
    cdef const np.double_t[::1] c_lat = np.ascontiguousarray(lat, dtype=np.double)
    cdef const np.double_t[::1] c_alt = np.ascontiguousarray(alt, dtype=np.double)
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_rec = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_rec = p_rec
    # TODO fix strides lookups below
    with nogil:
        for i in range(n):
            georec_c(
                c_lon[i],
                c_lat[i],
                c_alt[i],
                re,
                f,  
                &c_rec[i, 0]
            )
    return p_rec


def georec(
    lon: float | double[::1],
    lat: float | double[::1],
    alt: float | double[::1],
    re: float,
    f: float
    ) -> Vector | Geodetic_N:
    """
    Convert geodetic coordinates to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/georec_c.html

    :param lon: Geodetic longitude of point (radians).
    :param lat: Geodetic latitude  of point (radians).
    :param alt: Altitude of point above the reference spheroid.
    :param re: Equatorial radius of the reference spheroid.
    :param f: Flattening coefficient.
    :return: Rectangular coordinates of point.
    """
    if PyFloat_Check(lon):
        return georec_s(lon, lat, alt, re, f)
    else:
        return georec_v(lon, lat, alt, re, f)


cpdef tuple[float, np.ndarray] getelm_s(
    int frstyr,  
    np.ndarray lines
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.getelm`

    Given a the "lines" of a two-line element set, parse the
    lines and return the elements in units suitable for use
    in SPICE software.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/getelm_c.html

    :param frstyr: Year of earliest representable two-line elements.
    :param lines: A pair of "lines" containing two-line elements.
    :return:
            The epoch of the elements in seconds past J2000,
            The elements converted to SPICE units (see naif docs for units).
    """
    # allocate outputs
    cdef double c_epoch = 0.0
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_elems = np.empty(10, dtype=np.double, order='C')
    cdef np.double_t[::1] c_elems = p_elems
    # ge the char memory view
    cdef const char[:,::1] c_lines = make_char_array(lines, TLELEN)
    cdef const char* c_lines_ptr = &c_lines[0,0]
    # now call getelm
    getelm_c(
        frstyr,
        TLELEN,
        c_lines_ptr,
        &c_epoch,
        &c_elems[0]
    )
    check_for_spice_error()
    return c_epoch, p_elems


@boundscheck(False)
@wraparound(False)
cpdef tuple[np.ndarray, np.ndarray] getelm_v(
    int[::1] frstyr,  
    np.ndarray lines
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.getelm`

    Given a the "lines" of a two-line element set, parse the
    lines and return the elements in units suitable for use
    in SPICE software.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/getelm_c.html

    :param frstyr: Year of earliest representable two-line elements.
    :param lines: A array of pairs of "lines" containing two-line elements, shape is (2*n_pairs,70).
    :return:
            The epoch of the elements in seconds past J2000,
            The elements converted to SPICE units (see naif docs for units).
    """
    # allocate outputs
    cdef const np.uint32_t[::1] c_frstyr = np.ascontiguousarray(frstyr, dtype=np.uint32)
    cdef Py_ssize_t i, n = c_frstyr.shape[0]
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_epochs = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_epochs = p_epochs
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_elems = np.empty((n,10), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_elems = p_elems
    # get the char memory view
    cdef char[:,::1] c_lines 
    cdef char* c_lines_ptr 
    # now call getelm in loop
    for i in range(n):
        c_lines = make_char_array(lines[i], TLELEN)
        c_lines_ptr = &c_lines[0, 0]
        getelm_c(
            c_frstyr[i],
            TLELEN,
            c_lines_ptr,
            &c_epochs[i],
            &c_elems[i, 0]
        )
    check_for_spice_error()
    return p_epochs, p_elems


def getelm(
    frstyr: int | int[::1],  
    lines: np.ndarray,
    )-> tuple[np.ndarray, np.ndarray]:
    """

    Given a the "lines" of a two-line element set, parse the
    lines and return the elements in units suitable for use
    in SPICE software.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/getelm_c.html

    :param frstyr: Year of earliest representable two-line elements.
    :param lines: A array of pairs of "lines" containing two-line elements, shape is (2*n_pairs,70).
    :return:
            The epoch of the elements in seconds past J2000,
            The elements converted to SPICE units (see naif docs for units).
    """
    if PyLong_Check(frstyr):
        return getelm_s(frstyr, lines)
    else:
        return getelm_v(frstyr, lines)


cpdef str getmsg(
    str option,
    int msglen
    ):
    """
    Retrieve the current short error message,
    the explanation of the short error message, or the
    long error message.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/getmsg_c.html

    :param option: Indicates type of error message.
    :param lenout: Available space in the output string msg.
    :return: The error message to be retrieved.
    """
    cdef Py_ssize_t length = _default_len_out
    cdef const char* c_option = option
    cdef int c_msglen = msglen
    if c_msglen <= 0:
        raise ValueError("msglen must be positive")
    cdef char* c_msgstr = <char*> malloc((msglen) * sizeof(char))
    if c_msgstr == NULL:
        raise MemoryError("Unable to allocate memory for traceback string in getmsg.")
    try:
        getmsg_c(
            c_option,
            c_msglen,
            c_msgstr
        )
        length = strlen(c_msgstr)
        p_msgstr = PyUnicode_DecodeUTF8(c_msgstr, length, "replace")
        return p_msgstr
    finally:
        free(c_msgstr)

# H

def halfpi() -> float:
    """
    Return half the value of pi (the ratio of the circumference of
    a circle to its diameter).

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/halfpi_c.html

    :return: Half the value of pi.
    """
    return halfpi_c()

# I

@boundscheck(False)
@wraparound(False)
cpdef tuple[float, np.ndarray, float, float, float, bool, bool] illumf_s(
    const char * method,
    const char * target,
    const char * ilusrc,
    double et,
    const char * fixref,
    const char * abcorr,
    const char * obsrvr,
    double[::1] spoint,
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.illumf`

    Compute the illumination angles---phase, incidence, and
    emission---at a specified point on a target body. Return logical
    flags indicating whether the surface point is visible from
    the observer's position and whether the surface point is
    illuminated.

    The target body's surface is represented using topographic data
    provided by DSK files, or by a reference ellipsoid.

    The illumination source is a specified ephemeris object.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/illumf_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param ilusrc: Name of illumination source.
    :param et: Epoch in ephemeris seconds past J2000.
    :param fixref: Body-fixed, body-centered target body frame.
    :param abcorr: Desired aberration correction.
    :param obsrvr: Name of observing body.
    :param spoint: Body-fixed coordinates of a target surface point.
    :return: 
        Target surface point epoch in seconds past J2000 TDB, 
        Vector from observer to target surface point in km,
        Phase angle at the surface point in radians, 
        Source incidence angle at the surface point in radians,
        Emission angle at the surface point in radians,
        Visibility flag, 
        Illumination flag
    """
    cdef const np.double_t[::1] c_spoint = np.ascontiguousarray(spoint, dtype=np.double)
    #allocate outputs
    cdef SpiceBoolean c_visibl = SPICEFALSE
    cdef SpiceBoolean c_lit = SPICEFALSE
    cdef double trgepc = 0.0
    cdef double phase  = 0.0
    cdef double incdnc = 0.0
    cdef double emissn = 0.0
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_srfvec = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_srfvec = p_srfvec
    # make the call
    illumf_c(
        method, 
        target,
        ilusrc,
        et,
        fixref,
        abcorr,
        obsrvr,
        &c_spoint[0],
        &trgepc,
        &c_srfvec[0],
        &phase,
        &incdnc,
        &emissn,
        <SpiceBoolean *> &c_visibl,
        <SpiceBoolean *> &c_lit
    )
    check_for_spice_error()
    return trgepc, p_srfvec, phase, incdnc, emissn, PyBool_FromLong(c_visibl), PyBool_FromLong(c_lit) 


@boundscheck(False)
@wraparound(False)
cpdef tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray] illumf_v(
    const char* method,
    const char* target,
    const char* ilusrc,
    double[::1] ets,
    const char* fixref,
    const char* abcorr,
    const char* obsrvr,
    double[:,::1] spoints,
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.illumf`

    Compute the illumination angles---phase, incidence, and
    emission---at a specified point on a target body. Return logical
    flags indicating whether the surface point is visible from
    the observer's position and whether the surface point is
    illuminated.

    The target body's surface is represented using topographic data
    provided by DSK files, or by a reference ellipsoid.

    The illumination source is a specified ephemeris object.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/illumf_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param ilusrc: Name of illumination source.
    :param ets: Epochs in ephemeris seconds past J2000.
    :param fixref: Body-fixed, body-centered target body frame.
    :param abcorr: Desired aberration correction.
    :param obsrvr: Name of observing body.
    :param spoints: Body-fixed coordinates of target surface points.
    :return: 
        Target surface point epoch in seconds past J2000 TDB, 
        Vector from observer to target surface point in km,
        Phase angle at the surface point in radians, 
        Source incidence angle at the surface point in radians,
        Emission angle at the surface point in radians,
        Visibility flag, 
        Illumination flag
    """
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef const np.double_t[:,::1] c_spoints = np.ascontiguousarray(spoints, dtype=np.double)
    cdef Py_ssize_t i, j, n, m = 0
    n = c_ets.shape[0]
    m = c_spoints.shape[0]
    cdef double c_et_r = 0.0
    #allocate outputs
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_trgepc = np.empty((n,m), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_trgepc = p_trgepc
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_phase  = np.empty((n,m), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_phase = p_phase
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_incdnc = np.empty((n,m), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_incdnc = p_incdnc
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_emissn = np.empty((n,m), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_emissn = p_emissn
    cdef np.ndarray[np.int32_t, ndim=2, mode='c'] p_visibl = np.empty((n,m), dtype=np.int32, order='C')
    cdef np.int32_t[:,::1] c_visibl = p_visibl
    cdef np.ndarray[np.int32_t, ndim=2, mode='c'] p_lit    = np.empty((n,m), dtype=np.int32, order='C')
    cdef np.int32_t[:,::1] c_lit = p_lit
    cdef np.ndarray[np.double_t, ndim=3, mode='c'] p_srfvec = np.empty((n,m,3), dtype=np.double, order='C')
    cdef np.double_t[:,:,::1] c_srfvec = p_srfvec
    # make the call
    with nogil:
        for i in range(n):
            c_et_r = c_ets[i]
            for j in range(m):
                illumf_c(
                    method, 
                    target,
                    ilusrc,
                    c_et_r,
                    fixref,
                    abcorr,
                    obsrvr,
                    &c_spoints[j,0],
                    &c_trgepc[i,j],
                    &c_srfvec[i,j,0],
                    &c_phase[i,j],
                    &c_incdnc[i,j],
                    &c_emissn[i,j],
                    <SpiceBoolean *> &c_visibl[i,j],
                    <SpiceBoolean *> &c_lit[i,j]
                )
    check_for_spice_error()
    return p_trgepc, p_srfvec, p_phase, p_incdnc, p_emissn, p_visibl.astype(np.bool_), p_lit.astype(np.bool_) 


def illumf(
    method: str,
    target: str,
    ilusrc: str,
    et: float | double[::1],
    fixref: str,
    abcorr: str,
    obsrvr: str,
    spoint: double[::1] | double[:,::1],
    ) -> tuple[float, np.ndarray, float, float, float, bool, bool] | tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute the illumination angles---phase, incidence, and
    emission---at a specified point on a target body. Return logical
    flags indicating whether the surface point is visible from
    the observer's position and whether the surface point is
    illuminated.

    The target body's surface is represented using topographic data
    provided by DSK files, or by a reference ellipsoid.

    The illumination source is a specified ephemeris object.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/illumf_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param ilusrc: Name of illumination source.
    :param et: Epoch in ephemeris seconds past J2000.
    :param fixref: Body-fixed, body-centered target body frame.
    :param abcorr: Desired aberration correction.
    :param obsrvr: Name of observing body.
    :param spoint: Body-fixed coordinates of a target surface point.
    :return: 
        Target surface point epoch in seconds past J2000 TDB, 
        Vector from observer to target surface point in km,
        Phase angle at the surface point in radians, 
        Source incidence angle at the surface point in radians,
        Emission angle at the surface point in radians,
        Visibility flag, 
        Illumination flag
    """
    if PyFloat_Check(et):
        return illumf_s(method, target, ilusrc, et, fixref, abcorr, obsrvr, spoint)
    else:
        return illumf_v(method, target, ilusrc, et, fixref, abcorr, obsrvr, spoint)



@boundscheck(False)
@wraparound(False)
cpdef tuple[float, np.ndarray, float, float, float] illumg_s(
    const char* method,
    const char* target,
    const char* ilusrc,
    double et,
    const char* fixref,
    const char* abcorr,
    const char* obsrvr,
    double[::1] spoint,
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.illumg`

    Find the illumination angles (phase, incidence, and
    emission) at a specified surface point of a target body.

    The surface of the target body may be represented by a triaxial
    ellipsoid or by topographic data provided by DSK files.

    The illumination source is a specified ephemeris object.
    param method: Computation method.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/illumg_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param ilusrc: Name of illumination source.
    :param et: Epoch in ephemeris seconds past J2000.
    :param fixref: Body-fixed, body-centered target body frame.
    :param abcorr: Desired aberration correction.
    :param obsrvr: Name of observing body.
    :param spoint: Body-fixed coordinates of a target surface point.
    :return: 
        Target surface point epoch in seconds past J2000 TDB, 
        Vector from observer to target surface point in km,
        Phase angle at the surface point in radians, 
        Source incidence angle at the surface point in radians, 
        Emission angle at the surface point in radians,
    """
    cdef const np.double_t[::1] c_spoint = np.ascontiguousarray(spoint, dtype=np.double)
    #allocate outputs
    cdef double trgepc = 0.0
    cdef double phase  = 0.0
    cdef double incdnc = 0.0
    cdef double emissn = 0.0
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_srfvec = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_srfvec = p_srfvec
    # make the call
    illumg_c(
        method, 
        target,
        ilusrc,
        et,
        fixref,
        abcorr,
        obsrvr,
        &c_spoint[0],
        &trgepc,
        &c_srfvec[0],
        &phase,
        &incdnc,
        &emissn
    )
    check_for_spice_error()
    return trgepc, p_srfvec, phase, incdnc, emissn 


@boundscheck(False)
@wraparound(False)
cpdef tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray] illumg_v(
    const char* method,
    const char* target,
    const char* ilusrc,
    double[::1] ets,
    const char* fixref,
    const char* abcorr,
    const char* obsrvr,
    double[:,::1] spoint,
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.illumg`

    Find the illumination angles (phase, incidence, and
    emission) at a specified surface point of a target body.

    The surface of the target body may be represented by a triaxial
    ellipsoid or by topographic data provided by DSK files.

    The illumination source is a specified ephemeris object.
    param method: Computation method.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/illumg_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param ilusrc: Name of illumination source.
    :param ets: Epochs in ephemeris seconds past J2000.
    :param fixref: Body-fixed, body-centered target body frame.
    :param abcorr: Desired aberration correction.
    :param obsrvr: Name of observing body.
    :param spoint: Body-fixed coordinates of a target surface point.
    :return: 
        Target surface point epoch in seconds past J2000 TDB, 
        Vector from observer to target surface point in km,
        Phase angle at the surface point in radians, 
        Source incidence angle at the surface point in radians, 
        Emission angle at the surface point in radians,
    """
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef const np.double_t[:,::1] c_spoint = np.ascontiguousarray(spoint, dtype=np.double)
    cdef Py_ssize_t i, j, n, m = 0
    n = c_ets.shape[0]
    m = c_spoint.shape[0]
    cdef double c_et_r = 0.0
    #allocate outputs
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_trgepc = np.empty((n,m), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_trgepc = p_trgepc
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_phase  = np.empty((n,m), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_phase = p_phase
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_incdnc = np.empty((n,m), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_incdnc = p_incdnc
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_emissn = np.empty((n,m), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_emissn = p_emissn
    cdef np.ndarray[np.double_t, ndim=3, mode='c'] p_srfvec = np.empty((n,m,3), dtype=np.double, order='C')
    cdef np.double_t[:,:,::1] c_srfvec = p_srfvec
    # make the call
    with nogil:
        for i in range(n):
            c_et_r = c_ets[i]
            for j in range(m):
                illumg_c(
                    method, 
                    target,
                    ilusrc,
                    c_et_r,
                    fixref,
                    abcorr,
                    obsrvr,
                    &c_spoint[j,0],
                    &c_trgepc[i,j],
                    &c_srfvec[i,j,0],
                    &c_phase[i,j],
                    &c_incdnc[i,j],
                    &c_emissn[i,j]
                )
    check_for_spice_error()
    return p_trgepc, p_srfvec, p_phase, p_incdnc, p_emissn 


def illumg(
    method: str,
    target: str,
    ilusrc: str,
    et: float | double[::1],
    fixref: str,
    abcorr: str,
    obsrvr: str,
    spoint: double[::1] | double[:,::1],
    ) -> tuple[float, np.ndarray, float, float, float] | tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Find the illumination angles (phase, incidence, and
    emission) at a specified surface point of a target body.

    The surface of the target body may be represented by a triaxial
    ellipsoid or by topographic data provided by DSK files.

    The illumination source is a specified ephemeris object.
    param method: Computation method.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/illumg_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param ilusrc: Name of illumination source.
    :param et: Epoch in ephemeris seconds past J2000.
    :param fixref: Body-fixed, body-centered target body frame.
    :param abcorr: Desired aberration correction.
    :param obsrvr: Name of observing body.
    :param spoint: Body-fixed coordinates of a target surface point.
    :return: 
        Target surface point epoch in seconds past J2000 TDB, 
        Vector from observer to target surface point in km,
        Phase angle at the surface point in radians, 
        Source incidence angle at the surface point in radians, 
        Emission angle at the surface point in radians,
    """
    if PyFloat_Check(et):
        return illumg_s(method, target, ilusrc, et, fixref, abcorr, obsrvr, spoint)
    else:
        return illumg_v(method, target, ilusrc, et, fixref, abcorr, obsrvr, spoint)


@boundscheck(False)
@wraparound(False)
cpdef tuple[float, np.ndarray, float, float, float] ilumin_s(
    const char* method,
    const char* target,
    double et,
    const char* fixref,
    const char* abcorr,
    const char* obsrvr,
    double[::1] spoint,
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.ilumin`

    Find the illumination angles (phase, solar incidence, and
    emission) at a specified surface point of a target body.

    This routine supersedes illum.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/ilumin_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param et: Epoch in ephemeris seconds past J2000.
    :param fixref: Body-fixed, body-centered target body frame.
    :param abcorr: Desired aberration correction.
    :param obsrvr: Name of observing body.
    :param spoint: Body-fixed coordinates of a target surface point.
    :return: Target surface point epoch, Vector from observer to target
     surface point, Phase angle, Solar incidence angle, and Emission
     angle at the surface point.
    """
    cdef const np.double_t[::1] c_spoint = np.ascontiguousarray(spoint, dtype=np.double)
    #allocate outputs
    cdef double trgepc = 0.0
    cdef double phase  = 0.0
    cdef double incdnc = 0.0
    cdef double emissn = 0.0
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_srfvec = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_srfvec = p_srfvec
    # make the call
    ilumin_c(
        method, 
        target,
        et,
        fixref,
        abcorr,
        obsrvr,
        &c_spoint[0],
        &trgepc,
        &c_srfvec[0],
        &phase,
        &incdnc,
        &emissn
    )
    check_for_spice_error()
    return trgepc, p_srfvec, phase, incdnc, emissn 


@boundscheck(False)
@wraparound(False)
cpdef tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray] ilumin_v(
    const char* method,
    const char* target,
    double[::1] ets,
    const char* fixref,
    const char* abcorr,
    const char* obsrvr,
    double[:,::1] spoint,
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.ilumin`

    Find the illumination angles (phase, solar incidence, and
    emission) at a specified surface point of a target body.

    This routine supersedes illum.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/ilumin_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param ets: Epochs in ephemeris seconds past J2000.
    :param fixref: Body-fixed, body-centered target body frame.
    :param abcorr: Desired aberration correction.
    :param obsrvr: Name of observing body.
    :param spoint: Body-fixed coordinates of a target surface point.
    :return: Target surface point epoch, Vector from observer to target
     surface point, Phase angle, Solar incidence angle, and Emission
     angle at the surface point.
    """
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef const np.double_t[:,::1] c_spoint = np.ascontiguousarray(spoint, dtype=np.double)
    cdef Py_ssize_t i, j, n, m = 0
    n = c_ets.shape[0]
    m = c_spoint.shape[0]
    cdef double c_et_r = 0.0
    #allocate outputs
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_trgepc = np.empty((n,m), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_trgepc = p_trgepc
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_phase  = np.empty((n,m), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_phase = p_phase
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_incdnc = np.empty((n,m), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_incdnc = p_incdnc
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_emissn = np.empty((n,m), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_emissn = p_emissn
    cdef np.ndarray[np.double_t, ndim=3, mode='c'] p_srfvec = np.empty((n,m,3), dtype=np.double, order='C')
    cdef np.double_t[:,:,::1] c_srfvec = p_srfvec
    # make the call
    with nogil:
        for i in range(n):
            c_et_r = c_ets[i]
            for j in range(m):
                ilumin_c(
                    method, 
                    target,
                    c_et_r,
                    fixref,
                    abcorr,
                    obsrvr,
                    &c_spoint[j,0],
                    &c_trgepc[i,j],
                    &c_srfvec[i,j,0],
                    &c_phase[i,j],
                    &c_incdnc[i,j],
                    &c_emissn[i,j]
                )
    check_for_spice_error()
    return p_trgepc, p_srfvec, p_phase, p_incdnc, p_emissn 


def ilumin(
    method: str,
    target: str,
    et: float | double[::1],
    fixref: str,
    abcorr: str,
    obsrvr: str,
    spoint: double[::1] | double[:,::1],
    ) -> tuple[float, np.ndarray, float, float, float] | tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Find the illumination angles (phase, solar incidence, and
    emission) at a specified surface point of a target body.

    This routine supersedes illum.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/ilumin_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param et: Epoch in ephemeris seconds past J2000.
    :param fixref: Body-fixed, body-centered target body frame.
    :param abcorr: Desired aberration correction.
    :param obsrvr: Name of observing body.
    :param spoint: Body-fixed coordinates of a target surface point.
    :return: Target surface point epoch, Vector from observer to target
     surface point, Phase angle, Solar incidence angle, and Emission
     angle 
    """
    if PyFloat_Check(et):
        return ilumin_s(method, target, et, fixref, abcorr, obsrvr, spoint)
    else:
        return ilumin_v(method, target, et, fixref, abcorr, obsrvr, spoint)

# J


def j1900() -> float:
    """
    Return the Julian Date of 1899 DEC 31 12:00:00 (1900 JAN 0.5).

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/j1900_c.html

    :return: Julian Date of 1899 DEC 31 12:00:00
    """
    return j1900_c()



def j1950() -> float:
    """
    Return the Julian Date of 1950 JAN 01 00:00:00 (1950 JAN 1.0).

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/j1950_c.html

    :return: Julian Date of 1950 JAN 01 00:00:00
    """
    return j1950_c()



def j2000() -> float:
    """
    Return the Julian Date of 2000 JAN 01 12:00:00 (2000 JAN 1.5).
    
    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/j2000_c.html

    :return: Julian Date of 2000 JAN 01 12:00:00
    """
    return j2000_c()



def j2100() -> float:
    """
    Return the Julian Date of 2100 JAN 01 12:00:00 (2100 JAN 1.5).

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/j2100_c.html

    :return: Julian Date of 2100 JAN 01 12:00:00
    """
    return j2100_c()


def jyear() -> float:
    """
    Return the number of seconds in a julian year.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/jyear_c.html

    :return: number of seconds in a julian year
    """
    return jyear_c()

# K

# L

cpdef tuple[float, float, float] latcyl_s(
    radius: float, 
    lon: float, 
    lat: float
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.latcyl`

    Convert from latitudinal coordinates to cylindrical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/latcyl_c.html

    :param radius: Distance of a point from the origin.
    :param lon: Angle of the point from the XZ plane in radians.
    :param lat: Angle of the point from the XY plane in radians.
    :return: (r, lonc, z)
    """
    cdef double r    = 0.0
    cdef double lonc = 0.0
    cdef double z    = 0.0
    latcyl_c(
        radius, 
        lon, 
        lat, 
        &r, 
        &lonc,
        &z
    )
    return r, lonc, z


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=2, mode='c'] latcyl_v(
    const double[::1] radius, 
    const double[::1] lon, 
    const double[::1] lat
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.latcyl`

    Convert from latitudinal coordinates to cylindrical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/latcyl_c.html

    :param radius: Distance of a point from the origin.
    :param lon: Angle of the point from the XZ plane in radians.
    :param lat: Angle of the point from the XY plane in radians.
    :return: (r, lonc, z)
    """
    cdef const np.double_t[::1] c_radius = np.ascontiguousarray(radius, dtype=np.double)
    cdef Py_ssize_t i, n = c_radius.shape[0]
    cdef const np.double_t[::1] c_lon = np.ascontiguousarray(lon, dtype=np.double)
    cdef const np.double_t[::1] c_lat = np.ascontiguousarray(lat, dtype=np.double)
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_cyl = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_cyl = p_cyl
    # TODO fix strides lookups below
    with nogil:
        for i in range(n):
            latcyl_c(
                c_radius[i], 
                c_lon[i], 
                c_lat[i], 
                <SpiceDouble *> &c_cyl[i,0], 
                <SpiceDouble *> &c_cyl[i,1],
                <SpiceDouble *> &c_cyl[i,2]
            )
    return p_cyl


def latcyl(
    radius: float | double[::1], 
    lon: float | double[::1], 
    lat: float | double[::1]
    ) -> tuple[float, float, float] | Cylindrical_N:
    """
    Convert from latitudinal coordinates to cylindrical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/latcyl_c.html

    :param radius: Distance of a point from the origin.
    :param lon: Angle of the point from the XZ plane in radians.
    :param lat: Angle of the point from the XY plane in radians.
    :return: (r, lonc, z)
    """
    if PyFloat_Check(radius):
        return latcyl_s(radius, lon, lat)
    else:
        return latcyl_v(radius, lon, lat)


cpdef np.ndarray[np.double_t, ndim=1, mode='c'] latrec_s(
    radius: float, 
    lon: float, 
    lat: float
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.latrec`

    Convert from latitudinal coordinates to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/latrec_c.html

    :param radius: Distance of a point from the origin.
    :param longitude: Longitude of point in radians.
    :param latitude: Latitude of point in radians.
    :return: Rectangular coordinates of the point.
    """
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_rec = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_rec = p_rec
    latrec_c(
        radius, 
        lon, 
        lat, 
        &c_rec[0],
    )
    return p_rec


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=2, mode='c'] latrec_v(
    const double[::1] radius, 
    const double[::1] lon, 
    const double[::1] lat
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.latrec`

    Convert from latitudinal coordinates to cylindrical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/latrec_c.html

    :param radius: Distance of a point from the origin.
    :param lon: Angle of the point from the XZ plane in radians.
    :param lat: Angle of the point from the XY plane in radians.
    :return: (r, lonc, z)
    """
    cdef const np.double_t[::1] c_radius = np.ascontiguousarray(radius, dtype=np.double)
    cdef Py_ssize_t i, n = c_radius.shape[0]
    cdef const np.double_t[::1] c_lon = np.ascontiguousarray(lon, dtype=np.double)
    cdef const np.double_t[::1] c_lat = np.ascontiguousarray(lat, dtype=np.double)
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_rec = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_rec = p_rec
    # TODO fix strides lookups below
    with nogil:
        for i in range(n):
            latrec_c(
                c_radius[i], 
                c_lon[i], 
                c_lat[i], 
                &c_rec[i, 0]
            )
    return p_rec


def latrec(
    radius: float | double[::1], 
    lon: float | double[::1], 
    lat: float | double[::1]
    ) -> Vector | Vector_N:
    """
    Convert from latitudinal coordinates to cylindrical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/latrec_c.html

    :param radius: Distance of a point from the origin.
    :param lon: Angle of the point from the XZ plane in radians.
    :param lat: Angle of the point from the XY plane in radians.
    :return: (r, lonc, z)
    """
    if PyFloat_Check(radius):
        return latrec_s(radius, lon, lat)
    else:
        return latrec_v(radius, lon, lat)


cpdef tuple[float, float, float] latsph_s(
    radius: float, 
    lon: float, 
    lat: float
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.latsph`

    Convert from latitudinal coordinates to spherical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/latsph_c.html

    :param radius: Distance of a point from the origin.
    :param lon: Angle of the point from the XZ plane in radians.
    :param lat: Angle of the point from the XY plane in radians.
    :return: (rho colat, lons)
    """
    cdef double rho    = 0.0
    cdef double colat  = 0.0
    cdef double lons   = 0.0
    latsph_c(
        radius, 
        lon, 
        lat, 
        &rho, 
        &colat,
        &lons
    )
    return rho, colat, lons


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=2, mode='c'] latsph_v(
    const double[::1] radius, 
    const double[::1] lon, 
    const double[::1] lat
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.latsph`

    Convert from latitudinal coordinates to spherical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/latsph_c.html

    :param radius: Distance of a point from the origin.
    :param lon: Angle of the point from the XZ plane in radians.
    :param lat: Angle of the point from the XY plane in radians.
    :return: (rho colat, lons)
    """
    cdef const np.double_t[::1] c_radius = np.ascontiguousarray(radius, dtype=np.double)
    cdef Py_ssize_t i, n = c_radius.shape[0]
    cdef const np.double_t[::1] c_lon = np.ascontiguousarray(lon, dtype=np.double)
    cdef const np.double_t[::1] c_lat = np.ascontiguousarray(lat, dtype=np.double)
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_sph = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_sph = p_sph
    # TODO fix strides lookups below
    with nogil:
        for i in range(n):
            latsph_c(
                c_radius[i], 
                c_lon[i], 
                c_lat[i], 
                <SpiceDouble *> &c_sph[i,0], 
                <SpiceDouble *> &c_sph[i,1],
                <SpiceDouble *> &c_sph[i,2]
            )
    return p_sph


def latsph(
    radius: float | double[::1], 
    lon: float | double[::1], 
    lat: float | double[::1]
    ) -> tuple[float, float, float] | Cylindrical_N:
    """
    Convert from latitudinal coordinates to spherical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/latsph_c.html

    :param radius: Distance of a point from the origin.
    :param lon: Angle of the point from the XZ plane in radians.
    :param lat: Angle of the point from the XY plane in radians.
    :return: (rho colat, lons)
    """
    if PyFloat_Check(radius):
        return latsph_s(radius, lon, lat)
    else:
        return latsph_v(radius, lon, lat)


@boundscheck(False)
@wraparound(False)
cpdef tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray] limbpt_s(
    const char * method,
    const char * target,
    double et,
    const char * fixref,
    const char * abcorr,
    const char * corloc,
    const char * obsrvr,
    double[::1] refvec,
    double rolstp,
    int ncuts,
    double schstp,
    double soltol,
    int maxn
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.limbpt`

    Find limb points on a target body. The limb is the set of points
    of tangency on the target of rays emanating from the observer.
    The caller specifies half-planes bounded by the observer-target
    center vector in which to search for limb points.

    The surface of the target body may be represented either by a
    triaxial ellipsoid or by topographic data.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/limbpt_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param et: Epoch in ephemeris seconds past J2000 TDB.
    :param fixref: Body-fixed, body-centered target body frame.
    :param abcorr: Aberration correction.
    :param corloc: Aberration correction locus.
    :param obsrvr: Name of observing body.
    :param refvec: Reference vector for cutting half-planes.
    :param rolstp: Roll angular step for cutting half-planes.
    :param ncuts: Number of cutting half-planes.
    :param schstp: Angular step size for searching.
    :param soltol: Solution convergence tolerance.
    :param maxn: Maximum number of entries in output arrays.
    :return: 
        Counts of limb points corresponding to cuts
        Limb points in km, 
        Times associated with limb points in seconds, 
        Tangent vectors emanating from the observer in km
    """
    # process inputs
    cdef Py_ssize_t c_maxn = maxn
    cdef const np.double_t[::1] c_refvec = np.ascontiguousarray(refvec, dtype=np.double)
    # allocate outputs
    cdef np.ndarray[np.int32_t, ndim=1, mode='c'] p_npts = np.empty(c_maxn, dtype=np.int32, order='C')
    cdef int[::1] c_npts = p_npts
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_points = np.empty((c_maxn, 3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_points = p_points
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_epochs = np.empty(c_maxn, dtype=np.double, order='C')
    cdef np.double_t[::1] c_epochs = p_epochs
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_tangts = np.empty((c_maxn, 3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_tangts = p_tangts
    # call the c function
    with nogil:
        limbpt_c(
            method,
            target,
            et,
            fixref,
            abcorr,
            corloc,
            obsrvr,
            &c_refvec[0],
            rolstp,
            ncuts,
            schstp,
            soltol,
            maxn,
            &c_npts[0],
            <SpiceDouble (*)[3]> &c_points[0, 0],
            &c_epochs[0],
            <SpiceDouble (*)[3]> &c_tangts[0, 0]
        )
    check_for_spice_error()
    # return the results
    return p_npts, p_points, p_epochs, p_tangts


@boundscheck(False)
@wraparound(False)
cpdef tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray] limbpt_v(
    const char * method,
    const char * target,
    double[::1] ets,
    const char * fixref,
    const char * abcorr,
    const char * corloc,
    const char * obsrvr,
    double[::1] refvec,
    double rolstp,
    int ncuts,
    double schstp,
    double soltol,
    int maxn
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.limbpt`

    Find limb points on a target body. The limb is the set of points
    of tangency on the target of rays emanating from the observer.
    The caller specifies half-planes bounded by the observer-target
    center vector in which to search for limb points.

    The surface of the target body may be represented either by a
    triaxial ellipsoid or by topographic data.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/limbpt_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param ets: Epochs in ephemeris seconds past J2000 TDB.
    :param fixref: Body-fixed, body-centered target body frame.
    :param abcorr: Aberration correction.
    :param corloc: Aberration correction locus.
    :param obsrvr: Name of observing body.
    :param refvec: Reference vector for cutting half-planes.
    :param rolstp: Roll angular step for cutting half-planes.
    :param ncuts: Number of cutting half-planes.
    :param schstp: Angular step size for searching.
    :param soltol: Solution convergence tolerance.
    :param maxn: Maximum number of entries in output arrays.
    :return: 
        Counts of limb points corresponding to cuts
        Limb points in km, 
        Times associated with limb points in seconds, 
        Tangent vectors emanating from the observer in km
    """
    # process inputs
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    cdef Py_ssize_t c_maxn = maxn
    cdef const np.double_t[::1] c_refvec = np.ascontiguousarray(refvec, dtype=np.double)
    cdef const SpiceDouble* c_refvec_ptr = &c_refvec[0]
    # allocate outputs
    cdef np.ndarray[np.int32_t, ndim=2, mode='c'] p_npts = np.empty((n, c_maxn), dtype=np.int32, order='C')
    cdef int[:,::1] c_npts = p_npts
    cdef np.ndarray[np.double_t, ndim=3, mode='c'] p_points = np.empty((n, c_maxn, 3), dtype=np.double, order='C')
    cdef np.double_t[:,:,::1] c_points = p_points
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_epochs = np.empty((n, c_maxn), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_epochs = p_epochs
    cdef np.ndarray[np.double_t, ndim=3, mode='c'] p_tangts = np.empty((n, c_maxn, 3), dtype=np.double, order='C')
    cdef np.double_t[:,:,::1] c_tangts = p_tangts
    # call the c function
    with nogil:
        for i in range(n):
            limbpt_c(
                method,
                target,
                c_ets[i],
                fixref,
                abcorr,
                corloc,
                obsrvr,
                c_refvec_ptr,
                rolstp,
                ncuts,
                schstp,
                soltol,
                maxn,
                &c_npts[i, 0],
                <SpiceDouble (*)[3]> &c_points[i, 0, 0],
                &c_epochs[i, 0],
                <SpiceDouble (*)[3]> &c_tangts[i, 0, 0]
            )
    check_for_spice_error()
    # return the results
    return p_npts, p_points, p_epochs, p_tangts


def limbpt(
    method: str,
    target: str,
    et: float | double[::1],
    fixref: str,
    abcorr: str,
    corloc: str,
    obsrvr: str,
    refvec: np.ndarray,
    rolstp: float,
    ncuts: int,
    schstp: float,
    soltol: float,
    maxn: int,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Find limb points on a target body. The limb is the set of points
    of tangency on the target of rays emanating from the observer.
    The caller specifies half-planes bounded by the observer-target
    center vector in which to search for limb points.

    The surface of the target body may be represented either by a
    triaxial ellipsoid or by topographic data.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/limbpt_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param et: Epoch in ephemeris seconds past J2000 TDB.
    :param fixref: Body-fixed, body-centered target body frame.
    :param abcorr: Aberration correction.
    :param corloc: Aberration correction locus.
    :param obsrvr: Name of observing body.
    :param refvec: Reference vector for cutting half-planes.
    :param rolstp: Roll angular step for cutting half-planes.
    :param ncuts: Number of cutting half-planes.
    :param schstp: Angular step size for searching.
    :param soltol: Solution convergence tolerance.
    :param maxn: Maximum number of entries in output arrays.
    :return: 
        Counts of limb points corresponding to cuts
        Limb points in km, 
        Times associated with limb points in seconds, 
        Tangent vectors emanating from the observer in km
    """
    if PyFloat_Check(et):
        return limbpt_s(method, target, et, fixref, abcorr, corloc, obsrvr, refvec, rolstp, ncuts, schstp, soltol, maxn)
    else:
        return limbpt_v(method, target, et, fixref, abcorr, corloc, obsrvr, refvec, rolstp, ncuts, schstp, soltol, maxn)


def lspcn_s(
    str body,
    double et,
    str abcorr
    ) -> float:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.lspcn`

    Compute L_s, the planetocentric longitude of the sun, as seen
    from a specified body.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/lspcn_c.html

    :param body: Name of central body.
    :param et: Epoch in seconds past J2000 TDB.
    :param abcorr: Aberration correction.
    :return: planetocentric longitude of the sun in radians
    """
    cdef double l_s = 0.0
    cdef double c_et = et
    cdef const char* c_body   = body
    cdef const char* c_abcorr = abcorr
    l_s = lspcn_c(
        c_body,
        c_et,
        c_abcorr
    )
    check_for_spice_error()
    return l_s


@boundscheck(False)
@wraparound(False)
def lspcn_v(
    str body,
    double[::1] ets,
    str abcorr
    ) -> Double_N:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.lspcn`

    Compute L_s, the planetocentric longitude of the sun, as seen
    from a specified body.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/lspcn_c.html

    :param body: Name of central body.
    :param ets: Epochs in seconds past J2000 TDB.
    :param abcorr: Aberration correction.
    :return: planetocentric longitudes of the sun in radians
    """
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    cdef const char* c_body   = body
    cdef const char* c_abcorr = abcorr
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_l_s_s = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_l_s_s = p_l_s_s
    with nogil:
        for i in range(n):
            c_l_s_s[i] = lspcn_c(
                c_body,
                c_ets[i],
                c_abcorr
            )
    check_for_spice_error()
    return p_l_s_s


def lspcn(
    body: str,
    et: float | float[::1],
    abcorr: str
    ) -> float | Double_N:
    """
    Compute L_s, the planetocentric longitude of the sun, as seen
    from a specified body.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/lspcn_c.html

    :param body: Name of central body.
    :param et: Epoch in seconds past J2000 TDB.
    :param abcorr: Aberration correction.
    :return: planetocentric longitude of the sun in radians
    """
    if PyFloat_Check(et):
        return lspcn_s(body, et, abcorr)
    else:
        return lspcn_v(body, et, abcorr)

# M

# N

# O

cpdef int occult_s(
    const char* target1,
    const char* shape1,
    const char* frame1,
    const char* target2,
    const char* shape2,
    const char* frame2,
    const char* abcorr,
    const char* observer,
    double et,
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.occult`

    Determines the occultation condition (not occulted, partially,
    etc.) of one target relative to another target as seen by
    an observer at a given time.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/occult_c.html

    :param target1: Name or ID of first target.
    :param shape1: Type of shape model used for first target.
    :param frame1: Body-fixed, body-centered frame for first body.
    :param target2: Name or ID of second target.
    :param shape2: Type of shape model used for second target.
    :param frame2: Body-fixed, body-centered frame for second body.
    :param abcorr: Aberration correction flag.
    :param observer: Name or ID of the observer.
    :param et: Time of the observation (seconds past J2000).
    :return: Occultation identification code.
    """
    cdef int c_ocltid = 0
    occult_c(
        target1,
        shape1,
        frame1,
        target2,
        shape2,
        frame2,
        abcorr,
        observer,
        et,
        &c_ocltid
    )
    check_for_spice_error()
    return c_ocltid


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.int32_t, ndim=1, mode='c'] occult_v(
    const char* target1,
    const char* shape1,
    const char* frame1,
    const char* target2,
    const char* shape2,
    const char* frame2,
    const char* abcorr,
    const char* observer,
    double[::1] ets,
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.occult`

    Determines the occultation condition (not occulted, partially,
    etc.) of one target relative to another target as seen by
    an observer at a given time.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/occult_c.html

    :param target1: Name or ID of first target.
    :param shape1: Type of shape model used for first target.
    :param frame1: Body-fixed, body-centered frame for first body.
    :param target2: Name or ID of second target.
    :param shape2: Type of shape model used for second target.
    :param frame2: Body-fixed, body-centered frame for second body.
    :param abcorr: Aberration correction flag.
    :param observer: Name or ID of the observer.
    :param ets: Time of the observation (seconds past J2000).
    :return: Occultation identification code.
    """
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # allocate output array
    cdef np.ndarray[np.int32_t, ndim=1, mode='c'] p_ocltids = np.empty(n, dtype=np.int32, order='C')
    cdef SpiceInt[::1] c_ocltids = p_ocltids
    with nogil:
        for i in range(n):
            occult_c(
                target1,
                shape1,
                frame1,
                target2,
                shape2,
                frame2,
                abcorr,
                observer,
                c_ets[i],
                &c_ocltids[i]
            )
    check_for_spice_error()
    return p_ocltids


def occult(
    target1: str,
    shape1: str,
    frame1: str,
    target2: str,
    shape2: str,
    frame2: str,
    abcorr: str,
    observer: str,
    et: float | float[::1]
    ) -> int | Int_N:
    """
    Determines the occultation condition (not occulted, partially,
    etc.) of one target relative to another target as seen by
    an observer at a given time.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/occult_c.html

    :param target1: Name or ID of first target.
    :param shape1: Type of shape model used for first target.
    :param frame1: Body-fixed, body-centered frame for first body.
    :param target2: Name or ID of second target.
    :param shape2: Type of shape model used for second target.
    :param frame2: Body-fixed, body-centered frame for second body.
    :param abcorr: Aberration correction flag.
    :param observer: Name or ID of the observer.
    :param et: Time(s) of the observation (seconds past J2000).
    :return: Occultation identification code.
    """
    if PyFloat_Check(et):
        return occult_s(target1, shape1, frame1, target2, shape2, frame2, abcorr, observer, et)
    else:
        return occult_v(target1, shape1, frame1, target2, shape2, frame2, abcorr, observer, et)


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=1, mode='c'] oscelt_s(
    const double[::1] state,
    double et,
    double mu,
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.oscelt`

    Determine the set of osculating conic orbital elements that
    corresponds to the state (position, velocity) of a body at
    some epoch.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/oscelt_c.html

    :param state: State of body at epoch of elements.
    :param et: Epoch of elements in ephemeris seconds past J2000.
    :param mu: Gravitational parameter (GM) of primary body in km**3/sec**2 units.
    :return: Equivalent conic elements in  km, rad, rad/sec units.
    """
    cdef const np.double_t[::1] c_state = np.ascontiguousarray(state, dtype=np.double)
    if c_state.shape[0] != 6:
        raise ValueError(f'in oscelt_s, state vector had shape {c_state.shape[0]}, not 6 as expected')
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_elts = np.empty(8, dtype=np.double, order='C')
    cdef np.double_t[::1] c_elts = p_elts
    oscelt_c(
        &c_state[0],
        et,
        mu,
        &c_elts[0]
    )
    check_for_spice_error()
    return p_elts


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=2, mode='c'] oscelt_v(
    const double[:,::1] state,
    double[::1] et,
    double mu,
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.oscelt`

    Determine the set of osculating conic orbital elements that
    corresponds to the state (position, velocity) of a body at
    some epoch.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/oscelt_c.html

    :param state: State of body at epoch of elements.
    :param et: Epoch of elements in ephemeris seconds past J2000.
    :param mu: Gravitational parameter (GM) of primary body in km**3/sec**2 units.
    :return: Equivalent conic elements in  km, rad, rad/sec units.
    """
    cdef const np.double_t[:,::1] c_state = np.ascontiguousarray(state, dtype=np.double)
    cdef const np.double_t[::1] c_et = np.ascontiguousarray(et, dtype=np.double)
    if c_state.shape[1] != 6:
        raise ValueError(f'in oscelt_v, state vector had shape {c_state.shape}, not Nx6 as expected')
    cdef Py_ssize_t i, n = c_state.shape[0]
    if c_et.shape[0] != n:
        raise ValueError(f'in oscelt_v, state and et vectors did not have the same length, state: {c_state.shape[0]} et: {c_et.shape[1]}')
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_elts = np.empty((n,8), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_elts = p_elts
    with nogil:
        for i in range(n):
            oscelt_c(
            &c_state[i, 0],
            et[i],
            mu,
            &c_elts[i, 0]
        )
    check_for_spice_error()
    return p_elts


cpdef oscelt(
    state: double[::1] | double[:,::1],
    et: float | double[::1],
    mu: float
    ):
    """
    Determine the set of osculating conic orbital elements that
    corresponds to the state (position, velocity) of a body at
    some epoch.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/oscelt_c.html

    :param state: State of body at epoch of elements.
    :param et: Epoch of elements in ephemeris seconds past J2000.
    :param mu: Gravitational parameter (GM) of primary body in km**3/sec**2 units.
    :return: Equivalent conic elements in  km, rad, rad/sec units.
    """
    cdef Py_ssize_t ndim = state.ndim
    if ndim == 1:
        return oscelt_s(state, et, mu)
    elif ndim == 2:
        return oscelt_v(state, et, mu)
    else:
        raise RuntimeError(f'Oscelt provided wrong shape for state: {ndim}')

# P

@boundscheck(False)
cpdef np.ndarray[np.double_t, ndim=1, mode='c'] pgrrec_s(
    const char* body,
    double lon,
    double lat,
    double alt,
    double re,
    double f,
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.pgrrec`

    Convert planetographic coordinates to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/pgrrec_c.html

    :param body: Body with which coordinate system is associated.
    :param lon: Planetographic longitude of a point (radians).
    :param lat: Planetographic latitude of a point (radians).
    :param alt: Altitude of a point above reference spheroid.
    :param re: Equatorial radius of the reference spheroid.
    :param f: Flattening coefficient.
    :return: Rectangular coordinates of the point.
    """
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_rec = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_rec = p_rec
    pgrrec_c(
        body,
        lon,
        lat,
        alt,
        re,
        f,
        &c_rec[0]
    )
    return p_rec


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=2, mode='c'] pgrrec_v(
    const char* body,
    const double[::1] lon,
    const double[::1] lat,
    const double[::1] alt,
    double re,
    double f,
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.pgrrec`

    Convert planetographic coordinates to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/pgrrec_c.html

    :param body: Body with which coordinate system is associated.
    :param lon: Planetographic longitude of each point (radians).
    :param lat: Planetographic latitude of each point (radians).
    :param alt: Altitude of each point above reference spheroid.
    :param re: Equatorial radius of the reference spheroid.
    :param f: Flattening coefficient.
    :return: Rectangular coordinates of the point.
    """
    cdef const np.double_t[::1] c_lon = np.ascontiguousarray(lon, dtype=np.double)
    cdef Py_ssize_t i, n = lon.shape[0]
    cdef const np.double_t[::1] c_lat = np.ascontiguousarray(lat, dtype=np.double)
    cdef const np.double_t[::1] c_alt = np.ascontiguousarray(alt, dtype=np.double)
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_rec = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_rec = p_rec
    # TODO fix strides lookups below
    with nogil:
        for i in range(n):
            pgrrec_c(
                body,
                c_lon[i],
                c_lat[i],
                c_alt[i],
                re,
                f,  
                &c_rec[i, 0]
            )
    return p_rec


def pgrrec(
    body: str,
    lon: float | double[::1],
    lat: float | double[::1],
    alt: float | double[::1],
    re: float,
    f: float
    ) -> Vector | Geodetic_N:
    """
    Convert planetographic coordinates to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/pgrrec_c.html

    :param body: Body with which coordinate system is associated.
    :param lon: Planetographic longitude of a point (radians).
    :param lat: Planetographic latitude of a point (radians).
    :param alt: Altitude of a point above reference spheroid.
    :param re: Equatorial radius of the reference spheroid.
    :param f: Flattening coefficient.
    :return: Rectangular coordinates of the point.
    """
    cdef const char* c_body = body
    if PyFloat_Check(lon):
        return pgrrec_s(c_body, lon, lat, alt, re, f)
    else:
        return pgrrec_v(c_body, lon, lat, alt, re, f)


cpdef double phaseq_s(
    double et,
    const char* target,
    const char* illmn,
    const char* obsrvr,
    const char* abcorr
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.phaseq`

    Compute the apparent phase angle for a target, observer,
    illuminator set of ephemeris objects.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/phaseq_c.html

    :param et: Ephemeris seconds past J2000 TDB.
    :param target: Target body name.
    :param illmn: Illuminating body name.
    :param obsrvr: Observer body.
    :param abcorr: Aberration correction flag.
    :return: Value of phase angle in radians.
    """
    cdef double c_phase = 0.0
    c_phase = phaseq_c(
        et,
        target,
        illmn,
        obsrvr,
        abcorr
    ) 
    check_for_spice_error()
    return c_phase


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=1, mode='c'] phaseq_v(
    double[::1] et,
    const char* target,
    const char* illmn,
    const char* obsrvr,
    const char* abcorr
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.phaseq`

    Compute the apparent phase angle for a target, observer,
    illuminator set of ephemeris objects.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/phaseq_c.html

    :param et: Ephemeris seconds past J2000 TDB.
    :param target: Target body name.
    :param illmn: Illuminating body name.
    :param obsrvr: Observer body.
    :param abcorr: Aberration correction flag.
    :return: Value of phase angle in radians.
    """
    cdef const np.double_t[::1] c_et = np.ascontiguousarray(et, dtype=np.double)
    cdef Py_ssize_t i, n = c_et.shape[0]
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_phase = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_phase = p_phase
    # perform the call
    with nogil:
        for i in range(n):
            c_phase[i] = phaseq_c(
                c_et[i],
                target,
                illmn,
                obsrvr,
                abcorr
            ) 
    check_for_spice_error()
    return p_phase


def phaseq(
    et: float | double[::1] ,
    target : str,
    illmn  : str,
    obsrvr : str,
    abcorr : str
    ) -> float | Double_N:
    """
    Compute the apparent phase angle for a target, observer,
    illuminator set of ephemeris objects.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/phaseq_c.html

    :param et: Ephemeris seconds past J2000 TDB.
    :param target: Target body name.
    :param illmn: Illuminating body name.
    :param obsrvr: Observer body.
    :param abcorr: Aberration correction flag.
    :return: Value of phase angle in radians.
    """
    if PyFloat_Check(et):
        return phaseq_s(et, target, illmn, obsrvr, abcorr)
    else:
        return phaseq_v(et, target, illmn, obsrvr, abcorr)


def pi() -> float:
    """
    Return the value of pi (the ratio of the circumference of
    a circle to its diameter).

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/pi_c.html

    :return: value of pi.
    """
    return pi_c()


@boundscheck(False)
@wraparound(False)
def pxform_s(
    str fromstring,
    str tostring,
    double et
    ) -> Matrix_3:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.pxform`

    Return the matrix that transforms position vectors from one
    specified frame to another at a specified epoch.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/pxform_c.html


    :param instring: Name of the frame to transform from.
    :param tostring: Name of the frame to transform to.
    :param et: Epoch of the rotation matrix.
    :return: A rotation matrix.
    """
    # initialize c variables
    cdef double c_et = et
    cdef const char* c_fromstring = fromstring
    cdef const char* c_tostring = tostring
    # initialize output
    cdef np.ndarray[np.double_t, ndim=2, mode="c"] p_xrot = np.empty((3, 3), dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_xrot = p_xrot
    pxform_c(
        c_fromstring,
        c_tostring,
        c_et,
        <SpiceDouble (*)[3]> &c_xrot[0, 0]
    )
    check_for_spice_error()
    return p_xrot


@boundscheck(False)
@wraparound(False)
def pxform_v(
    str fromstring,
    str tostring,
    double[::1] ets
    ) -> Matrix_N_3:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.pxform`

    Return the matrix that transforms position vectors from one
    specified frame to another at a specified epoch.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/pxform_c.html


    :param instring: Name of the frame to transform from.
    :param tostring: Name of the frame to transform to.
    :param ets: Epochs of the rotation matricies.
    :return: rotation matricies.
    """
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    cdef const char* c_fromstring = fromstring
    cdef const char* c_tostring = tostring
    # initialize output
    cdef np.ndarray[np.double_t, ndim=3, mode="c"] p_xrot = np.empty((n, 3, 3), dtype=np.double, order='C')
    cdef np.double_t[:, :, ::1] c_xrot = p_xrot
    # pointer to element
    cdef SpiceDouble* base = &c_xrot[0, 0, 0]
    with nogil:
        for i in range(n):
            pxform_c(
                c_fromstring,
                c_tostring,
                c_ets[i],
                <SpiceDouble (*)[3]> (base + i*9)
            )
    check_for_spice_error()
    return p_xrot


def pxform(
    fromstring: str,
    tostring:   str,
    et: float | float[::1]
    ) -> Matrix_3 | Matrix_N_3:
    """
    Return the matrix that transforms position vectors from one
    specified frame to another at a specified epoch.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/pxform_c.html


    :param instring: Name of the frame to transform from.
    :param tostring: Name of the frame to transform to.
    :param et: Epoch of the rotation matrix.
    :return: A rotation matrix.
    """
    if PyFloat_Check(et):
        return pxform_s(fromstring, tostring, et)
    else:
        return pxform_v(fromstring, tostring, et)

# Q


cpdef str qcktrc(
    int tracelen
    ):
    """
    Return a string containing a traceback.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/qcktrc_c.html

    :param tracelen: Maximum length of output traceback string.
    :return: A traceback string.
    """
    cdef int c_tracelen = tracelen
    cdef Py_ssize_t length = _default_len_out
    if c_tracelen <= 0:
        raise ValueError("tracelen must be positive")
    cdef char* c_tracestr = <char*> malloc((tracelen) * sizeof(char))
    if c_tracestr == NULL:
        raise MemoryError("Unable to allocate memory for traceback string in qcktrc.")
    try:
        qcktrc_c(
            c_tracelen,
            c_tracestr
        )
        length = strlen(c_tracestr)
        p_tracestr = PyUnicode_DecodeUTF8(c_tracestr, length, "strict")
        return p_tracestr
    finally:
        free(c_tracestr)

# R
@boundscheck(False)
cpdef np.ndarray[np.double_t, ndim=1, mode='c'] radrec_s(
    inrange: float, 
    ra: float, 
    dec: float
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.radrec`

    Convert from range, right ascension, and declination to rectangular
    coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/radrec_c.html

    :param inrange: Distance of a point from the origin.
    :param ra: Right ascension of point in radians.
    :param dec: Declination of point in radians.
    :return: Rectangular coordinates of the point.
    """
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_rec = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_rec = p_rec
    radrec_c(
        inrange, 
        ra, 
        dec, 
        &c_rec[0],
    )
    return p_rec


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=2, mode='c'] radrec_v(
    const double[::1] inrange, 
    const double[::1] ra, 
    const double[::1] dec
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.radrec`

    Convert from range, right ascension, and declination to rectangular
    coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/radrec_c.html

    :param inrange: Distance of a point from the origin.
    :param ra: Right ascension of point in radians.
    :param dec: Declination of point in radians.
    :return: Rectangular coordinates of the point.
    """
    cdef const np.double_t[::1] c_range = np.ascontiguousarray(inrange, dtype=np.double)
    cdef Py_ssize_t i, n = c_range.shape[0]
    cdef const np.double_t[::1] c_ra = np.ascontiguousarray(ra, dtype=np.double)
    cdef const np.double_t[::1] c_dec = np.ascontiguousarray(dec, dtype=np.double)
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_rec = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_rec = p_rec
    # TODO fix strides lookups below
    with nogil:
        for i in range(n):
            radrec_c(
                c_range[i], 
                c_ra[i], 
                c_dec[i], 
                &c_rec[i, 0]
            )
    return p_rec


def radrec(
    inrange: float | double[::1], 
    ra: float | double[::1], 
    dec: float | double[::1]
    ) -> Vector | Rectangular_N:
    """
    Convert from range, right ascension, and declination to rectangular
    coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/radrec_c.html

    :param inrange: Distance of a point from the origin.
    :param ra: Right ascension of point in radians.
    :param dec: Declination of point in radians.
    :return: Rectangular coordinates of the point.
    """
    if PyFloat_Check(inrange):
        return radrec_s(inrange, ra, dec)
    else:
        return radrec_v(inrange, ra, dec)


@boundscheck(False)
cpdef tuple[float, float, float] recazl_s(
    double[::1] rectan,
    SpiceBoolean azccw,
    SpiceBoolean elplsz
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.recazl`

    Convert rectangular coordinates of a point to range, azimuth and
    elevation.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/recazl_c.html

    :param rectan: Rectangular coordinates of a point.
    :param azccw: Flag indicating how Azimuth is measured.
    :param elplsz: Flag indicating how Elevation is measured.
    :return:
            Distance of the point from the origin,
            Azimuth in radians,
            Elevation in radians.
    """
    cdef const double* c_rectan = &rectan[0]
    cdef double orange = 0.0
    cdef double az = 0.0
    cdef double el = 0.0
    recazl_c(
        c_rectan, 
        <SpiceBoolean> azccw, 
        <SpiceBoolean> elplsz, 
        &orange,
        &az,
        &el
    )
    return orange, az, el


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=2, mode='c'] recazl_v(
    const double[:,::1] rectan, 
    const SpiceBoolean azccw, 
    const SpiceBoolean elplsz
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.recazl`

    Convert rectangular coordinates points to range, azimuth and
    elevation.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/recazl_c.html

    :param rectan: Rectangular coordinates of points.
    :param azccw: Flag indicating how Azimuth is measured.
    :param elplsz: Flag indicating how Elevation is measured.
    :return:
            Distance of the point from the origin,
            Azimuth in radians,
            Elevation in radians.
    """
    cdef Py_ssize_t i, n = rectan.shape[0]
    cdef SpiceBoolean c_azccw  = <SpiceBoolean> azccw 
    cdef SpiceBoolean c_elplsz = <SpiceBoolean> elplsz
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_azl = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_azl = p_azl
    # TODO fix strides lookups below
    with nogil:
        for i in range(n):
            recazl_c(
                &rectan[i, 0], 
                c_azccw,
                c_elplsz, 
                &c_azl[i, 0],
                &c_azl[i, 1],
                &c_azl[i, 2]
            )
    return p_azl


def recazl(
    rectan: double[::1] | double[:,::1], 
    azccw: bool | SpiceBoolean, 
    elplsz: bool | SpiceBoolean
    ) -> tuple[float, float, float] | Rectangular_N:
    """
    Convert rectangular coordinates points to range, azimuth and
    elevation.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/recazl_c.html

    :param rectan: Rectangular coordinates of points.
    :param azccw: Flag indicating how Azimuth is measured.
    :param elplsz: Flag indicating how Elevation is measured.
    :return:
            Distance of the point from the origin,
            Azimuth in radians,
            Elevation in radians.
    """
    cdef Py_ssize_t ndim = rectan.ndim
    if ndim == 1:
        return recazl_s(rectan, azccw, elplsz)
    elif ndim == 2:
        return recazl_v(rectan, azccw, elplsz)
    else:
        raise RuntimeError(f'Rectan provided wrong shape of {ndim}')


@boundscheck(False)
cpdef tuple[float, float, float] reccyl_s(
    double[::1] rectan
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.reccyl`

    Convert from rectangular to cylindrical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/reccyl_c.html

    :param rectan: Rectangular coordinates of a point.
    :return:
            Distance from z axis,
            Angle (radians) from xZ plane,
            Height above xY plane.
    """
    cdef const double* c_rectan = &rectan[0]
    cdef double r = 0.0
    cdef double clon = 0.0
    cdef double z = 0.0
    reccyl_c(
        c_rectan, 
        &r,
        &clon,
        &z
    )
    return r, clon, z


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=2, mode='c'] reccyl_v(
    const double[:,::1] rectan
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.reccyl`

    Convert from rectangular to cylindrical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/reccyl_c.html

    :param rectan: Rectangular coordinates of a point.
    :return:
            Distance from z axis,
            Angle (radians) from xZ plane,
            Height above xY plane.
    """
    cdef Py_ssize_t i, n = rectan.shape[0]
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_cyl = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_cyl = p_cyl
    # TODO fix strides lookups below
    with nogil:
        for i in range(n):
            reccyl_c(
                &rectan[i, 0],  
                &c_cyl[i, 0],
                &c_cyl[i, 1],
                &c_cyl[i, 2]
            )
    return p_cyl


def reccyl(
    rectan: double[::1] | double[:,::1]
    ) -> tuple[float, float, float] | Cylindrical_N:
    """
    Convert from rectangular to cylindrical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/reccyl_c.html

    :param rectan: Rectangular coordinates of a point.
    :return:
            Distance from z axis,
            Angle (radians) from xZ plane,
            Height above xY plane.
    """
    cdef Py_ssize_t ndim = rectan.ndim
    if ndim == 1:
        return reccyl_s(rectan)
    elif ndim == 2:
        return reccyl_v(rectan)
    else:
        raise RuntimeError(f'Rectan provided wrong shape of {ndim}')


@boundscheck(False)
cpdef tuple[float, float, float] recgeo_s(
    double[::1] rectan,
    double re,
    double f,
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.recgeo`

    Convert from rectangular coordinates to geodetic coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/recgeo_c.html

    :param rectan: Rectangular coordinates of a point.
    :param re: Equatorial radius of the reference spheroid.
    :param f: Flattening coefficient.
    :return:
            Geodetic longitude (radians),
            Geodetic latitude (radians),
            Altitude above reference spheroid
    """
    cdef const double* c_rectan = &rectan[0]
    cdef double lon = 0.0
    cdef double lat = 0.0
    cdef double alt = 0.0
    recgeo_c(
        c_rectan, 
        re,
        f,
        &lon,
        &lat,
        &alt
    )
    return lon, lat, alt


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=2, mode='c'] recgeo_v(
    const double[:,::1] rectan,
    double re,
    double f,
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.recgeo`

    Convert from rectangular coordinates to geodetic coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/recgeo_c.html

    :param rectan: Rectangular coordinates of a point.
    :param re: Equatorial radius of the reference spheroid.
    :param f: Flattening coefficient.
    :return:
            Geodetic longitude (radians),
            Geodetic latitude (radians),
            Altitude above reference spheroid
    """
    cdef Py_ssize_t i, n = rectan.shape[0]
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_geo = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_geo = p_geo
    # TODO fix strides lookups below
    with nogil:
        for i in range(n):
            recgeo_c(
                &rectan[i, 0],
                re,
                f,  
                &c_geo[i, 0],
                &c_geo[i, 1],
                &c_geo[i, 2]
            )
    return p_geo


def recgeo(
    rectan: double[::1] | double[:,::1],
    re: float,
    f: float,
    ) -> tuple[float, float, float] | Geodetic_N:
    """
    Convert from rectangular coordinates to geodetic coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/recgeo_c.html

    :param rectan: Rectangular coordinates of a point.
    :param re: Equatorial radius of the reference spheroid.
    :param f: Flattening coefficient.
    :return:
            Geodetic longitude (radians),
            Geodetic latitude (radians),
            Altitude above reference spheroid
    """
    cdef Py_ssize_t ndim = rectan.ndim
    if ndim == 1:
        return recgeo_s(rectan, re, f)
    elif ndim == 2:
        return recgeo_v(rectan, re, f)
    else:
        raise RuntimeError(f'Rectan provided wrong shape of {ndim}')


@boundscheck(False)
cpdef tuple[float, float, float] reclat_s(
    double[::1] rectan
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.reclat`

    Convert from rectangular coordinates to latitudinal coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/reclat_c.html

    :param rectan: Rectangular coordinates of a point.
    :return: Distance from the origin, Longitude in radians, Latitude in radians
    """
    cdef const double* c_rectan = &rectan[0]
    cdef double radius = 0.0
    cdef double lon = 0.0
    cdef double lat = 0.0
    reclat_c(
        c_rectan, 
        &radius,
        &lon,
        &lat
    )
    return radius, lon, lat


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=2, mode='c'] reclat_v(
    const double[:,::1] rectan
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.reclat`

    Convert from rectangular coordinates to latitudinal coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/reclat_c.html

    :param rectan: Rectangular coordinates of a point.
    :return: Distance from the origin, Longitude in radians, Latitude in radians
    """
    cdef Py_ssize_t i, n = rectan.shape[0]
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_lat = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_lat = p_lat
    # TODO fix strides lookups below
    with nogil:
        for i in range(n):
            reclat_c(
                &rectan[i, 0],  
                &c_lat[i, 0],
                &c_lat[i, 1],
                &c_lat[i, 2]
            )
    return p_lat


def reclat(
    rectan: double[::1] | double[:,::1]
    ) -> tuple[float, float, float] | Latitudinal_N:
    """
    Convert from rectangular coordinates to latitudinal coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/reclat_c.html

    :param rectan: Rectangular coordinates of a point.
    :return: Distance from the origin, Longitude in radians, Latitude in radians
    """
    cdef Py_ssize_t ndim = rectan.ndim
    if ndim == 1:
        return reclat_s(rectan)
    elif ndim == 2:
        return reclat_v(rectan)
    else:
        raise RuntimeError(f'Rectan provided wrong shape of {ndim}')


@boundscheck(False)
cpdef tuple[float, float, float] recpgr_s(
    const char* body,
    double[::1] rectan,
    double re,
    double f,
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.recpgr`

    Convert rectangular coordinates to planetographic coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/recpgr_c.html

    :param body: Body with which coordinate system is associated.
    :param rectan: Rectangular coordinates of a point.
    :param re: Equatorial radius of the reference spheroid.
    :param f: Flattening coefficient.
    :return:
            Planetographic longitude (radians),
            Planetographic latitude (radians),
            Altitude above reference spheroid
    """
    cdef double* c_rectan = &rectan[0]
    cdef double lon = 0.0
    cdef double lat = 0.0
    cdef double alt = 0.0
    recpgr_c(
        body,
        c_rectan, 
        re,
        f,
        &lon,
        &lat,
        &alt
    )
    return lon, lat, alt


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=2, mode='c'] recpgr_v(
    const char* body,
    double[:,::1] rectan,
    double re,
    double f,
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.recpgr`

    Convert rectangular coordinates to planetographic coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/recpgr_c.html

    :param body: Body with which coordinate system is associated.
    :param rectan: Rectangular coordinates of a point.
    :param re: Equatorial radius of the reference spheroid.
    :param f: Flattening coefficient.
    :return:
            Planetographic longitude (radians),
            Planetographic latitude (radians),
            Altitude above reference spheroid
    """
    cdef Py_ssize_t i, n = rectan.shape[0]
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_pgr = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_pgr = p_pgr
    # TODO fix strides lookups below
    with nogil:
        for i in range(n):
            recpgr_c(
                body,
                &rectan[i, 0],
                re,
                f,  
                &c_pgr[i, 0],
                &c_pgr[i, 1],
                &c_pgr[i, 2]
            )
    return p_pgr


def recpgr(
    body: str,
    rectan: double[::1] | double[:,::1],
    re: float,
    f: float,
    ) -> tuple[float, float, float] | Planetographic_N:
    """
    Convert rectangular coordinates to planetographic coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/recpgr_c.html

    :param body: Body with which coordinate system is associated.
    :param rectan: Rectangular coordinates of a/the point(s).
    :param re: Equatorial radius of the reference spheroid.
    :param f: Flattening coefficient.
    :return:
            Planetographic longitude (radians),
            Planetographic latitude (radians),
            Altitude above reference spheroid
    """
    cdef Py_ssize_t ndim = rectan.ndim
    if ndim == 1:
        return recpgr_s(body, rectan, re, f)
    elif ndim == 2:
        return recpgr_v(body, rectan, re, f)
    else:
        raise RuntimeError(f'Rectan provided wrong shape of {ndim}')


@boundscheck(False)
cpdef tuple[float, float, float] recrad_s(
    double[::1] rectan
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.recrad`

    Convert rectangular coordinates to range, right ascension, and declination.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/recrad_c.html

    :param rectan: Rectangular coordinates of a point.
    :return:
            Distance of the point from the origin,
            Right ascension in radians,
            Declination in radians
    """
    cdef const double* c_rectan = &rectan[0]
    cdef double orange = 0.0
    cdef double ra = 0.0
    cdef double dec = 0.0
    recrad_c(
        c_rectan, 
        &orange,
        &ra,
        &dec
    )
    return orange, ra, dec


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=2, mode='c'] recrad_v(
    const double[:,::1] rectan
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.recrad`

    Convert rectangular coordinates to range, right ascension, and declination.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/recrad_c.html

    :param rectan: Rectangular coordinates of a point.
    :return:
            Distance of the point from the origin,
            Right ascension in radians,
            Declination in radians
    """
    cdef Py_ssize_t i, n = rectan.shape[0]
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_rad = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_rad = p_rad
    # TODO fix strides lookups below
    with nogil:
        for i in range(n):
            recrad_c(
                &rectan[i, 0],  
                &c_rad[i, 0],
                &c_rad[i, 1],
                &c_rad[i, 2]
            )
    return p_rad


def recrad(
    rectan: double[::1] | double[:,::1]
    ) -> tuple[float, float, float] | Vector_N:
    """
    Convert rectangular coordinates to range, right ascension, and declination.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/recrad_c.html

    :param rectan: Rectangular coordinates of a point.
    :return:
            Distance of the point from the origin,
            Right ascension in radians,
            Declination in radians
    """
    cdef Py_ssize_t ndim = rectan.ndim
    if ndim == 1:
        return recrad_s(rectan)
    elif ndim == 2:
        return recrad_v(rectan)
    else:
        raise RuntimeError(f'Rectan provided wrong shape of {ndim}')


@boundscheck(False)
cpdef tuple[float, float, float] recsph_s(
    double[::1] rectan
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.recsph`

    Convert from rectangular coordinates to spherical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/recrad_c.html

    :param rectan: Rectangular coordinates of a point.
    :return:
            Distance from the origin,
            Angle from the positive Z-axis,
            Longitude in radians.
    """
    cdef const double* c_rectan = &rectan[0]
    cdef double r = 0.0
    cdef double colat = 0.0
    cdef double slon = 0.0
    recsph_c(
        c_rectan, 
        &r,
        &colat,
        &slon
    )
    return r, colat, slon


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=2, mode='c'] recsph_v(
    const double[:,::1] rectan
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.recsph`

    Convert from rectangular coordinates to spherical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/recrad_c.html

    :param rectan: Rectangular coordinates of a point.
    :return:
            Distance from the origin,
            Angle from the positive Z-axis,
            Longitude in radians.
    """
    cdef Py_ssize_t i, n = rectan.shape[0]
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_sph = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_sph = p_sph
    # TODO fix strides lookups below
    with nogil:
        for i in range(n):
            recsph_c(
                &rectan[i, 0],  
                &c_sph[i, 0],
                &c_sph[i, 1],
                &c_sph[i, 2]
            )
    return p_sph


def recsph(
    rectan: double[::1] | double[:,::1]
    ) -> tuple[float, float, float] | Spherical_N:
    """
    Convert from rectangular coordinates to spherical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/recrad_c.html

    :param rectan: Rectangular coordinates of a point.
    :return:
            Distance from the origin,
            Angle from the positive Z-axis,
            Longitude in radians.
    """
    cdef Py_ssize_t ndim = rectan.ndim
    if ndim == 1:
        return recsph_s(rectan)
    elif ndim == 2:
        return recsph_v(rectan)
    else:
        raise RuntimeError(f'Rectan provided wrong shape of {ndim}')


cpdef void reset() noexcept:
    """
    Reset the SPICE error status to a value of "no error."
    As a result, the status routine, :py:meth:`~spiceypy.cyice.cyice.failed`, will return a value
    of False

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/reset_c.html

    """
    reset_c()


def rpd() -> float:
    """
    Return the number of radians per degree.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/rpd_c.html

    :return: The number of radians per degree, pi/180.
    """
    return rpd_c()


# S
def scdecd_s(
    int sc,
    double sclkdp
    ) -> str:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.scdecd`

    Convert double precision encoding of spacecraft clock time into
    a character representation.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/scdecd_c.html

    :param sc: NAIF spacecraft identification code.
    :param sclkdp: Encoded representation of a spacecraft clock count.
    :return: Character representation of a clock count.
    """
    cdef int c_sc = sc
    cdef double c_sclkdp = sclkdp
    cdef char[_default_len_out] c_buffer
    scdecd_c(
        c_sc,
        c_sclkdp,
        _default_len_out,
        &c_buffer[0]
    )
    check_for_spice_error()
    p_clkout = PyUnicode_DecodeUTF8(c_buffer, strlen(c_buffer), "strict")
    return p_clkout


@boundscheck(False)
@wraparound(False)
def scdecd_v(
    int sc,
    double[::1] sclkdps
    ) -> String_N:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.scdecd`

    Convert double precision encoding of spacecraft clock time into
    a character representation.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/scdecd_c.html

    :param sc: NAIF spacecraft identification code.
    :param sclkdps: Encoded representations of a spacecraft clock count.
    :return: Character representation of a clock count.
    """
    cdef int c_sc = sc
    cdef const np.double_t[::1] c_sclkdps = np.ascontiguousarray(sclkdps, dtype=np.double)
    cdef Py_ssize_t i, n = c_sclkdps.shape[0]
    # initialize output arrays
    p_np_s_dtype = np.dtype(('S', _default_len_out))
    p_np_u_dtype = np.dtype(('U', _default_len_out))
    cdef np.ndarray[np.uint8_t, ndim=2, mode='c'] p_sclkchs = np.zeros((n, _default_len_out), dtype=np.uint8, order='C')
    cdef np.uint8_t[:, ::1] c_sclkchs = p_sclkchs
    cdef char* base = <char*> &c_sclkchs[0, 0]
    with nogil:
        for i in range(n):
            scdecd_c(
                c_sc,
                c_sclkdps[i],
                _default_len_out,
                base + i*_default_len_out
            )
    check_for_spice_error()
    # return values
    py_sclkchs = p_sclkchs.view(p_np_s_dtype).reshape(n)
    py_sclkchs = np.char.rstrip(py_sclkchs).astype(p_np_u_dtype)
    return py_sclkchs


def scdecd(
    sc: int,
    sclkdp: float | float[::1]
    ) -> str | String_N:
    """
    Convert double precision encoding of spacecraft clock time into
    a character representation.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/scdecd_c.html

    :param sc: NAIF spacecraft identification code.
    :param sclkdp: Encoded representation of a spacecraft clock count.
    :return: Character representation of a clock count.
    """
    if PyFloat_Check(sclkdp):
        return scdecd_s(sc, sclkdp)
    else:
        return scdecd_v(sc, sclkdp)


def scencd_s(
    int sc,
    str sclkch
    ) -> float:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.scencd`

    Encode character representation of spacecraft clock time into a
    double precision number.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/scencd_c.html

    :param sc: NAIF spacecraft identification code.
    :param sclkch: Character representation of a spacecraft clock.
    :return: Encoded representation of the clock count.
    """
    cdef int c_sc = sc
    cdef double c_sclkdp = 0.0
    cdef const char* c_sclkch = sclkch
    scencd_c(
        c_sc,
        c_sclkch,
        &c_sclkdp
    )
    check_for_spice_error()
    return c_sclkdp


@boundscheck(False)
@wraparound(False)
def scencd_v(
    int sc,
    np.ndarray sclkchs
    ) -> Double_N:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.scencd`

    Encode character representation of spacecraft clock time into a
    double precision number.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/scencd_c.html

    :param sc: NAIF spacecraft identification code.
    :param sclkchs: Character representations of a spacecraft clock.
    :return: Encoded representations of the clock count.
    """
    cdef int c_sc = sc
    cdef Py_ssize_t i, n = sclkchs.shape[0]
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_sclkdps = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_sclkdps = p_sclkdps
    cdef const char* c_sclkchs_ptr
    # TODO possibly this is faster than calling encode via numpy, but it calls a lot of python methods, so see if there is room to improve this
    cdef bytes encoded
    for i in range(n):
        encoded = sclkchs[i].encode('ascii')
        c_sclkchs_ptr = encoded
        scencd_c(
            c_sc,
            c_sclkchs_ptr,
            &c_sclkdps[i]
        )
    check_for_spice_error()
    return p_sclkdps


def scencd(
    sc: int,
    sclkch: str | String_N
    ) -> float | Double_N:
    """
    Encode character representation of spacecraft clock time into a
    double precision number.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/scencd_c.html

    :param sc: NAIF spacecraft identification code.
    :param sclkch: Character representation of a spacecraft clock.
    :return: Encoded representation of the clock count.
    """
    if PyUnicode_Check(sclkch):
        return scencd_s(sc, sclkch)
    else:
        return scencd_v(sc, sclkch)


def sce2c_s(
    int sc,
    double et
    ) -> float:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.sce2c`

    Convert ephemeris seconds past J2000 (ET) to continuous encoded
    spacecraft clock "ticks".  Non-integral tick values may be
    returned.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/sce2c_c.html

    :param sc: NAIF spacecraft ID code.
    :param et: Ephemeris time, seconds past J2000 TDB.
    :return:
            SCLK, encoded as ticks since spacecraft clock start.
            sclkdp need not be integral.
    """
    cdef int c_sc = sc
    cdef double c_et = et
    cdef double c_sclkdp = 0.0
    sce2c_c(
        c_sc,
        c_et,
        &c_sclkdp
    )
    check_for_spice_error()
    return c_sclkdp


@boundscheck(False)
@wraparound(False)
def sce2c_v(
    int sc,
    double[::1] ets
) -> Double_N:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.sce2c`

    Convert ephemeris seconds past J2000 (ET) to continuous encoded
    spacecraft clock "ticks".  Non-integral tick values may be
    returned.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/sce2c_c.html

    :param sc: NAIF spacecraft ID code.
    :param ets: Ephemeris times, seconds past J2000 TDB.
    :return:
            SCLK, encoded as ticks since spacecraft clock start.
            sclkdp need not be integral.
    """
    cdef int c_sc = sc
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_sclkdps = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_sclkdps = p_sclkdps
    with nogil:
        for i in range(n):
            sce2c_c(
                c_sc,
                c_ets[i],
                &c_sclkdps[i]
            )
    check_for_spice_error()
    return p_sclkdps


def sce2c(
    sc: int,
    et: float | float[::1]
    ) -> float | Double_N:
    """
    Convert ephemeris seconds past J2000 (ET) to continuous encoded
    spacecraft clock "ticks".  Non-integral tick values may be
    returned.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/sce2c_c.html

    :param sc: NAIF spacecraft ID code.
    :param et: Ephemeris time, seconds past J2000 TDB.
    :return:
            SCLK, encoded as ticks since spacecraft clock start.
            sclkdp need not be integral.
    """
    if PyFloat_Check(et):
        return sce2c_s(sc, et)
    else:
        return sce2c_v(sc, et)


def sce2s_s(
    int sc,
    double et
    ) -> str:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.sce2s`

    Convert an epoch specified as ephemeris seconds past J2000 (ET) to a
    character string representation of a spacecraft clock value (SCLK).

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/sce2s_c.html

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
    check_for_spice_error()
    p_sclks = PyUnicode_DecodeUTF8(c_buffer, strlen(c_buffer), "strict")
    return p_sclks


@boundscheck(False)
@wraparound(False)
def sce2s_v(
    int sc,
    double[::1] ets
    ) -> String_N:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.sce2s`

    Convert an epoch specified as ephemeris seconds past J2000 (ET) to a
    character string representation of a spacecraft clock value (SCLK).

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/sce2s_c.html

    :param sc: NAIF spacecraft clock ID code.
    :param ets: Ephemeris times, specified as seconds past J2000 TDB.
    :param lenout: Maximum length of output string.
    :return: An SCLK string.
    """
    cdef int c_sc = sc
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # initialize output arrays
    p_np_s_dtype = np.dtype(('S', _default_len_out))
    p_np_u_dtype = np.dtype(('U', _default_len_out))
    cdef np.ndarray[np.uint8_t, ndim=2, mode='c'] p_sclkchs = np.zeros((n, _default_len_out), dtype=np.uint8, order='C')
    cdef np.uint8_t[:, ::1] c_sclkchs = p_sclkchs
    cdef char* base = <char*> &c_sclkchs[0, 0]
    with nogil:
        for i in range(n):
            sce2s_c(
                c_sc,
                c_ets[i],
                _default_len_out,
                base + i*_default_len_out
            )
    check_for_spice_error()
    # return values
    py_sclkchs = p_sclkchs.view(p_np_s_dtype).reshape(n)
    py_sclkchs = np.char.rstrip(py_sclkchs).astype(p_np_u_dtype)
    return py_sclkchs


def sce2s(
    sc: int,
    et: float | float[::1]
    ) -> str | String_N:
    """
    Convert an epoch specified as ephemeris seconds past J2000 (ET) to a
    character string representation of a spacecraft clock value (SCLK).

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/sce2s_c.html

    :param sc: NAIF spacecraft clock ID code.
    :param et: Ephemeris time, specified as seconds past J2000 TDB.
    :return: An SCLK string.
    """
    if PyFloat_Check(et):
        return sce2s_s(sc, et)
    else:
        return sce2s_v(sc, et)


def scs2e_s(
    int sc,
    str sclkch
    ) -> float:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.scs2e`

    Convert a spacecraft clock string to ephemeris seconds past J2000 (ET).

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/scs2e_c.html

    :param sc: NAIF integer code for a spacecraft.
    :param sclkch: An SCLK string.
    :return: Ephemeris time, seconds past J2000.
    """
    cdef int c_sc = sc
    cdef double c_et = 0.0
    cdef const char* c_sclkch = sclkch
    scs2e_c(
        c_sc,
        c_sclkch,
        &c_et
    )
    check_for_spice_error()
    return c_et


@boundscheck(False)
@wraparound(False)
def scs2e_v(
    int sc,
    np.ndarray sclkchs
    ) -> Double_N:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.scs2e`

    Convert a spacecraft clock string to ephemeris seconds past J2000 (ET).

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/scs2e_c.html

    :param sc: NAIF integer code for a spacecraft.
    :param sclkchs: SCLK strings.
    :return: Ephemeris time, seconds past J2000.
    """
    cdef int c_sc = sc
    cdef Py_ssize_t i, n = sclkchs.shape[0]
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_ets = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_ets = p_ets
    cdef const char* c_sclkchs
    # coerce unicode to a byte-string array
    if sclkchs.dtype.kind == 'U':
        sclkchs = np.char.encode(sclkchs, 'ascii')
    for i in range(n):
        c_sclkchs = sclkchs[i]
        scs2e_c(
            c_sc,
            c_sclkchs,
            &c_ets[i]
        )
    check_for_spice_error()
    return p_ets


def scs2e(
    sc: int,
    sclkch: str | np.ndarray
    ) -> float | Double_N:
    """
    Convert a spacecraft clock string to ephemeris seconds past J2000 (ET).

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/scs2e_c.html

    :param sc: NAIF integer code for a spacecraft.
    :param sclkch: An SCLK string.
    :return: Ephemeris time, seconds past J2000.
    """
    if PyUnicode_Check(sclkch):
        return scs2e_s(sc, sclkch)
    else:
        return scs2e_v(sc, sclkch)


def sct2e_s(
    int sc,
    double sclkdp
    ) -> float:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.sct2e`

    Convert encoded spacecraft clock ("ticks") to ephemeris
    seconds past J2000 (ET).

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/sct2e_c.html

    :param sc: NAIF spacecraft ID code.
    :param sclkdp: SCLK, encoded as ticks since spacecraft clock start.
    :return: Ephemeris time, seconds past J2000.
    """
    cdef double c_sclkdp = sclkdp
    cdef int c_sc = sc
    cdef double et = 0.0
    sct2e_c(
        c_sc,
        c_sclkdp,
        &et
    )
    check_for_spice_error()
    return et


@boundscheck(False)
@wraparound(False)
def sct2e_v(
    int sc,
    double[::1] sclkdps
    ) -> Double_N:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.sct2e`

    Convert encoded spacecraft clock ("ticks") to ephemeris
    seconds past J2000 (ET).

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/sct2e_c.html

    :param sc: NAIF spacecraft ID code.
    :param sclkdps: SCLKs, encoded as ticks since spacecraft clock start.
    :return: Ephemeris time, seconds past J2000.
    """
    cdef int c_sc = sc
    cdef const np.double_t[::1] c_sclkdps = np.ascontiguousarray(sclkdps, dtype=np.double)
    cdef Py_ssize_t i, n = c_sclkdps.shape[0]
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_ets = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_ets = p_ets
    with nogil:
        for i in range(n):
            sct2e_c(
                c_sc,
                c_sclkdps[i],
                &c_ets[i]
            )
    check_for_spice_error()
    return p_ets


def sct2e(
    sc: int,
    sclkdp: float | float[::1]
    ) -> float | Double_N:
    """
    Convert encoded spacecraft clock ("ticks") to ephemeris
    seconds past J2000 (ET).

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/sct2e_c.html

    :param sc: NAIF spacecraft ID code.
    :param sclkdp: SCLK, encoded as ticks since spacecraft clock start.
    :return: Ephemeris time, seconds past J2000.
    """
    if PyFloat_Check(sclkdp):
        return sct2e_s(sc, sclkdp)
    else:
        return sct2e_v(sc, sclkdp)


def spd() -> float:
    """
    Return the number of seconds in a day.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spd_c.html

    :return: The number of seconds in a day.
    """
    return spd_c()


cpdef tuple[float, float, float] sphcyl_s(
    radius: float, 
    colat: float, 
    slon: float
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.sphcyl`

    Convert from spherical coordinates to cylindrical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/sphcyl_c.html

    :param radius: Distance of point from origin.
    :param colat: Polar angle (co-latitude in radians) of point.
    :param slon: Azimuthal angle (longitude) of point (radians).
    :return:
            Distance of point from z axis,
            angle (radians) of point from XZ plane,
            Height of point above XY plane.
    """
    cdef double r    = 0.0
    cdef double clon = 0.0
    cdef double z    = 0.0
    sphcyl_c(
        radius, 
        colat, 
        slon, 
        &r, 
        &clon,
        &z,
    )
    return r, clon, z


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=2, mode='c'] sphcyl_v(
    const double[::1] radius, 
    const double[::1] colat, 
    const double[::1] slon
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.sphcyl`

    Convert from spherical coordinates to cylindrical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/sphcyl_c.html

    :param radius: Distance of point from origin.
    :param colat: Polar angle (co-latitude in radians) of point.
    :param slon: Azimuthal angle (longitude) of point (radians).
    :return:
            Distance of point from z axis,
            angle (radians) of point from XZ plane,
            Height of point above XY plane.
    """
    cdef const np.double_t[::1] c_radius = np.ascontiguousarray(radius, dtype=np.double)
    cdef Py_ssize_t i, n = c_radius.shape[0]
    cdef const np.double_t[::1] c_colat = np.ascontiguousarray(colat, dtype=np.double)
    cdef const np.double_t[::1] c_slon = np.ascontiguousarray(slon, dtype=np.double)
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_cyl = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_cyl = p_cyl
    # TODO fix strides lookups below
    with nogil:
        for i in range(n):
            sphcyl_c(
                c_radius[i], 
                c_colat[i], 
                c_slon[i], 
                <SpiceDouble *> &c_cyl[i,0], 
                <SpiceDouble *> &c_cyl[i,1],
                <SpiceDouble *> &c_cyl[i,2]
            )
    return p_cyl


def sphcyl(
    radius: float | double[::1], 
    colat: float | double[::1], 
    slon: float | double[::1]
    ) -> tuple[float, float, float] | Vector_N:
    """
    Convert from spherical coordinates to cylindrical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/sphcyl_c.html

    :param radius: Distance of point from origin.
    :param colat: Polar angle (co-latitude in radians) of point.
    :param slon: Azimuthal angle (longitude) of point (radians).
    :return:
            Distance of point from z axis,
            angle (radians) of point from XZ plane,
            Height of point above XY plane.
    """
    if PyFloat_Check(radius):
        return sphcyl_s(radius, colat, slon)
    else:
        return sphcyl_v(radius, colat, slon)


cpdef tuple[float, float, float] sphlat_s(
    r: float, 
    colat: float, 
    slon: float
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.sphlat`

    Convert from spherical coordinates to latitudinal coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/sphlat_c.html

    :param r: Distance of the point from the origin.
    :param colat: Angle of the point from positive z axis (radians).
    :param slon: Angle of the point from the XZ plane (radians).
    :return:
            Distance of a point from the origin,
            Angle of the point from the XZ plane in radians,
            Angle of the point from the XY plane in radians.
    """
    cdef double radius = 0.0
    cdef double lon    = 0.0
    cdef double lat    = 0.0
    sphlat_c(
        r, 
        colat,
        slon,
        &radius, 
        &lon, 
        &lat, 
    )
    return radius, lon, lat


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=2, mode='c'] sphlat_v(
    const double[::1] r, 
    const double[::1] colat, 
    const double[::1] slon
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.sphlat`

    Convert from spherical coordinates to latitudinal coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/sphlat_c.html

    :param r: Distance of the point from the origin.
    :param colat: Angle of the point from positive z axis (radians).
    :param slon: Angle of the point from the XZ plane (radians).
    :return:
            Distance of a point from the origin,
            Angle of the point from the XZ plane in radians,
            Angle of the point from the XY plane in radians.
    """
    cdef const np.double_t[::1] c_r = np.ascontiguousarray(r, dtype=np.double)
    cdef Py_ssize_t i, n = c_r.shape[0]
    cdef const np.double_t[::1] c_colat = np.ascontiguousarray(colat, dtype=np.double)
    cdef const np.double_t[::1] c_slon = np.ascontiguousarray(slon, dtype=np.double)
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_lat = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_lat = p_lat
    # TODO fix strides lookups below
    with nogil:
        for i in range(n):
            sphlat_c(
                c_r[i], 
                c_colat[i], 
                c_slon[i], 
                <SpiceDouble *> &c_lat[i,0], 
                <SpiceDouble *> &c_lat[i,1],
                <SpiceDouble *> &c_lat[i,2]
            )
    return p_lat


def sphlat(
    r: float | double[::1], 
    colat: float | double[::1], 
    slon: float | double[::1]
    ) -> tuple[float, float, float] | Vector_N:
    """
    Convert from spherical coordinates to latitudinal coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/sphlat_c.html

    :param r: Distance of the point from the origin.
    :param colat: Angle of the point from positive z axis (radians).
    :param slon: Angle of the point from the XZ plane (radians).
    :return:
            Distance of a point from the origin,
            Angle of the point from the XZ plane in radians,
            Angle of the point from the XY plane in radians.
    """
    if PyFloat_Check(r):
        return sphlat_s(r, colat, slon)
    else:
        return sphlat_v(r, colat, slon)


cpdef np.ndarray[np.double_t, ndim=1, mode='c'] sphrec_s(
    r: float, 
    colat: float, 
    slon: float
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.sphrec`

    Convert from spherical coordinates to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/sphrec_c.html

    :param r: Distance of a point from the origin.
    :param colat: Angle of the point from the positive Z-axis.
    :param slon: Angle of the point from the XZ plane in radians.
    :return: Rectangular coordinates of the point.
    """
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_rec = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_rec = p_rec
    sphrec_c(
        r, 
        colat, 
        slon, 
        &c_rec[0],
    )
    return p_rec


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=2, mode='c'] sphrec_v(
    const double[::1] r, 
    const double[::1] colat, 
    const double[::1] slon
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.sphrec`

    Convert from spherical coordinates to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/sphrec_c.html

    :param r: Distance of a point from the origin.
    :param colat: Angle of the point from the positive Z-axis.
    :param slon: Angle of the point from the XZ plane in radians.
    :return: Rectangular coordinates of the point.
    """
    cdef const np.double_t[::1] c_r = np.ascontiguousarray(r, dtype=np.double)
    cdef Py_ssize_t i, n = c_r.shape[0]
    cdef const np.double_t[::1] c_colat = np.ascontiguousarray(colat, dtype=np.double)
    cdef const np.double_t[::1] c_slon = np.ascontiguousarray(slon, dtype=np.double)
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_rec = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_rec = p_rec
    # TODO fix strides lookups below
    with nogil:
        for i in range(n):
            sphrec_c(
                c_r[i], 
                c_colat[i], 
                c_slon[i], 
                &c_rec[i, 0]
            )
    return p_rec


def sphrec(
    r: float | double[::1], 
    colat: float | double[::1], 
    slon: float | double[::1]
    ) -> Vector | Vector_N:
    """
    Convert from spherical coordinates to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/sphrec_c.html

    :param r: Distance of a point from the origin.
    :param colat: Angle of the point from the positive Z-axis.
    :param slon: Angle of the point from the XZ plane in radians.
    :return: Rectangular coordinates of the point.
    """
    if PyFloat_Check(r):
        return sphrec_s(r, colat, slon)
    else:
        return sphrec_v(r, colat, slon)


@boundscheck(False)
@wraparound(False)
def spkapo_s(
    int targ,
    double et,
    str ref,
    double[::1] sobs,
    str abcorr
    ) -> tuple[Vector, float]:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.spkapo`

    Return the position of a target body relative to an observer,
    optionally corrected for light time and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkapo_c.html

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
    cdef int c_targ = targ
    cdef double c_et = et
    cdef double c_lt = 0.0
    cdef const double* c_sobs = &sobs[0]
    # convert the strings to pointers once
    cdef const char* c_ref    = ref
    cdef const char* c_abcorr = abcorr
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_ptarg = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_ptarg = p_ptarg
    spkapo_c(
        c_targ,
        c_et,
        c_ref,
        c_sobs,
        c_abcorr,
        &c_ptarg[0],
        &c_lt
    )
    check_for_spice_error()
    return p_ptarg, c_lt


@boundscheck(False)
@wraparound(False)
def spkapo_v(
    int targ,
    double[::1] ets,
    str ref,
    double[::1] sobs,
    str abcorr
    ) -> tuple[Vector_N, Double_N]:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.spkapo`

    Return the position of a target body relative to an observer,
    optionally corrected for light time and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkapo_c.html

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
    cdef int c_targ = targ
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    cdef const np.double_t[::1] c_sobs = np.ascontiguousarray(sobs, dtype=np.double)
    # convert the strings to pointers once
    cdef const char* c_ref    = ref
    cdef const char* c_abcorr = abcorr
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_ptargs = np.empty((n, 3), dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_ptargs = p_ptargs
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_lts = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_lts = p_lts
    # perform the call
    with nogil:
        for i in range(n):
            spkapo_c(
                c_targ,
                c_ets[i],
                c_ref,
                &c_sobs[0],
                c_abcorr,
                &c_ptargs[i, 0],
                &c_lts[i]
            )
    check_for_spice_error()
    return p_ptargs, p_lts


def spkapo(
    targ: int,
    et: float | float[::1],
    ref: str,
    sobs: float[::1],
    abcorr: str
    ) -> tuple[Vector, float] | tuple[Vector_N, Double_N]:
    """
    Return the position of a target body relative to an observer,
    optionally corrected for light time and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkapo_c.html

    :param targ: Target body.
    :param et: Observer epoch in seconds past J2000 TDB..
    :param ref: Inertial reference frame of observer's state.
    :param sobs: State of observer wrt. solar system barycenter.
    :param abcorr: Aberration correction flag.
    :return:
            Position of target in km,
            One way light time between observer and target in seconds.
    """
    if PyFloat_Check(et):
        return spkapo_s(targ, et, ref, sobs, abcorr)
    else:
        return spkapo_v(targ, et, ref, sobs, abcorr)


@boundscheck(False)
@wraparound(False)
def spkcpo_s(
    str target,
    double et,
    str outref,
    str refloc,
    str abcorr,
    double[::1] obspos,
    str obsctr,
    str obsref
    ) -> tuple[State, float]:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.spkcpo`

    Return the state of a specified target relative to an "observer,"
    where the observer has constant position in a specified reference
    frame. The observer's position is provided by the calling program
    rather than by loaded SPK files.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkcpo_c.html

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
    # convert input c arrays
    cdef const double* c_obspos = &obspos[0]
    # initialize output arrays
    cdef double c_et = et
    cdef double c_lt = 0.0
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_state = np.empty(6, dtype=np.double, order='C')
    cdef np.double_t[::1] c_state = p_state
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
        &c_state[0],
        &c_lt
    )
    check_for_spice_error()
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
    str obsref) -> tuple[State_N, Double_N]:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.spkcpo`

    Return the state of a specified target relative to an "observer,"
    where the observer has constant position in a specified reference
    frame. The observer's position is provided by the calling program
    rather than by loaded SPK files.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkcpo_c.html

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
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    cdef const np.double_t[::1] c_obspos = np.ascontiguousarray(obspos, dtype=np.double)
    # convert the strings to pointers once
    cdef const char* c_target   = target
    cdef const char* c_outref   = outref
    cdef const char* c_refloc   = refloc
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsctr   = obsctr
    cdef const char* c_obsref   = obsref
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_states = np.empty((n, 6), dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_states = p_states
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_lts = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_lts = p_lts
    # perform the call
    with nogil:
        for i in range(n):
            spkcpo_c(
                c_target,
                c_ets[i],
                c_outref,
                c_refloc,
                c_abcorr,
                &c_obspos[0],
                c_obsctr,
                c_obsref,
                &c_states[i, 0],
                &c_lts[i]
            )
    check_for_spice_error()
    # return output
    return p_states, p_lts


def spkcpo(
    target: str,
    et: float | float[::1],
    outref: str,
    refloc: str,
    abcorr: str,
    obspos: float[::1],
    obsctr: str,
    obsref: str
    ) -> tuple[State, float] | tuple[State_N, Double_N]:
    """
    Return the state of a specified target relative to an "observer,"
    where the observer has constant position in a specified reference
    frame. The observer's position is provided by the calling program
    rather than by loaded SPK files.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkcpo_c.html

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
    if PyFloat_Check(et):
        return spkcpo_s(target, et, outref, refloc, abcorr, obspos, obsctr, obsref)
    else:
        return spkcpo_v(target, et, outref, refloc, abcorr, obspos, obsctr, obsref)


@boundscheck(False)
@wraparound(False)
def spkcpt_s(
    double[::1] trgpos,
    str trgctr,
    str trgref,
    double et,
    str outref,
    str refloc,
    str abcorr,
    str obsrvr
    ) -> tuple[State, float]:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.spkcpt`

    Return the state, relative to a specified observer, of a target
    having constant position in a specified reference frame. The
    target's position is provided by the calling program rather than by
    loaded SPK files.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkcpt_c.html

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
    cdef double c_et = et
    # convert the strings to pointers once
    cdef const char* c_trgctr   = trgctr
    cdef const char* c_trgref   = trgref
    cdef const char* c_outref   = outref
    cdef const char* c_refloc   = refloc
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsrvr   = obsrvr
    # convert input c arrays
    cdef const double* c_trgpos = &trgpos[0]
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_state = np.empty(6, dtype=np.double, order='C')
    cdef np.double_t[::1] c_state = p_state
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
        &c_state[0],
        &c_lt
    )
    check_for_spice_error()
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
    ) -> tuple[State_N, Double_N]:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.spkcpt`

    Return the state, relative to a specified observer, of a target
    having constant position in a specified reference frame. The
    target's position is provided by the calling program rather than by
    loaded SPK files.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkcpt_c.html

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
    # initialize c variables
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert the strings to pointers once
    cdef const char* c_trgctr   = trgctr
    cdef const char* c_trgref   = trgref
    cdef const char* c_outref   = outref
    cdef const char* c_refloc   = refloc
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsrvr   = obsrvr
    # convert input c arrays
    cdef const double* c_trgpos = &trgpos[0]
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_states = np.empty((n, 6), dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_states = p_states
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_lts = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_lts = p_lts
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
                &c_states[i, 0],
                &c_lts[i]
            )
    check_for_spice_error()
    # return output
    return p_states, p_lts


def spkcpt(
    trgpos: float[::1],
    trgctr: str,
    trgref: str,
    et: float | float[::1],
    outref: str,
    refloc: str,
    abcorr: str,
    obsrvr: str
    ) -> tuple[State, float] | tuple[State_N, Double_N]:
    """
    Return the state, relative to a specified observer, of a target
    having constant position in a specified reference frame. The
    target's position is provided by the calling program rather than by
    loaded SPK files.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkcpt_c.html

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
    if PyFloat_Check(et):
        return spkcpt_s(trgpos, trgctr, trgref, et, outref, refloc, abcorr, obsrvr)
    else:
        return spkcpt_v(trgpos, trgctr, trgref, et, outref, refloc, abcorr, obsrvr)


@boundscheck(False)
@wraparound(False)
def spkcvo_s(
    str target,
    double et,
    str outref,
    str refloc,
    str abcorr,
    double[::1] obssta,
    double obsepc,
    str obsctr,
    str obsref)-> tuple[State, float]:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.spkcvo`

    Return the state of a specified target relative to an "observer,"
    where the observer has constant velocity in a specified reference
    frame.  The observer's state is provided by the calling program
    rather than by loaded SPK files.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkcvo_c.html

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
    # convert input c arrays
    cdef const double* c_obssta = &obssta[0]
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
        c_obssta,
        c_obsepc,
        c_obsctr,
        c_obsref,
        &c_state[0],
        &c_lt
    )
    check_for_spice_error()
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
    double[::1] obssta,
    double obsepc,
    str obsctr,
    str obsref)-> tuple[State_N, Double_N]:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.spkcvo`

    Return the state of a specified target relative to an "observer,"
    where the observer has constant velocity in a specified reference
    frame.  The observer's state is provided by the calling program
    rather than by loaded SPK files.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkcvo_c.html

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
    # initialize c variables
    cdef double c_obsepc = obsepc
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert the strings to pointers once
    cdef const char* c_target   = target
    cdef const char* c_outref   = outref
    cdef const char* c_refloc   = refloc
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsctr   = obsctr
    cdef const char* c_obsref   = obsref
    # convert input c arrays
    cdef const double* c_obssta = &obssta[0]
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_states = np.empty((n, 6), dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_states = p_states
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_lts = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_lts = p_lts
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
                &c_states[i, 0],
                &c_lts[i]
            )
    check_for_spice_error()
    # return output
    return p_states, p_lts


def spkcvo(
    target: str,
    et: float | float[::1],
    outref: str,
    refloc: str,
    abcorr: str,
    obssta: float[::1],
    obsepc: float,
    obsctr: str,
    obsref: str
    )-> tuple[State, float] | tuple[State_N, Double_N]:
    """
    Return the state of a specified target relative to an "observer,"
    where the observer has constant velocity in a specified reference
    frame.  The observer's state is provided by the calling program
    rather than by loaded SPK files.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkcvo_c.html

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
    if PyFloat_Check(et):
        return spkcvo_s(target, et, outref, refloc, abcorr, obssta, obsepc, obsctr, obsref)
    else:
        return spkcvo_v(target, et, outref, refloc, abcorr, obssta, obsepc, obsctr, obsref)


@boundscheck(False)
@wraparound(False)
def spkcvt_s(
    double[::1] trgsta,
    double trgepc,
    str trgctr,
    str trgref,
    double et,
    str outref,
    str refloc,
    str abcorr,
    str obsrvr)-> tuple[State, float]:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.spkcvt`

    Return the state, relative to a specified observer, of a target
    having constant velocity in a specified reference frame. The
    target's state is provided by the calling program rather than by
    loaded SPK files.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkcvt_c.html

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
    cdef double c_trgepc = trgepc
    cdef double c_et = et
    cdef double c_lt = 0.0
    # convert the strings to pointers once
    cdef const char* c_trgctr   = trgctr
    cdef const char* c_trgref   = trgref
    cdef const char* c_outref   = outref
    cdef const char* c_refloc   = refloc
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsrvr   = obsrvr
    # convert input c arrays
    cdef const double* c_trgsta = &trgsta[0]
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_state = np.empty(6, dtype=np.double, order='C')
    cdef np.double_t[::1] c_state = p_state
    # perform the call
    spkcvt_c(
        c_trgsta,
        c_trgepc,
        c_trgctr,
        c_trgref,
        c_et,
        c_outref,
        c_refloc,
        c_abcorr,
        c_obsrvr,
        &c_state[0],
        &c_lt
    )
    check_for_spice_error()
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
    str obsrvr)-> tuple[State_N, Double_N]:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.spkcvt`

    Return the state, relative to a specified observer, of a target
    having constant velocity in a specified reference frame. The
    target's state is provided by the calling program rather than by
    loaded SPK files.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkcvt_c.html

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
    cdef double c_trgepc = trgepc
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert the strings to pointers once
    cdef const char* c_trgctr   = trgctr
    cdef const char* c_trgref   = trgref
    cdef const char* c_outref   = outref
    cdef const char* c_refloc   = refloc
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_obsrvr   = obsrvr
    # convert input c arrays
    cdef const double* c_trgsta = &trgsta[0]
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_states = np.empty((n, 6), dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_states = p_states
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_lts = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_lts = p_lts
    # perform the call
    with nogil:
        for i in range(n):
            spkcvt_c(
                c_trgsta,
                c_trgepc,
                c_trgctr,
                c_trgref,
                c_ets[i],
                c_outref,
                c_refloc,
                c_abcorr,
                c_obsrvr,
                &c_states[i, 0],
                &c_lts[i]
            )
    check_for_spice_error()
    # return output
    return p_states, p_lts


def spkcvt(
    trgsta: float[::1],
    trgepc: float,
    trgctr: str,
    trgref: str,
    et: float | float[::1],
    outref: str,
    refloc: str,
    abcorr: str,
    obsrvr: str
    )-> tuple[State, float] | tuple[State_N, Double_N]:
    """
    Return the state, relative to a specified observer, of a target
    having constant velocity in a specified reference frame. The
    target's state is provided by the calling program rather than by
    loaded SPK files.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkcvt_c.html

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
    if PyFloat_Check(et):
        return spkcvt_s(trgsta, trgepc, trgctr, trgref, et, outref, refloc, abcorr, obsrvr)
    else:
        return spkcvt_v(trgsta, trgepc, trgctr, trgref, et, outref, refloc, abcorr, obsrvr)


@boundscheck(False)
@wraparound(False)
def spkez_s(
    int target,
    double epoch,
    str ref,
    str abcorr,
    int observer
    )-> tuple[State, float]:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.spkez`

    Return the state (position and velocity) of a target body
    relative to an observing body, optionally corrected for light
    time (planetary aberration) and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkez_c.html

    :param target: Target body.
    :param et: Observer epoch in seconds past J2000 TDB.
    :param ref: Reference frame of output state vector.
    :param abcorr: Aberration correction flag.
    :param observer: Observing body.
    :return:
            State of target in km and km/sec,
            One way light time between observer and target in seconds.
    """
    # initialize c variables
    cdef int c_target = target
    cdef double c_epoch = epoch
    cdef int c_observer = observer
    # convert the strings to pointers once
    cdef const char* c_ref    = ref
    cdef const char* c_abcorr = abcorr
    # allocate output variables
    cdef double c_lt = 0.0
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_state = np.empty(6, dtype=np.double, order='C')
    cdef np.double_t[::1] c_state = p_state
    spkez_c(
        c_target,
        c_epoch,
        c_ref,
        c_abcorr,
        c_observer,
        &c_state[0],
        &c_lt
    )
    check_for_spice_error()
    return p_state, c_lt


@boundscheck(False)
@wraparound(False)
def spkez_v(
    int target,
    double[::1] epochs,
    str ref,
    str abcorr,
    int observer)-> tuple[State_N, Double_N]:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.spkez`

    Return the state (position and velocity) of a target body
    relative to an observing body, optionally corrected for light
    time (planetary aberration) and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkez_c.html

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
    cdef const np.double_t[::1] c_epochs = np.ascontiguousarray(epochs, dtype=np.double)
    cdef Py_ssize_t i, n = c_epochs.shape[0]
    # convert the strings to pointers once
    cdef int c_target   = target
    cdef const char* c_ref    = ref
    cdef const char* c_abcorr = abcorr
    cdef int c_observer = observer
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_states = np.empty((n, 6), dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_states = p_states
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_lts = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_lts = p_lts
    # main loop
    with nogil:
        for i in range(n):
            spkez_c(
                c_target,
                c_epochs[i],
                c_ref,
                c_abcorr,
                c_observer,
                &c_states[i, 0],
                &c_lts[i]
            )
    check_for_spice_error()

    return p_states, p_lts


def spkez(
    target: int,
    epoch: float | float[::1],
    ref:      str,
    abcorr:   str,
    observer: int,
    )-> tuple[State, float] | tuple[State_N, Double_N]:
    """
    Return the state (position and velocity) of a target body
    relative to an observing body, optionally corrected for light
    time (planetary aberration) and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkez_c.html

    :param target: Target body.
    :param et: Observer epoch in seconds past J2000 TDB.
    :param ref: Reference frame of output state vector.
    :param abcorr: Aberration correction flag.
    :param observer: Observing body.
    :return:
            State of target in km and km/sec,
            One way light time between observer and target in seconds.
    """
    if PyFloat_Check(epoch):
        return spkez_s(target, epoch, ref, abcorr, observer)
    else:
        return spkez_v(target, epoch, ref, abcorr, observer)


@boundscheck(False)
@wraparound(False)
def spkezp_s(
    int targ,
    double et,
    str ref,
    str abcorr,
    int obs
    ) -> tuple[Vector, float]:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.spkezp`

    Return the position of a target body relative to an observing
    body, optionally corrected for light time (planetary aberration)
    and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkezp_c.html

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
    cdef int c_targ = targ
    cdef double c_et = et
    cdef int c_obs = obs
    cdef double c_lt = 0.0
    # convert the strings to pointers once
    cdef const char* c_ref    = ref
    cdef const char* c_abcorr = abcorr
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_ptarg = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_ptarg = p_ptarg
    spkezp_c(
        c_targ,
        c_et,
        c_ref,
        c_abcorr,
        c_obs,
        &c_ptarg[0],
        &c_lt
    )
    check_for_spice_error()
    return p_ptarg, c_lt


@boundscheck(False)
@wraparound(False)
def spkezp_v(
    int targ,
    double[::1] ets,
    str ref,
    str abcorr,
    int obs
    )-> tuple[Vector_N, Double_N]:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.spkezp`

    Return the position of a target body relative to an observing
    body, optionally corrected for light time (planetary aberration)
    and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkezp_c.html

    :param targ: Target body NAIF ID code.
    :param ets: Observer epochs in seconds past J2000 TDB.
    :param ref: Reference frame of output position vector.
    :param abcorr: Aberration correction flag.
    :param obs: Observing body NAIF ID code.
    :return:
            Position of target in km,
            One way light time between observer and target in seconds.
    """
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert the strings to pointers once
    cdef const char* c_ref    = ref
    cdef const char* c_abcorr = abcorr
    cdef int c_targ = targ
    cdef int c_obs  = obs
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_ptargs = np.empty((n, 3), dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_ptargs = p_ptargs
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_lts = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_lts = p_lts
    # main loop
    with nogil:
        for i in range(n):
            spkezp_c(
                c_targ,
                c_ets[i],
                c_ref,
                c_abcorr,
                c_obs,
                &c_ptargs[i, 0],
                &c_lts[i]
            )
    check_for_spice_error()

    return p_ptargs, p_lts


def spkezp(
    target: int,
    epoch: float | float[::1],
    ref:      str,
    abcorr:   str,
    observer: int,
    )-> tuple[Vector, float] | tuple[Vector_N, Double_N]:
    """
    Return the position of a target body relative to an observing
    body, optionally corrected for light time (planetary aberration)
    and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkezp_c.html

    :param targ: Target body NAIF ID code.
    :param et: Observer epoch in seconds past J2000 TDB.
    :param ref: Reference frame of output position vector.
    :param abcorr: Aberration correction flag.
    :param obs: Observing body NAIF ID code.
    :return:
            Position of target in km,
            One way light time between observer and target in seconds.
    """
    if PyFloat_Check(epoch):
        return spkezp_s(target, epoch, ref, abcorr, observer)
    else:
        return spkezp_v(target, epoch, ref, abcorr, observer)


@boundscheck(False)
@wraparound(False)
def spkezr_s(
    str target,
    double epoch,
    str frame,
    str abcorr,
    str observer
    )-> tuple[State, float]:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.spkezr`

    Return the state (position and velocity) of a target body
    relative to an observing body, optionally corrected for light
    time (planetary aberration) and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkezr_c.html

    :param target: Target body name.
    :param epoch: Observer epoch in seconds past J2000 TDB.
    :param frame: Reference frame of output state vector.
    :param abcorr: Aberration correction flag.
    :param observer: Observing body name.
    :return:
            State of target in km and km/sec,
            One way light time between observer and target in seconds.
    """
    cdef double c_epoch = epoch
    cdef double c_lt = 0.0
    # convert the strings to pointers once
    cdef const char* c_target   = target
    cdef const char* c_frame    = frame
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_observer = observer
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_state = np.empty(6, dtype=np.double, order='C')
    cdef np.double_t[::1] c_state = p_state
    spkezr_c(
        c_target,
        c_epoch,
        c_frame,
        c_abcorr,
        c_observer,
        &c_state[0],
        &c_lt
    )
    check_for_spice_error()
    return p_state, c_lt


@boundscheck(False)
@wraparound(False)
def spkezr_v(
    str target,
    double[::1] epochs,
    str frame,
    str abcorr,
    str observer)-> tuple[State_N, Double_N]:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.spkezr`

    Return the state (position and velocity) of a target body
    relative to an observing body, optionally corrected for light
    time (planetary aberration) and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkezr_c.html

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
    cdef const np.double_t[::1] c_epochs = np.ascontiguousarray(epochs, dtype=np.double)
    cdef Py_ssize_t i, n = c_epochs.shape[0]
    # convert the strings to pointers once
    cdef const char* c_target   = target
    cdef const char* c_frame    = frame
    cdef const char* c_abcorr   = abcorr
    cdef const char* c_observer = observer
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_states = np.empty((n, 6), dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_states = p_states
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_lts = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_lts = p_lts
    # main loop
    with nogil:
        for i in range(n):
            spkezr_c(
                c_target,
                c_epochs[i],
                c_frame,
                c_abcorr,
                c_observer,
                &c_states[i, 0],
                &c_lts[i]
            )
    check_for_spice_error()

    return p_states, p_lts


def spkezr(
    target:   str,
    epoch: float | float[::1],
    frame:    str,
    abcorr:   str,
    observer: str,
    )-> tuple[State, float]:
    """
    Return the state (position and velocity) of a target body
    relative to an observing body, optionally corrected for light
    time (planetary aberration) and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkezr_c.html

    :param target: Target body name.
    :param epoch: Observer epoch in seconds past J2000 TDB.
    :param frame: Reference frame of output state vector.
    :param abcorr: Aberration correction flag.
    :param observer: Observing body name.
    :return:
            State of target in km and km/sec,
            One way light time between observer and target in seconds.
    """
    if PyFloat_Check(epoch):
        return spkezr_s(target, epoch, frame, abcorr, observer)
    else:
        return spkezr_v(target, epoch, frame, abcorr, observer)


@boundscheck(False)
@wraparound(False)
def spkgeo_s(
    int targ,
    double et,
    str ref,
    int obs
    )-> tuple[State, float]:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.spkgeo`

    Compute the geometric state (position and velocity) of a target
    body relative to an observing body.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkgeo_c.html

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
    check_for_spice_error()
    # return output
    return p_state, c_lt


@boundscheck(False)
@wraparound(False)
def spkgeo_v(
    int targ,
    double[::1] ets,
    str ref,
    int obs,
    )-> tuple[State_N, Double_N]:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.spkgeo`

    Compute the geometric state (position and velocity) of a target
    body relative to an observing body.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkgeo_c.html

    :param targ: Target body.
    :param ets: Target epochs.
    :param ref: Target reference frame.
    :param obs: Observing body.
    :return:
        State of target in km and km/sec,
        One way light time between observer and target in seconds.
    """
    # initialize c variables
    cdef int c_targ = targ
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    cdef int c_obs  = obs
    # convert the strings to pointers once
    cdef const char* c_ref   = ref
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_states = np.empty((n, 6), dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_states = p_states
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_lts = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_lts = p_lts
    # perform the call
    with nogil:
        for i in range(n):
            spkgeo_c(
                c_targ,
                c_ets[i],
                c_ref,
                c_obs,
                &c_states[i, 0],
                &c_lts[i]
            )
    check_for_spice_error()
    # return output
    return p_states, p_lts


def spkgeo(
    targ: int,
    et: float | float[::1],
    ref: str,
    obs: int
    )-> tuple[State, float] | tuple[State_N, Double_N]:
    """
    Compute the geometric state (position and velocity) of a target
    body relative to an observing body.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkgeo_c.html

    :param targ: Target body.
    :param et: Target epoch.
    :param ref: Target reference frame.
    :param obs: Observing body.
    :return:
        State of target in km and km/sec,
        One way light time between observer and target in seconds.
    """
    if PyFloat_Check(et):
        return spkgeo_s(targ, et, ref, obs)
    else:
        return spkgeo_v(targ, et, ref, obs)


@boundscheck(False)
@wraparound(False)
def spkgps_s(
    int targ,
    double et,
    str ref,
    int obs
    ) -> tuple[Vector, float]:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.spkgps`

    Compute the geometric position of a target body relative to an
    observing body.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkgps_c.html

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
    cdef const char* c_ref = ref
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_pos = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_pos = p_pos
    # perform the call
    spkgps_c(
        c_targ,
        c_et,
        c_ref,
        c_obs,
        &c_pos[0],
        &c_lt
    )
    check_for_spice_error()
    # return output
    return p_pos, c_lt


@boundscheck(False)
@wraparound(False)
def spkgps_v(
    int targ,
    double[::1] ets,
    str ref,
    int obs,
    ) -> tuple[Vector_N, Double_N]:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.spkgps`

    Compute the geometric position of a target body relative to an
    observing body.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkgps_c.html

    :param targ: Target body.
    :param ets: Target epochs.
    :param ref: Target reference frame.
    :param obs: Observing body.
    :return: Position of target in km, Light time.
    """
    # initialize c variables
    cdef int c_targ = targ
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    cdef int c_obs  = obs
    # convert the strings to pointers once
    cdef const char* c_ref = ref
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_pos = np.empty((n, 3), dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_pos = p_pos
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_lts = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_lts = p_lts
    # perform the call
    with nogil:
        for i in range(n):
            spkgps_c(
                c_targ,
                c_ets[i],
                c_ref,
                c_obs,
                &c_pos[i, 0],
                &c_lts[i]
            )
    check_for_spice_error()
    # return output
    return p_pos, p_lts


def spkgps(
    targ: int,
    et: float | float[::1],
    ref: str,
    obs: int
    ) -> tuple[Vector, float] | tuple[Vector_N, Double_N]:
    """
    Compute the geometric position of a target body relative to an
    observing body.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkgps_c.html

    :param targ: Target body.
    :param et: Target epoch.
    :param ref: Target reference frame.
    :param obs: Observing body.
    :return: Position of target in km, Light time.
    """
    if PyFloat_Check(et):
        return spkgps_s(targ, et, ref, obs)
    else:
        return spkgps_v(targ, et, ref, obs)


@boundscheck(False)
@wraparound(False)
def spkpos_s(
    str target,
    double et,
    str ref,
    str abcorr,
    str obs
    ) -> tuple[Vector, float]:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.spkpos`

    Return the position of a target body relative to an observing
    body, optionally corrected for light time (planetary aberration)
    and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkpos_c.html

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
    cdef double c_et = et
    cdef double c_lt = 0.0
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
        c_et,
        c_ref,
        c_abcorr,
        c_obs,
        &c_ptarg[0],
        &c_lt
    )
    check_for_spice_error()
    return p_ptarg, c_lt


@boundscheck(False)
@wraparound(False)
def spkpos_v(
    str targ,
    double[::1] ets,
    str ref,
    str abcorr,
    str obs
    )-> tuple[Vector_N, Double_N]:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.spkpos`

    Return the position of a target body relative to an observing
    body, optionally corrected for light time (planetary aberration)
    and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkpos_c.html

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
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert the strings to pointers once
    cdef const char* c_targ   = targ
    cdef const char* c_ref    = ref
    cdef const char* c_abcorr = abcorr
    cdef const char* c_obs    = obs
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_ptargs = np.empty((n, 3), dtype=np.double, order='C')
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_lts = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_ptargs = p_ptargs
    cdef np.double_t[::1]   c_lts = p_lts
    # main loop
    with nogil:
        for i in range(n):
            spkpos_c(
                c_targ,
                c_ets[i],
                c_ref,
                c_abcorr,
                c_obs,
                &c_ptargs[i, 0],
                &c_lts[i]
            )
    check_for_spice_error()

    return p_ptargs, p_lts


def spkpos(
    target: str,
    et: float | float[::1],
    ref:    str,
    abcorr: str,
    obs:    str
    ) -> tuple[Vector, float] | tuple[Vector_N, Double_N]:
    """
    Return the position of a target body relative to an observing
    body, optionally corrected for light time (planetary aberration)
    and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkpos_c.html

    :param targ: Target body name.
    :param et: Observer epoch in seconds past J2000 TDB.
    :param ref: Reference frame of output position vector.
    :param abcorr: Aberration correction flag.
    :param obs: Observing body name.
    :return:
            Position of target in km,
            One way light time between observer and target in seconds.
    """
    if PyFloat_Check(et):
        return spkpos_s(target, et, ref, abcorr, obs)
    else:
        return spkpos_v(target, et, ref, abcorr, obs)


@boundscheck(False)
@wraparound(False)
def spkpvn_s(
    int handle,
    double[::1] descr,
    double et
    ) -> tuple[int, State, int]:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.spkpvn`

    For a specified SPK segment and time, return the state (position and
    velocity) of the segment's target body relative to its center of
    motion.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkpvn_c.html

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
    # convert input c arrays
    cdef const double* c_descr = &descr[0]
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_state = np.empty(6, dtype=np.double, order='C')
    cdef np.double_t[::1] c_state = p_state
    # perform the call
    spkpvn_c(
        c_handle,
        c_descr,
        c_et,
        &c_ref,
        &c_state[0],
        &c_center
    )
    check_for_spice_error()
    # return output
    return c_ref, p_state, c_center


@boundscheck(False)
@wraparound(False)
def spkpvn_v(
    int handle,
    double[::1] descr,
    double[::1] ets
    ) -> tuple[Int_N, State_N, Int_N]:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.spkpvn`

    For a specified SPK segment and time, return the state (position and
    velocity) of the segment's target body relative to its center of
    motion.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkpvn_c.html

    :param handle: File handle.
    :param descr: Segment descriptor.
    :param ets: Evaluation epochs.
    :return:
            Segment reference frame ID code,
            Output state vector,
            Center of state.
    """
    # initialize c variables
    cdef np.double_t[::1] c_ets = np.ascontiguousarray(ets)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    cdef int c_handle = handle
    # convert input c arrays
    cdef const double* c_descr = &descr[0]
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_states = np.empty((n, 6), dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_states = p_states
    cdef np.ndarray[np.int32_t, ndim=1, mode='c'] p_refs = np.empty(n, dtype=np.int32, order='C')
    cdef np.int32_t[::1] c_refs = p_refs
    cdef np.ndarray[np.int32_t, ndim=1, mode='c'] p_centers = np.empty(n, dtype=np.int32, order='C')
    cdef np.int32_t[::1] c_centers = p_centers
    # perform the call
    with nogil:
        for i in range(n):
            spkpvn_c(
                c_handle,
                c_descr,
                c_ets[i],
                <SpiceInt *> &c_refs[i],
                &c_states[i, 0],
                <SpiceInt *> &c_centers[i]
            )
    check_for_spice_error()
    # return output
    return p_refs, p_states, p_centers


def spkpvn(
    handle: int,
    descr: float[::1],
    et: float | float[::1]
    ) -> tuple[int, State, int] | tuple[Int_N, State_N, Int_N]:
    """
    For a specified SPK segment and time, return the state (position and
    velocity) of the segment's target body relative to its center of
    motion.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkpvn_c.html

    :param handle: File handle.
    :param descr: Segment descriptor.
    :param et: Evaluation epoch.
    :return:
            Segment reference frame ID code,
            Output state vector,
            Center of state.
    """
    if PyFloat_Check(et):
        return spkpvn_s(handle, descr, et)
    else:
        return spkpvn_v(handle, descr, et)


@boundscheck(False)
@wraparound(False)
def spkssb_s(
    int targ,
    double et,
    str ref,
    ) -> State:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.spkssb`

    Return the state (position and velocity) of a target body
    relative to the solar system barycenter.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkssb_c.html

    :param targ: Target body.
    :param et: Target epoch.
    :param ref: Target reference frame.
    :return: State of target.
    """
    # initialize c variables
    cdef int c_targ = targ
    cdef double c_et = et
    # convert the strings to pointers once
    cdef const char* c_ref = ref
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_state = np.empty(6, dtype=np.double, order='C')
    cdef np.double_t[::1] c_state = p_state
    # perform the call
    spkssb_c(
        c_targ,
        c_et,
        c_ref,
        &c_state[0],
    )
    check_for_spice_error()
    # return output
    return p_state


@boundscheck(False)
@wraparound(False)
def spkssb_v(
    int targ,
    double[::1] ets,
    str ref,
    ) -> State_N:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.spkssb`

    Return the state (position and velocity) of a target body
    relative to the solar system barycenter.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkssb_c.html

    :param targ: Target body.
    :param ets: Target epochs.
    :param ref: Target reference frame.
    :return: States of target.
    """
    # initialize c variables
    cdef int c_targ = targ
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert the strings to pointers once
    cdef const char* c_ref   = ref
    # initialize output arrays
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_states = np.empty((n, 6), dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_states = p_states
    # perform the call
    with nogil:
        for i in range(n):
            spkssb_c(
                c_targ,
                c_ets[i],
                c_ref,
                &c_states[i, 0],
            )
    check_for_spice_error()
    # return output
    return p_states


def spkssb(
    targ: int,
    et: float | float[::1],
    ref: str,
    ) -> State | State_N:
    """
    Return the state (position and velocity) of a target body
    relative to the solar system barycenter.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/spkssb_c.html

    :param targ: Target body.
    :param et: Target epoch.
    :param ref: Target reference frame.
    :return: State of target.
    """
    if PyFloat_Check(et):
        return spkssb_s(targ, et, ref)
    else:
        return spkssb_v(targ, et, ref)


def str2et_s(
    const char* time
    ) -> float:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.str2et`

    Convert a string representing an epoch to a double precision
    value representing the number of TDB seconds past the J2000
    epoch corresponding to the input epoch.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/str2et_c.html

    :param time: A string representing an epoch.
    :return: The equivalent value in seconds past J2000, TDB.
    """
    # initialize c variables
    cdef double c_et = 0.0
    str2et_c(
        time,
        &c_et
    )
    check_for_spice_error()
    return c_et


@boundscheck(False)
@wraparound(False)
def str2et_v(
    np.ndarray times
    ) -> Double_N:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.str2et`

    Convert a string representing an epoch to a double precision
    value representing the number of TDB seconds past the J2000
    epoch corresponding to the input epoch.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/str2et_c.html

    :param times: Strings representing an epoch.
    :return: The equivalent values in seconds past J2000, TDB.
    """
    # initialize c variables
    cdef Py_ssize_t i, n = times.shape[0]
    # initialize output
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_ets = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_ets = p_ets
    cdef const char* c_time
    # coerce unicode to a byte-string array
    if times.dtype.kind == 'U':
        times = np.char.encode(times, 'ascii')
    for i in range(n):
        c_time = times[i]
        str2et_c(
            c_time,
            &c_ets[i]
        )
    check_for_spice_error()

    return p_ets


def str2et(
    time: str | String_N
    ) -> float | Double_N:
    """
    Convert a string representing an epoch to a double precision
    value representing the number of TDB seconds past the J2000
    epoch corresponding to the input epoch.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/str2et_c.html

    :param time: A string representing an epoch.
    :return: The equivalent value in seconds past J2000, TDB.
    """
    if PyUnicode_Check(time):
        return str2et_s(time)
    else:
        return str2et_v(time)


@boundscheck(False)
@wraparound(False)
@cyice_found_exception_thrower
def sincpt_s(
    str method,
    str target,
    double et,
    str fixref,
    str abcorr,
    str obsrvr,
    str dref,
    double[::1] dvec
    ) -> tuple[Vector, float, Vector, bool]:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.sincpt`

    Given an observer and a direction vector defining a ray, compute
    the surface intercept of the ray on a target body at a specified
    epoch, optionally corrected for light time and stellar
    aberration.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/sincpt_c.html

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
    # initialize c variables
    cdef double c_et = et
    # convert strings
    cdef const char* c_method = method
    cdef const char* c_target = target
    cdef const char* c_fixref = fixref
    cdef const char* c_abcorr = abcorr
    cdef const char* c_obsrvr = obsrvr
    cdef const char* c_dref   = dref
    # Allocate output floats and arrays with appropriate shapes.
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_spoint = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_spoint = p_spoint
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_srfvec = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_srfvec = p_srfvec
    cdef double c_trgepc = 0.0
    cdef SpiceBoolean c_found = SPICEFALSE
    # perform the call
    sincpt_c(
        c_method,
        c_target,
        c_et,
        c_fixref,
        c_abcorr,
        c_obsrvr,
        c_dref,
        &dvec[0],
        &c_spoint[0],
        &c_trgepc,
        &c_srfvec[0],
        <SpiceBoolean *> &c_found
    )
    check_for_spice_error()

    return p_spoint, c_trgepc, p_srfvec, PyBool_FromLong(c_found)


@boundscheck(False)
@wraparound(False)
@cyice_found_exception_thrower
def sincpt_v(
    str method,
    str target,
    double[::1] ets,
    str fixref,
    str abcorr,
    str obsrvr,
    str dref,
    double[::1] dvec
    ) -> tuple[Vector_N, Double_N, Vector_N, Found_N]:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.sincpt`

    Given an observer and a direction vector defining a ray, compute
    the surface intercept of the ray on a target body at a specified
    epoch, optionally corrected for light time and stellar
    aberration.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/sincpt_c.html

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
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert strings
    cdef const char* c_method = method
    cdef const char* c_target = target
    cdef const char* c_fixref = fixref
    cdef const char* c_abcorr = abcorr
    cdef const char* c_obsrvr = obsrvr
    cdef const char* c_dref   = dref
    # Allocate output floats and arrays with appropriate shapes.
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_spoint = np.empty((n, 3), dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_spoint = p_spoint
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_srfvec = np.empty((n, 3), dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_srfvec = p_srfvec
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_trgepc = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1]   c_trgepc = p_trgepc
    cdef np.ndarray[np.int32_t, ndim=1, mode='c'] p_found = np.empty(n, dtype=np.int32, order='C')
    cdef np.int32_t[::1] c_found = p_found
    # perform the call
    with nogil:
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
                &c_spoint[i, 0],
                &c_trgepc[i],
                &c_srfvec[i, 0],
                <SpiceBoolean *> &c_found[i]
            )
    check_for_spice_error()

    return p_spoint, p_trgepc, p_srfvec, p_found.astype(np.bool_)


def sincpt(
    method: str,
    target: str,
    et: float | float[::1],
    fixref: str,
    abcorr: str,
    obsrvr: str,
    dref: str,
    dvec: float[::1]
    ) -> tuple[Vector, float, Vector, bool] | tuple[Vector_N, Double_N, Vector_N, Found_N]:
    """
    Given an observer and a direction vector defining a ray, compute
    the surface intercept of the ray on a target body at a specified
    epoch, optionally corrected for light time and stellar
    aberration.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/sincpt_c.html

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
    if PyFloat_Check(et):
        return sincpt_s(method, target, et, fixref, abcorr, obsrvr, dref, dvec)
    else:
        return sincpt_v(method, target, et, fixref, abcorr, obsrvr, dref, dvec)


cpdef np.ndarray[np.double_t, ndim=1, mode='c'] srfrec_s(
    body: int, 
    lon: float, 
    lat: float
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.srfrec`

    Convert planetocentric latitude and longitude of a surface
    point on a specified body to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/srfrec_c.html

    :param body: NAIF integer code of an extended body.
    :param lon: Longitude of point in radians.
    :param lat: Latitude of point in radians.
    :return: Rectangular coordinates of the point, same units as used in radii definition (typically km).
    """
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_rec = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_rec = p_rec
    srfrec_c(
        body, 
        lon, 
        lat, 
        &c_rec[0],
    )
    return p_rec


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=2, mode='c'] srfrec_v(
    int body, 
    const double[::1] lon, 
    const double[::1] lat
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.srfrec`

    Convert planetocentric latitude and longitude of a surface
    point on a specified body to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/srfrec_c.html

    :param body: NAIF integer code of an extended body.
    :param lon: Longitude of point in radians.
    :param lat: Latitude of point in radians.
    :return: Rectangular coordinates of the point, same units as used in radii definition (typically km).
    """
    cdef SpiceInt c_body = body
    cdef const np.double_t[::1] c_lon = np.ascontiguousarray(lon, dtype=np.double)
    cdef Py_ssize_t i, n = c_lon.shape[0]
    cdef const np.double_t[::1] c_lat   = np.ascontiguousarray(lat, dtype=np.double)
    # allocate output array
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_rec = np.empty((n,3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_rec = p_rec
    # TODO fix strides lookups below
    with nogil:
        for i in range(n):
            srfrec_c(
                c_body, 
                c_lon[i], 
                c_lat[i], 
                &c_rec[i, 0]
            )
    return p_rec


def srfrec(
    body: int, 
    lon: float | double[::1], 
    lat: float | double[::1]
    ) -> Vector | Vector_N:
    """
    Convert planetocentric latitude and longitude of a surface
    point on a specified body to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/srfrec_c.html

    :param body: NAIF integer code of an extended body.
    :param longitude: Longitude of point in radians.
    :param latitude: Latitude of point in radians.
    :return: Rectangular coordinates of the point, same units as used in radii definition (typically km).
    :return: Rectangular coordinates of the point.
    """
    if PyFloat_Check(lon):
        return srfrec_s(body, lon, lat)
    else:
        return srfrec_v(body, lon, lat)


@boundscheck(False)
@wraparound(False)
def subpnt_s(
    str method,
    str target,
    double et,
    str fixref,
    str abcorr,
    str obsrvr
    ) -> tuple[Vector, float, Vector]:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.subpnt`

    Compute the rectangular coordinates of the sub-observer point on
    a target body at a specified epoch, optionally corrected for
    light time and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/subpnt_c.html

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
    cdef double c_et = et
    # convert strings
    cdef const char* c_method = method
    cdef const char* c_target = target
    cdef const char* c_fixref = fixref
    cdef const char* c_abcorr = abcorr
    cdef const char* c_obsrvr = obsrvr
    # Allocate output floats and arrays with appropriate shapes.
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_spoint = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_spoint = p_spoint
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_srfvec = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_srfvec = p_srfvec
    cdef double c_trgepc = 0.0
    # perform the call
    subpnt_c(
        c_method,
        c_target,
        c_et,
        c_fixref,
        c_abcorr,
        c_obsrvr,
        &c_spoint[0],
        &c_trgepc,
        &c_srfvec[0]
        )
    check_for_spice_error()

    return p_spoint, c_trgepc, p_srfvec


@boundscheck(False)
@wraparound(False)
def subpnt_v(
    str method,
    str target,
    double[::1] ets,
    str fixref,
    str abcorr,
    str obsrvr
    ) -> tuple[Vector_N, Double_N, Vector_N]:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.subpnt`

    Compute the rectangular coordinates of the sub-observer point on
    a target body at a specified epoch, optionally corrected for
    light time and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/subpnt_c.html

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
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert strings
    cdef const char* c_method = method
    cdef const char* c_target = target
    cdef const char* c_fixref = fixref
    cdef const char* c_abcorr = abcorr
    cdef const char* c_obsrvr = obsrvr
    # Allocate output floats and arrays with appropriate shapes.
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_spoint = np.empty((n, 3), dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_spoint = p_spoint
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_srfvec = np.empty((n, 3), dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_srfvec = p_srfvec
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_trgepc = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_trgepc = p_trgepc
    # perform the call
    with nogil:
        for i in range(n):
            subpnt_c(
                c_method,
                c_target,
                c_ets[i],
                c_fixref,
                c_abcorr,
                c_obsrvr,
                &c_spoint[i, 0],
                &c_trgepc[i],
                &c_srfvec[i, 0]
            )
    check_for_spice_error()

    return p_spoint, p_trgepc, p_srfvec


def subpnt(
    method: str,
    target: str,
    et: float | float[::1],
    fixref: str,
    abcorr: str,
    obsrvr: str
    ) -> tuple[Vector, float, Vector] | tuple[Vector_N, Double_N, Vector_N]:
    """
    Compute the rectangular coordinates of the sub-observer point on
    a target body at a specified epoch, optionally corrected for
    light time and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/subpnt_c.html

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
    if PyFloat_Check(et):
        return subpnt_s(method, target, et, fixref, abcorr, obsrvr)
    else:
        return subpnt_v(method, target, et, fixref, abcorr, obsrvr)


@boundscheck(False)
@wraparound(False)
def subslr_s(
    str method,
    str target,
    double et,
    str fixref,
    str abcorr,
    str obsrvr
    ) -> tuple[Vector, float, Vector]:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.subslr`

    Compute the rectangular coordinates of the sub-solar point on
    a target body at a specified epoch, optionally corrected for
    light time and stellar aberration.

    This routine supersedes subsol_c.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/subslr_c.html

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
    # initialize c variables
    cdef double c_et = et
    # convert strings
    cdef const char* c_method = method
    cdef const char* c_target = target
    cdef const char* c_fixref = fixref
    cdef const char* c_abcorr = abcorr
    cdef const char* c_obsrvr = obsrvr
    # Allocate output floats and arrays with appropriate shapes.
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_spoint = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_spoint = p_spoint
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_srfvec = np.empty(3, dtype=np.double, order='C')
    cdef np.double_t[::1] c_srfvec = p_srfvec
    cdef double c_trgepc = 0.0
    # perform the call
    subslr_c(
        c_method,
        c_target,
        c_et,
        c_fixref,
        c_abcorr,
        c_obsrvr,
        &c_spoint[0],
        &c_trgepc,
        &c_srfvec[0]
        )
    check_for_spice_error()

    return p_spoint, c_trgepc, p_srfvec


@boundscheck(False)
@wraparound(False)
def subslr_v(
    str method,
    str target,
    double[::1] ets,
    str fixref,
    str abcorr,
    str obsrvr
    ) -> tuple[Vector_N, Double_N, Vector_N]:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.subslr`

    Compute the rectangular coordinates of the sub-solar point on
    a target body at a specified epoch, optionally corrected for
    light time and stellar aberration.

    This routine supersedes subsol_c.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/subslr_c.html

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
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert strings
    cdef const char* c_method = method
    cdef const char* c_target = target
    cdef const char* c_fixref = fixref
    cdef const char* c_abcorr = abcorr
    cdef const char* c_obsrvr = obsrvr
    # Allocate output floats and arrays with appropriate shapes.
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_spoint = np.empty((n, 3), dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_spoint = p_spoint
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_srfvec = np.empty((n, 3), dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_srfvec = p_srfvec
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_trgepc = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_trgepc = p_trgepc
    # perform the call
    with nogil:
        for i in range(n):
            subslr_c(
                c_method,
                c_target,
                c_ets[i],
                c_fixref,
                c_abcorr,
                c_obsrvr,
                &c_spoint[i, 0],
                &c_trgepc[i],
                &c_srfvec[i, 0]
            )
    check_for_spice_error()

    return p_spoint, p_trgepc, p_srfvec


def subslr(
    method: str,
    target: str,
    et: float | float[::1],
    fixref: str,
    abcorr: str,
    obsrvr: str
    ) -> tuple[Vector, float, Vector] | tuple[Vector_N, Double_N, Vector_N]:
    """
    Compute the rectangular coordinates of the sub-solar point on
    a target body at a specified epoch, optionally corrected for
    light time and stellar aberration.

    This routine supersedes subsol_c.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/subslr_c.html

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
    if PyFloat_Check(et):
        return subslr_s(method, target, et, fixref, abcorr, obsrvr)
    else:
        return subslr_v(method, target, et, fixref, abcorr, obsrvr)


@boundscheck(False)
@wraparound(False)
def sxform_s(
    str fromstring,
    str tostring,
    double et
    ) -> Matrix_6:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.sxform`

    Return the state transformation matrix from one frame to
    another at a specified epoch.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/sxform_c.html


    :param instring: Name of the frame to transform from.
    :param tostring: Name of the frame to transform to.
    :param et: Epoch of the state transformation matrix.
    :return: A state transformation matrix.
    """
    # initialize c variables
    cdef double c_et = et
    cdef const char* c_fromstring = fromstring
    cdef const char* c_tostring = tostring
    # initialize output
    cdef np.ndarray[np.double_t, ndim=2, mode="c"] p_xform = np.empty((6, 6), dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_xform = p_xform
    sxform_c(
        c_fromstring,
        c_tostring,
        c_et,
        <SpiceDouble (*)[6]> &c_xform[0, 0]
    )
    check_for_spice_error()
    return p_xform


@boundscheck(False)
@wraparound(False)
def sxform_v(
    str fromstring,
    str tostring,
    double[::1] ets
    ) -> Matrix_N_6:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.sxform`

    Return the state transformation matrix from one frame to
    another at a specified epoch.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/sxform_c.html


    :param instring: Name of the frame to transform from.
    :param tostring: Name of the frame to transform to.
    :param et: Epochs of the state transformation matrix.
    :return: A state transformation matrix.
    """
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    cdef const char* c_fromstring = fromstring
    cdef const char* c_tostring = tostring
    # initialize output
    cdef np.ndarray[np.double_t, ndim=3, mode="c"] p_xform = np.empty((n, 6, 6), dtype=np.double, order='C')
    cdef np.double_t[:, :, ::1] c_xform = p_xform
    # pointer to element
    cdef SpiceDouble* base = &c_xform[0, 0, 0]
    with nogil:
        for i in range(n):
            sxform_c(
                c_fromstring,
                c_tostring,
                c_ets[i],
                <SpiceDouble (*)[6]> (base + i*36)
            )
    check_for_spice_error()
    return p_xform


def sxform(
    fromstring: str,
    tostring:   str,
    et: float | float[::1]
    ) -> Matrix_6 | Matrix_N_6:
    """
    Return the state transformation matrix from one frame to
    another at a specified epoch.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/sxform_c.html


    :param instring: Name of the frame to transform from.
    :param tostring: Name of the frame to transform to.
    :param et: Epoch of the state transformation matrix.
    :return: A state transformation matrix.
    """
    if PyFloat_Check(et):
        return sxform_s(fromstring, tostring, et)
    else:
        return sxform_v(fromstring, tostring, et)


# T

@boundscheck(False)
@wraparound(False)
def tangpt_s(
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
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.tangpt`

    Compute, for a given observer, ray emanating from the observer,
    and target, the "tangent point": the point on the ray nearest
    to the target's surface. Also compute the point on the target's
    surface nearest to the tangent point.

    The locations of both points are optionally corrected for light
    time and stellar aberration.

    The surface shape is modeled as a triaxial ellipsoid.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/tangpt_c.html

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
     correction locus, Vector from observer to surface point 'srfpt'.
    """
    # initialize c variables
    cdef double c_et = et
    # convert strings
    cdef const char* c_method = method
    cdef const char* c_target = target
    cdef const char* c_fixref = fixref
    cdef const char* c_abcorr = abcorr
    cdef const char* c_corloc = corloc
    cdef const char* c_obsrvr = obsrvr
    cdef const char* c_dref   = dref
    # Allocate output floats and arrays with appropriate shapes.
    cdef double c_alt    = 0.0
    cdef double c_vrange = 0.0
    cdef double c_trgepc = 0.0
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
        c_et,
        c_fixref,
        c_abcorr,
        c_corloc,
        c_obsrvr,
        c_dref,
        &dvec[0],
        &c_tanpt[0],
        &c_alt,
        &c_vrange,
        &c_srfpt[0],
        &c_trgepc,
        &c_srfvec[0]
    )
    check_for_spice_error()
    # return values
    return p_tanpt, c_alt, c_vrange, p_srfpt, c_trgepc, p_srfvec


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

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/tangpt_c.html

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
     correction locus, Vector from observer to surface point 'srfpt'.
    """
    # allocate sizes
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    # convert strings to ascii
    cdef const char* c_method = method
    cdef const char* c_target = target
    cdef const char* c_fixref = fixref
    cdef const char* c_abcorr = abcorr
    cdef const char* c_corloc = corloc
    cdef const char* c_obsrvr = obsrvr
    cdef const char* c_dref   = dref
    # Allocate output floats and arrays with appropriate shapes.
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_tanpt = np.empty((n, 3), dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_tanpt = p_tanpt
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_alt = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_alt = p_alt
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_vrange = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_vrange = p_vrange
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_srfpt = np.empty((n, 3), dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_srfpt = p_srfpt
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_srfvec = np.empty((n, 3), dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_srfvec = p_srfvec
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_trgepc = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_trgepc = p_trgepc
    # perform the calls
    with nogil:
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
                &c_tanpt[i, 0],
                &c_alt[i],
                &c_vrange[i],
                &c_srfpt[i, 0],
                &c_trgepc[i],
                &c_srfvec[i, 0]
            )
    check_for_spice_error()
    # return values
    return p_tanpt, p_alt, p_vrange, p_srfpt, p_trgepc, p_srfvec


def tangpt(
    method: str,
    target: str,
    et: float | float[::1],
    fixref: str,
    abcorr: str,
    corloc: str,
    obsrvr: str,
    dref: str,
    dvec: float[::1]
    ):
    """
    Compute, for a given observer, ray emanating from the observer,
    and target, the "tangent point": the point on the ray nearest
    to the target's surface. Also compute the point on the target's
    surface nearest to the tangent point.

    The locations of both points are optionally corrected for light
    time and stellar aberration.

    The surface shape is modeled as a triaxial ellipsoid.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/tangpt_c.html

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
     correction locus, Vector from observer to surface point 'srfpt'.
    """
    if PyFloat_Check(et):
        return tangpt_s(method, target, et, fixref, abcorr, corloc, obsrvr, dref, dvec)
    else:
        return tangpt_v(method, target, et, fixref, abcorr, corloc, obsrvr, dref, dvec)


@boundscheck(False)
@wraparound(False)
cpdef tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray] termpt_s(
    const char * method,
    const char * ilusrc,
    const char * target,
    double et,
    const char * fixref,
    const char * abcorr,
    const char * corloc,
    const char * obsrvr,
    double[::1] refvec,
    double rolstp,
    int ncuts,
    double schstp,
    double soltol,
    int maxn
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.termpt`

    Find terminator points on a target body. The caller specifies
    half-planes, bounded by the illumination source center-target center
    vector, in which to search for terminator points.

    The terminator can be either umbral or penumbral. The umbral
    terminator is the boundary of the region on the target surface
    where no light from the source is visible. The penumbral
    terminator is the boundary of the region on the target surface
    where none of the light from the source is blocked by the target
    itself.

    The surface of the target body may be represented either by a
    triaxial ellipsoid or by topographic data.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/termpt_c.html

    :param method: Computation method.
    :param ilusrc: Illumination source.
    :param target: Name of target body.
    :param et: Epoch in ephemeris seconds past J2000 TDB.
    :param fixref: Body-fixed, body-centered target body frame.
    :param abcorr: Aberration correction.
    :param corloc: Aberration correction locus.
    :param obsrvr: Name of observing body.
    :param refvec: Reference vector for cutting half-planes.
    :param rolstp: Roll angular step for cutting half-planes.
    :param ncuts: Number of cutting half-planes.
    :param schstp: Angular step size for searching.
    :param soltol: Solution convergence tolerance.
    :param maxn: Maximum number of entries in output arrays.
    :return: 
        Counts of terminator points corresponding to cuts, 
        Terminator points in km, 
        Times associated with terminator points in seconds, 
        Terminator vectors emanating from the observer in km
    """
    # process inputs
    cdef Py_ssize_t c_maxn = maxn
    cdef const np.double_t[::1] c_refvec = np.ascontiguousarray(refvec, dtype=np.double)
    # allocate outputs
    cdef np.ndarray[np.int32_t, ndim=1, mode='c'] p_npts = np.empty(c_maxn, dtype=np.int32, order='C')
    cdef int[::1] c_npts = p_npts
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_points = np.empty((c_maxn, 3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_points = p_points
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_epochs = np.empty(c_maxn, dtype=np.double, order='C')
    cdef np.double_t[::1] c_epochs = p_epochs
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_trmvcs = np.empty((c_maxn, 3), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_trmvcs = p_trmvcs
    # call the c function
    with nogil:
        termpt_c(
            method,
            ilusrc,
            target,
            et,
            fixref,
            abcorr,
            corloc,
            obsrvr,
            &c_refvec[0],
            rolstp,
            ncuts,
            schstp,
            soltol,
            maxn,
            &c_npts[0],
            <SpiceDouble (*)[3]> &c_points[0, 0],
            &c_epochs[0],
            <SpiceDouble (*)[3]> &c_trmvcs[0, 0]
        )
    check_for_spice_error()
    # return the results
    return p_npts, p_points, p_epochs, p_trmvcs


@boundscheck(False)
@wraparound(False)
cpdef tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray] termpt_v(
    const char * method,
    const char * ilusrc,
    const char * target,
    double[::1] ets,
    const char * fixref,
    const char * abcorr,
    const char * corloc,
    const char * obsrvr,
    double[::1] refvec,
    double rolstp,
    int ncuts,
    double schstp,
    double soltol,
    int maxn
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.termpt`

    Find terminator points on a target body. The caller specifies
    half-planes, bounded by the illumination source center-target center
    vector, in which to search for terminator points.

    The terminator can be either umbral or penumbral. The umbral
    terminator is the boundary of the region on the target surface
    where no light from the source is visible. The penumbral
    terminator is the boundary of the region on the target surface
    where none of the light from the source is blocked by the target
    itself.

    The surface of the target body may be represented either by a
    triaxial ellipsoid or by topographic data.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/termpt_c.html

    :param method: Computation method.
    :param ilusrc: Illumination source.
    :param target: Name of target body.
    :param et: Epoch in ephemeris seconds past J2000 TDB.
    :param fixref: Body-fixed, body-centered target body frame.
    :param abcorr: Aberration correction.
    :param corloc: Aberration correction locus.
    :param obsrvr: Name of observing body.
    :param refvec: Reference vector for cutting half-planes.
    :param rolstp: Roll angular step for cutting half-planes.
    :param ncuts: Number of cutting half-planes.
    :param schstp: Angular step size for searching.
    :param soltol: Solution convergence tolerance.
    :param maxn: Maximum number of entries in output arrays.
    :return: 
        Counts of terminator points corresponding to cuts, 
        Terminator points in km, 
        Times associated with terminator points in seconds, 
        Terminator vectors emanating from the observer in km
    """
    # process inputs
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    cdef Py_ssize_t c_maxn = maxn
    cdef const np.double_t[::1] c_refvec = np.ascontiguousarray(refvec, dtype=np.double)
    cdef const SpiceDouble* c_refvec_ptr = &c_refvec[0]
    # allocate outputs
    cdef np.ndarray[np.int32_t, ndim=2, mode='c'] p_npts = np.empty((n, c_maxn), dtype=np.int32, order='C')
    cdef int[:,::1] c_npts = p_npts
    cdef np.ndarray[np.double_t, ndim=3, mode='c'] p_points = np.empty((n, c_maxn, 3), dtype=np.double, order='C')
    cdef np.double_t[:,:,::1] c_points = p_points
    cdef np.ndarray[np.double_t, ndim=2, mode='c'] p_epochs = np.empty((n, c_maxn), dtype=np.double, order='C')
    cdef np.double_t[:,::1] c_epochs = p_epochs
    cdef np.ndarray[np.double_t, ndim=3, mode='c'] p_trmvcs = np.empty((n, c_maxn, 3), dtype=np.double, order='C')
    cdef np.double_t[:,:,::1] c_trmvcs = p_trmvcs
    # call the c function
    with nogil:
        for i in range(n):
            termpt_c(
                method,
                ilusrc,
                target,
                c_ets[i],
                fixref,
                abcorr,
                corloc,
                obsrvr,
                c_refvec_ptr,
                rolstp,
                ncuts,
                schstp,
                soltol,
                maxn,
                &c_npts[i, 0],
                <SpiceDouble (*)[3]> &c_points[i, 0, 0],
                &c_epochs[i, 0],
                <SpiceDouble (*)[3]> &c_trmvcs[i, 0, 0]
            )
    check_for_spice_error()
    # return the results
    return p_npts, p_points, p_epochs, p_trmvcs


def termpt(
    method: str,
    ilusrc: str,
    target: str,
    et: float | double[::1],
    fixref: str,
    abcorr: str,
    corloc: str,
    obsrvr: str,
    refvec: np.ndarray,
    rolstp: float,
    ncuts: int,
    schstp: float,
    soltol: float,
    maxn: int,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Find terminator points on a target body. The caller specifies
    half-planes, bounded by the illumination source center-target center
    vector, in which to search for terminator points.

    The terminator can be either umbral or penumbral. The umbral
    terminator is the boundary of the region on the target surface
    where no light from the source is visible. The penumbral
    terminator is the boundary of the region on the target surface
    where none of the light from the source is blocked by the target
    itself.

    The surface of the target body may be represented either by a
    triaxial ellipsoid or by topographic data.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/termpt_c.html

    :param method: Computation method.
    :param ilusrc: Illumination source.
    :param target: Name of target body.
    :param et: Epoch in ephemeris seconds past J2000 TDB.
    :param fixref: Body-fixed, body-centered target body frame.
    :param abcorr: Aberration correction.
    :param corloc: Aberration correction locus.
    :param obsrvr: Name of observing body.
    :param refvec: Reference vector for cutting half-planes.
    :param rolstp: Roll angular step for cutting half-planes.
    :param ncuts: Number of cutting half-planes.
    :param schstp: Angular step size for searching.
    :param soltol: Solution convergence tolerance.
    :param maxn: Maximum number of entries in output arrays.
    :return: 
        Counts of terminator points corresponding to cuts, 
        Terminator points in km, 
        Times associated with terminator points in seconds, 
        Terminator vectors emanating from the observer in km
    """
    if PyFloat_Check(et):
        return termpt_s(method, ilusrc, target, et, fixref, abcorr, corloc, obsrvr, refvec, rolstp, ncuts, schstp, soltol, maxn)
    else:
        return termpt_v(method, ilusrc, target, et, fixref, abcorr, corloc, obsrvr, refvec, rolstp, ncuts, schstp, soltol, maxn)


def timout_s(
    double et,
    str pictur
    ) -> str:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.timout`

    This vectorized routine converts an input epoch represented in TDB seconds
    past the TDB epoch of J2000 to a character string formatted to
    the specifications of a user's format picture.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/timout_c.html

    :param et: An epoch in seconds past the ephemeris epoch J2000.
    :param pictur: A format specification for the output string.
    :return: A string representation of the input epoch.
    """
    # initialize c variables
    cdef double c_et = et
    cdef const char* c_pictur = pictur
    cdef char[TIMELEN] c_buffer
    timout_c(
        c_et,
        c_pictur,
        TIMELEN,
        &c_buffer[0]
    )
    check_for_spice_error()
    return PyUnicode_DecodeUTF8(c_buffer, strlen(c_buffer), "strict")


@boundscheck(False)
@wraparound(False)
def timout_v(
    double[::1] ets,
    str pictur
    ) -> String_N:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.timout`

    This routine converts an input epoch represented in TDB seconds
    past the TDB epoch of J2000 to a character string formatted to
    the specifications of a user's format picture.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/timout_c.html

    :param ets: Epochs in seconds past the ephemeris epoch J2000.
    :param pictur: A format specification for the output string.
    :return: A string representation of the input epoch.
    """
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    cdef const char* c_pictur = pictur
    # initialize output arrays
    p_np_s_dtype = np.dtype(('S', TIMELEN))
    p_np_u_dtype = np.dtype(('U', TIMELEN))
    cdef np.ndarray[np.uint8_t, ndim=2, mode='c'] p_outputs = np.zeros((n, TIMELEN), dtype=np.uint8, order='C')
    cdef np.uint8_t[:, ::1] c_outputs = p_outputs
    cdef char* base = <char*> &c_outputs[0, 0]
    with nogil:
        for i in range(n):
            timout_c(
                c_ets[i],
                c_pictur,
                TIMELEN,
                base + i*TIMELEN
            )
    check_for_spice_error()
    # return values
    py_outputs = p_outputs.view(p_np_s_dtype).reshape(n)
    py_outputs = np.char.rstrip(py_outputs).astype(p_np_u_dtype)
    return py_outputs


def timout(
    et: float | float[::1],
    pictur: str
    ) -> str | String_N:
    """
    This vectorized routine converts an input epoch represented in TDB seconds
    past the TDB epoch of J2000 to a character string formatted to
    the specifications of a user's format picture.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/timout_c.html

    :param et: An epoch in seconds past the ephemeris epoch J2000.
    :param pictur: A format specification for the output string.
    :return: A string representation of the input epoch.
    """
    if PyFloat_Check(et):
        return timout_s(et, pictur)
    else:
        return timout_v(et, pictur)


def trgsep_s(
    double et,
    str targ1,
    str shape1,
    str frame1,
    str targ2,
    str shape2,
    str frame2,
    str obsrvr,
    str abcorr
    ) -> float:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.trgsep`

    Compute the angular separation in radians between two spherical
    or point objects.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/trgsep_c.html

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
    cdef double c_angsep = 0.0
    cdef double c_et = et
    cdef const char* c_targ1   = targ1
    cdef const char* c_shape1  = shape1
    cdef const char* c_frame1  = frame1
    cdef const char* c_targ2   = targ2
    cdef const char* c_shape2  = shape2
    cdef const char* c_frame2  = frame2
    cdef const char* c_obsrvr  = obsrvr
    cdef const char* c_abcorr  = abcorr
    c_angsep = trgsep_c(
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
    check_for_spice_error()
    return c_angsep


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
    ) -> Double_N:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.trgsep`

    Compute the angular separation in radians between two spherical
    or point objects.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/trgsep_c.html

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
    cdef const np.double_t[::1] c_ets = np.ascontiguousarray(ets, dtype=np.double)
    cdef Py_ssize_t i, n = c_ets.shape[0]
    cdef const char* c_targ1   = targ1
    cdef const char* c_shape1  = shape1
    cdef const char* c_frame1  = frame1
    cdef const char* c_targ2   = targ2
    cdef const char* c_shape2  = shape2
    cdef const char* c_frame2  = frame2
    cdef const char* c_obsrvr  = obsrvr
    cdef const char* c_abcorr  = abcorr
    # initialize output
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_angseps = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_angseps = p_angseps
    with nogil:
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
    check_for_spice_error()
    return p_angseps


def trgsep(
    et: float | float[::1],
    targ1:  str,
    shape1: str,
    frame1: str,
    targ2:  str,
    shape2: str,
    frame2: str,
    obsrvr: str,
    abcorr: str
    ) -> float:
    """
    Compute the angular separation in radians between two spherical
    or point objects.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/trgsep_c.html

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
    if PyFloat_Check(et):
        return trgsep_s(et, targ1, shape1, frame1, targ2, shape2, frame2, obsrvr, abcorr)
    else:
        return trgsep_v(et, targ1, shape1, frame1, targ2, shape2, frame2, obsrvr, abcorr)


def twopi() -> float:
    """
    Return twice the value of pi
    (the ratio of the circumference of a circle to its diameter).

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/twopi_c.html

    :return: Twice the value of pi.
    """
    return twopi_c()


def tyear() -> float:
    """
    Return the number of seconds in a tropical year.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/tyear_c.html

    :return: The number of seconds in a tropical year.
    """
    return tyear_c()

# U


def unitim_s(
        double epoch,
        str insys,
        str outsys,
    ) -> float:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.unitim`

    Transform time from one uniform scale to another.  The uniform
    time scales are TAI, TDT, TDB, ET, JED, JDTDB, JDTDT.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/unitim_c.html

    :param epoch: An epoch to be converted.
    :param insys: The time scale associated with the input epoch.
    :param outsys: The time scale associated with the function value.
    :return:
            The float in outsys that is equivalent
            to the epoch on the insys time scale.
    """
    cdef double c_unitim = 0.0
    cdef double c_epoch = epoch
    cdef const char* c_insys = insys
    cdef const char* c_outsys = outsys
    c_unitim = unitim_c(
        c_epoch,
        c_insys,
        c_outsys
    )
    check_for_spice_error()
    return c_unitim


@boundscheck(False)
@wraparound(False)
def unitim_v(
        double[::1] epochs,
        insys: str,
        outsys: str,
    ) -> Double_N:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.unitim`

    Transform time from one uniform scale to another.  The uniform
    time scales are TAI, TDT, TDB, ET, JED, JDTDB, JDTDT.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/unitim_c.html

    :param epochs: Epochs to be converted.
    :param insys: The time scale associated with the input epoch.
    :param outsys: The time scale associated with the function value.
    :return:
            The float in outsys that is equivalent
            to the epoch on the insys time scale.
    """
    cdef const np.double_t[::1] c_epochs = np.ascontiguousarray(epochs, dtype=np.double)
    cdef Py_ssize_t i, n = c_epochs.shape[0]
    cdef const char* c_insys = insys
    cdef const char* c_outsys = outsys
    # initialize output
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_unitims = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_unitims = p_unitims
    # perform the actual call
    with nogil:
        for i in range(n):
            c_unitims[i] = unitim_c(
                c_epochs[i],
                c_insys,
                c_outsys
            )
    check_for_spice_error()
    return p_unitims


def unitim(
        epoch: float | float[::1],
        insys: str,
        outsys: str,
    ) -> float | Double_N:
    """
    Transform time from one uniform scale to another.  The uniform
    time scales are TAI, TDT, TDB, ET, JED, JDTDB, JDTDT.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/unitim_c.html

    :param epoch: An epoch to be converted.
    :param insys: The time scale associated with the input epoch.
    :param outsys: The time scale associated with the function value.
    :return:
            The float in outsys that is equivalent
            to the epoch on the insys time scale.
    """
    if PyFloat_Check(epoch):
        return unitim_s(epoch, insys, outsys)
    else:
        return unitim_v(epoch, insys, outsys)


def unload(str file) -> None:
    """
    Unload a SPICE kernel.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/unload_c.html

    :param filename: The name of a kernel to unload.
    """
    cdef const char* c_file = file
    unload_c(c_file)


def utc2et_s(const char* utcstr)-> float:
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.utc2et`

    Convert an input time from Calendar or Julian Date format, UTC,
    to ephemeris seconds past J2000.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/utc2et_c.html

    :param utcstr: Input time string, UTC.
    :return: Output epoch, ephemeris seconds past J2000.
    """
    cdef double c_et = 0.0
    utc2et_c(
        utcstr,
        &c_et
    )
    check_for_spice_error()
    return c_et


@boundscheck(False)
@wraparound(False)
def utc2et_v(
    np.ndarray utcstr
    ) -> Double_N:
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.utc2et`

    Convert an input time from Calendar or Julian Date format, UTC,
    to ephemeris seconds past J2000.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/utc2et_c.html

    :param utcstr: Input time strings, UTC.
    :return: Output epochs, ephemeris seconds past J2000.
    """
    cdef Py_ssize_t i, n = utcstr.shape[0]
    # initialize output
    cdef np.ndarray[np.double_t, ndim=1, mode='c'] p_ets = np.empty(n, dtype=np.double, order='C')
    cdef np.double_t[::1] c_ets = p_ets
    cdef const char* c_utcstr
    # coerce unicode to a byte-string array
    if utcstr.dtype.kind == 'U':
        utcstr = np.char.encode(utcstr, 'ascii')
    for i in range(n):
        c_utcstr = utcstr[i]
        utc2et_c(
            c_utcstr,
            &c_ets[i]
        )
    check_for_spice_error()
    return p_ets


def utc2et(utcstr: str | String_N)-> float | Double_N:
    """
    Convert an input time from Calendar or Julian Date format, UTC,
    to ephemeris seconds past J2000.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/utc2et_c.html

    :param utcstr: Input time string, UTC.
    :return: Output epoch, ephemeris seconds past J2000.
    """
    if PyUnicode_Check(utcstr):
        return utc2et_s(utcstr)
    else:
        return utc2et_v(utcstr)


#X 


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=1, mode='c'] xfmsta_s(
    const double[::1] istate, 
    const char* icosys,
    const char* ocosys,
    const char* body,
    ):
    """
    Scalar version of :py:meth:`~spiceypy.cyice.cyice.xfmsta`

    Transform a state between coordinate systems.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/xfmsta_c.html

    :param istate: Input state.
    :param icosys: Current (input) coordinate system.
    :param ocosys: Desired (output) coordinate system.
    :param body:
                Name or NAIF ID of body with which coordinates
                are associated (if applicable).
    :return: Converted output state
    """
    # initialize c variables
    cdef const np.double_t[::1] c_istate = np.ascontiguousarray(istate, dtype=np.double)
    if c_istate.shape[0] != 6:
        raise ValueError(f'in xfmsta_s, state vector had shape {c_istate.shape[0]}, not 6 as expected')
    # initialize output
    cdef np.ndarray[np.double_t, ndim=1, mode="c"] p_state = np.empty(6, dtype=np.double, order='C')
    cdef np.double_t[::1] c_state = p_state
    xfmsta_c(
        &c_istate[0],
        icosys,
        ocosys,
        body,
        &c_state[0]    
    )
    check_for_spice_error()
    return p_state


@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[np.double_t, ndim=2, mode='c'] xfmsta_v(
    const double[:,::1] istate, 
    const char* icosys,
    const char* ocosys,
    const char* body,
    ):
    """
    Vectorized version of :py:meth:`~spiceypy.cyice.cyice.xfmsta`

    Transform a state between coordinate systems.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/xfmsta_c.html

    :param istate: Input states.
    :param icosys: Current (input) coordinate system.
    :param ocosys: Desired (output) coordinate system.
    :param body:
                Name or NAIF ID of body with which coordinates
                are associated (if applicable).
    :return: Converted output states
    """
    # initialize c variables
    cdef np.double_t[:, ::1] c_istate = np.ascontiguousarray(istate, dtype=np.double)
    if c_istate.shape[1] != 6:
        raise ValueError(f'in xfmsta_v, state vector had shape {c_istate.shape[1]}, not 6 as expected')
    cdef Py_ssize_t i, n = c_istate.shape[0]
    # initialize output
    cdef np.ndarray[np.double_t, ndim=2, mode="c"] p_states = np.empty((n,6), dtype=np.double, order='C')
    cdef np.double_t[:, ::1] c_states = p_states
    # pointer to element
    with nogil:
        for i in range(n):
            xfmsta_c(
                &c_istate[i, 0],
                icosys,
                ocosys,
                body,
                &c_states[i, 0]
            )
    check_for_spice_error()
    return p_states


def xfmsta(
    istate: State | State_N,
    icosys: str,
    ocosys: str,
    body:   str
    ) -> State | State_N:
    """
    Transform a state between coordinate systems.

    https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/xfmsta_c.html

    :param istate: Input state or states.
    :param icosys: Current (input) coordinate system.
    :param ocosys: Desired (output) coordinate system.
    :param body:
                Name or NAIF ID of body with which coordinates
                are associated (if applicable).
    :return: Converted output state
    """
    cdef Py_ssize_t ndim = istate.ndim
    if ndim == 1:
        return xfmsta_s(istate, icosys, ocosys, body)
    elif ndim == 2:
        return xfmsta_v(istate, icosys, ocosys, body)
    else:
        raise RuntimeError(f'xfmsta provided wrong shape for state: {ndim}')

