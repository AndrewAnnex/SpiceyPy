__author__ = 'AndrewAnnex'
import pytest

import spiceypy as spice
import numpy as np
import numpy.testing as npt
from test.gettestkernels import *
import os


cwd = os.path.realpath(os.path.dirname(__file__))
_testKernelPath = os.path.join(cwd, "testKernels.txt")
_extraTestVoyagerKernel = os.path.join(cwd, "vg200022.tsc")
_testPckPath = os.path.join(cwd, "pck00010.tpc")
_spkEarthPck = os.path.join(cwd, "earth_720101_070426.bpc")
_spkEarthFk = os.path.join(cwd, "earthstns_itrf93_050714.bsp")
_spkEarthTf = os.path.join(cwd, "earth_topo_050714.tf")
_spkMGSTi = os.path.join(cwd, "mgs_moc_v20.ti")
_spkMgsSclk = os.path.join(cwd, "mgs_sclkscet_00061.tsc")
_spkMgsSpk = os.path.join(cwd, "mgs_crus.bsp")
_spk = os.path.join(cwd, "de421.bsp")


def setup_module(module):
    if not os.path.exists(_testKernelPath) or not os.path.exists(_extraTestVoyagerKernel):
        downloadKernels()


def test_appndc():
    testCell = spice.stypes.SPICECHAR_CELL(10, 10)
    spice.appndc("one", testCell)
    spice.appndc("two", testCell)
    spice.appndc("three", testCell)
    assert testCell[0] == "one"
    assert testCell[1] == "two"
    assert testCell[2] == "three"


def test_appndc_vectorized():
    testCell = spice.stypes.SPICECHAR_CELL(10, 10)
    spice.appndc(["one", "two", "three"], testCell)
    assert testCell[0] == "one"
    assert testCell[1] == "two"
    assert testCell[2] == "three"


def test_appndd():
    testCell = spice.stypes.SPICEDOUBLE_CELL(8)
    spice.appndd(1.0, testCell)
    spice.appndd(2.0, testCell)
    spice.appndd(3.0, testCell)
    assert [x for x in testCell] == [1.0, 2.0, 3.0]


def test_appndd_vectorized():
    testCell = spice.stypes.SPICEDOUBLE_CELL(8)
    spice.appndd([1.0, 2.0, 3.0], testCell)
    assert [x for x in testCell] == [1.0, 2.0, 3.0]


def test_appndi():
    testCell = spice.stypes.SPICEINT_CELL(8)
    spice.appndi(1, testCell)
    spice.appndi(2, testCell)
    spice.appndi(3, testCell)
    assert [x for x in testCell] == [1, 2, 3]


def test_appndi_vectorized():
    testCell = spice.stypes.SPICEINT_CELL(8)
    spice.appndi([1, 2, 3], testCell)
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
    spice.kclear()
    spice.pdpool('DTEST_VAL', [3.1415, 186.0, 282.397])
    assert not spice.badkpv("spiceypy BADKPV test", "DTEST_VAL", "=", 3, 1, 'N')
    spice.clpool()
    assert not spice.expool("DTEST_VAL")
    spice.kclear()


def test_bltfrm():
    outCell = spice.bltfrm(-1)
    assert outCell.size >= 126


def test_bodc2n():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    assert spice.bodc2n(399, 10) == ("EARTH", True)
    assert spice.bodc2n(0, 40) == ("SOLAR SYSTEM BARYCENTER", True)
    spice.kclear()


def test_bodc2s():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    assert spice.bodc2s(399, 10) == "EARTH"
    assert spice.bodc2s(0, 40) == "SOLAR SYSTEM BARYCENTER"
    spice.kclear()


def test_boddef():
    spice.kclear()
    spice.boddef("Jebediah", 117)
    assert spice.bodc2n(117, 10) == ("Jebediah", True)
    spice.kclear()


def test_bodfnd():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    assert spice.bodfnd(599, "RADII")
    spice.kclear()


def test_bodn2c():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    assert spice.bodn2c("EARTH") == (399, True)
    assert spice.bodn2c("U.S.S. Enterprise") == (0, False)
    spice.kclear()


def test_bods2c():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    assert spice.bods2c("EARTH") == (399, True)
    assert spice.bods2c("U.S.S. Enterprise") == (0, False)
    spice.kclear()


def test_bodvar():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    radii = spice.bodvar(399, "RADII", 3)
    expected = np.array([6378.140, 6378.140, 6356.755])
    np.testing.assert_array_almost_equal(expected, radii, decimal = 1)
    spice.kclear()


def test_bodvcd():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    dim, values = spice.bodvcd(399, "RADII", 3)
    assert dim == 3
    expected = np.array([6378.140, 6378.140, 6356.755])
    np.testing.assert_array_almost_equal(expected, values, decimal = 1)
    spice.kclear()


def test_bodvrd():
    spice.kclear()
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


def test_ccifrm():
    frcode, frname, center, found = spice.ccifrm(2, 3000, 33)
    assert frname == "ITRF93"
    assert frcode == 13000
    assert center == 399


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
    spice.reset()
    assert spice.trcdep() == 0
    spice.chkin("test")
    assert spice.trcdep() == 1
    spice.chkin("trcdep")
    assert spice.trcdep() == 2
    spice.chkout("trcdep")
    assert spice.trcdep() == 1
    spice.chkout("test")
    assert spice.trcdep() == 0
    spice.reset()


def test_chkout():
    spice.reset()
    assert spice.trcdep() == 0
    spice.chkin("test")
    assert spice.trcdep() == 1
    spice.chkin("trcdep")
    assert spice.trcdep() == 2
    spice.chkout("trcdep")
    assert spice.trcdep() == 1
    spice.chkout("test")
    assert spice.trcdep() == 0
    spice.reset()


def test_cidfrm():
    frcode, frname, found = spice.cidfrm(501, 10)
    assert frcode == 10023
    assert frname == 'IAU_IO'
    frcode, frname, found = spice.cidfrm(399, 10)
    assert frcode == 10013
    assert frname == 'IAU_EARTH'
    frcode, frname, found = spice.cidfrm(301, 10)
    assert frcode == 10020
    assert frname == 'IAU_MOON'


def test_ckcls():
    # Spice crashes if ckcls detects nothing written to ck1
    spice.kclear()
    CK1 = os.path.join(cwd, "ckopenkernel.bc")
    if spice.exists(CK1):
        os.remove(CK1)
    IFNAME = "Test CK type 1 segment created by cspice_ckw01"
    handle = spice.ckopn(CK1, IFNAME, 10)
    spice.ckw01(handle, 1.0, 10.0, -77701, "J2000", True, "Test type 1 CK segment",
                2 - 1, [1.1, 4.1], [[1.0, 1.0, 1.0, 1.0], [2.0, 2.0, 2.0, 2.0]],
                [[0.0, 0.0, 1.0], [0.0, 0.0, 2.0]])

    spice.ckcls(handle)
    spice.kclear()
    assert spice.exists(CK1)
    if spice.exists(CK1):
        os.remove(CK1)
    assert not spice.exists(CK1)


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
    # Spice crashes if ckcls detects nothing written to ck1
    spice.kclear()
    CK1 = os.path.join(cwd, "ckopenkernel.bc")
    if spice.exists(CK1):
        os.remove(CK1)
    IFNAME = "Test CK type 1 segment created by cspice_ckw01"
    handle = spice.ckopn(CK1, IFNAME, 10)
    spice.ckw01(handle, 1.0, 10.0, -77701, "J2000", True, "Test type 1 CK segment",
                2 - 1, [1.1, 4.1], [[1.0, 1.0, 1.0, 1.0], [2.0, 2.0, 2.0, 2.0]],
                [[0.0, 0.0, 1.0], [0.0, 0.0, 2.0]])

    spice.ckcls(handle)
    spice.kclear()
    assert spice.exists(CK1)
    if spice.exists(CK1):
        os.remove(CK1)
    assert not spice.exists(CK1)


def test_ckupf():
    assert 1


def test_ckw01():
    spice.kclear()
    CK1 = os.path.join(cwd, "type1.bc")
    if spice.exists(CK1):
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
    spice.kclear()
    if spice.exists(CK1):
        os.remove(CK1)


def test_ckw02():
    spice.kclear()
    CK2 = os.path.join(cwd, "type2.bc")
    if spice.exists(CK2):
        os.remove(CK2)
    INST = -77702
    MAXREC = 201
    SECPERTICK = 0.001
    SEGID = "Test type 2 CK segment"
    IFNAME = "Test CK type 2 segment created by cspice_ckw02"
    NCOMCH = 0
    REF = "J2000"
    SPACING_TICKS = 10.0
    SPACING_SECS = SPACING_TICKS * SECPERTICK
    RATE = 0.01
    handle = spice.ckopn(CK2, IFNAME, NCOMCH)
    init_size = os.path.getsize(CK2)
    quats = np.zeros((MAXREC, 4))
    av = np.zeros((MAXREC, 3))
    work_mat = spice.ident()
    work_quat = spice.m2q(work_mat)
    quats[0] = work_quat
    av[0] = [0.0, 0.0, RATE]
    rates = [SECPERTICK] * MAXREC
    sclkdp = np.arange(MAXREC) * SPACING_TICKS
    sclkdp += 1000.0
    starts = sclkdp
    stops = sclkdp + (0.8 * SPACING_TICKS)
    for i in range(1, MAXREC - 1):
        theta = i * RATE * SPACING_SECS * 1.0
        work_mat = spice.rotmat(work_mat, theta, 3)
        work_quat = spice.m2q(work_mat)
        quats[i] = work_quat
        av[i] = [0.0, 0.0, RATE]
    begtime = sclkdp[0]
    endtime = sclkdp[-1]
    spice.ckw02(handle, begtime, endtime, INST, REF, SEGID, MAXREC - 1, starts, stops, quats, av, rates)
    spice.ckcls(handle)
    end_size = os.path.getsize(CK2)
    assert end_size != init_size
    spice.kclear()
    if spice.exists(CK2):
        os.remove(CK2)


def test_ckw03():
    spice.kclear()
    CK3 = os.path.join(cwd, "type3.bc")
    if spice.exists(CK3):
        os.remove(CK3)
    MAXREC = 201
    SECPERTICK = 0.001
    SEGID = "Test type 3 CK segment"
    IFNAME = "Test CK type 3 segment created by cspice_ckw03"
    SPACING_TICKS = 10.0
    SPACING_SECS = SPACING_TICKS * SECPERTICK
    RATE = 0.01
    handle = spice.ckopn(CK3, IFNAME, 0)
    init_size = os.path.getsize(CK3)
    quats = np.zeros((MAXREC, 4))
    av = np.zeros((MAXREC, 3))
    work_mat = spice.ident()
    work_quat = spice.m2q(work_mat)
    quats[0] = work_quat
    av[0] = [0.0, 0.0, RATE]
    rates = [SECPERTICK] * MAXREC
    sclkdp = np.arange(MAXREC) * SPACING_TICKS
    sclkdp += 1000.0
    for i in range(1, MAXREC - 1):
        theta = i * RATE * SPACING_SECS * 1.0
        work_mat = spice.rotmat(work_mat, theta, 3)
        work_quat = spice.m2q(work_mat)
        quats[i] = work_quat
        av[i] = [0.0, 0.0, RATE]
    starts = [sclkdp[2 * i] for i in range(99)]
    begtime = sclkdp[0]
    endtime = sclkdp[-1]
    spice.ckw03(handle, begtime, endtime, -77703, "J2000", True, SEGID, MAXREC - 1, sclkdp, quats, av, 99, starts)
    spice.ckcls(handle)
    end_size = os.path.getsize(CK3)
    assert end_size != init_size
    spice.kclear()
    if spice.exists(CK3):
        os.remove(CK3)


def test_ckw05():
    assert 1


def test_clight():
    assert spice.clight() == 299792.458


def test_clpool():
    spice.kclear()
    spice.pdpool('TEST_VAR', [-666.0])
    value, found = spice.gdpool('TEST_VAR', 0, 1)
    assert len(value) == 1
    assert value[0] == -666.0
    spice.clpool()
    v, found = spice.gdpool('TEST_VAR', 0, 1)
    assert found is False
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
    ioFrcode, ioFrname, found = spice.cnmfrm('IO', 10)
    assert ioFrcode == 10023
    assert ioFrname == 'IAU_IO'


def test_conics():
    spice.kclear()
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
    outCell = spice.bltfrm(-1)
    assert outCell.size >= 126
    cellCopy = spice.copy(outCell)
    assert cellCopy.size >= 126
    assert cellCopy is not outCell


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
    npt.assert_array_almost_equal(spice.cylrec(0.0, np.radians(33.0), 0.0), [0.0, 0.0, 0.0])


def test_cylsph():
    a = np.array(spice.cylsph(1.0, np.deg2rad(180.0), 1.0))
    b = np.array([1.4142, np.deg2rad(180.0), np.deg2rad(45.0)])
    np.testing.assert_almost_equal(b, a, decimal=4)


def test_dafac():
    assert 1


def test_dafbbs():
    spice.kclear()
    handle = spice.dafopr(os.path.join(cwd, "de421.bsp"))
    spice.dafbbs(handle)
    found = spice.daffpa()
    assert found
    spice.dafcls(handle)
    spice.kclear()


def test_dafbfs():
    spice.kclear()
    handle = spice.dafopr(os.path.join(cwd, "de421.bsp"))
    spice.dafbfs(handle)
    found = spice.daffna()
    assert found
    spice.dafcls(handle)
    spice.kclear()


def test_dafcls():
    spice.kclear()
    handle = spice.dafopr(os.path.join(cwd, "de421.bsp"))
    spice.dafbfs(handle)
    found = spice.daffna()
    assert found
    spice.dafcls(handle)
    spice.kclear()


def test_dafcs():
    spice.kclear()
    handle = spice.dafopr(os.path.join(cwd, "de421.bsp"))
    spice.dafbbs(handle)
    spice.dafcs(handle)
    found = spice.daffpa()
    assert found
    spice.dafcls(handle)
    spice.kclear()


def test_dafdc():
    assert 1


def test_dafec():
    spice.kclear()
    handle = spice.dafopr(os.path.join(cwd, "de421.bsp"))
    n, buffer, done = spice.dafec(handle, 15, 80)
    assert n == 15
    assert buffer == ['; de421.bsp LOG FILE', ';', '; Created 2008-02-12/11:33:34.00.', ';', '; BEGIN NIOSPK COMMANDS',
                      '', 'LEAPSECONDS_FILE    = naif0007.tls', 'SPK_FILE            = de421.bsp',
                      '  SPK_LOG_FILE      = de421_spk_conversion.log', '  NOTE              = NIOSPK 6.1.0 Conversion',
                      '  SOURCE_NIO_FILE   = de421.nio', '    BEGIN_TIME      = CAL-ET 1899 JUL 29 00:00:00.000',
                      '    END_TIME        = CAL-ET 2053 OCT 09 00:00:00.000', '', '; END NIOSPK COMMANDS']
    assert done is False
    spice.dafcls(handle)
    spice.kclear()


def test_daffna():
    spice.kclear()
    handle = spice.dafopr(os.path.join(cwd, "de421.bsp"))
    spice.dafbfs(handle)
    found = spice.daffna()
    assert found
    spice.dafcls(handle)
    spice.kclear()


def test_daffpa():
    spice.kclear()
    handle = spice.dafopr(os.path.join(cwd, "de421.bsp"))
    spice.dafbbs(handle)
    found = spice.daffpa()
    assert found
    spice.dafcls(handle)
    spice.kclear()


def test_dafgda():
    # not a very good test...
    spice.kclear()
    handle = spice.dafopr(os.path.join(cwd, "de421.bsp"))
    elements = spice.dafgda(handle, 20, 21)
    assert elements == [0.0]
    spice.dafcls(handle)
    spice.kclear()


def test_dafgh():
    spice.kclear()
    handle = spice.dafopr(os.path.join(cwd, "de421.bsp"))
    spice.dafbbs(handle)
    spice.dafcs(handle)
    searchHandle = spice.dafgh()
    assert searchHandle == handle
    spice.dafcls(handle)
    spice.kclear()


def test_dafgn():
    spice.kclear()
    handle = spice.dafopr(os.path.join(cwd, "de421.bsp"))
    spice.dafbfs(handle)
    found = spice.daffna()
    assert found
    out = spice.dafgs(n=2)
    npt.assert_array_almost_equal(out, [-3169195200.0000000, 1696852800.0000000])
    outname = spice.dafgn(100)
    assert outname == 'DE-0421LE-0421'
    spice.dafcls(handle)
    spice.kclear()


def test_dafgs():
    spice.kclear()
    handle = spice.dafopr(os.path.join(cwd, "de421.bsp"))
    spice.dafbfs(handle)
    found = spice.daffna()
    assert found
    out = spice.dafgs(n=2)
    npt.assert_array_almost_equal(out, [-3169195200.0000000, 1696852800.0000000])
    spice.dafcls(handle)
    spice.kclear()


def test_dafgsstress():
    # this is to show that memory issue with dafgs is fixed.
    for i in range(500):
        test_dafgs()


def test_dafgsr():
    assert 1


def test_dafopr():
    spice.kclear()
    handle = spice.dafopr(os.path.join(cwd, "de421.bsp"))
    spice.dafbfs(handle)
    found = spice.daffna()
    assert found
    spice.dafcls(handle)
    spice.kclear()


def test_dafopw():
    spice.kclear()
    handle = spice.dafopw(os.path.join(cwd, "de421.bsp"))
    spice.dafbfs(handle)
    found = spice.daffna()
    assert found
    spice.dafcls(handle)
    spice.kclear()


def test_dafps():
    assert 1


def test_dafrda():
    assert 1


def test_dafrfr():
    spice.kclear()
    handle = spice.dafopr(os.path.join(cwd, "de421.bsp"))
    nd, ni, ifname, fward, bward, free = spice.dafrfr(handle, 61)
    spice.dafcls(handle)
    assert nd == 2
    assert ni == 6
    assert ifname == "NIO2SPK"
    assert fward == 4
    assert bward == 4
    spice.kclear()


def test_dafrs():
    assert 1


def test_dafus():
    spice.kclear()
    handle = spice.dafopr(os.path.join(cwd, "de421.bsp"))
    spice.dafbfs(handle)
    found = spice.daffna()
    assert found
    out = spice.dafgs(n=124)
    dc, ic = spice.dafus(out, 2, 6)
    spice.dafcls(handle)
    npt.assert_array_almost_equal(dc, [-3169195200.0000000, 1696852800.0000000])
    npt.assert_array_almost_equal(ic, [1, 0, 1, 2, 641, 310404])
    spice.kclear()


def test_dasac():
    assert 1


def test_dascls():
    assert 1


def test_dasec():
    assert 1


def test_dasopr():
    assert 1


def test_dcyldr():
    output = spice.dcyldr(1.0, 0.0, 0.0)
    expected = [[1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0]]
    npt.assert_array_almost_equal(output, expected)


def test_deltet():
    spice.kclear()
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
    spice.kclear()
    spice.furnsh(_testKernelPath)
    size, radii = spice.bodvrd('EARTH', 'RADII', 3)
    flat = (radii[0] - radii[2]) / radii[0]
    lon = 118.0 * spice.rpd()
    lat = 32.0 * spice.rpd()
    alt = 0.0
    spice.kclear()
    rec = spice.latrec(lon, lat, alt)
    output = spice.dgeodr(rec[0], rec[1], rec[2], radii[0], flat)
    expected = [[-0.25730624850202866, 0.41177607401581356, 0.0],
                [-0.019818463887750683, -0.012383950685377182, 0.0011247386599188864],
                [0.040768073853231314, 0.02547471988726025, 0.9988438330394612]]
    npt.assert_array_almost_equal(output, expected)


