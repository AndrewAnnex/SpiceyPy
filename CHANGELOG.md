# Change Log   
All notable changes to SpiceyPy will be documented here

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project tries to adhere to [Semantic Versioning](http://semver.org/).

## [7.0.0] - 2025-09-22
SpiceyPy with Cyice, Cython accelerated Spice

### Added
- Cython extension submodule Cyice for accelerated SpiceyPy
- Cyice includes wrappers for over 90 CSPICE functions, vectorized for majority of functions, shares kernel pool with spiceypy so new functions are drop-in replacements
- Cyice functions tested and benchmarked against spiceypy ctypes wrapper functions
- new Cyice docs
- new required reading docs pages (#489)
- python 3.13 builds (#488) and native aarch64 runners (#490)

### Fixed
- Various issues and typos in docs (#503) (#492) (#350) (#481) (#477)
- Various CI improvements (#484) (#479)

### Changed
- Switched build system to scikit_build_core/cmake to simplify builds
- Pckcov returns “cover” arg (#504)
- URLs to naif are now versioned (#493)

### Removed
- Get_spice.py, setup.cfg, setup.py, and related old build system 


## [6.0.3] - 2025-07-17
Backport fix for spice cell functions

### Added
- Add assertions that passed-in SpiceCell is correct type for `bltfrm()`, `ckcov()`, `ckobj()`, `kplfrm()`, `spkobj()`

### Fixed
- Corrected bug where bool was used instead of is Null for specifying return SpiceCell in `bltfrm()`, `ckcov()`, `ckobj()`, `kplfrm()`, `spkobj()`
- fixed sdist publishing issue in ci publish workflow


## [6.0.2] - 2025-07-12
Backport fix to avoid numpy version change before v7.0.0 release
### Changed
- changed numpy version pin to be 'numpy>=1.23.5'


## [6.0.1] - 2025-06-24
Backport release of various small fixes and typo corrections
### Added
- python 3.13 builds
- missing exceptions from cspice #494
- new required readings docs #489

### Removed
- cirrus ci was removed
- gitter chat info

### Changed
- Added units to many parameter descriptions in function docstrings to address #350
- updated various aspects of ci builds
- copyright date ranges updated to 2025
- moved naif doc urls to versioned 

### Fixed
- various readthedocs and docs issues
- cylsph was fixed as it was calling the wrong cspice function #496
- various typos


## [6.0.0] - 2023-08-31
Fixed several major typos and fortran array ordering issues in tkfram, zzdynrot as well as failing tests on arm64 macos. 
### Added
- SpiceNOTENOUGHDATA2 exception #466
- Context manager for SPICE kernels #458
- CITATION.cff file
- DeprecationWarning for zzdynrot

### Changed
- tkfram_c now used in tkfram wrapper function
- updated setup.cfg
- type hints for sincpt to be more correct

### Deprecated
- python 3.6
- python 3.7

### Removed
- codecov as a dependency in dev

### Fixed
- fixed zzdynrot and tkfram return matrix element ordering
- typo in exceptions.rst #459
- fixed test test_sphlat
- fixed sphlat to use correct libspice function call
- fixed tests for dskx02, dskxsi, gfsntc for arm64 macos floating point issues #470
- fixed typo in test_oscelt and test_oscltx


## [5.1.2] - 2022-10-14
fix for exception error message toolkit version
### Fixed
- exceptions now use dynamic lookup of toolkit version for error messages


## [5.1.1] - 2022-07-30
fixes macOS arm64 cross compile
### Fixed
- updated get_spice.py to allow for arch override for macos arm64


## [5.1.0] - 2022-07-09
adds wrappers for the majority of new function in n67
### Added
- azlcpo
- azlrec
- chbigr
- chbint
- chbval
- ckfrot
- ckfxfm
- ckgr02
- ckgr03
- ckmeta
- cknr02
- cknr03
- dafhsf
- dasadc
- dasadd
- dasadi
- dashfs
- daslla
- dasllc
- dasonw
- dasops
- dasrdd
- dasrdi
- dasudd
- dasudi
- daswbr
- dazldr
- dlabns
- dlaens
- dlaopn
- dnearp
- drdazl
- ednmpt
- edpnt
- evsgp4
- getfvn
- hrmesp
- invstm
- lgresp
- lgrint
- qderiv
- recazl
- stlabx
- tagnpt
- tkfram
- tparch
- trgsep
- twovxf
- vprojg

### Fixed
- fixed docstring for frinfo
- fixed freebsd support in getspice


## [5.0.1] - 2022-03-23
minor update to make ld_library_path update safer
### Fixed
- override of ld_library_path is now temporary

### Changed
- updated copyrights for 2022

## [5.0.0] - 2022-02-17
### Changed
- switched to N67 CSPICE, no new wrapper functions yet
- removed deprecated named args mentioned in 4.0.1 release notes

### Removed
- deprecation warnings for params of mtxmg, mtxvg, mxm, mxmg, mxmt, mxmtg, mxvg, vtmvg, xposeg, unormg, vaddg, vdistg, vdotg, vequg, vhatg, vminug, vnromg, vrelg, vsclg, vsepg, vsubg, vzerog
- ncol/nrow params for: mtxmg, mtxvg, mxm, mxmg, mxmt, mxmtg, mxvg, vtmvg, xposeg
- ndim param for: unormg, vaddg, vdistg, vdotg, vequg, vhatg, vminug, vnromg, vrelg, vsclg, vsepg, vsubg, vzerog

## [4.0.3] - 2021-11-14
### Added
- changelog now rendered in docs
- runtime override of cspice via env var or ld_library_path
- pyproject.toml and setup.cfg
- CSPICE N66 patches from NAIF/conda-forge feedstock
- builds for aarch64 and macos arm64

### Changed
- switched to src layout
- switched "cspice.dll/.so" to "libcspice.dll/so"
- updated get_spice.py to build cspice from source
- moved most metadata to setup.cfg
- updated ci workflows to build wheels for major platforms using cibuildwheels
- updated install commands in docs to use pip instead of setup.py

## [4.0.2] - 2021-08-13
### Fixed
- getfat variables size #420
- safer cleanups in tests 

## [4.0.1] - 2021-05-31
### Added
- docs info about ARM support, currently limited to conda-forge spiceypy
- docs citation info/basic intro
- hash checksums for test kernels
- offline install ci tests 
- warn_deprecated_args function to aid future deprecations

### Deprecated
- added deprecation warnings for ncol/nrow params for: mtxmg, mtxvg, mxm, mxmg, mxmt, mxmtg, mxvg, vtmvg, xposeg pending next major release.
- added deprecation warnings for ndim param for: unormg, vaddg, vdistg, vdotg, vequg, vhatg, vminug, vnromg, vrelg, vsclg, vsepg, vsubg, vzerog pending next major release.    

### Changed
- copyright year
- a number of typehints to accept np.ndarray
- changed test_wrapper to use a pytest autouse fixture to call reset/kclear automatically for most tests

### Fixed
- missing docs for xf2eul
- numpy bool_ deprecation warnings
- numpy float warning
- type hint for appndd

## [4.0.0] - 2020-12-07
### Added
- bodeul

### Changed
- main branch is now the default branch
- switched to use 'fromisoformat' in datetime2et

### Fixed
- fixed nintvls spelling inconsistency 

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
