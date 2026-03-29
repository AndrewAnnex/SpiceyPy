#
# Solution xform.py
#
import spiceypy


def xform(utctim="2004 jun 11 19:32:00"):
    METAKR = "xform.tm"
    spiceypy.furnsh(METAKR)
    print(f"Converting UTC Time: {utctim}")
    et = spiceypy.str2et(utctim)
    print(f"   ET seconds past J2000: {et:16.3f}")

    # Compute the apparent state of Phoebe as seen from CASSINI in J2000.
    state, ltime = spiceypy.spkezr("PHOEBE", et, "J2000", "LT+S", "CASSINI")

    # Obtain the state transformation from J2000 to the non-inertial
    # body-fixed IAU_PHOEBE frame at the light-time corrected epoch.
    sform = spiceypy.sxform("J2000", "IAU_PHOEBE", et - ltime)

    # Rotate the apparent J2000 state into IAU_PHOEBE.
    bfixst = spiceypy.mxvg(sform, state)

    print(
        "   Apparent state of Phoebe as seen from CASSINI in the IAU_PHOEBE\n"
        "      body-fixed frame (km, km/s):"
    )
    print(f"      X = {bfixst[0]:19.6f}")
    print(f"      Y = {bfixst[1]:19.6f}")
    print(f"      Z = {bfixst[2]:19.6f}")
    print(f"     VX = {bfixst[3]:19.6f}")
    print(f"     VY = {bfixst[4]:19.6f}")
    print(f"     VZ = {bfixst[5]:19.6f}")

    # All of the above can be done with a single spkezr call directly
    # into the target frame. This is slightly more accurate for velocity
    # because it accounts for the rate of change of light time on the
    # apparent angular velocity of the body-fixed frame.
    state, ltime = spiceypy.spkezr("PHOEBE", et, "IAU_PHOEBE", "LT+S", "CASSINI")

    print(
        "   Apparent state of Phoebe as seen from CASSINI in the IAU_PHOEBE\n"
        "      body-fixed frame (km, km/s) obtained using spkezr directly:"
    )
    print(f"      X = {state[0]:19.6f}")
    print(f"      Y = {state[1]:19.6f}")
    print(f"      Z = {state[2]:19.6f}")
    print(f"     VX = {state[3]:19.6f}")
    print(f"     VY = {state[4]:19.6f}")
    print(f"     VZ = {state[5]:19.6f}")

    # Compute the angular separation between the apparent position of Earth
    # as seen from CASSINI and the nominal HGA boresight (+Z of CASSINI_HGA).
    pos, _ = spiceypy.spkpos("EARTH", et, "J2000", "LT+S", "CASSINI")

    # Rotate the nominal boresight from CASSINI_HGA into J2000.
    bsight = spiceypy.mxv(spiceypy.pxform("CASSINI_HGA", "J2000", et), [0.0, 0.0, 1.0])

    sep = spiceypy.convrt(spiceypy.vsep(bsight, pos), "RADIANS", "DEGREES")
    print(
        f"   Angular separation between the apparent position of\n"
        f"      Earth and the CASSINI high gain antenna boresight (degrees):\n"
        f"      {sep:16.3f}"
    )

    # Alternatively, work directly in the antenna frame.
    pos, _ = spiceypy.spkpos("EARTH", et, "CASSINI_HGA", "LT+S", "CASSINI")

    # The antenna boresight is the Z-axis in the CASSINI_HGA frame.
    sep = spiceypy.convrt(spiceypy.vsep([0.0, 0.0, 1.0], pos), "RADIANS", "DEGREES")
    print(
        "   Angular separation between the apparent position of\n"
        "      Earth and the CASSINI high gain antenna boresight computed\n"
        "      using vectors in the CASSINI_HGA frame (degrees):\n"
        f"      {sep:16.3f}"
    )

    spiceypy.unload(METAKR)


xform()
