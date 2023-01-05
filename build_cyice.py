from pathlib import Path
from setuptools import Extension
from setuptools.command.build_py import build_py as _build_py

import numpy
from Cython.Build import cythonize
from Cython.Distutils.build_ext import new_build_ext as cython_build_ext

#https://setuptools.pypa.io/en/latest/userguide/ext_modules.html

# first check if cspice exists, if not download it to src/cspice
if not Path('./src/cspice/src/').exists():
    import get_spice
    get_spice.main(build=False)

cspice_c = list(map(str, Path('./src/cspice/src/cspice/').glob('*.c')))
csupport_c = list(map(str, Path('./src/cspice/src/csupport/').glob('*.c')))

ext_options = {
    'language': 'c',
    'include_dirs': ['src/cspice/include/', numpy.get_include()],
    'define_macros': [],
    'extra_compile_args': ["-m64", "-c", "-ansi", "-O2", "-fPIC"],
}

cythonize_options = {"language_level": 3}


class BuildCyice(_build_py):
    def run(self):
        self.run_command("build_ext")
        return super().run()

    def initialize_options(self):
        super().initialize_options()
        if self.distribution.ext_modules == None:
            self.distribution.ext_modules = []

        self.distribution.ext_modules.append(
            Extension('cyice', ['src/cyice/cyice.pyx', *cspice_c, *csupport_c], **ext_options)
        )

        cythonize(self.distribution.ext_modules, quiet=True)
