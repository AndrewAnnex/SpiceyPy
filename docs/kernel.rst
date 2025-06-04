*****************************
SPICE Kernel Required Reading
*****************************

This required reading document is reproduced from the original NAIF
document available at `https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/kernel.html <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/kernel.html>`_

.. note::
   These required readings documents were translated from documentation for N67 CSPICE.
   These pages may not be updated as frequently as the CSPICE version, and so may be out of date.
   Please consult the changelog_ for more information. 

.. _changelog: ./changelog.html

.. important::
   NOTE any functions postfixed by "_" mentioned below are
   Fortan-SPICE functions unavailable in SpiceyPy
   as the NAIF does not officially support these with "_c" function
   wrappers within the CSPICE API.
   If these functions are necessary for your work
   please contact the NAIF to request that they be added to
   the CSPICE API

Abstract
========

| The kernel subsystem loads and unloads kernels, retrieves loaded
  data, and for text kernels, inserts data into the kernel pool.

Document Outline
================

| This document has five major sections.

- Introduction to kernels

- Kernel type identification and kernel naming

- Binary kernel specifications

- Text kernel specifications and interfaces, including extra
  rules for meta-kernels

- Kernel management

"Introduction to kernels" should be read by anyone new to SPICE or
needing a refresher about kernels.
"Kernel type identification and kernel naming" contains
specifications for kernel architecture and type identification and
restrictions and recommendations concerning kernel file naming.

"Binary kernel specifications" points the reader to other SPICE
documents for most information on binary kernels.

"Text kernel specifications and interfaces," which includes extra
rules for meta-kernels, provides a good deal of technical detail for
both producers and consumers (users) of text kernels.

"Kernel management" contains important information about managing
and obtaining information about both text and binary kernels.

Appendix A discusses the notion of "competing data."

Appendix B provides definitions of terms used in this document with
SPICE-specific meaning.

Appendix C provides a listing of kernel subsystem functions.

Appendix D provides a summary of key text kernel parameter values.

Appendix E provides the revision history of this document.


Introduction to Kernels
=======================



| Files containing the data used by SPICE are known as kernels
  (sometimes called "kernel files"). Two kernel architectures
  exist, referred to as text kernels and binary kernels. Text kernels
  consist of human readable ASCII text; binary kernels consist of
  mostly non-ASCII data.

Within each architecture there are several kernel types.


Kernel Types
------------

| The SPICE text kernels are:

- text form of planetary constants (text PCK)

- leapseconds (LSK)

- spacecraft clock coefficients (SCLK)

- instrument geometry (IK)

- reference frame specifications (FK)

- meta-kernels (MK)

The SPICE binary kernels are:

- ephemeris for vehicles, planets, satellites, comets,
  asteroids (SPK)

- orientation (attitude) of a spacecraft or other structure
  (CK)

- special binary form of planetary constants containing only
  orientation (binary PCK)

- shape models or topographic data for extended objects (DSK)

- mission events (EK)


Text Kernels and the Kernel Pool
---------------------------------

| Text kernels are used where the amount of data being stored is
  relatively small, and where easy human readability and revision are
  important.

Text kernels should contain descriptive information, provided by the
kernel producer, describing the sources and intended uses of the
kernel data.

Text kernels associate values with variables using a "name =
value(s)" form of assignment. The kernel pool is the repository of
the information provided in these assignments. Populating the kernel
pool occurs in either or both of two ways: by loading text kernels --
by far the most used method -- or by using pool subsystem functions.

Once "name = value(s)" assignments provided in a text kernel have
been loaded into the kernel pool the value(s) are said to be
associated with the names. You may access these data through kernel
pool look-up functions using the names as keys to find the associated
values. The kernel pool look-up functions are described in detail a
bit later in this document. However, some higher-level and more often
used functions also access data loaded into the kernel pool. Two
tables in the tutorial named "Summary of Key Points" provide
details.


Binary Kernels
-----------------

| Binary kernels store large data sets of primarily non-ASCII data,
  using either the DAF or DAS format (see the technical reference
  documents `daf.req <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/daf.html>`__ and
  `das.req <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/das.html>`__ for details). For all but EK binary
  kernels, loading the binary kernel does not cause the subsystem
  associated with the kernel's type to read the principal kernel
  data; rather only a small amount of descriptive data are read so
  the subsystem becomes aware of the existence of the kernel and the
  nature of the data contained therein. The subsystem physically
  reads primary binary kernel data only when a data request is made
  by a kernel reader function.

For EK binary kernels, the descriptive data mentioned above, and some
database schema information, are read in at kernel load time.
Principal data are read only when an EK query is made by a kernel
reader function.

Data from binary kernels do NOT get placed in the kernel pool; the
pool is used only for text kernel data.

Binary kernels contain a "comment area" where important
descriptive information in ASCII form should be provided by the
kernel producer.

On occasion one may be given, or need to make, a "transfer format"
file. This is an ASCII-format representation of a binary kernel, used
in early versions of CSPICE to port binary kernels between dissimilar
computers (e.g. IEEE - Little endian to IEEE - Big endian, or
vice-versa). For the most part these transfer format files are no
longer needed due to the addition of run-time translation
capabilities in the binary kernel readers. But there are some
situations when transfer format binary kernels are still needed;
refer to the tutorial named "Porting Kernels" for details.


SPICE Kernel Type Identification and Kernel Naming
===================================================

SPICE Kernel Type Identification
---------------------------------

| Most SPICE users don't need to know about kernel type
  identification, but since this aspect of kernels is used later on
  in this document we have to explain the concept here.

The first 6 to 8 bytes of a SPICE kernel are used for file type
identification. In binary and text kernels this identifier consists
of two string IDs separated by the "/" character. The first ID,
identifying the file architecture of the kernel file ("DAF",
"DAS", "KPL"), is always three characters long. The second ID,
identifying the file type of the kernel file ("SPK", "PCK",
"IK", "SCLK", etc.), is two to four characters long.

In transfer format files this file type identifier consists of a
single string ID. See the Convert User's Guide for details.

In binary kernels the kernel type identifier always occupies the
first eight bytes. If the combined length of the kernel architecture
ID, the "/" character, and the kernel type ID is less than 8
characters, the identifier is padded on the right to eight characters
using blanks (e.g. "DAF/SPK ", "DAS/EK "). The correct
identifier is written to a binary kernel automatically when the
kernel is created by calling the kernel type specific "open new
file" function -- :py:meth:`~spiceypy.spiceypy.spkopn` for SPK
files, :py:meth:`~spiceypy.spiceypy.ckopn` for CK files, etc. If a
binary kernel is created by calling an architecture specific "open
new file" function -- dafonw_c for DAF files,
:py:meth:`~spiceypy.spiceypy.dasonw` for DAS files, etc., -- it is
the caller's responsibility to specify the correct kernel type in the
corresponding input argument of these functions to make sure the
correct kernel type identifier is written into the kernel.

