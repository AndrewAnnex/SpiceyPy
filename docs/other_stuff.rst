Other Stuff (Python)
====================

November 20, 2017

The extensive scope of the SpiceyPy system's functionality includes
features the average user may not expect or appreciate, features NAIF
refers to as “Other Stuff.” This workbook includes a set of lessons to
introduce the beginning to moderate user to such features.

The lessons provide a brief description to several related sets of
routines, associated reference documents, a programming task designed to
teach the use of the routines, and an example solution to the
programming problem.

Overview
--------

This workbook contains lessons to demonstrate use of the less celebrated
SpiceyPy routines.

#. Kernel Management with the Kernel Subsystem
#. The Kernel Pool
#. Coordinate Conversions
#. Advanced Time Manipulation Routines
#. Error Handling
#. Windows and Cells
#. Utility and Constants Routines

References
----------

This section lists SPICE documents referred to in this lesson.

The following SPICE tutorials serve as references for the discussions in
this lesson:

.. code-block:: text

      Name              Lesson steps/functions it describes
      ----------------  -----------------------------------------------
      concepts          Concepts of space geometry and time
      intro_to_kernels  Using kernels, meta-kernels
      time              Time systems, conversions and formats
      lsk_and_sclk      LSK and SCLK
      derived_quant     "high-level" observation geometry computations
      other_functions   Intro to some SPICE "low level" computations
      exceptions        built-in mechanism for trapping/handling errors

These tutorials are available from the NAIF ftp server at JPL:

https://naif.jpl.nasa.gov/naif/tutorials.html

Required Readings
^^^^^^^^^^^^^^^^^

.. tip::
   The `Required Readings <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/index.html>`_ are also available on the NAIF website at:
      https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/index.html.

The Required Reading documents are provided with the Toolkit and are
located under the "cspice/doc" directory in the CSPICE Toolkit
installation tree.

.. code-block:: text

      Name             Lesson steps/functions that it describes
      ---------------  -----------------------------------------
      cells.req        The SPICE cell data type
      error.req        The SPICE error handling system
      kernel.req       Loading SPICE kernels
      time.req         Time conversion
      windows.req      The SPICE window data type

The Permuted Index
^^^^^^^^^^^^^^^^^^

.. tip::
   The `Permuted Index <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/info/cspice_idx.html>`_ is also available on the NAIF website at:
      https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/info/cspice_idx.html.

Another useful document distributed with the Toolkit is the permuted
index. This is located under the "cspice/doc" directory in the C
installation tree.

This text document provides a simple mechanism by which users can
discover which SpiceyPy functions perform functions of interest, as well
as the names of the source files that contain these functions.

SpiceyPy API Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^

A SpiceyPy function's parameters specification is available using the
built-in Python help system.


.. py-editor::
    :env: other
    :config: pyscript_other_stuff.json
    :setup:

    import spiceypy

For example, the Python help function


.. py-editor::
    :env: other

    import spiceypy
    
    help(spiceypy.str2et)

describes the str2et function's parameters, while the

`str2et documentation <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/str2et_c.html>`_

describes extensively the str2et functionality.

Kernels Used
------------

The following kernels are used in examples provided in this lesson:

.. code-block:: text

      #  FILE NAME    TYPE DESCRIPTION
      -- ------------ ---- ------------------------------------------------
      1  naif0008.tls LSK  Generic LSK
      2  de405s.bsp   SPK  Planet Ephemeris SPK
      3  pck00008.tpc PCK  Generic PCK

These SPICE kernels are included in the lesson package available from
the NAIF server at JPL:

https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/Lessons/

SpiceyPy Modules Used
---------------------

This section provides a complete list of the functions and kernels that
are suggested for usage in each of the exercises in this lesson. (You
may wish to not look at this list unless/until you "get stuck" while
working on your own.)

