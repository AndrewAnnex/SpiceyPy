mk = r"""
KPL/MK
\begindata
KERNELS_TO_LOAD = ( 'kernels/lsk/naif0008.tls',
                    'kernels/spk/de405s.bsp',
                    'kernels/pck/pck00008.tpc')
"""
with open("xtic.tm", "w") as dst:
    dst.write(mk)
print("Wrote kernel file corrd.tm")
#
# Import the CSPICE-Python interface.
#
import spiceypy


def xtic():
    #
    # Assign the META variable to the name of the meta-kernel
    # that contains the LSK kernel and create an arbitrary
    # time string.
    #
    CALSTR = "Mar 15, 2003 12:34:56.789 AM PST"
    META = "xtic.tm"
    AMBIGSTR = "Mar 15, 79 12:34:56"
    T_FORMAT1 = "Wkd Mon DD HR:MN:SC PDT YYYY ::UTC-7"
    T_FORMAT2 = "Wkd Mon DD HR:MN ::UTC-7 YR (JULIAND.##### JDUTC)"
    #
    # Load the meta-kernel.
    #
    spiceypy.furnsh(META)
    print(f"Original time string     : f{CALSTR}")
    #
    # Convert the time string to the number of ephemeris
    # seconds past the J2000 epoch. This is the most common
    # internal time representation used by the CSPICE
    # system; CSPICE refers to this as ephemeris time (ET).
    #
    et = spiceypy.str2et(CALSTR)
    print(f"Corresponding ET         : {et:20.6f}\n")
    #
    # Make a picture of an output format. Describe a Unix-like
    # time string then send the picture and the 'et' value through
    # spiceypy.timout to format and convert the ET representation
    # of the time string into the form described in
    # spiceypy.timout. The '::UTC-7' token indicates the time
    # zone for the `timstr' output - PDT. 'PDT' is part of the
    # output, but not a time system token.
    #
    timstr = spiceypy.timout(et, T_FORMAT1)
    print(f"Time in string format 1  : {timstr}")
    timstr = spiceypy.timout(et, T_FORMAT2)
    print(f"Time in string format 2  : {timstr}")
    #
    # Why create a picture by hand when spiceypy can do it for
    # you? Input a string to spiceypy.tpictr with the format of
    # interest. `ok' returns a boolean indicating whether an
    # error occurred while parsing the picture string, if so,
    # an error diagnostic message returns in 'xerror'. In this
    # example the picture string is known as correct.
    #
    pic = "12:34:56.789 P.M. PDT January 1, 2006"
    [pictr, ok, xerror] = spiceypy.tpictr(pic)
    if not bool(ok):
        print(xerror)
        return
    timstr = spiceypy.timout(et, pictr)
    print(f"Time in string format 3  : {timstr}")
    #
    # Two digit year representations often cause problems due to
    # the ambiguity of the century. The routine spiceypy.tsetyr
    # gives the user the ability to set a default range for 2
    # digit year representation. SPICE uses 1969AD as the default
    # start year so the numbers inclusive of 69 to 99 represent
    # years 1969AD to 1999AD, the numbers inclusive of 00 to 68
    # represent years 2000AD to 2068AD.
    #
    # The defined time string 'AMBIGSTR' contains a two-digit
    # year. Since the SPICE base year is 1969, the time subsystem
    # interprets the string as 1979.
    #
    et1 = spiceypy.str2et(AMBIGSTR)
    #
    # Set 1980 as the base year causes SPICE to interpret the
    # time string's "79" as 2079.
    #
    spiceypy.tsetyr(1980)
    et2 = spiceypy.str2et(AMBIGSTR)
    #
    # Calculate the number of years between the two ET
    # representations, ~100.
    #
    years = (et2 - et1) / spiceypy.jyear()
    print(f"Years between evaluations: {years:20.6f}")
    #
    # Reset the default year to 1969.
    #
    spiceypy.tsetyr(1969)
    #
    # Done. Unload the kernels.
    #
    spiceypy.kclear()


if __name__ == "__main__":
    xtic()
