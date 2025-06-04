****************
Reference Frames
****************

This required reading document is reproduced from the original NAIF
document available at `https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/frames.html <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/frames.html>`_

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

| The frames subsystem specifies the relationships of various kinds
  of reference frames supported by SPICE. This facilitates
  `behind-the-scenes` transformations between these frames.



Purpose
-------

| This document describes how reference frames are treated within
  SPICE. The document includes a general discussion of reference
  frames, detailed information about various types of frames
  supported within SPICE, and instructions on defining additional
  reference frames to assist in a user's computations.



Intended Audience
-----------------

| This document addresses the needs of several groups of users. Users
  looking for a basic discussion of reference frames and a list of
  the frames supported by the SPICE system should read the chapter
  `Using Frames.` Users desiring to customize their environment by
  adding new frames should read the chapter `Creating a Frame
  Kernel.`

This document assumes you have some familiarity with SPICE concepts
and terminology. If you are new to the SPICE system, or just a bit
rusty with it, you should consider reviewing `An Overview of the
SPICE System` and `An Introduction to SPICE.`



Using Frames
============

|



Frame Functions in SPICE
-------------------------

| The SPICE frame subsystem facilitates `behind-the-scenes` frame
  transformations. This allows you to concentrate on questions more
  closely related to the problem you are trying to solve instead of
  the details of on how to get position or state vectors in the frame
  of interest.



Frame Transformation Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Several user-level CSPICE functions require that the user supply
  the name of a reference frame as one of the inputs to the function.
  The most important of these is the function
  :py:meth:`~spiceypy.spiceypy.spkezr`. This function returns the
  state (Cartesian position and velocity) of one object relative to
  another in a user specified reference frame. The choice of
  reference frame often makes a big difference in the usefulness of a
  returned state. If the state is given relative to the reference
  frame of interest to the user, computations involving that state
  can be much simpler than if the state is returned relative to some
  other reference frame.

The two user-level interface functions that deal solely with frame
transformations are :py:meth:`~spiceypy.spiceypy.sxform` and
:py:meth:`~spiceypy.spiceypy.pxform`. sxform_c supports
transformations of Cartesian state vectors (6 components) between
reference frames while :py:meth:`~spiceypy.spiceypy.pxform`
supports transformations of Cartesian position vectors (3
components). :py:meth:`~spiceypy.spiceypy.pxform` may be used when
only position information is needed, or when the derivatives required
for a state transformation are unavailable, for example when one
frame is defined by a C-kernel that lacks angular velocity data.

The calling sequences for these functions are

.. code-block:: python

        xform  = sxform( from, to, et )
        rotate = pxform( from, to, et )

The output of :py:meth:`~spiceypy.spiceypy.sxform`, \`xform', is a
6 by 6 matrix used to transform state vectors relative to a reference
frame, the name of which is specified by the \`from' input argument,
to states relative to another reference frame, the name of which is
specified by the \`to' input argument, at the epoch \`et' (specified
in seconds past J2000).
The output of :py:meth:`~spiceypy.spiceypy.pxform`, \`rotate', is a
3 by 3 transformation matrix equivalent to the upper left 3x3 block
of \`xform'. This matrix transforms position as opposed to state
vectors.



Frame Information Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| The SPICE frame subsystem contains a set of functions that enable
  applications to retrieve information about frames known to SPICE,
  whether they are built-in or specified by means of frame kernels:

:py:meth:`~spiceypy.spiceypy.frmnam`
   Convert frame ID code to frame name.

:py:meth:`~spiceypy.spiceypy.namfrm`
   Convert frame name to frame ID code.

:py:meth:`~spiceypy.spiceypy.frinfo`
   Return frame specification parameters: frame center, frame class,
   and frame class ID.

:py:meth:`~spiceypy.spiceypy.cidfrm`
   Map body ID code to the default frame centered on the specified
   body. Both frame name and ID are returned.

:py:meth:`~spiceypy.spiceypy.cnmfrm`
   Map body name to the default frame centered on the specified body.
   Both frame name and ID are returned.

:py:meth:`~spiceypy.spiceypy.ccifrm`
   Map frame class and class ID to frame specification parameters:
   frame ID code, frame name and frame center are returned.

   This function provides a way to identify frames referenced in CK
   and PCK files: in these files, segment descriptors contain class
   IDs of frames.

See the section `Specifying a New Frame` below for more
information on frame specification parameters.


Frames Supported in SPICE
--------------------------

| In both cases -- with the functions requiring specification of a
  reference frame as one of the inputs (for example
  :py:meth:`~spiceypy.spiceypy.spkezr`), and with the functions
  computing transformation between two reference frames
  (:py:meth:`~spiceypy.spiceypy.sxform` and
  :py:meth:`~spiceypy.spiceypy.pxform`) -- you specify the frame or
  frames of interest using a character string that contains the name
  of the reference frame.

In SPICE function interfaces, frames are typically designated by C
strings. In text kernel files, frame names are designated by strings
delimited by single quotes, as in FORTRAN. Examples below showing
single-quoted frame names exhibit the names as they appear in text
kernels; these same names are double-quoted when referred to as
literal strings in C source code.

A number of names are automatically recognized by the frame subsystem
because the definitions for these frames are `built into` SPICE
software. Among these frames are:

- inertial frames such as Earth mean equator and equinox of
  J2000 frame ('J2000'), Mean ecliptic and equinox of J2000
  ('ECLIPJ2000'), Galactic System II frame ('GALACTIC'), Mars Mean
  Equator and IAU vector of J2000 frame ('MARSIAU'), etc. For the
  complete list of `built in` inertial reference frames refer to
  the appendix `built in Inertial Reference Frames` of this
  document.

- The ICRF is a special case. See the section titled `ICRF vs
  J2000` below.

- body-fixed frames based on IAU rotation models provided in
  text PCK files, such as Earth body-fixed rotating frame
  ('IAU_EARTH') and Mars body-fixed rotating frame ('IAU_MARS'), and
  body-fixed frames based on high precision Earth rotation models
  provided in binary PCK files such as 'ITRF93'. For the complete
  lists of `built in` body-fixed reference frames refer to the
  appendixes `built in PCK-Based Reference Frames` and High
  Precision Earth Fixed Frames` of this document.

For all other frames the names are not `built into` SPICE.
Instead, these names, as well as the parameters specifying the
frames, are provided via keywords included in a text kernel file.
Text kernel frame definitions cannot overwrite definitions `built
into` SPICE. The `built-in` frames are always accessed first,
making text kernel frames with the same names or IDs invisible to the
Toolkit.
The types of frames defined in text kernels include:

- body-fixed frames based on text or binary PCK data for
  bodies whose rotational data is not yet included in the IAU
  rotational constants reports

- CK-based frames, i.e. frames for which orientation is
  provided in CK files

- Fixed offset frames, i.e. frames for which orientation is
  constant with respect to another frame and is specified as part of
  the frame definition stored in a text kernel. Fixed offset frames
  are also called TK frames.

- Dynamic frames, i.e. frames for which orientation is based
  on dynamic directions computed based on SPICE kernel data (SPKs,
  CK, PCKs), on mathematical models implemented in CSPICE functions,
  or on formulas defined in frame kernels.

- Switch frames, i.e. frames that choose at run time other
  frames with which to align their orientation. Switch frames
  `switch` the base frames they align with as a function of time,
  using a prioritized list of base frames and optional, associated
  time bounds; this list is provided as part of the switch frame
  definition stored in a text kernel.

You can find the names of these frames by examining the text kernel
file that contains the frame definitions. Normally definitions of all
frames specific for a given mission are stored in that mission's
Frames Kernel (FK) file but they can also be provided in the
Instrument Kernels (IK) or any other text kernels. In order to make
frame definitions from the text kernels available to SPICE, these
kernels need to be loaded via a call to
:py:meth:`~spiceypy.spiceypy.furnsh`. For example, to load an FK
named `myframe.tf`, call :py:meth:`~spiceypy.spiceypy.furnsh` as
follows:

.. code-block:: python

         furnsh( "myframe.tf" )


ICRF vs J2000
---------------

