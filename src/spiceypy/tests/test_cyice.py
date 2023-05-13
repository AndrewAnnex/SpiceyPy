import os

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


def test_b1900():
    assert cyice.b1900() == 2415020.31352


def test_b1900_cyice_benchmark(benchmark):
    benchmark(cyice.b1900)


def test_b1900_spiceypy_benchmark(benchmark):
    benchmark(spice.b1900)


def test_convrt():
    assert cyice.convrt(300.0, "statute_miles", "km") == 482.80320


def test_convrt_cyice_benchmark(benchmark):
    benchmark(cyice.convrt, 1.0, "parsecs", "lightyears")


def test_convrt_spiceypy_benchmark(benchmark):
    benchmark(spice.convrt, 1.0, "parsecs", "lightyears")


def test_convrt_cyice_v_benchmark(benchmark):
    data = np.arange(0, 1000.0, dtype=float)
    benchmark(cyice.convrt_v, data, "parsecs", "lightyears")


def test_convrt_spiceypy_v_benchmark(benchmark):
    data = np.arange(0, 1000.0, dtype=float)
    benchmark(spice.convrt, data, "parsecs", "lightyears")


def test_et2utc_v():
    spice.furnsh(CoreKernels.testMetaKernel)
    et = -527644192.5403653
    output = cyice.et2utc_v(np.array([et] * 100), "J", 6)
    assert np.array_equal(
        output,
        np.array(["JD 2445438.006415"] * 100),
    )


def test_et2utc_cyice_benchmark(benchmark):
    spice.furnsh(CoreKernels.testMetaKernel)
    benchmark(cyice.et2utc, -527644192.5403653, "J", 6)


def test_et2utc_spiceypy_benchmark(benchmark):
    spice.furnsh(CoreKernels.testMetaKernel)
    benchmark(spice.et2utc, -527644192.5403653, "J", 6)


def test_etcal_cyice_benchmark(benchmark):
    benchmark(cyice.etcal, 0.0)


def test_etcal_v_cyice_benchmark(benchmark):
    data = np.arange(1000.0, dtype=float)
    benchmark(cyice.etcal_v, data)


def test_etcal_spiceypy_benchmark(benchmark):
    benchmark(spice.etcal, 0.0)


def test_etcal_v_spiceypy_benchmark(benchmark):
    data = np.arange(1000.0, dtype=float)
    benchmark(spice.etcal, data)


def test_failed_cyice_benchmark(benchmark):
    benchmark(cyice.failed)


def test_failed_spiceypy_benchmark(benchmark):
    benchmark(spice.failed)


def test_getmsg_cyice_benchmark(benchmark):
    cyice.reset()
    spice.sigerr("test error")
    benchmark(cyice.getmsg, "SHORT", 200)
    cyice.reset()


def test_getmsg_spiceypy_benchmark(benchmark):
    spice.reset()
    spice.sigerr("test error")
    benchmark(spice.getmsg, "SHORT", 200)
    spice.reset()


def test_qcktrc():
    cyice.reset()
    spice.chkin("test")
    spice.chkin("qcktrc")
    trace = cyice.qcktrc(40)
    assert trace == "test --> qcktrc"
    cyice.reset()


def test_qcktrc_cyice_benchmark(benchmark):
    cyice.reset()
    spice.chkin("test")
    spice.chkin("qcktrc")
    benchmark(cyice.qcktrc, 40)
    cyice.reset()


def test_qcktrc_spiceypy_benchmark(benchmark):
    spice.reset()
    spice.chkin("test")
    spice.chkin("qcktrc")
    benchmark(spice.qcktrc, 40)
    spice.reset()


def test_reset_cyice_benchmark(benchmark):
    benchmark(cyice.reset)


def test_reset_spiceypy_benchmark(benchmark):
    benchmark(spice.reset)


def test_spkez_cyice_benchmark(benchmark):
    spice.furnsh(CoreKernels.testMetaKernel)
    et = cyice.str2et("July 4, 2003 11:00 AM PST")
    benchmark(cyice.spkez, 499, et, "J2000", "LT+S", 399)


