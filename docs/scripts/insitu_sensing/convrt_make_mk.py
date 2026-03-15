mk = r"""
KPL/MK

   The names and contents of the kernels referenced by this
   meta-kernel are as follows:


   File Name                   Description
   --------------------------  ----------------------------------
   naif0008.tls                Generic LSK.

\begindata
   KERNELS_TO_LOAD = (
                     'kernels/lsk/naif0008.tls'
                     )
\begintext
"""
with open("convrt.tm", "w") as dst:
    dst.write(mk)
print("Wrote kernel file convrt.tm")
