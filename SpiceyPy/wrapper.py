__author__ = 'Apollo117'
# wrapper.py, a weak wrapper for libspice.py, here is where all the important ctypes setup and returning occurs.


import ctypes
import SpiceyPy.SupportTypes as stypes
from SpiceyPy.libspice import libspice

########################################################################################################################
# A


def axisar(axis, angle):
    #todo: test
    axis = stypes.listtodoublevector(axis)
    angle = ctypes.c_double(angle)
    r = stypes.doubleMatrix()
    libspice.axisar_c(axis, angle, r)
    return stypes.matrixtolist(r)

########################################################################################################################
# B


def b1900():
    return libspice.b1900_c()


def b1950():
    return libspice.b1950_c()


def badkpv(caller, name, comp, size, divby, intype):
    #todo: test
    caller = stypes.strtocharpoint(caller)
    name = stypes.strtocharpoint(name)
    comp = stypes.strtocharpoint(comp)
    size = ctypes.c_int(size)
    divby = ctypes.c_int(divby)
    intype = stypes.strtocharpoint(intype)
    return libspice.badkpv(caller, name, comp, size, divby, intype)


def bodc2n(code, lenout):
    #todo: test
    code = ctypes.c_int(code)
    name = stypes.strtocharpoint(" "*lenout)
    lenout = ctypes.c_int(lenout)
    found = ctypes.c_bool(0)
    libspice.bodc2n_c(code, lenout, name, ctypes.byref(found))
    return name.value


def bodc2s(code, lenout):
    #todo: test
    code = ctypes.c_int(code)
    name = stypes.strtocharpoint(" "*lenout)
    lenout = ctypes.c_int(lenout)
    libspice.bodc2s_c(code, lenout, name)
    return name.value


def boddef(name, code):
    #todo: test
    name = stypes.strtocharpoint(name)
    code = ctypes.c_int(code)
    libspice.boddef_c(name, code)
    pass


def bodfnd(body, item):
    body = ctypes.c_int(body)
    item = stypes.strtocharpoint(item)
    return libspice.bodfnd(body, item)


def bodn2c(name):
    name = stypes.strtocharpoint(name)
    code = ctypes.c_int(0)
    found = ctypes.c_bool(0)
    libspice.bodn2c_c(name, ctypes.byref(code), ctypes.byref(found))
    if found.value:
        return code.value
    else:
        return None


def bods2c(name):
    #Todo: test
    name = stypes.strtocharpoint(name)
    code = ctypes.c_int(0)
    found = ctypes.c_bool(0)
    libspice.bods2c_c(name, ctypes.byref(code), ctypes.byref(found))
    if found.value:
        return code.value
    else:
        return None


def bodvar(body, item, dim):
    #Todo: test
    body = ctypes.c_int(body)
    dim = ctypes.c_int(dim)
    item = stypes.strtocharpoint(item)
    values = stypes.doubleVector(dim.value)
    libspice.bodvar(body, item, ctypes.byref(dim), values)
    return stypes.vectortolist(values)


def bodvcd(bodyid, item, maxn):
    #todo: test
    bodyid = ctypes.c_int(bodyid)
    item = stypes.strtocharpoint(item)
    maxn = ctypes.c_int(maxn)
    dim = ctypes.c_int(0)
    values = stypes.doubleVector(maxn)
    libspice.bodvcd_c(bodyid, item, maxn, ctypes.byref(dim), values)
    return stypes.vectortolist(values)


def bodvrd(bodynm, item, maxn):
    bodynm = stypes.strtocharpoint(bodynm)
    item = stypes.strtocharpoint(item)
    maxn = ctypes.c_int(maxn)
    dim = ctypes.c_int(0)
    values = stypes.doubleVector(3)
    libspice.bodvrd_c(bodynm, item, maxn, ctypes.byref(dim), values)
    return stypes.vectortolist(values)


def brcktd(number, end1, end2):
    number = ctypes.c_double(number)
    end1 = ctypes.c_double(end1)
    end2 = ctypes.c_double(end2)
    return libspice.brcktd_c(number, end1, end2)


def brckti(number, end1, end2):
    number = ctypes.c_int(number)
    end1 = ctypes.c_int(end1)
    end2 = ctypes.c_int(end2)
    return libspice.brckti_c(number, end1, end2)


def bschoc(value, ndim, lenvals, array, order):
    #todo: Fix, probably not working
    value = stypes.strtocharpoint(value)
    ndim = ctypes.c_int(ndim)
    lenvals = ctypes.c_int(lenvals)
    array = stypes.listtocharvector(array)
    order = stypes.listtointvector(order)
    return libspice.bschoc(value, ndim, lenvals, array, order)


