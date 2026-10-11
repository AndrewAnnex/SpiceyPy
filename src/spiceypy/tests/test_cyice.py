"""
Unit tests for cyice top-level function dispatching.

The top-level cyice functions (no _s/_v suffix) inspect their key argument
and route to the scalar (_s) or vectorized (_v) implementation. These tests
verify that routing for the input types users are likely to pass: Python
scalars, numpy scalars, 0-d numpy arrays, and 1-d numpy arrays. They also
cover the ndim guards on the string-input _v functions.

Benchmark coverage for the same functions lives in
spiceypy/benchmarks/test_cyice.py; this file is only for
dispatch correctness.
"""

import numpy as np
import numpy.testing as npt
import pytest

import spiceypy as spice
from spiceypy import cyice
from spiceypy.tests.gettestkernels import (
    download_kernels,
    CoreKernels,
    ExtraKernels,
)


def setup_module(module):
    download_kernels()


@pytest.fixture
def load_core_kernels():
    spice.furnsh(CoreKernels.testMetaKernel)


@pytest.fixture
def load_voyager_kernels():
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.voyagerSclk)


@pytest.fixture(autouse=True)
def clear_kernel_pool_and_reset():
    spice.kclear()
    spice.reset()
    yield
    spice.kclear()
    spice.reset()


# constructors producing every scalar-like numeric form a user might pass
# to a double-valued dispatch argument like et
numeric_scalar_ctors = [
    pytest.param(float, id="py_float"),
    pytest.param(np.float64, id="np_float64"),
    pytest.param(np.float32, id="np_float32"),
    pytest.param(np.array, id="ndarray_0d_f8"),
    pytest.param(lambda x: np.array(x, dtype=np.float32), id="ndarray_0d_f4"),
    pytest.param(lambda x: int(x), id="py_int"),
    pytest.param(lambda x: np.int64(x), id="np_int64"),
    pytest.param(lambda x: np.array(int(x), dtype=np.int64), id="ndarray_0d_i8"),
]

# constructors producing every scalar-like string form
string_scalar_ctors = [
    pytest.param(str, id="py_str"),
    pytest.param(np.str_, id="np_str"),
    pytest.param(np.array, id="ndarray_0d_U"),
    pytest.param(lambda s: np.array(s.encode("ascii")), id="ndarray_0d_S"),
    pytest.param(lambda s: np.array(s, dtype=object), id="ndarray_0d_object"),
]


@pytest.mark.parametrize("ctor", numeric_scalar_ctors)
def test_etcal_scalar_dispatch(ctor):
    et = ctor(0.0)
    result = cyice.etcal(et)
    assert isinstance(result, str)
    assert result == cyice.etcal_s(float(et))


def test_etcal_vectorized_dispatch():
    ets = np.zeros(3, dtype=np.double)
    result = cyice.etcal(ets)
    assert isinstance(result, np.ndarray)
    assert result.shape == (3,)


@pytest.mark.parametrize("ctor", numeric_scalar_ctors)
def test_spkssb_scalar_dispatch(ctor, load_core_kernels):
    et = ctor(cyice.str2et("July 4, 2003 11:00 AM PST"))
    state = cyice.spkssb(499, et, "J2000")
    assert isinstance(state, np.ndarray)
    assert state.shape == (6,)
    npt.assert_array_equal(state, cyice.spkssb_s(499, float(et), "J2000"))


def test_spkssb_vectorized_dispatch(load_core_kernels):
    ets = np.full(4, cyice.str2et("July 4, 2003 11:00 AM PST"))
    state = cyice.spkssb(499, ets, "J2000")
    assert isinstance(state, np.ndarray)
    assert state.shape == (4, 6)


# getelm dispatches on an integer argument (frstyr)

tle_lines = np.array(
    [
        "1 44420U 19036AC  19311.70264562  .00005403  00000-0  12176-2 0  9991",
        "2 44420  24.0060  72.9267 0016343 241.6999 118.1833 14.53580129 17852",
    ]
)


@pytest.mark.parametrize(
    "ctor",
    [
        pytest.param(int, id="py_int"),
        pytest.param(np.int64, id="np_int64"),
        pytest.param(np.int32, id="np_int32"),
        pytest.param(lambda x: np.array(x, dtype=np.int64), id="ndarray_0d_i8"),
    ],
)
def test_getelm_scalar_dispatch(ctor, load_core_kernels):
    epoch, elems = cyice.getelm(ctor(2019), tle_lines)
    expected_epoch, expected_elems = cyice.getelm_s(2019, tle_lines)
    assert epoch == expected_epoch
    npt.assert_array_equal(elems, expected_elems)


