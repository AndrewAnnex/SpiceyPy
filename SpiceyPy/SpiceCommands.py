import numpy
from SpiceyPy.SpiceCell import SpiceCell
from SpiceyPy.SpiceHelpers import MaxAbs
from SpiceyPy.SpiceEllipse import Ellipse
from SpiceyPy.SpicePool import SpicePool


def appndc(item, cell):
    assert isinstance(cell, SpiceCell)
    cell.append(item)
    pass


def appndd(item, cell):
    #Append an item to a double precision cell.
    appndc(item, cell)
    pass


def axisar(axis, angle, r):
    #Construct a rotation matrix that rotates vectors by a specified angle about a specified axis.
    pass


def b1900():
    #Return the Julian Date corresponding to Besselian Date 1900.0.
    return 2415020.31352


def b1950():
    #Return the Julian Date corresponding to Besselian Date 1950.0.
    return 2433282.42345905


def badkpv(caller, name, comp, size, divby, typeParam):
    #Determine if a kernel pool variable is present and if so that it has the correct size and type.
    pass


def bodc2n(code, name, found):
    #Translate the SPICE integer code of a body into a common name for that body.
    pass


def boddef(name, code):
    #Define a body name/ID code pair for later translation via bodn2c_c or bodc2n_c.
    pass


def bodfnd(body, item):
    #Determine whether values exist for some item for any body in the kernel pool.
    pass


def bodn2c(name, code, found):
    #Translate the name of a body or object to the corresponding SPICE integer ID code.
    pass


def bodvar(body, item, dim, values):
    pool = SpicePool()
    #Return the values of some item for any body in the kernel pool.
    code = pool.intstr(body)
    varname = 'BODY'
    varname = suffix(code, 0, varname)
    varname = suffix('_', 0, varname)
    varname = suffix(item, 0, varname)

    #Grab the items. Complain if they aren't there.
    values, found = pool.rtpool(varname, dim)
    return values


def bodvrd(bodynm, item, maxn, dim, values):
    #Fetch from the kernel pool the double precision values of an item associated with a body.
    pass


def brcktd(number, end1, end2):
    if number < end1:
        return end1
    elif number > end2:
        return end2
    return number


def brckti(number, end1, end2):
    return brcktd(number, end1, end2)


def bschoc(value, ndim, array, order):
    #Do a binary search for a given value within a character string array, accompanied by an order vector.
    pass


def bschoi(value, ndim, array, order):
    #Do a binary search for a given value within a integer array, accompanied by an order vector.
    pass


def bsrchc(value, ndim, array):
    #Do a binary earch for a given value within a character string array, accompanied by an order vector.
    pass


def bsrchd(value, ndim, array):
    #Do a binary earch for a given value within a double precision array, accompanied by an order vector.
    pass


def bsrchi(value, ndim, array):
    #Do a binary earch for a given value within a integer precision array, accompanied by an order vector.
    pass


def cardc(cell):
    #Return the cardinality (current number of elements):in a cell of any data type.
    assert isinstance(cell, SpiceCell)
    return cell.card()


def cgv2el(center, vec1, vec2):
    #Form a CSPICE ellipse from a center vector and two generating vectors.
    return Ellipse(center, vec1, vec2)


def chkin(module):
    #Inform the CSPICE error handling mechanism of entry into a routine.
    pass


def chkout(module):
    #Inform the CSPICE error handling mechanism of exit from a routine subsequent reference.
    pass


def cidfrm(cent, frcode, frname, found):
    #Retrieve frame ID code and name to associate with a frame center.
    pass


def ckcls(handle):
    #Close an open CK file.
    pass


def ckgp(inst, sclkdp, tol, ref, cmat, clkout, found):
    #Get pointing (attitude):for a specified spacecraft clock time
    pass


def ckgpav(inst, sclkdp, tol, ref, cmat, av, clkout, found):
    #Get pointing (attitude):for a specified spacecraft clock time
    pass


def cklpf(fname, handle):
    #Load a CK pointing file for use by the CK readers.
    pass


def ckopn(name, ifname, ncomch, handle):
    #Open a new CK file, returning the handle of the opened file
    pass


def ckupf(handle):
    #Unload a CK pointing file so that it will no longer be searched by the readers
    pass


def ckw01(handle, begtim, endtim, inst, ref, avflag, segid, nrec, sclkdp, quats, avvs):
    #Add a type 1 segment to a C-kernel
    pass


def ckw02(handle, begtim, endtim, inst, ref, segid, nrec, start, stop, quats, avvs, rates):
    #Write a type 2 segment to a C-kernel
    pass


def ckw03(handle, begtim, endtim, inst, ref, avflag, segid, nrec, sclkdp, quats, avvs, nints, starts):
    #Write CK segment type 3
    pass


def ckw05(handle, subtyp, degree, begtim, endtim, inst, ref, avflag, segid, n, sclkdp, packts, rate, nints, starts):
    #Write CK segment type 5
    pass


def clight():
    #Return the speed of light in a vacuum (IAU official value, in km/sec)
    return 299792.458


def clpool():
    #Remove all variables from the kernel pool
    pass


def cmprss(delim, n, input, output):
    #Compress a character string by removing occurrences of more than N consecutive occurrences of a specified character.
    pass


