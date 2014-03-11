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
    return {'shape': shape.value, 'frame': frame.value, 'bsight': stypes.vectortolist(bsight),
            'bounds': stypes.matrixtolist(bounds)}

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

#ordc


#ordd


#ordi


def orderc(lenvals, array, ndim):
    #Todo: test, works but I am not convinced yet
    iorder = stypes.listtointvector([0] * ndim)
    ndim = ctypes.c_int(ndim)
    array = stypes.listtocharvector(array)
    lenvals = ctypes.c_int(lenvals)
    libspice.orderc_c(lenvals, array, ndim, iorder)
    return stypes.vectortolist(iorder)


def orderd(array, ndim):
    #Todo: test
    array = stypes.listtodoublevector(array)
    iorder = stypes.listtointvector([0] * ndim)
    ndim = ctypes.c_int(ndim)
    libspice.orderd_c(array, ndim, iorder)
    return stypes.vectortolist(iorder)


def orderi(array, ndim):
    array = stypes.listtointvector(array)
    iorder = stypes.listtointvector([0] * ndim)
    ndim = ctypes.c_int(ndim)
    libspice.orderi_c(array, ndim, iorder)
    return stypes.vectortolist(iorder)


def oscelt(stat, et, mu):
    #Todo: Test
    stat = stypes.listtodoublevector(stat)
    et = ctypes.c_double(et)
    mu = ctypes.c_double(mu)
    elts = stypes.doubleVector(8)
    libspice.oscelt_c(stat, et, mu, elts)
    return stypes.vectortolist(elts)

########################################################################################################################
# P


def pcklof(filename):
    #Todo: test
    filename = stypes.strtocharpoint(filename)
    handle = ctypes.c_int()
    libspice.pcklof_c(filename, ctypes.byref(handle))
    return handle.value


def pckuof(handle):
    #Todo: test
    handle = ctypes.c_int(handle)
    libspice.pckuof_c(handle)
    pass


def pcpool(name, n, lenvals, cvals):
    #Todo: test
    name = stypes.strtocharpoint(name)
    cvals = stypes.listtocharvector(cvals)
    n = ctypes.c_int(n)
    lenvals = ctypes.c_int(lenvals)
    libspice.pcpool_c(name, n, lenvals, cvals)


def pdpool(name, n, dvals):
    #Todo: test
    name = stypes.strtocharpoint(name)
    dvals = stypes.listtodoublevector(dvals)
    n = ctypes.c_int(n)
    libspice.pdpool_c(name, n, dvals)


def pipool(name, n, ivals):
    #Todo: test
    name = stypes.strtocharpoint(name)
    ivals = stypes.listtointvector(ivals)
    n = ctypes.c_int(n)
    libspice.pipool_c(name, n, ivals)


def pgrrec(body, lon, lat, alt, re, f):
    #Todo: test
    body = stypes.strtocharpoint(body)
    lon = ctypes.c_double(lon)
    lat = ctypes.c_double(lat)
    alt = ctypes.c_double(alt)
    re = ctypes.c_double(re)
    f = ctypes.c_double(f)
    rectan = stypes.doubleVector(3)
    libspice.pgrrec(body, lon, lat, alt, re, f, rectan)
    return stypes.vectortolist(rectan)


def pi():
    return libspice.pi_c()

#pjelpl

#pl2ncv

#pl2nvp

#pl2psv


def pos(string, substr, start):
    string = stypes.strtocharpoint(string)
    substr = stypes.strtocharpoint(substr)
    start = ctypes.c_int(start)
    return libspice.pos_c(string, substr, start)


def posr(string, substr, start):
    string = stypes.strtocharpoint(string)
    substr = stypes.strtocharpoint(substr)
    start = ctypes.c_int(start)
    return libspice.posr_c(string, substr, start)


#prompt, skip for no as this is not really an important function for python users


def prop2b(gm, pvinit, dt):
    #todo: test
    gm = ctypes.c_double(gm)
    pvinit = stypes.listtodoublevector(pvinit)
    dt = ctypes.c_double(dt)
    pvprop = stypes.doubleVector(6)
    libspice.prop2b_c(gm, pvinit, dt, pvprop)
    return stypes.vectortolist(pvprop)


