# SpiceyPy

| Continuous Integration | Code Coverage | Docs | Chat |              
|:----------------------:|:-------------:|:----:|:----:|  
| <a href="https://travis-ci.org/AndrewAnnex/SpiceyPy"><img alt="Travis Build Status" src="https://travis-ci.org/AndrewAnnex/SpiceyPy.svg?style=flat?branch=master"/></a> <a href="https://ci.appveyor.com/project/AndrewAnnex/spiceypy/"><img alt="Windows Build Status" src="https://ci.appveyor.com/api/projects/status/wly0q2cwy33ffura/branch/master?svg=true"/></a> | <a href="https://coveralls.io/r/AndrewAnnex/SpiceyPy?branch=master"><img alt="Coverage Status" src="https://img.shields.io/coveralls/AndrewAnnex/SpiceyPy.svg"/></a> | <a href="http://spiceypy.readthedocs.org"><img alt="Documentation Status" src="https://readthedocs.org/projects/spiceypy/badge/?version=master"/></a> | <a href="https://gitter.im/AndrewAnnex/SpiceyPy"><img alt="Join the chat at https://gitter.im/AndrewAnnex/SpiceyPy" src="https://badges.gitter.im/Join%20Chat.svg"/></a> |

SpiceyPy is a Python wrapper for the NAIF C SPICE Toolkit (N65), compatible with Python 2 and 3, written using ctypes.

### Introduction

The [SPICE Toolkit](http://naif.jpl.nasa.gov/naif/). 
In short it is an essential tool for scientists and engineers alike in the planetary science field for Solar System Geometry.   
Please visit the NAIF website for more details.

*IMPORTANT*: I have no current affiliation with NASA, NAIF, or JPL. The code is provided "as is", use at your own risk.
### Travis and Coveralls Status

A secondary list (non-maintained) of what functions have been wrapped can be found [here](https://github.com/AndrewAnnex/SpiceyPy/wiki/Wrapper-Completion).  
A majority of SPICE functions have written wrappers along with tests mainly derived from the CSPICE documentation.  
A small number of functions have no wrapper functions of any kind due to lack of necessity, they are labeled as "Skipped".   
The rest of the functions generally have written wrapper functions but remain untested, mostly due to lack of SPICE documentation (the EK kernel functions are one example of this).  
Functions that utilize call-backs have not been wrapped or tested yet, although ctypes does support call-backs so they will be revisited.  
If you encounter an error with a function please report it or write up a PR to fix it, with ctypes it is easy! 

### Documentation
 
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
- [x] Useful, but abbreviated commenting on functions.
- [x] Python 2 and 3 support.
- [x] Numpy Support.
- [ ] Enable vectorization of certain functions to be more like ICY.

### Installation
First install the dependencies (numpy, six, pytest). Then download the project, extract it, and inside just run `python setup.py install`.
If you are updating to the newest commit/version, be sure to completely delete the SpiceyPy folder in your site-packages.
This can most commonly be done by uninstalling SpiceyPy using pip.

### Known Working Environments:
SpicyPy is now compatible with modern Linux, Mac, and Windows environments. Since the package
is a wrapper, any environment not supported by the NAIF is similarly not supported by SpiceyPy.
Below is a list of known working environments. If you run into issues with your system please
submit an issue with details.

* Python 3.4.1 64-bit Mac OS X 10.10.4
* Python 3.3.3 64-bit Mac OS X 10.9.4
* Python 2.7.5 64-bit Mac OS X 10.9.4
* Python 3.3.3 64-bit Mac OS X 10.9.2
* Python 2.7.5 64-bit Mac OS X 10.9.2
* Python 3.2.3 64-bit Ubuntu 12.04 LTS (VM)
* _Python 3.4.3 64-bit Windows (Appveyor), using Visual Studio 2013_
* _Python 3.4.3 32-bit Windows (Appveyor), using Visual Studio 2013_
* _Python 2.7.9 64-bit Windows (Appveyor), using Visual Studio 2013_
* _Python 2.7.9 32-bit Windows (Appveyor), using Visual Studio 2013_

#### A Note About Windows Support
Windows support is currently highly experimental and difficult for the author to test locally.
If attempting to install on windows platforms, please ensure you have a recent version of Visual Studio is 
installed and ensure cl.exe and link.exe is available on the path. Given the variability of systems, 
I will not be able to diagnose most issues encountered with running SpiceyPy on Windows. Below is a 
semi-complete list of instructions for getting SpiceyPy built and installed. For a more complete
but less readable guide follow the appveyor.yml file included in this distribution.

1. Ensure Visual Studio is properly installed and that cl.exe and link.exe are available on the path.
  * If you run `cl` or `link` you should see some indication that you have done this correctly. 
2. Ensure you have pip, numpy, pytest, and six installed.
3. Call `vcvarsall.bat` from your visual studio with the option "amd64" for 64 bit builds (I have not tested 32bit yet)
4. Run `python setup.py install` to install SpiceyPy (this will take a few minutes.)
5. You are done! 
  * You can run tests by running py.test test, ensure the root directory of SpiceyPy does not have a lengthy path as the spice function furnsh fails with long absolute paths.

### Acknowledgements
[DaRasch](https://github.com/DaRasch) wrote spiceminer, which I looked at to get SpiceCells working, thanks!

#### Steps for making the shared library (now integrated into setup.py)
The below steps are now integrated into the setup.py file included and can be ignored, but for those who want to try for themselves I left the following sequences for you.

_First the user must generate their own shared library of CSPICE. In the Lib subdirectory in CSPICE run the following commands:_
```
ar -x cspice.a
ar -x csupport.a
```
_This will generate a large collection of `*.o` files.
Next compile the shared library, last I checked this was correct on my system._
```
gcc -shared -fPIC -lm *.o -o spice.so
```
