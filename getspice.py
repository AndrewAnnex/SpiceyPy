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
import subprocess
import ssl
import sys
import time
from zipfile import ZipFile

import six.moves.urllib as urllib


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
        ('Darwin', '32bit'): ('MacIntel_OSX_AppleC_32bit', 'tar.Z'),
        ('Darwin', '64bit'): ('MacIntel_OSX_AppleC_64bit', 'tar.Z'),
        ('cygwin', '32bit'): ('PC_Cygwin_GCC_32bit', 'tar.Z'),
        ('cygwin', '64bit'): ('PC_Cygwin_GCC_64bit', 'tar.Z'),
        ('FreeBSD', '32bit'): ('PC_Linux_GCC_32bit', 'tar.Z'),
        ('FreeBSD', '64bit'): ('PC_Linux_GCC_64bit', 'tar.Z'),
        ('Linux', '32bit'): ('PC_Linux_GCC_32bit', 'tar.Z'),
        ('Linux', '64bit'): ('PC_Linux_GCC_64bit', 'tar.Z'),
        ('Windows', '32bit'): ('PC_Windows_VisualC_32bit', 'zip'),
        ('Windows', '64bit'): ('PC_Windows_VisualC_64bit', 'zip')}

    def __init__(self, version='N0066'):
        """Init method that uses either the default N0066 toolkit version token
        or a user provided one.
        """
        try:
            # Get the remote file path for the Python architecture that
            # executes the script.
            distribution, self._ext = self._distribution_info()
        except KeyError:
            print('SpiceyPy currently does not support your system.')
        else:
            cspice = 'cspice.{}'.format(self._ext)
            self._rcspice = ('https://naif.jpl.nasa.gov/pub/naif/misc'
                             '/toolkit_{0}/C/{1}/packages'
                             '/{2}').format(version, distribution, cspice)

            # Setup the local directory (where the package will be downloaded)
            self._root = os.path.realpath(os.path.dirname(__file__))

            # Download the file
            print('Downloading CSPICE for {0}...'.format(distribution))
            attempts = 10   # Let's try a maximum of attempts for getting SPICE
            while attempts:
                attempts -= 1
                try:
                    self._download()
                except RuntimeError as error:
                    print("Download failed with URLError: {0}, trying again after "
                          "15 seconds!".format(error))
                    time.sleep(15)
                else:
                    # Unpack the file
                    print('Unpacking... (this may take some time!)')
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

        print('Gathering information...')
        system = platform.system()

        # Cygwin system is CYGWIN-NT-xxx.
        system = 'cygwin' if 'CYGWIN' in system else system

        processor = platform.processor()
        machine = '64bit' if sys.maxsize > 2 ** 32 else '32bit'

        print('SYSTEM:   ', system)
        print('PROCESSOR:', processor)
        print('MACHINE:  ', machine)

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
        """
        # Use urllib3 (based on PyOpenSSL).
        if ssl.OPENSSL_VERSION < 'OpenSSL 1.0.1g':
            # Force urllib3 to use pyOpenSSL
            import urllib3.contrib.pyopenssl
            urllib3.contrib.pyopenssl.inject_into_urllib3()

            import certifi
            import urllib3

            try:
                # Create a PoolManager
                https = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                                            ca_certs=certifi.where())
                # Send the request to get the CSPICE package.
                response = https.request('GET', self._rcspice,
                                         timeout=urllib3.Timeout(10))
            except urllib3.exceptions.HTTPError as err:
                raise RuntimeError(err.message)

            # Convert the response to io.BytesIO and store it in local memory.
            self._local = io.BytesIO(response.data)

        # Use the standard urllib (using system OpenSSL).
        else:
            try:
                # Send the request to get the CSPICE package.
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
        if self._ext == 'zip':
            with ZipFile(self._local, 'r') as archive:
                archive.extractall(self._root)
        else:
            cmd = 'gunzip | tar xC ' + self._root
            proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE)
            proc.stdin.write(self._local.read())
        self._local.close()
