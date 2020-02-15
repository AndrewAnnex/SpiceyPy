Remote Sensing Hands-On Lesson, using CASSINI
==============================================

November 20, 2017

Overview
--------

In this lesson you will develop a series of simple programs that
demonstrate the usage of SpiceyPy to compute a variety of different
geometric quantities applicable to experiments carried out by a remote
sensing instrument flown on an interplanetary spacecraft. This
particular lesson focuses on a framing camera flying on the Cassini
spacecraft, but many of the concepts are easily extended and generalized
to other scenarios.

References
----------

This section lists SPICE documents referred to in this lesson.

In some cases the lesson explanations also refer to the information
provided in the meta-data area of the kernels used in the lesson
examples. It is especially true in case of the FK and IK files, which
often contain comprehensive descriptions of the frames, instrument FOVs,
etc. Since both the FK and IK are text kernels, the information provided
in them can be viewed using any text editor, while the meta information
provided in binary kernels—SPKs and CKs—can be viewed using
"commnt" or" spacit" utility programs located in "cspice/exe" of
Toolkit installation tree.

Tutorials
^^^^^^^^^^

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
      CK                Spacecraft Orientation Data
      DSK               Detailed Target Shape (Topography) Data

These tutorials are available from the NAIF ftp server at JPL:

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
      ck.req           Obtaining spacecraft orientation data
      dsk.req          Obtaining detailed body shape data
      frames.req       Using reference frames
      naif_ids.req     Determining body ID codes
      pck.req          Obtaining planetary constants data
      sclk.req         SCLK time conversion
      spk.req          Obtaining ephemeris Data
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

      #  FILE NAME                 TYPE DESCRIPTION
      -- ------------------------- ---- -----------------------------------
      1  naif0008.tls              LSK  Generic LSK
      2  cas00084.tsc              SCLK Cassini SCLK
      3  981005_PLTEPH-DE405S.bsp  SPK  Solar System Ephemeris
      4  020514_SE_SAT105.bsp      SPK  Saturnian Satellite Ephemeris
      5  030201AP_SK_SM546_T45.bsp SPK  Cassini Spacecraft SPK
      6  cas_v37.tf                FK   Cassini FK
      7  04135_04171pc_psiv2.bc    CK   Cassini Spacecraft CK
      8  cpck05Mar2004.tpc         PCK  Cassini Project PCK
      9  phoebe_64q.bds            DSK  Phoebe DSK
      10 cas_iss_v09.ti            IK   ISS Instrument Kernel

These SPICE kernels are included in the lesson package available from
the NAIF server at JPL:

::

      ftp://naif.jpl.nasa.gov/pub/naif/toolkit_docs/Lessons/

In addition to these kernels, the extra credit exercises require the
following kernels:

::

      #  FILE NAME       TYPE DESCRIPTION
      -- --------------- ---- ---------------------------------------------
      11 jup310_2004.bsp SPK  Generic Jovian Satellite Ephemeris

These SPICE kernels are available from the NAIF server at JPL:

::

      https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/satellites/

SpiceyPy Modules Used
---------------------

This section provides a complete list of the functions and kernels that
are suggested for usage in each of the exercises in this lesson. (You
may wish to not look at this list unless/until you "get stuck" while
working on your own.)

::

      CHAPTER EXERCISE   FUNCTIONS        NON-VOID         KERNELS
      ------- ---------  ---------------  ---------------  ----------
         1    convtm     spiceypy.furnsh  spiceypy.str2et  1,2
                         spiceypy.unload  spiceypy.etcal
                                          spiceypy.timout
                                          spiceypy.sce2s

              extra (*)                   spiceypy.unitim  1,2
                                          spiceypy.sct2e
                                          spiceypy.et2utc
                                          spiceypy.scs2e

         2    getsta     spiceypy.furnsh  spiceypy.str2et  1,3-5
                         spiceypy.unload  spiceypy.spkezr
                                          spiceypy.spkpos
                                          spiceypy.vnorm
                                          spiceypy.convrt

              extra (*)  spiceypy.kclear                   1,3-5,11

         3    xform      spiceypy.furnsh  spiceypy.str2et  1-8
                         spiceypy.unload  spiceypy.spkezr
                                          spiceypy.sxform
                                          spiceypy.mxvg
                                          spiceypy.spkpos
                                          spiceypy.pxform
                                          spiceypy.mxv
                                          spiceypy.convrt
                                          spiceypy.vsep

              extra (*)  spiceypy.kclear                   1-8

         4    subpts     spiceypy.furnsh  spiceypy.str2et  1,3-5,8,9
                         spiceypy.unload  spiceypy.subpnt
                                          spiceypy.vnorm
                                          spiceypy.subslr

              extra (*)  spiceypy.kclear  spiceypy.reclat  1,3-5,8
                                          spiceypy.dpr
                                          spiceypy.bodvrd
                                          spiceypy.recpgr

         5    fovint     spiceypy.furnsh  spiceypy.str2et  1-10
                         spiceypy.unload  spiceypy.bodn2c
                                          spiceypy.getfov
                                          spiceypy.sincpt
                                          spiceypy.reclat
                                          spiceypy.dpr
                                          spiceypy.illumf
                                          spiceypy.et2lst


         (*) Additional APIs and kernels used in Extra Credit tasks.

Use the Python built-in help system on the various functions listed
above for the API parameters' description, and refer to the headers of
their corresponding CSPICE versions for detailed interface
specifications.

Time Conversion (convtm)
------------------------------

Task Statement
^^^^^^^^^^^^^^

Write a program that prompts the user for an input UTC time string,
converts it to the following time systems and output formats:

::

       1.   Ephemeris Time (ET) in seconds past J2000

       2.   Calendar Ephemeris Time

       3.   Spacecraft Clock Time

and displays the results. Use the program to convert “2004 jun 11
19:32:00” UTC into these alternate systems.

Learning Goals
^^^^^^^^^^^^^^

Familiarity with the various time conversion and parsing functions
available in the Toolkit. Exposure to source code headers and their
usage in learning to call functions.

Approach
^^^^^^^^

The solution to the problem can be broken down into a series of simple
steps:

::

       --   Decide which SPICE kernels are necessary. Prepare a meta-kernel
            listing the kernels and load it into the program.

       --   Prompt the user for an input UTC time string.

       --   Convert the input time string into ephemeris time expressed as
            seconds past J2000 TDB. Display the result.

       --   Convert ephemeris time into a calendar format. Display the
            result.

       --   Convert ephemeris time into a spacecraft clock string. Display
            the result.

You may find it useful to consult the permuted index, the headers of
various source modules, and the
"Time Required Reading" (time.req) and" SCLK Required Reading"
(sclk.req) documents.

When completing the "calendar format" step above, consider using one
of two possible methods: spiceypy.etcal or spiceypy.timout.

Solution
^^^^^^^^

Solution Meta-Kernel

The meta-kernel we created for the solution to this exercise is named
'convtm.tm'. Its contents follow:

::

      KPL/MK

         This is the meta-kernel used in the solution of the "Time
         Conversion" task in the Remote Sensing Hands On Lesson.

         The names and contents of the kernels referenced by this
         meta-kernel are as follows:

         File name                   Contents
         --------------------------  -----------------------------
         naif0008.tls                Generic LSK
         cas00084.tsc                Cassini SCLK


         \begindata
         KERNELS_TO_LOAD = ( 'kernels/lsk/naif0008.tls',
                             'kernels/sclk/cas00084.tsc' )
         \begintext

Solution Source Code

A sample solution to the problem follows:

::

      #
      # Solution convtm
      #
      from __future__ import print_function
      from builtins import input

      import spiceypy

      def convtm():
          #
          # Local Parameters
          #
          METAKR = 'convtm.tm'
          SCLKID = -82

          spiceypy.furnsh( METAKR )

          #
          # Prompt the user for the input time string.
          #
          utctim = input( 'Input UTC Time: ' )

          print( 'Converting UTC Time: {:s}'.format( utctim ) )

          #
          # Convert utctim to ET.
          #
          et = spiceypy.str2et( utctim )

          print( '   ET Seconds Past J2000: {:16.3f}'.format( et ) )

          #
          # Now convert ET to a calendar time string.
          # This can be accomplished in two ways.
          #
          calet = spiceypy.etcal( et )

          print( '   Calendar ET (etcal):   {:s}'.format( calet ) )

          #
          # Or use timout for finer control over the
          # output format. The picture below was built
          # by examining the header of timout.
          #
          calet = spiceypy.timout( et, 'YYYY-MON-DDTHR:MN:SC ::TDB' )

          print( '   Calendar ET (timout):  {:s}'.format( calet ) )

          #
          # Convert ET to spacecraft clock time.
          #
          sclkst = spiceypy.sce2s( SCLKID, et )

          print( '   Spacecraft Clock Time: {:s}'.format( sclkst ) )

          spiceypy.unload( METAKR )

      if __name__ == '__main__':
          convtm()

Solution Sample Output

Execute the program:

::

      Input UTC Time: 2004 jun 11 19:32:00
      Converting UTC Time: 2004 jun 11 19:32:00
         ET Seconds Past J2000:    140254384.185
         Calendar ET (etcal):   2004 JUN 11 19:33:04.184
         Calendar ET (timout):  2004-JUN-11T19:33:04
         Spacecraft Clock Time: 1/1465674964.105

Extra Credit
^^^^^^^^^^^^^

In this "extra credit" section you will be presented with more
complex tasks, aimed at improving your understanding of time
conversions, the Toolkit routines that deal with them, and some common
errors that may happen during the execution of these conversions.

These "extra credit" tasks are provided as task statements, and
unlike the regular tasks, no approach or solution source code is
provided. In the next section, you will find the numeric solutions (when
applicable) and answers to the questions asked in these tasks.

