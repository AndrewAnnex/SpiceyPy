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

