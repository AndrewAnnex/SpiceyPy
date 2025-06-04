********************
PCK Required Reading
********************

This required reading document is reproduced from the original NAIF
document available at `https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/pck.html <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/pck.html>`_

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
 | The Planetary Constants Kernel (PCK) subsystem provides
   cartographic and physical constants data for Solar System bodies.
   CSPICE software uses these data when determining observation
   geometry dependent on the size, shape, and orientation of planets,
   natural satellites, comets, and asteroids.

Intended Audience
-----------------

 | This document is recommended reading for all users of PCK files.

References
----------


#. KERNEL Required Reading
   (`kernel.req <./kernel.html>`__).

#. NAIF IDS Required Reading
   (`naif_ids.req <./naif_ids.html>`__).

#. FRAMES Required Reading
   (`frames.req <./frames.html>`__).

#. SPK Required Reading (`spk.req <./spk.html>`__).

#. TIME Required Reading (`time.req <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/time.html>`__).

#. ROTATIONS Required Reading
   (`rotation.req <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/rotation.html>`__).

#. Double Precision Array Files Required Reading
   (`daf.req <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/daf.html>`__).

#. ''Planetary Geodetic Control Using Satellite Imaging,''
   Journal of Geophysical Research, Vol. 84, No. B3, March 10, 1979,
   by Thomas C. Duxbury.

#. ''Report of the IAU/IAG Working Group on Cartographic
   Coordinates and Rotational Elements of the Planets and Satellites:
   2000.''

#. ''Report of the IAU/IAG Working Group on Cartographic
   Coordinates and Rotational Elements: 2006.''

#. ''Report of the IAU Working Group on Cartographic
   Coordinates and Rotational Elements: 2009.''



Introduction
============

 | The functionality of the PCK subsystem is supplied by data files
   called `PCK files` (or PCKs) and by CSPICE subroutines that can
   read and interpret the data in these files.

 Historically, only one type of PCK existed, the text PCK (called the
 "P constants kernel.") These ASCII files can be easily viewed and
 modified via text editor. The current SPICE system also supports a
 non-ascii binary PCK. These files contain more precise body
 orientation information in binary format (no size and shape data).
 This format permits large amounts of data to be stored and quickly
 accessed. As of the date of this document, binary PCK files exists
 only for the moon, earth, and the asteroid Eros.

 The purpose of the PCK and associated software is to provide SPICE
 users a convenient mechanism for supplying planetary physical
 constants to application programs. CSPICE software reads files
 conforming to these formats and returns both the data contained in
 such files and a few commonly used numeric quantities derived from
 the kernel data.

Body Codes
-----------

 | NAIF software uses a system of integer codes to conveniently
   represent celestial bodies, locations such as barycenters, Lagrange
   points, and spacecraft. The NAIF IDS Required Reading document,
   `naif_ids <./naif_ids.html>`__, describes this system in
   detail.

 In this document, the following features of the code system will be
 relied on:

 - The code for the barycenter of the nth planetary system is
   n. The count starts at 1, which stands for Mercury; e.g. the code
   for Jupiter's barycenter is 5. The code for the Sun is 10. SPICE
   maintains Pluto as the 9th planet.

 - The code for the nth planet's barycenter is n

 - The code for the nth planet's mass center is n99; e.g, the
   code for the Earth (Earth barycenter is 3) is 399.

 - Natural satellites have ID codes of the form

      .. code-block:: text

                        PNN, where

                               P  is  1, ..., 9
                           and NN is 01, ... 98

      or

      .. code-block:: text

                        PXNNN, where

                               P   is    1, ...,  9,
                               X   is    0  or    5,
                           and NNN is  001, ... 999

                        Codes with X = 5 are provisional.

 - For example, the code for the Earth's moon (moon 1 of body 1) is 301, and the code for Ganymede (moon 3 of body 599) is 503.



Epochs and Reference Frames
---------------------------

 | Some constants that frequently appear in PCK files are associated
   with a particular epoch and with a particular reference frame. For
   example, PCK files released by NAIF typically contain constants
   that define the axes of various body-fixed planetocentric
   coordinate systems, given relative to a specified inertial
   reference frame, as a function of time. In this sort of definition,
   the independent variable, time, is measured relative to a specified
   reference epoch.

 Within SPICE, reference frames are identified by short character
 strings such as 'J2000'. The names of the body-fixed reference frames
 are usually constructed by adding the prefix `IAU\_` to the name
 of the body, for example `IAU_MARS` for Mars. The exception from
 this rule are body-fixed reference frames associated with
 high-precision orientation provided in binary PCK files. For more
 details see FRAMES Required Reading,
 `frames <./frames.html>`__.

 However, SPICE also has a system of integer codes used by some
 routines to specify reference frames. This coding system is also
 described in detail in `frames <./frames.html>`__.

