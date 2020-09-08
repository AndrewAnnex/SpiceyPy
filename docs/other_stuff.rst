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

::

       1.   Kernel Management with the Kernel Subsystem

       2.   The Kernel Pool

       3.   Coordinate Conversions

       4.   Advanced Time Manipulation Routines

       5.   Error Handling

       6.   Windows and Cells

       7.   Utility and Constants Routines

References
----------

This section lists SPICE documents referred to in this lesson.

The following SPICE tutorials serve as references for the discussions in
this lesson:

::

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
      cells.req        The SPICE cell data type
      error.req        The SPICE error handling system
      kernel.req       Loading SPICE kernels
      time.req         Time conversion
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

      #  FILE NAME    TYPE DESCRIPTION
      -- ------------ ---- ------------------------------------------------
      1  naif0008.tls LSK  Generic LSK
      2  de405s.bsp   SPK  Planet Ephemeris SPK
      3  pck00008.tpc PCK  Generic PCK

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
------------------------------

The technical complexity of the various SPICE subsystems mandates an
extensive, user-friendly documentation set. The set differs somewhat
depending on your choice of development language but provides the same
information with regards to SPICE operation. The sources for a user
needing information concerning SPICE are:

::

       --   Required Readings and Users Guides

       --   Library Source Code Documentation

       --   API Documentation

       --   Tutorials

Required Reading and Users Guides
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. tip::
   The `Required Readings <https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/index.html>`_ are also available on the NAIF website at:
      https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/index.html.
   The `User Guides <https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/ug/index.html>`_ are also available on the NAIF website at:
      https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/ug/index.html

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

NAIF Users Guides (\*.ug) describe the proper use of particular SpiceyPy
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

These text documents exist in the 'doc' directory of the main CSPICE
Toolkit directory:

::

         ../cspice/doc/

HTML format documentation

The SpiceyPy distributions include HTML versions of Required Readings
and Users Guides, accessible from the HTML documentation directory:

::

         ../cspice/doc/html/index.html

Library Source Code Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All SPICELIB and CSPICE source files include usage and design
information incorporated in a comment block known as the “header.”
(Every toolkit includes either the SPICELIB or CSPICE library.)

A header consists of several marked sections:

::

       --   Procedure: Routine name and one line expansion of the routine's
            name.

       --   Abstract: A tersely worded explanation describing the routine.

       --   Copyright: An identification of the copyright holder for the
            routine.

       --   Required_Reading: A list of SpiceyPy required reading documents
            relating to the routine.

       --   Brief_I/O: A table of arguments, identifying each as either
            input, output, or both, with a very brief description of the
            variable.

       --   Detailed_Input & Detailed_Output: An elaboration of the
            Brief_I/O section providing comprehensive information on
            argument use.

       --   Parameters: Description and declaration of any parameters
            (constants) specific to the routine.

       --   Exceptions: A list of error conditions the routine detects and
            signals plus a discussion of any other exceptional conditions
            the routine may encounter.

       --   Files: A list of other files needed for the routine to operate.

       --   Particulars: A discussion of the routine's function (if
            needed). This section may also include information relating to
            "how" and "why" the routine performs an operation and to
            explain functionality of routines that operate by side effects.

       --   Examples: Descriptions and code snippets concerning usage of
            the routine.

       --   Restrictions: Restrictions or warnings concerning use.

       --   Literature_References: A list of sources required to understand
            the algorithms or data used in the routine.

       --   Author_and_Institution: The names and affiliations for authors
            of the routine.

       --   Version: A list of edits and the authors of those edits made to
            the routine since initial delivery to the SpiceyPy system.

The source code for SpiceyPy products is stored in 'src' sub-directory
of the main SpiceyPy directory:

API Documentation
^^^^^^^^^^^^^^^^^^^

The SpiceyPy package is documented in "readthedocs" website:

::

      https://spiceypy.readthedocs.io/en/main/index.html

Each API documentation page is in large part copied from the
"Abstract" and" Brief_I/O" sections of the corresponding CSPICE
function documentation. Each API page includes a link to the API
documentation for the CSPICE routine called by the SpiceyPy interface.

This SpiceyPy API documentation (the same information as in the website
but without hyperlinks) is also available from the Python built-in help
system:

::

      >>> help ( spiceypy.str2et )
      Help on function str2et in module spiceypy.spiceypy:

      str2et(*args, **kwargs)
          Convert a string representing an epoch to a double precision
          value representing the number of TDB seconds past the J2000
          epoch corresponding to the input epoch.

             ...

          :param time: A string representing an epoch.
          :type time: str
          :return: The equivalent value in seconds past J2000, TDB.
          :rtype: float

In order to have offline access to the documentation it is recommended
to have the CSPICE Toolkit installed locally. The CSPICE package
includes the CSPICE Reference Guide, an index of all CSPICE wrapper APIs
with hyperlinks to API specific documentation. Each API documentation
page includes cross-links to any other wrapper API mentioned in the
document and links to the wrapper source code.

::

         ...cspice/doc/html/cspice/index.html

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

