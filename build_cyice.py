import os
import platform
from pathlib import Path
from setuptools import Extension
from setuptools.command.build_py import build_py as _build_py

import numpy

host_OS = platform.system()
host_arch = platform.machine()
# Get platform is Unix-like OS or not
is_unix = host_OS in ("Linux", "Darwin", "FreeBSD")

# https://setuptools.pypa.io/en/latest/userguide/ext_modules.html

cspice_dir = os.environ.get("CSPICE_SRC_DIR", "./src/cspice/")

# cspice_c = list(map(str, Path("src/cspice/src/cspice/").glob("*.c")))
# csupport_c = list(map(str, Path("src/cspice/src/csupport/").glob("*.c")))


ext_options = {
    "include_dirs": [
        f"{cspice_dir}include/",
        f"{cspice_dir}/src/cspice/",
        numpy.get_include(),
    ],
    "libraries": ["cspice" if is_unix else "libcspice"],
    "library_dirs": [
        "/usr/local/lib",
        "./src/spiceypy/utils",
    ],
    "language": "c",
    "define_macros": [],
    "extra_compile_args": [],
}

cyice_ext = Extension(
    name="spiceypy.cyice.cyice",
    sources=[
        "./src/spiceypy/cyice/cyice.pyx",
        "./src/spiceypy/cyice/cyice.pxd",
    ],
    **ext_options,
)
