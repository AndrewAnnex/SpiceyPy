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
    CK1 = cwd + "/type1.bc"
    if os.path.isfile(CK1):
        os.remove(CK1)
    INST = -77701
    MAXREC = 201
    SECPERTICK = 0.001
    SEGID = "Test type 1 CK segment"
    IFNAME = "Test CK type 1 segment created by cspice_ckw01"
    NCOMCH = 0
    REF = "J2000"
    SPACING_TICKS = 10.0
    SPACING_SECS = SPACING_TICKS * SECPERTICK
    RATE = 0.01
    handle = spice.ckopn(CK1, IFNAME, NCOMCH)
    init_size = os.path.getsize(CK1)
    quats = np.zeros((MAXREC, 4))
    av = np.zeros((MAXREC, 3))
    work_mat = spice.ident()
    work_quat = spice.m2q(work_mat)
    quats[0] = work_quat
    av[0] = [0.0, 0.0, RATE]
    sclkdp = np.arange(MAXREC) * SPACING_TICKS
    sclkdp += 1000.0
    for i in range(1, MAXREC - 1):
        theta = i * RATE * SPACING_SECS * 1.0
        work_mat = spice.rotmat(work_mat, theta, 3)
        work_quat = spice.m2q(work_mat)
        quats[i] = work_quat
        av[i] = [0.0, 0.0, RATE]
    avflag = True
    begtime = sclkdp[0]
    endtime = sclkdp[-1]
    spice.ckw01(handle, begtime, endtime, INST, REF, avflag, SEGID, MAXREC - 1, sclkdp, quats, av)
    spice.ckcls(handle)
    end_size = os.path.getsize(CK1)
    assert end_size != init_size
    # cleanup
    if os.path.isfile(CK1):
        os.remove(CK1)


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
    spice.pdpool('TEST_VAR', [-666.0])
    value = spice.gdpool('TEST_VAR', 0, 1)
    assert len(value) == 1
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
    mag = np.array([-4.0, 4, 12])
    x = np.array([1.0, np.sqrt(2.0), np.sqrt(3.0)])
    s1 = np.array([x * 10.0 ** mag[0], x]).flatten()
    s2 = np.array([x * 10.0 ** mag[1], -x]).flatten()
    s3 = np.array([[0.0, 0.0, 0.0], x * 10 ** mag[2]]).flatten()
    npt.assert_approx_equal(spice.dvnorm(s1), 2.4494897)
    npt.assert_approx_equal(spice.dvnorm(s2), -2.4494897)
    npt.assert_approx_equal(spice.dvnorm(s3), 0.0)


def test_dvpool():
    assert 1


def test_dvsep():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et('JAN 1 2009')
    state_e, eltime = spice.spkezr('EARTH', et, 'J2000', 'NONE', 'SUN')
    state_m, mltime = spice.spkezr('MOON', et, 'J2000', 'NONE', 'SUN')
    dsept = spice.dvsep(state_e, state_m)
    npt.assert_approx_equal(dsept, 3.8121194e-09)
    spice.kclear()


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
    # same as pcpool test
    import string

    spice.kclear()
    data = [j + str(i) for i, j in enumerate(list(string.ascii_lowercase))]
    spice.pcpool('pcpool_test', data)
    cvals = spice.gcpool('pcpool_test', 0, 30, 4)
    assert data == cvals
    spice.kclear()


def test_gdpool():
    # same as pdpool test
    spice.kclear()
    data = np.arange(0.0, 10.0)
    spice.pdpool('pdpool_array', data)
    dvals = spice.gdpool('pdpool_array', 0, 30)
    npt.assert_array_almost_equal(data, dvals)
    spice.kclear()


def test_georec():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    size, radii = spice.bodvrd('EARTH', 'RADII', 3)
    flat = (radii[0] - radii[2]) / radii[0]
    lon = 118.0 * spice.rpd()
    lat = 32.0 * spice.rpd()
    alt = 0.0
    spice.kclear()
    output = spice.georec(lon, lat, alt, radii[0], flat)
    expected = [-2541.74621567, 4780.329376, 3360.4312092]
    npt.assert_array_almost_equal(expected, output)