def test_spkez_spiceypy_benchmark(benchmark):
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("July 4, 2003 11:00 AM PST")
    benchmark(spice.spkez, 499, et, "J2000", "LT+S", 399)


def test_spkezr_v():
    spice.furnsh(CoreKernels.testMetaKernel)
    et = np.full((100,), spice.str2et("July 4, 2003 11:00 AM PST"))
    state, lt = cyice.spkezr_v("Mars", et, "J2000", "LT+S", "Earth")
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


def test_spkezr_cyice_benchmark(benchmark):
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("July 4, 2003 11:00 AM PST")
    benchmark(cyice.spkezr, "Mars", et, "J2000", "LT+S", "Earth")


def test_spkezr_spiceypy_benchmark(benchmark):
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("July 4, 2003 11:00 AM PST")
    benchmark(spice.spkezr, "Mars", et, "J2000", "LT+S", "Earth")


def test_spkpos_v():
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


def test_spkpos_cyice_benchmark(benchmark):
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("July 4, 2003 11:00 AM PST")
    benchmark(cyice.spkpos, "Mars", et, "J2000", "LT+S", "Earth")


def test_spkpos_spiceypy_benchmark(benchmark):
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("July 4, 2003 11:00 AM PST")
    benchmark(spice.spkpos, "Mars", et, "J2000", "LT+S", "Earth")


def test_str2et_v():
    spice.furnsh(CoreKernels.testMetaKernel)
    date = "Thu Mar 20 12:53:29 PST 1997"
    expected_ets = np.ones(100) * -87836728.81438904
    dates = np.array([date] * 100, dtype=np.string_)
    print(dates.shape, dates.dtype, flush=True)
    ets = cyice.str2et_v(dates)
    npt.assert_array_almost_equal(ets, expected_ets)


def test_str2et_cyice_benchmark(benchmark):
    spice.furnsh(CoreKernels.testMetaKernel)
    benchmark(cyice.str2et, "Thu Mar 20 12:53:29 PST 1997")


def test_str2et_spiceypy_benchmark(benchmark):
    spice.furnsh(CoreKernels.testMetaKernel)
    benchmark(spice.str2et, "Thu Mar 20 12:53:29 PST 1997")


def test_sxform():
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
    with pytest.raises(AssertionError):
        npt.assert_array_almost_equal(jstate, expected, decimal=4)


def test_sxform_cyice_benchmark(benchmark):
    spice.furnsh(CoreKernels.testMetaKernel)
    utc1 = "January 1, 1990"
    et = spice.str2et(utc1)
    benchmark(cyice.sxform, "IAU_EARTH", "J2000", et)


def test_sxform_spiceypy_benchmark(benchmark):
    spice.furnsh(CoreKernels.testMetaKernel)
    utc1 = "January 1, 1990"
    et = spice.str2et(utc1)
    benchmark(spice.sxform, "IAU_EARTH", "J2000", et)


def test_sxform_v_cyice_benchmark(benchmark):
    spice.furnsh(CoreKernels.testMetaKernel)
    utc1 = "January 1, 1990"
    et = spice.str2et(utc1)
    ets = np.repeat(et, 1000)
    benchmark(cyice.sxform_v, "IAU_EARTH", "J2000", ets)


def test_sxform_v_spiceypy_benchmark(benchmark):
    spice.furnsh(CoreKernels.testMetaKernel)
    utc1 = "January 1, 1990"
    et = spice.str2et(utc1)
    ets = np.repeat(et, 1000)
    benchmark(spice.sxform, "IAU_EARTH", "J2000", ets)


def test_utc2et_cyice_benchmark(benchmark):
    spice.furnsh(CoreKernels.testMetaKernel)
    benchmark(cyice.utc2et, "December 1, 2004 15:04:11")


def test_utc2et_spiceypy_benchmark(benchmark):
    spice.furnsh(CoreKernels.testMetaKernel)
    benchmark(spice.utc2et, "December 1, 2004 15:04:11")
