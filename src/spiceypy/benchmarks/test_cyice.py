import os
import time
import timeit

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

def get_qualified_name(func):
    return '.'.join(f"{func.__module__}.{func.__qualname__}".split('.')[-2:])

def get_module_name(func):
    return f"{func.__module__.split('.')[-1]}"

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

def cleanup_kernel(path):
    spice.kclear()
    spice.reset()
    if spice.exists(path):
        os.remove(path)  # pragma: no cover
    pass


def setup_module(module):
    download_kernels()


def test_cyice_b1900_correctness():
    assert cyice.b1900() == 2415020.31352


@pytest.mark.parametrize('function', [cyice.b1900, spice.b1900], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["b1900"], indirect=True)
def test_perf_b1900(function, grouped_benchmark):
    grouped_benchmark(function)


@pytest.mark.parametrize('function', [cyice.ckgp, spice.ckgp], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["ckgp"], indirect=True)
def test_perf_ckgp(function, grouped_benchmark, load_cassini_kernels):
    ckid  = -82000
    cover = 267832537952.0
    grouped_benchmark(function, ckid, cover, 256, "J2000")
    res = function(ckid, cover, 256, "J2000")
    cmat, clkout = res[0], res[1]
    assert clkout == 267832537952.0
    assert isinstance(cmat, np.ndarray)
    expected_cmat = [
        [0.5064665782997639365, -0.75794210739897316387, 0.41111478554891744963],
        [-0.42372128242505308071, 0.19647683351734512858, 0.88422685364733510927],
        [-0.7509672961490383436, -0.6220294331642198804, -0.22164725216433822652],
    ]
    npt.assert_array_almost_equal(cmat, expected_cmat)


@pytest.mark.parametrize('function', [cyice.ckgpav, spice.ckgpav], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["ckgpav"], indirect=True)
def test_perf_ckgpav(function, grouped_benchmark, load_cassini_kernels):
    ckid  = -82000
    cover = 267832537952.0
    grouped_benchmark(function, ckid, cover, 256, "J2000")
    res = function(ckid, cover, 256, "J2000")
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


@pytest.mark.parametrize('function', [cyice.convrt, spice.convrt], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["convrt"], indirect=True)
def test_perf_convrt(function, grouped_benchmark):
    grouped_benchmark(function, 1.0, "parsecs", "lightyears")
    assert function(300.0, "statute_miles", "km") == 482.80320


@pytest.mark.parametrize('function', [cyice.convrt_v, spice.convrt], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["convrt_v"], indirect=True)
def test_perf_convrt_v(function, grouped_benchmark):
    data = np.arange(0, 1000.0, dtype=float)
    grouped_benchmark(function, data, "parsecs", "lightyears")


@pytest.mark.parametrize('function', [cyice.deltet, spice.deltet], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["deltet"], indirect=True)
def test_perf_deltet(function, grouped_benchmark, load_core_kernels):
    et_2004 = spice.str2et("Jan 1 2004")
    grouped_benchmark(function, et_2004, "ET")


