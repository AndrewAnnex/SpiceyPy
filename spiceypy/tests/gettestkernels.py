import os
import six.moves.urllib as urllib

standardKernelList = ['pck00010.tpc',
                      'de421.bsp',
                      'gm_de431.tpc',
                      'naif0011.tls']
cwd = os.path.realpath(os.path.dirname(__file__))


def getKernel(url):
    kernelName = url.split('/')[-1]
    kernelFile = os.path.join(cwd, kernelName)
    # does not download if files are present, which allows us to potentially cache kernels
    if not os.path.isfile(kernelFile):
        print('Downloading: {0}'.format(kernelName))
        with open(kernelFile, "wb") as kernel:
            kernel.write(urllib.request.urlopen(url).read())


def getStandardKernels():
    print("\tChecking for kernels...\n")
    kernelURLlist = ['http://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/pck00010.tpc',
                     'http://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/a_old_versions/de421.bsp',
                     'http://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/gm_de431.tpc',
                     'http://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0011.tls']
    for kernel in kernelURLlist:
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


def getExtraMarsTestKernels():
    merExt10 = "https://naif.jpl.nasa.gov/pub/naif/pds/data/mer1-m-spice-6-v1.0/mer1sp_1000/data/spk/mer1_surf_rover_ext10_v1.bsp"
    getKernel(merExt10)
    merExt11 = "https://naif.jpl.nasa.gov/pub/naif/pds/data/mer1-m-spice-6-v1.0/mer1sp_1000/data/spk/mer1_surf_rover_ext11_v1.bsp"
    getKernel(merExt11)
    merIau2000 = "https://naif.jpl.nasa.gov/pub/naif/pds/data/mer1-m-spice-6-v1.0/mer1sp_1000/data/spk/mer1_ls_040128_iau2000_v1.bsp"
    getKernel(merIau2000)
    merFK = "https://naif.jpl.nasa.gov/pub/naif/MER/kernels/fk/mer1_v10.tf"
    getKernel(merFK)
    print("About to Download 'mro_psp1.bsp' which is over 170MB...")
    mroPsp = "https://naif.jpl.nasa.gov/pub/naif/MRO/kernels/spk/mro_psp1.bsp"
    getKernel(mroPsp)

def getMGSTestKernels():
    mgsSclk = "https://naif.jpl.nasa.gov/pub/naif/pds/data/mgs-m-spice-6-v1.0/mgsp_1000/data/sclk/mgs_sclkscet_00061.tsc"
    getKernel(mgsSclk)
    mgsPck = "https://naif.jpl.nasa.gov/pub/naif/pds/data/ody-m-spice-6-v1.0/odsp_1000/data/pck/mars_iau2000_v0.tpc"
    getKernel(mgsPck)
    mgsIk = "https://naif.jpl.nasa.gov/pub/naif/pds/data/mgs-m-spice-6-v1.0/mgsp_1000/data/ik/mgs_moc_v20.ti"
    getKernel(mgsIk)
    mgsSpk = "https://naif.jpl.nasa.gov/pub/naif/pds/data/mgs-m-spice-6-v1.0/mgsp_1000/data/spk/mgs_ext26.bsp"
    getKernel(mgsSpk)
    mgsCk = "https://naif.jpl.nasa.gov/pub/naif/pds/data/mgs-m-spice-6-v1.0/mgsp_1000/data/ck/mgs_sc_ext26.bc"
    getKernel(mgsCk)

def writeTestMetaKernel():
    # Update the paths!
    with open(os.path.join(cwd, "exampleKernels.txt"), 'w') as kernelFile:
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
    # Now create the meta kernel file for tests
    writeTestMetaKernel()
    # Now download other extra kernels
    getExtraMarsTestKernels()
    getMGSTestKernels()


if __name__ == '__main__':
    downloadKernels()
