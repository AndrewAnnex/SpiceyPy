#!/usr/bin/env python3
__author__ = 'AndrewAnnex'

import os
import sys
import platform
from six.moves import urllib
import io
import zipfile
import subprocess


def getSpice():
    """
        Downloads CSPICE
        # Sources: mostly from DaRasch, spiceminer/getcspice.py,
        # with edits as needed for python2/3 compatibility
        # https://github.com/DaRasch/spiceminer/blob/master/getcspice.py
    """
    root_url = 'http://naif.jpl.nasa.gov/pub/naif/toolkit/C/'

    platform_map = {'Windows': {'32bit': 'PC_Windows_VisualC_32bit/',
                                '64bit': 'PC_Windows_VisualC_64bit/'},
                    'Linux':   {'32bit': 'PC_Linux_GCC_32bit/',
                                '64bit': 'PC_Linux_GCC_64bit/'},
                    'Darwin':  {'32bit': 'MacIntel_OSX_AppleC_32bit/',
                                '64bit': 'MacIntel_OSX_AppleC_64bit/'}}

    system = platform.system()

    if system in platform_map.keys():
        # OK we are on a supported platform
        available_archs = platform_map.get(system)
        architecture = '64bit' if sys.maxsize > 2 ** 32 else '32bit'
        selected_package = available_archs.get(architecture)
        url = root_url + selected_package + "packages/cspice.tar.Z"
        if system is 'Windows':
            url = url.replace('.tar.Z', '.zip')
        print("Downloading: {}".format(url))

        # DOWNLOAD AND UNPACK BEST PACKAGE
        root_dir = os.path.realpath(os.path.dirname(__file__))
        download = urllib.request.urlopen(url)

        print('Unpacking... (this may take some time!)')

        if url.endswith('zip'):
            filelike = io.BytesIO(download.read())
            with zipfile.ZipFile(filelike, 'r') as archive:
                archive.extractall(root_dir)
            filelike.close()
        else:
            # .Z archieves throw python gzip/tar modules for a loop :(
            cmd = 'gunzip | tar xC ' + root_dir
            proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE)
            proc.stdin.write(download.read())
        download.close()
        print('CSPICE download and extraction complete...')


if __name__ == '__main__':
    # Call getSpice
    getSpice()