.. code-block:: text

      CHAPTER EXERCISE   FUNCTIONS        NON-VOID         KERNELS
      ------- ---------  ---------------  ---------------  ----------
         1    kpool      spiceypy.furnsh  spiceypy.ktotal  1-3
                         spiceypy.unload  spiceypy.kdata
                         spiceypy.kclear

         2    kervar     spiceypy.furnsh  spiceypy.gnpool  1-3
                         spiceypy.kclear  spiceypy.dtpool
                                          spiceypy.gdpool
                                          spiceypy.gcpool

         3    coord      spiceypy.furnsh  spiceypy.dpr     1-3
                         spiceypy.kclear  spiceypy.str2et
                                          spiceypy.bodvrd
                                          spiceypy.spkpos
                                          spiceypy.recrad
                                          spiceypy.reclat
                                          spiceypy.recsph
                                          spiceypy.recgeo

         4    xtic       spiceypy.furnsh  spiceypy.str2et  1
                         spiceypy.tsetyr  spiceypy.timout
                         spiceypy.kclear  spiceypy.tpictr
                                          spiceypy.jyear

         5    aderr      spiceypy.furnsh  spiceypy.spkezr  1-3
                         spiceypy.kclear

         6    win        spiceypy.furnsh  spiceypy.str2et  1-3
                         spiceypy.wninsd  spiceypy.wnvald
                         spiceypy.kclear  spiceypy.wnintd
                                          spiceypy.card
                                          spiceypy.wnfetd
                                          spiceypy.et2utc
                                          spiceypy.wnsumd

         7    units                       spiceypy.tkvrsn
                                          spiceypy.convrt

              xconst                      spiceypy.spd
                                          spiceypy.dpr
                                          spiceypy.rpd
                                          spiceypy.clight
                                          spiceypy.j2100
                                          spiceypy.j2000
                                          spiceypy.tyear
                                          spiceypy.halfpi

Use the Python built-in help system on the various functions listed
above for the API parameters' description, and refer to the headers of
their corresponding CSPICE versions for detailed interface
specifications.

NAIF Documentation
------------------

The technical complexity of the various SPICE subsystems mandates an
extensive, user-friendly documentation set. The set differs somewhat
depending on your choice of development language but provides the same
information with regards to SPICE operation. The sources for a user
needing information concerning SPICE are:

- Required Readings and Users Guides
- Library Source Code Documentation
- API Documentation
- Tutorials

Required Reading and Users Guides
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. tip::
   The `Required Readings <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/index.html>`_ are also available on the NAIF website at:
      https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/index.html.
   The `User Guides <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/ug/index.html>`_ are also available on the NAIF website at:
      https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/ug/index.html

NAIF Required Reading (\*.req) documents introduce the functionality of
particular Spice subsystems:

::

      abcorr.req
      cells.req
      ck.req
      daf.req
      das.req
      dla.req
      dsk.req
      ek.req
      ellipses.req
      error.req
      frames.req
      gf.req
      kernel.req
      naif_ids.req
      pck.req
      planes.req
      problems.req
      rotation.req
      scanning.req
      sclk.req
      sets.req
      spc.req
      spk.req
      symbols.req
      time.req
      windows.req

NAIF Users Guides (\*.ug) describe the proper use of particular Spice command line
tools:

::

      brief.ug
      chronos.ug
      ckbrief.ug
      commnt.ug
      convert.ug
      dskbrief.ug
      dskexp.ug
      frmdiff.ug
      inspekt.ug
      mkdsk.ug
      mkspk.ug
      msopck.ug
      simple.ug
      spacit.ug
      spkdiff.ug
      spkmerge.ug
      states.ug
      subpt.ug
      tictoc.ug
      tobin.ug
      toxfr.ug
      version.ug

Library Source Code Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All SPICELIB and CSPICE source files include usage and design
information incorporated in a comment block known as the “header.”
(Every toolkit includes either the SPICELIB or CSPICE library.)

A header consists of several marked sections:

- **Procedure**: Routine name and one line expansion of the routine's
  name.
- **Abstract**: A tersely worded explanation describing the routine.
- **Copyright**: An identification of the copyright holder for the
  routine.
- **Required_Reading**: A list of SpiceyPy required reading documents
  relating to the routine.
- **Brief_I/O**: A table of arguments, identifying each as either
  input, output, or both, with a very brief description of the
  variable.
- **Detailed_Input & Detailed_Output**: An elaboration of the
  Brief_I/O section providing comprehensive information on
  argument use.
- **Parameters**: Description and declaration of any parameters
  (constants) specific to the routine.
- **Exceptions**: A list of error conditions the routine detects and
  signals plus a discussion of any other exceptional conditions
  the routine may encounter.
- **Files**: A list of other files needed for the routine to operate.
- **Particulars**: A discussion of the routine's function (if
  needed). This section may also include information relating to
  "how" and "why" the routine performs an operation and to
  explain functionality of routines that operate by side effects.
- **Examples**: Descriptions and code snippets concerning usage of
  the routine.
- **Restrictions**: Restrictions or warnings concerning use.
- **Literature_References**: A list of sources required to understand
  the algorithms or data used in the routine.
