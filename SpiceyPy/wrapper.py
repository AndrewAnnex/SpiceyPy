__author__ = 'AndrewAnnex'
# wrapper.py, a weak wrapper for libspice.py, here is where all the important ctypes setup and returning occurs.

import ctypes
import SpiceyPy.support_types as stypes
from SpiceyPy.libspice import libspice
import numpy

########################################################################################################################
# A


def appndc(item, cell):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/appndc_c.html

    :param item: The item to append.
    :type item: str
    :param cell: The cell to append to.
    :type cell: SpiceCell
    """
    assert isinstance(cell, stypes.SpiceCell)
    if isinstance(item, list):
        for c in item:
            libspice.appndc_c(stypes.stringToCharP(c), cell)
    else:
        item = stypes.stringToCharP(item)
        libspice.appndc_c(item, cell)
    pass


def appndd(item, cell):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/appndd_c.html

    :param item: The item to append.
    :type item: float
    :param cell: The cell to append to.
    :type cell: SpiceCell
    """
    assert isinstance(cell, stypes.SpiceCell)
    if hasattr(item, "__iter__"):
        for d in item:
            libspice.appndd_c(ctypes.c_double(d), cell)
    else:
        item = ctypes.c_double(item)
        libspice.appndd_c(item, cell)
    pass


def appndi(item, cell):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/appndi_c.html

    :param item: The item to append.
    :type item: int
    :param cell: The cell to append to.
    :type cell: SpiceCell
    """
    assert isinstance(cell, stypes.SpiceCell)
    if hasattr(item, "__iter__"):
        for i in item:
            libspice.appndi_c(ctypes.c_int(i), cell)
    else:
        item = ctypes.c_int(item)
        libspice.appndi_c(item, cell)
    pass


def axisar(axis, angle):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/axisar_c.html

    :param axis: Rotation axis.
    :type axis: 3 Element vector (list, tuple, numpy array)
    :param angle: Rotation angle, in radians.
    :type angle: float
    :return: Rotation matrix corresponding to axis and angle.
    :rtype numpy array ((3, 3))
    """
    axis = stypes.toDoubleVector(axis)
    angle = ctypes.c_double(angle)
    r = stypes.emptyDoubleMatrix()
    libspice.axisar_c(axis, angle, r)
    return stypes.matrixToList(r)


########################################################################################################################
# B


def b1900():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/b1900_c.html

    :return: The Julian Date corresponding to Besselian Date 1900.0. :rtype : float
    """
    return libspice.b1900_c()


def b1950():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/b1950_c.html

    :return: The Julian Date corresponding to Besselian Date 1950.0. :rtype : float
    """
    return libspice.b1950_c()


def badkpv(caller, name, comp, insize, divby, intype):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/badkpv_c.html

    :param caller: Name of the routine calling this routine.
    :param name: Name of a kernel pool variable.
    :param comp: Comparison operator.
    :param insize: Expected size of the kernel pool variable.
    :param divby: A divisor of the size of the kernel pool variable.
    :param intype: Expected type of the kernel pool variable
    :return: returns false if the kernel pool variable is OK. :rtype: bool
    """
    caller = stypes.stringToCharP(caller)
    name = stypes.stringToCharP(name)
    comp = stypes.stringToCharP(comp)
    insize = ctypes.c_int(insize)
    divby = ctypes.c_int(divby)
    intype = ctypes.c_char(intype.encode(encoding='UTF-8'))
    return libspice.badkpv_c(caller, name, comp, insize, divby, intype)


def bltfrm(frmcls, outSize=126):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bltfrm_c.html

    :param frmcls: Frame class.
    :param outSize: Optional size for return cell.
    :return: Set (SpiceCell) of ID codes of frames of the specified class. :rtype : SpiceINTCell
    """
    frmcls = ctypes.c_int(frmcls)
    outcell = stypes.SPICEINT_CELL(outSize)
    libspice.bltfrm_c(frmcls, outcell)
    return outcell


def bodc2n(code, lenout):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodc2n_c.html


    :param code: Integer ID code to be translated into a name.
    :param lenout: Maximum length of output name.
    :return: If found: A common name for the body identified by code. Else: None
    """
    code = ctypes.c_int(code)
    name = stypes.stringToCharP(" " * lenout)
    lenout = ctypes.c_int(lenout)
    found = ctypes.c_bool()
    libspice.bodc2n_c(code, lenout, name, ctypes.byref(found))
    if found.value:
        return stypes.toPythonString(name)
    else:
        return None


def bodc2s(code, lenout):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodc2s_c.html


    :param code: Integer ID code to translate to a string.
    :param lenout: Maximum length of output name.
    :return: String corresponding to 'code'. :rtype: str
    """
    code = ctypes.c_int(code)
    name = stypes.stringToCharP(" " * lenout)
    lenout = ctypes.c_int(lenout)
    libspice.bodc2s_c(code, lenout, name)
    return stypes.toPythonString(name)


def boddef(name, code):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/boddef_c.html


    :param name: Common name of some body.
    :param code: Integer code for that body.
    """
    name = stypes.stringToCharP(name)
    code = ctypes.c_int(code)
    libspice.boddef_c(name, code)
    pass


def bodfnd(body, item):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodfnd_c.html

    :param body: ID code of body.
    :param item: Item to find ("RADII", "NUT_AMP_RA", etc.).
    :return: :rtype: bool
    """
    body = ctypes.c_int(body)
    item = stypes.stringToCharP(item)
    return libspice.bodfnd_c(body, item)


def bodn2c(name):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodn2c_c.html

    :param name: Body name to be translated into a SPICE ID code.
    :return: SPICE integer ID code for the named body. :rtype: int
    """
    name = stypes.stringToCharP(name)
    code = ctypes.c_int(0)
    found = ctypes.c_bool(0)
    libspice.bodn2c_c(name, ctypes.byref(code), ctypes.byref(found))
    if found.value:
        return code.value
    else:
        return None


def bods2c(name):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bods2c_c.html

    :param name: String to be translated to an ID code.
    :return: Integer ID code corresponding to `name'. :rtype: int
    """
    name = stypes.stringToCharP(name)
    code = ctypes.c_int(0)
    found = ctypes.c_bool(0)
    libspice.bods2c_c(name, ctypes.byref(code), ctypes.byref(found))
    if found.value:
        return code.value
    else:
        return None


def bodvar(body, item, dim):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodvar_c.html

    :param body: ID code of body.
    :param item: Item for which values are desired. ("RADII", "NUT_PREC_ANGLES", etc. )
    :param dim: Number of values returned.
    :return: values :rtype: numpy array
    """
    body = ctypes.c_int(body)
    dim = ctypes.c_int(dim)
    item = stypes.stringToCharP(item)
    values = stypes.emptyDoubleVector(dim.value)
    libspice.bodvar_c(body, item, ctypes.byref(dim), values)
    return stypes.vectorToList(values)


def bodvcd(bodyid, item, maxn):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodvcd_c.html

    :param bodyid: Body ID code.
    :param item: Item for which values are desired. ("RADII", "NUT_PREC_ANGLES", etc. )
    :param maxn: Maximum number of values that may be returned.
    :return: tuple of (dim, values) :rtype: tuple
    """
    bodyid = ctypes.c_int(bodyid)
    item = stypes.stringToCharP(item)
    dim = ctypes.c_int()
    values = stypes.emptyDoubleVector(maxn)
    maxn = ctypes.c_int(maxn)
    libspice.bodvcd_c(bodyid, item, maxn, ctypes.byref(dim), values)
    return dim.value, stypes.vectorToList(values)


def bodvrd(bodynm, item, maxn):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bodvrd_c.html

    :param bodynm: Body name.
    :param item: Item for which values are desired. ("RADII", "NUT_PREC_ANGLES", etc. )
    :param maxn: Maximum number of values that may be returned.
    :return: tuple of (dim, values) :rtype: tuple
    """
    bodynm = stypes.stringToCharP(bodynm)
    item = stypes.stringToCharP(item)
    dim = ctypes.c_int()
    values = stypes.emptyDoubleVector(maxn)
    maxn = ctypes.c_int(maxn)
    libspice.bodvrd_c(bodynm, item, maxn, ctypes.byref(dim), values)
    return dim.value, stypes.vectorToList(values)


def brcktd(number, end1, end2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/brcktd_c.html

    :param number: Number to be bracketed.
    :param end1: One of the bracketing endpoints for number.
    :param end2: The other bracketing endpoint for number.
    :return: value within an interval :rtype: float
    """
    number = ctypes.c_double(number)
    end1 = ctypes.c_double(end1)
    end2 = ctypes.c_double(end2)
    return libspice.brcktd_c(number, end1, end2)


