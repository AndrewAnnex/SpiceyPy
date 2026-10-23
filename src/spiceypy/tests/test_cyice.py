"""
Unit tests for cyice top-level function dispatching and error handling.

The top-level cyice functions (no _s/_v suffix) inspect their key argument
and route to the scalar (_s) or vectorized (_v) implementation. These tests
verify that routing for the input types users are likely to pass: Python
scalars, numpy scalars, 0-d numpy arrays, and 1-d numpy arrays. They also
cover the ndim guards on the string-input _v functions.

Benchmark coverage for the same functions lives in
spiceypy/benchmarks/test_cyice.py.
"""

import numpy as np
import numpy.testing as npt
import pytest

import spiceypy as spice
from spiceypy import cyice
from spiceypy.utils.exceptions import (
    SpiceEMPTYSTRING,
    SpiceIDCODENOTFOUND,
    SpiceKERNELVARNOTFOUND,
    SpiceORBITDECAY,
    SpiceVALUEOUTOFRANGE,
)
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
    spice.reset()
    spice.kclear()
    yield
    spice.reset()
    spice.kclear()


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


@pytest.mark.parametrize("function", [cyice.getelm_v, cyice.getelm])
@pytest.mark.parametrize(
    "frstyr",
    [
        pytest.param(np.full(3, 2019, dtype=np.int64), id="ndarray_i8"),
        pytest.param(np.full(3, 2019, dtype=np.int32), id="ndarray_i4"),
        pytest.param(np.full(6, 2019, dtype=np.int64)[::2], id="ndarray_i8_strided"),
    ],
)
def test_getelm_vector_int_dtypes(function, frstyr, load_core_kernels):
    lines = np.array([tle_lines] * 3)
    epochs, elems = function(frstyr, lines)
    expected_epoch, expected_elems = spice.getelm(2019, tle_lines)
    npt.assert_array_equal(epochs, np.full(3, expected_epoch))
    npt.assert_array_equal(elems, np.repeat(expected_elems[None, :], 3, axis=0))


@pytest.mark.parametrize("function", [cyice.xfmsta_v, cyice.xfmsta])
@pytest.mark.parametrize("writable", [False, True])
def test_xfmsta_batch_preserves_input_states(function, writable):
    states = np.array(
        [
            [7000.0, 1200.0, 2000.0, 1.0, 7.0, 0.3],
            [7100.0, 1300.0, 2100.0, 1.1, 7.1, 0.4],
        ]
    )
    original = states.copy()
    states.flags.writeable = writable
    expected = np.array(
        [
            spice.xfmsta(state, "RECTANGULAR", "LATITUDINAL", "EARTH")
            for state in original
        ]
    )
    actual = function(states, "RECTANGULAR", "LATITUDINAL", "EARTH")
    npt.assert_array_equal(actual, expected)
    npt.assert_array_equal(states, original)
    assert states.flags.writeable == writable


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


@pytest.fixture
def decaying_satellite(load_core_kernels):
    spice.furnsh(ExtraKernels.geophKer)
    # SL-14 debris from Vallado's SGP4 verification data.
    line1 = "1 29141U 85108AA  06170.26783845  .99999999  00000-0  13519-0 0   718"
    line2 = "2 29141  82.4288 273.4882 0015848 277.2124  83.9133 15.93343074  6828"
    tle = [line1, line2]
    names = ["J2", "J3", "J4", "KE", "QO", "SO", "ER", "AE"]
    geophs = np.array([spice.bodvcd(399, name, 1)[1] for name in names]).ravel()
    epoch, elems = spice.getelm(1957, tle)
    return epoch, geophs, elems


@pytest.mark.parametrize("function", [cyice.evsgp4_s, cyice.evsgp4])
def test_evsgp4_scalar_error_recovery(function, decaying_satellite):
    epoch, geophs, elems = decaying_satellite
    with pytest.raises(SpiceORBITDECAY):
        function(epoch + 440 * 60, geophs, elems)
    assert not spice.failed()
    npt.assert_array_equal(
        function(epoch, geophs, elems), spice.evsgp4(epoch, geophs, elems)
    )


