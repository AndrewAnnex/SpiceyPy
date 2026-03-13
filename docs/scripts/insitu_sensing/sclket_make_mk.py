mk = r"""
KPL/MK

   The names and contents of the kernels referenced by this
   meta-kernel are as follows:


   File Name                   Description
   --------------------------  ----------------------------------
   naif0008.tls                Generic LSK.
   cas00084.tsc                Cassini SCLK.

\begindata
   KERNELS_TO_LOAD = (
                     'kernels/lsk/naif0008.tls'
                     'kernels/sclk/cas00084.tsc'
                     )
\begintext
"""
with open("sclket.tm", "w") as dst:
    dst.write(mk)
print("Wrote kernel file sclket.tm")