Planetocentric Coordinates
--------------------------

 | The body-fixed `Planetocentric` coordinate system referred to in
   this document is defined for solar system bodies as follows:

 - The x-axis of the Planetocentric coordinate system for a
   specified body lies both in the body's equatorial plane and in the
   plane containing the body's prime meridian.

 - The z-axis is parallel to the body's mean axis of rotation
   and points North of the invariable plane of the solar system
   (regardless of the body's spin direction). The north pole is the
   pole of rotation.

 - The y-axis is defined as the cross product of the z and x
   axes, in that order. Thus, the frame is right-handed.

 The above definition implies that the axes of a planetocentric system
 are time-varying. Thus a complete specification of the axes requires
 identification of an epoch as well as the body.


Using the PCK System: Overview
===============================

 | This section describes how PCK files and software are used in
   application programs.

 The use of PCK data in an application program requires three steps:

#. Selecting the appropriate PCK file(s) for the problem.

#. Reading the PCK data into the program.

#. Using the data within the program.

 Step 1 is not necessarily trivial since there may be no single set of
 `best values` for physical constants of interest; the `best`
 values - if such exist - depend on the problem. The user's judgment,
 supported by comments and usage notes in the PCK file, is required
 for this step.
 Step 2 is referred to as `loading` a PCK file. Text PCK files are
 loaded by calling the CSPICE subroutine
 :py:meth:`~spiceypy.spiceypy.furnsh` and supplying the name of the
 PCK file to load as the input argument or by loading a meta kernel
 that lists the PCK. All data in a text PCK file is read into memory
 when the file is loaded by an application program at run-time. Load
 binary PCKs in the same way. The program can access all loaded data
 during the program run, unless deliberately overwritten or unloaded.
 Multiple text and multiple binary PCKs can be used simultaneously.

 The data available from binary PCKs take precedence over that from
 text PCKs. If data for a requested planetary constant and time period
 is covered by a loaded binary PCK file, the subsystem returns and
 uses the binary data. If multiple binary PCK files are loaded, the
 most recently loaded file takes precedence, down to the binary file
 loaded earliest. The subsystem defaults to text PCK data when no
 binary PCK data is available. If the user loaded multiple text PCKs,
 and those PCKs contained variable assignments using the same variable
 name, the later loads overwrite the assignments defined by earlier
 loads.

 Step 3, using loaded PCK data, is accomplished via calls to CSPICE
 routines. At the lowest level, these access routines allow the
 calling program to retrieve specified data that has been read from
 one or more PCK files. Higher-level access routines can return
 quantities derived from loaded PCK data.

 For text PCK files, the PCK software can be thought of as
 `buffering` all data loaded from PCK files: the data from these
 files is retained in memory. Therefore, repeated calls to the PCK
 access routines do not incur the inefficiency of re-reading data from
 files. For binary PCK file, like the case of the SPK and CK readers,
 only a portion of the most recently used information is buffered.

 The data structure used by CSPICE to maintain associations of text
 kernel variable names and values is called the `kernel pool.` Data
 loaded into memory via :py:meth:`~spiceypy.spiceypy.furnsh` is
 referred to as `being present in the kernel pool.` There is no
 analog to the kernel pool for binary PCK files.

Orientation Models used by PCK Software
========================================

 | The orientation models used by SPICE PCK access routines all
   express the direction of the pole and location of the prime
   meridian of a body with respect to an inertial reference frame, as
   a function of time. This information defines the coordinate axes of
   the `Body Equator and Prime Meridian` system.

 The orientation models use three Euler angles to describe the pole
 and prime meridian location: the first two angles, in order, are the
 right ascension and declination (henceforth RA and DEC) of the north
 pole of a body as a function of time. The third angle is the prime
 meridian location (represented by \`W'), which is expressed as a
 rotation about the north pole, also a function of time. The
 coordinate transformation defined by the Euler angles is represented
 by the matrix product

.. code-block:: text

       [ W ]    [ Pi/2 - Dec ]    [ Pi/2 + RA ]
            3                 1                3

where

.. code-block:: text

       [ W ]
            i

 denotes the matrix that rotates a coordinate system by W radians
 about the ith coordinate axis (or rotates vectors by -W radians about
 the same axis), using the right hand rule. (This notation is
 explained in detail in `rotation.req <./req/rotation.html>`__).
 In PCK files, the time arguments of functions that define orientation
 always refer to Barycentric Dynamical Time (TDB), measured in
 centuries or days past a specified epoch such as J2000, which is
 Julian ephemeris date 2451545.0. The time units expected by the
 CSPICE software are ephemeris days for prime meridian motion and
 ephemeris centuries for motion of the pole.


The Two Formats of PCK files
============================

 | There are two general forms for PCK files, text and binary files.
   Text files are ASCII and can be created and modified with an
   editor. Therefore, they are easily changed and read. Binary files
   are created via CSPICE programs and have a particular format and
   architecture. They cannot be examined or changed with an editor.
   These files require CSPICE software for their manipulation. Binary
   PCKs can contain more data and are faster to use. In the PCK case,
   the binary files contain higher precision data than the text files.
   Binary PCKs contain only orientation data, while text PCKs usually
   include orientation, size, and shape data, and may include other
   physical data associated with a body.

Detection of Non-native Text Files
-----------------------------------

 | The various platforms supported by CSPICE use different end-of-line
   (EOL) indicators in text files:

.. code-block:: text

       Environment                  Native End-Of-Line
                                    Indicator
       ___________                  _____________________
       PC DOS/Windows               <CR><LF>
       Mac OS X, Linux, Unix        <LF>

As of CSPICE N0059, the CSPICE text kernel loaders,
:py:meth:`~spiceypy.spiceypy.furnsh` and
:py:meth:`~spiceypy.spiceypy.ldpool`, can read and parse non-native
text files. The FORTRAN SPICELIB does not include this capability.
Please be aware the CSPICE text file reader,
:py:meth:`~spiceypy.spiceypy.rdtext`, does not possess the
capability to read non-native text files.

DAF Run-Time Binary File Format Translation
-------------------------------------------

 | As of the CSPICE N0052 release (January, 2002), supported platforms
   are able to read DAF-based binary files (SPK, CK and binary PCK)
   written in a non-native, binary representation. This access is
   read-only; any operations requiring writing to the file (adding
   information to the comment area, or appending additional ephemeris
   data, for example) require prior conversion of the file to the
   native binary file format. See the Convert User's Guide,
   `convert.ug <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/ug/convert.html>`__, for details.

NAIF Text Kernel Format
-----------------------

 | Text PCK files express data as `assignments`; in text PCKs,
   values are associated with name strings using a `keyword =
   value` format. These name strings, together with their associated
   values, are called `kernel variables.` The CSPICE routines that
   access text PCK data at run time use these associations established
   by loaded text PCK files to reference desired data values; these
   routines look up data `by name.` Therefore, programmers writing
   applications that use text PCKs must coordinate use of kernel
   variable names between their software and the text PCK files used
   by their software.

 Text PCK files conform to a flexible format called `NAIF text
 kernel` format. The SPICE file identification word provided by
 itself on the first line of the text PCK file, starting in the
 leftmost column, is `KPL/PCK`. Both the NAIF text kernel format
 and SPICE file identification word are described in detail in the
 Kernel Required Reading document,
 `kernel.req <./kernel.html>`__. For the reader's convenience, an
 overview of the NAIF text kernel format is provided here.

 NAIF text kernels are, first of all, ASCII files. As such, they are
 human readable and can be easily modified by text editors. In
 addition, NAIF text kernels can be readily ported between computer
 systems, even when the systems in question have different file
 systems and file formats.

 The NAIF text kernel format provides for representation of data in a
 `keyword = value` syntax. The format also provides for the
 inclusion of free-form comment blocks.

 There are two kinds of data that can be placed in NAIF text kernel
 files: double precision numbers and UTC time strings.

 According to the text kernel format, a text kernel nominally consists
 of a series of sets of contiguous lines (or `blocks`) of comments,
 alternating with blocks of data. Comment blocks are started with the
 string (called a `control sequence`)

 .. code-block:: text

       \begintext

 alone on a line, as shown here. Comment blocks are ended by the
 control sequence

 .. code-block:: text

       \begindata

 alone on a line. In a text kernel file, the lines preceding the first

 .. code-block:: text

       \begindata

 control sequence are considered to constitute a comment block; the

 .. code-block:: text

       \begintext

 control sequence is optional for this comment block.
 Comment blocks can contain arbitrary text, except for non-printing
 characters or lines that can be interpreted as control sequences. On
 the other hand, data must be organized according to a very specific
 format: all of the data in a text kernel must appear in the form of
 an `assignment` such as

 .. code-block:: text

       NAME = VALUE

 or

 .. code-block:: text

       NAME = ( VALUE1, VALUE2, ... )

 where "NAME" is a string no longer than 32 characters, and one or
 more values appear on the right hand. A specific example is shown
 below:

 .. code-block:: text

       BODY399_RADII     = (  6378.140  6378.140  6356.75  )

 The "VALUES" may be integer, double precision or string values.
 Some variations on the form shown here are allowed: commas between
 data values are optional, the right hand side of the assignment can
 be continued over multiple lines, and the data values can be
 expressed as integers or reals without causing the PCK software to
 fail. Either an "E" or "D" can be used to set off an exponent.
 Assignments of scalars do not require the value on the right hand
 side to be enclosed in parentheses, but that notation is frequently
 used as a visual cue. Blank lines within or between assignments are
 ignored by the CSPICE software that reads text kernels.

 In addition to numbers, UTC strings can be assigned to variables. The
 `@` character is used to identify the strings as time strings. The
 strings are stored internally as double precision numbers
 representing `UTC seconds past J2000.` An example is the
 assignment:

 .. code-block:: text

       SCLK_KERNEL_ID            = ( @01-MAY-1991/16:25 )

 See `kernel.req <./kernel.html>`__ for a complete discussion of
 the allowed form of assignments.
 The effect of an assignment in a text PCK file is to associate values
 with a name. The name is referred to as a `kernel variable.` When
 a text PCK file is loaded by an application, the associations of
 names and values established by the PCK are maintained: the values
 associated with a given name can be retrieved at any time.

Text PCK Contents
-----------------

 | Other than the limitations imposed by the PCK file formats, no
   absolute restrictions exist on the names or values of the variables
   used in PCK files. However, the SPICE kernel concept calls for the
   contents of PCK files to be limited to physical and cartographic
   constants describing extended solar system bodies: radii of bodies,
   constants defining orientation models, and masses or values of GM
   are examples of data appropriate for inclusion in PCKs.

 CSPICE includes a set of routines
 (:py:meth:`~spiceypy.spiceypy.gipool`,
 :py:meth:`~spiceypy.spiceypy.gdpool`, gipool_c) for general access
 to text PCK defined data. Another set
 (:py:meth:`~spiceypy.spiceypy.bodvrd`,
 :py:meth:`~spiceypy.spiceypy.bodvcd`, sxform_c,
 :py:meth:`~spiceypy.spiceypy.pxform`) recognizes and uses
 particular PCK data to return body constants or the matrices to
 transform position or state vectors between reference frames.

 In this document, the formulas defining time-varying coordinate
 transformation matrices and Euler angles are referred to as
 `orientation models` since they define the orientation of an
 extended body with respect to specific inertial frames.

 Because PCK access routines that deal with orientation models are
 used extensively in CSPICE and applications that use the Toolkit, the
 kernel variables that these routines rely on will be discussed in
 detail.

 Those functions defining the Euler angles are characterized by a set
 of parameters. The specific values of the parameters are values
 assigned to kernel variables in PCK files. The functions themselves
 are implemented by code within CSPICE routines. The general form of
 the functions is that used in the IAU/IAG 2000 report. Values shown
 in this document reflect the 2000 report. For the latest PCK values,
 check with NAIF.

 In a text PCK file, the variables (Euler angles)

 .. code-block:: text

       RA,  DEC,  W

 for the Earth (Earth ID = 399) are represented by the names

 .. code-block:: text

       BODY399_POLE_RA
       BODY399_POLE_DEC
       BODY399_POLE_PM

 The equations above are expressed in a text PCK file by the kernel
 variable assignments (Values taken from IAU/IAG 2000 report.)

 .. code-block:: text

       BODY399_POLE_RA        = (    0.      -0.641         0. )
       BODY399_POLE_DEC       = (  +90.      -0.557         0. )
       BODY399_PM             = (  190.16  +360.9856235     0. )



Reference Ellipsoid Orientation Offsets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 | If you examine a PCK file produced by NAIF, you'll see an
   additional symbol grouped with the ones listed above; it is

 .. code-block:: text

       BODY399_LONG_AXIS

 The CSPICE function bodeul_c returns the value of the kernel variable

 .. code-block:: text

       BODY<id code>_LONG_AXIS

 as an output argument, but CSPICE does not make use of this value.
 This value represents the offset between the longest axis of the
 triaxial ellipsoid used to model the shape of a body and the prime
 meridian of the body. Historically, IAU orientation models have had
 only zero offsets.

 CSPICE high-level geometry software that makes use of reference
 ellipsoids assumes that ellipsoid axes are aligned with those of the
 corresponding PCK reference frame. When this is not the case, a new
 TK reference frame can be defined that provides the correct reference
 ellipsoid orientation relative to the PCK frame. See the Frames
 Required Reading document `frames <./frames.html>`__ for
 more information on TK frames.

 Defining a TK frame for reference ellipsoid orientation relative to
 the corresponding PCK frame is an effective way of representing such
 offsets. It enables user applications to pass the TK frame name to
 CSPICE APIs, so that those APIs will perform computations using the
 desired ellipsoid orientation.

Text PCK Kernel Variable Names
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 | Text PCK variables recognized by CSPICE PCK access routines have
   names that follow a simple pattern: variables related to a body
   whose NAIF integer code is nnn have names of the form

 .. code-block:: text

       BODYnnn_<item name>

 where

 .. code-block:: text

       <item name>

 is a short string that identifies the type of quantity the kernel
 variable represents. For example, the variable containing quadratic
 polynomial coefficients for the right ascension of the Earth's north
 pole is

 .. code-block:: text

       BODY399_POLE_RA

 The following sections specify the specific item names recognized by
 PCK access routines.


Restrictions on the Availability of Orientation Models in Text PCK Kernels
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 | Orientation models usable by CSPICE's text PCK access routines are
   not available for all solar system bodies. For example, Saturn's
   moon Hyperion is `tumbling` and does not admit a description of
   its motion by the sort of models used in text PCKs.

Models for the Sun, Planets, and some Minor Bodies in Text PCK Kernels
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 | For the Sun, planets, and minor bodies, the expressions used in
   text PCK files for the north pole direction and prime meridian
   location are always quadratic polynomials, where the independent
   variable is time. Some coefficients may be zero.

 Let RA and DEC represent the right ascension and declination of a
 body's north pole as expressed in the J2000 frame, and let W be the
 prime meridian location, measured in the counterclockwise direction,
 from the direction defined by the cross product of the Z direction in
 the J2000 frame (the Earth's `mean` North pole at the J2000 epoch)
 and BODY's North pole at ET, to BODY's prime meridian at ET.

 The variables RA, DEC, and W constitute sufficient information to
 compute the transformation from a specified inertial frame to
 body-fixed, planetocentric coordinates for the body to which they
 apply, at a specified time.

 The angles RA, DEC, and W are defined as follows:

 .. code-block:: text

                                       2
                                  RA2*t

      RA  =  RA0  +  RA1*t/T  +  ------  + [optional trig polynomials]
                                     2
                                    T

                                        2
                                  DEC2*t

      DEC =  DEC0 + DEC1*t/T  +  ------- + [optional trig polynomials]
                                     2
                                    T

                                      2
                                  W2*t

      W   =  W0   + W1*t/d    +  -----   + [optional trig polynomials]
                                     2
                                    d

 where

 .. code-block:: text

       d = seconds/day
       T = seconds/Julian century
       t = ephemeris time, expressed as seconds past the reference epoch
           for this body or planetary system

 Expressions for RA, Dec, and W for planets rarely include the
 trigonometric polynomial terms shown above. If they are used, these
 terms follow the form described below which is used for natural
 satellites.


Models for Satellites in Text PCK Kernels
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 | Orientation models for natural satellites of planets are a little
   more complicated; in addition to polynomial terms, the RA, DEC, and
   W expressions include trigonometric terms. The arguments of the
   trigonometric terms are linear polynomials. These arguments are
   sometimes called `phase angles.` However, within CSPICE internal
   documentation, these quantities often are called `nutation
   precession angles.` That terminology is used here.

 Expressions for the right ascension and declination of the north pole
 and the location of the prime meridian for any satellite of a given
 planet are as follows:

  .. code-block:: text

                                    2      ____
                               RA2*t       \
       RA  = RA0  + RA1*t/T  + ------   +  /     a  * sin * theta
                                  2        ----   i              i
                                 T           i

                                     2     ____
                               DEC2*t      \
       DEC = DEC0 + DEC1*t/T + -------  +  /    d  * cos * theta
                                   2       ----  i              i
                                  T          i

                                   2       ____
                               W2*t        \
       W   = W0   + W1*t/d   + -----    +  /     w  * sin * theta
                                  2        ----   i              i
                                 d           i

 where

 .. code-block:: text

       d = seconds/day
       T = seconds/Julian century
       t = ephemeris time, expressed as seconds past a reference epoch

 RA0, RA1, DEC0, DEC1, W0, and W1 are constants specific to each
 satellite.
 The nutation precession angles

 .. code-block:: text

       theta
            i

 are specific to each planet. The coefficients

 .. code-block:: text

       a ,  d ,  and w
        i    i        i

 are specific to each satellite.
 CSPICE software for text PCKs expects the models for satellite
 orientation to follow the form of the model shown here: the
 polynomial terms in the RA, DEC, and W expressions are expected to be
 quadratic, the trigonometric terms for RA and W (satellite prime
 meridian) are expected to be sums of sines of nutation precession
 angles, and the trigonometric terms for DEC are expected to be sums
 of cosines of nutation precession angles.

 The nutation precession angles themselves, by default, are defined by
 linear polynomial functions of time. It is possible to use
 polynomials of degree up to 3 to represent nutation precession angles
 for a specified planetary system. This is done by adding to a text
 PCK file the kernel variable assignment

 .. code-block:: text

       BODY<id code>_MAX_PHASE_DEGREE = <degree>

 where `id` is the code of the planetary system barycenter. For
 example, quadratic nutation precession angle expressions can be used
 for the Mars system if a text PCK contains the assignment

 .. code-block:: text

       BODY4_MAX_PHASE_DEGREE = 2

 For any planetary system, all nutation precession angles must have
 the same number of coefficients.
 Units of the polynomial coefficients of the nutation precession
 angles are, in order of increasing degree,

 .. code-block:: text

                     degrees            degrees
       degrees,   --------------,   ---------------,  ...
                  Julian century                  2
                                    Julian century

 Note that the number of values defining the nutation precession
 angles for a planetary system must be consistent with the number of
 trigonometric terms used in the expressions for the RA, DEC and W
 angles for the satellites of that system. See `Creating and
 Modifying Text PCKs Kernels` for details.


Shape models in Text PCK Kernels
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 | CSPICE contains a number of geometry routines that make use of
   triaxial ellipsoidal models of extended solar system bodies.
   Although CSPICE currently contains no routines that directly use
   the specific PCK variables that define these models, text PCK files
   typically contain radii of solar system bodies, since these values
   can be looked up by low-level text PCK access routines and
   subsequently used by CSPICE geometry routines.

 In text PCK files produced by NAIF, the radius values for body nnn
 are assigned to the variable as:

 .. code-block:: text

       BODYnnn_RADII = ( a, b, c )

 where `a,` `b,` and `c` are the radius values for each axis.
 Three radius values are always assigned for each instance of this
 variable. The data are ordered as in the IAU/IAG report: the
 equatorial radii are listed with the largest axis, normally called
 the `a` axis, appearing first; the polar radius, normally called
 the `c` axis, is last.

 Spheroids and spheres are obtained when two or all three radii are
 equal.

Summary of PCK Variables used in Text PCK Kernels by CSPICE
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 | In order to compute transformations for the Sun, a planet, or an
   asteroid (say body number ppp), the PCK access routines require
   that one or more PCK files containing values for the following
   variables be loaded:

 .. code-block:: text

       BODYppp_POLE_RA
       BODYppp_POLE_DEC
       BODYppp_PM

 For a satellite (say body number sss), one or more PCK files
 containing values for the following variables must be loaded:

 .. code-block:: text

       BODYsss_POLE_RA
       BODYsss_POLE_DEC
       BODYsss_PM
       BODYsss_NUT_PREC_RA
       BODYsss_NUT_PREC_DEC
       BODYsss_NUT_PREC_PM
       BODYbbb_NUT_PREC_ANGLES

 where the code bbb embedded in the last name above is that of the
 barycenter of the planetary system to which the satellite belongs.
 The triaxial ellipsoidal model for body nnn is expressed by the
 assignment

 .. code-block:: text

       BODYnnn_RADII = ( <larger equatorial radius>,
                         <smaller  equatorial radius>,
                         <polar radius> )



Creating and Modifying Text PCKs
---------------------------------

 | The text PCK file format allows NAIF Toolkit users to easily modify
   existing text PCKs and to create their own files containing values
   of their choosing. Any text editor capable of working with ASCII
   files can be used to edit text PCK files.

 Although the text PCK format makes it easy to modify text PCK files,
 NAIF recommends that application programmers avoid software designs
 that call for special-purpose, user-created text PCK files. The
 opportunities for confusion and errors increase with the number of
 available versions of a text PCK file (or any data file).

 NAIF recommends that you take the following precautions when
 modifying a text PCK file:

 - Change the name of the updated file.

 - Document the changes by adding appropriate comments to the
   file. Each text PCK file should contain sufficient information to
   allow a reader to find out who was responsible for creating the
   current version of the file and what the source was for each data
   value in the file. If the file is an update, the reason for the
   update and a summary of the differences from the previous version
   should be included.

 - Test the file using software that makes use of any values
   that you've added or modified.

 The reasons why a NAIF Toolkit user might wish to modify an existing
 text PCK are:

 - Removing unneeded data or comments to speed up loading and
   simplify the file. Removal of data is much more important than
   removal of comments, as far as speeding up kernel loading is
   concerned.

 - Adding data values for new bodies.

 - Updating existing data values or substituting preferred data
   values.

 New kernel variables added to text PCK files should follow the naming
 conventions described in the `Kernel Variable Names` section. All
 text PCK variable names, whether or not they are recognized by CSPICE
 software, should start with the prefix

 .. code-block:: text

       BODYnnn_

 where nnn is the NAIF integer code of the body corresponding to the
 variable.
 Kernel variables having names recognized by users' application
 software are a potential problem area: if the names used in the
 application don't match those in the text PCK file, the application
 will fail to obtain the data as intended. The most frequent cause of
 this type of failure is misspelling of variable names, but
 programmers who considering changing the names of PCK variables
 already in use should also keep this problem in mind.

 Modifying orientation models for satellites requires attention to
 consistency between the number of nutation precession angles and the
 number of coefficients of trigonometric functions having the nutation
 precession angles as arguments. For any planetary system, if DEG is
 the maximum nutation precession angle polynomial degree for that
 system, there should be DEG+1 times as many values for the nutation
 precession angles as the maximum number of trigonometric terms in the
 expressions for prime meridian location or right ascension or
 declination of the pole of any satellite in the system. This is
 because all nutation precession angle polynomials for a given
 planetary system must have the same degree.

Binary PCK Kernel Format
------------------------

 | The binary PCK file format is built upon the SPICE DAF (Double
   precision Array File) architecture. Readers who are not familiar
   with this architecture are referred to the DAF Required Reading
   document, `daf.req <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/daf.html>`__, which describes the common
   aspects of all DAF formats, as well as a collection of CSPICE
   subroutines that support the DAF architecture. The SPICE file
   identification word occupying the first eight bytes of a properly
   created binary PCK file is `DAF/PCK`. For more information on
   SPICE identification words refer to the Kernel Required Reading
   document, `kernel.req <./kernel.html>`__. Most users will not
   need to understand the details of the structure of binary PCK
   files.

Segments--The Fundamental PCK Building Blocks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 | A binary PCK file contains one or more `segments`. Each segment
   contains data sufficient to compute the axes of a body-fixed
   planetary coordinate system, relative to a specified inertial
   reference frame, as a function of time.

 The data in each segment are stored as a single array. The summary
 for the array, called a `descriptor`, has two double precision
 components:

#. The initial epoch of the interval for which data are
   contained in the segment, in ephemeris seconds past Julian year
   2000;

#. The final epoch of the interval for which data are contained
   in the segment, in ephemeris seconds past Julian year 2000.

 The descriptor has five integer components:

#. The frame class ID of the PCK reference frame for which the
   segment provides orientation data. See the Frames Required Reading
   document `frames <./frames.html>`__ for further
   information on frame class IDs.

 - Some older SPICE documentation refers to this ID code as as a
   `body` ID code.

#. The NAIF integer code for the inertial reference frame.

#. The integer code for the representation (type of PCK data).
   Currently types 2, 3, and 20 are supported.

#. The initial address of the array.

#. The final address of the array.

 The name of each array may contain up to 40 characters. This space
 may be used to store a `pedigree` for the data in the array. The
 pedigree of a segment should allow a user to determine the conditions
 under which the data in the segment were generated.


The Comment Area
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 | Preceding the `segments`, the Comment Area provides space in a
   binary PCK file for storing additional textual information besides
   what is written in the array names. Ideally, each binary PCK file
   would contain internal documentation that describes the origin,
   recommended use, and any other pertinent information about the data
   in that file. For example, the beginning and ending epochs for the
   file, the names and NAIF integer codes of the bodies included, an
   accuracy estimate, the date the file was produced, and the names of
   the source files used in making the binary PCK file could be
   included in the Comment Area.

 CSPICE provides a family of subroutines for handling this Comment
 Area. This software provides the ability to add, extract, read, and
 delete comments and convert commented files from binary format to
 transfer format and back to binary again.

Binary PCK Data Types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 | The third integer component of the descriptor---the code for the
   representation, or `data type`---is the key to the binary PCK
   format. For purposes of determining the segment best suited to
   fulfill a particular request, all segments are treated equally. It
   is only when the data in a segment are to be evaluated that the
   type of data used to represent the data becomes important. Because
   this step is isolated within low-level readers, new data types can
   be added to the binary PCK format without affecting application
   programs that use the higher level readers.

Supported Data Types
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 | Three representations, or data types, are currently supported by
   the binary PCK routines in CSPICE. They are:

#. Type 2, Chebyshev polynomials (Euler angles only).

#. Type 3, Chebyshev polynomials (Euler angles and their
   derivatives) for intervals of possibly varying lengths.

#. Type 20, Chebyshev polynomials (Derivatives of Euler
   angles).



Type 2: Chebyshev (Angles only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 | These are sets of Chebyshev polynomial coefficients for the Euler
   angles, defining as a function of time the right ascension (RA) and
   declination (DEC) of a body's north pole, and the prime meridian
   rotation (W). The rates of the angles are obtained by
   differentiation.

 The segments contain an arbitrary number of logical records with each
 record describing a set of Chebyshev coefficients valid across an
 interval of fixed length.

 A segment consists of a set of records, ordered by increasing initial
 epoch, each record containing the same number of coefficients. The
 segment structure is illustrated below:

 .. code-block:: text

               +---------------+
               | Record 1      |
               +---------------+
               | Record 2      |
               +---------------+
                 .
                 .
                 .
               +---------------+
               | Record N      |
               +---------------+
               | INIT          |
               +---------------+
               | INTLEN        |
               +---------------+
               | RSIZE         |
               +---------------+
               | N             |
               +---------------+

 A four-number \`directory' at the end of the segment contains the
 information needed to determine the location of the record
 corresponding to a particular epoch.

#. INIT is the initial epoch of the first record, given in
   ephemeris seconds past 2000 Jan 01 12:00:00, also known as J2000.

#. INTLEN is the length of the interval covered by each record,
   in seconds.

#. RSIZE is the total size of (number of array elements in)
   each record.

#. N is the number of records contained in the segment.

 Each component has the same number of coefficients, and all records
 are the same size (RSIZE), so the degree of each polynomial is  \

 .. code-block:: text

        polynomial degree = ( RSIZE - 2 ) / 3 - 1

 The structure of each record:

 .. code-block:: text

       ---------------------------------------------------------------
       |  The midpoint of the approximation interval in TDB seconds  |
       ---------------------------------------------------------------
       |  The radius of the approximation interval in TDB seconds    |
       ---------------------------------------------------------------
       |  (polynomial degree + 1) coefficients for RA                |
       ---------------------------------------------------------------
       |  (polynomial degree + 1) coefficients for DEC               |
       ---------------------------------------------------------------
       |  (polynomial degree + 1) coefficients for W                 |
       ---------------------------------------------------------------

 TDB seconds is time in ephemeris seconds past J2000, often called ET
 in the SPICE system.
 The first two elements in the record, MID and RADIUS, are the
 midpoint and radius of the time interval covered by coefficients in
 the record. These are used as parameters to perform transformations
 between the domain of the record (from MID - RADIUS to MID + RADIUS)
 and the domain of Chebyshev polynomials (from -1 to 1 ).

Type 3: Chebyshev (Angles and their derivatives)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 | A type 03 PCK segment consists of coefficient sets for fixed order
   Chebyshev polynomials over consecutive time intervals, where the
   time intervals need not all be of the same length. The Chebyshev
   polynomials represent the orientation of a body specified relative
   to an inertial frame by the angles RA, DEC, W and body fixed
   angular rates for each axis of the body fixed coordinate system
   defined by RA, DEC, and W. The angles and the angular rates of the
   axes are given in degrees and degrees/sec.

 Each segment contains an arbitrary number of logical records. All
 records contain the same number of coefficients.

 A segment of this type is structured as follows:

 .. code-block:: text

               +---------------+
               | Record 1      |
               +---------------+
               | Record 2      |
               +---------------+
                 .
                 .
                 .
               +---------------+
               | Record N - 1  |
               +---------------+
               | Record N      |
               +---------------+

 The structure of each record:

 .. code-block:: text

       ---------------------------------------------------------------
       |  The midpoint of the approximation interval in TDB seconds  |
       ---------------------------------------------------------------
       |  The radius of the approximation interval in TDB seconds    |
       ---------------------------------------------------------------
       |  (polynomial degree + 1) coefficients for RA                |
       ---------------------------------------------------------------
       |  (polynomial degree + 1) coefficients for DEC               |
       ---------------------------------------------------------------
       |  (polynomial degree + 1) coefficients for W                 |
       ---------------------------------------------------------------
       |  (polynomial degree + 1) coefficients for the body          |
       |  fixed X-axis rate                                          |
       ---------------------------------------------------------------
       |  (polynomial degree + 1) coefficients for the body          |
       |  fixed Y-axis rate                                          |
       ---------------------------------------------------------------
       |  (polynomial degree + 1) coefficients for the body          |
       |  fixed Z-axis rate                                          |
       ---------------------------------------------------------------

 TDB seconds is time in ephemeris seconds past J2000, called ET in the
 SPICE system.
 The type 3 data type is seldom used.

Type 20: Chebyshev (Only angular derivatives)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 | PCK data type 20 contains Chebyshev polynomial coefficients for a
   specified set of Euler angle rates of a body-fixed, body-centered
   reference frame as a function of time. Euler angles representing
   the orientation of the frame are obtained by integrating the rates
   using a specified integration constant.

 This data type is provided to accurately represent `EPM`
 orientation data developed by the Institute of Applied Astronomy
 (IAA), Russian Academy of Sciences (RAS).

 Each type 20 segment contains an arbitrary number of logical records.
 Each record contains a set of Chebyshev coefficients valid throughout
 an interval of fixed length. Each record also contains an Euler angle
 set applicable at the midpoint of its coverage interval.

 The records within a segment are ordered by increasing initial epoch.
 All records contain the same number of coefficients.

 A segment of this type is structured as follows:

 .. code-block:: text

               +---------------+
               | Record 1      |
               +---------------+
               | Record 2      |
               +---------------+
                 .
                 .
                 .
               +---------------+
               | Record N      |
               +---------------+
               | ASCALE        |
               +---------------+
               | TSCALE        |
               +---------------+
               | INITJD        |
               +---------------+
               | INITFR        |
               +---------------+
               | INTLEN        |
               +---------------+
               | RSIZE         |
               +---------------+
               | N             |
               +---------------+

 A seven-number \`directory' at the end of the segment contains the
 information needed to determine the location of the record and
 perform an evaluation of the record corresponding to a particular
 epoch.

#. ASCALE is the angular scale used for both orientation and
   angular rates; ASCALE has units of radians. For example, if the
   angular units are degrees, then ASCALE is the number of radians in
   one degree.

#. TSCALE is the time scale used for angular rates; TSCALE has
   units of TDB seconds. For example, if the time units of the rate
   data are TDB Julian days, then TSCALE is 86400.

#. INITJD is the integer part of the TDB Julian date of the
   initial epoch of the first record. INITJD has units of Julian days.
   INITJD may be less than, equal to, or greater than the initial
   epoch.

#. INITFR is the fractional part of the TDB Julian date of the
   initial epoch of the first record. INITFR has units of Julian days.
   INITFR has magnitude strictly less than 1 day. The sum INITJD +
   INITFR equals the TDB Julian date of the initial epoch of the first
   record.

#. INTLEN is the length of the interval covered by each record,
   in TDB Julian days.

#. RSIZE is the total size of (number of array elements in)
   each record. The same number of coefficients is always used for
   each component, and all records are the same size. RSIZE is 3 +
   3*(DEGP+1), where DEGP is the common degree of the Chebyshev
   expansions for each Euler angle rate component.

#. N is the number of records contained in the segment.

 Each component has the same number of coefficients, and all records
 are the same size (RSIZE), so the degree of each polynomial is (solve
 RSIZE for DEGP)

 .. code-block:: text

       polynomial degree = ( RSIZE/3 - 2 )

 Define the angles as:

 .. code-block:: text

       angle  * ASCALE = ( RA   + pi/2 )
            1

       angle  * ASCALE = ( pi/2 - DEC )
            2

       angle  * ASCALE = ( W )
            3

 The structure of each record:

 .. code-block:: text

       ---------------------------------------------------------------
       |  (polynomial degree + 1) coefficients for the rate of       |
       |  angle 1                                                    |
       ---------------------------------------------------------------
       |  value of angle 1 at interval midpoint                      |
       ---------------------------------------------------------------
       |  (polynomial degree + 1) coefficients for the rate of       |
       |  angle 2                                                    |
       ---------------------------------------------------------------
       |  value of angle 2 at interval midpoint                      |
       ---------------------------------------------------------------
       |  (polynomial degree + 1) coefficients for the rate of       |
       |  angle 3                                                    |
       ---------------------------------------------------------------
       |  value of angle 3 at interval midpoint                      |
       ---------------------------------------------------------------

 The rate coefficients have units of ASCALE radians/TSCALE seconds:
 multiplying a Chebyshev expansion's value by ASCALE/TSCALE converts
 angular rates to units of radians/s.
 Euler angles at a record's midpoint epoch are given in units of
 ASCALE radians: multiplying the angles by ASCALE converts the angles
 to units of radians.

 The Euler angles represent the orientation of the PCK reference frame
 relative to its base frame. The angles, which are numbered according
 to their ordinal position in the logical records, define a
 transformation matrix R as follows:

 .. code-block:: text

       R = [ angle  *A ]  [ angle  *A ]  [ angle  *A ]
                  3     3        2     1        1     3

 where A is the angular scale ASCALE. Here the notation

 .. code-block:: text

          [ THETA ]
                   i

 denotes a reference frame rotation of THETA radians in the right-hand
 sense about the ith coordinate axis. See the Rotation Required
 Reading for further discussion of this notation.


Creating Binary PCKs
--------------------

 | NAIF creates most binary PCKs. Normally, binary PCK files should be
   obtained from NAIF.

 Only very knowledgeable users who need to incorporate new
 planetary/satellite orientation information in binary format should
 consider writing binary PCK files. Users who write binary PCK files
 must have a thorough understanding of the information they wish to
 place in a binary PCK file. They must also master the high level
 structure of the PCK files, and they must be sure to correctly
 package the data for the PCK writing subroutines provided in CSPICE.
 We also strongly recommend that the writer of a PCK file include
 descriptive comments in the comment area.

 The user should keep in mind that the PCK segments should be as large
 as possible to create smaller, faster to load files.

 The are generally three steps to creating a binary PCK file.

 #. Open the file.

 #. Begin the segment, add data to the segment and close the segment.

 #. Close the file.

 The subroutine :py:meth:`~spiceypy.spiceypy.pckopn` is used to open
 a new binary PCK file. Below is an example of a call to
 :py:meth:`~spiceypy.spiceypy.pckopn`. `name` is the name of the
 file to be opened, `ifname` is the internal file name, `handle`
 is the handle of the opened SPK file. We use `i` for the number of
 records to reserve for comments.

 .. code-block:: python

      handle = pckopn(file, ifname, i)

 The method for beginning the segment, adding data to the segment and
 closing the segment differs with the PCK type.
 For type 2, CSPICE includes a segment writing routine called
 :py:meth:`~spiceypy.spiceypy.pckw02`. This routine takes as input
 arguments the handle of an PCK file that is open for writing, the
 information needed to construct the segment descriptor, and the data
 to be stored in the segment. The header of the subroutine provides a
 complete description of the input arguments and an example of its
 usage.

 An example of a call to :py:meth:`~spiceypy.spiceypy.pckw02`:

 .. code-block:: python

      pckw02(handle, clssid, frame, first, last, segid, intlen, n, polydg, cdata, btime)

 For type 3, there are three subroutines used in creating a binary PCK
 file. They are pck03b\_, which begins a type 3 segment, PCK03A, which
 adds data to segment, and pck03e\_, which ends a segment. The type 3
 subroutines can be used in a loop, where pck03a\_ is called to add
 data to the segment. Here is a code fragment that begins a type 3
 segment, writes data to that segment in a loop, and then closes the
 segment.

 .. code-block:: python

          pck03b_(handle, segid, body, frame, first, last, chbdeg, len(segid), len(frame))

          while something_true:
              ...
              pck03a_(handle, n, coeffs, epochs)
              ...


          pck03e_(handle)

 For type 20, CSPICE includes a segment writing routine called
 pckw20\_. takes as input arguments the handle of a PCK file that is
 open for writing, the information needed to construct the segment
 descriptor, and the data to be stored in the segment. The header of
 the function provides a complete description of the input arguments
 and an example of its usage.
 An example of a call to pckw20\_:

 .. code-block:: python

          pckw20_(
              handle,
              clssid,
              frame,
              first,
              last,
              segid,
              intlen,
              n,
              polydg,
              cdata,
              ascale,
              tscale,
              initjd,
              initfr,
              len(frame),
              len(segid),
          )

 When a user finishes writing segments of any type to a binary PCK,
 the PCK must be closed with the subroutine
 :py:meth:`~spiceypy.spiceypy.pckcls`.

 .. code-block:: python

       pckcls_c(handle)



PCK Software
============

 | This section describes the proper use of the CSPICE PCK software.

Getting PCK Data into Your Program
-----------------------------------

 | Because loading PCK files is usually time-consuming, it is good
   programming practice to have applications load PCK files during
   program initialization rather than throughout their main processing
   thread, especially if that processing thread is a loop.

 It is also wise to avoid designing data processing systems that
 effectively place PCK loading in a tight loop by requiring repeated
 runs of programs that expend a significant fraction of their run time
 on loading PCK files. If a program loads PCK files, it is preferable
 that it do all of its processing in a single run, or at least in a
 small number of runs, rather than carry out its processing by being
 re-run a large number of times: the former design will greatly reduce
 the ratio of the time the program spends loading PCKs to the time it
 spends on the rest of its data processing.

Loading Text PCK Kernels
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 | As earlier mentioned, in order to use text PCK files in an
   application, the data in the files must be read into memory. This
   is accomplished by calling the CSPICE routine
   :py:meth:`~spiceypy.spiceypy.furnsh`. The name of the text PCK
   file to load is supplied as an input to
   :py:meth:`~spiceypy.spiceypy.furnsh`, for example:

 ::

       furnsh("example_pck.tcp")

 File names supplied to :py:meth:`~spiceypy.spiceypy.furnsh` will
 generally be system-dependent. It is good programming practice to not
 use hard-coded file names in calls to
 :py:meth:`~spiceypy.spiceypy.furnsh`. Instead, applications should
 obtain kernel file names by one of the following methods:

 - Reading the kernel file names from a meta-kernel, a file
   containing the names. (This allows users to change the kernel files
   without re-compiling and re-linking the application.)

 - Prompting the user for the file names at run-time.

 An application can load any number of text PCK files during a single
 program run. There are, however, parameterized limits on both the
 total number of kernel variables that can be stored and on the total
 number of data values assigned to those variables.
 Each time a text PCK is loaded, the assignments made in the file are
 maintained in the PCK software. In particular, if a kernel variable
 occurs in multiple PCKs loaded in a single run of a program, the
 value of the variable will be the one assigned in the following
 priority: last binary PCK file loaded, previously loaded binary PCK
 files, then last loaded text PCK files followed by previously loaded
 text PCK files. All binary PCK files take precedence over text PCK
 files. Within the binary and/or text file groups, the last loaded
 files takes precedence.

Loading Binary PCK Kernels
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 | The routine :py:meth:`~spiceypy.spiceypy.furnsh` maintains a
   database of loaded binary PCK files. The calling program indicates
   which files are to be used by passing their names to
   :py:meth:`~spiceypy.spiceypy.furnsh`.

 ::

       furnsh("example_binary_pck.tcp")

 Once an PCK file has been loaded, it may be accessed by the PCK
 software. Each set of constants is computed from a distinct segment.
 A PCK file may contain any number of segments. In fact, the same file
 may contain overlapping segments: segments containing data for the
 same body over a common interval. When this happens, the latest
 segment in a file supersedes any competing segments earlier in the
 file. Similarly, the latest file loaded supersedes any earlier files.
 In effect, several loaded files become equivalent to one large file.
 Binary PCK files take precedence over text PCK files.

Unloading Binary PCK Kernels
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 | It is possible, though unlikely, that a program would need to make
   use of many binary PCK files in the course of a single execution.
   On the other hand, the number of binary PCK files that may be open
   at any one time is limited, so such a program might need to unload
   some PCK files to make room for others. A binary PCK file may be
   unloaded by supplying its name to subroutine
   :py:meth:`~spiceypy.spiceypy.unload`. The call to this subroutine
   is shown below,

 ::

       unload("example_binary_pck.tcp")



Binary PCK Coverage Summary Routines
-------------------------------------

 | CSPICE includes two functions for obtaining information about the
   contents of a binary PCK file from within an application.

 The :py:meth:`~spiceypy.spiceypy.pckfrm` function provides an API
 via which an application can find the set of reference frames for
 which a specified binary PCK file contains data. The reference frame
 class ID codes are returned in a SPICE `set` data structure (see
 `sets.req <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/sets.html>`__).

 The :py:meth:`~spiceypy.spiceypy.pckcov` function provides an API
 via which an application can find the time periods for which a
 specified binary PCK file provides data for a reference frame of
 interest. The coverage information is a set of disjoint time
 intervals returned in a SPICE `window` data structure (see `other stuff tutorial <./other_stuff.html>`__ and
 `windows.req <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/windows.html>`__).

 Refer to the headers of :py:meth:`~spiceypy.spiceypy.pckfrm` and
 :py:meth:`~spiceypy.spiceypy.pckcov` for details on the use of
 those routines.

Access Routines
---------------

 | CSPICE contains two basic categories of PCK access routines: those
   that return PCK data directly, and those that return quantities
   derived from PCK data. This section discusses the PCK access
   routines in the later category: these routines deal with coordinate
   and state transformations.

 All of the routines listed here make use of the orientation models
 discussed in the section titled `Orientation Models used by PCK
 Software.` Note that in order to use these routines, an application
 must first load a PCK file (or files) containing sufficient data to
 define all of the required orientation models. If needed data has not
 been loaded, these routines will signal run-time errors when called.

High-Level PCK Data Access
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 | To obtain the matrix that transforms 3-vectors from a specified
   reference frame to another frame, at a specified ephemeris time,
   use the routine :py:meth:`~spiceypy.spiceypy.pxform`. The calling
   sequence is

 .. code-block:: python

       rotate = pxform(f_from, to_f, et)

 In the argument list for :py:meth:`~spiceypy.spiceypy.pxform`:

 **f_from**
    is the name of a reference frame in which a position vector is
    known.

 **to_f**
    is the name of a reference frame in which it is desired to
    represent a position vector.

 **et**
    is the epoch in ephemeris seconds past the epoch of J2000 (TDB) at
    which the position transformation matrix `rotate` should be
    evaluated.

 **rotate**
    is the matrix that transforms position vectors from the reference
    frame `f_from` to the frame `to_f` at epoch `et`.

 The fundamental quantities defined by PCK orientation models are
 actually Euler angles, not matrices. These Euler angles, which we
 call `RA, DEC, and W,` are related to the transformation operator
 returned from :py:meth:`~spiceypy.spiceypy.pxform` by the equation

 .. code-block:: text

       rotate = [ W ]   [ Pi/2 - DEC ]   [ Pi/2 + RA ]
                     3                1               3

 To directly retrieve these angles, use the call:

 .. code-block:: python

       ra, dec, w, lam = bodeul(body, et)

 **body**
    is the NAIF integer code of the body defining the planetocentric
    coordinate system.

 **et**
    is the ephemeris time at which the orientation model given the
    basis vectors of the planetocentric frame is to be evaluated.

 **ra**
    is the right ascension of the North pole of body at et with
    respect to the J2000 inertial reference frame.

 **dec**
    is the declination of the North pole of body at et with respect to
    the J2000 inertial reference frame.

 **w**
    is the prime meridian location for `body` at `et`, also
    measured with respect to the J2000 inertial reference frame.

 **lam**
    is the positive west longitude, measured from the prime meridian
    of body, of the longest axis of the triaxial ellipsoidal model for
    body given in a PCK file.

 Currently, the only body having a non-zero value of LAMBDA is Mars
 (see Duxbury 1979). SPICE software does not currently make use of
 `lam`.
 SPICE provides a routine analogous to
 :py:meth:`~spiceypy.spiceypy.pxform` that returns the matrix to
 transform state vectors between reference frames for a particular
 time. This routine is called :py:meth:`~spiceypy.spiceypy.sxform`;
 the calling sequence being

 .. code-block:: python

       rotate = sxform(f_from, to_f, et)

 The input arguments `f_from`, `to_f`, and `et` have the same
 meanings as in the argument list of
 :py:meth:`~spiceypy.spiceypy.pxform`. The output argument
 `rotate` is the 6x6 matrix required to transform state vectors
 from inertial to body-fixed coordinates. Left multiplication of a
 state vector by `rotate` will transform it from the frame
 specified by `f_from` to the frame specified by `to_f` at time
 `et`.


Low-Level PCK Data Access
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 .. warning::
   These low-level access routines for text PCK files only
   search the text kernel pool for these values. Values found in
   loaded binary PCK files will NOT be found by these routines. The
   values retrieved from a binary PCK file take precedence over the
   values found in text PCK kernels. Therefore, if binary kernels have
   been loaded, values returned by these low level routines may not be
   the same values used by higher level routines like
   :py:meth:`~spiceypy.spiceypy.sxform` and
   :py:meth:`~spiceypy.spiceypy.pxform`.
   We recommend the user who loads binary PCKs NOT USE these low-level routines!

 The lowest-level CSPICE PCK access routines are
 :py:meth:`~spiceypy.spiceypy.gipool`,
 :py:meth:`~spiceypy.spiceypy.gdpool` and
 :py:meth:`~spiceypy.spiceypy.gcpool`. These are general-purpose
 routines for retrieving any text kernel data by data type (integer,
 double precision, and character string, respectively) loaded via
 :py:meth:`~spiceypy.spiceypy.furnsh`. The calling sequences for the
 routines:

 .. code-block:: python

       vals = gcpool(name, start, room)
       vals = gdpool(name, start, room)
       vals = gipool(name, start, room)

 The meanings of the arguments are follows:

 **name**
    is the name of the kernel variable whose values are desired. This
    is the name used in a PCK file to make an assignment.

 **start**
    is the index of the first component of NAME to return. The index
    follows the C convention of being 0 based. If \`start' is less
    than 0, it will be treated as 0.

 **room**
    is the maximum number of components that should be returned for
    this variable.

 **lenout**
    is the allowed length of the output string. This length must be
    large enough to hold the output string plus the terminator.

 **vals**
    is the return arrays of sufficient size and correct type to
    contain the data corresponding to `name`.


 The :py:meth:`~spiceypy.spiceypy.gipool`,
 :py:meth:`~spiceypy.spiceypy.gdpool`, and
 :py:meth:`~spiceypy.spiceypy.gcpool` set is frequently used by
 other SPICE routines; however, SPICE users will usually find it
 more convenient to use the PCK access routines that return double
 precision body constants, e.g radius, RA/DEC of the spin axis, the GM
 value, etc.
 In text PCKs produced by NAIF, PCK variables will have names
 conforming to the naming convention used in CSPICE, that is, the
 kernel variable names have the form

 .. code-block:: text

       BODYnnn_<item name>

 :py:meth:`~spiceypy.spiceypy.bodvrd` and
 :py:meth:`~spiceypy.spiceypy.bodvcd` retrieve the values of such
 variables from the kernel pool;
 :py:meth:`~spiceypy.spiceypy.bodvrd` accepts as inputs the body
 name and a string making up the portion of the item's name following
 the prefix:

 .. code-block:: python

      dim, values = bodvrd(bodynm, item, maxn)

 :py:meth:`~spiceypy.spiceypy.bodvcd` functions in the same manner
 as :py:meth:`~spiceypy.spiceypy.bodvrd` except bodvcd_c accepts as
 inputs the body NAIF ID and the string, `item`, as described for
 :py:meth:`~spiceypy.spiceypy.bodvrd`:

 .. code-block:: python

      dim, values = bodvcd(bodyid, item, maxn)

 It is possible to test whether a kernel variable has been loaded by
 calling the SPICE logical function
 :py:meth:`~spiceypy.spiceypy.bodfnd`, as long as the variables in
 question follow the SPICE naming convention. The calling sequence is

 .. code-block:: python

       found = bodfnd(body, item)

 where body is the NAIF integer code of the body, and `item` is the
 string making up the portion of the item's name following the prefix

 .. code-block:: text

       BODYnnn_



Appendix A --- Summary of PCK Routines
=======================================


 .. code-block:: text

       bodeul ( Return Euler angles for a body )
       bodfnd ( Find values from the kernel pool )
       bodvcd ( Return d.p. values from the kernel pool )
       bodvrd ( Return d.p. values from the kernel pool )
       furnsh ( Furnish a program with SPICE kernels )
       gcpool ( Get character data from the kernel pool )
       gdpool ( Get d.p. values from the kernel pool )
       gipool ( Get integers from the kernel pool )
       pck03a_  ( PCK, add data to a type 3 segment )
       pck03b_  ( PCK, begin a type 3 segment )
       pck03e_  ( PCK, end a type 3 segment )
       pckcls ( PCK, close file )
       pckcov ( PCK, coverage )
       pcke02_  ( PCK, evaluate data record from type 2 segment )
       pcke03_  ( PCK, evaluate data record from type 3 segment )
       pcke20_  ( PCK, evaluate data record from type 20 segment )
       pckeul_  ( PCK, get Euler angles at time from PCK file )
       pckfrm ( PCK, get reference frame class ID set )
       pcklof ( PCK Kernel, Load binary file )
       pckopn ( PCK, open new file )
       pckr02_  ( PCK, read record from type 2 segment )
       pckr03_  ( PCK, read record from type 3 segment )
       pckr20_  ( PCK, read record from type 20 segment )
       pcksfs_  ( PCK, select file and segment )
       pckuof_  ( PCK Kernel, Unload binary file )
       pckw02 ( PCK, write type 2 segment )
       pckw20_  ( PCK, write type 20 segment )
       pxform ( Position Transformation Matrix )
       sxform ( State Transformation Matrix )
       unload ( Unload a kernel )



Appendix B --- Epoch and Frame Specifications in Text PCK Kernels
=================================================================

 | The constants used in PCK files to define an orientation model for
   a specified body are assumed by default to define a time-dependent
   rotation R(t) that converts vectors from J2000 coordinates to
   body-fixed, planetocentric coordinates at the epoch t seconds past
   J2000, TDB (JED 2451545.0). We say that the constants are
   `referenced to the J2000 epoch and J2000 frame.` However, these
   default values for the epoch and frame of the constants may be
   overridden: it is possible to use constants referenced to the B1950
   frame and to the J1950 epoch, for example.

 The default epoch and inertial base frame for a body are overridden
 by setting the values of either of the kernel variables

 .. code-block:: text

       BODY<id code>_CONSTANTS_REF_FRAME
       BODY<id code>_CONSTS_REF_FRAME

 and

 .. code-block:: text

       BODY<id code>_CONSTANTS_JED_EPOCH
       BODY<id code>_CONSTS_JED_EPOCH

 The shorter forms of the kernel variable names enable use of
 11-character ID codes, which can represent any 32-bit signed integer,
 while keeping the names within the 32-character limit imposed by
 CSPICE.
 Here

 .. code-block:: text

       <id code>

 is:

 - for planets and their satellites: the NAIF integer code of
   the corresponding planetary system's barycenter.

 - for other bodies: the NAIF integer code of the body itself.

 The values of the frame specifier variables

 .. code-block:: text

       BODY<id code>_CONSTANTS_REF_FRAME
       BODY<id code>_CONSTS_REF_FRAME

 are the frames IDs for the inertial reference frames coded into the
 Frames subsystem. Refer to the Frames Required Reading document,
 `frames.req <./frames.html>`__, for a list of the inertial
 reference frames and the corresponding frame IDs.
 For example, to use constants referenced to the FK4 frame (frame ID
 1) for the asteroid Gaspra (ID code = 9511010), the PCK file
 containing the constants should include one of the assignments

 .. code-block:: text

       BODY9511010_CONSTANTS_REF_FRAME   =   3
       BODY9511010_CONSTS_REF_FRAME      =   3

 The values of the epoch specifier variables

 .. code-block:: text

       BODY<id code>_CONSTANTS_JED_EPOCH
       BODY<id code>_CONSTS_JED_EPOCH

 are Julian ephemeris dates. To use constants for Gaspra referenced to
 the J1950 epoch, the PCK file containing the constants should include
 one of the assignments

 .. code-block:: text

       BODY9511010_CONSTANTS_JED_EPOCH   =   2433282.5
       BODY9511010_CONSTS_JED_EPOCH      =   2433282.5

 The creator of a PCK file can set the frame and epoch of the
 constants on a body-by-body basis, except in the case of planets and
 their (natural) satellites, where a single choice of frame and epoch
 must be used for each planetary system. For example, to use constants
 referenced to the B1950 frame (frame ID 2) and J1950 epoch for the
 Earth and Moon, use the assignments

 .. code-block:: text

       BODY3_CONSTANTS_REF_FRAME   =   2
       BODY3_CONSTANTS_JED_EPOCH   =   2433282.5

          or

       BODY3_CONSTS_REF_FRAME   =   2
       BODY3_CONSTS_JED_EPOCH   =   2433282.5

 The ID code \`3' designates the Earth-Moon barycenter.
 Note: the assignments

 .. code-block:: text

       BODY399_CONSTANTS_REF_FRAME   =   2
       BODY399_CONSTANTS_JED_EPOCH   =   2433282.5

          or

       BODY399_CONSTS_REF_FRAME   =   2
       BODY399_CONSTS_JED_EPOCH   =   2433282.5

 would be ignored by the PCK reader routines; you cannot assign a
 frame or epoch using the ID code of a planet or satellite.

