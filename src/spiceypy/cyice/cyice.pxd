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

    # A

    cdef void azlcpo_c(ConstSpiceChar    * method,
                       ConstSpiceChar    * target,
                       SpiceDouble         et,
                       ConstSpiceChar    * abcorr,
                       SpiceBoolean        azccw,
                       SpiceBoolean        elplsz,
                       ConstSpiceDouble[3] obspos,
                       ConstSpiceChar    * obsctr,
                       ConstSpiceChar    * obsref,
                       SpiceDouble[6]      azlsta,
                       SpiceDouble       * lt)

    cdef void azlrec_c(SpiceDouble    range,
                       SpiceDouble    az,
                       SpiceDouble    el,
                       SpiceBoolean   azccw,
                       SpiceBoolean   elplsz,
                       SpiceDouble[3] rectan)

    # B
    cdef SpiceDouble b1900_c()

    cdef SpiceDouble b1950_c()

    #C

    cdef void ckgp_c(SpiceInt            inst,
                     SpiceDouble         sclkdp,
                     SpiceDouble         tol,
                     ConstSpiceChar    * ref,
                     SpiceDouble[3][3]   cmat,
                     SpiceDouble       * clkout,
                     SpiceBoolean      * found)


    cdef void ckgpav_c(SpiceInt            inst,
                       SpiceDouble         sclkdp,
                       SpiceDouble         tol,
                       ConstSpiceChar    * ref,
                       SpiceDouble[3][3]   cmat,
                       SpiceDouble[3]      av,
                       SpiceDouble       * clkout,
                       SpiceBoolean      * found)

    cdef SpiceDouble clight_c()

    cdef void conics_c(ConstSpiceDouble[8]  elts,
                       SpiceDouble          et,
                       SpiceDouble[6]       state)

    cdef void convrt_c(SpiceDouble      x,
                       ConstSpiceChar * inunit,
                       ConstSpiceChar * outunit,
                       SpiceDouble    * y)

    cdef void cyllat_c(SpiceDouble    r,
                       SpiceDouble    clon,
                       SpiceDouble    z,
                       SpiceDouble *  radius,
                       SpiceDouble *  lon,
                       SpiceDouble *  lat)

    cdef void cylrec_c(SpiceDouble    r,
                       SpiceDouble    clon,
                       SpiceDouble    z,
                       SpiceDouble[3] rectan)

    cdef void cylsph_c(SpiceDouble    r,
                       SpiceDouble    clon,
                       SpiceDouble    z,
                       SpiceDouble *  radius,
                       SpiceDouble *  colat,
                       SpiceDouble *  slon)

    #D
    # deltet

    cdef void deltet_c(SpiceDouble      epoch,
                       ConstSpiceChar * eptype,
                       SpiceDouble    * delta)

    cdef SpiceDouble dpr_c()

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

    cdef void evsgp4_c(SpiceDouble            et,
                       ConstSpiceDouble[8]    geophs,
                       ConstSpiceDouble[10]   elems,
                       SpiceDouble[6]         state)

    #F
    cdef SpiceBoolean failed_c()

    cdef void fovray_c(ConstSpiceChar   *  inst,
                       ConstSpiceDouble[3] raydir,
                       ConstSpiceChar   *  rframe,
                       ConstSpiceChar   *  abcorr,
                       ConstSpiceChar   *  obsrvr,
                       SpiceDouble      *  et,
                       SpiceBoolean     *  visibl)

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

    cdef void georec_c(SpiceDouble    lon,
                       SpiceDouble    lat,
                       SpiceDouble    alt,
                       SpiceDouble    re,
                       SpiceDouble    f,
                       SpiceDouble[3] rectan)

    cdef void getelm_c(SpiceInt      frstyr,
                       SpiceInt      lineln,
                       const void  * lines,
                       SpiceDouble * epoch,
                       SpiceDouble * elems)

    cdef void getmsg_c(ConstSpiceChar * option,
                       SpiceInt         msglen,
                       SpiceChar      * msg)

    #H

    cdef SpiceDouble halfpi_c()

    #I

    cdef void illumf_c(ConstSpiceChar      * method,
                       ConstSpiceChar      * target,
                       ConstSpiceChar      * ilusrc,
                       SpiceDouble           et,
                       ConstSpiceChar      * fixref,
                       ConstSpiceChar      * abcorr,
                       ConstSpiceChar      * obsrvr,
                       ConstSpiceDouble[3]   spoint,
                       SpiceDouble         * trgepc,
                       SpiceDouble[3]        srfvec,
                       SpiceDouble         * phase,
                       SpiceDouble         * incdnc,
                       SpiceDouble         * emissn,
                       SpiceBoolean        * visibl,
                       SpiceBoolean        * lit)

    cdef void illumg_c(ConstSpiceChar      * method,
                       ConstSpiceChar      * target,
                       ConstSpiceChar      * ilusrc,
                       SpiceDouble           et,
                       ConstSpiceChar      * fixref,
                       ConstSpiceChar      * abcorr,
                       ConstSpiceChar      * obsrvr,
                       ConstSpiceDouble[3]   spoint,
                       SpiceDouble         * trgepc,
                       SpiceDouble[3]        srfvec,
                       SpiceDouble         * phase,
                       SpiceDouble         * incdnc,
                       SpiceDouble         * emissn)

    cdef void ilumin_c(ConstSpiceChar      * method,
                       ConstSpiceChar      * target,
                       SpiceDouble           et,
                       ConstSpiceChar      * fixref,
                       ConstSpiceChar      * abcorr,
                       ConstSpiceChar      * obsrvr,
                       ConstSpiceDouble[3]   spoint,
                       SpiceDouble         * trgepc,
                       SpiceDouble[3]        srfvec,
                       SpiceDouble         * phase,
                       SpiceDouble         * incdnc,
                       SpiceDouble         * emissn)


    #J

    cdef SpiceDouble j1900_c()

    cdef SpiceDouble j1950_c()

    cdef SpiceDouble j2000_c()

    cdef SpiceDouble j2100_c()

    cdef SpiceDouble jyear_c()

    #K

    #L

    cdef void latcyl_c(SpiceDouble    radius,
                       SpiceDouble    lon,
                       SpiceDouble    lat,
                       SpiceDouble *  r,
                       SpiceDouble *  clon,
                       SpiceDouble *  z )

    cdef void latrec_c(SpiceDouble    radius,
                       SpiceDouble    lon,
                       SpiceDouble    lat,
                       SpiceDouble[3] rectan)

    cdef void latsph_c(SpiceDouble    radius,
                       SpiceDouble    lon,
                       SpiceDouble    lat,
                       SpiceDouble *  rho,
                       SpiceDouble *  colat,
                       SpiceDouble *  slon)

    cdef void limbpt_c(ConstSpiceChar      * method,
                       ConstSpiceChar      * target,
                       SpiceDouble           et,
                       ConstSpiceChar      * fixref,
                       ConstSpiceChar      * abcorr,
                       ConstSpiceChar      * corloc,
                       ConstSpiceChar      * obsrvr,
                       ConstSpiceDouble[3]   refvec,
                       SpiceDouble           rolstp,
                       SpiceInt              ncuts,
                       SpiceDouble           schstp,
                       SpiceDouble           soltol,
                       SpiceInt              maxn,
                       SpiceInt            * npts,
                       void                * points,
                       SpiceDouble         * epochs,
                       void                * trmvcs)

    cdef SpiceDouble lspcn_c(ConstSpiceChar * body,
                             SpiceDouble      et,
                             ConstSpiceChar * abcorr)

    #M

    #N

    #O

    cdef void occult_c(ConstSpiceChar * targ1,
                       ConstSpiceChar * shape1,
                       ConstSpiceChar * frame1,
                       ConstSpiceChar * targ2,
                       ConstSpiceChar * shape2,
                       ConstSpiceChar * frame2,
                       ConstSpiceChar * abcorr,
                       ConstSpiceChar * obsrvr,
                       SpiceDouble      et,
                       SpiceInt       * ocltid)

    cdef void oscelt_c(ConstSpiceDouble[6] state,
                       SpiceDouble         et,
                       SpiceDouble         mu,
                       SpiceDouble[8]      elts)

    #P

    cdef void pgrrec_c(ConstSpiceChar * body,
                       SpiceDouble      lon,
                       SpiceDouble      lat,
                       SpiceDouble      alt,
                       SpiceDouble      re,
                       SpiceDouble      f,
                       SpiceDouble[3]   rectan)

    cdef SpiceDouble phaseq_c(SpiceDouble       et,
                              ConstSpiceChar  * target,
                              ConstSpiceChar  * illmn,
                              ConstSpiceChar  * obsrvr,
                              ConstSpiceChar  * abcorr)

    cdef SpiceDouble pi_c()

    cdef void pxform_c(ConstSpiceChar *  fromstring,
                       ConstSpiceChar *  tostring,
                       SpiceDouble       et,
                       SpiceDouble[3][3] xform)

    #Q
    cdef void qcktrc_c(SpiceInt    tracelen,
                       SpiceChar * trace)

    #R
    cdef void radrec_c(SpiceDouble range,
                       SpiceDouble ra,
                       SpiceDouble dec,
                       SpiceDouble[3] rectan)

    cdef void recazl_c(ConstSpiceDouble[3] rectan,
                       SpiceBoolean        azccw,
                       SpiceBoolean        elplsz,
                       SpiceDouble       * range,
                       SpiceDouble       * az,
                       SpiceDouble       * el)

    cdef void reccyl_c(ConstSpiceDouble[3]  rectan,
                       SpiceDouble        * r,
                       SpiceDouble        * clon,
                       SpiceDouble        * z)

    cdef void recgeo_c(ConstSpiceDouble[3]  rectan,
                       SpiceDouble          re,
                       SpiceDouble          f,
                       SpiceDouble        * lon,
                       SpiceDouble        * lat,
                       SpiceDouble        * alt)

    cdef void reclat_c(ConstSpiceDouble[3] rectan,
                       SpiceDouble       * radius,
                       SpiceDouble       * lon,
                       SpiceDouble       * lat)

    cdef void recpgr_c(ConstSpiceChar   * body,
                       SpiceDouble[3]     rectan,
                       SpiceDouble        re,
                       SpiceDouble        f,
                       SpiceDouble      * lon,
                       SpiceDouble      * lat,
                       SpiceDouble      * alt)

    cdef void recrad_c(ConstSpiceDouble[3] rectan,
                       SpiceDouble       * range,
                       SpiceDouble       * ra,
                       SpiceDouble       * dec)

    cdef void recsph_c(ConstSpiceDouble[3]  rectan,
                       SpiceDouble        * r,
                       SpiceDouble        * colat,
                       SpiceDouble        * slon)

    cdef void reset_c()

    cdef SpiceDouble rpd_c()

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
                      SpiceChar     * sclkch)

    cdef void scs2e_c(SpiceInt          sc,
                      ConstSpiceChar  * sclkch,
                      SpiceDouble     * et)

    cdef void sct2e_c(SpiceInt       sc,
                      SpiceDouble    sclkdp,
                      SpiceDouble  * et)

    cdef SpiceDouble spd_c()

    cdef void sphcyl_c(SpiceDouble   radius,
                       SpiceDouble   colat,
                       SpiceDouble   slon,
                       SpiceDouble * r,
                       SpiceDouble * clon,
                       SpiceDouble * z)

    cdef void sphlat_c(SpiceDouble   r,
                       SpiceDouble   colat,
                       SpiceDouble   slon,
                       SpiceDouble * radius,
                       SpiceDouble * lon,
                       SpiceDouble * lat)

    cdef void sphrec_c(SpiceDouble    r,
                       SpiceDouble    colat,
                       SpiceDouble    slon,
                       SpiceDouble[3] rectan)

    cdef void spkez_c(SpiceInt         target,
                      SpiceDouble      epoch,
                      ConstSpiceChar * frame,
                      ConstSpiceChar * abcorr,
                      SpiceInt         observer,
                      SpiceDouble[6]   state,
                      SpiceDouble    * lt)

    cdef void spkezp_c(SpiceInt         targ,
                       SpiceDouble      et,
                       ConstSpiceChar * ref,
                       ConstSpiceChar * abcorr,
                       SpiceInt         obs,
                       SpiceDouble[3]   ptarg,
                       SpiceDouble    * lt)

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
                       SpiceDouble          * lt)

    cdef void spkpvn_c(SpiceInt             handle,
                       ConstSpiceDouble[5]  descr,
                       SpiceDouble          et,
                       SpiceInt           * ref,
                       SpiceDouble[6]       state,
                       SpiceInt           * center)

    cdef void spkssb_c(SpiceInt           targ,
                       SpiceDouble        et,
                       ConstSpiceChar   * ref,
                       SpiceDouble[6]     starg)

    cdef void spkgeo_c(SpiceInt          targ,
                       SpiceDouble       et,
                       ConstSpiceChar  * ref,
                       SpiceInt          obs,
                       SpiceDouble[6]    state,
                       SpiceDouble     * lt)

    cdef void spkgps_c(SpiceInt           targ,
                       SpiceDouble        et,
                       ConstSpiceChar   * ref,
                       SpiceInt           obs,
                       SpiceDouble[3]     pos,
                       SpiceDouble      * lt)

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
                       SpiceDouble          * lt)

    cdef void spkcvt_c(ConstSpiceDouble[6]   trgsta,
                       SpiceDouble           trgepc,
                       ConstSpiceChar      * trgctr,
                       ConstSpiceChar      * trgref,
                       SpiceDouble           et,
                       ConstSpiceChar      * outref,
                       ConstSpiceChar      * refloc,
                       ConstSpiceChar      * abcorr,
                       ConstSpiceChar      * obsrvr,
                       SpiceDouble[6]        state,
                       SpiceDouble         * lt)

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
                       SpiceBoolean        * found)

    cdef void srfrec_c(SpiceInt      body,
                       SpiceDouble   lon,
                       SpiceDouble   lat,
                       SpiceDouble[3]   rectan)

    cdef void subpnt_c(ConstSpiceChar * method,
                       ConstSpiceChar * target,
                       SpiceDouble      et,
                       ConstSpiceChar * fixref,
                       ConstSpiceChar * abcorr,
                       ConstSpiceChar * obsrvr,
                       SpiceDouble[3]   spoint,
                       SpiceDouble    * trgepc,
                       SpiceDouble[3]   srfvec)

    cdef void subslr_c(ConstSpiceChar * method,
                       ConstSpiceChar * target,
                       SpiceDouble      et,
                       ConstSpiceChar * fixref,
                       ConstSpiceChar * abcorr,
                       ConstSpiceChar * obsrvr,
                       SpiceDouble[3]   spoint,
                       SpiceDouble    * trgepc,
                       SpiceDouble[3]   srfvec)

    cdef void str2et_c(ConstSpiceChar * date,
                       SpiceDouble * et)

    cdef void sxform_c(ConstSpiceChar *  fromstring,
                       ConstSpiceChar *  tostring,
                       SpiceDouble       et,
                       SpiceDouble[6][6] xform)
    # T

    cdef void tangpt_c(ConstSpiceChar    * method,
                       ConstSpiceChar    * target,
                       SpiceDouble         et,
                       ConstSpiceChar    * fixref,
                       ConstSpiceChar    * abcorr,
                       ConstSpiceChar    * corloc,
                       ConstSpiceChar    * obsrvr,
                       ConstSpiceChar    * dref,
                       ConstSpiceDouble[3] dvec,
                       SpiceDouble[3]      tanpt,
                       SpiceDouble       * alt,
                       SpiceDouble       * range,
                       SpiceDouble[3]      srfpt,
                       SpiceDouble       * trgepc,
                       SpiceDouble[3]      srfvec)


    cdef void termpt_c(ConstSpiceChar      * method,
                       ConstSpiceChar      * ilusrc,
                       ConstSpiceChar      * target,
                       SpiceDouble           et,
                       ConstSpiceChar      * fixref,
                       ConstSpiceChar      * abcorr,
                       ConstSpiceChar      * corloc,
                       ConstSpiceChar      * obsrvr,
                       ConstSpiceDouble[3]   refvec,
                       SpiceDouble           rolstp,
                       SpiceInt              ncuts,
                       SpiceDouble           schstp,
                       SpiceDouble           soltol,
                       SpiceInt              maxn,
                       SpiceInt            * npts,
                       void                * points,
                       SpiceDouble         * epochs,
                       void                * trmvcs)


    cdef void timout_c(SpiceDouble        et,
                       ConstSpiceChar   * pictur,
                       SpiceInt           outlen,
                       ConstSpiceChar   * output)


    cdef SpiceDouble trgsep_c(SpiceDouble      et,
                              ConstSpiceChar * targ1,
                              ConstSpiceChar * shape1,
                              ConstSpiceChar * frame1,
                              ConstSpiceChar * targ2,
                              ConstSpiceChar * shape2,
                              ConstSpiceChar * frame2,
                              ConstSpiceChar * obsrvr,
                              ConstSpiceChar * abcorr)

    cdef SpiceDouble twopi_c()


    cdef SpiceDouble tyear_c()

    # U

    cdef SpiceDouble unitim_c(SpiceDouble      epoch,
                              ConstSpiceChar * insys,
                              ConstSpiceChar * outsys)

    cdef void unload_c(ConstSpiceChar * file)

    cdef void utc2et_c(ConstSpiceChar * utcstr, 
                       SpiceDouble * et)

    # X 

    cdef void xfmsta_c(ConstSpiceDouble[6]  istate,
                       ConstSpiceChar     * icosys,
                       ConstSpiceChar     * ocosys,
                       ConstSpiceChar     * body,
                       SpiceDouble[6]       ostate)