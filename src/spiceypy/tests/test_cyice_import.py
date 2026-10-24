"""Cyice must initialize its annotations before a first native geometry call."""

import subprocess
import sys

import pytest

# these tests launch a fresh interpreter, which emscripten cannot do
pytestmark = pytest.mark.skipif(
    sys.platform == "emscripten", reason="emscripten does not support processes"
)


def test_cyice_geometry_in_fresh_interpreter():
    code = """
import math
import numpy as np
from spiceypy import cyice

state = np.array([3.0, 4.0, 12.0, 0.1, 0.2, 0.3])
actual = cyice.xfmsta_s(state, "RECTANGULAR", "CYLINDRICAL", "EARTH")
expected = [5.0, math.atan2(4.0, 3.0), 12.0, 0.22, 0.008, 0.3]
np.testing.assert_allclose(actual, expected, rtol=1e-14)
"""
    result = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, result.stderr
