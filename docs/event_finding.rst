Geometric Event Finding Hands-On Lesson, using MEX
===================================================

November 20, 2017

Overview
--------

This lesson illustrates how the Geometry Finder (GF) subsystem of the
SpiceyPy Toolkit can be used to find time intervals when specified
geometric conditions are satisfied.

In this lesson the student is asked to construct a program that finds
the time intervals, within a specified time range, when the Mars Express
Orbiter (MEX) is visible from the DSN station DSS-14. Possible
occultation of the spacecraft by Mars is to be considered.

References
----------

This section lists SPICE documents referred to in this lesson.

In some cases the lesson explanations also refer to the information
provided in the meta-data area of the kernels used in the lesson
examples. It is especially true in case of the FK and IK files, which
often contain comprehensive descriptions of the frames, instrument FOVs,
etc. Since both FK and IK are text kernels, the information provided in
them can be viewed using any text editor, while the meta information
provided in binary kernels – SPKs and CKs – can be viewed using
"commnt" or" spacit" utility programs located in "cspice/exe" of
Toolkit installation tree.

The following SPICE tutorials serve as references for the discussions in
this lesson:

::

      Name              Lesson steps/functions it describes
      ----------------  -----------------------------------------------
      Time              Time Conversion
      SCLK and LSK      Time Conversion
      SPK               Obtaining Ephemeris Data
      Frames            Reference Frames
      Using Frames      Reference Frames
      PCK               Planetary Constants Data
      Lunar-Earth PCK   Lunar and Earth Orientation Data
      GF                The SPICE Geometry Finder (GF) subsystem

These tutorials are available from the NAIF ftp server at JPL:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

      https://naif.jpl.nasa.gov/naif/tutorials.html

Required Readings
^^^^^^^^^^^^^^^^^^

.. tip::
   The `Required Readings <https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/index.html>`_ are also available on the NAIF website at:
      https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/index.html.

The Required Reading documents are provided with the Toolkit and are
located under the "cspice/doc" directory in the CSPICE Toolkit
installation tree.

::

      Name             Lesson steps/functions that it describes
      ---------------  -----------------------------------------
      cells.req        Cell/window initialization
      frames.req       Using reference frames
      gf.req           The SPICE geometry finder (GF) subsystem
      kernel.req       Loading SPICE kernels
      naif_ids.req     Body and reference frame names
      pck.req          Obtaining planetary constants data
      spk.req          Computing positions and velocities
      time.req         UTC to ET time conversion
      windows.req      The SPICE window data type

The Permuted Index
^^^^^^^^^^^^^^^^^^^

.. tip::
   The `Permuted Index <https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/info/cspice_idx.html>`_ is also available on the NAIF website at:
      https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/info/cspice_idx.html.

Another useful document distributed with the Toolkit is the permuted
index. This is located under the "cspice/doc" directory in the C
installation tree.

This text document provides a simple mechanism by which users can
discover which SpiceyPy functions perform functions of interest, as well
as the names of the source files that contain these functions.

SpiceyPy API Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^

A SpiceyPy function's parameters specification is available using the
built-in Python help system.

For example, the Python help function

::

      >>> import spiceypy
      >>> help(spiceypy.str2et)

describes of the str2et function's parameters, while the document

::

      https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/str2et_c.html

describes extensively the str2et functionality.

Kernels Used
------------

The following kernels are used in examples provided in this lesson:

::

      #  FILE NAME                      TYPE DESCRIPTION
      -- ------------------------------ ---- ------------------------------
      1  de405xs.bsp                    SPK  Planetary ephemeris SPK,
                                             subsetted to cover only time
                                             range of interest
      2  earthstns_itrf93_050714.bsp    SPK  DSN station SPK
      3  earth_topo_050714.tf           FK   DSN station frame definitions
      4  earth_000101_060525_060303.bpc PCK  Binary PCK for Earth
      5  naif0008.tls                   LSK  Generic LSK
      6  ORMM__040501000000_00076XS.BSP SPK  MEX Orbiter trajectory SPK,
                                             subsetted to cover only time
                                             range of interest
      7  pck00008.tpc                   PCK  Generic PCK
      8  mars_lowres.bds                DSK  Low-resolution Mars DSK