@pytest.mark.parametrize('function', [cyice.deltet_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["deltet_v"], indirect=True)
def test_perf_deltet_v(function, grouped_benchmark, load_core_kernels):
    ets_2004 = np.repeat(spice.str2et("Jan 1 2004"), 100)
    grouped_benchmark(function, ets_2004, "ET")
    res = function(ets_2004, "ET")
    assert isinstance(res, np.ndarray)


def test_cyice_et2utc_v_correctness(load_core_kernels):
    et = -527644192.5403653
    output = cyice.et2utc_v(np.array([et] * 100), "J", 6)
    assert isinstance(output, list)
    assert np.array_equal(
        output,
        np.array(["JD 2445438.006415"] * 100),
    )


@pytest.mark.parametrize('function', [cyice.et2utc, spice.et2utc], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["et2utc"], indirect=True)
def test_perf_et2utc(function, grouped_benchmark, load_core_kernels):
    grouped_benchmark(function,  -527644192.5403653, "J", 6)


@pytest.mark.parametrize('function', [cyice.et2utc_v, spice.et2utc], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["et2utc_v"], indirect=True)
def test_perf_et2utc_v(function, grouped_benchmark, load_core_kernels):
    ets = np.array([-527644192.5403653] * 10000)
    grouped_benchmark(function, ets, "J", 6)


@pytest.mark.parametrize('function', [cyice.etcal, spice.etcal], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["etcal"], indirect=True)
def test_perf_etcal(function, grouped_benchmark):
    grouped_benchmark(function, 0.0)


@pytest.mark.parametrize('function', [cyice.etcal_v, spice.etcal], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["etcal_v"], indirect=True)
def test_perf_etcal_v(function, grouped_benchmark):
    data = np.arange(10000.0, dtype=float)
    grouped_benchmark(function, data)
    res = function(data)
    assert isinstance(res, np.ndarray)


@pytest.mark.parametrize('function', [cyice.failed, spice.failed], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["failed"], indirect=True)
def test_perf_failed(function, grouped_benchmark):
    grouped_benchmark(function)


@pytest.mark.parametrize('function', [cyice.fovray, spice.fovray], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["fovray"], indirect=True)
def test_perf_fovray(function, grouped_benchmark, load_cassini_kernels):
    # core of test
    camid = spice.bodn2c("CASSINI_ISS_NAC")
    shape, frame, bsight, n, bounds = spice.getfov(camid, 4)
    et = spice.str2et("2013 FEB 25 11:50:00 UTC")
    raydir = np.array([0.0, 0.0, 1.0])
    grouped_benchmark(function, "CASSINI_ISS_NAC", raydir, frame, "S", "CASSINI", et)
    assert function("CASSINI_ISS_NAC", raydir, frame, "S", "CASSINI", et)


@pytest.mark.parametrize('function', [cyice.fovray_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["fovray_v"], indirect=True)
def test_perf_fovray_v(function, grouped_benchmark, load_cassini_kernels):
    # core of test
    ets = np.repeat(spice.str2et("2013 FEB 25 11:50:00 UTC"), 100)
    raydir = np.array([0.0, 0.0, 1.0])
    grouped_benchmark(function, "CASSINI_ISS_NAC", raydir, "CASSINI_ISS_NAC", "S", "CASSINI", ets)
    res = function("CASSINI_ISS_NAC", raydir, "CASSINI_ISS_NAC", "S", "CASSINI", ets)
    assert isinstance(res, np.ndarray)
    assert res.dtype == np.bool


@pytest.mark.parametrize('function', [cyice.fovtrg, spice.fovtrg], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["fovtrg"], indirect=True)
def test_perf_fovtrg(function, grouped_benchmark, load_cassini_kernels):
    et = spice.str2et("2013 FEB 25 11:50:00 UTC")
    grouped_benchmark(function, "CASSINI_ISS_NAC", "Enceladus", "Ellipsoid", "IAU_ENCELADUS", "LT+S","CASSINI", et)


@pytest.mark.parametrize('function', [cyice.fovtrg_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["fovtrg_v"], indirect=True)
def test_perf_fovtrg_v(function, grouped_benchmark, load_cassini_kernels):
    ets = np.repeat(spice.str2et("2013 FEB 25 11:50:00 UTC"), 100)
    grouped_benchmark(function, "CASSINI_ISS_NAC","Enceladus", "Ellipsoid", "IAU_ENCELADUS", "LT+S","CASSINI", ets)
    res = function( "CASSINI_ISS_NAC","Enceladus", "Ellipsoid", "IAU_ENCELADUS", "LT+S","CASSINI", ets)
    assert isinstance(res, np.ndarray)
    assert res.dtype == np.bool


@pytest.mark.parametrize('function', [cyice.lspcn, spice.lspcn], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["lspcn"], indirect=True)
def test_perf_lspcn(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("21 march 2005")
    grouped_benchmark(function, "EARTH", et, "NONE")


@pytest.mark.parametrize('function', [cyice.reset, spice.reset], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["reset"], indirect=True)
def test_perf_reset(function, grouped_benchmark):
   grouped_benchmark(function)


def test_cyice_spkcvt_correctness(load_earth_kernels):
    obstime = spice.str2et("2003 Oct 13 06:00:00")
    trgstate = np.array([
        -2353.6213656676991,
        -4641.3414911499403,
        3677.0523293197439,
        -0.00000000000057086,
        0.00000000000020549,
        -0.00000000000012171,
    ])
    state, lt = cyice.spkcvt(
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


@pytest.mark.parametrize('function', [cyice.spkcvt, spice.spkcvt], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkcvt"], indirect=True)
def test_perf_spkcvt(function, grouped_benchmark, load_earth_kernels):
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


@pytest.mark.parametrize('function', [cyice.scdecd, spice.scdecd], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["scdecd"], indirect=True)
def test_perf_scdecd(function, grouped_benchmark, load_voyager_kernels):
    timein = spice.scencd(-32, "2/20538:39:768")
    grouped_benchmark(function, -32, timein)


@pytest.mark.parametrize('function', [cyice.scencd, spice.scencd], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["scencd"], indirect=True)
def test_perf_scencd(function, grouped_benchmark, load_voyager_kernels):
    grouped_benchmark(function, -32,  "2/20538:39:768")


@pytest.mark.parametrize('function', [cyice.sce2c, spice.sce2c], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sce2c"], indirect=True)
def test_perf_sce2c(function, grouped_benchmark, load_voyager_kernels):
    et = spice.str2et("1979 JUL 05 21:50:21.23379")
    grouped_benchmark(function, -32, et)


@pytest.mark.parametrize('function', [cyice.sce2s, spice.sce2s], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sce2s"], indirect=True)
def test_perf_sce2s(function, grouped_benchmark):
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.voyagerSclk)
    et = spice.str2et("1979 JUL 05 21:50:21.23379")
    grouped_benchmark(function, -32, et)


@pytest.mark.parametrize('function', [cyice.scs2e, spice.scs2e], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["scs2e"], indirect=True)
def test_perf_scs2e(function, grouped_benchmark, load_voyager_kernels):
    grouped_benchmark(function, -32, "2/20538:39:768")


@pytest.mark.parametrize('function', [cyice.sct2e, spice.sct2e], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sct2e"], indirect=True)
def test_perf_sct2e(function, grouped_benchmark, load_voyager_kernels):
    grouped_benchmark(function, -32,  985327965.0)


@pytest.mark.parametrize('function', [cyice.getmsg, spice.getmsg], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["getmsg"], indirect=True)
def test_perf_getmsg(function, grouped_benchmark):
    cyice.reset()
    spice.sigerr("test error")
    grouped_benchmark(function, "SHORT", 200)
    cyice.reset()


@pytest.mark.parametrize('function', [cyice.qcktrc, spice.qcktrc], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["qcktrc"], indirect=True)
def test_perf_qcktrc(function, grouped_benchmark):
    cyice.reset()
    spice.chkin("test")
    spice.chkin("qcktrc")
    grouped_benchmark(function, 40)
    trace = function(40)
    assert trace == "test --> qcktrc"
    spice.chkout("qcktrc")
    spice.chkout("test")
    cyice.reset()


@pytest.mark.parametrize('function', [cyice.spkez, spice.spkez], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkez"], indirect=True)
def test_perf_spkez(function, grouped_benchmark, load_core_kernels):
    et = cyice.str2et("July 4, 2003 11:00 AM PST")
    grouped_benchmark(function, 499, et, "J2000", "LT+S", 399)
    state, lt = function(499, et, "J2000", "LT+S", 399)
    assert isinstance(state, np.ndarray)


@pytest.mark.parametrize('function', [cyice.spkez_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkez_v"], indirect=True)
def test_perf_spkez_v(function, grouped_benchmark, load_core_kernels):
    ets = np.repeat(cyice.str2et("July 4, 2003 11:00 AM PST"), 100)
    grouped_benchmark(function, 499, ets, "J2000", "LT+S", 399)
    state, lts = function(499, ets, "J2000", "LT+S", 399)
    assert isinstance(state, np.ndarray)
    assert isinstance(lts, np.ndarray)


@pytest.mark.parametrize('function', [cyice.spkezr, spice.spkezr], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkezr"], indirect=True)
def test_perf_spkezr(function, grouped_benchmark, load_core_kernels):
    et = cyice.str2et("July 4, 2003 11:00 AM PST")
    grouped_benchmark(function, "Mars", et, "J2000", "LT+S", "Earth")
    state, lt = function("Mars", et, "J2000", "LT+S", "Earth")
    assert isinstance(state, np.ndarray)


@pytest.mark.parametrize('function', [cyice.spkezr_v, spice.spkezr], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkezr_v"], indirect=True)
def test_perf_spkezr_v(function, grouped_benchmark, load_core_kernels):
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


@pytest.mark.parametrize('function', [cyice.spkpos, spice.spkpos], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkpos"], indirect=True)
def test_perf_spkpos(function, grouped_benchmark, load_core_kernels):
    et = cyice.str2et("July 4, 2003 11:00 AM PST")
    grouped_benchmark(function, "Mars", et, "J2000", "LT+S", "Earth")


@pytest.mark.parametrize('function', [cyice.spkpos_v, spice.spkpos], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkpos_v"], indirect=True)
def test_perf_spkpos_v(function, grouped_benchmark, load_core_kernels):
    _et = spice.str2et(["July 4, 2003 11:00 AM PST", "July 11, 2003 11:10 AM PST"])
    et = np.linspace(_et[0], _et[1], num=100)
    grouped_benchmark(function, "Mars", et, "J2000", "LT+S", "Earth")
    ptargs, lts = function("Mars", et, "J2000", "LT+S", "Earth")
    assert isinstance(ptargs, np.ndarray)


@pytest.mark.parametrize('function', [cyice.str2et, spice.str2et], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["str2et"], indirect=True)
def test_perf_str2et(function, grouped_benchmark, load_core_kernels):
    grouped_benchmark(function, "Thu Mar 20 12:53:29 PST 1997")


@pytest.mark.parametrize('function', [cyice.str2et_v, spice.str2et], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["str2et_v"], indirect=True)
def test_perf_str2et_v(function, grouped_benchmark, load_core_kernels):
    date = "Thu Mar 20 12:53:29 PST 1997"
    dates = np.array([date] * 100, dtype=np.str_)
    grouped_benchmark(function, dates)
    expected_ets = np.ones(100) * -87836728.81438904
    ets = function(dates)
    assert isinstance(ets, np.ndarray)
    npt.assert_array_almost_equal(ets, expected_ets)


@pytest.mark.parametrize('function', [cyice.sxform, spice.sxform], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sxform"], indirect=True)
def test_perf_sxform(function, grouped_benchmark, load_core_kernels):
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


@pytest.mark.parametrize('function', [cyice.sxform_v, spice.sxform], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sxform_v"], indirect=True)
def test_perf_sxform_v(function, grouped_benchmark, load_core_kernels):
    et = np.repeat(spice.str2et("January 1, 1990"), 1000)
    grouped_benchmark(function, "IAU_EARTH", "J2000", et)
    res = function("IAU_EARTH", "J2000", et)
    assert isinstance(res, np.ndarray)


@pytest.mark.parametrize('function', [cyice.tangpt, spice.tangpt], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["tangpt"], indirect=True)
def test_perf_tangpt(function, grouped_benchmark, load_core_kernels):
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


@pytest.mark.parametrize('function', [cyice.trgsep, spice.trgsep], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["trgsep"], indirect=True)
def test_perf_trgsep(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("2007-JAN-11 11:21:20.213872 (TDB)")
    grouped_benchmark(function, et, "MOON", "POINT", "IAU_MOON", "EARTH", "POINT", "IAU_EARTH", "SUN", "LT+S")
    point_sep = function(et, "MOON", "POINT", "IAU_MOON", "EARTH", "POINT", "IAU_EARTH", "SUN", "LT+S")
    assert spice.dpr() * point_sep == pytest.approx(0.15729276)


@pytest.mark.parametrize('function', [cyice.trgsep_v,], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["trgsep_v"], indirect=True)
def test_perf_trgsep_v(function, grouped_benchmark, load_core_kernels):
    ets = np.repeat(spice.str2et("2007-JAN-11 11:21:20.213872 (TDB)"),100)
    grouped_benchmark(function, ets, "MOON", "POINT", "IAU_MOON", "EARTH", "POINT", "IAU_EARTH", "SUN", "LT+S")  
    res = function(ets, "MOON", "POINT", "IAU_MOON", "EARTH", "POINT", "IAU_EARTH", "SUN", "LT+S")
    assert isinstance(res, np.ndarray)


@pytest.mark.parametrize('function', [cyice.unitim, spice.unitim], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["unitim"], indirect=True)
def test_perf_unitim(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("Dec 19 2003")
    grouped_benchmark(function, et, "ET", "JED")
    # correctness assertion can be performed before or after
    converted_et = function(et, "ET", "JED")
    npt.assert_almost_equal(converted_et, 2452992.5007428653)


@pytest.mark.parametrize('function', [cyice.unitim_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["unitim_v"], indirect=True)
def test_perf_unitim_v(function, grouped_benchmark, load_core_kernels):
    ets = np.repeat(spice.str2et("Dec 19 2003"), 100)
    grouped_benchmark(function, ets, "ET", "JED")
    res = function(ets, "ET", "JED")
    assert isinstance(res, np.ndarray)


@pytest.mark.parametrize('function', [cyice.utc2et, spice.utc2et], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["utc2et"], indirect=True)
def test_perf_utc2et(function, grouped_benchmark, load_core_kernels):
    grouped_benchmark(function, "December 1, 2004 15:04:11")
    assert function("December 1, 2004 15:04:11") == 155185515.1831043


@pytest.mark.parametrize('function', [cyice.utc2et_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["utc2et_v"], indirect=True)
def test_perf_utc2et_v(function, grouped_benchmark, load_core_kernels):
    date = "December 1, 2004 15:04:11"
    dates = np.array([date] * 100, dtype=np.str_)
    grouped_benchmark(function, dates)
    res = function(dates)
    assert isinstance(res, np.ndarray)