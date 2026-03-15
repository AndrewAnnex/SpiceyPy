mk = r"""
KPL/MK

Meta-kernel for the "Earth Rotation" task
in the Binary PCK Hands On Lesson.

The names and contents of the kernels referenced by this
meta-kernel are as follows:

File name                       Contents
------------------------------  ---------------------------------
naif0008.tls                    Generic LSK
de414_2000_2020.bsp             Solar System Ephemeris
earthstns_itrf93_050714.bsp     DSN station Ephemeris
earth_topo_050714.tf            Earth topocentric FK
pck00008.tpc                    NAIF text PCK
earth_000101_070725_070503.bpc  Earth binary PCK


\begindata

KERNELS_TO_LOAD = ( 'kernels/lsk/naif0008.tls'
                    'kernels/spk/de414_2000_2020.bsp'
                    'kernels/spk/earthstns_itrf93_050714.bsp'
                    'kernels/fk/earth_topo_050714.tf'
                    'kernels/pck/pck00008.tpc'
                    'kernels/pck/earth_000101_070725_070503.bpc' )

\begintext
"""
with open("erotat.tm", "w") as dst:
    dst.write(mk)
print("Wrote kernel file erotat.tm")
