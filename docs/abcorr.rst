***************************************
Aberration Corrections Required Reading
***************************************

This required reading document is reproduced from the original NAIF
document available at `https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/abcorr.html <https://naif.jpl.nasa.gov/pub/naif/misc/toolkit_docs_N0067/C/req/abcorr.html>`_

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

 | The SPICE Toolkit can calculate positions, velocities, and
   orientations corrected for aberrations caused by the finite speed
   of light, and the relative velocity of the target to observer.


Purpose
-------

 | This document is a reference guide describing the details of the
   aberration correction calculations as implemented in the SPICE
   system.


Intended Audience
-----------------

 | This document is for SPICE users who need specifics concerning the
   application of aberration corrections to state calculations.


References
^^^^^^^^^^

    #. Jesperson and Fitz-Randolph, From Sundials to Atomic Clocks, Dover Publications, New York, 1977.


Introduction
============

 | In space science or engineering applications one frequently wishes
   to know where to point a remote sensing instrument, such as an
   optical camera or radio antenna, in order to observe or otherwise
   receive radiation from a target. This pointing problem is
   complicated by the finite speed of light: one needs to point to
   where the target appears to be as opposed to where it actually is
   at the epoch of observation. We use the adjectives "geometric,"
   "uncorrected," or "true" to refer to an actual position or state of
   a target at a specified epoch. When a geometric position or state
   vector is modified to reflect how it appears to an observer, we
   describe that vector by any of the terms "apparent," "corrected,"
   "aberration corrected," or "light time and stellar aberration
   corrected." The SPICE Toolkit can correct for two phenomena
   affecting the apparent location of an object: one-way light time
   (also called "planetary aberration") and stellar aberration.


Types of Corrections
--------------------


One-way Light Time
^^^^^^^^^^^^^^^^^^

 | Correcting for one-way light time is done by computing, given an
   observer and observation epoch, where a target was when the
   observed photons departed the target's location. The vector from
   the observer to this computed target location is called a "light
   time corrected" vector. The light time correction depends on the
   motion of the target relative to the solar system barycenter, but
   it is independent of the velocity of the observer relative to the
   solar system barycenter. Relativistic effects such as light bending
   and gravitational delay are not accounted for in the light time
   corrections.


Stellar Aberration
^^^^^^^^^^^^^^^^^^

 | The velocity of the observer also affects the apparent location of
   a target: photons arriving at the observer are subject to a
   "raindrop effect" whereby their velocity relative to the observer
   is, using a Newtonian approximation, the photons' velocity relative
   to the solar system barycenter minus the velocity of the observer
   relative to the solar system barycenter. This effect is called
   "stellar aberration." Stellar aberration is independent of the
   velocity of the target. The stellar aberration formula used by
   SPICE routines does not include (the much smaller) relativistic
   effects.

 Stellar aberration corrections are applied after light time
 corrections: the light time corrected target position vector is used
 as an input to the stellar aberration correction.

 When light time and stellar aberration corrections are both applied
 to a geometric position vector, the resulting position vector
 indicates where the target "appears to be" from the observer's
 location.

 As opposed to computing the apparent position of a target, one may
 wish to compute the pointing direction required for transmission of
 photons to the target. This also requires correction of the geometric
 target position for the effects of light time and stellar aberration,
 but in this case the corrections are computed for radiation traveling
 \*from\* the observer to the target. We will refer to this situation
 as the "transmission" case.

 The "transmission" light time correction yields the target's location
 as it will be when photons emitted from the observer's location at
 ``et`` arrive at the target. The transmission stellar aberration
 correction is the inverse of the traditional stellar aberration
 correction: it indicates the direction in which radiation should be
 emitted so that, using a Newtonian approximation, the sum of the
 velocity of the radiation relative to the observer and of the
 observer's velocity, relative to the solar system barycenter, yields
 a velocity vector that points in the direction of the light time
 corrected position of the target.

 One may object to using the term "observer" in the transmission case,
 in which radiation is emitted from the observer's location. The
 terminology was retained for consistency with earlier documentation.


SPICE Aberration Identifiers (also called Flags)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 | SPICE uses a set of string flags to indicate the particular
   aberration corrections to apply to state evaluations.


``NONE``
  **Apply no correction.** Return the geometric state of the target body relative to the observer.

 The following flags apply to the "reception" case in which photons
 depart from the target's location at the light-time corrected epoch
 ET-LT and \*arrive\* at the observer's location at ET:

