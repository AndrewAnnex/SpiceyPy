****************************************
Ellipses and Ellipsoids Required Reading
****************************************

This required reading document is reproduced from the original NAIF
document available at `https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/ellipses.html <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/ellipses.html>`_

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

| SPICE contains a substantial set of subroutines that solve common
  mathematical problems involving ellipses and triaxial ellipsoids.
  This required reading file documents those routines, gives examples
  of their use, and presents some of the mathematical background
  required to understand the routines.

Introduction
------------

| The 'ellipse' is a structured data type used in SPICE to
  represent ellipses in three-dimensional space. SPICE ellipses exist
  to simplify calling sequences of routines that output or accept as
  input data that defines ellipses.

Ellipses turn up frequently in the sort of science analysis problems
SPICE is designed to help solve. The shapes of extended
bodies--planets, satellites, and the Sun--are frequently modeled by
triaxial ellipsoids. The IAU has defined such models for the Sun, all
of the planets, and most of their satellites, in the IAU/IAG/COSPAR
working group report IAU_IAG_COSPAR_. Many geometry problems involving triaxial
ellipsoids give rise to ellipses as 'mathematical byproducts'.
Ellipses are also used in modeling orbits and planetary rings.


References
^^^^^^^^^^

.. _IAU_IAG_COSPAR:

#. 'Report of the IAU/IAG/COSPAR Working Group on Cartographic Coordinates and Rotational Elements of the Planets and Satellites: 2009', December 4, 2010.

#. 'Calculus, Vol. II'. Tom Apostol. John Wiley and Sons,

   * See Chapter 5, 'Eigenvalues of Operators Acting on Euclidean Spaces'.

#. Planes required reading  (`planes <./planes.html>`__).



Ellipse Data Type Description
=============================


| The following representation of an ellipse is used throughout
  SPICE, and in particular by the ellipse access routines: An ellipse
  is the set of points

::

     ellipse = CENTER    +    cos(theta) * V1    +    sin(theta) * V2

where CENTER, V1, and V2 are 3-vectors, and theta is in the range
::

      (-pi, pi].

The set of points "ellipse" is an ellipse (see Appendix A:
Mathematical notes). The ellipse defined by this parametric
representation is non-degenerate if and only if V1 and V2 are
linearly independent.
We call CENTER the 'center' of the ellipse, and we refer to V1 and
V2 as 'generating vectors'. Note that an ellipse centered at the
coordinate origin (0, 0, 0,) is completely specified by its
generating vectors. Further mention of the center or generating
vectors for a particular ellipse, means vectors that play the role of
CENTER or V1 and V2 in defining that ellipse.

This representation of ellipses has the particularly convenient
property that it allows easy computation of the image of an ellipse
under a linear transformation. If M is a matrix representing a linear
transformation, and E is the ellipse

::

      CENTER    +    cos(theta) * V1    +    sin(theta) * V2,

then the image of E under the transformation represented by M is
::

      M*CENTER    +    cos(theta) * M*V1    +    sin(theta) * M*V2.

If we accept that the first set of points is an ellipse, then we can
see that the image of an ellipse under a linear transformation is
always another (possibly degenerate) ellipse.
Since many geometric computations involving ellipses and ellipsoids
may be greatly simplified by judicious application of linear
transformations to ellipses, it is useful to have a representation
for ellipses that allows ready computation of their images under such
mappings.

The internal design of the ellipse data type is not part of its
specification. The design is an implementation choice based on the
programming language and so the design may change. Users should not
write code based on the current implementation; such code might fail
when used with a future version of CSPICE.

NAIF implemented the SPICE ellipse data type in C as a structure with
the fields

::

         SpiceDouble      center    [3];
         SpiceDouble      semiMajor [3];
         SpiceDouble      semiMinor [3];

In SpiceyPy, this structure is defined by :py:class:`spiceypy.utils.support_types.Ellipse`,
although users are encouraged not to directly interact with this object and to instead use the spice routines described below for creating and using them.

