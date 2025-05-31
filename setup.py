import sys
import os
import platform
from pathlib import Path

import numpy
from setuptools import setup, find_packages, Command, Extension
from setuptools.command.install import install
from setuptools.command.build_py import build_py
from setuptools.command.bdist_wheel import bdist_wheel as _bdist_wheel
from setuptools.dist import Distribution
try:
    from Cython.Build import cythonize
    from Cython.Build import build_ext
    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False
    

host_OS = platform.system()
host_arch = platform.machine()
# Get platform is Unix-like OS or not
is_linux = host_OS == 'Linux'
is_macos = host_OS in ("Darwin", "FreeBSD")
is_unix = is_linux or is_macos

# https://setuptools.pypa.io/en/latest/userguide/ext_modules.html

passnumber = 0


def try_get_spice():
    global passnumber
    print("try_get_spice", passnumber)
    if passnumber > 0:
        print("already built libcspice")
        return
    try:
        # first attempt to locate existing shared libraries and headers for cspice
        cspice_header_include_dir, cspice_shared_library_dir = get_cspice_headers_and_lib_dirs()
        print(cspice_header_include_dir, ' header')
        print(cspice_shared_library_dir, ' shared')
        # if either is none we need to actually call get_spice.py
        if not cspice_header_include_dir or not cspice_shared_library_dir:
            print('Did not locate either the cspice shared library or headers, attempting to build.')
            thisfile = Path(__file__).resolve(strict=False)
            curdir = thisfile.parent
            sys.path.append(str(curdir))
            from get_spice import main
            main()
        # else we are probably done
        passnumber += 1
    except Exception as e:
        print("Caught file not found")
        print(e)
        pass
    except ModuleNotFoundError as mnfe:
        print("Could not import try_get_spice")
        pass
    return


def path_to_folder(path:Path) -> Path:
    """
    Resolve a path or path to a file to a path
      (the parent of the file if a file)
    """
    path = path.resolve()
    if path.is_file():
        return path.parent
    return path

def folder_has_libcspice(path: Path):
    # first check to ensure the path exists
    if not path.exists():
        # if the path doesn't even exist just short cut to "no"
        return None
    # resolve to a path
    path = path_to_folder(path)
    # define the extensions we care about
    exts = {'.so', '.dylib', '.dll'} 
    # glob anything with cspice in the name
    results = list(path.glob('*cspice*'))
    # return the first file that matches an extension we care about, else none
    for ext in exts:
        for r in results:
            if r.suffix == ext:
                return r.absolute()
    # else we never found it, so return None
    return None

def get_cspice_lib_dir():
    # set the variables to start
    cspice_shared_library_dir = None
    # set the system prefix, if we are in a conda environment use it instead
    prefix = Path(os.environ.get("CONDA_PREFIX", sys.prefix))
    src_dir = Path(os.environ.get("CSPICE_SRC_DIR", "./src/cspice/"))
    utils_dir = Path("./src/spiceypy/utils/").resolve()
    _shared_lib_var = os.environ.get("CSPICE_SHARED_LIB")
    # try :
    #    1) the user provided path to the shared library, 
    #    2) the src dir for the project
    #    3) lib
    #    4) lib64
    lib_candidates: list[Path] = [
        prefix / "lib", 
        prefix / "lib64",
        src_dir,
        utils_dir,
    ]
    if _shared_lib_var:
        lib_candidates = [Path(_shared_lib_var), *lib_candidates]
    # try each possibility for cspice shared library
    for can in lib_candidates:
        _path_to_cspice = folder_has_libcspice(can)
        if _path_to_cspice is not None:
            # we found the cspice shared library, so grab the parent path and continue
            cspice_shared_library_dir = str(_path_to_cspice.parent)
            # we can break
            break
    # finally return whatever we got
    return cspice_shared_library_dir


