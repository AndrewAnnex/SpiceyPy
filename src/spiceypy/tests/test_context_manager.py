import spiceypy as spice
from spiceypy.tests.gettestkernels import (
    get_standard_kernels,
    write_test_meta_kernel,
    cleanup_core_kernels,
    CoreKernels,
)
import pytest

get_standard_kernels()
write_test_meta_kernel()
# cleanup_core_kernels()


@pytest.mark.parametrize(
    ["expected_length", "kernel_list"],
    [
        (1, CoreKernels.lsk),
        (len(CoreKernels.standardKernelList) + 1, CoreKernels.testMetaKernel),
        (2, [CoreKernels.lsk, CoreKernels.pck]),
        (
            len(CoreKernels.standardKernelList) + 2,
            [CoreKernels.lsk, CoreKernels.testMetaKernel],
        ),
    ],
)
def test_input_types(expected_length, kernel_list):
    """
    Ensure that a single kernel, a single meta-kernel, a list of kernels, a
    list of meta-kernel files, and a list that combines both, are all valid
    inputs.
    """
    assert spice.ktotal("all") == 0
    with spice.KernelPool(kernel_list):
        assert spice.ktotal("all") == expected_length
    assert spice.ktotal("all") == 0


@pytest.mark.parametrize(
    ["local_len", "global_len", "local_kernels", "global_kernels"],
    [
        (1, 1, [CoreKernels.lsk], [CoreKernels.pck]),
        (
            1,
            len(CoreKernels.standardKernelList) + 1,
            [CoreKernels.lsk],
            CoreKernels.testMetaKernel,
        ),
        (
            len(CoreKernels.standardKernelList) + 1,
            len(CoreKernels.standardKernelList) + 1,
            CoreKernels.testMetaKernel,
            CoreKernels.testMetaKernel,
        ),
        (
            len(CoreKernels.standardKernelList) + 1,
            1,
            CoreKernels.testMetaKernel,
            [CoreKernels.lsk],
        ),
    ],
)
def test_side_effect(local_len, global_len, local_kernels, global_kernels):
    """
    Ensure that local kernels are only accessible inside the context manager,
    and that global kernels can be accessed both before, and after the context
    manager, but not inside it.
    """
    assert spice.ktotal("all") == 0
    try:
        spice.furnsh(global_kernels)
        assert spice.ktotal("all") == global_len
        with spice.KernelPool(local_kernels):
            assert spice.ktotal("all") == local_len
        assert spice.ktotal("all") == global_len
    finally:
        spice.kclear()
    assert spice.ktotal("all") == 0


def test_invalid_input():
    """
    Ensure that kernels are still unloaded if an exception is raised while
    loading them.
    """
    assert spice.ktotal("all") == 0
    kernels = CoreKernels.standardKernelList + ["foo.file"]
    with pytest.raises(spice.utils.exceptions.SpiceNOSUCHFILE):
        with spice.KernelPool(kernels):
            pass
    assert spice.ktotal("all") == 0


@pytest.mark.parametrize(
    ["expected_len", "kernel_list"],
    [
        (1, CoreKernels.lsk),
        (len(CoreKernels.standardKernelList) + 1, CoreKernels.testMetaKernel),
        (2, [CoreKernels.lsk, CoreKernels.pck]),
        (
            len(CoreKernels.standardKernelList) + 2,
            [CoreKernels.lsk, CoreKernels.testMetaKernel],
        ),
    ],
)
def test_unload_if_error(expected_len, kernel_list):
    """
    Ensure that kernels are unloaded if an error occurs within the context
    manager.
    """
    assert spice.ktotal("all") == 0
    with pytest.raises(
        spice.utils.exceptions.SpiceyPyRuntimeError, match="Error in user code"
    ):
        with spice.KernelPool(kernel_list):
            assert spice.ktotal("all") == expected_len
            raise spice.utils.exceptions.SpiceyPyRuntimeError("Error in user code")
    assert spice.ktotal("all") == 0


def test_actually_works():
    """
    Check if a spice function that depends on kernels works within the
    context manager.
    """
    assert spice.ktotal("all") == 0
    with spice.KernelPool([CoreKernels.lsk]):
        assert spice.str2et("06-28-2000") == 15422464.184185712
    assert spice.ktotal("all") == 0