The fields are set and accessed by a small set of access routines
provided for that purpose. Do not access the fields in any other way.
The elements of SPICE ellipses are set using
:py:meth:`~spiceypy.spiceypy.cgv2el` (center and generating vectors
to ellipse) and accessed using :py:meth:`~spiceypy.spiceypy.el2cgv`
(ellipse to center and generating vectors).



Ellipse and ellipsoid routines
==============================



Constructing ellipses
---------------------

| Let 'center', 'v1', and 'v2' be a center vector and two
  generating vectors for an ellipse.

Let 'center', 'v1', and 'v2' be declared with assigned values:

.. code-block:: python

      import numpy as np

      center = np.array([ -1.0, 1.0, -1.0 ])
      v1     = np.array([  1.0, 1.0, 1.0  ])
      v2     = np.array([  1.0, -1.0, 1.0 ])

After 'center', 'v1', and 'v2' have been assigned values, you can
construct a SPICE ellipse using :py:meth:`~spiceypy.spiceypy.cgv2el`:

.. code-block:: python

      import spiceypy

      ellipse = spiceypy.cgv2el( center, v1, v2 )

This call produces the SPICE ellipse 'ellips', which represents the
same mathematical ellipse as do 'center', 'v1', and 'v2'.
The generating vectors need not be linearly independent. If they are
not, the resulting ellipse will be degenerate. Specifically, if the
generating vectors are both zero, the ellipse will be the single
point represented by 'center', and if just one of the semi-axis
vectors (call it V) is non-zero, the ellipse will be the line segment
extending from

 ::

      CENTER - V

 to

 ::

      CENTER + V



Access to ellipse data elements
-------------------------------

| Let 'ellips' be a SPICE ellipse. To produce the center and two
  generating vectors for 'ellips', we can make the call

.. code-block:: python

      center,  v1,  v2  = spiceypy.el2cgv( ellips )

On output, 'v1' will be a semi-major axis vector for the ellipse
represented by 'ellips', and 'v2' will be a semi-minor axis vector.
Semi-axis vectors are never unique; if X is a semi-axis vector; then
so is -X.
'v1' is a vector of maximum norm extending from the ellipse's center
to the ellipse itself; 'v2' is an analogous vector of minimum norm.
'v1' and V2 are orthogonal vectors.


:py:meth:`~spiceypy.spiceypy.cgv2el` and :py:meth:`~spiceypy.spiceypy.el2cgv` are not inverses
----------------------------------------------------------------------------------------------

| Because the routine :py:meth:`~spiceypy.spiceypy.el2cgv` always
  returns semi-axes as generating vectors, if 'v1' and 'v2' are not
  semi-axes on input to :py:meth:`~spiceypy.spiceypy.cgv2el`, the
  sequence of calls

::

      ellips = spiceypy.cgv2el( center, v1, v2 )
      center,  v1,  v2  = spiceypy.el2cgv( ellips )

will certainly modify 'v1' and 'v2'. Even if 'v1' and 'v2' are
semi-axes to start out with, because of the non-uniqueness of
semi-axes, one or both of these vectors could be negated on output
from :py:meth:`~spiceypy.spiceypy.el2cgv`.
There is a sense in which :py:meth:`~spiceypy.spiceypy.cgv2el` and
:py:meth:`~spiceypy.spiceypy.el2cgv` are inverses, though: the
above sequence of calls returns a center and generating vectors that
define the same ellipse as the input center and generating vectors.


Triaxial ellipsoid routines
---------------------------


| The routines used to perform geometric calculations  involving ellipsoids:

:py:meth:`~spiceypy.spiceypy.edlimb`
   Ellipsoid limb

:py:meth:`~spiceypy.spiceypy.inedpl`
   Intersection of ellipsoid and plane

:py:meth:`~spiceypy.spiceypy.nearpt`
   Nearest point on ellipsoid to point

:py:meth:`~spiceypy.spiceypy.npedln`
   Nearest point on ellipsoid to line

:py:meth:`~spiceypy.spiceypy.sincpt`
   Surface intercept