In text kernels the kernel type identifier occupies the first six to
eight characters and is followed by optional trailing blanks and then
by the end-of-line terminator character(s), resulting in the
identifier appearing on a line by itself. If the combined length of
the kernel architecture ID, the "/" character, and the kernel type
ID is less than 8 characters, the identifier can, but does not have
to be padded on the right to eight characters using blanks (e.g.
"KPL/SCLK", "KPL/IK ", etc.). Since most text kernels are
created manually using a text editor, it is the responsibility of the
person making the kernel to put the correct identifier by itself on
the first line of the kernel.

In transfer format files the SPICE kernel type identifier occupies
the first six characters of the file and is followed by the expanded
name of the format (e.g. "DAFETF NAIF DAF ENCODED TRANSFER FILE").
The correct kernel type identifier is written to a transfer format
file automatically when the file is created by the SPICE utility
programs TOXFR or SPACIT. See their user guides,
`toxfr.ug <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/ug/toxfr.html>`__ and
`spacit.ug <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/ug/spacit.html>`__, for details.

The SPICE kernel type identifiers used in modern SPICE kernels are as
follows.

.. code-block:: text

            Binary Kernels:

               SPK           DAF/SPK
               CK            DAF/CK
               DSK           DAS/DSK
               PCK           DAF/PCK
               EK            DAS/EK

            Text Kernels:

               FK            KPL/FK
               IK            KPL/IK
               LSK           KPL/LSK
               MK            KPL/MK
               PCK           KPL/PCK
               SCLK          KPL/SCLK

            Transfer format files:

               DAF           DAFETF
               DAS           DASETF



Some older kernels used an earlier version of the kernel type
identifier. In these kernels one would find:

.. code-block:: text

              NAIF/DAF
              NAIF/DAS

The Toolkit includes the :py:meth:`~spiceypy.spiceypy.getfat`
function to retrieve the kernel file architecture and kernel type
encapsulated in the SPICE kernel type identifier.
A text kernel not having a kernel type identifier can, in fact, be
processed by high-level functions, and by low-level functions other
than :py:meth:`~spiceypy.spiceypy.getfat` that use text kernel
data. However, NAIF strongly recommends kernel creators to provide
the identifier.


Recommendations on Kernel File Naming
--------------------------------------

| CSPICE places a few restrictions on kernel file names beyond those
  imposed by your operating system:

- Kernel file names, including path specifications, must not
  exceed 255 characters.

- Use of embedded blanks in kernel file names is not supported
  by CSPICE. Such names generally will not be recognized when passed
  as command-line arguments to CSPICE utility programs.

- Host system "shell variables" or "environment
  variables" cannot be passed as input arguments to CSPICE
  functions.

Mission operations teams often include a variety of identifying and
user information in kernel names, making them quite long. This
practice is probably unavoidable, but kernel producers should be
aware that when the mission's SPICE archive is prepared for delivery
to the Planetary Data System (PDS), all kernels to be archived must
have names consistent with PDS standards, including a limitation to a
"36.3" format (1 to 36 alphanumeric characters, followed by the
decimal character, followed by 1 to 3 alphanumeric characters) and
using only letters, digits and the underscore character.
NAIF recommends kernel names use only lower case letters. NAIF
further recommends one follows the conventions established for kernel
name extensions, shown below.

.. code-block:: text

               .bc    binary CK
               .bds   binary DSK
               .bes   binary Sequence Component EK
               .bpc   binary PCK
               .bsp   binary SPK
               .tf    text FK
               .ti    text IK
               .tls   text LSK
               .tm    text meta-kernel (FURNSH kernel)
               .tpc   text PCK
               .tsc   text SCLK

Binary Kernel Specifications
=============================



| Other than the general specifications and recommendations in the
  section "Kernel type identification and kernel naming" that are
  applicable to binary kernels, specifications for the various binary
  kernels are provided in kernel type specific technical reference
  documents, such as "SPK Required Reading" and "CK Required
  Reading."


Text Kernel Specifications and Interfaces
==========================================



| The specifications and restrictions discussed below apply to any
  text kernel. However, the special type of text kernel known as a
  meta-kernel (sometimes called a "FURNSH kernel") has additional
  restrictions; these are discussed later in a section on
  meta-kernels.


Text Kernel Specifications
--------------------------

| Often the easiest and best way to create a text kernel is to start
  with an existing text kernel, editing it to meet your needs. But
  knowing text kernel rules is still important. Those rules are
  documented in the remainder of this section.

As the name implies, SPICE text kernels contain printable ASCII text
(ASCII code 32-126). Text kernels may not contain non-printing
characters, excepting tab (ASCII code 9). However NAIF recommends
against use of tabs in text kernels. NAIF also recommends caution be
exercised when cutting/pasting text from a formatted document into a
text kernel; the text characters displayed in a document may not be
in the accepted ASCII range, in which case the text kernel parser
will fail when reading those characters.

Assignments in SPICE text kernels have a "name = value(s)" or
"name += value(s)" format. We illustrate this format by way of an
example using an excerpt from a SPICE text planetary constants kernel
(PCK). The format description given below applies to all SPICE text
kernels; the specific data names shown in this example apply only to
text PCK kernels.

Vectors of values are enclosed in parentheses.

The example begins with a SPICE kernel type identifier and is then
filled out with a combination of descriptive information, called
comment blocks, and data blocks.

.. code-block:: text

    KPL/PCK

    Planets first. Each has quadratic expressions for the direction
    (RA, Dec) of the north pole and the location and rotation state
    of the prime meridian. Planets with satellites (except Pluto)
    also have linear expressions for the auxiliary (phase) angles
    used in the nutation and libration expressions of their satellites.

    \begindata


    BODY399_POLE_RA        = (    0.      -0.64061614  -0.00008386  )

    BODY399_POLE_DEC       = (  +90.      -0.55675303  +0.00011851  )

    BODY399_PM             = (   10.21  +360.98562970  +0.          )

    BODY399_LONG_AXIS      = (    0.                                )

    BODY3_NUT_PREC_ANGLES  = (  125.045    -1935.53
                                249.390    -3871.06
                                196.694  -475263.
                                176.630  +487269.65
                                358.219   -36000.    )

    \begintext


    Each satellite has similar quadratic expressions for the pole and

    prime meridian. In addition, some satellites have nonzero nutation
    and libration amplitudes. (The number of amplitudes matches the
    number of auxiliary phase angles of the primary.)

    \begindata


    BODY301_POLE_RA      = (  270.000   -0.64061614  -0.00008386   )

    BODY301_POLE_DEC     = (  +66.534   -0.55675303  +0.00011851   )

    BODY301_PM           = (   38.314  +13.1763581    0.           )

    BODY301_LONG_AXIS    = (    0.                                 )


    BODY301_NUT_PREC_RA  = (  -3.878  -0.120  +0.070  -0.017   0.     )

    BODY301_NUT_PREC_DEC = (  +1.543  +0.024  -0.028  +0.007   0.     )

    BODY301_NUT_PREC_PM  = (  +3.558  +0.121  -0.064  +0.016  +0.025  )

    \begintext

    Here we include the radii of the satellites and planets.

    \begindata

    BODY399_RADII    = (     6378.140    6378.140     6356.755  )
    BODY301_RADII    = (     1738.       1738.        1738.     )

    \begintext

