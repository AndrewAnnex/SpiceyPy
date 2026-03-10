#
# Import the CSPICE-Python interface.
#
import spiceypy


def xconst():
    #
    # All the function have the same calling sequence:
    #
    #    VALUE = function_name()
    #
    #    some_procedure( function_name() )
    #
    # First a simple example using the seconds per day
    # constant...
    #
    print("Number of (S)econds (P)er (D)ay   : {0:19.12f}".format(spiceypy.spd()))

    #
    # ...then show the value of degrees per radian, 180/Pi...
    #
    print("Number of (D)egrees (P)er (R)adian: {0:19.16f}".format(spiceypy.dpr()))

    #
    # ...and the inverse, radians per degree, Pi/180.
    # It is obvious spiceypy.dpr() equals 1.d/spiceypy.rpd(), or
    # more simply spiceypy.dpr() * spiceypy.rpd() equals 1
    #
    print("Number of (R)adians (P)er (D)egree: {0:19.16f}".format(spiceypy.rpd()))

    #
    # What's the value for the astrophysicist's favorite
    # physical constant (in a vacuum)?
    #
    print("Speed of light in KM per second   : {0:19.12f}".format(spiceypy.clight()))

    #
    # How long (in Julian days) from the J2000 epoch to the
    # J2100 epoch?
    #
    print("Number of days between epochs J2000")
    print("  and J2100     : {0:19.12f}".format(spiceypy.j2100() - spiceypy.j2000()))

    #
    # Redo the calculation returning seconds...
    #
    print("Number of seconds between epochs")
    print(
        "  J2000 and J2100     : {0:19.5f}".format(
            spiceypy.spd() * (spiceypy.j2100() - spiceypy.j2000())
        )
    )

    #
    # ...then tropical years.
    #
    val = (spiceypy.spd() / spiceypy.tyear()) * (spiceypy.j2100() - spiceypy.j2000())
    print("Number of tropical years between")
    print("  epochs J2000 and J2100    : {0:19.12f}".format(val))

    #
    # Finally, how can I convert a radian value to degrees.
    #
    print(
        "Number of degrees in Pi/2 radians of arc: {0:19.16f}".format(
            spiceypy.halfpi() * spiceypy.dpr()
        )
    )

    #
    # and degrees to radians.
    #
    print(
        "Number of radians in 250 degrees of arc : {0:19.16f}".format(
            250.0 * spiceypy.rpd()
        )
    )


if __name__ == "__main__":
    xconst()
