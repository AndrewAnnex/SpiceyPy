# SpiceyPy

[![Join the chat at https://gitter.im/AndrewAnnex/SpiceyPy](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/AndrewAnnex/SpiceyPy?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

A wrapper for the NAIF C SPICE Toolkit (N65), compatible with Python 2 and 3, written using ctypes.

*IMPORTANT*: I have no current affiliation with NASA, NAIF, or JPL. The code is provided "as is", use at your own risk.
### Introduction

The [SPICE Toolkit](http://naif.jpl.nasa.gov/naif/). 
In short it is an essential tool for scientists and engineers alike in the planetary science field for Solar System Geometry.   
Please visit the NAIF website listed earlier for more details.


### Travis and Coveralls Status

[![Build Status](https://travis-ci.org/AndrewAnnex/SpiceyPy.svg?style=flat?branch=master)](https://travis-ci.org/AndrewAnnex/SpiceyPy)
[![Coverage Status](https://img.shields.io/coveralls/AndrewAnnex/SpiceyPy.svg)](https://coveralls.io/r/AndrewAnnex/SpiceyPy?branch=master) 
A secondary list (non-maintained) of what functions have been wrapped can be found [here](https://github.com/AndrewAnnex/SpiceyPy/wiki/Wrapper-Completion).  
A majority of SPICE functions have written wrappers along with tests mainly derived from the CSPICE documentation.  
A small number of functions have no wrapper functions of any kind due to lack of necessity, they are labeled as "Skipped".   
The rest of the functions generally have written wrapper functions but remain untested, mostly due to lack of SPICE documentation (the EK kernel functions are one example of this).  
Functions that utilize call-backs have not been wrapped or tested yet, although ctypes does support call-backs so they will be revisited.  
If you encounter an error with a function please report it or write up a PR to fix it, with ctypes it is easy! 

### Documentation
 
[![Documentation Status](https://readthedocs.org/projects/spiceypy/badge/?version=master)](https://readthedocs.org/projects/spiceypy/?badge=master) 
 
**The SpiceyPy docs are available at: [spiceypy.readthedocs.org](http://spiceypy.readthedocs.org).**
 
The documentation for SpiceyPy is intentionally abridged so as to utilize the excellent [documentation provided by the NAIF.](http://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/index.html)  
Please refer to C and IDL documentation available on the NAIF website for in-depth explanations. 
Each function has a link to the corresponding C function in the NAIF docs at a minimum.
 
### How to Help

Feedback is always welcomed, if you discover that a function is not working as expected, submit an issue detailing how  
to reproduce the problem. If you utilize SpiceyPy frequently please consider contributing to the project by:  
writing a test, writing a wrapper, doing some code review, adding documentation, improving infrastructure code (like setup.py), or by spreading the word.  
Any changes can be easily shared by submitting a pull request.

### Citing SpiceyPy

If SpiceyPy helps lead to a scientific publication, please consider citing the SPICE toolkit, and listing SpiceyPy in the acknowledgments.  
The citation information for SPICE can be found on the NAIF website and please contact the author of this git repository for further information regarding SpiceyPy itself.

### Design Goals
- [x] Majorly complete coverage of all existing CSPICE commands, within reason.
- [ ] Useful, but abbreviated commenting on functions.
- [ ] Enable vectorization of certain functions to be more like ICY.
- [x] Python 2 and 3 support.
- [x] Numpy Support.

### Installation
First install the dependencies (numpy, six, pytest). Then download the project, extract it, and inside just run `python setup.py install`.
If you are updating to the newest commit/version, be sure to completely delete the SpiceyPy folder in your site-packages.
This can most commonly be done by uninstalling SpiceyPy using pip.

### Known Working Environments:
These are the following OS environments I have been able to run the exampleProgramTest.py program on. SpiceyPy is being developed
in a Python 3.4.1 64-bit Mac OS X 10.9.5 environment. Travis CI is also ubuntu 12.04 LTS to my knowledge.
* Python 3.3.3 64-bit Mac OS X 10.9.4
* Python 2.7.5 64-bit Mac OS X 10.9.4
* Python 3.3.3 64-bit Mac OS X 10.9.2
* Python 2.7.5 64-bit Mac OS X 10.9.2
* Python 3.2.3 64-bit Ubuntu 12.04 LTS (VM)

### Acknowledgements
[DaRasch](https://github.com/DaRasch) wrote spiceminer, which I looked at to get SpiceCells working, thanks!

### Steps for making the shared library
The below steps are now integrated into the setup.py file included and can be ignored, but for those who want to try for themselves I left the following sequences for you.

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