End of example text kernel.
In this example there are several comment blocks providing
information about the data. Except for the comments appearing just
after the kernel type identifier and before the first data block, all
comment blocks are introduced by the control word

.. code-block:: text

      \begintext

A comment block may contain any number of comment lines. Once a
comment block has begun, no special characters are required to
introduce subsequent lines of comments within that block. A comment
block is terminated by the control word

.. code-block:: text

      \begindata

or by the end of the kernel file.
The

.. code-block:: text

      \begindata

control word also serves to introduce a block of data that will be
stored in the kernel pool. A data block is terminated by the control
word

.. code-block:: text

      \begintext

or by the end of the kernel file.
Each of these control words must appear on a line by itself, and each
may be preceded by white space.

Within each data block there are one or more variable assignments.
Each variable assignment consists of three components:

#. A variable name.

#. An assignment operator. This must be "=" (direct
   assignment) or "+=" (incremental assignment).

#. A scalar or vector value.



Variable Name Rules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| A variable name can include any printable character except:

#. " " (space)

#. "," (comma)

#. "(" (open parentheses)

#. ")" (close parentheses)

#. "=" (equal sign)

#. TAB character

Variable names must not exceed 32 characters in length.
Variable names are case-sensitive. Note that this behavior is
different from that of most CSPICE high-level functions, which tend
to ignore case in string inputs. Variable names that don't have the
expected case will be invisible to CSPICE functions that try to fetch
their values. Since high-level CSPICE functions that use kernel
variables accept only upper case names, NAIF recommends upper case
always be used for variable names.

NAIF recommends you do not use a variable name with "+" as the
last character.


Assignment Rules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Direct assignments supersede previous assignments, whereas
  incremental assignments append the specified values to the set
  created by previous assignments. For example, the series of
  assignments

.. code-block:: text

      BODY301_NUT_PREC_RA  = -3.878
      BODY301_NUT_PREC_RA += -0.120
      BODY301_NUT_PREC_RA += +0.070
      BODY301_NUT_PREC_RA += -0.017
      BODY301_NUT_PREC_RA += 0.

has the same effect as the single assignment

.. code-block:: text

      BODY301_NUT_PREC_RA = (  -3.878  -0.120  +0.070  -0.017   0 )



Variable Value Rules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Values may be scalar (a single item) or vectors (two or more
  items). A value may be a number, a string, or a special form of a
  date.

Numeric values may be provided in integer or floating point
representation, with an optional sign. Engineering notation using an
"E" or "D" is allowed. All numeric values, including integers,
are stored as double precision numbers. Examples of assignments using
valid numeric formats:

.. code-block:: text

      BODY399_RADII     = ( 6378.1366     6378.1366     6356.7519   )
      BODY399_RADII     = ( 6.3781366D3   6.3781366D3   6.3567519D3 )
      BODY399_RADII     = ( 6.3781366d3   6.3781366d3   6.3567519d3 )
      BODY399_RADII     = ( 6.3781366E3   6.3781366E3   6.3567519E3 )
      BODY399_RADII     = ( 6.3781366e3   6.3781366e3   6.3567519e3 )
      BODY399_RADII     = ( 6378          6378          6357        )

String values are supplied by quoting the string using a single quote
at each end of the string, for example

.. code-block:: text

            DISTANCE_UNITS = 'KILOMETERS'

This quoting convention is independent of the SPICE Toolkit language
version being used.
All string values, whether part of a scalar or vector assignment,
must not exceed 80 characters on a given line. Creating a string
value longer than 80 characters is possible through continuation of
an assignment over multiple lines; this is described later.

There is no practical limit on the length of a string value other
than as mentioned in the section on String Continuation below.

If you need to include a single quote in the string value, use the
FORTRAN convention of "doubling" the quote.

.. code-block:: text

            MESSAGE = 'You can"t always get what you want.'

Date values may be entered in a wide variety of formats, using two
methods. The easiest method is to enter a date as a string, as
described above. There are no restrictions on the format of a date
string entered as a string, but if you wish to later use that date
string in SPICE software the string must conform to SPICE date/time
formation rules (see the "Time Required Reading" document for
details).
A second method for entering dates, unique to text kernels, uses an
"@" syntax. Some examples:

.. code-block:: text

            CALIBRATION_DATES = ( @31-JAN-1987,
                                  @feb/4/1987,
                                  @March-7-1987-3:10:39.221 )

Dates entered using the "@" syntax may not contain embedded
blanks.
Dates entered using the "@" syntax are converted to double
precision seconds past the reference epoch J2000 as they are read
into the kernel pool.

Note that NO time system specification (e.g. UTC or TDB) is implied
by dates using the "@" syntax. Association of a time system with
such dates is performed by the software that uses them. For example,
in SPICE leapseconds kernels, such dates represent UTC times; in
frames kernels, they represent TDB times. You should refer to
software user's guides or API documentation to understand the
interpretation of these dates for your application.

Vector values, whether of numeric, string or date types, are enclosed
in parentheses, and adjacent components are separated by either white
space (blank or carriage return, but not TAB) or commas. Multiple
components can be placed on a single line. Multiple lines may be used
to continue a list of values. Individual numeric, date, and string
values may not be split across lines, but a long string may be
continued using multiple substrings. See the section "Additional
Text Kernel Syntax Rules" below for details.

.. code-block:: text

            MISSION_UNITS = ( 'KILOMETERS','SECONDS'
                              'KILOMETERS/SECOND' )

The types of values assigned to a given kernel pool variable must all
be the same. If you attempt to make an assignment such as the one
shown here:

.. code-block:: text

            ERROR_EXAMPLE = ( 1, 2, 'THREE', 4, 'FIVE' )



the kernel pool reader will regard the assignment as erroneous and
reject it.
|

Additional Text Kernel Syntax Rules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Line Length

    All assignments, or portions of an assignment, occurring on a line
    must not exceed 132 characters, including the assignment operator and
    any leading or embedded white space.

Blank Lines

    Blank lines in data blocks are ignored.