::

       1.   The \begindata tag marks the start of a data definition block.
            The subsystem processes all text following this marker as SPICE
            kernel data assignments until finding a \begintext marker.

       2.   The kernel subsystem defaults to the \begintext mode until the
            parser encounters a \begindata tag. Once in \begindata mode the
            subsystem processes all text as variable assignments until the
            next \begintext tag.

       3.   Enter the tags as the only text on a line, i.e.:


         \begintext

            ... commentary information on the data assignments ...

         \begindata

            ... data assignments ...


       4.   CSPICE delivery N0059 added to the CSPICE and Icy text kernel
            parsers the functionality to read non native text kernels, i.e.
            a Unix compiled library can read a MS Windows native text
            kernel, a MS Windows compiled library can read a Unix native
            text kernel. Mice acquires this capability from CSPICE.

       5.   With regards to the FORTRAN distribution, as of delivery N0057
            the spiceypy.furnsh call includes a line terminator check,
            signaling an error on any attempt to read non-native text
            kernels.

Text kernel format

Scalar assignments.

::

         VAR_NAME_DP  = 1.234
         VAR_NAME_INT = 1234
         VAR_NAME_STR = 'FORBIN'

Please note the use of a single quote in string assignments.

Vector assignments. Vectors must contain the same type data.

::

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

Time assignments.

::

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

::

      KPL/MK

      \begindata

         KERNELS_TO_LOAD = ( 'kernels/spk/de405s.bsp',
                             'kernels/pck/pck00008.tpc',
                             'kernels/lsk/naif0008.tls' )

      \begintext

… or a more generic meta kernel using the PATH_VALUES/PATH_SYMBOLS
functionality to declare path names as variables:

::

      KPL/MK

         Define the paths to the kernel directory. Use the PATH_SYMBOLS
         as aliases to the paths.

         The names and contents of the kernels referenced by this
         meta-kernel are as follows:

            File Name        Description
            ---------------  ------------------------------
            naif0008.tls     Generic LSK.
            de405s.bsp       Planet Ephemeris SPK.
            pck00008.tpc     Generic PCK.


      \begindata

         PATH_VALUES     = ( 'kernels/lsk',
                             'kernels/spk',
                             'kernels/pck' )

         PATH_SYMBOLS    = ( 'LSK', 'SPK', 'PCK' )

         KERNELS_TO_LOAD = ( '$LSK/naif0008.tls',
                             '$SPK/de405s.bsp',
                             '$PCK/pck00008.tpc' )

      \begintext

Now the solution source code:

::

      from __future__ import print_function

      #
      # Import the CSPICE-Python interface.
      #
      import spiceypy

      def kpool():

          #
          # Assign the path name of the meta kernel to META.
          #
          META = 'kpool.tm'


          #
          # Load the meta kernel then use KTOTAL to interrogate the SPICE
          # kernel subsystem.
          #
          spiceypy.furnsh( META )


          count = spiceypy.ktotal( 'ALL' );
          print( 'Kernel count after load:        {0}\n'.format(count))


          #
          # Loop over the number of files; interrogate the SPICE system
          # with spiceypy.kdata for the kernel names and the type.
          # 'found' returns a boolean indicating whether any kernel files
          # of the specified type were loaded by the kernel subsystem.
          # This example ignores checking 'found' as kernels are known
          # to be loaded.
          #
          for i in range(0, count):
              [ file, type, source, handle] = spiceypy.kdata(i, 'ALL');
              print( 'File   {0}'.format(file) )
              print( 'Type   {0}'.format(type) )
              print( 'Source {0}\n'.format(source) )


          #
          # Unload one kernel then check the count.
          #
          spiceypy.unload( 'kernels/spk/de405s.bsp')
          count = spiceypy.ktotal( 'ALL' );

          #
          # The subsystem should report one less kernel.
          #
          print( 'Kernel count after one unload:  {0}'.format(count))

          #
          # Now unload the meta kernel. This action unloads all
          # files listed in the meta kernel.
          #
          spiceypy.unload( META )


          #
          # Check the count; spiceypy should return a count of zero.
          #
          count = spiceypy.ktotal( 'ALL');
          print( 'Kernel count after meta unload: {0}'.format(count))


          #
          # Done. Unload the kernels.
          #
          spiceypy.kclear

      if __name__ == '__main__':
         kpool()

Run the code example

First we see the number of all loaded kernels returned from the
spiceypy.ktotal call.

Then the spiceypy.kdata loop returns the name of each loaded kernel, the
type of kernel (SPK, CK, TEXT, etc.) and the source of the kernel - the
mechanism that loaded the kernel. The source either identifies a meta
kernel, or contains an empty string. An empty source string indicates a
direct load of the kernel with a spiceypy.furnsh call.

::

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

Lesson 2: The Kernel Pool
------------------------------

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

