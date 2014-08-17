# SpiceyPy

The now mostly complete NAIF C SPICE Toolkit Wrapper for Python 2 and 3, written using ctypes.

*IMPORTANT*: I have no current affiliation with NASA, NAIF, or JPL. The code is provided "as is", use at your own risk.
### Introduction

The [SPICE Toolkit](http://naif.jpl.nasa.gov/naif/). In short it is an essential tool for scientists and engineers alike in the planetary science field for Solar System Geometry. Please visit the NAIF website listed earlier for more details.


### Travis and Coveralls Status

[![Build Status](https://travis-ci.org/Apollo117/SpiceyPy.svg?style=flat?branch=master)](https://travis-ci.org/Apollo117/SpiceyPy)
[![Coverage Status](https://img.shields.io/coveralls/Apollo117/SpiceyPy.svg?style=flat)](https://coveralls.io/r/Apollo117/SpiceyPy?branch=master)
A secondary list (non-maintained) can be found [here](https://github.com/Apollo117/SpiceyPy/wiki/Wrapper-Completion).
Functions that have written functions that have not been tested do generally work, but tests may not have been written yet.
Functions labeled with 'Skip' are being ignored, as they are either not needed in a python environment or impossible to implement.
If you encounter an error with a function please report it or write up a PR to fix it, with ctypes it is easy!

### Design Goals
- [ ] Majorly complete coverage of all existing CSPICE commands, within reason.
- [ ] Useful, but abbreviated commenting on functions.
- [ ] Enable vectorization of certain functions to be more like ICY.
- [x] Python 2 and 3 support.
- [x] Numpy Support.

### Installation
First install the dependencies (numpy, six, pytest). Then download the project, extract it, and inside just run `python setup.py install`.
If you are updating to the newest commit/version, be sure to completely delete the SpiceyPy folder in your site-packages.

### Known Working Environments:
These are the following OS environments I have been able to run the exampleProgramTest.py program on. SpiceyPy is being developed
in the Python 3.3.3 64-bit Mac OS X 10.9.4 environment. Travis CI is also ubuntu 12.04 LTS to my knowledge.
* Python 3.3.3 64-bit Mac OS X 10.9.4
* Python 2.7.5 64-bit Mac OS X 10.9.4
* Python 3.3.3 64-bit Mac OS X 10.9.2
* Python 2.7.5 64-bit Mac OS X 10.9.2
* Python 3.2.3 64-bit Ubuntu 12.04 LTS (VM)

### Acknowledgements
[DaRasch](https://github.com/DaRasch) wrote spiceminer, which I looked at to get SpiceCells working, thanks!

### Steps for making the shared library
The below steps are now integrated into the setup.py file included, but for those who want to try for themselves I left the following sequences for you.

First the user must generate their own shared library of CSPICE. In the Lib subdirectory in CSPICE run the following commands:
```
ar -x cspice.a
ar -x csupport.a
```
This will generate a large collection of `*.o` files.
Next compile the shared library, last I checked this was correct on my system.
```
gcc -shared -fPIC -lm *.o -o spice.so
```