Task statements and questions

::

       1.   Extend your program to convert the input UTC time string to TDB
            Julian Date. Convert "2004 jun 11 19:32:00" UTC.

       2.   Remove the LSK from the original meta-kernel and run your
            program again, using the same inputs as before. Has anything
            changed? Why?

       3.   Remove the SCLK from the original meta-kernel and run your
            program again, using the same inputs as before. Has anything
            changed? Why?

       4.   Modify your program to perform conversion of UTC or ephemeris
            time, to a spacecraft clock string using the NAIF ID for the
            CASSINI ISS NAC camera. Convert "2004 jun 11 19:32:00" UTC.

       5.   Find the earliest UTC time that can be converted to CASSINI
            spacecraft clock.

       6.   Extend your program to convert the spacecraft clock time
            obtained in the regular task back to UTC Time and present it in
            ISO calendar date format, with a resolution of milliseconds.

       7.   Examine the contents of the generic LSK and the CASSINI SCLK
            kernels. Can you understand and explain what you see?

Solutions and answers

::

       1.   Two methods exist in order to convert ephemeris time to Julian
            Date: spiceypy.unitim and spiceypy.timout. The difference
            between them is the type of output produced by each method.
            spiceypy.unitim returns the double precision value of an input
            epoch, while spiceypy.timout returns the string representation
            of the ephemeris time in Julian Date format (when picture input
            is set to 'JULIAND.######### ::TDB'). Refer to the function
            header for further details. The solution for the requested
            input UTC string is:

         Julian Date TDB:   2453168.3146318

       2.   When running the original program without the LSK kernel, an
            error is produced:

      Traceback (most recent call last):
        File "convtm.py", line 67, in <module>
          convtm()
        File "convtm.py", line 30, in convtm
          et = spiceypy.str2et( utctim )
        File "/home/bsemenov/local/lib/python3.5/site-packages/spiceypy/spi
      ceypy.py", line 76, in with_errcheck
          check_for_spice_error(f)
        File "/home/bsemenov/local/lib/python3.5/site-packages/spiceypy/spi
      ceypy.py", line 59, in check_for_spice_error
          raise stypes.SpiceyError(msg)
      spiceypy.utils.support_types.SpiceyError:
      =====================================================================
      ===========

      Toolkit version: N0066

      SPICE(NOLEAPSECONDS) --

      The variable that points to the leapseconds (DELTET/DELTA_AT) could n
      ot be located in the kernel pool.  It is likely that the leapseconds
      kernel has not been loaded via the routine FURNSH.

      str2et_c --> STR2ET --> TTRANS

      =====================================================================
      ===========

            This error is triggered by spiceypy.str2et because the variable
            that points to the leapseconds is not present in the kernel
            pool and therefore the program lacks data required to perform
            the requested UTC to ephemeris time conversion.

            By default, SPICE will report, as a minimum, a short
            descriptive message and a expanded form of this short message
            where more details about the error are provided. If this error
            message is not sufficient for you to understand what has
            happened, you could go to the "Exceptions" section in the
            SPICELIB or CSPICE headers of the function that has triggered
            the error and find out more information about the possible
            causes.

       3.   When running the original program without the SCLK kernel, an
            error is produced:

      Traceback (most recent call last):
        File "convtm.py", line 67, in <module>
          convtm()
        File "convtm.py", line 58, in convtm
          sclkst = spiceypy.sce2s( SCLKID, et )
        File "/home/bsemenov/local/lib/python3.5/site-packages/spiceypy/spi
      ceypy.py", line 76, in with_errcheck
          check_for_spice_error(f)
        File "/home/bsemenov/local/lib/python3.5/site-packages/spiceypy/spi
      ceypy.py", line 59, in check_for_spice_error
          raise stypes.SpiceyError(msg)
      spiceypy.utils.support_types.SpiceyError:
      =====================================================================
      ===========

      Toolkit version: N0066

      SPICE(KERNELVARNOTFOUND) --
      The Variable Was not Found in the Kernel Pool.
      SCLK_DATA_TYPE_82 not found. Did you load the SCLK kernel?

      sce2s_c --> SCE2S --> SCE2T --> SCTYPE --> SCLI01

      =====================================================================
      ===========

            This error is triggered by spiceypy.sce2s. In this case the
            error message may not give you enough information to understand
            what has actually happened. Nevertheless, the expanded form of
            this short message clearly indicates that the SCLK kernel for
            the spacecraft ID -82 has not been loaded.

            The UTC string to ephemeris time conversion and the conversion
            of ephemeris time into a calendar format worked normally as
            these conversions only require the LSK kernel to be loaded.

       4.   The first thing you need to do is to find out what the NAIF ID
            is for the CASSINI ISS NAC camera. In order to do so, examine
            the ISS instrument kernel listed above and look for the "NAIF
            ID Code to Name Mapping" and there, for the NAIF ID given to
            CASSINI_ISS_NAC (which is -82360). Then replace in your code
            the SCLK ID -82 with -82360. After executing the program using
            the original meta-kernel, you will be getting the same error as
            in the previous task. Despite the error being exactly the same,
            this case is different. Generally, spacecraft clocks are
            associated with the spacecraft ID and not with its payload,
            sensors or structures IDs. Therefore, in order to do
            conversions from/to spacecraft clock for payload, sensors or
            spacecraft structures, the spacecraft ID must be used.

            Note that this does not need to be true for all missions or
            payloads, as SPICE does not restrict the SCLKs to spacecraft
            IDs only. Please refer to your mission's SCLK kernels for
            particulars.

       5.   Use spiceypy.sct2e with the encoding of the Cassini spacecraft
            clock time set to 0.0 ticks and convert the resulting ephemeris
            time to UTC using either spiceypy.timout or spiceypy.et2utc.
            The solution for the requested SCLK string is:

         Earliest UTC convertible to SCLK: 1980-01-01T00:00:00.000

       6.   Use spiceypy.scs2e with the SCLK string obtained in the
            computations performed in the regular tasks and convert the
            resulting ephemeris time to UTC using either spiceypy.et2utc,
            with 'ISOC' format and 3 digits precision, or using
            spiceypy.timout using the time picture 'YYYY-MM-DDTHR:MN:SC.###
            ::RND'. The solution of the requested conversion is:

         Spacecraft Clock Time:          1/1465674964.105
         UTC time from spacecraft clock: 2004-06-11T19:31:59.999

Obtaining Target States and Positions (getsta)
----------------------------------------------

.. _task-statement-rs-1:

Task Statement
^^^^^^^^^^^^^^

Write a program that prompts the user for an input UTC time string,
computes the following quantities at that epoch:

::

       1.   The apparent state of Phoebe as seen from CASSINI in the J2000
            frame, in kilometers and kilometers/second. This vector itself
            is not of any particular interest, but it is a useful
            intermediate quantity in some geometry calculations.

       2.   The apparent position of the Earth as seen from CASSINI in the
            J2000 frame, in kilometers.

       3.   The one-way light time between CASSINI and the apparent
            position of Earth, in seconds.

       4.   The apparent position of the Sun as seen from Phoebe in the
            J2000 frame (J2000), in kilometers.

       5.   The actual (geometric) distance between the Sun and Phoebe, in
            astronomical units.

and displays the results. Use the program to compute these quantities at
“2004 jun 11 19:32:00” UTC.

.. _learning-goals-rs-1:

Learning Goals
^^^^^^^^^^^^^^

Understand the anatomy of an spiceypy.spkezr call. Discover the
difference between spiceypy.spkezr and spiceypy.spkpos. Familiarity with
the Toolkit utility "brief". Exposure to unit conversion with
SpiceyPy.

.. _approach-rs-1:

Approach
^^^^^^^^

The solution to the problem can be broken down into a series of simple
steps:

::

       --   Decide which SPICE kernels are necessary. Prepare a meta-kernel
            listing the kernels and load it into the program.

       --   Prompt the user for an input time string.

       --   Convert the input time string into ephemeris time expressed as
            seconds past J2000 TDB.

       --   Compute the state of Phoebe relative to CASSINI in the J2000
            reference frame, corrected for aberrations.

       --   Compute the position of Earth relative to CASSINI in the J2000
            reference frame, corrected for aberrations. (The function in
            the library that computes this also returns the one-way light
            time between CASSINI and Earth.)

       --   Compute the position of the Sun relative to Phoebe in the J2000
            reference frame, corrected for aberrations.

       --   Compute the position of the Sun relative to Phoebe without
            correcting for aberration.

            Compute the length of this vector. This provides the desired
            distance in kilometers.

       --   Convert the distance in kilometers into AU.

You may find it useful to consult the permuted index, the headers of
various source modules, and the "SPK Required Reading" (spk.req)
document.

When deciding which SPK files to load, the Toolkit utility "brief"
may be of some use.

"brief" is located in the" cspice/exe"directory for C toolkits.
Consult its user's guide available in "cspice/doc/brief.ug" for
details.

.. _solution-rs-1:

Solution
^^^^^^^^

Solution Meta-Kernel

The meta-kernel we created for the solution to this exercise is named
'getsta.tm'. Its contents follow:

::

      KPL/MK

         This is the meta-kernel used in the solution of the
         "Obtaining Target States and Positions" task in the
         Remote Sensing Hands On Lesson.

         The names and contents of the kernels referenced by this
         meta-kernel are as follows:

         File name                   Contents
         --------------------------  -----------------------------
         naif0008.tls                Generic LSK
         981005_PLTEPH-DE405S.bsp    Solar System Ephemeris
         020514_SE_SAT105.bsp        Saturnian Satellite Ephemeris
         030201AP_SK_SM546_T45.bsp   Cassini Spacecraft SPK


         \begindata
         KERNELS_TO_LOAD = ( 'kernels/lsk/naif0008.tls',
                             'kernels/spk/981005_PLTEPH-DE405S.bsp',
                             'kernels/spk/020514_SE_SAT105.bsp',
                             'kernels/spk/030201AP_SK_SM546_T45.bsp' )
         \begintext

