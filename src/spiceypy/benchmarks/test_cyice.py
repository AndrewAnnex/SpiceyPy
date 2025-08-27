import os
import time
import timeit
import itertools

import pytest


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
import numpy as np
import numpy.testing as npt
import spiceypy as spice
from spiceypy.cyice import cyice


def get_module_name(func):
    module = f"{func.__module__.split('.')[-1]}"
    if module == 'cyice':
        if '_s' in func.__name__:
            return module+'_s'
        elif '_v' in func.__name__:
            return module+'_v'
    return module

# https://pytest-benchmark.readthedocs.io/en/latest/pedantic.html

@pytest.fixture
def load_core_kernels():
    spice.furnsh(CoreKernels.testMetaKernel)

@pytest.fixture
def load_cassini_kernels():
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(CassiniKernels.cassSclk)
    spice.furnsh(CassiniKernels.cassFk)
    spice.furnsh(CassiniKernels.cassPck)
    spice.furnsh(CassiniKernels.cassIk)
    spice.furnsh(CassiniKernels.cassSclk)
    spice.furnsh(CassiniKernels.satSpk)
    spice.furnsh(CassiniKernels.cassTourSpk)
    spice.furnsh(CassiniKernels.cassCk)

@pytest.fixture
def load_voyager_kernels():
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.voyagerSclk)

@pytest.fixture
def load_earth_kernels():
    spice.furnsh(ExtraKernels.earthStnSpk)
    spice.furnsh(ExtraKernels.earthHighPerPck)
    spice.furnsh(ExtraKernels.earthTopoTf)
    spice.furnsh(CoreKernels.testMetaKernel)

@pytest.fixture(autouse=True)
def clear_kernel_pool_and_reset():
    spice.kclear()
    spice.reset()
    # yield for test
    yield
    # clear kernel pool again
    spice.kclear()
    spice.reset()

@pytest.fixture
def grouped_benchmark(request, benchmark):
    benchmark.group = request.param
    return benchmark


def setup_module(module):
    download_kernels()

#A

@pytest.mark.parametrize('function', [cyice.azlcpo_s, cyice.azlcpo, spice.azlcpo], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["azlcpo"], indirect=True)
def test_azlcpo(function, grouped_benchmark, load_core_kernels, load_earth_kernels):
    et = spice.str2et("2003 Oct 13 06:00:00 UTC")
    obspos = np.array([-2353.621419700, -4641.341471700, 3677.052317800])
    azlsta, lt = grouped_benchmark(function, "ELLIPSOID", "VENUS", et, "CN+S", False, True, obspos, "EARTH", "ITRF93")
    assert azlsta == pytest.approx([2.45721479e8, 5.13974044, -8.54270565e-1, -4.68189831, 7.02070016e-5, -5.39579640e-5])


@pytest.mark.parametrize('function', [cyice.azlcpo_v, cyice.azlcpo], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["azlcpo_v"], indirect=True)
def test_azlcpo_v(function, grouped_benchmark, load_core_kernels, load_earth_kernels):
    et = spice.str2et("2003 Oct 13 06:00:00 UTC")
    obspos = np.array([[-2353.621419700, -4641.341471700, 3677.052317800]])
    ets = np.repeat(et, 100)
    obsposs = np.repeat(obspos, 100, axis=0)
    azlsta, lt = grouped_benchmark(function, "ELLIPSOID", "VENUS", ets, "CN+S", False, True, obsposs, "EARTH", "ITRF93")
    assert azlsta[0,0] == pytest.approx([2.45721479e8, 5.13974044, -8.54270565e-1, -4.68189831, 7.02070016e-5, -5.39579640e-5])
    assert azlsta.shape == (100, 100, 6)
    assert lt.shape == (100, 100)


@pytest.mark.parametrize('function', [cyice.azlrec_s, cyice.azlrec, spice.azlrec], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["azlrec"], indirect=True)
def test_azlrec(function, grouped_benchmark):
    res = grouped_benchmark(function, 1.0, np.radians(90.0), 0.0, True, True)
    expected = np.array([0.0, 1.0, 0.0])
    npt.assert_array_almost_equal(res, expected)


@pytest.mark.parametrize('function', [cyice.azlrec_v, cyice.azlrec], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["azlrec_v"], indirect=True)
def test_azlrec_v(function, grouped_benchmark):
    inrange = np.ones(100, dtype=float)
    az = np.repeat(np.radians(90), 100)
    el = np.zeros(100, dtype=float)
    res = grouped_benchmark(function, inrange, az, el, True, True)
    assert isinstance(res, np.ndarray)
    expected = np.array([[0.0, 1.0, 0.0]])
    expected_v = np.repeat(expected, 100, axis=0)
    npt.assert_array_almost_equal(res, expected_v)


#B

@pytest.mark.parametrize('function', [cyice.b1900, spice.b1900], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["b1900"], indirect=True)
def test_b1900(function, grouped_benchmark):
    grouped_benchmark(function)
    assert function() == 2415020.31352


@pytest.mark.parametrize('function', [cyice.b1950, spice.b1950], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["b1950"], indirect=True)
def test_b1950(function, grouped_benchmark):
    grouped_benchmark(function)
    assert function() == 2433282.42345905

# C

@pytest.mark.parametrize('function', [cyice.ckgp_s, cyice.ckgp, spice.ckgp], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["ckgp"], indirect=True)
def test_ckgp(function, grouped_benchmark, load_cassini_kernels):
    ckid  = -82000
    cover = 267832537952.0
    tol = 256.0
    ref = "J2000"
    grouped_benchmark(function, ckid, cover, tol, ref)
    res = function(ckid, cover, tol, ref)
    cmat, clkout = res[0], res[1]
    assert clkout == 267832537952.0
    assert isinstance(cmat, np.ndarray)
    expected_cmat = np.array([
        [0.5064665782997639365, -0.75794210739897316387, 0.41111478554891744963],
        [-0.42372128242505308071, 0.19647683351734512858, 0.88422685364733510927],
        [-0.7509672961490383436, -0.6220294331642198804, -0.22164725216433822652],
    ])
    npt.assert_array_almost_equal(cmat, expected_cmat)


