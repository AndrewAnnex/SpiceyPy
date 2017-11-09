"""
The MIT License (MIT)

Copyright (c) [2015-2017] [Andrew Annex]

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
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.test import test as TestCommand
from setuptools.dist import Distribution
import ssl
import sys
import os
import subprocess
import platform
import shutil

__author__ = 'AndrewAnnex'

# Get OS platform
host_OS = platform.system()
# Get platform is Unix-like OS or not
is_unix = host_OS in ("Linux", "Darwin", "FreeBSD")
# Get current working directory
root_dir = os.path.dirname(os.path.realpath(__file__))
# Make the directory path for cspice
cspice_dir = os.path.join(root_dir, 'cspice')
# Make the directory path for cspice/lib
lib_dir = os.path.join(cspice_dir, 'lib')

TEST_DEPENDENCIES = ['numpy>=1.12.0', 'six>=1.9.0', 'pytest>=2.9.0']
DEPENDENCIES = ['numpy>=1.12.0', 'six>=1.9.0', 'certifi>=2017.1.23']
REQUIRES = ['numpy', 'six']

# If we have an old version of OpenSSL, CSPICE will be downloaded
# (if required) using urllib3.  Extend the list of required packages.
if ssl.OPENSSL_VERSION < 'OpenSSL 1.0.1g':
    DEPENDENCIES.extend(['urllib3[secure]>=1.22', 'pyOpenSSL>=17.3.0'])


# py.test integration from pytest.org
class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


class BinaryDistribution(Distribution):
    def is_pure(self):
        return False


class InstallSpiceyPy(install):
    """Class that extends the install command and encapsulates the
    process for installing the required CSPICE distribution at the
    right place.
    """

    def run(self):
        self.check_for_spice()

        print("Host OS: {0}".format(host_OS))
        if is_unix:
            self.unix_method()
        elif host_OS == "Windows":
            self.windows_method()
        else:
            sys.exit("Unsupported OS: {0}".format(host_OS))

        install.run(self)

    @staticmethod
    def check_for_spice():
        print('Checking the path', cspice_dir)
        if not os.path.exists(cspice_dir):
            import getspice
            message = 'Unable to find CSPICE at {0}. Attempting to Download CSPICE For you:'.format(cspice_dir)
            print(message)
            # Download cspice using getspice.py
            getspice.GetCSPICE(version='N0066')
            if not os.path.exists(cspice_dir):
                message = 'Unable to find CSPICE at {0}. Exiting'.format(cspice_dir)
                sys.exit(message)

    @staticmethod
    def unpack_cspice():
        if is_unix:
            cspice_lib = os.path.join(lib_dir, ("cspice.lib" if host_OS is "Windows" else "cspice.a"))
            csupport_lib = os.path.join(lib_dir, ("csupport.lib" if host_OS is "Windows" else "csupport.a"))

            if os.path.exists(cspice_lib) and os.path.exists(csupport_lib):
                cwd = os.getcwd()
                try:
                    os.chdir(lib_dir)
                    if host_OS is "Windows":
                        raise BaseException("Windows is not supported in this build method")
                    elif is_unix:
                        for lib in ["ar -x cspice.a", "ar -x csupport.a"]:
                            unpack_lib_process = subprocess.Popen(lib, shell=True)
                            process_status = os.waitpid(unpack_lib_process.pid, 0)[1]
                            if process_status != 0:
                                raise BaseException('{0}'.format(process_status))
                    else:
                        raise BaseException("Unsupported OS: {0}".format(host_OS))
                except BaseException as error:
                    status = error.args
                    sys.exit('Error: cspice object file extraction failed with exit status: {0}'.format(status))
                finally:
                    os.chdir(cwd)
            else:
                error_Message = "Error, cannot find CSPICE " \
                                "static libraries at {0}".format(lib_dir)
                sys.exit(error_Message)

    @staticmethod
    def build_library():
        # Get the current working directory
        cwd = os.getcwd()

        if is_unix:
            try:
                os.chdir(lib_dir)
                # find a way to make this work via Extension and setuptools, not using popen.
                build_lib = subprocess.Popen('gcc -shared -fPIC -lm *.o -o spice.so', shell=True)
                status = os.waitpid(build_lib.pid, 0)[1]
                if status != 0:
                    raise BaseException('{0}'.format(status))
                success = os.path.exists(os.path.join(os.getcwd(), 'spice.so'))
                if not success:
                    raise BaseException("Did not find spice.so, build went badly.")
            except BaseException as errorInst:
                status = errorInst.args
                sys.exit('Error: compilation of shared spice.so build exit status: {0}'.format(status))

        elif host_OS == "Windows":
            try:
                destination = os.path.join(cspice_dir, "src", "cspice")
                defFile = os.path.join(root_dir, "appveyor", "cspice.def")
                makeBat = os.path.join(root_dir, "appveyor", "makeDynamicSpice.bat")
                shutil.copy(defFile, destination)
                shutil.copy(makeBat, destination)
                # run the script
                os.chdir(destination)
                windows_build = subprocess.Popen("makeDynamicSpice.bat", shell=True)
                status = windows_build.wait()
                if status != 0:
                    raise BaseException('{0}'.format(status))
            except BaseException as error:
                sys.exit("Build failed with: {0}".format(error.args))
        # Change back to the stored 'current working directory
        os.chdir(cwd)

    @staticmethod
    def move_to_root_directory():
        sharedlib = 'spice.so' if is_unix else 'cspice.dll'
        destination = os.path.join(root_dir, 'spiceypy', 'utils', sharedlib)
        if not os.path.isfile(destination):
            if is_unix:
                target = os.path.join(cspice_dir, 'lib', sharedlib)
            else:
                target = os.path.join(cspice_dir, 'src', 'cspice', sharedlib)
            print("Attempting to move: {0}   to: {1}".format(target, destination))
            try:
                os.rename(target, destination)
            except BaseException as e:
                sys.exit('{0} file not found, what happend?: {1}'.format(sharedlib, e))

    @staticmethod
    def cleanup():
        # Remove CSPICE folder
        try:
            shutil.rmtree(os.path.join(os.getcwd(), "cspice"))
        except OSError as e:
            print("Error Cleaning up cspice folder")
            raise e

    def unix_method(self):
        # Unpack cspice.a and csupport.a
        self.unpack_cspice()
        # Build the shared Library
        self.build_library()
        # Move to correct location (root of the distribution)
        self.move_to_root_directory()

    def windows_method(self):
        if os.path.exists(os.path.join(cspice_dir, "lib", "cspice.dll")):
            print("Found pre-made cspice.dll, not building")
        elif os.path.exists(os.path.join(root_dir, 'spiceypy', 'utils', 'cspice.dll')):
            print("Found pre-made cspice.dll in spiceypy, not building")
        else:
            # Build the DLL
            self.build_library()
            # Move to correct location (root of the distribution)
            self.move_to_root_directory()


readme = open('README.rst', 'r')
readmetext = readme.read()
readme.close()

setup(
    name='spiceypy',
    version='2.1.0',
    license='MIT',
    author='Andrew Annex',
    author_email='ama6fy@virginia.edu',
    description='A Python Wrapper for the NAIF CSPICE Toolkit',
    long_description=readmetext,
    keywords=['spiceypy', 'spice', 'naif', 'jpl', 'space', 'geometry'],
    url='https://github.com/AndrewAnnex/SpiceyPy',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Astronomy",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: POSIX :: BSD :: FreeBSD",
        "Operating System :: Microsoft :: Windows"
    ],
    packages=find_packages(exclude=["*.tests"]),
    include_package_data=True,
    zip_safe=False,
    distclass=BinaryDistribution,
    package_data={'': ['*.so', "*.dll"]},
    setup_requires=DEPENDENCIES,
    install_requires=DEPENDENCIES,
    requires=REQUIRES,
    tests_require=TEST_DEPENDENCIES,
    cmdclass={
        'install': InstallSpiceyPy,
        'test': PyTest},
    test_suite='spiceypy.tests.test_wrapper.py',
    extras_require={'testing': ['pytest']}
)
