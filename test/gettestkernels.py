__author__ = 'AndrewAnnex'

import os
from six.moves import urllib

standardKernelList = ['pck00010.tpc', 'de421.bsp', 'gm_de431.tpc',
                      'naif0011.tls']
cwd = os.path.realpath(os.path.dirname(__file__))


def getKernel(url):
    kernelName = url.split('/')[-1]
    print('Downloading: {0}'.format(kernelName))
    with open(os.path.join(cwd, kernelName), "wb") as kernel:
        kernel.write(urllib.request.urlopen(url).read())


def getStandardKernels():
    print("\tChecking for kernels...\n")
    kernelURLlist = ['http://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/pck00010.tpc',
                     'http://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/a_old_versions/de421.bsp',
                     'http://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/gm_de431.tpc',
                     'http://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0011.tls']
    for kernel in kernelURLlist:
        if not os.path.isfile(os.path.join(cwd, kernel.split('/')[-1])):
            getKernel(kernel)


def getExtraTestKernels():
    # these are test kernels not included in the standard meta kernel
    voyagerSclk = "http://naif.jpl.nasa.gov/pub/naif/VOYAGER/kernels/sclk/vg200022.tsc"
    getKernel(voyagerSclk)
    earthTopoTf = "http://naif.jpl.nasa.gov/pub/naif/generic_kernels/fk/stations/earth_topo_050714.tf"
    getKernel(earthTopoTf)
    earthStnSpk = "http://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/stations/earthstns_itrf93_050714.bsp"
    getKernel(earthStnSpk)
    earthGenPck = "http://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_720101_070426.bpc"
    getKernel(earthGenPck)


def writeTestMetaKernel():
    # Update the paths!
    with open(os.path.join(cwd, "testKernels.txt"), 'w') as kernelFile:
        kernelFile.write('\\begindata\n')
        kernelFile.write('KERNELS_TO_LOAD = (\n')
        for kernel in standardKernelList:
            kernelFile.write('\'{0}\'\n'.format(os.path.join(cwd, kernel)))
        kernelFile.write(')\n')
        kernelFile.write('\\begintext')
        kernelFile.close()
    print('\nDone writing test meta kernel.')


def downloadKernels():
    # Download the kernels listed in kernelList and kernelURLlist
    getStandardKernels()
    # Now grab any extra test kernels we need
    getExtraTestKernels()
    # Now create the meta kernal file for tests
    writeTestMetaKernel()


if __name__ == '__main__':
    downloadKernels()
    getExtraTestKernels()
