*********************
NAIF Integer ID codes
*********************

This required reading document is reproduced from the original NAIF
document available at `https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/naif_ids.html <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/naif_ids.html>`_

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

| The NAIF IDS Required Reading lists all default body ID-name
  mappings for the SPICE toolkits and a description of functionality
  of the corresponding software.


Introduction
============

| SPICE system kernels and routines refer to ephemeris objects,
  reference frames, and instruments by integer codes, usually
  referred as the ID.

The reference frame ID-name mappings routines constitute a subsystem
separate from the body ID-name mapping routines. Please refer to the
Frames Required Reading document
(`frames <./frames.html>`__) for specific information.

Likewise, the surface ID-name mappings routines constitute a
subsystem separate from the body ID-name mapping routines. Please
refer to the DSK Required Reading document
(`dsk.req <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/dsk.html>`__) for specific information.

An ephemeris object is any object that may have ephemeris or
trajectory data such as a planet, natural satellite, tracking
station, spacecraft, barycenter (the center of mass of a group of
bodies), asteroid, or comet. Each body in the solar system is
associated with an integer code for use with SPICE. The names and
codes for many of these objects are listed below.

Spacecraft ID codes are negative. These ID codes are usually derived
from NASA control authority assignments. Instruments mounted on
spacecraft also have ID codes. These are determined by multiplying
the spacecraft ID by 1000 and subtracting the ordinal number of the
instrument from the resulting product. Thus we can algorithmically
recover the spacecraft code from an instrument code, and each
instrument may have a unique code as long as there are 999 or fewer
on a spacecraft.

Caution: the NASA spacecraft ID control authority at GSFC is forced
into reusing some IDs. This can affect the SPICE system for planetary
or other spacecraft for which ID-name mappings are registered. (Here
"registered" means a spacecraft for which use of the SPICE system is
an actuality, or was contemplated.) Three cases exist.

#. This document and ID-to-name mapping software include both
   past and current ID-name mappings for cases where both the old and
   the new ID assignments are for spacecraft registered within SPICE.
   The last mentioned ID-to-name mapping in this document is the one
   that will be used in SPICE software to effect ID-to-name
   translations within SPICE-based code.

#. This document and ID-to-name mapping software contain only a
   mapping for the current use of a given ID if prior uses involved
   spacecraft never registered with SPICE (e.g. many non-planetary
   missions).

#. This document and ID-to-name mapping software contain only a
   mapping for a prior use of a given ID if that prior use was for a
   spacecraft registered within SPICE and current use of the ID is for
   a spacecraft not registered within SPICE.

For spacecraft the ID-to-name mapping may be a one-to-many mapping,
allowing two or more names for a spacecraft to exist for a single
numeric ID. The last mentioned ID-to-name mapping in this document is
the one that will be used in SPICE software to effect ID-to-name
translations within SPICE-based code.
As the reader will see, ID codes now show the wear that results from
an expanding system. As the SPICE system has expanded so has the
number of objects that require identifying codes. Many of these
objects do not fit neatly into the schemes originally envisioned as
needing ID codes. As a result, the current system is a bit eclectic.


Use of Code-to-Name/Name-to-Code Mappings from SPICE
====================================================

| Software exists within the SPICE system that allows a user to
  easily map between an integer code and the object name that code
  represents or vice-versa.

:py:meth:`~spiceypy.spiceypy.bodc2n` performs the integer code to
name mapping; input a code, the routine returns the corresponding
name:

::

         from spiceypy import *
         bodc2n( code )



:py:meth:`~spiceypy.spiceypy.bodn2c` performs the name to integer
code mapping; input a name, the routine returns the corresponding ID
code:
::

         bodn2c( name )

:py:meth:`~spiceypy.spiceypy.boddef` performs a run-time assignment
of a name/code mapping for later translation by
:py:meth:`~spiceypy.spiceypy.bodc2n` and
:py:meth:`~spiceypy.spiceypy.bodn2c`:
::

         boddef( name, code )

