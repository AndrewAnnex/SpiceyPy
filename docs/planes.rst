************************
Planes Required Reading
************************

This required reading document is reproduced from the original NAIF
document available at `https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/planes.html <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/planes.html>`_

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

 | CSPICE contains a substantial set of subroutines that solve common
   mathematical problems involving planes.

Introduction
------------

 | In CSPICE, the 'plane' is a data representation describing planes
   in three-dimensional space. The purpose of the plane data type is
   to simplify the calling sequences of some geometry routines. Also,
   using a "plane" data type helps to centralize error checking and
   facilitate conversion between different representations of planes.

References
^^^^^^^^^^


#. 'Calculus, Vol. II'. Tom Apostol. John Wiley and Sons,
   * See Chapter 5, 'Eigenvalues of Operators Acting on Euclidean Spaces'.

#. Ellipses required reading
   (`ellipses <./ellipses.html>`__).



Plane Data Type Description
============================

 | NAIF defines a SPICE plane using a unit vector N, normal to the
   plane, and a scalar constant C. Let

 ::

       < X, Y >

 denote the inner product of the vectors X and Y, then the
 relationship
 ::

       < X, N > = C

 holds for all vectors X in the plane. C is the distance of the plane
 from the origin. The vector
 ::

       C * N

 is the closest point in the plane to the origin. For planes that do
 not contain the origin, the vector N points from the origin toward
 the plane.
 The internal design of the plane data type is not part of its
 specification. The design is an implementation choice based on the
 programming language and so the design may change. Users should not
 write code based on the current implementation; such code might fail
 when used with a future version of CSPICE.

 NAIF implemented the SPICE plane data type in C as a structure with
 the fields

 ::

          SpiceDouble      normal   [3];
          SpiceDouble      constant;

 'normal' contains the unit normal vector N; 'constant' contains the
 plane constant C.

 In SpiceyPy, this structure is defined by :py:class:`~spiceypy.utils.support_types.Plane`,
 although users are encouraged not to directly interact with this object and to instead use the spice routines described below for creating and using them.


Plane routines
===============


Constructing planes
--------------------

 | The CSPICE routines that create SPICE planes from various forms of
   data that define geometric planes:

 :py:meth:`~spiceypy.spiceypy.nvc2pl`
    Normal vector and constant to plane

 :py:meth:`~spiceypy.spiceypy.nvp2pl`
    Normal vector and point to plane

 :py:meth:`~spiceypy.spiceypy.psv2pl`
    Point and spanning vectors to plane

 SPICE routines that take planes as input arguments can accept planes
 created by any of the routines listed above.
 The information stored in SPICE planes is not necessarily the input
 information you supply to a plane-making routine. SPICE planes use a
 single, uniform internal representation for planes, no matter what
 data you use to create them. As a consequence, when you create a
 SPICE plane and then break it apart into data that define a plane,
 the returned data will not necessarily be the data you originally
 supplied, though they define the same geometric plane as the data you
 originally supplied.

 This 'loss of information' may seem to be a liability at first but
 turns out to be a convenience in the end: the SPICE routines that
 break apart SPICE planes into various representations return outputs
 that are particularly useful for many geometric computations. In the
 case of the routine :py:meth:`~spiceypy.spiceypy.pl2nvp` (Plane to
 normal vector and point), the output normal vector is always a unit
 vector, and the output point is always the closest point in the plane
 to the origin. The normal vector points from the origin toward the
 plane, if the plane does not contain the origin.

 You can convert any of the following representations of planes to a
 SPICE plane:

 **A normal vector and a constant**
    If N is a normal vector and C is a constant, then the plane is the
    set of points X such that

 ::

                                  < X, N > = C.

 **A normal vector and a point**
    If P is a point in the plane and N is a normal vector, then the
    plane is the set of points X such that

 ::

                                  < X - P,  N > = 0.

 **A point and two spanning vectors**
    If P is a point in the plane and V1 and V2 are two linearly
    independent but not necessarily orthogonal vectors, then the plane
    is the set of points

 ::

                                  P   +   s * V1   +   t * V2,

 where s and t are real numbers.

 The calling sequences of the SPICE routines that create planes are
 described below. For examples of how you might use these routines in
 a program, see the Examples section.


