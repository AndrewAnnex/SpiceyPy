# Change Log   
All notable changes to SpiceyPy will be documented here

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project tries to adhere to [Semantic Versioning](http://semver.org/).

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
