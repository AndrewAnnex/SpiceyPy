Binary PCK Hands-On Lesson
===========================

November 20, 2017

Overview
--------

In this lesson you will develop two programs that demonstrate geometric
computations using "high-accuracy" Earth and Moon binary PCKs. The
programs also demonstrate use of frame kernels and SPK files normally
used together with these high-accuracy PCKs.

References
----------

This section lists SPICE documents referred to in this lesson.

The following SPICE tutorials serve as references for the discussions in
this lesson:

.. code-block:: text

      Name              Lesson steps/functions it describes
      ----------------  -----------------------------------------------
      Frames            Moon rotation, Earth rotation
      PCK               Moon rotation, Earth rotation
      "High Accuracy
      Orientation and
      Body-Fixed
      frames for Moon
      and Earth"
      (backup)          Moon rotation, Earth rotation

These tutorials are available from the NAIF ftp server at JPL:

::

      https://naif.jpl.nasa.gov/naif/tutorials.html

Required Readings

.. tip::
   The `Required Readings <https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/index.html>`_ are also available on the NAIF website at:
      https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/index.html.

The Required Reading documents are provided with the Toolkit and are
located under the "cspice/doc" directory in the CSPICE Toolkit
installation tree.

.. code-block:: text

      Name             Lesson steps/functions that it describes
      ---------------  -----------------------------------------
      frames.req       Using reference frames
      pck.req          Obtaining planetary constants data
      spk.req          Obtaining ephemeris data
      time.req         Time conversion

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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

.. code-block:: text

      #  FILE NAME                      TYPE DESCRIPTION
      -- ------------------------------ ---- ------------------------------
      1  naif0008.tls                   LSK  Generic LSK
      2  de414_2000_2020.bsp            SPK  Solar System Ephemeris
      3  moon_060721.tf                 FK   Lunar FK
      4  pck00008.tpc                   PCK  NAIF text PCK
      5  moon_pa_de403_1950-2198.bpc    PCK  Moon binary PCK
      6  earthstns_itrf93_050714.bsp    SPK  DSN station Ephemeris
      7  earth_topo_050714.tf           FK   Earth topocentric FK
      8  earth_000101_070725_070503.bpc PCK  Earth binary PCK

These SPICE kernels are included in the lesson package available from
the NAIF server at JPL:

::

      ftp://naif.jpl.nasa.gov/pub/naif/toolkit_docs/Lessons/

SpiceyPy Modules Used
---------------------

This section provides a complete list of the functions and kernels that
are suggested for usage in each of the exercises in this lesson. (You
may wish to not look at this list unless/until you "get stuck" while
working on your own.)

.. code-block:: text

      CHAPTER EXERCISE   FUNCTIONS        NON-VOID         KERNELS
      ------- ---------  ---------------  ---------------  ----------
         1    mrotat     spiceypy.furnsh  spiceypy.str2et  1-5
                         spiceypy.unload  spiceypy.spkpos
                                          spiceypy.reclat
                                          spiceypy.dpr
                                          spiceypy.vsep
                                          spiceypy.subpnt
                                          spiceypy.vdist

         2    erotat     spiceypy.furnsh  spiceypy.str2et  1-2,4,6-8
                         spiceypy.unload  spiceypy.spkpos
                                          spiceypy.reclat
                                          spiceypy.dpr
                                          spiceypy.vsep
                                          spiceypy.spd
                                          spiceypy.timout
                                          spiceypy.pxform
                                          spiceypy.twopi
                                          spiceypy.subslr
                                          spiceypy.vdist

Use the Python built-in help system on the various functions listed
above for the API parameters' description, and refer to the headers of
their corresponding CSPICE versions for detailed interface
specifications.

Moon rotation (mrotat)
------------------------------

Task Statement
^^^^^^^^^^^^^^

Write a program that performs the following computations:

.. code-block:: text

       1.   Convert the time string 2007 JAN 1 00:00:00 UTC to a double
            precision number representing seconds past J2000 TDB.

            In the following instructions, we'll call the result of this
            computation ET.

       2.   Compute the apparent position of the Earth as seen from the
            Moon in the IAU_MOON reference frame at the epoch ET. Use light
            time and stellar aberration corrections. Use spiceypy.reclat to
            compute the planetocentric longitude and latitude of the Earth
            position vector; display these coordinates in degrees.

       3.   Repeat the computation of step 2 using the MOON_ME reference
            frame. Display the results as above.

       4.   Compute the angular separation of the position vectors found in
            steps 2 and 3. Display the result in degrees.

       5.   Repeat the computation of step 2 using the MOON_PA reference
            frame. Display the results as above.

       6.   Compute the angular separation of the position vectors found in
            steps 3 and 5 (these vectors are expressed in the MOON_ME and
            MOON_PA frames). Display the result in degrees.

       7.   Compute the apparent sub-Earth point on the Moon at ET,
            expressed in the MOON_ME reference frame and using light time
            and stellar aberration corrections. Convert the sub-Earth point
            to latitudinal coordinates using spiceypy.reclat. Display the
            longitude and latitude of the sub-Earth point in degrees.

       8.   Repeat step 7, now using the MOON_PA frame.

       9.   Compute the distance between the two sub-Earth points found
            above in steps 7 and 8. Display the result in kilometers.

Learning Goals
^^^^^^^^^^^^^^

Familiarity with SPICE kernels required to obtain high-accuracy
orientation of the Moon. Understanding the differences between results
obtained using low and high-accuracy Moon orientation data.
Understanding the difference between the MOON_ME and MOON_PA frames.

Approach
^^^^^^^^

The following "tips" may simplify the solution process.

.. code-block:: text

       --   Examine the SPICE kernels provided with this lesson. Use BRIEF
            to find coverage periods of SPK kernels and binary PCKs. Use
            COMMNT to view the comment areas of binary PCKs. Examine text
            kernels, in particular text kernel comments, using a text
            editor or browser.

       --   Decide which SPICE kernels are necessary. Prepare a meta-kernel
            listing the kernels and load it into the program.

       --   Consult the above list titled "SpiceyPy Modules Used" to see
            which routines are needed.

       --   The computational steps listed above should be followed in the
            order shown.

You may find it useful to consult the permuted index, the headers of
various source modules, and the tutorials titled "PCK" and" High
Accuracy Orientation and Body-Fixed frames for Moon and Earth."

Solution
^^^^^^^^

Solution Meta-Kernel

The meta-kernel we created for the solution to this exercise is named
'mrotat.tm'. Its contents follow:

.. code-block:: text

      KPL/MK

      Meta-kernel for the "Moon Rotation" task in the Binary PCK
      Hands On Lesson.

      The names and contents of the kernels referenced by this
      meta-kernel are as follows:

      File name                    Contents
      ---------------------------  ------------------------------------
      naif0008.tls                 Generic LSK
      de414_2000_2020.bsp          Solar System Ephemeris
      moon_060721.tf               Lunar FK
      pck00008.tpc                 NAIF text PCK
      moon_pa_de403_1950-2198.bpc  Moon binary PCK

      \begindata

         KERNELS_TO_LOAD = ( 'kernels/lsk/naif0008.tls'
                             'kernels/spk/de414_2000_2020.bsp'
                             'kernels/fk/moon_060721.tf'
                             'kernels/pck/pck00008.tpc'
                             'kernels/pck/moon_pa_de403_1950-2198.bpc' )
      \begintext

Solution Source Code

A sample solution to the problem follows:

.. code-block:: python

      #
      # Solution mrotat
      #
      from __future__ import print_function
      #
      # SpiceyPy package:
      #
      import spiceypy

      def mrotat():
          #
          # Local parameters
          #
          METAKR = 'mrotat.tm'

          #
          # Load the kernels that this program requires.
          #
          spiceypy.furnsh( METAKR )

          #
          # Convert our UTC string to seconds past J2000 TDB.
          #
          timstr = '2007 JAN 1 00:00:00'
          et     = spiceypy.str2et( timstr )

          #
          # Look up the apparent position of the Earth relative
          # to the Moon's center in the IAU_MOON frame at ET.
          #
          [imoonv, ltime] = spiceypy.spkpos(
              'earth', et, 'iau_moon', 'lt+s', 'moon' )

          #
          #Express the Earth direction in terms of longitude
          #and latitude in the IAU_MOON frame.
          #
          [r, lon, lat] = spiceypy.reclat( imoonv )

          print( '\n'
                 'Moon-Earth direction using low accuracy\n'
                 'PCK and IAU_MOON frame:\n'
                 'Earth lon (deg):        {0:15.6f}\n'
                 'Earth lat (deg):        {1:15.6f}\n'.format(
                     lon * spiceypy.dpr(),
                     lat * spiceypy.dpr() )  )
          #
          # Look up the apparent position of the Earth relative
          # to the Moon's center in the MOON_ME frame at ET.
          #
          [mmoonv, ltime] = spiceypy.spkpos( 'earth', et, 'moon_me',
                                             'lt+s', 'moon'        )
          #
          # Express the Earth direction in terms of longitude
          # and latitude in the MOON_ME frame.
          #
          [r, lon, lat] = spiceypy.reclat( mmoonv )

          print( 'Moon-Earth direction using high accuracy\n'
                 'PCK and MOON_ME frame:\n'
                 'Earth lon (deg):        {0:15.6f}\n'
                 'Earth lat (deg):        {1:15.6f}\n'.format(
                     lon * spiceypy.dpr(),
                     lat * spiceypy.dpr() )  )
          #
          # Find the angular separation of the Earth position
          # vectors in degrees.
          #
          sep = spiceypy.dpr() * spiceypy.vsep( imoonv, mmoonv )

          print( 'For IAU_MOON vs MOON_ME frames:' )
          print( 'Moon-Earth vector separation angle (deg):     '
                 '{:15.6f}\n'.format( sep )  )
          #
          # Look up the apparent position of the Earth relative
          # to the Moon's center in the MOON_PA frame at ET.
          #
          [pmoonv, ltime] = spiceypy.spkpos( 'earth', et, 'moon_pa',
                                             'lt+s',  'moon'        )
          #
          # Express the Earth direction in terms of longitude
          # and latitude in the MOON_PA frame.
          #
          [r, lon, lat] = spiceypy.reclat( pmoonv )

          print( 'Moon-Earth direction using high accuracy\n'
                 'PCK and MOON_PA frame:\n'
                 'Earth lon (deg):        {0:15.6f}\n'
                 'Earth lat (deg):        {1:15.6f}\n'.format(
                     lon * spiceypy.dpr(),
                     lat * spiceypy.dpr() )  )
          #
          # Find the angular separation of the Earth position
          # vectors in degrees.
          #
          sep = spiceypy.dpr() * spiceypy.vsep( pmoonv, mmoonv )

          print( 'For MOON_PA vs MOON_ME frames:' )
          print( 'Moon-Earth vector separation angle (deg):     '
                 '{:15.6f}\n'.format( sep )  )
          #
          # Find the apparent sub-Earth point on the Moon at ET
          # using the MOON_ME frame.
          #
          [msub, trgepc, srfvec ] = spiceypy.subpnt(
              'near point: ellipsoid', 'moon',
              et,  'moon_me', 'lt+s',  'earth' )
          #
          # Display the sub-point in latitudinal coordinates.
          #
          [r, lon, lat] = spiceypy.reclat( msub )

          print( 'Sub-Earth point on Moon using high accuracy\n'
                 'PCK and MOON_ME frame:\n'
                 'Sub-Earth lon (deg):   {0:15.6f}\n'
                 'Sub-Earth lat (deg):   {1:15.6f}\n'.format(
                     lon * spiceypy.dpr(),
                     lat * spiceypy.dpr()  )  )
          #
          # Find the apparent sub-Earth point on the Moon at
          # ET using the MOON_PA frame.
          #
          [psub, trgepc, srfvec] = spiceypy.subpnt(
              'near point: ellipsoid',  'moon',
               et,   'moon_pa', 'lt+s', 'earth'    )
          #
          # Display the sub-point in latitudinal coordinates.
          #
          [r, lon, lat] = spiceypy.reclat( psub )

          print( 'Sub-Earth point on Moon using high accuracy\n'
                 'PCK and MOON_PA frame:\n'
                 'Sub-Earth lon (deg):   {0:15.6f}\n'
                 'Sub-Earth lat (deg):   {1:15.6f}\n'.format(
                     lon * spiceypy.dpr(),
                     lat * spiceypy.dpr() )  )
          #
          # Find the distance between the sub-Earth points
          # in km.
          #
          dist = spiceypy.vdist( msub, psub )

          print( 'Distance between sub-Earth points (km): '
                 '{:15.6f}\n'.format( dist )  )

          spiceypy.unload( METAKR )

      if __name__ == '__main__':
           mrotat()