::

      KPL/MK

         Name the kernels to load. Use path symbols.

         The names and contents of the kernels referenced by this
         meta-kernel are as follows:

            File Name        Description
            ---------------  ------------------------------
            naif0008.tls     Generic LSK.
            de405s.bsp       Planet Ephemeris SPK.
            pck00008.tpc     Generic PCK.


      \begindata

         PATH_VALUES     = ('kernels/spk',
                            'kernels/pck',
                            'kernels/lsk')

         PATH_SYMBOLS    = ('SPK' , 'PCK' , 'LSK' )

         KERNELS_TO_LOAD = ( '$SPK/de405s.bsp',
                             '$PCK/pck00008.tpc',
                             '$LSK/naif0008.tls')

      \begintext

      Ring model data.

      \begindata

         BODY699_RING1_NAME     = 'A Ring'
         BODY699_RING1          = (122170.0 136780.0 0.1 0.1 0.5)

         BODY699_RING1_1_NAME   = 'Encke Gap'
         BODY699_RING1_1        = (133405.0 133730.0 0.0 0.0 0.0)

         BODY699_RING2_NAME     = 'Cassini Division'
         BODY699_RING2          = (117580.0 122170.0 0.0 0.0 0.0)

      \begintext

      The kernel pool recognizes values preceded by '@' as time
      values. When read, the kernel subsystem converts these
      representations into double precision ephemeris time.

      Caution: The kernel subsystem interprets the time strings
      identified by '@' as TDB. The same string passed as input
      to @STR2ET is processed as UTC.

      The three expressions stored in the EXAMPLE_TIMES array represent
      the same epoch.

      \begindata

         EXAMPLE_TIMES       = ( @APRIL-1-2004-12:34:56.789,
                                 @4/1/2004-12:34:56.789,
                                 @JD2453097.0242684
                                )

      \begintext

The main references for pool routines are found in the help command, the
CSPICE source files or the API documentation for the particular
routines.

.. _code-solution-1:

Code Solution
^^^^^^^^^^^^^

::

      from __future__ import print_function

      #
      # Import the CSPICE-Python interface.
      #
      import spiceypy
      from spiceypy.utils.support_types import SpiceyError

      def kervar():

          #
          # Define the max number of kernel variables
          # of concern for this examples.
          #
          N_ITEMS =  20

          #
          # Load the example kernel containing the kernel variables.
          # The kernels defined in KERNELS_TO_LOAD load into the
          # kernel pool with this call.
          #
          spiceypy.furnsh( 'kervar.tm' )

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
          tmplate = '*RING*'

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
              cvals = spiceypy.gnpool( tmplate, START, N_ITEMS )
              print( 'Number variables matching template: {0}'.\
              format( len(cvals)) )
          except SpiceyError:
              print( 'No kernel variables matched template.' )
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
              [dim, type] = spiceypy.dtpool( cval )

              print( '\n' + cval )
              print( ' Number items: {0}   Of type: {1}\n'.\
              format(dim, type) )

              #
              # Test character equality, 'N' or 'C'.
              #
              if type == 'N':

                  #
                  # If 'type' equals 'N', we found a numeric array.
                  # In this case any numeric array will be an array
                  # of double precision numbers ('doubles').
                  # spiceypy.gdpool retrieves doubles from the
                  # kernel pool.
                  #
                  dvars = spiceypy.gdpool( cval, START, N_ITEMS )
                  for dvar in dvars:
                      print('  Numeric value: {0:20.6f}'.format(dvar))

              elif type == 'C':

                  #
                  # If 'type' equals 'C', we found a string array.
                  # spiceypy.gcpool retrieves string values from the
                  # kernel pool.
                  #
                  cvars = spiceypy.gcpool( cval, START, N_ITEMS )

                  for cvar in cvars:
                      print('  String value: {0}\n'.format(cvar))

              else:

                  #
                  # This block should never execute.
                  #
                  print('Unknown type. Code error.')


          #
          # Now look at the time variable EXAMPLE_TIMES. Extract this
          # value as an array of doubles.
          #
          dvars = spiceypy.gdpool( 'EXAMPLE_TIMES', START, N_ITEMS )

          print( 'EXAMPLE_TIMES' )

          for dvar in dvars:
              print('  Time value:    {0:20.6f}'.format(dvar))

          #
          # Done. Unload the kernels.
          #
          spiceypy.kclear

      if __name__ == '__main__':
         kervar()

Run the code example

The program runs and first reports the number of kernel pool variables
matching the template, 6.

The program then loops over the spiceypy.dtpool 6 times, reporting the
name of each pool variable, the number of data items assigned to that
variable, and the variable type. Within the spiceypy.dtpool loop, a
second loop outputs the contents of the data variable using
spiceypy.gcpool or spiceypy.gdpool.

::

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
^^^^^^^^^^^^^^^^^

::

       --   spiceypy.gipool retrieves integer values from the kernel
            subsystem.

Lesson 3: Coordinate Conversions
---------------------------------

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

