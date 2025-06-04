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

Sources for this file are mostly from DaRasch, spiceminer/getcspice.py,
with edits by me as needed for python2/3 compatibility
https://github.com/DaRasch/spiceminer/blob/master/getcspice.py

The MIT License (MIT)

Copyright (c) 2013 Philipp Rasch

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

The MIT License (MIT)

Copyright (c) 2017 ODC Space

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

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
import io
import platform
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import tempfile
import urllib
import urllib.request
import urllib.error
from zipfile import ZipFile

from typing import List

CSPICE_SRC_DIR = "CSPICE_SRC_DIR"
CSPICE_SHARED_LIB = "CSPICE_SHARED_LIB"
CSPICE_NO_PATCH = "CSPICE_NO_PATCH"
CSPICE_NO_TEMP = "CSPICE_NO_TEMP"
CSPICE_NO_BUILD = "CSPICE_NO_BUILD"

host_OS = platform.system()
host_arch = platform.machine()
# get the Conda environment prefix if present else get the python prefix
prefix = Path(os.environ.get("CONDA_PREFIX", sys.prefix))
# Check if platform is supported
os_supported = host_OS in ("Linux", "Darwin", "FreeBSD", "Windows")
# Get platform is Unix-like OS or not
is_unix = host_OS in ("Linux", "Darwin", "FreeBSD")
is_macos = host_OS == "Darwin"
# Get current working directory
root_dir = str(Path(os.path.realpath(__file__)).parent)
# Make the directory path for cspice
cspice_dir = os.environ.get(CSPICE_SRC_DIR, os.path.join(root_dir, "src", "cspice"))
# get the spiceypy utils folder
utils_dir = Path("./src/spiceypy/utils/").resolve()
# and make a global tmp cspice directory
tmp_cspice_root_dir = None
# macos builds can occur on x86 or arm64 machines.
# but we need to support cross compilation either way 
# so be a little pedantic here
requested_arch_x86 = os.environ.get("ARCHFLAGS", "").strip("'\"") == "-arch x86_64"
requested_arch_arm = os.environ.get("ARCHFLAGS", "").strip("'\"") == "-arch arm64"
# if both are false and on macos do something
if is_macos and (not requested_arch_arm and not requested_arch_x86):
    # default to building arm on macos
    requested_arch_arm = True
build_macos_x86 = is_macos and (('x86' in host_arch) or requested_arch_x86) and not requested_arch_arm
build_macos_arm = is_macos and ((host_arch == 'arm64') or requested_arch_arm) and not requested_arch_x86
# if host arch is x86 it will go to x86 build
# if however archflags was set explicitly to not be arm64 we need cross compile
# if we need to cross compile or compile for arm64
is_macos_arm = build_macos_arm 
# versions
spice_version = "N0067"
spice_num_v = "67"

if is_macos:
    print(f"On macOS {host_OS}, host arch {host_arch}")
    print(f"requested_arch_x86: {requested_arch_x86}")
    print(f"requested_arch_arm: {requested_arch_arm}")
    print(f"build_macox_x86: {build_macos_x86}")
    print(f"build_macos_arm: {build_macos_arm}")
    print(f"is_macos_arm: {is_macos_arm}")

