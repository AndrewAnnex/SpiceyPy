from __future__ import print_function
import spiceypy

def convrt():

    mkfile = 'convrt.tm'
    spiceypy.furnsh(mkfile)

    utc =  '2004-06-11T19:32:00'
    et = spiceypy.str2et(utc)

    print('UTC       = {:s}'.format(utc))
    print('ET        = {:20.6f}'.format(et))

    spiceypy.unload(mkfile)


if __name__ == '__main__':
    convrt()