:py:meth:`~spiceypy.spiceypy.surfnm`
   Surface normal on ellipsoid

:py:meth:`~spiceypy.spiceypy.surfpt`
   Surface intercept point on ellipsoid


Ellipse routines
----------------


| The CSPICE routines used to perform geometric calculations
  involving ellipses:

:py:meth:`~spiceypy.spiceypy.inelpl`
   Intersection of ellipse and plane

:py:meth:`~spiceypy.spiceypy.npelpt`
   Nearest point on ellipse to point

:py:meth:`~spiceypy.spiceypy.pjelpl`
   Projection of ellipse onto plane

:py:meth:`~spiceypy.spiceypy.saelgv`
   Semi-axes of ellipse from generating vectors


Examples
=========


Finding the 'limb angle' of an instrument boresight
----------------------------------------------------

| If we want to find the angle of a ray above the limb of an
  ellipsoid, where the angle is measured in a plane containing the
  ray and a 'down' vector, we can follow the procedure given below.
  We assume the ray does not intersect the ellipsoid. Name the result
  'angle'.

We assume that all vectors are given in body-fixed coordinates.

- 'observ' is the body-center to observer vector.

- 'raydir' is the boresight ray's direction vector in
  body-fixed coordinates.

- 'limb' is an ellipse, the result of the limb calculation.

Find the limb of the ellipsoid as seen from the point 'observ'. Here
'a', 'b', and 'c' are the lengths of the semi-axes of the
ellipsoid.

.. code-block:: python

      limb = spiceypy.edlimb( a, b, c, observ )

The ray direction vector is 'raydir', so the ray is the set of
points
::

      OBSERV + t * RAYDIR

where t is any non-negative real number.
The 'down' vector is just - 'observ'. The vectors OBSERV and RAYDIR
are spanning vectors for the plane we're interested in. We can use
:py:meth:`~spiceypy.spiceypy.psv2pl` to represent this plane by a
SPICELIB plane.

.. code-block:: python

      plane = spiceypy.psv2pl( observ, observ, raydir )

Find the intersection of the plane defined by 'observ' and 'raydir'
with the limb.

.. code-block:: python

      nxpts, xpt1, xpt2 = spiceypy.inelpl( limb, plane )

We always expect two intersection points, if 'down' is valid. If
'nxpts' has value less-than two, the user must respond to the error
condition.
Form the vectors from 'observ' to the intersection points. Find the
angular separation between the boresight ray and each vector from
'observ' to the intersection points.

.. code-block:: python

      vec1 = spiceypy.vsub( xpt1, observ )
      vec2 = spiceypy.vsub( xpt2, observ )

      sep1 = spiceypy.vsep( vec1, raydir )
      sep2 = spiceypy.vsep( vec2, raydir )

The angular separation we're after is the minimum of the two
separations we've computed.

.. code-block:: python

      angle = min(sep1, sep2)



Use of ellipses with planes
---------------------------

| The nature of geometry problems involving planes often includes use
  of the SPICE ellipse data type. The example C code listed in the
  headers of the routines `inelpl_c <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/inelpl_c.html>`__ and
  `pjelpl_c <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/pjelpl_c.html>`__ show examples of problems
  solved using both the ellipse and plane data type that can be converted into the equivalent python by readers.



Summary of routines
===================
|
| The following table summarizes the SPICE ellipse and ellipsoid
  routines.

:py:meth:`~spiceypy.spiceypy.cgv2el`
      Center and generating vectors to ellipse
:py:meth:`~spiceypy.spiceypy.edlimb`
      Ellipsoid limb
:py:meth:`~spiceypy.spiceypy.edterm`
      Ellipsoid terminator
:py:meth:`~spiceypy.spiceypy.el2cgv`
      Ellipse to center and generating vectors
:py:meth:`~spiceypy.spiceypy.inedpl`
      Intersection of ellipsoid and plane
:py:meth:`~spiceypy.spiceypy.inelpl`
      Intersection of ellipse and plane
:py:meth:`~spiceypy.spiceypy.nearpt`
      Nearest point on ellipsoid to point