# TODO de-duplicate from setup.py

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
    # try :
    #    1) the user provided path to the shared library, 
    #    2) the src dir for the project
    #    3) lib
    #    4) lib64
    lib_candidates: list[Path] = [
        Path(cspice_dir),
        utils_dir,
        prefix / "lib", 
        prefix / "lib64"
    ]
    _shared_lib_var = os.environ.get(CSPICE_SHARED_LIB)
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
    # locate the cspice header folder (should be prefix/include/cspice folder and look for SpiceUsr.h inside that)
    header_candidates: list[Path] = [
        Path(cspice_dir) / "include/",
        prefix / "include/cspice/"
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


class GetCSPICE(object):
    """
    Class that support the download from the NAIF FTP server of the required
    CSPICE package for the architecture used by the Python distribution that
    invokes this module. By default the CSPICE Toolkit version N0067 is
    downloaded and unpacked on the directory where this module is located.

    Arguments
    ---------
    :argument version: String indicating the required version of the CSPICE
                       Toolkit. By default it is 'N0067'.
    :type: str

    """

    # This class variable will be used to store the CSPICE package in memory.
    _local = None

    # Supported distributions
    _dists = {
        # system   arch        distribution name           extension
        # -------- ----------  -------------------------   ---------
        ("Darwin", "x86_64", "64bit"): ("MacIntel_OSX_AppleC_64bit", "tar.Z"),
        ("Darwin", "arm64", "64bit"): ("MacM1_OSX_clang_64bit", "tar.Z"),
        ("cygwin", "x86_64", "64bit"): ("PC_Cygwin_GCC_64bit", "tar.Z"),
        ("FreeBSD", "x86_64", "64bit"): ("PC_Linux_GCC_64bit", "tar.Z"),
        ("Linux", "x86_64", "64bit"): ("PC_Linux_GCC_64bit", "tar.Z"),
        ("Linux", "aarch64", "64bit"): ("PC_Linux_GCC_64bit", "tar.Z"),
        ("Windows", "x86_64", "64bit"): ("PC_Windows_VisualC_64bit", "zip"),
    }

    def __init__(self, version=spice_version, dst=None):
        """Init method that uses either the default N0067 toolkit version token
        or a user provided one.
        """
        try:
            # Get the remote file path for the Python architecture that
            # executes the script.
            distribution, self._ext = self._distribution_info()
        except KeyError:
            print("SpiceyPy currently does not support your system.")
        else:
            cspice = "cspice.{}".format(self._ext)
            self._rcspice = (
                "https://naif.jpl.nasa.gov/pub/naif/misc"
                "/toolkit_{0}/C/{1}/packages"
                "/{2}"
            ).format(version, distribution, cspice)

            # Setup the local directory (where the package will be downloaded)
            if dst is None:
                dst = os.path.realpath(os.path.dirname(__file__))
            self._root = dst

            # Download the file
            print("Downloading CSPICE for {0}...".format(distribution))
            attempts = 10  # Let's try a maximum of attempts for getting SPICE
            while attempts:
                attempts -= 1
                try:
                    self._download()
                except RuntimeError as error:
                    print(
                        "Download failed with URLError: {0}, trying again after "
                        "15 seconds!".format(error)
                    )
                    time.sleep(15)
                else:
                    # Unpack the file
                    print("Unpacking... (this may take some time!)")
                    self._unpack()
                    # We are done.  Let's return to the calling code.
                    break

    def _distribution_info(self):
        """Creates the distribution name and the expected extension for the
        CSPICE package and returns it.

        :return (distribution, extension) tuple where distribution is the best
                guess from the strings available within the platform_urls list
                of strings, and extension is either "zip" or "tar.Z" depending
                on whether we are dealing with a Windows platform or else.
        :rtype: tuple (str, str)

        :raises: KeyError if the (system, machine) tuple does not correspond
                 to any of the supported SpiceyPy environments.
        """

        print("Gathering information...")
        system = platform.system()
        processor = platform.processor()
        machine = platform.machine()

        # Cygwin system is CYGWIN-NT-xxx.
        system = "cygwin" if "CYGWIN" in system else system
        cpu_bits = "64bit" if sys.maxsize > 2 ** 32 else "32bit"

        if machine in ("x86", "x86_64", "AMD64", "i686"):
            machine = "x86_64"

        if is_macos_arm:
            machine = "arm64"

        print("SYSTEM:   ", system)
        print("PROCESSOR:", processor)
        print("MACHINE:  ", cpu_bits, machine)

        if machine in ("i386", "x86_32") or cpu_bits == "32bit":
            raise RuntimeError("32bit bit builds are not supported")

        return self._dists[(system, machine, cpu_bits)]

    def _download(self):
        """Support function that encapsulates the OpenSSL transfer of the CSPICE
        package to the self._local io.ByteIO stream.

        :raises RuntimeError if there has been any issue with the HTTPS
                             communication

        .. note::

           Handling of CSPICE downloads from HTTPS
           ---------------------------------------
           Some Python distributions may be linked to an old version of OpenSSL
           which will not let you connect to NAIF server due to recent SSL cert
           upgrades on the JPL servers.  Moreover, versions older than
           OpenSSL 1.0.1g are known to contain the 'the Heartbleed Bug'.
           Therefore this method provides two different implementations for the
           HTTPS GET call to the NAIF server to download the required CSPICE
           distribution package.

           * as of 3.0.1, we default back to use built in openssl, as we require python 3.6 or above *
        """
        try:
            # Send the request to get the CSPICE package (proxy auto detected).
            response = urllib.request.urlopen(self._rcspice, timeout=10)
        except urllib.error.URLError as err:
            raise RuntimeError(err.reason)

        # Convert the response to io.BytesIO and store it in local memory.
        self._local = io.BytesIO(response.read())

    def _unpack(self):
        """Unpacks the CSPICE package on the given root directory. Note that
        Package could either be the zipfile.ZipFile class for Windows platforms
        or tarfile.TarFile for other platforms.
        """
        if self._ext == "zip":
            with ZipFile(self._local, "r") as archive:
                archive.extractall(self._root)
        else:
            cmd = (
                f"gunzip | tar {'xfC -' if host_OS == 'FreeBSD' else 'xC'} {self._root}"
            )
            proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE)
            proc.stdin.write(self._local.read())
        self._local.close()