- **Author_and_Institution**: The names and affiliations for authors
  of the routine.
- **Version**: A list of edits and the authors of those edits made to
  the routine since initial delivery to the Spice system.

The source code for SpiceyPy products is stored in 'src' sub-directory
of the main SpiceyPy directory:

API Documentation
^^^^^^^^^^^^^^^^^

The SpiceyPy package is documented in "readthedocs" website:


https://spiceypy.readthedocs.io/en/main/index.html

Each API documentation page is in large part copied from the
"Abstract" and" Brief_I/O" sections of the corresponding CSPICE
function documentation. Each API page includes a link to the API
documentation for the CSPICE routine called by the SpiceyPy interface.

This SpiceyPy API documentation (the same information as in the website
but without hyperlinks) is also available from the Python built-in help
system:

.. py-editor::
    :env: other

     import spiceypy
     help(spiceypy.str2et) # hit run button to see help


Text kernels
------------

Several workbooks use SPICE text kernels. SPICE identifies a text kernel
as an ASCII text file containing the mark-up tags the kernel subsystem
requires to identify data assignments in that file, and “name=value”
data assignments.

The subsystem uses two tags:

::

         \begintext

and

::

         \begindata

to mark information blocks within the text kernel. The
`\\begintext` tag specifies all text following the tag as
comment information to be ignored by the subsystem.

Things to know:

#. The ``\begindata`` tag marks the start of a data definition block.
   The subsystem processes all text following this marker as SPICE
   kernel data assignments until finding a ``\begintext`` marker.

#. The kernel subsystem defaults to the ``\begintext`` mode until the
   parser encounters a ``\begindata`` tag. Once in ``\begindata`` mode the
   subsystem processes all text as variable assignments until the
   next ``\begintext`` tag.

#. Enter the tags as the only text on a line, i.e.:

   .. code-block:: text

      \begintext

         ... commentary information on the data assignments ...

      \begindata

         ... data assignments ...

#. CSPICE delivery N0059 added to the CSPICE and Icy text kernel
   parsers the functionality to read non native text kernels, i.e.
   a Unix compiled library can read a MS Windows native text
   kernel, a MS Windows compiled library can read a Unix native
   text kernel. Mice acquires this capability from CSPICE.

#. With regards to the FORTRAN distribution, as of delivery N0057
   the :py:func:`spiceypy.furnsh <spiceypy.spiceypy.furnsh>` call includes a line terminator check,
   signaling an error on any attempt to read non-native text
   kernels.

**Text kernel format scalar assignments.**

.. code-block:: text

   VAR_NAME_DP  = 1.234
   VAR_NAME_INT = 1234
   VAR_NAME_STR = 'FORBIN'

Please note the use of a single quote in string assignments.

**Vector assignments.** Vectors must contain the same type data.

.. code-block:: text

   VEC_NAME_DP  = ( 1.234   , 45.678  , 901234.5 )
   VEC_NAME_INT = ( 1234    , 456     , 789      )
   VEC_NAME_STR = ( 'FORBIN', 'FALKEN', 'ROBUR'  )

   also

   VEC_NAME_DP  = ( 1.234,
                   45.678,
                   901234.5 )

   VEC_NAME_STR = ( 'FORBIN',
                    'FALKEN',
                    'ROBUR' )

**Time assignments.**

.. code-block:: text

   TIME_VAL = @31-JAN-2003-12:34:56.798
   TIME_VEC = ( @01-DEC-2004, @15-MAR-2004 )

The at-sign character '@' indicates a time string. The pool subsystem
converts the strings to double precision TDB (a numeric value). Please
note, the time strings must not contain embedded blanks. WARNING - a TDB
string is not the same as a UTC string.

The above examples depict direct assignments via the '=' operator. The
kernel pool also permits incremental assignments via the '+=' operator.

Please refer to the kernels required reading, kernel.req, for additional
information.

Lesson 1: Kernel Management with the Kernel Subsystem
-----------------------------------------------------

Task Statement
^^^^^^^^^^^^^^

Write a program to load a meta kernel, interrogate the SpiceyPy system
for the names and types of all loaded kernels, then demonstrate the
unload functionality and the resulting effects.

Learning Goals
^^^^^^^^^^^^^^

This lesson demonstrates use of the kernel subsystem to load, unload,
and list loaded kernels.

This lesson requires creation of a SPICE meta kernel.

Code Solution
^^^^^^^^^^^^^