:py:meth:`~spiceypy.spiceypy.npedln`
      Nearest point on ellipsoid to line
:py:meth:`~spiceypy.spiceypy.npelpt`
      Nearest point on ellipse to point
:py:meth:`~spiceypy.spiceypy.pjelpl`
      Projection of ellipse onto plane
:py:meth:`~spiceypy.spiceypy.saelgv`
      Semi-axes of ellipse from generating vectors
:py:meth:`~spiceypy.spiceypy.sincpt`
      Surface intercept
:py:meth:`~spiceypy.spiceypy.surfnm`
      Surface normal on ellipsoid
:py:meth:`~spiceypy.spiceypy.surfpt`
      Surface intercept point on ellipsoid
:py:meth:`~spiceypy.spiceypy.surfpv`
      Surface point and velocity


Appendix A: Mathematical notes
==============================

Defining an ellipse parametrically
-----------------------------------


| Our aim is to show that the set of points

::

      CENTER    +    cos(theta) * V1    +    sin(theta) * V2

where CENTER, V1, and V2 are specified vectors in three-dimensional
space, and where theta is a real number in the interval (-pi, pi], is
in fact an ellipse as we've claimed.
Since the vector CENTER simply translates the set, we may assume
without loss of generality that it is the zero vector. So we'll
re-write our expression for the alleged ellipse as

::

      cos(theta) * V1    +    sin(theta) * V2

where theta is a real number in the interval (-pi, pi]. We'll give
the name S to the above set of vectors. Without loss of generality,
we can assume that V1 and V2 lie in the x-y plane. Therefore, we can
treat V1 and V2 as two-dimensional vectors.
If V1 and V2 are linearly dependent, S is a line segment or a point,
so there is nothing to prove. We'll assume from now on that V1 and V2
are linearly independent.

Every point in S has coordinates ( cos(theta), sin(theta) ) relative
to the basis

::

      {V1, V2}.

Define the change-of-basis matrix C by setting the first and second
columns of C equal to V1 and V2, respectively. If (x,y) are the
coordinates of a point P on S relative to the standard basis
::

      { (1,0), (0,1) },

then the coordinates of P relative to the basis
::

      {V1, V2}

are
::

                 +- -+
            -1   | x |
           C     |   |
                 | y |
                 +- -+

               +-          -+
               | cos(theta) |
      =        |            |
               | sin(theta) |
               +-          -+

Taking inner products, we find
::

           +-    -+      -1 T     -1   +- -+
           | x  y |   ( C  )     C     | x |
           +-    -+                    |   |
                                       | y |
                                       +- -+


           +-                      -+  +-          -+
      =    | cos(theta)  sin(theta) |  | cos(theta) |
           +-                      -+  |            |
                                       | sin(theta) |
                                       +-          -+

      =    1

The matrix
::

         -1  T   -1
      ( C   )   C

is symmetric; let's say that it has entries
::

      +-          -+
      |   a   b/2  |
      |            |.
      |  b/2   c   |
      +-          -+

We know that a and c are positive because they are squares of norms
of the columns of
::

       -1
      C

which is a non-singular matrix. Then the equation above reduces to
::

         2                2
      a x   +  b xy  + c y   =  1,     a, c  >  0.

We can find a new orthogonal basis such that this equation transforms
to
::

          2           2
      d1 u    +   d2 v

with respect to this new basis. Let's give the name SYM to the matrix
::

      +-          -+
      |   a   b/2  |
      |            |;
      |  b/2   c   |
      +-          -+

since SYM is symmetric, there exists an orthogonal matrix M that
diagonalizes SYM. That is, we can find an orthogonal matrix M such
that
::

                       +-      -+
       T               | d1   0 |
      M  SYM  M    =   |        |.
                       | 0   d2 |
                       +-      -+

The existence of such a matrix M will not be proved here; see
reference [2]. The columns of M are the elements of the basis we're
looking for: if we define the variables (u,v) by the transformation
::

      +- -+        +- -+
      | u |      T | x |
      |   |  =  M  |   |,
      | v |        | y |
      +- -+        +- -+