``LT``
  **Correct for one-way light time (also called "planetary aberration") using a Newtonian formulation.**

 This correction yields the state of the target at the moment it emitted photons arriving at the observer at ET.
 The light time correction uses an iterative solution of the light
 time equation (see Particulars for details). The solution invoked by
 the ``LT`` option uses one iteration.

``LT+S``
  **Correct for one-way light time and stellar aberration using a Newtonian formulation.**

  This option modifies the state obtained with the ``LT`` option to account for the observer's velocity relative to the solar system barycenter. The result is the apparent state of the target---the position and velocity of the target as seen by the observer.

``CN``
  **Converged Newtonian light time correction.**

 In solving the light time equation, the ``CN`` correction iterates until the
 solution converges (three iterations on all supported platforms).
 Whether the ``CN+S`` solution is substantially more accurate than the
 ``LT`` solution depends on the geometry of the participating objects
 and on the accuracy of the input data. In all cases, the correction
 calculation will execute more slowly when a converged solution is
 computed. See the Particulars section below for a discussion of
 precision of light time corrections.

``CN+S``
  **Converged Newtonian light time correction and stellar aberration correction.**

 The following values of ABCORR apply to the "transmission" case in
 which photons **depart** from the observer's location at ET and
 arrive at the target's location at the light-time corrected epoch
 ET+LT:

``XLT``
  **"Transmission" case: correct for one-way light time using a Newtonian formulation.**

  This correction yields the state of the
  target at the moment it receives photons emitted from the
  observer's location at ET.

``XLT+S``
  **"Transmission" case: correct for one-way light time and stellar aberration using a Newtonian formulation.**

  This option modifies the state obtained with the ``XLT`` option to account for
  the observer's velocity relative to the solar system barycenter.
  The position component of the computed target state indicates the
  direction that photons emitted from the observer's location must be
  "aimed" to hit the target.

``XCN``
  **"Transmission" case: converged Newtonian light time correction.**

``XCN+S``
  **"Transmission" case: converged Newtonian light time correction and stellar aberration correction.**


Common Correction Applications
------------------------------

 | Below, we indicate the aberration corrections to use for some
   common applications:

#.  Find the apparent direction of a target. This is the most common case for a remote-sensing observation.

    **Use LT+S or CN+S**: apply both light time and stellar aberration corrections.

    .. note::

        Note that using light time corrections alone (``LT``) is
        generally not a good way to obtain an approximation to an apparent
        target vector: since light time and stellar aberration corrections
        often partially cancel each other, it may be more accurate to use
        no correction at all than to use light time alone.

#.  Find the corrected pointing direction to radiate a signal to a target. This computation is often applicable for implementing communications sessions.

    **Use XLT+S or XCN+S**: apply both light time and stellar  aberration corrections for transmission.

#.  Compute the apparent position of a target body relative to a star or other distant object.

    **Use one of LT, CN, LT+S, or CN+S as needed to match the correction applied to the position of the distant object.**
    For example, if a star position is obtained from a catalog, the
    position vector may not be corrected for stellar aberration. In
    this case, to find the angular separation of the star and the limb
    of a planet, the vector from the observer to the planet should be
    corrected for light time but not stellar aberration.

#. Obtain an uncorrected state vector derived directly from data in an SPK file.

    **Use NONE.**

#. Use a geometric state vector as a low-accuracy estimate of the apparent state for an application where execution speed is critical.

    **Use NONE.**

#. While the correction routines do not perform the relativistic aberration corrections required to compute states with the highest possible accuracy, they can supply the geometric states required as inputs to these computations.

    **Use NONE, then apply relativistic aberration corrections (not available in the SPICE Toolkit).**


Computation of Corrections
--------------------------

Below, we discuss in more detail how the aberration corrections are computed.

Geometric case
^^^^^^^^^^^^^^
 | The algorithm begins by computing the geometric position T(t) of
   the target body relative to the solar system barycenter (SSB).
   Subtracting the geometric position of the observer O(t) gives the
   geometric position of the target body relative to the observer. The
   one-way light time, lt, is given by

 .. math::
    lt = \frac{\lVert T(t) - O(t) \rVert}{c}

 | The geometric relationship between the observer, target, and solar system barycenter is as shown:

 ::

             SSB ---> O(t)
              |      /
              |     /
              |    /
              |   /  T(t) - O(t)
              |  /
              | /
              |/
              V
             T(t)



 | The returned state consists of the position vector

 .. math::
    T(t) - O(t)

 | and a velocity obtained by taking the difference of the corresponding
  velocities. In the geometric case, the returned velocity is actually
  the time derivative of the position.

