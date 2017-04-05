#!/usr/bin/env python3

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
"""

import os
import sys
import platform

import time

import six.moves.urllib as urllib
import io
import zipfile
import subprocess

__author__ = 'AndrewAnnex'

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

    root_url = 'https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_N0065/C/'
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

    attemptSpiceDownloadXTimes(10, root_url, result, root_dir)


def downloadSpice(urlpath):
    return urllib.request.urlopen(urlpath, timeout=10)


def attemptSpiceDownloadXTimes(x, root_url, result, root_dir):
    attempts = 0
    while attempts < x:
        try:
            print("Attempting to download spice...")
            download = downloadSpice(root_url + result)
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
            break
        except urllib.error.URLError:
            print("Download failed with URLError, trying again after 15 seconds!")
        except urllib.error.HTTPError as h:
            print("Some http error: ", h, ", trying again after 15 seconds!")
        attempts += 1
        time.sleep(15)


if __name__ == '__main__':
    # Call getSpice
    getSpice()
