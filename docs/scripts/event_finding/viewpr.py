#
# Solution viewpr
#
import spiceypy

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
    print("\nInputs for target visibility search:\n")
    print(f"   Target                       = {target}")
    print(f"   Observation surface location = {srfpt}")
    print(f"   Observer's reference frame   = {obsfrm}")
    print(f"   Elevation limit (degrees)    = {elvlim}")
    print(f"   Aberration correction        = {abcorr}")
    print(f"   Step size (seconds)          = {stepsz}")
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
    print(f"   Start time                   = {timstr}")
    timstr = spiceypy.timout(etend, TDBFMT)
    print(f"   Stop time                    = {timstr}")
    print(" ")
    #
    # Initialize the "confinement" window with the interval
    # over which we'll conduct the search.
    #
    cnfine = spiceypy.cell_double(2)
    spiceypy.wninsd(etbeg, etend, cnfine)
    #
    # In the call below, the maximum number of window
    # intervals gfposc can store internally is set to MAXIVL.
    # We set the cell size to MAXWIN to achieve this.
    #
    riswin = spiceypy.cell_double(MAXWIN)
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
        print(f"Visibility times of {target} as seen from {srfpt}:\n")
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
                print(f"Visibility or window start time:  {timstr}")
            else:
                print(f"Visibility start time:            {timstr}")
            #
            # Convert the set time to a TDB calendar string.
            #
            timstr = spiceypy.timout(intend, TDBFMT)
            #
            # Write the string to standard output.
            #
            if i == (winsiz - 1):
                print(f"Visibility or window stop time:   {timstr}")
            else:
                print(f"Visibility stop time:             {timstr}")
            print(" ")
    
    spiceypy.unload(METAKR)


if __name__ == "__main__":
    viewpr()