def test_getcml():
    assert 1


def test_getelm():
    assert 1


def test_getfat():
    arch, outtype = spice.getfat(cwd + '/naif0010.tls')
    assert arch == "KPL"
    assert outtype == "LSK"


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
    # same as pipool test
    spice.kclear()
    data = np.arange(0, 10)
    spice.pipool('pipool_array', data)
    ivals = spice.gipool('pipool_array', 0, 50)
    npt.assert_array_almost_equal(data, ivals)
    spice.kclear()


def test_gnpool():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    var = "BODY599*"
    index = 0
    room = 10
    strlen = 81
    expected = ["BODY599_POLE_DEC", "BODY599_LONG_AXIS", "BODY599_PM", "BODY599_RADII",
                "BODY599_POLE_RA", "BODY599_GM", "BODY599_NUT_PREC_PM", "BODY599_NUT_PREC_DEC",
                "BODY599_NUT_PREC_RA"]
    kervar, found = spice.gnpool(var, index, room, strlen)
    spice.kclear()
    assert found
    assert set(expected) == set(kervar)


def test_halfpi():
    assert spice.halfpi() == np.pi / 2


def test_hx2dp():
    assert spice.hx2dp('1^1') == 1.0
    assert spice.hx2dp('7F5EB^5') == 521707.0
    assert spice.hx2dp('+1B^+2') == 27.0


def test_ident():
    ident = spice.ident()
    expected = np.identity(3)
    npt.assert_array_almost_equal(ident, expected)


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
    np.testing.assert_almost_equal(np.array(xpt), expectedXpt, decimal=6)
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
    assert spice.intmax() >= 2147483647 or spice.intmax() >= 32768


def test_intmin():
    assert spice.intmin() <= -2147483648 or spice.intmin() <= -32768


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
    # same as unload test
    spice.furnsh(_testKernelPath)
    # 4 kernels + the meta kernel = 5
    assert spice.ktotal("ALL") == 5
    spice.unload(_testKernelPath)
    assert spice.ktotal("ALL") == 0
    spice.kclear()


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
    spice.kclear()
    lmpoolNames = ['DELTET/DELTA_T_A', 'DELTET/K', 'DELTET/EB', 'DELTET/M', 'DELTET/DELTA_AT']
    lmpoolLens = [1, 1, 1, 2, 46]
    textbuf = ['DELTET/DELTA_T_A = 32.184', 'DELTET/K = 1.657D-3', 'DELTET/EB  = 1.671D-2',
               'DELTET/M = ( 6.239996 1.99096871D-7 )', 'DELTET/DELTA_AT = ( 10, @1972-JAN-1',
               '                     11, @1972-JUL-1',
               '                     12, @1973-JAN-1',
               '                     13, @1974-JAN-1',
               '                     14, @1975-JAN-1',
               '                     15, @1976-JAN-1',
               '                     16, @1977-JAN-1',
               '                     17, @1978-JAN-1',
               '                     18, @1979-JAN-1',
               '                     19, @1980-JAN-1',
               '                     20, @1981-JUL-1',
               '                     21, @1982-JUL-1',
               '                     22, @1983-JUL-1',
               '                     23, @1985-JUL-1',
               '                     24, @1988-JAN-1',
               '                     25, @1990-JAN-1',
               '                     26, @1991-JAN-1',
               '                     27, @1992-JUL-1',
               '                     28, @1993-JUL-1',
               '                     29, @1994-JUL-1',
               '                     30, @1996-JAN-1',
               '                     31, @1997-JUL-1',
               '                     32, @1999-JAN-1 )']
    spice.lmpool(textbuf)
    for var, expectLen in zip(lmpoolNames, lmpoolLens):
        found, n, vartype = spice.dtpool(var)
        assert found
        assert expectLen == n
        assert vartype == 'N'
    spice.kclear()


