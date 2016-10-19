from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from setuptools.dist import Distribution
import sys
import getspice
import os
import subprocess
import platform
import shutil

__author__ = 'AndrewAnnex'

# Get OS platform
host_OS = platform.system()
# Get current working directory
root_dir = os.path.dirname(os.path.realpath(__file__))
# Make the directory path for cspice
cspice_dir = os.path.join(root_dir, 'cspice')
# Make the directory path for cspice/lib
lib_dir = os.path.join(cspice_dir, 'lib')

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

def check_for_spice():
    if not os.path.exists(cspice_dir):
        message = 'Unable to find CSPICE at {0}. Attempting to Download CSPICE For you:'.format(cspice_dir)
        print(message)
        # Download cspice using getspice.py
        getspice.getSpice()
        if not os.path.exists(cspice_dir):
            message = 'Unable to find CSPICE at {0}. Exiting'.format(cspice_dir)
            sys.exit(message)


def unpack_cspice():
    if host_OS == "Linux" or host_OS == "Darwin":
        cspice_lib = os.path.join(lib_dir, ("cspice.lib" if host_OS is "Windows" else "cspice.a"))
        csupport_lib = os.path.join(lib_dir, ("csupport.lib" if host_OS is "Windows" else "csupport.a"))

        if os.path.exists(cspice_lib) and os.path.exists(csupport_lib):
            cwd = os.getcwd()
            try:
                os.chdir(lib_dir)
                if host_OS is "Windows":
                    raise BaseException("Windows is not supported in this build method")
                elif host_OS == "Linux" or host_OS == "Darwin":
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


def build_library():
    if host_OS == "Linux" or host_OS == "Darwin":
        currentDir = os.getcwd()
        try:
            os.chdir(lib_dir)
            #find a way to make this work via Extension and setuptools, not using popen.
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
        finally:
            os.chdir(currentDir)
    elif host_OS == "Windows":
        currentDir = os.getcwd()
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
            pass
        finally:
            os.chdir(currentDir)


def move_to_root_directory():
    sharedLib = 'spice.so' if host_OS == "Linux" or host_OS == "Darwin" else 'cspice.dll'
    destination = os.path.join(root_dir, 'spiceypy', 'utils', sharedLib)
    if not os.path.isfile(destination):
        target = os.path.join(cspice_dir, 'lib', sharedLib) \
                if host_OS == "Linux" or host_OS == "Darwin" else \
                os.path.join(cspice_dir, 'src', 'cspice', sharedLib)
        print("Attempting to move: {0}   to: {1}".format(target, destination))
        try:
            os.rename(target, destination)
        except BaseException as e:
            sys.exit('{0} file not found, what happend?: {1}'.format(sharedLib, e))


def cleanup():
    # Remove CSPICE folder
    try:
        shutil.rmtree(os.path.join(os.getcwd(), "cspice"))
    except OSError as e:
        print("Error Cleaning up cspice folder")
        raise e


def mac_linux_method():
    if host_OS == "Linux" or host_OS == "Darwin":
        # Next unpack cspice.a and csupport.a
        unpack_cspice()
        # Build the shared Library
        build_library()
        # Move to correct location (root of the distribution)
        move_to_root_directory()


def windows_method():
    if host_OS == "Windows":
        if os.path.exists(os.path.join(cspice_dir, "lib", "cspice.dll")):
            print("Found premade cspice.dll, not building")
            return
        elif os.path.exists(os.path.join(root_dir, 'spiceypy', 'utils', 'cspice.dll')):
            print("Found premade cspice.dll in spiceypy, not building")
            return
        else:
            # Build the DLL
            build_library()
            # Move to correct location (root of the distribution)
            move_to_root_directory()


try:
    # First check for spice
    check_for_spice()

    print("Host OS: {}".format(host_OS))
    if host_OS == "Linux" or host_OS == "Darwin":
        mac_linux_method()
    elif host_OS == "Windows":
        windows_method()
    else:
        sys.exit("Unsupported OS: {0}".format(host_OS))

    readme = open('README.rst', 'r')
    readmetext = readme.read()
    readme.close()

    setup(
        name='spiceypy',
        version='1.1.0',
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
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: POSIX :: Linux",
            "Operating System :: Microsoft :: Windows"
        ],
        packages=find_packages(exclude=["*.tests"]),
        include_package_data=True,
        zip_safe=False,
        distclass=BinaryDistribution,
        package_data={'': ['*.so', "*.dll"]},
        install_requires=['six'],
        requires=['numpy', 'pytest', 'six'],
        tests_require=['pytest', 'numpy', 'six'],
        cmdclass={'test': PyTest},
        test_suite='spiceypy.tests.test_wrapper.py',
        extras_require={'testing': ['pytest']}
    )
finally:
    pass