These SPICE kernels are included in the lesson package available from
the NAIF server at JPL:

::

      https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/Lessons/

SpiceyPy Modules Used
---------------------

This section provides a complete list of the functions and kernels that
are suggested for usage in each of the exercises in this lesson. (You
may wish to not look at this list unless/until you "get stuck" while
working on your own.)

::

      CHAPTER EXERCISE   FUNCTIONS        NON-VOID         KERNELS
      ------- ---------  ---------------  ---------------  ----------
         1    viewpr     spiceypy.furnsh  spiceypy.rpd     1-7
                         spiceypy.wninsd  spiceypy.str2et
                         spiceypy.gfposc  spiceypy.timout
                         spiceypy.unload  spiceypy.wncard
                                          spiceypy.wnfetd

         2    visibl     spiceypy.furnsh  spiceypy.rpd     1-8
                         spiceypy.wninsd  spiceypy.str2et
                         spiceypy.gfposc  spiceypy.timout
                         spiceypy.gfoclt  spiceypy.wndifd
                         spiceypy.unload  spiceypy.wncard
                                          spiceypy.wnfetd

              extra (*)  spiceypy.gfdist  spiceypy.repmc   1,5-7
                         spiceypy.kclear  spiceypy.repmf


         (*) Additional APIs and kernels used in Extra Credit tasks.

Use the Python built-in help system on the various functions listed
above for the API parameters' description, and refer to the headers of
their corresponding CSPICE versions for detailed interface
specifications.

Find View Periods
------------------------------

Task Statement
^^^^^^^^^^^^^^

Write a program that finds the set of time intervals, within the time
range

::

      2004 MAY 2 TDB
      2004 MAY 6 TDB

when the Mars Express Orbiter (MEX) is visible from the DSN station
DSS-14. These time intervals are frequently called "view periods."

The spacecraft is considered visible if its apparent position (that is,
its position corrected for light time and stellar aberration) has
elevation of at least 6 degrees in the topocentric reference frame
DSS-14_TOPO. In this exercise, we ignore the possibility of occultation
of the spacecraft by Mars.

Use a search step size that ensures that no view periods of duration 5
minutes or longer will be missed by the search.

Display the start and stop times of these intervals using TDB calendar
dates and millisecond precision.

Learning Goals
^^^^^^^^^^^^^^

Exposure to SPICE GF event finding routines. Familiarity with SPICE
windows and routines that manipulate them. Exposure to SPICE time
parsing and output formatting routines.

Approach
^^^^^^^^

Solution steps

A possible solution could consist of the following steps:

Preparation:

::

       1.   Decide what SPICE kernels are necessary. Use the SPICE summary
            tool BRIEF to examine the coverage of the binary kernels and
            verify the availability of required data.

       2.   Create a meta-kernel listing the SPICE kernels to be loaded.
            (Hint: consult a programming example tutorial, or the
            Introduction to Kernels tutorial, for a reminder of how to do
            this.)

            Name the meta-kernel 'viewpr.tm'.

Next, write a program that performs the following steps:

::

       1.   Use spiceypy.furnsh to load the meta-kernel.

       2.   Create confinement and output SpiceyPy windows using
            stypes.SPICEDOUBLE_CELL.

       3.   Insert the given time bounds into the confinement window using
            spiceypy.wninsd.

       4.   Select a step size for searching for visibility state
            transitions: in this case, each target rise or set event is a
            state transition.

            The step size must be large enough so the search proceeds with
            reasonable speed, but small enough so that no visibility
            transition events---that is, target rise or set events---are
            missed.

       5.   Use the GF routine spiceypy.gfposc to find the window of times,
            within the confinement window, during which the MEX spacecraft
            is above the elevation limit as seen from DSN station DSS-14,
            in the reference frame DSS-14_TOPO.

            Use light time and stellar aberration corrections for the
            apparent position of the spacecraft as seen from the station.

       6.   Fetch and display the contents of the result window. Use
            spiceypy.wnfetd to extract from the result window the start and
            stop times of each time interval. Display each of the intervals
            in the result window as a pair of start and stop times. Express
            each time as a TDB calendar date using the routine
            spiceypy.timout.