def prsdp(string):
    #Todo: test
    string = stypes.strtocharpoint(string)
    dpval = ctypes.c_double()
    libspice.prsdp_c(string, ctypes.POINTER(dpval))
    return dpval.value


def prsint(string):
    #Todo: test
    string = stypes.strtocharpoint(string)
    intval = ctypes.c_int()
    libspice.prsint_c(string, ctypes.POINTER(intval))
    return intval.value


# psv2pl


# skip putcml, is this really needed for python users?


def pxform(fromstr, tostr, et):
    #Todo: test
    et = ctypes.c_double(et)
    tostr = stypes.strtocharpoint(tostr)
    fromstr = stypes.strtocharpoint(fromstr)
    rotate = stypes.doubleMatrix()
    libspice.pxform_c(fromstr, tostr, et, rotate)
    return stypes.matrixtolist(rotate)


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


def radrec(inrange, re, dec):
    #Todo: test
    inrange = ctypes.c_double(inrange)
    re = ctypes.c_double(re)
    dec = ctypes.c_double(dec)
    rectan = stypes.doubleVector(3)
    libspice.radrec_c(inrange, re, dec, rectan)
    return stypes.vectortolist(rectan)


def rav2xf(rot, av):
    #Todo: test
    rot = stypes.listtodoublematrix(rot)
    av = stypes.listtodoublevector(av)
    xform = stypes.doubleMatrix(x=6, y=6)
    libspice.rav2xf_c(rot, av, xform)
    return stypes.matrixtolist(xform)


def raxisa(matrix):
    #Todo: test
    matrix = stypes.listtodoublematrix(matrix)
    axis = stypes.doubleVector(3)
    angle = ctypes.c_double()
    libspice.raxisa_c(matrix, axis, ctypes.byref(angle))
    return stypes.vectortolist(axis), angle.value


def rdtext(file, lenout):
    #Todo: test
    file = stypes.strtocharpoint(file)
    line = stypes.strtocharpoint(" "*lenout)
    lenout = ctypes.c_int(lenout)
    eof = ctypes.c_bool()
    libspice.rdtext_c(file, lenout, line, ctypes.byref(eof))
    return line, eof.value


def reccyl(rectan):
    rectan = stypes.listtodoublevector(rectan)
    radius = ctypes.c_double(0)
    lon = ctypes.c_double(0)
    z = ctypes.c_double(0)
    libspice.reccyl_c(rectan, ctypes.byref(radius), ctypes.byref(lon), ctypes.byref(z))
    return radius.value, lon.value, z.value


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


def recpgr(body, rectan, re, f):
    #Todo: Test
    body = stypes.strtocharpoint(body)
    rectan = stypes.listtodoublevector(rectan)
    re = ctypes.c_double(re)
    f = ctypes.c_double(f)
    lon = ctypes.c_double()
    lat = ctypes.c_double()
    alt = ctypes.c_double()
    libspice.recpgr_c(body, rectan, re, f, ctypes.byref(lon), ctypes.byref(lat), ctypes.byref(alt))
    return lon.value, lat.value, alt.value


def recrad(rectan):
    #Todo: Test
    rectan = stypes.listtodoublevector(rectan)
    outrange = ctypes.c_double()
    ra = ctypes.c_double()
    dec = ctypes.c_double()
    libspice.recrad_c(rectan, ctypes.byref(outrange), ctypes.byref(ra), ctypes.byref(dec))
    return outrange.value, ra.value, dec.value


def recsph(rectan):
    #Todo: Test
    rectan = stypes.listtodoublevector(rectan)
    r = ctypes.c_double()
    colat = ctypes.c_double()
    lon = ctypes.c_double()
    libspice.rectan_c(rectan, ctypes.byref(r), ctypes.byref(colat), ctypes.byref(lon))
    return r.value, colat.value, lon.value

#removc
#removd
#removi
#reordc
#reordi
#reordi
#reordl
#repmc
#repmct
#repmd
#repmf
#repmi
#repmot


def reset():
    libspice.reset_c()
    pass


#skipping return_c


def rotate(angle, iaxis):
    #Todo: test
    angle = ctypes.c_double(angle)
    iaxis = ctypes.c_int(iaxis)
    mout = stypes.doubleMatrix()
    libspice.rotate_c(angle, iaxis, mout)
    return stypes.matrixtolist(mout)