def brckti(number, end1, end2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/brckti_c.html

    :param number: Number to be bracketed.
    :param end1: One of the bracketing endpoints for number.
    :param end2: The other bracketing endpoint for number.
    :return: value within an interval :rtype: int
    """
    number = ctypes.c_int(number)
    end1 = ctypes.c_int(end1)
    end2 = ctypes.c_int(end2)
    return libspice.brckti_c(number, end1, end2)


def bschoc(value, ndim, lenvals, array, order):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bschoc_c.html

    :param value: Key value to be found in array.
    :param ndim: Dimension of array.
    :param lenvals: String length.
    :param array: Character string array to search.
    :param order: Order vector.
    :return: index :rtype: int
    """
    value = stypes.stringToCharP(value)
    ndim = ctypes.c_int(ndim)
    lenvals = ctypes.c_int(lenvals)
    array = stypes.listToCharArrayPtr(array, xLen=lenvals, yLen=ndim)
    order = stypes.toIntVector(order)
    return libspice.bschoc_c(value, ndim, lenvals, array, order)


def bschoi(value, ndim, array, order):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bschoi_c.html

    :param value: Key value to be found in array.
    :param ndim: Dimension of array.
    :param array: Integer array to search.
    :param order: Order vector.
    :return: index :rtype: int
    """
    value = ctypes.c_int(value)
    ndim = ctypes.c_int(ndim)
    array = stypes.toIntVector(array)
    order = stypes.toIntVector(order)
    return libspice.bschoi_c(value, ndim, array, order)


def bsrchc(value, ndim, lenvals, array):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bsrchc_c.html

    :param value: Key value to be found in array.
    :param ndim: Dimension of array.
    :param lenvals: String length.
    :param array: Character string array to search.
    :return: index :rtype: int
    """
    value = stypes.stringToCharP(value)
    ndim = ctypes.c_int(ndim)
    lenvals = ctypes.c_int(lenvals)
    array = stypes.listToCharArrayPtr(array, xLen=lenvals, yLen=ndim)
    return libspice.bsrchc_c(value, ndim, lenvals, array)


def bsrchd(value, ndim, array):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bsrchd_c.html

    :param value: Value to find in array.
    :param ndim: Dimension of array.
    :param array: Array to be searched.
    :return: index :rtype: int
    """
    value = ctypes.c_double(value)
    ndim = ctypes.c_int(ndim)
    array = stypes.toDoubleVector(array)
    return libspice.bsrchd_c(value, ndim, array)


def bsrchi(value, ndim, array):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/bsrchi_c.html

    :param value: Value to find in array.
    :param ndim: Dimension of array.
    :param array: Array to be searched.
    :return: index :rtype: int
    """
    value = ctypes.c_int(value)
    ndim = ctypes.c_int(ndim)
    array = stypes.toIntVector(array)
    return libspice.bsrchi_c(value, ndim, array)


########################################################################################################################
# C

def card(cell):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/card_c.html

    :param cell:
    :return: :rtype:
    """
    return libspice.card_c(ctypes.byref(cell))


def ccifrm(frclss, clssid, lenout):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ccifrm_c.html


    :param frclss:
    :param clssid:
    :param lenout:
    :return: :rtype:
    """
    frclss = ctypes.c_int(frclss)
    clssid = ctypes.c_int(clssid)
    lenout = ctypes.c_int(lenout)
    frcode = ctypes.c_int()
    frname = stypes.stringToCharP(lenout)
    center = ctypes.c_int()
    found = ctypes.c_bool()
    libspice.ccifrm_c(frclss, clssid, lenout, ctypes.byref(frcode), frname, ctypes.byref(center), ctypes.byref(found))
    if found.value:
        return frcode.value, stypes.toPythonString(frname), center.value,
    else:
        return None


def cgv2el(center, vec1, vec2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cgv2el_c.html


    :param center:
    :param vec1:
    :param vec2:
    :return: :rtype:
    """
    center = stypes.toDoubleVector(center)
    vec1 = stypes.toDoubleVector(vec1)
    vec2 = stypes.toDoubleVector(vec2)
    ellipse = stypes.Ellipse()
    libspice.cgv2el_c(center, vec1, vec2, ctypes.byref(ellipse))
    return ellipse


def chkin(module):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/chkin_c.html


    :param module:
    """
    module = stypes.stringToCharP(module)
    libspice.chkin_c(module)
    pass


def chkout(module):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/chkout_c.html


    :param module:
    """
    module = stypes.stringToCharP(module)
    libspice.chkout_c(module)
    pass


def cidfrm(cent, lenout):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cidfrm_c.html


    :param cent:
    :param lenout:
    :return: :rtype:
    """
    cent = ctypes.c_int(cent)
    lenout = ctypes.c_int(lenout)
    frcode = ctypes.c_int()
    frname = stypes.stringToCharP(lenout)
    found = ctypes.c_bool()
    libspice.cidfrm_c(cent, lenout, ctypes.byref(frcode), frname, ctypes.byref(found))
    if found.value:
        return frcode.value, stypes.toPythonString(frname)
    else:
        return None


def ckcls(handle):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckcls_c.html


    :param handle:
    """
    handle = ctypes.c_int(handle)
    libspice.ckcls_c(handle)
    pass


def ckcov(ck, idcode, needav, level, tol, timsys, cover=None):
    #Todo: test ckcov
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckcov_c.html

    :param ck:
    :param idcode:
    :param needav:
    :param level:
    :param tol:
    :param timsys:
    :param cover:
    :return: :rtype:
    """
    ck = stypes.stringToCharP(ck)
    idcode = ctypes.c_int(idcode)
    needav = ctypes.c_bool(needav)
    level = stypes.stringToCharP(level)
    tol = ctypes.c_double(tol)
    timsys = stypes.stringToCharP(timsys)
    if not cover:
        cover = stypes.SPICEDOUBLE_CELL(2000)
    assert isinstance(cover, stypes.SpiceCell)
    assert cover.dtype == 1
    libspice.ckcov_c(ck, idcode, needav, level, tol, timsys, ctypes.byref(cover))
    return cover


def ckgp(inst, sclkdp, tol, ref):
    #Todo: test ckgp
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckgp_c.html

    :param inst:
    :param sclkdp:
    :param tol:
    :param ref:
    :return: :rtype:
    """
    inst = ctypes.c_int(inst)
    sclkdp = ctypes.c_double(sclkdp)
    tol = ctypes.c_double(tol)
    ref = stypes.stringToCharP(ref)
    cmat = stypes.emptyDoubleMatrix()
    clkout = ctypes.c_double()
    found = ctypes.c_bool()
    libspice.ckgp_c(inst, sclkdp, tol, ref, cmat, ctypes.byref(clkout), ctypes.byref(found))
    return stypes.matrixToList(cmat), clkout.value, found.value


def ckgpav(inst, sclkdp, tol, ref):
    #Todo: test ckgpav
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckgpav_c.html

    :param inst:
    :param sclkdp:
    :param tol:
    :param ref:
    :return: :rtype:
    """
    inst = ctypes.c_int(inst)
    sclkdp = ctypes.c_double(sclkdp)
    tol = ctypes.c_double(tol)
    ref = stypes.stringToCharP(ref)
    cmat = stypes.emptyDoubleMatrix()
    av = stypes.emptyDoubleVector(3)
    clkout = ctypes.c_double()
    found = ctypes.c_bool()
    libspice.ckgpav_c(inst, sclkdp, tol, ref, cmat, av, ctypes.byref(clkout), ctypes.byref(found))
    return stypes.matrixToList(cmat), stypes.vectorToList(av), clkout.value, found.value


def cklpf(filename):
    #Todo: test cklpf
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cklpf_c.html

    :param filename:
    :return: :rtype:
    """
    filename = stypes.stringToCharP(filename)
    handle = ctypes.c_int()
    libspice.cklpf_c(filename, ctypes.byref(handle))
    return handle.value


def ckobj(ck, ids):
    #Todo: test ckobj
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckobj_c.html

    :param ck:
    :param ids:
    :return: :rtype:
    """
    assert isinstance(ck, str)
    ck = stypes.stringToCharP(ck)
    if not ids:
        ids = stypes.SPICEINT_CELL(1000)
    assert isinstance(ids, stypes.SpiceCell)
    assert ids.dtype == 2
    libspice.ckobj_c(ck, ctypes.byref(ids))
    return ids


def ckopn(filename, ifname, ncomch):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckopn_c.html


    :param filename:
    :param ifname:
    :param ncomch:
    :return: :rtype:
    """
    filename = stypes.stringToCharP(filename)
    ifname = stypes.stringToCharP(ifname)
    ncomch = ctypes.c_int(ncomch)
    handle = ctypes.c_int()
    libspice.ckopn_c(filename, ifname, ncomch, ctypes.byref(handle))
    return handle.value


def ckupf(handle):
    #Todo: test ckupf
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckupf_c.html

    :param handle:
    """
    handle = ctypes.c_int(handle)
    libspice.ckupf_c(handle)
    pass


def ckw01(handle, begtim, endtim, inst, ref, avflag, segid, nrec, sclkdp, quats, avvs):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckw01_c.html


    :param handle:
    :param begtim:
    :param endtim:
    :param inst:
    :param ref:
    :param avflag:
    :param segid:
    :param nrec:
    :param sclkdp:
    :param quats:
    :param avvs:
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
    libspice.ckw01_c(handle, begtim, endtim, inst, ref, avflag, segid, nrec, sclkdp, quats, avvs)
    pass


def ckw02(handle, begtim, endtim, inst, ref, segid, nrec, start, stop, quats, avvs, rates):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckw02_c.html


    :param handle:
    :param begtim:
    :param endtim:
    :param inst:
    :param ref:
    :param segid:
    :param nrec:
    :param start:
    :param stop:
    :param quats:
    :param avvs:
    :param rates:
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
    libspice.ckw02_c(handle, begtim, endtim, inst, ref, segid, nrec, start, stop, quats, avvs, rates)
    pass


def ckw03(handle, begtim, endtim, inst, ref, avflag, segid, nrec, sclkdp, quats, avvs, nints, starts):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/ckw03_c.html


    :param handle:
    :param begtim:
    :param endtim:
    :param inst:
    :param ref:
    :param avflag:
    :param segid:
    :param nrec:
    :param sclkdp:
    :param quats:
    :param avvs:
    :param nints:
    :param starts:
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
    libspice.ckw03_c(handle, begtim, endtim, inst, ref, avflag, segid, nrec, sclkdp, quats, avvs, nints, starts)
    pass


# ckw05, skipping, ck05subtype?


def clight():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/clight_c.html



    :return: :rtype:
    """
    return libspice.clight_c()


def clpool():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/clpool_c.html



    """
    libspice.clpool_c()
    pass


def cmprss(delim, n, instr, lenout=None):
    # automatically determine lenout (cannot be more than instr)
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cmprss_c.html

    :param delim:
    :param n:
    :param instr:
    :param lenout:
    :return: :rtype:
    """
    if lenout is None:
        lenout = ctypes.c_int(len(instr) + 1)
    delim = ctypes.c_char(delim.encode(encoding='UTF-8'))
    n = ctypes.c_int(n)
    instr = stypes.stringToCharP(instr)
    output = stypes.stringToCharP(lenout)
    libspice.cmprss_c(delim, n, instr, lenout, output)
    return stypes.toPythonString(output)


def cnmfrm(cname, lenout):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cnmfrm_c.html


    :param cname:
    :param lenout:
    :return: :rtype:
    """
    lenout = ctypes.c_int(lenout)
    frname = stypes.stringToCharP(lenout)
    cname = stypes.stringToCharP(cname)
    found = ctypes.c_bool()
    frcode = ctypes.c_int()
    libspice.cnmfrm_c(cname, lenout, ctypes.byref(frcode), frname, ctypes.byref(found))
    if found.value:
        return frcode.value, stypes.toPythonString(frname)
    else:
        return None


def conics(elts, et):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/conics_c.html


    :param elts:
    :param et:
    :return: :rtype:
    """
    elts = stypes.toDoubleVector(elts)
    et = ctypes.c_double(et)
    state = stypes.emptyDoubleVector(6)
    libspice.conics_c(elts, et, state)
    return stypes.vectorToList(state)


def convrt(x, inunit, outunit):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/convrt_c.html


    :param x:
    :param inunit:
    :param outunit:
    :return: :rtype:
    """
    x = ctypes.c_double(x)
    inunit = stypes.stringToCharP(inunit)
    outunit = stypes.stringToCharP(outunit)
    y = ctypes.c_double()
    libspice.convrt_c(x, inunit, outunit, ctypes.byref(y))
    return y.value


def copy(cell):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/copy_c.html


    :param cell:
    :return: :rtype: :raise NotImplementedError:
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


def cpos(string, chars, start):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cpos_c.html


    :param string:
    :param chars:
    :param start:
    :return: :rtype:
    """
    string = stypes.stringToCharP(string)
    chars = stypes.stringToCharP(chars)
    start = ctypes.c_int(start)
    return libspice.cpos_c(string, chars, start)


def cposr(string, chars, start):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cposr_c.html


    :param string:
    :param chars:
    :param start:
    :return: :rtype:
    """
    string = stypes.stringToCharP(string)
    chars = stypes.stringToCharP(chars)
    start = ctypes.c_int(start)
    return libspice.cposr_c(string, chars, start)


def cvpool(agent):
    #Todo: test cvpool
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cvpool_c.html

    :param agent:
    :return: :rtype:
    """
    agent = stypes.stringToCharP(agent)
    update = ctypes.c_bool()
    libspice.cvpool_c(agent, ctypes.byref(update))
    return update.value


def cyllat(r, lonc, z):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cyllat_c.html


    :param r:
    :param lonc:
    :param z:
    :return: :rtype:
    """
    r = ctypes.c_double(r)
    lonc = ctypes.c_double(lonc)
    z = ctypes.c_double(z)
    radius = ctypes.c_double()
    lon = ctypes.c_double()
    lat = ctypes.c_double()
    libspice.cyllat_c(r, lonc, z, ctypes.byref(radius), ctypes.byref(lon), ctypes.byref(lat))
    return radius.value, lon.value, lat.value


def cylrec(r, lon, z):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cylrec_c.html


    :param r:
    :param lon:
    :param z:
    :return: :rtype:
    """
    r = ctypes.c_double(r)
    lon = ctypes.c_double(lon)
    z = ctypes.c_double(z)
    rectan = stypes.emptyDoubleVector(3)
    libspice.cylrec_c(r, lon, z, rectan)
    return stypes.vectorToList(rectan)


def cylsph(r, lonc, z):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/cylsph_c.html


    :param r:
    :param lonc:
    :param z:
    :return: :rtype:
    """
    r = ctypes.c_double(r)
    lonc = ctypes.c_double(lonc)
    z = ctypes.c_double(z)
    radius = ctypes.c_double()
    colat = ctypes.c_double()
    lon = ctypes.c_double()
    libspice.cyllat_c(r, lonc, z, ctypes.byref(radius), ctypes.byref(colat), ctypes.byref(lon))
    return radius.value, colat.value, lon.value


########################################################################################################################
# D

def dafac(handle, n, lenvals, buffer):
    #Todo: test dafac
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param handle:
    :param n:
    :param lenvals:
    :param buffer:
    """
    handle = ctypes.c_int(handle)
    buffer = stypes.listToCharArrayPtr(buffer)
    n = ctypes.c_int(n)
    lenvals = ctypes.c_int(lenvals)
    libspice.dafac_c(handle, n, lenvals, ctypes.byref(buffer))
    pass


def dafbbs(handle):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    """
    handle = ctypes.c_int(handle)
    libspice.dafbbs_c(handle)
    pass


def dafbfs(handle):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    """
    handle = ctypes.c_int(handle)
    libspice.dafbfs_c(handle)
    pass


def dafcls(handle):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    """
    handle = ctypes.c_int(handle)
    libspice.dafcls_c(handle)
    pass


def dafcs(handle):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    """
    handle = ctypes.c_int(handle)
    libspice.dafcs_c(handle)
    pass


def dafdc(handle):
    #Todo: test dafdc
    """

    :param handle:
    """
    handle = ctypes.c_int(handle)
    libspice.dafcc_c(handle)
    pass


def dafec(handle, bufsiz, lenout):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    :param bufsiz:
    :param lenout:
    :return: :rtype:
    """
    handle = ctypes.c_int(handle)
    buffer = stypes.charvector(bufsiz, lenout)
    bufsiz = ctypes.c_int(bufsiz)
    lenout = ctypes.c_int(lenout)
    n = ctypes.c_int()
    done = ctypes.c_bool()
    libspice.dafec_c(handle, bufsiz, lenout, ctypes.byref(n), ctypes.byref(buffer), ctypes.byref(done))
    return n.value, stypes.vectorToList(buffer), done.value


def daffna():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    :return: :rtype:
    """
    found = ctypes.c_bool()
    libspice.daffna_c(ctypes.byref(found))
    return found.value


def daffpa():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    :return: :rtype:
    """
    found = ctypes.c_bool()
    libspice.daffpa_c(ctypes.byref(found))
    return found.value


def dafgda(handle, begin, end):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    :param begin:
    :param end:
    :return: :rtype:
    """
    handle = ctypes.c_int(handle)
    data = stypes.emptyDoubleVector(abs(end - begin))
    begin = ctypes.c_int(begin)
    end = ctypes.c_int(end)
    libspice.dafgda_c(handle, begin, end, data)
    return stypes.vectorToList(data)


def dafgh():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    :return: :rtype:
    """
    outvalue = ctypes.c_int()
    libspice.dafgh_c(ctypes.byref(outvalue))
    return outvalue.value


def dafgn(lenout):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param lenout:
    :return: :rtype:
    """
    lenout = ctypes.c_int(lenout)
    name = stypes.stringToCharP(lenout)
    libspice.dafgn_c(lenout, name)
    return stypes.toPythonString(name)


def dafgs(n=125):
    # The 125 may be a hard set, I got strange errors that occasionally happend without it
    """

    :param n:
    :return: :rtype:
    """
    retarray = stypes.emptyDoubleVector(125)
    # libspice.dafgs_c(ctypes.cast(retarray, ctypes.POINTER(ctypes.c_double)))
    libspice.dafgs_c(retarray)
    return stypes.vectorToList(retarray)[0:n]


def dafgsr(handle, recno, begin, end):
    #Todo test dafgsr
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param handle:
    :param recno:
    :param begin:
    :param end:
    :return: :rtype:
    """
    handle = ctypes.c_int(handle)
    recno = ctypes.c_int(recno)
    begin = ctypes.c_int(begin)
    end = ctypes.c_int(end)
    data = ctypes.c_double()
    found = ctypes.c_bool()
    libspice.dafgsr_c(handle, recno, begin, end, ctypes.byref(data), ctypes.byref(found))
    return data.value, found.value


def dafopr(fname):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param fname:
    :return: :rtype:
    """
    fname = stypes.stringToCharP(fname)
    handle = ctypes.c_int()
    libspice.dafopr_c(fname, ctypes.byref(handle))
    return handle.value


def dafopw(fname):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param fname:
    :return: :rtype:
    """
    fname = stypes.stringToCharP(fname)
    handle = ctypes.c_int()
    libspice.dafopw_c(fname, ctypes.byref(handle))
    return handle.value


def dafps(nd, ni, dc, ic):
    #Todo: test dafps
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param nd:
    :param ni:
    :param dc:
    :param ic:
    :return: :rtype:
    """
    dc = stypes.toDoubleVector(dc)
    ic = stypes.toIntVector(ic)
    outsum = stypes.emptyDoubleVector(nd + ni)
    nd = ctypes.c_int(nd)
    ni = ctypes.c_int(ni)
    libspice.dafps_c(nd, ni, ctypes.byref(dc), ctypes.byref(ic), ctypes.byref(outsum))
    return stypes.vectorToList(outsum)


def dafrda(handle, begin, end):
    #Todo: test dafrda
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param handle:
    :param begin:
    :param end:
    :return: :rtype:
    """
    handle = ctypes.c_int(handle)
    begin = ctypes.c_int(begin)
    end = ctypes.c_int(end)
    data = stypes.emptyDoubleVector(8)  # value of 8 from help file
    libspice.dafrda_c(handle, begin, end, ctypes.byref(data))
    return stypes.vectorToList(data)


def dafrfr(handle, lenout):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    :param lenout:
    :return: :rtype:
    """
    handle = ctypes.c_int(handle)
    lenout = ctypes.c_int(lenout)
    nd = ctypes.c_int()
    ni = ctypes.c_int()
    ifname = stypes.stringToCharP(lenout)
    fward = ctypes.c_int()
    bward = ctypes.c_int()
    free = ctypes.c_int()
    libspice.dafrfr_c(handle, lenout, ctypes.byref(nd), ctypes.byref(ni), ifname, ctypes.byref(fward), ctypes.byref(bward), ctypes.byref(free))
    return nd.value, ni.value, stypes.toPythonString(ifname), fward.value, bward.value, free.value


def dafrs(insum):
    #Todo: test dafrs
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param insum:
    """
    insum = stypes.toDoubleVector(insum)
    libspice.dafrs_c(ctypes.byref(insum))
    pass


def dafus(insum, nd, ni):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param insum:
    :param nd:
    :param ni:
    :return: :rtype:
    """
    insum = stypes.toDoubleVector(insum)
    dc = stypes.emptyDoubleVector(nd)
    ic = stypes.emptyIntVector(ni)
    nd = ctypes.c_int(nd)
    ni = ctypes.c_int(ni)
    libspice.dafus_c(insum, nd, ni, dc, ic)
    return stypes.vectorToList(dc), stypes.vectorToList(ic)


def dasac(handle, n, buflen, buffer):
    #Todo: test dasac
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param handle:
    :param n:
    :param buflen:
    :param buffer:
    :return: :rtype:
    """
    handle = ctypes.c_int(handle)
    buffer = stypes.charvector(n, buflen)
    n = ctypes.c_int(n)
    buflen = ctypes.c_int(buflen)
    libspice.dasac_c(handle, n, buflen, ctypes.byref(buffer))
    return stypes.vectorToList(buffer)


def dascls(handle):
    #Todo: test dafdc
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param handle:
    """
    handle = ctypes.c_int(handle)
    libspice.dascls_c(handle)
    pass


def dasec(handle, bufsiz, buflen):
    #Todo: test dasec
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param handle:
    :param bufsiz:
    :param buflen:
    :return: :rtype:
    """
    handle = ctypes.c_int(handle)
    buffer = stypes.charvector(bufsiz, buflen)
    bufsiz = ctypes.c_int(bufsiz)
    buflen = ctypes.c_int(buflen)
    n = ctypes.c_int()
    done = ctypes.c_bool()
    libspice.dafec_c(handle, bufsiz, buflen, ctypes.byref(n), ctypes.byref(buffer), ctypes.byref(done))
    return n.value, stypes.vectorToList(buffer), done.value


def dasopr(fname):
    #Todo: test dasopr
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param fname:
    """
    fname = stypes.stringToCharP(fname)
    handle = ctypes.c_int()
    libspice.dasopr_c(fname, ctypes.byref(handle))


def dcyldr(x, y, z):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param x:
    :param y:
    :param z:
    :return: :rtype:
    """
    x = ctypes.c_double(x)
    y = ctypes.c_double(y)
    z = ctypes.c_double(z)
    jacobi = stypes.emptyDoubleMatrix()
    libspice.dcyldr_c(x, y, z, jacobi)
    return stypes.matrixToList(jacobi)


def deltet(epoch, eptype):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param epoch:
    :param eptype:
    :return: :rtype:
    """
    epoch = ctypes.c_double(epoch)
    eptype = stypes.stringToCharP(eptype)
    delta = ctypes.c_double()
    libspice.deltet_c(epoch, eptype, ctypes.byref(delta))
    return delta.value


def det(m1):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param m1:
    :return: :rtype:
    """
    m1 = stypes.listtodoublematrix(m1)
    return libspice.det_c(m1)


def dgeodr(x, y, z, re, f):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param x:
    :param y:
    :param z:
    :param re:
    :param f:
    :return: :rtype:
    """
    x = ctypes.c_double(x)
    y = ctypes.c_double(y)
    z = ctypes.c_double(z)
    re = ctypes.c_double(re)
    f = ctypes.c_double(f)
    jacobi = stypes.emptyDoubleMatrix()
    libspice.dgeodr_c(x, y, z, re, f, jacobi)
    return stypes.matrixToList(jacobi)


def diags2(symmat):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param symmat:
    :return: :rtype:
    """
    symmat = stypes.listtodoublematrix(symmat, x=2, y=2)
    diag = stypes.emptyDoubleMatrix(x=2, y=2)
    rotateout = stypes.emptyDoubleMatrix(x=2, y=2)
    libspice.diags2_c(symmat, diag, rotateout)
    return stypes.matrixToList(diag), stypes.matrixToList(rotateout)


def diff(a, b):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param a:
    :param b:
    :return: :rtype: :raise NotImplementedError:
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


def dlatdr(x, y, z):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param x:
    :param y:
    :param z:
    :return: :rtype:
    """
    x = ctypes.c_double(x)
    y = ctypes.c_double(y)
    z = ctypes.c_double(z)
    jacobi = stypes.emptyDoubleMatrix()
    libspice.dlatdr_c(x, y, z, jacobi)
    return stypes.matrixToList(jacobi)


def dp2hx(number, lenout=None):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param number:
    :param lenout:
    :return: :rtype:
    """
    if lenout is None:
        lenout = 255
    number = ctypes.c_double(number)
    lenout = ctypes.c_int(lenout)
    string = stypes.stringToCharP(lenout)
    length = ctypes.c_int()
    libspice.dp2hx_c(number, lenout, string, ctypes.byref(length))
    return stypes.toPythonString(string)


def dpgrdr(body, x, y, z, re, f):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param body:
    :param x:
    :param y:
    :param z:
    :param re:
    :param f:
    :return: :rtype:
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


def dpmax():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    :return: :rtype:
    """
    return libspice.dpmax_c()


def dpmin():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    :return: :rtype:
    """
    return libspice.dpmin_c()


def dpr():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    :return: :rtype:
    """
    return libspice.dpr_c()


def drdcyl(r, lon, z):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param r:
    :param lon:
    :param z:
    :return: :rtype:
    """
    r = ctypes.c_double(r)
    lon = ctypes.c_double(lon)
    z = ctypes.c_double(z)
    jacobi = stypes.emptyDoubleMatrix()
    libspice.drdcyl_c(r, lon, z, jacobi)
    return stypes.matrixToList(jacobi)


def drdgeo(lon, lat, alt, re, f):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param lon:
    :param lat:
    :param alt:
    :param re:
    :param f:
    :return: :rtype:
    """
    lon = ctypes.c_double(lon)
    lat = ctypes.c_double(lat)
    alt = ctypes.c_double(alt)
    re = ctypes.c_double(re)
    f = ctypes.c_double(f)
    jacobi = stypes.emptyDoubleMatrix()
    libspice.drdgeo_c(lon, lat, alt, re, f, jacobi)
    return stypes.matrixToList(jacobi)


def drdlat(r, lon, lat):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param r:
    :param lon:
    :param lat:
    :return: :rtype:
    """
    r = ctypes.c_double(r)
    lon = ctypes.c_double(lon)
    lat = ctypes.c_double(lat)
    jacobi = stypes.emptyDoubleMatrix()
    libspice.drdsph_c(r, lon, lat, jacobi)
    return stypes.matrixToList(jacobi)


def drdpgr(body, lon, lat, alt, re, f):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param body:
    :param lon:
    :param lat:
    :param alt:
    :param re:
    :param f:
    :return: :rtype:
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


def drdsph(r, colat, lon):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param r:
    :param colat:
    :param lon:
    :return: :rtype:
    """
    r = ctypes.c_double(r)
    colat = ctypes.c_double(colat)
    lon = ctypes.c_double(lon)
    jacobi = stypes.emptyDoubleMatrix()
    libspice.drdsph_c(r, colat, lon, jacobi)
    return stypes.matrixToList(jacobi)


def dsphdr(x, y, z):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param x:
    :param y:
    :param z:
    :return: :rtype:
    """
    x = ctypes.c_double(x)
    y = ctypes.c_double(y)
    z = ctypes.c_double(z)
    jacobi = stypes.emptyDoubleMatrix()
    libspice.dsphdr_c(x, y, z, jacobi)
    return stypes.matrixToList(jacobi)


def dtpool(name):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param name:
    :return: :rtype:
    """
    name = stypes.stringToCharP(name)
    found = ctypes.c_bool()
    n = ctypes.c_int()
    typeout = ctypes.c_char()
    libspice.dtpool_c(name, ctypes.byref(found), ctypes.byref(n), ctypes.byref(typeout))
    return found.value, n.value, stypes.toPythonString(typeout.value)


def ducrss(s1, s2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param s1:
    :param s2:
    :return: :rtype:
    """
    assert len(s1) is 6 and len(s2) is 6
    s1 = stypes.toDoubleVector(s1)
    s2 = stypes.toDoubleVector(s2)
    sout = stypes.emptyDoubleVector(6)
    libspice.ducrss_c(s1, s2, sout)
    return stypes.vectorToList(sout)


def dvcrss(s1, s2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param s1:
    :param s2:
    :return: :rtype:
    """
    assert len(s1) is 6 and len(s2) is 6
    s1 = stypes.toDoubleVector(s1)
    s2 = stypes.toDoubleVector(s2)
    sout = stypes.emptyDoubleVector(6)
    libspice.dvcrss_c(s1, s2, sout)
    return stypes.vectorToList(sout)


def dvdot(s1, s2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param s1:
    :param s2:
    :return: :rtype:
    """
    assert len(s1) is 6 and len(s2) is 6
    s1 = stypes.toDoubleVector(s1)
    s2 = stypes.toDoubleVector(s2)
    return libspice.dvdot_c(s1, s2)


def dvhat(s1):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param s1:
    :return: :rtype:
    """
    assert len(s1) is 6
    s1 = stypes.toDoubleVector(s1)
    sout = stypes.emptyDoubleVector(6)
    libspice.dvhat_c(s1, sout)
    return stypes.vectorToList(sout)


def dvnorm(state):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param state:
    :return: :rtype:
    """
    assert len(state) is 6
    state = stypes.toDoubleVector(state)
    return libspice.dvnorm_c(state)


def dvpool(name):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param name:
    """
    name = stypes.stringToCharP(name)
    libspice.dvpool_c(name)
    pass


def dvsep(s1, s2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param s1:
    :param s2:
    :return: :rtype:
    """
    assert len(s1) is 6 and len(s2) is 6
    s1 = stypes.toDoubleVector(s1)
    s2 = stypes.toDoubleVector(s2)
    return libspice.dvsep_c(s1, s2)

########################################################################################################################
# E


def edlimb(a, b, c, viewpt):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param a:
    :param b:
    :param c:
    :param viewpt:
    :return: :rtype:
    """
    limb = stypes.Ellipse()
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    viewpt = stypes.toDoubleVector(viewpt)
    libspice.edlimb_c(a, b, c, viewpt, ctypes.byref(limb))
    return limb


def edterm(trmtyp, source, target, et, fixref, abcorr, obsrvr, npts):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param trmtyp:
    :param source:
    :param target:
    :param et:
    :param fixref:
    :param abcorr:
    :param obsrvr:
    :param npts:
    :return: :rtype:
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
    libspice.edterm_c(trmtyp, source, target, et, fixref, abcorr, obsrvr, npts, ctypes.byref(trgepc), obspos, trmpts)
    return trgepc.value, stypes.vectorToList(obspos), stypes.matrixToList(trmpts)


def ekacec(handle, segno, recno, column, nvals, vallen, cvals, isnull):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    :param segno:
    :param recno:
    :param column:
    :param nvals:
    :param vallen:
    :param cvals:
    :param isnull:
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.stringToCharP(column)
    nvals = ctypes.c_int(nvals)
    vallen = ctypes.c_int(vallen)
    cvals = stypes.listToCharArrayPtr(cvals)
    isnull = ctypes.c_bool(isnull)
    libspice.ekacec_c(handle, segno, recno, column, nvals, vallen, cvals, isnull)
    pass


def ekaced(handle, segno, recno, column, nvals, dvals, isnull):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    :param segno:
    :param recno:
    :param column:
    :param nvals:
    :param dvals:
    :param isnull:
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.stringToCharP(column)
    nvals = ctypes.c_int(nvals)
    dvals = stypes.toDoubleVector(dvals)
    isnull = ctypes.c_bool(isnull)
    libspice.ekaced_c(handle, segno, recno, column, nvals, dvals, isnull)
    pass


def ekacei(handle, segno, recno, column, nvals, ivals, isnull):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    :param segno:
    :param recno:
    :param column:
    :param nvals:
    :param ivals:
    :param isnull:
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.stringToCharP(column)
    nvals = ctypes.c_int(nvals)
    ivals = stypes.toIntVector(ivals)
    isnull = ctypes.c_bool(isnull)
    libspice.ekacei_c(handle, segno, recno, column, nvals, ivals, isnull)


def ekaclc(handle, segno, column, vallen, cvals, entszs, nlflgs, rcptrs, wkindx):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    :param segno:
    :param column:
    :param vallen:
    :param cvals:
    :param entszs:
    :param nlflgs:
    :param rcptrs:
    :param wkindx:
    :return: :rtype:
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
    libspice.ekaclc_c(handle, segno, column, vallen, cvals, entszs, nlflgs, rcptrs, wkindx)
    return stypes.vectorToList(wkindx)


def ekacld(handle, segno, column, dvals, entszs, nlflgs, rcptrs, wkindx):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    :param segno:
    :param column:
    :param dvals:
    :param entszs:
    :param nlflgs:
    :param rcptrs:
    :param wkindx:
    :return: :rtype:
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    column = stypes.stringToCharP(column)
    dvals = stypes.toDoubleVector(dvals)
    entszs = stypes.toIntVector(entszs)
    nlflgs = stypes.toBoolVector(nlflgs)
    rcptrs = stypes.toIntVector(rcptrs)
    wkindx = stypes.toIntVector(wkindx)
    libspice.ekacld_c(handle, segno, column, dvals, entszs, nlflgs, rcptrs, wkindx)
    return stypes.vectorToList(wkindx)


def ekacli(handle, segno, column, ivals, entszs, nlflgs, rcptrs, wkindx):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    :param segno:
    :param column:
    :param ivals:
    :param entszs:
    :param nlflgs:
    :param rcptrs:
    :param wkindx:
    :return: :rtype:
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    column = stypes.stringToCharP(column)
    ivals = stypes.toIntVector(ivals)
    entszs = stypes.toIntVector(entszs)
    nlflgs = stypes.toBoolVector(nlflgs)
    rcptrs = stypes.toIntVector(rcptrs)
    wkindx = stypes.toIntVector(wkindx)
    libspice.ekacli_c(handle, segno, column, ivals, entszs, nlflgs, rcptrs, wkindx)
    return stypes.vectorToList(wkindx)


def ekappr(handle, segno):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    :param segno:
    :return: :rtype:
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int()
    libspice.ekappr_c(handle, segno, ctypes.byref(recno))
    return recno.value


def ekbseg(handle, tabnam, ncols, cnmlen, cnames, declen, decls):
    # if 'cnmlen' in kwargs:
    # cnmlen = kwargs['cnmlen']
    # else:
    #     cnmlen = len(max(cnames, key=len)) + 1
    # if 'declen' in kwargs:
    #     declen = kwargs['declen']
    # else:
    #     declen = len(max(decls, key=len)) + 1
    # if 'ncols' in kwargs:
    #     ncols = kwargs['ncols']
    # else:
    #     ncols = len(cnames)
    """

    :param handle:
    :param tabnam:
    :param ncols:
    :param cnmlen:
    :param cnames:
    :param declen:
    :param decls:
    :return: :rtype:
    """
    handle = ctypes.c_int(handle)
    tabnam = stypes.stringToCharP(tabnam)
    cnmlen = ctypes.c_int(cnmlen)
    cnames = stypes.listToCharArray(cnames)  # not sure if this works
    declen = ctypes.c_int(declen)
    decls = stypes.listToCharArray(decls)
    segno = ctypes.c_int()
    libspice.ekbseg_c(handle, tabnam, ncols, cnmlen, cnames, declen, decls, ctypes.byref(segno))
    return segno.value


def ekccnt(table):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param table:
    :return: :rtype:
    """
    table = stypes.stringToCharP(table)
    ccount = ctypes.c_int()
    libspice.ekccnt_c(table, ctypes.byref(ccount))
    return ccount.value


def ekcii(table, cindex, lenout):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param table:
    :param cindex:
    :param lenout:
    :return: :rtype:
    """
    table = stypes.stringToCharP(table)
    cindex = ctypes.c_int(cindex)
    lenout = ctypes.c_int(lenout)
    column = stypes.stringToCharP(lenout)
    attdsc = stypes.SpiceEKAttDsc()
    libspice.ekcii_c(table, cindex, lenout, column, ctypes.byref(attdsc))
    return stypes.toPythonString(column), attdsc


def ekcls(handle):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    """
    handle = ctypes.c_int(handle)
    libspice.ekcls_c(handle)
    pass


def ekdelr(handle, segno, recno):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    :param segno:
    :param recno:
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    libspice.ekdelr_c(handle, segno, recno)
    pass


def ekffld(handle, segno, rcptrs):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    :param segno:
    :param rcptrs:
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    rcptrs = stypes.toIntVector(rcptrs)
    libspice.ekffld_c(handle, segno, ctypes.cast(rcptrs, ctypes.POINTER(ctypes.c_int)))
    pass


def ekfind(query, lenout):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param query:
    :param lenout:
    :return: :rtype:
    """
    query = stypes.stringToCharP(query)
    lenout = ctypes.c_int(lenout)
    nmrows = ctypes.c_int()
    error = ctypes.c_bool()
    errmsg = stypes.stringToCharP(lenout)
    libspice.ekfind_c(query, lenout, ctypes.byref(nmrows), ctypes.byref(error), errmsg)
    return nmrows.value, error.value, stypes.toPythonString(errmsg)


def ekgc(selidx, row, element, lenout):
    # ekgc has issues grabbing last element/row in column
    """

    :param selidx:
    :param row:
    :param element:
    :param lenout:
    :return: :rtype:
    """
    selidx = ctypes.c_int(selidx)
    row = ctypes.c_int(row)
    element = ctypes.c_int(element)
    lenout = ctypes.c_int(lenout)
    null = ctypes.c_bool()
    found = ctypes.c_bool()
    cdata = stypes.stringToCharP(lenout)
    libspice.ekgc_c(selidx, row, element, lenout, cdata, ctypes.byref(null), ctypes.byref(found))
    return stypes.toPythonString(cdata), null.value, found.value


def ekgd(selidx, row, element):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param selidx:
    :param row:
    :param element:
    :return: :rtype:
    """
    selidx = ctypes.c_int(selidx)
    row = ctypes.c_int(row)
    element = ctypes.c_int(element)
    ddata = ctypes.c_double()
    null = ctypes.c_bool()
    found = ctypes.c_bool()
    libspice.ekgd_c(selidx, row, element, ctypes.byref(ddata), ctypes.byref(null), ctypes.byref(found))
    return ddata.value, null.value, found.value


def ekgi(selidx, row, element):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param selidx:
    :param row:
    :param element:
    :return: :rtype:
    """
    selidx = ctypes.c_int(selidx)
    row = ctypes.c_int(row)
    element = ctypes.c_int(element)
    idata = ctypes.c_int()
    null = ctypes.c_bool()
    found = ctypes.c_bool()
    libspice.ekgi_c(selidx, row, element, ctypes.byref(idata), ctypes.byref(null), ctypes.byref(found))
    return idata.value, null.value, found.value


def ekifld(handle, tabnam, ncols, nrows, cnmlen, cnames, declen, decls):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    :param tabnam:
    :param ncols:
    :param nrows:
    :param cnmlen:
    :param cnames:
    :param declen:
    :param decls:
    :return: :rtype:
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
    libspice.ekifld_c(handle, tabnam, ncols, nrows, cnmlen, cnames, declen, decls, ctypes.byref(segno), recptrs)
    return segno.value, stypes.vectorToList(recptrs)


def ekinsr(handle, segno, recno):
    #Todo: test ekinsr
    """

    :param handle:
    :param segno:
    :param recno:
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    libspice.ekinsr_c(handle, segno, recno)
    pass


def eklef(fname):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param fname:
    :return: :rtype:
    """
    fname = stypes.stringToCharP(fname)
    handle = ctypes.c_int()
    libspice.eklef_c(fname, handle)
    return handle.value


def eknelt(selidx, row):
    #Todo: test eknelt
    """

    :param selidx:
    :param row:
    :return: :rtype:
    """
    selidx = ctypes.c_int(selidx)
    row = ctypes.c_int(row)
    return libspice.eknelt_c(selidx, row)


def eknseg(handle):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    :return: :rtype:
    """
    handle = ctypes.c_int(handle)
    return libspice.eknseg_c(handle)


def ekntab():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    :return: :rtype:
    """
    n = ctypes.c_int(0)
    libspice.ekntab_c(ctypes.byref(n))
    return n.value


def ekopn(fname, ifname, ncomch):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param fname:
    :param ifname:
    :param ncomch:
    :return: :rtype:
    """
    fname = stypes.stringToCharP(fname)
    ifname = stypes.stringToCharP(ifname)
    ncomch = ctypes.c_int(ncomch)
    handle = ctypes.c_int()
    libspice.ekopn_c(fname, ifname, ncomch, handle)
    return handle.value


def ekopr(fname):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param fname:
    :return: :rtype:
    """
    fname = stypes.stringToCharP(fname)
    handle = ctypes.c_int()
    libspice.ekopr_c(fname, ctypes.byref(handle))
    return handle.value


def ekops():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    :return: :rtype:
    """
    handle = ctypes.c_int()
    libspice.ekops_c(ctypes.byref(handle))
    return handle.value


def ekopw(fname):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param fname:
    :return: :rtype:
    """
    fname = stypes.stringToCharP(fname)
    handle = ctypes.c_int()
    libspice.ekopw_c(fname, ctypes.byref(handle))
    return handle.value


def ekpsel(query, msglen, tablen, collen):
    #Todo: test ekpsel
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param query:
    :param msglen:
    :param tablen:
    :param collen:
    :return: :rtype:
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
    libspice.ekpsel_c(query, msglen, tablen, collen, ctypes.byref(n), ctypes.byref(xbegs), ctypes.byref(xends), ctypes.byref(xtypes), ctypes.byref(xclass), ctypes.byref(tabs), ctypes.byref(cols), ctypes.byref(error), ctypes.byref(errmsg))
    return n.value, xbegs.value, xends.value, xtypes.value, xclass.value, stypes.vectorToList(tabs), stypes.vectorToList(cols), error.value, stypes.toPythonString(errmsg)


def ekrcec(handle, segno, recno, column, lenout, nelts=3):
    #Todo: test ekrcec , possible new way to get back 2d char arrays
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param handle:
    :param segno:
    :param recno:
    :param column:
    :param lenout:
    :param nelts:
    :return: :rtype:
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.stringToCharP(column)
    lenout = ctypes.c_int(lenout)
    nvals = ctypes.c_int()
    cvals = stypes.charvector(ndim=nelts, lenvals=lenout)
    isnull = ctypes.c_bool()
    libspice.ekrcec_c(handle, segno, recno, column, lenout, ctypes.byref(nvals), ctypes.byref(cvals), ctypes.byref(isnull))
    return nvals.value, stypes.vectorToList(cvals), isnull.value


def ekrced(handle, segno, recno, column):
    #Todo: test ekrced
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param handle:
    :param segno:
    :param recno:
    :param column:
    :return: :rtype:
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.stringToCharP(column)
    nvals = ctypes.c_int()
    dvals = ctypes.POINTER(ctypes.c_double)  # array of length nvals
    isnull = ctypes.c_bool()
    libspice.ekrced_c(handle, segno, recno, column, ctypes.byref(nvals), ctypes.byref(dvals), ctypes.byref(isnull))
    return nvals.value, stypes.vectorToList(dvals), isnull.value


def ekrcei(handle, segno, recno, column):
    #Todo: test ekrcei
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param handle:
    :param segno:
    :param recno:
    :param column:
    :return: :rtype:
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.stringToCharP(column)
    nvals = ctypes.c_int()
    ivals = ctypes.pointer(ctypes.c_int)  # array of length nvals
    isnull = ctypes.c_bool()
    libspice.ekrcei_c(handle, segno, recno, column, ctypes.byref(nvals), ivals, ctypes.byref(isnull))
    return nvals.value, stypes.vectorToList(ivals), isnull.value


def ekssum(handle, segno):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    :param segno:
    :return: :rtype:
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    segsum = stypes.SpiceEKSegSum()
    libspice.ekssum_c(handle, segno, ctypes.byref(segsum))
    return segsum


def ektnam(n, lenout):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param n:
    :param lenout:
    :return: :rtype:
    """
    n = ctypes.c_int(n)
    lenout = ctypes.c_int(lenout)
    table = stypes.stringToCharP(lenout)
    libspice.ektnam_c(n, lenout, table)
    return stypes.toPythonString(table)


def ekucec(handle, segno, recno, column, nvals, vallen, cvals, isnull):
    #Todo: test ekucec
    """

    :param handle:
    :param segno:
    :param recno:
    :param column:
    :param nvals:
    :param vallen:
    :param cvals:
    :param isnull:
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.stringToCharP(column)
    nvals = ctypes.c_int(nvals)
    vallen = ctypes.c_int(vallen)
    isnull = ctypes.c_bool(isnull)
    cvals = stypes.listToCharArrayPtr(cvals, xLen=vallen, yLen=nvals)
    libspice.ekucec_c(handle, segno, recno, column, nvals, vallen, cvals, isnull)
    pass


def ekuced(handle, segno, recno, column, nvals, dvals, isnull):
    #Todo: test ekucei
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param handle:
    :param segno:
    :param recno:
    :param column:
    :param nvals:
    :param dvals:
    :param isnull:
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.stringToCharP(column)
    nvals = ctypes.c_int(nvals)
    isnull = ctypes.c_bool(isnull)
    dvals = stypes.toDoubleVector(dvals)
    libspice.ekuced_c(handle, segno, recno, column, nvals, ctypes.byref(dvals), isnull)
    pass


def ekucei(handle, segno, recno, column, nvals, ivals, isnull):
    #Todo: test ekucei
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param handle:
    :param segno:
    :param recno:
    :param column:
    :param nvals:
    :param ivals:
    :param isnull:
    """
    handle = ctypes.c_int(handle)
    segno = ctypes.c_int(segno)
    recno = ctypes.c_int(recno)
    column = stypes.stringToCharP(column)
    nvals = ctypes.c_int(nvals)
    isnull = ctypes.c_bool(isnull)
    ivals = stypes.toIntVector(ivals)
    libspice.ekucei_c(handle, segno, recno, column, nvals, ctypes.byref(ivals), isnull)
    pass


def ekuef(handle):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    """
    handle = ctypes.c_int(handle)
    libspice.ekuef_c(handle)
    pass


def el2cgv(ellipse):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param ellipse:
    :return: :rtype:
    """
    assert(isinstance(ellipse, stypes.Ellipse))
    center = stypes.emptyDoubleVector(3)
    smajor = stypes.emptyDoubleVector(3)
    sminor = stypes.emptyDoubleVector(3)
    libspice.el2cgv_c(ctypes.byref(ellipse), center, smajor, sminor)
    return stypes.vectorToList(center), stypes.vectorToList(smajor), stypes.vectorToList(sminor)


def elemc(item, inset):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param item:
    :param inset:
    :return: :rtype:
    """
    assert isinstance(inset, stypes.SpiceCell)
    item = stypes.stringToCharP(item)
    return libspice.elemc_c(item, ctypes.byref(inset))


def elemd(item, inset):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param item:
    :param inset:
    :return: :rtype:
    """
    assert isinstance(inset, stypes.SpiceCell)
    assert inset.dtype == 1
    item = ctypes.c_double(item)
    return libspice.elemd_c(item, ctypes.byref(inset))


def elemi(item, inset):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param item:
    :param inset:
    :return: :rtype:
    """
    assert isinstance(inset, stypes.SpiceCell)
    assert inset.dtype == 2
    item = ctypes.c_int(item)
    return libspice.elemi_c(item, ctypes.byref(inset))


def eqncpv(et, epoch, eqel, rapol, decpol):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param et:
    :param epoch:
    :param eqel:
    :param rapol:
    :param decpol:
    :return: :rtype:
    """
    et = ctypes.c_double(et)
    epoch = ctypes.c_double(epoch)
    eqel = stypes.toDoubleVector(eqel)
    rapol = ctypes.c_double(rapol)
    decpol = ctypes.c_double(decpol)
    state = stypes.emptyDoubleVector(6)
    libspice.eqncpv_c(et, epoch, eqel, rapol, decpol, state)
    return stypes.vectorToList(state)


def eqstr(a, b):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param a:
    :param b:
    :return: :rtype:
    """
    return libspice.eqstr_c(stypes.stringToCharP(a), stypes.stringToCharP(b))


def erract(op, lenout, action=None):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param op:
    :param lenout:
    :param action:
    :return: :rtype:
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
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param marker:
    :param string:
    """
    marker = stypes.stringToCharP(marker)
    string = stypes.stringToCharP(string)
    libspice.errch_c(marker, string)
    pass


def errdev(op, lenout, device):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param op:
    :param lenout:
    :param device:
    :return: :rtype:
    """
    lenout = ctypes.c_int(lenout)
    op = stypes.stringToCharP(op)
    device = ctypes.create_string_buffer(str.encode(device), lenout.value)
    deviceptr = ctypes.c_char_p(ctypes.addressof(device))
    libspice.errdev_c(op, lenout, deviceptr)
    return stypes.toPythonString(deviceptr)


def errdp(marker, number):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param marker:
    :param number:
    """
    marker = stypes.stringToCharP(marker)
    number = ctypes.c_double(number)
    libspice.errdp_c(marker, number)
    pass


def errint(marker, number):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param marker:
    :param number:
    """
    marker = stypes.stringToCharP(marker)
    number = ctypes.c_int(number)
    libspice.errint_c(marker, number)
    pass


def errprt(op, lenout, inlist):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param op:
    :param lenout:
    :param inlist:
    :return: :rtype:
    """
    lenout = ctypes.c_int(lenout)
    op = stypes.stringToCharP(op)
    inlist = ctypes.create_string_buffer(str.encode(inlist), lenout.value)
    inlistptr = ctypes.c_char_p(ctypes.addressof(inlist))
    libspice.errdev_c(op, lenout, inlistptr)
    return stypes.toPythonString(inlistptr)


def esrchc(value, array):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param value:
    :param array:
    :return: :rtype:
    """
    value = stypes.stringToCharP(value)
    ndim = ctypes.c_int(len(array))
    lenvals = ctypes.c_int(len(max(array, key=len)) + 1)
    array = stypes.listToCharArray(array, xLen=lenvals, yLen=ndim)
    return libspice.esrchc_c(value, ndim, lenvals, array)


def et2lst(et, body, lon, typein, timlen, ampmlen):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param et:
    :param body:
    :param lon:
    :param typein:
    :param timlen:
    :param ampmlen:
    :return: :rtype:
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
                    ctypes.byref(hr), ctypes.byref(mn), ctypes.byref(sc), time, ampm)
    return hr.value, mn.value, sc.value, stypes.toPythonString(time), stypes.toPythonString(ampm)


def et2utc(et, formatStr, prec, lenout):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param et:
    :param formatStr:
    :param prec:
    :param lenout:
    :return: :rtype:
    """
    et = ctypes.c_double(et)
    prec = ctypes.c_int(prec)
    lenout = ctypes.c_int(lenout)
    formatStr = stypes.stringToCharP(formatStr)
    utcstr = stypes.stringToCharP(lenout)
    libspice.et2utc_c(et, formatStr, prec, lenout, utcstr)
    return stypes.toPythonString(utcstr)


def etcal(et, lenout):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param et:
    :param lenout:
    :return: :rtype:
    """
    et = ctypes.c_double(et)
    lenout = ctypes.c_int(lenout)
    string = stypes.stringToCharP(lenout)
    libspice.etcal_c(et, lenout, string)
    return stypes.toPythonString(string)


def eul2m(angle3, angle2, angle1, axis3, axis2, axis1):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param angle3:
    :param angle2:
    :param angle1:
    :param axis3:
    :param axis2:
    :param axis1:
    :return: :rtype:
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


def eul2xf(eulang, axisa, axisb, axisc):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param eulang:
    :param axisa:
    :param axisb:
    :param axisc:
    :return: :rtype:
    """
    assert len(eulang) is 6
    eulang = stypes.toDoubleVector(eulang)
    axisa = ctypes.c_int(axisa)
    axisb = ctypes.c_int(axisb)
    axisc = ctypes.c_int(axisc)
    xform = stypes.emptyDoubleMatrix(x=6, y=6)
    libspice.eul2xf_c(eulang, axisa, axisb, axisc, xform)
    return stypes.matrixToList(xform)


def exists(fname):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param fname:
    :return: :rtype:
    """
    fname = stypes.stringToCharP(fname)
    return libspice.exists_c(fname)


def expool(name):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param name:
    :return: :rtype:
    """
    name = stypes.stringToCharP(name)
    found = ctypes.c_bool()
    libspice.expool_c(name, ctypes.byref(found))
    return found.value


########################################################################################################################
# F


def failed():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    :return: :rtype:
    """
    return libspice.failed_c()


def fovray(inst, raydir, rframe, abcorr, observer, et):
    # Unsure if et is returned or not (I vs I/O)
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param inst:
    :param raydir:
    :param rframe:
    :param abcorr:
    :param observer:
    :param et:
    :return: :rtype:
    """
    inst = stypes.stringToCharP(inst)
    raydir = stypes.toDoubleVector(raydir)
    rframe = stypes.stringToCharP(rframe)
    abcorr = stypes.stringToCharP(abcorr)
    observer = stypes.stringToCharP(observer)
    et = ctypes.c_double(et)
    visible = ctypes.c_bool()
    libspice.fovray_c(inst, raydir, rframe, abcorr, observer, ctypes.byref(et), ctypes.byref(visible))
    return visible.value


def fovtrg(inst, target, tshape, tframe, abcorr, observer, et):
    # Unsure if et is returned or not (I vs I/O)
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param inst:
    :param target:
    :param tshape:
    :param tframe:
    :param abcorr:
    :param observer:
    :param et:
    :return: :rtype:
    """
    inst = stypes.stringToCharP(inst)
    target = stypes.stringToCharP(target)
    tshape = stypes.stringToCharP(tshape)
    tframe = stypes.stringToCharP(tframe)
    abcorr = stypes.stringToCharP(abcorr)
    observer = stypes.stringToCharP(observer)
    et = ctypes.c_double(et)
    visible = ctypes.c_bool()
    libspice.fovtrg_c(inst, target, tshape, tframe, abcorr, observer, ctypes.byref(et), ctypes.byref(visible))
    return visible.value


def frame(x):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param x:
    :return: :rtype:
    """
    x = stypes.toDoubleVector(x)
    y = stypes.emptyDoubleVector(3)
    z = stypes.emptyDoubleVector(3)
    libspice.frame_c(x, y, z)
    return stypes.vectorToList(x), stypes.vectorToList(y), stypes.vectorToList(z)


def frinfo(frcode):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param frcode:
    :return: :rtype:
    """
    frcode = ctypes.c_int(frcode)
    cent = ctypes.c_int()
    frclss = ctypes.c_int()
    clssid = ctypes.c_int()
    found = ctypes.c_bool()
    libspice.frinfo_c(frcode, ctypes.byref(cent), ctypes.byref(frclss), ctypes.byref(clssid), ctypes.byref(found))
    return cent.value, frclss.value, clssid.value, found.value


def frmnam(frcode, lenout=125):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param frcode:
    :param lenout:
    :return: :rtype:
    """
    frcode = ctypes.c_int(frcode)
    lenout = ctypes.c_int(lenout)
    frname = stypes.stringToCharP(lenout)
    libspice.frmnam_c(frcode, lenout, frname)
    return stypes.toPythonString(frname)


def ftncls(unit):
    #Todo: close ftncls
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param unit:
    """
    unit = ctypes.c_int(unit)
    libspice.ftncls_c(unit)
    pass


def furnsh(path):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param path:
    """
    if isinstance(path, list):
        for p in path:
            libspice.furnsh_c(stypes.stringToCharP(p))
    else:
        path = stypes.stringToCharP(path)
        libspice.furnsh_c(path)
    pass

########################################################################################################################
# G


def gcpool(name, start, room, lenout):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param name:
    :param start:
    :param room:
    :param lenout:
    :return: :rtype:
    """
    name = stypes.stringToCharP(name)
    start = ctypes.c_int(start)
    room = ctypes.c_int(room)
    lenout = ctypes.c_int(lenout)
    n = ctypes.c_int()
    cvals = stypes.emptyCharArray(lenout, room)
    found = ctypes.c_bool()
    libspice.gcpool_c(name, start, room, lenout, ctypes.byref(n), ctypes.byref(cvals), ctypes.byref(found))
    if found.value:
        return [stypes.toPythonString(x.value) for x in cvals[0:n.value]]
    else:
        return None


def gdpool(name, start, room):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param name:
    :param start:
    :param room:
    :return: :rtype:
    """
    name = stypes.stringToCharP(name)
    start = ctypes.c_int(start)
    values = stypes.emptyDoubleVector(room)
    room = ctypes.c_int(room)
    n = ctypes.c_int()
    found = ctypes.c_bool()
    libspice.gdpool_c(name, start, room, ctypes.byref(n),
                      ctypes.cast(values, ctypes.POINTER(ctypes.c_double)), ctypes.byref(found))
    if found.value:
        return stypes.vectorToList(values)[0:n.value]
    else:
        return None


def georec(lon, lat, alt, re, f):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param lon:
    :param lat:
    :param alt:
    :param re:
    :param f:
    :return: :rtype:
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


def getelm(frstyr, lineln, lines):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param frstyr:
    :param lineln:
    :param lines:
    :return: :rtype:
    """
    frstyr = ctypes.c_int(frstyr)
    lineln = ctypes.c_int(lineln)
    lines = stypes.listToCharArrayPtr(lines, xLen=lineln, yLen=2)
    epoch = ctypes.c_double()
    elems = stypes.emptyDoubleVector(10)  # guess for length
    libspice.getelm_c(frstyr, lineln, lines, ctypes.byref(epoch), elems)
    return epoch.value, stypes.vectorToList(elems)


def getfat(file):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param file:
    :return: :rtype:
    """
    file = stypes.stringToCharP(file)
    arclen = ctypes.c_int(4)
    typlen = ctypes.c_int(4)
    arch = stypes.stringToCharP(arclen)
    rettype = stypes.stringToCharP(typlen)
    libspice.getfat_c(file, arclen, typlen, arch, rettype)
    return stypes.toPythonString(arch), stypes.toPythonString(rettype)


def getfov(instid, room, shapelen, framelen):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param instid:
    :param room:
    :param shapelen:
    :param framelen:
    :return: :rtype:
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
    libspice.getfov_c(instid, room, shapelen, framelen, shape, framen, bsight, ctypes.byref(n), bounds)
    return stypes.toPythonString(shape), stypes.toPythonString(framen), stypes.vectorToList(
        bsight), n.value, stypes.matrixToList(bounds)[0:n.value]


def getmsg(option, lenout):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param option:
    :param lenout:
    :return: :rtype:
    """
    option = stypes.stringToCharP(option)
    lenout = ctypes.c_int(lenout)
    msg = stypes.stringToCharP(lenout)
    libspice.getmsg_c(option, lenout, msg)
    return stypes.toPythonString(msg)


def gfbail():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    :return: :rtype:
    """
    return libspice.gfbail_c()


def gfclrh():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    """
    libspice.gfclrh_c()
    pass


def gfdist(target, abcorr, obsrvr, relate, refval, adjust, step, nintvls, cnfine, result):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param target:
    :param abcorr:
    :param obsrvr:
    :param relate:
    :param refval:
    :param adjust:
    :param step:
    :param nintvls:
    :param cnfine:
    :param result:
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


#gdevnt  callbacks? cells


#gffove  callbacks? cells


# gfilum


def gfinth(sigcode):
    #Todo: test gfinth
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param sigcode:
    """
    sigcode = ctypes.c_int(sigcode)
    libspice.gfinth_c(sigcode)
    pass


#gfocce  callbacks? cells


def gfoclt(occtyp, front, fshape, fframe, back, bshape, bframe, abcorr, obsrvr, step, cnfine, result):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param occtyp:
    :param front:
    :param fshape:
    :param fframe:
    :param back:
    :param bshape:
    :param bframe:
    :param abcorr:
    :param obsrvr:
    :param step:
    :param cnfine:
    :param result:
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
                      abcorr, obsrvr, step, ctypes.byref(cnfine), ctypes.byref(result))


def gfpa(target, illmin, abcorr, obsrvr, relate, refval, adjust, step, nintvals, cnfine, result):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param target:
    :param illmin:
    :param abcorr:
    :param obsrvr:
    :param relate:
    :param refval:
    :param adjust:
    :param step:
    :param nintvals:
    :param cnfine:
    :param result:
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
                    adjust, step, nintvals, ctypes.byref(cnfine), ctypes.byref(result))
    pass


def gfposc(target, inframe, abcorr, obsrvr, crdsys, coord, relate, refval, adjust, step, nintvals, cnfine, result):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param target:
    :param inframe:
    :param abcorr:
    :param obsrvr:
    :param crdsys:
    :param coord:
    :param relate:
    :param refval:
    :param adjust:
    :param step:
    :param nintvals:
    :param cnfine:
    :param result:
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
                      relate, refval, adjust, step, nintvals, ctypes.byref(cnfine), ctypes.byref(result))
    pass


