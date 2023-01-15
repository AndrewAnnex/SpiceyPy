# cython: language_level = 3
# cython: embedsignature = True
# cython: c_string_type = unicode
# cython: c_string_encoding = utf-8
"""
main cython wrapper code

defs are visible to python
cdef's are not visible to python and are pure c, use for inner loops
cpdefs are both, really only useful for recursion

"""

cdef extern from "Python.h":
    object PyString_FromStringAndSize(char *, Py_ssize_t)
    char *PyString_AsString(object)


# okay for some reason making a pxd file causes cython to fail
# todo maybe okay to just use "*" for header file
# grab externs from SpiceZpr.h
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
    # A
    cdef void appndc_c(ConstSpiceChar * item,
                       SpiceCell * cell)

    cdef void appndd_c(SpiceDouble item,
                       SpiceCell * cell)

    cdef void appndi_c(SpiceInt item,
                       SpiceCell * cell)

    cdef void axisar_c(ConstSpiceDouble     axis   [3],
                       SpiceDouble          angle,
                       SpiceDouble          r      [3][3])

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
                       SpiceDouble * lt)

    cdef void  azlrec_c(SpiceDouble         range,
                        SpiceDouble         az,
                        SpiceDouble         el,
                        SpiceBoolean        azccw,
                        SpiceBoolean        elplsz,
                        SpiceDouble         rectan [3])
    # B
    cdef SpiceBoolean      badkpv_c(ConstSpiceChar *caller,
                                    ConstSpiceChar *name,
                                    ConstSpiceChar *comp,
                                    SpiceInt             size,
                                    SpiceInt             divby,
                                    SpiceChar            type)

    cdef void              bltfrm_c(SpiceInt             frmcls,
                                    SpiceCell * idset)

    cdef void              bodc2n_c(SpiceInt             code,
                                    SpiceInt             namelen,
                                    SpiceChar * name,
                                    SpiceBoolean * found)

    cdef void              bodc2s_c(SpiceInt             code,
                                    SpiceInt             lenout,
                                    SpiceChar * name)

    cdef void              boddef_c(ConstSpiceChar * name,
                                    SpiceInt             code)

    cdef SpiceBoolean      bodfnd_c(SpiceInt             body,
                                    ConstSpiceChar * item)

    cdef void              bodn2c_c(ConstSpiceChar * name,
                                    SpiceInt * code,
                                    SpiceBoolean * found)

    cdef void              bods2c_c(ConstSpiceChar * name,
                                    SpiceInt * code,
                                    SpiceBoolean * found)

    cdef void              bodvar_c(SpiceInt             body,
                                    ConstSpiceChar * item,
                                    SpiceInt * dim,
                                    SpiceDouble * values)

    cdef void              bodvcd_c(SpiceInt             body,
                                    ConstSpiceChar * item,
                                    SpiceInt             maxn,
                                    SpiceInt * dim,
                                    SpiceDouble * values)

    cdef void              bodvrd_c(ConstSpiceChar * body,
                                    ConstSpiceChar * item,
                                    SpiceInt             maxn,
                                    SpiceInt * dim,
                                    SpiceDouble * values)

    cdef SpiceDouble       brcktd_c(SpiceDouble          number,
                                    SpiceDouble          end1,
                                    SpiceDouble          end2)

    cdef SpiceInt          brckti_c(SpiceInt             number,
                                    SpiceInt             end1,
                                    SpiceInt             end2)

    cdef SpiceInt          bschoc_c(ConstSpiceChar * value,
                                    SpiceInt             ndim,
                                    SpiceInt             lenvals,
                                    const void * array,
                                    ConstSpiceInt * order)

    cdef SpiceInt          bschoi_c(SpiceInt             value,
                                    SpiceInt             ndim,
                                    ConstSpiceInt * array,
                                    ConstSpiceInt * order)

    cdef SpiceInt          bsrchc_c(ConstSpiceChar * value,
                                    SpiceInt             ndim,
                                    SpiceInt             lenvals,
                                    const void * array)

    cdef SpiceInt          bsrchd_c(SpiceDouble          value,
                                    SpiceInt             ndim,
                                    ConstSpiceDouble * array)

    cdef SpiceInt          bsrchi_c(SpiceInt             value,
                                    SpiceInt             ndim,
                                    ConstSpiceInt * array)
    cdef double b1900_c()

    cdef double b1950_c()

    #C 

    #F 
    cdef void furnsh_c(ConstSpiceChar * file)

    #S
    cdef void spkez_c(SpiceInt            target,
                      SpiceDouble         epoch,
                      ConstSpiceChar * frame,
                      ConstSpiceChar * abcorr,
                      SpiceInt            observer,
                      SpiceDouble         state[6],
                      SpiceDouble * lt)

    cdef void spkezp_c(SpiceInt            targ,
                        SpiceDouble         et,
                        ConstSpiceChar * ref,
                        ConstSpiceChar * abcorr,
                        SpiceInt            obs,
                        SpiceDouble         ptarg[3],
                        SpiceDouble * lt)

    cdef void spkezr_c(ConstSpiceChar * target,
                        SpiceDouble      epoch,
                        ConstSpiceChar * frame,
                        ConstSpiceChar * abcorr,
                        ConstSpiceChar * observer,
                        SpiceDouble state[6],
                        SpiceDouble * lt)


cpdef double b1900() nogil:
    return b1900_c()

cpdef double b1950() nogil:
    return b1950_c()

cpdef furnsh(str file):
    furnsh_c(file)
    
cpdef spkezr(str target, double epoch, str frame, str abcorr, str observer):
    cdef double[6] state = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    cdef double lt = 0.0
    spkezr_c(target, epoch, frame, abcorr, observer, state, &lt)
    return state, lt
