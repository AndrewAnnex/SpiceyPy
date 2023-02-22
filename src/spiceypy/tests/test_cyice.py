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


def test_et2utc_v():
    spice.furnsh(CoreKernels.testMetaKernel)
    et = -527644192.5403653
    output = cyice.et2utc_v2(np.array([et] * 100), "J", 6)
    assert np.array_equal(
        output,
        np.array(["JD 2445438.006415"] * 100),
    )


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


def test_str2et_v():
    spice.furnsh(CoreKernels.testMetaKernel)
    date = "Thu Mar 20 12:53:29 PST 1997"
    expected_ets = np.ones(100) * -87836728.81438904
    dates = np.array([date] * 100, dtype=np.string_)
    print(dates.shape, dates.dtype, flush=True)
    ets = cyice.str2et_v(dates)
    npt.assert_array_almost_equal(ets, expected_ets)