def gfrefn(t1, t2, s1, s2):
    #Todo: test gfrefn
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param t1:
    :param t2:
    :param s1:
    :param s2:
    :return: :rtype:
    """
    t1 = ctypes.c_double(t1)
    t2 = ctypes.c_double(t2)
    s1 = ctypes.c_bool(s1)
    s2 = ctypes.c_bool(s2)
    t = ctypes.c_bool()
    libspice.gfrefn_c(t1, t2, s1, s2, ctypes.byref(t))
    return t.value


def gfrepf():
    #Todo: test gfrepf
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    """
    libspice.gfrepf_c()
    pass


def gfrepi(window, begmss, endmss):
    #Todo: test gfrepi
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param window:
    :param begmss:
    :param endmss:
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.is_double()
    begmss = stypes.stringToCharP(begmss)
    endmss = stypes.stringToCharP(endmss)
    libspice.gfrepi_c(ctypes.byref(window), begmss, endmss)
    pass


def gfrepu(ivbeg, ivend, time):
    #Todo: test gfrepu
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param ivbeg:
    :param ivend:
    :param time:
    """
    ivbeg = ctypes.c_double(ivbeg)
    ivend = ctypes.c_double(ivend)
    time = ctypes.c_double(time)
    libspice.gfrepu_c(ivbeg, ivend, time)
    pass


def gfrfov(inst, raydir, rframe, abcorr, obsrvr, step, cnfine, result):
    #Todo: test gfrfov
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param inst:
    :param raydir:
    :param rframe:
    :param abcorr:
    :param obsrvr:
    :param step:
    :param cnfine:
    :param result:
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
    libspice.gfrfov_c(inst, raydir, rframe, abcorr, obsrvr, step, ctypes.byref(cnfine), ctypes.byref(result))


def gfrr(target, abcorr, obsrvr, relate, refval, adjust, step, nintvals, cnfine, result):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param target:
    :param abcorr:
    :param obsrvr:
    :param relate:
    :param refval:
    :param adjust:
    :param step:
    :param nintvals:
    :param cnfine:
    :param result:
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
                    adjust, step, nintvals, ctypes.byref(cnfine), ctypes.byref(result))


def gfsep(targ1, shape1, inframe1, targ2, shape2, inframe2, abcorr, obsrvr, relate, refval, adjust, step, nintvals, cnfine, result):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param targ1:
    :param shape1:
    :param inframe1:
    :param targ2:
    :param shape2:
    :param inframe2:
    :param abcorr:
    :param obsrvr:
    :param relate:
    :param refval:
    :param adjust:
    :param step:
    :param nintvals:
    :param cnfine:
    :param result:
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


def gfsntc(target, fixref, method, abcorr, obsrvr, dref, dvec, crdsys, coord, relate, refval, adjust, step, nintvals,
           cnfine, result):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param target:
    :param fixref:
    :param method:
    :param abcorr:
    :param obsrvr:
    :param dref:
    :param dvec:
    :param crdsys:
    :param coord:
    :param relate:
    :param refval:
    :param adjust:
    :param step:
    :param nintvals:
    :param cnfine:
    :param result:
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
                      adjust, step, nintvals, ctypes.byref(cnfine), ctypes.byref(result))


def gfsstp(step):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param step:
    """
    step = ctypes.c_double(step)
    libspice.gfsstp_c(step)
    pass


