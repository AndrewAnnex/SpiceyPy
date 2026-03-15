#
# Import the CSPICE-Python interface.
#
import spiceypy

aliases = {
    "meter": "METER",
    "klicks": "KM",
    "kilometers": "KM",
    "kilometer": "KM",
    "secs": "SECONDS",
    "miles": "STATUTE_MILES",
}


def tostan(alias):
    return aliases.get(alias, alias)


def units(funits, fvalue, tunits):
    #
    # Display the Toolkit version string with a spiceypy.tkvrsn
    # call.
    #
    vers = spiceypy.tkvrsn("TOOLKIT")
    print("\nConvert demo program compiled against CSPICE Toolkit " + vers)
    #
    # The user first inputs the name of a unit of measure.
    # Send the name through tostan for de-aliasing.
    #
    print(f"From Units : {funits}")
    funits = tostan(funits)
    #
    # Input a double precision value to express in a new
    # unit format.
    #
    print(f"From Value : {fvalue}")
    #
    # Now the user inputs the name of the output units.
    # Again we send the units name through tostan for
    # de-aliasing.
    #
    print(f"To Units : {tunits}")
    tunits = tostan(tunits)
    tvalue = spiceypy.convrt(fvalue, funits, tunits)
    print("{0:12.5f} {1}".format(tvalue, tunits))


if __name__ == "__main__":
    units("klicks", 3, "miles")
    units("miles", 26.2, "km")