First, create a meta text kernel:

You can use two versions of a meta kernel with code examples (kpool.tm)
in this lesson. Either a kernel with explicit path information:

.. py-editor::
    :env: other
    :src: scripts/other_stuff/kpool_make_mk.py


… or a more generic meta kernel using the PATH_VALUES/PATH_SYMBOLS
functionality to declare path names as variables:

.. py-editor::
    :env: other
    :src: scripts/other_stuff/kpool_generic_make_mk.py


Now the solution source code:

.. py-editor::
    :env: other
    :src: scripts/other_stuff/kpool.py



**Run the code example** locally or by clicking the run button above.

First we see the number of all loaded kernels returned from the
:py:func:`spiceypy.ktotal <spiceypy.spiceypy.ktotal>` call.

Then the :py:func:`spiceypy.kdata <spiceypy.spiceypy.kdata>` loop returns the name of each loaded kernel, the
type of kernel (SPK, CK, TEXT, etc.) and the source of the kernel - the
mechanism that loaded the kernel. The source either identifies a meta
kernel, or contains an empty string. An empty source string indicates a
direct load of the kernel with a :py:func:`spiceypy.furnsh <spiceypy.spiceypy.furnsh>` call.

.. code-block:: text

      Kernel count after load:        4

      File   kpool.tm
      Type   META
      Source

      File   kernels/lsk/naif0008.tls
      Type   TEXT
      Source kpool.tm

      File   kernels/spk/de405s.bsp
      Type   SPK
      Source kpool.tm

      File   kernels/pck/pck00008.tpc
      Type   TEXT
      Source kpool.tm

      Kernel count after one unload:  3
      Kernel count after meta unload: 0

this repeats for the kpool_generic.tm file.

Lesson 2: The Kernel Pool
-------------------------

.. _task-statement-os-1:

Task Statement
^^^^^^^^^^^^^^

Write a program to retrieve particular string and numeric text kernel
variables, both scalars and arrays. Interrogate the kernel pool for
assigned variable names.

.. _learning-goals-os-1:

Learning Goals
^^^^^^^^^^^^^^

The lesson demonstrates the SpiceyPy system's facility to retrieve
different types of data (string, numeric, scalar, array) from the kernel
pool.

For the code examples, use this generic text kernel (kervar.tm)
containing PCK-type data, kernels to load, and example time strings:

.. py-editor::
    :env: other
    :src: scripts/other_stuff/kervar_make_mk.py


The main references for pool routines are found in the help command, the
CSPICE source files or the API documentation for the particular
routines.

.. _code-solution-1:

Code Solution
^^^^^^^^^^^^^

.. py-editor::
    :env: other
    :src: scripts/other_stuff/kervar.py



**Run the code example**

The program runs and first reports the number of kernel pool variables
matching the template, 6.

The program then loops over :py:func:`spiceypy.dtpool <spiceypy.spiceypy.dtpool>` 6 times, reporting the
name of each pool variable, the number of data items assigned to that
variable, and the variable type. Within the :py:func:`spiceypy.dtpool <spiceypy.spiceypy.dtpool>` loop, a
second loop outputs the contents of the data variable using
:py:func:`spiceypy.gcpool <spiceypy.spiceypy.gcpool>` or :py:func:`spiceypy.gdpool <spiceypy.spiceypy.gdpool>`.

.. code-block:: text

      Number variables matching template: 6

      BODY699_RING1_1
       Number items: 5   Of type: N

        Numeric value:        133405.000000
        Numeric value:        133730.000000
        Numeric value:             0.000000
        Numeric value:             0.000000
        Numeric value:             0.000000

      BODY699_RING1
       Number items: 5   Of type: N

        Numeric value:        122170.000000
        Numeric value:        136780.000000
        Numeric value:             0.100000
        Numeric value:             0.100000
        Numeric value:             0.500000

      BODY699_RING2
       Number items: 5   Of type: N

        Numeric value:        117580.000000
        Numeric value:        122170.000000
        Numeric value:             0.000000
        Numeric value:             0.000000
        Numeric value:             0.000000

      BODY699_RING1_1_NAME
       Number items: 1   Of type: C

        String value: Encke Gap


      BODY699_RING2_NAME
       Number items: 1   Of type: C

        String value: Cassini Division


      BODY699_RING1_NAME
       Number items: 1   Of type: C

        String value: A Ring

      EXAMPLE_TIMES
        Time value:        134094896.789000
        Time value:        134094896.789000
        Time value:        134094896.789753