def cnmfrm(cname, frcode, frname, found):
    pass


def conics(elts, et, state):
    pass


def convrt(x, inParam, out, y):
    pass


def copyc(cell):
    return cell


def cpos(string, chars, start):
    assert(isinstance(chars, list))
    assert(isinstance(string, str))
    assert(isinstance(start, int))
    for char in chars:
        index = string.find(char, start)
        if index != -1:
            return index
    #else
    return 0


def cposr(string, chars, start):
    assert(isinstance(chars, list))
    assert(isinstance(string, str))
    assert(isinstance(start, int))
    for char in chars:
        index = string.rfind(char, start)
        if index != -1:
            return index
    #else
    return 0


def cvpool(agent, update):
    pass


def cyllat(r, longc, z):
    big = MaxAbs(r, z)
    if big > 0:
        x = r / big
        y = z / big
        rho = big * numpy.sqrt(x * x + y * y)
    else:
        rho = 0
    if rho == 0:
        lattitude = 0.0
    else:
        lattitude = numpy.arctan2(z, r)
    return tuple((longc, rho, lattitude))


def cylrec(r, longi, z):
    x = r * numpy.cos(longi)
    y = r * numpy.sin(longi)
    z = z
    return tuple((x, y, z))


def cylsph(r, longc, z):
    big = MaxAbs(r, z)
    if big == 0:
        th = 0
        rh = 0
    else:
        x = r / big
        y = z / big
        rh = big * numpy.sqrt(x * x + y * y)
        th = numpy.arctan2(r, z)
    return tuple((rh, th, longc))


def dafbbs(handle):
    pass


def dafbfs(handle):
    pass


def dafcls(handle):
    pass


def dafcs(handle):
    pass


def daffna(found):
    pass


def daffpa(found):
    pass


def dafgn(name):
    pass


def dafgs(sum):
    pass


def dafopr(fname, handle):
    pass


def dafrda(handle, begin, end, data):
    pass


def dafus(sum, nd, ni, dc, ic):
    pass


def dasac(handle, n, buffer):
    pass


def dasec(handle, bufsiz, n, buffer, done):
    pass


def dcyldr(x, y, z, jacobi):
    pass


def deltet(epoch, eptype, delta):
    pass


def det(matrix):
    return numpy.linalg.det(matrix)


def dgeodr(x, y, z, re, f, jacobi):
    pass


def diags2(symmat, diag, rotate):
    pass


def dlatdr(x, y, z, jacobi):
    pass


def dpr():
    return 180.0 / numpy.pi


def drdcyl(r, longi):
    return numpy.array([numpy.cos(longi), numpy.sin(longi), 0.0, numpy.sin(longi) * -1.0 * r, numpy.cos(longi)*r, 0.0, 0.0, 0.0, 1.0])


def drdgeo(longi, lat, alt, re, f, jacobi):
    pass


def drdlat(r, longi, lat, jacobi):
    pass


def drdsph(r, colat, longi, jacobi):
    pass


def dsphdr(x, y, z, jacobi):
    pass


def dtpool(name, found, n, typeParam):
    pass


def dvdot(s1, s2):
    #(x, y, z, dx/dt, dy/dt, dz/dt )
    return s1[0] * s2[3] + s1[1] * s2[4] + s1[2] * s2[5] + s1[3] * s2[0] + s1[4] * s2[1] + s1[5] * s2[2]


def dvhat(s1, sout):
    pass


def dvpool(name):
    pass


def edlimb(a, b, c, viewpt, limb):
    pass


def ekacec(handle, segno, recno, column, nvals, cvals, isnull):
    pass


def ekaced(handle, segno, recno, column, nvals, dvals, isnull):
    pass


def ekacei(handle, segno, recno, column, nvals, ivals, isnull):
    pass


def ekaclc(handle, segno, column, cvals, entszs, nlflgs, rcptrs, wkindx):
    pass


def ekacld(handle, segno, column, dvals, entszs, nlflgs, rcptrs, wkindx):
    pass


def ekacli(handle, segno, column, ivals, entszs, nlflgs, rcptrs, wkindx):
    pass


def ekappr(handle, segno, recno):
    pass


def ekbseg(handle, tabnam, ncols, cnames, decls, segno):
    pass


def ekccnt(table, ccount):
    pass


def ekcii(table, cindex, column, attdsc):
    pass


def ekcls(handle):
    pass


def ekdelr(handle, segno, recno):
    pass


def ekffld(handle, segno, rcptrs):
    pass


def ekfind(query, nmrows, error, errmsg):
    pass


def ekgc(selidx, row, elment, cdata, nulle, found):
    pass


def ekgd(selidx, row, elment, ddata, nulle, found):
    pass


def ekgi(selidx, row, elment, idata, nulle, found):
    pass


def ekifld(handle, tabnam, ncols, nrows, cnames, decls, segno, rcptrs):
    pass


def ekinsr(handle, segno, recno):
    pass


def eklef(fname, handle):
    pass


def eknelt(selidx, row, nelt):
    pass


def eknseg(handle):
    pass


def ekntab(n):
    pass


def ekopn(fname, ifname, ncomch, handle):
    pass