def copy_supplements() -> None:
    """
    Copy supplement files (patches, windows build files)
    to cspice directory
    """
    cwd = os.getcwd()
    patches = list(Path().cwd().glob("*.patch"))
    print("copy supplements to: ", cspice_dir, flush=True)
    for p in patches:
        shutil.copy(p, cspice_dir)
    if host_OS == "Windows":
        windows_files = [Path("./makeDynamicSpice.bat"), Path("./cspice.def")]
        cspice_src_dir = os.path.join(cspice_dir, "cspice", "src", "cspice")
        for w in windows_files:
            shutil.copy(w, cspice_src_dir)
    os.chdir(cwd)
    pass


def apply_patches() -> None:
    if int(spice_num_v) == 66:
        cwd = os.getcwd()
        os.chdir(cspice_dir)
        iswin = "-windows" if host_OS == "Windows" else ""
        patches = [
            f"0001-patch-for-n66-dskx02.c{iswin}.patch",
            f"0002-patch-for-n66-subpnt.c{iswin}.patch",
        ]
        if is_macos_arm:
            patches.append("0004_inquire_unistd.patch")
        for p in patches:
            try:
                print(f"Applying Patch {p}", flush=True)
                patch_cmd = subprocess.run(["git", "apply", "--reject", p], check=True)
            except subprocess.CalledProcessError as cpe:
                raise cpe
        os.chdir(cwd)
    pass


def prepare_cspice() -> None:
    """
    Prepare temporary cspice source directory,
    If not provided by the user, or if not readable, download a fresh copy
    :return: None
    """
    cwd = os.getcwd()
    global cspice_dir, tmp_cspice_root_dir
    tmp_cspice_root_dir = os.path.join(root_dir, "src")
    tmp_cspice_src_dir = os.path.join(tmp_cspice_root_dir, "cspice")
    if tmp_cspice_src_dir == cspice_dir and os.path.exists(cspice_dir):
        print(f"CSPICE src dir already in place {cspice_dir}, moving on")
    elif os.access(cspice_dir, os.R_OK):
        print(
            f"Found usable CSPICE src directory {cspice_dir} {tmp_cspice_src_dir}",
            flush=True,
        )
        # newer shutil.copytree has a flag for this that negates need for this
        shutil.copytree(
            cspice_dir + "/",
            tmp_cspice_src_dir,
            copy_function=shutil.copy,
        )
    else:
        print("Downloading CSPICE src from NAIF", flush=True)
        Path(tmp_cspice_src_dir).mkdir(exist_ok=True, parents=True)
        GetCSPICE(dst=tmp_cspice_root_dir)
    # okay cspice_dir need to be inside the root level cspice src dir
    cspice_dir = tmp_cspice_root_dir
    print("end of prep:", cspice_dir, flush=True)
    os.chdir(cwd)
    # okay now copy any and all files needed for building
    pass


def build_cspice() -> List[str]:
    """
    Builds cspice
    :return: absolute path to new compiled shared library
    """
    cwd = os.getcwd()
    global cspice_dir, host_OS
    if is_unix:
        libname = f"libcspice.so"
        target = ""
        if host_OS == "Darwin":
            target = "-target arm64-apple-macos11" if build_macos_arm else "-target x86_64-apple-macos10.9"
            extra_flags = f"-dynamiclib -install_name @rpath/{libname}"
        else:
            extra_flags = f"-shared -Wl,-soname,{libname}"
        destination = cspice_dir
        os.chdir(destination)
        print(f"Running CSPICE compilation in {destination}")
        cmds = [
            f"gcc {target} -Iinclude -c -fPIC -O2 -ansi ./cspice/src/cspice/*.c",
            f"gcc {target} {extra_flags} -fPIC -O2 -lm *.o -o {libname}",
            "rm ./*.o",
            "rm ./*.patch",
        ]
    elif host_OS == "Windows":
        destination = os.path.join(cspice_dir, "cspice", "src", "cspice")
        os.chdir(destination)
        cmds = ["makeDynamicSpice.bat"]
    else:
        os.chdir(cwd)
        raise NotImplementedError(f"non implemented host os for build {host_OS}")
    try:
        for cmd in cmds:
            _ = subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as cpe:
        os.chdir(cwd)
        pass
    # get the built shared library
    shared_lib_path = [
        str(p.absolute())
        for p in Path(destination).glob("*.*")
        if p.suffix in (".dll", ".dylib", ".so", ".lib")
    ]
    if len(shared_lib_path) < 1:
        os.chdir(cwd)
        raise RuntimeError(
            f'Could not find built shared library of SpiceyPy in {list(Path(destination).glob("*.*"))}'
        )
    print(shared_lib_path, flush=True)
    os.chdir(cwd)
    return shared_lib_path