Note the final time value differs from the previous values in the final
three decimal places despite the intention that all three strings
represent the same time. This results from round-off when converting a
decimal Julian day representation to the seconds past J2000 ET
representation.

Related Routines
^^^^^^^^^^^^^^^^

- :py:func:`spiceypy.gipool <spiceypy.spiceypy.gipool>` retrieves integer values from the kernel
  subsystem.

Lesson 3: Coordinate Conversions
--------------------------------

.. _task-statement-os-2:

Task Statement
^^^^^^^^^^^^^^

Write a program to convert a Cartesian 3-vector representing some
location to the other coordinate representations. Use the position of
the Moon with respect to Earth in an inertial and non-inertial reference
frame as the example vector.

.. _learning-goals-os-2:

Learning Goals
^^^^^^^^^^^^^^

The SpiceyPy system provides functions to convert coordinate tuples
between Cartesian and various non Cartesian coordinate systems including
conversion between geodetic and rectangular coordinates.

This lesson presents these coordinate transform routines for
rectangular, cylindrical, and spherical systems.

.. _code-solution-2:

Code Solution
^^^^^^^^^^^^^

.. py-editor::
    :env: other
    :src: scripts/other_stuff/coord.py



**Run the code example:**

.. py-editor::
    :env: other

    coord("Feb 3 2002 TDB")


Input “Feb 3 2002 TDB” to calculate the Moon's position. (the 'TDB' tag
indicates a Barycentric Dynamical Time value).

.. code-block:: text

      Time of interest: Feb 3 2002 TDB

Examine the Moon position in the J2000 inertial frame, display the time
and frame:

.. code-block:: text

       Time : Feb 3 2002 TDB
        Inertial Frame: J2000

Convert the Moon Cartesian coordinates to right ascension declination.

.. code-block:: text

         Range/Ra/Dec
          Range:        369340.815193
          RA   :           203.643686
          DEC  :            -4.979010

Latitudinal. Note the difference in the expressions for longitude and
right ascension though they represent a measure of the same quantity.
The RA/DEC system measures RA in the interval [0,2Pi). Latitudinal
coordinates measures longitude in the interval (-Pi,Pi].

.. code-block:: text

         Latitudinal
          Rad  :        369340.815193
          Lon  :          -156.356314
          Lat  :            -4.979010

Spherical. Note the difference between the expression of latitude in the
Latitudinal system and the corresponding Spherical colatitude. The
spherical coordinate system uses the colatitude, the angle measure away
from the positive Z axis. Latitude is the angle between the position
vector and the x-y (equatorial) plane with positive angle defined as
toward the positive Z direction

.. code-block:: text

         Spherical
          Rad  :        369340.815193
          Lon  :          -156.356314
          Colat:            94.979010

The same position look-up in a body fixed (non-inertial) frame,
IAU_EARTH.

.. code-block:: text

        Non-inertial Frame: IAU_EARTH

Latitudinal coordinates return the geocentric latitude.

.. code-block:: text

         Latitudinal
          Rad  :        369340.815193
          Lon  :            70.986950
          Lat  :            -4.989675

Spherical.

.. code-block:: text

         Spherical
          Rad  :        369340.815193
          Lon  :            70.986950
          Colat:            94.989675

Geodetic. The cartographic lat/lon.

.. code-block:: text

         Geodetic
          Rad  :        362962.836755
          Lon  :            70.986950
          Lat  :            -4.990249

.. _related-routines-1:

Related Routines
^^^^^^^^^^^^^^^^

- :py:func:`spiceypy.latrec <spiceypy.spiceypy.latrec>`, latitudinal to rectangular
- :py:func:`spiceypy.latcyl <spiceypy.spiceypy.latcyl>`, latitudinal to cylindrical
- :py:func:`spiceypy.latsph <spiceypy.spiceypy.latsph>`, latitudinal to spherical
- :py:func:`spiceypy.reccyl <spiceypy.spiceypy.reccyl>`, rectangular to cylindrical
- :py:func:`spiceypy.sphrec <spiceypy.spiceypy.sphrec>`, spherical to rectangular
- :py:func:`spiceypy.sphcyl <spiceypy.spiceypy.sphcyl>`, spherical to cylindrical
- :py:func:`spiceypy.sphlat <spiceypy.spiceypy.sphlat>`, spherical to latitudinal
- :py:func:`spiceypy.cyllat <spiceypy.spiceypy.cyllat>`, cylindrical to latitudinal
- :py:func:`spiceypy.cylsph <spiceypy.spiceypy.cylsph>`, cylindrical to spherical
- :py:func:`spiceypy.cylrec <spiceypy.spiceypy.cylrec>`, cylindrical to rectangular
- :py:func:`spiceypy.georec <spiceypy.spiceypy.georec>`, geodetic to rectangular