def ekopr(fname, handle):
    pass


def ekops(handle):
    pass


def ekopw(fname, handle):
    pass


def ekpsel(query, n, xbegs, xends, xtypes, xclasse, tabs, cols, error, errmsg):
    pass


def ekrcec(handle, segno, recno, column, nvals, cvals, isnull):
    pass


def ekrced(handle, segno, recno, column, nvals, dvals, isnull):
    pass


def ekrcei(handle, segno, recno, column, nvals, ivals, isnull):
    pass


def ekssum(handle, segno, tabnam, nrows, ncols, cnames, dtypes, sizes, strlns, indexd, nullok):
    pass


def ektnam(n, table):
    pass


def ekucec(handle, segno, recno, column, nvals, cvals, isnull):
    pass


def ekuced(handle, segno, recno, column, nvals, dvals, isnull):
    pass


def ekucei(handle, segno, recno, column, nvals, ivals, isnull):
    pass


def ekuef(handle):
    pass


def el2cgv(ellips, center, smajor, sminor):
    pass


def elemc(item, a):
    pass


def elemd(item, a):
    pass


def elemi(item, a):
    pass


def eqstr(a, b):
    pass


def erract(op, action):
    pass


def errch(marker, string):
    pass


def errdev(op, device):
    pass


def errdp(marker, dpnum):
    pass


def errint(marker, integr):
    pass


def errprt(op, listParam):
    pass


def esrchc(value, ndim, array):
    pass


def et2lst(et, body, longi, typeParam, hr, mn, sc, time, ampm):
    pass


def et2utc(et, formatParam, prec, utcstr):
    pass


def etcal(et, string):
    pass


def eul2m(angle3, angle2, angle1, axis3, axis2, axis1, r):
    pass


def eul2xf(eulang, axisa, axisb, axisc, xform):
    pass


def exists(file):
    try:
        with open(file):
            return True
    except IOError:
        return False


def expool(name):
    pass


def failed():
    pass


def frame(x, y, z):
    pass


def frinfo(frcode, cent, classe, clssid, found):
    pass


def frmnam(frcode, frname):
    pass


def furnsh(file):
    #Load one or more SPICE kernels into a program.
    pass


def gcpool(name, start, room, n, cvals, found):
    pass


def gdpool(name, start, room, n, values, found):
    pass


def georec(longi, lat, alt, re, f, rectan):
    pass


def getelm(frstyr, lines, epoch, elems):
    pass


def getfat(file, arch, kertyp):
    pass


def getfov(instid, room, shape, frame, bsight, n, bounds):
    pass


def getmsg(option, msg):
    pass


def gipool(name, start, room, n, ivals, found):
    pass


def gnpool(name, start, room, n, cvals, found):
    pass


def halfpi():
    return numpy.pi / 2


def ident(matrix):
    return numpy.identity(matrix)


def illum(target, et, abcorr, obsrvr, spoint, phase, solar, emissn):
    pass


def inedpl(a, b, c, plane, ellips, found):
    pass


def inelpl(ellips, plane, nxpts, xpt1, xpt2):
    pass


def inrypl(vertex, dirParam, plane, nxpts, xpt):
    pass


def insrtc(item, a):
    pass


def insrtd(item, a):
    pass


def insrti(item, a):
    pass


def invert(matrix1, mout):
    pass


def invort(m, mit):
    pass


def isordv(array, n):
    pass


def isrchc(value, ndim, array):
    pass


def isrchd(value, ndim, array):
    pass


def isrchi(value, ndim, array):
    pass


def isrot(m, ntol, dtol):
    if ntol < 0:
        pass  # error! should be non-negative
    elif dtol < 0:
        pass  # error! should be non-negative also

    mtrans = xpose(m)
    unit0, norm0 = unorm(mtrans[0])
    unit1, norm1 = unorm(mtrans[1])
    unit2, norm2 = unorm(mtrans[2])

    test0 = (norm0 == brcktd(norm0, 1 - ntol, 1 + ntol))
    test1 = (norm1 == brcktd(norm1, 1 - ntol, 1 + ntol))
    test2 = (norm2 == brcktd(norm2, 1 - ntol, 1 + ntol))
    normOK = test0 and test1 and test2
    d = det([unit0, unit1, unit2])
    detOK = (d == brcktd(d, 1 - dtol, 1 + dtol))
    return detOK & normOK


def j1900():
    """



    :rtype : float
    :return: the Julian Date of 1899 DEC 31 12:00:00 (1900 JAN 0.5)
    """
    return 2415020.0


def j1950():
    #Return the Julian Date of 1950 JAN 01 00:00:00 (1950 JAN 1.0)
    return 2433282.5


def j2000():
    #Return the Julian Date of 2000 JAN 01 12:00:00 (2000 JAN 1.5)
    return 2451545.0


def j2100():
    #Return the Julian Date of 2100 JAN 01 12:00:00 (2100 JAN 1.5)
    return 2488070.0


def jyear():
    #Return the number of seconds in a julian year.
    return 31557600.0


def kdata(which, kind, file, filtyp, source, handle, found):
    #Determine if a kernel pool variable is present and if so that it has the correct size and type.
    pass


