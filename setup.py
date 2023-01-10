from setuptools import setup, find_packages
from build_spiceypy import (
    InstallSpiceyPy,
    BuildPyCommand,
    SpiceyPyWheelBuild,
    SpiceyPyBinaryDistribution,
)
from Cython.Distutils import build_ext
from Cython.Build import cythonize
from build_cyice import cyice_ext


setup(
    distclass=SpiceyPyBinaryDistribution,
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"spiceypy": ["utils/*.so", "utils/*.dylib", "utils/*.dll"]},
    include_package_data=True,
    cmdclass=dict(
        install=InstallSpiceyPy,
        build_py=BuildPyCommand,
        bdist_wheel=SpiceyPyWheelBuild,
        build_ext=build_ext,
    ),
    ext_modules=cythonize([cyice_ext], annotate=True, nthreads=4),
)
