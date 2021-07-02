import logging
from contextlib import ContextDecorator
from os import chdir, getcwd
from os.path import dirname

from .spiceypy import furnsh, ktotal, unload

LOGGER = logging.getLogger(__name__)


def _in_spice_dir(func):
    """Decorator used in the SpiceKernel context manager to load in a given folder."""

    def wrapper(*args, **kwargs):
        """Move to SPICE_FOLDER and run func()."""
        orig_dir = getcwd()
        chdir(args[0].kernel_dir)  # Because args[0] should always be the instance.
        output = func(*args, **kwargs)
        chdir(orig_dir)
        return output

    return wrapper


class SpiceKernel(ContextDecorator):
    """Context manager for having spice loaded."""

    def __init__(self, kernel_file):
        self.kernel_file = kernel_file
        self.kernel_dir = dirname(self.kernel_file)

    @_in_spice_dir
    def __enter__(self):
        """Move to spice directory, load spice kernel."""
        furnsh(self.kernel_file)
        logging.info(
            f"Loaded {self.kernel_file}, {ktotal('ALL')} kernels now loaded."
        )

    @_in_spice_dir
    def __exit__(self, exc, exca, excb):
        unload(self.kernel_file)
        logging.info(
            f"Unloaded {self.kernel_file}, {ktotal('ALL')} kernels still loaded"
        )