def kinfo(file, filtyp, source, handle, found):
    #Return information about a loaded kernel specified by name.
    pass


def ktotal(kind, count):
    #Return the current number of kernels that have been loaded via the KEEPER interface that are of a specified type.
    pass


def kxtrct(keywd, terms, nterms, string, found, substr):
    pass


def lastnb(string):
    #Return the zero based index of the last non-blank character in
    #a character string.
    if string is None or len(string) is 0:
        return -1
    else:
        return len(string.strip()) - 1


def latcyl(radius, longi, lat):
    # r, longc, z
    rh = radius * numpy.cos(lat)
    zz = radius * numpy.sin(lat)
    return tuple((longi, rh, zz))


def latrec(radius, longi, lat):
    rectang = numpy.array([[0.0], [0.0], [0.0]])
    rectang[0] = radius * numpy.cos(longi) * numpy.cos(lat)
    rectang[1] = radius * numpy.sin(longi) * numpy.cos(lat)
    rectang[2] = radius * numpy.sin(lat)
    return rectang


def latsph(radius, longi, lat):
    #, rho, colat, longs
    colat = halfpi() - lat
    longs = longi
    rho = radius
    return tuple((rho, colat, longs))


def lcase(inv):
    #Convert the characters in a string to lowercase.
    return inv.lower()


def ldpool(kernel):
    pass


def lmpool(cvals, n):
    pass


def lparse(listParam, delim, nmax, n, items):
    pass


def lparsm(listParam, delims, nmax, n, items):
    pass


def lparss(listParam, delims, setParam):
    pass


def lstlec(string, n, array):
    pass


def lstled(x, n, array):
    pass


def lstlei(x, n, array):
    pass


def lstltc(string, n, array):
    pass


def lstltd(x, n, array):
    pass


def lstlti(x, n, array):
    pass


def ltime(etobs, obs, dirParam, targ, ettarg, elapsd):
    pass


def lx4dec(string, first, last, nchar):
    pass


def lx4num(string, first, last, nchar):
    pass


def lx4sgn(string, first, last, nchar):
    pass


def lx4uns(string, first, last, nchar):
    pass


def lxqstr(string, qchar, first, last, nchar):
    pass


def m2eul(r, axis3, axis2, axis1, angle3, angle2, angle1):
    pass


def m2q(r):
    #check if r is a rotation matrix
    assert isinstance(r, numpy.array)
    if not isrot(r, 0.1, 0.1):
        raise Exception
    r = r.flatten()
    tra = r[0] + r[4] + r[8]
    mtrace = 1 - tra
    cc4 = tra + 1
    s11 = mtrace + r[0] * 2
    s22 = mtrace + r[1] * 2
    s33 = mtrace + r[8] * 2
    if cc4 >= 1.0:
        c = numpy.sqrt(cc4 * 0.25)
        factor = 1.0 // (c * 4)
        s = numpy.array([r[5] - r[7], r[6] - r[2], r[1] - r[3]]) * factor
    elif s11 >= 1.0:
        s = numpy.zeros(3)
        s[0] = numpy.sqrt(s11 * 0.25)
        factor = 1.0 // (s[0] * 4)
        c = (r[5] - r[7]) * factor
        s[1] = (r[3] + r[1]) * factor
        s[2] = (r[6] + r[2]) * factor
    elif s22 >= 1.0:
        s = numpy.zeros(3)
        s[1] = numpy.sqrt(s22 * 0.25)
        factor = 1.0 // (s[1] * 4)
        c = (r[6] - r[2]) * factor
        s[0] = (r[3] + r[1]) * factor
        s[2] = (r[7] + r[5]) * factor
    else:
        s = numpy.zeros(3)
        s[2] = numpy.sqrt(s33 * 0.25)
        factor = 1.0 // (s[2] * 4)
        c = (r[1] - r[3]) * factor
        s[0] = (r[6] + r[2]) * factor
        s[1] = (r[7] + r[5]) * factor
    #cleanup
    l = c ^ 2 * s[0] ^ 2 + s[1] ^ 2 + s[2] ^ 2
    q = numpy.zeros(4)
    if l != 1.0:
        polish = 1 / numpy.sqrt(l)
        c *= polish
        s *= polish
    if c > 0:
        q[0] = c
        q[1] = s[0]
        q[2] = s[1]
        q[3] = s[3]
    else:
        q[0] = c
        q[1] = s[0]
        q[2] = s[1]
        q[3] = s[3]
        q *= -1.0
    return q


def matchi(string, templ, wstr, wchr):
    pass


def matchw(string, templ, wstr, wchr):
    pass


def mequ(matrix1):
    return matrix1


def mequg(matrix1):
    return matrix1


def mtxm(matrix1, matrix2):
    return numpy.dot(matrix1, matrix2)


def mtxmg(matrix1, matrix2):
    return numpy.dot(matrix1.T, matrix2)


def mtxv(matrix, vin):
    return numpy.dot(matrix.T, vin)


def mtxvg(matrix1, v2):
    return numpy.dot(matrix1.T, v2)


def mxm(matrix1, matrix2):
    return numpy.dot(matrix1, matrix2)


def mxmg(matrix1, matrix2):
    return numpy.dot(matrix1, matrix2)


