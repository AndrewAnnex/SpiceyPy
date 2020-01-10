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


# Acknowledgements
The authors would like to acknowledge the authors of the SPICE toolkit for continued 

# References