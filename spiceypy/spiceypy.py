import ctypes
from .utils import support_types as stypes
from .utils.libspicehelper import libspice
from .utils.callbacks import SpiceUDF
import functools
import numpy

__author__ = 'AndrewAnnex'

################################################################################

_default_len_out = 256


def checkForSpiceError(f):
    """
    Internal function to check
    :param f:
    :raise stypes.SpiceyError:
    """
    if failed():
        errorparts = {
            "tkvsn": tkvrsn("TOOLKIT").replace("CSPICE_", ""),
            "short": getmsg("SHORT", 26),
            "explain": getmsg("EXPLAIN", 100).strip(),
            "long": getmsg("LONG", 321).strip(),
            "traceback": qcktrc(200)}
        msg = stypes.errorformat.format(**errorparts)
        reset()
        raise stypes.SpiceyError(msg)


def spiceErrorCheck(f):
    """
    Decorator for spiceypy hooking into spice error system.
    If an error is detected, an output similar to outmsg

    :type f: builtins.function
    :return:
    :rtype:
    """

    @functools.wraps(f)
    def with_errcheck(*args, **kwargs):
        try:
            res = f(*args, **kwargs)
            checkForSpiceError(f)
            return res
        except:
            raise

    return with_errcheck


def spiceFoundExceptionThrower(f):
    """
    Decorator for wrapping functions that use status codes
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        res = f(*args, **kwargs)
        found = res[-1]
        if isinstance(found, bool) and not found:
            raise stypes.SpiceyError("Spice returns not found for function: {}".format(f.__name__))
        else:
            actualres = res[0:-1]
            if len(actualres) == 1:
                return actualres[0]
            else:
                return actualres
    return wrapper


################################################################################
# A

@spiceErrorCheck
def appndc(item, cell):
    """
    Append an item to a character cell.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/appndc_c.html

    :param item: The item to append.
    :type item: str or list
    :param cell: The cell to append to.
    :type cell: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(cell, stypes.SpiceCell)
    if isinstance(item, list):
        for c in item:
            libspice.appndc_c(stypes.stringToCharP(c), cell)
    else:
        item = stypes.stringToCharP(item)
        libspice.appndc_c(item, cell)


@spiceErrorCheck
def appndd(item, cell):
    """
    Append an item to a double precision cell.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/appndd_c.html

    :param item: The item to append.
    :type item: float or list
    :param cell: The cell to append to.
    :type cell: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(cell, stypes.SpiceCell)
    if hasattr(item, "__iter__"):
        for d in item:
            libspice.appndd_c(ctypes.c_double(d), cell)
    else:
        item = ctypes.c_double(item)
        libspice.appndd_c(item, cell)


@spiceErrorCheck
def appndi(item, cell):
    """
    Append an item to an integer cell.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/appndi_c.html

    :param item: The item to append.
    :type item: int or list
    :param cell: The cell to append to.
    :type cell: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(cell, stypes.SpiceCell)
    if hasattr(item, "__iter__"):
        for i in item:
            libspice.appndi_c(ctypes.c_int(i), cell)
    else:
        item = ctypes.c_int(item)
        libspice.appndi_c(item, cell)


@spiceErrorCheck
def axisar(axis, angle):
    """
    Construct a rotation matrix that rotates vectors by a specified
    angle about a specified axis.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/axisar_c.html

    :param axis: Rotation axis. 
    :type axis: 3 Element vector (list, tuple, numpy array)
    :param angle: Rotation angle, in radians. 
    :type angle: float
    :return: Rotation matrix corresponding to axis and angle.
    :rtype: numpy array ((3, 3))
    """
    axis = stypes.toDoubleVector(axis)
    angle = ctypes.c_double(angle)
    r = stypes.emptyDoubleMatrix()
    libspice.axisar_c(axis, angle, r)
    return stypes.matrixToList(r)


################################################################################
# B

@spiceErrorCheck
def b1900():
    """
    Return the Julian Date corresponding to Besselian Date 1900.0.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/b1900_c.html

    :return: The Julian Date corresponding to Besselian Date 1900.0.
    :rtype: float
    """
    return libspice.b1900_c()


@spiceErrorCheck
def b1950():
    """
    Return the Julian Date corresponding to Besselian Date 1950.0.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/b1950_c.html

    :return: The Julian Date corresponding to Besselian Date 1950.0.
    :rtype: float
    """
    return libspice.b1950_c()


@spiceErrorCheck
def badkpv(caller, name, comp, insize, divby, intype):
    """
    Determine if a kernel pool variable is present and if so
    that it has the correct size and type.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/badkpv_c.html

    :param caller: Name of the routine calling this routine.
    :type caller: str
    :param name: Name of a kernel pool variable.
    :type name: str
    :param comp: Comparison operator.
    :type comp: str
    :param insize: Expected size of the kernel pool variable.
    :type insize: int
    :param divby: A divisor of the size of the kernel pool variable.
    :type divby: int
    :param intype: Expected type of the kernel pool variable
    :type intype: str
    :return: returns false if the kernel pool variable is OK.
    :rtype: bool
    """
    caller = stypes.stringToCharP(caller)
    name = stypes.stringToCharP(name)
    comp = stypes.stringToCharP(comp)
    insize = ctypes.c_int(insize)
    divby = ctypes.c_int(divby)
    intype = ctypes.c_char(intype.encode(encoding='UTF-8'))
    return libspice.badkpv_c(caller, name, comp, insize, divby, intype)


@spiceErrorCheck
def bltfrm(frmcls, outCell=None):
    """
    Return a SPICE set containing the frame IDs of all built-in frames
    of a specified class.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bltfrm_c.html

    :param frmcls: Frame class.
    :type frmcls: int
    :param outCell: Optional SpiceInt Cell that is returned
    :type outCell: spiceypy.utils.support_types.SpiceCell
    :return: Set of ID codes of frames of the specified class.
    :rtype: spiceypy.utils.support_types.SpiceCell
    """
    frmcls = ctypes.c_int(frmcls)
    if not outCell:
        outCell = stypes.SPICEINT_CELL(1000)
    libspice.bltfrm_c(frmcls, outCell)
    return outCell


@spiceErrorCheck
@spiceFoundExceptionThrower
def bodc2n(code, lenout=_default_len_out):
    """
    Translate the SPICE integer code of a body into a common name
    for that body.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodc2n_c.html

    :param code: Integer ID code to be translated into a name.
    :type code: int
    :param lenout: Maximum length of output name.
    :type lenout: int
    :return: A common name for the body identified by code.
    :rtype: str
    """
    code = ctypes.c_int(code)
    name = stypes.stringToCharP(" " * lenout)
    lenout = ctypes.c_int(lenout)
    found = ctypes.c_bool()
    libspice.bodc2n_c(code, lenout, name, ctypes.byref(found))
    return stypes.toPythonString(name), found.value


@spiceErrorCheck
def bodc2s(code, lenout=_default_len_out):
    """
    Translate a body ID code to either the corresponding name or if no
    name to ID code mapping exists, the string representation of the
    body ID value.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodc2s_c.html

    :param code: Integer ID code to translate to a string.
    :type code: int
    :param lenout: Maximum length of output name.
    :type lenout: int
    :return: String corresponding to 'code'.
    :rtype: str
    """
    code = ctypes.c_int(code)
    name = stypes.stringToCharP(" " * lenout)
    lenout = ctypes.c_int(lenout)
    libspice.bodc2s_c(code, lenout, name)
    return stypes.toPythonString(name)


@spiceErrorCheck
def boddef(name, code):
    """
    Define a body name/ID code pair for later translation via
    :func:`bodn2c` or :func:`bodc2n`.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/boddef_c.html

    :param name: Common name of some body.
    :type name: str
    :param code: Integer code for that body.
    :type code: int
    """
    name = stypes.stringToCharP(name)
    code = ctypes.c_int(code)
    libspice.boddef_c(name, code)


@spiceErrorCheck
def bodfnd(body, item):
    """
    Determine whether values exist for some item for any body
    in the kernel pool.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodfnd_c.html

    :param body: ID code of body.
    :type body: int
    :param item: Item to find ("RADII", "NUT_AMP_RA", etc.).
    :type item: str
    :return: True if the item is in the kernel pool, and is False if it is not.
    :rtype: bool
    """
    body = ctypes.c_int(body)
    item = stypes.stringToCharP(item)
    return libspice.bodfnd_c(body, item)


@spiceErrorCheck
@spiceFoundExceptionThrower
def bodn2c(name):
    """
    Translate the name of a body or object to the corresponding SPICE
    integer ID code.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodn2c_c.html

    :param name: Body name to be translated into a SPICE ID code.
    :type name: str
    :return: SPICE integer ID code for the named body.
    :rtype: int
    """
    name = stypes.stringToCharP(name)
    code = ctypes.c_int(0)
    found = ctypes.c_bool(0)
    libspice.bodn2c_c(name, ctypes.byref(code), ctypes.byref(found))
    return code.value, found.value


@spiceErrorCheck
@spiceFoundExceptionThrower
def bods2c(name):
    """
    Translate a string containing a body name or ID code to an integer code.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bods2c_c.html

    :param name: String to be translated to an ID code.
    :type name: str
    :return: Integer ID code corresponding to name.
    :rtype: int
    """
    name = stypes.stringToCharP(name)
    code = ctypes.c_int(0)
    found = ctypes.c_bool(0)
    libspice.bods2c_c(name, ctypes.byref(code), ctypes.byref(found))
    return code.value, found.value


@spiceErrorCheck
def bodvar(body, item, dim):
    """
    Deprecated: This routine has been superseded by :func:`bodvcd` and
    :func:`bodvrd`. This routine is supported for purposes of backward
    compatibility only.

    Return the values of some item for any body in the kernel pool.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodvar_c.html

    :param body: ID code of body.
    :type body: int
    :param item:
                Item for which values are desired,
                ("RADII", "NUT_PREC_ANGLES", etc.)
    :type item: str
    :param dim: Number of values returned.
    :type dim: int
    :return: values
    :rtype: Array of floats
    """
    body = ctypes.c_int(body)
    dim = ctypes.c_int(dim)
    item = stypes.stringToCharP(item)
    values = stypes.emptyDoubleVector(dim.value)
    libspice.bodvar_c(body, item, ctypes.byref(dim), values)
    return stypes.vectorToList(values)


@spiceErrorCheck
def bodvcd(bodyid, item, maxn):
    """
    Fetch from the kernel pool the double precision values of an item
    associated with a body, where the body is specified by an integer ID
    code.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodvcd_c.html

    :param bodyid: Body ID code.
    :type bodyid: int
    :param item:
                Item for which values are desired,
                ("RADII", "NUT_PREC_ANGLES", etc.)
    :type item: str
    :param maxn: Maximum number of values that may be returned.
    :type maxn: int
    :return: dim, values
    :rtype: tuple
    """
    bodyid = ctypes.c_int(bodyid)
    item = stypes.stringToCharP(item)
    dim = ctypes.c_int()
    values = stypes.emptyDoubleVector(maxn)
    maxn = ctypes.c_int(maxn)
    libspice.bodvcd_c(bodyid, item, maxn, ctypes.byref(dim), values)
    return dim.value, stypes.vectorToList(values)


@spiceErrorCheck
def bodvrd(bodynm, item, maxn):
    """
    Fetch from the kernel pool the double precision values
    of an item associated with a body.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodvrd_c.html

    :param bodynm: Body name.
    :type bodynm: str
    :param item:
                Item for which values are desired,
                ("RADII", "NUT_PREC_ANGLES", etc.)
    :type item: str
    :param maxn: Maximum number of values that may be returned.
    :type maxn: int
    :return: tuple of (dim, values)
    :rtype: tuple
    """
    bodynm = stypes.stringToCharP(bodynm)
    item = stypes.stringToCharP(item)
    dim = ctypes.c_int()
    values = stypes.emptyDoubleVector(maxn)
    maxn = ctypes.c_int(maxn)
    libspice.bodvrd_c(bodynm, item, maxn, ctypes.byref(dim), values)
    return dim.value, stypes.vectorToList(values)


@spiceErrorCheck
def brcktd(number, end1, end2):
    """
    Bracket a number. That is, given a number and an acceptable
    interval, make sure that the number is contained in the
    interval. (If the number is already in the interval, leave it
    alone. If not, set it to the nearest endpoint of the interval.)

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/brcktd_c.html

    :param number: Number to be bracketed.
    :type number: float
    :param end1: One of the bracketing endpoints for number.
    :type end1: float
    :param end2: The other bracketing endpoint for number.
    :type end2: float
    :return: value within an interval
    :rtype: float
    """
    number = ctypes.c_double(number)
    end1 = ctypes.c_double(end1)
    end2 = ctypes.c_double(end2)
    return libspice.brcktd_c(number, end1, end2)


@spiceErrorCheck
def brckti(number, end1, end2):
    """
    Bracket a number. That is, given a number and an acceptable
    interval, make sure that the number is contained in the
    interval. (If the number is already in the interval, leave it
    alone. If not, set it to the nearest endpoint of the interval.)

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/brckti_c.html

    :param number: Number to be bracketed.
    :type number: int
    :param end1: One of the bracketing endpoints for number.
    :type end1: int
    :param end2: The other bracketing endpoint for number.
    :type end2: int
    :return: value within an interval
    :rtype: int
    """
    number = ctypes.c_int(number)
    end1 = ctypes.c_int(end1)
    end2 = ctypes.c_int(end2)
    return libspice.brckti_c(number, end1, end2)


@spiceErrorCheck
def bschoc(value, ndim, lenvals, array, order):
    """
    Do a binary search for a given value within a character string array,
    accompanied by an order vector.  Return the index of the matching array
    entry, or -1 if the key value is not found.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bschoc_c.html

    :param value: Key value to be found in array.
    :type value: str
    :param ndim: Dimension of array.
    :type ndim: int
    :param lenvals: String length.
    :type lenvals: int
    :param array: Character string array to search.
    :type array: list of strings
    :param order: Order vector.
    :type order: Array of ints
    :return: index
    :rtype: int
    """
    value = stypes.stringToCharP(value)
    ndim = ctypes.c_int(ndim)
    lenvals = ctypes.c_int(lenvals)
    array = stypes.listToCharArrayPtr(array, xLen=lenvals, yLen=ndim)
    order = stypes.toIntVector(order)
    return libspice.bschoc_c(value, ndim, lenvals, array, order)


@spiceErrorCheck
def bschoi(value, ndim, array, order):
    """
    Do a binary search for a given value within an integer array,
    accompanied by an order vector.  Return the index of the
    matching array entry, or -1 if the key value is not found.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bschoi_c.html

    :param value: Key value to be found in array.
    :type value: int
    :param ndim: Dimension of array.
    :type ndim: int
    :param array: Integer array to search.
    :type array: Array of ints
    :param order: Order vector.
    :type order: Array of ints
    :return: index
    :rtype: int
    """
    value = ctypes.c_int(value)
    ndim = ctypes.c_int(ndim)
    array = stypes.toIntVector(array)
    order = stypes.toIntVector(order)
    return libspice.bschoi_c(value, ndim, array, order)


@spiceErrorCheck
def bsrchc(value, ndim, lenvals, array):
    """
    Do a binary earch for a given value within a character string array.
    Return the index of the first matching array entry, or -1 if the key
    value was not found.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bsrchc_c.html

    :param value: Key value to be found in array.
    :type value: str
    :param ndim: Dimension of array.
    :type ndim: int
    :param lenvals: String length.
    :type lenvals: int
    :param array: Character string array to search.
    :type array: list of strings
    :return: index
    :rtype: int
    """
    value = stypes.stringToCharP(value)
    ndim = ctypes.c_int(ndim)
    lenvals = ctypes.c_int(lenvals)
    array = stypes.listToCharArrayPtr(array, xLen=lenvals, yLen=ndim)
    return libspice.bsrchc_c(value, ndim, lenvals, array)


@spiceErrorCheck
def bsrchd(value, ndim, array):
    """
    Do a binary search for a key value within a double precision array,
    assumed to be in increasing order. Return the index of the matching
    array entry, or -1 if the key value is not found.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bsrchd_c.html

    :param value: Value to find in array.
    :type value: float
    :param ndim: Dimension of array.
    :type ndim: int
    :param array: Array to be searched.
    :type array: Array of floats
    :return: index
    :rtype: int
    """
    value = ctypes.c_double(value)
    ndim = ctypes.c_int(ndim)
    array = stypes.toDoubleVector(array)
    return libspice.bsrchd_c(value, ndim, array)


@spiceErrorCheck
def bsrchi(value, ndim, array):
    """
    Do a binary search for a key value within an integer array,
    assumed to be in increasing order. Return the index of the
    matching array entry, or -1 if the key value is not found.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bsrchi_c.html

    :param value: Value to find in array.
    :type value: int
    :param ndim: Dimension of array.
    :type ndim: int
    :param array: Array to be searched.
    :type array: Array of ints
    :return: index
    :rtype: int
    """
    value = ctypes.c_int(value)
    ndim = ctypes.c_int(ndim)
    array = stypes.toIntVector(array)
    return libspice.bsrchi_c(value, ndim, array)


################################################################################
# C

@spiceErrorCheck
def card(cell):
    """
    Return the cardinality (current number of elements) in a
    cell of any data type.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/card_c.html

    :param cell: Input cell.
    :type cell: spiceypy.utils.support_types.SpiceCell
    :return: the number of elements in a cell of any data type.
    :rtype: int
    """
    return libspice.card_c(ctypes.byref(cell))


@spiceErrorCheck
@spiceFoundExceptionThrower
def ccifrm(frclss, clssid, lenout=_default_len_out):
    """
    Return the frame name, frame ID, and center associated with
    a given frame class and class ID.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ccifrm_c.html

    :param frclss: Class of frame.
    :type frclss: int
    :param clssid: Class ID of frame.
    :type clssid: int
    :param lenout: Maximum length of output string.
    :type lenout: int
    :return:
            the frame name,
            frame ID,
            center.
    :rtype: tuple
    """
    frclss = ctypes.c_int(frclss)
    clssid = ctypes.c_int(clssid)
    lenout = ctypes.c_int(lenout)
    frcode = ctypes.c_int()
    frname = stypes.stringToCharP(lenout)
    center = ctypes.c_int()
    found = ctypes.c_bool()
    libspice.ccifrm_c(frclss, clssid, lenout, ctypes.byref(frcode), frname,
                      ctypes.byref(center), ctypes.byref(found))
    return frcode.value, stypes.toPythonString(
        frname), center.value, found.value


@spiceErrorCheck
def cgv2el(center, vec1, vec2):
    """
    Form a SPICE ellipse from a center vector and two generating vectors.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cgv2el_c.html

    :param center: Center Vector
    :type center: 3-Element Array of floats
    :param vec1: Vector 1
    :type vec1: 3-Element Array of floats
    :param vec2: Vector 2
    :type vec2: 3-Element Array of floats
    :return: Ellipse
    :rtype: spiceypy.utils.support_types.Ellipse
    """
    center = stypes.toDoubleVector(center)
    vec1 = stypes.toDoubleVector(vec1)
    vec2 = stypes.toDoubleVector(vec2)
    ellipse = stypes.Ellipse()
    libspice.cgv2el_c(center, vec1, vec2, ctypes.byref(ellipse))
    return ellipse


@spiceErrorCheck
def chkin(module):
    """
    Inform the SPICE error handling mechanism of entry into a routine.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/chkin_c.html

    :param module: The name of the calling routine.
    :type module: str
    """
    module = stypes.stringToCharP(module)
    libspice.chkin_c(module)


@spiceErrorCheck
def chkout(module):
    """
    Inform the SPICE error handling mechanism of exit from a routine.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/chkout_c.html

    :param module: The name of the calling routine.
    :type module: str
    """
    module = stypes.stringToCharP(module)
    libspice.chkout_c(module)


@spiceErrorCheck
@spiceFoundExceptionThrower
def cidfrm(cent, lenout=_default_len_out):
    """
    Retrieve frame ID code and name to associate with a frame center.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cidfrm_c.html

    :param cent: An object to associate a frame with.
    :type cent: int
    :param lenout: Available space in output string frname.
    :type lenout: int
    :return:
            frame ID code,
            name to associate with a frame center.
    :rtype: tuple
    """
    cent = ctypes.c_int(cent)
    lenout = ctypes.c_int(lenout)
    frcode = ctypes.c_int()
    frname = stypes.stringToCharP(lenout)
    found = ctypes.c_bool()
    libspice.cidfrm_c(cent, lenout, ctypes.byref(frcode), frname,
                      ctypes.byref(found))
    return frcode.value, stypes.toPythonString(frname), found.value


@spiceErrorCheck
def ckcls(handle):
    """
    Close an open CK file.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckcls_c.html

    :param handle: Handle of the CK file to be closed.
    :type handle: int
    """
    handle = ctypes.c_int(handle)
    libspice.ckcls_c(handle)


@spiceErrorCheck
def ckcov(ck, idcode, needav, level, tol, timsys, cover=None):
    """
    Find the coverage window for a specified object in a specified CK file.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckcov_c.html

    :param ck: Name of CK file.
    :type ck: str
    :param idcode: ID code of object.
    :type idcode: int
    :param needav: Flag indicating whether angular velocity is needed.
    :type needav: bool
    :param level: Coverage level: (SEGMENT OR INTERVAL)
    :type level: str
    :param tol: Tolerance in ticks.
    :type tol: float
    :param timsys: Time system used to represent coverage.
    :type timsys: str
    :param cover: Window giving coverage for idcode.
    :type cover: Optional SpiceCell
    :return: coverage window for a specified object in a specified CK file
    :rtype: spiceypy.utils.support_types.SpiceCell
    """
    ck = stypes.stringToCharP(ck)
    idcode = ctypes.c_int(idcode)
    needav = ctypes.c_bool(needav)
    level = stypes.stringToCharP(level)
    tol = ctypes.c_double(tol)
    timsys = stypes.stringToCharP(timsys)
    if not cover:
        cover = stypes.SPICEDOUBLE_CELL(20000)
    assert isinstance(cover, stypes.SpiceCell)
    assert cover.dtype == 1
    libspice.ckcov_c(ck, idcode, needav, level, tol, timsys,
                     ctypes.byref(cover))
    return cover


@spiceErrorCheck
@spiceFoundExceptionThrower
def ckgp(inst, sclkdp, tol, ref):
    """
    Get pointing (attitude) for a specified spacecraft clock time.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckgp_c.html

    :param inst: NAIF ID of instrument, spacecraft, or structure.
    :type inst: int
    :param sclkdp: Encoded spacecraft clock time.
    :type sclkdp: float
    :param tol: Time tolerance.
    :type tol: float
    :param ref: Reference frame.
    :type ref: str
    :return:
            C-matrix pointing data,
            Output encoded spacecraft clock time
    :rtype: tuple
    """
    inst = ctypes.c_int(inst)
    sclkdp = ctypes.c_double(sclkdp)
    tol = ctypes.c_double(tol)
    ref = stypes.stringToCharP(ref)
    cmat = stypes.emptyDoubleMatrix()
    clkout = ctypes.c_double()
    found = ctypes.c_bool()
    libspice.ckgp_c(inst, sclkdp, tol, ref, cmat, ctypes.byref(clkout),
                    ctypes.byref(found))
    return stypes.matrixToList(cmat), clkout.value, found.value


@spiceErrorCheck
@spiceFoundExceptionThrower
def ckgpav(inst, sclkdp, tol, ref):
    """
    Get pointing (attitude) and angular velocity
    for a specified spacecraft clock time.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckgpav_c.html

    :param inst: NAIF ID of instrument, spacecraft, or structure.
    :type inst: int
    :param sclkdp: Encoded spacecraft clock time.
    :type sclkdp: float
    :param tol: Time tolerance.
    :type tol: float
    :param ref: Reference frame.
    :type ref: str
    :return:
            C-matrix pointing data,
            Angular velocity vector,
            Output encoded spacecraft clock time.
    :rtype: tuple
    """
    inst = ctypes.c_int(inst)
    sclkdp = ctypes.c_double(sclkdp)
    tol = ctypes.c_double(tol)
    ref = stypes.stringToCharP(ref)
    cmat = stypes.emptyDoubleMatrix()
    av = stypes.emptyDoubleVector(3)
    clkout = ctypes.c_double()
    found = ctypes.c_bool()
    libspice.ckgpav_c(inst, sclkdp, tol, ref, cmat, av, ctypes.byref(clkout),
                      ctypes.byref(found))
    return stypes.matrixToList(cmat), stypes.vectorToList(
            av), clkout.value, found.value


@spiceErrorCheck
def cklpf(filename):
    """
    Load a CK pointing file for use by the CK readers.  Return that
    file's handle, to be used by other CK routines to refer to the
    file.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cklpf_c.html

    :param filename: Name of the CK file to be loaded.
    :type filename: str
    :return: Loaded file's handle.
    :rtype: int
    """
    filename = stypes.stringToCharP(filename)
    handle = ctypes.c_int()
    libspice.cklpf_c(filename, ctypes.byref(handle))
    return handle.value


@spiceErrorCheck
def ckobj(ck, outCell=None):
    """
    Find the set of ID codes of all objects in a specified CK file.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckobj_c.html

    :param ck: Name of CK file.
    :type ck: str
    :param outCell: Optional user provided Spice Int cell.
    :type outCell: Optional spiceypy.utils.support_types.SpiceCell
    :return: Set of ID codes of objects in CK file.
    :rtype: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(ck, str)
    ck = stypes.stringToCharP(ck)
    if not outCell:
        outCell = stypes.SPICEINT_CELL(1000)
    assert isinstance(outCell, stypes.SpiceCell)
    assert outCell.dtype == 2
    libspice.ckobj_c(ck, ctypes.byref(outCell))
    return outCell


@spiceErrorCheck
def ckopn(filename, ifname, ncomch):
    """
    Open a new CK file, returning the handle of the opened file.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckopn_c.html

    :param filename: The name of the CK file to be opened.
    :type filename: str
    :param ifname: The internal filename for the CK.
    :type ifname: str
    :param ncomch: The number of characters to reserve for comments.
    :type ncomch: int
    :return: The handle of the opened CK file.
    :rtype: int
    """
    filename = stypes.stringToCharP(filename)
    ifname = stypes.stringToCharP(ifname)
    ncomch = ctypes.c_int(ncomch)
    handle = ctypes.c_int()
    libspice.ckopn_c(filename, ifname, ncomch, ctypes.byref(handle))
    return handle.value


@spiceErrorCheck
def ckupf(handle):
    """
    Unload a CK pointing file so that it will no longer be searched
    by the readers.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckupf_c.html

    :param handle: Handle of CK file to be unloaded
    :type handle: int
    """
    handle = ctypes.c_int(handle)
    libspice.ckupf_c(handle)


@spiceErrorCheck
def ckw01(handle, begtim, endtim, inst, ref, avflag, segid, nrec, sclkdp, quats,
          avvs):
    """
    Add a type 1 segment to a C-kernel.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckw01_c.html

    :param handle: Handle of an open CK file.
    :type handle: int
    :param begtim: The beginning encoded SCLK of the segment.
    :type begtim: float
    :param endtim: The ending encoded SCLK of the segment.
    :type endtim: float
    :param inst: The NAIF instrument ID code.
    :type inst: int
    :param ref: The reference frame of the segment.
    :type ref: str
    :param avflag: True if the segment will contain angular velocity.
    :type avflag: bool
    :param segid: Segment identifier.
    :type segid: str
    :param nrec: Number of pointing records.
    :type nrec: int
    :param sclkdp: Encoded SCLK times.
    :type sclkdp: Array of floats
    :param quats: Quaternions representing instrument pointing.
    :type quats: Nx4-Element Array of floats
    :param avvs: Angular velocity vectors.
    :type avvs: Nx3-Element Array of floats
    """
    handle = ctypes.c_int(handle)
    begtim = ctypes.c_double(begtim)
    endtim = ctypes.c_double(endtim)
    inst = ctypes.c_int(inst)
    ref = stypes.stringToCharP(ref)
    avflag = ctypes.c_bool(avflag)
    segid = stypes.stringToCharP(segid)
    sclkdp = stypes.toDoubleVector(sclkdp)
    quats = stypes.toDoubleMatrix(quats)
    avvs = stypes.toDoubleMatrix(avvs)
    nrec = ctypes.c_int(nrec)
    libspice.ckw01_c(handle, begtim, endtim, inst, ref, avflag, segid, nrec,
                     sclkdp, quats, avvs)


@spiceErrorCheck
def ckw02(handle, begtim, endtim, inst, ref, segid, nrec, start, stop, quats,
          avvs, rates):
    """
    Write a type 2 segment to a C-kernel.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckw02_c.html

    :param handle: Handle of an open CK file.
    :type handle: int
    :param begtim: The beginning encoded SCLK of the segment.
    :type begtim: float
    :param endtim: The ending encoded SCLK of the segment.
    :type endtim: float
    :param inst: The NAIF instrument ID code.
    :type inst: int
    :param ref: The reference frame of the segment.
    :type ref: str
    :param segid: Segment identifier.
    :type segid: str
    :param nrec: Number of pointing records.
    :type nrec: int
    :param start: Encoded SCLK interval start times.
    :type start: Array of floats
    :param stop: Encoded SCLK interval stop times.
    :type stop: Array of floats
    :param quats: Quaternions representing instrument pointing.
    :type quats: Nx4-Element Array of floats
    :param avvs: Angular velocity vectors.
    :type avvs: Nx3-Element Array of floats
    :param rates: Number of seconds per tick for each interval.
    :type rates: Array of floats
    """
    handle = ctypes.c_int(handle)
    begtim = ctypes.c_double(begtim)
    endtim = ctypes.c_double(endtim)
    inst = ctypes.c_int(inst)
    ref = stypes.stringToCharP(ref)
    segid = stypes.stringToCharP(segid)
    start = stypes.toDoubleVector(start)
    stop = stypes.toDoubleVector(stop)
    rates = stypes.toDoubleVector(rates)
    quats = stypes.toDoubleMatrix(quats)
    avvs = stypes.toDoubleMatrix(avvs)
    nrec = ctypes.c_int(nrec)
    libspice.ckw02_c(handle, begtim, endtim, inst, ref, segid, nrec, start,
                     stop, quats, avvs, rates)


@spiceErrorCheck
def ckw03(handle, begtim, endtim, inst, ref, avflag, segid, nrec, sclkdp, quats,
          avvs, nints, starts):
    """
    Add a type 3 segment to a C-kernel.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckw03_c.html

    :param handle: Handle of an open CK file.
    :type handle: int
    :param begtim: The beginning encoded SCLK of the segment.
    :type begtim: float
    :param endtim: The ending encoded SCLK of the segment.
    :type endtim: float
    :param inst: The NAIF instrument ID code.
    :type inst: int
    :param ref: The reference frame of the segment.
    :type ref: str
    :param avflag: True if the segment will contain angular velocity.
    :type avflag: bool
    :param segid: Segment identifier.
    :type segid: str
    :param nrec: Number of pointing records.
    :type nrec: int
    :param sclkdp: Encoded SCLK times.
    :type sclkdp: Array of floats
    :param quats: Quaternions representing instrument pointing.
    :type quats: Nx4-Element Array of floats
    :param avvs: Angular velocity vectors.
    :type avvs: Nx3-Element Array of floats
    :param nints: Number of intervals.
    :type nints: int
    :param starts: Encoded SCLK interval start times.
    :type starts: Array of floats
    """
    handle = ctypes.c_int(handle)
    begtim = ctypes.c_double(begtim)
    endtim = ctypes.c_double(endtim)
    inst = ctypes.c_int(inst)
    ref = stypes.stringToCharP(ref)
    avflag = ctypes.c_bool(avflag)
    segid = stypes.stringToCharP(segid)
    sclkdp = stypes.toDoubleVector(sclkdp)
    quats = stypes.toDoubleMatrix(quats)
    avvs = stypes.toDoubleMatrix(avvs)
    nrec = ctypes.c_int(nrec)
    starts = stypes.toDoubleVector(starts)
    nints = ctypes.c_int(nints)
    libspice.ckw03_c(handle, begtim, endtim, inst, ref, avflag, segid, nrec,
                     sclkdp, quats, avvs, nints, starts)


# ckw05, skipping, ck05subtype?


@spiceErrorCheck
def clight():
    """
    Return the speed of light in a vacuum (IAU official value, in km/sec).

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/clight_c.html

    :return: The function returns the speed of light in vacuum (km/sec).
    :rtype: float
    """
    return libspice.clight_c()


@spiceErrorCheck
def clpool():
    """
    Remove all variables from the kernel pool. Watches
    on kernel variables are retained.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/clpool_c.html
    """
    libspice.clpool_c()


@spiceErrorCheck
def cmprss(delim, n, instr, lenout=_default_len_out):
    """
    Compress a character string by removing occurrences of
    more than N consecutive occurrences of a specified
    character.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cmprss_c.html

    :param delim: Delimiter to be compressed.
    :type delim: str
    :param n: Maximum consecutive occurrences of delim.
    :type n: int
    :param instr: Input string.
    :type instr: str
    :param lenout: Optional available space in output string.
    :type lenout: Optional int
    :return: Compressed string.
    :rtype: str
    """
    delim = ctypes.c_char(delim.encode(encoding='UTF-8'))
    n = ctypes.c_int(n)
    instr = stypes.stringToCharP(instr)
    output = stypes.stringToCharP(lenout)
    libspice.cmprss_c(delim, n, instr, lenout, output)
    return stypes.toPythonString(output)


@spiceErrorCheck
@spiceFoundExceptionThrower
def cnmfrm(cname, lenout=_default_len_out):
    """
    Retrieve frame ID code and name to associate with an object.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cnmfrm_c.html

    :param cname: Name of the object to find a frame for.
    :type cname: int
    :param lenout: Maximum length available for frame name.
    :type lenout: int
    :return:
            The ID code of the frame associated with cname,
            The name of the frame with ID frcode.
    :rtype: tuple
    """
    lenout = ctypes.c_int(lenout)
    frname = stypes.stringToCharP(lenout)
    cname = stypes.stringToCharP(cname)
    found = ctypes.c_bool()
    frcode = ctypes.c_int()
    libspice.cnmfrm_c(cname, lenout, ctypes.byref(frcode), frname,
                      ctypes.byref(found))
    return frcode.value, stypes.toPythonString(frname), found.value


@spiceErrorCheck
def conics(elts, et):
    """
    Determine the state (position, velocity) of an orbiting body
    from a set of elliptic, hyperbolic, or parabolic orbital
    elements.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/conics_c.html

    :param elts: Conic elements.
    :type elts: 8-Element Array of floats
    :param et: Input time.
    :type et: float
    :return: State of orbiting body at et.
    :rtype: 6-Element Array of floats
    """
    elts = stypes.toDoubleVector(elts)
    et = ctypes.c_double(et)
    state = stypes.emptyDoubleVector(6)
    libspice.conics_c(elts, et, state)
    return stypes.vectorToList(state)


@spiceErrorCheck
def convrt(x, inunit, outunit):
    """
    Take a measurement X, the units associated with
    X, and units to which X should be converted; return Y
    the value of the measurement in the output units.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/convrt_c.html

    :param x: Number representing a measurement in some units.
    :type x: float
    :param inunit: The units in which x is measured.
    :type inunit: str
    :param outunit: Desired units for the measurement.
    :type outunit: str
    :return: The measurment in the desired units.
    :rtype: float
    """
    x = ctypes.c_double(x)
    inunit = stypes.stringToCharP(inunit)
    outunit = stypes.stringToCharP(outunit)
    y = ctypes.c_double()
    libspice.convrt_c(x, inunit, outunit, ctypes.byref(y))
    return y.value


@spiceErrorCheck
def copy(cell):
    """
    Copy the contents of a SpiceCell of any data type to another
    cell of the same type.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/copy_c.html

    :param cell: Cell to be copied.
    :type cell: spiceypy.utils.support_types.SpiceCell
    :return: New cell
    :rtype: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(cell, stypes.SpiceCell)
    assert cell.dtype == 0 or cell.dtype == 1 or cell.dtype == 2
    if cell.dtype is 0:
        newcopy = stypes.SPICECHAR_CELL(cell.size, cell.length)
    elif cell.dtype is 1:
        newcopy = stypes.SPICEDOUBLE_CELL(cell.size)
    elif cell.dtype is 2:
        newcopy = stypes.SPICEINT_CELL(cell.size)
    else:
        raise NotImplementedError
    libspice.copy_c(ctypes.byref(cell), ctypes.byref(newcopy))
    return newcopy


@spiceErrorCheck
def cpos(string, chars, start):
    """
    Find the first occurrence in a string of a character belonging
    to a collection of characters, starting at a specified location,
    searching forward.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cpos_c.html

    :param string: Any character string.
    :type string: str
    :param chars: A collection of characters.
    :type chars: str
    :param start: Position to begin looking for one of chars.
    :type start: int
    :return:
            The index of the first character of str at or
            following index start that is in the collection chars.
    :rtype: int
    """
    string = stypes.stringToCharP(string)
    chars = stypes.stringToCharP(chars)
    start = ctypes.c_int(start)
    return libspice.cpos_c(string, chars, start)


@spiceErrorCheck
def cposr(string, chars, start):
    """
    Find the first occurrence in a string of a character belonging
    to a collection of characters, starting at a specified location,
    searching in reverse.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cposr_c.html

    :param string: Any character string.
    :type string: str
    :param chars: A collection of characters.
    :type chars: str
    :param start: Position to begin looking for one of chars.
    :type start: int
    :return:
            The index of the last character of str at or
            before index start that is in the collection chars.
    :rtype: int
    """
    string = stypes.stringToCharP(string)
    chars = stypes.stringToCharP(chars)
    start = ctypes.c_int(start)
    return libspice.cposr_c(string, chars, start)


@spiceErrorCheck
def cvpool(agent):
    """
    Indicate whether or not any watched kernel variables that have a
    specified agent on their notification list have been updated.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cvpool_c.html

    :param agent: Name of the agent to check for notices.
    :type agent: str
    :return: True if variables for "agent" have been updated.
    :rtype: bool
    """
    agent = stypes.stringToCharP(agent)
    update = ctypes.c_bool()
    libspice.cvpool_c(agent, ctypes.byref(update))
    return update.value


@spiceErrorCheck
def cyllat(r, lonc, z):
    """
    Convert from cylindrical to latitudinal coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cyllat_c.html

    :param r: Distance of point from z axis.
    :type r: float
    :param lonc: Cylindrical angle of point from XZ plane(radians).
    :type lonc: float
    :param z: Height of point above XY plane.
    :type z: float
    :return: Distance, Longitude (radians), and Latitude of point (radians).
    :rtype: tuple
    """
    r = ctypes.c_double(r)
    lonc = ctypes.c_double(lonc)
    z = ctypes.c_double(z)
    radius = ctypes.c_double()
    lon = ctypes.c_double()
    lat = ctypes.c_double()
    libspice.cyllat_c(r, lonc, z, ctypes.byref(radius), ctypes.byref(lon),
                      ctypes.byref(lat))
    return radius.value, lon.value, lat.value


@spiceErrorCheck
def cylrec(r, lon, z):
    """
    Convert from cylindrical to rectangular coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cylrec_c.html

    :param r: Distance of a point from z axis.
    :type r: float
    :param lon: Angle (radians) of a point from xZ plane.
    :type lon: float
    :param z: Height of a point above xY plane.
    :type z: float
    :return: Rectangular coordinates of the point.
    :rtype: 3-Element Array of floats
    """
    r = ctypes.c_double(r)
    lon = ctypes.c_double(lon)
    z = ctypes.c_double(z)
    rectan = stypes.emptyDoubleVector(3)
    libspice.cylrec_c(r, lon, z, rectan)
    return stypes.vectorToList(rectan)


@spiceErrorCheck
def cylsph(r, lonc, z):
    """
    Convert from cylindrical to spherical coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cylsph_c.html

    :param r: Rectangular coordinates of the point.
    :type r: float
    :param lonc: Angle (radians) of point from XZ plane.
    :type lonc: float
    :param z: Height of point above XY plane.
    :type z: float
    :return:
            Distance of point from origin,
            Polar angle (co-latitude in radians) of point,
            Azimuthal angle (longitude) of point (radians).
    :rtype: tuple
    """
    r = ctypes.c_double(r)
    lonc = ctypes.c_double(lonc)
    z = ctypes.c_double(z)
    radius = ctypes.c_double()
    colat = ctypes.c_double()
    lon = ctypes.c_double()
    libspice.cyllat_c(r, lonc, z, ctypes.byref(radius), ctypes.byref(colat),
                      ctypes.byref(lon))
    return radius.value, colat.value, lon.value


################################################################################
# D

@spiceErrorCheck
def dafac(handle, n, lenvals, buffer):
    # Todo: test dafac
    """
    Add comments from a buffer of character strings to the comment
    area of a binary DAF file, appending them to any comments which
    are already present in the file's comment area.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafac_c.html

    :param handle: handle of a DAF opened with write access.
    :type handle: int
    :param n: Number of comments to put into the comment area.
    :type n: int
    :param lenvals: Length of elements
    :type lenvals: int
    :param buffer: Buffer of comments to put into the comment area.
    :type buffer: Array of str
    """
    handle = ctypes.c_int(handle)
    buffer = stypes.listToCharArrayPtr(buffer)
    n = ctypes.c_int(n)
    lenvals = ctypes.c_int(lenvals)
    libspice.dafac_c(handle, n, lenvals, ctypes.byref(buffer))


@spiceErrorCheck
def dafbbs(handle):
    """
    Begin a backward search for arrays in a DAF.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafbbs_c.html

    :param handle: Handle of DAF to be searched.
    :type handle: int
    """
    handle = ctypes.c_int(handle)
    libspice.dafbbs_c(handle)


@spiceErrorCheck
def dafbfs(handle):
    """
    Begin a forward search for arrays in a DAF.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafbfs_c.html

    :param handle: Handle of file to be searched.
    :type handle: int
    """
    handle = ctypes.c_int(handle)
    libspice.dafbfs_c(handle)


@spiceErrorCheck
def dafcls(handle):
    """
    Close the DAF associated with a given handle.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafcls_c.html

    :param handle: Handle of DAF to be closed.
    :type handle: int
    """
    handle = ctypes.c_int(handle)
    libspice.dafcls_c(handle)


@spiceErrorCheck
def dafcs(handle):
    """
    Select a DAF that already has a search in progress as the
    one to continue searching.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafcs_c.html

    :param handle: Handle of DAF to continue searching.
    :type handle: int
    """
    handle = ctypes.c_int(handle)
    libspice.dafcs_c(handle)


@spiceErrorCheck
def dafdc(handle):
    # Todo: test dafdc
    """
    Delete the entire comment area of a specified DAF file.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafdc_c.html

    :param handle: The handle of a binary DAF opened for writing.
    :type handle: int
    """
    handle = ctypes.c_int(handle)
    libspice.dafcc_c(handle)


@spiceErrorCheck
def dafec(handle, bufsiz, lenout=_default_len_out):
    """
    Extract comments from the comment area of a binary DAF.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafec_c.html

    :param handle: Handle of binary DAF opened with read access.
    :type handle: int
    :param bufsiz: Maximum size, in lines, of buffer.
    :type bufsiz: int
    :param lenout: Length of strings in output buffer.
    :type lenout: int
    :return:
            Number of extracted comment lines,
            buffer where extracted comment lines are placed,
            Indicates whether all comments have been extracted.
    :rtype: tuple
    """
    handle = ctypes.c_int(handle)
    buffer = stypes.charvector(bufsiz, lenout)
    bufsiz = ctypes.c_int(bufsiz)
    lenout = ctypes.c_int(lenout)
    n = ctypes.c_int()
    done = ctypes.c_bool()
    libspice.dafec_c(handle, bufsiz, lenout, ctypes.byref(n),
                     ctypes.byref(buffer), ctypes.byref(done))
    return n.value, stypes.vectorToList(buffer), done.value


@spiceErrorCheck
def daffna():
    """
    Find the next (forward) array in the current DAF.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/daffna_c.html

    :return: True if an array was found.
    :rtype: bool
    """
    found = ctypes.c_bool()
    libspice.daffna_c(ctypes.byref(found))
    return found.value


@spiceErrorCheck
def daffpa():
    """
    Find the previous (backward) array in the current DAF.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/daffpa_c.html

    :return: True if an array was found.
    :rtype: bool
    """
    found = ctypes.c_bool()
    libspice.daffpa_c(ctypes.byref(found))
    return found.value


@spiceErrorCheck
def dafgda(handle, begin, end):
    """
    Read the double precision data bounded by two addresses within a DAF.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafgda_c.html

    :param handle: Handle of a DAF.
    :type handle: int
    :param begin: Initial address within file.
    :type begin: int
    :param end: Final address within file.
    :type end: int
    :return: Data contained between begin and end.
    :rtype: Array of floats
    """
    handle = ctypes.c_int(handle)
    data = stypes.emptyDoubleVector(abs(end - begin))
    begin = ctypes.c_int(begin)
    end = ctypes.c_int(end)
    libspice.dafgda_c(handle, begin, end, data)
    return stypes.vectorToList(data)


@spiceErrorCheck
def dafgh():
    """
    Return (get) the handle of the DAF currently being searched.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafgh_c.html

    :return: Handle for current DAF.
    :rtype: int
    """
    outvalue = ctypes.c_int()
    libspice.dafgh_c(ctypes.byref(outvalue))
    return outvalue.value


@spiceErrorCheck
def dafgn(lenout=_default_len_out):
    """
    Return (get) the name for the current array in the current DAF.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafgn_c.html

    :param lenout: Length of array name string.
    :type lenout: int
    :return: Name of current array.
    :rtype: str
    """
    lenout = ctypes.c_int(lenout)
    name = stypes.stringToCharP(lenout)
    libspice.dafgn_c(lenout, name)
    return stypes.toPythonString(name)


@spiceErrorCheck
def dafgs(n=125):
    # The 125 may be a hard set,
    # I got strange errors that occasionally happend without it
    """
    Return (get) the summary for the current array in the current DAF.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafgs_c.html

    :param n: Optional length N for result Array.
    :return: Summary for current array.
    :rtype: Array of floats
    """
    retarray = stypes.emptyDoubleVector(125)
    # libspice.dafgs_c(ctypes.cast(retarray, ctypes.POINTER(ctypes.c_double)))
    libspice.dafgs_c(retarray)
    return stypes.vectorToList(retarray)[0:n]


@spiceErrorCheck
@spiceFoundExceptionThrower
def dafgsr(handle, recno, begin, end):
    # Todo test dafgsr
    """
    Read a portion of the contents of a summary record in a DAF file.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafgsr_c.html

    :param handle: Handle of DAF.
    :type handle: int
    :param recno: Record number.
    :type recno: int
    :param begin: First word to read from record.
    :type begin: int
    :param end: Last word to read from record.
    :type end: int
    :return: Contents of record.
    :rtype: float
    """
    handle = ctypes.c_int(handle)
    recno = ctypes.c_int(recno)
    begin = ctypes.c_int(begin)
    end = ctypes.c_int(end)
    data = ctypes.c_double()
    found = ctypes.c_bool()
    libspice.dafgsr_c(handle, recno, begin, end, ctypes.byref(data),
                      ctypes.byref(found))
    return data.value, found.value


@spiceErrorCheck
def dafopr(fname):
    """
    Open a DAF for subsequent read requests.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafopr_c.html

    :param fname: Name of DAF to be opened.
    :type fname: str
    :return: Handle assigned to DAF.
    :rtype: int
    """
    fname = stypes.stringToCharP(fname)
    handle = ctypes.c_int()
    libspice.dafopr_c(fname, ctypes.byref(handle))
    return handle.value


@spiceErrorCheck
def dafopw(fname):
    """
    Open a DAF for subsequent write requests.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafopw_c.html

    :param fname: Name of DAF to be opened.
    :type fname: str
    :return: Handle assigned to DAF.
    :rtype: int
    """
    fname = stypes.stringToCharP(fname)
    handle = ctypes.c_int()
    libspice.dafopw_c(fname, ctypes.byref(handle))
    return handle.value


@spiceErrorCheck
def dafps(nd, ni, dc, ic):
    # Todo: test dafps
    """
    Pack (assemble) an array summary from its double precision and
    integer components.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafps_c.html

    :param nd: Number of double precision components.
    :type nd: int
    :param ni: Number of integer components.
    :type ni: int
    :param dc: Double precision components.
    :type dc: Array of floats
    :param ic: Integer components.
    :type ic: Array of ints
    :return: Array summary.
    :rtype: Array of floats
    """
    dc = stypes.toDoubleVector(dc)
    ic = stypes.toIntVector(ic)
    outsum = stypes.emptyDoubleVector(nd + ni)
    nd = ctypes.c_int(nd)
    ni = ctypes.c_int(ni)
    libspice.dafps_c(nd, ni, ctypes.byref(dc), ctypes.byref(ic),
                     ctypes.byref(outsum))
    return stypes.vectorToList(outsum)


@spiceErrorCheck
def dafrda(handle, begin, end):
    # Todo: test dafrda
    """
    Read the double precision data bounded by two addresses within a DAF.

    Deprecated: This routine has been superseded by :func:`dafgda` and
    :func:`dafgsr`.  This routine is supported for purposes of backward
    compatibility only.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafrda_c.html

    :param handle: Handle of a DAF.
    :type handle: int
    :param begin: Initial address within file.
    :type begin: int
    :param end: Final address within file.
    :type end: int
    :return: Data contained between begin and end.
    :rtype: Array of floats
    """
    handle = ctypes.c_int(handle)
    begin = ctypes.c_int(begin)
    end = ctypes.c_int(end)
    data = stypes.emptyDoubleVector(8)  # value of 8 from help file
    libspice.dafrda_c(handle, begin, end, ctypes.byref(data))
    return stypes.vectorToList(data)


@spiceErrorCheck
def dafrfr(handle, lenout=_default_len_out):
    """
    Read the contents of the file record of a DAF.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafrfr_c.html


    :param handle: Handle of an open DAF file.
    :type handle: int
    :param lenout: Available room in the output string
    :type lenout: int
    :return:
            Number of double precision components in summaries,
            Number of integer components in summaries,
            Internal file name, Forward list pointer,
            Backward list pointer, Free address pointer.
    :rtype: tuple
    """
    handle = ctypes.c_int(handle)
    lenout = ctypes.c_int(lenout)
    nd = ctypes.c_int()
    ni = ctypes.c_int()
    ifname = stypes.stringToCharP(lenout)
    fward = ctypes.c_int()
    bward = ctypes.c_int()
    free = ctypes.c_int()
    libspice.dafrfr_c(handle, lenout, ctypes.byref(nd), ctypes.byref(ni),
                      ifname, ctypes.byref(fward), ctypes.byref(bward),
                      ctypes.byref(free))
    return nd.value, ni.value, stypes.toPythonString(
            ifname), fward.value, bward.value, free.value


@spiceErrorCheck
def dafrs(insum):
    # Todo: test dafrs
    """
    Change the summary for the current array in the current DAF.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafrs_c.html

    :param insum: New summary for current array.
    :type insum: Array of floats
    """
    insum = stypes.toDoubleVector(insum)
    libspice.dafrs_c(ctypes.byref(insum))


@spiceErrorCheck
def dafus(insum, nd, ni):
    """
    Unpack an array summary into its double precision and integer components.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dafus_c.html

    :param insum: Array summary.
    :type insum: Array of floats
    :param nd: Number of double precision components.
    :type nd: int
    :param ni: Number of integer components.
    :type ni: int
    :return: Double precision components, Integer components.
    :rtype: tuple
    """
    insum = stypes.toDoubleVector(insum)
    dc = stypes.emptyDoubleVector(nd)
    ic = stypes.emptyIntVector(ni)
    nd = ctypes.c_int(nd)
    ni = ctypes.c_int(ni)
    libspice.dafus_c(insum, nd, ni, dc, ic)
    return stypes.vectorToList(dc), stypes.vectorToList(ic)


@spiceErrorCheck
def dasac(handle, n, buffer, buflen=_default_len_out):
    # Todo: test dasac
    """
    Add comments from a buffer of character strings to the comment
    area of a binary DAS file, appending them to any comments which
    are already present in the file's comment area.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dasac_c.html

    :param handle: DAS handle of a file opened with write access.
    :type handle: int
    :param n: Number of comments to put into the comment area.
    :type n: int
    :param buffer: Buffer of lines to be put into the comment area.
    :type buffer: Array of strs
    :param buflen: Line length associated with buffer.
    :type buflen: int
    :return: :rtype:
    """
    handle = ctypes.c_int(handle)
    # TODO: make this a mutable 2d string array
    buffer = stypes.charvector(n, buflen)
    n = ctypes.c_int(n)
    buflen = ctypes.c_int(buflen)
    libspice.dasac_c(handle, n, buflen, ctypes.byref(buffer))
    return stypes.vectorToList(buffer)


@spiceErrorCheck
def dascls(handle):
    # Todo: test dafdc
    """
    Close a DAS file.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dascls_c.html

    :param handle: Handle of an open DAS file.
    :type handle: int
    """
    handle = ctypes.c_int(handle)
    libspice.dascls_c(handle)


@spiceErrorCheck
def dasec(handle, bufsiz=_default_len_out, buflen=_default_len_out):
    # Todo: test dasec
    """
    Extract comments from the comment area of a binary DAS file.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dasec_c.html

    :param handle: Handle of binary DAS file open with read access.
    :type handle: int
    :param bufsiz: Maximum size, in lines, of buffer.
    :type bufsiz: int
    :param buflen: Line length associated with buffer.
    :type buflen: int
    :return:
            Number of comments extracted from the DAS file,
            Buffer in which extracted comments are placed,
            Indicates whether all comments have been extracted.
    :rtype: tuple
    """
    handle = ctypes.c_int(handle)
    buffer = stypes.charvector(bufsiz, buflen)
    bufsiz = ctypes.c_int(bufsiz)
    buflen = ctypes.c_int(buflen)
    n = ctypes.c_int()
    done = ctypes.c_bool()
    libspice.dafec_c(handle, bufsiz, buflen, ctypes.byref(n),
                     ctypes.byref(buffer), ctypes.byref(done))
    return n.value, stypes.vectorToList(buffer), done.value


@spiceErrorCheck
def dasopr(fname):
    # Todo: test dasopr
    """
    Open a DAS file for reading.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dasopr_c.html

    :param fname: Name of a DAS file to be opened.
    :type fname: str
    :return: Handle assigned to the opened DAS file.
    :rtype: int
    """
    fname = stypes.stringToCharP(fname)
    handle = ctypes.c_int()
    libspice.dasopr_c(fname, ctypes.byref(handle))
    return handle.value


@spiceErrorCheck
def dcyldr(x, y, z):
    """
    This routine computes the Jacobian of the transformation from
    rectangular to cylindrical coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dcyldr_c.html

    :param x: X-coordinate of point.
    :type x: float
    :param y: Y-coordinate of point.
    :type y: float
    :param z: Z-coordinate of point.
    :type z: float
    :return: Matrix of partial derivatives.
    :rtype: 3x3-Element Array of floats
    """
    x = ctypes.c_double(x)
    y = ctypes.c_double(y)
    z = ctypes.c_double(z)
    jacobi = stypes.emptyDoubleMatrix()
    libspice.dcyldr_c(x, y, z, jacobi)
    return stypes.matrixToList(jacobi)


@spiceErrorCheck
def deltet(epoch, eptype):
    """
    Return the value of Delta ET (ET-UTC) for an input epoch.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/deltet_c.html

    :param epoch: Input epoch (seconds past J2000).
    :type epoch: float
    :param eptype: Type of input epoch ("UTC" or "ET").
    :type eptype: str
    :return: Delta ET (ET-UTC) at input epoch.
    :rtype: float
    """
    epoch = ctypes.c_double(epoch)
    eptype = stypes.stringToCharP(eptype)
    delta = ctypes.c_double()
    libspice.deltet_c(epoch, eptype, ctypes.byref(delta))
    return delta.value


@spiceErrorCheck
def det(m1):
    """
    Compute the determinant of a double precision 3x3 matrix.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/det_c.html

    :param m1: Matrix whose determinant is to be found.
    :type m1: 3x3-Element Array of floats
    :return: The determinant of the matrix.
    :rtype: float
    """
    m1 = stypes.listtodoublematrix(m1)
    return libspice.det_c(m1)


@spiceErrorCheck
def dgeodr(x, y, z, re, f):
    """
    This routine computes the Jacobian of the transformation from
    rectangular to geodetic coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dgeodr_c.html

    :param x: X-coordinate of point.
    :type x: float
    :param y: Y-coordinate of point.
    :type y: float
    :param z: Z-coord
    :type z: float
    :param re: Equatorial radius of the reference spheroid.
    :type re: float
    :param f: Flattening coefficient.
    :type f: float
    :return: Matrix of partial derivatives.
    :rtype: 3x3-Element Array of floats
    """
    x = ctypes.c_double(x)
    y = ctypes.c_double(y)
    z = ctypes.c_double(z)
    re = ctypes.c_double(re)
    f = ctypes.c_double(f)
    jacobi = stypes.emptyDoubleMatrix()
    libspice.dgeodr_c(x, y, z, re, f, jacobi)
    return stypes.matrixToList(jacobi)


@spiceErrorCheck
def diags2(symmat):
    """
    Diagonalize a symmetric 2x2 matrix.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/diags2_c.html

    :param symmat: A symmetric 2x2 matrix.
    :type symmat: 2x2-Element Array of floats
    :return:
            A diagonal matrix similar to symmat,
            A rotation used as the similarity transformation.
    :rtype: tuple
    """
    symmat = stypes.listtodoublematrix(symmat, x=2, y=2)
    diag = stypes.emptyDoubleMatrix(x=2, y=2)
    rotateout = stypes.emptyDoubleMatrix(x=2, y=2)
    libspice.diags2_c(symmat, diag, rotateout)
    return stypes.matrixToList(diag), stypes.matrixToList(rotateout)


@spiceErrorCheck
def diff(a, b):
    """
    Take the difference of two sets of any data type to form a third set.
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/diff_c.html

    :param a: First input set.
    :type a: spiceypy.utils.support_types.SpiceCell
    :param b: Second input set.
    :type b: spiceypy.utils.support_types.SpiceCell
    :return: Difference of a and b.
    :rtype: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(a, stypes.SpiceCell)
    assert isinstance(b, stypes.SpiceCell)
    assert a.dtype == b.dtype
    assert a.dtype == 0 or a.dtype == 1 or a.dtype == 2
    if a.dtype is 0:
        c = stypes.SPICECHAR_CELL(max(a.size, b.size), max(a.length, b.length))
    elif a.dtype is 1:
        c = stypes.SPICEDOUBLE_CELL(max(a.size, b.size))
    elif a.dtype is 2:
        c = stypes.SPICEINT_CELL(max(a.size, b.size))
    else:
        raise NotImplementedError
    libspice.diff_c(ctypes.byref(a), ctypes.byref(b), ctypes.byref(c))
    return c


@spiceErrorCheck
def dlatdr(x, y, z):
    """
    This routine computes the Jacobian of the transformation from
    rectangular to latitudinal coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dlatdr_c.html

    :param x: X-coordinate of point.
    :type x: float
    :param y: Y-coordinate of point.
    :type y: float
    :param z: Z-coord
    :type z: float
    :return: Matrix of partial derivatives.
    :rtype: 3x3-Element Array of floats
    """
    x = ctypes.c_double(x)
    y = ctypes.c_double(y)
    z = ctypes.c_double(z)
    jacobi = stypes.emptyDoubleMatrix()
    libspice.dlatdr_c(x, y, z, jacobi)
    return stypes.matrixToList(jacobi)


@spiceErrorCheck
def dp2hx(number, lenout=None):
    """
    Convert a double precision number to an equivalent character
    string using base 16 "scientific notation."

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dp2hx_c.html

    :param number: D.p. number to be converted.
    :type number: float
    :param lenout: Available space for output string.
    :return: Equivalent character string, left justified.
    :rtype: str
    """
    if lenout is None:
        lenout = 255
    number = ctypes.c_double(number)
    lenout = ctypes.c_int(lenout)
    string = stypes.stringToCharP(lenout)
    length = ctypes.c_int()
    libspice.dp2hx_c(number, lenout, string, ctypes.byref(length))
    return stypes.toPythonString(string)


@spiceErrorCheck
def dpgrdr(body, x, y, z, re, f):
    """
    This routine computes the Jacobian matrix of the transformation
    from rectangular to planetographic coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dpgrdr_c.html

    :param body: Body with which coordinate system is associated.
    :type body: str
    :param x: X-coordinate of point.
    :type x: float
    :param y: Y-coordinate of point.
    :type y: float
    :param z: Z-coordinate of point.
    :type z: float
    :param re: Equatorial radius of the reference spheroid.
    :type re: float
    :param f: Flattening coefficient.
    :type f: float
    :return: Matrix of partial derivatives.
    :rtype: 3x3-Element Array of floats
    """
    body = stypes.stringToCharP(body)
    x = ctypes.c_double(x)
    y = ctypes.c_double(y)
    z = ctypes.c_double(z)
    re = ctypes.c_double(re)
    f = ctypes.c_double(f)
    jacobi = stypes.emptyDoubleMatrix()
    libspice.dpgrdr_c(body, x, y, z, re, f, jacobi)
    return stypes.matrixToList(jacobi)


@spiceErrorCheck
def dpmax():
    """
    Return the value of the largest (positive) number representable
    in a double precision variable.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dpmax_c.html

    :return:
            The largest (positive) number representable
            in a double precision variable.
    :rtype: float
    """
    return libspice.dpmax_c()


@spiceErrorCheck
def dpmin():
    """
    Return the value of the smallest (negative) number representable
    in a double precision variable.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dpmin_c.html

    :return:
            The smallest (negative) number that can be represented
            in a double precision variable.
    :rtype: float
    """
    return libspice.dpmin_c()


@spiceErrorCheck
def dpr():
    """
    Return the number of degrees per radian.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dpr_c.html

    :return: The number of degrees per radian.
    :rtype: float
    """
    return libspice.dpr_c()


@spiceErrorCheck
def drdcyl(r, lon, z):
    """
    This routine computes the Jacobian of the transformation from
    cylindrical to rectangular coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/drdcyl_c.html

    :param r: Distance of a point from the origin.
    :type r: float
    :param lon: Angle of the point from the xz plane in radians.
    :type lon: float
    :param z: Height of the point above the xy plane.
    :type z: float
    :return: Matrix of partial derivatives.
    :rtype: 3x3-Element Array of floats
    """
    r = ctypes.c_double(r)
    lon = ctypes.c_double(lon)
    z = ctypes.c_double(z)
    jacobi = stypes.emptyDoubleMatrix()
    libspice.drdcyl_c(r, lon, z, jacobi)
    return stypes.matrixToList(jacobi)


@spiceErrorCheck
def drdgeo(lon, lat, alt, re, f):
    """
    This routine computes the Jacobian of the transformation from
    geodetic to rectangular coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/drdgeo_c.html

    :param lon: Geodetic longitude of point (radians).
    :type lon: float
    :param lat: Geodetic latitude of point (radians).
    :type lat: float
    :param alt: Altitude of point above the reference spheroid.
    :type alt: float
    :param re: Equatorial radius of the reference spheroid.
    :type re: float
    :param f: Flattening coefficient.
    :type f: float
    :return: Matrix of partial derivatives.
    :rtype: 3x3-Element Array of floats
    """
    lon = ctypes.c_double(lon)
    lat = ctypes.c_double(lat)
    alt = ctypes.c_double(alt)
    re = ctypes.c_double(re)
    f = ctypes.c_double(f)
    jacobi = stypes.emptyDoubleMatrix()
    libspice.drdgeo_c(lon, lat, alt, re, f, jacobi)
    return stypes.matrixToList(jacobi)


@spiceErrorCheck
def drdlat(r, lon, lat):
    """
    Compute the Jacobian of the transformation from latitudinal to
    rectangular coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/drdlat_c.html

    :param r: Distance of a point from the origin.
    :type r: float
    :param lon: Angle of the point from the XZ plane in radians.
    :type lon: float
    :param lat: Angle of the point from the XY plane in radians.
    :type lat: float
    :return: Matrix of partial derivatives.
    :rtype: 3x3-Element Array of floats
    """
    r = ctypes.c_double(r)
    lon = ctypes.c_double(lon)
    lat = ctypes.c_double(lat)
    jacobi = stypes.emptyDoubleMatrix()
    libspice.drdsph_c(r, lon, lat, jacobi)
    return stypes.matrixToList(jacobi)


@spiceErrorCheck
def drdpgr(body, lon, lat, alt, re, f):
    """
    This routine computes the Jacobian matrix of the transformation
    from planetographic to rectangular coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/drdpgr_c.html

    :param body: Body with which coordinate system is associated.
    :type body: str
    :param lon: Planetographic longitude of a point (radians).
    :type lon: float
    :param lat: Planetographic latitude of a point (radians).
    :type lat: float
    :param alt: Altitude of a point above reference spheroid.
    :type alt: float
    :param re: Equatorial radius of the reference spheroid.
    :type re: float
    :param f: Flattening coefficient.
    :type f: float
    :return: Matrix of partial derivatives.
    :rtype: 3x3-Element Array of floats
    """
    body = stypes.stringToCharP(body)
    lon = ctypes.c_double(lon)
    lat = ctypes.c_double(lat)
    alt = ctypes.c_double(alt)
    re = ctypes.c_double(re)
    f = ctypes.c_double(f)
    jacobi = stypes.emptyDoubleMatrix()
    libspice.drdpgr_c(body, lon, lat, alt, re, f, jacobi)
    return stypes.matrixToList(jacobi)


@spiceErrorCheck
def drdsph(r, colat, lon):
    """
    This routine computes the Jacobian of the transformation from
    spherical to rectangular coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/drdsph_c.html

    :param r: Distance of a point from the origin.
    :type r: float
    :param colat: Angle of the point from the positive z-axis.
    :type colat: float
    :param lon: Angle of the point from the xy plane.
    :type lon: float
    :return: Matrix of partial derivatives.
    :rtype: 3x3-Element Array of floats
    """
    r = ctypes.c_double(r)
    colat = ctypes.c_double(colat)
    lon = ctypes.c_double(lon)
    jacobi = stypes.emptyDoubleMatrix()
    libspice.drdsph_c(r, colat, lon, jacobi)
    return stypes.matrixToList(jacobi)


@spiceErrorCheck
def dsphdr(x, y, z):
    """
    This routine computes the Jacobian of the transformation from
    rectangular to spherical coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dsphdr_c.html


    :param x: X-coordinate of point.
    :type x: float
    :param y: Y-coordinate of point.
    :type y: float
    :param z: Z-coordinate of point.
    :type z: float
    :return: Matrix of partial derivatives.
    :rtype: 3x3-Element Array of floats
    """
    x = ctypes.c_double(x)
    y = ctypes.c_double(y)
    z = ctypes.c_double(z)
    jacobi = stypes.emptyDoubleMatrix()
    libspice.dsphdr_c(x, y, z, jacobi)
    return stypes.matrixToList(jacobi)


@spiceErrorCheck
@spiceFoundExceptionThrower
def dtpool(name):
    """
    Return the data about a kernel pool variable.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dtpool_c.html

    :param name: Name of the variable whose value is to be returned.
    :type name: str
    :return:
            Number of values returned for name,
            Type of the variable "C", "N", or "X".
    :rtype: tuple
    """
    name = stypes.stringToCharP(name)
    found = ctypes.c_bool()
    n = ctypes.c_int()
    typeout = ctypes.c_char()
    libspice.dtpool_c(name, ctypes.byref(found), ctypes.byref(n),
                      ctypes.byref(typeout))
    return n.value, stypes.toPythonString(typeout.value), found.value


@spiceErrorCheck
def ducrss(s1, s2):
    """
    Compute the unit vector parallel to the cross product of
    two 3-dimensional vectors and the derivative of this unit vector.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ducrss_c.html

    :param s1: Left hand state for cross product and derivative.
    :type s1: 6-Element Array of floats
    :param s2: Right hand state for cross product and derivative.
    :type s2: 6-Element Array of floats
    :return: Unit vector and derivative of the cross product.
    :rtype: 6-Element Array of floats
    """
    assert len(s1) is 6 and len(s2) is 6
    s1 = stypes.toDoubleVector(s1)
    s2 = stypes.toDoubleVector(s2)
    sout = stypes.emptyDoubleVector(6)
    libspice.ducrss_c(s1, s2, sout)
    return stypes.vectorToList(sout)


@spiceErrorCheck
def dvcrss(s1, s2):
    """
    Compute the cross product of two 3-dimensional vectors
    and the derivative of this cross product.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dvcrss_c.html

    :param s1: Left hand state for cross product and derivative.
    :type s1: 6-Element Array of floats
    :param s2: Right hand state for cross product and derivative.
    :type s2: 6-Element Array of floats
    :return: State associated with cross product of positions.
    :rtype: 6-Element Array of floats
    """
    assert len(s1) is 6 and len(s2) is 6
    s1 = stypes.toDoubleVector(s1)
    s2 = stypes.toDoubleVector(s2)
    sout = stypes.emptyDoubleVector(6)
    libspice.dvcrss_c(s1, s2, sout)
    return stypes.vectorToList(sout)


@spiceErrorCheck
def dvdot(s1, s2):
    """
    Compute the derivative of the dot product of two double
    precision position vectors.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dvdot_c.html

    :param s1: First state vector in the dot product.
    :type s1: 6-Element Array of floats
    :param s2: Second state vector in the dot product.
    :type s2: 6-Element Array of floats
    :return: The derivative of the dot product.
    :rtype: float
    """
    assert len(s1) is 6 and len(s2) is 6
    s1 = stypes.toDoubleVector(s1)
    s2 = stypes.toDoubleVector(s2)
    return libspice.dvdot_c(s1, s2)


@spiceErrorCheck
def dvhat(s1):
    """
    Find the unit vector corresponding to a state vector and the
    derivative of the unit vector.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dvhat_c.html

    :param s1: State to be normalized.
    :type s1: 6-Element Array of floats
    :return: Unit vector s1 / abs(s1), and its time derivative.
    :rtype: 6-Element Array of floats
    """
    assert len(s1) is 6
    s1 = stypes.toDoubleVector(s1)
    sout = stypes.emptyDoubleVector(6)
    libspice.dvhat_c(s1, sout)
    return stypes.vectorToList(sout)


@spiceErrorCheck
def dvnorm(state):
    """
    Function to calculate the derivative of the norm of a 3-vector.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dvnorm_c.html

    :param state:
                A 6-vector composed of three coordinates and their derivatives.
    :type state: 6-Element Array of floats
    :return: The derivative of the norm of a 3-vector.
    :rtype: float
    """
    assert len(state) is 6
    state = stypes.toDoubleVector(state)
    return libspice.dvnorm_c(state)


@spiceErrorCheck
def dvpool(name):
    """
    Delete a variable from the kernel pool.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dvpool_c.html

    :param name: Name of the kernel variable to be deleted.
    :type name: str
    """
    name = stypes.stringToCharP(name)
    libspice.dvpool_c(name)


@spiceErrorCheck
def dvsep(s1, s2):
    """
    Calculate the time derivative of the separation angle between
    two input states, S1 and S2.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/dvsep_c.html

    :param s1: State vector of the first body.
    :type s1: 6-Element Array of floats
    :param s2: State vector of the second body.
    :type s2: 6-Element Array of floats
    :return: The time derivative of the angular separation between S1 and S2.
    :rtype: float
    """
    assert len(s1) is 6 and len(s2) is 6
    s1 = stypes.toDoubleVector(s1)
    s2 = stypes.toDoubleVector(s2)
    return libspice.dvsep_c(s1, s2)


################################################################################
# E


@spiceErrorCheck
def edlimb(a, b, c, viewpt):
    """
    Find the limb of a triaxial ellipsoid, viewed from a specified point.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/edlimb_c.html

    :param a: Length of ellipsoid semi-axis lying on the x-axis.
    :type a: float
    :param b: Length of ellipsoid semi-axis lying on the y-axis.
    :type b: float
    :param c: Length of ellipsoid semi-axis lying on the z-axis.
    :type c: float
    :param viewpt: Location of viewing point.
    :type viewpt: 3-Element Array of floats
    :return: Limb of ellipsoid as seen from viewing point.
    :rtype: spiceypy.utils.support_types.Ellipse
    """
    limb = stypes.Ellipse()
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    viewpt = stypes.toDoubleVector(viewpt)
    libspice.edlimb_c(a, b, c, viewpt, ctypes.byref(limb))
    return limb


@spiceErrorCheck
def edterm(trmtyp, source, target, et, fixref, abcorr, obsrvr, npts):
    """
    Compute a set of points on the umbral or penumbral terminator of
    a specified target body, where the target shape is modeled as an
    ellipsoid.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/edterm_c.html

    :param trmtyp: Terminator type.
    :type trmtyp: str
    :param source: Light source.
    :type source: str
    :param target: Target body.
    :type target: str
    :param et: Observation epoch.
    :type et: str
    :param fixref: Body-fixed frame associated with target.
    :type fixref: str
    :param abcorr: Aberration correction.
    :type abcorr: str
    :param obsrvr: Observer.
    :type obsrvr: str
    :param npts: Number of points in terminator set.
    :type npts: int
    :return:
            Epoch associated with target center,
            Position of observer in body-fixed frame,
            Terminator point set.
    :rtype: tuple
    """
    trmtyp = stypes.stringToCharP(trmtyp)
    source = stypes.stringToCharP(source)
    target = stypes.stringToCharP(target)
    et = ctypes.c_double(et)
    fixref = stypes.stringToCharP(fixref)
    abcorr = stypes.stringToCharP(abcorr)
    obsrvr = stypes.stringToCharP(obsrvr)
    trgepc = ctypes.c_double()
    obspos = stypes.emptyDoubleVector(3)
    trmpts = stypes.emptyDoubleMatrix(x=3, y=npts)
    npts = ctypes.c_int(npts)
    libspice.edterm_c(trmtyp, source, target, et, fixref, abcorr, obsrvr, npts,
                      ctypes.byref(trgepc), obspos, trmpts)
    return trgepc.value, stypes.vectorToList(obspos), stypes.matrixToList(
            trmpts)


@spiceErrorCheck
def ekacec(handle, segno, recno, column, nvals, vallen, cvals, isnull):
    """
    Add data to a character column in a specified EK record.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekacec_c.html

    :param handle: EK file handle.
    :type handle: int
    :param segno: Index of segment containing record.
    :type segno: int
    :param recno: Record to which data is to be added.
    :type recno: int
    :param column: Column name.
    :type column: str
    :param nvals: Number of values to add to column.
    :type nvals: int
    :param vallen: Declared length of character values.
    :type vallen: int
    :param cvals: Character values to add to column.
    :type cvals: list of str.
    :param isnull: Flag indicating whether column entry is null.
    :type isnull: bool
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.stringToCharP(column)
    nvals = ctypes.c_int(nvals)
    vallen = ctypes.c_int(vallen)
    cvals = stypes.listToCharArrayPtr(cvals)
    isnull = ctypes.c_bool(isnull)
    libspice.ekacec_c(handle, segno, recno, column, nvals, vallen, cvals,
                      isnull)


@spiceErrorCheck
def ekaced(handle, segno, recno, column, nvals, dvals, isnull):
    """
    Add data to an double precision column in a specified EK record.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekaced_c.html

    :param handle: EK file handle.
    :type handle: int
    :param segno: Index of segment containing record.
    :type segno: int
    :param recno: Record to which data is to be added.
    :type recno: int
    :param column: Column name.
    :type column: str
    :param nvals: Number of values to add to column.
    :type nvals: int
    :param dvals: Double precision values to add to column.
    :type dvals: Array of floats
    :param isnull: Flag indicating whether column entry is null.
    :type isnull: bool
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.stringToCharP(column)
    nvals = ctypes.c_int(nvals)
    dvals = stypes.toDoubleVector(dvals)
    isnull = ctypes.c_bool(isnull)
    libspice.ekaced_c(handle, segno, recno, column, nvals, dvals, isnull)


@spiceErrorCheck
def ekacei(handle, segno, recno, column, nvals, ivals, isnull):
    """
    Add data to an integer column in a specified EK record.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekacei_c.html

    :param handle: EK file handle.
    :type handle: int
    :param segno: Index of segment containing record.
    :type segno: int
    :param recno: Record to which data is to be added.
    :type recno: int
    :param column: Column name.
    :type column: str
    :param nvals: Number of values to add to column.
    :type nvals: int
    :param ivals: Integer values to add to column.
    :type ivals: Array of ints
    :param isnull: Flag indicating whether column entry is null.
    :type isnull: bool
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.stringToCharP(column)
    nvals = ctypes.c_int(nvals)
    ivals = stypes.toIntVector(ivals)
    isnull = ctypes.c_bool(isnull)
    libspice.ekacei_c(handle, segno, recno, column, nvals, ivals, isnull)


@spiceErrorCheck
def ekaclc(handle, segno, column, vallen, cvals, entszs, nlflgs, rcptrs,
           wkindx):
    """
    Add an entire character column to an EK segment.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekaclc_c.html

    :param handle: EK file handle.
    :type handle: int
    :param segno: Number of segment to add column to.
    :type segno: int
    :param column: Column name.
    :type column: str
    :param vallen: Length of character values.
    :type vallen: int
    :param cvals: Character values to add to column.
    :type cvals: list of str.
    :param entszs: Array of sizes of column entries.
    :type entszs: Array of ints
    :param nlflgs: Array of null flags for column entries.
    :type nlflgs: Array of bools
    :param rcptrs: Record pointers for segment.
    :type rcptrs: Array of ints
    :param wkindx: Work space for column index.
    :type wkindx: Array of ints
    :return: Work space for column index.
    :rtype: Array of ints
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    column = stypes.stringToCharP(column)
    vallen = ctypes.c_int(vallen)
    cvals = stypes.listToCharArrayPtr(cvals)
    entszs = stypes.toIntVector(entszs)
    nlflgs = stypes.toBoolVector(nlflgs)
    rcptrs = stypes.toIntVector(rcptrs)
    wkindx = stypes.toIntVector(wkindx)
    libspice.ekaclc_c(handle, segno, column, vallen, cvals, entszs, nlflgs,
                      rcptrs, wkindx)
    return stypes.vectorToList(wkindx)


@spiceErrorCheck
def ekacld(handle, segno, column, dvals, entszs, nlflgs, rcptrs, wkindx):
    """
    Add an entire double precision column to an EK segment.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekacld_c.html

    :param handle: EK file handle.
    :type handle: int
    :param segno: Number of segment to add column to.
    :type segno: int
    :param column: Column name.
    :type column: str
    :param dvals: Double precision values to add to column.
    :type dvals: Array of floats
    :param entszs: Array of sizes of column entries.
    :type entszs: Array of ints
    :param nlflgs: Array of null flags for column entries.
    :type nlflgs: Array of bools
    :param rcptrs: Record pointers for segment.
    :type rcptrs: Array of ints
    :param wkindx: Work space for column index.
    :type wkindx: Array of ints
    :return: Work space for column index.
    :rtype: Array of ints
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    column = stypes.stringToCharP(column)
    dvals = stypes.toDoubleVector(dvals)
    entszs = stypes.toIntVector(entszs)
    nlflgs = stypes.toBoolVector(nlflgs)
    rcptrs = stypes.toIntVector(rcptrs)
    wkindx = stypes.toIntVector(wkindx)
    libspice.ekacld_c(handle, segno, column, dvals, entszs, nlflgs, rcptrs,
                      wkindx)
    return stypes.vectorToList(wkindx)


@spiceErrorCheck
def ekacli(handle, segno, column, ivals, entszs, nlflgs, rcptrs, wkindx):
    """
    Add an entire integer column to an EK segment.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekacli_c.html

    :param handle: EK file handle.
    :type handle: int
    :param segno: Number of segment to add column to.
    :type segno: int
    :param column: Column name.
    :type column: str
    :param ivals: Integer values to add to column.
    :type ivals: Array of ints
    :type entszs: Array of ints
    :param nlflgs: Array of null flags for column entries.
    :type nlflgs: Array of bools
    :param rcptrs: Record pointers for segment.
    :type rcptrs: Array of ints
    :param wkindx: Work space for column index.
    :type wkindx: Array of ints
    :return: Work space for column index.
    :rtype: Array of ints
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    column = stypes.stringToCharP(column)
    ivals = stypes.toIntVector(ivals)
    entszs = stypes.toIntVector(entszs)
    nlflgs = stypes.toBoolVector(nlflgs)
    rcptrs = stypes.toIntVector(rcptrs)
    wkindx = stypes.toIntVector(wkindx)
    libspice.ekacli_c(handle, segno, column, ivals, entszs, nlflgs, rcptrs,
                      wkindx)
    return stypes.vectorToList(wkindx)


@spiceErrorCheck
def ekappr(handle, segno):
    """
    Append a new, empty record at the end of a specified E-kernel segment.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekappr_c.html

    :param handle: File handle.
    :type handle: int
    :param segno: Segment number.
    :type segno: int
    :return: Number of appended record.
    :rtype: int
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int()
    libspice.ekappr_c(handle, segno, ctypes.byref(recno))
    return recno.value


@spiceErrorCheck
def ekbseg(handle, tabnam, ncols, cnmlen, cnames, declen, decls):
    # if 'cnmlen' in kwargs:
    # cnmlen = kwargs['cnmlen']
    # else:
    # cnmlen = len(max(cnames, key=len)) + 1
    # if 'declen' in kwargs:
    #     declen = kwargs['declen']
    # else:
    #     declen = len(max(decls, key=len)) + 1
    # if 'ncols' in kwargs:
    #     ncols = kwargs['ncols']
    # else:
    #     ncols = len(cnames)
    """
    Start a new segment in an E-kernel.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekbseg_c.html

    :param handle: File handle.
    :type handle: int
    :param tabnam: Table name.
    :type tabnam: str
    :param ncols: Number of columns in the segment.
    :type ncols: int
    :param cnmlen: Length of names in in column name array.
    :type cnmlen: int
    :param cnames: Names of columns.
    :type cnames: list of str.
    :param declen: Length of declaration strings in declaration array.
    :type declen: int
    :param decls: Declarations of columns.
    :type decls: list of str.
    :return: Segment number.
    :rtype: int
    """
    handle = ctypes.c_int(handle)
    tabnam = stypes.stringToCharP(tabnam)
    cnmlen = ctypes.c_int(cnmlen)
    cnames = stypes.listToCharArray(cnames)  # not sure if this works
    declen = ctypes.c_int(declen)
    decls = stypes.listToCharArray(decls)
    segno = ctypes.c_int()
    libspice.ekbseg_c(handle, tabnam, ncols, cnmlen, cnames, declen, decls,
                      ctypes.byref(segno))
    return segno.value


@spiceErrorCheck
def ekccnt(table):
    """
    Return the number of distinct columns in a specified,
    currently loaded table.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekccnt_c.html

    :param table: Name of table.
    :type table: str
    :return: Count of distinct, currently loaded columns.
    :rtype: int
    """
    table = stypes.stringToCharP(table)
    ccount = ctypes.c_int()
    libspice.ekccnt_c(table, ctypes.byref(ccount))
    return ccount.value


@spiceErrorCheck
def ekcii(table, cindex, lenout=_default_len_out):
    """
    Return attribute information about a column belonging to a loaded
    EK table, specifying the column by table and index.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekcii_c.html

    :param table: Name of table containing column.
    :type table: str
    :param cindex: Index of column whose attributes are to be found.
    :type cindex: int
    :param lenout: Maximum allowed length of column name.
    :return: Name of column, Column attribute descriptor.
    :rtype: tuple
    """
    table = stypes.stringToCharP(table)
    cindex = ctypes.c_int(cindex)
    lenout = ctypes.c_int(lenout)
    column = stypes.stringToCharP(lenout)
    attdsc = stypes.SpiceEKAttDsc()
    libspice.ekcii_c(table, cindex, lenout, column, ctypes.byref(attdsc))
    return stypes.toPythonString(column), attdsc


@spiceErrorCheck
def ekcls(handle):
    """
    Close an E-kernel.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekcls_c.html

    :param handle: EK file handle.
    :type handle: int
    """
    handle = ctypes.c_int(handle)
    libspice.ekcls_c(handle)


@spiceErrorCheck
def ekdelr(handle, segno, recno):
    """
    Delete a specified record from a specified E-kernel segment.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekdelr_c.html

    :param handle: File handle.
    :type handle: int
    :param segno: Segment number.
    :type segno: int
    :param recno: Record number.
    :type recno: int
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    libspice.ekdelr_c(handle, segno, recno)


@spiceErrorCheck
def ekffld(handle, segno, rcptrs):
    """
    Complete a fast write operation on a new E-kernel segment.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekffld_c.html

    :param handle: File handle.
    :type handle: int
    :param segno: Segment number.
    :type segno: int
    :param rcptrs: Record pointers.
    :type rcptrs: Array of ints
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    rcptrs = stypes.toIntVector(rcptrs)
    libspice.ekffld_c(handle, segno,
                      ctypes.cast(rcptrs, ctypes.POINTER(ctypes.c_int)))


@spiceErrorCheck
def ekfind(query, lenout=_default_len_out):
    """
    Find E-kernel data that satisfy a set of constraints.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekfind_c.html

    :param query: Query specifying data to be found.
    :type query: str
    :param lenout: Declared length of output error message string.
    :type lenout: int
    :return:
            Number of matching rows,
            Flag indicating whether query parsed correctly,
            Parse error description.
    :rtype: tuple
    """
    query = stypes.stringToCharP(query)
    lenout = ctypes.c_int(lenout)
    nmrows = ctypes.c_int()
    error = ctypes.c_bool()
    errmsg = stypes.stringToCharP(lenout)
    libspice.ekfind_c(query, lenout, ctypes.byref(nmrows), ctypes.byref(error),
                      errmsg)
    return nmrows.value, error.value, stypes.toPythonString(errmsg)


@spiceErrorCheck
@spiceFoundExceptionThrower
def ekgc(selidx, row, element, lenout=_default_len_out):
    # ekgc has issues grabbing last element/row in column
    """
    Return an element of an entry in a column of character type in a specified
    row.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekgc_c.html

    :param selidx: Index of parent column in SELECT clause.
    :type selidx: int
    :param row: Row to fetch from.
    :type row: int
    :param element: Index of element, within column entry, to fetch.
    :type element: int
    :param lenout: Maximum length of column element.
    :type lenout: int
    :return:
            Character string element of column entry,
            Flag indicating whether column entry was null.
    :rtype: tuple
    """
    selidx = ctypes.c_int(selidx)
    row = ctypes.c_int(row)
    element = ctypes.c_int(element)
    lenout = ctypes.c_int(lenout)
    null = ctypes.c_bool()
    found = ctypes.c_bool()
    cdata = stypes.stringToCharP(lenout)
    libspice.ekgc_c(selidx, row, element, lenout, cdata, ctypes.byref(null),
                    ctypes.byref(found))
    return stypes.toPythonString(cdata), null.value, found.value


@spiceErrorCheck
@spiceFoundExceptionThrower
def ekgd(selidx, row, element):
    """
    Return an element of an entry in a column of double precision type in a
    specified row.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekgd_c.html

    :param selidx: Index of parent column in SELECT clause.
    :type selidx: int
    :param row: Row to fetch from.
    :type row: int
    :param element: Index of element, within column entry, to fetch.
    :type element: int
    :return:
            Double precision element of column entry,
            Flag indicating whether column entry was null.
    :rtype: tuple
    """
    selidx = ctypes.c_int(selidx)
    row = ctypes.c_int(row)
    element = ctypes.c_int(element)
    ddata = ctypes.c_double()
    null = ctypes.c_bool()
    found = ctypes.c_bool()
    libspice.ekgd_c(selidx, row, element, ctypes.byref(ddata),
                    ctypes.byref(null), ctypes.byref(found))
    return ddata.value, null.value, found.value


@spiceErrorCheck
@spiceFoundExceptionThrower
def ekgi(selidx, row, element):
    """
    Return an element of an entry in a column of integer type in a specified
    row.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekgi_c.html

    :param selidx: Index of parent column in SELECT clause.
    :type selidx: int
    :param row: Row to fetch from.
    :type row: int
    :param element: Index of element, within column entry, to fetch.
    :type element: int
    :return:
            Integer element of column entry,
            Flag indicating whether column entry was null.
    :rtype: tuple
    """
    selidx = ctypes.c_int(selidx)
    row = ctypes.c_int(row)
    element = ctypes.c_int(element)
    idata = ctypes.c_int()
    null = ctypes.c_bool()
    found = ctypes.c_bool()
    libspice.ekgi_c(selidx, row, element, ctypes.byref(idata),
                    ctypes.byref(null), ctypes.byref(found))
    return idata.value, null.value, found.value


@spiceErrorCheck
def ekifld(handle, tabnam, ncols, nrows, cnmlen, cnames, declen, decls):
    """
    Initialize a new E-kernel segment to allow fast writing.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekifld_c.html

    :param handle: File handle.
    :type handle: int
    :param tabnam: Table name.
    :type tabnam: str
    :param ncols: Number of columns in the segment.
    :type ncols: int
    :param nrows: Number of rows in the segment.
    :type nrows: int
    :param cnmlen: Length of names in in column name array.
    :type cnmlen: int
    :param cnames: Names of columns.
    :type cnames: list of str.
    :param declen: Length of declaration strings in declaration array.
    :type declen: int
    :param decls: Declarations of columns.
    :type decls: list of str.
    :return: Segment number, Array of record pointers.
    :rtype: tuple
    """
    handle = ctypes.c_int(handle)
    tabnam = stypes.stringToCharP(tabnam)
    ncols = ctypes.c_int(ncols)
    nrows = ctypes.c_int(nrows)
    cnmlen = ctypes.c_int(cnmlen)
    cnames = stypes.listToCharArray(cnames)
    declen = ctypes.c_int(declen)
    recptrs = stypes.emptyIntVector(nrows)
    decls = stypes.listToCharArray(decls)
    segno = ctypes.c_int()
    libspice.ekifld_c(handle, tabnam, ncols, nrows, cnmlen, cnames, declen,
                      decls, ctypes.byref(segno), recptrs)
    return segno.value, stypes.vectorToList(recptrs)


@spiceErrorCheck
def ekinsr(handle, segno, recno):
    # Todo: test ekinsr
    """
    Add a new, empty record to a specified E-kernel segment at a specified
    index.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekinsr_c.html

    :param handle: File handle.
    :type handle: int
    :param segno: Segment number.
    :type segno: int
    :param recno: Record number.
    :type recno: int
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    libspice.ekinsr_c(handle, segno, recno)


@spiceErrorCheck
def eklef(fname):
    """
    Load an EK file, making it accessible to the EK readers.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/eklef_c.html

    :param fname: Name of EK file to load.
    :type fname: str
    :return: File handle of loaded EK file.
    :rtype: int
    """
    fname = stypes.stringToCharP(fname)
    handle = ctypes.c_int()
    libspice.eklef_c(fname, handle)
    return handle.value


@spiceErrorCheck
def eknelt(selidx, row):
    # Todo: test eknelt
    """
    Return the number of elements in a specified column entry in
    the current row.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/eknelt_c.html

    :param selidx: Index of parent column in SELECT clause.
    :type selidx: int
    :param row: Row containing element.
    :type row: int
    :return: The number of elements in entry in current row.
    :rtype: int
    """
    selidx = ctypes.c_int(selidx)
    row = ctypes.c_int(row)
    return libspice.eknelt_c(selidx, row)


@spiceErrorCheck
def eknseg(handle):
    """
    Return the number of segments in a specified EK.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/eknseg_c.html

    :param handle: EK file handle.
    :type handle: int
    :return: The number of segments in the specified E-kernel.
    :rtype: int
    """
    handle = ctypes.c_int(handle)
    return libspice.eknseg_c(handle)


@spiceErrorCheck
def ekntab():
    """
    Return the number of loaded EK tables.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekntab_c.html

    :return: The number of loaded EK tables.
    :rtype: int
    """
    n = ctypes.c_int(0)
    libspice.ekntab_c(ctypes.byref(n))
    return n.value


@spiceErrorCheck
def ekopn(fname, ifname, ncomch):
    """
    Open a new E-kernel file and prepare the file for writing.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekopn_c.html

    :param fname: Name of EK file.
    :type fname: str
    :param ifname: Internal file name.
    :type ifname: str
    :param ncomch: The number of characters to reserve for comments.
    :type ncomch: int
    :return: Handle attached to new EK file.
    :rtype: int
    """
    fname = stypes.stringToCharP(fname)
    ifname = stypes.stringToCharP(ifname)
    ncomch = ctypes.c_int(ncomch)
    handle = ctypes.c_int()
    libspice.ekopn_c(fname, ifname, ncomch, handle)
    return handle.value


@spiceErrorCheck
def ekopr(fname):
    """
    Open an existing E-kernel file for reading.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekopr_c.html

    :param fname: Name of EK file.
    :type fname: str
    :return: Handle attached to EK file.
    :rtype: int
    """
    fname = stypes.stringToCharP(fname)
    handle = ctypes.c_int()
    libspice.ekopr_c(fname, ctypes.byref(handle))
    return handle.value


@spiceErrorCheck
def ekops():
    """
    Open a scratch (temporary) E-kernel file and prepare the file
    for writing.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekops_c.html

    :return: Handle attached to new EK file.
    :rtype: int
    """
    handle = ctypes.c_int()
    libspice.ekops_c(ctypes.byref(handle))
    return handle.value


@spiceErrorCheck
def ekopw(fname):
    """
    Open an existing E-kernel file for writing.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekopw_c.html

    :param fname: Name of EK file.
    :type fname: str
    :return: Handle attached to EK file.
    :rtype: int
    """
    fname = stypes.stringToCharP(fname)
    handle = ctypes.c_int()
    libspice.ekopw_c(fname, ctypes.byref(handle))
    return handle.value


@spiceErrorCheck
def ekpsel(query, msglen, tablen, collen):
    # Todo: test ekpsel
    """
    Parse the SELECT clause of an EK query, returning full particulars
    concerning each selected item.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekpsel_c.html
    note: oddly docs at url are incomplete/incorrect.

    :param query: EK query.
    :type query: str
    :param msglen: Available space in the output error message string.
    :type msglen: int
    :param tablen: UNKNOWN? Length of Table?
    :type tablen: int
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
    :rtype: tuple
    """
    query = stypes.stringToCharP(query)
    msglen = ctypes.c_int(msglen)
    tablen = ctypes.c_int(tablen)
    collen = ctypes.c_int(collen)
    n = ctypes.c_int()
    xbegs = ctypes.c_int()
    xends = ctypes.c_int()
    xtypes = stypes.SpiceEKDataType()
    xclass = stypes.SpiceEKExprClass()
    tabs = stypes.charvector(100, 33)
    cols = stypes.charvector(100, 65)
    error = ctypes.c_bool()
    errmsg = stypes.stringToCharP(msglen)
    libspice.ekpsel_c(query, msglen, tablen, collen, ctypes.byref(n),
                      ctypes.byref(xbegs), ctypes.byref(xends),
                      ctypes.byref(xtypes), ctypes.byref(xclass),
                      ctypes.byref(tabs), ctypes.byref(cols),
                      ctypes.byref(error), ctypes.byref(errmsg))
    return n.value, xbegs.value, xends.value, xtypes.value, xclass.value, \
           stypes.vectorToList(tabs), stypes.vectorToList(cols), error.value, \
           stypes.toPythonString(errmsg)


@spiceErrorCheck
def ekrcec(handle, segno, recno, column, lenout, nelts=3):
    # Todo: test ekrcec , possible new way to get back 2d char arrays
    """
    Read data from a character column in a specified EK record.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekrcec_c.html

    :param handle: Handle attached to EK file.
    :type handle: int
    :param segno: Index of segment containing record.
    :type segno: int
    :param recno: Record from which data is to be read.
    :type recno: int
    :param column: Column name.
    :type column: str
    :param lenout: Maximum length of output strings.
    :type lenout: int
    :param nelts: ???
    :type nelts: int
    :return:
            Number of values in column entry,
            Character values in column entry,
            Flag indicating whether column entry is null.
    :rtype: tuple
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.stringToCharP(column)
    lenout = ctypes.c_int(lenout)
    nvals = ctypes.c_int()
    cvals = stypes.charvector(ndim=nelts, lenvals=lenout)
    isnull = ctypes.c_bool()
    libspice.ekrcec_c(handle, segno, recno, column, lenout, ctypes.byref(nvals),
                      ctypes.byref(cvals), ctypes.byref(isnull))
    return nvals.value, stypes.vectorToList(cvals), isnull.value


@spiceErrorCheck
def ekrced(handle, segno, recno, column):
    # Todo: test ekrced
    """
    Read data from a double precision column in a specified EK record.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekrced_c.html

    :param handle: Handle attached to EK file.
    :type handle: int
    :param segno: Index of segment containing record.
    :type segno: int
    :param recno: Record from which data is to be read.
    :type recno: int
    :param column: Column name.
    :type column: str
    :return:
            Number of values in column entry,
            Float values in column entry,
            Flag indicating whether column entry is null.
    :rtype: tuple
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.stringToCharP(column)
    nvals = ctypes.c_int()
    dvals = ctypes.POINTER(ctypes.c_double)  # array of length nvals
    isnull = ctypes.c_bool()
    libspice.ekrced_c(handle, segno, recno, column, ctypes.byref(nvals),
                      ctypes.byref(dvals), ctypes.byref(isnull))
    return nvals.value, stypes.vectorToList(dvals), isnull.value


@spiceErrorCheck
def ekrcei(handle, segno, recno, column):
    # Todo: test ekrcei
    """
    Read data from an integer column in a specified EK record.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekrcei_c.html

    :param handle: Handle attached to EK file.
    :type handle: int
    :param segno: Index of segment containing record.
    :type segno: int
    :param recno: Record from which data is to be read.
    :type recno: int
    :param column: Column name.
    :type column: str
    :return:
            Number of values in column entry,
            Integer values in column entry,
            Flag indicating whether column entry is null.
    :rtype: tuple
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.stringToCharP(column)
    nvals = ctypes.c_int()
    ivals = ctypes.pointer(ctypes.c_int)  # array of length nvals
    isnull = ctypes.c_bool()
    libspice.ekrcei_c(handle, segno, recno, column, ctypes.byref(nvals), ivals,
                      ctypes.byref(isnull))
    return nvals.value, stypes.vectorToList(ivals), isnull.value


@spiceErrorCheck
def ekssum(handle, segno):
    """
    Return summary information for a specified segment in a specified EK.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekssum_c.html

    :param handle: Handle of EK.
    :type handle: int
    :param segno: Number of segment to be summarized.
    :type segno: int
    :return: EK segment summary.
    :rtype: spicepy.utils.support_types.SpiceEKSegSum
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    segsum = stypes.SpiceEKSegSum()
    libspice.ekssum_c(handle, segno, ctypes.byref(segsum))
    return segsum


@spiceErrorCheck
def ektnam(n, lenout=_default_len_out):
    """
    Return the name of a specified, loaded table.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ektnam_c.html

    :param n: Index of table.
    :type n: int
    :param lenout: Maximum table name length.
    :type lenout: int
    :return: Name of table.
    :rtype: str
    """
    n = ctypes.c_int(n)
    lenout = ctypes.c_int(lenout)
    table = stypes.stringToCharP(lenout)
    libspice.ektnam_c(n, lenout, table)
    return stypes.toPythonString(table)


@spiceErrorCheck
def ekucec(handle, segno, recno, column, nvals, vallen, cvals, isnull):
    # Todo: test ekucec
    """
    Update a character column entry in a specified EK record.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekucec_c.html

    :param handle: EK file handle.
    :type handle: int
    :param segno: Index of segment containing record.
    :type segno: int
    :param recno: Record to which data is to be updated.
    :type recno: int
    :param column: Column name.
    :type column: str
    :param nvals: Number of values in new column entry.
    :type nvals: int
    :param vallen: Declared length of character values.
    :type vallen: int
    :param cvals: Character values comprising new column entry.
    :type cvals: list of str.
    :param isnull: Flag indicating whether column entry is null.
    :type isnull: bool
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.stringToCharP(column)
    nvals = ctypes.c_int(nvals)
    vallen = ctypes.c_int(vallen)
    isnull = ctypes.c_bool(isnull)
    cvals = stypes.listToCharArrayPtr(cvals, xLen=vallen, yLen=nvals)
    libspice.ekucec_c(handle, segno, recno, column, nvals, vallen, cvals,
                      isnull)


@spiceErrorCheck
def ekuced(handle, segno, recno, column, nvals, dvals, isnull):
    # Todo: test ekucei
    """
    Update a double precision column entry in a specified EK record.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekuced_c.html

    :param handle: EK file handle.
    :type handle: int
    :param segno: Index of segment containing record.
    :type segno: int
    :param recno: Record to which data is to be updated.
    :type recno: int
    :param column: Column name.
    :type column: str
    :param nvals: Number of values in new column entry.
    :type nvals: int
    :param dvals: Double precision values comprising new column entry.
    :type dvals: Array of floats
    :param isnull: Flag indicating whether column entry is null.
    :type isnull: bool
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.stringToCharP(column)
    nvals = ctypes.c_int(nvals)
    isnull = ctypes.c_bool(isnull)
    dvals = stypes.toDoubleVector(dvals)
    libspice.ekuced_c(handle, segno, recno, column, nvals, ctypes.byref(dvals),
                      isnull)


@spiceErrorCheck
def ekucei(handle, segno, recno, column, nvals, ivals, isnull):
    # Todo: test ekucei
    """
    Update an integer column entry in a specified EK record.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekucei_c.html

    :param handle: EK file handle.
    :type handle: int
    :param segno: Index of segment containing record.
    :type segno: int
    :param recno: Record to which data is to be updated.
    :type recno: int
    :param column: Column name.
    :type column: str
    :param nvals: Number of values in new column entry.
    :type nvals: int
    :param ivals: Integer values comprising new column entry.
    :type ivals: Array of ints
    :param isnull: Flag indicating whether column entry is null.
    :type isnull: bool
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.stringToCharP(column)
    nvals = ctypes.c_int(nvals)
    isnull = ctypes.c_bool(isnull)
    ivals = stypes.toIntVector(ivals)
    libspice.ekucei_c(handle, segno, recno, column, nvals, ctypes.byref(ivals),
                      isnull)


@spiceErrorCheck
def ekuef(handle):
    """
    Unload an EK file, making its contents inaccessible to the
    EK reader routines, and clearing space in order to allow other
    EK files to be loaded.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ekuef_c.html

    :param handle: Handle of EK file.
    :type handle: int
    """
    handle = ctypes.c_int(handle)
    libspice.ekuef_c(handle)


@spiceErrorCheck
def el2cgv(ellipse):
    """
    Convert an ellipse to a center vector and two generating
    vectors. The selected generating vectors are semi-axes of the
    ellipse.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/el2cgv_c.html

    :param ellipse: An Ellipse
    :type ellipse: spiceypy.utils.support_types.Ellipse
    :return: Center and semi-axes of ellipse.
    :rtype: tuple
    """
    assert (isinstance(ellipse, stypes.Ellipse))
    center = stypes.emptyDoubleVector(3)
    smajor = stypes.emptyDoubleVector(3)
    sminor = stypes.emptyDoubleVector(3)
    libspice.el2cgv_c(ctypes.byref(ellipse), center, smajor, sminor)
    return stypes.vectorToList(center), stypes.vectorToList(
            smajor), stypes.vectorToList(sminor)


@spiceErrorCheck
def elemc(item, inset):
    """
    Determine whether an item is an element of a character set.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/elemc_c.html

    :param item: Item to be tested.
    :type item: str
    :param inset: Set to be tested.
    :type inset: spiceypy.utils.support_types.SpiceCell
    :return: True if item is an element of set.
    :rtype: bool
    """
    assert isinstance(inset, stypes.SpiceCell)
    item = stypes.stringToCharP(item)
    return libspice.elemc_c(item, ctypes.byref(inset))


@spiceErrorCheck
def elemd(item, inset):
    """
    Determine whether an item is an element of a double precision set.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/elemd_c.html

    :param item: Item to be tested.
    :type item: float
    :param inset: Set to be tested.
    :type inset: spiceypy.utils.support_types.SpiceCell
    :return: True if item is an element of set.
    :rtype: bool
    """
    assert isinstance(inset, stypes.SpiceCell)
    assert inset.dtype == 1
    item = ctypes.c_double(item)
    return libspice.elemd_c(item, ctypes.byref(inset))


@spiceErrorCheck
def elemi(item, inset):
    """
    Determine whether an item is an element of an integer set.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/elemi_c.html

    :param item: Item to be tested.
    :type item: int
    :param inset: Set to be tested.
    :type inset: spiceypy.utils.support_types.SpiceCell
    :return: True if item is an element of set.
    :rtype: bool
    """
    assert isinstance(inset, stypes.SpiceCell)
    assert inset.dtype == 2
    item = ctypes.c_int(item)
    return libspice.elemi_c(item, ctypes.byref(inset))


@spiceErrorCheck
def eqncpv(et, epoch, eqel, rapol, decpol):
    """
    Compute the state (position and velocity of an object whose
    trajectory is described via equinoctial elements relative to some
    fixed plane (usually the equatorial plane of some planet).

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/eqncpv_c.html

    :param et: Epoch in seconds past J2000 to find state.
    :type et: float
    :param epoch: Epoch of elements in seconds past J2000.
    :type epoch: float
    :param eqel: Array of equinoctial elements
    :type eqel: 9-Element Array of floats
    :param rapol: Right Ascension of the pole of the reference plane.
    :type rapol: float
    :param decpol: Declination of the pole of the reference plane.
    :type decpol: float
    :return: State of the object described by eqel.
    :rtype: 6-Element Array of floats
    """
    et = ctypes.c_double(et)
    epoch = ctypes.c_double(epoch)
    eqel = stypes.toDoubleVector(eqel)
    rapol = ctypes.c_double(rapol)
    decpol = ctypes.c_double(decpol)
    state = stypes.emptyDoubleVector(6)
    libspice.eqncpv_c(et, epoch, eqel, rapol, decpol, state)
    return stypes.vectorToList(state)


@spiceErrorCheck
def eqstr(a, b):
    """
    Determine whether two strings are equivalent.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/eqstr_c.html

    :param a: Arbitrary character string.
    :type a: str
    :param b: Arbitrary character string.
    :type b: str
    :return: True if A and B are equivalent.
    :rtype: bool
    """
    return libspice.eqstr_c(stypes.stringToCharP(a), stypes.stringToCharP(b))


def erract(op, lenout, action=None):
    """
    Retrieve or set the default error action.
    spiceypy sets the default error action to "report" on init.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/erract_c.html

    :param op: peration, "GET" or "SET".
    :type op: str
    :param lenout: Length of list for output.
    :type lenout: int
    :param action: Error response action.
    :type action: str
    :return: Error response action.
    :rtype: str
    """
    if action is None:
        action = ""
    lenout = ctypes.c_int(lenout)
    op = stypes.stringToCharP(op)
    action = ctypes.create_string_buffer(str.encode(action), lenout.value)
    actionptr = ctypes.c_char_p(ctypes.addressof(action))
    libspice.erract_c(op, lenout, actionptr)
    return stypes.toPythonString(actionptr)


def errch(marker, string):
    """
    Substitute a character string for the first occurrence of
    a marker in the current long error message.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/errch_c.html

    :param marker: A substring of the error message to be replaced.
    :type marker: str
    :param string: The character string to substitute for marker.
    :type string: str
    """
    marker = stypes.stringToCharP(marker)
    string = stypes.stringToCharP(string)
    libspice.errch_c(marker, string)


def errdev(op, lenout, device):
    """
    Retrieve or set the name of the current output device for error messages.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/errdev_c.html

    :param op: The operation, "GET" or "SET".
    :type op: str
    :param lenout: Length of device for output.
    :type lenout: int
    :param device: The device name.
    :type device: str
    :return: The device name.
    :rtype: str
    """
    lenout = ctypes.c_int(lenout)
    op = stypes.stringToCharP(op)
    device = ctypes.create_string_buffer(str.encode(device), lenout.value)
    deviceptr = ctypes.c_char_p(ctypes.addressof(device))
    libspice.errdev_c(op, lenout, deviceptr)
    return stypes.toPythonString(deviceptr)


def errdp(marker, number):
    """
    Substitute a double precision number for the first occurrence of
    a marker found in the current long error message.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/errdp_c.html

    :param marker: A substring of the error message to be replaced.
    :type marker: str
    :param number: The d.p. number to substitute for marker.
    :type number: float
    """
    marker = stypes.stringToCharP(marker)
    number = ctypes.c_double(number)
    libspice.errdp_c(marker, number)


def errint(marker, number):
    """
    Substitute an integer for the first occurrence of a marker found
    in the current long error message.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/errint_c.html

    :param marker: A substring of the error message to be replaced.
    :type marker: str
    :param number: The integer to substitute for marker.
    :type number: int
    """
    marker = stypes.stringToCharP(marker)
    number = ctypes.c_int(number)
    libspice.errint_c(marker, number)


def errprt(op, lenout, inlist):
    """
    Retrieve or set the list of error message items to be output when an
    error is detected.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/errprt_c.html

    :param op: The operation, "GET" or "SET".
    :type op: str
    :param lenout: Length of list for output.
    :type lenout: int
    :param inlist: Specification of error messages to be output.
    :type inlist: list of str.
    :return: A list of error message items.
    :rtype: list of str.
    """
    lenout = ctypes.c_int(lenout)
    op = stypes.stringToCharP(op)
    inlist = ctypes.create_string_buffer(str.encode(inlist), lenout.value)
    inlistptr = ctypes.c_char_p(ctypes.addressof(inlist))
    libspice.errdev_c(op, lenout, inlistptr)
    return stypes.toPythonString(inlistptr)


def esrchc(value, array):
    """
    Search for a given value within a character string array.
    Return the index of the first equivalent array entry, or -1
    if no equivalent element is found.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/esrchc_c.html

    :param value: Key value to be found in array.
    :type value: str
    :param array: Character string array to search.
    :type array: list of str.
    :return:
            The index of the first array entry equivalent to value,
            or -1 if none is found.
    :rtype: int
    """
    value = stypes.stringToCharP(value)
    ndim = ctypes.c_int(len(array))
    lenvals = ctypes.c_int(len(max(array, key=len)) + 1)
    array = stypes.listToCharArray(array, xLen=lenvals, yLen=ndim)
    return libspice.esrchc_c(value, ndim, lenvals, array)


@spiceErrorCheck
def et2lst(et, body, lon, typein, timlen=_default_len_out, ampmlen=_default_len_out):
    """
    Given an ephemeris epoch, compute the local solar time for
    an object on the surface of a body at a specified longitude.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/et2lst_c.html

    :param et: Epoch in seconds past J2000 epoch.
    :type et: float
    :param body: ID-code of the body of interest.
    :type body: int
    :param lon: Longitude of surface point (RADIANS).
    :type lon: float
    :param typein: Type of longitude "PLANETOCENTRIC", etc.
    :type typein: str
    :param timlen: Available room in output time string.
    :type timlen: int
    :param ampmlen: Available room in output ampm string.
    :type ampmlen: int
    :return:
            Local hour on a "24 hour" clock,
            Minutes past the hour,
            Seconds past the minute,
            String giving local time on 24 hour clock,
            String giving time on A.M. / P.M. scale.
    :rtype: tuple
    """
    et = ctypes.c_double(et)
    body = ctypes.c_int(body)
    lon = ctypes.c_double(lon)
    typein = stypes.stringToCharP(typein)
    timlen = ctypes.c_int(timlen)
    ampmlen = ctypes.c_int(ampmlen)
    hr = ctypes.c_int()
    mn = ctypes.c_int()
    sc = ctypes.c_int()
    time = stypes.stringToCharP(timlen)
    ampm = stypes.stringToCharP(ampmlen)
    libspice.et2lst_c(et, body, lon, typein, timlen, ampmlen,
                      ctypes.byref(hr), ctypes.byref(mn), ctypes.byref(sc),
                      time, ampm)
    return hr.value, mn.value, sc.value, stypes.toPythonString(
            time), stypes.toPythonString(ampm)


@spiceErrorCheck
def et2utc(et, formatStr, prec, lenout=_default_len_out):
    """
    Convert an input time from ephemeris seconds past J2000
    to Calendar, Day-of-Year, or Julian Date format, UTC.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/et2utc_c.html

    :param et: Input epoch, given in ephemeris seconds past J2000.
    :type et: float
    :param formatStr: Format of output epoch.
    :type formatStr: str
    :param prec: Digits of precision in fractional seconds or days.
    :type prec: int
    :param lenout: The length of the output string plus 1.
    :type lenout: int
    :return: Output time string in UTC
    :rtype: str
    """
    et = ctypes.c_double(et)
    prec = ctypes.c_int(prec)
    lenout = ctypes.c_int(lenout)
    formatStr = stypes.stringToCharP(formatStr)
    utcstr = stypes.stringToCharP(lenout)
    libspice.et2utc_c(et, formatStr, prec, lenout, utcstr)
    return stypes.toPythonString(utcstr)


@spiceErrorCheck
def etcal(et, lenout=_default_len_out):
    """
    Convert from an ephemeris epoch measured in seconds past
    the epoch of J2000 to a calendar string format using a
    formal calendar free of leapseconds.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/etcal_c.html

    :param et: Ephemeris time measured in seconds past J2000.
    :type et: float or iterable of float
    :param lenout: Length of output string.
    :type lenout: int
    :return: A standard calendar representation of et.
    :rtype: str
    """
    if hasattr(et, "__iter__"):
        return [etcal(t) for t in et]
    et = ctypes.c_double(et)
    lenout = ctypes.c_int(lenout)
    string = stypes.stringToCharP(lenout)
    libspice.etcal_c(et, lenout, string)
    return stypes.toPythonString(string)


@spiceErrorCheck
def eul2m(angle3, angle2, angle1, axis3, axis2, axis1):
    """
    Construct a rotation matrix from a set of Euler angles.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/eul2m_c.html

    :param angle3: Rotation angle about third rotation axis (radians).
    :type angle3: float
    :param angle2: Rotation angle about second rotation axis (radians).
    :type angle2: float
    :param angle1: Rotation angle about first rotation axis (radians).
    :type angle1: float
    :param axis3: Axis number of third rotation axis.
    :type axis3: int
    :param axis2: Axis number of second rotation axis.
    :type axis2: int
    :param axis1: Axis number of first rotation axis.]
    :type axis1: int
    :return: Product of the 3 rotations.
    :rtype: 3x3-Element Array of floats
    """
    angle3 = ctypes.c_double(angle3)
    angle2 = ctypes.c_double(angle2)
    angle1 = ctypes.c_double(angle1)
    axis3 = ctypes.c_int(axis3)
    axis2 = ctypes.c_int(axis2)
    axis1 = ctypes.c_int(axis1)
    r = stypes.emptyDoubleMatrix()
    libspice.eul2m_c(angle3, angle2, angle1, axis3, axis2, axis1, r)
    return stypes.matrixToList(r)


@spiceErrorCheck
def eul2xf(eulang, axisa, axisb, axisc):
    """
    This routine computes a state transformation from an Euler angle
    factorization of a rotation and the derivatives of those Euler
    angles.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/eul2xf_c.html

    :param eulang: An array of Euler angles and their derivatives.
    :type eulang: 6-Element Array of floats
    :param axisa: Axis A of the Euler angle factorization.
    :type axisa: int
    :param axisb: Axis B of the Euler angle factorization.
    :type axisb: int
    :param axisc: Axis C of the Euler angle factorization.
    :type axisc: int
    :return: A state transformation matrix.
    :rtype: 6x6-Element Array of floats
    """
    assert len(eulang) is 6
    eulang = stypes.toDoubleVector(eulang)
    axisa = ctypes.c_int(axisa)
    axisb = ctypes.c_int(axisb)
    axisc = ctypes.c_int(axisc)
    xform = stypes.emptyDoubleMatrix(x=6, y=6)
    libspice.eul2xf_c(eulang, axisa, axisb, axisc, xform)
    return stypes.matrixToList(xform)


@spiceErrorCheck
def exists(fname):
    """
    Determine whether a file exists.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/exists_c.html

    :param fname: Name of the file in question.
    :return: True if the file exists, False otherwise.
    :rtype: bool
    """
    fname = stypes.stringToCharP(fname)
    return libspice.exists_c(fname)


@spiceErrorCheck
def expool(name):
    """
    Confirm the existence of a kernel variable in the kernel pool.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/expool_c.html

    :param name: Name of the variable whose value is to be returned.
    :type name: str
    :return: True when the variable is in the pool.
    :rtype: bool
    """
    name = stypes.stringToCharP(name)
    found = ctypes.c_bool()
    libspice.expool_c(name, ctypes.byref(found))
    return found.value


################################################################################
# F


def failed():
    """
    True if an error condition has been signalled via sigerr_c.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/failed_c.html

    :return: a boolean
    :rtype: bool
    """
    return libspice.failed_c()


@spiceErrorCheck
def fovray(inst, raydir, rframe, abcorr, observer, et):
    """
    Determine if a specified ray is within the field-of-view (FOV) of a
    specified instrument at a given time.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/fovray_c.html

    :param inst: Name or ID code string of the instrument.
    :type inst: str
    :param raydir: Ray's direction vector.
    :type raydir: 3-Element Array of floats
    :param rframe: Body-fixed, body-centered frame for target body.
    :type rframe: str
    :param abcorr: Aberration correction flag.
    :type abcorr: str
    :param observer: Name or ID code string of the observer.
    :type observer: str
    :param et: Time of the observation (seconds past J2000).
    :type et: float
    :return: Visibility flag
    :rtype: bool
    """
    inst = stypes.stringToCharP(inst)
    raydir = stypes.toDoubleVector(raydir)
    rframe = stypes.stringToCharP(rframe)
    abcorr = stypes.stringToCharP(abcorr)
    observer = stypes.stringToCharP(observer)
    et = ctypes.c_double(et)
    visible = ctypes.c_bool()
    libspice.fovray_c(inst, raydir, rframe, abcorr, observer, ctypes.byref(et),
                      ctypes.byref(visible))
    return visible.value


@spiceErrorCheck
def fovtrg(inst, target, tshape, tframe, abcorr, observer, et):
    """
    Determine if a specified ephemeris object is within the field-of-view (FOV)
    of a specified instrument at a given time.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/fovtrg_c.html

    :param inst: Name or ID code string of the instrument.
    :type inst: str
    :param target: Name or ID code string of the target.
    :type target: str
    :param tshape: Type of shape model used for the target.
    :type tshape: str
    :param tframe: Body-fixed, body-centered frame for target body.
    :type tframe: str
    :param abcorr: Aberration correction flag.
    :type abcorr: str
    :param observer: Name or ID code string of the observer.
    :type observer: str
    :param et: Time of the observation (seconds past J2000).
    :type et: float
    :return: Visibility flag
    :rtype: bool
    """
    inst = stypes.stringToCharP(inst)
    target = stypes.stringToCharP(target)
    tshape = stypes.stringToCharP(tshape)
    tframe = stypes.stringToCharP(tframe)
    abcorr = stypes.stringToCharP(abcorr)
    observer = stypes.stringToCharP(observer)
    et = ctypes.c_double(et)
    visible = ctypes.c_bool()
    libspice.fovtrg_c(inst, target, tshape, tframe, abcorr, observer,
                      ctypes.byref(et), ctypes.byref(visible))
    return visible.value


@spiceErrorCheck
def frame(x):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/frame_c.html

    :param x: Input vector. A parallel unit vector on output.
    :type x: 3-Element Array of floats
    :return: a tuple of 3 list[3]
    :rtype: tuple
    """
    x = stypes.toDoubleVector(x)
    y = stypes.emptyDoubleVector(3)
    z = stypes.emptyDoubleVector(3)
    libspice.frame_c(x, y, z)
    return stypes.vectorToList(x), stypes.vectorToList(y), stypes.vectorToList(
            z)


@spiceErrorCheck
@spiceFoundExceptionThrower
def frinfo(frcode):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/frinfo_c.html

    :param frcode: the idcode for some frame.
    :type frcode: int
    :return: a tuple of attributes associated with the frame.
    :rtype: tuple
    """
    frcode = ctypes.c_int(frcode)
    cent = ctypes.c_int()
    frclss = ctypes.c_int()
    clssid = ctypes.c_int()
    found = ctypes.c_bool()
    libspice.frinfo_c(frcode, ctypes.byref(cent), ctypes.byref(frclss),
                      ctypes.byref(clssid), ctypes.byref(found))
    return cent.value, frclss.value, clssid.value, found.value


@spiceErrorCheck
def frmnam(frcode, lenout=125):
    """
    Retrieve the name of a reference frame associated with a SPICE ID code.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/frmnam_c.html

    :param frcode: an integer code for a reference frame
    :type frcode: int
    :param lenout: Maximum length of output string.
    :type lenout: int
    :return: the name associated with the reference frame.
    :rtype: str
    """
    frcode = ctypes.c_int(frcode)
    lenout = ctypes.c_int(lenout)
    frname = stypes.stringToCharP(lenout)
    libspice.frmnam_c(frcode, lenout, frname)
    return stypes.toPythonString(frname)


@spiceErrorCheck
def ftncls(unit):
    """
    Close a file designated by a Fortran-style integer logical unit.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ftncls_c.html

    :param unit: Fortran-style logical unit.
    :type unit: int
    """
    unit = ctypes.c_int(unit)
    libspice.ftncls_c(unit)


@spiceErrorCheck
def furnsh(path):
    """
    Load one or more SPICE kernels into a program.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/furnsh_c.html

    :param path: one or more paths to kernels
    :type path: str or list of str
    """
    if isinstance(path, list):
        for p in path:
            libspice.furnsh_c(stypes.stringToCharP(p))
    else:
        path = stypes.stringToCharP(path)
        libspice.furnsh_c(path)


################################################################################
# G


@spiceErrorCheck
@spiceFoundExceptionThrower
def gcpool(name, start, room, lenout=_default_len_out):
    """
    Return the character value of a kernel variable from the kernel pool.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gcpool_c.html

    :param name: Name of the variable whose value is to be returned.
    :type name: str
    :param start: Which component to start retrieving for name.
    :type start: int
    :param room: The largest number of values to return.
    :type room: int
    :param lenout: The length of the output string.
    :type lenout: int
    :return: Values associated with name.
    :rtype: list of str
    """
    name = stypes.stringToCharP(name)
    start = ctypes.c_int(start)
    room = ctypes.c_int(room)
    lenout = ctypes.c_int(lenout)
    n = ctypes.c_int()
    cvals = stypes.emptyCharArray(lenout, room)
    found = ctypes.c_bool()
    libspice.gcpool_c(name, start, room, lenout, ctypes.byref(n),
                      ctypes.byref(cvals), ctypes.byref(found))
    return [stypes.toPythonString(x.value) for x in
            cvals[0:n.value]], found.value


@spiceErrorCheck
@spiceFoundExceptionThrower
def gdpool(name, start, room):
    """
    Return the d.p. value of a kernel variable from the kernel pool.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gdpool_c.html

    :param name: Name of the variable whose value is to be returned.
    :type name: str
    :param start: Which component to start retrieving for name.
    :type start: int
    :param room: The largest number of values to return.
    :type room: int
    :return: Values associated with name.
    :rtype: list of float
    """
    name = stypes.stringToCharP(name)
    start = ctypes.c_int(start)
    values = stypes.emptyDoubleVector(room)
    room = ctypes.c_int(room)
    n = ctypes.c_int()
    found = ctypes.c_bool()
    libspice.gdpool_c(name, start, room, ctypes.byref(n),
                      ctypes.cast(values, ctypes.POINTER(ctypes.c_double)),
                      ctypes.byref(found))
    return stypes.vectorToList(values)[0:n.value], found.value


@spiceErrorCheck
def georec(lon, lat, alt, re, f):
    """
    Convert geodetic coordinates to rectangular coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/georec_c.html

    :param lon: Geodetic longitude of point (radians).
    :type lon: float
    :param lat: Geodetic latitude  of point (radians).
    :type lat: float
    :param alt: Altitude of point above the reference spheroid.
    :type alt: float
    :param re: Equatorial radius of the reference spheroid.
    :type re: float
    :param f: Flattening coefficient.
    :type f: float
    :return: Rectangular coordinates of point.
    :rtype: 3-Element Array of floats
    """
    lon = ctypes.c_double(lon)
    lat = ctypes.c_double(lat)
    alt = ctypes.c_double(alt)
    re = ctypes.c_double(re)
    f = ctypes.c_double(f)
    rectan = stypes.emptyDoubleVector(3)
    libspice.georec_c(lon, lat, alt, re, f, rectan)
    return stypes.vectorToList(rectan)


# getcml not really needed


@spiceErrorCheck
def getelm(frstyr, lineln, lines):
    """
    Given a the "lines" of a two-line element set, parse the
    lines and return the elements in units suitable for use
    in SPICE software.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/getelm_c.html

    :param frstyr: Year of earliest representable two-line elements.
    :type frstyr: int
    :param lineln: Length of strings in lines array.
    :type lineln: int
    :param lines: A pair of "lines" containing two-line elements.
    :type lines: list of str
    :return:
            The epoch of the elements in seconds past J2000,
            The elements converted to SPICE units.
    :rtype: tuple
    """
    frstyr = ctypes.c_int(frstyr)
    lineln = ctypes.c_int(lineln)
    lines = stypes.listToCharArrayPtr(lines, xLen=lineln, yLen=2)
    epoch = ctypes.c_double()
    elems = stypes.emptyDoubleVector(10)  # guess for length
    libspice.getelm_c(frstyr, lineln, lines, ctypes.byref(epoch), elems)
    return epoch.value, stypes.vectorToList(elems)


@spiceErrorCheck
def getfat(file):
    """
    Determine the file architecture and file type of most SPICE kernel files.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/getfat_c.html

    :param file: The name of a file to be examined.
    :type file: str
    :return: The architecture of the kernel file, The type of the kernel file.
    :rtype: tuple
    """
    file = stypes.stringToCharP(file)
    arclen = ctypes.c_int(4)
    typlen = ctypes.c_int(4)
    arch = stypes.stringToCharP(arclen)
    rettype = stypes.stringToCharP(typlen)
    libspice.getfat_c(file, arclen, typlen, arch, rettype)
    return stypes.toPythonString(arch), stypes.toPythonString(rettype)


@spiceErrorCheck
def getfov(instid, room, shapelen=_default_len_out, framelen=_default_len_out):
    """
    This routine returns the field-of-view (FOV) parameters for a
    specified instrument.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/getfov_c.html

    :param instid: NAIF ID of an instrument.
    :type instid: int
    :param room: Maximum number of vectors that can be returned.
    :type room: int
    :param shapelen: Space available in the string shape.
    :type shapelen: int
    :param framelen: Space available in the string frame.
    :type framelen: int
    :return:
            Instrument FOV shape,
            Name of the frame in which FOV vectors are defined,
            Boresight vector,
            Number of boundary vectors returned,
            FOV boundary vectors.
    :rtype: tuple
    """
    instid = ctypes.c_int(instid)
    shape = stypes.stringToCharP(" " * shapelen)
    framen = stypes.stringToCharP(" " * framelen)
    shapelen = ctypes.c_int(shapelen)
    framelen = ctypes.c_int(framelen)
    bsight = stypes.emptyDoubleVector(3)
    n = ctypes.c_int()
    bounds = stypes.emptyDoubleMatrix(x=3, y=room)
    room = ctypes.c_int(room)
    libspice.getfov_c(instid, room, shapelen, framelen, shape, framen, bsight,
                      ctypes.byref(n), bounds)
    return stypes.toPythonString(shape), stypes.toPythonString(
            framen), stypes.vectorToList(
            bsight), n.value, stypes.matrixToList(bounds)[0:n.value]


def getmsg(option, lenout=_default_len_out):
    """
    Retrieve the current short error message,
    the explanation of the short error message, or the
    long error message.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/getmsg_c.html

    :param option: Indicates type of error message.
    :type option: str
    :param lenout: Available space in the output string msg.
    :type lenout: int
    :return: The error message to be retrieved.
    :rtype: str
    """
    option = stypes.stringToCharP(option)
    lenout = ctypes.c_int(lenout)
    msg = stypes.stringToCharP(lenout)
    libspice.getmsg_c(option, lenout, msg)
    return stypes.toPythonString(msg)


@spiceErrorCheck
def gfbail():
    """
    Indicate whether an interrupt signal (SIGINT) has been received.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfbail_c.html

    :return: True if an interrupt signal has been received by the GF handler.
    :rtype: bool
    """
    return libspice.gfbail_c()


@spiceErrorCheck
def gfclrh():
    """
    Clear the interrupt signal handler status, so that future calls
    to :func:`gfbail` will indicate no interrupt was received.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfclrh_c.html

    """
    libspice.gfclrh_c()


@spiceErrorCheck
def gfdist(target, abcorr, obsrvr, relate, refval, adjust, step, nintvls,
           cnfine, result):
    """
    Return the time window over which a specified constraint on
    observer-target distance is met.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfdist_c.html

    :param target: Name of the target body.
    :type target: str
    :param abcorr: Aberration correction flag.
    :type abcorr: str
    :param obsrvr: Name of the observing body.
    :type obsrvr: str
    :param relate: Relational operator.
    :type relate: str
    :param refval: Reference value.
    :type refval: float
    :param adjust: Adjustment value for absolute extrema searches.
    :type adjust: float
    :param step: Step size used for locating extrema and roots.
    :type step: float
    :param nintvls: Workspace window interval count.
    :type nintvls: int
    :param cnfine: SPICE window to which the search is confined.
    :type cnfine: spiceypy.utils.support_types.SpiceCell
    :param result: SPICE window containing results.
    :type result: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(cnfine, stypes.SpiceCell)
    assert cnfine.is_double()
    assert isinstance(result, stypes.SpiceCell)
    assert result.is_double()
    target = stypes.stringToCharP(target)
    abcorr = stypes.stringToCharP(abcorr)
    obsrvr = stypes.stringToCharP(obsrvr)
    relate = stypes.stringToCharP(relate)
    refval = ctypes.c_double(refval)
    adjust = ctypes.c_double(adjust)
    step = ctypes.c_double(step)
    nintvls = ctypes.c_int(nintvls)
    libspice.gfdist_c(target, abcorr, obsrvr, relate, refval, adjust,
                      step, nintvls, ctypes.byref(cnfine), ctypes.byref(result))


# gdevnt  callbacks? cells


# gffove  callbacks? cells


@spiceErrorCheck
def gfilum(method, angtyp, target, illumn,
           fixref, abcorr, obsrvr, spoint,
           relate, refval, adjust, step, nintvls, cnfine, result):
    """
    Return the time window over which a specified constraint on
    the observed phase, solar incidence, or emission angle at
    a specifed target body surface point is met.

    :param method: Shape model used to represent the surface of the target body.
    :type method: str
    :param angtyp: The type of illumination angle for which a search is to be performed.
    :type angtyp: str
    :param target: Name of a target body.
    :type target: str
    :param illumn: Name of the illumination source.
    :type illumn: str
    :param fixref: Name of the body-fixed, body-centered reference frame associated with the target body.
    :type fixref: str
    :param abcorr: The aberration corrections to be applied.
    :type abcorr: str
    :param obsrvr: Name of an observing body.
    :type obsrvr: str
    :param spoint: Body-fixed coordinates of a target surface point.
    :type spoint: 3-Element Array of floats
    :param relate: Relational operator used to define a constraint on a specified illumination angle.
    :type relate: str
    :param refval: Reference value used with 'relate' to define an equality or inequality to be satisfied by the specified illumination angle.
    :type refval: float
    :param adjust: Parameter used to modify searches for absolute extrema.
    :type adjust: float
    :param step: Step size to be used in the search.
    :type step: float
    :param nintvls: Number of intervals that can be accommodated by each of the dynamically allocated workspace windows used internally by this routine.
    :type nintvls: int
    :param cnfine: Window that confines the time period over which the specified search is conducted. This can be updated by gfilum
    :type cnfine: spiceypy.utils.support_types.SpiceCell
    :param result: Window of intervals in the confinement window that the illumination angle constraint is satisfied.
    :type result: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(cnfine, stypes.SpiceCell)
    assert isinstance(result, stypes.SpiceCell)
    method = stypes.stringToCharP(method)
    angtyp = stypes.stringToCharP(angtyp)
    target = stypes.stringToCharP(target)
    illumn = stypes.stringToCharP(illumn)
    fixref = stypes.stringToCharP(fixref)
    abcorr = stypes.stringToCharP(abcorr)
    obsrvr = stypes.stringToCharP(obsrvr)
    spoint = stypes.toDoubleVector(spoint)
    relate = stypes.stringToCharP(relate)
    refval = ctypes.c_double(refval)
    adjust = ctypes.c_double(adjust)
    step   = ctypes.c_double(step)
    nintvls = ctypes.c_int(nintvls)
    libspice.gfilum_c(method, angtyp, target, illumn,
                      fixref, abcorr, obsrvr, spoint,
                      relate, refval, adjust, step,
                      nintvls, ctypes.byref(cnfine), ctypes.byref(result))


@spiceErrorCheck
def gfinth(sigcode):
    # Todo: test gfinth
    """
    Respond to the interrupt signal SIGINT: save an indication
    that the signal has been received. This routine restores
    itself as the handler for SIGINT.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfinth_c.html

    :param sigcode: Interrupt signal ID code.
    :type sigcode: int
    """
    sigcode = ctypes.c_int(sigcode)
    libspice.gfinth_c(sigcode)


# gfocce  callbacks? cells


@spiceErrorCheck
def gfoclt(occtyp, front, fshape, fframe, back, bshape, bframe, abcorr, obsrvr,
           step, cnfine, result):
    """
    Determine time intervals when an observer sees one target
    occulted by, or in transit across, another.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfoclt_c.html

    :param occtyp: Type of occultation.
    :type occtyp: str
    :param front: Name of body occulting the other.
    :type front: str
    :param fshape: Type of shape model used for front body.
    :type fshape: str
    :param fframe: Body-fixed, body-centered frame for front body.
    :type fframe: str
    :param back: Name of body occulted by the other.
    :type back: str
    :param bshape: Type of shape model used for back body.
    :type bshape: str
    :param bframe: Body-fixed, body-centered frame for back body.
    :type bframe: str
    :param abcorr: Aberration correction flag.
    :type abcorr: str
    :param obsrvr: Name of the observing body.
    :type obsrvr: str
    :param step: Step size in seconds for finding occultation events.
    :type step: float
    :param cnfine: SPICE window to which the search is restricted.
    :type cnfine: spiceypy.utils.support_types.SpiceCell
    :param result: SPICE window containing results.
    :type result: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(cnfine, stypes.SpiceCell)
    assert cnfine.is_double()
    assert isinstance(result, stypes.SpiceCell)
    assert result.is_double()
    occtyp = stypes.stringToCharP(occtyp)
    front = stypes.stringToCharP(front)
    fshape = stypes.stringToCharP(fshape)
    fframe = stypes.stringToCharP(fframe)
    back = stypes.stringToCharP(back)
    bshape = stypes.stringToCharP(bshape)
    bframe = stypes.stringToCharP(bframe)
    abcorr = stypes.stringToCharP(abcorr)
    obsrvr = stypes.stringToCharP(obsrvr)
    step = ctypes.c_double(step)
    libspice.gfoclt_c(occtyp, front, fshape, fframe, back, bshape, bframe,
                      abcorr, obsrvr, step, ctypes.byref(cnfine),
                      ctypes.byref(result))


@spiceErrorCheck
def gfpa(target, illmin, abcorr, obsrvr, relate, refval, adjust, step, nintvals,
         cnfine, result):
    """
    Determine time intervals for which a specified constraint
    on the phase angle between an illumination source, a target,
    and observer body centers is met.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfpa_c.html

    :param target: Name of the target body.
    :type target: str
    :param illmin: Name of the illuminating body.
    :type illmin: str
    :param abcorr: Aberration correction flag.
    :type abcorr: str
    :param obsrvr: Name of the observing body.
    :type obsrvr: str
    :param relate: Relational operator.
    :type relate: str
    :param refval: Reference value.
    :type refval: float
    :param adjust: Adjustment value for absolute extrema searches.
    :type adjust: float
    :param step: Step size used for locating extrema and roots.
    :type step: float
    :param nintvals: Workspace window interval count.
    :type nintvals: int
    :param cnfine: SPICE window to which the search is restricted.
    :type cnfine: spiceypy.utils.support_types.SpiceCell
    :param result: SPICE window containing results.
    :type result: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(cnfine, stypes.SpiceCell)
    assert cnfine.is_double()
    assert isinstance(result, stypes.SpiceCell)
    assert result.is_double()
    target = stypes.stringToCharP(target)
    illmin = stypes.stringToCharP(illmin)
    abcorr = stypes.stringToCharP(abcorr)
    obsrvr = stypes.stringToCharP(obsrvr)
    relate = stypes.stringToCharP(relate)
    refval = ctypes.c_double(refval)
    adjust = ctypes.c_double(adjust)
    step = ctypes.c_double(step)
    nintvals = ctypes.c_int(nintvals)
    libspice.gfpa_c(target, illmin, abcorr, obsrvr, relate, refval,
                    adjust, step, nintvals, ctypes.byref(cnfine),
                    ctypes.byref(result))


@spiceErrorCheck
def gfposc(target, inframe, abcorr, obsrvr, crdsys, coord, relate, refval,
           adjust, step, nintvals, cnfine, result):
    """
    Determine time intervals for which a coordinate of an
    observer-target position vector satisfies a numerical constraint.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfposc_c.html

    :param target: Name of the target body.
    :type target: str
    :param inframe: Name of the reference frame for coordinate calculations.
    :type inframe: str
    :param abcorr: Aberration correction flag.
    :type abcorr: str
    :param obsrvr: Name of the observing body.
    :type obsrvr: str
    :param crdsys: Name of the coordinate system containing COORD
    :type crdsys: str
    :param coord: Name of the coordinate of interest
    :type coord: str
    :param relate: Relational operator.
    :type relate: str
    :param refval: Reference value.
    :type refval: float
    :param adjust: Adjustment value for absolute extrema searches.
    :type adjust: float
    :param step: Step size used for locating extrema and roots.
    :type step: float
    :param nintvals: Workspace window interval count.
    :type nintvals: int
    :param cnfine: SPICE window to which the search is restricted.
    :type cnfine: spiceypy.utils.support_types.SpiceCell
    :param result: SPICE window containing results.
    :type result: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(cnfine, stypes.SpiceCell)
    assert cnfine.is_double()
    assert isinstance(result, stypes.SpiceCell)
    assert result.is_double()
    target = stypes.stringToCharP(target)
    inframe = stypes.stringToCharP(inframe)
    abcorr = stypes.stringToCharP(abcorr)
    obsrvr = stypes.stringToCharP(obsrvr)
    crdsys = stypes.stringToCharP(crdsys)
    coord = stypes.stringToCharP(coord)
    relate = stypes.stringToCharP(relate)
    refval = ctypes.c_double(refval)
    adjust = ctypes.c_double(adjust)
    step = ctypes.c_double(step)
    nintvals = ctypes.c_int(nintvals)
    libspice.gfposc_c(target, inframe, abcorr, obsrvr, crdsys, coord,
                      relate, refval, adjust, step, nintvals,
                      ctypes.byref(cnfine), ctypes.byref(result))


@spiceErrorCheck
def gfrefn(t1, t2, s1, s2):
    # Todo: test gfrefn
    """
    For those times when we can't do better, we use a bisection
    method to find the next time at which to test for state change.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfrefn_c.html

    :param t1: One of two values bracketing a state change.
    :type t1: float
    :param t2: The other value that brackets a state change.
    :type t2: float
    :param s1: State at t1.
    :type s1: bool
    :param s2: State at t2.
    :type s2: bool
    :return: New value at which to check for transition.
    :rtype: bool
    """
    t1 = ctypes.c_double(t1)
    t2 = ctypes.c_double(t2)
    s1 = ctypes.c_bool(s1)
    s2 = ctypes.c_bool(s2)
    t = ctypes.c_bool()
    libspice.gfrefn_c(t1, t2, s1, s2, ctypes.byref(t))
    return t.value


@spiceErrorCheck
def gfrepf():
    # Todo: test gfrepf
    """
    Finish a GF progress report.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfrepf_c.html

    """
    libspice.gfrepf_c()


@spiceErrorCheck
def gfrepi(window, begmss, endmss):
    # Todo: test gfrepi
    """
    This entry point initializes a search progress report.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfrepi_c.html

    :param window: A window over which a job is to be performed.
    :type window: spiceypy.utils.support_types.SpiceCell
    :param begmss: Beginning of the text portion of the output message.
    :type begmss: str
    :param endmss: End of the text portion of the output message.
    :type endmss: str
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.is_double()
    begmss = stypes.stringToCharP(begmss)
    endmss = stypes.stringToCharP(endmss)
    libspice.gfrepi_c(ctypes.byref(window), begmss, endmss)


@spiceErrorCheck
def gfrepu(ivbeg, ivend, time):
    # Todo: test gfrepu
    """
    This function tells the progress reporting system
    how far a search has progressed.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfrepu_c.html

    :param ivbeg: Start time of work interval.
    :type ivbeg: float
    :param ivend: End time of work interval.
    :type ivend: float
    :param time: Current time being examined in the search process.
    :type time: float
    """
    ivbeg = ctypes.c_double(ivbeg)
    ivend = ctypes.c_double(ivend)
    time = ctypes.c_double(time)
    libspice.gfrepu_c(ivbeg, ivend, time)


@spiceErrorCheck
def gfrfov(inst, raydir, rframe, abcorr, obsrvr, step, cnfine, result):
    """
    Determine time intervals when a specified ray intersects the
    space bounded by the field-of-view (FOV) of a specified
    instrument.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfrfov_c.html

    :param inst: Name of the instrument.
    :type inst: str
    :param raydir: Ray's direction vector.
    :type raydir: 3-Element Array of Float.
    :param rframe: Reference frame of ray's direction vector.
    :type rframe: str
    :param abcorr: Aberration correction flag.
    :type abcorr: str
    :param obsrvr: Name of the observing body.
    :type obsrvr: str
    :param step: Step size in seconds for finding FOV events.
    :type step: float
    :param cnfine: SPICE window to which the search is restricted.
    :type cnfine: spiceypy.utils.support_types.SpiceCell
    :param result: SPICE window containing results.
    :type result: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(cnfine, stypes.SpiceCell)
    assert cnfine.is_double()
    assert isinstance(result, stypes.SpiceCell)
    assert result.is_double()
    inst = stypes.stringToCharP(inst)
    raydir = stypes.toDoubleVector(raydir)
    rframe = stypes.stringToCharP(rframe)
    abcorr = stypes.stringToCharP(abcorr)
    obsrvr = stypes.stringToCharP(obsrvr)
    step = ctypes.c_double(step)
    libspice.gfrfov_c(inst, raydir, rframe, abcorr, obsrvr, step,
                      ctypes.byref(cnfine), ctypes.byref(result))


@spiceErrorCheck
def gfrr(target, abcorr, obsrvr, relate, refval, adjust, step, nintvals, cnfine,
         result):
    """
    Determine time intervals for which a specified constraint
    on the observer-target range rate is met.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfrr_c.html

    :param target: Name of the target body.
    :type target: str
    :param abcorr: Aberration correction flag.
    :type abcorr: str
    :param obsrvr: Name of the observing body.
    :type obsrvr: str
    :param relate: Relational operator.
    :type relate: str
    :param refval: Reference value.
    :type refval: float
    :param adjust: Adjustment value for absolute extrema searches.
    :type adjust: float
    :param step: Step size used for locating extrema and roots.
    :type step: float
    :param nintvals: Workspace window interval count.
    :type nintvals: int
    :param cnfine: SPICE window to which the search is restricted.
    :type cnfine: spiceypy.utils.support_types.SpiceCell
    :param result: SPICE window containing results.
    :type result: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(cnfine, stypes.SpiceCell)
    assert cnfine.is_double()
    assert isinstance(result, stypes.SpiceCell)
    assert result.is_double()
    target = stypes.stringToCharP(target)
    abcorr = stypes.stringToCharP(abcorr)
    obsrvr = stypes.stringToCharP(obsrvr)
    relate = stypes.stringToCharP(relate)
    refval = ctypes.c_double(refval)
    adjust = ctypes.c_double(adjust)
    step = ctypes.c_double(step)
    nintvals = ctypes.c_int(nintvals)
    libspice.gfrr_c(target, abcorr, obsrvr, relate, refval,
                    adjust, step, nintvals, ctypes.byref(cnfine),
                    ctypes.byref(result))


@spiceErrorCheck
def gfsep(targ1, shape1, inframe1, targ2, shape2, inframe2, abcorr, obsrvr,
          relate, refval, adjust, step, nintvals, cnfine, result):
    """
    Determine time intervals when the angular separation between
    the position vectors of two target bodies relative to an observer
    satisfies a numerical relationship.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfsep_c.html

    :param targ1: Name of first body.
    :type targ1: str
    :param shape1: Name of shape model describing the first body.
    :type shape1: str
    :param inframe1: The body-fixed reference frame of the first body.
    :type inframe1: str
    :param targ2: Name of second body.
    :type targ2: str
    :param shape2: Name of the shape model describing the second body.
    :type shape2: str
    :param inframe2: The body-fixed reference frame of the second body
    :type inframe2: str
    :param abcorr: Aberration correction flag
    :type abcorr: str
    :param obsrvr: Name of the observing body.
    :type obsrvr: str
    :param relate: Relational operator.
    :type relate: str
    :param refval: Reference value.
    :type refval: float
    :param adjust: Absolute extremum adjustment value.
    :type adjust: float
    :param step: Step size in seconds for finding angular separation events.
    :type step: float
    :param nintvals: Workspace window interval count.
    :type nintvals: int
    :param cnfine: SPICE window to which the search is restricted.
    :type cnfine: spiceypy.utils.support_types.SpiceCell
    :param result: SPICE window containing results.
    :type result: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(cnfine, stypes.SpiceCell)
    assert cnfine.is_double()
    assert isinstance(result, stypes.SpiceCell)
    assert result.is_double()
    targ1 = stypes.stringToCharP(targ1)
    shape1 = stypes.stringToCharP(shape1)
    inframe1 = stypes.stringToCharP(inframe1)
    targ2 = stypes.stringToCharP(targ2)
    shape2 = stypes.stringToCharP(shape2)
    inframe2 = stypes.stringToCharP(inframe2)
    abcorr = stypes.stringToCharP(abcorr)
    obsrvr = stypes.stringToCharP(obsrvr)
    relate = stypes.stringToCharP(relate)
    refval = ctypes.c_double(refval)
    adjust = ctypes.c_double(adjust)
    step = ctypes.c_double(step)
    nintvals = ctypes.c_int(nintvals)
    libspice.gfsep_c(targ1, shape1, inframe1, targ2, shape2, inframe2,
                     abcorr, obsrvr, relate, refval, adjust, step, nintvals,
                     ctypes.byref(cnfine), ctypes.byref(result))


@spiceErrorCheck
def gfsntc(target, fixref, method, abcorr, obsrvr, dref, dvec, crdsys, coord,
           relate, refval, adjust, step, nintvals,
           cnfine, result):
    """
    Determine time intervals for which a coordinate of an
    surface intercept position vector satisfies a numerical constraint.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfsntc_c.html

    :param target: Name of the target body.
    :type target: str
    :param fixref: Body fixed frame associated with the target.
    :type fixref: str
    :param method: Name of method type for surface intercept calculation.
    :type method: str
    :param abcorr: Aberration correction flag
    :type abcorr: str
    :param obsrvr: Name of the observing body.
    :type obsrvr: str
    :param dref: Reference frame of direction vector of dvec.
    :type dref: str
    :param dvec: Pointing direction vector from the observer.
    :type dvec: 3-Element Array of floats
    :param crdsys: Name of the coordinate system containing COORD.
    :type crdsys: str
    :param coord: Name of the coordinate of interest
    :type coord: str
    :param relate: Relational operator.
    :type relate: str
    :param refval: Reference value.
    :type refval: float
    :param adjust: Absolute extremum adjustment value.
    :type adjust: float
    :param step: Step size in seconds for finding angular separation events.
    :type step: float
    :param nintvals: Workspace window interval count.
    :type nintvals: int
    :param cnfine: SPICE window to which the search is restricted.
    :type cnfine: spiceypy.utils.support_types.SpiceCell
    :param result: SPICE window containing results.
    :type result: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(cnfine, stypes.SpiceCell)
    assert cnfine.is_double()
    assert isinstance(result, stypes.SpiceCell)
    assert result.is_double()
    target = stypes.stringToCharP(target)
    fixref = stypes.stringToCharP(fixref)
    method = stypes.stringToCharP(method)
    abcorr = stypes.stringToCharP(abcorr)
    obsrvr = stypes.stringToCharP(obsrvr)
    dref = stypes.stringToCharP(dref)
    dvec = stypes.toDoubleVector(dvec)
    crdsys = stypes.stringToCharP(crdsys)
    coord = stypes.stringToCharP(coord)
    relate = stypes.stringToCharP(relate)
    refval = ctypes.c_double(refval)
    adjust = ctypes.c_double(adjust)
    step = ctypes.c_double(step)
    nintvals = ctypes.c_int(nintvals)
    libspice.gfsntc_c(target, fixref, method, abcorr, obsrvr,
                      dref, dvec, crdsys, coord, relate, refval,
                      adjust, step, nintvals, ctypes.byref(cnfine),
                      ctypes.byref(result))


@spiceErrorCheck
def gfsstp(step):
    """
    Set the step size to be returned by :func:`gfstep`.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfsstp_c.html

    :param step: Time step to take.
    :type step: float
    """
    step = ctypes.c_double(step)
    libspice.gfsstp_c(step)


@spiceErrorCheck
def gfstep(time):
    """
    Return the time step set by the most recent call to :func:`gfsstp`.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfstep_c.html

    :param time: Ignored ET value.
    :type time: float
    :return: Time step to take.
    :rtype: float
    """
    time = ctypes.c_double(time)
    step = ctypes.c_double()
    libspice.gfstep_c(time, ctypes.byref(step))
    return step.value


@spiceErrorCheck
def gfstol(value):
    """
    Override the default GF convergence
    value used in the high level GF routines.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfstol_c.html

    :param value: Double precision value returned or to store.
    :type value: float
    """
    value = ctypes.c_double(value)
    libspice.gfstol_c(value)


@spiceErrorCheck
def gfsubc(target, fixref, method, abcorr, obsrvr, crdsys, coord, relate,
           refval, adjust, step, nintvals, cnfine,
           result):
    """
    Determine time intervals for which a coordinate of an
    subpoint position vector satisfies a numerical constraint.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gfsubc_c.html

    :param target: Name of the target body.
    :type target: str
    :param fixref: Body fixed frame associated with the target.
    :type fixref: str
    :param method: Name of method type for subpoint calculation.
    :type method: str
    :param abcorr: Aberration correction flag
    :type abcorr: str
    :param obsrvr: Name of the observing body.
    :type obsrvr: str
    :param crdsys: Name of the coordinate system containing COORD.
    :type crdsys: str
    :param coord: Name of the coordinate of interest
    :type coord: str
    :param relate: Relational operator.
    :type relate: str
    :param refval: Reference value.
    :type refval: float
    :param adjust: Adjustment value for absolute extrema searches.
    :type adjust: float
    :param step: Step size used for locating extrema and roots.
    :type step: float
    :param nintvals: Workspace window interval count.
    :type nintvals: int
    :param cnfine: SPICE window to which the search is restricted.
    :type cnfine: spiceypy.utils.support_types.SpiceCell
    :param result: SPICE window containing results.
    :type result: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(cnfine, stypes.SpiceCell)
    assert cnfine.is_double()
    assert isinstance(result, stypes.SpiceCell)
    assert result.is_double()
    target = stypes.stringToCharP(target)
    fixref = stypes.stringToCharP(fixref)
    method = stypes.stringToCharP(method)
    abcorr = stypes.stringToCharP(abcorr)
    obsrvr = stypes.stringToCharP(obsrvr)
    crdsys = stypes.stringToCharP(crdsys)
    coord = stypes.stringToCharP(coord)
    relate = stypes.stringToCharP(relate)
    refval = ctypes.c_double(refval)
    adjust = ctypes.c_double(adjust)
    step = ctypes.c_double(step)
    nintvals = ctypes.c_int(nintvals)
    libspice.gfsubc_c(target, fixref, method, abcorr, obsrvr, crdsys,
                      coord, relate, refval, adjust, step, nintvals,
                      ctypes.byref(cnfine), ctypes.byref(result))


@spiceErrorCheck
def gftfov(inst, target, tshape, tframe, abcorr, obsrvr, step, cnfine):
    """
    Determine time intervals when a specified ephemeris object
    intersects the space bounded by the field-of-view (FOV) of a
    specified instrument.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gftfov_c.html

    :param inst: Name of the instrument.
    :type inst: str
    :param target: Name of the target body.
    :type target: str
    :param tshape: Type of shape model used for target body.
    :type tshape: str
    :param tframe: Body-fixed, body-centered frame for target body.
    :type tframe: str
    :param abcorr: Aberration correction flag.
    :type abcorr: str
    :param obsrvr: Name of the observing body.
    :type obsrvr: str
    :param step: Step size in seconds for finding FOV events.
    :type step: float
    :param cnfine: SPICE window to which the search is restricted.
    :type cnfine: spiceypy.utils.support_types.SpiceCell
    :return: SpiceCell containing set of time  intervals, within the confinement period, when the target body is visible
    :rtype: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(cnfine, stypes.SpiceCell)
    assert cnfine.is_double()
    inst   = stypes.stringToCharP(inst)
    target = stypes.stringToCharP(target)
    tshape = stypes.stringToCharP(tshape)
    tframe = stypes.stringToCharP(tframe)
    abcorr = stypes.stringToCharP(abcorr)
    obsrvr = stypes.stringToCharP(obsrvr)
    step = ctypes.c_double(step)
    result = stypes.SPICEDOUBLE_CELL(20000)
    libspice.gftfov_c(inst, target, tshape, tframe, abcorr, obsrvr, step,
                      ctypes.byref(cnfine), ctypes.byref(result))
    return result


# gfudb has call backs


# gfuds has call backs


@spiceErrorCheck
@spiceFoundExceptionThrower
def gipool(name, start, room):
    """
    Return the integer value of a kernel variable from the kernel pool.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gipool_c.html

    :param name: Name of the variable whose value is to be returned.
    :type name: str
    :param start: Which component to start retrieving for name.
    :type start: int
    :param room: The largest number of values to return.
    :type room: int
    :return: Values associated with name.
    :rtype: list of int
    """
    name = stypes.stringToCharP(name)
    start = ctypes.c_int(start)
    ivals = stypes.emptyIntVector(room)
    room = ctypes.c_int(room)
    n = ctypes.c_int()
    found = ctypes.c_bool()
    libspice.gipool_c(name, start, room, ctypes.byref(n), ivals,
                      ctypes.byref(found))
    return stypes.vectorToList(ivals)[0:n.value], found.value


@spiceErrorCheck
@spiceFoundExceptionThrower
def gnpool(name, start, room, lenout=_default_len_out):
    """
    Return names of kernel variables matching a specified template.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/gnpool_c.html

    :param name: Template that names should match.
    :type name: str
    :param start: Index of first matching name to retrieve.
    :type start: int
    :param room: The largest number of values to return.
    :type room: int
    :param lenout: Length of strings in output array kvars.
    :type lenout: int
    :return: Kernel pool variables whose names match name.
    :rtype: list of str
    """
    name = stypes.stringToCharP(name)
    start = ctypes.c_int(start)
    kvars = stypes.charvector(room, lenout)
    room = ctypes.c_int(room)
    lenout = ctypes.c_int(lenout)
    n = ctypes.c_int()
    found = ctypes.c_bool()
    libspice.gnpool_c(name, start, room, lenout, ctypes.byref(n), kvars,
                      ctypes.byref(found))
    return stypes.vectorToList(kvars)[0:n.value], found.value


################################################################################
# H


@spiceErrorCheck
def halfpi():
    """
    Return half the value of pi (the ratio of the circumference of
    a circle to its diameter).

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/halfpi_c.html

    :return: Half the value of pi.
    :rtype: float
    """
    return libspice.halfpi_c()


@spiceErrorCheck
def hx2dp(string):
    """
    Convert a string representing a double precision number in a
    base 16 scientific notation into its equivalent double
    precision number.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/hx2dp_c.html

    :param string: Hex form string to convert to double precision.
    :type string: str
    :return: Double precision value to be returned, Or Error Message.
    :rtype: float or str
    """
    string = stypes.stringToCharP(string)
    lenout = ctypes.c_int(80)
    errmsg = stypes.stringToCharP(lenout)
    number = ctypes.c_double()
    error = ctypes.c_bool()
    libspice.hx2dp_c(string, lenout, ctypes.byref(number), ctypes.byref(error),
                     errmsg)
    if not error.value:
        return number.value
    else:
        return stypes.toPythonString(errmsg)


################################################################################
# I


@spiceErrorCheck
def ident():
    """
    This routine returns the 3x3 identity matrix.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ident_c.html

    :return: The 3x3 identity matrix.
    :rtype: 3x3-Element Array of floats
    """
    matrix = stypes.emptyDoubleMatrix()
    libspice.ident_c(matrix)
    return stypes.matrixToList(matrix)


@spiceErrorCheck
def illum(target, et, abcorr, obsrvr, spoint):
    """
    Deprecated: This routine has been superseded by the CSPICE
    routine ilumin. This routine is supported for purposes of
    backward compatibility only.

    Find the illumination angles at a specified surface point of a
    target body.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/illum_c.html

    :param target: Name of target body.
    :type target: str
    :param et: Epoch in ephemeris seconds past J2000.
    :type et: float
    :param abcorr: Desired aberration correction.
    :type abcorr: str
    :param obsrvr: Name of observing body.
    :type obsrvr: str
    :param spoint: Body-fixed coordinates of a target surface point.
    :type spoint: 3-Element Array of floats
    :return:
            Phase angle,
            Solar incidence angle,
            and Emission angle at the surface point.
    :rtype: tuple
    """
    target = stypes.stringToCharP(target)
    et = ctypes.c_double(et)
    abcorr = stypes.stringToCharP(abcorr)
    obsrvr = stypes.stringToCharP(obsrvr)
    spoint = stypes.toDoubleVector(spoint)
    phase = ctypes.c_double(0)
    solar = ctypes.c_double(0)
    emissn = ctypes.c_double(0)
    libspice.illum_c(target, et, abcorr, obsrvr, spoint, ctypes.byref(phase),
                     ctypes.byref(solar), ctypes.byref(emissn))
    return phase.value, solar.value, emissn.value


@spiceErrorCheck
def ilumin(method, target, et, fixref, abcorr, obsrvr, spoint):
    """
    Find the illumination angles (phase, solar incidence, and
    emission) at a specified surface point of a target body.

    This routine supersedes illum.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ilumin_c.html

    :param method: Computation method.
    :type method: str
    :param target: Name of target body.
    :type target: str
    :param et: Epoch in ephemeris seconds past J2000.
    :type et: float
    :param fixref: Body-fixed, body-centered target body frame.
    :type fixref: str
    :param abcorr: Desired aberration correction.
    :type abcorr: str
    :param obsrvr: Name of observing body.
    :type obsrvr: str
    :param spoint: Body-fixed coordinates of a target surface point.
    :type spoint: 3-Element Array of floats
    :return: Target surface point epoch, Vector from observer to target
     surface point, Phase angle, Solar incidence angle, and Emission
     angle at the surface point.
    :rtype: tuple
    """
    method = stypes.stringToCharP(method)
    target = stypes.stringToCharP(target)
    et = ctypes.c_double(et)
    fixref = stypes.stringToCharP(fixref)
    abcorr = stypes.stringToCharP(abcorr)
    obsrvr = stypes.stringToCharP(obsrvr)
    spoint = stypes.toDoubleVector(spoint)
    trgepc = ctypes.c_double(0)
    srfvec = stypes.emptyDoubleVector(3)
    phase = ctypes.c_double(0)
    solar = ctypes.c_double(0)
    emissn = ctypes.c_double(0)
    libspice.ilumin_c(method, target, et, fixref, abcorr, obsrvr, spoint,
                      ctypes.byref(trgepc),
                      srfvec, ctypes.byref(phase), ctypes.byref(solar),
                      ctypes.byref(emissn))
    return trgepc.value, stypes.vectorToList(
            srfvec), phase.value, solar.value, emissn.value


@spiceErrorCheck
@spiceFoundExceptionThrower
def inedpl(a, b, c, plane):
    """
    Find the intersection of a triaxial ellipsoid and a plane.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/inedpl_c.html

    :param a: Length of ellipsoid semi-axis lying on the x-axis.
    :type a: float
    :param b: Length of ellipsoid semi-axis lying on the y-axis.
    :type b: float
    :param c: Length of ellipsoid semi-axis lying on the z-axis.
    :type c: float
    :param plane: Plane that intersects ellipsoid.
    :type plane: spiceypy.utils.support_types.Plane
    :return: Intersection ellipse.
    :rtype: spiceypy.utils.support_types.Ellipse
    """
    assert (isinstance(plane, stypes.Plane))
    ellipse = stypes.Ellipse()
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    found = ctypes.c_bool() #TODO: throw exception?
    libspice.inedpl_c(a, b, c, ctypes.byref(plane), ctypes.byref(ellipse),
                      ctypes.byref(found))
    return ellipse, found.value


@spiceErrorCheck
def inelpl(ellips, plane):
    """
    Find the intersection of an ellipse and a plane.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/inelpl_c.html

    :param ellips: A SPICE ellipse.
    :type plane: spiceypy.utils.support_types.Ellipse
    :param plane: A SPICE plane.
    :type plane: spiceypy.utils.support_types.Plane
    :return:
            Number of intersection points of plane and ellipse,
            Point 1,
            Point 2.
    :rtype: tuple
    """
    assert (isinstance(plane, stypes.Plane))
    assert (isinstance(ellips, stypes.Ellipse))
    nxpts = ctypes.c_int()
    xpt1 = stypes.emptyDoubleVector(3)
    xpt2 = stypes.emptyDoubleVector(3)
    libspice.inelpl_c(ctypes.byref(ellips), ctypes.byref(plane),
                      ctypes.byref(nxpts), xpt1, xpt2)
    return nxpts.value, stypes.vectorToList(xpt1), stypes.vectorToList(xpt2)


@spiceErrorCheck
def inrypl(vertex, direct, plane):
    """
    Find the intersection of a ray and a plane.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/inrypl_c.html

    :param vertex: Vertex vector of ray.
    :type vertex: 3-Element Array of floats
    :param direct: Direction vector of ray.
    :type direct: 3-Element Array of floats
    :param plane: A SPICE plane.
    :type plane: spiceypy.utils.support_types.Plane
    :return:
            Number of intersection points of ray and plane,
            Intersection point,
            if nxpts == 1.
    :rtype: tuple
    """
    assert (isinstance(plane, stypes.Plane))
    vertex = stypes.toDoubleVector(vertex)
    direct = stypes.toDoubleVector(direct)
    nxpts = ctypes.c_int()
    xpt = stypes.emptyDoubleVector(3)
    libspice.inrypl_c(vertex, direct, ctypes.byref(plane), ctypes.byref(nxpts),
                      xpt)
    return nxpts.value, stypes.vectorToList(xpt)


@spiceErrorCheck
def insrtc(item, inset):
    """
    Insert an item into a character set.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/insrtc_c.html

    :param item: Item to be inserted.
    :type item: str or list of str
    :param inset: Insertion set.
    :type inset: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(inset, stypes.SpiceCell)
    if isinstance(item, list):
        for c in item:
            libspice.insrtc_c(stypes.stringToCharP(c), ctypes.byref(inset))
    else:
        item = stypes.stringToCharP(item)
        libspice.insrtc_c(item, ctypes.byref(inset))


@spiceErrorCheck
def insrtd(item, inset):
    """
    Insert an item into a double precision set.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/insrtd_c.html

    :param item: Item to be inserted.
    :type item: float or list of floats
    :param inset: Insertion set.
    :type inset: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(inset, stypes.SpiceCell)
    if hasattr(item, "__iter__"):
        for d in item:
            libspice.insrtd_c(ctypes.c_double(d), ctypes.byref(inset))
    else:
        item = ctypes.c_double(item)
        libspice.insrtd_c(item, ctypes.byref(inset))


@spiceErrorCheck
def insrti(item, inset):
    """
    Insert an item into an integer set.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/insrti_c.html

    :param item: Item to be inserted.
    :type item: int or list of ints
    :param inset: Insertion set.
    :type inset: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(inset, stypes.SpiceCell)
    if hasattr(item, "__iter__"):
        for i in item:
            libspice.insrti_c(ctypes.c_int(i), ctypes.byref(inset))
    else:
        item = ctypes.c_int(item)
        libspice.insrti_c(item, ctypes.byref(inset))


@spiceErrorCheck
def inter(a, b):
    """
    Intersect two sets of any data type to form a third set.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/inter_c.html

    :param a: First input set.
    :type a: spiceypy.utils.support_types.SpiceCell
    :param b: Second input set.
    :type b: spiceypy.utils.support_types.SpiceCell
    :return: Intersection of a and b.
    :rtype: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(a, stypes.SpiceCell)
    assert isinstance(b, stypes.SpiceCell)
    assert a.dtype == b.dtype
    assert a.dtype == 0 or a.dtype == 1 or a.dtype == 2
    if a.dtype is 0:
        c = stypes.SPICECHAR_CELL(max(a.size, b.size), max(a.length, b.length))
    elif a.dtype is 1:
        c = stypes.SPICEDOUBLE_CELL(max(a.size, b.size))
    elif a.dtype is 2:
        c = stypes.SPICEINT_CELL(max(a.size, b.size))
    else:
        raise NotImplementedError
    libspice.inter_c(ctypes.byref(a), ctypes.byref(b), ctypes.byref(c))
    return c


@spiceErrorCheck
def intmax():
    """
    Return the value of the largest (positive) number representable
    in a int variable.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/intmax_c.html

    :return: The largest (positive) number representablein a Int variable.
    :rtype: int
    """
    return libspice.intmax_c()


@spiceErrorCheck
def intmin():
    """
    Return the value of the smallest (negative) number representable
    in a SpiceInt variable.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/intmin_c.html

    :return: The smallest (negative) number representablein a Int variable.
    :rtype: int
    """
    return libspice.intmin_c()


@spiceErrorCheck
def invert(m):
    """
    Generate the inverse of a 3x3 matrix.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/invert_c.html

    :param m: Matrix to be inverted.
    :type m: 3x3-Element Array of floats
    :return: Inverted matrix (m1)^-1
    :rtype: 3x3-Element Array of floats
    """
    m = stypes.listtodoublematrix(m)
    mout = stypes.emptyDoubleMatrix()
    libspice.invert_c(m, mout)
    return stypes.matrixToList(mout)


@spiceErrorCheck
def invort(m):
    """
    Given a matrix, construct the matrix whose rows are the
    columns of the first divided by the length squared of the
    the corresponding columns of the input matrix.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/invort_c.html

    :param m: A 3x3 Matrix.
    :type m: 3x3-Element Array of floats
    :return: m after transposition and scaling of rows.
    :rtype: 3x3-Element Array of floats
    """
    m = stypes.listtodoublematrix(m)
    mout = stypes.emptyDoubleMatrix()
    libspice.invort_c(m, mout)
    return stypes.matrixToList(mout)


@spiceErrorCheck
def isordv(array, n):
    """
    Determine whether an array of n items contains the integers
    0 through n-1.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/isordv_c.html

    :param array: Array of integers.
    :type array: Array of ints
    :param n: Number of integers in array.
    :type n: int
    :return:
            The function returns True if the array contains the
            integers 0 through n-1, otherwise it returns False.
    :rtype: bool
    """
    array = stypes.toIntVector(array)
    n = ctypes.c_int(n)
    return libspice.isordv_c(array, n)


@spiceErrorCheck
def isrchc(value, ndim, lenvals, array):
    """
    Search for a given value within a character string array. Return
    the index of the first matching array entry, or -1 if the key
    value was not found.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/isrchc_c.html

    :param value: Key value to be found in array.
    :type value: str
    :param ndim: Dimension of array.
    :type ndim: int
    :param lenvals: String length.
    :type lenvals: int
    :param array: Character string array to search.
    :type array: list of str
    :return:
            The index of the first matching array element or -1
            if the value is not found.
    :rtype: int
    """
    value = stypes.stringToCharP(value)
    array = stypes.listToCharArrayPtr(array, xLen=lenvals, yLen=ndim)
    ndim = ctypes.c_int(ndim)
    lenvals = ctypes.c_int(lenvals)
    return libspice.isrchc_c(value, ndim, lenvals, array)


@spiceErrorCheck
def isrchd(value, ndim, array):
    """
    Search for a given value within a double precision array. Return
    the index of the first matching array entry, or -1 if the key value
    was not found.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/isrchd_c.html

    :param value: Key value to be found in array.
    :type value: float
    :param ndim: Dimension of array.
    :type ndim: int
    :param array: Double Precision array to search.
    :type array: Array of floats
    :return:
            The index of the first matching array element or -1
            if the value is not found.
    :rtype: int
    """
    value = ctypes.c_double(value)
    ndim = ctypes.c_int(ndim)
    array = stypes.toDoubleVector(array)
    return libspice.isrchd_c(value, ndim, array)


@spiceErrorCheck
def isrchi(value, ndim, array):
    """
    Search for a given value within an integer array. Return
    the index of the first matching array entry, or -1 if the key
    value was not found.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/isrchi_c.html

    :param value: Key value to be found in array.
    :type value: int
    :param ndim: Dimension of array.
    :type ndim: int
    :param array: Integer array to search.
    :type array: Array of ints
    :return:
            The index of the first matching array element or -1
            if the value is not found.
    :rtype: int
    """
    value = ctypes.c_int(value)
    ndim = ctypes.c_int(ndim)
    array = stypes.toIntVector(array)
    return libspice.isrchi_c(value, ndim, array)


@spiceErrorCheck
def isrot(m, ntol, dtol):
    """
    Indicate whether a 3x3 matrix is a rotation matrix.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/isrot_c.html

    :param m: A matrix to be tested.
    :type m: 3x3-Element Array of floats
    :param ntol: Tolerance for the norms of the columns of m.
    :type ntol: float
    :param dtol:
                Tolerance for the determinant of a matrix whose columns
                are the unitized columns of m.
    :type dtol: float
    :return: True if and only if m is a rotation matrix.
    :rtype: bool
    """
    m = stypes.listtodoublematrix(m)
    ntol = ctypes.c_double(ntol)
    dtol = ctypes.c_double(dtol)
    return libspice.isrot_c(m, ntol, dtol)


@spiceErrorCheck
def iswhsp(string):
    """
    Return a boolean value indicating whether a string contains
    only white space characters.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/iswhsp_c.html

    :param string: String to be tested.
    :type string: str
    :return:
            the boolean value True if the string is empty or contains
            only white space characters; otherwise it returns the value False.
    :rtype: bool
    """
    string = stypes.stringToCharP(string)
    return libspice.iswhsp_c(string)


################################################################################
# J


@spiceErrorCheck
def j1900():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/j1900_c.html

    :return: Julian Date of 1899 DEC 31 12:00:00
    :rtype: float
    """
    return libspice.j1900_c()


@spiceErrorCheck
def j1950():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/j1950_c.html

    :return: Julian Date of 1950 JAN 01 00:00:00
    :rtype: float
    """
    return libspice.j1950_c()


@spiceErrorCheck
def j2000():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/j2000_c.html

    :return: Julian Date of 2000 JAN 01 12:00:00
    :rtype: float
    """
    return libspice.j2000_c()


@spiceErrorCheck
def j2100():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/j2100_c.html

    :return: Julian Date of 2100 JAN 01 12:00:00
    :rtype: float
    """
    return libspice.j2100_c()


@spiceErrorCheck
def jyear():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/jyear_c.html

    :return: number of seconds in a julian year
    :rtype: float
    """
    return libspice.jyear_c()


################################################################################
# K


@spiceErrorCheck
def kclear():
    """
    Clear the KEEPER subsystem: unload all kernels, clear the kernel
    pool, and re-initialize the subsystem. Existing watches on kernel
    variables are retained.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/kclear_c.html

    """
    libspice.kclear_c()


@spiceErrorCheck
@spiceFoundExceptionThrower
def kdata(which, kind, fillen=_default_len_out, typlen=_default_len_out, srclen=_default_len_out):
    """
    Return data for the nth kernel that is among a list of specified
    kernel types.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/kdata_c.html

    :param which: Index of kernel to fetch from the list of kernels.
    :type which: int
    :param kind: The kind of kernel to which fetches are limited.
    :type kind: str
    :param fillen: Available space in output file string.
    :type fillen: int
    :param typlen: Available space in output kernel type string.
    :type typlen: int
    :param srclen: Available space in output source string.
    :type srclen: int
    :return:
            The name of the kernel file, The type of the kernel,
            Name of the source file used to load file,
            The handle attached to file.
    :rtype: tuple
    """
    which = ctypes.c_int(which)
    kind = stypes.stringToCharP(kind)
    fillen = ctypes.c_int(fillen)
    typlen = ctypes.c_int(typlen)
    srclen = ctypes.c_int(srclen)
    file = stypes.stringToCharP(fillen)
    filtyp = stypes.stringToCharP(typlen)
    source = stypes.stringToCharP(srclen)
    handle = ctypes.c_int()
    found = ctypes.c_bool()
    libspice.kdata_c(which, kind, fillen, typlen, srclen, file, filtyp, source,
                     ctypes.byref(handle), ctypes.byref(found))
    return stypes.toPythonString(file), stypes.toPythonString(
            filtyp), stypes.toPythonString(source), handle.value, found.value


@spiceErrorCheck
@spiceFoundExceptionThrower
def kinfo(file, typlen=_default_len_out, srclen=_default_len_out):
    """
    Return information about a loaded kernel specified by name.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/kinfo_c.html

    :param file: Name of a kernel to fetch information for
    :type file: str
    :param typlen: Available space in output kernel type string.
    :type typlen: int
    :param srclen: Available space in output source string.
    :type srclen: int
    :return:
            The type of the kernel,
            Name of the source file used to load file,
            The handle attached to file.
    :rtype: tuple
    """
    typlen = ctypes.c_int(typlen)
    srclen = ctypes.c_int(srclen)
    file = stypes.stringToCharP(file)
    filtyp = stypes.stringToCharP(" " * typlen.value)
    source = stypes.stringToCharP(" " * srclen.value)
    handle = ctypes.c_int()
    found = ctypes.c_bool()
    libspice.kinfo_c(file, typlen, srclen, filtyp, source, ctypes.byref(handle),
                     ctypes.byref(found))
    return stypes.toPythonString(filtyp), stypes.toPythonString(
            source), handle.value, found.value


@spiceErrorCheck
def kplfrm(frmcls, outCell=None):
    """
    Return a SPICE set containing the frame IDs of all reference
    frames of a given class having specifications in the kernel pool.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/kplfrm_c.html

    :param frmcls: Frame class.
    :type frmcls: int
    :param outCell: Optional output Spice Int Cell
    :type outCell: spiceypy.utils.support_types.SpiceCell
    :return: Set of ID codes of frames of the specified class.
    :rtype: spiceypy.utils.support_types.SpiceCell
    """
    if not outCell:
        outCell = stypes.SPICEINT_CELL(1000)
    frmcls = ctypes.c_int(frmcls)
    libspice.kplfrm_c(frmcls, ctypes.byref(outCell))
    return outCell


@spiceErrorCheck
def ktotal(kind):
    """
    Return the current number of kernels that have been loaded
    via the KEEPER interface that are of a specified type.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ktotal_c.html

    :param kind: A list of kinds of kernels to count.
    :type kind: str
    :return: The number of kernels of type kind.
    :rtype: int
    """
    kind = stypes.stringToCharP(kind)
    count = ctypes.c_int()
    libspice.ktotal_c(kind, ctypes.byref(count))
    return count.value


@spiceErrorCheck
@spiceFoundExceptionThrower
def kxtrct(keywd, terms, nterms, instring, termlen=_default_len_out, stringlen=_default_len_out, substrlen=_default_len_out):
    """
    Locate a keyword in a string and extract the substring from
    the beginning of the first word following the keyword to the
    beginning of the first subsequent recognized terminator of a list.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/kxtrct_c.html

    :param keywd: Word that marks the beginning of text of interest.
    :type keywd: str
    :param terms: Set of words, any of which marks the end of text.
    :type terms: Array of str
    :param nterms: Number of terms.
    :type nterms: int
    :param instring: String containing a sequence of words.
    :type instring: str
    :param termlen: Length of strings in string array term.
    :type termlen: int
    :param stringlen: Available space in argument string.
    :type stringlen: int
    :param substrlen: Available space in output substring.
    :type substrlen: int
    :return:
            String containing a sequence of words,
            String from end of keywd to beginning of first terms item found.
    :rtype: tuple
    """
    keywd = stypes.stringToCharP(keywd)
    termlen = ctypes.c_int(termlen)
    terms = stypes.listToCharArrayPtr(terms)
    nterms = ctypes.c_int(nterms)
    instring = stypes.stringToCharP(instring)
    substr = stypes.stringToCharP(substrlen)
    stringlen = ctypes.c_int(stringlen)
    substrlen = ctypes.c_int(substrlen)
    found = ctypes.c_bool()
    libspice.kxtrct_c(keywd, termlen, ctypes.byref(terms), nterms,
                      stringlen, substrlen, instring, ctypes.byref(found),
                      substr)
    return stypes.toPythonString(instring), stypes.toPythonString(
            substr), found.value


################################################################################
# L


@spiceErrorCheck
def lastnb(string):
    """
    Return the zero based index of the last non-blank character in
    a character string.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lastnb_c.html

    :param string: Input character string.
    :type string: str
    :return: :rtype:
    """
    string = stypes.stringToCharP(string)
    return libspice.lastnb_c(string)


@spiceErrorCheck
def latcyl(radius, lon, lat):
    """
    Convert from latitudinal coordinates to cylindrical coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/latcyl_c.html

    :param radius: Distance of a point from the origin.
    :type radius:
    :param lon: Angle of the point from the XZ plane in radians.
    :param lat: Angle of the point from the XY plane in radians.
    :return: (r, lonc, z)
    :rtype: tuple
    """
    radius = ctypes.c_double(radius)
    lon = ctypes.c_double(lon)
    lat = ctypes.c_double(lat)
    r = ctypes.c_double()
    lonc = ctypes.c_double()
    z = ctypes.c_double()
    libspice.latcyl_c(radius, lon, lat, ctypes.byref(r), ctypes.byref(lonc),
                      ctypes.byref(z))
    return r.value, lonc.value, z.value


@spiceErrorCheck
def latrec(radius, longitude, latitude):
    """
    Convert from latitudinal coordinates to rectangular coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/latrec_c.html

    :param radius: Distance of a point from the origin.
    :type radius: float
    :param longitude: Longitude of point in radians.
    :type longitude: float
    :param latitude: Latitude of point in radians.
    :type latitude: float
    :return: Rectangular coordinates of the point.
    :rtype: 3-Element Array of floats
    """
    radius = ctypes.c_double(radius)
    longitude = ctypes.c_double(longitude)
    latitude = ctypes.c_double(latitude)
    rectan = stypes.emptyDoubleVector(3)
    libspice.latrec_c(radius, longitude, latitude, rectan)
    return stypes.vectorToList(rectan)


@spiceErrorCheck
def latsph(radius, lon, lat):
    """
    Convert from latitudinal coordinates to spherical coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/latsph_c.html

    :param radius: Distance of a point from the origin.
    :param lon: Angle of the point from the XZ plane in radians.
    :param lat: Angle of the point from the XY plane in radians.
    :return: (rho colat, lons)
    :rtype: tuple
    """
    radius = ctypes.c_double(radius)
    lon = ctypes.c_double(lon)
    lat = ctypes.c_double(lat)
    rho = ctypes.c_double()
    colat = ctypes.c_double()
    lons = ctypes.c_double()
    libspice.latsph_c(radius, lon, lat, ctypes.byref(rho), ctypes.byref(colat),
                      ctypes.byref(lons))
    return rho.value, colat.value, lons.value


@spiceErrorCheck
def lcase(instr, lenout=_default_len_out):
    """
    Convert the characters in a string to lowercase.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lcase_c.html

    :param instr: Input string.
    :type instr: str
    :param lenout: Maximum length of output string.
    :type lenout: int
    :return: Output string, all lowercase.
    :rtype: str
    """
    instr = stypes.stringToCharP(instr)
    lenout = ctypes.c_int(lenout)
    outstr = stypes.stringToCharP(lenout)
    libspice.lcase_c(instr, lenout, outstr)
    return stypes.toPythonString(outstr)


@spiceErrorCheck
def ldpool(filename):
    """
    Load the variables contained in a NAIF ASCII kernel file into the
    kernel pool.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ldpool_c.html

    :param filename: Name of the kernel file.
    :type filename: str
    """
    filename = stypes.stringToCharP(filename)
    libspice.ldpool_c(filename)


@spiceErrorCheck
def lmpool(cvals):
    """
    Load the variables contained in an internal buffer into the
    kernel pool.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lmpool_c.html

    :param cvals: list of strings.
    :type cvals: list of str
    """
    lenvals = ctypes.c_int(len(max(cvals, key=len)) + 1)
    n = ctypes.c_int(len(cvals))
    cvals = stypes.listToCharArrayPtr(cvals, xLen=lenvals, yLen=n)
    libspice.lmpool_c(cvals, lenvals, n)


@spiceErrorCheck
def lparse(inlist, delim, nmax):
    """
    Parse a list of items delimited by a single character.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lparse_c.html

    :param inlist: list of items delimited by delim.
    :type inlist: list of strings
    :param delim: Single character used to delimit items.
    :type delim: str
    :param nmax: Maximum number of items to return.
    :type nmax: int
    :return: Items in the list, left justified.
    :rtype: list of str
    """
    delim = stypes.stringToCharP(delim)
    lenout = ctypes.c_int(len(inlist))
    inlist = stypes.stringToCharP(inlist)
    nmax = ctypes.c_int(nmax)
    items = stypes.emptyCharArray(lenout, nmax)
    n = ctypes.c_int()
    libspice.lparse_c(inlist, delim, nmax, lenout, ctypes.byref(n),
                      ctypes.byref(items))
    return [stypes.toPythonString(x.value) for x in items[0:n.value]]


@spiceErrorCheck
def lparsm(inlist, delims, nmax, lenout=None):
    """
    Parse a list of items separated by multiple delimiters.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lparsm_c.html

    :param inlist: list of items delimited by delims.
    :type inlist: list of strings
    :param delims: Single characters which delimit items.
    :type delims: str
    :param nmax: Maximum number of items to return.
    :type nmax: int
    :param lenout: Optional Length of strings in item array.
    :type lenout: int
    :return: Items in the list, left justified.
    :rtype: list of strings
    """
    if lenout is None:
        lenout = ctypes.c_int(len(inlist) + 1)
    inlist = stypes.stringToCharP(inlist)
    delims = stypes.stringToCharP(delims)
    items = stypes.emptyCharArray(nmax, lenout)
    nmax = ctypes.c_int(nmax)
    n = ctypes.c_int()
    libspice.lparsm_c(inlist, delims, nmax, lenout, ctypes.byref(n), items)
    return [stypes.toPythonString(x.value) for x in items][0:n.value]


@spiceErrorCheck
def lparss(inlist, delims, NMAX=20, LENGTH=50):
    """
    Parse a list of items separated by multiple delimiters, placing the
    resulting items into a set.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lparss_c.html

    :param inlist: list of items delimited by delims.
    :type inlist:
    :param delims: Single characters which delimit items.
    :type delims: str
    :param NMAX: Optional nmax of spice set.
    :type NMAX: int
    :param LENGTH: Optional length of strings in spice set
    :type LENGTH: int
    :return: Set containing items in the list, left justified.
    :rtype:
    """
    inlist = stypes.stringToCharP(inlist)
    delims = stypes.stringToCharP(delims)
    returnSet = stypes.SPICECHAR_CELL(NMAX, LENGTH)
    libspice.lparss_c(inlist, delims, ctypes.byref(returnSet))
    return returnSet


@spiceErrorCheck
def lspcn(body, et, abcorr):
    """
    Compute L_s, the planetocentric longitude of the sun, as seen
    from a specified body.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lspcn_c.html

    :param body: Name of central body.
    :type body: str
    :param et: Epoch in seconds past J2000 TDB.
    :type et: float
    :param abcorr: Aberration correction.
    :type abcorr: str
    :return: planetocentric longitude of the sun
    :rtype: float
    """
    body = stypes.stringToCharP(body)
    et = ctypes.c_double(et)
    abcorr = stypes.stringToCharP(abcorr)
    return libspice.lspcn_c(body, et, abcorr)


@spiceErrorCheck
def lstlec(string, n, lenvals, array):
    """
    Given a character string and an ordered array of character
    strings, find the index of the largest array element less than
    or equal to the given string.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lstlec_c.html

    :param string: Upper bound value to search against.
    :type string: str
    :param n: Number elements in array.
    :type n: int
    :param lenvals: String length.
    :type lenvals: int
    :param array: Array of possible lower bounds.
    :type array: list
    :return:
            index of the last element of array that is
            lexically less than or equal to string.
    :rtype: int
    """
    string = stypes.stringToCharP(string)
    array = stypes.listToCharArrayPtr(array, xLen=lenvals, yLen=n)
    n = ctypes.c_int(n)
    lenvals = ctypes.c_int(lenvals)
    return libspice.lstlec_c(string, n, lenvals, array)


@spiceErrorCheck
def lstled(x, n, array):
    """
    Given a number x and an array of non-decreasing floats
    find the index of the largest array element less than or equal to x.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lstled_c.html

    :param x: Value to search against.
    :type x: float
    :param n: Number elements in array.
    :type n: int
    :param array: Array of possible lower bounds
    :type array: list
    :return: index of the last element of array that is less than or equal to x.
    :rtype: int
    """
    array = stypes.toDoubleVector(array)
    x = ctypes.c_double(x)
    n = ctypes.c_int(n)
    return libspice.lstled_c(x, n, array)


@spiceErrorCheck
def lstlei(x, n, array):
    """
    Given a number x and an array of non-decreasing ints,
    find the index of the largest array element less than or equal to x.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lstlei_c.html

    :param x: Value to search against.
    :type x: int
    :param n: Number elements in array.
    :type n: int
    :param array: Array of possible lower bounds
    :type array: list
    :return: index of the last element of array that is less than or equal to x.
    :rtype: int
    """
    array = stypes.toIntVector(array)
    x = ctypes.c_int(x)
    n = ctypes.c_int(n)
    return libspice.lstlei_c(x, n, array)


@spiceErrorCheck
def lstltc(string, n, lenvals, array):
    """
    Given a character string and an ordered array of character
    strings, find the index of the largest array element less than
    the given string.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lstltc_c.html

    :param string: Upper bound value to search against.
    :type string: int
    :param n: Number elements in array.
    :type n: int
    :param lenvals: String length.
    :type lenvals: int
    :param array: Array of possible lower bounds
    :type array: list
    :return:
            index of the last element of array that
            is lexically less than string.
    :rtype: int
    """
    string = stypes.stringToCharP(string)
    array = stypes.listToCharArrayPtr(array, xLen=lenvals, yLen=n)
    n = ctypes.c_int(n)
    lenvals = ctypes.c_int(lenvals)
    return libspice.lstltc_c(string, n, lenvals, array)


@spiceErrorCheck
def lstltd(x, n, array):
    """
    Given a number x and an array of non-decreasing floats
    find the index of the largest array element less than x.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lstltd_c.html

    :param x: Value to search against
    :type x: float
    :param n: Number elements in array
    :type n: int
    :param array: Array of possible lower bounds
    :type array: list
    :return: index of the last element of array that is less than x.
    :rtype: int
    """
    array = stypes.toDoubleVector(array)
    x = ctypes.c_double(x)
    n = ctypes.c_int(n)
    return libspice.lstltd_c(x, n, array)


@spiceErrorCheck
def lstlti(x, n, array):
    """
    Given a number x and an array of non-decreasing int,
    find the index of the largest array element less than x.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lstlti_c.html

    :param x: Value to search against
    :type x: int
    :param n: Number elements in array
    :type n: int
    :param array: Array of possible lower bounds
    :type array: list
    :return: index of the last element of array that is less than x.
    :rtype: int
    """
    array = stypes.toIntVector(array)
    x = ctypes.c_int(x)
    n = ctypes.c_int(n)
    return libspice.lstlti_c(x, n, array)


@spiceErrorCheck
def ltime(etobs, obs, direct, targ):
    """
    This routine computes the transmit (or receive) time
    of a signal at a specified target, given the receive
    (or transmit) time at a specified observer. The elapsed
    time between transmit and receive is also returned.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ltime_c.html

    :param etobs: Epoch of a signal at some observer
    :type etobs: float
    :param obs: NAIF ID of some observer
    :type obs: int
    :param direct: Direction the signal travels ( "->" or "<-" )
    :type direct: str
    :param targ: NAIF ID of the target object
    :type targ: int
    :return: epoch and time
    :rtype: tuple
    """
    etobs = ctypes.c_double(etobs)
    obs = ctypes.c_int(obs)
    direct = stypes.stringToCharP(direct)
    targ = ctypes.c_int(targ)
    ettarg = ctypes.c_double()
    elapsd = ctypes.c_double()
    libspice.ltime_c(etobs, obs, direct, targ, ctypes.byref(ettarg),
                     ctypes.byref(elapsd))
    return ettarg.value, elapsd.value


@spiceErrorCheck
def lx4dec(string, first):
    """
    Scan a string from a specified starting position for the
    end of a decimal number.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lx4dec_c.html

    :param string: Any character string.
    :type string: str
    :param first: First character to scan from in string.
    :type first: int
    :return: last and nchar
    :rtype: tuple
    """
    string = stypes.stringToCharP(string)
    first = ctypes.c_int(first)
    last = ctypes.c_int()
    nchar = ctypes.c_int()
    libspice.lx4dec_c(string, first, ctypes.byref(last), ctypes.byref(nchar))
    return last.value, nchar.value


@spiceErrorCheck
def lx4num(string, first):
    """
    Scan a string from a specified starting position for the
    end of a number.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lx4num_c.html

    :param string: Any character string.
    :type string: str
    :param first: First character to scan from in string.
    :type first: int
    :return: last and nchar
    :rtype: tuple
    """
    string = stypes.stringToCharP(string)
    first = ctypes.c_int(first)
    last = ctypes.c_int()
    nchar = ctypes.c_int()
    libspice.lx4num_c(string, first, ctypes.byref(last), ctypes.byref(nchar))
    return last.value, nchar.value


@spiceErrorCheck
def lx4sgn(string, first):
    """
    Scan a string from a specified starting position for the
    end of a signed integer.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lx4sgn_c.html

    :param string: Any character string.
    :type string: str
    :param first: First character to scan from in string.
    :type first: int
    :return: last and nchar
    :rtype: tuple
    """
    string = stypes.stringToCharP(string)
    first = ctypes.c_int(first)
    last = ctypes.c_int()
    nchar = ctypes.c_int()
    libspice.lx4sgn_c(string, first, ctypes.byref(last), ctypes.byref(nchar))
    return last.value, nchar.value


@spiceErrorCheck
def lx4uns(string, first):
    """
    Scan a string from a specified starting position for the
    end of an unsigned integer.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lx4uns_c.html

    :param string: Any character string.
    :type string: str
    :param first: First character to scan from in string.
    :type first: int
    :return: last and nchar
    :rtype: tuple
    """
    string = stypes.stringToCharP(string)
    first = ctypes.c_int(first)
    last = ctypes.c_int()
    nchar = ctypes.c_int()
    libspice.lx4uns_c(string, first, ctypes.byref(last), ctypes.byref(nchar))
    return last.value, nchar.value


@spiceErrorCheck
def lxqstr(string, qchar, first):
    """
    Lex (scan) a quoted string.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/lxqstr_c.html

    :param string: String to be scanned.
    :type string: str
    :param qchar: Quote delimiter character.
    :type qchar: char (string of one char)
    :param first: Character position at which to start scanning.
    :type first: int
    :return: last and nchar
    :rtype: tuple
    """
    string = stypes.stringToCharP(string)
    qchar = ctypes.c_char(qchar.encode(encoding='UTF-8'))
    first = ctypes.c_int(first)
    last = ctypes.c_int()
    nchar = ctypes.c_int()
    libspice.lxqstr_c(string, qchar, first, ctypes.byref(last),
                      ctypes.byref(nchar))
    return last.value, nchar.value


################################################################################
# M


@spiceErrorCheck
def m2eul(r, axis3, axis2, axis1):
    """
    Factor a rotation matrix as a product of three rotations
    about specified coordinate axes.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/m2eul_c.html

    :param r: A rotation matrix to be factored
    :type r: 3x3-Element Array of floats
    :param axis3: third rotation axes.
    :type axis3: int
    :param axis2: second rotation axes.
    :type axis2: int
    :param axis1: first rotation axes.
    :type axis1: int
    :return: Third, second, and first Euler angles, in radians.
    :rtype: tuple
    """
    r = stypes.listtodoublematrix(r)
    axis3 = ctypes.c_int(axis3)
    axis2 = ctypes.c_int(axis2)
    axis1 = ctypes.c_int(axis1)
    angle3 = ctypes.c_double()
    angle2 = ctypes.c_double()
    angle1 = ctypes.c_double()
    libspice.m2eul_c(r, axis3, axis2, axis1, ctypes.byref(angle3),
                     ctypes.byref(angle2), ctypes.byref(angle1))
    return angle3.value, angle2.value, angle1.value


@spiceErrorCheck
def m2q(r):
    """
    Find a unit quaternion corresponding to a specified rotation matrix.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/m2q_c.html

    :param r: A rotation matrix to be factored
    :type r: 3x3-Element Array of floats
    :return: A unit quaternion representing the rotation matrix
    :rtype: 4-Element Array of floats
    """
    r = stypes.listtodoublematrix(r)
    q = stypes.emptyDoubleVector(4)
    libspice.m2q_c(r, q)
    return stypes.vectorToList(q)


@spiceErrorCheck
def matchi(string, templ, wstr, wchr):
    """
    Determine whether a string is matched by a template containing wild cards.
    The pattern comparison is case-insensitive.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/matchi_c.html

    :param string: String to be tested.
    :type string: str
    :param templ: Template (with wild cards) to test against string.
    :type templ: str
    :param wstr: Wild string token.
    :type wstr: str of length 1
    :param wchr: Wild character token.
    :type wchr: str of length 1
    :return: The function returns True if string matches templ, else False
    :rtype: bool
    """
    string = stypes.stringToCharP(string)
    templ = stypes.stringToCharP(templ)
    wstr = ctypes.c_char(wstr.encode(encoding='UTF-8'))
    wchr = ctypes.c_char(wchr.encode(encoding='UTF-8'))
    return libspice.matchi_c(string, templ, wstr, wchr)


@spiceErrorCheck
def matchw(string, templ, wstr, wchr):
    # ctypes.c_char(wstr.encode(encoding='UTF-8')
    """
    Determine whether a string is matched by a template containing wild cards.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/matchw_c.html

    :param string: String to be tested.
    :type string: str
    :param templ: Template (with wild cards) to test against string.
    :type templ: str
    :param wstr: Wild string token.
    :type wstr: str of length 1
    :param wchr: Wild character token.
    :type wchr: str of length 1
    :return: The function returns True if string matches templ, else False
    :rtype: bool
    """
    string = stypes.stringToCharP(string)
    templ = stypes.stringToCharP(templ)
    wstr = ctypes.c_char(wstr.encode(encoding='UTF-8'))
    wchr = ctypes.c_char(wchr.encode(encoding='UTF-8'))
    return libspice.matchw_c(string, templ, wstr, wchr)


# skiping for now maxd_c,
# odd as arguments must be parsed and not really important


# skiping for now maxi_c,
# odd as arguments must be parsed and not really important


@spiceErrorCheck
def mequ(m1):
    """
    Set one double precision 3x3 matrix equal to another.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mequ_c.html

    :param m1: input matrix.
    :type m1: 3x3-Element Array of floats
    :return: Output matrix equal to m1.
    :rtype: 3x3-Element Array of floats
    """
    m1 = stypes.listtodoublematrix(m1)
    mout = stypes.emptyDoubleMatrix()
    libspice.mequ_c(m1, mout)
    return stypes.matrixToList(mout)


@spiceErrorCheck
def mequg(m1, nr, nc):
    """
    Set one double precision matrix of arbitrary size equal to another.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mequg_c.html

    :param m1: Input matrix.
    :type m1: NxM-Element Array of floats
    :param nr: Row dimension of m1.
    :type nr: int
    :param nc: Column dimension of m1.
    :type nc: int
    :return: Output matrix equal to m1
    :rtype: NxM-Element Array of floats
    """
    m1 = stypes.listtodoublematrix(m1, x=nc, y=nr)
    mout = stypes.emptyDoubleMatrix(x=nc, y=nr)
    nc = ctypes.c_int(nc)
    nr = ctypes.c_int(nr)
    libspice.mequg_c(m1, nc, nr, mout)
    return stypes.matrixToList(mout)


# skiping for now mind_c,
#  odd as arguments must be parsed and not really important


# skiping for now mini_c,
# odd as arguments must be parsed and not really important


@spiceErrorCheck
def mtxm(m1, m2):
    """
    Multiply the transpose of a 3x3 matrix and a 3x3 matrix.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mtxm_c.html

    :param m1: 3x3 double precision matrix.
    :type m1: 3x3-Element Array of floats
    :param m2: 3x3 double precision matrix.
    :type m2: 3x3-Element Array of floats
    :return: The produce m1 transpose times m2.
    :rtype: 3x3-Element Array of floats
    """
    m1 = stypes.listtodoublematrix(m1)
    m2 = stypes.listtodoublematrix(m2)
    mout = stypes.emptyDoubleMatrix()
    libspice.mtxm_c(m1, m2, mout)
    return stypes.matrixToList(mout)


@spiceErrorCheck
def mtxmg(m1, m2, ncol1, nr1r2, ncol2):
    """
    Multiply the transpose of a matrix with
    another matrix, both of arbitrary size.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mtxmg_c.html

    :param m1: nr1r2 X ncol1 double precision matrix.
    :type m1: NxM-Element Array of floats
    :param m2: nr1r2 X ncol2 double precision matrix.
    :type m2: NxM-Element Array of floats
    :param ncol1: Column dimension of m1 and row dimension of mout.
    :type ncol1: int
    :param nr1r2: Row dimension of m1 and m2.
    :type nr1r2: int
    :param ncol2: Column dimension of m2.
    :type ncol2: int
    :return: Transpose of m1 times m2.
    :rtype: NxM-Element Array of floats
    """
    m1 = stypes.listtodoublematrix(m1, x=ncol1, y=nr1r2)
    m2 = stypes.listtodoublematrix(m2, x=ncol2, y=nr1r2)
    mout = stypes.emptyDoubleMatrix(x=ncol2, y=ncol1)
    ncol1 = ctypes.c_int(ncol1)
    nr1r2 = ctypes.c_int(nr1r2)
    ncol2 = ctypes.c_int(ncol2)
    libspice.mtxmg_c(m1, m2, ncol1, nr1r2, ncol2, mout)
    return stypes.matrixToList(mout)


@spiceErrorCheck
def mtxv(m1, vin):
    """
    Multiplies the transpose of a 3x3 matrix
    on the left with a vector on the right.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mtxv_c.html

    :param m1: 3x3 double precision matrix.
    :type m1: 3x3-Element Array of floats
    :param vin: 3-dimensional double precision vector.
    :type vin: 3-Element Array of floats
    :return: 3-dimensional double precision vector.
    :rtype: 3-Element Array of floats
    """
    m1 = stypes.listtodoublematrix(m1)
    vin = stypes.toDoubleVector(vin)
    vout = stypes.emptyDoubleVector(3)
    libspice.mtxv_c(m1, vin, vout)
    return stypes.vectorToList(vout)


@spiceErrorCheck
def mtxvg(m1, v2, ncol1, nr1r2):
    """
    Multiply the transpose of a matrix and
    a vector of arbitrary size.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mtxvg_c.html

    :param m1: Left-hand matrix to be multiplied.
    :type m1: NxM-Element Array of floats
    :param v2: Right-hand vector to be multiplied.
    :type v2: Array of floats
    :param ncol1: Column dimension of m1 and length of vout.
    :type ncol1: int
    :param nr1r2: Row dimension of m1 and length of v2.
    :type nr1r2: int
    :return: Product vector m1 transpose * v2.
    :rtype: Array of floats
    """
    m1 = stypes.listtodoublematrix(m1, x=ncol1, y=nr1r2)
    v2 = stypes.toDoubleVector(v2)
    ncol1 = ctypes.c_int(ncol1)
    nr1r2 = ctypes.c_int(nr1r2)
    vout = stypes.emptyDoubleVector(ncol1.value)
    libspice.mtxvg_c(m1, v2, ncol1, nr1r2, vout)
    return stypes.vectorToList(vout)


@spiceErrorCheck
def mxm(m1, m2):
    """
    Multiply two 3x3 matrices.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mxm_c.html

    :param m1: 3x3 double precision matrix.
    :type m1: 3x3-Element Array of floats
    :param m2: 3x3 double precision matrix.
    :type m2: 3x3-Element Array of floats
    :return: 3x3 double precision matrix.
    :rtype: 3x3-Element Array of floats
    """
    m1 = stypes.listtodoublematrix(m1)
    m2 = stypes.listtodoublematrix(m2)
    mout = stypes.emptyDoubleMatrix()
    libspice.mxm_c(m1, m2, mout)
    return stypes.matrixToList(mout)


@spiceErrorCheck
def mxmg(m1, m2, nrow1, ncol1, ncol2):
    """
    Multiply two double precision matrices of arbitrary size.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mxmg_c.html

    :param m1: nrow1 X ncol1 double precision matrix.
    :type m1: NxM-Element Array of floats
    :param m2: ncol1 X ncol2 double precision matrix.
    :type m2: NxM-Element Array of floats
    :param nrow1: Row dimension of m1
    :type nrow1: int
    :param ncol1: Column dimension of m1 and row dimension of m2.
    :type ncol1: int
    :param ncol2: Column dimension of m2
    :type ncol2: int
    :return: nrow1 X ncol2 double precision matrix.
    :rtype: NxM-Element Array of floats
    """
    m1 = stypes.listtodoublematrix(m1, x=ncol1, y=nrow1)
    m2 = stypes.listtodoublematrix(m2, x=ncol2, y=ncol1)
    mout = stypes.emptyDoubleMatrix(x=ncol2, y=nrow1)
    nrow1 = ctypes.c_int(nrow1)
    ncol1 = ctypes.c_int(ncol1)
    ncol2 = ctypes.c_int(ncol2)
    libspice.mxmg_c(m1, m2, nrow1, ncol1, ncol2, mout)
    return stypes.matrixToList(mout)


@spiceErrorCheck
def mxmt(m1, m2):
    """
    Multiply a 3x3 matrix and the transpose of another 3x3 matrix.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mxmt_c.html

    :param m1: 3x3 double precision matrix.
    :type m1: 3x3-Element Array of floats
    :param m2: 3x3 double precision matrix.
    :type m2: 3x3-Element Array of floats
    :return: The product m1 times m2 transpose.
    :rtype: float
    """
    m1 = stypes.listtodoublematrix(m1)
    m2 = stypes.listtodoublematrix(m2)
    mout = stypes.emptyDoubleMatrix()
    libspice.mxmt_c(m1, m2, mout)
    return stypes.matrixToList(mout)


@spiceErrorCheck
def mxmtg(m1, m2, nrow1, nc1c2, nrow2):
    """
    Multiply a matrix and the transpose of a matrix, both of arbitrary size.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mxmtg_c.html

    :param m1: Left-hand matrix to be multiplied.
    :type m1: NxM-Element Array of floats
    :param m2: Right-hand matrix whose transpose is to be multiplied
    :type m2: NxM-Element Array of floats
    :param nrow1: Row dimension of m1 and row dimension of mout.
    :type nrow1: int
    :param nc1c2: Column dimension of m1 and column dimension of m2.
    :type nc1c2: int
    :param nrow2: Row dimension of m2 and column dimension of mout.
    :type nrow2: int
    :return: Product matrix.
    :rtype: NxM-Element Array of floats
    """
    m1 = stypes.listtodoublematrix(m1, x=nc1c2, y=nrow1)
    m2 = stypes.listtodoublematrix(m2, x=nc1c2, y=nrow2)
    mout = stypes.emptyDoubleMatrix(x=nrow2, y=nrow1)
    nrow1 = ctypes.c_int(nrow1)
    nc1c2 = ctypes.c_int(nc1c2)
    nrow2 = ctypes.c_int(nrow2)
    libspice.mxmtg_c(m1, m2, nrow1, nc1c2, nrow2, mout)
    return stypes.matrixToList(mout)


@spiceErrorCheck
def mxv(m1, vin):
    """
    Multiply a 3x3 double precision matrix with a
    3-dimensional double precision vector.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mxv_c.html

    :param m1: 3x3 double precision matrix.
    :type m1: 3x3-Element Array of floats
    :param vin: 3-dimensional double precision vector.
    :type vin: 3-Element Array of floats
    :return: 3-dimensional double precision vector.
    :rtype: 3-Element Array of floats
    """
    m1 = stypes.listtodoublematrix(m1)
    vin = stypes.toDoubleVector(vin)
    vout = stypes.emptyDoubleVector(3)
    libspice.mxv_c(m1, vin, vout)
    return stypes.vectorToList(vout)


@spiceErrorCheck
def mxvg(m1, v2, nrow1, nc1r2):
    """
    Multiply a matrix and a vector of arbitrary size.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/mxvg_c.html

    :param m1: Left-hand matrix to be multiplied.
    :type m1: NxM-Element Array of floats
    :param v2: Right-hand vector to be multiplied.
    :type v2: Array of floats
    :param nrow1: Row dimension of m1 and length of vout.
    :type nrow1: int
    :param nc1r2: Column dimension of m1 and length of v2.
    :type nc1r2: int
    :return: Product vector m1*v2
    :rtype: Array of floats
    """
    m1 = stypes.listtodoublematrix(m1, x=nc1r2, y=nrow1)
    v2 = stypes.toDoubleVector(v2)
    nrow1 = ctypes.c_int(nrow1)
    nc1r2 = ctypes.c_int(nc1r2)
    vout = stypes.emptyDoubleVector(nrow1.value)
    libspice.mxvg_c(m1, v2, nrow1, nc1r2, vout)
    return stypes.vectorToList(vout)


################################################################################
# N


@spiceErrorCheck
def namfrm(frname):
    """
    Look up the frame ID code associated with a string.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/namfrm_c.html

    :param frname: The name of some reference frame.
    :type frname: str
    :return: The SPICE ID code of the frame.
    :rtype: int
    """
    frname = stypes.stringToCharP(frname)
    frcode = ctypes.c_int()
    libspice.namfrm_c(frname, ctypes.byref(frcode))
    return frcode.value


@spiceErrorCheck
def ncpos(string, chars, start):
    """
    Find the first occurrence in a string of a character NOT belonging
    to a collection of characters, starting at a specified
    location searching forward.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ncpos_c.html

    :param string: Any character string.
    :type string: str
    :param chars: A collection of characters.
    :type chars: str
    :param start: Position to begin looking for one not in chars.
    :type start: int
    :return: index
    :rtype: int
    """
    string = stypes.stringToCharP(string)
    chars = stypes.stringToCharP(chars)
    start = ctypes.c_int(start)
    return libspice.ncpos_c(string, chars, start)


@spiceErrorCheck
def ncposr(string, chars, start):
    """
    Find the first occurrence in a string of a character NOT belonging to a
    collection of characters, starting at a specified location,
    searching in reverse.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ncposr_c.html

    :param string: Any character string.
    :type string: str
    :param chars: A collection of characters.
    :type chars: str
    :param start: Position to begin looking for one of chars.
    :type start: int
    :return: index
    :rtype: int
    """
    string = stypes.stringToCharP(string)
    chars = stypes.stringToCharP(chars)
    start = ctypes.c_int(start)
    return libspice.ncposr_c(string, chars, start)


@spiceErrorCheck
def nearpt(positn, a, b, c):
    """
    locates the point on the surface of an ellipsoid that is nearest to a
    specified position. It also returns the altitude of the
    position above the ellipsoid.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/nearpt_c.html

    :param positn: Position of a point in bodyfixed frame.
    :type positn: 3-Element Array of floats
    :param a: Length of semi-axis parallel to x-axis.
    :type a: float
    :param b: Length of semi-axis parallel to y-axis.
    :type b: float
    :param c: Length on semi-axis parallel to z-axis.
    :type c: float
    :return:
            Point on the ellipsoid closest to positn,
            Altitude of positn above the ellipsoid.
    :rtype: tuple
    """
    positn = stypes.toDoubleVector(positn)
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    npoint = stypes.emptyDoubleVector(3)
    alt = ctypes.c_double()
    libspice.nearpt_c(positn, a, b, c, npoint, ctypes.byref(alt))
    return stypes.vectorToList(npoint), alt.value


@spiceErrorCheck
def npedln(a, b, c, linept, linedr):
    """
    Find nearest point on a triaxial ellipsoid to a specified
    line and the distance from the ellipsoid to the line.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/npedln_c.html

    :param a: Length of ellipsoid's semi-axis in the x direction
    :type a: float
    :param b: Length of ellipsoid's semi-axis in the y direction
    :type b: float
    :param c: Length of ellipsoid's semi-axis in the z direction
    :type c: float
    :param linept: Length of ellipsoid's semi-axis in the z direction
    :type linept: 3-Element Array of floats
    :param linedr: Direction vector of line
    :type linedr: 3-Element Array of floats
    :return: Nearest point on ellipsoid to line, Distance of ellipsoid from line
    :rtype: tuple
    """
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    linept = stypes.toDoubleVector(linept)
    linedr = stypes.toDoubleVector(linedr)
    pnear = stypes.emptyDoubleVector(3)
    dist = ctypes.c_double()
    libspice.npedln_c(a, b, c, linept, linedr, pnear, ctypes.byref(dist))
    return stypes.vectorToList(pnear), dist.value


@spiceErrorCheck
def npelpt(point, ellips):
    """
    Find the nearest point on an ellipse to a specified point, both
    in three-dimensional space, and find the distance between the
    ellipse and the point.
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/npelpt_c.html

    :param point: Point whose distance to an ellipse is to be found.
    :type point: 3-Element Array of floats
    :param ellips: An ellipse.
    :type ellips: spiceypy.utils.support_types.Ellipse
    :return: Nearest point on ellipsoid to line, Distance of ellipsoid from line
    :rtype: tuple
    """
    assert (isinstance(ellips, stypes.Ellipse))
    point = stypes.toDoubleVector(point)
    pnear = stypes.emptyDoubleVector(3)
    dist = ctypes.c_double()
    libspice.npelpt_c(point, ctypes.byref(ellips), pnear, ctypes.byref(dist))
    return stypes.vectorToList(pnear), dist.value


@spiceErrorCheck
def nplnpt(linpt, lindir, point):
    """
    Find the nearest point on a line to a specified point,
    and find the distance between the two points.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/nplnpt_c.html

    :param linpt: Point on a line
    :type linpt: 3-Element Array of floats
    :param lindir: line's direction vector
    :type lindir: 3-Element Array of floats
    :param point: A second point.
    :type point: 3-Element Array of floats
    :return:
            Nearest point on the line to point,
            Distance between point and pnear
    :rtype: tuple
    """
    linpt = stypes.toDoubleVector(linpt)
    lindir = stypes.toDoubleVector(lindir)
    point = stypes.toDoubleVector(point)
    pnear = stypes.emptyDoubleVector(3)
    dist = ctypes.c_double()
    libspice.nplnpt_c(linpt, lindir, point, pnear, ctypes.byref(dist))
    return stypes.vectorToList(pnear), dist.value


@spiceErrorCheck
def nvc2pl(normal, constant):
    """
    Make a plane from a normal vector and a constant.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/nvc2pl_c.html

    :param normal: A normal vector defining a plane.
    :type normal: 3-Element Array of floats
    :param constant: A constant defining a plane.
    :type constant: float
    :return: plane
    :rtype: spiceypy.utils.support_types.Plane
    """
    plane = stypes.Plane()
    normal = stypes.toDoubleVector(normal)
    constant = ctypes.c_double(constant)
    libspice.nvc2pl_c(normal, constant, ctypes.byref(plane))
    return plane


@spiceErrorCheck
def nvp2pl(normal, point):
    """
    Make a plane from a normal vector and a point.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/nvp2pl_c.html

    :param normal: A normal vector defining a plane.
    :type normal: 3-Element Array of floats
    :param point: A point defining a plane.
    :type point: 3-Element Array of floats
    :return: plane
    :rtype: spiceypy.utils.support_types.Plane
    """
    normal = stypes.toDoubleVector(normal)
    point = stypes.toDoubleVector(point)
    plane = stypes.Plane()
    libspice.nvp2pl_c(normal, point, ctypes.byref(plane))
    return plane


################################################################################
# O

@spiceErrorCheck
def occult(target1, shape1, frame1, target2, shape2, frame2, abcorr, observer,
           et):
    """
    Determines the occultation condition (not occulted, partially,
    etc.) of one target relative to another target as seen by
    an observer at a given time.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/occult_c.html

    :param target1: Name or ID of first target.
    :type target1: str
    :param shape1: Type of shape model used for first target.
    :type shape1: str
    :param frame1: Body-fixed, body-centered frame for first body.
    :type frame1: str
    :param target2: Name or ID of second target.
    :type target2: str
    :param shape2: Type of shape model used for second target.
    :type shape2: str
    :param frame2: Body-fixed, body-centered frame for second body.
    :type frame2: str
    :param abcorr: Aberration correction flag.
    :type abcorr: str
    :param observer: Name or ID of the observer.
    :type observer: str
    :param et: Time of the observation (seconds past J2000).
    :type et: float
    :return: Occultation identification code.
    :rtype: int
    """
    target1 = stypes.stringToCharP(target1)
    shape1 = stypes.stringToCharP(shape1)
    frame1 = stypes.stringToCharP(frame1)
    target2 = stypes.stringToCharP(target2)
    shape2 = stypes.stringToCharP(shape2)
    frame2 = stypes.stringToCharP(frame2)
    abcorr = stypes.stringToCharP(abcorr)
    observer = stypes.stringToCharP(observer)
    et = ctypes.c_double(et)
    occult_code = ctypes.c_int()
    libspice.occult_c(target1, shape1, frame1, target2, shape2, frame2, abcorr,
                      observer, et, ctypes.byref(occult_code))
    return occult_code.value


@spiceErrorCheck
def ordc(item, inset):
    """
    The function returns the ordinal position of any given item in a
    character set.  If the item does not appear in the set, the function
    returns -1.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ordc_c.html

    :param item: An item to locate within a set.
    :type item: str
    :param inset: A set to search for a given item.
    :type inset: SpiceCharCell
    :return: the ordinal position of item within the set
    :rtype: int
    """
    assert isinstance(inset, stypes.SpiceCell)
    assert inset.is_char()
    assert isinstance(item, str)
    item = stypes.stringToCharP(item)
    return libspice.ordc_c(item, ctypes.byref(inset))


@spiceErrorCheck
def ordd(item, inset):
    """
    The function returns the ordinal position of any given item in a
    double precision set.  If the item does not appear in the set, the
    function returns -1.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ordd_c.html

    :param item: An item to locate within a set.
    :type item: float
    :param inset: A set to search for a given item.
    :type inset: SpiceDoubleCell
    :return: the ordinal position of item within the set
    :rtype: int
    """
    assert isinstance(inset, stypes.SpiceCell)
    assert inset.is_double()
    item = ctypes.c_double(item)
    return libspice.ordd_c(item, ctypes.byref(inset))


@spiceErrorCheck
def ordi(item, inset):
    """
    The function returns the ordinal position of any given item in an
    integer set.  If the item does not appear in the set, the function
    returns -1.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ordi_c.html

    :param item: An item to locate within a set.
    :type item: int
    :param inset: A set to search for a given item.
    :type inset: SpiceIntCell
    :return: the ordinal position of item within the set
    :rtype: int
    """
    assert isinstance(inset, stypes.SpiceCell)
    assert inset.is_int()
    assert isinstance(item, int)
    item = ctypes.c_int(item)
    return libspice.ordi_c(item, ctypes.byref(inset))


@spiceErrorCheck
def orderc(array, ndim=None):
    """
    Determine the order of elements in an array of character strings.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/orderc_c.html

    :param array: Input array.
    :type array: Array of strings.
    :param ndim: Optional Length of input array
    :type ndim: int
    :return: Order vector for array.
    :rtype: array of ints
    """
    if ndim is None:
        ndim = ctypes.c_int(len(array))
    else:
        ndim = ctypes.c_int(ndim)
    lenvals = ctypes.c_int(len(max(array, key=len)) + 1)
    iorder = stypes.emptyIntVector(ndim)
    array = stypes.listToCharArray(array, lenvals, ndim)
    libspice.orderc_c(lenvals, array, ndim, iorder)
    return stypes.vectorToList(iorder)


@spiceErrorCheck
def orderd(array, ndim=None):
    """
    Determine the order of elements in a double precision array.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/orderd_c.html

    :param array: Input array.
    :type array: Array of floats
    :param ndim: Optional Length of input array
    :type ndim: int
    :return: Order vector for array.
    :rtype: array of ints
    """
    if ndim is None:
        ndim = ctypes.c_int(len(array))
    else:
        ndim = ctypes.c_int(ndim)
    array = stypes.toDoubleVector(array)
    iorder = stypes.emptyIntVector(ndim)
    libspice.orderd_c(array, ndim, iorder)
    return stypes.vectorToList(iorder)


@spiceErrorCheck
def orderi(array, ndim=None):
    """
    Determine the order of elements in an integer array.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/orderi_c.html

    :param array: Input array.
    :type array: Array of ints
    :param ndim: Optional Length of input array
    :type ndim: int
    :return: Order vector for array.
    :rtype: array of ints
    """
    if ndim is None:
        ndim = ctypes.c_int(len(array))
    else:
        ndim = ctypes.c_int(ndim)
    array = stypes.toIntVector(array)
    iorder = stypes.emptyIntVector(ndim)
    libspice.orderi_c(array, ndim, iorder)
    return stypes.vectorToList(iorder)


@spiceErrorCheck
def oscelt(state, et, mu):
    """
    Determine the set of osculating conic orbital elements that
    corresponds to the state (position, velocity) of a body at
    some epoch.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/oscelt_c.html

    :param state: State of body at epoch of elements.
    :type state: Float Array of 6 elements.
    :param et: Epoch of elements.
    :type et: float
    :param mu: Gravitational parameter (GM) of primary body.
    :type mu: float
    :return: Equivalent conic elements
    :rtype: Float Array of 8 elements.
    """
    state = stypes.toDoubleVector(state)
    et = ctypes.c_double(et)
    mu = ctypes.c_double(mu)
    elts = stypes.emptyDoubleVector(8)
    libspice.oscelt_c(state, et, mu, elts)
    return stypes.vectorToList(elts)


################################################################################
# P


@spiceErrorCheck
def pckcov(pck, idcode, cover):
    """
    Find the coverage window for a specified reference frame in a
    specified binary PCK file.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pckcov_c.html

    :param pck: Name of PCK file.
    :type pck: str
    :param idcode: Class ID code of PCK reference frame.
    :type idcode: int
    :param cover: Window giving coverage in pck for idcode.
    :type cover: SpiceCell
    """
    pck = stypes.stringToCharP(pck)
    idcode = ctypes.c_int(idcode)
    assert isinstance(cover, stypes.SpiceCell)
    assert cover.dtype == 1
    libspice.pckcov_c(pck, idcode, ctypes.byref(cover))


@spiceErrorCheck
def pckfrm(pck, ids):
    """
    Find the set of reference frame class ID codes of all frames
    in a specified binary PCK file.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pckfrm_c.html

    :param pck: Name of PCK file.
    :type pck: str
    :param ids: Set of frame class ID codes of frames in PCK file.
    :type ids: SpiceCell
    """
    pck = stypes.stringToCharP(pck)
    assert isinstance(ids, stypes.SpiceCell)
    assert ids.dtype == 2
    libspice.pckfrm_c(pck, ctypes.byref(ids))


@spiceErrorCheck
def pcklof(filename):
    """
    Load a binary PCK file for use by the readers.  Return the
    handle of the loaded file which is used by other PCK routines to
    refer to the file.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pcklof_c.html

    :param filename: Name of the file to be loaded.
    :type filename: str
    :return: Loaded file's handle.
    :rtype: int
    """
    filename = stypes.stringToCharP(filename)
    handle = ctypes.c_int()
    libspice.pcklof_c(filename, ctypes.byref(handle))
    return handle.value


@spiceErrorCheck
def pckuof(handle):
    """
    Unload a binary PCK file so that it will no longer be searched by
    the readers.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pckuof_c.html

    :param handle: Handle of PCK file to be unloaded
    :type handle: int
    """
    handle = ctypes.c_int(handle)
    libspice.pckuof_c(handle)


@spiceErrorCheck
def pcpool(name, cvals):
    """
    This entry point provides toolkit programmers a method for
    programmatically inserting character data into the
    kernel pool.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pcpool_c.html

    :param name: The kernel pool name to associate with cvals.
    :type name: str
    :param cvals: An array of strings to insert into the kernel pool.
    :type cvals: Array of str
    """
    name = stypes.stringToCharP(name)
    lenvals = ctypes.c_int(len(max(cvals, key=len)) + 1)
    n = ctypes.c_int(len(cvals))
    cvals = stypes.listToCharArray(cvals, lenvals, n)
    libspice.pcpool_c(name, n, lenvals, cvals)


@spiceErrorCheck
def pdpool(name, dvals):
    """
    This entry point provides toolkit programmers a method for
    programmatically inserting double precision data into the
    kernel pool.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pdpool_c.html

    :param name: The kernel pool name to associate with dvals.
    :type name: str
    :param dvals: An array of values to insert into the kernel pool.
    :type dvals: SpiceCell
    """
    name = stypes.stringToCharP(name)
    n = ctypes.c_int(len(dvals))
    dvals = stypes.toDoubleVector(dvals)
    libspice.pdpool_c(name, n, dvals)


@spiceErrorCheck
def pgrrec(body, lon, lat, alt, re, f):
    """
    Convert planetographic coordinates to rectangular coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pgrrec_c.html

    :param body: Body with which coordinate system is associated.
    :type body: str
    :param lon: Planetographic longitude of a point (radians).
    :type lon: float
    :param lat: Planetographic latitude of a point (radians).
    :type lat: float
    :param alt: Altitude of a point above reference spheroid.
    :type alt: float
    :param re: Equatorial radius of the reference spheroid.
    :type re: float
    :param f: Flattening coefficient.
    :type f: float
    :return: Rectangular coordinates of the point.
    :rtype: 3-Element Array of floats
    """
    body = stypes.stringToCharP(body)
    lon = ctypes.c_double(lon)
    lat = ctypes.c_double(lat)
    alt = ctypes.c_double(alt)
    re = ctypes.c_double(re)
    f = ctypes.c_double(f)
    rectan = stypes.emptyDoubleVector(3)
    libspice.pgrrec_c(body, lon, lat, alt, re, f, rectan)
    return stypes.vectorToList(rectan)


@spiceErrorCheck
def phaseq(et, target, illmn, obsrvr, abcorr):
    """
    Compute the apparent phase angle for a target, observer,
    illuminator set of ephemeris objects.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/phaseq_c.html

    :param et: Ephemeris seconds past J2000 TDB.
    :type et: float
    :param target: Target body name.
    :type target: str
    :param illmn: Illuminating body name.
    :type illmn: str
    :param obsrvr: Observer body.
    :type obsrvr: str
    :param abcorr: Aberration correction flag.
    :type abcorr: str
    :return: Value of phase angle.
    :rtype: float
    """
    et = ctypes.c_double(et)
    target = stypes.stringToCharP(target)
    illmn = stypes.stringToCharP(illmn)
    obsrvr = stypes.stringToCharP(obsrvr)
    abcorr = stypes.stringToCharP(abcorr)
    return libspice.phaseq_c(et, target, illmn, obsrvr, abcorr)


@spiceErrorCheck
def pi():
    """
    Return the value of pi (the ratio of the circumference of
    a circle to its diameter).

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pi_c.html

    :return: value of pi.
    :rtype: float
    """
    return libspice.pi_c()


@spiceErrorCheck
def pipool(name, ivals):
    """
    This entry point provides toolkit programmers a method for
    programmatically inserting integer data into the kernel pool.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pipool_c.html

    :param name: The kernel pool name to associate with values.
    :type name: str
    :param ivals: An array of integers to insert into the pool.
    :type ivals: Array of ints
    """
    name = stypes.stringToCharP(name)
    n = ctypes.c_int(len(ivals))
    ivals = stypes.toIntVector(ivals)
    libspice.pipool_c(name, n, ivals)


@spiceErrorCheck
def pjelpl(elin, plane):
    """
    Project an ellipse onto a plane, orthogonally.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pjelpl_c.html

    :param elin: A SPICE ellipse to be projected.
    :type elin: spiceypy.utils.support_types.Ellipse
    :param plane: A plane onto which elin is to be projected.
    :type plane: supporttypes.Plane
    :return: A SPICE ellipse resulting from the projection.
    :rtype: spiceypy.utils.support_types.Ellipse
    """
    assert (isinstance(elin, stypes.Ellipse))
    assert (isinstance(plane, stypes.Plane))
    elout = stypes.Ellipse()
    libspice.pjelpl_c(ctypes.byref(elin), ctypes.byref(plane),
                      ctypes.byref(elout))
    return elout


@spiceErrorCheck
def pl2nvc(plane):
    """
    Return a unit normal vector and constant that define a specified plane.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pl2nvc_c.html

    :param plane: A SPICE plane.
    :type plane: supporttypes.Plane
    :return:
            A normal vector and constant defining
            the geometric plane represented by plane.
    :rtype: tuple
    """
    assert (isinstance(plane, stypes.Plane))
    normal = stypes.emptyDoubleVector(3)
    constant = ctypes.c_double()
    libspice.pl2nvc_c(ctypes.byref(plane), normal, ctypes.byref(constant))
    return stypes.vectorToList(normal), constant.value


@spiceErrorCheck
def pl2nvp(plane):
    """
    Return a unit normal vector and point that define a specified plane.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pl2nvp_c.html


    :param plane: A SPICE plane.
    :type plane: supporttypes.Plane
    :return: A unit normal vector and point that define plane.
    :rtype: tuple
    """
    assert (isinstance(plane, stypes.Plane))
    normal = stypes.emptyDoubleVector(3)
    point = stypes.emptyDoubleVector(3)
    libspice.pl2nvp_c(ctypes.byref(plane), normal, point)
    return stypes.vectorToList(normal), stypes.vectorToList(point)


@spiceErrorCheck
def pl2psv(plane):
    """
    Return a point and two orthogonal spanning vectors that generate
    a specified plane.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pl2psv_c.html

    :param plane: A SPICE plane.
    :type plane: supporttypes.Plane
    :return:
            A point in the input plane and two vectors
            spanning the input plane.
    :rtype: tuple
    """
    assert (isinstance(plane, stypes.Plane))
    point = stypes.emptyDoubleVector(3)
    span1 = stypes.emptyDoubleVector(3)
    span2 = stypes.emptyDoubleVector(3)
    libspice.pl2psv_c(ctypes.byref(plane), point, span1, span2)
    return stypes.vectorToList(point), stypes.vectorToList(
            span1), stypes.vectorToList(span2)


@spiceErrorCheck
def pos(string, substr, start):
    """
    Find the first occurrence in a string of a substring, starting at
    a specified location, searching forward.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pos_c.html

    :param string: Any character string.
    :type string: str
    :param substr: Substring to locate in the character string.
    :type substr: str
    :param start: Position to begin looking for substr in string.
    :type start: int
    :return:
            The index of the first occurrence of substr
            in string at or following index start.
    :rtype: int
    """
    string = stypes.stringToCharP(string)
    substr = stypes.stringToCharP(substr)
    start = ctypes.c_int(start)
    return libspice.pos_c(string, substr, start)


@spiceErrorCheck
def posr(string, substr, start):
    """
    Find the first occurrence in a string of a substring, starting at
    a specified location, searching backward.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/posr_c.html

    :param string: Any character string.
    :type string: str
    :param substr: Substring to locate in the character string.
    :type substr: str
    :param start: Position to begin looking for substr in string.
    :type start: int
    :return:
            The index of the last occurrence of substr
            in string at or preceding index start.
    :rtype: int
    """
    string = stypes.stringToCharP(string)
    substr = stypes.stringToCharP(substr)
    start = ctypes.c_int(start)
    return libspice.posr_c(string, substr, start)


# prompt,
# skip for no as this is not really an important function for python users


@spiceErrorCheck
def prop2b(gm, pvinit, dt):
    """
    Given a central mass and the state of massless body at time t_0,
    this routine determines the state as predicted by a two-body
    force model at time t_0 + dt.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/prop2b_c.html

    :param gm: Gravity of the central mass.
    :type gm: float
    :param pvinit: Initial state from which to propagate a state.
    :type pvinit: 6-Element Array of floats
    :param dt: Time offset from initial state to propagate to.
    :type dt: float
    :return: The propagated state.
    :rtype: 6-Element Array of floats
    """
    gm = ctypes.c_double(gm)
    pvinit = stypes.toDoubleVector(pvinit)
    dt = ctypes.c_double(dt)
    pvprop = stypes.emptyDoubleVector(6)
    libspice.prop2b_c(gm, pvinit, dt, pvprop)
    return stypes.vectorToList(pvprop)


@spiceErrorCheck
def prsdp(string):
    """
    Parse a string as a double precision number, encapsulating error handling.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/prsdp_c.html

    :param string: String representing a d.p. number.
    :type string: str
    :return: D.p. value obtained by parsing string.
    :rtype: float
    """
    string = stypes.stringToCharP(string)
    dpval = ctypes.c_double()
    libspice.prsdp_c(string, ctypes.byref(dpval))
    return dpval.value


@spiceErrorCheck
def prsint(string):
    """
    Parse a string as an integer, encapsulating error handling.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/prsint_c.html

    :param string: String representing an integer.
    :type string: str
    :return: Integer value obtained by parsing string.
    :rtype: int
    """
    string = stypes.stringToCharP(string)
    intval = ctypes.c_int()
    libspice.prsint_c(string, ctypes.byref(intval))
    return intval.value


@spiceErrorCheck
def psv2pl(point, span1, span2):
    """
    Make a CSPICE plane from a point and two spanning vectors.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/psv2pl_c.html

    :param point: A Point.
    :type point: 3-Element Array of floats
    :param span1: First Spanning vector.
    :type span1: 3-Element Array of floats
    :param span2: Second Spanning vector.
    :type span2: 3-Element Array of floats
    :return: A SPICE plane.
    :rtype: supportypes.Plane
    """
    point = stypes.toDoubleVector(point)
    span1 = stypes.toDoubleVector(span1)
    span2 = stypes.toDoubleVector(span2)
    plane = stypes.Plane()
    libspice.psv2pl_c(point, span1, span2, ctypes.byref(plane))
    return plane


# skip putcml, is this really needed for python users?


@spiceErrorCheck
def pxform(fromstr, tostr, et):
    """
    Return the matrix that transforms position vectors from one
    specified frame to another at a specified epoch.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pxform_c.html

    :param fromstr: Name of the frame to transform from.
    :type fromstr: str
    :param tostr: Name of the frame to transform to.
    :type tostr: str
    :param et: Epoch of the rotation matrix.
    :type et: float
    :return: A rotation matrix.
    :rtype: 3x3 Element Array of floats
    """
    et = ctypes.c_double(et)
    tostr = stypes.stringToCharP(tostr)
    fromstr = stypes.stringToCharP(fromstr)
    rotatematrix = stypes.emptyDoubleMatrix()
    libspice.pxform_c(fromstr, tostr, et, rotatematrix)
    return stypes.matrixToList(rotatematrix)


@spiceErrorCheck
def pxfrm2(frame_from, frame_to, etfrom, etto):
    """
    Return the 3x3 matrix that transforms position vectors from one
    specified frame at a specified epoch to another specified
    frame at another specified epoch.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/pxfrm2_c.html

    :param frame_from: Name of the frame to transform from.
    :type frame_from: str
    :param frame_to: Name of the frame to transform to.
    :type frame_to: str
    :param etfrom: Evaluation time of frame_from.
    :type etfrom: float
    :param etto: Evaluation time of frame_to.
    :type etto: float
    :return: A position transformation matrix from frame_from to frame_to
    :rtype: 3x3 Element Array of floats
    """
    frame_from = stypes.stringToCharP(frame_from)
    frame_to = stypes.stringToCharP(frame_to)
    etfrom = ctypes.c_double(etfrom)
    etto = ctypes.c_double(etto)
    outmatrix = stypes.emptyDoubleMatrix()
    libspice.pxfrm2_c(frame_from, frame_to, etfrom, etto, outmatrix)
    return stypes.matrixToList(outmatrix)


################################################################################
# Q


@spiceErrorCheck
def q2m(q):
    """
    Find the rotation matrix corresponding to a specified unit quaternion.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/q2m_c.html

    :param q: A unit quaternion.
    :type q: 4-Element Array of floats
    :return: A rotation matrix corresponding to q
    :rtype: 3x3-Element Array of floats
    """
    q = stypes.toDoubleVector(q)
    mout = stypes.emptyDoubleMatrix()
    libspice.q2m_c(q, mout)
    return stypes.matrixToList(mout)


# @spiceErrorCheck
def qcktrc(tracelen=_default_len_out):
    """
    Return a string containing a traceback.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/qcktrc_c.html

    :param tracelen: Maximum length of output traceback string.
    :type tracelen: int
    :return: A traceback string.
    :rtype: str
    """
    tracestr = stypes.stringToCharP(tracelen)
    tracelen = ctypes.c_int(tracelen)
    libspice.qcktrc_c(tracelen, tracestr)
    return stypes.toPythonString(tracestr)


@spiceErrorCheck
def qdq2av(q, dq):
    """
    Derive angular velocity from a unit quaternion and its derivative
    with respect to time.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/qdq2av_c.html

    :param q: Unit SPICE quaternion.
    :type q: 4-Element Array of floats
    :param dq: Derivative of q with respect to time
    :type dq: 4-Element Array of floats
    :return: Angular velocity defined by q and dq.
    :rtype: 3-Element Array of floats
    """
    q = stypes.toDoubleVector(q)
    dq = stypes.toDoubleVector(dq)
    vout = stypes.emptyDoubleVector(3)
    libspice.qdq2av_c(q, dq, vout)
    return stypes.vectorToList(vout)


@spiceErrorCheck
def qxq(q1, q2):
    """
    Multiply two quaternions.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/qxq_c.html

    :param q1: First SPICE quaternion.
    :type q1: 4-Element Array of floats
    :param q2: Second SPICE quaternion.
    :type q2: 4-Element Array of floats
    :return: Product of q1 and q2.
    :rtype: 4-Element Array of floats
    """
    q1 = stypes.toDoubleVector(q1)
    q2 = stypes.toDoubleVector(q2)
    vout = stypes.emptyDoubleVector(4)
    libspice.qxq_c(q1, q2, vout)
    return stypes.vectorToList(vout)


################################################################################
# R


@spiceErrorCheck
def radrec(inrange, re, dec):
    """
    Convert from range, right ascension, and declination to rectangular
    coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/radrec_c.html

    :param inrange: Distance of a point from the origin.
    :type inrange: float
    :param re: Right ascension of point in radians.
    :type re: float
    :param dec: Declination of point in radians.
    :type dec: float
    :return: Rectangular coordinates of the point.
    :rtype: 3-Element Array of floats
    """
    inrange = ctypes.c_double(inrange)
    re = ctypes.c_double(re)
    dec = ctypes.c_double(dec)
    rectan = stypes.emptyDoubleVector(3)
    libspice.radrec_c(inrange, re, dec, rectan)
    return stypes.vectorToList(rectan)


@spiceErrorCheck
def rav2xf(rot, av):
    """
    This routine determines a state transformation matrix
    from a rotation matrix and the angular velocity of the
    rotation.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/rav2xf_c.html

    :param rot: Rotation matrix.
    :type rot: 3x3-Element Array of floats
    :param av: Angular velocity vector.
    :type av: 3-Element Array of floats
    :return: State transformation associated with rot and av.
    :rtype: 6x6-Element Array of floats
    """
    rot = stypes.toDoubleMatrix(rot)
    av = stypes.toDoubleVector(av)
    xform = stypes.emptyDoubleMatrix(x=6, y=6)
    libspice.rav2xf_c(rot, av, xform)
    return stypes.matrixToList(xform)


@spiceErrorCheck
def raxisa(matrix):
    """
    Compute the axis of the rotation given by an input matrix
    and the angle of the rotation about that axis.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/raxisa_c.html

    :param matrix: Rotation matrix.
    :type matrix: 3x3-Element Array of floats
    :return: Axis of the rotation, Angle through which the rotation is performed
    :rtype: tuple
    """
    matrix = stypes.listtodoublematrix(matrix)
    axis = stypes.emptyDoubleVector(3)
    angle = ctypes.c_double()
    libspice.raxisa_c(matrix, axis, ctypes.byref(angle))
    return stypes.vectorToList(axis), angle.value


@spiceErrorCheck
def rdtext(file, lenout=_default_len_out):  # pragma: no cover
    """
    Read the next line of text from a text file.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/rdtext_c.html

    :param file: Name of text file.
    :type file: str
    :param lenout: Available room in output line.
    :type lenout: int
    :return: Next line from the text file, End-of-file indicator
    :rtype: tuple
    """
    file = stypes.stringToCharP(file)
    line = stypes.stringToCharP(lenout)
    lenout = ctypes.c_int(lenout)
    eof = ctypes.c_bool()
    libspice.rdtext_c(file, lenout, line, ctypes.byref(eof))
    return stypes.toPythonString(line), eof.value


@spiceErrorCheck
def reccyl(rectan):
    """
    Convert from rectangular to cylindrical coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/reccyl_c.html

    :param rectan: Rectangular coordinates of a point.
    :type rectan: 3-Element Array of floats
    :return:
            Distance from z axis,
            Angle (radians) from xZ plane,
            Height above xY plane.
    :rtype: tuple
    """
    rectan = stypes.toDoubleVector(rectan)
    radius = ctypes.c_double(0)
    lon = ctypes.c_double(0)
    z = ctypes.c_double(0)
    libspice.reccyl_c(rectan, ctypes.byref(radius), ctypes.byref(lon),
                      ctypes.byref(z))
    return radius.value, lon.value, z.value


@spiceErrorCheck
def recgeo(rectan, re, f):
    """
    Convert from rectangular coordinates to geodetic coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/recgeo_c.html

    :param rectan: Rectangular coordinates of a point.
    :type rectan: 3-Element Array of floats
    :param re: Equatorial radius of the reference spheroid.
    :type re: float
    :param f: Flattening coefficient.
    :type f: float
    :return:
            Geodetic longitude (radians),
            Geodetic latitude (radians),
            Altitude above reference spheroid
    :rtype: tuple
    """
    rectan = stypes.toDoubleVector(rectan)
    re = ctypes.c_double(re)
    f = ctypes.c_double(f)
    longitude = ctypes.c_double(0)
    latitude = ctypes.c_double(0)
    alt = ctypes.c_double(0)
    libspice.recgeo_c(rectan, re, f, ctypes.byref(longitude),
                      ctypes.byref(latitude), ctypes.byref(alt))
    return longitude.value, latitude.value, alt.value


@spiceErrorCheck
def reclat(rectan):
    """
    Convert from rectangular coordinates to latitudinal coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/reclat_c.html

    :param rectan: Rectangular coordinates of a point.
    :type rectan: 3-Element Array of floats
    :return: Distance from the origin, Longitude in radians, Latitude in radians
    :rtype: tuple
    """
    rectan = stypes.toDoubleVector(rectan)
    radius = ctypes.c_double(0)
    longitude = ctypes.c_double(0)
    latitude = ctypes.c_double(0)
    libspice.reclat_c(rectan, ctypes.byref(radius), ctypes.byref(longitude),
                      ctypes.byref(latitude))
    return radius.value, longitude.value, latitude.value


@spiceErrorCheck
def recpgr(body, rectan, re, f):
    """
    Convert rectangular coordinates to planetographic coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/recpgr_c.html

    :param body: Body with which coordinate system is associated.
    :type body: str
    :param rectan: Rectangular coordinates of a point.
    :type rectan: 3-Element Array of floats
    :param re: Equatorial radius of the reference spheroid.
    :type re: float
    :param f: Flattening coefficient.
    :type f: float
    :return:
            Planetographic longitude (radians),
            Planetographic latitude (radians),
            Altitude above reference spheroid
    :rtype: tuple
    """
    body = stypes.stringToCharP(body)
    rectan = stypes.toDoubleVector(rectan)
    re = ctypes.c_double(re)
    f = ctypes.c_double(f)
    lon = ctypes.c_double()
    lat = ctypes.c_double()
    alt = ctypes.c_double()
    libspice.recpgr_c(body, rectan, re, f, ctypes.byref(lon), ctypes.byref(lat),
                      ctypes.byref(alt))
    return lon.value, lat.value, alt.value


@spiceErrorCheck
def recrad(rectan):
    """
    Convert rectangular coordinates to range, right ascension, and declination.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/recrad_c.html

    :param rectan: Rectangular coordinates of a point.
    :type rectan: 3-Element Array of floats
    :return:
            Distance of the point from the origin,
            Right ascension in radians,
            Declination in radians
    :rtype: tuple
    """
    rectan = stypes.toDoubleVector(rectan)
    outrange = ctypes.c_double()
    ra = ctypes.c_double()
    dec = ctypes.c_double()
    libspice.recrad_c(rectan, ctypes.byref(outrange), ctypes.byref(ra),
                      ctypes.byref(dec))
    return outrange.value, ra.value, dec.value


@spiceErrorCheck
def recsph(rectan):
    """
    Convert from rectangular coordinates to spherical coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/recrad_c.html

    :param rectan: Rectangular coordinates of a point.
    :type rectan: 3-Element Array of floats
    :return:
            Distance from the origin,
            Angle from the positive Z-axis,
            Longitude in radians.
    :rtype: tuple
    """
    rectan = stypes.toDoubleVector(rectan)
    r = ctypes.c_double()
    colat = ctypes.c_double()
    lon = ctypes.c_double()
    libspice.recsph_c(rectan, ctypes.byref(r), ctypes.byref(colat),
                      ctypes.byref(lon))
    return r.value, colat.value, lon.value


@spiceErrorCheck
def removc(item, inset):
    """
    Remove an item from a character set.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/removc_c.html

    :param item: Item to be removed.
    :type item: str
    :param inset: Set to be updated.
    :type inset: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(inset, stypes.SpiceCell)
    assert inset.dtype == 0
    item = stypes.stringToCharP(item)
    libspice.removc_c(item, ctypes.byref(inset))


@spiceErrorCheck
def removd(item, inset):
    """
    Remove an item from a double precision set.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/removd_c.html

    :param item: Item to be removed.
    :type item: float
    :param inset: Set to be updated.
    :type inset: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(inset, stypes.SpiceCell)
    assert inset.dtype == 1
    item = ctypes.c_double(item)
    libspice.removd_c(item, ctypes.byref(inset))


@spiceErrorCheck
def removi(item, inset):
    """
    Remove an item from an integer set.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/removi_c.html

    :param item: Item to be removed.
    :type item: int
    :param inset: Set to be updated.
    :type inset: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(inset, stypes.SpiceCell)
    assert inset.dtype == 2
    item = ctypes.c_int(item)
    libspice.removi_c(item, ctypes.byref(inset))


@spiceErrorCheck
def reordc(iorder, ndim, lenvals, array):
    """
    Re-order the elements of an array of character strings
    according to a given order vector.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/reordc_c.html

    :param iorder: Order vector to be used to re-order array.
    :type iorder: Array of ints
    :param ndim: Dimension of array.
    :type ndim: int
    :param lenvals: String length.
    :type lenvals: int
    :param array: Array to be re-ordered.
    :type array: Array of strs
    :return: Re-ordered Array.
    :rtype: Array of strs
    """
    iorder = stypes.toIntVector(iorder)
    array = stypes.listToCharArray(array)
    ndim = ctypes.c_int(ndim)
    lenvals = ctypes.c_int(lenvals)
    libspice.reordc_c(iorder, ndim, lenvals, array)
    return [stypes.toPythonString(x.value) for x in array]


@spiceErrorCheck
def reordd(iorder, ndim, array):
    """
    Re-order the elements of a double precision array according to
    a given order vector.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/reordd_c.html

    :param iorder: Order vector to be used to re-order array.
    :type iorder: Array of ints
    :param ndim: Dimension of array.
    :type ndim: int
    :param array: Array to be re-ordered.
    :type array: Array of floats
    :return: Re-ordered Array.
    :rtype: Array of floats
    """
    iorder = stypes.toIntVector(iorder)
    ndim = ctypes.c_int(ndim)
    array = stypes.toDoubleVector(array)
    libspice.reordd_c(iorder, ndim, array)
    return stypes.vectorToList(array)


@spiceErrorCheck
def reordi(iorder, ndim, array):
    """
    Re-order the elements of an integer array according to
    a given order vector.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/reordi_c.html

    :param iorder: Order vector to be used to re-order array.
    :type iorder: Array of ints
    :param ndim: Dimension of array.
    :type ndim: int
    :param array: Array to be re-ordered.
    :type array: Array of ints
    :return: Re-ordered Array.
    :rtype: Array of ints
    """
    iorder = stypes.toIntVector(iorder)
    ndim = ctypes.c_int(ndim)
    array = stypes.toIntVector(array)
    libspice.reordi_c(iorder, ndim, array)
    return stypes.vectorToList(array)


@spiceErrorCheck
def reordl(iorder, ndim, array):
    """
    Re-order the elements of a logical (Boolean) array according to
    a given order vector.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/reordl_c.html

    :param iorder: Order vector to be used to re-order array.
    :type iorder: Array of ints
    :param ndim: Dimension of array.
    :type ndim: int
    :param array: Array to be re-ordered.
    :type array: Array of ints
    :return: Re-ordered Array.
    :rtype: Array of bools
    """
    iorder = stypes.toIntVector(iorder)
    ndim = ctypes.c_int(ndim)
    array = stypes.toBoolVector(array)
    libspice.reordl_c(iorder, ndim, array)
    return stypes.vectorToList(array)


@spiceErrorCheck
def repmc(instr, marker, value, lenout=None):
    """
    Replace a marker with a character string.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/repmc_c.html

    :param instr: Input string.
    :type instr: str
    :param marker: Marker to be replaced.
    :type marker: str
    :param value: Replacement value.
    :type value: str
    :param lenout: Optional available space in output string
    :type lenout: int
    :return: Output string.
    :rtype: str
    """
    if lenout is None:
        lenout = ctypes.c_int(len(instr) + len(value) + len(marker) + 15)
    instr = stypes.stringToCharP(instr)
    marker = stypes.stringToCharP(marker)
    value = stypes.stringToCharP(value)
    out = stypes.stringToCharP(lenout)
    libspice.repmc_c(instr, marker, value, lenout, out)
    return stypes.toPythonString(out)


@spiceErrorCheck
def repmct(instr, marker, value, repcase, lenout=None):
    """
    Replace a marker with the text representation of a
    cardinal number.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/repmc_c.html

    :param instr: Input string.
    :type instr: str
    :param marker: Marker to be replaced.
    :type marker: str
    :param value: Replacement value.
    :type value: int
    :param repcase: Case of replacement text.
    :type repcase: str
    :param lenout: Optional available space in output string
    :type lenout: int
    :return: Output string.
    :rtype: str
    """
    if lenout is None:
        lenout = ctypes.c_int(len(instr) + len(marker) + 15)
    instr = stypes.stringToCharP(instr)
    marker = stypes.stringToCharP(marker)
    value = ctypes.c_int(value)
    repcase = ctypes.c_char(repcase.encode(encoding='UTF-8'))
    out = stypes.stringToCharP(lenout)
    libspice.repmct_c(instr, marker, value, repcase, lenout, out)
    return stypes.toPythonString(out)


@spiceErrorCheck
def repmd(instr, marker, value, sigdig):
    """
    Replace a marker with a double precision number.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/repmd_c.html

    :param instr: Input string.
    :type instr: str
    :param marker: Marker to be replaced.
    :type marker: str
    :param value: Replacement value.
    :type value: float
    :param sigdig: Significant digits in replacement text.
    :type sigdig: int
    :return: Output string.
    :rtype: str
    """
    lenout = ctypes.c_int(len(instr) + len(marker) + 15)
    instr = stypes.stringToCharP(instr)
    marker = stypes.stringToCharP(marker)
    value = ctypes.c_double(value)
    sigdig = ctypes.c_int(sigdig)
    out = stypes.stringToCharP(lenout)
    libspice.repmd_c(instr, marker, value, sigdig, lenout, out)
    return stypes.toPythonString(out)


@spiceErrorCheck
def repmf(instr, marker, value, sigdig, informat, lenout=None):
    """
    Replace a marker in a string with a formatted double precision value.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/repmf_c.html

    :param instr: Input string.
    :type instr: str
    :param marker: Marker to be replaced.
    :type marker: str
    :param value: Replacement value.
    :type value: float
    :param sigdig: Significant digits in replacement text.
    :type sigdig: int
    :param informat: Format 'E' or 'F'.
    :type informat: str
    :param lenout: Optional available space in output string.
    :type lenout: int
    :return: Output string.
    :rtype: str
    """
    if lenout is None:
        lenout = ctypes.c_int(len(instr) + len(marker) + 15)
    instr = stypes.stringToCharP(instr)
    marker = stypes.stringToCharP(marker)
    value = ctypes.c_double(value)
    sigdig = ctypes.c_int(sigdig)
    informat = ctypes.c_char(informat.encode(encoding='UTF-8'))
    out = stypes.stringToCharP(lenout)
    libspice.repmf_c(instr, marker, value, sigdig, informat, lenout, out)
    return stypes.toPythonString(out)


@spiceErrorCheck
def repmi(instr, marker, value, lenout=None):
    """
    Replace a marker with an integer.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/repmi_c.html

    :param instr: Input string.
    :type instr: str
    :param marker: Marker to be replaced.
    :type marker: str
    :param value: Replacement value.
    :type value: int
    :param lenout: Optional available space in output string.
    :type lenout: int
    :return: Output string.
    :rtype: str
    """
    if lenout is None:
        lenout = ctypes.c_int(len(instr) + len(marker) + 15)
    instr = stypes.stringToCharP(instr)
    marker = stypes.stringToCharP(marker)
    value = ctypes.c_int(value)
    out = stypes.stringToCharP(lenout)
    libspice.repmi_c(instr, marker, value, lenout, out)
    return stypes.toPythonString(out)


@spiceErrorCheck
def repmot(instr, marker, value, repcase, lenout=None):
    """
    Replace a marker with the text representation of an ordinal number.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/repmot_c.html

    :param instr: Input string.
    :type instr: str
    :param marker: Marker to be replaced.
    :type marker: str
    :param value: Replacement value.
    :type value: int
    :param repcase: Case of replacement text.
    :type repcase: str
    :param lenout: Optional available space in output string.
    :type lenout: int
    :return: Output string.
    :rtype: str
    """
    if lenout is None:
        lenout = ctypes.c_int(len(instr) + len(marker) + 15)
    instr = stypes.stringToCharP(instr)
    marker = stypes.stringToCharP(marker)
    value = ctypes.c_int(value)
    repcase = ctypes.c_char(repcase.encode(encoding='UTF-8'))
    out = stypes.stringToCharP(lenout)
    libspice.repmot_c(instr, marker, value, repcase, lenout, out)
    return stypes.toPythonString(out)


def reset():
    """
    Reset the SPICE error status to a value of "no error."
    As a result, the status routine, failed, will return a value
    of False

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/reset_c.html

    """
    libspice.reset_c()


@spiceErrorCheck
def return_c():
    """
    True if SPICE routines should return immediately upon entry.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/return_c.html

    :return: True if SPICE routines should return immediately upon entry.
    :rtype: bool
    """
    return libspice.return_c()


@spiceErrorCheck
def rotate(angle, iaxis):
    """
    Calculate the 3x3 rotation matrix generated by a rotation
    of a specified angle about a specified axis. This rotation
    is thought of as rotating the coordinate system.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/rotate_c.html

    :param angle: Angle of rotation (radians).
    :type angle: float
    :param iaxis: Axis of rotation X=1, Y=2, Z=3.
    :type iaxis: int
    :return: Resulting rotation matrix
    :rtype: 3x3-Element Array of floats
    """
    angle = ctypes.c_double(angle)
    iaxis = ctypes.c_int(iaxis)
    mout = stypes.emptyDoubleMatrix()
    libspice.rotate_c(angle, iaxis, mout)
    return stypes.matrixToList(mout)


@spiceErrorCheck
def rotmat(m1, angle, iaxis):
    """
    Rotmat applies a rotation of angle radians about axis iaxis to a
    matrix. This rotation is thought of as rotating the coordinate
    system.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/rotmat_c.html

    :param m1: Matrix to be rotated.
    :type m1: 3x3-Element Array of floats
    :param angle: Angle of rotation (radians).
    :type angle: float
    :param iaxis: Axis of rotation X=1, Y=2, Z=3.
    :type iaxis: int
    :return: Resulting rotated matrix.
    :rtype: 3x3-Element Array of floats
    """
    m1 = stypes.listtodoublematrix(m1)
    angle = ctypes.c_double(angle)
    iaxis = ctypes.c_int(iaxis)
    mout = stypes.emptyDoubleMatrix()
    libspice.rotmat_c(m1, angle, iaxis, mout)
    return stypes.matrixToList(mout)


@spiceErrorCheck
def rotvec(v1, angle, iaxis):
    """
    Transform a vector to a new coordinate system rotated by angle
    radians about axis iaxis.  This transformation rotates v1 by
    angle radians about the specified axis.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/rotvec_c.html

    :param v1: Vector whose coordinate system is to be rotated.
    :type v1: 3-Element Array of floats
    :param angle: Angle of rotation (radians).
    :type angle: float
    :param iaxis: Axis of rotation X=1, Y=2, Z=3.
    :type iaxis: int
    :return: the vector expressed in the new coordinate system.
    :rtype: 3-Element Array of floats
    """
    v1 = stypes.toDoubleVector(v1)
    angle = ctypes.c_double(angle)
    iaxis = ctypes.c_int(iaxis)
    vout = stypes.emptyDoubleVector(3)
    libspice.rotvec_c(v1, angle, iaxis, vout)
    return stypes.vectorToList(vout)


@spiceErrorCheck
def rpd():
    """
    Return the number of radians per degree.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/rpd_c.html

    :return: The number of radians per degree, pi/180.
    :rtype: float
    """
    return libspice.rpd_c()


@spiceErrorCheck
def rquad(a, b, c):
    """
    Find the roots of a quadratic equation.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/rquad_c.html

    :param a: Coefficient of quadratic term.
    :type a: float
    :param b: Coefficient of linear term.
    :type b: float
    :param c: Constant.
    :type c: float
    :return: Root built from positive and negative discriminant term.
    :rtype: tuple
    """
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    root1 = stypes.emptyDoubleVector(2)
    root2 = stypes.emptyDoubleVector(2)
    libspice.rquad_c(a, b, c, root1, root2)
    return stypes.vectorToList(root1), stypes.vectorToList(root2)


################################################################################
# S


@spiceErrorCheck
def saelgv(vec1, vec2):
    """
    Find semi-axis vectors of an ellipse generated by two arbitrary
    three-dimensional vectors.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/saelgv_c.html

    :param vec1: First vector used to generate an ellipse.
    :type vec1: 3-Element Array of floats
    :param vec2: Second vector used to generate an ellipse.
    :type vec2: 3-Element Array of floats
    :return: Semi-major axis of ellipse, Semi-minor axis of ellipse.
    :rtype: tuple
    """
    vec1 = stypes.toDoubleVector(vec1)
    vec2 = stypes.toDoubleVector(vec2)
    smajor = stypes.emptyDoubleVector(3)
    sminor = stypes.emptyDoubleVector(3)
    libspice.saelgv_c(vec1, vec2, smajor, sminor)
    return stypes.vectorToList(smajor), stypes.vectorToList(sminor)


@spiceErrorCheck
def scard(incard, cell):
    """
    Set the cardinality of a SPICE cell of any data type.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scard_c.html

    :param incard: Cardinality of (number of elements in) the cell.
    :type incard: int
    :param cell: The cell.
    :type cell: spiceypy.utils.support_types.SpiceCell
    :return: The updated Cell.
    :rtype: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(cell, stypes.SpiceCell)
    incard = ctypes.c_int(incard)
    libspice.scard_c(incard, ctypes.byref(cell))
    return cell


@spiceErrorCheck
def scdecd(sc, sclkdp, lenout=_default_len_out, MXPART=None):
    # todo: figure out how to use mxpart, and test scdecd
    """
    Convert double precision encoding of spacecraft clock time into
    a character representation.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scdecd_c.html

    :param sc: NAIF spacecraft identification code.
    :type sc: int
    :param sclkdp: Encoded representation of a spacecraft clock count.
    :type sclkdp: float
    :param lenout: Maximum allowed length of output SCLK string.
    :type lenout: int
    :param MXPART: Maximum number of spacecraft clock partitions.
    :type MXPART: int
    :return: Character representation of a clock count.
    :rtype: str
    """
    sc = ctypes.c_int(sc)
    sclkdp = ctypes.c_double(sclkdp)
    sclkch = stypes.stringToCharP(" " * lenout)
    lenout = ctypes.c_int(lenout)
    libspice.scdecd_c(sc, sclkdp, lenout, sclkch)
    return stypes.toPythonString(sclkch)


@spiceErrorCheck
def sce2c(sc, et):
    """
    Convert ephemeris seconds past J2000 (ET) to continuous encoded
    spacecraft clock "ticks".  Non-integral tick values may be
    returned.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sce2c_c.html

    :param sc: NAIF spacecraft ID code.
    :type sc: int
    :param et: Ephemeris time, seconds past J2000.
    :type et: float
    :return:
            SCLK, encoded as ticks since spacecraft clock start.
            sclkdp need not be integral.
    :rtype: float
    """
    sc = ctypes.c_int(sc)
    et = ctypes.c_double(et)
    sclkdp = ctypes.c_double()
    libspice.sce2c_c(sc, et, ctypes.byref(sclkdp))
    return sclkdp.value


@spiceErrorCheck
def sce2s(sc, et, lenout=_default_len_out):
    """
    Convert an epoch specified as ephemeris seconds past J2000 (ET) to a
    character string representation of a spacecraft clock value (SCLK).

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sce2s_c.html

    :param sc: NAIF spacecraft clock ID code.
    :type sc: int
    :param et: Ephemeris time, specified as seconds past J2000.
    :type et: float
    :param lenout: Maximum length of output string.
    :type lenout: int
    :return: An SCLK string.
    :rtype: str
    """
    sc = ctypes.c_int(sc)
    et = ctypes.c_double(et)
    sclkch = stypes.stringToCharP(" " * lenout)
    lenout = ctypes.c_int(lenout)
    libspice.sce2s_c(sc, et, lenout, sclkch)
    return stypes.toPythonString(sclkch)


@spiceErrorCheck
def sce2t(sc, et):
    """
    Convert ephemeris seconds past J2000 (ET) to integral
    encoded spacecraft clock ("ticks"). For conversion to
    fractional ticks, (required for C-kernel production), see
    the routine :func:`sce2c`.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sce2t_c.html

    :param sc: NAIF spacecraft ID code.
    :type sc: int
    :param et: Ephemeris time, seconds past J2000.
    :type et: float
    :return: SCLK, encoded as ticks since spacecraft clock start.
    :rtype: float
    """
    sc = ctypes.c_int(sc)
    et = ctypes.c_double(et)
    sclkdp = ctypes.c_double()
    libspice.sce2t_c(sc, et, ctypes.byref(sclkdp))
    return sclkdp.value


@spiceErrorCheck
def scencd(sc, sclkch, MXPART=None):
    """
    Encode character representation of spacecraft clock time into a
    double precision number.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scencd_c.html

    :param sc: NAIF spacecraft identification code.
    :type sc: int
    :param sclkch: Character representation of a spacecraft clock.
    :type sclkch: str
    :param MXPART: Maximum number of spacecraft clock partitions.
    :type MXPART: int
    :return: Encoded representation of the clock count.
    :rtype: float
    """
    sc = ctypes.c_int(sc)
    sclkch = stypes.stringToCharP(sclkch)
    sclkdp = ctypes.c_double()
    libspice.scencd_c(sc, sclkch, ctypes.byref(sclkdp))
    return sclkdp.value


@spiceErrorCheck
def scfmt(sc, ticks, lenout=_default_len_out):
    """
    Convert encoded spacecraft clock ticks to character clock format.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scfmt_c.html

    :param sc: NAIF spacecraft identification code.
    :type sc: int
    :param ticks: Encoded representation of a spacecraft clock count.
    :type ticks: float
    :param lenout: Maximum allowed length of output string.
    :type lenout: int
    :return: Character representation of a clock count.
    :rtype: str
    """
    sc = ctypes.c_int(sc)
    ticks = ctypes.c_double(ticks)
    clkstr = stypes.stringToCharP(lenout)
    lenout = ctypes.c_int(lenout)
    libspice.scfmt_c(sc, ticks, lenout, clkstr)
    return stypes.toPythonString(clkstr)


@spiceErrorCheck
def scpart(sc):
    """
    Get spacecraft clock partition information from a spacecraft
    clock kernel file.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scpart_c.html

    :param sc: NAIF spacecraft identification code.
    :type sc: int
    :return:
            The number of spacecraft clock partitions,
            Array of partition start times,
            Array of partition stop times.
    :rtype: tuple
    """
    sc = ctypes.c_int(sc)
    nparts = ctypes.c_int()
    pstart = stypes.emptyDoubleVector(9999)
    pstop = stypes.emptyDoubleVector(9999)
    libspice.scpart_c(sc, nparts, pstart, pstop)
    return stypes.vectorToList(pstart)[0:nparts.value], stypes.vectorToList(
            pstop)[0:nparts.value]


@spiceErrorCheck
def scs2e(sc, sclkch):
    """
    Convert a spacecraft clock string to ephemeris seconds past J2000 (ET).

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/scs2e_c.html

    :param sc: NAIF integer code for a spacecraft.
    :type sc: int
    :param sclkch: An SCLK string.
    :type sclkch: str
    :return: Ephemeris time, seconds past J2000.
    :rtype: float
    """
    sc = ctypes.c_int(sc)
    sclkch = stypes.stringToCharP(sclkch)
    et = ctypes.c_double()
    libspice.scs2e_c(sc, sclkch, ctypes.byref(et))
    return et.value


@spiceErrorCheck
def sct2e(sc, sclkdp):
    """
    Convert encoded spacecraft clock ("ticks") to ephemeris
    seconds past J2000 (ET).

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sct2e_c.html

    :param sc: NAIF spacecraft ID code.
    :type sc: int
    :param sclkdp: SCLK, encoded as ticks since spacecraft clock start.
    :type sclkdp: float
    :return: Ephemeris time, seconds past J2000.
    :rtype: float
    """
    sc = ctypes.c_int(sc)
    sclkdp = ctypes.c_double(sclkdp)
    et = ctypes.c_double()
    libspice.sct2e_c(sc, sclkdp, ctypes.byref(et))
    return et.value


@spiceErrorCheck
def sctiks(sc, clkstr):
    """
    Convert a spacecraft clock format string to number of "ticks".

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sctiks_c.html

    :param sc: NAIF spacecraft identification code.
    :type sc: int
    :param clkstr: Character representation of a spacecraft clock.
    :type clkstr: str
    :return: Number of ticks represented by the clock string.
    :rtype: float
    """
    sc = ctypes.c_int(sc)
    clkstr = stypes.stringToCharP(clkstr)
    ticks = ctypes.c_double()
    libspice.sctiks_c(sc, clkstr, ctypes.byref(ticks))
    return ticks.value


@spiceErrorCheck
def sdiff(a, b):
    """
    Take the symmetric difference of two sets of any data type to form a
    third set.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sdiff_c.html

    :param a: First input set.
    :type a: spiceypy.utils.support_types.SpiceCell
    :param b: Second input set.
    :type b: spiceypy.utils.support_types.SpiceCell
    :return: Symmetric difference of a and b.
    :rtype: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(a, stypes.SpiceCell)
    assert isinstance(b, stypes.SpiceCell)
    assert a.dtype == b.dtype
    assert a.dtype == 0 or a.dtype == 1 or a.dtype == 2
    if a.dtype is 0:
        c = stypes.SPICECHAR_CELL(a.size, a.length)
    elif a.dtype is 1:
        c = stypes.SPICEDOUBLE_CELL(a.size)
    elif a.dtype is 2:
        c = stypes.SPICEINT_CELL(a.size)
    else:
        raise NotImplementedError
    libspice.sdiff_c(ctypes.byref(a), ctypes.byref(b), ctypes.byref(c))
    return c


@spiceErrorCheck
def set_c(a, op, b):
    """
    Given a relational operator, compare two sets of any data type.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/set_c.html

    :param a: First set.
    :type a: spiceypy.utils.support_types.SpiceCell
    :param op: Comparison operator.
    :type op: str
    :param b: Second set.
    :type b: spiceypy.utils.support_types.SpiceCell
    :return: The function returns the result of the comparison.
    :rtype: bool
    """
    assert isinstance(a, stypes.SpiceCell)
    assert isinstance(b, stypes.SpiceCell)
    assert a.dtype == b.dtype
    assert isinstance(op, str)
    op = stypes.stringToCharP(op)
    return libspice.set_c(ctypes.byref(a), op, ctypes.byref(b))


@spiceErrorCheck
def setmsg(message):
    """
    Set the value of the current long error message.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/setmsg_c.html

    :param message: A long error message.
    :type message: str
    """
    message = stypes.stringToCharP(message)
    libspice.setmsg_c(message)


@spiceErrorCheck
def shellc(ndim, lenvals, array):
    # This works! looks like this is a mutable 2d char array
    """
    Sort an array of character strings according to the ASCII
    collating sequence using the Shell Sort algorithm.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/shellc_c.html

    :param ndim: Dimension of the array.
    :type ndim: int
    :param lenvals: String length.
    :type lenvals: int
    :param array: The array to be sorted.
    :type array: list of str.
    :return: The sorted array.
    :rtype: list of str.
    """
    array = stypes.listToCharArray(array, xLen=lenvals, yLen=ndim)
    ndim = ctypes.c_int(ndim)
    lenvals = ctypes.c_int(lenvals)
    libspice.shellc_c(ndim, lenvals, ctypes.byref(array))
    return stypes.vectorToList(array)


@spiceErrorCheck
def shelld(ndim, array):
    # Works!, use this as example for "I/O" parameters
    """
    Sort a double precision array using the Shell Sort algorithm.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/shelld_c.html

    :param ndim: Dimension of the array.
    :type ndim: int
    :param array: The array to be sorted.
    :type array: Array of floats
    :return: The sorted array.
    :rtype: Array of floats
    """
    array = stypes.toDoubleVector(array)
    ndim = ctypes.c_int(ndim)
    libspice.shelld_c(ndim, ctypes.cast(array, ctypes.POINTER(ctypes.c_double)))
    return stypes.vectorToList(array)


@spiceErrorCheck
def shelli(ndim, array):
    # Works!, use this as example for "I/O" parameters
    """
    Sort an integer array using the Shell Sort algorithm.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/shelli_c.html

    :param ndim: Dimension of the array.
    :type ndim: int
    :param array: The array to be sorted.
    :type array: Array of ints
    :return: The sorted array.
    :rtype: Array of ints
    """
    array = stypes.toIntVector(array)
    ndim = ctypes.c_int(ndim)
    libspice.shelli_c(ndim, ctypes.cast(array, ctypes.POINTER(ctypes.c_int)))
    return stypes.vectorToList(array)


def sigerr(message):
    """
    Inform the CSPICE error processing mechanism that an error has
    occurred, and specify the type of error.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sigerr_c.html

    :param message: A short error message.
    :type message: str
    """
    message = stypes.stringToCharP(message)
    libspice.sigerr_c(message)


@spiceErrorCheck
@spiceFoundExceptionThrower
def sincpt(method, target, et, fixref, abcorr, obsrvr, dref, dvec):
    """
    Given an observer and a direction vector defining a ray, compute
    the surface intercept of the ray on a target body at a specified
    epoch, optionally corrected for light time and stellar
    aberration.

    This routine supersedes :func:`srfxpt`.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sincpt_c.html

    :param method: Computation method.
    :type method: str
    :param target: Name of target body.
    :type target: str
    :param et: Epoch in ephemeris seconds past J2000 TDB.
    :type et: float
    :param fixref: Body-fixed, body-centered target body frame.
    :type fixref: str
    :param abcorr: Aberration correction.
    :type abcorr: str
    :param obsrvr: Name of observing body.
    :type obsrvr: str
    :param dref: Reference frame of ray's direction vector.
    :type dref: str
    :param dvec: Ray's direction vector.
    :type dvec: 3-Element Array of floats
    :return:
            Surface intercept point on the target body,
            Intercept epoch,
            Vector from observer to intercept point.
    :rtype: tuple
    """
    method = stypes.stringToCharP(method)
    target = stypes.stringToCharP(target)
    et = ctypes.c_double(et)
    fixref = stypes.stringToCharP(fixref)
    abcorr = stypes.stringToCharP(abcorr)
    obsrvr = stypes.stringToCharP(obsrvr)
    dref = stypes.stringToCharP(dref)
    dvec = stypes.toDoubleVector(dvec)
    spoint = stypes.emptyDoubleVector(3)
    trgepc = ctypes.c_double(0)
    srfvec = stypes.emptyDoubleVector(3)
    found = ctypes.c_bool(0)
    libspice.sincpt_c(method, target, et, fixref, abcorr, obsrvr, dref, dvec,
                      spoint, ctypes.byref(trgepc), srfvec, ctypes.byref(found))
    return stypes.vectorToList(spoint), trgepc.value, stypes.vectorToList(
            srfvec), found.value


@spiceErrorCheck
def size(cell):
    """
    Return the size (maximum cardinality) of a SPICE cell of any
    data type.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/size_c.html

    :param cell: Input cell.
    :type cell: spiceypy.utils.support_types.SpiceCell
    :return: The size of the input cell.
    :rtype: int
    """
    assert isinstance(cell, stypes.SpiceCell)
    return libspice.size_c(ctypes.byref(cell))


@spiceErrorCheck
def spd():
    """
    Return the number of seconds in a day.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spd_c.html

    :return: The number of seconds in a day.
    :rtype: float
    """
    return libspice.spd_c()


@spiceErrorCheck
def sphcyl(radius, colat, slon):
    """
    This routine converts from spherical coordinates to cylindrical
    coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sphcyl_c.html

    :param radius: Distance of point from origin.
    :type radius: float
    :param colat: Polar angle (co-latitude in radians) of point.
    :type colat: float
    :param slon: Azimuthal angle (longitude) of point (radians).
    :type slon: float
    :return:
            Distance of point from z axis,
            angle (radians) of point from XZ plane,
            Height of point above XY plane.
    :rtype: tuple
    """
    radius = ctypes.c_double(radius)
    colat = ctypes.c_double(colat)
    slon = ctypes.c_double(slon)
    r = ctypes.c_double()
    lon = ctypes.c_double()
    z = ctypes.c_double()
    libspice.sphcyl_c(radius, colat, slon, ctypes.byref(r), ctypes.byref(lon),
                      ctypes.byref(z))
    return r.value, lon.value, z.value


@spiceErrorCheck
def sphlat(r, colat, lons):
    """
    Convert from spherical coordinates to latitudinal coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sphlat_c.html

    :param r: Distance of the point from the origin.
    :type r: float
    :param colat: Angle of the point from positive z axis (radians).
    :type colat: float
    :param lons: Angle of the point from the XZ plane (radians).
    :type lons: float
    :return:
            Distance of a point from the origin,
            Angle of the point from the XZ plane in radians,
            Angle of the point from the XY plane in radians.
    :rtype: tuple
    """
    r = ctypes.c_double(r)
    colat = ctypes.c_double(colat)
    lons = ctypes.c_double(lons)
    radius = ctypes.c_double()
    lon = ctypes.c_double()
    lat = ctypes.c_double()
    libspice.sphcyl_c(r, colat, lons, ctypes.byref(radius), ctypes.byref(lon),
                      ctypes.byref(lat))
    return radius.value, lon.value, lat.value


@spiceErrorCheck
def sphrec(r, colat, lon):
    """
    Convert from spherical coordinates to rectangular coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sphrec_c.html

    :param r: Distance of a point from the origin.
    :type r: float
    :param colat: Angle of the point from the positive Z-axis.
    :type colat: float
    :param lon: Angle of the point from the XZ plane in radians.
    :type lon: float
    :return: Rectangular coordinates of the point.
    :rtype: 3-Element Array of floats
    """
    r = ctypes.c_double(r)
    colat = ctypes.c_double(colat)
    lon = ctypes.c_double(lon)
    rectan = stypes.emptyDoubleVector(3)
    libspice.sphrec_c(r, colat, lon, rectan)
    return stypes.vectorToList(rectan)


@spiceErrorCheck
def spkacs(targ, et, ref, abcorr, obs):
    """
    Return the state (position and velocity) of a target body
    relative to an observer, optionally corrected for light time
    and stellar aberration, expressed relative to an inertial
    reference frame.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkacs_c.html

    :param targ: Target body.
    :type targ: int
    :param et: Observer epoch.
    :type et: float
    :param ref: Inertial reference frame of output state.
    :type ref: str
    :param abcorr: Aberration correction flag.
    :type abcorr: str
    :param obs: Observer.
    :type obs: int
    :return:
            State of target,
            One way light time between observer and target,
            Derivative of light time with respect to time.
    :rtype: tuple
    """
    targ = ctypes.c_int(targ)
    et = ctypes.c_double(et)
    ref = stypes.stringToCharP(ref)
    abcorr = stypes.stringToCharP(abcorr)
    obs = ctypes.c_int(obs)
    starg = stypes.emptyDoubleVector(6)
    lt = ctypes.c_double()
    dlt = ctypes.c_double()
    libspice.spkacs_c(targ, et, ref, abcorr, obs, starg, ctypes.byref(lt),
                      ctypes.byref(dlt))
    return stypes.vectorToList(starg), lt.value, dlt.value


@spiceErrorCheck
def spkapo(targ, et, ref, sobs, abcorr):
    """
    Return the position of a target body relative to an observer,
    optionally corrected for light time and stellar aberration.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkapo_c.html

    :param targ: Target body.
    :type targ: int
    :param et: Observer epoch.
    :type et: float
    :param ref: Inertial reference frame of observer's state.
    :type ref: str
    :param sobs: State of observer wrt. solar system barycenter.
    :type sobs: 6-Element Array of floats
    :param abcorr: Aberration correction flag.
    :type abcorr: str
    :return:
            Position of target,
            One way light time between observer and target.
    :rtype: tuple
    """
    targ = ctypes.c_int(targ)
    et = ctypes.c_double(et)
    ref = stypes.stringToCharP(ref)
    abcorr = stypes.stringToCharP(abcorr)
    sobs = stypes.toDoubleVector(sobs)
    ptarg = stypes.emptyDoubleVector(3)
    lt = ctypes.c_double()
    libspice.spkapo_c(targ, et, ref, sobs, abcorr, ptarg, ctypes.byref(lt))
    return stypes.vectorToList(ptarg), lt.value


@spiceErrorCheck
def spkapp(targ, et, ref, sobs, abcorr):
    """
    Deprecated: This routine has been superseded by :func:`spkaps`. This
    routine is supported for purposes of backward compatibility only.

    Return the state (position and velocity) of a target body
    relative to an observer, optionally corrected for light time and
    stellar aberration.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkapp_c.html

    :param targ: Target body.
    :type targ: int
    :param et: Observer epoch.
    :type et: float
    :param ref: Inertial reference frame of observer's state.
    :type ref: str
    :param sobs: State of observer wrt. solar system barycenter.
    :type sobs: 6-Element Array of floats
    :param abcorr: Aberration correction flag.
    :type abcorr: str
    :return:
            State of target,
            One way light time between observer and target.
    :rtype: tuple
    """
    targ = ctypes.c_int(targ)
    et = ctypes.c_double(et)
    ref = stypes.stringToCharP(ref)
    abcorr = stypes.stringToCharP(abcorr)
    sobs = stypes.toDoubleVector(sobs)
    starg = stypes.emptyDoubleVector(6)
    lt = ctypes.c_double()
    libspice.spkapp_c(targ, et, ref, sobs, abcorr, starg, ctypes.byref(lt))
    return stypes.vectorToList(starg), lt.value


@spiceErrorCheck
def spkaps(targ, et, ref, abcorr, stobs, accobs):
    """
    Given the state and acceleration of an observer relative to the
    solar system barycenter, return the state (position and velocity)
    of a target body relative to the observer, optionally corrected
    for light time and stellar aberration. All input and output
    vectors are expressed relative to an inertial reference frame.

    This routine supersedes :func:`spkapp`.

    SPICE users normally should call the high-level API routines
    :func:`spkezr` or :func:`spkez` rather than this routine.
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkaps_c.html

    :param targ: Target body.
    :type targ: int
    :param et: Observer epoch.
    :type et: float
    :param ref: Inertial reference frame of output state.
    :type ref: str
    :param abcorr: Aberration correction flag.
    :type abcorr: str
    :param stobs: State of the observer relative to the SSB.
    :type stobs: 6-Element Array of floats
    :param accobs: Acceleration of the observer relative to the SSB.
    :type accobs: 6-Element Array of floats
    :return:
             State of target,
             One way light time between observer and target,
             Derivative of light time with respect to time.
    :rtype: tuple
    """
    targ = ctypes.c_int(targ)
    et = ctypes.c_double(et)
    ref = stypes.stringToCharP(ref)
    abcorr = stypes.stringToCharP(abcorr)
    stobs = stypes.toDoubleVector(stobs)
    accobs = stypes.toDoubleVector(accobs)
    starg = stypes.emptyDoubleVector(6)
    lt = ctypes.c_double()
    dlt = ctypes.c_double()
    libspice.spkaps_c(targ, et, ref, abcorr, stobs, accobs, starg,
                      ctypes.byref(lt), ctypes.byref(dlt))
    return stypes.vectorToList(starg), lt.value, dlt.value


@spiceErrorCheck
def spk14a(handle, ncsets, coeffs, epochs):
    """
    Add data to a type 14 SPK segment associated with handle. See
    also :func:`spk14b` and :func:`spk14e`.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spk14a_c.html

    :param handle: The handle of an SPK file open for writing.
    :type handle: int
    :param ncsets: The number of coefficient sets and epochs.
    :type ncsets: int
    :param coeffs: The collection of coefficient sets.
    :type coeffs: Array of floats
    :param epochs: The epochs associated with the coefficient sets.
    :type epochs: Array of floats
    """
    handle = ctypes.c_int(handle)
    ncsets = ctypes.c_int(ncsets)
    coeffs = stypes.toDoubleVector(coeffs)
    epochs = stypes.toDoubleVector(epochs)
    libspice.spk14a_c(handle, ncsets, coeffs, epochs)


@spiceErrorCheck
def spk14b(handle, segid, body, center, framename, first, last, chbdeg):
    """
    Begin a type 14 SPK segment in the SPK file associated with
    handle. See also :func:`spk14a` and :func:`spk14e`.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spk14b_c.html

    :param handle: The handle of an SPK file open for writing.
    :type handle: int
    :param segid: The string to use for segment identifier.
    :type segid: str
    :param body: The NAIF ID code for the body of the segment.
    :type body: int
    :param center: The center of motion for body.
    :type center: int
    :param framename: The reference frame for this segment.
    :type framename: str
    :param first: The first epoch for which the segment is valid.
    :type first: float
    :param last: The last epoch for which the segment is valid.
    :type last: float
    :param chbdeg: The degree of the Chebyshev Polynomial used.
    :type chbdeg: int
    """
    handle = ctypes.c_int(handle)
    segid = stypes.stringToCharP(segid)
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    framename = stypes.stringToCharP(framename)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    chbdeg = ctypes.c_int(chbdeg)
    libspice.spk14b_c(handle, segid, body, center, framename, first, last,
                      chbdeg)


@spiceErrorCheck
def spk14e(handle):
    """
    End the type 14 SPK segment currently being written to the SPK
    file associated with handle. See also :func:`spk14a` and :func:`spk14b`.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spk14e_c.html

    :param handle: The handle of an SPK file open for writing.
    :type handle: int
    """
    handle = ctypes.c_int(handle)
    libspice.spk14e_c(handle)


@spiceErrorCheck
def spkcls(handle):
    """
    Close an open SPK file.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkcls_c.html

    :param handle: Handle of the SPK file to be closed.
    :type handle: int
    """
    handle = ctypes.c_int(handle)
    libspice.spkcls_c(handle)


@spiceErrorCheck
def spkcov(spk, idcode, cover):
    """
    Find the coverage window for a specified ephemeris object in a
    specified SPK file.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkcov_c.html

    :param spk: Name of SPK file.
    :type spk: str
    :param idcode: ID code of ephemeris object.
    :type idcode: int
    :param cover: Window giving coverage in "spk" for "idcode".
    :type cover: spiceypy.utils.support_types.SpiceCell
    """
    spk = stypes.stringToCharP(spk)
    idcode = ctypes.c_int(idcode)
    assert isinstance(cover, stypes.SpiceCell)
    assert cover.dtype == 1
    libspice.spkcov_c(spk, idcode, ctypes.byref(cover))


@spiceErrorCheck
def spkcpo(target, et, outref, refloc, abcorr, obspos, obsctr, obsref):
    """
    Return the state of a specified target relative to an "observer,"
    where the observer has constant position in a specified reference
    frame. The observer's position is provided by the calling program
    rather than by loaded SPK files.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkcpo_c.html

    :param target: Name of target ephemeris object.
    :type target: str
    :param et: Observation epoch.
    :type et: float
    :param outref: Reference frame of output state.
    :type outref: str
    :param refloc: Output reference frame evaluation locus.
    :type refloc: str
    :param abcorr: Aberration correction.
    :type abcorr: str
    :param obspos: Observer position relative to center of motion.
    :type obspos: 3-Element Array of floats
    :param obsctr: Center of motion of observer.
    :type obsctr: str
    :param obsref: Frame of observer position.
    :type obsref: str
    :return:
            State of target with respect to observer,
            One way light time between target and observer.
    :rtype: tuple
    """
    target = stypes.stringToCharP(target)
    et = ctypes.c_double(et)
    outref = stypes.stringToCharP(outref)
    refloc = stypes.stringToCharP(refloc)
    abcorr = stypes.stringToCharP(abcorr)
    obspos = stypes.toDoubleVector(obspos)
    obsctr = stypes.stringToCharP(obsctr)
    obsref = stypes.stringToCharP(obsref)
    state = stypes.emptyDoubleVector(6)
    lt = ctypes.c_double()
    libspice.spkcpo_c(target, et, outref, refloc, abcorr, obspos, obsctr,
                      obsref, state, ctypes.byref(lt))
    return stypes.vectorToList(state), lt.value


@spiceErrorCheck
def spkcpt(trgpos, trgctr, trgref, et, outref, refloc, abcorr, obsrvr):
    """
    Return the state, relative to a specified observer, of a target
    having constant position in a specified reference frame. The
    target's position is provided by the calling program rather than by
    loaded SPK files.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkcpt_c.html

    :param trgpos: Target position relative to center of motion.
    :type trgpos: 3-Element Array of floats
    :param trgctr: Center of motion of target.
    :type trgctr: str
    :param trgref: Observation epoch.
    :type trgref: str
    :param et: Observation epoch.
    :type et: float
    :param outref: Reference frame of output state.
    :type outref: str
    :param refloc: Output reference frame evaluation locus.
    :type refloc: str
    :param abcorr: Aberration correction.
    :type abcorr: str
    :param obsrvr: Name of observing ephemeris object.
    :return:
            State of target with respect to observer,
            One way light time between target and observer.
    :rtype: tuple
    """
    trgpos = stypes.toDoubleVector(trgpos)
    trgctr = stypes.stringToCharP(trgctr)
    trgref = stypes.stringToCharP(trgref)
    et = ctypes.c_double(et)
    outref = stypes.stringToCharP(outref)
    refloc = stypes.stringToCharP(refloc)
    abcorr = stypes.stringToCharP(abcorr)
    obsrvr = stypes.stringToCharP(obsrvr)
    state = stypes.emptyDoubleVector(6)
    lt = ctypes.c_double()
    libspice.spkcpt_c(trgpos, trgctr, trgref, et, outref, refloc, abcorr,
                      obsrvr, state, ctypes.byref(lt))
    return stypes.vectorToList(state), lt.value


@spiceErrorCheck
def spkcvo(target, et, outref, refloc, abcorr, obssta, obsepc, obsctr, obsref):
    """
    Return the state of a specified target relative to an "observer,"
    where the observer has constant velocity in a specified reference
    frame.  The observer's state is provided by the calling program
    rather than by loaded SPK files.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkcvo_c.html

    :param target: Name of target ephemeris object.
    :type target: str
    :param et: Observation epoch.
    :type et: float
    :param outref: Reference frame of output state.
    :type outref: str
    :param refloc: Output reference frame evaluation locus.
    :type refloc: str
    :param abcorr: Aberration correction.
    :type abcorr: str
    :param obssta: Observer state relative to center of motion.
    :type obssta: 6-Element Array of floats
    :param obsepc: Epoch of observer state.
    :type obsepc: float
    :param obsctr: Center of motion of observer.
    :type obsctr: str
    :param obsref: Frame of observer state.
    :type obsref: str
    :return:
            State of target with respect to observer,
            One way light time between target and observer.
    :rtype: tuple
    """
    target = stypes.stringToCharP(target)
    et = ctypes.c_double(et)
    outref = stypes.stringToCharP(outref)
    refloc = stypes.stringToCharP(refloc)
    abcorr = stypes.stringToCharP(abcorr)
    obssta = stypes.toDoubleVector(obssta)
    obsepc = ctypes.c_double(obsepc)
    obsctr = stypes.stringToCharP(obsctr)
    obsref = stypes.stringToCharP(obsref)
    state = stypes.emptyDoubleVector(6)
    lt = ctypes.c_double()
    libspice.spkcvo_c(target, et, outref, refloc, abcorr, obssta, obsepc,
                      obsctr, obsref, state, ctypes.byref(lt))
    return stypes.vectorToList(state), lt.value


@spiceErrorCheck
def spkcvt(trgsta, trgepc, trgctr, trgref, et, outref, refloc, abcorr, obsrvr):
    """
    Return the state, relative to a specified observer, of a target
    having constant velocity in a specified reference frame. The
    target's state is provided by the calling program rather than by
    loaded SPK files.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkcvt_c.html

    :param trgsta: Target state relative to center of motion.
    :type trgsta: 6-Element Array of floats
    :param trgepc: Epoch of target state.
    :type trgepc: float
    :param trgctr: Center of motion of target.
    :type trgctr: str
    :param trgref: Frame of target state.
    :type trgref: str
    :param et: Observation epoch.
    :type et: float
    :param outref: Reference frame of output state.
    :type outref: str
    :param refloc: Output reference frame evaluation locus.
    :type refloc: str
    :param abcorr: Aberration correction.
    :type abcorr: str
    :param obsrvr: Name of observing ephemeris object.
    :type obsrvr: str
    :return:
            State of target with respect to observer,
            One way light time between target and observer.
    :rtype: tuple
    """
    trgpos = stypes.toDoubleVector(trgsta)
    trgepc = ctypes.c_double(trgepc)
    trgctr = stypes.stringToCharP(trgctr)
    trgref = stypes.stringToCharP(trgref)
    et = ctypes.c_double(et)
    outref = stypes.stringToCharP(outref)
    refloc = stypes.stringToCharP(refloc)
    abcorr = stypes.stringToCharP(abcorr)
    obsrvr = stypes.stringToCharP(obsrvr)
    state = stypes.emptyDoubleVector(6)
    lt = ctypes.c_double()
    libspice.spkcvt_c(trgpos, trgepc, trgctr, trgref, et, outref, refloc,
                      abcorr, obsrvr, state, ctypes.byref(lt))
    return stypes.vectorToList(state), lt.value


@spiceErrorCheck
def spkez(targ, et, ref, abcorr, obs):
    """
    Return the state (position and velocity) of a target body
    relative to an observing body, optionally corrected for light
    time (planetary aberration) and stellar aberration.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkez_c.html

    :param targ: Target body.
    :type targ: int
    :param et: Observer epoch.
    :type et: float
    :param ref: Reference frame of output state vector.
    :type ref: str
    :param abcorr: Aberration correction flag.
    :type abcorr: str
    :param obs: Observing body.
    :type obs: int
    :return:
            State of target,
            One way light time between observer and target.
    :rtype: tuple
    """
    targ = ctypes.c_int(targ)
    et = ctypes.c_double(et)
    ref = stypes.stringToCharP(ref)
    abcorr = stypes.stringToCharP(abcorr)
    obs = ctypes.c_int(obs)
    starg = stypes.emptyDoubleVector(6)
    lt = ctypes.c_double()
    libspice.spkez_c(targ, et, ref, abcorr, obs, starg, ctypes.byref(lt))
    return stypes.vectorToList(starg), lt.value


@spiceErrorCheck
def spkezp(targ, et, ref, abcorr, obs):
    """
    Return the position of a target body relative to an observing
    body, optionally corrected for light time (planetary aberration)
    and stellar aberration.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkezp_c.html

    :param targ: Target body NAIF ID code.
    :type targ: int
    :param et: Observer epoch.
    :type et: float
    :param ref: Reference frame of output position vector.
    :type ref: str
    :param abcorr: Aberration correction flag.
    :type abcorr: str
    :param obs: Observing body NAIF ID code.
    :type obs: int
    :return:
            Position of target,
            One way light time between observer and target.
    :rtype: tuple
    """
    targ = ctypes.c_int(targ)
    et = ctypes.c_double(et)
    ref = stypes.stringToCharP(ref)
    abcorr = stypes.stringToCharP(abcorr)
    obs = ctypes.c_int(obs)
    ptarg = stypes.emptyDoubleVector(3)
    lt = ctypes.c_double()
    libspice.spkezp_c(targ, et, ref, abcorr, obs, ptarg, ctypes.byref(lt))
    return stypes.vectorToList(ptarg), lt.value


@spiceErrorCheck
def spkezr(targ, et, ref, abcorr, obs):
    """
    Return the state (position and velocity) of a target body
    relative to an observing body, optionally corrected for light
    time (planetary aberration) and stellar aberration.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkezr_c.html

    :param targ: Target body name.
    :type targ: str
    :param et: Observer epoch.
    :type et: float
    :param ref: Reference frame of output state vector.
    :type ref: str
    :param abcorr: Aberration correction flag.
    :type abcorr: str
    :param obs: Observing body name.
    :type obs: str
    :return:
            State of target,
            One way light time between observer and target.
    :rtype: tuple
    """
    targ = stypes.stringToCharP(targ)
    et = ctypes.c_double(et)
    ref = stypes.stringToCharP(ref)
    abcorr = stypes.stringToCharP(abcorr)
    obs = stypes.stringToCharP(obs)
    starg = stypes.emptyDoubleVector(6)
    lt = ctypes.c_double()
    libspice.spkezr_c(targ, et, ref, abcorr, obs, starg, ctypes.byref(lt))
    return stypes.vectorToList(starg), lt.value


@spiceErrorCheck
def spkgeo(targ, et, ref, obs):
    """
    Compute the geometric state (position and velocity) of a target
    body relative to an observing body.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkgeo_c.html

    :param targ: Target body.
    :type targ: int
    :param et: Target epoch.
    :type et: float
    :param ref: Target reference frame.
    :type ref: str
    :param obs: Observing body.
    :type obs: int
    :return: State of target, Light time.
    :rtype: tuple
    """
    targ = ctypes.c_int(targ)
    et = ctypes.c_double(et)
    ref = stypes.stringToCharP(ref)
    obs = ctypes.c_int(obs)
    state = stypes.emptyDoubleVector(6)
    lt = ctypes.c_double()
    libspice.spkgeo_c(targ, et, ref, obs, state, ctypes.byref(lt))
    return stypes.vectorToList(state), lt.value


@spiceErrorCheck
def spkgps(targ, et, ref, obs):
    """
    Compute the geometric position of a target body relative to an
    observing body.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkgps_c.html

    :param targ: Target body.
    :type targ: int
    :param et: Target epoch.
    :type et: float
    :param ref: Target reference frame.
    :type ref: str
    :param obs: Observing body.
    :type obs: int
    :return: Position of target, Light time.
    :rtype: tuple
    """
    targ = ctypes.c_int(targ)
    et = ctypes.c_double(et)
    ref = stypes.stringToCharP(ref)
    obs = ctypes.c_int(obs)
    position = stypes.emptyDoubleVector(3)
    lt = ctypes.c_double()
    libspice.spkgps_c(targ, et, ref, obs, position, ctypes.byref(lt))
    return stypes.vectorToList(position), lt.value


@spiceErrorCheck
def spklef(filename):
    """
    Load an ephemeris file for use by the readers.  Return that file's
    handle, to be used by other SPK routines to refer to the file.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spklef_c.html

    :param filename: Name of the file to be loaded.
    :type filename: str
    :return: Loaded file's handle.
    :rtype: int
    """
    filename = stypes.stringToCharP(filename)
    handle = ctypes.c_int()
    libspice.spklef_c(filename, ctypes.byref(handle))
    return handle.value


@spiceErrorCheck
def spkltc(targ, et, ref, abcorr, stobs):
    """
    Return the state (position and velocity) of a target body
    relative to an observer, optionally corrected for light time,
    expressed relative to an inertial reference frame.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkltc_c.html

    :param targ: Target body.
    :type targ: int
    :param et: Observer epoch.
    :type et: float
    :param ref: Inertial reference frame of output state.
    :type ref: str
    :param abcorr: Aberration correction flag.
    :type abcorr: str
    :param stobs: State of the observer relative to the SSB.
    :type stobs: 6-Element Array of floats
    :return:
            One way light time between observer and target,
            Derivative of light time with respect to time
    :rtype: tuple
    """
    assert len(stobs) == 6
    targ = stypes.c_int(targ)
    et = ctypes.c_double(et)
    ref = stypes.stringToCharP(ref)
    abcorr = stypes.stringToCharP(abcorr)
    stobs = stypes.toDoubleVector(stobs)
    starg = stypes.emptyDoubleVector(6)
    lt = ctypes.c_double()
    dlt = ctypes.c_double()
    libspice.spkltc_c(targ, et, ref, abcorr, stobs, starg, ctypes.byref(lt),
                      ctypes.byref(dlt))
    return stypes.vectorToList(starg), lt.value, dlt.value


@spiceErrorCheck
def spkobj(spk, outCell=None):
    """
    Find the set of ID codes of all objects in a specified SPK file.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkobj_c.html

    :param spk: Name of SPK file.
    :type spk: str
    :param outCell: Optional Spice Int Cell.
    :type outCell: spiceypy.utils.support_types.SpiceCell
    """
    spk = stypes.stringToCharP(spk)
    if not outCell:
        outCell = stypes.SPICEINT_CELL(1000)
    assert isinstance(outCell, stypes.SpiceCell)
    assert outCell.dtype == 2
    libspice.spkobj_c(spk, ctypes.byref(outCell))
    return outCell


@spiceErrorCheck
def spkopa(filename):
    # Todo: test spkopa
    """
    Open an existing SPK file for subsequent write.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkopa_c.html

    :param filename: The name of an existing SPK file.
    :type filename: str
    :return: A handle attached to the SPK file opened to append.
    :rtype: int
    """
    filename = stypes.stringToCharP(filename)
    handle = ctypes.c_int()
    libspice.spkopa_c(filename, ctypes.byref(handle))
    return handle.value


@spiceErrorCheck
def spkopn(filename, ifname, ncomch):
    """
    Create a new SPK file, returning the handle of the opened file.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkopn_c.html

    :param filename: The name of the new SPK file to be created.
    :type filename: str
    :param ifname: The internal filename for the SPK file.
    :type ifname: str
    :param ncomch: The number of characters to reserve for comments.
    :type ncomch: int
    :return: The handle of the opened SPK file.
    :rtype: int
    """
    filename = stypes.stringToCharP(filename)
    ifname = stypes.stringToCharP(ifname)
    ncomch = ctypes.c_int(ncomch)
    handle = ctypes.c_int()
    libspice.spkopn_c(filename, ifname, ncomch, ctypes.byref(handle))
    return handle.value


@spiceErrorCheck
def spkpds(body, center, framestr, typenum, first, last):
    # Todo: test spkpds
    """
    Perform routine error checks and if all check pass, pack the
    descriptor for an SPK segment

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkpds_c.html

    :param body: The NAIF ID code for the body of the segment.
    :type body: int
    :param center: The center of motion for body.
    :type center: int
    :param framestr: The frame for this segment.
    :type framestr: str
    :param typenum: The type of SPK segment to create.
    :type typenum: int
    :param first: The first epoch for which the segment is valid.
    :type first: float
    :param last: The last  epoch for which the segment is valid.
    :type last: float
    :return: An SPK segment descriptor.
    :rtype: 5-Element Array of floats
    """
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    framestr = stypes.stringToCharP(framestr)
    typenum = ctypes.c_int(typenum)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    descr = stypes.emptyDoubleVector(5)
    libspice.spkpds_c(body, center, framestr, typenum, first, last, descr)
    return stypes.vectorToList(descr)


@spiceErrorCheck
def spkpos(targ, et, ref, abcorr, obs):
    """
    Return the position of a target body relative to an observing
    body, optionally corrected for light time (planetary aberration)
    and stellar aberration.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkpos_c.html

    :param targ: Target body name.
    :type targ: str
    :param et: Observer epoch.
    :type et: float or List of Floats
    :param ref: Reference frame of output position vector.
    :type ref: str
    :param abcorr: Aberration correction flag.
    :type abcorr: str
    :param obs: Observing body name.
    :type obs: str
    :return:
            Position of target,
            One way light time between observer and target.
    :rtype: tuple
    """
    if hasattr(et, "__iter__"):
        vlen = len(et)
        positions = numpy.zeros((vlen, 3), dtype=numpy.float)
        times = numpy.zeros(vlen, dtype=numpy.float)
        for (index, time) in enumerate(et):
            positions[index], times[index] = spkpos(targ, time, ref, abcorr,
                                                    obs)
        return positions, times
    targ = stypes.stringToCharP(targ)
    ref = stypes.stringToCharP(ref)
    abcorr = stypes.stringToCharP(abcorr)
    obs = stypes.stringToCharP(obs)
    ptarg = stypes.emptyDoubleVector(3)
    lt = ctypes.c_double()
    libspice.spkpos_c(targ, et, ref, abcorr, obs, ptarg, ctypes.byref(lt))
    return stypes.vectorToList(ptarg), lt.value


@spiceErrorCheck
def spkpvn(handle, descr, et):
    """
    For a specified SPK segment and time, return the state (position and
    velocity) of the segment's target body relative to its center of
    motion.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkpvn_c.html

    :param handle: File handle.
    :type handle: int
    :param descr: Segment descriptor.
    :type descr: 5-Element Array of floats
    :param et: Evaluation epoch.
    :type et: float
    :return:
            Segment reference frame ID code,
            Output state vector,
            Center of state.
    :rtype: tuple
    """
    handle = ctypes.c_int(handle)
    descr = stypes.toDoubleVector(descr)
    et = ctypes.c_double(et)
    ref = ctypes.c_int()
    state = stypes.emptyDoubleVector(6)
    center = ctypes.c_int()
    libspice.spkpvn_c(handle, descr, et, ctypes.byref(ref), state,
                      ctypes.byref(center))
    return ref.value, stypes.vectorToList(state), center.value


@spiceErrorCheck
@spiceFoundExceptionThrower
def spksfs(body, et, idlen):
    # spksfs has a Parameter SIDLEN,
    # sounds like an optional but is that possible?
    """
    Search through loaded SPK files to find the highest-priority segment
    applicable to the body and time specified.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spksfs_c.html

    :param body: Body ID.
    :type body: int
    :param et: Ephemeris time.
    :type et: float
    :param idlen: Length of output segment ID string.
    :type idlen: int
    :return:
            Handle of file containing the applicable segment,
            Descriptor of the applicable segment,
            Identifier of the applicable segment.
    :rtype: tuple
    """
    body = ctypes.c_int(body)
    et = ctypes.c_double(et)
    idlen = ctypes.c_int(idlen)
    handle = ctypes.c_int()
    descr = stypes.emptyDoubleVector(5)
    identstring = stypes.stringToCharP(idlen)
    found = ctypes.c_bool()
    libspice.spksfs_c(body, et, idlen, ctypes.byref(handle), descr, identstring,
                      ctypes.byref(found))
    return handle.value, stypes.vectorToList(descr), \
           stypes.toPythonString(identstring), found.value


@spiceErrorCheck
def spkssb(targ, et, ref):
    # Todo: test spkssb
    """
    Return the state (position and velocity) of a target body
    relative to the solar system barycenter.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkssb_c.html

    :param targ: Target body.
    :type targ: int
    :param et: Target epoch.
    :type et: float
    :param ref: Target reference frame.
    :type ref: str
    :return: State of target.
    :rtype: 6-Element Array of floats
    """
    targ = ctypes.c_int(targ)
    et = ctypes.c_double(et)
    ref = stypes.stringToCharP(ref)
    starg = stypes.emptyDoubleVector(6)
    libspice.spkssb_c(targ, et, ref, starg)
    return stypes.vectorToList(starg)


@spiceErrorCheck
def spksub(handle, descr, identin, begin, end, newh):
    # Todo: test spksub
    """
    Extract a subset of the data in an SPK segment into a
    separate segment.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spksub_c.html

    :param handle: Handle of source segment.
    :type handle: int
    :param descr: Descriptor of source segment.
    :type descr: 5-Element Array of floats
    :param identin: Indentifier of source segment.
    :type identin: str
    :param begin: Beginning (initial epoch) of subset.
    :type begin: int
    :param end: End (fincal epoch) of subset.
    :type end: int
    :param newh: Handle of new segment.
    :type newh: int
    """
    assert len(descr) is 5
    handle = ctypes.c_int(handle)
    descr = stypes.toDoubleVector(descr)
    identin = stypes.stringToCharP(identin)
    begin = ctypes.c_double(begin)
    end = ctypes.c_double(end)
    newh = ctypes.c_int(newh)
    libspice.spksub_c(handle, descr, identin, begin, end, newh)


@spiceErrorCheck
def spkuds(descr):
    # Todo: test spkuds
    """
    Unpack the contents of an SPK segment descriptor.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkuds_c.html

    :param descr: An SPK segment descriptor.
    :type descr: 5-Element Array of floats
    :return:
            The NAIF ID code for the body of the segment,
            The center of motion for body,
            The ID code for the frame of this segment,
            The type of SPK segment,
            The first epoch for which the segment is valid,
            The last  epoch for which the segment is valid,
            Beginning DAF address of the segment,
            Ending DAF address of the segment.
    :rtype: tuple
    """
    assert len(descr) is 5
    descr = stypes.toDoubleVector(descr)
    body = ctypes.c_int()
    center = ctypes.c_int()
    framenum = ctypes.c_int()
    typenum = ctypes.c_int()
    first = ctypes.c_double()
    last = ctypes.c_double()
    begin = ctypes.c_int()
    end = ctypes.c_int()
    libspice.spkuds_c(descr, ctypes.byref(body), ctypes.byref(center),
                      ctypes.byref(framenum), ctypes.byref(typenum),
                      ctypes.byref(first), ctypes.byref(last),
                      ctypes.byref(begin), ctypes.byref(end))
    return body.value, center.value, framenum.value, typenum.value, \
           first.value, last.value, begin.value, end.value


@spiceErrorCheck
def spkuef(handle):
    # Todo: test spkuef
    """
    Unload an ephemeris file so that it will no longer be searched by
    the readers.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkuef_c.html

    :param handle: Handle of file to be unloaded
    :type handle: int
    """
    handle = ctypes.c_int(handle)
    libspice.spkuef_c(handle)


@spiceErrorCheck
def spkw02(handle, body, center, inframe, first, last, segid, intlen, n, polydg,
           cdata, btime):
    """
    Write a type 2 segment to an SPK file.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkw02_c.html

    :param handle: Handle of an SPK file open for writing.
    :type handle: int
    :param body: Body code for ephemeris object.
    :type body: int
    :param center: Body code for the center of motion of the body.
    :type center: int
    :param inframe: The reference frame of the states.
    :type inframe: str
    :param first: First valid time for which states can be computed.
    :type first: float
    :param last: Last valid time for which states can be computed.
    :type last: float
    :param segid: Segment identifier.
    :type segid: str
    :param intlen: Length of time covered by logical record.
    :type intlen: float
    :param n: Number of coefficient sets.
    :type n: int
    :param polydg: Chebyshev polynomial degree.
    :type polydg: int
    :param cdata: Array of Chebyshev coefficients.
    :type cdata: Array of floats
    :param btime: Begin time of first logical record.
    :type btime: float
    """
    handle = ctypes.c_int(handle)
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    inframe = stypes.stringToCharP(inframe)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    segid = stypes.stringToCharP(segid)
    intlen = ctypes.c_double(intlen)
    n = ctypes.c_int(n)
    polydg = ctypes.c_int(polydg)
    cdata = stypes.toDoubleVector(cdata)
    btime = ctypes.c_double(btime)
    libspice.spkw02_c(handle, body, center, inframe, first, last, segid, intlen,
                      n, polydg, cdata, btime)


@spiceErrorCheck
def spkw03(handle, body, center, inframe, first, last, segid, intlen, n, polydg,
           cdata, btime):
    """
    Write a type 3 segment to an SPK file.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkw03_c.html

    :param handle: Handle of SPK file open for writing.
    :type handle: int
    :param body: NAIF code for ephemeris object.
    :type body: int
    :param center: NAIF code for the center of motion of the body.
    :type center: int
    :param inframe: Reference frame name.
    :type inframe: str
    :param first: Start time of interval covered by segment.
    :type first: float
    :param last: End time of interval covered by segment.
    :type last: float
    :param segid: Segment identifier.
    :type segid: str
    :param intlen: Length of time covered by record.
    :type intlen: float
    :param n: Number of records in segment.
    :type n: int
    :param polydg: Chebyshev polynomial degree.
    :type polydg: int
    :param cdata: Array of Chebyshev coefficients.
    :type cdata: Array of floats
    :param btime: Begin time of first record.
    :type btime: float
    """
    handle = ctypes.c_int(handle)
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    inframe = stypes.stringToCharP(inframe)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    segid = stypes.stringToCharP(segid)
    intlen = ctypes.c_double(intlen)
    n = ctypes.c_int(n)
    polydg = ctypes.c_int(polydg)
    cdata = stypes.toDoubleVector(cdata)
    btime = ctypes.c_double(btime)
    libspice.spkw03_c(handle, body, center, inframe, first, last, segid, intlen,
                      n, polydg, cdata, btime)


@spiceErrorCheck
def spkw05(handle, body, center, inframe, first, last, segid, gm, n, states,
           epochs):
    # see libspice args for solution to array[][N] problem
    """
    Write an SPK segment of type 5 given a time-ordered set of
    discrete states and epochs, and the gravitational parameter
    of a central body.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkw05_c.html

    :param handle: Handle of an SPK file open for writing.
    :type handle: int
    :param body: Body code for ephemeris object.
    :type body: int
    :param center: Body code for the center of motion of the body.
    :type center: int
    :param inframe: The reference frame of the states.
    :type inframe: str
    :param first: First valid time for which states can be computed.
    :type first: float
    :param last: Last valid time for which states can be computed.
    :type last: float
    :param segid: Segment identifier.
    :type segid: str
    :param gm: Gravitational parameter of central body.
    :type gm: float
    :param n: Number of states and epochs.
    :type n: int
    :param states: States.
    :type states: Nx6-Element Array of floats
    :param epochs: Epochs.
    :type epochs: Array of floats
    """
    handle = ctypes.c_int(handle)
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    inframe = stypes.stringToCharP(inframe)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    segid = stypes.stringToCharP(segid)
    gm = ctypes.c_double(gm)
    n = ctypes.c_int(n)
    states = stypes.toDoubleMatrix(states)
    epochs = stypes.toDoubleVector(epochs)
    libspice.spkw05_c(handle, body, center, inframe, first, last, segid, gm, n,
                      states, epochs)


@spiceErrorCheck
def spkw08(handle, body, center, inframe, first, last, segid, degree, n, states,
           epoch1, step):
    # see libspice args for solution to array[][N] problem
    """
    Write a type 8 segment to an SPK file.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkw08_c.html

    :param handle: Handle of an SPK file open for writing.
    :type handle: int
    :param body: NAIF code for an ephemeris object.
    :type body: int
    :param center: NAIF code for center of motion of "body".
    :type center: int
    :param inframe: Reference frame name.
    :type inframe: str
    :param first: Start time of interval covered by segment.
    :type first: float
    :param last: End time of interval covered by segment.
    :type last: float
    :param segid: Segment identifier.
    :type segid: str
    :param degree: Degree of interpolating polynomials.
    :type degree: int
    :param n: Number of states.
    :type n: int
    :param states: Array of states.
    :type states: Nx6-Element Array of floats
    :param epoch1: Epoch of first state in states array.
    :type epoch1: float
    :param step: Time step separating epochs of states.
    :type step: float
    """
    handle = ctypes.c_int(handle)
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    inframe = stypes.stringToCharP(inframe)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    segid = stypes.stringToCharP(segid)
    degree = ctypes.c_int(degree)
    n = ctypes.c_int(n)
    states = stypes.toDoubleMatrix(states)  # X by 6 array
    epoch1 = ctypes.c_double(epoch1)
    step = ctypes.c_double(step)
    libspice.spkw08_c(handle, body, center, inframe, first, last, segid, degree,
                      n, states, epoch1, step)


@spiceErrorCheck
def spkw09(handle, body, center, inframe, first, last, segid, degree, n, states,
           epochs):
    """
    Write a type 9 segment to an SPK file.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkw09_c.html

    :param handle: Handle of an SPK file open for writing.
    :type handle: int
    :param body: NAIF code for an ephemeris object.
    :type body: int
    :param center: NAIF code for center of motion of "body".
    :type center: int
    :param inframe: Reference frame name.
    :type inframe: str
    :param first: Start time of interval covered by segment.
    :type first: float
    :param last: End time of interval covered by segment.
    :type last: float
    :param segid: Segment identifier.
    :type segid: str
    :param degree: Degree of interpolating polynomials.
    :type degree: int
    :param n: Number of states.
    :type n: int
    :param states: Array of states.
    :type states: Nx6-Element Array of floats
    :param epochs: Array of epochs corresponding to states.
    :type epochs: Array of floats
    """
    handle = ctypes.c_int(handle)
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    inframe = stypes.stringToCharP(inframe)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    segid = stypes.stringToCharP(segid)
    degree = ctypes.c_int(degree)
    n = ctypes.c_int(n)
    states = stypes.toDoubleMatrix(states)  # X by 6 array
    epochs = stypes.toDoubleVector(epochs)
    libspice.spkw09_c(handle, body, center, inframe, first, last, segid, degree,
                      n, states, epochs)


@spiceErrorCheck
def spkw10(handle, body, center, inframe, first, last, segid, consts, n, elems,
           epochs):
    """
    Write an SPK type 10 segment to the DAF open and attached to
    the input handle.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkw10_c.html

    :param handle: The handle of a DAF file open for writing.
    :type handle: int
    :param body: The NAIF ID code for the body of the segment.
    :type body: int
    :param center: The center of motion for body.
    :type center: int
    :param inframe: The reference frame for this segment.
    :type inframe: str
    :param first: The first epoch for which the segment is valid.
    :type first: float
    :param last: The last  epoch for which the segment is valid.
    :type last: float
    :param segid: The string to use for segment identifier.
    :type segid: str
    :param consts: The array of geophysical constants for the segment.
    :type consts: 8-Element Array of floats
    :param n: The number of element/epoch pairs to be stored.
    :type n: int
    :param elems: The collection of "two-line" element sets.
    :type elems: Array of floats
    :param epochs: The epochs associated with the element sets.
    :type epochs: Array of floats
    """
    handle = ctypes.c_int(handle)
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    inframe = stypes.stringToCharP(inframe)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    segid = stypes.stringToCharP(segid)
    consts = stypes.toDoubleVector(consts)
    n = ctypes.c_int(n)
    elems = stypes.toDoubleVector(elems)
    epochs = stypes.toDoubleVector(epochs)
    libspice.spkw10_c(handle, body, center, inframe, first, last, segid, consts,
                      n, elems, epochs)


@spiceErrorCheck
def spkw12(handle, body, center, inframe, first, last, segid, degree, n, states,
           epoch0, step):
    """
    Write a type 12 segment to an SPK file.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkw12_c.html

    :param handle: Handle of an SPK file open for writing.
    :type handle: int
    :param body: NAIF code for an ephemeris object.
    :type body: int
    :param center: NAIF code for center of motion of body.
    :type center: int
    :param inframe: Reference frame name.
    :type inframe: str
    :param first: Start time of interval covered by segment.
    :type first: float
    :param last: End time of interval covered by segment.
    :type last: float
    :param segid: Segment identifier.
    :type segid: str
    :param degree: Degree of interpolating polynomials.
    :type degree: int
    :param n: Number of states.
    :type n: int
    :param states: Array of states.
    :type states: Nx6-Element Array of floats
    :param epoch0: Epoch of first state in states array.
    :type epoch0: float
    :param step: Time step separating epochs of states.
    :type step: float
    """
    handle = ctypes.c_int(handle)
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    inframe = stypes.stringToCharP(inframe)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    segid = stypes.stringToCharP(segid)
    degree = ctypes.c_int(degree)
    n = ctypes.c_int(n)
    states = stypes.toDoubleMatrix(states)  # X by 6 array
    epoch0 = ctypes.c_double(epoch0)
    step = ctypes.c_double(step)
    libspice.spkw12_c(handle, body, center, inframe, first, last, segid, degree,
                      n, states, epoch0, step)


@spiceErrorCheck
def spkw13(handle, body, center, inframe, first, last, segid, degree, n, states,
           epochs):
    """
    Write a type 13 segment to an SPK file.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkw13_c.html

    :param handle: Handle of an SPK file open for writing.
    :type handle: int
    :param body: NAIF code for an ephemeris object.
    :type body: int
    :param center: NAIF code for center of motion of body.
    :type center: int
    :param inframe: Reference frame name.
    :type inframe: str
    :param first: Start time of interval covered by segment.
    :type first: float
    :param last: End time of interval covered by segment.
    :type last: float
    :param segid: Segment identifier.
    :type segid: str
    :param degree: Degree of interpolating polynomials.
    :type degree: int
    :param n: Number of states.
    :type n: int
    :param states: Array of states.
    :type states: Nx6-Element Array of floats
    :param epochs: Array of epochs corresponding to states.
    :type epochs: Array of floats
    """
    handle = ctypes.c_int(handle)
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    inframe = stypes.stringToCharP(inframe)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    segid = stypes.stringToCharP(segid)
    degree = ctypes.c_int(degree)
    n = ctypes.c_int(n)
    states = stypes.toDoubleMatrix(states)  # X by 6 array
    epochs = stypes.toDoubleVector(epochs)
    libspice.spkw13_c(handle, body, center, inframe, first, last, segid, degree,
                      n, states, epochs)


@spiceErrorCheck
def spkw15(handle, body, center, inframe, first, last, segid, epoch, tp, pa, p,
           ecc, j2flg, pv, gm, j2, radius):
    # Todo: test spkw15
    """
    Write an SPK segment of type 15 given a type 15 data record.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkw15_c.html

    :param handle: Handle of an SPK file open for writing.
    :type handle: int
    :param body: Body code for ephemeris object.
    :type body: int
    :param center: Body code for the center of motion of the body.
    :type center: int
    :param inframe: The reference frame of the states.
    :type inframe: str
    :param first: First valid time for which states can be computed.
    :type first: float
    :param last: Last valid time for which states can be computed.
    :type last: float
    :param segid: Segment identifier.
    :type segid: str
    :param epoch: Epoch of the periapse.
    :type epoch: float
    :param tp: Trajectory pole vector.
    :type tp: 3-Element Array of floats
    :param pa: Periapsis vector.
    :type pa: 3-Element Array of floats
    :param p: Semi-latus rectum.
    :type p: float
    :param ecc: Eccentricity.
    :type ecc: float
    :param j2flg: J2 processing flag.
    :type j2flg: float
    :param pv: Central body pole vector.
    :type pv: float
    :param gm: Central body GM.
    :type gm: float
    :param j2: Central body J2.
    :type j2: float
    :param radius: Equatorial radius of central body.
    :type radius: float
    """
    handle = ctypes.c_int(handle)
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    inframe = stypes.stringToCharP(inframe)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    segid = stypes.stringToCharP(segid)
    epoch = ctypes.c_double(epoch)
    tp = stypes.toDoubleVector(tp)
    pa = stypes.toDoubleVector(pa)
    p = ctypes.c_double(p)
    ecc = ctypes.c_double(ecc)
    j2flg = ctypes.c_double(j2flg)
    pv = ctypes.c_double(pv)
    gm = ctypes.c_double(gm)
    j2 = ctypes.c_double(j2)
    radius = ctypes.c_double(radius)
    libspice.spkw15_c(handle, body, center, inframe, first, last, segid, epoch,
                      tp, pa, p, ecc, j2flg, pv, gm, j2, radius)


@spiceErrorCheck
def spkw17(handle, body, center, inframe, first, last, segid, epoch, eqel,
           rapol, decpol):
    # Todo: test spkw17
    """
    Write an SPK segment of type 17 given a type 17 data record.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/spkw17_c.html

    :param handle: Handle of an SPK file open for writing.
    :type handle: int
    :param body: Body code for ephemeris object.
    :type body: int
    :param center: Body code for the center of motion of the body.
    :type center: int
    :param inframe: The reference frame of the states.
    :type inframe: str
    :param first: First valid time for which states can be computed.
    :type first: float
    :param last: Last valid time for which states can be computed.
    :type last: float
    :param segid: Segment identifier.
    :type segid: str
    :param epoch: Epoch of elements in seconds past J2000.
    :type epoch: float
    :param eqel: Array of equinoctial elements.
    :type eqel: 9-Element Array of floats
    :param rapol: Right Ascension of the pole of the reference plane.
    :type rapol: float
    :param decpol: Declination of the pole of the reference plane.
    :type decpol: float
    """
    handle = ctypes.c_int(handle)
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    inframe = stypes.stringToCharP(inframe)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    segid = stypes.stringToCharP(segid)
    epoch = ctypes.c_double(epoch)
    eqel = stypes.toDoubleVector(eqel)
    rapol = ctypes.c_double(rapol)
    decpol = ctypes.c_double(decpol)
    libspice.spkw17_c(handle, body, center, inframe, first, last, segid, epoch,
                      eqel, rapol, decpol)


# spkw18


# spkw20


@spiceErrorCheck
def srfrec(body, longitude, latitude):
    """
    Convert planetocentric latitude and longitude of a surface
    point on a specified body to rectangular coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfrec_c.html

    :param body: NAIF integer code of an extended body.
    :type body: int
    :param longitude: Longitude of point in radians.
    :type longitude: float
    :param latitude: Latitude of point in radians.
    :type latitude: float
    :return: Rectangular coordinates of the point.
    :rtype: 3-Element Array of floats
    """
    body = ctypes.c_int(body)
    longitude = ctypes.c_double(longitude)
    latitude = ctypes.c_double(latitude)
    rectan = stypes.emptyDoubleVector(3)
    libspice.srfrec_c(body, longitude, latitude, rectan)
    return stypes.vectorToList(rectan)


@spiceErrorCheck
@spiceFoundExceptionThrower
def srfxpt(method, target, et, abcorr, obsrvr, dref, dvec):
    """
    Deprecated: This routine has been superseded by the CSPICE
    routine :func:`sincpt`. This routine is supported for purposes of
    backward compatibility only.

    Given an observer and a direction vector defining a ray, compute the
    surface intercept point of the ray on a target body at a specified
    epoch, optionally corrected for light time and stellar aberration.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/srfxpt_c.html

    :param method: Computation method.
    :type method: str
    :param target: Name of target body.
    :type target: str
    :param et: Epoch in ephemeris seconds past J2000 TDB.
    :type et: float
    :param abcorr: Aberration correction.
    :type abcorr: str
    :param obsrvr: Name of observing body.
    :type obsrvr: str
    :param dref: Reference frame of input direction vector.
    :type dref: str
    :param dvec: Ray's direction vector.
    :type dvec: 3-Element Array of floats
    :return:
            Surface intercept point on the target body,
            Distance from the observer to the intercept point,
            Intercept epoch,
            Observer position relative to target center.
    :rtype: tuple
    """
    if hasattr(et, "__iter__"):
        return numpy.array(
                [srfxpt(method, target, t, abcorr, obsrvr, dref, dvec) for t in
                 et])
    method = stypes.stringToCharP(method)
    target = stypes.stringToCharP(target)
    et = ctypes.c_double(et)
    abcorr = stypes.stringToCharP(abcorr)
    obsrvr = stypes.stringToCharP(obsrvr)
    dref = stypes.stringToCharP(dref)
    dvec = stypes.toDoubleVector(dvec)
    spoint = stypes.emptyDoubleVector(3)
    trgepc = ctypes.c_double()
    dist = ctypes.c_double()
    obspos = stypes.emptyDoubleVector(3)
    found = ctypes.c_bool()
    libspice.srfxpt_c(method, target, et, abcorr, obsrvr, dref, dvec,
                      spoint, ctypes.byref(dist), ctypes.byref(trgepc), obspos,
                      ctypes.byref(found))
    return stypes.vectorToList(
            spoint), dist.value, trgepc.value, stypes.vectorToList(
            obspos), found.value


@spiceErrorCheck
def ssize(newsize, cell):
    """
    Set the size (maximum cardinality) of a CSPICE cell of any data type.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ssize_c.html

    :param newsize: Size (maximum cardinality) of the cell.
    :type newsize: int
    :param cell: The cell.
    :type cell: spiceypy.utils.support_types.SpiceCell
    :return: The updated cell.
    :rtype: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(cell, stypes.SpiceCell)
    newsize = ctypes.c_int(newsize)
    libspice.ssize_c(newsize, ctypes.byref(cell))
    return cell


@spiceErrorCheck
def stelab(pobj, vobs):
    """
    Correct the apparent position of an object for stellar
    aberration.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/stelab_c.html

    :param pobj: Position of an object with respect to the observer.
    :type pobj: 3-Element Array of floats
    :param vobs:
                Velocity of the observer with respect
                to the Solar System barycenter.
    :type vobs: 3-Element Array of floats
    :return:
            Apparent position of the object with respect to
            the observer, corrected for stellar aberration.
    :rtype: 3-Element Array of floats
    """
    pobj = stypes.toDoubleVector(pobj)
    vobs = stypes.toDoubleVector(vobs)
    appobj = stypes.emptyDoubleVector(3)
    libspice.stelab_c(pobj, vobs, appobj)
    return stypes.vectorToList(appobj)


@spiceErrorCheck
@spiceFoundExceptionThrower
def stpool(item, nth, contin, lenout=_default_len_out):
    """
    Retrieve the nth string from the kernel pool variable, where the
    string may be continued across several components of the kernel pool
    variable.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/stpool_c.html

    :param item: Name of the kernel pool variable.
    :type item: str
    :param nth: Index of the full string to retrieve.
    :type nth: int
    :param contin: Character sequence used to indicate continuation.
    :type contin: str
    :param lenout: Available space in output string.
    :type lenout: int
    :return:
            A full string concatenated across continuations,
            The number of characters in the full string value.
    :rtype: tuple
    """
    item = stypes.stringToCharP(item)
    contin = stypes.stringToCharP(contin)
    nth = ctypes.c_int(nth)
    strout = stypes.stringToCharP(lenout)
    lenout = ctypes.c_int(lenout)
    found = ctypes.c_bool()
    sizet = ctypes.c_int()
    libspice.stpool_c(item, nth, contin, lenout, strout, ctypes.byref(sizet),
                      ctypes.byref(found))
    return stypes.toPythonString(strout), sizet.value, found.value


@spiceErrorCheck
def str2et(time):
    """
    Convert a string representing an epoch to a double precision
    value representing the number of TDB seconds past the J2000
    epoch corresponding to the input epoch.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/str2et_c.html

    :param time: A string representing an epoch.
    :type time: str
    :return: The equivalent value in seconds past J2000, TDB.
    :rtype: float
    """
    if isinstance(time, list):
        return numpy.array([str2et(t) for t in time])
    time = stypes.stringToCharP(time)
    et = ctypes.c_double()
    libspice.str2et_c(time, ctypes.byref(et))
    return et.value


@spiceErrorCheck
def subpnt(method, target, et, fixref, abcorr, obsrvr):
    """
    Compute the rectangular coordinates of the sub-observer point on
    a target body at a specified epoch, optionally corrected for
    light time and stellar aberration.

    This routine supersedes :func:`subpt`.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/subpnt_c.html

    :param method: Computation method.
    :type method: str
    :param target: Name of target body.
    :type target: str
    :param et: Epoch in ephemeris seconds past J2000 TDB.
    :type et: float
    :param fixref: Body-fixed, body-centered target body frame.
    :type fixref: str
    :param abcorr: Aberration correction.
    :type abcorr: str
    :param obsrvr: Name of observing body.
    :type obsrvr: str
    :return:
            Sub-observer point on the target body,
            Sub-observer point epoch,
            Vector from observer to sub-observer point.
    :rtype: tuple
    """
    method = stypes.stringToCharP(method)
    target = stypes.stringToCharP(target)
    et = ctypes.c_double(et)
    fixref = stypes.stringToCharP(fixref)
    abcorr = stypes.stringToCharP(abcorr)
    obsrvr = stypes.stringToCharP(obsrvr)
    spoint = stypes.emptyDoubleVector(3)
    trgepc = ctypes.c_double(0)
    srfvec = stypes.emptyDoubleVector(3)
    libspice.subpnt_c(method, target, et, fixref, abcorr, obsrvr, spoint,
                      ctypes.byref(trgepc), srfvec)
    return stypes.vectorToList(spoint), trgepc.value, stypes.vectorToList(
            srfvec)


@spiceErrorCheck
def subpt(method, target, et, abcorr, obsrvr):
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

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/subpt_c.html

    :param method: Computation method.
    :type method: str
    :param target: Name of target body.
    :type target: str
    :param et: Epoch in ephemeris seconds past J2000 TDB.
    :type et: float or  Array of floats
    :param abcorr: Aberration correction.
    :type abcorr: str
    :param obsrvr: Name of observing body.
    :type obsrvr: str
    :return:
            Sub-observer point on the target body,
            Altitude of the observer above the target body.
    :rtype: tuple
    """
    if hasattr(et, "__iter__"):
        return numpy.array(
                [subpt(method, target, t, abcorr, obsrvr) for t in et])
    method = stypes.stringToCharP(method)
    target = stypes.stringToCharP(target)
    et = ctypes.c_double(et)
    abcorr = stypes.stringToCharP(abcorr)
    obsrvr = stypes.stringToCharP(obsrvr)
    spoint = stypes.emptyDoubleVector(3)
    alt = ctypes.c_double()
    libspice.subpt_c(method, target, et, abcorr, obsrvr, spoint,
                     ctypes.byref(alt))
    return stypes.vectorToList(spoint), alt.value


@spiceErrorCheck
def subslr(method, target, et, fixref, abcorr, obsrvr):
    """
    Compute the rectangular coordinates of the sub-solar point on
    a target body at a specified epoch, optionally corrected for
    light time and stellar aberration.

    This routine supersedes subsol_c.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/subslr_c.html

    :param method: Computation method.
    :type method: str
    :param target: Name of target body.
    :type target: str
    :param et: Epoch in ephemeris seconds past J2000 TDB.
    :type et: float
    :param fixref: Body-fixed, body-centered target body frame.
    :type fixref: str
    :param abcorr: Aberration correction.
    :type abcorr: str
    :param obsrvr: Name of observing body.
    :type obsrvr: str
    :return:
            Sub-solar point on the target body,
            Sub-solar point epoch,
            Vector from observer to sub-solar point.
    :rtype: tuple
    """
    method = stypes.stringToCharP(method)
    target = stypes.stringToCharP(target)
    et = ctypes.c_double(et)
    fixref = stypes.stringToCharP(fixref)
    abcorr = stypes.stringToCharP(abcorr)
    obsrvr = stypes.stringToCharP(obsrvr)
    spoint = stypes.emptyDoubleVector(3)
    trgepc = ctypes.c_double(0)
    srfvec = stypes.emptyDoubleVector(3)
    libspice.subslr_c(method, target, et, fixref, abcorr, obsrvr, spoint,
                      ctypes.byref(trgepc), srfvec)
    return stypes.vectorToList(spoint), trgepc.value, stypes.vectorToList(
            srfvec)


@spiceErrorCheck
def subsol(method, target, et, abcorr, obsrvr):
    """
    Deprecated: This routine has been superseded by the CSPICE
    routine :func:`subslr`. This routine is supported for purposes of
    backward compatibility only.

    Determine the coordinates of the sub-solar point on a target
    body as seen by a specified observer at a specified epoch,
    optionally corrected for planetary (light time) and stellar
    aberration.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/subsol_c.html

    :param method: Computation method.
    :type method: str
    :param target: Name of target body.
    :type target: str
    :param et: Epoch in ephemeris seconds past J2000 TDB.
    :type et: float
    :param abcorr: Aberration correction.
    :type abcorr: str
    :param obsrvr: Name of observing body.
    :type obsrvr: str
    :return: Sub-solar point on the target body.
    :rtype: 3-Element Array of floats
    """
    method = stypes.stringToCharP(method)
    target = stypes.stringToCharP(target)
    et = ctypes.c_double(et)
    abcorr = stypes.stringToCharP(abcorr)
    obsrvr = stypes.stringToCharP(obsrvr)
    spoint = stypes.emptyDoubleVector(3)
    libspice.subsol_c(method, target, et, abcorr, obsrvr, spoint)
    return stypes.vectorToList(spoint)


@spiceErrorCheck
def sumad(array):
    """
    Return the sum of the elements of a double precision array.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sumad_c.html

    :param array: Input Array.
    :type array: Array of floats
    :return: The sum of the array.
    :rtype: float
    """
    n = ctypes.c_int(len(array))
    array = stypes.toDoubleVector(array)
    return libspice.sumad_c(array, n)


@spiceErrorCheck
def sumai(array):
    """
    Return the sum of the elements of an integer array.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sumai_c.html

    :param array: Input Array.
    :type array: Array of ints
    :return: The sum of the array.
    :rtype: int
    """
    n = ctypes.c_int(len(array))
    array = stypes.toIntVector(array)
    return libspice.sumai_c(array, n)


@spiceErrorCheck
def surfnm(a, b, c, point):
    """
    This routine computes the outward-pointing, unit normal vector
    from a point on the surface of an ellipsoid.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/surfnm_c.html

    :param a: Length of the ellisoid semi-axis along the x-axis.
    :type a: float
    :param b: Length of the ellisoid semi-axis along the y-axis.
    :type b: float
    :param c: Length of the ellisoid semi-axis along the z-axis.
    :type c: float
    :param point: Body-fixed coordinates of a point on the ellipsoid'
    :type point: 3-Element Array of floats
    :return: Outward pointing unit normal to ellipsoid at point.
    :rtype: 3-Element Array of floats
    """
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    point = stypes.toDoubleVector(point)
    normal = stypes.emptyDoubleVector(3)
    libspice.surfnm_c(a, b, c, point, normal)
    return stypes.vectorToList(normal)


@spiceErrorCheck
@spiceFoundExceptionThrower
def surfpt(positn, u, a, b, c):
    """
    Determine the intersection of a line-of-sight vector with the
    surface of an ellipsoid.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/surfpt_c.html

    :param positn: Position of the observer in body-fixed frame.
    :type positn: 3-Element Array of floats
    :param u: Vector from the observer in some direction.
    :type u: 3-Element Array of floats
    :param a: Length of the ellisoid semi-axis along the x-axis.
    :type a: float
    :param b: Length of the ellisoid semi-axis along the y-axis.
    :type b: float
    :param c: Length of the ellisoid semi-axis along the z-axis.
    :type c: float
    :return: Point on the ellipsoid pointed to by u.
    :rtype: 3-Element Array of floats
    """
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    positn = stypes.toDoubleVector(positn)
    u = stypes.toDoubleVector(u)
    point = stypes.emptyDoubleVector(3)
    found = ctypes.c_bool()
    libspice.surfpt_c(positn, u, a, b, c, point, ctypes.byref(found))
    return stypes.vectorToList(point), found.value


@spiceErrorCheck
@spiceFoundExceptionThrower
def surfpv(stvrtx, stdir, a, b, c):
    """
    Find the state (position and velocity) of the surface intercept
    defined by a specified ray, ray velocity, and ellipsoid.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/surfpv_c.html

    :param stvrtx: State of ray's vertex.
    :type stvrtx: 6-Element Array of floats
    :param stdir: State of ray's direction vector.
    :type stdir: 6-Element Array of floats
    :param a: Length of the ellisoid semi-axis along the x-axis.
    :type a: float
    :param b: Length of the ellisoid semi-axis along the y-axis.
    :type b: float
    :param c: Length of the ellisoid semi-axis along the z-axis.
    :type c: float
    :return: State of surface intercept.
    :rtype: list
    """
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    stvrtx = stypes.toDoubleVector(stvrtx)
    stdir = stypes.toDoubleVector(stdir)
    stx = stypes.emptyDoubleVector(6)
    found = ctypes.c_bool()
    libspice.surfpv_c(stvrtx, stdir, a, b, c, stx, ctypes.byref(found))
    return stypes.vectorToList(stx), found.value


@spiceErrorCheck
def swpool(agent, nnames, lenvals, names):
    """
    Add a name to the list of agents to notify whenever a member of
    a list of kernel variables is updated.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/swpool_c.html

    :param agent: The name of an agent to be notified after updates.
    :type agent: str
    :param nnames: The number of variables to associate with agent.
    :type nnames: int
    :param lenvals: Length of strings in the names array.
    :type lenvals: int
    :param names: Variable names whose update causes the notice.
    :type names: list of strs.
    """
    agent = stypes.stringToCharP(agent)
    nnames = ctypes.c_int(nnames)
    lenvals = ctypes.c_int(lenvals)
    names = stypes.listToCharArray(names)
    libspice.swpool_c(agent, nnames, lenvals, names)


@spiceErrorCheck
def sxform(instring, tostring, et):
    """
    Return the state transformation matrix from one frame to
    another at a specified epoch.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/sxform_c.html


    :param instring: Name of the frame to transform from.
    :type instring: str
    :param tostring: Name of the frame to transform to.
    :type tostring: str
    :param et: Epoch of the state transformation matrix.
    :type et: float
    :return: A state transformation matrix.
    :rtype: 6x6-Element Array of floats
    """
    if hasattr(et, "__iter__"):
        return numpy.array([sxform(instring, tostring, t) for t in et])
    instring = stypes.stringToCharP(instring)
    tostring = stypes.stringToCharP(tostring)
    et = ctypes.c_double(et)
    xform = stypes.emptyDoubleMatrix(x=6, y=6)
    libspice.sxform_c(instring, tostring, et, xform)
    return stypes.matrixToList(xform)


@spiceErrorCheck
@spiceFoundExceptionThrower
def szpool(name):
    """
    Return the kernel pool size limitations.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/szpool_c.html

    :param name: Name of the parameter to be returned.
    :type name: str
    :return: Value of parameter specified by name,
    :rtype: int
    """
    name = stypes.stringToCharP(name)
    n = ctypes.c_int()
    found = ctypes.c_bool(0)
    libspice.szpool_c(name, ctypes.byref(n), ctypes.byref(found))
    return n.value, found.value


################################################################################
# T


@spiceErrorCheck
def timdef(action, item, lenout, value=None):
    """
    Set and retrieve the defaults associated with calendar input strings.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/timdef_c.html

    :param action: the kind of action to take "SET" or "GET".
    :type action: str
    :param item: the default item of interest.
    :type item: str
    :param lenout: the length of list for output.
    :type lenout: int
    :param value: the optional string used if action is "SET"
    :type value: str
    :return: the value associated with the default item.
    :rtype: str
    """
    action = stypes.stringToCharP(action)
    item = stypes.stringToCharP(item)
    lenout = ctypes.c_int(lenout)
    if value is None:
        value = stypes.stringToCharP(lenout)
    else:
        value = stypes.stringToCharP(value)
    libspice.timdef_c(action, item, lenout, value)
    return stypes.toPythonString(value)


@spiceErrorCheck
def timout(et, pictur, lenout=_default_len_out):
    """
    This vectorized routine converts an input epoch represented in TDB seconds
    past the TDB epoch of J2000 to a character string formatted to
    the specifications of a user's format picture.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/timout_c.html

    :param et: An epoch in seconds past the ephemeris epoch J2000.
    :type et: float or  Array of floats
    :param pictur: A format specification for the output string.
    :type pictur: str
    :param lenout: The length of the output string plus 1.
    :type lenout: int
    :return: A string representation of the input epoch.
    :rtype: str or array of str
    """
    if hasattr(et, "__iter__"):
        return numpy.array([timout(t, pictur, lenout) for t in et])
    pictur = stypes.stringToCharP(pictur)
    output = stypes.stringToCharP(lenout)
    lenout = ctypes.c_int(lenout)
    et = ctypes.c_double(et)
    libspice.timout_c(et, pictur, lenout, output)
    return stypes.toPythonString(output)


@spiceErrorCheck
def tipbod(ref, body, et):
    """
    Return a 3x3 matrix that transforms positions in inertial
    coordinates to positions in body-equator-and-prime-meridian
    coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tipbod_c.html

    :param ref: ID of inertial reference frame to transform from.
    :type ref: str
    :param body: ID code of body.
    :type body: int
    :param et: Epoch of transformation.
    :type et: float
    :return: Transformation (position), inertial to prime meridian.
    :rtype: 3x3-Element Array of floats
    """
    ref = stypes.stringToCharP(ref)
    body = ctypes.c_int(body)
    et = ctypes.c_double(et)
    retmatrix = stypes.emptyDoubleMatrix()
    libspice.tipbod_c(ref, body, et, retmatrix)
    return stypes.matrixToList(retmatrix)


@spiceErrorCheck
def tisbod(ref, body, et):
    """
    Return a 6x6 matrix that transforms states in inertial coordinates to
    states in body-equator-and-prime-meridian coordinates.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tisbod_c.html

    :param ref: ID of inertial reference frame to transform from.
    :type ref: str
    :param body: ID code of body.
    :type body: int
    :param et: Epoch of transformation.
    :type et: float
    :return: Transformation (state), inertial to prime meridian.
    :rtype: 6x6-Element Array of floats
    """
    ref = stypes.stringToCharP(ref)
    body = ctypes.c_int(body)
    et = ctypes.c_double(et)
    retmatrix = stypes.emptyDoubleMatrix(x=6, y=6)
    libspice.tisbod_c(ref, body, et, retmatrix)
    return stypes.matrixToList(retmatrix)


# @spiceErrorCheck
def tkvrsn(item):
    """
    Given an item such as the Toolkit or an entry point name, return
    the latest version string.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tkvrsn_c.html

    :param item: Item for which a version string is desired.
    :type item: str
    :return: the latest version string.
    :rtype: str
    """
    item = stypes.stringToCharP(item)
    return stypes.toPythonString(libspice.tkvrsn_c(item))


@spiceErrorCheck
def tparse(instring, lenout=_default_len_out):
    """
    Parse a time string and return seconds past the J2000
    epoch on a formal calendar.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tparse_c.html

    :param instring: Input time string, UTC.
    :type instring: str
    :param lenout: Available space in output error message string.
    :type lenout: int
    :return: Equivalent UTC seconds past J2000, Descriptive error message.
    :rtype: tuple
    """
    errmsg = stypes.stringToCharP(lenout)
    lenout = ctypes.c_int(lenout)
    instring = stypes.stringToCharP(instring)
    sp2000 = ctypes.c_double()
    libspice.tparse_c(instring, lenout, ctypes.byref(sp2000), errmsg)
    return sp2000.value, stypes.toPythonString(errmsg)


@spiceErrorCheck
def tpictr(sample, lenout, lenerr):
    """
    Given a sample time string, create a time format picture
    suitable for use by the routine timout.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tpictr_c.html

    :param sample: A sample time string.
    :type sample: str
    :param lenout: The length for the output picture string.
    :type lenout: int
    :param lenerr: The length for the output error string.
    :type lenerr: int
    :return:
            A format picture that describes sample,
            Flag indicating whether sample parsed successfully,
            Diagnostic returned if sample cannot be parsed
    :rtype: tuple
    """
    sample = stypes.stringToCharP(sample)
    pictur = stypes.stringToCharP(lenout)
    errmsg = stypes.stringToCharP(lenerr)
    lenout = ctypes.c_int(lenout)
    lenerr = ctypes.c_int(lenerr)
    ok = ctypes.c_bool()
    libspice.tpictr_c(sample, lenout, lenerr, pictur, ctypes.byref(ok), errmsg)
    return stypes.toPythonString(pictur), ok.value, stypes.toPythonString(
            errmsg)


@spiceErrorCheck
def trace(matrix):
    """
    Return the trace of a 3x3 matrix.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/trace_c.html

    :param matrix: 3x3 matrix of double precision numbers.
    :type matrix: 3x3-Element Array of floats
    :return: The trace of matrix.
    :rtype: float
    """
    matrix = stypes.toDoubleMatrix(matrix)
    return libspice.trace_c(matrix)


@spiceErrorCheck
def trcdep():
    """
    Return the number of modules in the traceback representation.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/trcdep_c.html

    :return: The number of modules in the traceback.
    :rtype: int
    """
    depth = ctypes.c_int()
    libspice.trcdep_c(ctypes.byref(depth))
    return depth.value


@spiceErrorCheck
def trcnam(index, namlen=_default_len_out):
    """
    Return the name of the module having the specified position in
    the trace representation. The first module to check in is at
    index 0.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/trcnam_c.html

    :param index: The position of the requested module name.
    :type index: int
    :param namlen: Available space in output name string.
    :type namlen: int
    :return: The name at position index in the traceback.
    :rtype: str
    """
    index = ctypes.c_int(index)
    name = stypes.stringToCharP(namlen)
    namlen = ctypes.c_int(namlen)
    libspice.trcnam_c(index, namlen, name)
    return stypes.toPythonString(name)


@spiceErrorCheck
def trcoff():
    # Todo: test trcoff
    """
    Disable tracing.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/trcoff_c.html

    """
    libspice.trcoff_c()


@spiceErrorCheck
def tsetyr(year):
    # Todo: test tsetyr
    """
    Set the lower bound on the 100 year range.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tsetyr_c.html

    :param year: Lower bound on the 100 year interval of expansion
    :type year: int
    """
    year = ctypes.c_int(year)
    libspice.tsetyr_c(year)


@spiceErrorCheck
def twopi():
    """
    Return twice the value of pi
    (the ratio of the circumference of a circle to its diameter).

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/twopi_c.html

    :return: Twice the value of pi.
    :rtype: float
    """
    return libspice.twopi_c()


@spiceErrorCheck
def twovec(axdef, indexa, plndef, indexp):
    """
    Find the transformation to the right-handed frame having a
    given vector as a specified axis and having a second given
    vector lying in a specified coordinate plane.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/twovec_c.html

    :param axdef: Vector defining a principal axis.
    :type axdef: 3-Element Array of floats
    :param indexa: Principal axis number of axdef (X=1, Y=2, Z=3).
    :type indexa: int
    :param plndef: Vector defining (with axdef) a principal plane.
    :type plndef: 3-Element Array of floats
    :param indexp: Second axis number (with indexa) of principal plane.
    :type indexp: int
    :return: Output rotation matrix.
    :rtype: 3x3-Element Array of floats
    """
    axdef = stypes.toDoubleVector(axdef)
    indexa = ctypes.c_int(indexa)
    plndef = stypes.toDoubleVector(plndef)
    indexp = ctypes.c_int(indexp)
    mout = stypes.emptyDoubleMatrix()
    libspice.twovec_c(axdef, indexa, plndef, indexp, mout)
    return stypes.matrixToList(mout)


@spiceErrorCheck
def tyear():
    """
    Return the number of seconds in a tropical year.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/tyear_c.html

    :return: The number of seconds in a tropical year.
    :rtype: float
    """
    return libspice.tyear_c()


################################################################################
# U

@spiceErrorCheck
def ucase(inchar, lenout=None):
    """
    Convert the characters in a string to uppercase.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ucase_c.html

    :param inchar: Input string.
    :type inchar: str
    :param lenout: Optional Maximum length of output string.
    :type lenout: int
    :return: Output string, all uppercase.
    :rtype: str
    """
    if lenout is None:
        lenout = len(inchar) + 1
    inchar = stypes.stringToCharP(inchar)
    outchar = stypes.stringToCharP(" " * lenout)
    lenout = ctypes.c_int(lenout)
    libspice.ucase_c(inchar, lenout, outchar)
    return stypes.toPythonString(outchar)


@spiceErrorCheck
def ucrss(v1, v2):
    """
    Compute the normalized cross product of two 3-vectors.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ucrss_c.html

    :param v1: Left vector for cross product.
    :type v1: 3-Element Array of floats
    :param v2: Right vector for cross product.
    :type v2: 3-Element Array of floats
    :return: Normalized cross product v1xv2 / abs(v1xv2).
    :rtype: Array of floats
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    vout = stypes.emptyDoubleVector(3)
    libspice.ucrss_c(v1, v2, vout)
    return stypes.vectorToList(vout)


def uddc(udfunc, x, dx):
    """
    SPICE private routine intended solely for the support of SPICE
    routines. Users should not call this routine directly due to the
    volatile nature of this routine.

    This routine calculates the derivative of 'udfunc' with respect
    to time for 'et', then determines if the derivative has a
    negative value.

    Use the @spiceypy.utils.callbacks.SpiceUDF dectorator to wrap
    a given python function that takes one parameter (float) and
    returns a float. For example::

        @spiceypy.utils.callbacks.SpiceUDF
        def udfunc(et_in):
            pos, new_et = spice.spkpos("MERCURY", et_in, "J2000", "LT+S", "MOON")
            return new_et

        deriv = spice.uddf(udfunc, et, 1.0)

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/uddc_c.html

    :param udfunc: Name of the routine that computes the scalar value of interest.
    :type udfunc: ctypes.CFunctionType
    :param x: Independent variable of 'udfunc'.
    :type x: float
    :param dx: Interval from 'x' for derivative calculation.
    :type dx: float
    :return: Boolean indicating if the derivative is negative.
    :rtype: bool
    """
    x = ctypes.c_double(x)
    dx = ctypes.c_double(dx)
    isdescr = ctypes.c_bool()
    libspice.uddc_c(udfunc, x, dx, ctypes.byref(isdescr))
    return isdescr.value


@spiceErrorCheck
def uddf(udfunc, x, dx):
    """
    Routine to calculate the first derivative of a caller-specified
    function using a three-point estimation.

    Use the @spiceypy.utils.callbacks.SpiceUDF dectorator to wrap
    a given python function that takes one parameter (float) and
    returns a float. For example::

        @spiceypy.utils.callbacks.SpiceUDF
        def udfunc(et_in):
            pos, new_et = spice.spkpos("MERCURY", et_in, "J2000", "LT+S", "MOON")
            return new_et

        deriv = spice.uddf(udfunc, et, 1.0)

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/uddf_c.html

    :param udfunc: Name of the routine that computes the scalar value of interest.
    :type udfunc: ctypes.CFunctionType
    :param x: Independent variable of 'udfunc'.
    :type x: float
    :param dx: Interval from 'x' for derivative calculation.
    :type dx: float
    :return: Approximate derivative of 'udfunc' at 'x'
    :rtype: float
    """
    x = ctypes.c_double(x)
    dx = ctypes.c_double(dx)
    deriv = ctypes.c_double()
    libspice.uddf_c(udfunc, x, dx, ctypes.byref(deriv))
    return deriv.value


def udf(x):
    """
    No-op routine for with an argument signature matching udfuns.
    Allways returns 0.0 .

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/udf_c.html

    :param x: Double precision value, unused.
    :type x: float
    :return: Double precision value, unused.
    :rtype: float
    """
    x = ctypes.c_double(x)
    value = ctypes.c_double()
    libspice.udf_c(x, ctypes.byref(value))
    return value.value


@spiceErrorCheck
def union(a, b):
    """
    Compute the union of two sets of any data type to form a third set.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/union_c.html

    :param a: First input set.
    :type a: spiceypy.utils.support_types.SpiceCell
    :param b: Second input set.
    :type b: spiceypy.utils.support_types.SpiceCell
    :return: Union of a and b.
    :rtype: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(a, stypes.SpiceCell)
    assert isinstance(b, stypes.SpiceCell)
    assert a.dtype == b.dtype
    assert a.dtype == 0 or a.dtype == 1 or a.dtype == 2
    if a.dtype is 0:
        c = stypes.SPICECHAR_CELL(max(a.size, b.size), max(a.length, b.length))
    elif a.dtype is 1:
        c = stypes.SPICEDOUBLE_CELL(max(a.size, b.size))
    elif a.dtype is 2:
        c = stypes.SPICEINT_CELL(max(a.size, b.size))
    else:
        raise NotImplementedError
    libspice.union_c(ctypes.byref(a), ctypes.byref(b), ctypes.byref(c))
    return c


@spiceErrorCheck
def unitim(epoch, insys, outsys):
    """
    Transform time from one uniform scale to another.  The uniform
    time scales are TAI, TDT, TDB, ET, JED, JDTDB, JDTDT.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/unitim_c.html

    :param epoch: An epoch to be converted.
    :type epoch: float
    :param insys: The time scale associated with the input epoch.
    :type insys: str
    :param outsys: The time scale associated with the function value.
    :type outsys: str
    :return:
            The float in outsys that is equivalent
            to the epoch on the insys time scale.
    :rtype: float
    """
    epoch = ctypes.c_double(epoch)
    insys = stypes.stringToCharP(insys)
    outsys = stypes.stringToCharP(outsys)
    return libspice.unitim_c(epoch, insys, outsys)


@spiceErrorCheck
def unload(filename):
    """
    Unload a SPICE kernel.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/unload_c.html

    :param filename: The name of a kernel to unload.
    :type filename: str
    """
    if isinstance(filename, list):
        for f in filename:
            libspice.unload_c(stypes.stringToCharP(f))
    filename = stypes.stringToCharP(filename)
    libspice.unload_c(filename)


@spiceErrorCheck
def unorm(v1):
    """
    Normalize a double precision 3-vector and return its magnitude.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/unorm_c.html

    :param v1: Vector to be normalized. 
    :type v1: 3-Element Array of floats
    :return: Unit vector of v1, Magnitude of v1.
    :rtype: tuple
    """
    v1 = stypes.toDoubleVector(v1)
    vout = stypes.emptyDoubleVector(3)
    vmag = ctypes.c_double()
    libspice.unorm_c(v1, vout, ctypes.byref(vmag))
    return stypes.vectorToList(vout), vmag.value


@spiceErrorCheck
def unormg(v1, ndim):
    """
    Normalize a double precision vector of arbitrary dimension and
    return its magnitude.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/unormg_c.html

    :param v1: Vector to be normalized. 
    :type v1: Array of floats
    :param ndim: This is the dimension of v1 and vout. 
    :type ndim: int
    :return: Unit vector of v1, Magnitude of v1.
    :rtype: tuple
    """
    v1 = stypes.toDoubleVector(v1)
    vout = stypes.emptyDoubleVector(ndim)
    vmag = ctypes.c_double()
    ndim = ctypes.c_int(ndim)
    libspice.unormg_c(v1, ndim, vout, ctypes.byref(vmag))
    return stypes.vectorToList(vout), vmag.value


@spiceErrorCheck
def utc2et(utcstr):
    """
    Convert an input time from Calendar or Julian Date format, UTC,
    to ephemeris seconds past J2000.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/utc2et_c.html

    :param utcstr: Input time string, UTC. 
    :type utcstr: str
    :return: Output epoch, ephemeris seconds past J2000.
    :rtype: float
    """
    utcstr = stypes.stringToCharP(utcstr)
    et = ctypes.c_double()
    libspice.utc2et_c(utcstr, ctypes.byref(et))
    return et.value


################################################################################
# V


@spiceErrorCheck
def vadd(v1, v2):
    """ Add two 3 dimensional vectors.
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vadd_c.html

    :param v1: First vector to be added. 
    :type v1: 3-Element Array of floats
    :param v2: Second vector to be added. 
    :type v2: 3-Element Array of floats
    :return: v1+v2
    :rtype: 3-Element Array of floats
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    vout = stypes.emptyDoubleVector(3)
    libspice.vadd_c(v1, v2, vout)
    return stypes.vectorToList(vout)


@spiceErrorCheck
def vaddg(v1, v2, ndim):
    """ Add two n-dimensional vectors
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vaddg_c.html

    :param v1: First vector to be added. 
    :type v1: list[ndim]
    :param v2: Second vector to be added. 
    :type v2: list[ndim]
    :param ndim: Dimension of v1 and v2. 
    :type ndim: int
    :return: v1+v2
    :rtype: list[ndim]
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    vout = stypes.emptyDoubleVector(ndim)
    ndim = ctypes.c_int(ndim)
    libspice.vaddg_c(v1, v2, ndim, vout)
    return stypes.vectorToList(vout)


@spiceErrorCheck
def valid(insize, n, inset):
    """
    Create a valid CSPICE set from a CSPICE Cell of any data type.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/valid_c.html

    :param insize: Size (maximum cardinality) of the set. 
    :type insize: int
    :param n: Initial no. of (possibly non-distinct) elements. 
    :type n: int
    :param inset: Set to be validated.
    :return: validated set
    :rtype: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(inset, stypes.SpiceCell)
    insize = ctypes.c_int(insize)
    n = ctypes.c_int(n)
    libspice.valid_c(insize, n, inset)
    return inset


@spiceErrorCheck
def vcrss(v1, v2):
    """
    Compute the cross product of two 3-dimensional vectors.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vcrss_c.html

    :param v1: Left hand vector for cross product. 
    :type v1: 3-Element Array of floats
    :param v2: Right hand vector for cross product. 
    :type v2: 3-Element Array of floats
    :return: Cross product v1 x v2.
    :rtype: 3-Element Array of floats
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    vout = stypes.emptyDoubleVector(3)
    libspice.vcrss_c(v1, v2, vout)
    return stypes.vectorToList(vout)


@spiceErrorCheck
def vdist(v1, v2):
    """
    Return the distance between two three-dimensional vectors.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vdist_c.html

    :param v1: First vector in the dot product. 
    :type v1: 3-Element Array of floats
    :param v2: Second vector in the dot product. 
    :type v2: 3-Element Array of floats
    :return: the distance between v1 and v2
    :rtype: float
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    return libspice.vdist_c(v1, v2)


@spiceErrorCheck
def vdistg(v1, v2, ndim):
    """
    Return the distance between two vectors of arbitrary dimension.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vdistg_c.html

    :param v1: ndim-dimensional double precision vector. 
    :type v1: list[ndim]
    :param v2: ndim-dimensional double precision vector. 
    :type v2: list[ndim]
    :param ndim: Dimension of v1 and v2. 
    :type ndim: int
    :return: the distance between v1 and v2
    :rtype: float
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    ndim = ctypes.c_int(ndim)
    return libspice.vdistg_c(v1, v2, ndim)


@spiceErrorCheck
def vdot(v1, v2):
    """
    Compute the dot product of two double precision, 3-dimensional vectors.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vdot_c.html

    :param v1: First vector in the dot product. 
    :type v1: 3-Element Array of floats
    :param v2: Second vector in the dot product. 
    :type v2: 3-Element Array of floats
    :return: dot product of v1 and v2.
    :rtype: float
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    return libspice.vdot_c(v1, v2)


@spiceErrorCheck
def vdotg(v1, v2, ndim):
    """
    Compute the dot product of two double precision vectors of
    arbitrary dimension.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vdotg_c.html

    :param v1: First vector in the dot product. 
    :type v1: list[ndim]
    :param v2: Second vector in the dot product. 
    :type v2: list[ndim]
    :param ndim: Dimension of v1 and v2. 
    :type ndim: int
    :return: dot product of v1 and v2.
    :rtype: float
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    ndim = ctypes.c_int(ndim)
    return libspice.vdotg_c(v1, v2, ndim)


@spiceErrorCheck
def vequ(v1):
    """
    Make one double precision 3-dimensional vector equal to another.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vequ_c.html

    :param v1: 3-dimensional double precision vector. 
    :type v1: 3-Element Array of floats
    :return: 3-dimensional double precision vector set equal to vin.
    :rtype: 3-Element Array of floats
    """
    v1 = stypes.toDoubleVector(v1)
    vout = stypes.emptyDoubleVector(3)
    libspice.vequ_c(v1, vout)
    return stypes.vectorToList(vout)


@spiceErrorCheck
def vequg(v1, ndim):
    """
    Make one double precision vector of arbitrary dimension equal to another.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vequg_c.html

    :param v1: ndim-dimensional double precision vector. 
    :type v1: list[ndim]
    :param ndim: Dimension of vin (and also vout). 
    :type ndim: int
    :return: ndim-dimensional double precision vector set equal to vin.
    :rtype: list[ndim]
    """
    v1 = stypes.toDoubleVector(v1)
    vout = stypes.emptyDoubleVector(ndim)
    ndim = ctypes.c_int(ndim)
    libspice.vequg_c(v1, ndim, vout)
    return stypes.vectorToList(vout)


@spiceErrorCheck
def vhat(v1):
    """
    Find the unit vector along a double precision 3-dimensional vector.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vhat_c.html

    :param v1: Vector to be unitized. 
    :type v1: 3-Element Array of floats
    :return: Unit vector v / abs(v).
    :rtype: 3-Element Array of floats
    """
    v1 = stypes.toDoubleVector(v1)
    vout = stypes.emptyDoubleVector(3)
    libspice.vhat_c(v1, vout)
    return stypes.vectorToList(vout)


@spiceErrorCheck
def vhatg(v1, ndim):
    """
    Find the unit vector along a double precision vector of arbitrary dimension.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vhatg_c.html

    :param v1: Vector to be normalized. 
    :type v1: list[ndim]
    :param ndim: Dimension of v1 (and also vout). 
    :type ndim: int
    :return: Unit vector v / abs(v).
    :rtype: list[ndim]
    """
    v1 = stypes.toDoubleVector(v1)
    vout = stypes.emptyDoubleVector(ndim)
    ndim = ctypes.c_int(ndim)
    libspice.vhatg_c(v1, ndim, vout)
    return stypes.vectorToList(vout)


@spiceErrorCheck
def vlcom(a, v1, b, v2):
    """
    Compute a vector linear combination of two double precision,
    3-dimensional vectors.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vlcom_c.html

    :param a: Coefficient of v1 
    :type a: float
    :param v1: Vector in 3-space 
    :type v1: 3-Element Array of floats
    :param b: Coefficient of v2 
    :type b: float
    :param v2: Vector in 3-space 
    :type v2: 3-Element Array of floats
    :return: Linear Vector Combination a*v1 + b*v2.
    :rtype: 3-Element Array of floats
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    sumv = stypes.emptyDoubleVector(3)
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    libspice.vlcom_c(a, v1, b, v2, sumv)
    return stypes.vectorToList(sumv)


@spiceErrorCheck
def vlcom3(a, v1, b, v2, c, v3):
    """
    This subroutine computes the vector linear combination
    a*v1 + b*v2 + c*v3 of double precision, 3-dimensional vectors.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vlcom3_c.html

    :param a: Coefficient of v1 
    :type a: float
    :param v1: Vector in 3-space 
    :type v1: 3-Element Array of floats
    :param b: Coefficient of v2 
    :type b: float
    :param v2: Vector in 3-space 
    :type v2: 3-Element Array of floats
    :param c: Coefficient of v3 
    :type c: float
    :param v3: Vector in 3-space 
    :type v3: 3-Element Array of floats
    :return: Linear Vector Combination a*v1 + b*v2 + c*v3
    :rtype: 3-Element Array of floats
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    v3 = stypes.toDoubleVector(v3)
    sumv = stypes.emptyDoubleVector(3)
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    libspice.vlcom3_c(a, v1, b, v2, c, v3, sumv)
    return stypes.vectorToList(sumv)


@spiceErrorCheck
def vlcomg(n, a, v1, b, v2):
    """
    Compute a vector linear combination of two double precision
    vectors of arbitrary dimension.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vlcomg_c.html

    :param n: Dimension of vector space 
    :type n: int
    :param a: Coefficient of v1 
    :type a: float
    :param v1: Vector in n-space 
    :type v1: list[n]
    :param b: Coefficient of v2 
    :type b: float
    :param v2: Vector in n-space 
    :type v2: list[n]
    :return: Linear Vector Combination a*v1 + b*v2
    :rtype: list[n]
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    sumv = stypes.emptyDoubleVector(n)
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    n = ctypes.c_int(n)
    libspice.vlcomg_c(n, a, v1, b, v2, sumv)
    return stypes.vectorToList(sumv)


@spiceErrorCheck
def vminug(vin, ndim):
    """
    Negate a double precision vector of arbitrary dimension.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vminug_c.html

    :param vin: ndim-dimensional double precision vector to be negated. 
    :type vin: Array of floats
    :param ndim: Dimension of vin. 
    :type ndim: int
    :return: ndim-dimensional double precision vector equal to -vin.
    :rtype: list[ndim]
    """
    vin = stypes.toDoubleVector(vin)
    vout = stypes.emptyDoubleVector(ndim)
    ndim = ctypes.c_int(ndim)
    libspice.vminug_c(vin, ndim, vout)
    return stypes.vectorToList(vout)


@spiceErrorCheck
def vminus(vin):
    """
    Negate a double precision 3-dimensional vector.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vminus_c.html

    :param vin: Vector to be negated. 
    :type vin: 3-Element Array of floats
    :return: Negated vector -v1.
    :rtype: 3-Element Array of floats
    """
    vin = stypes.toDoubleVector(vin)
    vout = stypes.emptyDoubleVector(3)
    libspice.vminus_c(vin, vout)
    return stypes.vectorToList(vout)


@spiceErrorCheck
def vnorm(v):
    """
    Compute the magnitude of a double precision, 3-dimensional vector.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vnorm_c.html

    :param v: Vector whose magnitude is to be found. 
    :type v: 3-Element Array of floats
    :return: magnitude of v calculated in a numerically stable way
    :rtype: float
    """
    v = stypes.toDoubleVector(v)
    return libspice.vnorm_c(v)


@spiceErrorCheck
def vnormg(v, ndim):
    """
    Compute the magnitude of a double precision vector of arbitrary dimension.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vnormg_c.html

    :param v: Vector whose magnitude is to be found. 
    :type v: Array of floats
    :param ndim: Dimension of v 
    :type ndim: int
    :return: magnitude of v calculated in a numerically stable way
    :rtype: float
    """
    v = stypes.toDoubleVector(v)
    ndim = ctypes.c_int(ndim)
    return libspice.vnormg_c(v, ndim)


@spiceErrorCheck
def vpack(x, y, z):
    """
    Pack three scalar components into a vector.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vpack_c.html

    :param x: first scalar component 
    :type x: float
    :param y: second scalar component 
    :type y: float
    :param z: third scalar component 
    :type z: float
    :return: Equivalent 3-vector.
    :rtype: 3-Element Array of floats
    """
    x = ctypes.c_double(x)
    y = ctypes.c_double(y)
    z = ctypes.c_double(z)
    vout = stypes.emptyDoubleVector(3)
    libspice.vpack_c(x, y, z, vout)
    return stypes.vectorToList(vout)


@spiceErrorCheck
def vperp(a, b):
    """
    Find the component of a vector that is perpendicular to a second
    vector. All vectors are 3-dimensional.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vperp_c.html

    :param a: The vector whose orthogonal component is sought. 
    :type a: 3-Element Array of floats
    :param b: The vector used as the orthogonal reference. 
    :type b: 3-Element Array of floats
    :return: The component of a orthogonal to b.
    :rtype: 3-Element Array of floats
    """
    a = stypes.toDoubleVector(a)
    b = stypes.toDoubleVector(b)
    vout = stypes.emptyDoubleVector(3)
    libspice.vperp_c(a, b, vout)
    return stypes.vectorToList(vout)


@spiceErrorCheck
def vprjp(vin, plane):
    """
    Project a vector onto a specified plane, orthogonally.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vprjp_c.html

    :param vin: The projected vector. 
    :type vin: 3-Element Array of floats
    :param plane: Plane containing vin. 
    :type plane: spiceypy.utils.support_types.Plane
    :return: Vector resulting from projection.
    :rtype: 3-Element Array of floats
    """
    vin = stypes.toDoubleVector(vin)
    vout = stypes.emptyDoubleVector(3)
    libspice.vprjp_c(vin, ctypes.byref(plane), vout)
    return stypes.vectorToList(vout)


@spiceErrorCheck
@spiceFoundExceptionThrower
def vprjpi(vin, projpl, invpl):
    """
    Find the vector in a specified plane that maps to a specified
    vector in another plane under orthogonal projection.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vprjpi_c.html

    :param vin: The projected vector. 
    :type vin: 3-Element Array of floats
    :param projpl: Plane containing vin. 
    :type projpl: spiceypy.utils.support_types.Plane
    :param invpl: Plane containing inverse image of vin. 
    :type invpl: spiceypy.utils.support_types.Plane
    :return: Inverse projection of vin.
    :rtype: list
    """
    vin = stypes.toDoubleVector(vin)
    vout = stypes.emptyDoubleVector(3)
    found = ctypes.c_bool()
    libspice.vprjpi_c(vin, ctypes.byref(projpl), ctypes.byref(invpl), vout,
                      ctypes.byref(found))
    return stypes.vectorToList(vout), found.value


@spiceErrorCheck
def vproj(a, b):
    """
    Find the projection of one vector onto another vector.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vproj_c.html

    :param a: The vector to be projected. 
    :type a: 3-Element Array of floats
    :param b: The vector onto which a is to be projected. 
    :type b: 3-Element Array of floats
    :return: The projection of a onto b.
    :rtype: 3-Element Array of floats
    """
    a = stypes.toDoubleVector(a)
    b = stypes.toDoubleVector(b)
    vout = stypes.emptyDoubleVector(3)
    libspice.vproj_c(a, b, vout)
    return stypes.vectorToList(vout)


@spiceErrorCheck
def vrel(v1, v2):
    """
    Return the relative difference between two 3-dimensional vectors.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vrel_c.html

    :param v1: First vector 
    :type v1: 3-Element Array of floats
    :param v2: Second vector 
    :type v2: 3-Element Array of floats
    :return: the relative difference between v1 and v2.
    :rtype: float
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    return libspice.vrel_c(v1, v2)


@spiceErrorCheck
def vrelg(v1, v2, ndim):
    """
    Return the relative difference between two vectors of general dimension.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vrelg_c.html

    :param v1: First vector 
    :type v1: Array of floats
    :param v2: Second vector 
    :type v2: Array of floats
    :param ndim: Dimension of v1 and v2.
    :type ndim: int
    :return: the relative difference between v1 and v2.
    :rtype: float
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    ndim = ctypes.c_int(ndim)
    return libspice.vrelg_c(v1, v2, ndim)


@spiceErrorCheck
def vrotv(v, axis, theta):
    """
    Rotate a vector about a specified axis vector by a
    specified angle and return the rotated vector.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vrotv_c.html

    :param v: Vector to be rotated. 
    :type v: 3-Element Array of floats
    :param axis: Axis of the rotation. 
    :type axis: 3-Element Array of floats
    :param theta: Angle of rotation (radians). 
    :type theta: float
    :return: Result of rotating v about axis by theta
    :rtype: 3-Element Array of floats
    """
    v = stypes.toDoubleVector(v)
    axis = stypes.toDoubleVector(axis)
    theta = ctypes.c_double(theta)
    r = stypes.emptyDoubleVector(3)
    libspice.vrotv_c(v, axis, theta, r)
    return stypes.vectorToList(r)


@spiceErrorCheck
def vscl(s, v1):
    """
    Multiply a scalar and a 3-dimensional double precision vector.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vscl_c.html

    :param s: Scalar to multiply a vector 
    :type s: float
    :param v1: Vector to be multiplied 
    :type v1: 3-Element Array of floats
    :return: Product vector, s*v1.
    :rtype: 3-Element Array of floats
    """
    s = ctypes.c_double(s)
    v1 = stypes.toDoubleVector(v1)
    vout = stypes.emptyDoubleVector(3)
    libspice.vscl_c(s, v1, vout)
    return stypes.vectorToList(vout)


@spiceErrorCheck
def vsclg(s, v1, ndim):
    """
    Multiply a scalar and a double precision vector of arbitrary dimension.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vsclg_c.html

    :param s: Scalar to multiply a vector 
    :type s: float
    :param v1: Vector to be multiplied 
    :type v1: Array of floats
    :param ndim: Dimension of v1 
    :type ndim: int
    :return: Product vector, s*v1.
    :rtype: Array of floats
    """
    s = ctypes.c_double(s)
    v1 = stypes.toDoubleVector(v1)
    vout = stypes.emptyDoubleVector(ndim)
    ndim = ctypes.c_int(ndim)
    libspice.vsclg_c(s, v1, ndim, vout)
    return stypes.vectorToList(vout)


@spiceErrorCheck
def vsep(v1, v2):
    """
    Find the separation angle in radians between two double
    precision, 3-dimensional vectors. This angle is defined as zero
    if either vector is zero.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vsep_c.html

    :param v1: First vector 
    :type v1: 3-Element Array of floats
    :param v2: Second vector 
    :type v2: 3-Element Array of floats
    :return: separation angle in radians
    :rtype: float
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    return libspice.vsep_c(v1, v2)


@spiceErrorCheck
def vsepg(v1, v2, ndim):
    """
    Find the separation angle in radians between two double
    precision vectors of arbitrary dimension. This angle is defined
    as zero if either vector is zero.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vsepg_c.html

    :param v1: First vector 
    :type v1: Array of floats
    :param v2: Second vector 
    :type v2: Array of floats
    :param ndim: The number of elements in v1 and v2. 
    :type ndim: int
    :return: separation angle in radians
    :rtype: float
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    ndim = ctypes.c_int(ndim)
    return libspice.vsepg_c(v1, v2, ndim)


@spiceErrorCheck
def vsub(v1, v2):
    """
    Compute the difference between two 3-dimensional,
    double precision vectors.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vsub_c.html

    :param v1: First vector (minuend). 
    :type v1: 3-Element Array of floats
    :param v2: Second vector (subtrahend). 
    :type v2: 3-Element Array of floats
    :return: Difference vector, v1 - v2.
    :rtype: 3-Element Array of floats
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    vout = stypes.emptyDoubleVector(3)
    libspice.vsub_c(v1, v2, vout)
    return stypes.vectorToList(vout)


@spiceErrorCheck
def vsubg(v1, v2, ndim):
    """
    Compute the difference between two double precision
    vectors of arbitrary dimension.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vsubg_c.html

    :param v1: First vector (minuend). 
    :type v1: Array of floats
    :param v2: Second vector (subtrahend). 
    :type v2: Array of floats
    :param ndim: Dimension of v1, v2, and vout. 
    :type ndim: int
    :return: Difference vector, v1 - v2.
    :rtype: Array of floats
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    vout = stypes.emptyDoubleVector(ndim)
    ndim = ctypes.c_int(ndim)
    libspice.vsubg_c(v1, v2, ndim, vout)
    return stypes.vectorToList(vout)


@spiceErrorCheck
def vtmv(v1, matrix, v2):
    """
    Multiply the transpose of a 3-dimensional column vector
    a 3x3 matrix, and a 3-dimensional column vector.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vtmv_c.html

    :param v1: 3 dimensional double precision column vector. 
    :type v1: 3-Element Array of floats
    :param matrix: 3x3 double precision matrix. 
    :type matrix: 3x3-Element Array of floats
    :param v2: 3 dimensional double precision column vector. 
    :type v2: 3-Element Array of floats
    :return: the result of (v1**t * matrix * v2 ).
    :rtype: float
    """
    v1 = stypes.toDoubleVector(v1)
    matrix = stypes.listtodoublematrix(matrix)
    v2 = stypes.toDoubleVector(v2)
    return libspice.vtmv_c(v1, matrix, v2)


@spiceErrorCheck
def vtmvg(v1, matrix, v2, nrow, ncol):
    """
    Multiply the transpose of a n-dimensional
    column vector a nxm matrix,
    and a m-dimensional column vector.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vtmvg_c.html

    :param v1: n-dimensional double precision column vector. 
    :type v1: Array of floats
    :param matrix: nxm double precision matrix. 
    :type matrix: NxM-Element Array of floats
    :param v2: m-dimensional double porecision column vector. 
    :type v2: Array of floats
    :param nrow: Number of rows in matrix (number of rows in v1.) 
    :type nrow: int
    :param ncol: Number of columns in matrix (number of rows in v2.) 
    :type ncol: int
    :return: the result of (v1**t * matrix * v2 )
    :rtype: float
    """
    v1 = stypes.toDoubleVector(v1)
    matrix = stypes.listtodoublematrix(matrix, x=ncol, y=nrow)
    v2 = stypes.toDoubleVector(v2)
    nrow = ctypes.c_int(nrow)
    ncol = ctypes.c_int(ncol)
    return libspice.vtmvg_c(v1, matrix, v2, nrow, ncol)


@spiceErrorCheck
def vupack(v):
    """
    Unpack three scalar components from a vector.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vupack_c.html

    :param v: Vector 
    :type v: 3-Element Array of floats
    :return: (x, y, z)
    :rtype: tuple
    """
    v1 = stypes.toDoubleVector(v)
    x = ctypes.c_double()
    y = ctypes.c_double()
    z = ctypes.c_double()
    libspice.vupack_c(v1, ctypes.byref(x), ctypes.byref(y), ctypes.byref(z))
    return x.value, y.value, z.value


@spiceErrorCheck
def vzero(v):
    """
    Indicate whether a 3-vector is the zero vector.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vzero_c.html

    :param v: Vector to be tested 
    :type v: 3-Element Array of floats
    :return: true if and only if v is the zero vector
    :rtype: bool
    """
    v = stypes.toDoubleVector(v)
    return libspice.vzero_c(v)


@spiceErrorCheck
def vzerog(v, ndim):
    """
    Indicate whether a general-dimensional vector is the zero vector.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/vzerog_c.html

    :param v: Vector to be tested 
    :type v: Array of floats
    :param ndim: Dimension of v 
    :type ndim: int
    :return: true if and only if v is the zero vector
    :rtype: bool
    """
    v = stypes.toDoubleVector(v)
    ndim = ctypes.c_int(ndim)
    return libspice.vzerog_c(v, ndim)


################################################################################
# W


@spiceErrorCheck
def wncard(window):
    """
    Return the cardinality (number of intervals) of a double
    precision window.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wncard_c.html

    :param window: Input window 
    :type window: spiceypy.utils.support_types.SpiceCell
    :return: the cardinality of the input window.
    :rtype: int
    """
    assert isinstance(window, stypes.SpiceCell)
    return libspice.wncard_c(window)


@spiceErrorCheck
def wncomd(left, right, window):
    """
    Determine the complement of a double precision window with
    respect to a specified interval.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wncomd_c.html

    :param left: left endpoints of complement interval. 
    :type left: float
    :param right: right endpoints of complement interval. 
    :type right: float
    :param window: Input window 
    :type window: spiceypy.utils.support_types.SpiceCell
    :return: Complement of window with respect to left and right.
    :rtype: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    left = ctypes.c_double(left)
    right = ctypes.c_double(right)
    result = stypes.SpiceCell.double(window.size)
    libspice.wncomd_c(left, right, ctypes.byref(window), result)
    return result


@spiceErrorCheck
def wncond(left, right, window):
    """
    Contract each of the intervals of a double precision window.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wncond_c.html

    :param left: Amount added to each left endpoint. 
    :type left: float
    :param right: Amount subtracted from each right endpoint. 
    :type right: float
    :param window: Window to be contracted 
    :type window: spiceypy.utils.support_types.SpiceCell
    :return: Contracted Window.
    :rtype: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    left = ctypes.c_double(left)
    right = ctypes.c_double(right)
    libspice.wncond_c(left, right, ctypes.byref(window))
    return window


@spiceErrorCheck
def wndifd(a, b):
    """
    Place the difference of two double precision windows into
    a third window.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wndifd_c.html

    :param a: Input window A. 
    :type a: spiceypy.utils.support_types.SpiceCell
    :param b: Input window B. 
    :type b: spiceypy.utils.support_types.SpiceCell
    :return: Difference of a and b.
    :rtype: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(a, stypes.SpiceCell)
    assert isinstance(b, stypes.SpiceCell)
    assert a.dtype == 1
    assert b.dtype == 1
    c = stypes.SpiceCell.double(a.size + b.size)
    libspice.wndifd_c(ctypes.byref(a), ctypes.byref(b), ctypes.byref(c))
    return c


@spiceErrorCheck
def wnelmd(point, window):
    """
    Determine whether a point is an element of a double precision
    window.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wnelmd_c.html

    :param point: Input point. 
    :type point: float
    :param window: Input window 
    :type window: spiceypy.utils.support_types.SpiceCell
    :return: returns True if point is an element of window.
    :rtype: bool
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    point = ctypes.c_double(point)
    return libspice.wnelmd_c(point, ctypes.byref(window))


@spiceErrorCheck
def wnexpd(left, right, window):
    """
    Expand each of the intervals of a double precision window.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wnexpd_c.html

    :param left: Amount subtracted from each left endpoint. 
    :type left: float
    :param right: Amount added to each right endpoint. 
    :type right: float
    :param window: Window to be expanded. 
    :type window: spiceypy.utils.support_types.SpiceCell
    :return: Expanded Window.
    :rtype: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    left = ctypes.c_double(left)
    right = ctypes.c_double(right)
    libspice.wnexpd_c(left, right, ctypes.byref(window))
    return window


@spiceErrorCheck
def wnextd(side, window):
    """
    Extract the left or right endpoints from a double precision
    window.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wnextd_c.html

    :param side: Extract left "L" or right "R" endpoints. 
    :type side: str
    :param window: Window to be extracted. 
    :type window: spiceypy.utils.support_types.SpiceCell
    :return: Extracted Window.
    :rtype: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    assert side == 'L' or side == 'R'
    side = ctypes.c_char(side.encode(encoding='UTF-8'))
    libspice.wnextd_c(side, ctypes.byref(window))
    return window


@spiceErrorCheck
def wnfetd(window, n):
    """
    Fetch a particular interval from a double precision window.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wnfetd_c.html

    :param window: Input window 
    :type window: spiceypy.utils.support_types.SpiceCell
    :param n: Index of interval to be fetched. 
    :type n: int
    :return: Left, right endpoints of the nth interval.
    :rtype: tuple
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    n = ctypes.c_int(n)
    left = ctypes.c_double()
    right = ctypes.c_double()
    libspice.wnfetd_c(ctypes.byref(window), n, ctypes.byref(left),
                      ctypes.byref(right))
    return left.value, right.value


@spiceErrorCheck
def wnfild(small, window):
    """
    Fill small gaps between adjacent intervals of a double precision window.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wnfild_c.html

    :param small: Limiting measure of small gaps. 
    :type small: float
    :param window: Window to be filled 
    :type window: spiceypy.utils.support_types.SpiceCell
    :return: Filled Window.
    :rtype: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    small = ctypes.c_double(small)
    libspice.wnfild_c(small, ctypes.byref(window))
    return window


@spiceErrorCheck
def wnfltd(small, window):
    """
    Filter (remove) small intervals from a double precision window.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wnfltd_c.html

    :param small: Limiting measure of small intervals. 
    :type small: float
    :param window: Window to be filtered. 
    :type window: spiceypy.utils.support_types.SpiceCell
    :return: Filtered Window.
    :rtype: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    small = ctypes.c_double(small)
    libspice.wnfltd_c(small, ctypes.byref(window))
    return window


@spiceErrorCheck
def wnincd(left, right, window):
    """
    Determine whether an interval is included in a double precision window.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wnincd_c.html

    :param left: Left interval 
    :type left: float
    :param right: Right interval 
    :type right: float
    :param window: Input window 
    :type window: spiceypy.utils.support_types.SpiceCell
    :return: Returns True if the input interval is included in window.
    :rtype: bool
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    left = ctypes.c_double(left)
    right = ctypes.c_double(right)
    return libspice.wnincd_c(left, right, ctypes.byref(window))


@spiceErrorCheck
def wninsd(left, right, window):
    """
    Insert an interval into a double precision window.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wninsd_c.html

    :param left: Left endpoints of new interval. 
    :type left: float
    :param right: Right endpoints of new interval. 
    :type right: float
    :param window: Input window. 
    :type window: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    left = ctypes.c_double(left)
    right = ctypes.c_double(right)
    libspice.wninsd_c(left, right, ctypes.byref(window))


@spiceErrorCheck
def wnintd(a, b):
    """
    Place the intersection of two double precision windows into
    a third window.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wnintd_c.html


    :param a: Input window A. 
    :type a: spiceypy.utils.support_types.SpiceCell
    :param b: Input window B. 
    :type b: spiceypy.utils.support_types.SpiceCell
    :return: Intersection of a and b.
    :rtype: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(a, stypes.SpiceCell)
    assert b.dtype == 1
    assert isinstance(b, stypes.SpiceCell)
    assert a.dtype == 1
    c = stypes.SpiceCell.double(b.size + a.size)
    libspice.wnintd_c(ctypes.byref(a), ctypes.byref(b), ctypes.byref(c))
    return c


@spiceErrorCheck
def wnreld(a, op, b):
    """
    Compare two double precision windows.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wnreld_c.html

    :param a: First window. 
    :type a: spiceypy.utils.support_types.SpiceCell
    :param op: Comparison operator. 
    :type op: str
    :param b: Second window. 
    :type b: spiceypy.utils.support_types.SpiceCell
    :return: The result of comparison: a (op) b.
    :rtype: bool
    """
    assert isinstance(a, stypes.SpiceCell)
    assert b.dtype == 1
    assert isinstance(b, stypes.SpiceCell)
    assert a.dtype == 1
    assert isinstance(op, str)
    op = stypes.stringToCharP(op.encode(encoding='UTF-8'))
    return libspice.wnreld_c(ctypes.byref(a), op, ctypes.byref(b))


@spiceErrorCheck
def wnsumd(window):
    """
    Summarize the contents of a double precision window.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wnsumd_c.html

    :param window: Window to be summarized. 
    :type window: spiceypy.utils.support_types.SpiceCell
    :return:
            Total measure of intervals in window,
            Average measure, Standard deviation,
            Location of shortest interval,
            Location of longest interval.
    :rtype: tuple
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    meas = ctypes.c_double()
    avg = ctypes.c_double()
    stddev = ctypes.c_double()
    shortest = ctypes.c_int()
    longest = ctypes.c_int()
    libspice.wnsumd_c(ctypes.byref(window), ctypes.byref(meas),
                      ctypes.byref(avg), ctypes.byref(stddev),
                      ctypes.byref(shortest), ctypes.byref(longest))
    return meas.value, avg.value, stddev.value, shortest.value, longest.value


@spiceErrorCheck
def wnunid(a, b):
    """
    Place the union of two double precision windows into a third window.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wnunid_c.html

    :param a: Input window A. 
    :type a: spiceypy.utils.support_types.SpiceCell
    :param b: Input window B. 
    :type b: spiceypy.utils.support_types.SpiceCell
    :return: Union of a and b.
    :rtype: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(a, stypes.SpiceCell)
    assert b.dtype == 1
    assert isinstance(b, stypes.SpiceCell)
    assert a.dtype == 1
    c = stypes.SpiceCell.double(b.size + a.size)
    libspice.wnunid_c(ctypes.byref(a), ctypes.byref(b), ctypes.byref(c))
    return c


@spiceErrorCheck
def wnvald(insize, n, window):
    """
    Form a valid double precision window from the contents
    of a window array.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/wnvald_c.html

    :param insize: Size of window. 
    :type insize: int
    :param n: Original number of endpoints. 
    :type n: int
    :param window: Input window. 
    :type window: spiceypy.utils.support_types.SpiceCell
    :return: The union of the intervals in the input cell.
    :rtype: spiceypy.utils.support_types.SpiceCell
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    insize = ctypes.c_int(insize)
    n = ctypes.c_int(n)
    libspice.wnvald_c(insize, n, ctypes.byref(window))
    return window


################################################################################
# X

@spiceErrorCheck
def xf2eul(xform, axisa, axisb, axisc):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/xf2eul_c.html

    :param xform: state transformation matrix 
    :type xform: list[6][6]
    :param axisa: Axis A of the Euler angle factorization. 
    :type axisa: int
    :param axisb: Axis B of the Euler angle factorization. 
    :type axisb: int
    :param axisc: Axis C of the Euler angle factorization. 
    :type axisc: int
    :return: (eulang, unique)
    :rtype: tuple
    """
    xform = stypes.listtodoublematrix(xform, x=6, y=6)
    axisa = ctypes.c_int(axisa)
    axisb = ctypes.c_int(axisb)
    axisc = ctypes.c_int(axisc)
    eulang = stypes.emptyDoubleVector(6)
    unique = ctypes.c_bool()
    libspice.xf2eul_c(xform, axisa, axisb, axisc, eulang, unique)
    return stypes.vectorToList(eulang), unique.value


@spiceErrorCheck
def xf2rav(xform):
    """
    This routine determines the rotation matrix and angular velocity
    of the rotation from a state transformation matrix.
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/xf2rav_c.html

    :param xform: state transformation matrix 
    :type xform: list[6][6]
    :return:
            rotation associated with xform,
            angular velocity associated with xform.
    :rtype: tuple
    """
    xform = stypes.listtodoublematrix(xform, x=6, y=6)
    rot = stypes.emptyDoubleMatrix()
    av = stypes.emptyDoubleVector(3)
    libspice.xf2rav_c(xform, rot, av)
    return stypes.matrixToList(rot), stypes.vectorToList(av)


@spiceErrorCheck
def xfmsta(input_state, input_coord_sys, output_coord_sys, body):
    """
    Transform a state between coordinate systems.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/xfmsta_c.html

    :param input_state: Input state. 
    :type input_state: 6-Element Array of floats
    :param input_coord_sys: Current (input) coordinate system. 
    :type input_coord_sys: str
    :param output_coord_sys: Desired (output) coordinate system. 
    :type output_coord_sys: str
    :param body:
                Name or NAIF ID of body with which coordinates
                are associated (if applicable).
    :type body: str
    :return: Converted output state
    :rtype: 6-Element Array of floats
    """
    input_state = stypes.toDoubleVector(input_state)
    input_coord_sys = stypes.stringToCharP(input_coord_sys)
    output_coord_sys = stypes.stringToCharP(output_coord_sys)
    body = stypes.stringToCharP(body)
    output_state = stypes.emptyDoubleVector(6)
    libspice.xfmsta_c(input_state, input_coord_sys, output_coord_sys, body,
                      output_state)
    return stypes.vectorToList(output_state)


@spiceErrorCheck
def xpose(m):
    """
    Transpose a 3x3 matrix

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/xpose_c.html

    :param m: Matrix to be transposed 
    :type m: 3x3-Element Array of floats
    :return: Transposed matrix
    :rtype: 3x3-Element Array of floats
    """
    m = stypes.toDoubleMatrix(m)
    mout = stypes.emptyDoubleMatrix(x=3, y=3)
    libspice.xpose_c(m, mout)
    return stypes.matrixToList(mout)


@spiceErrorCheck
def xpose6(m):
    """
    Transpose a 6x6 matrix

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/xpose6_c.html

    :param m: Matrix to be transposed 
    :type m: list[6][6]
    :return: Transposed matrix
    :rtype: list[6][6]
    """
    m = stypes.toDoubleMatrix(m)
    mout = stypes.emptyDoubleMatrix(x=6, y=6)
    libspice.xpose6_c(m, mout)
    return stypes.matrixToList(mout)


@spiceErrorCheck
def xposeg(matrix, nrow, ncol):
    """
    Transpose a matrix of arbitrary size
    in place, the matrix need not be square.

    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/xposeg_c.html

    :param matrix: Matrix to be transposed 
    :type matrix: NxM-Element Array of floats
    :param nrow: Number of rows of input matrix.
    :type nrow: int
    :param ncol: Number of columns of input matrix
    :type ncol: int
    :return: Transposed matrix
    :rtype: NxM-Element Array of floats
    """
    matrix = stypes.listtodoublematrix(matrix, x=ncol, y=nrow)
    mout = stypes.emptyDoubleMatrix(x=ncol, y=nrow)
    ncol = ctypes.c_int(ncol)
    nrow = ctypes.c_int(nrow)
    libspice.xposeg_c(matrix, nrow, ncol, mout)
    return stypes.matrixToList(mout)
