__author__ = 'Apollo117'
import pytest

import SpiceyPy as spice
import numpy as np
import numpy.testing as npt
import os
cwd = os.path.realpath(os.path.dirname(__file__))
_testKernelPath = cwd + "/testKernels.txt"


def test_appndc():
    assert 1


def test_appndd():
    testCell = spice.stypes.SPICEDOUBLE_CELL(8)
    spice.appndd(1.0, testCell)
    spice.appndd(2.0, testCell)
    spice.appndd(3.0, testCell)
    assert [x for x in testCell] == [1.0, 2.0, 3.0]


def test_appndi():
    testCell = spice.stypes.SPICEINT_CELL(8)
    spice.appndi(1, testCell)
    spice.appndi(2, testCell)
    spice.appndi(3, testCell)
    assert [x for x in testCell] == [1, 2, 3]


def test_axisar():
    axis = np.array([0.0, 0.0, 1.0])
    outmatrix = spice.axisar(axis, spice.halfpi())
    expected = np.array(
        [[0.0, -1.0, 0.0],
         [1.0, 0.0, 0.0],
         [0.0, 0.0, 1.0]]
    )
    np.testing.assert_array_almost_equal(expected, outmatrix, decimal=6)


def test_b1900():
    assert spice.b1900() == 2415020.31352


def test_b1950():
    assert spice.b1950() == 2433282.42345905


def test_badkpv():
    assert 1


def test_bodc2n():
    spice.furnsh(_testKernelPath)
    assert spice.bodc2n(399, 10) == "EARTH"
    assert spice.bodc2n(0, 40) == "SOLAR SYSTEM BARYCENTER"
    spice.kclear()


def test_bodc2s():
    spice.furnsh(_testKernelPath)
    assert spice.bodc2s(399, 10) == "EARTH"
    assert spice.bodc2s(0, 40) == "SOLAR SYSTEM BARYCENTER"
    spice.kclear()


def test_boddef():
    spice.boddef("Jebediah", 117)
    assert spice.bodc2n(117, 10) == "Jebediah"


def test_bodfnd():
    spice.furnsh(_testKernelPath)
    assert spice.bodfnd(599, "RADII")
    spice.kclear()


def test_bodn2c():
    spice.furnsh(_testKernelPath)
    assert spice.bodn2c("EARTH") == 399
    assert spice.bodn2c("U.S.S. Enterprise") is None
    spice.kclear()


def test_bods2c():
    spice.furnsh(_testKernelPath)
    assert spice.bods2c("EARTH") == 399
    assert spice.bods2c("U.S.S. Enterprise") is None
    spice.kclear()


def test_bodvar():
    spice.furnsh(_testKernelPath)
    radii = spice.bodvar(399, "RADII", 3)
    expected = np.array([6378.140, 6378.140, 6356.755])
    np.testing.assert_array_almost_equal(expected, radii, decimal = 1)
    spice.kclear()


def test_bodvcd():
    spice.furnsh(_testKernelPath)
    dim, values = spice.bodvcd(399, "RADII", 3)
    assert dim == 3
    expected = np.array([6378.140, 6378.140, 6356.755])
    np.testing.assert_array_almost_equal(expected, values, decimal = 1)
    spice.kclear()


def test_bodvrd():
    spice.furnsh(_testKernelPath)
    dim, values = spice.bodvrd("EARTH", "RADII", 3)
    assert dim == 3
    expected = np.array([6378.140, 6378.140, 6356.755])
    np.testing.assert_array_almost_equal(expected, values, decimal = 1)
    spice.kclear()


def test_brcktd():
    assert spice.brcktd(-1.0, 1.0, 10.0) == 1.0
    assert spice.brcktd(29.0, 1.0, 10.0) == 10.0
    assert spice.brcktd(3.0, -10.0, 10.0) == 3.0
    assert spice.brcktd(3.0, -10.0, -1.0) == -1.0


def test_brckti():
    assert spice.brckti(-1, 1, 10) == 1
    assert spice.brckti(29, 1, 10) == 10
    assert spice.brckti(3, -10, 10) == 3
    assert spice.brckti(3, -10, -1) == -1


def test_bschoc():
    array = ["FEYNMAN", "BOHR", "EINSTEIN", "NEWTON", "GALILEO"]
    order = [1, 2, 0, 4, 3]
    lenvals = 10
    assert spice.bschoc("NEWTON", 5, lenvals, array, order) == 3
    assert spice.bschoc("EINSTEIN", 5, lenvals, array, order) == 2
    assert spice.bschoc("GALILEO", 5, lenvals, array, order) == 4
    assert spice.bschoc("Galileo", 5, lenvals, array, order) == -1
    assert spice.bschoc("BETHE", 5, lenvals, array, order) == -1


def test_bschoi():
    array = [100, 1, 10, 10000, 1000]
    order = [1, 2, 0, 4, 3]
    assert spice.bschoi(1000, 5, array, order) == 4
    assert spice.bschoi(1, 5, array, order) == 1
    assert spice.bschoi(10000, 5, array, order) == 3
    assert spice.bschoi(-1, 5, array, order) == -1
    assert spice.bschoi(17, 5, array, order) == -1


def test_bsrchc():
    array = ["BOHR", "EINSTEIN", "FEYNMAN", "GALILEO", "NEWTON"]
    lenvals = 10
    assert spice.bsrchc("NEWTON", 5, lenvals, array) == 4
    assert spice.bsrchc("EINSTEIN", 5, lenvals, array) == 1
    assert spice.bsrchc("GALILEO", 5, lenvals, array) == 3
    assert spice.bsrchc("Galileo", 5, lenvals, array) == -1
    assert spice.bsrchc("BETHE", 5, lenvals, array) == -1


def test_bsrchd():
    array = np.array([-11.0, 0.0, 22.0, 750.0])
    assert spice.bsrchd(-11.0, 4, array) == 0
    assert spice.bsrchd(22.0, 4, array) == 2
    assert spice.bsrchd(751.0, 4, array) == -1


def test_bsrchi():
    array = np.array([-11, 0, 22, 750])
    assert spice.bsrchi(-11, 4, array) == 0
    assert spice.bsrchi(22, 4, array) == 2
    assert spice.bsrchi(751, 4, array) == -1


def test_card():
    testCell = spice.stypes.SPICEDOUBLE_CELL(8)
    assert spice.card(testCell) == 0
    spice.appndd(1.0, testCell)
    assert spice.card(testCell) == 1
    spice.appndd(2.0, testCell)
    assert spice.card(testCell) == 2
    spice.appndd(3.0, testCell)
    assert spice.card(testCell) == 3


def test_cgv2el():
    vec1 = [1.0, 1.0, 1.0]
    vec2 = [1.0, -1.0, 1.0]
    center = [-1.0, 1.0, -1.0]
    ellipse = spice.cgv2el(center, vec1, vec2)
    expectedSmajor = [np.sqrt(2.0), 0.0, np.sqrt(2.0)]
    expectedSminor = [0.0, np.sqrt(2.0), 0.0]
    expectedCenter = [-1.0, 1.0, -1.0]
    npt.assert_array_almost_equal(expectedCenter, ellipse.center)
    npt.assert_array_almost_equal(expectedSmajor, ellipse.semi_major)
    npt.assert_array_almost_equal(expectedSminor, ellipse.semi_minor)


def test_chkin():
    assert 1


def test_chkout():
    assert 1


def test_cidfrm():
    frcode, frname = spice.cidfrm(501, 10)
    assert frcode == 10023
    assert frname == 'IAU_IO'
    frcode, frname = spice.cidfrm(399, 10)
    assert frcode == 10013
    assert frname == 'IAU_EARTH'
    frcode, frname = spice.cidfrm(301, 10)
    assert frcode == 10020
    assert frname == 'IAU_MOON'


def test_ckcls():
    assert 1


def test_ckcov():
    assert 1


def test_ckgp():
    assert 1


def test_ckgpav():
    assert 1


def test_cklpf():
    assert 1


def test_ckobj():
    assert 1


def test_ckopn():
    assert 1


def test_ckupf():
    assert 1


def test_ckw01():
    assert 1


def test_ckw02():
    assert 1


def test_ckw03():
    assert 1


def test_ckw05():
    assert 1


def test_clight():
    assert spice.clight() == 299792.458


def test_clpool():
    spice.kclear()
    spice.pdpool('TEST_VAR', 1, [-666.0])
    dval, value = spice.gdpool('TEST_VAR', 0, 1)
    assert dval == 1
    assert value[0] == -666.0
    spice.clpool()
    found = spice.gdpool('TEST_VAR', 0, 1)
    assert found is None
    spice.kclear()


def test_cmprss():
    strings = ['ABC...DE.F...', '...........', '.. ..AB....CD']
    assert spice.cmprss('.', 2, strings[0], 15) == 'ABC..DE.F..'
    assert spice.cmprss('.', 3, strings[1], 15) == '...'
    assert spice.cmprss('.', 1, strings[2], 15) == '. .AB.CD'
    assert spice.cmprss('.', 3, strings[1]) == '...'
    assert spice.cmprss('.', 1, strings[2]) == '. .AB.CD'
    assert spice.cmprss(' ', 0, ' Embe dde d -sp   a c  es   ', 20) == 'Embedded-spaces'


def test_cnmfrm():
    ioFrcode, ioFrname = spice.cnmfrm('IO', 10)
    assert ioFrcode == 10023
    assert ioFrname == 'IAU_IO'


def test_conics():
    spice.furnsh(_testKernelPath)
    et = spice.str2et('Dec 25, 2007')
    state, ltime = spice.spkezr('Moon', et, 'J2000', 'NONE', 'EARTH')
    dim, mu = spice.bodvrd('EARTH', 'GM', 1)
    elts = spice.oscelt(state, et, mu[0])
    later = et + 7.0 * spice.spd()
    later_state = spice.conics(elts, later)
    state, ltime = spice.spkezr('Moon', later, 'J2000', 'NONE', 'EARTH')
    spice.kclear()
    pert = np.array(later_state) - np.array(state)
    expectedPert = [-7488.85977, 397.610079, 195.745581, -0.0361527602, -0.00127926674, -0.00201458871]
    npt.assert_array_almost_equal(pert, expectedPert, decimal=5)


