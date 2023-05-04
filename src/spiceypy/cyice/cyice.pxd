# cython: language_level = 3
# cython: embedsignature = True
# cython: c_string_type = bytes
# cython: c_string_encoding = utf-8

cdef extern from "SpiceUsr.h" nogil:
    ctypedef bint SpiceBoolean
    ctypedef char SpiceChar
    ctypedef long SpiceInt
    ctypedef double SpiceDouble
    ctypedef const int ConstSpiceBool
    ctypedef const char ConstSpiceChar
    ctypedef const long ConstSpiceInt
    ctypedef const double ConstSpiceDouble

    # Cells
    cdef enum SpiceCellDataType:
        char = 0,
        double = 1,
        int = 2,
        time = 3,
        bool = 4

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
    cdef double b1900_c()

    cdef double b1950_c()

    #C 

    #E
    cdef void etcal_c(SpiceDouble   et,
                      SpiceInt      callen,
                      SpiceChar   * calstr)
    
    cdef void et2utc_c(SpiceDouble      et,
                       ConstSpiceChar * format,
                       SpiceInt         prec,
                       SpiceInt         lenout,
                       SpiceChar * utcstr)

    #F 
    cdef void furnsh_c(ConstSpiceChar * file)

    #S
    cdef void spkez_c(SpiceInt         target,
                      SpiceDouble      epoch,
                      ConstSpiceChar * frame,
                      ConstSpiceChar * abcorr,
                      SpiceInt         observer,
                      SpiceDouble      state[6],
                      SpiceDouble * lt)
    
    cdef void spkezr_c(ConstSpiceChar * target,
                       SpiceDouble      epoch,
                       ConstSpiceChar * frame,
                       ConstSpiceChar * abcorr,
                       ConstSpiceChar * observer,
                       SpiceDouble      state[6],
                       SpiceDouble * lt)

    cdef void spkpos_c(ConstSpiceChar * targ,
                       SpiceDouble      et,
                       ConstSpiceChar * ref,
                       ConstSpiceChar * abcorr,
                       ConstSpiceChar * obs,
                       SpiceDouble      ptarg[3],
                       SpiceDouble * lt)

    cdef void str2et_c(ConstSpiceChar * date,
                       SpiceDouble * et);
    
    # U
    cdef void utc2et_c(ConstSpiceChar * utcstr, SpiceDouble * et)