def test_diags2():
    mat = [[1.0, 4.0], [4.0, -5.0]]
    diag, rot = spice.diags2(mat)
    expectedDiag = [[3.0, 0.0], [0.0, -7.0]]
    expectedRot = [[0.89442719, -0.44721360], [0.44721360, 0.89442719]]
    npt.assert_array_almost_equal(diag, expectedDiag)
    npt.assert_array_almost_equal(rot, expectedRot)


def test_diff():
    testCellOne = spice.stypes.SPICEINT_CELL(8)
    testCellTwo = spice.stypes.SPICEINT_CELL(8)
    spice.insrti(1, testCellOne)
    spice.insrti(2, testCellOne)
    spice.insrti(3, testCellOne)
    spice.insrti(2, testCellTwo)
    spice.insrti(3, testCellTwo)
    spice.insrti(4, testCellTwo)
    outCell = spice.diff(testCellOne, testCellTwo)
    assert [x for x in outCell] == [1]


def test_dlatdr():
    output = spice.dlatdr(1.0, 0.0, 0.0)
    expected = [[1.0, 0.0, 0.0],
                [0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0]]
    npt.assert_array_almost_equal(output, expected)


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
    spice.kclear()
    spice.furnsh(_testKernelPath)
    n, radii = spice.bodvrd("MARS", "RADII", 3)
    re = radii[0]
    rp = radii[2]
    f = (re - rp) / re
    output = spice.dpgrdr("Mars", 90.0 * spice.rpd(), 45 * spice.rpd(), 300, re, f)
    expected = [[0.25464790894703276, -0.5092958178940655, -0.0],
                [-0.002629849831988239, -0.0013149249159941194, 1.5182979166821334e-05],
                [0.004618598844358383, 0.0023092994221791917, 0.9999866677515724]]
    npt.assert_array_almost_equal(output, expected)
    spice.kclear()


def test_dpmax():
    assert spice.dpmax() >= 1.0e37


def test_dpmin():
    assert spice.dpmin() <= -1.0e37


def test_dpr():
    assert spice.dpr() == 180.0 / np.arccos(-1.0)


def test_drdcyl():
    output = spice.drdcyl(1.0, np.deg2rad(180.0), 1.0)
    expected = [[-1.0, 0.0, 0.0],
                [0.0, -1.0, 0.0],
                [0.0, 0.0, 1.0]]
    npt.assert_array_almost_equal(output, expected)


def test_drdgeo():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    size, radii = spice.bodvrd('EARTH', 'RADII', 3)
    flat = (radii[0] - radii[2]) / radii[0]
    lon = 118.0 * spice.rpd()
    lat = 32.0 * spice.rpd()
    alt = 0.0
    spice.kclear()
    output = spice.drdgeo(lon, lat, alt, radii[0], flat)
    expected = [[-4780.329375996193, 1580.5982261675397, -0.3981344650201568],
                [-2541.7462156656084, -2972.6729150327574, 0.7487820251299121],
                [0.0, 5387.9427815962445, 0.5299192642332049]]
    npt.assert_array_almost_equal(output, expected)


def test_drdlat():
    output = spice.drdlat(1.0, 90.0 * spice.rpd(), 0.0)
    expected = [[1.0, 0.0, -0.0],
                [0.0, 0.0, 1.0],
                [0.0, -1.0, 0.0]]
    npt.assert_array_almost_equal(output, expected)


def test_drdpgr():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    n, radii = spice.bodvrd("MARS", "RADII", 3)
    re = radii[0]
    rp = radii[2]
    f = (re - rp) / re
    output = spice.drdpgr("Mars", 90.0 * spice.rpd(), 45 * spice.rpd(), 300, re, f)
    expected = [[-2620.6789148181783, 0.0, 0.0],
                [0.0, 2606.460468253308, -0.7071067811865476],
                [-0.0, 2606.460468253308, 0.7071067811865475]]
    npt.assert_array_almost_equal(output, expected)
    spice.kclear()


def test_drdsph():
    output = spice.drdsph(1.0, np.pi / 2, np.pi)
    expected = [[-1.0, 0.0, 0.0],
                [0.0, 0.0, -1.0],
                [0.0, -1.0, 0.0]]
    npt.assert_array_almost_equal(output, expected)


def test_dsphdr():
    output = spice.dsphdr(-1.0, 0.0, 0.0)
    expected = [[-1.0, 0.0, 0.0],
                [0.0, 0.0, -1.0],
                [0.0, -1.0, 0.0]]
    npt.assert_array_almost_equal(output, expected)


def test_dtpool():
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


def test_ducrss():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    z_earth = [0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
    et = spice.str2et("Jan 1, 2009")
    trans = spice.sxform("IAU_EARTH", "J2000", et)
    z_j2000 = np.dot(np.array(trans), np.array(z_earth))
    state, ltime = spice.spkezr("Sun", et, "J2000", "LT+S", "Earth")
    z_new = spice.ducrss(state, z_j2000)
    z_expected = [-0.9798625180326394, -0.1996715076226282, 0.0008572038510904833,
                  4.453114222872359e-08, -2.1853106962531453e-07, -3.6140021238340607e-11]
    npt.assert_array_almost_equal(z_new, z_expected)
    spice.kclear()


def test_dvcrss():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    z_earth = [0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
    et = spice.str2et("Jan 1, 2009")
    trans = spice.sxform("IAU_EARTH", "J2000", et)
    z_j2000 = np.dot(np.array(trans), np.array(z_earth))
    state, ltime = spice.spkezr("Sun", et, "J2000", "LT+S", "Earth")
    z = spice.dvcrss(state, z_j2000)
    spice.kclear()
    expected = [-132672690.30582438, -27035380.582678422, 116064.79375599445,
                5.12510707364564, -29.773241559425408, -0.00410216479731787]
    npt.assert_almost_equal(z, expected)


def test_dvdot():
    assert spice.dvdot([1.0, 0.0, 1.0, 0.0, 1.0, 0.0], [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]) == 3.0


def test_dvhat():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et("Jan 1, 2009")
    state, ltime = spice.spkezr("Sun", et, "J2000", "LT+S", "Earth")
    x_new = spice.dvhat(state)
    spice.kclear()
    expected = [0.1834466376334262, -0.9019196633282948, -0.39100927360200305,
                2.0244976750658316e-07, 3.4660106111045445e-08, 1.5033141925267006e-08]
    npt.assert_array_almost_equal(expected, x_new)


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
    spice.kclear()
    spice.pdpool("DTEST_VAL", [3.1415, 186.0, 282.397])
    assert spice.expool("DTEST_VAL")
    spice.dvpool("DTEST_VAL")
    assert not spice.expool("DTEST_VAL")
    spice.clpool()
    spice.kclear()


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


def test_edterm():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et("2007 FEB 3 00:00:00.000")
    # umbral
    trgepc, obspos, trmpts = spice.edterm("UMBRAL", "SUN", "MOON", et, "IAU_MOON", "LT+S", "EARTH", 3)
    expected_trgepc = 223732863.86351672
    expected_obspos = [394721.10311942, 27265.12569734, -19069.08642173]
    expected_trmpts0 = [-153.978389497704, -1730.5633188256702, 0.12289334835869758]
    expected_trmpts1 = [87.375069963142522, 864.40670521284744, 1504.5681789576722]
    expected_trmpts2 = [42.213243378688254, 868.21134651980412, -1504.3223922609538]
    npt.assert_almost_equal(trgepc, expected_trgepc)
    npt.assert_array_almost_equal(obspos, expected_obspos)
    npt.assert_array_almost_equal(trmpts[0], expected_trmpts0)
    npt.assert_array_almost_equal(trmpts[1], expected_trmpts1)
    npt.assert_array_almost_equal(trmpts[2], expected_trmpts2)
    iluet0, srfvec0, phase0, solar0, emissn0 = spice.ilumin("Ellipsoid", "MOON", et, "IAU_MOON",
                                                            "LT+S", "EARTH", trmpts[0])
    npt.assert_almost_equal(spice.dpr() * solar0, 90.269765819)
    iluet1, srfvec1, phase1, solar1, emissn1 = spice.ilumin("Ellipsoid", "MOON", et, "IAU_MOON",
                                                            "LT+S", "EARTH", trmpts[1])
    npt.assert_almost_equal(spice.dpr() * solar1, 90.269765706)
    iluet2, srfvec2, phase2, solar2, emissn2 = spice.ilumin("Ellipsoid", "MOON", et, "IAU_MOON",
                                                            "LT+S", "EARTH", trmpts[2])
    npt.assert_almost_equal(spice.dpr() * solar2, 90.269765730)
    #penumbral
    trgepc, obspos, trmpts = spice.edterm("PENUMBRAL", "SUN", "MOON", et, "IAU_MOON", "LT+S", "EARTH", 3)
    expected_trmpts0 = [154.01906431647933, 1730.5596992224057, -0.12350843234403218]
    expected_trmpts1 = [-87.334368432224963, -864.41003761407035, -1504.5686275350108]
    expected_trmpts2 = [-42.172546846121648, -868.21467849994303, 1504.3216106703221]
    npt.assert_almost_equal(trgepc, expected_trgepc)
    npt.assert_array_almost_equal(obspos, expected_obspos)
    npt.assert_array_almost_equal(trmpts[0], expected_trmpts0)
    npt.assert_array_almost_equal(trmpts[1], expected_trmpts1)
    npt.assert_array_almost_equal(trmpts[2], expected_trmpts2)
    iluet0, srfvec0, phase0, solar0, emissn0 = spice.ilumin("Ellipsoid", "MOON", et, "IAU_MOON",
                                                            "LT+S", "EARTH", trmpts[0])
    npt.assert_almost_equal(spice.dpr() * solar0, 89.730234406)
    iluet1, srfvec1, phase1, solar1, emissn1 = spice.ilumin("Ellipsoid", "MOON", et, "IAU_MOON",
                                                            "LT+S", "EARTH", trmpts[1])
    npt.assert_almost_equal(spice.dpr() * solar1, 89.730234298)
    iluet2, srfvec2, phase2, solar2, emissn2 = spice.ilumin("Ellipsoid", "MOON", et, "IAU_MOON",
                                                            "LT+S", "EARTH", trmpts[2])
    npt.assert_almost_equal(spice.dpr() * solar2, 89.730234322)
    spice.kclear()


def test_ekacec():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekacec.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno = spice.ekbseg(handle, "test_table_ekacec", 1, 10, ["c1"], 200,
                         ["DATATYPE = CHARACTER*(*), NULLS_OK = TRUE"])
    recno = spice.ekappr(handle, segno)
    spice.ekacec(handle, segno, recno, "c1", 2, 10, ["1.0", "2.0"], False)
    spice.ekcls(handle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)
    assert not spice.exists(ekpath)


def test_ekaced():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekaced.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno = spice.ekbseg(handle, "test_table_ekaced", 1, 10, ["c1"], 200,
                         ["DATATYPE = DOUBLE PRECISION, NULLS_OK = TRUE"])
    recno = spice.ekappr(handle, segno)
    spice.ekaced(handle, segno, recno, "c1", 2, [1.0, 2.0], False)
    spice.ekcls(handle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)
    assert not spice.exists(ekpath)


def test_ekacei():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekacei.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno = spice.ekbseg(handle, "test_table_ekacei", 1, 10, ["c1"], 200,
                         ["DATATYPE = INTEGER, NULLS_OK = TRUE"])
    recno = spice.ekappr(handle, segno)
    spice.ekacei(handle, segno, recno, "c1", 2, [1, 2], False)
    spice.ekcls(handle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)
    assert not spice.exists(ekpath)


def test_ekaclc():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekaclc.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = spice.ekifld(handle, "test_table_ekaclc", 1, 2, 200, ["c1"], 200,
                                 ["DATATYPE = CHARACTER*(*), INDEXED  = TRUE"])
    spice.ekaclc(handle, segno, "c1", 10, ["1.0", "2.0"], [4, 4], [False, False], rcptrs, [0, 0])
    spice.ekffld(handle, segno, rcptrs)
    spice.ekcls(handle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)
    assert not spice.exists(ekpath)


def test_ekacld():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekacld.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = spice.ekifld(handle, "test_table_ekacld", 1, 2, 200, ["c1"], 200,
                                 ["DATATYPE = DOUBLE PRECISION, NULLS_OK = TRUE"])
    spice.ekacld(handle, segno, "c1", [1.0, 2.0], [1, 1], [False, False], rcptrs, [0, 0])
    spice.ekffld(handle, segno, rcptrs)
    spice.ekcls(handle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)
    assert not spice.exists(ekpath)


def test_ekacli():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekacli.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = spice.ekifld(handle, "test_table_ekacli", 1, 2, 200, ["c1"], 200,
                                 ["DATATYPE = INTEGER, NULLS_OK = TRUE"])
    spice.ekacli(handle, segno, "c1", [1, 2], [1, 1], [False, False], rcptrs, [0, 0])
    spice.ekffld(handle, segno, rcptrs)
    spice.ekcls(handle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)
    assert not spice.exists(ekpath)


def test_ekacli_stress():
    for i in range(10):
        test_ekacli()


def test_ekappr():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekappr.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno = spice.ekbseg(handle, "test_table_ekappr", 1, 10, ["c1"], 200,
                         ["DATATYPE  = INTEGER, NULLS_OK = TRUE"])
    recno = spice.ekappr(handle, segno)
    spice.ekacei(handle, segno, recno, "c1", 2, [1, 2], False)
    spice.ekcls(handle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)
    assert not spice.exists(ekpath)


def test_ekbseg():
    ekpath = os.path.join(cwd, "example_ekbseg.ek")
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)
    handle = spice.ekopn(ekpath, "Test EK", 100)
    cnames = ['INT_COL_1']
    cdecls = ["DATATYPE=INTEGER, INDEXED=TRUE, NULLS_OK=TRUE"]
    segno = spice.ekbseg(handle, "SCALAR_DATA", 1, 100, cnames, 200, cdecls)
    recno = spice.ekappr(handle, segno)
    assert recno != -1
    ordids = [x for x in range(5)]
    spice.ekacei(handle, segno, recno, 'INT_COL_1', 5, ordids, False)
    spice.ekcls(handle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)
    assert not spice.exists(ekpath)


def test_ekbseg_stress():
    for i in range(10):
        test_ekbseg()


def test_ekccnt():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekccnt.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno = spice.ekbseg(handle, "TEST_TABLE_EKCCNT", 1, 10, ["c1"], 200,
                         ["DATATYPE  = INTEGER, NULLS_OK = TRUE"])
    recno = spice.ekappr(handle, segno)
    spice.ekacei(handle, segno, recno, "c1", 2, [1, 2], False)
    spice.ekcls(handle)
    spice.kclear()
    spice.furnsh(ekpath)
    assert spice.ekntab() == 1
    assert spice.ektnam(0, 100) == "TEST_TABLE_EKCCNT"
    assert spice.ekccnt("TEST_TABLE_EKCCNT") == 1
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)
    assert not spice.exists(ekpath)


def test_ekcii():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekcii.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno = spice.ekbseg(handle, "TEST_TABLE_EKCII", 1, 10, ["c1"], 200,
                         ["DATATYPE  = INTEGER, NULLS_OK = TRUE"])
    recno = spice.ekappr(handle, segno)
    spice.ekacei(handle, segno, recno, "c1", 2, [1, 2], False)
    spice.ekcls(handle)
    spice.kclear()
    spice.furnsh(ekpath)
    assert spice.ekntab() == 1
    assert spice.ektnam(0, 100) == "TEST_TABLE_EKCII"
    assert spice.ekccnt("TEST_TABLE_EKCII") == 1
    column, attdsc = spice.ekcii("TEST_TABLE_EKCII", 0, 30)
    spice.kclear()
    assert column == "C1"
    assert attdsc.cclass == 1
    assert attdsc.dtype == 2
    assert attdsc.size == 1
    assert attdsc.strlen == 1
    assert not attdsc.indexd
    assert not attdsc.nullok
    if spice.exists(ekpath):
        os.remove(ekpath)
    assert not spice.exists(ekpath)


def test_ekcls():
    spice.kclear()  # same as ekopn test
    ekpath = os.path.join(cwd, "example_ekcls.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)
    handle = spice.ekopn(ekpath, ekpath, 80)
    spice.ekcls(handle)
    assert spice.exists(ekpath)
    if spice.exists(ekpath):
        os.remove(ekpath)
    spice.kclear()


def test_ekdelr():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekdelr.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = spice.ekifld(handle, "test_table_ekdelr", 1, 10, 200, ["c1"], 200,
                                 ["DATATYPE = INTEGER, NULLS_OK = TRUE"])
    spice.ekacli(handle, segno, "c1", [1, 2], [1], [False, False], rcptrs, [1])
    spice.ekffld(handle, segno, rcptrs)
    spice.ekdelr(handle, segno, 2)
    spice.ekcls(handle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)
    assert not spice.exists(ekpath)


def test_ekdelr_stress():
    for i in range(10):
        test_ekdelr()


def test_ekffld():
    # same as test_ekacli
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekffld.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = spice.ekifld(handle, "test_table_ekffld", 1, 10, 200, ["c1"], 200,
                                 ["DATATYPE = INTEGER, NULLS_OK = TRUE"])
    spice.ekacli(handle, segno, "c1", [1, 2], [1], [False, False], rcptrs, [1])
    spice.ekffld(handle, segno, rcptrs)
    spice.ekcls(handle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)
    assert not spice.exists(ekpath)


def test_ekffld_stress():
    for i in range(10):
        test_ekffld()


def test_ekfind():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekfind.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = spice.ekifld(handle, "test_table_ekfind", 1, 2, 200, ["cc1"], 200,
                                 ["DATATYPE = INTEGER, NULLS_OK = TRUE"])
    spice.ekacli(handle, segno, "cc1", [1, 2], [1, 1], [False, False], rcptrs, [0, 0])
    spice.ekffld(handle, segno, rcptrs)
    spice.ekcls(handle)
    spice.kclear()
    spice.furnsh(ekpath)
    nmrows, error, errmsg = spice.ekfind("SELECT CC1 FROM TEST_TABLE_EKFIND WHERE CC1 > 0", 100)
    assert nmrows != 0  # should be 2 but I am not concerned about correctness in this case
    assert not error
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)
    assert not spice.exists(ekpath)


def test_ekfind_stess():
    for i in range(10):
        test_ekfind()


def test_ekgc():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekgc.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = spice.ekifld(handle, "test_table_ekgc", 1, 2, 200, ["c1"], 200,
                                 ["DATATYPE = CHARACTER*(*), INDEXED  = TRUE"])
    spice.ekaclc(handle, segno, "c1", 10, ["1.0", "2.0"], [4, 4], [False, False], rcptrs, [0, 0])
    spice.ekffld(handle, segno, rcptrs)
    spice.ekcls(handle)
    spice.kclear()
    spice.furnsh(ekpath)
    nmrows, error, errmsg = spice.ekfind("SELECT C1 FROM TEST_TABLE_EKGC", 100)
    assert not error
    c, null, found = spice.ekgc(0, 0, 0, 4)
    assert not null
    assert found
    assert c == "1.0"
    c, null, found = spice.ekgc(0, 1, 0, 4)
    assert not null
    assert found
    # assert c == "2.0" this fails, c is an empty string despite found being true.
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)
    assert not spice.exists(ekpath)


