from __future__ import print_function
import spiceypy

def sclket():

    mkfile = 'sclket.tm'
    spiceypy.furnsh(mkfile)

    utc =  '2004-06-11T19:32:00'
    et = spiceypy.str2et(utc)

    print('UTC       = {:s}'.format(utc))
    print('ET        = {:20.6f}'.format(et))

    scid = -82
    sclk = '1465674964.105'
    et = spiceypy.scs2e(scid, sclk)

    print('SCLK      = {:s}'.format(sclk))
    print('ET        = {:20.6f}'.format(et))

    spiceypy.unload(mkfile)


if __name__ == '__main__':
    sclket()
