In-situ Sensing Hands-On Lesson, using CASSINI
===============================================

November 20, 2017

Overview
--------

In this lesson you will develop a simple program illustrating how SPICE
can be used to compute various kinds of geometry information applicable
to the experiments carried out by an in-situ instrument flown on an
interplanetary spacecraft.

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
"commnt" or "spacit" utility programs located in "cspice/exe" of
Toolkit installation tree.

The following SPICE tutorials serve as references for the discussions in
this lesson:

.. code-block:: text

      Name              Lesson steps/functions it describes
      ----------------  -----------------------------------------------
      Time              UTC to ET and SCLK to ET
      Loading Kernels   Loading SPICE kernels
      SCLK              SCLK to ET time conversion
      SPK               Computing positions and velocities
      Frames            Computing transformations between frames

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

.. code-block:: text

      Name             Lesson steps/functions that it describes
      ---------------  -----------------------------------------
      kernel.req       Loading SPICE kernels
      naif_ids.req     Body and reference frame names
      spk.req          Computing positions and velocities
      sclk.req         SCLK to ET time conversion
      time.req         UTC to ET time conversion

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

      #  FILE NAME                 TYPE DESCRIPTION
      -- ------------------------- ---- -----------------------------------
      1  naif0008.tls              LSK  Generic LSK
      2  cas00084.tsc              SCLK Cassini SCLK
      3  020514_SE_SAT105.bsp      SPK  Saturnian Satellite Ephemeris SPK
      4  030201AP_SK_SM546_T45.bsp SPK  Cassini Spacecraft SPK
      5  981005_PLTEPH-DE405S.bsp  SPK  Planetary Ephemeris SPK
      6  sat128.bsp                SPK  Saturnian Satellite Ephemeris SPK
      7  04135_04171pc_psiv2.bc    CK   Cassini Spacecraft CK
      8  cas_v37.tf                FK   Cassini FK
      9  cpck05Mar2004.tpc         PCK  Cassini project PCK

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

.. code-block:: text

      CHAPTER EXERCISE   FUNCTIONS        NON-VOID         KERNELS
      ------- ---------  ---------------  ---------------  ----------
         1    convrt     spiceypy.furnsh  spiceypy.str2et  1
                         spiceypy.unload

         2    sclket     spiceypy.furnsh  spiceypy.str2et  1,2
                         spiceypy.unload  spiceypy.scs2e

         3    getsta     spiceypy.furnsh  spiceypy.str2et  1-6
                         spiceypy.unload  spiceypy.scs2e
                                          spiceypy.spkezr

         4    soldir     spiceypy.furnsh  spiceypy.str2et  1-8
                         spiceypy.unload  spiceypy.scs2e
                                          spiceypy.spkezr
                                          spiceypy.spkpos
                                          spiceypy.vhat

         5    sscpnt     spiceypy.furnsh  spiceypy.str2et  1-9
                         spiceypy.unload  spiceypy.scs2e
                                          spiceypy.spkezr
                                          spiceypy.spkpos
                                          spiceypy.vhat
                                          spiceypy.subpnt
                                          spiceypy.reclat
                                          spiceypy.pxform
                                          spiceypy.mxv
                                          spiceypy.dpr

         6    scvel      spiceypy.furnsh  spiceypy.str2et  1-9
                         spiceypy.unload  spiceypy.scs2e
                                          spiceypy.spkezr
                                          spiceypy.spkpos
                                          spiceypy.vhat
                                          spiceypy.subpnt
                                          spiceypy.reclat
                                          spiceypy.pxform
                                          spiceypy.mxv
                                          spiceypy.dpr

Use the Python built-in help system on the various functions listed
above for the API parameters' description, and refer to the headers of
their corresponding CSPICE versions for detailed interface
specifications.

Step-1: "UTC to ET"
------------------------------

"UTC to ET" Task Statement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Write a program that computes and prints the Ephemeris Time (ET)
corresponding to "2004-06-11T19:32:00" UTC, as the number of
ephemeris seconds past J2000, .

"UTC to ET" Hints
^^^^^^^^^^^^^^^^^^^^

Find out what SPICE kernel(s) is(are) needed to support this conversion.
Reference the "time.req" and/or "Time" tutorial.

Find necessary kernel(s) on the NAIF's FTP site.

Find out what routine should be called to load necessary kernel(s).
Reference the "kernel.req" and/or "Loading Kernels" tutorial.

Find the
"loader" routine calling sequence specification. Look at the "time.req"and
that routine's source code header. This routine may be an entry point,
in which case there will be no source file with the same name. To find
out in which source file this entry point is, search for its name in the
"Permuted Index".

Find the routine(s) used to convert time between UTC and ET. Look at the
"time.req" and/or "Time" tutorial.

Find the
"converter" routine(s) calling sequence specification. Look in the "time.req"
and the routine's source code header.

Put all calls together in a program, add variable declarations (the
routine header's "Declarations" and "Examples" sections are a good
place to look for declaration specification and examples) and output
print statements.

"UTC to ET" Solution Steps
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Only one kernel file is needed to support this conversion – an LSK file
"naif0008.tls".

As any other SPICE kernel this file can be loaded by the spiceypy.furnsh
function. For that, the name of the file can be provided as a sole
argument of this routine:

.. code-block:: python

      ...
      lskfile = 'naif0008.tls'

      spiceypy.furnsh(lskfile)

or it can be listed in a meta-kernel:

.. code-block:: text

      KPL/MK

         The names and contents of the kernels referenced by this
         meta-kernel are as follows:


         File Name                   Description
         --------------------------  ----------------------------------
         naif0008.tls                Generic LSK.

      \begindata
         KERNELS_TO_LOAD = (
                           'kernels/lsk/naif0008.tls'
                           )
      \begintext