def main(build: bool = True) -> None:
    """
    Main routine to build or not build cspice
    expected tmp src dir layout
    /tmpdir/ < top level temporary directory from TemporaryDirectory
           /cspice/ < directory containing contents of source code for cspice
                  /lib
                  /bin
                  /src/cspice/
                  ...
    to keep track of the scenarios:
    1. User has no cspice locally and need to build and compile
    2. User has prebuilt wheel and doesn't need cspice source (not true for cython, source is always needed)
    3. User has local src copy and doesn't need to compile (likely cython only)

    :param build: if true build the shared library, if false just download the source code
    :return: None
    """
    # first look for existing shared library and src headers
    # attempt to find the headers folder
    cspice_header_include_dir = get_cspice_headers_include_dir()
    # now attempt to locate the shared library folder
    cspice_shared_library_dir = get_cspice_lib_dir()
    # now actually check if both are true
    if cspice_header_include_dir and cspice_shared_library_dir:
        print(
            "Done! shared library and headers for cspice are found. Done!",
            flush=True,
        )
        return
    else:
        print(
            f"Could not locate cspice headers and or shared library from apriori locations: Shared: {cspice_shared_library_dir} Headers: {cspice_shared_library_dir}"
        )
    build = os.environ.get(CSPICE_NO_BUILD) is None  # if false (var is set) don't build
    cwd = os.getcwd()
    # set final destination for cspice dynamic library
    destination_dir = os.path.join(root_dir, "src", "spiceypy", "utils")
    destination = os.path.join(
        destination_dir,
        "libcspice.so" if is_unix else "libcspice.dll",
    )
    # check if the shared library already exists, if it does we are done
    if Path(destination).is_file() and build:
        print(
            "Done! shared library for cspice already exists in destination. Done!",
            flush=True,
        )
        return
    # next see if cspice shared library is provided
    shared_library_path = os.environ.get(CSPICE_SHARED_LIB)
    print(f"Did user provide shared library path?: {shared_library_path}")
    if shared_library_path is not None and build:
        print(f"User has provided a shared library...", flush=True)
        # todo: what if we can't read the file? we need to jump to building it... doubtful this happens
        pass  # now we don't need to do that much
    else:
        # okay, now we either are given a src dir, have already downloaded it, or don't have it
        print("Preparing cspice", flush=True)
        prepare_cspice()
        # add the patches
        print("Copying supplements", flush=True)
        copy_supplements()
        # okay now that we have the source in a writeable directory we can apply patches
        if CSPICE_NO_PATCH not in os.environ:
            print("Apply patches", flush=True)
            apply_patches()
        # now build, but not if you have the shared library path around
        if build and shared_library_path is None:
            print("Building cspice", flush=True)
            shared_library_path = build_cspice()
    # okay at this point we have to either have built cspice or have had a shared library provided, but I may not have built cspice
    # so copy the shared library path, but if I didn't build I had to have had it provided, if not provided we just build (or not) without moving
    if shared_library_path is not None or build:
        if isinstance(shared_library_path, str):
            shared_library_path = [shared_library_path]
            print(f"Had to update SLP to a list: {shared_library_path}")
        # first make the directory for the destination if it doesn't exist
        Path(destination).parent.mkdir(parents=True, exist_ok=True)
        for slp in shared_library_path:
            slp = slp.replace(".dylib", ".so")
            destination = Path(destination_dir) / Path(slp).name
            print(f"Copying: {slp} to {destination}", flush=True)
            # okay now move shared library to dst dir
            shutil.copy(slp, destination_dir)
            # cleanup slp
            os.remove(slp)
            # cleanup tmp dir, windows seems to fail with this:
            #    PermissionError: [WinError 32] The process cannot access the file because it is being used by another process
            # if tmp_cspice_root_dir is not None:
            #     if os.path.exists(tmp_cspice_root_dir) and os.path.isdir(tmp_cspice_root_dir):
            #         shutil.rmtree(tmp_cspice_root_dir)
    # and now we are done!
    os.chdir(cwd)
    print("Done!")


if __name__ == "__main__":
    main()