::

      from __future__ import print_function
      from builtins import input
      import sys

      #
      # Import the CSPICE-Python interface.
      #
      import spiceypy

      def coord():

          #
          # Define the inertial and non inertial frame names.
          #
          # Initialize variables or set type. All variables
          # used in a PROMPT construct must be initialized
          # as strings.
          #
          INRFRM = 'J2000'
          NONFRM = 'IAU_EARTH'
          r2d = spiceypy.dpr()

          #
          # Load the needed kernels using a spiceypy.furnsh call on the
          # meta kernel.
          #
          spiceypy.furnsh( 'coord.tm' )

          #
          # Prompt the user for a time string. Convert the
          # time string to ephemeris time J2000 (ET).
          #
          timstr = input( 'Time of interest: ')
          et     = spiceypy.str2et( timstr )

          #
          # Access the kernel pool data for the triaxial radii of the
          # Earth, rad[1][0] holds the equatorial radius, rad[1][2]
          # the polar radius.
          #
          rad = spiceypy.bodvrd( 'EARTH', 'RADII', 3 )

          #
          # Calculate the flattening factor for the Earth.
          #
          #          equatorial_radius - polar_radius
          # flat =   ________________________________
          #
          #                equatorial_radius
          #
          flat = (rad[1][0] - rad[1][2])/rad[1][0]

          #
          # Make the spiceypy.spkpos call to determine the apparent
          # position of the Moon w.r.t. to the Earth at 'et' in the
          # inertial frame.
          #
          [pos, ltime] = spiceypy.spkpos('MOON', et, INRFRM,
                                         'LT+S','EARTH'    )

          #
          # Show the current frame and time.
          #
          print( ' Time : {0}'.format(timstr) )
          print( ' Inertial Frame: {0}\n'.format(INRFRM) )

          #
          # First convert the position vector
          # X = pos(1), Y = pos(2), Z = pos(3), to RA/DEC.
          #
          [ range, ra, dec ] = spiceypy.recrad( pos )

          print('   Range/Ra/Dec' )
          print('    Range: {0:20.6f}'.format(range) )
          print('    RA   : {0:20.6f}'.format(ra * r2d) )
          print('    DEC  : {0:20.6f}'.format(dec* r2d) )

          #
          # ...latitudinal coordinates...
          #
          [ range, lon, lat ] = spiceypy.reclat( pos )
          print('   Latitudinal ' )
          print('    Rad  : {0:20.6f}'.format(range) )
          print('    Lon  : {0:20.6f}'.format(lon * r2d) )
          print('    Lat  : {0:20.6f}'.format(lat * r2d) )

          #
          # ...spherical coordinates use the colatitude,
          # the angle from the Z axis.
          #
          [ range, colat, lon ] = spiceypy.recsph( pos )
          print( '   Spherical' )
          print('    Rad  : {0:20.6f}'.format(range) )
          print('    Lon  : {0:20.6f}'.format(lon   * r2d) )
          print('    Colat: {0:20.6f}'.format(colat * r2d) )

          #
          # Make the spiceypy.spkpos call to determine the apparent
          # position of the Moon w.r.t. to the Earth at 'et' in the
          # non-inertial, body fixed, frame.
          #
          [pos, ltime] = spiceypy.spkpos('MOON', et, NONFRM,
                                         'LT+S','EARTH')

          print()
          print( '  Non-inertial Frame: {0}'.format(NONFRM) )

          #
          # ...latitudinal coordinates...
          #
          [ range, lon, lat ] = spiceypy.reclat( pos )
          print('   Latitudinal ' )
          print('    Rad  : {0:20.6f}'.format(range) )
          print('    Lon  : {0:20.6f}'.format(lon * r2d) )
          print('    Lat  : {0:20.6f}'.format(lat * r2d) )

          #
          # ...spherical coordinates use the colatitude,
          # the angle from the Z axis.
          #
          [ range, colat, lon ] = spiceypy.recsph( pos )
          print( '   Spherical' )
          print('    Rad  : {0:20.6f}'.format(range) )
          print('    Lon  : {0:20.6f}'.format(lon   * r2d) )
          print('    Colat: {0:20.6f}'.format(colat * r2d) )

          #
          # ...finally, convert the position to geodetic coordinates.
          #
          [ lon, lat, range ] = spiceypy.recgeo( pos, rad[1][0], flat )
          print( '   Geodetic' )
          print('    Rad  : {0:20.6f}'.format(range) )
          print('    Lon  : {0:20.6f}'.format(lon * r2d) )
          print('    Lat  : {0:20.6f}'.format(lat * r2d) )
          print()

          #
          # Done. Unload the kernels.
          #
          spiceypy.kclear


      if __name__ == '__main__':
         coord()

Run the code example

Input “Feb 3 2002 TDB” to calculate the Moon's position. (the 'TDB' tag
indicates a Barycentric Dynamical Time value).

::

      Time of interest: Feb 3 2002 TDB

Examine the Moon position in the J2000 inertial frame, display the time
and frame:

::

       Time : Feb 3 2002 TDB
        Inertial Frame: J2000

Convert the Moon Cartesian coordinates to right ascension declination.

::

         Range/Ra/Dec
          Range:        369340.815193
          RA   :           203.643686
          DEC  :            -4.979010

Latitudinal. Note the difference in the expressions for longitude and
right ascension though they represent a measure of the same quantity.
The RA/DEC system measures RA in the interval [0,2Pi). Latitudinal
coordinates measures longitude in the interval (-Pi,Pi].

::

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

::

         Spherical
          Rad  :        369340.815193
          Lon  :          -156.356314
          Colat:            94.979010

The same position look-up in a body fixed (non-inertial) frame,
IAU_EARTH.

::

        Non-inertial Frame: IAU_EARTH

Latitudinal coordinates return the geocentric latitude.

::

         Latitudinal
          Rad  :        369340.815193
          Lon  :            70.986950
          Lat  :            -4.989675

Spherical.

::

         Spherical
          Rad  :        369340.815193
          Lon  :            70.986950
          Colat:            94.989675

Geodetic. The cartographic lat/lon.