the name of which, let's call it "convrt.tm", can be then provided as
a sole argument of the :py:func:`spiceypy.spiceypy.furnsh` routine:

.. code-block:: python

          mkfile = 'convrt.tm'
          spiceypy.furnsh(mkfile)

While the second option seems to involve a bit more work – it requires
making an extra file – it is a much better way to go if you plan to load
more kernels as you extend the program. With the meta-kernel approach
simply adding more kernels to the list in KERNEL_TO_LOAD without
changing the program code will accomplish that.

The highest level SpiceyPy time routine converting UTC to ET is
spiceypy.str2et :py:func:`spiceypy.spiceypy.str2et` .

It has two arguments – input time string representing UTC in a variety
of formats (see :py:func:`spiceypy.spiceypy.str2et` header's section "Particulars" for
the complete description of input time formats) and output DP number of
ET seconds past J2000. A call to spiceypy.str2et converting a given UTC
to ET could look like this:

.. code-block:: python

          utc =  '2004-06-11T19:32:00'
          et = spiceypy.str2et(utc)

By combining :py:func:`spiceypy.spiceypy.furnsh` and :py:func:`spiceypy.spiceypy.str2et` calls and required
declarations and by adding a simple print statement, one would get a
complete program that prints ET for the given UTC epoch.

Use of SpiceyPy calls in a Python script requires the SpiceyPy package
to be installed in your Python distribution, either using pip or conda,
and imported within the script.

When you execute the script, "convrt", it produces the following
output:

.. code-block:: bash

      > python convrt.py
      UTC       = 2004-06-11T19:32:00
      ET        =     140254384.184625

"UTC to ET" Code
^^^^^^^^^^^^^^^^^

Program "convrt.py":

.. code-block:: python

      from __future__ import print_function
      import spiceypy

      def convrt():

          mkfile = 'convrt.tm'
          spiceypy.furnsh(mkfile)

          utc =  '2004-06-11T19:32:00'
          et = spiceypy.str2et(utc)

          print('UTC       = {:s}'.format(utc))
          print('ET        = {:20.6f}'.format(et))

          spiceypy.unload(mkfile)


      if __name__ == '__main__':
          convrt()

Meta-kernel file "convrt.tm":

.. code-block:: text

      KPL/MK

         The names and contents of the kernels referenced by this
         meta-kernel are as follows:


         File Name                   Description
         --------------------------  ----------------------------------
         naif0008.tls                Generic LSK.

      \begindata
         KERNELS_TO_LOAD = (
                           'kernels/lsk/naif0008.tls'
                           )
      \begintext

Step-2: "SCLK to ET"
------------------------------

"SCLK to ET" Task Statement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Extend the program from Step-1 to compute and print ET for the following
CASSINI on-board clock epoch "1465674964.105".

"SCLK to ET" Hints
^^^^^^^^^^^^^^^^^^^^^

Find out what additional (to those already loaded in Step-1) SPICE
kernel(s) is(are) needed to support SCLK to ET conversion. Look at the
"sclk.req" and/or "SCLK" tutorial.

Find necessary kernel(s) on the NAIF's FTP site.

Modify the program or meta-kernel to load this (these) kernels.

Find the routine(s) needed to convert time between SCLK and ET. Look at
the "sclk.req" and/or "Time" and "SCLK" tutorials.

Find the
"converter" routine's calling sequence specification. Look in the "sclk.req"
and the routine's source code header.

Look at "naif_ids.req" and the comments in the additional kernel(s)
that you have loaded for information on proper values of input arguments
of this routine.

Add calls to the
"converter" routine(s), necessary variable declarations (the routine header's" Declarations"and
"Examples" sections are a good place to look for declaration
specification and examples), and output print statements to the program.

"SCLK to ET" Solution Steps
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A CASSINI SCLK file is needed additionally to the LSK file loaded in the
Step-1 to support this conversion.

No code change is needed in the loading portion of the program if a
meta-kernel approach was used in the Step-1. The program will load the
file if it will be added to the list of kernels in the KERNELS_TO_LOAD
variable:

.. code-block:: text

      KPL/MK

         The names and contents of the kernels referenced by this
         meta-kernel are as follows:


         File Name                   Description
         --------------------------  ----------------------------------
         naif0008.tls                Generic LSK.
         cas00084.tsc                Cassini SCLK.

      \begindata
         KERNELS_TO_LOAD = (
                           'kernels/lsk/naif0008.tls'
                           'kernels/sclk/cas00084.tsc'
                           )
      \begintext

The highest level SpiceyPy routine converting SCLK to ET is
spiceypy.scs2e :py:func:`spiceypy.spiceypy.scs2e` .

It has three arguments – NAIF ID for CASSINI s/c (-82 as described by
"naif_ids.req" document), input time string representing CASSINI
SCLK, and output DP number of ET seconds past J2000. A call to
spiceypy.str2et converting given SCLK to ET could look like this:

.. code-block:: python

          scid = -82
          sclk = '1465674964.105'
          et = spiceypy.scs2e(scid, sclk)

By adding the spiceypy.scs2e call, required declarations and a simple
print statement, one would get a complete program that prints ET for the
given SCLK epoch.

When you execute the script, "sclket", it produces the following
output:

::

      > python convrt.py
      UTC       = 2004-06-11T19:32:00
      ET        =     140254384.184625
      SCLK      = 1465674964.105
      ET        =     140254384.183426

"SCLK to ET" Code
^^^^^^^^^^^^^^^^^^^^

Program "sclket.py":

