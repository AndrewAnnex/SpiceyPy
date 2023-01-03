# cython: language_level = 3
"""
Main file for external declarations for cspice

look around page 118 of cython book for particulars

also see https://github.com/alfonsoSR/HPLOP/blob/cdbcef68ffb6bcfb6e77edf0e424bf2aeb89f60f/src/hplop/core/equations.pxd
"""


cdef extern from "SpiceUsr.h" nogil:
    ctypedef int SpiceBoolean
    ctypedef char SpiceChar
    ctypedef long SpiceInt
    ctypedef double SpiceDouble
    ctypedef const int ConstSpiceBool
    ctypedef const char ConstSpiceChar
    ctypedef const long ConstSpiceInt
    ctypedef const double ConstSpiceDouble
    
    cdef SpiceDouble b1900_c()
    cdef SpiceDouble b1950_c()
    void furnsh_c(ConstSpiceChar * file)
    cdef void kclear_c()
    cdef void str2et_c(ConstSpiceChar * epoch, SpiceDouble * et)
    