::

         Geodetic
          Rad  :        362962.836755
          Lon  :            70.986950
          Lat  :            -4.990249

.. _related-routines-1:

Related Routines
^^^^^^^^^^^^^^^^^

::

       --   spiceypy.latrec, latitudinal to rectangular

       --   spiceypy.latcyl, latitudinal to cylindrical

       --   spiceypy.latsph, latitudinal to spherical

       --   spiceypy.reccyl, rectangular to cylindrical

       --   spiceypy.sphrec, spherical to rectangular

       --   spiceypy.sphcyl, spherical to cylindrical

       --   spiceypy.sphlat, spherical to latitudinal

       --   spiceypy.cyllat, cylindrical to latitudinal

       --   spiceypy.cylsph, cylindrical to spherical

       --   spiceypy.cylrec, cylindrical to rectangular

       --   spiceypy.georec, geodetic to rectangular

Lesson 4: Advanced Time Manipulation Routines
----------------------------------------------

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

::

      from __future__ import print_function

      #
      # Import the CSPICE-Python interface.
      #
      import spiceypy

      def xtic():

          #
          # Assign the META variable to the name of the meta-kernel
          # that contains the LSK kernel and create an arbitrary
          # time string.
          #
          CALSTR    = 'Mar 15, 2003 12:34:56.789 AM PST'
          META      = 'xtic.tm'
          AMBIGSTR  = 'Mar 15, 79 12:34:56'
          T_FORMAT1 = 'Wkd Mon DD HR:MN:SC PDT YYYY ::UTC-7'
          T_FORMAT2 = 'Wkd Mon DD HR:MN ::UTC-7 YR (JULIAND.##### JDUTC)'

          #
          # Load the meta-kernel.
          #
          spiceypy.furnsh( META )
          print( 'Original time string     : {0}'.format(CALSTR) )

          #
          # Convert the time string to the number of ephemeris
          # seconds past the J2000 epoch. This is the most common
          # internal time representation used by the CSPICE
          # system; CSPICE refers to this as ephemeris time (ET).
          #
          et = spiceypy.str2et( CALSTR )
          print( 'Corresponding ET         : {0:20.6f}\n'.format(et) )

          #
          # Make a picture of an output format. Describe a Unix-like
          # time string then send the picture and the 'et' value through
          # spiceypy.timout to format and convert the ET representation
          # of the time string into the form described in
          # spiceypy.timout. The '::UTC-7' token indicates the time
          # zone for the `timstr' output - PDT. 'PDT' is part of the
          # output, but not a time system token.
          #
          timstr = spiceypy.timout( et, T_FORMAT1)
          print( 'Time in string format 1  : {0}'.format(timstr) )

          timstr = spiceypy.timout( et, T_FORMAT2)
          print( 'Time in string format 2  : {0}'.format(timstr) )

          #
          # Why create a picture by hand when spiceypy can do it for
          # you? Input a string to spiceypy.tpictr with the format of
          # interest. `ok' returns a boolean indicating whether an
          # error occurred while parsing the picture string, if so,
          # an error diagnostic message returns in 'xerror'. In this
          # example the picture string is known as correct.
          #
          pic = '12:34:56.789 P.M. PDT January 1, 2006'
          [ pictr, ok, xerror] = spiceypy.tpictr(pic)

          if not bool(ok):
              print( xerror )
              exit


          timstr = spiceypy.timout( et, pictr)
          print( 'Time in string format 3  : {0}'.format( timstr ) )

          #
          # Two digit year representations often cause problems due to
          # the ambiguity of the century. The routine spiceypy.tsetyr
          # gives the user the ability to set a default range for 2
          # digit year representation. SPICE uses 1969AD as the default
          # start year so the numbers inclusive of 69 to 99 represent
          # years 1969AD to 1999AD, the numbers inclusive of 00 to 68
          # represent years 2000AD to 2068AD.
          #
          # The defined time string 'AMBIGSTR' contains a two-digit
          # year. Since the SPICE base year is 1969, the time subsystem
          # interprets the string as 1979.
          #
          et1 = spiceypy.str2et( AMBIGSTR )

          #
          # Set 1980 as the base year causes SPICE to interpret the
          # time string's "79" as 2079.
          #
          spiceypy.tsetyr( 1980 )
          et2 = spiceypy.str2et( AMBIGSTR )

          #
          # Calculate the number of years between the two ET
          # representations, ~100.
          #
          print( 'Years between evaluations: {0:20.6f}'.\
          format( (et2 - et1)/spiceypy.jyear()))

          #
          # Reset the default year to 1969.
          #
          spiceypy.tsetyr( 1969 )

          #
          # Done. Unload the kernels.
          #
          spiceypy.kclear


      if __name__ == '__main__':
         xtic()

Run the code example

::

      Original time string     : Mar 15, 2003 12:34:56.789 AM PST
      Corresponding ET         :     100989360.974561

      Time in string format 1  : Sat Mar 15 01:34:56 PDT 2003
      Time in string format 2  : Sat Mar 15 01:34  03 (2452713.85760 JDUTC)
      Time in string format 3  : 01:34:56.789 A.M. PDT March 15, 2003
      Years between evaluations:           100.000000

Lesson 5: Error Handling
------------------------------

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