String Continuation

    It is possible to treat specified, consecutive elements of a string
    array as a single "continued" string. String continuation is
    indicated by placing a user-specified sequence of non-blank
    characters at the end (excluding trailing blanks) of each string
    value that is to be concatenated to its successor. The string
    continuation marker can be any positive number of printing characters
    that fit in a string value (except not true for meta-kernels).

    For example, if the character sequence

    .. code-block:: text

                //

    is used as the continuation marker, the assignment

    .. code-block:: text

                CONTINUED_STRINGS = ( 'This //  ',
                                      'is //  ',
                                      'just //',
                                      'one long //',
                                      'string.',
                                      'Here"s a second //',
                                      'continued //'
                                      'string.'              )

    allows the string array elements on the right hand side of the
    assignment to be treated as the two strings

    .. code-block:: text

                This is just one long string.
                Here's a second continued string.

    Everything between the single quotes, including white space and the
    continuation marker, counts towards the limit of 80 characters in the
    length of each string element.
    The SPICE function :py:meth:`~spiceypy.spiceypy.stpool`, and ONLY
    that function, provides the capability of retrieving continued
    strings from the kernel pool. See the discussion below under
    "Fetching Data from the Kernel Pool" or the header of
    :py:meth:`~spiceypy.spiceypy.stpool` for further information.


Maximum Numbers of Variables and Variable Values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| All variable values from all text kernels loaded into your program
  are stored in the kernel pool. There are upper bounds on the total
  numbers of variables and variable values.

See Appendix D for the numeric values of these limits.


Treatment of Invalid Text Kernels
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| If during a call to :py:meth:`~spiceypy.spiceypy.furnsh`, an
  error is detected in a text kernel, CSPICE will signal an error. By
  default, a diagnostic message will be displayed to standard output
  and the program will terminate.

If the SPICE error handling subsystem is in RETURN mode,
:py:meth:`~spiceypy.spiceypy.furnsh` will return control to the
calling program. RETURN mode is typically used in interactive
programs.

In the latter case, all data loaded from the text kernel prior to
discovery of the error will remain loaded.

If, in RETURN mode, an error occurs while a meta-kernel is being
loaded, all files listed in that meta-kernel that have already been
loaded will remain loaded. Files listed in the meta-kernel later than
the file for which the failure occurred will not be loaded.

Note that continuing program operation after a load failure could,
due to changes in the availability of competing data, result in
performing computations with data that were not planned to be used.


Additional Meta-kernel Specifications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| A meta-kernel (also known as a "FURNSH kernel") is a special
  instance of a text kernel. Its use has been discussed earlier in
  this document. In addition to the text kernel specifications above,
  a meta-kernel has the following restrictions.

- When continuing the value field (a file name) over multiple
  lines, the continuation marker must be a single "+" character.

- The maximum length of any file name, including any path
  specification, is 255 characters.

- Embedded blanks are not allowed in path or file names.



Text Kernel Interfaces - Fetching Data from the Kernel Pool
------------------------------------------------------------

.. note::
  For most SPICE users the accessing of text kernel data occurs
  inside of high-level CSPICE functions, so you may choose to skip
  the rest of this section. But if you need to work with text kernel
  variables that are not present in traditional text kernels, and
  thus are not accessed by high-level SPICE functions, read on.

The values of variables stored in the kernel pool may be retrieved
using the functions:

:py:meth:`~spiceypy.spiceypy.gcpool`
   Used to fetch character data from the kernel pool.

:py:meth:`~spiceypy.spiceypy.gdpool`
   Used to fetch double precision data from the kernel pool.

:py:meth:`~spiceypy.spiceypy.gipool`
   Used to fetch integer data from the kernel pool. Within the kernel
   pool all numeric data are stored as double precision values. This
   interface is provided as a convenience so that users may insert
   and retrieve integer data from the kernel pool without having to
   worry about converting between double precision values and
   integers.

   Non-integer, numeric kernel variable values retrieved by calling
   :py:meth:`~spiceypy.spiceypy.gipool` are rounded by gipool to
   the nearest integer. Kernel creators must ensure that values to be
   read using :py:meth:`~spiceypy.spiceypy.gipool` are within the
   range representable by integers.

:py:meth:`~spiceypy.spiceypy.stpool`
   Used to fetch continued strings from the kernel pool.

See function documentation for specifics on function parameters.


Informational Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Four routines are provided for retrieving general information about
  the contents of the kernel pool.

:py:meth:`~spiceypy.spiceypy.dtpool`
   Returns information about the existence, dimension and type of a
   specified kernel pool variable.

:py:meth:`~spiceypy.spiceypy.expool`
   Returns information on the existence of a numeric kernel pool
   variable.

:py:meth:`~spiceypy.spiceypy.gnpool`
   Allows retrieval of names of kernel pool variables that match a
   string pattern.

:py:meth:`~spiceypy.spiceypy.szpool`
   Returns information about the size of various structures used in
   the implementation of the kernel pool.

These routines are discussed at length in their respective source
code headers and referenced NAIF CSPICE documentation.


Section 5 -- Kernel Management
==============================



| The kernel subsystem provides functions_c to load and unload SPICE
  files, known as kernels, and provides other kernel management and
  information functions. These functions_c are part of the
  "KEEPER" subsystem.


Loading Kernels
---------------

| For the SPICE system to use kernels, they must be made known to the
  system and opened at run time. This activity is called "loading"
  kernels. SPICE provides a simple interface for this purpose.

The principal kernel loading function is named
:py:meth:`~spiceypy.spiceypy.furnsh` (pronounced "furnish"). A
kernel database stores the existence information for any kernel (text
or binary) loaded by :py:meth:`~spiceypy.spiceypy.furnsh`. The
subsystem provides a set of functions that enable an application to
find the names and attributes of kernels stored in the database.

Early versions of CSPICE loaded kernels using functions specific to
each kernel type. Code written for the binary kernels also supported
a kernel unload facility. CSPICE continues to support the original
kernel loaders and unloaders, but anyone writing new code should use
the :py:meth:`~spiceypy.spiceypy.furnsh` function instead of the
kernel-specific functions.

NAIF recommends loading multiple kernels using a "meta-kernel"
rather than by executing multiple calls to
:py:meth:`~spiceypy.spiceypy.furnsh`. ("Meta-kernels" are
sometimes called "furnsh kernels.") A meta-kernel is a SPICE text
kernel that lists the names of the kernels to load. At run time, the
user's application supplies the name of the meta-kernel as an input
argument to :py:meth:`~spiceypy.spiceypy.furnsh`. For example,
instead of loading kernels using the code fragment:

.. code-block:: python


      from spiceypy import *

      furnsh("leapseconds.tls")
      furnsh("mgs.tsc")
      furnsh("generic.bsp")
      furnsh("mgs.bc")
      furnsh("earth.bpc")
      furnsh("mgs.bes")



one may now write

.. code-block:: python

      from spiceypy import *

      furnsh("kernels.tm")


where the file "kernels.tm" is a SPICE text meta-kernel containing
the lines

.. code-block:: text

      KPL/MK
      \begindata

      KERNELS_TO_LOAD = ( 'leapseconds.tls',
                          'mgs.tsc',
                          'generic.bsp',
                          'mgs.bc',
                          'earth.bpc',
                          'mgs.bes'           )

      \begintext

