import spiceypy


def scvel():

    mkfile = "scvel.tm"
    spiceypy.furnsh(mkfile)

    utc = "2004-06-11T19:32:00"
    et = spiceypy.str2et(utc)

    print(f"UTC       = {utc:s}")
    print(f"ET        = {et:20.6f}")

    scid = -82
    sclk = "1465674964.105"
    et = spiceypy.scs2e(scid, sclk)

    print(f"SCLK      = {sclk:s}")
    print(f"ET        = {et:20.6f}")

    target = "CASSINI"
    frame = "ECLIPJ2000"
    corrtn = "NONE"
    observ = "SUN"

    state, ltime = spiceypy.spkezr(target, et, frame, corrtn, observ)

    print(f" X        = {state[0]:20.6f}")
    print(f" Y        = {state[1]:20.6f}")
    print(f" Z        = {state[2]:20.6f}")
    print(f"VX        = {state[3]:20.6f}")
    print(f"VY        = {state[4]:20.6f}")
    print(f"VZ        = {state[5]:20.6f}")

    target = "SUN"
    frame = "CASSINI_INMS"
    corrtn = "LT+S"
    observ = "CASSINI"

    sundir, ltime = spiceypy.spkpos(target, et, frame, corrtn, observ)
    sundir = spiceypy.vhat(sundir)

    print(f"SUNDIR(X) = {sundir[0]:20.6f}")
    print(f"SUNDIR(Y) = {sundir[1]:20.6f}")
    print(f"SUNDIR(Z) = {sundir[2]:20.6f}")

    method = "NEAR POINT: ELLIPSOID"
    target = "PHOEBE"
    frame = "IAU_PHOEBE"
    corrtn = "NONE"
    observ = "CASSINI"

    spoint, trgepc, srfvec = spiceypy.subpnt(method, target, et, frame, corrtn, observ)

    srad, slon, slat = spiceypy.reclat(spoint)

    fromfr = "IAU_PHOEBE"
    tofr = "CASSINI_INMS"

    m2imat = spiceypy.pxform(fromfr, tofr, et)

    sbpdir = spiceypy.mxv(m2imat, srfvec)
    sbpdir = spiceypy.vhat(sbpdir)

    print(f"LON       = {slon * spiceypy.dpr():20.6f}")
    print(f"LAT       = {slat * spiceypy.dpr():20.6f}")
    print(f"SBPDIR(X) = {sbpdir[0]:20.6f}")
    print(f"SBPDIR(Y) = {sbpdir[1]:20.6f}")
    print(f"SBPDIR(Z) = {sbpdir[2]:20.6f}")

    target = "CASSINI"
    frame = "J2000"
    corrtn = "NONE"
    observ = "PHOEBE"

    state, ltime = spiceypy.spkezr(target, et, frame, corrtn, observ)
    scvdir = state[3:6]

    fromfr = "J2000"
    tofr = "CASSINI_INMS"
    j2imat = spiceypy.pxform(fromfr, tofr, et)

    scvdir = spiceypy.mxv(j2imat, scvdir)
    scvdir = spiceypy.vhat(scvdir)

    print(f"SCVDIR(X) = {scvdir[0]:20.6f}")
    print(f"SCVDIR(Y) = {scvdir[1]:20.6f}")
    print(f"SCVDIR(Z) = {scvdir[2]:20.6f}")

    spiceypy.unload(mkfile)


if __name__ == "__main__":
    scvel()
