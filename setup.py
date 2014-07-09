__author__ = 'Apollo117'
from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys
import getspice
import test.gettestkernels as getTestKernels
import os
import subprocess


module_name = os.path.basename(os.getcwd())
# Get current working directory
root_dir = os.path.dirname(__file__)
# Make the directory path for cspice
cspice_dir = os.path.join(root_dir, 'cspice')
# Make the directory path for cspice/lib
lib_dir = os.path.join(cspice_dir, 'lib')
data_files = []


# py.test integration from pytest.org
class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        getTestKernels.downloadKernels()
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


def check_for_spice():
    if not os.path.exists(cspice_dir):
        message = 'Unable to find CSPICE at {0}. Attempting to Download CSPICE For you:'.format(cspice_dir)
        print(message)
        # Download cspice using getspice.py
        getspice.getSpice()
        if not os.path.exists(cspice_dir):
            message = 'Unable to find CSPICE at {0}. Exiting'.format(cspice_dir)
            sys.exit(message)


def unpack_cspicelib():
    libfile_path = os.path.join(cspice_dir, 'lib', 'cspice.a')

    if not os.path.exists(libfile_path):
        messageerr = 'Error, cannot find %s/lib/cspice.a , exiting' % cspice_dir
        sys.exit(messageerr)

    currentDir = os.getcwd()

    try:
        os.chdir(lib_dir)
        unpackCspice = subprocess.Popen('ar -x cspice.a', shell=True)
        status = os.waitpid(unpackCspice.pid, 0)[1]

        if status != 0:
            raise BaseException('%d' % status)

    except BaseException as errorInst:
        status = errorInst.args
        sys.exit('Error: cspice .o file extraction failed with exit status: %d' % status)

    finally:
        os.chdir(currentDir)


def unpack_csupportlib():
    libfile_path = os.path.join(cspice_dir, 'lib', 'csupport.a')

    if not os.path.exists(libfile_path):
        messageerr = 'Error, cannot find %s/lib/csupport.a , exiting' % cspice_dir
        sys.exit(messageerr)

    currentDir = os.getcwd()

    try:
        os.chdir(lib_dir)
        unpackCsupport = subprocess.Popen('ar -x csupport.a', shell=True)
        status = os.waitpid(unpackCsupport.pid, 0)[1]

        if status != 0:
            raise BaseException('%d' % status)

    except BaseException as errorInst:
        status = errorInst.args
        sys.exit('Error: csupport .o file extraction failed with exit status: %d' % status)

    finally:
        os.chdir(currentDir)


def build_library():
    currentDir = os.getcwd()
    try:
        os.chdir(lib_dir)
        #find a way to make this work via Extension and setuptools, not using popen.
        build_lib = subprocess.Popen('gcc -shared -fPIC -lm *.o -o spice.so', shell=True)
        status = os.waitpid(build_lib.pid, 0)[1]
        if status != 0:
            raise BaseException('%d' % status)

    except BaseException as errorInst:
        status = errorInst.args
        sys.exit('Error: compilation of shared spice.so build exit status: %d' % status)
    finally:
        os.chdir(currentDir)


def move_to_root_directory():
    try:
        os.rename(cspice_dir+'/lib/spice.so', os.path.join(root_dir, 'SpiceyPy', 'spice.so'))

    except FileNotFoundError:
        sys.exit('spice.so file not found, what happend?')


def cleanup():
    # Delete the extra files created by this file
    os.chdir(lib_dir)
    currentDir = os.getcwd()
    cleanupList = [file for file in os.listdir(currentDir) if file.endswith('.o') or file.endswith('.so')]
    for file in cleanupList:
        os.remove(file)
    pass

try:
    #First check for spice
    check_for_spice()
    #Next unpack cspice.a
    unpack_cspicelib()
    #Next unpack csupport.a
    unpack_csupportlib()
    #Build the shared Library
    build_library()
    #Move to correct location (root of the distribution)
    move_to_root_directory()
    setup(
        name='SpiceyPy',
        version='0.5.2',
        description='A Python Wrapper for the NAIF CSPICE Toolkit using ctypes',
        author='Apollo117',
        packages=['SpiceyPy'],
        tests_require=['pytest'],
        cmdclass={'test': PyTest},
        test_suite='test.test_wrapper.py',
        requires=['numpy', 'pytest', 'coveralls', 'coverage', 'six'],
        package_data={'SpiceyPy': ['*.so']},
        include_package_data=True,
        zip_safe=False,
        extras_require={
            'testing': ['pytest'],
        }

    )

finally:
    cleanup()