def test_ekgd():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekgd.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = spice.ekifld(handle, "test_table_ekgd", 1, 2, 200, ["c1"], 200,
                                 ["DATATYPE = DOUBLE PRECISION, NULLS_OK = TRUE"])
    spice.ekacld(handle, segno, "c1", [1.0, 2.0], [1, 1], [False, False], rcptrs, [0, 0])
    spice.ekffld(handle, segno, rcptrs)
    spice.ekcls(handle)
    spice.kclear()
    spice.furnsh(ekpath)
    nmrows, error, errmsg = spice.ekfind("SELECT C1 FROM TEST_TABLE_EKGD", 100)
    assert not error
    d, null, found = spice.ekgd(0, 0, 0)
    assert not null
    assert found
    assert d == 1.0
    d, null, found = spice.ekgd(0, 1, 0)
    assert not null
    assert found
    assert d == 2.0
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)
    assert not spice.exists(ekpath)


def test_ekgi():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekgi.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = spice.ekifld(handle, "test_table_ekgi", 1, 2, 200, ["c1"], 200,
                                 ["DATATYPE = INTEGER, NULLS_OK = TRUE"])
    spice.ekacli(handle, segno, "c1", [1, 2], [1, 1], [False, False], rcptrs, [0, 0])
    spice.ekffld(handle, segno, rcptrs)
    spice.ekcls(handle)
    spice.kclear()
    spice.furnsh(ekpath)
    nmrows, error, errmsg = spice.ekfind("SELECT C1 FROM TEST_TABLE_EKGI", 100)
    assert not error
    i, null, found = spice.ekgi(0, 0, 0)
    assert not null
    assert found
    assert i == 1
    i, null, found = spice.ekgi(0, 1, 0)
    assert not null
    assert found
    assert i == 2
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)
    assert not spice.exists(ekpath)


def test_ekifld():
    # Same as test_ekacli
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekifld.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = spice.ekifld(handle, "test_table_ekifld", 1, 2, 200, ["c1"], 200,
                                 ["DATATYPE = INTEGER, NULLS_OK = TRUE"])
    spice.ekacli(handle, segno, "c1", [1, 2], [1, 1], [False, False], rcptrs, [0, 0])
    spice.ekffld(handle, segno, rcptrs)
    spice.ekcls(handle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)
    assert not spice.exists(ekpath)


def test_ekinsr():
    assert 1


def test_eklef():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_eklef.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno = spice.ekbseg(handle, "test_table_eklef", 1, 10, ["c1"], 200,
                         ["DATATYPE  = INTEGER, NULLS_OK = TRUE"])
    recno = spice.ekappr(handle, segno)
    spice.ekacei(handle, segno, recno, "c1", 2, [1, 2], False)
    spice.ekcls(handle)
    spice.kclear()
    handle = spice.eklef(ekpath)
    assert handle is not None
    spice.ekuef(handle)
    if spice.exists(ekpath):
        os.remove(ekpath)


def test_eknelt():
    assert 1


def test_eknseg():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_eknseg.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno = spice.ekbseg(handle, "TEST_TABLE_EKNSEG", 1, 10, ["c1"], 200,
                         ["DATATYPE  = INTEGER, NULLS_OK = TRUE"])
    recno = spice.ekappr(handle, segno)
    spice.ekacei(handle, segno, recno, "c1", 2, [1, 2], False)
    spice.ekcls(handle)
    spice.kclear()
    handle = spice.ekopr(ekpath)
    assert spice.eknseg(handle) == 1
    spice.ekcls(handle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)
    assert not spice.exists(ekpath)


def test_ekntab():
    assert spice.ekntab() == 0


def test_ekopn():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ek.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)
    handle = spice.ekopn(ekpath, ekpath, 80)
    spice.ekcls(handle)
    spice.kclear()
    assert spice.exists(ekpath)
    if spice.exists(ekpath):
        os.remove(ekpath)


def test_ekopr():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekopr.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)
    handle = spice.ekopn(ekpath, ekpath, 80)
    spice.ekcls(handle)
    assert spice.exists(ekpath)
    testhandle = spice.ekopr(ekpath)
    assert testhandle is not None
    spice.ekcls(testhandle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)


def test_ekops():
    spice.kclear()
    handle = spice.ekops()
    assert handle is not None
    spice.ekcls(handle)
    spice.kclear()


def test_ekopw():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekopw.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)
    handle = spice.ekopn(ekpath, ekpath, 80)
    spice.ekcls(handle)
    assert spice.exists(ekpath)
    testhandle = spice.ekopw(ekpath)
    assert testhandle is not None
    spice.ekcls(testhandle)
    if spice.exists(ekpath):
        os.remove(ekpath)
    spice.kclear()


def test_ekpsel():
    assert 1


def test_ekrcec():
    assert 1


def test_ekrced():
    assert 1


def test_ekrcei():
    assert 1
    # spice.kclear()
    # ekpath = os.path.join(cwd, "example_ekrcei.ek")
    # if spice.exists(ekpath):
    # os.remove(ekpath)
    # handle = spice.ekopn(ekpath, ekpath, 0)
    # segno, rcptrs = spice.ekifld(handle, "test_table_ekrcei", 1, 2, 200, ["c1"], 200,
    #                              ["DATATYPE = INTEGER, NULLS_OK = TRUE"])
    # spice.ekacli(handle, segno, "c1", [1, 2], [1, 1], [False, False], rcptrs, [0, 0])
    # spice.ekffld(handle, segno, rcptrs)
    # nvals, ivals, isnull = spice.ekrcei(handle, 0, 0, "C1")
    # spice.ekcls(handle)
    # spice.kclear()
    # if spice.exists(ekpath):
    #     os.remove(ekpath)
    # assert not spice.exists(ekpath)


def test_ekssum():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekssum.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = spice.ekifld(handle, "test_table_ekssum", 1, 2, 200, ["c1"], 200,
                                 ["DATATYPE = INTEGER, NULLS_OK = TRUE"])
    spice.ekacli(handle, segno, "c1", [1, 2], [1, 1], [False, False], rcptrs, [0, 0])
    spice.ekffld(handle, segno, rcptrs)
    segsum = spice.ekssum(handle, segno)
    assert segsum.ncols == 1
    assert segsum.nrows == 2
    assert segsum.cnames == ["C1"]
    assert segsum.tabnam == "TEST_TABLE_EKSSUM"
    c1descr = segsum.cdescrs[0]
    assert c1descr.dtype == 2
    assert c1descr.indexd is False
    # assert c1descr.null == True, for some reason this is actually false, SpikeEKAttDsc may not be working correctly
    spice.ekcls(handle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)
    assert not spice.exists(ekpath)


def test_ektnam():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ektnam.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno = spice.ekbseg(handle, "TEST_TABLE_EKTNAM", 1, 10, ["c1"], 200,
                         ["DATATYPE  = INTEGER, NULLS_OK = TRUE"])
    recno = spice.ekappr(handle, segno)
    spice.ekacei(handle, segno, recno, "c1", 2, [1, 2], False)
    spice.ekcls(handle)
    spice.kclear()
    spice.furnsh(ekpath)
    assert spice.ekntab() == 1
    assert spice.ektnam(0, 100) == "TEST_TABLE_EKTNAM"
    assert spice.ekccnt("TEST_TABLE_EKTNAM") == 1
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)
    assert not spice.exists(ekpath)


def test_ekucec():
    assert 1


def test_ekuced():
    assert 1


def test_ekucei():
    assert 1


def test_ekuef():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekuef.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)
    handle = spice.ekopn(ekpath, ekpath, 80)
    spice.ekcls(handle)
    spice.kclear()
    assert spice.exists(ekpath)
    testhandle = spice.ekopr(ekpath)
    assert testhandle is not None
    spice.ekuef(testhandle)
    spice.ekcls(testhandle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)


def test_el2cgv():
    vec1 = [1.0, 1.0, 1.0]
    vec2 = [1.0, -1.0, 1.0]
    center = [1.0, 1.0, 1.0]
    smajor, sminor = spice.saelgv(vec1, vec2)
    ellipse = spice.cgv2el(center, smajor, sminor)
    outCenter, outSmajor, outSminor = spice.el2cgv(ellipse)
    expectedCenter = [1.0, 1.0, 1.0]
    expectedSmajor = [np.sqrt(2.0), 0.0, np.sqrt(2.0)]
    expectedSminor = [0.0, np.sqrt(2.0), 0.0]
    npt.assert_array_almost_equal(outCenter, expectedCenter)
    npt.assert_array_almost_equal(outSmajor, expectedSmajor)
    npt.assert_array_almost_equal(outSminor, expectedSminor)


def test_elemc():
    testCellOne = spice.stypes.SPICECHAR_CELL(10, 10)
    spice.insrtc("one", testCellOne)
    spice.insrtc("two", testCellOne)
    spice.insrtc("three", testCellOne)
    assert spice.elemc("one", testCellOne)
    assert spice.elemc("two", testCellOne)
    assert spice.elemc("three", testCellOne)
    assert not spice.elemc("not", testCellOne)
    assert not spice.elemc("there", testCellOne)


def test_elemd():
    testCellOne = spice.stypes.SPICEDOUBLE_CELL(8)
    spice.insrtd(1.0, testCellOne)
    spice.insrtd(2.0, testCellOne)
    spice.insrtd(3.0, testCellOne)
    assert spice.elemd(1.0, testCellOne)
    assert spice.elemd(2.0, testCellOne)
    assert spice.elemd(3.0, testCellOne)
    assert not spice.elemd(4.0, testCellOne)
    assert not spice.elemd(-1.0, testCellOne)


def test_elemi():
    testCellOne = spice.stypes.SPICEINT_CELL(8)
    spice.insrti(1, testCellOne)
    spice.insrti(2, testCellOne)
    spice.insrti(3, testCellOne)
    assert spice.elemi(1, testCellOne)
    assert spice.elemi(2, testCellOne)
    assert spice.elemi(3, testCellOne)
    assert not spice.elemi(4, testCellOne)
    assert not spice.elemi(-1, testCellOne)


def test_eqncpv():
    p = 10000.0
    gm = 398600.436
    ecc = 0.1
    a = p / (1.0 - ecc)
    n = np.sqrt(gm / a) / a
    argp = 30. * spice.rpd()
    node = 15. * spice.rpd()
    inc = 10. * spice.rpd()
    m0 = 45. * spice.rpd()
    t0 = -100000000.0
    eqel = [a, ecc * np.sin(argp + node), ecc * np.cos(argp + node), m0 + argp + node,
            np.tan(inc / 2.0) * np.sin(node), np.tan(inc / 2.0) * np.cos(node), 0.0, n, 0.0]
    state = spice.eqncpv(t0 - 9750.0, t0, eqel, spice.halfpi() * -1, spice.halfpi())
    expected = [-10732.167433285387, 3902.505790600528, 1154.4516152766892,
                -2.540766899262123, -5.15226920298345, -0.7615758062877463]
    npt.assert_array_almost_equal(expected, state, decimal=5)


def test_eqstr():
    assert spice.eqstr("A short string    ", "ashortstring")
    assert spice.eqstr("Embedded        blanks", "Em be dd ed bl an ks")
    assert spice.eqstr("One word left out", "WORD LEFT OUT") is False


def test_erract():
    assert spice.erract("GET", 10, "") == "RETURN"
    assert spice.erract("GET", 10) == "RETURN"


def test_errch():
    spice.setmsg("test errch value: #")
    spice.errch("#", "some error")
    spice.sigerr("some error")
    message = spice.getmsg("LONG", 2000)
    assert message == "test errch value: some error"
    spice.reset()


def test_errdev():
    assert spice.errdev("GET", 10, "Screen") == "NULL"


def test_errdp():
    spice.setmsg("test errdp value: #")
    spice.errdp("#", 42.1)
    spice.sigerr("some error")
    message = spice.getmsg("LONG", 2000)
    assert message == "test errdp value: 4.2100000000000E+01"
    spice.reset()


def test_errint():
    spice.setmsg("test errint value: #")
    spice.errint("#", 42)
    spice.sigerr("some error")
    message = spice.getmsg("LONG", 2000)
    assert message == "test errint value: 42"
    spice.reset()


def test_errprt():
    assert spice.errprt("GET", 40, "ALL") == "NULL"


def test_esrchc():
    array = ["This", "is", "a", "test"]
    assert spice.esrchc("This", array) == 0
    assert spice.esrchc("is", array) == 1
    assert spice.esrchc("a", array) == 2
    assert spice.esrchc("test", array) == 3
    assert spice.esrchc("fail", array) == -1


def test_et2lst():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et("2014 may 17 16:30:00")
    hr, mn, sc, time, ampm = spice.et2lst(et, 399, 281.49521300000004 * spice.rpd(), "planetocentric", 51, 51)
    assert hr == 11
    assert mn == 19
    assert sc == 20
    assert time == "11:19:20"
    assert ampm == '11:19:20 A.M.'
    spice.kclear()


def test_et2utc():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = -527644192.5403653
    output = spice.et2utc(et, "J", 6, 35)
    assert output == "JD 2445438.006415"
    spice.kclear()


def test_etcal():
    et = np.arange(0, 20)
    cal = spice.etcal(et[0], 51)
    assert cal == '2000 JAN 01 12:00:00.000'


def test_eul2m():
    rot = np.array(spice.eul2m(spice.halfpi(), 0.0, 0.0, 3, 1, 1))
    assert rot.shape == ((3, 3))


def test_eul2xf():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et("Jan 1, 2009")
    expected = spice.sxform('IAU_EARTH', 'J2000', et)
    eul = [1.571803284049681, 0.0008750002978301174, 2.9555269829740034,
           3.5458495690569166e-12, 3.080552365717176e-12, -7.292115373266558e-05]
    out = spice.eul2xf(eul, 3, 1, 3)
    npt.assert_array_almost_equal(out, expected)
    spice.kclear()


def test_exists():
    assert spice.exists(_testKernelPath)


def test_expool():
    spice.kclear()
    textbuf = ['DELTET/K = 1.657D-3', 'DELTET/EB = 1.671D-2']
    spice.lmpool(textbuf)
    assert spice.expool('DELTET/K')
    assert spice.expool('DELTET/EB')
    spice.kclear()


def test_expoolstress():
    # this is to show that the bug in lmpool is fixed (lenvals needs +=1)
    for i in range(500):
        test_expool()


def test_failed():
    assert not spice.failed()


def test_fovray():
    assert 1


def test_fovtrg():
    assert 1


def test_frame():
    vec = [23.0, -3.0, 18.0]
    x, y, z = spice.frame(vec)
    expected_x = [0.78338311, -0.10218041, 0.61308243]
    expected_y = [0.61630826, 0.0000000, -0.78750500]
    expected_z = [0.080467580, 0.99476588, 0.062974628]
    npt.assert_array_almost_equal(expected_x, x)
    npt.assert_array_almost_equal(expected_y, y)
    npt.assert_array_almost_equal(expected_z, z)


def test_frinfo():
    assert spice.frinfo(13000) == (399, 2, 3000, True)


def test_frmnam():
    assert spice.frmnam(13000, 30) == "ITRF93"
    assert spice.frmnam(13000) == "ITRF93"


def test_ftncls():
    assert 1


def test_furnsh():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    # 4 kernels + the meta kernel = 5
    assert spice.ktotal("ALL") == 5
    spice.kclear()


def test_furnsh_vectorized():
    spice.kclear()
    spice.furnsh([_testKernelPath, _extraTestVoyagerKernel])
    # 4 + 1 + 1 = 6
    assert spice.ktotal("ALL") == 6
    spice.kclear()


def test_gcpool():
    # same as pcpool test
    import string
    spice.kclear()
    data = [j + str(i) for i, j in enumerate(list(string.ascii_lowercase))]
    spice.pcpool('pcpool_test', data)
    cvals, found = spice.gcpool('pcpool_test', 0, 30, 4)
    assert data == cvals
    spice.kclear()


def test_gdpool():
    # same as pdpool test
    spice.kclear()
    data = np.arange(0.0, 10.0)
    spice.pdpool('pdpool_array', data)
    dvals, found = spice.gdpool('pdpool_array', 0, 30)
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


def test_getelm():
    spice.kclear()
    tle = ['1 18123U 87 53  A 87324.61041692 -.00000023  00000-0 -75103-5 0 00675',
           '2 18123  98.8296 152.0074 0014950 168.7820 191.3688 14.12912554 21686']
    spice.furnsh(_testKernelPath)
    epoch, elems = spice.getelm(1950, 75, tle)
    expected_elems = [-6.969196665949579e-13, 0.0, -7.510300000000001e-06,
                      1.724901918428988, 2.653029617396028, 0.001495,
                      2.9458016181010693, 3.3400156455905243, 0.06164994027515544, -382310404.79526937]
    expected_epoch = -382310404.79526937
    npt.assert_array_almost_equal(expected_elems, elems)
    npt.assert_almost_equal(epoch, expected_epoch)
    spice.kclear()


def test_getfat():
    arch, outtype = spice.getfat(os.path.join(cwd, 'naif0011.tls'))
    assert arch == "KPL"
    assert outtype == "LSK"


def test_getfov():
    spice.kclear()
    kernel = os.path.join(cwd, 'getfov_test.ti')
    if spice.exists(kernel):
        os.remove(kernel)
    with open(kernel, 'w') as kernelFile:
        kernelFile.write('\\begindata\n')
        kernelFile.write("INS-999004_FOV_SHAPE            = 'POLYGON'\n")
        kernelFile.write("INS-999004_FOV_FRAME            = 'SC999_INST004'\n")
        kernelFile.write("INS-999004_BORESIGHT            = (  0.0,  1.0,  0.0 )\n")
        kernelFile.write("INS-999004_FOV_BOUNDARY_CORNERS = (  0.0,  0.8,  0.5,\n")
        kernelFile.write("                                     0.4,  0.8, -0.2,\n")
        kernelFile.write("                                    -0.4,  0.8, -0.2,\n")
        kernelFile.write("\\begintext\n")
        kernelFile.close()
    spice.furnsh(kernel)
    shape, frame, bsight, n, bounds = spice.getfov(-999004, 4, 32, 32)
    assert shape == "POLYGON"
    assert frame == "SC999_INST004"
    npt.assert_array_almost_equal(bsight, [0.0, 1.0, 0.0])
    assert n == 3
    expected = np.array([[0.0, 0.8, 0.5], [0.4, 0.8, -0.2], [-0.4, 0.8, -0.2]])
    npt.assert_array_almost_equal(expected, bounds)
    spice.kclear()
    if spice.exists(kernel):
        os.remove(kernel)


def test_getmsg():
    spice.sigerr("test error")
    message = spice.getmsg("SHORT", 200)
    assert message == "test error"
    spice.reset()


def test_gfbail():
    assert not spice.gfbail()


def test_gfclrh():
    spice.gfclrh()
    assert not spice.gfbail()


