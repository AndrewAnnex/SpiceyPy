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


def setup_module(module):
    download_kernels()

#A

#B

@pytest.mark.parametrize('function', [cyice.b1900, spice.b1900], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["b1900"], indirect=True)
def test_b1900(function, grouped_benchmark):
    grouped_benchmark(function)
    assert function() == 2415020.31352

# C

@pytest.mark.parametrize('function', [cyice.ckgp, spice.ckgp], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["ckgp"], indirect=True)
def test_ckgp(function, grouped_benchmark, load_cassini_kernels):
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


@pytest.mark.parametrize('function', [cyice.ckgp_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["ckgp_v"], indirect=True)
def test_ckgp_v(function, grouped_benchmark, load_cassini_kernels):
    ckid  = -82000
    covers = np.repeat(267832537952.0,100)
    grouped_benchmark(function, ckid, covers, 256, "J2000")
    res = function(ckid, covers, 256, "J2000")
    cmat, clkout = res[0], res[1]
    assert clkout[0] == 267832537952.0


@pytest.mark.parametrize('function', [cyice.ckgpav, spice.ckgpav], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["ckgpav"], indirect=True)
def test_ckgpav(function, grouped_benchmark, load_cassini_kernels):
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


@pytest.mark.parametrize('function', [cyice.ckgpav_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["ckgpav_v"], indirect=True)
def test_ckgpav_v(function, grouped_benchmark, load_cassini_kernels):
    ckid  = -82000
    covers = np.repeat(267832537952.0,100)
    grouped_benchmark(function, ckid, covers, 256, "J2000")
    res = function(ckid, covers, 256, "J2000")
    cmat, avout, clkout = res[0], res[1], res[2]
    assert clkout[0] == 267832537952.0


@pytest.mark.parametrize('function', [cyice.convrt, spice.convrt], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["convrt"], indirect=True)
def test_convrt(function, grouped_benchmark):
    grouped_benchmark(function, 1.0, "parsecs", "lightyears")
    assert function(300.0, "statute_miles", "km") == 482.80320


@pytest.mark.parametrize('function', [cyice.convrt_v, spice.convrt], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["convrt_v"], indirect=True)
def test_convrt_v(function, grouped_benchmark):
    data = np.arange(0, 1000.0, dtype=float)
    grouped_benchmark(function, data, "parsecs", "lightyears")
    res = function(data, "parsecs", "lightyears")
    assert isinstance(res, np.ndarray)


@pytest.mark.parametrize('function', [cyice.deltet, spice.deltet], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["deltet"], indirect=True)
def test_deltet(function, grouped_benchmark, load_core_kernels):
    et_2004 = spice.str2et("Jan 1 2004")
    grouped_benchmark(function, et_2004, "ET")

# D
@pytest.mark.parametrize('function', [cyice.deltet_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["deltet_v"], indirect=True)
def test_deltet_v(function, grouped_benchmark, load_core_kernels):
    ets_2004 = np.repeat(spice.str2et("Jan 1 2004"), 100)
    grouped_benchmark(function, ets_2004, "ET")
    res = function(ets_2004, "ET")
    assert isinstance(res, np.ndarray)

# E

@pytest.mark.parametrize('function', [cyice.et2lst, spice.et2lst], ids=get_module_name)
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


@pytest.mark.parametrize('function', [cyice.et2lst_v], ids=get_module_name)
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


@pytest.mark.parametrize('function', [cyice.et2utc, spice.et2utc], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["et2utc"], indirect=True)
def test_et2utc(function, grouped_benchmark, load_core_kernels):
    grouped_benchmark(function,  -527644192.5403653, "J", 6)


@pytest.mark.parametrize('function', [cyice.et2utc_v, spice.et2utc], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["et2utc_v"], indirect=True)
def test_et2utc_v(function, grouped_benchmark, load_core_kernels):
    ets = np.repeat(-527644192.5403653, 100)
    grouped_benchmark(function, ets, "J", 6)
    expected_res = np.repeat("JD 2445438.006415", 100)
    res = function(ets, "J", 6)
    assert isinstance(res, np.ndarray)
    assert np.array_equal(res, expected_res)


@pytest.mark.parametrize('function', [cyice.etcal, spice.etcal], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["etcal"], indirect=True)
def test_etcal(function, grouped_benchmark):
    grouped_benchmark(function, 0.0)


@pytest.mark.parametrize('function', [cyice.etcal_v, spice.etcal], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["etcal_v"], indirect=True)
def test_etcal_v(function, grouped_benchmark):
    data = np.arange(10000.0, dtype=float)
    grouped_benchmark(function, data)
    res = function(data)
    assert isinstance(res, np.ndarray)

# F
@pytest.mark.parametrize('function', [cyice.failed, spice.failed], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["failed"], indirect=True)
def test_failed(function, grouped_benchmark):
    grouped_benchmark(function)


@pytest.mark.parametrize('function', [cyice.fovray, spice.fovray], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["fovray"], indirect=True)
def test_fovray(function, grouped_benchmark, load_cassini_kernels):
    camid = spice.bodn2c("CASSINI_ISS_NAC")
    _, frame, _, _, _ = spice.getfov(camid, 4)
    et = spice.str2et("2013 FEB 25 11:50:00 UTC")
    raydir = np.array([0.0, 0.0, 1.0])
    grouped_benchmark(function, "CASSINI_ISS_NAC", raydir, frame, "S", "CASSINI", et)
    assert function("CASSINI_ISS_NAC", raydir, frame, "S", "CASSINI", et)


@pytest.mark.parametrize('function', [cyice.fovray_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["fovray_v"], indirect=True)
def test_fovray_v(function, grouped_benchmark, load_cassini_kernels):
    ets = np.repeat(spice.str2et("2013 FEB 25 11:50:00 UTC"), 100)
    raydir = np.array([0.0, 0.0, 1.0])
    grouped_benchmark(function, "CASSINI_ISS_NAC", raydir, "CASSINI_ISS_NAC", "S", "CASSINI", ets)
    res = function("CASSINI_ISS_NAC", raydir, "CASSINI_ISS_NAC", "S", "CASSINI", ets)
    assert isinstance(res, np.ndarray)
    assert res.dtype == np.bool


@pytest.mark.parametrize('function', [cyice.fovtrg, spice.fovtrg], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["fovtrg"], indirect=True)
def test_fovtrg(function, grouped_benchmark, load_cassini_kernels):
    et = spice.str2et("2013 FEB 25 11:50:00 UTC")
    grouped_benchmark(function, "CASSINI_ISS_NAC", "Enceladus", "Ellipsoid", "IAU_ENCELADUS", "LT+S","CASSINI", et)


@pytest.mark.parametrize('function', [cyice.fovtrg_v], ids=get_module_name)
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

@pytest.mark.parametrize('function', [cyice.getmsg, spice.getmsg], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["getmsg"], indirect=True)
def test_getmsg(function, grouped_benchmark):
    cyice.reset()
    spice.sigerr("test error")
    grouped_benchmark(function, "SHORT", 200)
    cyice.reset()

# H

# I

# J

# K

# L

@pytest.mark.parametrize('function', [cyice.lspcn, spice.lspcn], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["lspcn"], indirect=True)
def test_lspcn(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("21 march 2005")
    grouped_benchmark(function, "EARTH", et, "NONE")


@pytest.mark.parametrize('function', [cyice.lspcn_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["lspcn"], indirect=True)
def test_lspcn_v(function, grouped_benchmark, load_core_kernels):
    ets = np.repeat(spice.str2et("21 march 2005"),100)
    grouped_benchmark(function, "EARTH", ets, "NONE")
    res = function("EARTH", ets, "NONE")
    assert isinstance(res, np.ndarray)

# M

# N

# O

# P

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
@pytest.mark.parametrize('function', [cyice.reset, spice.reset], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["reset"], indirect=True)
def test_reset(function, grouped_benchmark):
   grouped_benchmark(function)


# S
@pytest.mark.parametrize('function', [cyice.scdecd, spice.scdecd], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["scdecd"], indirect=True)
def test_scdecd(function, grouped_benchmark, load_voyager_kernels):
    timein = spice.scencd(-32, "2/20538:39:768")
    grouped_benchmark(function, -32, timein)


@pytest.mark.parametrize('function', [cyice.scdecd_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["scdecd_v"], indirect=True)
def test_scdecd_v(function, grouped_benchmark, load_voyager_kernels):
    timein = np.repeat(spice.scencd(-32, "2/20538:39:768"), 100)
    grouped_benchmark(function, -32, timein)
    res = function(-32, timein) 
    assert isinstance(res, np.ndarray)


@pytest.mark.parametrize('function', [cyice.scencd, spice.scencd], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["scencd"], indirect=True)
def test_scencd(function, grouped_benchmark, load_voyager_kernels):
    grouped_benchmark(function, -32,  "2/20538:39:768")


@pytest.mark.parametrize('function', [cyice.scencd_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["scencd_v"], indirect=True)
def test_scencd_v(function, grouped_benchmark, load_voyager_kernels):
    timein = np.repeat("2/20538:39:768", 100).tolist()
    grouped_benchmark(function, -32,  timein)
    res = function(-32, timein)
    assert isinstance(res, np.ndarray)


@pytest.mark.parametrize('function', [cyice.sce2c, spice.sce2c], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sce2c"], indirect=True)
def test_sce2c(function, grouped_benchmark, load_voyager_kernels):
    et = spice.str2et("1979 JUL 05 21:50:21.23379")
    grouped_benchmark(function, -32, et)


@pytest.mark.parametrize('function', [cyice.sce2c_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sce2c_v"], indirect=True)
def test_sce2c_v(function, grouped_benchmark, load_voyager_kernels):
    ets = np.repeat(spice.str2et("1979 JUL 05 21:50:21.23379"), 100)
    grouped_benchmark(function, -32, ets)
    res = function(-32, ets)
    assert isinstance(res, np.ndarray)


@pytest.mark.parametrize('function', [cyice.sce2s, spice.sce2s], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sce2s"], indirect=True)
def test_sce2s(function, grouped_benchmark):
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.voyagerSclk)
    et = spice.str2et("1979 JUL 05 21:50:21.23379")
    grouped_benchmark(function, -32, et)


@pytest.mark.parametrize('function', [cyice.sce2s_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sce2s_v"], indirect=True)
def test_sce2s_v(function, grouped_benchmark):
    spice.furnsh(CoreKernels.testMetaKernel)
    spice.furnsh(ExtraKernels.voyagerSclk)
    ets = np.repeat(spice.str2et("1979 JUL 05 21:50:21.23379"), 100)
    grouped_benchmark(function, -32, ets)
    res = function(-32, ets)
    assert isinstance(res, np.ndarray)


@pytest.mark.parametrize('function', [cyice.scs2e, spice.scs2e], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["scs2e"], indirect=True)
def test_scs2e(function, grouped_benchmark, load_voyager_kernels):
    grouped_benchmark(function, -32, "2/20538:39:768")


@pytest.mark.parametrize('function', [cyice.scs2e_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["scs2e_v"], indirect=True)
def test_scs2e_v(function, grouped_benchmark, load_voyager_kernels):
    timein = np.repeat("2/20538:39:768", 100)
    grouped_benchmark(function, -32, timein)
    res = function(-32, timein)
    assert isinstance(res, np.ndarray)


@pytest.mark.parametrize('function', [cyice.sct2e, spice.sct2e], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sct2e"], indirect=True)
def test_sct2e(function, grouped_benchmark, load_voyager_kernels):
    grouped_benchmark(function, -32,  985327965.0)


@pytest.mark.parametrize('function', [cyice.sct2e_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sct2e_v"], indirect=True)
def test_sct2e_v(function, grouped_benchmark, load_voyager_kernels):
    sclkdps = np.repeat(985327965.0, 100)
    grouped_benchmark(function, -32, sclkdps)
    res = function(-32, sclkdps)
    assert isinstance(res, np.ndarray)


@pytest.mark.parametrize('function', [cyice.spkapo, spice.spkapo], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkapo"], indirect=True)
def test_spkapo(function, grouped_benchmark, load_core_kernels):
    MARS, MOON = 499, 301
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("Jan 1 2004 5:00 PM")
    state = spice.spkssb(MOON, et, "J2000")
    grouped_benchmark(function, MARS, et, "J2000", state,"LT+S")
    pos_vec, ltime = function(MARS, et, "J2000", state, "LT+S")
    expected_pos = np.array([
        1.64534472413454592228e08,
        2.51219951337271928787e07,
        1.11454124484200235456e07,
    ])
    assert isinstance(pos_vec, np.ndarray)
    npt.assert_array_almost_equal(pos_vec, expected_pos, decimal=5)


@pytest.mark.parametrize('function', [cyice.spkapo_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkapo_v"], indirect=True)
def test_spkapo_v(function, grouped_benchmark, load_core_kernels):
    MARS, MOON = 499, 301
    spice.furnsh(CoreKernels.testMetaKernel)
    et = spice.str2et("Jan 1 2004 5:00 PM")
    state = spice.spkssb(MOON, et, "J2000")
    ets = np.repeat(et, 100)
    grouped_benchmark(function, MARS, ets, "J2000", state,"LT+S")
    pos_vec, ltime = function(MARS, ets, "J2000", state, "LT+S")
    assert isinstance(pos_vec, np.ndarray)
    assert isinstance(ltime, np.ndarray)


@pytest.mark.parametrize('function', [cyice.spkcpo, spice.spkcpo], ids=get_module_name)
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


@pytest.mark.parametrize('function', [cyice.spkcpo_v], ids=get_module_name)
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


@pytest.mark.parametrize('function', [cyice.spkcpt, spice.spkcpt], ids=get_module_name)
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


@pytest.mark.parametrize('function', [cyice.spkcpt_v], ids=get_module_name)
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



@pytest.mark.parametrize('function', [cyice.spkez, spice.spkez], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkez"], indirect=True)
def test_spkez(function, grouped_benchmark, load_core_kernels):
    et = cyice.str2et("July 4, 2003 11:00 AM PST")
    grouped_benchmark(function, 499, et, "J2000", "LT+S", 399)
    state, lt = function(499, et, "J2000", "LT+S", 399)
    assert isinstance(state, np.ndarray)


@pytest.mark.parametrize('function', [cyice.spkez_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkez_v"], indirect=True)
def test_spkez_v(function, grouped_benchmark, load_core_kernels):
    ets = np.repeat(cyice.str2et("July 4, 2003 11:00 AM PST"), 100)
    grouped_benchmark(function, 499, ets, "J2000", "LT+S", 399)
    state, lts = function(499, ets, "J2000", "LT+S", 399)
    assert isinstance(state, np.ndarray)
    assert isinstance(lts, np.ndarray)


@pytest.mark.parametrize('function', [cyice.spkezp, spice.spkezp], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkezp"], indirect=True)
def test_spkezp(function, grouped_benchmark, load_core_kernels):
    et = cyice.str2et("July 4, 2003 11:00 AM PST")
    grouped_benchmark(function, 499, et, "J2000", "LT+S", 399)
    pos, lt = function(499, et, "J2000", "LT+S", 399)
    assert isinstance(pos, np.ndarray)
    expected_lt = 269.6898813661505
    npt.assert_almost_equal(lt, expected_lt)


@pytest.mark.parametrize('function', [cyice.spkezp_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkezp_v"], indirect=True)
def test_spkezp_v(function, grouped_benchmark, load_core_kernels):
    ets = np.repeat(cyice.str2et("July 4, 2003 11:00 AM PST"), 100)
    grouped_benchmark(function, 499, ets, "J2000", "LT+S", 399)
    pos, lts = function(499, ets, "J2000", "LT+S", 399)
    assert isinstance(pos, np.ndarray)
    assert isinstance(lts, np.ndarray)


@pytest.mark.parametrize('function', [cyice.spkezr, spice.spkezr], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkezr"], indirect=True)
def test_spkezr(function, grouped_benchmark, load_core_kernels):
    et = cyice.str2et("July 4, 2003 11:00 AM PST")
    grouped_benchmark(function, "Mars", et, "J2000", "LT+S", "Earth")
    state, lt = function("Mars", et, "J2000", "LT+S", "Earth")
    assert isinstance(state, np.ndarray)


@pytest.mark.parametrize('function', [cyice.spkezr_v, spice.spkezr], ids=get_module_name)
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


@pytest.mark.parametrize('function', [cyice.spkcvo, spice.spkcvo], ids=get_module_name)
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


@pytest.mark.parametrize('function', [cyice.spkcvo_v,], ids=get_module_name)
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


@pytest.mark.parametrize('function', [cyice.spkcvt, spice.spkcvt], ids=get_module_name)
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


@pytest.mark.parametrize('function', [cyice.spkcvt_v, ], ids=get_module_name)
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


@pytest.mark.parametrize('function', [cyice.spkgeo, spice.spkgeo], ids=get_module_name)
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


@pytest.mark.parametrize('function', [cyice.spkgeo_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkgeo_v"], indirect=True)
def test_spkgeo_v(function, grouped_benchmark, load_core_kernels):
    et = np.repeat(spice.str2et("July 4, 2003 11:00 AM PST"),100)
    grouped_benchmark(function, 499, et, "J2000", 399)
    state, lt = function(499, et, "J2000", 399)
    assert isinstance(state, np.ndarray)
    assert isinstance(lt, np.ndarray)


@pytest.mark.parametrize('function', [cyice.spkgps, spice.spkgps], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkgos"], indirect=True)
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


@pytest.mark.parametrize('function', [cyice.spkgps_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkgps_v"], indirect=True)
def test_spkgps_v(function, grouped_benchmark, load_core_kernels):
    et = np.repeat(spice.str2et("July 4, 2003 11:00 AM PST"),100)
    grouped_benchmark(function, 499, et, "J2000", 399)
    pos, lt = function(499, et, "J2000", 399)
    assert isinstance(pos, np.ndarray)
    assert isinstance(lt, np.ndarray)


@pytest.mark.parametrize('function', [cyice.spkpvn, spice.spkpvn], ids=get_module_name)
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


@pytest.mark.parametrize('function', [cyice.spkpvn_v], ids=get_module_name)
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


@pytest.mark.parametrize('function', [cyice.spkpos, spice.spkpos], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkpos"], indirect=True)
def test_spkpos(function, grouped_benchmark, load_core_kernels):
    et = cyice.str2et("July 4, 2003 11:00 AM PST")
    grouped_benchmark(function, "Mars", et, "J2000", "LT+S", "Earth")


@pytest.mark.parametrize('function', [cyice.spkpos_v, spice.spkpos], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkpos_v"], indirect=True)
def test_spkpos_v(function, grouped_benchmark, load_core_kernels):
    ets = np.repeat(spice.str2et("July 4, 2003 11:00 AM PST"), 100)
    grouped_benchmark(function, "Mars", ets, "J2000", "LT+S", "Earth")
    ptargs, lts = function("Mars", ets, "J2000", "LT+S", "Earth")
    assert isinstance(ptargs, np.ndarray)


@pytest.mark.parametrize('function', [cyice.spkssb, spice.spkssb], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkssb"], indirect=True)
def test_spkssb(function, grouped_benchmark, load_core_kernels):
    et = cyice.str2et("July 4, 2003 11:00 AM PST")
    grouped_benchmark(function, 499, et, "J2000")
    state = function(499, et, "J2000")
    assert isinstance(state, np.ndarray)


@pytest.mark.parametrize('function', [cyice.spkssb_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["spkssb_v"], indirect=True)
def test_spkssb_v(function, grouped_benchmark, load_core_kernels):
    ets = np.repeat(cyice.str2et("July 4, 2003 11:00 AM PST"), 100)
    grouped_benchmark(function, 499, ets, "J2000")
    state = function(499, ets, "J2000")
    assert isinstance(state, np.ndarray)


@pytest.mark.parametrize('function', [cyice.str2et, spice.str2et], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["str2et"], indirect=True)
def test_str2et(function, grouped_benchmark, load_core_kernels):
    grouped_benchmark(function, "Thu Mar 20 12:53:29 PST 1997")


@pytest.mark.parametrize('function', [cyice.str2et_v, spice.str2et], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["str2et_v"], indirect=True)
def test_str2et_v(function, grouped_benchmark, load_core_kernels):
    date = "Thu Mar 20 12:53:29 PST 1997"
    dates = np.array([date] * 100, dtype=np.str_)
    grouped_benchmark(function, dates)
    expected_ets = np.ones(100) * -87836728.81438904
    ets = function(dates)
    assert isinstance(ets, np.ndarray)
    npt.assert_array_almost_equal(ets, expected_ets)


@pytest.mark.parametrize('function', [cyice.sincpt, spice.sincpt], ids=get_module_name)
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


@pytest.mark.parametrize('function', [cyice.sincpt_v], ids=get_module_name)
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


@pytest.mark.parametrize('function', [cyice.subpnt, spice.subpnt], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["subpnt"], indirect=True)
def test_subpnt(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("2008 aug 11 00:00:00")
    method = "Intercept:  ellipsoid"
    grouped_benchmark(function, method, "Mars", et, "IAU_MARS", "LT+S", "Earth")
    spoint, trgepc, srfvec = function(method, "Mars", et, "IAU_MARS", "LT+S", "Earth")
    assert isinstance(spoint, np.ndarray)
    assert isinstance(srfvec, np.ndarray)


@pytest.mark.parametrize('function', [cyice.subpnt_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["subpnt_v"], indirect=True)
def test_subpnt_v(function, grouped_benchmark, load_core_kernels):
    et = np.repeat(spice.str2et("2008 aug 11 00:00:00"), 100)
    method = "Intercept:  ellipsoid"
    grouped_benchmark(function, method, "Mars", et, "IAU_MARS", "LT+S", "Earth")
    spoint, trgepc, srfvec = function(method, "Mars", et, "IAU_MARS", "LT+S", "Earth")
    assert isinstance(spoint, np.ndarray)
    assert isinstance(trgepc, np.ndarray)
    assert isinstance(srfvec, np.ndarray)


@pytest.mark.parametrize('function', [cyice.subslr, spice.subslr], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["subslr"], indirect=True)
def test_subslr(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("2008 aug 11 00:00:00")
    method = "Intercept:  ellipsoid"
    grouped_benchmark(function, method, "Mars", et, "IAU_MARS", "LT+S", "Earth")
    spoint, trgepc, srfvec = function(method, "Mars", et, "IAU_MARS", "LT+S", "Earth")
    assert isinstance(spoint, np.ndarray)
    assert isinstance(srfvec, np.ndarray)


@pytest.mark.parametrize('function', [cyice.subslr_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["subslr_v"], indirect=True)
def test_subslr_v(function, grouped_benchmark, load_core_kernels):
    et = np.repeat(spice.str2et("2008 aug 11 00:00:00"), 100)
    method = "Intercept:  ellipsoid"
    grouped_benchmark(function, method, "Mars", et, "IAU_MARS", "LT+S", "Earth")
    spoint, trgepc, srfvec = function(method, "Mars", et, "IAU_MARS", "LT+S", "Earth")
    assert isinstance(spoint, np.ndarray)
    assert isinstance(trgepc, np.ndarray)
    assert isinstance(srfvec, np.ndarray)


@pytest.mark.parametrize('function', [cyice.sxform, spice.sxform], ids=get_module_name)
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


@pytest.mark.parametrize('function', [cyice.sxform_v, spice.sxform], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["sxform_v"], indirect=True)
def test_sxform_v(function, grouped_benchmark, load_core_kernels):
    et = np.repeat(spice.str2et("January 1, 1990"), 1000)
    grouped_benchmark(function, "IAU_EARTH", "J2000", et)
    res = function("IAU_EARTH", "J2000", et)
    assert isinstance(res, np.ndarray)


@pytest.mark.parametrize('function', [cyice.tangpt, spice.tangpt], ids=get_module_name)
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


@pytest.mark.parametrize('function', [cyice.tangpt_v], ids=get_module_name)
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


@pytest.mark.parametrize('function', [cyice.timout, spice.timout], ids=get_module_name)
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


@pytest.mark.parametrize('function', [cyice.timout_v, spice.timout], ids=get_module_name)
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


@pytest.mark.parametrize('function', [cyice.trgsep, spice.trgsep], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["trgsep"], indirect=True)
def test_trgsep(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("2007-JAN-11 11:21:20.213872 (TDB)")
    grouped_benchmark(function, et, "MOON", "POINT", "IAU_MOON", "EARTH", "POINT", "IAU_EARTH", "SUN", "LT+S")
    point_sep = function(et, "MOON", "POINT", "IAU_MOON", "EARTH", "POINT", "IAU_EARTH", "SUN", "LT+S")
    assert spice.dpr() * point_sep == pytest.approx(0.15729276)


@pytest.mark.parametrize('function', [cyice.trgsep_v,], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["trgsep_v"], indirect=True)
def test_trgsep_v(function, grouped_benchmark, load_core_kernels):
    ets = np.repeat(spice.str2et("2007-JAN-11 11:21:20.213872 (TDB)"),100)
    grouped_benchmark(function, ets, "MOON", "POINT", "IAU_MOON", "EARTH", "POINT", "IAU_EARTH", "SUN", "LT+S")  
    res = function(ets, "MOON", "POINT", "IAU_MOON", "EARTH", "POINT", "IAU_EARTH", "SUN", "LT+S")
    assert isinstance(res, np.ndarray)


@pytest.mark.parametrize('function', [cyice.unitim, spice.unitim], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["unitim"], indirect=True)
def test_unitim(function, grouped_benchmark, load_core_kernels):
    et = spice.str2et("Dec 19 2003")
    grouped_benchmark(function, et, "ET", "JED")
    # correctness assertion can be performed before or after
    converted_et = function(et, "ET", "JED")
    npt.assert_almost_equal(converted_et, 2452992.5007428653)


@pytest.mark.parametrize('function', [cyice.unitim_v], ids=get_module_name)
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


@pytest.mark.parametrize('function', [cyice.utc2et, spice.utc2et], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["utc2et"], indirect=True)
def test_utc2et(function, grouped_benchmark, load_core_kernels):
    grouped_benchmark(function, "December 1, 2004 15:04:11")
    assert function("December 1, 2004 15:04:11") == 155185515.1831043


@pytest.mark.parametrize('function', [cyice.utc2et_v], ids=get_module_name)
@pytest.mark.parametrize('grouped_benchmark', ["utc2et_v"], indirect=True)
def test_utc2et_v(function, grouped_benchmark, load_core_kernels):
    date = "December 1, 2004 15:04:11"
    dates = np.array([date] * 100, dtype=np.str_)
    grouped_benchmark(function, dates)
    res = function(dates)
    assert isinstance(res, np.ndarray)