Solution Sample Output

Execute the program:

.. code-block:: text

      Moon-Earth direction using low accuracy
      PCK and IAU_MOON frame:
      Earth lon (deg):               3.613102
      Earth lat (deg):              -6.438342

      Moon-Earth direction using high accuracy
      PCK and MOON_ME frame:
      Earth lon (deg):               3.611229
      Earth lat (deg):              -6.439501

      For IAU_MOON vs MOON_ME frames:
      Moon-Earth vector separation angle (deg):            0.002194

      Moon-Earth direction using high accuracy
      PCK and MOON_PA frame:
      Earth lon (deg):               3.593319
      Earth lat (deg):              -6.417582

      For MOON_PA vs MOON_ME frames:
      Moon-Earth vector separation angle (deg):            0.028235

      Sub-Earth point on Moon using high accuracy
      PCK and MOON_ME frame:
      Sub-Earth lon (deg):          3.611419
      Sub-Earth lat (deg):         -6.439501

      Sub-Earth point on Moon using high accuracy
      PCK and MOON_PA frame:
      Sub-Earth lon (deg):          3.593509
      Sub-Earth lat (deg):         -6.417582

      Distance between sub-Earth points (km):        0.856182

Earth rotation (erotat)
------------------------------

.. _task-statement-1:

Task Statement
^^^^^^^^^^^^^^

Write a program that performs the following computations:

.. code-block:: text

       1.   Convert the time string 2007 JAN 1 00:00:00 UTC to a double
            precision number representing seconds past J2000 TDB.

            In the following instructions, we'll call the result of this
            computation ET.

       2.   Compute the apparent position of the Moon as seen from the
            Earth in the IAU_EARTH reference frame at the epoch ET. Use
            light time and stellar aberration corrections. Display the
            planetocentric longitude and latitude of the Moon position
            vector in degrees.

       3.   Repeat the first computation using the ITRF93 reference frame.
            Display the results as above.

       4.   Compute the angular separation of the position vectors found
            the the previous two steps. Display the result in degrees.

The following computations (steps 5-10) examine the cause of the angular
offset found above, which is attributable to the rotation between the
ITRF93 and IAU_EARTH frames. Steps 11 and up don't rely on the results
of steps 5-10, so steps 5-10 may be safely skipped if they're not of
interest to you.

For each of the two epochs ET and ET + 100 days, examine the differences
between the axes of the ITRF93 and IAU_EARTH frames using the following
method:

.. code-block:: text

       5.   Convert the epoch of interest to a string in the format style
            "2007-MAY-16 02:29:00.000 (UTC)." Display this string.

       6.   Look up the 3x3 position transformation matrix that converts
            vectors from the IAU_EARTH to the ITRF93 frame at the epoch of
            interest. We'll call the returned matrix RMAT.

       7.   Extract the first row of RMAT into a 3-vector, which we'll call
            ITRFX. This is the X-axis of the ITRF93 frame expressed
            relative to the IAU_EARTH frame.

       8.   Extract the third row of RMAT into a 3-vector, which we'll call
            ITRFZ. This is the Z-axis of the ITRF93 frame expressed
            relative to the IAU_EARTH frame.

       9.   Compute the angular separation between the vector ITRFX and the
            X-axis (1, 0, 0) of the IAU_EARTH frame. Display the result in
            degrees.

      10.   Compute the angular separation between the vector ITRFZ and the
            Z-axis (0, 0, 1) of the IAU_EARTH frame. Display the result in
            degrees.

This is the end of the computations to be performed for the epochs ET
and ET + 100 days. The following steps are part of a new computation.

Find the azimuth and elevation of the apparent position of the Moon as
seen from the DSN station DSS-13 by the following steps:

.. code-block:: text

      11.   Find the apparent position vector of the Moon relative to the
            DSN station DSS-13 in the topocentric reference frame
            DSS-13_TOPO at epoch ET. Use light time and stellar aberration
            corrections.

            For this step, you'll need to have loaded a station SPK file
            providing geocentric station position vectors, as well as a
            frame kernel specifying topocentric reference frames centered
            at the respective DSN stations. (Other kernels will be needed
            as well; you must choose these.)

      12.   Convert the position vector to latitudinal coordinates. Use the
            routine spiceypy.reclat for this computation.

      13.   Compute the Moon's azimuth and elevation as follows: azimuth is
            the negative of topocentric longitude and lies within the range
            0-360 degrees; elevation is equal to the topocentric latitude.
            Display the results in degrees.

The next computations demonstrate "high-accuracy" geometric
computations using the Earth as the target body. These computations are
*not* realistic; they are simply meant to demonstrate SPICE system
features used for geometry computations involving the Earth as a target
body. For example, the same basic techniques would be used to find the
sub-solar point on the Earth as seen from an Earth-orbiting spacecraft.

.. code-block:: text

      14.   Compute the apparent sub-solar point on the Earth at ET,
            expressed relative to the IAU_EARTH reference frame, using
            light time and stellar aberration corrections and using the Sun
            as the observer. Convert the sub-solar point to latitudinal
            coordinates using spiceypy.reclat. Display the longitude and
            latitude of the sub-solar point in degrees.

      15.   Repeat the sub-solar point computation described above, using
            the ITRF93 Earth body-fixed reference frame. Display the
            results as above.

      16.   Compute the distance between the two sub-solar points found
            above. Display the result in kilometers.

.. _learning-goals-1:

Learning Goals
^^^^^^^^^^^^^^

Familiarity with SPICE kernels required to obtain high-accuracy
orientation of the Earth. Understanding the differences between results
obtained using low and high-accuracy Earth orientation data.

Understanding of topocentric frames and computation of target geometry
relative to a surface location on the Earth. Knowledge of SPICE kernels
required to support such computations.

.. _approach-1:

Approach
^^^^^^^^

The following "tips" may simplify the solution process.

.. code-block:: text

       --   Examine the SPICE kernels provided with this lesson. Use BRIEF
            to find coverage periods of SPK kernels and binary PCKs. Use
            COMMNT to view the comment areas of binary PCKs. Examine text
            kernels, in particular text kernel comments, using a text
            editor or browser.

       --   Decide which SPICE kernels are necessary. Prepare a meta-kernel
            listing the kernels and load it into the program.

       --   Consult the above list titled "SpiceyPy Modules Used" to see
            which routines are needed. Note the functions used to provide
            the values "seconds per day," "degrees per radian," and "2
            times Pi."

       --   Examine the header of the function spiceypy.reclat. Note that
            this function may be used for coordinate conversions in
            situations where the input rectangular coordinates refer to any
            reference frame, not only a body-centered, body-fixed frame
            whose X-Y plane coincides with the body's equator.

       --   The computational steps listed above should be followed in the
            order shown, but steps 5-10 may be omitted.

You may find it useful to consult the permuted index, the headers of
various source modules, and the tutorials titled "PCK" and" High
Accuracy Orientation and Body-Fixed frames for Moon and Earth."

.. _solution-1:

Solution
^^^^^^^^

Solution Meta-Kernel

The meta-kernel we created for the solution to this exercise is named
'erotat.tm'. Its contents follow:

.. code-block:: text

      KPL/MK

      Meta-kernel for the "Earth Rotation" task
      in the Binary PCK Hands On Lesson.

      The names and contents of the kernels referenced by this
      meta-kernel are as follows:

      File name                       Contents
      ------------------------------  ---------------------------------
      naif0008.tls                    Generic LSK
      de414_2000_2020.bsp             Solar System Ephemeris
      earthstns_itrf93_050714.bsp     DSN station Ephemeris
      earth_topo_050714.tf            Earth topocentric FK
      pck00008.tpc                    NAIF text PCK
      earth_000101_070725_070503.bpc  Earth binary PCK


      \begindata

      KERNELS_TO_LOAD = ( 'kernels/lsk/naif0008.tls'
                          'kernels/spk/de414_2000_2020.bsp'
                          'kernels/spk/earthstns_itrf93_050714.bsp'
                          'kernels/fk/earth_topo_050714.tf'
                          'kernels/pck/pck00008.tpc'
                          'kernels/pck/earth_000101_070725_070503.bpc' )

      \begintext

Solution Source Code

A sample solution to the problem follows:

.. code-block:: python

      #
      # Solution mrotat
      #
      from __future__ import print_function
      #
      # SpiceyPy package:
      #
      import spiceypy

      def erotat():
          #
          # Local parameters
          #
          METAKR = 'erotat.tm'

          x = [ 1.0, 0.0, 0.0 ]
          z = [ 0.0, 0.0, 1.0 ]

          #
          # Load the kernels that this program requires.
          #
          spiceypy.furnsh( METAKR )

          #
          # Convert our UTC string to seconds past J2000 TDB.
          #
          timstr = '2007 JAN 1 00:00:00'
          et     = spiceypy.str2et( timstr )

          #
          # Look up the apparent position of the Moon relative
          # to the Earth's center in the IAU_EARTH frame at ET.
          #
          [lmoonv, ltime] = spiceypy.spkpos( 'moon', et, 'iau_earth',
                                             'lt+s', 'earth'        )
          #
          # Express the Moon direction in terms of longitude
          # and latitude in the IAU_EARTH frame.
          #
          [r, lon, lat] = spiceypy.reclat( lmoonv )

          print( 'Earth-Moon direction using low accuracy\n'
                 'PCK and IAU_EARTH frame:\n'
                 'Moon lon (deg):        {0:15.6f}\n'
                 'Moon lat (deg):        {1:15.6f}\n'.format(
                     lon * spiceypy.dpr(),
                     lat * spiceypy.dpr() )  )
          #
          # Look up the apparent position of the Moon relative
          # to the Earth's center in the ITRF93 frame at ET.
          #
          [hmoonv, ltime] = spiceypy.spkpos( 'moon', et, 'ITRF93',
                                             'lt+s', 'earth'      )
          #
          # Express the Moon direction in terms of longitude
          # and latitude in the ITRF93 frame.
          #
          [r, lon, lat] = spiceypy.reclat( hmoonv )

          print( 'Earth-Moon direction using high accuracy\n'
                 'PCK and ITRF93 frame:\n'
                 'Moon lon (deg):        {0:15.6f}\n'
                 'Moon lat (deg):        {1:15.6f}\n'.format(
                     lon * spiceypy.dpr(),
                     lat * spiceypy.dpr() )  )
          #
          # Find the angular separation of the Moon position
          # vectors in degrees.
          #
          sep = spiceypy.dpr() * spiceypy.vsep( lmoonv, hmoonv )

          print( 'Earth-Moon vector separation angle (deg):     '
                 '{:15.6f}\n'.format( sep )  )

          #
          # Next, express the +Z and +X axes of the ITRF93 frame in
          # the IAU_EARTH frame. We'll do this for two times: et
          # and et + 100 days.
          #
          for  i  in range(2):
              #
              # Set the time, expressing the time delta in
              # seconds.
              #
              t = et + i*spiceypy.spd()*100

              #
              # Convert the TDB time T to a string for output.
              #
              outstr = spiceypy.timout(
                  t, 'YYYY-MON-DD HR:MN:SC.### (UTC)' )

              print( 'Epoch: {:s}'.format( outstr ) )

              #
              # Find the rotation matrix for conversion of
              # position vectors from the IAU_EARTH to the
              # ITRF93 frame.
              #
              rmat  = spiceypy.pxform( 'iau_earth', 'itrf93', t )
              itrfx = rmat[0]
              itrfz = rmat[2]

              #
              # Display the angular offsets of the ITRF93
              # +X and +Z axes from their IAU_EARTH counterparts.
              #
              sep = spiceypy.vsep( itrfx, x )

              print( 'ITRF93 - IAU_EARTH +X axis separation '
                     'angle (deg): {:13.6f}'.format(
                         sep * spiceypy.dpr() )  )

              sep = spiceypy.vsep( itrfz, z )

              print( 'ITRF93 - IAU_EARTH +Z axis separation '
                     'angle (deg): {:13.6f}\n'.format(
                         sep * spiceypy.dpr() )  )

          #
          # Find the azimuth and elevation of apparent
          # position of the Moon in the local topocentric
          # reference frame at the DSN station DSS-13.
          # First look up the Moon's position relative to the
          # station in that frame.
          #
          [topov, ltime] = spiceypy.spkpos( 'moon', et, 'DSS-13_TOPO',
                                            'lt+s', 'DSS-13'         )

          #
          # Express the station-moon direction in terms of longitude
          # and latitude in the DSS-13_TOPO frame.
          #
          [r, lon, lat] = spiceypy.reclat( topov )

          #
          # Convert to azimuth-elevation.
          #
          az = -lon

          if  az < 0.0:
              az += spiceypy.twopi()

          el = lat

          print( 'DSS-13-Moon az/el using high accuracy '
                 'PCK and DSS-13_TOPO frame:\n'
                 'Moon Az (deg):        {0:15.6f}\n'
                 'Moon El (deg):        {1:15.6f}\n'.format(
                     az * spiceypy.dpr(),
                     el * spiceypy.dpr() )  )

          #
          # Find the sub-solar point on the Earth at ET using the
          # Earth body-fixed frame IAU_EARTH. Treat the Sun as
          # the observer.
          #
          [lsub, trgepc, srfvec] = spiceypy.subslr(
              'near point: ellipsoid', 'earth', et,
              'IAU_EARTH',             'lt+s',  'sun' );

          #
          # Display the sub-point in latitudinal coordinates.
          #
          [r, lon, lat] = spiceypy.reclat( lsub )

          print( 'Sub-Solar point on Earth using low accuracy\n'
                 'PCK and IAU_EARTH frame:\n'
                 'Sub-Solar lon (deg):   {0:15.6f}\n'
                 'Sub-Solar lat (deg):   {1:15.6f}\n'.format(
                     lon * spiceypy.dpr(),
                     lat * spiceypy.dpr() )  )

          #
          # Find the sub-solar point on the Earth at ET using the
          # Earth body-fixed frame ITRF93. Treat the Sun as
          # the observer.
          #
          [hsub, trgepc, srfvec] = spiceypy.subslr(
              'near point: ellipsoid', 'earth', et,
              'ITRF93',                'lt+s',  'sun' );

          #
          # Display the sub-point in latitudinal coordinates.
          #
          [r, lon, lat] = spiceypy.reclat( hsub )

          print( 'Sub-Solar point on Earth using '
                 'high accuracy \nPCK and ITRF93 frame:\n'
                 'Sub-Solar lon (deg):   {0:15.6f}\n'
                 'Sub-Solar lat (deg):   {1:15.6f}\n'.format(
                     lon * spiceypy.dpr(),
                     lat * spiceypy.dpr() )  )

          #
          # Find the distance between the sub-solar point
          # vectors in km.
          #
          dist = spiceypy.vdist( lsub, hsub )

          print( 'Distance between sub-solar points (km): '
                 '{:15.6f}'.format( dist )  )


          spiceypy.unload( METAKR )

      if __name__ == '__main__':
           erotat()