def bschoi(value, ndim, array, order):
    #todo: Fix, this is not working
    value = ctypes.c_int(value)
    ndim = ctypes.c_int(ndim)
    order = stypes.listtointvector(order)
    array = stypes.listtointvector(array)
    return libspice.bschoi_c(value, ndim, order, array)


def bsrchc(value, ndim, lenvals, array):
    #todo: Fix, this is not working
    value = stypes.strtocharpoint(value)
    ndim = ctypes.c_int(ndim)
    lenvals = ctypes.c_int(lenvals)
    array = stypes.listtocharvector(array)
    return libspice.bsrchc_c(value, ndim, lenvals, array)


def bsrchd(value, ndim, array):
    value = ctypes.c_double(value)
    ndim = ctypes.c_int(ndim)
    array = stypes.listtodoublevector(array)
    return libspice.bsrchd_c(value, ndim, array)


def bsrchi(value, ndim, array):
    value = ctypes.c_int(value)
    ndim = ctypes.c_int(ndim)
    array = stypes.listtointvector(array)
    return libspice.bsrchi_c(value, ndim, array)


########################################################################################################################
# C

########################################################################################################################
# D


def dpr():
    return libspice.dpr_c()

########################################################################################################################
# E

########################################################################################################################
# F


def furnsh(path):
    path = stypes.strtocharpoint(path)
    libspice.furnsh_c(path)
    pass

########################################################################################################################
# G


def getfov(instid, room, shapelen, framelen):
    instid = ctypes.c_int(instid)
    room = ctypes.c_int(room)
    shape = stypes.strtocharpoint(" "*shapelen)
    frame = stypes.strtocharpoint(" "*framelen)
    shapelen = ctypes.c_int(shapelen)
    framelen = ctypes.c_int(framelen)
    bsight = stypes.doubleVector(3)
    n = ctypes.c_int(0)
    bounds = stypes.doubleMatrix(x=3, y=4)
    libspice.getfov_c(instid, room, shapelen, framelen, shape, frame, bsight, ctypes.byref(n), bounds)
    return {'shape': shape.value, 'frame': frame.value, 'bsight': stypes.vectortolist(bsight), 'bounds': stypes.matrixtolist(bounds)}



########################################################################################################################
# H


def halfpi():
    return libspice.halfpi_c()


########################################################################################################################
# I


def ilumin(method, target, et, fixref, abcorr, obsrvr, spoint):
    method = stypes.strtocharpoint(method)
    target = stypes.strtocharpoint(target)
    et = ctypes.c_double(et)
    fixref = stypes.strtocharpoint(fixref)
    abcorr = stypes.strtocharpoint(abcorr)
    obsrvr = stypes.strtocharpoint(obsrvr)
    spoint = stypes.listtodoublevector(spoint)
    trgepc = ctypes.c_double(0)
    srfvec = stypes.doubleVector(3)
    phase = ctypes.c_double(0)
    solar = ctypes.c_double(0)
    emissn = ctypes.c_double(0)
    libspice.ilumin_c(method, target, et, fixref, abcorr, obsrvr, spoint, ctypes.byref(trgepc),
              srfvec, ctypes.byref(phase), ctypes.byref(solar), ctypes.byref(emissn))
    return {'trgepc': trgepc.value, 'srfvec': stypes.vectortolist(srfvec), 'phase': phase.value, 'solar': solar.value, 'emissn': emissn.value}



########################################################################################################################
# J

def j1900():
    return libspice.j1900_c()


def j1950():
    return libspice.j1950_c()


def j2000():
    return libspice.j2000_c()


def j2100():
    return libspice.j2100_c()


def jyear():
    return libspice.jyear_c()
########################################################################################################################
# K


def kclear():
    libspice.kclear_c()
    pass


def ktotal(kind):
    kind = stypes.strtocharpoint(kind)
    count = ctypes.c_int(0)
    libspice.ktotal_c(kind, ctypes.byref(count))
    return count.value

########################################################################################################################
# L


########################################################################################################################
# M


def mtxm(m1, m2):
    m1 = stypes.listtodoublematrix(m1)
    m2 = stypes.listtodoublematrix(m2)
    mout = stypes.doubleMatrix()
    libspice.mtxm_c(m1, m2, mout)
    return stypes.matrixtolist(mout)

########################################################################################################################
# N