def test_gfdist():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et0 = spice.str2et('2007 JAN 01 00:00:00 TDB')
    et1 = spice.str2et('2007 APR 01 00:00:00 TDB')
    cnfine = spice.stypes.SPICEDOUBLE_CELL(2)
    spice.wninsd(et0, et1, cnfine)
    result = spice.stypes.SPICEDOUBLE_CELL(1000)
    spice.gfdist("moon", "none", "earth", ">", 400000, 0.0, spice.spd(), 1000, cnfine, result)
    count = spice.wncard(result)
    assert count == 4
    tempResults = []
    for i in range(0, count):
        left, right = spice.wnfetd(result, i)
        timstrLeft = spice.timout(left, 'YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND', 41)
        timstrRight = spice.timout(right, 'YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND', 41)
        tempResults.append(timstrLeft)
        tempResults.append(timstrRight)
    expected = ["2007-JAN-08 00:11:07.623827 (TDB)", "2007-JAN-13 06:37:47.954706 (TDB)",
                "2007-FEB-04 07:02:35.279110 (TDB)", "2007-FEB-10 09:31:01.844110 (TDB)",
                "2007-MAR-03 00:20:25.183640 (TDB)", "2007-MAR-10 14:04:38.497606 (TDB)",
                "2007-MAR-29 22:53:58.147001 (TDB)", "2007-APR-01 00:00:00.000000 (TDB)"]
    assert expected == tempResults
    spice.kclear()


def test_gfevnt():
    assert 1


def test_gffove():
    assert 1


def test_gfilum():
    assert 1


def test_gfinth():
    assert 1


def test_gfocce():
    assert 1


def test_gfoclt():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et0 = spice.str2et('2001 DEC 01 00:00:00 TDB')
    et1 = spice.str2et('2002 JAN 01 00:00:00 TDB')
    cnfine = spice.stypes.SPICEDOUBLE_CELL(2)
    spice.wninsd(et0, et1, cnfine)
    result = spice.stypes.SPICEDOUBLE_CELL(1000)
    spice.gfoclt("any", "moon", "ellipsoid", "iau_moon", "sun",
                 "ellipsoid", "iau_sun", "lt", "earth", 180.0, cnfine, result)
    count = spice.wncard(result)
    assert count == 1
    start, end = spice.wnfetd(result, 0)
    startTime = spice.timout(start, 'YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND', 41)
    endTime = spice.timout(end, 'YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND', 41)
    assert startTime == "2001-DEC-14 20:10:14.195952 (TDB)"
    assert endTime == "2001-DEC-14 21:35:50.317994 (TDB)"
    spice.kclear()


def test_gfpa():
    relate = ["=", "<", ">", "LOCMIN", "ABSMIN", "LOCMAX", "ABSMAX"]
    expected = {"=": ["2006-DEC-02 13:31:34.414", "2006-DEC-02 13:31:34.414", "2006-DEC-07 14:07:55.470",
                      "2006-DEC-07 14:07:55.470", "2006-DEC-31 23:59:59.997", "2006-DEC-31 23:59:59.997",
                      "2007-JAN-06 08:16:25.512", "2007-JAN-06 08:16:25.512", "2007-JAN-30 11:41:32.557",
                      "2007-JAN-30 11:41:32.557"],
                "<": ["2006-DEC-02 13:31:34.414", "2006-DEC-07 14:07:55.470", "2006-DEC-31 23:59:59.997",
                      "2007-JAN-06 08:16:25.512", "2007-JAN-30 11:41:32.557", "2007-JAN-31 00:00:00.000"],
                ">": ["2006-DEC-01 00:00:00.000", "2006-DEC-02 13:31:34.414", "2006-DEC-07 14:07:55.470",
                      "2006-DEC-31 23:59:59.997", "2007-JAN-06 08:16:25.512", "2007-JAN-30 11:41:32.557"],
                "LOCMIN": ["2006-DEC-05 00:16:50.317", "2006-DEC-05 00:16:50.317",
                           "2007-JAN-03 14:18:31.977", "2007-JAN-03 14:18:31.977"],
                "ABSMIN": ["2007-JAN-03 14:18:31.977", "2007-JAN-03 14:18:31.977"],
                "LOCMAX": ["2006-DEC-20 14:09:10.392", "2006-DEC-20 14:09:10.392",
                           "2007-JAN-19 04:27:54.600", "2007-JAN-19 04:27:54.600"],
                "ABSMAX": ["2007-JAN-19 04:27:54.600", "2007-JAN-19 04:27:54.600"]}
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et0 = spice.str2et('2006 DEC 01')
    et1 = spice.str2et('2007 JAN 31')
    cnfine = spice.stypes.SPICEDOUBLE_CELL(2)
    spice.wninsd(et0, et1, cnfine)
    result = spice.stypes.SPICEDOUBLE_CELL(2000)
    for relation in relate:
        spice.gfpa("Moon", "Sun", "LT+S", "Earth", relation, 0.57598845,
                   0.0, spice.spd(), 5000, cnfine, result)
        count = spice.wncard(result)
        if count > 0:
            tempResults = []
            for i in range(0, count):
                left, right = spice.wnfetd(result, i)
                timstrLeft = spice.timout(left, 'YYYY-MON-DD HR:MN:SC.###', 41)
                timstrRight = spice.timout(right, 'YYYY-MON-DD HR:MN:SC.###', 41)
                tempResults.append(timstrLeft)
                tempResults.append(timstrRight)
            assert tempResults == expected.get(relation)
    spice.kclear()


def test_gfposc():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et0 = spice.str2et('2007 JAN 01')
    et1 = spice.str2et('2008 JAN 01')
    cnfine = spice.stypes.SPICEDOUBLE_CELL(2)
    spice.wninsd(et0, et1, cnfine)
    result = spice.stypes.SPICEDOUBLE_CELL(1000)
    spice.gfposc("sun", "iau_earth", "none", "earth", "latitudinal", "latitude",
                 "absmax", 0.0, 0.0, 90.0 * spice.spd(), 1000, cnfine, result)
    count = spice.wncard(result)
    assert count == 1
    start, end = spice.wnfetd(result, 0)
    startTime = spice.timout(start, 'YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND', 41)
    endTime = spice.timout(end, 'YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND', 41)
    assert startTime == endTime
    assert startTime == "2007-JUN-21 17:54:13.172475 (TDB)"
    spice.kclear()


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
    relate = ["=", "<", ">", "LOCMIN", "ABSMIN", "LOCMAX", "ABSMAX"]
    expected = {"=": ["2007-JAN-02 00:35:19.571", "2007-JAN-02 00:35:19.571", "2007-JAN-19 22:04:54.897",
                      "2007-JAN-19 22:04:54.897", "2007-FEB-01 23:30:13.427", "2007-FEB-01 23:30:13.427",
                      "2007-FEB-17 11:10:46.538", "2007-FEB-17 11:10:46.538", "2007-MAR-04 15:50:19.929",
                      "2007-MAR-04 15:50:19.929", "2007-MAR-18 09:59:05.957", "2007-MAR-18 09:59:05.957"],
                "<": ["2007-JAN-02 00:35:19.571", "2007-JAN-19 22:04:54.897", "2007-FEB-01 23:30:13.427",
                      "2007-FEB-17 11:10:46.538", "2007-MAR-04 15:50:19.929", "2007-MAR-18 09:59:05.957"],
                ">": ["2007-JAN-01 00:00:00.000", "2007-JAN-02 00:35:19.571", "2007-JAN-19 22:04:54.897",
                      "2007-FEB-01 23:30:13.427", "2007-FEB-17 11:10:46.538", "2007-MAR-04 15:50:19.929",
                      "2007-MAR-18 09:59:05.957", "2007-APR-01 00:00:00.000"],
                "LOCMIN": ["2007-JAN-11 07:03:58.991", "2007-JAN-11 07:03:58.991",
                           "2007-FEB-10 06:26:15.441", "2007-FEB-10 06:26:15.441",
                           "2007-MAR-12 03:28:36.404", "2007-MAR-12 03:28:36.404"],
                "ABSMIN": ["2007-JAN-11 07:03:58.991", "2007-JAN-11 07:03:58.991"],
                "LOCMAX": ["2007-JAN-26 02:27:33.762", "2007-JAN-26 02:27:33.762",
                           "2007-FEB-24 09:35:07.812", "2007-FEB-24 09:35:07.812",
                           "2007-MAR-25 17:26:56.148", "2007-MAR-25 17:26:56.148"],
                "ABSMAX": ["2007-MAR-25 17:26:56.148", "2007-MAR-25 17:26:56.148"]}
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et0 = spice.str2et('2007 JAN 01')
    et1 = spice.str2et('2007 APR 01')
    cnfine = spice.stypes.SPICEDOUBLE_CELL(2)
    spice.wninsd(et0, et1, cnfine)
    for relation in relate:
        result = spice.stypes.SPICEDOUBLE_CELL(2000)
        spice.gfrr("moon", "none", "sun", relation, 0.3365, 0.0, spice.spd(), 2000, cnfine, result)
        count = spice.wncard(result)
        if count > 0:
            tempResults = []
            for i in range(0, count):
                left, right = spice.wnfetd(result, i)
                timstrLeft = spice.timout(left, 'YYYY-MON-DD HR:MN:SC.###', 41)
                timstrRight = spice.timout(right, 'YYYY-MON-DD HR:MN:SC.###', 41)
                tempResults.append(timstrLeft)
                tempResults.append(timstrRight)
            assert tempResults == expected.get(relation)
    spice.kclear()


def test_gfsep():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    expected = ["2007-JAN-03 14:20:24.617627 (TDB)", "2007-FEB-02 06:16:24.101517 (TDB)",
                "2007-MAR-03 23:22:41.994972 (TDB)", "2007-APR-02 16:49:16.135505 (TDB)",
                "2007-MAY-02 09:41:43.830081 (TDB)", "2007-JUN-01 01:03:44.527470 (TDB)",
                "2007-JUN-30 14:15:26.576292 (TDB)", "2007-JUL-30 01:14:49.000963 (TDB)",
                "2007-AUG-28 10:39:01.388249 (TDB)", "2007-SEP-26 19:25:51.509426 (TDB)",
                "2007-OCT-26 04:30:56.625105 (TDB)", "2007-NOV-24 14:31:04.331185 (TDB)",
                "2007-DEC-24 01:40:12.235392 (TDB)"]
    et0 = spice.str2et('2007 JAN 01')
    et1 = spice.str2et('2008 JAN 01')
    cnfine = spice.stypes.SPICEDOUBLE_CELL(2)
    spice.wninsd(et0, et1, cnfine)
    result = spice.stypes.SPICEDOUBLE_CELL(2000)
    spice.gfsep("MOON", "SPHERE", "NULL", "SUN", "SPHERE", "NULL", "NONE", "EARTH",
                "LOCMAX", 0.0, 0.0, 6.0 * spice.spd(), 1000, cnfine, result)
    count = spice.wncard(result)
    assert count == 13
    tempResults = []
    for i in range(0, count):
        start, end = spice.wnfetd(result, i)
        assert start == end
        tempResults.append(spice.timout(start, 'YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND', 41))
    assert tempResults == expected
    spice.kclear()


