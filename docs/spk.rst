*********************
SPK Required Reading
*********************

This required reading document is reproduced from the original NAIF
document available at `https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/spk.html <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/spk.html>`_

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
=========

| The SPK system is the component of SPICE concerned with ephemeris
  data.

Purpose
--------

| The purpose of this document is to describe the SPICE Toolkit
  software provided in the software library CSPICE, (C SPICE library)
  used for producing and accessing SPICE ephemeris data. In addition
  this document describes SPK---the common file format for NAIF's
  S-kernel and ephemeris portion of the P-kernel.

Intended Audience
------------------

| This document is intended for all users of SPK (ephemeris) kernel
  files.

References
--------------

| All references are to NAIF documents. The notation [Dn] refers to
  NAIF document number.

#. [349] Frames Required Reading
   (`frames <./frames.html>`__)

#. [174] CK Required Reading (`ck <./ck.html>`__)

#. [254] PCK Required Reading (`pck <./pck.html>`__)

#. [222] Spacecraft Clock Time Required Reading
   (`sclk <./sclk.html>`__)

#. [218] KERNEL Required Reading
   (`kernel <./kernel.html>`__)

#. [219] NAIF IDS Required Reading
   (`naif_ids <./naif_ids.html>`__)

#. [163] JPL Internal Memorandum on Modified Difference Array
   polynomials; F. Krogh

#. [164] Precession Matrix Based on IAU (1976) System of
   Astronomical Constants; E. M. Standish; Astronomy and Astrophysics
   73, 282-284 (1979)

#. [165] Orientation of the JPL Ephemerides, DE200/LE200, to
   the Dynamical Equinox of J2000; E. M. Standish; Astronomy and
   Astrophysics 114, 297-302 (1982)

#. [166] The JPL Asteroid and Comet Database (as Implemented
   by NAIF); a collection of papers and memos; assembled by I.
   Underwood; 11 Dec 1989

#. [167] Double Precision Array Files (DAF) - Required
   Reading; latest version (`daf.req <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/daf.html>`__)

#. [212] COMMNT User's Guide
   (`commnt.ug <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/ug/commnt.html>`__)



DAF Run-Time Binary File Format Translation
-------------------------------------------

| Starting with the N0052 release of the SPICE Toolkit (January,
  1)    certain supported platforms are able to read DAF-based binary
  files (SPK, CK and binary PCK) that were written using a different,
  or non-native, binary representation. This access is read-only; any
  operations requiring writing to the file (adding information to the
  comment area, or appending additional ephemeris data, for example)
  require prior conversion of the file to the native binary file
  format. See the Convert User's Guide,
  `convert.ug <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/ug/convert.html>`__, for details.

Detection of Non-native Text Files
-----------------------------------

| Starting with the N0057 release of the SPICE Toolkit (March, 2004)
  the SPICE data loading mechanism detects and prohibits loading text
  kernel files containing lines terminated with EOF character(s)
  non-native to the platform on which the Toolkit was compiled. If a
  non-native EOL terminator is detected in the first 132 characters
  of a text kernel, the execution is stopped and an error message is
  displayed. This feature does not work with files that are smaller
  than 132 bytes or have the first line longer than 132 characters.

If you're in a hurry
=====================


| We'll discuss things in more detail in a moment but in case you are
  just looking for the right name of the function to perform some
  ephemeris task, here is a categorization of the most frequently
  used SPK and related functions in CSPICE. Input arguments are given
  in lower case and enclosed in `angle brackets.` Output arguments
  are given in plain lower case.

High Level Functions
--------------------

| Loading/Unloading an SPK file

* :py:meth:`~spiceypy.spiceypy.furnsh`
* :py:meth:`~spiceypy.spiceypy.unload`

Getting coverage summary

* :py:meth:`~spiceypy.spiceypy.spkobj`
* :py:meth:`~spiceypy.spiceypy.spkcov`

Retrieving states (position and velocity) using names of objects

* :py:meth:`~spiceypy.spiceypy.spkezr`

Retrieving positions using names of objects

* :py:meth:`~spiceypy.spiceypy.spkpos`

Retrieving states using NAIF ID codes

* :py:meth:`~spiceypy.spiceypy.spkez`
* :py:meth:`~spiceypy.spiceypy.spkgeo`

Retrieving positions using NAIF ID codes

* :py:meth:`~spiceypy.spiceypy.spkezp`
* :py:meth:`~spiceypy.spiceypy.spkgps`

Calculating `Uplink and Downlink` Light Time

* :py:meth:`~spiceypy.spiceypy.ltime`

Loading/Unloading Binary PCK files (see PCK Required Reading,
`pck <./pck.html>`__)

* :py:meth:`~spiceypy.spiceypy.furnsh`
* :py:meth:`~spiceypy.spiceypy.unload`

Loading Text based kernels---PCK, SCLK, etc.


* :py:meth:`~spiceypy.spiceypy.furnsh`

Loading/Unloading C-kernels (see CK Required Reading,
`ck <./ck.html>`__)


* :py:meth:`~spiceypy.spiceypy.furnsh`
* :py:meth:`~spiceypy.spiceypy.unload`



Foundation Functions
----------------------

| The functions listed in this section are the real `work horses`
  of the SPK and related systems. Not all of the functions in this
  section are described in this document. In those cases, the
  appropriate SPICE document is cited.

Selecting files and segments

* :py:meth:`~spiceypy.spiceypy.spksfs`

Computing states from segment descriptors

* :py:meth:`~spiceypy.spiceypy.spkpvn`

Correcting for stellar aberration

* :py:meth:`~spiceypy.spiceypy.stelab`

Translating between object names and object ID codes (see NAIF_IDS
Required Reading, `naif_ids <./naif_ids.html>`__)

* :py:meth:`~spiceypy.spiceypy.bodn2c`
* :py:meth:`~spiceypy.spiceypy.bodc2n`

Translating between frame names and frame ID codes (see Frames
Required Reading, `frames <./frames.html>`__)

* :py:meth:`~spiceypy.spiceypy.frmnam`
* :py:meth:`~spiceypy.spiceypy.namfrm`

State transformation matrices (see Frames Required Reading,
`frames <./frames.html>`__)

* :py:meth:`~spiceypy.spiceypy.sxform`

Classifying frames (see Frames Required Reading,
`frames <./frames.html>`__)

* :py:meth:`~spiceypy.spiceypy.frinfo`



Utility Programs
-----------------

| Examining SPK files


.. code-block:: python

      brief
      commnt
      spacit

Converting to and from transfer format

.. code-block:: python

      spacit
      tobin
      toxfr



Introduction
=======================


| To help fully understand the science data returned from a
  spacecraft's instruments it is necessary to know, at any given
  epoch, the positions and possibly the velocities of the spacecraft
  and all the target bodies of interest. The purpose of the
  SPK---which stands for S(pacecraft) and P(lanet) Kernel---file is
  to allow ephemerides for any collection of solar system bodies to
  be combined under a common file format, and accessed by a common
  set of functions.

Historically, ephemerides for spacecraft have been organized
differently from those for planets and satellites. They are usually
generated through different processes and using different
representations. However, there is no essential reason for keeping
them separate. A spacecraft, planet, satellite, comet, or asteroid
has a position and velocity relative to some center of mass and
reference frame. Consequently all of these objects can be represented
in an SPK file.

Consider the Galileo mission. Some of the objects of special interest
to the Galileo mission are:

.. code-block:: text

      Galileo Spacecraft
      Galileo Probe
      Earth
      Moon
      Earth Moon Barycenter
      Venus
      Sun
      Solar System Barycenter (S.S.B.)
      Asteroid Ida
      Ida's Satellite Dactyl
      Asteroid Gaspra
      Comet Shoemaker-Levy
      Jupiter System Barycenter (J.B.)
      Jupiter
      Io
      Ganymede
      Europa
      Callysto
      Goldstone Tracking Station.

Each of these objects has a position and velocity (state) relative to
some other object. The graph below illustrates which objects will be
used as reference objects for representing the states of others.

.. code-block:: text

                             +Gll
                            /             probe
                           /               |    o Comet
                   Gaspra /             Gll+   /  Shoemaker Levy
            Gll +--o     /                  \ /
                   |    /   Venus    Jupiter o--probe
                   |   /      o--+           |
       Gll +       |  /      /   Gll         |  Io
           |       | /      /                |  o-----+Gll
           |       |/      /             J.B.| /
      Ida  o-------o------o------------------o ----o------+Gll
          /         Sun   S.S.B.            / \    Europa
         o                 \      Ganymede /   \
      Dactyl                \             o     \
                             \            |      o Callisto
       Earth-Moon Barycenter  o----o      +      |
                              |   Moon    Gll    |
                              |                  + Gll
                              o Earth
                             / \
                            /   \
                           /     + Gll
                          o
                       Goldstone

This graph is somewhat complicated. Nevertheless, the complete
ephemeris history for all of these objects can be captured in a
single SPK file.
(Although we can store the entire ephemeris history illustrated above
in a single SPK file, for the sake of data management a project is
likely to use several SPK files. However, even in this case, all of
the SPK files can be used simultaneously.)

The SPK format is supported by a collection of functions that are
part of the CSPICE library---the major component of the SPICE
Toolkit. This family of SPK functions provides the following
capabilities:

#. Insert ephemeris data from some source into an SPK file.

#. Make the ephemeris data in one or more SPK files available to a user's program.

#. Return the apparent, true, or geometric state (position and velocity) of one ephemeris object as seen from another in some convenient reference frame.

The SPK software allows you to ignore the potential ephemeris
complexity associated with the a mission such as Galileo and allows
you to more directly compute various quantities that depend upon the
position or velocity of one object as seen from another.


SPK Files
=========


| SPICE software writes SPK files in a binary (non-ASCII) format
  structured in a NAIF developed abstract file architecture called
  Double Precision Array File (DAF). The DAF architecture and
  supporting software is discussed in the DAF Required Reading
  document, `daf.req <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/daf.html>`__. The SPICE file
  identification word occupying the first eight bytes of a properly
  created binary SPK file is `DAF/SPK` . For more information on
  SPICE identification words refer to the Kernel Required Reading
  document, `kernel <./kernel.html>`__. If you need only use
  SPK files as a data source or if you will use a SPICE utility
  program for creating SPK files, you can safely ignore aspects of
  the DAF system not covered by this document. On the other hand, if
  you plan to write software for creating SPK files you will probably
  need to familiarize yourself with the DAF software contained in
  CSPICE. The particular aspects of the DAF architecture that are
  relevant to the SPK format are discussed later in this document
  (see below---SPK Format).

Since SPKs are written as binary files, the specific binary format
depends on the computer architecture on which the SPK was created, in
the case of SPICE either big-endian or little-endian (NAIF no longer
supports DEC platforms).

Use of SPK files between computers
-----------------------------------

| NAIF extended the DAF capability in SPICE Toolkit delivery N0052 to
  allow reading of both big-endian and little-endian binary DAF files
  by all toolkits. This process is a run-time interpretation of
  non-native binary files. Run-time interpretation does not yet work
  for any file built upon the SPICE "DAS" architecture.

NAIF provides two utility programs---TOXFR and SPACIT for converting
SPICE binary kernels to a `transfer format` suitable for text
copying from one computer to another. Once the transfer format file
has been copied, the SPICE utilities TOBIN and SPACIT are available
for converting the transfer format file to the binary format suitable
for the new machine.

The utilities TOXFR and TOBIN are `command line` programs. To
convert a binary kernel to transfer format you simply type TOXFR
followed by the name of the binary kernel at your terminal prompt.

.. code-block:: text

      prompt> toxfr spk_file

To convert a transfer format to binary format, you type TOBIN
followed by the name of the transfer format kernel.
.. code-block:: text

      prompt> tobin transfer_file

The utility SPACIT is an interactive program that allows you to
select a function from a menu to perform on a file. This program can
also be used to convert to or from transfer format files.
Note that transfer format files cannot be `loaded` into a SPICE
based program to retrieve ephemeris data. Only binary format files
can be used for retrieving ephemeris data with SPICE software.

CSPICE (and by extension Icy and Mice) uses the same binary kernels
as does SPICELIB.

Examining SPK files
--------------------

| Since SPK files are binary files, you can't just open them with
  your favorite text editor to determine which ephemeris objects are
  represented in the file. Instead you need to use one of the SPICE
  utility programs that allow you to summarize the ephemeris contents
  of an SPK file. The first of these is SPACIT which was introduced
  above. The second is the command line utility BRIEF.

BRIEF gives a quick summary of the contents of the file and supports
a wide set of summary options. SPACIT on the other hand, provides
summaries that are more detailed and reflect closely the actual
internal structure of the file. Unless you need the more detailed
summary, you'll probably find BRIEF to be a better tool for examining
the contents of an SPK file.

Meta Data in the SPK file
---------------------------

| SPICE kernels may contain `meta` data that describe the
  contents, intended use, accuracy, etc. of the kernel. This meta
  data is called the `comments` portion of the kernel. Many SPK
  files contain comments that can help you decide upon the
  suitability of the kernel for your application. Two SPICE utilities
  are available for examining the comments of a binary
  kernel---COMMNT and SPACIT.

We've already introduced SPACIT. COMMNT is similar to SPACIT in that
it too is an interactive program. However, COMMNT also allows you to
modify the comments of an SPK file. Using COMMNT you can delete the
comments of an SPK file, extract the comments to a text file, or
append the text from some text file to the comments already present
in the kernel.

If you create SPK files, we strongly recommend that you add comments
to the kernel that describe who created it, expected usage of the
kernel, and the expected accuracy of the position/velocity
information contained in the kernel. A comment template is provided
in the appendix `COMMENTS`.

Warning: If you add comments to an SPK (or other binary kernel) using
COMMNT, you must wait for the program to complete the task before
exiting the program. Failure to wait for COMMNT to finish its work
will result in irreparable corruption of the binary kernel. (See the
COMMNT User's Guide, `commnt.ug <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/ug/commnt.html>`__, [212] for
details on the use of COMMNT).

Terminology
------------

| Throughout this document we shall be using terms such as reference
  frame, state, ephemeris time, etc. We include a brief review of
  these terms below.

**Reference Frame**
   A reference frame is a Cartesian coordinate system with three
   axes---x, y and z. The axes are mutually orthogonal. The center of
   the frame is the origin of the Cartesian reference system. For the
   reference frames in SPICE, the positions of the axes are typically
   defined by some observable object. For example, in the J2000
   reference frame, the x-axis is defined to lie in the intersection
   of two planes: the plane of the Earth's equator and the plane of
   the Earth's orbit. The z-axis is perpendicular to the Earth's
   equator. The y-axis completes a right-handed system. The center of
   the frame is typically taken to be the solar system barycenter.
   (Note we are not attempting to rigorously define the J2000 frame
   here. We are only illustrating how reference frames are defined.
   Many more details are required for a rigorous definition of the
   J2000 frame. These details are given in the SPICE document
   `Frames` [349].)

**State**
   A state is an array of six double precision numbers. The first
   three numbers give the x, y, and z coordinates respectively for
   the position of some object relative to another object in some
   Cartesian reference frame. The next three numbers give the
   velocity ( dx/dt, dy/dt and dz/dt respectively) of the object with
   respect to the same reference frame.

**Inertial Frame**
   An inertial frame, is one in which Newton's laws of motion apply.
   A frame whose axes are not moving with respect to the observed
   positions of distant galaxies and quasars approximates an inertial
   frame.

**Non-Inertial Frame**
   A non-inertial frame is a frame that rotates with respect to the
   celestial background. For example a frame whose axes are fixed
   with respect to the features on the surface of the Earth is a
   non-inertial frame.

**Ephemeris Time (ET)**
   Ephemeris time, ET, is the independent variable in the equations
   of motion that describe the positions and velocities of objects in
   the solar system. In CSPICE we treat ET as a synonym for
   Barycentric Dynamical Time. As far as has been experimentally
   determined, an atomic clock placed at the solar system barycenter,
   would provide a faithful measure of ET.

**Seconds Past 2000**
   In the SPK system times are specified as a count of seconds past a
   particular epoch---the epoch of the J2000 reference frame. This
   reference epoch is within a second or two of the UTC epoch:
   12:01:02.184 Jan 1, 2000 UTC. (See the document
   `time.req <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/time.html>`__ for a more thorough discussion of
   the J2000 epoch). Epochs prior to this epoch are represented as
   negative numbers. The `units` of ET are designated in several
   different ways: seconds past 2000, seconds past J2000, seconds
   past the Julian year 2000, seconds past the epoch of the J2000
   frame. All of these phrases mean the same thing and are used
   interchangeably throughout this document.

**SPK segment**
   The trajectories of objects in SPK files are represented in pieces
   called segments. A segment represents some arc of the full
   trajectory of an object. Each segment contains information that
   specifies the trajectory of a particular object relative to a
   particular center of motion in a fixed reference frame over some
   particular interval of time. From the point of view of the SPK
   system segments are the atomic portions of a trajectory.



The SPK Family of Functions
============================