def test_convrt():
    assert spice.convrt(300.0, 'statute_miles', 'km') == 482.80320
    npt.assert_almost_equal(spice.convrt(1.0, 'parsecs', 'lightyears'), 3.2615638, decimal=6)


def test_copy():
    assert 1


def test_cpos():
    string = "BOB, JOHN, TED, AND MARTIN...."
    assert spice.cpos(string, " ,", 0) == 3
    assert spice.cpos(string, " ,", 4) == 4
    assert spice.cpos(string, " ,", 5) == 9
    assert spice.cpos(string, " ,", 10) == 10
    assert spice.cpos(string, " ,", 11) == 14
    assert spice.cpos(string, " ,", 15) == 15
    assert spice.cpos(string, " ,", 16) == 19
    assert spice.cpos(string, " ,", 20) == -1
    assert spice.cpos(string, " ,", -112) == 3
    assert spice.cpos(string, " ,", -1) == 3
    assert spice.cpos(string, " ,", 1230) == -1


def test_cposr():
    string = "BOB, JOHN, TED, AND MARTIN...."
    assert spice.cposr(string, " ,", 29) == 19
    assert spice.cposr(string, " ,", 25) == 19
    assert spice.cposr(string, " ,", 18) == 15
    assert spice.cposr(string, " ,", 14) == 14
    assert spice.cposr(string, " ,", 13) == 10
    assert spice.cposr(string, " ,", 9) == 9
    assert spice.cposr(string, " ,", 8) == 4
    assert spice.cposr(string, " ,", 3) == 3
    assert spice.cposr(string, " ,", 2) == -1
    assert spice.cposr(string, " ,", 230) == 19
    assert spice.cposr(string, " ,", 30) == 19
    assert spice.cposr(string, " ,", -1) == -1
    assert spice.cposr(string, " ,", -10) == -1


def test_cvpool():
    assert 1


def test_cyllat():
    assert spice.cyllat(1.0, 180.0*spice.rpd(), -1.0) == (np.sqrt(2), np.pi, -np.pi/4)


def test_cylrec():
    assert spice.cylrec(0.0, np.radians(33.0), 0.0) == [0.0, 0.0, 0.0]


def test_cylsph():
    a = np.array(spice.cylsph(1.0, np.deg2rad(180.0), 1.0))
    b = np.array([1.4142, np.deg2rad(180.0), np.deg2rad(45.0)])
    np.testing.assert_almost_equal(b, a, decimal=4)


def test_dafac():
    assert 1


def test_dafbbs():
    assert 1


def test_dafbfs():
    assert 1


def test_dafcls():
    assert 1


def test_dafcs():
    assert 1


def test_dafdc():
    assert 1


def test_dafec():
    assert 1


def test_daffna():
    assert 1


def test_daffpa():
    assert 1


def test_dafgda():
    assert 1


def test_dafgn():
    assert 1


def test_dafgs():
    assert 1


def test_dafgsr():
    assert 1


def test_dafopr():
    assert 1


def test_dafopw():
    assert 1


def test_dafps():
    assert 1


def test_dafrda():
    assert 1


def test_dafrfr():
    assert 1


def test_dafrs():
    assert 1


def test_dafus():
    assert 1


def test_dasac():
    assert 1


def test_dascls():
    assert 1


def test_dasec():
    assert 1


def test_dasopr():
    assert 1


def test_dcyldr():
    assert 1


def test_deltet():
    spice.furnsh(_testKernelPath)
    UTC_1997 = 'Jan 1 1997'
    UTC_2004 = 'Jan 1 2004'
    et_1997 = spice.str2et(UTC_1997)
    et_2004 = spice.str2et(UTC_2004)
    delt_1997 = spice.deltet(et_1997, 'ET')
    delt_2004 = spice.deltet(et_2004, 'ET')
    npt.assert_almost_equal(delt_1997, 62.1839353, decimal=6)
    npt.assert_almost_equal(delt_2004, 64.1839116, decimal=6)
    spice.kclear()


def test_det():
    m1 = np.array([[5.0, -2.0, 1.0], [0.0, 3.0, -1.0], [2.0, 0.0, 7.0]])
    expected = 103
    assert spice.det(m1) == expected


def test_dgeodr():
    assert 1


def test_diags2():
    mat = [[1.0, 4.0], [4.0, -5.0]]
    diag, rot = spice.diags2(mat)
    expectedDiag = [[3.0, 0.0], [0.0, -7.0]]
    expectedRot = [[0.89442719, -0.44721360], [0.44721360, 0.89442719]]
    npt.assert_array_almost_equal(diag, expectedDiag)
    npt.assert_array_almost_equal(rot, expectedRot)


def test_diff():
    assert 1


def test_dlatdr():
    assert 1


def test_dp2hx():
    assert spice.dp2hx(2.0e-9) == "89705F4136B4A8^-7"
    assert spice.dp2hx(1.0) == "1^1"
    assert spice.dp2hx(-1.0) == "-1^1"
    assert spice.dp2hx(1024.0) == "4^3"
    assert spice.dp2hx(-1024.0) == "-4^3"
    assert spice.dp2hx(521707.0) == "7F5EB^5"
    assert spice.dp2hx(27.0) == "1B^2"
    assert spice.dp2hx(0.0) == "0^0"


def test_dpgrdr():
    assert 1


def test_dpmax():
    assert 1


def test_dpmin():
    assert 1


def test_dpr():
    assert spice.dpr() == 180.0 / np.arccos(-1.0)


def test_drdcyl():
    assert 1


def test_drdgeo():
    assert 1


def test_drdlat():
    assert 1


def test_drdpgr():
    assert 1


def test_drdsph():
    assert 1


def test_dsphdr():
    assert 1


def test_dtpool():
    assert 1


def test_ducrss():
    assert 1


def test_dvcrss():
    assert 1


def test_dvdot():
    assert 1


def test_dvhat():
    assert 1


def test_dvnorm():
    assert 1


def test_dvpool():
    assert 1


def test_dvsep():
    assert 1


def test_edlimb():
    viewpt = [2.0, 0.0, 0.0]
    limb = spice.edlimb(np.sqrt(2), 2.0 * np.sqrt(2), np.sqrt(2), viewpt)
    expectedSMinor = [0.0, 0.0, -1.0]
    expectedSMajor = [0.0, 2.0, 0.0]
    expectedCenter = [1.0, 0.0, 0.0]
    npt.assert_array_almost_equal(limb.center, expectedCenter)
    npt.assert_array_almost_equal(limb.semi_major, expectedSMajor)
    npt.assert_array_almost_equal(limb.semi_minor, expectedSMinor)


def test_ekacec():
    assert 1


def test_ekaced():
    assert 1


def test_ekacei():
    assert 1


def test_ekaclc():
    assert 1


def test_ekacld():
    assert 1


def test_ekacli():
    assert 1


def test_ekappr():
    assert 1


def test_ekbseg():
    assert 1


def test_ekccnt():
    assert 1


def test_ekcii():
    assert 1


def test_ekcls():
    assert 1


def test_ekdelr():
    assert 1


def test_ekffld():
    assert 1


def test_ekfind():
    assert 1


def test_ekgc():
    assert 1


def test_ekgd():
    assert 1


def test_ekgi():
    assert 1


def test_ekifld():
    assert 1


def test_ekinsr():
    assert 1


def test_eklef():
    assert 1


def test_eknelt():
    assert 1


def test_eknseg():
    assert 1


def test_ekntab():
    assert 1


def test_ekopn():
    assert 1


def test_ekopr():
    assert 1


def test_ekops():
    assert 1


def test_ekopw():
    assert 1


def test_ekpsel():
    assert 1


def test_ekrcec():
    assert 1


def test_ekrced():
    assert 1


def test_ekrcei():
    assert 1


def test_ekssum():
    assert 1


def test_ektnam():
    assert 1


def test_ekucec():
    assert 1


def test_ekuced():
    assert 1


def test_ekucei():
    assert 1


def test_ekuef():
    assert 1


def test_el2cgv():
    vec1 = [1.0, 1.0, 1.0]
    vec2 = [1.0, -1.0, 1.0]
    center = [1.0, 1.0, 1.0]
    smajor, sminor = spice.saelgv(vec1, vec2)
    ellipse = spice.cgv2el(center, smajor, sminor)
    expectedCenter = [1.0, 1.0, 1.0]
    expectedSmajor = [np.sqrt(2.0), 0.0, np.sqrt(2.0)]
    expectedSminor = [0.0, np.sqrt(2.0), 0.0]
    npt.assert_array_almost_equal(ellipse.center, expectedCenter)
    npt.assert_array_almost_equal(ellipse.semi_major, expectedSmajor)
    npt.assert_array_almost_equal(ellipse.semi_minor, expectedSminor)


def test_elemc():
    assert 1


def test_elemd():
    assert 1


def test_elemi():
    assert 1


def test_eqstr():
    assert spice.eqstr("A short string    ", "ashortstring")
    assert spice.eqstr("Embedded        blanks", "Em be dd ed bl an ks")
    assert spice.eqstr("One word left out", "WORD LEFT OUT") is False


def test_erract():
    assert spice.erract("GET", 10, "") == "REPORT"
    assert spice.erract("GET", 10) == "REPORT"


def test_errch():
    assert 1


def test_errdev():
    assert 1


def test_errdp():
    assert 1


def test_errint():
    assert 1


def test_errprt():
    assert 1


def test_esrchc():
    assert 1


def test_et2lst():
    assert 1


def test_et2utc():
    spice.furnsh(_testKernelPath)
    et = -527644192.5403653
    output = spice.et2utc(et, "J", 6, 35)
    assert output == "JD 2445438.006415"
    spice.kclear()


def test_etcal():
    assert 1


def test_eul2m():
    assert 1


def test_eul2xf():
    assert 1


def test_exists():
    assert spice.exists(_testKernelPath)


def test_expool():
    assert 1


def test_failed():
    assert 1


def test_frame():
    assert 1


def test_frinfo():
    assert 1