You may find it useful to consult the references listed above. In
particular, the header of the SPICE GF function spiceypy.gfposc contains
pertinent documentation.

Solution
^^^^^^^^

Solution Meta-Kernel

The meta-kernel we created for the solution to this exercise is named
'viewpr.tm'. Its contents follow:

::

      KPL/MK

         Example meta-kernel for geometric event finding hands-on
         coding lesson.

            Version 2.0.0 13-JUL-2017 (JDR)

         The names and contents of the kernels referenced by this
         meta-kernel are as follows:

         File Name                       Description
         ------------------------------  ------------------------------
         de405xs.bsp                     Planetary ephemeris SPK,
                                         subsetted to cover only
                                         time range of interest.
         earthstns_itrf93_050714.bsp     DSN station SPK.
         earth_topo_050714.tf            DSN station frame definitions.
         earth_000101_060525_060303.bpc  Binary PCK for Earth.
         naif0008.tls                    Generic LSK.
         ORMM__040501000000_00076XS.BSP  MEX Orbiter trajectory SPK,
                                         subsetted to cover only
                                         time range of interest.
         pck00008.tpc                    Generic PCK.


      \begindata

         KERNELS_TO_LOAD = (

                 'kernels/spk/de405xs.bsp'
                 'kernels/spk/earthstns_itrf93_050714.bsp'
                 'kernels/fk/earth_topo_050714.tf'
                 'kernels/pck/earth_000101_060525_060303.bpc'
                 'kernels/lsk/naif0008.tls'
                 'kernels/spk/ORMM__040501000000_00076XS.BSP'
                 'kernels/pck/pck00008.tpc'
                           )

      \begintext

Solution Code

The example program below shows one possible solution.

::

      #
      # Solution viewpr
      #
      from __future__ import print_function
      import spiceypy.utils.support_types as stypes
      import spiceypy

      def viewpr():
          #
          # Local Parameters
          #
          METAKR = 'viewpr.tm'
          TDBFMT = 'YYYY MON DD HR:MN:SC.### (TDB) ::TDB'
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
          print( '\n{:s}\n'.format(
                 'Inputs for target visibility search:' )  )

          print( '   Target                       = '
                 '{:s}'.format( target )  )
          print( '   Observation surface location = '
                 '{:s}'.format( srfpt  )  )
          print( '   Observer\'s reference frame   = '
                 '{:s}'.format( obsfrm )  )
          print( '   Elevation limit (degrees)    = '
                 '{:f}'.format( elvlim )  )
          print( '   Aberration correction        = '
                 '{:s}'.format( abcorr )  )
          print( '   Step size (seconds)          = '
                 '{:f}'.format( stepsz )  )

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
          timstr = spiceypy.timout( etbeg, TDBFMT )
          print( '   Start time                   = '
                 '{:s}'.format(timstr) )

          timstr = spiceypy.timout( etend, TDBFMT )
          print( '   Stop time                    = '
                 '{:s}'.format(timstr) )

          print( ' ' )

          #
          # Initialize the "confinement" window with the interval
          # over which we'll conduct the search.
          #
          cnfine = stypes.SPICEDOUBLE_CELL(2)
          spiceypy.wninsd( etbeg, etend, cnfine )

          #
          # In the call below, the maximum number of window
          # intervals gfposc can store internally is set to MAXIVL.
          # We set the cell size to MAXWIN to achieve this.
          #
          riswin = stypes.SPICEDOUBLE_CELL( MAXWIN )

          #
          # Now search for the time period, within our confinement
          # window, during which the apparent target has elevation
          # at least equal to the elevation limit.
          #
          spiceypy.gfposc( target, obsfrm, abcorr, srfpt,
                           crdsys, coord,  relate, revlim,
                           adjust, stepsz, MAXIVL, cnfine, riswin )

          #
          # The function wncard returns the number of intervals
          # in a SPICE window.
          #
          winsiz = spiceypy.wncard( riswin )

          if winsiz == 0:

              print( 'No events were found.' )

          else:

              #
              # Display the visibility time periods.
              #
              print( 'Visibility times of {0:s} '
                     'as seen from {1:s}:\n'.format(
                      target, srfpt )                )

              for  i  in  range(winsiz):
                  #
                  # Fetch the start and stop times of
                  # the ith interval from the search result
                  # window riswin.
                  #
                  [intbeg, intend] = spiceypy.wnfetd( riswin, i )

                  #
                  # Convert the rise time to a TDB calendar string.
                  #
                  timstr = spiceypy.timout( intbeg, TDBFMT )

                  #
                  # Write the string to standard output.
                  #
                  if  i  ==  0:

                      print( 'Visibility or window start time:'
                             '  {:s}'.format( timstr )          )
                  else:

                      print( 'Visibility start time:          '
                             '  {:s}'.format( timstr )          )

                  #
                  # Convert the set time to a TDB calendar string.
                  #
                  timstr = spiceypy.timout( intend, TDBFMT )

                  #
                  # Write the string to standard output.
                  #
                  if  i  ==  (winsiz-1):

                      print( 'Visibility or window stop time: '
                             '  {:s}'.format( timstr )          )
                  else:

                      print( 'Visibility stop time:           '
                             '  {:s}'.format( timstr )          )

                  print( ' ' )

          spiceypy.unload( METAKR )

      if __name__ == '__main__':
          viewpr()