Reception case
^^^^^^^^^^^^^^
 z When any of the options ``LT``, ``CN``, ``LT+S``, ``CN+S`` is selected for
  ``abcorr``, the algorithm computes the position of the target body
  at epoch et-lt, where ``lt`` is the one-way light time. Let T(t) and
  O(t) represent the positions of the target and observer relative to
  the solar system barycenter at time t; then ``lt`` is the solution
  of the light-time equation

 .. math:: lt = \frac{\lVert T(t-lt) - O(t) \rVert}{c} (1)

 | The ratio

 .. math:: \frac{\lVert T(t) - O(t) \rVert}{c} (2)

 is used as a first approximation to ``lt``; inserting (2) into the
 right hand side of the light-time equation (1) yields the
 "one-iteration" estimate of the one-way light time (``LT``). Repeating
 the process until the estimates of ``lt`` converge yields the
 "converged Newtonian" light time estimate (``CN``). This methodology
 performs a contraction mapping.
 Subtracting the geometric position of the observer O(t) gives the
 position of the target body relative to the observer: T(t-lt) - O(t).::

             SSB ---> O(t)
              | \     |
              |  \    |
              |   \   | T(t-lt) - O(t)
              |    \  |
              |     \ |
              |      \|
              V       V
             T(t)  T(t-lt)

 Note, in general, the vectors defined by T(t), O(t), T(t-lt) - O(t),
 and T(t-lt) are not coplanar.
 The position component of the light time corrected state is the
 vector

 .. math::
    T(t-lt) - O(t)

 The velocity component of the light time corrected state is the difference

 .. math::
    \frac{d(T(t - lt) - O(t))}{dt} = T_{\text{vel}}(t - lt) \cdot \left(1 - \frac{d(lt)}{dt}\right) - O_{\text{vel}}(t)

 where T_vel and O_vel are, respectively, the velocities of the target
 and observer relative to the solar system barycenter at the epochs
 et-lt and ``et``.
 If correction for stellar aberration is requested, the target
 position is rotated toward the solar system barycenter- relative
 velocity vector of the observer. The rotation is computed as follows:

 Let r be the light time corrected vector from the observer to the
 object, and v be the velocity of the observer with respect to the
 solar system barycenter. Let w be the angle between them. The
 aberration angle phi is given by

 .. math::
   sin(phi) = \frac{v sin(w)}{c}

 Let h be the vector given by the cross product

 .. math::
     h = r X v

 Rotate r by phi radians about h to obtain the apparent position of
 the object.
 When stellar aberration corrections are used, the rate of change of
 the stellar aberration correction is accounted for in the computation
 of the output velocity.


Transmission case
^^^^^^^^^^^^^^^^^
 | When any of the options ``XLT``, ``XCN``, ``XLT+S``, ``XCN+S`` is selected,
   the algorithm computes the position of the target body T at epoch
   et+lt, where ``lt`` is the one-way light time. ``lt`` is the solution
   of the light-time equation

 .. math::
   lt = \frac{\lVert T(t+lt) - O(t) \rVert}{c} (3)

 Subtracting the geometric position of the observer, O(t), gives the
 position of the target body relative to the observer: T(t+lt) - O(t).::

                      O(t) <--- SSB
                         |     / |
                         |    /  |
          T(t+lt) - O(t) |   /   |
                         |  /    |
                         | /     |
                         |/      |
                         V       V
                     T(t+lt)  T(t)

 Note, in general, the vectors defined by T(t), O(t), T(t+lt) - O(t),
 and T(t+lt) are not coplanar.
 The position component of the light-time corrected state is the
 vector

 .. math::
    T(t+lt) - O(t)

 The velocity component of the light-time corrected state consists of
 the difference

 .. math::
    \frac{d(T(t + lt) - O(t))}{dt} = T_{\text{vel}}(t + lt) \cdot \left(1 + \frac{d(lt)}{dt}\right) - O_{\text{vel}}(t)

 where T_vel and O_vel are, respectively, the velocities of the target
 and observer relative to the solar system barycenter at the epochs
 ``et+lt`` and ``et``.
 If correction for stellar aberration is requested, the target
 position is rotated away from the solar system barycenter-relative
 velocity vector of the observer. The rotation is computed as in the
 reception case, but the sign of the rotation angle is negated.


