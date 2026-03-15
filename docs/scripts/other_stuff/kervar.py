#
# Import the CSPICE-Python interface.
#
import spiceypy


def kervar():
    #
    # Define the max number of kernel variables
    # of concern for this examples.
    #
    N_ITEMS = 20
    #
    # Load the example kernel containing the kernel variables.
    # The kernels defined in KERNELS_TO_LOAD load into the
    # kernel pool with this call.
    #
    spiceypy.furnsh("kervar.tm")
    #
    # Initialize the start value. This value indicates
    # index of the first element to return if a kernel
    # variable is an array. START = 0 indicates return everything.
    # START = 1 indicates return everything but the first element.
    #
    START = 0
    #
    # Set the template for the variable names to find. Let's
    # look for all variables containing  the string RING.
    # Define this with the wildcard template '*RING*'. Note:
    # the template '*RING' would match any variable name
    # ending with the RING string.
    #
    tmplate = "*RING*"
    #
    # We're ready to interrogate the kernel pool for the
    # variables matching the template. spiceypy.gnpool tells us:
    #
    #  1. Does the kernel pool contain any variables that
    #     match the template (value of found).
    #  2. If so, how many variables?
    #  3. The variable names. (cvals, an array of strings)
    #
    try:
        cvals = spiceypy.gnpool(tmplate, START, N_ITEMS)
        print("Number variables matching template: {0}".format(len(cvals)))
    except spiceypy.SpiceyError:
        print("No kernel variables matched template.")
        return
    #
    # Okay, now we know something about the kernel pool
    # variables of interest to us. Let's find out more...
    #
    for cval in cvals:
        #
        # Use spiceypy.dtpool to return the dimension and type,
        # C (character) or N (numeric), of each pool
        # variable name in the cvals array. We know the
        # kernel data exists.
        #
        dim, type = spiceypy.dtpool(cval)
        print("\n" + cval)
        print(" Number items: {0}   Of type: {1}\n".format(dim, type))
        #
        # Test character equality, 'N' or 'C'.
        #
        if type == "N":
            #
            # If 'type' equals 'N', we found a numeric array.
            # In this case any numeric array will be an array
            # of double precision numbers ('doubles').
            # spiceypy.gdpool retrieves doubles from the
            # kernel pool.
            #
            dvars = spiceypy.gdpool(cval, START, N_ITEMS)
            for dvar in dvars:
                print("  Numeric value: {0:20.6f}".format(dvar))
        elif type == "C":
            #
            # If 'type' equals 'C', we found a string array.
            # spiceypy.gcpool retrieves string values from the
            # kernel pool.
            #
            cvars = spiceypy.gcpool(cval, START, N_ITEMS)
            for cvar in cvars:
                print("  String value: {0}\n".format(cvar))
        else:
            #
            # This block should never execute.
            #
            print("Unknown type. Code error.")
    #
    # Now look at the time variable EXAMPLE_TIMES. Extract this
    # value as an array of doubles.
    #
    dvars = spiceypy.gdpool("EXAMPLE_TIMES", START, N_ITEMS)
    print("EXAMPLE_TIMES")
    for dvar in dvars:
        print("  Time value:    {0:20.6f}".format(dvar))
    #
    # Done. Unload the kernels.
    #
    spiceypy.kclear()


if __name__ == "__main__":
    kervar()