########################################################################################################################
# O


########################################################################################################################
# P

def pi():
    return libspice.pi_c()

########################################################################################################################
# Q

def q2m(q):
    q = stypes.listtodoublevector(q)
    mout = stypes.doubleMatrix()
    libspice.q2m_c(q, mout)
    return stypes.matrixtolist(mout)


def qdq2av(q, dq):
    #Todo: test
    q = stypes.listtodoublevector(q)
    dq = stypes.listtodoublevector(dq)
    vout = stypes.doubleVector(3)
    libspice.qdq2av(q, dq, vout)
    return stypes.vectortolist(vout)


def qxq(q1, q2):
    #Todo: test
    q1 = stypes.listtodoublevector(q1)
    q2 = stypes.listtodoublevector(q2)
    vout = stypes.doubleVector(4)
    libspice.qxq_c(q1, q2, vout)
    return stypes.vectortolist(vout)

########################################################################################################################
# R

def reclat(rectan):
    rectan = stypes.listtodoublevector(rectan)
    radius = ctypes.c_double(0)
    longitude = ctypes.c_double(0)
    latitude = ctypes.c_double(0)
    libspice.reclat_c(rectan, ctypes.byref(radius), ctypes.byref(longitude), ctypes.byref(latitude))
    return radius.value, longitude.value, latitude.value


def recgeo(rectan, re, f):
    rectan = stypes.listtodoublevector(rectan)
    re = ctypes.c_double(re)
    f = ctypes.c_double(f)
    longitude = ctypes.c_double(0)
    latitude = ctypes.c_double(0)
    alt = ctypes.c_double(0)
    libspice.recgeo_c(rectan, re, f, ctypes.byref(longitude), ctypes.byref(latitude), ctypes.byref(alt))
    return longitude.value, latitude.value, alt.value


########################################################################################################################
# S

def str2et(time):
    time = stypes.strtocharpoint(time)
    et = ctypes.c_double(0)
    libspice.str2et_c(time, ctypes.byref(et))
    return et.value


def sincpt(method, target, et, fixref, abcorr, obsrvr, dref, dvec):
    method = stypes.strtocharpoint(method)
    target = stypes.strtocharpoint(target)
    et = ctypes.c_double(et)
    fixref = stypes.strtocharpoint(fixref)
    abcorr = stypes.strtocharpoint(abcorr)
    obsrvr = stypes.strtocharpoint(obsrvr)
    dref = stypes.strtocharpoint(dref)
    dvec = stypes.listtodoublevector(dvec)
    spoint = stypes.doubleVector(3)
    trgepc = ctypes.c_double(0)
    srfvec = stypes.doubleVector(3)
    found = ctypes.c_bool(0)
    libspice.sincpt_c(method, target, et, fixref, abcorr, obsrvr, dref, dvec,
              spoint, ctypes.byref(trgepc), srfvec, ctypes.byref(found))
    return {'spoint': stypes.vectortolist(spoint), 'trgepc': trgepc.value, 'srfvec': stypes.vectortolist(srfvec), 'found': found.value}




########################################################################################################################
# T

def twopi():
    return libspice.twopi_c()

########################################################################################################################
# U

def ucase(inchar, lenout):
    inchar = stypes.strtocharpoint(inchar)
    outchar = stypes.strtocharpoint(" "*lenout)
    lenout = ctypes.c_int(lenout)
    libspice.ucase_c(inchar, lenout, outchar)
    return outchar.value


########################################################################################################################
# V


def vadd(v1, v2):
    v1 = stypes.listtodoublevector(v1)
    v2 = stypes.listtodoublevector(v2)
    vout = stypes.doubleVector(3)
    libspice.vadd_c(v1, v2, vout)
    return stypes.vectortolist(vout)


def vaddg(v1, v2, ndim):
    v1 = stypes.listtodoublevector(v1)
    v2 = stypes.listtodoublevector(v2)
    vout = stypes.doubleVector(ndim)
    ndim = ctypes.c_int(ndim)
    libspice.vaddg_c(v1, v2, ndim, vout)
    return stypes.vectortolist(vout)


def vcrss(v1, v2):
    v1 = stypes.listtodoublevector(v1)
    v2 = stypes.listtodoublevector(v2)
    vout = stypes.doubleVector(3)
    libspice.vcrss_c(v1, v2, vout)
    return stypes.vectortolist(vout)


def vdist(v1, v2):
    v1 = stypes.listtodoublevector(v1)
    v2 = stypes.listtodoublevector(v2)
    return libspice.vdist_c(v1, v2)