.. code-block:: python

      from __future__ import print_function
      import spiceypy

      def sclket():

          mkfile = 'sclket.tm'
          spiceypy.furnsh(mkfile)

          utc =  '2004-06-11T19:32:00'
          et = spiceypy.str2et(utc)

          print('UTC       = {:s}'.format(utc))
          print('ET        = {:20.6f}'.format(et))

          scid = -82
          sclk = '1465674964.105'
          et = spiceypy.scs2e(scid, sclk)

          print('SCLK      = {:s}'.format(sclk))
          print('ET        = {:20.6f}'.format(et))

          spiceypy.unload(mkfile)


      if __name__ == '__main__':
          sclket()

Meta-kernel file "sclket.tm":

.. code-block:: text

      KPL/MK

         The names and contents of the kernels referenced by this
         meta-kernel are as follows:


         File Name                   Description
         --------------------------  ----------------------------------
         naif0008.tls                Generic LSK.
         cas00084.tsc                Cassini SCLK.

      \begindata
         KERNELS_TO_LOAD = (
                           'kernels/lsk/naif0008.tls'
                           'kernels/sclk/cas00084.tsc'
                           )
      \begintext

Step-3: "Spacecraft State"
------------------------------

"Spacecraft State" Task Statement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Extend the program from Step-2 to compute geometric state – position and
velocity – of the CASSINI spacecraft with respect to the Sun in the
Ecliptic frame at the epoch specified by SCLK time from Step-2.

"Spacecraft State" Hints
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Find out what additional (to those already loaded in Steps-1&2) SPICE
kernel(s) is(are) needed to support state computation. Look at the
"spk.req" and/or "SPK" tutorial.

Find necessary kernel(s) on the NAIF's FTP site.

Verify that the kernels contain enough data to compute the state of
interest. Use "brief" utility program located under "toolkit/exe"
directory for that.

Modify the meta-kernel to load this(these) kernels.

Determine the routine(s) needed to compute states. Look at the
"spk.req" and/or "SPK" tutorial presentation.

Find the the routine(s) calling sequence specification. Look in the
"spk.req" and the routine's source code header.

Reference the "naif_ids.req" and "frames.req"and the routine(s)
header "Inputs" and "Particulars" sections to determine proper
values of the input arguments of this routine.

Add calls to the routine(s), necessary variable declarations and output
print statements to the program.

"Spacecraft State" Solution Steps
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A CASSINI spacecraft trajectory SPK and generic planetary ephemeris SPK
files are needed to support computation of the state of interest.

The file names can be added to the meta-kernel to get them loaded into
the program:

.. code-block:: text

      KPL/MK

         The names and contents of the kernels referenced by this
         meta-kernel are as follows:


         File Name                   Description
         --------------------------  ----------------------------------
         naif0008.tls                Generic LSK.
         cas00084.tsc                Cassini SCLK.
         020514_SE_SAT105.bsp        Saturnian Satellite Ephemeris SPK.
         030201AP_SK_SM546_T45.bsp   Cassini Spacecraft SPK.
         981005_PLTEPH-DE405S.bsp    Planetary Ephemeris SPK.
         sat128.bsp                  Saturnian Satellite Ephemeris SPK.

      \begindata
         KERNELS_TO_LOAD = (
                           'kernels/lsk/naif0008.tls'
                           'kernels/sclk/cas00084.tsc'
                           'kernels/spk/020514_SE_SAT105.bsp'
                           'kernels/spk/030201AP_SK_SM546_T45.bsp'
                           'kernels/spk/981005_PLTEPH-DE405S.bsp'
                           'kernels/spk/sat128.bsp'
                           )
      \begintext

The highest level SpiceyPy routine computing states is spiceypy.spkezr
:py:func:`spiceypy.spiceypy.spkezr` .

We are interested in computing CASSINI position and velocity with
respect to the Sun, therefore the target and observer names should be
set to 'CASSINI' and 'Sun' (both names can be found in
"naif_ids.req").

The state should be in ecliptic frame, therefore the name of the frame
in which the state should be computed is 'ECLIPJ2000' (see
"frames.req" document.)