with \`name' defining the character string associated with integer
\`code'. When using :py:meth:`~spiceypy.spiceypy.bodn2c`, the
\`name' look-up is case insensitive, left justified, and space
compressed (multiple spaces between words reduced to one) format.
Spaces between words are significant.

.. attention::
   These strings are equivalent:
      'EARTH', '  Earth ', 'earth  '
   As well as:
      'Solar System Barycenter', 'SOLAR  System  barycenter'
   but:
      'SolarSystemBarycenter'

   is not due to the lack of spaces between words.


SpiceyPy by default does not return `found` boolean variables for functions from CSPICE functions
and instead raises a :py:exc:`spiceypy.utils.exceptions.NotFoundError` when the flag is `False`. This behavior can be configured
or disabled as described in `Exceptions in SpiceyPy <./exceptions.html>`__.


Use of an External Mapping Definition Kernel
--------------------------------------------

| If necessary, a user may elect to load additional name-ID pairs for
  access by SPICE software. These pairs may be new definitions, or
  they may override the default mapping assignment.

Create new name-ID pairs With a text kernel such as

.. code-block:: text

         \begintext

         Define an additional set of body, ID code mappings.

         \begindata

         NAIF_BODY_CODE  += ( 22, 23, 24, 25 )

         NAIF_BODY_NAME  += ( 'LARRY', 'MOE', 'CURLEY', 'SHEMP' )

Load the kernel as usual with a
:py:meth:`~spiceypy.spiceypy.furnsh` call. The names defined in
NAIF_BODY_NAME map to the corresponding index of NAIF_BODY_CODE, i.e.
LARRY->22, MOE->23, etc, and the IDs in NAIF_BODY_CODE map to the
corresponding index of NAIF_BODY_NAME.
If an external ID kernel is used, be aware of several rules:

#. All ID codes MUST be listed in the kernel variable
   NAIF_BODY_CODE, and all names MUST be listed in the kernel variable
   NAIF_BODY_NAME.

#. The CSPICE system can access 14983 external name-ID pairs
   defined via a text kernel. CSPICE signals an error when the number
   of assignments exceeds 14983.

#. Names must be no longer than 36 characters. SPICE truncates
   characters beyond 36th without signaling an error.

#. You may assign an ID code to multiple names. A
   :py:meth:`~spiceypy.spiceypy.bodc2n` call returns the last name
   assigned; a last in, first out situation.

Since NAIF_BODY_CODE and NAIF_BODY_NAME are kernel variables, use of
the "+=" notation in the previous example means the values are
appended to the mapping set present in memory. For example, the
block:
.. code-block:: text

         \begindata

         NAIF_BODY_CODE  += ( 170100, 170101 )

         NAIF_BODY_NAME  += ( 'Enterprise', 'Enterprise-A' )

appends the two pairings to the existent set of mappings.
CAUTION: Use of the assignment operator, ''='', instead of the append
operator, ''+='', destroys any previous name-ID definitions for a
kernel variable.


Masking
-------

| As of release N53, the SPICE Toolkit provides the user the
  functionality to override or mask any name/ID mapping. Use a
  :py:meth:`~spiceypy.spiceypy.boddef` call or define
  NAIF_BODY_NAME, NAIF_BODY_CODE assignments from a text kernel to
  perform a masking operations. Simplistically, the mask
  functionality provides the user the option of mapping multiple
  names to the same code.

Name/ID assignments function within a precedence hierarchy, so a
lower precedence operation cannot affect previous assignments created
by an operation of higher precedence. Kernel pool definitions have
the highest precedence, :py:meth:`~spiceypy.spiceypy.boddef`
definitions next, and finally the default definitions. The order of
assignments is significant.

.. code-block:: text

  Highest precedence

  (1) Kernel pool final assignment

  (2) Kernel pool initial assignment

  (3) A ``boddef'' call final assignment

  (4) A ``boddef'' call initial assignment

  (5) The default mappings final assignment

  (6) The default mappings initial assignment

  Lowest precedence

Example 1:
Assign the name 'x' (lower case) to ID 1000 with
:py:meth:`~spiceypy.spiceypy.boddef`:

::

         boddef( "x", 1000 )

A call to :py:meth:`~spiceypy.spiceypy.bodc2n` with 1000 as the
input ID:
::

        name = bodc2n( 1000 )

returns the name 'x'. The :py:meth:`~spiceypy.spiceypy.bodn2c`
calls:
::

         bodn2c( "x" )
         bodn2c( "X" )

both return the ID as 1000. Note the case insensitivity of the name
input.
Now a demo of simple masking functionality. Assign a new name to ID
1000:

::

         boddef( "Y", 1000 )

so the :py:meth:`~spiceypy.spiceypy.bodn2c` call
::

         bodn2c( "Y" )

returns an ID of 1000. In a similar manner, the
:py:meth:`~spiceypy.spiceypy.bodc2n` call:
::

         bodc2n( 1000 )

returns the name 'Y'. Still, the code assigned to 'x' persists within
SPICE as the call:
::

         bodn2c( "x" )

also returns ID 1000. If we reassign 'Y' to a different ID:
::

         boddef( "Y", 1001 )

then make a :py:meth:`~spiceypy.spiceypy.bodc2n` call with 1000 as
the input ID:
::

         bodc2n( 1000 )

the routine returns the name 'x'. We assigned an ID to 'x', masked it
with another name, then demasked it by reassigning the masking name,
'Y'.
If a :py:meth:`~spiceypy.spiceypy.boddef` assigns an existing name
to an existing code, that assignment takes precedence.

Example 2:

::

         bodn2c( "THEBE" )

returns a code value 514. Likewise
::

         bodc2n( 514 )

returns a name of 'THEBE'. Yet the name '1979J2' also maps to code
514, but with lower precedence.
The :py:meth:`~spiceypy.spiceypy.boddef` call:

::

         boddef( "1979J2", 514 )

places the '1979J2' <-> 514 mapping at the top of the precedence
list, so:
::

         bodc2n( 514 )

returns the name '1979J2'. Note, 'THEBE' still resolves to 514.
In those cases where a kernel pool assignment overrides a
:py:meth:`~spiceypy.spiceypy.boddef`, the
:py:meth:`~spiceypy.spiceypy.boddef` mapping 'reappears' when an
:py:meth:`~spiceypy.spiceypy.unload`, :py:meth:`~spiceypy.spiceypy.kclear` or :py:meth:`~spiceypy.spiceypy.clpool` call
clears the kernel pool mappings.

Example 3:

Execute a :py:meth:`~spiceypy.spiceypy.boddef` call:

::

         boddef( "vehicle2", -1010 )

A :py:meth:`~spiceypy.spiceypy.bodc2n` call:
::

         bodc2n( -1010 )

returns the name 'vehicle2' as expected. If you then load the name/ID
kernel body.ker:
::

         \begindata

         NAIF_BODY_NAME = ( 'vehicle1' )
         NAIF_BODY_CODE = ( -1010      )

         \begintext

with :py:meth:`~spiceypy.spiceypy.furnsh`:
::

         furnsh( "body.ker" )

the :py:meth:`~spiceypy.spiceypy.bodc2n` call:
::

         bodc2n( -1010 )

returns 'vehicle1' since the kernel assignment take precedence over
the :py:meth:`~spiceypy.spiceypy.boddef` assignment.
The name/ID map state:

.. code-block:: text

          -1010    -> vehicle1
          vehicle1 -> -1010
          vehicle2 -> -1010

Now, unload the body kernel:
::

         unload( "body.ker" )

The :py:meth:`~spiceypy.spiceypy.boddef` assignment resumes highest
precedence.
::

         bodc2n( -1010 )

The call returns 'vehicle2' for the name.
CAUTION: Please understand a :py:meth:`~spiceypy.spiceypy.clpool`
or :py:meth:`~spiceypy.spiceypy.kclear` call deletes all mapping
assignments defined through the kernel pool. No similar clear
functionality exists to clear :py:meth:`~spiceypy.spiceypy.boddef`.
:py:meth:`~spiceypy.spiceypy.boddef` assignments persist unless explicitly overridden.


NAIF Object ID numbers
======================

| In theory, a unique integer can be assigned to each body in the
  solar system, including interplanetary spacecraft. SPICE uses
  integer codes instead of names to refer to ephemeris bodies for
  three reasons.

#. Space
    * Integer codes are smaller than alphanumeric names.
#. Uniqueness
    * The names of some satellites conflict with the names of some
      asteroids and comets. Also, some satellites are commonly referred
      to by names other than those approved by the IAU.
#. Context
    * The type of a body (barycenter, planet, satellite, comet,
      asteroid, or spacecraft) and the system to which it belongs (Earth,
      Mars, Jupiter, Saturn, Uranus, Neptune, or Pluto) can be recovered
      algorithmically from the integer code assigned to a body. This is
      not generally true for names.



Barycenters
-----------

| The smallest positive codes are reserved for the Sun and planetary
  barycenters:

.. code-block:: text

         NAIF ID     NAME
         ________    ____________________
         0           'SOLAR_SYSTEM_BARYCENTER'
         0           'SSB'
         0           'SOLAR SYSTEM BARYCENTER'
         1           'MERCURY_BARYCENTER'
         1           'MERCURY BARYCENTER'
         2           'VENUS_BARYCENTER'
         2           'VENUS BARYCENTER'
         3           'EARTH_BARYCENTER'
         3           'EMB'
         3           'EARTH MOON BARYCENTER'
         3           'EARTH-MOON BARYCENTER'
         3           'EARTH BARYCENTER'
         4           'MARS_BARYCENTER'
         4           'MARS BARYCENTER'
         5           'JUPITER_BARYCENTER'
         5           'JUPITER BARYCENTER'
         6           'SATURN_BARYCENTER'
         6           'SATURN BARYCENTER'
         7           'URANUS_BARYCENTER'
         7           'URANUS BARYCENTER'
         8           'NEPTUNE_BARYCENTER'
         8           'NEPTUNE BARYCENTER'
         9           'PLUTO_BARYCENTER'
         9           'PLUTO BARYCENTER'
         10          'SUN'

For those planets without moons, Mercury and Venus, the barycenter
location coincides with the body center of mass. However do not infer
you may interchange use of the planet barycenter ID and the planet
ID. A barycenter has no radii, right ascension/declination of the
pole axis, etc. Use the planet ID when referring to a planet or any
property of that planet.

Planets and Satellites
----------------------

| Planets have ID codes of the form P99, where P is 1, ..., 9 (the
  planetary ID) a planet is always considered to be the 99th
  satellite of its own barycenter, e.g. Jupiter is body number 599.
  Natural satellites have ID codes of the form

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

e.g. Ananke, the 12th satellite of Jupiter (JXII), is body number

.. note:: Note the fragments of comet Shoemaker Levy 9 are exceptions to this rule.

.. code-block:: text

         NAIF ID     NAME                    IAU NUMBER
         ________    ____________________    __________
         199         'MERCURY'
         299         'VENUS'
         399         'EARTH'
         301         'MOON'
         499         'MARS'
         401         'PHOBOS'                MI
         402         'DEIMOS'                MII
         599         'JUPITER'
         501         'IO'                    JI
         502         'EUROPA'                JII
         503         'GANYMEDE'              JIII
         504         'CALLISTO'              JIV
         505         'AMALTHEA'              JV
         506         'HIMALIA'               JVI
         507         'ELARA'                 JVII
         508         'PASIPHAE'              JVIII
         509         'SINOPE'                JIX
         510         'LYSITHEA'              JX
         511         'CARME'                 JXI
         512         'ANANKE'                JXII
         513         'LEDA'                  JXIII
         514         'THEBE'                 JXIV
         515         'ADRASTEA'              JXV
         516         'METIS'                 JXVI
         517         'CALLIRRHOE'            JXVII
         518         'THEMISTO'              JXVIII
         519         'MEGACLITE'             JXIX
         520         'TAYGETE'               JXX
         521         'CHALDENE'              JXXI
         522         'HARPALYKE'             JXXII
         523         'KALYKE'                JXXIII
         524         'IOCASTE'               JXXIV
         525         'ERINOME'               JXXV
         526         'ISONOE'                JXXVI
         527         'PRAXIDIKE'             JXXVII
         528         'AUTONOE'               JXXVIII
         529         'THYONE'                JXXIX
         530         'HERMIPPE'              JXXX
         531         'AITNE'                 JXXXI
         532         'EURYDOME'              JXXXII
         533         'EUANTHE'               JXXXIII
         534         'EUPORIE'               JXXXIV
         535         'ORTHOSIE'              JXXXV
         536         'SPONDE'                JXXXVI
         537         'KALE'                  JXXXVII
         538         'PASITHEE'              JXXXVIII
         539         'HEGEMONE'
         540         'MNEME'
         541         'AOEDE'
         542         'THELXINOE'
         543         'ARCHE'
         544         'KALLICHORE'
         545         'HELIKE'
         546         'CARPO'
         547         'EUKELADE'
         548         'CYLLENE'
         549         'KORE'
         550         'HERSE'
         553         'DIA'
         699         'SATURN'
         601         'MIMAS'                 SI
         602         'ENCELADUS'             SII
         603         'TETHYS'                SIII
         604         'DIONE'                 SIV
         605         'RHEA'                  SV
         606         'TITAN'                 SVI
         607         'HYPERION'              SVII
         608         'IAPETUS'               SVIII
         609         'PHOEBE'                SIX
         610         'JANUS'                 SX
         611         'EPIMETHEUS'            SXI
         612         'HELENE'                SXII
         613         'TELESTO'               SXIII
         614         'CALYPSO'               SXIV
         615         'ATLAS'                 SXV
         616         'PROMETHEUS'            SXVI
         617         'PANDORA'               SXVII
         618         'PAN'                   SXVIII
         619         'YMIR'                  SXIX
         620         'PAALIAQ'               SXX
         621         'TARVOS'                SXXI
         622         'IJIRAQ'                SXXII
         623         'SUTTUNGR'              SXXIII
         624         'KIVIUQ'                SXXIV
         625         'MUNDILFARI'            SXXV
         626         'ALBIORIX'              SXXVI
         627         'SKATHI'                SXXVII
         628         'ERRIAPUS'              SXXVIII
         629         'SIARNAQ'               SXXIX
         630         'THRYMR'                SXXX
         631         'NARVI'                 SXXXI
         632         'METHONE'               SXXXII
         633         'PALLENE'               SXXXIII
         634         'POLYDEUCES'            SXXXIV
         635         'DAPHNIS'
         636         'AEGIR'
         637         'BEBHIONN'
         638         'BERGELMIR'
         639         'BESTLA'
         640         'FARBAUTI'
         641         'FENRIR'
         642         'FORNJOT'
         643         'HATI'
         644         'HYRROKKIN'
         645         'KARI'
         646         'LOGE'
         647         'SKOLL'
         648         'SURTUR'
         649         'ANTHE'
         650         'JARNSAXA'
         651         'GREIP'
         652         'TARQEQ'
         653         'AEGAEON'

         799         'URANUS'
         701         'ARIEL'                 UI
         702         'UMBRIEL'               UII
         703         'TITANIA'               UIII
         704         'OBERON'                UIV
         705         'MIRANDA'               UV
         706         'CORDELIA'              UVI
         707         'OPHELIA'               UVII
         708         'BIANCA'                UVIII
         709         'CRESSIDA'              UIX
         710         'DESDEMONA'             UX
         711         'JULIET'                UXI
         712         'PORTIA'                UXII
         713         'ROSALIND'              UXIII
         714         'BELINDA'               UXIV
         715         'PUCK'                  UXV
         716         'CALIBAN'               UXVI
         717         'SYCORAX'               UXVII
         718         'PROSPERO'              UXVIII
         719         'SETEBOS'               UXIX
         720         'STEPHANO'              UXX
         721         'TRINCULO'              UXXI
         722         'FRANCISCO'
         723         'MARGARET'
         724         'FERDINAND'
         725         'PERDITA'
         726         'MAB'
         727         'CUPID'
         899         'NEPTUNE'
         801         'TRITON'                NI
         802         'NEREID'                NII
         803         'NAIAD'                 NIII
         804         'THALASSA'              NIV
         805         'DESPINA'               NV
         806         'GALATEA'               NVI
         807         'LARISSA'               NVII
         808         'PROTEUS'               NVIII
         809         'HALIMEDE'
         810         'PSAMATHE'
         811         'SAO'
         812         'LAOMEDEIA'
         813         'NESO'
         999         'PLUTO'
         901         'CHARON'
         902         'NIX'
         903         'HYDRA'
         904         'KERBEROS'
         905         'STYX'




Spacecraft
----------

| THE SPICE convention uses negative integers as spacecraft ID codes.
  The code assigned to interplanetary spacecraft is normally the
  negative of the code assigned to the same spacecraft by JPL's Deep
  Space Network (DSN) as determined the NASA control authority at
  Goddard Space Flight Center.

The current SPICE vehicle code assignments:

.. code-block:: text

         NAIF ID     NAME
         ________    ____________________
         -1          'GEOTAIL'
         -3          'MOM'
         -3          'MARS ORBITER MISSION'
         -5          'AKATSUKI'
         -5          'VCO'
         -5          'PLC'
         -5          'PLANET-C'
         -6          'P6'
         -6          'PIONEER-6'
         -7          'P7'
         -7          'PIONEER-7'
         -8          'WIND'
         -12         'VENUS ORBITER'
         -12         'P12'
         -12         'PIONEER 12'
         -12         'LADEE'
         -13         'POLAR'
         -18         'MGN'
         -18         'MAGELLAN'
         -18         'LCROSS'
         -20         'P8'
         -20         'PIONEER-8'
         -21         'SOHO'
         -23         'P10'
         -23         'PIONEER-10'
         -24         'P11'
         -24         'PIONEER-11'
         -25         'LP'
         -25         'LUNAR PROSPECTOR'
         -27         'VK1'
         -27         'VIKING 1 ORBITER'
         -28         'JUPITER ICY MOONS EXPLORER'
         -28         'JUICE'
         -29         'STARDUST'
         -29         'SDU'
         -29         'NEXT'
         -30         'VK2'
         -30         'VIKING 2 ORBITER'
         -30         'DS-1'
         -31         'VG1'
         -31         'VOYAGER 1'
         -32         'VG2'
         -32         'VOYAGER 2'
         -33         'NEOS'
         -33         'NEO SURVEYOR'
         -37         'HYB2'
         -37         'HAYABUSA 2'
         -37         'HAYABUSA2'
         -39         'LUNAR POLAR HYDROGEN MAPPER'
         -39         'LUNAH-MAP'
         -40         'CLEMENTINE'
         -41         'MEX'
         -41         'MARS EXPRESS'
         -43         'IMAP'
         -44         'BEAGLE2'
         -44         'BEAGLE 2'
         -45         'JNSA'
         -45         'JANUS_A'
         -46         'MS-T5'
         -46         'SAKIGAKE'
         -47         'PLANET-A'
         -47         'SUISEI'
         -47         'GNS'
         -47         'GENESIS'
         -48         'HUBBLE SPACE TELESCOPE'
         -48         'HST'
         -49         'LUCY'
         -53         'MARS PATHFINDER'
         -53         'MPF'
         -53         'MARS ODYSSEY'
         -53         'MARS SURVEYOR 01 ORBITER'
         -55         'ULYSSES'
         -57         'LUNAR ICECUBE'
         -58         'VSOP'
         -58         'HALCA'
         -59         'RADIOASTRON'
         -61         'JUNO'
         -62         'EMM'
         -62         'EMIRATES MARS MISSION'
         -64         'ORX'
         -64         'OSIRIS-REX'
         -65         'MCOA'
         -65         'MARCO-A'
         -66         'VEGA 1'
         -66         'MCOB'
         -66         'MARCO-B'
         -67         'VEGA 2'
         -68         'MERCURY MAGNETOSPHERIC ORBITER'
         -68         'MMO'
         -68         'BEPICOLOMBO MMO'
         -70         'DEEP IMPACT IMPACTOR SPACECRAFT'
         -72         'JNSB'
         -72         'JANUS_B'
         -74         'MRO'
         -74         'MARS RECON ORBITER'
         -76         'CURIOSITY'
         -76         'MSL'
         -76         'MARS SCIENCE LABORATORY'
         -77         'GLL'
         -77         'GALILEO ORBITER'
         -78         'GIOTTO'
         -79         'SPITZER'
         -79         'SPACE INFRARED TELESCOPE FACILITY'
         -79         'SIRTF'
         -81         'CASSINI ITL'
         -82         'CAS'
         -82         'CASSINI'
         -84         'PHOENIX'
         -85         'LRO'
         -85         'LUNAR RECON ORBITER'
         -85         'LUNAR RECONNAISSANCE ORBITER'
         -86         'CH1'
         -86         'CHANDRAYAAN-1'
         -90         'CASSINI SIMULATION'
         -93         'NEAR EARTH ASTEROID RENDEZVOUS'
         -93         'NEAR'
         -94         'MO'
         -94         'MARS OBSERVER'
         -94         'MGS'
         -94         'MARS GLOBAL SURVEYOR'
         -95         'MGS SIMULATION'
         -96         'PARKER SOLAR PROBE'
         -96         'SPP'
         -96         'SOLAR PROBE PLUS'
         -97         'TOPEX/POSEIDON'
         -98         'NEW HORIZONS'
         -107        'TROPICAL RAINFALL MEASURING MISSION'
         -107        'TRMM'
         -112        'ICE'
         -116        'MARS POLAR LANDER'
         -116        'MPL'
         -117        'EDL DEMONSTRATOR MODULE'
         -117        'EDM'
         -117        'EXOMARS 2016 EDM'
         -119        'MARS_ORBITER_MISSION_2'
         -119        'MOM2'
         -121        'MERCURY PLANETARY ORBITER'
         -121        'MPO'
         -121        'BEPICOLOMBO MPO'
         -127        'MARS CLIMATE ORBITER'
         -127        'MCO'
         -130        'MUSES-C'
         -130        'HAYABUSA'
         -131        'SELENE'
         -131        'KAGUYA'
         -135        'DART'
         -135        'DOUBLE ASTEROID REDIRECTION TEST'
         -140        'EPOCH'
         -140        'DIXI'
         -140        'EPOXI'
         -140        'DEEP IMPACT FLYBY SPACECRAFT'
         -142        'TERRA'
         -142        'EOS-AM1'
         -143        'TRACE GAS ORBITER'
         -143        'TGO'
         -143        'EXOMARS 2016 TGO'
         -144        'SOLO'
         -144        'SOLAR ORBITER'
         -146        'LUNAR-A'
         -148        'DFLY'
         -148        'DRAGONFLY'
         -150        'CASSINI PROBE'
         -150        'HUYGENS PROBE'
         -150        'CASP'
         -151        'AXAF'
         -151        'CHANDRA'
         -152        'CH2O'
         -152        'CHANDRAYAAN-2 ORBITER'
         -153        'CH2L'
         -153        'CHANDRAYAAN-2 LANDER'
         -154        'AQUA'
         -155        'KPLO'
         -155        'KOREAN PATHFINDER LUNAR ORBITER'
         -156        'ADITYA'
         -156        'ADIT'
         -159        'EURC'
         -159        'EUROPA CLIPPER'
         -164        'LUNAR FLASHLIGHT'
         -165        'MAP'
         -166        'IMAGE'
         -168        'PERSEVERANCE'
         -168        'MARS 2020'
         -168        'MARS2020'
         -168        'M2020'
         -170        'JWST'
         -170        'JAMES WEBB SPACE TELESCOPE'
         -172        'EXM RSP SCC'
         -172        'EXM SPACECRAFT COMPOSITE'
         -172        'EXOMARS SCC'
         -173        'EXM RSP SP'
         -173        'EXM SURFACE PLATFORM'
         -173        'EXOMARS SP'
         -174        'EXM RSP RM'
         -174        'EXM ROVER'
         -174        'EXOMARS ROVER'
         -177        'GRAIL-A'
         -178        'PLANET-B'
         -178        'NOZOMI'
         -181        'GRAIL-B'
         -183        'CLUSTER 1'
         -185        'CLUSTER 2'
         -188        'MUSES-B'
         -189        'NSYT'
         -189        'INSIGHT'
         -190        'SIM'
         -194        'CLUSTER 3'
         -196        'CLUSTER 4'
         -197        'EXOMARS_LARA'
         -197        'LARA'
         -198        'INTEGRAL'
         -198        'NASA-ISRO SAR MISSION'
         -198        'NISAR'
         -200        'CONTOUR'
         -202        'MAVEN'
         -203        'DAWN'
         -205        'SOIL MOISTURE ACTIVE AND PASSIVE'
         -205        'SMAP'
         -210        'LICIA'
         -210        'LICIACUBE'
         -212        'STV51'
         -213        'STV52'
         -214        'STV53'
         -226        'ROSETTA'
         -227        'KEPLER'
         -228        'GLL PROBE'
         -228        'GALILEO PROBE'
         -234        'STEREO AHEAD'
         -235        'STEREO BEHIND'
         -236        'MESSENGER'
         -238        'SMART1'
         -238        'SM1'
         -238        'S1'
         -238        'SMART-1'
         -239        'MARTIAN MOONS EXPLORATION'
         -239        'MMX'
         -240        'SMART LANDER FOR INVESTIGATING MOON'
         -240        'SLIM'
         -242        'LUNAR TRAILBLAZER'
         -243        'VIPER'
         -248        'VEX'
         -248        'VENUS EXPRESS'
         -253        'OPPORTUNITY'
         -253        'MER-1'
         -254        'SPIRIT'
         -254        'MER-2'
         -255        'PSYC'
         -301        'HELIOS 1'
         -302        'HELIOS 2'
         -362        'RADIATION BELT STORM PROBE A'
         -362        'RBSP_A'
         -363        'RADIATION BELT STORM PROBE B'
         -363        'RBSP_B'
         -500        'RSAT'
         -500        'SELENE Relay Satellite'
         -500        'SELENE Rstar'
         -500        'Rstar'
         -502        'VSAT'
         -502        'SELENE VLBI Radio Satellite'
         -502        'SELENE VRAD Satellite'
         -502        'SELENE Vstar'
         -502        'Vstar'
         -550        'MARS-96'
         -550        'M96'
         -550        'MARS 96'
         -550        'MARS96'
         -652        'MERCURY TRANSFER MODULE'
         -652        'MTM'
         -652        'BEPICOLOMBO MTM'
         -750        'SPRINT-A'



Earth Orbiting Spacecraft.
--------------------------

| If an Earth orbiting spacecraft lacks a DSN identification code,
  the NAIF ID is derived from the tracking ID assigned to it by NORAD
  via:

.. code-block:: text

         NAIF ID = -100000 - NORAD ID code

For example, NORAD assigned the code 15427 to the NOAA 9 spacecraft.
This code corresponds to the NAIF ID -115427.

Comet Shoemaker Levy 9
-----------------------

| In July, 1992 Comet Shoemaker Levy 9 passed close enough to the
  planet Jupiter that it was torn apart by gravitational tidal
  forces. As a result it became a satellite of Jupiter. However, in
  July 1994 the remnants of Shoemaker Levy 9 collided with Jupiter.
  Consequently, the fragments existed as satellites of Jupiter for
  only two years. These fragments were given the NAIF ID's listed
  below. Unfortunately, there have been two competing conventions
  selected for identifying the fragments of the comet. In one
  convention the fragments have been assigned numbers 1 through 21.
  In the second convention the fragments have been assigned letters A
  through W (with I and O unused). To add to the confusion, the
  ordering for the numbers is reversed from the letter ordering.
  Fragment 21 corresponds to letter A; fragment 20 to letter B and so
  on. Fragment A was the first of the fragments to collide with
  Jupiter; fragment W was the last to collide with Jupiter.

.. note::
   The original fragments P and Q subdivided further creating the
   fragments P2 and Q1.

.. code-block:: text


        NAIF ID     NAME                    SHOEMAKER-LEVY 9 FRAGMENT

        ________    ____________________    _________________________
         50000001    'SHOEMAKER-LEVY 9-W'    FRAGMENT 1
         50000002    'SHOEMAKER-LEVY 9-V'    FRAGMENT 2
         50000003    'SHOEMAKER-LEVY 9-U'    FRAGMENT 3
         50000004    'SHOEMAKER-LEVY 9-T'    FRAGMENT 4
         50000005    'SHOEMAKER-LEVY 9-S'    FRAGMENT 5
         50000006    'SHOEMAKER-LEVY 9-R'    FRAGMENT 6
         50000007    'SHOEMAKER-LEVY 9-Q'    FRAGMENT 7
         50000008    'SHOEMAKER-LEVY 9-P'    FRAGMENT 8
         50000009    'SHOEMAKER-LEVY 9-N'    FRAGMENT 9
         50000010    'SHOEMAKER-LEVY 9-M'    FRAGMENT 10
         50000011    'SHOEMAKER-LEVY 9-L'    FRAGMENT 11
         50000012    'SHOEMAKER-LEVY 9-K'    FRAGMENT 12
         50000013    'SHOEMAKER-LEVY 9-J'    FRAGMENT 13
         50000014    'SHOEMAKER-LEVY 9-H'    FRAGMENT 14
         50000015    'SHOEMAKER-LEVY 9-G'    FRAGMENT 15
         50000016    'SHOEMAKER-LEVY 9-F'    FRAGMENT 16
         50000017    'SHOEMAKER-LEVY 9-E'    FRAGMENT 17
         50000018    'SHOEMAKER-LEVY 9-D'    FRAGMENT 18
         50000019    'SHOEMAKER-LEVY 9-C'    FRAGMENT 19
         50000020    'SHOEMAKER-LEVY 9-B'    FRAGMENT 20
         50000021    'SHOEMAKER-LEVY 9-A'    FRAGMENT 21
         50000022    'SHOEMAKER-LEVY 9-Q1'   FRAGMENT 7A
         50000023    'SHOEMAKER-LEVY 9-P2'   FRAGMENT 8B



Comets
--------

| ID codes for periodic comets begin at 1000001 and indefinitely
  continue in sequence. (The current numbering scheme assumes no need
  for more than one million comet ID codes.) For several years NAIF
  maintained a list of comets and NAIF ID codes in this document, and
  also coded in Toolkit software. But as the rate of discovery picked
  up pace at the same time that new Toolkit releases slowed down,
  this list has grown out of date. We decided to leave the last
  version of the list in this document, and note that one can find
  the NAIF ID code for any named periodic comet, and vice-versa, by
  using a webpage managed by JPL's Solar System Dynamics Group:

      https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html

.. note::
   Note that the partial listing shown below has an alphabetic ordering
   through ID 1000111, after which new ID codes were assigned in the
   order of discovery.
   Finally, note that Comet Shoemaker Levy 9 is included in this list
   (ID code 1000130) though it is no longer a comet, periodic or
   otherwise. It was an identified periodic comet prior to its breakup,
   which accounts for its inclusion in this list.

.. code-block:: text

         NAIF ID     NAME
         ________    ____________________
         1000001     'AREND'
         1000002     'AREND-RIGAUX'
         1000003     'ASHBROOK-JACKSON'
         1000004     'BOETHIN'
         1000005     'BORRELLY'
         1000006     'BOWELL-SKIFF'
         1000007     'BRADFIELD'
         1000008     'BROOKS 2'
         1000009     'BRORSEN-METCALF'
         1000010     'BUS'
         1000011     'CHERNYKH'
         1000012     '67P/CHURYUMOV-GERASIMENKO (1969 R1)'
         1000012     'CHURYUMOV-GERASIMENKO'
         1000013     'CIFFREO'
         1000014     'CLARK'
         1000015     'COMAS SOLA'
         1000016     'CROMMELIN'
         1000017     'D''ARREST'
         1000018     'DANIEL'
         1000019     'DE VICO-SWIFT'
         1000020     'DENNING-FUJIKAWA'
         1000021     'DU TOIT 1'
         1000022     'DU TOIT-HARTLEY'
         1000023     'DUTOIT-NEUJMIN-DELPORTE'
         1000024     'DUBIAGO'
         1000025     'ENCKE'
         1000026     'FAYE'
         1000027     'FINLAY'
         1000028     'FORBES'
         1000029     'GEHRELS 1'
         1000030     'GEHRELS 2'
         1000031     'GEHRELS 3'
         1000032     'GIACOBINI-ZINNER'
         1000033     'GICLAS'
         1000034     'GRIGG-SKJELLERUP'
         1000035     'GUNN'
         1000036     'HALLEY'
         1000037     'HANEDA-CAMPOS'
         1000038     'HARRINGTON'
         1000039     'HARRINGTON-ABELL'
         1000040     'HARTLEY 1'
         1000041     'HARTLEY 2'
         1000042     'HARTLEY-IRAS'
         1000043     'HERSCHEL-RIGOLLET'
         1000044     'HOLMES'
         1000045     'HONDA-MRKOS-PAJDUSAKOVA'
         1000046     'HOWELL'
         1000047     'IRAS'
         1000048     'JACKSON-NEUJMIN'
         1000049     'JOHNSON'
         1000050     'KEARNS-KWEE'
         1000051     'KLEMOLA'
         1000052     'KOHOUTEK'
         1000053     'KOJIMA'
         1000054     'KOPFF'
         1000055     'KOWAL 1'
         1000056     'KOWAL 2'
         1000057     'KOWAL-MRKOS'
         1000058     'KOWAL-VAVROVA'
         1000059     'LONGMORE'
         1000060     'LOVAS 1'
         1000061     'MACHHOLZ'
         1000062     'MAURY'
         1000063     'NEUJMIN 1'
         1000064     'NEUJMIN 2'
         1000065     'NEUJMIN 3'
         1000066     'OLBERS'
         1000067     'PETERS-HARTLEY'
         1000068     'PONS-BROOKS'
         1000069     'PONS-WINNECKE'
         1000070     'REINMUTH 1'
         1000071     'REINMUTH 2'
         1000072     'RUSSELL 1'
         1000073     'RUSSELL 2'
         1000074     'RUSSELL 3'
         1000075     'RUSSELL 4'
         1000076     'SANGUIN'
         1000077     'SCHAUMASSE'
         1000078     'SCHUSTER'
         1000079     'SCHWASSMANN-WACHMANN 1'
         1000080     'SCHWASSMANN-WACHMANN 2'
         1000081     'SCHWASSMANN-WACHMANN 3'
         1000082     'SHAJN-SCHALDACH'
         1000083     'SHOEMAKER 1'
         1000084     'SHOEMAKER 2'
         1000085     'SHOEMAKER 3'
         1000086     'SINGER-BREWSTER'
         1000087     'SLAUGHTER-BURNHAM'
         1000088     'SMIRNOVA-CHERNYKH'
         1000089     'STEPHAN-OTERMA'
         1000090     'SWIFT-GEHRELS'
         1000091     'TAKAMIZAWA'
         1000092     'TAYLOR'
         1000093     'TEMPEL_1'
         1000093     'TEMPEL 1'
         1000094     'TEMPEL 2'
         1000095     'TEMPEL-TUTTLE'
         1000096     'TRITTON'
         1000097     'TSUCHINSHAN 1'
         1000098     'TSUCHINSHAN 2'
         1000099     'TUTTLE'
         1000100     'TUTTLE-GIACOBINI-KRESAK'
         1000101     'VAISALA 1'
         1000102     'VAN BIESBROECK'
         1000103     'VAN HOUTEN'
         1000104     'WEST-KOHOUTEK-IKEMURA'
         1000105     'WHIPPLE'
         1000106     'WILD 1'
         1000107     'WILD 2'
         1000108     'WILD 3'
         1000109     'WIRTANEN'
         1000110     'WOLF'
         1000111     'WOLF-HARRINGTON'
         1000112     'LOVAS 2'
         1000113     'URATA-NIIJIMA'
         1000114     'WISEMAN-SKIFF'
         1000115     'HELIN'
         1000116     'MUELLER'
         1000117     'SHOEMAKER-HOLT 1'
         1000118     'HELIN-ROMAN-CROCKETT'
         1000119     'HARTLEY 3'
         1000120     'PARKER-HARTLEY'
         1000121     'HELIN-ROMAN-ALU 1'
         1000122     'WILD 4'
         1000123     'MUELLER 2'
         1000124     'MUELLER 3'
         1000125     'SHOEMAKER-LEVY 1'
         1000126     'SHOEMAKER-LEVY 2'
         1000127     'HOLT-OLMSTEAD'
         1000128     'METCALF-BREWINGTON'
         1000129     'LEVY'
         1000130     'SHOEMAKER-LEVY 9'
         1000131     'HYAKUTAKE'
         1000132     'HALE-BOPP'
         1003228     'C/2013 A1'
         1003228     'SIDING SPRING'



Asteroids
-------------

| According to the original schema, NAIF ID codes for permanently
  numbered asteroids registered in the JPL Solar System Dynamics
  (SSD) Group database are 7-digit numbers determined using the
  algorithm

.. code-block:: text

         NAIF ID code = 2000000 + Permanent Asteroid Number

limited to the 2000001 to 2999999 range and allowing up to 1 million
asteroids.
For newly discovered asteroids with provisional numbers SSD
internally uses 7-digit numbers determined via the algorithm

.. code-block:: text

         NAIF ID code = 3000000 + Provisional Asteroid Number

limited to the 3000001 to 3999999 range and also allowing up to 1
million asteroids.
Given the need to accommodate many more asteroids expected to be
discovered by surveys coming on-line in the near future and the
desire to encode in the NAIF ID codes the roles of individual
asteroids and barycenters in binary and multi-body asteroid systems
in a way similar to planetary systems, in 2019 SSD and NAIF agreed to
extend the original schema.

Under the extended schema all permanently numbered singular asteroids
have 8-digit NAIF ID codes with the original 7-digit IDs still
allowed to be used. Such asteroids are assigned NAIF ID codes using
the algorithm

.. code-block:: text

         NAIF ID code = 20000000 + Permanent Asteroid Number

limited to the 20000001 to 49999999 range and allowing up to 30
million asteroids.

For asteroid systems with two or more bodies the 8-digit NAIF ID code
represents the barycenter. Individual satellites have a prepended
number 1 through 8, while the primary body uses the \``last
available'' prefix 9, resulting in 9-digit NAIF ID codes. This is
analogous to the planetary system approach except a single extra
number is added as a prefix rather than two numbers added as a
suffix. In the case of ID codes presented by strings, a 0 prefix
could be added to the ID of the barycenter, if printing out uniform 9
digits is desired.

