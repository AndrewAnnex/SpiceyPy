"""
The MIT License (MIT)

Copyright (c) [2015-2025] [Andrew Annex]

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

import os
import sys
import subprocess
import pytest


def _env(env: dict[str, str]):
    full_env = os.environ.copy()
    # ensure we control the behavior even if developer/CI has this set
    full_env.pop("SPICEYPY_LOGLEVEL", None)
    full_env.update(env)
    return full_env


def test_import_default_does_not_emit_info():
    code = r"""
import spiceypy
"""
    env = _env({})
    p = subprocess.run(
        [sys.executable, "-c", code],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert "INFO:spiceypy" not in (p.stderr or "")


def test_import_with_warning_does_not_emit_info():
    code = r"""
import logging
logging.basicConfig(level=0, force=True, format="%(levelname)s:%(name)s:%(message)s")

import spiceypy
"""
    env = _env({"SPICEYPY_LOGLEVEL": "WARNING"})
    p = subprocess.run(
        [sys.executable, "-c", code],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert "INFO:spiceypy" not in (p.stderr or "")


def test_import_with_warning_does_not_emit_info_w_preconfig():
    code = r"""
import spiceypy
"""
    env = _env({"SPICEYPY_LOGLEVEL": "WARNING"})
    p = subprocess.run(
        [sys.executable, "-c", code],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert "INFO:spiceypy" not in (p.stderr or "")

def test_import_with_info_emits_info():
    code = r"""
import logging
logging.basicConfig(level=0, force=True, format="%(levelname)s:%(name)s:%(message)s")

import spiceypy
"""
    env = _env({"SPICEYPY_LOGLEVEL": "INFO"})
    p = subprocess.run(
        [sys.executable, "-c", code],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert "INFO:spiceypy" in (p.stderr or "")

def test_import_with_info_emits_info_w_preconfig():
    code = r"""
import spiceypy
"""
    env = _env({"SPICEYPY_LOGLEVEL": "INFO"})
    p = subprocess.run(
        [sys.executable, "-c", code],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert "INFO:spiceypy" in (p.stderr or "")


def test_import_with_invalid_setting_does_not_emit_info_w_preconfig():
    code = r"""
import spiceypy
"""
    env = _env({"SPICEYPY_LOGLEVEL": "TROGDOR"})
    p = subprocess.run(
        [sys.executable, "-c", code],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert "Unknown logger level" in (p.stderr or "")
    assert "INFO:spiceypy" not in (p.stderr or "")