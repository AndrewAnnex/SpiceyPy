__author__ = 'Apollo117'
from setuptools import setup
import sys
import os
from subprocess import Popen

module_name = os.path.basename(os.getcwd())
root_dir = os.path.dirname(__file__)
cspice_dir = os.path.join(root_dir, 'cspice')
lib_dir = os.path.join(cspice_dir, 'lib')
data_files = []

if not os.path.exists(cspice_dir):
    message = 'Unable to find cspice toolkit at %s. Please untar the source there' % cspice_dir
    sys.exit(message)


def unpack_cspicelib():
    libfile_path = os.path.join(cspice_dir, 'lib', 'cspice.a')

    if not os.path.exists(libfile_path):
        messageerr = 'Error, cannot find %s/lib/cspice.a , exiting' % cspice_dir
        sys.exit(messageerr)

    currentDir = os.getcwd()

    try:
        os.chdir(lib_dir)
        unpackCspice = Popen('ar -x cspice.a', shell=True)
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
        unpackCsupport = Popen('ar -x csupport.a', shell=True)
        status = os.waitpid(unpackCsupport.pid, 0)[1]

        if status != 0:
            raise BaseException('%d' % status)

    except BaseException as errorInst:
        status = errorInst.args
        sys.exit('Error: csupport .o file extraction failed with exit status: %d' % status)

    finally:
        os.chdir(currentDir)


def buildLib():

    currentDir = os.getcwd()
    try:
        os.chdir(lib_dir)
        build_lib = Popen('gcc -shared -fPIC -lm *.o -o spice.so', shell=True)
        status = os.waitpid(build_lib.pid, 0)[1]
        if status != 0:
            raise BaseException('%d' % status)

    except BaseException as errorInst:
        status = errorInst.args
        sys.exit('Error: compilation of shared spice.so build exit status: %d' % status)
    finally:
        os.chdir(currentDir)


def movetoLib():
    try:
        os.rename(cspice_dir+'/lib/spice.so', os.path.join(root_dir, 'SpiceyPy', 'spice.so'))

    except FileNotFoundError:
        sys.exit('spice.so file not found, what happend?')


def cleanup():
    pass  # not written yet, this should basically just deleted all of those .o files we made and whatever else
    #os.chdir(lib_dir)
    #os.listdir(lib_dir)


try:
    unpack_cspicelib()
    unpack_csupportlib()
    buildLib()
    movetoLib()
    setup(
     name='SpiceyPy',
     version='0.5.0',
     description='A Python Wrapper for the NAIF CSPICE Toolkit using ctypes',
     author='Apollo117',
     packages=['SpiceyPy'],
     requires=['numpy'],
     package_data = {'SpiceyPy': ['*.so']},
     include_package_data=True,
     zip_safe=False
    )

finally:
    cleanup()