| The International Celestial Reference System (ICRS) defines
  coordinate axes that are closely aligned with those of the J2000
  (aka EME2000) reference frame. The International Celestial
  Reference Frame (ICRF) and later versions of it (ICRF1, etc.) are
  realizations of the ICRS. For brevity, we'll simply refer to `the
  ICRF` below.

The rotational offset between the J2000 frame and the ICRS has
magnitude of under 0.1 arcseconds.

Certain JPL data products are referenced to the ICRF or later
versions of it. These include, but are not limited to,

- DE4xx series planetary ephemerides

- Satellite ephemerides compatible with DE4xx planetary
  ephemerides

- Small body ephemerides compatible with DE4xx planetary
  ephemerides

- Orientation of the terrestrial frame ITRF93

- Orientation of the lunar principal axes frame

Rotation models provided by the IAU are referenced to the ICRF.
Modern spacecraft ephemerides and attitude data, other than those for
Earth orbiters, are likely referenced to the ICRF. Users should
consult documentation or data providers to verify this for data sets
of interest.

SPK and binary PCK files produced by NAIF from the data sources
listed above are referenced to the same version of the ICRF as the
corresponding data sources. For historical and backward compatibility
reasons, these data products are labeled as being referenced to the
J2000 frame.

No transformation is required to convert state vectors or orientation
data from the J2000 frame to the ICRF (or later version), if the
vectors or orientation data are computed using SPICE kernels created
from the data sources listed above. For example:

- A call to :py:meth:`~spiceypy.spiceypy.spkezr` with the
  input frame name J2000 will return a state vector referenced to the
  ICRF, if the SPK data are from a JPL planetary ephemeris SPK, or
  from any other SPK in which data are referenced to the ICRF and
  labeled as referenced to the J2000 frame.

- A call to :py:meth:`~spiceypy.spiceypy.pxform` with the
  input `from` frame name J2000 and input `to` frame name
  ITRF93 will return a 3x3 matrix that transforms position vectors
  from the ICRF to the ITRF93 terrestrial frame, if the Earth
  orientation data are provided by a NAIF high-precision, binary
  Earth PCK.

- A call to :py:meth:`~spiceypy.spiceypy.pxform` with the
  input `from` frame name J2000 and input `to` frame name
  IAU_MARS will return a 3x3 matrix that transforms position vectors
  from the ICRF to the Mars body-fixed, body-centered IAU_MARS frame,
  if the orientation data are provided by a NAIF generic text PCK.

- A call to :py:meth:`~spiceypy.spiceypy.pxform` with the
  input `from` frame name J2000 and an input `to` CK frame name
  will return a 3x3 matrix that transforms position vectors from the
  ICRF to the specified CK frame, if the CK data used by this call
  are referenced to the ICRF and labeled as referenced to the J2000
  frame.

SPICE kernel creators intending to support use of data referenced to
the ICRF, as shown above, should write the data without first
converting it to the J2000 frame. Segments of such SPK, CK, or binary
PCK files should indicate the frame is J2000. It is strongly
recommended that kernel creators add comments to the files to explain
the actual characteristics of the data.
SPICE users who export kernel data to non-SPICE file formats may need
to transform the data, depending on the frame to which the SPICE data
are actually referenced (as opposed to the frame to which the kernel
indicates the data are referenced), and depending on the desired
output frame.



Kernels Needed For Computing Frame Transformations
---------------------------------------------------

| In many cases data needed to compute transformation of one frame
  relative to another is stored in SPICE kernels: PCK, CK, FK, and
  even SPK. The appropriate kernels must be loaded for the SPICE
  system to compute a frame transformation from a non-inertial frame
  to any other frame.

The `built in` inertial frames are the only frames the
transformations between which can be computed without loading any
SPICE kernels.

Since the body-fixed frames are tied to the rotation of planets,
satellites, asteroids, etc, the information about how the orientation
of these frames is changing with respect to inertial frames is stored
in SPICE PCK files. It is important to note that although the names
of these frames are `built in` their relationship to inertial
frames is not. This information must be `loaded` into the SPICE
system from a PCK file. Without loading this information you cannot
compute the transformation to or from a body-fixed frame.

As the name suggests, the orientation of CK-based frames is computed
using data provided in CK files and cannot be computed without
loading these. In addition to the CKs, an SCLK kernel establishing
time correlation for the on-board clock that is used to tag data in
the CKs must be loaded to support time conversion between that clock
and ephemeris time.

Because the fixed offset frame definitions stored in text kernels
provide all information needed to determine their orientation
relative to the frame with respect to which they are defined, only
the text kernel containing the definition need be loaded.

Depending on the particular family to which a dynamic frame belongs,
no additional data may be needed in order to compute its orientation,
or one or more types of SPICE kernels, including SPKs, PCKs, CKs, and
SCLK, may have to be loaded.

Data required to compute orientation of switch frames may be any
required to compute orientation of PCK, CK, or TK frames. Data for
dynamic and switch base frames are not required because the
orientation of a switch frame relative to base frames of those types
is the identity. In practice, data sufficient to connect the
orientation of a switch frame's base frames to other frames of
interest are required by most applications.



Creating a Frame Kernel
========================

| To create a frame kernel you will need to understand the SPICE text
  kernel file format described in detail in the Kernel Required
  Reading document, `kernel.req <./kernel.html>`__. When making
  a new frame kernel, make sure that the first line of the file
  contains the proper SPICE file identification word for the FK files
  -- `KPL/FK` -- left-justified, on a line by itself.

You will also need to understand the concept of a frame class.



Frame Classes
--------------

| The method by which a frame is related to some other frame is a
  function of the `class` of the frame. You describe the class of
  a frame with an integer called the frame's `class number.` The
  reference frame classes are enumerated below.

#. Inertial frames. These frames do not rotate with respect to
   the star background. They are the frames in which Newton's laws of
   motion apply. The class number associated with inertial frames is 1.

#. PCK (body-fixed) frames. PCK frames are reference frames
   whose orientation with respect to inertial frames is supplied
   through either binary or text PCK files. To determine a
   transformation to or from a PCK frame, you must load a PCK file
   that describes the orientation of the frame with respect to one of
   the inertial frames `built into` SPICE. The class number
   associated with PCK frames is 2.

#. CK frames. CK frames are reference frames whose orientation
   with respect to some other reference frame is supplied via a SPICE
   C-kernel. The other reference frame may be any of the four classes
   of frames described here. C-kernels use spacecraft clock `ticks`
   as their basic time unit. Consequently you need to load a
   spacecraft clock kernel appropriate for the C-kernel to determine
   the transformation from or to a C-kernel frame. In addition you
   will need to load a PCK, CK, or TK frame kernel if the `other`
   frame belongs to one of these classes. The class number associated
   with CK frames is 3.

#. Fixed offset frames. These frames are also called Text
   Kernel (TK) frames because they have a constant orientation with
   respect to some other reference frame and this orientation is
   included in the frame definition provided in a SPICE text kernel.
   They may be defined relative to a frame of any of the other classes
   of reference frames. The class number associated with TK frames is 4.

#. Dynamic frames. These are time-dependent reference frames
   defined via parameters or formulas specified in a frame kernel. The
   class number associated with dynamic frames is 5.

#. Switch frames. These are time-dependent frames that choose
   at run time other frames with which to align their orientation.
   Switch frames `switch` the base frames they align with as a
   function of time, using a prioritized list of base frames and
   optional, associated time bounds; this list is provided as part of
   the switch frame definition stored in a text kernel. The class
   number associated with switch frames is 6.



Specifying a New Frame
----------------------

| In addition to the data/model needed to specify the orientation of
  a frame with respect to some other reference frame, you must tell
  the SPICE system how to find the data or model. This specification
  requires five pieces of information:

#. the name of the frame,

#. the ID code for the frame,

#. the class number of the frame,

#. the SPK ID code or name for the frame center,

#. the internal ID code used by the class (CLASS_ID) to refer
   to the frame.

The rules for selecting these items are given in the next section,
but for the moment let's assume that the rules have been obeyed and
we have arrived at the following values.

.. code-block:: text

      Frame Name    :    'WALDO'

      Frame ID code :    1234567   (A number guaranteed to be suitable
                                    for private use)
      Frame Class   :          3   (C-kernel)
      Frame Center  :     -10001   (Waldo Spacecraft ID code)
      Frame Class_id:  -10000001   (ID code in C-kernel for Waldo)

The frame kernel that specifies this frame is given below:

.. code-block:: text

      \begindata

         FRAME_WALDO            =  1234567
         FRAME_1234567_NAME     = 'WALDO'
         FRAME_1234567_CLASS    =  3
         FRAME_1234567_CENTER   = -10001
         FRAME_1234567_CLASS_ID = -10000001

      \begintext

Note that single quotes are used to delimit strings in SPICE text
kernels.


Guidelines for Frame Specification
-----------------------------------

|



Selecting a Name
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| The name chosen for a frame must not exceed 26 characters taken
  from the set including uppercase letters, numbers, underscore, and
  plus and minus signs. It should have some mnemonic value so that
  users can recognize what the name means. Finally, it should not be
  the name of one of the `built in` frames listed above or the
  name of any other frame you wish to specify. If you try to use a
  `built in` name, the frame subsystem will ignore your frame
  specification. In the example given above, we chose the name
  'WALDO' for the name of our reference frame. If `Waldo` would be
  a lander and would need to specify a local level frame at its
  landing site, we could have named that frame 'WALDO_LOCAL_LEVEL'. A
  good name for a frame associated with the camera flown on
  `Waldo` would be 'WALDO_CAMERA'.



Selecting a Frame ID
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| What you choose for a frame ID depends upon the class of the frame.

If the class is CK, you may use the same ID as you use for the
CLASS_ID. In the previous example, we selected the Frame ID to be

.. note::

    Since our example frame above is of class 3, a CK frame, we
    would normally use the same number for the frame ID as we used for
    the class ID. However, in this example, we have chosen a different
    value to illustrate the connection between the frame ID and the
    variables needed to define the frame.


For TK frames, the frame and class IDs must be identical. For TK frames
associated with an instrument, the instrument ID is used for
both frame ID and class ID. For topocentric TK frames at tracking
station sites, both frame ID and class ID are created by
`combining` the ID of the body on which the station is located
with the station number (for example frame and class ID 1399012 is
used for `DSS-12`, with the formula used to arrive at this ID
being 1000000 + `Earth ID`*1000 + `station ID`.) For local
level and surface fixed TK frames at a landing site, both frame ID
and class ID are based on the ID of the lander (for example frame and
class ID of -222999 would be the natural choice for the lander with
ID -222.)

If the frame is a PCK frame or a dynamic frame and you are working
without consultation with NAIF, select an integer in the range from
1400000 to 2000000.



Selecting the Class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| This is usually the easiest part of specifying a frame. Presumably
  you know how the orientation of the frame with respect to some
  other frame will be computed. Simply choose the appropriate class
  number. In the example above, the class number is 3 because we are
  defining a CK-based frame.



Selecting the Center
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| A frame is used to specify the orientation of some object. The
  frame consists of a set of coordinate axes relative to some point
  -- the origin of the reference frame. When viewed from some other
  frame the axes rotate about the origin. The origin about which the
  rotation takes place is the center of the frame. For body-fixed
  frames this is the center of the body to which they are fixed. For
  C-kernel frames the center is often the spacecraft whose
  orientation is provided by the C-kernel. Simply find the SPK ID
  code or name for the object to which the frame is attached and use
  that as the value for the center. In our example, the SPK ID code
  for the `Waldo` spacecraft is -10001.

Note that this center ID is used to look up the position of the frame
origin when SPICE computes frame orientation adjusted for light time.
Therefore, only centers for which supporting SPK data are expected to
be available should be picked. It is usually an issue only for TK and
CK frames associated with instruments because the positions of
instruments are rarely available in SPKs. To get around the need to
provide the instrument positions, it is appropriate to specify the ID
of the spacecraft on which an instrument is mounted as the center of
a TK or CK frame associated with it.



Selecting a Class ID
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| A frame's `CLASS_ID` is an integer used internally by CSPICE
  software. It is the integer code used by the CSPICE reference frame
  subsystem to look up reference frame information.

If your frame is a PCK class frame the CLASS_ID is the ID code for
the body for which rotation constants are provided in the text PCK
file or the ID associated with the orientation data provided in the
binary PCK file.

If your frame is a CK class frame, the CLASS_ID is the ID code used
in the C-kernel to describe the orientation of the spacecraft.

If the frame is a TK frame, the class ID must match the frame ID.

If the frame is a dynamic frame, the class ID must match the frame
ID.

If the frame is a switch frame, it is recommended that the class ID
match the frame ID.



Frame IDs Reserved for Public Use
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| The range 1400000 to 2000000 has been set aside by NAIF as ranges
  of Frame IDs that can be used freely by SPICE users without fear of
  conflict with `officially recognized` frames. However, if you
  and a colleague plan to create several such frames, you will need
  to coordinate your work to ensure that your definitions are not in
  conflict with one another.



Why have a Frame ID and a Class ID?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| When the CSPICE software receives a request to compute a frame
  transformation, it first translates the name of the frame to the
  corresponding frame ID. There is a one to one correspondence
  between frame names and frame IDs. Once the frame ID is in hand,
  the class of the frame can be located and an appropriate subsystem
  identified for carrying out the initial computations needed to
  construct a frame transformation matrix. However, the frame
  subsystem evolved to unify several distinct reference frame
  systems. In each of these systems, reference frames are identified
  by integer codes. Unfortunately, since these subsystems evolved
  independently, the numeric codes used to identify the reference
  systems overlapped from one system to the next. Moreover, to
  support backward compatibility, NAIF was not free to change the
  numeric codes used by the various systems or the meaning of the
  frame codes that were already present in existing data products.

To support existing data products and allow extension of the SPICE
system, NAIF needed to associate the old ID code with the new frame
ID. The CLASS_ID fills this role. When the frame is identified, the
ID code suitable for the frame class is located and passed onto the
frame's class so that the initial portion of the frame transformation
can be carried out.



Putting the Pieces Together
-----------------------------

| Once you've determined the name, ID code, center, class and class
  ID of your frame, you create the frame specification by filling in
  the frame template below. This should be stored in a text kernel
  called a Frame Specification Kernel or Frames Kernel (FK).

.. code-block:: text

      FRAME_<name>             = <ID code>
      FRAME_<ID code>_NAME     = '<name>'
      FRAME_<ID code>_CLASS    = <class>
      FRAME_<ID code>_CLASS_ID = <classid>
      FRAME_<ID code>_CENTER   = <center>

The example we used for the frame 'WALDO' illustrates this.

.. code-block:: text

      \begindata

         FRAME_WALDO            =  1234567
         FRAME_1234567_NAME     = 'WALDO'
         FRAME_1234567_CLASS    =  3
         FRAME_1234567_CENTER   = -10001
         FRAME_1234567_CLASS_ID = -10000001

      \begintext

Once you've completed the frame specification you tell the SPICE
system about the frame by `loading` the frame kernel that contains
it. As with all text kernels, you load it via the routine
:py:meth:`~spiceypy.spiceypy.furnsh`. For example if the frame
kernel containing your frame specification is contained in the file
`myframe.tf` you load the kernel via the call


.. code-block:: python

         furnsh( "myframe.tf" )



Connecting an Object to its Body-fixed Frame
---------------------------------------------

| Every extended object has both a position and orientation in space.
  The SPICE ephemeris subsystem (SPK) allows you to specify the
  location of such an object. The frame subsystem allows you to name
  the body-fixed frame that describes the orientation of the object,
  and to retrieve the orientation of the frame relative to some other
  frame as a function of time. Given the name or SPK ID code
  associated with an object we can locate its position through the
  SPK subsystem. Unfortunately, the body-fixed frame of the object
  cannot always be determined from the object's name or ID code. For
  example, we have already mentioned that there are two `built in`
  reference frames that describe the orientation of the Earth:
  'IAU_EARTH' and 'ITRF93'. For other objects, such as the asteroid
  Simbad, there is no `built in` frame associated with the object.
  The body-fixed frame of Simbad must be defined through a text
  kernel. In both cases, the connection between the object and its
  body-fixed frame needs to be supplied via a kernel pool variable.
  There are two ways to do this.

.. code-block:: text

      OBJECT_<name or spk_id>_FRAME =  '<frame name>'

or

.. code-block:: text

      OBJECT_<name or spk_id>_FRAME =  <frame ID code>

You may use the ID codes for either the object, the frame or both. As
example, four of the following assignments could serve to connect the
Earth with the 'ITRF93' frame.

.. code-block:: text

      OBJECT_399_FRAME   =  13000
      OBJECT_399_FRAME   = 'ITRF93'
      OBJECT_EARTH_FRAME =  13000
      OBJECT_EARTH_FRAME = 'ITRF93'

Note: if you use the name of either the object or frame, you must use
upper case letters.
Of these four means of specifying an object's body-fixed frame the
second (OBJECT_399_FRAME = 'ITRF93') is the most robust.

For the sun, the planets and their satellites the frame subsystem
maintains a default connection between the object and its body-fixed
frame `built into` SPICE. The complete list of `built in`
body-fixed frames is provided in the `built in PCK-Based IAU
Body-Fixed Reference Frames` appendix of this document.



The rest of the frame information
----------------------------------

| The information supplied in the frame specification tells the SPICE
  system where to look for a particular frame model. However, the
  specification alone doesn't tell the SPICE system how to actually
  transform from the specified frame to some other frame of interest.
  To do this you need to supply other information. How this
  information is supplied depends upon the class of the frame.



Inertial Frames
===============

| Inertial frames are `built into` the SPICE system via the
  routine chgirf\_. Only the frames defined in that routine are
  available as inertial (class 1) frames. It is not possible to
  override these definitions.

It is possible to create aliases for built-in inertial frames. For
example you might define EME2000 as another name for the J2000 frame.

See the appendix containing frame definition examples for information
on how to create a frame alias using a TK frame.



PCK Frames
===========

| If you specify a PCK frame, you will need to load either a text or
  binary PCK file for the body with which the frame is associated.
  The construction of PC kernels is discussed in the SPICE document
  PCK Required Reading (`pck <./pck.html>`__.)



CK Frames
=========

| If a frame is defined as a CK frame, you will need both a C-kernel
  for the structure identified by the FRAME\_..._CLASS_ID variable
  and an SCLK kernel for converting ephemeris time to the `ticks`
  used to represent time in the C-kernel. Both the C-kernel(s) and
  SCLK kernel must be loaded prior to attempting to use the CK frame.



SCLK and SPK ID codes
----------------------

| For many C-kernels, the spacecraft clock and spacecraft ID codes
  can be determined by performing an integer division of the C-kernel
  ID code by 1000. However, under some circumstances this numerical
  correspondence between C-kernel ID code and the associated SCLK or
  spacecraft ID may break down. When the numerical relationship fails
  you need to tell the SPICE system the ID code of the SCLK or
  spacecraft via two kernel pool variables.

.. code-block:: text

      CK_<ck_ID code>_SCLK = <ID code of SCLK>
      CK_<ck_ID code>_SPK  = <SPK ID code>

These variables are normally placed in either the SCLK kernel or in
the frame specification kernel (FK).
To illustrate how you would create a C-kernel frame, we shall suppose
that we have a C-kernel for structure -100001 aboard the fictional
spacecraft `Waldo` which has ID code -1001. Moreover we shall
assume that the clock ID appropriate for this structure is -1002.
Below is a frame specification together with the CK\_..._SCLK and
CK\_..._SPK variable definitions for the 'WALDO' frame.

.. code-block:: text

      \begindata

         FRAME_WALDO            = -100001
         FRAME_-100001_NAME     = 'WALDO'
         FRAME_-100001_CLASS    = 3
         FRAME_-100001_CLASS_ID = -100001
         FRAME_-100001_CENTER   = -1001

         CK_-100001_SCLK        = -1002
         CK_-100001_SPK         = -1001

      \begintext



TK Frames
=========

| The relationship between a constant offset Text Kernel (TK) frame
  and the frame it is offset from is given via a text kernel that can
  be loaded via the kernel pool routine
  :py:meth:`~spiceypy.spiceypy.furnsh`. The first five kernel pool
  variables required for TK frame specification are the same as for
  any other frame defined via a text kernel:

.. code-block:: text

      FRAME_<name>             = <ID code>
      FRAME_<ID code>_NAME     = '<name>'
      FRAME_<ID code>_CLASS    = 4
      FRAME_<ID code>_CLASS_ID = <ID code>
      FRAME_<ID code>_CENTER   = <center>

You need to supply information that indicates the frame, RELATIVE,
from which the TK frame is offset. It is done using this kernel pool
variable:

.. code-block:: text

      TKFRAME_<frame>_RELATIVE = '<name of relative frame>'

where `frame` is the ID code or name you used in the frame
specification.
Because the rotation from the TK frame to the RELATIVE frame is fixed
(time invariant) it can be specified in the FK along with the frame
specification information described above. This rotation data can be
provided in any of three ways:

#. as a 3 by 3 matrix, M, that converts vectors from the TK
   frame to the RELATIVE frame by left multiplication

.. code-block:: text

                  V_relative = M * V_tkframe

#. as a set of 3 Euler angles and axes that can be used to
   produce M

#. as a SPICE-style quaternion representing M.

You let the frame subsystem know which method you've chosen for
representing the rotation via the kernel pool variable

.. code-block:: text

      TKFRAME_<frame>_SPEC.

To use a matrix to define the rotation, use the assignment:

.. code-block:: text

      TKFRAME_<frame>_SPEC = 'MATRIX'

To define the rotation via three Euler angles, use the assignment:

.. code-block:: text

      TKFRAME_<frame>_SPEC = 'ANGLES'

To define the rotation via a SPICE-style quaternion, use the
assignment:

.. code-block:: text

      TKFRAME_<frame>_SPEC = 'QUATERNION'

Depending upon the value of the `SPEC` variable, you need to supply
one of the following sets of kernel pool variables.


Defining a TK Frame Using a Matrix
-----------------------------------

| If you've chosen to define the rotation using a matrix, supply the
  matrix using the kernel pool variable assignment below:

.. code-block:: text

      TKFRAME_<frame>_MATRIX = ( matrix_value[0][0],
                                 matrix_value[1][0],
                                 matrix_value[2][0],
                                 matrix_value[0][1],
                                 matrix_value[1][1],
                                 matrix_value[2][1],
                                 matrix_value[0][2],
                                 matrix_value[1][2],
                                 matrix_value[2][2]  )

For example, if the matrix defining your TK frame is

.. code-block:: text

      0.4   -0.6   0.0
      0.6    0.4   0.0
      0.0    0.0   1.0

and the ID code you've selected for the frame is 1234567, then you
would supply the following information in a text kernel.

.. code-block:: text

      TKFRAME_1234567_SPEC   = 'MATRIX'

      TKFRAME_1234567_MATRIX = (  0.4
                                  0.6
                                  0.0
                                 -0.6
                                  0.4
                                  0.0
                                  0.0
                                  0.0
                                  1.0 )



Defining a TK Frame Using Euler Angles
----------------------------------------

| If you've chosen to define a TK frame as a sequence of three Euler
  angle rotations about specified coordinate axes, you need to supply
  the following pieces of information:

#. The values of the three Euler angles;

#. The axes about which the Euler rotations are performed;

#. The units associated with the three Euler angles. The
   recognized units are: 'DEGREES', 'RADIANS', 'ARCSECONDS',
   'ARCMINUTES' 'HOURANGLE', 'MINUTEANGLE', 'SECONDANGLE'.

This information is supplied to the SPICE system using the kernel
pool variables shown below.

.. code-block:: text

      TKFRAME_<frame>_ANGLES = ( angle_1, angle_2, angle_3 )
      TKFRAME_<frame>_AXES   = ( axis_1,  axis_2,  axis_3  )
      TKFRAME_<frame>_UNITS  = 'units_of_angles'

The units must be from the list given above. The axes must be chosen
from the set of integers 1,2,3 where 1 stands for the x-axis, 2 for
the y-axis, and 3 for the z-axis. If M is the matrix that converts
vectors relative to the TK frame to the RELATIVE frame by left
multiplication, then the angles and axes must satisfy the following
relationship:

.. code-block:: text

      M = [angle_1]      [angle_2]      [angle_3]
                   axis_1         axis_2         axis_3


where the symbol

.. code-block:: text

      [ A ]
           i

stands for a rotation by the angle A about the i'th axis.

.. code-block:: text

      +-                     -+
      |   1       0      0    |
      |   0     cos A   sin A |   =  [ A ]
      |   0    -sin A   cos A |           1
      +-                     -+

      +-                     -+
      |  cos A    0    -sin A |
      |   0       1      0    |   =  [ A ]
      |  sin A    0     cos A |           2
      +-                     -+

      +-                     -+
      |  cos A   sin A   0    |
      | -sin A   cos A   0    |   =  [ A ]
      |   0       0      1    |           3
      +-                     -+

This method of definition is particularly well suited for defining
topocentric frames on the surface of the Earth. For example, suppose
you have an SPK (ephemeris) file that specifies the location of some
surface point on the Earth, and that the SPK ID code of this point is
Moreover suppose you have the geodetic co-latitude (COLAT)
and longitude (LONG) measured in degrees for this point. (Note that
the co-latitude is the complement of latitude: latitude + co-latitude
= 90 degrees.)
Given this information we can easily define a topocentric reference
frame at the point such that the x-axis points north along the local
meridian, the y-axis points west along the local latitude and the
z-axis points up from the reference spheroid.

The transformation from Earth body-fixed frame to topocentric frame
is given by

.. code-block:: text

      BF2TP = [180] [COLAT] [LONG]
                   3       2      3

Consequently the transformation from the topocentric frame to the
body-fixed frame is given by

.. code-block:: text

      M = TP2BF = [-LONG] [-COLAT] [180]
                         3        2     3

Let 1234567 be the ID code for the topocentric frame; let the name of
this frame be 'MYTOPO'; and define this relative to the IAU frame for
the Earth (one of the `built in` frames). The topocentric frame at
the ephemeris point 399100 is specified as shown below:

.. code-block:: text

      \begindata

         FRAME_MYTOPO             = 1234567
         FRAME_1234567_NAME       = 'MYTOPO'
         FRAME_1234567_CLASS      = 4
         FRAME_1234567_CLASS_ID   = 1234567
         FRAME_1234567_CENTER     = 399100

         TKFRAME_1234567_SPEC     = 'ANGLES'
         TKFRAME_1234567_RELATIVE = 'IAU_EARTH'
         TKFRAME_1234567_ANGLES   = ( <-long>, <-colat>, 180 )
         TKFRAME_1234567_AXES     = (       3,        2,   3 )
         TKFRAME_1234567_UNITS    = 'DEGREES'

      \begintext

As we'll see a bit later, we can make a more flexible definition for
this topocentric frame.


Defining a TK Frame Using a SPICE-style Quaternion
---------------------------------------------------

| If you've chosen to define a TK frame using a SPICE-style
  quaternion, supply the quaternion using the kernel pool variable
  assignment below:

.. code-block:: text

      TKFRAME_<frame>_Q = ( q_0, q_1, q_2, q_3 )

where component zero is the so-called `real` component of the
quaternion (the `cosine` component of the quaternion). The last 3
components (components 1 through 3) are the `axis` components of
the quaternion -- the i, j, and k components respectively of the
quaternion. The quaternion must be a unit quaternion.

.. code-block:: text

           2        2        2        2
      (q_0)  + (q_1)  + (q_2)  + (q_3)  = 1

A more detailed discussion of quaternions is available in the
reference document `Rotations Required Reading`
(`rotation.req <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/rotation.html>`__), and in a `Quaternions
White Paper` available from NAIF.


Gaining Flexibility via TK Frames
-----------------------------------

| The use of non-inertial frames gives you an easy means of creating
  ephemerides for points on the surface of a body such as the Earth,
  Moon or Mars. The ephemeris is simply the body-fixed location of
  the object relative to a body-fixed frame for the same object.
  However, the model used to relate the body-fixed frame to other
  reference frames may not be fixed. Indeed, for the Earth there are
  several different methods with varying degrees of accuracy that
  give the orientation of the Earth with respect to inertial space.
  Each of these different realizations may have a different frame ID
  code. This ability to `plug in` different orientations is one of
  the strengths of the SPICE system. However, if you create an
  ephemeris relative to one of these specific models, you won't be
  able to use it unless you've loaded the correct model. To make the
  ephemeris usable regardless of the orientation model you happen to
  have at your disposal, you should define the body-fixed ephemeris
  relative to a TK frame. Then define the TK frame so that rotation
  from the TK frame to the PCK frame is the identity matrix. For
  example, you can define a lunar body-fixed frame as shown below.

.. code-block:: text

      \begindata

         FRAME_MOONFIXED          = 3010000
         FRAME_3010000_NAME       = 'MOONFIXED'
         FRAME_3010000_CLASS      = 4
         FRAME_3010000_CLASS_ID   = 3010000
         FRAME_3010000_CENTER     = 301

         TKFRAME_3010000_SPEC     = 'MATRIX'
         TKFRAME_3010000_RELATIVE = '<name of base frame>'
         TKFRAME_3010000_MATRIX   = ( 1,
                                      0,
                                      0,
                                      0,
                                      1,
                                      0,
                                      0,
                                      0,
                                      1 )

      \begintext

By editing this definition you can make the MOONFIXED frame be the
IAU MOON frame or some other model if one is available. Or you can
create several such definitions and, at run-time, load the file that
best fits your current environment.
Using this indirect method of defining the various frames for which
more than one orientation model may be available, you can avoid
limiting how various kernels can be used.



Dynamic Frames
=================

| In SPICE documentation, the term `dynamic frame` designates a
  time-dependent reference frame defined via a frame kernel.

A `parameterized dynamic frame` is a dynamic frame defined by a
formula implemented in CSPICE code and having user-selectable
parameters set via a frame kernel. The formula defining a dynamic
frame may rely on data from other SPICE kernels, for example state
vectors provided by SPK files or rotation matrices from C-kernels or
PCK files.

An example of a parameterized dynamic frame is a nadir-pointing
reference frame for a spacecraft orbiting a planet, where the
spacecraft's nadir direction and velocity vector define the frame.
Using a frame kernel, a CSPICE user may specify the planet and
spacecraft, the relationship between the nadir and velocity vectors
and the frame's axes, and a small set of additional parameters
required to define the frame.

Currently parameterized dynamic frames are the only type of dynamic
frame supported by CSPICE. Other types of dynamic frames, such as
frames defined by complete formulas (as opposed to parameters)
provided in frame kernels, may be implemented in future versions of
CSPICE.

Below we'll discuss the various types of supported dynamic frames,
how to create frame kernels that define dynamic frames, and dynamic
frame implementation considerations. The appendix `Frame Definition
Examples` contains frame definition templates for a variety of
popular dynamic frames.



Parameterized Dynamic Frame Families
=====================================

| The `family` to which a parameterized dynamic frame belongs
  indicates the underlying mathematical formula by which the frame is
  defined. Currently there are six parameterized dynamic frame
  families:

- Two-vector frames: a reference frame is defined by two
  vectors. The first vector is parallel to one axis of the frame; the
  component of the second vector orthogonal to the first is parallel
  to another axis of the frame, and the cross product of the two
  vectors is parallel to the remaining axis.

- Mean equator and equinox of date frames: these use
  mathematical precession models to define orientation of a body's
  equatorial plane and location of the frame's x-axis. Currently
  these frames are supported only for the earth.

- True equator and equinox of date frames: these use
  mathematical precession and nutation models to define orientation
  of a body's equatorial plane and location of the frame's x-axis.
  Currently these frames are supported only for the earth.

- Mean ecliptic and equinox of date frames: these use
  mathematical precession and mean obliquity models to define
  orientation of a body's orbital plane and location of the frame's
  x-axis. Currently these frames are supported only for the earth.

- Euler frames: polynomial coefficients, a reference epoch,
  and an axis sequence are used to specify time-dependent Euler
  angles giving the orientation of the frame relative to a second,
  specified frame as a function of time.

- Product frames: these define the orientation of a frame
  relative to a base frame as the product of a specified sequence of
  frame transformations. All of the factor transformations must be
  computable by CSPICE.



Notation
--------

| A lower case letter \`x' is used to designate the cross product
  operator, as in

.. code-block:: text

      C = A x B

Double vertical bars bracketing the name of a vector indicate the
norm of the vector:

.. code-block:: text

      ||A||

Throughout this discussion we'll use text enclosed in angle brackets
to indicate values to be filled in by the creator of a frame kernel.
Examples are:

.. code-block:: text

         Token                 Replacement Value

   -------------            -----------------------------------------
      <vec_ID>                 'PRI' or 'SEC' [See discussion of
                               two-vector frames below.]
      <frame_name>             SPICE frame name, .e.g. 'J2000'
      <frame_ID>               Integer frame ID code
      <observer_ID>            NAIF integer ID for the observing body

    <aberration correction>  String indicating aberration correction,
                               e.g.:  'NONE', 'LT', 'XLT', 'LT+S'



Required Keywords for Parameterized Dynamic Frames
---------------------------------------------------

| All parameterized dynamic frame kernel definitions contain the
  assignments shown here:

.. code-block:: text

      FRAME_<frame_name>                  =  <frame_ID>
      FRAME_<frame_ID>_NAME               =  <frame_name>
      FRAME_<frame_ID>_CLASS              =  5
      FRAME_<frame_ID>_CLASS_ID           =  <frame_ID>
      FRAME_<frame_ID>_CENTER             =  <center_ID>

      FRAME_<frame_ID>_RELATIVE           =  <base_frame_name>
      FRAME_<frame_ID>_DEF_STYLE          =  'PARAMETERIZED'
      FRAME_<frame_ID>_FAMILY             =  <frame_family>

These first five of the assignments are common to all CSPICE frame
definitions; the class code 5 indicates that the frame is dynamic.
See the section `Guidelines for Frame Specification` in the
chapter `Creating a Frame Kernel` above for a detailed discussion
of these assignments.
The sixth assignment (for keyword FRAME\_<frame_ID>_RELATIVE) is the
`base frame` specification; this indicates the frame the
transformation defined by the frame kernel `maps to`: starting
with an epoch ET and a state vector S specified relative to the
defined frame

.. code-block:: text

      <frame name>

the frame definition determines the 6x6 state transformation matrix
XFORM such that the product

.. code-block:: text

      XFORM * S

yields the equivalent state specified relative to the base frame at
ET.
The seventh assignment (for keyword FRAME\_<frame_ID>_DEF_STYLE) is
used to simplify future implementation of other dynamic frame
definition styles. Only the value

.. code-block:: text

      'PARAMETERIZED'

is currently supported.
The last assignment indicates the frame family. The possible values
are

.. code-block:: text

      'TWO-VECTOR'
      'MEAN_EQUATOR_AND_EQUINOX_OF_DATE'
      'TRUE_EQUATOR_AND_EQUINOX_OF_DATE'
      'MEAN_ECLIPTIC_AND_EQUINOX_OF_DATE'
      'EULER'

Additional, required frame kernel assignments are a function of the
family to which a dynamic frame belongs. These are discussed below.


Conditional Keywords for Parameterized Dynamic Frames
------------------------------------------------------

|



Rotation State
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| A parameterized dynamic frame definition can specify a frame's
  `rotation state` as `rotating` or `inertial.` Rotating
  frames are nominally time-dependent, although it is possible for
  them to be constant (an Euler frame with all Euler angles constant
  is an example).

When a parameterized dynamic frame is specified as `inertial,` the
derivative with respect to time of the transformation between the
frame and any inertial frame, for example the J2000 frame, is zero.
The rotation between the frame and any inertial frame is still
treated as time-dependent. For such a frame F, the call

.. code-block:: python

      xform = sxform( "F", "J2000", t )

yields a 6x6 state transformation matrix `xform` having the
structure

.. code-block:: text

      +-----+-----+
      | R(t)|  0  |
      +-----+-----+
      |  0  | R(t)|
      +-----+-----+

where R(t) is the 3x3 rotation matrix that transforms vectors from
frame F to the J2000 frame at time `t`. By contrast, when the
rotation state of F is `rotating,` `xform` has the structure

.. code-block:: text

      +-----+-----+
      | R(t)|  0  |
      +-----+-----+
      |dR/dt| R(t)|
      +-----+-----+

So, when the rotation state of frame F is `inertial,` velocities
are transformed from frame F to J2000 by left-multiplication by R(t)
the time derivative of the rotation from F to J2000 is simply
ignored.
Normally the inertial rotation state makes sense only for slowly
rotating frames such as the earth mean equator and equinox of date
frame.

A parameterized dynamic frame's rotation state is specified via the
assignment

.. code-block:: text

      FRAME_<frame_ID>_ROTATION_STATE     =  <state>

where

.. code-block:: text

      <state>

is one of

.. code-block:: text

      'ROTATING'
      'INERTIAL'

For frames belonging to the parameterized dynamic frame families

.. code-block:: text

      'MEAN_EQUATOR_AND_EQUINOX_OF_DATE'
      'TRUE_EQUATOR_AND_EQUINOX_OF_DATE'
      'MEAN_ECLIPTIC_AND_EQUINOX_OF_DATE'

either the rotation state must be specified, or the frame must be
frozen (see `Frozen Frames` below).
For two-vector and Euler frames, the rotation state specification is
optional; these frames are considered to be rotating by default.

When the rotation state of a parameterized frame is specified, the
frame cannot be frozen; these options are mutually exclusive.



Freeze Epoch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| A parameterized dynamic frame definition can specify a frame as
  `frozen` at a particular epoch. The rotation between a frozen
  frame and its base frame is constant; the derivative with respect
  to time of this rotation is zero.

A frozen frame whose base frame is time-varying is still
time-varying: it is the relationship between the frozen frame and the
base frame that is time-independent.

A frame is declared frozen by specifying a `freeze epoch.` This is
done via the assignment:

.. code-block:: text

      FRAME_<frame_ID>_FREEZE_EPOCH       =  <time_spec>

where

.. code-block:: text

      <time_spec>

is a TDB calendar date whose format conforms to the SPICE text kernel
date format specification. These dates

- are unquoted

- start with the character

.. code-block:: text

               @

- contain no embedded blanks

An example of a template for these calendar strings is

.. code-block:: text

      @YYYY-MON-DD/HR:MN.SEC.###

Literal examples include

.. code-block:: text

      @7-MAR-2005
      @March-7-2005-3:10:39.221
      @2005-MAR-07/3:10:39.221

Note that unlike time strings supported by the CSPICE function
:py:meth:`~spiceypy.spiceypy.str2et`, time system tokens such as

.. code-block:: text

      UTC
      TDT
      TDB

are not supported; times are always assumed to be TDB.
For frames belonging to the parameterized dynamic frame families

.. code-block:: text

      'MEAN_EQUATOR_AND_EQUINOX_OF_DATE'
      'TRUE_EQUATOR_AND_EQUINOX_OF_DATE'
      'MEAN_ECLIPTIC_AND_EQUINOX_OF_DATE'

either the frame must be frozen or the rotation state must be
specified, (see `Rotation State` above).
For two-vector and Euler frames, the freeze epoch specification is
optional; these frames are considered to be time-varying relative to
their base frames by default.

When a parameterized frame is frozen, the rotation state of the frame
cannot be specified; these options are mutually exclusive.



Two-Vector Frames
=================

| Two-vector frames use two user-specified, non-parallel vectors to
  define the mutually orthogonal axes of a right-handed reference
  frame.

In a two-vector frame definition, one defining vector is parallel to
a specified axis of the reference frame; this vector is called the
`primary vector.` The other vector, called the `secondary
vector,` defines another axis: the component of the secondary vector
orthogonal to the primary vector is parallel to a specified axis of
the reference frame. The secondary vector itself need not be, and
typically is not, aligned with an axis of the defined frame.

Below, we'll call the primary and secondary defining vectors PRI and
SEC, and we'll name the axes of the right-handed frame X, Y, and Z.
The unit +Z vector is the cross product of the unit +X and +Y vector.

In a two-vector frame definition, the vectors PRI and SEC are
specified geometrically; for example, PRI could be the position of
the earth relative to a spacecraft, and SEC could be defined by the
right ascension and declination of a given star in a specified
reference frame.

In a frame kernel, the vectors PRI and SEC are associated with two
members of the set of unit vectors

.. code-block:: text

      { X, -X, Y, -Y, Z, -Z }

An example: in this case PRI is associated with -Z and SEC is
associated with +X. SEC itself is not parallel to the X axis, but the
component of SEC orthogonal to PRI points in the +X direction.
The diagram below shows the relationship between PRI, SEC, X, Y, and
Z:

.. code-block:: text


         Component of SEC orthogonal to PRI
                         |
                         |      ^
                         v      |
                       <-----+--+
                        \    |  |
                         \   +--+
                          \     |
                       SEC \    |  +Z  = - PRI / ||PRI||
                            \   |
                             \  |
                              \ +--+
                               \|  |
      +X = Y x Z  <---------+---+--+
                           /   /|
                          +---/ |
                             /| /
                            / |/|
                           /  + |  -Z  =   PRI / ||PRI||
                          /     |
                         /      |
                        v       v  PRI

               Z x SEC
        +Y = -----------
             ||Z x SEC||

         =   Z x X

By defining PRI and SEC we can create a concrete frame definition.
Continuing the above example, we can define a nadir-pointing frame
for the Mars Global Surveyor (MGS) spacecraft as follows:

.. code-block:: text

      PRI  =  Vector from MGS to nearest point on Mars reference
              ellipsoid

      Z    =  -PRI / ||PRI||

      SEC  =  Inertially referenced velocity of MGS relative to Mars

      Y    =  Z x SEC / ||Z x SEC||

      X    =  Y x Z

For this nadir-pointing frame, -Z is the nadir direction, X points
roughly in the direction of the inertially referenced spacecraft
velocity, and Y is aligned with the orbital angular velocity vector.
By converting the above definition into the frame kernel
`keyword=value` format, we can make the definition usable by the
CSPICE system. Above, for brevity, we've glossed over a few aspects
of the vector definitions. Below we'll discuss in detail all of the
elements of two-vector frame specifications.



Defining a Two-Vector Frame in a Frame Kernel
---------------------------------------------


Kernel Availability
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| In the following discussion, for brevity, we will use the term
  `computable` to describe frames whose definitions are known to
  CSPICE and for which kernels have been loaded sufficient to enable
  computation of the transformations between these frames and their
  base frames.

We'll also call a frame transformation between frames F1 and F2
`computable` if both frames F1 and F2 are computable and kernels
have been loaded sufficient to enable computation of the
transformation between F1 and F2. For example, the transformation
between the J2000 and IAU_TITAN frames is computable once a PCK
containing rotational elements for TITAN has been loaded.



Specifying the Base Frame
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| When a two-vector frame F is defined with a base frame F_BASE, and
  when the necessary kernels are loaded, the transformation between F
  and F_BASE (in both directions) becomes computable by the CSPICE
  frame subsystem. In addition, for any frame F2 such that the
  transformation between F2 to F_BASE is computable, the
  transformation from F2 to F (in both directions) becomes
  computable.

For a two-vector frame, the base frame may be any frame F_BASE such
that the transformation between F_BASE and the J2000 reference frame
is computable at the time the two-vector frame definition is
referenced.

Normally for two-vector frames the base frame should be set to
'J2000'; this choice yields optimal run-time efficiency. The
assignment is made as follows.

.. code-block:: text

      FRAME_<frame_ID>_RELATIVE           =  'J2000'

Base frame specifications are part of the two-vector frame definition
because the base frame can be used to control how CSPICE chains
together two-vector frames with other frames. However, from a
mathematical point of view, two-vector frames are fully defined
without reference to a base frame. For example, suppose the
two-vector frame F1 is defined by the earth-moon position vector and
the earth-sun position vector, and the base frame for F1 is
IAU_EARTH. Suppose that the two-vector frame F2 is defined by the
same vectors and that the base frame of F2 is J2000. Then, ignoring
small round-off errors, the transformation between F1 and F2 is the
identity transformation.
Base frames should not be confused with other frames occurring in
two-vector frame definitions: constant vectors and velocity vectors
have associated frames which are also specified by keyword
assignments. See the discussion below under the heading `Constant
Vectors` and `Velocity Vectors` for details.



Specifying the Frame Family
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Definitions of two-vector frames include the frame family
  specification:

.. code-block:: text

      FRAME_<frame_ID>_FAMILY             =  'TWO-VECTOR'

Further assignments (discussed below) define the primary and
secondary vectors and relate these vectors to the frame's axes.


Specifying the Rotation state or Freeze Epoch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| These specifications are optional for two-vector frames. See the
  section above titled `Conditional Keywords for Parameterized
  Dynamic Frames` for details.



Specifying the Angular Separation Tolerance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| This specification applies only to two-vector frames and is
  optional. To diagnose near-degenerate geometry, specifically cases
  where the defining vectors have angular separation too close to
  zero or pi radians, users can specify a limit on these angular
  separations. This is done via the keyword assignment

.. code-block:: text

      FRAME_<frame_ID>_ANGLE_SEP_TOL      = <tolerance>

where <tolerance> is the separation limit in radians. If the angular
separation of the defining vectors differs from zero or pi radians by
less than the specified tolerance, an error will be signaled at run
time.
When a two-vector frame definition omits specification of an angular
separation tolerance, CSPICE uses a default value of one milliradian.



Frame Axis Labels
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| The primary defining vector is associated with a frame axis via the
  assignment

.. code-block:: text

      FRAME_<frame_ID>_PRI_AXIS           = <label>

Here

.. code-block:: text

      <label>

may be any of

.. code-block:: text

      { 'X',  '-X',  'Y',  '-Y',  'Z',  '-Z' }

Blanks and case in the label are not significant. Unsigned axis
designations are treated as positive; optionally '+' signs may be
used to prefix positive axis designations. The primary vector is
aligned with the indicated axis and has the sense indicated by the
implied or explicit sign.
The secondary defining vector is associated with a frame axis via the
assignment

.. code-block:: text

      FRAME_<frame_ID>_SEC_AXIS           = <label>

where the axis labels are as above. The assignment means that the
component of the secondary vector orthogonal to the primary vector is
aligned with the indicated axis and has the sense indicated by the
implied or explicit sign.


Vector Specifications
------------------------

| The vectors used to define a two-vector frame are specified by
  geometric means. Each defining vector may be any of:

- The position of one ephemeris object relative to another

- The vector from an observer to the nearest point on an
  extended body to the observer

- The velocity of one ephemeris object relative to another in
  a specified reference frame

- A constant vector in a specified reference frame

The frames (explicit or implicit) associated with the two defining
vectors need not match each other or the base frame. CSPICE will map
the defining vectors to a common frame before performing vector
arithmetic to derive the axes of the defined frame.
All keywords comprising the primary vector definition start with the
prefix

.. code-block:: text

      FRAME_<frame_ID>_PRI_

All keywords for the second defining vector are prefixed by

.. code-block:: text

      FRAME_<frame_ID>_SEC_

Here <frame_ID> is the integer ID code for the frame being defined.
Both the primary and secondary vectors are specified using the sets
of keywords described below.



Observer-Target Position Vectors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| An observer-target position vector is simply the position of one
  ephemeris object relative to another. These vectors are defined by
  an observer, a target, an aberration correction, a reference frame,
  and an epoch. In the frame kernel, there is no need to specify the
  reference frame or epoch: the CSPICE frame subsystem will determine
  which frame to use, and the epoch is supplied by the calling
  application at run time.

The observer and target are specified by name or ID code. The
aberration correction may be any value accepted by
:py:meth:`~spiceypy.spiceypy.spkezr`.

The frame kernel assignments used to define an observer-target
position vector are:

.. code-block:: text

    FRAME_<frame_ID>_<vec_ID>_VECTOR_DEF = 'OBSERVER_TARGET_POSITION'
    FRAME_<frame_ID>_<vec_ID>_VECTOR_DEF = 'OBSERVER_TARGET_POSITION'

    FRAME_<frame_ID>_<vec_ID>_VECTOR_DEF = 'OBSERVER_TARGET_POSITION'

    FRAME_<frame_ID>_<vec_ID>_OBSERVER   = <observer name or ID code>
    FRAME_<frame_ID>_<vec_ID>_TARGET     = <target name or ID code>
    FRAME_<frame_ID>_<vec_ID>_ABCORR     = <aberration correction>

where <vec_ID> may be either PRI or SEC, and <frame_ID> is the ID
code of the frame established by the generic assignments described
above.
In order for a two-vector frame using a position vector as part of
its definition to be computable, kernel data must be loaded that
enable computation of the specified position vector with respect to
the J2000 frame.

For an example of a two-vector frame definition using an
observer-target position vector, see the subsection titled
`Geocentric Solar Ecliptic (GSE) Frame` in the appendix `Frame
Definition Examples.`



Target Near point Vectors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Target near point vectors point from an observer to the closest
  point on an extended target body to the observer.

Target near point vectors are defined by an observer, a target, an
aberration correction, a frame, and an epoch. As with position
vectors, the frame and epoch are not specified in the frame kernel.

The observer and target are specified by name or ID code. Aberration
corrections may be any supported by the CSPICE function
:py:meth:`~spiceypy.spiceypy.subpt`. Light time corrections are
applied both to the observer- target center vector and to the
rotation of the target body. The stellar aberration correction, if
specified, is applied to the observer-target center vector.

The frame kernel assignments used to define a target near point
position vector are:

.. code-block:: text

      FRAME_<frame_ID>_<vec_ID>_VECTOR_DEF = 'TARGET_NEAR_POINT'
      FRAME_<frame_ID>_<vec_ID>_OBSERVER   = <observer name or ID code>
      FRAME_<frame_ID>_<vec_ID>_TARGET     = <target name or ID code>
      FRAME_<frame_ID>_<vec_ID>_ABCORR     = <aberration correction>

In order for a two-vector frame using a target near point vector as
part of its definition to be computable, kernel data must be loaded
that enable computation of the target near point vector with respect
to the J2000 frame.
For an example of a two-vector frame definition using a target near
point vector, see the subsection titled `Nadir Frame for Mars
Orbiting Spacecraft` in the appendix `Frame Definition Examples.`



Observer-Target Velocity Vectors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| An observer-target velocity vector is the velocity portion of the
  state of one ephemeris object relative to another. These vectors
  are defined by an observer, a target, an aberration correction, a
  reference frame, and an epoch. Of these, only the epoch is not
  specified in the frame kernel. Unlike observer-target position
  vectors, velocity vectors require a user-supplied frame
  specification. The specified frame (we'll call this the `velocity
  frame`) will be used to look up the velocity vector from the
  CSPICE SPK subsystem.

When the velocity frame is non-inertial and aberration corrections
are used, the epoch at which the velocity frame is evaluated will be
adjusted by the one-way light time between the observer and the
frame's center---just as is done by
:py:meth:`~spiceypy.spiceypy.spkezr` (see the header of that
function for details).

The reason the velocity frame specification is crucial is that,
(unlike rotations) state transformations between non-inertial frames
don't preserve geometric properties of velocity vectors. Example:
compare the specific angular momentum vector of a geosynchronous
satellite (obtained by taking the cross product of the satellite's
geocentric position and velocity vectors) in both the J2000 frame and
in the earth body-fixed frame. In the latter frame, the specific
angular momentum is zero. A valid two-vector frame could be defined
using the satellite's position and velocity in the J2000 frame, while
using the position and velocity in the earth body-fixed frame gives
rise to a degenerate case for which the two-vector frame is
undefined.

The observer and target defining the velocity vector are specified by
name or ID code. The aberration correction may be any value accepted
by :py:meth:`~spiceypy.spiceypy.spkezr`. The velocity frame may be
any computable by CSPICE, including a dynamic frame, as long as the
transformation between the velocity frame and the J2000 frame doesn't
require multiple levels of simulated recursion (see the discussion of
recursion in the chapter `Dynamic Frame Implementation
Considerations` below for details).

The frame kernel assignments used to define an observer-target
velocity vector are:

.. code-block:: text

    FRAME_<frame_ID>_<vec_ID>_VECTOR_DEF = 'OBSERVER_TARGET_VELOCITY'
    FRAME_<frame_ID>_<vec_ID>_OBSERVER   = <observer name or ID code>
    FRAME_<frame_ID>_<vec_ID>_TARGET     = <target name or ID code>
    FRAME_<frame_ID>_<vec_ID>_FRAME      = <frame_name>
    FRAME_<frame_ID>_<vec_ID>_ABCORR     = <aberration correction>

In order for a two-vector frame using a velocity vector as part of
its definition to be computable, kernel data must be loaded that
enable computation of the velocity vector with respect to both the
velocity frame and the J2000 frame.
For an example of a two-vector frame definition using an
observer-target velocity vector, see the subsection titled
`Geocentric Solar Ecliptic (GSE) Frame` in the appendix `Frame
Definition Examples.`



Constant Vectors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Constant vectors are defined by specifying a reference frame and a
  vector expressed relative to that frame. Optionally, aberration
  corrections may be specified.

The coordinates of a constant vector may be specified in any of the
rectangular, latitudinal, or RA/DEC (right ascension and declination)
systems. If the coordinates are angular, the associated angular units
must be specified; any angular units supported by the CSPICE function
:py:meth:`~spiceypy.spiceypy.convrt` may be used.

All constant vectors require the frame kernel assignments

.. code-block:: text

      FRAME_<frame_ID>_<vec_ID>_VECTOR_DEF = 'CONSTANT'
      FRAME_<frame_ID>_<vec_ID>_SPEC       = <coordinate_system>
      FRAME_<frame_ID>_<vec_ID>_FRAME      = <frame_name>

where <coordinate_system> is one of

.. code-block:: text

      'RECTANGULAR'
      'LATITUDINAL'
      'RA/DEC'

and the frame is any computable by CSPICE, including a dynamic frame,
as long as the transformation between the constant vector's frame and
the J2000 frame doesn't require multiple levels of simulated
recursion (see the discussion of recursion in the chapter `Dynamic
Frame Implementation Considerations` below for details).
When the coordinate system is rectangular, the vector is specified by
the frame kernel assignment

.. code-block:: text

      FRAME_<frame_ID>_<vec_ID>_SPEC   = 'RECTANGULAR'
      FRAME_<frame_ID>_<vec_ID>_VECTOR = ( <X component>,
                                           <Y component>,
                                           <Z component>  )

When the coordinate system is latitudinal, the vector is specified by
the frame kernel assignments

.. code-block:: text

      FRAME_<frame_ID>_<vec_ID>_SPEC      = 'LATITUDINAL'
      FRAME_<frame_ID>_<vec_ID>_UNITS     = <angular_units>
      FRAME_<frame_ID>_<vec_ID>_LONGITUDE = <longitude>
      FRAME_<frame_ID>_<vec_ID>_LATITUDE  = <latitude>

where <angular_units> designates one of the units supported by the
CSPICE function :py:meth:`~spiceypy.spiceypy.convrt`. The set of
supported units includes

.. code-block:: text

      'RADIANS'
      'DEGREES'
      'ARCSECONDS'

When the coordinate system is RA/DEC, the vector is specified by the
frame kernel assignments

.. code-block:: text

      FRAME_<frame_ID>_<vec_ID>_SPEC      = 'RA/DEC'
      FRAME_<frame_ID>_<vec_ID>_UNITS     = <angular_units>
      FRAME_<frame_ID>_<vec_ID>_RA        = <RA>
      FRAME_<frame_ID>_<vec_ID>_DEC       = <DEC>

where <angular_units> are as described above.
Aberration corrections are optional for constant vectors. The set of
available corrections is unique to this application: either light
time correction or stellar aberration correction may be applied, but
both cannot be applied together.

Light time corrections adjust the orientation of the constant
vector's frame for the one-way light time between the center of the
frame and a specified observer. The application to the frame of light
time correction is identical to that performed by the CSPICE function
:py:meth:`~spiceypy.spiceypy.spkezr` when it is asked to compute a
light-time corrected state relative to a non-inertial reference
frame. Supported light time corrections are any of those supported by
:py:meth:`~spiceypy.spiceypy.spkezr` that don't include stellar
aberration correction.

The user may also correct the constant vector for stellar aberration;
this correction is a function of the constant vector and the velocity
of an observer relative to the solar system barycenter. A typical
application would be to correct an inertially referenced star
direction vector for the stellar aberration induced by motion of an
observing spacecraft. The supported stellar aberration corrections
are

.. code-block:: text

      'S'      {correct for stellar aberration, reception case}
      'XS'     {correct for stellar aberration, transmission case}

In the application above, one would correct the apparent
observer-star direction by selecting the 'S' option. See the
discussion in the header of the CSPICE function
:py:meth:`~spiceypy.spiceypy.spkezr` for a description of the
`reception` and `transmission` aberration correction cases.
When aberration corrections are desired, the observer and the
correction are specified by the frame kernel assignments

.. code-block:: text

    FRAME_<frame_ID>_<vec_ID>_OBSERVER  = <observer name or ID code>
    FRAME_<frame_ID>_<vec_ID>_ABCORR    = <aberration correction>

In order for a two-vector frame using a constant vector as part of
its definition to be computable, kernel data must be loaded that
enable computation of the specified vector with respect to both the
constant vector's frame and the J2000 frame.
For examples of two-vector frame definitions using constant vectors,
see the subsections titled `Geocentric Solar Magnetospheric (GSM)
Frame` and `Mercury Solar Equatorial (MSEQ) Frame` in the
appendix `Frame Definition Examples.`



Mean Equator and Equinox of Date Frames
========================================

| Mean Equator and Equinox of Date Frames are defined for a solar
  system body (for example, a planet) using mathematical models of
  the orientation of the body's mean equatorial and orbital planes.
  The term `mean equator` indicates that orientation of the
  equatorial plane is modeled accounting for precession only. The
  `mean equinox` is the intersection of the body's mean orbital
  plane with the mean equatorial plane. The X-axis of such a frame is
  aligned with the cross product of the north-pointing vectors normal
  to the body's mean equator and mean orbital plane of date. The
  Z-axis is aligned with the first of these normal vectors. The Y
  axis is the cross product of the Z and X axes. The resulting
  reference frame is time-varying; the term `of date` means this
  frame is evaluated at a specified epoch.

The mathematical model for a mean equator and equinox of date frame
is typically called a `precession model`; CSPICE adopts this
usage.

The CSPICE frame subsystem supports mean equator and equinox of date
frames via precession models built into CSPICE. In principle, for any
body, a frame kernel definition for a mean equator and equinox of
date frame identifies which precession model to use for that body.
Currently CSPICE supports only one precession model: the 1976 IAU
precession model for the earth.



Defining a Mean Equator and Equinox of Date Frame in a Frame Kernel

|







Specifying the Base Frame
--------------------------

| The base frame of a mean equator and equinox of date frame is a
  function of the precession model. For the 1976 IAU earth precession
  model the base frame is J2000. This association is made via the
  assignment:

.. code-block:: text

      FRAME_<frame_ID>_RELATIVE           =  'J2000'



Specifying the Frame Family
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| A mean equator and equinox of date frame is identified by frame
  family specification:

.. code-block:: text

      FRAME_<frame_ID>_FAMILY = 'MEAN_EQUATOR_AND_EQUINOX_OF_DATE'



Specifying the Precession Model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| The 1976 IAU precession model is `selected` via the assignment:

.. code-block:: text

      FRAME_<frame_ID>_PREC_MODEL   = 'EARTH_IAU_1976'



Specifying a Rotation State or Freeze Epoch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Although mean equator and equinox of date frames are, strictly
  speaking, non-inertial, their time variation may be very slow. In
  some cases it may be desirable to treat them as inertial
  (specifically, non-rotating), perhaps in order to simplify
  computations or to ensure compatibility with computations from
  another source.

Users can instruct the CSPICE frame subsystem to treat a mean equator
and equinox of date frame as either inertial or rotating by making a
`rotation state` assignment. Users can also direct the frame
subsystem to treat a mean equator and equinox of date frame as though
it were `frozen` at a specified epoch. See the section above
titled `Conditional Keywords for Parameterized Dynamic Frames` for
instructions on how to make these assignments.

Definitions of mean equator and equinox of date frames require
either, but not both, the rotation state or a freeze epoch to be
specified.

For examples of Mean Equator and Equinox of Date frame definitions,
see the subsection titled `Earth Mean Equator and Equinox of Date
Frames` in the appendix `Frame Definition Examples.`



True Equator and Equinox of Date Frames
========================================

| True Equator and Equinox of Date Frames may be viewed as a
  refinement of mean equator and equinox of date frames. The term
  `true equator` indicates that orientation of a body's equatorial
  plane is modeled accounting for precession and nutation. The
  `true equinox` is the intersection of the body's mean orbital
  plane with the true equatorial plane. The X-axis of such a frame is
  aligned with the cross product of the north-pointing vectors normal
  to the body's true equator and mean orbital plane of date. The
  Z-axis is aligned with the first of these normal vectors. The Y
  axis is the cross product of the Z and X axes. The term `of
  date` means that these axes are evaluated at a specified epoch.



Defining a True Equator and Equinox of Date Frame in a Frame Kernel

| True Equator and Equinox of date frame definitions are nearly
  identical to those for mean of date frames (see above): the only
  differences are the frame family specification and the addition of
  an assignment identifying the nutation model.



Specifying the Base Frame
--------------------------

| The base frame of a true equator and equinox of date frame is a
  function of the precession model. For the 1976 IAU earth precession
  model the base frame is J2000. This association is made via the
  assignment:

.. code-block:: text

      FRAME_<frame_ID>_RELATIVE           =  'J2000'



Specifying the Frame Family
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| A true equator and equinox of date frame is identified by frame
  family specification:

.. code-block:: text

      FRAME_<frame_ID>_FAMILY = 'TRUE_EQUATOR_AND_EQUINOX_OF_DATE'



Specifying the Precession Model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Currently CSPICE supports only one precession model: the 1976 IAU
  precession model for the earth.

The 1976 IAU precession model is `selected` via the assignment:

.. code-block:: text

      FRAME_<frame_ID>_PREC_MODEL   = 'EARTH_IAU_1976'



Specifying the Nutation Model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| The choice of nutation model is specified by the assignment:

.. code-block:: text

      FRAME_<frame_ID>_NUT_MODEL     = <nutation_model>

Currently the only available nutation model is the 1980 IAU nutation
model for the earth. An assignment specifying this model has the
form:
::

      FRAME_<frame_ID>_NUT_MODEL     = 'EARTH_IAU_1980'



Specifying a Rotation State or Freeze Epoch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Although true equator and equinox of date frames are, strictly
  speaking, non-inertial, their time variation may be very slow. In
  some cases it may be desirable to treat them as inertial
  (specifically, non-rotating), perhaps in order to simplify
  computations or to ensure compatibility with computations from
  another source.

Users can instruct the CSPICE frame subsystem to treat a true equator
and equinox of date frame as either inertial or rotating by making a
`rotation state` assignment. Users can also direct the frame
subsystem to treat a true equator and equinox of date frame as though
it were `frozen` at a specified epoch. See the section above
titled `Conditional Keywords for Parameterized Dynamic Frames` for
instructions on how to make these assignments.

Definitions of true equator and equinox of date frames require
either, but not both, the rotation state or a freeze epoch to be
specified.

For examples of True Equator and Equinox of Date frame definitions,
see the subsection titled `Earth True Equator and Equinox of Date
Frames` in the appendix `Frame Definition Examples.`



Mean Ecliptic and Equinox of Date Frames
=========================================

| Mean Ecliptic and Equinox of Date Frames are closely related to
  mean equator and equinox of date frames: for a given body, the
  former is obtained by rotating the latter about the X-axis by the
  mean obliquity of date.

The term `mean equator` indicates that orientation of a body's
equatorial plane is modeled accounting for precession. The `mean
equinox` is the intersection of the body's mean orbital plane with
the mean equatorial plane. The X-axis of such a frame is aligned with
the cross product of the north-pointing vectors normal to the body's
mean equator and mean orbital plane of date. The Z-axis is aligned
with the second of these normal vectors. The Y axis is the cross
product of the Z and X axes. The term `of date` means that these
axes are evaluated at a specified epoch.



Defining a Mean Ecliptic and Equinox of Date Frame in a Frame Kernel
---------------------------------------------------------------------

| Mean Ecliptic and Equinox of date frame definitions are nearly
  identical to those for mean of date frames (see above): the only
  differences are the frame family specification and the addition of
  an assignment identifying the mean obliquity model.



Specifying the Base Frame
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| The base frame of a mean ecliptic and equinox of date frame is a
  function of the precession model. For the 1976 IAU earth precession
  model the base frame is J2000. This association is made via the
  assignment:

.. code-block:: text

      FRAME_<frame_ID>_RELATIVE           =  'J2000'



Specifying the Frame Family
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| A mean ecliptic and equinox of date frame is identified by frame
  family specification:

.. code-block:: text

      FRAME_<frame_ID>_FAMILY = 'MEAN_ECLIPTIC_AND_EQUINOX_OF_DATE'



Specifying the Precession Model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Currently CSPICE supports only one precession model: the 1976 IAU
  precession model for the earth.

The 1976 IAU precession model is `selected` via the assignment:

.. code-block:: text

      FRAME_<frame_ID>_PREC_MODEL   = 'EARTH_IAU_1976'



Specifying the Mean Obliquity Model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| The choice of mean obliquity model is specified by the assignment:

.. code-block:: text

      FRAME_<frame_ID>_OBLIQ_MODEL     = <obliquity_model>

Currently the only available mean obliquity model is the 1980 IAU
obliquity model for the earth. An assignment specifying this model
has the form:

.. code-block:: text

      FRAME_<frame_ID>_OBLIQ_MODEL     = 'EARTH_IAU_1980'



Specifying a Rotation State or Freeze Epoch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Although mean ecliptic and equinox of date frames are, strictly
  speaking, non-inertial, their time variation may be very slow. In
  some cases it may be desirable to treat them as inertial
  (specifically, non-rotating), perhaps in order to simplify
  computations or to ensure compatibility with computations from
  another source.

Users can instruct the CSPICE frame subsystem to treat a mean
ecliptic and equinox of date frame as either inertial or rotating by
making a `rotation state` assignment. Users can also direct the
frame subsystem to treat a mean ecliptic and equinox of date frame as
though it were `frozen` at a specified epoch. See the section
above titled `Conditional Keywords for Parameterized Dynamic
Frames` for instructions on how to make these assignments.

Definitions of mean ecliptic and equinox of date frames require
either, but not both, the rotation state or a freeze epoch to be
specified.

For examples of Mean Ecliptic and Equinox of Date frame definitions,
see the subsection titled `Earth Mean Ecliptic and Equinox of Date
Frames` in the appendix `Frame Definition Examples.`



Euler Frames
=============

| An Euler frame is defined by a sequence of rotation axes and
  corresponding time-dependent Euler angles. Each angle is defined by
  a set of polynomial coefficients. A reference epoch must be
  provided in the frame definition; the independent variable of each
  polynomial represents ephemeris seconds past the J2000 TDB epoch.

The rotation defined by the Euler angles maps position vectors via
left multiplication from the defined Euler reference frame to the
base frame:

.. code-block:: text

      V           = r(t) * V
       base_frame           Euler_frame

This rotation can be considered to be a time-dependent matrix

.. code-block:: text

      r(t)

where r(t) represents the composition of the rotations defined by the
input angle-axis pairs. Naming the axis indices and angles of the
Euler angle sequence

.. code-block:: text

      axindx_i, angle_i,  i = 1, 2, 3

r(t) is

.. code-block:: text

      r(t) = [ angle_1(t) ]      [ angle_2(t) ]      [ angle_3(t) ]
                       axindx_1            axindx_2            axindx_3

The axis indices axindx_i, for i = 1, 2, 3, are in the set { 1, 2, 3
}; axindx_2 cannot equal axindx_1 or axindx_3. For example, we could
have

.. code-block:: text

      axindx_1 = 3
      axindx_2 = 1
      axindx_3 = 3

Here the notation

.. code-block:: text

      [ A ]
           j

stands for a frame rotation by the angle A radians about the jth axis
of a right-handed frame, where we assign the axes {X, Y, Z} the
indices {1, 2, 3} respectively:

.. code-block:: text

      +-                     -+
      |   1       0      0    |
      |   0     cos A   sin A |   =  [ A ]
      |   0    -sin A   cos A |           1
      +-                     -+

      +-                     -+
      |  cos A    0    -sin A |
      |   0       1      0    |   =  [ A ]
      |  sin A    0     cos A |           2
      +-                     -+

      +-                     -+
      |  cos A   sin A   0    |
      | -sin A   cos A   0    |   =  [ A ]
      |   0       0      1    |           3
      +-                     -+

The base frame can be constructed from the Euler frame via a sequence
of Euler angle rotations as follows:

#. Rotate the axes of the Euler frame by angle_3 about the axis
   indexed by axindx_3.

#. Rotate the axes of the frame resulting from the first
   rotation by angle_2 about the axis indexed by axindx_2.

#. Rotate the axes of the frame resulting from the second
   rotation by angle_1 about the axis indexed by axindx_1.

The resulting set of axes are those of the base frame.
The rotation angles are defined as follows: letting t0 represent the
reference epoch, and letting

.. code-block:: text

      c   ,  i = 1, 2, 3;   j = 0, ... , ni
       i,j

be the polynomial coefficients for the ith angle, we have

.. code-block:: text

                                                           n1
      angle_1(t) = c   + c   * (t-t0) + ... + c    * (t-t0)
                    1,0   1,1                  1,n1

                                                           n2
      angle_2(t) = c   + c   * (t-t0) + ... + c    * (t-t0)
                    2,0   2,1                  2,n2

                                                           n3
      angle_3(t) = c   + c   * (t-t0) + ... + c    * (t-t0)
                    3,0   3,1                  3,n3

See the Rotation Required Reading,
`rotation.req <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/rotation.html>`__, or the header of the CSPICE
function :py:meth:`~spiceypy.spiceypy.eul2m` for details concerning
definition of rotations via Euler angles. Note however that the
referenced document and source code use a different convention for
labeling Euler angles and their rotation axes: here the elements of
the rotation sequence are numbered left to right; in those documents
the order is that in which rotations are performed, namely right to
left.


Defining an Euler Frame in a Frame Kernel
------------------------------------------

|



Specifying the Base Frame
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| The base frame of an Euler frame is specified via the assignment:

.. code-block:: text

      FRAME_<frame_ID>_RELATIVE           =  '<frame_name>'



Specifying the Frame Family
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| An Euler frame is identified by frame family specification:

.. code-block:: text

      FRAME_<frame_ID>_FAMILY = 'EULER'



Specifying the Epoch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| The zero epoch for the independent variable of the polynomials is
  defined using the SPICE text kernel calendar ephemeris time syntax.
  A sample template is shown below:

.. code-block:: text

      FRAME_<frame_ID>_EPOCH           =  @YYYY-MON-DD/HR:MN.SEC.###

A concrete example is:

.. code-block:: text

      FRAME_<frame_ID>_EPOCH           =  @2000-JAN-1/12:00:00.000

The calendar time string is assumed to represent a TDB epoch.
See the discussion in the section `Freeze Epoch` above or the
Kernel Required Reading, `kernel.req <./kernel.html>`__, for
further information.



Specifying the Euler Angles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Euler angles are specified by an axis sequence, a set of polynomial
  coefficients, and associated units. The axes are specified by an
  assignment of the form:

.. code-block:: text

      FRAME_<frame_ID>_AXES            =  ( <index of axis 1>
                                            <index of axis 2>
                                            <index of axis 3> )

The axis indices must be taken from the set

.. code-block:: text

      { 1, 2, 3 }

and the middle value must differ from its neighbors. The first
integer listed is the axis index for angle 1, the second for angle 2,
and the last for angle 3, where the role of the angles is as shown in
the equation for r(t) above.
Let n1, n2, and n3 represent the maximum degrees of the polynomials
for angles 1, 2, and 3 respectively. Then the polynomial coefficients
are defined by the assignments

.. code-block:: text

      FRAME_<frame_ID>_ANGLE_1_COEFFS = ( <order 0 coefficient>
                                          <order 1 coefficient>
                                                 ...
                                          <order n1 coefficient>  )

      FRAME_<frame_ID>_ANGLE_2_COEFFS = ( <order 0 coefficient>
                                          <order 1 coefficient>
                                                 ...
                                          <order n2 coefficient>  )

      FRAME_<frame_ID>_ANGLE_3_COEFFS = ( <order 0 coefficient>
                                          <order 1 coefficient>
                                                 ...
                                          <order n3 coefficient>  )

Angular units are specified by the frame kernel assignment

.. code-block:: text

      FRAME_<frame_ID>_UNITS     = <angular_units>

where <angular_units> designates one of the units supported by the
CSPICE function :py:meth:`~spiceypy.spiceypy.convrt`. The set of
supported units includes

.. code-block:: text

      'RADIANS'
      'DEGREES'
      'ARCSECONDS'

For an example of an Euler frame definition, see the subsection
titled `Euler Frames` in the appendix `Frame Definition
Examples.`


Product Frames
===============

| Product frames may be thought of as a generalization of TK frames.
  The orientation of a product frame relative to a specified base
  frame is defined by a product of one or more frame transformations,
  where each factor may be any transformation computable by the
  CSPICE frame subsystem.

Using the notation

.. code-block:: text

        B
      T
        A

to indicate the transformation from frame A to frame B, and letting
the names

.. code-block:: text

      PRODUCT
      BASE

denote a product frame and a `base` frame relative to which the
orientation of the product frame is defined, the transformation from
the base frame to the product frame is defined by a product of one or
more frame transformation `factors` consisting of transformations
from a given `from` frame to a given `to` frame:

.. code-block:: text

        PRODUCT      TO_1       TO_2            TO_N-1      TO_N
      T          =  T        * T       * ... * T         * T
        BASE         FROM_1     FROM_2          FROM_N-1    FROM_N

If the vector

.. code-block:: text

      v
        BASE

is expressed relative to the base frame, then applying a product
frame transformation to the vector expresses the vector relative to
the product frame:

.. code-block:: text

                   PRODUCT
      v        =  T        * v
       PRODUCT     BASE       BASE

In implementation of the equation above, the factor transformations
on the right hand side of the product frame's definition are applied
in right-to-left order.
The `from` and `to` frames of a product frame definition may be
completely arbitrary. The only restriction on these frames is that
the transformation from each `from` frame to its corresponding
`to` frame must be computable by CSPICE at the time the product
frame is used.

Note that because product frames are parameterized dynamic frames,
limits on recursion depth for dynamic frames imply that while the
factors may be dynamic frames, they may not be dynamic frames that
require a level of recursion in order to evaluate their orientation.



Defining a Product Frame in a Frame Kernel
----------------------------------------------

|



Specifying the Base Frame
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| The base frame of a product frame is specified via the assignment:

.. code-block:: text

      FRAME_<frame_ID>_RELATIVE =  '<frame_name>'



Specifying the Frame Family
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| A product frame is identified by frame family specification:

.. code-block:: text

      FRAME_<frame_ID>_FAMILY = 'PRODUCT'



Specifying the Factors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| The factor transformations are specified by the kernel variable
  assignments

.. code-block:: text

    FRAME_<frame_ID>_FROM_FRAMES = ( <from_frame 1> ... <from_frame N> )
    FRAME_<frame_ID>_TO_FRAMES   = ( <to_frame 1>   ... <to_frame N>   )

The `from` and `to` frames must be specified by name.
The Ith elements of the respective right-hand-side vectors of
`from` and `to` frame names define the Ith factor
transformation. The order of the factors in the kernel variables is
the same as the order of the factors in the transformation product.
When a vector is transformed from the base frame to the product
frame, the transformations defined by the factors are applied in
right-to-left order: the factor defined by the frames indexed by
`N` is applied first.



Dynamic Frame Implementation Considerations
============================================

|



Introduction
---------------

| This chapter discusses issues affecting implementation of dynamic
  frames:

- Simulated Recursion

- Frame Derivative Accuracy

- Degenerate Geometry

- Efficiency

By necessity, this chapter presents some aspects of the
implementation of the CSPICE parameterized dynamic frame subsystem.
The implementation described here is not considered part of the
SPICE API specification. Although unlikely, this implementation
could be changed in a future version of the SPICE Toolkit.


Simulated Recursion
---------------------

|

The Need for Recursion in the SPICE Frame Subsystem
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| In the following discussion, we'll use the graph notation below to
  indicate that function A calls function B:

.. code-block:: text

      A -> B

A function R_0 is `recursive` if it calls itself

.. code-block:: text

      R_0 -> R_0

or if some sequence of calls initiated in the function R_0 results in
a call to R_0:

.. code-block:: text

      R_0 -> R_1-> ... -> R_0

ANSI standard Fortran 77 doesn't permit recursive calls. However, the
implementation of two-vector frames requires sequences of calls that
at face value are recursive. For example, to look up a state vector
in the GSE frame (see the appendix `Frame Definition Examples`),
the function SPKEZ must initiate the sequence of calls (ellipses
indicate omitted portions of the call graph)

.. code-block:: text

      SPKEZ -> ... -> FRMGET -> ... -> SPKEZ -> ... -> FRMGET

Both SPKEZ and FRMGET are called recursively in this graph.
This issue affects not only SPICELIB but CSPICE and Icy as well
because these products rely on the SPICELIB (Fortran) implementation
of the frame subsystem.


Implementation of Limited Simulated Recursion
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| SPICELIB solves the recursion problem by providing renamed
  duplicates of routines that must be called recursively. For
  example, the invalid call graph

.. code-block:: text

      SPKEZ -> ... -> FRMGET -> ... -> SPKEZ -> ... -> FRMGET

is implemented in (valid) ANSI standard Fortran 77 using the call
graph

.. code-block:: text

      SPKEZ -> ... -> FRMGET -> ... -> ZZSPKEZ0 -> ... -> ZZFRMGT0

To a limited extent, two levels of simulated recursion are supported
in the frame subsystem, so call graphs of the form

.. code-block:: text


   SPKEZ -> ... -> FRMGET    -> ... -> ZZSPKEZ0    -> ... -> ZZFRMGT0
            -> ... -> ZZSPKEZ1  -> ... -> ZZFRMGT1

are possible.
For brevity, when we refer to recursion in the following discussion,
we'll omit the qualifier `simulated.`



Limits on Recursion in Frame Definitions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| We say a reference frame is `evaluated` when the transformation
  from the frame to its base frame is computed for some epoch. A
  parameterized dynamic frame normally is evaluated each time it is
  referenced in a function call. For example, the calls

.. code-block:: python

      state, lt  = spkezr( moon, et, "GSE", "NONE", "EARTH" )
      xform  = sxform() "GSE", "J2000", et )

both cause the GSE parameterized dynamic frame to be evaluated at ET.
When the definition of a parameterized dynamic frame F1 refers to a
second frame F2 as

- the base frame

- the frame relative to which a constant vector is specified

- the frame relative to which a velocity vector is specified

the referenced frame F2 may be dynamic, but F2 must not make
reference to any dynamic frame. If deeper recursion is required to
evaluate the referenced frame F2, an error will occur at run time.
If F2 is not dynamic but its evaluation requires evaluation of a
dynamic frame F3, the same restrictions apply to F3.

When a dynamic frame is used as a base frame in either an SPK or CK
segment, evaluation of data from that segment may result in a call to
the dynamic frame subsystem. That call may result in lookup of
another segment whose base frame is dynamic, and so on: the original
kernel lookup could easily exhaust the dynamic frame subsystem's
ability to handle recursive calls.

Clearly use of dynamic frames in SPK and CK files requires caution.
However, there are some `reasonable` applications that call for
dynamic base frames in kernels, for example: representing ephemerides
of earth orbiters expressed relative to the earth true equator and
equinox of date frame.



Frame Derivative Accuracy
--------------------------

| Transformation of state vectors between frames F1 and F2 via a
  time-dependent rotation R(t) requires the derivative with respect
  to time of R(t): d(R(t))/dt. The accuracy of the velocity portion
  of a transformed state is limited by the accuracy of d(R(t))/dt.
  When either frame F1 or F2 is dynamic, loss of accuracy in
  d(R(t))/dt can occur for a number of reasons, including but not
  limited to:

- R(t) depends on CK data. Often angular rates in C-kernels
  have low accuracy. (This issue applies to non-dynamic frames as
  well.)

- R(t) is defined via a two-vector frame using position
  vectors, and the velocities associated with those vectors have low
  accuracy. This can happen for SPK data types for which position and
  velocity are represented independently, for example SPK types 3 or
  1.

- R(t) is defined via a two-vector frame using
  aberration-corrected position vectors. Even if the geometric
  velocities of the vectors are accurate, the aberration-corrected
  velocities associated with those vectors will probably have low
  accuracy due to accuracy limitations of the aberration corrections
  applied to velocity vectors by the SPK subsystem.

- R(t) is defined via a two-vector frame using a velocity
  vector. The acceleration associated with the velocity vector is
  required to compute d(R(t))/dt, and this acceleration must be
  computed numerically. The results are likely to have at best single
  precision validity.



Degenerate Geometry
--------------------

| Two-vector frame definitions can suffer from singularities: the
  defining vectors may, in some cases, become extremely close to
  parallel. In such cases the frame evaluation may generate
  meaningless results.

Because two-vector frame definitions may be perfectly valid for some
epochs and yield degenerate geometry for others, testing can easily
fail to reveal problems with these definitions. Careful frame design
is the best defense.

As a backup measure, setting the angular separation tolerance in
two-vector frame definitions can enable the frame subsystem to
diagnose at run time degenerate or near-degenerate geometry. See the
section `Specifying the Angular Separation Tolerance` above for
details.



Efficiency Concerns
-------------------

| In many cases, when recursion is required by a frame evaluation,
  that evaluation requires a relatively large amount of computation.
  For example, when an SPK call results in a two-vector frame
  evaluation, several additional SPK calls may be required to support
  the original call. The original call may be many times slower than
  a call requiring only non-dynamic frame evaluation.

To minimize the performance degradation imposed by recursion, avoid
unnecessary references to dynamic frames in frame definitions. When
possible, use J2000 or another inertial frame as the base frame, or
as the frame relative to which constant or velocity vectors are
defined. When it is not possible to use an inertial frame, prefer
non-dynamic, non-inertial frames to dynamic frames.



Switch Frames
==============

| Switch frames choose at run time other frames, called `base
  frames,` with which to align their orientation. Switch frames
  `switch` the base frames they align with as a function of time,
  using a prioritized list of base frames and optional, associated
  time bounds; this list is provided as part of the switch frame
  definition stored in a text kernel.

Switch frames extend the flexibility of the SPICE frame subsystem by
allowing a user-defined frame to rely on different data sources at
different times. For example:

- A switch frame representing orientation of a spacecraft
  could have a top-priority CK frame for reconstructed data, and a
  lower-priority CK frame for predicted data, where the two CK frames
  have different frame class IDs (also called `instrument IDs` in
  some SPICE documentation) and different associated spacecraft
  clocks.

- A switch frame representing orientation of a spacecraft
  could have a top-priority CK frame for reconstructed data, and a
  lower-priority dynamic frame for times not covered by the CK data.

- A switch frame representing predicted orientation of a
  spacecraft could have a sequence of base frames of one or more
  classes covering time intervals which overlap only at their
  endpoints.

- A switch frame representing orientation of a comet's nucleus
  could have a top-priority CK frame covering a time interval over
  which accurate orientation data are available, and a lower-priority
  PCK frame for a time interval of greater extent.

Base frames of a switch frame may have associated time intervals
limiting their applicability. Given a request time, a base frame will
be considered as a data source only if the request time falls within
the time interval associated with that base frame. If time intervals
are used in a switch frame definition, they must be provided for all
base frames of that switch frame.
If base frames of a switch frame don't have associated time
intervals, the base frames are applicable for all request times.

A switch frame selects a base frame as follows: given a request time,
the switch frame subsystem attempts to obtain orientation data from
the highest priority, applicable base frame. If that base frame is a
CK frame and data are unavailable, the next applicable frame in the
base frame list is used, and so on. If an applicable base frame is
not a CK frame and requested data are unavailable, an error is
signaled. The orientation and optional angular velocity of the switch
frame are those of the selected base frame.



Specifying Switch Frames
-------------------------

| As with other frame classes, switch frames require a frame name,
  frame ID code, frame class ID code, and center. It is recommended
  that the frame class ID match the frame ID. The frame class is 6.
  The initial part of the frame specification has this form:

.. code-block:: text

      FRAME_<name>             = <ID code>
      FRAME_<ID code>_NAME     = '<name>'
      FRAME_<ID code>_CLASS    = 6
      FRAME_<ID code>_CLASS_ID = <frame class ID>
      FRAME_<ID code>_CENTER   = <center ID code or name>



The Base Frame List
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| The next part of the specification is the prioritized base frame
  list:

.. code-block:: text

      FRAME_<ID code>_ALIGNED_WITH = (
          < lowest priority base frame ID or name >
          < next-lowest priority base frame ID or name >
             ...
          < highest priority base frame ID or name >  )

All base frames of a given switch frame must be specified by name, or
all must be specified by frame ID code.
All base frames of a switch frame must have specifications available
at the time the switch frame is used. This applies even to CK base
frames. Note that CK frame ID codes and frame class ID codes are not
required to match; the latter is the ID stored in CK files. It is the
frame ID code that's required in the base frame list; this is
provided by a CK frame specification.

A base frame may occur multiple times in the base frame list. This
can be useful for base frame lists that have associated time
intervals.



Time Intervals Associated with Base Frames
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Optional time intervals associated with base frames are specified
  by two kernel variables, respectively containing start and stop
  times:

.. code-block:: text

      FRAME_<ID code>_START = (
      < start time for lowest priority base frame >
      < start time for next-lowest priority base frame >
         ...
      < start time for highest priority base frame>  )

      FRAME_<ID code>_STOP = (
      < stop time for lowest priority base frame >
      < stop time for next-lowest priority base frame >
         ...
      < stop time for highest priority base frame>  )

If time intervals are provided for a switch frame, the count of start
times must match the count of stop times, and each must match the
count of entries in the base frame list.
Start and stop times may be specified by single-quoted time strings,
double precision numbers, or as times using the text kernel `@
format.` For example:

.. code-block:: text

      '2021-12-31T12:00:00'
      694224069.183907
      6.94224069183907E+08
      @2021-DEC-31/12:01:09.183907

Times provided as single-quoted strings must be accepted by the
CSPICE function :py:meth:`~spiceypy.spiceypy.str2et`. A leapseconds
kernel must be loaded in order to use such time strings.
Numeric values are interpreted as seconds past J2000 TDB. Times in
text kernel time format are interpreted as TDB calendar dates. Use of
times in either of these formats does not require a leapseconds
kernel.

See the Kernel Required Reading `kernel.req <./kernel.html>`__
for details concerning the text kernel time format and accepted
formats of double precision values.

Each list of times for a given switch frame must be specified by
values of the same type: string or numeric. Times in text kernel
format are actually considered to be numeric values. The types used
for a switch frame's list of start times and for its list of stop
times need not match, but use of consistent types is recommended for
readability.



Binary Search
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| To improve efficiency of base frame selection for a given switch
  frame and request time, the switch frame subsystem may perform a
  binary search of the base frames' time intervals to find the
  highest priority frame providing data for the request time.

A switch frame is eligible for binary search if:

- Its base frames have associated time intervals

- Any pair of time intervals is disjoint or has only singleton
  overlap. For example, the stop time of one interval may coincide
  with the start time of another.

- The intervals are listed in increasing time order. This
  requires the intervals for later times to be associated with higher
  priority base frames than those of intervals for earlier times.

If the base frame identified by a binary search is a CK frame, and if
it does not provide data for the request time, it is still possible
that data are available in the special case where the request time
matches the start time of the selected base, and if that time is also
the stop time of preceding, next-lower-priority interval. In this
case the preceding interval will be checked for data availability.


Switch Frame Connections
---------------------------

| Connections between switch frames and other frames are made by the
  CSPICE functions frmget_c and rotget_c. If either of these
  functions is called with the frame ID of a switch frame as input,
  and if the selected base frame is

- a built-in inertial frame, then the output frame ID will be
  that of J2000, and the returned transformation will be that from
  the inertial base frame to J2000.

- a PCK frame, then the output frame ID will be that of J2000,
  and the returned transformation will be that from the PCK base
  frame to J2000.

- a CK frame, then the output frame ID will be that of the CK
  frame's base frame, and the returned transformation will be that
  from the CK frame to its base frame.

- a TK frame, then the output frame ID will be that of the TK
  frame's base frame, and the returned transformation will be that
  from the TK frame to its base frame.

- a dynamic frame, then the output frame ID will be that of
  the dynamic base frame itself, and the returned transformation will
  be the identity matrix of the appropriate dimension.

- a switch frame, then the output frame ID will be that of the
  switch base frame itself, and the returned transformation will be
  the identity matrix of the appropriate dimension.



Switch Frame Buffering
-----------------------

| The switch frame subsystem buffers switch frame specifications in a
  form suitable for efficient use. Expensive operations such as
  kernel pool lookups, frame name conversions, and time string
  conversions are performed only when the buffer contents must be
  modified.

It is possible for a user application to use many more switch frames
than can be buffered concurrently, but changing the buffer contents
with high frequency is inefficient.

The buffer limits shown below are hard-coded. They may be increased
in future versions of CSPICE.

- Maximum count of switch frames loaded concurrently: 1013

- Maximum count of base frames of all concurrently loaded
  switch frames: 15000



Appendix. `Built in` Inertial Reference Frames
===============================================

|



Complete List of `Built in` Inertial Reference Frames
-----------------------------------------------------

| SPICE software includes the definitions of several inertial
  reference frames. The numeric IDs and names of the inertial frames
  defined in SPICE software are:

.. code-block:: text

         ID  Name        Description
      -----  --------    -------------------------------------------

       1  J2000       Earth mean equator, dynamical equinox of J2000.
                         The root reference frame for SPICE.


       2  B1950       Earth mean equator, dynamical equinox of B1950.
                         The B1950 reference frame is obtained by
                         precessing the J2000 frame backwards from

                       Julian year 2000 to Besselian year 1950, using
                         the 1976 IAU precession model.

                         The rotation from B1950 to J2000 is

                         [ -z ]  [ theta ]  [ -zeta ]
                                3          2          3

                       The values for z, theta, and zeta are computed
                         from the formulas given in table 5 of [5].

                         z     =  1153.04066200330"
                         theta =  1002.26108439117"
                         zeta  =  1152.84248596724"

          3  FK4         Fundamental Catalog (4). The FK4 reference
                         frame is derived from the B1950 frame by
                         applying the equinox offset determined by
                         Fricke.

                         [ 0.525" ]
                                   3


         4  DE-118      JPL Developmental Ephemeris (118). The DE-118

                       reference frame is nearly identical to the FK4

                      frame. It is also derived from the B1950 frame.
                         Only the offset is different

                         [ 0.53155" ]
                                     3


                        In [2], Standish uses two separate rotations,

                         [ 0.00073" ]  P [ 0.5316" ]
                                      3              3


                      (where P is the precession matrix used above to

                     define the B1950 frame). The major effect of the

                     second rotation is to correct for truncating the
                         magnitude of the first rotation. At his

                       suggestion, we will use the untruncated value,
                         and stick to a single rotation.



                     Most of the other DE historical reference frames
                         are defined relative to either the DE-118 or
                         B1950 frame. The values below are taken
                         from [4].


                     DE number  Offset from DE-118  Offset from B1950

                     ---------  ------------------  -----------------

                            96            +0.1209"           +0.4107"

                           102            +0.3956"           +0.1359"

                           108            +0.0541"           +0.4775"

                           111            -0.0564"           +0.5880"

                           114            -0.0213"           +0.5529"

                           122            +0.0000"           +0.5316"

                           125            -0.0438"           +0.5754"

                           130            +0.0069"           +0.5247"

          5  DE-96       JPL Developmental Ephemeris ( 96).

          6  DE-102      JPL Developmental Ephemeris (102).

          7  DE-108      JPL Developmental Ephemeris (108).

          8  DE-111      JPL Developmental Ephemeris (111).

          9  DE-114      JPL Developmental Ephemeris (114).

         10  DE-122      JPL Developmental Ephemeris (122).

         11  DE-125      JPL Developmental Ephemeris (125).

         12  DE-130      JPL Developmental Ephemeris (130).

         13  GALACTIC    Galactic System II. The Galactic System II
                         reference frame is defined by the following
                         rotations:
                              o          o            o
                         [ 327  ]  [ 62.6  ]  [ 282.25  ]
                                 3          1            3

                         In the absence of better information, we
                         assume the rotations are relative to the
                         FK4 frame.

         14  DE-200      JPL Developmental Ephemeris (200).

         15  DE-202      JPL Developmental Ephemeris (202).

         16  MARSIAU     Mars Mean Equator and IAU vector of
                         J2000. The IAU-vector at Mars is the point

                        on the mean equator of Mars where the equator
                         ascends through the earth mean equator.
                         This vector is the cross product of Earth
                         mean north with Mars mean north.

         17  ECLIPJ2000  Ecliptic coordinates based upon the
                         J2000 frame.

                         The value for the obliquity of the
                         ecliptic at J2000 is taken from page 114

                        of [7] equation 3.222-1. This agrees with the
                         expression given in [5].

         18  ECLIPB1950  Ecliptic coordinates based upon the B1950
                         frame.


                       The value for the obliquity of the ecliptic at
                         B1950 is taken from page 171 of [7].

         19  DE-140      JPL Developmental Ephemeris. (140)

                        The DE-140 frame is the DE-400 frame rotated:


           0.9999256765384668  0.0111817701197967  0.0048589521583895

          -0.0111817701797229  0.9999374816848701 -0.0000271545195858

          -0.0048589520204830 -0.0000271791849815  0.9999881948535965

                         The DE-400 frame is treated as equivalent to
                         the J2000 frame.

         20  DE-142      JPL Developmental Ephemeris. (142)

                        The DE-142 frame is the DE-402 frame rotated:


           0.9999256765402605  0.0111817697320531  0.0048589526815484

          -0.0111817697907755  0.9999374816892126 -0.0000271547693170

          -0.0048589525464121 -0.0000271789392288  0.9999881948510477

                         The DE-402 frame is treated as equivalent to
                         the J2000 frame.

         21  DE-143      JPL Developmental Ephemeris. (143)

                        The DE-143 frame is the DE-403 frame rotated:


           0.9999256765435852  0.0111817743077255  0.0048589414674762

          -0.0111817743300355  0.9999374816382505 -0.0000271622115251

          -0.0048589414161348 -0.0000271713942366  0.9999881949053349

                         The DE-403 frame is treated as equivalent to
                         the J2000 frame.



Inertial Reference Frame References
------------------------------------


.. code-block:: text

      [1] Jay Lieske, ``Precession Matrix Based on IAU (1976)
          System of Astronomical Constants,` Astron. Astrophys.
          73, 282-284 (1979).

      [2] E.M. Standish, Jr., ``Orientation of the JPL Ephemerides,
          DE 200/LE 200, to the Dynamical Equinox of J2000,`
          Astron. Astrophys. 114, 297-302 (1982).

      [3] E.M. Standish, Jr., ``Conversion of Ephemeris Coordinates
          from the B1950 System to the J2000 System,` JPL IOM
          314.6-581, 24 June 1985.

      [4] E.M. Standish, Jr., ``The Equinox Offsets of the JPL
          Ephemeris,` JPL IOM 314.6-929, 26 February 1988.

      [5] Jay Lieske, ``Expressions for the Precession  Quantities
          Based upon the IAU (1976) System of Astronomical
          Constants` Astron. Astrophys. 58, 1-16 (1977).

      [6] Laura Bass and Robert Cesarone "Mars Observer Planetary
          Constants and Models" JPL D-3444 November 1990.

      [7] "Explanatory Supplement to the Astronomical Almanac"
           edited by P. Kenneth Seidelmann. University Science
           Books, 20 Edgehill Road, Mill Valley, CA 94941 (1992)



