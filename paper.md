---
title: 'SpiceyPy: a Pythonic Wrapper for the SPICE Toolkit'
tags:
  - Python
  - SPICE
  - ephemeris
  - geometry
  - navigation
  - spacecraft
authors:
  - name: Andrew M. Annex
    orcid: 0000-0002-0253-2313
    affiliation: 1
affiliations:
 - name: Johns Hopkins University
   index: 1
date: 10 January 2020
bibliography: paper.bib

---

# Summary

``SpiceyPy`` is a open source and community developed Python package that provides a ``pythonic`` interface 
to the SPICE toolkit produced by the Navigation and Ancillary Information Facility at JPL. SPICE is used by
scientists and engineers working with robotic planetary spacecraft missions to help plan observations and to
understand the positions of planetary bodies through time. SpiceyPy enables scientists to utilize the full
functionality of SPICE within python and the ecosystem of visualization and data science packages available. 
  
In the planetary sciences field, scientists and engineers work together to build and operate space missions. 
Operating in space necessitates quantifying the positions, velocities, and other properties of planetary bodies 
and spacecraft through time. The SPICE Toolkit was concieved in response to the 1982 The National Research Council's
 Committee on Data Management and Computation (CODMAC) report, which advocated for archieving engineering data 
from space missions operated by NASA to better contextualize and interpret data returned by missions.
SPICE is currently developed in Fortran77 and ANSI C, the C version is generated from the Fortran77 source code 
using the f2c program. The NAIF currently provides a small number of wrappers for SPICE in higher level languages, including Matlab, IDL, and Java.

``SpiceyPy`` is implemented in pure python using the ``ctypes`` module of the cpython standard library. The
library provides a practically complete interface to the CSPICE library with over 600 wrapper functions.
All wrapper functions are tested using a combination of unit and integration test using pytest, which are run 
using CI services. The numpy library is the primary dependency for ``SpiceyPy``, as numpy is foundational 
to the SciPy stack. Prior to version 3.0.0, ``SpiceyPy`` was written to by cross compatible with Python 2.7.X using the ``Six``
package for compatibility. Version 3.0.0 of ``SpiceyPy`` marked the deprication of Python 2 support in SpiceyPy 
along with the adoptation of the python black code linting style. Additonally, as of the 3.0.0 release migration
of type annotations from docstrings to the use of type hints enabled simplification of docstrings. SpiceyPy 
utilizes CI services such as appveyor, travis ci, readthedocs, coveralls, and conda-forge to simplify
development and deployment. 


# Acknowledgements
The authors would like to acknowledge the authors of the SPICE toolkit for continued 

# References