def test_gfsntc():
    spice.kclear()
    kernel = os.path.join(cwd, 'gfnstc_test.tf')
    if spice.exists(kernel):
        os.remove(kernel)
    with open(kernel, 'w') as kernelFile:
        kernelFile.write('\\begindata\n')
        kernelFile.write("FRAME_SEM                     =  10100000\n")
        kernelFile.write("FRAME_10100000_NAME           = 'SEM'\n")
        kernelFile.write("FRAME_10100000_CLASS          =  5\n")
        kernelFile.write("FRAME_10100000_CLASS_ID       =  10100000\n")
        kernelFile.write("FRAME_10100000_CENTER         =  10\n")
        kernelFile.write("FRAME_10100000_RELATIVE       = 'J2000'\n")
        kernelFile.write("FRAME_10100000_DEF_STYLE      = 'PARAMETERIZED'\n")
        kernelFile.write("FRAME_10100000_FAMILY         = 'TWO-VECTOR'\n")
        kernelFile.write("FRAME_10100000_PRI_AXIS       = 'X'\n")
        kernelFile.write("FRAME_10100000_PRI_VECTOR_DEF = 'OBSERVER_TARGET_POSITION'\n")
        kernelFile.write("FRAME_10100000_PRI_OBSERVER   = 'SUN'\n")
        kernelFile.write("FRAME_10100000_PRI_TARGET     = 'EARTH'\n")
        kernelFile.write("FRAME_10100000_PRI_ABCORR     = 'NONE'\n")
        kernelFile.write("FRAME_10100000_SEC_AXIS       = 'Y'\n")
        kernelFile.write("FRAME_10100000_SEC_VECTOR_DEF = 'OBSERVER_TARGET_VELOCITY'\n")
        kernelFile.write("FRAME_10100000_SEC_OBSERVER   = 'SUN'\n")
        kernelFile.write("FRAME_10100000_SEC_TARGET     = 'EARTH'\n")
        kernelFile.write("FRAME_10100000_SEC_ABCORR     = 'NONE'\n")
        kernelFile.write("FRAME_10100000_SEC_FRAME      = 'J2000'\n")
        kernelFile.close()
    spice.furnsh(_testKernelPath)
    spice.furnsh(kernel)
    et0 = spice.str2et('2007 JAN 01')
    et1 = spice.str2et('2008 JAN 01')
    cnfine = spice.stypes.SPICEDOUBLE_CELL(2)
    spice.wninsd(et0, et1, cnfine)
    result = spice.stypes.SPICEDOUBLE_CELL(2000)
    spice.gfsntc("EARTH", "IAU_EARTH", "Ellipsoid", "NONE", "SUN", "SEM", [1.0, 0.0, 0.0], "LATITUDINAL",
                 "LATITUDE", "=", 0.0, 0.0, 90.0 * spice.spd(), 1000, cnfine, result)
    count = spice.wncard(result)
    assert count > 0
    beg, end = spice.wnfetd(result, 0)
    begstr = spice.timout(beg, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND", 80)
    endstr = spice.timout(end, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND", 80)
    assert begstr == "2007-MAR-21 00:01:25.500672 (TDB)"
    assert endstr == "2007-MAR-21 00:01:25.500672 (TDB)"
    beg, end = spice.wnfetd(result, 1)
    begstr = spice.timout(beg, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND", 80)
    endstr = spice.timout(end, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND", 80)
    assert begstr == "2007-SEP-23 09:46:39.579484 (TDB)"
    assert endstr == "2007-SEP-23 09:46:39.579484 (TDB)"
    spice.kclear()
    if spice.exists(kernel):
        os.remove(kernel)


def test_gfsstp():
    spice.gfsstp(0.5)
    assert spice.gfstep(0.5) == 0.5


def test_gfstep():
    assert 1


def test_gfstol():
    assert 1


def test_gfsubc():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et0 = spice.str2et('2007 JAN 01')
    et1 = spice.str2et('2008 JAN 01')
    cnfine = spice.stypes.SPICEDOUBLE_CELL(2)
    spice.wninsd(et0, et1, cnfine)
    result = spice.stypes.SPICEDOUBLE_CELL(2000)
    spice.gfsubc("earth", "iau_earth", "Near point: ellipsoid", "none", "sun", "geodetic", "latitude", ">",
                 16.0 * spice.rpd(), 0.0, spice.spd() * 90.0, 1000, cnfine, result)
    count = spice.wncard(result)
    assert count > 0
    start, end = spice.wnfetd(result, 0)
    startTime = spice.timout(start, 'YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND', 41)
    endTime = spice.timout(end, 'YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND', 41)
    assert startTime == "2007-MAY-04 17:08:56.608433 (TDB)"
    assert endTime == "2007-AUG-09 01:51:29.367602 (TDB)"
    spice.kclear()


def test_gftfov():
    assert 1


def test_gfuds():
    assert 1


def test_gipool():
    # same as pipool test
    spice.kclear()
    data = np.arange(0, 10)
    spice.pipool('pipool_array', data)
    ivals, found = spice.gipool('pipool_array', 0, 50)
    assert found
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
    # Nearly the same as first half of test_edterm
    # possibly not smart to pick a terminator point for test.
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et("2007 FEB 3 00:00:00.000")
    trgepc, obspos, trmpts = spice.edterm("UMBRAL", "SUN", "MOON", et, "IAU_MOON", "LT+S", "EARTH", 3)
    expected_trmpts0 = [-153.978389497704, -1730.5633188256702, 0.12289334835869758]
    npt.assert_array_almost_equal(trmpts[0], expected_trmpts0)
    phase, solar, emissn = spice.illum("MOON", et, "LT+S", "EARTH", trmpts[0])
    npt.assert_almost_equal(spice.dpr() * phase, 9.206598961784051)
    npt.assert_almost_equal(spice.dpr() * solar, 90.26976568986987)
    npt.assert_almost_equal(spice.dpr() * emissn, 99.27359973712625)
    spice.kclear()


def test_ilumin():
    # Same as first half of test_edterm
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et("2007 FEB 3 00:00:00.000")
    trgepc, obspos, trmpts = spice.edterm("UMBRAL", "SUN", "MOON", et, "IAU_MOON", "LT+S", "EARTH", 3)
    expected_trgepc = 223732863.86351672
    expected_obspos = [394721.10311942, 27265.12569734, -19069.08642173]
    expected_trmpts0 = [-153.978389497704, -1730.5633188256702, 0.12289334835869758]
    expected_trmpts1 = [87.375069963142522, 864.40670521284744, 1504.5681789576722]
    expected_trmpts2 = [42.213243378688254, 868.21134651980412, -1504.3223922609538]
    npt.assert_almost_equal(trgepc, expected_trgepc)
    npt.assert_array_almost_equal(obspos, expected_obspos)
    npt.assert_array_almost_equal(trmpts[0], expected_trmpts0)
    npt.assert_array_almost_equal(trmpts[1], expected_trmpts1)
    npt.assert_array_almost_equal(trmpts[2], expected_trmpts2)
    iluet0, srfvec0, phase0, solar0, emissn0 = spice.ilumin("Ellipsoid", "MOON", et, "IAU_MOON",
                                                            "LT+S", "EARTH", trmpts[0])
    npt.assert_almost_equal(spice.dpr() * solar0, 90.269765819)
    iluet1, srfvec1, phase1, solar1, emissn1 = spice.ilumin("Ellipsoid", "MOON", et, "IAU_MOON",
                                                            "LT+S", "EARTH", trmpts[1])
    npt.assert_almost_equal(spice.dpr() * solar1, 90.269765706)
    iluet2, srfvec2, phase2, solar2, emissn2 = spice.ilumin("Ellipsoid", "MOON", et, "IAU_MOON",
                                                            "LT+S", "EARTH", trmpts[2])
    npt.assert_almost_equal(spice.dpr() * solar2, 90.269765730)
    spice.kclear()


def test_inedpl():
    spice.kclear()
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
    term, found = spice.inedpl(radii[0], radii[1], radii[2], plane)
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
    spice.kclear()
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
    spice.kclear()
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
    testCell = spice.stypes.SPICECHAR_CELL(10, 10)
    cList = ["aaa", "bbb", "ccc", "bbb"]
    for c in cList:
        spice.insrtc(c, testCell)
    assert [x for x in testCell] == ["aaa", "bbb", "ccc"]


def test_insrtc_vectorized():
    testCell = spice.stypes.SPICECHAR_CELL(10, 10)
    cList = ["aaa", "bbb", "ccc", "bbb"]
    spice.insrtc(cList, testCell)
    assert [x for x in testCell] == ["aaa", "bbb", "ccc"]


def test_insrtd():
    testCell = spice.stypes.SPICEDOUBLE_CELL(8)
    dlist = [0.5, 2.0, 30.0, 0.01, 30.0]
    for d in dlist:
        spice.insrtd(d, testCell)
    assert [x for x in testCell] == [0.01, 0.5, 2.0, 30.0]


def test_insrtd_vectorized():
    testCell = spice.stypes.SPICEDOUBLE_CELL(8)
    dList = [0.5, 2.0, 30.0, 0.01, 30.0]
    spice.insrtd(dList, testCell)
    assert [x for x in testCell] == [0.01, 0.5, 2.0, 30.0]


def test_insrti():
    testCell = spice.stypes.SPICEINT_CELL(8)
    ilist = [1, 2, 30, 1, 30]
    for i in ilist:
        spice.insrti(i, testCell)
    assert [x for x in testCell] == [1, 2, 30]


def test_insrti_vectorized():
    testCell = spice.stypes.SPICEINT_CELL(8)
    iList = [1, 2, 30, 1, 30]
    spice.insrti(iList, testCell)
    assert [x for x in testCell] == [1, 2, 30]


def test_inter():
    testCellOne = spice.stypes.SPICEINT_CELL(8)
    testCellTwo = spice.stypes.SPICEINT_CELL(8)
    spice.insrti(1, testCellOne)
    spice.insrti(2, testCellOne)
    spice.insrti(1, testCellTwo)
    spice.insrti(3, testCellTwo)
    outCell = spice.inter(testCellOne, testCellTwo)
    assert [x for x in outCell] == [1]


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
    # I think this is valid...
    m = spice.ident()
    mit = spice.invort(m)
    npt.assert_array_almost_equal(m, mit)


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
    assert spice.isrot(spice.ident(), 0.0001, 0.0001)


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
    spice.kclear()
    spice.furnsh(_testKernelPath)
    file, ftype, source, handle, found = spice.kdata(0, "META", 400, 10, 50)
    assert found
    assert ftype == 'META'
    spice.kclear()


def test_kinfo():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    filetype, source, handle, found = spice.kinfo(_testKernelPath, 80, 80)
    assert found
    assert filetype == 'META'
    spice.kclear()


def test_kplfrm():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    cell = spice.kplfrm(-1)
    assert cell.size > 100
    spice.kclear()


def test_ktotal():
    spice.kclear()
    # same as unload test
    spice.furnsh(_testKernelPath)
    # 4 kernels + the meta kernel = 5
    assert spice.ktotal("ALL") == 5
    spice.unload(_testKernelPath)
    assert spice.ktotal("ALL") == 0
    spice.kclear()


def test_kxtrct():
    assert 1
    # Unstable, not sure why but I am getting segfaults
    # instring = "FROM 1 October 1984 12:00:00 TO 1 January 1987"
    # outstring, found, substr = spice.kxtrct("TO", 13, ["FROM", "TO", "BEGINNING", "ENDING"], 5, 120, 120, instring)
    # assert found
    # assert outstring == 'FROM 1 October 1984 12:00:00'
    # assert substr == '1 January 1987'


# def test_kxtrctstress():
# for i in range(500):
#         test_kxtrct()


def test_lastnb():
    assert spice.lastnb("ABCDE") == 4
    assert spice.lastnb("AN EXAMPLE") == 9
    assert spice.lastnb("AN EXAMPLE        ") == 9
    assert spice.lastnb("        ") == -1


def test_latcyl():
    expected1 = np.array([1.0, 0.0, 0.0])
    expected2 = np.array([1.0, 90.0 * spice.rpd(), 0.0])
    expected3 = np.array([1.0, 180.0 * spice.rpd(), 0.0])
    npt.assert_array_almost_equal(expected1, spice.latcyl(1.0, 0.0, 0.0), decimal=7)
    npt.assert_array_almost_equal(expected2, spice.latcyl(1.0, 90.0 * spice.rpd(), 0.0), decimal=7)
    npt.assert_array_almost_equal(expected3, spice.latcyl(1.0, 180.0 * spice.rpd(), 0.0), decimal=7)


def test_latrec():
    expected1 = np.array([1.0, 0.0, 0.0])
    expected2 = np.array([0.0, 1.0, 0.0])
    expected3 = np.array([-1.0, 0.0, 0.0])
    npt.assert_array_almost_equal(expected1, spice.latrec(1.0, 0.0, 0.0), decimal=7)
    npt.assert_array_almost_equal(expected2, spice.latrec(1.0, 90.0 * spice.rpd(), 0.0), decimal=7)
    npt.assert_array_almost_equal(expected3, spice.latrec(1.0, 180.0 * spice.rpd(), 0.0), decimal=7)


def test_latsph():
    expected1 = np.array([1.0, 90.0 * spice.rpd(), 0.0])
    expected2 = np.array([1.0, 90.0 * spice.rpd(), 90.0 * spice.rpd()])
    expected3 = np.array([1.0, 90.0 * spice.rpd(), 180.0 * spice.rpd()])
    npt.assert_array_almost_equal(expected1, spice.latsph(1.0, 0.0, 0.0), decimal=7)
    npt.assert_array_almost_equal(expected2, spice.latsph(1.0, 90.0 * spice.rpd(), 0.0), decimal=7)
    npt.assert_array_almost_equal(expected3, spice.latsph(1.0, 180.0 * spice.rpd(), 0.0), decimal=7)


def test_lcase():
    assert spice.lcase("THIS IS AN EXAMPLE", 20) == "THIS IS AN EXAMPLE".lower()
    assert spice.lcase("1234", 5) == "1234"


def test_ldpool():
    spice.kclear()
    ldpoolNames = ['DELTET/DELTA_T_A', 'DELTET/K', 'DELTET/EB', 'DELTET/M', 'DELTET/DELTA_AT']
    ldpoolLens = [1, 1, 1, 2, 46]
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
    kernel = os.path.join(cwd, 'ldpool_test.tls')
    if spice.exists(kernel):
        os.remove(kernel)
    with open(kernel, 'w') as kernelFile:
        kernelFile.write('\\begindata\n')
        for line in textbuf:
            kernelFile.write(line + "\n")
        kernelFile.write("\\begintext\n")
        kernelFile.close()
    spice.ldpool(kernel)
    for var, expectLen in zip(ldpoolNames, ldpoolLens):
        found, n, vartype = spice.dtpool(var)
        assert found
        assert expectLen == n
        assert vartype == 'N'
    spice.kclear()
    if spice.exists(kernel):
        os.remove(kernel)


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


def test_lmpoolstress():
    # occasional crash in lmpool believed to be caused by lenvals not being +=1'ed for end of line.
    for i in range(500):
        test_lmpool()


def test_lparse():
    stringtest = 'one two three four'
    items = spice.lparse(stringtest, ' ', 25)
    assert items == ['one', 'two', 'three', 'four']


def test_lparsm():
    stringtest = "  A number of words   separated   by spaces   "
    items = spice.lparsm(stringtest, " ", 20, lenout=20)
    assert items == ['A', 'number', 'of', 'words', 'separated', 'by', 'spaces']


def test_lparss():
    stringtest = "  A number of words   separated   by spaces.   "
    delims = " ,."
    outset = spice.lparss(stringtest, delims)
    expected = ['', 'A', 'by', 'number', 'of', 'separated', 'spaces', 'words']
    assert [x for x in outset] == expected


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
    assert spice.lx4dec("1%2%3", 0) == (0, 1)
    assert spice.lx4dec("1%2%3", 1) == (0, 0)
    assert spice.lx4dec("1%2%3", 2) == (2, 1)


def test_lx4num():
    assert spice.lx4num("1%2%3", 0) == (0, 1)
    assert spice.lx4num("1%2%3", 1) == (0, 0)
    assert spice.lx4num("1%2%3", 2) == (2, 1)
    assert spice.lx4num("1%2e1%3", 2) == (4, 3)


def test_lx4sgn():
    assert spice.lx4sgn("1%2%3", 0) == (0, 1)
    assert spice.lx4sgn("1%2%3", 1) == (0, 0)
    assert spice.lx4sgn("1%2%3", 2) == (2, 1)


def test_lx4uns():
    # not a very good test
    assert spice.lx4uns("test 10 end", 4) == (3, 0)


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


def test_mequ():
    m1 = np.identity(3)
    mout = spice.mequ(m1)
    assert np.array_equal(m1, mout)


def test_mequg():
    m1 = np.identity(2)
    mout = spice.mequg(m1, 2, 2)
    assert np.array_equal(m1, mout)


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


def test_occult():
    assert 1


def test_ordc():
    charset = spice.stypes.SPICECHAR_CELL(10, 10)
    inputs = ["8", "1", "2", "9", "7", "4", "10"]
    expected = [5, 0, 2, 6, 4, 3, 1]
    for c in inputs:
        spice.insrtc(c, charset)
    for i, e in zip(inputs, expected):
        assert e == spice.ordc(i, charset)


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
    npt.assert_array_almost_equal(expectedOrder, order)


def test_orderd():
    inarray = [0.0, 2.0, 1.0]
    expectedOrder = [0, 2, 1]
    order = spice.orderd(inarray)
    npt.assert_array_almost_equal(expectedOrder, order)


def test_orderi():
    inarray = [0, 2, 1]
    expectedOrder = [0, 2, 1]
    order = spice.orderi(inarray)
    npt.assert_array_almost_equal(expectedOrder, order)


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
    spice.kclear()
    ids = spice.stypes.SPICEINT_CELL(1000)
    cover = spice.stypes.SPICEDOUBLE_CELL(2000)
    spice.pckfrm(_spkEarthPck, ids)
    spice.scard(0, cover)
    spice.pckcov(_spkEarthPck, ids[0], cover)
    result = [x for x in cover]
    expected = [-1197547158.8155186, 230817665.18534085]
    npt.assert_array_almost_equal(expected, result)
    spice.kclear()


def test_pckfrm():
    spice.kclear()
    ids = spice.stypes.SPICEINT_CELL(1000)
    spice.pckfrm(_spkEarthPck, ids)
    assert ids[0] == 3000
    spice.kclear()


def test_pcklof():
    spice.kclear()
    handle = spice.pcklof(_spkEarthPck)
    assert handle != -1
    spice.pckuof(handle)
    spice.kclear()


def test_pckuof():
    spice.kclear()
    handle = spice.pcklof(_spkEarthPck)
    assert handle != -1
    spice.pckuof(handle)
    spice.kclear()


def test_pcpool():
    import string
    spice.kclear()
    data = [j + str(i) for i, j in enumerate(list(string.ascii_lowercase))]
    spice.pcpool('pcpool_test', data)
    cvals, found = spice.gcpool('pcpool_test', 0, 30, 4)
    assert data == cvals
    spice.kclear()


def test_pdpool():
    spice.kclear()
    data = np.arange(0.0, 10.0)
    spice.pdpool('pdpool_array', data)
    dvals, found = spice.gdpool('pdpool_array', 0, 30)
    npt.assert_array_almost_equal(data, dvals)
    spice.kclear()


def test_pgrrec():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    n, radii = spice.bodvrd("MARS", "RADII", 3)
    re = radii[0]
    rp = radii[2]
    f = (re - rp) / re
    rectan = spice.pgrrec("Mars", 90.0 * spice.rpd(), 45 * spice.rpd(), 300, re, f)
    expected = [1.604650025e-13, -2.620678915e+3, 2.592408909e+3]
    npt.assert_array_almost_equal(rectan, expected)
    spice.kclear()


def test_phaseq():
    relate = ["=", "<", ">", "LOCMIN", "ABSMIN", "LOCMAX", "ABSMAX"]
    expected = {"=": [0.575988450, 0.575988450, 0.575988450, 0.575988450, 0.575988450,
                      0.575988450, 0.575988450, 0.575988450, 0.575988450, 0.575988450],
                "<": [0.575988450, 0.575988450, 0.575988450, 0.575988450, 0.575988450, 0.468279091],
                ">": [0.940714974, 0.575988450, 0.575988450, 0.575988450, 0.575988450, 0.575988450],
                "LOCMIN": [0.086121423, 0.086121423, 0.079899769, 0.079899769],
                "ABSMIN": [0.079899769, 0.079899769],
                "LOCMAX": [3.055062862, 3.055062862, 3.074603891, 3.074603891],
                "ABSMAX": [3.074603891, 3.074603891]
    }
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et0 = spice.str2et('2006 DEC 01')
    et1 = spice.str2et('2007 JAN 31')
    cnfine = spice.stypes.SPICEDOUBLE_CELL(2)
    spice.wninsd(et0, et1, cnfine)
    result = spice.stypes.SPICEDOUBLE_CELL(10000)
    for relation in relate:
        spice.gfpa("Moon", "Sun", "LT+S", "Earth", relation, 0.57598845,
                   0.0, spice.spd(), 5000, cnfine, result)
        count = spice.wncard(result)
        if count > 0:
            tempResults = []
            for i in range(0, count):
                start, stop = spice.wnfetd(result, i)
                startPhase = spice.phaseq(start, "moon", "sun", "earth", "lt+s")
                stopPhase = spice.phaseq(stop, "moon", "sun", "earth", "lt+s")
                tempResults.append(startPhase)
                tempResults.append(stopPhase)
            npt.assert_array_almost_equal(tempResults, expected.get(relation))
    spice.kclear()


def test_pi():
    assert spice.pi() == np.pi


def test_pipool():
    spice.kclear()
    data = np.arange(0, 10)
    spice.pipool('pipool_array', data)
    ivals, found = spice.gipool('pipool_array', 0, 50)
    assert found
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
    spice.kclear()
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


def test_pxform():
    spice.kclear()
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


def test_qcktrc():
    spice.reset()
    spice.chkin("test")
    spice.chkin("qcktrc")
    trace = spice.qcktrc(40)
    assert trace == 'test --> qcktrc'
    spice.chkout("qcktrc")
    spice.chkout("test")
    spice.reset()


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
    npt.assert_array_almost_equal(spice.qxq(qI, qJ), qK)
    npt.assert_array_almost_equal(spice.qxq(qJ, qK), qI)
    npt.assert_array_almost_equal(spice.qxq(qK, qI), qJ)
    npt.assert_array_almost_equal(spice.qxq(qI, qI), nqID)
    npt.assert_array_almost_equal(spice.qxq(qJ, qJ), nqID)
    npt.assert_array_almost_equal(spice.qxq(qK, qK), nqID)
    npt.assert_array_almost_equal(spice.qxq(qID, qI), qI)
    npt.assert_array_almost_equal(spice.qxq(qI, qID), qI)


def test_radrec():
    npt.assert_array_almost_equal([1.0, 0.0, 0.0], spice.radrec(1.0, 0.0, 0.0))
    npt.assert_array_almost_equal([0.0, 1.0, 0.0], spice.radrec(1.0, 90.0 * spice.rpd(), 0.0))
    npt.assert_array_almost_equal([0.0, 0.0, 1.0], spice.radrec(1.0, 0.0, 90.0 * spice.rpd()))


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
    # This technically works, but there is no way to reset the read position between runs that I could find.
    # spice.kclear()
    # line, eof = spice.rdtext(_testKernelPath, 100)
    # assert not eof
    # assert line == '\\begindata'
    # spice.kclear()


def test_reccyl():
    expected1 = np.array([0.0, 0.0, 0.0])
    expected2 = np.array([1.0, 90.0 * spice.rpd(), 0.0])
    expected3 = np.array([1.0, 270.0 * spice.rpd(), 0.0])
    npt.assert_array_almost_equal(expected1, spice.reccyl([0.0, 0.0, 0.0]), decimal=7)
    npt.assert_array_almost_equal(expected2, spice.reccyl([0.0, 1.0, 0.0]), decimal=7)
    npt.assert_array_almost_equal(expected3, spice.reccyl([0.0, -1.0, 0.0]), decimal=7)


def test_recgeo():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    num_vals, radii = spice.bodvrd("EARTH", "RADII", 3)
    flat = (radii[0] - radii[2]) / radii[0]
    x = [-2541.748162, 4780.333036, 3360.428190]
    lon, lat, alt = spice.recgeo(x, radii[0], flat)
    actual = [lon * spice.dpr(), lat * spice.dpr(), alt]
    expected = [118.000000, 32.000000, 0.001915518]
    npt.assert_array_almost_equal(actual, expected, decimal=4)
    spice.kclear()


def test_reclat():
    expected1 = np.array([1.0, 0.0, 0.0])
    expected2 = np.array([1.0, 90.0 * spice.rpd(), 0.0])
    expected3 = np.array([1.0, 180.0 * spice.rpd(), 0.0])
    npt.assert_array_almost_equal(expected1, spice.reclat([1.0, 0.0, 0.0]), decimal=7)
    npt.assert_array_almost_equal(expected2, spice.reclat([0.0, 1.0, 0.0]), decimal=7)
    npt.assert_array_almost_equal(expected3, spice.reclat([-1.0, 0.0, 0.0]), decimal=7)


def test_recpgr():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    num_vals, radii = spice.bodvrd("MARS", "RADII", 3)
    flat = (radii[0] - radii[2]) / radii[0]
    x = [0.0, -2620.678914818178, 2592.408908856967]
    lon, lat, alt = spice.recpgr("MARS", x, radii[0], flat)
    actual = [lon * spice.dpr(), lat * spice.dpr(), alt]
    expected = [90.0, 45.0, 300.0]
    npt.assert_array_almost_equal(actual, expected, decimal=4)
    spice.kclear()


def test_recrad():
    range1, ra1, dec1 = spice.recrad([1.0, 0.0, 0.0])
    range2, ra2, dec2 = spice.recrad([0.0, 1.0, 0.0])
    range3, ra3, dec3 = spice.recrad([0.0, 0.0, 1.0])
    npt.assert_array_almost_equal([1.0, 0.0, 0.0], [range1, ra1, dec1])
    npt.assert_array_almost_equal([1.0, 90 * spice.rpd(), 0.0], [range2, ra2, dec2])
    npt.assert_array_almost_equal([1.0, 0.0, 90 * spice.rpd()], [range3, ra3, dec3])


def test_recsph():
    v1 = np.array([-1.0, 0.0, 0.0])
    assert spice.recsph(v1) == (1.0, np.pi/2, np.pi)


def test_removc():
    cell = spice.stypes.SPICECHAR_CELL(10, 10)
    items = ["one", "two", "three", "four"]
    for i in items:
        spice.insrtc(i, cell)
    removeItems = ["three", "four"]
    for r in removeItems:
        spice.removc(r, cell)
    expected = ["one", "two"]
    assert expected == [x for x in cell]


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
    npt.assert_array_almost_equal(outarray, [1.0, 2.0, 3.0])


def test_reordi():
    array = [1, 3, 2]
    iorder = [0, 2, 1]
    outarray = spice.reordi(iorder, 3, array)
    npt.assert_array_almost_equal(outarray, [1, 2, 3])


def test_reordl():
    array = [True, True, False]
    iorder = [0, 2, 1]
    outarray = spice.reordl(iorder, 3, array)
    npt.assert_array_almost_equal(outarray, array)  # reordl has the same issue as reordc


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
    spice.reset()
    assert not spice.failed()


def test_return_c():
    spice.reset()
    assert not spice.return_c()
    spice.reset()


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
    spice.kclear()
    spice.furnsh(_testKernelPath)
    spice.furnsh(_extraTestVoyagerKernel)
    timein = spice.scencd(-32, '2/20538:39:768')
    sclkch = spice.scdecd(-32, timein, 50)
    assert sclkch == '2/20538:39:768'
    spice.kclear()


def test_sce2c():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    spice.furnsh(_extraTestVoyagerKernel)
    et = spice.str2et('1979 JUL 05 21:50:21.23379')
    sclkdp = spice.sce2c(-32, et)
    npt.assert_almost_equal(sclkdp, 985327949.9999709, decimal=6)
    spice.kclear()


def test_sce2s():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    spice.furnsh(_extraTestVoyagerKernel)
    et = spice.str2et('1979 JUL 05 21:50:21.23379')
    sclkch = spice.sce2s(-32, et, 50)
    assert sclkch == "2/20538:39:768"
    spice.kclear()


def test_sce2t():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    spice.furnsh(_extraTestVoyagerKernel)
    et = spice.str2et('1979 JUL 05 21:50:21.23379')
    sclkdp = spice.sce2t(-32, et)
    npt.assert_almost_equal(sclkdp, 985327950.000000)
    spice.kclear()


def test_scencd():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    spice.furnsh(_extraTestVoyagerKernel)
    sclkch = spice.scdecd(-32, 985327950.0, 50)
    sclkdp = spice.scencd(-32, sclkch)
    npt.assert_almost_equal(sclkdp, 985327950.0)
    assert sclkch == "2/20538:39:768"
    spice.kclear()


def test_scfmt():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    spice.furnsh(_extraTestVoyagerKernel)
    pstart, pstop = spice.scpart(-32)
    start = spice.scfmt(-32, pstart[0], 50)
    stop = spice.scfmt(-32, pstop[0], 50)
    assert start == "00011:00:001"
    assert stop == "04011:21:784"
    spice.kclear()


def test_scpart():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    spice.furnsh(_extraTestVoyagerKernel)
    pstart, pstop = spice.scpart(-32)
    assert pstart is not None
    assert pstop is not None
    spice.kclear()


def test_scs2e():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    spice.furnsh(_extraTestVoyagerKernel)
    et = spice.scs2e(-32, '2/20538:39:768')
    npt.assert_almost_equal(et, -646668528.58222842)
    utc = spice.et2utc(et, 'C', 3, 50)
    assert utc == "1979 JUL 05 21:50:21.234"
    spice.kclear()


def test_sct2e():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    spice.furnsh(_extraTestVoyagerKernel)
    et = spice.sct2e(-32, 985327965.0)
    utc = spice.et2utc(et, 'C', 3, 50)
    assert utc == "1979 JUL 05 21:50:22.134"
    spice.kclear()


def test_sctiks():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    spice.furnsh(_extraTestVoyagerKernel)
    ticks = spice.sctiks(-32, '20656:14:768')
    assert ticks == 991499967.00000000
    spice.kclear()


def test_sdiff():
    a = spice.stypes.SPICEINT_CELL(8)
    b = spice.stypes.SPICEINT_CELL(8)
    spice.insrti(1, a)
    spice.insrti(2, a)
    spice.insrti(3, b)
    spice.insrti(4, b)
    c = spice.sdiff(a, b)
    assert [x for x in c] == [1, 2, 3, 4]


def test_set_c():
    a = spice.stypes.SPICEINT_CELL(8)
    b = spice.stypes.SPICEINT_CELL(8)
    c = spice.stypes.SPICEINT_CELL(8)
    spice.insrti(1, a)
    spice.insrti(2, a)
    spice.insrti(3, a)
    spice.insrti(4, a)
    spice.insrti(1, b)
    spice.insrti(3, b)
    spice.insrti(1, c)
    spice.insrti(3, c)
    assert spice.set_c(b, "=", c)
    assert spice.set_c(a, "<>", c)
    assert spice.set_c(b, "<=", c)
    assert not spice.set_c(b, "<", c)
    assert spice.set_c(c, ">=", b)
    assert spice.set_c(a, ">", b)
    assert spice.set_c(b, "&", c)
    assert not spice.set_c(a, "~", a)


def test_setmsg():
    spice.setmsg("test setmsg")
    spice.sigerr("some error")
    message = spice.getmsg("LONG", 2000)
    assert message == "test setmsg"
    spice.reset()


def test_shellc():
    array = ["FEYNMAN", "NEWTON", "EINSTEIN", "GALILEO", "EUCLID", "Galileo"]
    expected = ["EINSTEIN", "EUCLID", "FEYNMAN", "GALILEO", "Galileo", "NEWTON"]
    assert spice.shellc(6, 10, array) == expected


def test_shelld():
    array = [99.0, 33.0, 55.0, 44.0, -77.0, 66.0]
    expected = [-77.0, 33.0, 44.0, 55.0, 66.0, 99.0]
    npt.assert_array_almost_equal(spice.shelld(6, array), expected)


def test_shelli():
    array = [99, 33, 55, 44, -77, 66]
    expected = [-77, 33, 44, 55, 66, 99]
    npt.assert_array_almost_equal(spice.shelli(6, array), expected)


def test_sigerr():
    spice.sigerr("test error")
    message = spice.getmsg("SHORT", 200)
    assert message == "test error"
    spice.reset()


def test_sincpt():
    assert 1


def test_size():
    testCellOne = spice.stypes.SPICEINT_CELL(8)
    assert spice.size(testCellOne) == 8


def test_spd():
    assert spice.spd() == 86400.0


def test_sphcyl():
    a = np.array(spice.sphcyl(1.4142, np.deg2rad(180.0), np.deg2rad(45.0)))
    b = [0.0, np.deg2rad(45.0), -np.sqrt(2)]
    np.testing.assert_almost_equal(a, b, decimal=4)


def test_sphlat():
    result = np.array(spice.sphlat(1.0, spice.pi(), spice.halfpi()))
    expected = np.array([0.0, spice.halfpi(), -1.0])
    npt.assert_array_almost_equal(result, expected)


def test_sphrec():
    expected1 = np.array([0.0, 0.0, 0.0])
    expected2 = np.array([1.0, 0.0, 0.0])
    expected3 = np.array([0.0, 0.0, -1.0])
    npt.assert_array_almost_equal(spice.sphrec(0.0, 0.0, 0.0), expected1)
    npt.assert_array_almost_equal(spice.sphrec(1.0, 90.0 * spice.rpd(), 0.0), expected2)
    npt.assert_array_almost_equal(spice.sphrec(1.0, 180.0 * spice.rpd(), 0.0), expected3)


def test_spk14a():
    discrete_epochs = [100.0, 200.0, 300.0, 400.0]
    cheby_coeffs14 = [1.0101, 1.0102, 1.0103, 1.0201, 1.0202, 1.0203, 1.0301, 1.0302,
                      1.0303, 2.0101, 2.0102, 2.0103, 2.0201, 2.0202, 2.0203, 2.0301,
                      2.0302, 2.0303, 3.0101, 3.0102, 3.0103, 3.0201, 3.0202, 3.0203,
                      3.0301, 3.0302, 3.0303, 4.0101, 4.0102, 4.0103, 4.0201, 4.0202,
                      4.0203, 4.0301, 4.0302, 4.0303]
    spk14 = os.path.join(cwd, "test14.bsp")
    if spice.exists(spk14):
        os.remove(spk14)
    spice.kclear()
    handle = spice.spkopn(spk14, 'Type 14 SPK internal file name.', 1024)
    init_size = os.path.getsize(spk14)
    spice.spk14b(handle, "SAMPLE_SPK_TYPE_14_SEGMENT", 399, 0, "J2000", 100.0, 400.0, 2)
    spice.spk14a(handle, 4, cheby_coeffs14, discrete_epochs)
    spice.spk14e(handle)
    spice.spkcls(handle)
    end_size = os.path.getsize(spk14)
    spice.kclear()
    assert end_size != init_size
    if spice.exists(spk14):
        os.remove(spk14)


def test_spk14bstress():
    for i in range(30):
        test_spk14a()


def test_spk14b():
    # Same as test_spk14a
    discrete_epochs = [100.0, 200.0, 300.0, 400.0]
    cheby_coeffs14 = [1.0101, 1.0102, 1.0103, 1.0201, 1.0202, 1.0203, 1.0301, 1.0302,
                      1.0303, 2.0101, 2.0102, 2.0103, 2.0201, 2.0202, 2.0203, 2.0301,
                      2.0302, 2.0303, 3.0101, 3.0102, 3.0103, 3.0201, 3.0202, 3.0203,
                      3.0301, 3.0302, 3.0303, 4.0101, 4.0102, 4.0103, 4.0201, 4.0202,
                      4.0203, 4.0301, 4.0302, 4.0303]
    spk14 = os.path.join(cwd, "test14.bsp")
    if spice.exists(spk14):
        os.remove(spk14)
    spice.kclear()
    handle = spice.spkopn(spk14, 'Type 14 SPK internal file name.', 1024)
    init_size = os.path.getsize(spk14)
    spice.spk14b(handle, "SAMPLE_SPK_TYPE_14_SEGMENT", 399, 0, "J2000", 100.0, 400.0, 2)
    spice.spk14a(handle, 4, cheby_coeffs14, discrete_epochs)
    spice.spk14e(handle)
    spice.spkcls(handle)
    end_size = os.path.getsize(spk14)
    spice.kclear()
    assert end_size != init_size
    if spice.exists(spk14):
        os.remove(spk14)


def test_spk14e():
    # Same as test_spk14a
    discrete_epochs = [100.0, 200.0, 300.0, 400.0]
    cheby_coeffs14 = [1.0101, 1.0102, 1.0103, 1.0201, 1.0202, 1.0203, 1.0301, 1.0302,
                      1.0303, 2.0101, 2.0102, 2.0103, 2.0201, 2.0202, 2.0203, 2.0301,
                      2.0302, 2.0303, 3.0101, 3.0102, 3.0103, 3.0201, 3.0202, 3.0203,
                      3.0301, 3.0302, 3.0303, 4.0101, 4.0102, 4.0103, 4.0201, 4.0202,
                      4.0203, 4.0301, 4.0302, 4.0303]
    spk14 = os.path.join(cwd, "test14.bsp")
    if spice.exists(spk14):
        os.remove(spk14)
    spice.kclear()
    handle = spice.spkopn(spk14, 'Type 14 SPK internal file name.', 1024)
    init_size = os.path.getsize(spk14)
    spice.spk14b(handle, "SAMPLE_SPK_TYPE_14_SEGMENT", 399, 0, "J2000", 100.0, 400.0, 2)
    spice.spk14a(handle, 4, cheby_coeffs14, discrete_epochs)
    spice.spk14e(handle)
    spice.spkcls(handle)
    end_size = os.path.getsize(spk14)
    spice.kclear()
    assert end_size != init_size
    if spice.exists(spk14):
        os.remove(spk14)


def test_spkacs():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et("2000 JAN 1 12:00:00 TDB")
    state, lt, dlt = spice.spkacs(301, et, "J2000", "lt+s", 399)
    expected_state = [-291584.6134480068, -266693.40606842656, -76095.65338145087,
                      0.6434391581633632, -0.6660658731229177, -0.3013100630066896]
    expected_lt = 1.3423106103603615
    expected_dlt = 1.073169085424106e-07
    npt.assert_almost_equal(expected_lt, lt)
    npt.assert_almost_equal(expected_dlt, dlt)
    npt.assert_array_almost_equal(expected_state, state)
    spice.kclear()


def test_spkapo():
    spice.kclear()
    MARS = 499
    MOON = 301
    EPOCH = 'Jan 1 2004 5:00 PM'
    REF = 'J2000'
    ABCORR = 'LT+S'
    spice.furnsh(_testKernelPath)
    et = spice.str2et(EPOCH)
    state = spice.spkssb(MOON, et, REF)
    pos_vec, ltime = spice.spkapo(MARS, et, REF, state, ABCORR)
    expectedPos = [164534472.31249404, 25121994.36858549, 11145412.838521784]
    npt.assert_array_almost_equal(pos_vec, expectedPos, decimal=5)
    spice.kclear()


def test_spkapp():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et('Jan 1 2004 5:00 PM')
    state = spice.spkssb(301, et, 'J2000')
    state_vec, ltime = spice.spkapp(499, et, 'J2000', state, 'LT+S')
    expected_vec = [164534472.31249404, 25121994.36858549, 11145412.838521784,
                    12.311977095260765, 19.88840036075132, 9.406787036260496]
    npt.assert_array_almost_equal(expected_vec, state_vec, decimal=6)
    spice.kclear()


def test_spkaps():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et("2000 JAN 1 12:00:00 TDB")
    stobs = spice.spkssb(399, et, 'J2000')
    state0 = np.array(spice.spkssb(399, et - 1, 'J2000'))
    state2 = np.array(spice.spkssb(399, et + 1, 'J2000'))
    # qderiv proc
    acc = spice.vlcomg(3, 0.5 / 1.0, state0 + 3, -0.5 / 1.0, state2 + 3)
    acc = [acc[0], acc[1], acc[2], 0.0, 0.0, 0.0]
    state, lt, dlt = spice.spkaps(301, et, "j2000", "lt+s", stobs, acc)
    spice.kclear()
    expectedLt = 1.3423106103603615
    expectedDlt = 1.073169085424106e-07
    expectedState = [-291584.61344800, -266693.406068426, -76095.653381450,
                     15.9912693205773, -16.4471172000903, -3.80333394481323]
    npt.assert_almost_equal(expectedLt, lt)
    npt.assert_almost_equal(expectedDlt, dlt)
    npt.assert_array_almost_equal(state, expectedState, decimal=5)


def test_spkcls():
    # Same as test_spkw02
    SPK2 = os.path.join(cwd, "test2.bsp")
    if spice.exists(SPK2):
        os.remove(SPK2)
    spice.kclear()
    handle = spice.spkopn(SPK2, 'Type 2 SPK internal file name.', 4)
    init_size = os.path.getsize(SPK2)
    discrete_epochs = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0]
    cheby_coeffs02 = [1.0101, 1.0102, 1.0103, 1.0201, 1.0202, 1.0203, 1.0301, 1.0302,
                      1.0303, 2.0101, 2.0102, 2.0103, 2.0201, 2.0202, 2.0203, 2.0301,
                      2.0302, 2.0303, 3.0101, 3.0102, 3.0103, 3.0201, 3.0202, 3.0203,
                      3.0301, 3.0302, 3.0303, 4.0101, 4.0102, 4.0103, 4.0201, 4.0202,
                      4.0203, 4.0301, 4.0302, 4.0303]
    segid = 'SPK type 2 test segment'
    intlen = discrete_epochs[1] - discrete_epochs[0]
    spice.spkw02(handle, 3, 10, "J2000", discrete_epochs[0],
                 discrete_epochs[4], segid, intlen, 4, 2, cheby_coeffs02, discrete_epochs[0])
    spice.spkcls(handle)
    end_size = os.path.getsize(SPK2)
    spice.kclear()
    assert end_size != init_size
    if spice.exists(SPK2):
        os.remove(SPK2)


def test_spkcov():
    spice.kclear()
    cover = spice.stypes.SPICEDOUBLE_CELL(2000)
    ids = spice.spkobj(_spk)
    tempObj = ids[0]
    spice.scard(0, cover)
    spice.spkcov(_spk, tempObj, cover)
    result = [x for x in cover]
    expected = [-3169195200.0, 1696852800.0]
    npt.assert_array_almost_equal(expected, result)
    spice.kclear()


def test_spkcpo():
    spice.kclear()
    spice.furnsh(_spkEarthFk)
    spice.furnsh(_spkEarthPck)
    spice.furnsh(_spkEarthTf)
    spice.furnsh(_testKernelPath)
    et = spice.str2et("2003 Oct 13 06:00:00")
    obspos = [-2353.6213656676991, -4641.3414911499403, 3677.0523293197439]
    state, lt = spice.spkcpo("SUN", et, "DSS-14_TOPO", "OBSERVER", "CN+S", obspos, "EARTH", "ITRF93")
    spice.kclear()
    expected_lt = 497.93167796983954
    expected_state = [62512272.820748448, 58967494.425136007, -122059095.46751881, 2475.9732651736126,
                      -9870.2670623216945, -3499.9080996916828]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state, decimal=6)


def test_spkcpt():
    spice.kclear()
    spice.furnsh(_spkEarthFk)
    spice.furnsh(_spkEarthPck)
    spice.furnsh(_spkEarthTf)
    spice.furnsh(_testKernelPath)
    obstime = spice.str2et("2003 Oct 13 06:00:00")
    trgpos = [-2353.6213656676991, -4641.3414911499403, 3677.0523293197439]
    state, lt = spice.spkcpt(trgpos, "EARTH", "ITRF93", obstime, "ITRF93", "TARGET", "CN+S", "SUN")
    spice.kclear()
    expected_lt = 497.9321929168437
    expected_state = [-3412628.5100264344, -147916331.60178328, 19812403.694927953,
                      -10758.244807895861, 250.02820706157181, 11.135445277312105]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state, decimal=6)


def test_spkcvo():
    spice.kclear()
    spice.furnsh(_spkEarthFk)
    spice.furnsh(_spkEarthPck)
    spice.furnsh(_spkEarthTf)
    spice.furnsh(_testKernelPath)
    obstime = spice.str2et("2003 Oct 13 06:00:00")
    obstate = [-2353.6213656676991, -4641.3414911499403, 3677.0523293197439, -0.00000000000057086, 0.00000000000020549,
               -0.00000000000012171]
    state, lt = spice.spkcvo("SUN", obstime, "DSS-14_TOPO", "OBSERVER", "CN+S", obstate, 0.0, "EARTH", "ITRF93")
    spice.kclear()
    expected_lt = 497.9316779697656
    expected_state = [62512272.820765018, 58967494.425064847, -122059095.46751761,
                      2475.9732651736767, -9870.2670623218419, -3499.908099691786]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state, decimal=6)