Low Level Inertial Reference Frame Functions
---------------------------------------------

| You may obtain the rotation between any two `built in` inertial
  frames using the CSPICE function irfrot_c and supplying the IDs for
  the frames of interest. The module header for irfrot_c, and this
  document, always contain the definitive list of recognized frames.

This example shows how to rotate a position vector from FK4
coordinates to J2000 coordinates (the ID for the FK4 frame is 3, the
ID for the J2000 frame is 1)

::

         SpiceInt from = 3;
         SpiceInt to   = 1;

         irfrot_ ( &from, &to, rot )
         mxv_c   ( rot  , old, new )

(\`rot' is a 3-by-3 matrix, \`old' and \`new' are 3-vectors;
subroutine :py:meth:`~spiceypy.spiceypy.mxv` multiplies a matrix and a
vector to produce a vector.)
Two additional subroutines can be used to convert a frame name to ID
and vice versa. This example shows how to find the index of the
DE-125 frame:

::

         irfnum_ ( "DE-125", frid, strlen("DE-125") )

This example shows how to find the name corresponding to ID 11:
::

         SpiceInt frid = 11;

         irfnam_ ( &fride, frname, strlen(frname) )



Appendix. `Built in` PCK-Based IAU Body-Fixed Reference Frames
===============================================================

| SPICE software includes the definitions of body-fixed frames for
  all natural bodies -- planets, satellites, and some asteroids --
  listed in International Astronomical Union (IAU) reports on
  cartographic constants. These frames are fixed to and do not move
  with respect to `surface` features of a natural object, but they
  do move with respect to inertial frames as the object rotates. The
  complete list of body-fixed frames `built into` SPICE is given
  below. Each name is constructed by adding the prefix `IAU\_` to
  the name of the body. The prefix `IAU\_` indicates that the
  orientation of this frame is typically determined from the IAU
  model for the body in question. The constants associated with this
  model are stored in one or more text PCK files, which, therefore,
  must be loaded in order for orientation of these frames to be
  computed.

.. code-block:: text

      IAU_52_EUROPA
      IAU_ADRASTEA
      IAU_AMALTHEA
      IAU_ANANKE
      IAU_ARIEL
      IAU_ARROKOTH
      IAU_ATLAS
      IAU_BELINDA
      IAU_BENNU
      IAU_BIANCA
      IAU_BORRELLY
      IAU_CALLIRRHOE
      IAU_CALLISTO
      IAU_CALYPSO
      IAU_CARME
      IAU_CERES
      IAU_CHALDENE
      IAU_CHARON
      IAU_CORDELIA
      IAU_CRESSIDA
      IAU_DAVIDA
      IAU_DEIMOS
      IAU_DESDEMONA
      IAU_DESPINA
      IAU_DIDYMOS
      IAU_DIMORPHOS
      IAU_DIONE
      IAU_DONALDJOHANSON
      IAU_EARTH
      IAU_ELARA
      IAU_ENCELADUS
      IAU_EPIMETHEUS
      IAU_ERINOME
      IAU_EROS
      IAU_EUROPA
      IAU_EURYBATES
      IAU_GALATEA
      IAU_GANYMEDE
      IAU_GASPRA
      IAU_HARPALYKE
      IAU_HELENE
      IAU_HIMALIA
      IAU_HYDRA
      IAU_HYPERION
      IAU_IAPETUS
      IAU_IDA
      IAU_IO
      IAU_IOCASTE
      IAU_ISONOE
      IAU_ITOKAWA
      IAU_JANUS
      IAU_JULIET
      IAU_JUPITER
      IAU_KALYKE
      IAU_LARISSA
      IAU_LEDA
      IAU_LEUCUS
      IAU_LUTETIA
      IAU_LYSITHEA
      IAU_MAGACLITE
      IAU_MARS
      IAU_MENOETIUS
      IAU_MERCURY
      IAU_METIS
      IAU_MIMAS
      IAU_MIRANDA
      IAU_MOON
      IAU_NAIAD
      IAU_NEPTUNE
      IAU_NEREID
      IAU_NIX
      IAU_OBERON
      IAU_OPHELIA
      IAU_ORUS
      IAU_PALLAS
      IAU_PAN
      IAU_PANDORA
      IAU_PASIPHAE
      IAU_PATROCLUS
      IAU_PHOBOS
      IAU_PHOEBE
      IAU_PLUTO
      IAU_POLYMELE
      IAU_PORTIA
      IAU_PRAXIDIKE
      IAU_PROMETHEUS
      IAU_PROTEUS
      IAU_PUCK
      IAU_QUETA
      IAU_RHEA
      IAU_ROSALIND
      IAU_RYUGU
      IAU_SATURN
      IAU_SINOPE
      IAU_STEINS
      IAU_SUN
      IAU_TAYGETE
      IAU_TELESTO
      IAU_TEMPEL_1
      IAU_TETHYS
      IAU_THALASSA
      IAU_THEBE
      IAU_THEMISTO
      IAU_TITAN
      IAU_TITANIA
      IAU_TRITON
      IAU_UMBRIEL
      IAU_URANUS
      IAU_VENUS
      IAU_VESTA



Appendix. High Precision Earth Fixed Frames
=============================================

| In addition to the text PCK based IAU body-fixed frame for Earth,
  'IAU_EARTH', these two body-fixed frames for Earth are also
  `built into` the SPICE system:

.. code-block:: text

      ITRF93
      EARTH_FIXED

'ITRF93' is a frame `fixed` to the Earth's crust. It provides a
high precision model for the orientation of the Earth with respect to
J2000. In SPICE this is also a PCK type frame but its orientation is
provided in a binary PCK file.
'EARTH_FIXED' is a `generic frame` that gives the orientation of
the Earth with respect to some other frame (usually 'IAU_EARTH' or
'ITRF93') via a constant rotational offset. Such frames are called
Text Kernel (TK) frames. See the subsection `Gaining Flexibility
via TK Frames` for a discussion of the use of TK frames.



Appendix. Frame Identifiers Reserved for Earth Fixed Frames
============================================================

| NAIF has set aside a range of frame ID codes for Earth fixed frames
  to be added in the future when/if additional high precision Earth
  orientation model become available and are implemented in SPICE.
  This reserved range is from 13000 to 13999. The ID assigned to
  'ITRF93', which is only currently implemented frame of this kind,
  is 13000. All of these frames are PCK based frames. They model the
  orientation of the Earth with respect to an inertial reference
  frame such as the J2000 frame. Since the primary customer of these
  frames is NASA's Deep Space Network (DSN), we shall refer to any
  frame with ID code in this reserved range as a DSN Earth Fixed
  frame or simply DSN frame.

The class ID to associate with any DSN frame is the frame ID minus
For example, the class ID associated with frame 13003 is 3003.
It is this class ID that should be placed in the PCK file that
implements the relationship between the DSN frame and the
corresponding inertial frame.

The center of any DSN frame is the center of mass of the Earth, which
has SPK ID code 399.

These frames are partially `built in`. Given a frame ID in the
range from 13001 to 13999, the frame subsystem `knows` that the
frame is a PCK frame, the center of the frame is 399 and the class ID
of the frame is the frame ID - 10000. This knowledge cannot be
overridden. However, the frame subsystem does not `know` the
relationship between the names of these frames and their ID codes.
The relationship must be specified via the appropriate kernel pool
frame definition.

.. code-block:: text

         FRAME_<name>              = <DSN Frame-ID>
         FRAME_<DSN Frame-ID>_NAME = '<name>'
         OBJECT_EARTH_FRAME        = <DSN Frame-ID>

Note that this specification leaves out the items below

.. code-block:: text

      FRAME_<DSN Frame-ID>_CENTER   = 399
      FRAME_<DSN Frame-ID>_CLASS    = 2
      FRAME_<DSN Frame-ID>_CLASS_ID = <DSN Frame-ID  - 10000>

You may supply these values if you like, but they have no effect on
the frame subsystem's recognition and interpretation of the frame
with the specified frame ID.


Appendix. Frame Definition Examples
=====================================

| Below are examples that you can modify to create frame
  specifications for similar situations.



Inertial Frames
---------------

| Inertial (class 1) frames cannot be defined in frame kernels; in
  particular, built-in definitions of class 1 frames cannot be
  overridden.

Aliases for inertial frames can be defined; see the section below on
creating aliases using TK frames.



PCK Frames
------------

| This definition shows how you create a frame definition for the
  asteroid Eros. Note we also define which frame is associated with
  the asteroid Eros.

.. code-block:: text

      \begindata

         FRAME_EROS_FIXED       =  2000433
         FRAME_2000433_NAME     = 'EROS_FIXED'
         FRAME_2000433_CLASS    =  2
         FRAME_2000433_CLASS_ID =  2000433
         FRAME_2000433_CENTER   =  2000433

         OBJECT_2000433_FRAME   = 'EROS_FIXED'

      \begintext



CK Frames
----------

| This definition shows how you create a frame definition for the MGS
  spacecraft. Note this frame definition includes the appropriate
  SCLK definition as well as which frame to attach to the MGS
  spacecraft.

.. code-block:: text

      \begindata

         FRAME_MGS_SPACECRAFT   = -94000
         FRAME_-94000_NAME      = 'MGS_SPACECRAFT'
         FRAME_-94000_CLASS     =  3
         FRAME_-94000_CLASS_ID  = -94000
         FRAME_-94000_CENTER    = -94

         CK_-94000_SCLK         = -94
         CK_-94000_SPK          = -94

         OBJECT_-94_FRAME       = 'MGS_SPACECRAFT'

      \begintext



TK frames
---------

| Examples of different uses of TK frames are shown below.



TK frame --- Alias
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| This example shows how you can make up an alias for a frame using a
  TK frame. Note we make the reference frame to associate with Mars
  the MARS_FIXED frame.

.. code-block:: text

      \begindata

         FRAME_MARS_FIXED       =  1400499
         FRAME_1400499_NAME     = 'MARS_FIXED'
         FRAME_1400499_CLASS    =  4
         FRAME_1400499_CLASS_ID =  1400499
         FRAME_1400499_CENTER   =  499

         OBJECT_499_FRAME       = 'MARS_FIXED'

      \begintext

      To make this point to another frame just replace
      'IAU_MARS' below with the name of that frame.

      \begindata

         TKFRAME_1400499_RELATIVE = 'IAU_MARS'
         TKFRAME_1400499_SPEC     = 'MATRIX'
         TKFRAME_1400499_MATRIX   = ( 1   0   0
                                      0   1   0
                                      0   0   1 )
      \begintext



TK frame --- Topographic
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| This example shows how you could create a topographic frame for the
  DSN Station DSS-17.

.. code-block:: text

      \begindata

         FRAME_DSS-17_TOPO      =  1399017
         FRAME_1399017_NAME     = 'DSS-17_TOPO'
         FRAME_1399017_CLASS    =  4
         FRAME_1399017_CLASS_ID =  1399017
         FRAME_1399017_CENTER   =   399017

         OBJECT_399017_FRAME    = 'DSS-17_TOPO'

      \begintext

      Note that the geodetic longitude and co-latitude of the DSS-17

      tracking station are: 243.126496675 and 54.657822839 respectively.

      \begindata

         TKFRAME_DSS-17_TOPO_RELATIVE = 'EARTH_FIXED'
         TKFRAME_DSS-17_TOPO_SPEC     = 'ANGLES'
         TKFRAME_DSS-17_TOPO_UNITS    = 'DEGREES'
         TKFRAME_DSS-17_TOPO_AXES     = ( 3, 2, 3 )
         TKFRAME_DSS-17_TOPO_ANGLES   = ( -243.126496675,
                                           -54.657822839,
                                           180.0 )
      \begintext

      Recall that the frame `EARTH_FIXED' is a TK frame. As a result
      its relationship to other frames must be specified via
      a kernel pool variable. We make that specification here.


      If the ITRF93 PCK kernel is not available we can simply rename the
      "RELATIVE" frame to be IAU_EARTH and still have the topocentric
      frame well defined.

      \begindata

         TKFRAME_EARTH_FIXED_RELATIVE = 'ITRF93'
         TKFRAME_EARTH_FIXED_SPEC     = 'MATRIX'
         TKFRAME_EARTH_FIXED_MATRIX   = ( 1   0   0
                                          0   1   0
                                          0   0   1 )

      \begintext



TK frame --- Instrument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| This example shows how you could create a TK frame for the Medium
  Resolution Imager (MRI) instrument on-board the Deep Impact Flyby
  (DIF) spacecraft.

The rotation from the DIF spacecraft frame to the MRI instrument
frame determined from the in-flight calibration data can be
represented by the following rotation angles:

.. code-block:: text

       mri

    M    = |0.129539306414|  * |-45.006884881185|  * |0.004898709285|

    sc                    Z                     Y                   X

The frame definition contains the opposite of these rotation angles
-- with the angle order reversed and the angle signs changed to the
opposite ones -- because the angles specified in it define the
transformation from the MRI frame to the spacecraft frame.

.. code-block:: text

      \begindata

         FRAME_DIF_MRI             = -140200
         FRAME_-140200_NAME        = 'DIF_MRI'
         FRAME_-140200_CLASS       = 4
         FRAME_-140200_CLASS_ID    = -140200
         FRAME_-140200_CENTER      = -140
         TKFRAME_-140200_SPEC      = 'ANGLES'
         TKFRAME_-140200_RELATIVE  = 'DIF_SPACECRAFT'
         TKFRAME_-140200_ANGLES    = ( -0.004898709285,
                                       45.006884881185,
                                       -0.129539306414 )
         TKFRAME_-140200_AXES      = ( 1,    2,   3   )
         TKFRAME_-140200_UNITS     = 'DEGREES'

      \begintext



Examples of Two-Vector Parameterized Dynamic Frames
----------------------------------------------------

|



Geocentric Solar Ecliptic (GSE) Frame
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Definition of the Geocentric Solar Ecliptic frame:

- All vectors are geometric: no aberration corrections are used.

- The position of the sun relative to the earth is the primary
  vector: the X axis points from the earth to the sun.

- The inertially referenced velocity of the sun relative to the
  earth is the secondary vector: the Y axis is the component of this
  velocity vector orthogonal to the X axis.

- The Z axis is X cross Y, completing the right-handed reference
  frame.

The GSE frame can be defined using the following assignments, where
<frame_ID> must be replaced by an integer ID code.

.. code-block:: text

      FRAME_GSE                       =  <frame_ID>
      FRAME_<frame_ID>_NAME           = 'GSE'
      FRAME_<frame_ID>_CLASS          =  5
      FRAME_<frame_ID>_CLASS_ID       =  <frame_ID>
      FRAME_<frame_ID>_CENTER         =  399
      FRAME_<frame_ID>_RELATIVE       = 'J2000'
      FRAME_<frame_ID>_DEF_STYLE      = 'PARAMETERIZED'
      FRAME_<frame_ID>_FAMILY         = 'TWO-VECTOR'
      FRAME_<frame_ID>_PRI_AXIS       = 'X'
      FRAME_<frame_ID>_PRI_VECTOR_DEF = 'OBSERVER_TARGET_POSITION'
      FRAME_<frame_ID>_PRI_OBSERVER   = 'EARTH'
      FRAME_<frame_ID>_PRI_TARGET     = 'SUN'
      FRAME_<frame_ID>_PRI_ABCORR     = 'NONE'
      FRAME_<frame_ID>_SEC_AXIS       = 'Y'
      FRAME_<frame_ID>_SEC_VECTOR_DEF = 'OBSERVER_TARGET_VELOCITY'
      FRAME_<frame_ID>_SEC_OBSERVER   = 'EARTH'
      FRAME_<frame_ID>_SEC_TARGET     = 'SUN'
      FRAME_<frame_ID>_SEC_ABCORR     = 'NONE'
      FRAME_<frame_ID>_SEC_FRAME      = 'J2000'



Geocentric Solar Magnetospheric (GSM) Frame
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Definition of the Geocentric Solar Magnetospheric frame:

- All vectors are geometric: no aberration corrections are used.

- The position of the sun relative to the earth is the primary
  vector: the X axis points from the earth to the sun.

- The earth's geomagnetic centered north dipole vector is
  secondary: the Z axis is the component of this vector orthogonal to
  the X axis. For the purpose of this definition, we treat the dipole
  vector as constant in the IAU_EARTH body-fixed frame. Note that in
  an earth-fixed reference frame, the north geomagnetic centered
  dipole is actually time-varying; the values shown here may be
  unsuitable for your application.

- The Y axis direction is the cross product of the Z-axis and
  the X-axis.

The GSM frame can be defined using the following assignments, where
<frame_ID> must be replaced by an integer ID code.

.. code-block:: text

      FRAME_GSM                       =  <frame_ID>
      FRAME_<frame_ID>_NAME           = 'GSM'
      FRAME_<frame_ID>_CLASS          =  5
      FRAME_<frame_ID>_CLASS_ID       =  <frame_ID>
      FRAME_<frame_ID>_CENTER         =  399
      FRAME_<frame_ID>_RELATIVE       = 'J2000'
      FRAME_<frame_ID>_DEF_STYLE      = 'PARAMETERIZED'
      FRAME_<frame_ID>_FAMILY         = 'TWO-VECTOR'
      FRAME_<frame_ID>_PRI_AXIS       = 'X'
      FRAME_<frame_ID>_PRI_VECTOR_DEF = 'OBSERVER_TARGET_POSITION'
      FRAME_<frame_ID>_PRI_OBSERVER   = 'EARTH'
      FRAME_<frame_ID>_PRI_TARGET     = 'SUN'
      FRAME_<frame_ID>_PRI_ABCORR     = 'NONE'
      FRAME_<frame_ID>_SEC_AXIS       = 'Z'
      FRAME_<frame_ID>_SEC_VECTOR_DEF = 'CONSTANT'
      FRAME_<frame_ID>_SEC_FRAME      = 'IAU_EARTH'
      FRAME_<frame_ID>_SEC_SPEC       = 'LATITUDINAL'
      FRAME_<frame_ID>_SEC_UNITS      = 'DEGREES'
      FRAME_<frame_ID>_SEC_LONGITUDE  =  288.43
      FRAME_<frame_ID>_SEC_LATITUDE   =   79.54



Mercury Solar Equatorial (MSEQ) Frame
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Definition of the Mercury Solar Equatorial Frame:

- All vectors are geometric: no aberration corrections are used.

- The sun's north spin axis direction is primary: the Z axis of
  the MSEQ frame is aligned with this spin axis.

- The position of the Sun relative to Mercury is secondary: the
  Y axis is aligned with the component of this position orthogonal to
  the Z axis.

- The X axis direction is the cross product of the Y axis and Z
  axis.

All vectors are geometric: no aberration corrections are used.
The MSEQ frame can be defined using the following assignments, where
<frame_ID> must be replaced by an integer ID code.

.. code-block:: text

      FRAME_MSEQ                      =  <frame_ID>
      FRAME_<frame_ID>_NAME           = 'MSEQ'
      FRAME_<frame_ID>_CLASS          =  5
      FRAME_<frame_ID>_CLASS_ID       =  <frame_ID>
      FRAME_<frame_ID>_CENTER         =  199
      FRAME_<frame_ID>_RELATIVE       = 'J2000'
      FRAME_<frame_ID>_DEF_STYLE      = 'PARAMETERIZED'
      FRAME_<frame_ID>_FAMILY         = 'TWO-VECTOR'
      FRAME_<frame_ID>_PRI_AXIS       = 'Z'
      FRAME_<frame_ID>_PRI_VECTOR_DEF = 'CONSTANT'
      FRAME_<frame_ID>_PRI_FRAME      = 'IAU_SUN'
      FRAME_<frame_ID>_PRI_SPEC       = 'RECTANGULAR'
      FRAME_<frame_ID>_PRI_VECTOR     =  ( 0, 0, 1 )
      FRAME_<frame_ID>_SEC_AXIS       = 'X'
      FRAME_<frame_ID>_SEC_VECTOR_DEF = 'OBSERVER_TARGET_POSITION'
      FRAME_<frame_ID>_SEC_OBSERVER   = 'MERCURY'
      FRAME_<frame_ID>_SEC_TARGET     = 'SUN'
      FRAME_<frame_ID>_SEC_ABCORR     = 'NONE'



Example: Nadir Frame for Mars Orbiting Spacecraft
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Definition of the nadir frame:

- All vectors are geometric: no aberration corrections are used.

- The Z axis points from the spacecraft to the closest point on
  Mars.

- The component of inertially referenced spacecraft velocity
  vector orthogonal to Z is aligned with the -X axis.

- The Y axis is the cross product of the Z axis and the X axis.

This nadir frame can be defined using the following assignments,
where

**<frame_name>**
   should be replaced by an actual frame name

**<orbiter_ID>**
   must be replaced with the integer ID code of the orbiter

**<orbiter_ID/name>**
   must be replaced with either the integer ID code of the orbiter or
   the name of the orbiter

**<frame_ID>**
   must be replaced by an integer ID code

.. code-block:: text

      FRAME_<frame_name>              = <frame_ID>
      FRAME_<frame_ID>_NAME           = <frame_name>
      FRAME_<frame_ID>_CLASS          = 5
      FRAME_<frame_ID>_CLASS_ID       = <frame_ID>
      FRAME_<frame_ID>_CENTER         = <orbiter_ID>
      FRAME_<frame_ID>_RELATIVE       = 'J2000'
      FRAME_<frame_ID>_DEF_STYLE      = 'PARAMETERIZED'
      FRAME_<frame_ID>_FAMILY         = 'TWO-VECTOR'
      FRAME_<frame_ID>_PRI_AXIS       = 'Z'
      FRAME_<frame_ID>_PRI_VECTOR_DEF = 'TARGET_NEAR_POINT'
      FRAME_<frame_ID>_PRI_OBSERVER   = <orbiter_ID/name>
      FRAME_<frame_ID>_PRI_TARGET     = 'MARS'
      FRAME_<frame_ID>_PRI_ABCORR     = 'NONE'
      FRAME_<frame_ID>_SEC_AXIS       = '-X'
      FRAME_<frame_ID>_SEC_VECTOR_DEF = 'OBSERVER_TARGET_VELOCITY'
      FRAME_<frame_ID>_SEC_OBSERVER   = <orbiter_ID/name>
      FRAME_<frame_ID>_SEC_TARGET     = 'MARS'
      FRAME_<frame_ID>_SEC_ABCORR     = 'NONE'
      FRAME_<frame_ID>_SEC_FRAME      = 'J2000'



Example: Roll-Celestial Spacecraft Frame
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| There are a variety of roll-celestial frames in use. This example
  may not match frame definitions used for any specific flight
  project; it is intended to demonstrate how to define this category
  of frame.

Definition of the roll-celestial frame:

- The Z axis points from the spacecraft to the earth. This
  vector is geometric (uncorrected).

- The component of an inertially referenced star direction
  vector orthogonal to the Z axis is the X axis. The star direction
  is provided by a specified star catalog in the form of right
  ascension and declination relative to the J2000 frame. If
  necessary, the RA/DEC coordinates should be adjusted for proper
  motion and parallax. This star direction vector is corrected for
  stellar aberration using the spacecraft as the observer.

- The Y axis is the cross product of the Z axis and the X axis.

This roll-celestial frame can be defined using the following
assignments, where

**<frame_name>**
   should be replaced by an actual frame name

**<spacecraft_ID>**
   must be replaced with the integer ID code of the spacecraft

**<spacecraft_ID/name>**
   must be replaced with either the integer ID code of the spacecraft
   or the name of the spacecraft

**<frame_ID>**
   must be replaced by an integer ID code

.. code-block:: text

      FRAME_<frame_name>              = <frame_ID>
      FRAME_<frame_ID>_NAME           = <frame_name>
      FRAME_<frame_ID>_CLASS          = 5
      FRAME_<frame_ID>_CLASS_ID       = <frame_ID>
      FRAME_<frame_ID>_CENTER         = <spacecraft_ID>
      FRAME_<frame_ID>_RELATIVE       = 'J2000'
      FRAME_<frame_ID>_DEF_STYLE      = 'PARAMETERIZED'
      FRAME_<frame_ID>_FAMILY         = 'TWO-VECTOR'
      FRAME_<frame_ID>_PRI_AXIS       = 'Z'
      FRAME_<frame_ID>_PRI_VECTOR_DEF = 'OBSERVER_TARGET_POSITION'
      FRAME_<frame_ID>_PRI_OBSERVER   = <spacecraft_ID/name>
      FRAME_<frame_ID>_PRI_TARGET     = 'EARTH'
      FRAME_<frame_ID>_PRI_ABCORR     = 'NONE'
      FRAME_<frame_ID>_SEC_AXIS       = 'X'
      FRAME_<frame_ID>_SEC_VECTOR_DEF = 'CONSTANT'
      FRAME_<frame_ID>_SEC_FRAME      = 'J2000'
      FRAME_<frame_ID>_SEC_SPEC       = 'RA/DEC'
      FRAME_<frame_ID>_SEC_UNITS      = 'DEGREES'
      FRAME_<frame_ID>_SEC_RA         = <star RA in degrees>
      FRAME_<frame_ID>_SEC_DEC        = <star DEC in degrees>
      FRAME_<frame_ID>_SEC_ABCORR     = 'S'
      FRAME_<frame_ID>_SEC_OBSERVER   = <spacecraft_ID/name>



Examples of Mean Equator and Equinox of Date Frames
----------------------------------------------------

|

Earth Mean Equator and Equinox of Date Frames
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| Definition of a non-inertial Earth Mean Equator and Equinox of Date
  frame using 1976 IAU precession model. Here <frame_name> must be
  replaced by a string containing the name of the frame, and
  <frame_ID> must be replaced by an integer ID code:

.. code-block:: text

      FRAME_<frame_name>             =  <frame_ID>
      FRAME_<frame_ID>_NAME          =  <frame_name>
      FRAME_<frame_ID>_CLASS         =  5
      FRAME_<frame_ID>_CLASS_ID      =  <frame_ID>
      FRAME_<frame_ID>_CENTER        =  399
      FRAME_<frame_ID>_RELATIVE      = 'J2000'
      FRAME_<frame_ID>_DEF_STYLE     = 'PARAMETERIZED'
      FRAME_<frame_ID>_FAMILY        = 'MEAN_EQUATOR_AND_EQUINOX_OF_DATE'
      FRAME_<frame_ID>_PREC_MODEL    = 'EARTH_IAU_1976'
      FRAME_<frame_ID>_ROTATION_STATE= 'ROTATING'

Definition for the inertial version of the above frame:

.. code-block:: text

      FRAME_<frame_name>             =  <frame_ID>
      FRAME_<frame_ID>_NAME          =  <frame_name>
      FRAME_<frame_ID>_CLASS         =  5
      FRAME_<frame_ID>_CLASS_ID      =  <frame_ID>
      FRAME_<frame_ID>_CENTER        =  399
      FRAME_<frame_ID>_RELATIVE      = 'J2000'
      FRAME_<frame_ID>_DEF_STYLE     = 'PARAMETERIZED'
      FRAME_<frame_ID>_FAMILY        = 'MEAN_EQUATOR_AND_EQUINOX_OF_DATE'
      FRAME_<frame_ID>_PREC_MODEL    = 'EARTH_IAU_1976'
      FRAME_<frame_ID>_ROTATION_STATE= 'INERTIAL'

Definition for the frozen version of the above frame, where the
`freeze epoch` is B1950 TDB. The resulting frame should match the
inertial frame B1950 to round-off level:

.. code-block:: text

      FRAME_<frame_name>             =  <frame_ID>
      FRAME_<frame_ID>_NAME          =  <frame_name>
      FRAME_<frame_ID>_CLASS         =  5
      FRAME_<frame_ID>_CLASS_ID      =  <frame_ID>
      FRAME_<frame_ID>_CENTER        =  399
      FRAME_<frame_ID>_RELATIVE      = 'J2000'
      FRAME_<frame_ID>_DEF_STYLE     = 'PARAMETERIZED'
      FRAME_<frame_ID>_FAMILY        = 'MEAN_EQUATOR_AND_EQUINOX_OF_DATE'
      FRAME_<frame_ID>_PREC_MODEL    = 'EARTH_IAU_1976'
      FRAME_<frame_ID>_FREEZE_EPOCH  = @1949-DEC-31/22:09:46.861901



Examples of True Equator and Equinox of Date Frames
----------------------------------------------------

| Definition of the Earth True Equator and Equinox of Date frame:

- The earth precession model is the 1976 IAU model.

- The earth nutation model is the 1980 IAU model.

Here <frame_name> must be replaced by a string containing the name of
the frame, and <frame_ID> must be replaced by an integer ID code:

.. code-block:: text

      FRAME_<frame_name>             =  <frame_ID>
      FRAME_<frame_ID>_NAME          =  <frame_name>
      FRAME_<frame_ID>_CLASS         =  5
      FRAME_<frame_ID>_CLASS_ID      =  <frame_ID>
      FRAME_<frame_ID>_CENTER        =  399
      FRAME_<frame_ID>_RELATIVE      = 'J2000'
      FRAME_<frame_ID>_DEF_STYLE     = 'PARAMETERIZED'
      FRAME_<frame_ID>_FAMILY        = 'TRUE_EQUATOR_AND_EQUINOX_OF_DATE'
      FRAME_<frame_ID>_PREC_MODEL    = 'EARTH_IAU_1976'
      FRAME_<frame_ID>_NUT_MODEL     = 'EARTH_IAU_1980'
      FRAME_<frame_ID>_ROTATION_STATE= 'ROTATING'

Definition for the inertial version of the above frame:

.. code-block:: text

      FRAME_<frame_name>             =  <frame_ID>
      FRAME_<frame_ID>_NAME          =  <frame_name>
      FRAME_<frame_ID>_CLASS         =  5
      FRAME_<frame_ID>_CLASS_ID      =  <frame_ID>
      FRAME_<frame_ID>_CENTER        =  399
      FRAME_<frame_ID>_RELATIVE      = 'J2000'
      FRAME_<frame_ID>_DEF_STYLE     = 'PARAMETERIZED'
      FRAME_<frame_ID>_FAMILY        = 'TRUE_EQUATOR_AND_EQUINOX_OF_DATE'
      FRAME_<frame_ID>_PREC_MODEL    = 'EARTH_IAU_1976'
      FRAME_<frame_ID>_NUT_MODEL     = 'EARTH_IAU_1980'
      FRAME_<frame_ID>_ROTATION_STATE= 'INERTIAL'

Definition for the frozen version of the above frame, where the
`freeze epoch` is B1950 TDB.

.. code-block:: text

      FRAME_<frame_name>             =  <frame_ID>
      FRAME_<frame_ID>_NAME          =  <frame_name>
      FRAME_<frame_ID>_CLASS         =  5
      FRAME_<frame_ID>_CLASS_ID      =  <frame_ID>
      FRAME_<frame_ID>_CENTER        =  399
      FRAME_<frame_ID>_RELATIVE      = 'J2000'
      FRAME_<frame_ID>_DEF_STYLE     = 'PARAMETERIZED'
      FRAME_<frame_ID>_FAMILY        = 'TRUE_EQUATOR_AND_EQUINOX_OF_DATE'
      FRAME_<frame_ID>_PREC_MODEL    = 'EARTH_IAU_1976'
      FRAME_<frame_ID>_NUT_MODEL     = 'EARTH_IAU_1980'
      FRAME_<frame_ID>_FREEZE_EPOCH  = @1949-DEC-31/22:09:46.861901



Example of a Mean Ecliptic and Equinox of Date Frame
-----------------------------------------------------

| Definition of the Earth Mean Ecliptic and Equinox of Date frame:

- The earth precession model is the 1976 IAU model.

- The earth mean obliquity model is the 1980 IAU model.

Here <frame_name> must be replaced by a string containing the name of
the frame, and <frame_ID> must be replaced by an integer ID code:

.. code-block:: text

      FRAME_<frame_name>             =  <frame_ID>
      FRAME_<frame_ID>_NAME          =  <frame_name>
      FRAME_<frame_ID>_CLASS         =  5
      FRAME_<frame_ID>_CLASS_ID      =  <frame_ID>
      FRAME_<frame_ID>_CENTER        =  399
      FRAME_<frame_ID>_RELATIVE      = 'J2000'
      FRAME_<frame_ID>_DEF_STYLE     = 'PARAMETERIZED'
      FRAME_<frame_ID>_FAMILY        = 'MEAN_ECLIPTIC_AND_EQUINOX_OF_DATE'
      FRAME_<frame_ID>_PREC_MODEL    = 'EARTH_IAU_1976'
      FRAME_<frame_ID>_OBLIQ_MODEL   = 'EARTH_IAU_1980'
      FRAME_<frame_ID>_ROTATION_STATE= 'ROTATING'

Definition for the inertial version of the above frame:

.. code-block:: text

      FRAME_<frame_name>             =  <frame_ID>
      FRAME_<frame_ID>_NAME          =  <frame_name>
      FRAME_<frame_ID>_CLASS         =  5
      FRAME_<frame_ID>_CLASS_ID      =  <frame_ID>
      FRAME_<frame_ID>_CENTER        =  399
      FRAME_<frame_ID>_RELATIVE      = 'J2000'
      FRAME_<frame_ID>_DEF_STYLE     = 'PARAMETERIZED'
      FRAME_<frame_ID>_FAMILY        = 'MEAN_ECLIPTIC_AND_EQUINOX_OF_DATE'
      FRAME_<frame_ID>_PREC_MODEL    = 'EARTH_IAU_1976'
      FRAME_<frame_ID>_OBLIQ_MODEL   = 'EARTH_IAU_1980'
      FRAME_<frame_ID>_ROTATION_STATE= 'INERTIAL'

Definition for the frozen version of the above frame, where the
`freeze epoch` is B1950 TDB.

.. code-block:: text

      FRAME_<frame_name>             =  <frame_ID>
      FRAME_<frame_ID>_NAME          =  <frame_name>
      FRAME_<frame_ID>_CLASS         =  5
      FRAME_<frame_ID>_CLASS_ID      =  <frame_ID>
      FRAME_<frame_ID>_CENTER        =  399
      FRAME_<frame_ID>_RELATIVE      = 'J2000'
      FRAME_<frame_ID>_DEF_STYLE     = 'PARAMETERIZED'
      FRAME_<frame_ID>_FAMILY        = 'MEAN_ECLIPTIC_AND_EQUINOX_OF_DATE'
      FRAME_<frame_ID>_PREC_MODEL    = 'EARTH_IAU_1976'
      FRAME_<frame_ID>_OBLIQ_MODEL   = 'EARTH_IAU_1980'
      FRAME_<frame_ID>_FREEZE_EPOCH  = @1949-DEC-31/22:09:46.861901



Example of an Euler Frame
-------------------------

| As an example, we construct an Euler frame called IAU_MARS_EULER.
  Frame IAU_MARS_EULER is mathematically identical to the PCK frame
  IAU_MARS.

The PCK data defining the underlying IAU_MARS frame are:

.. code-block:: text

      BODY499_POLE_RA          = (  317.68143   -0.1061      0.  )
      BODY499_POLE_DEC         = (   52.88650   -0.0609      0.  )
      BODY499_PM               = (  176.630    350.89198226  0.  )

These values are from:

.. code-block:: text


 Seidelmann, P.K., Abalakin, V.K., Bursa, M., Davies, M.E., Bergh, C.
      de, Lieske, J.H., Oberst, J., Simon, J.L., Standish, E.M.,

  Stooke, P., and Thomas, P.C. (2002). "Report of the IAU/IAG Working

     Group on Cartographic Coordinates and Rotational Elements of the

     Planets and Satellites: 2000," Celestial Mechanics and Dynamical
      Astronomy, v.82, Issue 1, pp. 83-111.

Here pole RA/Dec terms in the PCK are in degrees and degrees/century;
the rates here have been converted to degrees/sec. Prime meridian
terms in the PCK are in degrees and degrees/day; the rate here has
been converted to degrees/sec.
The 3x3 transformation matrix M defined by the angles is

.. code-block:: text

      M = [angle_1]   [angle_2]   [angle_3]
                   3           1           3

Vectors are mapped from the J2000 base frame to the IAU_MARS frame
via left multiplication by M.
The relationship of these Euler angles to RA/Dec/PM for the
J2000-to-IAU Mars body-fixed transformation is as follows:

.. code-block:: text

      angle_1 is        PM  * (radians/degree)
      angle_2 is pi/2 - Dec * (radians/degree)
      angle_3 is pi/2 + RA  * (radians/degree)

Since when we define the IAU_MARS_EULER frame we're defining the
\*inverse\* of the above transformation, the angles for our Euler
frame definition are reversed and the signs negated:

.. code-block:: text

      angle_1 is -pi/2 - RA  * (radians/degree)
      angle_2 is -pi/2 + Dec * (radians/degree)
      angle_3 is       - PM  * (radians/degree)

Then our frame definition is:

.. code-block:: text

      FRAME_IAU_MARS_EULER            =  <frame_ID>
      FRAME_<frame_ID>_NAME           = 'IAU_MARS_EULER'
      FRAME_<frame_ID>_CLASS          =  5
      FRAME_<frame_ID>_CLASS_ID       =  <frame_ID>
      FRAME_<frame_ID>_CENTER         =  499
      FRAME_<frame_ID>_RELATIVE       = 'J2000'
      FRAME_<frame_ID>_DEF_STYLE      = 'PARAMETERIZED'
      FRAME_<frame_ID>_FAMILY         = 'EULER'
      FRAME_<frame_ID>_EPOCH          =  @2000-JAN-1/12:00:00
      FRAME_<frame_ID>_AXES           =  ( 3  1  3 )
      FRAME_<frame_ID>_UNITS          = 'DEGREES'
      FRAME_<frame_ID>_ANGLE_1_COEFFS = (  -47.68143
                                            0.33621061170684714E-10 )
      FRAME_<frame_ID>_ANGLE_2_COEFFS = (  -37.1135
                                           -0.19298045478743630E-10 )
      FRAME_<frame_ID>_ANGLE_3_COEFFS = ( -176.630
                                           -0.40612497946759260E-02 )



Examples of Product Frames
--------------------------

|



IAU_EARTH Frame, Augmented with Nutation Model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| The example shown here is not realistic; it is provided only to
  show how to create a product frame specification.

The EARTH_ROTATING frame defined uses the Earth spin angle relative
to the mean equinox of date from the IAU_EARTH frame and pole and
equinox from the Earth true equator and true equinox of date frame.
While the pole direction of the IAU_EARTH frame reflects precession,
the pole direction of this frame reflects both precession and
nutation.

The transformation from the J2000 frame to the product frame is
defined by:

.. code-block:: text

        EARTH_ROTATING       IAU_EARTH       TETE
      T                =   T            *  T
        J2000                EME             J2000

where the notation

.. code-block:: text

        B
      T
        A

indicates the transformation from frame A to frame B.
The specifications of the frame and of the two supporting frames EME
and TETE are shown below.

.. code-block:: text

      \begindata

      FRAME_EARTH_ROTATING          =  1890000
      FRAME_1890000_NAME            =  'EARTH_ROTATING'
      FRAME_1890000_CLASS           =  5
      FRAME_1890000_CLASS_ID        =  1890000
      FRAME_1890000_CENTER          =  399
      FRAME_1890000_RELATIVE        = 'J2000'
      FRAME_1890000_DEF_STYLE       = 'PARAMETERIZED'
      FRAME_1890000_FAMILY          = 'PRODUCT'
      FRAME_1890000_ROTATION_STATE  = 'ROTATING'
      FRAME_1890000_FROM_FRAMES     = ( 'EME',       'J2000' )
      FRAME_1890000_TO_FRAMES       = ( 'IAU_EARTH', 'TETE'  )

      \begintext

      Earth mean equator and mean equinox of date frame "EME":

      \begindata

      FRAME_EME                     =  1890001
      FRAME_1890001_NAME            =  'EME'
      FRAME_1890001_CLASS           =  5
      FRAME_1890001_CLASS_ID        =  1890001
      FRAME_1890001_CENTER          =  399
      FRAME_1890001_RELATIVE        = 'J2000'
      FRAME_1890001_DEF_STYLE       = 'PARAMETERIZED'
      FRAME_1890001_FAMILY          = 'MEAN_EQUATOR_AND_EQUINOX_OF_DATE'
      FRAME_1890001_PREC_MODEL      = 'EARTH_IAU_1976'
      FRAME_1890001_ROTATION_STATE  = 'ROTATING'

      \begintext

      Earth true equator and true equinox of date frame "TETE":

      \begindata

      FRAME_TETE                    =  1890002
      FRAME_1890002_NAME            =  'TETE'
      FRAME_1890002_CLASS           =  5
      FRAME_1890002_CLASS_ID        =  1890002
      FRAME_1890002_CENTER          =  399
      FRAME_1890002_RELATIVE        = 'J2000'
      FRAME_1890002_DEF_STYLE       = 'PARAMETERIZED'
      FRAME_1890002_FAMILY          = 'TRUE_EQUATOR_AND_EQUINOX_OF_DATE'
      FRAME_1890002_PREC_MODEL      = 'EARTH_IAU_1976'
      FRAME_1890002_NUT_MODEL       = 'EARTH_IAU_1980'
      FRAME_1890002_ROTATION_STATE  = 'ROTATING'

      \begintext

In order for this frame to be generally useful, a more accurate Earth
spin model than that provided by the IAU_EARTH frame would need to be
used. In practice, high-precision binary Earth PCKs are more suitable
as a source of accurate Earth orientation data.


Dog-Leg Frame for Saturn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| A `Dog-Leg` frame for Saturn is a realistic application of
  product frames. The specification of this frame is quite complex.
  Contact NAIF for details.



Examples of Switch Frames
-------------------------

| In the examples below, all frame names and ID codes are fictitious.



Switch Frame Using Reconstructed and Predict CKs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| In this example, a switch frame uses distinct CK base frames for
  reconstructed and predicted data. The two CK frames use different
  spacecraft clocks.

The specification for such a switch frame would have the form:

.. code-block:: text

      \begindata

      FRAME_SWITCH1              = -123001
      FRAME_-123001_NAME         = 'SWITCH1'
      FRAME_-123001_CLASS        = 6
      FRAME_-123001_CLASS_ID     = -123001
      FRAME_-123001_CENTER       = -123
      FRAME_-123001_ALIGNED_WITH = (
                                      'CK_PREDICTED'
                                      'CK_RECONSTRUCTED'
                                   )
      \begintext

The base frames, which are specified by the assignment of the kernel
variable FRAME\_-123001_ALIGNED_WITH, are listed in order of
increasing priority: given a request time, the SWITCH1 frame first
tries to get orientation of the frame CK_RECONSTRUCTED; if not found,
it tries to get orientation of the frame CK_PREDICTED.
The CK frames referenced by this switch frame must be defined, and
the corresponding CKs loaded, along with associated SCLK kernels and
a leapseconds kernel, for the switch frame to be usable.

Loading the CKs without loading an FK that defines the CK frames
would not work. Examples of the CK frame definitions are shown below.

Reconstructed attitude CK frame:

.. code-block:: text

      \begindata

      FRAME_CK_RECONSTRUCTED = -123501
      FRAME_-123501_NAME     = 'CK_RECONSTRUCTED'
      FRAME_-123501_CLASS    = 3
      FRAME_-123501_CLASS_ID = -123601
      FRAME_-123501_CENTER   = -123
      CK_-123501_SCLK        = -123

      \begintext

Predicted attitude CK frame:

.. code-block:: text

      \begindata

      FRAME_CK_PREDICTED     = -123502
      FRAME_-123502_NAME     = 'CK_PREDICTED'
      FRAME_-123502_CLASS    = 3
      FRAME_-123502_CLASS_ID = -123602
      FRAME_-123502_CENTER   = -123
      CK_-123502_SCLK        = -123000

      \begintext

Base frames may also be specified by frame ID, so the `aligned
with` assignment may be written as

.. code-block:: text

      \begindata

      FRAME_-123001_ALIGNED_WITH = (
                                      -123502
                                      -123501
                                   )
      \begintext

Note that the frame ID of a CK frame might not match the frame's
frame class ID, which is the ID used in CKs providing data for that
frame. In this case, the IDs used in reconstructed and predicted CKs
would be -123601 and -123602 respectively. Using those IDs in the
`aligned with` assignment would not work.


Switch Frame Using CK and Dynamic Frames
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| This switch frame uses CK frames for reconstructed and predicted
  data as in the previous example, and it uses dynamic frames
  providing nominal attitude for the cruise and orbit mission phases,
  for times when no CK data are available.

This example is for a seven year long mission:

.. code-block:: text

      launch          -- 2018-01-01
      orbit insertion -- 2018-10-01
      end of mission  -- 2025-01-01

The CK frames are applicable for the entire mission.
The nominal cruise attitude is implemented by the dynamic frame
DYN_CRUISE (definition not shown). This frame is applicable only for
the cruise phase of the mission.

The nominal orbital attitude is implemented by the dynamic frame
DYN_ORBIT (definition not shown). This frame is applicable only for
the orbital phase of the mission.

The CK frames are listed last in the set of base frame names, so they
have highest priority.

Start and stop times below are expressed in text kernel format. The
times are interpreted as TDB calendar dates.

.. code-block:: text

      \begindata

      FRAME_SWITCH2              = -123002
      FRAME_-123002_NAME         = 'SWITCH2'
      FRAME_-123002_CLASS        = 6
      FRAME_-123002_CLASS_ID     = -123001
      FRAME_-123002_CENTER       = -123

      FRAME_-123002_ALIGNED_WITH = (
                                      'DYN_CRUISE'
                                      'DYN_ORBIT'
                                      'CK_PREDICTED'
                                      'CK_RECONSTRUCTED'
                                   )

      FRAME_-123002_START        = (
                                      @2018-01-01
                                      @2018-10-01
                                      @2018-01-01
                                      @2018-01-01
                                   )

      FRAME_-123002_STOP         = (
                                      @2018-10-01
                                      @2025-01-01
                                      @2025-01-01
                                      @2025-01-01
                                   )
      \begintext

Time strings recognized by the CSPICE function
:py:meth:`~spiceypy.spiceypy.str2et` also may be used. We could
define the interval start times using the assignment

.. code-block:: text

      \begindata

      FRAME_-123002_START        = (
                                      '2018 JAN 1 00:00:00.000 TDB'
                                      '2018 OCT 1 00:00:00.000 TDB'
                                      '2018 JAN 1 00:00:00.000 TDB'
                                      '2018 JAN 1 00:00:00.000 TDB'
                                   )
      \begintext



Predicted Attitude Profile for Observation Planning
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

| In this example, a sequence of base frames provides nominal
  predicted pointing, over a short time period, for a spacecraft
  observing a target object.

This example is for two six-hour long orbits, each broken into equal
chunks for Sun-pointing, Earth-pointing, and observation modes.
Pointing transitions are abrupt: at each transition time, the switch
frame instantaneously changes its orientation from that of one base
frame that of the next.

The nominal Sun-pointing attitude is implemented by the dynamic frame
DYN_SUN_POINTING (definition not shown).

The nominal Earth-pointing attitude is implemented by the dynamic
frame DYN_EARTH_POINTING (definition not shown).

The nominal observation attitude is implemented by the dynamic frame
DYN_OBSERVATION (definition not shown).

.. code-block:: text

      \begindata

         FRAME_SWITCH3              = -123003
         FRAME_-123003_NAME         = 'SWITCH3'
         FRAME_-123003_CLASS        = 6
         FRAME_-123003_CLASS_ID     = -123003
         FRAME_-123003_CENTER       = -123
         FRAME_-123003_ALIGNED_WITH = (
                                         'DYN_SUN_POINTING'
                                         'DYN_EARTH_POINTING'
                                         'DYN_OBSERVATION'
                                         'DYN_SUN_POINTING'
                                         'DYN_EARTH_POINTING'
                                         'DYN_OBSERVATION'
                                      )

         FRAME_-123003_START        = (
                                         @2018-01-01/00:00:00
                                         @2018-01-01/02:00:00
                                         @2018-01-01/04:00:00
                                         @2018-01-01/06:00:00
                                         @2018-01-01/08:00:00
                                         @2018-01-01/10:00:00
                                      )

         FRAME_-123003_STOP         = (
                                         @2018-01-01/02:00:00
                                         @2018-01-01/04:00:00
                                         @2018-01-01/06:00:00
                                         @2018-01-01/08:00:00
                                         @2018-01-01/10:00:00
                                         @2018-01-01/12:00:00
                                      )
      \begintext

Because the time intervals associated with the base frames are listed
in increasing time order and overlap only at their endpoints, request
times will be mapped to time intervals by binary search. If the time
intervals were listed in any other order, a linear search would be
used.

