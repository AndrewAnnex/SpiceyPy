# cython: language_level = 3
# cython: embedsignature = True
# cython: c_string_type = unicode
# cython: c_string_encoding = ascii
# cython: cdivision = True
# cython: profile = False
# cython: linetrace = False
# cython: warn.unused = True
# cython: warn.maybe_uninitialized = True
# cython: warn.multiple_declarators = True
# cython: show_performance_hints = True
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION

"""
The MIT License (MIT)

Copyright (c) [2015-2025] [Andrew Annex]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

cdef extern from "SpiceUsr.h" nogil:
    ctypedef char SpiceChar
    ctypedef int SpiceInt
    ctypedef double SpiceDouble
    ctypedef const char ConstSpiceChar
    ctypedef const int ConstSpiceInt
    ctypedef const double ConstSpiceDouble

    # Bool
    ctypedef enum SpiceBoolean:
        SPICEFALSE = 0
        SPICETRUE  = 1
    # const SpiceBoolean
    ctypedef const SpiceBoolean ConstSpiceBoolean

    # Cells
    # TODO I was overriding stuff in here with this enum! rename each kind to a unique name
    # cdef enum SpiceCellDataType:
    #     char = 0,
    #     double = 1,
    #     int = 2,
    #     time = 3,
    #     bool = 4

    # cdef struct _SpiceCell:
    #     SpiceCellDataType dtype
    #     SpiceInt           length
    #     SpiceInt           size
    #     SpiceInt           card
    #     SpiceBoolean       isSet
    #     SpiceBoolean       adjust
    #     SpiceBoolean       init
    #     void * base
    #     void * data

    # ctypedef _SpiceCell SpiceCell
    # ctypedef const SpiceCell ConstSpiceCell

    # start of function defs
    cdef SpiceDouble b1900_c()

    cdef SpiceDouble b1950_c()

    #C 

    cdef void ckgp_c(SpiceInt            inst,
                     SpiceDouble         sclkdp,
                     SpiceDouble         tol,
                     ConstSpiceChar    * ref,
                     SpiceDouble[3][3]   cmat,
                     SpiceDouble       * clkout,
                     SpiceBoolean      * found      )


    cdef void ckgpav_c(SpiceInt            inst,
                       SpiceDouble         sclkdp,
                       SpiceDouble         tol,
                       ConstSpiceChar    * ref,
                       SpiceDouble[3][3]   cmat,
                       SpiceDouble[3]      av,
                       SpiceDouble       * clkout,
                       SpiceBoolean      * found      )


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
    
    cdef void fovray_c(ConstSpiceChar   * inst,
                       ConstSpiceDouble[3]   raydir,
                       ConstSpiceChar   * rframe,
                       ConstSpiceChar   * abcorr,
                       ConstSpiceChar   * obsrvr,
                       SpiceDouble      * et,
                       SpiceBoolean     * visibl  )
    
    cdef void fovtrg_c(ConstSpiceChar   * inst,
                       ConstSpiceChar   * target,
                       ConstSpiceChar   * tshape,
                       ConstSpiceChar   * tframe,
                       ConstSpiceChar   * abcorr,
                       ConstSpiceChar   * obsrvr,
                       SpiceDouble      * et,
                       SpiceBoolean     * visibl)


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
                       SpiceDouble[6]   state,
                       SpiceDouble    * lt)

    cdef void spkpos_c(ConstSpiceChar * targ,
                       SpiceDouble      et,
                       ConstSpiceChar * ref,
                       ConstSpiceChar * abcorr,
                       ConstSpiceChar * obs,
                       SpiceDouble[3]   ptarg,
                       SpiceDouble * lt)

    cdef void spkapo_c(SpiceInt               targ,
                       SpiceDouble            et,
                       ConstSpiceChar       * ref,
                       ConstSpiceDouble[6]    sobs,
                       ConstSpiceChar       * abcorr,
                       SpiceDouble[3]         ptarg,
                       SpiceDouble          * lt        )
	
    cdef void spkpvn_c(SpiceInt             handle,
                       ConstSpiceDouble[5]  descr,
                       SpiceDouble          et,
                       SpiceInt           * ref,
                       SpiceDouble[6]       state,
                       SpiceInt           * center    )	

    cdef void spkssb_c(SpiceInt           targ,
                       SpiceDouble        et,
                       ConstSpiceChar   * ref,
                       SpiceDouble[6]     starg )

    cdef void spkgeo_c(SpiceInt          targ,
                       SpiceDouble       et,
                       ConstSpiceChar  * ref,
                       SpiceInt          obs,
                       SpiceDouble[6]    state,
                       SpiceDouble     * lt       )
	
    cdef void spkgps_c(SpiceInt           targ,
                       SpiceDouble        et,
                       ConstSpiceChar   * ref,
                       SpiceInt           obs,
                       SpiceDouble[3]     pos,
                       SpiceDouble      * lt     )

    cdef void spkcpo_c(ConstSpiceChar       * target,
                       SpiceDouble            et,
                       ConstSpiceChar       * outref,
                       ConstSpiceChar       * refloc,
                       ConstSpiceChar       * abcorr,
                       ConstSpiceDouble[3]    obspos,
                       ConstSpiceChar       * obsctr,
                       ConstSpiceChar       * obsref,
                       SpiceDouble[6]         state,
                       SpiceDouble          * lt)
    
    cdef void spkcpt_c(ConstSpiceDouble[3]    trgpos,
                       ConstSpiceChar       * trgctr,
                       ConstSpiceChar       * trgref,
                       SpiceDouble            et,
                       ConstSpiceChar       * outref,
                       ConstSpiceChar       * refloc,
                       ConstSpiceChar       * abcorr,
                       ConstSpiceChar       * obsrvr,
                       SpiceDouble[6]         state,
                       SpiceDouble          * lt)
    
    cdef void spkcvo_c(ConstSpiceChar       * target,
                       SpiceDouble            et,
                       ConstSpiceChar       * outref,
                       ConstSpiceChar       * refloc,
                       ConstSpiceChar       * abcorr,
                       ConstSpiceDouble[6]    obssta,
                       SpiceDouble            obsepc,
                       ConstSpiceChar       * obsctr,
                       ConstSpiceChar       * obsref,
                       SpiceDouble[6]         state,
                       SpiceDouble          * lt         )
    
    cdef void spkcvt_c(ConstSpiceDouble[6]    trgsta,
                       SpiceDouble            trgepc,
                       ConstSpiceChar       * trgctr,
                       ConstSpiceChar       * trgref,
                       SpiceDouble            et,
                       ConstSpiceChar       * outref,
                       ConstSpiceChar       * refloc,
                       ConstSpiceChar       * abcorr,
                       ConstSpiceChar       * obsrvr,
                       SpiceDouble[6]         state,
                       SpiceDouble          * lt         )

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

    cdef void str2et_c(ConstSpiceChar * date,
                       SpiceDouble * et)

    cdef void sxform_c(ConstSpiceChar * fromstring,
                       ConstSpiceChar * tostring,
                       SpiceDouble      et,
                       SpiceDouble[6][6]      xform)
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