def rotmat(m1, angle, iaxis):
    #Todo: test
    m1 = stypes.listtodoublematrix(m1)
    angle = ctypes.c_double(angle)
    iaxis = ctypes.c_int(iaxis)
    mout = stypes.doubleMatrix()
    libspice.rotmat_c(m1, angle, iaxis, mout)
    return stypes.matrixtolist(mout)


def rotvec(v1, angle, iaxis):
    #Todo: test
    v1 = stypes.listtodoublevector(v1)
    angle = ctypes.c_double(angle)
    iaxis = ctypes.c_int(iaxis)
    vout = stypes.doubleVector(3)
    libspice.rotvec_c(v1, angle, iaxis, vout)
    return stypes.vectortolist(vout)


def rpd():
    return libspice.rpd_c()


def rquad(a, b, c):
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    root1 = stypes.doubleVector(2)
    root2 = stypes.doubleVector(2)
    libspice.rquad(a, b, c, root1, root2)
    return root1, root2

########################################################################################################################
# S


def saelgv(vec1, vec2):
    #Todo: test saelgv
    vec1 = stypes.listtodoublevector(vec1)
    vec2 = stypes.listtodoublevector(vec2)
    smajor = stypes.doubleVector(3)
    sminor = stypes.doubleVector(3)
    libspice.saelgv_c(vec1, vec2, smajor, sminor)
    return stypes.vectortolist(smajor), stypes.vectortolist(sminor)


#skipping scard for now


def scdecd(sc, sclkdp, lenout, MXPART=None):
    #todo: figure out how to use mxpart, and test scdecd
    sc = ctypes.c_int(sc)
    sclkdp = ctypes.c_double(sclkdp)
    sclkch = stypes.strtocharpoint(" "*lenout)
    lenout = ctypes.c_int(lenout)
    libspice.scdecd_c(sc, sclkdp, lenout, sclkch)
    return sclkch


def sce2c(sc, et):
    #todo: test sce2c
    sc = ctypes.c_int(sc)
    et = ctypes.c_double(et)
    sclkdp = ctypes.c_double()
    libspice.sce2c_c(sc, et, ctypes.byref(sclkdp))
    return sclkdp.value


def sce2s(sc, et, lenout):
    #todo: test sce2s
    sc = ctypes.c_int(sc)
    et = ctypes.c_double(et)
    sclkch = stypes.strtocharpoint(" " * lenout)
    lenout = ctypes.c_int(lenout)
    libspice.sce2s_c(sc, et, lenout, sclkch)
    return sclkch


def sce2t(sc, et):
    #todo; test sce2t
    sc = ctypes.c_int(sc)
    et = ctypes.c_double(et)
    sclkdp = ctypes.c_double()
    libspice.sce2t_c(sc, et, ctypes.byref(sclkdp))
    return sclkdp.value


def scencd(sc, sclkch, MXPART=None):
    #todo: figure out how to use mxpart, and test scencd
    sc = ctypes.c_int(sc)
    sclkch = stypes.strtocharpoint(sclkch)
    sclkdp = ctypes.c_double()
    libspice.scencd_c(sc, sclkch, ctypes.byref(sclkdp))
    return sclkdp.value


def scfmt(sc, ticks, lenout):
    #Todo: test
    sc = ctypes.c_int(sc)
    ticks = ctypes.c_double(ticks)
    clkstr = stypes.strtocharpoint(lenout)
    lenout = ctypes.c_int(lenout)
    libspice.scfmt_c(sc, ticks, lenout, clkstr)
    return clkstr


def scpart(sc, nparts, pstart, MXPART=None):
    #todo: figure out how to use mxpart, and test scpart
    sc = ctypes.c_int(sc)
    nparts = ctypes.c_int(nparts)
    pstart = ctypes.c_double(pstart)
    pstop = ctypes.c_double()
    libspice.scpart_c(sc, nparts, pstart, ctypes.byref(pstop))
    return pstop.value


def scs2e(sc, sclkch):
    #todo: test scs2e
    sc = ctypes.c_int(sc)
    sclkch = stypes.strtocharpoint(sclkch)
    et = ctypes.c_double()
    libspice.scs2e_c(sc, sclkch, ctypes.byref(et))
    return et.value


