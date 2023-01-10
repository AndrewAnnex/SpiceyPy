from pathlib import Path
from setuptools import Extension
from setuptools.command.build_py import build_py as _build_py

import numpy

# https://setuptools.pypa.io/en/latest/userguide/ext_modules.html

cspice_c = list(map(str, Path("src/cspice/src/cspice/").glob("*.c")))
csupport_c = list(map(str, Path("src/cspice/src/csupport/").glob("*.c")))

ext_options = {
    "include_dirs": [
        "src/cspice/include/",
        "src/cspice/src/cspice/",
        "src/cspice/src/csupport/",
    ],
    "libraries": ["m", "src/cspice/lib/cspice.a", "src/cspice/lib/csupport.a"],
    "library_dirs": ["/usr/local/lib", "src/spiceypy/utils"],
    "language": "c",
    "define_macros": [],
    "extra_compile_args": ["-m64"],
}

cythonize_options = {"language_level": 3}

cyice_ext = Extension(
    name="cyice",
    sources=[
        "./src/spiceypy/cyice/cyice.pyx",
        *cspice_c,
        *csupport_c,
    ],
    **ext_options
)
