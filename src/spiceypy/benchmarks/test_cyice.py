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

# https://pytest-benchmark.readthedocs.io/en/latest/pedantic.html

@pytest.fixture(autouse=True)
def clear_kernel_pool_and_reset():
    spice.kclear()
    spice.reset()
    # yield for test
    yield
    # clear kernel pool again
    spice.kclear()
    spice.reset()


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


@pytest.mark.parametrize('function', [cyice.b1900, spice.b1900])
def test_perf_b1900(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
    benchmark(function)


def test_cyice_convrt_correctness():
    assert cyice.convrt(300.0, "statute_miles", "km") == 482.80320


@pytest.mark.parametrize('function', [cyice.convrt, spice.convrt])
def test_perf_convrt(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
    benchmark(function, 1.0, "parsecs", "lightyears")


@pytest.mark.parametrize('function', [cyice.convrt_v, spice.convrt])
def test_perf_convrt_v(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
    data = np.arange(0, 1000.0, dtype=float)
    benchmark(function, data, "parsecs", "lightyears")


@pytest.mark.parametrize('function', [cyice.deltet, spice.deltet])
def test_perf_deltet(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
    spice.furnsh(CoreKernels.testMetaKernel)
    et_2004 = spice.str2et("Jan 1 2004")
    benchmark(function, et_2004, "ET")


@pytest.mark.parametrize('function', [cyice.deltet_v])
def test_perf_deltet_v(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
    spice.furnsh(CoreKernels.testMetaKernel)
    ets_2004 = np.repeat(spice.str2et("Jan 1 2004"), 100)
    benchmark(function, ets_2004, "ET")


def test_cyice_et2utc_v_correctness():
    spice.furnsh(CoreKernels.testMetaKernel)
    et = -527644192.5403653
    output = cyice.et2utc_v(np.array([et] * 100), "J", 6)
    assert np.array_equal(
        output,
        np.array(["JD 2445438.006415"] * 100),
    )


@pytest.mark.parametrize('function', [cyice.et2utc, spice.et2utc])
def test_perf_et2utc(function, benchmark):
    spice.furnsh(CoreKernels.testMetaKernel)
    benchmark.group = '%s - perf' % get_qualified_name(function)
    benchmark(function,  -527644192.5403653, "J", 6)


@pytest.mark.parametrize('function', [cyice.et2utc_v, spice.et2utc])
def test_perf_et2utc_v(function, benchmark):
    spice.furnsh(CoreKernels.testMetaKernel)
    ets = np.array([-527644192.5403653] * 10000)
    benchmark.group = '%s - perf' % get_qualified_name(function)
    benchmark(function, ets, "J", 6)


@pytest.mark.parametrize('function', [cyice.etcal, spice.etcal])
def test_perf_etcal(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
    benchmark(function, 0.0)


@pytest.mark.parametrize('function', [cyice.etcal_v, spice.etcal])
def test_perf_etcal_v(function, benchmark):
    data = np.arange(10000.0, dtype=float)
    benchmark.group = '%s - perf' % get_qualified_name(function)
    benchmark(function, data)


@pytest.mark.parametrize('function', [cyice.failed, spice.failed])
def test_perf_failed(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
    benchmark(function)


@pytest.mark.parametrize('function', [cyice.fovray, spice.fovray])
def test_perf_fovray(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
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
    raydir = np.array([0.0, 0.0, 1.0])
    benchmark(function, "CASSINI_ISS_NAC", raydir, frame, "S", "CASSINI", et)


@pytest.mark.parametrize('function', [cyice.fovtrg, spice.fovtrg])
def test_perf_fovtrg(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
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
    benchmark(function,
        "CASSINI_ISS_NAC",
        "Enceladus",
        "Ellipsoid",
        "IAU_ENCELADUS",
        "LT+S",
        "CASSINI",
        et,
    )


@pytest.mark.parametrize('function', [cyice.lspcn, spice.lspcn])
def test_perf_lspcn(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("21 march 2005")
    benchmark(function, "EARTH", et, "NONE")





def test_cyice_spkcvt_correctness():
    spice.furnsh(ExtraKernels.earthStnSpk)
    spice.furnsh(ExtraKernels.earthHighPerPck)
    spice.furnsh(ExtraKernels.earthTopoTf)
    spice.furnsh(CoreKernels.testMetaKernel)
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
    npt.assert_array_almost_equal(state, expected_state, decimal=6)


@pytest.mark.parametrize('function', [cyice.spkcvt, spice.spkcvt])
def test_perf_spkcvt(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
    spice.furnsh(ExtraKernels.earthStnSpk)
    spice.furnsh(ExtraKernels.earthHighPerPck)
    spice.furnsh(ExtraKernels.earthTopoTf)
    spice.furnsh(CoreKernels.testMetaKernel)
    obstime = spice.str2et("2003 Oct 13 06:00:00")
    trgstate = np.array([
        -2353.6213656676991,
        -4641.3414911499403,
        3677.0523293197439,
        -0.00000000000057086,
        0.00000000000020549,
        -0.00000000000012171,
    ])
    benchmark(function, trgstate, 0.0, "EARTH", "ITRF93", obstime, "ITRF93", "TARGET", "CN+S", "SUN")


@pytest.mark.parametrize('function', [cyice.reset, spice.reset])
def test_perf_reset(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
    benchmark(function)


@pytest.mark.parametrize('function', [cyice.scdecd, spice.scdecd])
def test_perf_scdecd(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.voyagerSclk)
    timein = spice.scencd(-32, "2/20538:39:768")
    benchmark(function, -32, timein)


@pytest.mark.parametrize('function', [cyice.scencd, spice.scencd])
def test_perf_scencd(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.voyagerSclk)
    benchmark(function, -32,  "2/20538:39:768")


@pytest.mark.parametrize('function', [cyice.sce2c, spice.sce2c])
def test_perf_sce2c(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.voyagerSclk)
    et = spice.str2et("1979 JUL 05 21:50:21.23379")
    benchmark(function, -32, et)

@pytest.mark.skip(reason="broken")
@pytest.mark.parametrize('function', [cyice.sce2s, spice.sce2s])
def test_perf_sce2s(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.voyagerSclk)
    et = spice.str2et("1979 JUL 05 21:50:21.23379")
    benchmark(function, -32, et)


@pytest.mark.parametrize('function', [cyice.scs2e, spice.scs2e])
def test_perf_scs2e(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.voyagerSclk)
    benchmark(function, -32, "2/20538:39:768")


@pytest.mark.parametrize('function', [cyice.sct2e, spice.sct2e])
def test_perf_sct2e(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.voyagerSclk)
    benchmark(function, -32,  985327965.0)

# def test_getmsg_cyice_benchmark(benchmark):
#     cyice.reset()
#     spice.sigerr("test error")
#     benchmark(cyice.getmsg, "SHORT", 200)
#     cyice.reset()


# def test_getmsg_spiceypy_benchmark(benchmark):
#     spice.reset()
#     spice.sigerr("test error")
#     benchmark(spice.getmsg, "SHORT", 200)
#     spice.reset()


# def test_qcktrc():
#     cyice.reset()
#     spice.chkin("test")
#     spice.chkin("qcktrc")
#     trace = cyice.qcktrc(40)
#     assert trace == "test --> qcktrc"
#     spice.chkout("qcktrc")
#     spice.chkout("test")
#     cyice.reset()


# def test_qcktrc_cyice_benchmark(benchmark):
#     cyice.reset()
#     spice.chkin("test")
#     spice.chkin("qcktrc")
#     benchmark(cyice.qcktrc, 40)
#     spice.chkout("qcktrc")
#     spice.chkout("test")
#     cyice.reset()


# def test_qcktrc_spiceypy_benchmark(benchmark):
#     spice.reset()
#     spice.chkin("test")
#     spice.chkin("qcktrc")
#     benchmark(spice.qcktrc, 40)
#     spice.chkout("qcktrc")
#     spice.chkout("test")
#     spice.reset()


@pytest.mark.parametrize('function', [cyice.spkez, spice.spkez])
def test_perf_spkez(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
    spice.furnsh(CoreKernels.testMetaKernel)
    et = cyice.str2et("July 4, 2003 11:00 AM PST")
    benchmark(function, 499, et, "J2000", "LT+S", 399)


def test_cyice_spkez_v_correctness():
    spice.furnsh(CoreKernels.testMetaKernel)
    et = np.full((100,), spice.str2et("July 4, 2003 11:00 AM PST"))
    state, lt = cyice.spkez_v(499, et, "J2000", "LT+S", 399)
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


@pytest.mark.parametrize('function', [cyice.spkezr, spice.spkezr])
def test_perf_spkezr(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
    spice.furnsh(CoreKernels.testMetaKernel)
    et = cyice.str2et("July 4, 2003 11:00 AM PST")
    benchmark(function, "Mars", et, "J2000", "LT+S", "Earth")


@pytest.mark.parametrize('function', [cyice.spkezr_v, spice.spkezr])
def test_perf_spkezr_v(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
    spice.furnsh(CoreKernels.testMetaKernel)
    et = np.full((100,), spice.str2et("July 4, 2003 11:00 AM PST"))
    benchmark(function, "Mars", et, "J2000", "LT+S", "Earth")


def test_spkpos_v_correctness():
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et(["July 4, 2003 11:00 AM PST", "July 11, 2003 11:00 AM PST"])
    pos, lt = cyice.spkpos_v("Mars", et, "J2000", "LT+S", "Earth")
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


@pytest.mark.parametrize('function', [cyice.spkpos, spice.spkpos])
def test_perf_spkpos(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
    spice.furnsh(CoreKernels.testMetaKernel)
    et = cyice.str2et("July 4, 2003 11:00 AM PST")
    benchmark(function, "Mars", et, "J2000", "LT+S", "Earth")


def test_str2et_v_correctness():
    spice.furnsh(CoreKernels.testMetaKernel)
    date = "Thu Mar 20 12:53:29 PST 1997"
    expected_ets = np.ones(100) * -87836728.81438904
    dates = np.array([date] * 100, dtype=np.str_)
    print(dates.shape, dates.dtype, flush=True)
    ets = cyice.str2et_v(dates)
    npt.assert_array_almost_equal(ets, expected_ets)


@pytest.mark.parametrize('function', [cyice.str2et, spice.str2et])
def test_perf_str2et(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
    spice.furnsh(CoreKernels.testMetaKernel)
    benchmark(function, "Thu Mar 20 12:53:29 PST 1997")


@pytest.mark.parametrize('function', [cyice.str2et_v, spice.str2et])
def test_perf_str2et_v(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
    spice.furnsh(CoreKernels.testMetaKernel)
    date = "Thu Mar 20 12:53:29 PST 1997"
    dates = np.array([date] * 100, dtype=np.str_)
    benchmark(function, dates)


def test_cyice_sxform_correctness():
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
    xform = cyice.sxform("IAU_EARTH", "J2000", et)
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


@pytest.mark.parametrize('function', [cyice.sxform, spice.sxform])
def test_perf_sxform(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("January 1, 1990")
    benchmark(function, "IAU_EARTH", "J2000", et)


@pytest.mark.parametrize('function', [cyice.sxform_v, spice.sxform])
def test_perf_sxform_v(function, benchmark):
    benchmark.group = '%s - v - perf' % get_qualified_name(function)
    spice.furnsh(CoreKernels.testMetaKernel)
    et = np.repeat(spice.str2et("January 1, 1990"), 1000)
    benchmark(function, "IAU_EARTH", "J2000", et)


@pytest.mark.parametrize('function', [cyice.utc2et, spice.utc2et])
def test_perf_utc2et(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
    spice.furnsh(CoreKernels.testMetaKernel)
    benchmark(function, "December 1, 2004 15:04:11")


@pytest.mark.parametrize('function', [cyice.utc2et_v])
def test_perf_utc2et_v(function, benchmark):
    benchmark.group = '%s - perf' % get_qualified_name(function)
    spice.furnsh(CoreKernels.testMetaKernel)
    date = "December 1, 2004 15:04:11"
    dates = np.array([date] * 100, dtype=np.str_)
    benchmark(function, dates)