This technique has the important advantage of enabling a user to
easily change the set of kernels to be loaded without modifying his
source code.
While far less robust, it is also possible to provide the names of
kernels to be loaded as input arguments via a list or other iterable to
:py:meth:`~spiceypy.spiceypy.furnsh`. For example, one may write

.. code-block:: python

      kernels = [
          "leapseconds.tls",
          "mgs.tsc",
          "generic.bsp",
          "mgs.bc",
          "earth.bpc",
          "mgs.bes",
      ]

      furnsh(kernels)


Kernel Priority
---------------

| It is fairly common that two kernels of the same type - for example
  two SPKs - to have "competing data." "Competing" means that
  both kernels could provide an answer to the user's request for
  data, even though the numeric results would likely be different.
  This usually occurs when the two kernels were produced using
  different input data and mostly contain non-competing data, but do
  have some overlap in time. When two or more kernels contain
  competing data a kernel loaded later has higher priority than
  kernel(s) loaded earlier. This is true whether using separate calls
  to :py:meth:`~spiceypy.spiceypy.furnsh` for each kernel to be
  loaded, or a single call to furnsh_c with a list of kernels to be
  loaded, or a call to :py:meth:`~spiceypy.spiceypy.furnsh` that
  loads a meta-kernel. See Appendix A for a more complete discussion
  on competing data.

If orientation data for a given body-fixed frame are provided in both
a text PCK and a binary PCK, data from the binary PCK always have
higher priority.


Path Symbols in Meta-kernels
-----------------------------

| Inside a meta-kernel it is sometimes necessary to qualify kernel
  names with their path names. To reduce both typing and the need to
  continue kernel names over multiple lines, meta-kernels allow users
  to define symbols for paths. This is done using two kernel
  variables:

.. code-block:: text

      PATH_VALUES
      PATH_SYMBOLS

To create symbols for path names, one assigns an array of path names
to the variable PATH_VALUES. Next, one assigns an array of
corresponding symbol names to the variable PATH_SYMBOLS. The nth
symbol in the second array represents the nth path name in the first
array.
Then you can prefix with path symbols the kernel names specified in
the KERNELS_TO_LOAD variable. Each symbol is prefixed with a dollar
sign to indicate that it is in fact a symbol.

Suppose in our example above the MGS kernels reside in the path

.. code-block:: text

      /flight_projects/mgs/SPICE_kernels

and the other kernels reside in the path

.. code-block:: text

      /generic/SPICE_kernels

Then we can add paths to our meta-kernel as follows:

.. code-block:: text

      \begindata

      PATH_VALUES  = ( '/flight_projects/mgs/SPICE_kernels',
                       '/generic/SPICE_kernels'              )

      PATH_SYMBOLS = ( 'MGS',
                       'GEN' )


      KERNELS_TO_LOAD = ( '$GEN/leapseconds.tls',
                          '$MGS/mgs.tsc',
                          '$GEN/generic.bsp',
                          '$MGS/mgs.bc',
                          '$GEN/earth.bpc',
                          '$MGS/mgs.bes'           )

      \begintext

It is not required that paths be abbreviated using path symbols; it's
simply a convenience available to you.
Caution: the symbols defined using PATH_SYMBOLS are not related to
the symbols supported by a host shell or any other operating system
interface.


Specifying Kernels Using Relative Paths
-----------------------------------------

| When a kernel is specified with a relative path, this path should
  be valid at the time when :py:meth:`~spiceypy.spiceypy.furnsh` is
  called and stay valid for the rest of the application run. This is
  required because SPICE stores kernel names as provided by the
  caller and uses them to open and close binary kernels as needed by
  the DAF/DAS handle manager subsystem (behind the scenes, to allow
  reading many more binary kernels than available logical units), and
  to automatically reload into the POOL the rest of text kernels that
  should stay loaded when a particular text kernel is unloaded.

Changing the working directory from within an application during an
application run after calling :py:meth:`~spiceypy.spiceypy.furnsh`
to load kernels specified using relative paths is likely to
invalidate stored paths and prevent open/close and unload operations
mentioned above. A simple workaround when this is needed is to
specify kernels using absolute paths.


Keeping Track of Loaded Kernels
--------------------------------

| The KEEPER subsystem maintains a database of the load operations
  that :py:meth:`~spiceypy.spiceypy.furnsh` has performed during a
  program run. This is implemented using data structures of fixed
  size, so there is a limit on the maximum number of loaded kernels
  that the KEEPER subsystem can accommodate.

When a kernel is loaded using :py:meth:`~spiceypy.spiceypy.furnsh`,
a new entry is created in the database of loaded kernels, whether or
not the kernel is already loaded.

All load and unload operations (see the discussion of
:py:meth:`~spiceypy.spiceypy.unload` below) affect the list of
loaded kernels and therefore affect the results returned by the
functions :py:meth:`~spiceypy.spiceypy.ktotal`,
:py:meth:`~spiceypy.spiceypy.kdata`, and
:py:meth:`~spiceypy.spiceypy.kinfo`, all of which are discussed
below under "Finding Out What's Loaded."


Reloading Kernels
------------------

| Reloading an already loaded kernel creates another (duplicate)
  entry in the database of loaded kernels, and thus decreases the
  available space in that list.
  :py:meth:`~spiceypy.spiceypy.furnsh`'s treatment of reloaded
  kernels is thus slightly different from that performed by the
  CSPICE low-level kernel loaders, which handle a reload operation by
  first unloading the kernel in question, then loading it.


Changing Kernel Priority
-------------------------

| The recommended method of increasing the priority of a loaded
  binary kernel, or of a meta-kernel containing binary kernels, is to
  unload it using :py:meth:`~spiceypy.spiceypy.unload` (see below),
  then reload it using :py:meth:`~spiceypy.spiceypy.furnsh`. This
  technique helps reduce clutter in
  :py:meth:`~spiceypy.spiceypy.furnsh`'s kernel list.


Load Limits
--------------

| :py:meth:`~spiceypy.spiceypy.furnsh` can currently keep track of
  up to 5000 kernels. The list of loaded kernels may contain multiple
  entries for a given kernel, so the number of distinct loaded
  kernels would be smaller if some have been reloaded. Unloading
  kernels using :py:meth:`~spiceypy.spiceypy.unload` frees room in
  the kernel list, so there is no limit on the total number of load
  and corresponding unload operations performed in a program run.

The DAF/DAS handle manager system imposes its own limit on the number
of DAF binary kernels that may be loaded simultaneously. This limit
is currently set to a total of 5000 DAF kernels.


Finding Out What's Loaded
--------------------------

| SPICE-based applications may need to determine at run time which
  files have been loaded. Applications may need to find the DAF or
  DAS handles of loaded binary kernels so that the kernels may be
  searched. Some applications may need to unload kernels to make room
  for others, or change the priority of loaded kernels at run time.

