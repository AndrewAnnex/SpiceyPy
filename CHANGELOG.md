# Change Log   
All notable changes to SpiceyPy will be documented here

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project tries to adhere to [Semantic Versioning](http://semver.org/).

## [3.1.2] - 2020-09-??
### Changed
- main branch is now the default branch

## [3.1.1] - 2020-05-25
### Fixed
- missing get_spice.py in manifest

## [3.1.0] - 2020-05-25
### Added
- added irfnam, irfnum, irfrot, irftrn
- added kpsolv, kepleq
- better exceptions, many hundred spice toolkit defined exceptions
- copy button to docs codeblocks
- added CSPICE_SRC_DRI envvar override to specify cspice src directory during install
- added CSPICE_SHARED_LIB envvar override to specify cspice.so/.dll/.dylib during install

### Changed
- switch to codecov for code coverage
- various support type changes
- renamed getspice.py to get_spice.py

### Fixed
- fixed missing doc strings for callbacks

### Removed
- coveralls
- test cmd class in setup.py
- direct references to deprecated numpy matrix class

## [3.0.2] - 2020-02-19
### Added
- et2datetime function
- funding.yml

### Changed
- changed http to https in docs/docstrings

### Fixed
- many small issues with the docs
- author name in joss paper
- fixing SyntaxWarning in python 3.8
- year in docs
- issue with urllib usage in gettestkernels

## [3.0.1] - 2020-01-10
### Changed
- removed old logic from getspice for old openssl versions

### Removed
- import of six in getspice

## [3.0.0] - 2020-01-09
### Added
- Python 3.8 support

### Changed
- using black for code linting
- now using type hints 
- vectorized functions now return numpy arrays instead of lists of arrays

### Deprecated
- python 3.5 
- python 2.7

## [2.3.2] - 2019-12-19
### Added
- wrapper for ev2lin
- numpy string support

### Fixed
- some equality checks

### Changed
- updated MANIFEST.in to include test code
- vectorization of et2utc 
- vectorization of scencd
- vectroization of sc2e

## [2.3.1] - 2019-10-18
### Changed
- updated MANIFEST.in to include test code 

## [2.3.0] - 2019-09-25
### Added
- wrapper for tkfram
- wrapper for ckfrot
- wrapper for zzdynrot

### Fixed
- issue with dafgda absolute value problem, see issue #302

## [2.2.1] - 2019-08-19
### Changed
- set numpy version to 1.16.4 for python 2
- other dependency changes to setup.py and requirements.txt

### Fixed
- typo in a unit test fixed

## [2.2.0] - 2019-02-24
### Added
- gfevnt wrapper
- easier spice cell inits
- python datetime to et converter
- issue template
- code of conduct
- NAIF python lessons to docs

### Changed
- functions that modify a results spicecell now optionally create a return spicecell
- convrt now "vectorized"
- prioritized citation info in readme

### Removed
- removed anaconda build steps from appveyor, conda-fordge replaces it 

### Fixed
- newlines in changelog

## [2.1.2] - 2018-08-17
### Added
- python 3.7 builds on travis / appveyor

### Changed
- numpy to ctypes and back conversions improved

### Removed
- a few bool related internal things in support_types
- conda builds on appveyor removed in favor of conda-forge distribution of spiceypy

### Fixed
- issues relating to c_bool usage. everything is now c_int

## [2.1.1] - 2018-04-24
### Added
- wrapper functions for gffove and gfocce and associated callbacks
- proxymanager for spice download by B. Seignovert

### Changed
- simplifications in libspicehelper

### Fixed
- issue with cassini example in doc
- termpt docstring by Marcel Stefko
- various things in ci build configs
- missing dll/so file issue with pip installs

## [2.1.0] - 2017-11-09
### Added
- Completed wrapping of all new N66 DSK functions
- 3.6 classifier
- context manager for turning on/off found flag catches
- contributor guide
- freebsd support
- added tests for dozens of functions, wrapped almost all remaining functions

### Fixed
- added six and numpy to setup_requires setup.py kwargs
- bugs in some tests

### Changed
- changed naming of vectorToList to cVectorToPython
- Updated getspice module to use urllib3 for OpenSSL library versions older
  than OpenSSL 1.0.1g.
- getspice module provides now a class that handles the downloading and
  unpacking of N066 CSPICE distribution.
- Updated setup to pack the CSPICE installation code into a class that
  extends the setuptools.command.install command.
- made vectorized functions more consistent
- changed tests to point to smaller kernel set hosted on github

## [2.0.0] - 2017-06-09
### Added
- Implemented most of the new functions from N66 SPICE
- IntMatrixType support type
- SpiceDLADescr struct

### Changed
- now backing N66 CSPICE
- now builds 2.7, 3.4, 3.5, 3.6

### Deprecated
- 32 bit builds

### Fixed
- toPythonString now strips whitespace

## [1.1.1] - 2017-04-23
### Added
- added python3.6 builds

### Fixed
- fixed formatting on changelog
- fixed issues with rtd builds

### Changed
- version updated
- converted all downloads to use https

## [1.1.0] - 2016-10-19   
### Added    
- wrapper functions and tests for fovray, fovtrg, pxfrm2, occult #158
- wrapper functions and tests for spklef, spkopa, spkpds, spksub, spkuds, spkuef #155
- tests for srxpt and sincpt #154
- a bunch of other tests for CK related functions
- example added to docs
- automated artifact deployments (mostly) to pypi and conda cloud

### Fixed   
- improved use of six api to have better spicecells

### Changed   
- Start versioning based on the current English version at 0.3.0 to help
- refactored tests to be cleaner with kernel files
- fixed spice toolkit version to N65 pending new toolkit release.

## [1.0.0] - 2016-03-27  
### Added  
- DOI citation information

### Changed  
- updated versions for pytest, coverage, coveralls
- README updates

## [0.7.0] - 2016-03-26  
### Added  
- python wheel builds in appveyor #117
- wrapper for gfilum function

### Changed  
- converted README to rst format

### Fixed  
- inconsistencies in doc strings #143
- issue #136

## [0.6.8] - 2016-03-07
Got to a semi complete api here, lots of commits
before things so this version can be considered a bit of a baseline

### Added
- many things

### Changed
- the game

### Deprecated
- nothing important

### Removed
- what had to go

### Fixed
- it