def test_lparse():
    stringtest = 'one two three four'
    items = spice.lparse(stringtest, ' ', 25)
    assert items == ['one', 'two', 'three', 'four']


def test_lparsm():
    assert 1


def test_lparss():
    assert 1


def test_lspcn():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et('21 march 2005')
    lon = spice.dpr() * spice.lspcn('EARTH', et, 'NONE')
    spice.kclear()
    npt.assert_almost_equal(lon, 0.48153787)


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
    spice.kclear()
    spice.furnsh(_testKernelPath)
    OBS = 399
    TARGET = 5
    TIME_STR = 'July 4, 2004'
    et = spice.str2et(TIME_STR)
    arrive, ltime = spice.ltime(et, OBS, "->", TARGET)
    arrive_utc = spice.et2utc(arrive, 'C', 3, 50)
    npt.assert_almost_equal(ltime, 2918.71705, decimal=4)
    assert arrive_utc == '2004 JUL 04 00:48:38.717'
    receive, rtime = spice.ltime(et, OBS, "<-", TARGET)
    receive_utc = spice.et2utc(receive, 'C', 3, 50)
    spice.kclear()
    npt.assert_almost_equal(rtime, 2918.75247, decimal=4)
    assert receive_utc == '2004 JUL 03 23:11:21.248'


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
    ticam = [[0.49127379678135830, 0.50872620321864170, 0.70699908539882417],
             [-0.50872620321864193, -0.49127379678135802, 0.70699908539882428],
             [0.70699908539882406, -0.70699908539882439, 0.01745240643728360]]
    kappa, ang2, ang1 = spice.m2eul(ticam, 3, 1, 3)
    alpha = ang1 + 1.5 * spice.pi()
    delta = spice.halfpi() - ang2
    expected = [315.000000, 1.000000, 45.000000]
    result = [spice.dpr() * alpha, spice.dpr() * delta, spice.dpr() * kappa]
    npt.assert_array_almost_equal(expected, result)


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
    doubleset = spice.stypes.SPICEDOUBLE_CELL(7)
    inputs = [8.0, 1.0, 2.0, 9.0, 7.0, 4.0, 10.0]
    expected = [4, 0, 1, 5, 3, 2, 6]
    for d in inputs:
        spice.insrtd(d, doubleset)
    for i, e in zip(inputs, expected):
        assert e == spice.ordd(i, doubleset)


def test_ordi():
    intset = spice.stypes.SPICEINT_CELL(7)
    inputs = [8, 1, 2, 9, 7, 4, 10]
    expected = [4, 0, 1, 5, 3, 2, 6]
    for i in inputs:
        spice.insrti(i, intset)
    for i, e in zip(inputs, expected):
        assert e == spice.ordi(i, intset)


def test_orderc():
    inarray = ["a", "abc", "ab"]
    expectedOrder = [0, 2, 1]
    order = spice.orderc(inarray)
    assert expectedOrder == order


def test_orderd():
    inarray = [0.0, 2.0, 1.0]
    expectedOrder = [0, 2, 1]
    order = spice.orderd(inarray)
    assert expectedOrder == order


def test_orderi():
    inarray = [0, 2, 1]
    expectedOrder = [0, 2, 1]
    order = spice.orderi(inarray)
    assert expectedOrder == order


def test_oscelt():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et('Dec 25, 2007')
    state, ltime = spice.spkezr('Moon', et, 'J2000', 'LT+S', 'EARTH')
    mass_earth = spice.bodvrd('EARTH', 'GM', 1)
    elts = spice.oscelt(state, et, mass_earth[0])
    expected = [365914.1064478308, 423931.14818353514, 0.4871779356168817, 6.185842076488205,
                1.8854463601391007, 18676.97965206709, 251812865.1837092, 1.0000]
    npt.assert_array_almost_equal(elts, expected, decimal=4)
    spice.kclear()


def test_pckcov():
    assert 1