| CSPICE contains a family of functions that are designed
  specifically for use with SPK files. The name of each function
  begins with the letters `spk`, followed by a two- or
  three-character mnemonic. For example, the function that returns
  the state of one body with respect to another is named
  :py:meth:`~spiceypy.spiceypy.spkezr`, pronounced `S-P-K-easier`.
  A complete list of mnemonics, translations, and calling sequences
  can be found at the end of this document.

Each function is prefaced by a complete CSPICE header, which
describes inputs, outputs, restrictions, and exceptions, discusses
the context in which the function can be used, and shows typical
examples of its use. Any discussion of the functions in this document
is intended as an introduction: the final documentation for any
function is its header.

Whenever an SPK function appears in an example, the translation of
the mnemonic part of its name will appear to the right of the
reference, in braces. We also continue with the convention of
distinguishing between input and output arguments by enclosing input
arguments in angle brackets. For example,


.. code-block:: python

      state, lt = spkezr( <targ>,  <et>,  <frame>, <aberr>, <obs>)  # Easier state

All C functions, including those whose names do not begin with
`SPK`, are from CSPICE or the standard ANSI C library.
SPK readers are available to perform the following functions.

#. Determine the apparent, true, or geometric state of a body with respect to another body relative to a user specified reference frame.

#. Determine the apparent, true, or geometric state of a body with respect to an observer having a user-supplied state.

#. Determine the geometric state of a body with respect to the solar system barycenter.

#. Determine the geometric state of a target body with respect to its center of motion for a particular segment.

#. Determine, from a list of SPK files supplied by the calling program, the files and segments needed to fulfill a request for the state of a particular body.



Computing States
-----------------

| :py:meth:`~spiceypy.spiceypy.spkezr` is the most powerful of the
  SPK readers. It determines the apparent, true, or geometric state
  of one body (the target) as seen by a second body (the observer)
  relative to a user specified reference frame.


.. code-block:: python

      state, lt = spkezr( <targ>,  <et>,  <frame>, <aberr>, <obs>)  #  Easier state

The function accepts five inputs---target body, epoch, reference
frame, aberration correction type, and observing body---and returns
two outputs---state of the target body as seen from the observing
body, and one-way light-time from the target body to the observing
body.
The target body, observing body and frame are identified by strings
that contain the names of these items. For example, to determine the
state of Triton as seen from the Voyager-2 spacecraft relative to the
J2000 reference frame


.. code-block:: python

      state, lt = spkezr( "triton",  et,  "j2000", aberr, "voyager-2" ) #  Easier state

By definition, the ephemerides in SPK files are continuous: the user
can obtain states at any epoch within the interval of coverage.
Epochs are always specified in ephemeris seconds past the epoch of
the J2000 reference system (Julian Ephemeris Date 2451545.0 ) For
example, to determine the state of Triton as seen from Voyager-2 at
Julian Ephemeris Date 2447751.8293,

.. code-block:: python

      et = ( 2447751.8293 - j2000_c() ) * spd_c()

      state, lt = spkezr( "triton", et, "j2000", <aberr>,  "voyager-2" ) #  Easier state

where the function :py:meth:`~spiceypy.spiceypy.j2000` returns the
epoch of the J2000 frame (Julian Ephemeris Date 2451545.0) and the
function :py:meth:`~spiceypy.spiceypy.spd` returns the number of
seconds per Julian day (86400.0).
The ephemeris data in an SPK file may be referenced to a number of
different reference frames. States returned by
:py:meth:`~spiceypy.spiceypy.spkezr` do not have to be referenced
to any of these `native` frames. The user can specify that states
are to be returned in any of the frames recognized by the frame
subsystem. For example, to determine the state of Triton as seen from
Voyager-2, referenced to the J2000 ecliptic reference frame,


.. code-block:: python

      state, lt = spkezr( "triton", et, "eclipj2000", aberr, "voyager-2") #  Easier state

:py:meth:`~spiceypy.spiceypy.spkezr` returns apparent, true, or
geometric states depending on the value of the aberration correction
type flag `aberr`.
Apparent states are corrected for planetary aberration, which is the
composite of the apparent angular displacement produced by motion of
the observer (stellar aberration) and the actual motion of the target
body (correction for light-time). True states are corrected for
light-time only. Geometric states are uncorrected.

Instead of using the potentially confusing terms `true` and
`geometric` to specify the type of state to be returned,
:py:meth:`~spiceypy.spiceypy.spkezr` requires the specific
corrections to be named. To compute apparent states, specify
correction for both light-time and stellar aberration: `LT+S`. To
compute true states, specify correction for light-time only: `LT`.
To compute geometric states, specify no correction: `NONE`.

In all cases, the one-way light-time from the target to the observer
is returned along with the state.

Computing States using Constant-Velocity or Constant-Position Objects
----------------------------------------------------------------------

| Objects such as tracking stations, rover or spacecraft components,
  or fixed surface points can be treated by the SPK subsystem as
  ephemeris objects just as easily as bodies such as planets and
  natural satellites. For example, using an SPK file for the
  geocentric location of a tracking station enables
  :py:meth:`~spiceypy.spiceypy.spkezr` to compute states of targets
  relative to the tracking station, providing all needed kernel data
  have been loaded.

However, it is not always convenient to create an SPK file to provide
data for an ephemeris object, particularly when that object's
location is known only at run time.

For an object that has constant velocity, relative to a specified
center of motion, in a specified reference frame, CSPICE offers a set
of functions to compute states relative to other ephemeris objects,
where the other objects have ephemeris data provided by SPK files:


.. code-block:: python

      spkcpo_c  # SPK, constant position observer state
      spkcpt_c  # SPK, constant position target state
      spkcvo_c  # SPK, constant velocity observer state
      spkcvt_c  # SPK, constant velocity target state

The `constant position` routines have simplified interfaces; these
handle the special case where the constant velocity is zero.
Each of the above functions requires that sufficient SPK data be
available to compute the state of the center of motion, relative to
the other ephemeris object, of the constant-velocity or
constant-position object.

States computed by SPK functions for constant-velocity or
constant-position objects optionally can be corrected for light time
and stellar aberration, just as is done by
:py:meth:`~spiceypy.spiceypy.spkezr`.

A limitation of representing objects using constant velocities or
positions, instead of creating SPK files to provide the ephemerides
of those objects, is that high-level CSPICE geometry routines such as
:py:meth:`~spiceypy.spiceypy.sincpt` or
:py:meth:`~spiceypy.spiceypy.subpt` cannot work with such
objects---these functions require SPK data for all ephemeris objects
participating in the computations they perform.

The Computation of Light Time
------------------------------

| The light time corrected position component of a state vector
  returned by the SPK system is the 3-vector difference

.. code-block:: text

      TARGET_SSB ( ET + S*LT )  - OBSERVER_SSB ( ET )

where TARGET_SSB and OBSERVER_SSB give the position of the target and
observer relative to the solar system barycenter, and where S is -1
for reception corrections (where light travels from the target to the
observer) and 1 for transmission corrections (where light travels
from the observer to the target).
LT is the unique number that satisfies:

.. code-block:: text

            | TARGET_SSB ( ET + S*LT )  -  OBSERVER_SSB ( ET ) |
      LT =  ----------------------------------------------------
                              Speed of Light

where
.. code-block:: text

      | position |

indicates the length of a position vector.
The velocity portion of the returned state is the derivative with
respect to the observation time ET of the light time corrected
position.

Mathematically, LT can be computed to arbitrary precision via the
following algorithm:

.. code-block:: text

      LT_0 = 0



              | TARGET_SSB ( ET - LT_(i-1) ) - OBSERVER_SSB ( ET ) |
      LT_i =  ------------------------------------------------------
                                 Speed of Light


         for i = 1, ...

It can be shown that the sequence LT_0, LT_1, LT_2, ... converges to
LT geometrically. Moreover, it can be shown that the difference
between LT_i and LT satisfies the following inequality.

.. code-block:: text

                                    i
      | LT - LT_i | < LT_i * ( V/C )  / ( 1 - V/C )
         for i = 1, ...


where V is the maximum speed of the target body with respect to the
solar system barycenter and C is the speed of light.


Precision of Light Time Computations
----------------------------------------

| Let's examine the error we make if we use LT_2 as an approximation
  for LT. This is an analysis of precision; we'll ignore errors in
  the data and those in the input times.

For nearly all objects in the solar system V is less than 60 km/sec.
The value of C is approximately 300000 km/sec. Thus V/C is 2.0E-4,
and the one iteration solution for LT (in which the target-SSB vector
is corrected once) has a potential relative error of not more than
4.0E-8. This is a potential light time error of approximately 2.0E-5
seconds per astronomical unit of distance separating the observer and
target. Thus as long as the observer and target are separated by less
than 50 Astronomical Units, the error in the light time returned
using option `LT` is less than 1 millisecond.

For this reason, CSPICE uses LT_2 to approximate LT when you request
a light time corrected state by setting the aberration correction
argument in :py:meth:`~spiceypy.spiceypy.spkezr` to any of `LT`,
`XLT`, `LT+S`, `XLT+S`.

The maximum error in the light time corrected target-SSB position
vector is larger by a factor of C/V than V times the maximum relative
light time error. This is because the (i-1)st light time estimate is
used to compute the ith estimate of target-SSB position vector. Given
the assumptions above, the maximum position error for the `LT`-style
correction is bounded by

.. code-block:: text

      60 km/s * (1/(2.0E-4)) * 2*1.0E-5 s / AU

or 6 km per astronomical unit of distance separating the observer and
target.
In practice, the difference between positions obtained using
one-iteration and converged light time is usually much smaller than
the value computed above and can be insignificant. For example, for
the spacecraft Mars Reconnaissance Orbiter and Mars Express, the
position error for the one-iteration light time correction, applied
to the spacecraft-to-Mars center vector, is approximately 2 cm.