def mxmt(matrix1, matrix2):
    return numpy.dot(matrix1, matrix2.T)


def mxmtg(matrix1, matrix2):
    return numpy.dot(matrix1, matrix2.T)


def mxv(matrix, vin):
    return numpy.dot(matrix, vin)


def mxvg(matrix1, v2):
    return numpy.dot(matrix1, v2)


def namfrm(frname, frcode):
    pass


def ncpos(string, chars, start):
    pass


def ncposr(string, chars, start):
    pass


def nearpt(positn, a, b, c):
    #This routine locates the point on the surface of an ellipsoid
    #that is nearest to a specified position. It also returns the
    #altitude of the position above the ellipsoid.
    #return npoint, alt
    pass


def npedln(a, b, c, linept, linedr, pnear, dist):
    pass


def npelpt(point, ellips, pnear, dist):
    pass


def nplnpt(linpt, lindirParam, point, pnear, dist):
    pass


def nvc2pl(normal, constante, plane):
    pass


def nvp2pl(normal, point, plane):
    pass


def ordc(item, setParam):
    pass


def ordd(item, setParam):
    pass


def orderc(array, ndim, iorder):
    pass


def orderd(array, ndim, iorder):
    pass


def orderi(array, ndim, iorder):
    pass


def ordi(item, setParam):
    pass


def oscelt(state, et, mu, elts):
    pass


def pcklof(fname, handle):
    pass


def pckuof(handle):
    pass


def pcpool(name, n, cvals):
    pass


def pdpool(name, n, values):
    pass


def pi():
    return numpy.pi


def pipool(name, n, ivals):
    pass


def pjelpl(elin, plane, elout):
    pass


def pl2nvc(plane, normal, constante):
    pass


def pl2nvp(plane, normal, point):
    pass


def pl2psv(plane, point, span1, span2):
    pass


def pos(string, substr, start):
    return string.find(substr, start)


def posr(string, substr, start):
    return string.rfind(substr, start)


def prompt(prmpt):
    #This function prompts a user for keyboard input.
    return input(prmpt)


def prop2b(gm, pvinit, dt, pvprop):
    pass


def prsdp(string, dpval):
    pass


def prsint(string, intval):
    pass


def psv2pl(point, span1, span2, plane):
    pass


def pxform(fromParam, to, et, rotate):
    pass


def q2m(q):
    q01 = q[0] * q[1]
    q02 = q[0] * q[2]
    q03 = q[0] * q[3]
    q12 = q[1] * q[2]
    q13 = q[1] * q[3]
    q23 = q[2] * q[3]
    q1s = q[1] * q[1]
    q2s = q[2] * q[2]
    q3s = q[3] * q[3]

    l2 = q[0] * q[0] + q1s + q2s + q3s

    if l2 != 1 and l2 != 0:
        sharp = 1 / l2
        q01 *= sharp
        q02 *= sharp
        q03 *= sharp
        q12 *= sharp
        q13 *= sharp
        q23 *= sharp
        q1s *= sharp
        q2s *= sharp
        q3s *= sharp

    #returns the numpy matrix transposed as required (the T at the end)
    return numpy.asmatrix([[1. - (q2s + q3s) * 2., (q12 + q03) * 2., (q13 - q02) * 2.],
                           [(q12 - q03) * 2., 1. - (q1s + q3s) * 2., (q23 + q01) * 2.],
                           [(q13 + q02) * 2., (q23 - q01) * 2., 1. - (q1s + q2s) * 2.]]).T


def radrec(rangeparam, ra, dec):
    return latrec(rangeparam, ra, dec)


def rav2xf(rot, av):
    xform = numpy.zeros((6, 6))
    for i in range(3):
        for j in range(3):
            xform[i, j] = rot[i, j]
            xform[i+3, j+3] = rot[i, j]
            xform[i, j+3] = 0.0

    omega = numpy.array([[0, -av[3], av[2]], [av[3], 0, -av[1]], [-av[2], av[1], 0]])
    drotd = mxm(rot, omega)
    for i in range(3):
        for j in range(3):
            xform[i+3, j] = drotd[i, j]

    return xform


def raxisa(matrix):
    #Compute the axis of the rotation given by an input matrix
    #and the angle of the rotation about that axis.
    quat = m2q(matrix)
    if vzero(quat[1]):
        angle = 0
        axis = numpy.array([0.0, 0.0, 1.0])
    elif quat[0] == 0:
        angle = pi()
        axis = quat[0:3]
    else:
        axis = vhat(quat[1])
        angle = 2.0 * numpy.arctan2()
    return axis, angle


def rdtext(file, line, eof):
    pass


#Todo: make this one work
def reccyl(rectan):
    # r, longi, z
    big = 1  # MaxAbs(rectan[0], rectan[1])
    z = rectan[2]
    r = 0
    lon = 0
    if big == 0:
        return tuple((r, lon, z))
    else:
        x = rectan[0] / big
        y = rectan[1] / big
        r = big * numpy.sqrt(x * x + y * y)
        lon = numpy.arctan2(y, x)
        if lon < 0.0:
            lon += twopi()
    return tuple((r, lon, z))


