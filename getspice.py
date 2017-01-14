#!/usr/bin/env python3


# Sources: mostly from DaRasch, spiceminer/getcspice.py,
# with edits as needed for python2/3 compatibility
# https://github.com/DaRasch/spiceminer/blob/master/getcspice.py
import os
import sys
import platform

import time

import requests
import io
import zipfile
import subprocess
import random

import ssl
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.util.ssl_ import create_urllib3_context


class TLSv1_2HttpAdapter(HTTPAdapter):
    """"
    Transport adapter" that allows us to use TLSv1.2.
    adopted from https://github.com/kennethreitz/requests/issues/3774
    """
    CIPHERS = (
        'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:'
        'DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES:!aNULL:'
        '!eNULL:!MD5'
    )
    def init_poolmanager(self, connections, maxsize, block=False, *args, **kwargs):
        context = create_urllib3_context(ciphers=TLSv1_2HttpAdapter.CIPHERS)
        kwargs['ssl_context'] = context
        self.poolmanager = PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_version=ssl.PROTOCOL_TLSv1_2, *args, **kwargs)

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
    session = requests.Session()
    session.mount(urlpath, TLSv1_2HttpAdapter())
    return requests.get(urlpath, timeout=30)


def attemptSpiceDownloadXTimes(x, root_url, result, root_dir):
    attempts = 0
    while attempts < x:
        try:
            print("Attempting to download spice...")
            download = downloadSpice(root_url + result)
            if download.status_code == requests.codes.ok:
                print('Unpacking... (this may take some time!)')
                if result.endswith('zip'):
                    filelike = io.BytesIO(download.content)
                    with zipfile.ZipFile(filelike, 'r') as archive:
                        archive.extractall(root_dir)
                    filelike.close()
                else:
                    cmd = 'gunzip | tar xC ' + root_dir
                    proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE)
                    proc.stdin.write(download.content)
                download.close()
                break
            else:
                print("Download failed somehow {}, trying again after 15 seconds!".format(str(download)))
                attempts += 1
                time.sleep(15 + random.random())
        except requests.RequestException as r:
            print("Got the following error: {}, trying again after 15 seconds!".format(r))
            attempts += 1
            time.sleep(15 + random.random())


if __name__ == '__main__':
    # Call getSpice
    getSpice()
