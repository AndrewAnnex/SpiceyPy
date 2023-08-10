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
    cdef SpiceDouble b1900_c()

    cdef SpiceDouble b1950_c()

    #C 
    cdef void convrt_c(SpiceDouble      x,
                       ConstSpiceChar * inunit,
                       ConstSpiceChar * outunit,
                       SpiceDouble    * y)

    #E
    cdef void et2utc_c(SpiceDouble      et,
                       ConstSpiceChar * format,
                       SpiceInt         prec,
                       SpiceInt         lenout,
                       SpiceChar      * utcstr)
    
    cdef void etcal_c(SpiceDouble   et,
                      SpiceInt      callen,
                      SpiceChar   * calstr)

    #F 
    cdef SpiceBoolean failed_c()
    
    cdef void furnsh_c(ConstSpiceChar * file)
    
    #G
    cdef void getmsg_c(ConstSpiceChar * option,
                       SpiceInt         msglen,
                       SpiceChar      * msg)
    #Q
    cdef void qcktrc_c(SpiceInt         tracelen,
                       SpiceChar      * trace)
    
    #R
    cdef void reset_c()

    #S
    cdef void spkez_c(SpiceInt         target,
                      SpiceDouble      epoch,
                      ConstSpiceChar * frame,
                      ConstSpiceChar * abcorr,
                      SpiceInt         observer,
                      SpiceDouble      state[6],
                      SpiceDouble    * lt)
    
    cdef void spkezr_c(ConstSpiceChar * target,
                       SpiceDouble      epoch,
                       ConstSpiceChar * frame,
                       ConstSpiceChar * abcorr,
                       ConstSpiceChar * observer,
                       SpiceDouble      state[6],
                       SpiceDouble    * lt)

    cdef void spkpos_c(ConstSpiceChar * targ,
                       SpiceDouble      et,
                       ConstSpiceChar * ref,
                       ConstSpiceChar * abcorr,
                       ConstSpiceChar * obs,
                       SpiceDouble      ptarg[3],
                       SpiceDouble * lt)

    cdef void str2et_c(ConstSpiceChar * date,
                       SpiceDouble * et)

    cdef void sxform_c(ConstSpiceChar * fromstring,
                       ConstSpiceChar * tostring,
                       SpiceDouble      et,
                       SpiceDouble      xform[6][6])
    
    # U
    cdef void utc2et_c(ConstSpiceChar * utcstr, SpiceDouble * et)
