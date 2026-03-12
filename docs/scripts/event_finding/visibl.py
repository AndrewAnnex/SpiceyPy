#
# Solution visibl
#
import spiceypy

def visibl():
    #
    # Local Parameters
    #
    METAKR = 'visibl.tm'
    SCLKID = -82
    TDBFMT = 'YYYY MON DD HR:MN:SC.### TDB ::TDB'
    MAXIVL = 1000
    MAXWIN = 2 * MAXIVL
    #
    # Load the meta-kernel.
    #
    spiceypy.furnsh( METAKR )
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
    srfpt  = 'DSS-14'
    obsfrm = 'DSS-14_TOPO'
    target = 'MEX'
    abcorr = 'CN+S'
    start  = '2004 MAY 2 TDB'
    stop   = '2004 MAY 6 TDB'
    elvlim =  6.0
    #
    # The elevation limit above has units of degrees; we convert
    # this value to radians for computation using SPICE routines.
    # We'll store the equivalent value in radians in revlim.
    #
    revlim = spiceypy.rpd() * elvlim
    #
    # We model the target shape as a point. We either model the
    # blocking body's shape as an ellipsoid, or we represent
    # its shape using actual topographic data. No body-fixed
    # reference frame is required for the target since its
    # orientation is not used.
    #
    back   = target
    bshape = 'POINT'
    bframe = ' '
    front  = 'MARS'
    fshape = 'ELLIPSOID'
    fframe = 'IAU_MARS'
    #
    # The occultation type should be set to 'ANY' for a point
    # target.
    #
    occtyp = 'any'
    #
    # Since SPICE doesn't directly support the AZ/EL coordinate
    # system, we use the equivalent constraint
    #
    #    latitude > revlim
    #
    # in the latitudinal coordinate system, where the reference
    # frame is topocentric and is centered at the viewing location.
    #
    crdsys = 'LATITUDINAL'
    coord  = 'LATITUDE'
    relate = '>'
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
    print('\nInputs for target visibility search:\n')
    print(f'   Target                       = {target}')
    print(f'   Observation surface location = {srfpt}')
    print(f"   Observer's reference frame   = {obsfrm}")
    print(f'   Blocking body                = {front}')
    print(f"   Blocker's reference frame    = {fframe}")
    print(f'   Elevation limit (degrees)    = {elvlim:f}')
    print(f'   Aberration correction        = {abcorr}')
    print(f'   Step size (seconds)          = {stepsz:f}')
    #
    # Convert the start and stop times to ET.
    #
    etbeg = spiceypy.str2et( start )
    etend = spiceypy.str2et( stop  )
    #
    # Display the search interval start and stop times
    # using the format shown below.
    #
    #    2004 MAY 06 20:15:00.000 (TDB)
    #
    btmstr = spiceypy.timout( etbeg, TDBFMT )
    print(f'   Start time                   = {btmstr}')
    etmstr = spiceypy.timout(etend, TDBFMT)
    print(f'   Stop time                    = {etmstr}')

    print( ' ' )
    #
    # Initialize the "confinement" window with the interval
    # over which we'll conduct the search.
    #
    cnfine = spiceypy.spice_double(2)
    spiceypy.wninsd( etbeg, etend, cnfine )
    #
    # In the call below, the maximum number of window
    # intervals gfposc can store internally is set to MAXIVL.
    # We set the cell size to MAXWIN to achieve this.
    #
    riswin = spiceypy.spice_double( MAXWIN )
    #
    # Now search for the time period, within our confinement
    # window, during which the apparent target has elevation
    # at least equal to the elevation limit.
    #
    spiceypy.gfposc( target, obsfrm, abcorr, srfpt,
                     crdsys, coord,  relate, revlim,
                     adjust, stepsz, MAXIVL, cnfine, riswin )
    #
    # Now find the times when the apparent target is above
    # the elevation limit and is not occulted by the
    # blocking body (Mars). We'll find the window of times when
    # the target is above the elevation limit and *is* occulted,
    # then subtract that window from the view period window
    # riswin found above.
    #
    # For this occultation search, we can use riswin as
    # the confinement window because we're not interested in
    # occultations that occur when the target is below the
    # elevation limit.
    #
    # Find occultations within the view period window.
    #
    print( ' Searching using ellipsoid target shape model...' )
    eocwin = spiceypy.spice_double( MAXWIN )
    fshape = 'ELLIPSOID'
    spiceypy.gfoclt( occtyp, front,  fshape,  fframe,
                     back,   bshape, bframe,  abcorr,
                     srfpt,  stepsz, riswin,  eocwin )
    print( ' Done.' )
    #
    # Subtract the occultation window from the view period
    # window: this yields the time periods when the target
    # is visible.
    #
    evswin = spiceypy.wndifd( riswin, eocwin )
    #
    #  Repeat the search using low-resolution DSK data
    # for the front body.
    #
    print( ' Searching using DSK target shape model...' )
    docwin = spiceypy.spice_double( MAXWIN )
    fshape = 'DSK/UNPRIORITIZED'
    spiceypy.gfoclt( occtyp, front,  fshape,  fframe,
                     back,   bshape, bframe,  abcorr,
                     srfpt,  stepsz, riswin,  docwin )
    print( ' Done.\n' )
    dvswin = spiceypy.wndifd( riswin, docwin )
    #
    # The function wncard returns the number of intervals
    # in a SPICE window.
    #
    winsiz = spiceypy.wncard( evswin )
    if winsiz == 0:
        print( 'No events were found.' )
    else:
        #
        # Display the visibility time periods.
        #
        print(
            f'Visibility start and stop times of {target} as seen from {srfpt}\n'
            'using both ellipsoidal and DSK target shape models:\n'
        )
        for  i  in  range(winsiz):
            #
            # Fetch the start and stop times of
            # the ith interval from the ellipsoid
            # search result window evswin.
            #
            [intbeg, intend] = spiceypy.wnfetd( evswin, i )
            #
            # Convert the rise time to TDB calendar strings.
            # Write the results.
            #
            btmstr = spiceypy.timout( intbeg, TDBFMT )
            etmstr = spiceypy.timout( intend, TDBFMT )
            print(f' Ell: {btmstr} : {etmstr}')
            #
            # Fetch the start and stop times of
            # the ith interval from the DSK
            # search result window dvswin.
            #
            [dintbg, dinten] = spiceypy.wnfetd( dvswin, i )
            #
            # Convert the rise time to TDB calendar strings.
            # Write the results.
            #
            btmstr = spiceypy.timout( dintbg, TDBFMT )
            etmstr = spiceypy.timout( dinten, TDBFMT )
            print(f' DSK: {btmstr} : {etmstr}\n')
        #
        # End of result display loop.
        #
    spiceypy.unload( METAKR )
if __name__ == '__main__':
    visibl()