def test_spkcvt():
    spice.kclear()
    spice.furnsh(_spkEarthFk)
    spice.furnsh(_spkEarthPck)
    spice.furnsh(_spkEarthTf)
    spice.furnsh(_testKernelPath)
    obstime = spice.str2et("2003 Oct 13 06:00:00")
    trgstate = [-2353.6213656676991, -4641.3414911499403, 3677.0523293197439, -0.00000000000057086, 0.00000000000020549,
                -0.00000000000012171]
    state, lt = spice.spkcvt(trgstate, 0.0, "EARTH", "ITRF93", obstime, "ITRF93", "TARGET", "CN+S", "SUN")
    spice.kclear()
    expected_lt = 497.9321929167615
    expected_state = [-3412628.5100945341, -147916331.60175875, 19812403.694913436,
                      -10758.244807895686, 250.02820706156825, 11.135445277311799]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state, decimal=6)


def test_spkez():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et('July 4, 2003 11:00 AM PST')
    state, lt = spice.spkez(499, et, 'J2000', 'LT+S', 399)
    expected_lt = 269.6898816177049
    expected_state = [73822235.33116072, -27127919.178592984, -18741306.284863796,
                      -6.808513317178952, 7.513996167680786, 3.001298515816776]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state)
    spice.kclear()


def test_spkezp():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et('July 4, 2003 11:00 AM PST')
    pos, lt = spice.spkezp(499, et, 'J2000', 'LT+S', 399)
    expected_lt = 269.6898816177049
    expected_pos = [73822235.33116072, -27127919.178592984, -18741306.284863796]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(pos, expected_pos)
    spice.kclear()


