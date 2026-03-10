mk = r"""
KPL/MK
\begindata
KERNELS_TO_LOAD = ( 'kernels/lsk/naif0008.tls',
                    'kernels/spk/de405s.bsp',
                    'kernels/pck/pck00008.tpc')
"""
with open("win.tm", "w") as dst:
    dst.write(mk)
print("Wrote kernel file win.tm")
print("")

#
# Import the CSPICE-Python interface.
#
import spiceypy


def win():
    MAXSIZ = 8

    #
    # Define a set of time intervals. For the purposes of this
    # tutorial program, define time intervals representing
    # an unobscured line of sight between a ground station
    # and some body.
    #
    los = [
        "Jan 1, 2003 22:15:02",
        "Jan 2, 2003  4:43:29",
        "Jan 4, 2003  9:55:30",
        "Jan 4, 2003 11:26:52",
        "Jan 5, 2003 11:09:17",
        "Jan 5, 2003 13:00:41",
        "Jan 6, 2003 00:08:13",
        "Jan 6, 2003  2:18:01",
    ]

    #
    # A second set of intervals representing the times for which
    # an acceptable phase angle exists between the ground station,
    # the body and the Sun.
    #
    phase = [
        "Jan 2, 2003 00:03:30",
        "Jan 2, 2003 19:00:00",
        "Jan 3, 2003  8:00:00",
        "Jan 3, 2003  9:50:00",
        "Jan 5, 2003 12:00:00",
        "Jan 5, 2003 12:45:00",
        "Jan 6, 2003 00:30:00",
        "Jan 6, 2003 23:00:00",
    ]

    #
    # Load our meta kernel for the leapseconds data.
    #
    spiceypy.furnsh("win.tm")

    #
    # SPICE windows consist of double precision values; convert
    # the string time tags defined in the 'los' and 'phase'
    # arrays to double precision ET. Store the double values
    # in the 'loswin' and 'phswin' windows.
    #
    los_et = spiceypy.str2et(los)
    phs_et = spiceypy.str2et(phase)

    loswin = spiceypy.stypes.SPICEDOUBLE_CELL(MAXSIZ)
    phswin = spiceypy.stypes.SPICEDOUBLE_CELL(MAXSIZ)

    for i in range(0, int(MAXSIZ / 2)):
        spiceypy.wninsd(los_et[2 * i], los_et[2 * i + 1], loswin)
        spiceypy.wninsd(phs_et[2 * i], phs_et[2 * i + 1], phswin)

    spiceypy.wnvald(MAXSIZ, MAXSIZ, loswin)
    spiceypy.wnvald(MAXSIZ, MAXSIZ, phswin)

    #
    # The issue for consideration, at what times do line of
    # sight events coincide with acceptable phase angles?
    # Perform the set operation AND on loswin, phswin,
    # (the intersection of the time intervals)
    # place the results in the window 'sched'.
    #
    sched = spiceypy.wnintd(loswin, phswin)

    print("Number data values in sched : {0:2d}".format(spiceypy.card(sched)))

    #
    # Output the results. The number of intervals in 'sched'
    # is half the number of data points (the cardinality).
    #
    print(" ")
    print("Time intervals meeting defined criterion.")

    for i in range(spiceypy.card(sched) // 2):
        #
        # Extract from the derived 'sched' the values defining the
        # time intervals.
        #
        [left, right] = spiceypy.wnfetd(sched, i)

        #
        # Convert the ET values to UTC for human comprehension.
        #
        utcstr_l = spiceypy.et2utc(left, "C", 3)
        utcstr_r = spiceypy.et2utc(right, "C", 3)
        #
        # Output the UTC string and the corresponding index
        # for the interval.
        #
        print("{0:2d}   {1}   {2}".format(i, utcstr_l, utcstr_r))
    #
    # Summarize the 'sched' window.
    #
    [meas, avg, stddev, small, large] = spiceypy.wnsumd(sched)
    print("\nSummary of sched window\n")
    print("o Total measure of sched    : {0:16.6f}".format(meas))
    print("o Average measure of sched  : {0:16.6f}".format(avg))
    print("o Standard deviation of ")
    print("  the measures in sched     : {0:16.6f}".format(stddev))
    #
    # The values for small and large refer to the indexes of the
    # values in the window ('sched'). The shortest interval is
    #
    #      [ sched.base[ sched.data + small]
    #        sched.base[ sched.data + small +1]  ];
    #
    # the longest is
    #
    #      [ sched.base[ sched.data + large]
    #        sched.base[ sched.data + large +1]  ];
    #
    # Output the interval indexes for the shortest and longest
    # intervals. As Python bases an array index on 0, the interval
    # index is half the array index.
    #
    print("o Index of shortest interval: {0:2d}".format(int(small / 2)))
    print("o Index of longest interval : {0:2d}".format(int(large / 2)))
    #
    # Done. Unload the kernels.
    #
    spiceypy.kclear()


if __name__ == "__main__":
    win()