def recgeo(rectan, re, f):
    #Convert from rectangular coordinates to geodetic coordinates.
    if re <= 0:
        raise Exception
    if f >= 1:
        raise Exception
    temp_a = re
    temp_b = re
    temp_c = re - f*re
    base, alt = nearpt(rectan, temp_a, temp_b, temp_c)
    normal = surfnm(temp_a,temp_b,temp_c, base)
    long, lat = reclat(normal)
    return long, lat, alt


def reclat(rectan):
    vmax = MaxAbs(rectan[0], MaxAbs(rectan[1], rectan[2]))
    if vmax > 0:
        x1 = rectan[0]/vmax
        y1 = rectan[1]/vmax
        z1 = rectan[2]/vmax
        radius = vmax * numpy.sqrt(x1*x1 + y1*y1 + z1*z1)
        latitude = numpy.arctan2(z1, numpy.sqrt(x1*x1 + y1*y1))
        longitude = 0
        if x1 != 0 or y1 != 0:
            longitude = numpy.arctan2(y1, x1)
        return tuple((radius, latitude, longitude))
    else:
        return tuple((0, 0, 0))


def recrad(rectan):
    tempreturn = reclat(rectan)
    if tempreturn[1] < 0:
        return tuple((tempreturn[0], tempreturn[1]+twopi(), tempreturn[2]))
    return tempreturn


def recsph(rectan):
    big = MaxAbs(rectan[0], MaxAbs(rectan[1], rectan[2]))
    if big > 0:
        x1 = rectan[0]/big
        y1 = rectan[1]/big
        z1 = rectan[2]/big
        radius = big * numpy.sqrt(x1 * x1 + y1 * y1 + z1 * z1)
        colat = numpy.arctan2(numpy.sqrt(x1 * x1 + y1 * y1), z1)
        longi = 0.0
        if rectan[0] != 0 or rectan[1] != 0:
            longi = numpy.arctan2(rectan[1], rectan[0])
        return tuple((radius, colat, longi))


def removc(item, a):
    pass


def removd(item, a):
    pass


def removi(item, a):
    pass


def reordc(iorder, ndim, array):
    pass


def reordd(iorder, ndim, array):
    pass


def reordi(iorder, ndim, array):
    pass


def reordl(iorder, ndim, array):
    pass


def repmc(inParam, marker, value, out):
    pass


def repmct(inParam, marker, value, cases, out):
    pass


def repmd(inParam, marker, value, sigdig, out):
    pass


def repmf(inParam, marker, value, sigdig, formatParam, out):
    pass


def repmi(inParam, marker, value, out):
    pass


def repmot(inParam, marker, value, cases, out):
    pass


def resetParam():
    pass


def returne():
    pass


def rotate(angle, iaxis, mout):
    pass


def rotmat(matrix1, angle, iaxis, mout):
    pass


def rotvec(v1, angle, iaxis, vout):
    pass


def rpd():
    #Return the number of radians per degree.
    return numpy.pi / 180.0


def rquad(a, b, c):
    #Find the roots of a quadratic equation.
    roots = numpy.roots([a, b, c])
    real = numpy.real(roots)
    imag = numpy.imag(roots)
    return numpy.array([[real[0], imag[0]], [real[1], imag[1]]])


def saelgv(vec1, vec2, smajor, sminor):
    pass


def scdecd(sc, sclkdp, sclkch):
    pass


def sce2c(sc, et, sclkdp):
    pass


def sce2s(sc, et, sclkch):
    pass


def sce2t(sc, et, sclkdp):
    pass


def scencd(sc, sclkch, sclkdp):
    pass


def scfmt(sc, ticks, clkstr):
    pass


def scpart(sc, nparts, pstart, pstop):
    pass


def scs2e(sc, sclkch, et):
    pass


def sct2e(sc, sclkdp, et):
    pass


def sctiks(sc, clkstr, ticks):
    pass


def setParamc(a, op, b):
    pass


def setParammsg(msg):
    pass


def shellc(ndim, array):
    pass


def shelld(ndim, array):
    pass


def shelli(ndim, array):
    pass


def sigerr(msg):
    pass


def sizec(cell):
    pass


def spd():
    #Return the number of seconds in a day.
    return 86400.0


def sphcyl(radius, colat, slongi):
    # This returns the cylindrical coordinates of a point whose
    # position is input through spherical coordinates
    #TODO: replace numpy math with python math
    return radius*numpy.sin(colat), slongi, radius*numpy.cos(colat)


def sphlat(r, colat, longs):
    #Convert from spherical coordinates to latitudinal coordinates.
    return r, longs, colat-halfpi()


def sphrec(r, colat, longi):
    #Convert from spherical coordinates to rectangular coordinates.
    return r*numpy.cos(longi)*numpy.sin(colat), r*numpy.sin(longi)*numpy.sin(colat), r*numpy.cos(colat)


def spk14a(handle, ncsetParams, coeffs, epochs):
    pass


def spk14b(handle, segid, body, center, frame, first, last, chbdeg):
    pass


def spk14e(handle):
    pass


def spkapo(targ, et, ref, sobs, abcorr, ptarg, lt):
    pass


def spkapp(targ, et, ref, sobs, abcorr, starg, lt):
    pass