def test_pckfrm():
    assert 1


def test_pcklof():
    assert 1


def test_pckuof():
    assert 1


def test_pcpool():
    import string
    spice.kclear()
    data = [j + str(i) for i, j in enumerate(list(string.ascii_lowercase))]
    spice.pcpool('pcpool_test', data)
    cvals = spice.gcpool('pcpool_test', 0, 30, 4)
    assert data == cvals
    spice.kclear()


def test_pdpool():
    spice.kclear()
    data = np.arange(0.0, 10.0)
    spice.pdpool('pdpool_array', data)
    dvals = spice.gdpool('pdpool_array', 0, 30)
    npt.assert_array_almost_equal(data, dvals)
    spice.kclear()


def test_pgrrec():
    assert 1


def test_pi():
    assert spice.pi() == np.pi


def test_pipool():
    spice.kclear()
    data = np.arange(0, 10)
    spice.pipool('pipool_array', data)
    ivals = spice.gipool('pipool_array', 0, 50)
    npt.assert_array_almost_equal(data, ivals)
    spice.kclear()


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
    mu = 398600.45
    r = 1.0e8
    speed = np.sqrt(mu / r)
    t = spice.pi() * (r / speed)
    pvinit = np.array([0.0, r / np.sqrt(2.0), r / np.sqrt(2.0), 0.0, -speed / np.sqrt(2.0), speed / np.sqrt(2.0)])
    state = np.array(spice.prop2b(mu, pvinit, t))
    npt.assert_array_almost_equal(state, -1.0 * pvinit, decimal=6)


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
    spice.furnsh(_testKernelPath)
    lon = 118.25 * spice.rpd()
    lat = 34.05 * spice.rpd()
    alt = 0.0
    utc = 'January 1, 2005'
    et = spice.str2et(utc)
    len, abc = spice.bodvrd('EARTH', 'RADII', 3)
    equatr = abc[0]
    polar = abc[2]
    f = (equatr - polar) / equatr
    epos = spice.georec(lon, lat, alt, equatr, f)
    rotate = np.array(spice.pxform('IAU_EARTH', 'J2000', et))
    spice.kclear()
    jstate = np.dot(epos, rotate)
    expected = np.array([5042.1309421, 1603.52962986, 3549.82398086])
    npt.assert_array_almost_equal(jstate, expected, decimal=4)


def test_pxfrm2():
    assert 1


def test_q2m():
    mout = spice.q2m(np.array([0.5, 0.4, 0.3, 0.1]))
    expected = np.array([[0.607843137254902, 0.27450980392156854, 0.7450980392156862],
                         [0.6666666666666666, 0.33333333333333326, -0.6666666666666666],
                         [-0.43137254901960775, 0.9019607843137255, 0.019607843137254832]])
    assert np.array_equal(expected, mout)


def test_qdq2av():
    angle = [-20.0 * spice.rpd(), 50.0 * spice.rpd(), -60.0 * spice.rpd()]
    m = spice.eul2m(angle[2], angle[1], angle[0], 3, 1, 3)
    q = spice.m2q(m)
    expav = [1.0, 2.0, 3.0]
    qav = [0.0, 1.0, 2.0, 3.0]
    dq = spice.qxq(q, qav)
    dq = [-0.5 * x for x in dq]
    av = spice.qdq2av(q, dq)
    npt.assert_array_almost_equal(av, expav)


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
    e = [1.0, 0.0, 0.0]
    rz = [[0.0, 1.0, 0.0],
          [-1.0, 0.0, 0.0],
          [0.0, 0.0, 1.0]]
    assert spice.rav2xf(rz, e) is not None


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
    array = ["one", "three", "two", "zero"]
    iorder = [3, 0, 2, 1]
    outarray = spice.reordc(iorder, 4, 5, array)
    assert outarray == array  # reordc appears to be broken...


def test_reordd():
    array = [1.0, 3.0, 2.0]
    iorder = [0, 2, 1]
    outarray = spice.reordd(iorder, 3, array)
    assert outarray == [1.0, 2.0, 3.0]