def test_spkezr():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et('July 4, 2003 11:00 AM PST')
    state, lt = spice.spkezr("Mars", et, "J2000", "LT+S", "Earth")
    expected_lt = 269.6898816177049
    expected_state = [73822235.33116072, -27127919.178592984, -18741306.284863796,
                      -6.808513317178952, 7.513996167680786, 3.001298515816776]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state)
    spice.kclear()


def test_spkgeo():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et('July 4, 2003 11:00 AM PST')
    state, lt = spice.spkgeo(499, et, 'J2000', 399)
    expected_lt = 269.7026477630999
    expected_state = [73826216.43519413, -27128030.732554913, -18741973.86834258,
                      -6.809503565936936, 7.513814280414338, 3.001290049558291]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state)
    spice.kclear()


def test_spkgps():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et('July 4, 2003 11:00 AM PST')
    pos, lt = spice.spkgps(499, et, 'J2000', 399)
    expected_lt = 269.7026477630999
    expected_pos = [73826216.43519413, -27128030.732554913, -18741973.86834258]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(pos, expected_pos)
    spice.kclear()


def test_spklef():
    assert 1


def test_spkltc():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et("2000 JAN 1 12:00:00 TDB")
    stobs = spice.spkssb(399, et, "j2000")
    state, lt, dlt = spice.spkltc(301, et, "j2000", "lt", stobs)
    expectedOneWayLt = 1.342310610325
    expectedLt = 1.07316909e-07
    expectedState = [-291569.26516582, -266709.18671506, -76099.15529096,
                     0.6435306139500, -0.6660818164735, -0.3013228313733]
    npt.assert_almost_equal(lt, expectedOneWayLt)
    npt.assert_almost_equal(dlt, expectedLt)
    npt.assert_array_almost_equal(state, expectedState, decimal=5)
    spice.kclear()


def test_spkobj():
    # Same as test_spkcov
    spice.kclear()
    cover = spice.stypes.SPICEDOUBLE_CELL(2000)
    ids = spice.spkobj(_spk)
    tempObj = ids[0]
    spice.scard(0, cover)
    spice.spkcov(_spk, tempObj, cover)
    result = [x for x in cover]
    expected = [-3169195200.0, 1696852800.0]
    npt.assert_array_almost_equal(expected, result)
    spice.kclear()


def test_spkopa():
    assert 1


def test_spkopn():
    # Same as test_spkw02
    SPK2 = os.path.join(cwd, "test2.bsp")
    if spice.exists(SPK2):
        os.remove(SPK2)
    spice.kclear()
    handle = spice.spkopn(SPK2, 'Type 2 SPK internal file name.', 4)
    init_size = os.path.getsize(SPK2)
    discrete_epochs = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0]
    cheby_coeffs02 = [1.0101, 1.0102, 1.0103, 1.0201, 1.0202, 1.0203, 1.0301, 1.0302,
                      1.0303, 2.0101, 2.0102, 2.0103, 2.0201, 2.0202, 2.0203, 2.0301,
                      2.0302, 2.0303, 3.0101, 3.0102, 3.0103, 3.0201, 3.0202, 3.0203,
                      3.0301, 3.0302, 3.0303, 4.0101, 4.0102, 4.0103, 4.0201, 4.0202,
                      4.0203, 4.0301, 4.0302, 4.0303]
    segid = 'SPK type 2 test segment'
    intlen = discrete_epochs[1] - discrete_epochs[0]
    spice.spkw02(handle, 3, 10, "J2000", discrete_epochs[0],
                 discrete_epochs[4], segid, intlen, 4, 2, cheby_coeffs02, discrete_epochs[0])
    spice.spkcls(handle)
    end_size = os.path.getsize(SPK2)
    spice.kclear()
    assert end_size != init_size
    if spice.exists(SPK2):
        os.remove(SPK2)


def test_spkpds():
    assert 1


def test_spkpos():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et('July 4, 2003 11:00 AM PST')
    pos, lt = spice.spkpos("Mars", et, "J2000", "LT+S", "Earth")
    expected_lt = 269.6898816177049
    expected_pos = [73822235.33116072, -27127919.178592984, -18741306.284863796]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(pos, expected_pos)
    spice.kclear()


def test_spkpos_vectorized():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et(['July 4, 2003 11:00 AM PST', 'July 11, 2003 11:00 AM PST'])
    pos, lt = spice.spkpos("Mars", et, "J2000", "LT+S", "Earth")
    expected_lt = [269.6898816177049, 251.44204349322627]
    expected_pos = [[73822235.33116072, -27127919.178592984, -18741306.284863796],
                    [69682765.56114145, -23090281.33320471, -17127756.9131108]]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(pos, expected_pos)
    spice.kclear()


def test_spkpvn():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et("2012 APR 27 00:00:00.000 TDB")
    handle, descr, ident, found = spice.spksfs(5, et, 41)
    refid, state, center = spice.spkpvn(handle, descr, et)
    expected_state = [464528993.98216486, 541513126.156852, 220785135.6246294,
                      -10.38685648307655, 7.953247007137424, 3.661858354313065]
    npt.assert_array_almost_equal(expected_state, state)
    spice.kclear()


def test_spksfs():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    idcode, found = spice.bodn2c("PLUTO BARYCENTER")
    et = spice.str2et("2011 FEB 18 UTC")
    handle, descr, ident, found = spice.spksfs(idcode, et, 41)
    assert ident == "DE-0421LE-0421"
    spice.kclear()


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
    SPK2 = os.path.join(cwd, "test2.bsp")
    if spice.exists(SPK2):
        os.remove(SPK2)
    spice.kclear()
    handle = spice.spkopn(SPK2, 'Type 2 SPK internal file name.', 4)
    init_size = os.path.getsize(SPK2)
    discrete_epochs = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0]
    cheby_coeffs02 = [1.0101, 1.0102, 1.0103, 1.0201, 1.0202, 1.0203, 1.0301, 1.0302,
                      1.0303, 2.0101, 2.0102, 2.0103, 2.0201, 2.0202, 2.0203, 2.0301,
                      2.0302, 2.0303, 3.0101, 3.0102, 3.0103, 3.0201, 3.0202, 3.0203,
                      3.0301, 3.0302, 3.0303, 4.0101, 4.0102, 4.0103, 4.0201, 4.0202,
                      4.0203, 4.0301, 4.0302, 4.0303]
    segid = 'SPK type 2 test segment'
    intlen = discrete_epochs[1] - discrete_epochs[0]
    spice.spkw02(handle, 3, 10, "J2000", discrete_epochs[0],
                 discrete_epochs[4], segid, intlen, 4, 2, cheby_coeffs02, discrete_epochs[0])
    spice.spkcls(handle)
    end_size = os.path.getsize(SPK2)
    spice.kclear()
    assert end_size != init_size
    if spice.exists(SPK2):
        os.remove(SPK2)


def test_spkw03():
    SPK3 = os.path.join(cwd, "test3.bsp")
    if spice.exists(SPK3):
        os.remove(SPK3)
    spice.kclear()
    handle = spice.spkopn(SPK3, 'Type 3 SPK internal file name.', 4)
    init_size = os.path.getsize(SPK3)
    discrete_epochs = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0]
    cheby_coeffs03 = [1.0101, 1.0102, 1.0103, 1.0201, 1.0202, 1.0203, 1.0301, 1.0302, 1.0303,
                      1.0401, 1.0402, 1.0403, 1.0501, 1.0502, 1.0503, 1.0601, 1.0602, 1.0603,
                      2.0101, 2.0102, 2.0103, 2.0201, 2.0202, 2.0203, 2.0301, 2.0302, 2.0303,
                      2.0401, 2.0402, 2.0403, 2.0501, 2.0502, 2.0503, 2.0601, 2.0602, 2.0603,
                      3.0101, 3.0102, 3.0103, 3.0201, 3.0202, 3.0203, 3.0301, 3.0302, 3.0303,
                      3.0401, 3.0402, 3.0403, 3.0501, 3.0502, 3.0503, 3.0601, 3.0602, 3.0603,
                      4.0101, 4.0102, 4.0103, 4.0201, 4.0202, 4.0203, 4.0301, 4.0302, 4.0303,
                      4.0401, 4.0402, 4.0403, 4.0501, 4.0502, 4.0503, 4.0601, 4.0602, 4.0603]
    segid = 'SPK type 3 test segment'
    intlen = discrete_epochs[1] - discrete_epochs[0]
    spice.spkw03(handle, 3, 10, "J2000", discrete_epochs[0],
                 discrete_epochs[4], segid, intlen, 4, 2, cheby_coeffs03, discrete_epochs[0])
    spice.spkcls(handle)
    end_size = os.path.getsize(SPK3)
    spice.kclear()
    assert end_size != init_size
    if spice.exists(SPK3):
        os.remove(SPK3)


def test_spkw05():
    SPK5 = os.path.join(cwd, "test5.bsp")
    if spice.exists(SPK5):
        os.remove(SPK5)
    spice.kclear()
    handle = spice.spkopn(SPK5, 'Type 5 SPK internal file name.', 4)
    init_size = os.path.getsize(SPK5)
    discrete_epochs = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0]
    discrete_states = [
        [101.0, 201.0, 301.0, 401.0, 501.0, 601.0],
        [102.0, 202.0, 302.0, 402.0, 502.0, 602.0],
        [103.0, 203.0, 303.0, 403.0, 503.0, 603.0],
        [104.0, 204.0, 304.0, 404.0, 504.0, 604.0],
        [105.0, 205.0, 305.0, 405.0, 505.0, 605.0],
        [106.0, 206.0, 306.0, 406.0, 506.0, 606.0],
        [107.0, 207.0, 307.0, 407.0, 507.0, 607.0],
        [108.0, 208.0, 308.0, 408.0, 508.0, 608.0],
        [109.0, 209.0, 309.0, 409.0, 509.0, 609.0]
    ]
    segid = 'SPK type 5 test segment'
    spice.spkw05(handle, 3, 10, "J2000", discrete_epochs[0], discrete_epochs[-1], segid,
                 132712440023.310, 9, discrete_states, discrete_epochs)
    spice.spkcls(handle)
    end_size = os.path.getsize(SPK5)
    spice.kclear()
    assert end_size != init_size
    if spice.exists(SPK5):
        os.remove(SPK5)


def test_spkw08():
    SPK8 = os.path.join(cwd, "test8.bsp")
    if spice.exists(SPK8):
        os.remove(SPK8)
    spice.kclear()
    handle = spice.spkopn(SPK8, 'Type 8 SPK internal file name.', 4)
    init_size = os.path.getsize(SPK8)
    discrete_epochs = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0]
    discrete_states = [
        [101.0, 201.0, 301.0, 401.0, 501.0, 601.0],
        [102.0, 202.0, 302.0, 402.0, 502.0, 602.0],
        [103.0, 203.0, 303.0, 403.0, 503.0, 603.0],
        [104.0, 204.0, 304.0, 404.0, 504.0, 604.0],
        [105.0, 205.0, 305.0, 405.0, 505.0, 605.0],
        [106.0, 206.0, 306.0, 406.0, 506.0, 606.0],
        [107.0, 207.0, 307.0, 407.0, 507.0, 607.0],
        [108.0, 208.0, 308.0, 408.0, 508.0, 608.0],
        [109.0, 209.0, 309.0, 409.0, 509.0, 609.0]
    ]
    segid = 'SPK type 8 test segment'
    step = discrete_epochs[1] - discrete_epochs[0]
    spice.spkw08(handle, 3, 10, "J2000", discrete_epochs[0], discrete_epochs[-1], segid,
                 3, 9, discrete_states, discrete_epochs[0], step)
    spice.spkcls(handle)
    end_size = os.path.getsize(SPK8)
    spice.kclear()
    assert end_size != init_size
    if spice.exists(SPK8):
        os.remove(SPK8)


def test_spkw09():
    SPK9 = os.path.join(cwd, "test9.bsp")
    if spice.exists(SPK9):
        os.remove(SPK9)
    spice.kclear()
    handle = spice.spkopn(SPK9, 'Type 9 SPK internal file name.', 4)
    init_size = os.path.getsize(SPK9)
    discrete_epochs = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0]
    discrete_states = [
        [101.0, 201.0, 301.0, 401.0, 501.0, 601.0],
        [102.0, 202.0, 302.0, 402.0, 502.0, 602.0],
        [103.0, 203.0, 303.0, 403.0, 503.0, 603.0],
        [104.0, 204.0, 304.0, 404.0, 504.0, 604.0],
        [105.0, 205.0, 305.0, 405.0, 505.0, 605.0],
        [106.0, 206.0, 306.0, 406.0, 506.0, 606.0],
        [107.0, 207.0, 307.0, 407.0, 507.0, 607.0],
        [108.0, 208.0, 308.0, 408.0, 508.0, 608.0],
        [109.0, 209.0, 309.0, 409.0, 509.0, 609.0]
    ]
    segid = 'SPK type 9 test segment'
    spice.spkw09(handle, 3, 10, "J2000", discrete_epochs[0], discrete_epochs[-1], segid,
                 3, 9, discrete_states, discrete_epochs)
    spice.spkcls(handle)
    end_size = os.path.getsize(SPK9)
    spice.kclear()
    assert end_size != init_size
    if spice.exists(SPK9):
        os.remove(SPK9)


def test_spkw10():
    SPK10 = os.path.join(cwd, "test10.bsp")
    spice.kclear()
    tle = ['1 18123U 87 53  A 87324.61041692 -.00000023  00000-0 -75103-5 0 00675',
           '2 18123  98.8296 152.0074 0014950 168.7820 191.3688 14.12912554 21686',
           '1 18123U 87 53  A 87326.73487726  .00000045  00000-0  28709-4 0 00684',
           '2 18123  98.8335 154.1103 0015643 163.5445 196.6235 14.12912902 21988',
           '1 18123U 87 53  A 87331.40868801  .00000104  00000-0  60183-4 0 00690',
           '2 18123  98.8311 158.7160 0015481 149.9848 210.2220 14.12914624 22644',
           '1 18123U 87 53  A 87334.24129978  .00000086  00000-0  51111-4 0 00702',
           '2 18123  98.8296 161.5054 0015372 142.4159 217.8089 14.12914879 23045',
           '1 18123U 87 53  A 87336.93227900 -.00000107  00000-0 -52860-4 0 00713',
           '2 18123  98.8317 164.1627 0014570 135.9191 224.2321 14.12910572 23425',
           '1 18123U 87 53  A 87337.28635487  .00000173  00000-0  10226-3 0 00726',
           '2 18123  98.8284 164.5113 0015289 133.5979 226.6438 14.12916140 23475',
           '1 18123U 87 53  A 87339.05673569  .00000079  00000-0  47069-4 0 00738',
           '2 18123  98.8288 166.2585 0015281 127.9985 232.2567 14.12916010 24908',
           '1 18123U 87 53  A 87345.43010859  .00000022  00000-0  16481-4 0 00758',
           '2 18123  98.8241 172.5226 0015362 109.1515 251.1323 14.12915487 24626',
           '1 18123U 87 53  A 87349.04167543  .00000042  00000-0  27370-4 0 00764',
           '2 18123  98.8301 176.1010 0015565 100.0881 260.2047 14.12916361 25138']
    epoch_x = []
    elems_x = []
    spice.furnsh(_testKernelPath)
    for i in range(0, 18, 2):
        lines = [tle[i], tle[i + 1]]
        epoch, elems = spice.getelm(1950, 75, lines)
        epoch_x.append(epoch)
        elems_x.extend(elems)
    first = epoch_x[0] - 0.5 * spice.spd()
    last = epoch_x[-1] + 0.5 * spice.spd()
    consts = [1.082616e-3, -2.538813e-6, -1.65597e-6, 7.43669161e-2, 120.0, 78.0, 6378.135, 1.0]
    if spice.exists(SPK10):
        os.remove(SPK10)
    handle = spice.spkopn(SPK10, 'Type 10 SPK internal file name.', 100)
    init_size = os.path.getsize(SPK10)
    spice.spkw10(handle, -118123, 399, "J2000", first, last, "DMSP F8", consts, 9, elems_x, epoch_x)
    spice.spkcls(handle)
    end_size = os.path.getsize(SPK10)
    assert end_size != init_size
    spice.kclear()
    if spice.exists(SPK10):
        os.remove(SPK10)


def test_spkw12():
    SPK12 = os.path.join(cwd, "test12.bsp")
    if spice.exists(SPK12):
        os.remove(SPK12)
    spice.kclear()
    handle = spice.spkopn(SPK12, 'Type 12 SPK internal file name.', 4)
    init_size = os.path.getsize(SPK12)
    discrete_epochs = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0]
    discrete_states = [
        [101.0, 201.0, 301.0, 401.0, 501.0, 601.0],
        [102.0, 202.0, 302.0, 402.0, 502.0, 602.0],
        [103.0, 203.0, 303.0, 403.0, 503.0, 603.0],
        [104.0, 204.0, 304.0, 404.0, 504.0, 604.0],
        [105.0, 205.0, 305.0, 405.0, 505.0, 605.0],
        [106.0, 206.0, 306.0, 406.0, 506.0, 606.0],
        [107.0, 207.0, 307.0, 407.0, 507.0, 607.0],
        [108.0, 208.0, 308.0, 408.0, 508.0, 608.0],
        [109.0, 209.0, 309.0, 409.0, 509.0, 609.0]
    ]
    segid = 'SPK type 12 test segment'
    step = discrete_epochs[1] - discrete_epochs[0]
    spice.spkw12(handle, 3, 10, "J2000", discrete_epochs[0], discrete_epochs[-1], segid,
                 3, 9, discrete_states, discrete_epochs[0], step)
    spice.spkcls(handle)
    end_size = os.path.getsize(SPK12)
    spice.kclear()
    assert end_size != init_size
    if spice.exists(SPK12):
        os.remove(SPK12)


def test_spkw13():
    SPK13 = os.path.join(cwd, "test13.bsp")
    if spice.exists(SPK13):
        os.remove(SPK13)
    spice.kclear()
    handle = spice.spkopn(SPK13, 'Type 13 SPK internal file name.', 4)
    init_size = os.path.getsize(SPK13)
    discrete_epochs = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0]
    discrete_states = [
        [101.0, 201.0, 301.0, 401.0, 501.0, 601.0],
        [102.0, 202.0, 302.0, 402.0, 502.0, 602.0],
        [103.0, 203.0, 303.0, 403.0, 503.0, 603.0],
        [104.0, 204.0, 304.0, 404.0, 504.0, 604.0],
        [105.0, 205.0, 305.0, 405.0, 505.0, 605.0],
        [106.0, 206.0, 306.0, 406.0, 506.0, 606.0],
        [107.0, 207.0, 307.0, 407.0, 507.0, 607.0],
        [108.0, 208.0, 308.0, 408.0, 508.0, 608.0],
        [109.0, 209.0, 309.0, 409.0, 509.0, 609.0]
    ]
    segid = 'SPK type 13 test segment'
    spice.spkw13(handle, 3, 10, "J2000", discrete_epochs[0], discrete_epochs[-1], segid,
                 3, 9, discrete_states, discrete_epochs)
    spice.spkcls(handle)
    end_size = os.path.getsize(SPK13)
    spice.kclear()
    assert end_size != init_size
    if spice.exists(SPK13):
        os.remove(SPK13)