Lesson 4: Advanced Time Manipulation Routines
---------------------------------------------

.. _task-statement-os-3:

Task Statement
^^^^^^^^^^^^^^

Demonstrate the advanced functions of the time utilities with regard to
formatting of time strings for output. Formatting options include
altering calendar representations of the time strings. Convert time-date
strings between different SpiceyPy-supported formats.

.. _learning-goals-os-3:

Learning Goals
^^^^^^^^^^^^^^

Introduce the routines used for advanced manipulation of time strings.
Understand the concept of ephemeris time (ET) as used in SpiceyPy.

.. _code-solution-3:

Code Solution
^^^^^^^^^^^^^

Caution: Be sure to assign sufficient string lengths for time
formats/pictures.

.. py-editor::
    :env: other
    :src: scripts/other_stuff/xtic.py


**Run the code example**

.. code-block:: text

      Original time string     : Mar 15, 2003 12:34:56.789 AM PST
      Corresponding ET         :     100989360.974561

      Time in string format 1  : Sat Mar 15 01:34:56 PDT 2003
      Time in string format 2  : Sat Mar 15 01:34  03 (2452713.85760 JDUTC)
      Time in string format 3  : 01:34:56.789 A.M. PDT March 15, 2003
      Years between evaluations:           100.000000

Lesson 5: Error Handling
------------------------

.. _task-statement-os-4:

Task Statement
^^^^^^^^^^^^^^

Write an interactive program to return a state vector based on a user's
input. Code the program with the capability to recover from user input
mistakes, inform the user of the mistake, then continue to run.

.. _learning-goals-os-4:

Learning Goals
^^^^^^^^^^^^^^

Learn how to write a program that has the capability to recover from
expected SPICE errors.

The SpiceyPy error subsystem differs from CSPICE and SPICELIB packages
in that the user cannot alter the state of the error subsystem, rather
the user can respond to an error signal using try-except blocks. This
block natively receives and processes any SpiceyError exception signaled
from SpiceyPy. The user can therefore “catch” an error signal so as to
respond in an appropriate manner.

.. _code-solution-4:

Code Solution
^^^^^^^^^^^^^

.. py-editor::
    :env: other
    :src: scripts/other_stuff/aderr.py



**Run the code example**

Now run the code with various inputs to observe behavior. Begin the run
using known astronomical bodies, e.g. “Moon”, “Mars”, “Pluto barycenter”
and “Puck”. Recall the SpiceyPy default units are kilometers, kilometers
per second, kilograms, and seconds. The 'R' marker identifies the
(X,Y,Z) position of the body in kilometers, the 'V' marker identifies
the velocity of the body in kilometers per second, and the 'LT' marker
identifies the one-way light time between the bodies at the requested
evaluation time.


.. code-block:: text

      Target: Moon
      R :       -291584.616595       -266693.402359         -76095.64756
      V :             0.643439            -0.666066            -0.301310
      LT:             1.342311

      Target: Mars
      R :     234536077.419136    -132584383.595569      -63102685.70619
      V :            30.961373            28.932996            13.113031
      LT:           923.001080

      Target: Pluto barycenter
      R :   -1451304742.838526   -4318174144.406321     -918251433.58736
      V :            35.079843             3.053138            -0.036762
      LT:         15501.258293

      Target: Puck

      =====================================================================
      ===========

      Toolkit version: N0067

      SPICE(SPKINSUFFDATA) --

      Insufficient ephemeris data has been loaded to compute the state of 7
      15 (PUCK) relative to 0 (SOLAR SYSTEM BARYCENTER) at the ephemeris ep
      och 2000 JAN 01 12:00:00.000.

      spkezr_c --> SPKEZR --> SPKEZ --> SPKACS --> SPKAPS --> SPKLTC --> SP
      KGEO

      =====================================================================
      ===========

      Target:

Perplexing. What happened?

The kernel files named in meta.tm did not include ephemeris data for
Puck. When the SPK subsystem tried to evaluate Puck's position, the
evaluation failed due to lack of data, so an error signaled.

