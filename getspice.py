#!/usr/bin/env python3
__author__ = 'AndrewAnnex'

# Sources: mostly from DaRasch, spiceminer/getcspice.py,
# with edits as needed for python2/3 compatibility
# https://github.com/DaRasch/spiceminer/blob/master/getcspice.py
import os
import sys
import platform
from six.moves import urllib
import io
import zipfile
import subprocess


def getSpice():

    def give_points(dct, info):
        for key in dct:
            if info in key:
                dct[key] += 1

    def get_winner(dct):
        candidates = list(dct.keys())
        values = list(dct.values())
        winner = candidates[0]
        winner_value = 0
        for cand, value in zip(candidates, values):
            if value > winner_value:
                winner_value = value
                winner = cand
        return winner

    root_url = 'http://naif.jpl.nasa.gov/pub/naif/toolkit/C/'
    platform_urls = [
        'MacIntel_OSX_AppleC_32bit/',
        'MacIntel_OSX_AppleC_64bit/',
        'MacPPC_OSX_AppleC_32bit/',
        'PC_Cygwin_GCC_32bit/',
        'PC_Linux_GCC_32bit/',
        'PC_Linux_GCC_64bit/',
        'PC_Windows_VisualC_32bit/',
        'PC_Windows_VisualC_64bit/']
    ### DETERMINE BEST DOWNLOAD OPTION ###
    print('Gathering information...')
    points = {url: 0 for url in platform_urls}

    system = platform.system()
    if system == 'Darwin':
        system = 'Mac'
    print('SYSTEM:   ', system)
    give_points(points, system)

    processor = platform.processor()
    print('PROCESSOR:', processor)

    machine = '64bit' if sys.maxsize > 2 ** 32 else '32bit'
    print('MACHINE:  ', machine)
    give_points(points, machine)

    result = get_winner(points) + 'packages/cspice.tar.Z'

    if "Windows" in result:
        result = result.replace('.tar.Z', '.zip')

    print('Best option:', result.split('/')[0])
    print('URL: ', root_url + result)

    ### DOWNLOAD AND UNPACK BEST PACKAGE ###
    root_dir = os.path.realpath(os.path.dirname(__file__))

    print('\nDownloading...')
    download = urllib.request.urlopen(root_url + result)

    print('Unpacking... (this may take some time!)')
    if result.endswith('zip'):
        filelike = io.BytesIO(download.read())
        with zipfile.ZipFile(filelike, 'r') as archive:
            archive.extractall(root_dir)
        filelike.close()
    else:
        cmd = 'gunzip | tar xC ' + root_dir
        proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE)
        proc.stdin.write(download.read())
    download.close()
    print('CSPICE download and extraction complete...')


if __name__ == '__main__':
    # Call getSpice
    getSpice()