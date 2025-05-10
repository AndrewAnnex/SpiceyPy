Cython Enhancement to SpiceyPy: Cyice
=====================================

.. |ipa319| unicode:: U+026A
    :trim:

A recent NASA PDART grant award (80NSSC25K7040) has funded work to significantly enhance SpiceyPy by implementing Cython (`cython.org` <https://www.cython.org>_)-based wrapper functions to CSPICE within SpiceyPy.
This new submodule is called Cyice (pronounced “syce” or /sa|ipa319|s/). 

Cyice wrapper functions are much faster than the corresponding existing c-types wrappers in SpiceyPy,
up to an order of magnitude faster for certain functions. 
Vectorized functions will also be implemented for a majority of the Cyice wrappers.

Critically, because Cyice uses the same underlying shared library for CSPICE as SpiceyPy, 
Cyice and SpiceyPy functions can be used interchangeably in a Python program.
For example, you can load a kernel using SpiceyPy's furnsh function, then call spkpos from Cyice using the same kernel pool. 

This enables the gradual development of Cyice to occur in phases with minimal to no user disruption. 
Cyice is not replacing SpiceyPy, exactly, and will remain a submodule to SpiceyPy. 

Think of it like remodeling a house or replacing the drivetrain in a car.

As Cyice functions are being constructed in a new sub module, existing codes will not use these functions unless they are explicitly imported. 
A majority of Cyice functions will follow the existing SpiceyPy API and functionality, so breaking changes, if any, will be minimal and preceded by major version releases. 

Using Cyice
---------------

Cyice functions are nearly 1-to-1 replaceable with SpiceyPy functions, except for some minor caveats explained below.

Cyice is a submodule to SpiceyPy and can be imported via `from spiceypy import cyice`, like so:

```python
# do the regular import
import spiceypy
# call a spiceypy function
spiceypy.b1900()
# now import Cyice
from spiceypy import cyice
# now call the equivalent cyice function
cyice.b1900()
```

Because Cyice and SpiceyPy both link to the same CSPICE library, they can be used interchangeably.
For example:

```python
# load a kernel with SpiceyPy
spiceypy.furnsh('path/to/kernel.txt')
# call str2et from cyice using the same populated kernel pool
et = cyice.str2et("July 4, 2003 11:00 AM PST")
```

If a function from SpiceyPy is not available yet in Cyice, simply use the SpiceyPy version (and consider making a open source code contribution to add it!).

Scalar values and strings work just like with SpiceyPy, accepting conventional Python objects, integers, and floats:

```python
cyice.convrt(1.0, "parsecs", "lightyears") # returns ~482.8032
```

Numeric arrays, vectors, and matrices however must be provided as NumPy arrays, typically with the double (float64) datatype:

```python
camid = spice.bodn2c("CASSINI_ISS_NAC")
raydir = np.array([0.0, 0.0, 1.0], dtype=np.double)
cyice.fovray("CASSINI_ISS_NAC", raydir, frame, "S", "CASSINI", et)
```

Cyice will always return vectors and matrices as NumPy arrays:

```python
pos, lt = cyice.spkgps(499, et, "J2000", 399)
# lt is a scalar python float, pos is a double precision NumPy array
```

Vectorized functions are currently always postfixed by `_v` to differentiate them.

For example for `cyice.convrt`, the vectorized function equivalent is `cyice.convrt_v`

For vectorized functions Cyice will always return NumPy arrays,
one per scalar or array output, similar to how vectorized SpiceyPy functions behaved.

Cyice also expects inputs for vectorization to be NumPy arrays, even for lists of strings, these must be turned into NumPy arrays.

```python
dates = np.repeat(["Thu Mar 20 12:53:29 PST 1997"], 2)
ets = cyice.str2et_v(dates) # ets is a NumPy double array of length 2
```

Vectorized functions are generally advisable when running a function more than 100 times.
This is due to the overhead with creating NumPy arrays, which has a small cost that is irrelevant when thousands to millions of calls occur.


Development Plan
----------------

The first phase will introduce Cyice wrapper functions for the following CSPICE functions:

   * ckgp	
   * ckgpav	
   * deltet	
   * etcal	
   * et2lst	
   * et2utc	
   * fovray	
   * fovtrg	
   * furnsh	
   * lspcn	
   * str2et	
   * scs2e	
   * sce2s	
   * sct2e	
   * sce2c	
   * scencd	
   * scdecd	
   * spkezr	
   * spkez	
   * spkezp	
   * spkpos	
   * spkapo	
   * spkpvn	
   * spkssb	
   * spkgeo	
   * spkgps	
   * spkcpo	
   * spkcpt	
   * spkcvo	
   * spkcvt	
   * sincpt	
   * subpnt	
   * subslr	
   * tangpt	
   * timout	
   * trgsep	
   * unitim	
   * unload	
   * utc2et	

The second phase will then add the following functions:

   * azlcpo
   * azlrec
   * cyllat
   * cylrec
   * cylsph
   * georec
   * latcyl
   * latrec
   * latsph
   * pgrrec
   * radrec
   * recazl
   * reccyl
   * recgeo
   * reclat
   * recpgr
   * recrad
   * recsph
   * sphcyl
   * sphlat
   * sphrec
   * srfrec
   * xfmsta  
   * ilumin
   * illumg
   * illumf
   * phaseq
   * limpt
   * termpt
   * occult
   * conics
   * oscelt
   * getelm
   * evsgp4
   * halfpi
   * pi
   * twopi
   * dpr
   * rpd
   * spd
   * jyear
   * tyear
   * clight
   * b1900
   * b1950
   * j1900
   * j1950
   * j2000
   * j2100


Benchmarks
-----------