# string-dispatching functions: str2et, utc2et, scencd, scs2e


@pytest.mark.parametrize("ctor", string_scalar_ctors)
def test_str2et_scalar_dispatch(ctor, load_core_kernels):
    et = cyice.str2et(ctor("July 4, 2003 11:00 AM PST"))
    assert isinstance(et, float)
    assert et == cyice.str2et_s("July 4, 2003 11:00 AM PST")


def test_str2et_vectorized_dispatch(load_core_kernels):
    ets = cyice.str2et(np.repeat("July 4, 2003 11:00 AM PST", 3))
    assert isinstance(ets, np.ndarray)
    assert ets.shape == (3,)


@pytest.mark.parametrize("ctor", string_scalar_ctors)
def test_utc2et_scalar_dispatch(ctor, load_core_kernels):
    et = cyice.utc2et(ctor("July 4, 2003"))
    assert isinstance(et, float)
    assert et == cyice.utc2et_s("July 4, 2003")


def test_utc2et_vectorized_dispatch(load_core_kernels):
    ets = cyice.utc2et(np.repeat("July 4, 2003", 3))
    assert isinstance(ets, np.ndarray)
    assert ets.shape == (3,)


@pytest.mark.parametrize("ctor", string_scalar_ctors)
def test_scencd_scalar_dispatch(ctor, load_voyager_kernels):
    sclkdp = cyice.scencd(-32, ctor("2/20538:39:768"))
    assert isinstance(sclkdp, float)
    assert sclkdp == cyice.scencd_s(-32, "2/20538:39:768")


@pytest.mark.parametrize("ctor", string_scalar_ctors)
def test_scs2e_scalar_dispatch(ctor, load_voyager_kernels):
    et = cyice.scs2e(-32, ctor("2/20538:39:768"))
    assert isinstance(et, float)
    assert et == cyice.scs2e_s(-32, "2/20538:39:768")


# ndim guards: the string _v functions must reject non-1-d input with a
# ValueError rather than reading past the dims array (previously a segfault)

string_v_calls = [
    pytest.param(lambda arr: cyice.str2et_v(arr), id="str2et_v"),
    pytest.param(lambda arr: cyice.utc2et_v(arr), id="utc2et_v"),
    pytest.param(lambda arr: cyice.scencd_v(-32, arr), id="scencd_v"),
    pytest.param(lambda arr: cyice.scs2e_v(-32, arr), id="scs2e_v"),
]


@pytest.mark.parametrize("call", string_v_calls)
def test_string_v_rejects_0d(call):
    with pytest.raises(ValueError, match="expected a 1-D array"):
        call(np.array("2/20538:39:768"))


@pytest.mark.parametrize("call", string_v_calls)
def test_string_v_rejects_2d(call):
    with pytest.raises(ValueError, match="expected a 1-D array"):
        call(np.array([["a", "b"], ["c", "d"]]))


def test_numeric_v_rejects_0d():
    # memoryview-typed _v functions reject 0-d arrays at the buffer protocol
    with pytest.raises((ValueError, TypeError)):
        cyice.etcal_v(np.array(0.0))


def test_aux_string_params_accept_np_str(load_core_kernels):
    et = cyice.str2et("July 4, 2003 11:00 AM PST")
    state, lt = cyice.spkezr(
        np.str_("MARS"), et, np.str_("J2000"), np.str_("NONE"), np.str_("EARTH")
    )
    expected_state, expected_lt = cyice.spkezr("MARS", et, "J2000", "NONE", "EARTH")
    npt.assert_array_equal(state, expected_state)
    assert lt == expected_lt


def test_timout_pictur_accepts_np_str_and_bytes(load_core_kernels):
    expected = cyice.timout(0.0, "YYYY Mon DD")
    assert cyice.timout(0.0, np.str_("YYYY Mon DD")) == expected
    assert cyice.timout(0.0, b"YYYY Mon DD") == expected


def test_furnsh_accepts_np_str():
    cyice.furnsh(np.str_(CoreKernels.testMetaKernel))
    assert spice.ktotal("ALL") > 0


def test_string_dispatch_rejects_0d_numeric():
    with pytest.raises(TypeError):
        cyice.str2et(np.array(5.0))


def test_numeric_dispatch_rejects_0d_string(load_core_kernels):
    # a 0-d string array is not a numeric scalar, so it routes to _v,
    # which rejects it via the buffer protocol
    with pytest.raises((ValueError, TypeError)):
        cyice.spkssb(499, np.array("not a time"), "J2000")