def vdistg(v1, v2, ndim):
    #Todo: test
    v1 = stypes.listtodoublevector(v1)
    v2 = stypes.listtodoublevector(v2)
    ndim = ctypes.c_int(ndim)
    return libspice.vdist_c(v1, v2, ndim)


def vdot(v1, v2):
    #Works but not verified, this would take all of 2 seconds to do however
    v1 = stypes.listtodoublevector(v1)
    v2 = stypes.listtodoublevector(v2)
    return libspice.vdot_c(v1, v2)


def vdotg(v1, v2, ndim):
    #Works but not verified, this would take all of 2 seconds to do however
    v1 = stypes.listtodoublevector(v1)
    v2 = stypes.listtodoublevector(v2)
    ndim = ctypes.c_int(ndim)
    return libspice.vdot_c(v1, v2, ndim)


def vequ(v1):
    v1 = stypes.listtodoublevector(v1)
    vout = stypes.doubleVector(3)
    libspice.vequ_c(v1, vout)
    return stypes.vectortolist(vout)


def vequg(v1, ndim):
    v1 = stypes.listtodoublevector(v1)
    vout = stypes.doubleVector(ndim)
    ndim = ctypes.c_int(ndim)
    libspice.vequg_c(v1, ndim, vout)
    return stypes.vectortolist(vout)


def vhat(v1):
    v1 = stypes.listtodoublevector(v1)
    vout = stypes.doubleVector(3)
    libspice.vhat_c(v1, vout)
    return stypes.vectortolist(vout)


def vhatg(v1, ndim):
    v1 = stypes.listtodoublevector(v1)
    vout = stypes.doubleVector(ndim)
    ndim = ctypes.c_int(ndim)
    libspice.vhatg_c(v1, ndim, vout)
    return stypes.vectortolist(vout)


def vlcom(a, v1, b, v2):
    #Todo: test
    v1 = stypes.listtodoublevector(v1)
    v2 = stypes.listtodoublevector(v2)
    sumv = stypes.doubleVector(3)
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    libspice.vlcom_c(a, v1, b, v2, sumv)
    return stypes.vectortolist(sumv)


def vlcom3(a, v1, b, v2, c, v3):
    #Todo: test
    v1 = stypes.listtodoublevector(v1)
    v2 = stypes.listtodoublevector(v2)
    v3 = stypes.listtodoublevector(v3)
    sumv = stypes.doubleVector(3)
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    libspice.vlcom3_c(a, v1, b, v2, c, v3, sumv)
    return stypes.vectortolist(sumv)


def vlcomg(n, a, v1, b, v2):
    #Todo: test
    v1 = stypes.listtodoublevector(v1)
    v2 = stypes.listtodoublevector(v2)
    sumv = stypes.doubleVector(n)
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    n = ctypes.c_int(n)
    libspice.vlcomg_c(n, a, v1, b, v2, sumv)
    return stypes.vectortolist(sumv)


def vminug(vin, ndim):
    #todo: test
    vin = stypes.listtodoublevector(vin)
    vout = stypes.doubleVector(ndim)
    ndim = ctypes.c_int(ndim)
    libspice.vminug_c(vin, ndim, vout)
    return stypes.vectortolist(vout)


def vminus(vin):
    #todo: test
    vin = stypes.listtodoublevector(vin)
    vout = stypes.doubleVector(3)
    libspice.vminus_c(vin, vout)
    return stypes.vectortolist(vout)


def vnorm(v):
    v = stypes.listtodoublevector(v)
    return libspice.vnorm_c(v)


def vnormg(v, ndim):
    #todo: test
    v = stypes.listtodoublevector(v)
    ndim = ctypes.c_int(ndim)
    return libspice.vnormg_c(v, ndim)


def vpack(x, y, z):
    x = ctypes.c_double(x)
    y = ctypes.c_double(y)
    z = ctypes.c_double(z)
    vout = stypes.doubleVector(3)
    libspice.vpack_c(x, y, z, vout)
    return stypes.vectortolist(vout)


def vperp(a, b):
    a = stypes.listtodoublevector(a)
    b = stypes.listtodoublevector(b)
    vout = stypes.doubleVector(3)
    libspice.vperp_c(a, b, vout)
    return stypes.vectortolist(vout)

#vprjp

#vprjpi


def vproj(a, b):
    a = stypes.listtodoublevector(a)
    b = stypes.listtodoublevector(b)
    vout = stypes.doubleVector(3)
    libspice.vproj_c(a, b, vout)
    return stypes.vectortolist(vout)


