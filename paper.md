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

Operating in space necessitates quantifying the positions, velocities, and other properties of spacecraft and planetary bodies through time. 
The SPICE toolkit is produced by the Navigation and Ancillary Information Facility (NAIF) at the Jet Propulsion Lab (JPL).
Scientists and engineers working with robotic planetary spacecraft missions use SPICE to help plan observations and to quantify the positions of planetary bodies and spacecraft through time.
The NAIF develops SPICE in Fortran77, and provides some higher-level language wrappers; however, as of 2014, they did not offer a Python interface.

``SpiceyPy`` is an open-source Python package that provides a ``pythonic`` interface to nearly all of the SPICE toolkit C API N66. 
Unlike SWIG based wrapper libraries, ``SpiceyPy`` was developed in Python using the ``ctypes`` module of the CPython standard library. 
Developing ``SpiceyPy`` in Python enabled simplifications of the underlying C API.
``SpiceyPy`` relies on the NumPy library for numeric arrays and tight integration with the SciPy stack.

``SpiceyPy`` is extensively tested using a combination of unit and integration tests, which run using continuous integration services. 
The tests also serve as code examples translated from the NAIF documentation.
 Continuous deployment updates documentation and deploys artifacts of releases to PyPI and the conda-forge.

``SpiceyPy`` enables scientists to utilize the full functionality of SPICE within Python and the ecosystem of visualization and data science packages available.
``SpiceyPy`` has been utilized in peer-reviewed research, masters and doctoral theses, spacecraft and CubeSat mission operations, 
as a dependency in other python libraries, planetarium shows, and for a variety of projects by individuals and journalists. 


# Acknowledgements
The authors would like to acknowledge the authors of the SPICE toolkit for continued 

# References