::

      from __future__ import print_function
      from builtins import input

      #
      # Import the CSPICE-Python interface.
      #
      import spiceypy
      from spiceypy.utils.support_types import SpiceyError

      def aderr():

          #
          # Set initial parameters.
          #
          SPICETRUE =  True
          SPICEFALSE=  False
          doloop    =  SPICETRUE

          #
          # Load the data we need for state evaluation.
          #
          spiceypy.furnsh( 'aderr.tm' )

          #
          # Start our input query loop to the user.
          #
          while (doloop):

              #
              # For simplicity, we request only one input.
              # The program calculates the state vector from
              # Earth to the user specified target 'targ' in the
              # J2000 frame, at ephemeris time zero, using
              # aberration correction LT+S (light time plus
              # stellar aberration).
              #
              targ = input( 'Target: ' )


              if targ == 'NONE':
                  #
                  # An exit condition. If the user inputs NONE
                  # for a target name, set the loop to stop...
                  #
                  doloop = SPICEFALSE

              else:

                #
                # ...otherwise evaluate the state between the Earth
                # and the target. Initialize an error handler.
                #
                try:

                    #
                    # Perform the state lookup.
                    #
                    [state, ltime] = spiceypy.spkezr(targ, 0., 'J2000',
                                                     'LT+S',   'EARTH')

                    #
                    # No error, output the state.
                    #
                    print( 'R : {0:20.6f} {1:20.6f} '
                           '{2:20.5f}'.format(*state[0:3]))
                    print( 'V : {0:20.6f} {1:20.6f} '
                           '{2:20.6f}'.format(*state[3:6]) )
                    print( 'LT: {0:20.6f}\n'.format(float(ltime)))

                except SpiceyError as err:

                   #
                   # What if spiceypy.spkezr signaled an error?
                   # Then spiceypy signals an error to python.
                   #
                   # Examine the value of 'e' to retrieve the
                   # error message.
                   #
                  print( err )
                  print( )


          #
          # Done. Unload the kernels.
          #
          spiceypy.kclear


      if __name__ == '__main__':
         aderr()

Run the code example

Now run the code with various inputs to observe behavior. Begin the run
using known astronomical bodies, e.g. “Moon”, “Mars”, “Pluto barycenter”
and “Puck”. Recall the SpiceyPy default units are kilometers, kilometers
per second, kilograms, and seconds. The 'R' marker identifies the
(X,Y,Z) position of the body in kilometers, the 'V' marker identifies
the velocity of the body in kilometers per second, and the 'LT' marker
identifies the one-way light time between the bodies at the requested
evaluation time.

::

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

      Toolkit version: N0066

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

::

      Target: Casper

      =====================================================================
      ===========

      Toolkit version: N0066

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

::

      Target: Venus
      R :     -80970027.540532    -139655772.573898      -53860125.95820
      V :            31.166910           -27.001056           -12.316514
      LT:           567.655074

      Target:

The look-up succeeded despite two errors in our run. The SpiceyPy system
can respond to error conditions (not system errors) in much the same
fashion as languages with catch/throw instructions.

Lesson 6: Windows, and Cells
------------------------------

Programming task
^^^^^^^^^^^^^^^^^

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

::

         [ a , b ]
            i   i

where

::

         a    <   b
          i   -    i

The intervals within a window are both ordered and disjoint. That is,
the beginning of each interval is greater than the end of the previous
interval:

::

         b  <  a
          i     i+1

A common use of the windows facility is to calculate the intersection
set of a number of time intervals.

.. _code-solution-5:

Code Solution
^^^^^^^^^^^^^