SPICE provides kernel access functions to support these needs. For
every loaded kernel, an application can find the name of the kernel,
the kernel type (text or one of SPK, CK, DSK, PCK, or EK), the
kernel's DAF or DAS handle if applicable, and the name of the
meta-kernel used to load the kernel, if applicable.

The function :py:meth:`~spiceypy.spiceypy.ktotal` returns the count
of loaded kernels having their types on a caller-supplied list of one
or more types. The function :py:meth:`~spiceypy.spiceypy.kdata`
returns information on the nth kernel of the set having the types
named in the list. The two functions are normally used together. The
following example shows how an application could retrieve summary
information on the currently loaded SPK files:

.. code-block:: python

    #!/usr/bin/env python
    """
    This script uses SpiceyPy to list the names of loaded SPK kernel files.
    """

    import spiceypy as spice


    def main():
        # Get the total number of loaded SPK kernels.
        count = spice.ktotal("spk")
        if count == 0:
            print("No SPK files loaded at this time.")
        else:
            print("The loaded SPK files are:\n")
        # Loop over each loaded kernel and retrieve its data.
        for which in range(count):
            # kdata returns a tuple: (file, file type, source, handle)
            file, file_type, source, handle = spice.kdata(which, "spk")
            print(file)


    if __name__ == "__main__":
        main()

Above, the input argument
"spk"

is a kernel type specifier. More generally, a blank-delimited list of
types may be provided as the input argument. The set of types that
may appear in the list is shown below.

.. code-block:: text

               SPK  --- All SPK kernels are counted in the total
               CK   --- All CK kernels are counted in the total
               PCK  --- All binary PCK kernels are counted in the
                        total
               DSK  --- All DSK kernels are counted in the total
               EK   --- All EK kernels are counted in the total
               TEXT --- All text kernels that are not meta-
                        kernels are included in the total
               META --- All meta-kernels are counted in the
                        total
               ALL  --- Every type of kernel is counted in the
                        total

In this example, 'filtyp' is a string indicating the type of kernel.
'handle' is the file handle if the file is a binary SPICE kernel.
'source' is the name of the meta-kernel used to load the kernel, if
applicable.

CSPICE also contains the function
:py:meth:`~spiceypy.spiceypy.kinfo` that returns summary information
about a kernel whose name is already known.
:py:meth:`~spiceypy.spiceypy.kinfo` is called as follows:

.. code-block:: python

        # will throw a NotFoundError if file is not found
        filtyp, source, handle = kinfo(file)


Unloading Kernels
-----------------

| CSPICE-based applications may need to remove loaded kernels.
  Possible reasons for this are:

- to make room to load other kernels

- to change the priority of loaded kernel data

- to change the set of kernel data visible to CSPICE

The function :py:meth:`~spiceypy.spiceypy.unload` acts as an
inverse to :py:meth:`~spiceypy.spiceypy.furnsh`: passing a kernel
name to :py:meth:`~spiceypy.spiceypy.unload` undoes the effect of
the previous load operation performed on that kernel using
:py:meth:`~spiceypy.spiceypy.furnsh`. For binary kernels that have
been loaded just once, the meaning of this is simple: the kernel is
closed and the database referring to the file is adjusted to reflect
the absence of the kernel.
Text kernels are unloaded by clearing the kernel pool and then
reloading the other text kernels not designated for removal.

Note that unloading text kernels has the side effect of wiping out
any kernel variables and associated values that had been entered in
the kernel pool using any of the kernel pool assignment functions,
such as :py:meth:`~spiceypy.spiceypy.pcpool`. It is important to
consider whether this side effect is acceptable when writing code
that may unload text kernels or meta-kernels.

Call :py:meth:`~spiceypy.spiceypy.unload` as follows:

.. code-block:: python

         unload(kernel)


Unloading a meta-kernel involves unloading all the kernels referenced
by the meta-kernel.


Loading of Non-native Text and Binary Kernels
-----------------------------------------------

| The various platforms supported by CSPICE use different end-of-line
  (EOL) indicators in text files:

.. code-block:: text

      Environment                  Native End-Of-Line
                                   Indicator
      ___________                  _____________________

      PC DOS/Windows                <CR><LF>
      Unix                          <LF>
      Linux                         <LF>
      Mac OS X                      <LF>

As of CSPICE version N0059, the SPICE text kernel loader
:py:meth:`~spiceypy.spiceypy.furnsh` (and the deprecated loader
:py:meth:`~spiceypy.spiceypy.ldpool`) can read and parse non-native
text files. (Caution: the FORTRAN SPICELIB text kernel readers do not
include this capability.)
The CSPICE text file reader, :py:meth:`~spiceypy.spiceypy.rdtext`,
does not possess the capability to read non-native text files.

Starting with the version N0052 release of the SPICE Toolkit
(January, 2002), supported platforms are able to read DAF-based
binary kernels (SPK, CK and binary PCK) that were written using a
non-native binary representation. This access is read-only; any
operations requiring writing to the file--for example, adding
information to the comment area, or appending additional ephemeris
data-- require prior conversion of the kernel to the native binary
file format. See the "Convert User's Guide" for details.


Manipulating Kernel Pool Contents
----------------------------------

| The main way one adds to or changes the contents of the kernel pool
  is by "loading" a SPICE text kernel using the function
  :py:meth:`~spiceypy.spiceypy.furnsh`. However, the kernel
  subsystem also provides several other functions that allow one to
  change the contents of the kernel pool.

:py:meth:`~spiceypy.spiceypy.clpool`
   Clears (initializes) the kernel pool, deleting all the variables
   in the pool.

:py:meth:`~spiceypy.spiceypy.kclear`
   Clears (empties) the kernel pool, the kernel database (same effect
   as unloading all kernels), and re-initializes the subsystem. Use
   of :py:meth:`~spiceypy.spiceypy.kclear` also clears programmatic
   kernel pool assignments from the "put-pool" routines, e.g.
   :py:meth:`~spiceypy.spiceypy.pipool`,
   :py:meth:`~spiceypy.spiceypy.pdpool`,
   :py:meth:`~spiceypy.spiceypy.pcpool`.

:py:meth:`~spiceypy.spiceypy.dvpool`
   Deletes a specific variable from the kernel pool.

:py:meth:`~spiceypy.spiceypy.lmpool`
   Similar in effect to loading a text kernel using
   :py:meth:`~spiceypy.spiceypy.furnsh`, but the data being loaded
   into the pool come from an array of strings instead of a text
   kernel.

:py:meth:`~spiceypy.spiceypy.pcpool`
   Programmatically inserts a single character variable and its
   associated values into the kernel pool. The assignment is direct
   (the values replace any previously existing set of values
   associated with the variable.)

:py:meth:`~spiceypy.spiceypy.pdpool`
   Programmatically inserts a single double precision variable and
   its associated values into the kernel pool. The assignment is
   direct.