def sct2e(sc, sclkdp):
    #todo: test scs2e
    sc = ctypes.c_int(sc)
    sclkdp = ctypes.c_double(sclkdp)
    et = ctypes.c_double()
    libspice.sct2e_c(sc, sclkdp, ctypes.byref(et))
    return et.value


def sctiks(sc, clkstr):
    #todo: test sctiks
    sc = ctypes.c_int(sc)
    clkstr = stypes.strtocharpoint(clkstr)
    ticks = ctypes.c_double()
    libspice.sctiks_c(sc, clkstr, ctypes.byref(ticks))
    return ticks.value

#sdiff
#set


def setmsg(message):
    #todo: test
    message = stypes.strtocharpoint(message)
    libspice.setmsg_c(message)
    pass


def shellc(ndim, lenvals, array):
    #Todo: fix, this does not work!
    array = stypes.listtocharvector(array)
    ndim = ctypes.c_int(ndim)
    lenvals = ctypes.c_int(lenvals)
    #libspice.shellc_c(ndim, lenvals, ctypes.cast(array, ctypes.c_void_p))
    pass


def shelld(ndim, array):
    #Todo: Works!, use this as example for "I/O" parameters
    array = stypes.listtodoublevector(array)
    ndim = ctypes.c_int(ndim)
    libspice.shelld_c(ndim, ctypes.cast(array, ctypes.POINTER(ctypes.c_double)))
    return stypes.vectortolist(array)


def shelli(ndim, array):
    #Todo: Works!, use this as example for "I/O" parameters
    array = stypes.listtointvector(array)
    ndim = ctypes.c_int(ndim)
    libspice.shelli_c(ndim, ctypes.cast(array, ctypes.POINTER(ctypes.c_int)))
    return stypes.vectortolist(array)


def sigerr(message):
    #todo: test
    message = stypes.strtocharpoint(message)
    libspice.sigerr_c(message)
    pass


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
    return {'spoint': stypes.vectortolist(spoint), 'trgepc': trgepc.value,
            'srfvec': stypes.vectortolist(srfvec), 'found': found.value}


#size


def spd():
    return libspice.spd_c()


def sphcyl(radius, colat, slon):
    radius = ctypes.c_double(radius)
    colat = ctypes.c_double(colat)
    slon = ctypes.c_double(slon)
    r = ctypes.c_double()
    lon = ctypes.c_double()
    z = ctypes.c_double()
    libspice.sphcyl_c(radius, colat, slon, ctypes.byref(r), ctypes.byref(lon), ctypes.byref(z))
    return r.value, lon.value, z.value


def sphlat(r, colat, lons):
    r = ctypes.c_double(r)
    colat = ctypes.c_double(colat)
    lons = ctypes.c_double(lons)
    radius = ctypes.c_double()
    lon = ctypes.c_double()
    lat = ctypes.c_double()
    libspice.sphcyl_c(r, colat, lons, ctypes.byref(radius), ctypes.byref(lon), ctypes.byref(lat))
    return radius.value, lon.value, lat.value


def sphrec(r, colat, lon):
    r = ctypes.c_double(r)
    colat = ctypes.c_double(colat)
    lon = ctypes.c_double(lon)
    rectan = stypes.doubleVector(3)
    libspice.sphrec_c(r, colat, lon, rectan)
    return stypes.vectortolist(rectan)


#skipped all of the functions starting with SPK for now

def srfrec(body, longitude, latitude):
    #Todo: test srfrec
    body = ctypes.c_int(body)
    longitude = ctypes.c_double(longitude)
    latitude = ctypes.c_double(latitude)
    rectan = stypes.doubleVector(3)
    libspice.srfrec_c(body, longitude, latitude, rectan)
    return stypes.vectortolist(rectan)


def srfxpt(method, target, et, abcorr, obsrvr, dref, dvec):
    #Todo: test srfxpt, but it is depricated
    method = stypes.strtocharpoint(method)
    target = stypes.strtocharpoint(target)
    et = ctypes.c_double(et)
    abcorr = stypes.strtocharpoint(abcorr)
    obsrvr = stypes.strtocharpoint(obsrvr)
    dref = stypes.strtocharpoint(dref)
    dvec = stypes.listtodoublevector(dvec)
    spoint = stypes.doubleVector(3)
    trgepc = ctypes.c_double()
    dist = ctypes.c_double()
    obspos = stypes.doubleVector(3)
    found = ctypes.c_bool()
    libspice.srfxpt_c(method, target, et, abcorr, obsrvr, dref, dvec,
                      spoint, ctypes.byref(dist), ctypes.byref(trgepc), obspos, ctypes.byref(found))
    return stypes.vectortolist(spoint), dist.value, trgepc.value, stypes.vectortolist(obspos), found.value


