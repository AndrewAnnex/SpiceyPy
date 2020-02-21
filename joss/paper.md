---
title: 'SpiceyPy: a Pythonic Wrapper for the SPICE Toolkit'
tags:
  - Python
  - SPICE
  - ephemeris
  - geometry
  - navigation
  - spacecraft
  - planets
authors:
  - name: Andrew M. Annex
    orcid: 0000-0002-0253-2313
    affiliation: 1
  - name: Ben Pearson
    affiliation: 2
  - name: Benoît Seignovert
    orcid: 0000-0001-6533-275X
    affiliation: 3
  - name: Brian T. Carcich
    orcid: 0000-0001-9211-6526
    affiliation: 4
  - name: Helge Eichhorn
    orcid: 0000-0003-0303-5199
    affiliation: 5
  - name: Jesse A. Mapel
    orcid: 0000-0001-5756-0373
    affiliation: 6
  - name: Johan L. Freiherr von Forstner
    orcid: 0000-0002-1390-4776
    affiliation: 7
  - name: Jonathan McAuliffe
    affiliation: 8
  - name: Jorge Diaz del Rio
    affiliation: 9
  - name: Kristin L. Berry
    orcid: 0000-0001-9757-9706
    affiliation: 6
  - name: K.-Michael Aye
    orcid: 0000-0002-4088-1928
    affiliation: 10
  - name: Marcel Stefko
    orcid: 0000-0002-7736-2611
    affiliation: 11
  - name: Miguel de Val-Borro
    orcid: 0000-0002-0455-9384
    affiliation: 12
  - name: Shankar Kulumani
    orcid: 0000-0002-7822-0471
    affiliation: 13
  - name: Shin-ya Murakami
    orcid: 0000-0002-7137-4849
    affiliation: 14
affiliations:
 - name: Johns Hopkins University
   index: 1
 - name: None
   index: 2
 - name: Jet Propulsion Laboratory, California Institute of Technology
   index: 3
 - name: Latchmoor Services, LLC
   index: 4
 - name: Planetary Transportation Systems GmbH
   index: 5
 - name: USGS Astrogeology Science Center
   index: 6
 - name: Institute of Experimental and Applied Physics, University of Kiel
   index: 7
 - name: DLR Gesellschaft für Raumfahrtanwendungen (GfR) mbH
   index: 8
 - name: ODC Space
   index: 9
 - name: Laboratory for Atmospheric and Space Physics, University of Colorado
   index: 10
 - name: ETH Zurich
   index: 11
 - name: Planetary Science Institute
   index: 12
 - name: Collins Aerospace
   index: 13
 - name: GFD Dennou Club
   index: 14

date: 23 January 2020
bibliography: paper.bib

---
# Statement of Need

Operating in space necessitates quantifying the positions, velocities, geometries, and other properties of spacecraft and planetary
 bodies through time. 
Scientists and engineers working with robotic planetary spacecraft missions use the Spacecraft, Planet, Instrument, Camera-matrix, Events
 (SPICE) Toolkit [@acton:2018] to help plan observations and to quantify the positions of planetary bodies and spacecraft through time. 
SPICE is developed at the Jet Propulsion Laboratory by NASA's Navigation and Ancillary Information Facility (NAIF). Scientists also use
 SPICE to analyze data returned by these missions and to plan hypothetical orbital trajectories for future missions [@acton:2018]. 
For example, SPICE can calculate future occultations of planets relative to a camera on a rover or spacecraft. 
The NAIF provides SPICE in Fortran 77, C, and they also provide Matlab and IDL wrappers; however, as of 2014, they did not offer a Python
 interface. 
The growth of Python and movement away from proprietary interpreted languages [@burrell:2018] motivated the development of SpiceyPy so
 that planetary scientists and engineers can use SPICE within Python. 

# Summary

``SpiceyPy`` is an open-source, MIT licensed Python package that provides a ``pythonic`` interface to nearly all of the C SPICE toolkit N66. 
``SpiceyPy`` was developed in Python using the ``ctypes`` module of the CPython standard library to wrap the underlying C SPICE shared library. 
Developing ``SpiceyPy`` in Python enabled the SpiceyPy API to expose simplified and more ``pythonic`` interactions with the underlying C API for SPICE.
``SpiceyPy`` relies on the NumPy library for numeric arrays and tight integration with the SciPy stack.

``SpiceyPy`` is extensively tested using a combination of unit and integration tests, which run using continuous integration services. 
The tests also serve as code examples translated from the NAIF documentation. 
Continuous deployment updates documentation and deploys artifacts of releases to PyPI and the conda-forge. 
Every SPICE function wrapper in SpiceyPy contains docstrings that provide short descriptions of the function duplicated from the SPICE
 documentation. 
Docstrings in SpiceyPy also contain links to the corresponding CSPICE documentation page hosted by the NAIF to provide additional details
 regarding the function. 

``SpiceyPy`` enables scientists to utilize the full functionality of SPICE within Python and the ecosystem of visualization and
 scientific packages available. 
``SpiceyPy`` has been utilized in peer-reviewed research [@behar:2016; @behar:2017; @porter:2018; @zangari:2018; @attree:2019], masters
 and doctoral theses [@hackett:2019; @albin:2019], spacecraft mission operations, as a dependency in other Python libraries [@heliopy:2019
 ], and for a variety of other projects [@wilson:2016; @wilson_times:2017; @costa:2018]. 

# Acknowledgements
The authors would like to acknowledge members of the NAIF (Charles Acton, Ed Wright, Boris Semenov, Nat Bachman) for continued support for
 SpiceyPy and for providing to users a *SpiceyPy translation* of their excellent "Hands-on" lessons. 
The first author also thanks all of the contributors and users of SpiceyPy; they motivate further improvements to the project. 
Co-authors other than the first author are ordered solely alphabetically by their first name. 

# References
