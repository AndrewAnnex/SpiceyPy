"""
The MIT License (MIT)

Copyright (c) [2015-2018] [Andrew Annex]

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
"""

import os
import time
import six.moves.urllib as urllib
from six import print_ as six_print


cwd = os.path.realpath(os.path.dirname(__file__))

def getKernelNameFromURL(url):
    return url.split('/')[-1]

def getPathFromUrl(url):
    return os.path.join(cwd, getKernelNameFromURL(url))

def cleanupFile(path):
    if os.path.exists(path):
        os.remove(path)

class CassiniKernels(object):
    cassPck_url     = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/master/cpck05Mar2004.tpc"
    satSpk_url      = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/master/130220AP_SE_13043_13073.bsp"
    cassTourSpk_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/master/130212AP_SK_13043_13058.bsp"
    cassFk_url      = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/master/cas_v40.tf"
    cassCk_url      = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/master/13056_13057ra.bc"
    cassSclk_url    = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/master/cas00167.tsc"
    cassIk_url      = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/master/cas_iss_v10.ti"
    cassPck         = getPathFromUrl(cassPck_url)
    satSpk          = getPathFromUrl(satSpk_url)
    cassTourSpk     = getPathFromUrl(cassTourSpk_url)
    cassFk          = getPathFromUrl(cassFk_url)
    cassCk          = getPathFromUrl(cassCk_url)
    cassSclk        = getPathFromUrl(cassSclk_url)
    cassIk          = getPathFromUrl(cassIk_url)

def cleanup_Cassini_Kernels():
    cleanupFile(CassiniKernels.cassPck)
    cleanupFile(CassiniKernels.satSpk)
    cleanupFile(CassiniKernels.cassTourSpk)
    cleanupFile(CassiniKernels.cassFk)
    cleanupFile(CassiniKernels.cassCk)
    cleanupFile(CassiniKernels.cassSclk)
    cleanupFile(CassiniKernels.cassIk)


class ExtraKernels(object):
    voyagerSclk_url     = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/master/vg200022.tsc"
    earthTopoTf_url     = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/master/earth_topo_050714.tf"
    earthStnSpk_url     = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/master/earthstns_itrf93_050714.bsp"
    earthHighPerPck_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/master/earth_031228_231229_predict.bpc"
    phobosDsk_url       = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/master/phobos_lores.bds"
    marsSpk_url         = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/master/mar022-1.bsp"
    voyagerSclk         = getPathFromUrl(voyagerSclk_url)
    earthTopoTf         = getPathFromUrl(earthTopoTf_url)
    earthStnSpk         = getPathFromUrl(earthStnSpk_url)
    earthHighPerPck     = getPathFromUrl(earthHighPerPck_url)
    phobosDsk           = getPathFromUrl(phobosDsk_url)
    marsSpk             = getPathFromUrl(marsSpk_url)

def cleanup_Extra_Kernels():
    cleanupFile(ExtraKernels.voyagerSclk)
    cleanupFile(ExtraKernels.earthTopoTf)
    cleanupFile(ExtraKernels.earthStnSpk)
    cleanupFile(ExtraKernels.earthHighPerPck)
    cleanupFile(ExtraKernels.phobosDsk)
    cleanupFile(ExtraKernels.marsSpk)


class CoreKernels(object):
    import sys
    # note this gets updated
    currentLSK = 'naif0012.tls'
    #
    pck_url    = 'https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/master/pck00010.tpc'
    spk_url    = 'https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/master/de405s_{}endian.bsp'.format(sys.byteorder)
    gm_pck_url = 'https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/master/gm_de431.tpc'
    lsk_url    = 'https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/master/{}'.format(currentLSK)
    pck        = getPathFromUrl(pck_url)
    spk        = getPathFromUrl(spk_url)
    gm_pck     = getPathFromUrl(gm_pck_url)
    lsk        = getPathFromUrl(lsk_url)
    standardKernelList = [pck, spk, gm_pck, lsk]
    testMetaKernel     = os.path.join(cwd, "exampleKernels.txt")