#ssize


def stelab(pobj, vobs):
    #Todo: test stelab
    pobj = stypes.listtodoublevector(pobj)
    vobs = stypes.listtodoublevector(vobs)
    appobj = stypes.doubleVector(3)
    libspice.stelab_c(pobj, vobs, appobj)
    return stypes.vectortolist(appobj)


def stpool(item, nth, contin, lenout):
    #Todo: test stpool
    item = stypes.strtocharpoint(item)
    contin = stypes.strtocharpoint(contin)
    nth = ctypes.c_int(nth)
    lenout = ctypes.c_int(lenout)
    strout = stypes.strtocharpoint(" "*lenout.value)
    found = ctypes.c_bool()
    size = ctypes.c_int()
    libspice.stpool_c(item, nth, contin, lenout, strout, ctypes.byref(size), ctypes.byref(found))
    return strout, size.value, found.value


def str2et(time):
    time = stypes.strtocharpoint(time)
    et = ctypes.c_double(0)
    libspice.str2et_c(time, ctypes.byref(et))
    return et.value


def subpnt(method, target, et, fixref, abcorr, obsrvr):
    #Todo: test subpnt
    method = stypes.strtocharpoint(method)
    target = stypes.strtocharpoint(target)
    et = ctypes.c_double(et)
    fixref = stypes.strtocharpoint(fixref)
    abcorr = stypes.strtocharpoint(abcorr)
    obsrvr = stypes.strtocharpoint(obsrvr)
    spoint = stypes.doubleVector(3)
    trgepc = ctypes.c_double(0)
    srfvec = stypes.doubleVector(3)
    libspice.subpnt_c(method, target, et, fixref, abcorr, obsrvr, spoint, ctypes.byref(trgepc), srfvec)
    return stypes.vectortolist(spoint), trgepc.value, stypes.vectortolist(srfvec)


def subpt(method, target, et, abcorr, obsrvr):
    #Todo: test subpt
    method = stypes.strtocharpoint(method)
    target = stypes.strtocharpoint(target)
    et = ctypes.c_double(et)
    abcorr = stypes.strtocharpoint(abcorr)
    obsrvr = stypes.strtocharpoint(obsrvr)
    spoint = stypes.doubleVector(3)
    alt = ctypes.c_double()
    libspice.subpt_c(method, target, et, abcorr, obsrvr, spoint, ctypes.byref(alt))
    return stypes.vectortolist(spoint), alt.value


def subslr(method, target, et, fixref, abcorr, obsrvr):
    #Todo: test subslr
    method = stypes.strtocharpoint(method)
    target = stypes.strtocharpoint(target)
    et = ctypes.c_double(et)
    fixref = stypes.strtocharpoint(fixref)
    abcorr = stypes.strtocharpoint(abcorr)
    obsrvr = stypes.strtocharpoint(obsrvr)
    spoint = stypes.doubleVector(3)
    trgepc = ctypes.c_double(0)
    srfvec = stypes.doubleVector(3)
    libspice.subslr_c(method, target, et, fixref, abcorr, obsrvr, spoint, ctypes.byref(trgepc), srfvec)
    return stypes.vectortolist(spoint), trgepc.value, stypes.vectortolist(srfvec)


def subsol(method, target, et, abcorr, obsrvr):
    #Todo: test subsol
    method = stypes.strtocharpoint(method)
    target = stypes.strtocharpoint(target)
    et = ctypes.c_double(et)
    abcorr = stypes.strtocharpoint(abcorr)
    obsrvr = stypes.strtocharpoint(obsrvr)
    spoint = stypes.doubleVector(3)
    libspice.subsol_c(method, target, et, abcorr, obsrvr, spoint)
    return stypes.vectortolist(spoint)


def sumad(array, n):
    array = stypes.listtodoublevector(array)
    n = ctypes.c_int(n)
    return libspice.sumad_c(array, n)


def sumai(array, n):
    array = stypes.listtointvector(array)
    n = ctypes.c_int(n)
    return libspice.sumai_c(array, n)


