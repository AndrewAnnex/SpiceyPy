import sys
from pathlib import Path

from setuptools import setup, find_packages, Command, Extension
from setuptools.command.install import install
from setuptools.command.build_py import build_py
from setuptools.dist import Distribution
from Cython.Distutils import build_ext
from Cython.Build import cythonize
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

# import numpy
# https://setuptools.pypa.io/en/latest/userguide/ext_modules.html

# I can just use the shared library!
# cspice_c = list(map(str, Path("src/cspice/src/cspice/").glob("*.c")))
# csupport_c = list(map(str, Path("src/cspice/src/csupport/").glob("*.c")))

ext_options = {
    "include_dirs": [
        "src/cspice/include/",
        "src/cspice/src/cspice/",
    ],
    "libraries": ["m", "cspice"],
    "library_dirs": ["/usr/local/lib", "src/spiceypy/utils"],
    "language": "c",
    "define_macros": [],
    "extra_compile_args": ["-m64"],
}

cythonize_options = {"language_level": 3}

cyice_ext = Extension(
    name="spiceypy.cyice.cyice",
    sources=[
        "./src/spiceypy/cyice/cyice.pyx",
        "./src/spiceypy/cyice/cyice.pxd",
    ],
    **ext_options
)

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
        return super().run()


class BuildPyCommand(build_py):
    """Custom build command to ensure cspice is built and packaged"""

    def run(self):
        try_get_spice()
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

    def get_tag(self) -> (str, str, str):
        self.root_is_pure = False
        python, abi, plat = super().get_tag()
        self.root_is_pure = False
        return "py3", "none", plat


setup(
    distclass=SpiceyPyBinaryDistribution,
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={
        "spiceypy": ["utils/*.so", "utils/*.dylib", "utils/*.dll"],
        "*": ["get_spice.py", "build_cyice.py", "build_spiceypy.py"],
    },
    include_package_data=True,
    cmdclass=dict(
        install=InstallSpiceyPy,
        build_py=BuildPyCommand,
        bdist_wheel=SpiceyPyWheelBuild,
        build_ext=build_ext,
    ),
    ext_modules=cythonize([cyice_ext], annotate=True, nthreads=4),
)
