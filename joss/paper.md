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
  - name: Ben Pearson
    affiliation: 2
  - name: Benoît Seignovert
    orcid: 0000-0001-6533-275X
    affiliation: 3
  - name: Brain T. Carcich
    orcid: 0000-0001-9211-6526
    affiliation: 4
  - name: Jesse A. Mapel
    orcid: 0000-0001-5756-0373
    affilitation: 5
  - name: Kristin L. Berry
    orcid: 0000-0001-9757-9706
    affilitation: 5
  - name: K.-Michael Aye
    orcid: 0000-0002-4088-1928
    affiliation: 6
  - name: Miguel de Val-Borro
    orcid: 0000-0002-0455-9384
    affiliation: 7
  - name: Shankar Kulumani
    orcid: 0000-0002-7822-0471
    affiliation: 8
affiliations:
 - name: The Johns Hopkins University, Baltimore, MD 21218, USA.
   index: 1
 - name: General Public.
   index: 2
 - name: Jet Propulsion Laboratory, California Institute of Technology, Pasadena, CA 91109, USA.
   index: 3
 - name: Latchmoor Services, LLC.
   index: 4
 - name: USGS Astrogeology Science Center, Flagstaff, AZ 86001, USA.
   index: 5
 - name: Laboratory for Atmospheric and Space Physics, University of Colorado, Boulder, CO 80303, USA.
   index: 6
 - name: Planetary Science Institute.
   index: 7
 - name: Collins Aerospace.
   index: 8

date: 10 January 2020
bibliography: paper.bib

---
# Statement of Need

Operating in space necessitates quantifying the positions, velocities, and other properties of spacecraft and planetary bodies through time.
Scientists and engineers working with robotic planetary spacecraft missions use the SPICE Toolkit[@acton:2018] to help plan observations
 and to quantify the positions of planetary bodies and spacecraft through time.
For example, SPICE can be used to predict future occultations of planets relative to a camera in a rover or spacecraft.
Scientists also use SPICE to analyze data returned by these missions and to plan hypothetical orbital trajectories for future missions.
The NAIF develops SPICE in FORTRAN77 (aka SPICELIB) translated to ANSI C (CSPICE), and provide Matlab (Mice) and IDL (Icy) wrappers; however
, as of 2014, they did not offer a Python interface.
The growth of Python and movement away from proprietary interpreted languages motivated the development of SpiceyPy so that planetary
 scientists and engineers can use SPICE with the SciPy Stack [@burrell:2018].

# Summary

``SpiceyPy`` is an open-source Python package that provides a ``pythonic`` interface to nearly all of the SPICE toolkit API N66 (CSPICE). 
``SpiceyPy`` was developed in Python using the ``ctypes`` module of the CPython standard library. 
Developing ``SpiceyPy`` in Python enabled simplified interaction with the underlying C API by utilizing idiomatic Python.
``SpiceyPy`` relies on the NumPy library for numeric arrays and tight integration with the SciPy stack.

``SpiceyPy`` is extensively tested using a combination of unit and integration tests, which run using continuous integration services. 
The tests also serve as code examples translated from the NAIF documentation.
Continuous deployment updates documentation and deploys artifacts of releases to PyPI and the conda-forge. Docstrings in SpiceyPy
contain links to the corresponding CSPICE documentation page hosted by the NAIF for additional details regarding the function.

``SpiceyPy`` enables scientists to utilize the full functionality of SPICE within Python and the ecosystem of visualization and data science packages available.
``SpiceyPy`` has been utilized in peer-reviewed research [@behar:2016; @behar:2017; @porter:2018; @zangari:2018; @attree:2019;], masters
 and doctoral theses [@hackett2019; @albin:2019], spacecraft mission operations, planetarium shows,
as a dependency in other python libraries [@heliopy], and for a variety of smaller projects.

# Acknowledgements
The authors would like to acknowledge the NAIF (Charles Acton et al.) for continued support for SpiceyPy on the NAIF websites and for their
*SpiceyPy translation* of their excelent "Hands-on" lessons. The first author also thanks all contributors and users who have asked for
 support relating to SpiceyPy that motivates further improvements to the package. 

# References