@pytest.mark.parametrize('function', [cyice.ckgp, cyice.ckgp_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["ckgp_v"], indirect=True)
def test_ckgp_v(function, grouped_benchmark, load_cassini_kernels):
    ckid  = -82000
    covers = np.repeat(267832537952.0,100)
    tol = 256.0
    ref = "J2000"
    grouped_benchmark(function, ckid, covers, tol, ref)
    res = function(ckid, covers, tol, ref)
    cmat, clkout = res[0], res[1]
    assert isinstance(cmat, np.ndarray)
    assert isinstance(clkout, np.ndarray)
    assert clkout[0] == 267832537952.0


@pytest.mark.parametrize('function', [cyice.ckgpav_s, cyice.ckgpav, spice.ckgpav], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["ckgpav"], indirect=True)
def test_ckgpav(function, grouped_benchmark, load_cassini_kernels):
    ckid  = -82000
    cover = 267832537952.0
    tol = 256.0
    ref = "J2000"
    grouped_benchmark(function, ckid, cover, tol, ref)
    res = function(ckid, cover, tol, ref)
    cmat, avout, clkout = res[0], res[1], res[2]
    assert clkout == 267832537952.0
    assert isinstance(cmat, np.ndarray)
    assert isinstance(avout, np.ndarray)
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


@pytest.mark.parametrize('function', [cyice.ckgpav, cyice.ckgpav_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["ckgpav_v"], indirect=True)
def test_ckgpav_v(function, grouped_benchmark, load_cassini_kernels):
    ckid  = -82000
    covers = np.repeat(267832537952.0,100)
    tol = 256.0
    ref = "J2000"
    grouped_benchmark(function, ckid, covers, tol, ref)
    res = function(ckid, covers, tol, ref)
    cmat, avout, clkout = res[0], res[1], res[2]
    assert clkout[0] == 267832537952.0


@pytest.mark.parametrize('function', [cyice.clight, spice.clight], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["clight"], indirect=True)
def test_clight(function, grouped_benchmark):
    grouped_benchmark(function)
    assert function() == 299792.458


@pytest.mark.parametrize('function', [cyice.conics_s, cyice.conics, spice.conics], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["conics"], indirect=True)
def test_conics(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("Dec 25, 2007")
    state, ltime = spice.spkezr("Moon", et, "J2000", "NONE", "EARTH")
    dim, mu = spice.bodvrd("EARTH", "GM", 1)
    elts = spice.oscelt(state, et, mu[0])
    later = et + 7.0 * spice.spd()
    grouped_benchmark(function, elts, later)
    # now test correctness
    later_state = function(elts, later)
    assert isinstance(later_state, np.ndarray)
    state, ltime = spice.spkezr("Moon", later, "J2000", "NONE", "EARTH")
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


@pytest.mark.parametrize('function', [cyice.conics_v, cyice.conics], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["conics_v"], indirect=True)
def test_conics_v(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("Dec 25, 2007")
    state, ltime = spice.spkezr("Moon", et, "J2000", "NONE", "EARTH")
    dim, mu = spice.bodvrd("EARTH", "GM", 1)
    elts = spice.oscelt(state, et, mu[0])
    later = et + 7.0 * spice.spd()
    elts_v = np.repeat([elts], 100, axis=0)
    later_v = np.repeat(later, 100)
    grouped_benchmark(function, elts_v, later_v)
    # now test correctness
    later_state = function(elts_v, later_v)
    assert isinstance(later_state, np.ndarray)
    state, ltime = spice.spkezr("Moon", later, "J2000", "NONE", "EARTH")
    pert = np.array(later_state[0]) - np.array(state)
    expected_pert = [
        -7.48885583081946242601e03,
        3.97608014470621128567e02,
        1.95744667259379639290e02,
        -3.61527427787390887026e-02,
        -1.27926899069508159812e-03,
        -2.01458906615054056388e-03,
    ]
    npt.assert_array_almost_equal(pert, expected_pert, decimal=5)


@pytest.mark.parametrize('function', [cyice.convrt_s, cyice.convrt, spice.convrt], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["convrt"], indirect=True)
def test_convrt(function, grouped_benchmark):
    grouped_benchmark(function, 1.0, "parsecs", "lightyears")
    assert function(300.0, "statute_miles", "km") == 482.80320


@pytest.mark.parametrize('function', [cyice.convrt_v, cyice.convrt, spice.convrt], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["convrt_v"], indirect=True)
def test_convrt_v(function, grouped_benchmark):
    data = np.arange(0, 1000.0, dtype=np.double)
    grouped_benchmark(function, data, "parsecs", "lightyears")
    res = function(data, "parsecs", "lightyears")
    assert isinstance(res, np.ndarray)


@pytest.mark.parametrize('function', [cyice.cyllat_s, cyice.cyllat, spice.cyllat], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["cyllat"], indirect=True)
def test_cyllat(function, grouped_benchmark):
    r   = 1.0
    clon = 180.0 * spice.rpd()
    z = -1.0
    res = grouped_benchmark(function, r, clon, z)
    expected = np.array([np.sqrt(2), np.pi, -np.pi / 4])
    npt.assert_array_almost_equal(res, expected, decimal=7)


@pytest.mark.parametrize('function', [cyice.cyllat_v, cyice.cyllat], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["cyllat_v"], indirect=True)
def test_cyllat_v(function, grouped_benchmark):
    r   = np.ones(100, order='C')
    clon = np.repeat(180.0, 100) * spice.rpd()
    z = -np.ones(100, order='C')
    res = grouped_benchmark(function, r, clon, z)
    assert isinstance(res, np.ndarray)
    expected = np.array([[np.sqrt(2), np.pi, -np.pi / 4]])
    expected_v = np.repeat(expected, 100, axis=0)
    npt.assert_array_almost_equal(res, expected_v, decimal=7)


@pytest.mark.parametrize('function', [cyice.cylrec_s, cyice.cylrec, spice.cylrec], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["cylrec"], indirect=True)
def test_cylrec(function, grouped_benchmark):
    r   = 0.0
    clon = np.radians(33.0)
    z = 0.0
    res = grouped_benchmark(function, r, clon, z)
    assert isinstance(res, np.ndarray)
    expected = np.array([0.0, 0.0, 0.0])
    npt.assert_array_almost_equal(res, expected, decimal=7)


@pytest.mark.parametrize('function', [cyice.cylrec_v, cyice.cylrec], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["cylrec_v"], indirect=True)
def test_cylrec_v(function, grouped_benchmark):
    r    = np.zeros(100, order='C')
    clon = np.repeat(np.radians(33.0), 100)
    z    = np.zeros(100, order='C')
    res = grouped_benchmark(function, r, clon, z)
    assert isinstance(res, np.ndarray)
    expected_v = np.zeros((100,3))
    npt.assert_array_almost_equal(res, expected_v, decimal=7)


@pytest.mark.parametrize('function', [cyice.cylsph_s, cyice.cylsph, spice.cylsph], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["cylsph"], indirect=True)
def test_cylsph(function, grouped_benchmark):
    res = grouped_benchmark(function, 1.0, np.deg2rad(180.0), 1.0)
    expected = np.array([1.4142, np.deg2rad(45.0), np.deg2rad(180.0)])
    npt.assert_array_almost_equal(res, expected, decimal=4)


@pytest.mark.parametrize('function', [cyice.cylsph_v, cyice.cylsph], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["cylsph_v"], indirect=True)
def test_cylsph_v(function, grouped_benchmark):
    r   = np.ones(100, order='C')
    clon = np.repeat(np.deg2rad(180.0), 100)
    z = np.ones(100, order='C')
    res = grouped_benchmark(function, r, clon, z)
    assert isinstance(res, np.ndarray)
    expected = np.array([[1.4142, np.deg2rad(45.0), np.deg2rad(180.0)]])
    expected_v = np.repeat(expected, 100, axis=0)
    npt.assert_array_almost_equal(res, expected_v, decimal=4)


# D
@pytest.mark.parametrize('function', [cyice.deltet_s, cyice.deltet, spice.deltet], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["deltet"], indirect=True)
def test_deltet(function, grouped_benchmark, load_core_kernels):
    et_2004 = spice.str2et("Jan 1 2004")
    grouped_benchmark(function, et_2004, "ET")


@pytest.mark.parametrize('function', [cyice.deltet_v, cyice.deltet], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["deltet_v"], indirect=True)
def test_deltet_v(function, grouped_benchmark, load_core_kernels):
    ets_2004 = np.repeat(spice.str2et("Jan 1 2004"), 100)
    grouped_benchmark(function, ets_2004, "ET")
    res = function(ets_2004, "ET")
    assert isinstance(res, np.ndarray)


@pytest.mark.parametrize('function', [cyice.dpr, spice.dpr], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["dpr"], indirect=True)
def test_dpr(function, grouped_benchmark):
    grouped_benchmark(function)
    assert function() == 180.0 / np.arccos(-1.0)

# E

@pytest.mark.parametrize('function', [cyice.et2lst_s, cyice.et2lst, spice.et2lst], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["et2lst"], indirect=True)
def test_et2lst(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("2004 may 17 16:30:00")
    lon = 281.49521300000004 * spice.rpd()
    grouped_benchmark(function, et, 399, lon, "planetocentric")
    hr, mn, sc, time, ampm = function(
        et, 399, lon, "planetocentric"
    )
    assert hr == 11
    assert mn == 19
    assert sc == 22
    assert time == "11:19:22"
    assert ampm == "11:19:22 A.M."


@pytest.mark.parametrize('function', [cyice.et2lst_v, cyice.et2lst], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["et2lst_v"], indirect=True)
def test_et2lst_v(function, grouped_benchmark, load_core_kernels):
    ets = np.repeat(spice.str2et("2004 may 17 16:30:00"), 100)
    lon = 281.49521300000004 * spice.rpd()
    grouped_benchmark(function, ets, 399, lon, "planetocentric")
    hr, mn, sc, time, ampm = function(
        ets, 399, lon, "planetocentric"
    )
    assert hr[0] == 11
    assert mn[0] == 19
    assert sc[0] == 22
    assert time[0] == "11:19:22"
    assert ampm[0] == "11:19:22 A.M."
    assert len(time) == 100
    assert isinstance(time, np.ndarray)
    assert isinstance(hr, np.ndarray)


@pytest.mark.parametrize('function', [cyice.et2utc_s, cyice.et2utc, spice.et2utc], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["et2utc"], indirect=True)
def test_et2utc(function, grouped_benchmark, load_core_kernels):
    grouped_benchmark(function,  -527644192.5403653, "J", 6)


@pytest.mark.parametrize('function', [cyice.et2utc_v, cyice.et2utc, spice.et2utc], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["et2utc_v"], indirect=True)
def test_et2utc_v(function, grouped_benchmark, load_core_kernels):
    ets = np.repeat(-527644192.5403653, 100)
    grouped_benchmark(function, ets, "J", 6)
    expected_res = np.repeat("JD 2445438.006415", 100)
    res = function(ets, "J", 6)
    assert isinstance(res, np.ndarray)
    assert np.array_equal(res, expected_res)


@pytest.mark.parametrize('function', [cyice.etcal_s, cyice.etcal, spice.etcal], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["etcal"], indirect=True)
def test_etcal(function, grouped_benchmark):
    grouped_benchmark(function, 0.0)


@pytest.mark.parametrize('function', [cyice.etcal_v, cyice.etcal, spice.etcal], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["etcal_v"], indirect=True)
def test_etcal_v(function, grouped_benchmark):
    data = np.arange(10000.0, dtype=np.double)
    grouped_benchmark(function, data)
    res = function(data)
    assert isinstance(res, np.ndarray)

@pytest.mark.parametrize('function', [cyice.evsgp4_s, cyice.evsgp4, spice.evsgp4], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["evsgp4"], indirect=True)
def test_evsgp4(function, grouped_benchmark, load_core_kernels):
    spice.furnsh(ExtraKernels.geophKer)
    tle = np.array([
        "1 43908U 18111AJ  20146.60805006  .00000806  00000-0  34965-4 0  9999",
        "2 43908  97.2676  47.2136 0020001 220.6050 139.3698 15.24999521 78544",
    ])
    noadpn = ["J2", "J3", "J4", "KE", "QO", "SO", "ER", "AE"]
    geophs = np.array([spice.bodvcd(399, _, 1)[1] for _ in noadpn]).ravel()
    _, elems = spice.getelm(1957, tle)
    et = spice.str2et("2020-05-26 02:25:00")
    grouped_benchmark(function, et, geophs, elems)
    res = function(et, geophs, elems)
    expected_state = np.array(
        [
            -4644.60403398,
            -5038.95025539,
            -337.27141116,
            -0.45719025,
            0.92884817,
            -7.55917355,
        ]
    )
    assert isinstance(res, np.ndarray)
    npt.assert_array_almost_equal(expected_state, res)


@pytest.mark.parametrize('function', [cyice.evsgp4_v, cyice.evsgp4], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["evsgp4_v"], indirect=True)
def test_evsgp4_v(function, grouped_benchmark, load_core_kernels):
    spice.furnsh(ExtraKernels.geophKer)
    tle = np.array([
        "1 43908U 18111AJ  20146.60805006  .00000806  00000-0  34965-4 0  9999",
        "2 43908  97.2676  47.2136 0020001 220.6050 139.3698 15.24999521 78544",
    ])
    noadpn = ["J2", "J3", "J4", "KE", "QO", "SO", "ER", "AE"]
    geophs = np.array([spice.bodvcd(399, _, 1)[1] for _ in noadpn]).ravel()
    _, elems = spice.getelm(1957, tle)
    et = spice.str2et("2020-05-26 02:25:00")
    # make vectorized versions
    ets = np.repeat(et, 100)
    elems_v = np.repeat([elems], 100, axis=0)
    grouped_benchmark(function, ets, geophs, elems_v)
    res = function(ets, geophs, elems_v)
    expected_state = np.array(
        [
            -4644.60403398,
            -5038.95025539,
            -337.27141116,
            -0.45719025,
            0.92884817,
            -7.55917355,
        ]
    )
    assert isinstance(res, np.ndarray)
    assert res.shape == (100, 6)
    npt.assert_array_almost_equal(expected_state, res[0])

# F
@pytest.mark.parametrize('function', [cyice.failed, spice.failed], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["failed"], indirect=True)
def test_failed(function, grouped_benchmark):
    spice.reset()
    grouped_benchmark(function)
    spice.reset()
    assert not function()
    spice.sigerr("test error")
    assert function()
    spice.reset()
    assert not function()


@pytest.mark.parametrize('function', [cyice.fovray_s, cyice.fovray, spice.fovray], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["fovray"], indirect=True)
def test_fovray(function, grouped_benchmark, load_cassini_kernels):
    camid = spice.bodn2c("CASSINI_ISS_NAC")
    _, frame, _, _, _ = spice.getfov(camid, 4)
    et = spice.str2et("2013 FEB 25 11:50:00 UTC")
    raydir = np.array([0.0, 0.0, 1.0], dtype=np.double)
    grouped_benchmark(function, "CASSINI_ISS_NAC", raydir, frame, "S", "CASSINI", et)
    res = function("CASSINI_ISS_NAC", raydir, frame, "S", "CASSINI", et)
    assert res
    assert isinstance(res, bool)


@pytest.mark.parametrize('function', [cyice.fovray_v, cyice.fovray], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["fovray_v"], indirect=True)
def test_fovray_v(function, grouped_benchmark, load_cassini_kernels):
    ets = np.repeat(spice.str2et("2013 FEB 25 11:50:00 UTC"), 100)
    raydir = np.array([0.0, 0.0, 1.0])
    grouped_benchmark(function, "CASSINI_ISS_NAC", raydir, "CASSINI_ISS_NAC", "S", "CASSINI", ets)
    res = function("CASSINI_ISS_NAC", raydir, "CASSINI_ISS_NAC", "S", "CASSINI", ets)
    assert isinstance(res, np.ndarray)
    assert res.dtype == np.bool


@pytest.mark.parametrize('function', [cyice.fovtrg_s, cyice.fovtrg, spice.fovtrg], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["fovtrg"], indirect=True)
def test_fovtrg(function, grouped_benchmark, load_cassini_kernels):
    et = spice.str2et("2013 FEB 25 11:50:00 UTC")
    grouped_benchmark(function, "CASSINI_ISS_NAC", "Enceladus", "Ellipsoid", "IAU_ENCELADUS", "LT+S","CASSINI", et)


@pytest.mark.parametrize('function', [cyice.fovtrg_v, cyice.fovtrg], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["fovtrg_v"], indirect=True)
def test_fovtrg_v(function, grouped_benchmark, load_cassini_kernels):
    ets = np.repeat(spice.str2et("2013 FEB 25 11:50:00 UTC"), 100)
    grouped_benchmark(function, "CASSINI_ISS_NAC","Enceladus", "Ellipsoid", "IAU_ENCELADUS", "LT+S","CASSINI", ets)
    res = function( "CASSINI_ISS_NAC","Enceladus", "Ellipsoid", "IAU_ENCELADUS", "LT+S","CASSINI", ets)
    assert isinstance(res, np.ndarray)
    assert res.dtype == np.bool


@pytest.mark.parametrize('function', [cyice.furnsh, spice.furnsh], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["furnsh"], indirect=True)
def test_furnsh(function, grouped_benchmark):
    grouped_benchmark(function, CoreKernels.testMetaKernel)


# G

@pytest.mark.parametrize('function', [cyice.georec_s, cyice.georec, spice.georec], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["georec"], indirect=True)
def test_georec(function, grouped_benchmark, load_core_kernels):
    num_vals, radii = spice.bodvrd("EARTH", "RADII", 3)
    flat = (radii[0] - radii[2]) / radii[0]
    radius = radii[0]
    lon = np.radians(118.0)
    lat = np.radians(32.0)
    alt = 0.0
    res = grouped_benchmark(function, lon, lat, alt, radius, flat)
    assert isinstance(res, np.ndarray)
    expected = np.array([-2541.74621567, 4780.329376, 3360.4312092])
    npt.assert_array_almost_equal(res, expected)


@pytest.mark.parametrize('function', [cyice.georec_v, cyice.georec], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["georec_v"], indirect=True)
def test_georec_v(function, grouped_benchmark, load_core_kernels):
    num_vals, radii = spice.bodvrd("EARTH", "RADII", 3)
    flat = (radii[0] - radii[2]) / radii[0]
    radius = radii[0]
    lon = np.repeat(np.radians(118.0), 100, axis=0) 
    lat = np.repeat(np.radians(32.0), 100, axis=0) 
    alt = np.zeros(100, order='C')
    grouped_benchmark(function, lon, lat, alt, radius, flat)
    res = function(lon, lat, alt, radius, flat)
    assert isinstance(res, np.ndarray)
    expected = np.array([[-2541.74621567, 4780.329376, 3360.4312092]])
    expected_v = np.repeat(expected, 100, axis=0)
    npt.assert_array_almost_equal(res, expected_v)


@pytest.mark.parametrize('function', [cyice.getelm_s, cyice.getelm, spice.getelm], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["getelm"], indirect=True)
def test_getelm(function, grouped_benchmark, load_core_kernels):
    tle = np.array([
        "1 44420U 19036AC  19311.70264562  .00005403  00000-0  12176-2 0  9991",
        "2 44420  24.0060  72.9267 0016343 241.6999 118.1833 14.53580129 17852",
    ])
    res = grouped_benchmark(function, 2019, tle)
    assert isinstance(res[1], np.ndarray)
    assert len(res[1]) == 10


@pytest.mark.parametrize('function', [cyice.getelm_v, cyice.getelm], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["getelm_v"], indirect=True)
def test_getelm_v(function, grouped_benchmark, load_core_kernels):
    tl1 = "1 44420U 19036AC  19311.70264562  .00005403  00000-0  12176-2 0  9991"
    tl2 = "2 44420  24.0060  72.9267 0016343 241.6999 118.1833 14.53580129 17852"
    tles = np.array([[tl1, tl2] for _ in range(100)])
    years = np.repeat(2019, 100).astype(np.int32)
    res = grouped_benchmark(function, years, tles)
    assert isinstance(res[0], np.ndarray)
    assert isinstance(res[1], np.ndarray)
    assert len(res[0]) == 100
    assert res[1].shape == (100,10)


@pytest.mark.parametrize('function', [cyice.getmsg, spice.getmsg], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["getmsg"], indirect=True)
def test_getmsg(function, grouped_benchmark):
    cyice.reset()
    spice.sigerr("test error")
    grouped_benchmark(function, "SHORT", 200)
    cyice.reset()

# H

@pytest.mark.parametrize('function', [cyice.halfpi, spice.halfpi], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["halfpi"], indirect=True)
def test_halfpi(function, grouped_benchmark):
    grouped_benchmark(function)
    assert function() == np.pi / 2

# I

@pytest.mark.parametrize('function', [cyice.illumf_s, cyice.illumf, spice.illumf], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["illumf"], indirect=True)
def test_illumf(function, grouped_benchmark, load_core_kernels, load_cassini_kernels):
    et = spice.str2et("2013 FEB 25 11:50:00 UTC")
    camid = spice.bodn2c("CASSINI_ISS_NAC")
    shape, obsref, bsight, n, bounds = spice.getfov(camid, 4)
    spoint, etemit, srfvec = spice.sincpt(
        "Ellipsoid", "Enceladus", et, "IAU_ENCELADUS", "CN+S", "CASSINI", obsref, bsight
    )
    grouped_benchmark(function, "Ellipsoid", "Enceladus", "Sun", et, "IAU_ENCELADUS", "CN+S", "CASSINI", spoint)
    trgepc2, srfvec2, phase, incid, emissn, visibl, lit = function("Ellipsoid", "Enceladus", "Sun", et, "IAU_ENCELADUS", "CN+S", "CASSINI", spoint)
    assert np.degrees(phase) == pytest.approx(161.82854377660345)
    assert np.degrees(incid) == pytest.approx(134.92108561449996)
    assert np.degrees(emissn) == pytest.approx(63.23618556218115)
    assert isinstance(srfvec2, np.ndarray)
    assert not lit
    assert visibl


@pytest.mark.parametrize('function', [cyice.illumf_v, cyice.illumf], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["illumf_v"], indirect=True)
def test_illumf_v(function, grouped_benchmark, load_core_kernels, load_cassini_kernels):
    et = spice.str2et("2013 FEB 25 11:50:00 UTC")
    camid = spice.bodn2c("CASSINI_ISS_NAC")
    shape, obsref, bsight, n, bounds = spice.getfov(camid, 4)
    spoint, etemit, srfvec = spice.sincpt(
        "Ellipsoid", "Enceladus", et, "IAU_ENCELADUS", "CN+S", "CASSINI", obsref, bsight
    )
    ets = np.repeat(et, 100)
    spoints = np.repeat([spoint], 100, axis=0)
    grouped_benchmark(function, "Ellipsoid", "Enceladus", "Sun", ets, "IAU_ENCELADUS", "CN+S", "CASSINI", spoints)
    trgepc2, srfvec2, phase, incid, emissn, visibl, lit = function("Ellipsoid", "Enceladus", "Sun", ets, "IAU_ENCELADUS", "CN+S", "CASSINI", spoints)
    assert isinstance(trgepc2, np.ndarray)
    assert isinstance(phase, np.ndarray)
    assert isinstance(incid, np.ndarray)
    assert isinstance(emissn, np.ndarray)
    assert isinstance(srfvec2, np.ndarray)
    assert isinstance(visibl, np.ndarray)
    assert isinstance(lit, np.ndarray)
    assert trgepc2.shape == (100, 100)
    assert phase.shape   == (100, 100)
    assert incid.shape   == (100, 100)
    assert emissn.shape  == (100, 100)
    assert visibl.shape  == (100, 100)
    assert lit.shape  == (100, 100)    
    assert srfvec2.shape == (100, 100, 3)
    assert np.degrees(phase[0,0]) == pytest.approx(161.82854377660345)
    assert np.degrees(incid[0,0]) == pytest.approx(134.92108561449996)
    assert np.degrees(emissn[0,0]) == pytest.approx(63.23618556218115)
    assert np.all(visibl)
    assert not np.any(lit)


@pytest.mark.parametrize('function', [cyice.illumg_s, cyice.illumg, spice.illumg], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["illumg"], indirect=True)
def test_illumg(function, grouped_benchmark, load_core_kernels, load_cassini_kernels):
    et = spice.str2et("2013 FEB 25 11:50:00 UTC")
    spoint, trgepc, srfvec = spice.subpnt(
        "Near Point/Ellipsoid", "Enceladus", et, "IAU_ENCELADUS", "CN+S", "Earth"
    )
    grouped_benchmark(function, "Ellipsoid", "Enceladus", "Sun", et, "IAU_ENCELADUS", "CN+S", "CASSINI", spoint)
    trgepc2, srfvec2, phase, incid, emissn = function("Ellipsoid", "Enceladus", "Sun", et, "IAU_ENCELADUS", "CN+S", "CASSINI", spoint)
    assert np.degrees(phase) == pytest.approx(161.859925246638)
    assert np.degrees(incid) == pytest.approx(18.47670084384343)
    assert np.degrees(emissn) == pytest.approx(143.6546170649875)
    assert isinstance(srfvec2, np.ndarray)


@pytest.mark.parametrize('function', [cyice.illumg_v, cyice.illumg], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["illumg_v"], indirect=True)
def test_illumg_v(function, grouped_benchmark, load_core_kernels, load_cassini_kernels):
    et = spice.str2et("2013 FEB 25 11:50:00 UTC")
    spoint, trgepc, srfvec = spice.subpnt(
        "Near Point/Ellipsoid", "Enceladus", et, "IAU_ENCELADUS", "CN+S", "Earth"
    )
    ets = np.repeat(et, 100)
    spoints = np.repeat([spoint], 100, axis=0)
    grouped_benchmark(function, "Ellipsoid", "Enceladus", "Sun", ets, "IAU_ENCELADUS", "CN+S", "CASSINI", spoints)
    trgepc2, srfvec2, phase, incid, emissn = function("Ellipsoid", "Enceladus", "Sun", ets, "IAU_ENCELADUS", "CN+S", "CASSINI", spoints)
    assert isinstance(trgepc2, np.ndarray)
    assert isinstance(phase, np.ndarray)
    assert isinstance(incid, np.ndarray)
    assert isinstance(emissn, np.ndarray)
    assert isinstance(srfvec2, np.ndarray)
    assert trgepc2.shape == (100, 100)
    assert phase.shape   == (100, 100)
    assert incid.shape   == (100, 100)
    assert emissn.shape  == (100, 100)
    assert srfvec2.shape == (100, 100, 3)
    assert np.degrees(phase[0,0]) == pytest.approx(161.859925246638)
    assert np.degrees(incid[0,0]) == pytest.approx(18.47670084384343)
    assert np.degrees(emissn[0,0]) == pytest.approx(143.6546170649875)


@pytest.mark.parametrize('function', [cyice.ilumin_s, cyice.ilumin, spice.ilumin], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["ilumin"], indirect=True)
def test_ilumin(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("2007 FEB 3 00:00:00.000")
    trgepc, obspos, trmpts = spice.edterm(
        "UMBRAL", "SUN", "MOON", et, "IAU_MOON", "LT+S", "EARTH", 3
    )
    grouped_benchmark(function, "Ellipsoid", "MOON", et, "IAU_MOON", "LT+S", "EARTH", trmpts[0])
    iluet0, srfvec0, phase0, solar0, emissn0 = function("Ellipsoid", "MOON", et, "IAU_MOON", "LT+S", "EARTH", trmpts[0])
    npt.assert_almost_equal(np.degrees(solar0), 90.269765819)
    

@pytest.mark.parametrize('function', [cyice.ilumin_v, cyice.ilumin], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["ilumin_v"], indirect=True)
def test_ilumin_v(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("2007 FEB 3 00:00:00.000")
    ets = np.repeat(et, 100)
    trgepc, obspos, trmpts = spice.edterm(
        "UMBRAL", "SUN", "MOON", et, "IAU_MOON", "LT+S", "EARTH", 100
    )
    grouped_benchmark(function, "Ellipsoid", "MOON", ets, "IAU_MOON", "LT+S", "EARTH", trmpts)
    iluet0, srfvec0, phase0, solar0, emissn0 = function("Ellipsoid", "MOON", ets, "IAU_MOON", "LT+S", "EARTH", trmpts)
    assert isinstance(iluet0, np.ndarray)
    assert isinstance(srfvec0, np.ndarray)
    assert isinstance(phase0, np.ndarray)
    assert isinstance(solar0, np.ndarray)
    assert isinstance(emissn0, np.ndarray)
    assert phase0.shape  == (100, 100)
    assert solar0.shape  == (100, 100)
    assert emissn0.shape == (100, 100)
    assert srfvec0.shape == (100, 100, 3)
    npt.assert_almost_equal(np.degrees(solar0[0,0]), 90.269765819)



# J

@pytest.mark.parametrize('function', [cyice.j1900, spice.j1900], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["j1900"], indirect=True)
def test_j1900(function, grouped_benchmark):
    grouped_benchmark(function)
    assert function() == 2415020.0


@pytest.mark.parametrize('function', [cyice.j1950, spice.j1950], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["j1950"], indirect=True)
def test_j1950(function, grouped_benchmark):
    grouped_benchmark(function)
    assert function() == 2433282.5


@pytest.mark.parametrize('function', [cyice.j2000, spice.j2000], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["j2000"], indirect=True)
def test_j2000(function, grouped_benchmark):
    grouped_benchmark(function)
    assert function() == 2451545.0


@pytest.mark.parametrize('function', [cyice.j2100, spice.j2100], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["j2100"], indirect=True)
def test_j2100(function, grouped_benchmark):
    grouped_benchmark(function)
    assert function() == 2488070.0


@pytest.mark.parametrize('function', [cyice.jyear, spice.jyear], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["jyear"], indirect=True)
def test_jyear(function, grouped_benchmark):
    grouped_benchmark(function)
    assert function() == 31557600.0

# K

# L

@pytest.mark.parametrize('function', [cyice.latcyl_s, cyice.latcyl, spice.latcyl], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["latcyl"], indirect=True)
def test_latcyl(function, grouped_benchmark):
    r   = 1.0
    lon = 90.0 * spice.rpd()
    lat = 0.0
    res = grouped_benchmark(function, r, lon, lat)
    expected = np.array([r, lon, lat])
    npt.assert_array_almost_equal(res, expected, decimal=7)


@pytest.mark.parametrize('function', [cyice.latcyl_v, cyice.latcyl], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["latcyl_v"], indirect=True)
def test_latcyl_v(function, grouped_benchmark):
    r   = np.ones(100, order='C')
    lon = np.repeat(90.0, 100) * spice.rpd()
    lat = np.zeros(100, order='C')
    res = grouped_benchmark(function, r, lon, lat)
    expected = np.vstack([r, lon, lat]).T
    npt.assert_array_almost_equal(res, expected, decimal=7)


@pytest.mark.parametrize('function', [cyice.latrec_s, cyice.latrec, spice.latrec], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["latrec"], indirect=True)
def test_latrec(function, grouped_benchmark):
    r   = 1.0
    lon = 90.0 * spice.rpd()
    lat = 0.0
    res = grouped_benchmark(function, r, lon, lat)
    assert isinstance(res, np.ndarray)
    expected = np.array([0.0, 1.0, 0.0])
    npt.assert_array_almost_equal(res, expected, decimal=7)


@pytest.mark.parametrize('function', [cyice.latrec_v, cyice.latrec], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["latrec_v"], indirect=True)
def test_latrec_v(function, grouped_benchmark):
    r   = np.ones(100, order='C')
    lon = np.repeat(90.0, 100) * spice.rpd()
    lat = np.zeros(100, order='C')
    res = grouped_benchmark(function, r, lon, lat)
    assert isinstance(res, np.ndarray)
    expected = np.repeat([[0.0, 1.0, 0.0]], 100, axis=0)
    npt.assert_array_almost_equal(res, expected, decimal=7)


@pytest.mark.parametrize('function', [cyice.latsph_s, cyice.latsph, spice.latsph], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["latsph"], indirect=True)
def test_latsph(function, grouped_benchmark):
    r   = 1.0
    lon = 90.0 * spice.rpd()
    lat = 0.0
    res = grouped_benchmark(function, r, lon, lat)
    expected = np.array([r, 90.0 * spice.rpd(), 90.0 * spice.rpd()])
    npt.assert_array_almost_equal(res, expected, decimal=7)


@pytest.mark.parametrize('function', [cyice.limbpt_s, cyice.limbpt, spice.limbpt], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["limbpt"], indirect=True)
def test_limbpt(function, grouped_benchmark, load_core_kernels):
    spice.furnsh(ExtraKernels.marsSpk)
    spice.furnsh(ExtraKernels.phobosDsk)
    et = spice.str2et("1972 AUG 11 00:00:00")
    args = (
        "TANGENT/DSK/UNPRIORITIZED",
        "Phobos",
        et,
        "IAU_PHOBOS",
        "CN+S",
        "CENTER",
        "MARS",
        np.array([0.0, 0.0, 1.0]),
        spice.twopi() / 3.0,
        3,
        1.0e-4,
        1.0e-7,
        3,
    )
    npts, points, epochs, tangts = grouped_benchmark(function, *args)
    assert npts.sum() == 3
    assert len(points) == 3


@pytest.mark.parametrize('function', [cyice.limbpt_v, cyice.limbpt], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["limbpt_v"], indirect=True)
def test_limbpt_v(function, grouped_benchmark, load_core_kernels):
    spice.furnsh(ExtraKernels.marsSpk)
    spice.furnsh(ExtraKernels.phobosDsk)
    et = spice.str2et("1972 AUG 11 00:00:00")
    ets = np.linspace(et, et+1, 100)
    args = (
        "TANGENT/DSK/UNPRIORITIZED",
        "Phobos",
        ets,
        "IAU_PHOBOS",
        "CN+S",
        "CENTER",
        "MARS",
        np.array([0.0, 0.0, 1.0]),
        spice.twopi() / 3.0,
        3,
        1.0e-4,
        1.0e-7,
        3,
    )
    npts, points, epochs, tangts = grouped_benchmark(function, *args)
    assert npts.shape == (100,3)
    assert points.shape == (100, 3, 3)


@pytest.mark.parametrize('function', [cyice.lspcn_s, cyice.lspcn, spice.lspcn], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["lspcn"], indirect=True)
def test_lspcn(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("21 march 2005")
    grouped_benchmark(function, "EARTH", et, "NONE")


@pytest.mark.parametrize('function', [cyice.lspcn_v, cyice.lspcn], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["lspcn_v"], indirect=True)
def test_lspcn_v(function, grouped_benchmark, load_core_kernels):
    ets = np.repeat(spice.str2et("21 march 2005"),100)
    grouped_benchmark(function, "EARTH", ets, "NONE")
    res = function("EARTH", ets, "NONE")
    assert isinstance(res, np.ndarray)

# M

# N

# O

@pytest.mark.parametrize('function', [cyice.occult_s, cyice.occult, spice.occult], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["occult"], indirect=True)
def test_occult(function, grouped_benchmark, load_core_kernels, load_earth_kernels):
    # Mercury is in front of the Sun as seen by observer (DSS-13) ()
    et = spice.str2et("2006-11-08T22:00")
    grouped_benchmark(
        function,
        "MERCURY",
        "point",
        " ",
        "SUN",
        "ellipsoid",
        "IAU_SUN",
        "CN",
        "DSS-13",
        et
    )
    res = function(
        "MERCURY",
        "point",
        " ",
        "SUN",
        "ellipsoid",
        "IAU_SUN",
        "CN",
        "DSS-13",
        et
    )
    assert res == 2
    assert isinstance(res, int)


@pytest.mark.parametrize('function', [cyice.occult_v, cyice.occult], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["occult_v"], indirect=True)
def test_occult_v(function, grouped_benchmark, load_core_kernels, load_earth_kernels):
    # Mercury is in front of the Sun as seen by observer (DSS-13) ()
    et = spice.str2et("2006-11-08T22:00")
    ets = np.repeat(et, 100)
    grouped_benchmark(
        function,
        "MERCURY",
        "point",
        " ",
        "SUN",
        "ellipsoid",
        "IAU_SUN",
        "CN",
        "DSS-13",
        ets
    )
    res = function(
        "MERCURY",
        "point",
        " ",
        "SUN",
        "ellipsoid",
        "IAU_SUN",
        "CN",
        "DSS-13",
        ets
    )
    expected = np.repeat(2, 100)
    npt.assert_array_equal(res, expected)
    assert isinstance(res, np.ndarray)


@pytest.mark.parametrize('function', [cyice.oscelt_s, cyice.oscelt, spice.oscelt], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["oscelt"], indirect=True)
def test_oscelt(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("Dec 25, 2007")
    state, _ = spice.spkezr("Moon", et, "J2000", "LT+S", "EARTH")
    _, mass_earth = spice.bodvrd("EARTH", "GM", 1)
    mu = mass_earth[0]
    res = grouped_benchmark(function, state, et, mu)
    expected = np.array([
            3.60975119168868346605e+05,
            7.81035176779166367966e-02,
            4.87177926278510309288e-01,
            6.18584206992959551030e+00,
            1.28678805411666807856e+00,
            5.53312778515375192079e-01,
            2.51812865183709204197e+08,
            3.98600435436095925979e+05
    ])
    assert isinstance(res, np.ndarray)
    npt.assert_array_almost_equal(res, expected)


@pytest.mark.parametrize('function', [cyice.oscelt_v, cyice.oscelt], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["oscelt_v"], indirect=True)
def test_oscelt_v(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("Dec 25, 2007")
    state, _ = spice.spkezr("Moon", et, "J2000", "LT+S", "EARTH")
    _, mass_earth = spice.bodvrd("EARTH", "GM", 1)
    mu = mass_earth[0]
    state_v = np.repeat([state],100, axis=0)
    et_v = np.repeat(et, 100)
    res = grouped_benchmark(function, state_v, et_v, mu)
    expected = np.array([[
            3.60975119168868346605e+05,
            7.81035176779166367966e-02,
            4.87177926278510309288e-01,
            6.18584206992959551030e+00,
            1.28678805411666807856e+00,
            5.53312778515375192079e-01,
            2.51812865183709204197e+08,
            3.98600435436095925979e+05
    ]])
    expected_v = np.repeat(expected, 100, axis=0)
    assert isinstance(res, np.ndarray)
    npt.assert_array_almost_equal(res, expected_v)


# P

@pytest.mark.parametrize('function', [cyice.pgrrec_s, cyice.pgrrec, spice.pgrrec], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["pgrrec"], indirect=True)
def test_pgrrec(function, grouped_benchmark, load_core_kernels):
    num_vals, radii = spice.bodvrd("MARS", "RADII", 3)
    flat = (radii[0] - radii[2]) / radii[0]
    radius = radii[0]
    res = grouped_benchmark(function, "MARS", np.radians(90), np.radians(45), 300.0, radius, flat)
    expected = np.array([1.604650025e-13, -2.620678915e3, 2.592408909e3])
    assert isinstance(res, np.ndarray)
    npt.assert_array_almost_equal(res, expected)


@pytest.mark.parametrize('function', [cyice.pgrrec_v, cyice.pgrrec], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["pgrrec_v"], indirect=True)
def test_pgrrec_v(function, grouped_benchmark, load_core_kernels):
    num_vals, radii = spice.bodvrd("MARS", "RADII", 3)
    flat = (radii[0] - radii[2]) / radii[0]
    radius = radii[0]
    lon = np.repeat(np.radians(90), 100)
    lat = np.repeat(np.radians(45), 100)
    alt = np.repeat(300.0, 100)
    res = grouped_benchmark(function, "MARS", lon, lat, alt, radius, flat)
    assert isinstance(res, np.ndarray)
    expected = np.array([[1.604650025e-13, -2.620678915e3, 2.592408909e3]])
    expected_v = np.repeat(expected, 100, axis=0)
    npt.assert_array_almost_equal(res, expected_v)


@pytest.mark.parametrize('function', [cyice.phaseq_s, cyice.phaseq, spice.phaseq], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["phaseq"], indirect=True)
def test_phaseq(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et('2006 DEC 02 13:31:34.414')
    res = grouped_benchmark(function, et, "moon", "sun", "earth", "lt+s")
    expected = 0.575988450
    npt.assert_almost_equal(res, expected)


@pytest.mark.parametrize('function', [cyice.phaseq_v, cyice.phaseq], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["phaseq_v"], indirect=True)
def test_phaseq_v(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et('2006 DEC 02 13:31:34.414')
    ets = np.repeat(et, 100)
    res = grouped_benchmark(function, ets, "moon", "sun", "earth", "lt+s")
    assert isinstance(res, np.ndarray)
    expected = np.repeat(0.575988450, 100)
    npt.assert_array_almost_equal(res, expected)


@pytest.mark.parametrize('function', [cyice.pi, spice.pi], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["pi"], indirect=True)
def test_pi(function, grouped_benchmark):
    grouped_benchmark(function)
    assert function() == np.pi


@pytest.mark.parametrize('function', [cyice.pxform_s, cyice.pxform, spice.pxform], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["pxform"], indirect=True)
def test_pxform(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("January 1, 2005")
    grouped_benchmark(function, "IAU_EARTH", "J2000", et)
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
    rotate = function("IAU_EARTH", "J2000", et)
    assert isinstance(rotate, np.ndarray)
    jstate = np.dot(epos, rotate)
    expected = np.array(
        [
            5042.1309421, 
            1603.52962986, 
            3549.82398086
        ]
    )
    npt.assert_array_almost_equal(jstate, expected, decimal=4)


@pytest.mark.parametrize('function', [cyice.pxform_v, cyice.pxform], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["pxform_v"], indirect=True)
def test_pxform_v(function, grouped_benchmark, load_core_kernels):
    et = np.repeat(spice.str2et("January 1, 2005"), 1000)
    grouped_benchmark(function, "IAU_EARTH", "J2000", et)
    res = function("IAU_EARTH", "J2000", et)
    assert isinstance(res, np.ndarray)

# Q
@pytest.mark.parametrize('function', [cyice.qcktrc, spice.qcktrc], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["qcktrc"], indirect=True)
def test_qcktrc(function, grouped_benchmark):
    cyice.reset()
    spice.chkin("test")
    spice.chkin("qcktrc")
    grouped_benchmark(function, 40)
    trace = function(40)
    assert trace == "test --> qcktrc"
    spice.chkout("qcktrc")
    spice.chkout("test")
    cyice.reset()

# R
@pytest.mark.parametrize('function', [cyice.radrec_s, cyice.radrec, spice.radrec], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["radrec"], indirect=True)
def test_radrec(function, grouped_benchmark):
    res = grouped_benchmark(function, 1.0, np.radians(90.0), 0.0)
    assert isinstance(res, np.ndarray)
    expected = np.array([0.0, 1.0, 0.0])
    npt.assert_array_almost_equal(res, expected)


@pytest.mark.parametrize('function', [cyice.radrec_v, cyice.radrec], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["radrec_v"], indirect=True)
def test_radrec_v(function, grouped_benchmark):
    inrange = np.ones(100, order='C')
    ra      = np.repeat(np.radians(90.0), 100)
    dec     = np.zeros(100, order='C')
    res = grouped_benchmark(function, inrange, ra, dec)
    assert isinstance(res, np.ndarray)
    expected = np.array([[0.0, 1.0, 0.0]])
    expected_v = np.repeat(expected, 100, axis=0)
    npt.assert_array_almost_equal(res, expected_v)


@pytest.mark.parametrize('function', [cyice.recazl_s, cyice.recazl, spice.recazl], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["recazl"], indirect=True)
def test_recazl(function, grouped_benchmark):
    rectan = np.array([0.0, 1.0, 0.0])
    res = grouped_benchmark(function, rectan, True, True)
    expected = np.array([1.0, np.radians(90.0), 0.0])
    npt.assert_array_almost_equal(res, expected)


@pytest.mark.parametrize('function', [cyice.recazl_v, cyice.recazl], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["recazl_v"], indirect=True)
def test_recazl_v(function, grouped_benchmark):
    rectan = np.array([[0.0, 1.0, 0.0]])
    rectan_v = np.repeat(rectan, 100, axis=0)
    res = grouped_benchmark(function, rectan_v, True, True)
    assert isinstance(res, np.ndarray)
    expected = np.array([[1.0, np.radians(90.0), 0.0]])
    expected_v = np.repeat(expected, 100, axis=0)
    npt.assert_array_almost_equal(res, expected_v)


@pytest.mark.parametrize('function', [cyice.reccyl_s, cyice.reccyl, spice.reccyl], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["reccyl"], indirect=True)
def test_reccyl(function, grouped_benchmark):
    rectan = np.array([0.0, 1.0, 0.0])
    res = grouped_benchmark(function, rectan)
    expected = np.array([1.0, np.radians(90.0), 0.0])
    npt.assert_array_almost_equal(res, expected)


@pytest.mark.parametrize('function', [cyice.reccyl_v, cyice.reccyl], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["reccyl_v"], indirect=True)
def test_reccyl_v(function, grouped_benchmark):
    rectan = np.array([[0.0, 1.0, 0.0]])
    rectan_v = np.repeat(rectan, 100, axis=0)
    res = grouped_benchmark(function, rectan_v)
    assert isinstance(res, np.ndarray)
    expected = np.array([[1.0, np.radians(90.0), 0.0]])
    expected_v = np.repeat(expected, 100, axis=0)
    npt.assert_array_almost_equal(res, expected_v)


@pytest.mark.parametrize('function', [cyice.recgeo_s, cyice.recgeo, spice.recgeo], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["recgeo"], indirect=True)
def test_recgeo(function, grouped_benchmark, load_core_kernels):
    num_vals, radii = spice.bodvrd("EARTH", "RADII", 3)
    flat = (radii[0] - radii[2]) / radii[0]
    radius = radii[0]
    rectan = np.array([-2541.748162, 4780.333036, 3360.428190])
    res = grouped_benchmark(function, rectan, radius, flat)
    expected = np.array([np.radians(118.0), np.radians(32.0), 0.001915518])
    npt.assert_array_almost_equal(res, expected)


@pytest.mark.parametrize('function', [cyice.recgeo_v, cyice.recgeo], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["recgeo_v"], indirect=True)
def test_recgeo_v(function, grouped_benchmark, load_core_kernels):
    num_vals, radii = spice.bodvrd("EARTH", "RADII", 3)
    flat = (radii[0] - radii[2]) / radii[0]
    radius = radii[0]
    rectan = np.array([[-2541.748162, 4780.333036, 3360.428190]])
    rectan_v = np.repeat(rectan, 100, axis=0)
    res = grouped_benchmark(function, rectan_v, radius, flat)
    assert isinstance(res, np.ndarray)
    expected = np.array([[np.radians(118.0), np.radians(32.0), 0.001915518]])
    expected_v = np.repeat(expected, 100, axis=0)
    npt.assert_array_almost_equal(res, expected_v)


@pytest.mark.parametrize('function', [cyice.reclat_s, cyice.reclat, spice.reclat], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["reclat"], indirect=True)
def test_reclat(function, grouped_benchmark):
    rectan = np.array([0.0, 1.0, 0.0])
    res = grouped_benchmark(function, rectan)
    expected = np.array([1.0, np.radians(90.0), 0.0])
    npt.assert_array_almost_equal(res, expected)


@pytest.mark.parametrize('function', [cyice.reclat_v, cyice.reclat], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["reclat_v"], indirect=True)
def test_reclat_v(function, grouped_benchmark):
    rectan = np.array([[0.0, 1.0, 0.0]])
    rectan_v = np.repeat(rectan, 100, axis=0)
    res = grouped_benchmark(function, rectan_v)
    assert isinstance(res, np.ndarray)
    expected = np.array([[1.0, np.radians(90.0), 0.0]])
    expected_v = np.repeat(expected, 100, axis=0)
    npt.assert_array_almost_equal(res, expected_v)


@pytest.mark.parametrize('function', [cyice.recpgr_s, cyice.recpgr, spice.recpgr], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["recpgr"], indirect=True)
def test_recpgr(function, grouped_benchmark, load_core_kernels):
    num_vals, radii = spice.bodvrd("MARS", "RADII", 3)
    flat = (radii[0] - radii[2]) / radii[0]
    radius = radii[0]
    rectan = np.array([0.0, -2620.678914818178, 2592.408908856967])
    res = grouped_benchmark(function, "MARS", rectan, radius, flat)
    expected = np.array([np.radians(90.0), np.radians(45.0), 300.0])
    npt.assert_array_almost_equal(res, expected)


@pytest.mark.parametrize('function', [cyice.recpgr_v, cyice.recpgr], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["recpgr_v"], indirect=True)
def test_recpgr_v(function, grouped_benchmark, load_core_kernels):
    num_vals, radii = spice.bodvrd("MARS", "RADII", 3)
    flat = (radii[0] - radii[2]) / radii[0]
    radius = radii[0]
    rectan = np.array([[0.0, -2620.678914818178, 2592.408908856967]])
    rectan_v = np.repeat(rectan, 100, axis=0)
    res = grouped_benchmark(function, "MARS", rectan_v, radius, flat)
    assert isinstance(res, np.ndarray)
    expected = np.array([[np.radians(90.0), np.radians(45.0), 300.0]])
    expected_v = np.repeat(expected, 100, axis=0)
    npt.assert_array_almost_equal(res, expected_v)


@pytest.mark.parametrize('function', [cyice.recrad_s, cyice.recrad, spice.recrad], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["recrad"], indirect=True)
def test_recrad(function, grouped_benchmark):
    rectan = np.array([0.0, 1.0, 0.0])
    res = grouped_benchmark(function, rectan)
    expected = np.array([1.0, np.radians(90.0), 0.0])
    npt.assert_array_almost_equal(res, expected)


@pytest.mark.parametrize('function', [cyice.recrad_v, cyice.recrad], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["recrad_v"], indirect=True)
def test_recrad_v(function, grouped_benchmark):
    rectan = np.array([[0.0, 1.0, 0.0]])
    rectan_v = np.repeat(rectan, 100, axis=0)
    res = grouped_benchmark(function, rectan_v)
    assert isinstance(res, np.ndarray)
    expected = np.array([[1.0, np.radians(90.0), 0.0]])
    expected_v = np.repeat(expected, 100, axis=0)
    npt.assert_array_almost_equal(res, expected_v)


@pytest.mark.parametrize('function', [cyice.recsph_s, cyice.recsph, spice.recsph], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["recsph"], indirect=True)
def test_recsph(function, grouped_benchmark):
    rectan = np.array([-1.0, 0.0, 0.0])
    res = grouped_benchmark(function, rectan)
    expected = np.array([1.0, np.pi / 2, np.pi])
    npt.assert_array_almost_equal(res, expected)


@pytest.mark.parametrize('function', [cyice.recsph_v, cyice.recsph], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["recsph_v"], indirect=True)
def test_recsph_v(function, grouped_benchmark):
    rectan = np.array([[-1.0, 0.0, 0.0]])
    rectan_v = np.repeat(rectan, 100, axis=0)
    res = grouped_benchmark(function, rectan_v)
    assert isinstance(res, np.ndarray)
    expected = np.array([[1.0, np.pi / 2, np.pi]])
    expected_v = np.repeat(expected, 100, axis=0)
    npt.assert_array_almost_equal(res, expected_v)


@pytest.mark.parametrize('function', [cyice.reset, spice.reset], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["reset"], indirect=True)
def test_reset(function, grouped_benchmark):
   grouped_benchmark(function)


@pytest.mark.parametrize('function', [cyice.rpd, spice.rpd], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["rpd"], indirect=True)
def test_rpd(function, grouped_benchmark):
    grouped_benchmark(function)
    assert function() == np.arccos(-1.0) / 180.0

# S
@pytest.mark.parametrize('function', [cyice.scdecd_s, cyice.scdecd, spice.scdecd], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["scdecd"], indirect=True)
def test_scdecd(function, grouped_benchmark, load_voyager_kernels):
    timein = spice.scencd(-32, "2/20538:39:768")
    grouped_benchmark(function, -32, timein)


@pytest.mark.parametrize('function', [cyice.scdecd_v, cyice.scdecd], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["scdecd_v"], indirect=True)
def test_scdecd_v(function, grouped_benchmark, load_voyager_kernels):
    timein = np.repeat(spice.scencd(-32, "2/20538:39:768"), 100)
    grouped_benchmark(function, -32, timein)
    res = function(-32, timein)
    assert isinstance(res, np.ndarray)


@pytest.mark.parametrize('function', [cyice.scencd_s, cyice.scencd, spice.scencd], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["scencd"], indirect=True)
def test_scencd(function, grouped_benchmark, load_voyager_kernels):
    grouped_benchmark(function, -32,  "2/20538:39:768")


@pytest.mark.parametrize('function', [cyice.scencd_v, cyice.scencd], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["scencd_v"], indirect=True)
def test_scencd_v(function, grouped_benchmark, load_voyager_kernels):
    timein = np.repeat("2/20538:39:768", 100)
    grouped_benchmark(function, -32,  timein)
    res = function(-32, timein)
    assert isinstance(res, np.ndarray)


@pytest.mark.parametrize('function', [cyice.sce2c_s, cyice.sce2c, spice.sce2c], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sce2c"], indirect=True)
def test_sce2c(function, grouped_benchmark, load_voyager_kernels):
    et = spice.str2et("1979 JUL 05 21:50:21.23379")
    grouped_benchmark(function, -32, et)


@pytest.mark.parametrize('function', [cyice.sce2c_v, cyice.sce2c], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sce2c_v"], indirect=True)
def test_sce2c_v(function, grouped_benchmark, load_voyager_kernels):
    ets = np.repeat(spice.str2et("1979 JUL 05 21:50:21.23379"), 100)
    grouped_benchmark(function, -32, ets)
    res = function(-32, ets)
    assert isinstance(res, np.ndarray)


@pytest.mark.parametrize('function', [cyice.sce2s_s, cyice.sce2s, spice.sce2s], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sce2s"], indirect=True)
def test_sce2s(function, grouped_benchmark):
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.voyagerSclk)
    et = spice.str2et("1979 JUL 05 21:50:21.23379")
    grouped_benchmark(function, -32, et)


@pytest.mark.parametrize('function', [cyice.sce2s_v, cyice.sce2s], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sce2s_v"], indirect=True)
def test_sce2s_v(function, grouped_benchmark):
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.voyagerSclk)
    ets = np.repeat(spice.str2et("1979 JUL 05 21:50:21.23379"), 100)
    grouped_benchmark(function, -32, ets)
    res = function(-32, ets)
    assert isinstance(res, np.ndarray)


@pytest.mark.parametrize('function', [cyice.scs2e_s, cyice.scs2e, spice.scs2e], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["scs2e"], indirect=True)
def test_scs2e(function, grouped_benchmark, load_voyager_kernels):
    grouped_benchmark(function, -32, "2/20538:39:768")


@pytest.mark.parametrize('function', [cyice.scs2e_v, cyice.scs2e], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["scs2e_v"], indirect=True)
def test_scs2e_v(function, grouped_benchmark, load_voyager_kernels):
    timein = np.repeat("2/20538:39:768", 100)
    grouped_benchmark(function, -32, timein)
    res = function(-32, timein)
    assert isinstance(res, np.ndarray)


@pytest.mark.parametrize('function', [cyice.sct2e_s, cyice.sct2e, spice.sct2e], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sct2e"], indirect=True)
def test_sct2e(function, grouped_benchmark, load_voyager_kernels):
    grouped_benchmark(function, -32,  985327965.0)


@pytest.mark.parametrize('function', [cyice.sct2e_v, cyice.sct2e], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sct2e_v"], indirect=True)
def test_sct2e_v(function, grouped_benchmark, load_voyager_kernels):
    sclkdps = np.repeat(985327965.0, 100)
    grouped_benchmark(function, -32, sclkdps)
    res = function(-32, sclkdps)
    assert isinstance(res, np.ndarray)


@pytest.mark.parametrize('function', [cyice.spd, spice.spd], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spd"], indirect=True)
def test_spd(function, grouped_benchmark):
    grouped_benchmark(function)
    assert function() == 86400.0


@pytest.mark.parametrize('function', [cyice.sphcyl_s, cyice.sphcyl, spice.sphcyl], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sphcyl"], indirect=True)
def test_sphcyl(function, grouped_benchmark):
    res = grouped_benchmark(function, 1.4142, np.deg2rad(180.0), np.deg2rad(45.0))
    expected = np.array([0.0, np.deg2rad(45.0), -np.sqrt(2)])
    npt.assert_array_almost_equal(res, expected, decimal=4)


@pytest.mark.parametrize('function', [cyice.sphcyl_v, cyice.sphcyl], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sphcyl_v"], indirect=True)
def test_sphcyl_v(function, grouped_benchmark):
    radius = np.repeat(1.4142, 100)
    colat  = np.repeat(np.deg2rad(180.0), 100)
    slon   = np.repeat(np.deg2rad(45.0), 100)
    res = grouped_benchmark(function, radius, colat, slon)
    assert isinstance(res, np.ndarray)
    expected = np.array([[0.0, np.deg2rad(45.0), -np.sqrt(2)]])
    expected_v = np.repeat(expected, 100, axis=0)
    npt.assert_array_almost_equal(res, expected_v, decimal=4)


@pytest.mark.parametrize('function', [cyice.sphlat_s, cyice.sphlat, spice.sphlat], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sphlat"], indirect=True)
def test_sphlat(function, grouped_benchmark):
    res = grouped_benchmark(function, 1.0, spice.pi(), spice.halfpi())
    expected = np.array([1.0, spice.halfpi(), -spice.halfpi()])
    npt.assert_array_almost_equal(res, expected, decimal=7)


@pytest.mark.parametrize('function', [cyice.sphlat_v, cyice.sphlat], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sphlat_v"], indirect=True)
def test_sphlat_v(function, grouped_benchmark):
    r   = np.ones(100, order='C')
    colat = np.repeat(spice.pi(), 100) 
    slon = np.repeat(spice.halfpi(), 100)
    res = grouped_benchmark(function, r, colat, slon)
    assert isinstance(res, np.ndarray)
    expected = np.array([[1.0, spice.halfpi(), -spice.halfpi()]])
    expected_v = np.repeat(expected, 100, axis=0)
    npt.assert_array_almost_equal(res, expected_v, decimal=7)


@pytest.mark.parametrize('function', [cyice.sphrec_s, cyice.sphrec, spice.sphrec], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sphrec"], indirect=True)
def test_sphrec(function, grouped_benchmark):
    res = grouped_benchmark(function, 1.0, np.radians(90.0), 0.0)
    expected = np.array([1.0, 0.0, 0.0])
    assert isinstance(res, np.ndarray)
    npt.assert_array_almost_equal(res, expected, decimal=7)


@pytest.mark.parametrize('function', [cyice.sphrec_v, cyice.sphrec], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sphrec_v"], indirect=True)
def test_sphrec_v(function, grouped_benchmark):
    r     = np.ones(100, order='C')
    colat = np.repeat(np.radians(90.0), 100)
    slon  = np.zeros(100, order='C')
    res = grouped_benchmark(function, r, colat, slon)
    assert isinstance(res, np.ndarray)
    expected = np.array([[1.0, 0.0, 0.0]])
    expected_v = np.repeat(expected, 100, axis=0)
    npt.assert_array_almost_equal(res, expected_v, decimal=7)


@pytest.mark.parametrize('function', [cyice.spkapo_s, cyice.spkapo, spice.spkapo], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkapo"], indirect=True)
def test_spkapo(function, grouped_benchmark, load_core_kernels):
    MARS, MOON = 499, 301
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("Jan 1 2004 5:00 PM")
    state = spice.spkssb(MOON, et, "J2000")
    grouped_benchmark(function, MARS, et, "J2000", state, "LT+S")
    pos_vec, ltime = function(MARS, et, "J2000", state, "LT+S")
    expected_pos = np.array([
        1.64534472413454592228e08,
        2.51219951337271928787e07,
        1.11454124484200235456e07,
    ])
    assert isinstance(pos_vec, np.ndarray)
    npt.assert_array_almost_equal(pos_vec, expected_pos, decimal=5)


@pytest.mark.parametrize('function', [cyice.spkapo_v, cyice.spkapo], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkapo_v"], indirect=True)
def test_spkapo_v(function, grouped_benchmark, load_core_kernels):
    MARS, MOON = 499, 301
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("Jan 1 2004 5:00 PM")
    state = spice.spkssb(MOON, et, "J2000")
    ets = np.repeat(et, 100)
    grouped_benchmark(function, MARS, ets, "J2000", state, "LT+S")
    pos_vec, ltime = function(MARS, ets, "J2000", state, "LT+S")
    assert isinstance(pos_vec, np.ndarray)
    assert isinstance(ltime, np.ndarray)


@pytest.mark.parametrize('function', [cyice.spkcpo_s, cyice.spkcpo, spice.spkcpo], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkcpo"], indirect=True)
def test_spkcpo(function, grouped_benchmark, load_earth_kernels):
    et = spice.str2et("2003 Oct 13 06:00:00")
    obspos = np.array([-2353.6213656676991, -4641.3414911499403, 3677.0523293197439])
    grouped_benchmark(function,"SUN", et, "DSS-14_TOPO", "OBSERVER", "CN+S", obspos, "EARTH", "ITRF93")
    state, lt = function(
        "SUN", et, "DSS-14_TOPO", "OBSERVER", "CN+S", obspos, "EARTH", "ITRF93"
    )
    expected_lt = 497.93167787805714
    expected_state = [
        6.25122733012810498476e07,
        5.89674929926417097449e07,
        -1.22059095879866167903e08,
        2.47597313358008614159e03,
        -9.87026711803482794494e03,
        -3.49990805659246507275e03,
    ]
    assert isinstance(state, np.ndarray)
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state, decimal=6)


@pytest.mark.parametrize('function', [cyice.spkcpo_v, cyice.spkcpo], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkcpo_v"], indirect=True)
def test_spkcpo_v(function, grouped_benchmark, load_earth_kernels):
    ets = np.repeat(spice.str2et("2003 Oct 13 06:00:00"), 100)
    obspos = np.array([-2353.6213656676991, -4641.3414911499403, 3677.0523293197439])
    grouped_benchmark(function, "SUN", ets, "DSS-14_TOPO", "OBSERVER", "CN+S", obspos, "EARTH", "ITRF93")
    states, lts = function(
        "SUN", ets, "DSS-14_TOPO", "OBSERVER", "CN+S", obspos, "EARTH", "ITRF93"
    )
    expected_lt = 497.93167787805714
    expected_state = [
        6.25122733012810498476e07,
        5.89674929926417097449e07,
        -1.22059095879866167903e08,
        2.47597313358008614159e03,
        -9.87026711803482794494e03,
        -3.49990805659246507275e03,
    ]
    assert isinstance(states, np.ndarray)
    assert isinstance(lts, np.ndarray)
    npt.assert_almost_equal(lts[0], expected_lt)
    npt.assert_array_almost_equal(states[0], expected_state, decimal=6)


@pytest.mark.parametrize('function', [cyice.spkcpt_s, cyice.spkcpt, spice.spkcpt], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkcpt"], indirect=True)
def test_spkcpt(function, grouped_benchmark, load_earth_kernels):
    obstime = spice.str2et("2003 Oct 13 06:00:00")
    trgpos = np.array([-2353.6213656676991, -4641.3414911499403, 3677.0523293197439])
    grouped_benchmark(function, trgpos, "EARTH", "ITRF93", obstime, "ITRF93", "TARGET", "CN+S", "SUN")
    state, lt = function(
        trgpos, "EARTH", "ITRF93", obstime, "ITRF93", "TARGET", "CN+S", "SUN"
    )
    expected_lt = 497.9321928250503
    expected_state = [
        -3.41263006568005401641e06,
        -1.47916331564148992300e08,
        1.98124035009580813348e07,
        -1.07582448117249587085e04,
        2.50028331500427839273e02,
        1.11355285621842696742e01,
    ]
    assert isinstance(state, np.ndarray)
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state, decimal=6)


@pytest.mark.parametrize('function', [cyice.spkcpt_v, cyice.spkcpt], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkcpt_v"], indirect=True)
def test_spkcpt_v(function, grouped_benchmark, load_earth_kernels):
    obstimes = np.repeat(spice.str2et("2003 Oct 13 06:00:00"), 100)
    trgpos = np.array([-2353.6213656676991, -4641.3414911499403, 3677.0523293197439])
    grouped_benchmark(function, trgpos, "EARTH", "ITRF93", obstimes, "ITRF93", "TARGET", "CN+S", "SUN")
    states, lts = function(
        trgpos, "EARTH", "ITRF93", obstimes, "ITRF93", "TARGET", "CN+S", "SUN"
    )
    expected_lt = 497.9321928250503
    expected_state = [
        -3.41263006568005401641e06,
        -1.47916331564148992300e08,
        1.98124035009580813348e07,
        -1.07582448117249587085e04,
        2.50028331500427839273e02,
        1.11355285621842696742e01,
    ]
    assert isinstance(states, np.ndarray)
    assert isinstance(lts, np.ndarray)
    npt.assert_almost_equal(lts[0], expected_lt)
    npt.assert_array_almost_equal(states[0], expected_state, decimal=6)


@pytest.mark.parametrize('function', [cyice.spkcvo_s, cyice.spkcvo, spice.spkcvo], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkcvo"], indirect=True)
def test_spkcvo(function, grouped_benchmark, load_earth_kernels):
    obstime = spice.str2et("2003 Oct 13 06:00:00")
    obstate = np.array([
        -2353.6213656676991,
        -4641.3414911499403,
        3677.0523293197439,
        -0.00000000000057086,
        0.00000000000020549,
        -0.00000000000012171,
    ])
    grouped_benchmark(function, "SUN",
        obstime,
        "DSS-14_TOPO",
        "OBSERVER",
        "CN+S",
        obstate,
        0.0,
        "EARTH",
        "ITRF93",
    )
    state, lt = function(
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
    expected_lt = 497.93167787798325
    expected_state = [
        6.25122733012975975871e07,
        5.89674929925705492496e07,
        -1.22059095879864960909e08,
        2.47597313358015026097e03,
        -9.87026711803497346409e03,
        -3.49990805659256830040e03,
    ]
    assert isinstance(state, np.ndarray)
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state, decimal=6)


@pytest.mark.parametrize('function', [cyice.spkcvo_v, cyice.spkcvo], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkcvo_v"], indirect=True)
def test_spkcvo_v(function, grouped_benchmark, load_earth_kernels):
    obstime = np.repeat(spice.str2et("2003 Oct 13 06:00:00"),100)
    obstate = np.array([
        -2353.6213656676991,
        -4641.3414911499403,
        3677.0523293197439,
        -0.00000000000057086,
        0.00000000000020549,
        -0.00000000000012171,
    ])
    grouped_benchmark(function, "SUN",
        obstime,
        "DSS-14_TOPO",
        "OBSERVER",
        "CN+S",
        obstate,
        0.0,
        "EARTH",
        "ITRF93",
    )
    state, lts = function(
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
    assert isinstance(state, np.ndarray)
    assert isinstance(lts, np.ndarray)


@pytest.mark.parametrize('function', [cyice.spkcvt_s, cyice.spkcvt, spice.spkcvt], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkcvt"], indirect=True)
def test_spkcvt(function, grouped_benchmark, load_earth_kernels):
    obstime = spice.str2et("2003 Oct 13 06:00:00")
    trgstate = np.array([
        -2353.6213656676991,
        -4641.3414911499403,
        3677.0523293197439,
        -0.00000000000057086,
        0.00000000000020549,
        -0.00000000000012171,
    ])
    grouped_benchmark(function, trgstate, 0.0, "EARTH", "ITRF93", obstime, "ITRF93", "TARGET", "CN+S", "SUN")
    state, lt = function(
        trgstate, 0.0, "EARTH", "ITRF93", obstime, "ITRF93", "TARGET", "CN+S", "SUN"
    )
    expected_lt = 497.932192824968
    expected_state = np.array([
        -3.41263006574816117063e06,
        -1.47916331564124494791e08,
        1.98124035009435638785e07,
        -1.07582448117247804475e04,
        2.50028331500423831812e02,
        1.11355285621839659171e01,
    ])
    npt.assert_almost_equal(lt, expected_lt)
    assert isinstance(state, np.ndarray)
    npt.assert_array_almost_equal(state, expected_state, decimal=6)


@pytest.mark.parametrize('function', [cyice.spkcvt_v, cyice.spkcvt], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkcvt_v"], indirect=True)
def test_spkcvt_v(function, grouped_benchmark, load_earth_kernels):
    obstime = np.repeat(spice.str2et("2003 Oct 13 06:00:00"), 100)
    trgstate = np.array([
        -2353.6213656676991,
        -4641.3414911499403,
        3677.0523293197439,
        -0.00000000000057086,
        0.00000000000020549,
        -0.00000000000012171,
    ])
    grouped_benchmark(function, trgstate, 0.0, "EARTH", "ITRF93", obstime, "ITRF93", "TARGET", "CN+S", "SUN")
    states, lts = function(
        trgstate, 0.0, "EARTH", "ITRF93", obstime, "ITRF93", "TARGET", "CN+S", "SUN"
    )
    expected_lts = np.repeat(497.932192824968, 100)
    expected_states = np.repeat(np.array([[
        -3.41263006574816117063e06,
        -1.47916331564124494791e08,
        1.98124035009435638785e07,
        -1.07582448117247804475e04,
        2.50028331500423831812e02,
        1.11355285621839659171e01,
    ]]), 100, axis=0)
    assert isinstance(lts, np.ndarray)
    npt.assert_array_almost_equal(lts, expected_lts)
    assert isinstance(states, np.ndarray)
    npt.assert_array_almost_equal(states, expected_states, decimal=6)


@pytest.mark.parametrize('function', [cyice.spkez_s, cyice.spkez, spice.spkez], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkez"], indirect=True)
def test_spkez(function, grouped_benchmark, load_core_kernels):
    et = cyice.str2et("July 4, 2003 11:00 AM PST")
    grouped_benchmark(function, 499, et, "J2000", "LT+S", 399)
    state, lt = function(499, et, "J2000", "LT+S", 399)
    assert isinstance(state, np.ndarray)


@pytest.mark.parametrize('function', [cyice.spkez_v, cyice.spkez], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkez_v"], indirect=True)
def test_spkez_v(function, grouped_benchmark, load_core_kernels):
    ets = np.repeat(cyice.str2et("July 4, 2003 11:00 AM PST"), 100)
    grouped_benchmark(function, 499, ets, "J2000", "LT+S", 399)
    state, lts = function(499, ets, "J2000", "LT+S", 399)
    assert isinstance(state, np.ndarray)
    assert isinstance(lts, np.ndarray)


@pytest.mark.parametrize('function', [cyice.spkezp_s, cyice.spkezp, spice.spkezp], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkezp"], indirect=True)
def test_spkezp(function, grouped_benchmark, load_core_kernels):
    et = cyice.str2et("July 4, 2003 11:00 AM PST")
    grouped_benchmark(function, 499, et, "J2000", "LT+S", 399)
    pos, lt = function(499, et, "J2000", "LT+S", 399)
    assert isinstance(pos, np.ndarray)
    expected_lt = 269.6898813661505
    npt.assert_almost_equal(lt, expected_lt)


@pytest.mark.parametrize('function', [cyice.spkezp_v, cyice.spkezp], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkezp_v"], indirect=True)
def test_spkezp_v(function, grouped_benchmark, load_core_kernels):
    ets = np.repeat(cyice.str2et("July 4, 2003 11:00 AM PST"), 100)
    grouped_benchmark(function, 499, ets, "J2000", "LT+S", 399)
    pos, lts = function(499, ets, "J2000", "LT+S", 399)
    assert isinstance(pos, np.ndarray)
    assert isinstance(lts, np.ndarray)


@pytest.mark.parametrize('function', [cyice.spkezr_s, cyice.spkezr, spice.spkezr], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkezr"], indirect=True)
def test_spkezr(function, grouped_benchmark, load_core_kernels):
    et = cyice.str2et("July 4, 2003 11:00 AM PST")
    grouped_benchmark(function, "Mars", et, "J2000", "LT+S", "Earth")
    state, lt = function("Mars", et, "J2000", "LT+S", "Earth")
    assert isinstance(state, np.ndarray)


@pytest.mark.parametrize('function', [cyice.spkezr_v, cyice.spkezr, spice.spkezr], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkezr_v"], indirect=True)
def test_spkezr_v(function, grouped_benchmark, load_core_kernels):
    ets = np.full((100,), spice.str2et("July 4, 2003 11:00 AM PST"))
    grouped_benchmark(function, "Mars", ets, "J2000", "LT+S", "Earth")
    state, lts = function("Mars", ets, "J2000", "LT+S", "Earth")
    assert isinstance(lts, np.ndarray)
    assert isinstance(state, np.ndarray)
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
    npt.assert_allclose(lts, expected_lt)
    npt.assert_allclose(state, expected_state)



@pytest.mark.parametrize('function', [cyice.spkgeo_s, cyice.spkgeo, spice.spkgeo], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkgeo"], indirect=True)
def test_spkgeo(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("July 4, 2003 11:00 AM PST")
    grouped_benchmark(function, 499, et, "J2000", 399)
    state, lt = function(499, et, "J2000", 399)
    expected_lt = 269.70264751151603
    expected_state = [
        7.38262164145559966564e07,
        -2.71280305524311661720e07,
        -1.87419738849752545357e07,
        -6.80950358877040429206e00,
        7.51381423681132254444e00,
        3.00129002640705921934e00,
    ]
    assert isinstance(state, np.ndarray)
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(state, expected_state)


@pytest.mark.parametrize('function', [cyice.spkgeo_v, cyice.spkgeo], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkgeo_v"], indirect=True)
def test_spkgeo_v(function, grouped_benchmark, load_core_kernels):
    et = np.repeat(spice.str2et("July 4, 2003 11:00 AM PST"),100)
    grouped_benchmark(function, 499, et, "J2000", 399)
    state, lt = function(499, et, "J2000", 399)
    assert isinstance(state, np.ndarray)
    assert isinstance(lt, np.ndarray)


@pytest.mark.parametrize('function', [cyice.spkgps_s, cyice.spkgps, spice.spkgps], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkgps"], indirect=True)
def test_spkgps(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("July 4, 2003 11:00 AM PST")
    grouped_benchmark(function, 499, et, "J2000", 399)
    pos, lt = function(499, et, "J2000", 399)
    expected_lt = 269.70264751151603
    expected_pos = [
        73826216.41455599665641784668,
        -27128030.55243116617202758789,
        -18741973.88497525453567504883,
    ]
    assert isinstance(pos, np.ndarray)
    npt.assert_almost_equal(lt, expected_lt)
    npt.assert_array_almost_equal(pos, expected_pos)


@pytest.mark.parametrize('function', [cyice.spkgps_v, cyice.spkgps], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkgps_v"], indirect=True)
def test_spkgps_v(function, grouped_benchmark, load_core_kernels):
    et = np.repeat(spice.str2et("July 4, 2003 11:00 AM PST"),100)
    grouped_benchmark(function, 499, et, "J2000", 399)
    pos, lt = function(499, et, "J2000", 399)
    assert isinstance(pos, np.ndarray)
    assert isinstance(lt, np.ndarray)


@pytest.mark.parametrize('function', [cyice.spkpos_s, cyice.spkpos, spice.spkpos], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkpos"], indirect=True)
def test_spkpos(function, grouped_benchmark, load_core_kernels):
    et = cyice.str2et("July 4, 2003 11:00 AM PST")
    grouped_benchmark(function, "Mars", et, "J2000", "LT+S", "Earth")


@pytest.mark.parametrize('function', [cyice.spkpos_v, cyice.spkpos, spice.spkpos], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkpos_v"], indirect=True)
def test_spkpos_v(function, grouped_benchmark, load_core_kernels):
    ets = np.repeat(spice.str2et("July 4, 2003 11:00 AM PST"), 100)
    grouped_benchmark(function, "Mars", ets, "J2000", "LT+S", "Earth")
    ptargs, lts = function("Mars", ets, "J2000", "LT+S", "Earth")
    assert isinstance(ptargs, np.ndarray)


@pytest.mark.parametrize('function', [cyice.spkpvn_s, cyice.spkpvn, spice.spkpvn], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkpvn"], indirect=True)
def test_spkpvn(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("2002 APR 27 00:00:00.000 TDB")
    handle, descr, ident = spice.spksfs(5, et, 41)
    grouped_benchmark(function, handle, descr, et)
    refid, state, center = function(handle, descr, et)
    expected_state = [
        -2.70063336478468656540e08,
        6.69404818553274393082e08,
        2.93505043081457614899e08,
        -1.24191493217698472051e01,
        -3.70147572019018955558e00,
        -1.28422514561611489370e00,
    ]
    npt.assert_array_almost_equal(state, expected_state)
    assert isinstance(state, np.ndarray)


@pytest.mark.parametrize('function', [cyice.spkpvn_v, cyice.spkpvn], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkpvn_v"], indirect=True)
def test_spkpvn_v(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("2002 APR 27 00:00:00.000 TDB")
    handle, descr, ident = spice.spksfs(5, et, 41)
    ets = np.repeat(et, 100)
    grouped_benchmark(function, handle, descr, ets)
    refid, states, center = function(handle, descr, ets)
    assert isinstance(states, np.ndarray)
    assert states.dtype == float
    assert isinstance(refid, np.ndarray)
    assert refid.dtype == np.int32
    assert isinstance(center, np.ndarray)
    assert center.dtype == np.int32


@pytest.mark.parametrize('function', [cyice.spkssb_s, cyice.spkssb, spice.spkssb], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkssb"], indirect=True)
def test_spkssb(function, grouped_benchmark, load_core_kernels):
    et = cyice.str2et("July 4, 2003 11:00 AM PST")
    grouped_benchmark(function, 499, et, "J2000")
    state = function(499, et, "J2000")
    assert isinstance(state, np.ndarray)


@pytest.mark.parametrize('function', [cyice.spkssb_v, cyice.spkssb], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkssb_v"], indirect=True)
def test_spkssb_v(function, grouped_benchmark, load_core_kernels):
    ets = np.repeat(cyice.str2et("July 4, 2003 11:00 AM PST"), 100)
    grouped_benchmark(function, 499, ets, "J2000")
    state = function(499, ets, "J2000")
    assert isinstance(state, np.ndarray)


@pytest.mark.parametrize('function', [cyice.str2et_s, cyice.str2et, spice.str2et], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["str2et"], indirect=True)
def test_str2et(function, grouped_benchmark, load_core_kernels):
    grouped_benchmark(function, "Thu Mar 20 12:53:29 PST 1997")


@pytest.mark.parametrize('function', [cyice.str2et_v, cyice.str2et, spice.str2et], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["str2et_v"], indirect=True)
def test_str2et_v(function, grouped_benchmark, load_core_kernels):
    date = "Thu Mar 20 12:53:29 PST 1997"
    dates = np.repeat(date, 100)
    grouped_benchmark(function, dates)
    expected_ets = np.repeat(-87836728.81438904, 100)
    ets = function(dates)
    assert isinstance(ets, np.ndarray)
    npt.assert_array_almost_equal(ets, expected_ets)


@pytest.mark.parametrize('function', [cyice.sincpt_s, cyice.sincpt, spice.sincpt], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sincpt"], indirect=True)
def test_sincpt(function, grouped_benchmark, load_cassini_kernels):
    et = spice.str2et("2013 FEB 25 11:50:00 UTC")
    camid = spice.bodn2c("CASSINI_ISS_NAC")
    shape, frame, bsight, n, bounds = spice.getfov(camid, 4)
    grouped_benchmark(function, "Ellipsoid", "Enceladus", et, "IAU_ENCELADUS", "CN+S", "CASSINI", frame, bsight)
    res = function("Ellipsoid", "Enceladus", et, "IAU_ENCELADUS", "CN+S", "CASSINI", frame, bsight)
    spoint, trgepc, obspos = res[0], res[1], res[2]
    assert isinstance(spoint, np.ndarray)
    assert isinstance(obspos, np.ndarray)
    npt.assert_almost_equal(trgepc, 415065064.9055491)


@pytest.mark.parametrize('function', [cyice.sincpt_v, cyice.sincpt], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sincpt_v"], indirect=True)
def test_sincpt_v(function, grouped_benchmark, load_cassini_kernels):
    ets = np.repeat(spice.str2et("2013 FEB 25 11:50:00 UTC"), 100)
    camid = spice.bodn2c("CASSINI_ISS_NAC")
    shape, frame, bsight, n, bounds = spice.getfov(camid, 4)
    grouped_benchmark(function, "Ellipsoid", "Enceladus", ets, "IAU_ENCELADUS", "CN+S", "CASSINI", frame, bsight)
    res = function("Ellipsoid", "Enceladus", ets, "IAU_ENCELADUS", "CN+S", "CASSINI", frame, bsight)
    spoint, trgepc, obspos = res[0], res[1], res[2]
    assert isinstance(spoint, np.ndarray)
    assert isinstance(trgepc, np.ndarray)
    assert isinstance(obspos, np.ndarray)
    npt.assert_almost_equal(trgepc[0], 415065064.9055491)


@pytest.mark.parametrize('function', [cyice.srfrec_s, cyice.srfrec, spice.srfrec], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["srfrec"], indirect=True)
def test_srfrec(function, grouped_benchmark, load_core_kernels):
    lon = np.radians(100.0)
    lat = np.radians(35.0)
    res = grouped_benchmark(function, 399, lon, lat)
    assert isinstance(res, np.ndarray)
    expected = np.array([-906.24919474, 5139.59458217, 3654.29989637])
    npt.assert_array_almost_equal(res, expected, decimal=7)


@pytest.mark.parametrize('function', [cyice.srfrec_v, cyice.srfrec], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["srfrec_v"], indirect=True)
def test_srfrec_v(function, grouped_benchmark, load_core_kernels):
    lon = np.repeat(np.radians(100.0), 100)
    lat = np.repeat(np.radians(35.0),  100)
    res = grouped_benchmark(function, 399, lon, lat)
    assert isinstance(res, np.ndarray)
    expected = np.array([[-906.24919474, 5139.59458217, 3654.29989637]])
    expected_v = np.repeat(expected, 100, axis=0)
    npt.assert_array_almost_equal(res, expected_v, decimal=7)


@pytest.mark.parametrize('function', [cyice.subpnt_s, cyice.subpnt, spice.subpnt], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["subpnt"], indirect=True)
def test_subpnt(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("2008 aug 11 00:00:00")
    method = "Intercept:  ellipsoid"
    grouped_benchmark(function, method, "Mars", et, "IAU_MARS", "LT+S", "Earth")
    spoint, trgepc, srfvec = function(method, "Mars", et, "IAU_MARS", "LT+S", "Earth")
    assert isinstance(spoint, np.ndarray)
    assert isinstance(srfvec, np.ndarray)


@pytest.mark.parametrize('function', [cyice.subpnt_v, cyice.subpnt], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["subpnt_v"], indirect=True)
def test_subpnt_v(function, grouped_benchmark, load_core_kernels):
    et = np.repeat(spice.str2et("2008 aug 11 00:00:00"), 100)
    method = "Intercept:  ellipsoid"
    grouped_benchmark(function, method, "Mars", et, "IAU_MARS", "LT+S", "Earth")
    spoint, trgepc, srfvec = function(method, "Mars", et, "IAU_MARS", "LT+S", "Earth")
    assert isinstance(spoint, np.ndarray)
    assert isinstance(trgepc, np.ndarray)
    assert isinstance(srfvec, np.ndarray)


@pytest.mark.parametrize('function', [cyice.subslr_s, cyice.subslr, spice.subslr], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["subslr"], indirect=True)
def test_subslr(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("2008 aug 11 00:00:00")
    method = "Intercept:  ellipsoid"
    grouped_benchmark(function, method, "Mars", et, "IAU_MARS", "LT+S", "Earth")
    spoint, trgepc, srfvec = function(method, "Mars", et, "IAU_MARS", "LT+S", "Earth")
    assert isinstance(spoint, np.ndarray)
    assert isinstance(srfvec, np.ndarray)


@pytest.mark.parametrize('function', [cyice.subslr_v, cyice.subslr], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["subslr_v"], indirect=True)
def test_subslr_v(function, grouped_benchmark, load_core_kernels):
    et = np.repeat(spice.str2et("2008 aug 11 00:00:00"), 100)
    method = "Intercept:  ellipsoid"
    grouped_benchmark(function, method, "Mars", et, "IAU_MARS", "LT+S", "Earth")
    spoint, trgepc, srfvec = function(method, "Mars", et, "IAU_MARS", "LT+S", "Earth")
    assert isinstance(spoint, np.ndarray)
    assert isinstance(trgepc, np.ndarray)
    assert isinstance(srfvec, np.ndarray)


@pytest.mark.parametrize('function', [cyice.sxform_s, cyice.sxform, spice.sxform], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sxform"], indirect=True)
def test_sxform(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("January 1, 1990")
    grouped_benchmark(function, "IAU_EARTH", "J2000", et)
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
    xform = cyice.sxform("IAU_EARTH", "J2000", et)
    assert isinstance(xform, np.ndarray)
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


@pytest.mark.parametrize('function', [cyice.sxform_v, cyice.sxform, spice.sxform], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sxform_v"], indirect=True)
def test_sxform_v(function, grouped_benchmark, load_core_kernels):
    et = np.repeat(spice.str2et("January 1, 1990"), 1000)
    grouped_benchmark(function, "IAU_EARTH", "J2000", et)
    res = function("IAU_EARTH", "J2000", et)
    assert isinstance(res, np.ndarray)


@pytest.mark.parametrize('function', [cyice.tangpt_s, cyice.tangpt, spice.tangpt], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["tangpt"], indirect=True)
def test_tangpt(function, grouped_benchmark, load_core_kernels):
    spice.furnsh(
        [
            CassiniKernels.satSpk,
            CassiniKernels.cassTourSpk,
            ExtraKernels.earthHighPerPck,
            ExtraKernels.earthStnSpk,
        ]
    )
    locus = "TANGENT POINT"
    sc = "CASSINI"
    target = "SATURN"
    obsrvr = "DSS-14"
    fixref = "IAU_SATURN"
    rayfrm = "J2000"
    et = spice.str2et("2013-FEB-13 11:21:20.213872 (TDB)")
    raydir, raylt = spice.spkpos(sc, et, rayfrm, "NONE", obsrvr)
    grouped_benchmark(function, "ELLIPSOID", target, et, fixref, "NONE", locus, obsrvr, rayfrm, raydir)
    # correctness test
    tanpt, alt, range, srfpt, trgepc, srfvec = spice.tangpt(
        "ELLIPSOID", target, et, fixref, "NONE", locus, obsrvr, rayfrm, raydir
    )
    assert isinstance(tanpt, np.ndarray)
    assert isinstance(srfpt, np.ndarray)
    npt.assert_array_almost_equal(
        tanpt, [-113646.428171, 213634.489363, -222709.965702], decimal=5
    )
    assert alt == pytest.approx(271285.892825)
    assert range == pytest.approx(1425243487.098913)
    npt.assert_array_almost_equal(
        srfpt, [-21455.320586, 40332.076698, -35458.506180], decimal=5
    )
    assert trgepc == pytest.approx(414026480.213872)


@pytest.mark.parametrize('function', [cyice.tangpt_v, cyice.tangpt], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["tangpt_v"], indirect=True)
def test_tangpt_v(function, grouped_benchmark, load_core_kernels):
    spice.furnsh(
        [
            CassiniKernels.satSpk,
            CassiniKernels.cassTourSpk,
            ExtraKernels.earthHighPerPck,
            ExtraKernels.earthStnSpk,
        ]
    )
    locus = "TANGENT POINT"
    sc = "CASSINI"
    target = "SATURN"
    obsrvr = "DSS-14"
    fixref = "IAU_SATURN"
    rayfrm = "J2000"
    et = spice.str2et("2013-FEB-13 11:21:20.213872 (TDB)")
    raydir, raylt = spice.spkpos(sc, et, rayfrm, "NONE", obsrvr)
    ets = np.repeat(et, 100)
    grouped_benchmark(function, "ELLIPSOID", target, ets, fixref, "NONE", locus, obsrvr, rayfrm, raydir)


@pytest.mark.parametrize('function', [cyice.termpt_s, cyice.termpt, spice.termpt], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["termpt"], indirect=True)
def test_termpt(function, grouped_benchmark, load_core_kernels):
    spice.furnsh(ExtraKernels.marsSpk)
    spice.furnsh(ExtraKernels.phobosDsk)
    et = spice.str2et("1972 AUG 11 00:00:00")
    args = (
        "UMBRAL/TANGENT/DSK/UNPRIORITIZED",
        "SUN",
        "Phobos",
        et,
        "IAU_PHOBOS",
        "CN+S",
        "CENTER",
        "MARS",
        np.array([0.0, 0.0, 1.0]),
        spice.twopi() / 3.0,
        3,
        1.0e-4,
        1.0e-7,
        3,
    )
    npts, points, epochs, tangts = grouped_benchmark(function, *args)
    assert npts.sum() == 3
    assert len(points) == 3


@pytest.mark.parametrize('function', [cyice.termpt_v, cyice.termpt], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["termpt_v"], indirect=True)
def test_termpt_v(function, grouped_benchmark, load_core_kernels):
    spice.furnsh(ExtraKernels.marsSpk)
    spice.furnsh(ExtraKernels.phobosDsk)
    et = spice.str2et("1972 AUG 11 00:00:00")
    ets = np.linspace(et, et+1, 100)
    args = (
        "UMBRAL/TANGENT/DSK/UNPRIORITIZED",
        "SUN",
        "Phobos",
        ets,
        "IAU_PHOBOS",
        "CN+S",
        "CENTER",
        "MARS",
        np.array([0.0, 0.0, 1.0]),
        spice.twopi() / 3.0,
        3,
        1.0e-4,
        1.0e-7,
        3,
    )
    npts, points, epochs, tangts = grouped_benchmark(function, *args)
    assert npts.shape == (100,3)
    assert points.shape == (100, 3, 3)


@pytest.mark.parametrize('function', [cyice.timout_s, cyice.timout, spice.timout], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["timout"], indirect=True)
def test_timout(function, grouped_benchmark, load_core_kernels):
    sample = "Thu Oct 1 11:11:11 PDT 1111"
    spice.furnsh(CoreKernels.testMetaKernel)
    pic, ok, err = spice.tpictr(sample)
    assert ok
    et = 188745364.0
    grouped_benchmark(function, et, pic)
    out = function(et, pic)
    assert out == "Sat Dec 24 18:14:59 PDT 2005"


@pytest.mark.parametrize('function', [cyice.timout_v, cyice.timout, spice.timout], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["timout_v"], indirect=True)
def test_timout_v(function, grouped_benchmark, load_core_kernels):
    sample = "Thu Oct 1 11:11:11 PDT 1111"
    spice.furnsh(CoreKernels.testMetaKernel)
    pic, ok, err = spice.tpictr(sample)
    assert ok
    ets = np.repeat(188745364.0, 100)
    grouped_benchmark(function, ets, pic)
    out = function(ets, pic)
    assert out[0] == "Sat Dec 24 18:14:59 PDT 2005"


@pytest.mark.parametrize('function', [cyice.trgsep_s, cyice.trgsep, spice.trgsep], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["trgsep"], indirect=True)
def test_trgsep(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("2007-JAN-11 11:21:20.213872 (TDB)")
    grouped_benchmark(function, et, "MOON", "POINT", "IAU_MOON", "EARTH", "POINT", "IAU_EARTH", "SUN", "LT+S")
    point_sep = function(et, "MOON", "POINT", "IAU_MOON", "EARTH", "POINT", "IAU_EARTH", "SUN", "LT+S")
    assert spice.dpr() * point_sep == pytest.approx(0.15729276)


@pytest.mark.parametrize('function', [cyice.trgsep_v, cyice.trgsep], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["trgsep_v"], indirect=True)
def test_trgsep_v(function, grouped_benchmark, load_core_kernels):
    ets = np.repeat(spice.str2et("2007-JAN-11 11:21:20.213872 (TDB)"),100)
    grouped_benchmark(function, ets, "MOON", "POINT", "IAU_MOON", "EARTH", "POINT", "IAU_EARTH", "SUN", "LT+S")
    res = function(ets, "MOON", "POINT", "IAU_MOON", "EARTH", "POINT", "IAU_EARTH", "SUN", "LT+S")
    assert isinstance(res, np.ndarray)


@pytest.mark.parametrize('function', [cyice.twopi, spice.twopi], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["twopi"], indirect=True)
def test_twopi(function, grouped_benchmark):
    grouped_benchmark(function)
    assert function() == (np.pi * 2)


@pytest.mark.parametrize('function', [cyice.tyear, spice.tyear], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["tyear"], indirect=True)
def test_tyear(function, grouped_benchmark):
    grouped_benchmark(function)
    assert function() == 31556925.9747


@pytest.mark.parametrize('function', [cyice.unitim_s, cyice.unitim, spice.unitim], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["unitim"], indirect=True)
def test_unitim(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("Dec 19 2003")
    grouped_benchmark(function, et, "ET", "JED")
    # correctness assertion can be performed before or after
    converted_et = function(et, "ET", "JED")
    npt.assert_almost_equal(converted_et, 2452992.5007428653)


@pytest.mark.parametrize('function', [cyice.unitim_v, cyice.unitim], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["unitim_v"], indirect=True)
def test_unitim_v(function, grouped_benchmark, load_core_kernels):
    ets = np.repeat(spice.str2et("Dec 19 2003"), 100)
    grouped_benchmark(function, ets, "ET", "JED")
    res = function(ets, "ET", "JED")
    assert isinstance(res, np.ndarray)


@pytest.mark.parametrize('function', [cyice.unload, spice.unload], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["unload"], indirect=True)
def test_unload(function, grouped_benchmark):
    spice.furnsh(CoreKernels.testMetaKernel)
    grouped_benchmark(function, CoreKernels.testMetaKernel)


@pytest.mark.parametrize('function', [cyice.utc2et_s, cyice.utc2et, spice.utc2et], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["utc2et"], indirect=True)
def test_utc2et(function, grouped_benchmark, load_core_kernels):
    grouped_benchmark(function, "December 1, 2004 15:04:11")
    assert function("December 1, 2004 15:04:11") == 155185515.1831043


@pytest.mark.parametrize('function', [cyice.utc2et_v, cyice.utc2et], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["utc2et_v"], indirect=True)
def test_utc2et_v(function, grouped_benchmark, load_core_kernels):
    dates = np.repeat("December 1, 2004 15:04:11", 100)
    grouped_benchmark(function, dates)
    res = function(dates)
    assert isinstance(res, np.ndarray)


# X 

@pytest.mark.parametrize('function', [cyice.xfmsta_s, cyice.xfmsta, spice.xfmsta], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["xfmsta"], indirect=True)
def test_xfmsta(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("July 4, 2003 11:00 AM PST")
    state, lt = spice.spkezr("Mars", et, "J2000", "LT+S", "Earth")
    grouped_benchmark(function, state, "rectangular", "latitudinal", " ")
    res = function(state, "rectangular", "latitudinal", " ")
    expected_lat_state = np.array([
        8.08509924324866235256e07,
        -3.52158255331780634112e-01,
        -2.33928262716770696272e-01,
        -9.43348972618204761886e00,
        5.98157681117165682860e-08,
        1.03575559016377728336e-08,
    ])
    npt.assert_array_almost_equal(res, expected_lat_state)


@pytest.mark.parametrize('function', [cyice.xfmsta_v, cyice.xfmsta], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["xfmsta_v"], indirect=True)
def test_xfmsta_v(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("July 4, 2003 11:00 AM PST")
    state, lt = spice.spkezr("Mars", et, "J2000", "LT+S", "Earth")
    state_v = np.repeat([state], 100, axis=0)
    grouped_benchmark(function, state_v, "rectangular", "latitudinal", " ")
    res = function(state_v, "rectangular", "latitudinal", " ")
    expected_lat_state = np.array([[
        8.08509924324866235256e07,
        -3.52158255331780634112e-01,
        -2.33928262716770696272e-01,
        -9.43348972618204761886e00,
        5.98157681117165682860e-08,
        1.03575559016377728336e-08,
    ]])
    expected_lat_state_v = np.repeat(expected_lat_state, 100, axis=0)
    npt.assert_array_almost_equal(res, expected_lat_state_v)