For newly discovered singular asteroids and asteroid system
barycenters with provisional numbers NAIF ID codes are also 8-digit
numbers determined via the algorithm:

.. code-block:: text

         NAIF ID code = 50000000 + Provisional Asteroid Number

limited to the 50000001 to 99999999 range and allowing up to 50
million asteroids, with the same prefix rule used to derive the
9-digit IDs for the primary and satellite bodies in multi-body
systems.

For example, asteroid Yeomans (2956) has NAIF ID number 2002956
according to the original schema and NAIF ID number 20002956
according to the extended schema, while asteroids Didymos (65803) and
its satellite Dimorphos can be accommodated only using the extended
schema with IDs 920065803 and 120065803, and Didymos system
barycenter with ID 20065803.

The complete list of asteroids is far too numerous to include in this
document. However, below we include the NAIF ID codes for a few of
the most commonly requested asteroids. One may look up the NAIF ID
code for any named asteroid, or vice-versa, by using a webpage
managed by JPL's Solar System Dynamics Group:

      https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html

.. code-block:: text

         NAIF ID     NAME
         ________    ____________________
         2000001     'CERES'
         2000002     'PALLAS'
         2000004     'VESTA'
         2000016     'PSYCHE'
         2000021     'LUTETIA'
         2000052     '52_EUROPA'
         2000052     '52 EUROPA'
         2000216     'KLEOPATRA'
         2000253     'MATHILDE'
         2000433     'EROS'
         2000511     'DAVIDA'
         2002867     'STEINS'
         2004015     'WILSON-HARRINGTON'
         2004179     'TOUTATIS'
         2009969     '1992KD'
         2009969     'BRAILLE'
         2025143     'ITOKAWA'
         2101955     'BENNU'
         2162173     'RYUGU'
         2431010     'IDA'
         2431011     'DACTYL'
         2486958     'ARROKOTH'
         9511010     'GASPRA'
        20000617     'PATROCLUS_BARYCENTER'
        20000617     'PATROCLUS BARYCENTER'
        20003548     'EURYBATES_BARYCENTER'
        20003548     'EURYBATES BARYCENTER'
        20011351     'LEUCUS'
        20015094     'POLYMELE'
        20021900     'ORUS'
        20052246     'DONALDJOHANSON'
        20065803     'DIDYMOS_BARYCENTER'
        20065803     'DIDYMOS BARYCENTER'
       120000617     'MENOETIUS'
       120003548     'QUETA'
       120065803     'DIMORPHOS'
       920000617     'PATROCLUS'
       920003548     'EURYBATES'
       920065803     'DIDYMOS'