def test_frmnam():
    assert 1


def test_ftncls():
    assert 1


def test_furnsh():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    # 4 kernels + the meta kernel = 5
    assert spice.ktotal("ALL") == 5
    spice.kclear()


def test_gcpool():
    assert 1


def test_gdpool():
    assert 1


def test_georec():
    assert 1


def test_getcml():
    assert 1


def test_getelm():
    assert 1


def test_getfat():
    assert 1


def test_getfov():
    assert 1


def test_getmsg():
    assert 1


def test_gfbail():
    assert 1


def test_gfclrh():
    assert 1


def test_gfdist():
    assert 1


def test_gfevnt():
    assert 1


def test_gffove():
    assert 1


def test_gfinth():
    assert 1


def test_gfocce():
    assert 1


def test_gfoclt():
    assert 1


def test_gfposc():
    assert 1


def test_gfrefn():
    assert 1


def test_gfrepf():
    assert 1


def test_gfrepi():
    assert 1


def test_gfrepu():
    assert 1


def test_gfrfov():
    assert 1


def test_gfrr():
    assert 1


def test_gfsep():
    assert 1


def test_gfsntc():
    assert 1


def test_gfsstp():
    assert 1


def test_gfstep():
    assert 1


def test_gfsubc():
    assert 1


def test_gftfov():
    assert 1


def test_gfuds():
    assert 1


def test_gipool():
    assert 1


def test_gnpool():
    assert 1


def test_halfpi():
    assert spice.halfpi() == np.pi / 2


def test_hx2dp():
    assert 1


def test_ident():
    assert 1


def test_illum():
    assert 1


def test_ilumin():
    assert 1


def test_inedpl():
    spice.furnsh(_testKernelPath)
    TIME = 'Oct 31 2002, 12:55:00 PST'
    FRAME = 'J2000'
    CORR = 'LT+S'
    et = spice.str2et(TIME)
    state, ltime = spice.spkezr('EARTH', et, FRAME, CORR, 'SUN')
    pos = state[0:3]
    dim, radii = spice.bodvrd('EARTH', 'RADII', 3)
    pos = [pos[0] / radii[0] ** 2.0,
           pos[1] / radii[1] ** 2.0,
           pos[2] / radii[2] ** 2.0]
    plane = spice.nvc2pl(pos, 1.0)
    term = spice.inedpl(radii[0], radii[1], radii[2], plane)
    spice.kclear()
    expectedCenter = [0.21512031, 0.15544527, 0.067391641]
    expectedSMajor = [-3735.61161, 5169.70331, -9.7794273e-12]
    expectedSMinor = [-1276.33361, -922.27471, 6159.97370]
    npt.assert_array_almost_equal(expectedCenter, term.center)
    npt.assert_array_almost_equal(expectedSMajor, term.semi_major, decimal=5)
    npt.assert_array_almost_equal(expectedSMinor, term.semi_minor, decimal=5)
    npt.assert_almost_equal(spice.vnorm(term.semi_major), 6378.1365, decimal=2)
    npt.assert_almost_equal(spice.vnorm(term.semi_minor), 6358.0558, decimal=2)


def test_inelpl():
    spice.furnsh(_testKernelPath)
    dim, radii = spice.bodvrd('SATURN', 'RADII', 3)
    vertex = [100.0 * radii[0], 0.0, radii[0] * 100.0]
    limb = spice.edlimb(radii[0], radii[1], radii[2], vertex)
    normal = [0.0, 0.0, 1.0]
    point = [0.0, 0.0, 0.0]
    plane = spice.nvp2pl(normal, point)
    nxpts, xpt1, xpt2 = spice.inelpl(limb, plane)
    expectedXpt1 = [602.68000, 60264.9865, 0.0]
    expectedXpt2 = [602.68000, -60264.9865, 0.0]
    assert nxpts == 2.0
    npt.assert_array_almost_equal(expectedXpt1, xpt1, decimal=4)
    npt.assert_array_almost_equal(expectedXpt2, xpt2, decimal=4)
    spice.kclear()


def test_inrypl():
    spice.furnsh(_testKernelPath)
    dim, radii = spice.bodvrd("SATURN", "RADII", 3)
    vertex = [3.0 * radii[0], 0.0, radii[2] * 0.5]
    dire = [0.0, np.cos(30.0 * spice.rpd()), -1.0 * np.sin(30.0 * spice.rpd())]
    normal = [0.0, 0.0, 1.0]
    point = [0.0, 0.0, 0.0]
    plane = spice.nvp2pl(normal, point)
    nxpts, xpt = spice.inrypl(vertex, dire, plane)
    expectedXpt = np.array([180804.0, 47080.6050513, 0.0])
    assert nxpts == 1
    np.testing.assert_almost_equal(np.array(xpt), expectedXpt, decimal = 6)
    spice.kclear()


def test_insrtc():
    assert 1


def test_insrtd():
    testCell = spice.stypes.SPICEDOUBLE_CELL(8)
    dlist = [0.5, 2.0, 30.0, 0.01, 30.0]
    for d in dlist:
        spice.insrtd(d, testCell)
    assert [x for x in testCell] == [0.01, 0.5, 2.0, 30.0]


def test_insrti():
    testCell = spice.stypes.SPICEINT_CELL(8)
    ilist = [1, 2, 30, 1, 30]
    for i in ilist:
        spice.insrti(i, testCell)
    assert [x for x in testCell] == [1, 2, 30]


def test_inter():
    assert 1


def test_intmax():
    assert 1


def test_intmin():
    assert 1