The above error signifies an absence of state information at ephemeris
time 2000 JAN 01 12:00:00.000 (the requested time, ephemeris time zero).

Try another look-up, this time for “Casper”

.. py-editor::
    :env: other

    aderr('Casper')


.. code-block:: text

      Target: Casper

      =====================================================================
      ===========

      Toolkit version: N0067

      SPICE(IDCODENOTFOUND) --

      The target, 'Casper', is not a recognized name for an ephemeris objec
      t. The cause of this problem may be that you need an updated version
      of the SPICE Toolkit. Alternatively you may call SPKEZ directly if yo
      u know the SPICE ID codes for both 'Casper' and 'EARTH'

      spkezr_c --> SPKEZR

      =====================================================================
      ===========

      Target:

An easy to understand error. The SPICE system does not contain
information on a body named 'Casper.'

Another look-up, this time, “Venus”.

.. py-editor::
    :env: other

    aderr('Venus')


.. code-block:: text

      Target: Venus
      R :     -80970027.540532    -139655772.573898      -53860125.95820
      V :            31.166910           -27.001056           -12.316514
      LT:           567.655074

      Target:

The look-up succeeded despite two errors in our run. The SpiceyPy system
can respond to error conditions (not system errors) in much the same
fashion as languages with catch/throw instructions.

Lesson 6: Windows, and Cells
----------------------------

Programming task
^^^^^^^^^^^^^^^^

Given the times of line-of-sight for a vehicle from a ground station and
the times for an acceptable Sun-station-vehicle phase angle, write a
program to determine the time intervals common to both configurations.

.. _learning-goals-os-5:

Learning Goals
^^^^^^^^^^^^^^

SpiceyPy implementation of SPICE cells consists of a class that provides
an interface to the underlying CSPICE cell structure.

A user should create cells by use of the appropriate SpiceyPy calls.
NAIF recommends against manual creation of cells.

A 'window' is a type of cell containing ordered, double precision values
describing a collection of zero or more intervals.

We define an interval, 'i', as all double precision values bounded by
and including an ordered pair of numbers,

.. code-block:: text

         [ a , b ]
            i   i

where

.. code-block:: text

         a    <   b
          i   -    i

The intervals within a window are both ordered and disjoint. That is,
the beginning of each interval is greater than the end of the previous
interval:

.. code-block:: text

         b  <  a
          i     i+1

A common use of the windows facility is to calculate the intersection
set of a number of time intervals.

.. _code-solution-5:

Code Solution
^^^^^^^^^^^^^

.. py-editor::
    :env: other
    :src: scripts/other_stuff/win.py



**Run the code example**