Construct a plane from a normal vector and constant
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 | Let 'n' represent a vector normal to a plane, and 'c', a scalar
   constant.

 Let 'n' and 'c' be declared by

 .. code-block:: python

       n = [1.0, 1.0, 1.0] # can also use numpy arrays here
       c = 2.0

 After 'n' and 'c' have been assigned values, you can construct a
 SPICE plane that represents the plane having normal 'n' and constant
 'c' by calling :py:meth:`~spiceypy.spiceypy.nvc2pl`:

 .. code-block:: python

       import spiceypy

       plane = spiceypy.nvc2pl( n, c )



Construct a plane from a normal vector and a point
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 | Let 'n' represent a vector normal to a plane, and 'p', a point on
   the plane.

 Declare 'n' and 'p' as:

 .. code-block:: python

       n = [1.0, 1.0, 1.0] # can also use numpy arrays here
       p = [1.0, 4.0, 9.0]

 After 'n' and 'p' have been assigned values, you can construct a
 SPICE plane that represents the plane containing point 'p' and
 having normal 'n' by calling :py:meth:`~spiceypy.spiceypy.nvp2pl`:

 .. code-block:: python

       plane = spiceypy.nvp2pl( n, p )



Construct a plane from a point and spanning vectors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 | Let 'p' represent a point on a plane, 'v1' and 'v2', two vectors
   in the plane.

 Let 'p', 'v1', and 'v2' be declared by

 .. code-block:: python

       point = [..., ..., ...] # need 3 floating point numbers
       span1 = [..., ..., ...] # need 3 floating point numbers
       span2 = [..., ..., ...] # need 3 floating point numbers

 After 'p', 'v1', and 'v2' have been assigned values, you can
 construct a SPICE plane that represents the plane spanned by the
 vectors V1 and V2 and containing the point P by calling
 :py:meth:`~spiceypy.spiceypy.psv2pl`:

 .. code-block:: python

       plane = spiceypy.psv2pl ( p, v1, v2 )



Access plane data elements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 | You can 'take planes apart' as well as put them together. Any
   SPICE plane, regardless of which routine created it, can be
   converted to any of the representations listed in the previous
   section: normal vector and constant, point and normal vector, or
   point and spanning vectors.

 The CSPICE routines that break planes apart into data that define
 geometric planes are

:py:meth:`~spiceypy.spiceypy.pl2nvc`
    Plane to normal vector and constant

:py:meth:`~spiceypy.spiceypy.pl2nvp`
    Plane to normal vector and point

:py:meth:`~spiceypy.spiceypy.pl2psv`
    Plane to point and spanning vectors

 In the following discussion, 'plane' is a SPICE plane, 'n' is a
 normal vector, 'p' is a point, 'c' is a scalar constant, and V1 and
 V2 are spanning vectors. We omit the declarations; all are as in the
 previous section.
 To find a unit normal vector 'n' and a plane constant 'c' that
 define 'plane', use :py:meth:`~spiceypy.spiceypy.pl2nvc`:

 .. code-block:: python

       n, c = spiceypy.pl2nvc( plane )

 The constant 'c' is the distance of the plane from the origin. The
 vector
 ::

       C * N

 will be the closest point in the plane to the origin.
 To find a unit normal vector 'n' and a point 'p' that define
 'plane', use :py:meth:`~spiceypy.spiceypy.pl2nvp`:

 .. code-block:: python

       n, p = spiceypy.pl2nvp( plane )

 'p' will be the closest point in the plane to the origin. The unit
 normal vector 'n' will point from the origin toward the plane.
 To find a point 'p' and two spanning vectors 'v1' and 'v2' that
 define 'plane', use :py:meth:`~spiceypy.spiceypy.pl2psv`:

 .. code-block:: python

       p, v1, v2 = spiceypy.pl2psv( plane )

 'p' will be the closest point in the plane to the origin. The
 vectors 'v1' and 'v2' are mutually orthogonal unit vectors and are
 also orthogonal to 'p'.
 It is important to note that the xxx2PL and PL2xxx routines are not
 exact inverses of each other. The pairs of calls

 .. code-block:: python

       plane = spiceypy.nvc2pl( n, c )
       n, c = spiceypy.pl2nvc( plane )

       plane = spiceypy.nvp2pl( n, p )
       n, p = spiceypy.pl2nvp( plane )

       plane = spiceypy.psv2pl( p, v1, v2 )
       p, v1, v2 = spiceypy.pl2psv( plane )

 do not necessarily preserve the input arguments supplied to the
 xxx2PL routines. This is because the uniform internal representation
 of SPICE planes causes them to 'forget' what data they were created
 from; all sets of data that define the same geometric plane have the
 same internal representation in SPICE planes.
 In general, the routines :py:meth:`~spiceypy.spiceypy.pl2nvc`,
 :py:meth:`~spiceypy.spiceypy.pl2nvp`, and
 :py:meth:`~spiceypy.spiceypy.pl2psv` are used in routines that
 accept planes as input arguments. In this role, they simplify the
 routines that call them, because the calling routines no longer check
 the input planes' validity.