def test_invert():
    m1 = np.array([[0.0, -1.0, 0.0], [0.5, 0.0, 0.0], [0.0, 0.0, 1.0]])
    expected = np.array([[0.0, 2.0, 0.0], [-1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    mout = spice.invert(m1)
    assert np.array_equal(expected, mout)


def test_invort():
    assert 1


def test_isordv():
    assert spice.isordv([0, 1], 2)
    assert spice.isordv([0, 1, 2], 3)
    assert spice.isordv([0, 1, 2, 3], 4)
    assert spice.isordv([1, 1, 1], 3) is False


def test_isrchc():
    array = ["1", "0", "4", "2"]
    assert spice.isrchc("4", 4, 3, array) == 2
    assert spice.isrchc("2", 4, 3, array) == 3
    assert spice.isrchc("3", 4, 3, array) == -1


def test_isrchd():
    array = [1.0, 0.0, 4.0, 2.0]
    assert spice.isrchd(4.0, 4, array) == 2
    assert spice.isrchd(2.0, 4, array) == 3
    assert spice.isrchd(3.0, 4, array) == -1


def test_isrchi():
    array = [1, 0, 4, 2]
    assert spice.isrchi(4, 4, array) == 2
    assert spice.isrchi(2, 4, array) == 3
    assert spice.isrchi(3, 4, array) == -1


def test_isrot():
    assert 1


def test_iswhsp():
    assert spice.iswhsp("       ")
    assert spice.iswhsp("spice") is False


def test_j1900():
    assert spice.j1900() == 2415020.0


def test_j1950():
    assert spice.j1950() == 2433282.5


def test_j2000():
    assert spice.j2000() == 2451545.0


def test_j2100():
    assert spice.j2100() == 2488070.0


def test_jyear():
    assert spice.jyear() == 31557600.0


def test_kclear():
    spice.kclear()
    assert spice.ktotal("ALL") == 0


def test_kdata():
    assert 1


def test_kinfo():
    assert 1


def test_ktotal():
    assert 1


def test_kxtrct():
    assert 1


def test_lastnb():
    assert spice.lastnb("ABCDE") == 4
    assert spice.lastnb("AN EXAMPLE") == 9
    assert spice.lastnb("AN EXAMPLE        ") == 9
    assert spice.lastnb("        ") == -1


def test_latcyl():
    assert 1


def test_latrec():
    expected1 = np.array([1.0, 0.0, 0.0])
    expected2 = np.array([0.0, 1.0, 0.0])
    expected3 = np.array([-1.0, 0.0, 0.0])
    npt.assert_array_almost_equal(expected1, spice.latrec(1.0, 0.0, 0.0), decimal=7)
    npt.assert_array_almost_equal(expected2, spice.latrec(1.0, 90.0 * spice.rpd(), 0.0), decimal=7)
    npt.assert_array_almost_equal(expected3, spice.latrec(1.0, 180.0 * spice.rpd(), 0.0), decimal=7)


def test_latsph():
    assert 1


def test_lcase():
    assert spice.lcase("THIS IS AN EXAMPLE", 20) == "THIS IS AN EXAMPLE".lower()
    assert spice.lcase("1234", 5) == "1234"


def test_ldpool():
    assert 1


def test_lmpool():
    assert 1


def test_lparse():
    assert 1


def test_lparsm():
    assert 1


def test_lparss():
    assert 1


def test_lspcn():
    assert 1


def test_lstlec():
    array = ["BOHR", "EINSTEIN", "FEYNMAN", "GALILEO", "NEWTON"]
    lenvals = 10
    assert spice.lstlec("NEWTON", 5, lenvals, array) == 4
    assert spice.lstlec("EINSTEIN", 5, lenvals, array) == 1
    assert spice.lstlec("GALILEO", 5, lenvals, array) == 3
    assert spice.lstlec("Galileo", 5, lenvals, array) == 3
    assert spice.lstlec("BETHE", 5, lenvals, array) == -1


def test_lstled():
    array = [-2.0, -2.0, 0.0, 1.0, 1.0, 11.0]
    assert spice.lstled(-3.0, 6, array) == -1
    assert spice.lstled(-2.0, 6, array) == 1
    assert spice.lstled(0.0, 6, array) == 2
    assert spice.lstled(1.0, 6, array) == 4
    assert spice.lstled(11.1, 6, array) == 5


def test_lstlei():
    array = [-2, -2, 0, 1, 1, 11]
    assert spice.lstlei(-3, 6, array) == -1
    assert spice.lstlei(-2, 6, array) == 1
    assert spice.lstlei(0, 6, array) == 2
    assert spice.lstlei(1, 6, array) == 4
    assert spice.lstlei(12, 6, array) == 5


def test_lstltc():
    array = ["BOHR", "EINSTEIN", "FEYNMAN", "GALILEO", "NEWTON"]
    lenvals = 10
    assert spice.lstltc("NEWTON", 5, lenvals, array) == 3
    assert spice.lstltc("EINSTEIN", 5, lenvals, array) == 0
    assert spice.lstltc("GALILEO", 5, lenvals, array) == 2
    assert spice.lstltc("Galileo", 5, lenvals, array) == 3
    assert spice.lstltc("BETHE", 5, lenvals, array) == -1


def test_lstltd():
    array = [-2.0, -2.0, 0.0, 1.0, 1.0, 11.0]
    assert spice.lstltd(-3.0, 6, array) == -1
    assert spice.lstltd(-2.0, 6, array) == -1
    assert spice.lstltd(0.0, 6, array) == 1
    assert spice.lstltd(1.0, 6, array) == 2
    assert spice.lstltd(11.1, 6, array) == 5


def test_lstlti():
    array = [-2, -2, 0, 1, 1, 11]
    assert spice.lstlti(-3, 6, array) == -1
    assert spice.lstlti(-2, 6, array) == -1
    assert spice.lstlti(0, 6, array) == 1
    assert spice.lstlti(1, 6, array) == 2
    assert spice.lstlti(12, 6, array) == 5


def test_ltime():
    assert 1


def test_lx4dec():
    assert 1


def test_lx4num():
    assert 1


def test_lx4sgn():
    assert 1


def test_lx4uns():
    assert 1


def test_lxqstr():
    assert spice.lxqstr('The "SPICE" system', "\"", 4) == (10, 7)
    assert spice.lxqstr('The "SPICE" system', '"', 4) == (10, 7)
    assert spice.lxqstr('The "SPICE" system', '"', 0) == (-1, 0)
    assert spice.lxqstr('The "SPICE" system', "'", 4) == (3, 0)
    assert spice.lxqstr('The """SPICE"""" system', '"', 4) == (14, 11)
    assert spice.lxqstr('The &&&SPICE system', '&', 4) == (5, 2)
    assert spice.lxqstr("' '", "'", 0) == (2, 3)
    assert spice.lxqstr("''", "'", 0) == (1, 2)


def test_m2eul():
    assert 1


def test_m2q():
    r = spice.rotate(spice.halfpi(), 3)
    q = spice.m2q(r)
    expected = [np.sqrt(2) / 2.0, 0.0, 0.0, -np.sqrt(2) / 2.0]
    np.testing.assert_array_almost_equal(expected, q, decimal = 6)


def test_matchi():
    string = "  ABCDEFGHIJKLMNOPQRSTUVWXYZ  "
    wstr = "*"
    wchr = "%"
    assert spice.matchi(string, "*A*", wstr, wchr)
    assert spice.matchi(string, "A%D*", wstr, wchr) is False
    assert spice.matchi(string, "A%C*", wstr, wchr)
    assert spice.matchi(string, "%A*", wstr, wchr) is False
    assert spice.matchi(string, "%%CD*Z", wstr, wchr)
    assert spice.matchi(string, "%%CD", wstr, wchr) is False
    assert spice.matchi(string, "A*MN*Y*Z", wstr, wchr)
    assert spice.matchi(string, "A*MN*Y*%Z", wstr, wchr) is False
    assert spice.matchi(string, "*BCD*Z*", wstr, wchr)
    assert spice.matchi(string, "*bdc*z*", wstr, wchr) is False
    assert spice.matchi(string, " *bcD*Z*", wstr, wchr)


def test_matchw():
    string = "  ABCDEFGHIJKLMNOPQRSTUVWXYZ  "
    wstr = "*"
    wchr = "%"
    assert spice.matchw(string, "*A*", wstr, wchr)
    assert spice.matchw(string, "A%D*", wstr, wchr) is False
    assert spice.matchw(string, "A%C*", wstr, wchr)
    assert spice.matchw(string, "%A*", wstr, wchr) is False
    assert spice.matchw(string, "%%CD*Z", wstr, wchr)
    assert spice.matchw(string, "%%CD", wstr, wchr) is False
    assert spice.matchw(string, "A*MN*Y*Z", wstr, wchr)
    assert spice.matchw(string, "A*MN*Y*%Z", wstr, wchr) is False
    assert spice.matchw(string, "*BCD*Z*", wstr, wchr)
    assert spice.matchw(string, "*bdc*z*", wstr, wchr) is False
    assert spice.matchw(string, " *BCD*Z*", wstr, wchr)


def test_maxd():
    assert 1


def test_maxi():
    assert 1


def test_mequ():
    m1 = np.identity(3)
    mout = spice.mequ(m1)
    assert np.array_equal(m1, mout)


def test_mequg():
    m1 = np.identity(2)
    mout = spice.mequg(m1, 2, 2)
    assert np.array_equal(m1, mout)


def test_mind():
    assert 1


def test_mini():
    assert 1


def test_mtxm():
    m1 = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
    m2 = np.array([[1.0, 1.0, 0.0], [-1.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    mout = spice.mtxm(m1, m2)
    expected = np.array([[-3.0, 5.0, 7.0], [-3.0, 7.0, 8.0], [-3.0, 9.0, 9.0]])
    assert np.array_equal(mout, expected)


def test_mtxmg():
    m1 = np.array([[1.0, 2.0, 3.0, 0.0], [1.0, 1.0, 1.0, 1.0]])
    m2 = np.array([[1.0, 2.0, 3.0], [0.0, 0.0, 0.0]])
    mout = spice.mtxmg(m1, m2, 4, 2, 3)
    expected = np.array([[1.0, 2.0, 3.0], [2.0, 4.0, 6.0], [3.0, 6.0, 9.0], [0.0, 0.0, 0.0]])
    assert np.array_equal(mout, expected)


def test_mtxv():
    m1 = np.array([[1.0, 1.0, 0.0], [-1.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    vin = np.array([5.0, 10.0, 15.0])
    mout = spice.mtxv(m1, vin)
    expected = np.array([-5.0, 15.0, 15.0])
    assert np.array_equal(mout, expected)


def test_mtxvg():
    m1 = np.array([[1.0, 2.0], [1.0, 3.0], [1.0, 4.0]])
    v2 = np.array([1.0, 2.0, 3.0])
    mout = spice.mtxvg(m1, v2, 2, 3)
    expected = np.array([6.0, 20.0])
    assert np.array_equal(mout, expected)


def test_mxm():
    m1 = [[1.0, 1.0, 0.0], [-1.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    m2 = [[1.0, 0.0, 0.0], [0.0, 1.0, 1.0], [0.0, -1.0, 1.0]]
    mout = np.array(spice.mxm(m1, m2))
    m1 = np.array(m1)
    m2 = np.array(m2)
    mout2 = np.dot(m1, m2)
    assert np.array_equal(mout, mout2)


def test_mxmg():
    m1 = [[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]
    m2 = [[1.0, 2.0, 3.0], [2.0, 4.0, 6.0]]
    nrow1 = 3
    ncol1 = 2
    ncol2 = 3
    mout = np.array(spice.mxmg(m1, m2, nrow1, ncol1, ncol2))
    m1 = np.array(m1)
    m2 = np.array(m2)
    mout2 = np.dot(m1, m2)
    assert np.array_equal(mout, mout2)


def test_mxmt():
    m1 = [[0.0, 1.0, 0.0], [-1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
    mout = spice.mxmt(m1, m1)
    assert np.array_equal(mout, np.identity(3))


def test_mxmtg():
    m1 = np.array([[1.0, 2.0, 3.0], [3.0, 2.0, 1.0]])
    m2 = np.array([[1.0, 2.0, 0.0], [2.0, 1.0, 2.0], [1.0, 2.0, 0.0], [2.0, 1.0, 2.0]])
    mout = spice.mxmtg(m1, m2, 2, 3, 4)
    expected = np.array([[5.0, 10.0, 5.0, 10.0], [7.0, 10.0, 7.0, 10.0]])
    assert np.array_equal(mout, expected)


def test_mxv():
    m1 = np.array([[0.0, 1.0, 0.0], [-1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    vin = np.array([1.0, 2.0, 3.0])
    mout = spice.mxv(m1, vin)
    expected = np.array([2.0, -1.0, 3.0])
    assert np.array_equal(mout, expected)


def test_mxvg():
    m1 = np.array([[1.0, 1.0, 1.0], [2.0, 3.0, 4.0]])
    v2 = np.array([1.0, 2.0, 3.0])
    mout = spice.mxvg(m1, v2, 2, 3)
    expected = np.array([6.0, 20.0])
    assert np.array_equal(mout, expected)


def test_namfrm():
    assert spice.namfrm('J2000') == 1


def test_ncpos():
    string = "BOB, JOHN, TED, AND MARTIN    "
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    assert spice.ncpos(string, chars, 0) == 3
    assert spice.ncpos(string, chars, 4) == 4
    assert spice.ncpos(string, chars, 5) == 9
    assert spice.ncpos(string, chars, 10) == 10
    assert spice.ncpos(string, chars, 11) == 14
    assert spice.ncpos(string, chars, 15) == 15
    assert spice.ncpos(string, chars, 16) == 19
    assert spice.ncpos(string, chars, 20) == 26
    assert spice.ncpos(string, chars, 27) == 27
    assert spice.ncpos(string, chars, 28) == 28
    assert spice.ncpos(string, chars, 29) == 29
    assert spice.ncpos(string, chars, -12) == 3
    assert spice.ncpos(string, chars, -1) == 3
    assert spice.ncpos(string, chars, 30) == -1
    assert spice.ncpos(string, chars, 122) == -1


def test_ncposr():
    string = "BOB, JOHN, TED, AND MARTIN...."
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    assert spice.ncposr(string, chars, 29) == 29
    assert spice.ncposr(string, chars, 28) == 28
    assert spice.ncposr(string, chars, 27) == 27
    assert spice.ncposr(string, chars, 26) == 26
    assert spice.ncposr(string, chars, 25) == 19
    assert spice.ncposr(string, chars, 18) == 15
    assert spice.ncposr(string, chars, 14) == 14
    assert spice.ncposr(string, chars, 13) == 10
    assert spice.ncposr(string, chars, 9) == 9
    assert spice.ncposr(string, chars, 8) == 4
    assert spice.ncposr(string, chars, 3) == 3
    assert spice.ncposr(string, chars, 2) == -1
    assert spice.ncposr(string, chars, -1) == -1
    assert spice.ncposr(string, chars, -5) == -1
    assert spice.ncposr(string, chars, 30) == 29
    assert spice.ncposr(string, chars, 122) == 29


def test_nearpt():
    a, b, c = 1.0, 2.0, 3.0
    point = [3.5, 0.0, 0.0]
    pnear, alt = spice.nearpt(point, a, b, c)
    expectedPnear = [1.0, 0.0, 0.0]
    expectedAlt = 2.5
    npt.assert_almost_equal(alt, expectedAlt)
    npt.assert_array_almost_equal(pnear, expectedPnear)


def test_npedln():
    linept = [1.0e6, 2.0e6, 3.0e6]
    a, b, c = 7.0e5, 7.0e5, 6.0e5
    linedr = [-4.472091234e-1, -8.944182469e-1, -4.472091234e-3]
    pnear, dist = spice.npedln(a, b, c, linept, linedr)
    expectedPnear = [-1633.3111, -3266.6222, 599991.83]
    expectedDist = 2389967.9
    npt.assert_almost_equal(dist, expectedDist, decimal=1)
    npt.assert_array_almost_equal(expectedPnear, pnear, decimal=2)


def test_npelpt():
    center = [1.0, 2.0, 3.0]
    smajor = [3.0, 0.0, 0.0]
    sminor = [0.0, 2.0, 0.0]
    point = [-4.0, 2.0, 1.0]
    expectedPnear = [-2.0, 2.0, 3.0]
    expectedDist = 2.8284271
    ellipse = spice.cgv2el(center, smajor, sminor)
    pnear, dist = spice.npelpt(point, ellipse)
    npt.assert_almost_equal(dist, expectedDist)
    npt.assert_array_almost_equal(expectedPnear, pnear)


def test_nplnpt():
    linept = [1.0, 2.0, 3.0]
    linedr = [0.0, 1.0, 1.0]
    point = [-6.0, 9.0, 10.0]
    pnear, dist = spice.nplnpt(linept, linedr, point)
    expectedPnear = [1.0, 9.0, 10.0]
    expectedDist = 7.0
    assert dist == expectedDist
    npt.assert_array_almost_equal(expectedPnear, pnear)


def test_nvc2pl():
    normal = [1.0, 1.0, 1.0]
    constant = 23.0
    expectedConstant = 13.279056
    expectedNormal = [0.57735027, 0.57735027, 0.57735027]
    plane = spice.nvc2pl(normal, constant)
    npt.assert_array_almost_equal(plane.normal, expectedNormal)
    npt.assert_almost_equal(plane.constant, expectedConstant, decimal=6)


def test_nvp2pl():
    normal = [1.0, 1.0, 1.0]
    point = [1.0, 4.0, 9.0]
    expectedConstant = 8.0829038
    expectedNormal = [0.57735027, 0.57735027, 0.57735027]
    plane = spice.nvp2pl(normal, point)
    npt.assert_array_almost_equal(plane.normal, expectedNormal)
    npt.assert_almost_equal(plane.constant, expectedConstant, decimal=6)


def test_ordc():
    assert 1


def test_ordd():
    assert 1


def test_ordi():
    assert 1


def test_orderc():
    assert 1


def test_orderd():
    assert 1


def test_orderi():
    assert 1


def test_oscelt():
    assert 1


def test_pckcov():
    assert 1


def test_pckfrm():
    assert 1


def test_pcklof():
    assert 1


def test_pckuof():
    assert 1


def test_pcpool():
    assert 1


def test_pdpool():
    assert 1


def test_pgrrec():
    assert 1


def test_pi():
    assert spice.pi() == np.pi


def test_pipool():
    assert 1


def test_pjelpl():
    center = [1.0, 1.0, 1.0]
    vec1 = [2.0, 0.0, 0.0]
    vec2 = [0.0, 1.0, 1.0]
    normal = [0.0, 0.0, 1.0]
    plane = spice.nvc2pl(normal, 0.0)
    elin = spice.cgv2el(center, vec1, vec2)
    ellipse = spice.pjelpl(elin, plane)
    expectedSmajor = [2.0, 0.0, 0.0]
    expectedSminor = [0.0, 1.0, 0.0]
    expectedCenter = [1.0, 1.0, 0.0]
    npt.assert_array_almost_equal(expectedCenter, ellipse.center)
    npt.assert_array_almost_equal(expectedSmajor, ellipse.semi_major)
    npt.assert_array_almost_equal(expectedSminor, ellipse.semi_minor)


def test_pl2nvc():
    normal = [-1.0, 5.0, -3.5]
    point = [9.0, -0.65, -12.0]
    plane = spice.nvp2pl(normal, point)
    normal, constant = spice.pl2nvc(plane)
    expectedNormal = [-0.16169042, 0.80845208, -0.56591646]
    npt.assert_almost_equal(constant, 4.8102899, decimal=6)
    npt.assert_array_almost_equal(expectedNormal, normal, decimal=6)


def test_pl2nvp():
    plane_norm = [2.44, -5.0 / 3.0, 11.0 / 9.0]
    const = 3.141592654
    plane = spice.nvc2pl(plane_norm, const)
    norm_vec, point = spice.pl2nvp(plane)
    expectedPoint = [0.74966576, -0.51206678, 0.37551564]
    npt.assert_array_almost_equal(expectedPoint, point)


def test_pl2psv():
    normal = [-1.0, 5.0, -3.5]
    point = [9.0, -0.65, -12.0]
    plane = spice.nvp2pl(normal, point)
    point, span1, span2 = spice.pl2psv(plane)
    npt.assert_almost_equal(spice.vdot(point, span1), 0)
    npt.assert_almost_equal(spice.vdot(point, span2), 0)
    npt.assert_almost_equal(spice.vdot(span1, span2), 0)


def test_pos():
    string = "AN ANT AND AN ELEPHANT        "
    assert spice.pos(string, "AN", 0) == 0
    assert spice.pos(string, "AN", 2) == 3
    assert spice.pos(string, "AN", 5) == 7
    assert spice.pos(string, "AN", 9) == 11
    assert spice.pos(string, "AN", 13) == 19
    assert spice.pos(string, "AN", 21) == -1
    assert spice.pos(string, "AN", -6) == 0
    assert spice.pos(string, "AN", -1) == 0
    assert spice.pos(string, "AN", 30) == -1
    assert spice.pos(string, "AN", 43) == -1
    assert spice.pos(string, "AN", 0) == 0
    assert spice.pos(string, " AN", 0) == 2
    assert spice.pos(string, " AN ", 0) == 10
    assert spice.pos(string, " AN  ", 0) == -1


def test_posr():
    string = "AN ANT AND AN ELEPHANT        "
    assert spice.posr(string, "AN", 29) == 19
    assert spice.posr(string, "AN", 18) == 11
    assert spice.posr(string, "AN", 10) == 7
    assert spice.posr(string, "AN", 6) == 3
    assert spice.posr(string, "AN", 2) == 0
    assert spice.posr(string, "AN", -6) == -1
    assert spice.posr(string, "AN", -1) == -1
    assert spice.posr(string, "AN", 30) == 19
    assert spice.posr(string, "AN", 43) == 19
    assert spice.posr(string, " AN", 29) == 10
    assert spice.posr(string, " AN ", 29) == 10
    assert spice.posr(string, " AN ", 9) == -1
    assert spice.posr(string, " AN  ", 29) == -1


def test_prompt():
    assert 1


def test_prop2b():
    assert 1


def test_prsdp():
    assert spice.prsdp("-1. 000") == -1.0


def test_prsint():
    assert spice.prsint("PI") == 3


def test_psv2pl():
    epoch = 'Jan 1 2005'
    frame = 'ECLIPJ2000'
    spice.furnsh(_testKernelPath)
    et = spice.str2et(epoch)
    state, ltime = spice.spkezr('EARTH', et, frame, 'NONE', 'Solar System Barycenter')
    es_plane = spice.psv2pl(state[0:3], state[0:3], state[3:6])
    es_norm, es_const = spice.pl2nvc(es_plane)
    mstate, mltime = spice.spkezr('MOON', et, frame, 'NONE', 'EARTH BARYCENTER')
    em_plane = spice.psv2pl(mstate[0:3], mstate[0:3], mstate[3:6])
    em_norm, em_const = spice.pl2nvc(em_plane)
    spice.kclear()
    npt.assert_almost_equal(spice.vsep(es_norm, em_norm) * spice.dpr(), 5.0424941, decimal=6)


def test_putcml():
    assert 1


def test_pxform():
    assert 1


def test_q2m():
    mout = spice.q2m(np.array([0.5, 0.4, 0.3, 0.1]))
    expected = np.array([[0.607843137254902, 0.27450980392156854, 0.7450980392156862],
                         [0.6666666666666666, 0.33333333333333326, -0.6666666666666666],
                         [-0.43137254901960775, 0.9019607843137255, 0.019607843137254832]])
    assert np.array_equal(expected, mout)


def test_qdq2av():
    assert 1


def test_qxq():
    qID = [1.0, 0.0, 0.0, 0.0]
    nqID = [-1.0, 0.0, 0.0, 0.0]
    qI = [0.0, 1.0, 0.0, 0.0]
    qJ = [0.0, 0.0, 1.0, 0.0]
    qK = [0.0, 0.0, 0.0, 1.0]
    assert spice.qxq(qI, qJ) == qK
    assert spice.qxq(qJ, qK) == qI
    assert spice.qxq(qK, qI) == qJ
    assert spice.qxq(qI, qI) == nqID
    assert spice.qxq(qJ, qJ) == nqID
    assert spice.qxq(qK, qK) == nqID
    assert spice.qxq(qID, qI) == qI
    assert spice.qxq(qI, qID) == qI


def test_radrec():
    assert 1


def test_rav2xf():
    assert 1


def test_raxisa():
    axis = [1.0, 2.0, 3.0]
    angle = 0.1 * spice.twopi()
    rotate_matrix = spice.axisar(axis, angle)
    axout, angout = spice.raxisa(rotate_matrix)
    expectedAngout = [0.26726124, 0.53452248, 0.80178373]
    npt.assert_approx_equal(angout, 0.62831853, significant=7)
    npt.assert_array_almost_equal(axout, expectedAngout)


def test_rdtext():
    assert 1


def test_reccyl():
    expected1 = np.array([0.0, 0.0, 0.0])
    expected2 = np.array([1.0, 90.0 * spice.rpd(), 0.0])
    expected3 = np.array([1.0, 270.0 * spice.rpd(), 0.0])
    npt.assert_array_almost_equal(expected1, spice.reccyl([0.0, 0.0, 0.0]), decimal=7)
    npt.assert_array_almost_equal(expected2, spice.reccyl([0.0, 1.0, 0.0]), decimal=7)
    npt.assert_array_almost_equal(expected3, spice.reccyl([0.0, -1.0, 0.0]), decimal=7)


def test_recgeo():
    assert 1


def test_reclat():
    assert 1


def test_recpgr():
    assert 1


def test_recrad():
    assert 1


def test_recsph():
    v1 = np.array([-1.0, 0.0, 0.0])
    assert spice.recsph(v1) == (1.0, np.pi/2, np.pi)


def test_removc():
    assert 1


def test_removd():
    cell = spice.stypes.SPICEDOUBLE_CELL(10)
    items = [0.0, 1.0, 1.0, 2.0, 3.0, 5.0, 8.0, 13.0, 21.0]
    for i in items:
        spice.insrtd(i, cell)
    removeItems = [0.0, 2.0, 4.0, 6.0, 8.0, 12.0]
    for r in removeItems:
        spice.removd(r, cell)
    expected = [1.0, 3.0, 5.0, 13.0, 21.0]
    for x, y in zip(cell, expected):
        assert x == y


def test_removi():
    cell = spice.stypes.SPICEINT_CELL(10)
    items = [0, 1, 1, 2, 3, 5, 8, 13, 21]
    for i in items:
        spice.insrti(i, cell)
    removeItems = [0, 2, 4, 6, 8, 12]
    for r in removeItems:
        spice.removi(r, cell)
    expected = [1, 3, 5, 13, 21]
    for x, y in zip(cell, expected):
        assert x == y


def test_reordc():
    assert 1


def test_reordd():
    assert 1


def test_reordi():
    assert 1


def test_reordl():
    assert 1


def test_repmc():
    assert 1


def test_repmct():
    assert 1


def test_repmd():
    assert 1


def test_repmf():
    assert 1


def test_repmi():
    assert 1


def test_repmot():
    assert 1


def test_reset():
    assert 1


def test_return():
    assert 1


def test_rotate():
    mout = spice.rotate(spice.pi() / 4, 3)
    mExpected = [[np.sqrt(2) / 2.0, np.sqrt(2) / 2.0, 0.0],
                 [-np.sqrt(2) / 2.0, np.sqrt(2) / 2.0, 0.0],
                 [0.0, 0.0, 1.0]]
    npt.assert_array_almost_equal(mout, mExpected)


def test_rotmat():
    ident = spice.ident()
    expectedR = [[0.0, 0.0, -1.0],
                 [0.0, 1.0, 0.0],
                 [1.0, 0.0, 0.0]]
    rOut = spice.rotmat(ident, spice.halfpi(), 2)
    npt.assert_array_almost_equal(rOut, expectedR)


def test_rotvec():
    vin = [np.sqrt(2), 0.0, 0.0]
    angle = spice.pi() / 4
    iaxis = 3
    vExpected = [1.0, -1.0, 0.0]
    vout = spice.rotvec(vin, angle, iaxis)
    npt.assert_array_almost_equal(vout, vExpected)


def test_rpd():
    assert spice.rpd() == np.arccos(-1.0) / 180.0


def test_rquad():
    # solve x^2 + 2x + 3 = 0
    root1, root2 = spice.rquad(1.0, 2.0, 3.0)
    expectedRootOne = [-1.0, np.sqrt(2.0)]
    expectedRootTwo = [-1.0, -np.sqrt(2.0)]
    npt.assert_array_almost_equal(root1, expectedRootOne)
    npt.assert_array_almost_equal(root2, expectedRootTwo)


def test_saelgv():
    vec1 = [1.0, 1.0, 1.0]
    vec2 = [1.0, -1.0, 1.0]
    expectedSmajor = [np.sqrt(2.0), 0.0, np.sqrt(2.0)]
    expectedSminor = [0.0, np.sqrt(2.0), 0.0]
    smajor, sminor = spice.saelgv(vec1, vec2)
    npt.assert_array_almost_equal(smajor, expectedSmajor)
    npt.assert_array_almost_equal(sminor, expectedSminor)


def test_scard():
    cell = spice.stypes.SPICEDOUBLE_CELL(10)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    assert spice.card(cell) == 0
    for w in darray:
        spice.wninsd(w[0], w[1], cell)
    assert spice.card(cell) == 6
    spice.scard(0, cell)
    assert spice.card(cell) == 0


def test_scdecd():
    assert 1


def test_sce2c():
    assert 1


def test_sce2s():
    assert 1


def test_sce2t():
    assert 1


def test_scencd():
    assert 1


def test_scfmt():
    assert 1


def test_scpart():
    assert 1


def test_scs2e():
    assert 1


def test_sct2e():
    assert 1


def test_sctiks():
    assert 1


def test_sdiff():
    assert 1


def test_set():
    assert 1


def test_setmsg():
    assert 1


def test_shellc():
    array = ["FEYNMAN", "NEWTON", "EINSTEIN", "GALILEO", "EUCLID", "Galileo"]
    expected = ["EINSTEIN", "EUCLID", "FEYNMAN", "GALILEO", "Galileo", "NEWTON"]
    assert spice.shellc(6, 10, array) == expected


def test_shelld():
    array = [99.0, 33.0, 55.0, 44.0, -77.0, 66.0]
    expected = [-77.0, 33.0, 44.0, 55.0, 66.0, 99.0]
    assert spice.shelld(6, array) == expected


def test_shelli():
    array = [99, 33, 55, 44, -77, 66]
    expected = [-77, 33, 44, 55, 66, 99]
    assert spice.shelli(6, array) == expected


def test_sigerr():
    assert 1


def test_sincpt():
    assert 1


def test_size():
    assert 1


def test_spd():
    assert spice.spd() == 86400.0


def test_sphcyl():
    assert 1


def test_sphlat():
    assert 1


def test_sphrec():
    assert 1


def test_spk14a():
    assert 1


def test_spk14b():
    assert 1


def test_spk14e():
    assert 1


def test_spkacs():
    assert 1


def test_spkapo():
    assert 1


def test_spkapp():
    assert 1


def test_spkaps():
    assert 1


def test_spkcls():
    assert 1


def test_spkcov():
    assert 1


def test_spkez():
    assert 1


def test_spkezp():
    assert 1


def test_spkezr():
    assert 1


def test_spkgeo():
    assert 1


def test_spkgps():
    assert 1


def test_spklef():
    assert 1


def test_spkltc():
    assert 1


def test_spkobj():
    assert 1


def test_spkopa():
    assert 1


def test_spkopn():
    assert 1


def test_spkpds():
    assert 1


def test_spkpos():
    assert 1


def test_spkssb():
    assert 1


def test_spksub():
    assert 1


def test_spkuds():
    assert 1


def test_spkuef():
    assert 1


def test_spkw02():
    assert 1


def test_spkw03():
    assert 1


def test_spkw05():
    assert 1


def test_spkw08():
    assert 1


def test_spkw09():
    assert 1


def test_spkw10():
    assert 1


def test_spkw12():
    assert 1


def test_spkw13():
    assert 1


def test_spkw15():
    assert 1


def test_spkw17():
    assert 1


def test_spkw18():
    assert 1


def test_srfrec():
    assert 1


def test_srfxpt():
    assert 1


def test_ssize():
    assert 1


def test_stelab():
    assert 1


def test_stpool():
    assert 1


def test_str2et():
    assert 1


def test_subpnt():
    assert 1


def test_subpt():
    assert 1


def test_subslr():
    assert 1


def test_subsol():
    assert 1


def test_sumad():
    assert 1


def test_sumai():
    assert 1


def test_surfnm():
    point = [0.0, 0.0, 3.0]
    assert spice.surfnm(1.0, 2.0, 3.0, point) == [0.0, 0.0, 1.0]


def test_surfpt():
    position = [2.0, 0.0, 0.0]
    u = [-1.0, 0.0, 0.0]
    point = spice.surfpt(position, u, 1.0, 2.0, 3.0)
    assert point == [1.0, 0.0, 0.0]


def test_surfpv():
    assert 1


def test_swpool():
    assert 1


def test_sxform():
    assert 1


def test_szpool():
    assert 1


def test_timdef():
    assert 1


def test_timout():
    assert 1


def test_tipbod():
    assert 1


def test_tisbod():
    assert 1


def test_tkvrsn():
    version = spice.tkvrsn("toolkit")
    assert version == "CSPICE_N0065"


def test_tparse():
    assert 1


def test_tpictr():
    testString = "10:23 P.M. PDT January 3, 1993"
    pictur, ok, err = spice.tpictr(testString, 80, 80)
    assert pictur == "AP:MN AMPM PDT Month DD, YYYY ::UTC-7"


def test_trace():
    matrix = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    assert spice.trace(matrix) == 3.0


def test_trcoff():
    assert 1


def test_tsetyr():
    assert 1


def test_twopi():
    assert spice.twopi() == np.pi * 2


def test_twovec():
    axdef = [1.0, 0.0, 0.0]
    plndef = [0.0, -1.0, 0.0]
    expected = [[1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, -1.0]]
    assert spice.twovec(axdef, 1, plndef, 2) == expected


def test_tyear():
    assert spice.tyear() == 31556925.9747


def test_ucase():
    assert spice.ucase("hi") == "HI"
    assert spice.ucase("hi", 3) == "HI"


def test_ucrss():
    assert 1


def test_uddc():
    assert 1


def test_uddf():
    assert 1


def test_union():
    assert 1


def test_unitim():
    assert 1


def test_unload():
    spice.furnsh(_testKernelPath)
    # 4 kernels + the meta kernel = 5
    assert spice.ktotal("ALL") == 5
    spice.unload(_testKernelPath)
    assert spice.ktotal("ALL") == 0
    spice.kclear()


def test_unorm():
    v1 = np.array([5.0, 12.0, 0.0])
    expectedVout = np.array([5.0 / 13.0, 12.0 / 13.0, 0.0])
    expectedVmag = 13.0
    vout, vmag = spice.unorm(v1)
    assert vmag == expectedVmag
    assert np.array_equal(expectedVout, vout)


def test_unormg():
    v1 = np.array([5.0, 12.0])
    expectedVout = np.array([5.0/13.0, 12.0/13.0])
    expectedVmag = 13.0
    vout, vmag = spice.unormg(v1, 2)
    assert vmag == expectedVmag
    assert np.array_equal(expectedVout, vout)


def test_utc2et():
    spice.furnsh(_testKernelPath)
    utcstr = 'December 1, 2004 15:04:11'
    output = spice.utc2et(utcstr)
    assert output == 155185515.1831043
    # icy utc2et example gives 1.5518552e+08 as output
    spice.kclear()


def test_vadd():
    v1 = [1.0, 2.0, 3.0]
    v2 = [4.0, 5.0, 6.0]
    assert spice.vadd(v1, v2) == [5.0, 7.0, 9.0]


def test_vaddg():
    v1 = [1.0, 2.0, 3.0]
    v2 = [4.0, 5.0, 6.0]
    assert spice.vaddg(v1, v2, 3) == [5.0, 7.0, 9.0]


def test_valid():
    assert 1


def test_vcrss():
    v1 = np.array([0.0, 1.0, 0.0])
    v2 = np.array([1.0, 0.0, 0.0])
    vout = spice.vcrss(v1, v2)
    expected = np.array([0.0, 0.0, -1.0])
    assert np.array_equal(vout, expected)


def test_vdist():
    v1 = np.array([2.0, 3.0, 0.0])
    v2 = np.array([5.0, 7.0, 12.0])
    assert spice.vdist(v1, v2) == 13.0


def test_vdistg():
    v1 = np.array([2.0, 3.0])
    v2 = np.array([5.0, 7.0])
    assert spice.vdistg(v1, v2, 2) == 5.0


def test_vdot():
    v1 = np.array([1.0, 0.0, -2.0])
    v2 = np.array([2.0, 1.0, -1.0])
    assert spice.vdot(v1, v2) == 4.0


def test_vdotg():
    v1 = np.array([1.0, 0.0])
    v2 = np.array([2.0, 1.0])
    assert spice.vdotg(v1, v2, 2) == 2


def test_vequ():
    v1 = np.ones(3)
    assert np.array_equal(v1, spice.vequ(v1))


def test_vequg():
    v1 = np.ones(4)
    assert np.array_equal(v1, spice.vequg(v1, 4))


def test_vhat():
    v1 = np.array([5.0, 12.0, 0.0])
    expected = np.array([5/13.0, 12/13.0, 0.0])
    vout = spice.vhat(v1)
    assert np.array_equal(vout, expected)


def test_vhatg():
    v1 = np.array([5.0, 12.0, 0.0, 0.0])
    expected = np.array([5 / 13.0, 12 / 13.0, 0.0, 0.0])
    vout = spice.vhatg(v1, 4)
    assert np.array_equal(vout, expected)


def test_vlcom3():
    assert 1


def test_vlcom():
    assert 1


def test_vlcomg():
    assert 1


def test_vminug():
    v1 = np.array([1.0, -2.0, 4.0, 0.0])
    expected = np.array([-1.0, 2.0, -4.0, 0.0])
    assert np.array_equal(spice.vminug(v1, 4), expected)


def test_vminus():
    v1 = np.array([1.0, -2.0, 0.0])
    expected = np.array([-1.0, 2.0, 0.0])
    assert np.array_equal(spice.vminus(v1), expected)


def test_vnorm():
    v1 = np.array([1.e0, 2.e0, 2.e0])
    assert spice.vnorm(v1) == 3.e0


def test_vnormg():
    v1 = np.array([3.0, 3.0, 3.0, 3.0])
    assert spice.vnormg(v1, 4) == 6.0


def test_vpack():
    assert np.array_equal(spice.vpack(1.0, 1.0, 1.0), np.ones(3))


def test_vperp():
    v1 = np.array([6.0, 6.0, 6.0])
    v2 = np.array([2.0, 0.0, 0.0])
    expected = np.array([0.0, 6.0, 6.0])
    assert np.array_equal(spice.vperp(v1, v2), expected)


def test_vprjp():
    vec1 = [-5.0, 7.0, 2.2]
    norm = [0.0, 0.0, 1.0]
    orig = [0.0, 0.0, 0.0]
    plane = spice.nvp2pl(norm, orig)
    proj = spice.vprjp(vec1, plane)
    expected = [-5.0, 7.0, 0.0]
    npt.assert_array_almost_equal(proj, expected)


def test_vprjpi():
    norm1 = [0.0, 0.0, 1.0]
    norm2 = [1.0, 0.0, 1.0]
    con1 = 1.2
    con2 = 0.65
    plane1 = spice.nvc2pl(norm1, con1)
    plane2 = spice.nvc2pl(norm2, con2)
    vec = [1.0, 1.0, 0.0]
    result = spice.vprjpi(vec, plane1, plane2)
    expected = [1.0, 1.0, -0.35]
    npt.assert_array_almost_equal(result, expected)


def test_vproj():
    v1 = np.array([6.0, 6.0, 6.0])
    v2 = np.array([2.0, 0.0, 0.0])
    expected = np.array([6.0, 0.0, 0.0])
    vout = spice.vproj(v1, v2)
    assert np.array_equal(expected, vout)


def test_vrel():
    vec1 = [12.3, -4.32, 76.0]
    vec2 = [23.0423, -11.99, -0.10]
    npt.assert_almost_equal(spice.vrel(vec1, vec2), 1.0016370)


def test_vrelg():
    vec1 = [12.3, -4.32, 76.0, 1.87]
    vec2 = [23.0423, -11.99, -0.10, -99.1]
    npt.assert_almost_equal(spice.vrelg(vec1, vec2, 4), 1.2408623)


def test_vrotv():
    v = np.array([1.0, 2.0, 3.0])
    axis = np.array([0.0, 0.0, 1.0])
    theta = spice.halfpi()
    vout = spice.vrotv(v, axis, theta)
    expected = np.array([-2.0, 1.0, 3.0])
    np.testing.assert_almost_equal(vout, expected, decimal=7)


def test_vscl():
    v1 = np.array([1.0, -2.0, 0.0])
    expected = np.array([-1.0, 2.0, 0.0])
    assert np.array_equal(spice.vscl(-1.0, v1), expected)


def test_vsclg():
    v1 = np.array([1.0, 2.0, -3.0, 4.0])
    expected = np.zeros(4)
    assert np.array_equal(spice.vsclg(0.0, v1, 4), expected)


def test_vsep():
    v1 = np.array([1.0, 0.0, 0.0])
    v2 = np.array([0.0, 1.0, 0.0])
    assert spice.vsep(v1, v2) == np.pi/2


def test_vsepg():
    v1 = np.array([3.0, 0.0])
    v2 = np.array([-5.0, 0.0])
    assert spice.vsepg(v1, v2, 2) == np.pi


def test_vsub():
    v1 = np.array([1.0, 2.0, 3.0])
    v2 = np.array([4.0, 5.0, 6.0])
    expected = np.array([-3.0, -3.0, -3.0])
    assert np.array_equal(spice.vsub(v1, v2), expected)


def test_vsubg():
    v1 = np.array([1.0, 2.0, 3.0, 4.0])
    v2 = np.array([1.0, 1.0, 1.0, 1.0])
    expected = np.array([0.0, 1.0, 2.0, 3.0])
    assert np.array_equal(spice.vsubg(v1, v2, 4), expected)


def test_vtmv():
    v1 = np.array([2.0, 4.0, 6.0])
    v2 = np.array([1.0, 1.0, 1.0])
    matrix = np.array([[0.0, 1.0, 0.0], [-1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    assert spice.vtmv(v1, matrix, v2) == 4.0


def test_vtmvg():
    v1 = np.array([1.0, 2.0, 3.0])
    v2 = np.array([1.0, 2.0])
    matrix = np.array([[2.0, 0.0], [1.0, 2.0], [1.0, 1.0]])
    assert spice.vtmvg(v1, matrix, v2, 3, 2) == 21.0


def test_vupack():
    v1 = np.array([1.0, 2.0, 3.0])
    expected = (1.0, 2.0, 3.0)
    assert spice.vupack(v1) == expected


def test_vzero():
    assert spice.vzero(np.zeros(3))


def test_vzerog():
    assert spice.vzerog(np.zeros(5), 5)


def test_wncard():
    window = spice.stypes.SPICEDOUBLE_CELL(8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    for d in darray:
        spice.wninsd(d[0], d[1], window)
    assert spice.wncard(window) == 3


def test_wncomd():
    window1 = spice.stypes.SPICEDOUBLE_CELL(8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    for d in darray:
        spice.wninsd(d[0], d[1], window1)
    assert spice.wncard(window1) == 3
    window2 = spice.wncomd(2.0, 20.0, window1)
    assert spice.wncard(window2) == 2
    assert spice.wnfetd(window2, 0) == (3.0, 7.0)
    assert spice.wnfetd(window2, 1) == (11.0, 20.0)


def test_wncond():
    window = spice.stypes.SPICEDOUBLE_CELL(8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    for d in darray:
        spice.wninsd(d[0], d[1], window)
    assert spice.wncard(window) == 3
    window = spice.wncond(2.0, 1.0, window)
    assert spice.wncard(window) == 2
    assert spice.wnfetd(window, 0) == (9.0, 10.0)
    assert spice.wnfetd(window, 1) == (25.0, 26.0)


def test_wndifd():
    window1 = spice.stypes.SPICEDOUBLE_CELL(8)
    window2 = spice.stypes.SPICEDOUBLE_CELL(8)
    darray1 = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    darray2 = [[2.0, 6.0], [8.0, 10.0], [16.0, 18.0]]
    for d in darray1:
        spice.wninsd(d[0], d[1], window1)
    assert spice.wncard(window1) == 3
    for d in darray2:
        spice.wninsd(d[0], d[1], window2)
    assert spice.wncard(window2) == 3
    window3 = spice.wndifd(window1, window2)
    assert spice.wncard(window3) == 4
    assert spice.wnfetd(window3, 0) == (1.0, 2.0)
    assert spice.wnfetd(window3, 1) == (7.0, 8.0)
    assert spice.wnfetd(window3, 2) == (10.0, 11.0)
    assert spice.wnfetd(window3, 3) == (23.0, 27.0)


def test_wnelmd():
    window = spice.stypes.SPICEDOUBLE_CELL(8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    for d in darray:
        spice.wninsd(d[0], d[1], window)
    assert spice.wncard(window) == 3
    array = [0.0, 1.0, 9.0, 13.0, 29.0]
    expected = [False, True, True, False, False]
    for a, exp in zip(array, expected):
        assert spice.wnelmd(a, window) == exp


def test_wnexpd():
    window = spice.stypes.SPICEDOUBLE_CELL(8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0], [29.0, 29.0]]
    for d in darray:
        spice.wninsd(d[0], d[1], window)
    assert spice.wncard(window) == 4
    window = spice.wnexpd(2.0, 1.0, window)
    assert spice.wncard(window) == 3
    assert spice.wnfetd(window, 0) == (-1.0, 4.0)
    assert spice.wnfetd(window, 1) == (5.0, 12.0)
    assert spice.wnfetd(window, 2) == (21.0, 30.0)


def test_wnextd():
    window = spice.stypes.SPICEDOUBLE_CELL(8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0], [29.0, 29.0]]
    for d in darray:
        spice.wninsd(d[0], d[1], window)
    assert spice.wncard(window) == 4
    window = spice.wnextd('L', window)
    assert spice.wncard(window) == 4
    assert spice.wnfetd(window, 0) == (1.0, 1.0)
    assert spice.wnfetd(window, 1) == (7.0, 7.0)
    assert spice.wnfetd(window, 2) == (23.0, 23.0)
    assert spice.wnfetd(window, 3) == (29.0, 29.0)


def test_wnfetd():
    window = spice.stypes.SPICEDOUBLE_CELL(8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    for d in darray:
        spice.wninsd(d[0], d[1], window)
    assert spice.wncard(window) == 3
    assert spice.wnfetd(window, 0) == (1.0, 3.0)
    assert spice.wnfetd(window, 1) == (7.0, 11.0)
    assert spice.wnfetd(window, 2) == (23.0, 27.0)


def test_wnfild():
    window = spice.stypes.SPICEDOUBLE_CELL(8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0], [29.0, 29.0]]
    for d in darray:
        spice.wninsd(d[0], d[1], window)
    assert spice.wncard(window) == 4
    window = spice.wnfild(3.0, window)
    assert spice.wncard(window) == 3
    assert spice.wnfetd(window, 0) == (1.0, 3.0)
    assert spice.wnfetd(window, 1) == (7.0, 11.0)
    assert spice.wnfetd(window, 2) == (23.0, 29.0)


def test_wnfltd():
    window = spice.stypes.SPICEDOUBLE_CELL(8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0], [29.0, 29.0]]
    for d in darray:
        spice.wninsd(d[0], d[1], window)
    assert spice.wncard(window) == 4
    window = spice.wnfltd(3.0, window)
    assert spice.wncard(window) == 2
    assert spice.wnfetd(window, 0) == (7.0, 11.0)
    assert spice.wnfetd(window, 1) == (23.0, 27.0)


def test_wnincd():
    window = spice.stypes.SPICEDOUBLE_CELL(8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    for d in darray:
        spice.wninsd(d[0], d[1], window)
    assert spice.wncard(window) == 3
    array = [[1.0, 3.0], [9.0, 10.0], [0.0, 2.0], [13.0, 15.0], [29.0, 30.0]]
    expected = [True, True, False, False, False]
    for a, exp in zip(array, expected):
        assert spice.wnincd(a[0], a[1], window) == exp


def test_wninsd():
    window = spice.stypes.SPICEDOUBLE_CELL(8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    for d in darray:
        spice.wninsd(d[0], d[1], window)
    assert spice.wncard(window) == 3
    assert [x for x in window] == [1.0, 3.0, 7.0, 11.0, 23.0, 27.0]


def test_wnintd():
    window1 = spice.stypes.SPICEDOUBLE_CELL(8)
    window2 = spice.stypes.SPICEDOUBLE_CELL(8)
    darray1 = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    darray2 = [[2.0, 6.0], [8.0, 10.0], [16.0, 18.0]]
    for d in darray1:
        spice.wninsd(d[0], d[1], window1)
    assert spice.wncard(window1) == 3
    for d in darray2:
        spice.wninsd(d[0], d[1], window2)
    assert spice.wncard(window2) == 3
    window3 = spice.wnintd(window1, window2)
    assert spice.wncard(window3) == 2
    assert spice.wnfetd(window3, 0) == (2.0, 3.0)
    assert spice.wnfetd(window3, 1) == (8.0, 10.0)


def test_wnreld():
    window1 = spice.stypes.SPICEDOUBLE_CELL(8)
    window2 = spice.stypes.SPICEDOUBLE_CELL(8)
    darray1 = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    darray2 = [[1.0, 2.0], [9.0, 9.0], [24.0, 27.0]]
    for d in darray1:
        spice.wninsd(d[0], d[1], window1)
    assert spice.wncard(window1) == 3
    for d in darray2:
        spice.wninsd(d[0], d[1], window2)
    assert spice.wncard(window2) == 3
    ops = ['=', '<>', '<=', '<', '>=', '>']
    expected = [False, True, False, False, True, True]
    for op, exp in zip(ops, expected):
        assert spice.wnreld(window1, op, window2) == exp


def test_wnsumd():
    window = spice.stypes.SPICEDOUBLE_CELL(12)
    darray = [[1.0, 3.0], [7.0, 11.0], [18.0, 18.0], [23.0, 27.0], [30.0, 69.0], [72.0, 80.0]]
    for d in darray:
        spice.wninsd(d[0], d[1], window)
    meas, avg, stddev, shortest, longest = spice.wnsumd(window)
    assert meas == 57.0
    assert avg == 9.5
    assert np.around(stddev, decimals=6) == 13.413302
    assert shortest == 4
    assert longest == 8


def test_wnunid():
    window1 = spice.stypes.SPICEDOUBLE_CELL(8)
    window2 = spice.stypes.SPICEDOUBLE_CELL(8)
    darray1 = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    darray2 = [[2.0, 6.0], [8.0, 10.0], [16.0, 18.0]]
    for d in darray1:
        spice.wninsd(d[0], d[1], window1)
    assert spice.wncard(window1) == 3
    for d in darray2:
        spice.wninsd(d[0], d[1], window2)
    assert spice.wncard(window2) == 3
    window3 = spice.wnunid(window1, window2)
    assert spice.wncard(window3) == 4
    assert spice.wnfetd(window3, 0) == (1.0, 6.0)
    assert spice.wnfetd(window3, 1) == (7.0, 11.0)
    assert spice.wnfetd(window3, 2) == (16.0, 18.0)
    assert spice.wnfetd(window3, 3) == (23.0, 27.0)


def test_wnvald():
    window = spice.stypes.SPICEDOUBLE_CELL(30)
    array = [[0.0, 0.0], [10.0, 12.0], [2.0, 7.0],
             [13.0, 15.0], [1.0, 5.0], [23.0, 29.0],
             [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]
    for a in array:
        spice.wninsd(a[0], a[1], window)
    result = spice.wnvald(30, 20, window)
    assert spice.wncard(result) == 5
    assert spice.wnfetd(result, 0) == (0.0, 0.0)
    assert spice.wnfetd(result, 1) == (1.0, 7.0)
    assert spice.wnfetd(result, 2) == (10.0, 12.0)
    assert spice.wnfetd(result, 3) == (13.0, 15.0)
    assert spice.wnfetd(result, 4) == (23.0, 29.0)


def test_xf2eul():
    assert 1


def test_xf2rav():
    assert 1


def test_xpose6():
    m1 = [[1.0, 2.0, 3.0, 4.0, 5.0, 6.0], [0.0, 7.0, 8.0, 9.0, 10.0, 11.0], [0.0, 0.0, 12.0, 13.0, 14.0, 15.0],
          [0.0, 0.0, 0.0, 16.0, 17.0, 18.0], [0.0, 0.0, 0.0, 0.0, 19.0, 20.0], [0.0, 0.0, 0.0, 0.0, 0.0, 21.0]]
    mout_expected = np.array(m1).transpose().tolist()
    assert spice.xpose6(m1) == mout_expected


def test_xpose():
    m1 = [[1.0, 2.0, 3.0], [0.0, 4.0, 5.0], [0.0, 6.0, 0.0]]
    assert spice.xpose(m1) == [[1.0, 0.0, 0.0], [2.0, 4.0, 6.0], [3.0, 5.0, 0.0]]
    assert spice.xpose(np.array(m1)) == [[1.0, 0.0, 0.0], [2.0, 4.0, 6.0], [3.0, 5.0, 0.0]]


def test_xposeg():
    m1 = [[1.0, 2.0, 3.0], [0.0, 4.0, 5.0], [0.0, 6.0, 0.0]]
    assert spice.xposeg(m1, 3, 3) == [[1.0, 0.0, 0.0], [2.0, 4.0, 6.0], [3.0, 5.0, 0.0]]
    assert spice.xposeg(np.array(m1), 3, 3) == [[1.0, 0.0, 0.0], [2.0, 4.0, 6.0], [3.0, 5.0, 0.0]]
