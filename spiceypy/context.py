import logging
from contextlib import ContextDecorator, contextmanager
from os import chdir
from pathlib import Path
from types import TracebackType
from typing import Any, Generator, Iterable, Union

from .spiceypy import furnsh, ktotal, unload

LOGGER = logging.getLogger(__name__)


@contextmanager
def _change_dir(change: bool, target_dir: Path) -> Generator[None, None, None]:
    """Change directory to target_dir if change is True."""
    orig_dir = Path.cwd()
    try:
        if change:
            chdir(target_dir)
        yield

    finally:
        if change:
            chdir(orig_dir)


def _make_path(file_string: str) -> Path:
    """Convert a kernel filename string to a Path object and check it is valid."""
    path = Path(file_string)
    if not path.is_file():
        raise FileNotFoundError(f"File {path.name} is not a valid file.")
    return path


class SpiceKernel(ContextDecorator):
    """Context manager for loading and unloading SPICE kernels.

    Loads the kernel(s) given using `spiceypy.furnsh()` and unloads them using
    `spiceypy.unload()` when the context is exited. Can also be called as a decorator
    around a function, which treats the entire function as being in context (i.e. the
    entire function is executed with the kernels loaded).

    :param kernel_files: A kernel file or list of kernel files to load.
    :param allow_change_dir: Whether to change folder to load kernels. Defaults true.
    """

    def __init__(
        self, kernel_files: Union[str, Iterable[str]], allow_change_dir=True
    ) -> None:
        """Initialise the context and check all given files are valid."""

        # If we've been given a single string, make it a list so we can just work on
        # iterable sequences in the class.
        if isinstance(kernel_files, str):
            kernel_files = [kernel_files]

        # Now check each string in the list is a file, and convert to a list of pathlib
        # Path() objects.
        self.kernel_file_list = [_make_path(x) for x in kernel_files]
        self.allow_change_dir = allow_change_dir

    def __enter__(self) -> None:
        """Move to the directory of each kernel, then load it using `furnsh`."""
        for kernel in self.kernel_file_list:
            with _change_dir(self.allow_change_dir, kernel.parent):
                furnsh(str(kernel))
                logging.info(
                    f"Loaded {kernel.name}, {ktotal('ALL')} kernels now loaded."
                )

    def __exit__(self, exc: Any, exca: Any, excb: TracebackType) -> None:
        for kernel in self.kernel_file_list:
            with _change_dir(self.allow_change_dir, kernel.parent):
                unload(str(kernel))
                logging.info(
                    f"Unloaded {kernel.name}, {ktotal('ALL')} kernels still loaded"
                )