Examples
==========



Converting between representations of planes
---------------------------------------------

 | The SPICE plane routines can also be used as a convenient way to
   convert one representation of a plane to another. For example,
   suppose that given a normal vector 'n' and constant 'c' defining
   a plane, you must produce the closest point in the plane to the
   origin. The code fragment

 .. code-block:: python

       plane = spiceypy.nvc2pl( n, c )
       n,  point = spiceypy.pl2nvp( plane )



Translating planes
----------------------

 | A 'translation' T is a vector space mapping defined by the
   relation

 ::

       T(X) = X + A   for all vectors X

 where A is a constant vector. While it's not difficult to directly
 apply a translation map to a plane, using SPICE plane routines
 provides the convenience of automatically computing the closest point
 to the origin in the translated plane.
 Suppose a plane is defined by the point 'p' and the normal vector
 'n', and you wish to translate it by the vector 'x'. That is, you
 wish to find data defining the plane that results from adding 'x' to
 every vector in the original plane. You can do this with the code
 fragment

 .. code-block:: python

       p = spiceypy.vadd( p, x )              #(Vector addition, can be done with numpy instead)
       plane = spiceypy.nvp2pl( n, p )
       n, p = spiceypy.pl2nvp( plane )

 Now, 'p' is the closest point in the translated plane to the origin.


Applying linear transformations to planes
------------------------------------------

 | Suppose we have a normal vector N and constant C defining a plane,
   and we wish to apply a non-singular linear transformation T to the
   plane. We want to find a unit normal vector and constant that
   define the transformed plane; the constant should be the distance
   of the plane from the origin.

 Let T be represented by the matrix M.

 If Y is a point in the transformed plane, then

    .. math:: M^{-1} Y

 is a point in the original plane, so

    .. math:: \langle N, M^{-1} Y \rangle = C.

 But

    .. math::
       \langle N, M^{-1} Y \rangle
       = N^T M^{-1} Y

       = ( ( M^{-1} )^T N )^T Y

       = \langle ( M^{-1} )^T N , Y \rangle

 So

    .. math::   ( M^{-1} )^T N, C

 are, respectively, a normal vector and constant for the transformed plane.

 We can solve the problem using the following code fragments.
 Make a SPICE plane from 'n' and 'c', and then find a point in
 'plane' and spanning vectors for 'plane'. 'n' need not be a unit
 vector.

 .. code-block:: python

       plane = spiceypy.nvc2pl( n, c  )
       point, v1, v2 = spiceypy.pl2psv( plane )

 Apply the linear transformation to the point and spanning vectors.
 All we need to do is multiply these vectors by M, since for any
 linear transformation T,
 ::

                  T ( POINT   +     t1 * V1     +   t2 * V2 )

               =  T (POINT)   +   t1 * T (V1)   +   t2 * T (V2)

 which means that T(POINT), T(V1), and T(V2) are a a point and
 spanning vectors for the transformed plane.

 .. code-block:: python

       tpoint = spiceypy.mxv( m, point )
       tv1 = spiceypy.mxv( m, v1 )
       tv2 = spiceypy.mxv( m, v2 )

 Construct a new SPICE plane 'tplane' from the transformed point and
 spanning vectors, and find a unit normal and constant for this new
 plane.

 .. code-block:: python

       tplane = spiceypy.psv2pl( tpoint, tv1, tv2 )
       tn, tc = spiceypy.pl2nvc( tplane )