def surfnm(a, b, c, point):
    #Todo: test surfnm
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    point = stypes.listtodoublevector(point)
    normal = stypes.doubleVector(3)
    libspice.surfnm_c(a, b, c, point, normal)
    return stypes.vectortolist(normal)


def surfpt(positn, u, a, b, c):
    #Todo: test surfpt
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    positn = stypes.listtodoublevector(positn)
    u = stypes.listtodoublevector(u)
    point = stypes.doubleVector(3)
    found = ctypes.c_bool()
    libspice.surfpt_c(positn, u, a, b, c, point, ctypes.byref(found))
    return stypes.vectortolist(point), found.value


def surfpv(stvrtx, stdir, a, b, c):
    #Todo: test surfpv
    a = ctypes.c_double(a)
    b = ctypes.c_double(b)
    c = ctypes.c_double(c)
    stvrtx = stypes.listtodoublevector(stvrtx)
    stdir = stypes.listtodoublevector(stdir)
    stx = stypes.doubleVector(6)
    found = ctypes.c_bool()
    libspice.surfpv_c(stvrtx, stdir, a, b, c, stx, ctypes.byref(found))
    return stypes.vectortolist(stx), found.value

#swpool


def sxfrom(instring, tostring, et):
    #Todo: test sxform
    instring = stypes.strtocharpoint(instring)
    tostring = stypes.strtocharpoint(tostring)
    et = ctypes.c_double(et)
    xform = stypes.doubleMatrix(x=6, y=6)
    libspice.sxform_c(instring, tostring, et, xform)
    return stypes.matrixtolist(xform)


def szpool(name):
    name = stypes.strtocharpoint(name)
    n = ctypes.c_int()
    found = ctypes.c_bool(0)
    libspice.szpool_c(name, ctypes.byref(n), ctypes.byref(found))
    return n, found.value


########################################################################################################################
# T


def timdef(action, item, lenout, value=None):
    #todo: test
    action = stypes.strtocharpoint(action)
    item = stypes.strtocharpoint(item)
    lenout = ctypes.c_int(lenout)
    if value is None:
        value = stypes.strtocharpoint(" "*lenout.value)
    else:
        value = stypes.strtocharpoint(value)
    libspice.timdef_c(action, item, lenout, value)
    return value


def timout(et, pictur, lenout):
    #todo: test
    pictur = stypes.strtocharpoint(pictur)
    output = stypes.strtocharpoint(" " * lenout)
    et = ctypes.c_double(et)
    lenout = ctypes.c_int(lenout)
    libspice.timout_c(et, pictur, lenout, output)
    return output


def tipbod(ref, body, et):
    #Todo: test
    ref = stypes.strtocharpoint(ref)
    body = ctypes.c_int(body)
    et = ctypes.c_int(et)
    retmatrix = stypes.doubleMatrix()
    libspice.tipbod_c(ref, body, et, retmatrix)
    return stypes.matrixtolist(retmatrix)


def tisbod(ref, body, et):
    #Todo: test
    ref = stypes.strtocharpoint(ref)
    body = ctypes.c_int(body)
    et = ctypes.c_int(et)
    retmatrix = stypes.doubleMatrix(x=6, y=6)
    libspice.tisbod_c(ref, body, et, retmatrix)
    return stypes.matrixtolist(retmatrix)


def tkvrsn(item):
    item = stypes.strtocharpoint(item)
    return libspice.tkvrsn_c(item)


def tparse(instring, lenout):
    #Todo: test
    errmsg = stypes.strtocharpoint(lenout)
    lenout = ctypes.c_int(lenout)
    instring = stypes.strtocharpoint(instring)
    sp2000 = ctypes.c_double()
    libspice.tparse_c(instring, lenout, ctypes.POINTER(sp2000), errmsg)
    return sp2000.value, errmsg


def tpictr(sample, lenout, lenerr):
    #Todo: test
    sample = stypes.strtocharpoint(sample)
    pictur = stypes.strtocharpoint(lenout)
    errmsg = stypes.strtocharpoint(lenerr)
    lenout = ctypes.c_int(lenout)
    lenerr = ctypes.c_int(lenerr)
    ok = ctypes.c_bool()
    libspice.tpictr_c(sample, lenout, lenerr, pictur, ctypes.POINTER(ok), errmsg)
    return pictur, ok.value, errmsg