:py:meth:`~spiceypy.spiceypy.pipool`
   Programmatically inserts a single integer variable and its
   associated values into the kernel pool. The assignment is direct.

The following code fragment shows how the data provided in a
leapseconds kernel (LSK) could be loaded using
:py:meth:`~spiceypy.spiceypy.lmpool`.


.. code-block:: python

    #!/usr/bin/env python
    """
    This script uses SpiceyPy to demonstrate using lmpool.
    """

    import spiceypy as spice


    def main():
        text = [
            "DELTET/DELTA_T_A = 32.184",
            "DELTET/K = 1.657D-3",
            "DELTET/EB  = 1.671D-2",
            "DELTET/M = ( 6.239996 1.99096871D-7 )",
            "DELTET/DELTA_AT = ( 10, @1972-JAN-1",
            "                     11, @1972-JUL-1",
            "                     12, @1973-JAN-1",
            "                     13, @1974-JAN-1",
            "                     14, @1975-JAN-1",
            "                     15, @1976-JAN-1",
            "                     16, @1977-JAN-1",
            "                     17, @1978-JAN-1",
            "                     18, @1979-JAN-1",
            "                     19, @1980-JAN-1",
            "                     20, @1981-JUL-1",
            "                     21, @1982-JUL-1",
            "                     22, @1983-JUL-1",
            "                     23, @1985-JUL-1",
            "                     24, @1988-JAN-1",
            "                     25, @1990-JAN-1",
            "                     26, @1991-JAN-1",
            "                     27, @1992-JUL-1",
            "                     28, @1993-JUL-1",
            "                     29, @1994-JUL-1",
            "                     30, @1996-JAN-1",
            "                     31, @1997-JUL-1",
            "                     32, @1999-JAN-1",
            "                     33, @2006-JAN-1",
            "                     34, @2009-JAN-1  )",
        ]
        #
        # Add the contents of the buffer to the kernel pool:
        #
        spice.lmpool(text)


    if __name__ == "__main__":
        main()

See the docstrings of the kernel subsystem functions for specific
details regarding their use.


Detecting Changes in the Kernel Pool Using Watchers
---------------------------------------------------

| Since loading SPICE text kernels often happens only at program
  initialization, a function that relies on data in the kernel pool
  may run more efficiently if it can store a local copy of the values
  needed and update these only when a change occurs in the kernel
  pool. Two functions are available that allow a quick test to see
  whether kernel pool variables have been updated.

:py:meth:`~spiceypy.spiceypy.swpool`
   Sets up a watcher on a a list of variables so that a specified
   agent can be notified when any variables on the list have been
   updated.

:py:meth:`~spiceypy.spiceypy.cvpool`
   Indicates whether or not any of an agent's variables have been
   updated since the last time the agent checked with the pool.

See the docstrings of these functions for details and examples of their
use.


Appendix A -- Discussion of Competing Data
==========================================

Binary Kernels
--------------

| For binary kernels, the conditions resulting in competing data
  depend on the kernel type.

SPKs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| For SPKs, a segment contains data of a single SPK type, providing
  ephemeris for a single target measured relative to a single center
  and given in a single reference frame, spanning between specified
  start and stop times. If ephemeris data from any two segments,
  whether found in a single SPK file or in two SPK files, are for the
  same target and have an overlap in the time spans covered, then the
  two kernels are said to have some competing data. Note that centers
  play no role in the competition: two segments with the same target
  and different centers may compete.

By definition, SPKs contain continuous data during the time interval
covered by a segment, so there is no chance for a "data gap" in a
segment within a higher priority file (later loaded file) leading to
a state lookup coming from a segment in a lower priority file.

SPK segment chaining may lead to a problem. It may happen that you
have loaded into your program sufficient SPK data to compute the
desired state or position vector, but CSPICE nevertheless returns an
error message saying insufficient ephemeris data have been loaded.
This can occur if a higher priority SPK segment, for which there are
not sufficient additional SPK data to fully construct your requested
state or position vector, is masking (blocking) a segment that is
part of a viable (complete) chain. See the BACKUP section of the SPK
tutorial for further discussion about this.

Having competition between two SPKs can be a relatively common
occurrence when using mission operations kernels, but is far less
likely when using PDS-archived SPICE data sets because of the
clean-up and consolidation actions usually taken when an archive
delivery is produced.


CKs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| For CKs, a segment contains data of a single CK type providing the
  orientation of a reference frame associated with one object or
  structure, such as a spacecraft or instrument (sometimes called the
  "to" reference frame), relative to a second reference frame,
  generally referred to as the base reference frame (sometimes called
  the "from" reference frame), spanning between specified start
  and stop times.

If transformation data from any two segments, whether found in a
single CK file or in two CK files, are for the same object/structure
(are for the same "to" frame) and have an overlap in the time span
covered, then the two kernels may have competing data. But read on.

However, unlike for SPKs, competition between CK files goes beyond
segment-level considerations. The so-called "continuous" CK types
(Types 2 through 5) do not necessarily provide orientation results
for any epoch falling within a segment--there may be real data gaps.
And the now little used Type 1 CK, containing discrete instances of
orientation data, can be thought of as containing mostly data gaps.

While some of the Toolkit software used to compute orientation
obtained from CKs can provide an orientation result within a gap,
this is usually not the case. See the CK tutorial and the "CK
Required Reading" document for discussions on interpolation
intervals, tolerance, and how the various CK readers work.

CK segment chaining may lead to a problem. It may happen that you
have loaded into your program sufficient CK data to compute the
desired rotation matrix, but CSPICE nevertheless returns an error
message saying insufficient data have been loaded. This can occur if
a higher priority CK segment, for which there are not sufficient
additional CK data to fully construct your requested rotation matrix,
is masking (blocking) a segment that is part of a viable (complete)
chain.

Having competition between two CKs can be a relatively common
occurrence when using mission operations kernels, but is far less
likely when using PDS-archived SPICE data sets because of the
clean-up and consolidation actions usually taken when an archive
delivery is prepared.


Binary PCKs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| For binary PCKs, a segment contains data of a single binary PCK
  type providing orientation of a reference frame associated with a
  single object (a body-fixed frame), relative to a second reference
  frame, which is always an inertial frame, spanning between
  specified start and stop times. If orientation data from any
  segment in one binary PCK and orientation data from any segment in
  a second binary PCK are for the same body-fixed frame and overlap
  in time, then the two kernels are said to have competing data.

At present binary PCKs produced by NAIF exist only for the earth and
the moon. Having competition between the latest high precision, short
term earth orientation binary PCK and the lower precision, long term
predict earth orientation binary PCK is a clear possibility -- be
sure to load the long term predict file first to ensure any higher
precision files also loaded have higher priority.

Orientation data provided in any loaded binary PCK have priority over
what would have otherwise been competing data provided in any loaded
text PCK.


