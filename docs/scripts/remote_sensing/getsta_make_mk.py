mk = r"""
KPL/MK

   This is the meta-kernel used in the solution of the
   "Obtaining Target States and Positions" task in the
   Remote Sensing Hands On Lesson.

   The names and contents of the kernels referenced by this
   meta-kernel are as follows:

   File name                   Contents
   --------------------------  -----------------------------
   naif0008.tls                Generic LSK
   981005_PLTEPH-DE405S.bsp    Solar System Ephemeris
   020514_SE_SAT105.bsp        Saturnian Satellite Ephemeris
   030201AP_SK_SM546_T45.bsp   Cassini Spacecraft SPK


   \begindata
   KERNELS_TO_LOAD = ( 'kernels/lsk/naif0008.tls',
                       'kernels/spk/981005_PLTEPH-DE405S.bsp',
                       'kernels/spk/020514_SE_SAT105.bsp',
                       'kernels/spk/030201AP_SK_SM546_T45.bsp' )
   \begintext
"""
with open('getsta.tm', 'w') as dst:
    dst.write(mk)
print('Wrote kernel file getsta.tm')