def test_reordi():
    array = [1, 3, 2]
    iorder = [0, 2, 1]
    outarray = spice.reordi(iorder, 3, array)
    assert outarray == [1, 2, 3]


def test_reordl():
    array = [True, True, False]
    iorder = [0, 2, 1]
    outarray = spice.reordl(iorder, 3, array)
    assert outarray == array  # reordl has the same issue as reordc


def test_repmc():
    stringtestone = "The truth is #"
    outstringone = spice.repmc(stringtestone, "#", "SPICE")
    assert outstringone == "The truth is SPICE"


def test_repmct():
    stringtestone = "The value is #"
    outstringone = spice.repmct(stringtestone, '#', 5, 'U')
    outstringtwo = spice.repmct(stringtestone, '#', 5, 'l')
    assert outstringone == "The value is FIVE"
    assert outstringtwo == "The value is five"


def test_repmd():
    stringtestone = "The value is #"
    outstringone = spice.repmd(stringtestone, '#', 5.0e11, 1)
    assert outstringone == "The value is 5.E+11"


def test_repmf():
    stringtestone = "The value is #"
    outstringone = spice.repmf(stringtestone, '#', 5.0e3, 5, 'f')
    outstringtwo = spice.repmf(stringtestone, '#', -5.2e-9, 3, 'e')
    assert outstringone == "The value is 5000.0"
    assert outstringtwo == "The value is -5.20E-09"


def test_repmi():
    stringtest = "The value is <opcode>"
    outstring = spice.repmi(stringtest, "<opcode>", 5)
    assert outstring == "The value is 5"


def test_repmot():
    stringtestone = "The value is #"
    outstringone = spice.repmot(stringtestone, '#', 5, 'U')
    outstringtwo = spice.repmot(stringtestone, '#', 5, 'l')
    assert outstringone == "The value is FIFTH"
    assert outstringtwo == "The value is fifth"


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
    MARS = 499
    MOON = 301
    EPOCH = 'Jan 1 2004 5:00 PM'
    REF = 'J2000'
    ABCORR = 'LT+S'
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et(EPOCH)
    state = spice.spkssb(MOON, et, REF)
    state_vec, ltime = spice.spkapp(MARS, et, REF, state, ABCORR)
    spice.kclear()
    expected_vec = [164534472.31249404, 25121994.36858549, 11145412.838521784,
                    12.311977095260765, 19.88840036075132, 9.406787036260496]
    npt.assert_array_almost_equal(expected_vec, state_vec, decimal=6)


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
    spice.kclear()
    spice.furnsh(_testKernelPath)
    targ1 = 499
    epoch = 'July 4, 2003 11:00 AM PST'
    frame = 'J2000'
    targ2 = 399
    et = spice.str2et(epoch)
    state1 = spice.spkssb(targ1, et, frame)
    state2 = spice.spkssb(targ2, et, frame)
    dist = spice.vdist(state1[0:3], state2[0:3])
    npt.assert_approx_equal(dist, 80854820., significant=7)
    spice.kclear()


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
    IDOBS = 399
    IDTARG = 301
    UTC = 'July 4 2004'
    FRAME = 'J2000'
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et(UTC)
    sobs = spice.spkssb(IDOBS, et, FRAME)
    starg, ltime = spice.spkapp(IDTARG, et, FRAME, sobs, 'LT')
    expected_starg = [201738.7253671214, -260893.14140683413, -147722.58904585987, 0.9247270944892598,
                      0.532379624943486, 0.21766976140206307]
    npt.assert_array_almost_equal(expected_starg, starg)
    cortarg = spice.stelab(starg[0:3], starg[3:6])
    expected_cortarg = [201739.81114959955, -260892.46234305593, -147722.30552692513]
    npt.assert_array_almost_equal(expected_cortarg, cortarg)
    spice.kclear()


def test_stpool():
    assert 1