Solution Source Code

A sample solution to the problem follows:

::

      #
      # Solution getsta.py
      #
      from __future__ import print_function
      from builtins import input

      import spiceypy

      def getsta():
          #
          # Local parameters
          #
          METAKR = 'getsta.tm'

          #
          # Load the kernels that this program requires.  We
          # will need a leapseconds kernel to convert input
          # UTC time strings into ET.  We also will need the
          # necessary SPK files with coverage for the bodies
          # in which we are interested.
          #
          spiceypy.furnsh( METAKR )

          #
          #Prompt the user for the input time string.
          #
          utctim = input( 'Input UTC Time: ' )

          print( 'Converting UTC Time: {:s}'.format(utctim)  )

          #
          #Convert utctim to ET.
          #
          et = spiceypy.str2et( utctim )

          print( '   ET seconds past J2000: {:16.3f}'.format(et) )

          #
          # Compute the apparent state of Phoebe as seen from
          # CASSINI in the J2000 frame.  All of the ephemeris
          # readers return states in units of kilometers and
          # kilometers per second.
          #
          [state, ltime] = spiceypy.spkezr( 'PHOEBE', et,      'J2000',
                                            'LT+S',   'CASSINI'       )

          print( '   Apparent state of Phoebe as seen '
                 'from CASSINI in the J2000\n'
                 '      frame (km, km/s):'              )

          print( '      X = {:16.3f}'.format(state[0])       )
          print( '      Y = {:16.3f}'.format(state[1])       )
          print( '      Z = {:16.3f}'.format(state[2])       )
          print( '     VX = {:16.3f}'.format(state[3])       )
          print( '     VY = {:16.3f}'.format(state[4])       )
          print( '     VZ = {:16.3f}'.format(state[5])       )

          #
          # Compute the apparent position of Earth as seen from
          # CASSINI in the J2000 frame.  Note: We could have
          # continued using spkezr and simply ignored the
          # velocity components.
          #
          [pos, ltime] = spiceypy.spkpos( 'EARTH', et,        'J2000',
                                          'LT+S',  'CASSINI',         )

          print( '   Apparent position of Earth as '
                 'seen from CASSINI in the J2000\n'
                 '      frame (km):'                )
          print( '      X = {:16.3f}'.format(pos[0])  )
          print( '      Y = {:16.3f}'.format(pos[1])  )
          print( '      Z = {:16.3f}'.format(pos[2])  )

          #
          # We need only display LTIME, as it is precisely the
          # light time in which we are interested.
          #
          print( '   One way light time between CASSINI and '
                 'the apparent position\n'
                 '      of Earth (seconds):'
                 ' {:16.3f}'.format(ltime) )

          #
          # Compute the apparent position of the Sun as seen from
          # PHOEBE in the J2000 frame.
          #
          [pos, ltime] = spiceypy.spkpos( 'SUN',  et,       'J2000',
                                          'LT+S', 'PHOEBE',         )

          print( '   Apparent position of Sun as '
                 'seen from Phoebe in the\n'
                 '       J2000 frame (km):'           )
          print( '      X = {:16.3f}'.format(pos[0])  )
          print( '      Y = {:16.3f}'.format(pos[1])  )
          print( '      Z = {:16.3f}'.format(pos[2])  )

          #
          # Now we need to compute the actual distance between
          # the Sun and Phoebe.  The above spkpos call gives us
          # the apparent distance, so we need to adjust our
          # aberration correction appropriately.
          #
          [pos, ltime] = spiceypy.spkpos( 'SUN',  et,      'J2000',
                                          'NONE', 'PHOEBE'         )

          #
          # Compute the distance between the body centers in
          # kilometers.
          #
          dist = spiceypy.vnorm( pos )

          #
          # Convert this value to AU using convrt.
          #
          dist = spiceypy.convrt( dist, 'KM', 'AU' )

          print( '   Actual distance between Sun and '
                 'Phoebe body centers:\n'
                 '      (AU): {:16.3f}'.format(dist) )

          spiceypy.unload( METAKR )

      if __name__ == '__main__':
          getsta()

Solution Sample Output

Execute the program:

::

      Input UTC Time: 2004 jun 11 19:32:00
      Converting UTC Time: 2004 jun 11 19:32:00
         ET seconds past J2000:    140254384.185
         Apparent state of Phoebe as seen from CASSINI in the J2000
            frame (km, km/s):
            X =         -119.921
            Y =         2194.139
            Z =          -57.639
           VX =           -5.980
           VY =           -2.119
           VZ =           -0.295
         Apparent position of Earth as seen from CASSINI in the J2000
            frame (km):
            X =    353019393.123
            Y =  -1328180352.140
            Z =   -568134171.697
         One way light time between CASSINI and the apparent position
            of Earth (seconds):         4960.427
         Apparent position of Sun as seen from Phoebe in the
             J2000 frame (km):
            X =    376551465.272
            Y =  -1190495630.303
            Z =   -508438699.110
         Actual distance between Sun and Phoebe body centers:
            (AU):            9.012

.. _extra-credit-rs-1:

Extra Credit
^^^^^^^^^^^^^

In this "extra credit" section you will be presented with more
complex tasks, aimed at improving your understanding of state
computations, particularly the application of the different light time
and stellar aberration corrections available in the spiceypy.spkezr
function, and some common errors that may happen when computing these
states.

These "extra credit" tasks are provided as task statements, and
unlike the regular tasks, no approach or solution source code is
provided. In the next section, you will find the numeric solutions (when
applicable) and answers to the questions asked in these tasks.

Task statements and questions

::

       1.   Remove the Solar System ephemerides SPK from the original
            meta-kernel and run your program again, using the same inputs
            as before. Has anything changed? Why?

       2.   Extend your program to compute the geometric position of
            Jupiter as seen from Saturn in the J2000 frame (J2000), in
            kilometers.

       3.   Extend, or modify, your program to compute the position of the
            Sun as seen from Saturn in the J2000 frame (J2000), in
            kilometers, using the following light time and aberration
            corrections: NONE, LT and LT+S. Explain the differences.

       4.   Examine the CASSINI frames definition kernel and the ISS
            instrument kernel to find the SPICE ID/name definitions.

Solutions and answers

