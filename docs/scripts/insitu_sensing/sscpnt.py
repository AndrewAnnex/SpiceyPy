from __future__ import print_function
import spiceypy

def sscpnt():

    mkfile = 'sscpnt.tm'
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

    target = 'CASSINI'
    frame  = 'ECLIPJ2000'
    corrtn = 'NONE'
    observ = 'SUN'

    state, ltime = spiceypy.spkezr(target, et, frame,
                                   corrtn, observ)

    print(' X        = {:20.6f}'.format(state[0]))
    print(' Y        = {:20.6f}'.format(state[1]))
    print(' Z        = {:20.6f}'.format(state[2]))
    print('VX        = {:20.6f}'.format(state[3]))
    print('VY        = {:20.6f}'.format(state[4]))
    print('VZ        = {:20.6f}'.format(state[5]))

    target = 'SUN'
    frame  = 'CASSINI_INMS'
    corrtn = 'LT+S'
    observ = 'CASSINI'

    sundir, ltime = spiceypy.spkpos(target, et, frame,
                                    corrtn, observ)
    sundir = spiceypy.vhat(sundir)

    print('SUNDIR(X) = {:20.6f}'.format(sundir[0]))
    print('SUNDIR(Y) = {:20.6f}'.format(sundir[1]))
    print('SUNDIR(Z) = {:20.6f}'.format(sundir[2]))

    method = 'NEAR POINT: ELLIPSOID'
    target = 'PHOEBE'
    frame  = 'IAU_PHOEBE'
    corrtn = 'NONE'
    observ = 'CASSINI'

    spoint, trgepc, srfvec = spiceypy.subpnt(method, target, et,
                                             frame, corrtn, observ)

    srad, slon, slat = spiceypy.reclat(spoint)

    fromfr = 'IAU_PHOEBE'
    tofr   = 'CASSINI_INMS'

    m2imat = spiceypy.pxform(fromfr, tofr, et)

    sbpdir = spiceypy.mxv(m2imat, srfvec)
    sbpdir = spiceypy.vhat(sbpdir)

    print('LON       = {:20.6f}'.format(slon * spiceypy.dpr()))
    print('LAT       = {:20.6f}'.format(slat * spiceypy.dpr()))
    print('SBPDIR(X) = {:20.6f}'.format(sbpdir[0]))
    print('SBPDIR(Y) = {:20.6f}'.format(sbpdir[1]))
    print('SBPDIR(Z) = {:20.6f}'.format(sbpdir[2]))

    spiceypy.unload(mkfile)


if __name__ == '__main__':
    sscpnt()
