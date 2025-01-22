=========================
C-Kernel Required Reading
=========================

This required reading document is reproduced from the original NAIF
document available at `https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/ck.html <https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/ck.html>`_ 
                                                                      
Abstract                                                  
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| The C-kernel (CK) system is the component of SPICE concerned with   
  attitude of spacecraft structures or instruments.                   
                                            
                                                                      
References                                                
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| All references are to NAIF documents. The notation [Dn] refers to   
  NAIF document number.                                               
                                                                      
#. [167] Double Precision Array Files Required Reading 
    (`daf.req <../req/daf.html>`__)                                     
                                                                      
#. [349] FRAMES Required Reading                                
    (`frames.req <../req/frames.html>`__).                              
                                                                      
#. [222] Spacecraft Clock Time Required Reading                 
    (`sclk.req <../req/sclk.html>`__)                                   
                                                                      
#. [214] Rotations Required Reading                             
    (`rotation.req <../req/rotation.html>`__)                           
                                                                      
#. [211] SPC Required Reading: Comments in SPK and CK Files     
    (`spc.req <../req/spc.html>`__)                                     
                                                                      
                                                
                                                                      
DAF Run-Time Binary File Format Translation               
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| Starting with the N0052 release of the SPICE Toolkit (January,      
  1)    certain supported platforms are able to read DAF-based binary 
  files (SPK, CK and binary PCK) that were written using a different, 
  or non-native, binary representation. This access is read-only; any 
  operations requiring writing to the file (adding information to the 
  comment area, or appending additional ephemeris data, for example)  
  require prior conversion of the file to the native binary file      
  format. See the Convert User's Guide,                               
  `convert.ug <../ug/convert.html>`__, for details.                   
                                            
                                                                      
Detection of Non-native Text Files                        
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| Starting with the N0057 release of the SPICE Toolkit (March, 2004)  
  the SPICE data loading mechanism detects and prohibits loading text 
  kernel files containing lines terminated with EOF character(s)      
  non-native to the platform on which the Toolkit was compiled. If a  
  non-native EOL terminator is detected in the first 132 characters   
  of a text kernel, the execution is stopped and an error message is  
  displayed. This feature does not work with files that are smaller   
  that 132 bytes or have the first line longer that 132 characters.   
                                            
                                                                      
Introduction                                              
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| In the SPICE system, pointing data for science instruments are      
  stored in the C-kernel, the \``C'' in SPICE. The pointing of an     
  instrument is often expressed in terms of a transformation matrix   
  from some standard base reference frame to a local,                 
  instrument-fixed frame. In the past, the instrument was often a     
  camera, and the transformation was thus dubbed the \``C-matrix'';   
  hence the choice of C as the name for the pointing kernel.          
                                                                      
The data contained in C-kernel files can be accessed and manipulated  
by a collection of ANSI C functions which are part of the CSPICE      
library. These functions can be integrated into user application      
programs. The purpose of this document is to describe both the        
C-kernel file structure and the associated CSPICE software to the     
level of detail necessary for the user to program almost any          
application.                                                          
                                                                      
With few exceptions, all functions appearing in this document are     
part of CSPICE or the standard ANSI C library. The exceptions are     
placeholders for user-supplied functions which appear in some of the  
code examples. Each CSPICE function is prefaced with a complete       
CSPICE header which describes inputs, outputs, restrictions and       
context, and provides examples of usage. The authoritative            
documentation for any function is its header, which should be         
consulted before using the function in any program. A summary of the  
CK functions presented in this document is included as Appendix A.    
                                            
                                                                      
Preliminaries                                             
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| In this chapter we discuss four concepts that are essential to      
  using the C-kernel: specification of spacecraft and instruments,    
  C-matrices, angular velocity vectors, and spacecraft clock time.    
                                            
                                                                      
Specifying Spacecraft and Instruments                     
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| C-kernel files and software use integer codes to refer to           
  instruments and the spacecraft on which they are mounted. You will  
  use these instrument numbers with C-kernel readers to request       
  pointing data.                                                      
                                                                      
In order to avoid confusion, NAIF, in cooperation with the science    
teams from each flight project, will assign instrument codes using    
the following scheme.                                                 
                                                                      
If you're familiar with SPICE S- and P-kernels, you know that NAIF    
codes for spacecraft are negative integers: -31 for Voyager 1, -32    
for Voyager 2, -94 for Mars Global Surveyor, and so on. We borrow     
from this convention in defining instrument codes.                    
                                                                      
For example, the Voyager 2 instruments could have been given these    
IDs:                                                                  
                                                                      
**-32000**                                                            
   Instrument Scan Platform                                           
                                                                      
**-32001**                                                            
   ISSNA (Imaging science narrow angle camera)                        
                                                                      
**-32002**                                                            
   ISSWA (Imaging science wide angle camera)                          
                                                                      
**-32003**                                                            
   PPS (Photopolarimeter)                                             
                                                                      
**-32004**                                                            
   UVSAG (Ultraviolet Spectrometer, Airglow port)                     
                                                                      
**-32005**                                                            
   UVSOCC (Ultraviolet Spectrometer, Occultation port)                
                                                                      
**-32006**                                                            
   IRIS (Infrared Interferometer Spectrometer and Radiometer)         
                                                                      
The simple coding formula is                                          
::                                                                    
                                                                      
                                                                      
    SPICE s/c instrument code = (s/c code)*(1000) - instrument number 
                                                                      
which allows for 999 instruments on board any one spacecraft.         
The term \``instrument'' is used loosely throughout this document     
since the concept of orientation is applicable to structures other    
than just science instruments. For example, some of the Galileo       
instruments are in a fixed position relative to the scan platform. It 
might therefore be prudent to have a single file containing the       
orientation of the scan platform, and then produce the pointing for   
each of the scan platform science instruments by applying instrument  
offset angles obtained from the I-kernel.                             
                                            
                                                                      
C-Matrices                                                
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| A C-matrix is a 3x3 matrix that transforms Cartesian coordinates    
  referenced to a \``base frame'' to coordinates in an                
  instrument-fixed reference frame. In earlier versions of CSPICE,    
  the base frame was required to be inertial; this restriction has    
  been removed.                                                       
                                                                      