def trace(matrix):
    #Todo: test
    matrix = stypes.listtodoublematrix(matrix)
    return libspice.trace_c(matrix)


def trcoff():
    #Todo: test
    libspice.trcoff_c()
    pass


def tsetyr(year):
    #Todo: test
    year = ctypes.c_int(year)
    libspice.tsetyr(year)
    pass


def twopi():
    return libspice.twopi_c()


def twovec(axdef, indexa, plndef, indexp):
    #Todo: Test
    axdef = stypes.listtodoublevector(axdef)
    indexa = ctypes.c_int(indexa)
    plndef = stypes.listtodoublevector(plndef)
    indexp = ctypes.c_int(indexp)
    mout = stypes.doubleMatrix()
    libspice.twovec_c(axdef, indexa, plndef, indexp, mout)
    return stypes.matrixtolist(mout)


def tyear():
    #Todo: Test
    return libspice.tyear_c()


########################################################################################################################
# U

def ucase(inchar, lenout):
    inchar = stypes.strtocharpoint(inchar)
    outchar = stypes.strtocharpoint(lenout)
    lenout = ctypes.c_int(lenout)
    libspice.ucase_c(inchar, lenout, outchar)
    return outchar.value


def ucrss(v1, v2):
    #Todo: test
    v1 = stypes.listtodoublevector(v1)
    v2 = stypes.listtodoublevector(v2)
    vout = stypes.doubleVector(3)
    libspice.ucrss_c(v1, v2, vout)
    return stypes.vectortolist(vout)


#UDDC # callback?


#UDDF # callback?


#UNION # cells


def unitim(epoch, insys, outsys):
    #Todo: test
    epoch = ctypes.c_double(epoch)
    insys = stypes.strtocharpoint(insys)
    outsys = stypes.strtocharpoint(outsys)
    return libspice.unitim_c(epoch, insys, outsys)


def unload(filename):
    filename = stypes.strtocharpoint(filename)
    libspice.unload_c(filename)
    pass


def unorm(v1):
    v1 = stypes.listtodoublevector(v1)
    vout = stypes.doubleVector(3)
    vmag = ctypes.c_double(0)
    libspice.unorm_c(v1, vout, ctypes.byref(vmag))
    return stypes.vectortolist(vout), vmag.value


def unormg(v1, ndim):
    v1 = stypes.listtodoublevector(v1)
    vout = stypes.doubleVector(ndim)
    vmag = ctypes.c_double(0)
    ndim = ctypes.c_int(ndim)
    libspice.unormg_c(v1, ndim, vout, ctypes.byref(vmag))
    return stypes.vectortolist(vout), vmag.value


def utc2et(utcstr):
    #Todo: test
    utcstr = stypes.strtocharpoint(utcstr)
    et = ctypes.c_double(0)
    libspice.utc2et_c(utcstr, ctypes.byref(et))
    return et.value
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

def xf2eul(xform, axisa, axisb, axisc):
    #Todo: tes
    xform = stypes.listtodoublematrix(xform, x=6, y=6)
    axisa = ctypes.c_int(axisa)
    axisb = ctypes.c_int(axisb)
    axisc = ctypes.c_int(axisc)
    eulang = stypes.doubleVector(6)
    unique = ctypes.c_bool()
    libspice.xf2eul_c(xform, axisa, axisb, axisc, eulang, unique)
    return eulang, unique


def xf2rav(xform):
    #Todo: test
    xform = stypes.listtodoublematrix(xform, x=6, y=6)
    rot = stypes.doubleMatrix()
    av = stypes.doubleVector(3)
    libspice.xf2rav_c(xform, rot, av)
    return rot, av


def xpose(m):
    m = stypes.listtodoublematrix(m)
    mout = stypes.doubleMatrix()
    libspice.xpose_c(m, mout)
    return stypes.matrixtolist(m)


def xpose6(m):
    #Todo: test
    m = stypes.listtodoublematrix(m, x=6, y=6)
    mout = stypes.doubleMatrix(x=6, y=6)
    libspice.xpose6_c(m, mout)
    return stypes.matrixtolist(m)

# xposeg using void pointers, haven't attempted this yet

########################################################################################################################
# Y


########################################################################################################################
# Z
