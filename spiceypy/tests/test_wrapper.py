"""
The MIT License (MIT)

Copyright (c) [2015-2020] [Andrew Annex]

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

import pytest
import spiceypy as spice
import pandas as pd
import numpy as np
import numpy.testing as npt
import os
from datetime import datetime, timezone

import spiceypy.utils.callbacks
from spiceypy.tests.gettestkernels import (
    download_kernels,
    CoreKernels,
    CassiniKernels,
    ExtraKernels,
    cleanup_cassini_kernels,
    cleanup_extra_kernels,
    cleanup_core_kernels,
    cwd,
)


def setup_module(module):
    download_kernels()


def test_appndc():
    test_cell = spice.cell_char(10, 10)
    spice.appndc("one", test_cell)
    spice.appndc("two", test_cell)
    spice.appndc("three", test_cell)
    assert test_cell[0] == "one"
    assert test_cell[1] == "two"
    assert test_cell[2] == "three"


def test_appndc2():
    test_cell = spice.Cell_Char(10, 10)
    spice.appndc("one", test_cell)
    spice.appndc("two", test_cell)
    spice.appndc("three", test_cell)
    assert test_cell[0] == "one"
    assert test_cell[1] == "two"
    assert test_cell[2] == "three"


def test_appndc_vectorized():
    test_cell = spice.cell_char(10, 10)
    spice.appndc(["one", "two", "three"], test_cell)
    assert test_cell[0] == "one"
    assert test_cell[1] == "two"
    assert test_cell[2] == "three"


def test_appndc_numpy():
    test_cell = spice.cell_char(10, 10)
    spice.appndc(np.array(["one", "two"])[0], test_cell)
    assert test_cell[0] == "one"


def test_appndc_vectorized_numpy():
    test_cell = spice.cell_char(10, 10)
    spice.appndc(np.array(["one", "two", "three"]), test_cell)
    assert test_cell[0] == "one"
    assert test_cell[1] == "two"
    assert test_cell[2] == "three"


def test_appndc_vectorized_pandas():
    test_cell = spice.cell_char(10, 10)
    spice.appndc(pd.Series(["one", "two", "three"]), test_cell)
    assert test_cell[0] == "one"
    assert test_cell[1] == "two"
    assert test_cell[2] == "three"


def test_appndd():
    test_cell = spice.cell_double(8)
    spice.appndd(1.0, test_cell)
    spice.appndd(2.0, test_cell)
    spice.appndd(3.0, test_cell)
    assert [x for x in test_cell] == [1.0, 2.0, 3.0]


def test_appndd_vectorized():
    test_cell = spice.cell_double(8)
    spice.appndd([1.0, 2.0, 3.0], test_cell)
    assert [x for x in test_cell] == [1.0, 2.0, 3.0]


def test_appndi():
    test_cell = spice.cell_int(8)
    spice.appndi(1, test_cell)
    spice.appndi(2, test_cell)
    spice.appndi(3, test_cell)
    assert [x for x in test_cell] == [1, 2, 3]


def test_appndi_vectorized():
    test_cell = spice.cell_int(8)
    spice.appndi([1, 2, 3], test_cell)
    assert [x for x in test_cell] == [1, 2, 3]


def test_axisar():
    axis = np.array([0.0, 0.0, 1.0])
    outmatrix = spice.axisar(axis, spice.halfpi())
    expected = np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    np.testing.assert_array_almost_equal(expected, outmatrix, decimal=6)


def test_b1900():
    assert spice.b1900() == 2415020.31352


def test_b1950():
    assert spice.b1950() == 2433282.42345905


def test_badkpv():
    spice.kclear()
    spice.pdpool("DTEST_VAL", [3.1415, 186.0, 282.397])
    assert not spice.badkpv("spiceypy BADKPV test", "DTEST_VAL", "=", 3, 1, "N")
    spice.clpool()
    assert not spice.expool("DTEST_VAL")
    spice.kclear()


def test_bltfrm():
    out_cell = spice.bltfrm(-1)
    assert out_cell.size >= 126


def test_bodc2n():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    assert spice.bodc2n(399) == "EARTH"
    assert spice.bodc2n(0) == "SOLAR SYSTEM BARYCENTER"
    spice.kclear()


def test_bodc2s():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    assert spice.bodc2s(399) == "EARTH"
    assert spice.bodc2s(0) == "SOLAR SYSTEM BARYCENTER"
    spice.kclear()


def test_boddef():
    spice.kclear()
    spice.boddef("Jebediah", 117)
    assert spice.bodc2n(117) == "Jebediah"
    spice.kclear()


def test_bodeul():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    # define body-fixed unit vectors
    xbf = [1.0, 0.0, 0.0]
    ybf = [0.0, 1.0, 0.0]
    zbf = [0.0, 0.0, 1.0]
    # get the reference rotation matrix from pxform at et=0.0
    ref_rotate = spice.pxform("IAU_VENUS", "J2000", 0.0)
    # transform bf vectors to inertial coordinates
    xin = spice.mxv(ref_rotate, xbf)
    yin = spice.mxv(ref_rotate, ybf)
    zin = spice.mxv(ref_rotate, zbf)
    # obtain reference RA and DEC of north pole
    ref_range, ref_ra, ref_dec = spice.recrad(zin)
    # compute location of node
    node = spice.ucrss(zbf, zin)
    # obtain reference angle of prime meridian
    xproj = spice.vdot(node, xin)
    yproj = spice.vdot(node, yin)
    ref_w = -np.arctan2(yproj, xproj)
    ref_lam = 0
    # hopefully obtain the same angles with call to bodeul at et=0.0
    ra, dec, w, lam = spice.bodeul(299, 0.0)
    npt.assert_almost_equal(ra, ref_ra, decimal=4)
    npt.assert_almost_equal(dec, ref_dec, decimal=4)
    npt.assert_almost_equal(w, ref_w, decimal=4)
    npt.assert_almost_equal(lam, ref_lam, decimal=4)
    spice.kclear()


def test_bodfnd():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    assert spice.bodfnd(599, "RADII")
    spice.kclear()


def test_bodn2c():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    assert spice.bodn2c("EARTH") == 399
    with pytest.raises(spice.stypes.SpiceyError):
        spice.bodn2c("U.S.S. Enterprise")
    spice.kclear()


def test_bods2c():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    assert spice.bods2c("EARTH") == 399
    with pytest.raises(spice.stypes.SpiceyError):
        spice.bods2c("U.S.S. Enterprise")
    spice.kclear()


def test_bodvar():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    radii = spice.bodvar(399, "RADII", 3)
    expected = np.array([6378.140, 6378.140, 6356.755])
    np.testing.assert_array_almost_equal(expected, radii, decimal=1)
    spice.kclear()


def test_bodvcd():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    dim, values = spice.bodvcd(399, "RADII", 3)
    assert dim == 3
    expected = np.array([6378.140, 6378.140, 6356.755])
    np.testing.assert_array_almost_equal(expected, values, decimal=1)
    spice.kclear()


def test_bodvrd():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    dim, values = spice.bodvrd("EARTH", "RADII", 3)
    assert dim == 3
    expected = np.array([6378.140, 6378.140, 6356.755])
    np.testing.assert_array_almost_equal(expected, values, decimal=1)
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
    assert spice.bschoc("OBETHE", 5, lenvals, array, order) == -1


def test_bschoc_numpy():
    array = np.array(["FEYNMAN", "BOHR", "EINSTEIN", "NEWTON", "GALILEO"])
    order = [1, 2, 0, 4, 3]
    lenvals = 10
    assert spice.bschoc("NEWTON", 5, lenvals, array, order) == 3
    assert spice.bschoc(np.array(["NEWTON", "_"])[0], 5, lenvals, array, order) == 3
    assert spice.bschoc("EINSTEIN", 5, lenvals, array, order) == 2
    assert spice.bschoc("GALILEO", 5, lenvals, array, order) == 4
    assert spice.bschoc("Galileo", 5, lenvals, array, order) == -1
    assert spice.bschoc("BETHE", 5, lenvals, array, order) == -1
    assert spice.bschoc(np.array(["nan", "_"])[0], 5, lenvals, array, order) == -1


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
    test_cell = spice.cell_double(8)
    assert spice.card(test_cell) == 0
    spice.appndd(1.0, test_cell)
    assert spice.card(test_cell) == 1
    spice.appndd(2.0, test_cell)
    assert spice.card(test_cell) == 2
    spice.appndd(3.0, test_cell)
    assert spice.card(test_cell) == 3


def test_ccifrm():
    frcode, frname, center = spice.ccifrm(2, 3000)
    assert frname == "ITRF93"
    assert frcode == 13000
    assert center == 399


def test_cgv2el():
    vec1 = [1.0, 1.0, 1.0]
    vec2 = [1.0, -1.0, 1.0]
    center = [-1.0, 1.0, -1.0]
    ellipse = spice.cgv2el(center, vec1, vec2)
    expected_s_major = [np.sqrt(2.0), 0.0, np.sqrt(2.0)]
    expected_s_minor = [0.0, np.sqrt(2.0), 0.0]
    expected_center = [-1.0, 1.0, -1.0]
    npt.assert_array_almost_equal(expected_center, ellipse.center)
    npt.assert_array_almost_equal(expected_s_major, ellipse.semi_major)
    npt.assert_array_almost_equal(expected_s_minor, ellipse.semi_minor)


def test_chbder():
    cp = [1.0, 3.0, 0.5, 1.0, 0.5, -1.0, 1.0]
    x2s = [0.5, 3.0]
    dpdxs = spice.chbder(cp, 6, x2s, 1.0, 3)
    npt.assert_array_almost_equal([-0.340878, 0.382716, 4.288066, -1.514403], dpdxs)


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
    frcode, frname = spice.cidfrm(501)
    assert frcode == 10023
    assert frname == "IAU_IO"
    frcode, frname = spice.cidfrm(399)
    assert frcode == 10013
    assert frname == "IAU_EARTH"
    frcode, frname = spice.cidfrm(301)
    assert frcode == 10020
    assert frname == "IAU_MOON"


def test_ckcls():
    # Spice crashes if ckcls detects nothing written to ck1
    spice.kclear()
    ck1 = os.path.join(cwd, "ckopenkernel.bc")
    if spice.exists(ck1):
        os.remove(ck1)  # pragma: no cover
    ifname = "Test CK type 1 segment created by cspice_ckw01"
    handle = spice.ckopn(ck1, ifname, 10)
    spice.ckw01(
        handle,
        1.0,
        10.0,
        -77701,
        "J2000",
        True,
        "Test type 1 CK segment",
        2 - 1,
        [1.1, 4.1],
        [[1.0, 1.0, 1.0, 1.0], [2.0, 2.0, 2.0, 2.0]],
        [[0.0, 0.0, 1.0], [0.0, 0.0, 2.0]],
    )

    spice.ckcls(handle)
    spice.kclear()
    assert spice.exists(ck1)
    if spice.exists(ck1):
        os.remove(ck1)  # pragma: no cover
    assert not spice.exists(ck1)


def test_ckcov():
    spice.kclear()
    spice.furnsh(CassiniKernels.cassSclk)
    ckid = spice.ckobj(CassiniKernels.cassCk)[0]
    cover = spice.ckcov(CassiniKernels.cassCk, ckid, False, "INTERVAL", 0.0, "SCLK")
    expected_intervals = [
        [267832537952.000000, 267839247264.000000],
        [267839256480.000000, 267867970464.000000],
        [267868006304.000000, 267876773792.000000],
    ]
    assert [
        [cover[i * 2], cover[i * 2 + 1]] for i in range(spice.wncard(cover))
    ] == expected_intervals
    spice.kclear()


def test_ckfrot():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(CassiniKernels.cassSclk)
    spice.furnsh(CassiniKernels.cassCk)
    spice.furnsh(CassiniKernels.cassIk)
    spice.furnsh(CassiniKernels.cassFk)
    spice.furnsh(CassiniKernels.cassPck)
    ckid = spice.ckobj(CassiniKernels.cassCk)[0]
    # aribtrary time covered by test ck kernel
    et = spice.str2et("2013-FEB-26 00:01:08.828")
    rotation, ref = spice.ckfrot(ckid, et)
    expected = np.array(
        [
            [-0.64399206, 0.48057295, 0.5952511],
            [-0.34110294, -0.87682328, 0.33886533],
            [0.68477954, 0.01518468, 0.72859208],
        ]
    )
    npt.assert_array_almost_equal(rotation, expected)
    assert ref == 1
    spice.kclear()


def test_ckgp():
    spice.kclear()
    spice.reset()
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(CassiniKernels.cassSclk)
    spice.furnsh(CassiniKernels.cassCk)
    spice.furnsh(CassiniKernels.cassIk)
    spice.furnsh(CassiniKernels.cassFk)
    spice.furnsh(CassiniKernels.cassPck)
    ckid = spice.ckobj(CassiniKernels.cassCk)[0]
    cover = spice.ckcov(CassiniKernels.cassCk, ckid, False, "INTERVAL", 0.0, "SCLK")
    cmat, clkout = spice.ckgp(ckid, cover[0], 256, "J2000")
    expected_cmat = [
        [0.5064665782997639365, -0.75794210739897316387, 0.41111478554891744963],
        [-0.42372128242505308071, 0.19647683351734512858, 0.88422685364733510927],
        [-0.7509672961490383436, -0.6220294331642198804, -0.22164725216433822652],
    ]
    npt.assert_array_almost_equal(cmat, expected_cmat)
    assert clkout == 267832537952.0
    spice.reset()
    spice.kclear()


def test_ckgpav():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(CassiniKernels.cassSclk)
    spice.furnsh(CassiniKernels.cassCk)
    spice.furnsh(CassiniKernels.cassIk)
    spice.furnsh(CassiniKernels.cassFk)
    spice.furnsh(CassiniKernels.cassPck)
    ckid = spice.ckobj(CassiniKernels.cassCk)[0]
    cover = spice.ckcov(CassiniKernels.cassCk, ckid, False, "INTERVAL", 0.0, "SCLK")
    cmat, avout, clkout = spice.ckgpav(ckid, cover[0], 256, "J2000")
    expected_cmat = [
        [0.5064665782997639365, -0.75794210739897316387, 0.41111478554891744963],
        [-0.42372128242505308071, 0.19647683351734512858, 0.88422685364733510927],
        [-0.7509672961490383436, -0.6220294331642198804, -0.22164725216433822652],
    ]
    expected_avout = [
        -0.00231258422150853885,
        -0.00190333614370416515,
        -0.00069657429072504716,
    ]
    npt.assert_array_almost_equal(cmat, expected_cmat)
    npt.assert_array_almost_equal(avout, expected_avout)
    assert clkout == 267832537952.0
    spice.kclear()


def test_cklpf():
    spice.kclear()
    spice.reset()
    cklpf = os.path.join(cwd, "cklpfkernel.bc")
    if spice.exists(cklpf):
        os.remove(cklpf)  # pragma: no cover
    ifname = "Test CK type 1 segment created by cspice_cklpf"
    handle = spice.ckopn(cklpf, ifname, 10)
    spice.ckw01(
        handle,
        1.0,
        10.0,
        -77701,
        "J2000",
        True,
        "Test type 1 CK segment",
        2 - 1,
        [1.1, 4.1],
        [[1.0, 1.0, 1.0, 1.0], [2.0, 2.0, 2.0, 2.0]],
        [[0.0, 0.0, 1.0], [0.0, 0.0, 2.0]],
    )
    spice.ckcls(handle)
    spice.kclear()
    handle = spice.cklpf(cklpf)
    spice.ckupf(handle)
    spice.ckcls(handle)
    spice.kclear()
    spice.reset()
    assert spice.exists(cklpf)
    if spice.exists(cklpf):
        os.remove(cklpf)  # pragma: no cover
    assert not spice.exists(cklpf)


def test_ckobj():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(CassiniKernels.cassSclk)
    ids = spice.ckobj(CassiniKernels.cassCk)
    assert len(ids) == 1
    spice.kclear()


def test_ckopn():
    # Spice crashes if ckcls detects nothing written to ck1
    spice.kclear()
    ck1 = os.path.join(cwd, "ckopenkernel.bc")
    if spice.exists(ck1):
        os.remove(ck1)  # pragma: no cover
    ifname = "Test CK type 1 segment created by cspice_ckw01"
    handle = spice.ckopn(ck1, ifname, 10)
    spice.ckw01(
        handle,
        1.0,
        10.0,
        -77701,
        "J2000",
        True,
        "Test type 1 CK segment",
        2 - 1,
        [1.1, 4.1],
        [[1.0, 1.0, 1.0, 1.0], [2.0, 2.0, 2.0, 2.0]],
        [[0.0, 0.0, 1.0], [0.0, 0.0, 2.0]],
    )

    spice.ckcls(handle)
    spice.kclear()
    assert spice.exists(ck1)
    if spice.exists(ck1):
        os.remove(ck1)  # pragma: no cover
    assert not spice.exists(ck1)


def test_ckupf():
    spice.kclear()
    spice.reset()
    handle = spice.cklpf(CassiniKernels.cassCk)
    spice.ckupf(handle)
    spice.ckcls(handle)
    spice.reset()
    spice.kclear()


def test_ckw01():
    spice.kclear()
    ck1 = os.path.join(cwd, "type1.bc")
    if spice.exists(ck1):
        os.remove(ck1)  # pragma: no cover
    INST = -77701
    MAXREC = 201
    SECPERTICK = 0.001
    SEGID = "Test type 1 CK segment"
    ifname = "Test CK type 1 segment created by cspice_ckw01"
    NCOMCH = 0
    REF = "J2000"
    SPACING_TICKS = 10.0
    SPACING_SECS = SPACING_TICKS * SECPERTICK
    RATE = 0.01
    handle = spice.ckopn(ck1, ifname, NCOMCH)
    init_size = os.path.getsize(ck1)
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
    spice.ckw01(
        handle,
        begtime,
        endtime,
        INST,
        REF,
        avflag,
        SEGID,
        MAXREC - 1,
        sclkdp,
        quats,
        av,
    )
    spice.ckcls(handle)
    end_size = os.path.getsize(ck1)
    assert end_size != init_size
    spice.kclear()
    if spice.exists(ck1):
        os.remove(ck1)  # pragma: no cover


def test_ckw02():
    spice.kclear()
    ck2 = os.path.join(cwd, "type2.bc")
    if spice.exists(ck2):
        os.remove(ck2)  # pragma: no cover
    INST = -77702
    MAXREC = 201
    SECPERTICK = 0.001
    SEGID = "Test type 2 CK segment"
    ifname = "Test CK type 2 segment created by cspice_ckw02"
    NCOMCH = 0
    REF = "J2000"
    SPACING_TICKS = 10.0
    SPACING_SECS = SPACING_TICKS * SECPERTICK
    RATE = 0.01
    handle = spice.ckopn(ck2, ifname, NCOMCH)
    init_size = os.path.getsize(ck2)
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
    spice.ckw02(
        handle,
        begtime,
        endtime,
        INST,
        REF,
        SEGID,
        MAXREC - 1,
        starts,
        stops,
        quats,
        av,
        rates,
    )
    spice.ckcls(handle)
    end_size = os.path.getsize(ck2)
    assert end_size != init_size
    spice.kclear()
    if spice.exists(ck2):
        os.remove(ck2)  # pragma: no cover


def test_ckw03():
    spice.kclear()
    ck3 = os.path.join(cwd, "type3.bc")
    if spice.exists(ck3):
        os.remove(ck3)  # pragma: no cover
    MAXREC = 201
    SECPERTICK = 0.001
    SEGID = "Test type 3 CK segment"
    ifname = "Test CK type 3 segment created by cspice_ckw03"
    SPACING_TICKS = 10.0
    SPACING_SECS = SPACING_TICKS * SECPERTICK
    RATE = 0.01
    handle = spice.ckopn(ck3, ifname, 0)
    init_size = os.path.getsize(ck3)
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
    starts = [sclkdp[2 * i] for i in range(99)]
    begtime = sclkdp[0]
    endtime = sclkdp[-1]
    spice.ckw03(
        handle,
        begtime,
        endtime,
        -77703,
        "J2000",
        True,
        SEGID,
        MAXREC - 1,
        sclkdp,
        quats,
        av,
        99,
        starts,
    )
    spice.ckcls(handle)
    end_size = os.path.getsize(ck3)
    assert end_size != init_size
    spice.kclear()
    if spice.exists(ck3):
        os.remove(ck3)  # pragma: no cover


def test_ckw05():
    spice.kclear()
    ck5 = os.path.join(cwd, "type5.bc")
    if spice.exists(ck5):
        os.remove(ck5)  # pragma: no cover
    # constants
    avflag = True
    epochs = np.arange(0.0, 2.0)
    inst = [-41000, -41001, -41002, -41003]
    segid = "CK type 05 test segment"
    # make type 1 data
    type0data = [
        [9.999e-1, -1.530e-4, -8.047e-5, -4.691e-4, 0.0, 0.0, 0.0, 0.0],
        [
            9.999e-1,
            -4.592e-4,
            -2.414e-4,
            -1.407e-3,
            -7.921e-10,
            -1.616e-7,
            -8.499e-8,
            -4.954e-7,
        ],
    ]
    type1data = [
        [9.999e-1, -1.530e-4, -8.047e-5, -4.691e-4],
        [9.999e-1, -4.592e-4, -2.414e-4, -1.407e-3],
    ]
    type2data = [
        [
            0.959,
            -0.00015309,
            -8.0476e-5,
            -0.00046913,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        [
            0.959,
            -0.00045928,
            -0.00024143,
            -0.0014073,
            -7.921e-10,
            -1.616e-7,
            -8.499e-8,
            -4.954e-7,
            3.234e-7,
            1.7e-7,
            9.91e-7,
            3.234e-7,
            1.7e-9,
            9.91e-9,
        ],
    ]
    type3data = [
        [0.959, -0.00015309, -8.0476e-05, -0.00046913, 0.0, 0.0, 0.0],
        [0.959, -0.00045928, -0.00024143, -0.0014073, 3.234e-7, 1.7e-7, 9.91e-7],
    ]
    # begin testing ckw05
    handle = spice.ckopn(ck5, " ", 0)
    init_size = os.path.getsize(ck5)
    # test subtype 0
    spice.ckw05(
        handle,
        0,
        15,
        epochs[0],
        epochs[-1],
        inst[0],
        "J2000",
        avflag,
        segid,
        epochs,
        type0data,
        1000.0,
        1,
        epochs,
    )
    # test subtype 1
    spice.ckw05(
        handle,
        1,
        15,
        epochs[0],
        epochs[-1],
        inst[1],
        "J2000",
        avflag,
        segid,
        epochs,
        type1data,
        1000.0,
        1,
        epochs,
    )
    # test subtype 2
    spice.ckw05(
        handle,
        2,
        15,
        epochs[0],
        epochs[-1],
        inst[2],
        "J2000",
        avflag,
        segid,
        epochs,
        type2data,
        1000.0,
        1,
        epochs,
    )
    # test subtype 3
    spice.ckw05(
        handle,
        3,
        15,
        epochs[0],
        epochs[-1],
        inst[3],
        "J2000",
        avflag,
        segid,
        epochs,
        type3data,
        1000.0,
        1,
        epochs,
    )
    spice.ckcls(handle)
    # test size
    end_size = os.path.getsize(ck5)
    assert end_size != init_size
    # try reading using ck kernel
    spice.furnsh(ck5)
    cmat, av, clk = spice.ckgpav(-41000, epochs[0] + 0.5, 1.0, "J2000")
    assert clk == pytest.approx(0.5)
    spice.kclear()
    if spice.exists(ck5):
        os.remove(ck5)  # pragma: no cover
    spice.kclear()


def test_stress_ckw05():
    for i in range(1000):
        test_ckw05()


def test_cleard():
    with pytest.raises(NotImplementedError):
        spice.cleard()


def test_clight():
    assert spice.clight() == 299792.458


def test_clpool():
    spice.kclear()
    spice.pdpool("TEST_VAR", [-666.0])
    value = spice.gdpool("TEST_VAR", 0, 1)
    assert len(value) == 1
    assert value[0] == -666.0
    spice.clpool()
    with pytest.raises(spice.stypes.SpiceyError):
        spice.gdpool("TEST_VAR", 0, 1)
    spice.kclear()


def test_cmprss():
    strings = ["ABC...DE.F...", "...........", ".. ..AB....CD"]
    assert spice.cmprss(".", 2, strings[0]) == "ABC..DE.F.."
    assert spice.cmprss(".", 3, strings[1]) == "..."
    assert spice.cmprss(".", 1, strings[2]) == ". .AB.CD"
    assert spice.cmprss(".", 3, strings[1]) == "..."
    assert spice.cmprss(".", 1, strings[2]) == ". .AB.CD"
    assert spice.cmprss(" ", 0, " Embe dde d -sp   a c  es   ") == "Embedded-spaces"


def test_cnmfrm():
    ioFrcode, ioFrname = spice.cnmfrm("IO")
    assert ioFrcode == 10023
    assert ioFrname == "IAU_IO"


def test_conics():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("Dec 25, 2007")
    state, ltime = spice.spkezr("Moon", et, "J2000", "NONE", "EARTH")
    dim, mu = spice.bodvrd("EARTH", "GM", 1)
    elts = spice.oscelt(state, et, mu[0])
    later = et + 7.0 * spice.spd()
    later_state = spice.conics(elts, later)
    state, ltime = spice.spkezr("Moon", later, "J2000", "NONE", "EARTH")
    spice.kclear()
    pert = np.array(later_state) - np.array(state)
    expected_pert = [
        -7.48885583081946242601e03,
        3.97608014470621128567e02,
        1.95744667259379639290e02,
        -3.61527427787390887026e-02,
        -1.27926899069508159812e-03,
        -2.01458906615054056388e-03,
    ]
    npt.assert_array_almost_equal(pert, expected_pert, decimal=5)


def test_convrt():
    assert spice.convrt(300.0, "statute_miles", "km") == 482.80320
    npt.assert_almost_equal(
        spice.convrt(1.0, "parsecs", "lightyears"), 3.2615638, decimal=6
    )

    npt.assert_almost_equal(
        spice.convrt([1.0, 2.0], "AU", "km"), [149597870.7, 299195741.4], decimal=0
    )


def test_copy():
    # SPICEINT_CELL; dtype=2
    out_cell = spice.bltfrm(-1)
    assert out_cell.size >= 126
    cell_copy = spice.copy(out_cell)
    assert cell_copy.size >= 126
    assert cell_copy is not out_cell
    assert cell_copy.dtype == 2
    # SPICECHAR_CELL; dtype=0
    cell_src = spice.cell_char(10, 10)
    tmpRtn = [spice.appndc("{}".format(i), cell_src) for i in range(5)]
    cell_copy = spice.copy(cell_src)
    assert cell_copy.dtype == 0
    assert cell_copy.size == cell_src.size
    assert cell_copy.card == cell_src.card
    assert cell_copy[:] == cell_src[:]
    assert cell_copy.length >= cell_src.length
    # SPICEDOUBLE_CELL; dtype=1
    cell_src = spice.cell_double(10)
    tmpRtn = [spice.appndd(float(i), cell_src) for i in range(8)]
    cell_copy = spice.copy(cell_src)
    assert cell_copy.dtype == 1
    assert cell_copy.size == cell_src.size
    assert cell_copy.card == cell_src.card
    assert cell_copy[:] == cell_src[:]
    # SPICEBOOLEAN_CELL; dtype=4
    cell_src = spice.cell_bool(9)
    with pytest.raises(NotImplementedError):
        spice.copy(cell_src)


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
    spice.kclear()
    # add TEST_VAR_CVPOOL
    spice.pdpool("TEST_VAR_CVPOOL", [-646.0])
    # establish check for TEST_VAR_CVPOOL
    spice.swpool("TEST_CVPOOL", 1, 16, ["TEST_VAR_CVPOOL"])
    # update TEST_VAR_CVPOOL
    spice.pdpool("TEST_VAR_CVPOOL", [565.0])
    # check for updated variable
    updated = spice.cvpool("TEST_CVPOOL")
    value = spice.gdpool("TEST_VAR_CVPOOL", 0, 1)
    assert len(value) == 1
    assert value[0] == 565.0
    spice.clpool()
    spice.kclear()
    assert updated is True


def test_cyllat():
    assert spice.cyllat(1.0, 180.0 * spice.rpd(), -1.0) == (
        np.sqrt(2),
        np.pi,
        -np.pi / 4,
    )


def test_cylrec():
    npt.assert_array_almost_equal(
        spice.cylrec(0.0, np.radians(33.0), 0.0), [0.0, 0.0, 0.0]
    )


def test_cylsph():
    a = np.array(spice.cylsph(1.0, np.deg2rad(180.0), 1.0))
    b = np.array([1.4142, np.deg2rad(180.0), np.deg2rad(45.0)])
    np.testing.assert_almost_equal(b, a, decimal=4)


def test_dafac():
    # Create new DAF using CKOPN
    spice.kclear()
    dafpath = os.path.join(cwd, "ex_dafac.bc")
    if spice.exists(dafpath):
        os.remove(dafpath)  # pragma: no cover
    # Open CK to get new DAF because DAFONW (Create DAF) is not available to CSPICE/spiceypy
    handle = spice.ckopn(dafpath, "TEST_ex_dafac", 140)
    assert handle is not None
    # Write some comments
    cmnts = ["a", "bc", "def", "ghij"]
    spice.dafac(handle, cmnts)
    # Use DAFCLS because CKCLS requires segments to be written before closing
    spice.dafcls(handle)
    assert not spice.failed()
    spice.kclear()
    spice.reset()
    # Ensure all those DAF comments now exist in the new DAF
    handle = spice.dafopr(dafpath)
    assert handle is not None
    # Get up to 20 comments ...
    nOut, cmntsOut, done = spice.dafec(handle, 20, 99)
    # ...  nOut will have actual number of comments
    assert nOut == 4
    assert cmntsOut[:4] == cmnts
    assert done
    assert 0 == max([len(cmnt) for cmnt in cmntsOut[4:]])
    spice.dafcls(handle)
    assert not spice.failed()
    spice.kclear()
    spice.reset()
    # Once more ...
    handle = spice.dafopr(dafpath)
    assert handle is not None
    # ... to get fewer than the total number of comments
    nOut, cmntsOut, done = spice.dafec(handle, 3, 99)
    assert nOut == 3
    assert not done
    spice.dafcls(handle)
    assert not spice.failed()
    spice.kclear()
    spice.reset()
    if spice.exists(dafpath):
        os.remove(dafpath)  # pragma: no cover


def test_dafbbs():
    spice.kclear()
    handle = spice.dafopr(CoreKernels.spk)
    spice.dafbbs(handle)
    found = spice.daffpa()
    assert found
    spice.dafcls(handle)
    spice.kclear()


def test_dafbfs():
    spice.kclear()
    handle = spice.dafopr(CoreKernels.spk)
    spice.dafbfs(handle)
    found = spice.daffna()
    assert found
    spice.dafcls(handle)
    spice.kclear()


def test_dafcls():
    spice.kclear()
    handle = spice.dafopr(CoreKernels.spk)
    spice.dafbfs(handle)
    found = spice.daffna()
    assert found
    spice.dafcls(handle)
    spice.kclear()


def test_dafcs():
    spice.kclear()
    handle = spice.dafopr(CoreKernels.spk)
    spice.dafbbs(handle)
    spice.dafcs(handle)
    found = spice.daffpa()
    assert found
    spice.dafcls(handle)
    spice.kclear()


def test_dafdc():
    spice.kclear()
    dafpath = os.path.join(cwd, "ex_dafdc.bc")
    if spice.exists(dafpath):
        os.remove(dafpath)  # pragma: no cover
    # Open CK to get new DAF because DAFONW (Create DAF) is not available to CSPICE/spiceypy
    handle = spice.ckopn(dafpath, "TEST_ex_dafdc", 140)
    assert handle is not None
    # Write some comments
    cmnts = ["a", "bc", "def", "ghij"]
    spice.dafac(handle, cmnts)
    # Use DAFCLS because CKCLS requires segments to be written before closing
    spice.dafcls(handle)
    assert not spice.failed()
    spice.kclear()
    spice.reset()
    # Open the DAF for reading
    handle = spice.dafopr(dafpath)
    assert handle is not None
    nOut, cmntsOut, done = spice.dafec(handle, 20, 99)
    # Confirm that the number of comments is greater than zero
    assert nOut > 0
    spice.dafcls(handle)
    assert not spice.failed()
    spice.kclear()
    spice.reset()
    # Delete the comments
    handle = spice.dafopw(dafpath)
    assert handle is not None
    spice.dafdc(handle)
    spice.dafcls(handle)
    assert not spice.failed()
    spice.kclear()
    spice.reset()
    # Confirm there are no more comments
    handle = spice.dafopr(dafpath)
    assert handle is not None
    nOut, cmntsOut, done = spice.dafec(handle, 20, 99)
    assert nOut == 0
    spice.dafcls(handle)
    assert not spice.failed()
    spice.kclear()
    spice.reset()
    if spice.exists(dafpath):
        os.remove(dafpath)  # pragma: no cover


def test_dafec():
    spice.kclear()
    handle = spice.dafopr(CoreKernels.spk)
    n, buffer, done = spice.dafec(handle, 13)
    assert n == 13
    assert buffer == [
        "; de405s.bsp LOG FILE",
        ";",
        "; Created 1997-12-19/18:07:31.00.",
        ";",
        "; BEGIN NIOSPK COMMANDS",
        "",
        "LEAPSECONDS_FILE    = /kernels/gen/lsk/naif0006.tls",
        "SPK_FILE            = de405s.bsp",
        "  SOURCE_NIO_FILE   = /usr2/nio/gen/de405.nio",
        "    BODIES          = 1 2 3 4 5 6 7 8 9 10 301 399 199 299 499",
        "    BEGIN_TIME      = CAL-ET 1997 JAN 01 00:01:02.183",
        "    END_TIME        = CAL-ET 2010 JAN 02 00:01:03.183",
        "",
    ]
    assert done is False
    spice.dafcls(handle)
    spice.kclear()


def test_daffna():
    spice.kclear()
    handle = spice.dafopr(CoreKernels.spk)
    spice.dafbfs(handle)
    found = spice.daffna()
    assert found
    spice.dafcls(handle)
    spice.kclear()


def test_daffpa():
    spice.kclear()
    handle = spice.dafopr(CoreKernels.spk)
    spice.dafbbs(handle)
    found = spice.daffpa()
    assert found
    spice.dafcls(handle)
    spice.kclear()


def test_dafgda():
    # not a very good test...
    spice.kclear()
    handle = spice.dafopr(CoreKernels.spk)
    elements = spice.dafgda(handle, 20, 20)
    assert elements == [0.0]
    spice.dafcls(handle)
    spice.kclear()


def test_dafgh():
    spice.kclear()
    handle = spice.dafopr(CoreKernels.spk)
    spice.dafbbs(handle)
    spice.dafcs(handle)
    searchHandle = spice.dafgh()
    assert searchHandle == handle
    spice.dafcls(handle)
    spice.kclear()


def test_dafgn():
    spice.kclear()
    handle = spice.dafopr(CoreKernels.spk)
    spice.dafbfs(handle)
    found = spice.daffna()
    assert found
    out = spice.dafgs(n=2)
    npt.assert_array_almost_equal(
        out, [-9.46511378160646408796e07, 3.15662463183953464031e08]
    )
    outname = spice.dafgn(100)
    assert outname == "DE-405"
    spice.dafcls(handle)
    spice.kclear()


def test_dafgs():
    spice.kclear()
    handle = spice.dafopr(CoreKernels.spk)
    spice.dafbfs(handle)
    found = spice.daffna()
    assert found
    out = spice.dafgs(n=2)
    npt.assert_array_almost_equal(
        out, [-9.46511378160646408796e07, 3.15662463183953464031e08]
    )
    spice.dafcls(handle)
    spice.kclear()


def test_dafgsstress():
    # this is to show that memory issue with dafgs is fixed.
    for i in range(500):
        test_dafgs()


def test_dafgsr():
    spice.reset()
    spice.kclear()
    # Open DAF
    # N.B. The SPK used must use the LTL-IEEE double byte-ordering and format
    # This should be de405s.bsp from the test kernel set
    handle = spice.dafopr(CoreKernels.spk)
    # get ND, NI (N.B. for SPKs, ND=2 and NI=6),
    # and first, last and free record numbers
    nd, ni, ifname, fward, bward, free = spice.dafrfr(handle)
    assert nd == 2 and ni == 6
    # Calculate Single Summary size
    ss = nd + ((ni + 1) >> 1)
    # Loop over Summary records
    while fward > 0:
        iRecno = fward
        # Get first three words at summary record (DAF record iRecno)
        # * drec(1) NEXT forward pointer to next summary record
        # * drec(2) PREV backward pointer (not used here)
        # * drec(3) NSUM Number of single summaries in this DAF record
        fward, bward, nSS = drec = map(int, spice.dafgsr(handle, iRecno, 1, 3))
        # There is only one summary record in de405s.bsp
        assert iRecno == 7 and fward == 0 and bward == 0 and nSS == 15
        # Set index to first word of first summary
        firstWord = 4
        # Set DAF record before daf421.bsp next summary record's first record (641)
        lastIEndWord = 1024
        for iSS in range(1, nSS + 1):
            # Get packed summary
            drec = spice.dafgsr(handle, iRecno, firstWord, firstWord + ss - 1)
            # Unpack summary
            dc, ic = spice.dafus(drec, nd, ni)
            iBody, iCenter, iFrame, iSPKtype, iStartWord, iEndWord = ic
            # SPK de405s.bsp ephemerides run from [1997 JAN 01 00:01:02.183 (TDB)] to [2010 JAN 02 00:01:03.183 (TDB)]
            npt.assert_array_almost_equal(
                dc, [-9.46511378160646408796e07, 3.15662463183953464031e08]
            )
            # Solar System body barycenters (IDs 1-10) centers are the Solar System Barycenter (ID=0)
            # All other bodies' centers (e.g. 301; Moon) are their systems barycenter (e.g. 3 Earth-Moon Barycenter)
            assert (iBody // 100) == iCenter
            # All de405s.bsp ephemerides are in the J2000 frame (ID 1), use Type 2 SPK records,
            # and start after the last record for the previous ephemeris
            assert iFrame == 1 and iSPKtype == 2 and (lastIEndWord + 1) == iStartWord
            # Set up for next pa through loop
            firstWord += ss
            lastIEndWord = iEndWord
        # There is only one summary record in de405s.bsp
        assert fward == 0
    # Cleanup
    spice.dafcls(handle)
    spice.reset()
    spice.kclear()


def test_dafopr():
    spice.kclear()
    handle = spice.dafopr(CoreKernels.spk)
    spice.dafbfs(handle)
    found = spice.daffna()
    assert found
    spice.dafcls(handle)
    spice.kclear()


def test_dafopw():
    spice.kclear()
    handle = spice.dafopw(CoreKernels.spk)
    spice.dafbfs(handle)
    found = spice.daffna()
    assert found
    spice.dafcls(handle)
    spice.kclear()


def test_dafps_dafrs():
    spice.kclear()
    dafpath = os.path.join(cwd, "ckopenkernel_dafps.bc")
    if spice.exists(dafpath):
        os.remove(dafpath)  # pragma: no cover
    ifname = "Test CK type 1 segment created by cspice_ckw01"
    handle = spice.ckopn(dafpath, ifname, 10)
    spice.ckw01(
        handle,
        1.0,
        10.0,
        -77701,
        "J2000",
        True,
        "Test type 1 CK segment",
        2 - 1,
        [1.1, 4.1],
        [[1.0, 1.0, 1.0, 1.0], [2.0, 2.0, 2.0, 2.0]],
        [[0.0, 0.0, 1.0], [0.0, 0.0, 2.0]],
    )

    spice.ckcls(handle)
    spice.kclear()
    # reload
    handle = spice.dafopw(dafpath)
    assert handle is not None
    # begin forward search
    spice.dafbfs(handle)
    found = spice.daffna()
    assert found
    out = spice.dafgs(n=124)
    dc, ic = spice.dafus(out, 2, 6)
    # change the id code and repack
    ic[0] = -1999
    ic[1] = -2999
    summ = spice.dafps(2, 6, dc, ic)
    spice.dafrs(summ)
    # finished.
    spice.dafcls(handle)
    spice.kclear()
    # reload the kernel and verify the ic's got updated
    handle = spice.dafopr(dafpath)
    assert handle is not None
    # begin forward search
    spice.dafbfs(handle)
    found = spice.daffna()
    assert found
    out = spice.dafgs(n=124)
    dc, ic = spice.dafus(out, 2, 6)
    assert ic[0] == -1999
    assert ic[1] == -2999
    # cleanup
    spice.dafcls(handle)
    spice.kclear()
    if spice.exists(dafpath):
        os.remove(dafpath)  # pragma: no cover


def test_dafrda():
    spice.reset()
    spice.kclear()
    # Open DAF
    # N.B. The SPK used must use the LTL-IEEE double byte-ordering and format
    # This should be de405s.bsp from the test kernel set
    handle = spice.dafopr(CoreKernels.spk)
    # get ND, NI (N.B. for SPKs, ND=2 and NI=6),
    # and first, last and free record numbers
    nd, ni, ifname, fward, bward, free = spice.dafrfr(handle)
    assert nd == 2 and ni == 6
    # Calculate Single Summary size
    ss = nd + ((ni + 1) >> 1)
    iRecno = fward
    # Get first three words at summary record (DAF record iRecno)
    # * drec(1) NEXT forward pointer to next summary record
    # * drec(2) PREV backward pointer (not used here)
    # * drec(3) NSUM Number of single summaries in this DAF record
    fward, bward, nSS = drec = map(int, spice.dafgsr(handle, iRecno, 1, 3))
    # There is only one summary record in de405s.bsp
    assert iRecno == 7 and fward == 0 and bward == 0 and nSS == 15
    # Set index to first word of first summary
    firstWord = 4
    # Set DAF word before first segments first word (641 for de405s.bsp)
    lastIEndWord = 1024
    # Loop over single summaries
    for iSS in range(int(nSS)):
        # Get packed summary
        drec = spice.dafgsr(handle, iRecno, firstWord, firstWord + ss - 1)
        # Unpack summary
        dc, ic = spice.dafus(drec, nd, ni)
        iBody, iCenter, iFrame, iSPKtype, iStartWord, iEndWord = ic
        # SPK de405s.bsp ephemerides run from [1997 JAN 01 00:01:02.183 (TDB)] to [2010 JAN 02 00:01:03.183 (TDB)]
        npt.assert_array_almost_equal(
            dc, [-9.46511378160646408796e07, 3.15662463183953464031e08]
        )
        # Solar System body barycenters (IDs 1-10) centers are the Solar System Barycenter (ID=0)
        # All other bodies' centers (e.g. 301; Moon) are their systems barycenter (e.g. 3 Earth-Moon Barycenter)
        assert (iBody // 100) == iCenter
        # All de405s.bsp ephemeris segments are in the J2000 frame (ID 1),
        # are Type 2 SPK segments, and start immediately after the last
        # word (lastIEndWord) for the previous segment
        assert iFrame == 1 and iSPKtype == 2 and (lastIEndWord + 1) == iStartWord
        # Get the four-word directory at the end of the segment
        (
            segmentInit,
            segmentIntlen,
            segmentRsize,
            segmentN,
        ) = segmentLast4 = spice.dafrda(handle, ic[5] - 3, ic[5])
        # Check segment word count (1+END-BEGIN) against directory word content
        # Type 2 SPK segment word count:
        # - A count of [segmentN] Chebyshev polynomial records @ RSIZE words per Cheby. poly. record
        # - A four-word directory at the end of the segment
        # So ((RSIZE * N) + 4) == (1 + END - BEGIN)
        # - cf. https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/spk.html#Type%202:%20Chebyshev%20%28position%20only%29
        assert (3 + (segmentRsize * segmentN)) == (ic[5] - ic[4])
        # Setup for next segment:  advance BEGIN word of next single summary
        firstWord += ss
        lastIEndWord = iEndWord
    # Cleanup
    spice.dafcls(handle)
    spice.reset()
    spice.kclear()


def test_dafrfr():
    spice.kclear()
    handle = spice.dafopr(CoreKernels.spk)
    nd, ni, ifname, fward, bward, free = spice.dafrfr(handle)
    spice.dafcls(handle)
    assert nd == 2
    assert ni == 6
    assert ifname == ""
    assert fward == 7
    assert bward == 7
    spice.kclear()


def test_dafus():
    spice.kclear()
    handle = spice.dafopr(CoreKernels.spk)
    spice.dafbfs(handle)
    found = spice.daffna()
    assert found
    out = spice.dafgs(n=124)
    dc, ic = spice.dafus(out, 2, 6)
    spice.dafcls(handle)
    npt.assert_array_almost_equal(
        dc, [-9.46511378160646408796e07, 3.15662463183953464031e08]
    )
    npt.assert_array_almost_equal(ic, [1, 0, 1, 2, 1025, 27164])
    spice.kclear()


def test_dasac_dasopr_dasec_dasdc():
    spice.kclear()
    daspath = os.path.join(cwd, "ex_dasac.das")
    if spice.exists(daspath):
        os.remove(daspath)  # pragma: no cover
    handle = spice.dasonw(daspath, "TEST", "ex_dasac", 140)
    assert handle is not None
    # write some comments
    spice.dasac(handle, ["spice", "naif", "python"])
    spice.dascls(handle)
    spice.kclear()
    spice.reset()
    # we wrote to the test kernel, now load it in read mode
    handle = spice.dasopr(daspath)
    assert handle is not None
    # check that dashfn points to the correct path
    assert spice.dashfn(handle) == daspath
    # extract out the comment, say we only want 3 things out
    n, comments, done = spice.dasec(handle, bufsiz=3)
    assert n == 3
    assert set(comments) == {"spice", "naif", "python"} & set(comments)
    # close the das file
    spice.dascls(handle)
    ###############################################
    # now test dasrfr
    handle = spice.dasopr(daspath)
    assert handle is not None
    idword, ifname, nresvr, nresvc, ncomr, ncomc = spice.dasrfr(handle)
    assert idword is not None
    assert idword == "DAS/TEST"
    assert ifname == "ex_dasac"
    assert nresvr == 0
    assert nresvc == 0
    assert ncomr == 140
    assert ncomc == 18
    # close the das file
    spice.dascls(handle)
    ###############################################
    # now reload the kernel and delete the commnets
    handle = spice.dasopw(daspath)
    assert handle is not None
    # delete the comments
    spice.dasdc(handle)
    # close the das file
    spice.dascls(handle)
    # open again for reading
    handle = spice.dasopr(daspath)
    assert handle is not None
    # extract out the comments, hopefully nothing
    n, comments, done = spice.dasec(handle)
    assert n == 0
    # close it again
    spice.dascls(handle)
    # done, so clean up
    if spice.exists(daspath):
        os.remove(daspath)  # pragma: no cover
    spice.kclear()


def test_dasopw_dascls_dasopr():
    spice.kclear()
    daspath = os.path.join(cwd, "ex_das.das")
    if spice.exists(daspath):
        os.remove(daspath)  # pragma: no cover
    handle = spice.dasonw(daspath, "TEST", daspath, 0)
    assert handle is not None
    spice.dascls(handle)
    handle = spice.dasopw(daspath)
    assert handle is not None
    spice.dascls(handle)
    handle = spice.dasopr(daspath)
    spice.dascls(handle)
    assert handle is not None
    if spice.exists(daspath):
        os.remove(daspath)  # pragma: no cover
    spice.kclear()


def test_dcyldr():
    output = spice.dcyldr(1.0, 0.0, 0.0)
    expected = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    npt.assert_array_almost_equal(output, expected)


def test_deltet():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    UTC_1997 = "Jan 1 1997"
    UTC_2004 = "Jan 1 2004"
    et_1997 = spice.str2et(UTC_1997)
    et_2004 = spice.str2et(UTC_2004)
    delt_1997 = spice.deltet(et_1997, "ET")
    delt_2004 = spice.deltet(et_2004, "ET")
    npt.assert_almost_equal(delt_1997, 62.1839353, decimal=6)
    npt.assert_almost_equal(delt_2004, 64.1839116, decimal=6)
    spice.kclear()


def test_det():
    m1 = np.array([[5.0, -2.0, 1.0], [0.0, 3.0, -1.0], [2.0, 0.0, 7.0]])
    expected = 103
    assert spice.det(m1) == expected


def test_dgeodr():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    size, radii = spice.bodvrd("EARTH", "RADII", 3)
    flat = (radii[0] - radii[2]) / radii[0]
    lon = 118.0 * spice.rpd()
    lat = 32.0 * spice.rpd()
    alt = 0.0
    spice.kclear()
    rec = spice.latrec(lon, lat, alt)
    output = spice.dgeodr(rec[0], rec[1], rec[2], radii[0], flat)
    expected = [
        [-0.25730624850202866, 0.41177607401581356, 0.0],
        [-0.019818463887750683, -0.012383950685377182, 0.0011247386599188864],
        [0.040768073853231314, 0.02547471988726025, 0.9988438330394612],
    ]
    npt.assert_array_almost_equal(output, expected)


def test_diags2():
    mat = [[1.0, 4.0], [4.0, -5.0]]
    diag, rot = spice.diags2(mat)
    expected_diag = [[3.0, 0.0], [0.0, -7.0]]
    expected_rot = [[0.89442719, -0.44721360], [0.44721360, 0.89442719]]
    npt.assert_array_almost_equal(diag, expected_diag)
    npt.assert_array_almost_equal(rot, expected_rot)


def test_diff():
    # SPICEINT_CELL
    test_cell_one = spice.cell_int(8)
    test_cell_two = spice.cell_int(8)
    spice.insrti(1, test_cell_one)
    spice.insrti(2, test_cell_one)
    spice.insrti(3, test_cell_one)
    spice.insrti(2, test_cell_two)
    spice.insrti(3, test_cell_two)
    spice.insrti(4, test_cell_two)
    out_cell = spice.diff(test_cell_one, test_cell_two)
    assert [x for x in out_cell] == [1]
    out_cell = spice.diff(test_cell_two, test_cell_one)
    assert [x for x in out_cell] == [4]
    # SPICECHAR_CELL
    test_cell_one = spice.cell_char(8, 8)
    test_cell_two = spice.cell_char(8, 8)
    spice.insrtc("1", test_cell_one)
    spice.insrtc("2", test_cell_one)
    spice.insrtc("3", test_cell_one)
    spice.insrtc("2", test_cell_two)
    spice.insrtc("3", test_cell_two)
    spice.insrtc("4", test_cell_two)
    out_cell = spice.diff(test_cell_one, test_cell_two)
    assert [x for x in out_cell] == ["1"]
    out_cell = spice.diff(test_cell_two, test_cell_one)
    assert [x for x in out_cell] == ["4"]
    # SPICEDOUBLE_CELL
    test_cell_one = spice.cell_double(8)
    test_cell_two = spice.cell_double(8)
    spice.insrtd(1.0, test_cell_one)
    spice.insrtd(2.0, test_cell_one)
    spice.insrtd(3.0, test_cell_one)
    spice.insrtd(2.0, test_cell_two)
    spice.insrtd(3.0, test_cell_two)
    spice.insrtd(4.0, test_cell_two)
    out_cell = spice.diff(test_cell_one, test_cell_two)
    assert [x for x in out_cell] == [1.0]
    out_cell = spice.diff(test_cell_two, test_cell_one)
    assert [x for x in out_cell] == [4.0]
    # SPICEBOOLEAN_CELL; dtype=4
    test_cell_one = spice.cell_bool(9)
    test_cell_two = spice.cell_bool(9)
    with pytest.raises(NotImplementedError):
        spice.diff(test_cell_one, test_cell_two)


def test_dlabfs():
    spice.kclear()
    handle = spice.dasopr(ExtraKernels.phobosDsk)
    current = spice.dlabfs(handle)
    assert current is not None
    assert current.dsize == 1300
    with pytest.raises(spice.stypes.SpiceyError):
        next = spice.dlafns(handle, current)
    spice.dascls(handle)
    spice.kclear()


def test_dlabbs():
    spice.kclear()
    handle = spice.dasopr(ExtraKernels.phobosDsk)
    current = spice.dlabbs(handle)
    assert current is not None
    assert current.dsize == 1300
    with pytest.raises(spice.stypes.SpiceyError):
        prev = spice.dlafps(handle, current)
    spice.dascls(handle)
    spice.kclear()


def test_dlatdr():
    output = spice.dlatdr(1.0, 0.0, 0.0)
    expected = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
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
    spice.furnsh(CoreKernels.testMetaKernel)
    n, radii = spice.bodvrd("MARS", "RADII", 3)
    re = radii[0]
    rp = radii[2]
    f = (re - rp) / re
    output = spice.dpgrdr("Mars", 90.0 * spice.rpd(), 45 * spice.rpd(), 300, re, f)
    expected = [
        [0.25464790894703276, -0.5092958178940655, -0.0],
        [-0.002629849831988239, -0.0013149249159941194, 1.5182979166821334e-05],
        [0.004618598844358383, 0.0023092994221791917, 0.9999866677515724],
    ]
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
    expected = [[-1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 1.0]]
    npt.assert_array_almost_equal(output, expected)


def test_drdgeo():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    size, radii = spice.bodvrd("EARTH", "RADII", 3)
    flat = (radii[0] - radii[2]) / radii[0]
    lon = 118.0 * spice.rpd()
    lat = 32.0 * spice.rpd()
    alt = 0.0
    spice.kclear()
    output = spice.drdgeo(lon, lat, alt, radii[0], flat)
    expected = [
        [-4780.329375996193, 1580.5982261675397, -0.3981344650201568],
        [-2541.7462156656084, -2972.6729150327574, 0.7487820251299121],
        [0.0, 5387.9427815962445, 0.5299192642332049],
    ]
    npt.assert_array_almost_equal(output, expected)


def test_drdlat():
    output = spice.drdlat(1.0, 90.0 * spice.rpd(), 0.0)
    expected = [[0.0, -1.0, -0.0], [1.0, 0.0, -0.0], [0.0, 0.0, 1.0]]
    npt.assert_array_almost_equal(output, expected)


def test_drdpgr():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    n, radii = spice.bodvrd("MARS", "RADII", 3)
    re = radii[0]
    rp = radii[2]
    f = (re - rp) / re
    output = spice.drdpgr("Mars", 90.0 * spice.rpd(), 45 * spice.rpd(), 300, re, f)
    expected = [
        [-2620.6789148181783, 0.0, 0.0],
        [0.0, 2606.460468253308, -0.7071067811865476],
        [-0.0, 2606.460468253308, 0.7071067811865475],
    ]
    npt.assert_array_almost_equal(output, expected)
    spice.kclear()


def test_drdsph():
    output = spice.drdsph(1.0, np.pi / 2, np.pi)
    expected = [[-1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, -1.0, 0.0]]
    npt.assert_array_almost_equal(output, expected)


def test_dskgtl_dskstl():
    SPICE_DSK_KEYXFR = 1
    assert spice.dskgtl(SPICE_DSK_KEYXFR) == pytest.approx(1.0e-10)
    spice.dskstl(SPICE_DSK_KEYXFR, 1.0e-8)
    assert spice.dskgtl(SPICE_DSK_KEYXFR) == pytest.approx(1.0e-8)
    spice.dskstl(SPICE_DSK_KEYXFR, 1.0e-10)
    assert spice.dskgtl(SPICE_DSK_KEYXFR) == pytest.approx(1.0e-10)


def test_dskobj_dsksrf():
    spice.reset()
    spice.kclear()
    bodyids = spice.dskobj(ExtraKernels.phobosDsk)
    assert 401 in bodyids
    srfids = spice.dsksrf(ExtraKernels.phobosDsk, 401)
    assert 401 in srfids
    spice.kclear()
    spice.reset()


def test_dskopn_dskcls():
    spice.kclear()
    dskpath = os.path.join(cwd, "TEST.dsk")
    if spice.exists(dskpath):
        os.remove(dskpath)  # pragma: no cover
    handle = spice.dskopn(dskpath, "TEST.DSK/NAIF/NJB/20-OCT-2006/14:37:00", 0)
    assert handle is not None
    spice.dskcls(handle)
    if spice.exists(dskpath):
        os.remove(dskpath)  # pragma: no cover
    spice.kclear()


def test_dskb02():
    spice.kclear()
    # open the dsk file
    handle = spice.dasopr(ExtraKernels.phobosDsk)
    # get the dladsc from the file
    dladsc = spice.dlabfs(handle)
    # test dskb02
    (
        nv,
        nump,
        nvxtot,
        vtxbds,
        voxsiz,
        voxori,
        vgrext,
        cgscal,
        vtxnpl,
        voxnpt,
        voxnpl,
    ) = spice.dskb02(handle, dladsc)
    # test results
    assert nv == 422
    assert nump == 840
    assert nvxtot == 8232
    assert cgscal == 7
    assert vtxnpl == 0
    assert voxnpt == 2744
    assert voxnpl == 3257
    assert voxsiz == pytest.approx(3.320691339664286)
    # cleanup
    spice.dascls(handle)
    spice.kclear()


def test_dskd02():
    spice.kclear()
    # open the dsk file
    handle = spice.dasopr(ExtraKernels.phobosDsk)
    # get the dladsc from the file
    dladsc = spice.dlabfs(handle)
    # Fetch the vertex
    values = spice.dskd02(handle, dladsc, 19, 0, 3)
    assert len(values) > 0
    npt.assert_almost_equal(
        values,
        [
            5.12656957900699912362e-16,
            -0.00000000000000000000e00,
            -8.37260000000000026432e00,
        ],
    )
    spice.dascls(handle)
    spice.kclear()


def test_dskgd():
    spice.kclear()
    # open the dsk file
    handle = spice.dasopr(ExtraKernels.phobosDsk)
    # get the dladsc from the file
    dladsc = spice.dlabfs(handle)
    # get dskdsc for target radius
    dskdsc = spice.dskgd(handle, dladsc)
    # test results
    assert dskdsc.surfce == 401
    assert dskdsc.center == 401
    assert dskdsc.dclass == 1
    assert dskdsc.dtype == 2
    assert dskdsc.frmcde == 10021
    assert dskdsc.corsys == 1
    npt.assert_almost_equal(dskdsc.corpar, np.zeros(10))
    assert dskdsc.co1min == pytest.approx(-3.141593)
    assert dskdsc.co1max == pytest.approx(3.141593)
    assert dskdsc.co2min == pytest.approx(-1.570796)
    assert dskdsc.co2max == pytest.approx(1.570796)
    assert dskdsc.co3min == pytest.approx(8.181895873588292)
    assert dskdsc.co3max == pytest.approx(13.89340000000111)
    assert dskdsc.start == pytest.approx(-1577879958.816059)
    assert dskdsc.stop == pytest.approx(1577880066.183913)
    # cleanup
    spice.dascls(handle)
    spice.kclear()


def test_dski02():
    spice.kclear()
    # open the dsk file
    handle = spice.dasopr(ExtraKernels.phobosDsk)
    # get the dladsc from the file
    dladsc = spice.dlabfs(handle)
    # Find the number of plates in the model
    # SPICE_DSK02_KWNP == 2
    num_plates = spice.dski02(handle, dladsc, 2, 0, 3)
    assert len(num_plates) > 0
    spice.dascls(handle)
    spice.kclear()


def test_dskn02():
    spice.kclear()
    # open the dsk file
    handle = spice.dasopr(ExtraKernels.phobosDsk)
    # get the dladsc from the file
    dladsc = spice.dlabfs(handle)
    # get the normal vector for first plate
    normal = spice.dskn02(handle, dladsc, 1)
    npt.assert_almost_equal(
        normal,
        [0.20813166897151150203, 0.07187012861854354118, -0.97545676120650637309],
    )
    spice.dascls(handle)
    spice.kclear()


def test_dskp02():
    spice.kclear()
    # open the dsk file
    handle = spice.dasopr(ExtraKernels.phobosDsk)
    # get the dladsc from the file
    dladsc = spice.dlabfs(handle)
    # get the first plate
    plates = spice.dskp02(handle, dladsc, 1, 2)
    npt.assert_almost_equal(plates[0], [1, 9, 2])
    npt.assert_almost_equal(plates[1], [1, 2, 3])
    spice.dascls(handle)
    spice.kclear()


def test_dskv02():
    spice.kclear()
    # open the dsk file
    handle = spice.dasopr(ExtraKernels.phobosDsk)
    # get the dladsc from the file
    dladsc = spice.dlabfs(handle)
    # read the vertices
    vrtces = spice.dskv02(handle, dladsc, 1, 1)
    npt.assert_almost_equal(
        vrtces[0],
        [
            5.12656957900699912362e-16,
            -0.00000000000000000000e00,
            -8.37260000000000026432e00,
        ],
    )
    spice.dascls(handle)
    spice.kclear()


def test_dskw02_dskrb2_dskmi2():
    spice.kclear()
    dskpath = os.path.join(cwd, "TESTdskw02.dsk")
    if spice.exists(dskpath):
        os.remove(dskpath)  # pragma: no cover
    # open the dsk file
    handle = spice.dasopr(ExtraKernels.phobosDsk)
    # get the dladsc from the file
    dladsc = spice.dlabfs(handle)
    # declare some variables
    finscl = 5.0
    corscl = 4
    center = 401
    surfid = 1
    dclass = 2
    frame = "IAU_PHOBOS"
    first = -50 * spice.jyear()
    last = 50 * spice.jyear()
    # stuff from spicedsk.h
    SPICE_DSK02_MAXVRT = 16000002 // 128  # divide to lower memory usage
    SPICE_DSK02_MAXPLT = 2 * (SPICE_DSK02_MAXVRT - 2)
    SPICE_DSK02_MAXVXP = SPICE_DSK02_MAXPLT // 2
    SPICE_DSK02_MAXCEL = 60000000 // 128  # divide to lower memory usage
    SPICE_DSK02_MXNVLS = SPICE_DSK02_MAXCEL + (SPICE_DSK02_MAXVXP // 2)
    SPICE_DSK02_MAXCGR = 100000 // 128  # divide to lower memory usage
    SPICE_DSK02_IXIFIX = SPICE_DSK02_MAXCGR + 7
    SPICE_DSK02_MAXNPV = 3 * (SPICE_DSK02_MAXPLT // 2) + 1
    SPICE_DSK02_SPAISZ = (
        SPICE_DSK02_IXIFIX
        + SPICE_DSK02_MAXVXP
        + SPICE_DSK02_MXNVLS
        + SPICE_DSK02_MAXVRT
        + SPICE_DSK02_MAXNPV
    )
    worksz = SPICE_DSK02_MAXCEL
    voxpsz = SPICE_DSK02_MAXVXP
    voxlsz = SPICE_DSK02_MXNVLS
    spaisz = SPICE_DSK02_SPAISZ
    # get verts, number from dskb02 test
    vrtces = spice.dskv02(handle, dladsc, 1, 422)
    # get plates, number from dskb02 test
    plates = spice.dskp02(handle, dladsc, 1, 840)
    # close the input kernel
    spice.dskcls(handle)
    spice.kclear()
    # open new dsk file
    handle = spice.dskopn(dskpath, "TESTdskw02.dsk/AA/29-SEP-2017", 0)
    # create spatial index
    spaixd, spaixi = spice.dskmi2(
        vrtces, plates, finscl, corscl, worksz, voxpsz, voxlsz, False, spaisz
    )
    # do stuff
    corsys = 1
    mncor1 = -spice.pi()
    mxcor1 = spice.pi()
    mncor2 = -spice.pi() / 2
    mxcor2 = spice.pi() / 2
    # Compute plate model radius bounds.
    corpar = np.zeros(10)
    mncor3, mxcor3 = spice.dskrb2(vrtces, plates, corsys, corpar)
    # Write the segment to the file
    spice.dskw02(
        handle,
        center,
        surfid,
        dclass,
        frame,
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
        vrtces,
        plates,
        spaixd,
        spaixi,
    )
    # Close the dsk file
    spice.dskcls(handle, optmiz=True)
    # cleanup
    if spice.exists(dskpath):
        os.remove(dskpath)  # pragma: no cover
    spice.kclear()


def test_dskx02():
    spice.kclear()
    # open the dsk file
    handle = spice.dasopr(ExtraKernels.phobosDsk)
    # get the dladsc from the file
    dladsc = spice.dlabfs(handle)
    # get dskdsc for target radius
    dskdsc = spice.dskgd(handle, dladsc)
    r = 2.0 * dskdsc.co3max
    # Produce a ray vertex
    vertex = spice.latrec(r, 0.0, 0.0)
    raydir = spice.vminus(vertex)
    plid, xpt, found = spice.dskx02(handle, dladsc, vertex, raydir)
    # test results
    assert found
    assert plid == 421
    npt.assert_almost_equal(xpt, [12.36679999999999957083, 0.0, 0.0])
    # cleanup
    spice.dascls(handle)
    spice.kclear()


def test_dskxsi():
    spice.kclear()
    # load kernels
    spice.furnsh(ExtraKernels.phobosDsk)
    # get handle
    dsk1, filtyp, source, handle = spice.kdata(0, "DSK", 256, 5, 256)
    # get the dladsc from the file
    dladsc = spice.dlabfs(handle)
    # get dskdsc for target radius
    dskdsc = spice.dskgd(handle, dladsc)
    target = spice.bodc2n(dskdsc.center)
    fixref = spice.frmnam(dskdsc.frmcde)
    r = 1.0e10
    vertex = spice.latrec(r, 0.0, 0.0)
    raydir = spice.vminus(vertex)
    srflst = [dskdsc.surfce]
    # call dskxsi
    xpt, handle, dladsc2, dskdsc2, dc, ic = spice.dskxsi(
        False, target, srflst, 0.0, fixref, vertex, raydir
    )
    # check output
    assert handle is not None
    assert ic[0] == 420
    assert dc[0] == pytest.approx(0.0)
    npt.assert_almost_equal(xpt, [12.36679999999999957083, 0.0, 0.0])
    spice.kclear()


def test_dskxv():
    spice.kclear()
    # load kernels
    spice.furnsh(ExtraKernels.phobosDsk)
    # get handle
    dsk1, filtyp, source, handle = spice.kdata(0, "DSK", 256, 5, 256)
    # get the dladsc from the file
    dladsc = spice.dlabfs(handle)
    # get dskdsc for target radius
    dskdsc = spice.dskgd(handle, dladsc)
    target = spice.bodc2n(dskdsc.center)
    fixref = spice.frmnam(dskdsc.frmcde)
    r = 1.0e10
    vertex = spice.latrec(r, 0.0, 0.0)
    raydir = spice.vminus(vertex)
    srflst = [dskdsc.surfce]
    # call dskxsi
    xpt, foundarray = spice.dskxv(
        False, target, srflst, 0.0, fixref, [vertex], [raydir]
    )
    # check output
    assert len(xpt) == 1
    assert len(foundarray) == 1
    assert foundarray[0]
    npt.assert_almost_equal(xpt[0], [12.36679999999999957083, 0.0, 0.0])
    spice.kclear()


def test_dskxv_2():
    spice.kclear()
    # load kernels
    spice.furnsh(ExtraKernels.phobosDsk)
    # get handle
    dsk1, filtyp, source, handle = spice.kdata(0, "DSK", 256, 5, 256)
    # get the dladsc from the file
    dladsc = spice.dlabfs(handle)
    # get dskdsc for target radius
    dskdsc = spice.dskgd(handle, dladsc)
    target = spice.bodc2n(dskdsc.center)
    fixref = spice.frmnam(dskdsc.frmcde)
    r = 1.0e10
    polmrg = 0.5
    latstp = 1.0
    lonstp = 2.0

    lon = -180.0
    lat = 90.0
    nlstep = 0
    nrays = 0
    verticies = []
    raydirs = []

    while lon <= 180.0:
        while nlstep <= 180.0:
            if lon == 180.0:
                lat = 90.0 - nlstep * latstp
            else:
                if nlstep == 0:
                    lat = 90.0 - polmrg
                elif nlstep == 180:
                    lat = -90.0 + polmrg
                else:
                    lat = 90.0 - nlstep * latstp
            vertex = spice.latrec(r, np.radians(lon), np.radians(lat))
            raydir = spice.vminus(vertex)
            verticies.append(vertex)
            raydirs.append(raydir)
            nrays += 1
            nlstep += 1
        lon += lonstp
        lat = 90.0
        nlstep = 0

    srflst = [dskdsc.surfce]
    # call dskxsi
    xpt, foundarray = spice.dskxv(
        False, target, srflst, 0.0, fixref, verticies, raydirs
    )
    # check output
    assert len(xpt) == 32761
    assert len(foundarray) == 32761
    assert foundarray.all()
    spice.kclear()


def test_dskz02():
    spice.kclear()
    # open the dsk file
    handle = spice.dasopr(ExtraKernels.phobosDsk)
    # get the dladsc from the file
    dladsc = spice.dlabfs(handle)
    # get vertex and plate counts
    nv, nplates = spice.dskz02(handle, dladsc)
    assert nv > 0
    assert nplates > 0
    spice.dascls(handle)
    spice.kclear()


def test_dsphdr():
    output = spice.dsphdr(-1.0, 0.0, 0.0)
    expected = [[-1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, -1.0, 0.0]]
    npt.assert_array_almost_equal(output, expected)


def test_dtpool():
    spice.kclear()
    lmpool_names = [
        "DELTET/DELTA_T_A",
        "DELTET/K",
        "DELTET/EB",
        "DELTET/M",
        "DELTET/DELTA_AT",
    ]
    lmpool_lens = [1, 1, 1, 2, 46]
    textbuf = [
        "DELTET/DELTA_T_A = 32.184",
        "DELTET/K = 1.657D-3",
        "DELTET/EB  = 1.671D-2",
        "DELTET/M = ( 6.239996 1.99096871D-7 )",
        "DELTET/DELTA_AT = ( 10, @1972-JAN-1",
        "                     11, @1972-JUL-1",
        "                     12, @1973-JAN-1",
        "                     13, @1974-JAN-1",
        "                     14, @1975-JAN-1",
        "                     15, @1976-JAN-1",
        "                     16, @1977-JAN-1",
        "                     17, @1978-JAN-1",
        "                     18, @1979-JAN-1",
        "                     19, @1980-JAN-1",
        "                     20, @1981-JUL-1",
        "                     21, @1982-JUL-1",
        "                     22, @1983-JUL-1",
        "                     23, @1985-JUL-1",
        "                     24, @1988-JAN-1",
        "                     25, @1990-JAN-1",
        "                     26, @1991-JAN-1",
        "                     27, @1992-JUL-1",
        "                     28, @1993-JUL-1",
        "                     29, @1994-JUL-1",
        "                     30, @1996-JAN-1",
        "                     31, @1997-JUL-1",
        "                     32, @1999-JAN-1 )",
    ]
    spice.lmpool(textbuf)
    for var, expectLen in zip(lmpool_names, lmpool_lens):
        n, vartype = spice.dtpool(var)
        assert expectLen == n
        assert vartype == "N"
    spice.kclear()


def test_ducrss():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    z_earth = [0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
    et = spice.str2et("Jan 1, 2009")
    trans = spice.sxform("IAU_EARTH", "J2000", et)
    z_j2000 = np.dot(np.array(trans), np.array(z_earth))
    state, ltime = spice.spkezr("Sun", et, "J2000", "LT+S", "Earth")
    z_new = spice.ducrss(state, z_j2000)
    z_expected = [
        -0.9798625180326394,
        -0.1996715076226282,
        0.0008572038510904833,
        4.453114222872359e-08,
        -2.1853106962531453e-07,
        -3.6140021238340607e-11,
    ]
    npt.assert_array_almost_equal(z_new, z_expected)
    spice.kclear()


def test_dvcrss():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    z_earth = [0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
    et = spice.str2et("Jan 1, 2009")
    trans = spice.sxform("IAU_EARTH", "J2000", et)
    z_j2000 = np.dot(np.array(trans), np.array(z_earth))
    state, ltime = spice.spkezr("Sun", et, "J2000", "LT+S", "Earth")
    z = spice.dvcrss(state, z_j2000)
    spice.kclear()
    expected = [
        -1.32672690582546606660e08,
        -2.70353812480484284461e07,
        1.16064793997540167766e05,
        5.12510726479525757782e00,
        -2.97732415336074147660e01,
        -4.10216496370272454969e-03,
    ]
    npt.assert_almost_equal(z, expected)


def test_dvdot():
    assert (
        spice.dvdot([1.0, 0.0, 1.0, 0.0, 1.0, 0.0], [0.0, 1.0, 0.0, 1.0, 0.0, 1.0])
        == 3.0
    )


def test_dvhat():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("Jan 1, 2009")
    state, ltime = spice.spkezr("Sun", et, "J2000", "LT+S", "Earth")
    x_new = spice.dvhat(state)
    spice.kclear()
    expected = [
        0.1834466376334262,
        -0.9019196633282948,
        -0.39100927360200305,
        2.0244976750658316e-07,
        3.4660106111045445e-08,
        1.5033141925267006e-08,
    ]
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
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("JAN 1 2009")
    state_e, eltime = spice.spkezr("EARTH", et, "J2000", "NONE", "SUN")
    state_m, mltime = spice.spkezr("MOON", et, "J2000", "NONE", "SUN")
    dsept = spice.dvsep(state_e, state_m)
    npt.assert_approx_equal(dsept, 3.8121194e-09)
    spice.kclear()


def test_edlimb():
    viewpt = [2.0, 0.0, 0.0]
    limb = spice.edlimb(np.sqrt(2), 2.0 * np.sqrt(2), np.sqrt(2), viewpt)
    expected_s_minor = [0.0, 0.0, -1.0]
    expected_s_major = [0.0, 2.0, 0.0]
    expected_center = [1.0, 0.0, 0.0]
    npt.assert_array_almost_equal(limb.center, expected_center)
    npt.assert_array_almost_equal(limb.semi_major, expected_s_major)
    npt.assert_array_almost_equal(limb.semi_minor, expected_s_minor)


def test_edterm():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("2007 FEB 3 00:00:00.000")
    # umbral
    trgepc, obspos, trmpts = spice.edterm(
        "UMBRAL", "SUN", "MOON", et, "IAU_MOON", "LT+S", "EARTH", 3
    )
    expected_trgepc = 223732863.86351674795
    expected_obspos = [
        394721.1024056578753516078,
        27265.11780063395417528227,
        -19069.08478859506431035697,
    ]
    expected_trmpts0 = [
        -1.53978381936825627463e02,
        -1.73056331949840728157e03,
        1.22893325627419600088e-01,
    ]
    expected_trmpts1 = [
        87.37506200891714058798,
        864.40670594653545322217,
        1504.56817899807947469526,
    ]
    expected_trmpts2 = [
        42.21324376177891224415,
        868.21134635239388899208,
        -1504.3223923468244720425,
    ]
    npt.assert_almost_equal(trgepc, expected_trgepc)
    npt.assert_array_almost_equal(obspos, expected_obspos)
    npt.assert_array_almost_equal(trmpts[0], expected_trmpts0)
    npt.assert_array_almost_equal(trmpts[1], expected_trmpts1)
    npt.assert_array_almost_equal(trmpts[2], expected_trmpts2)
    iluet0, srfvec0, phase0, solar0, emissn0 = spice.ilumin(
        "Ellipsoid", "MOON", et, "IAU_MOON", "LT+S", "EARTH", trmpts[0]
    )
    npt.assert_almost_equal(spice.dpr() * solar0, 90.269765819)
    iluet1, srfvec1, phase1, solar1, emissn1 = spice.ilumin(
        "Ellipsoid", "MOON", et, "IAU_MOON", "LT+S", "EARTH", trmpts[1]
    )
    npt.assert_almost_equal(spice.dpr() * solar1, 90.269765706)
    iluet2, srfvec2, phase2, solar2, emissn2 = spice.ilumin(
        "Ellipsoid", "MOON", et, "IAU_MOON", "LT+S", "EARTH", trmpts[2]
    )
    npt.assert_almost_equal(spice.dpr() * solar2, 90.269765730)
    # penumbral
    trgepc, obspos, trmpts = spice.edterm(
        "PENUMBRAL", "SUN", "MOON", et, "IAU_MOON", "LT+S", "EARTH", 3
    )
    expected_trmpts0 = [
        1.54019056755619715204e02,
        1.73055969989532059117e03,
        -1.23508409498995316844e-01,
    ]
    expected_trmpts1 = [
        -87.33436047798454637814,
        -864.41003834758112134296,
        -1504.56862757530461749411,
    ]
    expected_trmpts2 = [
        -42.17254722919552278881,
        -868.21467833235510624945,
        1504.32161075630597224517,
    ]
    npt.assert_almost_equal(trgepc, expected_trgepc)
    npt.assert_array_almost_equal(obspos, expected_obspos)
    npt.assert_array_almost_equal(trmpts[0], expected_trmpts0)
    npt.assert_array_almost_equal(trmpts[1], expected_trmpts1)
    npt.assert_array_almost_equal(trmpts[2], expected_trmpts2)
    iluet0, srfvec0, phase0, solar0, emissn0 = spice.ilumin(
        "Ellipsoid", "MOON", et, "IAU_MOON", "LT+S", "EARTH", trmpts[0]
    )
    npt.assert_almost_equal(spice.dpr() * solar0, 89.730234406)
    iluet1, srfvec1, phase1, solar1, emissn1 = spice.ilumin(
        "Ellipsoid", "MOON", et, "IAU_MOON", "LT+S", "EARTH", trmpts[1]
    )
    npt.assert_almost_equal(spice.dpr() * solar1, 89.730234298)
    iluet2, srfvec2, phase2, solar2, emissn2 = spice.ilumin(
        "Ellipsoid", "MOON", et, "IAU_MOON", "LT+S", "EARTH", trmpts[2]
    )
    npt.assert_almost_equal(spice.dpr() * solar2, 89.730234322)
    spice.kclear()


def test_ekacec():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekacec.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno = spice.ekbseg(
        handle,
        "test_table_ekacec",
        ["c1"],
        ["DATATYPE = CHARACTER*(*), NULLS_OK = TRUE"],
    )
    recno = spice.ekappr(handle, segno)
    spice.ekacec(handle, segno, recno, "c1", 2, ["1.0", "2.0"], False)
    spice.ekcls(handle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    assert not spice.exists(ekpath)


def test_ekaced():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekaced.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno = spice.ekbseg(
        handle,
        "test_table_ekaced",
        ["c1"],
        ["DATATYPE = DOUBLE PRECISION, NULLS_OK = TRUE"],
    )
    recno = spice.ekappr(handle, segno)
    spice.ekaced(handle, segno, recno, "c1", 2, [1.0, 2.0], False)
    spice.ekcls(handle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    assert not spice.exists(ekpath)


def test_ekmany():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekmany.ek")
    tablename = "test_table_ekmany"
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    # Create new EK and new segment with table
    handle = spice.ekopn(ekpath, ekpath, 0)
    decls = [
        "DATATYPE = CHARACTER*(10),   NULLS_OK = FALSE, SIZE = VARIABLE",
        "DATATYPE = DOUBLE PRECISION, NULLS_OK = FALSE, SIZE = VARIABLE",
        "DATATYPE = INTEGER,          NULLS_OK = FALSE, SIZE = VARIABLE",
    ]
    segno = spice.ekbseg(handle, tablename, ["c1", "d1", "i1"], decls)
    # Insert records:  1, 2, and 3 entries at rows 0, 1, 2, respectively
    c_data = [["100"], ["101", "101"], ["102", "102", "102"]]
    d_data = [[100.0], [101.0, 101.0], [102.0, 102.0, 102.0]]
    i_data = [[100], [101, 101], [102, 102, 102]]
    for r in range(0, 3):
        spice.ekinsr(handle, segno, r)
        spice.ekacec(handle, segno, r, "c1", len(c_data[r]), c_data[r], False)
        spice.ekaced(handle, segno, r, "d1", len(d_data[r]), d_data[r], False)
        spice.ekacei(handle, segno, r, "i1", len(i_data[r]), i_data[r], False)
    # Try record insertion beyond the next available, verify the exception
    with pytest.raises(spice.stypes.SpiceyError):
        spice.ekinsr(handle, segno, 4)
    # Close EK, then reopen for reading
    spice.ekcls(handle)
    spice.kclear()
    #
    # Start of part two
    #
    handle = spice.eklef(ekpath)
    assert handle is not None
    # Test query using ekpsel
    query = "SELECT c1, d1, i1 from {}".format(tablename)
    n, xbegs, xends, xtypes, xclass, tabs, cols, err, errmsg = spice.ekpsel(
        query, 99, 99, 99
    )
    assert n == 3
    assert spice.stypes.SpiceEKDataType.SPICE_CHR == xtypes[0]
    assert spice.stypes.SpiceEKDataType.SPICE_DP == xtypes[1]
    assert spice.stypes.SpiceEKDataType.SPICE_INT == xtypes[2]
    assert ([spice.stypes.SpiceEKExprClass.SPICE_EK_EXP_COL] * 3) == list(xclass)
    assert (["TEST_TABLE_EKMANY"] * 3) == tabs
    assert "C1 D1 I1".split() == cols
    assert not err
    assert "" == errmsg
    # Run query to retrieve the row count
    nmrows, error, errmsg = spice.ekfind(query, 99)
    assert nmrows == 3
    assert not error
    assert "" == errmsg
    # test fail case for eknelt
    with pytest.raises(spice.stypes.SpiceyError):
        spice.eknelt(0, nmrows + 1)
    # Validate the content of each field, including exceptions when
    # Loop over rows, test .ekgc/.ekgd/.ekgi
    for r in range(nmrows):
        # get number of elements in this row
        n_elm = spice.eknelt(0, r)
        assert n_elm == r + 1
        for e in range(0, n_elm):
            # get row int data
            i_datum, i_null = spice.ekgi(2, r, e)
            assert not i_null
            assert i_datum == i_data[r][e]
            # get row double data
            d_datum, d_null = spice.ekgd(1, r, e)
            assert not d_null
            assert d_datum == d_data[r][e]
            # get row char data
            c_datum, c_null = spice.ekgc(0, r, e)
            assert not c_null
            assert c_datum == c_data[r][e]
    # Loop over rows, test .ekrcec/.ekrced/.ekrcei
    for r in range(nmrows):
        # get row int data
        ni_vals, ri_data, i_null = spice.ekrcei(handle, segno, r, "i1")
        assert not i_null
        assert ni_vals == r + 1
        npt.assert_array_equal(ri_data, i_data[r])
        # get row double data
        nd_vals, rd_data, d_null = spice.ekrced(handle, segno, r, "d1")
        assert not d_null
        assert nd_vals == r + 1
        npt.assert_array_equal(rd_data, d_data[r])
        # get row char data
        nc_vals, rc_data, c_null = spice.ekrcec(handle, segno, r, "c1", 11)
        assert not c_null
        assert nc_vals == r + 1
        assert rc_data == c_data[r]
    # test out of bounds
    with pytest.raises(spice.stypes.SpiceyError):
        spice.ekrcei(handle, segno, 3, "i1")
    with pytest.raises(spice.stypes.SpiceyError):
        spice.ekrced(handle, segno, 3, "d1")
    # with pytest.raises(spice.stypes.SpiceyError): TODO: FIX
    #    spice.ekrcec(handle, segno, 4, "c1", 4) # this causes a SIGSEGV
    #
    # Part 3
    #
    # Close file, re-open for writing
    spice.ekuef(handle)
    handle = spice.ekopw(ekpath)
    # Loop over rows, update values using .ekucec/.ekuced/.ekucei
    c_data = [["200"], ["201", "201"], ["202", "202", "202"]]
    d_data = [[200.0], [201.0, 201.0], [202.0, 202.0, 202.0]]
    i_data = [[200], [201, 201], [202, 202, 202]]
    for r in range(0, 3):
        spice.ekucec(handle, segno, r, "c1", len(c_data[r]), c_data[r], False)
        spice.ekuced(handle, segno, r, "d1", len(d_data[r]), d_data[r], False)
        spice.ekucei(handle, segno, r, "i1", len(i_data[r]), i_data[r], False)
    # Test invalid updates
    with pytest.raises(spice.stypes.SpiceyError):
        spice.ekucec(handle, segno, 3, "c1", 1, ["300"], False)
    with pytest.raises(spice.stypes.SpiceyError):
        spice.ekuced(handle, segno, 3, "d1", 1, [300.0], False)
    with pytest.raises(spice.stypes.SpiceyError):
        spice.ekucei(handle, segno, 3, "i1", 1, [300], False)
    # Loop over rows, use .ekrcec/.ekrced/.ekrcei to test updates
    for r in range(nmrows):
        # get row int data
        ni_vals, ri_data, i_null = spice.ekrcei(handle, segno, r, "i1")
        assert not i_null
        assert ni_vals == r + 1
        npt.assert_array_equal(ri_data, i_data[r])
        # get row double data
        nd_vals, rd_data, d_null = spice.ekrced(handle, segno, r, "d1")
        assert not d_null
        assert nd_vals == r + 1
        npt.assert_array_equal(rd_data, d_data[r])
        # get row char data
        nc_vals, rc_data, c_null = spice.ekrcec(handle, segno, r, "c1", 11)
        assert not c_null
        assert nc_vals == r + 1
        assert rc_data == c_data[r]
    # Cleanup
    spice.ekcls(handle)
    assert not spice.failed()
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover


def test_ekaclc():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekaclc.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = spice.ekifld(
        handle,
        "test_table_ekaclc",
        1,
        2,
        200,
        ["c1"],
        200,
        ["DATATYPE = CHARACTER*(*), INDEXED  = TRUE"],
    )
    spice.ekaclc(
        handle, segno, "c1", 10, ["1.0", "2.0"], [4, 4], [False, False], rcptrs, [0, 0]
    )
    spice.ekffld(handle, segno, rcptrs)
    spice.ekcls(handle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    assert not spice.exists(ekpath)


def test_ekacld():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekacld.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = spice.ekifld(
        handle,
        "test_table_ekacld",
        1,
        2,
        200,
        ["c1"],
        200,
        ["DATATYPE = DOUBLE PRECISION, NULLS_OK = FALSE"],
    )
    spice.ekacld(
        handle, segno, "c1", [1.0, 2.0], [1, 1], [False, False], rcptrs, [0, 0]
    )
    spice.ekffld(handle, segno, rcptrs)
    spice.ekcls(handle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    assert not spice.exists(ekpath)


def test_ekacli():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekacli.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = spice.ekifld(
        handle,
        "test_table_ekacli",
        1,
        2,
        200,
        ["c1"],
        200,
        ["DATATYPE = INTEGER, NULLS_OK = TRUE"],
    )
    spice.ekacli(handle, segno, "c1", [1, 2], [1, 1], [False, False], rcptrs, [0, 0])
    spice.ekffld(handle, segno, rcptrs)
    spice.ekcls(handle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    assert not spice.exists(ekpath)


def test_ekacli_stress():
    for i in range(10):
        test_ekacli()


def test_ekappr():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekappr.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno = spice.ekbseg(
        handle, "test_table_ekappr", ["c1"], ["DATATYPE  = INTEGER, NULLS_OK = TRUE"]
    )
    recno = spice.ekappr(handle, segno)
    spice.ekacei(handle, segno, recno, "c1", 2, [1, 2], False)
    spice.ekcls(handle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    assert not spice.exists(ekpath)


def test_ekbseg():
    ekpath = os.path.join(cwd, "example_ekbseg.ek")
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    handle = spice.ekopn(ekpath, "Test EK", 100)
    cnames = ["INT_COL_1"]
    cdecls = ["DATATYPE=INTEGER, INDEXED=TRUE, NULLS_OK=TRUE"]
    segno = spice.ekbseg(handle, "SCALAR_DATA", cnames, cdecls)
    recno = spice.ekappr(handle, segno)
    assert recno != -1
    ordids = [x for x in range(5)]
    spice.ekacei(handle, segno, recno, "INT_COL_1", 5, ordids, False)
    spice.ekcls(handle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    assert not spice.exists(ekpath)


def test_ekbseg_stress():
    for i in range(10):
        test_ekbseg()


def test_ekccnt():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekccnt.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno = spice.ekbseg(
        handle, "TEST_TABLE_EKCCNT", ["c1"], ["DATATYPE  = INTEGER, NULLS_OK = TRUE"]
    )
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
        os.remove(ekpath)  # pragma: no cover
    assert not spice.exists(ekpath)


def test_ekcii():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekcii.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno = spice.ekbseg(
        handle, "TEST_TABLE_EKCII", ["c1"], ["DATATYPE  = INTEGER, NULLS_OK = TRUE"]
    )
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
    assert (
        attdsc.nullok
    )  # this used to be false, although clearly it should be true given the call to ekbseg
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    assert not spice.exists(ekpath)


def test_ekcls():
    spice.kclear()  # same as ekopn test
    ekpath = os.path.join(cwd, "example_ekcls.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    handle = spice.ekopn(ekpath, ekpath, 80)
    spice.ekcls(handle)
    assert spice.exists(ekpath)
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    spice.kclear()


def test_ekdelr():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekdelr.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = spice.ekifld(
        handle,
        "test_table_ekdelr",
        1,
        10,
        200,
        ["c1"],
        200,
        ["DATATYPE = INTEGER, NULLS_OK = TRUE"],
    )
    spice.ekacli(handle, segno, "c1", [1, 2], [1], [False, False], rcptrs, [1])
    spice.ekffld(handle, segno, rcptrs)
    spice.ekdelr(handle, segno, 2)
    spice.ekcls(handle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    assert not spice.exists(ekpath)


def test_ekdelr_stress():
    for i in range(10):
        test_ekdelr()


def test_ekffld():
    # same as test_ekacli
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekffld.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = spice.ekifld(
        handle,
        "test_table_ekffld",
        1,
        10,
        200,
        ["c1"],
        200,
        ["DATATYPE = INTEGER, NULLS_OK = TRUE"],
    )
    spice.ekacli(handle, segno, "c1", [1, 2], [1], [False, False], rcptrs, [1])
    spice.ekffld(handle, segno, rcptrs)
    spice.ekcls(handle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    assert not spice.exists(ekpath)


def test_ekffld_stress():
    for i in range(10):
        test_ekffld()


def test_ekfind():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekfind.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = spice.ekifld(
        handle,
        "test_table_ekfind",
        1,
        2,
        200,
        ["cc1"],
        200,
        ["DATATYPE = INTEGER, NULLS_OK = TRUE"],
    )
    spice.ekacli(handle, segno, "cc1", [1, 2], [1, 1], [False, False], rcptrs, [0, 0])
    spice.ekffld(handle, segno, rcptrs)
    spice.ekcls(handle)
    spice.kclear()
    spice.furnsh(ekpath)
    nmrows, error, errmsg = spice.ekfind(
        "SELECT CC1 FROM TEST_TABLE_EKFIND WHERE CC1 > 0", 100
    )
    assert (
        nmrows != 0
    )  # should be 2 but I am not concerned about correctness in this case
    assert not error
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    assert not spice.exists(ekpath)


def test_ekfind_stess():
    for i in range(10):
        test_ekfind()


def test_ekgc():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekgc.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = spice.ekifld(
        handle,
        "test_table_ekgc",
        1,
        2,
        200,
        ["c1"],
        200,
        ["DATATYPE = CHARACTER*(*), INDEXED  = TRUE"],
    )
    spice.ekaclc(
        handle, segno, "c1", 10, ["1.0", "2.0"], [4, 4], [False, False], rcptrs, [0, 0]
    )
    spice.ekffld(handle, segno, rcptrs)
    spice.ekcls(handle)
    spice.kclear()
    spice.furnsh(ekpath)
    nmrows, error, errmsg = spice.ekfind("SELECT C1 FROM TEST_TABLE_EKGC", 100)
    assert not error
    c, null = spice.ekgc(0, 0, 0, 4)
    assert not null
    assert c == "1.0"
    c, null = spice.ekgc(0, 1, 0, 4)
    assert not null
    # assert c == "2.0" this fails, c is an empty string despite found being true.
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    assert not spice.exists(ekpath)


def test_ekgd():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekgd.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = spice.ekifld(
        handle,
        "test_table_ekgd",
        1,
        2,
        200,
        ["c1"],
        200,
        ["DATATYPE = DOUBLE PRECISION, NULLS_OK = TRUE"],
    )
    spice.ekacld(
        handle, segno, "c1", [1.0, 2.0], [1, 1], [False, False], rcptrs, [0, 0]
    )
    spice.ekffld(handle, segno, rcptrs)
    spice.ekcls(handle)
    spice.kclear()
    spice.furnsh(ekpath)
    nmrows, error, errmsg = spice.ekfind("SELECT C1 FROM TEST_TABLE_EKGD", 100)
    assert not error
    d, null = spice.ekgd(0, 0, 0)
    assert not null
    assert d == 1.0
    d, null = spice.ekgd(0, 1, 0)
    assert not null
    assert d == 2.0
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    assert not spice.exists(ekpath)


def test_ekgi():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekgi.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = spice.ekifld(
        handle,
        "test_table_ekgi",
        1,
        2,
        200,
        ["c1"],
        200,
        ["DATATYPE = INTEGER, NULLS_OK = FALSE"],
    )
    spice.ekacli(handle, segno, "c1", [1, 2], [1, 1], [False, False], rcptrs, [0, 0])
    spice.ekffld(handle, segno, rcptrs)
    spice.ekcls(handle)
    spice.kclear()
    spice.furnsh(ekpath)
    nmrows, error, errmsg = spice.ekfind("SELECT C1 FROM TEST_TABLE_EKGI", 100)
    assert not error
    i, null = spice.ekgi(0, 0, 0)
    assert not null
    assert i == 1
    i, null = spice.ekgi(0, 1, 0)
    assert not null
    assert i == 2
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    assert not spice.exists(ekpath)


def test_ekifld():
    # Same as test_ekacli
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekifld.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = spice.ekifld(
        handle,
        "test_table_ekifld",
        1,
        2,
        200,
        ["c1"],
        200,
        ["DATATYPE = INTEGER, NULLS_OK = TRUE"],
    )
    spice.ekacli(handle, segno, "c1", [1, 2], [1, 1], [False, False], rcptrs, [0, 0])
    spice.ekffld(handle, segno, rcptrs)
    spice.ekcls(handle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    assert not spice.exists(ekpath)


def test_eklef():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_eklef.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno = spice.ekbseg(
        handle, "test_table_eklef", ["c1"], ["DATATYPE  = INTEGER, NULLS_OK = TRUE"]
    )
    recno = spice.ekappr(handle, segno)
    spice.ekacei(handle, segno, recno, "c1", 2, [1, 2], False)
    spice.ekcls(handle)
    spice.kclear()
    handle = spice.eklef(ekpath)
    assert handle is not None
    spice.ekuef(handle)
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover


def test_eknseg():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_eknseg.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno = spice.ekbseg(
        handle, "TEST_TABLE_EKNSEG", ["c1"], ["DATATYPE  = INTEGER, NULLS_OK = TRUE"]
    )
    recno = spice.ekappr(handle, segno)
    spice.ekacei(handle, segno, recno, "c1", 2, [1, 2], False)
    spice.ekcls(handle)
    spice.kclear()
    handle = spice.ekopr(ekpath)
    assert spice.eknseg(handle) == 1
    spice.ekcls(handle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    assert not spice.exists(ekpath)


def test_ekntab():
    assert spice.ekntab() == 0


def test_ekopn():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ek.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    handle = spice.ekopn(ekpath, ekpath, 80)
    spice.ekcls(handle)
    spice.kclear()
    assert spice.exists(ekpath)
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover


def test_ekopr():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekopr.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    handle = spice.ekopn(ekpath, ekpath, 80)
    spice.ekcls(handle)
    assert spice.exists(ekpath)
    testhandle = spice.ekopr(ekpath)
    assert testhandle is not None
    spice.ekcls(testhandle)
    spice.kclear()
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover


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
        os.remove(ekpath)  # pragma: no cover
    handle = spice.ekopn(ekpath, ekpath, 80)
    spice.ekcls(handle)
    assert spice.exists(ekpath)
    testhandle = spice.ekopw(ekpath)
    assert testhandle is not None
    spice.ekcls(testhandle)
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    spice.kclear()


def test_ekssum():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ekssum.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno, rcptrs = spice.ekifld(
        handle,
        "test_table_ekssum",
        1,
        2,
        200,
        ["c1"],
        200,
        ["DATATYPE = INTEGER, NULLS_OK = TRUE"],
    )
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
        os.remove(ekpath)  # pragma: no cover
    assert not spice.exists(ekpath)


def test_ektnam():
    spice.kclear()
    ekpath = os.path.join(cwd, "example_ektnam.ek")
    if spice.exists(ekpath):
        os.remove(ekpath)  # pragma: no cover
    handle = spice.ekopn(ekpath, ekpath, 0)
    segno = spice.ekbseg(
        handle, "TEST_TABLE_EKTNAM", ["c1"], ["DATATYPE  = INTEGER, NULLS_OK = TRUE"]
    )
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
        os.remove(ekpath)  # pragma: no cover
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
        os.remove(ekpath)  # pragma: no cover
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
        os.remove(ekpath)  # pragma: no cover


def test_el2cgv():
    vec1 = [1.0, 1.0, 1.0]
    vec2 = [1.0, -1.0, 1.0]
    center = [1.0, 1.0, 1.0]
    smajor, sminor = spice.saelgv(vec1, vec2)
    ellipse = spice.cgv2el(center, smajor, sminor)
    outCenter, outSmajor, outSminor = spice.el2cgv(ellipse)
    expected_center = [1.0, 1.0, 1.0]
    expected_s_major = [np.sqrt(2.0), 0.0, np.sqrt(2.0)]
    expected_s_minor = [0.0, np.sqrt(2.0), 0.0]
    npt.assert_array_almost_equal(outCenter, expected_center)
    npt.assert_array_almost_equal(outSmajor, expected_s_major)
    npt.assert_array_almost_equal(outSminor, expected_s_minor)


def test_elemc():
    test_cell_one = spice.cell_char(10, 10)
    spice.insrtc("one", test_cell_one)
    spice.insrtc("two", test_cell_one)
    spice.insrtc("three", test_cell_one)
    assert spice.elemc("one", test_cell_one)
    assert spice.elemc("two", test_cell_one)
    assert spice.elemc("three", test_cell_one)
    assert not spice.elemc("not", test_cell_one)
    assert not spice.elemc("there", test_cell_one)


def test_elemd():
    test_cell_one = spice.cell_double(8)
    spice.insrtd(1.0, test_cell_one)
    spice.insrtd(2.0, test_cell_one)
    spice.insrtd(3.0, test_cell_one)
    assert spice.elemd(1.0, test_cell_one)
    assert spice.elemd(2.0, test_cell_one)
    assert spice.elemd(3.0, test_cell_one)
    assert not spice.elemd(4.0, test_cell_one)
    assert not spice.elemd(-1.0, test_cell_one)


def test_elemi():
    test_cell_one = spice.cell_int(8)
    spice.insrti(1, test_cell_one)
    spice.insrti(2, test_cell_one)
    spice.insrti(3, test_cell_one)
    assert spice.elemi(1, test_cell_one)
    assert spice.elemi(2, test_cell_one)
    assert spice.elemi(3, test_cell_one)
    assert not spice.elemi(4, test_cell_one)
    assert not spice.elemi(-1, test_cell_one)


def test_eqncpv():
    p = 10000.0
    gm = 398600.436
    ecc = 0.1
    a = p / (1.0 - ecc)
    n = np.sqrt(gm / a) / a
    argp = 30.0 * spice.rpd()
    node = 15.0 * spice.rpd()
    inc = 10.0 * spice.rpd()
    m0 = 45.0 * spice.rpd()
    t0 = -100000000.0
    eqel = [
        a,
        ecc * np.sin(argp + node),
        ecc * np.cos(argp + node),
        m0 + argp + node,
        np.tan(inc / 2.0) * np.sin(node),
        np.tan(inc / 2.0) * np.cos(node),
        0.0,
        n,
        0.0,
    ]
    state = spice.eqncpv(t0 - 9750.0, t0, eqel, spice.halfpi() * -1, spice.halfpi())
    expected = [
        -10732.167433285387,
        3902.505790600528,
        1154.4516152766892,
        -2.540766899262123,
        -5.15226920298345,
        -0.7615758062877463,
    ]
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
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("2004 may 17 16:30:00")
    hr, mn, sc, time, ampm = spice.et2lst(
        et, 399, 281.49521300000004 * spice.rpd(), "planetocentric", 51, 51
    )
    assert hr == 11
    assert mn == 19
    assert sc == 22
    assert time == "11:19:22"
    assert ampm == "11:19:22 A.M."
    spice.kclear()


def test_et2utc():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = -527644192.5403653
    output = spice.et2utc(et, "J", 6)
    assert output == "JD 2445438.006415"
    spice.kclear()


def test_et2utc_vectorized():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = -527644192.5403653
    output = spice.et2utc(3 * [et], "J", 6)
    assert np.array_equal(
        output,
        np.array(("JD 2445438.006415", "JD 2445438.006415", "JD 2445438.006415")),
    )
    spice.kclear()


def test_etcal():
    et = np.arange(0.0, 20.0)
    cal = spice.etcal(et[0])
    assert cal == "2000 JAN 01 12:00:00.000"
    calArr = spice.etcal(et)
    assert calArr[0] == cal
    assert calArr[1] == "2000 JAN 01 12:00:01.000"
    assert calArr[-1] == "2000 JAN 01 12:00:19.000"


def test_eul2m():
    rot = np.array(spice.eul2m(spice.halfpi(), 0.0, 0.0, 3, 1, 1))
    assert rot.shape == ((3, 3))


def test_eul2xf():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("Jan 1, 2009")
    expected = spice.sxform("IAU_EARTH", "J2000", et)
    eul = [
        1.571803284049681,
        0.0008750002978301174,
        2.9555269829740034,
        3.5458495690569166e-12,
        3.080552365717176e-12,
        -7.292115373266558e-05,
    ]
    out = spice.eul2xf(eul, 3, 1, 3)
    npt.assert_array_almost_equal(out, expected)
    spice.kclear()


def test_ev2lin():
    spice.kclear()
    # lightsail 2
    tle = [
        "1 44420U 19036AC  19311.70264562  .00005403  00000-0  12176-2 0  9991",
        "2 44420  24.0060  72.9267 0016343 241.6999 118.1833 14.53580129 17852",
    ]
    spice.furnsh(CoreKernels.testMetaKernel)
    epoch, elems = spice.getelm(2019, 75, tle)
    # adding 3 seconds manually as something is wrong with provided tle epoch or the lsk kernel was not used when generating the expected output
    expected_elems = np.array(
        [
            1.63715519939676e-10,
            0,
            0.0012176,
            0.418983740233759,
            1.27281102761415,
            0.0016343,
            4.21845905674104,
            2.06268770587221,
            0.0634243979815348,
            626417577.764171,
        ]
    )
    expected_epoch = 626417577.764171
    npt.assert_array_almost_equal(expected_elems, elems)
    npt.assert_almost_equal(epoch, expected_epoch)
    # test ev2lin
    geophs = [
        1.082616e-3,
        -2.53881e-6,
        -1.65597e-6,
        7.43669161e-2,
        120.0,
        78.0,
        6378.135,
        1.0,
    ]
    # test at t0
    state_0 = spice.ev2lin(epoch, geophs, elems)
    expected_state_0 = np.array(
        [
            2083.32107340449,
            6782.80001655649,
            -0.0505350227151017,
            -6.54335340061531,
            2.01771874263164,
            3.0515091420169,
        ]
    )
    npt.assert_array_almost_equal(expected_state_0, state_0)
    # test at t3600
    state_3600 = spice.ev2lin(epoch + 3600, geophs, elems)
    expected_state_3600 = np.array(
        [
            2175.83882413485,
            -6497.55066037852,
            -1786.06093660828,
            6.52417720498168,
            2.84696745594303,
            -2.39736415840424,
        ]
    )
    npt.assert_array_almost_equal(expected_state_3600, state_3600)
    spice.kclear()
    # test at t86400
    state_86400 = spice.ev2lin(epoch + 86400, geophs, elems)
    expected_state_86400 = np.array(
        [
            -193.463324028138,
            -6986.20486685614,
            -1154.18287208625,
            6.96216415803069,
            0.276466105258879,
            -2.79931910593688,
        ]
    )
    npt.assert_array_almost_equal(expected_state_86400, state_86400)
    spice.kclear()


def test_exists():
    assert spice.exists(CoreKernels.testMetaKernel)


def test_expool():
    spice.kclear()
    textbuf = ["DELTET/K = 1.657D-3", "DELTET/EB = 1.671D-2"]
    spice.lmpool(textbuf)
    assert spice.expool("DELTET/K")
    assert spice.expool("DELTET/EB")
    spice.kclear()


def test_expoolstress():
    # this is to show that the bug in lmpool is fixed (lenvals needs +=1)
    for i in range(500):
        test_expool()


def test_failed():
    assert not spice.failed()


def test_fovray():
    spice.kclear()
    # load kernels
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(CassiniKernels.cassSclk)
    spice.furnsh(CassiniKernels.cassFk)
    spice.furnsh(CassiniKernels.cassPck)
    spice.furnsh(CassiniKernels.cassIk)
    spice.furnsh(CassiniKernels.cassSclk)
    spice.furnsh(CassiniKernels.satSpk)
    spice.furnsh(CassiniKernels.cassTourSpk)
    spice.furnsh(CassiniKernels.cassCk)
    # core of test
    camid = spice.bodn2c("CASSINI_ISS_NAC")
    shape, frame, bsight, n, bounds = spice.getfov(camid, 4)
    et = spice.str2et("2013 FEB 25 11:50:00 UTC")
    visible = spice.fovray(
        "CASSINI_ISS_NAC", [0.0, 0.0, 1.0], frame, "S", "CASSINI", et
    )
    assert visible is True
    spice.kclear()


def test_fovtrg():
    spice.kclear()
    # load kernels
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(CassiniKernels.cassSclk)
    spice.furnsh(CassiniKernels.cassFk)
    spice.furnsh(CassiniKernels.cassPck)
    spice.furnsh(CassiniKernels.cassIk)
    spice.furnsh(CassiniKernels.cassSclk)
    spice.furnsh(CassiniKernels.satSpk)
    spice.furnsh(CassiniKernels.cassTourSpk)
    spice.furnsh(CassiniKernels.cassCk)
    # core of test
    et = spice.str2et("2013 FEB 25 11:50:00 UTC")
    visible = spice.fovtrg(
        "CASSINI_ISS_NAC",
        "Enceladus",
        "Ellipsoid",
        "IAU_ENCELADUS",
        "LT+S",
        "CASSINI",
        et,
    )
    assert visible is True
    spice.kclear()


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
    assert spice.frinfo(13000) == (399, 2, 3000)


def test_frmnam():
    assert spice.frmnam(13000) == "ITRF93"
    assert spice.frmnam(13000) == "ITRF93"


def test_ftncls():
    import datetime

    spice.reset()
    spice.kclear()
    # Create temporary filename
    FTNCLS = os.path.join(cwd, "ex_ftncls.txt")
    # Ensure file does not exist
    if spice.exists(FTNCLS):
        os.remove(FTNCLS)  # pragma no cover
    # Open new file using FORTRAN SPICE TXTOPN
    unit = spice.txtopn(FTNCLS)
    # Get the FORTRAN logical unit of the open file using FORTRAN SPICE FN2LEN
    assert unit == spice.fn2lun(FTNCLS)
    assert not spice.failed()
    # Close the FORTRAN logical unit using ftncls, the subject of this test
    spice.ftncls(unit)
    with pytest.raises(spice.stypes.SpiceyError):
        closed_unit = spice.fn2lun(FTNCLS)
    # Cleanup
    spice.reset()
    spice.kclear()
    if spice.exists(FTNCLS):
        os.remove(FTNCLS)  # pragma no cover


def test_furnsh():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    # 4 kernels + the meta kernel = 5
    assert spice.ktotal("ALL") == 5
    spice.kclear()


def test_furnsh_vectorized():
    spice.kclear()
    spice.furnsh([CoreKernels.testMetaKernel, ExtraKernels.voyagerSclk])
    # 4 + 1 + 1 = 6
    assert spice.ktotal("ALL") == 6
    spice.kclear()


def test_gcpool():
    # same as pcpool test
    import string

    spice.kclear()
    data = [j + str(i) for i, j in enumerate(list(string.ascii_lowercase))]
    spice.pcpool("pcpool_test", data)
    cvals = spice.gcpool("pcpool_test", 0, 30)
    assert data == cvals
    spice.kclear()


def test_gdpool():
    # same as pdpool test
    spice.kclear()
    data = np.arange(0.0, 10.0)
    spice.pdpool("pdpool_array", data)
    dvals = spice.gdpool("pdpool_array", 0, 30)
    npt.assert_array_almost_equal(data, dvals)
    spice.kclear()


def test_georec():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    size, radii = spice.bodvrd("EARTH", "RADII", 3)
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
    tle = [
        "1 18123U 87 53  A 87324.61041692 -.00000023  00000-0 -75103-5 0 00675",
        "2 18123  98.8296 152.0074 0014950 168.7820 191.3688 14.12912554 21686",
    ]
    spice.furnsh(CoreKernels.testMetaKernel)
    epoch, elems = spice.getelm(1950, 75, tle)
    expected_elems = [
        -6.969196665949579e-13,
        0.0,
        -7.510300000000001e-06,
        1.724901918428988,
        2.653029617396028,
        0.001495,
        2.9458016181010693,
        3.3400156455905243,
        0.06164994027515544,
        -382310404.79526937,
    ]
    expected_epoch = -382310404.79526937
    npt.assert_array_almost_equal(expected_elems, elems)
    npt.assert_almost_equal(epoch, expected_epoch)
    spice.kclear()


def test_getfat():
    arch, outtype = spice.getfat(CoreKernels.lsk)
    assert arch == "KPL"
    assert outtype == "LSK"


def test_getfov():
    spice.kclear()
    kernel = os.path.join(cwd, "getfov_test.ti")
    if spice.exists(kernel):
        os.remove(kernel)  # pragma: no cover
    with open(kernel, "w") as kernelFile:
        kernelFile.write("\\begindata\n")
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
        os.remove(kernel)  # pragma: no cover


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
    spice.furnsh(CoreKernels.testMetaKernel)
    et0 = spice.str2et("2007 JAN 01 00:00:00 TDB")
    et1 = spice.str2et("2007 APR 01 00:00:00 TDB")
    cnfine = spice.cell_double(2)
    spice.wninsd(et0, et1, cnfine)
    result = spice.cell_double(1000)
    spice.gfdist(
        "moon", "none", "earth", ">", 400000, 0.0, spice.spd(), 1000, cnfine, result
    )
    count = spice.wncard(result)
    assert count == 4
    temp_results = []
    for i in range(0, count):
        left, right = spice.wnfetd(result, i)
        timstr_left = spice.timout(
            left, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND", 41
        )
        timstr_right = spice.timout(
            right, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND", 41
        )
        temp_results.append(timstr_left)
        temp_results.append(timstr_right)
    expected = [
        "2007-JAN-08 00:11:07.661897 (TDB)",
        "2007-JAN-13 06:37:47.937762 (TDB)",
        "2007-FEB-04 07:02:35.320555 (TDB)",
        "2007-FEB-10 09:31:01.829206 (TDB)",
        "2007-MAR-03 00:20:25.228066 (TDB)",
        "2007-MAR-10 14:04:38.482902 (TDB)",
        "2007-MAR-29 22:53:58.186230 (TDB)",
        "2007-APR-01 00:00:00.000000 (TDB)",
    ]
    assert temp_results == expected
    spice.kclear()


def test_gfevnt():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    #
    et_start = spice.str2et("2001 jan 01 00:00:00.000")
    et_end = spice.str2et("2001 dec 31 00:00:00.000")
    cnfine = spice.cell_double(2)
    spice.wninsd(et_start, et_end, cnfine)
    result = spice.cell_double(1000)
    qpnams = ["TARGET", "OBSERVER", "ABCORR"]
    qcpars = ["MOON  ", "EARTH   ", "LT+S  "]
    # Set the step size to 1/1000 day and convert to seconds
    spice.gfsstp(0.001 * spice.spd())
    # setup callbacks
    udstep = spiceypy.utils.callbacks.SpiceUDSTEP(spice.gfstep)
    udrefn = spiceypy.utils.callbacks.SpiceUDREFN(spice.gfrefn)
    udrepi = spiceypy.utils.callbacks.SpiceUDREPI(spice.gfrepi)
    udrepu = spiceypy.utils.callbacks.SpiceUDREPU(spice.gfrepu)
    udrepf = spiceypy.utils.callbacks.SpiceUDREPF(spice.gfrepf)
    udbail = spiceypy.utils.callbacks.SpiceUDBAIL(spice.gfbail)
    qdpars = np.zeros(10, dtype=np.float)
    qipars = np.zeros(10, dtype=np.int32)
    qlpars = np.zeros(10, dtype=np.int32)
    # call gfevnt
    spice.gfevnt(
        udstep,
        udrefn,
        "DISTANCE",
        3,
        81,
        qpnams,
        qcpars,
        qdpars,
        qipars,
        qlpars,
        "LOCMAX",
        0,
        1.0e-6,
        0,
        True,
        udrepi,
        udrepu,
        udrepf,
        10000,
        True,
        udbail,
        cnfine,
        result,
    )

    # Verify the expected results
    assert len(result) == 26
    sTimout = "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND"
    assert spice.timout(result[0], sTimout) == "2001-JAN-24 19:22:01.418715 (TDB)"
    assert spice.timout(result[1], sTimout) == "2001-JAN-24 19:22:01.418715 (TDB)"
    assert spice.timout(result[2], sTimout) == "2001-FEB-20 21:52:07.900872 (TDB)"
    assert spice.timout(result[3], sTimout) == "2001-FEB-20 21:52:07.900872 (TDB)"
    # Cleanup
    if spice.gfbail():
        spice.gfclrh()  # pragma: no cover
    spice.gfsstp(0.5)
    spice.kclear()


def test_gffove():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(CassiniKernels.cassCk)
    spice.furnsh(CassiniKernels.cassFk)
    spice.furnsh(CassiniKernels.cassIk)
    spice.furnsh(CassiniKernels.cassPck)
    spice.furnsh(CassiniKernels.cassSclk)
    spice.furnsh(CassiniKernels.cassTourSpk)
    spice.furnsh(CassiniKernels.satSpk)
    # Cassini ISS NAC observed Enceladus on 2013-FEB-25 from ~11:00 to ~12:00
    # Split confinement window, from continuous CK coverage, into two pieces
    et_start = spice.str2et("2013-FEB-25 10:00:00.000")
    et_end = spice.str2et("2013-FEB-25 11:45:00.000")
    cnfine = spice.cell_double(2)
    spice.wninsd(et_start, et_end, cnfine)
    result = spice.cell_double(1000)
    # call gffove
    udstep = spiceypy.utils.callbacks.SpiceUDSTEP(spice.gfstep)
    udrefn = spiceypy.utils.callbacks.SpiceUDREFN(spice.gfrefn)
    udrepi = spiceypy.utils.callbacks.SpiceUDREPI(spice.gfrepi)
    udrepu = spiceypy.utils.callbacks.SpiceUDREPU(spice.gfrepu)
    udrepf = spiceypy.utils.callbacks.SpiceUDREPF(spice.gfrepf)
    udbail = spiceypy.utils.callbacks.SpiceUDBAIL(spice.gfbail)
    spice.gfsstp(1.0)
    spice.gffove(
        "CASSINI_ISS_NAC",
        "ELLIPSOID",
        [0.0, 0.0, 0.0],
        "ENCELADUS",
        "IAU_ENCELADUS",
        "LT+S",
        "CASSINI",
        1.0e-6,
        udstep,
        udrefn,
        True,
        udrepi,
        udrepu,
        udrepf,
        True,
        udbail,
        cnfine,
        result,
    )
    # Verify the expected results
    assert len(result) == 2
    sTimout = "YYYY-MON-DD HR:MN:SC UTC ::RND"
    assert spice.timout(result[0], sTimout) == "2013-FEB-25 10:42:33 UTC"
    assert spice.timout(result[1], sTimout) == "2013-FEB-25 11:45:00 UTC"
    # Cleanup
    if spice.gfbail():
        spice.gfclrh()  # pragma: no cover
    spice.gfsstp(0.5)
    spice.kclear()


def test_gfilum():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.marsSpk)  # to get Phobos ephemeris
    # Hard-code the future position of MER-1
    # pos, lt = spice.spkpos("MER-1", spice.str2et("2006 OCT 02 00:00:00 UTC"), "iau_mars", "CN+S", "Mars")
    pos = [
        3376.17890941875839416753,
        -325.55203839445334779157,
        -121.47422900638389364758,
    ]
    # Two-month Viking orbiter window for Phobos;
    # - marsSPK runs from [1971 OCT 01] to [1972 OCT 01]
    startET = spice.str2et("1971 OCT 02 00:00:00 UTC")
    endET = spice.str2et("1971 NOV 30 12:00:00 UTC")
    # Create confining and result windows for incidence angle GF check
    cnfine = spice.cell_double(2000)
    spice.wninsd(startET, endET, cnfine)
    wnsolr = spice.cell_double(2000)
    # Find windows where solar incidence angle at MER-1 position is < 60deg
    spice.gfilum(
        "Ellipsoid",
        "INCIDENCE",
        "Mars",
        "Sun",
        "iau_mars",
        "CN+S",
        "PHOBOS",
        pos,
        "<",
        60.0 * spice.rpd(),
        0.0,
        21600.0,
        1000,
        cnfine,
        wnsolr,
    )
    # Create result window for emission angle GF check
    result = spice.cell_double(2000)
    # Find windows, within solar incidence angle windows found above (wnsolar),
    # where emission angle from MER-1 position to Phobos is < 20deg
    spice.gfilum(
        "Ellipsoid",
        "EMISSION",
        "Mars",
        "Sun",
        "iau_mars",
        "CN+S",
        "PHOBOS",
        pos,
        "<",
        20.0 * spice.rpd(),
        0.0,
        900.0,
        1000,
        wnsolr,
        result,
    )
    # Ensure there were some results
    assert spice.wncard(result) > 0
    startEpoch = spice.timout(result[0], "YYYY MON DD HR:MN:SC.###### UTC")
    endEpoch = spice.timout(result[-1], "YYYY MON DD HR:MN:SC.###### UTC")
    # Check times of results
    assert startEpoch.startswith("1971 OCT 02")
    assert endEpoch.startswith("1971 NOV 29")
    # Cleanup
    spice.kclear()


def test_gfinth():
    spice.gfinth(2)
    with pytest.raises(spice.stypes.SpiceyError):
        spice.gfinth(0)


def test_gfocce():
    spice.kclear()
    if spice.gfbail():
        spice.gfclrh()  # pragma: no cover
    spice.furnsh(CoreKernels.testMetaKernel)
    et0 = spice.str2et("2001 DEC 01 00:00:00 TDB")
    et1 = spice.str2et("2002 JAN 01 00:00:00 TDB")
    cnfine = spice.cell_double(2)
    spice.wninsd(et0, et1, cnfine)
    result = spice.cell_double(1000)
    spice.gfsstp(20.0)
    udstep = spiceypy.utils.callbacks.SpiceUDSTEP(spice.gfstep)
    udrefn = spiceypy.utils.callbacks.SpiceUDREFN(spice.gfrefn)
    udrepi = spiceypy.utils.callbacks.SpiceUDREPI(spice.gfrepi)
    udrepu = spiceypy.utils.callbacks.SpiceUDREPU(spice.gfrepu)
    udrepf = spiceypy.utils.callbacks.SpiceUDREPF(spice.gfrepf)
    udbail = spiceypy.utils.callbacks.SpiceUDBAIL(spice.gfbail)
    # call gfocce
    spice.gfocce(
        "Any",
        "moon",
        "ellipsoid",
        "iau_moon",
        "sun",
        "ellipsoid",
        "iau_sun",
        "lt",
        "earth",
        1.0e-6,
        udstep,
        udrefn,
        True,
        udrepi,
        udrepu,
        udrepf,
        True,
        udbail,
        cnfine,
        result,
    )
    if spice.gfbail():
        spice.gfclrh()  # pragma: no cover
    count = spice.wncard(result)
    assert count == 1
    spice.kclear()


def test_gfoclt():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et0 = spice.str2et("2001 DEC 01 00:00:00 TDB")
    et1 = spice.str2et("2002 JAN 01 00:00:00 TDB")
    cnfine = spice.cell_double(2)
    spice.wninsd(et0, et1, cnfine)
    result = spice.cell_double(1000)
    spice.gfoclt(
        "any",
        "moon",
        "ellipsoid",
        "iau_moon",
        "sun",
        "ellipsoid",
        "iau_sun",
        "lt",
        "earth",
        180.0,
        cnfine,
        result,
    )
    count = spice.wncard(result)
    assert count == 1
    start, end = spice.wnfetd(result, 0)
    start_time = spice.timout(
        start, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND", 41
    )
    end_time = spice.timout(end, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND", 41)
    assert start_time == "2001-DEC-14 20:10:14.203347 (TDB)"
    assert end_time == "2001-DEC-14 21:35:50.328804 (TDB)"
    spice.kclear()


def test_gfpa():
    relate = ["=", "<", ">", "LOCMIN", "ABSMIN", "LOCMAX", "ABSMAX"]
    expected = {
        "=": [
            "2006-DEC-02 13:31:34.425",
            "2006-DEC-02 13:31:34.425",
            "2006-DEC-07 14:07:55.480",
            "2006-DEC-07 14:07:55.480",
            "2007-JAN-01 00:00:00.007",
            "2007-JAN-01 00:00:00.007",
            "2007-JAN-06 08:16:25.522",
            "2007-JAN-06 08:16:25.522",
            "2007-JAN-30 11:41:32.568",
            "2007-JAN-30 11:41:32.568",
        ],
        "<": [
            "2006-DEC-02 13:31:34.425",
            "2006-DEC-07 14:07:55.480",
            "2007-JAN-01 00:00:00.007",
            "2007-JAN-06 08:16:25.522",
            "2007-JAN-30 11:41:32.568",
            "2007-JAN-31 00:00:00.000",
        ],
        ">": [
            "2006-DEC-01 00:00:00.000",
            "2006-DEC-02 13:31:34.425",
            "2006-DEC-07 14:07:55.480",
            "2007-JAN-01 00:00:00.007",
            "2007-JAN-06 08:16:25.522",
            "2007-JAN-30 11:41:32.568",
        ],
        "LOCMIN": [
            "2006-DEC-05 00:16:50.327",
            "2006-DEC-05 00:16:50.327",
            "2007-JAN-03 14:18:31.987",
            "2007-JAN-03 14:18:31.987",
        ],
        "ABSMIN": ["2007-JAN-03 14:18:31.987", "2007-JAN-03 14:18:31.987"],
        "LOCMAX": [
            "2006-DEC-20 14:09:10.402",
            "2006-DEC-20 14:09:10.402",
            "2007-JAN-19 04:27:54.610",
            "2007-JAN-19 04:27:54.610",
        ],
        "ABSMAX": ["2007-JAN-19 04:27:54.610", "2007-JAN-19 04:27:54.610"],
    }
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et0 = spice.str2et("2006 DEC 01")
    et1 = spice.str2et("2007 JAN 31")
    cnfine = spice.cell_double(2)
    spice.wninsd(et0, et1, cnfine)
    result = spice.cell_double(2000)
    for relation in relate:
        spice.gfpa(
            "Moon",
            "Sun",
            "LT+S",
            "Earth",
            relation,
            0.57598845,
            0.0,
            spice.spd(),
            5000,
            cnfine,
            result,
        )
        count = spice.wncard(result)
        if count > 0:
            temp_results = []
            for i in range(0, count):
                left, right = spice.wnfetd(result, i)
                timstr_left = spice.timout(left, "YYYY-MON-DD HR:MN:SC.###", 41)
                timstr_right = spice.timout(right, "YYYY-MON-DD HR:MN:SC.###", 41)
                temp_results.append(timstr_left)
                temp_results.append(timstr_right)
            assert temp_results == expected.get(relation)
    spice.kclear()


def test_gfposc():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et0 = spice.str2et("2007 JAN 01")
    et1 = spice.str2et("2008 JAN 01")
    cnfine = spice.cell_double(2)
    spice.wninsd(et0, et1, cnfine)
    result = spice.cell_double(1000)
    spice.gfposc(
        "sun",
        "iau_earth",
        "none",
        "earth",
        "latitudinal",
        "latitude",
        "absmax",
        0.0,
        0.0,
        90.0 * spice.spd(),
        1000,
        cnfine,
        result,
    )
    count = spice.wncard(result)
    assert count == 1
    start, end = spice.wnfetd(result, 0)
    start_time = spice.timout(
        start, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND", 41
    )
    end_time = spice.timout(end, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND", 41)
    assert start_time == end_time
    assert start_time == "2007-JUN-21 17:54:13.201561 (TDB)"
    spice.kclear()


def test_gfrefn():
    s1 = [True, False]
    s2 = [True, False]
    for i in range(0, 2):
        for j in range(0, 2):
            scale = 10.0 * i + j
            t1 = 5.0 * scale
            t2 = 7.0 * scale
            t = spice.gfrefn(t1, t2, s1[i], s2[j])
            assert t == pytest.approx(scale * 6.0)
    for i in range(0, 2):
        for j in range(0, 2):
            scale = 10.0 * i + j
            t1 = 15.0 * scale
            t2 = 7.0 * scale
            t = spice.gfrefn(t1, t2, s1[i], s2[j])
            assert t == pytest.approx(scale * 11.0)
    for i in range(0, 2):
        for j in range(0, 2):
            scale = 10.0 * i + j
            t1 = -scale
            t2 = -scale
            t = spice.gfrefn(t1, t2, s1[i], s2[j])
            assert t == pytest.approx(-scale)


def test_gfrepf():
    # Minimal test; gfrepf does nothing PyTest can notice
    spice.gfrepf()
    # Pass bad argument list
    with pytest.raises(TypeError):
        spice.gfrepf(0)


def test_gfrepi():
    window = spice.cell_double(4)
    spice.wninsd(0.0, 100.0, window)
    spice.gfrepi(window, "x", "y")
    # BEGMSS or ENDMSS empty, too long, or containing non-printing characters
    with pytest.raises(spice.stypes.SpiceyError):
        spice.gfrepi(window, "", "y")
    with pytest.raises(spice.stypes.SpiceyError):
        spice.gfrepi(window, "x", "")
    with pytest.raises(spice.stypes.SpiceyError):
        spice.gfrepi(window, "x" * 1000, "y")
    with pytest.raises(spice.stypes.SpiceyError):
        spice.gfrepi(window, "x", "y" * 1000)
    with pytest.raises(spice.stypes.SpiceyError):
        spice.gfrepi(window, "y\n", "y")
    with pytest.raises(spice.stypes.SpiceyError):
        spice.gfrepi(window, "x", "y\n")
    spice.gfrepf()


def test_gfrepu():
    window = spice.cell_double(4)
    spice.wninsd(0.0, 100.0, window)
    spice.gfrepi(window, "x", "y")
    spice.gfrepu(0.0, 100.0, 50.0)
    spice.gfrepu(0.0, 100.0, 100.0)
    with pytest.raises(spice.stypes.SpiceyError):
        spice.gfrepu(100.0, 0.0, 100.0)
    with pytest.raises(spice.stypes.SpiceyError):
        spice.gfrepu(0.0, 100.0, -1.0)
    with pytest.raises(spice.stypes.SpiceyError):
        spice.gfrepu(0.0, 100.0, 1011.0)
    spice.gfrepu(0.0, 100.0, 100.0)
    spice.gfrepf()


def test_gfrfov():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(CassiniKernels.cassCk)
    spice.furnsh(CassiniKernels.cassFk)
    spice.furnsh(CassiniKernels.cassIk)
    spice.furnsh(CassiniKernels.cassPck)
    spice.furnsh(CassiniKernels.cassSclk)
    spice.furnsh(CassiniKernels.cassTourSpk)
    spice.furnsh(CassiniKernels.satSpk)
    # Changed ABCORR to NONE from S for this test, so we do not need SSB
    # begin test
    inst = "CASSINI_ISS_WAC"
    # Cassini ISS NAC observed Enceladus on 2013-FEB-25 from ~11:00 to ~12:00
    # Split confinement window, from continuous CK coverage, into two pieces
    et_start1 = spice.str2et("2013-FEB-25 07:20:00.000")
    et_end1 = spice.str2et("2013-FEB-25 11:45:00.000")  # \
    et_start2 = spice.str2et("2013-FEB-25 11:55:00.000")  # _>synthetic 10min gap
    et_end2 = spice.str2et("2013-FEB-26 14:25:00.000")
    cnfine = spice.cell_double(4)
    spice.wninsd(et_start1, et_end1, cnfine)
    spice.wninsd(et_start2, et_end2, cnfine)
    # The ray direction vector is from Cassini toward Enceladus during the gap
    et_nom = spice.str2et("2013-FEB-25 11:50:00.000")  # \
    raydir, lt = spice.spkpos("Enceladus", et_nom, "J2000", "NONE", "Cassini")
    result = spice.cell_double(2000)
    spice.gfrfov(inst, raydir, "J2000", "NONE", "Cassini", 10.0, cnfine, result)
    # Verify the expected results
    assert len(result) == 4
    sTimout = "YYYY-MON-DD HR:MN:SC UTC ::RND"
    assert spice.timout(result[0], sTimout) == "2013-FEB-25 11:26:46 UTC"
    assert spice.timout(result[1], sTimout) == "2013-FEB-25 11:45:00 UTC"
    assert spice.timout(result[2], sTimout) == "2013-FEB-25 11:55:00 UTC"
    assert spice.timout(result[3], sTimout) == "2013-FEB-25 12:05:33 UTC"
    # Cleanup
    spice.kclear()


def test_gfrr():
    relate = ["=", "<", ">", "LOCMIN", "ABSMIN", "LOCMAX", "ABSMAX"]
    expected = {
        "=": [
            "2007-JAN-02 00:35:19.583",
            "2007-JAN-02 00:35:19.583",
            "2007-JAN-19 22:04:54.905",
            "2007-JAN-19 22:04:54.905",
            "2007-FEB-01 23:30:13.439",
            "2007-FEB-01 23:30:13.439",
            "2007-FEB-17 11:10:46.547",
            "2007-FEB-17 11:10:46.547",
            "2007-MAR-04 15:50:19.940",
            "2007-MAR-04 15:50:19.940",
            "2007-MAR-18 09:59:05.966",
            "2007-MAR-18 09:59:05.966",
        ],
        "<": [
            "2007-JAN-02 00:35:19.583",
            "2007-JAN-19 22:04:54.905",
            "2007-FEB-01 23:30:13.439",
            "2007-FEB-17 11:10:46.547",
            "2007-MAR-04 15:50:19.940",
            "2007-MAR-18 09:59:05.966",
        ],
        ">": [
            "2007-JAN-01 00:00:00.000",
            "2007-JAN-02 00:35:19.583",
            "2007-JAN-19 22:04:54.905",
            "2007-FEB-01 23:30:13.439",
            "2007-FEB-17 11:10:46.547",
            "2007-MAR-04 15:50:19.940",
            "2007-MAR-18 09:59:05.966",
            "2007-APR-01 00:00:00.000",
        ],
        "LOCMIN": [
            "2007-JAN-11 07:03:59.001",
            "2007-JAN-11 07:03:59.001",
            "2007-FEB-10 06:26:15.451",
            "2007-FEB-10 06:26:15.451",
            "2007-MAR-12 03:28:36.414",
            "2007-MAR-12 03:28:36.414",
        ],
        "ABSMIN": ["2007-JAN-11 07:03:59.001", "2007-JAN-11 07:03:59.001"],
        "LOCMAX": [
            "2007-JAN-26 02:27:33.772",
            "2007-JAN-26 02:27:33.772",
            "2007-FEB-24 09:35:07.822",
            "2007-FEB-24 09:35:07.822",
            "2007-MAR-25 17:26:56.158",
            "2007-MAR-25 17:26:56.158",
        ],
        "ABSMAX": ["2007-MAR-25 17:26:56.158", "2007-MAR-25 17:26:56.158"],
    }
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et0 = spice.str2et("2007 JAN 01")
    et1 = spice.str2et("2007 APR 01")
    cnfine = spice.cell_double(2)
    spice.wninsd(et0, et1, cnfine)
    for relation in relate:
        result = spice.cell_double(2000)
        spice.gfrr(
            "moon",
            "none",
            "sun",
            relation,
            0.3365,
            0.0,
            spice.spd(),
            2000,
            cnfine,
            result,
        )
        count = spice.wncard(result)
        if count > 0:
            temp_results = []
            for i in range(0, count):
                left, right = spice.wnfetd(result, i)
                timstr_left = spice.timout(left, "YYYY-MON-DD HR:MN:SC.###", 41)
                timstr_right = spice.timout(right, "YYYY-MON-DD HR:MN:SC.###", 41)
                temp_results.append(timstr_left)
                temp_results.append(timstr_right)
            assert temp_results == expected.get(relation)
    spice.kclear()


def test_gfsep():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    expected = [
        "2007-JAN-03 14:20:24.628017 (TDB)",
        "2007-FEB-02 06:16:24.111794 (TDB)",
        "2007-MAR-03 23:22:42.005064 (TDB)",
        "2007-APR-02 16:49:16.145506 (TDB)",
        "2007-MAY-02 09:41:43.840096 (TDB)",
        "2007-JUN-01 01:03:44.537483 (TDB)",
        "2007-JUN-30 14:15:26.586223 (TDB)",
        "2007-JUL-30 01:14:49.010797 (TDB)",
        "2007-AUG-28 10:39:01.398087 (TDB)",
        "2007-SEP-26 19:25:51.519413 (TDB)",
        "2007-OCT-26 04:30:56.635336 (TDB)",
        "2007-NOV-24 14:31:04.341632 (TDB)",
        "2007-DEC-24 01:40:12.245932 (TDB)",
    ]
    et0 = spice.str2et("2007 JAN 01")
    et1 = spice.str2et("2008 JAN 01")
    cnfine = spice.cell_double(2)
    spice.wninsd(et0, et1, cnfine)
    result = spice.cell_double(2000)
    spice.gfsep(
        "MOON",
        "SPHERE",
        "NULL",
        "SUN",
        "SPHERE",
        "NULL",
        "NONE",
        "EARTH",
        "LOCMAX",
        0.0,
        0.0,
        6.0 * spice.spd(),
        1000,
        cnfine,
        result,
    )
    count = spice.wncard(result)
    assert count == 13
    temp_results = []
    for i in range(0, count):
        start, end = spice.wnfetd(result, i)
        assert start == end
        temp_results.append(
            spice.timout(start, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND", 41)
        )
    assert temp_results == expected
    spice.kclear()


def test_gfsntc():
    spice.kclear()
    kernel = os.path.join(cwd, "gfnstc_test.tf")
    if spice.exists(kernel):
        os.remove(kernel)  # pragma: no cover # pragma: no cover
    with open(kernel, "w") as kernelFile:
        kernelFile.write("\\begindata\n")
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
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(kernel)
    et0 = spice.str2et("2007 JAN 01")
    et1 = spice.str2et("2008 JAN 01")
    cnfine = spice.cell_double(2)
    spice.wninsd(et0, et1, cnfine)
    result = spice.cell_double(2000)
    spice.gfsntc(
        "EARTH",
        "IAU_EARTH",
        "Ellipsoid",
        "NONE",
        "SUN",
        "SEM",
        [1.0, 0.0, 0.0],
        "LATITUDINAL",
        "LATITUDE",
        "=",
        0.0,
        0.0,
        90.0 * spice.spd(),
        1000,
        cnfine,
        result,
    )
    count = spice.wncard(result)
    assert count > 0
    beg, end = spice.wnfetd(result, 0)
    begstr = spice.timout(beg, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND", 80)
    endstr = spice.timout(end, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND", 80)
    assert begstr == "2007-MAR-21 00:01:25.527303 (TDB)"
    assert endstr == "2007-MAR-21 00:01:25.527303 (TDB)"
    beg, end = spice.wnfetd(result, 1)
    begstr = spice.timout(beg, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND", 80)
    endstr = spice.timout(end, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND", 80)
    assert begstr == "2007-SEP-23 09:46:39.606982 (TDB)"
    assert endstr == "2007-SEP-23 09:46:39.606982 (TDB)"
    spice.kclear()
    if spice.exists(kernel):
        os.remove(kernel)  # pragma: no cover # pragma: no cover


def test_gfsstp():
    spice.gfsstp(0.5)
    assert spice.gfstep(0.5) == 0.5


def test_gfstep():
    spice.gfsstp(0.5)
    assert spice.gfstep(0.5) == 0.5


def test_gfstol():
    spice.gfstol(1.0e-16)
    spice.gfstol(1.0e-6)


def test_gfsubc():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et0 = spice.str2et("2007 JAN 01")
    et1 = spice.str2et("2008 JAN 01")
    cnfine = spice.cell_double(2)
    spice.wninsd(et0, et1, cnfine)
    result = spice.cell_double(2000)
    spice.gfsubc(
        "earth",
        "iau_earth",
        "Near point: ellipsoid",
        "none",
        "sun",
        "geodetic",
        "latitude",
        ">",
        16.0 * spice.rpd(),
        0.0,
        spice.spd() * 90.0,
        1000,
        cnfine,
        result,
    )
    count = spice.wncard(result)
    assert count > 0
    start, end = spice.wnfetd(result, 0)
    start_time = spice.timout(
        start, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND", 41
    )
    end_time = spice.timout(end, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND", 41)
    assert start_time == "2007-MAY-04 17:08:56.724320 (TDB)"
    assert end_time == "2007-AUG-09 01:51:29.307830 (TDB)"
    spice.kclear()


def test_gftfov():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(CassiniKernels.cassCk)
    spice.furnsh(CassiniKernels.cassFk)
    spice.furnsh(CassiniKernels.cassIk)
    spice.furnsh(CassiniKernels.cassPck)
    spice.furnsh(CassiniKernels.cassSclk)
    spice.furnsh(CassiniKernels.cassTourSpk)
    spice.furnsh(CassiniKernels.satSpk)
    # Changed ABCORR to LT from LT+S for this test, so we do not need SSB
    # begin test
    # Cassini ISS NAC observed Enceladus on 2013-FEB-25 from ~11:00 to ~12:00
    # Split confinement window, from continuous CK coverage, into two pieces
    et_start1 = spice.str2et("2013-FEB-25 07:20:00.000")
    et_end1 = spice.str2et("2013-FEB-25 11:45:00.000")  # \
    et_start2 = spice.str2et("2013-FEB-25 11:55:00.000")  # _>synthetic 10min gap
    et_end2 = spice.str2et("2013-FEB-26 14:25:00.000")
    cnfine = spice.cell_double(4)
    spice.wninsd(et_start1, et_end1, cnfine)
    spice.wninsd(et_start2, et_end2, cnfine)
    # Subtract off the position of the spacecraft relative to the solar system barycenter the result is the ray's direction vector.
    result = spice.gftfov(
        "CASSINI_ISS_NAC",
        "ENCELADUS",
        "ELLIPSOID",
        "IAU_ENCELADUS",
        "LT",
        "CASSINI",
        10.0,
        cnfine,
    )
    # Verify the expected results
    assert spice.card(result) == 4
    sTimout = "YYYY-MON-DD HR:MN:SC UTC ::RND"
    assert spice.timout(result[0], sTimout) == "2013-FEB-25 10:42:33 UTC"
    assert spice.timout(result[1], sTimout) == "2013-FEB-25 11:45:00 UTC"
    assert spice.timout(result[2], sTimout) == "2013-FEB-25 11:55:00 UTC"
    assert spice.timout(result[3], sTimout) == "2013-FEB-25 12:04:30 UTC"
    # Cleanup
    spice.kclear()


def test_gfudb():
    spice.kclear()
    # load kernels
    spice.furnsh(CoreKernels.testMetaKernel)
    # begin test
    et_start = spice.str2et("Jan 1 2001")
    et_end = spice.str2et("Jan 1 2002")
    result = spice.cell_double(40000)
    cnfine = spice.cell_double(2)
    spice.wninsd(et_start, et_end, cnfine)
    step = 5.0 * spice.spd()

    # make a udf callback
    udf = spiceypy.utils.callbacks.SpiceUDFUNS(spice.udf)

    # define gfq
    @spiceypy.utils.callbacks.SpiceUDFUNB
    def gfq(udfunc, et):
        # we are not using udfunc in this example
        state, lt = spice.spkez(301, et, "IAU_EARTH", "NONE", 399)
        return state[2] >= 0.0 and state[5] > 0.0

    # call gfudb
    spice.gfudb(udf, gfq, step, cnfine, result)
    # count
    assert len(result) > 20  # true value is 28
    spice.kclear()


def test_gfudb2():
    spice.kclear()
    # load kernels
    spice.furnsh(CoreKernels.testMetaKernel)
    # begin test
    et_start = spice.str2et("Jan 1 2001")
    et_end = spice.str2et("Jan 1 2002")
    result = spice.cell_double(40000)
    cnfine = spice.cell_double(2)
    spice.wninsd(et_start, et_end, cnfine)
    step = 60.0 * 60.0

    # define gfq
    @spiceypy.utils.callbacks.SpiceUDFUNS
    def gfq(et):
        pos, lt = spice.spkezp(301, et, "IAU_EARTH", "NONE", 399)
        return pos[2]

    # define gfb
    @spiceypy.utils.callbacks.SpiceUDFUNB
    def gfb(udfuns, et):
        value = spiceypy.utils.callbacks.CallUDFUNS(udfuns, et)
        return -1000.0 <= value <= 1000.0

    # call gfudb
    spice.gfudb(gfq, gfb, step, cnfine, result)
    # count
    assert len(result) > 50  # true value is 56
    spice.kclear()


def test_gfuds():
    relations = ["=", "<", ">", "LOCMIN", "ABSMIN", "LOCMAX", "ABSMAX"]
    spice.kclear()
    # load kernels
    spice.furnsh(CoreKernels.testMetaKernel)
    # begin test
    et_start = spice.str2et("Jan 1 2007")
    et_end = spice.str2et("Apr 1 2007")
    # set up some constants
    step = spice.spd()
    adjust = 0.0
    refval = 0.3365

    # declare the callbacks we will use in the test
    @spiceypy.utils.callbacks.SpiceUDFUNS
    def gfq(et):
        state, lt = spice.spkez(301, et, "J2000", "NONE", 10)
        return spice.dvnorm(state)

    @spiceypy.utils.callbacks.SpiceUDFUNB
    def gfdecrx(udfuns, et):
        return spice.uddc(udfuns, et, 10.0)

    # loop through to test each relation type
    for i, r in enumerate(relations):
        result = spice.cell_double(40000)
        cnfine = spice.cell_double(2)
        spice.wninsd(et_start, et_end, cnfine)
        # call gfuds
        result = spice.gfuds(
            gfq, gfdecrx, r, refval, adjust, step, 20000, cnfine, result
        )
        assert len(result) > 0
    # cleanup
    spice.kclear()


def test_gipool():
    # same as pipool test
    spice.kclear()
    data = np.arange(0, 10)
    spice.pipool("pipool_array", data)
    ivals = spice.gipool("pipool_array", 0, 50)
    npt.assert_array_almost_equal(data, ivals)
    spice.kclear()


def test_gnpool():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    var = "BODY599*"
    index = 0
    room = 10
    expected = [
        "BODY599_POLE_DEC",
        "BODY599_LONG_AXIS",
        "BODY599_PM",
        "BODY599_RADII",
        "BODY599_POLE_RA",
        "BODY599_GM",
        "BODY599_NUT_PREC_PM",
        "BODY599_NUT_PREC_DEC",
        "BODY599_NUT_PREC_RA",
    ]
    kervar = spice.gnpool(var, index, room)
    spice.kclear()
    assert set(expected) == set(kervar)


def test_halfpi():
    assert spice.halfpi() == np.pi / 2


def test_hrmint():
    xvals = [-1.0, 0.0, 3.0, 5.0]
    yvals = [6.0, 3.0, 5.0, 0.0, 2210.0, 5115.0, 78180.0, 109395.0]
    answer, deriv = spice.hrmint(xvals, yvals, 2)
    assert answer == pytest.approx(141.0)
    assert deriv == pytest.approx(456.0)


def test_hx2dp():
    assert spice.hx2dp("1^1") == 1.0
    assert spice.hx2dp("7F5EB^5") == 521707.0
    assert spice.hx2dp("+1B^+2") == 27.0
    # Bad value
    badReturn = "ERROR: Illegal character 'Z' encountered."
    assert spice.hx2dp("1Z^+2")[: len(badReturn)] == badReturn


def test_ident():
    ident = spice.ident()
    expected = np.identity(3)
    npt.assert_array_almost_equal(ident, expected)


def test_illum():
    # Nearly the same as first half of test_edterm
    # possibly not smart to pick a terminator point for test.
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("2007 FEB 3 00:00:00.000")
    trgepc, obspos, trmpts = spice.edterm(
        "UMBRAL", "SUN", "MOON", et, "IAU_MOON", "LT+S", "EARTH", 3
    )
    expected_trmpts0 = [
        -1.53978381936825627463e02,
        -1.73056331949840728157e03,
        1.22893325627419600088e-01,
    ]
    npt.assert_array_almost_equal(trmpts[0], expected_trmpts0)
    phase, solar, emissn = spice.illum("MOON", et, "LT+S", "EARTH", trmpts[0])
    npt.assert_almost_equal(spice.dpr() * phase, 9.206597597007834)
    npt.assert_almost_equal(spice.dpr() * solar, 90.26976568986987)
    npt.assert_almost_equal(spice.dpr() * emissn, 99.27359835825851)
    spice.kclear()


def test_ilumin():
    # Same as first half of test_edterm
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("2007 FEB 3 00:00:00.000")
    trgepc, obspos, trmpts = spice.edterm(
        "UMBRAL", "SUN", "MOON", et, "IAU_MOON", "LT+S", "EARTH", 3
    )
    expected_trgepc = 223732863.86351672
    expected_obspos = [
        394721.1024056578753516078,
        27265.11780063395417528227,
        -19069.08478859506431035697,
    ]
    expected_trmpts0 = [
        -1.53978381936825627463e02,
        -1.73056331949840728157e03,
        1.22893325627419600088e-01,
    ]
    expected_trmpts1 = [
        87.37506200891714058798,
        864.40670594653545322217,
        1504.56817899807947469526,
    ]
    expected_trmpts2 = [42.213243378688254, 868.21134651980412, -1504.3223922609538]
    npt.assert_almost_equal(trgepc, expected_trgepc)
    npt.assert_array_almost_equal(obspos, expected_obspos)
    npt.assert_array_almost_equal(trmpts[0], expected_trmpts0)
    npt.assert_array_almost_equal(trmpts[1], expected_trmpts1)
    npt.assert_array_almost_equal(trmpts[2], expected_trmpts2)
    iluet0, srfvec0, phase0, solar0, emissn0 = spice.ilumin(
        "Ellipsoid", "MOON", et, "IAU_MOON", "LT+S", "EARTH", trmpts[0]
    )
    npt.assert_almost_equal(spice.dpr() * solar0, 90.269765819)
    iluet1, srfvec1, phase1, solar1, emissn1 = spice.ilumin(
        "Ellipsoid", "MOON", et, "IAU_MOON", "LT+S", "EARTH", trmpts[1]
    )
    npt.assert_almost_equal(spice.dpr() * solar1, 90.269765706)
    iluet2, srfvec2, phase2, solar2, emissn2 = spice.ilumin(
        "Ellipsoid", "MOON", et, "IAU_MOON", "LT+S", "EARTH", trmpts[2]
    )
    npt.assert_almost_equal(spice.dpr() * solar2, 90.269765730)
    spice.kclear()


def test_illumf():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(CassiniKernels.cassSclk)
    spice.furnsh(CassiniKernels.cassFk)
    spice.furnsh(CassiniKernels.cassPck)
    spice.furnsh(CassiniKernels.cassIk)
    spice.furnsh(CassiniKernels.cassSclk)
    spice.furnsh(CassiniKernels.satSpk)
    spice.furnsh(CassiniKernels.cassTourSpk)
    spice.furnsh(CassiniKernels.cassCk)
    et = spice.str2et("2013 FEB 25 11:50:00 UTC")
    # start of test
    camid = spice.bodn2c("CASSINI_ISS_NAC")
    shape, obsref, bsight, n, bounds = spice.getfov(camid, 4)
    # run sincpt on boresight vector
    spoint, etemit, srfvec = spice.sincpt(
        "Ellipsoid", "Enceladus", et, "IAU_ENCELADUS", "CN+S", "CASSINI", obsref, bsight
    )
    trgepc2, srfvec2, phase, incid, emissn, visibl, lit = spice.illumf(
        "Ellipsoid", "Enceladus", "Sun", et, "IAU_ENCELADUS", "CN+S", "CASSINI", spoint
    )
    phase = phase * spice.dpr()
    incid = incid * spice.dpr()
    emissn = emissn * spice.dpr()
    assert phase == pytest.approx(161.82854377660345)
    assert incid == pytest.approx(134.92108561449996)
    assert emissn == pytest.approx(63.23618556218115)
    assert not lit  # Incidence angle is greater than 90deg
    assert visibl  # Emission angle is less than 90deg
    spice.kclear()


def test_illumg():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(CassiniKernels.cassSclk)
    spice.furnsh(CassiniKernels.cassFk)
    spice.furnsh(CassiniKernels.cassPck)
    spice.furnsh(CassiniKernels.cassIk)
    spice.furnsh(CassiniKernels.cassSclk)
    spice.furnsh(CassiniKernels.satSpk)
    spice.furnsh(CassiniKernels.cassTourSpk)
    spice.furnsh(CassiniKernels.cassCk)
    et = spice.str2et("2013 FEB 25 11:50:00 UTC")
    spoint, trgepc, srfvec = spice.subpnt(
        "Near Point/Ellipsoid", "Enceladus", et, "IAU_ENCELADUS", "CN+S", "Earth"
    )
    trgepc2, srfvec2, phase, incid, emissn = spice.illumg(
        "Ellipsoid", "Enceladus", "Sun", et, "IAU_ENCELADUS", "CN+S", "CASSINI", spoint
    )
    phase = phase * spice.dpr()
    incid = incid * spice.dpr()
    emissn = emissn * spice.dpr()
    assert phase == pytest.approx(161.859925246638)
    assert incid == pytest.approx(18.47670084384343)
    assert emissn == pytest.approx(143.6546170649875)
    spice.kclear()


def test_inedpl():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    TIME = "Oct 31 2002, 12:55:00 PST"
    FRAME = "J2000"
    CORR = "LT+S"
    et = spice.str2et(TIME)
    state, ltime = spice.spkezr("EARTH", et, FRAME, CORR, "SUN")
    pos = state[0:3]
    dim, radii = spice.bodvrd("EARTH", "RADII", 3)
    pos = [pos[0] / radii[0] ** 2.0, pos[1] / radii[1] ** 2.0, pos[2] / radii[2] ** 2.0]
    plane = spice.nvc2pl(pos, 1.0)
    term = spice.inedpl(radii[0], radii[1], radii[2], plane)
    spice.kclear()
    expected_center = [0.21512031, 0.15544527, 0.067391641]
    expected_s_major = [
        -3.73561164720596843836e03,
        5.16970328302375583007e03,
        1.35988201424391742850e-11,
    ]
    expected_s_minor = [
        -1276.33357469839393161237,
        -922.27470443423590040766,
        6159.97371233560443215538,
    ]
    npt.assert_array_almost_equal(term.center, expected_center)
    npt.assert_array_almost_equal(term.semi_major, expected_s_major, decimal=5)
    npt.assert_array_almost_equal(term.semi_minor, expected_s_minor, decimal=5)
    npt.assert_almost_equal(spice.vnorm(term.semi_major), 6378.1365, decimal=2)
    npt.assert_almost_equal(spice.vnorm(term.semi_minor), 6358.0558, decimal=2)


def test_inelpl():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    dim, radii = spice.bodvrd("SATURN", "RADII", 3)
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
    spice.furnsh(CoreKernels.testMetaKernel)
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
    test_cell = spice.cell_char(10, 10)
    cList = ["aaa", "bbb", "ccc", "bbb"]
    for c in cList:
        spice.insrtc(c, test_cell)
    assert [x for x in test_cell] == ["aaa", "bbb", "ccc"]


def test_insrtc_vectorized():
    test_cell = spice.cell_char(10, 10)
    cList = ["aaa", "bbb", "ccc", "bbb"]
    spice.insrtc(cList, test_cell)
    assert [x for x in test_cell] == ["aaa", "bbb", "ccc"]


def test_insrtd():
    test_cell = spice.cell_double(8)
    dlist = [0.5, 2.0, 30.0, 0.01, 30.0]
    for d in dlist:
        spice.insrtd(d, test_cell)
    assert [x for x in test_cell] == [0.01, 0.5, 2.0, 30.0]


def test_insrtd_vectorized():
    test_cell = spice.cell_double(8)
    dList = [0.5, 2.0, 30.0, 0.01, 30.0]
    spice.insrtd(dList, test_cell)
    assert [x for x in test_cell] == [0.01, 0.5, 2.0, 30.0]


def test_insrti():
    test_cell = spice.cell_int(8)
    ilist = [1, 2, 30, 1, 30]
    for i in ilist:
        spice.insrti(i, test_cell)
    assert [x for x in test_cell] == [1, 2, 30]


def test_insrti_vectorized():
    test_cell = spice.cell_int(8)
    iList = [1, 2, 30, 1, 30]
    spice.insrti(iList, test_cell)
    assert [x for x in test_cell] == [1, 2, 30]


def test_inter():
    test_cell_one = spice.cell_int(8)
    test_cell_two = spice.cell_int(8)
    spice.insrti(1, test_cell_one)
    spice.insrti(2, test_cell_one)
    spice.insrti(1, test_cell_two)
    spice.insrti(3, test_cell_two)
    out_cell = spice.inter(test_cell_one, test_cell_two)
    assert [x for x in out_cell] == [1]
    # SPICECHAR_CELL
    test_cell_one = spice.cell_char(8, 8)
    test_cell_two = spice.cell_char(8, 8)
    spice.insrtc("1", test_cell_one)
    spice.insrtc("2", test_cell_one)
    spice.insrtc("1", test_cell_two)
    spice.insrtc("3", test_cell_two)
    out_cell = spice.inter(test_cell_one, test_cell_two)
    assert [x for x in out_cell] == ["1"]
    # SPICEDOUBLE_CELL
    test_cell_one = spice.cell_double(8)
    test_cell_two = spice.cell_double(8)
    spice.insrtd(1.0, test_cell_one)
    spice.insrtd(2.0, test_cell_one)
    spice.insrtd(1.0, test_cell_two)
    spice.insrtd(3.0, test_cell_two)
    out_cell = spice.inter(test_cell_one, test_cell_two)
    assert [x for x in out_cell] == [1.0]
    # SPICEBOOLEAN_CELL; dtype=4
    test_cell_one = spice.cell_bool(9)
    test_cell_two = spice.cell_bool(9)
    with pytest.raises(NotImplementedError):
        spice.inter(test_cell_one, test_cell_two)


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


def test_irfnam():
    assert spice.irfnam(1) == "J2000"
    assert spice.irfnam(13) == "GALACTIC"
    assert spice.irfnam(21) == "DE-143"


def test_irfnum():
    assert spice.irfnum("J2000") == 1
    assert spice.irfnum("GALACTIC") == 13
    assert spice.irfnum("DE-143") == 21


def test_irfrot():
    # get the rotation matrix from pxform
    expected_rotate = spice.pxform("B1950", "J2000", 0.0)
    # get hopefully the same rotation matrix from irfrot
    fromfrm = spice.irfnum("B1950")
    tofrm = spice.irfnum("J2000")
    actual_rotate = spice.irfrot(fromfrm, tofrm)
    npt.assert_array_almost_equal(actual_rotate, expected_rotate, decimal=4)


def test_irftrn():
    # get the rotation matrix from pxform
    expected_rotate = spice.pxform("B1950", "J2000", 0.0)
    # get hopefully the same rotation matrix from irfrot
    actual_rotate = spice.irftrn("B1950", "J2000")
    npt.assert_array_almost_equal(actual_rotate, expected_rotate, decimal=4)


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
    spice.furnsh(CoreKernels.testMetaKernel)
    file, ftype, source, handle = spice.kdata(0, "META", 400, 10, 50)
    assert ftype == "META"
    spice.kclear()


def test_kepleq():
    p = 10000.0
    gm = 398600.436
    ecc = 0.1
    a = p / (1.0 - ecc)
    n = np.sqrt(gm / a) / a
    argp = 30.0 * spice.rpd()
    node = 15.0 * spice.rpd()
    m0 = 45.0 * spice.rpd()
    epoch = -100000000.0
    et = epoch - 9750.0
    eqel_1 = ecc * np.sin(argp + node)
    eqel_2 = ecc * np.cos(argp + node)
    eqel_3 = m0 + argp + node
    dt = et - epoch
    dlp = 0.0
    can = np.cos(dlp)
    san = np.sin(dlp)
    h = eqel_1 * can + eqel_2 * san
    k = eqel_2 * can - eqel_1 * san
    ml = eqel_3 + ((n * dt) % spice.twopi())
    eecan = spice.kepleq(ml, h, k)
    assert pytest.approx(2.692595464274983, eecan)


def test_kinfo():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    filetype, source, handle = spice.kinfo(CoreKernels.testMetaKernel, 80, 80)
    assert filetype == "META"
    spice.kclear()


def test_kplfrm():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    cell = spice.kplfrm(-1)
    assert cell.size > 100
    spice.kclear()


def test_kpsolv():
    spice.kclear()
    r = 0.0
    for i in range(1, 20):
        theta = 0.0
        for j in range(1, 63):
            h = r * np.cos(theta)
            k = r * np.sin(theta)
            x = spice.kpsolv((h, k))
            fx = h * np.cos(x) + k * np.sin(x)
            assert pytest.approx(fx, x, 1.0e-15)
            theta = theta + 0.1
        r = r + 0.05
        pass
    spice.kclear()


def test_ktotal():
    spice.kclear()
    # same as unload test
    spice.furnsh(CoreKernels.testMetaKernel)
    # 4 kernels + the meta kernel = 5
    assert spice.ktotal("ALL") == 5
    spice.unload(CoreKernels.testMetaKernel)
    assert spice.ktotal("ALL") == 0
    spice.kclear()


def test_kxtrct():
    # Tests from examples at this URL:  https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/kxtrct_c.html#Examples
    i = 0
    while i < 500:
        i += 1
        assert (" TO 1 January 1987", "1 October 1984 12:00:00") == spice.kxtrct(
            "FROM",
            "from to beginning ending".upper().split(),
            4,
            "FROM 1 October 1984 12:00:00 TO 1 January 1987",
        )
        assert ("FROM 1 October 1984 12:00:00", "1 January 1987") == spice.kxtrct(
            "TO",
            "from to beginning ending".upper().split(),
            4,
            "FROM 1 October 1984 12:00:00 TO 1 January 1987",
        )
        assert (" PHONE: 354-4321", "4800 OAK GROVE DRIVE") == spice.kxtrct(
            "ADDRESS:",
            "address: phone: name:".upper().split(),
            3,
            "ADDRESS: 4800 OAK GROVE DRIVE PHONE: 354-4321 ",
        )
        assert ("ADDRESS: 4800 OAK GROVE DRIVE", "354-4321") == spice.kxtrct(
            "PHONE:",
            "address: phone: name:".upper().split(),
            3,
            "ADDRESS: 4800 OAK GROVE DRIVE PHONE: 354-4321 ",
        )
        with pytest.raises(spice.stypes.SpiceyError):
            spice.kxtrct(
                "NAME:",
                "address: phone: name:".upper().split(),
                3,
                "ADDRESS: 4800 OAK GROVE DRIVE PHONE: 354-4321 ",
            )


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
    npt.assert_array_almost_equal(
        expected2, spice.latcyl(1.0, 90.0 * spice.rpd(), 0.0), decimal=7
    )
    npt.assert_array_almost_equal(
        expected3, spice.latcyl(1.0, 180.0 * spice.rpd(), 0.0), decimal=7
    )


def test_latrec():
    expected1 = np.array([1.0, 0.0, 0.0])
    expected2 = np.array([0.0, 1.0, 0.0])
    expected3 = np.array([-1.0, 0.0, 0.0])
    npt.assert_array_almost_equal(expected1, spice.latrec(1.0, 0.0, 0.0), decimal=7)
    npt.assert_array_almost_equal(
        expected2, spice.latrec(1.0, 90.0 * spice.rpd(), 0.0), decimal=7
    )
    npt.assert_array_almost_equal(
        expected3, spice.latrec(1.0, 180.0 * spice.rpd(), 0.0), decimal=7
    )


def test_latsph():
    expected1 = np.array([1.0, 90.0 * spice.rpd(), 0.0])
    expected2 = np.array([1.0, 90.0 * spice.rpd(), 90.0 * spice.rpd()])
    expected3 = np.array([1.0, 90.0 * spice.rpd(), 180.0 * spice.rpd()])
    npt.assert_array_almost_equal(expected1, spice.latsph(1.0, 0.0, 0.0), decimal=7)
    npt.assert_array_almost_equal(
        expected2, spice.latsph(1.0, 90.0 * spice.rpd(), 0.0), decimal=7
    )
    npt.assert_array_almost_equal(
        expected3, spice.latsph(1.0, 180.0 * spice.rpd(), 0.0), decimal=7
    )


def test_latsrf():
    spice.kclear()
    spice.furnsh(ExtraKernels.phobosDsk)
    srfpts = spice.latsrf(
        "DSK/UNPRIORITIZED", "phobos", 0.0, "iau_phobos", [[0.0, 45.0], [60.0, 45.0]]
    )
    radii = [spice.recrad(x)[0] for x in srfpts]
    assert radii[0] > 9.77
    assert radii[1] > 9.51
    spice.kclear()


def test_lcase():
    assert spice.lcase("THIS IS AN EXAMPLE") == "THIS IS AN EXAMPLE".lower()
    assert spice.lcase("1234") == "1234"


def test_ldpool():
    spice.kclear()
    ldpool_names = [
        "DELTET/DELTA_T_A",
        "DELTET/K",
        "DELTET/EB",
        "DELTET/M",
        "DELTET/DELTA_AT",
    ]
    ldpool_lens = [1, 1, 1, 2, 46]
    textbuf = [
        "DELTET/DELTA_T_A = 32.184",
        "DELTET/K = 1.657D-3",
        "DELTET/EB  = 1.671D-2",
        "DELTET/M = ( 6.239996 1.99096871D-7 )",
        "DELTET/DELTA_AT = ( 10, @1972-JAN-1",
        "                     11, @1972-JUL-1",
        "                     12, @1973-JAN-1",
        "                     13, @1974-JAN-1",
        "                     14, @1975-JAN-1",
        "                     15, @1976-JAN-1",
        "                     16, @1977-JAN-1",
        "                     17, @1978-JAN-1",
        "                     18, @1979-JAN-1",
        "                     19, @1980-JAN-1",
        "                     20, @1981-JUL-1",
        "                     21, @1982-JUL-1",
        "                     22, @1983-JUL-1",
        "                     23, @1985-JUL-1",
        "                     24, @1988-JAN-1",
        "                     25, @1990-JAN-1",
        "                     26, @1991-JAN-1",
        "                     27, @1992-JUL-1",
        "                     28, @1993-JUL-1",
        "                     29, @1994-JUL-1",
        "                     30, @1996-JAN-1",
        "                     31, @1997-JUL-1",
        "                     32, @1999-JAN-1 )",
    ]
    kernel = os.path.join(cwd, "ldpool_test.tls")
    if spice.exists(kernel):
        os.remove(kernel)  # pragma: no cover
    with open(kernel, "w") as kernelFile:
        kernelFile.write("\\begindata\n")
        for line in textbuf:
            kernelFile.write(line + "\n")
        kernelFile.write("\\begintext\n")
        kernelFile.close()
    spice.ldpool(kernel)
    for var, expectLen in zip(ldpool_names, ldpool_lens):
        n, vartype = spice.dtpool(var)
        assert expectLen == n
        assert vartype == "N"
    spice.kclear()
    if spice.exists(kernel):
        os.remove(kernel)  # pragma: no cover


def test_lgrind():
    p, dp = spice.lgrind([-1.0, 0.0, 1.0, 3.0], [-2.0, -7.0, -8.0, 26.0], 2.0)
    assert p == pytest.approx(1.0)
    assert dp == pytest.approx(16.0)


def test_limbpt():
    spice.kclear()
    spice.furnsh(CoreKernels.spk)
    spice.furnsh(ExtraKernels.marsSpk)
    spice.furnsh(CoreKernels.pck)
    spice.furnsh(CoreKernels.lsk)
    spice.furnsh(ExtraKernels.phobosDsk)
    # set the time
    et = spice.str2et("1972 AUG 11 00:00:00")
    # call limpt
    npts, points, epochs, tangts = spice.limbpt(
        "TANGENT/DSK/UNPRIORITIZED",
        "Phobos",
        et,
        "IAU_PHOBOS",
        "CN+S",
        "CENTER",
        "MARS",
        [0.0, 0.0, 1.0],
        spice.twopi() / 3.0,
        3,
        1.0e-4,
        1.0e-7,
        10000,
    )
    assert points is not None
    assert len(points) == 3
    spice.kclear()


def test_lmpool():
    spice.kclear()
    lmpool_names = [
        "DELTET/DELTA_T_A",
        "DELTET/K",
        "DELTET/EB",
        "DELTET/M",
        "DELTET/DELTA_AT",
    ]
    lmpool_lens = [1, 1, 1, 2, 46]
    textbuf = [
        "DELTET/DELTA_T_A = 32.184",
        "DELTET/K = 1.657D-3",
        "DELTET/EB  = 1.671D-2",
        "DELTET/M = ( 6.239996 1.99096871D-7 )",
        "DELTET/DELTA_AT = ( 10, @1972-JAN-1",
        "                     11, @1972-JUL-1",
        "                     12, @1973-JAN-1",
        "                     13, @1974-JAN-1",
        "                     14, @1975-JAN-1",
        "                     15, @1976-JAN-1",
        "                     16, @1977-JAN-1",
        "                     17, @1978-JAN-1",
        "                     18, @1979-JAN-1",
        "                     19, @1980-JAN-1",
        "                     20, @1981-JUL-1",
        "                     21, @1982-JUL-1",
        "                     22, @1983-JUL-1",
        "                     23, @1985-JUL-1",
        "                     24, @1988-JAN-1",
        "                     25, @1990-JAN-1",
        "                     26, @1991-JAN-1",
        "                     27, @1992-JUL-1",
        "                     28, @1993-JUL-1",
        "                     29, @1994-JUL-1",
        "                     30, @1996-JAN-1",
        "                     31, @1997-JUL-1",
        "                     32, @1999-JAN-1 )",
    ]
    spice.lmpool(textbuf)
    for var, expectLen in zip(lmpool_names, lmpool_lens):
        n, vartype = spice.dtpool(var)
        assert expectLen == n
        assert vartype == "N"
    spice.kclear()


def test_lmpool_numpy():
    spice.kclear()
    lmpool_names = [
        "DELTET/DELTA_T_A",
        "DELTET/K",
        "DELTET/EB",
        "DELTET/M",
        "DELTET/DELTA_AT",
    ]
    lmpool_lens = [1, 1, 1, 2, 46]
    textbuf = np.array(
        [
            "DELTET/DELTA_T_A = 32.184",
            "DELTET/K = 1.657D-3",
            "DELTET/EB  = 1.671D-2",
            "DELTET/M = ( 6.239996 1.99096871D-7 )",
            "DELTET/DELTA_AT = ( 10, @1972-JAN-1",
            "                     11, @1972-JUL-1",
            "                     12, @1973-JAN-1",
            "                     13, @1974-JAN-1",
            "                     14, @1975-JAN-1",
            "                     15, @1976-JAN-1",
            "                     16, @1977-JAN-1",
            "                     17, @1978-JAN-1",
            "                     18, @1979-JAN-1",
            "                     19, @1980-JAN-1",
            "                     20, @1981-JUL-1",
            "                     21, @1982-JUL-1",
            "                     22, @1983-JUL-1",
            "                     23, @1985-JUL-1",
            "                     24, @1988-JAN-1",
            "                     25, @1990-JAN-1",
            "                     26, @1991-JAN-1",
            "                     27, @1992-JUL-1",
            "                     28, @1993-JUL-1",
            "                     29, @1994-JUL-1",
            "                     30, @1996-JAN-1",
            "                     31, @1997-JUL-1",
            "                     32, @1999-JAN-1 )",
        ]
    )
    spice.lmpool(textbuf)
    for var, expectLen in zip(lmpool_names, lmpool_lens):
        n, vartype = spice.dtpool(var)
        assert expectLen == n
        assert vartype == "N"
    spice.kclear()


def test_lmpoolstress():
    # occasional crash in lmpool believed to be caused by lenvals not being +=1'ed for end of line.
    for i in range(500):
        test_lmpool()


def test_lparse():
    stringtest = "one two three four"
    items = spice.lparse(stringtest, " ", 25)
    assert items == ["one", "two", "three", "four"]


def test_lparsm():
    stringtest = "  A number of words   separated   by spaces   "
    # Test with nmax (20) not equal to lenout (23), to ensure that
    # their purposes have not been switched within spice.lparsm()
    items = spice.lparsm(stringtest, " ", 20, lenout=23)
    assert items == ["A", "number", "of", "words", "separated", "by", "spaces"]
    # Test without lenout
    items = spice.lparsm(stringtest, " ", len(stringtest) + 10)
    assert items == ["A", "number", "of", "words", "separated", "by", "spaces"]


def test_lparss():
    stringtest = "  A number of words   separated   by spaces.   "
    delims = " ,."
    outset = spice.lparss(stringtest, delims)
    expected = ["", "A", "by", "number", "of", "separated", "spaces", "words"]
    assert [x for x in outset] == expected


def test_lspcn():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("21 march 2005")
    lon = spice.dpr() * spice.lspcn("EARTH", et, "NONE")
    spice.kclear()
    npt.assert_almost_equal(lon, 0.48153755894179384)


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
    spice.furnsh(CoreKernels.testMetaKernel)
    OBS = 399
    TARGET = 5
    TIME_STR = "July 4, 2004"
    et = spice.str2et(TIME_STR)
    arrive, ltime = spice.ltime(et, OBS, "->", TARGET)
    arrive_utc = spice.et2utc(arrive, "C", 3, 50)
    npt.assert_almost_equal(ltime, 2918.71705, decimal=4)
    assert arrive_utc == "2004 JUL 04 00:48:38.717"
    receive, rtime = spice.ltime(et, OBS, "<-", TARGET)
    receive_utc = spice.et2utc(receive, "C", 3, 50)
    spice.kclear()
    npt.assert_almost_equal(rtime, 2918.75247, decimal=4)
    assert receive_utc == "2004 JUL 03 23:11:21.248"


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
    assert spice.lxqstr('The "SPICE" system', '"', 4) == (10, 7)
    assert spice.lxqstr('The "SPICE" system', '"', 4) == (10, 7)
    assert spice.lxqstr('The "SPICE" system', '"', 0) == (-1, 0)
    assert spice.lxqstr('The "SPICE" system', "'", 4) == (3, 0)
    assert spice.lxqstr('The """SPICE"""" system', '"', 4) == (14, 11)
    assert spice.lxqstr("The &&&SPICE system", "&", 4) == (5, 2)
    assert spice.lxqstr("' '", "'", 0) == (2, 3)
    assert spice.lxqstr("''", "'", 0) == (1, 2)


def test_m2eul():
    ticam = [
        [0.49127379678135830, 0.50872620321864170, 0.70699908539882417],
        [-0.50872620321864193, -0.49127379678135802, 0.70699908539882428],
        [0.70699908539882406, -0.70699908539882439, 0.01745240643728360],
    ]
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
    np.testing.assert_array_almost_equal(expected, q, decimal=6)


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
    expected = np.array(
        [[1.0, 2.0, 3.0], [2.0, 4.0, 6.0], [3.0, 6.0, 9.0], [0.0, 0.0, 0.0]]
    )
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
    assert spice.namfrm("J2000") == 1


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
    expected_pnear = [1.0, 0.0, 0.0]
    expected_alt = 2.5
    npt.assert_almost_equal(alt, expected_alt)
    npt.assert_array_almost_equal(pnear, expected_pnear)


def test_npedln():
    linept = [1.0e6, 2.0e6, 3.0e6]
    a, b, c = 7.0e5, 7.0e5, 6.0e5
    linedr = [-4.472091234e-1, -8.944182469e-1, -4.472091234e-3]
    pnear, dist = spice.npedln(a, b, c, linept, linedr)
    expected_pnear = [-1633.3111, -3266.6222, 599991.83]
    expected_dist = 2389967.9
    npt.assert_almost_equal(dist, expected_dist, decimal=1)
    npt.assert_array_almost_equal(expected_pnear, pnear, decimal=2)


def test_npelpt():
    center = [1.0, 2.0, 3.0]
    smajor = [3.0, 0.0, 0.0]
    sminor = [0.0, 2.0, 0.0]
    point = [-4.0, 2.0, 1.0]
    expected_pnear = [-2.0, 2.0, 3.0]
    expected_dist = 2.8284271
    ellipse = spice.cgv2el(center, smajor, sminor)
    pnear, dist = spice.npelpt(point, ellipse)
    npt.assert_almost_equal(dist, expected_dist)
    npt.assert_array_almost_equal(expected_pnear, pnear)


def test_nplnpt():
    linept = [1.0, 2.0, 3.0]
    linedr = [0.0, 1.0, 1.0]
    point = [-6.0, 9.0, 10.0]
    pnear, dist = spice.nplnpt(linept, linedr, point)
    expected_pnear = [1.0, 9.0, 10.0]
    expected_dist = 7.0
    assert dist == expected_dist
    npt.assert_array_almost_equal(expected_pnear, pnear)


def test_nvc2pl():
    normal = [1.0, 1.0, 1.0]
    constant = 23.0
    expected_constant = 13.279056
    expected_normal = [0.57735027, 0.57735027, 0.57735027]
    plane = spice.nvc2pl(normal, constant)
    npt.assert_array_almost_equal(plane.normal, expected_normal)
    npt.assert_almost_equal(plane.constant, expected_constant, decimal=6)


def test_nvp2pl():
    normal = [1.0, 1.0, 1.0]
    point = [1.0, 4.0, 9.0]
    expected_constant = 8.0829038
    expected_normal = [0.57735027, 0.57735027, 0.57735027]
    plane = spice.nvp2pl(normal, point)
    npt.assert_array_almost_equal(plane.normal, expected_normal)
    npt.assert_almost_equal(plane.constant, expected_constant, decimal=6)


def test_occult():
    spice.kclear()
    # load kernels
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.earthStnSpk)
    spice.furnsh(ExtraKernels.earthHighPerPck)
    spice.furnsh(ExtraKernels.earthTopoTf)
    # start test
    # Mercury transited the Sun w.r.t. Earth-based observer ca. 2006-11-08 for about 5h
    # cf. https://science.nasa.gov/science-news/science-at-nasa/2006/20oct_transitofmercury
    # Mercury was occulted by the sun about six months later
    et_sun_transited_by_mercury = spice.str2et("2006-11-08T22:00")
    occult_code_one = spice.occult(
        "MERCURY",
        "point",
        " ",
        "SUN",
        "ellipsoid",
        "IAU_SUN",
        "CN",
        "DSS-13",
        et_sun_transited_by_mercury,
    )
    # Mercury is in front of the Sun as seen by observer (DSS-13)
    assert occult_code_one == 2  # SPICE_OCCULT_ANNLR2
    et_sun_mercury_both_visible = spice.str2et("2006-11-09T02:00")
    occult_code_two = spice.occult(
        "MERCURY",
        "point",
        " ",
        "SUN",
        "ellipsoid",
        "IAU_SUN",
        "CN",
        "DSS-13",
        et_sun_mercury_both_visible,
    )
    # Both Mercury and the Sun are visible to observer (DSS-13)
    assert occult_code_two == 0  # SPICE_OCCULT_NOOCC
    et_sun_totally_occulted_mercury = spice.str2et("2007-05-03T05:00")
    occult_code_three = spice.occult(
        "MERCURY",
        "point",
        " ",
        "SUN",
        "ellipsoid",
        "IAU_SUN",
        "CN",
        "DSS-13",
        et_sun_totally_occulted_mercury,
    )
    # The Sun is in front of Mercury as seen by observer (DSS-13)
    assert occult_code_three == -3  # SPICE_OCCULT_TOTAL1
    # cleanup
    spice.kclear()


def test_ordc():
    charset = spice.cell_char(10, 10)
    inputs = ["8", "1", "2", "9", "7", "4", "10"]
    expected = [5, 0, 2, 6, 4, 3, 1]
    for c in inputs:
        spice.insrtc(c, charset)
    for i, e in zip(inputs, expected):
        assert e == spice.ordc(i, charset)


def test_ordd():
    doubleset = spice.cell_double(7)
    inputs = [8.0, 1.0, 2.0, 9.0, 7.0, 4.0, 10.0]
    expected = [4, 0, 1, 5, 3, 2, 6]
    for d in inputs:
        spice.insrtd(d, doubleset)
    for i, e in zip(inputs, expected):
        assert e == spice.ordd(i, doubleset)


def test_ordi():
    intset = spice.cell_int(7)
    inputs = [8, 1, 2, 9, 7, 4, 10]
    expected = [4, 0, 1, 5, 3, 2, 6]
    for i in inputs:
        spice.insrti(i, intset)
    for i, e in zip(inputs, expected):
        assert e == spice.ordi(i, intset)


def test_orderc():
    inarray = ["a", "abc", "ab"]
    expected_order = [0, 2, 1]
    order = spice.orderc(inarray)
    npt.assert_array_almost_equal(expected_order, order)
    # Using ndim
    order = spice.orderc(inarray, ndim=len(inarray))
    npt.assert_array_almost_equal(expected_order, order)


def test_orderd():
    inarray = [0.0, 2.0, 1.0]
    expected_order = [0, 2, 1]
    order = spice.orderd(inarray)
    npt.assert_array_almost_equal(expected_order, order)
    # Using ndim
    order = spice.orderd(inarray, ndim=len(inarray))
    npt.assert_array_almost_equal(expected_order, order)


def test_orderi():
    inarray = [0, 2, 1]
    expected_order = [0, 2, 1]
    order = spice.orderi(inarray)
    npt.assert_array_almost_equal(expected_order, order)
    # Using ndim
    order = spice.orderi(inarray, ndim=len(inarray))
    npt.assert_array_almost_equal(expected_order, order)


def test_oscelt():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("Dec 25, 2007")
    state, ltime = spice.spkezr("Moon", et, "J2000", "LT+S", "EARTH")
    mass_earth = spice.bodvrd("EARTH", "GM", 1)
    elts = spice.oscelt(state, et, mass_earth[0])
    expected = [
        3.65914105273643566761e05,
        4.23931145731340453494e05,
        4.87177926278510253777e-01,
        6.18584206992959551030e00,
        1.88544634402406319218e00,
        1.86769787246217056236e04,
        2.51812865183709204197e08,
        1.00000000000000000000e00,
    ]
    npt.assert_array_almost_equal(elts, expected, decimal=4)
    spice.kclear()


def test_oscltx_stress():
    for i in range(0, 30):
        test_oscltx()


def test_oscltx():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("Dec 25, 2007")
    state, ltime = spice.spkezr("Moon", et, "J2000", "LT+S", "EARTH")
    mass_earth = spice.bodvrd("EARTH", "GM", 1)
    elts = spice.oscltx(state, et, mass_earth[0])
    expected = [
        3.65914105273643566761e05,
        4.23931145731340453494e05,
        4.87177926278510253777e-01,
        6.18584206992959551030e00,
        1.88544634402406319218e00,
        1.86769787246217056236e04,
        2.51812865183709204197e08,
        1.00000000000000000000e00,
        4.40283687897870881778e-02,
        -8.63147169311087925081e-01,
        0.00000000000000000000e00,
    ]
    npt.assert_array_almost_equal(elts, expected, decimal=4)
    spice.kclear()


def test_pckopn_pckw02_pckcls():
    pck = os.path.join(cwd, "test_pck.pck")
    if spice.exists(pck):
        os.remove(pck)  # pragma: no cover
    spice.kclear()
    handle = spice.pckopn(pck, "Test PCK file", 5000)
    spice.pckw02(
        handle, 301, "j2000", 0.0, 3.0, "segid", 1.0, 3, 1, [1.0, 2.0, 3.0], 0.0
    )
    spice.pckcls(handle)
    spice.kclear()
    if spice.exists(pck):
        os.remove(pck)  # pragma: no cover


def test_pckcov():
    spice.kclear()
    ids = spice.cell_int(1000)
    cover = spice.cell_double(2000)
    spice.pckfrm(ExtraKernels.earthHighPerPck, ids)
    spice.scard(0, cover)
    spice.pckcov(ExtraKernels.earthHighPerPck, ids[0], cover)
    result = [x for x in cover]
    expected = [94305664.18380372, 757080064.1838132]
    npt.assert_array_almost_equal(result, expected)
    spice.kclear()


def test_pckfrm():
    spice.kclear()
    ids = spice.cell_int(1000)
    spice.pckfrm(ExtraKernels.earthHighPerPck, ids)
    assert ids[0] == 3000
    spice.kclear()


def test_pcklof():
    spice.kclear()
    handle = spice.pcklof(ExtraKernels.earthHighPerPck)
    assert handle != -1
    spice.pckuof(handle)
    spice.kclear()


def test_pckuof():
    spice.kclear()
    handle = spice.pcklof(ExtraKernels.earthHighPerPck)
    assert handle != -1
    spice.pckuof(handle)
    spice.kclear()


def test_pcpool():
    import string

    spice.kclear()
    data = [j + str(i) for i, j in enumerate(list(string.ascii_lowercase))]
    spice.pcpool("pcpool_test", data)
    cvals = spice.gcpool("pcpool_test", 0, 30, 4)
    assert data == cvals
    spice.kclear()


def test_pdpool():
    spice.kclear()
    data = np.arange(0.0, 10.0)
    spice.pdpool("pdpool_array", data)
    dvals = spice.gdpool("pdpool_array", 0, 30)
    npt.assert_array_almost_equal(data, dvals)
    spice.kclear()


def test_pgrrec():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    n, radii = spice.bodvrd("MARS", "RADII", 3)
    re = radii[0]
    rp = radii[2]
    f = (re - rp) / re
    rectan = spice.pgrrec("Mars", 90.0 * spice.rpd(), 45 * spice.rpd(), 300, re, f)
    expected = [1.604650025e-13, -2.620678915e3, 2.592408909e3]
    npt.assert_array_almost_equal(rectan, expected)
    spice.kclear()


def test_phaseq():
    relate = ["=", "<", ">", "LOCMIN", "ABSMIN", "LOCMAX", "ABSMAX"]
    expected = {
        "=": [
            0.575988450,
            0.575988450,
            0.575988450,
            0.575988450,
            0.575988450,
            0.575988450,
            0.575988450,
            0.575988450,
            0.575988450,
            0.575988450,
        ],
        "<": [
            0.575988450,
            0.575988450,
            0.575988450,
            0.575988450,
            0.575988450,
            0.468279091,
        ],
        ">": [
            0.940714974,
            0.575988450,
            0.575988450,
            0.575988450,
            0.575988450,
            0.575988450,
        ],
        "LOCMIN": [0.086121423, 0.086121423, 0.079899769, 0.079899769],
        "ABSMIN": [0.079899769, 0.079899769],
        "LOCMAX": [3.055062862, 3.055062862, 3.074603891, 3.074603891],
        "ABSMAX": [3.074603891, 3.074603891],
    }
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et0 = spice.str2et("2006 DEC 01")
    et1 = spice.str2et("2007 JAN 31")
    cnfine = spice.cell_double(2)
    spice.wninsd(et0, et1, cnfine)
    result = spice.cell_double(10000)
    for relation in relate:
        spice.gfpa(
            "Moon",
            "Sun",
            "LT+S",
            "Earth",
            relation,
            0.57598845,
            0.0,
            spice.spd(),
            5000,
            cnfine,
            result,
        )
        count = spice.wncard(result)
        if count > 0:
            temp_results = []
            for i in range(0, count):
                start, stop = spice.wnfetd(result, i)
                startPhase = spice.phaseq(start, "moon", "sun", "earth", "lt+s")
                stopPhase = spice.phaseq(stop, "moon", "sun", "earth", "lt+s")
                temp_results.append(startPhase)
                temp_results.append(stopPhase)
            npt.assert_array_almost_equal(temp_results, expected.get(relation))
    spice.kclear()


def test_pi():
    assert spice.pi() == np.pi


def test_pipool():
    spice.kclear()
    data = np.arange(0, 10)
    spice.pipool("pipool_array", data)
    ivals = spice.gipool("pipool_array", 0, 50)
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
    expected_s_major = [2.0, 0.0, 0.0]
    expected_s_minor = [0.0, 1.0, 0.0]
    expected_center = [1.0, 1.0, 0.0]
    npt.assert_array_almost_equal(expected_center, ellipse.center)
    npt.assert_array_almost_equal(expected_s_major, ellipse.semi_major)
    npt.assert_array_almost_equal(expected_s_minor, ellipse.semi_minor)


def test_pl2nvc():
    normal = [-1.0, 5.0, -3.5]
    point = [9.0, -0.65, -12.0]
    plane = spice.nvp2pl(normal, point)
    normal, constant = spice.pl2nvc(plane)
    expected_normal = [-0.16169042, 0.80845208, -0.56591646]
    npt.assert_almost_equal(constant, 4.8102899, decimal=6)
    npt.assert_array_almost_equal(expected_normal, normal, decimal=6)


def test_pl2nvp():
    plane_norm = [2.44, -5.0 / 3.0, 11.0 / 9.0]
    const = 3.141592654
    plane = spice.nvc2pl(plane_norm, const)
    norm_vec, point = spice.pl2nvp(plane)
    expected_point = [0.74966576, -0.51206678, 0.37551564]
    npt.assert_array_almost_equal(expected_point, point)


def test_pl2psv():
    normal = [-1.0, 5.0, -3.5]
    point = [9.0, -0.65, -12.0]
    plane = spice.nvp2pl(normal, point)
    point, span1, span2 = spice.pl2psv(plane)
    npt.assert_almost_equal(spice.vdot(point, span1), 0)
    npt.assert_almost_equal(spice.vdot(point, span2), 0)
    npt.assert_almost_equal(spice.vdot(span1, span2), 0)


def test_pltar():
    vrtces = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    plates = [[1, 4, 3], [1, 2, 4], [1, 3, 2], [2, 3, 4]]
    assert spice.pltar(vrtces, plates) == pytest.approx(2.3660254037844)


def test_pltexp():
    iverts = [
        [np.sqrt(3.0) / 2.0, -0.5, 7.0],
        [0.0, 1.0, 7.0],
        [-np.sqrt(3.0) / 2.0, -0.5, 7.0],
    ]
    overts = spice.pltexp(iverts, 1.0)
    expected = [
        [1.732050807569, -1.0, 7.0],
        [0.0, 2.0, 7.0],
        [-1.732050807569, -1.0, 7.0],
    ]
    npt.assert_array_almost_equal(expected, overts)


def test_pltnp():
    point = [2.0, 2.0, 2.0]
    v1 = [1.0, 0.0, 0.0]
    v2 = [0.0, 1.0, 0.0]
    v3 = [0.0, 0.0, 1.0]
    near, distance = spice.pltnp(point, v1, v2, v3)
    npt.assert_array_almost_equal([1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0], near)
    assert distance == pytest.approx(2.8867513)


def test_pltnrm():
    v1 = [np.sqrt(3.0) / 2.0, -0.5, 0.0]
    v2 = [0.0, 1.0, 0.0]
    v3 = [-np.sqrt(3.0) / 2.0, -0.5, 0.0]
    npt.assert_array_almost_equal([0.0, 0.0, 2.59807621135], spice.pltnrm(v1, v2, v3))


def test_pltvol():
    vrtces = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    plates = [[1, 4, 3], [1, 2, 4], [1, 3, 2], [2, 3, 4]]
    assert spice.pltvol(vrtces, plates) == pytest.approx(1.0 / 6.0)


def test_polyds():
    result = spice.polyds([1.0, 3.0, 0.5, 1.0, 0.5, -1.0, 1.0], 6, 3, 1)
    npt.assert_array_almost_equal([6.0, 10.0, 23.0, 78.0], result)


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
    pvinit = np.array(
        [
            0.0,
            r / np.sqrt(2.0),
            r / np.sqrt(2.0),
            0.0,
            -speed / np.sqrt(2.0),
            speed / np.sqrt(2.0),
        ]
    )
    state = np.array(spice.prop2b(mu, pvinit, t))
    npt.assert_array_almost_equal(state, -1.0 * pvinit, decimal=6)


def test_prsdp():
    assert spice.prsdp("-1. 000") == -1.0


def test_prsint():
    assert spice.prsint("PI") == 3


def test_psv2pl():
    spice.kclear()
    epoch = "Jan 1 2005"
    frame = "ECLIPJ2000"
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et(epoch)
    state, ltime = spice.spkezr("EARTH", et, frame, "NONE", "Solar System Barycenter")
    es_plane = spice.psv2pl(state[0:3], state[0:3], state[3:6])
    es_norm, es_const = spice.pl2nvc(es_plane)
    mstate, mltime = spice.spkezr("MOON", et, frame, "NONE", "EARTH BARYCENTER")
    em_plane = spice.psv2pl(mstate[0:3], mstate[0:3], mstate[3:6])
    em_norm, em_const = spice.pl2nvc(em_plane)
    spice.kclear()
    npt.assert_almost_equal(
        spice.vsep(es_norm, em_norm) * spice.dpr(), 5.0424941, decimal=6
    )


def test_pxform():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    lon = 118.25 * spice.rpd()
    lat = 34.05 * spice.rpd()
    alt = 0.0
    utc = "January 1, 2005"
    et = spice.str2et(utc)
    len, abc = spice.bodvrd("EARTH", "RADII", 3)
    equatr = abc[0]
    polar = abc[2]
    f = (equatr - polar) / equatr
    epos = spice.georec(lon, lat, alt, equatr, f)
    rotate = np.array(spice.pxform("IAU_EARTH", "J2000", et))
    spice.kclear()
    jstate = np.dot(epos, rotate)
    expected = np.array([5042.1309421, 1603.52962986, 3549.82398086])
    npt.assert_array_almost_equal(jstate, expected, decimal=4)


def test_pxfrm2():
    spice.kclear()
    # load kernels
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(CassiniKernels.cassSclk)
    spice.furnsh(CassiniKernels.cassFk)
    spice.furnsh(CassiniKernels.cassPck)
    spice.furnsh(CassiniKernels.cassIk)
    spice.furnsh(CassiniKernels.cassSclk)
    spice.furnsh(CassiniKernels.satSpk)
    spice.furnsh(CassiniKernels.cassTourSpk)
    spice.furnsh(CassiniKernels.cassCk)
    # start of test
    etrec = spice.str2et("2013 FEB 25 11:50:00 UTC")
    camid = spice.bodn2c("CASSINI_ISS_NAC")
    shape, obsref, bsight, n, bounds = spice.getfov(camid, 4)
    # run sincpt on boresight vector
    spoint, etemit, srfvec = spice.sincpt(
        "Ellipsoid",
        "Enceladus",
        etrec,
        "IAU_ENCELADUS",
        "CN+S",
        "CASSINI",
        obsref,
        bsight,
    )
    rotate = spice.pxfrm2(obsref, "IAU_ENCELADUS", etrec, etemit)
    # get radii
    num_vals, radii = spice.bodvrd("Enceladus", "RADII", 3)
    # find position of center with respect to MGS
    pcassmr = spice.vsub(spoint, srfvec)
    # rotate into IAU_MARS
    bndvec = spice.mxv(rotate, spice.vlcom(0.9999, bsight, 0.0001, bounds[1]))
    # get surface point
    spoint = spice.surfpt(pcassmr, bndvec, radii[0], radii[1], radii[2])
    radius, lon, lat = spice.reclat(spoint)
    lon *= spice.dpr()
    lat *= spice.dpr()
    # test output
    npt.assert_almost_equal(radius, 250.14507342586242, decimal=5)
    npt.assert_almost_equal(lon, 125.42089677611104, decimal=5)
    npt.assert_almost_equal(lat, -6.3718522103931585, decimal=5)
    # end of test
    spice.kclear()


def test_q2m():
    mout = spice.q2m(np.array([0.5, 0.4, 0.3, 0.1]))
    expected = np.array(
        [
            [0.607843137254902, 0.27450980392156854, 0.7450980392156862],
            [0.6666666666666666, 0.33333333333333326, -0.6666666666666666],
            [-0.43137254901960775, 0.9019607843137255, 0.019607843137254832],
        ]
    )
    assert np.array_equal(expected, mout)


def test_qcktrc():
    spice.reset()
    spice.chkin("test")
    spice.chkin("qcktrc")
    trace = spice.qcktrc(40)
    assert trace == "test --> qcktrc"
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
    npt.assert_array_almost_equal(
        [0.0, 1.0, 0.0], spice.radrec(1.0, 90.0 * spice.rpd(), 0.0)
    )
    npt.assert_array_almost_equal(
        [0.0, 0.0, 1.0], spice.radrec(1.0, 0.0, 90.0 * spice.rpd())
    )


def test_rav2xf():
    e = [1.0, 0.0, 0.0]
    rz = [[0.0, 1.0, 0.0], [-1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
    assert spice.rav2xf(rz, e) is not None


def test_raxisa():
    axis = [1.0, 2.0, 3.0]
    angle = 0.1 * spice.twopi()
    rotate_matrix = spice.axisar(axis, angle)
    axout, angout = spice.raxisa(rotate_matrix)
    expected_angout = [0.26726124, 0.53452248, 0.80178373]
    npt.assert_approx_equal(angout, 0.62831853, significant=7)
    npt.assert_array_almost_equal(axout, expected_angout)


def test_rdtext():
    import datetime

    # Create ISO UTC datetime string using current time
    utcnow = datetime.datetime.utcnow().isoformat()
    spice.reset()
    spice.kclear()
    # Create temporary filenames
    RDTEXT = os.path.join(cwd, "ex_rdtext.txt")
    xRDTEXT = os.path.join(cwd, "xex_rdtext.txt")
    # Ensure files do not exist
    if spice.exists(RDTEXT):
        os.remove(RDTEXT)  # pragma no cover
    if spice.exists(xRDTEXT):
        os.remove(xRDTEXT)  # pragma no cover
    # Open new file using FORTRAN SPICE TXTOPN
    unit = spice.txtopn(RDTEXT)
    xunit = spice.txtopn(xRDTEXT)
    # Build base lines
    writln_lines = ["{} writln_ to x.txt {}".format(c, utcnow) for c in "12"]
    xwritln_lines = ["x{}".format(writln_line) for writln_line in writln_lines]
    # Write lines to the files using FORTRAN SPICE WRITLN
    for writln_line in writln_lines:
        xwritln_line = "x{}".format(
            writln_line,
        )
        spice.writln(writln_line, unit)
        spice.writln(xwritln_line, xunit)
    # Close the FORTRAN logical units using ftncls
    spice.ftncls(unit)
    spice.ftncls(xunit)
    # Ensure the FORTRAN logical units can no longer be retrieved ...
    # ... first file, RDTEXT
    with pytest.raises(spice.stypes.SpiceyError):
        closed_unit = spice.fn2lun(RDTEXT)
    spice.reset()
    # ... second file, xRDTEXT
    with pytest.raises(spice.stypes.SpiceyError):
        xclosed_unit = spice.fn2lun(xRDTEXT)
    spice.reset()

    # Wrapper function to call spice.rdtext and assert expected result
    def rdtext_helper(filename, expected_line, expected_done):
        read_line, done = spice.rdtext(filename, 99)
        assert (read_line == expected_line) and (done is expected_done)

    #
    rdtext_helper(RDTEXT, writln_lines[0], False)  # Read first line from RDTEXT
    rdtext_helper(RDTEXT, writln_lines[1], False)  # Read second line from RDTEXT
    rdtext_helper(
        RDTEXT, "", True
    )  # Read another time from RDTEXT to confirm done will be set to True at end of file
    rdtext_helper(
        RDTEXT, writln_lines[0], False
    )  # Read another time from RDTEXT to confirm file will be re-opened
    spice.cltext(RDTEXT)  # Close text file.
    # Read two files in interleaved (1, 2, 2, 1) sequence to verify that can be done
    rdtext_helper(RDTEXT, writln_lines[0], False)  # Read first  line from RDTEXT
    rdtext_helper(xRDTEXT, xwritln_lines[0], False)  # Read first  line from xRDTEXT
    rdtext_helper(xRDTEXT, xwritln_lines[1], False)  # Read second line from xRDTEXT
    rdtext_helper(RDTEXT, writln_lines[1], False)  # Read second line from RDTEXT
    # Check end-of-file cases
    rdtext_helper(RDTEXT, "", True)
    rdtext_helper(xRDTEXT, "", True)
    # Cleanup
    spice.reset()
    spice.kclear()
    if spice.exists(RDTEXT):
        os.remove(RDTEXT)  # pragma no cover
    assert not spice.failed()
    if spice.exists(xRDTEXT):
        os.remove(xRDTEXT)  # pragma no cover


def test_reccyl():
    expected1 = np.array([0.0, 0.0, 0.0])
    expected2 = np.array([1.0, 90.0 * spice.rpd(), 0.0])
    expected3 = np.array([1.0, 270.0 * spice.rpd(), 0.0])
    npt.assert_array_almost_equal(expected1, spice.reccyl([0.0, 0.0, 0.0]), decimal=7)
    npt.assert_array_almost_equal(expected2, spice.reccyl([0.0, 1.0, 0.0]), decimal=7)
    npt.assert_array_almost_equal(expected3, spice.reccyl([0.0, -1.0, 0.0]), decimal=7)


def test_recgeo():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
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
    spice.furnsh(CoreKernels.testMetaKernel)
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
    assert spice.recsph(v1) == (1.0, np.pi / 2, np.pi)


def test_removc():
    cell = spice.cell_char(10, 10)
    items = ["one", "two", "three", "four"]
    for i in items:
        spice.insrtc(i, cell)
    remove_items = ["three", "four"]
    for r in remove_items:
        spice.removc(r, cell)
    expected = ["one", "two"]
    assert expected == [x for x in cell]


def test_removd():
    cell = spice.cell_double(10)
    items = [0.0, 1.0, 1.0, 2.0, 3.0, 5.0, 8.0, 13.0, 21.0]
    for i in items:
        spice.insrtd(i, cell)
    remove_items = [0.0, 2.0, 4.0, 6.0, 8.0, 12.0]
    for r in remove_items:
        spice.removd(r, cell)
    expected = [1.0, 3.0, 5.0, 13.0, 21.0]
    for x, y in zip(cell, expected):
        assert x == y


def test_removi():
    cell = spice.cell_int(10)
    items = [0, 1, 1, 2, 3, 5, 8, 13, 21]
    for i in items:
        spice.insrti(i, cell)
    remove_items = [0, 2, 4, 6, 8, 12]
    for r in remove_items:
        spice.removi(r, cell)
    expected = [1, 3, 5, 13, 21]
    for x, y in zip(cell, expected):
        assert x == y


def test_reordc():
    array = ["one", "three", "two", "zero"]
    iorder = [3, 0, 2, 1]
    outarray = spice.reordc(iorder, 4, 5, array)
    # reordc appears to be broken...
    with pytest.raises(AssertionError):
        assert outarray == ["zero", "one", "two", "three"]


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
    npt.assert_array_almost_equal(outarray, [True, False, True])


def test_repmc():
    stringtestone = "The truth is #"
    outstringone = spice.repmc(stringtestone, "#", "SPICE")
    assert outstringone == "The truth is SPICE"


def test_repmct():
    stringtestone = "The value is #"
    outstringone = spice.repmct(stringtestone, "#", 5, "U")
    outstringtwo = spice.repmct(stringtestone, "#", 5, "l")
    assert outstringone == "The value is FIVE"
    assert outstringtwo == "The value is five"


def test_repmd():
    stringtestone = "The value is #"
    outstringone = spice.repmd(stringtestone, "#", 5.0e11, 1)
    assert outstringone == "The value is 5.E+11"


def test_repmf():
    stringtestone = "The value is #"
    outstringone = spice.repmf(stringtestone, "#", 5.0e3, 5, "f")
    outstringtwo = spice.repmf(stringtestone, "#", -5.2e-9, 3, "e")
    assert outstringone == "The value is 5000.0"
    assert outstringtwo == "The value is -5.20E-09"


def test_repmi():
    stringtest = "The value is <opcode>"
    outstring = spice.repmi(stringtest, "<opcode>", 5)
    assert outstring == "The value is 5"


def test_repmot():
    stringtestone = "The value is #"
    outstringone = spice.repmot(stringtestone, "#", 5, "U")
    outstringtwo = spice.repmot(stringtestone, "#", 5, "l")
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
    mExpected = [
        [np.sqrt(2) / 2.0, np.sqrt(2) / 2.0, 0.0],
        [-np.sqrt(2) / 2.0, np.sqrt(2) / 2.0, 0.0],
        [0.0, 0.0, 1.0],
    ]
    npt.assert_array_almost_equal(mout, mExpected)


def test_rotmat():
    ident = spice.ident()
    expected_r = [[0.0, 0.0, -1.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]]
    r_out = spice.rotmat(ident, spice.halfpi(), 2)
    npt.assert_array_almost_equal(r_out, expected_r)


def test_rotvec():
    vin = [np.sqrt(2), 0.0, 0.0]
    angle = spice.pi() / 4
    iaxis = 3
    v_expected = [1.0, -1.0, 0.0]
    vout = spice.rotvec(vin, angle, iaxis)
    npt.assert_array_almost_equal(vout, v_expected)


def test_rpd():
    assert spice.rpd() == np.arccos(-1.0) / 180.0


def test_rquad():
    # solve x^2 + 2x + 3 = 0
    root1, root2 = spice.rquad(1.0, 2.0, 3.0)
    expected_root_one = [-1.0, np.sqrt(2.0)]
    expected_root_two = [-1.0, -np.sqrt(2.0)]
    npt.assert_array_almost_equal(root1, expected_root_one)
    npt.assert_array_almost_equal(root2, expected_root_two)


def test_saelgv():
    vec1 = [1.0, 1.0, 1.0]
    vec2 = [1.0, -1.0, 1.0]
    expected_s_major = [np.sqrt(2.0), 0.0, np.sqrt(2.0)]
    expected_s_minor = [0.0, np.sqrt(2.0), 0.0]
    smajor, sminor = spice.saelgv(vec1, vec2)
    npt.assert_array_almost_equal(smajor, expected_s_major)
    npt.assert_array_almost_equal(sminor, expected_s_minor)


def test_scard():
    cell = spice.cell_double(10)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    assert spice.card(cell) == 0
    for w in darray:
        spice.wninsd(w[0], w[1], cell)
    assert spice.card(cell) == 6
    spice.scard(0, cell)
    assert spice.card(cell) == 0


def test_scdecd():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.voyagerSclk)
    timein = spice.scencd(-32, "2/20538:39:768")
    sclkch = spice.scdecd(-32, timein)
    assert sclkch == "2/20538:39:768"
    spice.kclear()


def test_sce2c():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.voyagerSclk)
    et = spice.str2et("1979 JUL 05 21:50:21.23379")
    sclkdp = spice.sce2c(-32, et)
    npt.assert_almost_equal(sclkdp, 985327949.9999709, decimal=6)
    spice.kclear()


def test_sce2s():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.voyagerSclk)
    et = spice.str2et("1979 JUL 05 21:50:21.23379")
    sclkch = spice.sce2s(-32, et)
    assert sclkch == "2/20538:39:768"
    spice.kclear()


def test_sce2t():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.voyagerSclk)
    et = spice.str2et("1979 JUL 05 21:50:21.23379")
    sclkdp = spice.sce2t(-32, et)
    npt.assert_almost_equal(sclkdp, 985327950.000000)
    spice.kclear()


def test_scencd():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.voyagerSclk)
    sclkch = spice.scdecd(-32, 985327950.0, 50)
    sclkdp = spice.scencd(-32, sclkch)
    npt.assert_almost_equal(sclkdp, 985327950.0)
    assert sclkch == "2/20538:39:768"
    spice.kclear()


def test_scencd_vectorized():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.voyagerSclk)
    sclkch = "2/20538:39:768"
    sclkdp = spice.scencd(-32, 3 * [sclkch])
    npt.assert_almost_equal(sclkdp, 3 * [985327950.0], decimal=6)
    spice.kclear()


def test_scfmt():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.voyagerSclk)
    pstart, pstop = spice.scpart(-32)
    start = spice.scfmt(-32, pstart[0])
    stop = spice.scfmt(-32, pstop[0])
    assert start == "00011:00:001"
    assert stop == "04011:21:784"
    spice.kclear()


def test_scpart():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.voyagerSclk)
    pstart, pstop = spice.scpart(-32)
    assert pstart is not None
    assert pstop is not None
    spice.kclear()


def test_scs2e():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.voyagerSclk)
    et = spice.scs2e(-32, "2/20538:39:768")
    npt.assert_almost_equal(et, -646668528.58222842)
    utc = spice.et2utc(et, "C", 3, 50)
    assert utc == "1979 JUL 05 21:50:21.234"
    spice.kclear()


def test_sct2e():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.voyagerSclk)
    et = spice.sct2e(-32, 985327965.0)
    utc = spice.et2utc(et, "C", 3, 50)
    assert utc == "1979 JUL 05 21:50:22.134"
    spice.kclear()


def test_sct2e_vectorized():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.voyagerSclk)
    inputlist = 3 * [985327965.0]
    # -32 is the SPICE code for Voyager 2
    to_test = spice.sct2e(-32, inputlist)
    expected = -646668527.6822292
    npt.assert_almost_equal(3 * [expected], to_test, decimal=6)
    spice.kclear()


def test_sctiks():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.voyagerSclk)
    ticks = spice.sctiks(-32, "20656:14:768")
    assert ticks == 991499967.00000000
    spice.kclear()


def test_sdiff():
    # SPICEINT_CELL
    a = spice.cell_int(8)
    b = spice.cell_int(8)
    spice.insrti(1, a)
    spice.insrti(2, a)
    spice.insrti(5, a)
    spice.insrti(3, b)
    spice.insrti(4, b)
    spice.insrti(5, b)
    c = spice.sdiff(a, b)
    assert [x for x in c] == [1, 2, 3, 4]
    # SPICECHAR_CELL
    a = spice.cell_char(8, 8)
    b = spice.cell_char(8, 8)
    spice.insrtc("1", a)
    spice.insrtc("2", a)
    spice.insrtc("5", a)
    spice.insrtc("3", b)
    spice.insrtc("4", b)
    spice.insrtc("5", b)
    c = spice.sdiff(a, b)
    assert [x for x in c] == ["1", "2", "3", "4"]
    # SPICEDOUBLE_CELL
    a = spice.cell_double(8)
    b = spice.cell_double(8)
    spice.insrtd(1.0, a)
    spice.insrtd(2.0, a)
    spice.insrtd(5.0, a)
    spice.insrtd(3.0, b)
    spice.insrtd(4.0, b)
    spice.insrtd(5.0, b)
    c = spice.sdiff(a, b)
    assert [x for x in c] == [1.0, 2.0, 3.0, 4.0]
    # SPICEBOOLEAN_CELL
    test_cell_one = spice.cell_bool(9)
    test_cell_two = spice.cell_bool(9)
    with pytest.raises(NotImplementedError):
        spice.sdiff(test_cell_one, test_cell_two)


def test_set_c():
    a = spice.cell_int(8)
    b = spice.cell_int(8)
    c = spice.cell_int(8)
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
    spice.kclear()
    # load kernels
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(CassiniKernels.cassSclk)
    spice.furnsh(CassiniKernels.cassFk)
    spice.furnsh(CassiniKernels.cassPck)
    spice.furnsh(CassiniKernels.cassIk)
    spice.furnsh(CassiniKernels.cassSclk)
    spice.furnsh(CassiniKernels.satSpk)
    spice.furnsh(CassiniKernels.cassTourSpk)
    spice.furnsh(CassiniKernels.cassCk)
    # start test
    et = spice.str2et("2013 FEB 25 11:50:00 UTC")
    camid = spice.bodn2c("CASSINI_ISS_NAC")
    shape, frame, bsight, n, bounds = spice.getfov(camid, 4)
    # run sincpt on boresight vector
    spoint, trgepc, obspos = spice.sincpt(
        "Ellipsoid", "Enceladus", et, "IAU_ENCELADUS", "CN+S", "CASSINI", frame, bsight
    )
    npt.assert_almost_equal(trgepc, 415065064.9055491)
    expected_spoint = [
        -143.56046004007180272311,
        202.90045955888857065474,
        -27.99454300594213052022,
    ]
    expected_obspos = [
        -329794.62202281970530748367,
        -557628.89673861570190638304,
        217721.3870436516881454736,
    ]
    npt.assert_array_almost_equal(spoint, expected_spoint, 5)
    npt.assert_array_almost_equal(obspos, expected_obspos, 5)
    spice.kclear()


def test_size():
    test_cell_one = spice.cell_int(8)
    assert spice.size(test_cell_one) == 8


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
    npt.assert_array_almost_equal(
        spice.sphrec(1.0, 180.0 * spice.rpd(), 0.0), expected3
    )


def test_spk14a():
    discrete_epochs = [100.0, 200.0, 300.0, 400.0]
    cheby_coeffs14 = [
        150.0,
        50.0,
        1.0101,
        1.0102,
        1.0103,
        1.0201,
        1.0202,
        1.0203,
        1.0301,
        1.0302,
        1.0303,
        1.0401,
        1.0402,
        1.0403,
        1.0501,
        1.0502,
        1.0503,
        1.0601,
        1.0602,
        1.0603,
        250.0,
        50.0,
        2.0101,
        2.0102,
        2.0103,
        2.0201,
        2.0202,
        2.0203,
        2.0301,
        2.0302,
        2.0303,
        2.0401,
        2.0402,
        2.0403,
        2.0501,
        2.0502,
        2.0503,
        2.0601,
        2.0602,
        2.0603,
        350.0,
        50.0,
        3.0101,
        3.0102,
        3.0103,
        3.0201,
        3.0202,
        3.0203,
        3.0301,
        3.0302,
        3.0303,
        3.0401,
        3.0402,
        3.0403,
        3.0501,
        3.0502,
        3.0503,
        3.0601,
        3.0602,
        3.0603,
        450.0,
        50.0,
        4.0101,
        4.0102,
        4.0103,
        4.0201,
        4.0202,
        4.0203,
        4.0301,
        4.0302,
        4.0303,
        4.0401,
        4.0402,
        4.0403,
        4.0501,
        4.0502,
        4.0503,
        4.0601,
        4.0602,
        4.0603,
    ]
    spk14 = os.path.join(cwd, "test14.bsp")
    if spice.exists(spk14):
        os.remove(spk14)  # pragma: no cover
    spice.kclear()
    handle = spice.spkopn(spk14, "Type 14 SPK internal file name.", 1024)
    init_size = os.path.getsize(spk14)
    spice.spk14b(handle, "SAMPLE_SPK_TYPE_14_SEGMENT", 399, 0, "J2000", 100.0, 400.0, 2)
    spice.spk14a(handle, 4, cheby_coeffs14, discrete_epochs)
    spice.spk14e(handle)
    spice.spkcls(handle)
    end_size = os.path.getsize(spk14)
    spice.kclear()
    assert end_size != init_size
    if spice.exists(spk14):
        os.remove(spk14)  # pragma: no cover


def test_spk14bstress():
    for i in range(30):
        test_spk14a()


def test_spk14b():
    # Same as test_spk14a
    discrete_epochs = [100.0, 200.0, 300.0, 400.0]
    cheby_coeffs14 = [
        150.0,
        50.0,
        1.0101,
        1.0102,
        1.0103,
        1.0201,
        1.0202,
        1.0203,
        1.0301,
        1.0302,
        1.0303,
        1.0401,
        1.0402,
        1.0403,
        1.0501,
        1.0502,
        1.0503,
        1.0601,
        1.0602,
        1.0603,
        250.0,
        50.0,
        2.0101,
        2.0102,
        2.0103,
        2.0201,
        2.0202,
        2.0203,
        2.0301,
        2.0302,
        2.0303,
        2.0401,
        2.0402,
        2.0403,
        2.0501,
        2.0502,
        2.0503,
        2.0601,
        2.0602,
        2.0603,
        350.0,
        50.0,
        3.0101,
        3.0102,
        3.0103,
        3.0201,
        3.0202,
        3.0203,
        3.0301,
        3.0302,
        3.0303,
        3.0401,
        3.0402,
        3.0403,
        3.0501,
        3.0502,
        3.0503,
        3.0601,
        3.0602,
        3.0603,
        450.0,
        50.0,
        4.0101,
        4.0102,
        4.0103,
        4.0201,
        4.0202,
        4.0203,
        4.0301,
        4.0302,
        4.0303,
        4.0401,
        4.0402,
        4.0403,
        4.0501,
        4.0502,
        4.0503,
        4.0601,
        4.0602,
        4.0603,
    ]
    spk14 = os.path.join(cwd, "test14.bsp")
    if spice.exists(spk14):
        os.remove(spk14)  # pragma: no cover
    spice.kclear()
    handle = spice.spkopn(spk14, "Type 14 SPK internal file name.", 1024)
    init_size = os.path.getsize(spk14)
    spice.spk14b(handle, "SAMPLE_SPK_TYPE_14_SEGMENT", 399, 0, "J2000", 100.0, 400.0, 2)
    spice.spk14a(handle, 4, cheby_coeffs14, discrete_epochs)
    spice.spk14e(handle)
    spice.spkcls(handle)
    end_size = os.path.getsize(spk14)
    spice.kclear()
    assert end_size != init_size
    if spice.exists(spk14):
        os.remove(spk14)  # pragma: no cover


def test_spk14e():
    # Same as test_spk14a
    discrete_epochs = [100.0, 200.0, 300.0, 400.0]
    cheby_coeffs14 = [
        150.0,
        50.0,
        1.0101,
        1.0102,
        1.0103,
        1.0201,
        1.0202,
        1.0203,
        1.0301,
        1.0302,
        1.0303,
        1.0401,
        1.0402,
        1.0403,
        1.0501,
        1.0502,
        1.0503,
        1.0601,
        1.0602,
        1.0603,
        250.0,
        50.0,
        2.0101,
        2.0102,
        2.0103,
        2.0201,
        2.0202,
        2.0203,
        2.0301,
        2.0302,
        2.0303,
        2.0401,
        2.0402,
        2.0403,
        2.0501,
        2.0502,
        2.0503,
        2.0601,
        2.0602,
        2.0603,
        350.0,
        50.0,
        3.0101,
        3.0102,
        3.0103,
        3.0201,
        3.0202,
        3.0203,
        3.0301,
        3.0302,
        3.0303,
        3.0401,
        3.0402,
        3.0403,
        3.0501,
        3.0502,
        3.0503,
        3.0601,
        3.0602,
        3.0603,
        450.0,
        50.0,
        4.0101,
        4.0102,
        4.0103,
        4.0201,
        4.0202,
        4.0203,
        4.0301,
        4.0302,
        4.0303,
        4.0401,
        4.0402,
        4.0403,
        4.0501,
        4.0502,
        4.0503,
        4.0601,
        4.0602,
        4.0603,
    ]
    spk14 = os.path.join(cwd, "test14.bsp")
    if spice.exists(spk14):
        os.remove(spk14)  # pragma: no cover
    spice.kclear()
    handle = spice.spkopn(spk14, "Type 14 SPK internal file name.", 1024)
    init_size = os.path.getsize(spk14)
    spice.spk14b(handle, "SAMPLE_SPK_TYPE_14_SEGMENT", 399, 0, "J2000", 100.0, 400.0, 2)
    spice.spk14a(handle, 4, cheby_coeffs14, discrete_epochs)
    spice.spk14e(handle)
    spice.spkcls(handle)
    end_size = os.path.getsize(spk14)
    spice.kclear()
    assert end_size != init_size
    if spice.exists(spk14):
        os.remove(spk14)  # pragma: no cover


def test_spkacs():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("2000 JAN 1 12:00:00 TDB")
    state, lt, dlt = spice.spkacs(301, et, "J2000", "lt+s", 399)
    expected_state = [
        -2.91584616594972088933e05,
        -2.66693402359092258848e05,
        -7.60956475582799030235e04,
        6.43439144942984264652e-01,
        -6.66065882529007446955e-01,
        -3.01310065348405708985e-01,
    ]
    expected_lt = 1.3423106103603615
    expected_dlt = 1.073169085424106e-07
    npt.assert_almost_equal(expected_lt, lt)
    npt.assert_almost_equal(expected_dlt, dlt)
    npt.assert_array_almost_equal(state, expected_state)
    spice.kclear()


def test_spkapo():
    spice.kclear()
    MARS = 499
    MOON = 301
    EPOCH = "Jan 1 2004 5:00 PM"
    REF = "J2000"
    ABCORR = "LT+S"
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et(EPOCH)
    state = spice.spkssb(MOON, et, REF)
    pos_vec, ltime = spice.spkapo(MARS, et, REF, state, ABCORR)
    expected_pos = [
        1.64534472413454592228e08,
        2.51219951337271928787e07,
        1.11454124484200235456e07,
    ]
    npt.assert_array_almost_equal(pos_vec, expected_pos, decimal=5)
    spice.kclear()


def test_spkapp():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("Jan 1 2004 5:00 PM")
    state = spice.spkssb(301, et, "J2000")
    state_vec, ltime = spice.spkapp(499, et, "J2000", state, "LT+S")
    expected_vec = [
        1.64534472413454592228e08,
        2.51219951337271928787e07,
        1.11454124484200235456e07,
        1.23119770045260814584e01,
        1.98884005139675998919e01,
        9.40678685353050170193e00,
    ]
    npt.assert_array_almost_equal(state_vec, expected_vec, decimal=6)
    spice.kclear()


def test_spkaps():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("2000 JAN 1 12:00:00 TDB")
    stobs = spice.spkssb(399, et, "J2000")
    state0 = np.array(spice.spkssb(399, et - 1, "J2000"))
    state2 = np.array(spice.spkssb(399, et + 1, "J2000"))
    # qderiv proc
    acc = spice.vlcomg(3, 0.5 / 1.0, state0 + 3, -0.5 / 1.0, state2 + 3)
    acc = [acc[0], acc[1], acc[2], 0.0, 0.0, 0.0]
    state, lt, dlt = spice.spkaps(301, et, "j2000", "lt+s", stobs, acc)
    spice.kclear()
    expected_lt = 1.3423106103603615
    expected_dlt = 1.073169085424106e-07
    expected_state = [
        -2.91584616594972088933e05,
        -2.66693402359092258848e05,
        -7.60956475582799030235e04,
        1.59912685775666059129e01,
        -1.64471169612870582455e01,
        -3.80333369259831766129e00,
    ]
    npt.assert_almost_equal(expected_lt, lt)
    npt.assert_almost_equal(expected_dlt, dlt)
    npt.assert_array_almost_equal(state, expected_state, decimal=5)


def test_spkcls():
    # Same as test_spkw02
    spk2 = os.path.join(cwd, "test2.bsp")
    if spice.exists(spk2):
        os.remove(spk2)  # pragma: no cover
    spice.kclear()
    handle = spice.spkopn(spk2, "Type 2 SPK internal file name.", 4)
    init_size = os.path.getsize(spk2)
    discrete_epochs = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0]
    cheby_coeffs02 = [
        1.0101,
        1.0102,
        1.0103,
        1.0201,
        1.0202,
        1.0203,
        1.0301,
        1.0302,
        1.0303,
        2.0101,
        2.0102,
        2.0103,
        2.0201,
        2.0202,
        2.0203,
        2.0301,
        2.0302,
        2.0303,
        3.0101,
        3.0102,
        3.0103,
        3.0201,
        3.0202,
        3.0203,
        3.0301,
        3.0302,
        3.0303,
        4.0101,
        4.0102,
        4.0103,
        4.0201,
        4.0202,
        4.0203,
        4.0301,
        4.0302,
        4.0303,
    ]
    segid = "SPK type 2 test segment"
    intlen = discrete_epochs[1] - discrete_epochs[0]
    spice.spkw02(
        handle,
        3,
        10,
        "J2000",
        discrete_epochs[0],
        discrete_epochs[4],
        segid,
        intlen,
        4,
        2,
        cheby_coeffs02,
        discrete_epochs[0],
    )
    spice.spkcls(handle)
    end_size = os.path.getsize(spk2)
    spice.kclear()
    assert end_size != init_size
    if spice.exists(spk2):
        os.remove(spk2)  # pragma: no cover


def test_spkcov():
    spice.kclear()

    ids = spice.spkobj(CoreKernels.spk)
    temp_obj = ids[0]

    # Checks for defaults
    cover = spice.spkcov(CoreKernels.spk, temp_obj)
    result = [x for x in cover]
    expected = [-94651137.81606464, 315662463.18395346]
    npt.assert_array_almost_equal(result, expected)

    # Checks for old way, where if cover is pre-set, it should remain set
    cover = spice.cell_double(2000)
    spice.scard(0, cover)
    spice.spkcov(CoreKernels.spk, temp_obj, cover)
    result = [x for x in cover]
    expected = [-94651137.81606464, 315662463.18395346]
    npt.assert_array_almost_equal(result, expected)

    spice.kclear()


def test_spkcpo():
    spice.kclear()
    spice.furnsh(ExtraKernels.earthStnSpk)
    spice.furnsh(ExtraKernels.earthHighPerPck)
    spice.furnsh(ExtraKernels.earthTopoTf)
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("2003 Oct 13 06:00:00")
    obspos = [-2353.6213656676991, -4641.3414911499403, 3677.0523293197439]
    state, lt = spice.spkcpo(
        "SUN", et, "DSS-14_TOPO", "OBSERVER", "CN+S", obspos, "EARTH", "ITRF93"
    )
    spice.kclear()
    expected_lt = 497.93167787805714
    expected_state = [
        6.25122733012810498476e07,
        5.89674929926417097449e07,
        -1.22059095879866167903e08,
        2.47597313358008614159e03,
        -9.87026711803482794494e03,
        -3.49990805659246507275e03,
    ]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state, decimal=6)


def test_spkcpt():
    spice.kclear()
    spice.furnsh(ExtraKernels.earthStnSpk)
    spice.furnsh(ExtraKernels.earthHighPerPck)
    spice.furnsh(ExtraKernels.earthTopoTf)
    spice.furnsh(CoreKernels.testMetaKernel)
    obstime = spice.str2et("2003 Oct 13 06:00:00")
    trgpos = [-2353.6213656676991, -4641.3414911499403, 3677.0523293197439]
    state, lt = spice.spkcpt(
        trgpos, "EARTH", "ITRF93", obstime, "ITRF93", "TARGET", "CN+S", "SUN"
    )
    spice.kclear()
    expected_lt = 497.9321928250503
    expected_state = [
        -3.41263006568005401641e06,
        -1.47916331564148992300e08,
        1.98124035009580813348e07,
        -1.07582448117249587085e04,
        2.50028331500427839273e02,
        1.11355285621842696742e01,
    ]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state, decimal=6)


def test_spkcvo():
    spice.kclear()
    spice.furnsh(ExtraKernels.earthStnSpk)
    spice.furnsh(ExtraKernels.earthHighPerPck)
    spice.furnsh(ExtraKernels.earthTopoTf)
    spice.furnsh(CoreKernels.testMetaKernel)
    obstime = spice.str2et("2003 Oct 13 06:00:00")
    obstate = [
        -2353.6213656676991,
        -4641.3414911499403,
        3677.0523293197439,
        -0.00000000000057086,
        0.00000000000020549,
        -0.00000000000012171,
    ]
    state, lt = spice.spkcvo(
        "SUN",
        obstime,
        "DSS-14_TOPO",
        "OBSERVER",
        "CN+S",
        obstate,
        0.0,
        "EARTH",
        "ITRF93",
    )
    spice.kclear()
    expected_lt = 497.93167787798325
    expected_state = [
        6.25122733012975975871e07,
        5.89674929925705492496e07,
        -1.22059095879864960909e08,
        2.47597313358015026097e03,
        -9.87026711803497346409e03,
        -3.49990805659256830040e03,
    ]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state, decimal=6)


def test_spkcvt():
    spice.kclear()
    spice.furnsh(ExtraKernels.earthStnSpk)
    spice.furnsh(ExtraKernels.earthHighPerPck)
    spice.furnsh(ExtraKernels.earthTopoTf)
    spice.furnsh(CoreKernels.testMetaKernel)
    obstime = spice.str2et("2003 Oct 13 06:00:00")
    trgstate = [
        -2353.6213656676991,
        -4641.3414911499403,
        3677.0523293197439,
        -0.00000000000057086,
        0.00000000000020549,
        -0.00000000000012171,
    ]
    state, lt = spice.spkcvt(
        trgstate, 0.0, "EARTH", "ITRF93", obstime, "ITRF93", "TARGET", "CN+S", "SUN"
    )
    spice.kclear()
    expected_lt = 497.932192824968
    expected_state = [
        -3.41263006574816117063e06,
        -1.47916331564124494791e08,
        1.98124035009435638785e07,
        -1.07582448117247804475e04,
        2.50028331500423831812e02,
        1.11355285621839659171e01,
    ]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state, decimal=6)


def test_spkez():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("July 4, 2003 11:00 AM PST")
    state, lt = spice.spkez(499, et, "J2000", "LT+S", 399)
    expected_lt = 269.6898813661505
    expected_state = [
        7.38222353105354905128e07,
        -2.71279189984722770751e07,
        -1.87413063014898747206e07,
        -6.80851334001380692484e00,
        7.51399612408221173609e00,
        3.00129849265935222391e00,
    ]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state)
    spice.kclear()


def test_spkezp():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("July 4, 2003 11:00 AM PST")
    pos, lt = spice.spkezp(499, et, "J2000", "LT+S", 399)
    expected_lt = 269.6898813661505
    expected_pos = [
        73822235.31053550541400909424,
        -27127918.99847228080034255981,
        -18741306.30148987472057342529,
    ]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(pos, expected_pos)
    spice.kclear()


def test_spkezr():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("July 4, 2003 11:00 AM PST")
    state, lt = spice.spkezr("Mars", et, "J2000", "LT+S", "Earth")
    expected_lt = 269.6898813661505
    expected_state = [
        7.38222353105354905128e07,
        -2.71279189984722770751e07,
        -1.87413063014898747206e07,
        -6.80851334001380692484e00,
        7.51399612408221173609e00,
        3.00129849265935222391e00,
    ]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state)
    spice.kclear()


def test_spkezr_vectorized():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = np.full((100,), spice.str2et("July 4, 2003 11:00 AM PST"))
    state, lt = spice.spkezr("Mars", et, "J2000", "LT+S", "Earth")
    expected_lt = np.full((100,), 269.6898816177049)
    expected_state = np.full(
        (100, 6),
        [
            73822235.33116072,
            -27127919.178592984,
            -18741306.284863796,
            -6.808513317178952,
            7.513996167680786,
            3.001298515816776,
        ],
    )
    npt.assert_allclose(lt, expected_lt)
    npt.assert_allclose(state, expected_state)
    spice.kclear()


def test_spkgeo():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("July 4, 2003 11:00 AM PST")
    state, lt = spice.spkgeo(499, et, "J2000", 399)
    expected_lt = 269.70264751151603
    expected_state = [
        7.38262164145559966564e07,
        -2.71280305524311661720e07,
        -1.87419738849752545357e07,
        -6.80950358877040429206e00,
        7.51381423681132254444e00,
        3.00129002640705921934e00,
    ]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state)
    spice.kclear()


def test_spkgps():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("July 4, 2003 11:00 AM PST")
    pos, lt = spice.spkgps(499, et, "J2000", 399)
    expected_lt = 269.70264751151603
    expected_pos = [
        73826216.41455599665641784668,
        -27128030.55243116617202758789,
        -18741973.88497525453567504883,
    ]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(pos, expected_pos)
    spice.kclear()


def test_spklef():
    spice.kclear()
    handle = spice.spklef(CoreKernels.spk)
    assert handle != -1
    spice.spkuef(handle)
    spice.kclear()


def test_spkltc():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("2000 JAN 1 12:00:00 TDB")
    stobs = spice.spkssb(399, et, "j2000")
    state, lt, dlt = spice.spkltc(301, et, "j2000", "lt", stobs)
    expectedOneWayLt = 1.342310610325
    expected_lt = 1.07316909e-07
    expected_state = [
        -2.91569268313527107239e05,
        -2.66709183005481958389e05,
        -7.60991494675353169441e04,
        6.43530600728670520994e-01,
        -6.66081825882520739412e-01,
        -3.01322833716675120286e-01,
    ]
    npt.assert_almost_equal(lt, expectedOneWayLt)
    npt.assert_almost_equal(dlt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state, decimal=5)
    spice.kclear()


def test_spkobj():
    # Same as test_spkcov
    spice.kclear()
    cover = spice.cell_double(2000)
    ids = spice.spkobj(CoreKernels.spk)
    temp_obj = ids[0]
    spice.scard(0, cover)
    spice.spkcov(CoreKernels.spk, temp_obj, cover)
    result = [x for x in cover]
    expected = [-94651137.81606464, 315662463.18395346]
    npt.assert_array_almost_equal(result, expected)
    spice.kclear()


def test_spkopa():
    SPKOPA = os.path.join(cwd, "testspkopa.bsp")
    if spice.exists(SPKOPA):
        os.remove(SPKOPA)  # pragma: no cover
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("2002 APR 27 00:00:00.000 TDB")
    # load subset from kernels
    handle, descr, ident = spice.spksfs(5, et, 41)
    body, center, frame, otype, first, last, begin, end = spice.spkuds(descr)
    # create empty spk kernel
    handle_test = spice.spkopn(SPKOPA, "Test Kernel for spkopa unit test.", 4)
    # created empty spk kernel, write to it
    spice.spksub(handle, descr, ident, first, last, handle_test)
    # close kernel
    spice.spkcls(handle_test)
    # open the file to append to it
    handle_spkopa = spice.spkopa(SPKOPA)
    et2 = spice.str2et("2003 APR 27 00:00:00.000 TDB")
    handle, descr, ident = spice.spksfs(5, et2, 41)
    body, center, frame, otype, first, last, begin, end = spice.spkuds(descr)
    spice.spksub(handle, descr, ident, first, last, handle_spkopa)
    spice.spkcls(handle_spkopa)
    # clean up
    if spice.exists(SPKOPA):
        os.remove(SPKOPA)  # pragma: no cover
    spice.kclear()


def test_spkopn():
    # Same as test_spkw02
    spk2 = os.path.join(cwd, "test2.bsp")
    if spice.exists(spk2):
        os.remove(spk2)  # pragma: no cover
    spice.kclear()
    handle = spice.spkopn(spk2, "Type 2 SPK internal file name.", 4)
    init_size = os.path.getsize(spk2)
    discrete_epochs = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0]
    cheby_coeffs02 = [
        1.0101,
        1.0102,
        1.0103,
        1.0201,
        1.0202,
        1.0203,
        1.0301,
        1.0302,
        1.0303,
        2.0101,
        2.0102,
        2.0103,
        2.0201,
        2.0202,
        2.0203,
        2.0301,
        2.0302,
        2.0303,
        3.0101,
        3.0102,
        3.0103,
        3.0201,
        3.0202,
        3.0203,
        3.0301,
        3.0302,
        3.0303,
        4.0101,
        4.0102,
        4.0103,
        4.0201,
        4.0202,
        4.0203,
        4.0301,
        4.0302,
        4.0303,
    ]
    segid = "SPK type 2 test segment"
    intlen = discrete_epochs[1] - discrete_epochs[0]
    spice.spkw02(
        handle,
        3,
        10,
        "J2000",
        discrete_epochs[0],
        discrete_epochs[4],
        segid,
        intlen,
        4,
        2,
        cheby_coeffs02,
        discrete_epochs[0],
    )
    spice.spkcls(handle)
    end_size = os.path.getsize(spk2)
    spice.kclear()
    assert end_size != init_size
    if spice.exists(spk2):
        os.remove(spk2)  # pragma: no cover


def test_spkpds():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("2002 APR 27 00:00:00.000 TDB")
    handle, descr, ident = spice.spksfs(5, et, 41)
    body, center, frame, otype, first, last, begin, end = spice.spkuds(descr)
    outframe = spice.frmnam(frame)
    spkpds_output = spice.spkpds(body, center, outframe, otype, first, last)
    npt.assert_almost_equal(spkpds_output, descr)
    spice.kclear()


def test_spkpos():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("July 4, 2003 11:00 AM PST")
    pos, lt = spice.spkpos("Mars", et, "J2000", "LT+S", "Earth")
    expected_lt = 269.6898813661505
    expected_pos = [
        73822235.31053550541400909424,
        -27127918.99847228080034255981,
        -18741306.30148987472057342529,
    ]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(pos, expected_pos)
    spice.kclear()


def test_spkpos_vectorized():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et(["July 4, 2003 11:00 AM PST", "July 11, 2003 11:00 AM PST"])
    pos, lt = spice.spkpos("Mars", et, "J2000", "LT+S", "Earth")
    expected_lt = [269.68988136615047324085, 251.44204326148698669385]
    expected_pos = [
        [
            73822235.31053550541400909424,
            -27127918.99847228080034255981,
            -18741306.30148987472057342529,
        ],
        [
            69682765.52989411354064941406,
            -23090281.18098583817481994629,
            -17127756.93968883529305458069,
        ],
    ]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(pos, expected_pos)
    spice.kclear()


def test_spkpvn():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("2002 APR 27 00:00:00.000 TDB")
    handle, descr, ident = spice.spksfs(5, et, 41)
    refid, state, center = spice.spkpvn(handle, descr, et)
    expected_state = [
        -2.70063336478468656540e08,
        6.69404818553274393082e08,
        2.93505043081457614899e08,
        -1.24191493217698472051e01,
        -3.70147572019018955558e00,
        -1.28422514561611489370e00,
    ]
    npt.assert_array_almost_equal(state, expected_state)
    spice.kclear()


def test_spksfs():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    idcode = spice.bodn2c("PLUTO BARYCENTER")
    et = spice.str2et("2001 FEB 18 UTC")
    handle, descr, ident = spice.spksfs(idcode, et, 41)
    assert ident == "DE-405"
    spice.kclear()


def test_spkssb():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    targ1 = 499
    epoch = "July 4, 2003 11:00 AM PST"
    frame = "J2000"
    targ2 = 399
    et = spice.str2et(epoch)
    state1 = spice.spkssb(targ1, et, frame)
    state2 = spice.spkssb(targ2, et, frame)
    dist = spice.vdist(state1[0:3], state2[0:3])
    npt.assert_approx_equal(dist, 80854820.0, significant=7)
    spice.kclear()


def test_spksub():
    SPKSUB = os.path.join(cwd, "testspksub.bsp")
    if spice.exists(SPKSUB):
        os.remove(SPKSUB)  # pragma: no cover
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("2002 APR 27 00:00:00.000 TDB")
    # load subset from kernels
    handle, descr, ident = spice.spksfs(5, et, 41)
    body, center, frame, otype, first, last, begin, end = spice.spkuds(descr)
    # create empty spk kernel
    handle_test = spice.spkopn(SPKSUB, "Test Kernel for spksub unit test.", 4)
    # created empty spk kernel, write to it
    spice.spksub(handle, descr, ident, first, last, handle_test)
    # close kernel
    spice.spkcls(handle_test)
    if spice.exists(SPKSUB):
        os.remove(SPKSUB)  # pragma: no cover
    spice.kclear()


def test_spkuds():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("2002 APR 27 00:00:00.000 TDB")
    handle, descr, ident = spice.spksfs(5, et, 41)
    body, center, frame, otype, first, last, begin, end = spice.spkuds(descr)
    assert body == 5
    assert begin == 54073
    assert end == 57950
    assert otype == 2
    spice.kclear()


def test_spkuef():
    spice.kclear()
    handle = spice.spklef(CoreKernels.spk)
    assert handle != -1
    spice.spkuef(handle)
    spice.kclear()


def test_spkw02():
    spk2 = os.path.join(cwd, "test2.bsp")
    if spice.exists(spk2):
        os.remove(spk2)  # pragma: no cover
    spice.kclear()
    handle = spice.spkopn(spk2, "Type 2 SPK internal file name.", 4)
    init_size = os.path.getsize(spk2)
    discrete_epochs = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0]
    cheby_coeffs02 = [
        1.0101,
        1.0102,
        1.0103,
        1.0201,
        1.0202,
        1.0203,
        1.0301,
        1.0302,
        1.0303,
        2.0101,
        2.0102,
        2.0103,
        2.0201,
        2.0202,
        2.0203,
        2.0301,
        2.0302,
        2.0303,
        3.0101,
        3.0102,
        3.0103,
        3.0201,
        3.0202,
        3.0203,
        3.0301,
        3.0302,
        3.0303,
        4.0101,
        4.0102,
        4.0103,
        4.0201,
        4.0202,
        4.0203,
        4.0301,
        4.0302,
        4.0303,
    ]
    segid = "SPK type 2 test segment"
    intlen = discrete_epochs[1] - discrete_epochs[0]
    spice.spkw02(
        handle,
        3,
        10,
        "J2000",
        discrete_epochs[0],
        discrete_epochs[4],
        segid,
        intlen,
        4,
        2,
        cheby_coeffs02,
        discrete_epochs[0],
    )
    spice.spkcls(handle)
    end_size = os.path.getsize(spk2)
    spice.kclear()
    assert end_size != init_size
    if spice.exists(spk2):
        os.remove(spk2)  # pragma: no cover


def test_spkw03():
    spk3 = os.path.join(cwd, "test3.bsp")
    if spice.exists(spk3):
        os.remove(spk3)  # pragma: no cover
    spice.kclear()
    handle = spice.spkopn(spk3, "Type 3 SPK internal file name.", 4)
    init_size = os.path.getsize(spk3)
    discrete_epochs = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0]
    cheby_coeffs03 = [
        1.0101,
        1.0102,
        1.0103,
        1.0201,
        1.0202,
        1.0203,
        1.0301,
        1.0302,
        1.0303,
        1.0401,
        1.0402,
        1.0403,
        1.0501,
        1.0502,
        1.0503,
        1.0601,
        1.0602,
        1.0603,
        2.0101,
        2.0102,
        2.0103,
        2.0201,
        2.0202,
        2.0203,
        2.0301,
        2.0302,
        2.0303,
        2.0401,
        2.0402,
        2.0403,
        2.0501,
        2.0502,
        2.0503,
        2.0601,
        2.0602,
        2.0603,
        3.0101,
        3.0102,
        3.0103,
        3.0201,
        3.0202,
        3.0203,
        3.0301,
        3.0302,
        3.0303,
        3.0401,
        3.0402,
        3.0403,
        3.0501,
        3.0502,
        3.0503,
        3.0601,
        3.0602,
        3.0603,
        4.0101,
        4.0102,
        4.0103,
        4.0201,
        4.0202,
        4.0203,
        4.0301,
        4.0302,
        4.0303,
        4.0401,
        4.0402,
        4.0403,
        4.0501,
        4.0502,
        4.0503,
        4.0601,
        4.0602,
        4.0603,
    ]
    segid = "SPK type 3 test segment"
    intlen = discrete_epochs[1] - discrete_epochs[0]
    spice.spkw03(
        handle,
        3,
        10,
        "J2000",
        discrete_epochs[0],
        discrete_epochs[4],
        segid,
        intlen,
        4,
        2,
        cheby_coeffs03,
        discrete_epochs[0],
    )
    spice.spkcls(handle)
    end_size = os.path.getsize(spk3)
    spice.kclear()
    assert end_size != init_size
    if spice.exists(spk3):
        os.remove(spk3)  # pragma: no cover


def test_spkw05():
    spk5 = os.path.join(cwd, "test5.bsp")
    if spice.exists(spk5):
        os.remove(spk5)  # pragma: no cover
    spice.kclear()
    handle = spice.spkopn(spk5, "Type 5 SPK internal file name.", 4)
    init_size = os.path.getsize(spk5)
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
        [109.0, 209.0, 309.0, 409.0, 509.0, 609.0],
    ]
    segid = "SPK type 5 test segment"
    spice.spkw05(
        handle,
        3,
        10,
        "J2000",
        discrete_epochs[0],
        discrete_epochs[-1],
        segid,
        132712440023.310,
        9,
        discrete_states,
        discrete_epochs,
    )
    spice.spkcls(handle)
    end_size = os.path.getsize(spk5)
    spice.kclear()
    assert end_size != init_size
    if spice.exists(spk5):
        os.remove(spk5)  # pragma: no cover


def test_spkw08():
    spk8 = os.path.join(cwd, "test8.bsp")
    if spice.exists(spk8):
        os.remove(spk8)  # pragma: no cover
    spice.kclear()
    handle = spice.spkopn(spk8, "Type 8 SPK internal file name.", 4)
    init_size = os.path.getsize(spk8)
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
        [109.0, 209.0, 309.0, 409.0, 509.0, 609.0],
    ]
    segid = "SPK type 8 test segment"
    step = discrete_epochs[1] - discrete_epochs[0]
    spice.spkw08(
        handle,
        3,
        10,
        "J2000",
        discrete_epochs[0],
        discrete_epochs[-1],
        segid,
        3,
        9,
        discrete_states,
        discrete_epochs[0],
        step,
    )
    spice.spkcls(handle)
    end_size = os.path.getsize(spk8)
    spice.kclear()
    assert end_size != init_size
    if spice.exists(spk8):
        os.remove(spk8)  # pragma: no cover


def test_spkw09():
    spk9 = os.path.join(cwd, "test9.bsp")
    if spice.exists(spk9):
        os.remove(spk9)  # pragma: no cover
    spice.kclear()
    handle = spice.spkopn(spk9, "Type 9 SPK internal file name.", 4)
    init_size = os.path.getsize(spk9)
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
        [109.0, 209.0, 309.0, 409.0, 509.0, 609.0],
    ]
    segid = "SPK type 9 test segment"
    spice.spkw09(
        handle,
        3,
        10,
        "J2000",
        discrete_epochs[0],
        discrete_epochs[-1],
        segid,
        3,
        9,
        discrete_states,
        discrete_epochs,
    )
    spice.spkcls(handle)
    end_size = os.path.getsize(spk9)
    spice.kclear()
    assert end_size != init_size
    if spice.exists(spk9):
        os.remove(spk9)  # pragma: no cover


def test_spkw10():
    spk10 = os.path.join(cwd, "test10.bsp")
    spice.kclear()
    tle = [
        "1 18123U 87 53  A 87324.61041692 -.00000023  00000-0 -75103-5 0 00675",
        "2 18123  98.8296 152.0074 0014950 168.7820 191.3688 14.12912554 21686",
        "1 18123U 87 53  A 87326.73487726  .00000045  00000-0  28709-4 0 00684",
        "2 18123  98.8335 154.1103 0015643 163.5445 196.6235 14.12912902 21988",
        "1 18123U 87 53  A 87331.40868801  .00000104  00000-0  60183-4 0 00690",
        "2 18123  98.8311 158.7160 0015481 149.9848 210.2220 14.12914624 22644",
        "1 18123U 87 53  A 87334.24129978  .00000086  00000-0  51111-4 0 00702",
        "2 18123  98.8296 161.5054 0015372 142.4159 217.8089 14.12914879 23045",
        "1 18123U 87 53  A 87336.93227900 -.00000107  00000-0 -52860-4 0 00713",
        "2 18123  98.8317 164.1627 0014570 135.9191 224.2321 14.12910572 23425",
        "1 18123U 87 53  A 87337.28635487  .00000173  00000-0  10226-3 0 00726",
        "2 18123  98.8284 164.5113 0015289 133.5979 226.6438 14.12916140 23475",
        "1 18123U 87 53  A 87339.05673569  .00000079  00000-0  47069-4 0 00738",
        "2 18123  98.8288 166.2585 0015281 127.9985 232.2567 14.12916010 24908",
        "1 18123U 87 53  A 87345.43010859  .00000022  00000-0  16481-4 0 00758",
        "2 18123  98.8241 172.5226 0015362 109.1515 251.1323 14.12915487 24626",
        "1 18123U 87 53  A 87349.04167543  .00000042  00000-0  27370-4 0 00764",
        "2 18123  98.8301 176.1010 0015565 100.0881 260.2047 14.12916361 25138",
    ]
    epoch_x = []
    elems_x = []
    spice.furnsh(CoreKernels.testMetaKernel)
    for i in range(0, 18, 2):
        lines = [tle[i], tle[i + 1]]
        epoch, elems = spice.getelm(1950, 75, lines)
        epoch_x.append(epoch)
        elems_x.extend(elems)
    first = epoch_x[0] - 0.5 * spice.spd()
    last = epoch_x[-1] + 0.5 * spice.spd()
    consts = [
        1.082616e-3,
        -2.538813e-6,
        -1.65597e-6,
        7.43669161e-2,
        120.0,
        78.0,
        6378.135,
        1.0,
    ]
    if spice.exists(spk10):
        os.remove(spk10)  # pragma: no cover
    handle = spice.spkopn(spk10, "Type 10 SPK internal file name.", 100)
    init_size = os.path.getsize(spk10)
    spice.spkw10(
        handle,
        -118123,
        399,
        "J2000",
        first,
        last,
        "DMSP F8",
        consts,
        9,
        elems_x,
        epoch_x,
    )
    spice.spkcls(handle)
    end_size = os.path.getsize(spk10)
    assert end_size != init_size
    spice.kclear()
    if spice.exists(spk10):
        os.remove(spk10)  # pragma: no cover


def test_spkw12():
    spk12 = os.path.join(cwd, "test12.bsp")
    if spice.exists(spk12):
        os.remove(spk12)  # pragma: no cover
    spice.kclear()
    handle = spice.spkopn(spk12, "Type 12 SPK internal file name.", 4)
    init_size = os.path.getsize(spk12)
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
        [109.0, 209.0, 309.0, 409.0, 509.0, 609.0],
    ]
    segid = "SPK type 12 test segment"
    step = discrete_epochs[1] - discrete_epochs[0]
    spice.spkw12(
        handle,
        3,
        10,
        "J2000",
        discrete_epochs[0],
        discrete_epochs[-1],
        segid,
        3,
        9,
        discrete_states,
        discrete_epochs[0],
        step,
    )
    spice.spkcls(handle)
    end_size = os.path.getsize(spk12)
    spice.kclear()
    assert end_size != init_size
    if spice.exists(spk12):
        os.remove(spk12)  # pragma: no cover


def test_spkw13():
    spk13 = os.path.join(cwd, "test13.bsp")
    if spice.exists(spk13):
        os.remove(spk13)  # pragma: no cover
    spice.kclear()
    handle = spice.spkopn(spk13, "Type 13 SPK internal file name.", 4)
    init_size = os.path.getsize(spk13)
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
        [109.0, 209.0, 309.0, 409.0, 509.0, 609.0],
    ]
    segid = "SPK type 13 test segment"
    spice.spkw13(
        handle,
        3,
        10,
        "J2000",
        discrete_epochs[0],
        discrete_epochs[-1],
        segid,
        3,
        9,
        discrete_states,
        discrete_epochs,
    )
    spice.spkcls(handle)
    end_size = os.path.getsize(spk13)
    spice.kclear()
    assert end_size != init_size
    if spice.exists(spk13):
        os.remove(spk13)  # pragma: no cover


def test_spkw15():
    discrete_epochs = [100.0, 900.0]
    spice.kclear()
    #
    spk15 = os.path.join(cwd, "test15.bsp")
    if spice.exists(spk15):
        os.remove(spk15)  # pragma: no cover
    # create the test kernel
    handle = spice.spkopn(spk15, "Type 13 SPK internal file name.", 4)
    init_size = os.path.getsize(spk15)
    # load kernels
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("Dec 25, 2007")
    state, ltime = spice.spkezr("Moon", et, "J2000", "NONE", "EARTH")
    dim, mu = spice.bodvrd("EARTH", "GM", 1)
    elts = spice.oscelt(state, et, mu[0])
    # From these collect the eccentricity and semi-latus
    ecc = elts[1]
    p = elts[0] * (1.0 + ecc)
    # Next get the trajectory pole vector and the periapsis vector.
    state = state[0:3]
    tp = spice.ucrss(state, state + 4)
    pa = spice.vhat(state)
    # Enable both J2 corrections.
    j2flg = 0.0
    # other constants, as I don't need real values
    pv = [1.0, 2.0, 3.0]
    gm = 398600.436
    j2 = 1.0
    radius = 6000.0
    # now call spkw15
    spice.spkw15(
        handle,
        3,
        10,
        "J2000",
        discrete_epochs[0],
        discrete_epochs[-1],
        "Test SPKW15",
        et,
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
    # close the kernel
    spice.spkcls(handle)
    end_size = os.path.getsize(spk15)
    # cleanup
    assert end_size != init_size
    if spice.exists(spk15):
        os.remove(spk15)  # pragma: no cover
    #
    spice.kclear()


def test_spkw17():
    discrete_epochs = [100.0, 900.0]
    spice.kclear()
    #
    spk17 = os.path.join(cwd, "test17.bsp")
    if spice.exists(spk17):
        os.remove(spk17)  # pragma: no cover
    # create the test kernel
    handle = spice.spkopn(spk17, "Type 17 SPK internal file name.", 4)
    init_size = os.path.getsize(spk17)
    # load kernels
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("Dec 25, 2007")
    # make the eqel vector and the rapol and decpol floats
    p = 10000.0
    gm = 398600.436
    ecc = 0.1
    a = p / (1.0 - ecc)
    n = np.sqrt(gm / a) / a
    argp = 30.0 * spice.rpd()
    node = 15.0 * spice.rpd()
    inc = 10.0 * spice.rpd()
    m0 = 45.0 * spice.rpd()
    eqel = [
        a,
        ecc * np.sin(argp + node),
        ecc * np.cos(argp + node),
        m0 + argp + node,
        np.tan(inc / 2.0) * np.sin(node),
        np.tan(inc / 2.0) * np.cos(node),
        0.0,
        n,
        0.0,
    ]
    rapol = spice.halfpi() * -1
    decpol = spice.halfpi()
    # now call spkw17
    spice.spkw17(
        handle,
        3,
        10,
        "J2000",
        discrete_epochs[0],
        discrete_epochs[-1],
        "Test SPKW17",
        et,
        eqel,
        rapol,
        decpol,
    )
    # close the kernel
    spice.spkcls(handle)
    end_size = os.path.getsize(spk17)
    # cleanup
    assert end_size != init_size
    if spice.exists(spk17):
        os.remove(spk17)  # pragma: no cover
    #
    spice.kclear()


def test_spkw18():
    spice.kclear()
    #
    spk18 = os.path.join(cwd, "test18.bsp")
    if spice.exists(spk18):
        os.remove(spk18)  # pragma: no cover
    # make a new kernel
    handle = spice.spkopn(spk18, "Type 18 SPK internal file name.", 4)
    init_size = os.path.getsize(spk18)
    # test data
    body = 3
    center = 10
    ref = "J2000"
    epochs = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0]
    states = [
        [101.0, 201.0, 301.0, 401.0, 501.0, 601.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        [102.0, 202.0, 302.0, 402.0, 502.0, 602.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        [103.0, 203.0, 303.0, 403.0, 503.0, 603.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        [104.0, 204.0, 304.0, 404.0, 504.0, 604.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        [105.0, 205.0, 305.0, 405.0, 505.0, 605.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        [106.0, 206.0, 306.0, 406.0, 506.0, 606.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        [107.0, 207.0, 307.0, 407.0, 507.0, 607.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        [108.0, 208.0, 308.0, 408.0, 508.0, 608.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        [109.0, 209.0, 309.0, 409.0, 509.0, 609.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    ]
    # test spkw18 with S18TP0
    spice.spkw18(
        handle,
        spice.stypes.SpiceSPK18Subtype.S18TP0,
        body,
        center,
        ref,
        epochs[0],
        epochs[-1],
        "SPK type 18 test segment",
        3,
        states,
        epochs,
    )
    # close the kernel
    spice.spkcls(handle)
    end_size = os.path.getsize(spk18)
    assert end_size != init_size
    # test reading data
    handle = spice.spklef(spk18)
    state, lt = spice.spkgeo(body, epochs[0], ref, center)
    npt.assert_array_equal(state, [101.0, 201.0, 301.0, 1.0, 1.0, 1.0])
    state, lt = spice.spkgeo(body, epochs[1], ref, center)
    npt.assert_array_equal(state, [102.0, 202.0, 302.0, 1.0, 1.0, 1.0])
    spice.spkcls(handle)
    spice.kclear()
    # cleanup
    if spice.exists(spk18):
        os.remove(spk18)  # pragma: no cover


def test_spkw20():
    spice.kclear()
    #
    spk20 = os.path.join(cwd, "test20.bsp")
    if spice.exists(spk20):
        os.remove(spk20)  # pragma: no cover
    # create the test kernel
    handle = spice.spkopn(spk20, "Type 20 SPK internal file name.", 4)
    init_size = os.path.getsize(spk20)
    # now call spkw20, giving fake data from f_spk20.c from tspice
    intlen = 5.0
    n = 100
    polydg = 1
    cdata = np.arange(1.0, 198000.0)  #
    dscale = 1.0
    tscale = 1.0
    initjd = 2451545.0
    initfr = 0.25
    first = (initjd - spice.j2000() + initfr) * spice.spd()
    last = ((initjd - spice.j2000()) + initfr + n * intlen) * spice.spd()
    spice.spkw20(
        handle,
        301,
        3,
        "J2000",
        first,
        last,
        "Test SPKW20",
        intlen,
        n,
        polydg,
        cdata,
        dscale,
        tscale,
        initjd,
        initfr,
    )
    # close the kernel
    spice.spkcls(handle)
    end_size = os.path.getsize(spk20)
    # cleanup
    assert end_size != init_size
    if spice.exists(spk20):
        os.remove(spk20)  # pragma: no cover
    #
    spice.kclear()


def test_srfc2s():
    spice.kclear()
    kernel = os.path.join(cwd, "srfc2s_ex1.tm")
    if spice.exists(kernel):
        os.remove(kernel)  # pragma: no cover
    with open(kernel, "w") as kernelFile:
        kernelFile.write("\\begindata\n")
        kernelFile.write("NAIF_SURFACE_NAME += ( 'MGS MOLA  64 pixel/deg',\n")
        kernelFile.write("                       'MGS MOLA 128 pixel/deg',\n")
        kernelFile.write("                       'PHOBOS GASKELL Q512'     )\n")
        kernelFile.write("NAIF_SURFACE_CODE += (   1,   2,    1 )\n")
        kernelFile.write("NAIF_SURFACE_BODY += ( 499, 499,  401 )\n")
        kernelFile.write("\\begintext\n")
        kernelFile.close()
    spice.furnsh(kernel)
    assert spice.srfc2s(1, 499) == "MGS MOLA  64 pixel/deg"
    assert spice.srfc2s(1, 401) == "PHOBOS GASKELL Q512"
    assert spice.srfc2s(2, 499) == "MGS MOLA 128 pixel/deg"
    with pytest.raises(spice.stypes.SpiceyError):
        spice.srfc2s(1, -1)
    spice.reset()
    spice.kclear()
    if spice.exists(kernel):
        os.remove(kernel)  # pragma: no cover


def test_srfcss():
    spice.kclear()
    kernel = os.path.join(cwd, "srfcss_ex1.tm")
    if spice.exists(kernel):
        os.remove(kernel)  # pragma: no cover
    with open(kernel, "w") as kernelFile:
        kernelFile.write("\\begindata\n")
        kernelFile.write("NAIF_SURFACE_NAME += ( 'MGS MOLA  64 pixel/deg',\n")
        kernelFile.write("                       'MGS MOLA 128 pixel/deg',\n")
        kernelFile.write("                       'PHOBOS GASKELL Q512'     )\n")
        kernelFile.write("NAIF_SURFACE_CODE += (   1,   2,    1 )\n")
        kernelFile.write("NAIF_SURFACE_BODY += ( 499, 499,  401 )\n")
        kernelFile.write("\\begintext\n")
        kernelFile.close()
    spice.furnsh(kernel)
    assert spice.srfcss(1, "MARS") == "MGS MOLA  64 pixel/deg"
    assert spice.srfcss(1, "PHOBOS") == "PHOBOS GASKELL Q512"
    assert spice.srfcss(2, "499") == "MGS MOLA 128 pixel/deg"
    with pytest.raises(spice.stypes.SpiceyError):
        spice.srfcss(1, "ZZZ")
    spice.reset()
    spice.kclear()
    if spice.exists(kernel):
        os.remove(kernel)  # pragma: no cover


def test_srfnrm():
    spice.kclear()
    spice.furnsh(CoreKernels.pck)
    spice.furnsh(ExtraKernels.phobosDsk)
    srfpts = spice.latsrf(
        "DSK/UNPRIORITIZED", "phobos", 0.0, "iau_phobos", [[0.0, 45.0], [60.0, 45.0]]
    )
    normals = spice.srfnrm("DSK/UNPRIORITIZED", "phobos", 0.0, "iau_phobos", srfpts)
    srf_rad = np.array([spice.recrad(x) for x in srfpts])
    nrm_rad = np.array([spice.recrad(x) for x in normals])
    assert np.any(np.not_equal(srf_rad, nrm_rad))
    spice.kclear()


def test_srfrec():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    x = spice.srfrec(399, 100.0 * spice.rpd(), 35.0 * spice.rpd())
    expected = [-906.24919474, 5139.59458217, 3654.29989637]
    npt.assert_array_almost_equal(x, expected)
    spice.kclear()


def test_srfs2c():
    spice.kclear()
    kernel = os.path.join(cwd, "srfs2c_ex1.tm")
    if spice.exists(kernel):
        os.remove(kernel)  # pragma: no cover
    with open(kernel, "w") as kernelFile:
        kernelFile.write("\\begindata\n")
        kernelFile.write("NAIF_SURFACE_NAME += ( 'MGS MOLA  64 pixel/deg',\n")
        kernelFile.write("                       'MGS MOLA 128 pixel/deg',\n")
        kernelFile.write("                       'PHOBOS GASKELL Q512'     )\n")
        kernelFile.write("NAIF_SURFACE_CODE += (   1,   2,    1 )\n")
        kernelFile.write("NAIF_SURFACE_BODY += ( 499, 499,  401 )\n")
        kernelFile.write("\\begintext\n")
        kernelFile.close()
    spice.furnsh(kernel)
    assert spice.srfs2c("MGS MOLA  64 pixel/deg", "MARS") == 1
    assert spice.srfs2c("PHOBOS GASKELL Q512", "PHOBOS") == 1
    assert spice.srfs2c("MGS MOLA 128 pixel/deg", "MARS") == 2
    assert spice.srfs2c("MGS MOLA  64 pixel/deg", "499") == 1
    assert spice.srfs2c("1", "PHOBOS") == 1
    assert spice.srfs2c("2", "499") == 2
    with pytest.raises(spice.stypes.SpiceyError):
        spice.srfs2c("ZZZ", "MARS")
    spice.reset()
    spice.kclear()
    if spice.exists(kernel):
        os.remove(kernel)  # pragma: no cover


def test_srfscc():
    spice.kclear()
    kernel = os.path.join(cwd, "srfscc_ex1.tm")
    if spice.exists(kernel):
        os.remove(kernel)  # pragma: no cover
    with open(kernel, "w") as kernelFile:
        kernelFile.write("\\begindata\n")
        kernelFile.write("NAIF_SURFACE_NAME += ( 'MGS MOLA  64 pixel/deg',\n")
        kernelFile.write("                       'MGS MOLA 128 pixel/deg',\n")
        kernelFile.write("                       'PHOBOS GASKELL Q512'     )\n")
        kernelFile.write("NAIF_SURFACE_CODE += (   1,   2,    1 )\n")
        kernelFile.write("NAIF_SURFACE_BODY += ( 499, 499,  401 )\n")
        kernelFile.write("\\begintext\n")
        kernelFile.close()
    spice.furnsh(kernel)
    assert spice.srfscc("MGS MOLA  64 pixel/deg", 499) == 1
    assert spice.srfscc("PHOBOS GASKELL Q512", 401) == 1
    assert spice.srfscc("MGS MOLA 128 pixel/deg", 499) == 2
    assert spice.srfscc("1", 401) == 1
    assert spice.srfscc("2", 499) == 2
    with pytest.raises(spice.stypes.SpiceyError):
        spice.srfscc("ZZZ", 499)
    spice.reset()
    spice.kclear()
    if spice.exists(kernel):
        os.remove(kernel)  # pragma: no cover


def test_srfxpt():
    spice.kclear()
    # load kernels
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(CassiniKernels.cassSclk)
    spice.furnsh(CassiniKernels.cassFk)
    spice.furnsh(CassiniKernels.cassPck)
    spice.furnsh(CassiniKernels.cassIk)
    spice.furnsh(CassiniKernels.cassSclk)
    spice.furnsh(CassiniKernels.satSpk)
    spice.furnsh(CassiniKernels.cassTourSpk)
    spice.furnsh(CassiniKernels.cassCk)
    # start test
    et = spice.str2et("2013 FEB 25 11:50:00 UTC")
    camid = spice.bodn2c("CASSINI_ISS_NAC")
    shape, frame, bsight, n, bounds = spice.getfov(camid, 4)
    # run srfxpt on boresight vector
    spoint, dist, trgepc, obspos = spice.srfxpt(
        "Ellipsoid", "Enceladus", et, "LT+S", "CASSINI", frame, bsight
    )
    npt.assert_almost_equal(dist, 683459.6415073496)
    npt.assert_almost_equal(trgepc, 415065064.9055491)
    expected_spoint = [
        -143.56046006834264971985,
        202.9004595420923067195,
        -27.99454299292458969717,
    ]
    expected_obspos = [
        329627.25001832831185311079,
        557847.97086489037610590458,
        -217744.02422016291529871523,
    ]
    npt.assert_array_almost_equal(spoint, expected_spoint)
    npt.assert_array_almost_equal(obspos, expected_obspos)
    # Iterable ET argument:  et-10, et, et+10
    ets = [et - 10.0, et, et + 10.0]
    spoints, dists, trgepcs, obsposs = spice.srfxpt(
        "Ellipsoid", "Enceladus", ets, "LT+S", "CASSINI", frame, bsight
    )
    assert 0.0 == spice.vnorm(spice.vsub(spoints[1], spoint))
    assert 0.0 == (dists[1] - dist)
    assert 0.0 == (trgepcs[1] - trgepc)
    assert 0.0 == spice.vnorm(spice.vsub(obsposs[1], obspos))
    # Cleanup
    spice.kclear()


def test_ssize():
    cell = spice.cell_double(10)
    assert cell.size == 10
    spice.ssize(5, cell)
    assert cell.size == 5


def test_stelab():
    IDOBS = 399
    IDTARG = 301
    UTC = "July 4 2004"
    FRAME = "J2000"
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et(UTC)
    sobs = spice.spkssb(IDOBS, et, FRAME)
    starg, ltime = spice.spkapp(IDTARG, et, FRAME, sobs, "LT")
    expected_starg = [
        2.01738718005936592817e05,
        -2.60893145259797573090e05,
        -1.47722589585214853287e05,
        9.24727104822839152121e-01,
        5.32379608845730878386e-01,
        2.17669748758417824774e-01,
    ]
    npt.assert_array_almost_equal(starg, expected_starg)
    cortarg = spice.stelab(starg[0:3], starg[3:6])
    expected_cortarg = [
        201739.80378842627396807075,
        -260892.46619604207808151841,
        -147722.30606629714020527899,
    ]
    npt.assert_array_almost_equal(expected_cortarg, cortarg)
    spice.kclear()


def test_stpool():
    spice.kclear()
    kernel = os.path.join(cwd, "stpool_t.ker")
    if spice.exists(kernel):
        os.remove(kernel)  # pragma: no cover
    with open(kernel, "w") as kernelFile:
        kernelFile.write("\\begindata\n")
        kernelFile.write("SPK_FILES = ( 'this_is_the_full_path_specification_*',\n")
        kernelFile.write("              'of_a_file_with_a_long_name',\n")
        kernelFile.write("              'this_is_the_full_path_specification_*',\n")
        kernelFile.write("              'of_a_second_file_name' )\n")
        kernelFile.close()
    spice.furnsh(kernel)
    string, n = spice.stpool("SPK_FILES", 0, "*")
    assert n == 62
    assert string == "this_is_the_full_path_specification_of_a_file_with_a_long_name"
    string, n = spice.stpool("SPK_FILES", 1, "*")
    assert n == 57
    assert string == "this_is_the_full_path_specification_of_a_second_file_name"
    spice.kclear()
    if spice.exists(kernel):
        os.remove(kernel)  # pragma: no cover


def test_str2et():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    date = "Thu Mar 20 12:53:29 PST 1997"
    et = spice.str2et(date)
    npt.assert_almost_equal(et, -87836728.81438904)
    spice.kclear()


def test_datetime2et():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    date = datetime(1997, 3, 20, 12, 53, 29)
    et = spice.datetime2et(date)
    npt.assert_almost_equal(et, -87865528.8143913)

    expecteds = [-87865528.8143913, -792086354.8170365, -790847954.8166842]
    dates = [
        datetime(1997, 3, 20, 12, 53, 29),
        datetime(1974, 11, 25, 20, 0, 0),
        datetime(1974, 12, 10, 4, 0, 0),
    ]

    results = spice.datetime2et(dates)
    for expected, result in zip(expecteds, results):
        npt.assert_almost_equal(result, expected)

    # same test, with timezone-aware datetimes
    date = datetime(1997, 3, 20, 12, 53, 29, tzinfo=timezone.utc)
    et = spice.datetime2et(date)
    npt.assert_almost_equal(et, -87865528.8143913)

    expecteds = [-87865528.8143913, -792086354.8170365, -790847954.8166842]
    dates = [
        datetime(1997, 3, 20, 12, 53, 29, tzinfo=timezone.utc),
        datetime(1974, 11, 25, 20, 0, 0, tzinfo=timezone.utc),
        datetime(1974, 12, 10, 4, 0, 0, tzinfo=timezone.utc),
    ]

    results = spice.datetime2et(dates)
    for expected, result in zip(expecteds, results):
        npt.assert_almost_equal(result, expected)

    spice.kclear()


def test_et2datetime():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = -87865528.8143913
    dt = spice.et2datetime(et)
    assert dt == datetime(1997, 3, 20, 12, 53, 29, tzinfo=timezone.utc)

    expecteds = [
        datetime(1997, 3, 20, 12, 53, 29, tzinfo=timezone.utc),
        datetime(1974, 11, 25, 20, 0, 0, tzinfo=timezone.utc),
        datetime(1974, 12, 10, 4, 0, 0, tzinfo=timezone.utc),
    ]
    ets = [-87865528.8143913, -792086354.8170365, -790847954.8166842]

    results = spice.et2datetime(ets)
    for expected, result in zip(expecteds, results):
        assert result == expected

    spice.kclear()


def test_subpnt():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("2008 aug 11 00:00:00")
    num_vals, radii = spice.bodvrd("MARS", "RADII", 3)
    re = radii[0]
    rp = radii[2]
    f = (re - rp) / re
    methods = ["Intercept:  ellipsoid", "Near point: ellipsoid"]
    expecteds = [
        [
            349199089.604657,
            349199089.64135259,
            0.0,
            199.30230503198658,
            199.30230503198658,
            26.262401237213588,
            25.99493675077423,
            160.69769496801342,
            160.69769496801342,
            25.994934171245205,
            25.994934171245202,
        ],
        [
            349199089.6046486,
            349199089.60464859,
            0.0,
            199.30230503240247,
            199.30230503240247,
            25.99493675092049,
            25.99493675092049,
            160.69769496759753,
            160.69769496759753,
            25.729407227461937,
            25.994934171391463,
        ],
    ]
    for expected, method in zip(expecteds, methods):
        spoint, trgepc, srfvec = spice.subpnt(
            method, "Mars", et, "IAU_MARS", "LT+S", "Earth"
        )
        odist = np.linalg.norm(srfvec)
        npt.assert_almost_equal(odist, expected[1], decimal=5)
        spglon, spglat, spgalt = spice.recpgr("mars", spoint, re, f)
        npt.assert_almost_equal(spgalt, expected[2], decimal=5)
        npt.assert_almost_equal(spglon * spice.dpr(), expected[3], decimal=5)
        npt.assert_almost_equal(spglat * spice.dpr(), expected[5], decimal=5)
        spcrad, spclon, spclat = spice.reclat(spoint)
        npt.assert_almost_equal(spclon * spice.dpr(), expected[7], decimal=5)
        npt.assert_almost_equal(spclat * spice.dpr(), expected[9], decimal=5)
        obspos = np.subtract(spoint, srfvec)
        opglon, opglat, opgalt = spice.recpgr("mars", obspos, re, f)
        npt.assert_almost_equal(opgalt, expected[0], decimal=5)
        npt.assert_almost_equal(opglon * spice.dpr(), expected[4], decimal=5)
        npt.assert_almost_equal(opglat * spice.dpr(), expected[6], decimal=5)
        opcrad, opclon, opclat = spice.reclat(obspos)
        npt.assert_almost_equal(opclon * spice.dpr(), expected[8], decimal=5)
        npt.assert_almost_equal(opclat * spice.dpr(), expected[10], decimal=5)
    spice.kclear()


def test_subpt():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("JAN 1, 2006")
    point1, alt1 = np.array(spice.subpt("near point", "earth", et, "lt+s", "moon"))
    point2, alt2 = np.array(spice.subpt("intercept", "earth", et, "lt+s", "moon"))
    dist = np.linalg.norm(np.subtract(point1, point2))
    sep = spice.vsep(point1, point2) * spice.dpr()
    npt.assert_almost_equal(dist, 16.705476097706171)
    npt.assert_almost_equal(sep, 0.15016657506598063)
    # Iterable ET argument to spice.subpt()
    points, alts = spice.subpt(
        "near point", "earth", [et - 20.0, et, et + 20.0], "lt+s", "moon"
    )
    assert 0.0 == spice.vnorm(spice.vsub(points[1], point1))
    assert 0.0 == (alts[1] - alt1)
    # Cleanup
    spice.kclear()


def test_subslr():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("2008 aug 11 00:00:00")
    num_vals, radii = spice.bodvrd("MARS", "RADII", 3)
    re = radii[0]
    rp = radii[2]
    f = (re - rp) / re
    methods = ["Intercept:  ellipsoid", "Near point: ellipsoid"]
    expecteds = [
        [
            0.0,
            175.8106755102322,
            23.668550281477703,
            -175.81067551023222,
            23.420819936106213,
            175.810721536362,
            23.42082337182491,
            -175.810721536362,
            23.42081994605096,
        ],
        [
            0.0,
            175.8106754100492,
            23.420823361866685,
            -175.81067551023222,
            23.175085577910583,
            175.81072152220804,
            23.420823371828,
            -175.81072152220804,
            23.420819946054046,
        ],
    ]
    for expected, method in zip(expecteds, methods):
        spoint, trgepc, srfvec = spice.subslr(
            method, "Mars", et, "IAU_MARS", "LT+S", "Earth"
        )
        spglon, spglat, spgalt = spice.recpgr("mars", spoint, re, f)
        npt.assert_almost_equal(spgalt, expected[0], decimal=5)
        npt.assert_almost_equal(spglon * spice.dpr(), expected[1], decimal=5)
        npt.assert_almost_equal(spglat * spice.dpr(), expected[2], decimal=5)
        spcrad, spclon, spclat = spice.reclat(spoint)
        npt.assert_almost_equal(spclon * spice.dpr(), expected[3], decimal=5)
        npt.assert_almost_equal(spclat * spice.dpr(), expected[4], decimal=5)
        sunpos, sunlt = spice.spkpos("sun", trgepc, "iau_mars", "lt+s", "mars")
        supgln, supglt, supgal = spice.recpgr("mars", sunpos, re, f)
        npt.assert_almost_equal(supgln * spice.dpr(), expected[5], decimal=5)
        npt.assert_almost_equal(supglt * spice.dpr(), expected[6], decimal=5)
        supcrd, supcln, supclt = spice.reclat(sunpos)
        npt.assert_almost_equal(supcln * spice.dpr(), expected[7], decimal=5)
        npt.assert_almost_equal(supclt * spice.dpr(), expected[8], decimal=5)
    spice.kclear()


def test_subsol():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    point = spice.subsol("near point", "earth", 0.0, "lt+s", "mars")
    npt.assert_array_almost_equal(
        point, [5850.44947427, 509.68837118, -2480.24722673], decimal=4
    )
    intercept = spice.subsol("intercept", "earth", 0.0, "lt+s", "mars")
    npt.assert_array_almost_equal(
        intercept, [5844.4362338, 509.16450054, -2494.39569089], decimal=4
    )
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
    point = spice.surfpt(position, u, 1.0, 2.0, 3.0)
    npt.assert_array_almost_equal(point, [1.0, 0.0, 0.0])


def test_surfpv():
    stvrtx = [2.0, 0.0, 0.0, 0.0, 0.0, 3.0]
    stdir = [-1.0, 0.0, 0.0, 0.0, 0.0, 4.0]
    stx = spice.surfpv(stvrtx, stdir, 1.0, 2.0, 3.0)
    expected = [1.0, 0.0, 0.0, 0.0, 0.0, 7.0]
    npt.assert_array_almost_equal(expected, stx)


def test_swpool():
    spice.kclear()
    # add TEST_VAR_SWPOOL
    spice.pdpool("TEST_VAR_SWPOOL", [-666.0])
    # establish check for TEST_VAR_SWPOOL
    spice.swpool("TEST_SWPOOL", 1, 16, ["TEST_VAR_SWPOOL"])
    # update TEST_VAR_SWPOOL
    spice.pdpool("TEST_VAR_SWPOOL", [555.0])
    # check for updated variable
    updated = spice.cvpool("TEST_SWPOOL")
    value = spice.gdpool("TEST_VAR_SWPOOL", 0, 1)
    assert len(value) == 1
    assert value[0] == 555.0
    spice.clpool()
    spice.kclear()
    assert updated is True


def test_sxform():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    lon = 118.25 * spice.rpd()
    lat = 34.05 * spice.rpd()
    alt = 0.0
    utc = "January 1, 1990"
    et = spice.str2et(utc)
    len, abc = spice.bodvrd("EARTH", "RADII", 3)
    equatr = abc[0]
    polar = abc[2]
    f = (equatr - polar) / equatr
    estate = spice.georec(lon, lat, alt, equatr, f)
    estate = np.append(estate, [0.0, 0.0, 0.0])
    xform = np.array(spice.sxform("IAU_EARTH", "J2000", et))
    spice.kclear()
    jstate = np.dot(xform, estate)
    expected = np.array(
        [
            -4131.45969,
            -3308.36805,
            3547.02462,
            0.241249619,
            -0.301019201,
            0.000234215666,
        ]
    )
    npt.assert_array_almost_equal(jstate, expected, decimal=4)


def test_sxform_vectorized():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    utc1 = "January 1, 1990"
    utc2 = "January 1, 2010"
    et1 = spice.str2et(utc1)
    et2 = spice.str2et(utc2)
    step = (et2 - et1) / 240.0
    et = np.arange(240) * step + et1
    xform = spice.sxform("IAU_EARTH", "J2000", et)
    assert len(xform) == 240
    spice.kclear()


def test_szpool():
    assert spice.szpool("MAXVAR") == 26003
    assert spice.szpool("MAXLEN") == 32
    assert spice.szpool("MAXVAL") == 400000
    assert spice.szpool("MXNOTE") == 130015
    assert spice.szpool("MAXAGT") == 1000
    assert spice.szpool("MAXCHR") == 80
    assert spice.szpool("MAXLIN") == 15000


def test_termpt():
    spice.reset()
    spice.kclear()
    spice.furnsh(CoreKernels.spk)
    spice.furnsh(ExtraKernels.marsSpk)
    spice.furnsh(CoreKernels.pck)
    spice.furnsh(CoreKernels.lsk)
    spice.furnsh(ExtraKernels.phobosDsk)
    # set the time
    et = spice.str2et("1972 AUG 11 00:00:00")
    # call limpt
    npts, points, epochs, tangts = spice.termpt(
        "UMBRAL/TANGENT/DSK/UNPRIORITIZED",
        "SUN",
        "Phobos",
        et,
        "IAU_PHOBOS",
        "CN+S",
        "CENTER",
        "MARS",
        [0.0, 0.0, 1.0],
        spice.twopi() / 3.0,
        3,
        1.0e-4,
        1.0e-7,
        10000,
    )
    assert points is not None
    assert len(points) == 3
    spice.kclear()


def test_timdef():
    spice.kclear()
    LSK = os.path.join(cwd, CoreKernels.currentLSK)
    spice.furnsh(LSK)
    # Calendar - default is Gregorian
    value = spice.timdef("GET", "CALENDAR", 10)
    assert value == "GREGORIAN" or "JULIAN" or "MIXED"
    # System - ensure it changes the str2et results
    assert "UTC" == spice.timdef("GET", "SYSTEM", 10)
    # Approximately 64.184
    saveET = spice.str2et("2000-01-01T12:00:00")
    # Change to TDB system
    assert "TDB" == spice.timdef("SET", "SYSTEM", 10, "TDB")
    assert 0.0 == spice.str2et("2000-01-01T12:00:00")
    # Change back to UTC system
    assert "UTC" == spice.timdef("SET", "SYSTEM", 10, "UTC")
    assert saveET == spice.str2et("2000-01-01T12:00:00")
    # Cleanup
    spice.kclear()


def test_timout():
    sample = "Thu Oct 1 11:11:11 PDT 1111"
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    pic, ok, err = spice.tpictr(sample)
    assert ok
    et = 188745364.0
    out = spice.timout(et, pic)
    assert out == "Sat Dec 24 18:14:59 PDT 2005"
    spice.kclear()


def test_timout_vectorized():
    sample = "Thu Oct 1 11:11:11 PDT 1111"
    lenout = len(sample) + 2
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    pic, ok, err = spice.tpictr(sample, 64, 60)
    assert ok
    et = np.array(np.arange(5) * 10000) + 188745364.0
    out = list(spice.timout(et, pic, lenout))
    expected = [
        "Sat Dec 24 18:14:59 PDT 2005",
        "Sat Dec 24 21:01:39 PDT 2005",
        "Sat Dec 24 23:48:19 PDT 2005",
        "Sun Dec 25 02:34:59 PDT 2005",
        "Sun Dec 25 05:21:39 PDT 2005",
    ]
    for e in expected:
        assert e in out
    spice.kclear()


def test_tipbod():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("Jan 1 2005")
    tipm = spice.tipbod("J2000", 699, et)
    assert tipm is not None
    spice.kclear()


def test_tisbod():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("Jan 1 2005")
    tsipm = spice.tisbod("J2000", 699, et)
    assert tsipm is not None
    spice.kclear()


def test_tkfram():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(CassiniKernels.cassFk)
    rotation, nextFrame = spice.tkfram(-82001)
    expected = np.array(
        [
            [6.12323400e-17, 0.00000000e00, -1.00000000e00],
            [0.00000000e00, 1.00000000e00, -0.00000000e00],
            [1.00000000e00, 0.00000000e00, 6.12323400e-17],
        ]
    )
    npt.assert_array_almost_equal(rotation, expected)
    assert nextFrame == -82000
    spice.kclear()


def test_tkvrsn():
    version = spice.tkvrsn("toolkit")
    assert version == "CSPICE_N0066"


def test_tparse():
    actual_one, error_one = spice.tparse("1996-12-18T12:28:28")
    assert actual_one == -95815892.0
    actual_two, error_two = spice.tparse("1 DEC 1997 12:28:29.192")
    assert actual_two == -65748690.808
    actual_three, error_three = spice.tparse("1997-162::12:18:28.827")
    assert actual_three == -80696491.173


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


# test_trcoff() cannot be done anywhere but last
def teardown_test_trcoff():
    spice.reset()
    spice.kclear()
    # Initialize stack trace with two values, and test
    spice.chkin("A")
    spice.chkin("B")
    assert 2 == spice.trcdep()
    assert "B" == spice.trcnam(1)
    assert "A" == spice.trcnam(0)
    # Turn off tracing and test
    spice.trcoff()
    assert 0 == spice.trcdep()
    assert "" == spice.qcktrc(2)
    # Ensure subsequent checkins are also ignored
    spice.chkin("C")
    assert 0 == spice.trcdep()
    # Cleanup
    spice.reset()
    spice.kclear()


def test_tsetyr():
    spice.reset()

    # Expand 2-digit year to full year, typically 4-digit
    def tmp_getyr4(iy2):
        return int(spice.etcal(spice.tparse("3/3/{:02}".format(iy2), 22)[0]).split()[0])

    # Find current lower bound on the 100 year interval of expansion,
    # so it can be restored on exit
    tsetyr_lowerbound = tmp_getyr4(0)
    for iy2_test in range(100):
        tmp_lowerbound = tmp_getyr4(iy2_test)
        if tmp_lowerbound < tsetyr_lowerbound:
            tsetyr_lowerbound = tmp_lowerbound
            break
    # Run first case with a year not ending in 00
    tsetyr_y2 = tsetyr_lowerbound % 100
    tsetyr_y4 = tsetyr_lowerbound + 200 + ((tsetyr_y2 == 0) and 50 or 0)
    spice.tsetyr(tsetyr_y4)
    assert tmp_getyr4(tsetyr_y4 % 100) == tsetyr_y4
    assert tmp_getyr4((tsetyr_y4 - 1) % 100) == (tsetyr_y4 + 99)
    # Run second case with a year ending in 00
    tsetyr_y4 -= tsetyr_y4 % 100
    spice.tsetyr(tsetyr_y4)
    assert tmp_getyr4(tsetyr_y4 % 100) == tsetyr_y4
    assert tmp_getyr4((tsetyr_y4 - 1) % 100) == (tsetyr_y4 + 99)
    # Cleanup:  reset lowerbound to what it was when this routine started
    tsetyr_y4 = tsetyr_lowerbound
    spice.tsetyr(tsetyr_y4)
    assert tmp_getyr4(tsetyr_y4 % 100) == tsetyr_y4
    assert tmp_getyr4((tsetyr_y4 - 1) % 100) == (tsetyr_y4 + 99)
    assert not spice.failed()
    spice.reset()


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
    spice.kclear()

    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("JAN 1 2009")

    @spiceypy.utils.callbacks.SpiceUDFUNC
    def udfunc(et_in):
        pos, new_et = spice.spkpos("MERCURY", et_in, "J2000", "LT+S", "MOON")
        return new_et

    assert spice.uddc(udfunc, et, 1.0)

    spice.kclear()


def test_uddf():
    spice.kclear()

    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("JAN 1 2009")

    @spiceypy.utils.callbacks.SpiceUDFUNS
    def udfunc(et_in):
        pos, new_et = spice.spkpos("MERCURY", et_in, "J2000", "LT+S", "MOON")
        return new_et

    deriv = spice.uddf(udfunc, et, 1.0)

    npt.assert_almost_equal(deriv, -0.000135670940)
    spice.kclear()


def test_udf():
    assert spice.udf(0.0) == 0.0


def test_union():
    # SPICEINT_CELL
    test_cell_one = spice.cell_int(8)
    test_cell_two = spice.cell_int(8)
    spice.insrti(1, test_cell_one)
    spice.insrti(2, test_cell_one)
    spice.insrti(3, test_cell_one)
    spice.insrti(2, test_cell_two)
    spice.insrti(3, test_cell_two)
    spice.insrti(4, test_cell_two)
    out_cell = spice.union(test_cell_one, test_cell_two)
    assert [x for x in out_cell] == [1, 2, 3, 4]
    # SPICECHAR_CELL
    test_cell_one = spice.cell_char(8, 8)
    test_cell_two = spice.cell_char(8, 8)
    spice.insrtc("1", test_cell_one)
    spice.insrtc("2", test_cell_one)
    spice.insrtc("3", test_cell_one)
    spice.insrtc("2", test_cell_two)
    spice.insrtc("3", test_cell_two)
    spice.insrtc("4", test_cell_two)
    out_cell = spice.union(test_cell_one, test_cell_two)
    assert [x for x in out_cell] == ["1", "2", "3", "4"]
    # SPICEDOUBLE_CELL
    test_cell_one = spice.cell_double(8)
    test_cell_two = spice.cell_double(8)
    spice.insrtd(1.0, test_cell_one)
    spice.insrtd(2.0, test_cell_one)
    spice.insrtd(3.0, test_cell_one)
    spice.insrtd(2.0, test_cell_two)
    spice.insrtd(3.0, test_cell_two)
    spice.insrtd(4.0, test_cell_two)
    out_cell = spice.union(test_cell_one, test_cell_two)
    assert [x for x in out_cell] == [1.0, 2.0, 3.0, 4.0]
    # SPICEBOOLEAN_CELL
    test_cell_one = spice.cell_bool(9)
    test_cell_two = spice.cell_bool(9)
    with pytest.raises(NotImplementedError):
        spice.union(test_cell_one, test_cell_two)


def test_unitim():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("Dec 19 2003")
    converted_et = spice.unitim(et, "ET", "JED")
    npt.assert_almost_equal(converted_et, 2452992.5007428653)
    spice.kclear()


def test_unload():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    # 4 kernels + the meta kernel = 5
    assert spice.ktotal("ALL") == 5
    # Make list of FURNSHed non-meta-kernels
    kernel_list = []
    for iKernel in range(spice.ktotal("ALL")):
        filnam, filtyp, srcnam, handle = spice.kdata(iKernel, "ALL", 999, 999, 999)
        if filtyp != "META":
            kernel_list.append(filnam)
    assert len(kernel_list) > 0
    # Unload all kernels
    spice.unload(CoreKernels.testMetaKernel)
    assert spice.ktotal("ALL") == 0
    spice.kclear()
    # Test passing the [list of kernels] as an argument to spice.unload
    spice.furnsh(kernel_list)
    assert spice.ktotal("ALL") == len(kernel_list)
    spice.unload(kernel_list[1:])
    assert spice.ktotal("ALL") == 1
    spice.unload(kernel_list[:1])
    assert spice.ktotal("ALL") == 0


def test_unload_emptystring():
    spice.kclear()
    with pytest.raises(spice.stypes.SpiceyError):
        spice.unload("")
    spice.kclear()


def test_unorm():
    v1 = np.array([5.0, 12.0, 0.0])
    expected_vout = np.array([5.0 / 13.0, 12.0 / 13.0, 0.0])
    expected_vmag = 13.0
    vout, vmag = spice.unorm(v1)
    assert vmag == expected_vmag
    assert np.array_equal(expected_vout, vout)


def test_unormg():
    v1 = np.array([5.0, 12.0])
    expected_vout = np.array([5.0 / 13.0, 12.0 / 13.0])
    expected_vmag = 13.0
    vout, vmag = spice.unormg(v1, 2)
    assert vmag == expected_vmag
    assert np.array_equal(expected_vout, vout)


def test_utc2et():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    utcstr = "December 1, 2004 15:04:11"
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
    a = spice.cell_double(20)
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
    expected = np.array([5 / 13.0, 12 / 13.0, 0.0])
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
    v1 = np.array([1.0e0, 2.0e0, 2.0e0])
    assert spice.vnorm(v1) == 3.0e0


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
    assert spice.vsep(v1, v2) == np.pi / 2


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
    window = spice.cell_double(8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    for d in darray:
        spice.wninsd(d[0], d[1], window)
    assert spice.wncard(window) == 3


def test_wncomd():
    window1 = spice.cell_double(8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    for d in darray:
        spice.wninsd(d[0], d[1], window1)
    assert spice.wncard(window1) == 3
    window2 = spice.wncomd(2.0, 20.0, window1)
    assert spice.wncard(window2) == 2
    assert spice.wnfetd(window2, 0) == (3.0, 7.0)
    assert spice.wnfetd(window2, 1) == (11.0, 20.0)


def test_wncond():
    window = spice.cell_double(8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    for d in darray:
        spice.wninsd(d[0], d[1], window)
    assert spice.wncard(window) == 3
    window = spice.wncond(2.0, 1.0, window)
    assert spice.wncard(window) == 2
    assert spice.wnfetd(window, 0) == (9.0, 10.0)
    assert spice.wnfetd(window, 1) == (25.0, 26.0)


def test_wndifd():
    window1 = spice.cell_double(8)
    window2 = spice.cell_double(8)
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
    window = spice.cell_double(8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    for d in darray:
        spice.wninsd(d[0], d[1], window)
    assert spice.wncard(window) == 3
    array = [0.0, 1.0, 9.0, 13.0, 29.0]
    expected = [False, True, True, False, False]
    for a, exp in zip(array, expected):
        assert spice.wnelmd(a, window) == exp


def test_wnexpd():
    window = spice.cell_double(8)
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
    window = spice.cell_double(8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0], [29.0, 29.0]]
    for d in darray:
        spice.wninsd(d[0], d[1], window)
    assert spice.wncard(window) == 4
    window = spice.wnextd("L", window)
    assert spice.wncard(window) == 4
    assert spice.wnfetd(window, 0) == (1.0, 1.0)
    assert spice.wnfetd(window, 1) == (7.0, 7.0)
    assert spice.wnfetd(window, 2) == (23.0, 23.0)
    assert spice.wnfetd(window, 3) == (29.0, 29.0)


def test_wnfetd():
    window = spice.cell_double(8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    for d in darray:
        spice.wninsd(d[0], d[1], window)
    assert spice.wncard(window) == 3
    assert spice.wnfetd(window, 0) == (1.0, 3.0)
    assert spice.wnfetd(window, 1) == (7.0, 11.0)
    assert spice.wnfetd(window, 2) == (23.0, 27.0)


def test_wnfild():
    window = spice.cell_double(8)
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
    window = spice.cell_double(8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0], [29.0, 29.0]]
    for d in darray:
        spice.wninsd(d[0], d[1], window)
    assert spice.wncard(window) == 4
    window = spice.wnfltd(3.0, window)
    assert spice.wncard(window) == 2
    assert spice.wnfetd(window, 0) == (7.0, 11.0)
    assert spice.wnfetd(window, 1) == (23.0, 27.0)


def test_wnincd():
    window = spice.cell_double(8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    for d in darray:
        spice.wninsd(d[0], d[1], window)
    assert spice.wncard(window) == 3
    array = [[1.0, 3.0], [9.0, 10.0], [0.0, 2.0], [13.0, 15.0], [29.0, 30.0]]
    expected = [True, True, False, False, False]
    for a, exp in zip(array, expected):
        assert spice.wnincd(a[0], a[1], window) == exp


def test_wninsd():
    window = spice.cell_double(8)
    darray = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    for d in darray:
        spice.wninsd(d[0], d[1], window)
    assert spice.wncard(window) == 3
    assert [x for x in window] == [1.0, 3.0, 7.0, 11.0, 23.0, 27.0]


def test_wnintd():
    window1 = spice.cell_double(8)
    window2 = spice.cell_double(8)
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
    window1 = spice.cell_double(8)
    window2 = spice.cell_double(8)
    darray1 = [[1.0, 3.0], [7.0, 11.0], [23.0, 27.0]]
    darray2 = [[1.0, 2.0], [9.0, 9.0], [24.0, 27.0]]
    for d in darray1:
        spice.wninsd(d[0], d[1], window1)
    assert spice.wncard(window1) == 3
    for d in darray2:
        spice.wninsd(d[0], d[1], window2)
    assert spice.wncard(window2) == 3
    ops = ["=", "<>", "<=", "<", ">=", ">"]
    expected = [False, True, False, False, True, True]
    for op, exp in zip(ops, expected):
        assert spice.wnreld(window1, op, window2) == exp


def test_wnsumd():
    window = spice.cell_double(12)
    darray = [
        [1.0, 3.0],
        [7.0, 11.0],
        [18.0, 18.0],
        [23.0, 27.0],
        [30.0, 69.0],
        [72.0, 80.0],
    ]
    for d in darray:
        spice.wninsd(d[0], d[1], window)
    meas, avg, stddev, shortest, longest = spice.wnsumd(window)
    assert meas == 57.0
    assert avg == 9.5
    assert np.around(stddev, decimals=6) == 13.413302
    assert shortest == 4
    assert longest == 8


def test_wnunid():
    window1 = spice.cell_double(8)
    window2 = spice.cell_double(8)
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
    window = spice.cell_double(30)
    array = [
        [0.0, 0.0],
        [10.0, 12.0],
        [2.0, 7.0],
        [13.0, 15.0],
        [1.0, 5.0],
        [23.0, 29.0],
        [0.0, 0.0],
        [0.0, 0.0],
        [0.0, 0.0],
        [0.0, 0.0],
    ]
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
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("Jan 1, 2009")
    m = spice.sxform("IAU_EARTH", "J2000", et)
    eulang, unique = spice.xf2eul(m, 3, 1, 3)
    assert unique
    expected = [
        1.571803284049681,
        0.0008750002978301174,
        2.9555269829740034,
        3.5458495690569166e-12,
        3.080552365717176e-12,
        -7.292115373266558e-05,
    ]
    npt.assert_array_almost_equal(expected, eulang)
    spice.kclear()


def test_xf2rav():
    e = [1.0, 0.0, 0.0]
    rz = [[0.0, 1.0, 0.0], [-1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
    xform = spice.rav2xf(rz, e)
    rz2, e2 = spice.xf2rav(xform)
    npt.assert_array_almost_equal(e, e2)
    npt.assert_array_almost_equal(rz, rz2)


def test_xfmsta():
    spice.kclear()
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("July 4, 2003 11:00 AM PST")
    state, lt = spice.spkezr("Mars", et, "J2000", "LT+S", "Earth")
    expected_lt = 269.6898813661505
    expected_state = [
        7.38222353105354905128e07,
        -2.71279189984722770751e07,
        -1.87413063014898747206e07,
        -6.80851334001380692484e00,
        7.51399612408221173609e00,
        3.00129849265935222391e00,
    ]
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state)
    state_lat = spice.xfmsta(state, "rectangular", "latitudinal", " ")
    expected_lat_state = [
        8.08509924324866235256e07,
        -3.52158255331780634112e-01,
        -2.33928262716770696272e-01,
        -9.43348972618204761886e00,
        5.98157681117165682860e-08,
        1.03575559016377728336e-08,
    ]
    npt.assert_array_almost_equal(state_lat, expected_lat_state)
    spice.kclear()


def test_xpose6():
    m1 = [
        [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
        [0.0, 7.0, 8.0, 9.0, 10.0, 11.0],
        [0.0, 0.0, 12.0, 13.0, 14.0, 15.0],
        [0.0, 0.0, 0.0, 16.0, 17.0, 18.0],
        [0.0, 0.0, 0.0, 0.0, 19.0, 20.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 21.0],
    ]
    mout_expected = np.array(m1).transpose().tolist()
    npt.assert_array_almost_equal(spice.xpose6(m1), mout_expected)


def test_xpose():
    m1 = [[1.0, 2.0, 3.0], [0.0, 4.0, 5.0], [0.0, 6.0, 0.0]]
    npt.assert_array_almost_equal(
        spice.xpose(m1), [[1.0, 0.0, 0.0], [2.0, 4.0, 6.0], [3.0, 5.0, 0.0]]
    )
    npt.assert_array_almost_equal(
        spice.xpose(np.array(m1)), [[1.0, 0.0, 0.0], [2.0, 4.0, 6.0], [3.0, 5.0, 0.0]]
    )


def test_xposeg():
    m1 = [[1.0, 2.0, 3.0], [0.0, 4.0, 5.0], [0.0, 6.0, 0.0]]
    npt.assert_array_almost_equal(
        spice.xposeg(m1, 3, 3), [[1.0, 0.0, 0.0], [2.0, 4.0, 6.0], [3.0, 5.0, 0.0]]
    )
    npt.assert_array_almost_equal(
        spice.xposeg(np.array(m1), 3, 3),
        [[1.0, 0.0, 0.0], [2.0, 4.0, 6.0], [3.0, 5.0, 0.0]],
    )


def test_zzdynrot():
    spice.kclear()
    spice.furnsh(ExtraKernels.mroFk)
    rotation, frame = spice.zzdynrot(-74900, 499, 221051477.42023)
    expected = np.array(
        [
            [0.6733481, 0.73932559, 0.0],
            [-0.5895359, 0.53692566, 0.60345527],
            [0.44614992, -0.40633546, 0.79739685],
        ]
    )
    npt.assert_array_almost_equal(rotation, expected)
    assert frame == 1
    spice.kclear()


def teardown_tests():
    # Tests that must be done last are put here and
    # scheduled in teardown_module()
    teardown_test_trcoff()


def teardown_module(module):
    teardown_tests()
    # if you are developing spiceypy, and don't want to delete kernels each time you run the tests, set
    # set the following environment variable "spiceypy_do_not_remove_kernels" to anything
    if not os.environ.get("spiceypy_do_not_remove_kernels"):
        cleanup_cassini_kernels()
        cleanup_extra_kernels()
        cleanup_core_kernels()