def gfstep(time):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param time:
    :return: :rtype:
    """
    time = ctypes.c_double(time)
    step = ctypes.c_double()
    libspice.gfstep_c(time, ctypes.byref(step))
    return step.value


def gfstol(value):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param value:
    """
    value = ctypes.c_double(value)
    libspice.gfstol_c(value)
    pass


def gfsubc(target, fixref, method, abcorr, obsrvr, crdsys, coord, relate, refval, adjust, step, nintvals, cnfine,
           result):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param target:
    :param fixref:
    :param method:
    :param abcorr:
    :param obsrvr:
    :param crdsys:
    :param coord:
    :param relate:
    :param refval:
    :param adjust:
    :param step:
    :param nintvals:
    :param cnfine:
    :param result:
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
                      coord, relate, refval, adjust, step, nintvals, ctypes.byref(cnfine), ctypes.byref(result))


def gftfov(inst, target, tshape, tframe, abcorr, obsrvr, step, cnfine):
    #Todo: test gftfov
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param inst:
    :param target:
    :param tshape:
    :param tframe:
    :param abcorr:
    :param obsrvr:
    :param step:
    :param cnfine:
    """
    assert isinstance(cnfine, stypes.SpiceCell)
    assert cnfine.is_double()
    target = stypes.stringToCharP(target)
    tshape = stypes.stringToCharP(tshape)
    tframe = stypes.stringToCharP(tframe)
    abcorr = stypes.stringToCharP(abcorr)
    obsrvr = stypes.stringToCharP(obsrvr)
    step = ctypes.c_double(step)
    result = stypes.SPICEDOUBLE_CELL(cnfine.size)
    libspice.gftfov_c(inst, target, tshape, tframe, abcorr, obsrvr, step, ctypes.byref(cnfine), ctypes.byref(result))


# gfudb has call backs


#gfuds has call backs


def gipool(name, start, room):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param name:
    :param start:
    :param room:
    :return: :rtype:
    """
    name = stypes.stringToCharP(name)
    start = ctypes.c_int(start)
    ivals = stypes.emptyIntVector(room)
    room = ctypes.c_int(room)
    n = ctypes.c_int()
    found = ctypes.c_bool()
    libspice.gipool_c(name, start, room, ctypes.byref(n), ivals, ctypes.byref(found))
    if found.value:
        return stypes.vectorToList(ivals)[0:n.value]
    else:
        return False


def gnpool(name, start, room, lenout):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param name:
    :param start:
    :param room:
    :param lenout:
    :return: :rtype:
    """
    name = stypes.stringToCharP(name)
    start = ctypes.c_int(start)
    kvars = stypes.charvector(room, lenout)
    room = ctypes.c_int(room)
    lenout = ctypes.c_int(lenout)
    n = ctypes.c_int()
    found = ctypes.c_bool()
    libspice.gnpool_c(name, start, room, lenout, ctypes.byref(n), kvars, ctypes.byref(found))
    return stypes.vectorToList(kvars)[0:n.value], found.value


########################################################################################################################
# H


def halfpi():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    :return: :rtype:
    """
    return libspice.halfpi_c()


def hx2dp(string):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param string:
    :return: :rtype:
    """
    string = stypes.stringToCharP(string)
    lenout = ctypes.c_int(80)
    errmsg = stypes.stringToCharP(lenout)
    number = ctypes.c_double()
    error = ctypes.c_bool()
    libspice.hx2dp_c(string, lenout, ctypes.byref(number), ctypes.byref(error), errmsg)
    if not error.value:
        return number.value
    else:
        return stypes.toPythonString(errmsg)


########################################################################################################################
# I


def ident():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    :return: :rtype:
    """
    matrix = stypes.emptyDoubleMatrix()
    libspice.ident_c(matrix)
    return stypes.matrixToList(matrix)


def illum(target, et, abcorr, obsrvr, spoint):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param target:
    :param et:
    :param abcorr:
    :param obsrvr:
    :param spoint:
    :return: :rtype:
    """
    target = stypes.stringToCharP(target)
    et = ctypes.c_double(et)
    abcorr = stypes.stringToCharP(abcorr)
    obsrvr = stypes.stringToCharP(obsrvr)
    spoint = stypes.toDoubleVector(spoint)
    phase = ctypes.c_double(0)
    solar = ctypes.c_double(0)
    emissn = ctypes.c_double(0)
    libspice.illum_c(target, et, abcorr, obsrvr, spoint, ctypes.byref(phase), ctypes.byref(solar), ctypes.byref(emissn))
    return phase.value, solar.value, emissn.value


def ilumin(method, target, et, fixref, abcorr, obsrvr, spoint):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param method:
    :param target:
    :param et:
    :param fixref:
    :param abcorr:
    :param obsrvr:
    :param spoint:
    :return: :rtype:
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
    libspice.ilumin_c(method, target, et, fixref, abcorr, obsrvr, spoint, ctypes.byref(trgepc),
              srfvec, ctypes.byref(phase), ctypes.byref(solar), ctypes.byref(emissn))
    return trgepc.value, stypes.vectorToList(srfvec), phase.value, solar.value, emissn.value


def inedpl(a, b, c, plane):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param a:
    :param b:
    :param c:
    :param plane:
    :return: :rtype:
    """
    assert (isinstance(plane, stypes.Plane))
    ellipse = stypes.Ellipse()
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    found = ctypes.c_bool()
    libspice.inedpl_c(a, b, c, ctypes.byref(plane), ctypes.byref(ellipse), ctypes.byref(found))
    if found.value:
        return ellipse
    else:
        return None


def inelpl(ellips, plane):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param ellips:
    :param plane:
    :return: :rtype:
    """
    assert(isinstance(plane, stypes.Plane))
    assert(isinstance(ellips, stypes.Ellipse))
    nxpts = ctypes.c_int()
    xpt1 = stypes.emptyDoubleVector(3)
    xpt2 = stypes.emptyDoubleVector(3)
    libspice.inelpl_c(ctypes.byref(ellips), ctypes.byref(plane), ctypes.byref(nxpts), xpt1, xpt2)
    return nxpts.value, stypes.vectorToList(xpt1), stypes.vectorToList(xpt2)


def inrypl(vertex, direct, plane):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param vertex:
    :param direct:
    :param plane:
    :return: :rtype:
    """
    assert(isinstance(plane, stypes.Plane))
    vertex = stypes.toDoubleVector(vertex)
    direct = stypes.toDoubleVector(direct)
    nxpts = ctypes.c_int()
    xpt = stypes.emptyDoubleVector(3)
    libspice.inrypl_c(vertex, direct, ctypes.byref(plane), ctypes.byref(nxpts), xpt)
    return nxpts.value, stypes.vectorToList(xpt)


def insrtc(item, inset):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param item:
    :param inset:
    """
    assert isinstance(inset, stypes.SpiceCell)
    if isinstance(item, list):
        for c in item:
            libspice.insrtc_c(stypes.stringToCharP(c), ctypes.byref(inset))
    else:
        item = stypes.stringToCharP(item)
        libspice.insrtc_c(item, ctypes.byref(inset))
    pass


def insrtd(item, inset):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param item:
    :param inset:
    """
    assert isinstance(inset, stypes.SpiceCell)
    if hasattr(item, "__iter__"):
        for d in item:
            libspice.insrtd_c(ctypes.c_double(d), ctypes.byref(inset))
    else:
        item = ctypes.c_double(item)
        libspice.insrtd_c(item, ctypes.byref(inset))
    pass


def insrti(item, inset):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param item:
    :param inset:
    """
    assert isinstance(inset, stypes.SpiceCell)
    if hasattr(item, "__iter__"):
        for i in item:
            libspice.insrti_c(ctypes.c_int(i), ctypes.byref(inset))
    else:
        item = ctypes.c_int(item)
        libspice.insrti_c(item, ctypes.byref(inset))
    pass


def inter(a, b):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param a:
    :param b:
    :return: :rtype: :raise NotImplementedError:
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


def intmax():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    :return: :rtype:
    """
    return libspice.intmax_c()


def intmin():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    :return: :rtype:
    """
    return libspice.intmin_c()


def invert(m):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param m:
    :return: :rtype:
    """
    m = stypes.listtodoublematrix(m)
    mout = stypes.emptyDoubleMatrix()
    libspice.invert_c(m, mout)
    return stypes.matrixToList(mout)


def invort(m):
    #Todo: test invort
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param m:
    :return: :rtype:
    """
    m = stypes.listtodoublematrix(m)
    mout = stypes.emptyDoubleMatrix()
    libspice.invort_c(m, mout)
    return stypes.matrixToList(mout)


def isordv(array, n):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param array:
    :param n:
    :return: :rtype:
    """
    array = stypes.toIntVector(array)
    n = ctypes.c_int(n)
    return libspice.isordv_c(array, n)


def isrchc(value, ndim, lenvals, array):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param value:
    :param ndim:
    :param lenvals:
    :param array:
    :return: :rtype:
    """
    value = stypes.stringToCharP(value)
    array = stypes.listToCharArrayPtr(array, xLen=lenvals, yLen=ndim)
    ndim = ctypes.c_int(ndim)
    lenvals = ctypes.c_int(lenvals)
    return libspice.isrchc_c(value, ndim, lenvals, array)


def isrchd(value, ndim, array):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param value:
    :param ndim:
    :param array:
    :return: :rtype:
    """
    value = ctypes.c_double(value)
    ndim = ctypes.c_int(ndim)
    array = stypes.toDoubleVector(array)
    return libspice.isrchd_c(value, ndim, array)


def isrchi(value, ndim, array):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param value:
    :param ndim:
    :param array:
    :return: :rtype:
    """
    value = ctypes.c_int(value)
    ndim = ctypes.c_int(ndim)
    array = stypes.toIntVector(array)
    return libspice.isrchi_c(value, ndim, array)


def isrot(m, ntol, dtol):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param m:
    :param ntol:
    :param dtol:
    :return: :rtype:
    """
    m = stypes.listtodoublematrix(m)
    ntol = ctypes.c_double(ntol)
    dtol = ctypes.c_double(dtol)
    return libspice.isrot_c(m, ntol, dtol)


def iswhsp(string):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param string:
    :return: :rtype:
    """
    string = stypes.stringToCharP(string)
    return libspice.iswhsp_c(string)


########################################################################################################################
# J


def j1900():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    :return: :rtype:
    """
    return libspice.j1900_c()


def j1950():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    :return: :rtype:
    """
    return libspice.j1950_c()


def j2000():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    :return: :rtype:
    """
    return libspice.j2000_c()


def j2100():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    :return: :rtype:
    """
    return libspice.j2100_c()


def jyear():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    :return: :rtype:
    """
    return libspice.jyear_c()
########################################################################################################################
# K


def kclear():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    """
    libspice.kclear_c()
    pass


def kdata(which, kind, fillen, typlen, srclen):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param which:
    :param kind:
    :param fillen:
    :param typlen:
    :param srclen:
    :return: :rtype:
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
    libspice.kdata_c(which, kind, fillen, typlen, srclen, file, filtyp, source, ctypes.byref(handle), ctypes.byref(found))
    return stypes.toPythonString(file), stypes.toPythonString(filtyp), stypes.toPythonString(source), handle.value, found.value


def kinfo(file, typlen, srclen):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param file:
    :param typlen:
    :param srclen:
    :return: :rtype:
    """
    typlen = ctypes.c_int(typlen)
    srclen = ctypes.c_int(srclen)
    file = stypes.stringToCharP(file)
    filtyp = stypes.stringToCharP(" " * typlen.value)
    source = stypes.stringToCharP(" " * srclen.value)
    handle = ctypes.c_int()
    found = ctypes.c_bool()
    libspice.kinfo_c(file, typlen, srclen, filtyp, source, ctypes.byref(handle), ctypes.byref(found))
    return stypes.toPythonString(filtyp), stypes.toPythonString(source), handle.value, found.value


def kplfrm(frmcls, cell_size=1000):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param frmcls:
    :param cell_size:
    :return: :rtype:
    """
    frmcls = ctypes.c_int(frmcls)
    idset = stypes.SPICEINT_CELL(cell_size)
    libspice.kplfrm_c(frmcls, ctypes.byref(idset))
    return idset


def ktotal(kind):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param kind:
    :return: :rtype:
    """
    kind = stypes.stringToCharP(kind)
    count = ctypes.c_int()
    libspice.ktotal_c(kind, ctypes.byref(count))
    return count.value


def kxtrct(keywd, termlen, terms, nterms, stringlen, substrlen, instring):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param keywd:
    :param termlen:
    :param terms:
    :param nterms:
    :param stringlen:
    :param substrlen:
    :param instring:
    :return: :rtype:
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
                      stringlen, substrlen, instring, ctypes.byref(found), substr)
    return stypes.toPythonString(instring), found.value, stypes.toPythonString(substr)


########################################################################################################################
# L


def lastnb(string):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param string:
    :return: :rtype:
    """
    string = stypes.stringToCharP(string)
    return libspice.lastnb_c(string)


def latcyl(radius, lon, lat):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param radius:
    :param lon:
    :param lat:
    :return: :rtype:
    """
    radius = ctypes.c_double(radius)
    lon = ctypes.c_double(lon)
    lat = ctypes.c_double(lat)
    r = ctypes.c_double()
    lonc = ctypes.c_double()
    z = ctypes.c_double()
    libspice.latcyl_c(radius, lon, lat, ctypes.byref(r), ctypes.byref(lonc), ctypes.byref(z))
    return r.value, lonc.value, z.value


def latrec(radius, longitude, latitude):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param radius:
    :param longitude:
    :param latitude:
    :return: :rtype:
    """
    radius = ctypes.c_double(radius)
    longitude = ctypes.c_double(longitude)
    latitude = ctypes.c_double(latitude)
    rectan = stypes.emptyDoubleVector(3)
    libspice.latrec_c(radius, longitude, latitude, rectan)
    return stypes.vectorToList(rectan)


def latsph(radius, lon, lat):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param radius:
    :param lon:
    :param lat:
    :return: :rtype:
    """
    radius = ctypes.c_double(radius)
    lon = ctypes.c_double(lon)
    lat = ctypes.c_double(lat)
    rho = ctypes.c_double()
    colat = ctypes.c_double()
    lons = ctypes.c_double()
    libspice.latsph_c(radius, lon, lat, ctypes.byref(rho), ctypes.byref(colat), ctypes.byref(lons))
    return rho.value, colat.value, lons.value


def lcase(instr, lenout):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param instr:
    :param lenout:
    :return: :rtype:
    """
    instr = stypes.stringToCharP(instr)
    lenout = ctypes.c_int(lenout)
    outstr = stypes.stringToCharP(lenout)
    libspice.lcase_c(instr, lenout, outstr)
    return stypes.toPythonString(outstr)


def ldpool(filename):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param filename:
    """
    filename = stypes.stringToCharP(filename)
    libspice.ldpool_c(filename)
    pass


def lmpool(cvals):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param cvals:
    """
    lenvals = ctypes.c_int(len(max(cvals, key=len)) + 1)
    n = ctypes.c_int(len(cvals))
    cvals = stypes.listToCharArrayPtr(cvals, xLen=lenvals, yLen=n)
    libspice.lmpool_c(cvals, lenvals, n)
    pass


def lparse(inlist, delim, nmax):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param inlist:
    :param delim:
    :param nmax:
    :return: :rtype:
    """
    delim = stypes.stringToCharP(delim)
    lenout = ctypes.c_int(len(inlist))
    inlist = stypes.stringToCharP(inlist)
    nmax = ctypes.c_int(nmax)
    items = stypes.emptyCharArray(lenout, nmax)
    n = ctypes.c_int()
    libspice.lparse_c(inlist, delim, nmax, lenout, ctypes.byref(n), ctypes.byref(items))
    return [stypes.toPythonString(x.value) for x in items[0:n.value]]


def lparsm(inlist, delims, nmax, lenout=None):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param inlist:
    :param delims:
    :param nmax:
    :param lenout:
    :return: :rtype:
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


def lparss(inlist, delims, NMAX=20, LENGTH=50):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param inlist:
    :param delims:
    :param NMAX:
    :param LENGTH:
    :return: :rtype:
    """
    inlist = stypes.stringToCharP(inlist)
    delims = stypes.stringToCharP(delims)
    returnSet = stypes.SPICECHAR_CELL(NMAX, LENGTH)
    libspice.lparss_c(inlist, delims, ctypes.byref(returnSet))
    return returnSet


def lspcn(body, et, abcorr):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param body:
    :param et:
    :param abcorr:
    :return: :rtype:
    """
    body = stypes.stringToCharP(body)
    et = ctypes.c_double(et)
    abcorr = stypes.stringToCharP(abcorr)
    return libspice.lspcn_c(body, et, abcorr)


def ltime(etobs, obs, direct, targ):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param etobs:
    :param obs:
    :param direct:
    :param targ:
    :return: :rtype:
    """
    etobs = ctypes.c_double(etobs)
    obs = ctypes.c_int(obs)
    direct = stypes.stringToCharP(direct)
    targ = ctypes.c_int(targ)
    ettarg = ctypes.c_double()
    elapsd = ctypes.c_double()
    libspice.ltime_c(etobs, obs, direct, targ, ctypes.byref(ettarg), ctypes.byref(elapsd))
    return ettarg.value, elapsd.value


def lstlec(string, n, lenvals, array):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param string:
    :param n:
    :param lenvals:
    :param array:
    :return: :rtype:
    """
    string = stypes.stringToCharP(string)
    array = stypes.listToCharArrayPtr(array, xLen=lenvals, yLen=n)
    n = ctypes.c_int(n)
    lenvals = ctypes.c_int(lenvals)
    return libspice.lstlec_c(string, n, lenvals, array)


def lstled(x, n, array):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param x:
    :param n:
    :param array:
    :return: :rtype:
    """
    array = stypes.toDoubleVector(array)
    x = ctypes.c_double(x)
    n = ctypes.c_int(n)
    return libspice.lstled_c(x, n, array)


def lstlei(x, n, array):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param x:
    :param n:
    :param array:
    :return: :rtype:
    """
    array = stypes.toIntVector(array)
    x = ctypes.c_int(x)
    n = ctypes.c_int(n)
    return libspice.lstlei_c(x, n, array)


def lstltc(string, n, lenvals, array):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param string:
    :param n:
    :param lenvals:
    :param array:
    :return: :rtype:
    """
    string = stypes.stringToCharP(string)
    array = stypes.listToCharArrayPtr(array, xLen=lenvals, yLen=n)
    n = ctypes.c_int(n)
    lenvals = ctypes.c_int(lenvals)
    return libspice.lstltc_c(string, n, lenvals, array)


def lstltd(x, n, array):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param x:
    :param n:
    :param array:
    :return: :rtype:
    """
    array = stypes.toDoubleVector(array)
    x = ctypes.c_double(x)
    n = ctypes.c_int(n)
    return libspice.lstltd_c(x, n, array)


def lstlti(x, n, array):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param x:
    :param n:
    :param array:
    :return: :rtype:
    """
    array = stypes.toIntVector(array)
    x = ctypes.c_int(x)
    n = ctypes.c_int(n)
    return libspice.lstlti_c(x, n, array)


def lx4dec(string, first):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param string:
    :param first:
    :return: :rtype:
    """
    string = stypes.stringToCharP(string)
    first = ctypes.c_int(first)
    last = ctypes.c_int()
    nchar = ctypes.c_int()
    libspice.lx4dec_c(string, first, ctypes.byref(last), ctypes.byref(nchar))
    return last.value, nchar.value


