"""
The MIT License (MIT)

Copyright (c) [2015-2021] [Andrew Annex]

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
import os
import sys
from pathlib import Path


def try_get_spice():
    try:
        file = Path(__file__).resolve()
        curdir = file.parent
        sys.path.append(str(curdir))
        from get_spice import main

        main()

    except ModuleNotFoundError as mnfe:
        print("Could not import try_get_spice")
        raise mnfe
        pass

class InstallSpiceyPy(install):
    """Class that extends the install command and encapsulates the
    process for installing the required CSPICE distribution at the
    right place.
    """

    def finalize_options(self):
        install.finalize_options(self)
        self.install_lib = self.install_platlib

    def run(self):
        try:
            try_get_spice()
        except ModuleNotFoundError as mnfe:
            print("Could not import try_get_spice")
            raise mnfe
        finally:
            install.run(self)

class BuildPyCommand(build_py):
    """Custom build command to ensure cspice is built and packaged"""

    def run(self):
        try:
            try_get_spice()
        except ModuleNotFoundError as mnfe:
            print("Could not import try_get_spice")
            raise mnfe
        finally:
            build_py.run(self)


cmdclass = {
    "install": InstallSpiceyPy,
    "build_py": BuildPyCommand, #TODO override build_ext instead?
}

# https://stackoverflow.com/questions/45150304/how-to-force-a-python-wheel-to-be-platform-specific-when-building-it
# http://lepture.com/en/2014/python-on-a-hard-wheel
try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class generic_bdist_wheel(_bdist_wheel):
        """
        override for bdist_wheel
        """

        def run(self):
            try:
                try_get_spice()
            except ModuleNotFoundError as mnfe:
                print("Could not import try_get_spice")
                raise mnfe
            finally:
                _bdist_wheel.run(self)

        def finalize_options(self) -> None:
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = False

        def get_tag(self) -> (str, str, str):
            python, abi, plat = _bdist_wheel.get_tag(self)
            return "py3", "none", plat

    # add our override to the cmdclass dict so we can inject this behavior
    cmdclass["bdist_wheel"] = generic_bdist_wheel

except ImportError:
    # we don't have wheel installed so there is nothing to change
    pass


readme = open("README.rst", "r")
readmetext = readme.read()
readme.close()

# todo: https://setuptools.pypa.io/en/latest/userguide/extension.html, 
# https://setuptools.pypa.io/en/latest/deprecated/distutils/extending.html?highlight=cmdclass#integrating-new-commands

setup(
    cmdclass=cmdclass, 
)
