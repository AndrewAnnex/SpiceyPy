# SpiceyPy

The NAIF SPICE Toolkit written in pure Python* 

*almost, or eventually the goal is to use only the standard library, but numpy for now I think is needed to save time.

*IMPORTANT* I have no current affiliation with NASA, NAIF, JPL. The code is provided as is, you shouldn't even think to use this for anything important until I get some fancy legal stuff written here. I think you get the gist.

### Introduction

The [SPICE Toolkit](http://naif.jpl.nasa.gov/naif/) is detailed here, possibly I will write my own intro to it here. But in short it is an essential tool for scientists and engineers alike in the planetary science field. 

### Why?

Python is a greatly popular and readable language, and it is now becoming popular with planetary science and astronomy researchers due to shortcomings in more conventional (to that field) environments (such as IDL or MATLAB). Current python wrappers (PySPICE) do not provide access to certain important functions that make spice useful to the author of this readme. Currently the NAIF has no plans to extend SPICE to Python, at least as far as I know. The eventual goal is to have the entire spice library written in Python, with compatibility with 2.X and 3.X. Additionally, it is I think important to reduce or eliminate dependencies with other extensions, but for now Numpy will be used to speed things along.  

In addition, the author had a interest in learning more about SPICE for his own benefit.

_If you have a bit of time on your hands and a understanding of SPICE (particularly the low level code for accessing binary kernels), please help and contribute to this project!_


### Design Goals
- [ ] Complete working coverage of all existing SPICE commands (No additional functionality or commands)
- [ ] Useful, but abbreviated commenting on functions.
- [ ] Useful wrapper objects for spice objects, to make spice more OO for users new to it
- [ ] Reduced dependencies to commonly used extensions (Numpy)

_or:_

- [ ] Completely Pure Python code, no external libraries.

The idea for this project is to replicate the SPICE library as closely as possible to aid users transitioning code.

