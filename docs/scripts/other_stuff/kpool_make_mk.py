mk = r"""
KPL/MK
\begindata
KERNELS_TO_LOAD = ( 'kernels/lsk/naif0008.tls',
                    'kernels/spk/de405s.bsp',
                    'kernels/pck/pck00008.tpc')
\begintext
"""
with open("kpool.tm", "w") as dst:
    dst.write(mk)
print("Wrote kernel file kpool.tm")
