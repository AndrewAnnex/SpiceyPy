"""
The MIT License (MIT)

Copyright (c) [2015-2017] [Andrew Annex]

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
import os
cwd = os.path.realpath(os.path.dirname(__file__))


def test_geterror():
    spice.setmsg("some error occured")
    spice.sigerr("error")
    assert spice.failed()
    assert spice.getmsg("SHORT", 40) == "error"
    assert spice.getmsg("LONG", 200) == "some error occured"
    spice.reset()


def test_getSpiceyException():
    with pytest.raises(spice.stypes.SpiceyError):
        spice.furnsh(os.path.join(cwd, "_null_kernel.txt"))
    spice.reset()


def test_emptyKernelPoolException():
    with pytest.raises(spice.stypes.SpiceyError):
        spice.ckgp(0, 0, 0, "blah")
    spice.reset()


def test_foundErrorChecker():
    with pytest.raises(spice.stypes.SpiceyError):
        spice.bodc2n(-9991)
    spice.reset()