def lx4num(string, first):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param string:
    :param first:
    :return: :rtype:
    """
    string = stypes.stringToCharP(string)
    first = ctypes.c_int(first)
    last = ctypes.c_int()
    nchar = ctypes.c_int()
    libspice.lx4num_c(string, first, ctypes.byref(last), ctypes.byref(nchar))
    return last.value, nchar.value


def lx4sgn(string, first):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param string:
    :param first:
    :return: :rtype:
    """
    string = stypes.stringToCharP(string)
    first = ctypes.c_int(first)
    last = ctypes.c_int()
    nchar = ctypes.c_int()
    libspice.lx4sgn_c(string, first, ctypes.byref(last), ctypes.byref(nchar))
    return last.value, nchar.value


def lx4uns(string, first):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param string:
    :param first:
    :return: :rtype:
    """
    string = stypes.stringToCharP(string)
    first = ctypes.c_int(first)
    last = ctypes.c_int()
    nchar = ctypes.c_int()
    libspice.lx4uns_c(string, first, ctypes.byref(last), ctypes.byref(nchar))
    return last.value, nchar.value


def lxqstr(string, qchar, first):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param string:
    :param qchar:
    :param first:
    :return: :rtype:
    """
    string = stypes.stringToCharP(string)
    qchar = ctypes.c_char(qchar.encode(encoding = 'UTF-8'))
    first = ctypes.c_int(first)
    last = ctypes.c_int()
    nchar = ctypes.c_int()
    libspice.lxqstr_c(string, qchar, first, ctypes.byref(last), ctypes.byref(nchar))
    return last.value, nchar.value


########################################################################################################################
# M


def m2eul(r, axis3, axis2, axis1):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param r:
    :param axis3:
    :param axis2:
    :param axis1:
    :return: :rtype:
    """
    r = stypes.listtodoublematrix(r)
    axis3 = ctypes.c_int(axis3)
    axis2 = ctypes.c_int(axis2)
    axis1 = ctypes.c_int(axis1)
    angle3 = ctypes.c_double()
    angle2 = ctypes.c_double()
    angle1 = ctypes.c_double()
    libspice.m2eul_c(r, axis3, axis2, axis1, ctypes.byref(angle3), ctypes.byref(angle2), ctypes.byref(angle1))
    return angle3.value, angle2.value, angle1.value


def m2q(r):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param r:
    :return: :rtype:
    """
    r = stypes.listtodoublematrix(r)
    q = stypes.emptyDoubleVector(4)
    libspice.m2q_c(r, q)
    return stypes.vectorToList(q)


def matchi(string, templ, wstr, wchr):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param string:
    :param templ:
    :param wstr:
    :param wchr:
    :return: :rtype:
    """
    string = stypes.stringToCharP(string)
    templ = stypes.stringToCharP(templ)
    wstr = ctypes.c_char(wstr.encode(encoding = 'UTF-8'))
    wchr = ctypes.c_char(wchr.encode(encoding = 'UTF-8'))
    return libspice.matchi_c(string, templ, wstr, wchr)


def matchw(string, templ, wstr, wchr):
    # ctypes.c_char(wstr.encode(encoding='UTF-8')
    """

    :param string:
    :param templ:
    :param wstr:
    :param wchr:
    :return: :rtype:
    """
    string = stypes.stringToCharP(string)
    templ = stypes.stringToCharP(templ)
    wstr = ctypes.c_char(wstr.encode(encoding = 'UTF-8'))
    wchr = ctypes.c_char(wchr.encode(encoding = 'UTF-8'))
    return libspice.matchw_c(string, templ, wstr, wchr)


#skiping for now maxd_c, odd as arguments must be parsed and not really important


#skiping for now maxi_c, odd as arguments must be parsed and not really important


def mequ(m1):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param m1:
    :return: :rtype:
    """
    m1 = stypes.listtodoublematrix(m1)
    mout = stypes.emptyDoubleMatrix()
    libspice.mequ_c(m1, mout)
    return stypes.matrixToList(mout)


def mequg(m1, nr, nc):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param m1:
    :param nr:
    :param nc:
    :return: :rtype:
    """
    m1 = stypes.listtodoublematrix(m1, x=nc, y=nr)
    mout = stypes.emptyDoubleMatrix(x=nc, y=nr)
    nc = ctypes.c_int(nc)
    nr = ctypes.c_int(nr)
    libspice.mequg_c(m1, nc, nr, mout)
    return stypes.matrixToList(mout)


#skiping for now mind_c, odd as arguments must be parsed and not really important


#skiping for now mini_c, odd as arguments must be parsed and not really important


def mtxm(m1, m2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param m1:
    :param m2:
    :return: :rtype:
    """
    m1 = stypes.listtodoublematrix(m1)
    m2 = stypes.listtodoublematrix(m2)
    mout = stypes.emptyDoubleMatrix()
    libspice.mtxm_c(m1, m2, mout)
    return stypes.matrixToList(mout)