Since we need only the geometric position, the 'abcorr' argument of the
routine should be set to 'NONE' (see aberration correction discussion in
the :py:func:`spiceypy.spiceypy.spkezr` .

Putting it all together, we get:

.. code-block:: python

          target = 'CASSINI'
          frame  = 'ECLIPJ2000'
          corrtn = 'NONE'
          observ = 'SUN'

          state, ltime = spiceypy.spkezr(target, et, frame,
                                         corrtn, observ)

When you execute the script, "getsta", it produces the following
output:

::

      > python getsta.py
      UTC       = 2004-06-11T19:32:00
      ET        =     140254384.184625
      SCLK      = 1465674964.105
      ET        =     140254384.183426
       X        =    -376599061.916539
       Y        =    1294487780.929154
       Z        =      -7064853.054698
      VX        =            -5.164226
      VY        =             0.801719
      VZ        =             0.040603

"Spacecraft State" Code
^^^^^^^^^^^^^^^^^^^^^^^^^^

Program "getsta.py":

.. code-block:: python

      from __future__ import print_function
      import spiceypy

      def getsta():

          mkfile = 'getsta.tm'
          spiceypy.furnsh(mkfile)

          utc =  '2004-06-11T19:32:00'
          et = spiceypy.str2et(utc)

          print('UTC       = {:s}'.format(utc))
          print('ET        = {:20.6f}'.format(et))

          scid = -82
          sclk = '1465674964.105'
          et = spiceypy.scs2e(scid, sclk)

          print('SCLK      = {:s}'.format(sclk))
          print('ET        = {:20.6f}'.format(et))

          target = 'CASSINI'
          frame  = 'ECLIPJ2000'
          corrtn = 'NONE'
          observ = 'SUN'

          state, ltime = spiceypy.spkezr(target, et, frame,
                                         corrtn, observ)

          print(' X        = {:20.6f}'.format(state[0]))
          print(' Y        = {:20.6f}'.format(state[1]))
          print(' Z        = {:20.6f}'.format(state[2]))
          print('VX        = {:20.6f}'.format(state[3]))
          print('VY        = {:20.6f}'.format(state[4]))
          print('VZ        = {:20.6f}'.format(state[5]))

          spiceypy.unload(mkfile)


      if __name__ == '__main__':
          getsta()

Meta-kernel file "getsta.tm":

.. code-block:: text

      KPL/MK

         The names and contents of the kernels referenced by this
         meta-kernel are as follows:


         File Name                   Description
         --------------------------  ----------------------------------
         naif0008.tls                Generic LSK.
         cas00084.tsc                Cassini SCLK.
         020514_SE_SAT105.bsp        Saturnian Satellite Ephemeris SPK.
         030201AP_SK_SM546_T45.bsp   Cassini Spacecraft SPK.
         981005_PLTEPH-DE405S.bsp    Planetary Ephemeris SPK.
         sat128.bsp                  Saturnian Satellite Ephemeris SPK.

      \begindata
         KERNELS_TO_LOAD = (
                           'kernels/lsk/naif0008.tls'
                           'kernels/sclk/cas00084.tsc'
                           'kernels/spk/020514_SE_SAT105.bsp'
                           'kernels/spk/030201AP_SK_SM546_T45.bsp'
                           'kernels/spk/981005_PLTEPH-DE405S.bsp'
                           'kernels/spk/sat128.bsp'
                           )
      \begintext

Step-4: "Sun Direction"
------------------------------

"Sun Direction" Task Statement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Extend the program from Step-3 to compute apparent direction of the Sun
in the INMS frame at the epoch specified by SCLK time from Step-2.

"Sun Direction" Hints
^^^^^^^^^^^^^^^^^^^^^^^^

Determine the additional SPICE kernels needed to support the direction
computation, knowing that they should provide the s/c and instrument
frame orientation. Retrieve these kernels from the NAIF's FTP site.

Verify that the orientation data in the kernels have adequate coverage
to support computation of the direction of interest. Use
"ckbrief" utility program located under" toolkit/exe" directory
for that.

Modify the meta-kernel to load this(these) kernels.

Determine the proper input arguments for the spiceypy.spkpos call to
calculate the direction (which is the position portion of the output
state). Look through the Frames Kernel find the name of the frame to
used.

Add calls to the routine(s), necessary variable declarations and output
print statements to the program.

"Sun Direction" Solution Steps
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A CASSINI spacecraft orientation CK file, providing s/c orientation with
respect to an inertial frame, and CASSINI FK file, providing orientation
of the INMS frame with respect to the s/c frame, are needed additionally
to already loaded kernels to support computation of this direction.

The file names can be added to the meta-kernel to get them loaded into
the program:

.. code-block:: text

      KPL/MK

         The names and contents of the kernels referenced by this
         meta-kernel are as follows:


         File Name                   Description
         --------------------------  ----------------------------------
         naif0008.tls                Generic LSK.
         cas00084.tsc                Cassini SCLK.
         020514_SE_SAT105.bsp        Saturnian Satellite Ephemeris SPK.
         030201AP_SK_SM546_T45.bsp   Cassini Spacecraft SPK.
         981005_PLTEPH-DE405S.bsp    Planetary Ephemeris SPK.
         sat128.bsp                  Saturnian Satellite Ephemeris SPK.
         04135_04171pc_psiv2.bc      Cassini Spacecraft CK.
         cas_v37.tf                  Cassini FK.


      \begindata
         KERNELS_TO_LOAD = (
                           'kernels/lsk/naif0008.tls'
                           'kernels/sclk/cas00084.tsc'
                           'kernels/spk/020514_SE_SAT105.bsp'
                           'kernels/spk/030201AP_SK_SM546_T45.bsp'
                           'kernels/spk/981005_PLTEPH-DE405S.bsp'
                           'kernels/spk/sat128.bsp'
                           'kernels/ck/04135_04171pc_psiv2.bc'
                           'kernels/fk/cas_v37.tf'
                           )
      \begintext

The same highest level SpiceyPy routine computing positions,
spiceypy.spkpos, can be used to compute this direction.

Since this is the direction of the Sun as seen from the s/c, the target
argument should be set to 'Sun' and the observer argument should be set
to 'CASSINI'. The name of the INMS frame is 'CASSINI_INMS', the
definition and description of this frame are provided in the CASSINI FK
file, "cassini_v02.tf".

Since the apparent, or 'as seen', position is sought for, the 'abcorr'
argument of the routine should be set to 'LT+S' (see aberration correction discussion in the ("\cspice/src/cspice/spkpos_c.c")

If desired, the position can then be turned into a unit vector using
spiceypy.vhat function
(https://spiceypy.readthedocs.io/en/main/documentation.html#spiceypy.spiceypy.vhat).
Putting it all together, we get:

.. code-block:: python

          target = 'SUN'
          frame  = 'CASSINI_INMS'
          corrtn = 'LT+S'
          observ = 'CASSINI'

          sundir, ltime = spiceypy.spkpos(target, et, frame,
                                          corrtn, observ)
          sundir = spiceypy.vhat(sundir)

When you execute the script, "soldir", it produces the following
output:

::

      > python soldir.py
      UTC       = 2004-06-11T19:32:00
      ET        =     140254384.184625
      SCLK      = 1465674964.105
      ET        =     140254384.183426
       X        =    -376599061.916539
       Y        =    1294487780.929154
       Z        =      -7064853.054698
      VX        =            -5.164226
      VY        =             0.801719
      VZ        =             0.040603
      SUNDIR(X) =            -0.290204
      SUNDIR(Y) =             0.881631
      SUNDIR(Z) =             0.372167

"Sun Direction" Code
^^^^^^^^^^^^^^^^^^^^^^

Program "soldir.py":

.. code-block:: python

      from __future__ import print_function
      import spiceypy

      def soldir():

          mkfile = 'soldir.tm'
          spiceypy.furnsh(mkfile)

          utc =  '2004-06-11T19:32:00'
          et = spiceypy.str2et(utc)

          print('UTC       = {:s}'.format(utc))
          print('ET        = {:20.6f}'.format(et))

          scid = -82
          sclk = '1465674964.105'
          et = spiceypy.scs2e(scid, sclk)

          print('SCLK      = {:s}'.format(sclk))
          print('ET        = {:20.6f}'.format(et))

          target = 'CASSINI'
          frame  = 'ECLIPJ2000'
          corrtn = 'NONE'
          observ = 'SUN'

          state, ltime = spiceypy.spkezr(target, et, frame,
                                         corrtn, observ)

          print(' X        = {:20.6f}'.format(state[0]))
          print(' Y        = {:20.6f}'.format(state[1]))
          print(' Z        = {:20.6f}'.format(state[2]))
          print('VX        = {:20.6f}'.format(state[3]))
          print('VY        = {:20.6f}'.format(state[4]))
          print('VZ        = {:20.6f}'.format(state[5]))

          target = 'SUN'
          frame  = 'CASSINI_INMS'
          corrtn = 'LT+S'
          observ = 'CASSINI'

          sundir, ltime = spiceypy.spkpos(target, et, frame,
                                          corrtn, observ)
          sundir = spiceypy.vhat(sundir)

          print('SUNDIR(X) = {:20.6f}'.format(sundir[0]))
          print('SUNDIR(Y) = {:20.6f}'.format(sundir[1]))
          print('SUNDIR(Z) = {:20.6f}'.format(sundir[2]))

          spiceypy.unload(mkfile)


      if __name__ == '__main__':
          soldir()

Meta-kernel file "soldir.tm":

.. code-block:: text

      KPL/MK

         The names and contents of the kernels referenced by this
         meta-kernel are as follows:


         File Name                   Description
         --------------------------  ----------------------------------
         naif0008.tls                Generic LSK.
         cas00084.tsc                Cassini SCLK.
         020514_SE_SAT105.bsp        Saturnian Satellite Ephemeris SPK.
         030201AP_SK_SM546_T45.bsp   Cassini Spacecraft SPK.
         981005_PLTEPH-DE405S.bsp    Planetary Ephemeris SPK.
         sat128.bsp                  Saturnian Satellite Ephemeris SPK.
         04135_04171pc_psiv2.bc      Cassini Spacecraft CK.
         cas_v37.tf                  Cassini FK.


      \begindata
         KERNELS_TO_LOAD = (
                           'kernels/lsk/naif0008.tls'
                           'kernels/sclk/cas00084.tsc'
                           'kernels/spk/020514_SE_SAT105.bsp'
                           'kernels/spk/030201AP_SK_SM546_T45.bsp'
                           'kernels/spk/981005_PLTEPH-DE405S.bsp'
                           'kernels/spk/sat128.bsp'
                           'kernels/ck/04135_04171pc_psiv2.bc'
                           'kernels/fk/cas_v37.tf'
                           )
      \begintext

Step-5: "Sub-Spacecraft Point"
------------------------------

"Sub-Spacecraft Point" Task Statement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Extend the program from Step-4 to compute planetocentric longitude and
and latitude of the sub-spacecraft point on Phoebe, and the direction
from the spacecraft to that point in the INMS frame.

"Sub-Spacecraft Point" Hints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Find the SpiceyPy routine that computes sub-observer point coordinates.
Use "Most Used SpiceyPy APIs" or" subpt" cookbook program for that.

Refer to the routine's header to determine the additional kernels needed
for this direction computation. Get these kernels from the NAIF's FTP
site. Modify the meta-kernel to load this(these) kernels.

Determine the proper input arguments for the routine. Refer to the
routine's header for that information.

Convert the surface point Cartesian vector returned by this routine to
latitudinal coordinates. Use "Permuted Index" to find the routine
that does this conversion. Refer to the routine's header for
input/output argument specifications.

Since the Cartesian vector from the spacecraft to the sub-spacecraft
point is computed in the Phoebe body-fixed frame, it should be
transformed into the instrument frame get the direction we are looking
for. Refer to "frames.req" and/or" Frames" tutorial to determine
the name of the routine computing transformations and use it to compute
transformation from Phoebe body-fixed to the INMS frame.

Using "Permuted Index" find the routine that multiplies 3x3 matrix by
3d vector and use it to rotate the vector to the instrument frame.

Add calls to the routine(s), necessary variable declarations and output
print statements to the program.

"Sub-Spacecraft Point" Solution Steps
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :py:func:`spiceypy.spiceypy.subpnt` routine can be
used to compute the sub-observer point and the vector from the observer
to that point with a single call. To determine this point as the closest point on the Phoebe ellipsoid, the 'method'
argument has to be set to 'NEAR POINT: ELLIPSOID'. For our case the
'target' is 'PHOEBE', the target body-fixed frame is 'IAU_PHOEBE', and
the observer is 'CASSINI'.

Since the s/c is close to Phoebe, light time does not need to be taken
into account and, therefore, the 'abcorr' argument can be set to
'NONE'.

In order for spiceypy.subpnt to compute the nearest point location, a
PCK file containing Phoebe radii has to be loaded into the program (see
"Files" section of the routine's header.) All other files required
for this computation are already being loaded by the program. With PCK
file name added to it, the updated meta-kernel will look like this:

.. code-block:: text

      KPL/MK

         The names and contents of the kernels referenced by this
         meta-kernel are as follows:


         File Name                   Description
         --------------------------  ----------------------------------
         naif0008.tls                Generic LSK.
         cas00084.tsc                Cassini SCLK.
         020514_SE_SAT105.bsp        Saturnian Satellite Ephemeris SPK.
         030201AP_SK_SM546_T45.bsp   Cassini Spacecraft SPK.
         981005_PLTEPH-DE405S.bsp    Planetary Ephemeris SPK.
         sat128.bsp                  Saturnian Satellite Ephemeris SPK.
         04135_04171pc_psiv2.bc      Cassini Spacecraft CK.
         cas_v37.tf                  Cassini FK.
         cpck05Mar2004.tpc           Cassini project PCK.


      \begindata
         KERNELS_TO_LOAD = (
                           'kernels/lsk/naif0008.tls'
                           'kernels/sclk/cas00084.tsc'
                           'kernels/spk/020514_SE_SAT105.bsp'
                           'kernels/spk/030201AP_SK_SM546_T45.bsp'
                           'kernels/spk/981005_PLTEPH-DE405S.bsp'
                           'kernels/spk/sat128.bsp'
                           'kernels/ck/04135_04171pc_psiv2.bc'
                           'kernels/fk/cas_v37.tf'
                           'kernels/pck/cpck05Mar2004.tpc'
                           )
      \begintext

The sub-spacecraft point Cartesian vector can be converted to
planetocentric radius, longitude and latitude using the spiceypy.reclat
routine :py:func:`spiceypy.spiceypy.reclat` .

The vector from the spacecraft to the sub-spacecraft point returned by
spiceypy.subpnt has to be rotated from the body-fixed frame to the
instrument frame. The name of the routine that computes 3x3 matrices
rotating vectors from one frame to another is spiceypy.pxform
:py:func:`spiceypy.spiceypy.pxform` .

In our case the
"from' argument should be set to 'IAU_PHOEBE' and the 'to' argument
should be set to 'CASSINI_INMS'

The vector should be then multiplied by this matrix to rotate it to the
instrument frame. The spiceypy.mxv routine performs that function :py:func:`spiceypy.spiceypy.mxv` .

After applying the rotation, normalize the resultant vector using the
spiceypy.vhat function.

For output the longitude and latitude angles returned by spiceypy.reclat
in radians can be converted to degrees by multiplying by spiceypy.dpr
function :py:func:`spiceypy.spiceypy.dpr` .

Putting it all together, we get:

::

          method = 'NEAR POINT: ELLIPSOID'
          target = 'PHOEBE'
          frame  = 'IAU_PHOEBE'
          corrtn = 'NONE'
          observ = 'CASSINI'

          spoint, trgepc, srfvec = spiceypy.subpnt(method, target, et,
                                                   frame, corrtn, observ)

          srad, slon, slat = spiceypy.reclat(spoint)

          fromfr = 'IAU_PHOEBE'
          tofr   = 'CASSINI_INMS'

          m2imat = spiceypy.pxform(fromfr, tofr, et)

          sbpdir = spiceypy.mxv(m2imat, srfvec)
          sbpdir = spiceypy.vhat(sbpdir)

          print('LON       = {:20.6f}'.format(slon * spiceypy.dpr()))
          print('LAT       = {:20.6f}'.format(slat * spiceypy.dpr()))

When you execute the script, "sscpnt", it produces the following
output:

::

      > python sscpnt.py
      UTC       = 2004-06-11T19:32:00
      ET        =     140254384.184625
      SCLK      = 1465674964.105
      ET        =     140254384.183426
       X        =    -376599061.916539
       Y        =    1294487780.929154
       Z        =      -7064853.054698
      VX        =            -5.164226
      VY        =             0.801719
      VZ        =             0.040603
      SUNDIR(X) =            -0.290204
      SUNDIR(Y) =             0.881631
      SUNDIR(Z) =             0.372167
      LON       =            23.423158
      LAT       =             3.709797
      SBPDIR(X) =            -0.000776
      SBPDIR(Y) =            -0.999873
      SBPDIR(Z) =            -0.015905

"Sub-Spacecraft Point" Code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Program

::

      from __future__ import print_function
      import spiceypy

      def sscpnt():

          mkfile = 'sscpnt.tm'
          spiceypy.furnsh(mkfile)

          utc =  '2004-06-11T19:32:00'
          et = spiceypy.str2et(utc)

          print('UTC       = {:s}'.format(utc))
          print('ET        = {:20.6f}'.format(et))

          scid = -82
          sclk = '1465674964.105'
          et = spiceypy.scs2e(scid, sclk)

          print('SCLK      = {:s}'.format(sclk))
          print('ET        = {:20.6f}'.format(et))

          target = 'CASSINI'
          frame  = 'ECLIPJ2000'
          corrtn = 'NONE'
          observ = 'SUN'

          state, ltime = spiceypy.spkezr(target, et, frame,
                                         corrtn, observ)

          print(' X        = {:20.6f}'.format(state[0]))
          print(' Y        = {:20.6f}'.format(state[1]))
          print(' Z        = {:20.6f}'.format(state[2]))
          print('VX        = {:20.6f}'.format(state[3]))
          print('VY        = {:20.6f}'.format(state[4]))
          print('VZ        = {:20.6f}'.format(state[5]))

          target = 'SUN'
          frame  = 'CASSINI_INMS'
          corrtn = 'LT+S'
          observ = 'CASSINI'

          sundir, ltime = spiceypy.spkpos(target, et, frame,
                                          corrtn, observ)
          sundir = spiceypy.vhat(sundir)

          print('SUNDIR(X) = {:20.6f}'.format(sundir[0]))
          print('SUNDIR(Y) = {:20.6f}'.format(sundir[1]))
          print('SUNDIR(Z) = {:20.6f}'.format(sundir[2]))

          method = 'NEAR POINT: ELLIPSOID'
          target = 'PHOEBE'
          frame  = 'IAU_PHOEBE'
          corrtn = 'NONE'
          observ = 'CASSINI'

          spoint, trgepc, srfvec = spiceypy.subpnt(method, target, et,
                                                   frame, corrtn, observ)

          srad, slon, slat = spiceypy.reclat(spoint)

          fromfr = 'IAU_PHOEBE'
          tofr   = 'CASSINI_INMS'

          m2imat = spiceypy.pxform(fromfr, tofr, et)

          sbpdir = spiceypy.mxv(m2imat, srfvec)
          sbpdir = spiceypy.vhat(sbpdir)

          print('LON       = {:20.6f}'.format(slon * spiceypy.dpr()))
          print('LAT       = {:20.6f}'.format(slat * spiceypy.dpr()))
          print('SBPDIR(X) = {:20.6f}'.format(sbpdir[0]))
          print('SBPDIR(Y) = {:20.6f}'.format(sbpdir[1]))
          print('SBPDIR(Z) = {:20.6f}'.format(sbpdir[2]))

          spiceypy.unload(mkfile)


      if __name__ == '__main__':
          sscpnt()

Meta-kernel file "sscpnt.tm":

::

      KPL/MK

         The names and contents of the kernels referenced by this
         meta-kernel are as follows:


         File Name                   Description
         --------------------------  ----------------------------------
         naif0008.tls                Generic LSK.
         cas00084.tsc                Cassini SCLK.
         020514_SE_SAT105.bsp        Saturnian Satellite Ephemeris SPK.
         030201AP_SK_SM546_T45.bsp   Cassini Spacecraft SPK.
         981005_PLTEPH-DE405S.bsp    Planetary Ephemeris SPK.
         sat128.bsp                  Saturnian Satellite Ephemeris SPK.
         04135_04171pc_psiv2.bc      Cassini Spacecraft CK.
         cas_v37.tf                  Cassini FK.
         cpck05Mar2004.tpc           Cassini project PCK.


      \begindata
         KERNELS_TO_LOAD = (
                           'kernels/lsk/naif0008.tls'
                           'kernels/sclk/cas00084.tsc'
                           'kernels/spk/020514_SE_SAT105.bsp'
                           'kernels/spk/030201AP_SK_SM546_T45.bsp'
                           'kernels/spk/981005_PLTEPH-DE405S.bsp'
                           'kernels/spk/sat128.bsp'
                           'kernels/ck/04135_04171pc_psiv2.bc'
                           'kernels/fk/cas_v37.tf'
                           'kernels/pck/cpck05Mar2004.tpc'
                           )
      \begintext

Step-6: "Spacecraft Velocity"
------------------------------

"Spacecraft Velocity" Task Statement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Extend the program from Step-5 to compute the spacecraft velocity with
respect to Phoebe in the INMS frame.

"Spacecraft Velocity" Hints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Compute velocity of the spacecraft with respect to Phoebe in some
inertial frame, for example J2000. Recall that velocity is the last
three components of the state vector returned by spiceypy.spkezr.

Since the velocity vector is computed in the inertial frame, it should
be rotated to the instrument frame. Look at the previous step the
routine that compute necessary rotation and rotate vectors.

Add calls to the routine(s), necessary variable declarations and output
print statements to the program.

"Spacecraft Velocity" Solution Steps
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All kernels required for computations in this step are already being
loaded by the program, therefore, the meta-kernel does not need to be
changed.

The spacecraft velocity vector is the last three components of the state
returned by spiceypy.spkezr. To compute velocity of CASSINI with respect
to Phoebe in the J2000 inertial frame the spiceypy.spkezr arguments
should be set to 'CASSINI' (TARG), 'PHOEBE' (OBS), 'J2000' (REF) and
'NONE' (ABCORR).

The computed velocity vector has to be rotated from the J2000 frame to
the instrument frame. The spiceypy.pxform routine used in the previous
step can be used to compute the rotation matrix needed for that. In this
case the frame name arguments should be set to 'J2000' (FROM) and
'CASSINI_INMS' (TO).

As in the previous step the difference vector should be then multiplied
by this rotation matrix using the spiceypy.mxv routine. After applying
the rotation, normalize the resultant vector using the spiceypy.vhat
routine.

Putting it all together, we get:

::

          target = 'CASSINI'
          frame  = 'J2000'
          corrtn = 'NONE'
          observ = 'PHOEBE'

          state, ltime = spiceypy.spkezr(target, et, frame,
                                         corrtn, observ)
          scvdir = state[3:6]

          fromfr = 'J2000'
          tofr   = 'CASSINI_INMS'
          j2imat = spiceypy.pxform(fromfr, tofr, et)

          scvdir = spiceypy.mxv(j2imat, scvdir)
          scvdir = spiceypy.vhat(scvdir)

When you execute the script, "scvel", it produces the following
output:

::

      > python scvel.py
      UTC       = 2004-06-11T19:32:00
      ET        =     140254384.184625
      SCLK      = 1465674964.105
      ET        =     140254384.183426
       X        =    -376599061.916539
       Y        =    1294487780.929154
       Z        =      -7064853.054698
      VX        =            -5.164226
      VY        =             0.801719
      VZ        =             0.040603
      SUNDIR(X) =            -0.290204
      SUNDIR(Y) =             0.881631
      SUNDIR(Z) =             0.372167
      LON       =            23.423158
      LAT       =             3.709797
      SBPDIR(X) =            -0.000776
      SBPDIR(Y) =            -0.999873
      SBPDIR(Z) =            -0.015905
      SCVDIR(X) =             0.395785
      SCVDIR(Y) =            -0.292808
      SCVDIR(Z) =             0.870413

Note that computing the spacecraft velocity in the instrument frame by a
single call to spiceypy.spkezr by specifying 'CASSINI_INMS' in the
'ref' argument returns an incorrect result. Such computation will take
into account the spacecraft angular velocity from the CK files, which
should not be considered in this case.

"Spacecraft Velocity" Code Program "scvel.py":
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

      from __future__ import print_function
      import spiceypy

      def scvel():

          mkfile = 'scvel.tm'
          spiceypy.furnsh(mkfile)

          utc =  '2004-06-11T19:32:00'
          et = spiceypy.str2et(utc)

          print('UTC       = {:s}'.format(utc))
          print('ET        = {:20.6f}'.format(et))

          scid = -82
          sclk = '1465674964.105'
          et = spiceypy.scs2e(scid, sclk)

          print('SCLK      = {:s}'.format(sclk))
          print('ET        = {:20.6f}'.format(et))

          target = 'CASSINI'
          frame  = 'ECLIPJ2000'
          corrtn = 'NONE'
          observ = 'SUN'

          state, ltime = spiceypy.spkezr(target, et, frame,
                                         corrtn, observ)

          print(' X        = {:20.6f}'.format(state[0]))
          print(' Y        = {:20.6f}'.format(state[1]))
          print(' Z        = {:20.6f}'.format(state[2]))
          print('VX        = {:20.6f}'.format(state[3]))
          print('VY        = {:20.6f}'.format(state[4]))
          print('VZ        = {:20.6f}'.format(state[5]))

          target = 'SUN'
          frame  = 'CASSINI_INMS'
          corrtn = 'LT+S'
          observ = 'CASSINI'

          sundir, ltime = spiceypy.spkpos(target, et, frame,
                                          corrtn, observ)
          sundir = spiceypy.vhat(sundir)

          print('SUNDIR(X) = {:20.6f}'.format(sundir[0]))
          print('SUNDIR(Y) = {:20.6f}'.format(sundir[1]))
          print('SUNDIR(Z) = {:20.6f}'.format(sundir[2]))

          method = 'NEAR POINT: ELLIPSOID'
          target = 'PHOEBE'
          frame  = 'IAU_PHOEBE'
          corrtn = 'NONE'
          observ = 'CASSINI'

          spoint, trgepc, srfvec = spiceypy.subpnt(method, target, et,
                                                   frame, corrtn, observ)

          srad, slon, slat = spiceypy.reclat(spoint)

          fromfr = 'IAU_PHOEBE'
          tofr   = 'CASSINI_INMS'

          m2imat = spiceypy.pxform(fromfr, tofr, et)

          sbpdir = spiceypy.mxv(m2imat, srfvec)
          sbpdir = spiceypy.vhat(sbpdir)

          print('LON       = {:20.6f}'.format(slon * spiceypy.dpr()))
          print('LAT       = {:20.6f}'.format(slat * spiceypy.dpr()))
          print('SBPDIR(X) = {:20.6f}'.format(sbpdir[0]))
          print('SBPDIR(Y) = {:20.6f}'.format(sbpdir[1]))
          print('SBPDIR(Z) = {:20.6f}'.format(sbpdir[2]))

          target = 'CASSINI'
          frame  = 'J2000'
          corrtn = 'NONE'
          observ = 'PHOEBE'

          state, ltime = spiceypy.spkezr(target, et, frame,
                                         corrtn, observ)
          scvdir = state[3:6]

          fromfr = 'J2000'
          tofr   = 'CASSINI_INMS'
          j2imat = spiceypy.pxform(fromfr, tofr, et)

          scvdir = spiceypy.mxv(j2imat, scvdir)
          scvdir = spiceypy.vhat(scvdir)

          print('SCVDIR(X) = {:20.6f}'.format(scvdir[0]))
          print('SCVDIR(Y) = {:20.6f}'.format(scvdir[1]))
          print('SCVDIR(Z) = {:20.6f}'.format(scvdir[2]))

          spiceypy.unload(mkfile)


      if __name__ == '__main__':
          scvel()

Meta-kernel file "scvel.tm":

::

      KPL/MK

         The names and contents of the kernels referenced by this
         meta-kernel are as follows:


         File Name                   Description
         --------------------------  ----------------------------------
         naif0008.tls                Generic LSK.
         cas00084.tsc                Cassini SCLK.
         020514_SE_SAT105.bsp        Saturnian Satellite Ephemeris SPK.
         030201AP_SK_SM546_T45.bsp   Cassini Spacecraft SPK.
         981005_PLTEPH-DE405S.bsp    Planetary Ephemeris SPK.
         sat128.bsp                  Saturnian Satellite Ephemeris SPK.
         04135_04171pc_psiv2.bc      Cassini Spacecraft CK.
         cas_v37.tf                  Cassini FK.
         cpck05Mar2004.tpc           Cassini project PCK.


      \begindata
         KERNELS_TO_LOAD = (
                           'kernels/lsk/naif0008.tls'
                           'kernels/sclk/cas00084.tsc'
                           'kernels/spk/020514_SE_SAT105.bsp'
                           'kernels/spk/030201AP_SK_SM546_T45.bsp'
                           'kernels/spk/981005_PLTEPH-DE405S.bsp'
                           'kernels/spk/sat128.bsp'
                           'kernels/ck/04135_04171pc_psiv2.bc'
                           'kernels/fk/cas_v37.tf'
                           'kernels/pck/cpck05Mar2004.tpc'
                           )
      \begintext