Solution Sample Output

Numerical results shown for this example may differ across platforms
since the results depend on the SPICE kernels used as input and on the
host platform's arithmetic implementation.

Execute the program. The output is:

::

      Inputs for target visibility search:

         Target                       = MEX
         Observation surface location = DSS-14
         Observer's reference frame   = DSS-14_TOPO
         Elevation limit (degrees)    = 6.000000
         Aberration correction        = CN+S
         Step size (seconds)          = 300.000000
         Start time                   = 2004 MAY 02 00:00:00.000 (TDB)
         Stop time                    = 2004 MAY 06 00:00:00.000 (TDB)

      Visibility times of MEX as seen from DSS-14:

      Visibility or window start time:  2004 MAY 02 00:00:00.000 (TDB)
      Visibility stop time:             2004 MAY 02 05:35:03.096 (TDB)

      Visibility start time:            2004 MAY 02 16:09:14.078 (TDB)
      Visibility stop time:             2004 MAY 03 05:33:57.257 (TDB)

      Visibility start time:            2004 MAY 03 16:08:02.279 (TDB)
      Visibility stop time:             2004 MAY 04 05:32:50.765 (TDB)

      Visibility start time:            2004 MAY 04 16:06:51.259 (TDB)
      Visibility stop time:             2004 MAY 05 05:31:43.600 (TDB)

      Visibility start time:            2004 MAY 05 16:05:40.994 (TDB)
      Visibility or window stop time:   2004 MAY 06 00:00:00.000 (TDB)

Find Times when Target is Visible
----------------------------------

.. _task-statement-ef-1:

Task Statement
^^^^^^^^^^^^^^

Extend the program of the previous chapter to find times when the MEX
orbiter is:

::

       --   Above the elevation limit in the DSS-14_TOPO topocentric
            reference frame.

       --   and is not occulted by Mars

Finding time intervals that satisfy the second condition requires a
search for occultations of the spacecraft by Mars. Perform this search
twice: once using an ellipsoidal shape model for Mars, and once using a
DSK shape model.

Compute the final results twice as well, using the results of both
occultation searches.

For each of the two shape model cases, store the set of time intervals
when the spacecraft is visible in a SpiceyPy window. We'll call this the
"result window."

Display each of the intervals in each result window as a pair of start
and stop times. Express each time as a TDB calendar date using the same
format as in the previous program.

.. _learning-goals-ef-1:

Learning Goals
^^^^^^^^^^^^^^

Familiarity with the GF occultation finding routine spiceypy.gfoclt.
Experience with Digital Shape Kernel (DSK) shape models. Further
experience with the SpiceyPy window functions.

.. _approach-ef-1:

Approach
^^^^^^^^

Solution steps

