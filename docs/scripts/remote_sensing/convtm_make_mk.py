mk = r"""
KPL/MK

   This is the meta-kernel used in the solution of the "Time
   Conversion" task in the Remote Sensing Hands On Lesson.

   The names and contents of the kernels referenced by this
   meta-kernel are as follows:

   File name                   Contents
   --------------------------  -----------------------------
   naif0008.tls                Generic LSK
   cas00084.tsc                Cassini SCLK


   \begindata
   KERNELS_TO_LOAD = ( 'kernels/lsk/naif0008.tls',
                       'kernels/sclk/cas00084.tsc' )
   \begintext
"""
with open("convtm.tm", "w") as dst:
    dst.write(mk)
print("Wrote kernel file convtm.tm")