You can make :py:meth:`~spiceypy.spiceypy.spkezr` (and other
applicable SPK functions) compute a better approximation to LT and
compute more accurate light-time corrected states by commanding that
it compute a `converged Newtonian` value for LT. To do this set
the light time portion of the aberration correction specification to
`CN` (the possible such aberration correction specifications
are`CN', `XCN`, `CN+S`, or `XCN+S`).
:py:meth:`~spiceypy.spiceypy.spkezr` will then return a converged
value, usually equal to LT_4, as the approximation for light time;
the returned state will be converged as well. Then the maximum error
in LT_4 is less than

.. code-block:: text

      1.0E-3 * (V/C)**2 seconds

which is less than 4e-11 seconds for any observer/target pair in the
solar system that satisfies the assumptions above. The corresponding
position error bound is 1.2 cm at a separation of 50 AU.
However, you should note that this is a purely Newtonian
approximation to the light time. To model the actual light time
between target and observer one must take into account effects due to
General relativity. These may be as high as a few hundredths of a
millisecond for some geometric cases.

The functions in the SPK family do not attempt to perform either
general or special relativistic corrections in computing the various
aberration corrections. For many applications relativistic
corrections are not worth the expense of added computation cycles.
If, however, your application requires these additional corrections
we suggest you consult the astronomical almanac (page B36) for a
discussion of how to carry out these corrections.

Light Time Corrected Non-Inertial States
-----------------------------------------

| When we observe a distant object, we don't see it as it is at the
  moment of observation. We see it as it was when the photons we have
  sensed were emitted by or reflected from the object. Thus when we
  look at Mars through a telescope, we see it not as it is now, but
  rather as it was one `light-time` ago. This is true not only for
  the position of Mars, but for its orientation as well.

Suppose that a large balloon has been launched into the Martian
atmosphere and we want to determine the Mars bodyfixed state of the
balloon as seen from Earth at the epoch ET. We need to determine both
the light time corrected position of the balloon, and the light time
corrected orientation of Mars. To do this we compute two light times.
The light time to the center of the Mars bodyfixed frame (i.e. the
center of Mars) and the light time to the balloon. Call the light
time to the center of the Mars frame LT_F and call the light time to
the balloon LT_T. The light time corrected state of the balloon
relative to the Mars bodyfixed frame is the location of the balloon
at ET - LT_T in the bodyfixed frame of Mars as oriented at ET - LT_F.

:py:meth:`~spiceypy.spiceypy.spkezr` carries out all of these
computations automatically. In this case the computation would be
computed by a function call similar to this:


.. code-block:: python

      spkezr( "mars_balloon",  <et>,  "iau_mars", "lt",
                 "earth",         state, lt              )

:py:meth:`~spiceypy.spiceypy.spkezr` uses the following rules when
computing states.

#. When no corrections are requested from
   :py:meth:`~spiceypy.spiceypy.spkezr` (ABCORR = 'NONE'), the state
   of the target is determined at the request time ET and is
   represented in the specified reference frame as it is oriented at
   time ET.

#. When light time corrections are requested from
   :py:meth:`~spiceypy.spiceypy.spkezr` (ABCORR = 'LT'), two light
   times are determined: LT_F the light time to the center of the
   specified reference frame, and LT_T the light time to the target.
   The state of the target is given as it was at ET - LT_T in the
   frame as it was oriented at ET - LT_F.

#. When light time and stellar aberrations are requested from
   :py:meth:`~spiceypy.spiceypy.spkezr` (ABCORR = 'LT+S'), both LT_F
   and LT_T are again computed. The state of the target at ET - LT_T
   is corrected for stellar aberration and represented in the
   reference frame as it was oriented at ET - LT_F.

#. Light-time corrected velocities are computed taking into
   account the rate of change of light time both between observer and
   target and between observer and the center of the non-inertial
   frame. The rate of change of the target frame's orientation is
   accounted for as well.

In the actual implementation of
:py:meth:`~spiceypy.spiceypy.spkezr` a few short cuts are taken.
When light time requested states relative to an inertial frame are
requested, the orientation of the frame is not corrected for light
time. The orientation of an inertial frame at ET - LT_F is the same
as the orientation of the frame at ET. Computations involving
inertial frames take advantage of this observation and avoid
redundant computations.


An example
------------------------------------------------------------------------------------------------------------

| Here we illustrate how you could use
  :py:meth:`~spiceypy.spiceypy.spkezr` together with other CSPICE
  functions to determine if at a particular epoch ET the Mars Global
  Surveyor spacecraft is occulted by Mars.

We will need the lengths of the axes of the triaxial ellipsoid that
is used to model the surface of Mars. Either of the CSPICE functions
:py:meth:`~spiceypy.spiceypy.bodvcd` or
:py:meth:`~spiceypy.spiceypy.bodvrd` will retrieve this information
from a loaded PCK file. :py:meth:`~spiceypy.spiceypy.bodvrd` uses
the name of the body, while :py:meth:`~spiceypy.spiceypy.bodvcd`
uses the NAIF ID code for Mars (499) to retrieve the lengths of the
axes. We may call :py:meth:`~spiceypy.spiceypy.bodvcd` as shown:


.. code-block:: python

      nvals, axes =bodvcd( 499, "RADII", 3 )

      a = axes[0];
      b = axes[1];
      c = axes[2];

Next we compute the state of Mars relative to Earth and the state of
MGS relative to Earth in the Mars bodyfixed frame.

.. code-block:: python

      marsst, lt = spkezr( "mars", et, "iau_mars", "lt+s",  "earth")
      mgsst,  lt = spkezr( "mgs",  et, "iau_mars", "lt+s", "earth") # Easier State

Compute the apparent position of the Earth relative to Mars in the
apparent Mars bodyfixed frame. This means simply negating the
components of `marsst`. The CSPICE function
:py:meth:`~spiceypy.spiceypy.vminus` carries out this task.

.. code-block:: python

      vminus( marsst, estate )

Determine if the line of sight from Earth to MGS intersects the
surface of Mars. The CSPICE function
:py:meth:`~spiceypy.spiceypy.surfpt` will find this intersection
point if it exists.

.. code-block:: python

      surfpt( estate, mgsst, a, b, c, point, &found )

Finally, if a point of intersection was found, was it between the
Earth and the MGS spacecraft. To find out we can compare the
distances between the intersection point and the spacecraft. The
CSPICE function :py:meth:`~spiceypy.spiceypy.vnorm` computes the
length of the vector from Earth to MGS. The function
:py:meth:`~spiceypy.spiceypy.vdist` computes the distance between
the point and the Earth.

.. code-block:: python

      if ( found )
         {
         betwn = (  vdist ( estate, point ) < vnorm ( mgsst )  )
         }
      else
         {
         betwn = SPICEFALSE;
         }


      if ( betwn )
         {
         printf ( "mgs is behind mars\n" )
         }
      else
         {
         printf ( "mgs is not behind mars\n" )
         }



Integer ID Codes Used in SPK
------------------------------------------------------------------------------------------------------------

| Low level SPK software uses integer codes to identify ephemeris
  objects, reference frames and data representation, etc. At low
  levels of the SPICE system only integer codes are used to
  communicate information about objects. To some extent, these codes
  are a historical artifact in the design of the SPICE system.
  Nevertheless, these integer codes provide economies in the
  development of SPICE software.

High-level SPICE software uses names (character strings) to refer to
the various SPICE objects and translates between names and integer
codes. Thus to some extent you can disregard the integer codes used
by the SPICE internals. However, occasionally, due to the
introduction of new ephemeris objects, the name translation software
will be unable to find a name associated with an ID code. To retrieve
states for such an object you will need to use the integer code for
the object in question. If you are using
:py:meth:`~spiceypy.spiceypy.spkezr`, you can supply this integer
code as a quoted string. For example the following two function calls
will both return the state of TRITON as seen from Voyager-2. (The
NAIF integer code for TRITON is 801; the NAIF integer code for
Voyager 2 is -32).


.. code-block:: python

    state, lt = spkezr( "triton", et, "eclipJ2000", aberr,    "voyager-2") #  Easier state
    state, lt = spkezr( "801", et, "eclipJ2000", aberr,   "-32" ) #  Easier state

Consult the NAIF IDS Required Reading file,
`naif_ids <./naif_ids.html>`__, for the current list of body
codes recognized by the SPICE Toolkit software.


:py:meth:`~spiceypy.spiceypy.spkez`
------------------------------------------------------------------------------------------------------------^^^^^^^^^^^^^^^^^^^^

| :py:meth:`~spiceypy.spiceypy.spkezr` relies upon two lower level
  functions that may be useful under certain circumstances.

The function :py:meth:`~spiceypy.spiceypy.spkez` performs the same
functions as :py:meth:`~spiceypy.spiceypy.spkezr`. The only
difference is the means by which objects are specified.
:py:meth:`~spiceypy.spiceypy.spkez` requires that the target and
observing bodies be specified using the NAIF integer ID codes for
those bodies.


.. code-block:: python

      state, lt = spkez( <targ_id>, <et>, <frame>, <corr>, <obj_id> ) #  SPK Easy

The NAIF-ID codes for ephemeris objects are listed in the NAIF_IDS
required reading file, `naif_ids <./naif_ids.html>`__.
:py:meth:`~spiceypy.spiceypy.spkez` is useful in those situations
when you have ID codes for objects stored as integers. There is also
a modest efficiency gain when using integer ID codes instead of
character strings to specify targets and observers.

The function :py:meth:`~spiceypy.spiceypy.spkgeo` returns only
geometric (uncorrected) states. The following two function calls are
equivalent.


.. code-block:: python

      state, lt = spkez( <targ_id>,  <et>,   <frame>, "none", <obj_id>  ) # SPK Easy

      state, lt = spkgeo( <targ_id>,  <et>,   <frame>, <obj_id> ) # SPK Geometric

:py:meth:`~spiceypy.spiceypy.spkgeo` involves slightly less
overhead than does :py:meth:`~spiceypy.spiceypy.spkez` and thus may
be marginally faster than calling
:py:meth:`~spiceypy.spiceypy.spkez`.


Loading Files
------------------------------------------------------------------------------------------------------------

| Note that :py:meth:`~spiceypy.spiceypy.spkezr`,
  :py:meth:`~spiceypy.spiceypy.spkez` and
  :py:meth:`~spiceypy.spiceypy.spkgeo` do not require the name of
  an SPK file as input. These functions rely on the lower level
  routine in the SPK subsystem to maintain a database of ephemeris
  files. Your application program indicates which files are to be
  used by passing their names to function
  :py:meth:`~spiceypy.spiceypy.furnsh` -- `generic loader` that
  can be used to load SPICE kernel files of any type.


.. code-block:: python

      for e in ephem
          spice.furnsh(e)        # Load kernel file
      # or more simply:
      spice.furnsh(ephem)

In general, a state returned by
:py:meth:`~spiceypy.spiceypy.spkezr` is built from several more
primitive states. Consider the following diagram, which shows some of
the states that might be needed to determine the state of the Galileo
spacecraft as seen from Earth:

.. code-block:: text

               Jupiter_Barycenter --- Europa
               /                       \
              /                         \
             /                          Spacecraft
            /
           /
          /
         /
      SSB
         \
          \
           \
           EMB --- Earth

(SSB and EMB are the solar system and Earth-Moon barycenters.)
Each state is computed from a distinct segment. The segments may
reside in a single SPK file, or may be contained in as many as five
separate files. For example, the segments needed to compute the
Earth-spacecraft state shown above might come from the following set
of files:


.. code-block:: python

      furnsh( "barycenters.bsp"    )  # Load kernel file
      furnsh( "planet-centers.bsp" )  # Load kernel file
      furnsh( "satellites.bsp"     )  # Load kernel file
      furnsh( "spacecraft.bsp"     )  # Load kernel file

or from the following set:


.. code-block:: python

      furnsh( "earth.bsp"      )      # Load kernel file
      furnsh( "jupiter.bsp"    )      # Load kernel file
      furnsh( "spacecraft.bsp" )      # Load kernel file



Data Precedence
------------------------------------------------------------------------------------------------------------

| An SPK file may contain any number of segments. A single file may
  contain overlapping segments: segments containing data for the same
  body over a common interval. When this happens, the latest segment
  in a file supersedes any competing segments earlier in the file.
  Similarly, the latest file loaded supersedes any earlier files. In
  effect, several loaded files become equivalent to one large file.

Unloading Files
------------------------------------------------------------------------------------------------------------

| The number of SPK files that may be loaded at any one time is
  limited but very large -- up to 5000 total for all loaded SPK, CK,
  and binary PCK files combined. Although unlikely, in some cases
  your application program may need to unload some SPK files to make
  room for others or to remove a particular SPK from the set of
  loaded data. An SPK file may be unloaded by supplying its name to
  function :py:meth:`~spiceypy.spiceypy.unload` -- `generic
  unloader` that can be used to unload SPICE kernel of any type. The
  sequence of statements shown below,


.. code-block:: python

      furnsh( "file.a" )     # Load kernel file
      furnsh( "file.b" )     # Load kernel file
      furnsh( "file.c" )     # Load kernel file
      unload( "file.b" )     # Unload kernel file
      furnsh( "file.d" )     # Load kernel file
      unload( "file.c" )     # Unload kernel file

is equivalent to the following (shorter) sequence:


.. code-block:: python

      furnsh( "file.a" )     # Load kernel file
      furnsh( "file.d" )     # Load kernel file



Getting Coverage Summary
------------------------------------------------------------------------------------------------------------

| The CSPICE includes two functions for obtaining information about
  the contents of an SPK file from within an application.

The :py:meth:`~spiceypy.spiceypy.spkobj` function provides an API
via which an application can find the set of bodies for which a
specified SPK file contains data. The body IDs are returned in a
SPICE `set` data structure (see `sets.req <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/sets.html>`__).

The :py:meth:`~spiceypy.spiceypy.spkcov` function provides an API
via which an application can find the time periods for which a
specified SPK file provides data for an body of interest. The
coverage information is a set of disjoint time intervals returned in
a SPICE `window` data structure (see `other stuff tutorial <./other_stuff.html>`__ and
`windows.req <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/windows.html>`__).

Refer to the headers of :py:meth:`~spiceypy.spiceypy.spkobj` and
:py:meth:`~spiceypy.spiceypy.spkcov` for details on the use of
those routines.

Loading Auxiliary Files
------------------------------------------------------------------------------------------------------------

| Prior to the inclusion of non-inertial frames in the SPK system,
  the states of objects computed by the SPK system required only that
  you load the correct SPK files and call the correct functions. The
  inertial frame transformations needed for converting from one
  inertial frame to another are `hard wired` into the SPICE
  system. The transformations are part of the object code of the
  CSPICE library---no additional data need be supplied to compute
  these transformations. This approach to carrying out inertial frame
  transformations was chosen because the transformations are
  compactly represented and do not change as the result of further
  observations. They are essentially definitions.

On the other hand, the orientation of non-inertial frames with
respect to other frames are almost always the result of observation.
They are improved and extended as further observations are made. For
some of these frames (such as spacecraft fixed frames) very large
data sets are needed to express the orientation of the frame with
respect to other frames. Frame transformations that are a function of
time and require megabytes of data are not suitable for encapsulation
in C or FORTRAN source code. As a result, in the SPICE system, the
computation of non-inertial frame transformations depends upon data
stored in other SPICE kernels. If you request states relative to a
non-inertial frame or use ephemerides that are represented relative
to non-inertial frames you must load additional SPICE kernels. The
method by which an auxiliary kernel is loaded depends upon the type
of the kernel.

There are currently five classes of reference frames that are
supported by the SPICE system. We give a brief overview of these
frames here. For a more thorough discussion of the various types of
frames see the recommended reading file
`frames <./frames.html>`__.

Inertial frames

- Inertial frames are built into the SPICE system. You don't
  need to do anything to make their definitions available to your
  program. Inertial frames have NAIF ID codes whose values are in the
  range from 1 to 10000.

PCK frames

- PCK frames are bodyfixed frames. The orientation of a PCK
  frame is always expressed relative to an inertial frame. The
  relationship between a PCK frame and its associated inertial frame
  is provided by a PCK kernel. PCK frames have ID codes between 10000
  and 100000. There are two types of PCK kernels---binary and text.
  Binary PCK kernels are loaded (and unloaded) in a fashion analogous
  to the loading and unloading of SPK files. To load a binary PCK
  file

furnsh( <file> )

- To unload a binary PCK file


.. code-block:: python

               unload( <file> )

- Text based PCK files are loaded via the function
  :py:meth:`~spiceypy.spiceypy.furnsh`.


.. code-block:: python

               furnsh( <file> )

CK Frames

- CK frames are frames that are defined relative to a spacecraft
  structure. The orientation of the structure is provided through a
  binary SPICE kernel called a C-kernel. The ID codes for C-kernel
  frames are negative and usually less than -999. A C-kernel frame
  may be defined relative to any other kind of frame. (Most existing
  C-kernels are defined relative to inertial frames.)

- C-kernels are loaded and unloaded using the same loader
  functions as used to load and unload SPK kernels. To load a
  C-kernel


.. code-block:: python

               furnsh( <file> )

- To unload a C-kernel


.. code-block:: python

               unload( <file> )

- The times used to represent C-kernels are spacecraft clock
  times---not ET. The relationship between ET and spacecraft clock
  times is stored in a SPICE text kernel called a spacecraft clock
  kernel---usually abbreviated as SCLK (ess-clock) kernel. To
  retrieve states relative to a CK frame you need to make the
  relationship between ET and the spacecraft clock available to your
  program by loading the appropriate SCLK kernel. SCLK kernels are
  loaded via the function :py:meth:`~spiceypy.spiceypy.furnsh`.


.. code-block:: python

               furnsh( <sclk_file_name> )

TK Frames

- TK frames (short for Text Kernel frames) are frames that are
  defined via a SPICE text kernel. These frames can be transformed to
  another reference frame via a constant rotation matrix. Typical
  examples are topocentric frames and instrument frames. TK frames
  are loaded via the function :py:meth:`~spiceypy.spiceypy.furnsh`.


.. code-block:: python

               furnsh( <TK_frame_file> )

Dynamic Frames

- Dynamic frames, like TK frames, are defined via a SPICE text
  kernel. A dynamic frame has time-varying rotation relative to its
  base frame. A dynamic frame can be defined by two time-varying
  vectors, by a set of precession, nutation, and obliquity models, or
  by a set of Euler angles. Typical examples are the geocentric solar
  ecliptic frame or the Earth true equator and true equinox of date
  frame. Dynamic frames are loaded via the function
  :py:meth:`~spiceypy.spiceypy.furnsh`.


.. code-block:: python

               furnsh( <Dynamic_frame_file> )

In addition to the files mentioned above, it may be necessary to load
a `frame definition` file along with the one of the SPICE kernels
listed above. (If the producer of the file has done his or her
homework this step should be unnecessary.) The frame definition file
is a SPICE text kernel that specifies the type of the frame, the
center of the frame, the name of the frame, and its ID code. (See
`frames <./frames.html>`__ for more details concerning frame
definitions.)
As is evident from the above discussion, the use of non-inertial
frames requires more data management on the part of the user of the
SPICE system. However, this data management problem is not a new
problem. In previous versions of the SPICE system the same kernels
would have been required. Moreover, in previous versions of the SPICE
system, you would have been required to perform all non-inertial
transformations in your own code. With the inclusion of non-inertial
frames in the SPK system, we have relieved you of some of the tasks
associated with non-inertial frames.

SPK File Structure
===================


| An SPK file is made up of one or more data `segments` and a
  `comment` area. These components are described below.

Segments--The Fundamental SPK Building Blocks
------------------------------------------------------------------------------------------------------------

| An SPK file contains one or more `segments.` Each segment
  contains ephemeris data sufficient to compute the geometric state
  (position and velocity) of one solar system body (the `target`)
  with respect to another (the `center`) at any epoch throughout
  some finite interval of time.

Either body may be a spacecraft, a planet or planet barycenter, a
satellite, a comet, an asteroid, a tracking station, a roving
vehicle, or an arbitrary point for which an ephemeris has been
calculated. Each body in the solar system is associated with a unique
integer code. A list of names and codes for the planets, major
satellites, spacecraft, asteroids and comets can be found in the
document `naif_ids <./naif_ids.html>`__

The states computed from the ephemeris data in a segment must be
referenced to a single, recognized reference frame.

The data in each segment are stored as an array of double precision
numbers. The summary for the array, called a `descriptor`, has two
double precision components:

#. The initial epoch of the interval for which ephemeris data
   are contained in the segment, given in ephemeris seconds past
   Julian year 2000.

#. The final epoch of the interval for which ephemeris data are
   contained in the segment, given in ephemeris seconds past Julian
   year 2000.

The descriptor has six integer components:

#. The NAIF integer code for the target.

#. The NAIF integer code for the center.

#. The NAIF integer code for the reference frame.

#. The integer code for the representation (type of ephemeris data).

#. The initial address of the array.

#. The final address of the array.

In addition to a descriptor, each array also has a name. The name of
each array may contain up to 40 characters. This space may be used to
store a brief description of the segment. For example, the name may
contain pedigree information concerning the segment or may contain
the name of the object whose position is recorded in the segment.


Segment Order and Priority
------------------------------------------------------------------------------------------------------------

| Segments within an SPK file need not be ordered according to time;
  segments covering (that is, providing data for) a later time period
  may precede segments covering an earlier time period.

However, segment order does imply priority. For a given target body,
segment priority increases with distance from the start of the file:
segments closer to the end of the file have higher priority than
segments for the same target body that occur earlier in the file.
When a data request for a specified target body is made, the segment
for that target body with highest priority, and whose time interval
includes the request time, will be selected to satisfy the request.

SPK producers should note that this priority scheme would cause a
higher priority segment for a target body to mask a lower priority
segment for the same body over the intersection of the coverage
intervals of the two segments, if two such segments were written to
an SPK file. In particular, if an SPK file contained two segments for
the same target body and time interval, where the segments had
different central bodies, the lower priority segment would be
invisible to the SPK system.

The Comment Area
------------------------------------------------------------------------------------------------------------

| Preceding the `segments`, the Comment Area provides space in the
  SPK file for storing textual information besides what is written in
  the array names. Ideally, each SPK file would contain internal
  documentation that describes the origin, recommended use, and any
  other pertinent information about the data in that file. For
  example, the beginning and ending epochs for the file, the names
  and NAIF integer codes of the bodies included, an accuracy
  estimate, the date the file was produced, and the names of the
  source files used in making the SPK file could be included in the
  Comment Area.

The utility programs COMMNT and SPACIT may be used to examine and
manipulate the comments in an SPK file. In addition to these
utilities, CSPICE provides a family of functions for handling this
Comment Area. The name of each function in this family begins with
the letters `SPC` which stand for `SPk and Ck` because this feature
is common to both types of files. The SPC software provides the
ability to add, extract, read, and delete comments and convert
commented files from binary format to SPICE transfer format and back
to binary again.

The SPC functions and their functions are described in detail in the
SPC Required Reading, `spc <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/spc.html>`__.

SPK Data Types
------------------------------------------------------------------------------------------------------------

| The fourth integer component of the descriptor---the code for the
  representation, or `data type` ---is the key to the SPK format.

For purposes of determining the segment best suited to fulfill a
particular request, all segments are treated equally. It is only when
the data in a segment are to be evaluated---when a state vector is to
be computed---that the type of data used to represent the ephemeris
becomes important.

Because this step is isolated within a single low-level reader,
:py:meth:`~spiceypy.spiceypy.spkpvn`, new data types can be added
to the SPK format without affecting application programs that use the
higher level readers. :py:meth:`~spiceypy.spiceypy.spkpvn` is
designed so that the changes required to implement a new data type
are minimal.

There are no real limits on the possible representations that can be
used for ephemeris data. Users with access to data suitable for
creating an ephemeris may choose to invent their own representations,
adapting :py:meth:`~spiceypy.spiceypy.spkpvn` accordingly. (We
recommend that you consult with NAIF prior to implementing a new data
type.)

The data types currently supported by CSPICE software are listed
under `Supported Data Types` later in this document.

Primitive States
=================


| At the lowest level, it is possible to compute states without
  combining them at all. Given the handle and descriptor for a
  particular segment, function :py:meth:`~spiceypy.spiceypy.spkpvn`
  returns a state from that segment directly.


.. code-block:: python

      ref, state, center = spkpvn( <handle>, <descr>, <et>)  #  Position, velocity, native frame

:py:meth:`~spiceypy.spiceypy.spkpvn` is the most basic SPK reader.
It returns states relative to the frame in which they are stored in
the SPK file. It does not rotate or combine them: it returns a state
relative to the center whose integer code is stored in the descriptor
for the segment. This state is relative to the frame whose integer ID
code is also stored in the descriptor of the segment. The user is
responsible for using that state correctly.
The user is also responsible for using DAF functions to determine the
particular file and segment from which each state is to be computed.

Note that to use the state returned by
:py:meth:`~spiceypy.spiceypy.spkpvn` in any frame other than the
`native frame` of the segment, you must convert the state to the
frame of interest.

If files have been loaded by previous calls to
:py:meth:`~spiceypy.spiceypy.furnsh`, it is possible to use the
same segments that would normally be used by
:py:meth:`~spiceypy.spiceypy.spkezr`,
:py:meth:`~spiceypy.spiceypy.spkez`, spkssb_c, and
:py:meth:`~spiceypy.spiceypy.spkgeo`. Function
:py:meth:`~spiceypy.spiceypy.spksfs` selects, from the database of
loaded files, the file handle and segment descriptor for the segment
best suited to the request. If two segments from different files are
suitable, :py:meth:`~spiceypy.spiceypy.spksfs` selects the one from
the file that was loaded later. If two segments from the same file
are suitable, :py:meth:`~spiceypy.spiceypy.spksfs` selects the one
that is stored later in the file. The call


.. code-block:: python

      handle, descr, segnam = spksfs( <801>, <et>, idlen) #  Select file and segment

returns the handle, descriptor, and segment name for the latest
segment containing data for Triton at the specified epoch.
:py:meth:`~spiceypy.spiceypy.spksfs` maintains a buffer of segment
descriptors and segment names, so it doesn't waste time searching the
database for bodies it already knows about.


Examples of Using SPK Readers
================================


Example 1: Computing Latitude and Longitude
------------------------------------------------------------------------------------------------------------

| The next several sections present sample programs to show how the
  SPK readers can be used to compute state vectors, and how those
  vectors can be used to compute derived quantities.

All functions used in the examples are from CSPICE. The convention of
expanding SPK function names will be dropped for these examples.

The first example program computes the planetocentric latitude and
longitude of the sub-observer point on a target body for any
combination of observer, target, and epoch. (Note that planetocentric
coordinates differ from planetographic and cartographic coordinates
in that they are always right-handed, regardless of the rotation of
the body. Also note that for this example we define the sub-observer
point to be the point on the `surface` of the target that lies on
the ray from the center of the target to the observer. )


.. code-block:: python
  :linenos:

  #!/usr/bin/env python3
  """
  PROGRAM LATLON
  """

  # Standard includes
  import spiceypy as spice
  import numpy as np

  def main():
      # Load constants into the kernel pool. Two files are
      # needed. The first ("leapseconds.ker") contains the dates
      # of leap seconds and values for constants needed to
      # compute the difference between UTC and ET at any
      # epoch. The second ("pck.ker") contains IAU values
      # needed to compute transformations from inertial
      # (J2000) coordinates to body-fixed (pole and prime
      # meridian) coordinates for the major bodies of the
      # solar system.
      spice.furnsh("leapseconds.ker")
      spice.furnsh("pck.ker")

      # Several ephemeris files are used. Most contain data for
      # a single planetary system ("jupiter.bsp", "saturn.bsp",
      # and so on). Some contain data for spacecraft ("vgr1.bsp",
      # "mgn.bsp").
      spice.furnsh("mercury.bsp")
      spice.furnsh("venus.bsp")
      spice.furnsh("earth.bsp")
      spice.furnsh("mars.bsp")
      spice.furnsh("jupiter.bsp")
      spice.furnsh("saturn.bsp")
      spice.furnsh("uranus.bsp")
      spice.furnsh("neptune.bsp")
      spice.furnsh("pluto.bsp")
      spice.furnsh("vgr1.bsp")
      spice.furnsh("vgr2.bsp")
      spice.furnsh("mgn.bsp")
      spice.furnsh("gll.bsp")

      # Inputs are entered interactively. The user enters three
      # items: the name for the observer, the name
      # for the target, and the UTC epoch at which the
      # sub-observer point is to be computed (a free-format string).
      #
      # The epoch must be converted to ephemeris time (ET).
      while True:
          obs = input("Observer? ")
          targ = input("Target? ")
          time_str = input("Epoch? ")

          et = spice.str2et(time_str)
          frame = "IAU_" + targ

          # Compute the true state (corrected for light-time)
          # of the target as seen from the observer at the
          # specified epoch in the target fixed reference frame.
          state, lt = spice.spkezr(targ, et, frame, "LT", obs)

          # We need the vector FROM the target TO the observer
          # to compute latitude and longitude. So negate it.
          state = -np.array(state)

          # Convert from rectangular coordinates to latitude and
          # longitude, then from radians to degrees for output.
          # Note: reclat expects a 3-element vector (position only).
          radius, lon, lat = spice.reclat(state)
          lat_deg = np.degrees(lat)
          lon_deg = np.degrees(lon)

          print("\n"
                "Sub-observer latitude (deg): {}\n"
                "             longitude     : {}\n"
                "\n"
                "Range to target (km)       : {}\n"
                "Light-time (sec)           : {}\n".format(lat_deg, lon_deg, radius, lt))

          # Get the next set of inputs.

  if __name__ == "__main__":
      main()


Example 2: Occultation or Transit
------------------------------------------------------------------------------------------------------------

| The second example determines epochs if one target body
  (spacecraft, planet, or satellite) is occulted by or in transit
  across another target body as seen from an observer at a user
  specified epoch. It is similar in both form and generality to the
  first example.


.. code-block:: python
  :linenos:

  #!/usr/bin/env python3
  """
  PROGRAM OCCTRN
  """

  # Standard includes
  import spiceypy as spice
  import numpy as np
  import math

  # CSPICE prototypes and definitions.

  def main():
      """
      Constants
      """
      NTARG   = 2

      # Load constants into the kernel pool. Two files are
      # needed. The first ("leapseconds.ker") contains the dates
      # of leap seconds and values for constants needed to
      # compute the difference between UTC and ET at any
      # epoch. The second ("radii.tpc") contains values
      # for the tri-axial ellipsoids used to model the major
      # major bodies of the solar system.
      spice.furnsh("leapseconds.ker")
      spice.furnsh("radii.tpc")

      # Several ephemeris files are needed. Most contain data for
      # a single planetary system ("jupiter.ker", "saturn.ker",
      # and so on). Some contain data for spacecraft ("vgr1.ker",
      # "mgn.ker").
      spice.furnsh("mercury.bsp")
      spice.furnsh("venus.bsp")
      spice.furnsh("earth.bsp")
      spice.furnsh("mars.bsp")
      spice.furnsh("jupiter.bsp")
      spice.furnsh("saturn.bsp")
      spice.furnsh("uranus.bsp")
      spice.furnsh("neptune.bsp")
      spice.furnsh("pluto.bsp")
      spice.furnsh("vgr1.bsp")
      spice.furnsh("vgr2.bsp")
      spice.furnsh("mgn.bsp")
      spice.furnsh("gll.bsp")

      # Inputs are entered interactively. The user enters four
      # items: the code for the observer (an integer), the codes
      # for two target bodies (integers), and the epoch at which
      # check for occultation or transit is to be computed
      # (a free-format string).
      #
      # The epoch must be converted to ephemeris time (ET).
      while True:
          obs = input("Observer? ")
          targ = [None] * NTARG
          targ[0] = input("Target 1? ")
          targ[1] = input("Target 2? ")
          time_str = input("Epoch?    ")

          et = spice.str2et(time_str)

          # Get the ID codes associated with the targets
          # In spiceypy, bodn2c returns the NAIF ID code for a given name.
          try:
              t_ids = [spice.bodn2c(targ[0]), spice.bodn2c(targ[1])]
          except Exception as e:
              print("Error converting body name to ID:", e)
              continue

          d = [0.0, 0.0]
          r = [0.0, 0.0]
          s = [None, None]  # state vectors

          # Get the apparent states of the target objects as seen from
          # the observer. Also get the apparent radius of each object
          # from the kernel pool. (Use zero radius for any spacecraft;
          # use average radius for anything else.)
          #
          # targ[i]          is the ID code of the i'th target, i = 0, 1.
          # state[i][0..5]   is the apparent state of the i'th target.
          #
          # d[i]         is the apparent distance to the i'th target.
          #
          # r[i]         is the apparent radius of the i'th target.
          #
          # Function vnorm_c returns the Euclidean norm (magnitude) of
          # a three-vector.
          #
          # Function sumad_c returns the sum of the elements in a
          # double precision array.
          for i in range(NTARG):
              state, lt = spice.spkezr(targ[i], et, "J2000", "LT+S", obs)
              s[i] = state
              d[i] = np.linalg.norm(state[:3])
              if t_ids[i] < 0:
                  r[i] = 0.0
              else:
                  radii, dim = spice.bodvcd(t_ids[i], "RADII", 3)
                  avg = np.sum(radii) / 3.0
                  # Use arcsin to compute the apparent radius
                  ratio = avg / d[i]
                  # Clamp ratio to valid domain for arcsin
                  ratio = max(min(ratio, 1.0), -1.0)
                  r[i] = np.arcsin(ratio)

          # Determine the separation between the two bodies. If the
          # separation between the centers is greater than the sum of
          # the apparent radii, then the target bodies are clear of
          # each other.
          #
          # Function vsep_c returns the angle of separation between
          # two three-vectors.
          sep = spice.vsep(s[0][:3], s[1][:3]) - (r[0] + r[1])

          if sep > 0.0:
              print("\nClear.\n")
          else:
              #
              # Otherwise, the smaller body is either occulted or
              # in transit.  We compare ranges to decide which.
              #
              # Let index j indicate the target of smaller radius; let k
              # indicate the larger target.
              j = 0 if r[0] < r[1] else 1
              k = 1 - j

              if d[j] < d[k]:
                  print(f"\n{targ[j]} is in transit across {targ[k]}\n")
              else:
                  print(f"\n{targ[j]} is occulted by {targ[k]}\n")

          # Get the next set of inputs.

  if __name__ == "__main__":
      main()




Additional, working examples of using the principal SPK functions may
be found in the `Cookbook` programs distributed with the SPICE
Toolkit.


Supported Data Types
=======================


| The following representations, or data types, are currently
  supported by the SPK functions in CSPICE.

#. Modified Difference Arrays.

- Created by the JPL Orbit Determination Program (ODP), these
  are used primarily for spacecraft ephemerides.

#. Chebyshev polynomials (position only).

- These are sets of coefficients for the x, y, and z components
  of the body position. The velocity of the body is obtained by
  differentiation. This data type is normally used for planet
  barycenters, and for satellites whose orbits are integrated.

#. Chebyshev polynomials (position and velocity).

- These are sets of coefficients for the x, y, and z components
  of the body position, and for the corresponding components of the
  velocity. This data type is normally used for satellites whose
  orbits are computed directly from theories.

#. Reserved for future use (TRW elements for TDRS and Space Telescope).

#. Discrete states (two body propagation).

- This data type contains discrete state vectors. A state is
  obtained for a specified epoch by propagating the state vectors to
  that epoch according to the laws of two body motion and then taking
  a weighted average of the resulting states. Normally, this data
  type is used for comets and asteroids, whose ephemerides are
  integrated from an initial state or set of osculating elements.

#. Reserved for future use (Analytic Model for Phobos and Deimos).

#. Reserved for future use (Precessing Classical Elements---used by STScI).

#. Equally spaced discrete states (Lagrange interpolation)

- This data type contains discrete state vectors whose time tags
  are separated by a constant step size. A state is obtained for a
  specified epoch by finding a set of states `centered` at that
  epoch and using Lagrange interpolation on each component of the
  states.

#. Unequally spaced discrete states (Lagrange interpolation)

- This data type contains discrete state vectors whose time tags
  may be unequally spaced. A state is obtained for a specified epoch
  by finding a set of states `centered` at that epoch and using
  Lagrange interpolation on each component of the states.

#. Space Command Two-line Elements

- This data type contains Space Command two-line element
  representations for objects in Earth orbit (formally called NORAD
  two-line elements).

#. Reserved for future use.

#. Hermite Interpolation Uniform Spacing.

#. Hermite Interpolation Non-uniform Spacing.

#. Chebyshev polynomials non-uniform spacing (position and velocity).

- This data type contains Chebyshev polynomial coefficients for
  the position and velocity of an object. Unlike SPK Types 2 and 3,
  the time intervals to which polynomial coefficient sets apply do
  not have uniform duration.

#. Precessing conic propagation.

- This data type allows for first order precession of the line
  of apsides and regression of the line of nodes due to the effects
  of the J2 coefficient in the harmonic expansion of the
  gravitational potential of an oblate spheroid.

#. Reserved for future use (Elements for European Space Agency's ISO spacecraft).

#. Equinoctial Elements

- This data type represents the motion of an object about
  another using equinoctial elements. It provides for precession of
  the line of apsides and regression of the line of nodes. Unlike
  Type 15, the mean motion, regression of the nodes and precession of
  the line of apsides are not derived from the gravitational
  properties of the central body, but are empirical values.

#. ESOC/DDID Hermite/Lagrange Interpolation

- This data type has been provided to support accurate
  duplication within the SPK system of spacecraft ephemerides used by
  the European Space Agency (ESA) on the Mars Express, Rosetta,
  SMART-1, and Venus express missions.

#. ESOC/DDID Piecewise Interpolation

- SPK type 19 is an enhanced version of SPK type 18. Type 19
  enables creation of SPK files representing the same ephemerides
  that can be represented using type 18, but containing far fewer
  segments. Data from multiple type 18 segments can be stored in a
  single type 19 segment.

#. Chebyshev (velocity only)

- SPK data type 20 contains Chebyshev polynomial coefficients
  for the velocity of a body, relative to its center of motion, as a
  function of time. The position of the body is obtained by
  integrating the velocity using a specified integration constant.
  This data type is provided to accurately represent `EPM`
  ephemerides developed by the Institute of Applied Astronomy (IAA),
  Russian Academy of Sciences (RAS).

#. Extended Modified Difference Arrays

- SPK data type 21 contains extended Modified Difference Arrays
  (MDA), also called `difference lines.` These data structures use
  the same mathematical trajectory representation as SPK data type 1,
  but type 21 allows use of larger, higher-degree MDAs.

Because SPK files are Double Precision Array Files (DAFs), each
segment is stored as an array. Each array corresponding to a
particular data type has a particular internal structure. These
structures (for the non-reserved types) are described below.


Type 1: Modified Difference Arrays
------------------------------------------------------------------------------------------------------------

| The first SPK data type contains Modified Difference Arrays (MDA),
  sometimes called `difference lines`. This data type is normally
  used for spacecraft whose ephemerides are produced by JPL's
  principal trajectory integrator---DPTRAJ. Difference lines are
  extracted from the spacecraft trajectory file (`P-files` and
  `PV-files`) created by DPTRAJ.

Each segment containing Modified Difference Arrays contains an
arbitrary number of logical records. Each record contains difference
line coefficients valid up to some final epoch, along with the state
at that epoch. The contents of the records themselves are described
in [163]. The function spke01\_ contains the algorithm used to
construct a state from a particular record and epoch.

The records within a segment are ordered by increasing final epoch.
The final epochs associated with the records must be distinct.

A segment of this type is structured as follows:

.. code-block:: text

      +-----------------------------------------+
      | Record 1 (difference line coefficients) |
      +-----------------------------------------+
      | Record 2 (difference line coefficients) |
      +-----------------------------------------+
        .
        .
        .
      +-----------------------------------------+
      | Record N (difference line coefficients) |
      +-----------------------------------------+
      | Epoch 1                      |
      +------------------------------+
      | Epoch 2                      |
      +------------------------------+
        .
        .
        .
      +------------------------------+
      | Epoch N                      |
      +------------------------------+
      | Epoch 100                    |   (First directory epoch)
      +------------------------------+
      | Epoch 200                    |   (Second directory epoch)
      +------------------------------+
        .
        .
        .
      +------------------------------+
      | Epoch (N/100)*100            |   (Final directory epoch)
      +------------------------------+
      | N                            |
      +------------------------------+

The number of records in a segment, N, can be arbitrarily large.
Records 1 through N contain the difference line coefficients and
other constants needed to compute state data. Each one of these
records contains 71 double precision numbers.

The list of final epochs for the records is stored immediately after
the last record.

Following the list of epochs is a second list, the `directory`,
containing every 100th epoch from the previous list. If there are N
epochs, there will be N/100 directory epochs. If there are fewer than
100 epochs, then the segment will not contain any directory epochs.
Directory epochs are used to speed up access to desired records.

The final element in the segment is the number of records contained
in the segment, N.

The index of the record corresponding to a particular epoch is the
index of the first epoch not less than the target epoch.

Type 2: Chebyshev (position only)
------------------------------------------------------------------------------------------------------------

| The second SPK data type contains Chebyshev polynomial coefficients
  for the position of the body as a function of time. Normally, this
  data type is used for planet barycenters, and for satellites whose
  ephemerides are integrated. (The velocity of the body is obtained
  by differentiating the position.)

Each segment contains an arbitrary number of logical records. Each
record contains a set of Chebyshev coefficients valid throughout an
interval of fixed length. The function spke02\_ contains the
algorithm used to construct a state from a particular record and
epoch.

The records within a segment are ordered by increasing initial epoch.
All records contain the same number of coefficients. A segment of
this type is structured as follows:

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

A four-number `directory` at the end of the segment contains the
information needed to determine the location of the record
corresponding to a particular epoch.

#. INIT is the initial epoch of the first record, given in ephemeris seconds past J2000.

#. INTLEN is the length of the interval covered by each record, in seconds.

#. RSIZE is the total size of (number of array elements in) each record.

#. N is the number of records contained in the segment.

Each record is structured as follows:

.. code-block:: text

      +------------------+
      | MID              |
      +------------------+
      | RADIUS           |
      +------------------+
      | X  coefficients  |
      +------------------+
      | Y  coefficients  |
      +------------------+
      | Z  coefficients  |
      +------------------+

The first two elements in the record, MID and RADIUS, are the
midpoint and radius of the time interval covered by coefficients in
the record. These are used as parameters to perform transformations
between the domain of the record (from MID - RADIUS to MID + RADIUS)
and the domain of Chebyshev polynomials (from -1 to 1 ).
The same number of coefficients is always used for each component,
and all records are the same size (RSIZE), so the degree of each
polynomial is

.. code-block:: text

      ( RSIZE - 2 ) / 3 - 1

To facilitate the creation of Type 2 segments, a segment writing
function called :py:meth:`~spiceypy.spiceypy.spkw02` has been
provided. This function takes as input arguments the handle of an SPK
file that is open for writing, the information needed to construct
the segment descriptor, and the data to be stored in the segment. The
header of the function provides a complete description of the input
arguments and an example of its usage.


Type 3: Chebyshev (position and velocity)
------------------------------------------------------------------------------------------------------------

| The third SPK data type contains Chebyshev polynomial coefficients
  for the position and velocity of the body as a function of time.
  Normally, this data type is used for satellites for which the
  ephemerides are computed from analytical theories.

The structure of the segment is nearly identical to that of the SPK
data Type 2 (Chebyshev polynomials for position only). The only
difference is that each logical record contains six sets of
coefficients instead of three. The function spke03\_ contains the
algorithm used to construct a state from a particular record and
epoch.

Each record is structured as follows:

.. code-block:: text

      +------------------+
      | MID              |
      +------------------+
      | RADIUS           |
      +------------------+
      | X  coefficients  |
      +------------------+
      | Y  coefficients  |
      +------------------+
      | Z  coefficients  |
      +------------------+
      | X' coefficients  |
      +------------------+
      | Y' coefficients  |
      +------------------+
      | Z' coefficients  |
      +------------------+

The same number of coefficients is always used for each component,
and all records are the same size (RSIZE), so the degree of each
polynomial is

.. code-block:: text

      ( RSIZE - 2 ) / 6 - 1

To facilitate the creation of Type 3 segments, a segment writing
function called :py:meth:`~spiceypy.spiceypy.spkw03` has been
provided. This function takes as input arguments the handle of an SPK
file that is open for writing, the information needed to construct
the segment descriptor, and the data to be stored in the segment. The
header of the function provides a complete description of the input
arguments and an example of its usage.


Type 5: Discrete states (two body propagation)
------------------------------------------------------------------------------------------------------------

| The fifth standard SPK data type contains discrete state vectors. A
  state is obtained from a Type 5 segment for any epoch that is
  within the bounds of that segment by propagating the discrete
  states to the specified epoch according to the laws of two body
  motion. Normally, this data type is used for comets and asteroids,
  whose ephemerides are integrated from an initial state or set of
  osculating elements.

Each segment contains of a number of logical records. Each record
consists of an epoch (ephemeris seconds past J2000) and the geometric
state of the body at that epoch (x, y, z, dx/dt, dy/dt, dz/dt, in
kilometers and kilometers per second). Records are ordered with
respect to increasing time.

The records that correspond to an epoch for which a state is desired
are the ones whose associated epochs bracket that epoch. The state in
each record is used as the initial state in a two-body propagation; a
weighted average of the propagated states gives the position of the
body at the specified epoch. The velocity is given by the derivative
of the position. Thus the position and velocity at the specified
epoch are given by:

.. code-block:: text

      P  = W(t) * P1(t) + (1-W(t)) * P2(t)


     V  = W(t) * V1(t) + (1-W(t)) * V2(t) + W'(t) * ( P1(t) - P2(t) )

where P1, V1, P2, and V2 are the position and velocity components of
the propagated states and W is the weighting function.
The weighting function used is:

.. code-block:: text

      W(t) = 0.5 + 0.5 * cos [ PI * ( t - t1 ) / ( t2 - t1 ) ]

where t1 and t2 are the epochs that bracket the specified epoch t.
Physically, the epochs and states are stored separately, so that the
epochs can be searched as an ordered array. Thus, the initial part of
each segment looks like this:

.. code-block:: text

      +--------------------+
      | State 1            |
      +--------------------+
               .
               .
               .
      +--------------------+
      | State N            |
      +--------------------+
      | Epoch 1            |
      +--------------------+
               .
               .
               .
      +--------------------+
      | Epoch N            |
      +--------------------+

The number of records in a segment can be arbitrarily large. In order
to avoid the file reads required to search through a large array of
epochs, each segment contains a simple directory immediately after
the final epoch.
This directory contains every 100th epoch in the epoch array. If
there are N epochs, there will be N/100 directory epochs. (If there
are fewer than 100 epochs, no directory epochs are stored.)

The final items in the segment are GM, the gravitational parameter of
the central body (kilometers and seconds), and N, the number of
states in the segment. Thus, the complete segment looks like this:

.. code-block:: text

      +--------------------+
      | State 1            |
      +--------------------+
               .
               .
               .
      +--------------------+
      | Epoch 1            |
      +--------------------+
               .
               .
               .
      +--------------------+
      | Epoch N            |
      +--------------------+
      | Epoch 100          |           (First directory epoch)
      +--------------------+
      | Epoch 200          |
      +--------------------+
               .
               .
               .
      +--------------------+
      | Epoch (N/100)*100  |           (Final directory epoch)
      +--------------------+
      | GM                 |
      +--------------------+
      | N                  |
      +--------------------+

To facilitate the creation of Type 5 segments, a segment writing
function called :py:meth:`~spiceypy.spiceypy.spkw05` has been
provided. This function takes as input arguments the handle of an SPK
file that is open for writing, the information needed to construct
the segment descriptor, and the data to be stored in the segment. The
header of the function provides a complete description of the input
arguments and an example of its usage.


Type 8: Lagrange Interpolation --- Equal Time Steps
------------------------------------------------------------------------------------------------------------

| The eighth SPK data type represents a continuous ephemeris using a
  discrete set of states and a Lagrange interpolation method. The
  epochs (also called `time tags`) associated with the states must
  be evenly spaced: there must be some positive constant STEP such
  that each time tag differs from its predecessor and successor by
  STEP seconds. For a request epoch not corresponding to the time tag
  of some state, the data type defines a state by interpolating each
  component of a set of states whose epochs are `centered` near the
  request epoch. Details of how these states are selected and
  interpolated are given below.

The SPK system can also represent an ephemeris using unequally spaced
discrete states and Lagrange interpolation; SPK Type 9 does this. SPK
Type 9 sacrifices some run-time speed and economy of storage in order
to achieve greater flexibility.

The states in a Type 8 segment are geometric: they do not take into
account aberration corrections. The six components of each state
vector represent the position and velocity (x, y, z, dx/dt, dy/dt,
dz/dt, in kilometers and kilometers per second) of the body to which
the ephemeris applies, relative to the center specified by the
segment's descriptor. The epochs corresponding to the states are
barycentric dynamical times (TDB), expressed as seconds past J2000.

Each segment also has a polynomial degree associated with it; this is
the degree of the interpolating polynomials to be used in evaluating
states based on the data in the segment. The identical degree is used
for interpolation of each state component.

Type 8 SPK segments have the structure shown below:

.. code-block:: text

                                          +--------+
                                          |  x(1)  |
                                      /   +--------+
                                     /    |  y(1)  |
                                    /     +--------+
                                   /      |  z(1)  |
      +-----------------------+   /       +--------+
      | State 1               |  <        |dx(1)/dt|
      +-----------------------+   \       +--------+
      | State 2               |    \      |dy(1)/dt|
      +-----------------------+     \     +--------+
                  .                  \    |dz(1)/dt|
                  .                       +--------+
                  .
      +-----------------------+
      | State N               |
      +-----------------------+
      | Epoch of state 1 (TDB)|
      +-----------------------+
      | Step size             |
      +-----------------------+
      | Polynomial degree     |
      +-----------------------+
      | Number of states      |
      +-----------------------+

In the diagram, each box representing a state vector corresponds to
six double precision numbers; the other boxes represent individual
double precision numbers. Since the epochs of the states are evenly
spaced, they are represented by a start epoch and a step size. The
number of states must be greater than the interpolating polynomial
degree.
The Type 8 interpolation method works as follows: given an epoch at
which a state is requested and a segment having coverage for that
epoch, the Type 8 reader finds a group of states whose epochs are
`centered` about the epoch. The size of the group is one greater
than the polynomial degree associated with the segment. If the group
size N is even, then the group will consist of N consecutive states
such that the request time is between the epochs of the members of
the group having indices, relative to the start of the group, of N/2
and (N/2 + 1), inclusive. When N is odd, the group will contain a
central state whose epoch is closest to the request time, and will
also contain (N-1)/2 neighboring states on either side of the central
one. The Type 8 evaluator will then use Lagrange interpolation on
each component of the states to produce a state corresponding to the
request time. For the jth state component, the interpolation
algorithm is mathematically equivalent to finding the unique
polynomial of degree N-1 that interpolates the ordered pairs

.. code-block:: text

      ( epoch(i), state(j,i) ),  i = k ,  k , ... , k
                                      1    2         N

and evaluating the polynomial at the requested epoch. Here

.. code-block:: text

       k ,  k , ... , k
        1    2         N

are the indices of the states in the interpolation group,

.. code-block:: text

      epoch(i)

is the epoch of the ith state and

.. code-block:: text

      state(j,i)

is the jth component of the ith state.
There is an exception to the state selection algorithm described
above: the request time may be too near the first or last state of
the segment to be properly bracketed. In this case, the set of states
selected for interpolation still has size N, and includes either the
first or last state of the segment.

To facilitate the creation of Type 8 segments, a segment writing
function called :py:meth:`~spiceypy.spiceypy.spkw08` has been
provided. This function takes as input arguments the handle of an SPK
file that is open for writing, the information needed to construct
the segment descriptor, and the data to be stored in the segment. The
header of the function provides a complete description of the input
arguments and an example of its usage.

Type 9: Lagrange Interpolation --- Unequal Time Steps
------------------------------------------------------------------------------------------------------------

| The ninth SPK data type represents a continuous ephemeris using a
  discrete set of states and a Lagrange interpolation method. The
  epochs (also called `time tags` ) associated with the states need
  not be evenly spaced. For a request epoch not corresponding to the
  time tag of some state, the data type defines a state by
  interpolating each component of a set of states whose epochs are
  `centered` near the request epoch. Details of how these states are
  selected and interpolated are given below.

The states in a Type 9 segment are geometric: they do not take into
account aberration corrections. The six components of each state
vector represent the position and velocity (x, y, z, dx/dt, dy/dt,
dz/dt, in kilometers and kilometers per second) of the body to which
the ephemeris applies, relative to the center specified by the
segment's descriptor. The epochs corresponding to the states are
barycentric dynamical times (TDB), expressed as seconds past J2000.

Each segment also has a polynomial degree associated with it; this is
the degree of the interpolating polynomials to be used in evaluating
states based on the data in the segment. The identical degree is used
for interpolation of each state component.

Type 9 SPK segments have the structure shown below:

.. code-block:: text

                                          +--------+
                                          |  x(1)  |
                                      /   +--------+
                                     /    |  y(1)  |
                                    /     +--------+
                                   /      |  z(1)  |
      +-----------------------+   /       +--------+
      | State 1               |  <        |dx(1)/dt|
      +-----------------------+   \       +--------+
      | State 2               |    \      |dy(1)/dt|
      +-----------------------+     \     +--------+
                  .                  \    |dz(1)/dt|
                  .                       +--------+
                  .
      +-----------------------+
      | State N               |
      +-----------------------+
      | Epoch 1               |
      +-----------------------+
      | Epoch 2               |
      +-----------------------+
                  .
                  .
                  .
      +-----------------------+
      | Epoch N               |
      +-----------------------+
      | Epoch 100             | (First directory)
      +-----------------------+
                  .
                  .
                  .
      +-----------------------+
      | Epoch ((N-1)/100)*100 | (Last directory)
      +-----------------------+
      | Polynomial degree     |
      +-----------------------+
      | Number of states      |
      +-----------------------+


In the diagram, each box representing a state vector corresponds to
six double precision numbers; the other boxes represent individual
double precision numbers. The number of states must be greater than
the interpolating polynomial degree.
The set of time tags is augmented by a series of directory entries;
these entries allow the Type 9 reader to search for states more
efficiently. The directory entries contain time tags whose indices
are multiples of 100. The set of indices of time tags stored in the
directories ranges from 100 to

.. code-block:: text

      (  (N-1) / 100  ) * 100

where N is the total number of time tags. Note that if N is

.. code-block:: text

      Q * 100

then only

.. code-block:: text

      Q - 1

directory entries are stored, and in particular, if there are only
100 states in the segment, there are no directories.
The Type 9 interpolation algorithm is virtually identical to the Type
8 algorithm; see the discussion of SPK Type 8 for details. However,
the Type 9 algorithm executes more slowly than the Type 8 algorithm,
since the Type 9 reader must search through tables of time tags to
find appropriates states to interpolate, while the Type 8 reader can
locate the correct set of states to interpolate by a direct
computation.

To facilitate the creation of Type 9 segments, a segment writing
function called :py:meth:`~spiceypy.spiceypy.spkw09` has been
provided. This function takes as input arguments the handle of an SPK
file that is open for writing, the information needed to construct
the segment descriptor, and the data to be stored in the segment. The
header of the function provides a complete description of the input
arguments and an example of its usage.

Type 10: Space Command Two-Line Elements
------------------------------------------------------------------------------------------------------------

| The SPK data Type 10 uses the SPICE concept of a generic segment to
  store a collection of packets each of which models the trajectory
  of some Earth satellite using Space Command two-line element sets
  (TLEs) (formerly the North American Air Defense --- NORAD). TLE
  propagation occurs using the algorithms as described in the
  Spacetrak 3 report for SGP4 and SDP4. Note: The Spacetrak 3
  implementation of SDP4 contained several programming errors. The
  errors were corrected for CSPICE implementation.

The SPICE generic segment software handles storage, arrangement, and
retrieval of the TLEs. We review only the pertinent points about
generic segments here.

A generic SPK segment contains several logical data partitions:

#. A partition for constant values to be associated with each data packet in the segment.

#. A partition for the data packets.

#. A partition for epochs.

#. A partition for a packet directory, if the segment contains variable sized packets.

#. A partition for an epoch directory.

#. A reserved partition that is not currently used. This
   partition is only for the use of the NAIF group at the Jet
   Propulsion Laboratory (JPL).

#. A partition for the meta data which describes the locations
   and sizes of other partitions as well as providing some additional
   descriptive information about the generic segment.

.. code-block:: text

         +============================+
         |         Constants          |
         +============================+
         |          Packet 1          |
         |----------------------------|
         |          Packet 2          |
         |----------------------------|
         |              .             |
         |              .             |
         |              .             |
         |----------------------------|
         |          Packet N          |
         +============================+
         |      Reference Epochs      |
         +============================+
         |      Packet Directory      |
         +============================+
         |       Epoch Directory      |
         +============================+
         |       Reserved  Area       |
         +============================+
         |     Segment Meta Data      |
         +----------------------------+

Each `packet` of a Type 10 segment contains a set of two-line
elements, the nutations in longitude and obliquity of the Earth's
pole, and the rates of these nutations. Each packet is arranged as
shown below. (The notation below is taken from the description that
accompanies the code available from Space Command for the evaluation
of two-line elements.)

.. code-block:: text


         A single SPK Type 10 segment packet

         +-------------------+
       1 |      NDT20        |
         +-------------------+
       2 |      NDD60        |
         +-------------------+
       3 |      BSTAR        |
         +-------------------+
       4 |      INCL         |
         +-------------------+
       5 |      NODE0        |     Two-line element packet
         +-------------------+
       6 |      ECC          |
         +-------------------+
       7 |      OMEGA        |
         +-------------------+
       8 |      MO           |
         +-------------------+
       9 |      NO           |
         +-------------------+
      10 |      EPOCH        |
         +-------------------+
      11 |      NU.OBLIQUITY |
         +-------------------+
      12 |      NU.LONGITUDE |
         +-------------------+
      13 |     dOBLIQUITY/dt |
         +-------------------+
      14 |     dLONGITUDE/dt |
         +-------------------+

The constants partition of the Type 10 segment contains the following
eight geophysical constants.

.. code-block:: text

         +-------------------------------------------+
      1  |  J2 gravitational harmonic for Earth      |
         +-------------------------------------------+
      2  |  J3 gravitational harmonic for Earth      |
         +-------------------------------------------+
      3  |  J4 gravitational harmonic for Earth      |
         +-------------------------------------------+
         |  Square root of the GM for Earth where GM |
      4  |  is expressed in Earth radii cubed per    |
         |  minutes squared                          |
         +-------------------------------------------+
      5  |  High altitude bound for atmospheric      |
         |  model in km                              |
         +-------------------------------------------+
      6  |  Low altitude bound for atmospheric       |
         |  model in km                              |
         +-------------------------------------------+
      7  |  Equatorial radius of the Earth in km     |
         +-------------------------------------------+
      8  |  Distance units/Earth radius (normally 1) |
         +-------------------------------------------+

The reference epochs partition contains an ordered collection of
epochs. The i'th reference epoch is equal to the epoch in the i'th
packet.
The `epoch directory` contains every 100th reference epoch. The
epoch directory is used to efficiently locate an the reference epoch
that should be associated with a two line element packet.

The `packet directory` is empty.

Access to the data should be made via the SPK Type 10
reader---spkr10\_ or via the SPICELIB generic segment functions. Use
the function :py:meth:`~spiceypy.spiceypy.spkw10` to write a Type
10 generic segment.

Type 12: Hermite Interpolation --- Equal Time Steps
------------------------------------------------------------------------------------------------------------

| The twelfth SPK data type represents a continuous ephemeris using a
  discrete set of states and a sliding window Hermite interpolation
  method. The epochs, also called "time tags," associated with the
  states must be evenly spaced: there must be some positive constant
  STEP such that each time tag differs from its predecessor by STEP
  seconds. For any request epoch, the data type defines a state by
  interpolating a set of consecutive states, or "window," centered as
  closely as possible to the request epoch. Interpolated position
  values are obtained for each coordinate by fitting a Hermite
  polynomial to the window's set of position and velocity values for
  that coordinate; interpolated velocity is obtained by
  differentiating the interpolating polynomials. Details of the
  interpolation method are given below.

The SPK system can also represent an ephemeris using unequally spaced
discrete states and Hermite interpolation; SPK type 13 does this. SPK
type 13 sacrifices some run-time speed and economy of storage in
order to achieve greater flexibility.

The states in a type 12 segment are geometric: they do not take into
account aberration corrections. The six components of each state
vector represent the position and velocity (x, y, z, dx/dt, dy/dt,
dz/dt, in kilometers and kilometers per second) of the body to which
the ephemeris applies, relative to the center specified by the
segment's descriptor. The epochs corresponding to the states are
barycentric dynamical times (TDB), expressed as seconds past J2000.

Each segment also has a polynomial degree associated with it; this is
the degree of the interpolating polynomials to be used in evaluating
states based on the data in the segment. The identical degree is used
for interpolation of each state component.

Type 12 SPK segments have the structure shown below:

.. code-block:: text

                                          +--------+
                                          |  x(1)  |
                                      /   +--------+
                                     /    |  y(1)  |
                                    /     +--------+
                                   /      |  z(1)  |
      +-----------------------+   /       +--------+
      | State 1               |  <        |dx(1)/dt|
      +-----------------------+   \       +--------+
      | State 2               |    \      |dy(1)/dt|
      +-----------------------+     \     +--------+
                  .                  \    |dz(1)/dt|
                  .                       +--------+
                  .
      +-----------------------+
      | State N               |
      +-----------------------+
      | Epoch of state 1 (TDB)|
      +-----------------------+
      | Step size             |
      +-----------------------+
      | Window size - 1       |
      +-----------------------+
      | Number of states      |
      +-----------------------+

In the diagram, each box representing a state vector corresponds to
six double precision numbers; the other boxes represent individual
double precision numbers. Since the epochs of the states are evenly
spaced, they are represented by a start epoch and a step size. The
number of states must be greater than or equal to the window size,
which is related to the polynomial degree as shown:

.. code-block:: text

      DEGREE  =  2 * WINDOW_SIZE  -  1

The type 12 interpolation method works as follows: given an epoch at
which a state is requested and a segment having coverage for that
epoch, the type 12 reader finds a window of states whose epochs are
"centered" about the epoch. If the window size S is even, then the
window will consist of S consecutive states such that the request
time is between the epochs of the members of the group having
indices, relative to the start of the group, of S/2 and (S/2 + 1),
inclusive. When S is odd, the group will contain a central state
whose epoch is closest to the request time, and will also contain
(S-1)/2 neighboring states on either side of the central one. For
each of the x-, y-, and z-coordinates, the type 12 evaluator will fit
an Hermite polynomial to the corresponding position and velocity
values of the states in the selected window. Each polynomial is
evaluated at the request time to yield the interpolated position
components. The derivatives of these polynomials are evaluated at the
request time to yield the interpolated velocity components.
For the jth coordinate, the interpolation algorithm is mathematically
equivalent to finding the unique polynomial of degree 2*S-1 that
interpolates the ordered pairs

.. code-block:: text

      ( epoch(i), position(j,i) ),  i = k ,  k , ... , k
                                         1    2         S

and whose derivative interpolates the ordered pairs

.. code-block:: text

      ( epoch(i), velocity(j,i) ),  i = k ,  k , ... , k
                                         1    2         S

and evaluating the polynomial and its derivative at the requested
epoch. Here

.. code-block:: text

       k ,  k , ... , k
        1    2         S

are the indices of the states in the interpolation window,

.. code-block:: text

      epoch(i)

is the epoch of the ith state and

.. code-block:: text

      position(j,i)
      velocity(j,i)

are, respectively, the jth components of the position and velocity
comprising the ith state.
There is an exception to the state selection algorithm described
above: the request time may be too near the first or last state of
the segment to be properly bracketed. In this case, the set of states
selected for interpolation still has size S, and includes either the
first or last state of the segment.

To facilitate the creation of type 12 segments, a segment writing
routine called :py:meth:`~spiceypy.spiceypy.spkw12` has been
provided. This routine takes as input arguments the handle of an SPK
file that is open for writing, the information needed to construct
the segment descriptor, and the data to be stored in the segment. The
header of the subroutine provides a complete description of the input
arguments and an example of its usage.

Type 13: Hermite Interpolation --- Unequal Time Steps
------------------------------------------------------------------------------------------------------------

| The thirteenth SPK data type represents a continuous ephemeris
  using a discrete set of states and a sliding window Hermite
  interpolation method. The epochs, also called "time tags,"
  associated with the states need not be evenly spaced. For any
  request epoch, the data type defines a state by interpolating a set
  of consecutive states, or "window," centered as closely as possible
  to the request epoch. Interpolated position values are obtained for
  each coordinate by fitting a Hermite polynomial to the window's set
  of position and velocity values for that coordinate; interpolated
  velocity is obtained by differentiating the interpolating
  polynomials. Details of the interpolation method are given below.

The states in a type 13 segment are geometric: they do not take into
account aberration corrections. The six components of each state
vector represent the position and velocity (x, y, z, dx/dt, dy/dt,
dz/dt, in kilometers and kilometers per second) of the body to which
the ephemeris applies, relative to the center specified by the
segment's descriptor. The epochs corresponding to the states are
barycentric dynamical times (TDB), expressed as seconds past J2000.

Each segment also has a polynomial degree associated with it; this is
the degree of the interpolating polynomials to be used in evaluating
states based on the data in the segment. The identical degree is used
for interpolation of each state component.

Type 13 SPK segments have the structure shown below:

.. code-block:: text

                                          +--------+
                                          |  x(1)  |
                                      /   +--------+
                                     /    |  y(1)  |
                                    /     +--------+
                                   /      |  z(1)  |
      +-----------------------+   /       +--------+
      | State 1               |  <        |dx(1)/dt|
      +-----------------------+   \       +--------+
      | State 2               |    \      |dy(1)/dt|
      +-----------------------+     \     +--------+
                  .                  \    |dz(1)/dt|
                  .                       +--------+
                  .
      +-----------------------+
      | State N               |
      +-----------------------+
      | Epoch 1               |
      +-----------------------+
      | Epoch 2               |
      +-----------------------+
                  .
                  .
                  .
      +-----------------------+
      | Epoch N               |
      +-----------------------+
      | Epoch 100             | (First directory)
      +-----------------------+
                  .
                  .
                  .
      +-----------------------+
      | Epoch ((N-1)/100)*100 | (Last directory)
      +-----------------------+
      | Window size - 1       |
      +-----------------------+
      | Number of states      |
      +-----------------------+


In the diagram, each box representing a state vector corresponds to
six double precision numbers; the other boxes represent individual
double precision numbers. The number of states must be greater than
or equal to the window size, which is related to the polynomial
degree as shown:

.. code-block:: text

      DEGREE  =  2 * WINDOW_SIZE  -  1

The set of time tags is augmented by a series of directory entries;
these entries allow the type 13 reader to search for states more
efficiently. The directory entries contain time tags whose indices
are multiples of 100. The set of indices of time tags stored in the
directories ranges from 100 to

.. code-block:: text

      (  (N-1) / 100  ) * 100

where N is the total number of time tags. Note that if N is

.. code-block:: text

      Q * 100

then only

.. code-block:: text

      Q - 1

directory entries are stored, and in particular, if there are only
100 states in the segment, there are no directories.
The type 13 interpolation algorithm is virtually identical to the
type 12 algorithm; see the discussion of SPK type 12 for details.
However, the type 13 algorithm executes more slowly than the type 12
algorithm, since the type 13 reader must search through tables of
time tags to find appropriates states to interpolate, while the type
12 reader can locate the correct set of states to interpolate by a
direct computation.

To facilitate the creation of type 13 segments, a segment writing
routine called :py:meth:`~spiceypy.spiceypy.spkw13` has been
provided. This routine takes as input arguments the handle of an SPK
file that is open for writing, the information needed to construct
the segment descriptor, and the data to be stored in the segment. The
header of the subroutine provides a complete description of the input
arguments and an example of its usage.

Type 14: Chebyshev Polynomials --- Unequal Time Steps
------------------------------------------------------------------------------------------------------------

| The SPK data Type 14 uses the SPICE concept of a generic segment to
  store a collection of packets each of which models the trajectory
  of some object with respect to another over some interval of time.
  Each packet contains a set of coefficients for Chebyshev
  polynomials that approximate the position and velocity of some
  object. The time intervals corresponding to each packet are
  non-overlapping. Moreover their union covers the interval of time
  spanned by the start and end times of the Type 14 segment. Unlike
  Types 2 and 3 the time spacing between sets of coefficients for a
  Type 14 segment may be non-uniform.

The storage, arrangement and retrieval of packets is handled by the
SPICE generic segment software.
We only review the pertinent points about generic segments here.

A generic SPK segment contains several logical data partitions:

#. A partition for constant values to be associated with each
   data packet in the segment.

#. A partition for the data packets.

#. A partition for epochs.

#. A partition for a packet directory, if the segment contains
   variable sized packets.

#. A partition for an epoch directory.

#. A reserved partition that is not currently used. This
   partition is only for the use of the NAIF group at the Jet
   Propulsion Laboratory (JPL).

#. A partition for the meta data which describes the locations
   and sizes of other partitions as well as providing some additional
   descriptive information about the generic segment.

.. code-block:: text

         +============================+
         |         Constants          |
         +============================+
         |          Packet 1          |
         |----------------------------|
         |          Packet 2          |
         |----------------------------|
         |              .             |
         |              .             |
         |              .             |
         |----------------------------|
         |          Packet N          |
         +============================+
         |      Reference Epochs      |
         +============================+
         |      Packet Directory      |
         +============================+
         |       Epoch Directory      |
         +============================+
         |       Reserved  Area       |
         +============================+
         |     Segment Meta Data      |
         +----------------------------+

Only the placement of the meta data at the end of a generic segment
is required. The other data partitions may occur in any order in the
generic segment because the meta data will contain pointers to their
appropriate locations within the generic segment.
In the case of Type 14 SPK segments each `packet` contains an
epoch, EPOCH, an allowed time offset, OFFSET, from the epoch, and 6
sets of Chebyshev polynomial coefficients which are used to evaluate
the x,y,z, dx/dt, dy/dt, and dz/dt components of the state for epochs
within OFFSET seconds of the EPOCH. Each packet is organized with the
following structure:

.. code-block:: text

      ------------------------------------------------
      |  The midpoint of the approximation interval  |
      ------------------------------------------------
      |  The radius of the approximation interval    |
      ------------------------------------------------
      |  CHBDEG+1 coefficients for the X coordinate  |
      ------------------------------------------------
      |  CHBDEG+1 coefficients for the Y coordinate  |
      ------------------------------------------------
      |  CHBDEG+1 coefficients for the Z coordinate  |
      ------------------------------------------------
      |  CHBDEG+1 coefficients for the X velocity    |
      ------------------------------------------------
      |  CHBDEG+1 coefficients for the Y velocity    |
      ------------------------------------------------
      |  CHBDEG+1 coefficients for the Z velocity    |
      ------------------------------------------------

The maximum degree Chebyshev representation that can currently be
accommodated is 18. Packets are stored in increasing order of the
midpoint of the approximation interval.
The `constants` partition contains a single value, the degree of
the Chebyshev representation.

The reference epochs partition contains an ordered collection of
epochs. The i'th reference epoch corresponds to the beginning of the
interval for which the i'th packet can be used to determine the state
of the object modeled by this segment.

The `epoch directory` contains every 100th reference epoch. The
epoch directory is used to efficiently locate an the reference epoch
that should be associated with an epoch for which a state has been
requested.

The `packet directory` is empty.

As noted above the exact location of the various partitions must be
obtained from the Meta data contained at the end of the segment.

Access to the data should be made via the CSPICE generic segment
functions.

Type 14 segments should be created using the functions
:py:meth:`~spiceypy.spiceypy.spk14b`,
:py:meth:`~spiceypy.spiceypy.spk14a`, and
:py:meth:`~spiceypy.spiceypy.spk14e`. The usage of these functions
is discussed in :py:meth:`~spiceypy.spiceypy.spk14b`.

Type 15: Precessing Conic Propagation
------------------------------------------------------------------------------------------------------------

| The SPK data Type 15 represents a continuous ephemeris using a
  compact analytic model. The object is modeled as orbiting a central
  body under the influence of a central mass plus first order secular
  effects of the J2 term in harmonic expansion of the central body
  gravitational potential.

Type 15 SPK segments have the structure shown below:

.. code-block:: text

              +--------------------------------+
              | Epoch of Periapsis             |
              +--------------------------------+
              | Trajectory pole_x              |
              +--------------------------------+
              | Trajectory pole_y              |
              +--------------------------------+
              | Trajectory pole_z              |
              +--------------------------------+
              | Periapsis Unit Vector_x        |
              +--------------------------------+
              | Periapsis Unit Vector_y        |
              +--------------------------------+
              | Periapsis Unit Vector_z        |
              +--------------------------------+
              | Semi-Latus Rectum              |
              +--------------------------------+
              | Eccentricity                   |
              +--------------------------------+
              | J2 Processing Flag             |
              +--------------------------------+
              | Central Body Pole_x            |
              +--------------------------------+
              | Central Body Pole_y            |
              +--------------------------------+
              | Central Body Pole_z            |
              +--------------------------------+
              | Central Body GM                |
              +--------------------------------+
              | Central Body J2                |
              +--------------------------------+
              | Central Body Equatorial Radius |
              +--------------------------------+

It is important to note that the epoch must be that of periapsis
passage. Precession of the line of apsides and regression of the line
of nodes is computed relative to this epoch.
The effects of the J2 term are not applied if the eccentricity is
greater than or equal to 1.

To facilitate the creation of Type 15 segments, a segment writing
function called :py:meth:`~spiceypy.spiceypy.spkw15` has been
provided. This function takes as input arguments the handle of an SPK
file that is open for writing, the information needed to construct
the segment descriptor, and the data to be stored in the segment. The
header of the function provides a complete description of the input
arguments and an example of its usage.

Type 17: Equinoctial Elements
------------------------------------------------------------------------------------------------------------

| The SPK data Type 17 represents a continuous ephemeris using a
  compact analytic model. The object is following an elliptic orbit
  with precessing line of nodes and argument of periapse relative to
  the equatorial frame of some central body. The orbit is modeled via
  equinoctial elements.

Type 17 SPK segments have the structure shown below:

.. code-block:: text

                +----------------------------------+
             1  | Epoch of Periapsis               |
                +----------------------------------+
             2  | Semi-Major Axis                  |
                +----------------------------------+
             3  | H term of equinoctial elements   |
                +----------------------------------+
             4  | K term of equinoctial elements   |
                +----------------------------------+
             5  | Mean longitude at epoch          |
                +----------------------------------+
             6  | P term of equinoctial elements   |
                +----------------------------------+
             7  | Q term of equinoctial elements   |
                +----------------------------------+
             8  | rate of longitude of periapse    |
                +----------------------------------+
             9  | mean longitude rate              |
                +----------------------------------+
            10  | longitude of ascending node rate |
                +----------------------------------+
            11  | equatorial pole right ascension  |
                +----------------------------------+
            12  | equatorial pole declination      |
                +----------------------------------+

To facilitate the creation of Type 17 segments, a segment writing
function called :py:meth:`~spiceypy.spiceypy.spkw17` has been
provided. This function takes as input arguments the handle of an SPK
file that is open for writing, the information needed to construct
the segment descriptor, and the data to be stored in the segment. The
header of the function provides a complete description of the input
arguments and an example of its usage.


Type 18: ESOC/DDID Hermite/Lagrange Interpolation
------------------------------------------------------------------------------------------------------------

| SPK type 18 has been provided to support accurate duplication
  within the SPK system of spacecraft ephemerides used by the
  European Space Agency (ESA) on the Mars Express, Rosetta, SMART-1
  and Venus Express missions. However, the algorithms used by SPK
  type 18 are very general; type 18's applicability is by no means
  limited to these missions.

Because of the possibility of evolution of the mathematical
representations of ephemerides used by ESA, SPK type 18 is designed
to accommodate multiple representations, thereby avoiding a
proliferation of SPK data types. SPK type 18 refers to each supported
mathematical representation of ephemeris data as a `subtype.`

Currently SPK type 18 supports two subtypes:

#. Subtype 0

- Separate sliding-window Hermite interpolation of position and
  velocity. The ephemeris is represented by a series of 12-element
  `packets` and associated time tags. The time tags may be
  unequally spaced. Each packet contains three Cartesian position
  components, three velocity components meant to be used for Hermite
  interpolation of the position, three velocity components (not
  necessarily equal to the previous three), and three acceleration
  components meant to be used with the second set of velocity
  components for Hermite interpolation of the velocity. The position
  and velocity resulting from this interpolation method are in
  principle independent. The same interpolation degree is used for
  each position and velocity component.

#. Subtype 1

- Separate sliding-window Lagrange interpolation of position and
  velocity. The ephemeris is represented by a series of 6-element
  `packets` and associated time tags. The time tags may be
  unequally spaced. Each packet contains three Cartesian position
  components and three velocity components. The position components
  and velocity components are interpolated separately. The position
  and velocity resulting from this interpolation method are in
  principle independent. The same interpolation degree is used for
  each position and velocity component.

The sliding-window interpolation technique used by this data type
works as follows: for any request epoch, the data type defines a
component of position or velocity by interpolating a set of values of
that component defined on a set of consecutive time tags---a
"window"---centered as closely as possible to the request epoch. The
nominal window size is dictated by the degree and type (Hermite vs.
Lagrange) of the interpolating polynomials. Normally the window of
time tags has even size, and the window is selected so that the
request time is located between the two central time tags in the
window.
When the request time is near a segment boundary, the window is
truncated if necessary on the side closest to the boundary. If a
segment contains too few packets to form a window of nominal size, as
many packets as are needed and available are used to construct the
window. In this case the window size may be odd. In any case the
window never includes more than WNDSIZ/2 time tags on either side of
the request time, where WNDSIZ is the nominal window size.

The states in a type 18 segment are geometric: they do not take into
account aberration corrections. The position and velocity components
of each packet represent the position (x, y, z, in kilometers and
kilometers per second) of the body to which the ephemeris applies,
relative to the center specified by the segment's descriptor. The
epochs corresponding to the states are barycentric dynamical times
(TDB), expressed as seconds past J2000.

Type 18 SPK segments have the structure shown below:

.. code-block:: text

      +-----------------------+
      | Packet 1              |
      +-----------------------+
      | Packet 2              |
      +-----------------------+
                  .
                  .
                  .
      +-----------------------+
      | Packet N              |
      +-----------------------+
      | Epoch 1               |
      +-----------------------+
      | Epoch 2               |
      +-----------------------+
                  .
                  .
                  .
      +-----------------------+
      | Epoch N               |
      +-----------------------+
      | Epoch 100             | (First directory)
      +-----------------------+
                  .
                  .
                  .
      +-----------------------+
      | Epoch ((N-1)/100)*100 | (Last directory)
      +-----------------------+
      | Subtype code          |
      +-----------------------+
      | Window size           |
      +-----------------------+
      | Number of packets     |
      +-----------------------+


In the diagram, each box representing a packet corresponds to either
twelve or six double precision numbers; the other boxes represent
individual double precision numbers. The number of states normally
should be greater than or equal to the window size, which is related
to the polynomial degree as shown:

.. code-block:: text

      Subtype 0:     DEGREE  =  2 * WINDOW_SIZE  -  1
      Subtype 1:     DEGREE  =      WINDOW_SIZE  -  1

The set of time tags is augmented by a series of directory entries;
these entries allow the type 18 reader to search for states more
efficiently. The directory entries contain time tags whose indices
are multiples of 100. The set of indices of time tags stored in the
directories ranges from 100 to

.. code-block:: text

      (  (N-1) / 100  ) * 100

where N is the total number of time tags. Note that if N is

.. code-block:: text

      Q * 100

then only

.. code-block:: text

      Q - 1

directory entries are stored, and in particular, if there are only
100 states in the segment, there are no directories.
To facilitate the creation of type 18 segments, a segment writing
routine called :py:meth:`~spiceypy.spiceypy.spkw18` has been
provided. This routine takes as input arguments the handle of an SPK
file that is open for writing, the information needed to construct
the segment descriptor, and the data to be stored in the segment. The
header of the subroutine provides a complete description of the input
arguments and an example of its usage.

Type 19: ESOC/DDID Piecewise Interpolation
------------------------------------------------------------------------------------------------------------

| As with SPK type 18, SPK type 19 has been provided to support
  accurate duplication by the SPK system of spacecraft ephemerides
  used by the European Space Agency (ESA) on the Mars Express,
  Rosetta, SMART-1 and Venus Express missions.

SPK type 19 is an enhanced version of SPK type 18. Type 19 enables
creation of SPK files representing the same ephemerides that can be
represented using type 18, but containing far fewer segments. Data
from multiple type 18 segments can be stored in a single type 19
segment, as long as those segments satisfy certain restrictions:

- The segments are for the same body, center, and reference
  frame.

- The segments' coverage intervals, when arranged in
  increasing time order, overlap only at their endpoints, and have no
  intervening gaps.

Within a type 19 segment, each set of data corresponding to a type 18
segment is called a `mini-segment.` A type 19 segment contains one
or more mini-segments.
Each mini-segment contains a time ordered, strictly increasing
sequence of epochs (no two epochs of the same mini-segment may
coincide) and an associated sequence of ephemeris data sets called
`packets.` The composition of a packet depends on the subtype of
the mini-segment to which the packet belongs; subtypes are discussed
in more detail below.

The time coverage of a mini-segment is called an `interpolation interval.` The endpoints (boundaries) of each interpolation interval
must be contained in the time interval bounded by the first and last
members of the epoch sequence of the corresponding mini-segment. If
the Ith mini-segment's epoch sequence is

.. code-block:: text

      E_I1, ..., E_IM

and the mini-segment's interpolation interval bounds are

.. code-block:: text

      IV_IB, IV_IE

then it is required that

.. code-block:: text

      E_I1 < IV_IB < IV_IE < E_IM
           -              -

Mini-segments are allowed to contain `padding` epochs and packets
beyond both ends of their interpolation intervals. Padding epochs on
the left of an interpolation interval are less than the interval
start time; padding epochs on the right exceed the interval stop
time. Padding enables control of interpolation behavior at and near
interpolation interval boundaries. Padding does not contribute to a
type 19 segment's time coverage. The use of padding is discussed in
greater detail below.
The interpolation intervals of a type 19 segment have no intervening
gaps and overlap only at single points. The end time of each
interpolation interval is the start time of the next. The start time
of a type 19 segment is greater than or equal to the start time of
the first interval, and the segment's end time is less than or equal
to the stop time of the last interval.

Interpolation intervals must have strictly positive length.

When type 19 data are interpolated to produce a state vector for a
given request time, only data from a single mini-segment whose
interpolation interval contains the request time are used.

When a request time coincides with the boundary between two
interpolation intervals, there is a choice as to which interval will
provide ephemeris data. The creator of a type 19 segment can control
this behavior via a parameter passed to the type 19 segment writer
spkw19_c. For a given type 19 segment, depending on the value of this
parameter, either the earlier interval is always selected, or the
later interval is always selected.

Because of the possibility of evolution of the mathematical
representations of ephemerides used by ESA, SPK type 19 is designed
to accommodate multiple representations of state data, thereby
avoiding a proliferation of SPK data types. SPK type 19 refers to
each supported mathematical representation of ephemeris data as a
`subtype.`

Currently SPK type 19 supports three subtypes:

#. Subtype 0

- Separate sliding-window Hermite interpolation of position and
  velocity. The ephemeris is represented by a series of 12-element
  `packets` and associated time tags. The time tags may be
  unequally spaced. Each packet contains three Cartesian position
  components, three velocity components meant to be used for Hermite
  interpolation of the position, three velocity components (not
  necessarily equal to the previous three), and three acceleration
  components meant to be used with the second set of velocity
  components for Hermite interpolation of the velocity. The position
  and velocity resulting from this interpolation method are in
  principle independent. The same interpolation degree is used for
  each position and velocity component.

- The interpolation degree of a subtype 0 mini-segment must be
  equivalent to 3 mod 4, that is, it must be in the set

.. code-block:: text

               { 3, 7, 11, ..., MAXDEG }

- where MAXDEG is the maximum supported degree.

#. Subtype 1

- Separate sliding-window Lagrange interpolation of position and
  velocity. The ephemeris is represented by a series of 6-element
  `packets` and associated time tags. The time tags may be
  unequally spaced. Each packet contains three Cartesian position
  components and three velocity components. The position components
  and velocity components are interpolated separately. The position
  and velocity resulting from this interpolation method are in
  principle independent. The same interpolation degree is used for
  each position and velocity component.

- The interpolation degree of a subtype 1 mini-segment must be
  odd and must be in the range 1:MAXDEG, where MAXDEG is the maximum
  supported degree.

#. Subtype 2

- Sliding-window Hermite interpolation of position and velocity.
  The ephemeris is represented by a series of 6-element `packets`
  and associated time tags. The time tags may be unequally spaced.
  Each packet contains three Cartesian position components and three
  velocity components. The position components and velocity
  components are interpolated together.

- The interpolation degree of a subtype 2 mini-segment must be
  equivalent to 3 mod 4, that is, it must be in the set

.. code-block:: text

               { 3, 7, 11, ..., MAXDEG }

- where MAXDEG is the maximum supported degree.

The sliding-window interpolation technique used by this data type
works as follows: for any request epoch, the data type's state
evaluation code computes a component of position or velocity by
interpolating a set of values of that component defined on a set of
consecutive time tags---a "window"---centered as closely as possible
to the request epoch. The nominal window size is dictated by the
degree and type (Hermite vs. Lagrange) of the interpolating
polynomials. Normally the window of time tags has even size, and the
window is selected so that the request time is located between the
two central time tags in the window. When the request time is too
close to an endpoint of the mini-segment's epoch sequence to permit
construction of a window of nominal size, the window is truncated at
that endpoint.
Although type 19 interpolation intervals support padding, padding is
not required. Below we'll discuss the role of padding, but the reader
should keep in mind that the size of the pads at either end of an
interpolation interval could be zero.

In SPK type 19, interpolation interval padding boundaries (the start
time of the padding preceding the interval's coverage and the stop
time of the padding following the coverage) affect interpolation in
the same way that segment boundaries affect type 18 interpolation.
When the request time is near a padding boundary, the window is
truncated if necessary on the side closest to the boundary. If an
interpolation interval, including padding, contains too few packets
to form a window of nominal size, as many packets as are needed and
available are used to construct the window. In this case the window
size may be odd. In any case the window never includes more than
WNDSIZ/2 time tags on either side of the request time, where WNDSIZ
is the nominal window size.

The mini-segments of a type 19 segment need not use the same subtypes
and interpolation degrees.

The states in a type 19 segment are geometric: they do not take into
account aberration corrections. The position and velocity components
of each packet represent the position (x, y, z, in kilometers and
kilometers per second) of the body to which the ephemeris applies,
relative to the center specified by the segment's descriptor. The
epochs corresponding to the states are barycentric dynamical times
(TDB), expressed as seconds past J2000.

Type 19 SPK segments have the structure shown below:

.. code-block:: text

      +--------------------------------+
      | Interval 1 mini-segment        |
      +--------------------------------+
                      .
                      .
                      .
      +--------------------------------+
      | Interval N mini-segment        |
      +--------------------------------+
      | Interval 1 start time          |
      +--------------------------------+
                      .
                      .
                      .
      +--------------------------------+
      | Interval N start time          |
      +--------------------------------+
      | Interval N stop time           |
      +--------------------------------+
      | Interval start 100             | (First interval directory)
      +--------------------------------+
                      .
                      .
                      .
      +--------------------------------+
      | Interval start (N/100)*100     | (Last interval directory)
      +--------------------------------+
      | Mini-segment 1 start pointer   |
      +--------------------------------+
                      .
                      .
                      .
      +--------------------------------+
      | Mini-segment N start pointer   |
      +--------------------------------+
      | Mini-segment N stop pointer    |
      +--------------------------------+
      | Boundary choice flag           |
      +--------------------------------+
      | Number of intervals            |
      +--------------------------------+

Below we first describe the overall segment structure, then we cover
the mini-segment structure.
The array of interval boundaries contains the start time of each
interval, plus the stop time of the final interval.

The list of interpolation interval boundary times has its own
directory, which has the same structure as the time tag directories
of type 18 segments. Let the interval count be N. As with time tag
directories, the start time directory contains boundary times whose
indices are multiples of 100, except that if N+1 is a multiple of
100, the last boundary time is not included.

The array of mini-segment pointers contains a pointer to the start of
each mini-segment, plus a final `stop` pointer for the final
mini-segment. The stop pointer points to the location immediately
following the last address of the final mini-segment.

The mini-segment pointers are 1-based indices relative to the start
address of the segment. For example, a pointer value of 1 indicates
the first address of the segment.

Following the mini-segment pointers is the interval selection flag.
When this flag has the value 1.D0, the later interpolation interval
is used when a request time falls on the common boundary between two
interpolation intervals. If the selection flag is 0, the earlier
interval is used.

Each mini-segment has the structure of a type 18 SPK segment. The
structure is shown below:

.. code-block:: text

      +-----------------------+
      | Packet 1              |
      +-----------------------+
                  .
                  .
                  .
      +-----------------------+
      | Packet M              |
      +-----------------------+
      | Epoch 1               |
      +-----------------------+
                  .
                  .
                  .
      +-----------------------+
      | Epoch M               |
      +-----------------------+
      | Epoch 100             | (First time tag directory)
      +-----------------------+
                  .
                  .
                  .
      +-----------------------+
      | Epoch ((M-1)/100)*100 | (Last time tag directory)
      +-----------------------+
      | Subtype code          |
      +-----------------------+
      | Window size           |
      +-----------------------+
      | Number of packets     |
      +-----------------------+


In the mini-segment diagram, each box representing a packet
corresponds to either twelve or six double precision numbers; the
other boxes represent individual double precision numbers. The number
of packets normally should be greater than or equal to the window
size, which is related to the polynomial degree as shown:

.. code-block:: text

      Subtype 0:     DEGREE  =  2 * WINDOW_SIZE  -  1
      Subtype 1:     DEGREE  =      WINDOW_SIZE  -  1
      Subtype 2:     DEGREE  =  2 * WINDOW_SIZE  -  1

The mini-segment's set of time tags is augmented by a series of
directory entries; these entries allow the type 19 reader to search
for packets more efficiently. The directory entries contain time tags
whose indices are multiples of 100. The set of indices of time tags
stored in the directories ranges from 100 to

.. code-block:: text

      (  (M-1) / 100  ) * 100

where M is the total number of time tags. Note that if M is

.. code-block:: text

      Q * 100

then only

.. code-block:: text

      Q - 1

directory entries are stored, and in particular, if there are only
100 states in the segment, there are no directories.
Following the time tag directory are three parameters associated with
the mini-segment: the subtype, the interpolation window size, and the
packet count.

To facilitate the creation of type 19 segments, a segment writing
routine called spkw19_c has been provided. This routine takes as
input arguments the handle of an SPK file that is open for writing,
the information needed to construct the segment descriptor, and the
data to be stored in the segment. The header of the subroutine
provides a complete description of the input arguments and an example
of its usage.

Type 20: Chebyshev (velocity only)
------------------------------------------------------------------------------------------------------------

| SPK data type 20 contains Chebyshev polynomial coefficients for the
  velocity of a body, relative to its center of motion, as a function
  of time. The position of the body is obtained by integrating the
  velocity using a specified integration constant.

This data type is provided to accurately represent `EPM`
ephemerides developed by the Institute of Applied Astronomy (IAA),
Russian Academy of Sciences (RAS).

Each type 20 segment contains an arbitrary number of logical records.
Each record contains a set of Chebyshev coefficients valid throughout
an interval of fixed length. Each record also contains a position
vector applicable at the midpoint of its coverage interval.

The records within a segment are ordered by increasing initial epoch.
All records contain the same number of coefficients. A segment of
this type is structured as

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
      | DSCALE        |
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

A set of seven parameters at the end of the segment provides the
information needed to determine the location of the record
corresponding to a particular epoch and to determine the units
associated with the data:

#. DSCALE is the distance scale used for both position and
   velocity; DSCALE has units of km. For example, if the distance
   units are AU, then DSCALE is the value of the AU in km.

#. TSCALE is the time scale used for velocity; TSCALE has units
   of TDB seconds. For example, if the time units of the velocity data
   are TDB Julian days, then TSCALE is 86400.

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
   expansions for each velocity component.

#. N is the number of records contained in the segment.

Each record is structured as follows:

.. code-block:: text

      +------------------+
      | X  data          |
      +------------------+
      | Y  data          |
      +------------------+
      | Z  data          |
      +------------------+

where each data section for coordinate I contains

.. code-block:: text

      +-------------------------------------------------+
      | Chebyshev coefficients for velocity component I |
      +-------------------------------------------------+
      | Position component I at interval midpoint       |
      +-------------------------------------------------+

The velocity coefficients have units of DSCALE km/TSCALE seconds:
multiplying a Chebyshev expansion's value by DSCALE/TSCALE converts
velocity to units of km/s.
The position at a record's midpoint epoch is given in units of DSCALE
km: multiplying the position by DSCALE converts the position to units
of km.

Type 20 data are used to compute states as follows: for a given time
T seconds past J2000 TDB, let MID and RADIUS be the midpoint and
radius, expressed as seconds past J2000 TDB, of the record coverage
interval that contains T: the coverage interval is the time span

.. code-block:: text

      MID - RADIUS : MID + RADIUS

The velocity at T of the body relative to its center of motion is
given by the value of the corresponding record's Chebyshev expansions
at S, where

.. code-block:: text

      S = (T - MID) / RADIUS

The position of the body relative to its center of motion at T is
given by

.. code-block:: text

                                            S
      (Position at MID) +  RADIUS*( Integral ( Velocity ) )
                                            0

The function spke20\_ contains the algorithm used to construct a
state from a particular logical record.
To facilitate the creation of Type 20 segments, a segment writing
function called :py:meth:`~spiceypy.spiceypy.spkw20` has been
provided. This function takes as input arguments the handle of an SPK
file that is open for writing, the information needed to construct
the segment descriptor, and the data to be stored in the segment. The
header of the function provides a complete description of the input
arguments and an example of its usage.

Type 21: Extended Modified Difference Arrays
------------------------------------------------------------------------------------------------------------

| SPK data type 21 contains extended Modified Difference Arrays
  (MDA), also called `difference lines.` These data structures use
  the same mathematical trajectory representation as SPK data type 1,
  but type 21 allows use of larger, higher-degree MDAs.

This data type is normally used for spacecraft whose ephemerides are
produced by JPL's principal trajectory integrator---DPTRAJ.
Difference lines are extracted from spacecraft trajectory files
(`P-files` and `PV-files` ) created by DPTRAJ.

Each segment containing Modified Difference Arrays contains an
arbitrary number of logical records. Each record contains difference
line coefficients applicable over a time interval containing a
reference epoch, along with the state at that epoch. The time
intervals of adjacent records overlap at their common endpoints.

The contents of the records themselves are described in [163]. The
function spke21\_ contains the algorithm used to construct a state
from a particular record and epoch.

The records within a segment are ordered by increasing final epoch.
The final epochs associated with the records must be distinct.

A segment of this type is structured as follows:

.. code-block:: text

      +-----------------------------------------+
      | Record 1 (difference line coefficients) |
      +-----------------------------------------+
      | Record 2 (difference line coefficients) |
      +-----------------------------------------+
        .
        .
        .
      +-----------------------------------------+
      | Record N (difference line coefficients) |
      +-----------------------------------------+
      | Epoch 1                      |
      +------------------------------+
      | Epoch 2                      |
      +------------------------------+
        .
        .
        .
      +------------------------------+
      | Epoch N                      |
      +------------------------------+
      | Epoch 100                    |   (First directory epoch)
      +------------------------------+
      | Epoch 200                    |   (Second directory epoch)
      +------------------------------+
        .
        .
        .
      +------------------------------+
      | Epoch (N/100)*100            |   (Final directory epoch)
      +------------------------------+
      | Difference line size         |
      +------------------------------+
      | N                            |
      +------------------------------+

The number of records in a segment, N, can be arbitrarily large.
Records 1 through N contain the difference line coefficients and
other constants needed to compute state data. Each one of these
records contains DLSIZE double precision numbers, where DLSIZE is in
the range

..code-block::

      71 : (4*MAXTRM) + 1

inclusive. MAXTRM is declared in the SPICELIB include file spk21.inc.
A list of the final epochs of the records is stored immediately after
the last record.

Following the list of epochs is a second list, the `directory`
containing every 100th epoch from the previous list. If there are N
epochs, there will be N/100 directory epochs. If there are fewer than
100 epochs, then the segment will not contain any directory epochs.
Directory epochs are used to speed up access to desired records.

The penultimate element of the segment is the difference line size.
The final element in the segment is the number of records contained
in the segment, N.

The index of the record providing ephemeris data for a user-specified
epoch is the index of the first epoch in the segment's epoch list not
less than the specified epoch.

Appendix A --- Summary of SP-kernel Functions
================================================


Summary of Mnemonics
---------------------


| CSPICE contains a family of functions that are designed
  specifically for use with SPK files. The name of each function
  begins with the letters `spk`, followed by a two- or
  three-character mnemonic. For example, the function that returns
  the state of one body with respect to another is named
  :py:meth:`~spiceypy.spiceypy.spkez`, pronounced `S-P-K-E-Z` .

Many of the lower-level CSPICE functions have SPICELIB counterparts
implemented in Fortran as entry points of another function.

The following is a complete list of mnemonics and translations, in
alphabetical order.

Implemented CSPICE wrappers:

* :py:meth:`~spiceypy.spiceypy.furnsh`
* :py:meth:`~spiceypy.spiceypy.spk14a`
* :py:meth:`~spiceypy.spiceypy.spk14b`
* :py:meth:`~spiceypy.spiceypy.spk14e`
* :py:meth:`~spiceypy.spiceypy.spkacs`
* :py:meth:`~spiceypy.spiceypy.spkapo`
* :py:meth:`~spiceypy.spiceypy.spkaps`
* :py:meth:`~spiceypy.spiceypy.spkcls`
* :py:meth:`~spiceypy.spiceypy.spkcov`
* :py:meth:`~spiceypy.spiceypy.spkcpo`
* :py:meth:`~spiceypy.spiceypy.spkcpt`
* :py:meth:`~spiceypy.spiceypy.spkcvo`
* :py:meth:`~spiceypy.spiceypy.spkcvt`
* :py:meth:`~spiceypy.spiceypy.spkez`
* :py:meth:`~spiceypy.spiceypy.spkezp`
* :py:meth:`~spiceypy.spiceypy.spkezr`
* :py:meth:`~spiceypy.spiceypy.spkgeo`
* :py:meth:`~spiceypy.spiceypy.spkgps`
* :py:meth:`~spiceypy.spiceypy.spklef`
* :py:meth:`~spiceypy.spiceypy.spkltc`
* :py:meth:`~spiceypy.spiceypy.spkobj`
* :py:meth:`~spiceypy.spiceypy.spkopa`
* :py:meth:`~spiceypy.spiceypy.spkopn`
* :py:meth:`~spiceypy.spiceypy.spkpds`
* :py:meth:`~spiceypy.spiceypy.spkpos`
* :py:meth:`~spiceypy.spiceypy.spkpvn`
* :py:meth:`~spiceypy.spiceypy.spksfs`
* :py:meth:`~spiceypy.spiceypy.spkssb`
* :py:meth:`~spiceypy.spiceypy.spksub`
* :py:meth:`~spiceypy.spiceypy.spkuds`
* :py:meth:`~spiceypy.spiceypy.spkuef`
* :py:meth:`~spiceypy.spiceypy.spkw02`
* :py:meth:`~spiceypy.spiceypy.spkw03`
* :py:meth:`~spiceypy.spiceypy.spkw05`
* :py:meth:`~spiceypy.spiceypy.spkw08`
* :py:meth:`~spiceypy.spiceypy.spkw09`
* :py:meth:`~spiceypy.spiceypy.spkw10`
* :py:meth:`~spiceypy.spiceypy.spkw12`
* :py:meth:`~spiceypy.spiceypy.spkw13`
* :py:meth:`~spiceypy.spiceypy.spkw15`
* :py:meth:`~spiceypy.spiceypy.spkw17`
* :py:meth:`~spiceypy.spiceypy.spkw18`
* :py:meth:`~spiceypy.spiceypy.spkw20`
* :py:meth:`~spiceypy.spiceypy.unload`


Summary of Calling Sequences
------------------------------


| The calling sequences for the SPK functions are summarized below.
  The functions are grouped by purpose.

High level routines for loading, unloading files:

* :py:meth:`~spiceypy.spiceypy.furnsh`
* :py:meth:`~spiceypy.spiceypy.unload`

Lower level routines for loading, unloading files:

* :py:meth:`~spiceypy.spiceypy.spklef`
* :py:meth:`~spiceypy.spiceypy.spkuef`

Getting coverage summary:

* :py:meth:`~spiceypy.spiceypy.spkobj`
* :py:meth:`~spiceypy.spiceypy.spkcov`

Computing states and positions:

* :py:meth:`~spiceypy.spiceypy.spkezr`
* :py:meth:`~spiceypy.spiceypy.spkpos`
* :py:meth:`~spiceypy.spiceypy.spkez`
* :py:meth:`~spiceypy.spiceypy.spkezp`
* :py:meth:`~spiceypy.spiceypy.spkapo`
* :py:meth:`~spiceypy.spiceypy.spkpvn`
* :py:meth:`~spiceypy.spiceypy.spkssb`
* :py:meth:`~spiceypy.spiceypy.spkgeo`
* :py:meth:`~spiceypy.spiceypy.spkgps`

Low-level routines for computing states and positions:

* :py:meth:`~spiceypy.spiceypy.spkacs`
* :py:meth:`~spiceypy.spiceypy.spkaps`
* :py:meth:`~spiceypy.spiceypy.spkltc`

Computing states using constant-velocity or constant-position
objects:

* :py:meth:`~spiceypy.spiceypy.spkcpo`
* :py:meth:`~spiceypy.spiceypy.spkcpt`
* :py:meth:`~spiceypy.spiceypy.spkcvo`
* :py:meth:`~spiceypy.spiceypy.spkcvt`

Selecting files, segments:

* :py:meth:`~spiceypy.spiceypy.spksfs`

Writing segments to files:

* :py:meth:`~spiceypy.spiceypy.spkpds`
* :py:meth:`~spiceypy.spiceypy.spkw02`
* :py:meth:`~spiceypy.spiceypy.spkw03`
* :py:meth:`~spiceypy.spiceypy.spkw05`
* :py:meth:`~spiceypy.spiceypy.spkw08`
* :py:meth:`~spiceypy.spiceypy.spkw09`
* :py:meth:`~spiceypy.spiceypy.spkw10`
* :py:meth:`~spiceypy.spiceypy.spkw12`
* :py:meth:`~spiceypy.spiceypy.spkw13`
* :py:meth:`~spiceypy.spiceypy.spkw15`
* :py:meth:`~spiceypy.spiceypy.spkw17`
* :py:meth:`~spiceypy.spiceypy.spkw18`
* :py:meth:`~spiceypy.spiceypy.spkw20`

Examining segment descriptors:

* :py:meth:`~spiceypy.spiceypy.spkuds`

Extracting subsets of data from a segment:

* :py:meth:`~spiceypy.spiceypy.spksub`

To write new or append segments to SPK files:

* :py:meth:`~spiceypy.spiceypy.spkopn`
* :py:meth:`~spiceypy.spiceypy.spkopa`
* :py:meth:`~spiceypy.spiceypy.spkcls`



Appendix B --- A Template for SPK Comments
=============================================

| An undocumented ephemeris is in many respects worse than
  undocumented source code. With source code you can at least read
  the code and perhaps discern the function of the source code. An
  ephemeris on the other hand is a binary file. All it contains are
  numbers. It's very difficult to determine the purpose of an
  ephemeris simply from the state information it contains. For this
  reason, any ephemeris created for use by anyone other than yourself
  needs documentation.

If you create SPK files NAIF strongly recommends that you include
descriptive documentation in the comments portion of the SPK file.
You can use the utility program COMMNT to insert comments into the
file, or you may use the functions in the SPC family to insert the
comments when you create the SPK file. (See
`commnt.ug <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/ug/commnt.html>`__ or `spc.req <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/spc.html>`__
for further details.)

This appendix addresses the contents of your comments. What will
others (or yourself) want to know about the SPK file weeks, months or
years after it has been created? Providing this information can be a
challenge. It's difficult to know in advance all the questions
someone might ask about an ephemeris you've created. To assist with
this task NAIF has devised a `template` that you may wish to use
as a starting point when creating the comments for an SPK file.

Constraints
-------------

| The comments you place in an SPK file must be plain ASCII text.
  Each line of text must consist of 80 or fewer characters. The text
  must contain only printing characters (ASCII characters 32 through
  126).

The Basic Template
------------------

| Here's one way to create the comments for an SPK file.

Objects in the Ephemeris
------------------------------------------------------------------------------------------------------------

| List the names and NAIF ID codes for the objects in the file.

Approximate Time Coverage
------------------------------------------------------------------------------------------------------------

| Provide a summary of the time for which states are available for
  the objects in the file. If you use UTC times in this summary and
  the ephemeris extends more than 6 months into the future, you
  should probably state that the times are approximate. You don't
  know when leapseconds will occur more than a few months in advance,
  so you can't know the exact UTC time boundaries for the ephemeris
  if it extends years into the future.

Status
------------------------------------------------------------------------------------------------------------

| Provide the `status` of the ephemeris. Tell the user why this
  ephemeris was created and for whom it is intended. For example, if
  this is the second in a series of ephemerides that will be produced
  for some object tell which ephemeris this one supersedes. Tell the
  user when the next ephemeris in the series will be available. Is
  the ephemeris suitable only for preliminary studies? Is it good for
  all Earth based observations? Is this an official operational
  product? Are there situations for which the ephemeris is not
  suitable?

Pedigree
------------------------------------------------------------------------------------------------------------

| Provide a production summary for the ephemeris. Tell when the
  ephemeris was produced (the system time stamp may not port if the
  file is copied to other systems). Say who produced the ephemeris;
  what source products were used in the production; what version of
  the producing program was used in the creation of the ephemeris. If
  the ephemeris is based on a set of recent observations, say so. In
  short give the user the pedigree of this ephemeris. This
  information is mostly for your benefit. If a problem arises with
  the ephemeris, you will know how the problem was created and have a
  better chance of fixing the problem.

Usage
------------------------------------------------------------------------------------------------------------

| Provide information the user will need to effectively use the
  ephemeris. Tell the user what other SPICE kernels are needed to use
  this ephemeris. For example, if the ephemeris contains only the
  state of an asteroid relative to the sun, the user will probably
  need a planetary ephemeris to effectively use the one you've
  created. Recommend a planetary ephemeris to use with your SPK file.
  If the ephemeris contains states of objects relative to
  non-inertial frames, the user will probably need other kernels so
  that various state transformations can be performed. Recommend
  which of these kernels the user should use with your SPK file.

Accuracy
------------------------------------------------------------------------------------------------------------

| If possible give some estimate as to the accuracy of your SPK file.
  Use numbers. Words such as `this is the best available` do not
  convey how much you know about the ephemeris.

Special Notes
------------------------------------------------------------------------------------------------------------

| Provide a description of any special properties of this ephemeris.
  For example, if some observation seems to be in conflict with this
  ephemeris you should probably point this out.

References
------------------------------------------------------------------------------------------------------------

| List any references that may be relevant to the understanding of
  the ephemeris. For example, if the ephemeris is based upon
  observations contained in the literature, site the appropriate
  articles. If there is some technical memorandum or private
  communication that addresses certain aspects of this ephemeris list
  it. This will allow you to more easily answer questions about the
  ephemeris.