::

       1.   When running the original program without the Solar System
            ephemerides SPK, an error is produced by spiceypy.spkezr:

      Traceback (most recent call last):
        File "getsta.py", line 128, in <module>
          getsta()
        File "getsta.py", line 47, in getsta
          'LT+S',   'CASSINI'       )
        File "/home/bsemenov/local/lib/python3.5/site-packages/spiceypy/spi
      ceypy.py", line 76, in with_errcheck
          check_for_spice_error(f)
        File "/home/bsemenov/local/lib/python3.5/site-packages/spiceypy/spi
      ceypy.py", line 59, in check_for_spice_error
          raise stypes.SpiceyError(msg)
      spiceypy.utils.support_types.SpiceyError:
      =====================================================================
      ===========

      Toolkit version: N0066

      SPICE(SPKINSUFFDATA) --

      Insufficient ephemeris data has been loaded to compute the state of -
      82 (CASSINI) relative to 0 (SOLAR SYSTEM BARYCENTER) at the ephemeris
       epoch 2004 JUN 11 19:33:04.184.

      spkezr_c --> SPKEZR --> SPKEZ --> SPKACS --> SPKGEO

      =====================================================================
      ===========

            This error is generated when trying to compute the apparent
            state of Phoebe as seen from CASSINI in the J2000 frame because
            despite both Phoebe and CASSINI ephemeris data being relative
            to the Saturn Barycenter, the state of the spacecraft with
            respect to the solar system barycenter is required to compute
            the light time and stellar aberrations. The loaded SPK data are
            enough to compute geometric states of CASSINI with respect to
            the Saturn Barycenter, and geometric states of Phoebe with
            respect to the Saturn Barycenter, but insufficient to compute
            the state of the spacecraft relative to the Solar System
            Barycenter because the SPK data needed to compute geometric
            states of Saturn Barycenter relative to the Solar System
            barycenter are no longer loaded. Run "brief" on the SPKs used
            in the original task to find out which ephemeris objects are
            available from those kernels. If you want to find out what is
            the 'center of motion' for the ephemeris object(s) included in
            an SPK, use the -c option when running "brief":


      BRIEF -- Version 4.0.0, September 8, 2010 -- Toolkit Version N0066


      Summary for: kernels/spk/981005_PLTEPH-DE405S.bsp

      Bodies: MERCURY BARYCENTER (1) w.r.t. SOLAR SYSTEM BARYCENTER (0)
              VENUS BARYCENTER (2) w.r.t. SOLAR SYSTEM BARYCENTER (0)
              EARTH BARYCENTER (3) w.r.t. SOLAR SYSTEM BARYCENTER (0)
              MARS BARYCENTER (4) w.r.t. SOLAR SYSTEM BARYCENTER (0)
              JUPITER BARYCENTER (5) w.r.t. SOLAR SYSTEM BARYCENTER (0)
              SATURN BARYCENTER (6) w.r.t. SOLAR SYSTEM BARYCENTER (0)
              URANUS BARYCENTER (7) w.r.t. SOLAR SYSTEM BARYCENTER (0)
              NEPTUNE BARYCENTER (8) w.r.t. SOLAR SYSTEM BARYCENTER (0)
              PLUTO BARYCENTER (9) w.r.t. SOLAR SYSTEM BARYCENTER (0)
              SUN (10) w.r.t. SOLAR SYSTEM BARYCENTER (0)
              MERCURY (199) w.r.t. MERCURY BARYCENTER (1)
              VENUS (299) w.r.t. VENUS BARYCENTER (2)
              MOON (301) w.r.t. EARTH BARYCENTER (3)
              EARTH (399) w.r.t. EARTH BARYCENTER (3)
              MARS (499) w.r.t. MARS BARYCENTER (4)
              Start of Interval (UTC)             End of Interval (UTC)
              -----------------------------       -------------------------
      ----
              2004-JUN-11 05:00:00.000            2004-JUN-12 12:00:00.000


      Summary for: kernels/spk/020514_SE_SAT105.bsp

      Bodies: MIMAS (601) w.r.t. SATURN BARYCENTER (6)
              ENCELADUS (602) w.r.t. SATURN BARYCENTER (6)
              TETHYS (603) w.r.t. SATURN BARYCENTER (6)
              DIONE (604) w.r.t. SATURN BARYCENTER (6)
              RHEA (605) w.r.t. SATURN BARYCENTER (6)
              TITAN (606) w.r.t. SATURN BARYCENTER (6)
              HYPERION (607) w.r.t. SATURN BARYCENTER (6)
              IAPETUS (608) w.r.t. SATURN BARYCENTER (6)
              PHOEBE (609) w.r.t. SATURN BARYCENTER (6)
              SATURN (699) w.r.t. SATURN BARYCENTER (6)
              Start of Interval (UTC)             End of Interval (UTC)
              -----------------------------       -------------------------
      ----
              2004-JUN-11 05:00:00.000            2004-JUN-12 12:00:00.000


      Summary for: kernels/spk/030201AP_SK_SM546_T45.bsp

      Body: CASSINI (-82) w.r.t. SATURN BARYCENTER (6)
            Start of Interval (UTC)             End of Interval (UTC)
            -----------------------------       ---------------------------
      --
            2004-JUN-11 05:00:00.000            2004-JUN-12 12:00:00.000



       2.   If you run your extended program with the original meta-kernel,
            the SPICE(SPKINSUFFDATA) error should be produced by the
            spiceypy.spkpos function because you have not loaded enough
            ephemeris data to compute the position of Jupiter with respect
            to Saturn. The loaded SPKs contain data for Saturn relative to
            the Solar System Barycenter, and for the Jupiter System
            Barycenter relative to the Solar System Barycenter, but the
            data for Jupiter relative to the Jupiter System Barycenter are
            missing:


         Additional kernels required for this task:

         File name                Contents
         -----------------------  ----------------------------------
         jup310_2004.bsp          Generic Jovian Satellite Ephemeris


         available in the NAIF server at:

      https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/satellites/


            Download the relevant SPK, add it to the meta-kernel and run
            again your extended program. The solution for the input UTC
            time "2004 jun 11 19:32:00" when using the downloaded Jovian
            Satellite Ephemeris SPK:

         Actual position of Jupiter as seen from Saturn in the
            J2000 frame (km):
            X =   -436016583.291
            Y =  -1094176737.323
            Z =   -446585337.431

       3.   When using 'NONE' aberration corrections, spiceypy.spkpos
            returns the geometric position of the target body relative to
            the observer. If 'LT' is used, the returned vector corresponds
            to the position of the target at the moment it emitted photons
            arriving at the observer at `et'. If 'LT+S' is used instead,
            the returned vector takes into account the observer's velocity
            relative to the solar system barycenter. The solution for the
            input UTC time "2004 jun 11 19:32:00" is:


         Actual (geometric) position of Sun as seen from Saturn in the
            J2000 frame (km):
            X =    367770592.367
            Y =  -1197330367.359
            Z =   -510369088.677
         Light-time corrected position of Sun as seen from Saturn in the
            J2000 frame (km):
            X =    367770572.921
            Y =  -1197330417.733
            Z =   -510369109.509
         Apparent position of Sun as seen from Saturn in the
            J2000 frame (km):
            X =    367726456.168
            Y =  -1197342627.879
            Z =   -510372252.747

Spacecraft Orientation and Reference Frames (xform)
---------------------------------------------------

.. _task-statement-rs-2:

Task Statement
^^^^^^^^^^^^^^

Write a program that prompts the user for an input time string, computes
and displays the following at the epoch of interest:

::

       1.   The apparent state of Phoebe as seen from CASSINI in the
            IAU_PHOEBE body-fixed frame. This vector itself is not of any
            particular interest, but it is a useful intermediate quantity
            in some geometry calculations.

       2.   The angular separation between the apparent position of Earth
            as seen from CASSINI and the nominal boresight of the CASSINI
            high gain antenna (HGA).

            The HGA boresight direction is provided by the kernel variable
            TKFRAME_-82101_BORESIGHT, which is defined in the Cassini frame
            kernel cited above in the section "Kernels Used." In this
            kernel, the HGA boresight vector is expressed relative to the
            CASSINI_HGA reference frame.

Use the program to compute these quantities at the epoch “2004 jun 11
19:32:00” UTC.

.. _learning-goals-2:

Learning Goals
^^^^^^^^^^^^^^

Familiarity with the different types of kernels involved in chaining
reference frames together, both inertial and non-inertial. Discover some
of the matrix and vector math functions. Understand the difference
between spiceypy.pxform and spiceypy.sxform.

.. _approach-2:

Approach
^^^^^^^^

The solution to the problem can be broken down into a series of simple
steps:

::

       --   Decide which SPICE kernels are necessary. Prepare a meta-kernel
            listing the kernels and load it into the program.

       --   Prompt the user for an input time string.

       --   Convert the input time string into ephemeris time expressed as
            seconds past J2000 TDB.

       --   Compute the state of Phoebe relative to CASSINI in the J2000
            reference frame, corrected for aberrations.

       --   Compute the state transformation matrix from J2000 to
            IAU_PHOEBE at the epoch, adjusted for light time.

       --   Multiply the state of Phoebe relative to CASSINI in the J2000
            reference frame by the state transformation matrix computed in
            the previous step.

       --   Compute the position of Earth relative to CASSINI in the J2000
            reference frame, corrected for aberrations.

       --   Determine what the nominal boresight of the CASSINI high gain
            antenna is by examining the frame kernel's content.

       --   Compute the rotation matrix from the CASSINI high gain antenna
            frame to J2000.

       --   Multiply the nominal boresight expressed in the CASSINI high
            gain antenna frame by the rotation matrix from the previous
            step.

       --   Compute the separation between the result of the previous step
            and the apparent position of the Earth relative to CASSINI in
            the J2000 frame.

HINT: Several of the steps above may be compressed into a single step
using SpiceyPy functions with which you are already familiar. The
"long way" presented above is intended to facilitate the introduction
of the functions spiceypy.pxform and spiceypy.sxform.

You may find it useful to consult the permuted index, the headers of
various source modules, and the following toolkit documentation:

::

       1.   Frames Required Reading (frames.req)

       2.   PCK Required Reading (pck.req)

       3.   SPK Required Reading (spk.req)

       4.   CK Required Reading (ck.req)

This particular example makes use of many of the different types of
SPICE kernels. You should spend a few moments thinking about which
kernels you will need and what data they provide.

.. _solution-2:

Solution
^^^^^^^^

Solution Meta-Kernel

The meta-kernel we created for the solution to this exercise is named
'xform.tm'. Its contents follow:

::

      KPL/MK

         This is the meta-kernel used in the solution of the "Spacecraft
         Orientation and Reference Frames" task in the Remote Sensing
         Hands On Lesson.

         The names and contents of the kernels referenced by this
         meta-kernel are as follows:

         File name                   Contents
         --------------------------  -----------------------------
         naif0008.tls                Generic LSK
         cas00084.tsc                Cassini SCLK
         981005_PLTEPH-DE405S.bsp    Solar System Ephemeris
         020514_SE_SAT105.bsp        Saturnian Satellite Ephemeris
         030201AP_SK_SM546_T45.bsp   Cassini Spacecraft SPK
         cas_v37.tf                  Cassini FK
         04135_04171pc_psiv2.bc      Cassini Spacecraft CK
         cpck05Mar2004.tpc           Cassini Project PCK


         \begindata
         KERNELS_TO_LOAD = ( 'kernels/lsk/naif0008.tls',
                             'kernels/sclk/cas00084.tsc',
                             'kernels/spk/981005_PLTEPH-DE405S.bsp',
                             'kernels/spk/020514_SE_SAT105.bsp',
                             'kernels/spk/030201AP_SK_SM546_T45.bsp',
                             'kernels/fk/cas_v37.tf',
                             'kernels/ck/04135_04171pc_psiv2.bc',
                             'kernels/pck/cpck05Mar2004.tpc' )
         \begintext

Solution Source Code

A sample solution to the problem follows:

::

      #
      # Solution xform.py
      #
      from __future__ import print_function
      from builtins import input

      import spiceypy

      def xform():
          #
          # Local parameters
          #
          METAKR = 'xform.tm'

          #
          # Load the kernels that this program requires.  We
          # will need:
          #
          #    A leapseconds kernel
          #    A spacecraft clock kernel for CASSINI
          #    The necessary ephemerides
          #    A planetary constants file (PCK)
          #    A spacecraft orientation kernel for CASSINI (CK)
          #    A frame kernel (TF)
          #
          spiceypy.furnsh( METAKR )

          #
          #  Prompt the user for the input time string.
          #
          utctim = input( 'Input UTC Time: ' )

          print( 'Converting UTC Time: {:s}'.format(utctim)  )

          #
          #Convert utctim to ET.
          #
          et = spiceypy.str2et( utctim )

          print( '   ET seconds past J2000: {:16.3f}'.format(et) )

          #
          # Compute the apparent state of Phoebe as seen from
          # CASSINI in the J2000 frame.
          #
          [state, ltime] = spiceypy.spkezr( 'PHOEBE', et,      'J2000',
                                            'LT+S',   'CASSINI'       )
          #
          # Now obtain the transformation from the inertial
          # J2000 frame to the non-inertial body-fixed IAU_PHOEBE
          # frame.  Since we want the apparent position, we
          # need to subtract ltime from et.
          #
          sform = spiceypy.sxform( 'J2000', 'IAU_PHOEBE', et-ltime )

          #
          # Now rotate the apparent J2000 state into IAU_PHOEBE
          # with the following matrix multiplication:
          #
          bfixst = spiceypy.mxvg ( sform, state, 6, 6 )

          #
          # Display the results.
          #
          print( '   Apparent state of Phoebe as seen '
                 'from CASSINI in the IAU_PHOEBE\n'
                 '      body-fixed frame (km, km/s):'      )
          print( '      X = {:19.6f}'.format(bfixst[0])    )
          print( '      Y = {:19.6f}'.format(bfixst[1])    )
          print( '      Z = {:19.6f}'.format(bfixst[2])    )
          print( '     VX = {:19.6f}'.format(bfixst[3])    )
          print( '     VY = {:19.6f}'.format(bfixst[4])    )
          print( '     VZ = {:19.6f}'.format(bfixst[5])    )

          #
          # It is worth pointing out, all of the above could
          #  have been done with a single use of spkezr:
          #
          [state, ltime] = spiceypy.spkezr(
                              'PHOEBE', et,      'IAU_PHOEBE',
                              'LT+S',   'CASSINI'              )
          #
          # Display the results.
          #
          print( '   Apparent state of Phoebe as seen '
                 'from CASSINI in the IAU_PHOEBE\n'
                 '      body-fixed frame (km, km/s) '
                 'obtained using spkezr directly:'        )
          print( '      X = {:19.6f}'.format(state[0])    )
          print( '      Y = {:19.6f}'.format(state[1])    )
          print( '      Z = {:19.6f}'.format(state[2])    )
          print( '     VX = {:19.6f}'.format(state[3])    )
          print( '     VY = {:19.6f}'.format(state[4])    )
          print( '     VZ = {:19.6f}'.format(state[5])    )

          #
          # Note that the velocity found by using spkezr
          # to compute the state in the IAU_PHOEBE frame differs
          # at the few mm/second level from that found previously
          # by calling spkezr and then sxform. Computing
          # velocity via a single call to spkezr as we've
          # done immediately above is slightly more accurate because
          # it accounts for the effect of the rate of change of
          # light time on the apparent angular velocity of the
          # target's body-fixed reference frame.
          #
          # Now we are to compute the angular separation between
          # the apparent position of the Earth as seen from the
          # orbiter and the nominal boresight of the high gain
          # antenna.  First, compute the apparent position of
          # the Earth as seen from CASSINI in the J2000 frame.
          #
          [pos, ltime] = spiceypy.spkpos( 'EARTH', et,      'J2000',
                                          'LT+S',  'CASSINI'        )

          #
          # Now compute the location of the antenna boresight
          # at this same epoch.  From reading the frame kernel
          # we know that the antenna boresight is nominally the
          # +Z axis of the CASSINI_HGA frame defined there.
          #
          bsight = [ 0.0, 0.0, 1.0]

          #
          # Now compute the rotation matrix from CASSINI_HGA into
          # J2000.
          #
          pform = spiceypy.pxform( 'CASSINI_HGA', 'J2000', et )

          #
          # And multiply the result to obtain the nominal
          # antenna boresight in the J2000 reference frame.
          #
          bsight = spiceypy.mxv( pform, bsight )

          #
          # Lastly compute the angular separation.
          #
          sep =  spiceypy.convrt( spiceypy.vsep(bsight, pos),
                                  'RADIANS', 'DEGREES'       )

          print( '   Angular separation between the '
                 'apparent position of\n'
                 '      Earth and the CASSINI high '
                 'gain antenna boresight (degrees):\n'
                 '      {:16.3f}'.format(sep)        )

          #
          # Or alternatively we can work in the antenna
          # frame directly.
          #
          [pos, ltime] = spiceypy.spkpos(
                            'EARTH', et,      'CASSINI_HGA',
                            'LT+S',  'CASSINI'               )

          #
          # The antenna boresight is the Z-axis in the
          # CASSINI_HGA frame.
          #
          bsight = [ 0.0, 0.0, 1.0 ]

          #
          # Lastly compute the angular separation.
          #
          sep =  spiceypy.convrt( spiceypy.vsep(bsight, pos),
                                  'RADIANS', 'DEGREES'       )

          print( '   Angular separation between the '
                 'apparent position of\n'
                 '      Earth and the CASSINI high '
                 'gain antenna boresight computed\n'
                 '      using vectors in the CASSINI_HGA '
                 'frame (degrees):\n'
                 '      {:16.3f}'.format(sep)            )

          spiceypy.unload( METAKR )

      if __name__ == '__main__':
          xform()

Solution Sample Output

Execute the program:

::

      Input UTC Time: 2004 jun 11 19:32:00
      Converting UTC Time: 2004 jun 11 19:32:00
         ET seconds past J2000:    140254384.185
         Apparent state of Phoebe as seen from CASSINI in the IAU_PHOEBE
            body-fixed frame (km, km/s):
            X =        -1982.639762
            Y =         -934.530471
            Z =         -166.562595
           VX =            3.970833
           VY =           -3.812498
           VZ =           -2.371663
         Apparent state of Phoebe as seen from CASSINI in the IAU_PHOEBE
            body-fixed frame (km, km/s) obtained using spkezr directly:
            X =        -1982.639762
            Y =         -934.530471
            Z =         -166.562595
           VX =            3.970832
           VY =           -3.812496
           VZ =           -2.371663
         Angular separation between the apparent position of
            Earth and the CASSINI high gain antenna boresight (degrees):
                      71.924
         Angular separation between the apparent position of
            Earth and the CASSINI high gain antenna boresight computed
            using vectors in the CASSINI_HGA frame (degrees):
                      71.924

.. _extra-credit-2:

Extra Credit
^^^^^^^^^^^^

In this "extra credit" section you will be presented with more
complex tasks, aimed at improving your understanding of frame
transformations, and some common errors that may happen when computing
them.

These "extra credit" tasks are provided as task statements, and
unlike the regular tasks, no approach or solution source code is
provided. In the next section, you will find the numeric solutions (when
applicable) and answers to the questions asked in these tasks.

Task statements and questions

::

       1.   Run the original program using the input UTC time "2004 jun 11
            18:25:00". Explain what happens.

       2.   Compute the angular separation between the apparent position of
            the Sun as seen from CASSINI and the nominal boresight of the
            CASSINI high gain antenna (HGA). Is the HGA illuminated?

Solutions and answers

::

       1.   When running the original software using as input the UTC time
            string "2004 jun 11 18:25:00":

      Traceback (most recent call last):
        File "xform.py", line 183, in <module>
          xform()
        File "xform.py", line 130, in xform
          pform = spiceypy.pxform( 'CASSINI_HGA', 'J2000', et )
        File "/home/bsemenov/local/lib/python3.5/site-packages/spiceypy/spi
      ceypy.py", line 76, in with_errcheck
          check_for_spice_error(f)
        File "/home/bsemenov/local/lib/python3.5/site-packages/spiceypy/spi
      ceypy.py", line 59, in check_for_spice_error
          raise stypes.SpiceyError(msg)
      spiceypy.utils.support_types.SpiceyError:
      =====================================================================
      ===========

      Toolkit version: N0066

      SPICE(NOFRAMECONNECT) --

      At epoch 1.4025036418463E+08 TDB (2004 JUN 11 18:26:04.184 TDB), ther
      e is insufficient information available to transform from reference f
      rame -82101 (CASSINI_HGA) to reference frame 1 (J2000). Frame CASSINI
      _HGA could be transformed to frame -82000 (CASSINI_SC_COORD). The lat
      ter is a CK frame; a CK file containing data

      pxform_c --> PXFORM --> REFCHG

      =====================================================================
      ===========

            spiceypy.pxform returns the SPICE(NOFRAMECONNECT) error, which
            indicates that there are not sufficient data to perform the
            transformation from the CASSINI_HGA frame to J2000 at the
            requested epoch. If you summarize the CASSINI spacecraft CK
            using the "ckbrief" utility program with the -dump option
            (display interpolation intervals boundaries) you will find that
            the CK contains gaps within its segment:


      CKBRIEF -- Version 6.1.0, June 27, 2014 -- Toolkit Version N0066


      Summary for: kernels/ck/04135_04171pc_psiv2.bc

      Segment No.: 1

      Object:  -82000
        Interval Begin UTC       Interval End UTC         AV
        ------------------------ ------------------------ ---
        2004-JUN-11 05:00:00.000 2004-JUN-11 09:25:02.019 Y
        2004-JUN-11 09:26:14.019 2004-JUN-11 18:24:37.152 Y
        2004-JUN-11 18:26:13.152 2004-JUN-12 05:53:26.012 Y
        2004-JUN-12 05:54:56.012 2004-JUN-12 10:32:08.016 Y
        2004-JUN-12 10:33:26.016 2004-JUN-12 11:59:59.998 Y



            whereas if you had used ckbrief without -dump you would have
            gotten the following information (only CK segment begin/end
            times):


      CKBRIEF -- Version 6.1.0, June 27, 2014 -- Toolkit Version N0066


      Summary for: kernels/ck/04135_04171pc_psiv2.bc

      Object:  -82000
        Interval Begin UTC       Interval End UTC         AV
        ------------------------ ------------------------ ---
        2004-JUN-11 05:00:00.000 2004-JUN-12 11:59:59.998 Y



            which has insufficient detail to reveal the problem.

       2.   By computing the apparent position of the Sun as seen from
            CASSINI in the CASSINI_HGA frame, and the angular separation
            between this vector and the nominal boresight of the CASSINI
            high gain antenna (+Z-axis of the CASSINI_HGA frame), you will
            find whether the HGA is illuminated. The solution for the input
            UTC time "2004 jun 11 19:32:00" is:

      Angular separation between the apparent position of the Sun and the
      nominal boresight of the CASSINI high gain antenna (degrees):
           73.130

      HGA illumination:
         CASSINI high gain antenna IS illuminated.

            since the angular separation is smaller than 90 degrees.

Computing Sub-s/c and Sub-solar Points on an Ellipsoid and a DSK (subpts)
-------------------------------------------------------------------------

.. _task-statement-rs-3:

Task Statement
^^^^^^^^^^^^^^

Write a program that prompts the user for an input UTC time string and
computes the following quantities at that epoch:

::

       1.   The apparent sub-observer point of CASSINI on Phoebe, in the
            body fixed frame IAU_PHOEBE, in kilometers.

       2.   The apparent sub-solar point on Phoebe, as seen from CASSINI in
            the body fixed frame IAU_PHOEBE, in kilometers.

The program computes each point twice: once using an ellipsoidal shape
model and the

::

           near point/ellipsoid

definition, and once using a DSK shape model and the

::

           nadir/dsk/unprioritized

definition.

The program displays the results. Use the program to compute these
quantities at “2004 jun 11 19:32:00” UTC.

.. _learning-goals-3:

Learning Goals
^^^^^^^^^^^^^^

Discover higher level geometry calculation functions in SpiceyPy and
their usage as it relates to CASSINI.

.. _approach-3:

Approach
^^^^^^^^

This particular problem is more of an exercise in searching the permuted
index to find the appropriate functions and then reading their headers
to understand how to call them.

One point worth considering: how would the results change if the
sub-solar and sub-observer points were computed using the

::

           intercept/ellipsoid

and

::

           intercept/dsk/unprioritized

definitions? Which definition is appropriate?

.. _solution-3:

Solution
^^^^^^^^

Solution Meta-Kernel

The meta-kernel we created for the solution to this exercise is named
'subpts.tm'. Its contents follow:

::

      KPL/MK

         This is the meta-kernel used in the solution of the
         "Computing Sub-spacecraft and Sub-solar Points" task
         in the Remote Sensing Hands On Lesson.

         The names and contents of the kernels referenced by this
         meta-kernel are as follows:

         File name                   Contents
         --------------------------  -----------------------------
         naif0008.tls                Generic LSK
         981005_PLTEPH-DE405S.bsp    Solar System Ephemeris
         020514_SE_SAT105.bsp        Saturnian Satellite Ephemeris
         030201AP_SK_SM546_T45.bsp   Cassini Spacecraft SPK
         cpck05Mar2004.tpc           Cassini Project PCK
         phoebe_64q.bds              Phoebe DSK


         \begindata
         KERNELS_TO_LOAD = ( 'kernels/lsk/naif0008.tls',
                             'kernels/spk/981005_PLTEPH-DE405S.bsp',
                             'kernels/spk/020514_SE_SAT105.bsp',
                             'kernels/spk/030201AP_SK_SM546_T45.bsp',
                             'kernels/pck/cpck05Mar2004.tpc'
                             'kernels/dsk/phoebe_64q.bds' )

         \begintext

Solution Source Code

A sample solution to the problem follows:

::

      #
      # Solution subpts.py
      #
      from __future__ import print_function
      from builtins import input

      #
      # SpiceyPy package:
      #
      import spiceypy

      def subpts():
          #
          # Local parameters
          #
          METAKR = 'subpts.tm'

          #
          # Load the kernels that this program requires.  We
          # will need:
          #
          #    A leapseconds kernel
          #    The necessary ephemerides
          #    A planetary constants file (PCK)
          #    A DSK file containing Phoebe shape data
          #
          spiceypy.furnsh( METAKR )

          #
          #Prompt the user for the input time string.
          #
          utctim = input( 'Input UTC Time: ' )

          print( ' Converting UTC Time: {:s}'.format(utctim)  )

          #
          #Convert utctim to ET.
          #
          et = spiceypy.str2et( utctim )

          print( '   ET seconds past J2000: {:16.3f}'.format(et) )

          for  i  in range(2):

              if  i  == 0:
                  #
                  # Use the "near point" sub-point definition
                  # and an ellipsoidal model.
                  #
                  method = 'NEAR POINT/Ellipsoid'

              else:
                  #
                  # Use the "nadir" sub-point definition
                  # and a DSK model.
                  #
                  method = 'NADIR/DSK/Unprioritized'

              print( '\n Sub-point/target shape model: {:s}\n'.format(
                  method )  )

              #
              # Compute the apparent sub-observer point of CASSINI
              # on Phoebe.
              #
              [spoint, trgepc, srfvec] = spiceypy.subpnt(
                                      method,       'PHOEBE',  et,
                                      'IAU_PHOEBE', 'LT+S', 'CASSINI' )

              print( '   Apparent sub-observer point of CASSINI '
                     'on Phoebe in the\n'
                     '   IAU_PHOEBE frame (km):' )
              print( '      X = {:16.3f}'.format(spoint[0])              )
              print( '      Y = {:16.3f}'.format(spoint[1])              )
              print( '      Z = {:16.3f}'.format(spoint[2])              )
              print( '    ALT = {:16.3f}'.format(spiceypy.vnorm(srfvec)) )

              #
              # Compute the apparent sub-solar point on Phoebe
              # as seen from CASSINI.
              #
              [spoint, trgepc, srfvec] = spiceypy.subslr(
                              method,       'PHOEBE',  et,
                              'IAU_PHOEBE', 'LT+S', 'CASSINI' )

              print( '   Apparent sub-solar point on Phoebe '
                     'as seen from CASSINI in\n'
                     '   the IAU_PHOEBE frame (km):'  )
              print( '      X = {:16.3f}'.format(spoint[0])   )
              print( '      Y = {:16.3f}'.format(spoint[1])   )
              print( '      Z = {:16.3f}'.format(spoint[2])   )

          #
          # End of computation block for "method"
          #
          print( " )

          spiceypy.unload( METAKR )

      if __name__ == '__main__':
          subpts()

Solution Sample Output

Execute the program:

::

      Input UTC Time: 2004 jun 11 19:32:00
       Converting UTC Time: 2004 jun 11 19:32:00
         ET seconds past J2000:    140254384.185

       Sub-point/target shape model: NEAR POINT/Ellipsoid

         Apparent sub-observer point of CASSINI on Phoebe in the
         IAU_PHOEBE frame (km):
            X =          104.498
            Y =           45.269
            Z =            7.383
          ALT =         2084.116
         Apparent sub-solar point on Phoebe as seen from CASSINI in
         the IAU_PHOEBE frame (km):
            X =           78.681
            Y =           76.879
            Z =          -21.885

       Sub-point/target shape model: NADIR/DSK/Unprioritized

         Apparent sub-observer point of CASSINI on Phoebe in the
         IAU_PHOEBE frame (km):
            X =           95.373
            Y =           40.948
            Z =            6.610
          ALT =         2094.242
         Apparent sub-solar point on Phoebe as seen from CASSINI in
         the IAU_PHOEBE frame (km):
            X =           79.111
            Y =           77.338
            Z =          -22.028

.. _extra-credit-3:

Extra Credit
^^^^^^^^^^^^^

In this "extra credit" section you will be presented with more
complex tasks, aimed at improving your understanding of spiceypy.subpnt
and spiceypy.subslr functions.

These "extra credit" tasks are provided as task statements, and
unlike the regular tasks, no approach or solution source code is
provided. In the next section, you will find the numeric solutions (when
applicable) and answers to the questions asked in these tasks.

Task statements and questions

::

       1.   Recompute the apparent sub-solar point on Phoebe as seen from
            CASSINI in the body fixed frame IAU_PHOEBE in kilometers using
            the 'Intercept/ellipsoid' method at "2004 jun 11 19:32:00".
            Explain the differences.

       2.   Compute the geometric sub-spacecraft point of CASSINI on Phoebe
            in the body fixed frame IAU_PHOEBE in kilometers using the
            'Near point/ellipsoid' method at "2004 jun 11 19:32:00".

       3.   Transform the sub-spacecraft Cartesian coordinates obtained in
            the previous task to planetocentric and planetographic
            coordinates. When computing planetographic coordinates,
            retrieve Phoebe's radii by calling spiceypy.bodvrd and use the
            first element of the returned radii values as Phoebe's
            equatorial radius. Explain why planetocentric and
            planetographic latitudes and longitudes are different. Explain
            why the planetographic altitude for a point on the surface of
            Phoebe is not zero and whether this is correct or not.

Solutions and answers

::

       1.   The differences observed are due to the computation method. The
            "Intercept/ellipsoid" method defines the sub-solar point as
            the target surface intercept of the line containing the Sun and
            the target's center, while the "Near point/ellipsoid" method
            defines the sub-solar point as the the nearest point on the
            target relative to the Sun. Since Phoebe is not spherical,
            these two points are not the same:

         Apparent sub-solar point on Phoebe as seen from CASSINI in
         the IAU_PHOEBE frame using the 'Near Point: ellipsoid' method
         (km):
            X =           78.681
            Y =           76.879
            Z =          -21.885

         Apparent sub-solar point on Phoebe as seen from CASSINI in
         the IAU_PHOEBE frame using the 'Intercept: ellipsoid' method
         (km):
            X =           74.542
            Y =           79.607
            Z =          -24.871

       2.   The geometric sub-spacecraft point of CASSINI on Phoebe in the
            body fixed frame IAU_PHOEBE in kilometers at "2004 jun 11
            19:32:00" UTC epoch is:

         Geometric sub-spacecraft point of CASSINI on Phoebe in
         the IAU_PHOEBE frame using the 'Near Point: ellipsoid' method
         (km):
            X =          104.497
            Y =           45.270
            Z =            7.384

       3.   The sub-spacecraft point of CASSINI on Phoebe in planetocentric
            and planetographic coordinates at "2004 jun 11 19:32:00" UTC
            epoch is:

         Planetocentric coordinates of the CASSINI
         sub-spacecraft point on Phoebe (degrees, km):
         LAT =            3.710
         LON =           23.423
         R   =          114.121

         Planetographic coordinates of the CASSINI
         sub-spacecraft point on Phoebe (degrees, km):
         LAT =            4.454
         LON =          336.577
         ALT =           -0.831

            The planetocentric and planetographic longitudes are different
            ("graphic" = 360 - "centric") because planetographic
            longitudes on Phoebe are measured positive west as defined by
            Phoebe's rotation direction.

            The planetocentric and planetographic latitudes are different
            because the planetocentric latitude was computed as the angle
            between the direction from the center of the body to the point
            and the equatorial plane, while the planetographic latitude was
            computed as the angle between the surface normal at the point
            and the equatorial plane.

            The planetographic altitude is non zero because it was computed
            using a different and incorrect Phoebe surface model: a
            spheroid with equal equatorial radii. The surface point
            returned by spiceypy.subpnt was computed by treating Phoebe as
            a triaxial ellipsoid with different equatorial radii. The
            planetographic latitude is also incorrect because it is based
            on the normal to the surface of the spheroid rather than the
            ellipsoid, In general planetographic coordinates cannot be used
            for bodies with shapes modeled as triaxial ellipsoids.

Intersecting Vectors with an Ellipsoid and a DSK (fovint)
---------------------------------------------------------

.. _task-statement-rs-4:

Task Statement
^^^^^^^^^^^^^^

Write a program that prompts the user for an input UTC time string and,
for that time, computes the intersection of the CASSINI ISS NAC camera
boresight and field of view (FOV) boundary vectors with the surface of
Phoebe. Compute each intercept twice: once with Phoebe's shape modeled
as an ellipsoid, and once with Phoebe's shape modeled by DSK data. The
program presents each point of intersection as

::

       1.   A Cartesian vector in the IAU_PHOEBE frame

       2.   Planetocentric (latitudinal) coordinates in the IAU_PHOEBE
            frame.

For each of the camera FOV boundary and boresight vectors, if an
intersection is found, the program displays the results of the above
computations, otherwise it indicates no intersection exists.

At each point of intersection compute the following:

::

       3.   Phase angle

       4.   Solar incidence angle

       5.   Emission angle

These angles should be computed using both ellipsoidal and DSK shape
models.

Additionally compute the local solar time at the intercept of the camera
boresight with the surface of Phoebe, using both ellipsoidal and DSK
shape models.

Use this program to compute values at the epoch:

::

            "2004 jun 11 19:32:00" UTC

.. _learning-goals-4:

Learning Goals
^^^^^^^^^^^^^^

Understand how field of view parameters are retrieved from instrument
kernels. Learn how various standard planetary constants are retrieved
from text PCKs. Discover how to compute the intersection of field of
view vectors with target bodies whose shapes are modeled as ellipsoids
or provided by DSKs. Discover another high level geometry function and
another time conversion function in SpiceyPy.

.. _approach-4:

Approach
^^^^^^^^

This problem can be broken down into several simple, small steps:

::

       --   Decide which SPICE kernels are necessary. Prepare a meta-kernel
            listing the kernels and load it into the program. Remember, you
            will need to find a kernel with information about the CASSINI
            NAC camera.

       --   Prompt the user for an input time string.

       --   Convert the input time string into ephemeris time expressed as
            seconds past J2000 TDB.

       --   Retrieve the FOV (field of view) configuration for the CASSINI
            NAC camera.

For each vector in the set of boundary corner vectors, and for the
boresight vector, perform the following operations:

::

       --   Compute the intercept of the vector with Phoebe modeled as an
            ellipsoid or using DSK data

       --   If this intercept is found, convert the position vector of the
            intercept into planetocentric coordinates.

            Then compute the phase, solar incidence, and emission angles at
            the intercept. Otherwise indicate to the user no intercept was
            found for this vector.

       --   Compute the planetocentric longitude of the boresight
            intercept.

Finally

::

       --   Compute the local solar time at the boresight intercept
            longitude on a 24-hour clock. The input time for this
            computation should be the TDB observation epoch minus one-way
            light time from the boresight intercept to the spacecraft.

It may be useful to consult the CASSINI ISS instrument kernel to
determine the name of the NAC camera as well as its configuration. This
exercise may make use of some of the concepts and (loosely) code from
the "Spacecraft Orientation and Reference Frames" task.

.. _solution-4:

Solution
^^^^^^^^

Solution Meta-Kernel

The meta-kernel we created for the solution to this exercise is named
'fovint.tm'. Its contents follow:

::

      KPL/MK

         This is the meta-kernel used in the solution of the
         "Intersecting Vectors with a Triaxial Ellipsoid" task
         in the Remote Sensing Hands On Lesson.

         The names and contents of the kernels referenced by this
         meta-kernel are as follows:

         File name                   Contents
         --------------------------  -----------------------------
         naif0008.tls                Generic LSK
         cas00084.tsc                Cassini SCLK
         981005_PLTEPH-DE405S.bsp    Solar System Ephemeris
         020514_SE_SAT105.bsp        Saturnian Satellite Ephemeris
         030201AP_SK_SM546_T45.bsp   Cassini Spacecraft SPK
         cas_v37.tf                  Cassini FK
         04135_04171pc_psiv2.bc      Cassini Spacecraft CK
         cpck05Mar2004.tpc           Cassini Project PCK
         cas_iss_v09.ti              ISS Instrument Kernel
         phoebe_64q.bds              Phoebe DSK


         \begindata
         KERNELS_TO_LOAD = ( 'kernels/lsk/naif0008.tls',
                             'kernels/sclk/cas00084.tsc',
                             'kernels/spk/981005_PLTEPH-DE405S.bsp',
                             'kernels/spk/020514_SE_SAT105.bsp',
                             'kernels/spk/030201AP_SK_SM546_T45.bsp',
                             'kernels/fk/cas_v37.tf',
                             'kernels/ck/04135_04171pc_psiv2.bc',
                             'kernels/pck/cpck05Mar2004.tpc',
                             'kernels/ik/cas_iss_v09.ti'
                             'kernels/dsk/phoebe_64q.bds' )
         \begintext

Solution Source Code

A sample solution to the problem follows:

::

      #
      # Solution fovint.py
      #
      from __future__ import print_function
      from builtins import input

      #
      # SpiceyPy package:
      #
      import spiceypy
      from spiceypy.utils.support_types import SpiceyError

      def fovint():
          #
          # Local parameters
          #
          METAKR = 'fovint.tm'
          ROOM   = 4

          #
          # Load the kernels that this program requires.  We
          # will need:
          #
          #    A leapseconds kernel.
          #    A SCLK kernel for CASSINI.
          #    Any necessary ephemerides.
          #    The CASSINI frame kernel.
          #    A CASSINI C-kernel.
          #    A PCK file with Phoebe constants.
          #    The CASSINI ISS I-kernel.
          #    A DSK file containing Phoebe shape data.
          #
          spiceypy.furnsh( METAKR )

          #
          #Prompt the user for the input time string.
          #
          utctim = input( 'Input UTC Time: ' )

          print( 'Converting UTC Time: {:s}'.format(utctim)  )

          #
          #Convert utctim to ET.
          #
          et = spiceypy.str2et( utctim )

          print( '  ET seconds past J2000: {:16.3f}\n'.format(et) )

          #
          # Now we need to obtain the FOV configuration of
          # the ISS NAC camera.  To do this we will need the
          # ID code for CASSINI_ISS_NAC.
          #
          try:
              nacid = spiceypy.bodn2c( 'CASSINI_ISS_NAC' )

          except SpiceyError:
              #
              # Stop the program if the code was not found.
              #
              print( 'Unable to locate the ID code for '
                         'CASSINI_ISS_NAC'               )
              raise

          #
          # Now retrieve the field of view parameters.
          #
          [ shape,  insfrm,
            bsight, n,      bounds ] = spiceypy.getfov( nacid, ROOM )

          #
          # `bounds' is a numpy array. We'll convert it to a list.
          #
          # Rather than treat BSIGHT as a separate vector,
          # copy it into the last slot of BOUNDS.
          #
          bounds = bounds.tolist()
          bounds.append( bsight )

          #
          # Set vector names to be used for output.
          #
          vecnam = [ 'Boundary Corner 1',
                     'Boundary Corner 2',
                     'Boundary Corner 3',
                     'Boundary Corner 4',
                     'Cassini NAC Boresight' ]

          #
          # Set values of "method" string that specify use of
          # ellipsoidal and DSK (topographic) shape models.
          #
          # In this case, we can use the same methods for calls to both
          # spiceypy.sincpt and spiceypy.ilumin. Note that some SPICE
          # routines require different "method" inputs from those
          # shown here. See the API documentation of each routine
          # for details.
          #
          method = [ 'Ellipsoid', 'DSK/Unprioritized']

          #
          # Get ID code of Phoebe. We'll use this ID code later, when we
          # compute local solar time.
          #
          try:
              phoeid = spiceypy.bodn2c( 'PHOEBE' )
          except:
              #
              # The ID code for PHOEBE is built-in to the library.
              # However, it is good programming practice to get
              # in the habit of handling exceptions that may
              # be thrown when a quantity is not found.
              #
              print( 'Unable to locate the body ID code '
                     'for Phoebe.'                       )
              raise

          #
          # Now perform the same set of calculations for each
          # vector listed in the BOUNDS array. Use both
          # ellipsoidal and detailed (DSK) shape models.
          #
          for i  in  range(5):
              #
              # Call sincpt to determine coordinates of the
              # intersection of this vector with the surface
              # of Phoebe.
              #
              print( 'Vector: {:s}\n'.format( vecnam[i] ) )

              for  j  in range(2):

                  print ( ' Target shape model: {:s}\n'.format(
                                               method[j]      )  )
                  try:

                      [point, trgepc, srfvec ] = spiceypy.sincpt(
                          method[j],    'PHOEBE',  et,
                          'IAU_PHOEBE', 'LT+S',    'CASSINI',
                          insfrm,       bounds[i]               )

                      #
                      # Now, we have discovered a point of intersection.
                      # Start by displaying the position vector in the
                      # IAU_PHOEBE frame of the intersection.
                      #
                      print( '  Position vector of surface intercept '
                             'in the IAU_PHOEBE frame (km):'           )
                      print( '     X   = {:16.3f}'.format( point[0] )  )
                      print( '     Y   = {:16.3f}'.format( point[1] )  )
                      print( '     Z   = {:16.3f}'.format( point[2] )  )

                      #
                      # Display the planetocentric latitude and longitude
                      # of the intercept.
                      #
                      [radius, lon, lat] = spiceypy.reclat( point )

                      print( '  Planetocentric coordinates of '
                             'the intercept (degrees):'          )
                      print( '     LAT = {:16.3f}'.format(
                                         lat * spiceypy.dpr() )  )
                      print( '     LON = {:16.3f}'.format(
                                         lon * spiceypy.dpr() )  )
                      #
                      # Compute the illumination angles at this
                      # point.
                      #
                      [ trgepc, srfvec, phase, solar,      \
                        emissn, visibl, lit           ] =  \
                           spiceypy.illumf(
                               method[j],   'PHOEBE', 'SUN',     et,
                              'IAU_PHOEBE', 'LT+S',   'CASSINI', point )

                      print( '  Phase angle (degrees):           '
                             '{:16.3f}'.format( phase*spiceypy.dpr() )  )
                      print( '  Solar incidence angle (degrees): '
                             '{:16.3f}'.format( solar*spiceypy.dpr() )  )
                      print( '  Emission angle (degrees):        '
                             '{:16.3f}'.format( emissn*spiceypy.dpr())  )
                      print( '  Observer visible:  {:s}'.format(
                          str(visibl) )  )
                      print( '  Sun visible:       {:s}'.format(
                          str(lit)    )  )

                      if  i  ==  4:
                          #
                          # Compute local solar time corresponding
                          # to the light time corrected TDB epoch
                          # at the boresight intercept.
                          #
                          [hr, mn, sc, time, ampm] = spiceypy.et2lst(
                              trgepc,
                              phoeid,
                              lon,
                              'PLANETOCENTRIC' )

                          print( '\n  Local Solar Time at boresight '
                                 'intercept (24 Hour Clock):\n'
                                 '     {:s}'.format( time )       )
                      #
                      # End of LST computation block.
                      #

                  except SpiceyError as exc:
                      #
                      # Display a message if an exception was thrown.
                      # For simplicity, we treat this as an indication
                      # that the point of intersection was not found,
                      # although it could be due to other errors.
                      # Otherwise, continue with the calculations.
                      #
                      print( 'Exception message is: {:s}'.format(
                                exc.value ))
                  #
                  # End of SpiceyError try-catch block.
                  #
                  print( " )
              #
              # End of target shape model loop.
              #
          #
          # End of vector loop.
          #

          spiceypy.unload( METAKR )

      if __name__ == '__main__':
           fovint()

Solution Sample Output

Execute the program:

::

      Input UTC Time: 2004 jun 11 19:32:00
      Converting UTC Time: 2004 jun 11 19:32:00
        ET seconds past J2000:    140254384.185

      Vector: Boundary Corner 1

       Target shape model: Ellipsoid

        Position vector of surface intercept in the IAU_PHOEBE frame (km):
           X   =           91.026
           Y   =           67.190
           Z   =            2.030
        Planetocentric coordinates of the intercept (degrees):
           LAT =            1.028
           LON =           36.432
        Phase angle (degrees):                     28.110
        Solar incidence angle (degrees):           16.121
        Emission angle (degrees):                  14.627
        Observer visible:  true
        Sun visible:       true

       Target shape model: DSK/Unprioritized

        Position vector of surface intercept in the IAU_PHOEBE frame (km):
           X   =           78.770
           Y   =           61.570
           Z   =            0.964
        Planetocentric coordinates of the intercept (degrees):
           LAT =            0.552
           LON =           38.013
        Phase angle (degrees):                     28.110
        Solar incidence angle (degrees):           31.132
        Emission angle (degrees):                  16.539
        Observer visible:  true
        Sun visible:       true

      Vector: Boundary Corner 2

       Target shape model: Ellipsoid

        Position vector of surface intercept in the IAU_PHOEBE frame (km):
           X   =           89.991
           Y   =           66.726
           Z   =           14.733
        Planetocentric coordinates of the intercept (degrees):
           LAT =            7.492
           LON =           36.556
        Phase angle (degrees):                     27.894
        Solar incidence angle (degrees):           22.894
        Emission angle (degrees):                  14.988
        Observer visible:  true
        Sun visible:       true

       Target shape model: DSK/Unprioritized

        Position vector of surface intercept in the IAU_PHOEBE frame (km):
           X   =           76.586
           Y   =           60.579
           Z   =           13.657
        Planetocentric coordinates of the intercept (degrees):
           LAT =            7.962
           LON =           38.344
        Phase angle (degrees):                     27.894
        Solar incidence angle (degrees):           32.013
        Emission angle (degrees):                  11.845
        Observer visible:  true
        Sun visible:       true

      Vector: Boundary Corner 3

       Target shape model: Ellipsoid

        Position vector of surface intercept in the IAU_PHOEBE frame (km):
           X   =           80.963
           Y   =           76.643
           Z   =           14.427
        Planetocentric coordinates of the intercept (degrees):
           LAT =            7.373
           LON =           43.430
        Phase angle (degrees):                     28.171
        Solar incidence angle (degrees):           21.315
        Emission angle (degrees):                  21.977
        Observer visible:  true
        Sun visible:       true

       Target shape model: DSK/Unprioritized

        Position vector of surface intercept in the IAU_PHOEBE frame (km):
           X   =           68.677
           Y   =           71.100
           Z   =           13.444
        Planetocentric coordinates of the intercept (degrees):
           LAT =            7.745
           LON =           45.993
        Phase angle (degrees):                     28.171
        Solar incidence angle (degrees):           36.039
        Emission angle (degrees):                  14.474
        Observer visible:  true
        Sun visible:       true

      Vector: Boundary Corner 4

       Target shape model: Ellipsoid

        Position vector of surface intercept in the IAU_PHOEBE frame (km):
           X   =           81.997
           Y   =           77.106
           Z   =            1.698
        Planetocentric coordinates of the intercept (degrees):
           LAT =            0.865
           LON =           43.239
        Phase angle (degrees):                     28.385
        Solar incidence angle (degrees):           13.882
        Emission angle (degrees):                  21.763
        Observer visible:  true
        Sun visible:       true

       Target shape model: DSK/Unprioritized

        Position vector of surface intercept in the IAU_PHOEBE frame (km):
           X   =           73.186
           Y   =           73.131
           Z   =            0.934
        Planetocentric coordinates of the intercept (degrees):
           LAT =            0.517
           LON =           44.978
        Phase angle (degrees):                     28.385
        Solar incidence angle (degrees):           41.268
        Emission angle (degrees):                  17.493
        Observer visible:  true
        Sun visible:       true

      Vector: Cassini NAC Boresight

       Target shape model: Ellipsoid

        Position vector of surface intercept in the IAU_PHOEBE frame (km):
           X   =           86.390
           Y   =           72.089
           Z   =            8.255
        Planetocentric coordinates of the intercept (degrees):
           LAT =            4.196
           LON =           39.844
        Phase angle (degrees):                     28.139
        Solar incidence angle (degrees):           18.247
        Emission angle (degrees):                  17.858
        Observer visible:  true
        Sun visible:       true

        Local Solar Time at boresight intercept (24 Hour Clock):
           11:31:50

       Target shape model: DSK/Unprioritized

        Position vector of surface intercept in the IAU_PHOEBE frame (km):
           X   =           74.326
           Y   =           66.602
           Z   =            7.247
        Planetocentric coordinates of the intercept (degrees):
           LAT =            4.153
           LON =           41.863
        Phase angle (degrees):                     28.139
        Solar incidence angle (degrees):           33.200
        Emission angle (degrees):                   9.230
        Observer visible:  true
        Sun visible:       true

        Local Solar Time at boresight intercept (24 Hour Clock):
           11:39:55

.. _extra-credit-4:

Extra Credit
^^^^^^^^^^^^^

There are no "extra credit" tasks for this step of the lesson.
