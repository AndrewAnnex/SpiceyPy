"""
The MIT License (MIT)

Copyright (c) [2015-2025] [Andrew Annex]

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

from setuptools import setup, Command, find_packages
from setuptools.command.install import install
from setuptools.command.build_py import build_py
from setuptools.dist import Distribution
import os
import sys
from pathlib import Path

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
    """Class that extends the install command and encapsulates the
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


cmdclass = {
    "install": InstallSpiceyPy,
    "build_py": BuildPyCommand,
}

# https://stackoverflow.com/questions/45150304/how-to-force-a-python-wheel-to-be-platform-specific-when-building-it
# http://lepture.com/en/2014/python-on-a-hard-wheel
try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class generic_bdist_wheel(_bdist_wheel):
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

    # add our override to the cmdclass dict so we can inject this behavior
    cmdclass["bdist_wheel"] = generic_bdist_wheel

except ImportError:
    # we don't have wheel installed so there is nothing to change
    pass


# todo: https://setuptools.pypa.io/en/latest/userguide/extension.html,
# https://setuptools.pypa.io/en/latest/deprecated/distutils/extending.html?highlight=cmdclass#integrating-new-commands

setup(
    distclass=SpiceyPyBinaryDistribution,
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"spiceypy": ["utils/*.so", "utils/*.dylib", "utils/*.dll"]},
    include_package_data=True,
    cmdclass=cmdclass,
)