.. attention::
   There are three exceptions to the rule---asteroids Gaspra, Ida and
   Ida's satellite Dactyl, visited by the Galileo spacecraft. The ID
   codes for these asteroids were determined using an older numbering
   convention now abandoned by the SPICE system.

Ground Stations.
-----------------

| The SPICE system accommodates ephemerides for tracking stations and
  landed spacecraft. Currently five earth tracking station sites are
  supported: Goldstone, Canberra, Madrid, Usuda, and Parkes. Note
  that these refer only to the general geographic location of the
  various tracking sites. IDs for the individual antennas at a given
  site are assigned when more than one antenna is present.

The following NAIF ID codes are assigned.

.. code-block:: text

         NAIF ID     NAME
         ________    ____________________
         398989      'NOTO'
         398990      'NEW NORCIA'
         399001      'GOLDSTONE'
         399002      'CANBERRA'
         399003      'MADRID'
         399004      'USUDA'
         399005      'DSS-05'
         399005      'PARKES'
         399012      'DSS-12'
         399013      'DSS-13'
         399014      'DSS-14'
         399015      'DSS-15'
         399016      'DSS-16'
         399017      'DSS-17'
         399023      'DSS-23'
         399024      'DSS-24'
         399025      'DSS-25'
         399026      'DSS-26'
         399027      'DSS-27'
         399028      'DSS-28'
         399033      'DSS-33'
         399034      'DSS-34'
         399035      'DSS-35'
         399036      'DSS-36'
         399042      'DSS-42'
         399043      'DSS-43'
         399045      'DSS-45'
         399046      'DSS-46'
         399049      'DSS-49'
         399053      'DSS-53'
         399054      'DSS-54'
         399055      'DSS-55'
         399056      'DSS-56'
         399061      'DSS-61'
         399063      'DSS-63'
         399064      'DSS-64'
         399065      'DSS-65'
         399066      'DSS-66'
         399069      'DSS-69'



