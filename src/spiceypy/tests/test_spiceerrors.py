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

import pytest
import spiceypy as spice
from spiceypy.tests.gettestkernels import cwd
import os


def test_tkversion():
    assert spice.exceptions._tkversion == spice.tkvrsn("toolkit")


def test_geterror():
    spice.setmsg("some error occured")
    spice.sigerr("error")
    assert spice.failed()
    assert spice.getmsg("SHORT", 40) == "error"
    assert spice.getmsg("LONG", 200) == "some error occured"
    spice.reset()


def test_get_spiceypy_exceptions():
    with pytest.raises(
        (
            spice.exceptions.SpiceyError,
            spice.exceptions.SpiceyPyError,
            spice.exceptions.SpiceyPyIOError,
        )
    ):
        spice.furnsh(os.path.join(cwd, "_null_kernel.txt"))
    spice.reset()


def test_no_loaded_files_exception():
    with pytest.raises(spice.SpiceyError):
        spice.ckgp(0, 0, 0, "blah")
    spice.reset()
    with pytest.raises(spice.NotFoundError):
        spice.ckgp(0, 0, 0, "blah")
    spice.reset()
    with spice.no_found_check():
        with pytest.raises(spice.SpiceyPyIOError):
            spice.ckgp(0, 0, 0, "blah")
        spice.reset()
        with pytest.raises(spice.exceptions.SpiceNOLOADEDFILES):
            spice.ckgp(0, 0, 0, "blah")
        spice.reset()


def test_found_error_checker():
    with pytest.raises(
        (
            spice.exceptions.SpiceyError,
            spice.exceptions.SpiceyPyError,
            spice.exceptions.NotFoundError,
        )
    ):
        spice.bodc2n(-9991)
    spice.reset()


def test_error_to_str():
    try:
        spice.bodc2n(-9991)
    except spice.exceptions.SpiceyError as sp:
        assert str(sp) != ""


def test_disable_found_catch():
    spice.kclear()
    with spice.no_found_check():
        name, found = spice.bodc2n(-9991)
        assert not found
    with pytest.raises(spice.SpiceyError):
        spice.bodc2n(-9991)
    # try more hands on method
    spice.found_check_off()
    name, found = spice.bodc2n(-9991)
    assert not found
    spice.found_check_on()
    spice.kclear()


def test_recursive_disable_found_catch():
    spice.kclear()
    assert spice.config.catch_false_founds

    def _recursive_call(i):
        if i <= 0:
            return
        else:
            with spice.no_found_check():
                name, found = spice.bodc2n(-9991)
                assert not found
                _recursive_call(i - 1)

    assert spice.config.catch_false_founds
    _recursive_call(100)
    spice.kclear()
    spice.found_check_off()
    _recursive_call(100)
    spice.kclear()
    spice.found_check_on()
    _recursive_call(100)
    spice.kclear()


def test_found_check():
    spice.kclear()
    spice.found_check_off()
    name, found = spice.bodc2n(-9991)
    assert not found
    spice.kclear()
    with spice.found_check():
        with pytest.raises(spice.SpiceyError):
            name = spice.bodc2n(-9991)
    assert not spice.get_found_catch_state()
    spice.found_check_on()
    assert spice.get_found_catch_state()
    spice.kclear()


def test_multiple_founds():
    success = spice.NotFoundError(message="test", found=(True, True))
    assert all(success.found)
    failed = spice.NotFoundError(message="test", found=(True, False))
    assert not all(failed.found)
    # def test_fun
    @spice.spice_found_exception_thrower
    def test_fun():
        return [0, 0], [False, True]

    # test it
    with pytest.raises(spice.SpiceyError):
        test_fun()

    # test it
    with pytest.raises(spice.NotFoundError):
        test_fun()