A possible solution would consist of the following steps:

::

       1.   Use the meta-kernel from the previous chapter as the starting
            point. Add more kernels to it as needed.

            Name the meta-kernel 'visibl.tm'.

       2.   Include the code from the program of the previous chapter in a
            new source file; modify this code to create the new program.

       3.   Your program will need additional windows to capture the
            results of occultation searches performed using both
            ellipsoidal and DSK shape models. Additional windows will be
            needed to compute the set differences of the elevation search
            ("view period") window and each of the occultation search
            windows. Further details are provided below.

            Create additional output SpiceyPy windows using
            stypes.SPICEDOUBLE_CELL.

       4.   The remaining steps can be performed twice: once using an
            ellipsoidal shape model for Mars, and once using a DSK Mars
            shape model. Alternatively, two copies of the entire solution
            program can be created: one for each shape model.

       5.   Search for occultations of the MEX orbiter as seen from DSS-14
            using spiceypy.gfoclt. Use as the confinement window for this
            search the result window from the elevation search performed by
            spiceypy.gfposc.

            Since occultations occur when the apparent MEX spacecraft
            position is behind the apparent figure of Mars, light time
            correction must be performed for the occultation search. To
            improve accuracy of the occultation state determination, use
            "converged Newtonian" light time correction.

       6.   Use the SpiceyPy window subtraction routine spiceypy.wndifd to
            subtract the window of times when the spacecraft is occulted
            from the window of times when the spacecraft is above the
            elevation limit. The difference window is the final result.

       7.   Modify the code to display the contents of the difference
            window.

This completes the assignment.

.. _solution-ef-1:

Solution
^^^^^^^^

Solution Meta-Kernel

The meta-kernel we created for the solution to this exercise is named
'visibl.tm'. Its contents follow:

::

      KPL/MK

         Example meta-kernel for geometric event finding hands-on
         coding lesson.

            Version 3.0.0 26-OCT-2017 (BVS)

         The names and contents of the kernels referenced by this
         meta-kernel are as follows:

         File Name                       Description
         ------------------------------  ------------------------------
         de405xs.bsp                     Planetary ephemeris SPK,
                                         subsetted to cover only
                                         time range of interest.
         earthstns_itrf93_050714.bsp     DSN station SPK.
         earth_topo_050714.tf            DSN station frame definitions.
         earth_000101_060525_060303.bpc  Binary PCK for Earth.
         naif0008.tls                    Generic LSK.
         ORMM__040501000000_00076XS.BSP  MEX Orbiter trajectory SPK,
                                         subsetted to cover only
                                         time range of interest.
         pck00008.tpc                    Generic PCK.
         mars_lowres.bds                 Low-resolution Mars DSK.


      \begindata

         KERNELS_TO_LOAD = (

                 'kernels/spk/de405xs.bsp'
                 'kernels/spk/earthstns_itrf93_050714.bsp'
                 'kernels/fk/earth_topo_050714.tf'
                 'kernels/pck/earth_000101_060525_060303.bpc'
                 'kernels/lsk/naif0008.tls'
                 'kernels/spk/ORMM__040501000000_00076XS.BSP'
                 'kernels/pck/pck00008.tpc'
                 'kernels/dsk/mars_lowres.bds'
                           )

      \begintext

Solution Code