Precision of light time corrections
-----------------------------------

 | Let:

 .. math::
    \text{beta} =  \frac{V}{C}

 where V is the velocity of the target relative to an inertial frame
 and C is the speed of light.


Corrections using one iteration of the light time
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 | When the requested aberration correction is ``LT``, ``LT+S``, ``XLT``, or
   ``XLT+S``, only one iteration is performed in the algorithm used to
   compute lt.

 | The relative error in this computation

 .. math::
    \frac{\lVert \text{lt_actual} - \text{lt_computed} \rVert}{\text{lt_actual}}

 | is at most

 .. math::
    \frac{beta^2}{1 - beta}

 | which is well approximated by beta**2 for beta << 1 since

.. math::
  \frac{beta^2}{ -x} \approx 1 + x + x^2 + x^3 + x^4 + x^5 + O(x^6)  (4)

| about x = 0. So with x = beta

.. math::
  \frac{beta^2}{1 - beta} \approx beta^2 + beta^3 + beta^4 + O(beta^5)

For nearly all objects in the solar system V is less than 60 km/sec.
The value of C is ~300000 km/sec. Thus the one-iteration solution for
``lt`` has a potential relative error of not more than 4e-8. This is a
potential light time error of approximately 2e-5 seconds per
astronomical unit of distance separating the observer and target.
Given the bound on V cited above:
As long as the observer and target are separated by less than 50
astronomical units, the error in the light time returned using the
one-iteration light time corrections is less than 1 millisecond.

The magnitude of the corresponding position error, given the above
assumptions, may be as large as beta**2 \* the distance between the
observer and the uncorrected target position: 300 km or equivalently
6 km/AU.

In practice, the difference between positions obtained using
one-iteration and converged light time is usually much smaller than
the value computed above and can be insignificant. For example, for
the spacecraft Mars Reconnaissance Orbiter and Mars Express, the
position error for the one-iteration light time correction, applied
to the spacecraft-to-Mars center vector, is at the 1 cm level.

Comparison of results obtained using the one-iteration and converged
light time solutions is recommended when adequacy of the
one-iteration solution is in doubt.


Converged corrections
^^^^^^^^^^^^^^^^^^^^^
 | When the requested aberration correction is ``CN``, ``CN+S``, ``XCN``, or
   ``XCN+S``, as many iterations as are required for convergence are
   performed in the computation of LT. Usually the solution is found
   after three iterations.

 The relative error present in this case is at most

  .. math::
    \frac{beta^4}{1 - beta}

 which is well approximated by beta**4 for beta << 1 since using (4)
 with x = beta as before

 .. math::
  \frac{beta^4}{1 - beta} \approx beta^4 + beta^5 + beta^6 + O(beta^7)

 The precision of this computation (ignoring round-off error) is
 better than 4e-11 seconds for any pair of objects less than 50 AU
 apart, and having speed relative to the solar system barycenter less
 than 60 km/s ( beta = 2.001e-4, beta**4 = 1.604e-15).
 The magnitude of the corresponding position error, given the above
 assumptions, may be as large as beta**4 \* the distance between the
 observer and the uncorrected target position: 1.2 cm at 50 AU or
 equivalently 0.24 mm/AU.

 However, to very accurately model the light time between target and
 observer one must take into account effects due to general
 relativity. These may be as high as a few hundredths of a millisecond
 for some objects.


Corrections in Non-inertial Frames
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

 |
 | When applying corrections in a non inertial reference frame, the
   epoch at which to evaluate frame orientation is adjusted by the
   one-way light time, ``lt``, between the observer and the frame's
   center. The orientation of the frame is evaluated at the time of
   interest - lt, the time of interest + lt, or the time of interest
   depending on whether the requested aberration correction is,
   respectively, for received radiation, transmitted radiation, or is
   omitted. ``lt`` is computed using the method indicated by the
   aberration correction flag.


Relativistic Corrections
------------------------


 | SPICE aberration correction routines do not attempt to perform
   either general or special relativistic corrections in computing the
   various aberration corrections. For many applications relativistic
   corrections are not worth the expense of added computation cycles.
   If your application requires these additional corrections we
   suggest you consult the astronomical almanac (page B36) for a
   discussion of how to carry out these corrections.