def spkcls(handle):
    pass


def spkez(targ, et, ref, abcorr, obs, starg, lt):
    pass


def spkezp(targ, et, ref, abcorr, obs, ptarg, lt):
    pass


def spkezr(targ, et, ref, abcorr, obs, starg, lt):
    pass


def spkgeo(targ, et, ref, obs, state, lt):
    pass


def spkgps(targ, et, ref, obs, pos, lt):
    pass


def spkopa(file, handle):
    pass


def spkopn(name, ifname, ncomch, handle):
    pass


def spkpds(body, center, frame, typeParam, first, last, descr):
    pass


def spkpos(targ, et, ref, abcorr, obs, ptarg, lt):
    pass


def spkssb(targ, et, ref, starg):
    pass


def spksub(handle, descr, ident, begin, end, newh):
    pass


def spkuds(descr, body, center, frame, typeParam, first, last, begin, end):
    pass


def spkuef(handle):
    pass


def spkw01(handle, body, center, frame, first, last, segid, n, dlines, epochs):
    pass


def spkw02(handle, body, center, frame, first, last, segid, intlen, n, polydg, cdata, btime):
    pass


def spkw03(handle, body, center, frame, first, last, segid, intlen, n, polydg, cdata, btime):
    pass


def spkw05(handle, body, center, frame, first, last, segid, gm, n, states, epochs):
    pass


def spkw08(handle, body, center, frame, first, last, segid, degree, n, states, epoch1, step):
    pass


def spkw09(handle, body, center, frame, first, last, segid, degree, n, states, epochs):
    pass


def spkw10(handle, body, center, frame, first, last, segid, consts, n, elems, epochs):
    pass


def spkw12(handle, body, center, frame, first, last, segid, degree, n, states, epoch1, step):
    pass


def spkw13(handle, body, center, frame, first, last, segid, degree, n, states, epochs):
    pass


def spkw15(handle, body, center, frame, first, last, segid, epoch, tp, pa, p, ecc, j2flg, pv, gm, j2, radius):
    pass


def spkw17(handle, body, center, frame, first, last, segid, epoch, eqel, rapol, decpol):
    pass


def spkw18(handle, subtyp, body, center, frame, first, last, segid, degree, n, packts, epochs):
    pass


def srfxpt(method, target, et, abcorr, obsrvr, dref, dvec, spoint, dist, trgepc, obspos, found):
    pass


def stelab(pobj, vobs, appobj):
    pass


def stpool(item, nth, contin, string, size, found):
    pass


def str2et(string, et):
    pass


def subpt(method, target, et, abcorr, obsrvr, spoint, alt):
    pass


def subsol(method, target, et, abcorr, obsrvr, spoint):
    pass


def suffix(suff, spaces, string):
    assert(isinstance(suff, str))
    assert(isinstance(spaces, int))
    assert(isinstance(string, str))
    slen = len(string)
    loc = lastnb(string)
    end = loc + max(spaces, 0)
    if end < slen:
        string = string[end+1:]+suff
    return string[:slen]


def sumad(array, n):
    pass


def sumai(array, n):
    pass


def surfnm(a, b, c, point, normal):
    pass


def surfpt(positn, u, a, b, c, point, found):
    pass


def swpool(agent, nnames, names):
    pass


def szpool(name, n, found):
    pass


def timdef(action, item, value):
    pass


def timout(et, pictur, output):
    pass


def tipbod(ref, body, et, tipm):
    pass


def tisbod(ref, body, et, tsipm):
    pass


def tkvrsn(item, verstr):
    pass


def tparse(string, sp2000, error):
    pass


def tpictr(sample, pictur, ok, errorn):
    pass


def trace(matrix):
    return numpy.trace(matrix)


def trcoff():
    pass


def tsetParamyr(year):
    pass


def twopi():
    #Return twice the value of pi (the ratio of the circumference of a circle to its diameter)
    return numpy.pi * 2


def twovec(axdef, indexa, plndef, indexp, mout):
    pass


def tyear():
    #Return the number of seconds in a tropical year.
    return 31556925.9747


def ucase(inparam):
    assert isinstance(inparam, str)
    return inparam.upper()


def ucrss(v1, v2):
    assert(isinstance(v1, numpy.ndarray))
    assert(isinstance(v2, numpy.ndarray))
    return numpy.cross(v1, v2)/numpy.dot(v1, v2)


def unitim(epoch, insys, outsys):
    pass


def unload(file):
    #Unload a SPICE kernel.
    pass


def unorm(v1):
    vmag = vnorm(v1)
    vout = v1
    if vmag > 0.0:
        vout /= vmag
        return tuple((vout, vmag))
    else:
        return tuple((numpy.zeros_like(vout), vmag))


def unormg(v1):
    return unorm(v1)


def utc2et(utcstr, et):
    #Convert an input time from Calendar or Julian Date format, UTC, to ephemeris seconds past J2000.
    pass


def vadd(v1, v2):
    return v1 + v2


def vaddg(v1, v2):
    return vadd(v1, v2)


def validc(size, n, a=None):
    pass


def vcrss(v1, v2):
    return numpy.cross(v1, v2)


def vdist(v1, v2):
    diff = vsub(v1, v2)
    return vnorm(diff)