The C-matrix transforms coordinates as follows: if a vector v has     
coordinates ( x, y, z ) in some base reference frame (like J2000),    
then v has coordinates ( x', y', z' ) in instrument-fixed             
coordinates, where                                                    
                                                                      
::                                                                    
                                                                      
                                                                      
      [          ] [ x ]     [ x']                                    
      | C-matrix | | y |  =  | y'|                                    
      [          ] [ z ]     [ z']                                    
                                                                      
                                                                      
The transpose of a C-matrix rotates vectors from the instrument-fixed 
frame to the base frame:                                              
::                                                                    
                                                                      
                                                                      
      [          ]T [ x']     [ x ]                                   
      | C-matrix |  | y'|  =  | y |                                   
      [          ]  [ z']     [ z ]                                   
                                                                      
                                                                      
Therefore, if the coordinates of an instrument in the instrument      
fixed frame are known, then the transpose of the C-matrix can be used 
to determine the corresponding coordinates in a base reference frame. 
This information can be used to help answer questions such as,        
\``What is the latitude and longitude of the point on the planet that 
the camera was pointing at when it shuttered this picture?''          
The high-level CK file reader `ckgp_c <../cspice/ckgp_c.html>`__ (    
Get Pointing ) returns a C-matrix that specifies the pointing of a    
spacecraft structure at a particular time. An example program is      
included in Appendix B, which solves the longitude and latitude       
problem presented above using `ckgp_c <../cspice/ckgp_c.html>`__ and  
other CSPICE functions.                                               
                                            
                                                                      
Angular Velocity Vectors                                  
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| In the C-kernel an angular velocity vector is a vector with respect 
  to a base frame whose direction gives the right-handed axis about   
  which an instrument-fixed reference frame is rotating, and whose    
  magnitude is equal to the magnitude of the rotation velocity, in    
  radians per second.                                                 
                                                                      
Angular rate information may be important for certain types of        
science analysis. For instance, investigators for imaging instruments 
might use angular rates to determine how much smear to expect in      
their images.                                                         
                                                                      
CK files are capable of storing angular velocity data for             
instruments, although the presence of such data is optional. The CK   
reader :py:meth:`~spiceypy.spiceypy.ckgpav` (Get Pointing and       
Angular Velocity) returns an angular velocity vector in addition to a 
C-matrix.                                                             
                                            
                                                                      
Spacecraft Clock Time                                     
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| Each piece of data within the C-kernel is associated with a         
  spacecraft clock time (SCLK). This is because the spacecraft clock  
  time is typically appended to the telemetry data that is the source 
  for pointing information.                                           
                                                                      
Within the SPICE system, SCLK is represented as an encoded double     
precision number. You will need this form when using CK reader        
functions to read from CK files.                                      
                                                                      
CSPICE includes functions to convert between character SCLK format    
and the double precision encoding. There are also functions to        
convert between SCLK and standard time systems such as ET and UTC.    
                                                                      
The SCLK Required Reading, `sclk.req <../req/sclk.html>`__, contains  
a full description of SCLK including the clock formats for individual 
spacecraft. You should read that document before writing any C-kernel 
programs. A brief description of SCLK is included here because many   
of the functions presented require a clock time as an input argument. 
                                            
                                                                      
Encoded SCLK                                              
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| Encoded SCLK values may be discrete or continuous.                  
                                                                      
Discrete encoded SCLK values have units of \``ticks''; ticks          
represent the least significant counts representable by a clock.      
Continuous encoded SCLK supports non-integral tick values. This       
enables translation of other time systems to encoded SCLK without     
rounding.                                                             
                                                                      
Throughout this document, encoded SCLK should be assumed to be        
continuous unless otherwise specified.                                
                                                                      
To convert from a character string representation of SCLK to its      
double precision encoding, use the function                           
:py:meth:`~spiceypy.spiceypy.scencd` (Encode SCLK):                 
                                                                      
::                                                                    
                                                                      
      scencd_c ( sc, sclkch, &sclkdp );                               
                                                                      
Use :py:meth:`~spiceypy.spiceypy.scdecd` (Decode SCLK) to recover   
the character representation from its double precision encoding.      
::                                                                    
                                                                      
      scdecd_c ( sc, sclkdp, lenout, sclkch );                        
                                                                      
The first argument to both functions, \`sc', is the NAIF integer ID   
for the spacecraft whose clock count is being encoded or decoded (for 
example, -77 for Galileo).                                            
Above, the argument \`lenout' is used by the caller to indicate the   
available space in the output string.                                 
                                                                      
Each spacecraft may have a different format for its clock counts, so  
the encoding scheme may be different for each. The SCLK Required      
Reading, `sclk.req <../req/sclk.html>`__, indicates the expected      
clock string formats for each mission.                                
                                                                      
To convert from ET to continuous encoded SCLK, use                    
:py:meth:`~spiceypy.spiceypy.sce2c` (ET to continuous SCLK):         
                                                                      
::                                                                    
                                                                      
      sce2c_c ( sc, sclkch, &sclkdp );                                
                                                                      
To convert continuous encoded SCLK to ET, use                         
:py:meth:`~spiceypy.spiceypy.sct2e` (Ticks to ET):                   
::                                                                    
                                                                      
      sct2e_c ( sc, sclkdp, &et );                                    
                                                                      
                                                
                                                                      
Ticks and Partitions                                      
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| The units of encoded SCLK are \``ticks since clock start at         
  launch,'' where a \``tick'' is defined to be the shortest time      
  increment expressible by a particular spacecraft clock.             
                                                                      
The problem of encoding SCLK is complicated by the fact that          
spacecraft clocks do not always advance continuously. A discontinuity 
may occur if a clock resets to a different value. This occurs when a  
clock reaches its maximum value, but it can also happen due to other  
reasons which will not be discussed here. Anytime this occurs, we say 
that the clock has entered a new \``partition.''                      
                                                                      
SCLK strings should normally include a partition number prefixed to   
the rest of the clock count with a \``/''. The partition number       
uniquely separates a count from identical counts in other partitions. 
                                                                      
The presence of the partition number is not required. If it is        
missing, :py:meth:`~spiceypy.spiceypy.scencd` will assume the       
partition to be the earliest possible one containing the clock        
string.                                                               
                                            
                                                                      
SCLK and other time systems                               
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| CSPICE contains functions that convert between both the encoded and 
  character form of spacecraft clock time and two other time systems. 
                                                                      
The first is ephemeris time (ET), which is specified as some number   
of ephemeris seconds past a reference epoch. Within the SPICE system, 
state vectors of spacecraft and target bodies are referenced to ET    
seconds past the J2000 epoch.                                         
                                                                      
The other is Coordinated Universal Time (UTC), which is also called   
Greenwich Mean Time. Two function calls are necessary to convert      
between UTC and SCLK. One function converts from SCLK to ET, and      
another from ET to UTC.                                               
                                                                      
See Appendix A for a list of high level functions involved in         
spacecraft clock time conversions.                                    
                                            
                                                                      
The SCLK kernel file                                      
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| Before calling any of the SCLK conversion functions mentioned       
  above, you have to load the contents of the SCLK kernel file into   
  the kernel pool, using the function                                 
  :py:meth:`~spiceypy.spiceypy.furnsh`.                             
                                                                      
The SCLK kernel file contains spacecraft specific parameters needed   
to perform the conversions. Included are such things as clock format  
definitions, partition start and stop times, and time interpolation   
constants. You should make sure that the kernel file you are using    
contains information for the particular spacecraft you are working    
with.                                                                 
                                                                      
You also have to load the leapseconds kernel file into the kernel     
pool if you are going to convert between ET and UTC.                  
                                            
                                                                      
Basics                                                    
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| This chapter will present the easiest way to use C-kernel software  
  to obtain pointing data from a CK file for a particular instrument. 
  The mechanism for doing so is a \``reader,'' a function which reads 
  data from the C-kernel. The highest level readers will be discussed 
  here; one that returns the C-matrix, and another that returns the   
  C-matrix and angular velocity vector.                               
                                                                      
A later chapter will present lower level functions that allow the     
programmer to exert the highest amount of control in reading CK       
files.                                                                
                                                                      
Appendix B contains an example showing how some of the functions      
presented in this chapter fit together in a typical application       
program.                                                              
                                            
                                                                      
The CK File Reader `ckgp_c <../cspice/ckgp_c.html>`__     
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| Below is a code fragment illustrating the use of the C-kernel file  
  reader `ckgp_c <../cspice/ckgp_c.html>`__ (Get Pointing). The       
  example finds the C-matrix for the Voyager 2 narrow angle camera at 
  a particular epoch during the Jupiter encounter. The C-matrix       
  returned is a transformation from the J2000 frame to                
  instrument-fixed coordinates.                                       
                                                                      
Each of the functions used is briefly described below. See the        
individual function headers for a complete description.               
                                                                      
A complete description of how `ckgp_c <../cspice/ckgp_c.html>`__      
searches for pointing is provided in the \``Details'' chapter of this 
document.                                                             
                                                                      
::                                                                    
                                                                      
         #include "SpiceUsr.h"                                        
                                                                      
         SpiceBoolean            found;                               
                                                                      
         SpiceChar             * ref;                                 
                                                                      
         SpiceDouble             clkout;                              
         SpiceDouble             cmat[3][3];                          
         SpiceDouble             sclkdp;                              
         SpiceDouble             tol;                                 
                                                                      
         SpiceInt                inst;                                
         SpiceInt                sc;                                  
                                                                      
         /*                                                           
         NAIF ID numbers for the                                      
                                                                      
            1. Voyager 2 spacecraft                                   
            2. Voyager 2 narrow angle camera                          
                                                                      
         */                                                           
         sc    =  -32;                                                
         inst  =  -32001;                                             
                                                                      
         /*                                                           
         The C-matrix should transform from J2000 to camera-fixed     
         coordinates.                                                 
         */                                                           
         ref  =  "J2000";                                             
                                                                      
         /*                                                           
         Load the spacecraft clock partition kernel file into the     
         kernel pool, for SCLK encoding and decoding.                 
         */                                                           
         furnsh_c ( "vgr2_sclk.tsc" );                                
                                                                      
         /*                                                           
         Load the C-kernel pointing file.                             
         */                                                           
         furnsh_c ( "vgr2_jup_inbound.bc" );                          
                                                                      
         /*                                                           
         We want pointing at a spacecraft clock time appearing in     
         the third spacecraft clock partition.                        
         */                                                           
         scencd_c ( sc, "3/20556:17:768", &sclkdp );                  
                                                                      
         /*                                                           
         The Voyager 2 clock is of the form xxxxx yy www, where       
         yy is a modulus 60 counter.  Pictures were not shuttered     
         at intervals smaller than one mod 60 count.  Therefore,      
         use this as the tolerance.  ( Notice that no partition       
         number is used when specifying a tolerance )                 
         */                                                           
         sctiks_c ( sc, "0:01:000", &tol );                           
                                                                      
         /*                                                           
         Get the pointing for the narrow angle camera.                
         */                                                           
         ckgp_c ( inst, sclkdp, tol, ref, cmat, &clkout, &found );    
                                                                      
                                                
                                                                      
:py:meth:`~spiceypy.spiceypy.furnsh`                    
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| :py:meth:`~spiceypy.spiceypy.furnsh` loads the kernel pool with   
  the contents of the specified text kernel file, which, in this case 
  is the SCLK kernel file.                                            
                                                                      
:py:meth:`~spiceypy.spiceypy.scencd` (below) and                    
:py:meth:`~spiceypy.spiceypy.scdecd` require the contents of the    
SCLK kernel file in order to properly encode and decode clock values. 
(See section on Spacecraft Clock Time).                               
                                                                      
:py:meth:`~spiceypy.spiceypy.furnsh` also loads a CK file for       
processing by other CK functions. It takes as input the name of the   
C-kernel file to be used, in this example                             
                                                                      
::                                                                    
                                                                      
      "vgr2_jup_inbound.bc"                                           
                                                                      
Once loaded, a file is ready for any number of reads, so it needs to  
be loaded only once, typically in the initialization section of your  
program. Among other things, the lower level routines called by       
:py:meth:`~spiceypy.spiceypy.furnsh` open the file with all the     
appropriate options, relieving you of that responsibility.            
|                                                         
                                                                      
:py:meth:`~spiceypy.spiceypy.scencd`                               
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| :py:meth:`~spiceypy.spiceypy.scencd` encodes a character          
  representation of spacecraft clock time such as                     
                                                                      
::                                                                    
                                                                      
      "3/20556:17:768"                                                
                                                                      
into a double precision number (sclkdp). The value returned by        
:py:meth:`~spiceypy.spiceypy.scencd` is a discrete tick count. When 
starting with an ET value, a continuous tick count may be obtained by 
calling :py:meth:`~spiceypy.spiceypy.sce2c`.                         
You must use encoded SCLK when calling CK reader functions.           
                                            
                                                                      
:py:meth:`~spiceypy.spiceypy.sctiks`                    
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| :py:meth:`~spiceypy.spiceypy.sctiks` converts a clock string      
  without partition number to units of \``ticks,'' which are the      
  units of encoded SCLK returned by                                   
  :py:meth:`~spiceypy.spiceypy.scencd`.                             
                                                                      
The distinction between :py:meth:`~spiceypy.spiceypy.scencd` and    
:py:meth:`~spiceypy.spiceypy.sctiks` is important. The result of    
calling :py:meth:`~spiceypy.spiceypy.scencd` is a relative          
measurement: ticks since the start of the clock at launch. The result 
of calling :py:meth:`~spiceypy.spiceypy.sctiks` is an absolute      
measurement: ticks. It's like the difference between the times 3:55   
p.m. (a specific time of the day) and 3:55 (three hours and           
fifty-five minutes - a length of time).                               
                                            
                                                                      
`ckgp_c <../cspice/ckgp_c.html>`__                        
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| `ckgp_c <../cspice/ckgp_c.html>`__ looks through files loaded by    
  :py:meth:`~spiceypy.spiceypy.furnsh` to find the data needed to   
  compute the C-matrix for a specified spacecraft instrument at a     
  particular time. It uses the following inputs and outputs.          
                                                                      
Inputs are:                                                           
                                                                      
**\`inst'**                                                           
   The NAIF instrument ID. In this example, we want pointing for the  
   Voyager 2 narrow angle camera (NAIF code -32001).                  
                                                                      
**\`sclkdp'**                                                         
   Encoded SCLK time. Units are \``ticks since clock start at         
   launch'' May be discrete or continuous.                            
                                                                      
**\`tol'**                                                            
   SCLK time tolerance. \`tol' is measured in units of \``ticks.''    
                                                                      
   The pointing returned by `ckgp_c <../cspice/ckgp_c.html>`__ will   
   be for a time within \`tol' ticks of \`sclkdp'. In general, \`tol' 
   should be smaller than the typical spacecraft clock time interval  
   between instrument observations.                                   
                                                                      
**\`ref'**                                                            
   The NAIF mnemonic for the base reference frame. The output         
   C-matrix, if found, will be a transformation from \`ref' to        
   instrument-fixed coordinates.                                      
                                                                      
   See the FRAMES Required Reading,                                   
   `frames.req <../req/frames.html>`__, for a list of those frames    
   supported by the SPICE system, along with the accepted mnemonics   
   for those frames.                                                  
                                                                      
Outputs are:                                                          
                                                                      
**\`cmat'**                                                           
   The C-matrix. \`cmat' is a transformation matrix from the base     
   frame \`ref' to the instrument-fixed frame at the time \`clkout'.  
                                                                      
**\`clkout'**                                                         
   Continuous encoded spacecraft clock time for which \`cmat' is      
   valid. This will be within \`tol' ticks of \`sclkdp'.              
                                                                      
**\`found'**                                                          
   Found flag. \`found' will be true if it was possible to return a   
   C-matrix for \`inst' for a time within \`tol' ticks of \`sclkdp'.  
   \`found' will be false otherwise.                                  
                                                                      
                                                
                                                                      
The CK File Reader :py:meth:`~spiceypy.spiceypy.ckgpav` 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| :py:meth:`~spiceypy.spiceypy.ckgpav` (Get Pointing and Angular    
  Velocity) is almost identical to                                    
  `ckgp_c <../cspice/ckgp_c.html>`__, except that it returns an       
  angular velocity vector in addition to a C-matrix.                  
                                                                      
The calling sequence for :py:meth:`~spiceypy.spiceypy.ckgpav` is:   
                                                                      
::                                                                    
                                                                      
      ckgpav_c ( inst, sclkdp, tol, ref, cmat, av, &clkout, &found ); 
                                                                      
The angular velocity vector \`av' is a double precision array of size 
three. The components of \`av' are given relative to the base         
reference frame \`ref'.                                               
All of the other arguments are identical to those of                  
`ckgp_c <../cspice/ckgp_c.html>`__. And, just as with                 
`ckgp_c <../cspice/ckgp_c.html>`__, you must load a CK file by        
calling :py:meth:`~spiceypy.spiceypy.furnsh` before calling         
:py:meth:`~spiceypy.spiceypy.ckgpav`.                               
                                                                      
The behavior of :py:meth:`~spiceypy.spiceypy.ckgpav` is, however,   
slightly different from that of `ckgp_c <../cspice/ckgp_c.html>`__,   
and these differences will be explained in the \``Details'' chapter   
of this document.                                                     
                                            
                                                                      
Multiple Files and the C-kernel                           
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| There will probably be occasions when you will want to access       
  pointing that is contained in more than one CK file. For instance,  
  you may have several files describing pointing for several disjoint 
  time periods, or for different instruments. Or you may have one     
  file containing a partially updated version of another file's       
  pointing.                                                           
                                                                      
In both cases, you would like to be able to get the pointing you want 
without having to run your application on each file separately.       
C-kernel software allows you to do this through the file loading and  
unloading process.                                                    
                                                                      
The file loading function :py:meth:`~spiceypy.spiceypy.furnsh` was  
introduced in the last section. It was mentioned that you have to     
load the CK file before you try to access it, that you have to load   
it only once during program execution, and that in subsequent calls   
to `ckgp_c <../cspice/ckgp_c.html>`__, you don't have to refer to the 
file at all.                                                          
                                                                      
What was not mentioned was that multiple pointing files may be loaded 
and that `ckgp_c <../cspice/ckgp_c.html>`__ will automatically search 
through as many of the files as necessary to satisfy the request.     
                                                                      
If you have multiple files describing pointing for different time     
periods or different instruments, you can simply load them all at the 
beginning of your program, and then forget about which file covered   
what period or instrument. There is a hierarchy for searching,        
however, that you need to understand in case you happen to load files 
that have redundant coverage.                                         
                                                                      
A request for pointing is satisfied by searching through the last     
loaded files first. Thus if we ran                                    
                                                                      
::                                                                    
                                                                      
      furnsh_c ( "ckfile_1.bc" );                                     
      furnsh_c ( "ckfile_2.bc" );                                     
      furnsh_c ( "ckfile_3.bc" );                                     
                                                                      
and then later made a request for pointing, the software would search 
through ckfile_3 first, ckfile_2 second, and ckfile_1 last.           
This scheme is consistent with the fact that within an individual     
file, the data that were inserted last supersede those before them.   
In essence, loaded files are treated like one big file.               
                                                                      
What if you have files representing different versions of the same    
pointing? This is a likely scenario considering there are tools (such 
as NAIF's C-smithing program) to update and \``improve'' pointing     
results.                                                              
                                                                      
For example, suppose you have one file containing predicted pointing  
values, and another containing improved, updated values. One approach 
would be to load the files in the following order:                    
                                                                      
::                                                                    
                                                                      
      furnsh_c ( "predict.bc" );                                      
      furnsh_c ( "update.bc"  );                                      
                                                                      
This way, the \``better'' (updated) pointing file always gets         
searched first.                                                       
If, on the other hand, you want to be explicit about which file to    
search, you need a way of telling C-kernel software to stop looking   
in one file, and start looking in another.                            
:py:meth:`~spiceypy.spiceypy.furnsh` accomplishes the latter by     
loading a file for processing. To tell C-kernel software to stop      
looking through a file, then, you need to unload it, with             
:py:meth:`~spiceypy.spiceypy.unload` :                              
                                                                      
::                                                                    
                                                                      
         #include "SpiceUsr.h"                                        
                                                                      
         /*                                                           
         Load the first version.                                      
         */                                                           
         furnsh_c ( "predict.bc" );                                   
                                                                      
            .                                                         
            .  process pointing from first file.                      
            .                                                         
                                                                      
         /*                                                           
         Unload the first version.                                    
         */                                                           
         unload_c ( "predict.bc" );                                   
                                                                      
         /*                                                           
         Load the second version.                                     
         */                                                           
         furnsh_c ( "update.bc" );                                    
                                                                      
            .                                                         
            .  process pointing from the second file.                 
            .                                                         
                                                                      
                                                                      
                                                
                                                                      
CK Coverage Summary Routines                              
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| The CSPICE includes two functions for obtaining information about   
  the contents of a CK file from within an application.               
                                                                      
The :py:meth:`~spiceypy.spiceypy.ckobj` function provides an API via 
which an application can find the set of instruments for which a      
specified CK file contains data. The instrument IDs are returned in a 
SPICE \``set'' data structure (see `sets.req <../req/sets.html>`__).  
                                                                      
The :py:meth:`~spiceypy.spiceypy.ckcov` function provides an API via 
which an application can find the time periods for which a specified  
CK file provides data for an instrument of interest. The coverage     
information is a set of disjoint time intervals returned in a SPICE   
\``window'' data structure (see                                       
`windows.req <../req/windows.html>`__).                               
                                                                      
Refer to the headers of :py:meth:`~spiceypy.spiceypy.ckobj` and      
:py:meth:`~spiceypy.spiceypy.ckcov` for details on the use of those  
routines.                                                             
                                            
                                                                      
Details                                                   
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| In the previous chapter, we introduced the two CK readers,          
  `ckgp_c <../cspice/ckgp_c.html>`__ and                              
  :py:meth:`~spiceypy.spiceypy.ckgpav`, which return C-matrices and 
  angular velocity vectors from CK files.                             
                                                                      
In this chapter we introduce the concept of a CK file segment, and    
explain how these segments are organized into CK files. We then show  
exactly how `ckgp_c <../cspice/ckgp_c.html>`__ and                    
:py:meth:`~spiceypy.spiceypy.ckgpav` go about searching through     
files and segments to obtain the data that they need.                 
                                            
                                                                      
File Structure and Implementation                         
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| Each C-kernel file is made up of a number of \``segments.'' A       
  segment is a set of logical records containing double precision     
  numbers. When evaluated, each record gives a C-matrix and           
  optionally, an angular velocity vector, of some spacecraft          
  structure for some time within an interval. The segments in a file  
  are ordered from beginning to end, with new segments added to the   
  end of a file. The C-kernel readers use this ordering to check      
  segments at the end of the file first.                              
                                                                      
Notice that the definition of a segment does not specify what type of 
record it contains. This vagueness is intentional. One of the primary 
features of the C-kernel is to provide a framework in which to store  
pointing data in any form, without users having to worry about that   
form when reading the data. Thus, different segments may contain      
different implementations of discrete or continuous data, but the     
same high-level readers are used to access all types.                 
                                                                      
In fact, there are only a couple of functions that are concerned with 
the internal data type of a segment. Other functions obtain all the   
information they need about a segment from two fields which precede   
each segment: \``descriptors'' and \``identifiers.'' Their formats    
are identical from segment to segment, and provide important          
information about the data contained inside.                          
                                            
                                                                      
Segment Descriptors                                       
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| The C-kernel reader functions begin addressing the question, \``Can 
  the request for pointing be satisfied by this segment?'' by looking 
  at the descriptor.                                                  
                                                                      
A descriptor tells what instrument's pointing is being described, the 
interval of time for which the segment is valid, the reference frame  
of the internally stored data, and the segment data type.             
                                                                      
Each segment descriptor contains two double precision components      
(DCD) and six integer components (ICD).                               
                                                                      
::                                                                    
                                                                      
              -----------------------------------                     
      DCD(1)  |  Initial SCLK                   |                     
              -----------------------------------                     
      DCD(2)  |  Final SCLK                     |                     
              -----------------------------------                     
      ICD(1)  |  Instrument    |                                      
              ------------------                                      
      ICD(2)  |  Reference     |                                      
              ------------------                                      
      ICD(3)  |  Data type     |                                      
              ------------------                                      
      ICD(4)  |  Rates Flag    |                                      
              ------------------                                      
      ICD(5)  |  Begin Address |                                      
              ------------------                                      
      ICD(6)  |  End   Address |                                      
              ------------------                                      
                                                                      
**DCD(1),DCD(2)**                                                              
   The initial and final encoded spacecraft clock times for the       
   segment.                                                           
                                                                      
**ICD(1)**                                                            
   The integer code of the instrument whose pointing is being         
   described.                                                         
                                                                      
**ICD(2)**                                                            
   The NAIF integer ID of the base reference frame for the segment    
   data. (For example, J2000, B1950, and so on --- to see which ID    
   represents which coordinate system, see the Frames Required        
   Reading, `frames.req <../req/frames.html>`__.)                     
                                                                      
**ICD(3)**                                                            
   The data type of the segment. This indicates how the data is       
   stored internally. The reader functions will use it to evaluate    
   the data records. Typically, users will not have to know this      
   code.                                                              
                                                                      
**ICD(4)**                                                            
   The angular rates flag. This indicates whether or not the segment  
   is capable of producing angular velocity data. If ICD(4) = 0, then 
   the segment contains pointing data only. If ICD(4) = 1, then the   
   segment contains angular velocity data as well.                    
                                                                      
**ICD(5),ICD(6)**                                                              
   Initial and final addresses of the segment data within the file.   
   Users will typically not want or need to know about these          
   addresses. They tell the readers where to go within a file to get  
   the records needed to satisfy a particular request.                
                                                                      
The descriptor is stored as a double precision array, with pairs of   
integer components equivalenced to double precision numbers. We say   
that the descriptor is \``packed'' into a double precision array. The 
size of a packed descriptor is five double precision numbers.         
In the \``Looking at Descriptors'' section, you will be shown how to  
get a descriptor from a particular segment and \``unpack'' it into    
its double precision and integer components. You can then view the    
individual components.                                                
                                            
                                                                      
Segment Identifiers                                       
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| The idea behind a segment identifier is to provide a character      
  field which allows a user to determine the exact origin of the      
  segment.                                                            
                                                                      
For the most part, it will be up to the institution that creates a    
particular C-kernel segment to determine what goes in this            
free-format 40 character memory cell. However, it should be possible  
for users to look at a segment identifier and determine who knows the 
details about the creation of the segment.                            
                                                                      
For example, if a particular identifier looked like                   
                                                                      
::                                                                    
                                                                      
      NAIF CSMITHING RET LOGA151                                      
                                                                      
then a user should be able to contact NAIF to locate the right people 
to give the history of that segment: ephemerides used, source of      
pointing, assumptions, constraints, and so on.                        
Forty characters is not enough space to store all source information  
for every segment that might be built. Instead, the idea is to        
provide a pointer to the people or documents that will have all of    
the details about the source of the data.                             
                                            
                                                                      
Comment Area                                              
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| In addition to segment identifiers, every binary CK file has a      
  \``Comment Area'' for storing free-format textual information about 
  the pointing data in the file. Ideally, each CK file will contain   
  internal documentation that describes all of the details about the  
  source of the data, its recommended use, and any other pertinent    
  information. For example, the beginning and ending epochs for the   
  file, the names and NAIF integer codes of the instruments included, 
  an accuracy estimate, the date the file was produced, the names of  
  the ephemeris files used, and any assumptions or constraints could  
  be included. Comments about a particular segment in the file could  
  refer to the segment by its identifier.                             
                                                                      
CSPICE provides a family of functions for handling this Comment Area. 
The name of each function in this family begins with the letters      
\```spc''' which stand for \```spk' and \`ck''' because this feature  
is common to both types of files. The SPC software provides the       
ability to add, extract, and delete comments and convert commented    
files from binary format to SPICE transfer format and back to binary  
again.                                                                
                                                                      
The SPC functions and their purposes are described in detail in the   
SPC Required Reading, `spc.req <../req/spc.html>`__.                  
                                            
                                                                      
A CK file is a DAF                                        
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| Each CK file is one implementation of a NAIF construct called a     
  Double Precision Array File (DAF). DAFs are described in detail in  
  reference [1]. Each CK segment is an instance of the DAF double     
  precision array. The descriptor is an instance of a DAF             
  \``summary''; the identifier is an instance of a DAF \``name.''     
                                                                      
DAF functions are used at the lowest level to open, close, read,      
write and search CK files. As such, they allow for maximum            
flexibility in, for instance, examining a particular number within a  
segment, or searching for a particular segment within a file.         
Therefore, if the CK functions presented in this document do not      
allow you the control you want in looking through files, the DAF      
functions certainly will.                                             
                                            
                                                                      
SPICE File Identification Word in CK Files                
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| The SPICE file identification word occupying the first eight bytes  
  of a properly created binary CK file is \``DAF/CK ''. For more      
  information on SPICE file identification words refer to the Kernel  
  Required Reading document, `kernel.req <../req/kernel.html>`__.     
                                            
                                                                      
How the CK Readers Work                                   
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| There are basically two steps to reading data from the C-kernel:    
  locating the segment applicable to the request made, and evaluating 
  the data contained inside the segment to return the C-matrix and    
  angular velocity vector. In this section you'll see how these steps 
  are implemented by `ckgp_c <../cspice/ckgp_c.html>`__ and           
  :py:meth:`~spiceypy.spiceypy.ckgpav`.                             
                                            
                                                                      
The General Search Algorithm                              
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| The CK readers search through files loaded by                       
  :py:meth:`~spiceypy.spiceypy.furnsh` to satisfy a pointing        
  request. The files are searched in the reverse order from which     
  they were loaded. Thus the last-loaded file is searched first, then 
  the second to last, and so forth. The contents of individual files  
  are also searched in backwards order, giving priority to segments   
  that were added to a file later than the others.                    
                                                                      
The search ends when a segment is found that can give pointing for    
the specified instrument at a time falling within the specified       
tolerance on either side of the request time. Within that segment,    
the instance closest to the input time is located and returned.       
                                                                      
The time for which pointing is being returned is not always the       
closest to the request time in all of the loaded files. The returned  
time is actually the closest time within the tolerance of the request 
time from the first segment that can satisfy the request. The         
algorithm works like this because it assumes that the last loaded     
files contain the highest quality pointing. Because segments are      
prioritized in this way users should not make their tolerance         
argument larger than the minimum spacing between the data in the      
files they are reading.                                               
                                                                      
The following example illustrates this search procedure. Segments A   
and B are in the same file, with segment A located closer to the end  
of the file than segment B. Both segments A and B contain discrete    
pointing data.                                                        
                                                                      
::                                                                    
                                                                      
                                                                      
                                    SCLKDP    TOL                     
                                         \   /                        
                                          | |                         
                                          |/ \                        
           Request 1                  [---+---]                       
                                      .   .   .                       
                                      .   .   .                       
           Segment A          (0-----------------0--------0--0-----0) 
                                      .   .   .                       
                                      .   .   .                       
           Segment B         (-0--0--0--0--0--0--0--0--0--0--0--0--0) 
                                           ^                          
                                           |                          
                             CK reader returns this instance          
                                                                      
                                                                      
                                                                      
                                         SCLKDP                       
                                              \   TOL                 
                                               | /                    
                                               |/\                    
           Request 2                        [--+--]                   
                                            .  .  .                   
                                            .  .  .                   
           Segment A          (0-----------------0--------0--0-----0) 
                                                 ^                    
                                                 |                    
                                   CK reader returns this instance    
                                                                      
           Segment B         (0-0--0--0--0--0--0--0--0--0--0--0--0-0) 
                                                                      
                                                                      
Segments that contain continuous pointing data are searched in the    
same manner as discrete segments. For request times that fall within  
the bounds of continuous intervals, the CK reader will return         
pointing at the request time. When the request time does not fall     
within an interval, then a time at an endpoint of an interval may be  
returned if it is the closest time in the segment to the user request 
time and also within the tolerance.                                   
In the following examples segment A contains discrete pointing data   
and segment C contains continuous data. Segment A is located closer   
to the end of the file than segment C.                                
                                                                      
::                                                                    
                                                                      
                               SCLKDP                                 
                                    \  TOL                            
                                     | /                              
                                     |/\                              
      Request 3                   [--+--]                             
                                  .  .  .                             
                                  .  .  .                             
      Segment A          (0-----------------0--------0--0-----0)      
                                  .  .  .                             
                                  .  .  .                             
      Segment C          (--[=============]---[====]------[=]--)      
                                     ^                                
                                     |                                
                        CK reader returns this instance               
                                                                      
                                                                      
In the next example assume that the order of segment A and C in file  
are reversed.                                                         
::                                                                    
                                                                      
                                      SCLKDP                          
                                           \   TOL                    
                                            | /                       
                                            |/\                       
      Request 4                          [--+--]                      
                                         .  .  .                      
                                         .  .  .                      
      Segment C          (--[=============]---[====]------[=]--)      
                                              ^                       
                                              |                       
                                CK reader returns this instance       
                                                                      
      Segment A          (0-----------------0--------0--0-----0)      
                                            ^                         
                                            |                         
                                      "Best" answer                   
                                                                      
                                                                      
The next example illustrates an unfortunate side effect of using a    
non-zero tolerance when reading multi-segment CKs with continuous     
data. In all cases when the look-up interval formed using tolerance   
overlaps a segment boundary and the request time falls within the     
coverage of the lower priority segment, the data at the end of the    
higher priority segment will be picked instead of the data from the   
lower priority segment.                                               
::                                                                    
                                                                      
                                              SCLKDP                  
                                             /                        
                                            |  TOL                    
                                            | /                       
                                            |/\                       
      Your request                       [--+--]                      
                                         .  .  .                      
                                         .  .  .                      
      Segment C                                (===============)      
                                               ^                      
                                               |                      
                                 CK reader returns this instance      
                                                                      
      Segment A          (=====================)                      
                                            ^                         
                                            |                         
                                      "Best" answer                   
                                                                      
In general, because using a non-zero tolerance affects selection of   
the segment from which the data is obtained, users are strongly       
discouraged from using a non-zero tolerance when reading CKs with     
continuous data. Using a non-zero tolerance should be reserved        
exclusively to reading CKs with discrete data because in practice     
obtaining data from such CKs using a zero tolerance is often not      
possible due to time round off.                                       
The next few sections will go into greater detail about how           
`ckgp_c <../cspice/ckgp_c.html>`__ and                                
:py:meth:`~spiceypy.spiceypy.ckgpav` search through segments.       
                                            
                                                                      
The Difference Between `ckgp_c <../cspice/ckgp_c.html>`__ and :py:meth:`~spiceypy.spiceypy.ckgpav`                         
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| The only significant difference between the search algorithms of    
  `ckgp_c <../cspice/ckgp_c.html>`__ and                              
  :py:meth:`~spiceypy.spiceypy.ckgpav` is in which segments they    
  search through to satisfy a request for pointing data. Recall that  
  segments in a CK file only optionally contain angular velocity      
  data. Since `ckgp_c <../cspice/ckgp_c.html>`__ does not return an   
  angular velocity vector, it is free to consider all segments when   
  satisfying a request, because all segments will contain the data    
  for constructing C-matrices.                                        
  :py:meth:`~spiceypy.spiceypy.ckgpav`, on the other hand, will     
  consider only those segments which also contain angular velocity    
  data.                                                               
                                                                      
Because of this difference, it is possible that on the exact same set 
of inputs, `ckgp_c <../cspice/ckgp_c.html>`__ and                     
:py:meth:`~spiceypy.spiceypy.ckgpav` could return different values  
for the C-matrix. This could occur if a CK file contained two         
segments covering the same time period for the same instrument, one   
with angular rates and one without.                                   
`ckgp_c <../cspice/ckgp_c.html>`__ might use the C-matrix only        
segment, whereas :py:meth:`~spiceypy.spiceypy.ckgpav` would ignore  
that segment and use the one containing angular velocity data.        
                                                                      
To avoid this situation, NAIF advises users not to place segments     
with and without angular velocity data in the same file.              
                                            
                                                                      
Locating the Applicable Segment                           
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| Within `ckgp_c <../cspice/ckgp_c.html>`__ and                       
  :py:meth:`~spiceypy.spiceypy.ckgpav`, finding the right segment   
  is the job of ckbss\_ (Begin a Search for a Segment), and cksns\_   
  (Select the Next Segment).                                          
                                                                      
The SPICELIB Fortran routines from which ckbss\_ and cksns\_ are      
derived are both entry points to the SPICELIB Fortran routine CKBSR   
(Buffer Segments for Readers).                                        
                                                                      
ckbss\_ establishes a search for segments. It records the desired     
instrument (\`inst'), SCLK time (\`sclkdp'), and SCLK tolerance       
(\`tol') for the search. It also records the need for angular         
velocity --- \`needav' is true if angular velocity data is being      
requested, false otherwise.                                           
                                                                      
cksns\_ then uses DAF functions to search through loaded files to     
find a segment matching the criteria established in the call to       
ckbss\_. Last-loaded files get searched first, and within a single    
file, segments get checked starting from the end of the file and      
going backwards.                                                      
                                                                      
When an applicable segment is found, the descriptor and identifier    
for that segment, and the handle of the file containing the segment,  
are returned, and the readers output Boolean flag \`found' is set to  
true. If no applicable segment is found, \`found' is false.           
                                                                      
If a segment is found, but is subsequently found to be inadequate,    
cksns\_ can be called again to find the next applicable segment using 
the searching order described above.                                  
                                                                      
cksns\_ can be called any number of times after a search has been     
started by ckbss\_, and will just return a false value for \`found'   
whenever applicable segments have run out.                            
                                                                      
Because cksns\_ is called every time a request is made, an internal   
buffer of segment descriptors is maintained by ckbsr\_ to keep from   
performing superfluous file reads. You can adjust the size of the     
buffer by changing the parameter STSIZE in ckbsr\_.                   
                                            
                                                                      
Looking at Descriptors                                    
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| The descriptor and handle returned by cksns\_ are used by other CK  
  functions to locate and evaluate the pointing records. In order to  
  do so, those functions have to unpack a descriptor into its double  
  precision and integer parts, using the DAF function                 
  :py:meth:`~spiceypy.spiceypy.dafus` (Unpack Summary).              
                                            
                                                                      
Evaluating the Records --- the Reader ckpfs\_             
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| After locating an appropriate segment via cksns\_,                  
  `ckgp_c <../cspice/ckgp_c.html>`__ and                              
  :py:meth:`~spiceypy.spiceypy.ckgpav` evaluate pointing records    
  with a call to ckpfs\_ (Pointing From Segment), a low level CK      
  reader.                                                             
                                                                      
ckpfs\_ takes as input the handle and descriptor of the applicable    
file and segment, along with the time specifications and angular      
velocity flag.                                                        
                                                                      
ckpfs\_ returns the C-matrix and, if requested, the angular velocity  
vector for the time in the segment closest to \`sclkdp' and within    
\`tol' ticks of it. If ckpfs\_ can't locate a time close enough in    
the segment, then \`found' is set to false. (If \`found' is false,    
then `ckgp_c <../cspice/ckgp_c.html>`__ and                           
:py:meth:`~spiceypy.spiceypy.ckgpav` will try another segment by    
calling cksns\_ again, then ckpfs\_ again, and so on.)                
                                                                      
The output data are referenced to the base frame indicated by the     
descriptor. In other words, at this point, \`cmat' is a               
transformation from the base frame specified by icd[1] to             
instrument-fixed coordinates, and the coordinates of \`av' lie in     
that same base frame.                                                 
                                            
                                                                      
Transforming the Results                                  
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| The final task performed by `ckgp_c <../cspice/ckgp_c.html>`__ and  
  :py:meth:`~spiceypy.spiceypy.ckgpav` is to transform the returned 
  data from their stored reference frame to that requested by the     
  calling program.                                                    
                                                                      
First, the functions compare the NAIF ID for the requested frame with 
that of the stored frame. If the requested frame matches the segment  
frame, there is nothing to be done. Otherwise, the C-matrix and       
angular velocity vector have to be transformed.                       
                                                                      
Recall that the C-matrix returned by ckpfs_c is a rotation matrix     
from a base frame (call it \`refseg') to instrument-fixed             
coordinates:                                                          
                                                                      
::                                                                    
                                                                      
      [          ] I-fixed                                            
      |          |                                                    
      |   CMAT   |                                                    
      |          |                                                    
      [          ] REFSEG                                             
                                                                      
What we want is a rotation matrix from the requested frame (call it   
\`refreq') to instrument-fixed coordinates:                           
::                                                                    
                                                                      
      [          ] I-fixed                                            
      |          |                                                    
      |   CMAT   |                                                    
      |          |                                                    
      [          ] REFREQ                                             
                                                                      
So all we have to do is multiply the returned C-matrix by a rotation  
matrix, call it \`rmat', from the requested frame to the one          
specified in the segment:                                             
::                                                                    
                                                                      
                                                                      
  [          ] I-fixed      [          ] I-fixed  [          ] REFSEG 
      |          |              |          |          |          |    
      |   CMAT   |          =   |   CMAT   |          |   RMAT   |    
      |          |              |          |          |          |    
                                                                      
  [          ] REFREQ       [          ] REFSEG   [          ] REFREQ 
                                                                      
Once you have \`rmat', it is a trivial matter to transform the        
angular velocity vector. Its coordinates, upon return from ckpfs\_,   
are in the frame \`refseg'.                                           
|                                                         
                                                                      
Data Types                                                
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| The C-kernel framework for providing pointing data has been         
  designed for flexibility. Different methods of storing and          
  evaluating the data can be implemented independently of the         
  high-level functions used to read the data. The only real           
  restriction is that each segment must be stored as an array of      
  double precision numbers.                                           
                                                                      
Each method of storing and evaluating the data contained in a segment 
defines a different \``data type.'' The data type of a segment is     
specified by the third integer component of the segment descriptor.   
The integer code for a data type is equal to the number of that type. 
For example, a segment of data type 1 would have the third integer    
component of its descriptor equal to 1. A data type need not          
accommodate angular velocity data. If it can't, all segments of that  
data type would have the value of the fourth integer component of the 
descriptor set equal to zero, which indicates that the segment does   
not contain angular velocity data.                                    
                                                                      
The CK reader that makes a distinction between segments of different  
data types is the low level reader CKPFS. The main body of CKPFS      
consists of a case statement of the form:                             
                                                                      
::                                                                    
                                                                      
      if ( type == 1 )                                                
      {                                                               
         .                                                            
         .                                                            
         .                                                            
      }                                                               
      else if ( type == 2 )                                           
      {                                                               
         .                                                            
         .                                                            
         .                                                            
      }                                                               
      else if ( type == n )                                           
      {                                                               
                                                                      
      }                                                               
      else                                                            
      {                                                               
         setmsg_c ( "The data type # is not currently supported." );  
         errint_c ( "#", type                                     );  
         sigerr_c ( "SPICE(CKUNKNOWNDATATYPE)"                    );  
      }                                                               
                                                                      
Once ckpfs\_ determines the data type of a segment, two type-specific 
functions are called. The first, ckrxx\_, reads a segment of type xx  
and returns the information from the segment necessary to evaluate    
pointing at a particular time. The second function ckexx\_ evaluates  
the information returned by ckrxx\_, producing a C-matrix, and if     
requested, an angular velocity vector.                                
There are currently four supported CK data types in CSPICE and they   
are described in detail in the sections that follow.                  
                                            
                                                                      
Data Type 1                                               
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| The following method of storing and evaluating discrete pointing    
  and angular rate values defines C-kernel data type 1.               
                                                                      
Each pointing instance is stored as a four-tuple called a             
\``quaternion.'' Quaternions are widely used to represent rotation    
matrices. They require less than half the space of 3x3 matrices and   
finding the rotation matrix given by a quaternion is faster and       
easier than finding it from, say, RA, Dec, and Twist. In addition,    
other computations involving rotations, such as finding the rotation  
representing two successive rotations, may be performed on the        
quaternions directly.                                                 
                                                                      
The four numbers of a quaternion represent a unit vector and an       
angle. The vector represents the axis of a rotation, and the angle    
represents the magnitude of that rotation. If the vector is U = (u1,  
u2, u3), and the angle is T, then the quaternion Q is given by:       
                                                                      
::                                                                    
                                                                      
           Q = ( q0, q1, q2, q3 )                                     
             = ( cos(T/2), sin(T/2)*u1, sin(T/2)*u2, sin(T/2)*u3 )    
                                                                      
The details of quaternion representations of rotations, and the       
derivations of those representations are documented in the CSPICE     
Required Reading file ROTATIONS,                                      
`rotation.req <../req/rotation.html>`__.                              
Data type 1 provides the option of including angular velocity data.   
If such data is included, the angular velocity vector A = (a1, a2, a3 
) corresponding to each pointing instance will be stored as itself.   
The coordinates of the vector will be in the same base reference      
frame as that of the C-matrix quaternions.                            
                                                                      
A type 1 pointing record consists of either four or seven double      
precision numbers; four for the C-matrix quaternion, and, optionally, 
three for the angular velocity vector.                                
                                                                      
::                                                                    
                                                                      
                                                                      
     +--------+--------+--------+--------+--------+--------+--------+ 
                                                                      
     |   q    |   q    |   q    |   q    |   a    |   a    |   a    | 
                                                                      
     |    0   |    1   |    2   |    3   |    1   |    2   |    3   | 
                                                                      
     +--------+--------+--------+--------+--------+--------+--------+ 
                                                                      
Every type 1 segment has four parts to it:                            
::                                                                    
                                                                      
                                                                      
   +----------------------------------------------------------------+ 
                                                                      
   |                                                                | 
                                                                      
   |                                                                | 
                                                                      
   |                           Pointing                             | 
                                                                      
   |                                                                | 
                                                                      
   |                                                                | 
                                                                      
   +----------------------------------------------------------------+ 
      |                  |                                            
      |                  |                                            
      |    SCLK times    |                                            
      |                  |                                            
      |                  |                                            
      +------------------+                                            
      |                  |                                            
      |  SCLK directory  |                                            
      |                  |                                            
      +------------------+                                            
      |      NPREC       |                                            
      +------------------+                                            
                                                                      
The final component, NPREC, gives the total number of pointing        
instances described by the segment.                                   
Preceding it, starting from the top, are NPREC pointing records,      
ordered with respect to time, each consisting of the four or seven    
double precision numbers described above.                             
                                                                      
Following the pointing section are the NPREC encoded spacecraft clock 
times corresponding to the pointing records. These must be in         
strictly increasing order.                                            
                                                                      
Following the SCLK times is a very simple SCLK directory. The         
directory contains INT( (NPREC-1) / 100 ) entries. The Ith directory  
entry contains the midpoint of the (I*100)th and the (I*100 + 1)st    
SCLK time. Thus,                                                      
                                                                      
::                                                                    
                                                                      
      Directory(1) = ( SCLKDP(100) + SCLKDP(101) )   / 2              
                                                                      
      Directory(2) = ( SCLKDP(200) + SCLKDP(201) )   / 2              
                                                                      
and so on.                                                            
If there are 100 or fewer entries, there is no directory. The         
directory is used to narrow down searches for pointing records to     
groups of 100 or less. Midpoints of adjacent times are used so that   
if an input time falls on one side of the directory time, then the    
group represented by that side is guaranteed to contain the time      
closest to the input time.                                            
                                            
                                                                      
Type 1 functions                                          
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| There are several CK functions that support data type 1. Their      
  names and functions are:                                            
                                                                      
:py:meth:`~spiceypy.spiceypy.ckw01`                                  
   writes a type 1 segment to a file.                                 
                                                                      
**ckr01\_**                                                           
   reads a pointing record from a type 1 segment that satisfies a     
   request for pointing at a given time.                              
                                                                      
**cke01\_**                                                           
   evaluates the record supplied by CKR01.                            
                                                                      
**cknr01\_**                                                          
   gives the number of pointing instances in a type 1 segment.        
                                                                      
**ckgr01\_**                                                          
   gets the Ith pointing instance from a type 1 segment.              
                                                                      
                                                
                                                                      
Data Type 2                                               
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| The following method of storing and evaluating continuous pointing  
  data for a spacecraft structure defines C-kernel data type 2.       
                                                                      
A type 2 segment consists of disjoint intervals of time during which  
the angular velocity of the spacecraft is constant. Thus, throughout  
an interval, the spacecraft structure rotates from its initial        
position about a fixed right-handed axis defined by the direction of  
the angular velocity vector at a constant rate equal to the magnitude 
of that vector.                                                       
                                                                      
A type 2 CK segment contains the following information for each       
interval:                                                             
                                                                      
#. The encoded spacecraft clock START and STOP times for the    
    interval.                                                           
                                                                      
#. The quaternion representing the C-matrix associated with the 
    start time of the interval.                                         
                                                                      
#. The constant angular velocity vector, in radians per second, 
    for the interval.                                                   
                                                                      
#. A factor which relates seconds and encoded SCLK ticks. This  
    is necessary to convert the difference between the requested and    
    interval start times from SCLK to seconds.                          
                                                                      
The orientation of a spacecraft structure may be determined from the  
above information at any time that is within the bounds of one of the intervals.                                                            
Every type 2 segment is organized into four parts.                    
                                                                      
::                                                                    
                                                                      
                                                                      
   +----------------------------------------------------------------+ 
                                                                      
   |                                                                | 
                                                                      
   |                                                                | 
                                                                      
   |                          Pointing                              | 
                                                                      
   |                                                                | 
                                                                      
   |                                                                | 
                                                                      
   +----------------------------------------------------------------+ 
      |                    |                                          
      |                    |                                          
      |  SCLK start times  |                                          
      |                    |                                          
      |                    |                                          
      +--------------------+                                          
      |                    |                                          
      |                    |                                          
      |  SCLK stop times   |                                          
      |                    |                                          
      |                    |                                          
      +--------------------+                                          
      |                    |                                          
      |  SCLK directory    |                                          
      |                    |                                          
      +--------------------+                                          
                                                                      
The first part of a segment contains pointing records which are       
ordered with respect to their corresponding interval start times. A   
type 2 pointing record contains eight double precision numbers in the 
following form:                                                       
::                                                                    
                                                                      
                                                                      
     +-------+-------+-------+-------+-------+-------+-------+------+ 
                                                                      
     |       |       |       |       |       |       |       |      | 
                                                                      
     |  q0   |  q1   |  q2   |  q3   |  a1   |  a2   |  a3   | rate | 
                                                                      
     |       |       |       |       |       |       |       |      | 
                                                                      
     +-------+-------+-------+-------+-------+-------+-------+------+ 
                                                                      
The first four elements are the components of the quaternion Q =      
(q0,q1,q2,q3) that is used to represent the C-matrix associated with  
the start time of the interval. Next are the three components of the  
angular velocity vector A = (a1,a2,a3) which are given with respect   
to the base reference frame specified in the segment descriptor.      
The last element is a rate which converts the difference between the  
requested and interval start time from encoded SCLK ticks to seconds. 
                                                                      
For segments containing predict data, this factor will be equal to    
the nominal amount of time represented by one tick of the particular  
spacecraft's clock. The nominal rate is given here for several        
spacecraft.                                                           
                                                                      
::                                                                    
                                                                      
      spacecraft                   seconds / tick ( sec )             
      ---------------------        ----------------------             
      Galileo                      1 / 120                            
      Mars Global Surveyor         1 / 256                            
      Voyager I and II             0.06                               
                                                                      
For segments based on real rather than predicted pointing, the rate   
at which the spacecraft clock runs relative to ephemeris time will    
deviate from the nominal rate. The creator of the segment will need   
to determine an average value for this rate over the time period of   
the interval.                                                         
Located after the pointing data are the interval START times followed 
by the STOP times.                                                    
                                                                      
The START and STOP times should be ordered and in encoded SCLK form.  
The intervals should be disjoint except for possibly at the           
endpoints. If an input request time falls on an overlapping endpoint  
then the interval used will be the one corresponding to the start     
time. Degenerate intervals in which the STOP time equals the START    
time are not allowed.                                                 
                                                                      
Following the STOP times is a very simple directory of spacecraft     
clock times containing INT( (NPREC-1)/100 ) entries, where NPREC is   
the number of pointing intervals. The Ith directory entry contains    
the midpoint of the (I*100)th STOP and the (I*100 + 1)st START SCLK   
time.                                                                 
                                                                      
::                                                                    
                                                                      
      Thus,                                                           
                                                                      
      Directory(1) = ( STOP(100) + START(101) )   / 2                 
                                                                      
      Directory(2) = ( STOP(200) + START(201) )   / 2                 
                                                                      
      .                                                               
      .                                                               
      .                                                               
                                                                      
If there are 100 or fewer entries then there is no directory. The     
directory is used to narrow down searches for pointing records to     
groups of 100 or less.                                                
|                                                         
                                                                      
Type 2 functions                                          
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| There are several CK functions that support data type 2. Their      
  names and functions are:                                            
                                                                      
:py:meth:`~spiceypy.spiceypy.ckw02`                                  
   writes a type 2 segment to a file.                                 
                                                                      
**ckr02\_**                                                           
   reads a pointing record from a type 2 segment that satisfies a     
   request for pointing at a given time.                              
                                                                      
**cke02\_**                                                           
   evaluates the record supplied by CKR02.                            
                                                                      
**cknr02\_**                                                          
   gives the number of pointing records in a type 2 segment.          
                                                                      
**ckgr02\_**                                                          
   gets the Ith pointing record from a type 2 segment.                
                                                                      
                                                
                                                                      
Data Type 3                                               
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| The following method of storing and evaluating discrete pointing    
  data for a spacecraft structure defines C-kernel data type 3.       
                                                                      
A type 3 segment consists of discrete pointing instances that are     
partitioned into groups within which linear interpolation between     
adjacent pointing instances is valid. Since the pointing instances in 
a segment are ordered with respect to time, these groups can be       
thought of as representing intervals of time over which the pointing  
of a spacecraft structure is given continuously. Therefore, in the    
description that follows, these groups of pointing instances will be  
referred to as interpolation intervals.                               
                                                                      
All of the pointing instances in the segment must be ordered by       
encoded spacecraft clock time and must belong to one and only one     
interpolation interval. The intervals must begin and end at times for 
which there are pointing instances in the segment. The CK software    
that evaluates the data in the segment does not extrapolate pointing  
past the bounds of the intervals.                                     
                                                                      
A user's view of the time coverage provided by a type 3 segment can   
be viewed pictorially as follows:                                     
                                                                      
::                                                                    
                                                                      
                                                                      
                                                                      
    pointing instances:     0-0-0-0-0----0-0-0-0-0-----0------0-0-0-0 
                                                                      
                            |       |    |       |     |      |     | 
                                                                      
    interval bounds:       BEG      |   BEG      |    BEG    BEG    | 
                                                                      
                                  END          END   END          END 
                                                                      
                                                                      
In the above picture, the zeros indicate the times associated with    
the discrete pointing instances and the vertical bars show the bounds 
of the interpolation intervals that they are partitioned into. Note   
that the intervals begin and end at times associated with pointing    
instances. Also note that intervals consisting of just a single       
pointing instance are allowed.                                        
When pointing is desired for a time that is within the bounds of one  
of the intervals, the CK reader functions return interpolated         
pointing at the request time. In the example below, the pointing      
request time is indicated by SCLKDP and the user-supplied tolerance   
is given by TOL. In this example the tolerance argument of the CK     
readers could be set to zero and pointing would still be returned.    
                                                                      
::                                                                    
                                                                      
                                        SCLKDP    TOL                 
                                             \   /                    
                                              | |                     
                                              |/ \                    
                                          [---+---]                   
                                          .   .   .                   
                                          .   .   .                   
                                                                      
    pointing instances:     0-0-0-0-0----0-0-0-0-0-----0------0-0-0-0 
                                                                      
                            |       |    |  ^    |     |      |     | 
                                                                      
    interval bounds:       BEG      |   BEG |    |    BEG    BEG    | 
                                                                      
                                  END      |   END   END          END 
                                              |                       
               CK reader returns interpolated pointing at this time.  
                                                                      
When a request time falls in a gap between intervals, no              
extrapolation is performed. Instead, pointing is returned for the     
interval endpoint closest to the request time, provided that time is  
within the user supplied tolerance. In this example if the tolerance  
were set to zero no pointing would be returned.                       
::                                                                    
                                                                      
                                               SCLKDP                 
                                                    \   TOL           
                                                     | /              
                                                     |/\              
                                                 [---+---]            
                                                 .   .   .            
                                                 .   .   .            
                                                                      
    pointing instances:     0-0-0-0-0----0-0-0-0-0-----0------0-0-0-0 
                                                                      
                            |       |    |       |     |      |     | 
                                                                      
    interval bounds:       BEG      |   BEG      |    BEG    BEG    | 
                                                                      
                                  END          END   END          END 
                                                   ^                  
                                                   |                  
                                   CK reader returns this instance.   
                                                                      
The physical structure of the data stored in a type 3 segment is as   
follows:                                                              
::                                                                    
                                                                      
                                                                      
  +-----------------------------------------------------------------+ 
                                                                      
  |                                                                 | 
                                                                      
  |                                                                 | 
                                                                      
  |                          Pointing                               | 
                                                                      
  |                                                                 | 
                                                                      
  |                                                                 | 
                                                                      
  +-----------------------------------------------------------------+ 
      |                        |                                      
      |  SCLK times            |                                      
      |                        |                                      
      +------------------------+                                      
      |                        |                                      
      |  SCLK directory        |                                      
      |                        |                                      
      +------------------------+                                      
      |                        |                                      
      |  Interval start times  |                                      
      |                        |                                      
      +------------------------+                                      
      |                        |                                      
      |  Start times directory |                                      
      |                        |                                      
      +------------------------+                                      
      |                        |                                      
      |  Number of intervals   |                                      
      |                        |                                      
      +------------------------+                                      
      |                        |                                      
      |  Number of pointing    |                                      
      |      instances         |                                      
      |                        |                                      
      +------------------------+                                      
                                                                      
In the discussion that follows let NPREC be the number of pointing    
instances in the segment and let NUMINT be the number of intervals    
into which the pointing instances are partitioned.                    
The first part of a segment contains NPREC pointing records which are 
ordered with respect to increasing time. Depending on whether or not  
the segment contains angular velocity data, a type 3 pointing record  
contains either four or seven double precision numbers in the         
following form:                                                       
                                                                      
::                                                                    
                                                                      
                                                                      
     +--------+--------+--------+--------+--------+--------+--------+ 
                                                                      
     |        |        |        |        |        |        |        | 
                                                                      
     |   q0   |   q1   |   q2   |   q3   |   a1   |   a2   |   a3   | 
                                                                      
     |        |        |        |        |        |        |        | 
                                                                      
     +--------+--------+--------+--------+--------+--------+--------+ 
                                                                      
The first four elements are the components of the quaternion Q =      
(q0,q1,q2,q3) that is used to represent the pointing of the           
instrument or spacecraft structure to which the segment applies. Next 
are the three components of the angular velocity vector AV =          
(a1,a2,a3) which are given with respect to the base reference frame   
specified in the segment descriptor. These components are optional    
and are present only if the segment contains angular velocity data as 
specified by the fourth integer component of the segment descriptor.  
Following the pointing data are the NPREC times associated with the   
pointing instances. These times are in encoded SCLK form and should   
be strictly increasing.                                               
                                                                      
Immediately following the last time is a very simple directory of the 
SCLK times. The directory contains INT( (NPREC-1) / 100 ) entries.    
The Ith directory entry contains the (I*100)th SCLK time. Thus,       
                                                                      
::                                                                    
                                                                      
      Directory(1) = SCLKDP(100)                                      
                                                                      
      Directory(2) = SCLKDP(200)                                      
                                                                      
      .                                                               
      .                                                               
      .                                                               
                                                                      
If there are 100 or fewer entries, there is no directory. The         
directory is used to narrow down searches for pointing records to     
groups of 100 or less.                                                
Next are the NUMINT start times of the intervals that the pointing    
instances are partitioned into. These times are given in encoded      
spacecraft clock and must be strictly increasing. They must also be   
equal to times for which there are pointing instances in the segment. 
Note that the interval stop times are not stored in the segment. They 
are not needed because the stop time of the Ith interval is simply    
the time associated with the pointing instance that precedes the      
start time of the (I+1)th interval.                                   
                                                                      
Following the interval start times is a directory of these times.     
This directory is constructed in a form similar to the directory for  
the times associated with the pointing instances. The start times     
directory contains INT ( (NUMINT-1) / 100 ) entries and contains      
every 100th start time. Thus:                                         
                                                                      
::                                                                    
                                                                      
      Directory(1) = START(100)                                       
                                                                      
      Directory(2) = START(200)                                       
                                                                      
      .                                                               
      .                                                               
      .                                                               
                                                                      
Finally, the last two words in the segment give the total number of   
interpolation intervals (NUMINT) and the total number of pointing     
instances (NPREC) in the segment.                                     
A segment writer function is provided which calls the low level DAF   
functions necessary to write a type 3 segment to a C-kernel. However, 
the creator of the segment is responsible for determining whether or  
not it is valid to interpolate between adjacent pointing instances,   
and thus how they should be partitioned into intervals. See the       
header of the function :py:meth:`~spiceypy.spiceypy.ckw03` for a     
complete description of the inputs required to write a segment.       
                                            
                                                                      
Linear Interpolation Algorithm                            
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| The linear interpolation performed between adjacent pointing        
  instances by the CK software is defined by the following algorithm: 
                                                                      
#. Let t be the time for which pointing is desired and let      
   CMAT1 and CMAT2 be C-matrices associated with times t1 and t2 such  
   that:                                                               
                                                                      
::                                                                    
                                                                      
                              t1 <= t <= t2,  where t1 < t2.          
                                                                      
#. Assume that the spacecraft frame rotates about a fixed axis  
   at a constant angular rate from time t1 to time t2. Then the        
   rotation axis and angle can be derived from the rotation matrix     
   ROT12 where:                                                        
                                                                      
::                                                                    
                                                                      
                                   T                       T          
                              CMAT2   =  ROT12    *   CMAT1           
                                                                      
                  or                                                  
                                              T                       
                              ROT12   =  CMAT2    *   CMAT1           
                                                                      
#. Obtain the axis and angle of the rotation from the matrix    
   ROT12. Let the axis vector of the rotation be AXIS and the rotation 
   angle be ANGLE.                                                     
                                                                      
#. To obtain pointing information at time t, rotate the         
   spacecraft frame about the vector AXIS from its orientation at time 
   t1 by the angle THETA where:                                        
                                                                      
::                                                                    
                                                                      
                                                   ( t  - t1 )        
                              THETA  =  ANGLE  *   -----------        
                                                   ( t2 - t1 )        
                                                                      
#. Thus if ROT1t is the matrix that rotates vectors by the      
   angle THETA about the vector AXIS, then the desired C-matrix is     
   given by:                                                           
                                                                      
::                                                                    
                                                                      
                                                                      
                                  T                     T             
                              CMAT  =  ROT1t   *   CMAT1              
                                                                      
                                                        T             
                              CMAT  =  CMAT1   *   ROT1t              
                                                                      
#. The angular velocity is treated independently of the         
   C-matrix. If it is requested, then the AV at time t is the weighted 
   average of the angular velocity vectors at time t1 and time t2:     
                                                                      
::                                                                    
                                                                      
                                                                      
                                 ( t  - t1 )                          
                           W  =  -----------                          
                                 ( t2 - t1 )                          
                                                                      
                                                                      
                           AV  = ( 1 - W ) * AV1   +   W * AV2        
                                                                      
                                                                      
                                                
                                                                      
Type 3 functions                                          
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| There are several CK functions that support data type 3. Their      
  names and function are:                                             
                                                                      
:py:meth:`~spiceypy.spiceypy.ckw03`                                  
   writes a type 3 segment to a file.                                 
                                                                      
**ckr03\_**                                                           
   reads a pointing record from a type 3 segment that satisfies a     
   request for pointing at a given time.                              
                                                                      
**cke03\_**                                                           
   evaluates the record supplied by CKR03.                            
                                                                      
**cknr03\_**                                                          
   gives the number of pointing instances in a type 3 segment.        
                                                                      
**ckgr03\_**                                                          
   gets the Ith pointing instance from a type 3 segment.              
                                                                      
                                                
                                                                      
Data Type 4                                               
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| The following method of storing and evaluating continuous pointing  
  data for a spacecraft structure defines C-kernel data Type 4.       
                                                                      
A Type 4 segment contains one or more sets of Chebychev polynomial    
coefficients that approximate orientation and optionally angular rate 
of a spacecraft, spacecraft structure or science instrument. Each set 
of coefficients is valid for a specific interval of time, the bounds  
of which are attached to the set. A typical Type 4 segment coverage   
is shown in the picture below:                                        
                                                                      
::                                                                    
                                                                      
       continuous pointing:    0-------0-------0    00     0-----0    
                               |       |       |    ||     |     |    
       interval bounds:       BEG      |BEG    |  BEG|    BEG    |    
                                    END       END    END        END   
                                                                      
In the picture, the zeros indicate the times associated with the      
bounds of intervals where pointing is available (between BEG and END) 
and not available (between END and BEG). Zero length intervals are    
not allowed.                                                          
When pointing is desired for a time that is within the bounds of one  
of the intervals, the CK reader functions return pointing and         
optionally angular rate computed at the request time from Chebychev   
polynomials for that interval. In the example below, the pointing     
request time is indicated by SCLKDP and the user supplied tolerance   
is given by TOL. In this example the tolerance argument could be set  
to zero and pointing would still be returned.                         
                                                                      
::                                                                    
                                                                      
                                      SCLKDP    TOL                   
                                           \   /                      
                                            | |                       
                                            |/ \                      
                                        [---+---]                     
                                        .   .   .                     
                                        .   .   .                     
       continuous pointing:    0-------0-------0    00     0-----0    
                               |       |    ^  |    ||     |     |    
       interval bounds:       BEG      |BEG .  |  BEG|    BEG    |    
                                    END     . END    END        END   
                                            .                         
                          CK reader returns pointing at this time.    
                                                                      
When a request time falls in a gap between intervals, pointing is     
evaluated for the interval endpoint closest to the request time if    
there is an endpoint within the user supplied tolerance of the        
request time. In this example if the tolerance were set to zero no    
pointing would be returned.                                           
::                                                                    
                                                                      
                                           SCLKDP    TOL              
                                                \   /                 
                                                 | |                  
                                                 |/ \                 
                                             [---+---]                
                                             .   .   .                
                                             .   .   .                
       continuous pointing:    0-------0-------0    00     0-----0    
                               |       |       |    ||     |     |    
       interval bounds:       BEG      |BEG    |  BEG|    BEG    |    
                                    END       END    END        END   
                                               ^                      
                                               |                      
                                   CK reader returns this instance.   
                                                                      
The CK data Type 4 uses the CSPICE concept of a generic segment to    
store a collection of packets each of which models the pointing of a  
spacecraft, spacecraft structure or science instrument during some    
interval of time. Each packet contains sets of coefficients for       
Chebychev polynomials that approximate the orientation quaternion.    
The packets may optionally contain polynomial coefficients for        
angular velocity vector components. The time intervals covered by     
individual packets in a CK Type 4 segment are non-overlapping and can 
have variable length. There can be gaps between intervals; the gaps   
can also be of variable length.                                       
The storage, arrangement and retrieval of packets is handled by the   
CSPICE generic segment functions. That software is described in the   
document GENSEG.REQ. We only review the pertinent points about        
generic segments here.                                                
                                                                      
A generic CK segment contains several logical data partitions:        
                                                                      
#. A partition for constant values to be associated with each   
   data packet in the segment.                                         
                                                                      
#. A partition for the data packets.                            
                                                                      
#. A partition for packet coverage begin times.                 
                                                                      
#. A partition for a packet directory, if the segment contains  
   variable sized packets.                                             
                                                                      
#. A partition for a packet coverage begin time directory.      
                                                                      
#. A reserved partition that is not currently used. This        
   partition is only for the use of the NAIF group at the Jet          
   Propulsion Laboratory (JPL).                                        
                                                                      
#. A partition for the metadata which describes the locations   
   and sizes of other partitions as well as providing some additional  
   descriptive information about the generic segment.                  
                                                                      
::                                                                    
                                                                      
                     +============================+                   
                     |         Constants          |                   
                     +============================+                   
                     |          Packet 1          |                   
                     |----------------------------|                   
                     |          Packet 2          |                   
                     |----------------------------|                   
                     |              .             |                   
                     |              .             |                   
                     |              .             |                   
                     |----------------------------|                   
                     |          Packet N          |                   
                     +============================+                   
                     |      Reference Times       |                   
                     +============================+                   
                     |      Packet Directory      |                   
                     +============================+                   
                     |       Time  Directory      |                   
                     +============================+                   
                     |       Reserved  Area       |                   
                     +============================+                   
                     |      Segment Metadata      |                   
                     +----------------------------+                   
                                                                      
Only the placement of the metadata at the end of a generic segment is 
required. The other data partitions may occur in any order in the     
generic segment because the metadata will contain pointers to their   
appropriate locations within the generic segment.                     
In the case of Type 4 CK segments each \``packet'' contains time of   
the middle of approximation interval SCLKDP, radius of approximation  
interval RADIUS, numbers of coefficients for each quaternion and      
angular rate component encoded in a single DP number, and four or     
seven sets of Chebychev polynomial coefficients which approximate     
four quaternion components and (optionally) three angular velocity    
components during the given time interval.                            
                                                                      
In order to provide a more compact data representation the number of  
coefficients can vary from component to component. To accomodate this 
generic segments with variable sized data packets are used as the     
underlying structure holding CK Type 4 data.                          
                                                                      
Each data packet has the following structure:                         
                                                                      
::                                                                    
                                                                      
            +----------------------------------------------+          
            |        Midpoint of approx. interval          |          
            +----------------------------------------------+          
            |            Radius of interval                |          
            +----------------------------------------------+          
            |          Number of coefficients for          |          
            |          (Q0,Q1,Q2,Q3,AV1,AV2,AV3)           |          
            +----------------------------------------------+          
            |           q0 Cheby coefficients              |          
            +----------------------------------------------+          
            |           q1 Cheby coefficients              |          
            +----------------------------------------------+          
            |           q2 Cheby coefficients              |          
            +----------------------------------------------+          
            |           q3 Cheby coefficients              |          
            +----------------------------------------------+          
            |      av1 Cheby coefficients (optional)       |          
            +----------------------------------------------+          
            |      av2 Cheby coefficients (optional)       |          
            +----------------------------------------------+          
            |      av3 Cheby coefficients (optional)       |          
            +----------------------------------------------+          
                                                                      
The maximum Chebychev polynomial degree allowed in CK Type 4 is 18.   
Packets within a CK Type 4 segment must be stored in strictly time    
increasing order.                                                     
                                                                      
The numbers of coefficients for each quaternion and angular rate      
component are packed into a single DP number using an encoding        
function which is a part of the CSPICE CK4 functions family. This DP  
number occurs as the third entry in a packet.                         
                                                                      
The \``constants'' partition in CK Type 4 does not contain any        
values.                                                               
                                                                      
The reference times partition contains an ordered collection of       
encoded spacecraft clock times. The i'th reference time corresponds   
to the beginning of the interval for which the i'th packet can be     
used to determine the pointing of spacecraft.                         
                                                                      
The \``time directory'' contains every 100th reference time. The time 
directory is used to efficiently locate the reference times that      
should be associated with a time for which a pointing has been        
requested.                                                            
                                                                      
As noted above the exact location of the various partitions must be   
obtained from the metadata contained at the end of the segment.       
                                                                      
Access to the Type 4 CK data is made via the CSPICE generic segment   
functions.                                                            
                                                                      
Type 4 CK segments should be created using CK Type 4 writer functions 
ckw04b\_, ckw04a\_ and ckw04e\_, provided in the CSPICE.              
                                            
                                                                      
CK Type 4 pointing evaluation algorithm                   
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| The CSPICE function chbval\_ is used to evaluate individual         
  quaternion and angular rate components from the corresponding       
  Chebychev polynomial coefficients. Refer to the header of the       
  chbval\_ function for more information.                             
                                            
                                                                      
Type 4 functions                                          
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| There are several CK functions that support data Type 4. Their      
  names and functions are:                                            
                                                                      
**ckr04\_**                                                           
   reads a record from a Type 4 segment that satisfies a request for  
   pointing at a given time.                                          
                                                                      
**cke04\_**                                                           
   evaluates the record supplied by ckr04\_.                          
                                                                      
**cknr04\_**                                                          
   gives the total number of data packets in a Type 4 segment.        
                                                                      
**ckgr04\_**                                                          
   gets the I'th record from a Type 4 segment.                        
                                                                      
**ckw04b\_**                                                          
   begins a Type 4 CK data segment                                    
                                                                      
**ckw04a\_**                                                          
   adds data to a Type 4 CK segment                                   
                                                                      
**ckw04e\_**                                                          
   ends a Type 4 CK data segment                                      
                                                                      
                                                
                                                                      
Data Type 5                                               
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| CK type 5 has been provided to support accurate duplication within  
  the CK system of spacecraft attitude data used by the European      
  Space Agency (ESA) on the Mars Express (MEX) and Rosetta missions.  
  However, the algorithms used by CK type 5 are very general; type    
  5's applicability is by no means limited to these missions.         
                                                                      
Because of the possibility of evolution of the mathematical           
representations of spacecraft attitude used by ESA, CK type 5 is      
designed to accommodate multiple representations, thereby avoiding a  
proliferation of CK data types. CK type 5 refers to each supported    
mathematical representation of attitude data as a \``subtype.''       
                                                                      
Currently CK type 5 supports four subtypes. All of these use          
polynomial interpolation to provide continuous pointing data.         
However, the creator of a type 5 segment may wish to restrict the     
intervals over which interpolation is allowed to occur. To support    
this capability, CK type 5 uses the same interpolation interval       
scheme as does type 3. This scheme will be explained shortly.         
                                                                      
The CK type 5 subtypes are as follows:                                
                                                                      
#. Subtype 0:                                                   
                                                                      
- Sliding-window Hermite interpolation of quaternions and        
  quaternion derivatives. Attitude and angular velocity are           
  represented by a series of 8-element \``packets'' and associated    
  time tags. The time tags may be unequally spaced. Each packet       
  contains four quaternion components followed by four quaternion     
  time derivative components. A quaternion representing attitude at a 
  request time is derived by using Hermite interpolation on each      
  quaternion component and the corresponding derivative, where the    
  values to be interpolated are obtained for a consecutive series of  
  epochs centered at the request time. The interpolated quaternion is 
  then unitized. The same interpolation degree is used for each       
  quaternion component.                                               
                                                                      
#. Subtype 1:                                                   
                                                                      
- Sliding-window Lagrange interpolation of quaternions. Attitude 
  is represented by a series of 4-element \``packets'' and associated 
  time tags. The time tags may be unequally spaced. Each packet       
  contains four quaternion components. A quaternion representing      
  attitude at a request time is derived by using Lagrange             
  interpolation on each quaternion component, where the values to be  
  interpolated are obtained for a consecutive series of epochs        
  centered at the request time. The interpolated quaternion is then   
  unitized. The same interpolation degree is used for each quaternion 
  component.                                                          
                                                                      
- Angular velocity is obtained by first forming the time         
  derivative of the quaternion using the derivatives of the           
  interpolating polynomials, then combining the quaternion and its    
  derivative to obtain angular velocity.                              
                                                                      
#. Subtype 2:                                                   
                                                                      
- Sliding-window Hermite interpolation of quaternions and        
  angular velocity. Attitude and angular velocity are represented by  
  a series of 14-element \``packets'' and associated time tags. The   
  time tags may be unequally spaced. Each packet contains four        
  quaternion components, four quaternion derivative components, three 
  angular velocity components, and three angular acceleration         
  components. A quaternion representing attitude at a request time is 
  derived by using Hermite interpolation on each quaternion component 
  and the corresponding derivative, where the values to be            
  interpolated are obtained for a consecutive series of epochs        
  centered at the request time. The interpolated quaternion is then   
  unitized. Angular velocity is obtained by using Hermite             
  interpolation on each angular velocity component and the            
  corresponding derivative. The attitude and angular velocity         
  resulting from this interpolation method are in principle           
  independent. The same interpolation degree is used for each         
  quaternion and angular velocity component.                          
                                                                      
#. Subtype 3:                                                   
                                                                      
- Sliding-window Lagrange interpolation of quaternions and       
  angular velocity. Attitude and angular velocity are represented by  
  a series of 7-element \``packets'' and associated time tags. The    
  time tags may be unequally spaced. Each packet contains four        
  quaternion components and three angular velocity components. A      
  quaternion representing attitude at a request time is derived by    
  using Lagrange interpolation on each quaternion component, where    
  the values to be interpolated are obtained for a consecutive series 
  of epochs centered at the request time. The interpolated quaternion 
  is then unitized. Angular velocity is obtained by using Lagrange    
  interpolation on each angular velocity component. The attitude and  
  angular velocity resulting from this interpolation method are in    
  principle independent. The same interpolation degree is used for    
  each quaternion and angular velocity component.                     
                                                                      
The sliding-window interpolation technique used by this data type     
works as follows: for any request epoch, the data type defines a      
component of a quaternion or angular velocity by interpolating a set  
of values of that component defined on a set of consecutive time      
tags---a "window"---centered as closely as possible to the request    
epoch. The nominal window size is dictated by the degree and type     
(Hermite vs Lagrange) of the interpolating polynomials. Normally the  
window of time tags has even size, and the window is selected so that 
the request time is located on or between the two central time tags   
in the window.                                                        
If the request time coincides with a time tag, the window may be      
positioned so that either of the central time tags of the window      
matches the request time. The Lagrange and Hermite interpolation      
algorithms will produce only round-off level differences between the  
results obtained from either choice, provided the input data are      
suitable for interpolation.                                           
                                                                      
When the request time is near a segment or interpolation interval     
boundary, the window is truncated if necessary on the side closest to 
the boundary. If a segment or interpolation interval contains too few 
packets to form a window of nominal size, a window will be            
constructed from the all of the available packets that lie within the 
nominal window location. In this case the window size may be odd. In  
any case the window never includes more than WNDSIZ/2 time tags on    
either side of the request time, where WNDSIZ is the nominal window   
size.                                                                 
                                                                      
Regarding interpolation intervals: the pointing time tags in a type 5 
segment are partitioned into groups within which polynomial           
interpolation between adjacent groups of WNDSIZ pointing instances is 
valid. Since the pointing instances in a segment are ordered with     
respect to time, these groups can be thought of as representing       
intervals of time over which the pointing of the spacecraft (or a     
spacecraft instrument or structure) is given continuously. Therefore, 
in the description that follows, these groups of pointing instances   
will be referred to as interpolation intervals.                       
                                                                      
All of the pointing instances in the segment must be ordered by       
encoded spacecraft clock time and must belong to one and only one     
interpolation interval. The intervals must begin and end at times for 
which there are pointing instances in the segment. The CK software    
that evaluates the data in the segment does not extrapolate pointing  
past the bounds of the intervals.                                     
                                                                      
A user's view of the time coverage provided by a type 5 segment can   
be viewed pictorially as follows:                                     
                                                                      
::                                                                    
                                                                      
                                                                      
                                                                      
    pointing instances:     0-0-0-0-0----0-0-0-0-0-----0------0-0-0-0 
                                                                      
                            |       |    |       |     |      |     | 
                                                                      
    interval bounds:       BEG      |   BEG      |    BEG    BEG    | 
                                                                      
                                  END          END   END          END 
                                                                      
                                                                      
In the above picture, the zeros indicate the times associated with    
the discrete pointing instances and the vertical bars show the bounds 
of the interpolation intervals that they are partitioned into. Note   
that the intervals begin and end at times associated with pointing    
instances. Also note that intervals consisting of just a single       
pointing instance are allowed.                                        
When pointing is desired for a time that is within the bounds of one  
of the intervals, the CK reader functions return interpolated         
pointing at the request time. In the example below, the pointing      
request time is indicated by SCLKDP and the user supplied tolerance   
is given by TOL. In this example the tolerance argument of the CK     
readers could be set to zero and pointing would still be returned.    
                                                                      
::                                                                    
                                                                      
                                        SCLKDP    TOL                 
                                             \   /                    
                                              | |                     
                                              |/ \                    
                                          [---+---]                   
                                          .   .   .                   
                                          .   .   .                   
                                                                      
    pointing instances:     0-0-0-0-0----0-0-0-0-0-----0------0-0-0-0 
                                                                      
                            |       |    |  ^    |     |      |     | 
                                                                      
    interval bounds:       BEG      |   BEG |    |    BEG    BEG    | 
                                                                      
                                  END      |   END   END          END 
                                              |                       
               CK reader returns interpolated pointing at this time.  
                                                                      
When a request time falls in a gap between intervals, no              
extrapolation is performed. Instead, pointing is returned for the     
interval endpoint closest to the request time, provided that time is  
within the user supplied tolerance. In this example if the tolerance  
were set to zero no pointing would be returned.                       
::                                                                    
                                                                      
                                               SCLKDP                 
                                                    \   TOL           
                                                     | /              
                                                     |/\              
                                                 [---+---]            
                                                 .   .   .            
                                                 .   .   .            
                                                                      
    pointing instances:     0-0-0-0-0----0-0-0-0-0-----0------0-0-0-0 
                                                                      
                            |       |    |       |     |      |     | 
                                                                      
    interval bounds:       BEG      |   BEG      |    BEG    BEG    | 
                                                                      
                                  END          END   END          END 
                                                   ^                  
                                                   |                  
                                   CK reader returns this instance.   
                                                                      
The physical structure of the data stored in a type 5 segment is as   
follows:                                                              
::                                                                    
                                                                      
      +-----------------------+                                       
      | Packet 1              |                                       
      +-----------------------+                                       
      | Packet 2              |                                       
      +-----------------------+                                       
                  .                                                   
                  .                                                   
                  .                                                   
      +-----------------------+                                       
      | Packet N              |                                       
      +-----------------------+                                       
      | Epoch 1               |                                       
      +-----------------------+                                       
      | Epoch 2               |                                       
      +-----------------------+                                       
                  .                                                   
                  .                                                   
                  .                                                   
      +----------------------------+                                  
      | Epoch N                    |                                  
      +----------------------------+                                  
      | Epoch 100                  | (First directory)                
      +----------------------------+                                  
                  .                                                   
                  .                                                   
                  .                                                   
      +----------------------------+                                  
      | Epoch ((N-1)/100)*100      | (Last directory)                 
      +----------------------------+                                  
      | Start time 1               |                                  
      +----------------------------+                                  
      | Start time 2               |                                  
      +----------------------------+                                  
                  .                                                   
                  .                                                   
                  .                                                   
      +----------------------------+                                  
      | Start time NUMINT          |                                  
      +----------------------------+                                  
      | Start time 100             | (First interval start            
      +----------------------------+  time directory)                 
                  .                                                   
                  .                                                   
                  .                                                   
      +----------------------------+                                  
      | Start ((NUMINT-1)/100)*100 | (Last interval start             
      +----------------------------+  time directory)                 
      | Seconds per tick           |                                  
      +----------------------------+                                  
      | Subtype code               |                                  
      +----------------------------+                                  
      | Window size                |                                  
      +----------------------------+                                  
      | Number of interp intervals |                                  
      +----------------------------+                                  
      | Number of packets          |                                  
      +----------------------------+                                  
                                                                      
In the discussion that follows let N be the number of pointing        
instances in the segment and let NUMINT be the number of intervals    
into which the pointing instances are partitioned.                    
The first part of a segment contains N packets (pointing records)     
which are ordered with respect to increasing time. Depending the      
segment subtype, a type 5 packet contains from four to fourteen d.p.  
numbers.                                                              
                                                                      
Following the pointing data are the N times associated with the       
pointing instances. These times are in encoded SCLK form and should   
be strictly increasing.                                               
                                                                      
Immediately following the last time is a very simple directory of the 
SCLK times. The directory contains INT( (N-1) / 100 ) entries. The    
Ith directory entry contains the (I*100)th SCLK time. Thus,           
                                                                      
::                                                                    
                                                                      
      Directory(1) = SCLKDP(100)                                      
                                                                      
      Directory(2) = SCLKDP(200)                                      
                                                                      
      .                                                               
      .                                                               
      .                                                               
                                                                      
If there are 100 or fewer entries, there is no directory. The         
directory is used to narrow down searches for pointing records to     
groups of 100 or less.                                                
Next are the NUMINT start times of the intervals that the pointing    
instances are partitioned into. These times are given in encoded      
spacecraft clock and must be strictly increasing. They must also be   
equal to times for which there are pointing instances in the segment. 
Note that the interval stop times are not stored in the segment. They 
are not needed because the stop time of the Ith interval is simply    
the time associated with the pointing instance that precedes the      
start time of the (I+1)th interval.                                   
                                                                      
Following the interval start times is a directory of these times.     
This directory is constructed in a form similar to the directory for  
the times associated with the pointing instances. The start times     
directory contains INT ( (NUMINT-1) / 100 ) entries and contains      
every 100th start time. Thus:                                         
                                                                      
::                                                                    
                                                                      
      Directory(1) = START(100)                                       
                                                                      
      Directory(2) = START(200)                                       
                                                                      
      .                                                               
      .                                                               
      .                                                               
                                                                      
Finally, the last five words in the segment are:                      
                                                                      
- The nominal rate for the spacecraft clock associated with    
  this kernel, given in seconds/tick.                                 
                                                                      
- The CK type 5 subtype code.                                  
                                                                      
- The interpolation window size                                
                                                                      
- the total number of interpolation intervals (NUMINT)         
                                                                      
- The total number of packets (pointing instances) (N) in the  
  segment.                                                            
                                                                      
A segment writer function is provided which calls the low level DAF   
functions necessary to write a type 5 segment to a C-kernel. However, 
the creator of the segment is responsible for determining whether or  
not it is valid to interpolate between contiguous ranges of pointing  
instances, and thus how they should be partitioned into intervals.    
See the header of the function :py:meth:`~spiceypy.spiceypy.ckw05`   
for a complete description of the inputs required to write a segment. 
|                                                         
                                                                      
Type 5 functions                                          
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| There are several CK functions that support data type 5. Their      
  names and functions are:                                            
                                                                      
:py:meth:`~spiceypy.spiceypy.ckw05`                                  
   writes a type 5 segment to a file.                                 
                                                                      
**ckr05\_**                                                           
   reads a pointing record from a type 5 segment that satisfies a     
   request for pointing at a given time.                              
                                                                      
**cke05\_**                                                           
   evaluates the record supplied by CKR05.                            
                                                                      
**cknr05\_**                                                          
   gives the number of pointing instances in a type 5 segment.        
                                                                      
**ckgr05\_**                                                          
   gets the Ith pointing instance from a type 5 segment.              
                                                                      
                                                
                                                                      
Type 6: ESOC/DDID Piecewise Interpolation                 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| CK type 6 has been provided to support accurate duplication by the  
  SPICE CK subsystem of spacecraft attitude data used by the European 
  Space Agency (ESA) on the Mars Express, Rosetta, SMART-1 and Venus  
  Express missions.                                                   
                                                                      
CK type 6 is an enhanced version of CK type 5. Type 6 enables         
creation of CK files representing the same attitude data that can be  
represented using type 5, but containing far fewer segments. Data     
from multiple type 5 segments can be stored in a single type 6        
segment, as long as the type 5 segments satisfy certain restrictions: 
                                                                      
- The type 5 segments are for the same reference frame (for an 
  instrument or spacecraft structure) and have the same base frame.   
                                                                      
- All of the type 5 segments contain angular velocity data, or 
  none do.                                                            
                                                                      
- The type 5 segments' descriptor coverage intervals, when     
  arranged in increasing time order, overlap at, and only at, their   
  endpoints.                                                          
                                                                      
- Each type 5 segment contains no gaps, or has a single gap to 
  the right of its last pointing instance.                            
                                                                      
                                                
                                                                      
Terminology                                               
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| In this section of the document, \``pointing'' is a synonym for     
  \``attitude'' or \``orientation.''                                  
                                                                      
A \``packet'' is a set of data representing pointing for a given      
time. Such a set is also referred to as a \``pointing instance.''     
                                                                      
Times associated with packets are variously called \``times,''        
\``epochs,'' or \``time tags.'' Time tags represent the independent   
variable of attitude data: they are times at which the associated     
data are applicable.                                                  
                                                                      
All times, unless otherwise indicated, are encoded spacecraft clock   
values, also called \``ticks.''                                       
                                                                      
Mini-segment time coverage bounds are also called \``boundaries.''    
                                            
                                                                      
Mini-segments                                             
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| Within a type 6 segment, each set of data corresponding to a type 5 
  segment is called a \``mini-segment.'' A type 6 segment contains    
  one or more mini-segments.                                          
                                                                      
The mini-segments of a type 6 segment need not use the same packet    
counts, subtypes, clock rates, or interpolation degrees.              
                                                                      
The time coverage of a mini-segment is called a \``mini-segment       
interval.'' The mini-segment intervals of a type 6 segment have no    
intervening gaps (gaps may occur only within mini-segment intervals)  
and overlap only at single points. The stop time of each mini-segment 
interval is the start time of the next. The start time of a type 6    
segment is greater than (later than) or equal to the start time of    
the first interval, and the segment's stop time is less than (earlier 
than) or equal to the stop time of the last interval.                 
                                                                      
Mini-segment intervals must have strictly positive length.            
                                                                      
An example of the relationship between the time coverage of a type 6  
segment and that of its mini-segments is shown below:                 
                                                                      
::                                                                    
                                                                      
      mini-segment interval bounds:  |----------|----|--------|-|--|  
      segment bounds:                  [                           ]  
                                                                      
Each mini-segment contains a time ordered, strictly increasing        
sequence of epochs (no two epochs of the same mini-segment may        
coincide) and an associated sequence of attitude data sets called     
\``packets.'' The epoch associated with a packet is also called a     
\``time tag.'' The composition of a packet depends on the subtype of  
the mini-segment to which the packet belongs; subtypes are discussed  
in more detail below.                                                 
The start time of each mini-segment interval must be greater than or  
equal to the first member of the corresponding time tag sequence. The 
stop time of each mini-segment interval must be greater than the      
interval's start time and is allowed to exceed the last member of the 
mini-segment's time tag sequence. Thus a mini-segment interval can    
have a coverage gap between its last time tag and its stop time.      
There cannot be a gap between a mini-segment interval's stop time and 
the start time of the next mini-segment interval.                     
                                                                      
The interpolation interval associated with a mini-segment is the time 
interval over which the mini-segment can satisfy a pointing request.  
The interpolation interval extends from the start time of the         
corresponding \``mini-segment interval'' to the minimum of the stop   
time of the mini-segment interval and the last time tag of the        
mini-segment's time tag sequence.                                     
                                                                      
Mini-segments may contain optional \``padding'' time tags and packets 
beyond both ends of their coverage intervals. Padding time tags on    
the left of a mini-segment interval are less than the interval start  
time; padding time tags on the right exceed the interval stop time.   
Padding enables control of interpolation behavior at and near         
mini-segment interval boundaries. Within a mini-segment, padding      
cannot occur to the right of a gap. Padding does not contribute to a  
mini-segment's time coverage.                                         
                                                                      
The relationships between the time coverage of a mini-segment (the    
\``mini-segment interval''), the time tags of the pointing instances  
it contains, and the mini-segment's interpolation interval are shown  
below.                                                                
                                                                      
In the following diagrams, zeros represent pointing instances,        
hyphens represent time periods over which pointing data can be used   
as inputs for interpolation (this includes padding), and blank areas  
represent coverage gaps.                                              
                                                                      
Mini-segment interval without padding:                                
                                                                      
::                                                                    
                                                                      
                                                                      
    pointing instances:              0-0-0--0-0-0-0-0---0-0-0---0-0-0 
                                                                      
    mini-segment interval bounds:    |                              | 
                                                                      
    interpolation interval bounds:   ^                              ^ 
                                                                      
                                                                      
Mini-segment interval with padding on both sides:                     
::                                                                    
                                                                      
                                                                      
    pointing instances:              0-0-0--0-0-0-0-0---0-0-0---0-0-0 
      mini-segment interval bounds:          |                    |   
      interpolation interval bounds:         ^                    ^   
                                                                      
Note that when padding is present, mini-segment interval bounds need  
not coincide with time tags of pointing instances.                    
Mini-segment interval with left-side padding and with a gap:          
                                                                      
::                                                                    
                                                                      
      pointing instances:              0-0-0--0-0-0-0-0---0-0         
      mini-segment interval bounds:          |                    |   
      interpolation interval bounds:         ^              ^         
                                                                      
Padding within or beyond a gap is not supported:                      
::                                                                    
                                                                      
                                                                      
                                                          not allowed 
                                                               v v v  
      pointing instances:            0-0-0--0-0-0-0-0---0-0    0-0-0  
      mini-segment interval bounds:      |                     |      
      interpolation interval bounds:     ^                ^           
                                                                      
                                                                      
                      last "usable" time tag -------+                 
                                                    | not allowed     
                                                      v v v           
      pointing instances:            0-0-0--0-0-0-0-0-0-0-0           
      mini-segment interval bounds:      |                     |      
      interpolation interval bounds:     ^          ^                 
                                                                      
The use of padding is discussed in greater detail below.              
When type 6 data are interpolated to produce an attitude instance for 
a given request time, if the look-up tolerance is zero, only data     
from a single mini-segment whose interval contains the request time   
are used.                                                             
                                                                      
When a request time coincides with the boundary between two           
mini-segment intervals, there is a choice as to which interval will   
provide attitude data. The creator of a type 6 segment can control    
this behavior via a parameter passed to the type 6 segment writer     
ckw06\_; this parameter is called the interval selection flag. For a  
given type 6 segment, depending on the value of this flag, either the 
earlier interval is always selected, or the later interval is always  
selected:                                                             
                                                                      
::                                                                    
                                                                      
      Pointing request time:                       |                  
                                                                      
                                                                      
      mini-segment interval n:       0-0-0-0-0-0-0-0-0-0-0            
      mini-segment interval n+1:                 @-@-@-@-@-@-@-@-@-@  
      mini-segment interval bounds:   |            |             |    
                                                                      
In the case depicted by the above diagram, if the interval selection  
flag is set to "true," pointing will be selected from interval n+1;   
if the flag is "false," pointing will be selected from interval n.    
|                                                         
                                                                      
Type 6 subtypes                                           
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| Because of the possibility of evolution of the mathematical         
  representations of attitude used by ESA, CK type 6 is designed to   
  accommodate multiple representations of attitude data, thereby      
  avoiding a proliferation of CK data types. CK type 6 refers to each 
  supported mathematical representation of attitude data as a         
  \``subtype.''                                                       
                                                                      
Currently CK type 6 supports four subtypes:                           
                                                                      
- Subtype 0:                                                   
                                                                      
- Sliding-window Hermite interpolation of quaternions and        
  quaternion derivatives. Attitude and angular velocity are           
  represented by a sequence of 8-element \``packets'' and associated  
  time tags. The time tags may be unequally spaced. Each packet       
  contains four quaternion components followed by four quaternion     
  time derivative components. A quaternion representing attitude at a 
  request time is derived by using Hermite interpolation on each      
  quaternion component and the corresponding derivative, where the    
  values to be interpolated are obtained for a consecutive sequence   
  of time tags centered at the request time, and converting the       
  result to unit length. Angular velocity is derived from the unit    
  quaternion and its derivative with respect to time. The same        
  interpolation degree is used for each quaternion component.         
                                                                      
- Subtype 1:                                                   
                                                                      
- Sliding-window Lagrange interpolation of quaternions. Attitude 
  is represented by a sequence of 4-element \``packets'' and          
  associated time tags. The time tags may be unequally spaced. Each   
  packet contains four quaternion components. A quaternion            
  representing attitude at a request time is derived by using         
  Lagrange interpolation on each quaternion component, where the      
  values to be interpolated are obtained for a consecutive sequence   
  of time tags centered at the request time. The interpolated         
  quaternion is then unitized. The same interpolation degree is used  
  for each quaternion component.                                      
                                                                      
- Angular velocity is computed from the unit-length quaternion   
  and its time derivative. The derivative is computed using the       
  derivatives of the interpolating polynomials.                       
                                                                      
- Subtype 2:                                                   
                                                                      
- Sliding-window Hermite interpolation of quaternions and        
  angular velocity. Attitude and angular velocity are represented by  
  a sequence of 14-element \``packets'' and associated time tags. The 
  time tags may be unequally spaced. Each packet contains four        
  quaternion components, four quaternion derivative components, three 
  angular velocity components, and three angular acceleration         
  components. A quaternion representing attitude at a request time is 
  derived by using Hermite interpolation on each quaternion component 
  and the corresponding derivative, where the values to be            
  interpolated are obtained for a consecutive sequence of time tags   
  centered at the request time. The interpolated quaternion is then   
  unitized. Angular velocity is obtained by using Hermite             
  interpolation on each angular velocity component and the            
  corresponding derivative. The attitude and angular velocity         
  resulting from this interpolation method are in principle           
  independent. The same interpolation degree is used for each         
  quaternion and angular velocity component.                          
                                                                      
- Subtype 3:                                                   
                                                                      
- Sliding-window Lagrange interpolation of quaternions and       
  angular velocity. Attitude and angular velocity are represented by  
  a sequence of 7-element \``packets'' and associated time tags. The  
  time tags may be unequally spaced. Each packet contains four        
  quaternion components and three angular velocity components. A      
  quaternion representing attitude at a request time is derived by    
  using Lagrange interpolation on each quaternion component, where    
  the values to be interpolated are obtained for a consecutive        
  sequence of time tags centered at the request time. The             
  interpolated quaternion is then unitized. Angular velocity is       
  obtained by using Lagrange interpolation on each angular velocity   
  component. The attitude and angular velocity resulting from this    
  interpolation method are in principle independent. The same         
  interpolation degree is used for each quaternion and angular        
  velocity component.                                                 
                                                                      
The sliding-window interpolation techniques used by data type 6 work  
as follows: for any request epoch, the interpolation algorithm        
computes a component of a quaternion or angular velocity by           
interpolating a set of values of that component defined on a set of   
consecutive time tags---a "window"---centered as closely as possible  
to the request epoch. The nominal window size is dictated by the      
degree and type (Hermite vs Lagrange) of the interpolating            
polynomials. Normally the window of time tags has even size, and the  
window is selected so that the request time is located between the    
two central time tags in the window.                                  
If the request time coincides with a time tag, the window may be      
positioned so that either of the central time tags of the window      
matches the request time. The Lagrange and Hermite interpolation      
algorithms will produce only round-off level differences between the  
results obtained from either choice, provided the input data are      
suitable for interpolation.                                           
                                                                      
In CK type 6, mini-segment interval boundaries affect interpolation   
in the same way that segment boundaries affect type 5 interpolation.  
When the request time is near a mini-segment boundary, the window is  
truncated if necessary on the side closest to the boundary. If        
mini-segment interval, including padding, contains too few packets to 
form a window of nominal size, as many packets as are needed and      
available are used to construct the window. In this case the window   
size may be odd. In any case the window never includes more than      
WNDSIZ/2 time tags on either side of the request time, where WNDSIZ   
is the nominal window size.                                           
                                            
                                                                      
Restrictions on type 6 data                               
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| All data used in type 6 segments must be suitable for use by the    
  interpolation algorithms associated with the subtypes selected by   
  the CK creator. In general, adjacent pointing instances must        
  represent attitudes that do not differ greatly; otherwise           
  polynomial interpolation of quaternions will tend to yield invalid  
  results.                                                            
                                                                      
In addition, quaternion data for subtypes 0 and 2 must have signs     
chosen so that large variations between successive values of any      
quaternion element do not occur. For any attitude represented by a    
quaternion Q, the quaternion -Q represents the same attitude. But     
only one of these choices can be \``near'' the previous quaternion P  
in the mini-segment containing Q, in the Euclidean norm sense.        
                                                                      
Quaternion signs must be selected so that the elements of adjacent    
quaternions are always \``near'' each other, and quaternion           
derivatives must be consistent with the selected quaternions.         
                                                                      
Subtypes 1 and 3 do not have quaternion sign restrictions; the        
interpolation algorithms for these subtypes adjust quaternion signs   
at run time if necessary. These subtypes do require that the          
attitudes represented by adjacent quaternions be \``close'' to each   
other: if adjacent quaternions are converted to rotation matrices,    
the matrices must be close to each other.                             
                                            
                                                                      
Type 6 segment structure                                  
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| Below we first describe the overall type 6 segment structure, then  
  we cover the mini-segment structure.                                
                                                                      
Type 6 CK segments have the structure shown below:                    
                                                                      
::                                                                    
                                                                      
      +---------------------------------------+                       
      | Mini-segment 1                        |                       
      +---------------------------------------+                       
            .                                                         
            .                                                         
            .                                                         
      +---------------------------------------+                       
      | Mini-segment N                        |                       
      +---------------------------------------+                       
      | Mini-segment interval 1 start time    |                       
      +---------------------------------------+                       
            .                                                         
            .                                                         
            .                                                         
      +---------------------------------------+                       
      | Mini-segment interval N start time    |                       
      +---------------------------------------+                       
      | Mini-segment interval N stop time     |                       
      +---------------------------------------+                       
      | Mini-seg. interval start time 100     | (First interval       
      +---------------------------------------+  directory)           
            .                                                         
            .                                                         
            .                                                         
      +---------------------------------------+                       
      | Mini-seg. ival. start time (N/100)*100| (Last interval        
      +---------------------------------------+  directory)           
      | Mini-segment 1 start pointer          |                       
      +---------------------------------------+                       
            .                                                         
            .                                                         
            .                                                         
      +---------------------------------------+                       
      | Mini-segment N start pointer          |                       
      +---------------------------------------+                       
      | Mini-segment N stop pointer + 1       |                       
      +---------------------------------------+                       
      | Interval selection flag               |                       
      +---------------------------------------+                       
      | Number of intervals                   |                       
      +---------------------------------------+                       
                                                                      
In the diagram above, each box labeled as a mini-segment represents a 
data structure; the format of these data structures is described      
below. The other boxes represent individual double precision numbers. 
The mini-segments themselves form the initial portion of the segment. 
                                                                      
The array of mini-segment interval time bounds contains the start     
time of each mini-segment interval, plus the stop time of the final   
interval.                                                             
                                                                      
The list of mini-segment interval time bounds has its own directory,  
which has the same structure as the time tag directories of type 5    
segments. As with time tag directories, the mini-segment interval     
boundary directory contains boundary times whose indices are          
multiples of 100, except that if N+1 is a multiple of 100, the last   
boundary time is not included.                                        
                                                                      
The array of mini-segment pointers contains a pointer to the start of 
each mini-segment, plus a final \``stop'' pointer for the final       
mini-segment. The stop pointer points to the location immediately     
following the last address of the final mini-segment.                 
                                                                      
The mini-segment pointers are offsets relative to the start address   
of the segment. Each start pointer, when added to the segment's start 
address, yields the address of the first item in the corresponding    
mini-segment.                                                         
                                                                      
Following the mini-segment pointers is the interval selection flag.   
When this flag has the value 1, the later interpolation interval is   
used when a request time falls on the common boundary between two     
interpolation intervals. If the selection flag is 0, the earlier      
interval is used.                                                     
                                                                      
The structure of a type 6 CK mini-segment is similar to the structure 
of a type 5 CK segment, except that a type 6 mini-segment contains no 
array of interpolation interval start times, and hence no directory   
for interpolation interval start times. The CK type 6 mini-segment    
structure is as follows:                                              
                                                                      
::                                                                    
                                                                      
      +--------------------------+                                    
      | Packet 1                 |                                    
      +--------------------------+                                    
                  .                                                   
                  .                                                   
                  .                                                   
      +--------------------------+                                    
      | Packet M                 |                                    
      +--------------------------+                                    
      | Time tag 1               |                                    
      +--------------------------+                                    
                  .                                                   
                  .                                                   
                  .                                                   
      +--------------------------+                                    
      | Time tag M               |                                    
      +--------------------------+                                    
      | Time tag 100             | (First time tag directory)         
      +--------------------------+                                    
                  .                                                   
                  .                                                   
                  .                                                   
      +--------------------------+                                    
      | Time tag ((M-1)/100)*100 | (Last time tag directory)          
      +--------------------------+                                    
      | Clock rate (sec/tick)    |                                    
      +--------------------------+                                    
      | Subtype code             |                                    
      +--------------------------+                                    
      | Window size              |                                    
      +--------------------------+                                    
      | Number of packets        |                                    
      +--------------------------+                                    
                                                                      
In the mini-segment diagram, each box representing a packet           
corresponds to a set of PKTSIZ double precision numbers, where PKTSIZ 
depends on the mini-segment's subtype; the other boxes represent      
individual double precision numbers.                                  
The window size is related to the polynomial degree as shown:         
                                                                      
::                                                                    
                                                                      
      Subtypes 0,2:     WINDOW_SIZE = ( DEGREE + 1 ) / 2              
      Subtypes 1,3:     WINDOW_SIZE =   DEGREE + 1                    
                                                                      
Window sizes are required to be even; this imposes the interpolation  
degree restrictions                                                   
::                                                                    
                                                                      
      Subtypes 0,2: the degree is equivalent to 3 mod 4, i.e.,        
                    the degree is in the set { 3, 7, 11, ... }        
                                                                      
      Subtypes 1,3: the degree is odd                                 
                                                                      
The number of packets normally should be greater than or equal to the 
mini-segment's interpolation window size, but this is not a           
requirement. The packet count may not be less than 2.                 
The set of time tags is augmented by a sequence of directory entries; 
these entries allow the type 6 reader to search for time tags more    
efficiently. The directory entries contain time tags whose indices    
are multiples of 100. The set of indices of time tags stored in the   
directories ranges from 100 to                                        
                                                                      
::                                                                    
                                                                      
      (  (M-1) / 100  ) * 100                                         
                                                                      
where M is the total number of time tags. Note that if M is           
::                                                                    
                                                                      
      Q * 100                                                         
                                                                      
then only                                                             
::                                                                    
                                                                      
      Q - 1                                                           
                                                                      
directory entries are stored, and in particular, if there are only    
100 packets in the segment, there are no directories.                 
Following the time tag directory are four parameters associated with  
the mini-segment: the rate of the associated spacecraft clock, in     
units of seconds/tick, the subtype, the interpolation window size,    
and the packet count.                                                 
                                                                      
To facilitate the creation of type 6 segments, a segment writing      
function called ckw06_c has been provided. This function takes as     
input arguments the handle of an CK file that is open for writing,    
the information needed to construct the segment descriptor, the       
mini-segments' parameters, and the data to be stored in the segment.  
The header of the function provides a complete description of the     
input arguments and an example of its usage.                          
                                            
                                                                      
Use of non-zero tolerance                                 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| As with other CK types, type 6 segments can provide data for        
  request times outside of their interpolation intervals if a         
  positive tolerance value is used, and if the request time is within 
  the tolerance from the interpolation interval of some mini-segment. 
  If the tolerance permits, a request time that falls into a gap can  
  be satisfied by the closest of the last epoch of the mini-segment   
  whose coverage interval includes the request time, or by the        
  coverage start time of the next mini-segment, if there is one.      
  Requests outside of the segment's coverage interval can be          
  satisfied by data at the nearest endpoint of some mini-segment's    
  interpolation interval, if the tolerance permits it.                
                                                                      
When a non-zero tolerance value is used to look up data from a type 6 
segment, the algorithm for selecting data is not exactly the same as  
it would be for a sequence of type 5 segments corresponding to the    
type 6 segment's mini-segments.                                       
                                                                      
As described in the earlier section titled "The General Search        
Algorithm," if each mini-segment were replaced with a type 5 segment, 
it would be possible for a later segment to take precedence over an   
earlier one, even if the earlier segment had no coverage gap, if a    
request time were outside of the coverage interval of the higher      
priority segment but within the tolerance of the higher priority      
segment's coverage interval.                                          
                                                                      
This precedence effect cannot occur between two mini-segments of the  
same type 6 segment. Specifically, it is not possible for a           
mini-segment to provide data to satisfy a pointing request when the   
request time outside of its coverage interval and is in the           
interpolation interval (and hence not in a gap) of a different        
mini-segment of the same type 6 segment.                              
                                                                      
This difference is highly unlikely to affect users of type 6 CK       
segments.                                                             
                                            
                                                                      
Type 6 functions                                          
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| There are several CK functions that support data type 6. Their      
  names and functions are:                                            
                                                                      
**ckw06_c**                                                           
   writes a type 6 segment to a file.                                 
                                                                      
**ckr06\_**                                                           
   reads a pointing record from a type 6 segment that satisfies a     
   request for pointing at a given time.                              
                                                                      
**cke06\_**                                                           
   evaluates the record supplied by CKR06.                            
                                                                      
**cknm06\_**                                                          
   gives the number of mini-segments in a specified type 6 segment.   
                                                                      
**ckmp06\_**                                                          
   returns mini-segment parameters, including packet count, for       
   specified mini-segment in a type 6 segment.                        
                                                                      
**ckgr06\_**                                                          
   gets the Ith pointing instance from a specified mini-segment in a  
   type 6 segment.                                                    
                                                                      
                                                
                                                                      
Appendix A --- Summary of C-kernel Functions              
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                    
                                                                      
Summary of Mnemonics                                      
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| Each C-kernel function name consists of a mnemonic which translates 
  into a short description of the function's purpose. Those beginning 
  with \```ck''' are names of functions that deal solely with         
  C-kernel files. The other functions provide support that is not     
  necessarily C-kernel specific.                                      
                                                                      
::                                                                    
                                                                      
         Kernel Loading/Unloading Routines                            
                                                                      
                                                                      
  furnsh_c       ( Load kernel file of any type                     ) 
                                                                      
  unload_c       ( Unload kernel file of any type                   ) 
                                                                      
                                                                      
         C-kernel Routines                                            
                                                                      
                                                                      
            Wrappers                                                  
                                                                      
      ckcls_c   ( C-kernel, close a pointing file                  )  
      ckcov_c   ( C-kernel, coverage for an instrument             )  
      ckgp_c    ( C-kernel, get pointing                           )  
      ckgpav_c  ( C-kernel, get pointing and angular velocity      )  
      cklpf_c   ( C-kernel, load pointing file                     )  
      ckobj_c   ( C-kernel, instruments in a file                  )  
      ckopn_c   ( C-kernel, open a new pointing file               )  
      ckupf_c   ( C-kernel, unload pointing file                   )  
      ckw01_c   ( C-kernel, write segment to C-kernel, data type 1 )  
      ckw02_c   ( C-kernel, write segment to C-kernel, data type 2 )  
      ckw03_c   ( C-kernel, write segment to C-kernel, data type 3 )  
      ckw05_c   ( C-kernel, write segment to C-kernel, data type 5 )  
                                                                      
            Lower-level functions                                     
                                                                      
      ckbss_    ( C-kernel, begin search for segment               )  
      cke01_    ( C-kernel, evaluate pointing record, data type 1  )  
      cke02_    ( C-kernel, evaluate pointing record, data type 2  )  
      cke03_    ( C-kernel, evaluate pointing record, data type 3  )  
      cke04_    ( C-kernel, evaluate pointing record, data type 4  )  
      cke05_    ( C-kernel, evaluate pointing record, data type 5  )  
      cke06_    ( C-kernel, evaluate pointing record, data type 6  )  
      ckgr01_   ( C-kernel, get record, data type 1                )  
      ckgr02_   ( C-kernel, get record, data type 2                )  
      ckgr03_   ( C-kernel, get record, data type 3                )  
      ckgr04_   ( C-kernel, get record, data type 4                )  
      ckgr05_   ( C-kernel, get record, data type 5                )  
      ckgr06_   ( C-kernel, get record, data type 6                )  
      ckmp06_   ( C-kernel, get mini-segment params, data type 6   )  
      cknm06_   ( C-kernel, get mini-segment count, data type 6    )  
      cknr01_   ( C-kernel, number of records, data type 1         )  
      cknr02_   ( C-kernel, number of records, data type 2         )  
      cknr03_   ( C-kernel, number of records, data type 3         )  
      cknr04_   ( C-kernel, number of records, data type 4         )  
      cknr05_   ( C-kernel, number of records, data type 5         )  
      ckpfs_    ( C-kernel, pointing from segment                  )  
      ckr01_    ( C-kernel, read pointing record, data type 1      )  
      ckr02_    ( C-kernel, read pointing record, data type 2      )  
      ckr03_    ( C-kernel, read pointing record, data type 3      )  
      ckr04_    ( C-kernel, read pointing record, data type 4      )  
      ckr04_    ( C-kernel, read pointing record, data type 5      )  
      cksns_    ( C-kernel, select next segment                    )  
      ckw04a_   ( C-kernel, add to a Type 4 segment                )  
      ckw04b_   ( C-kernel, begin a Type 4 segment                 )  
      ckw04e_   ( C-kernel, end a Type 4 segment                   )  
      ckw06_    ( C-kernel, write segment to C-kernel, data type 6 )  
                                                                      
         SCLK conversion functions                                    
                                                                      
      scdecd_c       ( Decode spacecraft clock                )       
      scencd_c       ( Encode spacecraft clock                )       
      scpart_c       ( Spacecraft clock partitions            )       
      scfmt_c        ( Spacecraft clock format                )       
      sctiks_c       ( Spacecraft clock ticks                 )       
      sct2e_c        ( Convert encoded SCLK Ticks to ET       )       
      scs2e_c        ( Convert SCLK String to ET              )       
      sce2c_c        ( Convert ET to continuous SCLK Ticks    )       
      sce2t_c        ( Convert ET to encoded SCLK Ticks       )       
      sce2s_c        ( Convert ET to SCLK String              )       
                                                                      
      utc2et_c       ( UTC to Ephemeris Time                  )       
      et2utc_c       ( Ephemeris Time to UTC                  )       
                                                                      
                                                                      
         Inertial Reference frame functions                           
                                                                      
      irfrot_        ( Inertial reference frame, rotate      )        
      irfnum_        ( Inertial reference frame number       )        
      irfnam_        ( Inertial reference frame name         )        
      irfdef_        ( Inertial reference frame, default     )        
                                                                      
                                                
                                                                      
Summary of Calling Sequences                              
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
                                                                      
::                                                                    
                                                                      
             Kernel Loading/Unloading Routines                        
                                                                      
                                                                      
  furnsh_c ( fname                                                  ) 
                                                                      
  unload_c ( fname                                                  ) 
                                                                      
             C-kernel Routines                                        
                                                                      
               Wrappers                                               
                                                                      
                                                                      
  ckcls_c  ( handle                                                 ) 
                                                                      
  ckcov_c  ( fname,  idcode, needav, level,  tol,  timsys,  cover   ) 
                                                                      
  ckgp_c   ( inst,   sclkdp, tol,    ref,    cmat, &clkout, &found  ) 
                                                                      
   ckgpav_c ( inst,   sclkdp, tol,    ref,    cmat,   av,    &clkout, 
                                                                      
             &found                                                 ) 
                                                                      
  cklpf_c  ( fname, &handle                                         ) 
                                                                      
  ckobj_c  ( fname,  ids                                            ) 
                                                                      
  ckopn_c  ( fname,  ifname, ncomch, &handle                        ) 
                                                                      
  ckupf_c  (         handle                                         ) 
      ckw01_c  ( handle, begtim, endtim, inst,   ref,  avflag, segid, 
                                                                      
             nprec,  sclkdp, quats,  avvs                           ) 
                                                                      
     ckw02_c  ( handle, begtim, endtim, inst,   ref,   segid,  nprec, 
                                                                      
             start,  stop,   quats,  avvs,   rates                  ) 
                                                                      
     ckw03_c  ( handle, begtim, endtim, inst,   ref,   avflag, segid, 
                                                                      
             nprec,  sclkdp, quats,  avvs,   nints, starts          ) 
      ckw05_c  ( handle, subtyp, degree, begtim, endtim, inst,   ref, 
                                                                      
             avflag, segid,  nprec,  sclkdp, packts, nints,  starts ) 
                                                                      
                                                                      
               Lower-level functions                                  
                                                                      
                                                                      
    ckbss_  ( inst,    sclkdp, tol,    needav                       ) 
                                                                      
    cksns_  ( handle,  descr,  segid,  &found, SIDLEN               ) 
      ckpfs_  ( handle,  descr,  sclkdp, tol,    needav, cmat, av,    
                                                                      
              &clkout, &found                                       ) 
      ckr01_  ( handle,  descr,  sclkdp, tol,    needav, record,      
                                                                      
              &found                                                ) 
                                                                      
    cke01_  ( needav,  record, cmat,   av,     &clkout              ) 
                                                                      
    cknr01_ ( handle,  descr,  &nprec                               ) 
                                                                      
    ckgr01_ ( handle,  descr,  recno,  record                       ) 
                                                                      
    ckr02_  ( handle,  descr,  sclkdp, tol,    record, &found       ) 
                                                                      
    cke02_  ( needav,  record, cmat,   av,     &clkout              ) 
                                                                      
    cknr02_ ( handle,  descr,  &nprec                               ) 
                                                                      
    ckgr02_ ( handle,  descr,  recno,  record                       ) 
      ckr03_  ( handle,  descr,  sclkdp, tol,    needav, record,      
                                                                      
              &found                                                ) 
                                                                      
    cke03_  ( needav,  record, cmat,   av,     &clkout              ) 
                                                                      
    cknr03_ ( handle,  descr,  &nprec                               ) 
                                                                      
    ckgr03_ ( handle,  descr,  recno,  record                       ) 
                                                                      
    cke04_  ( needav,  record, cmat,   av,     &clkout              ) 
                                                                      
    ckgr04_ ( handle,  descr,  recno,  record                       ) 
                                                                      
    cknr04_ ( handle,  descr,  &nrec                                ) 
      ckr04_  ( handle,  descr,  sclkdp, tol,    needav, record,      
                                                                      
              &found                                                ) 
                                                                      
    ckw04a_ ( handle,  npkts,  pktsiz, pktdat, sclkdp               ) 
      ckw04b_ ( handle,  begtim, inst,   ref,    avflag, segid,       
                                                                      
              REFLEN,  SIDLEN                                       ) 
                                                                      
    ckw04e_ ( handle,  endtim                                       ) 
      ckr05_  ( handle,  descr,  sclkdp, tol,    needav, record,      
                                                                      
              &found                                                ) 
                                                                      
    cke05_  ( needav,  record, cmat,   av,     &clkout              ) 
                                                                      
    cknr05_ ( handle,  descr,  &nprec                               ) 
                                                                      
    ckgr05_ ( handle,  descr,  recno,  record                       ) 
      ckmp06_ ( handle,  descr,  msno,   &rate,  &subtyp, &winsiz,    
                                                                      
              &nrec,   ivlbds, &lstepc                              ) 
                                                                      
    cknm06_ ( handle,  descr,  &nmini                               ) 
                                                                      
    ckgr06_ ( handle,  descr,  msno,   recno,  record               ) 
                                                                      
    cke06_  ( needav,  record, cmat,   av,     &clkout              ) 
      ckr06_  ( handle,  descr,  sclkdp, tol,    needav, record,      
                                                                      
              &found                                                ) 
      ckw06_  ( handle,  inst,   ref,    avflag, first,  last,        
                segid,   nmini,  npkts,  subtps, degres, packts,      
                                                                      
              rates,   sclkdp, ivlbds, sellst, reflen, sidlen       ) 
                                                                      
             SCLK conversion functions                                
                                                                      
      scdecd_c ( sc,     sclkdp, lenout, sclkch         )             
      scencd_c ( sc,     sclkch, &sclkdp                )             
      scpart_c ( sc,     nparts, pstart, pstop          )             
      scfmt_c  ( sc,     ticks,  lenout, clkstr         )             
      sctiks_c ( sc,     clkstr, &ticks                 )             
      sct2e_c  ( sc,     sclkdp, &et                    )             
      scs2e_c  ( sc,     sclkch, &et                    )             
      sce2c_c  ( sc,     et,     &sclkdp                )             
      sce2t_c  ( sc,     et,     &sclkdp                )             
      sce2s_c  ( sc,     et,     lenout, sclkch         )             
                                                                      
      utc2et_c ( utcstr, &et                            )             
      et2utc_c ( et,     format, prec,  lenout, utcstr  )             
                                                                      
                                                                      
             Inertial Reference frame functions                       
                                                                      
      irfrot_ ( refa,   refb,   rotab  )                              
      irfnum_ ( name,   &index         )                              
      irfnam_ ( index,  name,   namlen )                              
      irfdef_ ( index                  )                              
                                                                      
                                                
                                                                      
Appendix B --- Example Program PLANET_POINT               
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| The following program shows how C-kernel functions fit together     
  with other CSPICE routines to solve a typical problem requiring     
  pointing data.                                                      
                                                                      
All of the functions used here are part of CSPICE or the ANSI C       
library.                                                              
                                                                      
::                                                                    
                                                                      
      /*                                                              
      PROGRAM PLANET_POINT                                            
                                                                      
                                                                      
         Compute the planetocentric latitude, longitude and radius of 
                                                                      
        the point at which the optic axis of an instrument intersects 
         the surface of a target planet. Assume that the axis of the  
         instrument is along the Z-axis of the instrument fixed       
         reference frame.                                             
                                                                      
         The following files are required:                            
                                                                      
            1) Kernel file containing planetary constants.            
            2) Kernel file containing spacecraft clock (SCLK) data.   
            3) SPK file containing planetary and spacecraft           
               ephemeris data.                                        
            4) CK file containing instrument pointing data.           
                                                                      
         The following quantities are required:                       
                                                                      
            1) NAIF integer spacecraft ID                             
            2) NAIF integer planet ID                                 
            3) NAIF integer instrument ID                             
            4) SCLK time string                                       
            5) SCLK tolerance.                                        
                                                                      
         The following steps are taken to locate the desired point:   
                                                                      
            1) The inertial pointing (VPNT) of the instrument at      
               the input SCLK time is read from the CK file.          
                                                                      
            2) The apparent position (VTARG) is computed for the      
               center of the target body as seen from the spacecraft, 
               at the ephemeris time (ET) corresponding to SCLK.      
                                                                      
               The one-way light time (TAU) from the target to the    
               spacecraft is also computed.                           
                                                                      
            3) The transformation (TIBF) from inertial to body-fixed  
               coordinates is computed for the epoch ET-TAU, using    
               quantities from the planetary constants kernel.        
                                                                      
            4) The radii (R) of the tri-axial ellipsoid used to model 
               the target body are extracted from the planetary       
               constants kernel.                                      
                                                                      
                                                                      
           5) The position of the observer, in body-fixed coordinates 
               is computed using VTARG and TIBF.                      
                                                                      
                                                                      
           6) VPNT is converted to body-fixed coordinates using TIBF. 
                                                                      
            7) The routine SURFPT computes the point of intersection, 
               given the two body-fixed positions, and tri-axial      
               ellipsoid radii.                                       
                                                                      
      -Particulars                                                    
                                                                      
          1) The instrument boresight is assumed to define the z-axis 
                                                                      
           of the instrument-fixed reference frame. This is reflected 
             in the choice of ( 0, 0, 1 ) as the boresight pointing   
             vector (VPNT) in instrument-fixed coordinates.           
                                                                      
      */                                                              
                                                                      
      #include <stdio.h>                                              
      #include <string.h>                                             
      #include "SpiceUsr.h"                                           
                                                                      
                                                                      
                                                                      
      int main()                                                      
      {                                                               
                                                                      
         /*                                                           
         Constants                                                    
                                                                      
         The inertial reference frame for all output.                 
         */                                                           
         #define   REF            "J2000"                             
                                                                      
         /*                                                           
         File name length.                                            
         */                                                           
         #define   FILSIZ         256                                 
                                                                      
         /*                                                           
         Body name length.                                            
         */                                                           
         #define   BDNMLN         37                                  
                                                                      
         /*                                                           
         SCLK string length.                                          
         */                                                           
         #define   TIMLEN         35                                  
                                                                      
         /*                                                           
         Instrument name length.                                      
         */                                                           
         #define   INNMLN         32                                  
         /*                                                           
         Local variables                                              
         */                                                           
         SpiceBoolean            found;                               
                                                                      
         SpiceChar               file      [ FILSIZ ];                
         SpiceChar               instch    [ INNMLN ];                
         SpiceChar               sclkch    [ TIMLEN ];                
         SpiceChar               scname    [ BDNMLN ];                
         SpiceChar               targname  [ BDNMLN ];                
         SpiceChar               tolch     [ TIMLEN ];                
                                                                      
         SpiceInt                inst;                                
         SpiceInt                n;                                   
         SpiceInt                sc;                                  
         SpiceInt                targ;                                
                                                                      
         SpiceDouble             clkout;                              
         SpiceDouble             cmat   [3][3];                       
         SpiceDouble             et;                                  
         SpiceDouble             lat;                                 
         SpiceDouble             lon;                                 
         SpiceDouble             r      [3];                          
         SpiceDouble             radius;                              
         SpiceDouble             sclkdp;                              
         SpiceDouble             tau;                                 
         SpiceDouble             tibf   [3][3];                       
         SpiceDouble             tol;                                 
         SpiceDouble             vpnt   [3];                          
         SpiceDouble             vpos   [3];                          
         SpiceDouble             vsurf  [3];                          
         SpiceDouble             vtarg  [6];                          
                                                                      
                                                                      
         /*                                                           
         Get all of the files and load them.                          
         */                                                           
         prompt_c ( "Enter the name of the kernel file\n"             
                    "containing planetary constants       > ",        
                    FILSIZ,                                           
                    file                                      );      
                                                                      
         furnsh_c ( file );                                           
                                                                      
                                                                      
         prompt_c ( "\nEnter the name of the kernel file\n"           
                    "containing SCLK coefficients         > ",        
                    FILSIZ,                                           
                    file                                      );      
                                                                      
         furnsh_c ( file );                                           
                                                                      
                                                                      
         prompt_c ( "\nEnter the name of the SPK file\n"              
                    "containing planetary and spacecraft\n"           
                    "ephemerides                          > ",        
                    FILSIZ,                                           
                    file                                      );      
                                                                      
         furnsh_c ( file );                                           
                                                                      
                                                                      
         prompt_c ( "\nEnter the name of the CK file\n"               
                    "containing instrument pointing       > ",        
                    FILSIZ,                                           
                    file                                      );      
                                                                      
         furnsh_c ( file );                                           
                                                                      
                                                                      
         /*                                                           
         Get the names of the spacecraft and target body; get the ID  
         code of the instrument.  Convert the instrument ID from      
         character to integer.  Translate the spacecraft and target   
         names to the corresponding integer codes.                    
         */                                                           
         prompt_c ( "\nEnter spacecraft name             > ",         
                    BDNMLN,                                           
                    scname                                    );      
                                                                      
         prompt_c ( "\nEnter target name                 > ",         
                    BDNMLN,                                           
                    targname                                  );      
                                                                      
         prompt_c ( "Enter NAIF integer instrument ID    > ",         
                    INNMLN,                                           
                    instch                                    );      
                                                                      
         prsint_c ( instch, &inst );                                  
         bodn2c_c ( scname, &sc, &found );                            
                                                                      
         if ( !found )                                                
         {                                                            
            setmsg_c ( "Spacecraft name # was not recognized." );     
            errch_c  ( "#", scname                             );     
            sigerr_c ( "SPICE(NAMENOTRECOGNIZED)"              );     
         }                                                            
                                                                      
         bodn2c_c ( targname, &targ, &found );                        
                                                                      
         if ( !found )                                                
         {                                                            
            setmsg_c ( "Target body name # was not recognized." );    
            errch_c  ( "#", targname                            );    
            sigerr_c ( "SPICE(NAMENOTRECOGNIZED)"               );    
         }                                                            
                                                                      
         /*                                                           
         Determine the input epoch.                                   
         */                                                           
         prompt_c ( "\nEnter SCLK string (blank line to quit) > ",    
                    TIMLEN,                                           
                    sclkch                                        );  
                                                                      
         while (  !iswhsp_c ( sclkch )  )                             
         {                                                            
            /*                                                        
            Convert the input clock string to ticks.                  
            */                                                        
            scencd_c ( sc, sclkch, &sclkdp );                         
                                                                      
            /*                                                        
            Determine the time tolerance.                             
            */                                                        
            prompt_c ( "Enter the tolerance as an SCLK string  > ",   
                       TIMLEN,                                        
                       tolch                                       ); 
                                                                      
            /*                                                        
            Convert the tolerance to ticks.                           
            */                                                        
            sctiks_c ( sc, tolch, &tol );                             
                                                                      
            /*                                                        
            Search the CK file for pointing data at the time sclkdp.  
            */                                                        
            ckgp_c ( inst, sclkdp, tol, REF, cmat, &clkout, &found ); 
                                                                      
            if ( !found )                                             
            {                                                         
               printf ( "\n"                                          
                        "The C-kernel file does not contain "         
                        "data for time %s SCLK %s.\n",                
                        scname,                                       
                        sclkch                              );        
            }                                                         
                                                                      
            /*                                                        
            Compute the inertial pointing vector for the instrument   
            boresight.                                                
                                                                      
                                                                      
          The boresight vector is assumed to define the z-axis of the 
                                                                      
          instrument-fixed frame.  This axis vector can be picked off 
            from the third row of the C-matrix.                       
            */                                                        
            vequ_c ( cmat[2], vpnt );                                 
                                                                      
            /*                                                        
            For all other computations, use the ET time corresponding 
            to the input SCLK.                                        
            */                                                        
            sct2e_c ( sc, sclkdp, &et );                              
                                                                      
            /*                                                        
            Compute the target state vector (position and velocity).  
            */                                                        
            spkez_c ( targ, et, REF, "lt+s", sc, vtarg, &tau );       
                                                                      
            /*                                                        
            Get the tibf matrix and radii of target ellipsoid model.  
                                                                      
            We need tibf for the target as it appeared when the       
            instrument took its measurement at time et. The target    
            was at its apparent location tau seconds earlier.         
                                                                      
                                                                      
         tipbod_c and bodvcd_c will read constants from the planetary 
            constants kernel file.                                    
            */                                                        
            tipbod_c ( REF,  targ,    et-tau, tibf );                 
            bodvcd_c ( targ, "RADII", 3,  &n, r    );                 
                                                                      
            /*                                                        
            The position of the observer is just the negative of the  
            position part of the spacecraft-target vector, vtarg.     
                                                                      
           Note that this is NOT the same as the apparent position of 
            the spacecraft as seen from the target.                   
            */                                                        
            vminus_c ( vtarg, vpos );                                 
                                                                      
            /*                                                        
            Put both vectors in body-fixed coordinates.               
            */                                                        
            mxv_c ( tibf, vpos, vpos );                               
            mxv_c ( tibf, vpnt, vpnt );                               
                                                                      
                                                                      
            /*                                                        
            Compute the point of intersection, if any.                
            */                                                        
            surfpt_c ( vpos, vpnt, r[0], r[1], r[2], vsurf, &found ); 
                                                                      
                                                                      
            if ( !found )                                             
            {                                                         
               printf ( "\nThe line-of-sight pointing vector "        
                        "does not intersect the target "              
                        "at the epoch %s SCLK %s.\n",                 
                        scname,                                       
                        sclkch                                );      
            }                                                         
                                                                      
            else                                                      
            {                                                         
               /*                                                     
                                                                      
              Convert intersection point from rectangular to lat-lon- 
               radius coordinates.                                    
               */                                                     
               reclat_c ( vsurf, &radius, &lon, &lat );               
                                                                      
                                                                      
               printf ( "\n"                                          
                        "Radius (km)         %f\n"                    
                        "Longitude (deg)     %f\n"                    
                        "Latitude (deg)      %f\n"                    
                        "\n",                                         
                        radius,                                       
                        lon * dpr_c(),                                
                        lat * dpr_c()             );                  
                                                                      
            }                                                         
                                                                      
            /*                                                        
            Input next epoch.                                         
            */                                                        
            prompt_c ( "\nEnter SCLK string (blank line to quit) > ", 
                       TIMLEN,                                        
                                                                      
                     sclkch                                        ); 
         }                                                            
                                                                      
         return (0);                                                  
      }                                                               
                                                                      
                                                
                                                                      
Appendix C --- An Example of Writing a Type 1 CK Segment  
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| The following example shows how one might write a program to create 
  or add to a C-kernel file.                                          
                                                                      
The program creates a single type 1 segment for the scan platform of  
the Galileo spacecraft. Assume that C-matrices, angular velocity      
vectors, and the associated SCLK time strings are contained in        
time-ordered arrays assumed to have been initialized elsewhere (by    
the function \`get_gll_pnt' --- not part of CSPICE). The program      
provides the option of adding the segment to an existing file, or     
creating a new file.                                                  
                                                                      
::                                                                    
                                                                      
         /*                                                           
         Local variables                                              
         */                                                           
         SpiceChar                ck      [FILSIZ];                   
         SpiceChar                sclkch  [MAXREC][CLKLEN];           
                                                                      
         SpiceDouble              avvs    [MAXREC][3];                
         SpiceDouble              begtim;                             
         SpiceDouble              cmats   [MAXREC][3][3];             
         SpiceDouble              endtim;                             
         SpiceDouble              quats   [MAXREC][4];                
         SpiceDouble              sclkdp  [MAXREC];                   
                                                                      
         SpiceInt                 handle;                             
         SpiceInt                 i;                                  
         SpiceInt                 nprec;                              
                                                                      
                                                                      
         /*                                                           
         Can either add to an existing CK file or create a brand      
         new one.                                                     
         */                                                           
         printf ( "You may either add to an existing CK file, or "    
                  "create a new one.\n"                            ); 
                                                                      
         prompt_c ( "Enter the name of the CK file to create > ",     
                    FILSIZ,                                           
                    ck                                           );   
                                                                      
                                                                      
         /*                                                           
         To convert SCLK times from clock strings to encoded SCLK,    
                                                                      
        we need to load the Galileo spacecraft clock kernel file into 
                                                                      
       the kernel pool.  Assume that the file is called gll_sclk.tsc. 
         */                                                           
         furnsh_c ( SCLKKER );                                        
                                                                      
                                                                      
         /*                                                           
         To open a new CK file use ckopn_c, and for an existing       
         file use dafopw_c.                                           
         */                                                           
         if (  exists_c ( ck )  )                                     
         {                                                            
            dafopw_ ( ck, &handle, strlen(ck) );                      
         }                                                            
         else                                                         
         {                                                            
            ckopn_c ( ck, ck, 0, &handle );                           
         }                                                            
                                                                      
                                                                      
         /*                                                           
         Get the pointing information to go in the C-kernel segment.  
                                                                      
            1) Number of pointing instances returned                  
            2) Array of SCLK times                                    
            3) Array of C-matrices, dimension [][3][3]                
            4) Array of angular velocity vectors, dimension [][3]     
                                                                      
         */                                                           
         get_gll_pnt ( &nprec, CLKLEN, sclkch, cmats, avvs );         
                                                                      
                                                                      
         /*                                                           
         Now convert the times to encoded SCLK.                       
         */                                                           
         for ( i = 0;  i < nprec;  i++ )                              
         {                                                            
            scencd_c ( GLL, sclkch[i], sclkdp+i );                    
         }                                                            
                                                                      
         /*                                                           
         Set the segment boundaries equal to the first and last       
         time in the segment.                                         
         */                                                           
         begtim = sclkdp[      0];                                    
         endtim = sclkdp[nprec-1];                                    
                                                                      
         /*                                                           
         The C-matrices are represented by quaternions in a type 1 CK 
         segment.  The CSPICE routine m2q_c converts C-matrices to    
         quaternions.                                                 
         */                                                           
                                                                      
         for ( i = 0;  i < nprec;  i++ )                              
         {                                                            
            m2q_c ( cmats[i], quats[i] );                             
         }                                                            
                                                                      
                                                                      
         /*                                                           
         The constants that will go into the segment descriptor are   
                                                                      
            AVFLAG ... Angular velocity flag.  Set to SPICETRUE.      
            INST   ... NAIF Instrument ID code.  Set to -77001.       
                                                                      
        REF    ... Name of inertial reference frame.  Set to "B1950". 
            SEGID  ... Segment identifer.  Set to                     
                                                                      
                         "GLL SCAN PLT - NAIF - 18-NOV-90"            
                                                                      
                                                                      
         That is all the information that we need. Write the segment. 
         */                                                           
                                                                      
         ckw01_c ( handle,                                            
                   begtim,                                            
                   endtim,                                            
                   INST,                                              
                   REF,                                               
                   AVFLAG,                                            
                   SEGID,                                             
                   nprec,                                             
                   sclkdp,                                            
                   quats,                                             
                   avvs    );                                         
                                                                      
         /*                                                           
         Close the file.                                              
         */                                                           
         ckcls_c ( handle );                                          
                                                                      
         return (0);                                                  
      }                                                               
                                                                      
                                                
                                                                      
Appendix D --- An Example of Writing a Type 2 CK Segment  
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| This example program creates a single type 2 segment of predict     
  pointing for the scan platform of the Galileo spacecraft.           
                                                                      
This program will use data type 2 to store pointing information for   
time intervals during which the pointing of the scan platform is      
constant. It is assumed that a function called \`gll_const_pnt' will  
provide ordered arrays of C-matrices and interval start and stop      
times. The Ith C-matrix represents the fixed platform pointing during 
the Ith interval. Assume that the start and stop times are given in   
Galileo clock string form so that they must be converted into encoded 
SCLK for use in the C-kernel.                                         
                                                                      
::                                                                    
                                                                      
      /*                                                              
                                                                      
      PROGRAM WRTCK2                                                  
                                                                      
         Write a type 2 CK segment to a new or existing C-kernel.     
         This example assumes the existence of a user-supplied        
         function to return time-tagged pointing values.              
                                                                      
      */                                                              
                                                                      
      #include <stdio.h>                                              
      #include <string.h>                                             
      #include "SpiceUsr.h"                                           
      #include "SpiceZfc.h"                                           
                                                                      
      int main()                                                      
      {                                                               
                                                                      
         /*                                                           
         Functions                                                    
         */                                                           
         void gll_const_pnt ( SpiceInt       * nprec,                 
                              SpiceInt         sclklen,               
                              void           * begch,                 
                              void           * endch,                 
                              SpiceDouble  ( * cmats  )[3][3] );      
                                                                      
         /*                                                           
         Local constants                                              
         */                                                           
         #define  CLKLEN         30                                   
         #define  FILSIZ         256                                  
         #define  GLL            -77                                  
         #define  IFNAME         "Test CK created by wrtck.c"         
         #define  INST           -77001                               
         #define  MAXREC         10000                                
         #define  NCOMCH         1000                                 
         #define  REF            "B1950"                              
         #define  REFLEN         10                                   
         #define  SCLKKER        "gll_sclk.tsc"                       
         #define  SECPERTICK     ( 1. / 120. )                        
                                                                      
       #define  SEGID          "GLL SCAN PLT - NAIF - TYPE 2 PREDICT" 
         #define  SIDLEN         40                                   
                                                                      
                                                                      
         /*                                                           
         Local variables                                              
         */                                                           
         SpiceChar                ck      [FILSIZ];                   
         SpiceChar                begch   [MAXREC][CLKLEN];           
         SpiceChar                endch   [MAXREC][CLKLEN];           
                                                                      
         SpiceDouble              avvs    [MAXREC][3];                
         SpiceDouble              begtim;                             
         SpiceDouble              cmats   [MAXREC][3][3];             
         SpiceDouble              endtim;                             
         SpiceDouble              quats   [MAXREC][4];                
         SpiceDouble              rates   [MAXREC];                   
         SpiceDouble              start   [MAXREC];                   
         SpiceDouble              stop    [MAXREC];                   
                                                                      
         SpiceInt                 handle;                             
         SpiceInt                 i;                                  
         SpiceInt                 nprec;                              
                                                                      
                                                                      
         /*                                                           
         Can either add to an existing CK file or create a brand      
         new one.                                                     
         */                                                           
         printf ( "You may either add to an existing CK file, or "    
                  "create a new one.\n"                            ); 
                                                                      
         prompt_c ( "Enter the name of the CK file to create > ",     
                    FILSIZ,                                           
                    ck                                           );   
                                                                      
                                                                      
         /*                                                           
         To convert SCLK times from clock string to encoded SCLK,     
                                                                      
        we need to load the Galileo spacecraft clock kernel file into 
                                                                      
       the kernel pool.  Assume that the file is called gll_sclk.tsc. 
         */                                                           
         furnsh_c ( SCLKKER );                                        
                                                                      
                                                                      
         /*                                                           
         To open a new CK file use ckopn_c, and for an existing       
         file use dafopw_c.                                           
         */                                                           
         if (  exists_c ( ck )  )                                     
         {                                                            
            dafopw_ ( ck, &handle, strlen(ck) );                      
         }                                                            
         else                                                         
         {                                                            
            ckopn_c ( ck, ck, 0, &handle );                           
         }                                                            
                                                                      
                                                                      
         /*                                                           
         Get the pointing information to go in the C-kernel segment.  
                                                                      
            1) Number of pointing instances returned                  
            2) Interval start times in clock string form              
            3) Interval stop times in clock string form               
            3) Array of C-matrices, dimension [][3][3]                
                                                                      
         */                                                           
         gll_const_pnt ( &nprec, CLKLEN, begch, endch, cmats );       
                                                                      
                                                                      
         /*                                                           
         Now convert the times to encoded SCLK.                       
         */                                                           
         for ( i = 0;  i < nprec;  i++ )                              
         {                                                            
            scencd_c ( GLL, begch[i], start+i );                      
            scencd_c ( GLL, endch[i], stop +i );                      
         }                                                            
                                                                      
                                                                      
         /*                                                           
         Set the segment boundaries equal to the first and last       
         time in the segment.                                         
         */                                                           
         begtim = start[      0];                                     
         endtim = stop [nprec-1];                                     
                                                                      
                                                                      
         /*                                                           
         The C-matrices are represented by quaternions in a type 1 CK 
         segment.  The CSPICE routine m2q_c converts C-matrices to    
         quaternions.                                                 
         */                                                           
         for ( i = 0;  i < nprec;  i++ )                              
         {                                                            
            m2q_c ( cmats[i], quats[i] );                             
         }                                                            
                                                                      
                                                                      
         /*                                                           
                                                                      
      Since the pointing is constant over each interval, each angular 
         velocity vector is zero.                                     
         */                                                           
         for ( i = 0;  i < (3*nprec);  i++ )                          
         {                                                            
           *( (SpiceDouble *)avvs+i ) = 0.;                           
         }                                                            
                                                                      
                                                                      
         /*                                                           
         Since this is a predict segment the number of seconds        
         represented by one tick during each of the intervals will    
         be set equal to the nominal amount of time represented by    
         the least significant field of the Galileo clock: 1/120 sec. 
         */                                                           
         for ( i = 0;  i < nprec;  i++ )                              
         {                                                            
            rates[i] = SECPERTICK;                                    
         }                                                            
                                                                      
                                                                      
         /*                                                           
         The constants that will go into the segment descriptor are   
                                                                      
            INST   ... NAIF Instrument ID code.  Set to -77001.       
                                                                      
            REF    ... Name of inertial reference frame.  Set to      
                       "B1950".                                       
                                                                      
            SEGID  ... Segment identifer.  Set to                     
                                                                      
                         "GLL SCAN PLT - NAIF - TYPE 2 PREDICT"       
                                                                      
                                                                      
         That is all the information that we need. Write the segment. 
         */                                                           
         ckw02_c ( handle,                                            
                   begtim,                                            
                   endtim,                                            
                   INST,                                              
                   REF,                                               
                   SEGID,                                             
                   nprec,                                             
                   start,                                             
                   stop,                                              
                   quats,                                             
                   avvs,                                              
                   rates    );                                        
                                                                      
         /*                                                           
         Close the file.                                              
         */                                                           
         ckcls_c ( handle );                                          
                                                                      
         return (0);                                                  
      }                                                               
                                                                      
                                                
                                                                      
Appendix E --- An Example of Writing a Type 3 CK Segment  
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                
| The following example program shows how one might write a type 3    
  C-kernel segment to a new file.                                     
                                                                      
The program creates a single type 3 segment for a two hour time       
period for the Mars Global Surveyor spacecraft bus. The program       
calculates the pointing instances directly from the spacecraft and    
planet ( SPK ) ephemeris file.                                        
                                                                      
The names of the input ephemeris, leapseconds, spacecraft clock, and  
planetary constants kernel files are fictitious.                      
                                                                      
::                                                                    
                                                                      
      /*                                                              
                                                                      
      PROGRAM WRTCK3                                                  
                                                                      
         This program creates a predict type 3 CK segment for the     
         Mars Global Surveyor spacecraft.                             
                                                                      
      */                                                              
                                                                      
      #include <stdio.h>                                              
      #include "SpiceUsr.h"                                           
                                                                      
                                                                      
      int main()                                                      
      {                                                               
                                                                      
         /*                                                           
         Functions                                                    
         */                                                           
         void get_dervrt ( SpiceDouble     epoch,                     
                           SpiceDouble     dcmat[3][3] );             
                                                                      
         void locvrt_m__ ( SpiceInt        center,                    
                           SpiceInt        sc,                        
                           SpiceDouble     epoch,                     
                           SpiceChar     * ref,                       
                           SpiceChar     * abcorr,                    
                           SpiceDouble     cmat  [3][3] );            
                                                                      
         /*                                                           
         Local constants                                              
         */                                                           
                                                                      
         /*                                                           
         Names of kernels:  LSK, SCLK, PCK, SPK, CK.                  
         */                                                           
         #define  LSK            "leap.tls"                           
         #define  SCLKKER        "mgs.tsc"                            
         #define  PCK            "mgs.tpc"                            
         #define  SPK            "mgs.bsp"                            
         #define  CK             "mgs_predict_ck.bc"                  
                                                                      
         /*                                                           
         The internal file name:  just set this equal to the CK name. 
         */                                                           
         #define  IFNAME         CK                                   
                                                                      
         /*                                                           
         The segment identifier:                                      
         */                                                           
         #define  SEGID          "MGS PREDICT TYPE 3 SEGMENT"         
                                                                      
         /*                                                           
         The number of characters to reserve in the comment area      
         when creating the file:                                      
         */                                                           
         #define  NCOMCH         0                                    
                                                                      
         /*                                                           
         The reference frame of the segment is J2000.                 
         */                                                           
         #define  REF            "J2000"                              
                                                                      
         /*                                                           
         Assign the NAIF body id codes for the Mars Global Surveyor   
         spacecraft and Mars.                                         
         */                                                           
         #define  CENTERNAME     "Mars"                               
         #define  SCNAME         "MGS"                                
                                                                      
                                                                      
         /*                                                           
         The ID code for the MGS spacecraft bus:                      
         */                                                           
         #define  INST           -94000                               
                                                                      
         /*                                                           
                                                                      
        The angular velocity flag will indicate that angular velocity 
         data are available.                                          
         */                                                           
         #define  AVFLAG         SPICETRUE                            
                                                                      
                                                                      
         /*                                                           
         We will need about 2000 pointing instances.                  
         */                                                           
         #define  MAXREC         2000                                 
                                                                      
         /*                                                           
         The segment begin and end times.                             
         */                                                           
         #define  UTCBEG         "1994 JAN 21 00:00:00"               
         #define  UTCEND         "1994 JAN 21 02:00:00"               
                                                                      
         /*                                                           
         The time step separating the time tags of the pointing       
         instances.  The units are ticks of encoded SCLK.             
         */                                                           
         #define  SCLKSTEP       1024.0                               
                                                                      
                                                                      
         /*                                                           
         Local variables                                              
         */                                                           
         SpiceBoolean            found;                               
                                                                      
         SpiceDouble             avvs    [MAXREC][3];                 
         SpiceDouble             begtime;                             
         SpiceDouble             cmat    [3][3];                      
         SpiceDouble             dcmat   [3][3];                      
         SpiceDouble             endtime;                             
         SpiceDouble             epoch;                               
         SpiceDouble             etBeg;                               
         SpiceDouble             etEnd;                               
         SpiceDouble             omega   [3][3];                      
         SpiceDouble             quats   [MAXREC][4] ;                
         SpiceDouble             scBeg;                               
         SpiceDouble             scEnd;                               
         SpiceDouble             sclk;                                
         SpiceDouble             sclkdp  [MAXREC];                    
         SpiceDouble             start   [MAXREC];                    
                                                                      
         SpiceInt                ckhan;                               
         SpiceInt                i;                                   
         SpiceInt                nint;                                
         SpiceInt                nrec;                                
         SpiceInt                SCID;                                
                                                                      
         SpiceInt                centerID;                            
                                                                      
                                                                      
         /*                                                           
         Translate the spacecraft and central body names to           
         NAIF ID codes.                                               
         */                                                           
         bodn2c_c ( SCNAME,     &SCID,  &found );                     
                                                                      
                                                                      
::                                                                    
                                                                      
         if ( !found )                                                
         {                                                            
                                                                      
        setmsg_c ( "Name # could not be mapped to a NAIF ID code." ); 
                                                                      
        errch_c  ( "#",  SCNAME                                    ); 
                                                                      
        sigerr_c ( "SPICE(NAMENOTFOUND)"                           ); 
         }                                                            
                                                                      
         bodn2c_c ( CENTERNAME, &centerID, &found );                  
                                                                      
         if ( !found )                                                
         {                                                            
                                                                      
        setmsg_c ( "Name # could not be mapped to a NAIF ID code." ); 
                                                                      
        errch_c  ( "#",  CENTERNAME                                ); 
                                                                      
        sigerr_c ( "SPICE(NAMENOTFOUND)"                           ); 
         }                                                            
                                                                      
::                                                                    
                                                                      
                                                                      
         /*                                                           
         Load the binary SPK file that provides states for MGS with   
         respect to Mars for the time period of interest.             
         */                                                           
         furnsh_c ( SPK );                                            
                                                                      
         /*                                                           
         Load the text leapseconds, spacecraft clock ( sclk ), and    
         planetary constants ( pck ) files into the kernel pool.      
         */                                                           
         furnsh_c ( LSK     );                                        
         furnsh_c ( SCLKKER );                                        
         furnsh_c ( PCK     );                                        
                                                                      
         /*                                                           
         Convert the segment begin and end times first to ET then to  
         MGS spacecraft clock.                                        
         */                                                           
         str2et_c ( UTCBEG, &etBeg );                                 
         str2et_c ( UTCEND, &etEnd );                                 
                                                                      
         sce2c_c  ( SCID, etBeg, &scBeg );                            
         sce2c_c  ( SCID, etEnd, &scEnd );                            
                                                                      
                                                                      
         /*                                                           
         Calculate the quaternions and angular velocity vectors at    
         roughly four second intervals from the segment start time    
         until the end.                                               
         */                                                           
                                                                      
         for (  ( i = 0,            sclk =  scBeg    );               
                ( i < MAXREC ) && ( sclk <= scEnd    );               
                ( i++,              sclk += SCLKSTEP )   )            
         {                                                            
                                                                      
            /*                                                        
            The times stored in the C-kernel are always in encoded    
            spacecraft clock form.  SPK takes ET as the input time.   
            */                                                        
            sclkdp[i] = sclk;                                         
                                                                      
            sct2e_c ( SCID, sclk, &epoch );                           
                                                                      
            /*                                                        
                                                                      
           Find the C-matrix using the non-CSPICE routine locvrt_m__. 
            locvrt_m__ returns the 3x3 matrix that transforms vectors 
            from a specified inertial reference frame to the `Local   
            Vertical Frame' for a specified observer and target body. 
            This frame is defined as follows:                         
                                                                      
                                                                      
               Z-axis:  The unit vector pointing from the orbiter to  
                                                                      
                    the sub-orbiter point on the extended body.  This 
                        point is the closest point on the body to the 
                                                                      
                      orbiter; thus the unit outward normal vector on 
                        the body's surface is the negative of the     
                        Z-vector.                                     
                                                                      
                                                                      
               Y-axis:  The unitized cross product                    
                                                                      
                           Z x V                                      
                                                                      
                                                                      
                       where V is the orbiter's inertially referenced 
                        velocity vector.                              
                                                                      
                                                                      
               X-axis:  The cross product                             
                                                                      
                           Y x Z                                      
                                                                      
                                                                      
                     (Z and Y are already orthonormal, so X is a unit 
                        vector.)                                      
                                                                      
                                                                      
            In the call below, the argument "NONE" indicates that the 
            vectors defining the frame are not to be corrected for    
            light time or stellar aberration.                         
            */                                                        
                                                                      
            locvrt_m__ ( centerID, SCID,  epoch,       REF,           
                         "NONE",   cmat,  strlen(REF), 4   );         
                                                                      
            m2q_c ( cmat, quats[i] );                                 
                                                                      
                                                                      
            /*                                                        
            Calculate the angular velocity vector using the following 
            formula:                                                  
                                                                      
            Let the angular velocity vector be  AV = ( a1, a2, a3 )   
            and let the matrix OMEGA be:                              
                                                                      
                        +--              --+                          
                        |   0   -a3   a2   |                          
                        |                  |                          
               OMEGA =  |  a3    0    -a1  |                          
                        |                  |                          
                        |  -a2   a1    0   |                          
                        +--              --+                          
                                                                      
             Then the derivative of a C-matrix C is given by          
                                                                      
                                      t                               
                         t       d [ C ]                              
                OMEGA * C   =    -------                              
                                    dt                                
                                                                      
             Thus, given a C-matrix and its derivative, the angular   
             velocity can be calculated from                          
                                                                      
                                 t                                    
                             d[ C  ]                                  
                 OMEGA  =    -------  *  C                            
                                dt                                    
                                                                      
                                                                      
                                                                      
            get_dervrt is a non-CSPICE routine that will calculate    
            the derivative of the C-matrix calculated by locvrt_m__.  
            */                                                        
            get_dervrt ( epoch, dcmat );                              
                                                                      
            mtxm_c ( dcmat, cmat, omega );                            
                                                                      
            avvs[i][0]  =  omega[2][1];                               
            avvs[i][1]  =  omega[0][2];                               
            avvs[i][2]  =  omega[1][0];                               
         }                                                            
                                                                      
         /*                                                           
         Set the pointing record count and the segment time bounds.   
         */                                                           
         nrec    -= i;                                                
                                                                      
         begtime =  sclkdp[0];                                        
         endtime =  sclkdp[nrec-1];                                   
                                                                      
                                                                      
         /*                                                           
         Unload the SPK file.                                         
         */                                                           
         unload_c ( SPK );                                            
                                                                      
                                                                      
         /*                                                           
         The process of determining how to partition the pointing     
         instances into interpolation intervals varies with respect   
         to the means by which the pointing instances are obtained.   
                                                                      
         For this example program it is acceptable to interpolate     
         between all of the adjacent pointing instances because:      
                                                                      
         1) The pointing was calculated at every 4 seconds so there   
            are no gaps in the data.                                  
                                                                      
         2) The pointing was calculated directly from the spacecraft  
            and planetary ephemeris so that the functions for the     
            spacecraft axis and angular velocity vectors will change  
            "slowly" and continuously.                                
                                                                      
         Therefore there is only one interpolation interval for the   
         entire segment.                                              
         */                                                           
                                                                      
         nint     =  1;                                               
         start[0] =  sclkdp[0];                                       
                                                                      
                                                                      
         /*                                                           
         Now that the pointing instances have been calculated the     
         segment can be written to a C-kernel file.                   
                                                                      
         Open a new file.                                             
         */                                                           
         ckopn_c ( CK, IFNAME, NCOMCH, &ckhan );                      
                                                                      
                                                                      
         /*                                                           
         The values that will go in the segment descriptor are        
         already set.  These are:                                     
                                                                      
            1) The NAIF ID code for the MGS spacecraft bus INST.      
            2) The angular velocity flag AVFLAG.                      
            3) The segment start and stop times scBeg and scEnd.      
            4) The reference frame REF.                               
            5) The segment time bounds begtime and endtime.           
                                                                      
         The segment identifier SEGID is set as well.                 
                                                                      
            1) Number of pointing instances returned                  
            2) Interval start times in clock string form              
            3) Interval stop times in clock string form               
            3) Array of C-matrices, dimension [][3][3]                
                                                                      
         */                                                           
                                                                      
                                                                      
         /*                                                           
         Write the segment to the file attached to HANDLE.            
         */                                                           
         ckw03_c ( ckhan,  begtime, endtime, INST,   REF,    AVFLAG,  
                   SEGID,  nrec,    sclkdp,  quats,  avvs,   nint,    
                   start                                           ); 
                                                                      
         /*                                                           
         Close the file.                                              
         */                                                           
         ckcls_c ( ckhan );                                           
                                                                      
         return (0);                                                  
                                                                      
      }                                                               
                                                                      
                                                
                                                                      
Appendix G: Document Revision History                     
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                    
                                                                      
February 13, 2014                                         
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| Added documentation of CK type 6.                                   
                                            
                                                                      
April 1, 2009                                             
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| Added a note about the SPICE file identification word for CK        
  kernels.                                                            
                                            
                                                                      
November 17, 2005                                         
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| Abstract was added.                                                 
                                                                      
Calls/references to the deprecated routine                            
:py:meth:`~spiceypy.spiceypy.bodvar` were replaced with             
calls/referenes to :py:meth:`~spiceypy.spiceypy.bodvcd`.            
:py:meth:`~spiceypy.spiceypy.bodvrd` is mentioned as another        
routine superseding :py:meth:`~spiceypy.spiceypy.bodvar`.           
                                                                      
C examples showing incorrect calling sequences for                    
:py:meth:`~spiceypy.spiceypy.prompt` were corrected.                
                                            
                                                                      
December 21, 2004                                         
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| Replaced references and examples of lower level CK                  
  loading/unloading functions with                                    
  `furnsh_c                                                           
 <../cspice/furnsh_c.html>`__/:py:meth:`~spiceypy.spiceypy.unload`. 
                                            
                                                                      
February 2, 2004                                          
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| Performed a spell-check on text.                                    
                                            
                                                                      
September 04, 2002                                        
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| Added a discussion of CK type 05.                                   
                                                                      
Added a brief discussion of the DAF run-time binary file format       
translation capability now present in the SPICE Toolkit.              
                                            
                                                                      
February 15, 2000                                         
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| This February 2000 version of the document differs from the         
  previous version of October 1999 in the following areas:            
                                                                      
The section describing new Chebyshev polynomial based data type--CK   
Type 4--was added to the document.                                    
                                            
                                                                      
October 14, 1999                                          
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| This is the initial release of the CSPICE edition of the CK         
  "Required Reading" document.                                        
                                            
                                                                      
Overview of the October 14, 1999 revision                 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                        
| The SPICE system has been extended to include CSPICE---a version of 
  the NAIF Toolkit software coded in the ANSI C programming language. 
                                                                      
The CSPICE library---the C counterpart of SPICELIB---consists of two  
categories of functions:                                              
                                                                      
- Low level functions, translated from Fortran to ANSI C via   
  the automatic translation program f2c.                              
                                                                      
- Application interface-level functions, hand-coded in ANSI C. 
  These hand-coded functions are called \``wrappers'' since they      
  typically serve to encapsulate C code generated by running f2c on   
  Fortran source code.                                                
                                                                      
Wrapper functions are denoted by names ending with the suffix         
::                                                                    
                                                                      
      _c                                                              
                                                                      
Functions created by f2c have names ending with the suffix            
::                                                                    
                                                                      
      _                                                               
                                                                      
In this first version of CSPICE, wrappers are provided for the        
principal C application interface functions. Hand-coded versions of   
other, less frequently used interface functions will be supplied in a 
later version of CSPICE. The remaining, lower-level functions will    
not be provided with wrappers.                                        
The set of currently available CSPICE CK wrapper functions is:        
                                                                      
::                                                                    
                                                                      
      ckcls_c                                                         
      ckgp_c                                                          
      ckgpav_c                                                        
      furnsh_c                                                        
      ckopn_c                                                         
      unload_c                                                        
      ckw01_c                                                         
      ckw02_c                                                         
      ckw03_c                                                         
                                                                      
Less frequently used application interface-level functions referenced 
here but for which wrappers are not yet implemented are:              
::                                                                    
                                                                      
      Portions of the DAF family of functions                         
      The SPC family of functions                                     