def vrel(v1, v2):
    v1 = stypes.listtodoublevector(v1)
    v2 = stypes.listtodoublevector(v2)
    return libspice.vrel_c(v1, v2)


def vrelg(v1, v2, ndim):
    #Todo: test
    v1 = stypes.listtodoublevector(v1)
    v2 = stypes.listtodoublevector(v2)
    ndim = ctypes.c_int(ndim)
    return libspice.vrelg_c(v1, v2, ndim)


def vrotv(v, axis, theta):
    #Tested, but clarly some rounding issues exist (0 as 6.123*10^-17, etc)
    # halfpi is not exactly reprentable in IEEE 754 notation,
    v = stypes.listtodoublevector(v)
    axis = stypes.listtodoublevector(axis)
    theta = ctypes.c_double(theta)
    r = stypes.doubleVector(3)
    libspice.vrotv_c(v, axis, theta, r)
    return stypes.vectortolist(r)


def vscl(s, v1):
    #Todo: test
    s = ctypes.c_double(s)
    v1 = stypes.listtodoublevector(v1)
    vout = stypes.doubleVector(3)
    libspice.vscl_c(s, v1, vout)
    return stypes.vectortolist(vout)


def vsclg(s, v1, ndim):
    #Todo: test
    s = ctypes.c_double(s)
    v1 = stypes.listtodoublevector(v1)
    vout = stypes.doubleVector(ndim)
    ndim = ctypes.c_int(ndim)
    libspice.vsclg_c(s, v1, ndim, vout)
    return stypes.vectortolist(vout)


def vsep(v1, v2):
    #Todo: test
    v1 = stypes.listtodoublevector(v1)
    v2 = stypes.listtodoublevector(v2)
    return libspice.vsep_c(v1, v2)


def vsepg(v1, v2, ndim):
    #Todo: test
    v1 = stypes.listtodoublevector(v1)
    v2 = stypes.listtodoublevector(v2)
    ndim = ctypes.c_int(ndim)
    return libspice.vsepg_c(v1, v2, ndim)


def vsub(v1, v2):
    #Todo: test
    v1 = stypes.listtodoublevector(v1)
    v2 = stypes.listtodoublevector(v2)
    vout = stypes.doubleVector(3)
    libspice.vsub_c(v1, v2, vout)
    return stypes.vectortolist(vout)


def vsubg(v1, v2, ndim):
    #Todo: test
    v1 = stypes.listtodoublevector(v1)
    v2 = stypes.listtodoublevector(v2)
    vout = stypes.doubleVector(ndim)
    ndim = stypes.ctypes.c_int(ndim)
    libspice.vsubg_c(v1, v2, ndim, vout)
    return stypes.vectortolist(vout)


def vtmv(v1, matrix, v2):
    #Todo: test
    v1 = stypes.listtodoublevector(v1)
    matrix = stypes.listtodoublematrix(matrix)
    v2 = stypes.listtodoublevector(v2)
    return libspice.vtmv_c(v1, matrix, v2)


def vtmvg(v1, matrix, v2, nrow, ncol):
    #Todo: test
    v1 = stypes.listtodoublevector(v1)
    matrix = stypes.listtodoublematrix(matrix, x=ncol, y=nrow)
    v2 = stypes.listtodoublevector(v2)
    nrow = ctypes.c_int(nrow)
    ncol = ctypes.c_int(ncol)
    return libspice.vtmvg_c(v1, matrix, v2, nrow, ncol)


def vupack(v):
    v1 = stypes.listtodoublevector(v)
    x = ctypes.c_double()
    y = ctypes.c_double()
    z = ctypes.c_double()
    libspice.vupack_c(v1, ctypes.byref(x), ctypes.byref(y), ctypes.byref(z))
    return x.value, y.value, z.value


def vzero(v):
    v = stypes.listtodoublevector(v)
    return libspice.vzero_c(v)


def vzerog(v, ndim):
    v = stypes.listtodoublevector(v)
    ndim = stypes.ctypes.c_int(ndim)
    return libspice.vzerog_c(v, ndim)

########################################################################################################################
# W


########################################################################################################################
# X

def xpose(m):
    #Todo: Fix, something is not right, something is not right with the types
    m = stypes.listtodoublematrix(m)
    mout = stypes.doubleMatrix()
    libspice.xpose_c(m, mout)
    return stypes.matrixtolist(m)

########################################################################################################################
# Y


########################################################################################################################
# Z
