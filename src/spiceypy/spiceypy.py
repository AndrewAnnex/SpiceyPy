"""
The MIT License (MIT)

Copyright (c) [2015-2022] [Andrew Annex]

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
import warnings
from contextlib import contextmanager
from datetime import datetime, timezone
import functools
import ctypes
from typing import Callable, Iterator, Iterable, Optional, Tuple, Union, Sequence


import numpy
from numpy import ndarray, str_

from .utils import support_types as stypes
from .utils.libspicehelper import libspice
from .utils.exceptions import *
from . import config

from .utils.callbacks import (
    UDFUNC,
    UDFUNS,
    UDFUNB,
    UDSTEP,
    UDREFN,
    UDREPI,
    UDREPU,
    UDREPF,
    UDBAIL,
    SpiceUDFUNS,
    SpiceUDFUNB,
)

from .utils.support_types import (
    Cell_Char,
    Cell_Bool,
    Cell_Time,
    Cell_Double,
    Cell_Int,
    Ellipse,
    Plane,
    SpiceCell,
    SpiceCellPointer,
    SpiceDLADescr,
    SpiceDSKDescr,
    SpiceEKAttDsc,
    SpiceEKSegSum,
)

# inject exceptions back into stypes for backwards compatibility
# cannot define these in stypes due to circular import
stypes.SpiceyError = SpiceyError
stypes.SpiceyPyError = SpiceyPyError
stypes.NotFoundError = NotFoundError
stypes.SpiceyPyIOError = SpiceyPyIOError
stypes.SpiceyPyMemoryError = SpiceyPyMemoryError
stypes.SpiceyPyTypeError = SpiceyPyTypeError
stypes.SpiceyPyKeyError = SpiceyPyKeyError
stypes.SpiceyPyIndexError = SpiceyPyIndexError
stypes.SpiceyPyRuntimeError = SpiceyPyRuntimeError
stypes.SpiceyPyZeroDivisionError = SpiceyPyZeroDivisionError
stypes.SpiceyPyValueError = SpiceyPyValueError


__author__ = "AndrewAnnex"

################################################################################
OptionalInt = Optional[int]

_default_len_out = 256

_SPICE_EK_MAXQSEL = 100  # Twice the 50 in gcc-linux-64
_SPICE_EK_EKRCEX_ROOM_DEFAULT = 100  # Enough?


def warn_deprecated_args(**kwargs) -> None:  # pragma: no cover
    keys = list(kwargs.keys())
    values = list(kwargs.values())
    if any(values):
        varnames = ", ".join(keys)
        warnings.warn(
            f"Specifying any of: {varnames} will be deprecated as of SpiceyPy 5.0.0",
            DeprecationWarning,
            stacklevel=2,
        )
    pass


def check_for_spice_error(f: Optional[Callable]) -> None:
    """
    Internal decorator function to check spice error system for failed calls

    :param f: function
    :raise stypes.SpiceyError:
    """
    if failed():
        short = getmsg("SHORT", 26)
        explain = getmsg("EXPLAIN", 100).strip()
        long = getmsg("LONG", 1841).strip()
        traceback = qcktrc(200)
        reset()
        raise dynamically_instantiate_spiceyerror(
            short=short, explain=explain, long=long, traceback=traceback
        )


def spice_error_check(f):
    """
    Decorator for spiceypy hooking into spice error system.
    If an error is detected, an output similar to outmsg

    :return:
    """

    @functools.wraps(f)
    def with_errcheck(*args, **kwargs):
        try:
            res = f(*args, **kwargs)
            check_for_spice_error(f)
            return res
        except BaseException:
            raise

    return with_errcheck


def spice_found_exception_thrower(f: Callable) -> Callable:
    """
    Decorator for wrapping functions that use status codes
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        res = f(*args, **kwargs)
        if config.catch_false_founds:
            found = res[-1]
            if isinstance(found, bool) and not found:
                raise NotFoundError(
                    "Spice returns not found for function: {}".format(f.__name__),
                    found=found,
                )
            elif stypes.is_iterable(found) and not all(found):
                raise NotFoundError(
                    "Spice returns not found in a series of calls for function: {}".format(
                        f.__name__
                    ),
                    found=found,
                )
            else:
                actualres = res[0:-1]
                if len(actualres) == 1:
                    return actualres[0]
                else:
                    return actualres
        else:
            return res

    return wrapper


@contextmanager
def no_found_check() -> Iterator[None]:
    """
    Temporarily disables spiceypy default behavior which raises exceptions for
    false found flags for certain spice functions. All spice
    functions executed within the context manager will no longer check the found
    flag return parameter and the found flag will be included in the return for
    the given function.
    For Example bodc2n in spiceypy is normally called like::

        name = spice.bodc2n(399)

    With the possibility that an exception is thrown in the even of a invalid ID::

        name = spice.bodc2n(-999991) # throws a SpiceyError

    With this function however, we can use it as a context manager to do this::

        with spice.no_found_check():
            name, found = spice.bodc2n(-999991) # found is false, no exception raised!

    Within the context any spice functions called that normally check the found
    flags will pass through the check without raising an exception if they are false.

    """
    current_catch_state = config.catch_false_founds
    config.catch_false_founds = False
    yield
    config.catch_false_founds = current_catch_state


@contextmanager
def found_check() -> Iterator[None]:
    """
    Temporarily enables spiceypy default behavior which raises exceptions for
    false found flags for certain spice functions. All spice
    functions executed within the context manager will check the found
    flag return parameter and the found flag will be removed from the return for
    the given function.
    For Example bodc2n in spiceypy is normally called like::

        name = spice.bodc2n(399)

    With the possibility that an exception is thrown in the even of a invalid ID::

        name = spice.bodc2n(-999991) # throws a SpiceyError

    With this function however, we can use it as a context manager to do this::

        with spice.found_check():
            found = spice.bodc2n(-999991) # will raise an exception!

    Within the context any spice functions called that normally check the found
    flags will pass through the check without raising an exception if they are false.

    """
    current_catch_state = config.catch_false_founds
    config.catch_false_founds = True
    yield
    config.catch_false_founds = current_catch_state


def found_check_off() -> None:
    """
    Method that turns off found catching

    """
    config.catch_false_founds = False


def found_check_on() -> None:
    """
    Method that turns on found catching

    """
    config.catch_false_founds = True


def get_found_catch_state() -> bool:
    """
    Returns the current found catch state

    :return:
    """
    return config.catch_false_founds


def cell_double(cell_size: int) -> SpiceCell:
    return stypes.SPICEDOUBLE_CELL(cell_size)


def cell_int(cell_size: int) -> SpiceCell:
    return stypes.SPICEINT_CELL(cell_size)


def cell_char(cell_size: int, length: int) -> SpiceCell:
    return stypes.SPICECHAR_CELL(cell_size, length)


def cell_bool(cell_size: int) -> SpiceCell:
    return stypes.SPICEBOOL_CELL(cell_size)


def cell_time(cell_size) -> SpiceCell:
    return stypes.SPICETIME_CELL(cell_size)


################################################################################
# A


@spice_error_check
def appndc(
    item: Union[str, Iterable[str], ndarray, str_], cell: Union[Cell_Char, SpiceCell]
) -> None:
    """
    Append an item to a character cell.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/appndc_c.html

    :param item: The item to append.
    :param cell: The cell to append to.
    """
    assert isinstance(cell, stypes.SpiceCell)
    if stypes.is_iterable(item):
        for c in item:
            libspice.appndc_c(stypes.string_to_char_p(c), cell)
    else:
        item = stypes.string_to_char_p(item)
        libspice.appndc_c(item, cell)


@spice_error_check
def appndd(
    item: Union[float, Iterable[float]], cell: Union[SpiceCell, Cell_Double]
) -> None:
    """
    Append an item to a double precision cell.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/appndd_c.html

    :param item: The item to append.
    :param cell: The cell to append to.
    """
    assert isinstance(cell, stypes.SpiceCell)
    if hasattr(item, "__iter__"):
        for d in item:
            libspice.appndd_c(ctypes.c_double(d), cell)
    else:
        item = ctypes.c_double(item)
        libspice.appndd_c(item, cell)


@spice_error_check
def appndi(item: Union[Iterable[int], int], cell: Union[SpiceCell, Cell_Int]) -> None:
    """
    Append an item to an integer cell.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/appndi_c.html

    :param item: The item to append.
    :param cell: The cell to append to.
    """
    assert isinstance(cell, stypes.SpiceCell)
    if hasattr(item, "__iter__"):
        for i in item:
            libspice.appndi_c(ctypes.c_int(i), cell)
    else:
        item = ctypes.c_int(item)
        libspice.appndi_c(item, cell)


@spice_error_check
def axisar(axis: Union[ndarray, Iterable[float]], angle: float) -> ndarray:
    """
    Construct a rotation matrix that rotates vectors by a specified
    angle about a specified axis.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/axisar_c.html

    :param axis: Rotation axis.
    :param angle: Rotation angle, in radians.
    :return: Rotation matrix corresponding to axis and angle.
    """
    axis = stypes.to_double_vector(axis)
    angle = ctypes.c_double(angle)
    r = stypes.empty_double_matrix()
    libspice.axisar_c(axis, angle, r)
    return stypes.c_matrix_to_numpy(r)


@spice_error_check
def azlcpo(
    method: str,
    target: str,
    et: float,
    abcorr: str,
    azccw: bool,
    elplsz: bool,
    obspos: ndarray,
    obsctr: str,
    obsref: str,
) -> Tuple[ndarray, float]:
    """
    Return the azimuth/elevation coordinates of a specified target
    relative to an "observer," where the observer has constant
    position in a specified reference frame. The observer's position
    is provided by the calling program rather than by loaded SPK
    files.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/azlcpo_c.html

    :param method: Method to obtain the surface normal vector.
    :param target: Name of target ephemeris object.
    :param et: Observation epoch.
    :param abcorr: Aberration correction.
    :param azccw: Flag indicating how azimuth is measured.
    :param elplsz: Flag indicating how elevation is measured.
    :param obspos: Observer position relative to center of motion.
    :param obsctr: Center of motion of observer.
    :param obsref: Body fixed body centered frame of observer's center.
    :return: State of target with respect to observer, in azimuth/elevation coordinates. and One way light time between target and observer.
    """
    _method = stypes.string_to_char_p(method)
    _target = stypes.string_to_char_p(target)
    _et = ctypes.c_double(et)
    _abcorr = stypes.string_to_char_p(abcorr)
    _azccw = ctypes.c_int(azccw)
    _elplsz = ctypes.c_int(elplsz)
    _obspos = stypes.to_double_vector(obspos)
    _obsctr = stypes.string_to_char_p(obsctr)
    _obsref = stypes.string_to_char_p(obsref)
    _azlsta = stypes.empty_double_vector(6)
    _lt = ctypes.c_double(0)
    libspice.azlcpo_c(
        _method,
        _target,
        _et,
        _abcorr,
        _azccw,
        _elplsz,
        _obspos,
        _obsctr,
        _obsref,
        _azlsta,
        ctypes.byref(_lt),
    )
    return stypes.c_vector_to_python(_azlsta), _lt.value


@spice_error_check
def azlrec(range: float, az: float, el: float, azccw: bool, elplsz: bool) -> ndarray:
    """
    Convert from range, azimuth and elevation of a point to
    rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/azlrec_c.html

    :param range: Distance of the point from the origin.
    :param az: Azimuth in radians.
    :param el: Elevation in radians.
    :param azccw: Flag indicating how azimuth is measured.
    :param elplsz: Flag indicating how elevation is measured.
    :return: Rectangular coordinates of a point.
    """
    _range = ctypes.c_double(range)
    _az = ctypes.c_double(az)
    _el = ctypes.c_double(el)
    _azccw = ctypes.c_int(azccw)
    _elplsz = ctypes.c_int(elplsz)
    _rectan = stypes.empty_double_vector(3)
    libspice.azlrec_c(_range, _az, _el, _azccw, _elplsz, _rectan)
    return stypes.c_vector_to_python(_rectan)


################################################################################
# B


@spice_error_check
def b1900() -> float:
    """
    Return the Julian Date corresponding to Besselian Date 1900.0.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/b1900_c.html

    :return: The Julian Date corresponding to Besselian Date 1900.0.
    """
    return libspice.b1900_c()


@spice_error_check
def b1950() -> float:
    """
    Return the Julian Date corresponding to Besselian Date 1950.0.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/b1950_c.html

    :return: The Julian Date corresponding to Besselian Date 1950.0.
    """
    return libspice.b1950_c()


@spice_error_check
def badkpv(
    caller: str, name: str, comp: str, insize: int, divby: int, intype: str
) -> bool:
    """
    Determine if a kernel pool variable is present and if so
    that it has the correct size and type.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/badkpv_c.html

    :param caller: Name of the routine calling this routine.
    :param name: Name of a kernel pool variable.
    :param comp: Comparison operator.
    :param insize: Expected size of the kernel pool variable.
    :param divby: A divisor of the size of the kernel pool variable.
    :param intype: Expected type of the kernel pool variable
    :return: returns false if the kernel pool variable is OK.
    """
    caller = stypes.string_to_char_p(caller)
    name = stypes.string_to_char_p(name)
    comp = stypes.string_to_char_p(comp)
    insize = ctypes.c_int(insize)
    divby = ctypes.c_int(divby)
    intype = ctypes.c_char(intype.encode(encoding="UTF-8"))
    return bool(libspice.badkpv_c(caller, name, comp, insize, divby, intype))


@spice_error_check
def bltfrm(frmcls: int, out_cell: Optional[SpiceCell] = None) -> SpiceCell:
    """
    Return a SPICE set containing the frame IDs of all built-in frames
    of a specified class.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bltfrm_c.html

    :param frmcls: Frame class.
    :param out_cell: Optional SpiceInt Cell that is returned
    :return: Set of ID codes of frames of the specified class.
    """
    frmcls = ctypes.c_int(frmcls)
    if not out_cell:
        out_cell = stypes.SPICEINT_CELL(1000)
    libspice.bltfrm_c(frmcls, out_cell)
    return out_cell


@spice_error_check
def bodeul(body: int, et: float) -> Tuple[float, float, float, float]:
    """
    Return the Euler angles needed to compute the transformation from
    inertial to body-fixed coordinates for any body in the kernel
    pool.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/FORTRAN/spicelib/bodeul.html

    :param body: NAIF ID code of body.
    :param et: Epoch of transformation in seconds past J2000 TDB.
    :return:
            Right ascension of the (IAU) north pole in radians.
            Declination of the (IAU) north pole of the body in radians.
            Prime meridian rotation angle in radians.
            Angle between the prime meridian and longitude of longest axis in radians.
    """
    body = ctypes.c_int(body)
    et = ctypes.c_double(et)
    ra = ctypes.c_double()
    dec = ctypes.c_double()
    w = ctypes.c_double()
    lam = ctypes.c_double()
    libspice.bodeul_(
        ctypes.byref(body),
        ctypes.byref(et),
        ctypes.byref(ra),
        ctypes.byref(dec),
        ctypes.byref(w),
        ctypes.byref(lam),
    )
    return ra.value, dec.value, w.value, lam.value


@spice_error_check
@spice_found_exception_thrower
def bodc2n(code: int, lenout: int = _default_len_out) -> Tuple[str, bool]:
    """
    Translate the SPICE integer code of a body into a common name
    for that body.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodc2n_c.html

    :param code: Integer ID code to be translated into a name.
    :param lenout: Maximum length of output name.
    :return: A common name for the body identified by code.
    """
    code = ctypes.c_int(code)
    name = stypes.string_to_char_p(" " * lenout)
    lenout = ctypes.c_int(lenout)
    found = ctypes.c_int()
    libspice.bodc2n_c(code, lenout, name, ctypes.byref(found))
    return stypes.to_python_string(name), bool(found.value)


@spice_error_check
def bodc2s(code: int, lenout: int = _default_len_out) -> str:
    """
    Translate a body ID code to either the corresponding name or if no
    name to ID code mapping exists, the string representation of the
    body ID value.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodc2s_c.html

    :param code: Integer ID code to translate to a string.
    :param lenout: Maximum length of output name.
    :return: String corresponding to 'code'.
    """
    code = ctypes.c_int(code)
    name = stypes.string_to_char_p(" " * lenout)
    lenout = ctypes.c_int(lenout)
    libspice.bodc2s_c(code, lenout, name)
    return stypes.to_python_string(name)


@spice_error_check
def boddef(name: str, code: int) -> None:
    """
    Define a body name/ID code pair for later translation via
    :func:`bodn2c` or :func:`bodc2n`.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/boddef_c.html

    :param name: Common name of some body.
    :param code: Integer code for that body.
    """
    name = stypes.string_to_char_p(name)
    code = ctypes.c_int(code)
    libspice.boddef_c(name, code)


@spice_error_check
def bodfnd(body: int, item: str) -> bool:
    """
    Determine whether values exist for some item for any body
    in the kernel pool.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodfnd_c.html

    :param body: ID code of body.
    :param item: Item to find ("RADII", "NUT_AMP_RA", etc.).
    :return: True if the item is in the kernel pool, and is False if it is not.
    """
    body = ctypes.c_int(body)
    item = stypes.string_to_char_p(item)
    return bool(libspice.bodfnd_c(body, item))


@spice_error_check
@spice_found_exception_thrower
def bodn2c(name: str) -> Tuple[int, bool]:
    """
    Translate the name of a body or object to the corresponding SPICE
    integer ID code.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodn2c_c.html

    :param name: Body name to be translated into a SPICE ID code.
    :return: SPICE integer ID code for the named body.
    """
    name = stypes.string_to_char_p(name)
    code = ctypes.c_int(0)
    found = ctypes.c_int(0)
    libspice.bodn2c_c(name, ctypes.byref(code), ctypes.byref(found))
    return code.value, bool(found.value)


@spice_error_check
@spice_found_exception_thrower
def bods2c(name: str) -> Tuple[int, bool]:
    """
    Translate a string containing a body name or ID code to an integer code.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bods2c_c.html

    :param name: String to be translated to an ID code.
    :return: Integer ID code corresponding to name.
    """
    name = stypes.string_to_char_p(name)
    code = ctypes.c_int(0)
    found = ctypes.c_int(0)
    libspice.bods2c_c(name, ctypes.byref(code), ctypes.byref(found))
    return code.value, bool(found.value)


@spice_error_check
def bodvar(body: int, item: str, dim: int) -> ndarray:
    """
    Deprecated: This routine has been superseded by :func:`bodvcd` and
    :func:`bodvrd`. This routine is supported for purposes of backward
    compatibility only.

    Return the values of some item for any body in the kernel pool.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodvar_c.html

    :param body: ID code of body.
    :param item:
                Item for which values are desired,
                ("RADII", "NUT_PREC_ANGLES", etc.)
    :param dim: Number of values returned.
    :return: values
    """
    body = ctypes.c_int(body)
    dim = ctypes.c_int(dim)
    item = stypes.string_to_char_p(item)
    values = stypes.empty_double_vector(dim.value)
    libspice.bodvar_c(body, item, ctypes.byref(dim), values)
    return stypes.c_vector_to_python(values)


@spice_error_check
def bodvcd(bodyid: int, item: str, maxn: int) -> Tuple[int, ndarray]:
    """
    Fetch from the kernel pool the double precision values of an item
    associated with a body, where the body is specified by an integer ID
    code.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodvcd_c.html

    :param bodyid: Body ID code.
    :param item:
                Item for which values are desired,
                ("RADII", "NUT_PREC_ANGLES", etc.)
    :param maxn: Maximum number of values that may be returned.
    :return: dim, values
    """
    bodyid = ctypes.c_int(bodyid)
    item = stypes.string_to_char_p(item)
    dim = ctypes.c_int()
    values = stypes.empty_double_vector(maxn)
    maxn = ctypes.c_int(maxn)
    libspice.bodvcd_c(bodyid, item, maxn, ctypes.byref(dim), values)
    return dim.value, stypes.c_vector_to_python(values)


@spice_error_check
def bodvrd(bodynm: str, item: str, maxn: int) -> Tuple[int, ndarray]:
    """
    Fetch from the kernel pool the double precision values
    of an item associated with a body.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodvrd_c.html

    :param bodynm: Body name.
    :param item:
                Item for which values are desired,
                ("RADII", "NUT_PREC_ANGLES", etc.)
    :param maxn: Maximum number of values that may be returned.
    :return: tuple of (dim, values)
    """
    bodynm = stypes.string_to_char_p(bodynm)
    item = stypes.string_to_char_p(item)
    dim = ctypes.c_int()
    values = stypes.empty_double_vector(maxn)
    maxn = ctypes.c_int(maxn)
    libspice.bodvrd_c(bodynm, item, maxn, ctypes.byref(dim), values)
    return dim.value, stypes.c_vector_to_python(values)


@spice_error_check
def brcktd(number: float, end1: float, end2: float) -> float:
    """
    Bracket a number. That is, given a number and an acceptable
    interval, make sure that the number is contained in the
    interval. (If the number is already in the interval, leave it
    alone. If not, set it to the nearest endpoint of the interval.)

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/brcktd_c.html

    :param number: Number to be bracketed.
    :param end1: One of the bracketing endpoints for number.
    :param end2: The other bracketing endpoint for number.
    :return: value within an interval
    """
    number = ctypes.c_double(number)
    end1 = ctypes.c_double(end1)
    end2 = ctypes.c_double(end2)
    return libspice.brcktd_c(number, end1, end2)


@spice_error_check
def brckti(number: int, end1: int, end2: int) -> int:
    """
    Bracket a number. That is, given a number and an acceptable
    interval, make sure that the number is contained in the
    interval. (If the number is already in the interval, leave it
    alone. If not, set it to the nearest endpoint of the interval.)

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/brckti_c.html

    :param number: Number to be bracketed.
    :param end1: One of the bracketing endpoints for number.
    :param end2: The other bracketing endpoint for number.
    :return: value within an interval
    """
    number = ctypes.c_int(number)
    end1 = ctypes.c_int(end1)
    end2 = ctypes.c_int(end2)
    return libspice.brckti_c(number, end1, end2)


@spice_error_check
def bschoc(
    value: Union[str_, str],
    ndim: int,
    lenvals: int,
    array: Union[ndarray, Iterable[str]],
    order: Union[ndarray, Iterable[int]],
) -> int:
    """
    Do a binary search for a given value within a character string array,
    accompanied by an order vector.  Return the index of the matching array
    entry, or -1 if the key value is not found.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bschoc_c.html

    :param value: Key value to be found in array.
    :param ndim: Dimension of array.
    :param lenvals: String length.
    :param array: Character string array to search.
    :param order: Order vector.
    :return: index
    """
    value = stypes.string_to_char_p(value)
    ndim = ctypes.c_int(ndim)
    lenvals = ctypes.c_int(lenvals)
    array = stypes.list_to_char_array_ptr(array, x_len=lenvals, y_len=ndim)
    order = stypes.to_int_vector(order)
    return libspice.bschoc_c(value, ndim, lenvals, array, order)


@spice_error_check
def bschoi(
    value: int,
    ndim: int,
    array: Union[ndarray, Iterable[int]],
    order: Union[ndarray, Iterable[int]],
) -> int:
    """
    Do a binary search for a given value within an integer array,
    accompanied by an order vector.  Return the index of the
    matching array entry, or -1 if the key value is not found.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bschoi_c.html

    :param value: Key value to be found in array.
    :param ndim: Dimension of array.
    :param array: Integer array to search.
    :param order: Order vector.
    :return: index
    """
    value = ctypes.c_int(value)
    ndim = ctypes.c_int(ndim)
    array = stypes.to_int_vector(array)
    order = stypes.to_int_vector(order)
    return libspice.bschoi_c(value, ndim, array, order)


@spice_error_check
def bsrchc(value: str, ndim: int, lenvals: int, array: Iterable[str]) -> int:
    """
    Do a binary earch for a given value within a character string array.
    Return the index of the first matching array entry, or -1 if the key
    value was not found.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bsrchc_c.html

    :param value: Key value to be found in array.
    :param ndim: Dimension of array.
    :param lenvals: String length.
    :param array: Character string array to search.
    :return: index
    """
    value = stypes.string_to_char_p(value)
    ndim = ctypes.c_int(ndim)
    lenvals = ctypes.c_int(lenvals)
    array = stypes.list_to_char_array_ptr(array, x_len=lenvals, y_len=ndim)
    return libspice.bsrchc_c(value, ndim, lenvals, array)


@spice_error_check
def bsrchd(value: float, ndim: int, array: ndarray) -> int:
    """
    Do a binary search for a key value within a double precision array,
    assumed to be in increasing order. Return the index of the matching
    array entry, or -1 if the key value is not found.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bsrchd_c.html

    :param value: Value to find in array.
    :param ndim: Dimension of array.
    :param array: Array to be searched.
    :return: index
    """
    value = ctypes.c_double(value)
    ndim = ctypes.c_int(ndim)
    array = stypes.to_double_vector(array)
    return libspice.bsrchd_c(value, ndim, array)


@spice_error_check
def bsrchi(value: int, ndim: int, array: ndarray) -> int:
    """
    Do a binary search for a key value within an integer array,
    assumed to be in increasing order. Return the index of the
    matching array entry, or -1 if the key value is not found.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bsrchi_c.html

    :param value: Value to find in array.
    :param ndim: Dimension of array.
    :param array: Array to be searched.
    :return: index
    """
    value = ctypes.c_int(value)
    ndim = ctypes.c_int(ndim)
    array = stypes.to_int_vector(array)
    return libspice.bsrchi_c(value, ndim, array)


################################################################################
# C


@spice_error_check
def card(cell: SpiceCell) -> int:
    """
    Return the cardinality (current number of elements) in a
    cell of any data type.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/card_c.html

    :param cell: Input cell.
    :return: the number of elements in a cell of any data type.
    """
    return libspice.card_c(ctypes.byref(cell))


@spice_error_check
@spice_found_exception_thrower
def ccifrm(
    frclss: int, clssid: int, lenout: int = _default_len_out
) -> Tuple[int, str, int, bool]:
    """
    Return the frame name, frame ID, and center associated with
    a given frame class and class ID.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ccifrm_c.html

    :param frclss: Class of frame.
    :param clssid: Class ID of frame.
    :param lenout: Maximum length of output string.
    :return:
            the frame name,
            frame ID,
            center.
    """
    frclss = ctypes.c_int(frclss)
    clssid = ctypes.c_int(clssid)
    lenout = ctypes.c_int(lenout)
    frcode = ctypes.c_int()
    frname = stypes.string_to_char_p(lenout)
    center = ctypes.c_int()
    found = ctypes.c_int()
    libspice.ccifrm_c(
        frclss,
        clssid,
        lenout,
        ctypes.byref(frcode),
        frname,
        ctypes.byref(center),
        ctypes.byref(found),
    )
    return (
        frcode.value,
        stypes.to_python_string(frname),
        center.value,
        bool(found.value),
    )


@spice_error_check
def cgv2el(
    center: Union[ndarray, Iterable[float]],
    vec1: Union[ndarray, Iterable[float]],
    vec2: Union[ndarray, Iterable[float]],
) -> Ellipse:
    """
    Form a SPICE ellipse from a center vector and two generating vectors.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cgv2el_c.html

    :param center: Center Vector
    :param vec1: Vector 1
    :param vec2: Vector 2
    :return: Ellipse
    """
    center = stypes.to_double_vector(center)
    vec1 = stypes.to_double_vector(vec1)
    vec2 = stypes.to_double_vector(vec2)
    ellipse = stypes.Ellipse()
    libspice.cgv2el_c(center, vec1, vec2, ctypes.byref(ellipse))
    return ellipse


@spice_error_check
def chbder(
    cp: Union[ndarray, Iterable[float]],
    degp: int,
    x2s: Union[ndarray, Iterable[float]],
    x: float,
    nderiv: int,
) -> ndarray:
    """
    Given the coefficients for the Chebyshev expansion of a
    polynomial, this returns the value of the polynomial and its
    first nderiv derivatives evaluated at the input X.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/chbder_c.html

    :param cp: degp+1 Chebyshev polynomial coefficients.
    :param degp: Degree of polynomial.
    :param x2s: Transformation parameters of polynomial.
    :param x: Value for which the polynomial is to be evaluated
    :param nderiv: The number of derivatives to compute
    :return: Array of the derivatives of the polynomial
    """
    cp = stypes.to_double_vector(cp)
    degp = ctypes.c_int(degp)
    x2s = stypes.to_double_vector(x2s)
    x = ctypes.c_double(x)
    partdp = stypes.empty_double_vector(3 * (nderiv + 1))
    dpdxs = stypes.empty_double_vector(nderiv + 1)
    nderiv = ctypes.c_int(nderiv)
    libspice.chbder_c(cp, degp, x2s, x, nderiv, partdp, dpdxs)
    return stypes.c_vector_to_python(dpdxs)


@spice_error_check
def chbigr(degp: int, cp: ndarray, x2s: ndarray, x: float) -> Tuple[float, float]:
    """
    Evaluate an indefinite integral of a Chebyshev expansion at a
    specified point `x' and return the value of the input expansion at
    `x' as well. The constant of integration is selected to make the
    integral zero when `x' equals the abscissa value x2s[0].

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/chbigr_c.html

    :param degp: Degree of input Chebyshev expansion.
    :param cp: Chebyshev coefficients of input expansion.
    :param x2s: Transformation parameters.
    :param x: Abscissa value of evaluation.
    :return: Input expansion evaluated at xIntegral evaluated at x.
    """
    _degp = ctypes.c_int(degp)
    _cp = stypes.to_double_vector(cp)
    _x2s = stypes.to_double_vector(x2s)
    _x = ctypes.c_double(x)
    _p = ctypes.c_double(0)
    _itgrlp = ctypes.c_double(0)
    libspice.chbigr_c(_degp, _cp, _x2s, _x, _p, _itgrlp)
    return _p.value, _itgrlp.value


@spice_error_check
def chbint(cp: ndarray, degp: int, x2s: ndarray, x: float) -> Tuple[float, float]:
    """
    Return the value of a polynomial and its derivative, evaluated at
    the input `x', using the coefficients of the Chebyshev expansion of
    the polynomial.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/chbint_c.html

    :param cp: degp 1 Chebyshev polynomial coefficients.
    :param degp: Degree of polynomial.
    :param x2s: Transformation parameters of polynomial.
    :param x: Value for which the polynomial is to be evaluated.
    :return: Value of the polynomial at xValue of the derivative of the polynomial at X.
    """
    _cp = stypes.to_double_vector(cp)
    _degp = ctypes.c_int(degp)
    _x2s = stypes.to_double_vector(x2s)
    _x = ctypes.c_double(x)
    _p = ctypes.c_double(0)
    _dpdx = ctypes.c_double(0)
    libspice.chbint_c(_cp, _degp, _x2s, _x, _p, _dpdx)
    return _p.value, _dpdx.value


@spice_error_check
def chbval(cp: ndarray, degp: int, x2s: ndarray, x: float) -> float:
    """
    Return the value of a polynomial evaluated at the input `x' using
    the coefficients for the Chebyshev expansion of the polynomial.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/chbval_c.html

    :param cp: degp 1 Chebyshev polynomial coefficients.
    :param degp: Degree of polynomial.
    :param x2s: Transformation parameters of polynomial.
    :param x: Value for which the polynomial is to be evaluated.
    :return: Value of the polynomial at x.
    """
    _cp = stypes.to_double_vector(cp)
    _degp = ctypes.c_int(degp)
    _x2s = stypes.to_double_vector(x2s)
    _x = ctypes.c_double(x)
    _p = ctypes.c_double(0)
    libspice.chbval_c(_cp, _degp, _x2s, _x, _p)
    return _p.value


@spice_error_check
def chkin(module: str) -> None:
    """
    Inform the SPICE error handling mechanism of entry into a routine.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/chkin_c.html

    :param module: The name of the calling routine.
    """
    module = stypes.string_to_char_p(module)
    libspice.chkin_c(module)


@spice_error_check
def chkout(module: str) -> None:
    """
    Inform the SPICE error handling mechanism of exit from a routine.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/chkout_c.html

    :param module: The name of the calling routine.
    """
    module = stypes.string_to_char_p(module)
    libspice.chkout_c(module)


@spice_error_check
@spice_found_exception_thrower
def cidfrm(cent: int, lenout: int = _default_len_out) -> Tuple[int, str, bool]:
    """
    Retrieve frame ID code and name to associate with a frame center.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cidfrm_c.html

    :param cent: An object to associate a frame with.
    :param lenout: Available space in output string frname.
    :return:
            frame ID code,
            name to associate with a frame center.
    """
    cent = ctypes.c_int(cent)
    lenout = ctypes.c_int(lenout)
    frcode = ctypes.c_int()
    frname = stypes.string_to_char_p(lenout)
    found = ctypes.c_int()
    libspice.cidfrm_c(cent, lenout, ctypes.byref(frcode), frname, ctypes.byref(found))
    return frcode.value, stypes.to_python_string(frname), bool(found.value)


@spice_error_check
def ckcls(handle: int) -> None:
    """
    Close an open CK file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckcls_c.html

    :param handle: Handle of the CK file to be closed.
    """
    handle = ctypes.c_int(handle)
    libspice.ckcls_c(handle)


@spice_error_check
def ckcov(
    ck: str,
    idcode: int,
    needav: bool,
    level: str,
    tol: float,
    timsys: str,
    cover: Optional[SpiceCell] = None,
) -> SpiceCell:
    """
    Find the coverage window for a specified object in a specified CK file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckcov_c.html

    :param ck: Name of CK file.
    :param idcode: ID code of object.
    :param needav: Flag indicating whether angular velocity is needed.
    :param level: Coverage level: (SEGMENT OR INTERVAL)
    :param tol: Tolerance in ticks.
    :param timsys: Time system used to represent coverage.
    :param cover: Window giving coverage for idcode.
    :return: coverage window for a specified object in a specified CK file
    """
    ck = stypes.string_to_char_p(ck)
    idcode = ctypes.c_int(idcode)
    needav = ctypes.c_int(needav)
    level = stypes.string_to_char_p(level)
    tol = ctypes.c_double(tol)
    timsys = stypes.string_to_char_p(timsys)
    if not cover:
        cover = stypes.SPICEDOUBLE_CELL(20000)
    assert isinstance(cover, stypes.SpiceCell)
    assert cover.dtype == 1
    libspice.ckcov_c(ck, idcode, needav, level, tol, timsys, ctypes.byref(cover))
    return cover


@spice_error_check
@spice_found_exception_thrower
def ckfrot(inst: int, et: float) -> Tuple[ndarray, int, bool]:
    """
    Find the rotation from a C-kernel Id to the native
    frame at the time requested.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckfrot_c.html

    :param inst: NAIF instrument ID
    :param et: Epoch measured in seconds past J2000
    :return: Rotation matrix from the input frame to the returned reference frame, id for the reference frame
    """
    inst = ctypes.c_int(inst)
    et = ctypes.c_double(et)
    rotate_m = stypes.empty_double_matrix(x=3, y=3)
    ref = ctypes.c_int()
    found = ctypes.c_int()
    libspice.ckfrot_c(
        inst,
        et,
        rotate_m,
        ctypes.byref(ref),
        ctypes.byref(found),
    )
    return stypes.c_matrix_to_numpy(rotate_m), ref.value, bool(found.value)


@spice_error_check
@spice_found_exception_thrower
def ckfxfm(inst: int, et: float) -> Tuple[ndarray, int, bool]:
    """
    Find the state transformation matrix from a C-kernel (CK) frame
    with the specified frame class ID (CK ID) to the base frame of
    the highest priority CK segment containing orientation and
    angular velocity data for this CK frame at the time requested.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckfxfm_c.html

    :param inst: Frame class ID CK ID of a CK frame.
    :param et: Epoch measured in seconds past J2000 TDB.
    :return: Transformation from CK frame to frame ref, Frame ID of the base reference.
    """
    _inst = ctypes.c_int(inst)
    _et = ctypes.c_double(et)
    _xform = stypes.empty_double_matrix(6, 6)
    _ref = ctypes.c_int(0)
    _found = ctypes.c_int(0)
    libspice.ckfxfm_c(_inst, _et, _xform, ctypes.byref(_ref), ctypes.byref(_found))
    return (
        stypes.c_matrix_to_numpy(_xform),
        _ref.value,
        bool(_found.value),
    )


@spice_error_check
@spice_found_exception_thrower
def ckgp(
    inst: int, sclkdp: Union[float, int], tol: int, ref: str
) -> Tuple[ndarray, float, bool]:
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
    inst = ctypes.c_int(inst)
    sclkdp = ctypes.c_double(sclkdp)
    tol = ctypes.c_double(tol)
    ref = stypes.string_to_char_p(ref)
    cmat = stypes.empty_double_matrix()
    clkout = ctypes.c_double()
    found = ctypes.c_int()
    libspice.ckgp_c(
        inst, sclkdp, tol, ref, cmat, ctypes.byref(clkout), ctypes.byref(found)
    )
    return stypes.c_matrix_to_numpy(cmat), clkout.value, bool(found.value)


@spice_error_check
@spice_found_exception_thrower
def ckgpav(
    inst: int, sclkdp: Union[float, float], tol: Union[float, int], ref: str
) -> Tuple[ndarray, ndarray, float, bool]:
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
    inst = ctypes.c_int(inst)
    sclkdp = ctypes.c_double(sclkdp)
    tol = ctypes.c_double(tol)
    ref = stypes.string_to_char_p(ref)
    cmat = stypes.empty_double_matrix()
    av = stypes.empty_double_vector(3)
    clkout = ctypes.c_double()
    found = ctypes.c_int()
    libspice.ckgpav_c(
        inst, sclkdp, tol, ref, cmat, av, ctypes.byref(clkout), ctypes.byref(found)
    )
    return (
        stypes.c_matrix_to_numpy(cmat),
        stypes.c_vector_to_python(av),
        clkout.value,
        bool(found.value),
    )


@spice_error_check
def ckgr02(handle: int, descr: ndarray, recno: int) -> ndarray:
    """
    Return a specified pointing instance from a CK type 02 segment.
    The segment is identified by a CK file handle and segment
    descriptor.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckgr02_c.html

    :param handle: The handle of the CK file containing the segment.
    :param descr: The segment descriptor.
    :param recno: The number of the pointing record to be returned.
    :return: The pointing record.
    """
    _handle = ctypes.c_int(handle)
    _descr = stypes.to_double_vector(descr)
    _recno = ctypes.c_int(recno)
    _record = stypes.empty_double_vector(10)
    libspice.ckgr02_c(_handle, _descr, _recno, _record)
    return stypes.c_vector_to_python(_record)


@spice_error_check
def ckgr03(handle: int, descr: ndarray, recno: int) -> ndarray:
    """
    Return a specified pointing instance from a CK type 03 segment.
    The segment is identified by a CK file handle and segment
    descriptor.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckgr03_c.html

    :param handle: The handle of the CK file containing the segment.
    :param descr: The segment descriptor.
    :param recno: The number of the pointing instance to be returned.
    :return: The pointing record.
    """
    _handle = ctypes.c_int(handle)
    _descr = stypes.to_double_vector(descr)
    _recno = ctypes.c_int(recno)
    _record = stypes.empty_double_vector(8)
    libspice.ckgr03_c(_handle, _descr, _recno, _record)
    return stypes.c_vector_to_python(_record)


@spice_error_check
def cklpf(filename: str) -> int:
    """
    Load a CK pointing file for use by the CK readers.  Return that
    file's handle, to be used by other CK routines to refer to the
    file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cklpf_c.html

    :param filename: Name of the CK file to be loaded.
    :return: Loaded file's handle.
    """
    filename = stypes.string_to_char_p(filename)
    handle = ctypes.c_int()
    libspice.cklpf_c(filename, ctypes.byref(handle))
    return handle.value


@spice_error_check
def ckmeta(ckid: int, meta: str) -> int:
    """
    Return (depending upon the user's request) the ID code of either
    the spacecraft or spacecraft clock associated with a C-Kernel ID
    code.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckmeta_c.html

    :param ckid: The ID code for some C kernel object.
    :param meta: The kind of meta data requested SPK or SCLK.
    :return: The requested SCLK or spacecraft ID code.
    """
    _ckid = ctypes.c_int(ckid)
    _meta = stypes.string_to_char_p(meta)
    _idcode = ctypes.c_int(0)
    libspice.ckmeta_c(_ckid, _meta, ctypes.byref(_idcode))
    return _idcode.value


@spice_error_check
def cknr02(handle: int, descr: ndarray) -> int:
    """
    Return the number of pointing records in a CK type 02 segment.
    The segment is identified by a CK file handle and segment
    descriptor.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cknr02_c.html

    :param handle: The handle of the CK file containing the segment.
    :param descr: The descriptor of the type 2 segment.
    :return: The number of records in the segment.
    """
    _handle = ctypes.c_int(handle)
    _descr = stypes.to_double_vector(descr)
    _nrec = ctypes.c_int(0)
    libspice.cknr02_c(_handle, _descr, ctypes.byref(_nrec))
    return _nrec.value


@spice_error_check
def cknr03(handle: int, descr: ndarray) -> int:
    """
    Return the number of pointing instances in a CK type 03 segment.
    The segment is identified by a CK file handle and segment
    descriptor.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cknr03_c.html

    :param handle: The handle of the CK file containing the segment.
    :param descr: The descriptor of the type 3 segment.
    :return: The number of pointing instances in the segment.
    """
    _handle = ctypes.c_int(handle)
    _descr = stypes.to_double_vector(descr)
    _nrec = ctypes.c_int(0)
    libspice.cknr03_c(_handle, _descr, ctypes.byref(_nrec))
    return _nrec.value


@spice_error_check
def ckobj(ck: str, out_cell: Optional[SpiceCell] = None) -> SpiceCell:
    """
    Find the set of ID codes of all objects in a specified CK file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckobj_c.html

    :param ck: Name of CK file.
    :param out_cell: Optional user provided Spice Int cell.
    :return: Set of ID codes of objects in CK file.
    """
    assert isinstance(ck, str)
    ck = stypes.string_to_char_p(ck)
    if not out_cell:
        out_cell = stypes.SPICEINT_CELL(1000)
    assert isinstance(out_cell, stypes.SpiceCell)
    assert out_cell.dtype == 2
    libspice.ckobj_c(ck, ctypes.byref(out_cell))
    return out_cell


@spice_error_check
def ckopn(filename: str, ifname: str, ncomch: int) -> int:
    """
    Open a new CK file, returning the handle of the opened file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckopn_c.html

    :param filename: The name of the CK file to be opened.
    :param ifname: The internal filename for the CK.
    :param ncomch: The number of characters to reserve for comments.
    :return: The handle of the opened CK file.
    """
    filename = stypes.string_to_char_p(filename)
    ifname = stypes.string_to_char_p(ifname)
    ncomch = ctypes.c_int(ncomch)
    handle = ctypes.c_int()
    libspice.ckopn_c(filename, ifname, ncomch, ctypes.byref(handle))
    return handle.value


@spice_error_check
def ckupf(handle: int) -> None:
    """
    Unload a CK pointing file so that it will no longer be searched
    by the readers.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckupf_c.html

    :param handle: Handle of CK file to be unloaded
    """
    handle = ctypes.c_int(handle)
    libspice.ckupf_c(handle)


@spice_error_check
def ckw01(
    handle: int,
    begtim: Union[float, float],
    endtim: Union[float, float],
    inst: int,
    ref: str,
    avflag: bool,
    segid: str,
    nrec: int,
    sclkdp: Union[ndarray, Iterable[float]],
    quats: Union[ndarray, Iterable[Iterable[float]]],
    avvs: Union[ndarray, Iterable[Iterable[float]]],
) -> None:
    """
    Add a type 1 segment to a C-kernel.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckw01_c.html

    :param handle: Handle of an open CK file.
    :param begtim: The beginning encoded SCLK of the segment.
    :param endtim: The ending encoded SCLK of the segment.
    :param inst: The NAIF instrument ID code.
    :param ref: The reference frame of the segment.
    :param avflag: True if the segment will contain angular velocity.
    :param segid: Segment identifier.
    :param nrec: Number of pointing records.
    :param sclkdp: Encoded SCLK times.
    :param quats: Quaternions representing instrument pointing.
    :param avvs: Angular velocity vectors.
    """
    handle = ctypes.c_int(handle)
    begtim = ctypes.c_double(begtim)
    endtim = ctypes.c_double(endtim)
    inst = ctypes.c_int(inst)
    ref = stypes.string_to_char_p(ref)
    avflag = ctypes.c_int(avflag)
    segid = stypes.string_to_char_p(segid)
    sclkdp = stypes.to_double_vector(sclkdp)
    quats = stypes.to_double_matrix(quats)
    avvs = stypes.to_double_matrix(avvs)
    nrec = ctypes.c_int(nrec)
    libspice.ckw01_c(
        handle, begtim, endtim, inst, ref, avflag, segid, nrec, sclkdp, quats, avvs
    )


@spice_error_check
def ckw02(
    handle: int,
    begtim: float,
    endtim: float,
    inst: int,
    ref: str,
    segid: str,
    nrec: int,
    start: ndarray,
    stop: ndarray,
    quats: ndarray,
    avvs: ndarray,
    rates: Union[ndarray, Iterable[float]],
) -> None:
    """
    Write a type 2 segment to a C-kernel.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckw02_c.html

    :param handle: Handle of an open CK file.
    :param begtim: The beginning encoded SCLK of the segment.
    :param endtim: The ending encoded SCLK of the segment.
    :param inst: The NAIF instrument ID code.
    :param ref: The reference frame of the segment.
    :param segid: Segment identifier.
    :param nrec: Number of pointing records.
    :param start: Encoded SCLK interval start times.
    :param stop: Encoded SCLK interval stop times.
    :param quats: Quaternions representing instrument pointing.
    :param avvs: Angular velocity vectors.
    :param rates: Number of seconds per tick for each interval.
    """
    handle = ctypes.c_int(handle)
    begtim = ctypes.c_double(begtim)
    endtim = ctypes.c_double(endtim)
    inst = ctypes.c_int(inst)
    ref = stypes.string_to_char_p(ref)
    segid = stypes.string_to_char_p(segid)
    start = stypes.to_double_vector(start)
    stop = stypes.to_double_vector(stop)
    rates = stypes.to_double_vector(rates)
    quats = stypes.to_double_matrix(quats)
    avvs = stypes.to_double_matrix(avvs)
    nrec = ctypes.c_int(nrec)
    libspice.ckw02_c(
        handle, begtim, endtim, inst, ref, segid, nrec, start, stop, quats, avvs, rates
    )


@spice_error_check
def ckw03(
    handle: int,
    begtim: float,
    endtim: float,
    inst: int,
    ref: str,
    avflag: bool,
    segid: str,
    nrec: int,
    sclkdp: ndarray,
    quats: ndarray,
    avvs: ndarray,
    nints: int,
    starts: Union[ndarray, Iterable[float]],
) -> None:
    """
    Add a type 3 segment to a C-kernel.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckw03_c.html

    :param handle: Handle of an open CK file.
    :param begtim: The beginning encoded SCLK of the segment.
    :param endtim: The ending encoded SCLK of the segment.
    :param inst: The NAIF instrument ID code.
    :param ref: The reference frame of the segment.
    :param avflag: True if the segment will contain angular velocity.
    :param segid: Segment identifier.
    :param nrec: Number of pointing records.
    :param sclkdp: Encoded SCLK times.
    :param quats: Quaternions representing instrument pointing.
    :param avvs: Angular velocity vectors.
    :param nints: Number of intervals.
    :param starts: Encoded SCLK interval start times.
    """
    handle = ctypes.c_int(handle)
    begtim = ctypes.c_double(begtim)
    endtim = ctypes.c_double(endtim)
    inst = ctypes.c_int(inst)
    ref = stypes.string_to_char_p(ref)
    avflag = ctypes.c_int(avflag)
    segid = stypes.string_to_char_p(segid)
    sclkdp = stypes.to_double_vector(sclkdp)
    quats = stypes.to_double_matrix(quats)
    avvs = stypes.to_double_matrix(avvs)
    nrec = ctypes.c_int(nrec)
    starts = stypes.to_double_vector(starts)
    nints = ctypes.c_int(nints)
    libspice.ckw03_c(
        handle,
        begtim,
        endtim,
        inst,
        ref,
        avflag,
        segid,
        nrec,
        sclkdp,
        quats,
        avvs,
        nints,
        starts,
    )


@spice_error_check
def ckw05(
    handle: int,
    subtype: int,
    degree: int,
    begtim: float,
    endtim: float,
    inst: int,
    ref: str,
    avflag: bool,
    segid: str,
    sclkdp: ndarray,
    packts: Sequence[Iterable[float]],
    rate: float,
    nints: int,
    starts: ndarray,
) -> None:
    """
    Write a type 5 segment to a CK file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckw05_c.html

    :param handle: Handle of an open CK file.
    :param subtype: CK type 5 subtype code. Can be: 0, 1, 2, 3 see naif docs via link above.
    :param degree: Degree of interpolating polynomials.
    :param begtim: The beginning encoded SCLK of the segment.
    :param endtim: The ending encoded SCLK of the segment.
    :param inst: The NAIF instrument ID code.
    :param ref: The reference frame of the segment.
    :param avflag: True if the segment will contain angular velocity.
    :param segid: Segment identifier.
    :param sclkdp: Encoded SCLK times.
    :param packts: Array of packets.
    :param rate: Nominal SCLK rate in seconds per tick.
    :param nints: Number of intervals.
    :param starts: Encoded SCLK interval start times.
    """
    handle = ctypes.c_int(handle)
    subtype = ctypes.c_int(subtype)
    degree = ctypes.c_int(degree)
    begtim = ctypes.c_double(begtim)
    endtim = ctypes.c_double(endtim)
    inst = ctypes.c_int(inst)
    ref = stypes.string_to_char_p(ref)
    avflag = ctypes.c_int(avflag)
    segid = stypes.string_to_char_p(segid)
    n = ctypes.c_int(len(packts))
    sclkdp = stypes.to_double_vector(sclkdp)
    packts = stypes.to_double_matrix(packts)
    rate = ctypes.c_double(rate)
    nints = ctypes.c_int(nints)
    starts = stypes.to_double_vector(starts)
    libspice.ckw05_c(
        handle,
        subtype,
        degree,
        begtim,
        endtim,
        inst,
        ref,
        avflag,
        segid,
        n,
        sclkdp,
        packts,
        rate,
        nints,
        starts,
    )


@spice_error_check
def clight() -> float:
    """
    Return the speed of light in a vacuum (IAU official value, in km/sec).

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/clight_c.html

    :return: The function returns the speed of light in vacuum (km/sec).
    """
    return libspice.clight_c()


@spice_error_check
def clpool() -> None:
    """
    Remove all variables from the kernel pool. Watches
    on kernel variables are retained.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/clpool_c.html
    """
    libspice.clpool_c()


@spice_error_check
def cltext(fname: str) -> None:
    """
    Internal undocumented command for closing a text file opened by RDTEXT.

    No URL available; relevant lines from SPICE source:

    FORTRAN SPICE, rdtext.f::

        C$Procedure  CLTEXT ( Close a text file opened by RDTEXT)
              ENTRY  CLTEXT ( FILE )
              CHARACTER*(*)       FILE
        C     VARIABLE  I/O  DESCRIPTION
        C     --------  ---  --------------------------------------------------
        C     FILE       I   Text file to be closed.

    CSPICE, rdtext.c::

        /* $Procedure  CLTEXT ( Close a text file opened by RDTEXT) */
        /* Subroutine */ int cltext_(char *file, ftnlen file_len)


    :param fname: Text file to be closed.
    """
    fname_p = stypes.string_to_char_p(fname)
    fname_len = ctypes.c_int(len(fname))
    libspice.cltext_(fname_p, fname_len)


@spice_error_check
def cmprss(delim: str, n: int, instr: str, lenout: int = _default_len_out) -> str:
    """
    Compress a character string by removing occurrences of
    more than N consecutive occurrences of a specified
    character.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cmprss_c.html

    :param delim: Delimiter to be compressed.
    :param n: Maximum consecutive occurrences of delim.
    :param instr: Input string.
    :param lenout: Optional available space in output string.
    :return: Compressed string.
    """
    delim = ctypes.c_char(delim.encode(encoding="UTF-8"))
    n = ctypes.c_int(n)
    instr = stypes.string_to_char_p(instr)
    output = stypes.string_to_char_p(lenout)
    libspice.cmprss_c(delim, n, instr, lenout, output)
    return stypes.to_python_string(output)


@spice_error_check
@spice_found_exception_thrower
def cnmfrm(cname: str, lenout: int = _default_len_out) -> Tuple[int, str, bool]:
    """
    Retrieve frame ID code and name to associate with an object.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cnmfrm_c.html

    :param cname: Name of the object to find a frame for.
    :param lenout: Maximum length available for frame name.
    :return:
            The ID code of the frame associated with cname,
            The name of the frame with ID frcode.
    """
    lenout = ctypes.c_int(lenout)
    frname = stypes.string_to_char_p(lenout)
    cname = stypes.string_to_char_p(cname)
    found = ctypes.c_int()
    frcode = ctypes.c_int()
    libspice.cnmfrm_c(cname, lenout, ctypes.byref(frcode), frname, ctypes.byref(found))
    return frcode.value, stypes.to_python_string(frname), bool(found.value)


@spice_error_check
def conics(elts: ndarray, et: float) -> ndarray:
    """
    Determine the state (position, velocity) of an orbiting body
    from a set of elliptic, hyperbolic, or parabolic orbital
    elements.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/conics_c.html

    :param elts: Conic elements.
    :param et: Input time.
    :return: State of orbiting body at et.
    """
    elts = stypes.to_double_vector(elts)
    et = ctypes.c_double(et)
    state = stypes.empty_double_vector(6)
    libspice.conics_c(elts, et, state)
    return stypes.c_vector_to_python(state)


@spice_error_check
def convrt(
    x: Union[float, Iterable[float]], inunit: str, outunit: str
) -> Union[ndarray, float]:
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

    inunit = stypes.string_to_char_p(inunit)
    outunit = stypes.string_to_char_p(outunit)
    y = ctypes.c_double()
    if hasattr(x, "__iter__"):
        out_array = []
        for n in x:
            libspice.convrt_c(n, inunit, outunit, ctypes.byref(y))
            check_for_spice_error(None)
            out_array.append(y.value)
        return numpy.array(out_array)
    else:
        x = ctypes.c_double(x)
        libspice.convrt_c(x, inunit, outunit, ctypes.byref(y))
        return y.value


@spice_error_check
def copy(cell: SpiceCell) -> SpiceCell:
    """
    Copy the contents of a SpiceCell of any data type to another
    cell of the same type.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/copy_c.html

    :param cell: Cell to be copied.
    :return: New cell
    """
    assert isinstance(cell, stypes.SpiceCell)
    # Next line was redundant with [raise NotImpImplementedError] below
    # assert cell.dtype == 0 or cell.dtype == 1 or cell.dtype == 2
    if cell.dtype == 0:
        newcopy = stypes.SPICECHAR_CELL(cell.size, cell.length)
    elif cell.dtype == 1:
        newcopy = stypes.SPICEDOUBLE_CELL(cell.size)
    elif cell.dtype == 2:
        newcopy = stypes.SPICEINT_CELL(cell.size)
    else:
        raise NotImplementedError
    libspice.copy_c(ctypes.byref(cell), ctypes.byref(newcopy))
    return newcopy


@spice_error_check
def cpos(string: str, chars: str, start: int) -> int:
    """
    Find the first occurrence in a string of a character belonging
    to a collection of characters, starting at a specified location,
    searching forward.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cpos_c.html

    :param string: Any character string.
    :param chars: A collection of characters.
    :param start: Position to begin looking for one of chars.
    :return:
            The index of the first character of str at or
            following index start that is in the collection chars.
    """
    string = stypes.string_to_char_p(string)
    chars = stypes.string_to_char_p(chars)
    start = ctypes.c_int(start)
    return libspice.cpos_c(string, chars, start)


@spice_error_check
def cposr(string: str, chars: str, start: int) -> int:
    """
    Find the first occurrence in a string of a character belonging
    to a collection of characters, starting at a specified location,
    searching in reverse.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cposr_c.html

    :param string: Any character string.
    :param chars: A collection of characters.
    :param start: Position to begin looking for one of chars.
    :return:
            The index of the last character of str at or
            before index start that is in the collection chars.
    """
    string = stypes.string_to_char_p(string)
    chars = stypes.string_to_char_p(chars)
    start = ctypes.c_int(start)
    return libspice.cposr_c(string, chars, start)


@spice_error_check
def cvpool(agent: str) -> bool:
    """
    Indicate whether or not any watched kernel variables that have a
    specified agent on their notification list have been updated.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cvpool_c.html

    :param agent: Name of the agent to check for notices.
    :return: True if variables for "agent" have been updated.
    """
    agent = stypes.string_to_char_p(agent)
    update = ctypes.c_int()
    libspice.cvpool_c(agent, ctypes.byref(update))
    return bool(update.value)


@spice_error_check
def cyllat(r: float, lonc: float, z: float) -> Tuple[float, float, float]:
    """
    Convert from cylindrical to latitudinal coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cyllat_c.html

    :param r: Distance of point from z axis.
    :param lonc: Cylindrical angle of point from XZ plane(radians).
    :param z: Height of point above XY plane.
    :return: Distance, Longitude (radians), and Latitude of point (radians).
    """
    r = ctypes.c_double(r)
    lonc = ctypes.c_double(lonc)
    z = ctypes.c_double(z)
    radius = ctypes.c_double()
    lon = ctypes.c_double()
    lat = ctypes.c_double()
    libspice.cyllat_c(
        r, lonc, z, ctypes.byref(radius), ctypes.byref(lon), ctypes.byref(lat)
    )
    return radius.value, lon.value, lat.value


@spice_error_check
def cylrec(r: float, lon: float, z: float) -> ndarray:
    """
    Convert from cylindrical to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cylrec_c.html

    :param r: Distance of a point from z axis.
    :param lon: Angle (radians) of a point from xZ plane.
    :param z: Height of a point above xY plane.
    :return: Rectangular coordinates of the point.
    """
    r = ctypes.c_double(r)
    lon = ctypes.c_double(lon)
    z = ctypes.c_double(z)
    rectan = stypes.empty_double_vector(3)
    libspice.cylrec_c(r, lon, z, rectan)
    return stypes.c_vector_to_python(rectan)


@spice_error_check
def cylsph(r: float, lonc: float, z: float) -> Tuple[float, float, float]:
    """
    Convert from cylindrical to spherical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cylsph_c.html

    :param r: Rectangular coordinates of the point.
    :param lonc: Angle (radians) of point from XZ plane.
    :param z: Height of point above XY plane.
    :return:
            Distance of point from origin,
            Polar angle (co-latitude in radians) of point,
            Azimuthal angle (longitude) of point (radians).
    """
    r = ctypes.c_double(r)
    lonc = ctypes.c_double(lonc)
    z = ctypes.c_double(z)
    radius = ctypes.c_double()
    colat = ctypes.c_double()
    lon = ctypes.c_double()
    libspice.cyllat_c(
        r, lonc, z, ctypes.byref(radius), ctypes.byref(colat), ctypes.byref(lon)
    )
    return radius.value, colat.value, lon.value


################################################################################
# D


@spice_error_check
def dafac(handle: int, buffer: Sequence[str]) -> None:
    """
    Add comments from a buffer of character strings to the comment
    area of a binary DAF file, appending them to any comments which
    are already present in the file's comment area.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafac_c.html

    :param handle: handle of a DAF opened with write access.
    :param buffer: Buffer of comments to put into the comment area.
    """
    handle = ctypes.c_int(handle)
    lenvals = ctypes.c_int(len(max(buffer, key=len)) + 1)
    n = ctypes.c_int(len(buffer))
    buffer = stypes.list_to_char_array_ptr(buffer)
    libspice.dafac_c(handle, n, lenvals, buffer)


@spice_error_check
def dafbbs(handle: int) -> None:
    """
    Begin a backward search for arrays in a DAF.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafbbs_c.html

    :param handle: Handle of DAF to be searched.
    """
    handle = ctypes.c_int(handle)
    libspice.dafbbs_c(handle)


@spice_error_check
def dafbfs(handle: int) -> None:
    """
    Begin a forward search for arrays in a DAF.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafbfs_c.html

    :param handle: Handle of file to be searched.
    """
    handle = ctypes.c_int(handle)
    libspice.dafbfs_c(handle)


@spice_error_check
def dafcls(handle: int) -> None:
    """
    Close the DAF associated with a given handle.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafcls_c.html

    :param handle: Handle of DAF to be closed.
    """
    handle = ctypes.c_int(handle)
    libspice.dafcls_c(handle)


@spice_error_check
def dafcs(handle: int) -> None:
    """
    Select a DAF that already has a search in progress as the
    one to continue searching.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafcs_c.html

    :param handle: Handle of DAF to continue searching.
    """
    handle = ctypes.c_int(handle)
    libspice.dafcs_c(handle)


@spice_error_check
def dafdc(handle: int) -> None:
    """
    Delete the entire comment area of a specified DAF file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafdc_c.html

    :param handle: The handle of a binary DAF opened for writing.
    """
    handle = ctypes.c_int(handle)
    libspice.dafdc_c(handle)


@spice_error_check
def dafec(
    handle: int, bufsiz: int, lenout: int = _default_len_out
) -> Tuple[int, Iterable[str], bool]:
    """
    Extract comments from the comment area of a binary DAF.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafec_c.html

    :param handle: Handle of binary DAF opened with read access.
    :param bufsiz: Maximum size, in lines, of buffer.
    :param lenout: Length of strings in output buffer.
    :return:
            Number of extracted comment lines,
            buffer where extracted comment lines are placed,
            Indicates whether all comments have been extracted.
    """
    handle = ctypes.c_int(handle)
    buffer = stypes.empty_char_array(y_len=bufsiz, x_len=lenout)
    bufsiz = ctypes.c_int(bufsiz)
    lenout = ctypes.c_int(lenout)
    n = ctypes.c_int()
    done = ctypes.c_int()
    libspice.dafec_c(
        handle,
        bufsiz,
        lenout,
        ctypes.byref(n),
        ctypes.byref(buffer),
        ctypes.byref(done),
    )
    return n.value, stypes.c_vector_to_python(buffer), bool(done.value)


@spice_error_check
def daffna() -> bool:
    """
    Find the next (forward) array in the current DAF.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/daffna_c.html

    :return: True if an array was found.
    """
    found = ctypes.c_int()
    libspice.daffna_c(ctypes.byref(found))
    return bool(found.value)


@spice_error_check
def daffpa() -> bool:
    """
    Find the previous (backward) array in the current DAF.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/daffpa_c.html

    :return: True if an array was found.
    """
    found = ctypes.c_int()
    libspice.daffpa_c(ctypes.byref(found))
    return bool(found.value)


@spice_error_check
def dafgda(handle: int, begin: int, end: int) -> ndarray:
    """
    Read the double precision data bounded by two addresses within a DAF.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafgda_c.html

    :param handle: Handle of a DAF.
    :param begin: Initial address within file.
    :param end: Final address within file.
    :return: Data contained between begin and end.
    """
    handle = ctypes.c_int(handle)
    data = stypes.empty_double_vector(abs(end - begin) + 1)
    begin = ctypes.c_int(begin)
    end = ctypes.c_int(end)
    libspice.dafgda_c(handle, begin, end, data)
    return stypes.c_vector_to_python(data)


@spice_error_check
def dafgh() -> int:
    """
    Return (get) the handle of the DAF currently being searched.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafgh_c.html

    :return: Handle for current DAF.
    """
    outvalue = ctypes.c_int()
    libspice.dafgh_c(ctypes.byref(outvalue))
    return outvalue.value


@spice_error_check
def dafgn(lenout: int = _default_len_out) -> str:
    """
    Return (get) the name for the current array in the current DAF.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafgn_c.html

    :param lenout: Length of array name string.
    :return: Name of current array.
    """
    lenout = ctypes.c_int(lenout)
    name = stypes.string_to_char_p(lenout)
    libspice.dafgn_c(lenout, name)
    return stypes.to_python_string(name)


@spice_error_check
def dafgs(n: int = 125) -> ndarray:
    """
    Return (get) the summary for the current array in the current DAF.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafgs_c.html

    :param n: Optional length N for result Array, defaults to 125.
    :return: Summary for current array.
    """
    retarray = stypes.empty_double_vector(125)
    libspice.dafgs_c(retarray)
    return stypes.c_vector_to_python(retarray)[0:n]


@spice_error_check
@spice_found_exception_thrower
def dafgsr(handle: int, recno: int, begin: int, end: int) -> Tuple[ndarray, bool]:
    """
    Read a portion of the contents of (words in) a summary record in a DAF file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafgsr_c.html

    :param handle: Handle of DAF.
    :param recno: Record number; word indices are 1-based, 1 to 128 inclusive.
    :param begin: Index of first word to read from record, will be clamped > 0.
    :param end: Index of last word to read, wll be clamped < 129
    :return: Contents of request sub-record
    """
    handle = ctypes.c_int(handle)
    recno = ctypes.c_int(recno)
    begin = ctypes.c_int(begin)
    end = ctypes.c_int(end)
    # dafgsr_c will retrieve no more than 128 words
    data = stypes.empty_double_vector(1 + min([128, end.value]) - max([begin.value, 1]))
    found = ctypes.c_int()
    libspice.dafgsr_c(handle, recno, begin, end, data, ctypes.byref(found))
    return stypes.c_vector_to_python(data), bool(found.value)


@spice_error_check
def dafhsf(handle: int) -> Tuple[int, int]:
    """
    Return the summary format associated with a handle.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafhsf_c.html

    :param handle: Handle of a DAF file.
    :return: Number of double precision components in summariesNumber of integer components in summaries.
    """
    _handle = ctypes.c_int(handle)
    _nd = ctypes.c_int(0)
    _ni = ctypes.c_int(0)
    libspice.dafhsf_c(_handle, ctypes.byref(_nd), ctypes.byref(_ni))
    return _nd.value, _ni.value


@spice_error_check
def dafopr(fname: str) -> int:
    """
    Open a DAF for subsequent read requests.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafopr_c.html

    :param fname: Name of DAF to be opened.
    :return: Handle assigned to DAF.
    """
    fname = stypes.string_to_char_p(fname)
    handle = ctypes.c_int(0)
    libspice.dafopr_c(fname, ctypes.byref(handle))
    return handle.value


@spice_error_check
def dafopw(fname: str) -> int:
    """
    Open a DAF for subsequent write requests.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafopw_c.html

    :param fname: Name of DAF to be opened.
    :return: Handle assigned to DAF.
    """
    fname = stypes.string_to_char_p(fname)
    handle = ctypes.c_int(0)
    libspice.dafopw_c(fname, ctypes.byref(handle))
    return handle.value


@spice_error_check
def dafps(nd: int, ni: int, dc: ndarray, ic: ndarray) -> ndarray:
    """
    Pack (assemble) an array summary from its double precision and
    integer components.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafps_c.html

    :param nd: Number of double precision components.
    :param ni: Number of integer components.
    :param dc: Double precision components.
    :param ic: Integer components.
    :return: Array summary.
    """
    dc = stypes.to_double_vector(dc)
    ic = stypes.to_int_vector(ic)
    outsum = stypes.empty_double_vector(nd + ni)
    nd = ctypes.c_int(nd)
    ni = ctypes.c_int(ni)
    libspice.dafps_c(nd, ni, dc, ic, outsum)
    return stypes.c_vector_to_python(outsum)


@spice_error_check
def dafrda(handle: int, begin: int, end: int) -> ndarray:
    """
    Read the double precision data bounded by two addresses within a DAF.

    Deprecated: This routine has been superseded by :func:`dafgda` and
    :func:`dafgsr`.  This routine is supported for purposes of backward
    compatibility only.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafrda_c.html

    :param handle: Handle of a DAF.
    :param begin: Initial address within file.
    :param end: Final address within file.
    :return: Data contained between begin and end.
    """
    handle = ctypes.c_int(handle)
    begin = ctypes.c_int(begin)
    end = ctypes.c_int(end)
    data = stypes.empty_double_vector(1 + end.value - begin.value)
    libspice.dafrda_c(handle, begin, end, data)
    return stypes.c_vector_to_python(data)


@spice_error_check
def dafrfr(
    handle: int, lenout: int = _default_len_out
) -> Tuple[int, int, str, int, int, int]:
    """
    Read the contents of the file record of a DAF.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafrfr_c.html


    :param handle: Handle of an open DAF file.
    :param lenout: Available room in the output string
    :return:
            Number of double precision components in summaries,
            Number of integer components in summaries,
            Internal file name, Forward list pointer,
            Backward list pointer, Free address pointer.
    """
    handle = ctypes.c_int(handle)
    lenout = ctypes.c_int(lenout)
    nd = ctypes.c_int()
    ni = ctypes.c_int()
    ifname = stypes.string_to_char_p(lenout)
    fward = ctypes.c_int()
    bward = ctypes.c_int()
    free = ctypes.c_int()
    libspice.dafrfr_c(
        handle,
        lenout,
        ctypes.byref(nd),
        ctypes.byref(ni),
        ifname,
        ctypes.byref(fward),
        ctypes.byref(bward),
        ctypes.byref(free),
    )
    return (
        nd.value,
        ni.value,
        stypes.to_python_string(ifname),
        fward.value,
        bward.value,
        free.value,
    )


@spice_error_check
def dafrs(insum: ndarray) -> None:
    """
    Change the summary for the current array in the current DAF.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafrs_c.html

    :param insum: New summary for current array.
    """
    insum = stypes.to_double_vector(insum)
    libspice.dafrs_c(ctypes.byref(insum))


@spice_error_check
def dafus(insum: ndarray, nd: int, ni: int) -> Tuple[ndarray, ndarray]:
    """
    Unpack an array summary into its double precision and integer components.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafus_c.html

    :param insum: Array summary.
    :param nd: Number of double precision components.
    :param ni: Number of integer components.
    :return: Double precision components, Integer components.
    """
    insum = stypes.to_double_vector(insum)
    dc = stypes.empty_double_vector(nd)
    ic = stypes.empty_int_vector(ni)
    nd = ctypes.c_int(nd)
    ni = ctypes.c_int(ni)
    libspice.dafus_c(insum, nd, ni, dc, ic)
    return stypes.c_vector_to_python(dc), stypes.c_vector_to_python(ic)


@spice_error_check
def dasac(handle: int, buffer: Sequence[str]) -> None:
    """
    Add comments from a buffer of character strings to the comment
    area of a binary DAS file, appending them to any comments which
    are already present in the file's comment area.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dasac_c.html

    :param handle: DAS handle of a file opened with write access.
    :param buffer: Buffer of lines to be put into the comment area.
    """
    handle = ctypes.c_int(handle)
    n = ctypes.c_int(len(buffer))
    buflen = ctypes.c_int(max(len(s) for s in buffer) + 1)
    buffer = stypes.list_to_char_array_ptr(buffer)
    libspice.dasac_c(handle, n, buflen, buffer)


@spice_error_check
def dasadc(
    handle: int, n: int, bpos: int, epos: int, datlen: int, data: Sequence[str]
) -> None:
    """
    Add character data to a DAS file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dasadc_c.html

    :param handle: DAS file handle.
    :param n: Number of characters to add to file.
    :param bpos: Begin positions of substrings.
    :param epos: End positions of substrings.
    :param datlen: Common length of the character arrays in data.
    :param data: Array providing the set of substrings to be added.
    """
    _handle = ctypes.c_int(handle)
    _n = ctypes.c_int(n)
    _bpos = ctypes.c_int(bpos)
    _epos = ctypes.c_int(epos)
    _datlen = ctypes.c_int(datlen)
    sublen = epos - bpos + 1
    r = int((n + sublen - 1) // sublen)
    _data = stypes.list_to_char_array_ptr(data, x_len=epos + 1, y_len=r)
    libspice.dasadc_c(_handle, _n, _bpos, _epos, _datlen, _data)


@spice_error_check
def dasadd(handle: int, n: int, data: ndarray) -> None:
    """
    Add an array of double precision numbers to a DAS file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dasadd_c.html

    :param handle: DAS file handle.
    :param n: Number of d p numbers to add to DAS file.
    :param data: Array of d p numbers to add.
    """
    _handle = ctypes.c_int(handle)
    _n = ctypes.c_int(n)
    _data = stypes.to_double_vector(data)
    libspice.dasadd_c(_handle, _n, _data)


@spice_error_check
def dasadi(handle: int, n: int, data: ndarray) -> None:
    """
    Add an array of integers to a DAS file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dasadi_c.html

    :param handle: DAS file handle.
    :param n: Number of integers to add to DAS file.
    :param data: Array of integers to add.
    """
    _handle = ctypes.c_int(handle)
    _n = ctypes.c_int(n)
    _data = stypes.to_int_vector(data)
    libspice.dasadi_c(_handle, _n, _data)


@spice_error_check
def dascls(handle: int) -> None:
    """
    Close a DAS file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dascls_c.html

    :param handle: Handle of an open DAS file.
    """
    handle = ctypes.c_int(handle)
    libspice.dascls_c(handle)


@spice_error_check
def dasdc(handle: int) -> None:
    """
    Delete the entire comment area of a previously opened binary
    DAS file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dasdc_c.html

    :param handle: The handle of a binary DAS file opened for writing.
    """
    handle = ctypes.c_int(handle)
    libspice.dasdc_c(handle)


@spice_error_check
def dasec(
    handle: int, bufsiz: int = _default_len_out, buflen: int = _default_len_out
) -> Tuple[int, Iterable[str], int]:
    """
    Extract comments from the comment area of a binary DAS file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dasec_c.html

    :param handle: Handle of binary DAS file open with read access.
    :param bufsiz: Maximum size, in lines, of buffer.
    :param buflen: Line length associated with buffer.
    :return:
            Number of comments extracted from the DAS file,
            Buffer in which extracted comments are placed,
            Indicates whether all comments have been extracted.
    """
    handle = ctypes.c_int(handle)
    buffer = stypes.empty_char_array(buflen, bufsiz)
    bufsiz = ctypes.c_int(bufsiz)
    buflen = ctypes.c_int(buflen)
    n = ctypes.c_int(0)
    done = ctypes.c_int()
    libspice.dasec_c(
        handle,
        bufsiz,
        buflen,
        ctypes.byref(n),
        ctypes.byref(buffer),
        ctypes.byref(done),
    )
    return n.value, stypes.c_vector_to_python(buffer), done.value


@spice_error_check
def dashfn(handle: int, lenout: int = _default_len_out) -> str:
    """
    Return the name of the DAS file associated with a handle.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dashfn_c.html

    :param handle: Handle of a DAS file.
    :param lenout: Length of output file name string.
    :return: Corresponding file name.
    """
    handle = ctypes.c_int(handle)
    namlen = ctypes.c_int(lenout)
    fname = stypes.string_to_char_p(lenout)
    libspice.dashfn_c(handle, namlen, fname)
    return stypes.to_python_string(fname)


@spice_error_check
def dashfs(handle: int) -> Tuple[int, int, int, int, int, ndarray, ndarray, ndarray]:
    """
    Return a file summary for a specified DAS file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dashfs_c.html

    :param handle: Handle of a DAS file.
    :return:
        Number of reserved records in file,
        Number of characters in use in reserved rec area,
        Number of comment records in file,
        Number of characters in use in comment area,
        Number of first free record,
        Array of last logical addresses for each data type,
        Record number of last descriptor of each data type,
        Word number of last descriptor of each data type.
    """
    _handle = ctypes.c_int(handle)
    _nresvr = ctypes.c_int(0)
    _nresvc = ctypes.c_int(0)
    _ncomr = ctypes.c_int(0)
    _ncomc = ctypes.c_int(0)
    _free = ctypes.c_int(0)
    _lastla = stypes.empty_int_vector(
        3,
    )
    _lastrc = stypes.empty_int_vector(
        3,
    )
    _lastwd = stypes.empty_int_vector(
        3,
    )
    libspice.dashfs_c(
        _handle, _nresvr, _nresvc, _ncomr, _ncomc, _free, _lastla, _lastrc, _lastwd
    )
    return (
        _nresvr.value,
        _nresvc.value,
        _ncomr.value,
        _ncomc.value,
        _free.value,
        stypes.c_matrix_to_numpy(_lastla),
        stypes.c_matrix_to_numpy(_lastrc),
        stypes.c_matrix_to_numpy(_lastwd),
    )


@spice_error_check
def daslla(handle: int) -> Tuple[int, int, int]:
    """
    Return last DAS logical addresses of character, double precision
    and integer type that are currently in use in a specified DAS
    file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/daslla_c.html

    :param handle: DAS file handle.
    :return: Last character address in use, Last double precision address in use, Last integer address in use.
    """
    _handle = ctypes.c_int(handle)
    _lastc = ctypes.c_int(0)
    _lastd = ctypes.c_int(0)
    _lasti = ctypes.c_int(0)
    libspice.daslla_c(_handle, _lastc, _lastd, _lasti)
    return (
        _lastc.value,
        _lastd.value,
        _lasti.value,
    )


@spice_error_check
def dasllc(handle: int) -> None:
    """
    Close the DAS file associated with a given handle, without
    flushing buffered data or segregating the file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dasllc_c.html

    :param handle: Handle of a DAS file to be closed.
    """
    _handle = ctypes.c_int(handle)
    libspice.dasllc_c(_handle)


@spice_error_check
def dasonw(fname: str, ftype: str, ifname: str, ncomr: int) -> int:
    """
    Open a new DAS file and set the file type.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dasonw_c.html

    :param fname: Name of a DAS file to be opened.
    :param ftype: type
    :param ifname: internal file name
    :param ncomr: amount of comment area
    :return: Handle to new DAS file
    """
    _fname = stypes.string_to_char_p(fname)
    _ftype = stypes.string_to_char_p(ftype)
    _ifname = stypes.string_to_char_p(ifname)
    _ncomr = ctypes.c_int(ncomr)
    _handle = ctypes.c_int(0)
    libspice.dasonw_c(_fname, _ftype, _ifname, _ncomr, ctypes.byref(_handle))
    return _handle.value


@spice_error_check
def dasopr(fname: str) -> int:
    """
    Open a DAS file for reading.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dasopr_c.html

    :param fname: Name of a DAS file to be opened.
    :return: Handle assigned to the opened DAS file.
    """
    _fname = stypes.string_to_char_p(fname)
    _handle = ctypes.c_int()
    libspice.dasopr_c(_fname, ctypes.byref(_handle))
    return _handle.value


@spice_error_check
def dasops() -> int:
    """
    Open a scratch DAS file for writing.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dasops_c.html

    :return: Handle assigned to a scratch DAS file.
    """
    _handle = ctypes.c_int(0)
    libspice.dasops_c(ctypes.byref(_handle))
    return _handle.value


@spice_error_check
def dasopw(fname: str) -> int:
    """
    Open a DAS file for writing.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dasopw_c.html
    :param fname: Name of a DAS file to be opened.
    :return: Handle assigned to the opened DAS file.
    """
    fname = stypes.string_to_char_p(fname)
    handle = ctypes.c_int(0)
    libspice.dasopw_c(fname, ctypes.byref(handle))
    return handle.value


@spice_error_check
def dasrdd(handle: int, first: int, last: int) -> ndarray:
    """
    Read double precision data from a range of DAS logical addresses.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dasrdd_c.html

    :param handle: DAS file handle.
    :param first: start of range of DAS double precision.
    :param last: end of range of DAS double precision.
    :return: Data having addresses first through last.
    """
    _handle = ctypes.c_int(handle)
    _first = ctypes.c_int(first)
    _last = ctypes.c_int(last)
    _data = stypes.empty_double_vector((last - first) + 1)
    libspice.dasrdd_c(_handle, _first, _last, _data)
    return stypes.c_vector_to_python(_data)


@spice_error_check
def dasrdi(handle: int, first: int, last: int) -> ndarray:
    """
    Read integer data from a range of DAS logical addresses.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dasrdi_c.html

    :param handle: DAS file handle.
    :param first: start of range of DAS double precision.
    :param last: end of range of DAS double precision.
    :return: Data having addresses first through last.
    """
    _handle = ctypes.c_int(handle)
    _first = ctypes.c_int(first)
    _last = ctypes.c_int(last)
    _data = stypes.empty_int_vector((last - first) + 1)
    libspice.dasrdi_c(_handle, _first, _last, _data)
    return stypes.c_vector_to_python(_data)


@spice_error_check
def dasrfr(
    handle: int, lenout: int = _default_len_out
) -> Tuple[str, str, int, int, int, int]:
    """
    Return the contents of the file record of a specified DAS file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dasrfr_c.html

    :param handle: DAS file handle.
    :param lenout: length of output strs
    :return: ID word, DAS internal file name, Number of reserved records in file, \
    Number of characters in use in reserved rec. area, Number of comment records in file, \
    Number of characters in use in comment area.
    """
    handle = ctypes.c_int(handle)
    idwlen = ctypes.c_int(lenout)  # intentional
    ifnlen = ctypes.c_int(lenout)  # intentional
    idword = stypes.string_to_char_p(lenout)
    ifname = stypes.string_to_char_p(lenout)
    nresvr = ctypes.c_int(0)
    nresvc = ctypes.c_int(0)
    ncomr = ctypes.c_int(0)
    ncomc = ctypes.c_int(0)
    libspice.dasrfr_c(
        handle,
        idwlen,
        ifnlen,
        idword,
        ifname,
        ctypes.byref(nresvr),
        ctypes.byref(nresvc),
        ctypes.byref(ncomr),
        ctypes.byref(ncomc),
    )
    return (
        stypes.to_python_string(idword),
        stypes.to_python_string(ifname),
        nresvr.value,
        nresvc.value,
        ncomr.value,
        ncomc.value,
    )


@spice_error_check
def dasudd(handle: int, first: int, last: int, data: ndarray) -> None:
    """
    Update data in a specified range of double precision addresses
    in a DAS file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dasudd_c.html

    :param handle: DAS file handle.
    :param first: first address
    :param last: Range of d p addresses to write to.
    :param data: An array of d p numbers.
    """
    _handle = ctypes.c_int(handle)
    _first = ctypes.c_int(first)
    _last = ctypes.c_int(last)
    _data = stypes.to_double_vector(data)
    libspice.dasudd_c(_handle, _first, _last, _data)


@spice_error_check
def dasudi(handle: int, first: int, last: int, data: ndarray) -> None:
    """
    Update data in a specified range of integer addresses in a DAS
    file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dasudi_c.html

    :param handle: DAS file handle.
    :param first: first integer addresses to write to.
    :param last: last integer addresses to write to.
    :param data: An array of integers.
    """
    _handle = ctypes.c_int(handle)
    _first = ctypes.c_int(first)
    _last = ctypes.c_int(last)
    _data = stypes.to_int_vector(data)
    libspice.dasudi_c(_handle, _first, _last, _data)


@spice_error_check
def daswbr(handle: int) -> None:
    """
    Write out all buffered records of a specified DAS file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/daswbr_c.html

    :param handle: Handle of DAS file.
    """
    _handle = ctypes.c_int(handle)
    libspice.daswbr_c(_handle)


@spice_error_check
def dazldr(x: float, y: float, z: float, azccw: bool, elplsz: bool) -> ndarray:
    """
    Compute the Jacobian matrix of the transformation from
    rectangular to azimuth/elevation coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dazldr_c.html

    :param x: x coordinate of point.
    :param y: y coordinate of point.
    :param z: z coordinate of point.
    :param azccw: Flag indicating how azimuth is measured.
    :param elplsz: Flag indicating how elevation is measured.
    :return: Matrix of partial derivatives.
    """
    _x = ctypes.c_double(x)
    _y = ctypes.c_double(y)
    _z = ctypes.c_double(z)
    _azccw = ctypes.c_int(azccw)
    _elplsz = ctypes.c_int(elplsz)
    _jacobi = stypes.empty_double_matrix(3, 3)
    libspice.dazldr_c(_x, _y, _z, _azccw, _elplsz, _jacobi)
    return stypes.c_matrix_to_numpy(_jacobi)


@spice_error_check
def dcyldr(x: float, y: float, z: float) -> ndarray:
    """
    This routine computes the Jacobian of the transformation from
    rectangular to cylindrical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dcyldr_c.html

    :param x: X-coordinate of point.
    :param y: Y-coordinate of point.
    :param z: Z-coordinate of point.
    :return: Matrix of partial derivatives.
    """
    x = ctypes.c_double(x)
    y = ctypes.c_double(y)
    z = ctypes.c_double(z)
    jacobi = stypes.empty_double_matrix()
    libspice.dcyldr_c(x, y, z, jacobi)
    return stypes.c_matrix_to_numpy(jacobi)


@spice_error_check
def deltet(epoch: float, eptype: str) -> float:
    """
    Return the value of Delta ET (ET-UTC) for an input epoch.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/deltet_c.html

    :param epoch: Input epoch (seconds past J2000).
    :param eptype: Type of input epoch ("UTC" or "ET").
    :return: Delta ET (ET-UTC) at input epoch.
    """
    epoch = ctypes.c_double(epoch)
    eptype = stypes.string_to_char_p(eptype)
    delta = ctypes.c_double()
    libspice.deltet_c(epoch, eptype, ctypes.byref(delta))
    return delta.value


@spice_error_check
def det(m1: ndarray) -> float:
    """
    Compute the determinant of a double precision 3x3 matrix.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/det_c.html

    :param m1: Matrix whose determinant is to be found.
    :return: The determinant of the matrix.
    """
    m1 = stypes.to_double_matrix(m1)
    return libspice.det_c(m1)


@spice_error_check
def dgeodr(x: float, y: float, z: float, re: float, f: float) -> ndarray:
    """
    This routine computes the Jacobian of the transformation from
    rectangular to geodetic coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dgeodr_c.html

    :param x: X-coordinate of point.
    :param y: Y-coordinate of point.
    :param z: Z-coord
    :param re: Equatorial radius of the reference spheroid.
    :param f: Flattening coefficient.
    :return: Matrix of partial derivatives.
    """
    x = ctypes.c_double(x)
    y = ctypes.c_double(y)
    z = ctypes.c_double(z)
    re = ctypes.c_double(re)
    f = ctypes.c_double(f)
    jacobi = stypes.empty_double_matrix()
    libspice.dgeodr_c(x, y, z, re, f, jacobi)
    return stypes.c_matrix_to_numpy(jacobi)


@spice_error_check
def diags2(
    symmat: Union[ndarray, Iterable[Iterable[float]]]
) -> Tuple[ndarray, ndarray]:
    """
    Diagonalize a symmetric 2x2 matrix.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/diags2_c.html

    :param symmat: A symmetric 2x2 matrix.
    :return:
            A diagonal matrix similar to symmat,
            A rotation used as the similarity transformation.
    """
    symmat = stypes.to_double_matrix(symmat)
    diag = stypes.empty_double_matrix(x=2, y=2)
    rotateout = stypes.empty_double_matrix(x=2, y=2)
    libspice.diags2_c(symmat, diag, rotateout)
    return stypes.c_matrix_to_numpy(diag), stypes.c_matrix_to_numpy(rotateout)


@spice_error_check
def diff(a: SpiceCell, b: SpiceCell) -> SpiceCell:
    """
    Take the difference of two sets of any data type to form a third set.
    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/diff_c.html

    :param a: First input set.
    :param b: Second input set.
    :return: Difference of a and b.
    """
    assert isinstance(a, stypes.SpiceCell)
    assert isinstance(b, stypes.SpiceCell)
    assert a.dtype == b.dtype
    # The next line was redundant with the [raise NotImplementedError] line below
    # assert a.dtype == 0 or a.dtype == 1 or a.dtype == 2
    if a.dtype == 0:
        c = stypes.SPICECHAR_CELL(max(a.size, b.size), max(a.length, b.length))
    elif a.dtype == 1:
        c = stypes.SPICEDOUBLE_CELL(max(a.size, b.size))
    elif a.dtype == 2:
        c = stypes.SPICEINT_CELL(max(a.size, b.size))
    else:
        raise NotImplementedError
    libspice.diff_c(ctypes.byref(a), ctypes.byref(b), ctypes.byref(c))
    return c


@spice_error_check
@spice_found_exception_thrower
def dlabbs(handle: int) -> Tuple[SpiceDLADescr, bool]:
    """
    Begin a backward segment search in a DLA file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dlabbs_c.html

    :param handle: Handle of open DLA file.
    :return: Descriptor of last segment in DLA file
    """
    handle = ctypes.c_int(handle)
    descr = stypes.SpiceDLADescr()
    found = ctypes.c_int()
    libspice.dlabbs_c(handle, ctypes.byref(descr), ctypes.byref(found))
    return descr, bool(found.value)


@spice_error_check
@spice_found_exception_thrower
def dlabfs(handle: int) -> Tuple[SpiceDLADescr, bool]:
    """
    Begin a forward segment search in a DLA file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dlabfs_c.html

    :param handle: Handle of open DLA file.
    :return: Descriptor of next segment in DLA file
    """
    handle = ctypes.c_int(handle)
    descr = stypes.SpiceDLADescr()
    found = ctypes.c_int()
    libspice.dlabfs_c(handle, ctypes.byref(descr), ctypes.byref(found))
    return descr, bool(found.value)


@spice_error_check
def dlabns(handle: int) -> None:
    """
    Begin a new segment in a DLA file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dlabns_c.html

    :param handle: Handle of open DLA file.
    """
    _handle = ctypes.c_int(handle)
    libspice.dlabns_c(_handle)


@spice_error_check
def dlaens(handle: int) -> None:
    """
    End a new segment in a DLA file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dlaens_c.html

    :param handle: Handle of open DLA file.
    """
    _handle = ctypes.c_int(handle)
    libspice.dlaens_c(_handle)


@spice_error_check
def dlaopn(fname: str, ftype: str, ifname: str, ncomch: int) -> int:
    """
    Open a new DLA file and set the file type.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dlaopn_c.html

    :param fname: Name of a DLA file to be opened.
    :param ftype: Mnemonic code for type of data in the DLA file.
    :param ifname: Internal file name.
    :param ncomch: Number of comment characters to allocate.
    :return: Handle assigned to the opened DLA file.
    """
    _fname = stypes.string_to_char_p(fname)
    _ftype = stypes.string_to_char_p(ftype)
    _ifname = stypes.string_to_char_p(ifname)
    _ncomch = ctypes.c_int(ncomch)
    _handle = ctypes.c_int(0)
    libspice.dlaopn_c(_fname, _ftype, _ifname, _ncomch, _handle)
    return _handle.value


@spice_error_check
@spice_found_exception_thrower
def dlafns(handle: int, descr: SpiceDLADescr) -> Tuple[SpiceDLADescr, bool]:
    """
    Find the segment following a specified segment in a DLA file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dlafns_c.html

    :param handle: Handle of open DLA file.
    :param descr: Descriptor of a DLA segment.
    :return: Descriptor of next segment in DLA file
    """
    assert isinstance(descr, stypes.SpiceDLADescr)
    handle = ctypes.c_int(handle)
    nxtdsc = stypes.SpiceDLADescr()
    found = ctypes.c_int()
    libspice.dlafns_c(
        handle, ctypes.byref(descr), ctypes.byref(nxtdsc), ctypes.byref(found)
    )
    return nxtdsc, bool(found.value)


@spice_error_check
@spice_found_exception_thrower
def dlafps(handle: int, descr: SpiceDLADescr) -> Tuple[SpiceDLADescr, bool]:
    """
    Find the segment preceding a specified segment in a DLA file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dlafps_c.html

    :param handle: Handle of open DLA file.
    :param descr: Descriptor of a segment in DLA file.
    :return: Descriptor of previous segment in DLA file
    """
    assert isinstance(descr, stypes.SpiceDLADescr)
    handle = ctypes.c_int(handle)
    prvdsc = stypes.SpiceDLADescr()
    found = ctypes.c_int()
    libspice.dlafps_c(
        handle, ctypes.byref(descr), ctypes.byref(prvdsc), ctypes.byref(found)
    )
    return prvdsc, bool(found.value)


@spice_error_check
def dlatdr(x: float, y: float, z: float) -> ndarray:
    """
    This routine computes the Jacobian of the transformation from
    rectangular to latitudinal coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dlatdr_c.html

    :param x: X-coordinate of point.
    :param y: Y-coordinate of point.
    :param z: Z-coord
    :return: Matrix of partial derivatives.
    """
    x = ctypes.c_double(x)
    y = ctypes.c_double(y)
    z = ctypes.c_double(z)
    jacobi = stypes.empty_double_matrix()
    libspice.dlatdr_c(x, y, z, jacobi)
    return stypes.c_matrix_to_numpy(jacobi)


@spice_error_check
@spice_found_exception_thrower
def dnearp(
    state: ndarray, a: float, b: float, c: float
) -> Tuple[ndarray, ndarray, bool]:
    """
    Compute the state (position and velocity) of an ellipsoid surface
    point nearest to the position component of a specified state.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dnearp_c.html

    :param state: State of an object in body fixed coordinates.
    :param a: Length of semi axis parallel to X axis.
    :param b: Length of semi axis parallel to Y axis.
    :param c: Length on semi axis parallel to Z axis.
    :return: State of the nearest point on the ellipsoid, Altitude and derivative of altitude
    """
    _state = stypes.to_double_matrix(state)
    _a = ctypes.c_double(a)
    _b = ctypes.c_double(b)
    _c = ctypes.c_double(c)
    _dnear = stypes.empty_double_vector(
        6,
    )
    _dalt = stypes.empty_double_vector(
        2,
    )
    _found = ctypes.c_int(0)
    libspice.dnearp_c(_state, _a, _b, _c, _dnear, _dalt, _found)
    return (
        stypes.c_vector_to_python(_dnear),
        stypes.c_vector_to_python(_dalt),
        bool(_found.value),
    )


@spice_error_check
def dp2hx(number: float, lenout: int = _default_len_out) -> str:
    """
    Convert a double precision number to an equivalent character
    string using base 16 "scientific notation."

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dp2hx_c.html

    :param number: D.p. number to be converted.
    :param lenout: Available space for output string.
    :return: Equivalent character string, left justified.
    """
    number = ctypes.c_double(number)
    lenout = ctypes.c_int(lenout)
    string = stypes.string_to_char_p(lenout)
    length = ctypes.c_int()
    libspice.dp2hx_c(number, lenout, string, ctypes.byref(length))
    return stypes.to_python_string(string)


@spice_error_check
def dpgrdr(body: str, x: float, y: float, z: int, re: float, f: float) -> ndarray:
    """
    This routine computes the Jacobian matrix of the transformation
    from rectangular to planetographic coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dpgrdr_c.html

    :param body: Body with which coordinate system is associated.
    :param x: X-coordinate of point.
    :param y: Y-coordinate of point.
    :param z: Z-coordinate of point.
    :param re: Equatorial radius of the reference spheroid.
    :param f: Flattening coefficient.
    :return: Matrix of partial derivatives.
    """
    body = stypes.string_to_char_p(body)
    x = ctypes.c_double(x)
    y = ctypes.c_double(y)
    z = ctypes.c_double(z)
    re = ctypes.c_double(re)
    f = ctypes.c_double(f)
    jacobi = stypes.empty_double_matrix()
    libspice.dpgrdr_c(body, x, y, z, re, f, jacobi)
    return stypes.c_matrix_to_numpy(jacobi)


@spice_error_check
def dpmax() -> float:
    """
    Return the value of the largest (positive) number representable
    in a double precision variable.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dpmax_c.html

    :return:
            The largest (positive) number representable
            in a double precision variable.
    """
    return libspice.dpmax_c()


@spice_error_check
def dpmin() -> float:
    """
    Return the value of the smallest (negative) number representable
    in a double precision variable.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dpmin_c.html

    :return:
            The smallest (negative) number that can be represented
            in a double precision variable.
    """
    return libspice.dpmin_c()


@spice_error_check
def dpr() -> float:
    """
    Return the number of degrees per radian.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dpr_c.html

    :return: The number of degrees per radian.
    """
    return libspice.dpr_c()


@spice_error_check
def drdazl(range: float, az: float, el: float, azccw: bool, elplsz: bool) -> ndarray:
    """
    Compute the Jacobian matrix of the transformation from
    azimuth/elevation to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/drdazl_c.html

    :param range: Distance of a point from the origin.
    :param az: Azimuth of input point in radians.
    :param el: Elevation of input point in radians.
    :param azccw: Flag indicating how azimuth is measured.
    :param elplsz: Flag indicating how elevation is measured.
    :return: Matrix of partial derivatives.
    """
    _range = ctypes.c_double(range)
    _az = ctypes.c_double(az)
    _el = ctypes.c_double(el)
    _azccw = ctypes.c_int(azccw)
    _elplsz = ctypes.c_int(elplsz)
    _jacobi = stypes.empty_double_matrix(3, 3)
    libspice.drdazl_c(_range, _az, _el, _azccw, _elplsz, _jacobi)
    return stypes.c_matrix_to_numpy(_jacobi)


@spice_error_check
def drdcyl(r: float, lon: float, z: float) -> ndarray:
    """
    This routine computes the Jacobian of the transformation from
    cylindrical to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/drdcyl_c.html

    :param r: Distance of a point from the origin.
    :param lon: Angle of the point from the xz plane in radians.
    :param z: Height of the point above the xy plane.
    :return: Matrix of partial derivatives.
    """
    r = ctypes.c_double(r)
    lon = ctypes.c_double(lon)
    z = ctypes.c_double(z)
    jacobi = stypes.empty_double_matrix()
    libspice.drdcyl_c(r, lon, z, jacobi)
    return stypes.c_matrix_to_numpy(jacobi)


@spice_error_check
def drdgeo(lon: float, lat: float, alt: float, re: float, f: float) -> ndarray:
    """
    This routine computes the Jacobian of the transformation from
    geodetic to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/drdgeo_c.html

    :param lon: Geodetic longitude of point (radians).
    :param lat: Geodetic latitude of point (radians).
    :param alt: Altitude of point above the reference spheroid.
    :param re: Equatorial radius of the reference spheroid.
    :param f: Flattening coefficient.
    :return: Matrix of partial derivatives.
    """
    lon = ctypes.c_double(lon)
    lat = ctypes.c_double(lat)
    alt = ctypes.c_double(alt)
    re = ctypes.c_double(re)
    f = ctypes.c_double(f)
    jacobi = stypes.empty_double_matrix()
    libspice.drdgeo_c(lon, lat, alt, re, f, jacobi)
    return stypes.c_matrix_to_numpy(jacobi)


@spice_error_check
def drdlat(r: float, lon: float, lat: float) -> ndarray:
    """
    Compute the Jacobian of the transformation from latitudinal to
    rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/drdlat_c.html

    :param r: Distance of a point from the origin.
    :param lon: Angle of the point from the XZ plane in radians.
    :param lat: Angle of the point from the XY plane in radians.
    :return: Matrix of partial derivatives.
    """
    r = ctypes.c_double(r)
    lon = ctypes.c_double(lon)
    lat = ctypes.c_double(lat)
    jacobi = stypes.empty_double_matrix()
    libspice.drdlat_c(r, lon, lat, jacobi)
    return stypes.c_matrix_to_numpy(jacobi)


@spice_error_check
def drdpgr(body: str, lon: float, lat: float, alt: int, re: float, f: float) -> ndarray:
    """
    This routine computes the Jacobian matrix of the transformation
    from planetographic to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/drdpgr_c.html

    :param body: Body with which coordinate system is associated.
    :param lon: Planetographic longitude of a point (radians).
    :param lat: Planetographic latitude of a point (radians).
    :param alt: Altitude of a point above reference spheroid.
    :param re: Equatorial radius of the reference spheroid.
    :param f: Flattening coefficient.
    :return: Matrix of partial derivatives.
    """
    body = stypes.string_to_char_p(body)
    lon = ctypes.c_double(lon)
    lat = ctypes.c_double(lat)
    alt = ctypes.c_double(alt)
    re = ctypes.c_double(re)
    f = ctypes.c_double(f)
    jacobi = stypes.empty_double_matrix()
    libspice.drdpgr_c(body, lon, lat, alt, re, f, jacobi)
    return stypes.c_matrix_to_numpy(jacobi)


@spice_error_check
def drdsph(r: float, colat: float, lon: float) -> ndarray:
    """
    This routine computes the Jacobian of the transformation from
    spherical to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/drdsph_c.html

    :param r: Distance of a point from the origin.
    :param colat: Angle of the point from the positive z-axis.
    :param lon: Angle of the point from the xy plane.
    :return: Matrix of partial derivatives.
    """
    r = ctypes.c_double(r)
    colat = ctypes.c_double(colat)
    lon = ctypes.c_double(lon)
    jacobi = stypes.empty_double_matrix()
    libspice.drdsph_c(r, colat, lon, jacobi)
    return stypes.c_matrix_to_numpy(jacobi)


@spice_error_check
def dskb02(
    handle: int, dladsc: SpiceDLADescr
) -> Tuple[int, int, int, ndarray, float, ndarray, ndarray, int, int, int, int]:
    """
    Return bookkeeping data from a DSK type 2 segment.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dskb02_c.html

    :param handle: DSK file handle
    :param dladsc: DLA descriptor
    :return: bookkeeping data from a DSK type 2 segment
    """

    handle = ctypes.c_int(handle)
    nv = ctypes.c_int(0)
    np = ctypes.c_int(0)
    nvxtot = ctypes.c_int(0)
    vtxbds = stypes.empty_double_matrix(3, 2)
    voxsiz = ctypes.c_double(0.0)
    voxori = stypes.empty_double_vector(3)
    vgrext = stypes.empty_int_vector(3)
    cgscal = ctypes.c_int(0)
    vtxnpl = ctypes.c_int(0)
    voxnpt = ctypes.c_int(0)
    voxnpl = ctypes.c_int(0)
    libspice.dskb02_c(
        handle,
        dladsc,
        ctypes.byref(nv),
        ctypes.byref(np),
        ctypes.byref(nvxtot),
        vtxbds,
        ctypes.byref(voxsiz),
        voxori,
        vgrext,
        ctypes.byref(cgscal),
        ctypes.byref(vtxnpl),
        ctypes.byref(voxnpt),
        ctypes.byref(voxnpl),
    )
    return (
        nv.value,
        np.value,
        nvxtot.value,
        stypes.c_matrix_to_numpy(vtxbds),
        voxsiz.value,
        stypes.c_vector_to_python(voxori),
        stypes.c_vector_to_python(vgrext),
        cgscal.value,
        vtxnpl.value,
        voxnpt.value,
        voxnpl.value,
    )


@spice_error_check
def dskcls(handle: int, optmiz: bool = False) -> None:
    """
    Close a DSK file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dskcls_c.html

    :param handle: Handle assigned to the opened DSK file.
    :param optmiz: Flag indicating whether to segregate the DSK.
    :return:
    """
    handle = ctypes.c_int(handle)
    optmiz = ctypes.c_int(optmiz)
    libspice.dskcls_c(handle, optmiz)


@spice_error_check
def dskd02(
    handle: int, dladsc: SpiceDLADescr, item: int, start: int, room: int
) -> ndarray:
    """
    Fetch double precision data from a type 2 DSK segment.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dskd02_c.html

    :param handle: DSK file handle
    :param dladsc: DLA descriptor
    :param item: Keyword identifying item to fetch
    :param start: Start index
    :param room: Amount of room in output array
    :return: Array containing requested item
    """

    handle = ctypes.c_int(handle)
    item = ctypes.c_int(item)
    start = ctypes.c_int(start)
    room = ctypes.c_int(room)
    n = ctypes.c_int(0)
    values = stypes.empty_double_vector(room)
    libspice.dskd02_c(handle, dladsc, item, start, room, ctypes.byref(n), values)
    return stypes.c_vector_to_python(values)


@spice_error_check
def dskgd(handle: int, dladsc: SpiceDLADescr) -> SpiceDSKDescr:
    """
    Return the DSK descriptor from a DSK segment identified
    by a DAS handle and DLA descriptor.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dskgd_c.html

    :param handle: Handle assigned to the opened DSK file.
    :param dladsc: DLA segment descriptor.
    :return: DSK segment descriptor.
    """
    handle = ctypes.c_int(handle)
    dskdsc = stypes.SpiceDSKDescr()
    libspice.dskgd_c(handle, ctypes.byref(dladsc), ctypes.byref(dskdsc))
    return dskdsc


@spice_error_check
def dskgtl(keywrd: int) -> float:
    """
    Retrieve the value of a specified DSK tolerance or margin parameter.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dskgtl_c.html

    :param keywrd: Code specifying parameter to retrieve.
    :return: Value of parameter.
    """
    keywrd = ctypes.c_int(keywrd)
    dpval = ctypes.c_double(0)
    libspice.dskgtl_c(keywrd, ctypes.byref(dpval))
    return dpval.value


@spice_error_check
def dski02(
    handle: int, dladsc: SpiceDLADescr, item: int, start: int, room: int
) -> ndarray:
    """
    Fetch integer data from a type 2 DSK segment.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dski02_c.html

    :param handle: DSK file handle.
    :param dladsc: DLA descriptor.
    :param item: Keyword identifying item to fetch.
    :param start: Start index.
    :param room: Amount of room in output array.
    :return: Array containing requested item.
    """
    handle = ctypes.c_int(handle)
    item = ctypes.c_int(item)
    start = ctypes.c_int(start)
    room = ctypes.c_int(room)
    n = ctypes.c_int()
    values = stypes.empty_int_vector(room)
    libspice.dski02_c(handle, dladsc, item, start, room, ctypes.byref(n), values)
    return stypes.c_matrix_to_numpy(values)


@spice_error_check
def dskmi2(
    vrtces: ndarray,
    plates: ndarray,
    finscl: float,
    corscl: int,
    worksz: int,
    voxpsz: int,
    voxlsz: int,
    makvtl: bool,
    spxisz: int,
) -> Tuple[ndarray, ndarray]:
    """
    Make spatial index for a DSK type 2 segment. The index is returned
    as a pair of arrays, one of type int and one of type
    float. These arrays are suitable for use with the DSK type 2
    writer dskw02.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dskmi2_c.html

    :param vrtces: Vertices
    :param plates: Plates
    :param finscl: Fine voxel scale
    :param corscl: Coarse voxel scale
    :param worksz: Workspace size
    :param voxpsz: Voxel plate pointer array size
    :param voxlsz: Voxel plate list array size
    :param makvtl: Vertex plate list flag
    :param spxisz: Spatial index integer component size
    :return: double precision and integer components of the spatial index of the segment.
    """
    nv = ctypes.c_int(len(vrtces))
    vrtces = stypes.to_double_matrix(vrtces)
    np = ctypes.c_int(len(plates))
    plates = stypes.to_int_matrix(plates)
    finscl = ctypes.c_double(finscl)
    corscl = ctypes.c_int(corscl)
    worksz = ctypes.c_int(worksz)
    voxpsz = ctypes.c_int(voxpsz)
    voxlsz = ctypes.c_int(voxlsz)
    makvtl = ctypes.c_int(makvtl)
    spxisz = ctypes.c_int(spxisz)
    work = stypes.empty_int_matrix(2, worksz)
    spaixd = stypes.empty_double_vector(10)  # SPICE_DSK02_SPADSZ
    spaixi = stypes.empty_int_vector(spxisz)
    libspice.dskmi2_c(
        nv,
        vrtces,
        np,
        plates,
        finscl,
        corscl,
        worksz,
        voxpsz,
        voxlsz,
        makvtl,
        spxisz,
        work,
        spaixd,
        spaixi,
    )
    return stypes.c_vector_to_python(spaixd), stypes.c_vector_to_python(spaixi)


@spice_error_check
def dskn02(handle: int, dladsc: SpiceDLADescr, plid: int) -> ndarray:
    """
    Compute the unit normal vector for a specified plate from a type
    2 DSK segment.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dskn02_c.html

    :param handle: DSK file handle.
    :param dladsc: DLA descriptor.
    :param plid: Plate ID.
    :return: late's unit normal vector.
    """
    handle = ctypes.c_int(handle)
    plid = ctypes.c_int(plid)
    normal = stypes.empty_double_vector(3)
    libspice.dskn02_c(handle, dladsc, plid, normal)
    return stypes.c_vector_to_python(normal)


@spice_error_check
def dskobj(dsk: str) -> SpiceCell:
    """
    Find the set of body ID codes of all objects for which
    topographic data are provided in a specified DSK file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dskobj_c.html

    :param dsk: Name of DSK file.
    :return: Set of ID codes of objects in DSK file.
    """
    dsk = stypes.string_to_char_p(dsk)
    bodids = stypes.SPICEINT_CELL(10000)
    libspice.dskobj_c(dsk, ctypes.byref(bodids))
    return bodids


@spice_error_check
def dskopn(fname: str, ifname: str, ncomch: int) -> int:
    """
    Open a new DSK file for subsequent write operations.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dskopn_c.html

    :param fname: Name of a DSK file to be opened.
    :param ifname: Internal file name.
    :param ncomch: Number of comment characters to allocate.
    :return: Handle assigned to the opened DSK file.
    """
    fname = stypes.string_to_char_p(fname)
    ifname = stypes.string_to_char_p(ifname)
    ncomch = ctypes.c_int(ncomch)
    handle = ctypes.c_int()
    libspice.dskopn_c(fname, ifname, ncomch, ctypes.byref(handle))
    return handle.value


@spice_error_check
def dskp02(handle: int, dladsc: SpiceDLADescr, start: int, room: int) -> ndarray:
    """
    Fetch triangular plates from a type 2 DSK segment.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dskp02_c.html

    :param handle: DSK file handle.
    :param dladsc: DLA descriptor.
    :param start: Start index.
    :param room: Amount of room in output array.
    :return: Array containing plates.

    """
    handle = ctypes.c_int(handle)
    start = ctypes.c_int(start)
    room = ctypes.c_int(room)
    n = ctypes.c_int(0)
    plates = stypes.empty_int_matrix(3, room)
    libspice.dskp02_c(handle, dladsc, start, room, ctypes.byref(n), plates)
    return stypes.c_matrix_to_numpy(plates)


@spice_error_check
def dskrb2(
    vrtces: ndarray, plates: ndarray, corsys: int, corpar: ndarray
) -> Tuple[float, float]:
    """
    Determine range bounds for a set of triangular plates to
    be stored in a type 2 DSK segment.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dskrb2_c.html

    :param vrtces: Vertices
    :param plates: Plates
    :param corsys: DSK coordinate system code
    :param corpar: DSK coordinate system parameters
    :return: Lower and Upper bound on range of third coordinate
    """
    nv = ctypes.c_int(len(vrtces))
    vrtces = stypes.to_double_matrix(vrtces)
    np = ctypes.c_int(len(plates))
    plates = stypes.to_int_matrix(plates)
    corsys = ctypes.c_int(corsys)
    corpar = stypes.to_double_vector(corpar)
    mncor3 = ctypes.c_double(0.0)
    mxcor3 = ctypes.c_double(0.0)
    libspice.dskrb2_c(
        nv,
        vrtces,
        np,
        plates,
        corsys,
        corpar,
        ctypes.byref(mncor3),
        ctypes.byref(mxcor3),
    )

    return mncor3.value, mxcor3.value


@spice_error_check
def dsksrf(dsk: str, bodyid: int) -> SpiceCell:
    """
    Find the set of surface ID codes for all surfaces associated with
    a given body in a specified DSK file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dsksrf_c.html

    :param dsk: Name of DSK file.
    :param bodyid: Integer body ID code.
    :return: Set of ID codes of surfaces in DSK file.
    """
    dsk = stypes.string_to_char_p(dsk)
    bodyid = ctypes.c_int(bodyid)
    srfids = stypes.SPICEINT_CELL(10000)
    libspice.dsksrf_c(dsk, bodyid, ctypes.byref(srfids))
    return srfids


@spice_error_check
def dskstl(keywrd: int, dpval: float) -> None:
    """
    Set the value of a specified DSK tolerance or margin parameter.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dskstl_c.html

    :param keywrd: Code specifying parameter to set.
    :param dpval: Value of parameter.
    :return:
    """
    keywrd = ctypes.c_int(keywrd)
    dpval = ctypes.c_double(dpval)
    libspice.dskstl_c(keywrd, dpval)


@spice_error_check
def dskv02(handle: int, dladsc: SpiceDLADescr, start: int, room: int) -> ndarray:
    """
    Fetch vertices from a type 2 DSK segment.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dskv02_c.html

    :param handle: DSK file handle.
    :param dladsc: DLA descriptor.
    :param start: Start index.
    :param room: Amount of room in output array.
    :return: Array containing vertices.
    """
    handle = ctypes.c_int(handle)
    start = ctypes.c_int(start)
    room = ctypes.c_int(room)
    n = ctypes.c_int()
    vrtces = stypes.empty_double_matrix(3, room)
    libspice.dskv02_c(handle, dladsc, start, room, ctypes.byref(n), vrtces)
    return stypes.c_matrix_to_numpy(vrtces)


@spice_error_check
def dskw02(
    handle: int,
    center: int,
    surfid: int,
    dclass: int,
    fname: str,
    corsys: int,
    corpar: ndarray,
    mncor1: float,
    mxcor1: float,
    mncor2: float,
    mxcor2: float,
    mncor3: float,
    mxcor3: float,
    first: float,
    last: float,
    vrtces: ndarray,
    plates: ndarray,
    spaixd: ndarray,
    spaixi: ndarray,
) -> None:
    """
    Write a type 2 segment to a DSK file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dskw02_c.html

    :param handle: Handle assigned to the opened DSK file
    :param center: Central body ID code
    :param surfid: Surface ID code
    :param dclass: Data class
    :param fname: Reference frame
    :param corsys: Coordinate system code
    :param corpar: Coordinate system parameters
    :param mncor1: Minimum value of first coordinate
    :param mxcor1: Maximum value of first coordinate
    :param mncor2: Minimum value of second coordinate
    :param mxcor2: Maximum value of second coordinate
    :param mncor3: Minimum value of third coordinate
    :param mxcor3: Maximum value of third coordinate
    :param first: Coverage start time
    :param last: Coverage stop time
    :param vrtces: Vertices
    :param plates: Plates
    :param spaixd: Double precision component of spatial index
    :param spaixi: Integer component of spatial index
    """
    handle = ctypes.c_int(handle)
    center = ctypes.c_int(center)
    surfid = ctypes.c_int(surfid)
    dclass = ctypes.c_int(dclass)
    fname = stypes.string_to_char_p(fname)
    corsys = ctypes.c_int(corsys)
    corpar = stypes.to_double_vector(corpar)
    mncor1 = ctypes.c_double(mncor1)
    mxcor1 = ctypes.c_double(mxcor1)
    mncor2 = ctypes.c_double(mncor2)
    mxcor2 = ctypes.c_double(mxcor2)
    mncor3 = ctypes.c_double(mncor3)
    mxcor3 = ctypes.c_double(mxcor3)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    nv = ctypes.c_int(len(vrtces))
    vrtces = stypes.to_double_matrix(vrtces)
    np = ctypes.c_int(len(plates))
    plates = stypes.to_int_matrix(plates)
    spaixd = stypes.to_double_vector(spaixd)
    spaixi = stypes.to_int_vector(spaixi)
    libspice.dskw02_c(
        handle,
        center,
        surfid,
        dclass,
        fname,
        corsys,
        corpar,
        mncor1,
        mxcor1,
        mncor2,
        mxcor2,
        mncor3,
        mxcor3,
        first,
        last,
        nv,
        vrtces,
        np,
        plates,
        spaixd,
        spaixi,
    )


@spice_error_check
def dskx02(
    handle: int, dladsc: SpiceDLADescr, vertex: ndarray, raydir: ndarray
) -> Tuple[int, ndarray, bool]:
    """
    Determine the plate ID and body-fixed coordinates of the
    intersection of a specified ray with the surface defined by a
    type 2 DSK plate model.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dskx02_c.html

    :param handle: Handle of DSK kernel containing plate model.
    :param dladsc: DLA descriptor of plate model segment.
    :param vertex: Ray's vertex in the  body fixed frame.
    :param raydir: Ray direction in the body fixed frame.
    :return: ID code of the plate intersected by the ray, Intercept, and Flag indicating whether intercept exists.
    """
    handle = ctypes.c_int(handle)
    vertex = stypes.to_double_vector(vertex)
    raydir = stypes.to_double_vector(raydir)
    plid = ctypes.c_int()
    xpt = stypes.empty_double_vector(3)
    found = ctypes.c_int()
    libspice.dskx02_c(
        handle,
        ctypes.byref(dladsc),
        vertex,
        raydir,
        ctypes.byref(plid),
        xpt,
        ctypes.byref(found),
    )
    return plid.value, stypes.c_vector_to_python(xpt), bool(found.value)


@spice_error_check
@spice_found_exception_thrower
def dskxsi(
    pri: bool,
    target: str,
    srflst: Sequence[int],
    et: float,
    fixref: str,
    vertex: ndarray,
    raydir: ndarray,
) -> Tuple[ndarray, int, SpiceDLADescr, SpiceDSKDescr, ndarray, ndarray, bool]:
    """
    Compute a ray-surface intercept using data provided by
    multiple loaded DSK segments. Return information about
    the source of the data defining the surface on which the
    intercept was found: DSK handle, DLA and DSK descriptors,
    and DSK data type-dependent parameters.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dskxsi_c.html

    :param pri: Data prioritization flag.
    :param target: Target body name.
    :param srflst: Surface ID list.
    :param et: Epoch, expressed as seconds past J2000 TDB.
    :param fixref: Name of target body-fixed reference frame.
    :param vertex: Vertex of ray.
    :param raydir: Direction vector of ray.
    :return: Intercept point, Handle of segment contributing surface data, DLADSC, DSKDSC, Double precision component of source info, Integer component of source info
    """
    pri = ctypes.c_int(pri)
    target = stypes.string_to_char_p(target)
    nsurf = ctypes.c_int(len(srflst))
    srflst = stypes.to_int_vector(srflst)
    et = ctypes.c_double(et)
    fixref = stypes.string_to_char_p(fixref)
    vertex = stypes.to_double_vector(vertex)
    raydir = stypes.to_double_vector(raydir)
    maxd = ctypes.c_int(1)
    maxi = ctypes.c_int(1)
    xpt = stypes.empty_double_vector(3)
    handle = ctypes.c_int(0)
    dladsc = stypes.SpiceDLADescr()
    dskdsc = stypes.SpiceDSKDescr()
    dc = stypes.empty_double_vector(1)
    ic = stypes.empty_int_vector(1)
    found = ctypes.c_int()
    libspice.dskxsi_c(
        pri,
        target,
        nsurf,
        srflst,
        et,
        fixref,
        vertex,
        raydir,
        maxd,
        maxi,
        xpt,
        handle,
        dladsc,
        dskdsc,
        dc,
        ic,
        found,
    )
    return (
        stypes.c_vector_to_python(xpt),
        handle.value,
        dladsc,
        dskdsc,
        stypes.c_vector_to_python(dc),
        stypes.c_vector_to_python(ic),
        bool(found.value),
    )


@spice_error_check
def dskxv(
    pri: bool,
    target: str,
    srflst: Sequence[int],
    et: float,
    fixref: str,
    vtxarr: Sequence[ndarray],
    dirarr: Sequence[ndarray],
) -> Tuple[ndarray, ndarray]:
    """
    Compute ray-surface intercepts for a set of rays, using data
    provided by multiple loaded DSK segments.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dskxv_c.html

    :param pri: Data prioritization flag.
    :param target: Target body name.
    :param srflst: Surface ID list.
    :param et: Epoch, expressed as seconds past J2000 TDB.
    :param fixref: Name of target body-fixed reference frame.
    :param vtxarr: Array of vertices of rays.
    :param dirarr: Array of direction vectors of rays.
    :return: Intercept point array and Found flag array.
    """
    pri = ctypes.c_int(pri)
    target = stypes.string_to_char_p(target)
    nsurf = ctypes.c_int(len(srflst))
    srflst = stypes.to_int_vector(srflst)
    et = ctypes.c_double(et)
    fixref = stypes.string_to_char_p(fixref)
    nray = ctypes.c_int(len(vtxarr))
    vtxarr = stypes.to_double_matrix(vtxarr)
    dirarr = stypes.to_double_matrix(dirarr)
    xptarr = stypes.empty_double_matrix(y=nray)
    fndarr = stypes.empty_int_vector(nray)
    libspice.dskxv_c(
        pri, target, nsurf, srflst, et, fixref, nray, vtxarr, dirarr, xptarr, fndarr
    )
    return stypes.c_matrix_to_numpy(xptarr), stypes.c_vector_to_python(fndarr)


@spice_error_check
def dskz02(handle: int, dladsc: SpiceDLADescr) -> Tuple[int, int]:
    """
    Return plate model size parameters---plate count and
    vertex count---for a type 2 DSK segment.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dskz02_c.html

    :param handle: DSK file handle.
    :param dladsc: DLA descriptor.
    :return: Number of vertices, Number of plates.
    """
    handle = ctypes.c_int(handle)
    nv = ctypes.c_int()
    np = ctypes.c_int()
    libspice.dskz02_c(handle, dladsc, ctypes.byref(nv), ctypes.byref(np))
    return nv.value, np.value


@spice_error_check
def dsphdr(x: float, y: float, z: float) -> ndarray:
    """
    This routine computes the Jacobian of the transformation from
    rectangular to spherical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dsphdr_c.html


    :param x: X-coordinate of point.
    :param y: Y-coordinate of point.
    :param z: Z-coordinate of point.
    :return: Matrix of partial derivatives.
    """
    x = ctypes.c_double(x)
    y = ctypes.c_double(y)
    z = ctypes.c_double(z)
    jacobi = stypes.empty_double_matrix()
    libspice.dsphdr_c(x, y, z, jacobi)
    return stypes.c_matrix_to_numpy(jacobi)


@spice_error_check
@spice_found_exception_thrower
def dtpool(name: str) -> Tuple[int, str, bool]:
    """
    Return the data about a kernel pool variable.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dtpool_c.html

    :param name: Name of the variable whose value is to be returned.
    :return:
            Number of values returned for name,
            Type of the variable "C", "N", or "X".
    """
    name = stypes.string_to_char_p(name)
    found = ctypes.c_int()
    n = ctypes.c_int()
    typeout = ctypes.c_char()
    libspice.dtpool_c(name, ctypes.byref(found), ctypes.byref(n), ctypes.byref(typeout))
    return n.value, stypes.to_python_string(typeout.value), bool(found.value)


@spice_error_check
def ducrss(s1: ndarray, s2: ndarray) -> ndarray:
    """
    Compute the unit vector parallel to the cross product of
    two 3-dimensional vectors and the derivative of this unit vector.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ducrss_c.html

    :param s1: Left hand state for cross product and derivative.
    :param s2: Right hand state for cross product and derivative.
    :return: Unit vector and derivative of the cross product.
    """
    assert len(s1) == 6 and len(s2) == 6
    s1 = stypes.to_double_vector(s1)
    s2 = stypes.to_double_vector(s2)
    sout = stypes.empty_double_vector(6)
    libspice.ducrss_c(s1, s2, sout)
    return stypes.c_vector_to_python(sout)


@spice_error_check
def dvcrss(s1: ndarray, s2: ndarray) -> ndarray:
    """
    Compute the cross product of two 3-dimensional vectors
    and the derivative of this cross product.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dvcrss_c.html

    :param s1: Left hand state for cross product and derivative.
    :param s2: Right hand state for cross product and derivative.
    :return: State associated with cross product of positions.
    """
    assert len(s1) == 6 and len(s2) == 6
    s1 = stypes.to_double_vector(s1)
    s2 = stypes.to_double_vector(s2)
    sout = stypes.empty_double_vector(6)
    libspice.dvcrss_c(s1, s2, sout)
    return stypes.c_vector_to_python(sout)


@spice_error_check
def dvdot(s1: Sequence[float], s2: Sequence[float]) -> float:
    """
    Compute the derivative of the dot product of two double
    precision position vectors.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dvdot_c.html

    :param s1: First state vector in the dot product.
    :param s2: Second state vector in the dot product.
    :return: The derivative of the dot product.
    """
    assert len(s1) == 6 and len(s2) == 6
    s1 = stypes.to_double_vector(s1)
    s2 = stypes.to_double_vector(s2)
    return libspice.dvdot_c(s1, s2)


@spice_error_check
def dvhat(s1: ndarray) -> ndarray:
    """
    Find the unit vector corresponding to a state vector and the
    derivative of the unit vector.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dvhat_c.html

    :param s1: State to be normalized.
    :return: Unit vector s1 / abs(s1), and its time derivative.
    """
    assert len(s1) == 6
    s1 = stypes.to_double_vector(s1)
    sout = stypes.empty_double_vector(6)
    libspice.dvhat_c(s1, sout)
    return stypes.c_vector_to_python(sout)


@spice_error_check
def dvnorm(state: ndarray) -> float:
    """
    Function to calculate the derivative of the norm of a 3-vector.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dvnorm_c.html

    :param state:
                A 6-vector composed of three coordinates and their derivatives.
    :return: The derivative of the norm of a 3-vector.
    """
    assert len(state) == 6
    state = stypes.to_double_vector(state)
    return libspice.dvnorm_c(state)


@spice_error_check
def dvpool(name: str) -> None:
    """
    Delete a variable from the kernel pool.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dvpool_c.html

    :param name: Name of the kernel variable to be deleted.
    """
    name = stypes.string_to_char_p(name)
    libspice.dvpool_c(name)


@spice_error_check
def dvsep(s1: ndarray, s2: ndarray) -> float:
    """
    Calculate the time derivative of the separation angle between
    two input states, S1 and S2.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dvsep_c.html

    :param s1: State vector of the first body.
    :param s2: State vector of the second body.
    :return: The time derivative of the angular separation between S1 and S2.
    """
    assert len(s1) == 6 and len(s2) == 6
    s1 = stypes.to_double_vector(s1)
    s2 = stypes.to_double_vector(s2)
    return libspice.dvsep_c(s1, s2)


################################################################################
# E


@spice_error_check
def edlimb(
    a: float,
    b: float,
    c: float,
    viewpt: Union[Iterable[Union[float, float]], Iterable[float]],
) -> Ellipse:
    """
    Find the limb of a triaxial ellipsoid, viewed from a specified point.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/edlimb_c.html

    :param a: Length of ellipsoid semi-axis lying on the x-axis.
    :param b: Length of ellipsoid semi-axis lying on the y-axis.
    :param c: Length of ellipsoid semi-axis lying on the z-axis.
    :param viewpt: Location of viewing point.
    :return: Limb of ellipsoid as seen from viewing point.
    """
    limb = stypes.Ellipse()
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    viewpt = stypes.to_double_vector(viewpt)
    libspice.edlimb_c(a, b, c, viewpt, ctypes.byref(limb))
    return limb


@spice_error_check
def ednmpt(a: float, b: float, c: float, normal: ndarray) -> ndarray:
    """
    Return the unique point on an ellipsoid's surface where the
    outward normal direction is a given vector.

    :param a: Length of the ellipsoid semi-axis along the X-axis.
    :param b: Length of the ellipsoid semi-axis along the Y-axis.
    :param c: Length of the ellipsoid semi-axis along the Z-axis.
    :param normal: Outward normal direction.
    :return: Point where outward normal is parallel to `normal'.
    """
    _a = ctypes.c_double(a)
    _b = ctypes.c_double(b)
    _c = ctypes.c_double(c)
    _normal = stypes.to_double_vector(normal)
    _o = stypes.empty_double_vector(3)
    libspice.ednmpt_c(_a, _b, _c, _normal, _o)
    return stypes.c_vector_to_python(_o)


@spice_error_check
def edpnt(p: ndarray, a: float, b: float, c: float) -> ndarray:
    """
    Scale a point so that it lies on the surface of a specified
    triaxial ellipsoid that is centered at the origin and aligned
    with the Cartesian coordinate axes.

    :param p: A point in three-dimensional space.
    :param a: Semi-axis length in the X direction.
    :param b: Semi-axis length in the Y direction.
    :param c: Semi-axis length in the Z direction.
    :return: Point on ellipsoid.
    """
    _p = stypes.to_double_vector(p)
    _a = ctypes.c_double(a)
    _b = ctypes.c_double(b)
    _c = ctypes.c_double(c)
    _o = stypes.empty_double_vector(3)
    libspice.edpnt_c(_p, _a, _b, _c, _o)
    return stypes.c_vector_to_python(_o)


@spice_error_check
def edterm(
    trmtyp: str,
    source: str,
    target: str,
    et: float,
    fixref: str,
    abcorr: str,
    obsrvr: str,
    npts: int,
) -> Tuple[float, ndarray, ndarray]:
    """
    Compute a set of points on the umbral or penumbral terminator of
    a specified target body, where the target shape is modeled as an
    ellipsoid.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/edterm_c.html

    :param trmtyp: Terminator type.
    :param source: Light source.
    :param target: Target body.
    :param et: Observation epoch.
    :param fixref: Body-fixed frame associated with target.
    :param abcorr: Aberration correction.
    :param obsrvr: Observer.
    :param npts: Number of points in terminator set.
    :return:
            Epoch associated with target center,
            Position of observer in body-fixed frame,
            Terminator point set.
    """
    trmtyp = stypes.string_to_char_p(trmtyp)
    source = stypes.string_to_char_p(source)
    target = stypes.string_to_char_p(target)
    et = ctypes.c_double(et)
    fixref = stypes.string_to_char_p(fixref)
    abcorr = stypes.string_to_char_p(abcorr)
    obsrvr = stypes.string_to_char_p(obsrvr)
    trgepc = ctypes.c_double()
    obspos = stypes.empty_double_vector(3)
    trmpts = stypes.empty_double_matrix(x=3, y=npts)
    npts = ctypes.c_int(npts)
    libspice.edterm_c(
        trmtyp,
        source,
        target,
        et,
        fixref,
        abcorr,
        obsrvr,
        npts,
        ctypes.byref(trgepc),
        obspos,
        trmpts,
    )
    return (
        trgepc.value,
        stypes.c_vector_to_python(obspos),
        stypes.c_matrix_to_numpy(trmpts),
    )


@spice_error_check
def ekacec(
    handle: int,
    segno: int,
    recno: int,
    column: str,
    nvals: int,
    cvals: Iterable[str],
    isnull: bool,
) -> None:
    """
    Add data to a character column in a specified EK record.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekacec_c.html

    :param handle: EK file handle.
    :param segno: Index of segment containing record.
    :param recno: Record to which data is to be added.
    :param column: Column name.
    :param nvals: Number of values to add to column.
    :param cvals: Character values to add to column.
    :param isnull: Flag indicating whether column entry is null.
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.string_to_char_p(column)
    nvals = ctypes.c_int(nvals)
    vallen = ctypes.c_int(len(max(cvals, key=len)) + 1)
    cvals = stypes.list_to_char_array_ptr(cvals)
    isnull = ctypes.c_int(isnull)
    libspice.ekacec_c(handle, segno, recno, column, nvals, vallen, cvals, isnull)


@spice_error_check
def ekaced(
    handle: int,
    segno: int,
    recno: int,
    column: str,
    nvals: int,
    dvals: Union[ndarray, Iterable[float]],
    isnull: bool,
) -> None:
    """
    Add data to an double precision column in a specified EK record.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekaced_c.html

    :param handle: EK file handle.
    :param segno: Index of segment containing record.
    :param recno: Record to which data is to be added.
    :param column: Column name.
    :param nvals: Number of values to add to column.
    :param dvals: Double precision values to add to column.
    :param isnull: Flag indicating whether column entry is null.
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.string_to_char_p(column)
    nvals = ctypes.c_int(nvals)
    dvals = stypes.to_double_vector(dvals)
    isnull = ctypes.c_int(isnull)
    libspice.ekaced_c(handle, segno, recno, column, nvals, dvals, isnull)


@spice_error_check
def ekacei(
    handle: int,
    segno: int,
    recno: int,
    column: str,
    nvals: int,
    ivals: Union[ndarray, Iterable[int]],
    isnull: bool,
) -> None:
    """
    Add data to an integer column in a specified EK record.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekacei_c.html

    :param handle: EK file handle.
    :param segno: Index of segment containing record.
    :param recno: Record to which data is to be added.
    :param column: Column name.
    :param nvals: Number of values to add to column.
    :param ivals: Integer values to add to column.
    :param isnull: Flag indicating whether column entry is null.
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.string_to_char_p(column)
    nvals = ctypes.c_int(nvals)
    ivals = stypes.to_int_vector(ivals)
    isnull = ctypes.c_int(isnull)
    libspice.ekacei_c(handle, segno, recno, column, nvals, ivals, isnull)


@spice_error_check
def ekaclc(
    handle: int,
    segno: int,
    column: str,
    vallen: int,
    cvals: Iterable[str],
    entszs: Union[ndarray, Iterable[int]],
    nlflgs: Iterable[bool],
    rcptrs: ndarray,
    wkindx: Union[ndarray, Iterable[int]],
) -> ndarray:
    """
    Add an entire character column to an EK segment.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekaclc_c.html

    :param handle: EK file handle.
    :param segno: Number of segment to add column to.
    :param column: Column name.
    :param vallen: Length of character values.
    :param cvals: Character values to add to column.
    :param entszs: Array of sizes of column entries.
    :param nlflgs: Array of null flags for column entries.
    :param rcptrs: Record pointers for segment.
    :param wkindx: Work space for column index.
    :return: Work space for column index.
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    column = stypes.string_to_char_p(column)
    vallen = ctypes.c_int(vallen)
    cvals = stypes.list_to_char_array_ptr(cvals)
    entszs = stypes.to_int_vector(entszs)
    nlflgs = stypes.to_int_vector(nlflgs)
    rcptrs = stypes.to_int_vector(rcptrs)
    wkindx = stypes.to_int_vector(wkindx)
    libspice.ekaclc_c(
        handle, segno, column, vallen, cvals, entszs, nlflgs, rcptrs, wkindx
    )
    return stypes.c_vector_to_python(wkindx)


@spice_error_check
def ekacld(
    handle: int,
    segno: int,
    column: str,
    dvals: Union[ndarray, Iterable[float]],
    entszs: Union[ndarray, Iterable[int]],
    nlflgs: Iterable[bool],
    rcptrs: ndarray,
    wkindx: Union[ndarray, Iterable[int]],
) -> ndarray:
    """
    Add an entire double precision column to an EK segment.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekacld_c.html

    :param handle: EK file handle.
    :param segno: Number of segment to add column to.
    :param column: Column name.
    :param dvals: Double precision values to add to column.
    :param entszs: Array of sizes of column entries.
    :param nlflgs: Array of null flags for column entries.
    :param rcptrs: Record pointers for segment.
    :param wkindx: Work space for column index.
    :return: Work space for column index.
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    column = stypes.string_to_char_p(column)
    dvals = stypes.to_double_vector(dvals)
    entszs = stypes.to_int_vector(entszs)
    nlflgs = stypes.to_int_vector(nlflgs)
    rcptrs = stypes.to_int_vector(rcptrs)
    wkindx = stypes.to_int_vector(wkindx)
    libspice.ekacld_c(handle, segno, column, dvals, entszs, nlflgs, rcptrs, wkindx)
    return stypes.c_vector_to_python(wkindx)


@spice_error_check
def ekacli(
    handle: int,
    segno: int,
    column: str,
    ivals: Union[ndarray, Iterable[int]],
    entszs: Union[ndarray, Iterable[int]],
    nlflgs: Iterable[bool],
    rcptrs: ndarray,
    wkindx: Union[ndarray, Iterable[int]],
) -> ndarray:
    """
    Add an entire integer column to an EK segment.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekacli_c.html

    :param handle: EK file handle.
    :param segno: Number of segment to add column to.
    :param column: Column name.
    :param ivals: Integer values to add to column.
    :param entszs: Array of sizes of column entries.
    :param nlflgs: Array of null flags for column entries.
    :param rcptrs: Record pointers for segment.
    :param wkindx: Work space for column index.
    :return: Work space for column index.
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    column = stypes.string_to_char_p(column)
    ivals = stypes.to_int_vector(ivals)
    entszs = stypes.to_int_vector(entszs)
    nlflgs = stypes.to_int_vector(nlflgs)
    rcptrs = stypes.to_int_vector(rcptrs)
    wkindx = stypes.to_int_vector(wkindx)
    libspice.ekacli_c(handle, segno, column, ivals, entszs, nlflgs, rcptrs, wkindx)
    return stypes.c_vector_to_python(wkindx)


@spice_error_check
def ekappr(handle: int, segno: int) -> int:
    """
    Append a new, empty record at the end of a specified E-kernel segment.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekappr_c.html

    :param handle: File handle.
    :param segno: Segment number.
    :return: Number of appended record.
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int()
    libspice.ekappr_c(handle, segno, ctypes.byref(recno))
    return recno.value


@spice_error_check
def ekbseg(
    handle: int, tabnam: str, cnames: Sequence[str], decls: Sequence[str]
) -> int:
    """
    Start a new segment in an E-kernel.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekbseg_c.html

    :param handle: File handle.
    :param tabnam: Table name.
    :param cnames: Names of columns.
    :param decls: Declarations of columns.
    :return: Segment number.
    """
    handle = ctypes.c_int(handle)
    tabnam = stypes.string_to_char_p(tabnam)
    ncols = ctypes.c_int(len(cnames))
    cnmlen = ctypes.c_int(
        len(max(cnames, key=len)) + 1
    )  # needs to be len(name)+1 ie 'c1' to 3 for ekbseg do not fail
    cnames = stypes.list_to_char_array_ptr(cnames)
    declen = ctypes.c_int(len(max(decls, key=len)) + 1)
    decls = stypes.list_to_char_array_ptr(decls)
    segno = ctypes.c_int()
    libspice.ekbseg_c(
        handle, tabnam, ncols, cnmlen, cnames, declen, decls, ctypes.byref(segno)
    )
    return segno.value


@spice_error_check
def ekccnt(table: str) -> int:
    """
    Return the number of distinct columns in a specified,
    currently loaded table.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekccnt_c.html

    :param table: Name of table.
    :return: Count of distinct, currently loaded columns.
    """
    table = stypes.string_to_char_p(table)
    ccount = ctypes.c_int()
    libspice.ekccnt_c(table, ctypes.byref(ccount))
    return ccount.value


@spice_error_check
def ekcii(
    table: str, cindex: int, lenout: int = _default_len_out
) -> Tuple[str, SpiceEKAttDsc]:
    """
    Return attribute information about a column belonging to a loaded
    EK table, specifying the column by table and index.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekcii_c.html

    :param table: Name of table containing column.
    :param cindex: Index of column whose attributes are to be found.
    :param lenout: Maximum allowed length of column name.
    :return: Name of column, Column attribute descriptor.
    """
    table = stypes.string_to_char_p(table)
    cindex = ctypes.c_int(cindex)
    lenout = ctypes.c_int(lenout)
    column = stypes.string_to_char_p(lenout)
    attdsc = stypes.SpiceEKAttDsc()
    libspice.ekcii_c(table, cindex, lenout, column, ctypes.byref(attdsc))
    return stypes.to_python_string(column), attdsc


@spice_error_check
def ekcls(handle: int) -> None:
    """
    Close an E-kernel.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekcls_c.html

    :param handle: EK file handle.
    """
    handle = ctypes.c_int(handle)
    libspice.ekcls_c(handle)


@spice_error_check
def ekdelr(handle: int, segno: int, recno: int) -> None:
    """
    Delete a specified record from a specified E-kernel segment.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekdelr_c.html

    :param handle: File handle.
    :param segno: Segment number.
    :param recno: Record number.
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    libspice.ekdelr_c(handle, segno, recno)


@spice_error_check
def ekffld(handle: int, segno: int, rcptrs: ndarray) -> None:
    """
    Complete a fast write operation on a new E-kernel segment.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekffld_c.html

    :param handle: File handle.
    :param segno: Segment number.
    :param rcptrs: Record pointers.
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    rcptrs = stypes.to_int_vector(rcptrs)
    libspice.ekffld_c(handle, segno, ctypes.cast(rcptrs, ctypes.POINTER(ctypes.c_int)))


@spice_error_check
def ekfind(query: str, lenout: int = _default_len_out) -> Tuple[int, int, str]:
    """
    Find E-kernel data that satisfy a set of constraints.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekfind_c.html

    :param query: Query specifying data to be found.
    :param lenout: Declared length of output error message string.
    :return:
            Number of matching rows,
            Flag indicating whether query parsed correctly,
            Parse error description.
    """
    query = stypes.string_to_char_p(query)
    lenout = ctypes.c_int(lenout)
    nmrows = ctypes.c_int()
    error = ctypes.c_int()
    errmsg = stypes.string_to_char_p(lenout)
    libspice.ekfind_c(query, lenout, ctypes.byref(nmrows), ctypes.byref(error), errmsg)
    return nmrows.value, error.value, stypes.to_python_string(errmsg)


@spice_error_check
@spice_found_exception_thrower
def ekgc(
    selidx: int, row: int, element: int, lenout: int = _default_len_out
) -> Tuple[str, int, bool]:
    """
    Return an element of an entry in a column of character type in a specified
    row.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekgc_c.html

    :param selidx: Index of parent column in SELECT clause.
    :param row: Row to fetch from.
    :param element: Index of element, within column entry, to fetch.
    :param lenout: Maximum length of column element.
    :return:
            Character string element of column entry,
            Flag indicating whether column entry was null.
    """
    selidx = ctypes.c_int(selidx)
    row = ctypes.c_int(row)
    element = ctypes.c_int(element)
    lenout = ctypes.c_int(lenout)
    null = ctypes.c_int()
    found = ctypes.c_int()
    cdata = stypes.string_to_char_p(lenout)
    libspice.ekgc_c(
        selidx, row, element, lenout, cdata, ctypes.byref(null), ctypes.byref(found)
    )
    return stypes.to_python_string(cdata), null.value, bool(found.value)


@spice_error_check
@spice_found_exception_thrower
def ekgd(selidx: int, row: int, element: int) -> Tuple[float, int, bool]:
    """
    Return an element of an entry in a column of double precision type in a
    specified row.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekgd_c.html

    :param selidx: Index of parent column in SELECT clause.
    :param row: Row to fetch from.
    :param element: Index of element, within column entry, to fetch.
    :return:
            Double precision element of column entry,
            Flag indicating whether column entry was null.
    """
    selidx = ctypes.c_int(selidx)
    row = ctypes.c_int(row)
    element = ctypes.c_int(element)
    ddata = ctypes.c_double()
    null = ctypes.c_int()
    found = ctypes.c_int()
    libspice.ekgd_c(
        selidx,
        row,
        element,
        ctypes.byref(ddata),
        ctypes.byref(null),
        ctypes.byref(found),
    )
    return ddata.value, null.value, bool(found.value)


@spice_error_check
@spice_found_exception_thrower
def ekgi(selidx: int, row: int, element: int) -> Tuple[int, int, bool]:
    """
    Return an element of an entry in a column of integer type in a specified
    row.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekgi_c.html

    :param selidx: Index of parent column in SELECT clause.
    :param row: Row to fetch from.
    :param element: Index of element, within column entry, to fetch.
    :return:
            Integer element of column entry,
            Flag indicating whether column entry was null.
    """
    selidx = ctypes.c_int(selidx)
    row = ctypes.c_int(row)
    element = ctypes.c_int(element)
    idata = ctypes.c_int()
    null = ctypes.c_int()
    found = ctypes.c_int()
    libspice.ekgi_c(
        selidx,
        row,
        element,
        ctypes.byref(idata),
        ctypes.byref(null),
        ctypes.byref(found),
    )
    return idata.value, null.value, bool(found.value)


@spice_error_check
def ekifld(
    handle: int,
    tabnam: str,
    ncols: int,
    nrows: int,
    cnmlen: int,
    cnames: Iterable[str],
    declen: int,
    decls: Iterable[str],
) -> Tuple[int, ndarray]:
    """
    Initialize a new E-kernel segment to allow fast writing.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekifld_c.html

    :param handle: File handle.
    :param tabnam: Table name.
    :param ncols: Number of columns in the segment.
    :param nrows: Number of rows in the segment.
    :param cnmlen: Length of names in in column name array.
    :param cnames: Names of columns.
    :param declen: Length of declaration strings in declaration array.
    :param decls: Declarations of columns.
    :return: Segment number, Array of record pointers.
    """
    handle = ctypes.c_int(handle)
    tabnam = stypes.string_to_char_p(tabnam)
    ncols = ctypes.c_int(ncols)
    nrows = ctypes.c_int(nrows)
    cnmlen = ctypes.c_int(cnmlen)
    cnames = stypes.list_to_char_array(cnames)
    declen = ctypes.c_int(declen)
    recptrs = stypes.empty_int_vector(nrows)
    decls = stypes.list_to_char_array(decls)
    segno = ctypes.c_int()
    libspice.ekifld_c(
        handle,
        tabnam,
        ncols,
        nrows,
        cnmlen,
        cnames,
        declen,
        decls,
        ctypes.byref(segno),
        recptrs,
    )
    return segno.value, stypes.c_vector_to_python(recptrs)


@spice_error_check
def ekinsr(handle: int, segno: int, recno: int) -> None:
    """
    Add a new, empty record to a specified E-kernel segment at a specified
    index.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekinsr_c.html

    :param handle: File handle.
    :param segno: Segment number.
    :param recno: Record number.
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    libspice.ekinsr_c(handle, segno, recno)


@spice_error_check
def eklef(fname: str) -> int:
    """
    Load an EK file, making it accessible to the EK readers.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/eklef_c.html

    :param fname: Name of EK file to load.
    :return: File handle of loaded EK file.
    """
    fname = stypes.string_to_char_p(fname)
    handle = ctypes.c_int()
    libspice.eklef_c(fname, ctypes.byref(handle))
    return handle.value


@spice_error_check
def eknelt(selidx: int, row: int) -> int:
    """
    Return the number of elements in a specified column entry in
    the current row.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/eknelt_c.html

    :param selidx: Index of parent column in SELECT clause.
    :param row: Row containing element.
    :return: The number of elements in entry in current row.
    """
    selidx = ctypes.c_int(selidx)
    row = ctypes.c_int(row)
    return libspice.eknelt_c(selidx, row)


@spice_error_check
def eknseg(handle: int) -> int:
    """
    Return the number of segments in a specified EK.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/eknseg_c.html

    :param handle: EK file handle.
    :return: The number of segments in the specified E-kernel.
    """
    handle = ctypes.c_int(handle)
    return libspice.eknseg_c(handle)


@spice_error_check
def ekntab() -> int:
    """
    Return the number of loaded EK tables.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekntab_c.html

    :return: The number of loaded EK tables.
    """
    n = ctypes.c_int(0)
    libspice.ekntab_c(ctypes.byref(n))
    return n.value


@spice_error_check
def ekopn(fname: str, ifname: str, ncomch: int) -> int:
    """
    Open a new E-kernel file and prepare the file for writing.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekopn_c.html

    :param fname: Name of EK file.
    :param ifname: Internal file name.
    :param ncomch: The number of characters to reserve for comments.
    :return: Handle attached to new EK file.
    """
    fname = stypes.string_to_char_p(fname)
    ifname = stypes.string_to_char_p(ifname)
    ncomch = ctypes.c_int(ncomch)
    handle = ctypes.c_int()
    libspice.ekopn_c(fname, ifname, ncomch, ctypes.byref(handle))
    return handle.value


@spice_error_check
def ekopr(fname: str) -> int:
    """
    Open an existing E-kernel file for reading.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekopr_c.html

    :param fname: Name of EK file.
    :return: Handle attached to EK file.
    """
    fname = stypes.string_to_char_p(fname)
    handle = ctypes.c_int()
    libspice.ekopr_c(fname, ctypes.byref(handle))
    return handle.value


@spice_error_check
def ekops() -> int:
    """
    Open a scratch (temporary) E-kernel file and prepare the file
    for writing.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekops_c.html

    :return: Handle attached to new EK file.
    """
    handle = ctypes.c_int()
    libspice.ekops_c(ctypes.byref(handle))
    return handle.value


@spice_error_check
def ekopw(fname: str) -> int:
    """
    Open an existing E-kernel file for writing.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekopw_c.html

    :param fname: Name of EK file.
    :return: Handle attached to EK file.
    """
    fname = stypes.string_to_char_p(fname)
    handle = ctypes.c_int()
    libspice.ekopw_c(fname, ctypes.byref(handle))
    return handle.value


@spice_error_check
def ekpsel(
    query: str, msglen: int, tablen: int, collen: int
) -> Tuple[
    int, ndarray, ndarray, ndarray, ndarray, Iterable[str], Iterable[str], int, str
]:
    """
    Parse the SELECT clause of an EK query, returning full particulars
    concerning each selected item.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekpsel_c.html
    note: oddly docs at url are incomplete/incorrect.

    :param query: EK query.
    :param msglen: Available space in the output error message string.
    :param tablen: UNKNOWN? Length of Table?
    :param collen: UNKOWN? Length of Column?
    :return:
            Number of items in SELECT clause of query,
            Begin positions of expressions in SELECT clause,
            End positions of expressions in SELECT clause,
            Data types of expressions,
            Classes of expressions,
            Names of tables qualifying SELECT columns,
            Names of columns in SELECT clause of query,
            Error flag,
            Parse error message.
    """
    query = stypes.string_to_char_p(query)
    msglen = ctypes.c_int(msglen)
    tablen = ctypes.c_int(tablen)
    collen = ctypes.c_int(collen)
    n = ctypes.c_int()
    xbegs = stypes.empty_int_vector(_SPICE_EK_MAXQSEL)
    xends = stypes.empty_int_vector(_SPICE_EK_MAXQSEL)
    xtypes = stypes.empty_int_vector(_SPICE_EK_MAXQSEL)
    xclass = stypes.empty_int_vector(_SPICE_EK_MAXQSEL)
    tabs = stypes.empty_char_array(y_len=_SPICE_EK_MAXQSEL, x_len=tablen)
    cols = stypes.empty_char_array(y_len=_SPICE_EK_MAXQSEL, x_len=collen)
    error = ctypes.c_int()
    errmsg = stypes.string_to_char_p(msglen)
    libspice.ekpsel_c(
        query,
        msglen,
        tablen,
        collen,
        ctypes.byref(n),
        xbegs,
        xends,
        xtypes,
        xclass,
        ctypes.byref(tabs),
        ctypes.byref(cols),
        ctypes.byref(error),
        errmsg,
    )
    return (
        n.value,
        stypes.c_vector_to_python(xbegs)[: n.value],
        stypes.c_vector_to_python(xends)[: n.value],
        stypes.c_vector_to_python(xtypes)[: n.value],
        stypes.c_vector_to_python(xclass)[: n.value],
        stypes.c_vector_to_python(tabs)[: n.value],
        stypes.c_vector_to_python(cols)[: n.value],
        error.value,
        stypes.to_python_string(errmsg),
    )


@spice_error_check
def ekrcec(
    handle: int,
    segno: int,
    recno: int,
    column: str,
    lenout: int,
    nelts: int = _SPICE_EK_EKRCEX_ROOM_DEFAULT,
) -> Tuple[int, Iterable[str], bool]:
    """
    Read data from a character column in a specified EK record.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekrcec_c.html

    :param handle: Handle attached to EK file.
    :param segno: Index of segment containing record.
    :param recno: Record from which data is to be read.
    :param column: Column name.
    :param lenout: Maximum length of output strings.
    :param nelts: Number of elements to allow for (default=100)
    :return:
            Number of values in column entry,
            Character values in column entry,
            Flag indicating whether column entry is null.
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.string_to_char_p(column)
    lenout = ctypes.c_int(lenout)
    nvals = ctypes.c_int()
    cvals = stypes.empty_char_array(y_len=nelts, x_len=lenout)
    isnull = ctypes.c_int()
    libspice.ekrcec_c(
        handle,
        segno,
        recno,
        column,
        lenout,
        ctypes.byref(nvals),
        ctypes.byref(cvals),
        ctypes.byref(isnull),
    )
    assert failed() or (nvals.value <= nelts)
    return (
        nvals.value,
        stypes.c_vector_to_python(cvals)[: nvals.value],
        bool(isnull.value),
    )


@spice_error_check
def ekrced(
    handle: int,
    segno: int,
    recno: int,
    column: str,
    nelts: int = _SPICE_EK_EKRCEX_ROOM_DEFAULT,
) -> Tuple[int, ndarray, bool]:
    """
    Read data from a double precision column in a specified EK record.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekrced_c.html

    :param handle: Handle attached to EK file.
    :param segno: Index of segment containing record.
    :param recno: Record from which data is to be read.
    :param column: Column name.
    :param nelts: room for data default 100
    :return:
            Number of values in column entry,
            Float values in column entry,
            Flag indicating whether column entry is null.
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.string_to_char_p(column)
    nvals = ctypes.c_int(0)
    dvals = stypes.empty_double_vector(nelts)
    isnull = ctypes.c_int()
    libspice.ekrced_c(
        handle, segno, recno, column, ctypes.byref(nvals), dvals, ctypes.byref(isnull)
    )
    assert failed() or (nvals.value <= nelts)
    return (
        nvals.value,
        stypes.c_vector_to_python(dvals)[: nvals.value],
        bool(isnull.value),
    )


@spice_error_check
def ekrcei(
    handle: int,
    segno: int,
    recno: int,
    column: str,
    nelts: int = _SPICE_EK_EKRCEX_ROOM_DEFAULT,
) -> Tuple[int, ndarray, bool]:
    """
    Read data from an integer column in a specified EK record.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekrcei_c.html

    :param handle: Handle attached to EK file.
    :param segno: Index of segment containing record.
    :param recno: Record from which data is to be read.
    :param column: Column name.
    :param nelts: room for data default 100
    :return:
            Number of values in column entry,
            Integer values in column entry,
            Flag indicating whether column entry is null.
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.string_to_char_p(column)
    nvals = ctypes.c_int()
    ivals = stypes.empty_int_vector(nelts)
    isnull = ctypes.c_int()
    libspice.ekrcei_c(
        handle, segno, recno, column, ctypes.byref(nvals), ivals, ctypes.byref(isnull)
    )
    assert failed() or (nvals.value <= nelts)
    return (
        nvals.value,
        stypes.c_vector_to_python(ivals)[: nvals.value],
        bool(isnull.value),
    )


@spice_error_check
def ekssum(handle: int, segno: int) -> SpiceEKSegSum:
    """
    Return summary information for a specified segment in a specified EK.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekssum_c.html

    :param handle: Handle of EK.
    :param segno: Number of segment to be summarized.
    :return: EK segment summary.
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    segsum = stypes.SpiceEKSegSum()
    libspice.ekssum_c(handle, segno, ctypes.byref(segsum))
    return segsum


@spice_error_check
def ektnam(n: int, lenout: int = _default_len_out) -> str:
    """
    Return the name of a specified, loaded table.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ektnam_c.html

    :param n: Index of table.
    :param lenout: Maximum table name length.
    :return: Name of table.
    """
    n = ctypes.c_int(n)
    lenout = ctypes.c_int(lenout)
    table = stypes.string_to_char_p(lenout)
    libspice.ektnam_c(n, lenout, table)
    return stypes.to_python_string(table)


@spice_error_check
def ekucec(
    handle: int,
    segno: int,
    recno: int,
    column: str,
    nvals: int,
    cvals: Iterable[str],
    isnull: bool,
) -> None:
    """
    Update a character column entry in a specified EK record.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekucec_c.html

    :param handle: EK file handle.
    :param segno: Index of segment containing record.
    :param recno: Record to which data is to be updated.
    :param column: Column name.
    :param nvals: Number of values in new column entry.
    :param cvals: Character values comprising new column entry.
    :param isnull: Flag indicating whether column entry is null.
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.string_to_char_p(column)
    nvals = ctypes.c_int(nvals)
    vallen = ctypes.c_int(len(max(cvals, key=len)) + 1)
    cvals = stypes.list_to_char_array_ptr(cvals, x_len=vallen)
    isnull = ctypes.c_int(isnull)
    libspice.ekucec_c(handle, segno, recno, column, nvals, vallen, cvals, isnull)


@spice_error_check
def ekuced(
    handle: int,
    segno: int,
    recno: int,
    column: str,
    nvals: int,
    dvals: Union[ndarray, Iterable[float]],
    isnull: bool,
) -> None:
    """
    Update a double precision column entry in a specified EK record.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekuced_c.html

    :param handle: EK file handle.
    :param segno: Index of segment containing record.
    :param recno: Record to which data is to be updated.
    :param column: Column name.
    :param nvals: Number of values in new column entry.
    :param dvals: Double precision values comprising new column entry.
    :param isnull: Flag indicating whether column entry is null.
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.string_to_char_p(column)
    nvals = ctypes.c_int(nvals)
    dvals = stypes.to_double_vector(dvals)
    isnull = ctypes.c_int(isnull)
    libspice.ekaced_c(handle, segno, recno, column, nvals, dvals, isnull)


@spice_error_check
def ekucei(
    handle: int,
    segno: int,
    recno: int,
    column: str,
    nvals: int,
    ivals: Union[ndarray, Iterable[int]],
    isnull: bool,
) -> None:
    """
    Update an integer column entry in a specified EK record.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekucei_c.html

    :param handle: EK file handle.
    :param segno: Index of segment containing record.
    :param recno: Record to which data is to be updated.
    :param column: Column name.
    :param nvals: Number of values in new column entry.
    :param ivals: Integer values comprising new column entry.
    :param isnull: Flag indicating whether column entry is null.
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.string_to_char_p(column)
    nvals = ctypes.c_int(nvals)
    ivals = stypes.to_int_vector(ivals)
    isnull = ctypes.c_int(isnull)
    libspice.ekucei_c(handle, segno, recno, column, nvals, ivals, isnull)


@spice_error_check
def ekuef(handle: int) -> None:
    """
    Unload an EK file, making its contents inaccessible to the
    EK reader routines, and clearing space in order to allow other
    EK files to be loaded.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekuef_c.html

    :param handle: Handle of EK file.
    """
    handle = ctypes.c_int(handle)
    libspice.ekuef_c(handle)


@spice_error_check
def el2cgv(ellipse: Ellipse) -> Tuple[ndarray, ndarray, ndarray]:
    """
    Convert an ellipse to a center vector and two generating
    vectors. The selected generating vectors are semi-axes of the
    ellipse.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/el2cgv_c.html

    :param ellipse: An Ellipse
    :return: Center and semi-axes of ellipse.
    """
    assert isinstance(ellipse, stypes.Ellipse)
    center = stypes.empty_double_vector(3)
    smajor = stypes.empty_double_vector(3)
    sminor = stypes.empty_double_vector(3)
    libspice.el2cgv_c(ctypes.byref(ellipse), center, smajor, sminor)
    return (
        stypes.c_vector_to_python(center),
        stypes.c_vector_to_python(smajor),
        stypes.c_vector_to_python(sminor),
    )


@spice_error_check
def elemc(item: str, inset: SpiceCell) -> bool:
    """
    Determine whether an item is an element of a character set.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/elemc_c.html

    :param item: Item to be tested.
    :param inset: Set to be tested.
    :return: True if item is an element of set.
    """
    assert isinstance(inset, stypes.SpiceCell)
    item = stypes.string_to_char_p(item)
    return bool(libspice.elemc_c(item, ctypes.byref(inset)))


@spice_error_check
def elemd(item: float, inset: SpiceCell) -> bool:
    """
    Determine whether an item is an element of a double precision set.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/elemd_c.html

    :param item: Item to be tested.
    :param inset: Set to be tested.
    :return: True if item is an element of set.
    """
    assert isinstance(inset, stypes.SpiceCell)
    assert inset.dtype == 1
    item = ctypes.c_double(item)
    return bool(libspice.elemd_c(item, ctypes.byref(inset)))


@spice_error_check
def elemi(item: int, inset: SpiceCell) -> bool:
    """
    Determine whether an item is an element of an integer set.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/elemi_c.html

    :param item: Item to be tested.
    :param inset: Set to be tested.
    :return: True if item is an element of set.
    """
    assert isinstance(inset, stypes.SpiceCell)
    assert inset.dtype == 2
    item = ctypes.c_int(item)
    return bool(libspice.elemi_c(item, ctypes.byref(inset)))


@spice_error_check
def eqncpv(
    et: float,
    epoch: float,
    eqel: Iterable[Union[float, float]],
    rapol: float,
    decpol: float,
) -> ndarray:
    """
    Compute the state (position and velocity of an object whose
    trajectory is described via equinoctial elements relative to some
    fixed plane (usually the equatorial plane of some planet).

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/eqncpv_c.html

    :param et: Epoch in seconds past J2000 to find state.
    :param epoch: Epoch of elements in seconds past J2000.
    :param eqel: Array of equinoctial elements
    :param rapol: Right Ascension of the pole of the reference plane.
    :param decpol: Declination of the pole of the reference plane.
    :return: State of the object described by eqel.
    """
    et = ctypes.c_double(et)
    epoch = ctypes.c_double(epoch)
    eqel = stypes.to_double_vector(eqel)
    rapol = ctypes.c_double(rapol)
    decpol = ctypes.c_double(decpol)
    state = stypes.empty_double_vector(6)
    libspice.eqncpv_c(et, epoch, eqel, rapol, decpol, state)
    return stypes.c_vector_to_python(state)


@spice_error_check
def eqstr(a: str, b: str) -> bool:
    """
    Determine whether two strings are equivalent.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/eqstr_c.html

    :param a: Arbitrary character string.
    :param b: Arbitrary character string.
    :return: True if A and B are equivalent.
    """
    return bool(
        libspice.eqstr_c(stypes.string_to_char_p(a), stypes.string_to_char_p(b))
    )


def erract(op: str, lenout: int, action: Optional[str] = None) -> str:
    """
    Retrieve or set the default error action.
    spiceypy sets the default error action to "report" on init.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/erract_c.html

    :param op: peration, "GET" or "SET".
    :param lenout: Length of list for output.
    :param action: Error response action.
    :return: Error response action.
    """
    if action is None:
        action = ""
    lenout = ctypes.c_int(lenout)
    op = stypes.string_to_char_p(op)
    action = ctypes.create_string_buffer(str.encode(action), lenout.value)
    actionptr = ctypes.c_char_p(ctypes.addressof(action))
    libspice.erract_c(op, lenout, actionptr)
    return stypes.to_python_string(actionptr)


def errch(marker: str, string: str) -> None:
    """
    Substitute a character string for the first occurrence of
    a marker in the current long error message.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/errch_c.html

    :param marker: A substring of the error message to be replaced.
    :param string: The character string to substitute for marker.
    """
    marker = stypes.string_to_char_p(marker)
    string = stypes.string_to_char_p(string)
    libspice.errch_c(marker, string)


def errdev(op: str, lenout: int, device: str) -> str:
    """
    Retrieve or set the name of the current output device for error messages.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/errdev_c.html

    :param op: The operation, "GET" or "SET".
    :param lenout: Length of device for output.
    :param device: The device name.
    :return: The device name.
    """
    lenout = ctypes.c_int(lenout)
    op = stypes.string_to_char_p(op)
    device = ctypes.create_string_buffer(str.encode(device), lenout.value)
    deviceptr = ctypes.c_char_p(ctypes.addressof(device))
    libspice.errdev_c(op, lenout, deviceptr)
    return stypes.to_python_string(deviceptr)


def errdp(marker: str, number: float) -> None:
    """
    Substitute a double precision number for the first occurrence of
    a marker found in the current long error message.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/errdp_c.html

    :param marker: A substring of the error message to be replaced.
    :param number: The d.p. number to substitute for marker.
    """
    marker = stypes.string_to_char_p(marker)
    number = ctypes.c_double(number)
    libspice.errdp_c(marker, number)


def errint(marker: str, number: int) -> None:
    """
    Substitute an integer for the first occurrence of a marker found
    in the current long error message.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/errint_c.html

    :param marker: A substring of the error message to be replaced.
    :param number: The integer to substitute for marker.
    """
    marker = stypes.string_to_char_p(marker)
    number = ctypes.c_int(number)
    libspice.errint_c(marker, number)


def errprt(op: str, lenout: int, inlist: str) -> str:
    """
    Retrieve or set the list of error message items to be output when an
    error is detected.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/errprt_c.html

    :param op: The operation, "GET" or "SET".
    :param lenout: Length of list for output.
    :param inlist: Specification of error messages to be output.
    :return: A list of error message items.
    """
    lenout = ctypes.c_int(lenout)
    op = stypes.string_to_char_p(op)
    inlist = ctypes.create_string_buffer(str.encode(inlist), lenout.value)
    inlistptr = ctypes.c_char_p(ctypes.addressof(inlist))
    libspice.errdev_c(op, lenout, inlistptr)
    return stypes.to_python_string(inlistptr)


def esrchc(value: str, array: Sequence[str]) -> int:
    """
    Search for a given value within a character string array.
    Return the index of the first equivalent array entry, or -1
    if no equivalent element is found.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/esrchc_c.html

    :param value: Key value to be found in array.
    :param array: Character string array to search.
    :return:
            The index of the first array entry equivalent to value,
            or -1 if none is found.
    """
    value = stypes.string_to_char_p(value)
    ndim = ctypes.c_int(len(array))
    lenvals = ctypes.c_int(len(max(array, key=len)) + 1)
    array = stypes.list_to_char_array(array, x_len=lenvals, y_len=ndim)
    return libspice.esrchc_c(value, ndim, lenvals, array)


@spice_error_check
def et2lst(
    et: float,
    body: int,
    lon: float,
    typein: str,
    timlen: int = _default_len_out,
    ampmlen: int = _default_len_out,
) -> Tuple[int, int, int, str, str]:
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
    et = ctypes.c_double(et)
    body = ctypes.c_int(body)
    lon = ctypes.c_double(lon)
    typein = stypes.string_to_char_p(typein)
    timlen = ctypes.c_int(timlen)
    ampmlen = ctypes.c_int(ampmlen)
    hr = ctypes.c_int()
    mn = ctypes.c_int()
    sc = ctypes.c_int()
    time = stypes.string_to_char_p(timlen)
    ampm = stypes.string_to_char_p(ampmlen)
    libspice.et2lst_c(
        et,
        body,
        lon,
        typein,
        timlen,
        ampmlen,
        ctypes.byref(hr),
        ctypes.byref(mn),
        ctypes.byref(sc),
        time,
        ampm,
    )
    return (
        hr.value,
        mn.value,
        sc.value,
        stypes.to_python_string(time),
        stypes.to_python_string(ampm),
    )


@spice_error_check
def et2utc(
    et: Union[float, Iterable[float]],
    format_str: str,
    prec: int,
    lenout: int = _default_len_out,
) -> Union[ndarray, str]:
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
    prec = ctypes.c_int(prec)
    lenout = ctypes.c_int(lenout)
    format_str = stypes.string_to_char_p(format_str)
    utcstr = stypes.string_to_char_p(lenout)
    if stypes.is_iterable(et):
        results = []
        for t in et:
            libspice.et2utc_c(ctypes.c_double(t), format_str, prec, lenout, utcstr)
            check_for_spice_error(None)
            results.append(stypes.to_python_string(utcstr))
        return numpy.array(results)
    else:
        libspice.et2utc_c(ctypes.c_double(et), format_str, prec, lenout, utcstr)
        return stypes.to_python_string(utcstr)


@spice_error_check
def etcal(
    et: Union[float, ndarray], lenout: int = _default_len_out
) -> Union[str, Iterable[str]]:
    """
    Convert from an ephemeris epoch measured in seconds past
    the epoch of J2000 to a calendar string format using a
    formal calendar free of leapseconds.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/etcal_c.html

    :param et: Ephemeris time measured in seconds past J2000.
    :param lenout: Length of output string.
    :return: A standard calendar representation of et.
    """
    lenout = ctypes.c_int(lenout)
    string = stypes.string_to_char_p(lenout)
    if hasattr(et, "__iter__"):
        strings = []
        for t in et:
            libspice.etcal_c(t, lenout, string)
            check_for_spice_error(None)
            strings.append(stypes.to_python_string(string))
        return strings
    else:
        et = ctypes.c_double(et)
        libspice.etcal_c(et, lenout, string)
        return stypes.to_python_string(string)


@spice_error_check
def eul2m(
    angle3: float, angle2: float, angle1: float, axis3: int, axis2: int, axis1: int
) -> ndarray:
    """
    Construct a rotation matrix from a set of Euler angles.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/eul2m_c.html

    :param angle3: Rotation angle about third rotation axis (radians).
    :param angle2: Rotation angle about second rotation axis (radians).
    :param angle1: Rotation angle about first rotation axis (radians).
    :param axis3: Axis number of third rotation axis.
    :param axis2: Axis number of second rotation axis.
    :param axis1: Axis number of first rotation axis.]
    :return: Product of the 3 rotations.
    """
    angle3 = ctypes.c_double(angle3)
    angle2 = ctypes.c_double(angle2)
    angle1 = ctypes.c_double(angle1)
    axis3 = ctypes.c_int(axis3)
    axis2 = ctypes.c_int(axis2)
    axis1 = ctypes.c_int(axis1)
    r = stypes.empty_double_matrix()
    libspice.eul2m_c(angle3, angle2, angle1, axis3, axis2, axis1, r)
    return stypes.c_matrix_to_numpy(r)


@spice_error_check
def eul2xf(eulang: Sequence[float], axisa: int, axisb: int, axisc: int) -> ndarray:
    """
    This routine computes a state transformation from an Euler angle
    factorization of a rotation and the derivatives of those Euler
    angles.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/eul2xf_c.html

    :param eulang: An array of Euler angles and their derivatives.
    :param axisa: Axis A of the Euler angle factorization.
    :param axisb: Axis B of the Euler angle factorization.
    :param axisc: Axis C of the Euler angle factorization.
    :return: A state transformation matrix.
    """
    assert len(eulang) == 6
    eulang = stypes.to_double_vector(eulang)
    axisa = ctypes.c_int(axisa)
    axisb = ctypes.c_int(axisb)
    axisc = ctypes.c_int(axisc)
    xform = stypes.empty_double_matrix(x=6, y=6)
    libspice.eul2xf_c(eulang, axisa, axisb, axisc, xform)
    return stypes.c_matrix_to_numpy(xform)


@spice_error_check
def ev2lin(et: float, geophs: Sequence[float], elems: Sequence[float]) -> ndarray:
    """
    This routine evaluates NORAD two-line element data for
    near-earth orbiting spacecraft (that is spacecraft with
    orbital periods less than 225 minutes).

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/FORTRAN/spicelib/ev2lin.html

    :param et: Epoch in seconds past ephemeris epoch J2000.
    :param geophs: Geophysical constants
    :param elems: Two-line element data
    :return: Evaluated state
    """
    et = ctypes.c_double(et)
    assert len(geophs) == 8
    geophs = stypes.to_double_vector(geophs)
    assert len(elems) == 10
    elems = stypes.to_double_vector(elems)
    state = stypes.empty_double_vector(6)
    libspice.ev2lin_(ctypes.byref(et), geophs, elems, state)
    return stypes.c_vector_to_python(state)


def evsgp4(et: float, geophs: Sequence[float], elems: Sequence[float]) -> ndarray:
    """
    Evaluate NORAD two-line element data for earth orbiting
    spacecraft. This evaluator uses algorithms as described
    in Vallado 2006

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/evsgp4_c.html

    :param et: Epoch in seconds past ephemeris epoch J2000.
    :param geophs: Geophysical constants
    :param elems: Two-line element data
    :return: Evaluated state
    """
    _et = ctypes.c_double(et)
    assert len(geophs) == 8
    _geophs = stypes.to_double_vector(geophs)
    assert len(elems) == 10
    _elems = stypes.to_double_vector(elems)
    _state = stypes.empty_double_vector(6)
    libspice.evsgp4_c(_et, _geophs, _elems, _state)
    return stypes.c_vector_to_python(_state)


@spice_error_check
def exists(fname: str) -> bool:
    """
    Determine whether a file exists.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/exists_c.html

    :param fname: Name of the file in question.
    :return: True if the file exists, False otherwise.
    """
    fname = stypes.string_to_char_p(fname)
    return bool(libspice.exists_c(fname))


@spice_error_check
def expool(name: str) -> bool:
    """
    Confirm the existence of a kernel variable in the kernel pool.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/expool_c.html

    :param name: Name of the variable whose value is to be returned.
    :return: True when the variable is in the pool.
    """
    name = stypes.string_to_char_p(name)
    found = ctypes.c_int()
    libspice.expool_c(name, ctypes.byref(found))
    return bool(found.value)


################################################################################
# F


def failed() -> bool:
    """
    True if an error condition has been signalled via sigerr_c.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/failed_c.html

    :return: a boolean
    """
    return bool(libspice.failed_c())


@spice_error_check
def fn2lun(fname: str) -> int:
    """
    Internal undocumented command for mapping name of open file to
    its FORTRAN (F2C) logical unit.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/FORTRAN/spicelib/fn2lun.html

    :param fname: name of the file to be mapped to its logical unit.
    :return: the FORTRAN (F2C) logical unit associated with the filename.
    """
    fname_p = stypes.string_to_char_p(fname)
    unit_out = ctypes.c_int()
    fname_len = ctypes.c_int(len(fname) + 1)
    libspice.fn2lun_(fname_p, ctypes.byref(unit_out), fname_len)
    return unit_out.value


@spice_error_check
def fovray(
    inst: str,
    raydir: Union[ndarray, Iterable[float]],
    rframe: str,
    abcorr: str,
    observer: str,
    et: float,
) -> bool:
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
    inst = stypes.string_to_char_p(inst)
    raydir = stypes.to_double_vector(raydir)
    rframe = stypes.string_to_char_p(rframe)
    abcorr = stypes.string_to_char_p(abcorr)
    observer = stypes.string_to_char_p(observer)
    et = ctypes.c_double(et)
    visible = ctypes.c_int()
    libspice.fovray_c(
        inst, raydir, rframe, abcorr, observer, ctypes.byref(et), ctypes.byref(visible)
    )
    return bool(visible.value)


@spice_error_check
def fovtrg(
    inst: str,
    target: str,
    tshape: str,
    tframe: str,
    abcorr: str,
    observer: str,
    et: float,
) -> bool:
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
    inst = stypes.string_to_char_p(inst)
    target = stypes.string_to_char_p(target)
    tshape = stypes.string_to_char_p(tshape)
    tframe = stypes.string_to_char_p(tframe)
    abcorr = stypes.string_to_char_p(abcorr)
    observer = stypes.string_to_char_p(observer)
    et = ctypes.c_double(et)
    visible = ctypes.c_int()
    libspice.fovtrg_c(
        inst,
        target,
        tshape,
        tframe,
        abcorr,
        observer,
        ctypes.byref(et),
        ctypes.byref(visible),
    )
    return bool(visible.value)


@spice_error_check
def frame(x: Union[ndarray, Iterable[float]]) -> Tuple[ndarray, ndarray, ndarray]:
    """
    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/frame_c.html

    :param x: Input vector. A parallel unit vector on output.
    :return: a tuple of 3 list[3]
    """
    x = stypes.to_double_vector(x)
    y = stypes.empty_double_vector(3)
    z = stypes.empty_double_vector(3)
    libspice.frame_c(x, y, z)
    return (
        stypes.c_vector_to_python(x),
        stypes.c_vector_to_python(y),
        stypes.c_vector_to_python(z),
    )


@spice_error_check
@spice_found_exception_thrower
def frinfo(frcode: int) -> Tuple[int, int, int, bool]:
    """
    Retrieve the minimal attributes associated with a frame
    needed for converting transformations to and from it.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/frinfo_c.html

    :param frcode: the idcode for some frame.
    :return: a tuple of attributes associated with the frame.
    """
    frcode = ctypes.c_int(frcode)
    cent = ctypes.c_int()
    frclss = ctypes.c_int()
    clssid = ctypes.c_int()
    found = ctypes.c_int()
    libspice.frinfo_c(
        frcode,
        ctypes.byref(cent),
        ctypes.byref(frclss),
        ctypes.byref(clssid),
        ctypes.byref(found),
    )
    return cent.value, frclss.value, clssid.value, bool(found.value)


@spice_error_check
def frmnam(frcode: int, lenout: int = _default_len_out) -> str:
    """
    Retrieve the name of a reference frame associated with a SPICE ID code.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/frmnam_c.html

    :param frcode: an integer code for a reference frame
    :param lenout: Maximum length of output string.
    :return: the name associated with the reference frame.
    """
    frcode = ctypes.c_int(frcode)
    lenout = ctypes.c_int(lenout)
    frname = stypes.string_to_char_p(lenout)
    libspice.frmnam_c(frcode, lenout, frname)
    return stypes.to_python_string(frname)


@spice_error_check
def ftncls(unit: int) -> None:
    """
    Close a file designated by a Fortran-style integer logical unit.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ftncls_c.html

    :param unit: Fortran-style logical unit.
    """
    unit = ctypes.c_int(unit)
    libspice.ftncls_c(unit)


@spice_error_check
def furnsh(path: Union[str, Iterable[str]]) -> None:
    """
    Load one or more SPICE kernels into a program.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/furnsh_c.html

    :param path: one or more paths to kernels
    """
    if stypes.is_iterable(path):
        for p in path:
            libspice.furnsh_c(stypes.string_to_char_p(p))
    else:
        path = stypes.string_to_char_p(path)
        libspice.furnsh_c(path)


################################################################################
# G


@spice_error_check
@spice_found_exception_thrower
def gcpool(
    name: str, start: int, room: int, lenout: int = _default_len_out
) -> Tuple[Iterable[str], bool]:
    """
    Return the character value of a kernel variable from the kernel pool.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gcpool_c.html

    :param name: Name of the variable whose value is to be returned.
    :param start: Which component to start retrieving for name.
    :param room: The largest number of values to return.
    :param lenout: The length of the output string.
    :return: Values associated with name.
    """
    name = stypes.string_to_char_p(name)
    start = ctypes.c_int(start)
    room = ctypes.c_int(room)
    lenout = ctypes.c_int(lenout)
    n = ctypes.c_int()
    cvals = stypes.empty_char_array(lenout, room)
    found = ctypes.c_int()
    libspice.gcpool_c(
        name,
        start,
        room,
        lenout,
        ctypes.byref(n),
        ctypes.byref(cvals),
        ctypes.byref(found),
    )
    return (
        [stypes.to_python_string(x.value) for x in cvals[0 : n.value]],
        bool(found.value),
    )


@spice_error_check
@spice_found_exception_thrower
def gdpool(name: str, start: int, room: int) -> Tuple[ndarray, bool]:
    """
    Return the d.p. value of a kernel variable from the kernel pool.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gdpool_c.html

    :param name: Name of the variable whose value is to be returned.
    :param start: Which component to start retrieving for name.
    :param room: The largest number of values to return.
    :return: Values associated with name.
    """
    name = stypes.string_to_char_p(name)
    start = ctypes.c_int(start)
    values = stypes.empty_double_vector(room)
    room = ctypes.c_int(room)
    n = ctypes.c_int()
    found = ctypes.c_int()
    libspice.gdpool_c(
        name,
        start,
        room,
        ctypes.byref(n),
        ctypes.cast(values, ctypes.POINTER(ctypes.c_double)),
        ctypes.byref(found),
    )
    return stypes.c_vector_to_python(values)[0 : n.value], bool(found.value)


@spice_error_check
def georec(lon: float, lat: float, alt: float, re: float, f: float) -> ndarray:
    """
    Convert geodetic coordinates to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/georec_c.html

    :param lon: Geodetic longitude of point (radians).
    :param lat: Geodetic latitude  of point (radians).
    :param alt: Altitude of point above the reference spheroid.
    :param re: Equatorial radius of the reference spheroid.
    :param f: Flattening coefficient.
    :return: Rectangular coordinates of point.
    """
    lon = ctypes.c_double(lon)
    lat = ctypes.c_double(lat)
    alt = ctypes.c_double(alt)
    re = ctypes.c_double(re)
    f = ctypes.c_double(f)
    rectan = stypes.empty_double_vector(3)
    libspice.georec_c(lon, lat, alt, re, f, rectan)
    return stypes.c_vector_to_python(rectan)


# getcml not really needed


@spice_error_check
def getelm(frstyr: int, lineln: int, lines: Iterable[str]) -> Tuple[float, ndarray]:
    """
    Given a the "lines" of a two-line element set, parse the
    lines and return the elements in units suitable for use
    in SPICE software.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/getelm_c.html

    :param frstyr: Year of earliest representable two-line elements.
    :param lineln: Length of strings in lines array.
    :param lines: A pair of "lines" containing two-line elements.
    :return:
            The epoch of the elements in seconds past J2000,
            The elements converted to SPICE units.
    """
    frstyr = ctypes.c_int(frstyr)
    lineln = ctypes.c_int(lineln)
    lines = stypes.list_to_char_array_ptr(lines, x_len=lineln, y_len=2)
    epoch = ctypes.c_double()
    elems = stypes.empty_double_vector(10)  # guess for length
    libspice.getelm_c(frstyr, lineln, lines, ctypes.byref(epoch), elems)
    return epoch.value, stypes.c_vector_to_python(elems)


@spice_error_check
def getfat(file: str) -> Tuple[str, str]:
    """
    Determine the file architecture and file type of most SPICE kernel files.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/getfat_c.html

    :param file: The name of a file to be examined.
    :return: The architecture of the kernel file, The type of the kernel file.
    """
    file = stypes.string_to_char_p(file)
    arclen = ctypes.c_int(5)
    typlen = ctypes.c_int(5)
    arch = stypes.string_to_char_p(arclen)
    rettype = stypes.string_to_char_p(typlen)
    libspice.getfat_c(file, arclen, typlen, arch, rettype)
    return stypes.to_python_string(arch), stypes.to_python_string(rettype)


@spice_error_check
def getfov(
    instid: int,
    room: int,
    shapelen: int = _default_len_out,
    framelen: int = _default_len_out,
) -> Tuple[str, str, ndarray, int, ndarray]:
    """
    This routine returns the field-of-view (FOV) parameters for a
    specified instrument.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/getfov_c.html

    :param instid: NAIF ID of an instrument.
    :param room: Maximum number of vectors that can be returned.
    :param shapelen: Space available in the string shape.
    :param framelen: Space available in the string frame.
    :return:
            Instrument FOV shape,
            Name of the frame in which FOV vectors are defined,
            Boresight vector,
            Number of boundary vectors returned,
            FOV boundary vectors.
    """
    instid = ctypes.c_int(instid)
    shape = stypes.string_to_char_p(" " * shapelen)
    framen = stypes.string_to_char_p(" " * framelen)
    shapelen = ctypes.c_int(shapelen)
    framelen = ctypes.c_int(framelen)
    bsight = stypes.empty_double_vector(3)
    n = ctypes.c_int()
    bounds = stypes.empty_double_matrix(x=3, y=room)
    room = ctypes.c_int(room)
    libspice.getfov_c(
        instid, room, shapelen, framelen, shape, framen, bsight, ctypes.byref(n), bounds
    )
    return (
        stypes.to_python_string(shape),
        stypes.to_python_string(framen),
        stypes.c_vector_to_python(bsight),
        n.value,
        stypes.c_matrix_to_numpy(bounds)[0 : n.value],
    )


@spice_error_check
def getfvn(
    inst: str,
    room: int,
    shapelen: int = _default_len_out,
    framelen: int = _default_len_out,
) -> Tuple[str, str, ndarray, int, ndarray]:
    """
    Return the field-of-view (FOV) parameters for a specified
    instrument. The instrument is specified by name.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/getfvn_c.html

    :param inst: Name of an instrument.
    :param room: Maximum number of vectors that can be returned.
    :param shapelen: Space available in the string shape.
    :param framelen: Space available in the string frame.
    :return:
            Instrument FOV shape,
            Name of the frame in which FOV vectors are defined,
            Boresight vector,
            Number of boundary vectors returned,
            FOV boundary vectors.
    """
    inst = stypes.string_to_char_p(inst)
    shape = stypes.string_to_char_p(" " * shapelen)
    framen = stypes.string_to_char_p(" " * framelen)
    shapelen = ctypes.c_int(shapelen)
    framelen = ctypes.c_int(framelen)
    bsight = stypes.empty_double_vector(3)
    n = ctypes.c_int()
    bounds = stypes.empty_double_matrix(x=3, y=room)
    room = ctypes.c_int(room)
    libspice.getfvn_c(
        inst, room, shapelen, framelen, shape, framen, bsight, ctypes.byref(n), bounds
    )
    return (
        stypes.to_python_string(shape),
        stypes.to_python_string(framen),
        stypes.c_vector_to_python(bsight),
        n.value,
        stypes.c_matrix_to_numpy(bounds)[0 : n.value],
    )


def getmsg(option: str, lenout: int = _default_len_out) -> str:
    """
    Retrieve the current short error message,
    the explanation of the short error message, or the
    long error message.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/getmsg_c.html

    :param option: Indicates type of error message.
    :param lenout: Available space in the output string msg.
    :return: The error message to be retrieved.
    """
    option = stypes.string_to_char_p(option)
    lenout = ctypes.c_int(lenout)
    msg = stypes.string_to_char_p(lenout)
    libspice.getmsg_c(option, lenout, msg)
    return stypes.to_python_string(msg)


@spice_error_check
def gfbail() -> bool:
    """
    Indicate whether an interrupt signal (SIGINT) has been received.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfbail_c.html

    :return: True if an interrupt signal has been received by the GF handler.
    """
    return bool(libspice.gfbail_c())


@spice_error_check
def gfclrh() -> None:
    """
    Clear the interrupt signal handler status, so that future calls
    to :func:`gfbail` will indicate no interrupt was received.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfclrh_c.html

    """
    libspice.gfclrh_c()


@spice_error_check
def gfdist(
    target: str,
    abcorr: str,
    obsrvr: str,
    relate: str,
    refval: int,
    adjust: float,
    step: float,
    nintvls: int,
    cnfine: SpiceCell,
    result: Optional[SpiceCell] = None,
) -> SpiceCell:
    """
    Return the time window over which a specified constraint on
    observer-target distance is met.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfdist_c.html

    :param target: Name of the target body.
    :param abcorr: Aberration correction flag.
    :param obsrvr: Name of the observing body.
    :param relate: Relational operator.
    :param refval: Reference value.
    :param adjust: Adjustment value for absolute extrema searches.
    :param step: Step size used for locating extrema and roots.
    :param nintvls: Workspace window interval count.
    :param cnfine: SPICE window to which the search is confined.
    :param result: Optional SPICE window containing results.
    """
    assert isinstance(cnfine, stypes.SpiceCell)
    assert cnfine.is_double()
    if result is None:
        result = stypes.SPICEDOUBLE_CELL(2000)
    else:
        assert isinstance(result, stypes.SpiceCell)
        assert result.is_double()
    target = stypes.string_to_char_p(target)
    abcorr = stypes.string_to_char_p(abcorr)
    obsrvr = stypes.string_to_char_p(obsrvr)
    relate = stypes.string_to_char_p(relate)
    refval = ctypes.c_double(refval)
    adjust = ctypes.c_double(adjust)
    step = ctypes.c_double(step)
    nintvls = ctypes.c_int(nintvls)
    libspice.gfdist_c(
        target,
        abcorr,
        obsrvr,
        relate,
        refval,
        adjust,
        step,
        nintvls,
        ctypes.byref(cnfine),
        ctypes.byref(result),
    )
    return result


@spice_error_check
def gfevnt(
    udstep: UDSTEP,
    udrefn: UDREFN,
    gquant: str,
    qnpars: int,
    lenvals: int,
    qpnams: Iterable[str],
    qcpars: Iterable[str],
    qdpars: Union[ndarray, Iterable[float]],
    qipars: Union[ndarray, Iterable[int]],
    qlpars: Union[ndarray, Iterable[int]],
    op: str,
    refval: float,
    tol: float,
    adjust: float,
    rpt: int,
    udrepi: UDREPI,
    udrepu: UDREPU,
    udrepf: UDREPF,
    nintvls: int,
    bail: int,
    udbail: UDBAIL,
    cnfine: SpiceCell,
    result: Optional[SpiceCell] = None,
):
    """
    Determine time intervals when a specified geometric quantity
    satisfies a specified mathematical condition.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfevnt_c.html

    :param udstep: Name of the routine that computes and returns a
    :param udrefn: Name of the routine that computes a refined time
    :param gquant: Type of geometric quantity
    :param qnpars: Number of quantity definition parameters
    :param lenvals: Length of strings in qpnams and qcpars
    :param qpnams: Names of quantity definition parameters
    :param qcpars: Array of character quantity definition parameters
    :param qdpars: Array of double precision quantity definition
    :param qipars: Array of integer quantity definition parameters
    :param qlpars: Array of logical quantity definition parameters
    :param op: Operator that either looks for an extreme value
    :param refval: Reference value
    :param tol: Convergence tolerance in seconds
    :param adjust: Absolute extremum adjustment value
    :param rpt: Progress reporter on TRUE or off FALSE
    :param udrepi: Function that initializes progress reporting
    :param udrepu: Function that updates the progress report
    :param udrepf: Function that finalizes progress reporting
    :param nintvls: Workspace window interval count
    :param bail: Logical indicating program interrupt monitoring
    :param udbail: Name of a routine that signals a program interrupt
    :param cnfine: SPICE window to which the search is restricted
    :param result: Optional SPICE window containing results
    """
    assert isinstance(cnfine, stypes.SpiceCell)
    assert cnfine.is_double()
    if result is None:
        result = stypes.SPICEDOUBLE_CELL(2000)
    else:
        assert isinstance(result, stypes.SpiceCell)
        assert result.is_double()
    gquant = stypes.string_to_char_p(gquant)
    qnpars = ctypes.c_int(qnpars)
    lenvals = ctypes.c_int(lenvals)
    qpnams = stypes.list_to_char_array_ptr(qpnams, x_len=lenvals, y_len=qnpars)
    qcpars = stypes.list_to_char_array_ptr(qcpars, x_len=lenvals, y_len=qnpars)
    qdpars = stypes.to_double_vector(qdpars)
    qipars = stypes.to_int_vector(qipars)
    qlpars = stypes.to_int_vector(qlpars)
    op = stypes.string_to_char_p(op)
    refval = ctypes.c_double(refval)
    tol = ctypes.c_double(tol)
    adjust = ctypes.c_double(adjust)
    rpt = ctypes.c_int(rpt)
    nintvls = ctypes.c_int(nintvls)
    bail = ctypes.c_int(bail)
    libspice.gfevnt_c(
        udstep,
        udrefn,
        gquant,
        qnpars,
        lenvals,
        qpnams,
        qcpars,
        qdpars,
        qipars,
        qlpars,
        op,
        refval,
        tol,
        adjust,
        rpt,
        udrepi,
        udrepu,
        udrepf,
        nintvls,
        bail,
        udbail,
        ctypes.byref(cnfine),
        ctypes.byref(result),
    )
    return result


@spice_error_check
def gffove(
    inst: str,
    tshape: str,
    raydir: Union[ndarray, Iterable[float]],
    target: str,
    tframe: str,
    abcorr: str,
    obsrvr: str,
    tol: float,
    udstep: UDSTEP,
    udrefn: UDREFN,
    rpt: int,
    udrepi: UDREPI,
    udrepu: UDREPU,
    udrepf: UDREPF,
    bail: int,
    udbail: UDBAIL,
    cnfine: SpiceCell,
    result: Optional[SpiceCell] = None,
):
    """
    Determine time intervals when a specified target body or ray
    intersects the space bounded by the field-of-view (FOV) of a
    specified instrument. Report progress and handle interrupts if so
    commanded.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gffove_c.html

    :param inst: Name of the instrument
    :param tshape: Type of shape model used for target body
    :param raydir: Ray s direction vector
    :param target: Name of the target body
    :param tframe: Body fixed body centered frame for target body
    :param abcorr: Aberration correction flag
    :param obsrvr: Name of the observing body
    :param tol: Convergence tolerance in seconds
    :param udstep: Name of the routine that returns a time step
    :param udrefn: Name of the routine that computes a refined time
    :param rpt:  Progress report flag
    :param udrepi: Function that initializes progress reporting.
    :param udrepu: Function that updates the progress report
    :param udrepf: Function that finalizes progress reporting
    :param bail: Logical indicating program interrupt monitoring
    :param udbail: Name of a routine that signals a program interrupt
    :param cnfine: SPICE window to which the search is restricted
    :param result: Optional SPICE window containing results
    """
    assert isinstance(cnfine, stypes.SpiceCell)
    assert cnfine.is_double()
    if result is None:
        result = stypes.SPICEDOUBLE_CELL(2000)
    else:
        assert isinstance(result, stypes.SpiceCell)
        assert result.is_double()
    inst = stypes.string_to_char_p(inst)
    tshape = stypes.string_to_char_p(tshape)
    raydir = stypes.to_double_vector(raydir)
    target = stypes.string_to_char_p(target)
    tframe = stypes.string_to_char_p(tframe)
    abcorr = stypes.string_to_char_p(abcorr)
    obsrvr = stypes.string_to_char_p(obsrvr)
    tol = ctypes.c_double(tol)
    rpt = ctypes.c_int(rpt)
    bail = ctypes.c_int(bail)
    libspice.gffove_c(
        inst,
        tshape,
        raydir,
        target,
        tframe,
        abcorr,
        obsrvr,
        tol,
        udstep,
        udrefn,
        rpt,
        udrepi,
        udrepu,
        udrepf,
        bail,
        udbail,
        ctypes.byref(cnfine),
        ctypes.byref(result),
    )
    return result


@spice_error_check
def gfilum(
    method: str,
    angtyp: str,
    target: str,
    illumn: str,
    fixref: str,
    abcorr: str,
    obsrvr: str,
    spoint: Union[ndarray, Iterable[float]],
    relate: str,
    refval: float,
    adjust: float,
    step: float,
    nintvls: int,
    cnfine: SpiceCell,
    result: Optional[SpiceCell] = None,
) -> SpiceCell:
    """
    Return the time window over which a specified constraint on
    the observed phase, solar incidence, or emission angle at
    a specifed target body surface point is met.

    :param method: Shape model used to represent the surface of the target body.
    :param angtyp: The type of illumination angle for which a search is to be performed.
    :param target: Name of a target body.
    :param illumn: Name of the illumination source.
    :param fixref: Name of the body-fixed, body-centered reference frame associated with the target body.
    :param abcorr: The aberration corrections to be applied.
    :param obsrvr: Name of an observing body.
    :param spoint: Body-fixed coordinates of a target surface point.
    :param relate: Relational operator used to define a constraint on a specified illumination angle.
    :param refval: Reference value used with 'relate' to define an equality or inequality to be satisfied by the specified illumination angle.
    :param adjust: Parameter used to modify searches for absolute extrema.
    :param step: Step size to be used in the search.
    :param nintvls: Number of intervals that can be accommodated by each of the dynamically allocated workspace windows used internally by this routine.
    :param cnfine: Window that confines the time period over which the specified search is conducted. This can be updated by gfilum
    :param result: Optional SPICE Window of intervals in the confinement window that the illumination angle constraint is satisfied.
    """
    assert isinstance(cnfine, stypes.SpiceCell)
    assert cnfine.is_double()
    if result is None:
        result = stypes.SPICEDOUBLE_CELL(2000)
    else:
        assert isinstance(result, stypes.SpiceCell)
        assert result.is_double()
    method = stypes.string_to_char_p(method)
    angtyp = stypes.string_to_char_p(angtyp)
    target = stypes.string_to_char_p(target)
    illumn = stypes.string_to_char_p(illumn)
    fixref = stypes.string_to_char_p(fixref)
    abcorr = stypes.string_to_char_p(abcorr)
    obsrvr = stypes.string_to_char_p(obsrvr)
    spoint = stypes.to_double_vector(spoint)
    relate = stypes.string_to_char_p(relate)
    refval = ctypes.c_double(refval)
    adjust = ctypes.c_double(adjust)
    step = ctypes.c_double(step)
    nintvls = ctypes.c_int(nintvls)
    libspice.gfilum_c(
        method,
        angtyp,
        target,
        illumn,
        fixref,
        abcorr,
        obsrvr,
        spoint,
        relate,
        refval,
        adjust,
        step,
        nintvls,
        ctypes.byref(cnfine),
        ctypes.byref(result),
    )
    return result


@spice_error_check
def gfinth(sigcode: int) -> None:
    """
    Respond to the interrupt signal SIGINT: save an indication
    that the signal has been received. This routine restores
    itself as the handler for SIGINT.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfinth_c.html

    :param sigcode: Interrupt signal ID code.
    """
    sigcode = ctypes.c_int(sigcode)
    libspice.gfinth_c(sigcode)


@spice_error_check
def gfocce(
    occtyp: str,
    front: str,
    fshape: str,
    fframe: str,
    back: str,
    bshape: str,
    bframe: str,
    abcorr: str,
    obsrvr: str,
    tol: float,
    udstep: UDSTEP,
    udrefn: UDREFN,
    rpt: int,
    udrepi: UDREPI,
    udrepu: UDREPU,
    udrepf: UDREPF,
    bail: int,
    udbail: UDBAIL,
    cnfine: SpiceCell,
    result: Optional[SpiceCell] = None,
):
    """
    Determine time intervals when an observer sees one target
    occulted by another. Report progress and handle interrupts
    if so commanded.

    The surfaces of the target bodies may be represented by triaxial
    ellipsoids or by topographic data provided by DSK files.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfocce_c.html

    :param occtyp: Type of occultation
    :param front: Name of body occulting the other
    :param fshape: Type of shape model used for front body
    :param fframe: Body fixed body centered frame for front body
    :param back: Name of body occulted by the other
    :param bshape: Type of shape model used for back body
    :param bframe: Body fixed body centered frame for back body
    :param abcorr: Aberration correction flag
    :param obsrvr: Name of the observing body
    :param tol: Convergence tolerance in seconds
    :param udstep: Name of the routine that returns a time step
    :param udrefn: Name of the routine that computes a refined time
    :param rpt: Progress report flag
    :param udrepi: Function that initializes progress reporting.
    :param udrepu: Function that updates the progress report
    :param udrepf: Function that finalizes progress reporting
    :param bail: Logical indicating program interrupt monitoring
    :param udbail: Name of a routine that signals a program interrupt
    :param cnfine: SPICE window to which the search is restricted
    :param result: Optional SPICE window containing results.
    """
    assert isinstance(cnfine, stypes.SpiceCell)
    assert cnfine.is_double()
    if result is None:
        result = stypes.SPICEDOUBLE_CELL(2000)
    else:
        assert isinstance(result, stypes.SpiceCell)
        assert result.is_double()
    occtyp = stypes.string_to_char_p(occtyp)
    front = stypes.string_to_char_p(front)
    fshape = stypes.string_to_char_p(fshape)
    fframe = stypes.string_to_char_p(fframe)
    back = stypes.string_to_char_p(back)
    bshape = stypes.string_to_char_p(bshape)
    bframe = stypes.string_to_char_p(bframe)
    abcorr = stypes.string_to_char_p(abcorr)
    obsrvr = stypes.string_to_char_p(obsrvr)
    tol = ctypes.c_double(tol)
    rpt = ctypes.c_int(rpt)
    bail = ctypes.c_int(bail)
    libspice.gfocce_c(
        occtyp,
        front,
        fshape,
        fframe,
        back,
        bshape,
        bframe,
        abcorr,
        obsrvr,
        tol,
        udstep,
        udrefn,
        rpt,
        udrepi,
        udrepu,
        udrepf,
        bail,
        udbail,
        ctypes.byref(cnfine),
        ctypes.byref(result),
    )
    return result


@spice_error_check
def gfoclt(
    occtyp: str,
    front: str,
    fshape: str,
    fframe: str,
    back: str,
    bshape: str,
    bframe: str,
    abcorr: str,
    obsrvr: str,
    step: float,
    cnfine: SpiceCell,
    result: Optional[SpiceCell] = None,
) -> SpiceCell:
    """
    Determine time intervals when an observer sees one target
    occulted by, or in transit across, another.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfoclt_c.html

    :param occtyp: Type of occultation.
    :param front: Name of body occulting the other.
    :param fshape: Type of shape model used for front body.
    :param fframe: Body-fixed, body-centered frame for front body.
    :param back: Name of body occulted by the other.
    :param bshape: Type of shape model used for back body.
    :param bframe: Body-fixed, body-centered frame for back body.
    :param abcorr: Aberration correction flag.
    :param obsrvr: Name of the observing body.
    :param step: Step size in seconds for finding occultation events.
    :param cnfine: SPICE window to which the search is restricted.
    :param result: Optional SPICE window containing results.
    """
    assert isinstance(cnfine, stypes.SpiceCell)
    assert cnfine.is_double()
    if result is None:
        result = stypes.SPICEDOUBLE_CELL(2000)
    else:
        assert isinstance(result, stypes.SpiceCell)
        assert result.is_double()
    occtyp = stypes.string_to_char_p(occtyp)
    front = stypes.string_to_char_p(front)
    fshape = stypes.string_to_char_p(fshape)
    fframe = stypes.string_to_char_p(fframe)
    back = stypes.string_to_char_p(back)
    bshape = stypes.string_to_char_p(bshape)
    bframe = stypes.string_to_char_p(bframe)
    abcorr = stypes.string_to_char_p(abcorr)
    obsrvr = stypes.string_to_char_p(obsrvr)
    step = ctypes.c_double(step)
    libspice.gfoclt_c(
        occtyp,
        front,
        fshape,
        fframe,
        back,
        bshape,
        bframe,
        abcorr,
        obsrvr,
        step,
        ctypes.byref(cnfine),
        ctypes.byref(result),
    )
    return result


@spice_error_check
def gfpa(
    target: str,
    illmin: str,
    abcorr: str,
    obsrvr: str,
    relate: str,
    refval: float,
    adjust: float,
    step: float,
    nintvls: int,
    cnfine: SpiceCell,
    result: Optional[SpiceCell] = None,
) -> SpiceCell:
    """
    Determine time intervals for which a specified constraint
    on the phase angle between an illumination source, a target,
    and observer body centers is met.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfpa_c.html

    :param target: Name of the target body.
    :param illmin: Name of the illuminating body.
    :param abcorr: Aberration correction flag.
    :param obsrvr: Name of the observing body.
    :param relate: Relational operator.
    :param refval: Reference value.
    :param adjust: Adjustment value for absolute extrema searches.
    :param step: Step size used for locating extrema and roots.
    :param nintvls: Workspace window interval count.
    :param cnfine: SPICE window to which the search is restricted.
    :param result: Optional SPICE window containing results.
    """
    assert isinstance(cnfine, stypes.SpiceCell)
    assert cnfine.is_double()
    if result is None:
        result = stypes.SPICEDOUBLE_CELL(2000)
    else:
        assert isinstance(result, stypes.SpiceCell)
        assert result.is_double()
    target = stypes.string_to_char_p(target)
    illmin = stypes.string_to_char_p(illmin)
    abcorr = stypes.string_to_char_p(abcorr)
    obsrvr = stypes.string_to_char_p(obsrvr)
    relate = stypes.string_to_char_p(relate)
    refval = ctypes.c_double(refval)
    adjust = ctypes.c_double(adjust)
    step = ctypes.c_double(step)
    nintvls = ctypes.c_int(nintvls)
    libspice.gfpa_c(
        target,
        illmin,
        abcorr,
        obsrvr,
        relate,
        refval,
        adjust,
        step,
        nintvls,
        ctypes.byref(cnfine),
        ctypes.byref(result),
    )
    return result


@spice_error_check
def gfposc(
    target: str,
    inframe: str,
    abcorr: str,
    obsrvr: str,
    crdsys: str,
    coord: str,
    relate: str,
    refval: float,
    adjust: float,
    step: float,
    nintvls: int,
    cnfine: SpiceCell,
    result: Optional[SpiceCell] = None,
) -> SpiceCell:
    """
    Determine time intervals for which a coordinate of an
    observer-target position vector satisfies a numerical constraint.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfposc_c.html

    :param target: Name of the target body.
    :param inframe: Name of the reference frame for coordinate calculations.
    :param abcorr: Aberration correction flag.
    :param obsrvr: Name of the observing body.
    :param crdsys: Name of the coordinate system containing COORD
    :param coord: Name of the coordinate of interest
    :param relate: Relational operator.
    :param refval: Reference value.
    :param adjust: Adjustment value for absolute extrema searches.
    :param step: Step size used for locating extrema and roots.
    :param nintvls: Workspace window interval count.
    :param cnfine: SPICE window to which the search is restricted.
    :param result: Optional SPICE window containing results.
    """
    assert isinstance(cnfine, stypes.SpiceCell)
    assert cnfine.is_double()
    if result is None:
        result = stypes.SPICEDOUBLE_CELL(2000)
    else:
        assert isinstance(result, stypes.SpiceCell)
        assert result.is_double()
    target = stypes.string_to_char_p(target)
    inframe = stypes.string_to_char_p(inframe)
    abcorr = stypes.string_to_char_p(abcorr)
    obsrvr = stypes.string_to_char_p(obsrvr)
    crdsys = stypes.string_to_char_p(crdsys)
    coord = stypes.string_to_char_p(coord)
    relate = stypes.string_to_char_p(relate)
    refval = ctypes.c_double(refval)
    adjust = ctypes.c_double(adjust)
    step = ctypes.c_double(step)
    nintvls = ctypes.c_int(nintvls)
    libspice.gfposc_c(
        target,
        inframe,
        abcorr,
        obsrvr,
        crdsys,
        coord,
        relate,
        refval,
        adjust,
        step,
        nintvls,
        ctypes.byref(cnfine),
        ctypes.byref(result),
    )
    return result


@spice_error_check
def gfrefn(t1: float, t2: float, s1: Union[bool, int], s2: Union[bool, int]) -> float:
    """
    For those times when we can't do better, we use a bisection
    method to find the next time at which to test for state change.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfrefn_c.html

    :param t1: One of two values bracketing a state change.
    :param t2: The other value that brackets a state change.
    :param s1: State at t1.
    :param s2: State at t2.
    :return: New value at which to check for transition.
    """
    t1 = ctypes.c_double(t1)
    t2 = ctypes.c_double(t2)
    s1 = ctypes.c_int(s1)
    s2 = ctypes.c_int(s2)
    t = ctypes.c_double()
    libspice.gfrefn_c(t1, t2, s1, s2, ctypes.byref(t))
    return t.value


@spice_error_check
def gfrepf() -> None:
    """
    Finish a GF progress report.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfrepf_c.html

    """
    libspice.gfrepf_c()


@spice_error_check
def gfrepi(
    window: Union[SpiceCell, SpiceCellPointer], begmss: str, endmss: str
) -> None:
    """
    This entry point initializes a search progress report.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfrepi_c.html

    :param window: A window over which a job is to be performed.
    :param begmss: Beginning of the text portion of the output message.
    :param endmss: End of the text portion of the output message.
    """
    begmss = stypes.string_to_char_p(begmss)
    endmss = stypes.string_to_char_p(endmss)
    # don't do anything if we were given a pointer to a SpiceCell, like if we were in a callback
    if not isinstance(window, SpiceCellPointer):
        assert isinstance(window, stypes.SpiceCell)
        assert window.is_double()
        window = ctypes.byref(window)
    libspice.gfrepi_c(window, begmss, endmss)


@spice_error_check
def gfrepu(ivbeg: float, ivend: float, time: float) -> None:
    """
    This function tells the progress reporting system
    how far a search has progressed.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfrepu_c.html

    :param ivbeg: Start time of work interval.
    :param ivend: End time of work interval.
    :param time: Current time being examined in the search process.
    """
    ivbeg = ctypes.c_double(ivbeg)
    ivend = ctypes.c_double(ivend)
    time = ctypes.c_double(time)
    libspice.gfrepu_c(ivbeg, ivend, time)


@spice_error_check
def gfrfov(
    inst: str,
    raydir: ndarray,
    rframe: str,
    abcorr: str,
    obsrvr: str,
    step: float,
    cnfine: SpiceCell,
    result: Optional[SpiceCell] = None,
) -> SpiceCell:
    """
    Determine time intervals when a specified ray intersects the
    space bounded by the field-of-view (FOV) of a specified
    instrument.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfrfov_c.html

    :param inst: Name of the instrument.
    :param raydir: Ray's direction vector.
    :param rframe: Reference frame of ray's direction vector.
    :param abcorr: Aberration correction flag.
    :param obsrvr: Name of the observing body.
    :param step: Step size in seconds for finding FOV events.
    :param cnfine: SPICE window to which the search is restricted.
    :param result: Optional SPICE window containing results.
    """
    assert isinstance(cnfine, stypes.SpiceCell)
    assert cnfine.is_double()
    if result is None:
        result = stypes.SPICEDOUBLE_CELL(2000)
    else:
        assert isinstance(result, stypes.SpiceCell)
        assert result.is_double()
    inst = stypes.string_to_char_p(inst)
    raydir = stypes.to_double_vector(raydir)
    rframe = stypes.string_to_char_p(rframe)
    abcorr = stypes.string_to_char_p(abcorr)
    obsrvr = stypes.string_to_char_p(obsrvr)
    step = ctypes.c_double(step)
    libspice.gfrfov_c(
        inst,
        raydir,
        rframe,
        abcorr,
        obsrvr,
        step,
        ctypes.byref(cnfine),
        ctypes.byref(result),
    )
    return result


@spice_error_check
def gfrr(
    target: str,
    abcorr: str,
    obsrvr: str,
    relate: str,
    refval: float,
    adjust: float,
    step: float,
    nintvls: int,
    cnfine: SpiceCell,
    result: SpiceCell,
) -> SpiceCell:
    """
    Determine time intervals for which a specified constraint
    on the observer-target range rate is met.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfrr_c.html

    :param target: Name of the target body.
    :param abcorr: Aberration correction flag.
    :param obsrvr: Name of the observing body.
    :param relate: Relational operator.
    :param refval: Reference value.
    :param adjust: Adjustment value for absolute extrema searches.
    :param step: Step size used for locating extrema and roots.
    :param nintvls: Workspace window interval count.
    :param cnfine: SPICE window to which the search is restricted.
    :param result: Optional SPICE window containing results.
    """
    assert isinstance(cnfine, stypes.SpiceCell)
    assert cnfine.is_double()
    if result is None:
        result = stypes.SPICEDOUBLE_CELL(2000)
    else:
        assert isinstance(result, stypes.SpiceCell)
        assert result.is_double()
    target = stypes.string_to_char_p(target)
    abcorr = stypes.string_to_char_p(abcorr)
    obsrvr = stypes.string_to_char_p(obsrvr)
    relate = stypes.string_to_char_p(relate)
    refval = ctypes.c_double(refval)
    adjust = ctypes.c_double(adjust)
    step = ctypes.c_double(step)
    nintvls = ctypes.c_int(nintvls)
    libspice.gfrr_c(
        target,
        abcorr,
        obsrvr,
        relate,
        refval,
        adjust,
        step,
        nintvls,
        ctypes.byref(cnfine),
        ctypes.byref(result),
    )
    return result


@spice_error_check
def gfsep(
    targ1: str,
    shape1: str,
    inframe1: str,
    targ2: str,
    shape2: str,
    inframe2: str,
    abcorr: str,
    obsrvr: str,
    relate: str,
    refval: float,
    adjust: float,
    step: float,
    nintvls: int,
    cnfine: SpiceCell,
    result: Optional[SpiceCell] = None,
) -> SpiceCell:
    """
    Determine time intervals when the angular separation between
    the position vectors of two target bodies relative to an observer
    satisfies a numerical relationship.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfsep_c.html

    :param targ1: Name of first body.
    :param shape1: Name of shape model describing the first body.
    :param inframe1: The body-fixed reference frame of the first body.
    :param targ2: Name of second body.
    :param shape2: Name of the shape model describing the second body.
    :param inframe2: The body-fixed reference frame of the second body
    :param abcorr: Aberration correction flag
    :param obsrvr: Name of the observing body.
    :param relate: Relational operator.
    :param refval: Reference value.
    :param adjust: Absolute extremum adjustment value.
    :param step: Step size in seconds for finding angular separation events.
    :param nintvls: Workspace window interval count.
    :param cnfine: SPICE window to which the search is restricted.
    :param result: Optional SPICE window containing results.
    """
    assert isinstance(cnfine, stypes.SpiceCell)
    assert cnfine.is_double()
    if result is None:
        result = stypes.SPICEDOUBLE_CELL(2000)
    else:
        assert isinstance(result, stypes.SpiceCell)
        assert result.is_double()
    targ1 = stypes.string_to_char_p(targ1)
    shape1 = stypes.string_to_char_p(shape1)
    inframe1 = stypes.string_to_char_p(inframe1)
    targ2 = stypes.string_to_char_p(targ2)
    shape2 = stypes.string_to_char_p(shape2)
    inframe2 = stypes.string_to_char_p(inframe2)
    abcorr = stypes.string_to_char_p(abcorr)
    obsrvr = stypes.string_to_char_p(obsrvr)
    relate = stypes.string_to_char_p(relate)
    refval = ctypes.c_double(refval)
    adjust = ctypes.c_double(adjust)
    step = ctypes.c_double(step)
    nintvls = ctypes.c_int(nintvls)
    libspice.gfsep_c(
        targ1,
        shape1,
        inframe1,
        targ2,
        shape2,
        inframe2,
        abcorr,
        obsrvr,
        relate,
        refval,
        adjust,
        step,
        nintvls,
        ctypes.byref(cnfine),
        ctypes.byref(result),
    )
    return result


@spice_error_check
def gfsntc(
    target: str,
    fixref: str,
    method: str,
    abcorr: str,
    obsrvr: str,
    dref: str,
    dvec: Union[ndarray, Iterable[float]],
    crdsys: str,
    coord: str,
    relate: str,
    refval: float,
    adjust: float,
    step: float,
    nintvls: int,
    cnfine: SpiceCell,
    result: Optional[SpiceCell] = None,
) -> SpiceCell:
    """
    Determine time intervals for which a coordinate of an
    surface intercept position vector satisfies a numerical constraint.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfsntc_c.html

    :param target: Name of the target body.
    :param fixref: Body fixed frame associated with the target.
    :param method: Name of method type for surface intercept calculation.
    :param abcorr: Aberration correction flag
    :param obsrvr: Name of the observing body.
    :param dref: Reference frame of direction vector of dvec.
    :param dvec: Pointing direction vector from the observer.
    :param crdsys: Name of the coordinate system containing COORD.
    :param coord: Name of the coordinate of interest
    :param relate: Relational operator.
    :param refval: Reference value.
    :param adjust: Absolute extremum adjustment value.
    :param step: Step size in seconds for finding angular separation events.
    :param nintvls: Workspace window interval count.
    :param cnfine: SPICE window to which the search is restricted.
    :param result: Optional SPICE window containing results.
    """
    assert isinstance(cnfine, stypes.SpiceCell)
    assert cnfine.is_double()
    if result is None:
        result = stypes.SPICEDOUBLE_CELL(2000)
    else:
        assert isinstance(result, stypes.SpiceCell)
        assert result.is_double()
    target = stypes.string_to_char_p(target)
    fixref = stypes.string_to_char_p(fixref)
    method = stypes.string_to_char_p(method)
    abcorr = stypes.string_to_char_p(abcorr)
    obsrvr = stypes.string_to_char_p(obsrvr)
    dref = stypes.string_to_char_p(dref)
    dvec = stypes.to_double_vector(dvec)
    crdsys = stypes.string_to_char_p(crdsys)
    coord = stypes.string_to_char_p(coord)
    relate = stypes.string_to_char_p(relate)
    refval = ctypes.c_double(refval)
    adjust = ctypes.c_double(adjust)
    step = ctypes.c_double(step)
    nintvls = ctypes.c_int(nintvls)
    libspice.gfsntc_c(
        target,
        fixref,
        method,
        abcorr,
        obsrvr,
        dref,
        dvec,
        crdsys,
        coord,
        relate,
        refval,
        adjust,
        step,
        nintvls,
        ctypes.byref(cnfine),
        ctypes.byref(result),
    )
    return result


@spice_error_check
def gfsstp(step: float) -> None:
    """
    Set the step size to be returned by :func:`gfstep`.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfsstp_c.html

    :param step: Time step to take.
    """
    step = ctypes.c_double(step)
    libspice.gfsstp_c(step)


@spice_error_check
def gfstep(time: float) -> float:
    """
    Return the time step set by the most recent call to :func:`gfsstp`.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfstep_c.html

    :param time: Ignored ET value.
    :return: Time step to take.
    """
    time = ctypes.c_double(time)
    step = ctypes.c_double()
    libspice.gfstep_c(time, ctypes.byref(step))
    return step.value


@spice_error_check
def gfstol(value: float) -> None:
    """
    Override the default GF convergence
    value used in the high level GF routines.

    Default value is 1.0e-6

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfstol_c.html

    :param value: Double precision value returned or to store.
    """
    value = ctypes.c_double(value)
    libspice.gfstol_c(value)


@spice_error_check
def gfsubc(
    target: str,
    fixref: str,
    method: str,
    abcorr: str,
    obsrvr: str,
    crdsys: str,
    coord: str,
    relate: str,
    refval: float,
    adjust: float,
    step: float,
    nintvls: int,
    cnfine: SpiceCell,
    result: SpiceCell,
) -> SpiceCell:
    """
    Determine time intervals for which a coordinate of an
    subpoint position vector satisfies a numerical constraint.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfsubc_c.html

    :param target: Name of the target body.
    :param fixref: Body fixed frame associated with the target.
    :param method: Name of method type for subpoint calculation.
    :param abcorr: Aberration correction flag
    :param obsrvr: Name of the observing body.
    :param crdsys: Name of the coordinate system containing COORD.
    :param coord: Name of the coordinate of interest
    :param relate: Relational operator.
    :param refval: Reference value.
    :param adjust: Adjustment value for absolute extrema searches.
    :param step: Step size used for locating extrema and roots.
    :param nintvls: Workspace window interval count.
    :param cnfine: SPICE window to which the search is restricted.
    :param result: Optional SPICE window containing results.
    """
    assert isinstance(cnfine, stypes.SpiceCell)
    assert cnfine.is_double()
    if result is None:
        result = stypes.SPICEDOUBLE_CELL(2000)
    else:
        assert isinstance(result, stypes.SpiceCell)
        assert result.is_double()
    target = stypes.string_to_char_p(target)
    fixref = stypes.string_to_char_p(fixref)
    method = stypes.string_to_char_p(method)
    abcorr = stypes.string_to_char_p(abcorr)
    obsrvr = stypes.string_to_char_p(obsrvr)
    crdsys = stypes.string_to_char_p(crdsys)
    coord = stypes.string_to_char_p(coord)
    relate = stypes.string_to_char_p(relate)
    refval = ctypes.c_double(refval)
    adjust = ctypes.c_double(adjust)
    step = ctypes.c_double(step)
    nintvls = ctypes.c_int(nintvls)
    libspice.gfsubc_c(
        target,
        fixref,
        method,
        abcorr,
        obsrvr,
        crdsys,
        coord,
        relate,
        refval,
        adjust,
        step,
        nintvls,
        ctypes.byref(cnfine),
        ctypes.byref(result),
    )
    return result


@spice_error_check
def gftfov(
    inst: str,
    target: str,
    tshape: str,
    tframe: str,
    abcorr: str,
    obsrvr: str,
    step: float,
    cnfine: SpiceCell,
    result: Optional[SpiceCell] = None,
) -> SpiceCell:
    """
    Determine time intervals when a specified ephemeris object
    intersects the space bounded by the field-of-view (FOV) of a
    specified instrument.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gftfov_c.html

    :param inst: Name of the instrument.
    :param target: Name of the target body.
    :param tshape: Type of shape model used for target body.
    :param tframe: Body-fixed, body-centered frame for target body.
    :param abcorr: Aberration correction flag.
    :param obsrvr: Name of the observing body.
    :param step: Step size in seconds for finding FOV events.
    :param cnfine: SPICE window to which the search is restricted.
    :param result: Optional pass-in SpiceCell for results
    :return: SpiceCell containing set of time  intervals, within the confinement period, when the target body is visible
    """
    assert isinstance(cnfine, stypes.SpiceCell)
    assert cnfine.is_double()
    if result is None:
        result = stypes.SPICEDOUBLE_CELL(20000)
    else:
        assert isinstance(result, stypes.SpiceCell)
        assert result.is_double()
    inst = stypes.string_to_char_p(inst)
    target = stypes.string_to_char_p(target)
    tshape = stypes.string_to_char_p(tshape)
    tframe = stypes.string_to_char_p(tframe)
    abcorr = stypes.string_to_char_p(abcorr)
    obsrvr = stypes.string_to_char_p(obsrvr)
    step = ctypes.c_double(step)
    libspice.gftfov_c(
        inst,
        target,
        tshape,
        tframe,
        abcorr,
        obsrvr,
        step,
        ctypes.byref(cnfine),
        ctypes.byref(result),
    )
    return result


@spice_error_check
def gfudb(
    udfuns: UDFUNS, udfunb: UDFUNB, step: float, cnfine: SpiceCell, result: SpiceCell
):
    """
    Perform a GF search on a user defined boolean quantity.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfudb_c.html

    :param udfuns: Name of the routine that computes a scalar quantity of interest corresponding to an 'et'.
    :param udfunb: Name of the routine returning the boolean value corresponding to an 'et'.
    :param step: Step size used for locating extrema and roots.
    :param cnfine: SPICE window to which the search is restricted.
    :param result: SPICE window containing results.
    :return: result
    """
    step = ctypes.c_double(step)
    libspice.gfudb_c(udfuns, udfunb, step, ctypes.byref(cnfine), ctypes.byref(result))


@spice_error_check
def gfuds(
    udfuns: UDFUNS,
    udqdec: UDFUNB,
    relate: str,
    refval: float,
    adjust: float,
    step: float,
    nintvls: int,
    cnfine: SpiceCell,
    result: SpiceCell,
) -> SpiceCell:
    """
    Perform a GF search on a user defined scalar quantity.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfuds_c.html

    :param udfuns: Name of the routine that computes the scalar quantity of interest at some time.
    :param udqdec: Name of the routine that computes whether the scalar quantity is decreasing.
    :param relate: Operator that either looks for an extreme value (max, min, local, absolute) or compares the geometric quantity value and a number.
    :param refval: Value used as reference for scalar quantity condition.
    :param adjust: Allowed variation for absolute extremal geometric conditions.
    :param step: Step size used for locating extrema and roots.
    :param nintvls: Workspace window interval count.
    :param cnfine: SPICE window to which the search is restricted.
    :param result: SPICE window containing results.
    :return: result
    """
    relate = stypes.string_to_char_p(relate)
    refval = ctypes.c_double(refval)
    adjust = ctypes.c_double(adjust)
    step = ctypes.c_double(step)
    nintvls = ctypes.c_int(nintvls)
    libspice.gfuds_c(
        udfuns,
        udqdec,
        relate,
        refval,
        adjust,
        step,
        nintvls,
        ctypes.byref(cnfine),
        ctypes.byref(result),
    )
    return result


@spice_error_check
@spice_found_exception_thrower
def gipool(name: str, start: int, room: int) -> Tuple[ndarray, bool]:
    """
    Return the integer value of a kernel variable from the kernel pool.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gipool_c.html

    :param name: Name of the variable whose value is to be returned.
    :param start: Which component to start retrieving for name.
    :param room: The largest number of values to return.
    :return: Values associated with name.
    """
    name = stypes.string_to_char_p(name)
    start = ctypes.c_int(start)
    ivals = stypes.empty_int_vector(room)
    room = ctypes.c_int(room)
    n = ctypes.c_int()
    found = ctypes.c_int()
    libspice.gipool_c(name, start, room, ctypes.byref(n), ivals, ctypes.byref(found))
    return stypes.c_vector_to_python(ivals)[0 : n.value], bool(found.value)


@spice_error_check
@spice_found_exception_thrower
def gnpool(
    name: str, start: int, room: int, lenout: int = _default_len_out
) -> Tuple[Iterable[str], bool]:
    """
    Return names of kernel variables matching a specified template.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gnpool_c.html

    :param name: Template that names should match.
    :param start: Index of first matching name to retrieve.
    :param room: The largest number of values to return.
    :param lenout: Length of strings in output array kvars.
    :return: Kernel pool variables whose names match name.
    """
    name = stypes.string_to_char_p(name)
    start = ctypes.c_int(start)
    kvars = stypes.empty_char_array(y_len=room, x_len=lenout)
    room = ctypes.c_int(room)
    lenout = ctypes.c_int(lenout)
    n = ctypes.c_int()
    found = ctypes.c_int()
    libspice.gnpool_c(
        name, start, room, lenout, ctypes.byref(n), kvars, ctypes.byref(found)
    )
    return stypes.c_vector_to_python(kvars)[0 : n.value], bool(found.value)


################################################################################
# H


@spice_error_check
def halfpi() -> float:
    """
    Return half the value of pi (the ratio of the circumference of
    a circle to its diameter).

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/halfpi_c.html

    :return: Half the value of pi.
    """
    return libspice.halfpi_c()


@spice_error_check
def hrmesp(first: float, step: float, yvals: ndarray, x: float) -> Tuple[float, float]:
    """
    Evaluate, at a specified point, a Hermite interpolating polynomial
    for a specified set of equally spaced abscissa values and
    corresponding pairs of function and function derivative values.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/hrmesp_c.html

    :param first: First abscissa value.
    :param step: Step size.
    :param yvals: Ordinate and derivative values.
    :param x: Point at which to interpolate the polynomial.
    :return: Interpolated function value and derivative at x
    """
    n = ctypes.c_int(int(len(yvals) // 2))
    _first = ctypes.c_double(first)
    _step = ctypes.c_double(step)
    _yvals = stypes.to_double_vector(yvals)
    _x = ctypes.c_double(x)
    f = ctypes.c_double(0)
    df = ctypes.c_double(0)
    libspice.hrmesp_c(n, _first, _step, _yvals, _x, f, df)
    return f.value, df.value


@spice_error_check
def hrmint(
    xvals: Sequence[float], yvals: Sequence[float], x: int
) -> Tuple[float, float]:
    """
    Evaluate a Hermite interpolating polynomial at a specified
    abscissa value.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/hrmint_c.html

    :param xvals: Abscissa values.
    :param yvals: Ordinate and derivative values.
    :param x: Point at which to interpolate the polynomial.
    :return: Interpolated function value at x and the Interpolated function's derivative at x
    """
    work = stypes.empty_double_vector(int(2 * len(yvals) + 1))
    n = ctypes.c_int(len(xvals))
    xvals = stypes.to_double_vector(xvals)
    yvals = stypes.to_double_vector(yvals)
    x = ctypes.c_double(x)
    f = ctypes.c_double(0)
    df = ctypes.c_double(0)
    libspice.hrmint_c(n, xvals, yvals, x, work, f, df)
    return f.value, df.value


@spice_error_check
def hx2dp(string: str) -> Union[float, str]:
    """
    Convert a string representing a double precision number in a
    base 16 scientific notation into its equivalent double
    precision number.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/hx2dp_c.html

    :param string: Hex form string to convert to double precision.
    :return: Double precision value to be returned, Or Error Message.
    """
    string = stypes.string_to_char_p(string)
    lenout = ctypes.c_int(80)
    errmsg = stypes.string_to_char_p(lenout)
    number = ctypes.c_double()
    error = ctypes.c_int()
    libspice.hx2dp_c(string, lenout, ctypes.byref(number), ctypes.byref(error), errmsg)
    if not error.value:
        return number.value
    else:
        return stypes.to_python_string(errmsg)


################################################################################
# I


@spice_error_check
def ident() -> ndarray:
    """
    This routine returns the 3x3 identity matrix.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ident_c.html

    :return: The 3x3 identity matrix.
    """
    matrix = stypes.empty_double_matrix()
    libspice.ident_c(matrix)
    return stypes.c_matrix_to_numpy(matrix)


@spice_error_check
def illum(
    target: str, et: float, abcorr: str, obsrvr: str, spoint: ndarray
) -> Tuple[float, float, float]:
    """
    Deprecated: This routine has been superseded by the CSPICE
    routine ilumin. This routine is supported for purposes of
    backward compatibility only.

    Find the illumination angles at a specified surface point of a
    target body.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/illum_c.html

    :param target: Name of target body.
    :param et: Epoch in ephemeris seconds past J2000.
    :param abcorr: Desired aberration correction.
    :param obsrvr: Name of observing body.
    :param spoint: Body-fixed coordinates of a target surface point.
    :return:
            Phase angle,
            Solar incidence angle,
            and Emission angle at the surface point.
    """
    target = stypes.string_to_char_p(target)
    et = ctypes.c_double(et)
    abcorr = stypes.string_to_char_p(abcorr)
    obsrvr = stypes.string_to_char_p(obsrvr)
    spoint = stypes.to_double_vector(spoint)
    phase = ctypes.c_double(0)
    solar = ctypes.c_double(0)
    emissn = ctypes.c_double(0)
    libspice.illum_c(
        target,
        et,
        abcorr,
        obsrvr,
        spoint,
        ctypes.byref(phase),
        ctypes.byref(solar),
        ctypes.byref(emissn),
    )
    return phase.value, solar.value, emissn.value


@spice_error_check
def illumf(
    method: str,
    target: str,
    ilusrc: str,
    et: float,
    fixref: str,
    abcorr: str,
    obsrvr: str,
    spoint: ndarray,
) -> Tuple[float, ndarray, float, float, float, bool, bool]:
    """
    Compute the illumination angles---phase, incidence, and
    emission---at a specified point on a target body. Return logical
    flags indicating whether the surface point is visible from
    the observer's position and whether the surface point is
    illuminated.

    The target body's surface is represented using topographic data
    provided by DSK files, or by a reference ellipsoid.

    The illumination source is a specified ephemeris object.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/illumf_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param ilusrc: Name of illumination source.
    :param et: Epoch in ephemeris seconds past J2000.
    :param fixref: Body-fixed, body-centered target body frame.
    :param abcorr: Desired aberration correction.
    :param obsrvr: Name of observing body.
    :param spoint: Body-fixed coordinates of a target surface point.
    :return: Target surface point epoch, Vector from observer to target
     surface point, Phase angle at the surface point, Source incidence
     angle at the surface point, Emission angle at the surface point,
     Visibility flag, Illumination flag
    """
    method = stypes.string_to_char_p(method)
    target = stypes.string_to_char_p(target)
    ilusrc = stypes.string_to_char_p(ilusrc)
    et = ctypes.c_double(et)
    fixref = stypes.string_to_char_p(fixref)
    abcorr = stypes.string_to_char_p(abcorr)
    obsrvr = stypes.string_to_char_p(obsrvr)
    spoint = stypes.to_double_vector(spoint)
    trgepc = ctypes.c_double(0)
    srfvec = stypes.empty_double_vector(3)
    phase = ctypes.c_double(0)
    incdnc = ctypes.c_double(0)
    emissn = ctypes.c_double(0)
    visibl = ctypes.c_int()
    lit = ctypes.c_int()
    libspice.illumf_c(
        method,
        target,
        ilusrc,
        et,
        fixref,
        abcorr,
        obsrvr,
        spoint,
        ctypes.byref(trgepc),
        srfvec,
        ctypes.byref(phase),
        ctypes.byref(incdnc),
        ctypes.byref(emissn),
        ctypes.byref(visibl),
        ctypes.byref(lit),
    )
    return (
        trgepc.value,
        stypes.c_vector_to_python(srfvec),
        phase.value,
        incdnc.value,
        emissn.value,
        bool(visibl.value),
        bool(lit.value),
    )


@spice_error_check
def illumg(
    method: str,
    target: str,
    ilusrc: str,
    et: float,
    fixref: str,
    abcorr: str,
    obsrvr: str,
    spoint: ndarray,
) -> Tuple[float, ndarray, float, float, float]:
    """
    Find the illumination angles (phase, incidence, and
    emission) at a specified surface point of a target body.

    The surface of the target body may be represented by a triaxial
    ellipsoid or by topographic data provided by DSK files.

    The illumination source is a specified ephemeris object.
    param method: Computation method.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/illumg_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param ilusrc: Name of illumination source.
    :param et: Epoch in ephemeris seconds past J2000.
    :param fixref: Body-fixed, body-centered target body frame.
    :param abcorr: Desired aberration correction.
    :param obsrvr: Name of observing body.
    :param spoint: Body-fixed coordinates of a target surface point.
    :return: Target surface point epoch, Vector from observer to target
     surface point, Phase angle at the surface point, Source incidence
     angle at the surface point, Emission angle at the surface point,
    """
    method = stypes.string_to_char_p(method)
    target = stypes.string_to_char_p(target)
    ilusrc = stypes.string_to_char_p(ilusrc)
    et = ctypes.c_double(et)
    fixref = stypes.string_to_char_p(fixref)
    abcorr = stypes.string_to_char_p(abcorr)
    obsrvr = stypes.string_to_char_p(obsrvr)
    spoint = stypes.to_double_vector(spoint)
    trgepc = ctypes.c_double(0)
    srfvec = stypes.empty_double_vector(3)
    phase = ctypes.c_double(0)
    incdnc = ctypes.c_double(0)
    emissn = ctypes.c_double(0)
    libspice.illumg_c(
        method,
        target,
        ilusrc,
        et,
        fixref,
        abcorr,
        obsrvr,
        spoint,
        ctypes.byref(trgepc),
        srfvec,
        ctypes.byref(phase),
        ctypes.byref(incdnc),
        ctypes.byref(emissn),
    )
    return (
        trgepc.value,
        stypes.c_vector_to_python(srfvec),
        phase.value,
        incdnc.value,
        emissn.value,
    )


@spice_error_check
def ilumin(
    method: str,
    target: str,
    et: float,
    fixref: str,
    abcorr: str,
    obsrvr: str,
    spoint: ndarray,
) -> Tuple[float, ndarray, float, float, float]:
    """
    Find the illumination angles (phase, solar incidence, and
    emission) at a specified surface point of a target body.

    This routine supersedes illum.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ilumin_c.html

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
    method = stypes.string_to_char_p(method)
    target = stypes.string_to_char_p(target)
    et = ctypes.c_double(et)
    fixref = stypes.string_to_char_p(fixref)
    abcorr = stypes.string_to_char_p(abcorr)
    obsrvr = stypes.string_to_char_p(obsrvr)
    spoint = stypes.to_double_vector(spoint)
    trgepc = ctypes.c_double(0)
    srfvec = stypes.empty_double_vector(3)
    phase = ctypes.c_double(0)
    solar = ctypes.c_double(0)
    emissn = ctypes.c_double(0)
    libspice.ilumin_c(
        method,
        target,
        et,
        fixref,
        abcorr,
        obsrvr,
        spoint,
        ctypes.byref(trgepc),
        srfvec,
        ctypes.byref(phase),
        ctypes.byref(solar),
        ctypes.byref(emissn),
    )
    return (
        trgepc.value,
        stypes.c_vector_to_python(srfvec),
        phase.value,
        solar.value,
        emissn.value,
    )


@spice_error_check
@spice_found_exception_thrower
def inedpl(a: float, b: float, c: float, plane: Plane) -> Tuple[Ellipse, bool]:
    """
    Find the intersection of a triaxial ellipsoid and a plane.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/inedpl_c.html

    :param a: Length of ellipsoid semi-axis lying on the x-axis.
    :param b: Length of ellipsoid semi-axis lying on the y-axis.
    :param c: Length of ellipsoid semi-axis lying on the z-axis.
    :param plane: Plane that intersects ellipsoid.
    :return: Intersection ellipse.
    """
    assert isinstance(plane, stypes.Plane)
    ellipse = stypes.Ellipse()
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    found = ctypes.c_int()
    libspice.inedpl_c(
        a, b, c, ctypes.byref(plane), ctypes.byref(ellipse), ctypes.byref(found)
    )
    return ellipse, bool(found.value)


@spice_error_check
def inelpl(ellips: Ellipse, plane: Plane) -> Tuple[int, ndarray, ndarray]:
    """
    Find the intersection of an ellipse and a plane.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/inelpl_c.html

    :param ellips: A SPICE ellipse.
    :param plane: A SPICE plane.
    :return:
            Number of intersection points of plane and ellipse,
            Point 1,
            Point 2.
    """
    assert isinstance(plane, stypes.Plane)
    assert isinstance(ellips, stypes.Ellipse)
    nxpts = ctypes.c_int()
    xpt1 = stypes.empty_double_vector(3)
    xpt2 = stypes.empty_double_vector(3)
    libspice.inelpl_c(
        ctypes.byref(ellips), ctypes.byref(plane), ctypes.byref(nxpts), xpt1, xpt2
    )
    return nxpts.value, stypes.c_vector_to_python(xpt1), stypes.c_vector_to_python(xpt2)


@spice_error_check
def inrypl(
    vertex: Iterable[Union[float, float]],
    direct: Iterable[Union[float, float]],
    plane: Plane,
) -> Tuple[int, ndarray]:
    """
    Find the intersection of a ray and a plane.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/inrypl_c.html

    :param vertex: Vertex vector of ray.
    :param direct: Direction vector of ray.
    :param plane: A SPICE plane.
    :return:
            Number of intersection points of ray and plane,
            Intersection point,
            if nxpts == 1.
    """
    assert isinstance(plane, stypes.Plane)
    vertex = stypes.to_double_vector(vertex)
    direct = stypes.to_double_vector(direct)
    nxpts = ctypes.c_int()
    xpt = stypes.empty_double_vector(3)
    libspice.inrypl_c(vertex, direct, ctypes.byref(plane), ctypes.byref(nxpts), xpt)
    return nxpts.value, stypes.c_vector_to_python(xpt)


@spice_error_check
def insrtc(item: Union[str, Iterable[str]], inset: SpiceCell) -> None:
    """
    Insert an item into a character set.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/insrtc_c.html

    :param item: Item to be inserted.
    :param inset: Insertion set.
    """
    assert isinstance(inset, stypes.SpiceCell)
    if stypes.is_iterable(item):
        for c in item:
            libspice.insrtc_c(stypes.string_to_char_p(c), ctypes.byref(inset))
    else:
        item = stypes.string_to_char_p(item)
        libspice.insrtc_c(item, ctypes.byref(inset))


@spice_error_check
def insrtd(item: Union[float, Iterable[float]], inset: SpiceCell) -> None:
    """
    Insert an item into a double precision set.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/insrtd_c.html

    :param item: Item to be inserted.
    :param inset: Insertion set.
    """
    assert isinstance(inset, stypes.SpiceCell)
    if hasattr(item, "__iter__"):
        for d in item:
            libspice.insrtd_c(ctypes.c_double(d), ctypes.byref(inset))
    else:
        item = ctypes.c_double(item)
        libspice.insrtd_c(item, ctypes.byref(inset))


@spice_error_check
def insrti(item: Union[Iterable[int], int], inset: SpiceCell) -> None:
    """
    Insert an item into an integer set.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/insrti_c.html

    :param item: Item to be inserted.
    :param inset: Insertion set.
    """
    assert isinstance(inset, stypes.SpiceCell)
    if hasattr(item, "__iter__"):
        for i in item:
            libspice.insrti_c(ctypes.c_int(i), ctypes.byref(inset))
    else:
        item = ctypes.c_int(item)
        libspice.insrti_c(item, ctypes.byref(inset))


@spice_error_check
def inter(a: SpiceCell, b: SpiceCell) -> SpiceCell:
    """
    Intersect two sets of any data type to form a third set.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/inter_c.html

    :param a: First input set.
    :param b: Second input set.
    :return: Intersection of a and b.
    """
    assert isinstance(a, stypes.SpiceCell)
    assert isinstance(b, stypes.SpiceCell)
    assert a.dtype == b.dtype
    # Next line was redundant with [raise NotImpImplementedError] below
    # assert a.dtype == 0 or a.dtype == 1 or a.dtype == 2
    if a.dtype == 0:
        c = stypes.SPICECHAR_CELL(max(a.size, b.size), max(a.length, b.length))
    elif a.dtype == 1:
        c = stypes.SPICEDOUBLE_CELL(max(a.size, b.size))
    elif a.dtype == 2:
        c = stypes.SPICEINT_CELL(max(a.size, b.size))
    else:
        raise NotImplementedError
    libspice.inter_c(ctypes.byref(a), ctypes.byref(b), ctypes.byref(c))
    return c


@spice_error_check
def intmax() -> int:
    """
    Return the value of the largest (positive) number representable
    in a int variable.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/intmax_c.html

    :return: The largest (positive) number representablein a Int variable.
    """
    return libspice.intmax_c()


@spice_error_check
def intmin() -> int:
    """
    Return the value of the smallest (negative) number representable
    in a SpiceInt variable.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/intmin_c.html

    :return: The smallest (negative) number representablein a Int variable.
    """
    return libspice.intmin_c()


@spice_error_check
def invert(m: ndarray) -> ndarray:
    """
    Generate the inverse of a 3x3 matrix.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/invert_c.html

    :param m: Matrix to be inverted.
    :return: Inverted matrix (m1)^-1
    """
    m = stypes.to_double_matrix(m)
    mout = stypes.empty_double_matrix()
    libspice.invert_c(m, mout)
    return stypes.c_matrix_to_numpy(mout)


@spice_error_check
def invort(m: ndarray) -> ndarray:
    """
    Given a matrix, construct the matrix whose rows are the
    columns of the first divided by the length squared of the
    the corresponding columns of the input matrix.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/invort_c.html

    :param m: A 3x3 Matrix.
    :return: m after transposition and scaling of rows.
    """
    m = stypes.to_double_matrix(m)
    mout = stypes.empty_double_matrix()
    libspice.invort_c(m, mout)
    return stypes.c_matrix_to_numpy(mout)


@spice_error_check
def invstm(mat: ndarray) -> ndarray:
    """
    Return the inverse of a state transformation matrix.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/invstm_c.html

    :param mat: A state transformation matrix.
    :return: The inverse of `mat'.
    """
    _mat = stypes.to_double_matrix(mat)
    mout = stypes.empty_double_matrix(6, 6)
    libspice.invstm_c(_mat, mout)
    return stypes.c_matrix_to_numpy(mout)


@spice_error_check
def irfnam(index: int) -> str:
    """
    Return the name of one of the standard inertial reference
    frames supported by :func:`irfrot`

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/FORTRAN/spicelib/irfnam.html

    :param index: Index of a standard inertial reference frame.
    :return: is the name of the frame.
    """
    index = ctypes.c_int(index)
    name = stypes.string_to_char_p(16)  # just give enough space
    name_len = ctypes.c_int(16)
    libspice.irfnam_(ctypes.byref(index), name, name_len)
    return stypes.to_python_string(name)


@spice_error_check
def irfnum(name: str) -> int:
    """
    Return the index of one of the standard inertial reference
    frames supported by :func:`irfrot`

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/FORTRAN/spicelib/irfnum.html

    :param name: Name of standard inertial reference frame.
    :return: is the index of the frame.
    """
    index = ctypes.c_int()
    name_len = ctypes.c_int(len(name))
    name = stypes.string_to_char_p(name)
    libspice.irfnum_(name, ctypes.byref(index), name_len)
    return index.value


@spice_error_check
def irfrot(refa: int, refb: int) -> ndarray:
    """
    Compute the matrix needed to rotate vectors between two
    standard inertial reference frames.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/FORTRAN/spicelib/irfrot.html

    :param refa: index of first reference frame.
    :param refb: index of second reference frame.
    :return: rotation from frame A to frame B.
    """
    refa = ctypes.c_int(refa)
    refb = ctypes.c_int(refb)
    rotab = stypes.empty_double_matrix()
    libspice.irfrot_(ctypes.byref(refa), ctypes.byref(refb), rotab)
    # make sure to transpose to get back into c order from fortran ordering
    return stypes.c_matrix_to_numpy(rotab).T


@spice_error_check
def irftrn(refa: str, refb: str) -> ndarray:
    """
    Return the matrix that transforms vectors from one specified
    inertial reference frame to another.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/FORTRAN/spicelib/irftrn.html

    :param refa: Name of reference frame to transform vectors FROM.
    :param refb: Name of reference frame to transform vectors TO.
    :return: REFA-to-REFB transformation matrix.
    """
    len_a = ctypes.c_int(len(refa))
    len_b = ctypes.c_int(len(refb))
    refa = stypes.string_to_char_p(refa)
    refb = stypes.string_to_char_p(refb)
    rotab = stypes.empty_double_matrix()
    libspice.irftrn_(refa, refb, rotab, len_a, len_b)
    # make sure to transpose to get back into c order from fortran ordering
    return stypes.c_matrix_to_numpy(rotab).T


@spice_error_check
def isordv(array: Union[ndarray, Iterable[int]], n: int) -> bool:
    """
    Determine whether an array of n items contains the integers
    0 through n-1.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/isordv_c.html

    :param array: Array of integers.
    :param n: Number of integers in array.
    :return:
            The function returns True if the array contains the
            integers 0 through n-1, otherwise it returns False.
    """
    array = stypes.to_int_vector(array)
    n = ctypes.c_int(n)
    return bool(libspice.isordv_c(array, n))


@spice_error_check
def isrchc(value: str, ndim: int, lenvals: int, array: Iterable[str]) -> int:
    """
    Search for a given value within a character string array. Return
    the index of the first matching array entry, or -1 if the key
    value was not found.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/isrchc_c.html

    :param value: Key value to be found in array.
    :param ndim: Dimension of array.
    :param lenvals: String length.
    :param array: Character string array to search.
    :return:
            The index of the first matching array element or -1
            if the value is not found.
    """
    value = stypes.string_to_char_p(value)
    array = stypes.list_to_char_array_ptr(array, x_len=lenvals, y_len=ndim)
    ndim = ctypes.c_int(ndim)
    lenvals = ctypes.c_int(lenvals)
    return libspice.isrchc_c(value, ndim, lenvals, array)


@spice_error_check
def isrchd(value: float, ndim: int, array: Union[ndarray, Iterable[float]]) -> int:
    """
    Search for a given value within a double precision array. Return
    the index of the first matching array entry, or -1 if the key value
    was not found.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/isrchd_c.html

    :param value: Key value to be found in array.
    :param ndim: Dimension of array.
    :param array: Double Precision array to search.
    :return:
            The index of the first matching array element or -1
            if the value is not found.
    """
    value = ctypes.c_double(value)
    ndim = ctypes.c_int(ndim)
    array = stypes.to_double_vector(array)
    return libspice.isrchd_c(value, ndim, array)


@spice_error_check
def isrchi(value: int, ndim: int, array: Union[ndarray, Iterable[int]]) -> int:
    """
    Search for a given value within an integer array. Return
    the index of the first matching array entry, or -1 if the key
    value was not found.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/isrchi_c.html

    :param value: Key value to be found in array.
    :param ndim: Dimension of array.
    :param array: Integer array to search.
    :return:
            The index of the first matching array element or -1
            if the value is not found.
    """
    value = ctypes.c_int(value)
    ndim = ctypes.c_int(ndim)
    array = stypes.to_int_vector(array)
    return libspice.isrchi_c(value, ndim, array)


@spice_error_check
def isrot(m: ndarray, ntol: float, dtol: float) -> bool:
    """
    Indicate whether a 3x3 matrix is a rotation matrix.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/isrot_c.html

    :param m: A matrix to be tested.
    :param ntol: Tolerance for the norms of the columns of m.
    :param dtol:
                Tolerance for the determinant of a matrix whose columns
                are the unitized columns of m.
    :return: True if and only if m is a rotation matrix.
    """
    m = stypes.to_double_matrix(m)
    ntol = ctypes.c_double(ntol)
    dtol = ctypes.c_double(dtol)
    return bool(libspice.isrot_c(m, ntol, dtol))


@spice_error_check
def iswhsp(string: str) -> bool:
    """
    Return a boolean value indicating whether a string contains
    only white space characters.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/iswhsp_c.html

    :param string: String to be tested.
    :return:
            the boolean value True if the string is empty or contains
            only white space characters; otherwise it returns the value False.
    """
    string = stypes.string_to_char_p(string)
    return bool(libspice.iswhsp_c(string))


################################################################################
# J


@spice_error_check
def j1900() -> float:
    """
    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/j1900_c.html

    :return: Julian Date of 1899 DEC 31 12:00:00
    """
    return libspice.j1900_c()


@spice_error_check
def j1950() -> float:
    """
    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/j1950_c.html

    :return: Julian Date of 1950 JAN 01 00:00:00
    """
    return libspice.j1950_c()


@spice_error_check
def j2000() -> float:
    """
    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/j2000_c.html

    :return: Julian Date of 2000 JAN 01 12:00:00
    """
    return libspice.j2000_c()


@spice_error_check
def j2100() -> float:
    """
    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/j2100_c.html

    :return: Julian Date of 2100 JAN 01 12:00:00
    """
    return libspice.j2100_c()


@spice_error_check
def jyear() -> float:
    """
    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/jyear_c.html

    :return: number of seconds in a julian year
    """
    return libspice.jyear_c()


################################################################################
# K


@spice_error_check
def kclear() -> None:
    """
    Clear the KEEPER subsystem: unload all kernels, clear the kernel
    pool, and re-initialize the subsystem. Existing watches on kernel
    variables are retained.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/kclear_c.html

    """
    libspice.kclear_c()


@spice_error_check
@spice_found_exception_thrower
def kdata(
    which: int,
    kind: str,
    fillen: int = _default_len_out,
    typlen: int = _default_len_out,
    srclen: int = _default_len_out,
) -> Tuple[str, str, str, int, bool]:
    """
    Return data for the nth kernel that is among a list of specified
    kernel types.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/kdata_c.html

    :param which: Index of kernel to fetch from the list of kernels.
    :param kind: The kind of kernel to which fetches are limited.
    :param fillen: Available space in output file string.
    :param typlen: Available space in output kernel type string.
    :param srclen: Available space in output source string.
    :return:
            The name of the kernel file, The type of the kernel,
            Name of the source file used to load file,
            The handle attached to file.
    """
    which = ctypes.c_int(which)
    kind = stypes.string_to_char_p(kind)
    fillen = ctypes.c_int(fillen)
    typlen = ctypes.c_int(typlen)
    srclen = ctypes.c_int(srclen)
    file = stypes.string_to_char_p(fillen)
    filtyp = stypes.string_to_char_p(typlen)
    source = stypes.string_to_char_p(srclen)
    handle = ctypes.c_int()
    found = ctypes.c_int()
    libspice.kdata_c(
        which,
        kind,
        fillen,
        typlen,
        srclen,
        file,
        filtyp,
        source,
        ctypes.byref(handle),
        ctypes.byref(found),
    )
    return (
        stypes.to_python_string(file),
        stypes.to_python_string(filtyp),
        stypes.to_python_string(source),
        handle.value,
        bool(found.value),
    )


@spice_error_check
def kepleq(ml: float, h: float, k: float) -> float:
    """
    This function solves the equinoctial version of Kepler's equation.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/FORTRAN/spicelib/kepleq.html

    :param ml: Mean longitude
    :param h: h component of equinoctial elements
    :param k: k component of equinoctial elements
    :return: the value of F such that ML = F + h*COS(F) - k*SIN(F)
    """
    ml = ctypes.c_double(ml)
    h = ctypes.c_double(h)
    k = ctypes.c_double(k)
    f = libspice.kepleq_(ctypes.byref(ml), ctypes.byref(h), ctypes.byref(k))
    return f


@spice_error_check
@spice_found_exception_thrower
def kinfo(
    file: str, typlen: int = _default_len_out, srclen: int = _default_len_out
) -> Tuple[str, str, int, bool]:
    """
    Return information about a loaded kernel specified by name.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/kinfo_c.html

    :param file: Name of a kernel to fetch information for
    :param typlen: Available space in output kernel type string.
    :param srclen: Available space in output source string.
    :return:
            The type of the kernel,
            Name of the source file used to load file,
            The handle attached to file.
    """
    typlen = ctypes.c_int(typlen)
    srclen = ctypes.c_int(srclen)
    file = stypes.string_to_char_p(file)
    filtyp = stypes.string_to_char_p(" " * typlen.value)
    source = stypes.string_to_char_p(" " * srclen.value)
    handle = ctypes.c_int()
    found = ctypes.c_int()
    libspice.kinfo_c(
        file, typlen, srclen, filtyp, source, ctypes.byref(handle), ctypes.byref(found)
    )
    return (
        stypes.to_python_string(filtyp),
        stypes.to_python_string(source),
        handle.value,
        bool(found.value),
    )


@spice_error_check
def kplfrm(frmcls: int, out_cell: Optional[SpiceCell] = None) -> SpiceCell:
    """
    Return a SPICE set containing the frame IDs of all reference
    frames of a given class having specifications in the kernel pool.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/kplfrm_c.html

    :param frmcls: Frame class.
    :param out_cell: Optional output Spice Int Cell
    :return: Set of ID codes of frames of the specified class.
    """
    if not out_cell:
        out_cell = stypes.SPICEINT_CELL(1000)
    frmcls = ctypes.c_int(frmcls)
    libspice.kplfrm_c(frmcls, ctypes.byref(out_cell))
    return out_cell


@spice_error_check
def kpsolv(evec: Tuple[float, float]) -> float:
    """
    This routine solves the equation X = < EVEC, U(X) > where
    U(X) is the unit vector [ Cos(X), SIN(X) ] and  < , > denotes
    the two-dimensional dot product.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/FORTRAN/spicelib/kpsolv.html

    :param evec: A 2-vector whose magnitude is less than 1.
    :return: the value of X such that X = EVEC(1)COS(X) + EVEC(2)SIN(X).
    """
    evec = stypes.to_double_vector(evec)
    x = libspice.kpsolv_(evec)
    return x


@spice_error_check
def ktotal(kind: str) -> int:
    """
    Return the current number of kernels that have been loaded
    via the KEEPER interface that are of a specified type.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ktotal_c.html

    :param kind: A list of kinds of kernels to count.
    :return: The number of kernels of type kind.
    """
    kind = stypes.string_to_char_p(kind)
    count = ctypes.c_int()
    libspice.ktotal_c(kind, ctypes.byref(count))
    return count.value


@spice_error_check
@spice_found_exception_thrower
def kxtrct(
    keywd: str,
    terms: Sequence[str],
    nterms: int,
    instring: str,
    termlen: int = _default_len_out,
    stringlen: int = _default_len_out,
    substrlen: int = _default_len_out,
) -> Tuple[str, str, bool]:
    """
    Locate a keyword in a string and extract the substring from
    the beginning of the first word following the keyword to the
    beginning of the first subsequent recognized terminator of a list.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/kxtrct_c.html

    :param keywd: Word that marks the beginning of text of interest.
    :param terms: Set of words, any of which marks the end of text.
    :param nterms: Number of terms.
    :param instring: String containing a sequence of words.
    :param termlen: Length of strings in string array term.
    :param stringlen: Available space in argument string.
    :param substrlen: Available space in output substring.
    :return:
            String containing a sequence of words,
            String from end of keywd to beginning of first terms item found.
    """
    assert nterms <= len(terms)
    # Python strings and string arrays => to C char pointers
    keywd = stypes.string_to_char_p(keywd)
    terms = stypes.list_to_char_array_ptr(
        [s[: termlen - 1] for s in terms[:nterms]], x_len=termlen, y_len=nterms
    )
    instring = stypes.string_to_char_p(instring[: stringlen - 1], inlen=stringlen)
    substr = stypes.string_to_char_p(substrlen)
    # Python ints => to C ints
    termlen = ctypes.c_int(termlen)
    nterms = ctypes.c_int(nterms)
    stringlen = ctypes.c_int(stringlen)
    substrlen = ctypes.c_int(substrlen)
    found = ctypes.c_int()
    libspice.kxtrct_c(
        keywd,
        termlen,
        terms,
        nterms,
        stringlen,
        substrlen,
        instring,
        ctypes.byref(found),
        substr,
    )
    return (
        stypes.to_python_string(instring),
        stypes.to_python_string(substr),
        bool(found.value),
    )


################################################################################
# L


@spice_error_check
def lastnb(string: str) -> int:
    """
    Return the zero based index of the last non-blank character in
    a character string.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lastnb_c.html

    :param string: Input character string.
    :return:
    """
    string = stypes.string_to_char_p(string)
    return libspice.lastnb_c(string)


@spice_error_check
def latcyl(radius: float, lon: float, lat: float) -> Tuple[float, float, float]:
    """
    Convert from latitudinal coordinates to cylindrical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/latcyl_c.html

    :param radius: Distance of a point from the origin.
    :param lon: Angle of the point from the XZ plane in radians.
    :param lat: Angle of the point from the XY plane in radians.
    :return: (r, lonc, z)
    """
    radius = ctypes.c_double(radius)
    lon = ctypes.c_double(lon)
    lat = ctypes.c_double(lat)
    r = ctypes.c_double()
    lonc = ctypes.c_double()
    z = ctypes.c_double()
    libspice.latcyl_c(
        radius, lon, lat, ctypes.byref(r), ctypes.byref(lonc), ctypes.byref(z)
    )
    return r.value, lonc.value, z.value


@spice_error_check
def latrec(
    radius: float, longitude: Union[float, float], latitude: Union[float, float]
) -> ndarray:
    """
    Convert from latitudinal coordinates to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/latrec_c.html

    :param radius: Distance of a point from the origin.
    :param longitude: Longitude of point in radians.
    :param latitude: Latitude of point in radians.
    :return: Rectangular coordinates of the point.
    """
    radius = ctypes.c_double(radius)
    longitude = ctypes.c_double(longitude)
    latitude = ctypes.c_double(latitude)
    rectan = stypes.empty_double_vector(3)
    libspice.latrec_c(radius, longitude, latitude, rectan)
    return stypes.c_vector_to_python(rectan)


@spice_error_check
def latsph(radius: float, lon: float, lat: float) -> Tuple[float, float, float]:
    """
    Convert from latitudinal coordinates to spherical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/latsph_c.html

    :param radius: Distance of a point from the origin.
    :param lon: Angle of the point from the XZ plane in radians.
    :param lat: Angle of the point from the XY plane in radians.
    :return: (rho colat, lons)
    """
    radius = ctypes.c_double(radius)
    lon = ctypes.c_double(lon)
    lat = ctypes.c_double(lat)
    rho = ctypes.c_double()
    colat = ctypes.c_double()
    lons = ctypes.c_double()
    libspice.latsph_c(
        radius, lon, lat, ctypes.byref(rho), ctypes.byref(colat), ctypes.byref(lons)
    )
    return rho.value, colat.value, lons.value


@spice_error_check
def latsrf(
    method: str, target: str, et: float, fixref: str, lonlat: Sequence[Sequence[float]]
) -> ndarray:
    """
    Map array of planetocentric longitude/latitude coordinate pairs
    to surface points on a specified target body.

    The surface of the target body may be represented by a triaxial
    ellipsoid or by topographic data provided by DSK files.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/latsrf_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param et: Epoch in TDB seconds past J2000 TDB.
    :param fixref: Body-fixed, body-centered target body frame.
    :param lonlat: Array of longitude/latitude coordinate pairs.
    :return: Array of surface points.
    """
    method = stypes.string_to_char_p(method)
    target = stypes.string_to_char_p(target)
    et = ctypes.c_double(et)
    fixref = stypes.string_to_char_p(fixref)
    npts = ctypes.c_int(len(lonlat))
    lonlat = stypes.to_double_matrix(lonlat)
    srfpts = stypes.empty_double_matrix(3, npts.value)
    libspice.latsrf_c(method, target, et, fixref, npts, lonlat, srfpts)
    return stypes.c_matrix_to_numpy(srfpts)


@spice_error_check
def lcase(instr: str, lenout: int = _default_len_out) -> str:
    """
    Convert the characters in a string to lowercase.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lcase_c.html

    :param instr: Input string.
    :param lenout: Maximum length of output string.
    :return: Output string, all lowercase.
    """
    instr = stypes.string_to_char_p(instr)
    lenout = ctypes.c_int(lenout)
    outstr = stypes.string_to_char_p(lenout)
    libspice.lcase_c(instr, lenout, outstr)
    return stypes.to_python_string(outstr)


@spice_error_check
def ldpool(filename: str) -> None:
    """
    Load the variables contained in a NAIF ASCII kernel file into the
    kernel pool.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ldpool_c.html

    :param filename: Name of the kernel file.
    """
    filename = stypes.string_to_char_p(filename)
    libspice.ldpool_c(filename)


@spice_error_check
def lgresp(first: float, step: float, yvals: ndarray, x: float) -> float:
    """
    Evaluate a Lagrange interpolating polynomial for a specified
    set of coordinate pairs whose first components are equally
    spaced, at a specified abscissa value.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lgresp_c.html

    :param first: First abscissa value.
    :param step: Step Size.
    :param yvals: Ordinate Values.
    :param x: Point at which to interpolate the polynomial.
    :return: The function returns the value at `x' of the unique polynomial of degree n-1 that fits the points in the plane defined by `first', `step', and `yvals'.
    """
    n = ctypes.c_int(len(yvals))
    _first = ctypes.c_double(first)
    _step = ctypes.c_double(step)
    _yvals = stypes.to_double_vector(yvals)
    _x = ctypes.c_double(x)
    return libspice.lgresp_c(n, _first, _step, _yvals, _x)


@spice_error_check
def lgrind(
    xvals: Sequence[float], yvals: Sequence[float], x: float
) -> Tuple[float, float]:
    """
    Evaluate a Lagrange interpolating polynomial for a specified
    set of coordinate pairs, at a specified abscissa value.
    Return the value of both polynomial and derivative.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lgrind_c.html

    :param xvals: Abscissa values.
    :param yvals: Ordinate values.
    :param x: Point at which to interpolate the polynomial.
    :return: Polynomial value at x, Polynomial derivative at x.
    """
    n = ctypes.c_int(len(xvals))
    xvals = stypes.to_double_vector(xvals)
    yvals = stypes.to_double_vector(yvals)
    work = stypes.empty_double_vector(n.value * 2)
    x = ctypes.c_double(x)
    p = ctypes.c_double(0)
    dp = ctypes.c_double(0)
    libspice.lgrind_c(n, xvals, yvals, work, x, p, dp)
    return p.value, dp.value


@spice_error_check
def lgrint(xvals: ndarray, yvals: ndarray, x: float) -> float:
    """
    Evaluate a Lagrange interpolating polynomial for a specified
    set of coordinate pairs, at a specified abscissa value.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lgrint_c.html

    :param xvals: Abscissa values.
    :param yvals: Ordinate values.
    :param x: Point at which to interpolate the polynomial.
    :return: The function returns the value at `x' of the unique polynomial of degree n-1 that fits the points in the plane defined by `xvals' and `yvals'.
    """
    n = ctypes.c_int(len(xvals))
    _xvals = stypes.to_double_vector(xvals)
    _yvals = stypes.to_double_vector(yvals)
    _x = ctypes.c_double(x)
    return libspice.lgrint_c(n, _xvals, _yvals, _x)


@spice_error_check
def limbpt(
    method: str,
    target: str,
    et: float,
    fixref: str,
    abcorr: str,
    corloc: str,
    obsrvr: str,
    refvec: Union[ndarray, Iterable[float]],
    rolstp: float,
    ncuts: int,
    schstp: float,
    soltol: float,
    maxn: int,
) -> Tuple[ndarray, ndarray, ndarray, ndarray]:
    """
    Find limb points on a target body. The limb is the set of points
    of tangency on the target of rays emanating from the observer.
    The caller specifies half-planes bounded by the observer-target
    center vector in which to search for limb points.

    The surface of the target body may be represented either by a
    triaxial ellipsoid or by topographic data.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/limbpt_c.html

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
    :return: Counts of limb points corresponding to cuts, Limb points, Times associated with limb points, Tangent vectors emanating from the observer
    """
    method = stypes.string_to_char_p(method)
    target = stypes.string_to_char_p(target)
    et = ctypes.c_double(et)
    fixref = stypes.string_to_char_p(fixref)
    abcorr = stypes.string_to_char_p(abcorr)
    corloc = stypes.string_to_char_p(corloc)
    obsrvr = stypes.string_to_char_p(obsrvr)
    refvec = stypes.to_double_vector(refvec)
    rolstp = ctypes.c_double(rolstp)
    ncuts = ctypes.c_int(ncuts)
    schstp = ctypes.c_double(schstp)
    soltol = ctypes.c_double(soltol)
    maxn = ctypes.c_int(maxn)
    npts = stypes.empty_int_vector(maxn.value)
    points = stypes.empty_double_matrix(3, maxn.value)
    epochs = stypes.empty_double_vector(maxn)
    tangts = stypes.empty_double_matrix(3, maxn.value)
    libspice.limbpt_c(
        method,
        target,
        et,
        fixref,
        abcorr,
        corloc,
        obsrvr,
        refvec,
        rolstp,
        ncuts,
        schstp,
        soltol,
        maxn,
        npts,
        points,
        epochs,
        tangts,
    )
    # Clip the empty elements out of returned results
    npts = stypes.c_vector_to_python(npts)
    valid_points = numpy.where(npts >= 1)
    return (
        npts[valid_points],
        stypes.c_matrix_to_numpy(points)[valid_points],
        stypes.c_vector_to_python(epochs)[valid_points],
        stypes.c_matrix_to_numpy(tangts)[valid_points],
    )


@spice_error_check
def lmpool(cvals: Union[ndarray, Iterable[str]]) -> None:
    """
    Load the variables contained in an internal buffer into the
    kernel pool.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lmpool_c.html

    :param cvals: list of strings.
    """
    lenvals = ctypes.c_int(len(max(cvals, key=len)) + 1)
    n = ctypes.c_int(len(cvals))
    cvals = stypes.list_to_char_array_ptr(cvals, x_len=lenvals, y_len=n)
    libspice.lmpool_c(cvals, lenvals, n)


@spice_error_check
def lparse(inlist: str, delim: str, nmax: int) -> Iterable[str]:
    """
    Parse a list of items delimited by a single character.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lparse_c.html

    :param inlist: list of items delimited by delim.
    :param delim: Single character used to delimit items.
    :param nmax: Maximum number of items to return.
    :return: Items in the list, left justified.
    """
    delim = stypes.string_to_char_p(delim)
    lenout = ctypes.c_int(len(inlist))
    inlist = stypes.string_to_char_p(inlist)
    nmax = ctypes.c_int(nmax)
    items = stypes.empty_char_array(lenout, nmax)
    n = ctypes.c_int()
    libspice.lparse_c(inlist, delim, nmax, lenout, ctypes.byref(n), ctypes.byref(items))
    return [stypes.to_python_string(x.value) for x in items[0 : n.value]]


@spice_error_check
def lparsm(
    inlist: str, delims: str, nmax: int, lenout: Optional[int] = None
) -> Iterable[str]:
    """
    Parse a list of items separated by multiple delimiters.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lparsm_c.html

    :param inlist: list of items delimited by delims.
    :param delims: Single characters which delimit items.
    :param nmax: Maximum number of items to return.
    :param lenout: Optional Length of strings in item array.
    :return: Items in the list, left justified.
    """
    if lenout is None:
        lenout = ctypes.c_int(len(inlist) + 1)
    else:
        lenout = ctypes.c_int(lenout)
    inlist = stypes.string_to_char_p(inlist)
    delims = stypes.string_to_char_p(delims)
    items = stypes.empty_char_array(lenout.value, nmax)
    nmax = ctypes.c_int(nmax)
    n = ctypes.c_int()
    libspice.lparsm_c(inlist, delims, nmax, lenout, ctypes.byref(n), items)
    return [stypes.to_python_string(x.value) for x in items][0 : n.value]


@spice_error_check
def lparss(inlist: str, delims: str, nmax: int = 20, length: int = 50) -> SpiceCell:
    """
    Parse a list of items separated by multiple delimiters, placing the
    resulting items into a set.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lparss_c.html

    :param inlist: list of items delimited by delims.
    :param delims: Single characters which delimit items.
    :param nmax: Optional nmax of spice set.
    :param length: Optional length of strings in spice set
    :return: Set containing items in the list, left justified.
    """
    inlist = stypes.string_to_char_p(inlist)
    delims = stypes.string_to_char_p(delims)
    return_set = stypes.SPICECHAR_CELL(nmax, length)
    libspice.lparss_c(inlist, delims, ctypes.byref(return_set))
    return return_set


@spice_error_check
def lspcn(body: str, et: float, abcorr: str) -> float:
    """
    Compute L_s, the planetocentric longitude of the sun, as seen
    from a specified body.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lspcn_c.html

    :param body: Name of central body.
    :param et: Epoch in seconds past J2000 TDB.
    :param abcorr: Aberration correction.
    :return: planetocentric longitude of the sun
    """
    body = stypes.string_to_char_p(body)
    et = ctypes.c_double(et)
    abcorr = stypes.string_to_char_p(abcorr)
    return libspice.lspcn_c(body, et, abcorr)


@spice_error_check
def lstlec(string: str, n: int, lenvals: int, array: Iterable[str]) -> int:
    """
    Given a character string and an ordered array of character
    strings, find the index of the largest array element less than
    or equal to the given string.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lstlec_c.html

    :param string: Upper bound value to search against.
    :param n: Number elements in array.
    :param lenvals: String length.
    :param array: Array of possible lower bounds.
    :return:
            index of the last element of array that is
            lexically less than or equal to string.
    """
    string = stypes.string_to_char_p(string)
    array = stypes.list_to_char_array_ptr(array, x_len=lenvals, y_len=n)
    n = ctypes.c_int(n)
    lenvals = ctypes.c_int(lenvals)
    return libspice.lstlec_c(string, n, lenvals, array)


@spice_error_check
def lstled(x: float, n: int, array: Union[ndarray, Iterable[float]]) -> int:
    """
    Given a number x and an array of non-decreasing floats
    find the index of the largest array element less than or equal to x.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lstled_c.html

    :param x: Value to search against.
    :param n: Number elements in array.
    :param array: Array of possible lower bounds
    :return: index of the last element of array that is less than or equal to x.
    """
    array = stypes.to_double_vector(array)
    x = ctypes.c_double(x)
    n = ctypes.c_int(n)
    return libspice.lstled_c(x, n, array)


@spice_error_check
def lstlei(x: int, n: int, array: Union[ndarray, Iterable[int]]) -> int:
    """
    Given a number x and an array of non-decreasing ints,
    find the index of the largest array element less than or equal to x.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lstlei_c.html

    :param x: Value to search against.
    :param n: Number elements in array.
    :param array: Array of possible lower bounds
    :return: index of the last element of array that is less than or equal to x.
    """
    array = stypes.to_int_vector(array)
    x = ctypes.c_int(x)
    n = ctypes.c_int(n)
    return libspice.lstlei_c(x, n, array)


@spice_error_check
def lstltc(string: str, n: int, lenvals: int, array: Iterable[str]) -> int:
    """
    Given a character string and an ordered array of character
    strings, find the index of the largest array element less than
    the given string.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lstltc_c.html

    :param string: Upper bound value to search against.
    :param n: Number elements in array.
    :param lenvals: String length.
    :param array: Array of possible lower bounds
    :return:
            index of the last element of array that
            is lexically less than string.
    """
    string = stypes.string_to_char_p(string)
    array = stypes.list_to_char_array_ptr(array, x_len=lenvals, y_len=n)
    n = ctypes.c_int(n)
    lenvals = ctypes.c_int(lenvals)
    return libspice.lstltc_c(string, n, lenvals, array)


@spice_error_check
def lstltd(x: float, n: int, array: Union[ndarray, Iterable[float]]) -> int:
    """
    Given a number x and an array of non-decreasing floats
    find the index of the largest array element less than x.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lstltd_c.html

    :param x: Value to search against
    :param n: Number elements in array
    :param array: Array of possible lower bounds
    :return: index of the last element of array that is less than x.
    """
    array = stypes.to_double_vector(array)
    x = ctypes.c_double(x)
    n = ctypes.c_int(n)
    return libspice.lstltd_c(x, n, array)


@spice_error_check
def lstlti(x: int, n: int, array: Union[ndarray, Iterable[int]]) -> int:
    """
    Given a number x and an array of non-decreasing int,
    find the index of the largest array element less than x.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lstlti_c.html

    :param x: Value to search against
    :param n: Number elements in array
    :param array: Array of possible lower bounds
    :return: index of the last element of array that is less than x.
    """
    array = stypes.to_int_vector(array)
    x = ctypes.c_int(x)
    n = ctypes.c_int(n)
    return libspice.lstlti_c(x, n, array)


@spice_error_check
def ltime(etobs: float, obs: int, direct: str, targ: int) -> Tuple[float, float]:
    """
    This routine computes the transmit (or receive) time
    of a signal at a specified target, given the receive
    (or transmit) time at a specified observer. The elapsed
    time between transmit and receive is also returned.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ltime_c.html

    :param etobs: Epoch of a signal at some observer
    :param obs: NAIF ID of some observer
    :param direct: Direction the signal travels ( "->" or "<-" )
    :param targ: NAIF ID of the target object
    :return: epoch and time
    """
    etobs = ctypes.c_double(etobs)
    obs = ctypes.c_int(obs)
    direct = stypes.string_to_char_p(direct)
    targ = ctypes.c_int(targ)
    ettarg = ctypes.c_double()
    elapsd = ctypes.c_double()
    libspice.ltime_c(
        etobs, obs, direct, targ, ctypes.byref(ettarg), ctypes.byref(elapsd)
    )
    return ettarg.value, elapsd.value


@spice_error_check
def lx4dec(string: str, first: int) -> Tuple[int, int]:
    """
    Scan a string from a specified starting position for the
    end of a decimal number.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lx4dec_c.html

    :param string: Any character string.
    :param first: First character to scan from in string.
    :return: last and nchar
    """
    string = stypes.string_to_char_p(string)
    first = ctypes.c_int(first)
    last = ctypes.c_int()
    nchar = ctypes.c_int()
    libspice.lx4dec_c(string, first, ctypes.byref(last), ctypes.byref(nchar))
    return last.value, nchar.value


@spice_error_check
def lx4num(string: str, first: int) -> Tuple[int, int]:
    """
    Scan a string from a specified starting position for the
    end of a number.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lx4num_c.html

    :param string: Any character string.
    :param first: First character to scan from in string.
    :return: last and nchar
    """
    string = stypes.string_to_char_p(string)
    first = ctypes.c_int(first)
    last = ctypes.c_int()
    nchar = ctypes.c_int()
    libspice.lx4num_c(string, first, ctypes.byref(last), ctypes.byref(nchar))
    return last.value, nchar.value


@spice_error_check
def lx4sgn(string: str, first: int) -> Tuple[int, int]:
    """
    Scan a string from a specified starting position for the
    end of a signed integer.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lx4sgn_c.html

    :param string: Any character string.
    :param first: First character to scan from in string.
    :return: last and nchar
    """
    string = stypes.string_to_char_p(string)
    first = ctypes.c_int(first)
    last = ctypes.c_int()
    nchar = ctypes.c_int()
    libspice.lx4sgn_c(string, first, ctypes.byref(last), ctypes.byref(nchar))
    return last.value, nchar.value


@spice_error_check
def lx4uns(string: str, first: int) -> Tuple[int, int]:
    """
    Scan a string from a specified starting position for the
    end of an unsigned integer.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lx4uns_c.html

    :param string: Any character string.
    :param first: First character to scan from in string.
    :return: last and nchar
    """
    string = stypes.string_to_char_p(string)
    first = ctypes.c_int(first)
    last = ctypes.c_int()
    nchar = ctypes.c_int()
    libspice.lx4uns_c(string, first, ctypes.byref(last), ctypes.byref(nchar))
    return last.value, nchar.value


@spice_error_check
def lxqstr(string: str, qchar: str, first: int) -> Tuple[int, int]:
    """
    Lex (scan) a quoted string.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lxqstr_c.html

    :param string: String to be scanned.
    :param qchar: Quote delimiter character.
    :param first: Character position at which to start scanning.
    :return: last and nchar
    """
    string = stypes.string_to_char_p(string)
    qchar = ctypes.c_char(qchar.encode(encoding="UTF-8"))
    first = ctypes.c_int(first)
    last = ctypes.c_int()
    nchar = ctypes.c_int()
    libspice.lxqstr_c(string, qchar, first, ctypes.byref(last), ctypes.byref(nchar))
    return last.value, nchar.value


################################################################################
# M


@spice_error_check
def m2eul(
    r: Union[ndarray, Iterable[Iterable[float]]], axis3: int, axis2: int, axis1: int
) -> Tuple[float, float, float]:
    """
    Factor a rotation matrix as a product of three rotations
    about specified coordinate axes.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/m2eul_c.html

    :param r: A rotation matrix to be factored
    :param axis3: third rotation axes.
    :param axis2: second rotation axes.
    :param axis1: first rotation axes.
    :return: Third, second, and first Euler angles, in radians.
    """
    r = stypes.to_double_matrix(r)
    axis3 = ctypes.c_int(axis3)
    axis2 = ctypes.c_int(axis2)
    axis1 = ctypes.c_int(axis1)
    angle3 = ctypes.c_double()
    angle2 = ctypes.c_double()
    angle1 = ctypes.c_double()
    libspice.m2eul_c(
        r,
        axis3,
        axis2,
        axis1,
        ctypes.byref(angle3),
        ctypes.byref(angle2),
        ctypes.byref(angle1),
    )
    return angle3.value, angle2.value, angle1.value


@spice_error_check
def m2q(r: ndarray) -> ndarray:
    """
    Find a unit quaternion corresponding to a specified rotation matrix.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/m2q_c.html

    :param r: A rotation matrix to be factored
    :return: A unit quaternion representing the rotation matrix
    """
    r = stypes.to_double_matrix(r)
    q = stypes.empty_double_vector(4)
    libspice.m2q_c(r, q)
    return stypes.c_vector_to_python(q)


@spice_error_check
def matchi(string: str, templ: str, wstr: str, wchr: str) -> bool:
    """
    Determine whether a string is matched by a template containing wild cards.
    The pattern comparison is case-insensitive.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/matchi_c.html

    :param string: String to be tested.
    :param templ: Template (with wild cards) to test against string.
    :param wstr: Wild string token.
    :param wchr: Wild character token.
    :return: The function returns True if string matches templ, else False
    """
    string = stypes.string_to_char_p(string)
    templ = stypes.string_to_char_p(templ)
    wstr = ctypes.c_char(wstr.encode(encoding="UTF-8"))
    wchr = ctypes.c_char(wchr.encode(encoding="UTF-8"))
    return bool(libspice.matchi_c(string, templ, wstr, wchr))


@spice_error_check
def matchw(string: str, templ: str, wstr: str, wchr: str) -> bool:
    # ctypes.c_char(wstr.encode(encoding='UTF-8')
    """
    Determine whether a string is matched by a template containing wild cards.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/matchw_c.html

    :param string: String to be tested.
    :param templ: Template (with wild cards) to test against string.
    :param wstr: Wild string token.
    :param wchr: Wild character token.
    :return: The function returns True if string matches templ, else False
    """
    string = stypes.string_to_char_p(string)
    templ = stypes.string_to_char_p(templ)
    wstr = ctypes.c_char(wstr.encode(encoding="UTF-8"))
    wchr = ctypes.c_char(wchr.encode(encoding="UTF-8"))
    return bool(libspice.matchw_c(string, templ, wstr, wchr))


# skiping for now maxd_c,
# odd as arguments must be parsed and not really important


# skiping for now maxi_c,
# odd as arguments must be parsed and not really important


@spice_error_check
def mequ(m1: ndarray) -> ndarray:
    """
    Set one double precision 3x3 matrix equal to another.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mequ_c.html

    :param m1: input matrix.
    :return: Output matrix equal to m1.
    """
    m1 = stypes.to_double_matrix(m1)
    mout = stypes.empty_double_matrix()
    libspice.mequ_c(m1, mout)
    return stypes.c_matrix_to_numpy(mout)


@spice_error_check
def mequg(m1: ndarray, nr: int, nc: int) -> ndarray:
    """
    Set one double precision matrix of arbitrary size equal to another.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mequg_c.html

    :param m1: Input matrix.
    :param nr: Row dimension of m1.
    :param nc: Column dimension of m1.
    :return: Output matrix equal to m1
    """
    m1 = stypes.to_double_matrix(m1)
    mout = stypes.empty_double_matrix(x=nc, y=nr)
    nc = ctypes.c_int(nc)
    nr = ctypes.c_int(nr)
    libspice.mequg_c(m1, nc, nr, mout)
    return stypes.c_matrix_to_numpy(mout)


# skiping for now mind_c,
#  odd as arguments must be parsed and not really important


# skiping for now mini_c,
# odd as arguments must be parsed and not really important


@spice_error_check
def mtxm(m1: ndarray, m2: ndarray) -> ndarray:
    """
    Multiply the transpose of a 3x3 matrix and a 3x3 matrix.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mtxm_c.html

    :param m1: 3x3 double precision matrix.
    :param m2: 3x3 double precision matrix.
    :return: The produce m1 transpose times m2.
    """
    m1 = stypes.to_double_matrix(m1)
    m2 = stypes.to_double_matrix(m2)
    mout = stypes.empty_double_matrix()
    libspice.mtxm_c(m1, m2, mout)
    return stypes.c_matrix_to_numpy(mout)


@spice_error_check
def mtxmg(m1: ndarray, m2: ndarray) -> ndarray:
    """
    Multiply the transpose of a matrix with
    another matrix, both of arbitrary size.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mtxmg_c.html

    :param m1: N x M double precision matrix.
    :param m2: N x O double precision matrix.
    :param ncol1: Column dimension of m1 and row dimension of mout.
    :param nr1r2: Row dimension of m1 and m2.
    :param ncol2: Column dimension of m2.
    :return: Transpose of m1 times m2 (O x M).
    """
    ncol1, ncol2 = len(m1[0]), len(m2[0])
    nr1r2 = len(m1)
    m1 = stypes.to_double_matrix(m1)
    m2 = stypes.to_double_matrix(m2)
    mout = stypes.empty_double_matrix(x=ncol2, y=ncol1)
    ncol1 = ctypes.c_int(ncol1)
    nr1r2 = ctypes.c_int(nr1r2)
    ncol2 = ctypes.c_int(ncol2)
    libspice.mtxmg_c(m1, m2, ncol1, nr1r2, ncol2, mout)
    return stypes.c_matrix_to_numpy(mout)


@spice_error_check
def mtxv(m1: ndarray, vin: ndarray) -> ndarray:
    """
    Multiplies the transpose of a 3x3 matrix
    on the left with a vector on the right.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mtxv_c.html

    :param m1: 3x3 double precision matrix.
    :param vin: 3-dimensional double precision vector.
    :return: 3-dimensional double precision vector.
    """
    m1 = stypes.to_double_matrix(m1)
    vin = stypes.to_double_vector(vin)
    vout = stypes.empty_double_vector(3)
    libspice.mtxv_c(m1, vin, vout)
    return stypes.c_vector_to_python(vout)


@spice_error_check
def mtxvg(m1: ndarray, v2: ndarray) -> ndarray:
    """
    Multiply the transpose of a matrix and
    a vector of arbitrary size.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mtxvg_c.html

    :param m1: Left-hand matrix to be multiplied.
    :param v2: Right-hand vector to be multiplied.
    :return: Product vector m1 transpose * v2.
    """
    ncol1 = len(m1[0])
    nr1r2 = len(v2)
    m1 = stypes.to_double_matrix(m1)
    v2 = stypes.to_double_vector(v2)
    ncol1 = ctypes.c_int(ncol1)
    nr1r2 = ctypes.c_int(nr1r2)
    vout = stypes.empty_double_vector(ncol1.value)
    libspice.mtxvg_c(m1, v2, ncol1, nr1r2, vout)
    return stypes.c_vector_to_python(vout)


@spice_error_check
def mxm(
    m1: Union[ndarray, Iterable[Iterable[float]]],
    m2: Union[ndarray, Iterable[Iterable[float]]],
) -> ndarray:
    """
    Multiply two 3x3 matrices.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mxm_c.html

    :param m1: 3x3 double precision matrix.
    :param m2: 3x3 double precision matrix.
    :return: 3x3 double precision matrix.
    """
    m1 = stypes.to_double_matrix(m1)
    m2 = stypes.to_double_matrix(m2)
    mout = stypes.empty_double_matrix()
    libspice.mxm_c(m1, m2, mout)
    return stypes.c_matrix_to_numpy(mout)


@spice_error_check
def mxmg(
    m1: Union[ndarray, Iterable[Iterable[float]]],
    m2: Union[ndarray, Iterable[Iterable[float]]],
) -> ndarray:
    """
    Multiply two double precision matrices of arbitrary size.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mxmg_c.html

    :param m1: nrow1 X ncol1 double precision matrix.
    :param m2: ncol1 X ncol2 double precision matrix.
    :return: nrow1 X ncol2 double precision matrix.
    """
    nrow1, ncol1, ncol2 = len(m1), len(m1[0]), len(m2[0])
    m1 = stypes.to_double_matrix(m1)
    m2 = stypes.to_double_matrix(m2)
    mout = stypes.empty_double_matrix(x=ncol2, y=nrow1)
    nrow1 = ctypes.c_int(nrow1)
    ncol1 = ctypes.c_int(ncol1)
    ncol2 = ctypes.c_int(ncol2)
    libspice.mxmg_c(m1, m2, nrow1, ncol1, ncol2, mout)
    return stypes.c_matrix_to_numpy(mout)


@spice_error_check
def mxmt(
    m1: Union[ndarray, Iterable[Iterable[float]]],
    m2: Union[ndarray, Iterable[Iterable[float]]],
) -> ndarray:
    """
    Multiply a 3x3 matrix and the transpose of another 3x3 matrix.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mxmt_c.html

    :param m1: 3x3 double precision matrix.
    :param m2: 3x3 double precision matrix.
    :return: The product m1 times m2 transpose.
    """
    m1 = stypes.to_double_matrix(m1)
    m2 = stypes.to_double_matrix(m2)
    mout = stypes.empty_double_matrix()
    libspice.mxmt_c(m1, m2, mout)
    return stypes.c_matrix_to_numpy(mout)


@spice_error_check
def mxmtg(
    m1: Union[ndarray, Iterable[Iterable[float]]],
    m2: Union[ndarray, Iterable[Iterable[float]]],
) -> ndarray:
    """
    Multiply a matrix and the transpose of a matrix, both of arbitrary size.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mxmtg_c.html

    :param m1: Left-hand matrix to be multiplied.
    :param m2: Right-hand matrix whose transpose is to be multiplied
    :return: Product matrix.
    """
    nrow1, nc1c2, nrow2 = len(m1), len(m1[0]), len(m2)
    m1 = stypes.to_double_matrix(m1)
    m2 = stypes.to_double_matrix(m2)
    mout = stypes.empty_double_matrix(x=nrow2, y=nrow1)
    nrow1 = ctypes.c_int(nrow1)
    nc1c2 = ctypes.c_int(nc1c2)
    nrow2 = ctypes.c_int(nrow2)
    libspice.mxmtg_c(m1, m2, nrow1, nc1c2, nrow2, mout)
    return stypes.c_matrix_to_numpy(mout)


@spice_error_check
def mxv(m1: ndarray, vin: ndarray) -> ndarray:
    """
    Multiply a 3x3 double precision matrix with a
    3-dimensional double precision vector.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mxv_c.html

    :param m1: 3x3 double precision matrix.
    :param vin: 3-dimensional double precision vector.
    :return: 3-dimensional double precision vector.
    """
    m1 = stypes.to_double_matrix(m1)
    vin = stypes.to_double_vector(vin)
    vout = stypes.empty_double_vector(3)
    libspice.mxv_c(m1, vin, vout)
    return stypes.c_vector_to_python(vout)


@spice_error_check
def mxvg(
    m1: Union[ndarray, Iterable[Iterable[float]]],
    v2: Union[ndarray, Iterable[Iterable[float]]],
) -> ndarray:
    """
    Multiply a matrix and a vector of arbitrary size.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mxvg_c.html

    :param m1: Left-hand matrix to be multiplied.
    :param v2: Right-hand vector to be multiplied.
    :return: Product vector m1*v2
    """
    nrow1, nc1r2 = len(m1), len(m1[0])
    m1 = stypes.to_double_matrix(m1)
    v2 = stypes.to_double_vector(v2)
    nrow1 = ctypes.c_int(nrow1)
    nc1r2 = ctypes.c_int(nc1r2)
    vout = stypes.empty_double_vector(nrow1.value)
    libspice.mxvg_c(m1, v2, nrow1, nc1r2, vout)
    return stypes.c_vector_to_python(vout)


################################################################################
# N


@spice_error_check
def namfrm(frname: str) -> int:
    """
    Look up the frame ID code associated with a string.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/namfrm_c.html

    :param frname: The name of some reference frame.
    :return: The SPICE ID code of the frame.
    """
    frname = stypes.string_to_char_p(frname)
    frcode = ctypes.c_int()
    libspice.namfrm_c(frname, ctypes.byref(frcode))
    return frcode.value


@spice_error_check
def ncpos(string: str, chars: str, start: int) -> int:
    """
    Find the first occurrence in a string of a character NOT belonging
    to a collection of characters, starting at a specified
    location searching forward.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ncpos_c.html

    :param string: Any character string.
    :param chars: A collection of characters.
    :param start: Position to begin looking for one not in chars.
    :return: index
    """
    string = stypes.string_to_char_p(string)
    chars = stypes.string_to_char_p(chars)
    start = ctypes.c_int(start)
    return libspice.ncpos_c(string, chars, start)


@spice_error_check
def ncposr(string: str, chars: str, start: int) -> int:
    """
    Find the first occurrence in a string of a character NOT belonging to a
    collection of characters, starting at a specified location,
    searching in reverse.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ncposr_c.html

    :param string: Any character string.
    :param chars: A collection of characters.
    :param start: Position to begin looking for one of chars.
    :return: index
    """
    string = stypes.string_to_char_p(string)
    chars = stypes.string_to_char_p(chars)
    start = ctypes.c_int(start)
    return libspice.ncposr_c(string, chars, start)


@spice_error_check
def nearpt(
    positn: Union[ndarray, Iterable[float]], a: float, b: float, c: float
) -> Tuple[ndarray, float]:
    """
    locates the point on the surface of an ellipsoid that is nearest to a
    specified position. It also returns the altitude of the
    position above the ellipsoid.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/nearpt_c.html

    :param positn: Position of a point in bodyfixed frame.
    :param a: Length of semi-axis parallel to x-axis.
    :param b: Length of semi-axis parallel to y-axis.
    :param c: Length on semi-axis parallel to z-axis.
    :return:
            Point on the ellipsoid closest to positn,
            Altitude of positn above the ellipsoid.
    """
    positn = stypes.to_double_vector(positn)
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    npoint = stypes.empty_double_vector(3)
    alt = ctypes.c_double()
    libspice.nearpt_c(positn, a, b, c, npoint, ctypes.byref(alt))
    return stypes.c_vector_to_python(npoint), alt.value


@spice_error_check
def npedln(
    a: float,
    b: float,
    c: float,
    linept: Union[ndarray, Iterable[float]],
    linedr: Union[ndarray, Iterable[float]],
) -> Tuple[ndarray, float]:
    """
    Find nearest point on a triaxial ellipsoid to a specified
    line and the distance from the ellipsoid to the line.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/npedln_c.html

    :param a: Length of ellipsoid's semi-axis in the x direction
    :param b: Length of ellipsoid's semi-axis in the y direction
    :param c: Length of ellipsoid's semi-axis in the z direction
    :param linept: Length of ellipsoid's semi-axis in the z direction
    :param linedr: Direction vector of line
    :return: Nearest point on ellipsoid to line, Distance of ellipsoid from line
    """
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    linept = stypes.to_double_vector(linept)
    linedr = stypes.to_double_vector(linedr)
    pnear = stypes.empty_double_vector(3)
    dist = ctypes.c_double()
    libspice.npedln_c(a, b, c, linept, linedr, pnear, ctypes.byref(dist))
    return stypes.c_vector_to_python(pnear), dist.value


@spice_error_check
def npelpt(
    point: Union[ndarray, Iterable[float]], ellips: Ellipse
) -> Tuple[ndarray, float]:
    """
    Find the nearest point on an ellipse to a specified point, both
    in three-dimensional space, and find the distance between the
    ellipse and the point.
    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/npelpt_c.html

    :param point: Point whose distance to an ellipse is to be found.
    :param ellips: An ellipse.
    :return: Nearest point on ellipsoid to line, Distance of ellipsoid from line
    """
    assert isinstance(ellips, stypes.Ellipse)
    point = stypes.to_double_vector(point)
    pnear = stypes.empty_double_vector(3)
    dist = ctypes.c_double()
    libspice.npelpt_c(point, ctypes.byref(ellips), pnear, ctypes.byref(dist))
    return stypes.c_vector_to_python(pnear), dist.value


@spice_error_check
def nplnpt(
    linpt: Union[ndarray, Iterable[float]],
    lindir: Union[ndarray, Iterable[float]],
    point: Union[ndarray, Iterable[float]],
) -> Tuple[ndarray, float]:
    """
    Find the nearest point on a line to a specified point,
    and find the distance between the two points.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/nplnpt_c.html

    :param linpt: Point on a line
    :param lindir: line's direction vector
    :param point: A second point.
    :return:
            Nearest point on the line to point,
            Distance between point and pnear
    """
    linpt = stypes.to_double_vector(linpt)
    lindir = stypes.to_double_vector(lindir)
    point = stypes.to_double_vector(point)
    pnear = stypes.empty_double_vector(3)
    dist = ctypes.c_double()
    libspice.nplnpt_c(linpt, lindir, point, pnear, ctypes.byref(dist))
    return stypes.c_vector_to_python(pnear), dist.value


@spice_error_check
def nvc2pl(normal: Union[Iterable[float], Iterable[float]], constant: float) -> Plane:
    """
    Make a plane from a normal vector and a constant.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/nvc2pl_c.html

    :param normal: A normal vector defining a plane.
    :param constant: A constant defining a plane.
    :return: plane
    """
    plane = stypes.Plane()
    normal = stypes.to_double_vector(normal)
    constant = ctypes.c_double(constant)
    libspice.nvc2pl_c(normal, constant, ctypes.byref(plane))
    return plane


@spice_error_check
def nvp2pl(
    normal: Union[ndarray, Iterable[float]], point: Union[ndarray, Iterable[float]]
) -> Plane:
    """
    Make a plane from a normal vector and a point.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/nvp2pl_c.html

    :param normal: A normal vector defining a plane.
    :param point: A point defining a plane.
    :return: plane
    """
    normal = stypes.to_double_vector(normal)
    point = stypes.to_double_vector(point)
    plane = stypes.Plane()
    libspice.nvp2pl_c(normal, point, ctypes.byref(plane))
    return plane


################################################################################
# O


@spice_error_check
def occult(
    target1: str,
    shape1: str,
    frame1: str,
    target2: str,
    shape2: str,
    frame2: str,
    abcorr: str,
    observer: str,
    et: float,
) -> int:
    """
    Determines the occultation condition (not occulted, partially,
    etc.) of one target relative to another target as seen by
    an observer at a given time.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/occult_c.html

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
    target1 = stypes.string_to_char_p(target1)
    shape1 = stypes.string_to_char_p(shape1)
    frame1 = stypes.string_to_char_p(frame1)
    target2 = stypes.string_to_char_p(target2)
    shape2 = stypes.string_to_char_p(shape2)
    frame2 = stypes.string_to_char_p(frame2)
    abcorr = stypes.string_to_char_p(abcorr)
    observer = stypes.string_to_char_p(observer)
    et = ctypes.c_double(et)
    occult_code = ctypes.c_int()
    libspice.occult_c(
        target1,
        shape1,
        frame1,
        target2,
        shape2,
        frame2,
        abcorr,
        observer,
        et,
        ctypes.byref(occult_code),
    )
    return occult_code.value


@spice_error_check
def ordc(item: str, inset: SpiceCell) -> int:
    """
    The function returns the ordinal position of any given item in a
    character set.  If the item does not appear in the set, the function
    returns -1.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ordc_c.html

    :param item: An item to locate within a set.
    :param inset: A set to search for a given item.
    :return: the ordinal position of item within the set
    """
    assert isinstance(inset, stypes.SpiceCell)
    assert inset.is_char()
    assert isinstance(item, str)
    item = stypes.string_to_char_p(item)
    return libspice.ordc_c(item, ctypes.byref(inset))


@spice_error_check
def ordd(item: float, inset: SpiceCell) -> int:
    """
    The function returns the ordinal position of any given item in a
    double precision set.  If the item does not appear in the set, the
    function returns -1.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ordd_c.html

    :param item: An item to locate within a set.
    :param inset: A set to search for a given item.
    :return: the ordinal position of item within the set
    """
    assert isinstance(inset, stypes.SpiceCell)
    assert inset.is_double()
    item = ctypes.c_double(item)
    return libspice.ordd_c(item, ctypes.byref(inset))


@spice_error_check
def ordi(item: int, inset: SpiceCell) -> int:
    """
    The function returns the ordinal position of any given item in an
    integer set.  If the item does not appear in the set, the function
    returns -1.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ordi_c.html

    :param item: An item to locate within a set.
    :param inset: A set to search for a given item.
    :return: the ordinal position of item within the set
    """
    assert isinstance(inset, stypes.SpiceCell)
    assert inset.is_int()
    assert isinstance(item, int)
    item = ctypes.c_int(item)
    return libspice.ordi_c(item, ctypes.byref(inset))


@spice_error_check
def orderc(array: Sequence[str], ndim: Optional[int] = None) -> ndarray:
    """
    Determine the order of elements in an array of character strings.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/orderc_c.html

    :param array: Input array.
    :param ndim: Optional Length of input array
    :return: Order vector for array.
    """
    if ndim is None:
        ndim = ctypes.c_int(len(array))
    else:
        ndim = ctypes.c_int(ndim)
    lenvals = ctypes.c_int(len(max(array, key=len)) + 1)
    iorder = stypes.empty_int_vector(ndim)
    array = stypes.list_to_char_array(array, lenvals, ndim)
    libspice.orderc_c(lenvals, array, ndim, iorder)
    return stypes.c_vector_to_python(iorder)


@spice_error_check
def orderd(array: Sequence[float], ndim: Optional[int] = None) -> ndarray:
    """
    Determine the order of elements in a double precision array.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/orderd_c.html

    :param array: Input array.
    :param ndim: Optional Length of input array
    :return: Order vector for array.
    """
    if ndim is None:
        ndim = ctypes.c_int(len(array))
    else:
        ndim = ctypes.c_int(ndim)
    array = stypes.to_double_vector(array)
    iorder = stypes.empty_int_vector(ndim)
    libspice.orderd_c(array, ndim, iorder)
    return stypes.c_vector_to_python(iorder)


@spice_error_check
def orderi(array: Sequence[int], ndim: Optional[int] = None) -> ndarray:
    """
    Determine the order of elements in an integer array.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/orderi_c.html

    :param array: Input array.
    :param ndim: Optional Length of input array
    :return: Order vector for array.
    """
    if ndim is None:
        ndim = ctypes.c_int(len(array))
    else:
        ndim = ctypes.c_int(ndim)
    array = stypes.to_int_vector(array)
    iorder = stypes.empty_int_vector(ndim)
    libspice.orderi_c(array, ndim, iorder)
    return stypes.c_vector_to_python(iorder)


@spice_error_check
def oscelt(state: ndarray, et: float, mu: Union[float, int]) -> ndarray:
    """
    Determine the set of osculating conic orbital elements that
    corresponds to the state (position, velocity) of a body at
    some epoch.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/oscelt_c.html

    :param state: State of body at epoch of elements.
    :param et: Epoch of elements.
    :param mu: Gravitational parameter (GM) of primary body.
    :return: Equivalent conic elements
    """
    state = stypes.to_double_vector(state)
    et = ctypes.c_double(et)
    mu = ctypes.c_double(mu)
    elts = stypes.empty_double_vector(8)
    libspice.oscelt_c(state, et, mu, elts)
    return stypes.c_vector_to_python(elts)


def oscltx(state: ndarray, et: float, mu: int) -> ndarray:
    """
    Determine the set of osculating conic orbital elements that
    corresponds to the state (position, velocity) of a body at some
    epoch. In additional to the classical elements, return the true
    anomaly, semi-major axis, and period, if applicable.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/oscltx_c.html

    :param state: State of body at epoch of elements.
    :param et: Epoch of elements.
    :param mu: Gravitational parameter (GM) of primary body.
    :return: Extended set of classical conic elements.
    """
    state = stypes.to_double_vector(state)
    et = ctypes.c_double(et)
    mu = ctypes.c_double(mu)
    elts = stypes.empty_double_vector(20)
    libspice.oscltx_c(state, et, mu, elts)
    return stypes.c_vector_to_python(elts)[0:11]


################################################################################
# P
@spice_error_check
def pckcls(handle: int) -> None:
    """
    Close an open PCK file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pckcls_c.html

    :param handle: Handle of the PCK file to be closed.
    """
    handle = ctypes.c_int(handle)
    libspice.pckcls_c(handle)


@spice_error_check
def pckcov(pck: str, idcode: int, cover: SpiceCell) -> None:
    """
    Find the coverage window for a specified reference frame in a
    specified binary PCK file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pckcov_c.html

    :param pck: Name of PCK file.
    :param idcode: Class ID code of PCK reference frame.
    :param cover: Window giving coverage in pck for idcode.
    """
    pck = stypes.string_to_char_p(pck)
    idcode = ctypes.c_int(idcode)
    assert isinstance(cover, stypes.SpiceCell)
    assert cover.dtype == 1
    libspice.pckcov_c(pck, idcode, ctypes.byref(cover))


@spice_error_check
def pckfrm(pck: str, ids: SpiceCell) -> None:
    """
    Find the set of reference frame class ID codes of all frames
    in a specified binary PCK file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pckfrm_c.html

    :param pck: Name of PCK file.
    :param ids: Set of frame class ID codes of frames in PCK file.
    """
    pck = stypes.string_to_char_p(pck)
    assert isinstance(ids, stypes.SpiceCell)
    assert ids.dtype == 2
    libspice.pckfrm_c(pck, ctypes.byref(ids))


@spice_error_check
def pcklof(filename: str) -> int:
    """
    Load a binary PCK file for use by the readers.  Return the
    handle of the loaded file which is used by other PCK routines to
    refer to the file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pcklof_c.html

    :param filename: Name of the file to be loaded.
    :return: Loaded file's handle.
    """
    filename = stypes.string_to_char_p(filename)
    handle = ctypes.c_int()
    libspice.pcklof_c(filename, ctypes.byref(handle))
    return handle.value


@spice_error_check
def pckopn(name: str, ifname: str, ncomch: int) -> int:
    """
    Create a new PCK file, returning the handle of the opened file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pckopn_c.html

    :param name: The name of the PCK file to be opened.
    :param ifname: The internal filename for the PCK.
    :param ncomch: The number of characters to reserve for comments.
    :return: The handle of the opened PCK file.
    """
    name = stypes.string_to_char_p(name)
    ifname = stypes.string_to_char_p(ifname)
    ncomch = ctypes.c_int(ncomch)
    handle = ctypes.c_int()
    libspice.pckopn_c(name, ifname, ncomch, ctypes.byref(handle))
    return handle.value


@spice_error_check
def pckuof(handle: int) -> None:
    """
    Unload a binary PCK file so that it will no longer be searched by
    the readers.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pckuof_c.html

    :param handle: Handle of PCK file to be unloaded
    """
    handle = ctypes.c_int(handle)
    libspice.pckuof_c(handle)


@spice_error_check
def pckw02(
    handle: int,
    classid: int,
    frname: str,
    first: float,
    last: float,
    segid: str,
    intlen: float,
    n: int,
    polydg: int,
    cdata: Union[ndarray, Iterable[float]],
    btime: float,
) -> None:
    """
    Write a type 2 segment to a PCK binary file given the file handle,
    frame class ID, base frame, time range covered by the segment, and
    the Chebyshev polynomial coefficients.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pckw02_c.html

    :param handle: Handle of binary PCK file open for writing.
    :param classid: Frame class ID of body-fixed frame.
    :param frname: Name of base reference frame.
    :param first: Start time of interval covered by segment.
    :param last: End time of interval covered by segment.
    :param segid: Segment identifier.
    :param intlen: Length of time covered by logical record.
    :param n: Number of logical records in segment.
    :param polydg: Chebyshev polynomial degree.
    :param cdata: Array of Chebyshev coefficients.
    :param btime: Begin time of first logical record.
    """
    handle = ctypes.c_int(handle)
    classid = ctypes.c_int(classid)
    frname = stypes.string_to_char_p(frname)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    segid = stypes.string_to_char_p(segid)
    intlen = ctypes.c_double(intlen)
    n = ctypes.c_int(n)
    polydg = ctypes.c_int(polydg)
    cdata = stypes.to_double_vector(cdata)
    btime = ctypes.c_double(btime)
    libspice.pckw02_c(
        handle, classid, frname, first, last, segid, intlen, n, polydg, cdata, btime
    )


@spice_error_check
def pcpool(name: str, cvals: Sequence[str]) -> None:
    """
    This entry point provides toolkit programmers a method for
    programmatically inserting character data into the
    kernel pool.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pcpool_c.html

    :param name: The kernel pool name to associate with cvals.
    :param cvals: An array of strings to insert into the kernel pool.
    """
    name = stypes.string_to_char_p(name)
    lenvals = ctypes.c_int(len(max(cvals, key=len)) + 1)
    n = ctypes.c_int(len(cvals))
    cvals = stypes.list_to_char_array(cvals, lenvals, n)
    libspice.pcpool_c(name, n, lenvals, cvals)


@spice_error_check
def pdpool(name: str, dvals: Union[ndarray, Iterable[float]]) -> None:
    """
    This entry point provides toolkit programmers a method for
    programmatically inserting double precision data into the
    kernel pool.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pdpool_c.html

    :param name: The kernel pool name to associate with dvals.
    :param dvals: An array of values to insert into the kernel pool.
    """
    name = stypes.string_to_char_p(name)
    n = ctypes.c_int(len(dvals))
    dvals = stypes.to_double_vector(dvals)
    libspice.pdpool_c(name, n, dvals)


@spice_error_check
def pgrrec(body: str, lon: float, lat: float, alt: int, re: float, f: float) -> ndarray:
    """
    Convert planetographic coordinates to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pgrrec_c.html

    :param body: Body with which coordinate system is associated.
    :param lon: Planetographic longitude of a point (radians).
    :param lat: Planetographic latitude of a point (radians).
    :param alt: Altitude of a point above reference spheroid.
    :param re: Equatorial radius of the reference spheroid.
    :param f: Flattening coefficient.
    :return: Rectangular coordinates of the point.
    """
    body = stypes.string_to_char_p(body)
    lon = ctypes.c_double(lon)
    lat = ctypes.c_double(lat)
    alt = ctypes.c_double(alt)
    re = ctypes.c_double(re)
    f = ctypes.c_double(f)
    rectan = stypes.empty_double_vector(3)
    libspice.pgrrec_c(body, lon, lat, alt, re, f, rectan)
    return stypes.c_vector_to_python(rectan)


@spice_error_check
def phaseq(et: float, target: str, illmn: str, obsrvr: str, abcorr: str) -> float:
    """
    Compute the apparent phase angle for a target, observer,
    illuminator set of ephemeris objects.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/phaseq_c.html

    :param et: Ephemeris seconds past J2000 TDB.
    :param target: Target body name.
    :param illmn: Illuminating body name.
    :param obsrvr: Observer body.
    :param abcorr: Aberration correction flag.
    :return: Value of phase angle.
    """
    et = ctypes.c_double(et)
    target = stypes.string_to_char_p(target)
    illmn = stypes.string_to_char_p(illmn)
    obsrvr = stypes.string_to_char_p(obsrvr)
    abcorr = stypes.string_to_char_p(abcorr)
    return libspice.phaseq_c(et, target, illmn, obsrvr, abcorr)


@spice_error_check
def pi() -> float:
    """
    Return the value of pi (the ratio of the circumference of
    a circle to its diameter).

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pi_c.html

    :return: value of pi.
    """
    return libspice.pi_c()


@spice_error_check
def pipool(name: str, ivals: ndarray) -> None:
    """
    This entry point provides toolkit programmers a method for
    programmatically inserting integer data into the kernel pool.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pipool_c.html

    :param name: The kernel pool name to associate with values.
    :param ivals: An array of integers to insert into the pool.
    """
    name = stypes.string_to_char_p(name)
    n = ctypes.c_int(len(ivals))
    ivals = stypes.to_int_vector(ivals)
    libspice.pipool_c(name, n, ivals)


@spice_error_check
def pjelpl(elin: Ellipse, plane: Plane) -> Ellipse:
    """
    Project an ellipse onto a plane, orthogonally.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pjelpl_c.html

    :param elin: A SPICE ellipse to be projected.
    :param plane: A plane onto which elin is to be projected.
    :return: A SPICE ellipse resulting from the projection.
    """
    assert isinstance(elin, stypes.Ellipse)
    assert isinstance(plane, stypes.Plane)
    elout = stypes.Ellipse()
    libspice.pjelpl_c(ctypes.byref(elin), ctypes.byref(plane), ctypes.byref(elout))
    return elout


@spice_error_check
def pl2nvc(plane: Plane) -> Tuple[ndarray, float]:
    """
    Return a unit normal vector and constant that define a specified plane.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pl2nvc_c.html

    :param plane: A SPICE plane.
    :return:
            A normal vector and constant defining
            the geometric plane represented by plane.
    """
    assert isinstance(plane, stypes.Plane)
    normal = stypes.empty_double_vector(3)
    constant = ctypes.c_double()
    libspice.pl2nvc_c(ctypes.byref(plane), normal, ctypes.byref(constant))
    return stypes.c_vector_to_python(normal), constant.value


@spice_error_check
def pl2nvp(plane: Plane) -> Tuple[ndarray, ndarray]:
    """
    Return a unit normal vector and point that define a specified plane.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pl2nvp_c.html


    :param plane: A SPICE plane.
    :return: A unit normal vector and point that define plane.
    """
    assert isinstance(plane, stypes.Plane)
    normal = stypes.empty_double_vector(3)
    point = stypes.empty_double_vector(3)
    libspice.pl2nvp_c(ctypes.byref(plane), normal, point)
    return stypes.c_vector_to_python(normal), stypes.c_vector_to_python(point)


@spice_error_check
def pl2psv(plane: Plane) -> Tuple[ndarray, ndarray, ndarray]:
    """
    Return a point and two orthogonal spanning vectors that generate
    a specified plane.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pl2psv_c.html

    :param plane: A SPICE plane.
    :return:
            A point in the input plane and two vectors
            spanning the input plane.
    """
    assert isinstance(plane, stypes.Plane)
    point = stypes.empty_double_vector(3)
    span1 = stypes.empty_double_vector(3)
    span2 = stypes.empty_double_vector(3)
    libspice.pl2psv_c(ctypes.byref(plane), point, span1, span2)
    return (
        stypes.c_vector_to_python(point),
        stypes.c_vector_to_python(span1),
        stypes.c_vector_to_python(span2),
    )


@spice_error_check
def pltar(vrtces: Sequence[Iterable[float]], plates: Sequence[Iterable[int]]) -> float:
    """
    Compute the total area of a collection of triangular plates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pltar_c.html

    :param vrtces: Array of vertices.
    :param plates: Array of plates.
    :return: total area of the set of plates
    """
    nv = ctypes.c_int(len(vrtces))
    vrtces = stypes.to_double_matrix(vrtces)
    np = ctypes.c_int(len(plates))
    plates = stypes.to_int_matrix(plates)
    return libspice.pltar_c(nv, vrtces, np, plates)


@spice_error_check
def pltexp(
    iverts: Iterable[Union[Iterable[Union[float, float]], Iterable[float]]],
    delta: float,
) -> ndarray:
    """
    Expand a triangular plate by a specified amount. The expanded
    plate is co-planar with, and has the same orientation as, the
    original. The centroids of the two plates coincide.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pltexp_c.html

    :param iverts: Vertices of the plate to be expanded.
    :param delta: Fraction by which the plate is to be expanded.
    :return: Vertices of the expanded plate.
    """
    iverts = stypes.to_double_matrix(iverts)
    delta = ctypes.c_double(delta)
    overts = stypes.empty_double_matrix()
    libspice.pltexp_c(iverts, delta, overts)
    return stypes.c_matrix_to_numpy(overts)


@spice_error_check
def pltnp(
    point: Union[ndarray, Iterable[float]],
    v1: Union[ndarray, Iterable[float]],
    v2: Union[ndarray, Iterable[float]],
    v3: Union[ndarray, Iterable[float]],
) -> Tuple[ndarray, float]:
    """
    Find the nearest point on a triangular plate to a given point.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pltnp_c.html

    :param point: A point in 3-dimensional space.
    :param v1: Vertices of a triangular plate.
    :param v2: Vertices of a triangular plate.
    :param v3: Vertices of a triangular plate.
    :return: the nearest point on a triangular plate to a given point and distance
    """
    point = stypes.to_double_vector(point)
    v1 = stypes.to_double_vector(v1)
    v2 = stypes.to_double_vector(v2)
    v3 = stypes.to_double_vector(v3)
    pnear = stypes.empty_double_vector(3)
    dist = ctypes.c_double()
    libspice.pltnp_c(point, v1, v2, v3, pnear, ctypes.byref(dist))
    return stypes.c_vector_to_python(pnear), dist.value


@spice_error_check
def pltnrm(
    v1: Iterable[Union[float, float]],
    v2: Union[ndarray, Iterable[float]],
    v3: Iterable[Union[float, float]],
) -> ndarray:
    """
    Compute an outward normal vector of a triangular plate.
    The vector does not necessarily have unit length.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pltnrm_c.html

    :param v1: Vertices of a plate.
    :param v2: Vertices of a plate.
    :param v3: Vertices of a plate.
    :return: Plate's outward normal vector.
    """
    v1 = stypes.to_double_vector(v1)
    v2 = stypes.to_double_vector(v2)
    v3 = stypes.to_double_vector(v3)
    normal = stypes.empty_double_vector(3)
    libspice.pltnrm_c(v1, v2, v3, normal)
    return stypes.c_vector_to_python(normal)


@spice_error_check
def pltvol(vrtces: Sequence[Iterable[float]], plates: Sequence[Iterable[int]]) -> float:
    """
    Compute the volume of a three-dimensional region bounded by a
    collection of triangular plates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pltvol_c.html

    :param vrtces: Array of vertices.
    :param plates: Array of plates.
    :return: the volume of the spatial region bounded by the plates.
    """
    nv = ctypes.c_int(len(vrtces))
    vrtces = stypes.to_double_matrix(vrtces)
    np = ctypes.c_int(len(plates))
    plates = stypes.to_int_matrix(plates)
    return libspice.pltvol_c(nv, vrtces, np, plates)


@spice_error_check
def polyds(
    coeffs: Union[ndarray, Iterable[float]], deg: int, nderiv: int, t: int
) -> ndarray:
    """
    Compute the value of a polynomial and it's first
    n derivatives at the value t.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/polyds_c.html

    :param coeffs: Coefficients of the polynomial to be evaluated.
    :param deg: Degree of the polynomial to be evaluated.
    :param nderiv: Number of derivatives to compute.
    :param t: Point to evaluate the polynomial and derivatives
    :return: Value of polynomial and derivatives.
    """
    coeffs = stypes.to_double_vector(coeffs)
    deg = ctypes.c_int(deg)
    p = stypes.empty_double_vector(nderiv + 1)
    nderiv = ctypes.c_int(nderiv)
    t = ctypes.c_double(t)
    libspice.polyds_c(ctypes.byref(coeffs), deg, nderiv, t, p)
    return stypes.c_vector_to_python(p)


@spice_error_check
def pos(string: str, substr: str, start: int) -> int:
    """
    Find the first occurrence in a string of a substring, starting at
    a specified location, searching forward.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pos_c.html

    :param string: Any character string.
    :param substr: Substring to locate in the character string.
    :param start: Position to begin looking for substr in string.
    :return:
            The index of the first occurrence of substr
            in string at or following index start.
    """
    string = stypes.string_to_char_p(string)
    substr = stypes.string_to_char_p(substr)
    start = ctypes.c_int(start)
    return libspice.pos_c(string, substr, start)


@spice_error_check
def posr(string: str, substr: str, start: int) -> int:
    """
    Find the first occurrence in a string of a substring, starting at
    a specified location, searching backward.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/posr_c.html

    :param string: Any character string.
    :param substr: Substring to locate in the character string.
    :param start: Position to begin looking for substr in string.
    :return:
            The index of the last occurrence of substr
            in string at or preceding index start.
    """
    string = stypes.string_to_char_p(string)
    substr = stypes.string_to_char_p(substr)
    start = ctypes.c_int(start)
    return libspice.posr_c(string, substr, start)


# prompt,
# skip for no as this is not really an important function for python users


@spice_error_check
def prop2b(gm: float, pvinit: ndarray, dt: float) -> ndarray:
    """
    Given a central mass and the state of massless body at time t_0,
    this routine determines the state as predicted by a two-body
    force model at time t_0 + dt.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/prop2b_c.html

    :param gm: Gravity of the central mass.
    :param pvinit: Initial state from which to propagate a state.
    :param dt: Time offset from initial state to propagate to.
    :return: The propagated state.
    """
    gm = ctypes.c_double(gm)
    pvinit = stypes.to_double_vector(pvinit)
    dt = ctypes.c_double(dt)
    pvprop = stypes.empty_double_vector(6)
    libspice.prop2b_c(gm, pvinit, dt, pvprop)
    return stypes.c_vector_to_python(pvprop)


@spice_error_check
def prsdp(string: str) -> float:
    """
    Parse a string as a double precision number, encapsulating error handling.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/prsdp_c.html

    :param string: String representing a d.p. number.
    :return: D.p. value obtained by parsing string.
    """
    string = stypes.string_to_char_p(string)
    dpval = ctypes.c_double()
    libspice.prsdp_c(string, ctypes.byref(dpval))
    return dpval.value


@spice_error_check
def prsint(string: str) -> int:
    """
    Parse a string as an integer, encapsulating error handling.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/prsint_c.html

    :param string: String representing an integer.
    :return: Integer value obtained by parsing string.
    """
    string = stypes.string_to_char_p(string)
    intval = ctypes.c_int()
    libspice.prsint_c(string, ctypes.byref(intval))
    return intval.value


@spice_error_check
def psv2pl(point: ndarray, span1: ndarray, span2: ndarray) -> Plane:
    """
    Make a CSPICE plane from a point and two spanning vectors.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/psv2pl_c.html

    :param point: A Point.
    :param span1: First Spanning vector.
    :param span2: Second Spanning vector.
    :return: A SPICE plane.
    """
    point = stypes.to_double_vector(point)
    span1 = stypes.to_double_vector(span1)
    span2 = stypes.to_double_vector(span2)
    plane = stypes.Plane()
    libspice.psv2pl_c(point, span1, span2, ctypes.byref(plane))
    return plane


# skip putcml, is this really needed for python users?


@spice_error_check
def pxform(fromstr: str, tostr: str, et: float) -> ndarray:
    """
    Return the matrix that transforms position vectors from one
    specified frame to another at a specified epoch.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pxform_c.html

    :param fromstr: Name of the frame to transform from.
    :param tostr: Name of the frame to transform to.
    :param et: Epoch of the rotation matrix.
    :return: A rotation matrix.
    """
    et = ctypes.c_double(et)
    tostr = stypes.string_to_char_p(tostr)
    fromstr = stypes.string_to_char_p(fromstr)
    rotatematrix = stypes.empty_double_matrix()
    libspice.pxform_c(fromstr, tostr, et, rotatematrix)
    return stypes.c_matrix_to_numpy(rotatematrix)


@spice_error_check
def pxfrm2(frame_from: str, frame_to: str, etfrom: float, etto: float) -> ndarray:
    """
    Return the 3x3 matrix that transforms position vectors from one
    specified frame at a specified epoch to another specified
    frame at another specified epoch.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pxfrm2_c.html

    :param frame_from: Name of the frame to transform from.
    :param frame_to: Name of the frame to transform to.
    :param etfrom: Evaluation time of frame_from.
    :param etto: Evaluation time of frame_to.
    :return: A position transformation matrix from frame_from to frame_to
    """
    frame_from = stypes.string_to_char_p(frame_from)
    frame_to = stypes.string_to_char_p(frame_to)
    etfrom = ctypes.c_double(etfrom)
    etto = ctypes.c_double(etto)
    outmatrix = stypes.empty_double_matrix()
    libspice.pxfrm2_c(frame_from, frame_to, etfrom, etto, outmatrix)
    return stypes.c_matrix_to_numpy(outmatrix)


################################################################################
# Q


@spice_error_check
def q2m(q: ndarray) -> ndarray:
    """
    Find the rotation matrix corresponding to a specified unit quaternion.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/q2m_c.html

    :param q: A unit quaternion.
    :return: A rotation matrix corresponding to q
    """
    q = stypes.to_double_vector(q)
    mout = stypes.empty_double_matrix()
    libspice.q2m_c(q, mout)
    return stypes.c_matrix_to_numpy(mout)


# @spice_error_check
def qcktrc(tracelen: int = _default_len_out) -> str:
    """
    Return a string containing a traceback.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/qcktrc_c.html

    :param tracelen: Maximum length of output traceback string.
    :return: A traceback string.
    """
    tracestr = stypes.string_to_char_p(tracelen)
    tracelen = ctypes.c_int(tracelen)
    libspice.qcktrc_c(tracelen, tracestr)
    return stypes.to_python_string(tracestr)


@spice_error_check
def qderiv(f0: ndarray, f2: ndarray, delta: float) -> ndarray:
    """
    Estimate the derivative of a function by finding the derivative
    of a quadratic approximating function. This derivative estimate
    is equivalent to that found by computing the average of forward
    and backward differences.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/qderiv_c.html

    :param f0: Function values at left endpoint.
    :param f2: Function values at right endpoint.
    :param delta: Separation of abscissa points.
    :return: Derivative vector.
    """
    _ndim = ctypes.c_int(len(f0))
    _f0 = stypes.to_double_vector(f0)
    _f2 = stypes.to_double_vector(f2)
    _delta = ctypes.c_double(delta)
    _dfdt = stypes.empty_double_vector(_ndim)
    libspice.qderiv_c(_ndim, _f0, _f2, _delta, _dfdt)
    return stypes.c_vector_to_python(_dfdt)


@spice_error_check
def qdq2av(q: ndarray, dq: Union[ndarray, Iterable[float]]) -> ndarray:
    """
    Derive angular velocity from a unit quaternion and its derivative
    with respect to time.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/qdq2av_c.html

    :param q: Unit SPICE quaternion.
    :param dq: Derivative of q with respect to time
    :return: Angular velocity defined by q and dq.
    """
    q = stypes.to_double_vector(q)
    dq = stypes.to_double_vector(dq)
    vout = stypes.empty_double_vector(3)
    libspice.qdq2av_c(q, dq, vout)
    return stypes.c_vector_to_python(vout)


@spice_error_check
def qxq(
    q1: Union[ndarray, Iterable[float]], q2: Union[ndarray, Iterable[float]]
) -> ndarray:
    """
    Multiply two quaternions.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/qxq_c.html

    :param q1: First SPICE quaternion.
    :param q2: Second SPICE quaternion.
    :return: Product of q1 and q2.
    """
    q1 = stypes.to_double_vector(q1)
    q2 = stypes.to_double_vector(q2)
    vout = stypes.empty_double_vector(4)
    libspice.qxq_c(q1, q2, vout)
    return stypes.c_vector_to_python(vout)


################################################################################
# R


@spice_error_check
def radrec(inrange: float, re: float, dec: float) -> ndarray:
    """
    Convert from range, right ascension, and declination to rectangular
    coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/radrec_c.html

    :param inrange: Distance of a point from the origin.
    :param re: Right ascension of point in radians.
    :param dec: Declination of point in radians.
    :return: Rectangular coordinates of the point.
    """
    inrange = ctypes.c_double(inrange)
    re = ctypes.c_double(re)
    dec = ctypes.c_double(dec)
    rectan = stypes.empty_double_vector(3)
    libspice.radrec_c(inrange, re, dec, rectan)
    return stypes.c_vector_to_python(rectan)


@spice_error_check
def rav2xf(
    rot: Union[ndarray, Iterable[Iterable[float]]], av: Union[ndarray, Iterable[float]]
) -> ndarray:
    """
    This routine determines a state transformation matrix
    from a rotation matrix and the angular velocity of the
    rotation.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/rav2xf_c.html

    :param rot: Rotation matrix.
    :param av: Angular velocity vector.
    :return: State transformation associated with rot and av.
    """
    rot = stypes.to_double_matrix(rot)
    av = stypes.to_double_vector(av)
    xform = stypes.empty_double_matrix(x=6, y=6)
    libspice.rav2xf_c(rot, av, xform)
    return stypes.c_matrix_to_numpy(xform)


@spice_error_check
def raxisa(matrix: ndarray) -> Tuple[ndarray, float]:
    """
    Compute the axis of the rotation given by an input matrix
    and the angle of the rotation about that axis.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/raxisa_c.html

    :param matrix: Rotation matrix.
    :return: Axis of the rotation, Angle through which the rotation is performed
    """
    matrix = stypes.to_double_matrix(matrix)
    axis = stypes.empty_double_vector(3)
    angle = ctypes.c_double()
    libspice.raxisa_c(matrix, axis, ctypes.byref(angle))
    return stypes.c_vector_to_python(axis), angle.value


@spice_error_check
def rdtext(
    file: str, lenout: int = _default_len_out
) -> Tuple[str, bool]:  # pragma: no cover
    """
    Read the next line of text from a text file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/rdtext_c.html

    :param file: Name of text file.
    :param lenout: Available room in output line.
    :return: Next line from the text file, End-of-file indicator
    """
    file = stypes.string_to_char_p(file)
    line = stypes.string_to_char_p(lenout)
    lenout = ctypes.c_int(lenout)
    eof = ctypes.c_int()
    libspice.rdtext_c(file, lenout, line, ctypes.byref(eof))
    return stypes.to_python_string(line), bool(eof.value)


@spice_error_check
def recazl(
    rectan: Union[ndarray, Iterable[float]], azccw: bool, elplsz: bool
) -> Tuple[float, float, float]:
    """
    Convert rectangular coordinates of a point to range, azimuth and
    elevation.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/recazl_c.html

    :param rectan: Rectangular coordinates of a point.
    :param azccw: Flag indicating how Azimuth is measured.
    :param elplsz: Flag indicating how Elevation is measured.
    :return:
            Distance of the point from the origin,
            Azimuth in radians,
            Elevation in radians.
    """
    _rectan = stypes.to_double_vector(rectan)
    _azccw = ctypes.c_int(azccw)
    _elplsz = ctypes.c_int(elplsz)
    _range = ctypes.c_double(0)
    _az = ctypes.c_double(0)
    _el = ctypes.c_double(0)
    libspice.recazl_c(
        _rectan,
        _azccw,
        _elplsz,
        ctypes.byref(_range),
        ctypes.byref(_az),
        ctypes.byref(_el),
    )
    return _range.value, _az.value, _el.value


@spice_error_check
def reccyl(rectan: Union[ndarray, Iterable[float]]) -> Tuple[float, float, float]:
    """
    Convert from rectangular to cylindrical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/reccyl_c.html

    :param rectan: Rectangular coordinates of a point.
    :return:
            Distance from z axis,
            Angle (radians) from xZ plane,
            Height above xY plane.
    """
    rectan = stypes.to_double_vector(rectan)
    radius = ctypes.c_double(0)
    lon = ctypes.c_double(0)
    z = ctypes.c_double(0)
    libspice.reccyl_c(rectan, ctypes.byref(radius), ctypes.byref(lon), ctypes.byref(z))
    return radius.value, lon.value, z.value


@spice_error_check
def recgeo(
    rectan: Union[ndarray, Iterable[float]], re: float, f: float
) -> Tuple[float, float, float]:
    """
    Convert from rectangular coordinates to geodetic coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/recgeo_c.html

    :param rectan: Rectangular coordinates of a point.
    :param re: Equatorial radius of the reference spheroid.
    :param f: Flattening coefficient.
    :return:
            Geodetic longitude (radians),
            Geodetic latitude (radians),
            Altitude above reference spheroid
    """
    rectan = stypes.to_double_vector(rectan)
    re = ctypes.c_double(re)
    f = ctypes.c_double(f)
    longitude = ctypes.c_double(0)
    latitude = ctypes.c_double(0)
    alt = ctypes.c_double(0)
    libspice.recgeo_c(
        rectan,
        re,
        f,
        ctypes.byref(longitude),
        ctypes.byref(latitude),
        ctypes.byref(alt),
    )
    return longitude.value, latitude.value, alt.value


@spice_error_check
def reclat(rectan: Union[ndarray, Iterable[float]]) -> Tuple[float, float, float]:
    """
    Convert from rectangular coordinates to latitudinal coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/reclat_c.html

    :param rectan: Rectangular coordinates of a point.
    :return: Distance from the origin, Longitude in radians, Latitude in radians
    """
    rectan = stypes.to_double_vector(rectan)
    radius = ctypes.c_double(0)
    longitude = ctypes.c_double(0)
    latitude = ctypes.c_double(0)
    libspice.reclat_c(
        rectan, ctypes.byref(radius), ctypes.byref(longitude), ctypes.byref(latitude)
    )
    return radius.value, longitude.value, latitude.value


@spice_error_check
def recpgr(
    body: str, rectan: Union[ndarray, Iterable[float]], re: float, f: float
) -> Tuple[float, float, float]:
    """
    Convert rectangular coordinates to planetographic coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/recpgr_c.html

    :param body: Body with which coordinate system is associated.
    :param rectan: Rectangular coordinates of a point.
    :param re: Equatorial radius of the reference spheroid.
    :param f: Flattening coefficient.
    :return:
            Planetographic longitude (radians),
            Planetographic latitude (radians),
            Altitude above reference spheroid
    """
    body = stypes.string_to_char_p(body)
    rectan = stypes.to_double_vector(rectan)
    re = ctypes.c_double(re)
    f = ctypes.c_double(f)
    lon = ctypes.c_double()
    lat = ctypes.c_double()
    alt = ctypes.c_double()
    libspice.recpgr_c(
        body, rectan, re, f, ctypes.byref(lon), ctypes.byref(lat), ctypes.byref(alt)
    )
    return lon.value, lat.value, alt.value


@spice_error_check
def recrad(rectan: Union[ndarray, Iterable[float]]) -> Tuple[float, float, float]:
    """
    Convert rectangular coordinates to range, right ascension, and declination.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/recrad_c.html

    :param rectan: Rectangular coordinates of a point.
    :return:
            Distance of the point from the origin,
            Right ascension in radians,
            Declination in radians
    """
    rectan = stypes.to_double_vector(rectan)
    outrange = ctypes.c_double()
    ra = ctypes.c_double()
    dec = ctypes.c_double()
    libspice.recrad_c(
        rectan, ctypes.byref(outrange), ctypes.byref(ra), ctypes.byref(dec)
    )
    return outrange.value, ra.value, dec.value


@spice_error_check
def recsph(rectan: ndarray) -> Tuple[float, float, float]:
    """
    Convert from rectangular coordinates to spherical coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/recrad_c.html

    :param rectan: Rectangular coordinates of a point.
    :return:
            Distance from the origin,
            Angle from the positive Z-axis,
            Longitude in radians.
    """
    rectan = stypes.to_double_vector(rectan)
    r = ctypes.c_double()
    colat = ctypes.c_double()
    lon = ctypes.c_double()
    libspice.recsph_c(rectan, ctypes.byref(r), ctypes.byref(colat), ctypes.byref(lon))
    return r.value, colat.value, lon.value


@spice_error_check
def removc(item: str, inset: SpiceCell) -> None:
    """
    Remove an item from a character set.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/removc_c.html

    :param item: Item to be removed.
    :param inset: Set to be updated.
    """
    assert isinstance(inset, stypes.SpiceCell)
    assert inset.dtype == 0
    item = stypes.string_to_char_p(item)
    libspice.removc_c(item, ctypes.byref(inset))


@spice_error_check
def removd(item: float, inset: SpiceCell) -> None:
    """
    Remove an item from a double precision set.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/removd_c.html

    :param item: Item to be removed.
    :param inset: Set to be updated.
    """
    assert isinstance(inset, stypes.SpiceCell)
    assert inset.dtype == 1
    item = ctypes.c_double(item)
    libspice.removd_c(item, ctypes.byref(inset))


@spice_error_check
def removi(item: int, inset: SpiceCell) -> None:
    """
    Remove an item from an integer set.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/removi_c.html

    :param item: Item to be removed.
    :param inset: Set to be updated.
    """
    assert isinstance(inset, stypes.SpiceCell)
    assert inset.dtype == 2
    item = ctypes.c_int(item)
    libspice.removi_c(item, ctypes.byref(inset))


@spice_error_check
def reordc(
    iorder: Union[ndarray, Iterable[int]], ndim: int, lenvals: int, array: Iterable[str]
) -> Iterable[str]:
    """
    Re-order the elements of an array of character strings
    according to a given order vector.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/reordc_c.html

    :param iorder: Order vector to be used to re-order array.
    :param ndim: Dimension of array.
    :param lenvals: String length.
    :param array: Array to be re-ordered.
    :return: Re-ordered Array.
    """
    iorder = stypes.to_int_vector(iorder)
    ndim = ctypes.c_int(ndim)
    lenvals = ctypes.c_int(lenvals + 1)
    array = stypes.list_to_char_array(array, x_len=lenvals, y_len=ndim)
    libspice.reordc_c(iorder, ndim, lenvals, array)
    return [stypes.to_python_string(x.value) for x in array]


@spice_error_check
def reordd(
    iorder: Union[ndarray, Iterable[int]],
    ndim: int,
    array: Union[ndarray, Iterable[float]],
) -> ndarray:
    """
    Re-order the elements of a double precision array according to
    a given order vector.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/reordd_c.html

    :param iorder: Order vector to be used to re-order array.
    :param ndim: Dimension of array.
    :param array: Array to be re-ordered.
    :return: Re-ordered Array.
    """
    iorder = stypes.to_int_vector(iorder)
    ndim = ctypes.c_int(ndim)
    array = stypes.to_double_vector(array)
    libspice.reordd_c(iorder, ndim, array)
    return stypes.c_vector_to_python(array)


@spice_error_check
def reordi(
    iorder: Union[ndarray, Iterable[int]],
    ndim: int,
    array: Union[ndarray, Iterable[int]],
) -> ndarray:
    """
    Re-order the elements of an integer array according to
    a given order vector.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/reordi_c.html

    :param iorder: Order vector to be used to re-order array.
    :param ndim: Dimension of array.
    :param array: Array to be re-ordered.
    :return: Re-ordered Array.
    """
    iorder = stypes.to_int_vector(iorder)
    ndim = ctypes.c_int(ndim)
    array = stypes.to_int_vector(array)
    libspice.reordi_c(iorder, ndim, array)
    return stypes.c_vector_to_python(array)


@spice_error_check
def reordl(
    iorder: Union[ndarray, Iterable[int]], ndim: int, array: Iterable[bool]
) -> ndarray:
    """
    Re-order the elements of a logical (Boolean) array according to
    a given order vector.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/reordl_c.html

    :param iorder: Order vector to be used to re-order array.
    :param ndim: Dimension of array.
    :param array: Array to be re-ordered.
    :return: Re-ordered Array.
    """
    iorder = stypes.to_int_vector(iorder)
    ndim = ctypes.c_int(ndim)
    array = stypes.to_int_vector(array)
    libspice.reordl_c(iorder, ndim, array)
    return stypes.c_int_vector_to_bool_python(array)


@spice_error_check
def repmc(instr: str, marker: str, value: str, lenout: Optional[int] = None) -> str:
    """
    Replace a marker with a character string.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/repmc_c.html

    :param instr: Input string.
    :param marker: Marker to be replaced.
    :param value: Replacement value.
    :param lenout: Optional available space in output string
    :return: Output string.
    """
    if lenout is None:
        lenout = ctypes.c_int(len(instr) + len(value) + len(marker) + 15)
    instr = stypes.string_to_char_p(instr)
    marker = stypes.string_to_char_p(marker)
    value = stypes.string_to_char_p(value)
    out = stypes.string_to_char_p(lenout)
    libspice.repmc_c(instr, marker, value, lenout, out)
    return stypes.to_python_string(out)


@spice_error_check
def repmct(
    instr: str, marker: str, value: int, repcase: str, lenout: Optional[int] = None
) -> str:
    """
    Replace a marker with the text representation of a
    cardinal number.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/repmc_c.html

    :param instr: Input string.
    :param marker: Marker to be replaced.
    :param value: Replacement value.
    :param repcase: Case of replacement text.
    :param lenout: Optional available space in output string
    :return: Output string.
    """
    if lenout is None:
        lenout = ctypes.c_int(len(instr) + len(marker) + 15)
    instr = stypes.string_to_char_p(instr)
    marker = stypes.string_to_char_p(marker)
    value = ctypes.c_int(value)
    repcase = ctypes.c_char(repcase.encode(encoding="UTF-8"))
    out = stypes.string_to_char_p(lenout)
    libspice.repmct_c(instr, marker, value, repcase, lenout, out)
    return stypes.to_python_string(out)


@spice_error_check
def repmd(instr: str, marker: str, value: float, sigdig: int) -> str:
    """
    Replace a marker with a double precision number.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/repmd_c.html

    :param instr: Input string.
    :param marker: Marker to be replaced.
    :param value: Replacement value.
    :param sigdig: Significant digits in replacement text.
    :return: Output string.
    """
    lenout = ctypes.c_int(len(instr) + len(marker) + 15)
    instr = stypes.string_to_char_p(instr)
    marker = stypes.string_to_char_p(marker)
    value = ctypes.c_double(value)
    sigdig = ctypes.c_int(sigdig)
    out = stypes.string_to_char_p(lenout)
    libspice.repmd_c(instr, marker, value, sigdig, lenout, out)
    return stypes.to_python_string(out)


@spice_error_check
def repmf(
    instr: str,
    marker: str,
    value: float,
    sigdig: int,
    informat: str,
    lenout: Optional[int] = None,
) -> str:
    """
    Replace a marker in a string with a formatted double precision value.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/repmf_c.html

    :param instr: Input string.
    :param marker: Marker to be replaced.
    :param value: Replacement value.
    :param sigdig: Significant digits in replacement text.
    :param informat: Format 'E' or 'F'.
    :param lenout: Optional available space in output string.
    :return: Output string.
    """
    if lenout is None:
        lenout = ctypes.c_int(len(instr) + len(marker) + 15)
    instr = stypes.string_to_char_p(instr)
    marker = stypes.string_to_char_p(marker)
    value = ctypes.c_double(value)
    sigdig = ctypes.c_int(sigdig)
    informat = ctypes.c_char(informat.encode(encoding="UTF-8"))
    out = stypes.string_to_char_p(lenout)
    libspice.repmf_c(instr, marker, value, sigdig, informat, lenout, out)
    return stypes.to_python_string(out)


@spice_error_check
def repmi(instr: str, marker: str, value: int, lenout: Optional[int] = None) -> str:
    """
    Replace a marker with an integer.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/repmi_c.html

    :param instr: Input string.
    :param marker: Marker to be replaced.
    :param value: Replacement value.
    :param lenout: Optional available space in output string.
    :return: Output string.
    """
    if lenout is None:
        lenout = ctypes.c_int(len(instr) + len(marker) + 15)
    instr = stypes.string_to_char_p(instr)
    marker = stypes.string_to_char_p(marker)
    value = ctypes.c_int(value)
    out = stypes.string_to_char_p(lenout)
    libspice.repmi_c(instr, marker, value, lenout, out)
    return stypes.to_python_string(out)


@spice_error_check
def repmot(
    instr: str, marker: str, value: int, repcase: str, lenout: Optional[int] = None
) -> str:
    """
    Replace a marker with the text representation of an ordinal number.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/repmot_c.html

    :param instr: Input string.
    :param marker: Marker to be replaced.
    :param value: Replacement value.
    :param repcase: Case of replacement text.
    :param lenout: Optional available space in output string.
    :return: Output string.
    """
    if lenout is None:
        lenout = ctypes.c_int(len(instr) + len(marker) + 15)
    instr = stypes.string_to_char_p(instr)
    marker = stypes.string_to_char_p(marker)
    value = ctypes.c_int(value)
    repcase = ctypes.c_char(repcase.encode(encoding="UTF-8"))
    out = stypes.string_to_char_p(lenout)
    libspice.repmot_c(instr, marker, value, repcase, lenout, out)
    return stypes.to_python_string(out)


def reset() -> None:
    """
    Reset the SPICE error status to a value of "no error."
    As a result, the status routine, failed, will return a value
    of False

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/reset_c.html

    """
    libspice.reset_c()


@spice_error_check
def return_c() -> bool:
    """
    True if SPICE routines should return immediately upon entry.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/return_c.html

    :return: True if SPICE routines should return immediately upon entry.
    """
    return bool(libspice.return_c())


@spice_error_check
def rotate(angle: float, iaxis: int) -> ndarray:
    """
    Calculate the 3x3 rotation matrix generated by a rotation
    of a specified angle about a specified axis. This rotation
    is thought of as rotating the coordinate system.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/rotate_c.html

    :param angle: Angle of rotation (radians).
    :param iaxis: Axis of rotation X=1, Y=2, Z=3.
    :return: Resulting rotation matrix
    """
    angle = ctypes.c_double(angle)
    iaxis = ctypes.c_int(iaxis)
    mout = stypes.empty_double_matrix()
    libspice.rotate_c(angle, iaxis, mout)
    return stypes.c_matrix_to_numpy(mout)


@spice_error_check
def rotmat(m1: ndarray, angle: float, iaxis: int) -> ndarray:
    """
    Rotmat applies a rotation of angle radians about axis iaxis to a
    matrix. This rotation is thought of as rotating the coordinate
    system.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/rotmat_c.html

    :param m1: Matrix to be rotated.
    :param angle: Angle of rotation (radians).
    :param iaxis: Axis of rotation X=1, Y=2, Z=3.
    :return: Resulting rotated matrix.
    """
    m1 = stypes.to_double_matrix(m1)
    angle = ctypes.c_double(angle)
    iaxis = ctypes.c_int(iaxis)
    mout = stypes.empty_double_matrix()
    libspice.rotmat_c(m1, angle, iaxis, mout)
    return stypes.c_matrix_to_numpy(mout)


@spice_error_check
def rotvec(v1: Iterable[Union[float, float]], angle: float, iaxis: int) -> ndarray:
    """
    Transform a vector to a new coordinate system rotated by angle
    radians about axis iaxis.  This transformation rotates v1 by
    angle radians about the specified axis.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/rotvec_c.html

    :param v1: Vector whose coordinate system is to be rotated.
    :param angle: Angle of rotation (radians).
    :param iaxis: Axis of rotation X=1, Y=2, Z=3.
    :return: the vector expressed in the new coordinate system.
    """
    v1 = stypes.to_double_vector(v1)
    angle = ctypes.c_double(angle)
    iaxis = ctypes.c_int(iaxis)
    vout = stypes.empty_double_vector(3)
    libspice.rotvec_c(v1, angle, iaxis, vout)
    return stypes.c_vector_to_python(vout)


@spice_error_check
def rpd() -> float:
    """
    Return the number of radians per degree.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/rpd_c.html

    :return: The number of radians per degree, pi/180.
    """
    return libspice.rpd_c()


@spice_error_check
def rquad(a: float, b: float, c: float) -> Tuple[ndarray, ndarray]:
    """
    Find the roots of a quadratic equation.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/rquad_c.html

    :param a: Coefficient of quadratic term.
    :param b: Coefficient of linear term.
    :param c: Constant.
    :return: Root built from positive and negative discriminant term.
    """
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    root1 = stypes.empty_double_vector(2)
    root2 = stypes.empty_double_vector(2)
    libspice.rquad_c(a, b, c, root1, root2)
    return stypes.c_vector_to_python(root1), stypes.c_vector_to_python(root2)


################################################################################
# S


@spice_error_check
def saelgv(
    vec1: Union[ndarray, Iterable[float]], vec2: Union[ndarray, Iterable[float]]
) -> Tuple[ndarray, ndarray]:
    """
    Find semi-axis vectors of an ellipse generated by two arbitrary
    three-dimensional vectors.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/saelgv_c.html

    :param vec1: First vector used to generate an ellipse.
    :param vec2: Second vector used to generate an ellipse.
    :return: Semi-major axis of ellipse, Semi-minor axis of ellipse.
    """
    vec1 = stypes.to_double_vector(vec1)
    vec2 = stypes.to_double_vector(vec2)
    smajor = stypes.empty_double_vector(3)
    sminor = stypes.empty_double_vector(3)
    libspice.saelgv_c(vec1, vec2, smajor, sminor)
    return stypes.c_vector_to_python(smajor), stypes.c_vector_to_python(sminor)


@spice_error_check
def scard(incard: int, cell: SpiceCell) -> SpiceCell:
    """
    Set the cardinality of a SPICE cell of any data type.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scard_c.html

    :param incard: Cardinality of (number of elements in) the cell.
    :param cell: The cell.
    :return: The updated Cell.
    """
    assert isinstance(cell, stypes.SpiceCell)
    incard = ctypes.c_int(incard)
    libspice.scard_c(incard, ctypes.byref(cell))
    return cell


@spice_error_check
def scdecd(
    sc: int, sclkdp: float, lenout: int = _default_len_out, mxpart: Optional[int] = None
) -> str:
    # todo: figure out how to use mxpart
    """
    Convert double precision encoding of spacecraft clock time into
    a character representation.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scdecd_c.html

    :param sc: NAIF spacecraft identification code.
    :param sclkdp: Encoded representation of a spacecraft clock count.
    :param lenout: Maximum allowed length of output SCLK string.
    :param mxpart: Maximum number of spacecraft clock partitions.
    :return: Character representation of a clock count.
    """
    sc = ctypes.c_int(sc)
    sclkdp = ctypes.c_double(sclkdp)
    sclkch = stypes.string_to_char_p(" " * lenout)
    lenout = ctypes.c_int(lenout)
    libspice.scdecd_c(sc, sclkdp, lenout, sclkch)
    return stypes.to_python_string(sclkch)


@spice_error_check
def sce2c(sc: int, et: float) -> float:
    """
    Convert ephemeris seconds past J2000 (ET) to continuous encoded
    spacecraft clock "ticks".  Non-integral tick values may be
    returned.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sce2c_c.html

    :param sc: NAIF spacecraft ID code.
    :param et: Ephemeris time, seconds past J2000.
    :return:
            SCLK, encoded as ticks since spacecraft clock start.
            sclkdp need not be integral.
    """
    sc = ctypes.c_int(sc)
    et = ctypes.c_double(et)
    sclkdp = ctypes.c_double()
    libspice.sce2c_c(sc, et, ctypes.byref(sclkdp))
    return sclkdp.value


@spice_error_check
def sce2s(sc: int, et: float, lenout: int = _default_len_out) -> str:
    """
    Convert an epoch specified as ephemeris seconds past J2000 (ET) to a
    character string representation of a spacecraft clock value (SCLK).

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sce2s_c.html

    :param sc: NAIF spacecraft clock ID code.
    :param et: Ephemeris time, specified as seconds past J2000.
    :param lenout: Maximum length of output string.
    :return: An SCLK string.
    """
    sc = ctypes.c_int(sc)
    et = ctypes.c_double(et)
    sclkch = stypes.string_to_char_p(" " * lenout)
    lenout = ctypes.c_int(lenout)
    libspice.sce2s_c(sc, et, lenout, sclkch)
    return stypes.to_python_string(sclkch)


@spice_error_check
def sce2t(sc: int, et: float) -> float:
    """
    Convert ephemeris seconds past J2000 (ET) to integral
    encoded spacecraft clock ("ticks"). For conversion to
    fractional ticks, (required for C-kernel production), see
    the routine :func:`sce2c`.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sce2t_c.html

    :param sc: NAIF spacecraft ID code.
    :param et: Ephemeris time, seconds past J2000.
    :return: SCLK, encoded as ticks since spacecraft clock start.
    """
    sc = ctypes.c_int(sc)
    et = ctypes.c_double(et)
    sclkdp = ctypes.c_double()
    libspice.sce2t_c(sc, et, ctypes.byref(sclkdp))
    return sclkdp.value


@spice_error_check
def scencd(
    sc: int, sclkch: Union[str, Iterable[str]], mxpart: Optional[int] = None
) -> Union[float, ndarray]:
    """
    Encode character representation of spacecraft clock time into a
    double precision number.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scencd_c.html

    :param sc: NAIF spacecraft identification code.
    :param sclkch: Character representation of a spacecraft clock.
    :param mxpart: Maximum number of spacecraft clock partitions.
    :return: Encoded representation of the clock count.
    """
    sc = ctypes.c_int(sc)
    sclkdp = ctypes.c_double()
    if stypes.is_iterable(sclkch):
        results = []
        for chars in sclkch:
            libspice.scencd_c(sc, stypes.string_to_char_p(chars), ctypes.byref(sclkdp))
            check_for_spice_error(None)
            results.append(sclkdp.value)
        return numpy.array(results)
    else:
        libspice.scencd_c(sc, stypes.string_to_char_p(sclkch), ctypes.byref(sclkdp))
        return sclkdp.value


@spice_error_check
def scfmt(sc: int, ticks: float, lenout: int = _default_len_out) -> str:
    """
    Convert encoded spacecraft clock ticks to character clock format.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scfmt_c.html

    :param sc: NAIF spacecraft identification code.
    :param ticks: Encoded representation of a spacecraft clock count.
    :param lenout: Maximum allowed length of output string.
    :return: Character representation of a clock count.
    """
    sc = ctypes.c_int(sc)
    ticks = ctypes.c_double(ticks)
    clkstr = stypes.string_to_char_p(lenout)
    lenout = ctypes.c_int(lenout)
    libspice.scfmt_c(sc, ticks, lenout, clkstr)
    return stypes.to_python_string(clkstr)


@spice_error_check
def scpart(sc: int) -> Tuple[ndarray, ndarray]:
    """
    Get spacecraft clock partition information from a spacecraft
    clock kernel file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scpart_c.html

    :param sc: NAIF spacecraft identification code.
    :return:
            The number of spacecraft clock partitions,
            Array of partition start times,
            Array of partition stop times.
    """
    sc = ctypes.c_int(sc)
    nparts = ctypes.c_int()
    pstart = stypes.empty_double_vector(9999)
    pstop = stypes.empty_double_vector(9999)
    libspice.scpart_c(sc, nparts, pstart, pstop)
    return (
        stypes.c_vector_to_python(pstart)[0 : nparts.value],
        stypes.c_vector_to_python(pstop)[0 : nparts.value],
    )


@spice_error_check
def scs2e(sc: int, sclkch: str) -> float:
    """
    Convert a spacecraft clock string to ephemeris seconds past J2000 (ET).

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scs2e_c.html

    :param sc: NAIF integer code for a spacecraft.
    :param sclkch: An SCLK string.
    :return: Ephemeris time, seconds past J2000.
    """
    sc = ctypes.c_int(sc)
    sclkch = stypes.string_to_char_p(sclkch)
    et = ctypes.c_double()
    libspice.scs2e_c(sc, sclkch, ctypes.byref(et))
    return et.value


@spice_error_check
def sct2e(sc: int, sclkdp: Union[float, Iterable[float]]) -> Union[float, ndarray]:
    """
    Convert encoded spacecraft clock ("ticks") to ephemeris
    seconds past J2000 (ET).

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sct2e_c.html

    :param sc: NAIF spacecraft ID code.
    :param sclkdp: SCLK, encoded as ticks since spacecraft clock start.
    :return: Ephemeris time, seconds past J2000.
    """
    sc = ctypes.c_int(sc)
    et = ctypes.c_double()
    if stypes.is_iterable(sclkdp):
        results = []
        for sclk in sclkdp:
            libspice.sct2e_c(sc, ctypes.c_double(sclk), ctypes.byref(et))
            check_for_spice_error(None)
            results.append(et.value)
        return numpy.array(results)
    else:
        sclkdp = ctypes.c_double(sclkdp)
        libspice.sct2e_c(sc, sclkdp, ctypes.byref(et))
        return et.value


@spice_error_check
def sctiks(sc: int, clkstr: str) -> float:
    """
    Convert a spacecraft clock format string to number of "ticks".

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sctiks_c.html

    :param sc: NAIF spacecraft identification code.
    :param clkstr: Character representation of a spacecraft clock.
    :return: Number of ticks represented by the clock string.
    """
    sc = ctypes.c_int(sc)
    clkstr = stypes.string_to_char_p(clkstr)
    ticks = ctypes.c_double()
    libspice.sctiks_c(sc, clkstr, ctypes.byref(ticks))
    return ticks.value


@spice_error_check
def sdiff(a: SpiceCell, b: SpiceCell) -> SpiceCell:
    """
    Take the symmetric difference of two sets of any data type to form a
    third set.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sdiff_c.html

    :param a: First input set.
    :param b: Second input set.
    :return: Symmetric difference of a and b.
    """
    assert isinstance(a, stypes.SpiceCell)
    assert isinstance(b, stypes.SpiceCell)
    assert a.dtype == b.dtype
    # The next line was redundant with the [raise NotImplementedError] line below
    # assert a.dtype == 0 or a.dtype == 1 or a.dtype == 2
    if a.dtype == 0:
        c = stypes.SPICECHAR_CELL(a.size, a.length)
    elif a.dtype == 1:
        c = stypes.SPICEDOUBLE_CELL(a.size)
    elif a.dtype == 2:
        c = stypes.SPICEINT_CELL(a.size)
    else:
        raise NotImplementedError
    libspice.sdiff_c(ctypes.byref(a), ctypes.byref(b), ctypes.byref(c))
    return c


@spice_error_check
def set_c(a: SpiceCell, op: str, b: SpiceCell) -> bool:
    """
    Given a relational operator, compare two sets of any data type.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/set_c.html

    :param a: First set.
    :param op: Comparison operator.
    :param b: Second set.
    :return: The function returns the result of the comparison.
    """
    assert isinstance(a, stypes.SpiceCell)
    assert isinstance(b, stypes.SpiceCell)
    assert a.dtype == b.dtype
    assert isinstance(op, str)
    op = stypes.string_to_char_p(op)
    return bool(libspice.set_c(ctypes.byref(a), op, ctypes.byref(b)))


@spice_error_check
def setmsg(message: str) -> None:
    """
    Set the value of the current long error message.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/setmsg_c.html

    :param message: A long error message.
    """
    message = stypes.string_to_char_p(message)
    libspice.setmsg_c(message)


@spice_error_check
def shellc(ndim: int, lenvals: int, array: Iterable[str]) -> Iterable[str]:
    # This works! looks like this is a mutable 2d char array
    """
    Sort an array of character strings according to the ASCII
    collating sequence using the Shell Sort algorithm.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/shellc_c.html

    :param ndim: Dimension of the array.
    :param lenvals: String length.
    :param array: The array to be sorted.
    :return: The sorted array.
    """
    array = stypes.list_to_char_array(array, x_len=lenvals, y_len=ndim)
    ndim = ctypes.c_int(ndim)
    lenvals = ctypes.c_int(lenvals)
    libspice.shellc_c(ndim, lenvals, ctypes.byref(array))
    return stypes.c_vector_to_python(array)


@spice_error_check
def shelld(ndim: int, array: Union[ndarray, Iterable[float]]) -> ndarray:
    # Works!, use this as example for "I/O" parameters
    """
    Sort a double precision array using the Shell Sort algorithm.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/shelld_c.html

    :param ndim: Dimension of the array.
    :param array: The array to be sorted.
    :return: The sorted array.
    """
    array = stypes.to_double_vector(array)
    ndim = ctypes.c_int(ndim)
    libspice.shelld_c(ndim, ctypes.cast(array, ctypes.POINTER(ctypes.c_double)))
    return stypes.c_vector_to_python(array)


@spice_error_check
def shelli(ndim: int, array: Union[ndarray, Iterable[int]]) -> ndarray:
    # Works!, use this as example for "I/O" parameters
    """
    Sort an integer array using the Shell Sort algorithm.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/shelli_c.html

    :param ndim: Dimension of the array.
    :param array: The array to be sorted.
    :return: The sorted array.
    """
    array = stypes.to_int_vector(array)
    ndim = ctypes.c_int(ndim)
    libspice.shelli_c(ndim, ctypes.cast(array, ctypes.POINTER(ctypes.c_int)))
    return stypes.c_vector_to_python(array)


def sigerr(message: str) -> None:
    """
    Inform the CSPICE error processing mechanism that an error has
    occurred, and specify the type of error.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sigerr_c.html

    :param message: A short error message.
    """
    message = stypes.string_to_char_p(message)
    libspice.sigerr_c(message)


@spice_error_check
@spice_found_exception_thrower
def sincpt(
    method: str,
    target: str,
    et: float,
    fixref: str,
    abcorr: str,
    obsrvr: str,
    dref: str,
    dvec: ndarray,
) -> Tuple[ndarray, float, ndarray, bool]:
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
            Surface intercept point on the target body,
            Intercept epoch,
            Vector from observer to intercept point.
    """
    method = stypes.string_to_char_p(method)
    target = stypes.string_to_char_p(target)
    et = ctypes.c_double(et)
    fixref = stypes.string_to_char_p(fixref)
    abcorr = stypes.string_to_char_p(abcorr)
    obsrvr = stypes.string_to_char_p(obsrvr)
    dref = stypes.string_to_char_p(dref)
    dvec = stypes.to_double_vector(dvec)
    spoint = stypes.empty_double_vector(3)
    trgepc = ctypes.c_double(0)
    srfvec = stypes.empty_double_vector(3)
    found = ctypes.c_int(0)
    libspice.sincpt_c(
        method,
        target,
        et,
        fixref,
        abcorr,
        obsrvr,
        dref,
        dvec,
        spoint,
        ctypes.byref(trgepc),
        srfvec,
        ctypes.byref(found),
    )
    return (
        stypes.c_vector_to_python(spoint),
        trgepc.value,
        stypes.c_vector_to_python(srfvec),
        bool(found.value),
    )


@spice_error_check
def size(cell: SpiceCell) -> int:
    """
    Return the size (maximum cardinality) of a SPICE cell of any
    data type.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/size_c.html

    :param cell: Input cell.
    :return: The size of the input cell.
    """
    assert isinstance(cell, stypes.SpiceCell)
    return libspice.size_c(ctypes.byref(cell))


@spice_error_check
def spd() -> float:
    """
    Return the number of seconds in a day.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spd_c.html

    :return: The number of seconds in a day.
    """
    return libspice.spd_c()


@spice_error_check
def sphcyl(radius: float, colat: float, slon: float) -> Tuple[float, float, float]:
    """
    This routine converts from spherical coordinates to cylindrical
    coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sphcyl_c.html

    :param radius: Distance of point from origin.
    :param colat: Polar angle (co-latitude in radians) of point.
    :param slon: Azimuthal angle (longitude) of point (radians).
    :return:
            Distance of point from z axis,
            angle (radians) of point from XZ plane,
            Height of point above XY plane.
    """
    radius = ctypes.c_double(radius)
    colat = ctypes.c_double(colat)
    slon = ctypes.c_double(slon)
    r = ctypes.c_double()
    lon = ctypes.c_double()
    z = ctypes.c_double()
    libspice.sphcyl_c(
        radius, colat, slon, ctypes.byref(r), ctypes.byref(lon), ctypes.byref(z)
    )
    return r.value, lon.value, z.value


@spice_error_check
def sphlat(r: float, colat: float, lons: float) -> Tuple[float, float, float]:
    """
    Convert from spherical coordinates to latitudinal coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sphlat_c.html

    :param r: Distance of the point from the origin.
    :param colat: Angle of the point from positive z axis (radians).
    :param lons: Angle of the point from the XZ plane (radians).
    :return:
            Distance of a point from the origin,
            Angle of the point from the XZ plane in radians,
            Angle of the point from the XY plane in radians.
    """
    r = ctypes.c_double(r)
    colat = ctypes.c_double(colat)
    lons = ctypes.c_double(lons)
    radius = ctypes.c_double()
    lon = ctypes.c_double()
    lat = ctypes.c_double()
    libspice.sphcyl_c(
        r, colat, lons, ctypes.byref(radius), ctypes.byref(lon), ctypes.byref(lat)
    )
    return radius.value, lon.value, lat.value


@spice_error_check
def sphrec(r: float, colat: float, lon: float) -> ndarray:
    """
    Convert from spherical coordinates to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sphrec_c.html

    :param r: Distance of a point from the origin.
    :param colat: Angle of the point from the positive Z-axis.
    :param lon: Angle of the point from the XZ plane in radians.
    :return: Rectangular coordinates of the point.
    """
    r = ctypes.c_double(r)
    colat = ctypes.c_double(colat)
    lon = ctypes.c_double(lon)
    rectan = stypes.empty_double_vector(3)
    libspice.sphrec_c(r, colat, lon, rectan)
    return stypes.c_vector_to_python(rectan)


@spice_error_check
def spkacs(
    targ: int, et: float, ref: str, abcorr: str, obs: int
) -> Tuple[ndarray, float, float]:
    """
    Return the state (position and velocity) of a target body
    relative to an observer, optionally corrected for light time
    and stellar aberration, expressed relative to an inertial
    reference frame.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkacs_c.html

    :param targ: Target body.
    :param et: Observer epoch.
    :param ref: Inertial reference frame of output state.
    :param abcorr: Aberration correction flag.
    :param obs: Observer.
    :return:
            State of target,
            One way light time between observer and target,
            Derivative of light time with respect to time.
    """
    targ = ctypes.c_int(targ)
    et = ctypes.c_double(et)
    ref = stypes.string_to_char_p(ref)
    abcorr = stypes.string_to_char_p(abcorr)
    obs = ctypes.c_int(obs)
    starg = stypes.empty_double_vector(6)
    lt = ctypes.c_double()
    dlt = ctypes.c_double()
    libspice.spkacs_c(
        targ, et, ref, abcorr, obs, starg, ctypes.byref(lt), ctypes.byref(dlt)
    )
    return stypes.c_vector_to_python(starg), lt.value, dlt.value


@spice_error_check
def spkapo(
    targ: int, et: float, ref: str, sobs: ndarray, abcorr: str
) -> Tuple[ndarray, float]:
    """
    Return the position of a target body relative to an observer,
    optionally corrected for light time and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkapo_c.html

    :param targ: Target body.
    :param et: Observer epoch.
    :param ref: Inertial reference frame of observer's state.
    :param sobs: State of observer wrt. solar system barycenter.
    :param abcorr: Aberration correction flag.
    :return:
            Position of target,
            One way light time between observer and target.
    """
    targ = ctypes.c_int(targ)
    et = ctypes.c_double(et)
    ref = stypes.string_to_char_p(ref)
    abcorr = stypes.string_to_char_p(abcorr)
    sobs = stypes.to_double_vector(sobs)
    ptarg = stypes.empty_double_vector(3)
    lt = ctypes.c_double()
    libspice.spkapo_c(targ, et, ref, sobs, abcorr, ptarg, ctypes.byref(lt))
    return stypes.c_vector_to_python(ptarg), lt.value


@spice_error_check
def spkapp(
    targ: int, et: float, ref: str, sobs: ndarray, abcorr: str
) -> Tuple[ndarray, float]:
    """
    Deprecated: This routine has been superseded by :func:`spkaps`. This
    routine is supported for purposes of backward compatibility only.

    Return the state (position and velocity) of a target body
    relative to an observer, optionally corrected for light time and
    stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkapp_c.html

    :param targ: Target body.
    :param et: Observer epoch.
    :param ref: Inertial reference frame of observer's state.
    :param sobs: State of observer wrt. solar system barycenter.
    :param abcorr: Aberration correction flag.
    :return:
            State of target,
            One way light time between observer and target.
    """
    targ = ctypes.c_int(targ)
    et = ctypes.c_double(et)
    ref = stypes.string_to_char_p(ref)
    abcorr = stypes.string_to_char_p(abcorr)
    sobs = stypes.to_double_vector(sobs)
    starg = stypes.empty_double_vector(6)
    lt = ctypes.c_double()
    libspice.spkapp_c(targ, et, ref, sobs, abcorr, starg, ctypes.byref(lt))
    return stypes.c_vector_to_python(starg), lt.value


@spice_error_check
def spkaps(
    targ: int,
    et: float,
    ref: str,
    abcorr: str,
    stobs: ndarray,
    accobs: Iterable[Union[float, float]],
) -> Tuple[ndarray, float, float]:
    """
    Given the state and acceleration of an observer relative to the
    solar system barycenter, return the state (position and velocity)
    of a target body relative to the observer, optionally corrected
    for light time and stellar aberration. All input and output
    vectors are expressed relative to an inertial reference frame.

    This routine supersedes :func:`spkapp`.

    SPICE users normally should call the high-level API routines
    :func:`spkezr` or :func:`spkez` rather than this routine.
    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkaps_c.html

    :param targ: Target body.
    :param et: Observer epoch.
    :param ref: Inertial reference frame of output state.
    :param abcorr: Aberration correction flag.
    :param stobs: State of the observer relative to the SSB.
    :param accobs: Acceleration of the observer relative to the SSB.
    :return:
             State of target,
             One way light time between observer and target,
             Derivative of light time with respect to time.
    """
    targ = ctypes.c_int(targ)
    et = ctypes.c_double(et)
    ref = stypes.string_to_char_p(ref)
    abcorr = stypes.string_to_char_p(abcorr)
    stobs = stypes.to_double_vector(stobs)
    accobs = stypes.to_double_vector(accobs)
    starg = stypes.empty_double_vector(6)
    lt = ctypes.c_double()
    dlt = ctypes.c_double()
    libspice.spkaps_c(
        targ, et, ref, abcorr, stobs, accobs, starg, ctypes.byref(lt), ctypes.byref(dlt)
    )
    return stypes.c_vector_to_python(starg), lt.value, dlt.value


@spice_error_check
def spk14a(
    handle: int,
    ncsets: int,
    coeffs: Union[ndarray, Iterable[float]],
    epochs: Union[ndarray, Iterable[float]],
) -> None:
    """
    Add data to a type 14 SPK segment associated with handle. See
    also :func:`spk14b` and :func:`spk14e`.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spk14a_c.html

    :param handle: The handle of an SPK file open for writing.
    :param ncsets: The number of coefficient sets and epochs.
    :param coeffs: The collection of coefficient sets.
    :param epochs: The epochs associated with the coefficient sets.
    """
    handle = ctypes.c_int(handle)
    ncsets = ctypes.c_int(ncsets)
    coeffs = stypes.to_double_vector(coeffs)
    epochs = stypes.to_double_vector(epochs)
    libspice.spk14a_c(handle, ncsets, coeffs, epochs)


@spice_error_check
def spk14b(
    handle: int,
    segid: str,
    body: int,
    center: int,
    framename: str,
    first: float,
    last: float,
    chbdeg: int,
) -> None:
    """
    Begin a type 14 SPK segment in the SPK file associated with
    handle. See also :func:`spk14a` and :func:`spk14e`.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spk14b_c.html

    :param handle: The handle of an SPK file open for writing.
    :param segid: The string to use for segment identifier.
    :param body: The NAIF ID code for the body of the segment.
    :param center: The center of motion for body.
    :param framename: The reference frame for this segment.
    :param first: The first epoch for which the segment is valid.
    :param last: The last epoch for which the segment is valid.
    :param chbdeg: The degree of the Chebyshev Polynomial used.
    """
    handle = ctypes.c_int(handle)
    segid = stypes.string_to_char_p(segid)
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    framename = stypes.string_to_char_p(framename)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    chbdeg = ctypes.c_int(chbdeg)
    libspice.spk14b_c(handle, segid, body, center, framename, first, last, chbdeg)


@spice_error_check
def spk14e(handle: int) -> None:
    """
    End the type 14 SPK segment currently being written to the SPK
    file associated with handle. See also :func:`spk14a` and :func:`spk14b`.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spk14e_c.html

    :param handle: The handle of an SPK file open for writing.
    """
    handle = ctypes.c_int(handle)
    libspice.spk14e_c(handle)


@spice_error_check
def spkcls(handle: int) -> None:
    """
    Close an open SPK file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkcls_c.html

    :param handle: Handle of the SPK file to be closed.
    """
    handle = ctypes.c_int(handle)
    libspice.spkcls_c(handle)


@spice_error_check
def spkcov(spk: str, idcode: int, cover: Optional[SpiceCell] = None) -> SpiceCell:
    """
    Find the coverage window for a specified ephemeris object in a
    specified SPK file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkcov_c.html

    :param spk: Name of SPK file.
    :param idcode: ID code of ephemeris object.
    :param cover: Optional SPICE Window giving coverage in "spk" for "idcode".
    """
    spk = stypes.string_to_char_p(spk)
    idcode = ctypes.c_int(idcode)
    if cover is None:
        cover = stypes.SPICEDOUBLE_CELL(2000)
    else:
        assert isinstance(cover, stypes.SpiceCell)
        assert cover.is_double()
    libspice.spkcov_c(spk, idcode, ctypes.byref(cover))
    return cover


@spice_error_check
def spkcpo(
    target: str,
    et: float,
    outref: str,
    refloc: str,
    abcorr: str,
    obspos: Union[ndarray, Iterable[float]],
    obsctr: str,
    obsref: str,
) -> Tuple[ndarray, float]:
    """
    Return the state of a specified target relative to an "observer,"
    where the observer has constant position in a specified reference
    frame. The observer's position is provided by the calling program
    rather than by loaded SPK files.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkcpo_c.html

    :param target: Name of target ephemeris object.
    :param et: Observation epoch.
    :param outref: Reference frame of output state.
    :param refloc: Output reference frame evaluation locus.
    :param abcorr: Aberration correction.
    :param obspos: Observer position relative to center of motion.
    :param obsctr: Center of motion of observer.
    :param obsref: Frame of observer position.
    :return:
            State of target with respect to observer,
            One way light time between target and observer.
    """
    target = stypes.string_to_char_p(target)
    et = ctypes.c_double(et)
    outref = stypes.string_to_char_p(outref)
    refloc = stypes.string_to_char_p(refloc)
    abcorr = stypes.string_to_char_p(abcorr)
    obspos = stypes.to_double_vector(obspos)
    obsctr = stypes.string_to_char_p(obsctr)
    obsref = stypes.string_to_char_p(obsref)
    state = stypes.empty_double_vector(6)
    lt = ctypes.c_double()
    libspice.spkcpo_c(
        target,
        et,
        outref,
        refloc,
        abcorr,
        obspos,
        obsctr,
        obsref,
        state,
        ctypes.byref(lt),
    )
    return stypes.c_vector_to_python(state), lt.value


@spice_error_check
def spkcpt(
    trgpos: Union[ndarray, Iterable[float]],
    trgctr: str,
    trgref: str,
    et: float,
    outref: str,
    refloc: str,
    abcorr: str,
    obsrvr: str,
) -> Tuple[ndarray, float]:
    """
    Return the state, relative to a specified observer, of a target
    having constant position in a specified reference frame. The
    target's position is provided by the calling program rather than by
    loaded SPK files.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkcpt_c.html

    :param trgpos: Target position relative to center of motion.
    :param trgctr: Center of motion of target.
    :param trgref: Observation epoch.
    :param et: Observation epoch.
    :param outref: Reference frame of output state.
    :param refloc: Output reference frame evaluation locus.
    :param abcorr: Aberration correction.
    :param obsrvr: Name of observing ephemeris object.
    :return:
            State of target with respect to observer,
            One way light time between target and observer.
    """
    trgpos = stypes.to_double_vector(trgpos)
    trgctr = stypes.string_to_char_p(trgctr)
    trgref = stypes.string_to_char_p(trgref)
    et = ctypes.c_double(et)
    outref = stypes.string_to_char_p(outref)
    refloc = stypes.string_to_char_p(refloc)
    abcorr = stypes.string_to_char_p(abcorr)
    obsrvr = stypes.string_to_char_p(obsrvr)
    state = stypes.empty_double_vector(6)
    lt = ctypes.c_double()
    libspice.spkcpt_c(
        trgpos,
        trgctr,
        trgref,
        et,
        outref,
        refloc,
        abcorr,
        obsrvr,
        state,
        ctypes.byref(lt),
    )
    return stypes.c_vector_to_python(state), lt.value


@spice_error_check
def spkcvo(
    target: str,
    et: float,
    outref: str,
    refloc: str,
    abcorr: str,
    obssta: Union[ndarray, Iterable[float]],
    obsepc: float,
    obsctr: str,
    obsref: str,
) -> Tuple[ndarray, float]:
    """
    Return the state of a specified target relative to an "observer,"
    where the observer has constant velocity in a specified reference
    frame.  The observer's state is provided by the calling program
    rather than by loaded SPK files.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkcvo_c.html

    :param target: Name of target ephemeris object.
    :param et: Observation epoch.
    :param outref: Reference frame of output state.
    :param refloc: Output reference frame evaluation locus.
    :param abcorr: Aberration correction.
    :param obssta: Observer state relative to center of motion.
    :param obsepc: Epoch of observer state.
    :param obsctr: Center of motion of observer.
    :param obsref: Frame of observer state.
    :return:
            State of target with respect to observer,
            One way light time between target and observer.
    """
    target = stypes.string_to_char_p(target)
    et = ctypes.c_double(et)
    outref = stypes.string_to_char_p(outref)
    refloc = stypes.string_to_char_p(refloc)
    abcorr = stypes.string_to_char_p(abcorr)
    obssta = stypes.to_double_vector(obssta)
    obsepc = ctypes.c_double(obsepc)
    obsctr = stypes.string_to_char_p(obsctr)
    obsref = stypes.string_to_char_p(obsref)
    state = stypes.empty_double_vector(6)
    lt = ctypes.c_double()
    libspice.spkcvo_c(
        target,
        et,
        outref,
        refloc,
        abcorr,
        obssta,
        obsepc,
        obsctr,
        obsref,
        state,
        ctypes.byref(lt),
    )
    return stypes.c_vector_to_python(state), lt.value


@spice_error_check
def spkcvt(
    trgsta: Union[ndarray, Iterable[float]],
    trgepc: float,
    trgctr: str,
    trgref: str,
    et: float,
    outref: str,
    refloc: str,
    abcorr: str,
    obsrvr: str,
) -> Tuple[ndarray, float]:
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
    :param et: Observation epoch.
    :param outref: Reference frame of output state.
    :param refloc: Output reference frame evaluation locus.
    :param abcorr: Aberration correction.
    :param obsrvr: Name of observing ephemeris object.
    :return:
            State of target with respect to observer,
            One way light time between target and observer.
    """
    trgpos = stypes.to_double_vector(trgsta)
    trgepc = ctypes.c_double(trgepc)
    trgctr = stypes.string_to_char_p(trgctr)
    trgref = stypes.string_to_char_p(trgref)
    et = ctypes.c_double(et)
    outref = stypes.string_to_char_p(outref)
    refloc = stypes.string_to_char_p(refloc)
    abcorr = stypes.string_to_char_p(abcorr)
    obsrvr = stypes.string_to_char_p(obsrvr)
    state = stypes.empty_double_vector(6)
    lt = ctypes.c_double()
    libspice.spkcvt_c(
        trgpos,
        trgepc,
        trgctr,
        trgref,
        et,
        outref,
        refloc,
        abcorr,
        obsrvr,
        state,
        ctypes.byref(lt),
    )
    return stypes.c_vector_to_python(state), lt.value


@spice_error_check
def spkez(
    targ: int, et: float, ref: str, abcorr: str, obs: int
) -> Tuple[ndarray, float]:
    """
    Return the state (position and velocity) of a target body
    relative to an observing body, optionally corrected for light
    time (planetary aberration) and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkez_c.html

    :param targ: Target body.
    :param et: Observer epoch.
    :param ref: Reference frame of output state vector.
    :param abcorr: Aberration correction flag.
    :param obs: Observing body.
    :return:
            State of target,
            One way light time between observer and target.
    """
    targ = ctypes.c_int(targ)
    et = ctypes.c_double(et)
    ref = stypes.string_to_char_p(ref)
    abcorr = stypes.string_to_char_p(abcorr)
    obs = ctypes.c_int(obs)
    starg = stypes.empty_double_vector(6)
    lt = ctypes.c_double()
    libspice.spkez_c(targ, et, ref, abcorr, obs, starg, ctypes.byref(lt))
    return stypes.c_vector_to_python(starg), lt.value


@spice_error_check
def spkezp(
    targ: int, et: float, ref: str, abcorr: str, obs: int
) -> Tuple[ndarray, float]:
    """
    Return the position of a target body relative to an observing
    body, optionally corrected for light time (planetary aberration)
    and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkezp_c.html

    :param targ: Target body NAIF ID code.
    :param et: Observer epoch.
    :param ref: Reference frame of output position vector.
    :param abcorr: Aberration correction flag.
    :param obs: Observing body NAIF ID code.
    :return:
            Position of target,
            One way light time between observer and target.
    """
    targ = ctypes.c_int(targ)
    et = ctypes.c_double(et)
    ref = stypes.string_to_char_p(ref)
    abcorr = stypes.string_to_char_p(abcorr)
    obs = ctypes.c_int(obs)
    ptarg = stypes.empty_double_vector(3)
    lt = ctypes.c_double()
    libspice.spkezp_c(targ, et, ref, abcorr, obs, ptarg, ctypes.byref(lt))
    return stypes.c_vector_to_python(ptarg), lt.value


@spice_error_check
def spkezr(
    targ: str, et: Union[ndarray, float], ref: str, abcorr: str, obs: str
) -> Union[Tuple[ndarray, float], Tuple[Iterable[ndarray], Iterable[float]]]:
    """
    Return the state (position and velocity) of a target body
    relative to an observing body, optionally corrected for light
    time (planetary aberration) and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkezr_c.html

    :param targ: Target body name.
    :param et: Observer epoch.
    :param ref: Reference frame of output state vector.
    :param abcorr: Aberration correction flag.
    :param obs: Observing body name.
    :return:
            State of target,
            One way light time between observer and target.
    """
    targ = stypes.string_to_char_p(targ)
    ref = stypes.string_to_char_p(ref)
    abcorr = stypes.string_to_char_p(abcorr)
    obs = stypes.string_to_char_p(obs)
    starg = stypes.empty_double_vector(6)
    lt = ctypes.c_double()
    if hasattr(et, "__iter__"):
        states = []
        times = []
        for t in et:
            libspice.spkezr_c(
                targ, ctypes.c_double(t), ref, abcorr, obs, starg, ctypes.byref(lt)
            )
            check_for_spice_error(None)
            states.append(stypes.c_vector_to_python(starg))
            times.append(lt.value)
        return states, times
    else:
        libspice.spkezr_c(
            targ, ctypes.c_double(et), ref, abcorr, obs, starg, ctypes.byref(lt)
        )
        return stypes.c_vector_to_python(starg), lt.value


@spice_error_check
def spkgeo(targ: int, et: float, ref: str, obs: int) -> Tuple[ndarray, float]:
    """
    Compute the geometric state (position and velocity) of a target
    body relative to an observing body.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkgeo_c.html

    :param targ: Target body.
    :param et: Target epoch.
    :param ref: Target reference frame.
    :param obs: Observing body.
    :return: State of target, Light time.
    """
    targ = ctypes.c_int(targ)
    et = ctypes.c_double(et)
    ref = stypes.string_to_char_p(ref)
    obs = ctypes.c_int(obs)
    state = stypes.empty_double_vector(6)
    lt = ctypes.c_double()
    libspice.spkgeo_c(targ, et, ref, obs, state, ctypes.byref(lt))
    return stypes.c_vector_to_python(state), lt.value


@spice_error_check
def spkgps(targ: int, et: float, ref: str, obs: int) -> Tuple[ndarray, float]:
    """
    Compute the geometric position of a target body relative to an
    observing body.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkgps_c.html

    :param targ: Target body.
    :param et: Target epoch.
    :param ref: Target reference frame.
    :param obs: Observing body.
    :return: Position of target, Light time.
    """
    targ = ctypes.c_int(targ)
    et = ctypes.c_double(et)
    ref = stypes.string_to_char_p(ref)
    obs = ctypes.c_int(obs)
    position = stypes.empty_double_vector(3)
    lt = ctypes.c_double()
    libspice.spkgps_c(targ, et, ref, obs, position, ctypes.byref(lt))
    return stypes.c_vector_to_python(position), lt.value


@spice_error_check
def spklef(filename: str) -> int:
    """
    Load an ephemeris file for use by the readers.  Return that file's
    handle, to be used by other SPK routines to refer to the file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spklef_c.html

    :param filename: Name of the file to be loaded.
    :return: Loaded file's handle.
    """
    filename = stypes.string_to_char_p(filename)
    handle = ctypes.c_int()
    libspice.spklef_c(filename, ctypes.byref(handle))
    return handle.value


@spice_error_check
def spkltc(
    targ: int, et: float, ref: str, abcorr: str, stobs: ndarray
) -> Tuple[ndarray, float, float]:
    """
    Return the state (position and velocity) of a target body
    relative to an observer, optionally corrected for light time,
    expressed relative to an inertial reference frame.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkltc_c.html

    :param targ: Target body.
    :param et: Observer epoch.
    :param ref: Inertial reference frame of output state.
    :param abcorr: Aberration correction flag.
    :param stobs: State of the observer relative to the SSB.
    :return:
            One way light time between observer and target,
            Derivative of light time with respect to time
    """
    assert len(stobs) == 6
    targ = stypes.c_int(targ)
    et = ctypes.c_double(et)
    ref = stypes.string_to_char_p(ref)
    abcorr = stypes.string_to_char_p(abcorr)
    stobs = stypes.to_double_vector(stobs)
    starg = stypes.empty_double_vector(6)
    lt = ctypes.c_double()
    dlt = ctypes.c_double()
    libspice.spkltc_c(
        targ, et, ref, abcorr, stobs, starg, ctypes.byref(lt), ctypes.byref(dlt)
    )
    return stypes.c_vector_to_python(starg), lt.value, dlt.value


@spice_error_check
def spkobj(spk: str, out_cell: Optional[SpiceCell] = None) -> SpiceCell:
    """
    Find the set of ID codes of all objects in a specified SPK file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkobj_c.html

    :param spk: Name of SPK file.
    :param out_cell: Optional Spice Int Cell.
    """
    spk = stypes.string_to_char_p(spk)
    if not out_cell:
        out_cell = stypes.SPICEINT_CELL(1000)
    assert isinstance(out_cell, stypes.SpiceCell)
    assert out_cell.dtype == 2
    libspice.spkobj_c(spk, ctypes.byref(out_cell))
    return out_cell


@spice_error_check
def spkopa(filename: str) -> int:
    """
    Open an existing SPK file for subsequent write.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkopa_c.html

    :param filename: The name of an existing SPK file.
    :return: A handle attached to the SPK file opened to append.
    """
    filename = stypes.string_to_char_p(filename)
    handle = ctypes.c_int()
    libspice.spkopa_c(filename, ctypes.byref(handle))
    return handle.value


@spice_error_check
def spkopn(filename: str, ifname: str, ncomch: int) -> int:
    """
    Create a new SPK file, returning the handle of the opened file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkopn_c.html

    :param filename: The name of the new SPK file to be created.
    :param ifname: The internal filename for the SPK file.
    :param ncomch: The number of characters to reserve for comments.
    :return: The handle of the opened SPK file.
    """
    filename = stypes.string_to_char_p(filename)
    ifname = stypes.string_to_char_p(ifname)
    ncomch = ctypes.c_int(ncomch)
    handle = ctypes.c_int()
    libspice.spkopn_c(filename, ifname, ncomch, ctypes.byref(handle))
    return handle.value


@spice_error_check
def spkpds(
    body: int, center: int, framestr: str, typenum: int, first: float, last: float
) -> ndarray:
    """
    Perform routine error checks and if all check pass, pack the
    descriptor for an SPK segment

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkpds_c.html

    :param body: The NAIF ID code for the body of the segment.
    :param center: The center of motion for body.
    :param framestr: The frame for this segment.
    :param typenum: The type of SPK segment to create.
    :param first: The first epoch for which the segment is valid.
    :param last: The last  epoch for which the segment is valid.
    :return: An SPK segment descriptor.
    """
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    framestr = stypes.string_to_char_p(framestr)
    typenum = ctypes.c_int(typenum)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    descr = stypes.empty_double_vector(5)
    libspice.spkpds_c(body, center, framestr, typenum, first, last, descr)
    return stypes.c_vector_to_python(descr)


@spice_error_check
def spkpos(
    targ: str, et: Union[float, ndarray], ref: str, abcorr: str, obs: str
) -> Union[Tuple[ndarray, float], Tuple[ndarray, ndarray]]:
    """
    Return the position of a target body relative to an observing
    body, optionally corrected for light time (planetary aberration)
    and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkpos_c.html

    :param targ: Target body name.
    :param et: Observer epoch.
    :param ref: Reference frame of output position vector.
    :param abcorr: Aberration correction flag.
    :param obs: Observing body name.
    :return:
            Position of target,
            One way light time between observer and target.
    """
    targ = stypes.string_to_char_p(targ)
    ref = stypes.string_to_char_p(ref)
    abcorr = stypes.string_to_char_p(abcorr)
    obs = stypes.string_to_char_p(obs)
    ptarg = stypes.empty_double_vector(3)
    lt = ctypes.c_double()
    if hasattr(et, "__iter__"):
        ptargs = []
        lts = []
        for t in et:
            libspice.spkpos_c(targ, t, ref, abcorr, obs, ptarg, ctypes.byref(lt))
            check_for_spice_error(None)
            ptargs.append(stypes.c_vector_to_python(ptarg))
            lts.append(lt.value)
        return numpy.array(ptargs), numpy.array(lts)
    else:
        libspice.spkpos_c(targ, et, ref, abcorr, obs, ptarg, ctypes.byref(lt))
        return stypes.c_vector_to_python(ptarg), lt.value


@spice_error_check
def spkpvn(handle: int, descr: ndarray, et: float) -> Tuple[int, ndarray, int]:
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
    handle = ctypes.c_int(handle)
    descr = stypes.to_double_vector(descr)
    et = ctypes.c_double(et)
    ref = ctypes.c_int()
    state = stypes.empty_double_vector(6)
    center = ctypes.c_int()
    libspice.spkpvn_c(handle, descr, et, ctypes.byref(ref), state, ctypes.byref(center))
    return ref.value, stypes.c_vector_to_python(state), center.value


@spice_error_check
@spice_found_exception_thrower
def spksfs(body: int, et: float, idlen: int) -> Tuple[int, ndarray, str, bool]:
    # spksfs has a Parameter SIDLEN,
    # sounds like an optional but is that possible?
    """
    Search through loaded SPK files to find the highest-priority segment
    applicable to the body and time specified.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spksfs_c.html

    :param body: Body ID.
    :param et: Ephemeris time.
    :param idlen: Length of output segment ID string.
    :return:
            Handle of file containing the applicable segment,
            Descriptor of the applicable segment,
            Identifier of the applicable segment.
    """
    body = ctypes.c_int(body)
    et = ctypes.c_double(et)
    idlen = ctypes.c_int(idlen)
    handle = ctypes.c_int()
    descr = stypes.empty_double_vector(5)
    identstring = stypes.string_to_char_p(idlen)
    found = ctypes.c_int()
    libspice.spksfs_c(
        body, et, idlen, ctypes.byref(handle), descr, identstring, ctypes.byref(found)
    )
    return (
        handle.value,
        stypes.c_vector_to_python(descr),
        stypes.to_python_string(identstring),
        bool(found.value),
    )


@spice_error_check
def spkssb(targ: int, et: float, ref: str) -> ndarray:
    """
    Return the state (position and velocity) of a target body
    relative to the solar system barycenter.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkssb_c.html

    :param targ: Target body.
    :param et: Target epoch.
    :param ref: Target reference frame.
    :return: State of target.
    """
    targ = ctypes.c_int(targ)
    et = ctypes.c_double(et)
    ref = stypes.string_to_char_p(ref)
    starg = stypes.empty_double_vector(6)
    libspice.spkssb_c(targ, et, ref, starg)
    return stypes.c_vector_to_python(starg)


@spice_error_check
def spksub(
    handle: int, descr: ndarray, identin: str, begin: float, end: float, newh: int
) -> None:
    """
    Extract a subset of the data in an SPK segment into a
    separate segment.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spksub_c.html

    :param handle: Handle of source segment.
    :param descr: Descriptor of source segment.
    :param identin: Indentifier of source segment.
    :param begin: Beginning (initial epoch) of subset.
    :param end: End (fincal epoch) of subset.
    :param newh: Handle of new segment.
    """
    assert len(descr) == 5
    handle = ctypes.c_int(handle)
    descr = stypes.to_double_vector(descr)
    identin = stypes.string_to_char_p(identin)
    begin = ctypes.c_double(begin)
    end = ctypes.c_double(end)
    newh = ctypes.c_int(newh)
    libspice.spksub_c(handle, descr, identin, begin, end, newh)


@spice_error_check
def spkuds(descr: ndarray) -> Tuple[int, int, int, int, float, float, int, int]:
    """
    Unpack the contents of an SPK segment descriptor.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkuds_c.html

    :param descr: An SPK segment descriptor.
    :return:
            The NAIF ID code for the body of the segment,
            The center of motion for body,
            The ID code for the frame of this segment,
            The type of SPK segment,
            The first epoch for which the segment is valid,
            The last  epoch for which the segment is valid,
            Beginning DAF address of the segment,
            Ending DAF address of the segment.
    """
    assert len(descr) == 5
    descr = stypes.to_double_vector(descr)
    body = ctypes.c_int()
    center = ctypes.c_int()
    framenum = ctypes.c_int()
    typenum = ctypes.c_int()
    first = ctypes.c_double()
    last = ctypes.c_double()
    begin = ctypes.c_int()
    end = ctypes.c_int()
    libspice.spkuds_c(
        descr,
        ctypes.byref(body),
        ctypes.byref(center),
        ctypes.byref(framenum),
        ctypes.byref(typenum),
        ctypes.byref(first),
        ctypes.byref(last),
        ctypes.byref(begin),
        ctypes.byref(end),
    )
    return (
        body.value,
        center.value,
        framenum.value,
        typenum.value,
        first.value,
        last.value,
        begin.value,
        end.value,
    )


@spice_error_check
def spkuef(handle: int) -> None:
    """
    Unload an ephemeris file so that it will no longer be searched by
    the readers.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkuef_c.html

    :param handle: Handle of file to be unloaded
    """
    handle = ctypes.c_int(handle)
    libspice.spkuef_c(handle)


@spice_error_check
def spkw02(
    handle: int,
    body: int,
    center: int,
    inframe: str,
    first: float,
    last: float,
    segid: str,
    intlen: float,
    n: int,
    polydg: int,
    cdata: Union[ndarray, Iterable[float]],
    btime: float,
) -> None:
    """
    Write a type 2 segment to an SPK file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkw02_c.html

    :param handle: Handle of an SPK file open for writing.
    :param body: Body code for ephemeris object.
    :param center: Body code for the center of motion of the body.
    :param inframe: The reference frame of the states.
    :param first: First valid time for which states can be computed.
    :param last: Last valid time for which states can be computed.
    :param segid: Segment identifier.
    :param intlen: Length of time covered by logical record.
    :param n: Number of coefficient sets.
    :param polydg: Chebyshev polynomial degree.
    :param cdata: Array of Chebyshev coefficients.
    :param btime: Begin time of first logical record.
    """
    handle = ctypes.c_int(handle)
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    inframe = stypes.string_to_char_p(inframe)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    segid = stypes.string_to_char_p(segid)
    intlen = ctypes.c_double(intlen)
    n = ctypes.c_int(n)
    polydg = ctypes.c_int(polydg)
    cdata = stypes.to_double_vector(cdata)
    btime = ctypes.c_double(btime)
    libspice.spkw02_c(
        handle,
        body,
        center,
        inframe,
        first,
        last,
        segid,
        intlen,
        n,
        polydg,
        cdata,
        btime,
    )


@spice_error_check
def spkw03(
    handle: int,
    body: int,
    center: int,
    inframe: str,
    first: float,
    last: float,
    segid: str,
    intlen: float,
    n: int,
    polydg: int,
    cdata: Union[ndarray, Iterable[float]],
    btime: float,
) -> None:
    """
    Write a type 3 segment to an SPK file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkw03_c.html

    :param handle: Handle of SPK file open for writing.
    :param body: NAIF code for ephemeris object.
    :param center: NAIF code for the center of motion of the body.
    :param inframe: Reference frame name.
    :param first: Start time of interval covered by segment.
    :param last: End time of interval covered by segment.
    :param segid: Segment identifier.
    :param intlen: Length of time covered by record.
    :param n: Number of records in segment.
    :param polydg: Chebyshev polynomial degree.
    :param cdata: Array of Chebyshev coefficients.
    :param btime: Begin time of first record.
    """
    handle = ctypes.c_int(handle)
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    inframe = stypes.string_to_char_p(inframe)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    segid = stypes.string_to_char_p(segid)
    intlen = ctypes.c_double(intlen)
    n = ctypes.c_int(n)
    polydg = ctypes.c_int(polydg)
    cdata = stypes.to_double_vector(cdata)
    btime = ctypes.c_double(btime)
    libspice.spkw03_c(
        handle,
        body,
        center,
        inframe,
        first,
        last,
        segid,
        intlen,
        n,
        polydg,
        cdata,
        btime,
    )


@spice_error_check
def spkw05(
    handle: int,
    body: int,
    center: int,
    inframe: str,
    first: float,
    last: float,
    segid: str,
    gm: float,
    n: int,
    states: Union[ndarray, Iterable[Iterable[float]]],
    epochs: Union[ndarray, Iterable[float]],
) -> None:
    # see libspice args for solution to array[][N] problem
    """
    Write an SPK segment of type 5 given a time-ordered set of
    discrete states and epochs, and the gravitational parameter
    of a central body.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkw05_c.html

    :param handle: Handle of an SPK file open for writing.
    :param body: Body code for ephemeris object.
    :param center: Body code for the center of motion of the body.
    :param inframe: The reference frame of the states.
    :param first: First valid time for which states can be computed.
    :param last: Last valid time for which states can be computed.
    :param segid: Segment identifier.
    :param gm: Gravitational parameter of central body.
    :param n: Number of states and epochs.
    :param states: States.
    :param epochs: Epochs.
    """
    handle = ctypes.c_int(handle)
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    inframe = stypes.string_to_char_p(inframe)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    segid = stypes.string_to_char_p(segid)
    gm = ctypes.c_double(gm)
    n = ctypes.c_int(n)
    states = stypes.to_double_matrix(states)
    epochs = stypes.to_double_vector(epochs)
    libspice.spkw05_c(
        handle, body, center, inframe, first, last, segid, gm, n, states, epochs
    )


@spice_error_check
def spkw08(
    handle: int,
    body: int,
    center: int,
    inframe: str,
    first: float,
    last: float,
    segid: str,
    degree: int,
    n: int,
    states: Union[ndarray, Iterable[Iterable[float]]],
    epoch1: float,
    step: float,
) -> None:
    # see libspice args for solution to array[][N] problem
    """
    Write a type 8 segment to an SPK file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkw08_c.html

    :param handle: Handle of an SPK file open for writing.
    :param body: NAIF code for an ephemeris object.
    :param center: NAIF code for center of motion of "body".
    :param inframe: Reference frame name.
    :param first: Start time of interval covered by segment.
    :param last: End time of interval covered by segment.
    :param segid: Segment identifier.
    :param degree: Degree of interpolating polynomials.
    :param n: Number of states.
    :param states: Array of states.
    :param epoch1: Epoch of first state in states array.
    :param step: Time step separating epochs of states.
    """
    handle = ctypes.c_int(handle)
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    inframe = stypes.string_to_char_p(inframe)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    segid = stypes.string_to_char_p(segid)
    degree = ctypes.c_int(degree)
    n = ctypes.c_int(n)
    states = stypes.to_double_matrix(states)  # X by 6 array
    epoch1 = ctypes.c_double(epoch1)
    step = ctypes.c_double(step)
    libspice.spkw08_c(
        handle,
        body,
        center,
        inframe,
        first,
        last,
        segid,
        degree,
        n,
        states,
        epoch1,
        step,
    )


@spice_error_check
def spkw09(
    handle: int,
    body: int,
    center: int,
    inframe: str,
    first: float,
    last: float,
    segid: str,
    degree: int,
    n: int,
    states: Union[ndarray, Iterable[Iterable[float]]],
    epochs: Union[ndarray, Iterable[float]],
) -> None:
    """
    Write a type 9 segment to an SPK file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkw09_c.html

    :param handle: Handle of an SPK file open for writing.
    :param body: NAIF code for an ephemeris object.
    :param center: NAIF code for center of motion of "body".
    :param inframe: Reference frame name.
    :param first: Start time of interval covered by segment.
    :param last: End time of interval covered by segment.
    :param segid: Segment identifier.
    :param degree: Degree of interpolating polynomials.
    :param n: Number of states.
    :param states: Array of states.
    :param epochs: Array of epochs corresponding to states.
    """
    handle = ctypes.c_int(handle)
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    inframe = stypes.string_to_char_p(inframe)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    segid = stypes.string_to_char_p(segid)
    degree = ctypes.c_int(degree)
    n = ctypes.c_int(n)
    states = stypes.to_double_matrix(states)  # X by 6 array
    epochs = stypes.to_double_vector(epochs)
    libspice.spkw09_c(
        handle, body, center, inframe, first, last, segid, degree, n, states, epochs
    )


@spice_error_check
def spkw10(
    handle: int,
    body: int,
    center: int,
    inframe: str,
    first: float,
    last: float,
    segid: str,
    consts: Union[ndarray, Iterable[float]],
    n: int,
    elems: Union[ndarray, Iterable[float]],
    epochs: Union[ndarray, Iterable[float]],
) -> None:
    """
    Write an SPK type 10 segment to the DAF open and attached to
    the input handle.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkw10_c.html

    :param handle: The handle of a DAF file open for writing.
    :param body: The NAIF ID code for the body of the segment.
    :param center: The center of motion for body.
    :param inframe: The reference frame for this segment.
    :param first: The first epoch for which the segment is valid.
    :param last: The last  epoch for which the segment is valid.
    :param segid: The string to use for segment identifier.
    :param consts: The array of geophysical constants for the segment.
    :param n: The number of element/epoch pairs to be stored.
    :param elems: The collection of "two-line" element sets.
    :param epochs: The epochs associated with the element sets.
    """
    handle = ctypes.c_int(handle)
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    inframe = stypes.string_to_char_p(inframe)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    segid = stypes.string_to_char_p(segid)
    consts = stypes.to_double_vector(consts)
    n = ctypes.c_int(n)
    elems = stypes.to_double_vector(elems)
    epochs = stypes.to_double_vector(epochs)
    libspice.spkw10_c(
        handle, body, center, inframe, first, last, segid, consts, n, elems, epochs
    )


@spice_error_check
def spkw12(
    handle: int,
    body: int,
    center: int,
    inframe: str,
    first: float,
    last: float,
    segid: str,
    degree: int,
    n: int,
    states: Union[ndarray, Iterable[Iterable[float]]],
    epoch0: float,
    step: float,
) -> None:
    """
    Write a type 12 segment to an SPK file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkw12_c.html

    :param handle: Handle of an SPK file open for writing.
    :param body: NAIF code for an ephemeris object.
    :param center: NAIF code for center of motion of body.
    :param inframe: Reference frame name.
    :param first: Start time of interval covered by segment.
    :param last: End time of interval covered by segment.
    :param segid: Segment identifier.
    :param degree: Degree of interpolating polynomials.
    :param n: Number of states.
    :param states: Array of states.
    :param epoch0: Epoch of first state in states array.
    :param step: Time step separating epochs of states.
    """
    handle = ctypes.c_int(handle)
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    inframe = stypes.string_to_char_p(inframe)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    segid = stypes.string_to_char_p(segid)
    degree = ctypes.c_int(degree)
    n = ctypes.c_int(n)
    states = stypes.to_double_matrix(states)  # X by 6 array
    epoch0 = ctypes.c_double(epoch0)
    step = ctypes.c_double(step)
    libspice.spkw12_c(
        handle,
        body,
        center,
        inframe,
        first,
        last,
        segid,
        degree,
        n,
        states,
        epoch0,
        step,
    )


@spice_error_check
def spkw13(
    handle: int,
    body: int,
    center: int,
    inframe: str,
    first: float,
    last: float,
    segid: str,
    degree: int,
    n: int,
    states: Union[ndarray, Iterable[Iterable[float]]],
    epochs: Union[ndarray, Iterable[float]],
) -> None:
    """
    Write a type 13 segment to an SPK file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkw13_c.html

    :param handle: Handle of an SPK file open for writing.
    :param body: NAIF code for an ephemeris object.
    :param center: NAIF code for center of motion of body.
    :param inframe: Reference frame name.
    :param first: Start time of interval covered by segment.
    :param last: End time of interval covered by segment.
    :param segid: Segment identifier.
    :param degree: Degree of interpolating polynomials.
    :param n: Number of states.
    :param states: Array of states.
    :param epochs: Array of epochs corresponding to states.
    """
    handle = ctypes.c_int(handle)
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    inframe = stypes.string_to_char_p(inframe)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    segid = stypes.string_to_char_p(segid)
    degree = ctypes.c_int(degree)
    n = ctypes.c_int(n)
    states = stypes.to_double_matrix(states)  # X by 6 array
    epochs = stypes.to_double_vector(epochs)
    libspice.spkw13_c(
        handle, body, center, inframe, first, last, segid, degree, n, states, epochs
    )


@spice_error_check
def spkw15(
    handle: int,
    body: int,
    center: int,
    inframe: str,
    first: float,
    last: float,
    segid: str,
    epoch: float,
    tp: ndarray,
    pa: ndarray,
    p: float,
    ecc: float,
    j2flg: float,
    pv: Union[ndarray, Iterable[float]],
    gm: float,
    j2: float,
    radius: float,
) -> None:
    """
    Write an SPK segment of type 15 given a type 15 data record.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkw15_c.html

    :param handle: Handle of an SPK file open for writing.
    :param body: Body code for ephemeris object.
    :param center: Body code for the center of motion of the body.
    :param inframe: The reference frame of the states.
    :param first: First valid time for which states can be computed.
    :param last: Last valid time for which states can be computed.
    :param segid: Segment identifier.
    :param epoch: Epoch of the periapse.
    :param tp: Trajectory pole vector.
    :param pa: Periapsis vector.
    :param p: Semi-latus rectum.
    :param ecc: Eccentricity.
    :param j2flg: J2 processing flag.
    :param pv: Central body pole vector.
    :param gm: Central body GM.
    :param j2: Central body J2.
    :param radius: Equatorial radius of central body.
    """
    handle = ctypes.c_int(handle)
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    inframe = stypes.string_to_char_p(inframe)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    segid = stypes.string_to_char_p(segid)
    epoch = ctypes.c_double(epoch)
    tp = stypes.to_double_vector(tp)
    pa = stypes.to_double_vector(pa)
    p = ctypes.c_double(p)
    ecc = ctypes.c_double(ecc)
    j2flg = ctypes.c_double(j2flg)
    pv = stypes.to_double_vector(pv)
    gm = ctypes.c_double(gm)
    j2 = ctypes.c_double(j2)
    radius = ctypes.c_double(radius)
    libspice.spkw15_c(
        handle,
        body,
        center,
        inframe,
        first,
        last,
        segid,
        epoch,
        tp,
        pa,
        p,
        ecc,
        j2flg,
        pv,
        gm,
        j2,
        radius,
    )


@spice_error_check
def spkw17(
    handle: int,
    body: int,
    center: int,
    inframe: str,
    first: float,
    last: float,
    segid: str,
    epoch: float,
    eqel: Iterable[Union[float, float]],
    rapol: float,
    decpol: float,
) -> None:
    """
    Write an SPK segment of type 17 given a type 17 data record.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkw17_c.html

    :param handle: Handle of an SPK file open for writing.
    :param body: Body code for ephemeris object.
    :param center: Body code for the center of motion of the body.
    :param inframe: The reference frame of the states.
    :param first: First valid time for which states can be computed.
    :param last: Last valid time for which states can be computed.
    :param segid: Segment identifier.
    :param epoch: Epoch of elements in seconds past J2000.
    :param eqel: Array of equinoctial elements.
    :param rapol: Right Ascension of the pole of the reference plane.
    :param decpol: Declination of the pole of the reference plane.
    """
    handle = ctypes.c_int(handle)
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    inframe = stypes.string_to_char_p(inframe)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    segid = stypes.string_to_char_p(segid)
    epoch = ctypes.c_double(epoch)
    eqel = stypes.to_double_vector(eqel)
    rapol = ctypes.c_double(rapol)
    decpol = ctypes.c_double(decpol)
    libspice.spkw17_c(
        handle, body, center, inframe, first, last, segid, epoch, eqel, rapol, decpol
    )


@spice_error_check
def spkw18(
    handle: int,
    subtyp: int,
    body: int,
    center: int,
    inframe: str,
    first: float,
    last: float,
    segid: str,
    degree: int,
    packts: Sequence[Iterable[float]],
    epochs: Sequence[float],
) -> None:
    """
    Write a type 18 segment to an SPK file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkw18_c.html

    :param handle: Handle of an SPK file open for writing.
    :param subtyp: SPK type 18 subtype code.
    :param body: Body code for ephemeris object.
    :param center: Body code for the center of motion of the body.
    :param inframe: The reference frame of the states.
    :param first: First valid time for which states can be computed.
    :param last: Last valid time for which states can be computed.
    :param segid: Segment identifier.
    :param degree:  Degree of interpolating polynomials.
    :param packts: data packets
    :param epochs: Array of epochs corresponding to states.
    """
    handle = ctypes.c_int(handle)
    subtyp = ctypes.c_int(subtyp)
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    inframe = stypes.string_to_char_p(inframe)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    segid = stypes.string_to_char_p(segid)
    degree = ctypes.c_int(degree)
    n = ctypes.c_int(len(packts))
    packts = stypes.to_double_matrix(packts)
    epochs = stypes.to_double_vector(epochs)
    libspice.spkw18_c(
        handle,
        subtyp,
        body,
        center,
        inframe,
        first,
        last,
        segid,
        degree,
        n,
        packts,
        epochs,
    )


@spice_error_check
def spkw20(
    handle: int,
    body: int,
    center: int,
    inframe: str,
    first: float,
    last: float,
    segid: str,
    intlen: float,
    n: int,
    polydg: int,
    cdata: ndarray,
    dscale: float,
    tscale: float,
    initjd: float,
    initfr: float,
) -> None:
    """
    Write a type 20 segment to an SPK file.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkw20_c.html

    :param handle: Handle of an SPK file open for writing.
    :param body: Body code for ephemeris object.
    :param center: Body code for the center of motion of the body.
    :param inframe: The reference frame of the states.
    :param first: First valid time for which states can be computed.
    :param last: Last valid time for which states can be computed.
    :param segid: Segment identifier.
    :param intlen: Length of time covered by logical record (days).
    :param n: Number of logical records in segment.
    :param polydg: Chebyshev polynomial degree.
    :param cdata: Array of Chebyshev coefficients and positions.
    :param dscale: Distance scale of data.
    :param tscale: Time scale of data.
    :param initjd: Integer part of begin time (TDB Julian date) of first record.
    :param initfr: Fractional part of begin time (TDB Julian date) of first record.
    """
    handle = ctypes.c_int(handle)
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    inframe = stypes.string_to_char_p(inframe)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    segid = stypes.string_to_char_p(segid)
    intlen = ctypes.c_double(intlen)
    n = ctypes.c_int(n)
    polydg = ctypes.c_int(polydg)
    cdata = stypes.to_double_vector(cdata)
    dscale = ctypes.c_double(dscale)
    tscale = ctypes.c_double(tscale)
    initjd = ctypes.c_double(initjd)
    initfr = ctypes.c_double(initfr)
    libspice.spkw20_c(
        handle,
        body,
        center,
        inframe,
        first,
        last,
        segid,
        intlen,
        n,
        polydg,
        cdata,
        dscale,
        tscale,
        initjd,
        initfr,
    )


@spice_error_check
@spice_found_exception_thrower
def srfc2s(code: int, bodyid: int, srflen: int = _default_len_out) -> Tuple[str, bool]:
    """
    Translate a surface ID code, together with a body ID code, to the
    corresponding surface name. If no such name exists, return a
    string representation of the surface ID code.

    note: from NAIF if isname is false, this case is not treated as an error.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfc2s_c.html

    :param code: Integer surface ID code to translate to a string.
    :param bodyid: ID code of body associated with surface.
    :param srflen: Available space in output string.
    :param srflen: int
    :return: String corresponding to surface ID code.
    """
    code = ctypes.c_int(code)
    bodyid = ctypes.c_int(bodyid)
    srfstr = stypes.string_to_char_p(srflen)
    srflen = ctypes.c_int(srflen)
    isname = ctypes.c_int()
    libspice.srfc2s_c(code, bodyid, srflen, srfstr, ctypes.byref(isname))
    return stypes.to_python_string(srfstr), bool(isname.value)


@spice_error_check
@spice_found_exception_thrower
def srfcss(code: int, bodstr: str, srflen: int = _default_len_out) -> Tuple[str, bool]:
    """
    Translate a surface ID code, together with a body string, to the
    corresponding surface name. If no such surface name exists,
    return a string representation of the surface ID code.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfcss_c.html

    :param code: Integer surface ID code to translate to a string.
    :param bodstr: Name or ID of body associated with surface.
    :param srflen: Available space in output string.
    :param srflen: int
    :return: String corresponding to surface ID code.
    """
    code = ctypes.c_int(code)
    bodstr = stypes.string_to_char_p(bodstr)
    srfstr = stypes.string_to_char_p(srflen)
    srflen = ctypes.c_int(srflen)
    isname = ctypes.c_int()
    libspice.srfcss_c(code, bodstr, srflen, srfstr, ctypes.byref(isname))
    return stypes.to_python_string(srfstr), bool(isname.value)


@spice_error_check
def srfnrm(
    method: str, target: str, et: float, fixref: str, srfpts: ndarray
) -> ndarray:
    """
    Map array of surface points on a specified target body to
    the corresponding unit length outward surface normal vectors.

    The surface of the target body may be represented by a triaxial
    ellipsoid or by topographic data provided by DSK files.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfnrm_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param et: Epoch in TDB seconds past J2000 TDB.
    :param fixref: Body-fixed, body-centered target body frame.
    :param srfpts: Array of surface points.
    :return: Array of outward, unit length normal vectors.
    """
    method = stypes.string_to_char_p(method)
    target = stypes.string_to_char_p(target)
    et = ctypes.c_double(et)
    fixref = stypes.string_to_char_p(fixref)
    npts = ctypes.c_int(len(srfpts))
    srfpts = stypes.to_double_matrix(srfpts)
    normls = stypes.empty_double_matrix(3, npts.value)
    libspice.srfnrm_c(method, target, et, fixref, npts, srfpts, normls)
    return stypes.c_matrix_to_numpy(normls)


@spice_error_check
def srfrec(body: int, longitude: float, latitude: float) -> ndarray:
    """
    Convert planetocentric latitude and longitude of a surface
    point on a specified body to rectangular coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfrec_c.html

    :param body: NAIF integer code of an extended body.
    :param longitude: Longitude of point in radians.
    :param latitude: Latitude of point in radians.
    :return: Rectangular coordinates of the point.
    """
    body = ctypes.c_int(body)
    longitude = ctypes.c_double(longitude)
    latitude = ctypes.c_double(latitude)
    rectan = stypes.empty_double_vector(3)
    libspice.srfrec_c(body, longitude, latitude, rectan)
    return stypes.c_vector_to_python(rectan)


@spice_error_check
@spice_found_exception_thrower
def srfs2c(srfstr: str, bodstr: str) -> Tuple[int, bool]:
    """
    Translate a surface string, together with a body string, to the
    corresponding surface ID code. The input strings may contain
    names or integer ID codes.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfs2c_c.html

    :param srfstr: Surface name or ID string.
    :param bodstr: Body name or ID string.
    :return: Integer surface ID code.
    """
    srfstr = stypes.string_to_char_p(srfstr)
    bodstr = stypes.string_to_char_p(bodstr)
    code = ctypes.c_int()
    isname = ctypes.c_int()
    libspice.srfs2c_c(srfstr, bodstr, ctypes.byref(code), ctypes.byref(isname))
    return code.value, bool(isname.value)


@spice_error_check
@spice_found_exception_thrower
def srfscc(srfstr: str, bodyid: int) -> Tuple[int, bool]:
    """
    Translate a surface string, together with a body ID code, to the
    corresponding surface ID code. The input surface string may
    contain a name or an integer ID code.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfscc_c.html

    :param srfstr: Surface name or ID string.
    :param bodyid: ID code of body associated with surface.
    :return: Integer surface ID code.
    """
    srfstr = stypes.string_to_char_p(srfstr)
    bodyid = ctypes.c_int(bodyid)
    code = ctypes.c_int()
    isname = ctypes.c_int()
    libspice.srfscc_c(srfstr, bodyid, ctypes.byref(code), ctypes.byref(isname))
    return code.value, bool(isname.value)


@spice_error_check
@spice_found_exception_thrower
def srfxpt(
    method: str,
    target: str,
    et: Union[float, Iterable[float]],
    abcorr: str,
    obsrvr: str,
    dref: str,
    dvec: ndarray,
) -> Union[
    Tuple[ndarray, float, float, ndarray, bool],
    Tuple[ndarray, ndarray, ndarray, ndarray, ndarray],
]:
    """
    Deprecated: This routine has been superseded by the CSPICE
    routine :func:`sincpt`. This routine is supported for purposes of
    backward compatibility only.

    Given an observer and a direction vector defining a ray, compute the
    surface intercept point of the ray on a target body at a specified
    epoch, optionally corrected for light time and stellar aberration.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfxpt_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param et: Epoch in ephemeris seconds past J2000 TDB.
    :param abcorr: Aberration correction.
    :param obsrvr: Name of observing body.
    :param dref: Reference frame of input direction vector.
    :param dvec: Ray's direction vector.
    :return:
            Surface intercept point on the target body,
            Distance from the observer to the intercept point,
            Intercept epoch,
            Observer position relative to target center.
    """
    method = stypes.string_to_char_p(method)
    target = stypes.string_to_char_p(target)
    abcorr = stypes.string_to_char_p(abcorr)
    obsrvr = stypes.string_to_char_p(obsrvr)
    dref = stypes.string_to_char_p(dref)
    dvec = stypes.to_double_vector(dvec)
    spoint = stypes.empty_double_vector(3)
    trgepc = ctypes.c_double()
    dist = ctypes.c_double()
    obspos = stypes.empty_double_vector(3)
    found = ctypes.c_int()
    if hasattr(et, "__iter__"):
        spoints = []
        dists = []
        trgepcs = []
        obsposs = []
        founds = []
        for t in et:
            libspice.srfxpt_c(
                method,
                target,
                t,
                abcorr,
                obsrvr,
                dref,
                dvec,
                spoint,
                ctypes.byref(dist),
                ctypes.byref(trgepc),
                obspos,
                ctypes.byref(found),
            )
            check_for_spice_error(None)
            spoints.append(stypes.c_vector_to_python(spoint))
            dists.append(dist.value)
            trgepcs.append(trgepc.value)
            obsposs.append(stypes.c_vector_to_python(obspos))
            founds.append(bool(found.value))
        return (
            numpy.array(spoints),
            numpy.array(dists),
            numpy.array(trgepcs),
            numpy.array(obsposs),
            numpy.array(founds),
        )
    else:
        et = ctypes.c_double(et)
        libspice.srfxpt_c(
            method,
            target,
            et,
            abcorr,
            obsrvr,
            dref,
            dvec,
            spoint,
            ctypes.byref(dist),
            ctypes.byref(trgepc),
            obspos,
            ctypes.byref(found),
        )
        return (
            stypes.c_vector_to_python(spoint),
            dist.value,
            trgepc.value,
            stypes.c_vector_to_python(obspos),
            bool(found.value),
        )


@spice_error_check
def ssize(newsize: int, cell: SpiceCell) -> SpiceCell:
    """
    Set the size (maximum cardinality) of a CSPICE cell of any data type.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ssize_c.html

    :param newsize: Size (maximum cardinality) of the cell.
    :param cell: The cell.
    :return: The updated cell.
    """
    assert isinstance(cell, stypes.SpiceCell)
    newsize = ctypes.c_int(newsize)
    libspice.ssize_c(newsize, ctypes.byref(cell))
    return cell


@spice_error_check
def stelab(pobj: ndarray, vobs: ndarray) -> ndarray:
    """
    Correct the apparent position of an object for stellar
    aberration.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/stelab_c.html

    :param pobj: Position of an object with respect to the observer.
    :param vobs:
                Velocity of the observer with respect
                to the Solar System barycenter.
    :return:
            Apparent position of the object with respect to
            the observer, corrected for stellar aberration.
    """
    pobj = stypes.to_double_vector(pobj)
    vobs = stypes.to_double_vector(vobs)
    appobj = stypes.empty_double_vector(3)
    libspice.stelab_c(pobj, vobs, appobj)
    return stypes.c_vector_to_python(appobj)


@spice_error_check
def stlabx(pobj: ndarray, vobs: ndarray) -> ndarray:
    """
    Correct the position of a target for the stellar aberration
    effect on radiation transmitted from a specified observer to
    the target.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/stlabx_c.html

    :param pobj: Position of an object with respect to the observer.
    :param vobs:
                Velocity of the observer with respect
                to the Solar System barycenter.
    :return: Corrected position of the object.
    """
    _pobj = stypes.to_double_vector(pobj)
    _vobs = stypes.to_double_vector(vobs)
    _corpos = stypes.empty_double_vector(3)
    libspice.stlabx_c(_pobj, _vobs, _corpos)
    return stypes.c_vector_to_python(_corpos)


@spice_error_check
@spice_found_exception_thrower
def stpool(
    item: str, nth: int, contin: str, lenout: int = _default_len_out
) -> Tuple[str, int, bool]:
    """
    Retrieve the nth string from the kernel pool variable, where the
    string may be continued across several components of the kernel pool
    variable.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/stpool_c.html

    :param item: Name of the kernel pool variable.
    :param nth: Index of the full string to retrieve.
    :param contin: Character sequence used to indicate continuation.
    :param lenout: Available space in output string.
    :return:
            A full string concatenated across continuations,
            The number of characters in the full string value.
    """
    item = stypes.string_to_char_p(item)
    contin = stypes.string_to_char_p(contin)
    nth = ctypes.c_int(nth)
    strout = stypes.string_to_char_p(lenout)
    lenout = ctypes.c_int(lenout)
    found = ctypes.c_int()
    sizet = ctypes.c_int()
    libspice.stpool_c(
        item, nth, contin, lenout, strout, ctypes.byref(sizet), ctypes.byref(found)
    )
    return stypes.to_python_string(strout), sizet.value, bool(found.value)


@spice_error_check
def str2et(time: Union[str, Iterable[str]]) -> Union[float, ndarray]:
    """
    Convert a string representing an epoch to a double precision
    value representing the number of TDB seconds past the J2000
    epoch corresponding to the input epoch.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/str2et_c.html

    :param time: A string representing an epoch.
    :return: The equivalent value in seconds past J2000, TDB.
    """
    et = ctypes.c_double()
    if stypes.is_iterable(time):
        ets = []
        for t in time:
            libspice.str2et_c(stypes.string_to_char_p(t), ctypes.byref(et))
            check_for_spice_error(None)
            ets.append(et.value)
        return numpy.array(ets)
    else:
        time = stypes.string_to_char_p(time)
        libspice.str2et_c(time, ctypes.byref(et))
        return et.value


@spice_error_check
def datetime2et(dt: Union[Iterable[datetime], datetime]) -> Union[ndarray, float]:
    """
    Converts a standard Python datetime to a double precision value
    representing the number of TDB seconds past the J2000 epoch
    corresponding to the input epoch.

    Timezone-naive datetimes will be assumed to be UTC, timezone-aware
    datetimes will be handled correctly by converting to UTC before
    passing them to CSPICE.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/time.html#The%20J2000%20Epoch

    :param dt: A standard Python datetime
    :return: The equivalent value in seconds past J2000, TDB.
    """
    lt = ctypes.c_double()
    if hasattr(dt, "__iter__"):
        ets = []
        for t in dt:
            if t.tzinfo is not None and t.tzinfo.utcoffset(t) is not None:
                t = t.astimezone(timezone.utc).replace(tzinfo=None)
            libspice.utc2et_c(stypes.string_to_char_p(t.isoformat()), ctypes.byref(lt))
            check_for_spice_error(None)
            ets.append(lt.value)
        return numpy.array(ets)
    else:
        if dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None:
            dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
        dt = stypes.string_to_char_p(dt.isoformat())
        et = ctypes.c_double()
        libspice.utc2et_c(dt, ctypes.byref(et))
        return et.value


if hasattr(datetime, "fromisoformat"):

    def fromisoformat(s):
        return datetime.fromisoformat(s + "+00:00")


else:

    def fromisoformat(s):
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=timezone.utc)


@spice_error_check
def et2datetime(et: Union[Iterable[float], float]) -> Union[ndarray, datetime]:
    """
    Convert an input time from ephemeris seconds past J2000 to
    a standard Python datetime.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/time.html#The%20J2000%20Epoch

    :param et: Input epoch, given in ephemeris seconds past J2000.
    :return: Output datetime object in UTC
    """
    result = et2utc(et, "ISOC", 6)
    if stypes.is_iterable(result):
        return numpy.array([fromisoformat(s) for s in result])
    else:
        return fromisoformat(result)


@spice_error_check
def subpnt(
    method: str, target: str, et: float, fixref: str, abcorr: str, obsrvr: str
) -> Tuple[ndarray, float, ndarray]:
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
    method = stypes.string_to_char_p(method)
    target = stypes.string_to_char_p(target)
    et = ctypes.c_double(et)
    fixref = stypes.string_to_char_p(fixref)
    abcorr = stypes.string_to_char_p(abcorr)
    obsrvr = stypes.string_to_char_p(obsrvr)
    spoint = stypes.empty_double_vector(3)
    trgepc = ctypes.c_double(0)
    srfvec = stypes.empty_double_vector(3)
    libspice.subpnt_c(
        method, target, et, fixref, abcorr, obsrvr, spoint, ctypes.byref(trgepc), srfvec
    )
    return (
        stypes.c_vector_to_python(spoint),
        trgepc.value,
        stypes.c_vector_to_python(srfvec),
    )


@spice_error_check
def subpt(
    method: str,
    target: str,
    et: Union[float, Iterable[float]],
    abcorr: str,
    obsrvr: str,
) -> Union[Tuple[ndarray, ndarray], Tuple[ndarray, float]]:
    """
    Deprecated: This routine has been superseded by the CSPICE
    routine :func:`subpnt`. This routine is supported for purposes of
    backward compatibility only.

    Compute the rectangular coordinates of the sub-observer point on
    a target body at a particular epoch, optionally corrected for
    planetary (light time) and stellar aberration.  Return these
    coordinates expressed in the body-fixed frame associated with the
    target body.  Also, return the observer's altitude above the
    target body.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/subpt_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param et: Epoch in ephemeris seconds past J2000 TDB.
    :param abcorr: Aberration correction.
    :param obsrvr: Name of observing body.
    :return:
            Sub-observer point on the target body,
            Altitude of the observer above the target body.
    """
    method = stypes.string_to_char_p(method)
    target = stypes.string_to_char_p(target)
    abcorr = stypes.string_to_char_p(abcorr)
    obsrvr = stypes.string_to_char_p(obsrvr)
    spoint = stypes.empty_double_vector(3)
    alt = ctypes.c_double()
    if hasattr(et, "__iter__"):
        points = []
        alts = []
        for t in et:
            libspice.subpt_c(
                method,
                target,
                ctypes.c_double(t),
                abcorr,
                obsrvr,
                spoint,
                ctypes.byref(alt),
            )
            check_for_spice_error(None)
            points.append(stypes.c_vector_to_python(spoint))
            alts.append(alt.value)
        return numpy.array(points), numpy.array(alts)
    else:
        et = ctypes.c_double(et)
        libspice.subpt_c(method, target, et, abcorr, obsrvr, spoint, ctypes.byref(alt))
        return stypes.c_vector_to_python(spoint), alt.value


@spice_error_check
def subslr(
    method: str, target: str, et: float, fixref: str, abcorr: str, obsrvr: str
) -> Tuple[ndarray, float, ndarray]:
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
            Sub-solar point on the target body,
            Sub-solar point epoch,
            Vector from observer to sub-solar point.
    """
    method = stypes.string_to_char_p(method)
    target = stypes.string_to_char_p(target)
    et = ctypes.c_double(et)
    fixref = stypes.string_to_char_p(fixref)
    abcorr = stypes.string_to_char_p(abcorr)
    obsrvr = stypes.string_to_char_p(obsrvr)
    spoint = stypes.empty_double_vector(3)
    trgepc = ctypes.c_double(0)
    srfvec = stypes.empty_double_vector(3)
    libspice.subslr_c(
        method, target, et, fixref, abcorr, obsrvr, spoint, ctypes.byref(trgepc), srfvec
    )
    return (
        stypes.c_vector_to_python(spoint),
        trgepc.value,
        stypes.c_vector_to_python(srfvec),
    )


@spice_error_check
def subsol(method: str, target: str, et: float, abcorr: str, obsrvr: str) -> ndarray:
    """
    Deprecated: This routine has been superseded by the CSPICE
    routine :func:`subslr`. This routine is supported for purposes of
    backward compatibility only.

    Determine the coordinates of the sub-solar point on a target
    body as seen by a specified observer at a specified epoch,
    optionally corrected for planetary (light time) and stellar
    aberration.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/subsol_c.html

    :param method: Computation method.
    :param target: Name of target body.
    :param et: Epoch in ephemeris seconds past J2000 TDB.
    :param abcorr: Aberration correction.
    :param obsrvr: Name of observing body.
    :return: Sub-solar point on the target body.
    """
    method = stypes.string_to_char_p(method)
    target = stypes.string_to_char_p(target)
    et = ctypes.c_double(et)
    abcorr = stypes.string_to_char_p(abcorr)
    obsrvr = stypes.string_to_char_p(obsrvr)
    spoint = stypes.empty_double_vector(3)
    libspice.subsol_c(method, target, et, abcorr, obsrvr, spoint)
    return stypes.c_vector_to_python(spoint)


@spice_error_check
def sumad(array: Sequence[float]) -> float:
    """
    Return the sum of the elements of a double precision array.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sumad_c.html

    :param array: Input Array.
    :return: The sum of the array.
    """
    n = ctypes.c_int(len(array))
    array = stypes.to_double_vector(array)
    return libspice.sumad_c(array, n)


@spice_error_check
def sumai(array: Sequence[int]) -> int:
    """
    Return the sum of the elements of an integer array.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sumai_c.html

    :param array: Input Array.
    :return: The sum of the array.
    """
    n = ctypes.c_int(len(array))
    array = stypes.to_int_vector(array)
    return libspice.sumai_c(array, n)


@spice_error_check
def surfnm(
    a: float, b: float, c: float, point: Union[ndarray, Iterable[float]]
) -> ndarray:
    """
    This routine computes the outward-pointing, unit normal vector
    from a point on the surface of an ellipsoid.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/surfnm_c.html

    :param a: Length of the ellisoid semi-axis along the x-axis.
    :param b: Length of the ellisoid semi-axis along the y-axis.
    :param c: Length of the ellisoid semi-axis along the z-axis.
    :param point: Body-fixed coordinates of a point on the ellipsoid'
    :return: Outward pointing unit normal to ellipsoid at point.
    """
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    point = stypes.to_double_vector(point)
    normal = stypes.empty_double_vector(3)
    libspice.surfnm_c(a, b, c, point, normal)
    return stypes.c_vector_to_python(normal)


@spice_error_check
@spice_found_exception_thrower
def surfpt(
    positn: Union[ndarray, Iterable[float]],
    u: Union[ndarray, Iterable[float]],
    a: Union[float, float],
    b: Union[float, float],
    c: Union[float, float],
) -> Tuple[ndarray, bool]:
    """
    Determine the intersection of a line-of-sight vector with the
    surface of an ellipsoid.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/surfpt_c.html

    :param positn: Position of the observer in body-fixed frame.
    :param u: Vector from the observer in some direction.
    :param a: Length of the ellisoid semi-axis along the x-axis.
    :param b: Length of the ellisoid semi-axis along the y-axis.
    :param c: Length of the ellisoid semi-axis along the z-axis.
    :return: Point on the ellipsoid pointed to by u.
    """
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    positn = stypes.to_double_vector(positn)
    u = stypes.to_double_vector(u)
    point = stypes.empty_double_vector(3)
    found = ctypes.c_int()
    libspice.surfpt_c(positn, u, a, b, c, point, ctypes.byref(found))
    return stypes.c_vector_to_python(point), bool(found.value)


@spice_error_check
@spice_found_exception_thrower
def surfpv(
    stvrtx: Union[ndarray, Iterable[float]],
    stdir: Union[ndarray, Iterable[float]],
    a: float,
    b: float,
    c: float,
) -> Tuple[ndarray, bool]:
    """
    Find the state (position and velocity) of the surface intercept
    defined by a specified ray, ray velocity, and ellipsoid.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/surfpv_c.html

    :param stvrtx: State of ray's vertex.
    :param stdir: State of ray's direction vector.
    :param a: Length of the ellisoid semi-axis along the x-axis.
    :param b: Length of the ellisoid semi-axis along the y-axis.
    :param c: Length of the ellisoid semi-axis along the z-axis.
    :return: State of surface intercept.
    """
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    stvrtx = stypes.to_double_vector(stvrtx)
    stdir = stypes.to_double_vector(stdir)
    stx = stypes.empty_double_vector(6)
    found = ctypes.c_int()
    libspice.surfpv_c(stvrtx, stdir, a, b, c, stx, ctypes.byref(found))
    return stypes.c_vector_to_python(stx), bool(found.value)


@spice_error_check
def swpool(agent: str, nnames: int, lenvals: int, names: Iterable[str]) -> None:
    """
    Add a name to the list of agents to notify whenever a member of
    a list of kernel variables is updated.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/swpool_c.html

    :param agent: The name of an agent to be notified after updates.
    :param nnames: The number of variables to associate with agent.
    :param lenvals: Length of strings in the names array.
    :param names: Variable names whose update causes the notice.
    """
    agent = stypes.string_to_char_p(agent)
    nnames = ctypes.c_int(nnames)
    lenvals = ctypes.c_int(lenvals)
    names = stypes.list_to_char_array(names)
    libspice.swpool_c(agent, nnames, lenvals, names)


@spice_error_check
def sxform(instring: str, tostring: str, et: Union[float, ndarray]) -> ndarray:
    """
    Return the state transformation matrix from one frame to
    another at a specified epoch.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sxform_c.html


    :param instring: Name of the frame to transform from.
    :param tostring: Name of the frame to transform to.
    :param et: Epoch of the state transformation matrix.
    :return: A state transformation matrix.
    """
    instring = stypes.string_to_char_p(instring)
    tostring = stypes.string_to_char_p(tostring)
    xform = stypes.empty_double_matrix(x=6, y=6)
    if hasattr(et, "__iter__"):
        xforms = []
        for t in et:
            libspice.sxform_c(instring, tostring, ctypes.c_double(t), xform)
            check_for_spice_error(None)
            xforms.append(stypes.c_matrix_to_numpy(xform))
        return numpy.array(xforms)
    else:
        et = ctypes.c_double(et)
        libspice.sxform_c(instring, tostring, et, xform)
        return stypes.c_matrix_to_numpy(xform)


@spice_error_check
@spice_found_exception_thrower
def szpool(name: str) -> Tuple[int, bool]:
    """
    Return the kernel pool size limitations.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/szpool_c.html

    :param name: Name of the parameter to be returned.
    :return: Value of parameter specified by name,
    """
    name = stypes.string_to_char_p(name)
    n = ctypes.c_int()
    found = ctypes.c_int(0)
    libspice.szpool_c(name, ctypes.byref(n), ctypes.byref(found))
    return n.value, bool(found.value)


################################################################################
# T


@spice_error_check
def tangpt(
    method: str,
    target: str,
    et: float,
    fixref: str,
    abcorr: str,
    corloc: str,
    obsrvr: str,
    dref: str,
    dvec: Union[ndarray, Iterable[float]],
) -> Tuple[ndarray, float, float, ndarray, float, ndarray]:
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
    _method = stypes.string_to_char_p(method)
    _target = stypes.string_to_char_p(target)
    _et = ctypes.c_double(et)
    _fixref = stypes.string_to_char_p(fixref)
    _abcorr = stypes.string_to_char_p(abcorr)
    _corloc = stypes.string_to_char_p(corloc)
    _obsrvr = stypes.string_to_char_p(obsrvr)
    _dref = stypes.string_to_char_p(dref)
    _dvec = stypes.to_double_vector(dvec)
    tanpt = stypes.empty_double_vector(3)
    alt = ctypes.c_double(0)
    _range = ctypes.c_double(0)
    srfpt = stypes.empty_double_vector(3)
    trgepc = ctypes.c_double(0)
    srfvec = stypes.empty_double_vector(3)
    libspice.tangpt_c(
        _method,
        _target,
        _et,
        _fixref,
        _abcorr,
        _corloc,
        _obsrvr,
        _dref,
        _dvec,
        tanpt,
        ctypes.byref(alt),
        ctypes.byref(_range),
        srfpt,
        ctypes.byref(trgepc),
        srfvec,
    )
    return (
        stypes.c_vector_to_python(tanpt),
        alt.value,
        _range.value,
        stypes.c_vector_to_python(srfpt),
        trgepc.value,
        stypes.c_vector_to_python(srfvec),
    )


@spice_error_check
def termpt(
    method: str,
    ilusrc: str,
    target: str,
    et: float,
    fixref: str,
    abcorr: str,
    corloc: str,
    obsrvr: str,
    refvec: Union[ndarray, Iterable[float]],
    rolstp: float,
    ncuts: int,
    schstp: float,
    soltol: float,
    maxn: int,
) -> Tuple[ndarray, ndarray, ndarray, ndarray]:
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

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/termpt_c.html

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
    :return: Counts of terminator points corresponding to cuts, Terminator points, Times associated with terminator points, Terminator vectors emanating from the observer
    """
    method = stypes.string_to_char_p(method)
    ilusrc = stypes.string_to_char_p(ilusrc)
    target = stypes.string_to_char_p(target)
    et = ctypes.c_double(et)
    fixref = stypes.string_to_char_p(fixref)
    abcorr = stypes.string_to_char_p(abcorr)
    corloc = stypes.string_to_char_p(corloc)
    obsrvr = stypes.string_to_char_p(obsrvr)
    refvec = stypes.to_double_vector(refvec)
    rolstp = ctypes.c_double(rolstp)
    ncuts = ctypes.c_int(ncuts)
    schstp = ctypes.c_double(schstp)
    soltol = ctypes.c_double(soltol)
    maxn = ctypes.c_int(maxn)
    npts = stypes.empty_int_vector(maxn.value)
    points = stypes.empty_double_matrix(3, maxn.value)
    epochs = stypes.empty_double_vector(maxn)
    trmvcs = stypes.empty_double_matrix(3, maxn.value)
    libspice.termpt_c(
        method,
        ilusrc,
        target,
        et,
        fixref,
        abcorr,
        corloc,
        obsrvr,
        refvec,
        rolstp,
        ncuts,
        schstp,
        soltol,
        maxn,
        npts,
        points,
        epochs,
        trmvcs,
    )
    # Clip the empty elements out of returned results
    npts = stypes.c_vector_to_python(npts)
    valid_points = numpy.where(npts >= 1)
    return (
        npts[valid_points],
        stypes.c_matrix_to_numpy(points)[valid_points],
        stypes.c_vector_to_python(epochs)[valid_points],
        stypes.c_matrix_to_numpy(trmvcs)[valid_points],
    )


@spice_error_check
def timdef(action: str, item: str, lenout: int, value: Optional[str] = None) -> str:
    """
    Set and retrieve the defaults associated with calendar input strings.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/timdef_c.html

    :param action: the kind of action to take "SET" or "GET".
    :param item: the default item of interest.
    :param lenout: the length of list for output.
    :param value: the optional string used if action is "SET"
    :return: the value associated with the default item.
    """
    action = stypes.string_to_char_p(action)
    item = stypes.string_to_char_p(item)
    lenout = ctypes.c_int(lenout)
    if value is None:
        value = stypes.string_to_char_p(lenout)
    else:
        value = stypes.string_to_char_p(value)
    libspice.timdef_c(action, item, lenout, value)
    return stypes.to_python_string(value)


@spice_error_check
def timout(
    et: Union[ndarray, float], pictur: str, lenout: int = _default_len_out
) -> Union[ndarray, str]:
    """
    This vectorized routine converts an input epoch represented in TDB seconds
    past the TDB epoch of J2000 to a character string formatted to
    the specifications of a user's format picture.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/timout_c.html

    :param et: An epoch in seconds past the ephemeris epoch J2000.
    :param pictur: A format specification for the output string.
    :param lenout: The length of the output string plus 1.
    :return: A string representation of the input epoch.
    """
    pictur = stypes.string_to_char_p(pictur)
    output = stypes.string_to_char_p(lenout)
    lenout = ctypes.c_int(lenout)
    if hasattr(et, "__iter__"):
        times = []
        for t in et:
            libspice.timout_c(ctypes.c_double(t), pictur, lenout, output)
            check_for_spice_error(None)
            times.append(stypes.to_python_string(output))
        return numpy.array(times)
    else:
        et = ctypes.c_double(et)
        libspice.timout_c(et, pictur, lenout, output)
        return stypes.to_python_string(output)


@spice_error_check
def tipbod(ref: str, body: int, et: float) -> ndarray:
    """
    Return a 3x3 matrix that transforms positions in inertial
    coordinates to positions in body-equator-and-prime-meridian
    coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tipbod_c.html

    :param ref: ID of inertial reference frame to transform from.
    :param body: ID code of body.
    :param et: Epoch of transformation.
    :return: Transformation (position), inertial to prime meridian.
    """
    ref = stypes.string_to_char_p(ref)
    body = ctypes.c_int(body)
    et = ctypes.c_double(et)
    retmatrix = stypes.empty_double_matrix()
    libspice.tipbod_c(ref, body, et, retmatrix)
    return stypes.c_matrix_to_numpy(retmatrix)


@spice_error_check
def tisbod(ref: str, body: int, et: float) -> ndarray:
    """
    Return a 6x6 matrix that transforms states in inertial coordinates to
    states in body-equator-and-prime-meridian coordinates.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tisbod_c.html

    :param ref: ID of inertial reference frame to transform from.
    :param body: ID code of body.
    :param et: Epoch of transformation.
    :return: Transformation (state), inertial to prime meridian.
    """
    ref = stypes.string_to_char_p(ref)
    body = ctypes.c_int(body)
    et = ctypes.c_double(et)
    retmatrix = stypes.empty_double_matrix(x=6, y=6)
    libspice.tisbod_c(ref, body, et, retmatrix)
    return stypes.c_matrix_to_numpy(retmatrix)


@spice_error_check
@spice_found_exception_thrower
def tkfram(typid: int) -> Tuple[ndarray, int, bool]:
    """
    This routine returns the rotation from the input frame
    specified by ID to the associated frame given by FRAME.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/FORTRAN/spicelib/tkfram.html

    :param typid: Class identification code for the instrument
    :return: Rotation matrix from the input frame to the returned reference frame, id for the reference frame
    """
    code = ctypes.c_int(typid)
    matrix = stypes.empty_double_matrix(x=3, y=3)
    next_frame = ctypes.c_int()
    found = ctypes.c_int()
    libspice.tkfram_(
        ctypes.byref(code), matrix, ctypes.byref(next_frame), ctypes.byref(found)
    )
    return stypes.c_matrix_to_numpy(matrix), next_frame.value, bool(found.value)


# @spice_error_check
def tkvrsn(item: str) -> str:
    """
    Given an item such as the Toolkit or an entry point name, return
    the latest version string.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tkvrsn_c.html

    :param item: Item for which a version string is desired.
    :return: the latest version string.
    """
    item = stypes.string_to_char_p(item)
    return stypes.to_python_string(libspice.tkvrsn_c(item))


@spice_error_check
def tparch(type: str) -> None:
    """
    Restrict the set of strings that are recognized by SPICE time
    parsing routines to those that have standard values for all time
    components.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tparch_c.html

    :param type: String: Use "YES" to restrict time inputs.
    """
    _type = stypes.string_to_char_p(type)
    libspice.tparch_c(_type)


@spice_error_check
def tparse(instring: str, lenout: int = _default_len_out) -> Tuple[float, str]:
    """
    Parse a time string and return seconds past the J2000
    epoch on a formal calendar.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tparse_c.html

    :param instring: Input time string, UTC.
    :param lenout: Available space in output error message string.
    :return: Equivalent UTC seconds past J2000, Descriptive error message.
    """
    errmsg = stypes.string_to_char_p(lenout)
    lenout = ctypes.c_int(lenout)
    instring = stypes.string_to_char_p(instring)
    sp2000 = ctypes.c_double()
    libspice.tparse_c(instring, lenout, ctypes.byref(sp2000), errmsg)
    return sp2000.value, stypes.to_python_string(errmsg)


@spice_error_check
def tpictr(
    sample: str, lenout: int = _default_len_out, lenerr: int = _default_len_out
) -> Tuple[str, int, str]:
    """
    Given a sample time string, create a time format picture
    suitable for use by the routine timout.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tpictr_c.html

    :param sample: A sample time string.
    :param lenout: The length for the output picture string.
    :param lenerr: The length for the output error string.
    :return:
            A format picture that describes sample,
            Flag indicating whether sample parsed successfully,
            Diagnostic returned if sample cannot be parsed
    """
    sample = stypes.string_to_char_p(sample)
    pictur = stypes.string_to_char_p(lenout)
    errmsg = stypes.string_to_char_p(lenerr)
    lenout = ctypes.c_int(lenout)
    lenerr = ctypes.c_int(lenerr)
    ok = ctypes.c_int()
    libspice.tpictr_c(sample, lenout, lenerr, pictur, ctypes.byref(ok), errmsg)
    return stypes.to_python_string(pictur), ok.value, stypes.to_python_string(errmsg)


@spice_error_check
def trace(matrix: Union[ndarray, Iterable[Iterable[float]]]) -> float:
    """
    Return the trace of a 3x3 matrix.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/trace_c.html

    :param matrix: 3x3 matrix of double precision numbers.
    :return: The trace of matrix.
    """
    matrix = stypes.to_double_matrix(matrix)
    return libspice.trace_c(matrix)


@spice_error_check
def trcdep() -> int:
    """
    Return the number of modules in the traceback representation.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/trcdep_c.html

    :return: The number of modules in the traceback.
    """
    depth = ctypes.c_int()
    libspice.trcdep_c(ctypes.byref(depth))
    return depth.value


@spice_error_check
def trcnam(index: int, namlen: int = _default_len_out) -> str:
    """
    Return the name of the module having the specified position in
    the trace representation. The first module to check in is at
    index 0.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/trcnam_c.html

    :param index: The position of the requested module name.
    :param namlen: Available space in output name string.
    :return: The name at position index in the traceback.
    """
    index = ctypes.c_int(index)
    name = stypes.string_to_char_p(namlen)
    namlen = ctypes.c_int(namlen)
    libspice.trcnam_c(index, namlen, name)
    return stypes.to_python_string(name)


@spice_error_check
def trcoff() -> None:
    """
    Disable tracing.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/trcoff_c.html

    """
    libspice.trcoff_c()


@spice_error_check
def trgsep(
    et: float,
    targ1: str,
    shape1: str,
    frame1: str,
    targ2: str,
    shape2: str,
    frame2: str,
    obsrvr: str,
    abcorr: str,
) -> float:
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
    _et = ctypes.c_double(et)
    _targ1 = stypes.string_to_char_p(targ1)
    _shape1 = stypes.string_to_char_p(shape1)
    # intentional, N67 does not support additional frames
    _frame1 = stypes.string_to_char_p("NULL")
    _targ2 = stypes.string_to_char_p(targ2)
    _shape2 = stypes.string_to_char_p(shape2)
    # intentional, N67 does not support additional frames
    _frame2 = stypes.string_to_char_p("NULL")
    _obsrvr = stypes.string_to_char_p(obsrvr)
    _abcorr = stypes.string_to_char_p(abcorr)
    return libspice.trgsep_c(
        _et,
        _targ1,
        _shape1,
        _frame1,
        _targ2,
        _shape2,
        _frame2,
        _obsrvr,
        _abcorr,
    )


@spice_error_check
def tsetyr(year: int) -> None:
    """
    Set the lower bound on the 100 year range.

    Default value is 1969

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tsetyr_c.html

    :param year: Lower bound on the 100 year interval of expansion
    """
    year = ctypes.c_int(year)
    libspice.tsetyr_c(year)


@spice_error_check
def twopi() -> float:
    """
    Return twice the value of pi
    (the ratio of the circumference of a circle to its diameter).

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/twopi_c.html

    :return: Twice the value of pi.
    """
    return libspice.twopi_c()


@spice_error_check
def twovec(
    axdef: Union[ndarray, Iterable[float]],
    indexa: int,
    plndef: Union[ndarray, Iterable[float]],
    indexp: int,
) -> ndarray:
    """
    Find the transformation to the right-handed frame having a
    given vector as a specified axis and having a second given
    vector lying in a specified coordinate plane.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/twovec_c.html

    :param axdef: Vector defining a principal axis.
    :param indexa: Principal axis number of axdef (X=1, Y=2, Z=3).
    :param plndef: Vector defining (with axdef) a principal plane.
    :param indexp: Second axis number (with indexa) of principal plane.
    :return: Output rotation matrix.
    """
    axdef = stypes.to_double_vector(axdef)
    indexa = ctypes.c_int(indexa)
    plndef = stypes.to_double_vector(plndef)
    indexp = ctypes.c_int(indexp)
    mout = stypes.empty_double_matrix()
    libspice.twovec_c(axdef, indexa, plndef, indexp, mout)
    return stypes.c_matrix_to_numpy(mout)


@spice_error_check
def twovxf(
    axdef: Union[ndarray, Iterable[float]],
    indexa: int,
    plndef: Union[ndarray, Iterable[float]],
    indexp: int,
) -> ndarray:
    """
    Find the state transformation from a base frame to the
    right-handed frame defined by two state vectors: one state
    vector defining a specified axis and a second state vector
    defining a specified coordinate plane.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/twovxf_c.html

    :param axdef: Vector defining a principal axis.
    :param indexa: Principal axis number of axdef (X=1, Y=2, Z=3).
    :param plndef: Vector defining (with axdef) a principal plane.
    :param indexp: Second axis number (with indexa) of principal plane.
    :return: Output rotation matrix.
    """
    _axdef = stypes.to_double_vector(axdef)
    _indexa = ctypes.c_int(indexa)
    _plndef = stypes.to_double_vector(plndef)
    _indexp = ctypes.c_int(indexp)
    mout = stypes.empty_double_matrix(6, 6)
    libspice.twovxf_c(_axdef, _indexa, _plndef, _indexp, mout)
    return stypes.c_matrix_to_numpy(mout)


@spice_error_check
def txtopn(fname: str) -> int:
    """
    Internal undocumented command for opening a new text file for
    subsequent write access.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ftncls_c.html#Files
    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ftncls_c.html#Examples

    :param fname: name of the new text file to be opened.
    :return: FORTRAN logical unit of opened file
    """
    fname_p = stypes.string_to_char_p(fname)
    unit_out = ctypes.c_int()
    fname_len = ctypes.c_int(len(fname))
    libspice.txtopn_(fname_p, ctypes.byref(unit_out), fname_len)
    return unit_out.value


@spice_error_check
def tyear() -> float:
    """
    Return the number of seconds in a tropical year.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tyear_c.html

    :return: The number of seconds in a tropical year.
    """
    return libspice.tyear_c()


################################################################################
# U


@spice_error_check
def ucase(inchar: str, lenout: Optional[int] = None) -> str:
    """
    Convert the characters in a string to uppercase.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ucase_c.html

    :param inchar: Input string.
    :param lenout: Optional Maximum length of output string.
    :return: Output string, all uppercase.
    """
    if lenout is None:
        lenout = len(inchar) + 1
    inchar = stypes.string_to_char_p(inchar)
    outchar = stypes.string_to_char_p(" " * lenout)
    lenout = ctypes.c_int(lenout)
    libspice.ucase_c(inchar, lenout, outchar)
    return stypes.to_python_string(outchar)


@spice_error_check
def ucrss(v1: ndarray, v2: ndarray) -> ndarray:
    """
    Compute the normalized cross product of two 3-vectors.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ucrss_c.html

    :param v1: Left vector for cross product.
    :param v2: Right vector for cross product.
    :return: Normalized cross product v1xv2 / abs(v1xv2).
    """
    v1 = stypes.to_double_vector(v1)
    v2 = stypes.to_double_vector(v2)
    vout = stypes.empty_double_vector(3)
    libspice.ucrss_c(v1, v2, vout)
    return stypes.c_vector_to_python(vout)


def uddc(udfunc: UDFUNC, x: float, dx: float) -> bool:
    """
    SPICE private routine intended solely for the support of SPICE
    routines. Users should not call this routine directly due to the
    volatile nature of this routine.

    This routine calculates the derivative of 'udfunc' with respect
    to time for 'et', then determines if the derivative has a
    negative value.

    Use the @spiceypy.utils.callbacks.SpiceUDFUNS dectorator to wrap
    a given python function that takes one parameter (float) and
    returns a float. For example::

        @spiceypy.utils.callbacks.SpiceUDFUNS
        def udfunc(et_in):
            pos, new_et = spice.spkpos("MERCURY", et_in, "J2000", "LT+S", "MOON")
            return new_et

        is_negative = spice.uddc(udfunc, et, 1.0)

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/uddc_c.html

    :param udfunc: Name of the routine that computes the scalar value of interest.
    :param x: Independent variable of 'udfunc'.
    :param dx: Interval from 'x' for derivative calculation.
    :return: Boolean indicating if the derivative is negative.
    """
    x = ctypes.c_double(x)
    dx = ctypes.c_double(dx)
    isdescr = ctypes.c_int()
    libspice.uddc_c(udfunc, x, dx, ctypes.byref(isdescr))
    return bool(isdescr.value)


@spice_error_check
def uddf(udfunc: UDFUNC, x: float, dx: float) -> float:
    """
    Routine to calculate the first derivative of a caller-specified
    function using a three-point estimation.

    Use the @spiceypy.utils.callbacks.SpiceUDFUNS dectorator to wrap
    a given python function that takes one parameter (float) and
    returns a float. For example::

        @spiceypy.utils.callbacks.SpiceUDFUNS
        def udfunc(et_in):
            pos, new_et = spice.spkpos("MERCURY", et_in, "J2000", "LT+S", "MOON")
            return new_et

        deriv = spice.uddf(udfunc, et, 1.0)

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/uddf_c.html

    :param udfunc: Name of the routine that computes the scalar value of interest.
    :param x: Independent variable of 'udfunc'.
    :param dx: Interval from 'x' for derivative calculation.
    :return: Approximate derivative of 'udfunc' at 'x'
    """
    x = ctypes.c_double(x)
    dx = ctypes.c_double(dx)
    deriv = ctypes.c_double()
    libspice.uddf_c(udfunc, x, dx, ctypes.byref(deriv))
    return deriv.value


def udf(x: float) -> float:
    """
    No-op routine for with an argument signature matching udfuns.
    Allways returns 0.0 .

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/udf_c.html

    :param x: Double precision value, unused.
    :return: Double precision value, unused.
    """
    x = ctypes.c_double(x)
    value = ctypes.c_double()
    libspice.udf_c(x, ctypes.byref(value))
    return value.value


@spice_error_check
def union(a: SpiceCell, b: SpiceCell) -> SpiceCell:
    """
    Compute the union of two sets of any data type to form a third set.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/union_c.html

    :param a: First input set.
    :param b: Second input set.
    :return: Union of a and b.
    """
    assert isinstance(a, stypes.SpiceCell)
    assert isinstance(b, stypes.SpiceCell)
    assert a.dtype == b.dtype
    # Next line was redundant with [raise NotImpImplementedError] below
    # assert a.dtype == 0 or a.dtype == 1 or a.dtype == 2
    if a.dtype == 0:
        c = stypes.SPICECHAR_CELL(max(a.size, b.size), max(a.length, b.length))
    elif a.dtype == 1:
        c = stypes.SPICEDOUBLE_CELL(max(a.size, b.size))
    elif a.dtype == 2:
        c = stypes.SPICEINT_CELL(max(a.size, b.size))
    else:
        raise NotImplementedError
    libspice.union_c(ctypes.byref(a), ctypes.byref(b), ctypes.byref(c))
    return c


@spice_error_check
def unitim(epoch: float, insys: str, outsys: str) -> float:
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
    epoch = ctypes.c_double(epoch)
    insys = stypes.string_to_char_p(insys)
    outsys = stypes.string_to_char_p(outsys)
    return libspice.unitim_c(epoch, insys, outsys)


@spice_error_check
def unload(filename: Union[str, Iterable[str]]) -> None:
    """
    Unload a SPICE kernel.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/unload_c.html

    :param filename: The name of a kernel to unload.
    """
    if stypes.is_iterable(filename):
        for f in filename:
            libspice.unload_c(stypes.string_to_char_p(f))
    else:
        filename = stypes.string_to_char_p(filename)
        libspice.unload_c(filename)


@spice_error_check
def unorm(v1: ndarray) -> Tuple[ndarray, float]:
    """
    Normalize a double precision 3-vector and return its magnitude.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/unorm_c.html

    :param v1: Vector to be normalized.
    :return: Unit vector of v1, Magnitude of v1.
    """
    v1 = stypes.to_double_vector(v1)
    vout = stypes.empty_double_vector(3)
    vmag = ctypes.c_double()
    libspice.unorm_c(v1, vout, ctypes.byref(vmag))
    return stypes.c_vector_to_python(vout), vmag.value


@spice_error_check
def unormg(v1: ndarray) -> Tuple[ndarray, float]:
    """
    Normalize a double precision vector of arbitrary dimension and
    return its magnitude.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/unormg_c.html

    :param v1: Vector to be normalized.
    :return: Unit vector of v1, Magnitude of v1.
    """
    ndim = len(v1)
    v1 = stypes.to_double_vector(v1)
    vout = stypes.empty_double_vector(ndim)
    vmag = ctypes.c_double()
    ndim = ctypes.c_int(ndim)
    libspice.unormg_c(v1, ndim, vout, ctypes.byref(vmag))
    return stypes.c_vector_to_python(vout), vmag.value


@spice_error_check
def utc2et(utcstr: str) -> float:
    """
    Convert an input time from Calendar or Julian Date format, UTC,
    to ephemeris seconds past J2000.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/utc2et_c.html

    :param utcstr: Input time string, UTC.
    :return: Output epoch, ephemeris seconds past J2000.
    """
    utcstr = stypes.string_to_char_p(utcstr)
    et = ctypes.c_double()
    libspice.utc2et_c(utcstr, ctypes.byref(et))
    return et.value


################################################################################
# V


@spice_error_check
def vadd(
    v1: Union[ndarray, Iterable[float]], v2: Union[ndarray, Iterable[float]]
) -> ndarray:
    """Add two 3 dimensional vectors.
    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vadd_c.html

    :param v1: First vector to be added.
    :param v2: Second vector to be added.
    :return: v1+v2
    """
    v1 = stypes.to_double_vector(v1)
    v2 = stypes.to_double_vector(v2)
    vout = stypes.empty_double_vector(3)
    libspice.vadd_c(v1, v2, vout)
    return stypes.c_vector_to_python(vout)


@spice_error_check
def vaddg(
    v1: Union[ndarray, Iterable[float]], v2: Union[ndarray, Iterable[float]]
) -> ndarray:
    """
    Add two n-dimensional vectors
    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vaddg_c.html

    :param v1: First vector to be added.
    :param v2: Second vector to be added.
    :return: v1+v2
    """
    ndim = len(v1)
    v1 = stypes.to_double_vector(v1)
    v2 = stypes.to_double_vector(v2)
    vout = stypes.empty_double_vector(ndim)
    ndim = ctypes.c_int(ndim)
    libspice.vaddg_c(v1, v2, ndim, vout)
    return stypes.c_vector_to_python(vout)


@spice_error_check
def valid(insize: int, n: int, inset: SpiceCell) -> SpiceCell:
    """
    Create a valid CSPICE set from a CSPICE Cell of any data type.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/valid_c.html

    :param insize: Size (maximum cardinality) of the set.
    :param n: Initial no. of (possibly non-distinct) elements.
    :param inset: Set to be validated.
    :return: validated set
    """
    assert isinstance(inset, stypes.SpiceCell)
    insize = ctypes.c_int(insize)
    n = ctypes.c_int(n)
    libspice.valid_c(insize, n, inset)
    return inset


@spice_error_check
def vcrss(v1: ndarray, v2: ndarray) -> ndarray:
    """
    Compute the cross product of two 3-dimensional vectors.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vcrss_c.html

    :param v1: Left hand vector for cross product.
    :param v2: Right hand vector for cross product.
    :return: Cross product v1 x v2.
    """
    v1 = stypes.to_double_vector(v1)
    v2 = stypes.to_double_vector(v2)
    vout = stypes.empty_double_vector(3)
    libspice.vcrss_c(v1, v2, vout)
    return stypes.c_vector_to_python(vout)


@spice_error_check
def vdist(v1: ndarray, v2: ndarray) -> float:
    """
    Return the distance between two three-dimensional vectors.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vdist_c.html

    :param v1: First vector in the dot product.
    :param v2: Second vector in the dot product.
    :return: the distance between v1 and v2
    """
    v1 = stypes.to_double_vector(v1)
    v2 = stypes.to_double_vector(v2)
    return libspice.vdist_c(v1, v2)


@spice_error_check
def vdistg(v1: ndarray, v2: ndarray) -> float:
    """
    Return the distance between two vectors of arbitrary dimension.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vdistg_c.html

    :param v1: ndim-dimensional double precision vector.
    :param v2: ndim-dimensional double precision vector.
    :return: the distance between v1 and v2
    """
    ndim = len(v1)
    v1 = stypes.to_double_vector(v1)
    v2 = stypes.to_double_vector(v2)
    ndim = ctypes.c_int(ndim)
    return libspice.vdistg_c(v1, v2, ndim)


@spice_error_check
def vdot(v1: ndarray, v2: ndarray) -> float:
    """
    Compute the dot product of two double precision, 3-dimensional vectors.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vdot_c.html

    :param v1: First vector in the dot product.
    :param v2: Second vector in the dot product.
    :return: dot product of v1 and v2.
    """
    v1 = stypes.to_double_vector(v1)
    v2 = stypes.to_double_vector(v2)
    return libspice.vdot_c(v1, v2)


@spice_error_check
def vdotg(v1: ndarray, v2: ndarray) -> float:
    """
    Compute the dot product of two double precision vectors of
    arbitrary dimension.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vdotg_c.html

    :param v1: First vector in the dot product.
    :param v2: Second vector in the dot product.
    :return: dot product of v1 and v2.
    """
    ndim = len(v1)
    v1 = stypes.to_double_vector(v1)
    v2 = stypes.to_double_vector(v2)
    ndim = ctypes.c_int(ndim)
    return libspice.vdotg_c(v1, v2, ndim)


@spice_error_check
def vequ(v1: ndarray) -> ndarray:
    """
    Make one double precision 3-dimensional vector equal to another.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vequ_c.html

    :param v1: 3-dimensional double precision vector.
    :return: 3-dimensional double precision vector set equal to vin.
    """
    v1 = stypes.to_double_vector(v1)
    vout = stypes.empty_double_vector(3)
    libspice.vequ_c(v1, vout)
    return stypes.c_vector_to_python(vout)


@spice_error_check
def vequg(v1: ndarray) -> ndarray:
    """
    Make one double precision vector of arbitrary dimension equal to another.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vequg_c.html

    :param v1: ndim-dimensional double precision vector.
    :param ndim: Dimension of vin (and also vout).
    :return: ndim-dimensional double precision vector set equal to vin.
    """
    ndim = len(v1)
    v1 = stypes.to_double_vector(v1)
    vout = stypes.empty_double_vector(ndim)
    ndim = ctypes.c_int(ndim)
    libspice.vequg_c(v1, ndim, vout)
    return stypes.c_vector_to_python(vout)


@spice_error_check
def vhat(v1: ndarray) -> ndarray:
    """
    Find the unit vector along a double precision 3-dimensional vector.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vhat_c.html

    :param v1: Vector to be unitized.
    :return: Unit vector v / abs(v).
    """
    v1 = stypes.to_double_vector(v1)
    vout = stypes.empty_double_vector(3)
    libspice.vhat_c(v1, vout)
    return stypes.c_vector_to_python(vout)


@spice_error_check
def vhatg(v1: ndarray) -> ndarray:
    """
    Find the unit vector along a double precision vector of arbitrary dimension.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vhatg_c.html

    :param v1: Vector to be normalized.
    :return: Unit vector v / abs(v).
    """
    ndim = len(v1)
    v1 = stypes.to_double_vector(v1)
    vout = stypes.empty_double_vector(ndim)
    ndim = ctypes.c_int(ndim)
    libspice.vhatg_c(v1, ndim, vout)
    return stypes.c_vector_to_python(vout)


@spice_error_check
def vlcom(
    a: float,
    v1: Union[ndarray, Iterable[float]],
    b: float,
    v2: Union[ndarray, Iterable[float]],
) -> ndarray:
    """
    Compute a vector linear combination of two double precision,
    3-dimensional vectors.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vlcom_c.html

    :param a: Coefficient of v1
    :param v1: Vector in 3-space
    :param b: Coefficient of v2
    :param v2: Vector in 3-space
    :return: Linear Vector Combination a*v1 + b*v2.
    """
    v1 = stypes.to_double_vector(v1)
    v2 = stypes.to_double_vector(v2)
    sumv = stypes.empty_double_vector(3)
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    libspice.vlcom_c(a, v1, b, v2, sumv)
    return stypes.c_vector_to_python(sumv)


@spice_error_check
def vlcom3(
    a: float,
    v1: Union[ndarray, Iterable[float]],
    b: float,
    v2: Union[ndarray, Iterable[float]],
    c: float,
    v3: Union[ndarray, Iterable[float]],
) -> ndarray:
    """
    This subroutine computes the vector linear combination
    a*v1 + b*v2 + c*v3 of double precision, 3-dimensional vectors.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vlcom3_c.html

    :param a: Coefficient of v1
    :param v1: Vector in 3-space
    :param b: Coefficient of v2
    :param v2: Vector in 3-space
    :param c: Coefficient of v3
    :param v3: Vector in 3-space
    :return: Linear Vector Combination a*v1 + b*v2 + c*v3
    """
    v1 = stypes.to_double_vector(v1)
    v2 = stypes.to_double_vector(v2)
    v3 = stypes.to_double_vector(v3)
    sumv = stypes.empty_double_vector(3)
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    libspice.vlcom3_c(a, v1, b, v2, c, v3, sumv)
    return stypes.c_vector_to_python(sumv)


@spice_error_check
def vlcomg(
    n: int,
    a: float,
    v1: Union[ndarray, Iterable[float]],
    b: float,
    v2: Union[ndarray, Iterable[float]],
) -> ndarray:
    """
    Compute a vector linear combination of two double precision
    vectors of arbitrary dimension.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vlcomg_c.html

    :param n: Dimension of vector space
    :param a: Coefficient of v1
    :param v1: Vector in n-space
    :param b: Coefficient of v2
    :param v2: Vector in n-space
    :return: Linear Vector Combination a*v1 + b*v2
    """
    v1 = stypes.to_double_vector(v1)
    v2 = stypes.to_double_vector(v2)
    sumv = stypes.empty_double_vector(n)
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    n = ctypes.c_int(n)
    libspice.vlcomg_c(n, a, v1, b, v2, sumv)
    return stypes.c_vector_to_python(sumv)


@spice_error_check
def vminug(vin: ndarray) -> ndarray:
    """
    Negate a double precision vector of arbitrary dimension.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vminug_c.html

    :param vin: ndim-dimensional double precision vector to be negated.
    :return: ndim-dimensional double precision vector equal to -vin.
    """
    ndim = len(vin)
    vin = stypes.to_double_vector(vin)
    vout = stypes.empty_double_vector(ndim)
    ndim = ctypes.c_int(ndim)
    libspice.vminug_c(vin, ndim, vout)
    return stypes.c_vector_to_python(vout)


@spice_error_check
def vminus(vin: ndarray) -> ndarray:
    """
    Negate a double precision 3-dimensional vector.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vminus_c.html

    :param vin: Vector to be negated.
    :return: Negated vector -v1.
    """
    vin = stypes.to_double_vector(vin)
    vout = stypes.empty_double_vector(3)
    libspice.vminus_c(vin, vout)
    return stypes.c_vector_to_python(vout)


@spice_error_check
def vnorm(v: ndarray) -> float:
    """
    Compute the magnitude of a double precision, 3-dimensional vector.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vnorm_c.html

    :param v: Vector whose magnitude is to be found.
    :return: magnitude of v calculated in a numerically stable way
    """
    v = stypes.to_double_vector(v)
    return libspice.vnorm_c(v)


@spice_error_check
def vnormg(v: ndarray) -> float:
    """
    Compute the magnitude of a double precision vector of arbitrary dimension.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vnormg_c.html

    :param v: Vector whose magnitude is to be found.
    :return: magnitude of v calculated in a numerically stable way
    """
    ndim = len(v)
    v = stypes.to_double_vector(v)
    ndim = ctypes.c_int(ndim)
    return libspice.vnormg_c(v, ndim)


@spice_error_check
def vpack(x: float, y: float, z: float) -> ndarray:
    """
    Pack three scalar components into a vector.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vpack_c.html

    :param x: first scalar component
    :param y: second scalar component
    :param z: third scalar component
    :return: Equivalent 3-vector.
    """
    x = ctypes.c_double(x)
    y = ctypes.c_double(y)
    z = ctypes.c_double(z)
    vout = stypes.empty_double_vector(3)
    libspice.vpack_c(x, y, z, vout)
    return stypes.c_vector_to_python(vout)


@spice_error_check
def vperp(a: ndarray, b: ndarray) -> ndarray:
    """
    Find the component of a vector that is perpendicular to a second
    vector. All vectors are 3-dimensional.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vperp_c.html

    :param a: The vector whose orthogonal component is sought.
    :param b: The vector used as the orthogonal reference.
    :return: The component of a orthogonal to b.
    """
    a = stypes.to_double_vector(a)
    b = stypes.to_double_vector(b)
    vout = stypes.empty_double_vector(3)
    libspice.vperp_c(a, b, vout)
    return stypes.c_vector_to_python(vout)


@spice_error_check
def vprjp(vin: Union[ndarray, Iterable[float]], plane: Plane) -> ndarray:
    """
    Project a vector onto a specified plane, orthogonally.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vprjp_c.html

    :param vin: The projected vector.
    :param plane: Plane containing vin.
    :return: Vector resulting from projection.
    """
    vin = stypes.to_double_vector(vin)
    vout = stypes.empty_double_vector(3)
    libspice.vprjp_c(vin, ctypes.byref(plane), vout)
    return stypes.c_vector_to_python(vout)


@spice_error_check
@spice_found_exception_thrower
def vprjpi(
    vin: Union[ndarray, Iterable[float]], projpl: Plane, invpl: Plane
) -> Tuple[ndarray, bool]:
    """
    Find the vector in a specified plane that maps to a specified
    vector in another plane under orthogonal projection.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vprjpi_c.html

    :param vin: The projected vector.
    :param projpl: Plane containing vin.
    :param invpl: Plane containing inverse image of vin.
    :return: Inverse projection of vin.
    """
    vin = stypes.to_double_vector(vin)
    vout = stypes.empty_double_vector(3)
    found = ctypes.c_int()
    libspice.vprjpi_c(
        vin, ctypes.byref(projpl), ctypes.byref(invpl), vout, ctypes.byref(found)
    )
    return stypes.c_vector_to_python(vout), bool(found.value)


@spice_error_check
def vproj(a: ndarray, b: ndarray) -> ndarray:
    """
    Find the projection of one vector onto another vector.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vproj_c.html

    :param a: The vector to be projected.
    :param b: The vector onto which a is to be projected.
    :return: The projection of a onto b.
    """
    a = stypes.to_double_vector(a)
    b = stypes.to_double_vector(b)
    vout = stypes.empty_double_vector(3)
    libspice.vproj_c(a, b, vout)
    return stypes.c_vector_to_python(vout)


@spice_error_check
def vprojg(a: ndarray, b: ndarray) -> ndarray:
    """
    Find the projection of one vector onto another vector.
    All vectors are of arbitrary dimension.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vprojg_c.html

    :param a: The vector to be projected.
    :param b: The vector onto which a is to be projected.
    :return: The projection of a onto b.
    """
    ndim = len(a)
    assert ndim == len(b)
    _a = stypes.to_double_vector(a)
    _b = stypes.to_double_vector(b)
    vout = stypes.empty_double_vector(ndim)
    ndim = ctypes.c_int(ndim)
    libspice.vprojg_c(_a, _b, ndim, vout)
    return stypes.c_vector_to_python(vout)


@spice_error_check
def vrel(
    v1: Union[ndarray, Iterable[float]], v2: Union[ndarray, Iterable[float]]
) -> float:
    """
    Return the relative difference between two 3-dimensional vectors.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vrel_c.html

    :param v1: First vector
    :param v2: Second vector
    :return: the relative difference between v1 and v2.
    """
    v1 = stypes.to_double_vector(v1)
    v2 = stypes.to_double_vector(v2)
    return libspice.vrel_c(v1, v2)


@spice_error_check
def vrelg(
    v1: Union[ndarray, Iterable[float]], v2: Union[ndarray, Iterable[float]]
) -> float:
    """
    Return the relative difference between two vectors of general dimension.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vrelg_c.html

    :param v1: First vector
    :param v2: Second vector
    :return: the relative difference between v1 and v2.
    """
    ndim = len(v1)
    v1 = stypes.to_double_vector(v1)
    v2 = stypes.to_double_vector(v2)
    ndim = ctypes.c_int(ndim)
    return libspice.vrelg_c(v1, v2, ndim)


@spice_error_check
def vrotv(v: ndarray, axis: ndarray, theta: float) -> ndarray:
    """
    Rotate a vector about a specified axis vector by a
    specified angle and return the rotated vector.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vrotv_c.html

    :param v: Vector to be rotated.
    :param axis: Axis of the rotation.
    :param theta: Angle of rotation (radians).
    :return: Result of rotating v about axis by theta
    """
    v = stypes.to_double_vector(v)
    axis = stypes.to_double_vector(axis)
    theta = ctypes.c_double(theta)
    r = stypes.empty_double_vector(3)
    libspice.vrotv_c(v, axis, theta, r)
    return stypes.c_vector_to_python(r)


@spice_error_check
def vscl(s: float, v1: ndarray) -> ndarray:
    """
    Multiply a scalar and a 3-dimensional double precision vector.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vscl_c.html

    :param s: Scalar to multiply a vector
    :param v1: Vector to be multiplied
    :return: Product vector, s*v1.
    """
    s = ctypes.c_double(s)
    v1 = stypes.to_double_vector(v1)
    vout = stypes.empty_double_vector(3)
    libspice.vscl_c(s, v1, vout)
    return stypes.c_vector_to_python(vout)


@spice_error_check
def vsclg(s: float, v1: ndarray) -> ndarray:
    """
    Multiply a scalar and a double precision vector of arbitrary dimension.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vsclg_c.html

    :param s: Scalar to multiply a vector
    :param v1: Vector to be multiplied
    :return: Product vector, s*v1.
    """
    ndim = len(v1)
    s = ctypes.c_double(s)
    v1 = stypes.to_double_vector(v1)
    vout = stypes.empty_double_vector(ndim)
    ndim = ctypes.c_int(ndim)
    libspice.vsclg_c(s, v1, ndim, vout)
    return stypes.c_vector_to_python(vout)


@spice_error_check
def vsep(v1: ndarray, v2: ndarray) -> float:
    """
    Find the separation angle in radians between two double
    precision, 3-dimensional vectors. This angle is defined as zero
    if either vector is zero.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vsep_c.html

    :param v1: First vector
    :param v2: Second vector
    :return: separation angle in radians
    """
    v1 = stypes.to_double_vector(v1)
    v2 = stypes.to_double_vector(v2)
    return libspice.vsep_c(v1, v2)


@spice_error_check
def vsepg(v1: ndarray, v2: ndarray) -> float:
    """
    Find the separation angle in radians between two double
    precision vectors of arbitrary dimension. This angle is defined
    as zero if either vector is zero.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vsepg_c.html

    :param v1: First vector
    :param v2: Second vector
    :return: separation angle in radians
    """
    ndim = len(v1)
    v1 = stypes.to_double_vector(v1)
    v2 = stypes.to_double_vector(v2)
    ndim = ctypes.c_int(ndim)
    return libspice.vsepg_c(v1, v2, ndim)


@spice_error_check
def vsub(v1: ndarray, v2: ndarray) -> ndarray:
    """
    Compute the difference between two 3-dimensional,
    double precision vectors.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vsub_c.html

    :param v1: First vector (minuend).
    :param v2: Second vector (subtrahend).
    :return: Difference vector, v1 - v2.
    """
    v1 = stypes.to_double_vector(v1)
    v2 = stypes.to_double_vector(v2)
    vout = stypes.empty_double_vector(3)
    libspice.vsub_c(v1, v2, vout)
    return stypes.c_vector_to_python(vout)


@spice_error_check
def vsubg(v1: ndarray, v2: ndarray) -> ndarray:
    """
    Compute the difference between two double precision
    vectors of arbitrary dimension.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vsubg_c.html

    :param v1: First vector (minuend).
    :param v2: Second vector (subtrahend).
    :return: Difference vector, v1 - v2.
    """
    ndim = len(v1)
    v1 = stypes.to_double_vector(v1)
    v2 = stypes.to_double_vector(v2)
    vout = stypes.empty_double_vector(ndim)
    ndim = ctypes.c_int(ndim)
    libspice.vsubg_c(v1, v2, ndim, vout)
    return stypes.c_vector_to_python(vout)


@spice_error_check
def vtmv(v1: ndarray, matrix: ndarray, v2: ndarray) -> float:
    """
    Multiply the transpose of a 3-dimensional column vector
    a 3x3 matrix, and a 3-dimensional column vector.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vtmv_c.html

    :param v1: 3 dimensional double precision column vector.
    :param matrix: 3x3 double precision matrix.
    :param v2: 3 dimensional double precision column vector.
    :return: the result of (v1**t * matrix * v2 ).
    """
    v1 = stypes.to_double_vector(v1)
    matrix = stypes.to_double_matrix(matrix)
    v2 = stypes.to_double_vector(v2)
    return libspice.vtmv_c(v1, matrix, v2)


@spice_error_check
def vtmvg(v1: ndarray, matrix: ndarray, v2: ndarray) -> float:
    """
    Multiply the transpose of a n-dimensional
    column vector a nxm matrix,
    and a m-dimensional column vector.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vtmvg_c.html

    :param v1: n-dimensional double precision column vector.
    :param matrix: nxm double precision matrix.
    :param v2: m-dimensional double porecision column vector.
    :return: the result of (v1**t * matrix * v2 )
    """
    nrow, ncol = len(v1), len(v2)
    v1 = stypes.to_double_vector(v1)
    matrix = stypes.to_double_matrix(matrix)
    v2 = stypes.to_double_vector(v2)
    nrow = ctypes.c_int(nrow)
    ncol = ctypes.c_int(ncol)
    return libspice.vtmvg_c(v1, matrix, v2, nrow, ncol)


@spice_error_check
def vupack(v: ndarray) -> Tuple[float, float, float]:
    """
    Unpack three scalar components from a vector.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vupack_c.html

    :param v: Vector
    :return: (x, y, z)
    """
    v1 = stypes.to_double_vector(v)
    x = ctypes.c_double()
    y = ctypes.c_double()
    z = ctypes.c_double()
    libspice.vupack_c(v1, ctypes.byref(x), ctypes.byref(y), ctypes.byref(z))
    return x.value, y.value, z.value


@spice_error_check
def vzero(v: ndarray) -> bool:
    """
    Indicate whether a 3-vector is the zero vector.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vzero_c.html

    :param v: Vector to be tested
    :return: true if and only if v is the zero vector
    """
    v = stypes.to_double_vector(v)
    return bool(libspice.vzero_c(v))


@spice_error_check
def vzerog(v: ndarray) -> bool:
    """
    Indicate whether a general-dimensional vector is the zero vector.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vzerog_c.html

    :param v: Vector to be tested
    :return: true if and only if v is the zero vector
    """
    ndim = len(v)
    v = stypes.to_double_vector(v)
    ndim = ctypes.c_int(ndim)
    return bool(libspice.vzerog_c(v, ndim))


################################################################################
# W


@spice_error_check
def wncard(window: SpiceCell) -> int:
    """
    Return the cardinality (number of intervals) of a double
    precision window.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wncard_c.html

    :param window: Input window
    :return: the cardinality of the input window.
    """
    assert isinstance(window, stypes.SpiceCell)
    return libspice.wncard_c(window)


@spice_error_check
def wncomd(left: float, right: float, window: SpiceCell) -> SpiceCell:
    """
    Determine the complement of a double precision window with
    respect to a specified interval.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wncomd_c.html

    :param left: left endpoints of complement interval.
    :param right: right endpoints of complement interval.
    :param window: Input window
    :return: Complement of window with respect to left and right.
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    left = ctypes.c_double(left)
    right = ctypes.c_double(right)
    result = stypes.SpiceCell.double(window.size)
    libspice.wncomd_c(left, right, ctypes.byref(window), result)
    return result


@spice_error_check
def wncond(left: float, right: float, window: SpiceCell) -> SpiceCell:
    """
    Contract each of the intervals of a double precision window.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wncond_c.html

    :param left: Amount added to each left endpoint.
    :param right: Amount subtracted from each right endpoint.
    :param window: Window to be contracted
    :return: Contracted Window.
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    left = ctypes.c_double(left)
    right = ctypes.c_double(right)
    libspice.wncond_c(left, right, ctypes.byref(window))
    return window


@spice_error_check
def wndifd(a: SpiceCell, b: SpiceCell) -> SpiceCell:
    """
    Place the difference of two double precision windows into
    a third window.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wndifd_c.html

    :param a: Input window A.
    :param b: Input window B.
    :return: Difference of a and b.
    """
    assert isinstance(a, stypes.SpiceCell)
    assert isinstance(b, stypes.SpiceCell)
    assert a.dtype == 1
    assert b.dtype == 1
    c = stypes.SpiceCell.double(a.size + b.size)
    libspice.wndifd_c(ctypes.byref(a), ctypes.byref(b), ctypes.byref(c))
    return c


@spice_error_check
def wnelmd(point: float, window: SpiceCell) -> bool:
    """
    Determine whether a point is an element of a double precision
    window.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wnelmd_c.html

    :param point: Input point.
    :param window: Input window
    :return: returns True if point is an element of window.
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    point = ctypes.c_double(point)
    return bool(libspice.wnelmd_c(point, ctypes.byref(window)))


@spice_error_check
def wnexpd(left: float, right: float, window: SpiceCell) -> SpiceCell:
    """
    Expand each of the intervals of a double precision window.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wnexpd_c.html

    :param left: Amount subtracted from each left endpoint.
    :param right: Amount added to each right endpoint.
    :param window: Window to be expanded.
    :return: Expanded Window.
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    left = ctypes.c_double(left)
    right = ctypes.c_double(right)
    libspice.wnexpd_c(left, right, ctypes.byref(window))
    return window


@spice_error_check
def wnextd(side: str, window: SpiceCell) -> SpiceCell:
    """
    Extract the left or right endpoints from a double precision
    window.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wnextd_c.html

    :param side: Extract left "L" or right "R" endpoints.
    :param window: Window to be extracted.
    :return: Extracted Window.
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    assert side == "L" or side == "R"
    side = ctypes.c_char(side.encode(encoding="UTF-8"))
    libspice.wnextd_c(side, ctypes.byref(window))
    return window


@spice_error_check
def wnfetd(window: SpiceCell, n: int) -> Tuple[float, float]:
    """
    Fetch a particular interval from a double precision window.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wnfetd_c.html

    :param window: Input window
    :param n: Index of interval to be fetched.
    :return: Left, right endpoints of the nth interval.
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    n = ctypes.c_int(n)
    left = ctypes.c_double()
    right = ctypes.c_double()
    libspice.wnfetd_c(ctypes.byref(window), n, ctypes.byref(left), ctypes.byref(right))
    return left.value, right.value


@spice_error_check
def wnfild(small: float, window: SpiceCell) -> SpiceCell:
    """
    Fill small gaps between adjacent intervals of a double precision window.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wnfild_c.html

    :param small: Limiting measure of small gaps.
    :param window: Window to be filled
    :return: Filled Window.
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    small = ctypes.c_double(small)
    libspice.wnfild_c(small, ctypes.byref(window))
    return window


@spice_error_check
def wnfltd(small: float, window: SpiceCell) -> SpiceCell:
    """
    Filter (remove) small intervals from a double precision window.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wnfltd_c.html

    :param small: Limiting measure of small intervals.
    :param window: Window to be filtered.
    :return: Filtered Window.
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    small = ctypes.c_double(small)
    libspice.wnfltd_c(small, ctypes.byref(window))
    return window


@spice_error_check
def wnincd(left: float, right: float, window: SpiceCell) -> bool:
    """
    Determine whether an interval is included in a double precision window.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wnincd_c.html

    :param left: Left interval
    :param right: Right interval
    :param window: Input window
    :return: Returns True if the input interval is included in window.
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    left = ctypes.c_double(left)
    right = ctypes.c_double(right)
    return bool(libspice.wnincd_c(left, right, ctypes.byref(window)))


@spice_error_check
def wninsd(left: float, right: float, window: SpiceCell) -> None:
    """
    Insert an interval into a double precision window.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wninsd_c.html

    :param left: Left endpoints of new interval.
    :param right: Right endpoints of new interval.
    :param window: Input window.
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    left = ctypes.c_double(left)
    right = ctypes.c_double(right)
    libspice.wninsd_c(left, right, ctypes.byref(window))


@spice_error_check
def wnintd(a: SpiceCell, b: SpiceCell) -> SpiceCell:
    """
    Place the intersection of two double precision windows into
    a third window.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wnintd_c.html


    :param a: Input window A.
    :param b: Input window B.
    :return: Intersection of a and b.
    """
    assert isinstance(a, stypes.SpiceCell)
    assert b.dtype == 1
    assert isinstance(b, stypes.SpiceCell)
    assert a.dtype == 1
    c = stypes.SpiceCell.double(b.size + a.size)
    libspice.wnintd_c(ctypes.byref(a), ctypes.byref(b), ctypes.byref(c))
    return c


@spice_error_check
def wnreld(a: SpiceCell, op: str, b: SpiceCell) -> bool:
    """
    Compare two double precision windows.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wnreld_c.html

    :param a: First window.
    :param op: Comparison operator.
    :param b: Second window.
    :return: The result of comparison: a (op) b.
    """
    assert isinstance(a, stypes.SpiceCell)
    assert b.dtype == 1
    assert isinstance(b, stypes.SpiceCell)
    assert a.dtype == 1
    assert isinstance(op, str)
    op = stypes.string_to_char_p(op.encode(encoding="UTF-8"))
    return bool(libspice.wnreld_c(ctypes.byref(a), op, ctypes.byref(b)))


@spice_error_check
def wnsumd(window: SpiceCell) -> Tuple[float, float, float, int, int]:
    """
    Summarize the contents of a double precision window.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wnsumd_c.html

    :param window: Window to be summarized.
    :return:
            Total measure of intervals in window,
            Average measure, Standard deviation,
            Location of shortest interval,
            Location of longest interval.
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    meas = ctypes.c_double()
    avg = ctypes.c_double()
    stddev = ctypes.c_double()
    shortest = ctypes.c_int()
    longest = ctypes.c_int()
    libspice.wnsumd_c(
        ctypes.byref(window),
        ctypes.byref(meas),
        ctypes.byref(avg),
        ctypes.byref(stddev),
        ctypes.byref(shortest),
        ctypes.byref(longest),
    )
    return meas.value, avg.value, stddev.value, shortest.value, longest.value


@spice_error_check
def wnunid(a: SpiceCell, b: SpiceCell) -> SpiceCell:
    """
    Place the union of two double precision windows into a third window.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wnunid_c.html

    :param a: Input window A.
    :param b: Input window B.
    :return: Union of a and b.
    """
    assert isinstance(a, stypes.SpiceCell)
    assert b.dtype == 1
    assert isinstance(b, stypes.SpiceCell)
    assert a.dtype == 1
    c = stypes.SpiceCell.double(b.size + a.size)
    libspice.wnunid_c(ctypes.byref(a), ctypes.byref(b), ctypes.byref(c))
    return c


@spice_error_check
def wnvald(insize: int, n: int, window: SpiceCell) -> SpiceCell:
    """
    Form a valid double precision window from the contents
    of a window array.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wnvald_c.html

    :param insize: Size of window.
    :param n: Original number of endpoints.
    :param window: Input window.
    :return: The union of the intervals in the input cell.
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    insize = ctypes.c_int(insize)
    n = ctypes.c_int(n)
    libspice.wnvald_c(insize, n, ctypes.byref(window))
    return window


@spice_error_check
def writln(line: str, unit: int) -> None:
    """
    Internal undocumented command for writing a text line to a logical unit

    No URL available; relevant lines from SPICE source:

    FORTRAN SPICE, writln.f::

        C$Procedure      WRITLN ( Write a text line to a logical unit )
              SUBROUTINE WRITLN ( LINE, UNIT )
              CHARACTER*(*)      LINE
              INTEGER            UNIT

        C     Variable  I/O  Description
        C     --------  ---  --------------------------------------------------
        C     LINE       I   The line which is to be written to UNIT.
        C     UNIT       I   The Fortran unit number to use for output.

    CSPICE, writln.c::

        /* $Procedure      WRITLN ( Write a text line to a logical unit ) */
        /* Subroutine */ int writln_(char *line, integer *unit, ftnlen line_len)

    :param line: The line which is to be written to UNIT.
    :param unit: The Fortran unit number to use for output.
    """
    line_p = stypes.string_to_char_p(line)
    unit = ctypes.c_int(unit)
    line_len = ctypes.c_int(len(line))
    libspice.writln_(line_p, ctypes.byref(unit), line_len)


################################################################################
# X


@spice_error_check
def xf2eul(xform: ndarray, axisa: int, axisb: int, axisc: int) -> Tuple[ndarray, int]:
    """
    Convert a state transformation matrix to Euler angles and their
    derivatives with respect to a specified set of axes.

    The companion routine :func:`eul2xf` converts Euler angles and their
    derivatives with respect to a specified set of axes to a state
    transformation matrix.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/xf2eul_c.html

    :param xform: state transformation matrix
    :param axisa: Axis A of the Euler angle factorization.
    :param axisb: Axis B of the Euler angle factorization.
    :param axisc: Axis C of the Euler angle factorization.
    :return: (eulang, unique)
    """
    xform = stypes.to_double_matrix(xform)
    axisa = ctypes.c_int(axisa)
    axisb = ctypes.c_int(axisb)
    axisc = ctypes.c_int(axisc)
    eulang = stypes.empty_double_vector(6)
    unique = ctypes.c_int()
    libspice.xf2eul_c(xform, axisa, axisb, axisc, eulang, unique)
    return stypes.c_vector_to_python(eulang), unique.value


@spice_error_check
def xf2rav(xform: ndarray) -> Tuple[ndarray, ndarray]:
    """
    This routine determines the rotation matrix and angular velocity
    of the rotation from a state transformation matrix.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/xf2rav_c.html

    :param xform: state transformation matrix
    :return:
            rotation associated with xform,
            angular velocity associated with xform.
    """
    xform = stypes.to_double_matrix(xform)
    rot = stypes.empty_double_matrix()
    av = stypes.empty_double_vector(3)
    libspice.xf2rav_c(xform, rot, av)
    return stypes.c_matrix_to_numpy(rot), stypes.c_vector_to_python(av)


@spice_error_check
def xfmsta(
    input_state: ndarray, input_coord_sys: str, output_coord_sys: str, body: str
) -> ndarray:
    """
    Transform a state between coordinate systems.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/xfmsta_c.html

    :param input_state: Input state.
    :param input_coord_sys: Current (input) coordinate system.
    :param output_coord_sys: Desired (output) coordinate system.
    :param body:
                Name or NAIF ID of body with which coordinates
                are associated (if applicable).
    :return: Converted output state
    """
    input_state = stypes.to_double_vector(input_state)
    input_coord_sys = stypes.string_to_char_p(input_coord_sys)
    output_coord_sys = stypes.string_to_char_p(output_coord_sys)
    body = stypes.string_to_char_p(body)
    output_state = stypes.empty_double_vector(6)
    libspice.xfmsta_c(
        input_state, input_coord_sys, output_coord_sys, body, output_state
    )
    return stypes.c_vector_to_python(output_state)


@spice_error_check
def xpose(m: Union[ndarray, Iterable[Iterable[float]]]) -> ndarray:
    """
    Transpose a 3x3 matrix

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/xpose_c.html

    :param m: Matrix to be transposed
    :return: Transposed matrix
    """
    m = stypes.to_double_matrix(m)
    mout = stypes.empty_double_matrix(x=3, y=3)
    libspice.xpose_c(m, mout)
    return stypes.c_matrix_to_numpy(mout)


@spice_error_check
def xpose6(m: Union[ndarray, Iterable[Iterable[float]]]) -> ndarray:
    """
    Transpose a 6x6 matrix

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/xpose6_c.html

    :param m: Matrix to be transposed
    :return: Transposed matrix
    """
    m = stypes.to_double_matrix(m)
    mout = stypes.empty_double_matrix(x=6, y=6)
    libspice.xpose6_c(m, mout)
    return stypes.c_matrix_to_numpy(mout)


@spice_error_check
def xposeg(matrix: Union[ndarray, Iterable[Iterable[float]]]) -> ndarray:
    """
    Transpose a matrix of arbitrary size
    in place, the matrix need not be square.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/xposeg_c.html

    :param matrix: Matrix to be transposed
    :return: Transposed matrix
    """
    ncol, nrow = len(matrix[0]), len(matrix)
    matrix = stypes.to_double_matrix(matrix)
    mout = stypes.empty_double_matrix(x=nrow, y=ncol)
    ncol = ctypes.c_int(ncol)
    nrow = ctypes.c_int(nrow)
    libspice.xposeg_c(matrix, nrow, ncol, mout)
    return stypes.c_matrix_to_numpy(mout)


@spice_error_check
def zzdynrot(typid: int, center: int, et: float) -> Tuple[ndarray, int]:
    """
    Find the rotation from a dynamic frame ID to the associated frame at the time requested

    :param typid: ID code for the dynamic frame
    :param center: the ID for the center of the frame
    :param et: Epoch measured in seconds past J2000
    :return:  Rotation matrix from the input frame to the returned associated frame, id for the associated frame
    """
    typid = ctypes.c_int(typid)
    center = ctypes.c_int(center)
    et = ctypes.c_double(et)
    matrix = stypes.empty_double_matrix(x=3, y=3)
    next_frame = ctypes.c_int()
    libspice.zzdynrot_(
        ctypes.byref(typid),
        ctypes.byref(center),
        ctypes.byref(et),
        matrix,
        ctypes.byref(next_frame),
    )
    return stypes.c_matrix_to_numpy(matrix), next_frame.value
