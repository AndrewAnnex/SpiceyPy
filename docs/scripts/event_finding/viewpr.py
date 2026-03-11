#
# Solution viewpr
#
import spiceypy
import spiceypy.utils.support_types as stypes


def viewpr():
    #
    # Local Parameters
    #
    METAKR = "viewpr.tm"
    TDBFMT = "YYYY MON DD HR:MN:SC.### (TDB) ::TDB"
    MAXIVL = 1000
    MAXWIN = 2 * MAXIVL
    #
    # Load the meta-kernel.
    #
    spiceypy.furnsh(METAKR)
    #
    # Assign the inputs for our search.
    #
    # Since we're interested in the apparent location of the
    # target, we use light time and stellar aberration
    # corrections. We use the "converged Newtonian" form
    # of the light time correction because this choice may
    # increase the accuracy of the occultation times we'll
    # compute using gfoclt.
    #
    srfpt = "DSS-14"
    obsfrm = "DSS-14_TOPO"
    target = "MEX"
    abcorr = "CN+S"
    start = "2004 MAY 2 TDB"
    stop = "2004 MAY 6 TDB"
    elvlim = 6.0
    #
    # The elevation limit above has units of degrees; we convert
    # this value to radians for computation using SPICE routines.
    # We'll store the equivalent value in radians in revlim.
    #
    revlim = spiceypy.rpd() * elvlim
    #
    # Since SPICE doesn't directly support the AZ/EL coordinate
    # system, we use the equivalent constraint
    #
    #    latitude > revlim
    #
    # in the latitudinal coordinate system, where the reference
    # frame is topocentric and is centered at the viewing location.
    #
    crdsys = "LATITUDINAL"
    coord = "LATITUDE"
    relate = ">"
    #
    # The adjustment value only applies to absolute extrema
    # searches; simply give it an initial value of zero
    # for this inequality search.
    #
    adjust = 0.0
    #
    # stepsz is the step size, measured in seconds, used to search
    # for times bracketing a state transition. Since we don't expect
    # any events of interest to be shorter than five minutes, and
    # since the separation between events is well over 5 minutes,
    # we'll use this value as our step size. Units are seconds.
    #
    stepsz = 300.0
    #
    # Display a banner for the output report:
    #
    print("\n{:s}\n".format("Inputs for target visibility search:"))
    print("   Target                       = {:s}".format(target))
    print("   Observation surface location = {:s}".format(srfpt))
    print("   Observer's reference frame   = {:s}".format(obsfrm))
    print("   Elevation limit (degrees)    = {:f}".format(elvlim))
    print("   Aberration correction        = {:s}".format(abcorr))
    print("   Step size (seconds)          = {:f}".format(stepsz))
    #
    # Convert the start and stop times to ET.
    #
    etbeg = spiceypy.str2et(start)
    etend = spiceypy.str2et(stop)
    #
    # Display the search interval start and stop times
    # using the format shown below.
    #
    #    2004 MAY 06 20:15:00.000 (TDB)
    #
    timstr = spiceypy.timout(etbeg, TDBFMT)
    print("   Start time                   = {:s}".format(timstr))
    timstr = spiceypy.timout(etend, TDBFMT)
    print("   Stop time                    = {:s}".format(timstr))
    print(" ")
    #
    # Initialize the "confinement" window with the interval
    # over which we'll conduct the search.
    #
    cnfine = stypes.SPICEDOUBLE_CELL(2)
    spiceypy.wninsd(etbeg, etend, cnfine)
    #
    # In the call below, the maximum number of window
    # intervals gfposc can store internally is set to MAXIVL.
    # We set the cell size to MAXWIN to achieve this.
    #
    riswin = stypes.SPICEDOUBLE_CELL(MAXWIN)
    #
    # Now search for the time period, within our confinement
    # window, during which the apparent target has elevation
    # at least equal to the elevation limit.
    #
    spiceypy.gfposc(
        target,
        obsfrm,
        abcorr,
        srfpt,
        crdsys,
        coord,
        relate,
        revlim,
        adjust,
        stepsz,
        MAXIVL,
        cnfine,
        riswin,
    )
    #
    # The function wncard returns the number of intervals
    # in a SPICE window.
    #
    winsiz = spiceypy.wncard(riswin)
    if winsiz == 0:
        print("No events were found.")
    else:
        #
        # Display the visibility time periods.
        #
        print("Visibility times of {0:s} as seen from {1:s}:\n".format(target, srfpt))
        for i in range(winsiz):
            #
            # Fetch the start and stop times of
            # the ith interval from the search result
            # window riswin.
            #
            [intbeg, intend] = spiceypy.wnfetd(riswin, i)
            #
            # Convert the rise time to a TDB calendar string.
            #
            timstr = spiceypy.timout(intbeg, TDBFMT)
            #
            # Write the string to standard output.
            #
            if i == 0:
                print("Visibility or window start time:  {:s}".format(timstr))
            else:
                print("Visibility start time:            {:s}".format(timstr))
            #
            # Convert the set time to a TDB calendar string.
            #
            timstr = spiceypy.timout(intend, TDBFMT)
            #
            # Write the string to standard output.
            #
            if i == (winsiz - 1):
                print("Visibility or window stop time:   {:s}".format(timstr))
            else:
                print("Visibility stop time:             {:s}".format(timstr))
            print(" ")
    spiceypy.unload(METAKR)


if __name__ == "__main__":
    viewpr()
