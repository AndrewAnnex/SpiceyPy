import sys
import os
import platform
from pathlib import Path

import numpy
from setuptools import setup, find_packages, Command, Extension
from setuptools.command.install import install
from setuptools.command.build_py import build_py
from setuptools.command.bdist_wheel import bdist_wheel as _bdist_wheel
from setuptools.dist import Distribution
try:
    from Cython.Build import cythonize
    from Cython.Distutils import build_ext
    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False
    

host_OS = platform.system()
host_arch = platform.machine()
# Get platform is Unix-like OS or not
is_unix = host_OS in ("Linux", "Darwin", "FreeBSD")

# https://setuptools.pypa.io/en/latest/userguide/ext_modules.html

passnumber = 0


def try_get_spice():
    global passnumber
    print("try_get_spice", passnumber)
    if passnumber > 0:
        print("already built libcspice")
        return
    try:
        thisfile = Path(__file__).resolve(strict=False)
        curdir = thisfile.parent
        sys.path.append(str(curdir))
        from get_spice import main

        main()
        passnumber += 1
    except Exception as e:
        print("Caught file not found")
        print(e)
        pass
    except ModuleNotFoundError as mnfe:
        print("Could not import try_get_spice")
        pass
    return


def get_cyice_extension(default_path: str = "./src/cspice/"):
    cyice_ext = 'pyx' if USE_CYTHON else 'c'

    cspice_dir = Path(os.environ.get("CSPICE_SRC_DIR", default_path))

    ext_options = {
        "include_dirs": [
            f"{cspice_dir / 'include/'}",
            f"{cspice_dir / 'src/cspice/'}",
            numpy.get_include(),
        ],
        "libraries": ["cspice" if is_unix else "libcspice"],
        "library_dirs": [
            "./src/spiceypy/utils",
        ],
        "language": "c",
        "define_macros": [],
        "extra_compile_args": [],
    }

    cyice_ext = Extension(
        name="spiceypy.cyice.cyice",
        sources=[
            f"./src/spiceypy/cyice/cyice.{cyice_ext}",
        ],
        **ext_options,
    )
    return cyice_ext


class SpiceyPyBinaryDistribution(Distribution):
    def is_pure(self):
        return False

    def root_is_pure(self):
        return False


class InstallSpiceyPy(install):
    """
    Class that extends the install command and encapsulates the
    process for installing the required CSPICE distribution at the
    right place.
    """

    def finalize_options(self):
        super().finalize_options()
        self.install_lib = self.install_platlib

    def run(self):
        try_get_spice()
        self.run_command("build_ext")
        return super().run()


class BuildPyCommand(build_py):
    """Custom build command to ensure cspice is built and packaged"""

    def run(self):
        try_get_spice()
        self.run_command("build_ext")
        return super().run()


class SpiceyPyWheelBuild(_bdist_wheel):
    """
    override for bdist_wheel
    """

    root_is_pure = False

    def finalize_options(self) -> None:
        self.root_is_pure = False
        super().finalize_options()
        self.root_is_pure = False

cmd_class = dict(
    install=InstallSpiceyPy,
    build_py=BuildPyCommand,
    bdist_wheel=SpiceyPyWheelBuild,
)

ext_modules = [get_cyice_extension()]

if USE_CYTHON:
    cmd_class['build_ext'] = build_ext
    ext_modules = cythonize(ext_modules, annotate=True, nthreads=2)

setup(
    distclass=SpiceyPyBinaryDistribution,
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={
        "spiceypy": [
            "utils/*.so",
            "utils/*.dylib",
            "utils/*.dll",
            "utils/*.lib",
            "cyice/*.c",
            "cyice/*.so",
            "cyice/*.pyd",
            "cyice/*.pyx",
            "cyice/*.pxd",
        ],
        "*": ["get_spice.py"],
    },
    include_package_data=True,
    cmdclass=cmd_class,
    ext_modules=ext_modules,
)