def get_cspice_headers_include_dir():
    # set the variables to start
    cspice_header_include_dir = None
    # set the system prefix, if we are in a conda environment use it instead
    prefix = Path(os.environ.get("CONDA_PREFIX", sys.prefix))
    src_dir = Path(os.environ.get("CSPICE_SRC_DIR", "./src/cspice/"))
    # locate the cspice header folder (should be prefix/include/cspice folder and look for SpiceUsr.h inside that)
    header_candidates: list[Path] = [
        prefix / "include/cspice/",
        src_dir / "include/",
    ]
    # try each possible header location and look for SpiceUsr.h
    for can in header_candidates:
        if can.exists():
            _path_to_spice_header = can.resolve() / 'SpiceUsr.h'
            if _path_to_spice_header.exists():
                # we found the header folder 
                cspice_header_include_dir = str(_path_to_spice_header.parent)
                # now we can exit the loop
                break
    # finally return whatever we got
    return cspice_header_include_dir


def get_cspice_headers_and_lib_dirs():
    """
    Get the cspice header and shared library locations for the installation
    """
    # attempt to find the headers folder
    cspice_header_include_dir = get_cspice_headers_include_dir()
    # now attempt to locate the shared library folder
    cspice_shared_library_dir = get_cspice_lib_dir()
    # now we are done! 
    return cspice_header_include_dir, cspice_shared_library_dir


def get_cyice_extension():
    """
    Build the cyice extension
    """
    # first attempt to locate existing shared libraries and headers for cspice
    cspice_header_include_dir, cspice_shared_library_dir = get_cspice_headers_and_lib_dirs()
    # if not both of these try to get spice manually
    if not cspice_header_include_dir or not cspice_shared_library_dir:
        # try and get spice
        try_get_spice()
        # attempt to re-get the paths
        cspice_header_include_dir, cspice_shared_library_dir = get_cspice_headers_and_lib_dirs()
    # at this point both the shared library and headers should be found, if not we have a problem
    if not cspice_header_include_dir:
        # raise an error
        raise RuntimeError('Could not locate a suitable header folder for cspice in setup.py for SpiceyPy')
    if not cspice_shared_library_dir:
        # raise an error 
        raise RuntimeError('Could not locate a suitable libcspice file in setup.py for SpiceyPy')
    # else we can proceed
    # set the expected lib names
    libraries = ["cspice" if is_unix else "libcspice"]
    library_dirs = [cspice_shared_library_dir, ]
    include_dirs = [
        numpy.get_include(),
        cspice_header_include_dir
    ]
    runtime_library_dirs = []
    extra_link_args =  []
    if is_linux:
        extra_link_args.append("-Wl,-rpath,$ORIGIN/../utils")
        runtime_library_dirs = ["$ORIGIN/../utils"]
    elif is_macos:
        extra_link_args.append("-Wl,-rpath,@loader_path/../utils")
        runtime_library_dirs = ["@loader_path/../utils"]
    if is_unix:
        extra_link_args.append('-lm')
    extra_compile_args = [

    ]
    ext_options = {
        "include_dirs": include_dirs,
        "libraries": libraries,
        "library_dirs": library_dirs,
        "language": "c",
        "define_macros": [],
        "extra_compile_args": extra_compile_args,
        "extra_link_args": extra_link_args,
        "runtime_library_dirs": runtime_library_dirs
    }
    cyice_ext = Extension(
        name="spiceypy.cyice.cyice",
        sources=[
            f"./src/spiceypy/cyice/cyice.pyx",
        ],
        **ext_options,
    )
    return cyice_ext


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
        self.run_command("build_ext")
        return super().run()


class BuildPyCommand(build_py):
    """Custom build command to ensure cspice is built and packaged"""

    def run(self):
        try_get_spice()
        self.run_command("build_ext")
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
    
    def run(self):
        try_get_spice()
        return super().run()

cmd_class = dict(
    install=InstallSpiceyPy,
    build_py=BuildPyCommand,
    bdist_wheel=SpiceyPyWheelBuild
)

ext_modules = [get_cyice_extension()]

if USE_CYTHON:
    cmd_class['build_ext'] = build_ext
    ext_modules = cythonize(ext_modules, annotate=True, nthreads=4)

setup(
    distclass=SpiceyPyBinaryDistribution,
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={
        "spiceypy": [
            "utils/*.so",
            "utils/*.dylib",
            "utils/*.dll",
            "utils/*.lib",
            "cyice/*.c",
            "cyice/*.so",
            "cyice/*.pyd",
            "cyice/*.pyx",
            "cyice/*.pxd",
        ],
        "*": ["get_spice.py"],
    },
    include_package_data=True,
    cmdclass=cmd_class,
    ext_modules=ext_modules,
)
