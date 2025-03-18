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

    #ckgp 
    #ckgpav

    cdef void convrt_c(SpiceDouble      x,
                       ConstSpiceChar * inunit,
                       ConstSpiceChar * outunit,
                       SpiceDouble    * y)

    #D
    # deltet

    cdef void deltet_c(SpiceDouble      epoch,
                       ConstSpiceChar * eptype,
                       SpiceDouble    * delta )


    #E

    cdef void et2lst_c(SpiceDouble        et,
                       SpiceInt           body,
                       SpiceDouble        lon,
                       ConstSpiceChar   * type,
                       SpiceInt           timlen,
                       SpiceInt           ampmlen,
                       SpiceInt         * hr,
                       SpiceInt         * mn,
                       SpiceInt         * sc,
                       SpiceChar        * time,
                       SpiceChar        * ampm )

    cdef void et2utc_c(SpiceDouble      et,
                       ConstSpiceChar * format,
                       SpiceInt         prec,
                       SpiceInt         lenout,
                       SpiceChar      * utcstr)
    
    cdef void etcal_c(SpiceDouble   et,
                      SpiceInt      callen,
                      SpiceChar   * calstr)

    #L 

    cdef SpiceDouble lspcn_c(ConstSpiceChar   * body,
                             SpiceDouble        et,
                             ConstSpiceChar   * abcorr )


    #F 
    cdef SpiceBoolean failed_c()
    
    # fovray

    # fovtrg

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
    
    cdef void scdecd_c(SpiceInt        sc,
                       SpiceDouble     sclkdp,
                       SpiceInt        scllen,
                       SpiceChar     * sclkch)

    cdef void scencd_c(SpiceInt         sc,
                        ConstSpiceChar * sclkch,
                        SpiceDouble    * sclkdp)

    cdef void str2et_c(ConstSpiceChar * date,
                       SpiceDouble * et)

    cdef void sce2c_c(SpiceInt        sc,
                      SpiceDouble     et,
                      SpiceDouble   * sclkdp)

    cdef void sce2s_c(SpiceInt        sc,
                      SpiceDouble     et,
                      SpiceInt        scllen,
                      SpiceChar     * sclkch  )

    cdef void scs2e_c(SpiceInt          sc,
                      ConstSpiceChar  * sclkch,
                      SpiceDouble     * et      )

    cdef void sct2e_c(SpiceInt       sc,
                      SpiceDouble    sclkdp,
                      SpiceDouble  * et     )

    cdef void spkez_c(SpiceInt         target,
                      SpiceDouble      epoch,
                      ConstSpiceChar * frame,
                      ConstSpiceChar * abcorr,
                      SpiceInt         observer,
                      SpiceDouble[6]   state,
                      SpiceDouble    * lt)

    cdef void spkezp_c(SpiceInt            targ,
                       SpiceDouble         et,
                       ConstSpiceChar    * ref,
                       ConstSpiceChar    * abcorr,
                       SpiceInt            obs,
                       SpiceDouble[3]      ptarg,
                       SpiceDouble       * lt        )
    
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
                       SpiceDouble[3]   ptarg,
                       SpiceDouble * lt)

    cdef void sxform_c(ConstSpiceChar * fromstring,
                       ConstSpiceChar * tostring,
                       SpiceDouble      et,
                       SpiceDouble[6][6]      xform)
    #spkapo	
    #spkpvn	
    #spkssb	
    #spkgeo	
    #spkgps	
    #spkcpo	
    #spkcpt	
    #spkcvo	
    #spkcvt
    cdef void sincpt_c(ConstSpiceChar      * method,
                       ConstSpiceChar      * target,
                       SpiceDouble           et,
                       ConstSpiceChar      * fixref,
                       ConstSpiceChar      * abcorr,
                       ConstSpiceChar      * obsrvr,
                       ConstSpiceChar      * dref,
                       ConstSpiceDouble[3]   dvec,
                       SpiceDouble[3]        spoint,
                       SpiceDouble         * trgepc,
                       SpiceDouble[3]        srfvec,
                       SpiceBoolean        * found       )

    cdef void subpnt_c(ConstSpiceChar       * method,
                       ConstSpiceChar       * target,
                       SpiceDouble            et,
                       ConstSpiceChar       * fixref,
                       ConstSpiceChar       * abcorr,
                       ConstSpiceChar       * obsrvr,
                       SpiceDouble[3]         spoint,
                       SpiceDouble          * trgepc,
                       SpiceDouble[3]         srfvec)


    cdef void subslr_c(ConstSpiceChar       * method,
                       ConstSpiceChar       * target,
                       SpiceDouble            et,
                       ConstSpiceChar       * fixref,
                       ConstSpiceChar       * abcorr,
                       ConstSpiceChar       * obsrvr,
                       SpiceDouble[3]         spoint,
                       SpiceDouble          * trgepc,
                       SpiceDouble[3]         srfvec)


    # T

    cdef void tangpt_c(ConstSpiceChar    * method,
                       ConstSpiceChar    * target,
                       SpiceDouble         et,
                       ConstSpiceChar    * fixref,
                       ConstSpiceChar    * abcorr,
                       ConstSpiceChar    * corloc,
                       ConstSpiceChar    * obsrvr,
                       ConstSpiceChar    * dref,
                       ConstSpiceDouble[3]    dvec,
                       SpiceDouble[3]         tanpt,
                       SpiceDouble       * alt,
                       SpiceDouble       * range,
                       SpiceDouble[3]         srfpt,
                       SpiceDouble       * trgepc,
                       SpiceDouble[3]         srfvec)


    cdef void timout_c(SpiceDouble        et,
                       ConstSpiceChar   * pictur,
                       SpiceInt           outlen,
                       ConstSpiceChar   * output)


    cdef SpiceDouble trgsep_c(SpiceDouble         et,
                              ConstSpiceChar    * targ1,
                              ConstSpiceChar    * shape1,
                              ConstSpiceChar    * frame1,
                              ConstSpiceChar    * targ2,
                              ConstSpiceChar    * shape2,
                              ConstSpiceChar    * frame2,
                              ConstSpiceChar    * obsrvr,
                              ConstSpiceChar    * abcorr)

    # U

    cdef SpiceDouble unitim_c(SpiceDouble        epoch,
                              ConstSpiceChar   * insys,
                              ConstSpiceChar   * outsys)

    cdef void unload_c(ConstSpiceChar * file)

    cdef void utc2et_c(ConstSpiceChar * utcstr, SpiceDouble * et)


