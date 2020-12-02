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
import shutil
import subprocess
import sys
import time
import urllib
import urllib.request
import urllib.error
from zipfile import ZipFile

CSPICE_SRC_DIR = "CSPICE_SRC_DIR"
CSPICE_SHARED_LIB = "CSPICE_SHARED_LIB"

host_OS = platform.system()
# Check if platform is supported
os_supported = host_OS in ("Linux", "Darwin", "FreeBSD", "Windows")
# Get platform is Unix-like OS or not
is_unix = host_OS in ("Linux", "Darwin", "FreeBSD")
# Get current working directory
root_dir = os.path.dirname(os.path.realpath(__file__))
# Make the directory path for cspice
cspice_dir = os.environ.get(CSPICE_SRC_DIR, os.path.join(root_dir, "cspice"))
# Make the directory path for cspice/lib
lib_dir = os.path.join(cspice_dir, "lib")


class GetCSPICE(object):
    """
    Class that support the download from the NAIF FTP server of the required
    CSPICE package for the architecture used by the Python distribution that
    invokes this module.  By default the CSPICE Toolkit version N0066 is
    downloaded and unpacked on the directory where this module is located.

    Arguments
    ---------
    :argument version: String indicating the required version of the CSPICE
                       Toolkit. By default it is 'N0066'.
    :type: str

    """

    # This class variable will be used to store the CSPICE package in memory.
    _local = None

    # Supported distributions
    _dists = {
        # system   arch        distribution name           extension
        # -------- ----------  -------------------------   ---------
        ("Darwin", "32bit"): ("MacIntel_OSX_AppleC_32bit", "tar.Z"),
        ("Darwin", "64bit"): ("MacIntel_OSX_AppleC_64bit", "tar.Z"),
        ("cygwin", "32bit"): ("PC_Cygwin_GCC_32bit", "tar.Z"),
        ("cygwin", "64bit"): ("PC_Cygwin_GCC_64bit", "tar.Z"),
        ("FreeBSD", "32bit"): ("PC_Linux_GCC_32bit", "tar.Z"),
        ("FreeBSD", "64bit"): ("PC_Linux_GCC_64bit", "tar.Z"),
        ("Linux", "32bit"): ("PC_Linux_GCC_32bit", "tar.Z"),
        ("Linux", "64bit"): ("PC_Linux_GCC_64bit", "tar.Z"),
        ("Windows", "32bit"): ("PC_Windows_VisualC_32bit", "zip"),
        ("Windows", "64bit"): ("PC_Windows_VisualC_64bit", "zip"),
    }

    def __init__(self, version="N0066"):
        """Init method that uses either the default N0066 toolkit version token
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
            self._root = os.path.realpath(os.path.dirname(__file__))

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

        # Cygwin system is CYGWIN-NT-xxx.
        system = "cygwin" if "CYGWIN" in system else system

        processor = platform.processor()
        machine = "64bit" if sys.maxsize > 2 ** 32 else "32bit"

        print("SYSTEM:   ", system)
        print("PROCESSOR:", processor)
        print("MACHINE:  ", machine)

        return self._dists[(system, machine)]

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
            cmd = "gunzip | tar xC " + self._root
            proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE)
            proc.stdin.write(self._local.read())
        self._local.close()


class InstallCSpice(object):
    @staticmethod
    def get_cspice():
        if InstallCSpice.check_for_spice():
            print("Host OS: {0}".format(host_OS))
            if os_supported:
                InstallCSpice.unified_method()
            else:
                sys.exit("Unsupported OS: {0}".format(host_OS))

    @staticmethod
    def check_for_spice():
        print("Checking the path", cspice_dir)
        if os.path.exists(cspice_dir):
            print(f"Found CSPICE source at {cspice_dir}")
            return True
        elif os.environ.get(CSPICE_SHARED_LIB) is not None:
            print(f"User has provided a shared library...")
            return True
        elif os.environ.get(CSPICE_SRC_DIR) is not None:
            message = f"Unable to find user provided CSPICE_SRC_DIR at {cspice_dir}"
            sys.exit(message)
        else:
            message = "Unable to find CSPICE at {0}. Attempting to Download CSPICE For you:".format(
                cspice_dir
            )
            print(message)
            # Download cspice using getspice.py
            GetCSPICE(version="N0066")
        if not os.path.exists(cspice_dir):
            message = "Unable to find CSPICE at {0}. Exiting".format(cspice_dir)
            sys.exit(message)
        return True

    @staticmethod
    def unpack_cspice():
        if is_unix:
            cspice_lib = os.path.join(
                lib_dir, ("cspice.lib" if host_OS == "Windows" else "cspice.a")
            )
            csupport_lib = os.path.join(
                lib_dir, ("csupport.lib" if host_OS == "Windows" else "csupport.a")
            )

            if os.path.exists(cspice_lib) and os.path.exists(csupport_lib):
                cwd = os.getcwd()
                try:
                    os.chdir(lib_dir)
                    if host_OS == "Windows":
                        raise BaseException(
                            "Windows is not supported in this build method"
                        )
                    elif is_unix:
                        for lib in ["ar -x cspice.a", "ar -x csupport.a"]:
                            unpack_lib_process = subprocess.Popen(lib, shell=True)
                            process_status = os.waitpid(unpack_lib_process.pid, 0)[1]
                            if process_status != 0:
                                raise BaseException("{0}".format(process_status))
                    else:
                        raise BaseException("Unsupported OS: {0}".format(host_OS))
                except BaseException as error:
                    status = error.args
                    sys.exit(
                        "Error: cspice object file extraction failed with exit status: {0}".format(
                            status
                        )
                    )
                finally:
                    os.chdir(cwd)
            else:
                error_message = (
                    "Error, cannot find CSPICE "
                    "static libraries at {0}".format(lib_dir)
                )
                sys.exit(error_message)

    @staticmethod
    def build_library():
        # Get the current working directory
        cwd = os.getcwd()
        if is_unix:
            try:
                os.chdir(lib_dir)
                # find a way to make this work via Extension and setuptools, not using popen.
                build_lib = subprocess.Popen(
                    "gcc -shared -fPIC -lm *.o -o spice.so", shell=True
                )
                status = os.waitpid(build_lib.pid, 0)[1]
                if status != 0:
                    raise BaseException("{0}".format(status))
                success = os.path.exists(os.path.join(os.getcwd(), "spice.so"))
                if not success:
                    raise BaseException("Did not find spice.so, build went badly.")
            except BaseException as errorInst:
                status = errorInst.args
                sys.exit(
                    "Error: compilation of shared spice.so build exit status: {0}".format(
                        status
                    )
                )

        elif host_OS == "Windows":
            try:
                destination = os.path.join(cspice_dir, "src", "cspice")
                def_file = os.path.join(root_dir, "cspice.def")
                make_bat = os.path.join(root_dir, "makeDynamicSpice.bat")
                shutil.copy(def_file, destination)
                shutil.copy(make_bat, destination)
                # run the script
                os.chdir(destination)
                windows_build = subprocess.Popen("makeDynamicSpice.bat", shell=True)
                status = windows_build.wait()
                if status != 0:
                    raise BaseException("{0}".format(status))
            except BaseException as error:
                sys.exit("Build failed with: {0}".format(error.args))
        # Change back to the stored 'current working directory
        os.chdir(cwd)

    @staticmethod
    def move_to_root_directory(shared_lib_path=None):
        sharedlib = "spice.so" if is_unix else "cspice.dll"
        destination = os.path.join(root_dir, "spiceypy", "utils", sharedlib)
        if os.path.isfile(destination):
            print("Shared Library is already present in destination folder")
            return  # break out of function
        if shared_lib_path:
            # we have the path to the shared library, just move it
            print(
                "Attempting to move: {0}   to: {1}".format(shared_lib_path, destination)
            )
            try:
                shutil.copyfile(shared_lib_path, destination)
            except BaseException as e:
                sys.exit(
                    "{0} file not found, what happend?: {1}".format(shared_lib_path, e)
                )
        else:
            if is_unix:
                shared_lib_path = os.path.join(cspice_dir, "lib", sharedlib)
            else:
                shared_lib_path = os.path.join(cspice_dir, "src", "cspice", sharedlib)
            # finally call this function with the new path
            InstallCSpice.move_to_root_directory(shared_lib_path=shared_lib_path)

    @staticmethod
    def cleanup():
        # Remove CSPICE folder
        try:
            shutil.rmtree(os.path.join(os.getcwd(), "cspice"))
        except OSError as e:
            print("Error Cleaning up cspice folder")
            raise e

    @staticmethod
    def unified_method():
        shared_lib_name = "spice.so" if is_unix else "cspice.dll"
        cspice_shared_lib = os.environ.get(
            CSPICE_SHARED_LIB
        )  # will be none if not defined
        if cspice_shared_lib:
            # user has provideded a shared library to be used
            print(f"User defined CSPICE shared library defined at: {cspice_shared_lib}")
            if not os.path.exists(cspice_shared_lib):
                raise RuntimeError(
                    f"Error: could not find CSPICE shared library user defined at: {cspice_shared_lib}"
                )
            else:
                print(f"Found user provided shared library, not building")
        elif os.path.exists(os.path.join(cspice_dir, "lib", shared_lib_name)):
            print(f"Found pre-made {shared_lib_name}, not building")
        elif os.path.exists(
            os.path.join(root_dir, "spiceypy", "utils", shared_lib_name)
        ):
            print(f"Found pre-made {shared_lib_name} in spiceypy, not building")
        else:
            # we did not find a user provided shared library
            if is_unix:
                InstallCSpice.unpack_cspice()
            # Build the DLL
            if not cspice_shared_lib:
                InstallCSpice.build_library()
        # Move to correct location (root of the distribution), always run
        InstallCSpice.move_to_root_directory(shared_lib_path=cspice_shared_lib)


if __name__ == "__main__":
    InstallCSpice.get_cspice()