Inertial and Non-inertial Reference Frames
-------------------------------------------

| Please refer to the Frames Required Reading document,
  `frames <./frames.html>`__, for detailed information on
  the implementation of reference frames in the SPICE system.


Spacecraft Clocks.
====================

| The ID code used to identify the on-board clock of a spacecraft
  (spacecraft clock or SCLK) in SPICE software is the same as the ID
  code of the spacecraft. This convention assumes that only one clock
  is used on-board a spacecraft to control all observations and
  spacecraft functions. However, missions are envisioned in which
  instruments may have clocks not tightly coupled to the primary
  spacecraft control clock. When this situation occurs, the
  correspondence between clocks and spacecraft will be broken and
  more than one clock ID code will be associated with a mission. It
  is anticipated that the I-kernel will contain the information
  needed to associate the appropriate clock with a particular
  instrument.


Instruments
============

| With regards to a spacecraft, the term `instrument` means a
  science instrument or vehicle structure to which the concept of
  orientation is applicable.

NAIF, in cooperation with the science teams from each flight project,
assigns ID codes to a vehicle instrument. The instruments are simply
enumerated via some project convention to arrive at an 'instrument
number.' The NAIF ID code for an instrument derives from the
instrument number via the function:

.. code-block:: text

         NAIF instrument code = (s/c code)*(1000) - instrument number

This allows for 1000 instrument assignments on board a spacecraft. An
application of the instrument ID concept applied to the Voyager 2
vehicle (ID -32):

.. code-block:: text

    -32000 -> Instrument Scan Platform

    -32001 -> ISSNA (Imaging science narrow angle camera)

    -32002 -> ISSWA (Imaging science wide angle camera)

    -32003 -> PPS (Photopolarimeter)

    -32004 -> UVSAG (Ultraviolet Spectrometer, Airglow port)

    -32005 -> UVSOCC (Ultraviolet Spectrometer, Occultation port)

    -32006 -> IRIS (Infrared Interferometer Spectrometer and Radiometer)

Use SPICE text kernels (usually Instrument or Frames kernels) to
define the instrument name/ID mappings.

