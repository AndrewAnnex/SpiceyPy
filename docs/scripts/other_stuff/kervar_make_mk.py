mk = r"""
  KPL/MK
     Name the kernels to load. Use path symbols.
     The names and contents of the kernels referenced by this
     meta-kernel are as follows:
        File Name        Description
        ---------------  ------------------------------
        naif0008.tls     Generic LSK.
        de405s.bsp       Planet Ephemeris SPK.
        pck00008.tpc     Generic PCK.
  \begindata
     PATH_VALUES     = ('kernels/spk',
                        'kernels/pck',
                        'kernels/lsk')
     PATH_SYMBOLS    = ('SPK' , 'PCK' , 'LSK' )
     KERNELS_TO_LOAD = ( '$SPK/de405s.bsp',
                         '$PCK/pck00008.tpc',
                         '$LSK/naif0008.tls')
  \begintext
  Ring model data.
  \begindata
     BODY699_RING1_NAME     = 'A Ring'
     BODY699_RING1          = (122170.0 136780.0 0.1 0.1 0.5)
     BODY699_RING1_1_NAME   = 'Encke Gap'
     BODY699_RING1_1        = (133405.0 133730.0 0.0 0.0 0.0)
     BODY699_RING2_NAME     = 'Cassini Division'
     BODY699_RING2          = (117580.0 122170.0 0.0 0.0 0.0)
  \begintext
  The kernel pool recognizes values preceded by '@' as time
  values. When read, the kernel subsystem converts these
  representations into double precision ephemeris time.
  Caution: The kernel subsystem interprets the time strings
  identified by '@' as TDB. The same string passed as input
  to @STR2ET is processed as UTC.
  The three expressions stored in the EXAMPLE_TIMES array represent
  the same epoch.
  \begindata
     EXAMPLE_TIMES       = ( @APRIL-1-2004-12:34:56.789,
                             @4/1/2004-12:34:56.789,
                             @JD2453097.0242684
                            )
  \begintext
"""
with open("kervar.tm", "w") as dst:
    dst.write(mk)
print("Wrote kernel file kervar.tm")
