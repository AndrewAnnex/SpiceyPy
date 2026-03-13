import spiceypy


def erotat():
    METAKR = "erotat.tm"

    x = [1.0, 0.0, 0.0]
    z = [0.0, 0.0, 1.0]

    spiceypy.furnsh(METAKR)

    timstr = "2007 JAN 1 00:00:00"
    et = spiceypy.str2et(timstr)

    #
    # Look up the apparent position of the Moon relative
    # to the Earth's center in the IAU_EARTH frame at ET.
    #
    [lmoonv, ltime] = spiceypy.spkpos("moon", et, "iau_earth", "lt+s", "earth")
    #
    # Express the Moon direction in terms of longitude
    # and latitude in the IAU_EARTH frame.
    #
    [r, lon, lat] = spiceypy.reclat(lmoonv)

    print(
        f"Earth-Moon direction using low accuracy\n"
        f"PCK and IAU_EARTH frame:\n"
        f"Moon lon (deg):        {lon * spiceypy.dpr():15.6f}\n"
        f"Moon lat (deg):        {lat * spiceypy.dpr():15.6f}\n"
    )
    #
    # Look up the apparent position of the Moon relative
    # to the Earth's center in the ITRF93 frame at ET.
    #
    [hmoonv, ltime] = spiceypy.spkpos("moon", et, "ITRF93", "lt+s", "earth")
    #
    # Express the Moon direction in terms of longitude
    # and latitude in the ITRF93 frame.
    #
    [r, lon, lat] = spiceypy.reclat(hmoonv)

    print(
        f"Earth-Moon direction using high accuracy\n"
        f"PCK and ITRF93 frame:\n"
        f"Moon lon (deg):        {lon * spiceypy.dpr():15.6f}\n"
        f"Moon lat (deg):        {lat * spiceypy.dpr():15.6f}\n"
    )
    #
    # Find the angular separation of the Moon position
    # vectors in degrees.
    #
    sep = spiceypy.dpr() * spiceypy.vsep(lmoonv, hmoonv)

    print(f"Earth-Moon vector separation angle (deg):     {sep:15.6f}\n")

    #
    # Next, express the +Z and +X axes of the ITRF93 frame in
    # the IAU_EARTH frame. We'll do this for two times: et
    # and et + 100 days.
    #
    for i in range(2):
        t = et + i * spiceypy.spd() * 100

        outstr = spiceypy.timout(t, "YYYY-MON-DD HR:MN:SC.### (UTC)")

        print(f"Epoch: {outstr:s}")

        #
        # Find the rotation matrix for conversion of
        # position vectors from the IAU_EARTH to the
        # ITRF93 frame.
        #
        rmat = spiceypy.pxform("iau_earth", "itrf93", t)
        itrfx = rmat[0]
        itrfz = rmat[2]

        #
        # Display the angular offsets of the ITRF93
        # +X and +Z axes from their IAU_EARTH counterparts.
        #
        sep = spiceypy.vsep(itrfx, x)

        print(f"ITRF93 - IAU_EARTH +X axis separation angle (deg): {sep * spiceypy.dpr():13.6f}")

        sep = spiceypy.vsep(itrfz, z)

        print(f"ITRF93 - IAU_EARTH +Z axis separation angle (deg): {sep * spiceypy.dpr():13.6f}\n")

    #
    # Find the azimuth and elevation of apparent
    # position of the Moon in the local topocentric
    # reference frame at the DSN station DSS-13.
    # First look up the Moon's position relative to the
    # station in that frame.
    #
    [topov, ltime] = spiceypy.spkpos("moon", et, "DSS-13_TOPO", "lt+s", "DSS-13")

    #
    # Express the station-moon direction in terms of longitude
    # and latitude in the DSS-13_TOPO frame.
    #
    [r, lon, lat] = spiceypy.reclat(topov)

    #
    # Convert to azimuth-elevation.
    #
    az = -lon

    if az < 0.0:
        az += spiceypy.twopi()

    el = lat

    print(
        f"DSS-13-Moon az/el using high accuracy PCK and DSS-13_TOPO frame:\n"
        f"Moon Az (deg):        {az * spiceypy.dpr():15.6f}\n"
        f"Moon El (deg):        {el * spiceypy.dpr():15.6f}\n"
    )

    #
    # Find the sub-solar point on the Earth at ET using the
    # Earth body-fixed frame IAU_EARTH. Treat the Sun as
    # the observer.
    #
    [lsub, trgepc, srfvec] = spiceypy.subslr(
        "near point: ellipsoid", "earth", et, "IAU_EARTH", "lt+s", "sun"
    )

    #
    # Display the sub-point in latitudinal coordinates.
    #
    [r, lon, lat] = spiceypy.reclat(lsub)

    print(
        f"Sub-Solar point on Earth using low accuracy\n"
        f"PCK and IAU_EARTH frame:\n"
        f"Sub-Solar lon (deg):   {lon * spiceypy.dpr():15.6f}\n"
        f"Sub-Solar lat (deg):   {lat * spiceypy.dpr():15.6f}\n"
    )

    #
    # Find the sub-solar point on the Earth at ET using the
    # Earth body-fixed frame ITRF93. Treat the Sun as
    # the observer.
    #
    [hsub, trgepc, srfvec] = spiceypy.subslr(
        "near point: ellipsoid", "earth", et, "ITRF93", "lt+s", "sun"
    )

    #
    # Display the sub-point in latitudinal coordinates.
    #
    [r, lon, lat] = spiceypy.reclat(hsub)

    print(
        f"Sub-Solar point on Earth using high accuracy\n"
        f"PCK and ITRF93 frame:\n"
        f"Sub-Solar lon (deg):   {lon * spiceypy.dpr():15.6f}\n"
        f"Sub-Solar lat (deg):   {lat * spiceypy.dpr():15.6f}\n"
    )

    #
    # Find the distance between the sub-solar point
    # vectors in km.
    #
    dist = spiceypy.vdist(lsub, hsub)

    print(f"Distance between sub-solar points (km): {dist:15.6f}")

    spiceypy.unload(METAKR)


if __name__ == "__main__":
    erotat()
