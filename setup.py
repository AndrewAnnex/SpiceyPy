"""
The MIT License (MIT)

Copyright (c) [2015-2019] [Andrew Annex]

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
__author__ = "AndrewAnnex"

from setuptools import setup, Command
from setuptools.command.install import install
from setuptools.command.build_py import build_py
from setuptools.dist import Distribution

from get_spice import InstallCSpice

TEST_DEPENDENCIES = [
    'numpy>=1.17.0;python_version>="3.5"',
    "pytest>=2.9.0",
    "pandas>=0.24.0",
]
DEPENDENCIES = [
    'numpy>=1.17.0;python_version>="3.5"',
]
REQUIRES = ["numpy"]


class SpiceyPyBinaryDistribution(Distribution):
    def is_pure(self):
        return False

    def root_is_pure(self):
        return False


class InstallSpiceyPy(install):
    """Class that extends the install command and encapsulates the
    process for installing the required CSPICE distribution at the
    right place.
    """

    def finalize_options(self):
        install.finalize_options(self)
        self.install_lib = self.install_platlib

    def run(self):
        InstallCSpice.get_cspice()
        install.run(self)


class GetCSPICECommand(Command):
    """ Custom command to get the correct cspice and build the shared library for spiceypy """

    description = "downloads cspice and builds the shared library"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        InstallCSpice.get_cspice()


class BuildPyCommand(build_py):
    """ Custom build command to ensure cspice is built and packaged """

    def run(self):
        InstallCSpice.get_cspice()
        build_py.run(self)


cmdclass = {
    "install": InstallSpiceyPy,
    "build_py": BuildPyCommand,
    "get_cspice": GetCSPICECommand,
}

readme = open("README.rst", "r")
readmetext = readme.read()
readme.close()

setup(
    name="spiceypy",
    version="3.1.1",
    license="MIT",
    author="Andrew Annex",
    author_email="ama6fy@virginia.edu",
    description="A Python Wrapper for the NAIF CSPICE Toolkit",
    long_description=readmetext,
    python_requires=">=3.6, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4",
    keywords=["spiceypy", "spice", "naif", "jpl", "space", "geometry"],
    url="https://github.com/AndrewAnnex/SpiceyPy",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Astronomy",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: POSIX :: BSD :: FreeBSD",
        "Operating System :: Microsoft :: Windows",
    ],
    packages=["spiceypy", "spiceypy.tests", "spiceypy.utils"],
    include_package_data=True,
    zip_safe=False,
    distclass=SpiceyPyBinaryDistribution,
    package_data={"spiceypy": ["utils/*.so", "utils/*.dll"]},
    setup_requires=DEPENDENCIES,
    install_requires=DEPENDENCIES,
    requires=REQUIRES,
    tests_require=TEST_DEPENDENCIES,
    cmdclass=cmdclass,
    test_suite="spiceypy.tests.test_wrapper.py",
    extras_require={"testing": ["pytest"]},
)
