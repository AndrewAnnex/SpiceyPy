"""
The MIT License (MIT)

Copyright (c) [2015-2020] [Andrew Annex]

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
import platform
import tempfile
import urllib
import urllib.error
import urllib.request
import sys

cwd = "/tmp" if platform.system() == "Darwin" else tempfile.gettempdir()


def get_kernel_name_from_url(url):
    return url.split("/")[-1]


def get_path_from_url(url):
    return os.path.join(cwd, get_kernel_name_from_url(url))


def cleanup_file(path):
    if os.path.exists(path):
        os.remove(path)


class CassiniKernels(object):
    cassPck_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/main/cpck05Mar2004.tpc"
    satSpk_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/main/130220AP_SE_13043_13073.bsp"
    cassTourSpk_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/main/130212AP_SK_13043_13058.bsp"
    cassFk_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/main/cas_v40.tf"
    cassCk_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/main/13056_13057ra.bc"
    cassSclk_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/main/cas00167.tsc"
    cassIk_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/main/cas_iss_v10.ti"
    cassPck = get_path_from_url(cassPck_url)
    satSpk = get_path_from_url(satSpk_url)
    cassTourSpk = get_path_from_url(cassTourSpk_url)
    cassFk = get_path_from_url(cassFk_url)
    cassCk = get_path_from_url(cassCk_url)
    cassSclk = get_path_from_url(cassSclk_url)
    cassIk = get_path_from_url(cassIk_url)


def cleanup_cassini_kernels():
    cleanup_file(CassiniKernels.cassPck)
    cleanup_file(CassiniKernels.satSpk)
    cleanup_file(CassiniKernels.cassTourSpk)
    cleanup_file(CassiniKernels.cassFk)
    cleanup_file(CassiniKernels.cassCk)
    cleanup_file(CassiniKernels.cassSclk)
    cleanup_file(CassiniKernels.cassIk)


class ExtraKernels(object):
    voyagerSclk_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/main/vg200022.tsc"
    earthTopoTf_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/main/earth_topo_050714.tf"
    earthStnSpk_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/main/earthstns_itrf93_050714.bsp"
    earthHighPerPck_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/main/earth_031228_231229_predict.bpc"
    phobosDsk_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/main/phobos_lores.bds"
    marsSpk_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/main/mar022-1.bsp"
    mroFk_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/main/mro_v15.tf"
    voyagerSclk = get_path_from_url(voyagerSclk_url)
    earthTopoTf = get_path_from_url(earthTopoTf_url)
    earthStnSpk = get_path_from_url(earthStnSpk_url)
    earthHighPerPck = get_path_from_url(earthHighPerPck_url)
    phobosDsk = get_path_from_url(phobosDsk_url)
    marsSpk = get_path_from_url(marsSpk_url)
    mroFk = get_path_from_url(mroFk_url)


def cleanup_extra_kernels():
    cleanup_file(ExtraKernels.voyagerSclk)
    cleanup_file(ExtraKernels.earthTopoTf)
    cleanup_file(ExtraKernels.earthStnSpk)
    cleanup_file(ExtraKernels.earthHighPerPck)
    cleanup_file(ExtraKernels.phobosDsk)
    cleanup_file(ExtraKernels.marsSpk)
    cleanup_file(ExtraKernels.mroFk)


class CoreKernels(object):
    # note this gets updated
    currentLSK = "naif0012.tls"
    #
    pck_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/main/pck00010.tpc"
    spk_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/main/de405s_{}endian.bsp".format(
        sys.byteorder
    )
    gm_pck_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/main/gm_de431.tpc"
    lsk_url = "https://raw.githubusercontent.com/AndrewAnnex/SpiceyPyTestKernels/main/{}".format(
        currentLSK
    )
    pck = get_path_from_url(pck_url)
    spk = get_path_from_url(spk_url)
    gm_pck = get_path_from_url(gm_pck_url)
    lsk = get_path_from_url(lsk_url)
    standardKernelList = [pck, spk, gm_pck, lsk]
    testMetaKernel = os.path.join(cwd, "exampleKernels.txt")


def cleanup_core_kernels():
    cleanup_file(CoreKernels.pck)
    cleanup_file(CoreKernels.spk)
    cleanup_file(CoreKernels.gm_pck)
    cleanup_file(CoreKernels.lsk)


def get_kernel(url):
    kernel_name = get_kernel_name_from_url(url)
    kernel_file = os.path.join(cwd, kernel_name)
    # does not download if files are present, which allows us to potentially cache kernels
    if not os.path.isfile(kernel_file):
        attempt_download(url, kernel_name, kernel_file, 5)


def attempt_download(url, kernel_name, target_file_name, num_attempts):
    current_attempt = 0
    while current_attempt < num_attempts:
        try:
            print("Attempting to Download kernel: {}".format(kernel_name), flush=True)
            current_kernel = urllib.request.urlopen(url, timeout=10)
            with open(target_file_name, "wb") as kernel:
                kernel.write(current_kernel.read())
            print("Downloaded kernel: {}".format(kernel_name), flush=True)
            break
        # N.B. .HTTPError inherits from .URLError, so [except:....HTTPError]
        #      must be listed before [except:....URLError], otherwise the
        #      .HTTPError exception cannot be caught
        except urllib.error.HTTPError as h:
            print(
                "Some http error when downloading kernel {}, error: ".format(
                    kernel_name
                ),
                h,
                ", trying again after a bit.",
            )
        except urllib.error.URLError:
            print(
                "Download of kernel: {} failed with URLError, trying again after a bit.".format(
                    kernel_name
                ),
                flush=True,
            )
        current_attempt += 1
        print("\t Attempting to Download kernel again...", flush=True)
        time.sleep(2 + current_attempt)
    if current_attempt >= num_attempts:
        raise BaseException(
            "Error Downloading kernel: {}, check if kernel exists at url: {}".format(
                kernel_name, url
            )
        )


def get_standard_kernels():
    print("\tChecking for kernels...\n", flush=True)
    get_kernel(CoreKernels.pck_url)
    get_kernel(CoreKernels.spk_url)
    get_kernel(CoreKernels.gm_pck_url)
    get_kernel(CoreKernels.lsk_url)


def get_extra_test_kernels():
    # these are test kernels not included in the standard meta kernel
    get_kernel(ExtraKernels.voyagerSclk_url)
    get_kernel(ExtraKernels.earthTopoTf_url)
    get_kernel(ExtraKernels.earthStnSpk_url)
    get_kernel(ExtraKernels.earthHighPerPck_url)
    get_kernel(ExtraKernels.phobosDsk_url)
    get_kernel(ExtraKernels.marsSpk_url)
    get_kernel(ExtraKernels.mroFk_url)


def get_cassini_test_kernels():
    get_kernel(CassiniKernels.cassPck_url)
    get_kernel(CassiniKernels.satSpk_url)
    get_kernel(CassiniKernels.cassTourSpk_url)
    get_kernel(CassiniKernels.cassFk_url)
    get_kernel(CassiniKernels.cassCk_url)
    get_kernel(CassiniKernels.cassSclk_url)
    get_kernel(CassiniKernels.cassIk_url)


def write_test_meta_kernel():
    # Update the paths!
    with open(os.path.join(cwd, "exampleKernels.txt"), "w") as kernelFile:
        kernelFile.write("\\begindata\n")
        kernelFile.write("KERNELS_TO_LOAD = (\n")
        for kernel in CoreKernels.standardKernelList:
            kernelFile.write("'{0}'\n".format(os.path.join(cwd, kernel)))
        kernelFile.write(")\n")
        kernelFile.write("\\begintext")
    print("\nDone writing test meta kernel.", flush=True)


def download_kernels():
    get_standard_kernels()  # Download the kernels listed in kernelList and kernelURLlist
    get_cassini_test_kernels()  # Download Cassini kernels
    get_extra_test_kernels()  # Download any extra test kernels we need
    write_test_meta_kernel()  # Create the meta kernel file for tests