::

      #
      # Solution visibl
      #
      from __future__ import print_function

      #
      # SpiceyPy package:
      #
      import spiceypy.utils.support_types as stypes
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
          print( '\n{:s}\n'.format(
                 'Inputs for target visibility search:' )  )

          print( '   Target                       = '
                 '{:s}'.format( target )  )
          print( '   Observation surface location = '
                 '{:s}'.format( srfpt  )  )
          print( '   Observer\'s reference frame   = '
                 '{:s}'.format( obsfrm )  )
          print( '   Blocking body                = '
                 '{:s}'.format( front  )  )
          print( '   Blocker\'s reference frame    = '
                 '{:s}'.format( fframe )  )
          print( '   Elevation limit (degrees)    = '
                 '{:f}'.format( elvlim )  )
          print( '   Aberration correction        = '
                 '{:s}'.format( abcorr )  )
          print( '   Step size (seconds)          = '
                 '{:f}'.format( stepsz )  )

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
          print( '   Start time                   = '
                 '{:s}'.format(btmstr) )

          etmstr = spiceypy.timout( etend, TDBFMT )
          print( '   Stop time                    = '
                 '{:s}'.format(etmstr) )

          print( ' ' )

          #
          # Initialize the "confinement" window with the interval
          # over which we'll conduct the search.
          #
          cnfine = stypes.SPICEDOUBLE_CELL(2)
          spiceypy.wninsd( etbeg, etend, cnfine )

          #
          # In the call below, the maximum number of window
          # intervals gfposc can store internally is set to MAXIVL.
          # We set the cell size to MAXWIN to achieve this.
          #
          riswin = stypes.SPICEDOUBLE_CELL( MAXWIN )

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

          eocwin = stypes.SPICEDOUBLE_CELL( MAXWIN )

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

          docwin = stypes.SPICEDOUBLE_CELL( MAXWIN )

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
              print( 'Visibility start and stop times of '
                     '{0:s} as seen from {1:s}\n'
                     'using both ellipsoidal and DSK '
                     'target shape models:\n'.format(
                         target, srfpt )                 )

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

                  print( ' Ell: {:s} : {:s}'.format( btmstr, etmstr ) )

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

                  print( ' DSK: {:s} : {:s}\n'.format( btmstr, etmstr ) )
              #
              # End of result display loop.
              #

          spiceypy.unload( METAKR )

      if __name__ == '__main__':
          visibl()

Solution Sample Output

Numerical results shown for this example may differ across platforms
since the results depend on the SPICE kernels used as input and on the
host platform's arithmetic implementation.

Execute the program. The output is:

::

      Inputs for target visibility search:

         Target                       = MEX
         Observation surface location = DSS-14
         Observer's reference frame   = DSS-14_TOPO
         Blocking body                = MARS
         Blocker's reference frame    = IAU_MARS
         Elevation limit (degrees)    = 6.000000
         Aberration correction        = CN+S
         Step size (seconds)          = 300.000000
         Start time                   = 2004 MAY 02 00:00:00.000 TDB
         Stop time                    = 2004 MAY 06 00:00:00.000 TDB

       Searching using ellipsoid target shape model...
       Done.
       Searching using DSK target shape model...
       Done.

      Visibility start and stop times of MEX as seen from DSS-14
      using both ellipsoidal and DSK target shape models:

       Ell: 2004 MAY 02 00:00:00.000 TDB : 2004 MAY 02 04:49:30.827 TDB
       DSK: 2004 MAY 02 00:00:00.000 TDB : 2004 MAY 02 04:49:32.645 TDB

       Ell: 2004 MAY 02 16:09:14.078 TDB : 2004 MAY 02 20:00:22.514 TDB
       DSK: 2004 MAY 02 16:09:14.078 TDB : 2004 MAY 02 20:00:23.980 TDB

       Ell: 2004 MAY 02 21:01:38.222 TDB : 2004 MAY 03 03:35:42.256 TDB
       DSK: 2004 MAY 02 21:01:43.195 TDB : 2004 MAY 03 03:35:44.140 TDB

       Ell: 2004 MAY 03 04:36:42.484 TDB : 2004 MAY 03 05:33:57.257 TDB
       DSK: 2004 MAY 03 04:36:46.856 TDB : 2004 MAY 03 05:33:57.257 TDB

       Ell: 2004 MAY 03 16:08:02.279 TDB : 2004 MAY 03 18:46:26.013 TDB
       DSK: 2004 MAY 03 16:08:02.279 TDB : 2004 MAY 03 18:46:27.306 TDB

       Ell: 2004 MAY 03 19:46:54.618 TDB : 2004 MAY 04 02:21:44.562 TDB
       DSK: 2004 MAY 03 19:46:59.723 TDB : 2004 MAY 04 02:21:46.574 TDB

       Ell: 2004 MAY 04 03:21:56.347 TDB : 2004 MAY 04 05:32:50.765 TDB
       DSK: 2004 MAY 04 03:22:00.850 TDB : 2004 MAY 04 05:32:50.765 TDB

       Ell: 2004 MAY 04 16:06:51.259 TDB : 2004 MAY 04 17:32:25.809 TDB
       DSK: 2004 MAY 04 16:06:51.259 TDB : 2004 MAY 04 17:32:27.118 TDB

       Ell: 2004 MAY 04 18:32:05.975 TDB : 2004 MAY 05 01:07:48.264 TDB
       DSK: 2004 MAY 04 18:32:11.046 TDB : 2004 MAY 05 01:07:50.061 TDB

       Ell: 2004 MAY 05 02:07:11.601 TDB : 2004 MAY 05 05:31:43.600 TDB
       DSK: 2004 MAY 05 02:07:16.241 TDB : 2004 MAY 05 05:31:43.600 TDB

       Ell: 2004 MAY 05 16:05:40.994 TDB : 2004 MAY 05 16:18:35.560 TDB
       DSK: 2004 MAY 05 16:05:40.994 TDB : 2004 MAY 05 16:18:36.994 TDB

       Ell: 2004 MAY 05 17:17:27.717 TDB : 2004 MAY 05 23:54:04.672 TDB
       DSK: 2004 MAY 05 17:17:32.375 TDB : 2004 MAY 05 23:54:06.221 TDB