@pytest.mark.parametrize("function", [cyice.evsgp4_v, cyice.evsgp4])
@pytest.mark.parametrize("error_index", [0, 1, 2])
def test_evsgp4_vector_error_recovery(function, error_index, decaying_satellite):
    epoch, geophs, elems = decaying_satellite
    ets = np.full(3, epoch)
    ets[error_index] += 440 * 60
    elements = np.repeat(elems[None, :], 3, axis=0)
    with pytest.raises(SpiceORBITDECAY):
        function(ets, geophs, elements)
    assert not spice.failed()
    ets[error_index] = epoch
    expected = np.repeat(spice.evsgp4(epoch, geophs, elems)[None, :], 3, axis=0)
    npt.assert_array_equal(function(ets, geophs, elements), expected)


rect = np.array([1000.0, 2000.0, 3000.0])
rects = np.array([rect, rect * 2.0, rect * 3.0])
lons = np.array([0.1, 0.2, 0.3])
lats = np.array([0.4, 0.5, 0.6])
alts = np.array([1.0, 2.0, 3.0])

# (cyice function, bad args, good args, expected error, ctypes equivalent)
error_cases = [
    pytest.param(
        cyice.georec_s,
        (0.1, 0.4, 1.0, -1.0, 0.5),
        (0.1, 0.4, 1.0, 6378.0, 0.003),
        SpiceVALUEOUTOFRANGE,
        spice.georec,
        id="georec_s",
    ),
    pytest.param(
        cyice.georec_v,
        (lons, lats, alts, -1.0, 0.5),
        (lons, lats, alts, 6378.0, 0.003),
        SpiceVALUEOUTOFRANGE,
        None,
        id="georec_v",
    ),
    pytest.param(
        cyice.recgeo_s,
        (rect, 6378.0, 2.0),
        (rect, 6378.0, 0.003),
        SpiceVALUEOUTOFRANGE,
        spice.recgeo,
        id="recgeo_s",
    ),
    pytest.param(
        cyice.recgeo_v,
        (rects, 6378.0, 2.0),
        (rects, 6378.0, 0.003),
        SpiceVALUEOUTOFRANGE,
        None,
        id="recgeo_v",
    ),
    pytest.param(
        cyice.pgrrec_s,
        ("NOTABODY", 0.1, 0.4, 1.0, 3396.0, 0.006),
        ("MARS", 0.1, 0.4, 1.0, 3396.0, 0.006),
        SpiceIDCODENOTFOUND,
        spice.pgrrec,
        id="pgrrec_s",
    ),
    pytest.param(
        cyice.pgrrec_v,
        ("NOTABODY", lons, lats, alts, 3396.0, 0.006),
        ("MARS", lons, lats, alts, 3396.0, 0.006),
        SpiceIDCODENOTFOUND,
        None,
        id="pgrrec_v",
    ),
    pytest.param(
        cyice.recpgr_s,
        ("NOTABODY", rect, 3396.0, 0.006),
        ("MARS", rect, 3396.0, 0.006),
        SpiceIDCODENOTFOUND,
        spice.recpgr,
        id="recpgr_s",
    ),
    pytest.param(
        cyice.recpgr_v,
        ("NOTABODY", rects, 3396.0, 0.006),
        ("MARS", rects, 3396.0, 0.006),
        SpiceIDCODENOTFOUND,
        None,
        id="recpgr_v",
    ),
    pytest.param(
        cyice.srfrec_s,
        (-99999, 0.1, 0.4),
        (399, 0.1, 0.4),
        SpiceKERNELVARNOTFOUND,
        spice.srfrec,
        id="srfrec_s",
    ),
    pytest.param(
        cyice.srfrec_v,
        (-99999, lons, lats),
        (399, lons, lats),
        SpiceKERNELVARNOTFOUND,
        None,
        id="srfrec_v",
    ),
]


@pytest.mark.parametrize(
    "function, bad_args, good_args, error, ctypes_function", error_cases
)
def test_error_recovery(
    function, bad_args, good_args, error, ctypes_function, load_core_kernels
):
    with pytest.raises(error):
        function(*bad_args)
    assert not spice.failed()
    result = function(*good_args)
    if ctypes_function is not None:
        npt.assert_allclose(result, ctypes_function(*good_args), rtol=1e-14)


def test_unload_error_recovery(load_core_kernels):
    with pytest.raises(SpiceEMPTYSTRING):
        cyice.unload("")
    assert not spice.failed()
    cyice.unload(CoreKernels.testMetaKernel)
    assert spice.ktotal("ALL") == 0