then our equation in x and y transforms to the equation
::

          2           2
      d1 u    +   d2 v

since
::

           2                 2
          a x   +  b xy  +  c y

           +-    -+              +- -+
      =    | x  y |      SYM     | x |
           +-    -+              |   |
                                 | y |
                                 +- -+

           +-    -+   T          +- -+
      =    | u  v |  M   SYM  M  | u |
           +-    -+              |   |
                                 | v |
                                 +- -+

           +-    -+  +-      -+  +- -+
      =    | u  v |  | d1   0 |  | u |
           +-    -+  |        |  |   |
                     | 0   d2 |  | v |
                     +-      -+  +- -+


               2            2
      =    d1 u    +    d2 v

This last equation is that of an ellipse, as long as d1 and d2 are
positive. To verify that they are, note that d1 and d2 are the
eigenvalues of the matrix SYM, and SYM is the product
::

         -1  T   -1
      ( C   )   C,

which is of the form
::

       T
      M   M,

so SYM is positive semi-definite (its eigenvalues are non-negative).
Furthermore, since the product
::

         -1  T   -1
      ( C   )   C

is non-singular if C is non-singular, and since the columns of C are
V1 and V2, SYM exists and is non-singular precisely when V1 and V2
are linearly independent, a condition that we have assumed. So the
eigenvalues of SYM can't be zero. They're not negative either. We
conclude they're positive.


Solving intersection problems
-------------------------------


| There is one problem solving technique used in SPICE ellipse and
  ellipsoid routines that is so useful that it deserves special
  mention: using a 'distortion map' to solve intersection problems.

The distortion map (as it is referred to in CSPICE routines) is
simply a linear transformation that maps an ellipsoid to the unit
sphere. The distortion map defined by an ellipsoid whose semi-axes
are A, B, and C is represented by the matrix

::

      +-                -+
      |  1/A   0    0    |
      |   0   1/B   0    |.
      |   0    0    1/C  |
      +-                -+

The distortion map is (as is clear from examining the matrix)
one-to-one and onto, and in particular is invertible, so it preserves
set operations such as intersection. That is, if M is a distortion
map and X, Y are two sets, then
::

      M( X intersect Y ) = M(X) intersect M(Y).

The same is true of the inverse of the distortion map.
The utility of these facts is that frequently it's easier to find the
intersection of the images under the distortion map of two sets than
it is to find the intersection of the original two sets. Having found
the intersection of the 'distorted' sets, we apply the inverse
distortion map to arrive at the intersection of the original sets.
Some examples:

- To find the intersection of a ray and an ellipsoid, apply
  the distortion map to both. Because the distortion map is linear,
  the ray maps to another ray, and the ellipsoid maps to the unit
  sphere. The resulting intersection problem is easy to solve. Having
  found the points of intersection of the new ray and the unit
  sphere, if any, we apply the inverse distortion map to these
  points, and we're done.

- To find the intersection of a plane and an ellipsoid, apply
  the distortion map to both. The linearity of the distortion map
  ensures that the original plane maps to a second plane (whose
  formula is easily calculated). The ellipsoid maps to the unit
  sphere. The intersection of a plane and a unit sphere is easily
  found. The inverse distortion map is then applied to the circle of
  intersection (when the intersection is non-trivial), and the
  ellipse of intersection of the original plane and ellipsoid
  results. This procedure is used in the CSPICE routine
  `inedpl_c <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/cspice/inedpl_c.html>`__.

- To find the image under gnomonic projection onto a plane
  (camera projection) of an ellipsoid, given a focal point, we must
  find the intersection of the plane and the cone generated by
  ellipsoid and the focal point. Applying the distortion map to the
  ellipsoid, plane, and focal point, the problem is transformed into
  that of finding the intersection of the transformed plane with the
  cone generated by a unit sphere and the transformed focal point.
  This 'transformed' problem is much easier to solve. The resulting
  intersection ellipse is then mapped back to the original
  intersection ellipse by the inverse distortion mapping.