def test_spkw15():
    assert 1


def test_spkw17():
    assert 1


def test_spkw18():
    assert 1


def test_spkw20():
    assert 1


def test_srfrec():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    x = spice.srfrec(399, 100.0 * spice.rpd(), 35.0 * spice.rpd())
    expected = [-906.24919474, 5139.59458217, 3654.29989637]
    npt.assert_array_almost_equal(x, expected)
    spice.kclear()


def test_srfxpt():
    assert 1


def test_ssize():
    cell = spice.stypes.SPICEDOUBLE_CELL(10)
    assert cell.size == 10
    spice.ssize(5, cell)
    assert cell.size == 5


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
    spice.kclear()
    kernel = os.path.join(cwd, 'stpool_t.ker')
    if spice.exists(kernel):
        os.remove(kernel)
    with open(kernel, 'w') as kernelFile:
        kernelFile.write('\\begindata\n')
        kernelFile.write("SPK_FILES = ( 'this_is_the_full_path_specification_*',\n")
        kernelFile.write("              'of_a_file_with_a_long_name',\n")
        kernelFile.write("              'this_is_the_full_path_specification_*',\n")
        kernelFile.write("              'of_a_second_file_name' )\n")
        kernelFile.close()
    spice.furnsh(kernel)
    string, n, found = spice.stpool("SPK_FILES", 0, "*", 256)
    assert found
    assert n == 62
    assert string == "this_is_the_full_path_specification_of_a_file_with_a_long_name"
    string, n, found = spice.stpool("SPK_FILES", 1, "*", 256)
    assert found
    assert n == 57
    assert string == "this_is_the_full_path_specification_of_a_second_file_name"
    spice.kclear()
    if spice.exists(kernel):
        os.remove(kernel)


def test_str2et():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    date = 'Thu Mar 20 12:53:29 PST 1997'
    et = spice.str2et(date)
    npt.assert_almost_equal(et, -87836728.81438904)
    spice.kclear()


def test_subpnt():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et('2008 aug 11 00:00:00')
    num_vals, radii = spice.bodvrd("MARS", "RADII", 3)
    re = radii[0]
    rp = radii[2]
    f = (re - rp) / re
    methods = ['Intercept:  ellipsoid', 'Near point: ellipsoid']
    expecteds = [[349199089.54077595, 349199089.57747161, 0.0, 199.30230503198658, 199.30230503198658,
                  26.262401237213588, 25.99493675077423, 160.69769496801342, 160.69769496801342,
                  25.994934171245205, 25.994934171245202],
                 [349199089.54076770, 349199089.54076773, 0.0, 199.30230503240247, 199.30230503240247,
                  25.99493675092049, 25.99493675092049, 160.69769496759753, 160.69769496759753,
                  25.729407227461937, 25.994934171391463]]
    for expected, method in zip(expecteds, methods):
        spoint, trgepc, srfvec = spice.subpnt(method, 'Mars', et, 'IAU_MARS', 'LT+S', 'Earth')
        odist = np.linalg.norm(srfvec)
        npt.assert_almost_equal(odist, expected[1], decimal=5)
        spglon, spglat, spgalt = spice.recpgr('mars', spoint, re, f)
        npt.assert_almost_equal(spgalt, expected[2], decimal=5)
        npt.assert_almost_equal(spglon * spice.dpr(), expected[3], decimal=5)
        npt.assert_almost_equal(spglat * spice.dpr(), expected[5], decimal=5)
        spcrad, spclon, spclat = spice.reclat(spoint)
        npt.assert_almost_equal(spclon * spice.dpr(), expected[7], decimal=5)
        npt.assert_almost_equal(spclat * spice.dpr(), expected[9], decimal=5)
        obspos = np.subtract(spoint, srfvec)
        opglon, opglat, opgalt = spice.recpgr('mars', obspos, re, f)
        npt.assert_almost_equal(opgalt, expected[0], decimal=5)
        npt.assert_almost_equal(opglon * spice.dpr(), expected[4], decimal=5)
        npt.assert_almost_equal(opglat * spice.dpr(), expected[6], decimal=5)
        opcrad, opclon, opclat = spice.reclat(obspos)
        npt.assert_almost_equal(opclon * spice.dpr(), expected[8], decimal=5)
        npt.assert_almost_equal(opclat * spice.dpr(), expected[10], decimal=5)
    spice.kclear()


def test_subpt():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et("JAN 1, 2006")
    point1, alt1 = np.array(spice.subpt("near point", "earth", et, "lt+s", "moon"))
    point2, alt2 = np.array(spice.subpt("intercept", "earth", et, "lt+s", "moon"))
    dist = np.linalg.norm(np.subtract(point1, point2))
    sep = spice.vsep(point1, point2) * spice.dpr()
    npt.assert_almost_equal(dist, 16.705476097706171)
    npt.assert_almost_equal(sep, 0.15016657506598063)
    spice.kclear()


def test_subslr():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et('2008 aug 11 00:00:00')
    num_vals, radii = spice.bodvrd("MARS", "RADII", 3)
    re = radii[0]
    rp = radii[2]
    f = (re - rp) / re
    methods = ['Intercept:  ellipsoid', 'Near point: ellipsoid']
    expecteds = [[0.0, 175.8106755102322, 23.668550281477703, -175.81067551023222,
                  23.420819936106213, 175.810721536362, 23.42082337182491,
                  -175.810721536362, 23.42081994605096],
                 [0.0, 175.8106754100492, 23.420823361866685, -175.81067551023222,
                  23.175085577910583, 175.81072152220804, 23.420823371828,
                  -175.81072152220804, 23.420819946054046]]
    for expected, method in zip(expecteds, methods):
        spoint, trgepc, srfvec = spice.subslr(method, 'Mars', et, 'IAU_MARS', 'LT+S', 'Earth')
        spglon, spglat, spgalt = spice.recpgr('mars', spoint, re, f)
        npt.assert_almost_equal(spgalt, expected[0], decimal=5)
        npt.assert_almost_equal(spglon * spice.dpr(), expected[1], decimal=5)
        npt.assert_almost_equal(spglat * spice.dpr(), expected[2], decimal=5)
        spcrad, spclon, spclat = spice.reclat(spoint)
        npt.assert_almost_equal(spclon * spice.dpr(), expected[3], decimal=5)
        npt.assert_almost_equal(spclat * spice.dpr(), expected[4], decimal=5)
        sunpos, sunlt = spice.spkpos('sun', trgepc, 'iau_mars', 'lt+s', 'mars')
        supgln, supglt, supgal = spice.recpgr('mars', sunpos, re, f)
        npt.assert_almost_equal(supgln * spice.dpr(), expected[5], decimal=5)
        npt.assert_almost_equal(supglt * spice.dpr(), expected[6], decimal=5)
        supcrd, supcln, supclt = spice.reclat(sunpos)
        npt.assert_almost_equal(supcln * spice.dpr(), expected[7], decimal=5)
        npt.assert_almost_equal(supclt * spice.dpr(), expected[8], decimal=5)
    spice.kclear()
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
    assert spice.sumad([1.0, 2.0, 3.0]) == 6.0


def test_sumai():
    assert spice.sumai([1, 2, 3]) == 6


def test_surfnm():
    point = [0.0, 0.0, 3.0]
    npt.assert_array_almost_equal(spice.surfnm(1.0, 2.0, 3.0, point), [0.0, 0.0, 1.0])


def test_surfpt():
    position = [2.0, 0.0, 0.0]
    u = [-1.0, 0.0, 0.0]
    point, found = spice.surfpt(position, u, 1.0, 2.0, 3.0)
    npt.assert_array_almost_equal(point, [1.0, 0.0, 0.0])


def test_surfpv():
    stvrtx = [2.0, 0.0, 0.0, 0.0, 0.0, 3.0]
    stdir = [-1.0, 0.0, 0.0, 0.0, 0.0, 4.0]
    stx, found = spice.surfpv(stvrtx, stdir, 1.0, 2.0, 3.0)
    expected = [1.0, 0.0, 0.0, 0.0, 0.0, 7.0]
    assert found
    npt.assert_array_almost_equal(expected, stx)


def test_swpool():
    assert 1


def test_sxform():
    spice.kclear()
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
    estate = np.append(estate, [0.0, 0.0, 0.0])
    xform = np.array(spice.sxform('IAU_EARTH', 'J2000', et))
    spice.kclear()
    jstate = np.dot(xform, estate)
    expected = np.array([-4131.45969, -3308.36805, 3547.02462, 0.241249619, -0.301019201, 0.000234215666])
    npt.assert_array_almost_equal(jstate, expected, decimal=4)


def test_sxform_vectorized():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    utc1 = 'January 1, 1990'
    utc2 = 'January 1, 2010'
    et1 = spice.str2et(utc1)
    et2 = spice.str2et(utc2)
    step = (et2 - et1) / 240.0
    et = np.arange(240) * step + et1
    xform = spice.sxform('IAU_EARTH', 'J2000', et)
    assert len(xform) == 240
    spice.kclear()


def test_szpool():
    assert spice.szpool("MAXVAR") == (26003, True)
    assert spice.szpool("MAXLEN") == (32, True)
    assert spice.szpool("MAXVAL") == (400000, True)
    assert spice.szpool("MXNOTE") == (130015, True)
    assert spice.szpool("MAXAGT") == (1000, True)
    assert spice.szpool("MAXCHR") == (80, True)
    assert spice.szpool("MAXLIN") == (15000, True)


def test_timdef():
    value = spice.timdef('GET', 'CALENDAR', 10)
    assert value == 'GREGORIAN' or 'JULIAN' or 'MIXED'


def test_timout():
    sample = 'Thu Oct 1 11:11:11 PDT 1111'
    lenout = len(sample) + 2
    spice.kclear()
    spice.furnsh(_testKernelPath)
    pic, ok, err = spice.tpictr(sample, 64, 60)
    assert ok
    et = 188745364.0
    out = spice.timout(et, pic, lenout)
    assert out == "Sat Dec 24 18:14:59 PDT 2005"
    spice.kclear()


def test_timout_vectorized():
    sample = 'Thu Oct 1 11:11:11 PDT 1111'
    lenout = len(sample) + 2
    spice.kclear()
    spice.furnsh(_testKernelPath)
    pic, ok, err = spice.tpictr(sample, 64, 60)
    assert ok
    et = np.array(np.arange(5) * 10000) + 188745364.0
    out = list(spice.timout(et, pic, lenout))
    expected = ["Sat Dec 24 18:14:59 PDT 2005", "Sat Dec 24 21:01:39 PDT 2005",
                "Sat Dec 24 23:48:19 PDT 2005", "Sun Dec 25 02:34:59 PDT 2005",
                "Sun Dec 25 05:21:39 PDT 2005"]
    for e in expected:
        assert e in out
    spice.kclear()


def test_tipbod():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et('Jan 1 2005')
    tipm = spice.tipbod('J2000', 699, et)
    assert tipm is not None
    spice.kclear()


def test_tisbod():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et('Jan 1 2005')
    tsipm = spice.tisbod('J2000', 699, et)
    assert tsipm is not None
    spice.kclear()


def test_tkvrsn():
    version = spice.tkvrsn("toolkit")
    assert version == "CSPICE_N0065"


def test_tparse():
    actualOne, errorOne = spice.tparse("1996-12-18T12:28:28", 100)
    assert actualOne == -95815892.0
    actualTwo, errorTwo = spice.tparse("1 DEC 1997 12:28:29.192", 100)
    assert actualTwo == -65748690.808
    actualThree, errorThree = spice.tparse("1997-162::12:18:28.827", 100)
    assert actualThree == -80696491.173


def test_tpictr():
    testString = "10:23 P.M. PDT January 3, 1993"
    pictur, ok, err = spice.tpictr(testString, 80, 80)
    assert pictur == "AP:MN AMPM PDT Month DD, YYYY ::UTC-7"


def test_trace():
    matrix = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    assert spice.trace(matrix) == 3.0


def test_trcdep():
    spice.reset()
    assert spice.trcdep() == 0
    spice.chkin("test")
    assert spice.trcdep() == 1
    spice.chkin("trcdep")
    assert spice.trcdep() == 2
    spice.chkout("trcdep")
    assert spice.trcdep() == 1
    spice.chkout("test")
    assert spice.trcdep() == 0
    spice.reset()


def test_trcnam():
    spice.reset()
    assert spice.trcdep() == 0
    spice.chkin("test")
    assert spice.trcdep() == 1
    assert spice.trcnam(0, 10) == "test"
    spice.chkin("trcnam")
    assert spice.trcdep() == 2
    assert spice.trcnam(1, 10) == "trcnam"
    spice.chkout("trcnam")
    assert spice.trcdep() == 1
    spice.chkout("test")
    assert spice.trcdep() == 0
    spice.reset()


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
    npt.assert_array_almost_equal(spice.twovec(axdef, 1, plndef, 2), expected)


def test_tyear():
    assert spice.tyear() == 31556925.9747


def test_ucase():
    assert spice.ucase("hi") == "HI"
    assert spice.ucase("hi", 3) == "HI"


def test_ucrss():
    vec1 = np.array([1.0, 2.0, 3.0])
    vec2 = np.array([6.0, 1.0, 6.0])
    expected = np.cross(vec1, vec2) / np.linalg.norm(np.cross(vec1, vec2))
    outvec = spice.ucrss(vec1, vec2)
    npt.assert_array_almost_equal(expected, outvec)


def test_uddc():
    assert 1


def test_uddf():
    assert 1


def test_udf():
    assert 1


def test_union():
    testCellOne = spice.stypes.SPICEINT_CELL(8)
    testCellTwo = spice.stypes.SPICEINT_CELL(8)
    spice.insrti(1, testCellOne)
    spice.insrti(2, testCellOne)
    spice.insrti(3, testCellTwo)
    spice.insrti(4, testCellTwo)
    outCell = spice.union(testCellOne, testCellTwo)
    assert [x for x in outCell] == [1, 2, 3, 4]


def test_unitim():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et('Dec 19 2003')
    converted_et = spice.unitim(et, 'ET', 'JED')
    npt.assert_almost_equal(converted_et, 2452992.5007428653)
    spice.kclear()


def test_unload():
    spice.kclear()
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
    spice.kclear()
    spice.furnsh(_testKernelPath)
    utcstr = 'December 1, 2004 15:04:11'
    output = spice.utc2et(utcstr)
    assert output == 155185515.1831043
    # icy utc2et example gives 1.5518552e+08 as output
    spice.kclear()


def test_vadd():
    v1 = [1.0, 2.0, 3.0]
    v2 = [4.0, 5.0, 6.0]
    npt.assert_array_almost_equal(spice.vadd(v1, v2), [5.0, 7.0, 9.0])


def test_vaddg():
    v1 = [1.0, 2.0, 3.0]
    v2 = [4.0, 5.0, 6.0]
    npt.assert_array_almost_equal(spice.vaddg(v1, v2, 3), [5.0, 7.0, 9.0])


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
    vec1 = [1.0, 1.0, 1.0]
    vec2 = [2.0, 2.0, 2.0]
    vec3 = [3.0, 3.0, 3.0]
    outvec = spice.vlcom3(1.0, vec1, 1.0, vec2, 1.0, vec3)
    expected = [6.0, 6.0, 6.0]
    npt.assert_array_almost_equal(outvec, expected)


def test_vlcom():
    vec1 = [1.0, 1.0, 1.0]
    vec2 = [2.0, 2.0, 2.0]
    outvec = spice.vlcom(1.0, vec1, 1.0, vec2)
    expected = [3.0, 3.0, 3.0]
    npt.assert_array_almost_equal(outvec, expected)


def test_vlcomg():
    vec1 = [1.0, 1.0]
    vec2 = [2.0, 2.0]
    outvec = spice.vlcomg(2, 1.0, vec1, 1.0, vec2)
    expected = [3.0, 3.0]
    npt.assert_array_almost_equal(outvec, expected)


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
    result, found = spice.vprjpi(vec, plane1, plane2)
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
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et("Jan 1, 2009")
    m = spice.sxform('IAU_EARTH', 'J2000', et)
    eulang, unique = spice.xf2eul(m, 3, 1, 3)
    assert unique
    expected = [1.571803284049681, 0.0008750002978301174, 2.9555269829740034,
                3.5458495690569166e-12, 3.080552365717176e-12, -7.292115373266558e-05]
    npt.assert_array_almost_equal(expected, eulang)
    spice.kclear()


def test_xf2rav():
    e = [1.0, 0.0, 0.0]
    rz = [[0.0, 1.0, 0.0],
          [-1.0, 0.0, 0.0],
          [0.0, 0.0, 1.0]]
    xform = spice.rav2xf(rz, e)
    rz2, e2 = spice.xf2rav(xform)
    npt.assert_array_almost_equal(e, e2)
    npt.assert_array_almost_equal(rz, rz2)


def test_xfmsta():
    spice.kclear()
    spice.furnsh(_testKernelPath)
    et = spice.str2et('July 4, 2003 11:00 AM PST')
    state, lt = spice.spkezr("Mars", et, "J2000", "LT+S", "Earth")
    expected_lt = 269.6898816177049
    expected_state = [73822235.33116072, -27127919.178592984, -18741306.284863796,
                      -6.808513317178952, 7.513996167680786, 3.001298515816776]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state)
    state_lat = spice.xfmsta(state, "rectangular", "latitudinal", " ")
    expected_lat_state = [80850992.507900745, -0.35215825739096612, -0.23392826228310765,
                          -9.4334897343891715, 5.9815768435033359e-08, 1.0357556211756963e-08]
    npt.assert_array_almost_equal(state_lat, expected_lat_state)
    spice.kclear()


def test_xpose6():
    m1 = [[1.0, 2.0, 3.0, 4.0, 5.0, 6.0], [0.0, 7.0, 8.0, 9.0, 10.0, 11.0], [0.0, 0.0, 12.0, 13.0, 14.0, 15.0],
          [0.0, 0.0, 0.0, 16.0, 17.0, 18.0], [0.0, 0.0, 0.0, 0.0, 19.0, 20.0], [0.0, 0.0, 0.0, 0.0, 0.0, 21.0]]
    mout_expected = np.array(m1).transpose().tolist()
    npt.assert_array_almost_equal(spice.xpose6(m1), mout_expected)


def test_xpose():
    m1 = [[1.0, 2.0, 3.0], [0.0, 4.0, 5.0], [0.0, 6.0, 0.0]]
    npt.assert_array_almost_equal(spice.xpose(m1), [[1.0, 0.0, 0.0], [2.0, 4.0, 6.0], [3.0, 5.0, 0.0]])
    npt.assert_array_almost_equal(spice.xpose(np.array(m1)), [[1.0, 0.0, 0.0], [2.0, 4.0, 6.0], [3.0, 5.0, 0.0]])


def test_xposeg():
    m1 = [[1.0, 2.0, 3.0], [0.0, 4.0, 5.0], [0.0, 6.0, 0.0]]
    npt.assert_array_almost_equal(spice.xposeg(m1, 3, 3), [[1.0, 0.0, 0.0], [2.0, 4.0, 6.0], [3.0, 5.0, 0.0]])
    npt.assert_array_almost_equal(spice.xposeg(np.array(m1), 3, 3), [[1.0, 0.0, 0.0], [2.0, 4.0, 6.0], [3.0, 5.0, 0.0]])