def cleanup_Core_Kernels():
    cleanupFile(CoreKernels.pck)
    cleanupFile(CoreKernels.spk)
    cleanupFile(CoreKernels.gm_pck)
    cleanupFile(CoreKernels.lsk)

def getKernel(url):
    kernelName = getKernelNameFromURL(url)
    kernelFile = os.path.join(cwd, kernelName)
    # does not download if files are present, which allows us to potentially cache kernels
    if not os.path.isfile(kernelFile):
        attemptDownload(url, kernelName, kernelFile, 5)


def attemptDownload(url, kernelName, targetFileName, num_attempts):
    current_attempt = 0
    while current_attempt < num_attempts:
        try:
            six_print("Attempting to Download kernel: {}".format(kernelName), flush=True)
            current_kernel = urllib.request.urlopen(url, timeout=10)
            with open(targetFileName, "wb") as kernel:
                kernel.write(current_kernel.read())
            six_print("Downloaded kernel: {}".format(kernelName), flush=True)
            break
        # N.B. .HTTPError inherits from .URLError, so [except:....HTTPError]
        #      must be listed before [except:....URLError], otherwise the
        #      .HTTPError exception cannot be caught
        except urllib.error.HTTPError as h:
            print("Some http error when downloading kernel {}, error: ".format(kernelName), h, ", trying again after a bit.")
        except urllib.error.URLError:
            six_print("Download of kernel: {} failed with URLError, trying again after a bit.".format(kernelName), flush=True)
        current_attempt += 1
        six_print("\t Attempting to Download kernel again...", flush=True)
        time.sleep(2 + current_attempt)
    if current_attempt >= num_attempts:
        raise BaseException("Error Downloading kernel: {}, check if kernel exists at url: {}".format(kernelName, url))


def getStandardKernels():
    six_print("\tChecking for kernels...\n", flush=True)
    getKernel(CoreKernels.pck_url)
    getKernel(CoreKernels.spk_url)
    getKernel(CoreKernels.gm_pck_url)
    getKernel(CoreKernels.lsk_url)


def getExtraTestKernels():
    # these are test kernels not included in the standard meta kernel
    getKernel(ExtraKernels.voyagerSclk_url)
    getKernel(ExtraKernels.earthTopoTf_url)
    getKernel(ExtraKernels.earthStnSpk_url)
    getKernel(ExtraKernels.earthHighPerPck_url)
    getKernel(ExtraKernels.phobosDsk_url)
    getKernel(ExtraKernels.marsSpk_url)


def getCassiniTestKernels():
    getKernel(CassiniKernels.cassPck_url)
    getKernel(CassiniKernels.satSpk_url)
    getKernel(CassiniKernels.cassTourSpk_url)
    getKernel(CassiniKernels.cassFk_url)
    getKernel(CassiniKernels.cassCk_url)
    getKernel(CassiniKernels.cassSclk_url)
    getKernel(CassiniKernels.cassIk_url)


def writeTestMetaKernel():
    # Update the paths!
    with open(os.path.join(cwd, "exampleKernels.txt"), 'w') as kernelFile:
        kernelFile.write('\\begindata\n')
        kernelFile.write('KERNELS_TO_LOAD = (\n')
        for kernel in CoreKernels.standardKernelList:
            kernelFile.write('\'{0}\'\n'.format(os.path.join(cwd, kernel)))
        kernelFile.write(')\n')
        kernelFile.write('\\begintext')
    six_print('\nDone writing test meta kernel.', flush=True)


def downloadKernels():
    getStandardKernels()     # Download the kernels listed in kernelList and kernelURLlist
    getCassiniTestKernels()  # Download Cassini kernels
    getExtraTestKernels()    # Download any extra test kernels we need
    writeTestMetaKernel()    # Create the meta kernel file for tests

