#!/usr/bin/env python3
__author__ = 'Apollo117'

# Sources: mostly from DaRasch, spiceminer/getcspice.py, with edits as needed for python3
# https://github.com/DaRasch/spiceminer/blob/master/getcspice.py
import os
import sys
import platform

#Python 2 and 3 compatibility
try:
    # Python 3 urllib
    from urllib.request import urlopen
except ImportError:
    # Fallback for python2
    from urllib2 import urlopen
import io
import zipfile
import subprocess


def getSpice():
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

    def give_points(dct, info):
        for key in dct:
            if info in key:
                dct[key] += 1

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

    result = get_winner(points) + 'packages/cspice.tar.Z'
    print('Best option:', result.split('/')[0])

    ### DOWNLOAD AND UNPACK BEST PACKAGE ###
    root_dir = os.path.realpath(os.path.dirname(__file__))
    archive_path = os.path.join(root_dir, result.split('/')[1])

    print('\nDownloading...')
    download = urlopen(root_url + result)

    print('Unpacking... (this may take some time!)')
    if result[:-3] == 'zip':
        filelike = io.StringIO(download.read())
        with zipfile.ZipFile(filelike, 'r') as archive:
            archive.extractall(root_dir)
        filelike.close()
    else:
        cmd = 'gunzip | tar xC ' + root_dir
        proc = subprocess.Popen(cmd, shell = True, stdin = subprocess.PIPE)
        proc.stdin.write(download.read())
    download.close()

    print('CSPICE download and extraction complete...')


if __name__ == '__main__':
    # Call getSpice
    getSpice()