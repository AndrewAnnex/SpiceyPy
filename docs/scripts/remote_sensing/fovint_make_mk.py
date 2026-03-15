mk = r"""
KPL/MK

   This is the meta-kernel used in the solution of the
   "Intersecting Vectors with a Triaxial Ellipsoid" task
   in the Remote Sensing Hands On Lesson.

   The names and contents of the kernels referenced by this
   meta-kernel are as follows:

   File name                   Contents
   --------------------------  -----------------------------
   naif0008.tls                Generic LSK
   cas00084.tsc                Cassini SCLK
   981005_PLTEPH-DE405S.bsp    Solar System Ephemeris
   020514_SE_SAT105.bsp        Saturnian Satellite Ephemeris
   030201AP_SK_SM546_T45.bsp   Cassini Spacecraft SPK
   cas_v37.tf                  Cassini FK
   04135_04171pc_psiv2.bc      Cassini Spacecraft CK
   cpck05Mar2004.tpc           Cassini Project PCK
   cas_iss_v09.ti              ISS Instrument Kernel
   phoebe_64q.bds              Phoebe DSK


   \begindata
   KERNELS_TO_LOAD = ( 'kernels/lsk/naif0008.tls',
                       'kernels/sclk/cas00084.tsc',
                       'kernels/spk/981005_PLTEPH-DE405S.bsp',
                       'kernels/spk/020514_SE_SAT105.bsp',
                       'kernels/spk/030201AP_SK_SM546_T45.bsp',
                       'kernels/fk/cas_v37.tf',
                       'kernels/ck/04135_04171pc_psiv2.bc',
                       'kernels/pck/cpck05Mar2004.tpc',
                       'kernels/ik/cas_iss_v09.ti',
                       'kernels/dsk/phoebe_64q.bds' )
   \begintext
"""
with open('fovint.tm', 'w') as dst:
    dst.write(mk)
print('Wrote kernel file fovint.tm')