Solution Sample Output

Execute the program:

.. code-block:: text

      Earth-Moon direction using low accuracy
      PCK and IAU_EARTH frame:
      Moon lon (deg):             -35.496272
      Moon lat (deg):              26.416959

      Earth-Moon direction using high accuracy
      PCK and ITRF93 frame:
      Moon lon (deg):             -35.554286
      Moon lat (deg):              26.419156

      Earth-Moon vector separation angle (deg):            0.052002

      Epoch: 2007-JAN-01 00:00:00.000 (UTC)
      ITRF93 - IAU_EARTH +X axis separation angle (deg):      0.057677
      ITRF93 - IAU_EARTH +Z axis separation angle (deg):      0.002326

      Epoch: 2007-APR-10 23:59:59.998 (UTC)
      ITRF93 - IAU_EARTH +X axis separation angle (deg):      0.057787
      ITRF93 - IAU_EARTH +Z axis separation angle (deg):      0.002458

      DSS-13-Moon az/el using high accuracy PCK and DSS-13_TOPO frame:
      Moon Az (deg):              72.169006
      Moon El (deg):              20.689488

      Sub-Solar point on Earth using low accuracy
      PCK and IAU_EARTH frame:
      Sub-Solar lon (deg):       -177.100531
      Sub-Solar lat (deg):        -22.910377

      Sub-Solar point on Earth using high accuracy
      PCK and ITRF93 frame:
      Sub-Solar lon (deg):       -177.157874
      Sub-Solar lat (deg):        -22.912593

      Distance between sub-solar points (km):        5.881861
