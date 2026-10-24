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
import tempfile

import spiceypy

from spiceypy.tests.gettestkernels import (
    attempt_download,
    CoreKernels,
    write_test_meta_kernel,
)


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


def _write_empty_kernel(tpc_path: str):
    with open(tpc_path, "w") as tpc_file:
        tpc_file.write("KPL/PCK\n")


def _test_metakernel_long_path(
    metakernel_path: str, tpc_path: str, fixed_tpc_path: str
):
    _write_empty_kernel(tpc_path)
    write_test_meta_kernel(metakernel_path, (tpc_path, fixed_tpc_path))
    spiceypy.furnsh(metakernel_path)
    # unloading the metakernel also unloads the kernels it listed, so nothing
    # stays loaded for later tests or after the temporary directory is removed
    spiceypy.unload(metakernel_path)


def test_metakernel_long_paths():
    with tempfile.TemporaryDirectory() as temp_dir:
        MAX_PIECE_LEN = 80
        EMPTY_TPC_NAME = "empty.tpc"
        FIXED_TPC_NAME = "fixed.tpc"

        # This makes the test a little more interesting by having the metakernel
        # reference a second kernel after the long-path one under test. This can
        # expose problems with poor handling of paths that end with continuation
        # characters.
        fixed_tpc_path = os.path.join(temp_dir, FIXED_TPC_NAME)
        _write_empty_kernel(fixed_tpc_path)

        for path_len in range(MAX_PIECE_LEN - 2, MAX_PIECE_LEN + 3):
            filler = "x" * max(0, path_len - len(temp_dir + os.sep + EMPTY_TPC_NAME))
            tpc_path = os.path.join(temp_dir, filler + EMPTY_TPC_NAME)
            assert len(tpc_path) >= path_len
            metakernel_path = os.path.join(temp_dir, "meta.txt")
            _test_metakernel_long_path(metakernel_path, tpc_path, fixed_tpc_path)

            # Put a continuation character at the end to test an especially
            # tricky case.
            stressful_tpc_path = tpc_path[:-1] + "+"
            _test_metakernel_long_path(
                metakernel_path,
                stressful_tpc_path,
                fixed_tpc_path,
            )
