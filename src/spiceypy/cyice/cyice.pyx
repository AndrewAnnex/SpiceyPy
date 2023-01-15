# cython: language_level = 3
"""
main cython wrapper code

defs are visible to python
cdef's are not visible to python and are pure c, use for inner loops
cpdefs are both, really only useful for recursion

"""

# okay for some reason making a pxd file causes cython to fail
# todo maybe okay to just use "*" for header file
# grab externs from SpiceZpr.h
cdef extern from "SpiceUsr.h" nogil:
    ctypedef int SpiceBoolean
    ctypedef char SpiceChar
    ctypedef long SpiceInt
    ctypedef double SpiceDouble
    ctypedef const int ConstSpiceBool
    ctypedef const char ConstSpiceChar
    ctypedef const long ConstSpiceInt
    ctypedef const double ConstSpiceDouble
    
    # Cells
    cdef enum SpiceCellDataType:
        char   = 0,
        double = 1,
        int    = 2,
        time   = 3,
        bool   = 4

    cdef struct _SpiceCell:
        SpiceCellDataType dtype
        SpiceInt           length
        SpiceInt           size
        SpiceInt           card
        SpiceBoolean       isSet
        SpiceBoolean       adjust
        SpiceBoolean       init
        void * base
        void * data
    
    ctypedef _SpiceCell SpiceCell
    ctypedef const SpiceCell ConstSpiceCell

    # start of function defs
    # A
    cdef void appndc_c(ConstSpiceChar * item,
                       SpiceCell * cell);

    cdef void appndd_c(SpiceDouble item,
                       SpiceCell * cell);

    cdef void appndi_c(SpiceInt item,
                       SpiceCell * cell);

    cdef void axisar_c(ConstSpiceDouble     axis   [3],
                       SpiceDouble          angle,
                       SpiceDouble          r      [3][3]);

    cdef void azlcpo_c(ConstSpiceChar * method,
                       ConstSpiceChar * target,
                       SpiceDouble         et,
                       ConstSpiceChar * abcorr,
                       SpiceBoolean        azccw,
                       SpiceBoolean        elplsz,
                       ConstSpiceDouble    obspos [3],
                       ConstSpiceChar * obsctr,
                       ConstSpiceChar * obsref,
                       SpiceDouble         azlsta [6],
                       SpiceDouble * lt);

    cdef void  azlrec_c(SpiceDouble         range,
                        SpiceDouble         az,
                        SpiceDouble         el,
                        SpiceBoolean        azccw,
                        SpiceBoolean        elplsz,
                        SpiceDouble         rectan [3]);
    # B
    cdef double b1900_c()

cpdef b1900():
    return b1900_c()
