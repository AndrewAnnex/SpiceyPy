# SpiceyPy

The NAIF C SPICE Toolkit Wrapper for Python 3, written using ctypes.

*IMPORTANT*: I have no current affiliation with NASA, NAIF, or JPL. The code is provided as is, you shouldn't even think to use this for any production code until I get some fancy legal stuff written here. I think you get the gist.

### Introduction

The [SPICE Toolkit](http://naif.jpl.nasa.gov/naif/). In short it is an essential tool for scientists and engineers alike in the planetary science field.

### Completion

A growing list of completed functions can be found [here](https://github.com/Apollo117/SpiceyPy/wiki/Wrapper-Completion).
Functions that have written functions that have not been tested do generally work, but tests have not been written yet.

### Design Goals
- [ ] Complete working coverage of all existing CSPICE commands (No additional functionality or commands)
- [ ] Useful, but abbreviated commenting on functions.
- [ ] Make vectorized versions of certain functions to be more like ICY.
- [ ] Python 2 and 3 support.
- [ ] Numpy integration?

### Important User Information
*UPDATE* A very primative setup.py file exists and should get the shared library generated for you and placed in your site-packages directory. Be sure to completely delete the resulting folder in your site-packages folder if you are uninstalling the library or upgrading to a new version

*This is only known to work on OS X 10.9.2 with Python 3.3. Making the library work with Python 2.7 should be rather trivial and will happen eventually.*

*Unknown if this works at all in linux environments (Ubuntu, etc).*

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