def vdistg(v1, v2):
    return vdist(v1, v2)


def vdot(v1, v2):
    return numpy.dot(v1, v2)


def vdotg(v1, v2):
    return vdot(v1, v2)


def vequ(vin):
    return vin


def vequg(vin):
    return vin


def vhat(v1):
    mag = vnorm(v1)
    if mag > 0.0:
        return v1 / mag
    else:
        return numpy.zeros_like(v1)


def vhatg(v1):
    return vhat(v1)


def vlcom(a, v1, b, v2):
    return a * v1 + b * v2


def vlcom3(a, v1, b, v2, c, v3):
    return a*v1 + b*v2 + c*v3


def vlcomg(a, v1, b, v2):
    return vlcom(a, v1, b, v2)


def vminug(vin):
    return vminus(vin)


def vminus(v1):
    return numpy.negative(v1)


def vnorm(v1):
    return numpy.linalg.norm(v1)


def vnormg(v1):
    return vnorm(v1)


def vpack(x, y, z):
    return numpy.array([[x], [y], [z]])


def vperp(a, b):
    biga = MaxAbs(a[0], MaxAbs(a[1], a[2]))
    bigb = MaxAbs(b[0], MaxAbs(b[1], b[2]))
    if biga == 0 or bigb == 0:
        return tuple((0.0, 0.0, 0.0))
    t = vscl(1.0/biga, a)
    r = vscl(1.0/bigb, b)
    v = vproj(t, r)
    p = vsub(t, v)
    return vscl(biga, p)


def vprjp(vin, plane):
    normal, const = pl2nvc(plane)
    return vlcom(1.0, vin, const - vdot(vin, normal), normal)


def vprjpi(vin, projpl, invpl, vout, found):
    pass


def vproj(a, b):
    biga = MaxAbs(a[0], MaxAbs(a[1], a[2]))
    bigb = MaxAbs(b[0], MaxAbs(b[1], b[2]))
    if biga == 0 or bigb == 0:
        return tuple((0.0, 0.0, 0.0))
    t = vscl(1.0/biga, a)
    r = vscl(1.0/bigb, b)
    scale = vdot(t, r) * biga / vdot(r, r)
    return vscl(scale, r)


def vrel(v1, v2):
    nunorm = vdist(v1, v2)
    if nunorm == 0.0:
        return 0.0
    else:
        denorm = max(vnorm(v1), vnorm(v2))
        return nunorm/denorm


def vrelg(v1, v2):
    return vrel(v1, v2)


def vrotv(v, axis, theta):
    if vnorm(axis) == 0.0:
        return v
    x = vhat(axis)
    p = vproj(v, x)
    v1 = vsub(v, p)
    v2 = vcrss(x, v1)
    c = numpy.cos(theta)
    s = numpy.sin(theta)
    rplane = vlcom(c, v1, s, v2)
    return vadd(rplane, p)


def vscl(s, v1):
    return numpy.array(v1) * s


def vsclg(s, v1):
    return vscl(s, v1)


def vsep(v1, v2):
    u1 = unorm(v1)
    u2 = unorm(v2)
    if u1[1] == 0.0:
        return 0.0
    if u2[1] == 0.0:
        return 0.0
    if vdot(u1[0], u2[0]) > 0.0:
        vtemp = u1[0] - u2[0]
        return 2.0 * numpy.arcsin(0.50 * vnorm(vtemp))
    elif vdot(u1[0], u2[0]) < 0:
        vtemp = u1[0] + u2[0]
        return pi() - 2.0 * numpy.arcsin(0.50 * vnorm(vtemp))
    else:
        return halfpi()
    pass


def vsepg(v1, v2):
    return vsep(v1, v2)


def vsub(v1, v2):
    return v1 - v2


def vsubg(v1, v2):
    return vsub(v1, v2)


def vtmv(v1, matrix, v2):
    return numpy.dot(numpy.dot(v1.T, matrix), v2).flatten()


def vtmvg(v1, matrix, v2):
    return vtmv(v1, matrix, v2)


def vupack(v):
    return tuple((v[0], v[1], v[2]))


def vzero(v):
    assert type(v) is numpy.ndarray
    return v.any() is False


def vzerog(v):
    return vzero(v)


def wncomd(left, right, window, result):
    pass


def wncond(left, right, window):
    pass


def wndifd(a, b, c):
    pass


def wnelmd(point, window):
    pass


def wnexpd(left, right, window):
    pass


def wnextd(side, window):
    pass


def wnfetd(window, n, left, right):
    pass


def wnfild(small, window):
    pass


def wnfltd(small, window):
    pass


def wnincd(left, right, window):
    pass


def wninsd(left, right, window):
    pass


def wnintd(a, b, c):
    pass


def wnreld(a, op, b):
    pass


def wnsumd(window, meas, avg, stddev, shortt, longi):
    pass


def wnunid(a, b, c):
    pass


def wnvald(size, n, a):
    pass


def xf2eul(xform, axisa, axisb, axisc, eulang, unique):
    pass


def xf2rav(xform, rot, av):
    pass


def xpose(matrix1):
    return matrix1.T


def xposeg(matrix):
    return xpose(matrix)