def test_str2et():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    date = 'Thu Mar 20 12:53:29 PST 1997'
    et = spice.str2et(date)
    npt.assert_almost_equal(et, -87836728.81438904)
    spice.kclear()


def test_subpnt():
    assert 1


def test_subpt():
    assert 1


def test_subslr():
    assert 1


def test_subsol():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    point = spice.subsol('near point', 'earth', 0.0, 'lt+s', 'mars')
    npt.assert_array_almost_equal(point, [5850.44947427, 509.68837118, -2480.24722673], decimal=4)
    intercept = spice.subsol('intercept', 'earth', 0.0, 'lt+s', 'mars')
    npt.assert_array_almost_equal(intercept, [5844.4362338, 509.16450054, -2494.39569089], decimal=4)
    spice.kclear()


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
    spice.furnsh(_testKernelPath)
    lon = 118.25 * spice.rpd()
    lat = 34.05 * spice.rpd()
    alt = 0.0
    utc = 'January 1, 1990'
    et = spice.str2et(utc)
    len, abc = spice.bodvrd('EARTH', 'RADII', 3)
    equatr = abc[0]
    polar = abc[2]
    f = (equatr - polar) / equatr
    estate = spice.georec(lon, lat, alt, equatr, f)
    estate += [0.0, 0.0, 0.0]
    xform = np.array(spice.sxfrom('IAU_EARTH', 'J2000', et))
    spice.kclear()
    jstate = np.dot(xform, estate)
    expected = np.array([-4131.45969, -3308.36805, 3547.02462, 0.241249619, -0.301019201, 0.000234215666])
    npt.assert_array_almost_equal(jstate, expected, decimal=4)


def test_szpool():
    assert spice.szpool("MAXVAR") == 26003
    assert spice.szpool("MAXLEN") == 32
    assert spice.szpool("MAXVAL") == 400000
    assert spice.szpool("MXNOTE") == 130015
    assert spice.szpool("MAXAGT") == 1000
    assert spice.szpool("MAXCHR") == 80
    assert spice.szpool("MAXLIN") == 15000


def test_timdef():
    value = spice.timdef('GET', 'CALENDAR', 10)
    assert value == 'GREGORIAN' or 'JULIAN' or 'MIXED'


def test_timout():
    sample = 'Thu Oct 1 11:11:11 PDT 1111'
    lenout = len(sample) + 2
    spice.furnsh(_testKernelPath)
    pic, ok, err = spice.tpictr(sample, 64, 60)
    assert ok
    et = 188745364.0
    out = spice.timout(et, pic, lenout)
    assert out == "Sat Dec 24 18:14:59 PDT 2005"
    spice.kclear()


def test_tipbod():
    spice.furnsh(_testKernelPath)
    et = spice.str2et('Jan 1 2005')
    tipm = spice.tipbod('J2000', 699, et)
    assert tipm is not None
    spice.kclear()


def test_tisbod():
    spice.furnsh(_testKernelPath)
    et = spice.str2et('Jan 1 2005')
    tsipm = spice.tisbod('J2000', 699, et)
    assert tsipm is not None
    spice.kclear()


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
    spice.furnsh(_testKernelPath)
    et = spice.str2et('Dec 19 2003')
    converted_et = spice.unitim(et, 'ET', 'JED')
    npt.assert_almost_equal(converted_et, 2452992.5007428653)
    spice.kclear()


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
    data = np.arange(0, 10)[::-1]
    a = spice.stypes.SPICEDOUBLE_CELL(20)
    for x in data:
        spice.appndd(x, a)
    assert a.is_set() is False
    a = spice.valid(20, 10, a)
    assert a.is_set() is True


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
    e = [1.0, 0.0, 0.0]
    rz = [[0.0, 1.0, 0.0],
          [-1.0, 0.0, 0.0],
          [0.0, 0.0, 1.0]]
    xform = spice.rav2xf(rz, e)
    rz2, e2 = spice.xf2rav(xform)
    assert e == e2
    assert rz == rz2


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