def mtxmg(m1, m2, ncol1, nr1r2, ncol2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param m1:
    :param m2:
    :param ncol1:
    :param nr1r2:
    :param ncol2:
    :return: :rtype:
    """
    m1 = stypes.listtodoublematrix(m1, x=ncol1, y=nr1r2)
    m2 = stypes.listtodoublematrix(m2, x=ncol2, y=nr1r2)
    mout = stypes.emptyDoubleMatrix(x=ncol2, y=ncol1)
    ncol1 = ctypes.c_int(ncol1)
    nr1r2 = ctypes.c_int(nr1r2)
    ncol2 = ctypes.c_int(ncol2)
    libspice.mtxmg_c(m1, m2, ncol1, nr1r2, ncol2, mout)
    return stypes.matrixToList(mout)


def mtxv(m1, vin):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param m1:
    :param vin:
    :return: :rtype:
    """
    m1 = stypes.listtodoublematrix(m1)
    vin = stypes.toDoubleVector(vin)
    vout = stypes.emptyDoubleVector(3)
    libspice.mtxv_c(m1, vin, vout)
    return stypes.vectorToList(vout)


def mtxvg(m1, v2, ncol1, nr1r2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param m1:
    :param v2:
    :param ncol1:
    :param nr1r2:
    :return: :rtype:
    """
    m1 = stypes.listtodoublematrix(m1, x=ncol1, y=nr1r2)
    v2 = stypes.toDoubleVector(v2)
    ncol1 = ctypes.c_int(ncol1)
    nr1r2 = ctypes.c_int(nr1r2)
    vout = stypes.emptyDoubleVector(ncol1.value)
    libspice.mtxvg_c(m1, v2, ncol1, nr1r2, vout)
    return stypes.vectorToList(vout)


def mxm(m1, m2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param m1:
    :param m2:
    :return: :rtype:
    """
    m1 = stypes.listtodoublematrix(m1)
    m2 = stypes.listtodoublematrix(m2)
    mout = stypes.emptyDoubleMatrix()
    libspice.mxm_c(m1, m2, mout)
    return stypes.matrixToList(mout)


def mxmg(m1, m2, nrow1, ncol1, ncol2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param m1:
    :param m2:
    :param nrow1:
    :param ncol1:
    :param ncol2:
    :return: :rtype:
    """
    m1 = stypes.listtodoublematrix(m1, x=ncol1, y=nrow1)
    m2 = stypes.listtodoublematrix(m2, x=ncol2, y=ncol1)
    mout = stypes.emptyDoubleMatrix(x=ncol2, y=nrow1)
    nrow1 = ctypes.c_int(nrow1)
    ncol1 = ctypes.c_int(ncol1)
    ncol2 = ctypes.c_int(ncol2)
    libspice.mxmg_c(m1, m2, nrow1, ncol1, ncol2, mout)
    return stypes.matrixToList(mout)


def mxmt(m1, m2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param m1:
    :param m2:
    :return: :rtype:
    """
    m1 = stypes.listtodoublematrix(m1)
    m2 = stypes.listtodoublematrix(m2)
    mout = stypes.emptyDoubleMatrix()
    libspice.mxmt_c(m1, m2, mout)
    return stypes.matrixToList(mout)


def mxmtg(m1, m2, nrow1, nc1c2, nrow2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param m1:
    :param m2:
    :param nrow1:
    :param nc1c2:
    :param nrow2:
    :return: :rtype:
    """
    m1 = stypes.listtodoublematrix(m1, x=nc1c2, y=nrow1)
    m2 = stypes.listtodoublematrix(m2, x=nc1c2, y=nrow2)
    mout = stypes.emptyDoubleMatrix(x=nrow2, y=nrow1)
    nrow1 = ctypes.c_int(nrow1)
    nc1c2 = ctypes.c_int(nc1c2)
    nrow2 = ctypes.c_int(nrow2)
    libspice.mxmtg_c(m1, m2, nrow1, nc1c2, nrow2, mout)
    return stypes.matrixToList(mout)


def mxv(m1, vin):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param m1:
    :param vin:
    :return: :rtype:
    """
    m1 = stypes.listtodoublematrix(m1)
    vin = stypes.toDoubleVector(vin)
    vout = stypes.emptyDoubleVector(3)
    libspice.mxv_c(m1, vin, vout)
    return stypes.vectorToList(vout)


def mxvg(m1, v2, nrow1, nc1r2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param m1:
    :param v2:
    :param nrow1:
    :param nc1r2:
    :return: :rtype:
    """
    m1 = stypes.listtodoublematrix(m1, x=nc1r2, y=nrow1)
    v2 = stypes.toDoubleVector(v2)
    nrow1 = ctypes.c_int(nrow1)
    nc1r2 = ctypes.c_int(nc1r2)
    vout = stypes.emptyDoubleVector(nrow1.value)
    libspice.mxvg_c(m1, v2, nrow1, nc1r2, vout)
    return stypes.vectorToList(vout)

########################################################################################################################
# N


def namfrm(frname):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param frname:
    :return: :rtype:
    """
    frname = stypes.stringToCharP(frname)
    frcode = ctypes.c_int()
    libspice.namfrm_c(frname, ctypes.byref(frcode))
    return frcode.value


def ncpos(string, chars, start):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param string:
    :param chars:
    :param start:
    :return: :rtype:
    """
    string = stypes.stringToCharP(string)
    chars = stypes.stringToCharP(chars)
    start = ctypes.c_int(start)
    return libspice.ncpos_c(string, chars, start)


def ncposr(string, chars, start):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param string:
    :param chars:
    :param start:
    :return: :rtype:
    """
    string = stypes.stringToCharP(string)
    chars = stypes.stringToCharP(chars)
    start = ctypes.c_int(start)
    return libspice.ncposr_c(string, chars, start)


def nearpt(positn, a, b, c):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param positn:
    :param a:
    :param b:
    :param c:
    :return: :rtype:
    """
    positn = stypes.toDoubleVector(positn)
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    npoint = stypes.emptyDoubleVector(3)
    alt = ctypes.c_double()
    libspice.nearpt_c(positn, a, b, c, npoint, ctypes.byref(alt))
    return stypes.vectorToList(npoint), alt.value


def npedln(a, b, c, linept, linedr):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param a:
    :param b:
    :param c:
    :param linept:
    :param linedr:
    :return: :rtype:
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


def npelpt(point, ellips):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param point:
    :param ellips:
    :return: :rtype:
    """
    assert(isinstance(ellips, stypes.Ellipse))
    point = stypes.toDoubleVector(point)
    pnear = stypes.emptyDoubleVector(3)
    dist = ctypes.c_double()
    libspice.npelpt_c(point, ctypes.byref(ellips), pnear, ctypes.byref(dist))
    return stypes.vectorToList(pnear), dist.value


def nplnpt(linpt, lindir, point):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param linpt:
    :param lindir:
    :param point:
    :return: :rtype:
    """
    linpt = stypes.toDoubleVector(linpt)
    lindir = stypes.toDoubleVector(lindir)
    point = stypes.toDoubleVector(point)
    pnear = stypes.emptyDoubleVector(3)
    dist = ctypes.c_double()
    libspice.nplnpt_c(linpt, lindir, point, pnear, ctypes.byref(dist))
    return stypes.vectorToList(pnear), dist.value


def nvc2pl(normal, constant):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param normal:
    :param constant:
    :return: :rtype:
    """
    plane = stypes.Plane()
    normal = stypes.toDoubleVector(normal)
    constant = ctypes.c_double(constant)
    libspice.nvc2pl_c(normal, constant, ctypes.byref(plane))
    return plane


def nvp2pl(normal, point):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param normal:
    :param point:
    :return: :rtype:
    """
    normal = stypes.toDoubleVector(normal)
    point = stypes.toDoubleVector(point)
    plane = stypes.Plane()
    libspice.nvp2pl_c(normal, point, ctypes.byref(plane))
    return plane


########################################################################################################################
# O

def occult(target1, shape1, frame1, target2, shape2, frame2, abcorr, observer, et):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param target1:
    :param shape1:
    :param frame1:
    :param target2:
    :param shape2:
    :param frame2:
    :param abcorr:
    :param observer:
    :param et:
    :return: :rtype:
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
    libspice.occult_c(target1, shape1, frame1, target2, shape2, frame2, abcorr, observer, et, ctypes.byref(occult_code))
    return occult_code.value


def ordc(item, inset):
    #Todo: test ordc
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param item:
    :param inset:
    :return: :rtype:
    """
    assert isinstance(inset, stypes.SpiceCell)
    assert inset.is_char()
    assert isinstance(item, str)
    item = stypes.stringToCharP(item)
    return libspice.ordc_c(item, ctypes.byref(inset))


def ordd(item, inset):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param item:
    :param inset:
    :return: :rtype:
    """
    assert isinstance(inset, stypes.SpiceCell)
    assert inset.is_double()
    item = ctypes.c_double(item)
    return libspice.ordd_c(item, ctypes.byref(inset))


def ordi(item, inset):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param item:
    :param inset:
    :return: :rtype:
    """
    assert isinstance(inset, stypes.SpiceCell)
    assert inset.is_int()
    assert isinstance(item, int)
    item = ctypes.c_int(item)
    return libspice.ordi_c(item, ctypes.byref(inset))


def orderc(array, ndim=None):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param array:
    :param ndim:
    :return: :rtype:
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


def orderd(array, ndim=None):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param array:
    :param ndim:
    :return: :rtype:
    """
    if ndim is None:
        ndim = ctypes.c_int(len(array))
    else:
        ndim = ctypes.c_int(ndim)
    array = stypes.toDoubleVector(array)
    iorder = stypes.emptyIntVector(ndim)
    libspice.orderd_c(array, ndim, iorder)
    return stypes.vectorToList(iorder)


def orderi(array, ndim=None):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param array:
    :param ndim:
    :return: :rtype:
    """
    if ndim is None:
        ndim = ctypes.c_int(len(array))
    else:
        ndim = ctypes.c_int(ndim)
    array = stypes.toIntVector(array)
    iorder = stypes.emptyIntVector(ndim)
    libspice.orderi_c(array, ndim, iorder)
    return stypes.vectorToList(iorder)


def oscelt(state, et, mu):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param state:
    :param et:
    :param mu:
    :return: :rtype:
    """
    state = stypes.toDoubleVector(state)
    et = ctypes.c_double(et)
    mu = ctypes.c_double(mu)
    elts = stypes.emptyDoubleVector(8)
    libspice.oscelt_c(state, et, mu, elts)
    return stypes.vectorToList(elts)

########################################################################################################################
# P


def pckcov(pck, idcode, cover):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param pck:
    :param idcode:
    :param cover:
    """
    pck = stypes.stringToCharP(pck)
    idcode = ctypes.c_int(idcode)
    assert isinstance(cover, stypes.SpiceCell)
    assert cover.dtype == 1
    libspice.pckcov_c(pck, idcode, ctypes.byref(cover))


def pckfrm(pck, ids):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param pck:
    :param ids:
    """
    pck = stypes.stringToCharP(pck)
    assert isinstance(ids, stypes.SpiceCell)
    assert ids.dtype == 2
    libspice.pckfrm_c(pck, ctypes.byref(ids))


def pcklof(filename):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param filename:
    :return: :rtype:
    """
    filename = stypes.stringToCharP(filename)
    handle = ctypes.c_int()
    libspice.pcklof_c(filename, ctypes.byref(handle))
    return handle.value


def pckuof(handle):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    """
    handle = ctypes.c_int(handle)
    libspice.pckuof_c(handle)
    pass


def pcpool(name, cvals):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param name:
    :param cvals:
    """
    name = stypes.stringToCharP(name)
    lenvals = ctypes.c_int(len(max(cvals, key=len)) + 1)
    n = ctypes.c_int(len(cvals))
    cvals = stypes.listToCharArray(cvals, lenvals, n)
    libspice.pcpool_c(name, n, lenvals, cvals)


def pdpool(name, dvals):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param name:
    :param dvals:
    """
    name = stypes.stringToCharP(name)
    n = ctypes.c_int(len(dvals))
    dvals = stypes.toDoubleVector(dvals)
    libspice.pdpool_c(name, n, dvals)


def pgrrec(body, lon, lat, alt, re, f):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param body:
    :param lon:
    :param lat:
    :param alt:
    :param re:
    :param f:
    :return: :rtype:
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


def phaseq(et, target, illmn, obsrvr, abcorr):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param et:
    :param target:
    :param illmn:
    :param obsrvr:
    :param abcorr:
    :return: :rtype:
    """
    et = ctypes.c_double(et)
    target = stypes.stringToCharP(target)
    illmn = stypes.stringToCharP(illmn)
    obsrvr = stypes.stringToCharP(obsrvr)
    abcorr = stypes.stringToCharP(abcorr)
    return libspice.phaseq_c(et, target, illmn, obsrvr, abcorr)


def pi():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    :return: :rtype:
    """
    return libspice.pi_c()


def pipool(name, ivals):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param name:
    :param ivals:
    """
    name = stypes.stringToCharP(name)
    n = ctypes.c_int(len(ivals))
    ivals = stypes.toIntVector(ivals)
    libspice.pipool_c(name, n, ivals)


def pjelpl(elin, plane):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param elin:
    :param plane:
    :return: :rtype:
    """
    assert(isinstance(elin, stypes.Ellipse))
    assert(isinstance(plane, stypes.Plane))
    elout = stypes.Ellipse()
    libspice.pjelpl_c(ctypes.byref(elin), ctypes.byref(plane), ctypes.byref(elout))
    return elout


def pl2nvc(plane):
    #Works! we have working planes!
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param plane:
    :return: :rtype:
    """
    assert(isinstance(plane, stypes.Plane))
    normal = stypes.emptyDoubleVector(3)
    constant = ctypes.c_double()
    libspice.pl2nvc_c(ctypes.byref(plane), normal, ctypes.byref(constant))
    return stypes.vectorToList(normal), constant.value


def pl2nvp(plane):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param plane:
    :return: :rtype:
    """
    assert(isinstance(plane, stypes.Plane))
    normal = stypes.emptyDoubleVector(3)
    point = stypes.emptyDoubleVector(3)
    libspice.pl2nvp_c(ctypes.byref(plane), normal, point)
    return stypes.vectorToList(normal), stypes.vectorToList(point)


def pl2psv(plane):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param plane:
    :return: :rtype:
    """
    assert (isinstance(plane, stypes.Plane))
    point = stypes.emptyDoubleVector(3)
    span1 = stypes.emptyDoubleVector(3)
    span2 = stypes.emptyDoubleVector(3)
    libspice.pl2psv_c(ctypes.byref(plane), point, span1, span2)
    return stypes.vectorToList(point), stypes.vectorToList(span1), stypes.vectorToList(span2)


def pos(string, substr, start):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param string:
    :param substr:
    :param start:
    :return: :rtype:
    """
    string = stypes.stringToCharP(string)
    substr = stypes.stringToCharP(substr)
    start = ctypes.c_int(start)
    return libspice.pos_c(string, substr, start)


def posr(string, substr, start):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param string:
    :param substr:
    :param start:
    :return: :rtype:
    """
    string = stypes.stringToCharP(string)
    substr = stypes.stringToCharP(substr)
    start = ctypes.c_int(start)
    return libspice.posr_c(string, substr, start)


#prompt, skip for no as this is not really an important function for python users


def prop2b(gm, pvinit, dt):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param gm:
    :param pvinit:
    :param dt:
    :return: :rtype:
    """
    gm = ctypes.c_double(gm)
    pvinit = stypes.toDoubleVector(pvinit)
    dt = ctypes.c_double(dt)
    pvprop = stypes.emptyDoubleVector(6)
    libspice.prop2b_c(gm, pvinit, dt, pvprop)
    return stypes.vectorToList(pvprop)


def prsdp(string):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param string:
    :return: :rtype:
    """
    string = stypes.stringToCharP(string)
    dpval = ctypes.c_double()
    libspice.prsdp_c(string, ctypes.byref(dpval))
    return dpval.value


def prsint(string):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param string:
    :return: :rtype:
    """
    string = stypes.stringToCharP(string)
    intval = ctypes.c_int()
    libspice.prsint_c(string, ctypes.byref(intval))
    return intval.value


def psv2pl(point, span1, span2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param point:
    :param span1:
    :param span2:
    :return: :rtype:
    """
    point = stypes.toDoubleVector(point)
    span1 = stypes.toDoubleVector(span1)
    span2 = stypes.toDoubleVector(span2)
    plane = stypes.Plane()
    libspice.psv2pl_c(point, span1, span2, ctypes.byref(plane))
    return plane


# skip putcml, is this really needed for python users?


def pxform(fromstr, tostr, et):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param fromstr:
    :param tostr:
    :param et:
    :return: :rtype:
    """
    et = ctypes.c_double(et)
    tostr = stypes.stringToCharP(tostr)
    fromstr = stypes.stringToCharP(fromstr)
    rotatematrix = stypes.emptyDoubleMatrix()
    libspice.pxform_c(fromstr, tostr, et, rotatematrix)
    return stypes.matrixToList(rotatematrix)


def pxfrm2(frame_from, frame_to, etfrom, etto):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param frame_from:
    :param frame_to:
    :param etfrom:
    :param etto:
    :return: :rtype:
    """
    frame_from = stypes.stringToCharP(frame_from)
    frame_to = stypes.stringToCharP(frame_to)
    etfrom = ctypes.c_double(etfrom)
    etto = ctypes.c_double(etto)
    outmatrix = stypes.emptyDoubleMatrix()
    libspice.pxfrm2_c(frame_from, frame_to, etfrom, etto, outmatrix)
    return stypes.matrixToList(outmatrix)

########################################################################################################################
# Q


def q2m(q):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param q:
    :return: :rtype:
    """
    q = stypes.toDoubleVector(q)
    mout = stypes.emptyDoubleMatrix()
    libspice.q2m_c(q, mout)
    return stypes.matrixToList(mout)


def qcktrc(tracelen):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param tracelen:
    :return: :rtype:
    """
    tracestr = stypes.stringToCharP(tracelen)
    tracelen = ctypes.c_int(tracelen)
    libspice.qcktrc_c(tracelen, tracestr)
    return stypes.toPythonString(tracestr)


def qdq2av(q, dq):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param q:
    :param dq:
    :return: :rtype:
    """
    q = stypes.toDoubleVector(q)
    dq = stypes.toDoubleVector(dq)
    vout = stypes.emptyDoubleVector(3)
    libspice.qdq2av_c(q, dq, vout)
    return stypes.vectorToList(vout)


def qxq(q1, q2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param q1:
    :param q2:
    :return: :rtype:
    """
    q1 = stypes.toDoubleVector(q1)
    q2 = stypes.toDoubleVector(q2)
    vout = stypes.emptyDoubleVector(4)
    libspice.qxq_c(q1, q2, vout)
    return stypes.vectorToList(vout)

########################################################################################################################
# R


def radrec(inrange, re, dec):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param inrange:
    :param re:
    :param dec:
    :return: :rtype:
    """
    inrange = ctypes.c_double(inrange)
    re = ctypes.c_double(re)
    dec = ctypes.c_double(dec)
    rectan = stypes.emptyDoubleVector(3)
    libspice.radrec_c(inrange, re, dec, rectan)
    return stypes.vectorToList(rectan)


def rav2xf(rot, av):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param rot:
    :param av:
    :return: :rtype:
    """
    rot = stypes.toDoubleMatrix(rot)
    av = stypes.toDoubleVector(av)
    xform = stypes.emptyDoubleMatrix(x=6, y=6)
    libspice.rav2xf_c(rot, av, xform)
    return stypes.matrixToList(xform)


def raxisa(matrix):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param matrix:
    :return: :rtype:
    """
    matrix = stypes.listtodoublematrix(matrix)
    axis = stypes.emptyDoubleVector(3)
    angle = ctypes.c_double()
    libspice.raxisa_c(matrix, axis, ctypes.byref(angle))
    return stypes.vectorToList(axis), angle.value


def rdtext(file, lenout):  # pragma: no cover
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param file:
    :param lenout:
    :return: :rtype:
    """
    file = stypes.stringToCharP(file)
    line = stypes.stringToCharP(lenout)
    lenout = ctypes.c_int(lenout)
    eof = ctypes.c_bool()
    libspice.rdtext_c(file, lenout, line, ctypes.byref(eof))
    return stypes.toPythonString(line), eof.value


def reccyl(rectan):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param rectan:
    :return: :rtype:
    """
    rectan = stypes.toDoubleVector(rectan)
    radius = ctypes.c_double(0)
    lon = ctypes.c_double(0)
    z = ctypes.c_double(0)
    libspice.reccyl_c(rectan, ctypes.byref(radius), ctypes.byref(lon), ctypes.byref(z))
    return radius.value, lon.value, z.value


def reclat(rectan):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param rectan:
    :return: :rtype:
    """
    rectan = stypes.toDoubleVector(rectan)
    radius = ctypes.c_double(0)
    longitude = ctypes.c_double(0)
    latitude = ctypes.c_double(0)
    libspice.reclat_c(rectan, ctypes.byref(radius), ctypes.byref(longitude), ctypes.byref(latitude))
    return radius.value, longitude.value, latitude.value


def recgeo(rectan, re, f):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param rectan:
    :param re:
    :param f:
    :return: :rtype:
    """
    rectan = stypes.toDoubleVector(rectan)
    re = ctypes.c_double(re)
    f = ctypes.c_double(f)
    longitude = ctypes.c_double(0)
    latitude = ctypes.c_double(0)
    alt = ctypes.c_double(0)
    libspice.recgeo_c(rectan, re, f, ctypes.byref(longitude), ctypes.byref(latitude), ctypes.byref(alt))
    return longitude.value, latitude.value, alt.value


def recpgr(body, rectan, re, f):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param body:
    :param rectan:
    :param re:
    :param f:
    :return: :rtype:
    """
    body = stypes.stringToCharP(body)
    rectan = stypes.toDoubleVector(rectan)
    re = ctypes.c_double(re)
    f = ctypes.c_double(f)
    lon = ctypes.c_double()
    lat = ctypes.c_double()
    alt = ctypes.c_double()
    libspice.recpgr_c(body, rectan, re, f, ctypes.byref(lon), ctypes.byref(lat), ctypes.byref(alt))
    return lon.value, lat.value, alt.value


def recrad(rectan):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param rectan:
    :return: :rtype:
    """
    rectan = stypes.toDoubleVector(rectan)
    outrange = ctypes.c_double()
    ra = ctypes.c_double()
    dec = ctypes.c_double()
    libspice.recrad_c(rectan, ctypes.byref(outrange), ctypes.byref(ra), ctypes.byref(dec))
    return outrange.value, ra.value, dec.value


def recsph(rectan):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param rectan:
    :return: :rtype:
    """
    rectan = stypes.toDoubleVector(rectan)
    r = ctypes.c_double()
    colat = ctypes.c_double()
    lon = ctypes.c_double()
    libspice.recsph_c(rectan, ctypes.byref(r), ctypes.byref(colat), ctypes.byref(lon))
    return r.value, colat.value, lon.value


def removc(item, inset):
    #Todo: test removc
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param item:
    :param inset:
    """
    assert isinstance(inset, stypes.SpiceCell)
    item = stypes.stringToCharP(item)
    libspice.removc_c(item, ctypes.byref(inset))
    pass


def removd(item, inset):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param item:
    :param inset:
    """
    assert isinstance(inset, stypes.SpiceCell)
    item = ctypes.c_double(item)
    libspice.removd_c(item, ctypes.byref(inset))
    pass


def removi(item, inset):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param item:
    :param inset:
    """
    assert isinstance(inset, stypes.SpiceCell)
    item = ctypes.c_int(item)
    libspice.removi_c(item, ctypes.byref(inset))
    pass


def reordc(iorder, ndim, lenvals, array):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param iorder:
    :param ndim:
    :param lenvals:
    :param array:
    :return: :rtype:
    """
    iorder = stypes.toIntVector(iorder)
    array = stypes.listToCharArray(array)
    ndim = ctypes.c_int(ndim)
    lenvals = ctypes.c_int(lenvals)
    libspice.reordc_c(iorder, ndim, lenvals, array)
    return [stypes.toPythonString(x.value) for x in array]


def reordd(iorder, ndim, array):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param iorder:
    :param ndim:
    :param array:
    :return: :rtype:
    """
    iorder = stypes.toIntVector(iorder)
    ndim = ctypes.c_int(ndim)
    array = stypes.toDoubleVector(array)
    libspice.reordd_c(iorder, ndim, array)
    return stypes.vectorToList(array)


def reordi(iorder, ndim, array):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param iorder:
    :param ndim:
    :param array:
    :return: :rtype:
    """
    iorder = stypes.toIntVector(iorder)
    ndim = ctypes.c_int(ndim)
    array = stypes.toIntVector(array)
    libspice.reordi_c(iorder, ndim, array)
    return stypes.vectorToList(array)


def reordl(iorder, ndim, array):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param iorder:
    :param ndim:
    :param array:
    :return: :rtype:
    """
    iorder = stypes.toIntVector(iorder)
    ndim = ctypes.c_int(ndim)
    array = stypes.toBoolVector(array)
    libspice.reordl_c(iorder, ndim, array)
    return stypes.vectorToList(array)


def repmc(instr, marker, value, lenout=None):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param instr:
    :param marker:
    :param value:
    :param lenout:
    :return: :rtype:
    """
    if lenout is None:
        lenout = ctypes.c_int(len(instr) + len(value) + len(marker) + 15)
    instr = stypes.stringToCharP(instr)
    marker = stypes.stringToCharP(marker)
    value = stypes.stringToCharP(value)
    out = stypes.stringToCharP(lenout)
    libspice.repmc_c(instr, marker, value, lenout, out)
    return stypes.toPythonString(out)


def repmct(instr, marker, value, repcase, lenout=None):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param instr:
    :param marker:
    :param value:
    :param repcase:
    :param lenout:
    :return: :rtype:
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


def repmd(instr, marker, value, sigdig):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param instr:
    :param marker:
    :param value:
    :param sigdig:
    :return: :rtype:
    """
    lenout = ctypes.c_int(len(instr) + len(marker) + 15)
    instr = stypes.stringToCharP(instr)
    marker = stypes.stringToCharP(marker)
    value = ctypes.c_double(value)
    sigdig = ctypes.c_int(sigdig)
    out = stypes.stringToCharP(lenout)
    libspice.repmd_c(instr, marker, value, sigdig, lenout, out)
    return stypes.toPythonString(out)


def repmf(instr, marker, value, sigdig, informat, lenout=None):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param instr:
    :param marker:
    :param value:
    :param sigdig:
    :param informat:
    :param lenout:
    :return: :rtype:
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


def repmi(instr, marker, value, lenout=None):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param instr:
    :param marker:
    :param value:
    :param lenout:
    :return: :rtype:
    """
    if lenout is None:
        lenout = ctypes.c_int(len(instr) + len(marker) + 15)
    instr = stypes.stringToCharP(instr)
    marker = stypes.stringToCharP(marker)
    value = ctypes.c_int(value)
    out = stypes.stringToCharP(lenout)
    libspice.repmi_c(instr, marker, value, lenout, out)
    return stypes.toPythonString(out)


def repmot(instr, marker, value, repcase, lenout=None):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param instr:
    :param marker:
    :param value:
    :param repcase:
    :param lenout:
    :return: :rtype:
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
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    """
    libspice.reset_c()
    pass


def return_c():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    :return: :rtype:
    """
    return libspice.return_c()


def rotate(angle, iaxis):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param angle:
    :param iaxis:
    :return: :rtype:
    """
    angle = ctypes.c_double(angle)
    iaxis = ctypes.c_int(iaxis)
    mout = stypes.emptyDoubleMatrix()
    libspice.rotate_c(angle, iaxis, mout)
    return stypes.matrixToList(mout)


def rotmat(m1, angle, iaxis):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param m1:
    :param angle:
    :param iaxis:
    :return: :rtype:
    """
    m1 = stypes.listtodoublematrix(m1)
    angle = ctypes.c_double(angle)
    iaxis = ctypes.c_int(iaxis)
    mout = stypes.emptyDoubleMatrix()
    libspice.rotmat_c(m1, angle, iaxis, mout)
    return stypes.matrixToList(mout)


def rotvec(v1, angle, iaxis):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v1:
    :param angle:
    :param iaxis:
    :return: :rtype:
    """
    v1 = stypes.toDoubleVector(v1)
    angle = ctypes.c_double(angle)
    iaxis = ctypes.c_int(iaxis)
    vout = stypes.emptyDoubleVector(3)
    libspice.rotvec_c(v1, angle, iaxis, vout)
    return stypes.vectorToList(vout)


def rpd():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    :return: :rtype:
    """
    return libspice.rpd_c()


def rquad(a, b, c):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param a:
    :param b:
    :param c:
    :return: :rtype:
    """
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    root1 = stypes.emptyDoubleVector(2)
    root2 = stypes.emptyDoubleVector(2)
    libspice.rquad_c(a, b, c, root1, root2)
    return stypes.vectorToList(root1), stypes.vectorToList(root2)

########################################################################################################################
# S


def saelgv(vec1, vec2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param vec1:
    :param vec2:
    :return: :rtype:
    """
    vec1 = stypes.toDoubleVector(vec1)
    vec2 = stypes.toDoubleVector(vec2)
    smajor = stypes.emptyDoubleVector(3)
    sminor = stypes.emptyDoubleVector(3)
    libspice.saelgv_c(vec1, vec2, smajor, sminor)
    return stypes.vectorToList(smajor), stypes.vectorToList(sminor)


def scard(incard, cell):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param incard:
    :param cell:
    :return: :rtype:
    """
    assert isinstance(cell, stypes.SpiceCell)
    incard = ctypes.c_int(incard)
    libspice.scard_c(incard, ctypes.byref(cell))
    return cell


def scdecd(sc, sclkdp, lenout, MXPART=None):
    #todo: figure out how to use mxpart, and test scdecd
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param sc:
    :param sclkdp:
    :param lenout:
    :param MXPART:
    :return: :rtype:
    """
    sc = ctypes.c_int(sc)
    sclkdp = ctypes.c_double(sclkdp)
    sclkch = stypes.stringToCharP(" " * lenout)
    lenout = ctypes.c_int(lenout)
    libspice.scdecd_c(sc, sclkdp, lenout, sclkch)
    return stypes.toPythonString(sclkch)


def sce2c(sc, et):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param sc:
    :param et:
    :return: :rtype:
    """
    sc = ctypes.c_int(sc)
    et = ctypes.c_double(et)
    sclkdp = ctypes.c_double()
    libspice.sce2c_c(sc, et, ctypes.byref(sclkdp))
    return sclkdp.value


def sce2s(sc, et, lenout):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param sc:
    :param et:
    :param lenout:
    :return: :rtype:
    """
    sc = ctypes.c_int(sc)
    et = ctypes.c_double(et)
    sclkch = stypes.stringToCharP(" " * lenout)
    lenout = ctypes.c_int(lenout)
    libspice.sce2s_c(sc, et, lenout, sclkch)
    return stypes.toPythonString(sclkch)


def sce2t(sc, et):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param sc:
    :param et:
    :return: :rtype:
    """
    sc = ctypes.c_int(sc)
    et = ctypes.c_double(et)
    sclkdp = ctypes.c_double()
    libspice.sce2t_c(sc, et, ctypes.byref(sclkdp))
    return sclkdp.value


def scencd(sc, sclkch, MXPART=None):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param sc:
    :param sclkch:
    :param MXPART:
    :return: :rtype:
    """
    sc = ctypes.c_int(sc)
    sclkch = stypes.stringToCharP(sclkch)
    sclkdp = ctypes.c_double()
    libspice.scencd_c(sc, sclkch, ctypes.byref(sclkdp))
    return sclkdp.value


def scfmt(sc, ticks, lenout):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param sc:
    :param ticks:
    :param lenout:
    :return: :rtype:
    """
    sc = ctypes.c_int(sc)
    ticks = ctypes.c_double(ticks)
    clkstr = stypes.stringToCharP(lenout)
    lenout = ctypes.c_int(lenout)
    libspice.scfmt_c(sc, ticks, lenout, clkstr)
    return stypes.toPythonString(clkstr)


def scpart(sc):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param sc:
    :return: :rtype:
    """
    sc = ctypes.c_int(sc)
    nparts = ctypes.c_int()
    pstart = stypes.emptyDoubleVector(9999)
    pstop = stypes.emptyDoubleVector(9999)
    libspice.scpart_c(sc, nparts, pstart, pstop)
    return stypes.vectorToList(pstart)[0:nparts.value], stypes.vectorToList(pstop)[0:nparts.value]


def scs2e(sc, sclkch):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param sc:
    :param sclkch:
    :return: :rtype:
    """
    sc = ctypes.c_int(sc)
    sclkch = stypes.stringToCharP(sclkch)
    et = ctypes.c_double()
    libspice.scs2e_c(sc, sclkch, ctypes.byref(et))
    return et.value


def sct2e(sc, sclkdp):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param sc:
    :param sclkdp:
    :return: :rtype:
    """
    sc = ctypes.c_int(sc)
    sclkdp = ctypes.c_double(sclkdp)
    et = ctypes.c_double()
    libspice.sct2e_c(sc, sclkdp, ctypes.byref(et))
    return et.value


def sctiks(sc, clkstr):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param sc:
    :param clkstr:
    :return: :rtype:
    """
    sc = ctypes.c_int(sc)
    clkstr = stypes.stringToCharP(clkstr)
    ticks = ctypes.c_double()
    libspice.sctiks_c(sc, clkstr, ctypes.byref(ticks))
    return ticks.value


def sdiff(a, b):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param a:
    :param b:
    :return: :rtype: :raise NotImplementedError:
    """
    assert isinstance(a, stypes.SpiceCell)
    assert isinstance(b, stypes.SpiceCell)
    assert a.dtype == b.dtype
    assert a.dtype == 0 or a.dtype == 1 or a.dtype == 2
    if a.dtype is 0:
        c = stypes.SPICECHAR_CELL(a.size, a.length)
    if a.dtype is 1:
        c = stypes.SPICEDOUBLE_CELL(a.size)
    elif a.dtype is 2:
        c = stypes.SPICEINT_CELL(a.size)
    else:
        raise NotImplementedError
    libspice.sdiff_c(ctypes.byref(a), ctypes.byref(b), ctypes.byref(c))
    return c


def set_c(a, op, b):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param a:
    :type a:
    :param op:
    :type op:
    :param b:
    :type b:
    :return:
    :rtype:
    """
    assert isinstance(a, stypes.SpiceCell)
    assert isinstance(b, stypes.SpiceCell)
    assert a.dtype == b.dtype
    assert isinstance(op, str)
    op = stypes.stringToCharP(op)
    return libspice.set_c(ctypes.byref(a), op, ctypes.byref(b))


def setmsg(message):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param message:
    """
    message = stypes.stringToCharP(message)
    libspice.setmsg_c(message)
    pass


def shellc(ndim, lenvals, array):
    #This works! looks like this is a mutable 2d char array
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param ndim:
    :param lenvals:
    :param array:
    :return: :rtype:
    """
    array = stypes.listToCharArray(array, xLen=lenvals, yLen=ndim)
    ndim = ctypes.c_int(ndim)
    lenvals = ctypes.c_int(lenvals)
    libspice.shellc_c(ndim, lenvals, ctypes.byref(array))
    return stypes.vectorToList(array)


def shelld(ndim, array):
    # Works!, use this as example for "I/O" parameters
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param ndim:
    :param array:
    :return: :rtype:
    """
    array = stypes.toDoubleVector(array)
    ndim = ctypes.c_int(ndim)
    libspice.shelld_c(ndim, ctypes.cast(array, ctypes.POINTER(ctypes.c_double)))
    return stypes.vectorToList(array)


def shelli(ndim, array):
    # Works!, use this as example for "I/O" parameters
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param ndim:
    :param array:
    :return: :rtype:
    """
    array = stypes.toIntVector(array)
    ndim = ctypes.c_int(ndim)
    libspice.shelli_c(ndim, ctypes.cast(array, ctypes.POINTER(ctypes.c_int)))
    return stypes.vectorToList(array)


def sigerr(message):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param message:
    """
    message = stypes.stringToCharP(message)
    libspice.sigerr_c(message)
    pass


def sincpt(method, target, et, fixref, abcorr, obsrvr, dref, dvec):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param method:
    :param target:
    :param et:
    :param fixref:
    :param abcorr:
    :param obsrvr:
    :param dref:
    :param dvec:
    :return: :rtype:
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
    libspice.sincpt_c(method, target, et, fixref, abcorr, obsrvr, dref, dvec, spoint, ctypes.byref(trgepc), srfvec, ctypes.byref(found))
    return stypes.vectorToList(spoint), trgepc.value, stypes.vectorToList(srfvec), found.value


def size(cell):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param cell:
    :return: :rtype:
    """
    assert isinstance(cell, stypes.SpiceCell)
    return libspice.size_c(ctypes.byref(cell))


def spd():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    :return: :rtype:
    """
    return libspice.spd_c()


def sphcyl(radius, colat, slon):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param radius:
    :param colat:
    :param slon:
    :return: :rtype:
    """
    radius = ctypes.c_double(radius)
    colat = ctypes.c_double(colat)
    slon = ctypes.c_double(slon)
    r = ctypes.c_double()
    lon = ctypes.c_double()
    z = ctypes.c_double()
    libspice.sphcyl_c(radius, colat, slon, ctypes.byref(r), ctypes.byref(lon), ctypes.byref(z))
    return r.value, lon.value, z.value


def sphlat(r, colat, lons):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param r:
    :param colat:
    :param lons:
    :return: :rtype:
    """
    r = ctypes.c_double(r)
    colat = ctypes.c_double(colat)
    lons = ctypes.c_double(lons)
    radius = ctypes.c_double()
    lon = ctypes.c_double()
    lat = ctypes.c_double()
    libspice.sphcyl_c(r, colat, lons, ctypes.byref(radius), ctypes.byref(lon), ctypes.byref(lat))
    return radius.value, lon.value, lat.value


def sphrec(r, colat, lon):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param r:
    :param colat:
    :param lon:
    :return: :rtype:
    """
    r = ctypes.c_double(r)
    colat = ctypes.c_double(colat)
    lon = ctypes.c_double(lon)
    rectan = stypes.emptyDoubleVector(3)
    libspice.sphrec_c(r, colat, lon, rectan)
    return stypes.vectorToList(rectan)


def spkacs(targ, et, ref, abcorr, obs):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param targ:
    :param et:
    :param ref:
    :param abcorr:
    :param obs:
    :return: :rtype:
    """
    targ = ctypes.c_int(targ)
    et = ctypes.c_double(et)
    ref = stypes.stringToCharP(ref)
    abcorr = stypes.stringToCharP(abcorr)
    obs = ctypes.c_int(obs)
    starg = stypes.emptyDoubleVector(6)
    lt = ctypes.c_double()
    dlt = ctypes.c_double()
    libspice.spkacs_c(targ, et, ref, abcorr, obs, starg, ctypes.byref(lt), ctypes.byref(dlt))
    return stypes.vectorToList(starg), lt.value, dlt.value


def spkapo(targ, et, ref, sobs, abcorr):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param targ:
    :param et:
    :param ref:
    :param sobs:
    :param abcorr:
    :return: :rtype:
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


def spkapp(targ, et, ref, sobs, abcorr):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param targ:
    :param et:
    :param ref:
    :param sobs:
    :param abcorr:
    :return: :rtype:
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


def spkaps(targ, et, ref, abcorr, stobs, accobs):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param targ:
    :param et:
    :param ref:
    :param abcorr:
    :param stobs:
    :param accobs:
    :return: :rtype:
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
    libspice.spkaps_c(targ, et, ref, abcorr, stobs, accobs, starg, ctypes.byref(lt), ctypes.byref(dlt))
    return stypes.vectorToList(starg), lt.value, dlt.value


def spk14a(handle, ncsets, coeffs, epochs):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    :param ncsets:
    :param coeffs:
    :param epochs:
    """
    handle = ctypes.c_int(handle)
    ncsets = ctypes.c_int(ncsets)
    coeffs = stypes.toDoubleVector(coeffs)
    epochs = stypes.toDoubleVector(epochs)
    libspice.spk14a_c(handle, ncsets, coeffs, epochs)
    pass


def spk14b(handle, segid, body, center, framename, first, last, chbdeg):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    :param segid:
    :param body:
    :param center:
    :param framename:
    :param first:
    :param last:
    :param chbdeg:
    """
    handle = ctypes.c_int(handle)
    segid = stypes.stringToCharP(segid)
    body = ctypes.c_int(body)
    center = ctypes.c_int(center)
    framename = stypes.stringToCharP(framename)
    first = ctypes.c_double(first)
    last = ctypes.c_double(last)
    chbdeg = ctypes.c_int(chbdeg)
    libspice.spk14b_c(handle, segid, body, center, framename, first, last, chbdeg)
    pass


def spk14e(handle):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    """
    handle = ctypes.c_int(handle)
    libspice.spk14e_c(handle)
    pass


def spkcls(handle):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    """
    handle = ctypes.c_int(handle)
    libspice.spkcls_c(handle)
    pass


def spkcov(spk, idcode, cover):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param spk:
    :param idcode:
    :param cover:
    """
    spk = stypes.stringToCharP(spk)
    idcode = ctypes.c_int(idcode)
    assert isinstance(cover, stypes.SpiceCell)
    assert cover.dtype == 1
    libspice.spkcov_c(spk, idcode, ctypes.byref(cover))


def spkcpo(target, et, outref, refloc, abcorr, obspos, obsctr, obsref):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param target:
    :param et:
    :param outref:
    :param refloc:
    :param abcorr:
    :param obspos:
    :param obsctr:
    :param obsref:
    :return: :rtype:
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
    libspice.spkcpo_c(target, et, outref, refloc, abcorr, obspos, obsctr, obsref, state, ctypes.byref(lt))
    return stypes.vectorToList(state), lt.value


def spkcpt(trgpos, trgctr, trgref, et, outref, refloc, abcorr, obsrvr):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param trgpos:
    :param trgctr:
    :param trgref:
    :param et:
    :param outref:
    :param refloc:
    :param abcorr:
    :param obsrvr:
    :return: :rtype:
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
    libspice.spkcpt_c(trgpos, trgctr, trgref, et, outref, refloc, abcorr, obsrvr, state, ctypes.byref(lt))
    return stypes.vectorToList(state), lt.value


def spkcvo(target, et, outref, refloc, abcorr, obssta, obsepc, obsct, obsref):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param target:
    :param et:
    :param outref:
    :param refloc:
    :param abcorr:
    :param obssta:
    :param obsepc:
    :param obsct:
    :param obsref:
    :return: :rtype:
    """
    target = stypes.stringToCharP(target)
    et = ctypes.c_double(et)
    outref = stypes.stringToCharP(outref)
    refloc = stypes.stringToCharP(refloc)
    abcorr = stypes.stringToCharP(abcorr)
    obssta = stypes.toDoubleVector(obssta)
    obsepc = ctypes.c_double(obsepc)
    obsct = stypes.stringToCharP(obsct)
    obsref = stypes.stringToCharP(obsref)
    state = stypes.emptyDoubleVector(6)
    lt = ctypes.c_double()
    libspice.spkcvo_c(target, et, outref, refloc, abcorr, obssta, obsepc, obsct, obsref, state, ctypes.byref(lt))
    return stypes.vectorToList(state), lt.value


def spkcvt(trgsta, trgepc, trgctr, trgref, et, outref, refloc, abcorr, obsrvr):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param trgsta:
    :param trgepc:
    :param trgctr:
    :param trgref:
    :param et:
    :param outref:
    :param refloc:
    :param abcorr:
    :param obsrvr:
    :return: :rtype:
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
    libspice.spkcvt_c(trgpos, trgepc, trgctr, trgref, et, outref, refloc, abcorr, obsrvr, state, ctypes.byref(lt))
    return stypes.vectorToList(state), lt.value


def spkez(targ, et, ref, abcorr, obs):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param targ:
    :param et:
    :param ref:
    :param abcorr:
    :param obs:
    :return: :rtype:
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


def spkezp(targ, et, ref, abcorr, obs):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param targ:
    :param et:
    :param ref:
    :param abcorr:
    :param obs:
    :return: :rtype:
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


def spkezr(targ, et, ref, abcorr, obs):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param targ:
    :param et:
    :param ref:
    :param abcorr:
    :param obs:
    :return: :rtype:
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


def spkgeo(targ, et, ref, obs):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param targ:
    :param et:
    :param ref:
    :param obs:
    :return: :rtype:
    """
    targ = ctypes.c_int(targ)
    et = ctypes.c_double(et)
    ref = stypes.stringToCharP(ref)
    obs = ctypes.c_int(obs)
    state = stypes.emptyDoubleVector(6)
    lt = ctypes.c_double()
    libspice.spkgeo_c(targ, et, ref, obs, state, ctypes.byref(lt))
    return stypes.vectorToList(state), lt.value


def spkgps(targ, et, ref, obs):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param targ:
    :param et:
    :param ref:
    :param obs:
    :return: :rtype:
    """
    targ = ctypes.c_int(targ)
    et = ctypes.c_double(et)
    ref = stypes.stringToCharP(ref)
    obs = ctypes.c_int(obs)
    position = stypes.emptyDoubleVector(3)
    lt = ctypes.c_double()
    libspice.spkgps_c(targ, et, ref, obs, position, ctypes.byref(lt))
    return stypes.vectorToList(position), lt.value


def spklef(filename):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param filename:
    :return: :rtype:
    """
    filename = stypes.stringToCharP(filename)
    handle = ctypes.c_int()
    libspice.spklef_c(filename, ctypes.byref(handle))
    return handle.value


def spkltc(targ, et, ref, abcorr, stobs):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param targ:
    :param et:
    :param ref:
    :param abcorr:
    :param stobs:
    :return: :rtype:
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
    libspice.spkltc_c(targ, et, ref, abcorr, stobs, starg, ctypes.byref(lt), ctypes.byref(dlt))
    return stypes.vectorToList(starg), lt.value, dlt.value


def spkobj(spk, ids):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param spk:
    :param ids:
    """
    spk = stypes.stringToCharP(spk)
    assert isinstance(ids, stypes.SpiceCell)
    assert ids.dtype == 2
    libspice.spkobj_c(spk, ctypes.byref(ids))


def spkopa(filename):
    #Todo: test spkopa
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param filename:
    :return: :rtype:
    """
    filename = stypes.stringToCharP(filename)
    handle = ctypes.c_int()
    libspice.spkopa_c(filename, ctypes.byref(handle))
    return handle.value


def spkopn(filename, ifname, ncomch):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param filename:
    :param ifname:
    :param ncomch:
    :return: :rtype:
    """
    filename = stypes.stringToCharP(filename)
    ifname = stypes.stringToCharP(ifname)
    ncomch = ctypes.c_int(ncomch)
    handle = ctypes.c_int()
    libspice.spkopn_c(filename, ifname, ncomch, ctypes.byref(handle))
    return handle.value


def spkpds(body, center, framestr, typenum, first, last):
    #Todo: test spkpds
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param body:
    :param center:
    :param framestr:
    :param typenum:
    :param first:
    :param last:
    :return: :rtype:
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


def spkpos(targ, et, ref, abcorr, obs):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param targ:
    :param et:
    :param ref:
    :param abcorr:
    :param obs:
    :return: :rtype:
    """
    if hasattr(et, "__iter__"):
        vlen = len(et)
        positions = numpy.zeros((vlen, 3), dtype=numpy.float)
        times = numpy.zeros(vlen, dtype=numpy.float)
        for (index, time) in enumerate(et):
            positions[index], times[index] = spkpos(targ, time, ref, abcorr, obs)
        return positions, times
    targ = stypes.stringToCharP(targ)
    ref = stypes.stringToCharP(ref)
    abcorr = stypes.stringToCharP(abcorr)
    obs = stypes.stringToCharP(obs)
    ptarg = stypes.emptyDoubleVector(3)
    lt = ctypes.c_double()
    libspice.spkpos_c(targ, et, ref, abcorr, obs, ptarg, ctypes.byref(lt))
    return stypes.vectorToList(ptarg), lt.value


def spkpvn(handle, descr, et):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    :param descr:
    :param et:
    :return: :rtype:
    """
    handle = ctypes.c_int(handle)
    descr = stypes.toDoubleVector(descr)
    et = ctypes.c_double(et)
    ref = ctypes.c_int()
    state = stypes.emptyDoubleVector(6)
    center = ctypes.c_int()
    libspice.spkpvn_c(handle, descr, et, ctypes.byref(ref), state, ctypes.byref(center))
    return ref.value, stypes.vectorToList(state), center.value


def spksfs(body, et, idlen):
    # spksfs has a Parameter SIDLEN, sounds like an optional but is that possible?
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param body:
    :param et:
    :param idlen:
    :return: :rtype:
    """
    body = ctypes.c_int(body)
    et = ctypes.c_double(et)
    idlen = ctypes.c_int(idlen)
    handle = ctypes.c_int()
    descr = stypes.emptyDoubleVector(5)
    identstring = stypes.stringToCharP(idlen)
    found = ctypes.c_bool()
    libspice.spksfs_c(body, et, idlen, ctypes.byref(handle), descr, identstring, ctypes.byref(found))
    if found.value:
        return handle.value, stypes.vectorToList(descr), stypes.toPythonString(identstring)
    else:
        return None


def spkssb(targ, et, ref):
    #Todo: test spkssb
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param targ:
    :param et:
    :param ref:
    :return: :rtype:
    """
    targ = ctypes.c_int(targ)
    et = ctypes.c_double(et)
    ref = stypes.stringToCharP(ref)
    starg = stypes.emptyDoubleVector(6)
    libspice.spkssb_c(targ, et, ref, starg)
    return stypes.vectorToList(starg)


def spksub(handle, descr, identin, begin, end, newh):
    #Todo: test spksub
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param handle:
    :param descr:
    :param identin:
    :param begin:
    :param end:
    :param newh:
    """
    assert len(descr) is 5
    handle = ctypes.c_int(handle)
    descr = stypes.toDoubleVector(descr)
    identin = stypes.stringToCharP(identin)
    begin = ctypes.c_int(begin)
    end = ctypes.c_int(end)
    newh = ctypes.c_int(newh)
    libspice.spksub_c(handle, descr, identin, begin, end, newh)
    pass


def spkuds(descr):
    #Todo: test spkuds
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param descr:
    :return: :rtype:
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
    libspice.spkuds_c(descr, ctypes.byref(body), ctypes.byref(center), ctypes.byref(framenum), ctypes.byref(typenum), ctypes.byref(first), ctypes.byref(last), ctypes.byref(begin), ctypes.byref(end))
    return body.value, center.value, framenum.value, typenum.value, first.value, last.value, begin.value, end.value


def spkuef(handle):
    #Todo: test spkuef
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param handle:
    """
    handle = ctypes.c_int(handle)
    libspice.spkuef_c(handle)
    pass


def spkw02(handle, body, center, inframe, first, last, segid, intlen, n, polydg, cdata, btime):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    :param body:
    :param center:
    :param inframe:
    :param first:
    :param last:
    :param segid:
    :param intlen:
    :param n:
    :param polydg:
    :param cdata:
    :param btime:
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
    libspice.spkw02_c(handle, body, center, inframe, first, last, segid, intlen, n, polydg, cdata, btime)
    pass


def spkw03(handle, body, center, inframe, first, last, segid, intlen, n, polydg, cdata, btime):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    :param body:
    :param center:
    :param inframe:
    :param first:
    :param last:
    :param segid:
    :param intlen:
    :param n:
    :param polydg:
    :param cdata:
    :param btime:
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
    libspice.spkw03_c(handle, body, center, inframe, first, last, segid, intlen, n, polydg, cdata, btime)
    pass


def spkw05(handle, body, center, inframe, first, last, segid, gm, n, states, epochs):
    # see libspice args for solution to array[][N] problem
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param handle:
    :param body:
    :param center:
    :param inframe:
    :param first:
    :param last:
    :param segid:
    :param gm:
    :param n:
    :param states:
    :param epochs:
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
    libspice.spkw05_c(handle, body, center, inframe, first, last, segid, gm, n, states, epochs)
    pass


def spkw08(handle, body, center, inframe, first, last, segid, degree, n, states, epoch1, step):
    # see libspice args for solution to array[][N] problem
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param handle:
    :param body:
    :param center:
    :param inframe:
    :param first:
    :param last:
    :param segid:
    :param degree:
    :param n:
    :param states:
    :param epoch1:
    :param step:
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
    libspice.spkw08_c(handle, body, center, inframe, first, last, segid, degree, n, states, epoch1, step)
    pass


def spkw09(handle, body, center, inframe, first, last, segid, degree, n, states, epochs):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    :param body:
    :param center:
    :param inframe:
    :param first:
    :param last:
    :param segid:
    :param degree:
    :param n:
    :param states:
    :param epochs:
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
    libspice.spkw09_c(handle, body, center, inframe, first, last, segid, degree, n, states, epochs)
    pass


def spkw10(handle, body, center, inframe, first, last, segid, consts, n, elems, epochs):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    :param body:
    :param center:
    :param inframe:
    :param first:
    :param last:
    :param segid:
    :param consts:
    :param n:
    :param elems:
    :param epochs:
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
    libspice.spkw10_c(handle, body, center, inframe, first, last, segid, consts, n, elems, epochs)
    pass


def spkw12(handle, body, center, inframe, first, last, segid, degree, n, states, epoch0, step):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    :param body:
    :param center:
    :param inframe:
    :param first:
    :param last:
    :param segid:
    :param degree:
    :param n:
    :param states:
    :param epoch0:
    :param step:
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
    libspice.spkw12_c(handle, body, center, inframe, first, last, segid, degree, n, states, epoch0, step)
    pass


def spkw13(handle, body, center, inframe, first, last, segid, degree, n, states, epochs):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param handle:
    :param body:
    :param center:
    :param inframe:
    :param first:
    :param last:
    :param segid:
    :param degree:
    :param n:
    :param states:
    :param epochs:
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
    libspice.spkw13_c(handle, body, center, inframe, first, last, segid, degree, n, states, epochs)
    pass


def spkw15(handle, body, center, inframe, first, last, segid, epoch, tp, pa, p, ecc, j2flg, pv, gm, j2, radius):
    #Todo: test spkw15
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param handle:
    :param body:
    :param center:
    :param inframe:
    :param first:
    :param last:
    :param segid:
    :param epoch:
    :param tp:
    :param pa:
    :param p:
    :param ecc:
    :param j2flg:
    :param pv:
    :param gm:
    :param j2:
    :param radius:
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
    libspice.spkw15_c(handle, body, center, inframe, first, last, segid, epoch, tp, pa, p, ecc, j2flg, pv, gm, j2, radius)
    pass


def spkw17(handle, body, center, inframe, first, last, segid, epoch, eqel, rapol, decpol):
    #Todo: test spkw17
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param handle:
    :param body:
    :param center:
    :param inframe:
    :param first:
    :param last:
    :param segid:
    :param epoch:
    :param eqel:
    :param rapol:
    :param decpol:
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
    libspice.spkw17_c(handle, body, center, inframe, first, last, segid, epoch, eqel, rapol, decpol)
    pass


#spkw18


def srfrec(body, longitude, latitude):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param body:
    :param longitude:
    :param latitude:
    :return: :rtype:
    """
    if hasattr(longitude, "__iter__") and hasattr(latitude, "__iter__"):
        return numpy.array([srfrec(body, lon, lat) for lon, lat in zip(longitude, latitude)])
    body = ctypes.c_int(body)
    longitude = ctypes.c_double(longitude)
    latitude = ctypes.c_double(latitude)
    rectan = stypes.emptyDoubleVector(3)
    libspice.srfrec_c(body, longitude, latitude, rectan)
    return stypes.vectorToList(rectan)


def srfxpt(method, target, et, abcorr, obsrvr, dref, dvec):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param method:
    :param target:
    :param et:
    :param abcorr:
    :param obsrvr:
    :param dref:
    :param dvec:
    :return: :rtype:
    """
    if hasattr(et, "__iter__"):
        return numpy.array([srfxpt(method, target, t, abcorr, obsrvr, dref, dvec) for t in et])
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
                      spoint, ctypes.byref(dist), ctypes.byref(trgepc), obspos, ctypes.byref(found))
    return stypes.vectorToList(spoint), dist.value, trgepc.value, stypes.vectorToList(obspos), found.value


def ssize(newsize, cell):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param newsize:
    :param cell:
    :return: :rtype:
    """
    assert isinstance(cell, stypes.SpiceCell)
    newsize = ctypes.c_int(newsize)
    libspice.ssize_c(newsize, ctypes.byref(cell))
    return cell


def stelab(pobj, vobs):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param pobj:
    :param vobs:
    :return: :rtype:
    """
    pobj = stypes.toDoubleVector(pobj)
    vobs = stypes.toDoubleVector(vobs)
    appobj = stypes.emptyDoubleVector(3)
    libspice.stelab_c(pobj, vobs, appobj)
    return stypes.vectorToList(appobj)


def stpool(item, nth, contin, lenout):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param item:
    :param nth:
    :param contin:
    :param lenout:
    :return: :rtype:
    """
    item = stypes.stringToCharP(item)
    contin = stypes.stringToCharP(contin)
    nth = ctypes.c_int(nth)
    strout = stypes.stringToCharP(lenout)
    lenout = ctypes.c_int(lenout)
    found = ctypes.c_bool()
    sizet = ctypes.c_int()
    libspice.stpool_c(item, nth, contin, lenout, strout, ctypes.byref(sizet), ctypes.byref(found))
    return stypes.toPythonString(strout), sizet.value, found.value


def str2et(time):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param time:
    :return: :rtype:
    """
    if isinstance(time, list):
        return numpy.array([str2et(t) for t in time])
    time = stypes.stringToCharP(time)
    et = ctypes.c_double()
    libspice.str2et_c(time, ctypes.byref(et))
    return et.value


def subpnt(method, target, et, fixref, abcorr, obsrvr):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param method:
    :param target:
    :param et:
    :param fixref:
    :param abcorr:
    :param obsrvr:
    :return: :rtype:
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
    libspice.subpnt_c(method, target, et, fixref, abcorr, obsrvr, spoint, ctypes.byref(trgepc), srfvec)
    return stypes.vectorToList(spoint), trgepc.value, stypes.vectorToList(srfvec)


def subpt(method, target, et, abcorr, obsrvr):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param method:
    :param target:
    :param et:
    :param abcorr:
    :param obsrvr:
    :return: :rtype:
    """
    if hasattr(et, "__iter__"):
        return numpy.array([subpt(method, target, t, abcorr, obsrvr) for t in et])
    method = stypes.stringToCharP(method)
    target = stypes.stringToCharP(target)
    et = ctypes.c_double(et)
    abcorr = stypes.stringToCharP(abcorr)
    obsrvr = stypes.stringToCharP(obsrvr)
    spoint = stypes.emptyDoubleVector(3)
    alt = ctypes.c_double()
    libspice.subpt_c(method, target, et, abcorr, obsrvr, spoint, ctypes.byref(alt))
    return stypes.vectorToList(spoint), alt.value


def subslr(method, target, et, fixref, abcorr, obsrvr):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param method:
    :param target:
    :param et:
    :param fixref:
    :param abcorr:
    :param obsrvr:
    :return: :rtype:
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
    libspice.subslr_c(method, target, et, fixref, abcorr, obsrvr, spoint, ctypes.byref(trgepc), srfvec)
    return stypes.vectorToList(spoint), trgepc.value, stypes.vectorToList(srfvec)


def subsol(method, target, et, abcorr, obsrvr):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param method:
    :param target:
    :param et:
    :param abcorr:
    :param obsrvr:
    :return: :rtype:
    """
    method = stypes.stringToCharP(method)
    target = stypes.stringToCharP(target)
    et = ctypes.c_double(et)
    abcorr = stypes.stringToCharP(abcorr)
    obsrvr = stypes.stringToCharP(obsrvr)
    spoint = stypes.emptyDoubleVector(3)
    libspice.subsol_c(method, target, et, abcorr, obsrvr, spoint)
    return stypes.vectorToList(spoint)


def sumad(array):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param array:
    :return: :rtype:
    """
    n = ctypes.c_int(len(array))
    array = stypes.toDoubleVector(array)
    return libspice.sumad_c(array, n)


def sumai(array):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param array:
    :return: :rtype:
    """
    n = ctypes.c_int(len(array))
    array = stypes.toIntVector(array)
    return libspice.sumai_c(array, n)


def surfnm(a, b, c, point):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param a:
    :param b:
    :param c:
    :param point:
    :return: :rtype:
    """
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    point = stypes.toDoubleVector(point)
    normal = stypes.emptyDoubleVector(3)
    libspice.surfnm_c(a, b, c, point, normal)
    return stypes.vectorToList(normal)


def surfpt(positn, u, a, b, c):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param positn:
    :param u:
    :param a:
    :param b:
    :param c:
    :return: :rtype:
    """
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    positn = stypes.toDoubleVector(positn)
    u = stypes.toDoubleVector(u)
    point = stypes.emptyDoubleVector(3)
    found = ctypes.c_bool()
    libspice.surfpt_c(positn, u, a, b, c, point, ctypes.byref(found))
    if found.value:
        return stypes.vectorToList(point)
    else:
        return None


def surfpv(stvrtx, stdir, a, b, c):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param stvrtx:
    :param stdir:
    :param a:
    :param b:
    :param c:
    :return: :rtype:
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


def swpool(agent, nnames, lenvals, names):
    #Todo: test swpool
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param agent:
    :param nnames:
    :param lenvals:
    :param names:
    """
    agent = stypes.stringToCharP(agent)
    nnames = ctypes.c_int(nnames)
    lenvals = ctypes.c_int(lenvals)
    names = stypes.listtocharvector(names)
    libspice.swpool_c(agent, nnames, lenvals, names)
    pass


def sxform(instring, tostring, et):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param instring:
    :param tostring:
    :param et:
    :return: :rtype:
    """
    if hasattr(et, "__iter__"):
        return numpy.array([sxform(instring, tostring, t) for t in et])
    instring = stypes.stringToCharP(instring)
    tostring = stypes.stringToCharP(tostring)
    et = ctypes.c_double(et)
    xform = stypes.emptyDoubleMatrix(x=6, y=6)
    libspice.sxform_c(instring, tostring, et, xform)
    return stypes.matrixToList(xform)


def szpool(name):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param name:
    :return: :rtype:
    """
    name = stypes.stringToCharP(name)
    n = ctypes.c_int()
    found = ctypes.c_bool(0)
    libspice.szpool_c(name, ctypes.byref(n), ctypes.byref(found))
    if found.value:
        return n.value
    else:
        return False


########################################################################################################################
# T


def timdef(action, item, lenout, value=None):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param action:
    :param item:
    :param lenout:
    :param value:
    :return: :rtype:
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


def timout(et, pictur, lenout):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param et:
    :param pictur:
    :param lenout:
    :return: :rtype:
    """
    if hasattr(et, "__iter__"):
        return numpy.array([timout(t, pictur, lenout) for t in et])
    pictur = stypes.stringToCharP(pictur)
    output = stypes.stringToCharP(lenout)
    lenout = ctypes.c_int(lenout)
    et = ctypes.c_double(et)
    libspice.timout_c(et, pictur, lenout, output)
    return stypes.toPythonString(output)


def tipbod(ref, body, et):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param ref:
    :param body:
    :param et:
    :return: :rtype:
    """
    ref = stypes.stringToCharP(ref)
    body = ctypes.c_int(body)
    et = ctypes.c_double(et)
    retmatrix = stypes.emptyDoubleMatrix()
    libspice.tipbod_c(ref, body, et, retmatrix)
    return stypes.matrixToList(retmatrix)


def tisbod(ref, body, et):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param ref:
    :param body:
    :param et:
    :return: :rtype:
    """
    ref = stypes.stringToCharP(ref)
    body = ctypes.c_int(body)
    et = ctypes.c_double(et)
    retmatrix = stypes.emptyDoubleMatrix(x=6, y=6)
    libspice.tisbod_c(ref, body, et, retmatrix)
    return stypes.matrixToList(retmatrix)


def tkvrsn(item):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param item:
    :return: :rtype:
    """
    item = stypes.stringToCharP(item)
    return stypes.toPythonString(libspice.tkvrsn_c(item))


def tparse(instring, lenout):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param instring:
    :param lenout:
    :return: :rtype:
    """
    errmsg = stypes.stringToCharP(lenout)
    lenout = ctypes.c_int(lenout)
    instring = stypes.stringToCharP(instring)
    sp2000 = ctypes.c_double()
    libspice.tparse_c(instring, lenout, ctypes.byref(sp2000), errmsg)
    return sp2000.value, stypes.toPythonString(errmsg)


def tpictr(sample, lenout, lenerr):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param sample:
    :param lenout:
    :param lenerr:
    :return: :rtype:
    """
    sample = stypes.stringToCharP(sample)
    pictur = stypes.stringToCharP(lenout)
    errmsg = stypes.stringToCharP(lenerr)
    lenout = ctypes.c_int(lenout)
    lenerr = ctypes.c_int(lenerr)
    ok = ctypes.c_bool()
    libspice.tpictr_c(sample, lenout, lenerr, pictur, ctypes.byref(ok), errmsg)
    return stypes.toPythonString(pictur), ok.value, stypes.toPythonString(errmsg)


def trace(matrix):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param matrix:
    :return: :rtype:
    """
    matrix = stypes.toDoubleMatrix(matrix)
    return libspice.trace_c(matrix)


def trcnam(index, namlen):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param index:
    :param namlen:
    :return: :rtype:
    """
    index = ctypes.c_int(index)
    name = stypes.stringToCharP(namlen)
    namlen = ctypes.c_int(namlen)
    libspice.trcnam_c(index, namlen, name)
    return stypes.toPythonString(name)


def trcdep():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    :return: :rtype:
    """
    depth = ctypes.c_int()
    libspice.trcdep_c(ctypes.byref(depth))
    return depth.value


def trcoff():
    #Todo: test trcoff
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    """
    libspice.trcoff_c()
    pass


def tsetyr(year):
    #Todo: test tsetyr
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param year:
    """
    year = ctypes.c_int(year)
    libspice.tsetyr_c(year)
    pass


def twopi():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    :return: :rtype:
    """
    return libspice.twopi_c()


def twovec(axdef, indexa, plndef, indexp):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param axdef:
    :param indexa:
    :param plndef:
    :param indexp:
    :return: :rtype:
    """
    axdef = stypes.toDoubleVector(axdef)
    indexa = ctypes.c_int(indexa)
    plndef = stypes.toDoubleVector(plndef)
    indexp = ctypes.c_int(indexp)
    mout = stypes.emptyDoubleMatrix()
    libspice.twovec_c(axdef, indexa, plndef, indexp, mout)
    return stypes.matrixToList(mout)


def tyear():
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/



    :return: :rtype:
    """
    return libspice.tyear_c()


########################################################################################################################
# U

def ucase(inchar, lenout=None):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param inchar:
    :param lenout:
    :return: :rtype:
    """
    if lenout is None:
        lenout = len(inchar) + 1
    inchar = stypes.stringToCharP(inchar)
    outchar = stypes.stringToCharP(" " * lenout)
    lenout = ctypes.c_int(lenout)
    libspice.ucase_c(inchar, lenout, outchar)
    return stypes.toPythonString(outchar)


def ucrss(v1, v2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v1:
    :param v2:
    :return: :rtype:
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    vout = stypes.emptyDoubleVector(3)
    libspice.ucrss_c(v1, v2, vout)
    return stypes.vectorToList(vout)


#UDDC # callback?


#UDDF # callback?


# UDF # callback?


def union(a, b):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param a:
    :param b:
    :return: :rtype: :raise NotImplementedError:
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


def unitim(epoch, insys, outsys):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param epoch:
    :param insys:
    :param outsys:
    :return: :rtype:
    """
    epoch = ctypes.c_double(epoch)
    insys = stypes.stringToCharP(insys)
    outsys = stypes.stringToCharP(outsys)
    return libspice.unitim_c(epoch, insys, outsys)


def unload(filename):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param filename:
    """
    if isinstance(filename, list):
        for f in filename:
            libspice.unload_c(stypes.stringToCharP(f))
    filename = stypes.stringToCharP(filename)
    libspice.unload_c(filename)
    pass


def unorm(v1):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v1:
    :return: :rtype:
    """
    v1 = stypes.toDoubleVector(v1)
    vout = stypes.emptyDoubleVector(3)
    vmag = ctypes.c_double()
    libspice.unorm_c(v1, vout, ctypes.byref(vmag))
    return stypes.vectorToList(vout), vmag.value


def unormg(v1, ndim):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v1:
    :param ndim:
    :return: :rtype:
    """
    v1 = stypes.toDoubleVector(v1)
    vout = stypes.emptyDoubleVector(ndim)
    vmag = ctypes.c_double()
    ndim = ctypes.c_int(ndim)
    libspice.unormg_c(v1, ndim, vout, ctypes.byref(vmag))
    return stypes.vectorToList(vout), vmag.value


def utc2et(utcstr):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param utcstr:
    :return: :rtype:
    """
    utcstr = stypes.stringToCharP(utcstr)
    et = ctypes.c_double()
    libspice.utc2et_c(utcstr, ctypes.byref(et))
    return et.value
########################################################################################################################
# V


def vadd(v1, v2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v1:
    :param v2:
    :return: :rtype:
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    vout = stypes.emptyDoubleVector(3)
    libspice.vadd_c(v1, v2, vout)
    return stypes.vectorToList(vout)


def vaddg(v1, v2, ndim):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v1:
    :param v2:
    :param ndim:
    :return: :rtype:
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    vout = stypes.emptyDoubleVector(ndim)
    ndim = ctypes.c_int(ndim)
    libspice.vaddg_c(v1, v2, ndim, vout)
    return stypes.vectorToList(vout)


def valid(insize, n, inset):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param insize:
    :param n:
    :param inset:
    :return: :rtype:
    """
    assert isinstance(inset, stypes.SpiceCell)
    insize = ctypes.c_int(insize)
    n = ctypes.c_int(n)
    libspice.valid_c(insize, n, inset)
    return inset


def vcrss(v1, v2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v1:
    :param v2:
    :return: :rtype:
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    vout = stypes.emptyDoubleVector(3)
    libspice.vcrss_c(v1, v2, vout)
    return stypes.vectorToList(vout)


def vdist(v1, v2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v1:
    :param v2:
    :return: :rtype:
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    return libspice.vdist_c(v1, v2)


def vdistg(v1, v2, ndim):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v1:
    :param v2:
    :param ndim:
    :return: :rtype:
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    ndim = ctypes.c_int(ndim)
    return libspice.vdistg_c(v1, v2, ndim)


def vdot(v1, v2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v1:
    :param v2:
    :return: :rtype:
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    return libspice.vdot_c(v1, v2)


def vdotg(v1, v2, ndim):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v1:
    :param v2:
    :param ndim:
    :return: :rtype:
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    ndim = ctypes.c_int(ndim)
    return libspice.vdotg_c(v1, v2, ndim)


def vequ(v1):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v1:
    :return: :rtype:
    """
    v1 = stypes.toDoubleVector(v1)
    vout = stypes.emptyDoubleVector(3)
    libspice.vequ_c(v1, vout)
    return stypes.vectorToList(vout)


def vequg(v1, ndim):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v1:
    :param ndim:
    :return: :rtype:
    """
    v1 = stypes.toDoubleVector(v1)
    vout = stypes.emptyDoubleVector(ndim)
    ndim = ctypes.c_int(ndim)
    libspice.vequg_c(v1, ndim, vout)
    return stypes.vectorToList(vout)


def vhat(v1):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v1:
    :return: :rtype:
    """
    v1 = stypes.toDoubleVector(v1)
    vout = stypes.emptyDoubleVector(3)
    libspice.vhat_c(v1, vout)
    return stypes.vectorToList(vout)


def vhatg(v1, ndim):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v1:
    :param ndim:
    :return: :rtype:
    """
    v1 = stypes.toDoubleVector(v1)
    vout = stypes.emptyDoubleVector(ndim)
    ndim = ctypes.c_int(ndim)
    libspice.vhatg_c(v1, ndim, vout)
    return stypes.vectorToList(vout)


def vlcom(a, v1, b, v2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param a:
    :param v1:
    :param b:
    :param v2:
    :return: :rtype:
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    sumv = stypes.emptyDoubleVector(3)
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    libspice.vlcom_c(a, v1, b, v2, sumv)
    return stypes.vectorToList(sumv)


def vlcom3(a, v1, b, v2, c, v3):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param a:
    :param v1:
    :param b:
    :param v2:
    :param c:
    :param v3:
    :return: :rtype:
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


def vlcomg(n, a, v1, b, v2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param n:
    :param a:
    :param v1:
    :param b:
    :param v2:
    :return: :rtype:
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    sumv = stypes.emptyDoubleVector(n)
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    n = ctypes.c_int(n)
    libspice.vlcomg_c(n, a, v1, b, v2, sumv)
    return stypes.vectorToList(sumv)


def vminug(vin, ndim):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param vin:
    :param ndim:
    :return: :rtype:
    """
    vin = stypes.toDoubleVector(vin)
    vout = stypes.emptyDoubleVector(ndim)
    ndim = ctypes.c_int(ndim)
    libspice.vminug_c(vin, ndim, vout)
    return stypes.vectorToList(vout)


def vminus(vin):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param vin:
    :return: :rtype:
    """
    vin = stypes.toDoubleVector(vin)
    vout = stypes.emptyDoubleVector(3)
    libspice.vminus_c(vin, vout)
    return stypes.vectorToList(vout)


def vnorm(v):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v:
    :return: :rtype:
    """
    v = stypes.toDoubleVector(v)
    return libspice.vnorm_c(v)


def vnormg(v, ndim):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v:
    :param ndim:
    :return: :rtype:
    """
    v = stypes.toDoubleVector(v)
    ndim = ctypes.c_int(ndim)
    return libspice.vnormg_c(v, ndim)


def vpack(x, y, z):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param x:
    :param y:
    :param z:
    :return: :rtype:
    """
    x = ctypes.c_double(x)
    y = ctypes.c_double(y)
    z = ctypes.c_double(z)
    vout = stypes.emptyDoubleVector(3)
    libspice.vpack_c(x, y, z, vout)
    return stypes.vectorToList(vout)


def vperp(a, b):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param a:
    :param b:
    :return: :rtype:
    """
    a = stypes.toDoubleVector(a)
    b = stypes.toDoubleVector(b)
    vout = stypes.emptyDoubleVector(3)
    libspice.vperp_c(a, b, vout)
    return stypes.vectorToList(vout)


def vprjp(vin, plane):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param vin:
    :param plane:
    :return: :rtype:
    """
    vin = stypes.toDoubleVector(vin)
    vout = stypes.emptyDoubleVector(3)
    libspice.vprjp_c(vin, ctypes.byref(plane), vout)
    return stypes.vectorToList(vout)


def vprjpi(vin, projpl, invpl):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param vin:
    :param projpl:
    :param invpl:
    :return: :rtype:
    """
    vin = stypes.toDoubleVector(vin)
    vout = stypes.emptyDoubleVector(3)
    found = ctypes.c_bool()
    libspice.vprjpi_c(vin, ctypes.byref(projpl), ctypes.byref(invpl), vout, ctypes.byref(found))
    if found.value:
        return stypes.vectorToList(vout)
    else:
        return None


def vproj(a, b):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param a:
    :param b:
    :return: :rtype:
    """
    a = stypes.toDoubleVector(a)
    b = stypes.toDoubleVector(b)
    vout = stypes.emptyDoubleVector(3)
    libspice.vproj_c(a, b, vout)
    return stypes.vectorToList(vout)


def vrel(v1, v2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v1:
    :param v2:
    :return: :rtype:
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    return libspice.vrel_c(v1, v2)


def vrelg(v1, v2, ndim):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v1:
    :param v2:
    :param ndim:
    :return: :rtype:
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    ndim = ctypes.c_int(ndim)
    return libspice.vrelg_c(v1, v2, ndim)


def vrotv(v, axis, theta):
    #Tested, but clarly some rounding issues exist (0 as 6.123*10^-17, etc)
    # halfpi is not exactly reprentable in IEEE 754 notation,
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/

    :param v:
    :param axis:
    :param theta:
    :return: :rtype:
    """
    v = stypes.toDoubleVector(v)
    axis = stypes.toDoubleVector(axis)
    theta = ctypes.c_double(theta)
    r = stypes.emptyDoubleVector(3)
    libspice.vrotv_c(v, axis, theta, r)
    return stypes.vectorToList(r)


def vscl(s, v1):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param s:
    :param v1:
    :return: :rtype:
    """
    s = ctypes.c_double(s)
    v1 = stypes.toDoubleVector(v1)
    vout = stypes.emptyDoubleVector(3)
    libspice.vscl_c(s, v1, vout)
    return stypes.vectorToList(vout)


def vsclg(s, v1, ndim):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param s:
    :param v1:
    :param ndim:
    :return: :rtype:
    """
    s = ctypes.c_double(s)
    v1 = stypes.toDoubleVector(v1)
    vout = stypes.emptyDoubleVector(ndim)
    ndim = ctypes.c_int(ndim)
    libspice.vsclg_c(s, v1, ndim, vout)
    return stypes.vectorToList(vout)


def vsep(v1, v2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v1:
    :param v2:
    :return: :rtype:
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    return libspice.vsep_c(v1, v2)


def vsepg(v1, v2, ndim):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v1:
    :param v2:
    :param ndim:
    :return: :rtype:
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    ndim = ctypes.c_int(ndim)
    return libspice.vsepg_c(v1, v2, ndim)


def vsub(v1, v2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v1:
    :param v2:
    :return: :rtype:
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    vout = stypes.emptyDoubleVector(3)
    libspice.vsub_c(v1, v2, vout)
    return stypes.vectorToList(vout)


def vsubg(v1, v2, ndim):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v1:
    :param v2:
    :param ndim:
    :return: :rtype:
    """
    v1 = stypes.toDoubleVector(v1)
    v2 = stypes.toDoubleVector(v2)
    vout = stypes.emptyDoubleVector(ndim)
    ndim = ctypes.c_int(ndim)
    libspice.vsubg_c(v1, v2, ndim, vout)
    return stypes.vectorToList(vout)


def vtmv(v1, matrix, v2):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v1:
    :param matrix:
    :param v2:
    :return: :rtype:
    """
    v1 = stypes.toDoubleVector(v1)
    matrix = stypes.listtodoublematrix(matrix)
    v2 = stypes.toDoubleVector(v2)
    return libspice.vtmv_c(v1, matrix, v2)


def vtmvg(v1, matrix, v2, nrow, ncol):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v1:
    :param matrix:
    :param v2:
    :param nrow:
    :param ncol:
    :return: :rtype:
    """
    v1 = stypes.toDoubleVector(v1)
    matrix = stypes.listtodoublematrix(matrix, x=ncol, y=nrow)
    v2 = stypes.toDoubleVector(v2)
    nrow = ctypes.c_int(nrow)
    ncol = ctypes.c_int(ncol)
    return libspice.vtmvg_c(v1, matrix, v2, nrow, ncol)


def vupack(v):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v:
    :return: :rtype:
    """
    v1 = stypes.toDoubleVector(v)
    x = ctypes.c_double()
    y = ctypes.c_double()
    z = ctypes.c_double()
    libspice.vupack_c(v1, ctypes.byref(x), ctypes.byref(y), ctypes.byref(z))
    return x.value, y.value, z.value


def vzero(v):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v:
    :return: :rtype:
    """
    v = stypes.toDoubleVector(v)
    return libspice.vzero_c(v)


def vzerog(v, ndim):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param v:
    :param ndim:
    :return: :rtype:
    """
    v = stypes.toDoubleVector(v)
    ndim = ctypes.c_int(ndim)
    return libspice.vzerog_c(v, ndim)

########################################################################################################################
# W


def wncard(window):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param window:
    :return: :rtype:
    """
    assert isinstance(window, stypes.SpiceCell)
    return libspice.wncard_c(window)


def wncomd(left, right, window):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param left:
    :param right:
    :param window:
    :return: :rtype:
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    left = ctypes.c_double(left)
    right = ctypes.c_double(right)
    result = stypes.SpiceCell.double(window.size)
    libspice.wncomd_c(left, right, ctypes.byref(window), result)
    return result


def wncond(left, right, window):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param left:
    :param right:
    :param window:
    :return: :rtype:
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    left = ctypes.c_double(left)
    right = ctypes.c_double(right)
    libspice.wncond_c(left, right, ctypes.byref(window))
    return window


def wndifd(a, b):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param a:
    :param b:
    :return: :rtype:
    """
    assert isinstance(a, stypes.SpiceCell)
    assert isinstance(b, stypes.SpiceCell)
    assert a.dtype == 1
    assert b.dtype == 1
    c = stypes.SpiceCell.double(a.size + b.size)
    libspice.wndifd_c(ctypes.byref(a), ctypes.byref(b), ctypes.byref(c))
    return c


def wnelmd(point, window):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param point:
    :param window:
    :return: :rtype:
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    point = ctypes.c_double(point)
    return libspice.wnelmd_c(point, ctypes.byref(window))


def wnexpd(left, right, window):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param left:
    :param right:
    :param window:
    :return: :rtype:
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    left = ctypes.c_double(left)
    right = ctypes.c_double(right)
    libspice.wnexpd_c(left, right, ctypes.byref(window))
    return window


def wnextd(side, window):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param side:
    :param window:
    :return: :rtype:
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    assert side == 'L' or side == 'R'
    side = ctypes.c_char(side.encode(encoding='UTF-8'))
    libspice.wnextd_c(side, ctypes.byref(window))
    return window


def wnfetd(window, n):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param window:
    :param n:
    :return: :rtype:
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    n = ctypes.c_int(n)
    left = ctypes.c_double()
    right = ctypes.c_double()
    libspice.wnfetd_c(ctypes.byref(window), n, ctypes.byref(left), ctypes.byref(right))
    return left.value, right.value


def wnfild(small, window):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param small:
    :param window:
    :return: :rtype:
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    small = ctypes.c_double(small)
    libspice.wnfild_c(small, ctypes.byref(window))
    return window


def wnfltd(small, window):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param small:
    :param window:
    :return: :rtype:
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    small = ctypes.c_double(small)
    libspice.wnfltd_c(small, ctypes.byref(window))
    return window


def wnincd(left, right, window):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param left:
    :param right:
    :param window:
    :return: :rtype:
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    left = ctypes.c_double(left)
    right = ctypes.c_double(right)
    return libspice.wnincd_c(left, right, ctypes.byref(window))


def wninsd(left, right, window):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param left:
    :param right:
    :param window:
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    left = ctypes.c_double(left)
    right = ctypes.c_double(right)
    libspice.wninsd_c(left, right, ctypes.byref(window))


def wnintd(a, b):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param a:
    :param b:
    :return: :rtype:
    """
    assert isinstance(a, stypes.SpiceCell)
    assert b.dtype == 1
    assert isinstance(b, stypes.SpiceCell)
    assert a.dtype == 1
    c = stypes.SpiceCell.double(b.size + a.size)
    libspice.wnintd_c(ctypes.byref(a), ctypes.byref(b), ctypes.byref(c))
    return c


def wnreld(a, op, b):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param a:
    :param op:
    :param b:
    :return: :rtype:
    """
    assert isinstance(a, stypes.SpiceCell)
    assert b.dtype == 1
    assert isinstance(b, stypes.SpiceCell)
    assert a.dtype == 1
    assert isinstance(op, str)
    op = stypes.stringToCharP(op.encode(encoding='UTF-8'))
    return libspice.wnreld_c(ctypes.byref(a), op, ctypes.byref(b))


def wnsumd(window):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param window:
    :return: :rtype:
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    meas = ctypes.c_double()
    avg = ctypes.c_double()
    stddev = ctypes.c_double()
    shortest = ctypes.c_int()
    longest = ctypes.c_int()
    libspice.wnsumd_c(ctypes.byref(window), ctypes.byref(meas), ctypes.byref(avg), ctypes.byref(stddev), ctypes.byref(shortest), ctypes.byref(longest))
    return meas.value, avg.value, stddev.value, shortest.value, longest.value


def wnunid(a, b):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param a:
    :param b:
    :return: :rtype:
    """
    assert isinstance(a, stypes.SpiceCell)
    assert b.dtype == 1
    assert isinstance(b, stypes.SpiceCell)
    assert a.dtype == 1
    c = stypes.SpiceCell.double(b.size+a.size)
    libspice.wnunid_c(ctypes.byref(a), ctypes.byref(b), ctypes.byref(c))
    return c


def wnvald(insize, n, window):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param insize:
    :param n:
    :param window:
    :return: :rtype:
    """
    assert isinstance(window, stypes.SpiceCell)
    assert window.dtype == 1
    insize = ctypes.c_int(insize)
    n = ctypes.c_int(n)
    libspice.wnvald_c(insize, n, ctypes.byref(window))
    return window


########################################################################################################################
# X

def xf2eul(xform, axisa, axisb, axisc):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param xform:
    :param axisa:
    :param axisb:
    :param axisc:
    :return: :rtype:
    """
    xform = stypes.listtodoublematrix(xform, x=6, y=6)
    axisa = ctypes.c_int(axisa)
    axisb = ctypes.c_int(axisb)
    axisc = ctypes.c_int(axisc)
    eulang = stypes.emptyDoubleVector(6)
    unique = ctypes.c_bool()
    libspice.xf2eul_c(xform, axisa, axisb, axisc, eulang, unique)
    return stypes.vectorToList(eulang), unique.value


def xf2rav(xform):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param xform:
    :return: :rtype:
    """
    xform = stypes.listtodoublematrix(xform, x=6, y=6)
    rot = stypes.emptyDoubleMatrix()
    av = stypes.emptyDoubleVector(3)
    libspice.xf2rav_c(xform, rot, av)
    return stypes.matrixToList(rot), stypes.vectorToList(av)


def xfmsta(input_state, input_coord_sys, output_coord_sys, body):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param input_state:
    :param input_coord_sys:
    :param output_coord_sys:
    :param body:
    :return: :rtype:
    """
    input_state = stypes.toDoubleVector(input_state)
    input_coord_sys = stypes.stringToCharP(input_coord_sys)
    output_coord_sys = stypes.stringToCharP(output_coord_sys)
    body = stypes.stringToCharP(body)
    output_state = stypes.emptyDoubleVector(6)
    libspice.xfmsta_c(input_state, input_coord_sys, output_coord_sys, body, output_state)
    return stypes.vectorToList(output_state)


def xpose(m):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param m:
    :return: :rtype:
    """
    m = stypes.toDoubleMatrix(m)
    mout = stypes.emptyDoubleMatrix(x=3, y=3)
    libspice.xpose_c(m, mout)
    return stypes.matrixToList(mout)


def xpose6(m):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param m:
    :return: :rtype:
    """
    m = stypes.toDoubleMatrix(m)
    mout = stypes.emptyDoubleMatrix(x=6, y=6)
    libspice.xpose6_c(m, mout)
    return stypes.matrixToList(mout)


def xposeg(matrix, nrow, ncol):
    """
    http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/


    :param matrix:
    :param nrow:
    :param ncol:
    :return: :rtype:
    """
    matrix = stypes.listtodoublematrix(matrix, x=ncol, y=nrow)
    mout = stypes.emptyDoubleMatrix(x=ncol, y=nrow)
    ncol = ctypes.c_int(ncol)
    nrow = ctypes.c_int(nrow)
    libspice.xposeg_c(matrix, nrow, ncol, mout)
    return stypes.matrixToList(mout)