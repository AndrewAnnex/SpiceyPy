# SpiceyPy

The NAIF C SPICE Toolkit Wrapper for Python 3, written using ctypes.

*IMPORTANT* I have no current affiliation with NASA, NAIF, JPL. The code is provided as is, you shouldn't even think to use this for anything important until I get some fancy legal stuff written here. I think you get the gist.

### Introduction

The [SPICE Toolkit](http://naif.jpl.nasa.gov/naif/). In short it is an essential tool for scientists and engineers alike in the planetary science field.


### Design Goals
- [ ] Complete working coverage of all existing SPICE commands (No additional functionality or commands)
- [ ] Useful, but abbreviated commenting on functions.
- [ ] Python 2 and 3 support.
- [ ] Numpy integration?

### Important User Information
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