Finding the limb of an ellipsoid
---------------------------------

 | This problem is somewhat artificial, because the SPICE routine
   :py:meth:`~spiceypy.spiceypy.edlimb` already solves this problem.
   Nonetheless, it is a good illustration of how CSPICE plane routines
   are used.

 We'll work in body-fixed coordinates, which is to say that the
 ellipsoid is centered at the origin and has axes aligned with the x,
 y and z axes. Suppose that the semi-axes of the ellipsoid has lengths
 A, B, and C, and call our observation point

 .. math::

    P = (p_1, p_2, p_3).

 Then every point:

 .. math::

    X = (x_1, x_2, x_3)

 on the limb satisfies:

 .. math::

    \langle P - X, N \rangle = 0,

 where **N** is a surface normal vector at **X**. In particular, the gradient vector:

 .. math::

    \left( \frac{x_1}{A^2}, \frac{x_2}{B^2}, \frac{x_3}{C^2} \right)

 is a surface normal, so **X** satisfies:

 .. math::

    0 = \langle P - X, N \rangle

 .. math::

       = \langle P - X, ( \frac{x_1}{A^2}, \frac{x_2}{B^2}, \frac{x_3}{C^2} ) \rangle

 .. math::

       = \langle P, ( \frac{x_1}{A^2}, \frac{x_2}{B^2}, \frac{x_3}{C^2} ) \rangle
       - \langle X, ( \frac{x_1}{A^2}, \frac{x_2}{B^2}, \frac{x_3}{C^2} ) \rangle

 .. math::

       = \langle ( \frac{p_1}{A^2}, \frac{p_2}{B^2}, \frac{p_3}{C^2} ), X \rangle - 1


 and constant 1. We can create a SPICE plane representing the limb
 with the code fragment

 .. code-block:: python

      n[0] = p[0] / a**2
      n[1] = p[1] / b**2
      n[2] = p[2] / c**2

      plane = spiceypy.nvc2pl( n, 1. )

 The limb is the intersection of the limb plane and the ellipsoid. To
 find the intersection, we use the CSPICE routine
 :py:meth:`~spiceypy.spiceypy.inedpl` (Intersection of ellipsoid and plane):

 .. code-block:: python

        plane, ellips = spiceypy.inedpl( a,  b,  c )

 'ellips' is a SPICE 'ellipse', a data type analogous to the SPICE
 plane. We can use the SPICE routine
 :py:meth:`~spiceypy.spiceypy.el2cgv` (Ellipse to center and
 generating vectors) to find the limb's center, semi-major axis, and
 semi-minor axis:

 .. code-block:: python

       center, smajor, sminor = spiceypy.el2cgv( ellips )

Use of ellipses with planes
============================

 | The nature of geometry problems involving planes often includes use
   of the SPICE ellipse data type. The example code listed in the
   headers of the routines :py:meth:`~spiceypy.spiceypy.inelpl` and
   :py:meth:`~spiceypy.spiceypy.pjelpl` show examples of problems
   solved using both the ellipse and plane data type.

Summary of routines
===================

 | The following table summarizes the CSPICE plane routines.

       :py:meth:`~spiceypy.spiceypy.inedpl`
                   Intersection of ellipsoid and plane
       :py:meth:`~spiceypy.spiceypy.inelpl`
                   Intersection of ellipse and plane
       :py:meth:`~spiceypy.spiceypy.inrypl`
                   Intersection of ray and plane
       :py:meth:`~spiceypy.spiceypy.nvc2pl`
                   Normal vector and constant to plane
       :py:meth:`~spiceypy.spiceypy.nvp2pl`
                   Normal vector and point to plane
       :py:meth:`~spiceypy.spiceypy.pjelpl`
                   Project ellipse onto plane
       :py:meth:`~spiceypy.spiceypy.pl2nvc`
                   Plane to normal vector and constant
       :py:meth:`~spiceypy.spiceypy.pl2nvp`
                   Plane to normal vector and point
       :py:meth:`~spiceypy.spiceypy.pl2psv`
                   Plane to point and spanning vectors
       :py:meth:`~spiceypy.spiceypy.psv2pl`
                   Point and spanning vectors to plane
       :py:meth:`~spiceypy.spiceypy.vprjp`
                   Vector projection onto plane
       :py:meth:`~spiceypy.spiceypy.vprjpi`
                   Vector projection onto plane, inverted