Extra Credit
------------------------------

In this "extra credit" section you will be presented with more
complex tasks, aimed at improving your understanding of the geometry
event finding subsystem and particularly the spiceypy.gfposc and
spiceypy.gfdist functions.

These "extra credit" tasks are provided as task statements, and
unlike the regular tasks, no approach or solution source code is
provided. In the next section, you will find the numeric solutions to
the questions asked in these tasks.

Task statements
^^^^^^^^^^^^^^^

::

       1.   Write a program that finds the times, within the time range

            2004 MAY 2 TDB
            2004 MAY 6 TDB

            when the MEX spacecraft crosses Mars' equator. Display the
            results using TDB calendar dates and millisecond precision.

       2.   Write a program that finds the times, within the time range

            2004 MAY 2 TDB
            2004 MAY 6 TDB

            when the MEX spacecraft is at periapsis. Display the results
            using TDB calendar dates and millisecond precision.

       3.   Write a program that finds the times, within the time range

            2004 MAY 2 TDB
            2004 MAY 6 TDB

            when the MEX spacecraft is at apoapsis. Display the results
            using TDB calendar dates and millisecond precision.

Solutions
^^^^^^^^^

::

       1.   Solution for the equator crossing search, using spiceypy.gfposc
            for the MEX spacecraft latitude in the Mars body-fixed frame
            equal to 0 degrees:


      Inputs for equator crossing search:

         Target                       = MEX
         Observer                     = MARS
         Observer's reference frame   = IAU_MARS
         Latitude limit (degrees)     = 0.000000
         Aberration correction        = NONE
         Step size (seconds)          = 300.000000
         Start time                   = 2004 MAY 02 00:00:00.000 (TDB)
         Stop time                    = 2004 MAY 06 00:00:00.000 (TDB)

      MEX MARS equator crossing times:

       Equator crossing or start time:  2004 MAY 02 05:00:08.334 (TDB)
       Equator crossing time:           2004 MAY 02 06:15:13.074 (TDB)
       Equator crossing time:           2004 MAY 02 12:35:14.856 (TDB)
       Equator crossing time:           2004 MAY 02 13:50:09.161 (TDB)
       Equator crossing time:           2004 MAY 02 20:10:24.439 (TDB)
       Equator crossing time:           2004 MAY 02 21:25:10.344 (TDB)
       Equator crossing time:           2004 MAY 03 03:45:26.758 (TDB)
       Equator crossing time:           2004 MAY 03 05:00:04.086 (TDB)
       Equator crossing time:           2004 MAY 03 11:20:32.419 (TDB)
       Equator crossing time:           2004 MAY 03 12:34:57.968 (TDB)
       Equator crossing time:           2004 MAY 03 18:55:34.883 (TDB)
       Equator crossing time:           2004 MAY 03 20:09:53.063 (TDB)
       Equator crossing time:           2004 MAY 04 02:30:35.509 (TDB)
       Equator crossing time:           2004 MAY 04 03:44:42.753 (TDB)
       Equator crossing time:           2004 MAY 04 10:05:41.638 (TDB)
       Equator crossing time:           2004 MAY 04 11:19:38.397 (TDB)
       Equator crossing time:           2004 MAY 04 17:40:41.405 (TDB)
       Equator crossing time:           2004 MAY 04 18:54:31.413 (TDB)
       Equator crossing time:           2004 MAY 05 01:15:45.967 (TDB)
       Equator crossing time:           2004 MAY 05 02:29:25.294 (TDB)
       Equator crossing time:           2004 MAY 05 08:50:53.931 (TDB)
       Equator crossing time:           2004 MAY 05 10:04:26.915 (TDB)
       Equator crossing time:           2004 MAY 05 16:25:58.350 (TDB)
       Equator crossing or stop time:   2004 MAY 05 17:39:23.889 (TDB)

       2.   Solution for the periapsis search, using spiceypy.gfdist for
            the MEX spacecraft distance from Mars at a local minimum:


      Inputs for periapsis search:

         Target                       = MEX
         Observer                     = MARS
         Aberration correction        = NONE
         Step size (seconds)          = 300.000000
         Start time                   = 2004 MAY 02 00:00:00.000 (TDB)
         Stop time                    = 2004 MAY 06 00:00:00.000 (TDB)

      MEX periapsis times:

       Periapsis or start time:         2004 MAY 02 05:57:51.000 (TDB)
       Periapsis time:                  2004 MAY 02 13:32:43.325 (TDB)
       Periapsis time:                  2004 MAY 02 21:07:41.124 (TDB)
       Periapsis time:                  2004 MAY 03 04:42:30.648 (TDB)
       Periapsis time:                  2004 MAY 03 12:17:21.143 (TDB)
       Periapsis time:                  2004 MAY 03 19:52:12.267 (TDB)
       Periapsis time:                  2004 MAY 04 03:26:57.755 (TDB)
       Periapsis time:                  2004 MAY 04 11:01:49.826 (TDB)
       Periapsis time:                  2004 MAY 04 18:36:38.448 (TDB)
       Periapsis time:                  2004 MAY 05 02:11:28.558 (TDB)
       Periapsis time:                  2004 MAY 05 09:46:26.309 (TDB)
       Periapsis or end time:           2004 MAY 05 17:21:18.875 (TDB)

       3.   Solution for the apoapsis search, using spiceypy.gfdist for the
            MEX spacecraft distance from Mars at a local maximum:


      Inputs for apoapsis search:

         Target                       = MEX
         Observer                     = MARS
         Aberration correction        = NONE
         Step size (seconds)          = 300.000000
         Start time                   = 2004 MAY 02 00:00:00.000 (TDB)
         Stop time                    = 2004 MAY 06 00:00:00.000 (TDB)

      MEX apoapsis times:

       Apoapsis or start time:          2004 MAY 02 02:10:24.948 (TDB)
       Apoapsis time:                   2004 MAY 02 09:45:19.189 (TDB)
       Apoapsis time:                   2004 MAY 02 17:20:14.194 (TDB)
       Apoapsis time:                   2004 MAY 03 00:55:07.633 (TDB)
       Apoapsis time:                   2004 MAY 03 08:29:57.890 (TDB)
       Apoapsis time:                   2004 MAY 03 16:04:48.524 (TDB)
       Apoapsis time:                   2004 MAY 03 23:39:36.745 (TDB)
       Apoapsis time:                   2004 MAY 04 07:14:25.662 (TDB)
       Apoapsis time:                   2004 MAY 04 14:49:15.904 (TDB)
       Apoapsis time:                   2004 MAY 04 22:24:05.351 (TDB)
       Apoapsis time:                   2004 MAY 05 05:58:59.270 (TDB)
       Apoapsis time:                   2004 MAY 05 13:33:54.433 (TDB)
       Apoapsis or stop time:           2004 MAY 05 21:08:50.211 (TDB)