::

      from __future__ import print_function

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
          los = [ 'Jan 1, 2003 22:15:02', 'Jan 2, 2003  4:43:29',
                  'Jan 4, 2003  9:55:30', 'Jan 4, 2003 11:26:52',
                  'Jan 5, 2003 11:09:17', 'Jan 5, 2003 13:00:41',
                  'Jan 6, 2003 00:08:13', 'Jan 6, 2003  2:18:01' ]

          #
          # A second set of intervals representing the times for which
          # an acceptable phase angle exists between the ground station,
          # the body and the Sun.
          #
          phase = [ 'Jan 2, 2003 00:03:30', 'Jan 2, 2003 19:00:00',
                    'Jan 3, 2003  8:00:00', 'Jan 3, 2003  9:50:00',
                    'Jan 5, 2003 12:00:00', 'Jan 5, 2003 12:45:00',
                    'Jan 6, 2003 00:30:00', 'Jan 6, 2003 23:00:00' ]

          #
          # Load our meta kernel for the leapseconds data.
          #
          spiceypy.furnsh( 'win.tm' )

          #
          # SPICE windows consist of double precision values; convert
          # the string time tags defined in the 'los' and 'phase'
          # arrays to double precision ET. Store the double values
          # in the 'loswin' and 'phswin' windows.
          #
          los_et = spiceypy.str2et( los   )
          phs_et = spiceypy.str2et( phase )

          loswin = spiceypy.stypes.SPICEDOUBLE_CELL( MAXSIZ )
          phswin = spiceypy.stypes.SPICEDOUBLE_CELL( MAXSIZ )

          for i in range(0, int( MAXSIZ/2 ) ):
              spiceypy.wninsd( los_et[2*i], los_et[2*i+1], loswin )
              spiceypy.wninsd( phs_et[2*i], phs_et[2*i+1], phswin )

          spiceypy.wnvald( MAXSIZ, MAXSIZ, loswin )
          spiceypy.wnvald( MAXSIZ, MAXSIZ, phswin )

          #
          # The issue for consideration, at what times do line of
          # sight events coincide with acceptable phase angles?
          # Perform the set operation AND on loswin, phswin,
          # (the intersection of the time intervals)
          # place the results in the window 'sched'.
          #
          sched = spiceypy.wnintd( loswin, phswin )

          print( 'Number data values in sched : '
                 '{0:2d}'.format(spiceypy.card(sched)) )

          #
          # Output the results. The number of intervals in 'sched'
          # is half the number of data points (the cardinality).
          #
          print( ' ' )
          print( 'Time intervals meeting defined criterion.' )

          for i in range( spiceypy.card(sched)//2):

             #
             # Extract from the derived 'sched' the values defining the
             # time intervals.
             #
             [left, right ] = spiceypy.wnfetd( sched, i )

             #
             # Convert the ET values to UTC for human comprehension.
             #
             utcstr_l = spiceypy.et2utc( left , 'C', 3 )
             utcstr_r = spiceypy.et2utc( right, 'C', 3 )

             #
             # Output the UTC string and the corresponding index
             # for the interval.
             #
             print( '{0:2d}   {1}   {2}'.format(i, utcstr_l, utcstr_r))


          #
          # Summarize the 'sched' window.
          #
          [meas, avg, stddev, small, large] = spiceypy.wnsumd( sched )

          print( '\nSummary of sched window\n' )

          print( 'o Total measure of sched    : {0:16.6f}'.format(meas))
          print( 'o Average measure of sched  : {0:16.6f}'.format(avg))
          print( 'o Standard deviation of ' )
          print( '  the measures in sched     : '
                 '{0:16.6f}'.format(stddev))

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
          print( 'o Index of shortest interval: '
                 '{0:2d}'.format(int(small/2)) )
          print( 'o Index of longest interval : '
                 '{0:2d}'.format(int(large/2)) )

          #
          # Done. Unload the kernels.
          #
          spiceypy.kclear

      if __name__ == '__main__':
         win()

Run the code example

The output window has the name \`sched' (schedule).

Output the amount of data held in \`sched' compared to the maximum
possible amount.

::

      Number data values in sched :  6

List the time intervals for which a line of sight exists during the time
of a proper phase angle.

::

      Time intervals meeting defined criterion.
       0   2003 JAN 02 00:03:30.000   2003 JAN 02 04:43:29.000
       1   2003 JAN 05 12:00:00.000   2003 JAN 05 12:45:00.000
       2   2003 JAN 06 00:30:00.000   2003 JAN 06 02:18:01.000

Finally, an analysis of the \`sched' data. The measure of an interval
[a,b] (a <= b) equals b-a. Real values output in units of seconds.

::

      Summary of sched window

      o Total measure of sched    :     25980.000009
      o Average measure of sched  :      8660.000003
      o Standard deviation of
        the measures in sched     :      5958.550217
      o Index of shortest interval:  1
      o Index of longest interval :  0

.. _related-routines-2:

Related Routines
^^^^^^^^^^^^^^^^^^

::

       --   spiceypy.wncomd determines the compliment of a window with
            respect to a defined interval.

       --   spiceypy.wncond contracts a window's intervals.

       --   spiceypy.wndifd : Calculate the difference between two windows;
            i.e. every point existing in the first but not the second.

       --   spiceypy.wnelmd returns TRUE or FALSE if a value exists in a
            window.

       --   spiceypy.wnexpd expands the size of the intervals in a window.

       --   spiceypy.wnextd extracts a window's endpoints .

       --   spiceypy.wnfild fills gaps between intervals in a window.

       --   spiceypy.wnfltd filter/removes small intervals from a window.

       --   spiceypy.wnincd determines if an interval exists within a
            window.

       --   spiceypy.wninsd inserts an interval into a window.

       --   spiceypy.wnreld compares two windows. Comparison operations
            available, equality '=', inequality '<>', subset '<=' and '>=',
            proper subset '<' and '>'.

       --   spiceypy.wnunid calculates the union of two windows.

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

::

      from __future__ import print_function
      from builtins import input

      #
      # Import the CSPICE-Python interface.
      #
      import spiceypy


      def tostan(alias):

          value = alias

          #
          # As a convenience, let's alias a few common terms
          # to their appropriate counterpart.
          #
          if alias == 'meter':

              #
              # First, a 'meter' by any other name is a
              # 'METER' and smells as sweet ...
              #
              value = 'METERS'

          elif (alias == 'klicks')        \
              or (alias == 'kilometers')  \
              or (alias =='kilometer'):

              #
              # ... 'klicks' and 'KILOMETERS' and 'KILOMETER'
              # identifies 'KM'....
              #
              value = 'KM'

          elif alias == 'secs':

              #
              # ... 'secs' to 'SECONDS'.
              #
              value = 'SECONDS'

          elif alias == 'miles':

              #
              # ... and finally 'miles' to 'STATUTE_MILES'.
              # Normal people think in statute miles.
              # Only sailors think in nautical miles - one
              # minute of arc at the equator.
              #
              value = 'STATUTE_MILES'

          else:
              pass


          #
          # Much better. Now return. If the input matched
          # none of the aliases, this function did nothing.
          #
          return value

      def units():

          #
          # Display the Toolkit version string with a spiceypy.tkvrsn
          # call.
          #
          vers = spiceypy.tkvrsn( 'TOOLKIT' )
          print('\nConvert demo program compiled against CSPICE '
                'Toolkit ' + vers)

          #
          # The user first inputs the name of a unit of measure.
          # Send the name through tostan for de-aliasing.
          #
          funits = input( 'From Units : '  )
          funits = tostan( funits )

          #
          # Input a double precision value to express in a new
          # unit format.
          #
          fvalue = float(input( 'From Value : ' ))

          #
          # Now the user inputs the name of the output units.
          # Again we send the units name through tostan for
          # de-aliasing.
          #
          tunits = input( 'To Units   : ' )
          tunits = tostan( tunits )

          tvalue = spiceypy.convrt( fvalue, funits, tunits)
          print( '{0:12.5f} {1}'.format(tvalue, tunits) )

      if __name__ == '__main__':
         units()

Run the code example

Run a few conversions through the application to ensure it works. The
intro banner gives us the Toolkit version against which the application
was linked:

::

      Convert demo program compiled against CSPICE Toolkit CSPICE_N0066
      From Units : klicks
      From Value : 3
      To Units   : miles
           1.86411 STATUTE_MILES

Now we know. Three kilometers equals 1.864 miles.

Legend states Pheidippides ran from the Marathon Plain to Athens. The
modern marathon race (inspired by this event) spans 26.2 miles. How far
in kilometers?

::

      Convert demo program compiled against CSPICE Toolkit CSPICE_N0066
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

::

      from __future__ import print_function

      #
      # Import the CSPICE-Python interface.
      #
      import spiceypy

      def xconst():

          #
          # All the function have the same calling sequence:
          #
          #    VALUE = function_name()
          #
          #    some_procedure( function_name() )
          #
          # First a simple example using the seconds per day
          # constant...
          #
          print( 'Number of (S)econds (P)er (D)ay         : '
                 '{0:19.12f}'.format(spiceypy.spd() ))

          #
          # ...then show the value of degrees per radian, 180/Pi...
          #
          print( 'Number of (D)egrees (P)er (R)adian      : '
                 '{0:19.16f}'.format(spiceypy.dpr() ))

          #
          # ...and the inverse, radians per degree, Pi/180.
          # It is obvious spiceypy.dpr() equals 1.d/spiceypy.rpd(), or
          # more simply spiceypy.dpr() * spiceypy.rpd() equals 1
          #
          print( 'Number of (R)adians (P)er (D)egree      : '
                 '{0:19.16f}'.format(spiceypy.rpd() ))

          #
          # What's the value for the astrophysicist's favorite
          # physical constant (in a vacuum)?
          #
          print( 'Speed of light in KM per second         : '
                 '{0:19.12f}'.format(spiceypy.clight() ))

          #
          # How long (in Julian days) from the J2000 epoch to the
          # J2100 epoch?
          #
          print( 'Number of days between epochs J2000')
          print( '  and J2100                             : '
                 '{0:19.12f}'.format(  spiceypy.j2100()
                                     - spiceypy.j2000() ))

          #
          # Redo the calculation returning seconds...
          #
          print( 'Number of seconds between epochs' )
          print( '  J2000 and J2100                       : '
                 '{0:19.5f}'.format(spiceypy.spd() *          \
                 (spiceypy.j2100() - spiceypy.j2000() ) ))


          #
          # ...then tropical years.
          #
          val =(spiceypy.spd()/spiceypy.tyear()    ) *        \
               (spiceypy.j2100()- spiceypy.j2000() )
          print( 'Number of tropical years between' )
          print( '  epochs J2000 and J2100                : '
                 '{0:19.12f}'.format(val))


          #
          # Finally, how can I convert a radian value to degrees.
          #
          print( 'Number of degrees in Pi/2 radians of arc: '
                 '{0:19.16f}'.format(  spiceypy.halfpi()
                                     * spiceypy.dpr()      ))

          #
          # and degrees to radians.
          #
          print( 'Number of radians in 250 degrees of arc : '
                 '{0:19.16f}'.format(250. * spiceypy.rpd() ))

      if __name__ == '__main__':
         xconst()

Run the code example

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
^^^^^^^^^^^^^^^^^^

::

       --   spiceypy.b1900 : Julian Date of the epoch Besselian Date 1900.0

       --   spiceypy.b1950 : Julian date of the epoch Besselian Date 1950.0

       --   spiceypy.j1900 : Julian date of 1900 JAN 0.5 this corresponds
            to calendar date 1899 DEC 31 12:00:00

       --   spiceypy.j1950 : Julian date of 1950 JAN 1.0 this corresponds
            to calendar date 1950 JAN 01 00:00:00

       --   spiceypy.twopi : double precision value of 2 * Pi

       --   spiceypy.pi : double precision value of Pi

       --   spiceypy.jyear : seconds per Julian year (365.25 Julian days)
