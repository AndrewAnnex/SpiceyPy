# Solution getsta.py
import spiceypy


def getsta(utctim="2004 jun 11 19:32:00"):
    # Local parameters
    METAKR = "getsta.tm"
    # Load the kernels that this program requires.  We
    # will need a leapseconds kernel to convert input
    # UTC time strings into ET.  We also will need the
    # necessary SPK files with coverage for the bodies
    # in which we are interested.
    spiceypy.furnsh(METAKR)

    print(f"Converting UTC Time: {utctim}")
    # Convert utctim to ET.
    et = spiceypy.str2et(utctim)
    print(f"   ET seconds past J2000: {et:16.3f}")

    # Compute the apparent state of Phoebe as seen from CASSINI in the
    # J2000 frame. Ephemeris readers return km and km/s.
    state, ltime = spiceypy.spkezr("PHOEBE", et, "J2000", "LT+S", "CASSINI")

    print(
        "   Apparent state of Phoebe as seen from CASSINI in the J2000\n"
        "      frame (km, km/s):"
    )
    print(f"      X = {state[0]:16.3f}")
    print(f"      Y = {state[1]:16.3f}")
    print(f"      Z = {state[2]:16.3f}")
    print(f"     VX = {state[3]:16.3f}")
    print(f"     VY = {state[4]:16.3f}")
    print(f"     VZ = {state[5]:16.3f}")

    # Compute the apparent position of Earth as seen from CASSINI.
    # Note: spkpos instead of spkezr since we only need position.
    pos, ltime = spiceypy.spkpos("EARTH", et, "J2000", "LT+S", "CASSINI")

    print(
        "   Apparent position of Earth as seen from CASSINI in the J2000\n"
        "      frame (km):"
    )
    print(f"      X = {pos[0]:16.3f}")
    print(f"      Y = {pos[1]:16.3f}")
    print(f"      Z = {pos[2]:16.3f}")

    # ltime is the one-way light time between CASSINI and Earth.
    print(
        f"   One way light time between CASSINI and the apparent position\n"
        f"      of Earth (seconds): {ltime:16.3f}"
    )

    # Compute the apparent position of the Sun as seen from Phoebe in the J2000 frame.
    pos, ltime = spiceypy.spkpos("SUN", et, "J2000", "LT+S", "PHOEBE")

    print(
        "   Apparent position of Sun as seen from Phoebe in the\n"
        "       J2000 frame (km):"
    )
    print(f"      X = {pos[0]:16.3f}")
    print(f"      Y = {pos[1]:16.3f}")
    print(f"      Z = {pos[2]:16.3f}")

    # For the actual (geometric) distance we use no aberration correction,
    # then convert km to AU.
    pos, _ = spiceypy.spkpos("SUN", et, "J2000", "NONE", "PHOEBE")
    dist = spiceypy.convrt(spiceypy.vnorm(pos), "KM", "AU")

    print(
        f"   Actual distance between Sun and Phoebe body centers:\n"
        f"      (AU): {dist:16.3f}"
    )

    spiceypy.unload(METAKR)


# provide the input UTC Time:
getsta("2004 jun 11 19:32:00")
