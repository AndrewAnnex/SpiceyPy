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
import pytest

from spiceypy.tests.gettestkernels import attempt_download, CoreKernels


def test_gettestkernels():
    # Force exceptions in gettestkernels.py to get complete coverage there
    # To complete code coverage in spiceypy.tests.gettestkernels.py
    with pytest.raises(BaseException):
        # Generate .HTTPError, return BaseException
        attempt_download(
            "https://naif.jpl.nasa.gov/404", "httperror.txt", "httperror.txt", 1
        )
    with pytest.raises(BaseException):
        # Generate .URLError, return BaseException
        attempt_download(
            "https://no_such_host.naif.jpl.nasa.gov/404",
            "urlerror.txt",
            "urlerror.txt",
            1,
        )
    with pytest.raises(BaseException):
        # download a file with an incorrect hash
        attempt_download(
            CoreKernels.lsk_url,
            "badhashkernel.txt",
            "badhashkernel.txt",
            1,
            provided_hash="11c9b4793b6676d464266e790262b986",
        )
