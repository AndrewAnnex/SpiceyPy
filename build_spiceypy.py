from setuptools import setup, Command, find_packages
from setuptools.command.install import install
from setuptools.command.build_py import build_py
from setuptools.command.bdist_wheel import bdist_wheel as _bdist_wheel
from setuptools.dist import Distribution

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