The output window has the name \`sched' (schedule).

Output the amount of data held in \`sched' compared to the maximum
possible amount.

.. code-block:: text

      Number data values in sched :  6

List the time intervals for which a line of sight exists during the time
of a proper phase angle.

.. code-block:: text

      Time intervals meeting defined criterion.
       0   2003 JAN 02 00:03:30.000   2003 JAN 02 04:43:29.000
       1   2003 JAN 05 12:00:00.000   2003 JAN 05 12:45:00.000
       2   2003 JAN 06 00:30:00.000   2003 JAN 06 02:18:01.000

Finally, an analysis of the \`sched' data. The measure of an interval
[a,b] (a <= b) equals b-a. Real values output in units of seconds.

.. code-block:: text

      Summary of sched window

      o Total measure of sched    :     25980.000009
      o Average measure of sched  :      8660.000003
      o Standard deviation of
        the measures in sched     :      5958.550217
      o Index of shortest interval:  1
      o Index of longest interval :  0

.. _related-routines-2:

Related Routines
^^^^^^^^^^^^^^^^

- :py:func:`spiceypy.wncomd <spiceypy.spiceypy.wncomd>` determines the complement of a window with
  respect to a defined interval.
- :py:func:`spiceypy.wncond <spiceypy.spiceypy.wncond>` contracts a window's intervals.
- :py:func:`spiceypy.wndifd <spiceypy.spiceypy.wndifd>`: Calculate the difference between two windows;
  i.e. every point existing in the first but not the second.
- :py:func:`spiceypy.wnelmd <spiceypy.spiceypy.wnelmd>` returns TRUE or FALSE if a value exists in a
  window.
- :py:func:`spiceypy.wnexpd <spiceypy.spiceypy.wnexpd>` expands the size of the intervals in a window.
- :py:func:`spiceypy.wnextd <spiceypy.spiceypy.wnextd>` extracts a window's endpoints.
- :py:func:`spiceypy.wnfild <spiceypy.spiceypy.wnfild>` fills gaps between intervals in a window.
- :py:func:`spiceypy.wnfltd <spiceypy.spiceypy.wnfltd>` filter/removes small intervals from a window.
- :py:func:`spiceypy.wnincd <spiceypy.spiceypy.wnincd>` determines if an interval exists within a
  window.
- :py:func:`spiceypy.wninsd <spiceypy.spiceypy.wninsd>` inserts an interval into a window.
- :py:func:`spiceypy.wnreld <spiceypy.spiceypy.wnreld>` compares two windows. Comparison operations
  available, equality '=', inequality '<>', subset '<=' and '>=',
  proper subset '<' and '>'.
- :py:func:`spiceypy.wnunid <spiceypy.spiceypy.wnunid>` calculates the union of two windows.

Lesson 7: Utility and Constants Routines
----------------------------------------

.. _task-statement-os-5:

Task Statement
^^^^^^^^^^^^^^

Write an interactive program to convert values between various units.
Demonstrate the flexibility of the unit conversion routine, the string
equality function, and show the version ID function.

.. _learning-goals-os-6:

Learning Goals
^^^^^^^^^^^^^^

SpiceyPy provides several routines to perform commonly needed tasks.
Among these:

SpiceyPy also includes a set of functions that return constant values
often used in astrodynamics, time calculations, and geometry.

.. _code-solution-6:

Code Solution
^^^^^^^^^^^^^

.. py-editor::
    :env: other
    :src: scripts/other_stuff/units.py


**Run the code example**

Run a few conversions through the application to ensure it works. The
intro banner gives us the Toolkit version against which the application
was linked:

.. code-block:: text

      Convert demo program compiled against CSPICE Toolkit CSPICE_N0067
      From Units : klicks
      From Value : 3
      To Units   : miles
           1.86411 STATUTE_MILES

Now we know. Three kilometers equals 1.864 miles.

Legend states Pheidippides ran from the Marathon Plain to Athens. The
modern marathon race (inspired by this event) spans 26.2 miles. How far
in kilometers?

.. code-block:: text

      Convert demo program compiled against CSPICE Toolkit CSPICE_N0067
      From Units : miles
      From Value : 26.2
      To Units   : km
          42.16481 km

.. _task-statement-os-6:

Task Statement
^^^^^^^^^^^^^^

Write a program to output SpiceyPy constants and use those constants to
calculate some rudimentary values.

.. _code-solution-7:

Code Solution
^^^^^^^^^^^^^

.. py-editor::
    :env: other
    :src: scripts/other_stuff/xconst.py

**Run the code example**

::

      Number of (S)econds (P)er (D)ay         :  86400.000000000000
      Number of (D)egrees (P)er (R)adian      : 57.2957795130823229
      Number of (R)adians (P)er (D)egree      :  0.0174532925199433
      Speed of light in KM per second         : 299792.457999999984
      Number of days between epochs J2000
        and J2100                             :  36525.000000000000
      Number of seconds between epochs
        J2000 and J2100                       :    3155760000.00000
      Number of tropical years between
        epochs J2000 and J2100                :    100.002135902909
      Number of degrees in Pi/2 radians of arc: 90.0000000000000000
      Number of radians in 250 degrees of arc :  4.3633231299858242

.. _related-routines-3:

Related Routines
^^^^^^^^^^^^^^^^

- :py:func:`spiceypy.b1900 <spiceypy.spiceypy.b1900>`: Julian Date of the epoch Besselian Date 1900.0
- :py:func:`spiceypy.b1950 <spiceypy.spiceypy.b1950>`: Julian date of the epoch Besselian Date 1950.0
- :py:func:`spiceypy.j1900 <spiceypy.spiceypy.j1900>`: Julian date of 1900 JAN 0.5 this corresponds
  to calendar date 1899 DEC 31 12:00:00
- :py:func:`spiceypy.j1950 <spiceypy.spiceypy.j1950>`: Julian date of 1950 JAN 1.0 this corresponds
  to calendar date 1950 JAN 01 00:00:00
- :py:func:`spiceypy.twopi <spiceypy.spiceypy.twopi>`: double precision value of 2 * Pi
- :py:func:`spiceypy.pi <spiceypy.spiceypy.pi>`: double precision value of Pi
- :py:func:`spiceypy.jyear <spiceypy.spiceypy.jyear>`: seconds per Julian year (365.25 Julian days)