Text Kernels
--------------



| If a given variable name has two or more assignments, with the
  final assignment made using the "=" operator, whether within a
  single loaded text kernel, or from multiple loaded text kernels, or
  achieved using CSPICE functions, the last such assignment
  supersedes all previous occurrences of the assignment. This
  superseding happens no matter how many values are contained in the
  last assignment. (It's as if all previous assignments for the
  subject name had never occurred.)

It is generally best to unload a text kernel before loading another
one containing competing data.


Appendix B -- Glossary of Terms
================================


Agent
    | A string associated with a list of kernel variables to be watched
      for updates. The string can be passed to the update checking
      function :py:meth:`~spiceypy.spiceypy.cvpool` to determine
      whether any of the variables on the list have been updated.

    Often the string is the name of a function that needs to be informed
    if any of a specified set of kernel variables has had a change made
    to its associated value(s).


Assignment
    | What appears inside data blocks of a text kernel. Each assignment
      consists of three parts: a variable (also called variable name), an
      operator, and a scalar or vector value. For example,

    .. code-block:: text

          BODY399_RADII = ( 6378.14   6378.14   6356.75 )

    is an assignment with a vector value.
    Once a text kernel is loaded, the value(s) on the right hand sides of
    the assignments become associated with the variable names on the
    corresponding left hand sides. See "direct assignment" and
    "incremental assignment" below.


Continued string
    | A string value composed of two or more pieces--called
      elements--each of which is no longer than 80 characters.


Control words
    | Markers indicating the start of data or comment blocks,
      specifically

    .. code-block:: text

          \begindata
          \begintext



Direct assignment
    | A text kernel assignment, made using the "=" operator. When a
      direct assignment is processed during text kernel loading, it
      associates one or more values with a variable name, and in so
      doing, replaces any previous such associations.


Element
    | Within the kernel pool the length of a string value is limited to
      80 characters. A string value that is longer than 80 characters may
      be stored in and extracted from the pool by chunking it into
      pieces--called elements--each of which is no longer than 80
      characters. Such a string is referred to as a "continued
      string."


Incremental assignment
    | A text kernel assignment made using the "+=" operator. When an
      incremental assignment is processed during text kernel loading, it
      appends one or more values to the list of values already associated
      with a variable name. Any previous such associations are NOT
      replaced; rather they are supplemented with the new value(s).
      Incremental assignments may be made to variables that didn't
      previously exist in the kernel pool; in such cases incremental
      assignments are equivalent to direct assignments.


Keeper (subsystem)
    | The SPICE subsystem used to keep track of (manage) loaded kernel
      files. In this sense it is also involved with the unloading of
      kernels.


Kernel pool (sometimes just called "the pool")
    | A specially managed area of program memory where data from text
      kernel assignment statements are stored.


Kernel variable
    | Often a synonym for "variable name," but may refer to the
      combination of a variable name and its associated values.


Meta-kernel (also known as "FURNSH kernel")
    | A special kind of text kernel, used to name a collection of kernels
      that are to be loaded into a user's application at run-time. May
      include the path names for the kernels as well as the file names.


Operator
    | Within SPICE text kernels, an operator is either "=" or the
      sequence of "+" and "=", written as "+=". The former is
      used to make direct assignments, the latter is used to make
      incremental assignments.


Principal data
    | This term occurs only within this document. It is used to refer to
      the "elemental" data contained in a kernel, as opposed to
      meta-data or bookkeeping data. For instance, within an SPK the
      principal data are the polynomials or other numeric data providing
      ephemeris information. Not part of the principal data are the
      descriptive information placed in the comment area, the file
      architecture IDs, and the indexes that help the subsystem quickly
      find the principal data needed to return a state vector.


Value
    | That which appears on the right-hand side of an assignment. May be
      a single value or a vector of values.

    variable name = value(s)


Variable name
    | That which appears on the left-hand side of an assignment.

    variable name = value(s)


Vector value
    | Two or more values associated with a single variable name.


Appendix C -- Summary of Routines
===================================



| Each of the function names is a mnemonic that translates into a
  short description of the function's purpose.

      :py:meth:`~spiceypy.spiceypy.clpool`
          Clear the pool of kernel variables
      :py:meth:`~spiceypy.spiceypy.cvpool`
          Check variable in the pool for update
      :py:meth:`~spiceypy.spiceypy.dtpool`
          Return information about a kernel pool variable
      :py:meth:`~spiceypy.spiceypy.dvpool`
          Delete a variable from the kernel pool
      :py:meth:`~spiceypy.spiceypy.expool`
          Confirm the existence of a pool kernel variable
      :py:meth:`~spiceypy.spiceypy.furnsh`
          Furnish a program with SPICE kernels
      :py:meth:`~spiceypy.spiceypy.gcpool`
          Get character data from the kernel pool
      :py:meth:`~spiceypy.spiceypy.gdpool`
          Get double precision values from the kernel pool
      :py:meth:`~spiceypy.spiceypy.gipool`
          Get integers from the kernel pool
      :py:meth:`~spiceypy.spiceypy.gnpool`
          Get names of kernel pool variables
      :py:meth:`~spiceypy.spiceypy.kclear`
          Clear and re-initialize the kernel database
      :py:meth:`~spiceypy.spiceypy.kdata`
           Return information about the nth loaded kernel
      :py:meth:`~spiceypy.spiceypy.kinfo`
           Return information about a specific loaded kernel
      :py:meth:`~spiceypy.spiceypy.ktotal`
          Return the number of kernels loaded using KEEPER
      :py:meth:`~spiceypy.spiceypy.lmpool`
          Load variables from memory into the pool
      :py:meth:`~spiceypy.spiceypy.pcpool`
          Put character strings into the kernel pool
      :py:meth:`~spiceypy.spiceypy.pdpool`
          Put double precision values into the kernel pool
      :py:meth:`~spiceypy.spiceypy.pipool`
          Put integers into the kernel pool
      :py:meth:`~spiceypy.spiceypy.stpool`
          Return a string associated with a kernel variable
      :py:meth:`~spiceypy.spiceypy.swpool`
          Set watch on a pool variable
      :py:meth:`~spiceypy.spiceypy.szpool`
          Get size parameters of the kernel pool
      :py:meth:`~spiceypy.spiceypy.unload`
          Unload a kernel



Appendix D -- Summary of Key Text Kernel Parameter Values
==========================================================



| Text kernel limits

.. code-block:: text

      Maximum variable name length:                         32
      Maximum length of any element of a string value:      80
      Maximum number of distinct variables:              26003
      Maximum number of numeric variable values:        400000
      Maximum number of character strings
       stored in the kernel pool as values:              15000
      Maximum length of a file name, including any
       path specification, placed in a meta-kernel:        255

Other applicable limits

.. code-block:: text

      Maximum total number of kernel files of any
      type that can be loaded simultaneously:             5000



