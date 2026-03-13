import spiceypy


def mrotat():
    METAKR = "mrotat.tm"

    spiceypy.furnsh(METAKR)

    timstr = "2007 JAN 1 00:00:00"
    et = spiceypy.str2et(timstr)

    #
    # Look up the apparent position of the Earth relative
    # to the Moon's center in the IAU_MOON frame at ET.
    #
    [imoonv, ltime] = spiceypy.spkpos("earth", et, "iau_moon", "lt+s", "moon")

    #
    # Express the Earth direction in terms of longitude
    # and latitude in the IAU_MOON frame.
    #
    [r, lon, lat] = spiceypy.reclat(imoonv)

    print(
        f"\n"
        f"Moon-Earth direction using low accuracy\n"
        f"PCK and IAU_MOON frame:\n"
        f"Earth lon (deg):        {lon * spiceypy.dpr():15.6f}\n"
        f"Earth lat (deg):        {lat * spiceypy.dpr():15.6f}\n"
    )
    #
    # Look up the apparent position of the Earth relative
    # to the Moon's center in the MOON_ME frame at ET.
    #
    [mmoonv, ltime] = spiceypy.spkpos("earth", et, "moon_me", "lt+s", "moon")
    #
    # Express the Earth direction in terms of longitude
    # and latitude in the MOON_ME frame.
    #
    [r, lon, lat] = spiceypy.reclat(mmoonv)

    print(
        f"Moon-Earth direction using high accuracy\n"
        f"PCK and MOON_ME frame:\n"
        f"Earth lon (deg):        {lon * spiceypy.dpr():15.6f}\n"
        f"Earth lat (deg):        {lat * spiceypy.dpr():15.6f}\n"
    )
    #
    # Find the angular separation of the Earth position
    # vectors in degrees.
    #
    sep = spiceypy.dpr() * spiceypy.vsep(imoonv, mmoonv)

    print("For IAU_MOON vs MOON_ME frames:")
    print(f"Moon-Earth vector separation angle (deg):     {sep:15.6f}\n")
    #
    # Look up the apparent position of the Earth relative
    # to the Moon's center in the MOON_PA frame at ET.
    #
    [pmoonv, ltime] = spiceypy.spkpos("earth", et, "moon_pa", "lt+s", "moon")
    #
    # Express the Earth direction in terms of longitude
    # and latitude in the MOON_PA frame.
    #
    [r, lon, lat] = spiceypy.reclat(pmoonv)

    print(
        f"Moon-Earth direction using high accuracy\n"
        f"PCK and MOON_PA frame:\n"
        f"Earth lon (deg):        {lon * spiceypy.dpr():15.6f}\n"
        f"Earth lat (deg):        {lat * spiceypy.dpr():15.6f}\n"
    )
    #
    # Find the angular separation of the Earth position
    # vectors in degrees.
    #
    sep = spiceypy.dpr() * spiceypy.vsep(pmoonv, mmoonv)

    print("For MOON_PA vs MOON_ME frames:")
    print(f"Moon-Earth vector separation angle (deg):     {sep:15.6f}\n")
    #
    # Find the apparent sub-Earth point on the Moon at ET
    # using the MOON_ME frame.
    #
    [msub, trgepc, srfvec] = spiceypy.subpnt(
        "near point: ellipsoid", "moon", et, "moon_me", "lt+s", "earth"
    )
    #
    # Display the sub-point in latitudinal coordinates.
    #
    [r, lon, lat] = spiceypy.reclat(msub)

    print(
        f"Sub-Earth point on Moon using high accuracy\n"
        f"PCK and MOON_ME frame:\n"
        f"Sub-Earth lon (deg):   {lon * spiceypy.dpr():15.6f}\n"
        f"Sub-Earth lat (deg):   {lat * spiceypy.dpr():15.6f}\n"
    )
    #
    # Find the apparent sub-Earth point on the Moon at
    # ET using the MOON_PA frame.
    #
    [psub, trgepc, srfvec] = spiceypy.subpnt(
        "near point: ellipsoid", "moon", et, "moon_pa", "lt+s", "earth"
    )
    #
    # Display the sub-point in latitudinal coordinates.
    #
    [r, lon, lat] = spiceypy.reclat(psub)

    print(
        f"Sub-Earth point on Moon using high accuracy\n"
        f"PCK and MOON_PA frame:\n"
        f"Sub-Earth lon (deg):   {lon * spiceypy.dpr():15.6f}\n"
        f"Sub-Earth lat (deg):   {lat * spiceypy.dpr():15.6f}\n"
    )
    #
    # Find the distance between the sub-Earth points
    # in km.
    #
    dist = spiceypy.vdist(msub, psub)

    print(f"Distance between sub-Earth points (km): {dist:15.6f}\n")

    spiceypy.unload(METAKR)


if __name__ == "__main__":
    mrotat()
