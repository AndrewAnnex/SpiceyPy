mk = r"""
KPL/MK
\begindata
KERNELS_TO_LOAD = ( 'kernels/lsk/naif0008.tls',
                    'kernels/spk/de405s.bsp',
                    'kernels/pck/pck00008.tpc')
"""
with open("coord.tm", "w") as dst:
    dst.write(mk)
print("Wrote kernel file corrd.tm")

#
# Import the CSPICE-Python interface.
#
import spiceypy


def coord(timstr: str):
    #
    # Define the inertial and non inertial frame names.
    #
    # Initialize variables or set type. All variables
    # used in a PROMPT construct must be initialized
    # as strings.
    #
    INRFRM = "J2000"
    NONFRM = "IAU_EARTH"
    r2d = spiceypy.dpr()
    #
    # Load the needed kernels using a spiceypy.furnsh call on the
    # meta kernel.
    #
    spiceypy.furnsh("coord.tm")
    #
    # Convert the time string to ephemeris time J2000 (ET).
    #
    et = spiceypy.str2et(timstr)
    #
    # Access the kernel pool data for the triaxial radii of the
    # Earth, rad[1][0] holds the equatorial radius, rad[1][2]
    # the polar radius.
    #
    rad = spiceypy.bodvrd("EARTH", "RADII", 3)
    #
    # Calculate the flattening factor for the Earth.
    #
    #          equatorial_radius - polar_radius
    # flat =   ________________________________
    #
    #                equatorial_radius
    #
    flat = (rad[1][0] - rad[1][2]) / rad[1][0]
    #
    # Make the spiceypy.spkpos call to determine the apparent
    # position of the Moon w.r.t. to the Earth at 'et' in the
    # inertial frame.
    #
    [pos, ltime] = spiceypy.spkpos("MOON", et, INRFRM, "LT+S", "EARTH")
    #
    # Show the current frame and time.
    #
    print(" Time : {0}".format(timstr))
    print(" Inertial Frame: {0}\n".format(INRFRM))
    #
    # First convert the position vector
    # X = pos(1), Y = pos(2), Z = pos(3), to RA/DEC.
    #
    [range, ra, dec] = spiceypy.recrad(pos)
    print("   Range/Ra/Dec")
    print("    Range: {0:20.6f}".format(range))
    print("    RA   : {0:20.6f}".format(ra * r2d))
    print("    DEC  : {0:20.6f}".format(dec * r2d))
    #
    # ...latitudinal coordinates...
    #
    [range, lon, lat] = spiceypy.reclat(pos)
    print("   Latitudinal ")
    print("    Rad  : {0:20.6f}".format(range))
    print("    Lon  : {0:20.6f}".format(lon * r2d))
    print("    Lat  : {0:20.6f}".format(lat * r2d))
    #
    # ...spherical coordinates use the colatitude,
    # the angle from the Z axis.
    #
    [range, colat, lon] = spiceypy.recsph(pos)
    print("   Spherical")
    print("    Rad  : {0:20.6f}".format(range))
    print("    Lon  : {0:20.6f}".format(lon * r2d))
    print("    Colat: {0:20.6f}".format(colat * r2d))
    #
    # Make the spiceypy.spkpos call to determine the apparent
    # position of the Moon w.r.t. to the Earth at 'et' in the
    # non-inertial, body fixed, frame.
    #
    [pos, ltime] = spiceypy.spkpos("MOON", et, NONFRM, "LT+S", "EARTH")
    print()
    print("  Non-inertial Frame: {0}".format(NONFRM))
    #
    # ...latitudinal coordinates...
    #
    [range, lon, lat] = spiceypy.reclat(pos)
    print("   Latitudinal ")
    print("    Rad  : {0:20.6f}".format(range))
    print("    Lon  : {0:20.6f}".format(lon * r2d))
    print("    Lat  : {0:20.6f}".format(lat * r2d))
    #
    # ...spherical coordinates use the colatitude,
    # the angle from the Z axis.
    #
    [range, colat, lon] = spiceypy.recsph(pos)
    print("   Spherical")
    print("    Rad  : {0:20.6f}".format(range))
    print("    Lon  : {0:20.6f}".format(lon * r2d))
    print("    Colat: {0:20.6f}".format(colat * r2d))
    #
    # ...finally, convert the position to geodetic coordinates.
    #
    [lon, lat, range] = spiceypy.recgeo(pos, rad[1][0], flat)
    print("   Geodetic")
    print("    Rad  : {0:20.6f}".format(range))
    print("    Lon  : {0:20.6f}".format(lon * r2d))
    print("    Lat  : {0:20.6f}".format(lat * r2d))
    print()
    #
    # Done. Unload the kernels.
    #
    spiceypy.kclear()


# if running locally, uncomment below
# from builtins import input
# if __name__ == '__main__':
#   timstr = input( 'Time of interest: ')
#   coord(timstr)
