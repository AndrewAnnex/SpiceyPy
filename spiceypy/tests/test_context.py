"""
The MIT License (MIT)

Copyright (c) [2015-2021] [Andrew Annex]

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
from unittest.mock import patch

import pytest

import spiceypy as spice
from spiceypy.context import SpiceKernel
from spiceypy.tests.gettestkernels import (
    CoreKernels,
    cleanup_core_kernels,
    get_standard_kernels,
    write_test_meta_kernel,
)


class ManualException(Exception):
    """Error class to be raised for explicit testing. Use this so no other exceptions
    are erroneously caught.
    """
    pass


def setup_module(module):
    get_standard_kernels()
    write_test_meta_kernel()


def teardown_module(module):
    cleanup_core_kernels()


def assert_loaded_kernels(num: int) -> None:
    """Asserts that the number of loaded kernels is equal to num."""
    assert spice.ktotal("ALL") == num


@pytest.mark.parametrize(
    ["expected_num", "arg_to_pass"],
    [
        (1, CoreKernels.spk),
        (len(CoreKernels.standardKernelList) + 1, CoreKernels.testMetaKernel),
        (len(CoreKernels.standardKernelList), CoreKernels.standardKernelList),
    ],
)
def test_spicekernel_enter_exit(expected_num, arg_to_pass):
    """Test that a single kernel is correctly loaded and unloaded."""
    assert_loaded_kernels(0)
    with SpiceKernel(arg_to_pass):
        assert_loaded_kernels(expected_num)
    assert_loaded_kernels(0)


def test_spicekernel_enter_exit_invalid_list():
    """Ensure that an error is raised if one of the kernels is invalid."""
    assert_loaded_kernels(0)
    with pytest.raises(FileNotFoundError):
        kernels = CoreKernels.standardKernelList + ["invalid/file.txt"]
        with SpiceKernel(kernels):
            # If we get here, raise an error that isn't caught because the test has
            # failed.
            AssertionError("Expected error not raised")


def test_spicekernel_exit_with_error():
    """Ensure that kernels are still properly unloaded on an error."""
    try:
        assert_loaded_kernels(0)
        with SpiceKernel(CoreKernels.testMetaKernel):
            assert_loaded_kernels(len(CoreKernels.standardKernelList) + 1)
            raise ManualException
    except ManualException:
        assert_loaded_kernels(0)


def test_spicekernel_directory_change_user_transparent():
    """Test that the working directory is properly restored inside and after the
    context manager (ensuring user transparency)."""
    initial_dir = os.getcwd()
    with SpiceKernel(CoreKernels.testMetaKernel):
        assert initial_dir == os.getcwd()

        # Now change directory to ensure the exit maintains the change.
        os.chdir("..")
        inside_dir = os.getcwd()
    assert inside_dir == os.getcwd()


@patch("spiceypy.context.chdir")
def test_spicekernel_allow_change_dir(chdir_mock):
    """Check that the allow_change_dir argument of SpiceKernel works."""
    assert_loaded_kernels(0)
    with SpiceKernel(CoreKernels.spk, allow_change_dir=False):
        assert_loaded_kernels(1)
    chdir_mock.assert_not_called()
